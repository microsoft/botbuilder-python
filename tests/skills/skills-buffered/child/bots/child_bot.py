# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, TurnContext


class ChildBot(ActivityHandler):
    async def on_message_activity(self, turn_context: TurnContext):
        await turn_context.send_activity("child: activity (1)")
        await turn_context.send_activity("child: activity (2)")
        await turn_context.send_activity("child: activity (3)")
        await turn_context.send_activity(f"child: {turn_context.activity.text}")
