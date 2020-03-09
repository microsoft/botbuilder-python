# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.


from typing import List, Union

from botbuilder.core import (
    AutoSaveStateMiddleware,
    ConversationState,
    MemoryStorage,
    Middleware,
    StatePropertyAccessor,
    TurnContext,
)
from botbuilder.core.adapters import TestAdapter
from botbuilder.dialogs import Dialog, DialogSet, DialogTurnResult, DialogTurnStatus
from botbuilder.schema import Activity, ConversationReference


class DialogTestClient:
    """A client for testing dialogs in isolation."""

    def __init__(
        self,
        channel_or_adapter: Union[str, TestAdapter],
        target_dialog: Dialog,
        initial_dialog_options: object = None,
        middlewares: List[Middleware] = None,
        conversation_state: ConversationState = None,
    ):
        """
        Create a DialogTestClient to test a dialog without having to create a full-fledged adapter.

        ```python
        client = DialogTestClient("test", MY_DIALOG, MY_OPTIONS)
        reply = await client.send_activity("first message")
        self.assertEqual(reply.text, "first reply", "reply failed")
        ```

        :param channel_or_adapter: The channel Id or test adapter to be used for the test.
        For channel Id, use 'emulator' or 'test' if you are uncertain of the channel you are targeting.
        Otherwise, it is recommended that you use the id for the channel(s) your bot will be using and
        write a test case for each channel.
        Or, a test adapter instance can be used.
        :type channel_or_adapter: Union[str, TestAdapter]
        :param target_dialog: The dialog to be tested. This will be the root dialog for the test client.
        :type target_dialog: Dialog
        :param initial_dialog_options: (Optional) additional argument(s) to pass to the dialog being started.
        :type initial_dialog_options: object
        :param middlewares: (Optional) The test adapter to use. If this parameter is not provided, the test client will
        use a default TestAdapter.
        :type middlewares: List[Middleware]
        :param conversation_state: (Optional) A ConversationState instance to use in the test client.
        :type conversation_state: ConversationState
        """
        self.dialog_turn_result: DialogTurnResult = None
        self.dialog_context = None
        self.conversation_state: ConversationState = (
            ConversationState(MemoryStorage())
            if conversation_state is None
            else conversation_state
        )
        dialog_state = self.conversation_state.create_property("DialogState")
        self._callback = self._get_default_callback(
            target_dialog, initial_dialog_options, dialog_state
        )

        if isinstance(channel_or_adapter, str):
            conversation_reference = ConversationReference(
                channel_id=channel_or_adapter
            )
            self.test_adapter = TestAdapter(self._callback, conversation_reference)
            self.test_adapter.use(
                AutoSaveStateMiddleware().add(self.conversation_state)
            )
        else:
            self.test_adapter = channel_or_adapter

        self._add_user_middlewares(middlewares)

    async def send_activity(self, activity) -> Activity:
        """
        Send an activity into the dialog.

        :param activity: an activity potentially with text.
        :type activity:
        :return: a TestFlow that can be used to assert replies etc.
        :rtype: Activity
        """
        await self.test_adapter.receive_activity(activity)
        return self.test_adapter.get_next_activity()

    def get_next_reply(self) -> Activity:
        """
        Get the next reply waiting to be delivered (if one exists)

        :return: a TestFlow that can be used to assert replies etc.
        :rtype: Activity
        """
        return self.test_adapter.get_next_activity()

    def _get_default_callback(
        self,
        target_dialog: Dialog,
        initial_dialog_options: object,
        dialog_state: StatePropertyAccessor,
    ):
        async def default_callback(turn_context: TurnContext) -> None:
            dialog_set = DialogSet(dialog_state)
            dialog_set.add(target_dialog)

            self.dialog_context = await dialog_set.create_context(turn_context)
            self.dialog_turn_result = await self.dialog_context.continue_dialog()
            if self.dialog_turn_result.status == DialogTurnStatus.Empty:
                self.dialog_turn_result = await self.dialog_context.begin_dialog(
                    target_dialog.id, initial_dialog_options
                )

        return default_callback

    def _add_user_middlewares(self, middlewares: List[Middleware]) -> None:
        if middlewares is not None:
            for middleware in middlewares:
                self.test_adapter.use(middleware)
