# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from datetime import datetime, timedelta
from threading import Lock
from warnings import warn

from botbuilder.core import (
    BotAdapter,
    BotStateSet,
    ConversationState,
    UserState,
    TurnContext,
)
from botbuilder.core.skills import SkillConversationReference, SkillHandler
from botbuilder.dialogs.memory import DialogStateManagerConfiguration
from botbuilder.schema import Activity, ActivityTypes, EndOfConversationCodes
from botframework.connector.auth import (
    AuthenticationConstants,
    ClaimsIdentity,
    GovernmentConstants,
    SkillValidation,
)

from .dialog import Dialog
from .dialog_context import DialogContext
from .dialog_events import DialogEvents
from .dialog_extensions import DialogExtensions
from .dialog_set import DialogSet
from .dialog_state import DialogState
from .dialog_manager_result import DialogManagerResult
from .dialog_turn_status import DialogTurnStatus
from .dialog_turn_result import DialogTurnResult


class DialogManager:
    """
    Class which runs the dialog system.
    """

    def __init__(self, root_dialog: Dialog = None, dialog_state_property: str = None):
        """
        Initializes a instance of the <see cref="DialogManager"/> class.
        :param root_dialog: Root dialog to use.
        :param dialog_state_property: alternate name for the dialog_state property. (Default is "DialogState").
        """
        self.last_access = "_lastAccess"
        self._root_dialog_id = ""
        self._dialog_state_property = dialog_state_property or "DialogState"
        self._lock = Lock()

        # Gets or sets root dialog to use to start conversation.
        self.root_dialog = root_dialog

        # Gets or sets the ConversationState.
        self.conversation_state: ConversationState = None

        # Gets or sets the UserState.
        self.user_state: UserState = None

        # Gets InitialTurnState collection to copy into the TurnState on every turn.
        self.initial_turn_state = {}

        # Gets or sets global dialogs that you want to have be callable.
        self.dialogs = DialogSet()

        # Gets or sets the DialogStateManagerConfiguration.
        self.state_configuration: DialogStateManagerConfiguration = None

        # Gets or sets (optional) number of milliseconds to expire the bot's state after.
        self.expire_after: int = None

    async def on_turn(self, context: TurnContext) -> DialogManagerResult:
        """
        Runs dialog system in the context of an ITurnContext.
        :param context: turn context.
        :return:
        """
        # pylint: disable=too-many-statements
        # Lazy initialize RootDialog so it can refer to assets like LG function templates
        if not self._root_dialog_id:
            with self._lock:
                if not self._root_dialog_id:
                    self._root_dialog_id = self.root_dialog.id
                    # self.dialogs = self.root_dialog.telemetry_client
                    self.dialogs.add(self.root_dialog)

        bot_state_set = BotStateSet([])

        # Preload TurnState with DM TurnState.
        for key, val in self.initial_turn_state.items():
            context.turn_state[key] = val

        # register DialogManager with TurnState.
        context.turn_state[DialogManager.__name__] = self
        conversation_state_name = ConversationState.__name__
        if self.conversation_state is None:
            if conversation_state_name not in context.turn_state:
                raise Exception(
                    f"Unable to get an instance of {conversation_state_name} from turn_context."
                )
            self.conversation_state: ConversationState = context.turn_state[
                conversation_state_name
            ]
        else:
            context.turn_state[conversation_state_name] = self.conversation_state

        bot_state_set.add(self.conversation_state)

        user_state_name = UserState.__name__
        if self.user_state is None:
            self.user_state = context.turn_state.get(user_state_name, None)
        else:
            context.turn_state[user_state_name] = self.user_state

        if self.user_state is not None:
            self.user_state: UserState = self.user_state
            bot_state_set.add(self.user_state)

        # create property accessors
        # DateTime(last_access)
        last_access_property = self.conversation_state.create_property(self.last_access)
        last_access: datetime = await last_access_property.get(context, datetime.now)

        # Check for expired conversation
        if self.expire_after is not None and (
            datetime.now() - last_access
        ) >= timedelta(milliseconds=float(self.expire_after)):
            # Clear conversation state
            await self.conversation_state.clear_state(context)

        last_access = datetime.now()
        await last_access_property.set(context, last_access)

        # get dialog stack
        dialogs_property = self.conversation_state.create_property(
            self._dialog_state_property
        )
        dialog_state: DialogState = await dialogs_property.get(context, DialogState)

        # Create DialogContext
        dialog_context = DialogContext(self.dialogs, context, dialog_state)

        # Call the common dialog "continue/begin" execution pattern shared with the classic RunAsync extension method
        turn_result = (
            await DialogExtensions._internal_run(  # pylint: disable=protected-access
                context, self._root_dialog_id, dialog_context
            )
        )

        # save BotState changes
        await bot_state_set.save_all_changes(dialog_context.context, False)

        return DialogManagerResult(turn_result=turn_result)

    @staticmethod
    async def send_state_snapshot_trace(
        dialog_context: DialogContext,
        trace_label: str = None,  # pylint: disable=unused-argument
    ):
        """
        Helper to send a trace activity with a memory snapshot of the active dialog DC.
        :param dialog_context:
        :param trace_label:
        :return:
        """
        warn(
            "This method will be deprecated as no longer is necesary",
            PendingDeprecationWarning,
        )
        await DialogExtensions._send_state_snapshot_trace(  # pylint: disable=protected-access
            dialog_context
        )

    @staticmethod
    def is_from_parent_to_skill(turn_context: TurnContext) -> bool:
        if turn_context.turn_state.get(
            SkillHandler.SKILL_CONVERSATION_REFERENCE_KEY, None
        ):
            return False

        claims_identity: ClaimsIdentity = turn_context.turn_state.get(
            BotAdapter.BOT_IDENTITY_KEY, None
        )
        return isinstance(
            claims_identity, ClaimsIdentity
        ) and SkillValidation.is_skill_claim(claims_identity.claims)

    # Recursively walk up the DC stack to find the active DC.
    @staticmethod
    def get_active_dialog_context(dialog_context: DialogContext) -> DialogContext:
        """
        Recursively walk up the DC stack to find the active DC.
        :param dialog_context:
        :return:
        """
        warn(
            "This method will be deprecated as no longer is necesary",
            PendingDeprecationWarning,
        )
        return DialogExtensions._get_active_dialog_context(  # pylint: disable=protected-access
            dialog_context
        )

    @staticmethod
    def should_send_end_of_conversation_to_parent(
        context: TurnContext, turn_result: DialogTurnResult
    ) -> bool:
        """
        Helper to determine if we should send an EndOfConversation to the parent or not.
        :param context:
        :param turn_result:
        :return:
        """
        if not (
            turn_result.status == DialogTurnStatus.Complete
            or turn_result.status == DialogTurnStatus.Cancelled
        ):
            # The dialog is still going, don't return EoC.
            return False
        claims_identity: ClaimsIdentity = context.turn_state.get(
            BotAdapter.BOT_IDENTITY_KEY, None
        )
        if isinstance(
            claims_identity, ClaimsIdentity
        ) and SkillValidation.is_skill_claim(claims_identity.claims):
            # EoC Activities returned by skills are bounced back to the bot by SkillHandler.
            # In those cases we will have a SkillConversationReference instance in state.
            skill_conversation_reference: SkillConversationReference = (
                context.turn_state.get(SkillHandler.SKILL_CONVERSATION_REFERENCE_KEY)
            )
            if skill_conversation_reference:
                # If the skill_conversation_reference.OAuthScope is for one of the supported channels, we are at the
                # root and we should not send an EoC.
                return skill_conversation_reference.oauth_scope not in (
                    AuthenticationConstants.TO_CHANNEL_FROM_BOT_OAUTH_SCOPE,
                    GovernmentConstants.TO_CHANNEL_FROM_BOT_OAUTH_SCOPE,
                )

            return True

        return False

    async def handle_skill_on_turn(
        self, dialog_context: DialogContext
    ) -> DialogTurnResult:
        warn(
            "This method will be deprecated as no longer is necesary",
            PendingDeprecationWarning,
        )
        # the bot is running as a skill.
        turn_context = dialog_context.context

        # Process remote cancellation
        if (
            turn_context.activity.type == ActivityTypes.end_of_conversation
            and dialog_context.active_dialog is not None
            and self.is_from_parent_to_skill(turn_context)
        ):
            # Handle remote cancellation request from parent.
            active_dialog_context = self.get_active_dialog_context(dialog_context)

            # Send cancellation message to the top dialog in the stack to ensure all the parents are canceled in the
            # right order.
            return await active_dialog_context.cancel_all_dialogs(True)

        # Handle reprompt
        # Process a reprompt event sent from the parent.
        if (
            turn_context.activity.type == ActivityTypes.event
            and turn_context.activity.name == DialogEvents.reprompt_dialog
        ):
            if not dialog_context.active_dialog:
                return DialogTurnResult(DialogTurnStatus.Empty)

            await dialog_context.reprompt_dialog()
            return DialogTurnResult(DialogTurnStatus.Waiting)

        # Continue execution
        # - This will apply any queued up interruptions and execute the current/next step(s).
        turn_result = await dialog_context.continue_dialog()
        if turn_result.status == DialogTurnStatus.Empty:
            # restart root dialog
            turn_result = await dialog_context.begin_dialog(self._root_dialog_id)

        await DialogManager.send_state_snapshot_trace(dialog_context, "Skill State")

        if self.should_send_end_of_conversation_to_parent(turn_context, turn_result):
            # Send End of conversation at the end.
            activity = Activity(
                type=ActivityTypes.end_of_conversation,
                value=turn_result.result,
                locale=turn_context.activity.locale,
                code=(
                    EndOfConversationCodes.completed_successfully
                    if turn_result.status == DialogTurnStatus.Complete
                    else EndOfConversationCodes.user_cancelled
                ),
            )
            await turn_context.send_activity(activity)

        return turn_result

    async def handle_bot_on_turn(
        self, dialog_context: DialogContext
    ) -> DialogTurnResult:
        warn(
            "This method will be deprecated as no longer is necesary",
            PendingDeprecationWarning,
        )
        # the bot is running as a root bot.
        if dialog_context.active_dialog is None:
            # start root dialog
            turn_result = await dialog_context.begin_dialog(self._root_dialog_id)
        else:
            # Continue execution
            # - This will apply any queued up interruptions and execute the current/next step(s).
            turn_result = await dialog_context.continue_dialog()

            if turn_result.status == DialogTurnStatus.Empty:
                # restart root dialog
                turn_result = await dialog_context.begin_dialog(self._root_dialog_id)

        await self.send_state_snapshot_trace(dialog_context, "Bot State")

        return turn_result
