# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
# pylint: disable=pointless-string-statement

from collections import namedtuple

import aiounittest

from botbuilder.core import (
    ConversationState,
    MemoryStorage,
    TurnContext,
)
from botbuilder.core.adapters import TestAdapter
from botbuilder.dialogs import (
    Dialog,
    DialogContext,
    DialogContainer,
    DialogInstance,
    DialogSet,
    DialogState,
    ObjectPath,
)
from botbuilder.dialogs.memory.scopes import ClassMemoryScope, ConversationMemoryScope
from botbuilder.schema import (
    Activity,
    ActivityTypes,
    ChannelAccount,
    ConversationAccount,
)


class TestDialog(Dialog):
    def __init__(self, id: str, message: str):
        super().__init__(id)

        def aux_try_get_value(state):  # pylint: disable=unused-argument
            return "resolved value"

        ExpressionObject = namedtuple("ExpressionObject", "try_get_value")
        self.message = message
        self.expression = ExpressionObject(aux_try_get_value)

    async def begin_dialog(self, dialog_context: DialogContext, options: object = None):
        dialog_context.active_dialog.state.is_dialog = True
        await dialog_context.context.send_activity(self.message)
        return Dialog.end_of_turn


class TestContainer(DialogContainer):
    def __init__(self, id: str, child: Dialog):
        super().__init__(id)
        if child:
            self.dialogs.add(child)
            self.child_id = child.id

    async def begin_dialog(self, dialog_context: DialogContext, options: object = None):
        state = dialog_context.active_dialog.state
        state.is_container = True
        if self.child_id:
            state.dialog = {}
            child_dc = self.create_child_context(dialog_context)
            return await child_dc.begin_dialog(self.child_id, options)

        return Dialog.end_of_turn

    async def continue_dialog(self, dialog_context: DialogContext):
        child_dc = self.create_child_context(dialog_context)
        if child_dc:
            return await child_dc.continue_dialog()

        return Dialog.end_of_turn

    def create_child_context(self, dialog_context: DialogContext):
        state = dialog_context.active_dialog.state
        if state.dialog:
            child_dc = DialogContext(self.dialogs, dialog_context.context, state.dialog)
            child_dc.parent = dialog_context
            return child_dc

        return None


