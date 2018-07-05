# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import asyncio
import inspect
from datetime import datetime
from typing import Coroutine, List
from copy import copy
from botbuilder.core import BotAdapter, TurnContext
from botbuilder.schema import (ActivityTypes, Activity, ConversationAccount,
                               ConversationReference, ChannelAccount, ResourceResponse)


class TestAdapter(BotAdapter):
    def __init__(self, logic: Coroutine=None, template: ConversationReference=None):
        """
        Creates a new TestAdapter instance.
        :param logic:
        :param template:
        """
        super(TestAdapter, self).__init__()
        self.logic = logic
        self._next_id: int = 0
        self.activity_buffer: List[Activity] = []
        self.updated_activities: List[Activity] = []
        self.deleted_activities: List[ConversationReference] = []

        self.template: Activity = Activity(
            channel_id='test',
            service_url='https://test.com',
            from_property=ChannelAccount(id='User1', name='user'),
            recipient=ChannelAccount(id='bot', name='Bot'),
            conversation=ConversationAccount(id='Convo1')
        )
        if template is not None:
            self.template.service_url = template.service_url
            self.template.conversation = template.conversation
            self.template.channel_id = template.channel_id

    async def send_activities(self, context, activities: List[Activity]):
        """
        INTERNAL: called by the logic under test to send a set of activities. These will be buffered
        to the current `TestFlow` instance for comparison against the expected results.
        :param context:
        :param activities:
        :return:
        """
        def id_mapper(activity):
            self.activity_buffer.append(activity)
            self._next_id += 1
            return ResourceResponse(id=str(self._next_id))
        """This if-else code is temporary until the BotAdapter and Bot/TurnContext are revamped."""
        if type(activities) == list:
            responses = [id_mapper(activity) for activity in activities]
        else:
            responses = [id_mapper(activities)]
        return responses

    async def delete_activity(self, context, reference: ConversationReference):
        """
        INTERNAL: called by the logic under test to delete an existing activity. These are simply
        pushed onto a [deletedActivities](#deletedactivities) array for inspection after the turn
        completes.
        :param reference:
        :return:
        """
        self.deleted_activities.append(reference)

    async def update_activity(self, context, activity: Activity):
        """
        INTERNAL: called by the logic under test to replace an existing activity. These are simply
        pushed onto an [updatedActivities](#updatedactivities) array for inspection after the turn
        completes.
        :param activity:
        :return:
        """
        self.updated_activities.append(activity)

    async def continue_conversation(self, reference, logic):
        """
        The `TestAdapter` doesn't implement `continueConversation()` and will return an error if it's
        called.
        :param reference:
        :param logic:
        :return:
        """
        raise NotImplementedError('TestAdapter.continue_conversation(): is not implemented.')

    async def receive_activity(self, activity):
        """
        INTERNAL: called by a `TestFlow` instance to simulate a user sending a message to the bot.
        This will cause the adapters middleware pipe to be run and it's logic to be called.
        :param activity:
        :return:
        """
        if type(activity) == str:
            activity = Activity(type='message', text=activity)
        # Initialize request
        request = copy(self.template)

        for key, value in vars(activity).items():
            if value is not None and key != 'additional_properties':
                setattr(request, key, value)

        if not request.type:
            request.type = ActivityTypes.message
        if not request.id:
            self._next_id += 1
            request.id = str(self._next_id)

        # Create context object and run middleware
        context = TurnContext(self, request)
        return await self.run_middleware(context, self.logic)

    async def send(self, user_says):
        """
        Sends something to the bot. This returns a new `TestFlow` instance which can be used to add
        additional steps for inspecting the bots reply and then sending additional activities.
        :param user_says:
        :return:
        """
        return TestFlow(await self.receive_activity(user_says), self)

    async def test(self, user_says, expected, description=None, timeout=None) -> 'TestFlow':
        """
        Send something to the bot and expects the bot to return with a given reply. This is simply a
        wrapper around calls to `send()` and `assertReply()`. This is such a common pattern that a
        helper is provided.
        :param user_says:
        :param expected:
        :param description:
        :param timeout:
        :return:
        """
        test_flow = await self.send(user_says)
        test_flow = await test_flow.assert_reply(expected, description, timeout)
        return test_flow

    async def tests(self, *args):
        """
        Support multiple test cases without having to manually call `test()` repeatedly. This is a
        convenience layer around the `test()`. Valid args are either lists or tuples of parameters
        :param args:
        :return:
        """
        for arg in args:
            description = None
            timeout = None
            if len(arg) >= 3:
                description = arg[2]
                if len(arg) == 4:
                    timeout = arg[3]
            await self.test(arg[0], arg[1], description, timeout)


class TestFlow(object):
    def __init__(self, previous, adapter: TestAdapter):
        """
        INTERNAL: creates a new TestFlow instance.
        :param previous:
        :param adapter:
        """
        self.previous = previous
        self.adapter = adapter

    async def test(self, user_says, expected, description=None, timeout=None) -> 'TestFlow':
        """
        Send something to the bot and expects the bot to return with a given reply. This is simply a
        wrapper around calls to `send()` and `assertReply()`. This is such a common pattern that a
        helper is provided.
        :param user_says:
        :param expected:
        :param description:
        :param timeout:
        :return:
        """
        test_flow = await self.send(user_says)
        return await test_flow.assert_reply(expected, description or f'test("{user_says}", "{expected}")', timeout)

    async def send(self, user_says) -> 'TestFlow':
        """
        Sends something to the bot.
        :param user_says:
        :return:
        """
        async def new_previous():
            nonlocal self, user_says
            if callable(self.previous):
                await self.previous()
            await self.adapter.receive_activity(user_says)

        return TestFlow(await new_previous(), self.adapter)

    async def assert_reply(self, expected, description=None, timeout=None) -> 'TestFlow':
        """
        Generates an assertion if the bots response doesn't match the expected text/activity.
        :param expected:
        :param description:
        :param timeout:
        :return:
        """
        def default_inspector(reply, description=None):
            if isinstance(expected, Activity):
                validate_activity(reply, expected)
            else:
                assert reply.type == 'message', description + f" type == {reply.type}"
                assert reply.text == expected, description + f" text == {reply.text}"

        if description is None:
            description = ''

        inspector = expected if type(expected) == 'function' else default_inspector

        async def test_flow_previous():
            nonlocal timeout
            if not timeout:
                timeout = 3000
            start = datetime.now()
            adapter = self.adapter

            async def wait_for_activity():
                nonlocal expected, timeout
                current = datetime.now()
                if (current - start).total_seconds() * 1000 > timeout:
                    if type(expected) == Activity:
                        expecting = expected.text
                    elif callable(expected):
                        expecting = inspect.getsourcefile(expected)
                    else:
                        expecting = str(expected)
                    raise RuntimeError(f'TestAdapter.assert_reply({expecting}): {description} Timed out after '
                                       f'{current - start}ms.')
                elif len(adapter.activity_buffer) > 0:
                    reply = adapter.activity_buffer.pop(0)
                    inspector(reply, description)
                else:
                    await asyncio.sleep(0.05)
                    await wait_for_activity()

            await wait_for_activity()

        return TestFlow(await test_flow_previous(), self.adapter)


def validate_activity(activity, expected) -> None:
    """
    Helper method that compares activities
    :param activity:
    :param expected:
    :return:
    """
    iterable_expected = vars(expected).items()
    for attr, value in iterable_expected:
        if value is not None and attr != 'additional_properties':
            assert value == getattr(activity, attr)
