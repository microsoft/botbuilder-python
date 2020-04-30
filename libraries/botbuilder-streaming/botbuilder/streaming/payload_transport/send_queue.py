# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from queue import Queue
from typing import Awaitable, Callable
from threading import Event, Lock, Semaphore

import asyncio


class SendQueue:
    def __init__(self, action: Callable[[object], Awaitable], timeout: int = 30):
        self._action = action

        self._queue = Queue()
        self._timeout_seconds = timeout

        # TODO: this have to be abstracted so can remove asyncio dependency
        loop = asyncio.get_event_loop()
        loop.create_task(self._process())

    def post(self, item: object):
        self._post_internal(item)

    def _post_internal(self, item: object):
        self._queue.put(item)

    async def _process(self):
        while True:
            try:
                while True:
                    item = self._queue.get()
                    if not item:
                        break
                    try:
                        await self._action(item)
                    except Exception:
                        # AppInsights.TrackException(e)
                        pass
                    finally:
                        self._queue.task_done()
            except Exception:
                # AppInsights.TrackException(e)
                pass
