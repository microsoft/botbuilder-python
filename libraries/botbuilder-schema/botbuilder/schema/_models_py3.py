# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List

from botbuilder.schema._connector_client_enums import ActivityTypes
from datetime import datetime
from enum import Enum
from msrest.serialization import Model
from msrest.exceptions import HttpOperationError


class ActivityEventNames(str, Enum):
    continue_conversation = "ContinueConversation"
    create_conversation = "CreateConversation"


class ConversationReference(Model):
    """An object relating to a particular point in a conversation.

    :param activity_id: (Optional) ID of the activity to refer to
    :type activity_id: str
    :param user: (Optional) User participating in this conversation
    :type user: ~botframework.connector.models.ChannelAccount
    :param bot: Bot participating in this conversation
    :type bot: ~botframework.connector.models.ChannelAccount
    :param conversation: Conversation reference
    :type conversation: ~botframework.connector.models.ConversationAccount
    :param channel_id: Channel ID
    :type channel_id: str
    :param locale: A locale name for the contents of the text field.
        The locale name is a combination of an ISO 639 two- or three-letter
        culture code associated with a language and an ISO 3166 two-letter
        subculture code associated with a country or region.
        The locale name can also correspond to a valid BCP-47 language tag.
    :type locale: str
    :param service_url: Service endpoint where operations concerning the
     referenced conversation may be performed
    :type service_url: str
    """

    _attribute_map = {
        "activity_id": {"key": "activityId", "type": "str"},
        "user": {"key": "user", "type": "ChannelAccount"},
        "bot": {"key": "bot", "type": "ChannelAccount"},
        "conversation": {"key": "conversation", "type": "ConversationAccount"},
        "channel_id": {"key": "channelId", "type": "str"},
        "locale": {"key": "locale", "type": "str"},
        "service_url": {"key": "serviceUrl", "type": "str"},
    }

    def __init__(
        self,
        *,
        activity_id: str = None,
        user=None,
        bot=None,
        conversation=None,
        channel_id: str = None,
        locale: str = None,
        service_url: str = None,
        **kwargs
    ) -> None:
        super(ConversationReference, self).__init__(**kwargs)
        self.activity_id = activity_id
        self.user = user
        self.bot = bot
        self.conversation = conversation
        self.channel_id = channel_id
        self.locale = locale
        self.service_url = service_url


class Mention(Model):
    """Mention information (entity type: "mention").

    :param mentioned: The mentioned user
    :type mentioned: ~botframework.connector.models.ChannelAccount
    :param text: Sub Text which represents the mention (can be null or empty)
    :type text: str
    :param type: Type of this entity (RFC 3987 IRI)
    :type type: str
    """

    _attribute_map = {
        "mentioned": {"key": "mentioned", "type": "ChannelAccount"},
        "text": {"key": "text", "type": "str"},
        "type": {"key": "type", "type": "str"},
    }

    def __init__(
        self, *, mentioned=None, text: str = None, type: str = None, **kwargs
    ) -> None:
        super(Mention, self).__init__(**kwargs)
        self.mentioned = mentioned
        self.text = text
        self.type = type


class ResourceResponse(Model):
    """A response containing a resource ID.

    :param id: Id of the resource
    :type id: str
    """

    _attribute_map = {"id": {"key": "id", "type": "str"}}

    def __init__(self, *, id: str = None, **kwargs) -> None:
        super(ResourceResponse, self).__init__(**kwargs)
        self.id = id


