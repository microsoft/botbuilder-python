"""
Adapters used to pipe input to bot

Copyright (c) Microsoft Corporation. All rights reserved.
Licensed under the MIT License.
"""

import asyncio
import datetime
import os
import warnings
from typing import List, Callable

from botbuilder.core import MemoryStorage
from botbuilder.core.bot_adapter import BotAdapter
from botbuilder.core.turn_context import TurnContext
from botbuilder.schema import (Activity, ActivityTypes,
                               ChannelAccount, ConversationAccount,
                               ResourceResponse, ConversationReference)

from application import PAX_SETTINGS, DAX_SETTINGS
from lost_and_found.bots import PAXActivityHandler, DAXActivityHandler


class StringAdapter(BotAdapter):
    """
    Adapter to Pass Array of Strings to Bot
    """

    def __init__(self, file='string', reference: ConversationReference = None):
        super(StringAdapter, self).__init__()

        self.reference = ConversationReference(channel_id='test',
                                               user=ChannelAccount(id='user', name='User1'),
                                               bot=ChannelAccount(id='bot', name='Bot'),
                                               conversation=ConversationAccount(id='convo1', name='', is_group=False),
                                               service_url='')

        # Warn users to pass in an instance of a ConversationReference, otherwise the parameter will be ignored.
        if reference is not None and not isinstance(reference, ConversationReference):
            warnings.warn('StringAdapter: `reference` argument is not an instance of ConversationReference and will '
                          'be ignored.')
        else:
            self.reference.channel_id = getattr(reference, 'channel_id', self.reference.channel_id)
            self.reference.user = getattr(reference, 'user', self.reference.user)
            self.reference.bot = getattr(reference, 'bot', self.reference.bot)
            self.reference.conversation = getattr(reference, 'conversation', self.reference.conversation)
            self.reference.service_url = getattr(reference, 'service_url', self.reference.service_url)
            # The only attribute on self.reference without an initial value is activity_id, so if reference does not
            # have a value for activity_id, default self.reference.activity_id to None
            self.reference.activity_id = getattr(reference, 'activity_id', None)

        self._next_id = 0
        self.file = file

    async def process_activities(self, msgs, logic: Callable):
        """
        Loops through array of strings to bot

        :param msgs:
        :param logic:
        :return:
        """
        for msg in msgs:
            if msg is None:
                pass
            else:
                self._next_id += 1
                activity = Activity(text=msg,
                                    channel_id='console',
                                    from_property=ChannelAccount(id='user', name='User1'),
                                    recipient=ChannelAccount(id='bot', name='Bot'),
                                    conversation=ConversationAccount(id='Convo1'),
                                    type=ActivityTypes.message,
                                    timestamp=datetime.datetime.now(),
                                    id=str(self._next_id))

                activity = TurnContext.apply_conversation_reference(activity, self.reference, True)
                context = TurnContext(self, activity)
                print(context.get_conversation_reference(activity))

                await self.run_middleware(context, logic)

    async def send_activities(self, context: TurnContext, activities: List[Activity]):
        """
        Logs a series of activities to the console.
        :param context:
        :param activities:
        :return:
        """
        if context is None:
            raise TypeError('ConsoleAdapter.send_activities(): `context` argument cannot be None.')
        if not isinstance(activities, list):
            raise TypeError('ConsoleAdapter.send_activities(): `activities` argument must be a list.')
        if not activities:
            raise ValueError('ConsoleAdapter.send_activities(): `activities` argument cannot have a length of 0.')

        async def next_activity(i: int):
            responses = []

            file = open(self.file + "bot.out", "a")
            if i < len(activities):
                responses.append(ResourceResponse())
                activity = activities[i]

                if activity.type == 'delay':
                    await asyncio.sleep(activity.delay)
                    await next_activity(i + 1)
                elif activity.type == ActivityTypes.message:
                    if activity.attachments is not None:
                        append = '(1 attachment)' if len(activity.attachments) == 1 \
                            else f'({len(activity.attachments)} attachments)'
                        file.write(f'{activity.text} {append}' + "\n")
                    else:
                        file.write(activity.text + "\n")
                    await next_activity(i + 1)
                else:
                    file.write(f'[{activity.type}]' + "\n")
                    await next_activity(i + 1)
            else:
                return responses

        await next_activity(0)

    async def delete_activity(self, context: TurnContext, reference: ConversationReference):
        """
        Not supported for the ConsoleAdapter. Calling this method or `TurnContext.delete_activity()`
        will result an error being returned.
        :param context:
        :param reference:
        :return:
        """
        raise NotImplementedError('ConsoleAdapter.delete_activity(): not supported.')

    async def update_activity(self, context: TurnContext, activity: Activity):
        """
        Not supported for the ConsoleAdapter. Calling this method or `TurnContext.update_activity()`
        will result an error being returned.
        :param context:
        :param activity:
        :return:
        """
        raise NotImplementedError('ConsoleAdapter.update_activity(): not supported.')


MEMORY = MemoryStorage()
LOOP = asyncio.get_event_loop()


async def string_test_struc(msgs, answers, file='test'):
    """
    Structure used to test static input and output

    :param msgs: Array of User Inputs
    :param answers: Array of expected Bot Outputs
    :param file: temp file used to test async output, each test should use a different file
    """
    bot = ActivityHandler(MEMORY, PAX_SETTINGS, LOOP)
    adapter = StringAdapter(file=file)

    await adapter.process_activities(msgs, bot.on_turn)
    test_array = []
    with open(file + 'bot.out') as my_file:
        for line in my_file:
            test_array.append(line)
    try:
        i = 0
        for answer in answers:
            assert test_array[i] == answer
            i += 1
    finally:
        print("Done")
        os.remove(file + 'bot.out')


async def notify_struc(bot, client):
    """
    Test Notify Post Endpoint
    """
    url = '/api/notify/' + bot

    response = client.post(url)

    assert response.status != '201 CREATED'
