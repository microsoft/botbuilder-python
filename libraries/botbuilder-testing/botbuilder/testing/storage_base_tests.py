"""
Base tests that all storage providers should implement in their own tests.
They handle the storage-based assertions, internally.

All tests return true if assertions pass to indicate that the code ran to completion, passing internal assertions.
Therefore, all tests using theses static tests should strictly check that the method returns true.

:Example:
    async def test_handle_null_keys_when_reading(self):
        await reset()

        test_ran = await StorageBaseTests.handle_null_keys_when_reading(get_storage())

        assert test_ran
"""
import pytest
from botbuilder.azure import CosmosDbStorage
from botbuilder.core import (
    ConversationState,
    TurnContext,
    MessageFactory,
    MemoryStorage,
)
from botbuilder.core.adapters import TestAdapter
from botbuilder.dialogs import (
    DialogSet,
    DialogTurnStatus,
    TextPrompt,
    PromptValidatorContext,
    WaterfallStepContext,
    Dialog,
    WaterfallDialog,
    PromptOptions,
)


class StorageBaseTests:
    @staticmethod
    async def return_empty_object_when_reading_unknown_key(storage) -> bool:
        result = await storage.read(["unknown"])

        assert result is not None
        assert len(result) == 0

        return True

    @staticmethod
    async def handle_null_keys_when_reading(storage) -> bool:
        if isinstance(storage, (CosmosDbStorage, MemoryStorage)):
            result = await storage.read(None)
            assert len(result.keys()) == 0
        # Catch-all
        else:
            with pytest.raises(Exception) as err:
                await storage.read(None)
            assert err.value.args[0] == "Keys are required when reading"

        return True

    @staticmethod
    async def handle_null_keys_when_writing(storage) -> bool:
        with pytest.raises(Exception) as err:
            await storage.write(None)
        assert err.value.args[0] == "Changes are required when writing"

        return True

    @staticmethod
    async def does_not_raise_when_writing_no_items(storage) -> bool:
        # noinspection PyBroadException
        try:
            await storage.write([])
        except:
            pytest.fail("Should not raise")

        return True

    @staticmethod
    async def create_object(storage) -> bool:
        store_items = {
            "createPoco": {"id": 1},
            "createPocoStoreItem": {"id": 2},
        }

        await storage.write(store_items)

        read_store_items = await storage.read(store_items.keys())

        assert store_items["createPoco"]["id"] == read_store_items["createPoco"]["id"]
        assert (
            store_items["createPocoStoreItem"]["id"]
            == read_store_items["createPocoStoreItem"]["id"]
        )
        assert read_store_items["createPoco"]["e_tag"] is not None
        assert read_store_items["createPocoStoreItem"]["e_tag"] is not None

        return True

    @staticmethod
    async def handle_crazy_keys(storage) -> bool:
        key = '!@#$%^&*()_+??><":QASD~`'
        store_item = {"id": 1}
        store_items = {key: store_item}

        await storage.write(store_items)

        read_store_items = await storage.read(store_items.keys())

        assert read_store_items[key] is not None
        assert read_store_items[key]["id"] == 1

        return True

    @staticmethod
    async def update_object(storage) -> bool:
        original_store_items = {
            "pocoItem": {"id": 1, "count": 1},
            "pocoStoreItem": {"id": 1, "count": 1},
        }

        # 1st write should work
        await storage.write(original_store_items)

        loaded_store_items = await storage.read(["pocoItem", "pocoStoreItem"])

        update_poco_item = loaded_store_items["pocoItem"]
        update_poco_item["e_tag"] = None
        update_poco_store_item = loaded_store_items["pocoStoreItem"]
        assert update_poco_store_item["e_tag"] is not None

        # 2nd write should work
        update_poco_item["count"] += 1
        update_poco_store_item["count"] += 1

        await storage.write(loaded_store_items)

        reloaded_store_items = await storage.read(loaded_store_items.keys())

        reloaded_update_poco_item = reloaded_store_items["pocoItem"]
        reloaded_update_poco_store_item = reloaded_store_items["pocoStoreItem"]

        assert reloaded_update_poco_item["e_tag"] is not None
        assert (
            update_poco_store_item["e_tag"] != reloaded_update_poco_store_item["e_tag"]
        )
        assert reloaded_update_poco_item["count"] == 2
        assert reloaded_update_poco_store_item["count"] == 2

        # Write with old e_tag should succeed for non-storeItem
        update_poco_item["count"] = 123
        await storage.write({"pocoItem": update_poco_item})

        # Write with old eTag should FAIL for storeItem
        update_poco_store_item["count"] = 123

        with pytest.raises(Exception) as err:
            await storage.write({"pocoStoreItem": update_poco_store_item})
        assert err.value is not None

        reloaded_store_items2 = await storage.read(["pocoItem", "pocoStoreItem"])

        reloaded_poco_item2 = reloaded_store_items2["pocoItem"]
        reloaded_poco_item2["e_tag"] = None
        reloaded_poco_store_item2 = reloaded_store_items2["pocoStoreItem"]

        assert reloaded_poco_item2["count"] == 123
        assert reloaded_poco_store_item2["count"] == 2

        # write with wildcard etag should work
        reloaded_poco_item2["count"] = 100
        reloaded_poco_store_item2["count"] = 100
        reloaded_poco_store_item2["e_tag"] = "*"

        wildcard_etag_dict = {
            "pocoItem": reloaded_poco_item2,
            "pocoStoreItem": reloaded_poco_store_item2,
        }

        await storage.write(wildcard_etag_dict)

        reloaded_store_items3 = await storage.read(["pocoItem", "pocoStoreItem"])

        assert reloaded_store_items3["pocoItem"]["count"] == 100
        assert reloaded_store_items3["pocoStoreItem"]["count"] == 100

        # Write with empty etag should not work
        reloaded_store_items4 = await storage.read(["pocoStoreItem"])
        reloaded_store_item4 = reloaded_store_items4["pocoStoreItem"]

        assert reloaded_store_item4 is not None

        reloaded_store_item4["e_tag"] = ""
        dict2 = {"pocoStoreItem": reloaded_store_item4}

        with pytest.raises(Exception) as err:
            await storage.write(dict2)
        assert err.value is not None

        final_store_items = await storage.read(["pocoItem", "pocoStoreItem"])
        assert final_store_items["pocoItem"]["count"] == 100
        assert final_store_items["pocoStoreItem"]["count"] == 100

        return True

    @staticmethod
    async def delete_object(storage) -> bool:
        store_items = {"delete1": {"id": 1, "count": 1}}

        await storage.write(store_items)

        read_store_items = await storage.read(["delete1"])

        assert read_store_items["delete1"]["e_tag"]
        assert read_store_items["delete1"]["count"] == 1

        await storage.delete(["delete1"])

        reloaded_store_items = await storage.read(["delete1"])

        assert reloaded_store_items.get("delete1", None) is None

        return True

    @staticmethod
    async def delete_unknown_object(storage) -> bool:
        # noinspection PyBroadException
        try:
            await storage.delete(["unknown_key"])
        except:
            pytest.fail("Should not raise")

        return True

    @staticmethod
    async def perform_batch_operations(storage) -> bool:
        await storage.write(
            {"batch1": {"count": 10}, "batch2": {"count": 20}, "batch3": {"count": 30},}
        )

        result = await storage.read(["batch1", "batch2", "batch3"])

        assert result.get("batch1", None) is not None
        assert result.get("batch2", None) is not None
        assert result.get("batch3", None) is not None
        assert result["batch1"]["count"] == 10
        assert result["batch2"]["count"] == 20
        assert result["batch3"]["count"] == 30
        assert result["batch1"].get("e_tag", None) is not None
        assert result["batch2"].get("e_tag", None) is not None
        assert result["batch3"].get("e_tag", None) is not None

        await storage.delete(["batch1", "batch2", "batch3"])

        result = await storage.read(["batch1", "batch2", "batch3"])

        assert result.get("batch1", None) is None
        assert result.get("batch2", None) is None
        assert result.get("batch3", None) is None

        return True

    @staticmethod
    async def proceeds_through_waterfall(storage) -> bool:
        convo_state = ConversationState(storage)

        dialog_state = convo_state.create_property("dialogState")
        dialogs = DialogSet(dialog_state)

        async def exec_test(turn_context: TurnContext) -> None:
            dialog_context = await dialogs.create_context(turn_context)

            await dialog_context.continue_dialog()
            if not turn_context.responded:
                await dialog_context.begin_dialog(WaterfallDialog.__name__)
            await convo_state.save_changes(turn_context)

        adapter = TestAdapter(exec_test)

        async def prompt_validator(prompt_context: PromptValidatorContext):
            result = prompt_context.recognized.value
            if len(result) > 3:
                succeeded_message = MessageFactory.text(
                    f"You got it at the {prompt_context.options.number_of_attempts}rd try!"
                )
                await prompt_context.context.send_activity(succeeded_message)
                return True

            reply = MessageFactory.text(
                f"Please send a name that is longer than 3 characters. {prompt_context.options.number_of_attempts}"
            )
            await prompt_context.context.send_activity(reply)
            return False

        async def step_1(step_context: WaterfallStepContext) -> DialogTurnStatus:
            assert isinstance(step_context.active_dialog.state["stepIndex"], int)
            await step_context.context.send_activity("step1")
            return Dialog.end_of_turn

        async def step_2(step_context: WaterfallStepContext) -> None:
            assert isinstance(step_context.active_dialog.state["stepIndex"], int)
            await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(prompt=MessageFactory.text("Please type your name")),
            )

        async def step_3(step_context: WaterfallStepContext) -> DialogTurnStatus:
            assert isinstance(step_context.active_dialog.state["stepIndex"], int)
            await step_context.context.send_activity("step3")
            return Dialog.end_of_turn

        steps = [step_1, step_2, step_3]

        dialogs.add(WaterfallDialog(WaterfallDialog.__name__, steps))

        dialogs.add(TextPrompt(TextPrompt.__name__, prompt_validator))

        step1 = await adapter.send("hello")
        step2 = await step1.assert_reply("step1")
        step3 = await step2.send("hello")
        step4 = await step3.assert_reply("Please type your name")  # None
        step5 = await step4.send("hi")
        step6 = await step5.assert_reply(
            "Please send a name that is longer than 3 characters. 0"
        )
        step7 = await step6.send("hi")
        step8 = await step7.assert_reply(
            "Please send a name that is longer than 3 characters. 1"
        )
        step9 = await step8.send("hi")
        step10 = await step9.assert_reply(
            "Please send a name that is longer than 3 characters. 2"
        )
        step11 = await step10.send("Kyle")
        step12 = await step11.assert_reply("You got it at the 3rd try!")
        await step12.assert_reply("step3")

        return True