class Activity(Model):
    """An Activity is the basic communication type for the Bot Framework 3.0
    protocol.

    :param type: Contains the activity type. Possible values include:
     'message', 'contactRelationUpdate', 'conversationUpdate', 'typing',
     'endOfConversation', 'event', 'invoke', 'deleteUserData', 'messageUpdate',
     'messageDelete', 'installationUpdate', 'messageReaction', 'suggestion',
     'trace', 'handoff'
    :type type: str or ~botframework.connector.models.ActivityTypes
    :param id: Contains an ID that uniquely identifies the activity on the
     channel.
    :type id: str
    :param timestamp: Contains the date and time that the message was sent, in
     UTC, expressed in ISO-8601 format.
    :type timestamp: datetime
    :param local_timestamp: Contains the local date and time of the message
     expressed in ISO-8601 format.
     For example, 2016-09-23T13:07:49.4714686-07:00.
    :type local_timestamp: datetime
    :param local_timezone: Contains the name of the local timezone of the message,
     expressed in IANA Time Zone database format.
     For example, America/Los_Angeles.
    :type local_timezone: str
    :param service_url: Contains the URL that specifies the channel's service
     endpoint. Set by the channel.
    :type service_url: str
    :param channel_id: Contains an ID that uniquely identifies the channel.
     Set by the channel.
    :type channel_id: str
    :param from_property: Identifies the sender of the message.
    :type from_property: ~botframework.connector.models.ChannelAccount
    :param conversation: Identifies the conversation to which the activity
     belongs.
    :type conversation: ~botframework.connector.models.ConversationAccount
    :param recipient: Identifies the recipient of the message.
    :type recipient: ~botframework.connector.models.ChannelAccount
    :param text_format: Format of text fields Default:markdown. Possible
     values include: 'markdown', 'plain', 'xml'
    :type text_format: str or ~botframework.connector.models.TextFormatTypes
    :param attachment_layout: The layout hint for multiple attachments.
     Default: list. Possible values include: 'list', 'carousel'
    :type attachment_layout: str or
     ~botframework.connector.models.AttachmentLayoutTypes
    :param members_added: The collection of members added to the conversation.
    :type members_added: list[~botframework.connector.models.ChannelAccount]
    :param members_removed: The collection of members removed from the
     conversation.
    :type members_removed: list[~botframework.connector.models.ChannelAccount]
    :param reactions_added: The collection of reactions added to the
     conversation.
    :type reactions_added:
     list[~botframework.connector.models.MessageReaction]
    :param reactions_removed: The collection of reactions removed from the
     conversation.
    :type reactions_removed:
     list[~botframework.connector.models.MessageReaction]
    :param topic_name: The updated topic name of the conversation.
    :type topic_name: str
    :param history_disclosed: Indicates whether the prior history of the
     channel is disclosed.
    :type history_disclosed: bool
    :param locale: A locale name for the contents of the text field.
     The locale name is a combination of an ISO 639 two- or three-letter
     culture code associated with a language
     and an ISO 3166 two-letter subculture code associated with a country or
     region.
     The locale name can also correspond to a valid BCP-47 language tag.
    :type locale: str
    :param text: The text content of the message.
    :type text: str
    :param speak: The text to speak.
    :type speak: str
    :param input_hint: Indicates whether your bot is accepting,
     expecting, or ignoring user input after the message is delivered to the
     client. Possible values include: 'acceptingInput', 'ignoringInput',
     'expectingInput'
    :type input_hint: str or ~botframework.connector.models.InputHints
    :param summary: The text to display if the channel cannot render cards.
    :type summary: str
    :param suggested_actions: The suggested actions for the activity.
    :type suggested_actions: ~botframework.connector.models.SuggestedActions
    :param attachments: Attachments
    :type attachments: list[~botframework.connector.models.Attachment]
    :param entities: Represents the entities that were mentioned in the
     message.
    :type entities: list[~botframework.connector.models.Entity]
    :param channel_data: Contains channel-specific content.
    :type channel_data: object
    :param action: Indicates whether the recipient of a contactRelationUpdate
     was added or removed from the sender's contact list.
    :type action: str
    :param reply_to_id: Contains the ID of the message to which this message
     is a reply.
    :type reply_to_id: str
    :param label: A descriptive label for the activity.
    :type label: str
    :param value_type: The type of the activity's value object.
    :type value_type: str
    :param value: A value that is associated with the activity.
    :type value: object
    :param name: The name of the operation associated with an invoke or event
     activity.
    :type name: str
    :param relates_to: A reference to another conversation or activity.
    :type relates_to: ~botframework.connector.models.ConversationReference
    :param code: The a code for endOfConversation activities that indicates
     why the conversation ended. Possible values include: 'unknown',
     'completedSuccessfully', 'userCancelled', 'botTimedOut',
     'botIssuedInvalidMessage', 'channelFailed'
    :type code: str or ~botframework.connector.models.EndOfConversationCodes
    :param expiration: The time at which the activity should be considered to
     be "expired" and should not be presented to the recipient.
    :type expiration: datetime
    :param importance: The importance of the activity. Possible values
     include: 'low', 'normal', 'high'
    :type importance: str or ~botframework.connector.models.ActivityImportance
    :param delivery_mode: A delivery hint to signal to the recipient alternate
     delivery paths for the activity.
     The default delivery mode is "default". Possible values include: 'normal',
     'notification', 'expectReplies', 'ephemeral'
    :type delivery_mode: str or ~botframework.connector.models.DeliveryModes
    :param listen_for: List of phrases and references that speech and language
     priming systems should listen for
    :type listen_for: list[str]
    :param text_highlights: The collection of text fragments to highlight when
     the activity contains a ReplyToId value.
    :type text_highlights: list[~botframework.connector.models.TextHighlight]
    :param semantic_action: An optional programmatic action accompanying this
     request
    :type semantic_action: ~botframework.connector.models.SemanticAction
    :param caller_id: A string containing an IRI identifying the caller of a
     bot. This field is not intended to be transmitted over the wire, but is
     instead populated by bots and clients based on cryptographically
     verifiable data that asserts the identity of the callers (e.g. tokens).
    :type caller_id: str
    """

    _attribute_map = {
        "type": {"key": "type", "type": "str"},
        "id": {"key": "id", "type": "str"},
        "timestamp": {"key": "timestamp", "type": "iso-8601"},
        "local_timestamp": {"key": "localTimestamp", "type": "iso-8601"},
        "local_timezone": {"key": "localTimezone", "type": "str"},
        "service_url": {"key": "serviceUrl", "type": "str"},
        "channel_id": {"key": "channelId", "type": "str"},
        "from_property": {"key": "from", "type": "ChannelAccount"},
        "conversation": {"key": "conversation", "type": "ConversationAccount"},
        "recipient": {"key": "recipient", "type": "ChannelAccount"},
        "text_format": {"key": "textFormat", "type": "str"},
        "attachment_layout": {"key": "attachmentLayout", "type": "str"},
        "members_added": {"key": "membersAdded", "type": "[ChannelAccount]"},
        "members_removed": {"key": "membersRemoved", "type": "[ChannelAccount]"},
        "reactions_added": {"key": "reactionsAdded", "type": "[MessageReaction]"},
        "reactions_removed": {"key": "reactionsRemoved", "type": "[MessageReaction]"},
        "topic_name": {"key": "topicName", "type": "str"},
        "history_disclosed": {"key": "historyDisclosed", "type": "bool"},
        "locale": {"key": "locale", "type": "str"},
        "text": {"key": "text", "type": "str"},
        "speak": {"key": "speak", "type": "str"},
        "input_hint": {"key": "inputHint", "type": "str"},
        "summary": {"key": "summary", "type": "str"},
        "suggested_actions": {"key": "suggestedActions", "type": "SuggestedActions"},
        "attachments": {"key": "attachments", "type": "[Attachment]"},
        "entities": {"key": "entities", "type": "[Entity]"},
        "channel_data": {"key": "channelData", "type": "object"},
        "action": {"key": "action", "type": "str"},
        "reply_to_id": {"key": "replyToId", "type": "str"},
        "label": {"key": "label", "type": "str"},
        "value_type": {"key": "valueType", "type": "str"},
        "value": {"key": "value", "type": "object"},
        "name": {"key": "name", "type": "str"},
        "relates_to": {"key": "relatesTo", "type": "ConversationReference"},
        "code": {"key": "code", "type": "str"},
        "expiration": {"key": "expiration", "type": "iso-8601"},
        "importance": {"key": "importance", "type": "str"},
        "delivery_mode": {"key": "deliveryMode", "type": "str"},
        "listen_for": {"key": "listenFor", "type": "[str]"},
        "text_highlights": {"key": "textHighlights", "type": "[TextHighlight]"},
        "semantic_action": {"key": "semanticAction", "type": "SemanticAction"},
        "caller_id": {"key": "callerId", "type": "str"},
    }

    def __init__(
        self,
        *,
        type=None,
        id: str = None,
        timestamp=None,
        local_timestamp=None,
        local_timezone: str = None,
        service_url: str = None,
        channel_id: str = None,
        from_property=None,
        conversation=None,
        recipient=None,
        text_format=None,
        attachment_layout=None,
        members_added=None,
        members_removed=None,
        reactions_added=None,
        reactions_removed=None,
        topic_name: str = None,
        history_disclosed: bool = None,
        locale: str = None,
        text: str = None,
        speak: str = None,
        input_hint=None,
        summary: str = None,
        suggested_actions=None,
        attachments=None,
        entities=None,
        channel_data=None,
        action: str = None,
        reply_to_id: str = None,
        label: str = None,
        value_type: str = None,
        value=None,
        name: str = None,
        relates_to=None,
        code=None,
        expiration=None,
        importance=None,
        delivery_mode=None,
        listen_for=None,
        text_highlights=None,
        semantic_action=None,
        caller_id: str = None,
        **kwargs
    ) -> None:
        super(Activity, self).__init__(**kwargs)
        self.type = type
        self.id = id
        self.timestamp = timestamp
        self.local_timestamp = local_timestamp
        self.local_timezone = local_timezone
        self.service_url = service_url
        self.channel_id = channel_id
        self.from_property = from_property
        self.conversation = conversation
        self.recipient = recipient
        self.text_format = text_format
        self.attachment_layout = attachment_layout
        self.members_added = members_added
        self.members_removed = members_removed
        self.reactions_added = reactions_added
        self.reactions_removed = reactions_removed
        self.topic_name = topic_name
        self.history_disclosed = history_disclosed
        self.locale = locale
        self.text = text
        self.speak = speak
        self.input_hint = input_hint
        self.summary = summary
        self.suggested_actions = suggested_actions
        self.attachments = attachments
        self.entities = entities
        self.channel_data = channel_data
        self.action = action
        self.reply_to_id = reply_to_id
        self.label = label
        self.value_type = value_type
        self.value = value
        self.name = name
        self.relates_to = relates_to
        self.code = code
        self.expiration = expiration
        self.importance = importance
        self.delivery_mode = delivery_mode
        self.listen_for = listen_for
        self.text_highlights = text_highlights
        self.semantic_action = semantic_action
        self.caller_id = caller_id

    def apply_conversation_reference(
        self, reference: ConversationReference, is_incoming: bool = False
    ):
        """
        Updates this activity with the delivery information from an existing ConversationReference

        :param reference: The existing conversation reference.
        :param is_incoming: Optional, True to treat the activity as an
        incoming activity, where the bot is the recipient; otherwise, False.
        Default is False, and the activity will show the bot as the sender.

        :returns: his activity, updated with the delivery information.

        .. remarks::
            Call GetConversationReference on an incoming
            activity to get a conversation reference that you can then use to update an
            outgoing activity with the correct delivery information.
        """
        self.channel_id = reference.channel_id
        self.service_url = reference.service_url
        self.conversation = reference.conversation

        if reference.locale is not None:
            self.locale = reference.locale

        if is_incoming:
            self.from_property = reference.user
            self.recipient = reference.bot

            if reference.activity_id is not None:
                self.id = reference.activity_id
        else:
            self.from_property = reference.bot
            self.recipient = reference.user

            if reference.activity_id is not None:
                self.reply_to_id = reference.activity_id

        return self

    def as_contact_relation_update_activity(self):
        """
        Returns this activity as a ContactRelationUpdateActivity object;
        or None, if this is not that type of activity.

        :returns: This activity as a message activity; or None.
        """
        return (
            self if self.__is_activity(ActivityTypes.contact_relation_update) else None
        )

    def as_conversation_update_activity(self):
        """
        Returns this activity as a ConversationUpdateActivity object;
        or None, if this is not that type of activity.

        :returns: This activity as a conversation update activity; or None.
        """
        return self if self.__is_activity(ActivityTypes.conversation_update) else None

    def as_end_of_conversation_activity(self):
        """
        Returns this activity as an EndOfConversationActivity object;
        or None, if this is not that type of activity.

        :returns: This activity as an end of conversation activity; or None.
        """
        return self if self.__is_activity(ActivityTypes.end_of_conversation) else None

    def as_event_activity(self):
        """
        Returns this activity as an EventActivity object;
        or None, if this is not that type of activity.

        :returns: This activity as an event activity; or None.
        """
        return self if self.__is_activity(ActivityTypes.event) else None

    def as_handoff_activity(self):
        """
        Returns this activity as a HandoffActivity object;
        or None, if this is not that type of activity.

        :returns: This activity as a handoff activity; or None.
        """
        return self if self.__is_activity(ActivityTypes.handoff) else None

    def as_installation_update_activity(self):
        """
        Returns this activity as an InstallationUpdateActivity object;
        or None, if this is not that type of activity.

        :returns: This activity as an installation update activity; or None.
        """
        return self if self.__is_activity(ActivityTypes.installation_update) else None

    def as_invoke_activity(self):
        """
        Returns this activity as an InvokeActivity object;
        or None, if this is not that type of activity.

        :returns: This activity as an invoke activity; or None.
        """
        return self if self.__is_activity(ActivityTypes.invoke) else None

    def as_message_activity(self):
        """
        Returns this activity as a MessageActivity object;
        or None, if this is not that type of activity.

        :returns: This activity as a message activity; or None.
        """
        return self if self.__is_activity(ActivityTypes.message) else None

    def as_message_delete_activity(self):
        """
        Returns this activity as a MessageDeleteActivity object;
        or None, if this is not that type of activity.

        :returns: This activity as a message delete request; or None.
        """
        return self if self.__is_activity(ActivityTypes.message_delete) else None

    def as_message_reaction_activity(self):
        """
        Returns this activity as a MessageReactionActivity object;
        or None, if this is not that type of activity.

        :return: This activity as a message reaction activity; or None.
        """
        return self if self.__is_activity(ActivityTypes.message_reaction) else None

    def as_message_update_activity(self):
        """
        Returns this activity as an MessageUpdateActivity object;
        or None, if this is not that type of activity.

        :returns: This activity as a message update request; or None.
        """
        return self if self.__is_activity(ActivityTypes.message_update) else None

    def as_suggestion_activity(self):
        """
        Returns this activity as a SuggestionActivity object;
        or None, if this is not that type of activity.

        :returns: This activity as a suggestion activity; or None.
        """
        return self if self.__is_activity(ActivityTypes.suggestion) else None

    def as_trace_activity(self):
        """
        Returns this activity as a TraceActivity object;
        or None, if this is not that type of activity.

        :returns: This activity as a trace activity; or None.
        """
        return self if self.__is_activity(ActivityTypes.trace) else None

    def as_typing_activity(self):
        """
        Returns this activity as a TypingActivity object;
        or null, if this is not that type of activity.

        :returns: This activity as a typing activity; or null.
        """
        return self if self.__is_activity(ActivityTypes.typing) else None

    @staticmethod
    def create_contact_relation_update_activity():
        """
        Creates an instance of the :class:`Activity` class as aContactRelationUpdateActivity object.

        :returns: The new contact relation update activity.
        """
        return Activity(type=ActivityTypes.contact_relation_update)

    @staticmethod
    def create_conversation_update_activity():
        """
        Creates an instance of the :class:`Activity` class as a ConversationUpdateActivity object.

        :returns: The new conversation update activity.
        """
        return Activity(type=ActivityTypes.conversation_update)

    @staticmethod
    def create_end_of_conversation_activity():
        """
        Creates an instance of the :class:`Activity` class as an EndOfConversationActivity object.

        :returns: The new end of conversation activity.
        """
        return Activity(type=ActivityTypes.end_of_conversation)

    @staticmethod
    def create_event_activity():
        """
        Creates an instance of the :class:`Activity` class as an EventActivity object.

        :returns: The new event activity.
        """
        return Activity(type=ActivityTypes.event)

    @staticmethod
    def create_handoff_activity():
        """
        Creates an instance of the :class:`Activity` class as a HandoffActivity object.

        :returns: The new handoff activity.
        """
        return Activity(type=ActivityTypes.handoff)

    @staticmethod
    def create_invoke_activity():
        """
        Creates an instance of the :class:`Activity` class as an InvokeActivity object.

        :returns: The new invoke activity.
        """
        return Activity(type=ActivityTypes.invoke)

    @staticmethod
    def create_message_activity():
        """
        Creates an instance of the :class:`Activity` class as a MessageActivity object.

        :returns: The new message activity.
        """
        return Activity(type=ActivityTypes.message)

    def create_reply(self, text: str = None, locale: str = None):
        """
        Creates a new message activity as a response to this activity.

        :param text: The text of the reply.
        :param locale: The language code for the text.

        :returns: The new message activity.

        .. remarks::
            The new activity sets up routing information based on this activity.
        """
        return Activity(
            type=ActivityTypes.message,
            timestamp=datetime.utcnow(),
            from_property=ChannelAccount(
                id=self.recipient.id if self.recipient else None,
                name=self.recipient.name if self.recipient else None,
            ),
            recipient=ChannelAccount(
                id=self.from_property.id if self.from_property else None,
                name=self.from_property.name if self.from_property else None,
            ),
            reply_to_id=self.id,
            service_url=self.service_url,
            channel_id=self.channel_id,
            conversation=ConversationAccount(
                is_group=self.conversation.is_group,
                id=self.conversation.id,
                name=self.conversation.name,
            ),
            text=text if text else "",
            locale=locale if locale else self.locale,
            attachments=[],
            entities=[],
        )

    def create_trace(
        self, name: str, value: object = None, value_type: str = None, label: str = None
    ):
        """
        Creates a new trace activity based on this activity.

        :param name: The name of the trace operation to create.
        :param value: Optional, the content for this trace operation.
        :param value_type: Optional, identifier for the format of the value
        Default is the name of type of the value.
        :param label: Optional, a descriptive label for this trace operation.

        :returns: The new trace activity.
        """
        if not value_type and value:
            value_type = type(value)

        return Activity(
            type=ActivityTypes.trace,
            timestamp=datetime.utcnow(),
            from_property=ChannelAccount(
                id=self.recipient.id if self.recipient else None,
                name=self.recipient.name if self.recipient else None,
            ),
            recipient=ChannelAccount(
                id=self.from_property.id if self.from_property else None,
                name=self.from_property.name if self.from_property else None,
            ),
            reply_to_id=self.id,
            service_url=self.service_url,
            channel_id=self.channel_id,
            conversation=ConversationAccount(
                is_group=self.conversation.is_group,
                id=self.conversation.id,
                name=self.conversation.name,
            ),
            name=name,
            label=label,
            value_type=value_type,
            value=value,
        ).as_trace_activity()

    @staticmethod
    def create_trace_activity(
        name: str, value: object = None, value_type: str = None, label: str = None
    ):
        """
        Creates an instance of the :class:`Activity` class as a TraceActivity object.

        :param name: The name of the trace operation to create.
        :param value: Optional, the content for this trace operation.
        :param value_type: Optional, identifier for the format of the value.
        Default is the name of type of the value.
        :param label: Optional, a descriptive label for this trace operation.

        :returns: The new trace activity.
        """
        if not value_type and value:
            value_type = type(value)

        return Activity(
            type=ActivityTypes.trace,
            name=name,
            label=label,
            value_type=value_type,
            value=value,
        )

    @staticmethod
    def create_typing_activity():
        """
        Creates an instance of the :class:`Activity` class as a TypingActivity object.

        :returns: The new typing activity.
        """
        return Activity(type=ActivityTypes.typing)

    def get_conversation_reference(self):
        """
        Creates a ConversationReference based on this activity.

        :returns: A conversation reference for the conversation that contains this activity.
        """
        return ConversationReference(
            activity_id=self.id,
            user=self.from_property,
            bot=self.recipient,
            conversation=self.conversation,
            channel_id=self.channel_id,
            locale=self.locale,
            service_url=self.service_url,
        )

    def get_mentions(self) -> List[Mention]:
        """
        Resolves the mentions from the entities of this activity.

        :returns: The array of mentions; or an empty array, if none are found.

        .. remarks::
            This method is defined on the :class:`Activity` class, but is only intended
            for use with a message activity, where the activity Activity.Type is set to
            ActivityTypes.Message.
        """
        _list = self.entities
        return [x for x in _list if str(x.type).lower() == "mention"]

    def get_reply_conversation_reference(
        self, reply: ResourceResponse
    ) -> ConversationReference:
        """
        Create a ConversationReference based on this Activity's Conversation info
        and the ResourceResponse from sending an activity.

        :param reply: ResourceResponse returned from send_activity.

        :return: A ConversationReference that can be stored and used later to delete or update the activity.
        """
        reference = self.get_conversation_reference()
        reference.activity_id = reply.id
        return reference

    def has_content(self) -> bool:
        """
        Indicates whether this activity has content.

        :returns: True, if this activity has any content to send; otherwise, false.

        .. remarks::
            This method is defined on the :class:`Activity` class, but is only intended
            for use with a message activity, where the activity Activity.Type is set to
            ActivityTypes.Message.
        """
        if self.text and self.text.strip():
            return True

        if self.summary and self.summary.strip():
            return True

        if self.attachments and len(self.attachments) > 0:
            return True

        if self.channel_data:
            return True

        return False

    def is_from_streaming_connection(self) -> bool:
        """
        Determine if the Activity was sent via an Http/Https connection or Streaming
        This can be determined by looking at the service_url property:
        (1) All channels that send messages via http/https are not streaming
        (2) Channels that send messages via streaming have a ServiceUrl that does not begin with http/https.

        :returns: True if the Activity originated from a streaming connection.
        """
        if self.service_url:
            return not self.service_url.lower().startswith("http")
        return False

    def __is_activity(self, activity_type: str) -> bool:
        """
        Indicates whether this activity is of a specified activity type.

        :param activity_type: The activity type to check for.
        :return: True if this activity is of the specified activity type; otherwise, False.
        """
        if self.type is None:
            return False

        type_attribute = str(self.type).lower()
        activity_type = str(activity_type).lower()

        result = type_attribute.startswith(activity_type)

        if result:
            result = len(type_attribute) == len(activity_type)

            if not result:
                result = (
                    len(type_attribute) > len(activity_type)
                    and type_attribute[len(activity_type)] == "/"
                )

        return result


