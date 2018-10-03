# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import asyncio
from botbuilder.core import TurnContext, ConversationState, UserState, MemoryStorage
from botbuilder.schema import ActivityTypes

from adapter import ConsoleAdapter

import urllib3
from time import strftime
import json

# Create adapter
adapter = ConsoleAdapter()

# Create MemoryStorage, UserState and ConversationState
memory = MemoryStorage()
# Commented out user_state because it's not being used.
# user_state = UserState(memory)
conversation_state = ConversationState(memory)

# Register both State middleware on the adapter.
# Commented out user_state because it's not being used.
# adapter.use(user_state)
adapter.use(conversation_state)

def is_bridge_opened():
    time = strftime('%H')+strftime('%M')
    if 0000 <= time >= 1030 or 1100 <= time >= 1200 or 1300 <= time >= 1330 or 1430 <= time >= 1600 or 1730 <= time >= 2359:
        return True
    else:
        return False


class Weather():
    http = urllib3.PoolManager()

    def get_weather(self):
        r = self.http.request('GET', 'http://api.openweathermap.org/data/2.5/weather?q=Gizycko,pl&APPID=0ef268648751f483a62fd90feb04c5eb&units=metric')
        r = json.loads(r.data.decode('utf-8'))
        self.status = r["weather"][0]["description"]
        self.temp = int(r["main"]["temp"])
        self.wind_speed = r["wind"]["speed"]

async def logic(context: TurnContext):
    if context.activity.type == ActivityTypes.message:
        state = await conversation_state.get(context)

        # If our conversation_state already has the 'count' attribute, increment state.count by 1
        # Otherwise, initialize state.count with a value of 1
        if hasattr(state, 'count'):
            state.count += 1
        else:
            state.count = 1
        if "weather" in context.activity.text.lower():
            w = Weather()
            w.get_weather()
        
            await context.send_activity(f'{state.count}: Outside it is {w.status}, {w.temp}°C. Wind is blowing {w.wind_speed} m/s')
        elif "bridge" in context.activity.text.lower():
            if is_bridge_opened:
                await context.send_activity(f'{state.count}: The bridge is currently opened.')
            else:
                await context.send_activity(f'{state.count}: The bridge is currently closed.')
        else:
            await context.send_activity(f'{state.count}: I cannot help you.')
    else:
        await context.send_activity(f'[{context.activity.type} event detected]')

loop = asyncio.get_event_loop()

if __name__ == "__main__":
    try:
        # Greet user
        print("Hi... Welcome in Gizycko. Hope you like it.")

        loop.run_until_complete(adapter.process_activity(logic))
    except KeyboardInterrupt:
        pass
    finally:
        loop.stop()
        loop.close()
