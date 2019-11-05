# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List

from botbuilder.schema import ActivityTypes, ChannelAccount, MessageReaction
from botbuilder.schema.teams import TeamInfo
from .turn_context import TurnContext
from activity_handler import ActivityHandler
from botframework.connector import Channels
from http import HTTPStatus
from botbuilder.core import InvokeResponse


class TeamsActivityHandler(ActivityHandler):
    async def on_turn(self, turn_context: TurnContext):
        if turn_context is None:
            raise TypeError("ActivityHandler.on_turn(): turn_context cannot be None.")

        if hasattr(turn_context, "activity") and turn_context.activity is None:
            raise TypeError(
                "ActivityHandler.on_turn(): turn_context must have a non-None activity."
            )

        if (
            hasattr(turn_context.activity, "type")
            and turn_context.activity.type is None
        ):
            raise TypeError(
                "ActivityHandler.on_turn(): turn_context activity must have a non-None type."
            )

        if turn_context.activity.type == ActivityTypes.Invoke:
            pass
        else:
            await super(on_turn(turn_context))
        
        return

    async def on_invoke_activity_async(self, turn_context: TurnContext):
        try:
            if turn_context.activity.name == None and turn_context.activity.channel_id == Channels.ms_teams:
                return await on_teams_card_action_invoke(turn_context)
            else:
                if turn_context.activity.name == "signin/verifyState":
                    await on_teams_signin_verify_state_async(turn_context)
                    return _create_invoke_response()
                elif turn_context.activity.name == "fileConsent/invoke":
                    await on_teams_file_concent_async(turn_context, turn_context.activity.value)
                    return _create_invoke_response()
                elif turn_context.activity.name == "actionableMessage/executeAction":
                    await on_teams_o365_connector_card_action_async(turn_context, turn_context.activity.value)
                    return _create_invoke_response()
                elif turn_context.activity.name == "composeExtension/queryLink":
                    return createInvokeResponse(await on_teams_app_based_link_query_async(turn_context, turn_context.activity.value))
                elif turn_context.activity.name == "composeExtension/query":
                    return _create_invoke_response(await on_teams_messaging_extension_query_async(turn_context, turn_context.activity.value))
                elif turn_context.activity.name == "composeExtension/selectItem":
                    return _create_invoke_response(await on_teams_messaging_extension_select_item_async(turn_context, turn_context.activity.value))
                elif turn_context.activity.name == "composeExtension/submitAction":
                    return _create_invoke_response(await on_teams_messaging_extension_submit_action_dispatch_async(turn_context, turn_context.activity.value))
                elif turn_context.activity.name == "composeExtension/fetchTask":
                    return _create_invoke_response(await on_teams_messaging_extension_fetch_task_async(turn_context, turn_context.activity.value))
                elif turn_context.activity.name == "composeExtension/querySettingUrl":
                    return _create_invoke_response(await on_teams_messaging_extension_configuration_query_settings_url_async(turn_context, turn_context.activity.value))
                elif turn_context.acitivity.name == "composseExtension/settings":
                    await on_teams_messaging_extension_configuration_settings_async(turn_context, turn_context.activity.value)
                    return _create_invoke_response()
                elif turn_context.acitivity.name == "composeExtension/onCardButtonClicked":
                    await on_teams_messaging_extension_card_button_clicked_async(turn_context, turn_context.acitivity.value)
                    return _create_invoke_response()
                elif turn_context.acitivity.name == "task/fetch":
                    return _create_invoke_response(await on_teams_task_module_fetch_async(turn_context, turn_context.activity.value))
                elif turn_context.acitivity.name == "task/submit":
                    return _create_invoke_response(await on_teams_task_module_submit_async(turn_context, turn_context.activity.value))
                else:
                    raise invoke_response_exception(HTTPStatus.NOT_IMPLEMENTED)
        except InvokeResponseException as e:
            return e.CreateInvokeResponse()

    async def on_teams_card_action_invoke_async(self, turn_context: TurnContext):
        raise _InvokeResponseException(HTTPStatus.NOT_IMPLEMENTED)

    async def on_teams_singin_verify_state_async(self, turn_context: TurnContext):
        raise _InvokeResponseException(HTTPStatus.NOT_IMPLEMENTED)

    async def on_teams_file_concent_async(self, turn_context: TurnContext, file_consent_card_response: FileConcentCardResponse):
        if file_consent_card_response.action == "accept":
            await file_consent_card_response(turn_context, file_consent_card_response)
            return _create_invoke_response()
        elif file_consent_card_response.action == "decline":
            await on_teams_file_consent_decline_async(turn_context, file_consent_card_response)
            return _create_invoke_response()
        else:
            raise _InvokeResponseException(HTTPStatus.BAD_REQUEST, ("%s is not a supported action" % file_consent_card_response))

    async def on_teams_file_consent_accept_async(self, turn_context: TurnContext, file_consent_card_response: FileConsentCardResponse):
        raise _InvokeResponseException(HTTPStatus.NOT_IMPLMENENTED)

    async def on_teams_file_consent_decline_async(self, turn_context: TurnContext, file_consent_card_response: FileConsentCardResponse):
        raise _InvokeResponseException(HTTPStatus.NOT_IMPLMENENTED)

    async def on_teams_messaging_extension_query_async(self, turn_context: TurnContext, query: MessagingExtensionQuery):
        raise _InvokeResponseException(HTTPStatus.NOT_IMPLMENENTED)

    async def on_teams_o365_connector_card_action_async(self, turn_context: TurnContext, query: O365ConnectorCardActionQuery):
        raise _InvokeResponseException(HTTPStatus.NOT_IMPLEMENTED)

    async def on_teams_app_based_link_query_async(self, turn_context: TurnContext, query: AppBasedLinkQuery):
        raise _InvokeResponseException(HTTPStatus.NOT_IMPLEMENTED)

    async def on_teams_messaging_extension_select_item_async(self, turn_context: TurnContext, query: JObject):
        raise _InvokeResponseException(HTTPStatus.NOT_IMPLEMENTED)

    async def on_teams_messaging_extension_fetch_task_async(self, turn_context: TurnContext, action: MessagingExtensionAction):
        raise _InvokeResponseException(HTTPStatus.NOT_IMPLEMENTED)

    async def on_teams_messaging_extension_submit_action_dispatch_async(self, turn_context: TurnContext, action, MessagingExtensionAction):
        if action.BotMessagePreviewAction != None:
            if action.BotMessagePreviewAction == "edit":
                return await on_teams_messaging_extension_bot_message_preview_edit_async(turn_context, action)
            elif action.BotMessagePreview == "send":
                return await on_teams_messaging_extension_bot_message_preview_send_async(turn_context, action)
            else:
                raise _InvokeResponseException(HTTPStatus.BAD_REQUEST, 
                                               ("%s is not a supported BotMessagePreviewAction" % action.BotMessagePreviewAction))
        else:
            return await on_teams_messaging_extension_submit_action_async(turn_context, action)

    async def on_teams_messaging_extension_submit_action_async(self, turn_context: TurnContext, action: MEssagingExtensionAction):
        raise _InvokeResponseException(HTTPStatus.NOT_IMPLEMENTED)

    async def on_teams_messaging_extension_bot_message_preview_edit_async(self, turn_context: TurnContext, action: MessagingExtensionAction):
        raise _InvokeResponseException(HTTPStatus.NOT_IMPLEMENTED)

    async def on_teams_messaging_extension_bot_message_preview_send_async(self, turn_context: TurnContext, action: MessagingExtensionAction):
        raise _InvokeResponseException(HTTPStatus.NOT_IMPLEMENTED)

    async def on_teams_messaging_extension_configuration_query_setting_url_async(self, turn_context: TurnContext, query: MessagingExtensionQuery):
        raise _InvokeResponseException(HTTPStatus.NOT_IMPLEMENTED)

    async def on_teams_messaging_extension_configuration_setting_async(self, turn_context: TurnContext, settings: JObject):
        raise _InvokeResponseException(HTTPStatus.NOT_IMPLEMENTED)

    async def on_teams_messaging_extension_card_button_clicked_async(self, turn_context: TurnContext, cardData: JObject):
        raise _InvokeResponseException(HTTPStatus.NOT_IMPLEMENTED)

    async def on_teams_task_module_fetch_async(self, turn_context: TurnContext, taskModuleRequest: TaskModuleRequest):
        raise _InvokeResponseException(HTTPStatus.NOT_IMPLEMENTED)

    async def on_teams_task_module_submit_async(self, turn_context: TurnContext, task_module_request: TaskModuleRequest):
        raise _InvokeResponseException(HTTPStatus.NOT_IMPLEMENTED)

    async def on_conversation_update_activity_async(self, turn_context: TurnContext):
        if turn_context.activity.channel_id == Channels.Msteams:
            channel_data = turn_context.activity.get_channel_data()
            if turn_context.activity.members_added != None:
                return on_teams_members_added_dispatch_async(turn_context.activity.members_added, channel_data.team)

            if turn_context.activity.members_added != None:
                return on_teams_members_removed_dispatched_async(turn_context.acitivity.members_removed, channel_data.team)

            if channel_data != None:
                if channel_data.event_type == "channelCreated":
                    return on_teams_channel_created_async(channel_data.channel, channel_data.team, turn_context)
                elif channel_data.event_type == "channelDeleted":
                    return on_teams_channel_deleted_async(channel_data.channel, channel_data.team, turn_context)
                elif channel_data.event_type == "channelRenamed":
                    return on_teams_channel_renamed(channel_data.channel, channel_data.team, turn_context)
                elif channel_data.event_type == "teamRenamed":
                    return self.on_teams_team_renamed_async(channel_data.team, turn_context)
                else:
                    return super().on_conversation_update_activity(turn_context)
        
        return super().on_conversation_update_activity(turn_context)
    
    async def on_teams_member_added_dispatch(self, members_added: List, team_info: TeamInfo, turn_context: TurnContext):
        team_members = {}
        team_members_added = []
        for member_added in members_added:
            if member_added.properties != None:
                team_members_added.append(TeamsChannelAccount(member_added))
            else:
                if team_members == {}:
                    result = await TeamInfo.get_members_async(turn_context)
                    team_members = { i.id : i for i in result }
                
                if member_added.id in team_members:
                    team_members_added.append(member_added)
                else:
                    newTeamsChannelAccount = TeamsChannelAccount(
                        id=member_added.id, 
                        name = member_added.name, 
                        aad_object_id = member_added.aad_object_id,
                        role = member_added.role
                        )
                    team_members_added.append(newTeamsChannelAccount)
        
        await self.on_teams_members_added_async(teams_members_added, team_info, turn_context)

    async def on_teams_members_removed_dispatch_async(self, membersRemoved: List, teamInfo: TeamInfo, turn_context: TurnContext):
        teams_members_removed = []
        for member_removed in membersRemoved:
            teams_members_removed.append(TeamsChannelAccount(member_removed))

        return self.on_teams_members_removed_async(teams_members_removed, team_info, turn_context)

    async def on_teams_members_added_async(self, teams_members_added: List, team_info: TeamInfo, turn_context: TurnContext):
        members_added = [ ChannelAccount(i) for i in teams_members_added ]
        return super().on_members_added_activity(members_added, turn_context)

    async def on_teams_members_removed_async(self, teams_members_removed: List, team_info: TeamInfo, turn_context: TurnContext):
        members_removed = [ ChannelAccount(i) for i in teams_members_removed ]
        return super().on_members_removed_activity(members_removed, turn_context)

    async def on_teams_channel_created_async(self, channel_info: ChannelInfo, team_info: TeamInfo, turn_context, TurnContext):
        return #Task.CompleteTask

    async def on_teams_channel_deleted_async(self, channel_info: ChannelInfo, team_info: TeamInfo, turn_context: TurnContext):
        return #Task.CompleteTask

    async def on_teams_channel_renamed_async(self, channel_info: ChannelInfo, team_info: TeamInfo, turn_context: TurnContext):
        return #Task.CompleteTask

    async def on_teams_team_reanamed_async(self, teamInfo: TeamInfo, turn_context: TurnContext):
        return #Task.CompleteTask

    @staticmethod
    def _create_invoke_response(body: object = None) -> InvokeResponse:
        return InvokeResponse(status = int(HTTPStatus.OK), body = body)
    
    class _InvokeResponseException(Exception):
        def __init__(self, status_code: HTTPStatus, body: object = None):
            self._statusCode = status_code
            self._body = body

        def create_invoke_response() -> InvokeResponse:
            return InvokeResponse(status= int(self._statusCode), body = self._body)