class AnimationCard(Model):
    """An animation card (Ex: gif or short video clip).

    :param title: Title of this card
    :type title: str
    :param subtitle: Subtitle of this card
    :type subtitle: str
    :param text: Text of this card
    :type text: str
    :param image: Thumbnail placeholder
    :type image: ~botframework.connector.models.ThumbnailUrl
    :param media: Media URLs for this card. When this field contains more than
     one URL, each URL is an alternative format of the same content.
    :type media: list[~botframework.connector.models.MediaUrl]
    :param buttons: Actions on this card
    :type buttons: list[~botframework.connector.models.CardAction]
    :param shareable: This content may be shared with others (default:true)
    :type shareable: bool
    :param autoloop: Should the client loop playback at end of content
     (default:true)
    :type autoloop: bool
    :param autostart: Should the client automatically start playback of media
     in this card (default:true)
    :type autostart: bool
    :param aspect: Aspect ratio of thumbnail/media placeholder. Allowed values
     are "16:9" and "4:3"
    :type aspect: str
    :param duration: Describes the length of the media content without
     requiring a receiver to open the content. Formatted as an ISO 8601
     Duration field.
    :type duration: str
    :param value: Supplementary parameter for this card
    :type value: object
    """

    _attribute_map = {
        "title": {"key": "title", "type": "str"},
        "subtitle": {"key": "subtitle", "type": "str"},
        "text": {"key": "text", "type": "str"},
        "image": {"key": "image", "type": "ThumbnailUrl"},
        "media": {"key": "media", "type": "[MediaUrl]"},
        "buttons": {"key": "buttons", "type": "[CardAction]"},
        "shareable": {"key": "shareable", "type": "bool"},
        "autoloop": {"key": "autoloop", "type": "bool"},
        "autostart": {"key": "autostart", "type": "bool"},
        "aspect": {"key": "aspect", "type": "str"},
        "duration": {"key": "duration", "type": "str"},
        "value": {"key": "value", "type": "object"},
    }

    def __init__(
        self,
        *,
        title: str = None,
        subtitle: str = None,
        text: str = None,
        image=None,
        media=None,
        buttons=None,
        shareable: bool = None,
        autoloop: bool = None,
        autostart: bool = None,
        aspect: str = None,
        duration: str = None,
        value=None,
        **kwargs
    ) -> None:
        super(AnimationCard, self).__init__(**kwargs)
        self.title = title
        self.subtitle = subtitle
        self.text = text
        self.image = image
        self.media = media
        self.buttons = buttons
        self.shareable = shareable
        self.autoloop = autoloop
        self.autostart = autostart
        self.aspect = aspect
        self.duration = duration
        self.value = value


