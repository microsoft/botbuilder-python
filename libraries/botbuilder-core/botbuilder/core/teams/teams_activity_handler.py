# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

# pylint: disable=too-many-lines

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
    MeetingStartEventDetails,
    MeetingEndEventDetails,
    TeamsChannelData,
    TeamsChannelAccount,
    MessagingExtensionAction,
    MessagingExtensionQuery,
    MessagingExtensionActionResponse,
    MessagingExtensionResponse,
    O365ConnectorCardActionQuery,
    TaskModuleRequest,
    TaskModuleResponse,
    TabRequest,
    TabSubmit,
)
from botframework.connector import Channels
from ..serializer_helper import deserializer_helper


class TeamsActivityHandler(ActivityHandler):
    async def on_invoke_activity(self, turn_context: TurnContext) -> InvokeResponse:
        """
        Invoked when an invoke activity is received from the connector.
        Invoke activities can be used to communicate many different things.

        :param turn_context: A context object for this turn.

        :returns: An InvokeResponse that represents the work queued to execute.

        .. remarks::
            Invoke activities communicate programmatic commands from a client or channel to a bot.
            The meaning of an invoke activity is defined by the "invoke_activity.name" property,
            which is meaningful within the scope of a channel.
        """
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
                            MessagingExtensionAction,
                            turn_context.activity.value,
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

            if turn_context.activity.name == "tab/fetch":
                return self._create_invoke_response(
                    await self.on_teams_tab_fetch(
                        turn_context,
                        deserializer_helper(TabRequest, turn_context.activity.value),
                    )
                )

            if turn_context.activity.name == "tab/submit":
                return self._create_invoke_response(
                    await self.on_teams_tab_submit(
                        turn_context,
                        deserializer_helper(TabSubmit, turn_context.activity.value),
                    )
                )

            return await super().on_invoke_activity(turn_context)

        except _InvokeResponseException as invoke_exception:
            return invoke_exception.create_invoke_response()

    async def on_sign_in_invoke(self, turn_context: TurnContext):
        """
        Invoked when a signIn invoke activity is received from the connector.

        :param turn_context: A context object for this turn.

        :returns: A task that represents the work queued to execute.
        """
        return await self.on_teams_signin_verify_state(turn_context)

    async def on_teams_card_action_invoke(
        self, turn_context: TurnContext
    ) -> InvokeResponse:
        """
        Invoked when an card action invoke activity is received from the connector.

        :param turn_context: A context object for this turn.

        :returns: An InvokeResponse that represents the work queued to execute.
        """
        raise _InvokeResponseException(status_code=HTTPStatus.NOT_IMPLEMENTED)

    async def on_teams_signin_verify_state(self, turn_context: TurnContext):
        """
        Invoked when a signIn verify state activity is received from the connector.

        :param turn_context: A context object for this turn.

        :returns: A task that represents the work queued to execute.
        """
        raise _InvokeResponseException(status_code=HTTPStatus.NOT_IMPLEMENTED)

    async def on_teams_signin_token_exchange(self, turn_context: TurnContext):
        raise _InvokeResponseException(status_code=HTTPStatus.NOT_IMPLEMENTED)

    async def on_teams_file_consent(
        self,
        turn_context: TurnContext,
        file_consent_card_response: FileConsentCardResponse,
    ) -> InvokeResponse:
        """
        Invoked when a file consent card activity is received from the connector.

        :param turn_context: A context object for this turn.
        :param file_consent_card_response: The response representing the value of the invoke
        activity sent when the user acts on a file consent card.

        :returns: An InvokeResponse depending on the action of the file consent card.
        """
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
        """
        Invoked when a file consent card is accepted by the user.

        :param turn_context: A context object for this turn.
        :param file_consent_card_response: The response representing the value of the invoke
        activity sent when the user accepts a file consent card.

        :returns: A task that represents the work queued to execute.
        """
        raise _InvokeResponseException(status_code=HTTPStatus.NOT_IMPLEMENTED)

    async def on_teams_file_consent_decline(  # pylint: disable=unused-argument
        self,
        turn_context: TurnContext,
        file_consent_card_response: FileConsentCardResponse,
    ):
        """
        Invoked when a file consent card is declined by the user.

        :param turn_context: A context object for this turn.
        :param file_consent_card_response: The response representing the value of the invoke
        activity sent when the user declines a file consent card.

        :returns: A task that represents the work queued to execute.
        """
        raise _InvokeResponseException(status_code=HTTPStatus.NOT_IMPLEMENTED)

    async def on_teams_o365_connector_card_action(  # pylint: disable=unused-argument
        self, turn_context: TurnContext, query: O365ConnectorCardActionQuery
    ):
        """
        Invoked when a O365 Connector Card Action activity is received from the connector.

        :param turn_context: A context object for this turn.
        :param query: The O365 connector card HttpPOST invoke query.

        :returns: A task that represents the work queued to execute.
        """
        raise _InvokeResponseException(status_code=HTTPStatus.NOT_IMPLEMENTED)

    async def on_teams_app_based_link_query(  # pylint: disable=unused-argument
        self, turn_context: TurnContext, query: AppBasedLinkQuery
    ) -> MessagingExtensionResponse:
        """
        Invoked when an app based link query activity is received from the connector.

        :param turn_context: A context object for this turn.
        :param query: The invoke request body type for app-based link query.

        :returns: The Messaging Extension Response for the query.
        """
        raise _InvokeResponseException(status_code=HTTPStatus.NOT_IMPLEMENTED)

    async def on_teams_messaging_extension_query(  # pylint: disable=unused-argument
        self, turn_context: TurnContext, query: MessagingExtensionQuery
    ) -> MessagingExtensionResponse:
        """
        Invoked when a Messaging Extension Query activity is received from the connector.

        :param turn_context: A context object for this turn.
        :param query: The query for the search command.

        :returns: The Messaging Extension Response for the query.
        """
        raise _InvokeResponseException(status_code=HTTPStatus.NOT_IMPLEMENTED)

    async def on_teams_messaging_extension_select_item(  # pylint: disable=unused-argument
        self, turn_context: TurnContext, query
    ) -> MessagingExtensionResponse:
        """
        Invoked when a messaging extension select item activity is received from the connector.

        :param turn_context: A context object for this turn.
        :param query: The object representing the query.

        :returns: The Messaging Extension Response for the query.
        """
        raise _InvokeResponseException(status_code=HTTPStatus.NOT_IMPLEMENTED)

    async def on_teams_messaging_extension_submit_action_dispatch(
        self, turn_context: TurnContext, action: MessagingExtensionAction
    ) -> MessagingExtensionActionResponse:
        """
        Invoked when a messaging extension submit action dispatch activity is received from the connector.

        :param turn_context: A context object for this turn.
        :param action: The messaging extension action.

        :returns: The Messaging Extension Action Response for the action.
        """
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
        """
        Invoked when a messaging extension bot message preview edit activity is received from the connector.

        :param turn_context: A context object for this turn.
        :param action: The messaging extension action.

        :returns: The Messaging Extension Action Response for the action.
        """
        raise _InvokeResponseException(status_code=HTTPStatus.NOT_IMPLEMENTED)

    async def on_teams_messaging_extension_bot_message_preview_send(  # pylint: disable=unused-argument
        self, turn_context: TurnContext, action: MessagingExtensionAction
    ) -> MessagingExtensionActionResponse:
        """
        Invoked when a messaging extension bot message preview send activity is received from the connector.

        :param turn_context: A context object for this turn.
        :param action: The messaging extension action.

        :returns: The Messaging Extension Action Response for the action.
        """
        raise _InvokeResponseException(status_code=HTTPStatus.NOT_IMPLEMENTED)

    async def on_teams_messaging_extension_submit_action(  # pylint: disable=unused-argument
        self, turn_context: TurnContext, action: MessagingExtensionAction
    ) -> MessagingExtensionActionResponse:
        """
        Invoked when a messaging extension submit action activity is received from the connector.

        :param turn_context: A context object for this turn.
        :param action: The messaging extension action.

        :returns: The Messaging Extension Action Response for the action.
        """
        raise _InvokeResponseException(status_code=HTTPStatus.NOT_IMPLEMENTED)

    async def on_teams_messaging_extension_fetch_task(  # pylint: disable=unused-argument
        self, turn_context: TurnContext, action: MessagingExtensionAction
    ) -> MessagingExtensionActionResponse:
        """
        Invoked when a Messaging Extension Fetch activity is received from the connector.

        :param turn_context: A context object for this turn.
        :param action: The messaging extension action.

        :returns: The Messaging Extension Action Response for the action.
        """
        raise _InvokeResponseException(status_code=HTTPStatus.NOT_IMPLEMENTED)

    async def on_teams_messaging_extension_configuration_query_settings_url(  # pylint: disable=unused-argument
        self, turn_context: TurnContext, query: MessagingExtensionQuery
    ) -> MessagingExtensionResponse:
        """
        Invoked when a messaging extension configuration query setting url activity is received from the connector.

        :param turn_context: A context object for this turn.
        :param query: The Messaging extension query.

        :returns: The Messaging Extension Response for the query.
        """
        raise _InvokeResponseException(status_code=HTTPStatus.NOT_IMPLEMENTED)

    async def on_teams_messaging_extension_configuration_setting(  # pylint: disable=unused-argument
        self, turn_context: TurnContext, settings
    ):
        """
        Override this in a derived class to provide logic for when a configuration is set for a messaging extension.

        :param turn_context: A context object for this turn.
        :param settings: Object representing the configuration settings.

        :returns: A task that represents the work queued to execute.
        """
        raise _InvokeResponseException(status_code=HTTPStatus.NOT_IMPLEMENTED)

    async def on_teams_messaging_extension_card_button_clicked(  # pylint: disable=unused-argument
        self, turn_context: TurnContext, card_data
    ):
        """
        Override this in a derived class to provide logic for when a card button is clicked in a messaging extension.

        :param turn_context: A context object for this turn.
        :param card_data: Object representing the card data.

        :returns: A task that represents the work queued to execute.
        """
        raise _InvokeResponseException(status_code=HTTPStatus.NOT_IMPLEMENTED)

    async def on_teams_task_module_fetch(  # pylint: disable=unused-argument
        self, turn_context: TurnContext, task_module_request: TaskModuleRequest
    ) -> TaskModuleResponse:
        """
        Override this in a derived class to provide logic for when a task module is fetched.

        :param turn_context: A context object for this turn.
        :param task_module_request: The task module invoke request value payload.

        :returns: A Task Module Response for the request.
        """
        raise _InvokeResponseException(status_code=HTTPStatus.NOT_IMPLEMENTED)

    async def on_teams_task_module_submit(  # pylint: disable=unused-argument
        self, turn_context: TurnContext, task_module_request: TaskModuleRequest
    ) -> TaskModuleResponse:
        """
        Override this in a derived class to provide logic for when a task module is submitted.

        :param turn_context: A context object for this turn.
        :param task_module_request: The task module invoke request value payload.

        :returns: A Task Module Response for the request.
        """
        raise _InvokeResponseException(status_code=HTTPStatus.NOT_IMPLEMENTED)

    async def on_teams_tab_fetch(  # pylint: disable=unused-argument
        self, turn_context: TurnContext, tab_request: TabRequest
    ):
        """
        Override this in a derived class to provide logic for when a tab is fetched.

        :param turn_context: A context object for this turn.
        :param tab_request: The tab invoke request value payload.

        :returns: A Tab Response for the request.
        """
        raise _InvokeResponseException(status_code=HTTPStatus.NOT_IMPLEMENTED)

    async def on_teams_tab_submit(  # pylint: disable=unused-argument
        self, turn_context: TurnContext, tab_submit: TabSubmit
    ):
        """
        Override this in a derived class to provide logic for when a tab is submitted.

        :param turn_context: A context object for this turn.
        :param tab_submit: The tab submit invoke request value payload.

        :returns: A Tab Response for the request.
        """
        raise _InvokeResponseException(status_code=HTTPStatus.NOT_IMPLEMENTED)

    async def on_conversation_update_activity(self, turn_context: TurnContext):
        """
        Invoked when a conversation update activity is received from the channel.
        Conversation update activities are useful when it comes to responding to users
        being added to or removed from the channel.
        For example, a bot could respond to a user being added by greeting the user.

        :param turn_context: A context object for this turn.

        :returns: A task that represents the work queued to execute.

        .. remarks::
            In a derived class, override this method to add logic that applies
            to all conversation update activities.
        """
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
                if channel_data.event_type == "teamArchived":
                    return await self.on_teams_team_archived(
                        channel_data.team, turn_context
                    )
                if channel_data.event_type == "teamDeleted":
                    return await self.on_teams_team_deleted(
                        channel_data.team, turn_context
                    )
                if channel_data.event_type == "teamHardDeleted":
                    return await self.on_teams_team_hard_deleted(
                        channel_data.team, turn_context
                    )
                if channel_data.event_type == "channelRestored":
                    return await self.on_teams_channel_restored(
                        channel_data.channel, channel_data.team, turn_context
                    )
                if channel_data.event_type == "teamRenamed":
                    return await self.on_teams_team_renamed(
                        channel_data.team, turn_context
                    )
                if channel_data.event_type == "teamRestored":
                    return await self.on_teams_team_restored(
                        channel_data.team, turn_context
                    )
                if channel_data.event_type == "teamUnarchived":
                    return await self.on_teams_team_unarchived(
                        channel_data.team, turn_context
                    )

        return await super().on_conversation_update_activity(turn_context)

    async def on_teams_channel_created(  # pylint: disable=unused-argument
        self, channel_info: ChannelInfo, team_info: TeamInfo, turn_context: TurnContext
    ):
        """
        Invoked when a Channel Created event activity is received from the connector.
        Channel Created correspond to the user creating a new channel.

        :param channel_info: The channel info object which describes the channel.
        :param team_info: The team info object representing the team.
        :param turn_context: A context object for this turn.

        :returns: A task that represents the work queued to execute.
        """
        return

    async def on_teams_team_archived(  # pylint: disable=unused-argument
        self, team_info: TeamInfo, turn_context: TurnContext
    ):
        """
        Invoked when a Team Archived event activity is received from the connector.
        Team Archived correspond to the user archiving a team.

        :param team_info: The team info object representing the team.
        :param turn_context: A context object for this turn.

        :returns: A task that represents the work queued to execute.
        """
        return

    async def on_teams_team_deleted(  # pylint: disable=unused-argument
        self, team_info: TeamInfo, turn_context: TurnContext
    ):
        """
        Invoked when a Team Deleted event activity is received from the connector.
        Team Deleted corresponds to the user deleting a team.

        :param team_info: The team info object representing the team.
        :param turn_context: A context object for this turn.

        :returns: A task that represents the work queued to execute.
        """
        return

    async def on_teams_team_hard_deleted(  # pylint: disable=unused-argument
        self, team_info: TeamInfo, turn_context: TurnContext
    ):
        """
        Invoked when a Team Hard Deleted event activity is received from the connector.
        Team Hard Deleted corresponds to the user hard deleting a team.

        :param team_info: The team info object representing the team.
        :param turn_context: A context object for this turn.

        :returns: A task that represents the work queued to execute.
        """
        return

    async def on_teams_team_renamed(  # pylint: disable=unused-argument
        self, team_info: TeamInfo, turn_context: TurnContext
    ):
        """
        Invoked when a Team Renamed event activity is received from the connector.
        Team Renamed correspond to the user renaming an existing team.

        :param team_info: The team info object representing the team.
        :param turn_context: A context object for this turn.

        :returns: A task that represents the work queued to execute.
        """
        return await self.on_teams_team_renamed_activity(team_info, turn_context)

    async def on_teams_team_renamed_activity(  # pylint: disable=unused-argument
        self, team_info: TeamInfo, turn_context: TurnContext
    ):
        """
        DEPRECATED. Please use on_teams_team_renamed(). This method will remain in place throughout
        v4 so as not to break existing bots.

        Invoked when a Team Renamed event activity is received from the connector.
        Team Renamed correspond to the user renaming an existing team.

        :param team_info: The team info object representing the team.
        :param turn_context: A context object for this turn.

        :returns: A task that represents the work queued to execute.
        """
        return

    async def on_teams_team_restored(  # pylint: disable=unused-argument
        self, team_info: TeamInfo, turn_context: TurnContext
    ):
        """
        Invoked when a Team Restored event activity is received from the connector.
        Team Restored corresponds to the user restoring a team.

        :param team_info: The team info object representing the team.
        :param turn_context: A context object for this turn.

        :returns: A task that represents the work queued to execute.
        """
        return

    async def on_teams_team_unarchived(  # pylint: disable=unused-argument
        self, team_info: TeamInfo, turn_context: TurnContext
    ):
        """
        Invoked when a Team Unarchived event activity is received from the connector.
        Team Unarchived correspond to the user unarchiving a team.

        :param team_info: The team info object representing the team.
        :param turn_context: A context object for this turn.

        :returns: A task that represents the work queued to execute.
        """
        return

    async def on_teams_members_added_dispatch(  # pylint: disable=unused-argument
        self,
        members_added: [ChannelAccount],
        team_info: TeamInfo,
        turn_context: TurnContext,
    ):
        """
        Override this in a derived class to provide logic for when members other than the bot
        join the channel, such as your bot's welcome logic.
        It will get the associated members with the provided accounts.

        :param members_added: A list of all the accounts added to the channel, as
        described by the conversation update activity.
        :param team_info: The team info object representing the team.
        :param turn_context: A context object for this turn.

        :returns: A task that represents the work queued to execute.
        """
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
        """
        Override this in a derived class to provide logic for when members other than the bot
        join the channel, such as your bot's welcome logic.

        :param teams_members_added: A list of all the members added to the channel, as
        described by the conversation update activity.
        :param team_info: The team info object representing the team.
        :param turn_context: A context object for this turn.

        :returns: A task that represents the work queued to execute.
        """
        teams_members_added = [
            ChannelAccount().deserialize(member.serialize())
            for member in teams_members_added
        ]
        return await self.on_members_added_activity(teams_members_added, turn_context)

    async def on_teams_members_removed_dispatch(  # pylint: disable=unused-argument
        self,
        members_removed: [ChannelAccount],
        team_info: TeamInfo,
        turn_context: TurnContext,
    ):
        """
        Override this in a derived class to provide logic for when members other than the bot
        leave the channel, such as your bot's good-bye logic.
        It will get the associated members with the provided accounts.

        :param members_removed: A list of all the accounts removed from the channel, as
        described by the conversation update activity.
        :param team_info: The team info object representing the team.
        :param turn_context: A context object for this turn.

        :returns: A task that represents the work queued to execute.
        """
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
        """
        Override this in a derived class to provide logic for when members other than the bot
        leave the channel, such as your bot's good-bye logic.

        :param teams_members_removed: A list of all the members removed from the channel, as
        described by the conversation update activity.
        :param team_info: The team info object representing the team.
        :param turn_context: A context object for this turn.

        :returns: A task that represents the work queued to execute.
        """
        members_removed = [
            ChannelAccount().deserialize(member.serialize())
            for member in teams_members_removed
        ]
        return await self.on_members_removed_activity(members_removed, turn_context)

    async def on_teams_channel_deleted(  # pylint: disable=unused-argument
        self, channel_info: ChannelInfo, team_info: TeamInfo, turn_context: TurnContext
    ):
        """
        Invoked when a Channel Deleted event activity is received from the connector.
        Channel Deleted correspond to the user deleting an existing channel.

        :param channel_info: The channel info object which describes the channel.
        :param team_info: The team info object representing the team.
        :param turn_context: A context object for this turn.

        :returns: A task that represents the work queued to execute.
        """
        return

    async def on_teams_channel_renamed(  # pylint: disable=unused-argument
        self, channel_info: ChannelInfo, team_info: TeamInfo, turn_context: TurnContext
    ):
        """
        Invoked when a Channel Renamed event activity is received from the connector.
        Channel Renamed correspond to the user renaming an existing channel.

        :param channel_info: The channel info object which describes the channel.
        :param team_info: The team info object representing the team.
        :param turn_context: A context object for this turn.

        :returns: A task that represents the work queued to execute.
        """
        return

    async def on_teams_channel_restored(  # pylint: disable=unused-argument
        self, channel_info: ChannelInfo, team_info: TeamInfo, turn_context: TurnContext
    ):
        """
        Invoked when a Channel Restored event activity is received from the connector.
        Channel Restored correspond to the user restoring a previously deleted channel.

        :param channel_info: The channel info object which describes the channel.
        :param team_info: The team info object representing the team.
        :param turn_context: A context object for this turn.

        :returns: A task that represents the work queued to execute.
        """
        return

    async def on_event_activity(self, turn_context: TurnContext):
        """
        Invoked when an event activity is received from the connector when the base behavior of
        :meth:`on_turn()` is used.

        :param turn_context: The context object for this turn
        :type turn_context: :class:`botbuilder.core.TurnContext`

        :returns: A task that represents the work queued to execute

        .. remarks::
            When the :meth:`on_turn()` method receives an event activity, it calls this method.
            If the activity name is `tokens/response`, it calls :meth:`on_token_response_event()`;
            otherwise, it calls :meth:`on_event()`.

            In a derived class, override this method to add logic that applies to all event activities.
            Add logic to apply before the specific event-handling logic before the call to this base class method.
            Add logic to apply after the specific event-handling logic after the call to this base class method.

            Event activities communicate programmatic information from a client or channel to a bot.
            The meaning of an event activity is defined by the event activity name property, which is meaningful within
            the scope of a channel.
        """
        if turn_context.activity.channel_id == Channels.ms_teams:
            if turn_context.activity.name == "application/vnd.microsoft.meetingStart":
                return await self.on_teams_meeting_start_event(
                    turn_context.activity.value, turn_context
                )
            if turn_context.activity.name == "application/vnd.microsoft.meetingEnd":
                return await self.on_teams_meeting_end_event(
                    turn_context.activity.value, turn_context
                )

        return await super().on_event_activity(turn_context)

    async def on_teams_meeting_start_event(
        self, meeting: MeetingStartEventDetails, turn_context: TurnContext
    ):  # pylint: disable=unused-argument
        """
        Override this in a derived class to provide logic for when a Teams meeting start event is received.

        :param meeting: The details of the meeting.
        :param turn_context: A context object for this turn.

        :returns: A task that represents the work queued to execute.
        """
        return

    async def on_teams_meeting_end_event(
        self, meeting: MeetingEndEventDetails, turn_context: TurnContext
    ):  # pylint: disable=unused-argument
        """
        Override this in a derived class to provide logic for when a Teams meeting end event is received.

        :param meeting: The details of the meeting.
        :param turn_context: A context object for this turn.

        :returns: A task that represents the work queued to execute.
        """
        return
