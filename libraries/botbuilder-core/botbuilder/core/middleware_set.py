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

    def use(self, *middleware: Iterable[Middleware]):
        """
        Registers middleware plugin(s) with the bot or set.
        :param middleware :
        :return:
        """
        for plugin in middleware:
            if isinstance(plugin, Callable):
                self._middleware.append(plugin)
            elif isinstance(plugin, object) and hasattr(plugin, 'on_process_request'):
                self._middleware.append(lambda context, logic: plugin.on_process_request(context, logic))
            else:
                raise TypeError('MiddlewareSet.use(): invalid plugin type being added.')
        return self

    async def on_process_request(self, context, logic: Callable):
        await self.run(context, logic)

    async def run(self, context: BotContext, logic: Callable):
        handlers = self._middleware[0:]

        async def run_next(i: int):
            try:
                if i < len(handlers):
                    await run_next(handlers[i](context, run_next(i+1)))
                else:
                    return await logic(context)
            except BaseException as e:
                raise e

        return await run_next(0)