class Attachment(Model):
    """An attachment within an activity.

    :param content_type: mimetype/Contenttype for the file
    :type content_type: str
    :param content_url: Content Url
    :type content_url: str
    :param content: Embedded content
    :type content: object
    :param name: (OPTIONAL) The name of the attachment
    :type name: str
    :param thumbnail_url: (OPTIONAL) Thumbnail associated with attachment
    :type thumbnail_url: str
    """

    _attribute_map = {
        "content_type": {"key": "contentType", "type": "str"},
        "content_url": {"key": "contentUrl", "type": "str"},
        "content": {"key": "content", "type": "object"},
        "name": {"key": "name", "type": "str"},
        "thumbnail_url": {"key": "thumbnailUrl", "type": "str"},
    }

    def __init__(
        self,
        *,
        content_type: str = None,
        content_url: str = None,
        content=None,
        name: str = None,
        thumbnail_url: str = None,
        **kwargs
    ) -> None:
        super(Attachment, self).__init__(**kwargs)
        self.content_type = content_type
        self.content_url = content_url
        self.content = content
        self.name = name
        self.thumbnail_url = thumbnail_url


class AttachmentData(Model):
    """Attachment data.

    :param type: Content-Type of the attachment
    :type type: str
    :param name: Name of the attachment
    :type name: str
    :param original_base64: Attachment content
    :type original_base64: bytearray
    :param thumbnail_base64: Attachment thumbnail
    :type thumbnail_base64: bytearray
    """

    _attribute_map = {
        "type": {"key": "type", "type": "str"},
        "name": {"key": "name", "type": "str"},
        "original_base64": {"key": "originalBase64", "type": "bytearray"},
        "thumbnail_base64": {"key": "thumbnailBase64", "type": "bytearray"},
    }

    def __init__(
        self,
        *,
        type: str = None,
        name: str = None,
        original_base64: bytearray = None,
        thumbnail_base64: bytearray = None,
        **kwargs
    ) -> None:
        super(AttachmentData, self).__init__(**kwargs)
        self.type = type
        self.name = name
        self.original_base64 = original_base64
        self.thumbnail_base64 = thumbnail_base64


class AttachmentInfo(Model):
    """Metadata for an attachment.

    :param name: Name of the attachment
    :type name: str
    :param type: ContentType of the attachment
    :type type: str
    :param views: attachment views
    :type views: list[~botframework.connector.models.AttachmentView]
    """

    _attribute_map = {
        "name": {"key": "name", "type": "str"},
        "type": {"key": "type", "type": "str"},
        "views": {"key": "views", "type": "[AttachmentView]"},
    }

    def __init__(
        self, *, name: str = None, type: str = None, views=None, **kwargs
    ) -> None:
        super(AttachmentInfo, self).__init__(**kwargs)
        self.name = name
        self.type = type
        self.views = views


class AttachmentView(Model):
    """Attachment View name and size.

    :param view_id: Id of the attachment
    :type view_id: str
    :param size: Size of the attachment
    :type size: int
    """

    _attribute_map = {
        "view_id": {"key": "viewId", "type": "str"},
        "size": {"key": "size", "type": "int"},
    }

    def __init__(self, *, view_id: str = None, size: int = None, **kwargs) -> None:
        super(AttachmentView, self).__init__(**kwargs)
        self.view_id = view_id
        self.size = size


class AudioCard(Model):
    """Audio card.

    :param title: Title of this card
    :type title: str
    :param subtitle: Subtitle of this card
    :type subtitle: str
    :param text: Text of this card
    :type text: str
    :param image: Thumbnail placeholder
    :type image: ~botframework.connector.models.ThumbnailUrl
    :param media: Media URLs for this card. When this field contains more than
     one URL, each URL is an alternative format of the same content.
    :type media: list[~botframework.connector.models.MediaUrl]
    :param buttons: Actions on this card
    :type buttons: list[~botframework.connector.models.CardAction]
    :param shareable: This content may be shared with others (default:true)
    :type shareable: bool
    :param autoloop: Should the client loop playback at end of content
     (default:true)
    :type autoloop: bool
    :param autostart: Should the client automatically start playback of media
     in this card (default:true)
    :type autostart: bool
    :param aspect: Aspect ratio of thumbnail/media placeholder. Allowed values
     are "16:9" and "4:3"
    :type aspect: str
    :param duration: Describes the length of the media content without
     requiring a receiver to open the content. Formatted as an ISO 8601
     Duration field.
    :type duration: str
    :param value: Supplementary parameter for this card
    :type value: object
    """

    _attribute_map = {
        "title": {"key": "title", "type": "str"},
        "subtitle": {"key": "subtitle", "type": "str"},
        "text": {"key": "text", "type": "str"},
        "image": {"key": "image", "type": "ThumbnailUrl"},
        "media": {"key": "media", "type": "[MediaUrl]"},
        "buttons": {"key": "buttons", "type": "[CardAction]"},
        "shareable": {"key": "shareable", "type": "bool"},
        "autoloop": {"key": "autoloop", "type": "bool"},
        "autostart": {"key": "autostart", "type": "bool"},
        "aspect": {"key": "aspect", "type": "str"},
        "duration": {"key": "duration", "type": "str"},
        "value": {"key": "value", "type": "object"},
    }

    def __init__(
        self,
        *,
        title: str = None,
        subtitle: str = None,
        text: str = None,
        image=None,
        media=None,
        buttons=None,
        shareable: bool = None,
        autoloop: bool = None,
        autostart: bool = None,
        aspect: str = None,
        duration: str = None,
        value=None,
        **kwargs
    ) -> None:
        super(AudioCard, self).__init__(**kwargs)
        self.title = title
        self.subtitle = subtitle
        self.text = text
        self.image = image
        self.media = media
        self.buttons = buttons
        self.shareable = shareable
        self.autoloop = autoloop
        self.autostart = autostart
        self.aspect = aspect
        self.duration = duration
        self.value = value


class BasicCard(Model):
    """A basic card.

    :param title: Title of the card
    :type title: str
    :param subtitle: Subtitle of the card
    :type subtitle: str
    :param text: Text for the card
    :type text: str
    :param images: Array of images for the card
    :type images: list[~botframework.connector.models.CardImage]
    :param buttons: Set of actions applicable to the current card
    :type buttons: list[~botframework.connector.models.CardAction]
    :param tap: This action will be activated when user taps on the card
     itself
    :type tap: ~botframework.connector.models.CardAction
    """

    _attribute_map = {
        "title": {"key": "title", "type": "str"},
        "subtitle": {"key": "subtitle", "type": "str"},
        "text": {"key": "text", "type": "str"},
        "images": {"key": "images", "type": "[CardImage]"},
        "buttons": {"key": "buttons", "type": "[CardAction]"},
        "tap": {"key": "tap", "type": "CardAction"},
    }

    def __init__(
        self,
        *,
        title: str = None,
        subtitle: str = None,
        text: str = None,
        images=None,
        buttons=None,
        tap=None,
        **kwargs
    ) -> None:
        super(BasicCard, self).__init__(**kwargs)
        self.title = title
        self.subtitle = subtitle
        self.text = text
        self.images = images
        self.buttons = buttons
        self.tap = tap


class CardAction(Model):
    """A clickable action.

    :param type: The type of action implemented by this button. Possible
     values include: 'openUrl', 'imBack', 'postBack', 'playAudio', 'playVideo',
     'showImage', 'downloadFile', 'signin', 'call', 'messageBack'
    :type type: str or ~botframework.connector.models.ActionTypes
    :param title: Text description which appears on the button
    :type title: str
    :param image: Image URL which will appear on the button, next to text
     label
    :type image: str
    :param text: Text for this action
    :type text: str
    :param display_text: (Optional) text to display in the chat feed if the
     button is clicked
    :type display_text: str
    :param value: Supplementary parameter for action. Content of this property
     depends on the ActionType
    :type value: object
    :param channel_data: Channel-specific data associated with this action
    :type channel_data: object
    :param image_alt_text: Alternate image text to be used in place of the `image` field
    :type image_alt_text: str
    """

    _attribute_map = {
        "type": {"key": "type", "type": "str"},
        "title": {"key": "title", "type": "str"},
        "image": {"key": "image", "type": "str"},
        "text": {"key": "text", "type": "str"},
        "display_text": {"key": "displayText", "type": "str"},
        "value": {"key": "value", "type": "object"},
        "channel_data": {"key": "channelData", "type": "object"},
        "image_alt_text": {"key": "imageAltText", "type": "str"},
    }

    def __init__(
        self,
        *,
        type=None,
        title: str = None,
        image: str = None,
        text: str = None,
        display_text: str = None,
        value=None,
        channel_data=None,
        image_alt_text: str = None,
        **kwargs
    ) -> None:
        super(CardAction, self).__init__(**kwargs)
        self.type = type
        self.title = title
        self.image = image
        self.text = text
        self.display_text = display_text
        self.value = value
        self.channel_data = channel_data
        self.image_alt_text = image_alt_text


class CardImage(Model):
    """An image on a card.

    :param url: URL thumbnail image for major content property
    :type url: str
    :param alt: Image description intended for screen readers
    :type alt: str
    :param tap: Action assigned to specific Attachment
    :type tap: ~botframework.connector.models.CardAction
    """

    _attribute_map = {
        "url": {"key": "url", "type": "str"},
        "alt": {"key": "alt", "type": "str"},
        "tap": {"key": "tap", "type": "CardAction"},
    }

    def __init__(self, *, url: str = None, alt: str = None, tap=None, **kwargs) -> None:
        super(CardImage, self).__init__(**kwargs)
        self.url = url
        self.alt = alt
        self.tap = tap


