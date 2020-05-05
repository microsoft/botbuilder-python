# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import traceback

from queue import Queue
from typing import Awaitable, Callable
from threading import Event, Lock, Semaphore

import asyncio
import threading


class SendQueue:
    def __init__(self, action: Callable[[object], Awaitable], timeout: int = 30):
        self._action = action

        self._queue = Queue()
        self._timeout_seconds = timeout

        # TODO: this have to be abstracted so can remove asyncio dependency
        def schedule_task():
            loop = asyncio.new_event_loop()
            loop.run_until_complete(self._process())

        new_thread = threading.Thread(target=schedule_task, args=())
        new_thread.daemon = True
        new_thread.start()

    def post(self, item: object):
        self._post_internal(item)

    def _post_internal(self, item: object):
        self._queue.put(item)

    async def _process(self):
        while True:
            try:
                while True:
                    await asyncio.sleep(1)
                    item = self._queue.get(block=False)
                    try:
                        await self._action(item)
                    except Exception:
                        # AppInsights.TrackException(e)
                        pass
                    finally:
                        self._queue.task_done()
            except Exception:
                # AppInsights.TrackException(e)
                # traceback.print_exc()
                pass
