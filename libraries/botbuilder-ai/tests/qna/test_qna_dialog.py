import json
from os import path
from unittest.mock import patch
import aiounittest

# from botbuilder.ai.qna import QnAMakerEndpoint, QnAMaker, QnAMakerOptions
from botbuilder.ai.qna.dialogs import QnAMakerDialog
from botbuilder.schema import Activity, ActivityTypes
from botbuilder.core import ConversationState, MemoryStorage, TurnContext
from botbuilder.core.adapters import TestAdapter, TestFlow
from botbuilder.dialogs import DialogSet, DialogTurnStatus


class QnaMakerDialogTest(aiounittest.AsyncTestCase):
    # Note this is NOT a real QnA Maker application ID nor a real QnA Maker subscription-key
    # theses are GUIDs edited to look right to the parsing and validation code.

    _knowledge_base_id: str = "f028d9k3-7g9z-11d3-d300-2b8x98227q8w"
    _endpoint_key: str = "1k997n7w-207z-36p3-j2u1-09tas20ci6011"
    _host: str = "https://dummyqnahost.azurewebsites.net/qnamaker"

    _tell_me_about_birds: str = "Tell me about birds"
    _choose_bird: str = "Choose one of the following birds to get more info"
    _bald_eagle: str = "Bald Eagle"
    _esper: str = "Esper"

    DEFAULT_ACTIVE_LEARNING_TITLE: str = "Did you mean:"
    DEFAULT_NO_MATCH_TEXT: str = "None of the above."
    DEFAULT_CARD_NO_MATCH_RESPONSE: str = "Thanks for the feedback."

    async def test_multiturn_dialog(self):
        # Set Up QnAMakerDialog
        convo_state = ConversationState(MemoryStorage())
        dialog_state = convo_state.create_property("dialogState")
        dialogs = DialogSet(dialog_state)

        qna_dialog = QnAMakerDialog(
            self._knowledge_base_id, self._endpoint_key, self._host
        )
        dialogs.add(qna_dialog)

        # Callback that runs the dialog
        async def execute_qna_dialog(turn_context: TurnContext) -> None:
            if turn_context.activity.type != ActivityTypes.message:
                raise TypeError(
                    "Failed to execute QnA dialog. Should have received a message activity."
                )

            response_json = self._get_json_res(turn_context.activity.text)
            dialog_context = await dialogs.create_context(turn_context)
            with patch(
                "aiohttp.ClientSession.post",
                return_value=aiounittest.futurized(response_json),
            ):
                results = await dialog_context.continue_dialog()

                if results.status == DialogTurnStatus.Empty:
                    await dialog_context.begin_dialog("QnAMakerDialog")

                await convo_state.save_changes(turn_context)

        # Send and receive messages from QnA dialog
        test_adapter = TestAdapter(execute_qna_dialog)
        test_flow = TestFlow(None, test_adapter)
        tf2 = await test_flow.send(self._tell_me_about_birds)
        dialog_reply: Activity = tf2.adapter.activity_buffer[0]
        self._assert_has_valid_hero_card_buttons(dialog_reply, button_count=2)
        tf3 = await tf2.assert_reply(self._choose_bird)
        tf4 = await tf3.send(self._bald_eagle)
        await tf4.assert_reply("Apparently these guys aren't actually bald!")

    async def test_active_learning(self):
        # Set Up QnAMakerDialog
        convo_state = ConversationState(MemoryStorage())
        dialog_state = convo_state.create_property("dialogState")
        dialogs = DialogSet(dialog_state)

        qna_dialog = QnAMakerDialog(
            self._knowledge_base_id, self._endpoint_key, self._host
        )
        dialogs.add(qna_dialog)

        # Callback that runs the dialog
        async def execute_qna_dialog(turn_context: TurnContext) -> None:
            if turn_context.activity.type != ActivityTypes.message:
                raise TypeError(
                    "Failed to execute QnA dialog. Should have received a message activity."
                )

            response_json = self._get_json_res(turn_context.activity.text)
            dialog_context = await dialogs.create_context(turn_context)
            with patch(
                "aiohttp.ClientSession.post",
                return_value=aiounittest.futurized(response_json),
            ):
                results = await dialog_context.continue_dialog()

                if results.status == DialogTurnStatus.Empty:
                    await dialog_context.begin_dialog("QnAMakerDialog")

                await convo_state.save_changes(turn_context)

        # Send and receive messages from QnA dialog
        test_adapter = TestAdapter(execute_qna_dialog)
        test_flow = TestFlow(None, test_adapter)
        tf2 = await test_flow.send(self._esper)
        dialog_reply: Activity = tf2.adapter.activity_buffer[0]
        self._assert_has_valid_hero_card_buttons(dialog_reply, button_count=3)
        tf3 = await tf2.assert_reply(self.DEFAULT_ACTIVE_LEARNING_TITLE)
        tf4 = await tf3.send(self.DEFAULT_NO_MATCH_TEXT)
        await tf4.assert_reply(self.DEFAULT_CARD_NO_MATCH_RESPONSE)

        print(tf2)

    def _assert_has_valid_hero_card_buttons(
        self, activity: Activity, button_count: int
    ):
        self.assertIsInstance(activity, Activity)
        attachments = activity.attachments
        self.assertTrue(attachments)
        self.assertEqual(len(attachments), 1)
        buttons = attachments[0].content.buttons
        button_count_err = (
            f"Should have only received {button_count} buttons in multi-turn prompt"
        )

        if activity.text == self._choose_bird:
            self.assertEqual(len(buttons), button_count, button_count_err)
            self.assertEqual(buttons[0].value, self._bald_eagle)
            self.assertEqual(buttons[1].value, "Hummingbird")

        if activity.text == self.DEFAULT_ACTIVE_LEARNING_TITLE:
            self.assertEqual(len(buttons), button_count, button_count_err)
            self.assertEqual(buttons[0].value, "Esper seeks")
            self.assertEqual(buttons[1].value, "Esper sups")
            self.assertEqual(buttons[2].value, self.DEFAULT_NO_MATCH_TEXT)

    def _get_json_res(self, text: str) -> object:
        if text == self._tell_me_about_birds:
            return QnaMakerDialogTest._get_json_for_file(
                "QnAMakerDialog_MultiTurn_Answer1.json"
            )

        if text == self._bald_eagle:
            return QnaMakerDialogTest._get_json_for_file(
                "QnAMakerDialog_MultiTurn_Answer2.json"
            )

        if text == self._esper:
            return QnaMakerDialogTest._get_json_for_file(
                "QnAMakerDialog_ActiveLearning.json"
            )

        return None

    @staticmethod
    def _get_json_for_file(response_file: str) -> object:
        curr_dir = path.dirname(path.abspath(__file__))
        response_path = path.join(curr_dir, "test_data", response_file)

        with open(response_path, "r", encoding="utf-8-sig") as file:
            response_str = file.read()
        response_json = json.loads(response_str)

        return response_json