class ChannelAccount(Model):
    """Channel account information needed to route a message.

    :param id: Channel id for the user or bot on this channel (Example:
     joe@smith.com, or @joesmith or 123456)
    :type id: str
    :param name: Display friendly name
    :type name: str
    :param aad_object_id: This account's object ID within Azure Active
     Directory (AAD)
    :type aad_object_id: str
    :param role: Role of the entity behind the account (Example: User, Bot,
     etc.). Possible values include: 'user', 'bot'
    :type role: str or ~botframework.connector.models.RoleTypes
    """

    _attribute_map = {
        "id": {"key": "id", "type": "str"},
        "name": {"key": "name", "type": "str"},
        "aad_object_id": {"key": "aadObjectId", "type": "str"},
        "role": {"key": "role", "type": "str"},
    }

    def __init__(
        self,
        *,
        id: str = None,
        name: str = None,
        aad_object_id: str = None,
        role=None,
        **kwargs
    ) -> None:
        super(ChannelAccount, self).__init__(**kwargs)
        self.id = id
        self.name = name
        self.aad_object_id = aad_object_id
        self.role = role


class ConversationAccount(Model):
    """Conversation account represents the identity of the conversation within a channel.

    :param is_group: Indicates whether the conversation contains more than two
     participants at the time the activity was generated
    :type is_group: bool
    :param conversation_type: Indicates the type of the conversation in
     channels that distinguish between conversation types
    :type conversation_type: str
    :param id: Channel id for the user or bot on this channel (Example:
     joe@smith.com, or @joesmith or 123456)
    :type id: str
    :param name: Display friendly name
    :type name: str
    :param aad_object_id: This account's object ID within Azure Active
     Directory (AAD)
    :type aad_object_id: str
    :param role: Role of the entity behind the account (Example: User, Bot, Skill
     etc.). Possible values include: 'user', 'bot', 'skill'
    :type role: str or ~botframework.connector.models.RoleTypes
    :param tenant_id: This conversation's tenant ID
    :type tenant_id: str
    :param properties: This conversation's properties
    :type properties: object
    """

    _attribute_map = {
        "is_group": {"key": "isGroup", "type": "bool"},
        "conversation_type": {"key": "conversationType", "type": "str"},
        "id": {"key": "id", "type": "str"},
        "name": {"key": "name", "type": "str"},
        "aad_object_id": {"key": "aadObjectId", "type": "str"},
        "role": {"key": "role", "type": "str"},
        "tenant_id": {"key": "tenantID", "type": "str"},
        "properties": {"key": "properties", "type": "object"},
    }

    def __init__(
        self,
        *,
        is_group: bool = None,
        conversation_type: str = None,
        id: str = None,
        name: str = None,
        aad_object_id: str = None,
        role=None,
        tenant_id=None,
        properties=None,
        **kwargs
    ) -> None:
        super(ConversationAccount, self).__init__(**kwargs)
        self.is_group = is_group
        self.conversation_type = conversation_type
        self.id = id
        self.name = name
        self.aad_object_id = aad_object_id
        self.role = role
        self.tenant_id = tenant_id
        self.properties = properties


class ConversationMembers(Model):
    """Conversation and its members.

    :param id: Conversation ID
    :type id: str
    :param members: List of members in this conversation
    :type members: list[~botframework.connector.models.ChannelAccount]
    """

    _attribute_map = {
        "id": {"key": "id", "type": "str"},
        "members": {"key": "members", "type": "[ChannelAccount]"},
    }

    def __init__(self, *, id: str = None, members=None, **kwargs) -> None:
        super(ConversationMembers, self).__init__(**kwargs)
        self.id = id
        self.members = members


class ConversationParameters(Model):
    """Parameters for creating a new conversation.

    :param is_group: IsGroup
    :type is_group: bool
    :param bot: The bot address for this conversation
    :type bot: ~botframework.connector.models.ChannelAccount
    :param members: Members to add to the conversation
    :type members: list[~botframework.connector.models.ChannelAccount]
    :param topic_name: (Optional) Topic of the conversation (if supported by
     the channel)
    :type topic_name: str
    :param activity: (Optional) When creating a new conversation, use this
     activity as the initial message to the conversation
    :type activity: ~botframework.connector.models.Activity
    :param channel_data: Channel specific payload for creating the
     conversation
    :type channel_data: object
    :param tenant_id: (Optional) The tenant ID in which the conversation should be created
    :type tenant_id: str
    """

    _attribute_map = {
        "is_group": {"key": "isGroup", "type": "bool"},
        "bot": {"key": "bot", "type": "ChannelAccount"},
        "members": {"key": "members", "type": "[ChannelAccount]"},
        "topic_name": {"key": "topicName", "type": "str"},
        "activity": {"key": "activity", "type": "Activity"},
        "channel_data": {"key": "channelData", "type": "object"},
        "tenant_id": {"key": "tenantID", "type": "str"},
    }

    def __init__(
        self,
        *,
        is_group: bool = None,
        bot=None,
        members=None,
        topic_name: str = None,
        activity=None,
        channel_data=None,
        tenant_id=None,
        **kwargs
    ) -> None:
        super(ConversationParameters, self).__init__(**kwargs)
        self.is_group = is_group
        self.bot = bot
        self.members = members
        self.topic_name = topic_name
        self.activity = activity
        self.channel_data = channel_data
        self.tenant_id = tenant_id


class ConversationResourceResponse(Model):
    """A response containing a resource.

    :param activity_id: ID of the Activity (if sent)
    :type activity_id: str
    :param service_url: Service endpoint where operations concerning the
     conversation may be performed
    :type service_url: str
    :param id: Id of the resource
    :type id: str
    """

    _attribute_map = {
        "activity_id": {"key": "activityId", "type": "str"},
        "service_url": {"key": "serviceUrl", "type": "str"},
        "id": {"key": "id", "type": "str"},
    }

    def __init__(
        self,
        *,
        activity_id: str = None,
        service_url: str = None,
        id: str = None,
        **kwargs
    ) -> None:
        super(ConversationResourceResponse, self).__init__(**kwargs)
        self.activity_id = activity_id
        self.service_url = service_url
        self.id = id


class ConversationsResult(Model):
    """Conversations result.

    :param continuation_token: Paging token
    :type continuation_token: str
    :param conversations: List of conversations
    :type conversations:
     list[~botframework.connector.models.ConversationMembers]
    """

    _attribute_map = {
        "continuation_token": {"key": "continuationToken", "type": "str"},
        "conversations": {"key": "conversations", "type": "[ConversationMembers]"},
    }

    def __init__(
        self, *, continuation_token: str = None, conversations=None, **kwargs
    ) -> None:
        super(ConversationsResult, self).__init__(**kwargs)
        self.continuation_token = continuation_token
        self.conversations = conversations


class ExpectedReplies(Model):
    """ExpectedReplies.

    :param activities: A collection of Activities that conforms to the
     ExpectedReplies schema.
    :type activities: list[~botframework.connector.models.Activity]
    """

    _attribute_map = {"activities": {"key": "activities", "type": "[Activity]"}}

    def __init__(self, *, activities=None, **kwargs) -> None:
        super(ExpectedReplies, self).__init__(**kwargs)
        self.activities = activities


class Entity(Model):
    """Metadata object pertaining to an activity.

    :param type: Type of this entity (RFC 3987 IRI)
    :type type: str
    """

    _attribute_map = {"type": {"key": "type", "type": "str"}}

    def __init__(self, *, type: str = None, **kwargs) -> None:
        super(Entity, self).__init__(**kwargs)
        self.type = type


class Error(Model):
    """Object representing error information.

    :param code: Error code
    :type code: str
    :param message: Error message
    :type message: str
    :param inner_http_error: Error from inner http call
    :type inner_http_error: ~botframework.connector.models.InnerHttpError
    """

    _attribute_map = {
        "code": {"key": "code", "type": "str"},
        "message": {"key": "message", "type": "str"},
        "inner_http_error": {"key": "innerHttpError", "type": "InnerHttpError"},
    }

    def __init__(
        self, *, code: str = None, message: str = None, inner_http_error=None, **kwargs
    ) -> None:
        super(Error, self).__init__(**kwargs)
        self.code = code
        self.message = message
        self.inner_http_error = inner_http_error


class ErrorResponse(Model):
    """An HTTP API response.

    :param error: Error message
    :type error: ~botframework.connector.models.Error
    """

    _attribute_map = {"error": {"key": "error", "type": "Error"}}

    def __init__(self, *, error=None, **kwargs) -> None:
        super(ErrorResponse, self).__init__(**kwargs)
        self.error = error


class ErrorResponseException(HttpOperationError):
    """Server responsed with exception of type: 'ErrorResponse'.

    :param deserialize: A deserializer
    :param response: Server response to be deserialized.
    """

    def __init__(self, deserialize, response, *args):

        super(ErrorResponseException, self).__init__(
            deserialize, response, "ErrorResponse", *args
        )


class Fact(Model):
    """Set of key-value pairs. Advantage of this section is that key and value
    properties will be
    rendered with default style information with some delimiter between them.
    So there is no need for developer to specify style information.

    :param key: The key for this Fact
    :type key: str
    :param value: The value for this Fact
    :type value: str
    """

    _attribute_map = {
        "key": {"key": "key", "type": "str"},
        "value": {"key": "value", "type": "str"},
    }

    def __init__(self, *, key: str = None, value: str = None, **kwargs) -> None:
        super(Fact, self).__init__(**kwargs)
        self.key = key
        self.value = value


