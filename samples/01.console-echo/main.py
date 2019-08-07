# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import asyncio
from botbuilder.core import TurnContext, ConversationState, UserState, MemoryStorage
from botbuilder.schema import ActivityTypes

from adapter import ConsoleAdapter
from bot import EchoBot

# Create adapter
adapter = ConsoleAdapter()
bot = EchoBot()

loop = asyncio.get_event_loop()

if __name__ == "__main__":
    try:
        # Greet user
        print("Hi... I'm an echobot. Whatever you say I'll echo back.")

        loop.run_until_complete(adapter.process_activity(bot.on_turn))
    except KeyboardInterrupt:
        pass
    finally:
        loop.stop()
        loop.close()
