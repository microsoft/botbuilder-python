# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from abc import ABC, abstractmethod
from typing import Iterable, Callable

from .bot_context import BotContext


class Middleware(ABC):
    @abstractmethod
    def on_process_request(self, context: BotContext, next): pass


class MiddlewareSet(Middleware):
    """
    A set of `Middleware` plugins. The set itself is middleware so you can easily package up a set
    of middleware that can be composed into a bot with a single `bot.use(mySet)` call or even into
    another middleware set using `set.use(mySet)`.
    """
    def __init__(self):
        super(MiddlewareSet, self).__init__()
        self._middleware = []

    def use(self, middleware: Middleware):
        """
        Registers middleware plugin(s) with the bot or set.
        :param middleware :
        :return:
        """
        if hasattr(middleware, 'on_process_request') and callable(middleware.on_process_request):
            self._middleware.append(middleware)
            return self
        else:
            raise TypeError('MiddlewareSet.use(): invalid middleware being added.')

    async def receive_activity(self, context: BotContext):
        await self.receive_activity_internal(context, None)

    async def on_process_request(self, context, logic):
        await self.receive_activity_internal(context, None)
        await logic()

    async def receive_activity_with_status(self, context: BotContext, callback):
        return await self.receive_activity_internal(context, callback)

    async def receive_activity_internal(self, context, callback, next_middleware_index=0):
        if next_middleware_index == len(self._middleware):
            if callback:
                return await callback(context)
            else:
                return None
        next_middleware = self._middleware[next_middleware_index]

        async def call_next_middleware():
            return await self.receive_activity_internal(context, callback, next_middleware_index+1)
        return await next_middleware.on_process_request(
            context,
            call_next_middleware
        )
