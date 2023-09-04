import unittest
import openai
from unittest.mock import patch, Mock
import json
import time
import random
import pyaskit.gpt as gpt
import pyaskit
import pyaskit.types as t
from pyaskit.gpt import chat_with_retry, make_question, make_answer, make_example_chat_messages, make_qa, parse_code

class TestGPT(unittest.TestCase):
    def test_extract_json(self):
        self.assertEqual(1, gpt.extract_json("...```json 1 ```..."))
        data = gpt.extract_json('{ "reason": "ok"}')
        self.assertEqual("ok", data["reason"])
        # expect raise
        with self.assertRaises(ValueError):
            gpt.extract_json("...```json 1 ```...```")
            

class TestChatWithRetry(unittest.TestCase):
    @patch("openai.ChatCompletion.create")
    def test_success_on_first_try(self, mock_create):
        mock_create.return_value = "mock_response"

        response = chat_with_retry("test_model", "test_messages")
        
        self.assertEqual(response, "mock_response")
        mock_create.assert_called_once_with(model="test_model", messages="test_messages")

    @patch("openai.ChatCompletion.create")
    def test_success_on_second_try(self, mock_create):
        # Setup mock to raise an exception on the first call and succeed on the second
        mock_create.side_effect = [openai.error.APIError("test_error"), "mock_response"]

        response = chat_with_retry("test_model", "test_messages")

        self.assertEqual(response, "mock_response")
        self.assertEqual(mock_create.call_count, 2)

    @patch("openai.ChatCompletion.create")
    def test_max_retries_exceeded(self, mock_create):
        mock_create.side_effect = openai.error.APIError("test_error")

        with self.assertRaises(Exception) as context:
            chat_with_retry("test_model", "test_messages", 2)

        self.assertEqual(str(context.exception), "Failed to get response after 2 attempts")


class TestMakeQuestion(unittest.TestCase):

    def test_with_empty_varMap(self):
        task = "What is the capital of France?"
        varMap = {}
        expected_output = "What is the capital of France?\n\n"
        self.assertEqual(make_question(task, varMap), expected_output)

    def test_with_non_empty_varMap_single_item(self):
        task = "Compute the area."
        varMap = {"radius": 5}
        expected_output = "Compute the area.\n\nwhere\n  'radius' = 5"
        self.assertEqual(make_question(task, varMap), expected_output)

    def test_with_non_empty_varMap_multiple_items(self):
        task = "Calculate the total price."
        varMap = {"price": 50.5, "quantity": 3}
        # Note: Dictionary ordering is maintained from Python 3.7 onwards. 
        # If you're using <3.7, this test might be inconsistent.
        expected_output = (
            "Calculate the total price.\n\n"
            "where\n  'price' = 50.5\n  'quantity' = 3"
        )
        self.assertEqual(make_question(task, varMap), expected_output)

    def test_with_special_characters(self):
        task = "Print the message."
        varMap = {"message": "Hello, world!"}
        expected_output = (
            "Print the message.\n\n"
            "where\n  'message' = \"Hello, world!\""
        )
        self.assertEqual(make_question(task, varMap), expected_output)

class TestMakeAnswer(unittest.TestCase):

    def test_make_answer_with_string(self):
        output = "Hello, World!"
        expected_response = f"""```json
{{
    "reason": "...",
    "answer": {json.dumps(output)}
}}
```"""
        self.assertEqual(make_answer(output), expected_response)

    def test_make_answer_with_number(self):
        output = 12345
        expected_response = f"""```json
{{
    "reason": "...",
    "answer": {json.dumps(output)}
}}
```"""
        self.assertEqual(make_answer(output), expected_response)

    def test_make_answer_with_boolean(self):
        output = True
        expected_response = f"""```json
{{
    "reason": "...",
    "answer": {json.dumps(output)}
}}
```"""
        self.assertEqual(make_answer(output), expected_response)

    def test_make_answer_with_list(self):
        output = [1, 2, 3]
        expected_response = f"""```json
{{
    "reason": "...",
    "answer": {json.dumps(output)}
}}
```"""
        self.assertEqual(make_answer(output), expected_response)

    def test_make_answer_with_dict(self):
        output = {"key": "value", "number": 42}
        expected_response = f"""```json
{{
    "reason": "...",
    "answer": {json.dumps(output)}
}}
```"""
        self.assertEqual(make_answer(output), expected_response)
        


class TestMakeExampleChatMessages(unittest.TestCase):

    @patch("pyaskit.gpt.make_qa")
    def test_make_example_chat_messages(self, mock_make_qa):
        # Mocking the make_qa function to return a fixed output
        mock_make_qa.return_value = ("mock_question", "mock_answer")

        task = "mock_task"
        examples = [
            {"input": "input1", "output": "output1"},
            {"input": "input2", "output": "output2"}
        ]
        
        result = make_example_chat_messages(task, examples)

        expected_result = [
            {"role": "user", "content": "mock_question"},
            {"role": "assistant", "content": "mock_answer"},
            {"role": "user", "content": "mock_question"},
            {"role": "assistant", "content": "mock_answer"}
        ]

        self.assertEqual(result, expected_result)


class TestMakeQA(unittest.TestCase):
    
    @patch("pyaskit.gpt.make_question")  # Replace 'your_module_name' with the name of your module.
    @patch("pyaskit.gpt.make_answer")    # Replace 'your_module_name' with the name of your module.
    def test_make_qa(self, mock_make_answer, mock_make_question):
        # Setup mock returns
        mock_make_question.return_value = "mocked_question"
        mock_make_answer.return_value = "mocked_answer"

        task = "test_task"
        example = {"input": "test_input", "output": "test_output"}

        # Call the function
        q, a = make_qa(task, example)

        # Assertions
        self.assertEqual(q, "mocked_question")
        self.assertEqual(a, "mocked_answer")

        mock_make_question.assert_called_once_with(task, example["input"])
        mock_make_answer.assert_called_once_with(example["output"])
        

class TestParseCode(unittest.TestCase):
    def test_valid_python_code_extraction(self):
        # Test the extraction of python code
        text = """
Some text before the code.
```python
def hello():
    print("Hello, World!")
```
Some text after the code.
"""
        extracted_code = parse_code(text, t.CodeType("python"))
        expected_code = 'def hello():\n    print("Hello, World!")'
        self.assertEqual(extracted_code.strip(), expected_code)

    def test_invalid_python_code_extraction(self):
        # Test the extraction of python code
        text = """
Some text.
"""
        with self.assertRaises(ValueError):
            parse_code(text, t.CodeType("python"))





if __name__ == '__main__':
    unittest.main()
