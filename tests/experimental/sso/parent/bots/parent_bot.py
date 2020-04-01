from uuid import uuid4

from datetime import datetime
from http import HTTPStatus
from typing import List

from botbuilder.core import (
    ActivityHandler,
    BotFrameworkAdapter,
    BotFrameworkHttpClient,
    CardFactory,
    ConversationState,
    UserState,
    MessageFactory,
    TurnContext,
)
from botbuilder.schema import (
    Activity,
    ActivityTypes,
    ConversationAccount,
    DeliveryModes,
    ChannelAccount,
    OAuthCard,
    TokenExchangeInvokeRequest,
)
from botframework.connector.token_api.models import (
    TokenExchangeResource,
    TokenExchangeRequest,
)

from config import DefaultConfig
from helpers.dialog_helper import DialogHelper
from dialogs import MainDialog


class ParentBot(ActivityHandler):
    def __init__(
        self,
        skill_client: BotFrameworkHttpClient,
        config: DefaultConfig,
        dialog: MainDialog,
        conversation_state: ConversationState,
        user_state: UserState,
    ):
        self._client = skill_client
        self._conversation_state = conversation_state
        self._user_state = user_state
        self._dialog = dialog
        self._from_bot_id = config.APP_ID
        self._to_bot_id = config.SKILL_MICROSOFT_APP_ID
        self._connection_name = config.CONNECTION_NAME

    async def on_turn(self, turn_context: TurnContext):
        await super().on_turn(turn_context)

        await self._conversation_state.save_changes(turn_context)
        await self._user_state.save_changes(turn_context)

    async def on_message_activity(self, turn_context: TurnContext):
        # for signin, just use an oauth prompt to get the exchangeable token
        # also ensure that the channelId is not emulator
        if turn_context.activity.type != "emulator":
            if (
                turn_context.activity.text == "login"
                or turn_context.activity.text.isdigit()
            ):
                await self._conversation_state.load(turn_context, True)
                await self._user_state.load(turn_context, True)
                await DialogHelper.run_dialog(
                    self._dialog,
                    turn_context,
                    self._conversation_state.create_property("DialogState"),
                )
            elif turn_context.activity.text == "logout":
                bot_adapter = turn_context.adapter
                await bot_adapter.sign_out_user(turn_context, self._connection_name)
                await turn_context.send_activity(
                    MessageFactory.text("You have been signed out.")
                )
            elif turn_context.activity.text in ("skill login", "skill logout"):
                # incoming activity needs to be cloned for buffered replies
                clone_activity = MessageFactory.text(turn_context.activity.text)

                TurnContext.apply_conversation_reference(
                    clone_activity,
                    TurnContext.get_conversation_reference(turn_context.activity),
                    True,
                )

                clone_activity.delivery_mode = DeliveryModes.expect_replies

                activities = await self._client.post_buffered_activity(
                    self._from_bot_id,
                    self._to_bot_id,
                    "http://localhost:3979/api/messages",
                    "http://tempuri.org/whatever",
                    turn_context.activity.conversation.id,
                    clone_activity,
                )

                if activities:
                    if not await self._intercept_oauth_cards(
                        activities, turn_context
                    ):
                        await turn_context.send_activities(activities)

            return

        await turn_context.send_activity(MessageFactory.text("parent: before child"))

        activity = MessageFactory.text("parent: before child")
        TurnContext.apply_conversation_reference(
            activity,
            TurnContext.get_conversation_reference(turn_context.activity),
            True,
        )
        activity.delivery_mode = DeliveryModes.expect_replies

        activities = await self._client.post_buffered_activity(
            self._from_bot_id,
            self._to_bot_id,
            "http://localhost:3979/api/messages",
            "http://tempuri.org/whatever",
            str(uuid4()),
            activity,
        )

        await turn_context.send_activities(activities)
        await turn_context.send_activity(MessageFactory.text("parent: after child"))

    async def on_members_added_activity(
        self, members_added: List[ChannelAccount], turn_context: TurnContext
    ):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(
                    MessageFactory.text("Hello and welcome!")
                )

    async def _intercept_oauth_cards(
        self, activities: List[Activity], turn_context: TurnContext,
    ) -> bool:
        if not activities:
            return False
        activity = activities[0]

        if activity.attachments:
            for attachment in filter(
                lambda att: att.content_type == CardFactory.content_types.oauth_card,
                activity.attachments,
            ):
                oauth_card: OAuthCard = OAuthCard().from_dict(attachment.content)
                oauth_card.token_exchange_resource: TokenExchangeResource = TokenExchangeResource().from_dict(
                    oauth_card.token_exchange_resource
                )
                if oauth_card.token_exchange_resource:
                    token_exchange_provider: BotFrameworkAdapter = turn_context.adapter

                    result = await token_exchange_provider.exchange_token(
                        turn_context,
                        self._connection_name,
                        turn_context.activity.from_property.id,
                        TokenExchangeRequest(
                            uri=oauth_card.token_exchange_resource.uri
                        ),
                    )

                    if result.token:
                        return await self._send_token_exchange_invoke_to_skill(
                            turn_context,
                            activity,
                            oauth_card.token_exchange_resource.id,
                            result.token,
                        )
        return False

    async def _send_token_exchange_invoke_to_skill(
        self,
        turn_context: TurnContext,
        incoming_activity: Activity,
        identifier: str,
        token: str,
    ) -> bool:
        activity = self._create_reply(incoming_activity)
        activity.type = ActivityTypes.invoke
        activity.name = "signin/tokenExchange"
        activity.value = TokenExchangeInvokeRequest(id=identifier, token=token,)

        # route the activity to the skill
        response = await self._client.post_activity(
            self._from_bot_id,
            self._to_bot_id,
            "http://localhost:3979/api/messages",
            "http://tempuri.org/whatever",
            incoming_activity.conversation.id,
            activity,
        )

        # Check response status: true if success, false if failure
        is_success = int(HTTPStatus.OK) <= response.status <= 299
        message = (
            "Skill token exchange successful"
            if is_success
            else "Skill token exchange failed"
        )

        await turn_context.send_activity(MessageFactory.text(message))

        return is_success

    def _create_reply(self, activity) -> Activity:
        return Activity(
            type=ActivityTypes.message,
            timestamp=datetime.utcnow(),
            from_property=ChannelAccount(
                id=activity.recipient.id, name=activity.recipient.name
            ),
            recipient=ChannelAccount(
                id=activity.from_property.id, name=activity.from_property.name
            ),
            reply_to_id=activity.id,
            service_url=activity.service_url,
            channel_id=activity.channel_id,
            conversation=ConversationAccount(
                is_group=activity.conversation.is_group,
                id=activity.conversation.id,
                name=activity.conversation.name,
            ),
            text="",
            locale=activity.locale,
        )
