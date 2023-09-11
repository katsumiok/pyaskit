import unittest
import openai
from unittest.mock import patch, Mock
import json
import time
import random
import pyaskit.dialog as dialog
import pyaskit
import pyaskit.types as t
from pyaskit.llm_openai import (
    chat_with_retry,
)


class TestChatWithRetry(unittest.TestCase):
    @patch("openai.ChatCompletion.create")
    def test_success_on_first_try(self, mock_create):
        mock_create.return_value = "mock_response"

        response = chat_with_retry("test_model", "test_messages")

        self.assertEqual(response, "mock_response")
        mock_create.assert_called_once_with(
            model="test_model", messages="test_messages"
        )

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

        self.assertEqual(
            str(context.exception), "Failed to get response after 2 attempts"
        )
