# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.


import asyncio


class MiddlewareSet(object):
    """
    A set of `Middleware` plugins. The set itself is middleware so you can easily package up a set
    of middleware that can be composed into a bot with a single `bot.use(mySet)` call or even into
    another middleware set using `set.use(mySet)`.
    """
    def __init__(self):
        self._middleware = []
        self._loop = asyncio.get_event_loop()

    def middleware(self):
        """
        Returns the underlying array of middleware.
        :return:
        """
        return self._middleware

    def use(self, *middleware):
        """
        Registers middleware plugin(s) with the bot or set.
        :param middleware :
        :return:
        """
        self._middleware.extend(middleware)
        return self

    async def context_created(self, context):
        async def call_middleware(middleware_set):
            for middleware in middleware_set:
                if hasattr(middleware, 'context_created') and callable(middleware.context_created):
                    await asyncio.ensure_future(middleware.context_created(context))
                elif 'context_created' in middleware and callable(middleware['context_created']):
                    await asyncio.ensure_future(middleware['context_created'](context))
        return await asyncio.ensure_future(call_middleware(self._middleware[0:]))

    async def receive_activity(self, context):
        async def call_middleware(middleware_set):
            for middleware in middleware_set:
                if hasattr(middleware, 'receive_activity') and callable(middleware.receive_activity):
                    await asyncio.ensure_future(middleware.receive_activity(context))
                elif 'receive_activity' in middleware and callable(middleware['receive_activity']):
                    await asyncio.ensure_future(middleware['receive_activity'](context))
        return await asyncio.ensure_future(call_middleware(self._middleware[0:]))

    async def send_activity(self, context, activities):
        async def call_middleware(middleware_set):
            for middleware in middleware_set:
                if hasattr(middleware, 'send_activity') and callable(middleware.send_activity):
                    await asyncio.ensure_future(middleware.send_activity(context, activities))
                elif 'send_activity' in middleware and callable(middleware['send_activity']):
                    await asyncio.ensure_future(middleware['send_activity'](context, activities))
        return await asyncio.ensure_future(call_middleware(self._middleware[0:]))
