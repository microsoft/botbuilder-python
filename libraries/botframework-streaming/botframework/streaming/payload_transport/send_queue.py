# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import traceback

from asyncio import Queue, ensure_future
from typing import Awaitable, Callable


class SendQueue:
    def __init__(self, action: Callable[[object], Awaitable], timeout: int = 30):
        self._action = action

        self._queue = Queue()
        self._timeout_seconds = timeout

        # TODO: this have to be abstracted so can remove asyncio dependency
        ensure_future(self._process())

    def post(self, item: object):
        self._post_internal(item)

    def _post_internal(self, item: object):
        self._queue.put_nowait(item)

    async def _process(self):
        while True:
            try:
                while True:
                    item = await self._queue.get()
                    try:
                        await self._action(item)
                    except Exception:
                        traceback.print_exc()
                    finally:
                        self._queue.task_done()
            except Exception:
                # AppInsights.TrackException(e)
                traceback.print_exc()
                return
