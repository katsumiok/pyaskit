import unittest
from unittest.mock import patch, Mock
import json
import pyaskit.dialog as dialog
import pyaskit.types as t
from pyaskit.dialog import (
    make_question,
    make_answer,
    make_example_chat_messages,
    make_qa,
    parse_code,
    parse,
    ask_and_parse,
)


class TestGPT(unittest.TestCase):
    def test_extract_json(self):
        self.assertEqual(1, dialog.extract_json("...```json 1 ```..."))
        data = dialog.extract_json('{ "reason": "ok"}')
        self.assertEqual("ok", data["reason"])
        # expect raise
        with self.assertRaises(ValueError):
            dialog.extract_json("...```json 1 ```...```")


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
            "Calculate the total price.\n\n" "where\n  'price' = 50.5\n  'quantity' = 3"
        )
        self.assertEqual(make_question(task, varMap), expected_output)

    def test_with_special_characters(self):
        task = "Print the message."
        varMap = {"message": "Hello, world!"}
        expected_output = (
            "Print the message.\n\n" "where\n  'message' = \"Hello, world!\""
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
    @patch("pyaskit.dialog.make_qa")
    def test_make_example_chat_messages(self, mock_make_qa):
        # Mocking the make_qa function to return a fixed output
        mock_make_qa.return_value = ("mock_question", "mock_answer")

        task = "mock_task"
        examples = [
            {"input": "input1", "output": "output1"},
            {"input": "input2", "output": "output2"},
        ]

        result = make_example_chat_messages(task, examples)

        expected_result = [
            {"role": "user", "content": "mock_question"},
            {"role": "assistant", "content": "mock_answer"},
            {"role": "user", "content": "mock_question"},
            {"role": "assistant", "content": "mock_answer"},
        ]

        self.assertEqual(result, expected_result)


class TestMakeQA(unittest.TestCase):
    @patch(
        "pyaskit.dialog.make_question"
    )  # Replace 'your_module_name' with the name of your module.
    @patch(
        "pyaskit.dialog.make_answer"
    )  # Replace 'your_module_name' with the name of your module.
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


class TestParseFunction(unittest.TestCase):
    # Test successful parsing for CodeType
    def test_parse_code_success(self):
        text = """```python
print("Hello, world!")
```"""
        return_type = t.CodeType("python")
        result, _ = parse(text, return_type)
        self.assertEqual(result, 'print("Hello, world!")')

    # Test failure due to missing code block for CodeType
    def test_parse_code_failure(self):
        text = 'print("Hello, world!")'
        return_type = t.CodeType("python")
        with self.assertRaises(ValueError):
            parse(text, return_type)

    # Test successful parsing for JSON data
    def test_parse_json_success(self):
        text = """```json
{
    "reason": "Test Reason",
    "answer": "Hello, world!"
}
```"""
        return_type = t.StringType()
        data, reason = parse(text, return_type)
        self.assertEqual(data, "Hello, world!")
        self.assertEqual(reason, "Test Reason")

    # Test JSON parsing failure due to missing `answer` field
    def test_parse_json_missing_answer(self):
        text = """```json
{
    "reason": "Test Reason"
}
```"""
        return_type = t.StringType()
        with self.assertRaises(ValueError):
            parse(text, return_type)

    # Test JSON parsing failure due to wrong type in `answer` field
    def test_parse_json_wrong_type(self):
        text = """```json
{
    "reason": "Test Reason",
    "answer": 1234
}
```"""
        return_type = t.StringType()
        with self.assertRaises(ValueError):
            parse(text, return_type)


#
# class TestAskAndParse(unittest.TestCase):
#     # Mock the openai.ChatCompletion.create response
#     mock_response = Mock()
#     mock_response.choices = [Mock()]
#     mock_response.choices[0].message = Mock()

#     @patch("pyaskit.dialog.parse", return_value=("parsed_answer", "parsed_reason"))
#     def test_successful_chat(self, mock_parse):
#         self.mock_response.choices[0].message.content = "mock_content"

#         data, reason, errors, completion = ask_and_parse(
#             None, [], lambda messages: ("mock_content", self.mock_response)
#         )

#         self.assertEqual(data, "parsed_answer")
#         self.assertEqual(reason, "parsed_reason")
#         self.assertEqual(errors, [])
#         mock_parse.assert_called_once_with("mock_content", None)


# More test cases can be added

if __name__ == "__main__":
    unittest.main()