class GeoCoordinates(Model):
    """GeoCoordinates (entity type: "https://schema.org/GeoCoordinates").

    :param elevation: Elevation of the location [WGS
     84](https://en.wikipedia.org/wiki/World_Geodetic_System)
    :type elevation: float
    :param latitude: Latitude of the location [WGS
     84](https://en.wikipedia.org/wiki/World_Geodetic_System)
    :type latitude: float
    :param longitude: Longitude of the location [WGS
     84](https://en.wikipedia.org/wiki/World_Geodetic_System)
    :type longitude: float
    :param type: The type of the thing
    :type type: str
    :param name: The name of the thing
    :type name: str
    """

    _attribute_map = {
        "elevation": {"key": "elevation", "type": "float"},
        "latitude": {"key": "latitude", "type": "float"},
        "longitude": {"key": "longitude", "type": "float"},
        "type": {"key": "type", "type": "str"},
        "name": {"key": "name", "type": "str"},
    }

    def __init__(
        self,
        *,
        elevation: float = None,
        latitude: float = None,
        longitude: float = None,
        type: str = None,
        name: str = None,
        **kwargs
    ) -> None:
        super(GeoCoordinates, self).__init__(**kwargs)
        self.elevation = elevation
        self.latitude = latitude
        self.longitude = longitude
        self.type = type
        self.name = name


class HeroCard(Model):
    """A Hero card (card with a single, large image).

    :param title: Title of the card
    :type title: str
    :param subtitle: Subtitle of the card
    :type subtitle: str
    :param text: Text for the card
    :type text: str
    :param images: Array of images for the card
    :type images: list[~botframework.connector.models.CardImage]
    :param buttons: Set of actions applicable to the current card
    :type buttons: list[~botframework.connector.models.CardAction]
    :param tap: This action will be activated when user taps on the card
     itself
    :type tap: ~botframework.connector.models.CardAction
    """

    _attribute_map = {
        "title": {"key": "title", "type": "str"},
        "subtitle": {"key": "subtitle", "type": "str"},
        "text": {"key": "text", "type": "str"},
        "images": {"key": "images", "type": "[CardImage]"},
        "buttons": {"key": "buttons", "type": "[CardAction]"},
        "tap": {"key": "tap", "type": "CardAction"},
    }

    def __init__(
        self,
        *,
        title: str = None,
        subtitle: str = None,
        text: str = None,
        images=None,
        buttons=None,
        tap=None,
        **kwargs
    ) -> None:
        super(HeroCard, self).__init__(**kwargs)
        self.title = title
        self.subtitle = subtitle
        self.text = text
        self.images = images
        self.buttons = buttons
        self.tap = tap


class InnerHttpError(Model):
    """Object representing inner http error.

    :param status_code: HttpStatusCode from failed request
    :type status_code: int
    :param body: Body from failed request
    :type body: object
    """

    _attribute_map = {
        "status_code": {"key": "statusCode", "type": "int"},
        "body": {"key": "body", "type": "object"},
    }

    def __init__(self, *, status_code: int = None, body=None, **kwargs) -> None:
        super(InnerHttpError, self).__init__(**kwargs)
        self.status_code = status_code
        self.body = body


class InvokeResponse(Model):
    """
    Tuple class containing an HTTP Status Code and a JSON serializable
    object. The HTTP Status code is, in the invoke activity scenario, what will
    be set in the resulting POST. The Body of the resulting POST will be
    JSON serialized content.

    The body content is defined by the producer.  The caller must know what
    the content is and deserialize as needed.
    """

    _attribute_map = {
        "status": {"key": "status", "type": "int"},
        "body": {"key": "body", "type": "object"},
    }

    def __init__(self, *, status: int = None, body: object = None, **kwargs):
        """
        Gets or sets the HTTP status and/or body code for the response
        :param status: The HTTP status code.
        :param body: The JSON serializable body content for the response.  This object
        must be serializable by the core Python json routines.  The caller is responsible
        for serializing more complex/nested objects into native classes (lists and
        dictionaries of strings are acceptable).
        """
        super().__init__(**kwargs)
        self.status = status
        self.body = body

    def is_successful_status_code(self) -> bool:
        """
        Gets a value indicating whether the invoke response was successful.
        :return: A value that indicates if the HTTP response was successful. true if status is in
        the Successful range (200-299); otherwise false.
        """
        return 200 <= self.status <= 299


class MediaCard(Model):
    """Media card.

    :param title: Title of this card
    :type title: str
    :param subtitle: Subtitle of this card
    :type subtitle: str
    :param text: Text of this card
    :type text: str
    :param image: Thumbnail placeholder
    :type image: ~botframework.connector.models.ThumbnailUrl
    :param media: Media URLs for this card. When this field contains more than
     one URL, each URL is an alternative format of the same content.
    :type media: list[~botframework.connector.models.MediaUrl]
    :param buttons: Actions on this card
    :type buttons: list[~botframework.connector.models.CardAction]
    :param shareable: This content may be shared with others (default:true)
    :type shareable: bool
    :param autoloop: Should the client loop playback at end of content
     (default:true)
    :type autoloop: bool
    :param autostart: Should the client automatically start playback of media
     in this card (default:true)
    :type autostart: bool
    :param aspect: Aspect ratio of thumbnail/media placeholder. Allowed values
     are "16:9" and "4:3"
    :type aspect: str
    :param duration: Describes the length of the media content without
     requiring a receiver to open the content. Formatted as an ISO 8601
     Duration field.
    :type duration: str
    :param value: Supplementary parameter for this card
    :type value: object
    """

    _attribute_map = {
        "title": {"key": "title", "type": "str"},
        "subtitle": {"key": "subtitle", "type": "str"},
        "text": {"key": "text", "type": "str"},
        "image": {"key": "image", "type": "ThumbnailUrl"},
        "media": {"key": "media", "type": "[MediaUrl]"},
        "buttons": {"key": "buttons", "type": "[CardAction]"},
        "shareable": {"key": "shareable", "type": "bool"},
        "autoloop": {"key": "autoloop", "type": "bool"},
        "autostart": {"key": "autostart", "type": "bool"},
        "aspect": {"key": "aspect", "type": "str"},
        "duration": {"key": "duration", "type": "str"},
        "value": {"key": "value", "type": "object"},
    }

    def __init__(
        self,
        *,
        title: str = None,
        subtitle: str = None,
        text: str = None,
        image=None,
        media=None,
        buttons=None,
        shareable: bool = None,
        autoloop: bool = None,
        autostart: bool = None,
        aspect: str = None,
        duration: str = None,
        value=None,
        **kwargs
    ) -> None:
        super(MediaCard, self).__init__(**kwargs)
        self.title = title
        self.subtitle = subtitle
        self.text = text
        self.image = image
        self.media = media
        self.buttons = buttons
        self.shareable = shareable
        self.autoloop = autoloop
        self.autostart = autostart
        self.aspect = aspect
        self.duration = duration
        self.value = value


class MediaEventValue(Model):
    """Supplementary parameter for media events.

    :param card_value: Callback parameter specified in the Value field of the
     MediaCard that originated this event
    :type card_value: object
    """

    _attribute_map = {"card_value": {"key": "cardValue", "type": "object"}}

    def __init__(self, *, card_value=None, **kwargs) -> None:
        super(MediaEventValue, self).__init__(**kwargs)
        self.card_value = card_value


class MediaUrl(Model):
    """Media URL.

    :param url: Url for the media
    :type url: str
    :param profile: Optional profile hint to the client to differentiate
     multiple MediaUrl objects from each other
    :type profile: str
    """

    _attribute_map = {
        "url": {"key": "url", "type": "str"},
        "profile": {"key": "profile", "type": "str"},
    }

    def __init__(self, *, url: str = None, profile: str = None, **kwargs) -> None:
        super(MediaUrl, self).__init__(**kwargs)
        self.url = url
        self.profile = profile


class MessageReaction(Model):
    """Message reaction object.

    :param type: Message reaction type. Possible values include: 'like',
     'plusOne'
    :type type: str or ~botframework.connector.models.MessageReactionTypes
    """

    _attribute_map = {"type": {"key": "type", "type": "str"}}

    def __init__(self, *, type=None, **kwargs) -> None:
        super(MessageReaction, self).__init__(**kwargs)
        self.type = type


class OAuthCard(Model):
    """A card representing a request to perform a sign in via OAuth.

    :param text: Text for signin request
    :type text: str
    :param connection_name: The name of the registered connection
    :type connection_name: str
    :param buttons: Action to use to perform signin
    :type buttons: list[~botframework.connector.models.CardAction]
    """

    _attribute_map = {
        "text": {"key": "text", "type": "str"},
        "connection_name": {"key": "connectionName", "type": "str"},
        "buttons": {"key": "buttons", "type": "[CardAction]"},
        "token_exchange_resource": {"key": "tokenExchangeResource", "type": "object"},
    }

    def __init__(
        self,
        *,
        text: str = None,
        connection_name: str = None,
        buttons=None,
        token_exchange_resource=None,
        **kwargs
    ) -> None:
        super(OAuthCard, self).__init__(**kwargs)
        self.text = text
        self.connection_name = connection_name
        self.buttons = buttons
        self.token_exchange_resource = token_exchange_resource


class PagedMembersResult(Model):
    """Page of members.

    :param continuation_token: Paging token
    :type continuation_token: str
    :param members: The Channel Accounts.
    :type members: list[~botframework.connector.models.ChannelAccount]
    """

    _attribute_map = {
        "continuation_token": {"key": "continuationToken", "type": "str"},
        "members": {"key": "members", "type": "[ChannelAccount]"},
    }

    def __init__(
        self, *, continuation_token: str = None, members=None, **kwargs
    ) -> None:
        super(PagedMembersResult, self).__init__(**kwargs)
        self.continuation_token = continuation_token
        self.members = members


