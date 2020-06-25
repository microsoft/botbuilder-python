# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from http import HTTPStatus
from botbuilder.schema import ChannelAccount, ErrorResponseException, SignInConstants
from botbuilder.core import ActivityHandler, InvokeResponse
from botbuilder.core.activity_handler import _InvokeResponseException
from botbuilder.core.turn_context import TurnContext
from botbuilder.core.teams.teams_info import TeamsInfo
from botbuilder.schema.teams import (
    AppBasedLinkQuery,
    TeamInfo,
    ChannelInfo,
    FileConsentCardResponse,
    TeamsChannelData,
    TeamsChannelAccount,
    MessagingExtensionAction,
    MessagingExtensionQuery,
    MessagingExtensionActionResponse,
    MessagingExtensionResponse,
    O365ConnectorCardActionQuery,
    TaskModuleRequest,
    TaskModuleResponse,
)
from botframework.connector import Channels
from ..serializer_helper import deserializer_helper


class TeamsActivityHandler(ActivityHandler):
    async def on_invoke_activity(self, turn_context: TurnContext) -> InvokeResponse:
        try:
            if (
                not turn_context.activity.name
                and turn_context.activity.channel_id == Channels.ms_teams
            ):
                return await self.on_teams_card_action_invoke(turn_context)

            if (
                turn_context.activity.name
                == SignInConstants.token_exchange_operation_name
            ):
                await self.on_teams_signin_token_exchange(turn_context)
                return self._create_invoke_response()

            if turn_context.activity.name == "fileConsent/invoke":
                return await self.on_teams_file_consent(
                    turn_context,
                    deserializer_helper(
                        FileConsentCardResponse, turn_context.activity.value
                    ),
                )

            if turn_context.activity.name == "actionableMessage/executeAction":
                await self.on_teams_o365_connector_card_action(
                    turn_context,
                    deserializer_helper(
                        O365ConnectorCardActionQuery, turn_context.activity.value
                    ),
                )
                return self._create_invoke_response()

            if turn_context.activity.name == "composeExtension/queryLink":
                return self._create_invoke_response(
                    await self.on_teams_app_based_link_query(
                        turn_context,
                        deserializer_helper(
                            AppBasedLinkQuery, turn_context.activity.value
                        ),
                    )
                )

            if turn_context.activity.name == "composeExtension/query":
                return self._create_invoke_response(
                    await self.on_teams_messaging_extension_query(
                        turn_context,
                        deserializer_helper(
                            MessagingExtensionQuery, turn_context.activity.value
                        ),
                    )
                )

            if turn_context.activity.name == "composeExtension/selectItem":
                return self._create_invoke_response(
                    await self.on_teams_messaging_extension_select_item(
                        turn_context, turn_context.activity.value
                    )
                )

            if turn_context.activity.name == "composeExtension/submitAction":
                return self._create_invoke_response(
                    await self.on_teams_messaging_extension_submit_action_dispatch(
                        turn_context,
                        deserializer_helper(
                            MessagingExtensionAction, turn_context.activity.value
                        ),
                    )
                )

            if turn_context.activity.name == "composeExtension/fetchTask":
                return self._create_invoke_response(
                    await self.on_teams_messaging_extension_fetch_task(
                        turn_context,
                        deserializer_helper(
                            MessagingExtensionAction, turn_context.activity.value,
                        ),
                    )
                )

            if turn_context.activity.name == "composeExtension/querySettingUrl":
                return self._create_invoke_response(
                    await self.on_teams_messaging_extension_configuration_query_settings_url(
                        turn_context,
                        deserializer_helper(
                            MessagingExtensionQuery, turn_context.activity.value
                        ),
                    )
                )

            if turn_context.activity.name == "composeExtension/setting":
                await self.on_teams_messaging_extension_configuration_setting(
                    turn_context, turn_context.activity.value
                )
                return self._create_invoke_response()

            if turn_context.activity.name == "composeExtension/onCardButtonClicked":
                await self.on_teams_messaging_extension_card_button_clicked(
                    turn_context, turn_context.activity.value
                )
                return self._create_invoke_response()

            if turn_context.activity.name == "task/fetch":
                return self._create_invoke_response(
                    await self.on_teams_task_module_fetch(
                        turn_context,
                        deserializer_helper(
                            TaskModuleRequest, turn_context.activity.value
                        ),
                    )
                )

            if turn_context.activity.name == "task/submit":
                return self._create_invoke_response(
                    await self.on_teams_task_module_submit(
                        turn_context,
                        deserializer_helper(
                            TaskModuleRequest, turn_context.activity.value
                        ),
                    )
                )

            return await super().on_invoke_activity(turn_context)

        except _InvokeResponseException as invoke_exception:
            return invoke_exception.create_invoke_response()

    async def on_sign_in_invoke(self, turn_context: TurnContext):
        return await self.on_teams_signin_verify_state(turn_context)

    async def on_teams_card_action_invoke(
        self, turn_context: TurnContext
    ) -> InvokeResponse:
        raise _InvokeResponseException(status_code=HTTPStatus.NOT_IMPLEMENTED)

    async def on_teams_signin_verify_state(self, turn_context: TurnContext):
        raise _InvokeResponseException(status_code=HTTPStatus.NOT_IMPLEMENTED)

    async def on_teams_signin_token_exchange(self, turn_context: TurnContext):
        raise _InvokeResponseException(status_code=HTTPStatus.NOT_IMPLEMENTED)

    async def on_teams_file_consent(
        self,
        turn_context: TurnContext,
        file_consent_card_response: FileConsentCardResponse,
    ) -> InvokeResponse:
        if file_consent_card_response.action == "accept":
            await self.on_teams_file_consent_accept(
                turn_context, file_consent_card_response
            )
            return self._create_invoke_response()

        if file_consent_card_response.action == "decline":
            await self.on_teams_file_consent_decline(
                turn_context, file_consent_card_response
            )
            return self._create_invoke_response()

        raise _InvokeResponseException(
            HTTPStatus.BAD_REQUEST,
            f"{file_consent_card_response.action} is not a supported Action.",
        )

    async def on_teams_file_consent_accept(  # pylint: disable=unused-argument
        self,
        turn_context: TurnContext,
        file_consent_card_response: FileConsentCardResponse,
    ):
        raise _InvokeResponseException(status_code=HTTPStatus.NOT_IMPLEMENTED)

    async def on_teams_file_consent_decline(  # pylint: disable=unused-argument
        self,
        turn_context: TurnContext,
        file_consent_card_response: FileConsentCardResponse,
    ):
        raise _InvokeResponseException(status_code=HTTPStatus.NOT_IMPLEMENTED)

    async def on_teams_o365_connector_card_action(  # pylint: disable=unused-argument
        self, turn_context: TurnContext, query: O365ConnectorCardActionQuery
    ):
        raise _InvokeResponseException(status_code=HTTPStatus.NOT_IMPLEMENTED)

    async def on_teams_app_based_link_query(  # pylint: disable=unused-argument
        self, turn_context: TurnContext, query: AppBasedLinkQuery
    ) -> MessagingExtensionResponse:
        raise _InvokeResponseException(status_code=HTTPStatus.NOT_IMPLEMENTED)

    async def on_teams_messaging_extension_query(  # pylint: disable=unused-argument
        self, turn_context: TurnContext, query: MessagingExtensionQuery
    ) -> MessagingExtensionResponse:
        raise _InvokeResponseException(status_code=HTTPStatus.NOT_IMPLEMENTED)

    async def on_teams_messaging_extension_select_item(  # pylint: disable=unused-argument
        self, turn_context: TurnContext, query
    ) -> MessagingExtensionResponse:
        raise _InvokeResponseException(status_code=HTTPStatus.NOT_IMPLEMENTED)

    async def on_teams_messaging_extension_submit_action_dispatch(
        self, turn_context: TurnContext, action: MessagingExtensionAction
    ) -> MessagingExtensionActionResponse:
        if not action.bot_message_preview_action:
            return await self.on_teams_messaging_extension_submit_action(
                turn_context, action
            )

        if action.bot_message_preview_action == "edit":
            return await self.on_teams_messaging_extension_bot_message_preview_edit(
                turn_context, action
            )

        if action.bot_message_preview_action == "send":
            return await self.on_teams_messaging_extension_bot_message_preview_send(
                turn_context, action
            )

        raise _InvokeResponseException(
            status_code=HTTPStatus.BAD_REQUEST,
            body=f"{action.bot_message_preview_action} is not a supported BotMessagePreviewAction",
        )

    async def on_teams_messaging_extension_bot_message_preview_edit(  # pylint: disable=unused-argument
        self, turn_context: TurnContext, action: MessagingExtensionAction
    ) -> MessagingExtensionActionResponse:
        raise _InvokeResponseException(status_code=HTTPStatus.NOT_IMPLEMENTED)

    async def on_teams_messaging_extension_bot_message_preview_send(  # pylint: disable=unused-argument
        self, turn_context: TurnContext, action: MessagingExtensionAction
    ) -> MessagingExtensionActionResponse:
        raise _InvokeResponseException(status_code=HTTPStatus.NOT_IMPLEMENTED)

    async def on_teams_messaging_extension_submit_action(  # pylint: disable=unused-argument
        self, turn_context: TurnContext, action: MessagingExtensionAction
    ) -> MessagingExtensionActionResponse:
        raise _InvokeResponseException(status_code=HTTPStatus.NOT_IMPLEMENTED)

    async def on_teams_messaging_extension_fetch_task(  # pylint: disable=unused-argument
        self, turn_context: TurnContext, action: MessagingExtensionAction
    ) -> MessagingExtensionActionResponse:
        raise _InvokeResponseException(status_code=HTTPStatus.NOT_IMPLEMENTED)

    async def on_teams_messaging_extension_configuration_query_settings_url(  # pylint: disable=unused-argument
        self, turn_context: TurnContext, query: MessagingExtensionQuery
    ) -> MessagingExtensionResponse:
        raise _InvokeResponseException(status_code=HTTPStatus.NOT_IMPLEMENTED)

    async def on_teams_messaging_extension_configuration_setting(  # pylint: disable=unused-argument
        self, turn_context: TurnContext, settings
    ):
        raise _InvokeResponseException(status_code=HTTPStatus.NOT_IMPLEMENTED)

    async def on_teams_messaging_extension_card_button_clicked(  # pylint: disable=unused-argument
        self, turn_context: TurnContext, card_data
    ):
        raise _InvokeResponseException(status_code=HTTPStatus.NOT_IMPLEMENTED)

    async def on_teams_task_module_fetch(  # pylint: disable=unused-argument
        self, turn_context: TurnContext, task_module_request: TaskModuleRequest
    ) -> TaskModuleResponse:
        raise _InvokeResponseException(status_code=HTTPStatus.NOT_IMPLEMENTED)

    async def on_teams_task_module_submit(  # pylint: disable=unused-argument
        self, turn_context: TurnContext, task_module_request: TaskModuleRequest
    ) -> TaskModuleResponse:
        raise _InvokeResponseException(status_code=HTTPStatus.NOT_IMPLEMENTED)

    async def on_conversation_update_activity(self, turn_context: TurnContext):

        if turn_context.activity.channel_id == Channels.ms_teams:
            channel_data = TeamsChannelData().deserialize(
                turn_context.activity.channel_data
            )
            if turn_context.activity.members_added:
                return await self.on_teams_members_added_dispatch(
                    turn_context.activity.members_added, channel_data.team, turn_context
                )

            if turn_context.activity.members_removed:
                return await self.on_teams_members_removed_dispatch(
                    turn_context.activity.members_removed,
                    channel_data.team,
                    turn_context,
                )

            if channel_data:
                if channel_data.event_type == "channelCreated":
                    return await self.on_teams_channel_created(
                        ChannelInfo().deserialize(channel_data.channel),
                        channel_data.team,
                        turn_context,
                    )
                if channel_data.event_type == "channelDeleted":
                    return await self.on_teams_channel_deleted(
                        channel_data.channel, channel_data.team, turn_context
                    )
                if channel_data.event_type == "channelRenamed":
                    return await self.on_teams_channel_renamed(
                        channel_data.channel, channel_data.team, turn_context
                    )
                if channel_data.event_type == "teamRenamed":
                    return await self.on_teams_team_renamed_activity(
                        channel_data.team, turn_context
                    )

        return await super().on_conversation_update_activity(turn_context)

    async def on_teams_channel_created(  # pylint: disable=unused-argument
        self, channel_info: ChannelInfo, team_info: TeamInfo, turn_context: TurnContext
    ):
        return

    async def on_teams_team_renamed_activity(  # pylint: disable=unused-argument
        self, team_info: TeamInfo, turn_context: TurnContext
    ):
        return

    async def on_teams_members_added_dispatch(  # pylint: disable=unused-argument
        self,
        members_added: [ChannelAccount],
        team_info: TeamInfo,
        turn_context: TurnContext,
    ):

        team_members_added = []
        for member in members_added:
            is_bot = (
                turn_context.activity.recipient is not None
                and member.id == turn_context.activity.recipient.id
            )
            if member.additional_properties != {} or is_bot:
                team_members_added.append(
                    deserializer_helper(TeamsChannelAccount, member)
                )
            else:
                team_member = None
                try:
                    team_member = await TeamsInfo.get_member(turn_context, member.id)
                    team_members_added.append(team_member)
                except ErrorResponseException as ex:
                    if (
                        ex.error
                        and ex.error.error
                        and ex.error.error.code == "ConversationNotFound"
                    ):
                        new_teams_channel_account = TeamsChannelAccount(
                            id=member.id,
                            name=member.name,
                            aad_object_id=member.aad_object_id,
                            role=member.role,
                        )
                        team_members_added.append(new_teams_channel_account)
                    else:
                        raise ex

        return await self.on_teams_members_added(
            team_members_added, team_info, turn_context
        )

    async def on_teams_members_added(  # pylint: disable=unused-argument
        self,
        teams_members_added: [TeamsChannelAccount],
        team_info: TeamInfo,
        turn_context: TurnContext,
    ):
        teams_members_added = [
            ChannelAccount().deserialize(member.serialize())
            for member in teams_members_added
        ]
        return await super().on_members_added_activity(
            teams_members_added, turn_context
        )

    async def on_teams_members_removed_dispatch(  # pylint: disable=unused-argument
        self,
        members_removed: [ChannelAccount],
        team_info: TeamInfo,
        turn_context: TurnContext,
    ):
        teams_members_removed = []
        for member in members_removed:
            new_account_json = member.serialize()
            if "additional_properties" in new_account_json:
                del new_account_json["additional_properties"]
            teams_members_removed.append(
                TeamsChannelAccount().deserialize(new_account_json)
            )

        return await self.on_teams_members_removed(
            teams_members_removed, team_info, turn_context
        )

    async def on_teams_members_removed(  # pylint: disable=unused-argument
        self,
        teams_members_removed: [TeamsChannelAccount],
        team_info: TeamInfo,
        turn_context: TurnContext,
    ):
        members_removed = [
            ChannelAccount().deserialize(member.serialize())
            for member in teams_members_removed
        ]
        return await super().on_members_removed_activity(members_removed, turn_context)

    async def on_teams_channel_deleted(  # pylint: disable=unused-argument
        self, channel_info: ChannelInfo, team_info: TeamInfo, turn_context: TurnContext
    ):
        return

    async def on_teams_channel_renamed(  # pylint: disable=unused-argument
        self, channel_info: ChannelInfo, team_info: TeamInfo, turn_context: TurnContext
    ):
        return
