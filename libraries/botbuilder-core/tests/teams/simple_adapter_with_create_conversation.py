# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import unittest
from typing import List, Tuple, Awaitable, Callable
from botbuilder.core import BotAdapter, TurnContext
from botbuilder.schema import (
    Activity,
    ConversationReference,
    ResourceResponse,
    ConversationParameters,
)


class SimpleAdapterWithCreateConversation(BotAdapter):
    # pylint: disable=unused-argument

    def __init__(
        self,
        call_on_send=None,
        call_on_update=None,
        call_on_delete=None,
        call_create_conversation=None,
    ):
        super(SimpleAdapterWithCreateConversation, self).__init__()
        self.test_aux = unittest.TestCase("__init__")
        self._call_on_send = call_on_send
        self._call_on_update = call_on_update
        self._call_on_delete = call_on_delete
        self._call_create_conversation = call_create_conversation

    async def delete_activity(
        self, context: TurnContext, reference: ConversationReference
    ):
        self.test_aux.assertIsNotNone(
            reference, "SimpleAdapter.delete_activity: missing reference"
        )
        if self._call_on_delete is not None:
            self._call_on_delete(reference)

    async def send_activities(
        self, context: TurnContext, activities: List[Activity]
    ) -> List[ResourceResponse]:
        self.test_aux.assertIsNotNone(
            activities, "SimpleAdapter.delete_activity: missing reference"
        )
        self.test_aux.assertTrue(
            len(activities) > 0,
            "SimpleAdapter.send_activities: empty activities array.",
        )

        if self._call_on_send is not None:
            self._call_on_send(activities)
        responses = []

        for activity in activities:
            responses.append(ResourceResponse(id=activity.id))

        return responses

    async def create_conversation(
        self,
        reference: ConversationReference,
        logic: Callable[[TurnContext], Awaitable] = None,
        conversation_parameters: ConversationParameters = None,
    ) -> Tuple[ConversationReference, str]:
        if self._call_create_conversation is not None:
            self._call_create_conversation()
        ref = ConversationReference(activity_id="new_conversation_id")
        return (ref, "reference123")

    async def update_activity(self, context: TurnContext, activity: Activity):
        self.test_aux.assertIsNotNone(
            activity, "SimpleAdapter.update_activity: missing activity"
        )
        if self._call_on_update is not None:
            self._call_on_update(activity)

        return ResourceResponse(activity.id)

    async def process_request(self, activity, handler):
        context = TurnContext(self, activity)
        return await self.run_pipeline(context, handler)
