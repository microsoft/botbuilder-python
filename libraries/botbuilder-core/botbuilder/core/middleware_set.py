# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from asyncio import iscoroutinefunction
from abc import ABC, abstractmethod

from .turn_context import TurnContext


class Middleware(ABC):
    @abstractmethod
    def on_process_request(self, context: TurnContext, next): pass


class AnonymousReceiveMiddleware(Middleware):
    def __init__(self, anonymous_handler):
        if not iscoroutinefunction(anonymous_handler):
            raise TypeError('AnonymousReceiveMiddleware must be instantiated with a valid coroutine function.')
        self._to_call = anonymous_handler

    def on_process_request(self, context: TurnContext, next):
        return self._to_call(context, next)


class MiddlewareSet(Middleware):
    """
    A set of `Middleware` plugins. The set itself is middleware so you can easily package up a set
    of middleware that can be composed into a bot with a single `bot.use(mySet)` call or even into
    another middleware set using `set.use(mySet)`.
    """
    def __init__(self):
        super(MiddlewareSet, self).__init__()
        self._middleware = []

    def use(self, *middleware: Middleware):
        """
        Registers middleware plugin(s) with the bot or set.
        :param middleware :
        :return:
        """
        for (idx, m) in enumerate(middleware):
            if hasattr(m, 'on_process_request') and callable(m.on_process_request):
                self._middleware.append(m)
                return self
            else:
                raise TypeError('MiddlewareSet.use(): invalid middleware at index "%s" being added.' % idx)

    async def receive_activity(self, context: TurnContext):
        await self.receive_activity_internal(context, None)

    async def on_process_request(self, context, logic):
        await self.receive_activity_internal(context, None)
        await logic()

    async def receive_activity_with_status(self, context: TurnContext, callback):
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

        try:
            return await next_middleware.on_process_request(context,
                                                            call_next_middleware)
        except Exception as e:
            raise e