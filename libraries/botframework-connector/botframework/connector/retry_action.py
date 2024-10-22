# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import asyncio
import random


class RetryAction:
    @staticmethod
    async def run_async(
        task, max_retries=10, initial_delay=500, retry_exception_handler=None
    ):
        delay = initial_delay
        current_retry_count = 1
        errors = []
        while current_retry_count <= max_retries:
            try:
                return await task(current_retry_count)
            except Exception as ex:
                errors.append(ex)
                if (
                    retry_exception_handler
                    and retry_exception_handler(ex, current_retry_count) == 429
                ):
                    await RetryAction._wait_with_jitter(delay)
                    delay *= 2  # Exponential backoff
                current_retry_count += 1
        raise Exception(f"Failed after {max_retries} retries", errors)

    @staticmethod
    async def _wait_with_jitter(delay):
        jitter = random.uniform(0.8, 1.2)
        await asyncio.sleep(jitter * (delay / 1000.0))