class Place(Model):
    """Place (entity type: "https://schema.org/Place").

    :param address: Address of the place (may be `string` or complex object of
     type `PostalAddress`)
    :type address: object
    :param geo: Geo coordinates of the place (may be complex object of type
     `GeoCoordinates` or `GeoShape`)
    :type geo: object
    :param has_map: Map to the place (may be `string` (URL) or complex object
     of type `Map`)
    :type has_map: object
    :param type: The type of the thing
    :type type: str
    :param name: The name of the thing
    :type name: str
    """

    _attribute_map = {
        "address": {"key": "address", "type": "object"},
        "geo": {"key": "geo", "type": "object"},
        "has_map": {"key": "hasMap", "type": "object"},
        "type": {"key": "type", "type": "str"},
        "name": {"key": "name", "type": "str"},
    }

    def __init__(
        self,
        *,
        address=None,
        geo=None,
        has_map=None,
        type: str = None,
        name: str = None,
        **kwargs
    ) -> None:
        super(Place, self).__init__(**kwargs)
        self.address = address
        self.geo = geo
        self.has_map = has_map
        self.type = type
        self.name = name


class ReceiptCard(Model):
    """A receipt card.

    :param title: Title of the card
    :type title: str
    :param facts: Array of Fact objects
    :type facts: list[~botframework.connector.models.Fact]
    :param items: Array of Receipt Items
    :type items: list[~botframework.connector.models.ReceiptItem]
    :param tap: This action will be activated when user taps on the card
    :type tap: ~botframework.connector.models.CardAction
    :param total: Total amount of money paid (or to be paid)
    :type total: str
    :param tax: Total amount of tax paid (or to be paid)
    :type tax: str
    :param vat: Total amount of VAT paid (or to be paid)
    :type vat: str
    :param buttons: Set of actions applicable to the current card
    :type buttons: list[~botframework.connector.models.CardAction]
    """

    _attribute_map = {
        "title": {"key": "title", "type": "str"},
        "facts": {"key": "facts", "type": "[Fact]"},
        "items": {"key": "items", "type": "[ReceiptItem]"},
        "tap": {"key": "tap", "type": "CardAction"},
        "total": {"key": "total", "type": "str"},
        "tax": {"key": "tax", "type": "str"},
        "vat": {"key": "vat", "type": "str"},
        "buttons": {"key": "buttons", "type": "[CardAction]"},
    }

    def __init__(
        self,
        *,
        title: str = None,
        facts=None,
        items=None,
        tap=None,
        total: str = None,
        tax: str = None,
        vat: str = None,
        buttons=None,
        **kwargs
    ) -> None:
        super(ReceiptCard, self).__init__(**kwargs)
        self.title = title
        self.facts = facts
        self.items = items
        self.tap = tap
        self.total = total
        self.tax = tax
        self.vat = vat
        self.buttons = buttons


class ReceiptItem(Model):
    """An item on a receipt card.

    :param title: Title of the Card
    :type title: str
    :param subtitle: Subtitle appears just below Title field, differs from
     Title in font styling only
    :type subtitle: str
    :param text: Text field appears just below subtitle, differs from Subtitle
     in font styling only
    :type text: str
    :param image: Image
    :type image: ~botframework.connector.models.CardImage
    :param price: Amount with currency
    :type price: str
    :param quantity: Number of items of given kind
    :type quantity: str
    :param tap: This action will be activated when user taps on the Item
     bubble.
    :type tap: ~botframework.connector.models.CardAction
    """

    _attribute_map = {
        "title": {"key": "title", "type": "str"},
        "subtitle": {"key": "subtitle", "type": "str"},
        "text": {"key": "text", "type": "str"},
        "image": {"key": "image", "type": "CardImage"},
        "price": {"key": "price", "type": "str"},
        "quantity": {"key": "quantity", "type": "str"},
        "tap": {"key": "tap", "type": "CardAction"},
    }

    def __init__(
        self,
        *,
        title: str = None,
        subtitle: str = None,
        text: str = None,
        image=None,
        price: str = None,
        quantity: str = None,
        tap=None,
        **kwargs
    ) -> None:
        super(ReceiptItem, self).__init__(**kwargs)
        self.title = title
        self.subtitle = subtitle
        self.text = text
        self.image = image
        self.price = price
        self.quantity = quantity
        self.tap = tap


class SemanticAction(Model):
    """Represents a reference to a programmatic action.

    :param id: ID of this action
    :type id: str
    :param entities: Entities associated with this action
    :type entities: dict[str, ~botframework.connector.models.Entity]
    :param state: State of this action. Allowed values: `start`, `continue`, `done`
    :type state: str or ~botframework.connector.models.SemanticActionStates
    """

    _attribute_map = {
        "id": {"key": "id", "type": "str"},
        "entities": {"key": "entities", "type": "{Entity}"},
        "state": {"key": "state", "type": "str"},
    }

    def __init__(self, *, id: str = None, entities=None, state=None, **kwargs) -> None:
        super(SemanticAction, self).__init__(**kwargs)
        self.id = id
        self.entities = entities
        self.state = state


class SigninCard(Model):
    """A card representing a request to sign in.

    :param text: Text for signin request
    :type text: str
    :param buttons: Action to use to perform signin
    :type buttons: list[~botframework.connector.models.CardAction]
    """

    _attribute_map = {
        "text": {"key": "text", "type": "str"},
        "buttons": {"key": "buttons", "type": "[CardAction]"},
    }

    def __init__(self, *, text: str = None, buttons=None, **kwargs) -> None:
        super(SigninCard, self).__init__(**kwargs)
        self.text = text
        self.buttons = buttons


class SuggestedActions(Model):
    """SuggestedActions that can be performed.

    :param to: Ids of the recipients that the actions should be shown to.
     These Ids are relative to the channelId and a subset of all recipients of
     the activity
    :type to: list[str]
    :param actions: Actions that can be shown to the user
    :type actions: list[~botframework.connector.models.CardAction]
    """

    _attribute_map = {
        "to": {"key": "to", "type": "[str]"},
        "actions": {"key": "actions", "type": "[CardAction]"},
    }

    def __init__(self, *, to=None, actions=None, **kwargs) -> None:
        super(SuggestedActions, self).__init__(**kwargs)
        self.to = to
        self.actions = actions


class TextHighlight(Model):
    """Refers to a substring of content within another field.

    :param text: Defines the snippet of text to highlight
    :type text: str
    :param occurrence: Occurrence of the text field within the referenced
     text, if multiple exist.
    :type occurrence: int
    """

    _attribute_map = {
        "text": {"key": "text", "type": "str"},
        "occurrence": {"key": "occurrence", "type": "int"},
    }

    def __init__(self, *, text: str = None, occurrence: int = None, **kwargs) -> None:
        super(TextHighlight, self).__init__(**kwargs)
        self.text = text
        self.occurrence = occurrence


class Thing(Model):
    """Thing (entity type: "https://schema.org/Thing").

    :param type: The type of the thing
    :type type: str
    :param name: The name of the thing
    :type name: str
    """

    _attribute_map = {
        "type": {"key": "type", "type": "str"},
        "name": {"key": "name", "type": "str"},
    }

    def __init__(self, *, type: str = None, name: str = None, **kwargs) -> None:
        super(Thing, self).__init__(**kwargs)
        self.type = type
        self.name = name


class ThumbnailCard(Model):
    """A thumbnail card (card with a single, small thumbnail image).

    :param title: Title of the card
    :type title: str
    :param subtitle: Subtitle of the card
    :type subtitle: str
    :param text: Text for the card
    :type text: str
    :param images: Array of images for the card
    :type images: list[~botframework.connector.models.CardImage]
    :param buttons: Set of actions applicable to the current card
    :type buttons: list[~botframework.connector.models.CardAction]
    :param tap: This action will be activated when user taps on the card
     itself
    :type tap: ~botframework.connector.models.CardAction
    """

    _attribute_map = {
        "title": {"key": "title", "type": "str"},
        "subtitle": {"key": "subtitle", "type": "str"},
        "text": {"key": "text", "type": "str"},
        "images": {"key": "images", "type": "[CardImage]"},
        "buttons": {"key": "buttons", "type": "[CardAction]"},
        "tap": {"key": "tap", "type": "CardAction"},
    }

    def __init__(
        self,
        *,
        title: str = None,
        subtitle: str = None,
        text: str = None,
        images=None,
        buttons=None,
        tap=None,
        **kwargs
    ) -> None:
        super(ThumbnailCard, self).__init__(**kwargs)
        self.title = title
        self.subtitle = subtitle
        self.text = text
        self.images = images
        self.buttons = buttons
        self.tap = tap


class ThumbnailUrl(Model):
    """Thumbnail URL.

    :param url: URL pointing to the thumbnail to use for media content
    :type url: str
    :param alt: HTML alt text to include on this thumbnail image
    :type alt: str
    """

    _attribute_map = {
        "url": {"key": "url", "type": "str"},
        "alt": {"key": "alt", "type": "str"},
    }

    def __init__(self, *, url: str = None, alt: str = None, **kwargs) -> None:
        super(ThumbnailUrl, self).__init__(**kwargs)
        self.url = url
        self.alt = alt


class TokenExchangeInvokeRequest(Model):
    """TokenExchangeInvokeRequest.

    :param id: The id from the OAuthCard.
    :type id: str
    :param connection_name: The connection name.
    :type connection_name: str
    :param token: The user token that can be exchanged.
    :type token: str
    :param properties: Extension data for overflow of properties.
    :type properties: dict[str, object]
    """

    _attribute_map = {
        "id": {"key": "id", "type": "str"},
        "connection_name": {"key": "connectionName", "type": "str"},
        "token": {"key": "token", "type": "str"},
        "properties": {"key": "properties", "type": "{object}"},
    }

    def __init__(
        self,
        *,
        id: str = None,
        connection_name: str = None,
        token: str = None,
        properties=None,
        **kwargs
    ) -> None:
        super(TokenExchangeInvokeRequest, self).__init__(**kwargs)
        self.id = id
        self.connection_name = connection_name
        self.token = token
        self.properties = properties


