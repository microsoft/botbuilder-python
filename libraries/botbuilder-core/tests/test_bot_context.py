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

    def test_copy_to_should_copy_references(self):
        old_adapter = TestAdapter(None)
        old_activity = Activity(id='2', type='message', text='test copy')
        old_context = BotContext(old_adapter, old_activity)
        old_context.responded = True

        adapter = TestAdapter(None)
        new_context = BotContext(adapter, ACTIVITY)
        old_context.copy_to(new_context)

        assert new_context.adapter == old_adapter
        assert new_context.activity == old_activity
        assert new_context.responded is True

    def test_should_not_be_able_to_set_responded_to_True(self):
        context = BotContext(ADAPTER, ACTIVITY)
        context.responded = True

    def test_should_not_be_able_to_set_responded_to_False(self):
        context = BotContext(ADAPTER, ACTIVITY)
        try:
            context.responded = False
        except ValueError:
            pass
        except Exception as e:
            raise e
