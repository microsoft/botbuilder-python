# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from unittest.mock import MagicMock
import aiounittest

from botbuilder.core import (
    BotState,
    ConversationState,
    MemoryStorage,
    Storage,
    StoreItem,
    TurnContext,
    UserState,
)
from botbuilder.core.adapters import TestAdapter
from botbuilder.schema import Activity, ConversationAccount

from test_utilities import TestUtilities

RECEIVED_MESSAGE = Activity(type="message", text="received")
STORAGE_KEY = "stateKey"


def cached_state(context, state_key):
    cached = context.services.get(state_key)
    return cached["state"] if cached is not None else None


def key_factory(context):
    assert context is not None
    return STORAGE_KEY


class BotStateForTest(BotState):
    def __init__(self, storage: Storage):
        super().__init__(storage, f"BotState:BotState")

    def get_storage_key(self, turn_context: TurnContext) -> str:
        return f"botstate/{turn_context.activity.channel_id}/{turn_context.activity.conversation.id}/BotState"


class CustomState(StoreItem):
    def __init__(self, custom_string: str = None, e_tag: str = "*"):
        super().__init__(custom_string=custom_string, e_tag=e_tag)


class TestPocoState:
    def __init__(self, value=None):
        self.value = value


class TestBotState(aiounittest.AsyncTestCase):
    storage = MemoryStorage()
    adapter = TestAdapter()
    context = TurnContext(adapter, RECEIVED_MESSAGE)
    middleware = BotState(storage, key_factory)

    def test_state_empty_name(self):
        # Arrange
        dictionary = {}
        user_state = UserState(MemoryStorage(dictionary))

        # Act
        with self.assertRaises(TypeError) as _:
            user_state.create_property("")

    def test_state_none_name(self):
        # Arrange
        dictionary = {}
        user_state = UserState(MemoryStorage(dictionary))

        # Act
        with self.assertRaises(TypeError) as _:
            user_state.create_property(None)

    async def test_storage_not_called_no_changes(self):
        """Verify storage not called when no changes are made"""
        # Mock a storage provider, which counts read/writes
        dictionary = {}

        async def mock_write_result(self):  # pylint: disable=unused-argument
            return

        async def mock_read_result(self):  # pylint: disable=unused-argument
            return {}

        mock_storage = MemoryStorage(dictionary)
        mock_storage.write = MagicMock(side_effect=mock_write_result)
        mock_storage.read = MagicMock(side_effect=mock_read_result)

        # Arrange
        user_state = UserState(mock_storage)
        context = TestUtilities.create_empty_context()

        # Act
        property_a = user_state.create_property("property_a")
        self.assertEqual(mock_storage.write.call_count, 0)
        await user_state.save_changes(context)
        await property_a.set(context, "hello")
        self.assertEqual(mock_storage.read.call_count, 1)  # Initial save bumps count
        self.assertEqual(mock_storage.write.call_count, 0)  # Initial save bumps count
        await property_a.set(context, "there")
        self.assertEqual(
            mock_storage.write.call_count, 0
        )  # Set on property should not bump
        await user_state.save_changes(context)
        self.assertEqual(mock_storage.write.call_count, 1)  # Explicit save should bump
        value_a = await property_a.get(context)
        self.assertEqual("there", value_a)
        self.assertEqual(mock_storage.write.call_count, 1)  # Gets should not bump
        await user_state.save_changes(context)
        self.assertEqual(mock_storage.write.call_count, 1)
        await property_a.delete(context)  # Delete alone no bump
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
        user_state.create_property("property_a")
        await user_state.load(context)
        await user_state.load(context)

    async def test_state_get_no_load_with_default(self):
        """Should be able to get a property with no Load and default"""
        # Arrange
        dictionary = {}
        user_state = UserState(MemoryStorage(dictionary))
        context = TestUtilities.create_empty_context()

        # Act
        property_a = user_state.create_property("property_a")
        value_a = await property_a.get(context, lambda: "Default!")
        self.assertEqual("Default!", value_a)

    async def test_state_get_no_load_no_default(self):
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

    async def test_state_poco_no_default(self):
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

    async def test_state_bool_no_default(self):
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

    async def test_state_set_after_save(self):
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

    async def test_state_multiple_save(self):
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

    async def test_load_set_save(self):
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

    async def test_load_set_save_twice(self):
        # Arrange
        dictionary = {}
        context = TestUtilities.create_empty_context()

        # Act
        user_state = UserState(MemoryStorage(dictionary))

        property_a = user_state.create_property("property-a")
        property_b = user_state.create_property("property-b")
        property_c = user_state.create_property("property-c")

        await user_state.load(context)
        await property_a.set(context, "hello")
        await property_b.set(context, "world")
        await property_c.set(context, "test")
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

    async def test_load_save_delete(self):
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
            obj2["property-b"]  # pylint: disable=pointless-statement

    async def test_state_use_bot_state_directly(self):
        async def exec_test(context: TurnContext):
            # pylint: disable=unnecessary-lambda
            bot_state_manager = BotStateForTest(MemoryStorage())
            test_property = bot_state_manager.create_property("test")

            # read initial state object
            await bot_state_manager.load(context)

            custom_state = await test_property.get(context, lambda: CustomState())

            # this should be a 'CustomState' as nothing is currently stored in storage
            assert isinstance(custom_state, CustomState)

            # amend property and write to storage
            custom_state.custom_string = "test"
            await bot_state_manager.save_changes(context)

            custom_state.custom_string = "asdfsadf"

            # read into context again
            await bot_state_manager.load(context, True)

            custom_state = await test_property.get(context)

            # check object read from value has the correct value for custom_string
            assert custom_state.custom_string == "test"

        adapter = TestAdapter(exec_test)
        await adapter.send("start")

    async def test_user_state_bad_from_throws(self):
        dictionary = {}
        user_state = UserState(MemoryStorage(dictionary))
        context = TestUtilities.create_empty_context()
        context.activity.from_property = None
        test_property = user_state.create_property("test")
        with self.assertRaises(AttributeError):
            await test_property.get(context)

    async def test_conversation_state_bad_conversation_throws(self):
        dictionary = {}
        user_state = ConversationState(MemoryStorage(dictionary))
        context = TestUtilities.create_empty_context()
        context.activity.conversation = None
        test_property = user_state.create_property("test")
        with self.assertRaises(AttributeError):
            await test_property.get(context)

    async def test_clear_and_save(self):
        # pylint: disable=unnecessary-lambda
        turn_context = TestUtilities.create_empty_context()
        turn_context.activity.conversation = ConversationAccount(id="1234")

        storage = MemoryStorage({})

        # Turn 0
        bot_state1 = ConversationState(storage)
        (
            await bot_state1.create_property("test-name").get(
                turn_context, lambda: TestPocoState()
            )
        ).value = "test-value"
        await bot_state1.save_changes(turn_context)

        # Turn 1
        bot_state2 = ConversationState(storage)
        value1 = (
            await bot_state2.create_property("test-name").get(
                turn_context, lambda: TestPocoState(value="default-value")
            )
        ).value

        assert value1 == "test-value"

        # Turn 2
        bot_state3 = ConversationState(storage)
        await bot_state3.clear_state(turn_context)
        await bot_state3.save_changes(turn_context)

        # Turn 3
        bot_state4 = ConversationState(storage)
        value2 = (
            await bot_state4.create_property("test-name").get(
                turn_context, lambda: TestPocoState(value="default-value")
            )
        ).value

        assert value2, "default-value"

    async def test_bot_state_delete(self):
        # pylint: disable=unnecessary-lambda
        turn_context = TestUtilities.create_empty_context()
        turn_context.activity.conversation = ConversationAccount(id="1234")

        storage = MemoryStorage({})

        # Turn 0
        bot_state1 = ConversationState(storage)
        (
            await bot_state1.create_property("test-name").get(
                turn_context, lambda: TestPocoState()
            )
        ).value = "test-value"
        await bot_state1.save_changes(turn_context)

        # Turn 1
        bot_state2 = ConversationState(storage)
        value1 = (
            await bot_state2.create_property("test-name").get(
                turn_context, lambda: TestPocoState(value="default-value")
            )
        ).value

        assert value1 == "test-value"

        # Turn 2
        bot_state3 = ConversationState(storage)
        await bot_state3.delete(turn_context)

        # Turn 3
        bot_state4 = ConversationState(storage)
        value2 = (
            await bot_state4.create_property("test-name").get(
                turn_context, lambda: TestPocoState(value="default-value")
            )
        ).value

        assert value2 == "default-value"

    async def test_bot_state_get(self):
        # pylint: disable=unnecessary-lambda
        turn_context = TestUtilities.create_empty_context()
        turn_context.activity.conversation = ConversationAccount(id="1234")

        storage = MemoryStorage({})

        conversation_state = ConversationState(storage)
        (
            await conversation_state.create_property("test-name").get(
                turn_context, lambda: TestPocoState()
            )
        ).value = "test-value"

        result = conversation_state.get(turn_context)

        assert result["test-name"].value == "test-value"