class MemoryScopesTests(aiounittest.AsyncTestCase):
    begin_message = Activity(
        text="begin",
        type=ActivityTypes.message,
        channel_id="test",
        from_property=ChannelAccount(id="user"),
        recipient=ChannelAccount(id="bot"),
        conversation=ConversationAccount(id="convo1"),
    )

    async def test_class_memory_scope_should_find_registered_dialog(self):
        # Create ConversationState with MemoryStorage and register the state as middleware.
        conversation_state = ConversationState(MemoryStorage())

        # Create a DialogState property, DialogSet and register the dialogs.
        dialog_state = conversation_state.create_property("dialogs")
        dialogs = DialogSet(dialog_state)
        dialog = TestDialog("test", "test message")
        dialogs.add(dialog)

        # Create test context
        context = TurnContext(TestAdapter(), MemoryScopesTests.begin_message)
        await dialog_state.set(
            context, DialogState(stack=[DialogInstance(id="test", state={})])
        )

        dialog_context = await dialogs.create_context(context)

        # Run test
        scope = ClassMemoryScope()
        memory = scope.get_memory(dialog_context)
        self.assertTrue(memory, "memory not returned")
        self.assertEqual("test message", memory.message)
        self.assertEqual("resolved value", memory.expression)

    async def test_class_memory_scope_should_not_allow_set_memory_call(self):
        # Create ConversationState with MemoryStorage and register the state as middleware.
        conversation_state = ConversationState(MemoryStorage())

        # Create a DialogState property, DialogSet and register the dialogs.
        dialog_state = conversation_state.create_property("dialogs")
        dialogs = DialogSet(dialog_state)
        dialog = TestDialog("test", "test message")
        dialogs.add(dialog)

        # Create test context
        context = TurnContext(TestAdapter(), MemoryScopesTests.begin_message)
        await dialog_state.set(
            context, DialogState(stack=[DialogInstance(id="test", state={})])
        )

        dialog_context = await dialogs.create_context(context)

        # Run test
        scope = ClassMemoryScope()
        with self.assertRaises(Exception) as context:
            scope.set_memory(dialog_context, {})

        self.assertTrue("not supported" in str(context.exception))

    async def test_class_memory_scope_should_not_allow_load_and_save_changes_calls(
        self,
    ):
        # Create ConversationState with MemoryStorage and register the state as middleware.
        conversation_state = ConversationState(MemoryStorage())

        # Create a DialogState property, DialogSet and register the dialogs.
        dialog_state = conversation_state.create_property("dialogs")
        dialogs = DialogSet(dialog_state)
        dialog = TestDialog("test", "test message")
        dialogs.add(dialog)

        # Create test context
        context = TurnContext(TestAdapter(), MemoryScopesTests.begin_message)
        await dialog_state.set(
            context, DialogState(stack=[DialogInstance(id="test", state={})])
        )

        dialog_context = await dialogs.create_context(context)

        # Run test
        scope = ClassMemoryScope()
        await scope.load(dialog_context)
        memory = scope.get_memory(dialog_context)
        with self.assertRaises(AttributeError) as context:
            memory.message = "foo"

        self.assertTrue("can't set attribute" in str(context.exception))
        await scope.save_changes(dialog_context)
        self.assertEqual("test message", dialog.message)

    async def test_conversation_memory_scope_should_return_conversation_state(self):
        # Create ConversationState with MemoryStorage and register the state as middleware.
        conversation_state = ConversationState(MemoryStorage())

        # Create a DialogState property, DialogSet and register the dialogs.
        dialog_state = conversation_state.create_property("dialogs")
        dialogs = DialogSet(dialog_state)
        dialog = TestDialog("test", "test message")
        dialogs.add(dialog)

        # Create test context
        context = TurnContext(TestAdapter(), MemoryScopesTests.begin_message)
        context.turn_state["ConversationState"] = conversation_state

        dialog_context = await dialogs.create_context(context)

        # Initialize conversation state
        foo_cls = namedtuple("TestObject", "foo")
        conversation_prop = conversation_state.create_property("conversation")
        await conversation_prop.set(context, foo_cls(foo="bar"))
        await conversation_state.save_changes(context)

        # Run test
        scope = ConversationMemoryScope()
        memory = scope.get_memory(dialog_context)
        self.assertTrue(memory, "memory not returned")

        # TODO: Make get_path_value take conversation.foo
        test_obj = ObjectPath.get_path_value(memory, "conversation")
        self.assertEqual("bar", test_obj.foo)

    """
    async def test_conversation_memory_scope_should_return_conversation_state(self):
        # Create ConversationState with MemoryStorage and register the state as middleware.
        conversation_state = ConversationState(MemoryStorage())

        # Create a DialogState property, DialogSet and register the dialogs.
        dialog_state = conversation_state.create_property("dialogs")
        dialogs = DialogSet(dialog_state)
        dialog = TestDialog("test", "test message")
        dialogs.add(dialog)

        # Create test context
        context = TurnContext(TestAdapter(), MemoryScopesTests.begin_message)
        context.turn_state.set("ConversationState", conversation_state)
        dialog_context = await dialogs.createContext(context)

        # Initialize conversation state
        await conversation_state.create_property("conversation").set(context, { foo: "bar" })
        await conversation_state.saveChanges(context)

        # Run test
        scope = ConversationMemoryScope()
        memory = scope.get_memory(dialog_context)
        self.assertEqual(typeof memory, "object", "state not returned")
        self.assertEqual(memory.conversation.foo, "bar")

    it("UserMemoryScope should not return state if not loaded.", async function():
        # Initialize user state
        storage = MemoryStorage()
        context = TurnContext(TestAdapter(), MemoryScopesTests.begin_message)
        userState = UserState(storage)
        context.turn_state.set("UserState", userState)
        await userState.create_property("user").set(context, { foo: "bar" })
        await userState.saveChanges(context)

        # Replace context and conversation_state with new instances
        context = TurnContext(TestAdapter(), MemoryScopesTests.begin_message)
        userState = UserState(storage)
        context.turn_state.set("UserState", userState)

        # Create a DialogState property, DialogSet and register the dialogs.
        conversation_state = ConversationState(storage)
        dialog_state = conversation_state.create_property("dialogs")
        dialogs = DialogSet(dialog_state)
        dialog = TestDialog("test", "test message")
        dialogs.add(dialog)

        # Create test context
        dialog_context = await dialogs.createContext(context)

        # Run test
        scope = UserMemoryScope(userState)
        memory = scope.get_memory(dialog_context)
        self.assertEqual(memory, undefined, "state returned")
    })

    it("UserMemoryScope should return state once loaded.", async function():
        # Initialize user state
        storage = MemoryStorage()
        context = TurnContext(TestAdapter(), MemoryScopesTests.begin_message)
        userState = UserState(storage)
        context.turn_state.set("UserState", userState)
        await userState.create_property("user").set(context, { foo: "bar" })
        await userState.saveChanges(context)

        # Replace context and conversation_state with instances
        context = TurnContext(TestAdapter(), MemoryScopesTests.begin_message)
        userState = UserState(storage)
        context.turn_state.set("UserState", userState)

        # Create a DialogState property, DialogSet and register the dialogs.
        conversation_state = ConversationState(storage)
        context.turn_state.set("ConversationState", conversation_state)
        dialog_state = conversation_state.create_property("dialogs")
        dialogs = DialogSet(dialog_state)
        dialog = TestDialog("test", "test message")
        dialogs.add(dialog)

        # Create test context
        dialog_context = await dialogs.createContext(context)

        # Run test
        scope = UserMemoryScope()
        memory = scope.get_memory(dialog_context)
        self.assertEqual(memory, undefined, "state returned")
        
        await scope.load(dialog_context)
        memory = scope.get_memory(dialog_context)
        self.assertEqual(typeof memory, "object", "state not returned")
        self.assertEqual(memory.user.foo, "bar")
    })

    it("DialogMemoryScope should return containers state.", async function():
        # Create a DialogState property, DialogSet and register the dialogs.
        storage = MemoryStorage()
        conversation_state = ConversationState(storage)
        dialog_state = conversation_state.create_property("dialogs")
        dialogs = DialogSet(dialog_state)
        container = TestContainer("container")
        dialogs.add(container)

        # Create test context
        context = TurnContext(TestAdapter(), MemoryScopesTests.begin_message)
        dialog_context = await dialogs.createContext(context)

        # Run test
        scope = DialogMemoryScope()
        await dialog_context.beginDialog("container")
        memory = scope.get_memory(dialog_context)
        assert(typeof memory == "object", "state not returned")
        assert(memory.isContainer == True)
    })

    it("DialogMemoryScope should return parent containers state for children.", async function():
        # Create a DialogState property, DialogSet and register the dialogs.
        storage = MemoryStorage()
        conversation_state = ConversationState(storage)
        dialog_state = conversation_state.create_property("dialogs")
        dialogs = DialogSet(dialog_state)
        container = TestContainer("container", TestDialog("child", "test message"))
        dialogs.add(container)

        # Create test context
        context = TurnContext(TestAdapter(), MemoryScopesTests.begin_message)
        dialog_context = await dialogs.createContext(context)

        # Run test
        scope = DialogMemoryScope()
        await dialog_context.beginDialog("container")
        child_dc = dialog_context.child
        assert(child_dc != undefined, "No child DC")
        memory = scope.get_memory(child_dc)
        assert(typeof memory == "object", "state not returned")
        assert(memory.isContainer == True)
    })

    it("DialogMemoryScope should return childs state when no parent.", async function():
        # Create a DialogState property, DialogSet and register the dialogs.
        storage = MemoryStorage()
        conversation_state = ConversationState(storage)
        dialog_state = conversation_state.create_property("dialogs")
        dialogs = DialogSet(dialog_state)
        dialog = TestDialog("test", "test message")
        dialogs.add(dialog)

        # Create test context
        context = TurnContext(TestAdapter(), MemoryScopesTests.begin_message)
        dialog_context = await dialogs.createContext(context)

        # Run test
        scope = DialogMemoryScope()
        await dialog_context.beginDialog("test")
        memory = scope.get_memory(dialog_context)
        assert(typeof memory != undefined, "state not returned")
        assert(memory.is_dialog == True)
    })

    it("DialogMemoryScope should overwrite parents memory.", async function():
        # Create a DialogState property, DialogSet and register the dialogs.
        storage = MemoryStorage()
        conversation_state = ConversationState(storage)
        dialog_state = conversation_state.create_property("dialogs")
        dialogs = DialogSet(dialog_state)
        container = TestContainer("container", TestDialog("child", "test message"))
        dialogs.add(container)

        # Create test context
        context = TurnContext(TestAdapter(), MemoryScopesTests.begin_message)
        dialog_context = await dialogs.createContext(context)

        # Run test
        scope = DialogMemoryScope()
        await dialog_context.beginDialog("container")
        child_dc = dialog_context.child
        assert(child_dc != undefined, "No child DC")
        scope.setMemory(child_dc, { foo: "bar" })
        memory = scope.get_memory(child_dc)
        assert(typeof memory == "object", "state not returned")
        assert(memory.foo == "bar")
    })

    it("DialogMemoryScope should overwrite active dialogs memory.", async function():
        # Create a DialogState property, DialogSet and register the dialogs.
        storage = MemoryStorage()
        conversation_state = ConversationState(storage)
        dialog_state = conversation_state.create_property("dialogs")
        dialogs = DialogSet(dialog_state)
        container = TestContainer("container")
        dialogs.add(container)

        # Create test context
        context = TurnContext(TestAdapter(), MemoryScopesTests.begin_message)
        dialog_context = await dialogs.createContext(context)

        # Run test
        scope = DialogMemoryScope()
        await dialog_context.beginDialog("container")
        scope.setMemory(dialog_context, { foo: "bar" })
        memory = scope.get_memory(dialog_context)
        assert(typeof memory == "object", "state not returned")
        assert(memory.foo == "bar")
    })

    it("DialogMemoryScope should raise error if setMemory() called without memory.", async function():
        # Create a DialogState property, DialogSet and register the dialogs.
        storage = MemoryStorage()
        conversation_state = ConversationState(storage)
        dialog_state = conversation_state.create_property("dialogs")
        dialogs = DialogSet(dialog_state)
        container = TestContainer("container")
        dialogs.add(container)

        # Create test context
        context = TurnContext(TestAdapter(), MemoryScopesTests.begin_message)
        dialog_context = await dialogs.createContext(context)

        # Run test
        error = False
        try:
            scope = DialogMemoryScope()
            await dialog_context.beginDialog("container")
            scope.setMemory(dialog_context, undefined)
        } catch (err):
            error = True
        }
        assert(error)
    })

    it("DialogMemoryScope should raise error if delete() called.", async function():
        # Create a DialogState property, DialogSet and register the dialogs.
        storage = MemoryStorage()
        conversation_state = ConversationState(storage)
        dialog_state = conversation_state.create_property("dialogs")
        dialogs = DialogSet(dialog_state)
        container = TestContainer("container")
        dialogs.add(container)

        # Create test context
        context = TurnContext(TestAdapter(), MemoryScopesTests.begin_message)
        dialog_context = await dialogs.createContext(context)

        # Run test
        error = False
        try:
            scope = DialogMemoryScope()
            await scope.delete(dialog_context)
        } catch (err):
            error = True
        }
        assert(error)
    })

    it("SettingsMemoryScope should return content of settings.", async function():
        # Create a DialogState property, DialogSet and register the dialogs.
        conversation_state = ConversationState(MemoryStorage())
        dialog_state = conversation_state.create_property("dialogs")
        dialogs = DialogSet(dialog_state).add(TestDialog("test", "test message"))

        # Create test context
        context = TurnContext(TestAdapter(), MemoryScopesTests.begin_message)
        dialog_context = await dialogs.createContext(context)
        settings = require("./test.settings.json")
        dialog_context.context.turn_state.set("settings", settings)

        # Run test
        scope = SettingsMemoryScope()
        memory = scope.get_memory(dialog_context)
        self.assertEqual(typeof memory, "object", "settings not returned")
        self.assertEqual(memory.string, "test")
        self.assertEqual(memory.int, 3)
        self.assertEqual(memory.array[0], "zero")
        self.assertEqual(memory.array[1], "one")
        self.assertEqual(memory.array[2], "two")
        self.assertEqual(memory.array[3], "three")
        self.assertEqual(dialog_context.state.getValue("settings.fakeArray.0"), "zero")
        self.assertEqual(dialog_context.state.getValue("settings.fakeArray.1"), "one")
        self.assertEqual(dialog_context.state.getValue("settings.fakeArray.2"), "two")
        self.assertEqual(dialog_context.state.getValue("settings.fakeArray.3"), "three")
        self.assertEqual(dialog_context.state.getValue("settings.fakeArray.zzz"), "cat")
        for (key in process.env):
            if (typeof process.env[key] == "string"):
                assert(memory[key] == process.env[key])
            }
        }

        # override settings with process.env
        self.assertEqual(dialog_context.state.getValue("settings.to_be_overridden"), "one")
        process.env["to_be_overridden"] = "two"
        self.assertEqual(dialog_context.state.getValue("settings.not_to_be_overridden"), "one")
        self.assertEqual(dialog_context.state.getValue("settings.to_be_overridden"), "two", "settings should be overriden by environment variables")
    })

    it("ThisMemoryScope should return active dialogs state.", async function():
        # Create a DialogState property, DialogSet and register the dialogs.
        storage = MemoryStorage()
        conversation_state = ConversationState(storage)
        dialog_state = conversation_state.create_property("dialogs")
        dialogs = DialogSet(dialog_state)
        dialog = TestDialog("test", "test message")
        dialogs.add(dialog)

        # Create test context
        context = TurnContext(TestAdapter(), MemoryScopesTests.begin_message)
        dialog_context = await dialogs.createContext(context)

        # Run test
        scope = ThisMemoryScope()
        await dialog_context.beginDialog("test")
        memory = scope.get_memory(dialog_context)
        assert(typeof memory != undefined, "state not returned")
        assert(memory.is_dialog == True)
    })

    it("ThisMemoryScope should overwrite active dialogs memory.", async function():
        # Create a DialogState property, DialogSet and register the dialogs.
        storage = MemoryStorage()
        conversation_state = ConversationState(storage)
        dialog_state = conversation_state.create_property("dialogs")
        dialogs = DialogSet(dialog_state)
        container = TestContainer("container")
        dialogs.add(container)

        # Create test context
        context = TurnContext(TestAdapter(), MemoryScopesTests.begin_message)
        dialog_context = await dialogs.createContext(context)

        # Run test
        scope = ThisMemoryScope()
        await dialog_context.beginDialog("container")
        scope.setMemory(dialog_context, { foo: "bar" })
        memory = scope.get_memory(dialog_context)
        assert(typeof memory == "object", "state not returned")
        assert(memory.foo == "bar")
    })

    it("ThisMemoryScope should raise error if setMemory() called without memory.", async function():
        # Create a DialogState property, DialogSet and register the dialogs.
        storage = MemoryStorage()
        conversation_state = ConversationState(storage)
        dialog_state = conversation_state.create_property("dialogs")
        dialogs = DialogSet(dialog_state)
        container = TestContainer("container")
        dialogs.add(container)

        # Create test context
        context = TurnContext(TestAdapter(), MemoryScopesTests.begin_message)
        dialog_context = await dialogs.createContext(context)

        # Run test
        error = False
        try:
            scope = ThisMemoryScope()
            await dialog_context.beginDialog("container")
            scope.setMemory(dialog_context, undefined)
        } catch (err):
            error = True
        }
        assert(error)
    })

    it("ThisMemoryScope should raise error if setMemory() called without active dialog.", async function():
        # Create a DialogState property, DialogSet and register the dialogs.
        storage = MemoryStorage()
        conversation_state = ConversationState(storage)
        dialog_state = conversation_state.create_property("dialogs")
        dialogs = DialogSet(dialog_state)
        container = TestContainer("container")
        dialogs.add(container)

        # Create test context
        context = TurnContext(TestAdapter(), MemoryScopesTests.begin_message)
        dialog_context = await dialogs.createContext(context)

        # Run test
        error = False
        try:
            scope = ThisMemoryScope()
            scope.setMemory(dialog_context, { foo: "bar" })
        } catch (err):
            error = True
        }
        assert(error)
    })

    it("ThisMemoryScope should raise error if delete() called.", async function():
        # Create a DialogState property, DialogSet and register the dialogs.
        storage = MemoryStorage()
        conversation_state = ConversationState(storage)
        dialog_state = conversation_state.create_property("dialogs")
        dialogs = DialogSet(dialog_state)
        container = TestContainer("container")
        dialogs.add(container)

        # Create test context
        context = TurnContext(TestAdapter(), MemoryScopesTests.begin_message)
        dialog_context = await dialogs.createContext(context)

        # Run test
        error = False
        try:
            scope = ThisMemoryScope()
            await scope.delete(dialog_context)
        } catch (err):
            error = True
        }
        assert(error)
    })

    it("TurnMemoryScope should persist changes to turn state.", async function():
        # Create a DialogState property, DialogSet and register the dialogs.
        storage = MemoryStorage()
        conversation_state = ConversationState(storage)
        dialog_state = conversation_state.create_property("dialogs")
        dialogs = DialogSet(dialog_state)
        dialog = TestDialog("test", "test message")
        dialogs.add(dialog)

        # Create test context
        context = TurnContext(TestAdapter(), MemoryScopesTests.begin_message)
        dialog_context = await dialogs.createContext(context)

        # Run test
        scope = TurnMemoryScope()
        memory = scope.get_memory(dialog_context)
        assert(typeof memory != undefined, "state not returned")
        memory.foo = "bar"
        memory = scope.get_memory(dialog_context)
        assert(memory.foo == "bar")
    })

    it("TurnMemoryScope should overwrite values in turn state.", async function():
        # Create a DialogState property, DialogSet and register the dialogs.
        storage = MemoryStorage()
        conversation_state = ConversationState(storage)
        dialog_state = conversation_state.create_property("dialogs")
        dialogs = DialogSet(dialog_state)
        dialog = TestDialog("test", "test message")
        dialogs.add(dialog)

        # Create test context
        context = TurnContext(TestAdapter(), MemoryScopesTests.begin_message)
        dialog_context = await dialogs.createContext(context)

        # Run test
        scope = TurnMemoryScope()
        scope.setMemory(dialog_context, { foo: "bar" })
        memory = scope.get_memory(dialog_context)
        assert(typeof memory != undefined, "state not returned")
        assert(memory.foo == "bar")
    })

    it("TurnMemoryScope should raise error when setMemory() called without memory.", async function():
        # Create a DialogState property, DialogSet and register the dialogs.
        storage = MemoryStorage()
        conversation_state = ConversationState(storage)
        dialog_state = conversation_state.create_property("dialogs")
        dialogs = DialogSet(dialog_state)
        dialog = TestDialog("test", "test message")
        dialogs.add(dialog)

        # Create test context
        context = TurnContext(TestAdapter(), MemoryScopesTests.begin_message)
        dialog_context = await dialogs.createContext(context)

        # Run test
        error = False
        try:
            scope = TurnMemoryScope()
            scope.setMemory(dialog_context, undefined)
        } catch (err):
            error = True
        }
        assert(error)
    })

    it("TurnMemoryScope should raise error when delete() called.", async function():
        # Create a DialogState property, DialogSet and register the dialogs.
        storage = MemoryStorage()
        conversation_state = ConversationState(storage)
        dialog_state = conversation_state.create_property("dialogs")
        dialogs = DialogSet(dialog_state)
        dialog = TestDialog("test", "test message")
        dialogs.add(dialog)

        # Create test context
        context = TurnContext(TestAdapter(), MemoryScopesTests.begin_message)
        dialog_context = await dialogs.createContext(context)

        # Run test
        error = False
        try:
            scope = TurnMemoryScope()
            await scope.delete(dialog_context)
        } catch (err):
            error = True
        }
        assert(error)
    """
