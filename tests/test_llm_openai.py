import unittest
from unittest.mock import Mock, patch
import openai
from pyaskit.llm_openai import chat_with_retry


class TestChatWithRetry(unittest.TestCase):
    @patch('openai.ChatCompletion.create')
#    @patch('time.sleep', Mock())
#    @patch('config.get_model', Mock(return_value='some_model'))
    def test_success_on_first_attempt(self, mock_create):
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content='Hi there'))]
        mock_create.return_value = mock_response
        
        response_content, response = chat_with_retry(['Hello'])
        self.assertEqual(response_content, 'Hi there')
        self.assertEqual(response, mock_response)

    @patch('openai.ChatCompletion.create')
#    @patch('time.sleep', Mock())
#    @patch('config.get_model', Mock(return_value='some_model'))
    def test_retries_on_failure(self, mock_create):
        mock_create.side_effect = [
            openai.error.APIError('API error'),
            Mock(choices=[Mock(message=Mock(content='Hi after error'))]),
        ]
        
        response_content, response = chat_with_retry(['Hello'])
        self.assertEqual(response_content, 'Hi after error')
        self.assertEqual(mock_create.call_count, 2)

    @patch('openai.ChatCompletion.create')
#    @patch('time.sleep', Mock())
#    @patch('config.get_model', Mock(return_value='some_model'))
    def test_raises_after_max_retries(self, mock_create):
        mock_create.side_effect = openai.error.APIError('API error')
        
        with self.assertRaises(Exception) as context:
            chat_with_retry(['Hello'], max_retries=3)
        
        self.assertEqual(str(context.exception), "Failed to get response after 3 attempts")
        self.assertEqual(mock_create.call_count, 3)


if __name__ == '__main__':
    unittest.main()
