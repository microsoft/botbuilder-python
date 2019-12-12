# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from http import HTTPStatus
from botbuilder.schema import Activity, ActivityTypes, ChannelAccount
from botbuilder.core import ActivityHandler, InvokeResponse, BotFrameworkAdapter
from botbuilder.core.turn_context import TurnContext
from botbuilder.core.teams.teams_info import TeamsInfo
from botbuilder.core.teams.teams_helper import deserializer_helper
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


class TeamsActivityHandler(ActivityHandler):
    async def on_turn(self, turn_context: TurnContext):
        if turn_context is None:
            raise TypeError("ActivityHandler.on_turn(): turn_context cannot be None.")

        if not getattr(turn_context, "activity", None):
            raise TypeError(
                "ActivityHandler.on_turn(): turn_context must have a non-None activity."
            )

        if not getattr(turn_context.activity, "type", None):
            raise TypeError(
                "ActivityHandler.on_turn(): turn_context activity must have a non-None type."
            )

        if turn_context.activity.type == ActivityTypes.invoke:
            invoke_response = await self.on_invoke_activity(turn_context)
            if invoke_response and not turn_context.turn_state.get(
                BotFrameworkAdapter._INVOKE_RESPONSE_KEY  # pylint: disable=protected-access
            ):
                await turn_context.send_activity(
                    Activity(value=invoke_response, type=ActivityTypes.invoke_response)
                )
            return

        await super().on_turn(turn_context)

    async def on_invoke_activity(self, turn_context: TurnContext) -> InvokeResponse:
        try:
            if (
                not turn_context.activity.name
                and turn_context.activity.channel_id == Channels.ms_teams
            ):
                return await self.on_teams_card_action_invoke_activity(turn_context)

            if turn_context.activity.name == "signin/verifyState":
                await self.on_teams_signin_verify_state(turn_context)
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

            raise _InvokeResponseException(status_code=HTTPStatus.NOT_IMPLEMENTED)
        except _InvokeResponseException as err:
            return err.create_invoke_response()

    async def on_teams_card_action_invoke_activity(
        self, turn_context: TurnContext
    ) -> InvokeResponse:
        raise _InvokeResponseException(status_code=HTTPStatus.NOT_IMPLEMENTED)

    async def on_teams_signin_verify_state(self, turn_context: TurnContext):
        raise _InvokeResponseException(status_code=HTTPStatus.NOT_IMPLEMENTED)

    async def on_teams_file_consent(
        self,
        turn_context: TurnContext,
        file_consent_card_response: FileConsentCardResponse,
    ) -> InvokeResponse:
        if file_consent_card_response.action == "accept":
            await self.on_teams_file_consent_accept_activity(
                turn_context, file_consent_card_response
            )
            return self._create_invoke_response()

        if file_consent_card_response.action == "decline":
            await self.on_teams_file_consent_decline_activity(
                turn_context, file_consent_card_response
            )
            return self._create_invoke_response()

        raise _InvokeResponseException(
            HTTPStatus.BAD_REQUEST,
            f"{file_consent_card_response.action} is not a supported Action.",
        )

    async def on_teams_file_consent_accept_activity(  # pylint: disable=unused-argument
        self,
        turn_context: TurnContext,
        file_consent_card_response: FileConsentCardResponse,
    ):
        raise _InvokeResponseException(status_code=HTTPStatus.NOT_IMPLEMENTED)

    async def on_teams_file_consent_decline_activity(  # pylint: disable=unused-argument
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
            return await self.on_teams_messaging_extension_submit_action_activity(
                turn_context, action
            )

        if action.bot_message_preview_action == "edit":
            return await self.on_teams_messaging_extension_bot_message_preview_edit_activity(
                turn_context, action
            )

        if action.bot_message_preview_action == "send":
            return await self.on_teams_messaging_extension_bot_message_preview_send_activity(
                turn_context, action
            )

        raise _InvokeResponseException(
            status_code=HTTPStatus.BAD_REQUEST,
            body=f"{action.bot_message_preview_action} is not a supported BotMessagePreviewAction",
        )

    async def on_teams_messaging_extension_bot_message_preview_edit_activity(  # pylint: disable=unused-argument
        self, turn_context: TurnContext, action
    ) -> MessagingExtensionActionResponse:
        raise _InvokeResponseException(status_code=HTTPStatus.NOT_IMPLEMENTED)

    async def on_teams_messaging_extension_bot_message_preview_send_activity(  # pylint: disable=unused-argument
        self, turn_context: TurnContext, action
    ) -> MessagingExtensionActionResponse:
        raise _InvokeResponseException(status_code=HTTPStatus.NOT_IMPLEMENTED)

    async def on_teams_messaging_extension_submit_action_activity(  # pylint: disable=unused-argument
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
                return await self.on_teams_members_added_dispatch_activity(
                    turn_context.activity.members_added, channel_data.team, turn_context
                )

            if turn_context.activity.members_removed:
                return await self.on_teams_members_removed_dispatch_activity(
                    turn_context.activity.members_removed,
                    channel_data.team,
                    turn_context,
                )

            if channel_data:
                if channel_data.event_type == "channelCreated":
                    return await self.on_teams_channel_created_activity(
                        ChannelInfo().deserialize(channel_data.channel),
                        channel_data.team,
                        turn_context,
                    )
                if channel_data.event_type == "channelDeleted":
                    return await self.on_teams_channel_deleted_activity(
                        channel_data.channel, channel_data.team, turn_context
                    )
                if channel_data.event_type == "channelRenamed":
                    return await self.on_teams_channel_renamed_activity(
                        channel_data.channel, channel_data.team, turn_context
                    )
                if channel_data.event_type == "teamRenamed":
                    return await self.on_teams_team_renamed_activity(
                        channel_data.team, turn_context
                    )
                return await super().on_conversation_update_activity(turn_context)

        return await super().on_conversation_update_activity(turn_context)

    async def on_teams_channel_created_activity(  # pylint: disable=unused-argument
        self, channel_info: ChannelInfo, team_info: TeamInfo, turn_context: TurnContext
    ):
        return

    async def on_teams_team_renamed_activity(  # pylint: disable=unused-argument
        self, team_info: TeamInfo, turn_context: TurnContext
    ):
        return

    async def on_teams_members_added_dispatch_activity(  # pylint: disable=unused-argument
        self,
        members_added: [ChannelAccount],
        team_info: TeamInfo,
        turn_context: TurnContext,
    ):

        team_members = {}
        team_members_added = []
        for member in members_added:
            if member.additional_properties != {}:
                team_members_added.append(
                    deserializer_helper(TeamsChannelAccount, member)
                )
            else:
                if team_members == {}:
                    result = await TeamsInfo.get_members(turn_context)
                    team_members = {i.id: i for i in result}

                if member.id in team_members:
                    team_members_added.append(member)
                else:
                    new_teams_channel_account = TeamsChannelAccount(
                        id=member.id,
                        name=member.name,
                        aad_object_id=member.aad_object_id,
                        role=member.role,
                    )
                    team_members_added.append(new_teams_channel_account)

        return await self.on_teams_members_added_activity(
            team_members_added, team_info, turn_context
        )

    async def on_teams_members_added_activity(  # pylint: disable=unused-argument
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

    async def on_teams_members_removed_dispatch_activity(  # pylint: disable=unused-argument
        self,
        members_removed: [ChannelAccount],
        team_info: TeamInfo,
        turn_context: TurnContext,
    ):
        teams_members_removed = []
        for member in members_removed:
            # TODO: fix this
            new_account_json = member.serialize()
            if "additional_properties" in new_account_json:
                del new_account_json["additional_properties"]
            teams_members_removed.append(
                TeamsChannelAccount().deserialize(new_account_json)
            )

        return await self.on_teams_members_removed_activity(
            teams_members_removed, turn_context
        )

    async def on_teams_members_removed_activity(
        self, teams_members_removed: [TeamsChannelAccount], turn_context: TurnContext
    ):
        members_removed = [
            ChannelAccount().deserialize(member.serialize())
            for member in teams_members_removed
        ]
        return await super().on_members_removed_activity(members_removed, turn_context)

    async def on_teams_channel_deleted_activity(  # pylint: disable=unused-argument
        self, channel_info: ChannelInfo, team_info: TeamInfo, turn_context: TurnContext
    ):
        return  # Task.CompleteTask

    async def on_teams_channel_renamed_activity(  # pylint: disable=unused-argument
        self, channel_info: ChannelInfo, team_info: TeamInfo, turn_context: TurnContext
    ):
        return  # Task.CompleteTask

    @staticmethod
    def _create_invoke_response(body: object = None) -> InvokeResponse:
        return InvokeResponse(status=int(HTTPStatus.OK), body=body)


class _InvokeResponseException(Exception):
    def __init__(self, status_code: HTTPStatus, body: object = None):
        super(_InvokeResponseException, self).__init__()
        self._status_code = status_code
        self._body = body

    def create_invoke_response(self) -> InvokeResponse:
        return InvokeResponse(status=int(self._status_code), body=self._body)