class TokenExchangeInvokeResponse(Model):
    """TokenExchangeInvokeResponse.

    :param id: The id from the OAuthCard.
    :type id: str
    :param connection_name: The connection name.
    :type connection_name: str
    :param failure_detail: The details of why the token exchange failed.
    :type failure_detail: str
    :param properties: Extension data for overflow of properties.
    :type properties: dict[str, object]
    """

    _attribute_map = {
        "id": {"key": "id", "type": "str"},
        "connection_name": {"key": "connectionName", "type": "str"},
        "failure_detail": {"key": "failureDetail", "type": "str"},
        "properties": {"key": "properties", "type": "{object}"},
    }

    def __init__(
        self,
        *,
        id: str = None,
        connection_name: str = None,
        failure_detail: str = None,
        properties=None,
        **kwargs
    ) -> None:
        super(TokenExchangeInvokeResponse, self).__init__(**kwargs)
        self.id = id
        self.connection_name = connection_name
        self.failure_detail = failure_detail
        self.properties = properties


class TokenExchangeState(Model):
    """TokenExchangeState

    :param connection_name: The connection name that was used.
    :type connection_name: str
    :param conversation: Gets or sets a reference to the conversation.
    :type conversation: ~botframework.connector.models.ConversationReference
    :param relates_to: Gets or sets a reference to a related parent conversation for this token exchange.
    :type relates_to: ~botframework.connector.models.ConversationReference
    :param bot_ur: The URL of the bot messaging endpoint.
    :type bot_ur: str
    :param ms_app_id: The bot's registered application ID.
    :type ms_app_id: str
    """

    _attribute_map = {
        "connection_name": {"key": "connectionName", "type": "str"},
        "conversation": {"key": "conversation", "type": "ConversationReference"},
        "relates_to": {"key": "relatesTo", "type": "ConversationReference"},
        "bot_url": {"key": "connectionName", "type": "str"},
        "ms_app_id": {"key": "msAppId", "type": "str"},
    }

    def __init__(
        self,
        *,
        connection_name: str = None,
        conversation=None,
        relates_to=None,
        bot_url: str = None,
        ms_app_id: str = None,
        **kwargs
    ) -> None:
        super(TokenExchangeState, self).__init__(**kwargs)
        self.connection_name = connection_name
        self.conversation = conversation
        self.relates_to = relates_to
        self.bot_url = bot_url
        self.ms_app_id = ms_app_id


class TokenRequest(Model):
    """A request to receive a user token.

    :param provider: The provider to request a user token from
    :type provider: str
    :param settings: A collection of settings for the specific provider for
     this request
    :type settings: dict[str, object]
    """

    _attribute_map = {
        "provider": {"key": "provider", "type": "str"},
        "settings": {"key": "settings", "type": "{object}"},
    }

    def __init__(self, *, provider: str = None, settings=None, **kwargs) -> None:
        super(TokenRequest, self).__init__(**kwargs)
        self.provider = provider
        self.settings = settings


class TokenResponse(Model):
    """A response that includes a user token.

    :param connection_name: The connection name
    :type connection_name: str
    :param token: The user token
    :type token: str
    :param expiration: Expiration for the token, in ISO 8601 format (e.g.
     "2007-04-05T14:30Z")
    :type expiration: str
    :param channel_id: The channelId of the TokenResponse
    :type channel_id: str
    """

    _attribute_map = {
        "connection_name": {"key": "connectionName", "type": "str"},
        "token": {"key": "token", "type": "str"},
        "expiration": {"key": "expiration", "type": "str"},
        "channel_id": {"key": "channelId", "type": "str"},
    }

    def __init__(
        self,
        *,
        connection_name: str = None,
        token: str = None,
        expiration: str = None,
        channel_id: str = None,
        **kwargs
    ) -> None:
        super(TokenResponse, self).__init__(**kwargs)
        self.connection_name = connection_name
        self.token = token
        self.expiration = expiration
        self.channel_id = channel_id


class Transcript(Model):
    """Transcript.

    :param activities: A collection of Activities that conforms to the
     Transcript schema.
    :type activities: list[~botframework.connector.models.Activity]
    """

    _attribute_map = {"activities": {"key": "activities", "type": "[Activity]"}}

    def __init__(self, *, activities=None, **kwargs) -> None:
        super(Transcript, self).__init__(**kwargs)
        self.activities = activities


class VideoCard(Model):
    """Video card.

    :param title: Title of this card
    :type title: str
    :param subtitle: Subtitle of this card
    :type subtitle: str
    :param text: Text of this card
    :type text: str
    :param image: Thumbnail placeholder
    :type image: ~botframework.connector.models.ThumbnailUrl
    :param media: Media URLs for this card. When this field contains more than
     one URL, each URL is an alternative format of the same content.
    :type media: list[~botframework.connector.models.MediaUrl]
    :param buttons: Actions on this card
    :type buttons: list[~botframework.connector.models.CardAction]
    :param shareable: This content may be shared with others (default:true)
    :type shareable: bool
    :param autoloop: Should the client loop playback at end of content
     (default:true)
    :type autoloop: bool
    :param autostart: Should the client automatically start playback of media
     in this card (default:true)
    :type autostart: bool
    :param aspect: Aspect ratio of thumbnail/media placeholder. Allowed values
     are "16:9" and "4:3"
    :type aspect: str
    :param duration: Describes the length of the media content without
     requiring a receiver to open the content. Formatted as an ISO 8601
     Duration field.
    :type duration: str
    :param value: Supplementary parameter for this card
    :type value: object
    """

    _attribute_map = {
        "title": {"key": "title", "type": "str"},
        "subtitle": {"key": "subtitle", "type": "str"},
        "text": {"key": "text", "type": "str"},
        "image": {"key": "image", "type": "ThumbnailUrl"},
        "media": {"key": "media", "type": "[MediaUrl]"},
        "buttons": {"key": "buttons", "type": "[CardAction]"},
        "shareable": {"key": "shareable", "type": "bool"},
        "autoloop": {"key": "autoloop", "type": "bool"},
        "autostart": {"key": "autostart", "type": "bool"},
        "aspect": {"key": "aspect", "type": "str"},
        "duration": {"key": "duration", "type": "str"},
        "value": {"key": "value", "type": "object"},
    }

    def __init__(
        self,
        *,
        title: str = None,
        subtitle: str = None,
        text: str = None,
        image=None,
        media=None,
        buttons=None,
        shareable: bool = None,
        autoloop: bool = None,
        autostart: bool = None,
        aspect: str = None,
        duration: str = None,
        value=None,
        **kwargs
    ) -> None:
        super(VideoCard, self).__init__(**kwargs)
        self.title = title
        self.subtitle = subtitle
        self.text = text
        self.image = image
        self.media = media
        self.buttons = buttons
        self.shareable = shareable
        self.autoloop = autoloop
        self.autostart = autostart
        self.aspect = aspect
        self.duration = duration
        self.value = value


class AdaptiveCardInvokeAction(Model):
    """AdaptiveCardInvokeAction.

    Defines the structure that arrives in the Activity.Value.Action for Invoke activity with
    name of 'adaptiveCard/action'.

    :param type: The Type of this Adaptive Card Invoke Action.
    :type type: str
    :param id: The Id of this Adaptive Card Invoke Action.
    :type id: str
    :param verb: The Verb of this Adaptive Card Invoke Action.
    :type verb: str
    :param data: The data of this Adaptive Card Invoke Action.
    :type data: dict[str, object]
    """

    _attribute_map = {
        "type": {"key": "type", "type": "str"},
        "id": {"key": "id", "type": "str"},
        "verb": {"key": "verb", "type": "str"},
        "data": {"key": "data", "type": "{object}"},
    }

    def __init__(
        self, *, type: str = None, id: str = None, verb: str = None, data=None, **kwargs
    ) -> None:
        super(AdaptiveCardInvokeAction, self).__init__(**kwargs)
        self.type = type
        self.id = id
        self.verb = verb
        self.data = data


class AdaptiveCardInvokeResponse(Model):
    """AdaptiveCardInvokeResponse.

    Defines the structure that is returned as the result of an Invoke activity with Name of 'adaptiveCard/action'.

    :param status_code: The Card Action Response StatusCode.
    :type status_code: int
    :param type: The type of this Card Action Response.
    :type type: str
    :param value: The JSON response object.
    :type value: dict[str, object]
    """

    _attribute_map = {
        "status_code": {"key": "statusCode", "type": "int"},
        "type": {"key": "type", "type": "str"},
        "value": {"key": "value", "type": "{object}"},
    }

    def __init__(
        self, *, status_code: int = None, type: str = None, value=None, **kwargs
    ) -> None:
        super(AdaptiveCardInvokeResponse, self).__init__(**kwargs)
        self.status_code = status_code
        self.type = type
        self.value = value


class AdaptiveCardInvokeValue(Model):
    """AdaptiveCardInvokeResponse.

    Defines the structure that arrives in the Activity.Value for Invoke activity with Name of 'adaptiveCard/action'.

    :param action: The action of this adaptive card invoke action value.
    :type action: :class:`botframework.schema.models.AdaptiveCardInvokeAction`
    :param authentication: The TokenExchangeInvokeRequest for this adaptive card invoke action value.
    :type authentication: :class:`botframework.schema.models.TokenExchangeInvokeRequest`
    :param state: The 'state' or magic code for an OAuth flow.
    :type state: str
    """

    _attribute_map = {
        "action": {"key": "action", "type": "{object}"},
        "authentication": {"key": "authentication", "type": "{object}"},
        "state": {"key": "state", "type": "str"},
    }

    def __init__(
        self, *, action=None, authentication=None, state: str = None, **kwargs
    ) -> None:
        super(AdaptiveCardInvokeValue, self).__init__(**kwargs)
        self.action = action
        self.authentication = authentication
        self.state = state
