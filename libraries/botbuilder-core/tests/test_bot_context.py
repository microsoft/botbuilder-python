# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import pytest

from botbuilder.schema import Activity
from botbuilder.core import BotContext, TestAdapter

ACTIVITY = Activity(id='1', type='message', text='test')
ADAPTER = TestAdapter(None)


class TestBotContext:
    def test_should_create_context_with_request_and_adapter(self):
        context = BotContext(ADAPTER, ACTIVITY)

    def test_should_not_create_context_without_request(self):
        try:
            context = BotContext(ADAPTER, None)
        except TypeError:
            pass
        except Exception as e:
            raise e

    def test_should_not_create_context_without_adapter(self):
        try:
            context = BotContext(None, ACTIVITY)
        except TypeError:
            pass
        except Exception as e:
            raise e

    def test_should_create_context_with_older_context(self):
        context = BotContext(ADAPTER, ACTIVITY)
        new_context = BotContext(context)

    def test_copy_to_should_copy_all_references(self):
        old_adapter = TestAdapter(None)
        old_activity = Activity(id='2', type='message', text='test copy')
        old_context = BotContext(old_adapter, old_activity)
        old_context.responded = True

        async def send_activities_handler(context, next_handler):
            pass

        old_context.on_send_activities(send_activities_handler)

        adapter = TestAdapter(None)
        new_context = BotContext(adapter, ACTIVITY)
        old_context.copy_to(new_context)

        assert new_context.adapter == old_adapter
        assert new_context.activity == old_activity
        assert new_context.responded is True
        assert len(new_context._on_send_activities) == 1
        assert len(new_context._on_update_activity) == 0
        assert len(new_context._on_delete_activity) == 0

    def test_responded_should_be_automatically_set_to_False(self):
        context = BotContext(ADAPTER, ACTIVITY)
        assert context.responded is False

    def test_should_be_able_to_set_responded_to_True(self):
        context = BotContext(ADAPTER, ACTIVITY)
        assert context.responded is False
        context.responded = True
        assert context.responded

    def test_should_not_be_able_to_set_responded_to_False(self):
        context = BotContext(ADAPTER, ACTIVITY)
        try:
            context.responded = False
        except ValueError:
            pass
        except Exception as e:
            raise e
