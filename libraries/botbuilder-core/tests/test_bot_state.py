# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
import aiounittest
from unittest.mock import MagicMock

from botbuilder.core import TurnContext, BotState, MemoryStorage, UserState
from botbuilder.core.adapters import TestAdapter
from botbuilder.schema import Activity

from test_utilities import TestUtilities

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

        async def mock_write_result(self):
            return
        async def mock_read_result(self):
            return {}

        mock_storage = MemoryStorage(dictionary)
        mock_storage.write = MagicMock(side_effect= mock_write_result)
        mock_storage.read = MagicMock(side_effect= mock_read_result)

        # Arrange
        user_state = UserState(mock_storage)
        context = TestUtilities.create_empty_context()

        # Act
        property_a = user_state.create_property("property_a")
        self.assertEqual(mock_storage.write.call_count, 0)
        await user_state.save_changes(context)
        await property_a.set(context, "hello")
        self.assertEqual(mock_storage.read.call_count, 1)       # Initial save bumps count
        self.assertEqual(mock_storage.write.call_count, 0)       # Initial save bumps count
        await property_a.set(context, "there")
        self.assertEqual(mock_storage.write.call_count, 0)       # Set on property should not bump
        await user_state.save_changes(context)
        self.assertEqual(mock_storage.write.call_count, 1)       # Explicit save should bump
        value_a = await property_a.get(context)
        self.assertEqual("there", value_a)
        self.assertEqual(mock_storage.write.call_count, 1)       # Gets should not bump
        await user_state.save_changes(context)
        self.assertEqual(mock_storage.write.call_count, 1)
        await property_a.delete(context)   # Delete alone no bump
        self.assertEqual(mock_storage.write.call_count, 1)
        await user_state.save_changes(context)  # Save when dirty should bump
        self.assertEqual(mock_storage.write.call_count, 2)
        self.assertEqual(mock_storage.read.call_count, 1)
        await user_state.save_changes(context)  # Save not dirty should not bump
        self.assertEqual(mock_storage.write.call_count, 2)
        self.assertEqual(mock_storage.read.call_count, 1)
    
    async def test_state_set_no_load(self):
        """Should be able to set a property with no Load"""
        # Arrange
        dictionary = {}
        user_state = UserState(MemoryStorage(dictionary))
        context = TestUtilities.create_empty_context()

        # Act
        property_a = user_state.create_property("property_a")
        await property_a.set(context, "hello")
    
    
    
    async def test_state_multiple_loads(self):
        """Should be able to load multiple times"""
        # Arrange
        dictionary = {}
        user_state = UserState(MemoryStorage(dictionary))
        context = TestUtilities.create_empty_context()

        # Act
        property_a = user_state.create_property("property_a")
        await user_state.load(context)
        await user_state.load(context)

    
    async def test_State_GetNoLoadWithDefault(self):
        """Should be able to get a property with no Load and default"""
        # Arrange
        dictionary = {}
        user_state = UserState(MemoryStorage(dictionary))
        context = TestUtilities.create_empty_context()

        # Act
        property_a = user_state.create_property("property_a")
        value_a = await property_a.get(context, lambda : "Default!")
        self.assertEqual("Default!", value_a)

    
    
    async def test_State_GetNoLoadNoDefault(self):
        """Cannot get a string with no default set"""
        # Arrange
        dictionary = {}
        user_state = UserState(MemoryStorage(dictionary))
        context = TestUtilities.create_empty_context()

        # Act
        property_a = user_state.create_property("property_a")
        value_a = await property_a.get(context)

        # Assert
        self.assertIsNone(value_a)

    
    async def test_State_POCO_NoDefault(self):
        """Cannot get a POCO with no default set"""
        # Arrange
        dictionary = {}
        user_state = UserState(MemoryStorage(dictionary))
        context = TestUtilities.create_empty_context()

        # Act
        test_property = user_state.create_property("test")
        value = await test_property.get(context)

        # Assert
        self.assertIsNone(value)

    
    
    async def test_State_bool_NoDefault(self):
        """Cannot get a bool with no default set"""
        # Arange
        dictionary = {}
        user_state = UserState(MemoryStorage(dictionary))
        context = TestUtilities.create_empty_context()

        # Act
        test_property = user_state.create_property("test")
        value = await test_property.get(context)

        # Assert
        self.assertFalse(value)

    """
    TODO: Check if default int functionality is needed
    async def test_State_int_NoDefault(self):
        ""Cannot get a int with no default set""
        # Arrange
        dictionary = {}
        user_state = UserState(MemoryStorage(dictionary))
        context = TestUtilities.create_empty_context()

        # Act
        test_property = user_state.create_property("test")
        value = await test_property.get(context)

        # Assert
        self.assertEqual(0, value)
    """

    
    async def test_State_SetAfterSave(self):
        """Verify setting property after save"""
        # Arrange
        dictionary = {}
        user_state = UserState(MemoryStorage(dictionary))
        context = TestUtilities.create_empty_context()

        # Act
        property_a = user_state.create_property("property-a")
        property_b = user_state.create_property("property-b")

        await user_state.load(context)
        await property_a.set(context, "hello")
        await property_b.set(context, "world")
        await user_state.save_changes(context)

        await property_a.set(context, "hello2")

    
    async def test_State_MultipleSave(self):
        """Verify multiple saves"""
        # Arrange
        dictionary = {}
        user_state = UserState(MemoryStorage(dictionary))
        context = TestUtilities.create_empty_context()

        # Act
        property_a = user_state.create_property("property-a")
        property_b = user_state.create_property("property-b")

        await user_state.load(context)
        await property_a.set(context, "hello")
        await property_b.set(context, "world")
        await user_state.save_changes(context)

        await property_a.set(context, "hello2")
        await user_state.save_changes(context)
        value_a = await property_a.get(context)
        self.assertEqual("hello2", value_a)

    
    async def test_LoadSetSave(self):
        # Arrange
        dictionary = {}
        user_state = UserState(MemoryStorage(dictionary))
        context = TestUtilities.create_empty_context()

        # Act
        property_a = user_state.create_property("property-a")
        property_b = user_state.create_property("property-b")

        await user_state.load(context)
        await property_a.set(context, "hello")
        await property_b.set(context, "world")
        await user_state.save_changes(context)

        # Assert
        obj = dictionary["EmptyContext/users/empty@empty.context.org"]
        self.assertEqual("hello", obj["property-a"])
        self.assertEqual("world", obj["property-b"])

    
    async def test_LoadSetSaveTwice(self):
        # Arrange
        dictionary = {}
        context = TestUtilities.create_empty_context()

        # Act
        user_state = UserState(MemoryStorage(dictionary))

        property_a = user_state.create_property("property-a")
        property_b = user_state.create_property("property-b")
        propertyC = user_state.create_property("property-c")

        await user_state.load(context)
        await property_a.set(context, "hello")
        await property_b.set(context, "world")
        await propertyC.set(context, "test")
        await user_state.save_changes(context)

        # Assert
        obj = dictionary["EmptyContext/users/empty@empty.context.org"]
        self.assertEqual("hello", obj["property-a"])
        self.assertEqual("world", obj["property-b"])

        # Act 2
        user_state2 = UserState(MemoryStorage(dictionary))

        property_a2 = user_state2.create_property("property-a")
        property_b2 = user_state2.create_property("property-b")

        await user_state2.load(context)
        await property_a2.set(context, "hello-2")
        await property_b2.set(context, "world-2")
        await user_state2.save_changes(context)

        # Assert 2
        obj2 = dictionary["EmptyContext/users/empty@empty.context.org"]
        self.assertEqual("hello-2", obj2["property-a"])
        self.assertEqual("world-2", obj2["property-b"])
        self.assertEqual("test", obj2["property-c"])

    
    async def test_LoadSaveDelete(self):
        # Arrange
        dictionary = {}
        context = TestUtilities.create_empty_context()

        # Act
        user_state = UserState(MemoryStorage(dictionary))

        property_a = user_state.create_property("property-a")
        property_b = user_state.create_property("property-b")

        await user_state.load(context)
        await property_a.set(context, "hello")
        await property_b.set(context, "world")
        await user_state.save_changes(context)

        # Assert
        obj = dictionary["EmptyContext/users/empty@empty.context.org"]
        self.assertEqual("hello", obj["property-a"])
        self.assertEqual("world", obj["property-b"])

        # Act 2
        user_state2 = UserState(MemoryStorage(dictionary))

        property_a2 = user_state2.create_property("property-a")
        property_b2 = user_state2.create_property("property-b")

        await user_state2.load(context)
        await property_a2.set(context, "hello-2")
        await property_b2.delete(context)
        await user_state2.save_changes(context)

        # Assert 2
        obj2 = dictionary["EmptyContext/users/empty@empty.context.org"]
        self.assertEqual("hello-2", obj2["property-a"])
        with self.assertRaises(KeyError) as _:
            obj2["property-b"]