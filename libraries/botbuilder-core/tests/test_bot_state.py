# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
import aiounittest
from unittest.mock import MagicMock

from botbuilder.core import TurnContext, BotState, MemoryStorage, UserState
from botbuilder.core.adapters import TestAdapter
from botbuilder.schema import Activity

from .test_utilities import TestUtilities

RECEIVED_MESSAGE = Activity(type='message',
                            text='received')
STORAGE_KEY = 'stateKey'


def cached_state(context, state_key):
    cached = context.services.get(state_key)
    return cached['state'] if cached is not None else None


def key_factory(context):
    assert context is not None
    return STORAGE_KEY


class TestBotState(aiounittest.AsyncTestCase):
    storage = MemoryStorage()
    adapter = TestAdapter()
    context = TurnContext(adapter, RECEIVED_MESSAGE)
    middleware = BotState(storage, key_factory)

    
    def test_state_empty_name(self):
        #Arrange
        dictionary = {}
        user_state = UserState(MemoryStorage(dictionary))

        #Act
        with self.assertRaises(TypeError) as _:
            user_state.create_property('')
    
    def test_state_none_name(self):
        #Arrange
        dictionary = {}
        user_state = UserState(MemoryStorage(dictionary))

        #Act
        with self.assertRaises(TypeError) as _:
            user_state.create_property(None)
    
    async def test_storage_not_called_no_changes(self):
        """Verify storage not called when no changes are made"""
        # Mock a storage provider, which counts read/writes
        dictionary = {}
        mock_storage = MemoryStorage(dictionary)
        mock_storage.write = MagicMock(return_value= 1)
        mock_storage.read = MagicMock(return_value= 1)

        # Arrange
        user_state = UserState(mock_storage)
        context = TestUtilities.create_empty_context()

        # Act
        propertyA = user_state.create_property("propertyA")
        self.assertEqual(mock_storage.write.call_count, 0)
        await user_state.save_changes(context)
        await propertyA.set(context, "hello")
        self.assertEqual(mock_storage.read.call_count, 1)       # Initial save bumps count
        self.assertEqual(mock_storage.write.call_count, 0)       # Initial save bumps count
        await propertyA.set(context, "there")
        self.assertEqual(mock_storage.write.call_count, 0)       # Set on property should not bump
        await user_state.save_changes(context)
        self.assertEqual(mock_storage.write.call_count, 1)       # Explicit save should bump
        valueA = await propertyA.get(context)
        self.assertEqual("there", valueA)
        self.assertEqual(mock_storage.write.call_count, 1)       # Gets should not bump
        await user_state.save_changes(context)
        self.assertEqual(mock_storage.write.call_count, 1)
        await propertyA.DeleteAsync(context)   # Delete alone no bump
        self.assertEqual(mock_storage.write.call_count, 1)
        await user_state.save_changes(context)  # Save when dirty should bump
        self.assertEqual(mock_storage.write.call_count, 2)
        self.assertEqual(mock_storage.read.call_count, 1)
        await user_state.save_changes(context)  # Save not dirty should not bump
        self.assertEqual(mock_storage.write.call_count, 2)
        self.assertEqual(mock_storage.read.call_count, 1)
