# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from abc import ABC, abstractmethod
from typing import List, Callable
from botbuilder.schema import Activity, ConversationReference

from .bot_context import BotContext
from .middleware_set import Middleware, MiddlewareSet


class BotAdapter(ABC):
    def __init__(self):
        self._middleware = MiddlewareSet()

    @abstractmethod
    async def send_activity(self, activities: List[Activity]):
        raise NotImplementedError()

    @abstractmethod
    async def update_activity(self, activity: Activity):
        raise NotImplementedError()

    @abstractmethod
    async def delete_activity(self, reference: ConversationReference):
        raise NotImplementedError()

    def use(self, middleware):
        self._middleware.use(middleware)

    async def run_middleware(self, context: BotContext, logic: Callable=None):
        return await self._middleware.run(context, logic)
        # revocable has not been implemented.
