import aiounittest
import json
import unittest
from os import path
from unittest.mock import patch

# from botbuilder.ai.qna import QnAMakerEndpoint, QnAMaker, QnAMakerOptions
from botbuilder.ai.qna.dialogs import QnAMakerDialog
from botbuilder.core import ConversationState, MemoryStorage, TurnContext
from botbuilder.core.adapters import TestAdapter, TestFlow
from botbuilder.dialogs import (
    # Dialog,
    DialogSet,
    # WaterfallDialog,
    # WaterfallStepContext,
    # DialogTurnResult,
    DialogTurnStatus,
)

class QnaMakerDialogTest(aiounittest.AsyncTestCase):
    # Note this is NOT a real QnA Maker application ID nor a real QnA Maker subscription-key
    # theses are GUIDs edited to look right to the parsing and validation code.

    _knowledge_base_id: str = "f028d9k3-7g9z-11d3-d300-2b8x98227q8w"
    _endpoint_key: str = "1k997n7w-207z-36p3-j2u1-09tas20ci6011"
    _host: str = "https://dummyqnahost.azurewebsites.net/qnamaker"

    _tell_me_about_birds_text: str = "Tell me about birds"
    _choose_bird_text: str = "Choose one of the following birds to get more info"
    _bald_eagle_text: str = "Bald Eagle"
    _not_bald_text: str = "Apparently these guys aren't actually bald!"

    # tests_endpoint = QnAMakerEndpoint(_knowledge_base_id, _endpoint_key, _host)

    # TODO - this is from test_waterfall.py -- update it to work for qna dialog
    async def test_multiturn_qna_dialog(self):
        convo_state = ConversationState(MemoryStorage())
        dialog_state = convo_state.create_property("dialogState")
        # TODO - verify whether or not we need UserState too like in sample 49, or just convo state
        dialogs = DialogSet(dialog_state)

        qna_dialog = QnAMakerDialog(
            self._knowledge_base_id,
            self._endpoint_key,
            self._host
        )
        dialogs.add(qna_dialog)

        async def execute_qna_dialog_test(turn_context: TurnContext) -> None:
            if (turn_context.activity.type != 'message'):
                raise TypeError('Failed to execute QnA dialog. Should have received a message activity.')

            response_json = QnaMakerDialogTest._get_json_res(turn_context.activity.text)
            dialog_context = await dialogs.create_context(turn_context)

            with patch(
                "aiohttp.ClientSession.post",
                return_value=aiounittest.futurized(response_json),
            ):
                results = await dialog_context.continue_dialog()

                if results.status == DialogTurnStatus.Empty:
                    await dialog_context.begin_dialog("QnAMakerDialog")

                await convo_state.save_changes(turn_context)

        adapt = TestAdapter(execute_qna_dialog_test)

        test_flow = TestFlow(None, adapt)
        tf2 = await test_flow.send(self._tell_me_about_birds_text)
        dialog_reply = tf2.adapter.activity_buffer[0]
        tf3 = await tf2.assert_reply(self._choose_bird_text)
        tf4 = await tf3.send(self._bald_eagle_text)
        await tf4.assert_reply("Apparently these guys aren't actually bald!")
    
    # TODO - maybe this could be static
    @classmethod
    def _get_json_for_file(cls, response_file: str) -> object:
        curr_dir = path.dirname(path.abspath(__file__))
        response_path = path.join(curr_dir, "test_data", response_file)

        with open(response_path, "r", encoding="utf-8-sig") as file:
            response_str = file.read()
        response_json = json.loads(response_str)

        return response_json
    
    @classmethod
    def _get_json_res(cls, text: str) -> object:
        if (text == cls._tell_me_about_birds_text):
            return QnaMakerDialogTest._get_json_for_file("QnAMakerDialog_MultiTurn_Answer1.json")
        
        if (text == cls._bald_eagle_text):
            # file_name = cls._not_bald_text
            return QnaMakerDialogTest._get_json_for_file("QnAMakerDialog_MultiTurn_Answer2.json")

        
        # QnaMakerDialogTest._get_json_for_file("QnAMakerDialog_MultiTurn_Answer2.json")

        