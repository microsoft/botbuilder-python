# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import asyncio
import aiounittest
from botframework.connector import RetryAction

class TestRetryAction(aiounittest.AsyncTestCase):
    def setUp(self):
        self.loop = asyncio.get_event_loop()

    def test_retry_action_fails_after_max_retries(self):
        async def failing_task(retry_count):
            raise Exception(f"error {retry_count}")

        with self.assertRaises(Exception) as context:
            self.loop.run_until_complete(
                RetryAction.run_async(failing_task, max_retries=3)
            )
        self.assertEqual(context.exception.args[0], "Failed after 3 retries")
        self.assertEqual(len(context.exception.args[1]), 3)

    def test_retry_action_retries_and_succeeds(self):
        async def task(retry_count):
            if retry_count < 3:
                raise Exception(f"error {retry_count}")
            return "success"

        result = self.loop.run_until_complete(
            RetryAction.run_async(task, max_retries=3)
        )
        self.assertEqual(result, "success")

    def test_retry_action_with_jitter_delay(self):
        async def task(retry_count):
            if retry_count < 2:
                raise Exception("retry error")
            return "success"

        async def mock_sleep(duration):
            pass

        original_sleep = asyncio.sleep
        asyncio.sleep = mock_sleep

        try:
            result = self.loop.run_until_complete(
                RetryAction.run_async(task, max_retries=3, initial_delay=100)
            )
            self.assertEqual(result, "success")
        finally:
            asyncio.sleep = original_sleep
