# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
"""Middleware Component for logging Activity messages."""
from typing import Awaitable, Callable, List, Dict
from jsonpickle import encode

from botbuilder.schema import Activity, ConversationReference, ActivityTypes
from botbuilder.schema.teams import TeamsChannelData, TeamInfo
from botframework.connector import Channels

from .bot_telemetry_client import BotTelemetryClient
from .bot_assert import BotAssert
from .middleware_set import Middleware
from .null_telemetry_client import NullTelemetryClient
from .turn_context import TurnContext
from .telemetry_constants import TelemetryConstants
from .telemetry_logger_constants import TelemetryLoggerConstants


# pylint: disable=line-too-long
class TelemetryLoggerMiddleware(Middleware):
    """Middleware for logging incoming, outgoing, updated or deleted Activity messages."""

    def __init__(
        self, telemetry_client: BotTelemetryClient, log_personal_information: bool
    ) -> None:
        super(TelemetryLoggerMiddleware, self).__init__()
        self._telemetry_client = telemetry_client or NullTelemetryClient()
        self._log_personal_information = log_personal_information

    @property
    def telemetry_client(self) -> BotTelemetryClient:
        """Gets the currently configured BotTelemetryClient."""
        return self._telemetry_client

    @property
    def log_personal_information(self) -> bool:
        """Gets a value indicating whether determines whether to log personal
        information that came from the user."""
        return self._log_personal_information

    # pylint: disable=arguments-differ
    async def on_turn(
        self, context: TurnContext, logic_fn: Callable[[TurnContext], Awaitable]
    ) -> None:
        """Logs events based on incoming and outgoing activities using
        BotTelemetryClient base class

        :param turn_context: The context object for this turn.
        :param logic: Callable to continue the bot middleware pipeline

        :return:  None
        """
        BotAssert.context_not_none(context)

        # Log incoming activity at beginning of turn
        if context.activity:
            activity = context.activity
            # Log Bot Message Received
            await self.on_receive_activity(activity)

        # hook up onSend pipeline
        # pylint: disable=unused-argument
        async def send_activities_handler(
            ctx: TurnContext,
            activities: List[Activity],
            next_send: Callable[[], Awaitable[None]],
        ):
            # Run full pipeline
            responses = await next_send()
            for activity in activities:
                await self.on_send_activity(activity)
            return responses

        context.on_send_activities(send_activities_handler)

        # hook up update activity pipeline
        async def update_activity_handler(
            ctx: TurnContext, activity: Activity, next_update: Callable[[], Awaitable]
        ):
            # Run full pipeline
            response = await next_update()
            await self.on_update_activity(activity)
            return response

        context.on_update_activity(update_activity_handler)

        # hook up delete activity pipeline
        async def delete_activity_handler(
            ctx: TurnContext,
            reference: ConversationReference,
            next_delete: Callable[[], Awaitable],
        ):
            # Run full pipeline
            await next_delete()

            delete_msg = Activity(
                type=ActivityTypes.message_delete, id=reference.activity_id
            )
            deleted_activity: Activity = TurnContext.apply_conversation_reference(
                delete_msg, reference, False
            )
            await self.on_delete_activity(deleted_activity)

        context.on_delete_activity(delete_activity_handler)

        if logic_fn:
            await logic_fn()

    async def on_receive_activity(self, activity: Activity) -> None:
        """Invoked when a message is received from the user.
        Performs logging of telemetry data using the BotTelemetryClient.track_event() method.
        This event name used is "BotMessageReceived".
        :param activity: Current activity sent from user.
        """
        self.telemetry_client.track_event(
            TelemetryLoggerConstants.BOT_MSG_RECEIVE_EVENT,
            await self.fill_receive_event_properties(activity),
        )

    async def on_send_activity(self, activity: Activity) -> None:
        """Invoked when the bot sends a message to the user.
        Performs logging of telemetry data using the BotTelemetryClient.track_event() method.
        This event name used is "BotMessageSend".
        :param activity: Current activity sent from bot.
        """
        self.telemetry_client.track_event(
            TelemetryLoggerConstants.BOT_MSG_SEND_EVENT,
            await self.fill_send_event_properties(activity),
        )

    async def on_update_activity(self, activity: Activity) -> None:
        """Invoked when the bot updates a message.
        Performs logging of telemetry data using the BotTelemetryClient.track_event() method.
        This event name used is "BotMessageUpdate".
        :param activity: Current activity sent from user.
        """
        self.telemetry_client.track_event(
            TelemetryLoggerConstants.BOT_MSG_UPDATE_EVENT,
            await self.fill_update_event_properties(activity),
        )

    async def on_delete_activity(self, activity: Activity) -> None:
        """Invoked when the bot deletes a message.
        Performs logging of telemetry data using the BotTelemetryClient.track_event() method.
        This event name used is "BotMessageDelete".
        :param activity: Current activity sent from user.
        """
        self.telemetry_client.track_event(
            TelemetryLoggerConstants.BOT_MSG_DELETE_EVENT,
            await self.fill_delete_event_properties(activity),
        )

    async def fill_receive_event_properties(
        self, activity: Activity, additional_properties: Dict[str, str] = None
    ) -> Dict[str, str]:
        """Fills the event properties for the BotMessageReceived.
        Adheres to the LogPersonalInformation flag to filter Name, Text and Speak properties.
        :param activity: activity sent from user.
        :param additional_properties: Additional properties to add to the event.
        Additional properties can override "stock" properties.

        :return: A dictionary that is sent as "Properties" to
        BotTelemetryClient.track_event method for the BotMessageReceived event.
        """
        properties = {
            TelemetryConstants.FROM_ID_PROPERTY: activity.from_property.id
            if activity.from_property
            else None,
            TelemetryConstants.CONVERSATION_NAME_PROPERTY: activity.conversation.name,
            TelemetryConstants.LOCALE_PROPERTY: activity.locale,
            TelemetryConstants.RECIPIENT_ID_PROPERTY: activity.recipient.id,
            TelemetryConstants.RECIPIENT_NAME_PROPERTY: activity.recipient.name,
        }

        if self.log_personal_information:
            if (
                activity.from_property
                and activity.from_property.name
                and activity.from_property.name.strip()
            ):
                properties[
                    TelemetryConstants.FROM_NAME_PROPERTY
                ] = activity.from_property.name
            if activity.text and activity.text.strip():
                properties[TelemetryConstants.TEXT_PROPERTY] = activity.text
            if activity.speak and activity.speak.strip():
                properties[TelemetryConstants.SPEAK_PROPERTY] = activity.speak

        TelemetryLoggerMiddleware.__populate_additional_channel_properties(
            activity, properties
        )

        # Additional properties can override "stock" properties
        if additional_properties:
            for prop in additional_properties:
                properties[prop.key] = prop.value

        return properties

    async def fill_send_event_properties(
        self, activity: Activity, additional_properties: Dict[str, str] = None
    ) -> Dict[str, str]:
        """Fills the event properties for the BotMessageSend.
        These properties are logged when an activity message is sent by the Bot to the user.
        :param activity: activity sent from user.
        :param additional_properties: Additional properties to add to the event.
        Additional properties can override "stock" properties.

        :return: A dictionary that is sent as "Properties" to the
        BotTelemetryClient.track_event method for the BotMessageSend event.
        """
        properties = {
            TelemetryConstants.REPLY_ACTIVITY_ID_PROPERTY: activity.reply_to_id,
            TelemetryConstants.RECIPIENT_ID_PROPERTY: activity.recipient.id,
            TelemetryConstants.CONVERSATION_NAME_PROPERTY: activity.conversation.name,
            TelemetryConstants.LOCALE_PROPERTY: activity.locale,
        }

        # Use the LogPersonalInformation flag to toggle logging PII data, text and user name are common examples
        if self.log_personal_information:
            if activity.attachments and len(activity.attachments) > 0:
                properties[TelemetryConstants.ATTACHMENTS_PROPERTY] = encode(
                    activity.attachments
                )
            if activity.from_property.name and activity.from_property.name.strip():
                properties[
                    TelemetryConstants.FROM_NAME_PROPERTY
                ] = activity.from_property.name
            if activity.text and activity.text.strip():
                properties[TelemetryConstants.TEXT_PROPERTY] = activity.text
            if activity.speak and activity.speak.strip():
                properties[TelemetryConstants.SPEAK_PROPERTY] = activity.speak

        # Additional properties can override "stock" properties
        if additional_properties:
            for prop in additional_properties:
                properties[prop.key] = prop.value

        return properties

    async def fill_update_event_properties(
        self, activity: Activity, additional_properties: Dict[str, str] = None
    ) -> Dict[str, str]:
        """Fills the event properties for the BotMessageUpdate.
        These properties are logged when an activity message is updated by the Bot.
        For example, if a card is interacted with by the use, and the card needs
        to be updated to reflect some interaction.
        :param activity: activity sent from user.
        :param additional_properties: Additional properties to add to the event.
        Additional properties can override "stock" properties.

        :return: A dictionary that is sent as "Properties" to the
        BotTelemetryClient.track_event method for the BotMessageUpdate event.
        """
        properties = {
            TelemetryConstants.RECIPIENT_ID_PROPERTY: activity.recipient.id,
            TelemetryConstants.CONVERSATION_ID_PROPERTY: activity.conversation.id,
            TelemetryConstants.CONVERSATION_NAME_PROPERTY: activity.conversation.name,
            TelemetryConstants.LOCALE_PROPERTY: activity.locale,
        }

        # Use the LogPersonalInformation flag to toggle logging PII data, text is a common examples
        if self.log_personal_information:
            if activity.text and activity.text.strip():
                properties[TelemetryConstants.TEXT_PROPERTY] = activity.text

        # Additional properties can override "stock" properties
        if additional_properties:
            for prop in additional_properties:
                properties[prop.key] = prop.value

        return properties

    async def fill_delete_event_properties(
        self, activity: Activity, additional_properties: Dict[str, str] = None
    ) -> Dict[str, str]:
        """Fills the event properties for the BotMessageDelete.
        These properties are logged when an activity message is deleted by the Bot.
        :param activity: activity sent from user.
        :param additional_properties: Additional properties to add to the event.
        Additional properties can override "stock" properties.

        :return: A dictionary that is sent as "Properties" to the
        BotTelemetryClient.track_event method for the BotMessageUpdate event.
        """
        properties = {
            TelemetryConstants.RECIPIENT_ID_PROPERTY: activity.recipient.id,
            TelemetryConstants.CONVERSATION_ID_PROPERTY: activity.conversation.id,
            TelemetryConstants.CONVERSATION_NAME_PROPERTY: activity.conversation.name,
        }

        # Additional properties can override "stock" properties
        if additional_properties:
            for prop in additional_properties:
                properties[prop.key] = prop.value

        return properties

    @staticmethod
    def __populate_additional_channel_properties(
        activity: Activity,
        properties: dict,
    ):
        if activity.channel_id == Channels.ms_teams:
            teams_channel_data: TeamsChannelData = TeamsChannelData().deserialize(
                activity.channel_data
            )

            properties["TeamsTenantId"] = (
                teams_channel_data.tenant.id
                if teams_channel_data and teams_channel_data.tenant
                else ""
            )

            properties["TeamsUserAadObjectId"] = (
                activity.from_property.aad_object_id if activity.from_property else ""
            )

            if teams_channel_data and teams_channel_data.team:
                properties["TeamsTeamInfo"] = TeamInfo.serialize(
                    teams_channel_data.team
                )
