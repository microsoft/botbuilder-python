# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List
from msrest.serialization import Model
from botbuilder.schema import (
    Attachment,
    ChannelAccount,
    PagedMembersResult,
    ConversationAccount,
)


class TabEntityContext(Model):
    """
    Current TabRequest entity context, or 'tabEntityId'.

    :param tab_entity_id: Gets or sets the entity id of the tab.
    :type tab_entity_id: str
    """

    _attribute_map = {
        "tab_entity_id": {"key": "tabEntityId", "type": "str"},
    }

    def __init__(self, *, tab_entity_id=None, **kwargs) -> None:
        super(TabEntityContext, self).__init__(**kwargs)
        self.tab_entity_id = tab_entity_id
        self._custom_init()

    def _custom_init(self):
        return


class TaskModuleRequest(Model):
    """Task module invoke request value payload.

    :param data: User input data. Free payload with key-value pairs.
    :type data: object
    :param context: Current user context, i.e., the current theme
    :type context:
     ~botframework.connector.teams.models.TaskModuleRequestContext
    :param tab_entity_context: Gets or sets current tab request context.
    :type tab_entity_context:
     ~botframework.connector.teams.models.TabEntityContext
    """

    _attribute_map = {
        "data": {"key": "data", "type": "object"},
        "context": {"key": "context", "type": "TaskModuleRequestContext"},
        "tab_entity_context": {"key": "tabContext", "type": "TabEntityContext"},
    }

    def __init__(
        self, *, data=None, context=None, tab_entity_context=None, **kwargs
    ) -> None:
        super(TaskModuleRequest, self).__init__(**kwargs)
        self.data = data
        self.context = context
        self.tab_entity_context = tab_entity_context


class AppBasedLinkQuery(Model):
    """Invoke request body type for app-based link query.

    :param url: Url queried by user
    :type url: str
    :param state: The magic code for OAuth Flow
    :type state: str
    """

    _attribute_map = {
        "url": {"key": "url", "type": "str"},
        "state": {"key": "state", "type": "str"},
    }

    def __init__(self, *, url: str = None, state: str = None, **kwargs) -> None:
        super(AppBasedLinkQuery, self).__init__(**kwargs)
        self.url = url
        self.state = state


class ChannelInfo(Model):
    """A channel info object which describes the channel.

    :param id: Unique identifier representing a channel
    :type id: str
    :param name: Name of the channel
    :type name: str
    """

    _attribute_map = {
        "id": {"key": "id", "type": "str"},
        "name": {"key": "name", "type": "str"},
    }

    def __init__(self, *, id: str = None, name: str = None, **kwargs) -> None:
        super(ChannelInfo, self).__init__(**kwargs)
        self.id = id
        self.name = name


class CacheInfo(Model):
    """A cache info object which notifies Teams how long an object should be cached for.

    :param cache_type: Type of Cache Info
    :type cache_type: str
    :param cache_duration: Duration of the Cached Info.
    :type cache_duration: int
    """

    _attribute_map = {
        "cache_type": {"key": "cacheType", "type": "str"},
        "cache_duration": {"key": "cacheDuration", "type": "int"},
    }

    def __init__(
        self, *, cache_type: str = None, cache_duration: int = None, **kwargs
    ) -> None:
        super(CacheInfo, self).__init__(**kwargs)
        self.cache_type = cache_type
        self.cache_duration = cache_duration


class ConversationList(Model):
    """List of channels under a team.

    :param conversations:
    :type conversations:
     list[~botframework.connector.teams.models.ChannelInfo]
    """

    _attribute_map = {
        "conversations": {"key": "conversations", "type": "[ChannelInfo]"},
    }

    def __init__(self, *, conversations=None, **kwargs) -> None:
        super(ConversationList, self).__init__(**kwargs)
        self.conversations = conversations


class FileConsentCard(Model):
    """File consent card attachment.

    :param description: File description.
    :type description: str
    :param size_in_bytes: Size of the file to be uploaded in Bytes.
    :type size_in_bytes: long
    :param accept_context: Context sent back to the Bot if user consented to
     upload. This is free flow schema and is sent back in Value field of
     Activity.
    :type accept_context: object
    :param decline_context: Context sent back to the Bot if user declined.
     This is free flow schema and is sent back in Value field of Activity.
    :type decline_context: object
    """

    _attribute_map = {
        "description": {"key": "description", "type": "str"},
        "size_in_bytes": {"key": "sizeInBytes", "type": "long"},
        "accept_context": {"key": "acceptContext", "type": "object"},
        "decline_context": {"key": "declineContext", "type": "object"},
    }

    def __init__(
        self,
        *,
        description: str = None,
        size_in_bytes: int = None,
        accept_context=None,
        decline_context=None,
        **kwargs
    ) -> None:
        super(FileConsentCard, self).__init__(**kwargs)
        self.description = description
        self.size_in_bytes = size_in_bytes
        self.accept_context = accept_context
        self.decline_context = decline_context


class FileConsentCardResponse(Model):
    """Represents the value of the invoke activity sent when the user acts on a
    file consent card.

    :param action: The action the user took. Possible values include:
     'accept', 'decline'
    :type action: str
    :param context: The context associated with the action.
    :type context: object
    :param upload_info: If the user accepted the file, contains information
     about the file to be uploaded.
    :type upload_info: ~botframework.connector.teams.models.FileUploadInfo
    """

    _attribute_map = {
        "action": {"key": "action", "type": "str"},
        "context": {"key": "context", "type": "object"},
        "upload_info": {"key": "uploadInfo", "type": "FileUploadInfo"},
    }

    def __init__(
        self, *, action=None, context=None, upload_info=None, **kwargs
    ) -> None:
        super(FileConsentCardResponse, self).__init__(**kwargs)
        self.action = action
        self.context = context
        self.upload_info = upload_info


class FileDownloadInfo(Model):
    """File download info attachment.

    :param download_url: File download url.
    :type download_url: str
    :param unique_id: Unique Id for the file.
    :type unique_id: str
    :param file_type: Type of file.
    :type file_type: str
    :param etag: ETag for the file.
    :type etag: object
    """

    _attribute_map = {
        "download_url": {"key": "downloadUrl", "type": "str"},
        "unique_id": {"key": "uniqueId", "type": "str"},
        "file_type": {"key": "fileType", "type": "str"},
        "etag": {"key": "etag", "type": "object"},
    }

    def __init__(
        self,
        *,
        download_url: str = None,
        unique_id: str = None,
        file_type: str = None,
        etag=None,
        **kwargs
    ) -> None:
        super(FileDownloadInfo, self).__init__(**kwargs)
        self.download_url = download_url
        self.unique_id = unique_id
        self.file_type = file_type
        self.etag = etag


class FileInfoCard(Model):
    """File info card.

    :param unique_id: Unique Id for the file.
    :type unique_id: str
    :param file_type: Type of file.
    :type file_type: str
    :param etag: ETag for the file.
    :type etag: object
    """

    _attribute_map = {
        "unique_id": {"key": "uniqueId", "type": "str"},
        "file_type": {"key": "fileType", "type": "str"},
        "etag": {"key": "etag", "type": "object"},
    }

    def __init__(
        self, *, unique_id: str = None, file_type: str = None, etag=None, **kwargs
    ) -> None:
        super(FileInfoCard, self).__init__(**kwargs)
        self.unique_id = unique_id
        self.file_type = file_type
        self.etag = etag


class FileUploadInfo(Model):
    """Information about the file to be uploaded.

    :param name: Name of the file.
    :type name: str
    :param upload_url: URL to an upload session that the bot can use to set
     the file contents.
    :type upload_url: str
    :param content_url: URL to file.
    :type content_url: str
    :param unique_id: ID that uniquely identifies the file.
    :type unique_id: str
    :param file_type: Type of the file.
    :type file_type: str
    """

    _attribute_map = {
        "name": {"key": "name", "type": "str"},
        "upload_url": {"key": "uploadUrl", "type": "str"},
        "content_url": {"key": "contentUrl", "type": "str"},
        "unique_id": {"key": "uniqueId", "type": "str"},
        "file_type": {"key": "fileType", "type": "str"},
    }

    def __init__(
        self,
        *,
        name: str = None,
        upload_url: str = None,
        content_url: str = None,
        unique_id: str = None,
        file_type: str = None,
        **kwargs
    ) -> None:
        super(FileUploadInfo, self).__init__(**kwargs)
        self.name = name
        self.upload_url = upload_url
        self.content_url = content_url
        self.unique_id = unique_id
        self.file_type = file_type


class MessageActionsPayloadApp(Model):
    """Represents an application entity.

    :param application_identity_type: The type of application. Possible values
     include: 'aadApplication', 'bot', 'tenantBot', 'office365Connector',
     'webhook'
    :type application_identity_type: str or
     ~botframework.connector.teams.models.enum
    :param id: The id of the application.
    :type id: str
    :param display_name: The plaintext display name of the application.
    :type display_name: str
    """

    _attribute_map = {
        "application_identity_type": {"key": "applicationIdentityType", "type": "str"},
        "id": {"key": "id", "type": "str"},
        "display_name": {"key": "displayName", "type": "str"},
    }

    def __init__(
        self,
        *,
        application_identity_type=None,
        id: str = None,
        display_name: str = None,
        **kwargs
    ) -> None:
        super(MessageActionsPayloadApp, self).__init__(**kwargs)
        self.application_identity_type = application_identity_type
        self.id = id
        self.display_name = display_name


class MessageActionsPayloadAttachment(Model):
    """Represents the attachment in a message.

    :param id: The id of the attachment.
    :type id: str
    :param content_type: The type of the attachment.
    :type content_type: str
    :param content_url: The url of the attachment, in case of a external link.
    :type content_url: str
    :param content: The content of the attachment, in case of a code snippet,
     email, or file.
    :type content: object
    :param name: The plaintext display name of the attachment.
    :type name: str
    :param thumbnail_url: The url of a thumbnail image that might be embedded
     in the attachment, in case of a card.
    :type thumbnail_url: str
    """

    _attribute_map = {
        "id": {"key": "id", "type": "str"},
        "content_type": {"key": "contentType", "type": "str"},
        "content_url": {"key": "contentUrl", "type": "str"},
        "content": {"key": "content", "type": "object"},
        "name": {"key": "name", "type": "str"},
        "thumbnail_url": {"key": "thumbnailUrl", "type": "str"},
    }

    def __init__(
        self,
        *,
        id: str = None,
        content_type: str = None,
        content_url: str = None,
        content=None,
        name: str = None,
        thumbnail_url: str = None,
        **kwargs
    ) -> None:
        super(MessageActionsPayloadAttachment, self).__init__(**kwargs)
        self.id = id
        self.content_type = content_type
        self.content_url = content_url
        self.content = content
        self.name = name
        self.thumbnail_url = thumbnail_url


class MessageActionsPayloadBody(Model):
    """Plaintext/HTML representation of the content of the message.

    :param content_type: Type of the content. Possible values include: 'html',
     'text'
    :type content_type: str
    :param content: The content of the body.
    :type content: str
    """

    _attribute_map = {
        "content_type": {"key": "contentType", "type": "str"},
        "content": {"key": "content", "type": "str"},
    }

    def __init__(self, *, content_type=None, content: str = None, **kwargs) -> None:
        super(MessageActionsPayloadBody, self).__init__(**kwargs)
        self.content_type = content_type
        self.content = content


class MessageActionsPayloadConversation(Model):
    """Represents a team or channel entity.

    :param conversation_identity_type: The type of conversation, whether a
     team or channel. Possible values include: 'team', 'channel'
    :type conversation_identity_type: str or
     ~botframework.connector.teams.models.enum
    :param id: The id of the team or channel.
    :type id: str
    :param display_name: The plaintext display name of the team or channel
     entity.
    :type display_name: str
    """

    _attribute_map = {
        "conversation_identity_type": {
            "key": "conversationIdentityType",
            "type": "str",
        },
        "id": {"key": "id", "type": "str"},
        "display_name": {"key": "displayName", "type": "str"},
    }

    def __init__(
        self,
        *,
        conversation_identity_type=None,
        id: str = None,
        display_name: str = None,
        **kwargs
    ) -> None:
        super(MessageActionsPayloadConversation, self).__init__(**kwargs)
        self.conversation_identity_type = conversation_identity_type
        self.id = id
        self.display_name = display_name


class MessageActionsPayloadFrom(Model):
    """Represents a user, application, or conversation type that either sent or
    was referenced in a message.

    :param user: Represents details of the user.
    :type user: ~botframework.connector.teams.models.MessageActionsPayloadUser
    :param application: Represents details of the app.
    :type application:
     ~botframework.connector.teams.models.MessageActionsPayloadApp
    :param conversation: Represents details of the converesation.
    :type conversation:
     ~botframework.connector.teams.models.MessageActionsPayloadConversation
    """

    _attribute_map = {
        "user": {"key": "user", "type": "MessageActionsPayloadUser"},
        "application": {"key": "application", "type": "MessageActionsPayloadApp"},
        "conversation": {
            "key": "conversation",
            "type": "MessageActionsPayloadConversation",
        },
    }

    def __init__(
        self, *, user=None, application=None, conversation=None, **kwargs
    ) -> None:
        super(MessageActionsPayloadFrom, self).__init__(**kwargs)
        self.user = user
        self.application = application
        self.conversation = conversation


class MessageActionsPayloadMention(Model):
    """Represents the entity that was mentioned in the message.

    :param id: The id of the mentioned entity.
    :type id: int
    :param mention_text: The plaintext display name of the mentioned entity.
    :type mention_text: str
    :param mentioned: Provides more details on the mentioned entity.
    :type mentioned:
     ~botframework.connector.teams.models.MessageActionsPayloadFrom
    """

    _attribute_map = {
        "id": {"key": "id", "type": "int"},
        "mention_text": {"key": "mentionText", "type": "str"},
        "mentioned": {"key": "mentioned", "type": "MessageActionsPayloadFrom"},
    }

    def __init__(
        self, *, id: int = None, mention_text: str = None, mentioned=None, **kwargs
    ) -> None:
        super(MessageActionsPayloadMention, self).__init__(**kwargs)
        self.id = id
        self.mention_text = mention_text
        self.mentioned = mentioned


class MessageActionsPayloadReaction(Model):
    """Represents the reaction of a user to a message.

    :param reaction_type: The type of reaction given to the message. Possible
     values include: 'like', 'heart', 'laugh', 'surprised', 'sad', 'angry'
    :type reaction_type: str
    :param created_date_time: Timestamp of when the user reacted to the
     message.
    :type created_date_time: str
    :param user: The user with which the reaction is associated.
    :type user: ~botframework.connector.teams.models.MessageActionsPayloadFrom
    """

    _attribute_map = {
        "reaction_type": {"key": "reactionType", "type": "str"},
        "created_date_time": {"key": "createdDateTime", "type": "str"},
        "user": {"key": "user", "type": "MessageActionsPayloadFrom"},
    }

    def __init__(
        self, *, reaction_type=None, created_date_time: str = None, user=None, **kwargs
    ) -> None:
        super(MessageActionsPayloadReaction, self).__init__(**kwargs)
        self.reaction_type = reaction_type
        self.created_date_time = created_date_time
        self.user = user


class MessageActionsPayloadUser(Model):
    """Represents a user entity.

    :param user_identity_type: The identity type of the user. Possible values
     include: 'aadUser', 'onPremiseAadUser', 'anonymousGuest', 'federatedUser'
    :type user_identity_type: str
    :param id: The id of the user.
    :type id: str
    :param display_name: The plaintext display name of the user.
    :type display_name: str
    """

    _attribute_map = {
        "user_identity_type": {"key": "userIdentityType", "type": "str"},
        "id": {"key": "id", "type": "str"},
        "display_name": {"key": "displayName", "type": "str"},
    }

    def __init__(
        self,
        *,
        user_identity_type=None,
        id: str = None,
        display_name: str = None,
        **kwargs
    ) -> None:
        super(MessageActionsPayloadUser, self).__init__(**kwargs)
        self.user_identity_type = user_identity_type
        self.id = id
        self.display_name = display_name


class MessageActionsPayload(Model):
    """Represents the individual message within a chat or channel where a message
    actions is taken.

    :param id: Unique id of the message.
    :type id: str
    :param reply_to_id: Id of the parent/root message of the thread.
    :type reply_to_id: str
    :param message_type: Type of message - automatically set to message.
     Possible values include: 'message'
    :type message_type: str
    :param created_date_time: Timestamp of when the message was created.
    :type created_date_time: str
    :param last_modified_date_time: Timestamp of when the message was edited
     or updated.
    :type last_modified_date_time: str
    :param deleted: Indicates whether a message has been soft deleted.
    :type deleted: bool
    :param subject: Subject line of the message.
    :type subject: str
    :param summary: Summary text of the message that could be used for
     notifications.
    :type summary: str
    :param importance: The importance of the message. Possible values include:
     'normal', 'high', 'urgent'
    :type importance: str
    :param locale: Locale of the message set by the client.
    :type locale: str
    :param link_to_message: Link back to the message.
    :type link_to_message: str
    :param from_property: Sender of the message.
    :type from_property:
     ~botframework.connector.teams.models.MessageActionsPayloadFrom
    :param body: Plaintext/HTML representation of the content of the message.
    :type body: ~botframework.connector.teams.models.MessageActionsPayloadBody
    :param attachment_layout: How the attachment(s) are displayed in the
     message.
    :type attachment_layout: str
    :param attachments: Attachments in the message - card, image, file, etc.
    :type attachments:
     list[~botframework.connector.teams.models.MessageActionsPayloadAttachment]
    :param mentions: List of entities mentioned in the message.
    :type mentions:
     list[~botframework.connector.teams.models.MessageActionsPayloadMention]
    :param reactions: Reactions for the message.
    :type reactions:
     list[~botframework.connector.teams.models.MessageActionsPayloadReaction]
    """

    _attribute_map = {
        "id": {"key": "id", "type": "str"},
        "reply_to_id": {"key": "replyToId", "type": "str"},
        "message_type": {"key": "messageType", "type": "str"},
        "created_date_time": {"key": "createdDateTime", "type": "str"},
        "last_modified_date_time": {"key": "lastModifiedDateTime", "type": "str"},
        "deleted": {"key": "deleted", "type": "bool"},
        "subject": {"key": "subject", "type": "str"},
        "summary": {"key": "summary", "type": "str"},
        "importance": {"key": "importance", "type": "str"},
        "locale": {"key": "locale", "type": "str"},
        "link_to_message": {"key": "linkToMessage", "type": "str"},
        "from_property": {"key": "from", "type": "MessageActionsPayloadFrom"},
        "body": {"key": "body", "type": "MessageActionsPayloadBody"},
        "attachment_layout": {"key": "attachmentLayout", "type": "str"},
        "attachments": {
            "key": "attachments",
            "type": "[MessageActionsPayloadAttachment]",
        },
        "mentions": {"key": "mentions", "type": "[MessageActionsPayloadMention]"},
        "reactions": {"key": "reactions", "type": "[MessageActionsPayloadReaction]"},
    }

    def __init__(
        self,
        *,
        id: str = None,
        reply_to_id: str = None,
        message_type=None,
        created_date_time: str = None,
        last_modified_date_time: str = None,
        deleted: bool = None,
        subject: str = None,
        summary: str = None,
        importance=None,
        locale: str = None,
        link_to_message: str = None,
        from_property=None,
        body=None,
        attachment_layout: str = None,
        attachments=None,
        mentions=None,
        reactions=None,
        **kwargs
    ) -> None:
        super(MessageActionsPayload, self).__init__(**kwargs)
        self.id = id
        self.reply_to_id = reply_to_id
        self.message_type = message_type
        self.created_date_time = created_date_time
        self.last_modified_date_time = last_modified_date_time
        self.deleted = deleted
        self.subject = subject
        self.summary = summary
        self.importance = importance
        self.locale = locale
        self.link_to_message = link_to_message
        self.from_property = from_property
        self.body = body
        self.attachment_layout = attachment_layout
        self.attachments = attachments
        self.mentions = mentions
        self.reactions = reactions


class MessagingExtensionAction(TaskModuleRequest):
    """Messaging extension action.

    :param data: User input data. Free payload with key-value pairs.
    :type data: object
    :param context: Current user context, i.e., the current theme
    :type context:
     ~botframework.connector.teams.models.TaskModuleRequestContext
    :param command_id: Id of the command assigned by Bot
    :type command_id: str
    :param command_context: The context from which the command originates.
     Possible values include: 'message', 'compose', 'commandbox'
    :type command_context: str
    :param bot_message_preview_action: Bot message preview action taken by
     user. Possible values include: 'edit', 'send'
    :type bot_message_preview_action: str or
     ~botframework.connector.teams.models.enum
    :param bot_activity_preview:
    :type bot_activity_preview:
     list[~botframework.schema.models.Activity]
    :param message_payload: Message content sent as part of the command
     request.
    :type message_payload:
     ~botframework.connector.teams.models.MessageActionsPayload
    """

    _attribute_map = {
        "data": {"key": "data", "type": "object"},
        "context": {"key": "context", "type": "TaskModuleRequestContext"},
        "command_id": {"key": "commandId", "type": "str"},
        "command_context": {"key": "commandContext", "type": "str"},
        "bot_message_preview_action": {"key": "botMessagePreviewAction", "type": "str"},
        "bot_activity_preview": {"key": "botActivityPreview", "type": "[Activity]"},
        "message_payload": {"key": "messagePayload", "type": "MessageActionsPayload"},
    }

    def __init__(
        self,
        *,
        data=None,
        context=None,
        command_id: str = None,
        command_context=None,
        bot_message_preview_action=None,
        bot_activity_preview=None,
        message_payload=None,
        **kwargs
    ) -> None:
        super(MessagingExtensionAction, self).__init__(
            data=data, context=context, **kwargs
        )
        self.command_id = command_id
        self.command_context = command_context
        self.bot_message_preview_action = bot_message_preview_action
        self.bot_activity_preview = bot_activity_preview
        self.message_payload = message_payload


class MessagingExtensionActionResponse(Model):
    """Response of messaging extension action.

    :param task: The JSON for the Adaptive card to appear in the task module.
    :type task: ~botframework.connector.teams.models.TaskModuleResponseBase
    :param compose_extension:
    :type compose_extension:
     ~botframework.connector.teams.models.MessagingExtensionResult
    :param cache_info: CacheInfo for this MessagingExtensionActionResponse.
    :type cache_info: ~botframework.connector.teams.models.CacheInfo
    """

    _attribute_map = {
        "task": {"key": "task", "type": "TaskModuleResponseBase"},
        "compose_extension": {
            "key": "composeExtension",
            "type": "MessagingExtensionResult",
        },
        "cache_info": {"key": "cacheInfo", "type": "CacheInfo"},
    }

    def __init__(
        self,
        *,
        task=None,
        compose_extension=None,
        cache_info: CacheInfo = None,
        **kwargs
    ) -> None:
        super(MessagingExtensionActionResponse, self).__init__(**kwargs)
        self.task = task
        self.compose_extension = compose_extension
        self.cache_info = cache_info


class MessagingExtensionAttachment(Attachment):
    """Messaging extension attachment.

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
    :param preview:
    :type preview: ~botframework.connector.teams.models.Attachment
    """

    _attribute_map = {
        "content_type": {"key": "contentType", "type": "str"},
        "content_url": {"key": "contentUrl", "type": "str"},
        "content": {"key": "content", "type": "object"},
        "name": {"key": "name", "type": "str"},
        "thumbnail_url": {"key": "thumbnailUrl", "type": "str"},
        "preview": {"key": "preview", "type": "Attachment"},
    }

    def __init__(
        self,
        *,
        content_type: str = None,
        content_url: str = None,
        content=None,
        name: str = None,
        thumbnail_url: str = None,
        preview=None,
        **kwargs
    ) -> None:
        super(MessagingExtensionAttachment, self).__init__(
            content_type=content_type,
            content_url=content_url,
            content=content,
            name=name,
            thumbnail_url=thumbnail_url,
            **kwargs
        )
        self.preview = preview


class MessagingExtensionParameter(Model):
    """Messaging extension query parameters.

    :param name: Name of the parameter
    :type name: str
    :param value: Value of the parameter
    :type value: object
    """

    _attribute_map = {
        "name": {"key": "name", "type": "str"},
        "value": {"key": "value", "type": "object"},
    }

    def __init__(self, *, name: str = None, value=None, **kwargs) -> None:
        super(MessagingExtensionParameter, self).__init__(**kwargs)
        self.name = name
        self.value = value


class MessagingExtensionQuery(Model):
    """Messaging extension query.

    :param command_id: Id of the command assigned by Bot
    :type command_id: str
    :param parameters: Parameters for the query
    :type parameters:
     list[~botframework.connector.teams.models.MessagingExtensionParameter]
    :param query_options:
    :type query_options:
     ~botframework.connector.teams.models.MessagingExtensionQueryOptions
    :param state: State parameter passed back to the bot after
     authentication/configuration flow
    :type state: str
    """

    _attribute_map = {
        "command_id": {"key": "commandId", "type": "str"},
        "parameters": {"key": "parameters", "type": "[MessagingExtensionParameter]"},
        "query_options": {
            "key": "queryOptions",
            "type": "MessagingExtensionQueryOptions",
        },
        "state": {"key": "state", "type": "str"},
    }

    def __init__(
        self,
        *,
        command_id: str = None,
        parameters=None,
        query_options=None,
        state: str = None,
        **kwargs
    ) -> None:
        super(MessagingExtensionQuery, self).__init__(**kwargs)
        self.command_id = command_id
        self.parameters = parameters
        self.query_options = query_options
        self.state = state


class MessagingExtensionQueryOptions(Model):
    """Messaging extension query options.

    :param skip: Number of entities to skip
    :type skip: int
    :param count: Number of entities to fetch
    :type count: int
    """

    _attribute_map = {
        "skip": {"key": "skip", "type": "int"},
        "count": {"key": "count", "type": "int"},
    }

    def __init__(self, *, skip: int = None, count: int = None, **kwargs) -> None:
        super(MessagingExtensionQueryOptions, self).__init__(**kwargs)
        self.skip = skip
        self.count = count


class MessagingExtensionResponse(Model):
    """Messaging extension response.

    :param compose_extension:
    :type compose_extension: ~botframework.connector.teams.models.MessagingExtensionResult
    :param cache_info: CacheInfo for this MessagingExtensionResponse.
    :type cache_info: ~botframework.connector.teams.models.CacheInfo
    """

    _attribute_map = {
        "compose_extension": {
            "key": "composeExtension",
            "type": "MessagingExtensionResult",
        },
        "cache_info": {"key": "cacheInfo", "type": CacheInfo},
    }

    def __init__(self, *, compose_extension=None, cache_info=None, **kwargs) -> None:
        super(MessagingExtensionResponse, self).__init__(**kwargs)
        self.compose_extension = compose_extension
        self.cache_info = cache_info


class MessagingExtensionResult(Model):
    """Messaging extension result.

    :param attachment_layout: Hint for how to deal with multiple attachments.
     Possible values include: 'list', 'grid'
    :type attachment_layout: str
    :param type: The type of the result. Possible values include: 'result',
     'auth', 'config', 'message', 'botMessagePreview'
    :type type: str
    :param attachments: (Only when type is result) Attachments
    :type attachments:
     list[~botframework.connector.teams.models.MessagingExtensionAttachment]
    :param suggested_actions:
    :type suggested_actions:
     ~botframework.connector.teams.models.MessagingExtensionSuggestedAction
    :param text: (Only when type is message) Text
    :type text: str
    :param activity_preview: (Only when type is botMessagePreview) Message
     activity to preview
    :type activity_preview: ~botframework.connector.teams.models.Activity
    """

    _attribute_map = {
        "attachment_layout": {"key": "attachmentLayout", "type": "str"},
        "type": {"key": "type", "type": "str"},
        "attachments": {"key": "attachments", "type": "[MessagingExtensionAttachment]"},
        "suggested_actions": {
            "key": "suggestedActions",
            "type": "MessagingExtensionSuggestedAction",
        },
        "text": {"key": "text", "type": "str"},
        "activity_preview": {"key": "activityPreview", "type": "Activity"},
    }

    def __init__(
        self,
        *,
        attachment_layout=None,
        type=None,
        attachments=None,
        suggested_actions=None,
        text: str = None,
        activity_preview=None,
        **kwargs
    ) -> None:
        super(MessagingExtensionResult, self).__init__(**kwargs)
        self.attachment_layout = attachment_layout
        self.type = type
        self.attachments = attachments
        self.suggested_actions = suggested_actions
        self.text = text
        self.activity_preview = activity_preview


class MessagingExtensionSuggestedAction(Model):
    """Messaging extension Actions (Only when type is auth or config).

    :param actions: Actions
    :type actions: list[~botframework.connector.teams.models.CardAction]
    """

    _attribute_map = {
        "actions": {"key": "actions", "type": "[CardAction]"},
    }

    def __init__(self, *, actions=None, **kwargs) -> None:
        super(MessagingExtensionSuggestedAction, self).__init__(**kwargs)
        self.actions = actions


class NotificationInfo(Model):
    """Specifies if a notification is to be sent for the mentions.

    :param alert: true if notification is to be sent to the user, false
     otherwise.
    :type alert: bool
    """

    _attribute_map = {
        "alert": {"key": "alert", "type": "bool"},
        "alert_in_meeting": {"key": "alertInMeeting", "type": "bool"},
        "external_resource_url": {"key": "externalResourceUrl", "type": "str"},
    }

    def __init__(
        self,
        *,
        alert: bool = None,
        alert_in_meeting: bool = None,
        external_resource_url: str = None,
        **kwargs
    ) -> None:
        super(NotificationInfo, self).__init__(**kwargs)
        self.alert = alert
        self.alert_in_meeting = alert_in_meeting
        self.external_resource_url = external_resource_url


class O365ConnectorCard(Model):
    """O365 connector card.

    :param title: Title of the item
    :type title: str
    :param text: Text for the card
    :type text: str
    :param summary: Summary for the card
    :type summary: str
    :param theme_color: Theme color for the card
    :type theme_color: str
    :param sections: Set of sections for the current card
    :type sections:
     list[~botframework.connector.teams.models.O365ConnectorCardSection]
    :param potential_action: Set of actions for the current card
    :type potential_action:
     list[~botframework.connector.teams.models.O365ConnectorCardActionBase]
    """

    _attribute_map = {
        "title": {"key": "title", "type": "str"},
        "text": {"key": "text", "type": "str"},
        "summary": {"key": "summary", "type": "str"},
        "theme_color": {"key": "themeColor", "type": "str"},
        "sections": {"key": "sections", "type": "[O365ConnectorCardSection]"},
        "potential_action": {
            "key": "potentialAction",
            "type": "[O365ConnectorCardActionBase]",
        },
    }

    def __init__(
        self,
        *,
        title: str = None,
        text: str = None,
        summary: str = None,
        theme_color: str = None,
        sections=None,
        potential_action=None,
        **kwargs
    ) -> None:
        super(O365ConnectorCard, self).__init__(**kwargs)
        self.title = title
        self.text = text
        self.summary = summary
        self.theme_color = theme_color
        self.sections = sections
        self.potential_action = potential_action


class O365ConnectorCardInputBase(Model):
    """O365 connector card input for ActionCard action.

    :param type: Input type name. Possible values include: 'textInput',
     'dateInput', 'multichoiceInput'
    :type type: str
    :param id: Input Id. It must be unique per entire O365 connector card.
    :type id: str
    :param is_required: Define if this input is a required field. Default
     value is false.
    :type is_required: bool
    :param title: Input title that will be shown as the placeholder
    :type title: str
    :param value: Default value for this input field
    :type value: str
    """

    _attribute_map = {
        "type": {"key": "@type", "type": "str"},
        "id": {"key": "id", "type": "str"},
        "is_required": {"key": "isRequired", "type": "bool"},
        "title": {"key": "title", "type": "str"},
        "value": {"key": "value", "type": "str"},
    }

    def __init__(
        self,
        *,
        type=None,
        id: str = None,
        is_required: bool = None,
        title: str = None,
        value: str = None,
        **kwargs
    ) -> None:
        super(O365ConnectorCardInputBase, self).__init__(**kwargs)
        self.type = type
        self.id = id
        self.is_required = is_required
        self.title = title
        self.value = value


class O365ConnectorCardActionBase(Model):
    """O365 connector card action base.

    :param type: Type of the action. Possible values include: 'ViewAction',
     'OpenUri', 'HttpPOST', 'ActionCard'
    :type type: str
    :param name: Name of the action that will be used as button title
    :type name: str
    :param id: Action Id
    :type id: str
    """

    _attribute_map = {
        "type": {"key": "@type", "type": "str"},
        "name": {"key": "name", "type": "str"},
        "id": {"key": "@id", "type": "str"},
    }

    def __init__(
        self, *, type=None, name: str = None, id: str = None, **kwargs
    ) -> None:
        super(O365ConnectorCardActionBase, self).__init__(**kwargs)
        self.type = type
        self.name = name
        self.id = id


class O365ConnectorCardActionCard(O365ConnectorCardActionBase):
    """O365 connector card ActionCard action.

    :param type: Type of the action. Possible values include: 'ViewAction',
     'OpenUri', 'HttpPOST', 'ActionCard'
    :type type: str
    :param name: Name of the action that will be used as button title
    :type name: str
    :param id: Action Id
    :type id: str
    :param inputs: Set of inputs contained in this ActionCard whose each item
     can be in any subtype of O365ConnectorCardInputBase
    :type inputs:
     list[~botframework.connector.teams.models.O365ConnectorCardInputBase]
    :param actions: Set of actions contained in this ActionCard whose each
     item can be in any subtype of O365ConnectorCardActionBase except
     O365ConnectorCardActionCard, as nested ActionCard is forbidden.
    :type actions:
     list[~botframework.connector.teams.models.O365ConnectorCardActionBase]
    """

    _attribute_map = {
        "type": {"key": "@type", "type": "str"},
        "name": {"key": "name", "type": "str"},
        "id": {"key": "@id", "type": "str"},
        "inputs": {"key": "inputs", "type": "[O365ConnectorCardInputBase]"},
        "actions": {"key": "actions", "type": "[O365ConnectorCardActionBase]"},
    }

    def __init__(
        self,
        *,
        type=None,
        name: str = None,
        id: str = None,
        inputs=None,
        actions=None,
        **kwargs
    ) -> None:
        super(O365ConnectorCardActionCard, self).__init__(
            type=type, name=name, id=id, **kwargs
        )
        self.inputs = inputs
        self.actions = actions


class O365ConnectorCardActionQuery(Model):
    """O365 connector card HttpPOST invoke query.

    :param body: The results of body string defined in
     IO365ConnectorCardHttpPOST with substituted input values
    :type body: str
    :param action_id: Action Id associated with the HttpPOST action button
     triggered, defined in O365ConnectorCardActionBase.
    :type action_id: str
    """

    _attribute_map = {
        "body": {"key": "body", "type": "str"},
        "action_id": {"key": "actionId", "type": "str"},
    }

    def __init__(self, *, body: str = None, actionId: str = None, **kwargs) -> None:
        super(O365ConnectorCardActionQuery, self).__init__(**kwargs)
        self.body = body
        # This is how it comes in from Teams
        self.action_id = actionId


class O365ConnectorCardDateInput(O365ConnectorCardInputBase):
    """O365 connector card date input.

    :param type: Input type name. Possible values include: 'textInput',
     'dateInput', 'multichoiceInput'
    :type type: str
    :param id: Input Id. It must be unique per entire O365 connector card.
    :type id: str
    :param is_required: Define if this input is a required field. Default
     value is false.
    :type is_required: bool
    :param title: Input title that will be shown as the placeholder
    :type title: str
    :param value: Default value for this input field
    :type value: str
    :param include_time: Include time input field. Default value  is false
     (date only).
    :type include_time: bool
    """

    _attribute_map = {
        "type": {"key": "@type", "type": "str"},
        "id": {"key": "id", "type": "str"},
        "is_required": {"key": "isRequired", "type": "bool"},
        "title": {"key": "title", "type": "str"},
        "value": {"key": "value", "type": "str"},
        "include_time": {"key": "includeTime", "type": "bool"},
    }

    def __init__(
        self,
        *,
        type=None,
        id: str = None,
        is_required: bool = None,
        title: str = None,
        value: str = None,
        include_time: bool = None,
        **kwargs
    ) -> None:
        super(O365ConnectorCardDateInput, self).__init__(
            type=type,
            id=id,
            is_required=is_required,
            title=title,
            value=value,
            **kwargs
        )
        self.include_time = include_time


class O365ConnectorCardFact(Model):
    """O365 connector card fact.

    :param name: Display name of the fact
    :type name: str
    :param value: Display value for the fact
    :type value: str
    """

    _attribute_map = {
        "name": {"key": "name", "type": "str"},
        "value": {"key": "value", "type": "str"},
    }

    def __init__(self, *, name: str = None, value: str = None, **kwargs) -> None:
        super(O365ConnectorCardFact, self).__init__(**kwargs)
        self.name = name
        self.value = value


class O365ConnectorCardHttpPOST(O365ConnectorCardActionBase):
    """O365 connector card HttpPOST action.

    :param type: Type of the action. Possible values include: 'ViewAction',
     'OpenUri', 'HttpPOST', 'ActionCard'
    :type type: str
    :param name: Name of the action that will be used as button title
    :type name: str
    :param id: Action Id
    :type id: str
    :param body: Content to be posted back to bots via invoke
    :type body: str
    """

    _attribute_map = {
        "type": {"key": "@type", "type": "str"},
        "name": {"key": "name", "type": "str"},
        "id": {"key": "@id", "type": "str"},
        "body": {"key": "body", "type": "str"},
    }

    def __init__(
        self, *, type=None, name: str = None, id: str = None, body: str = None, **kwargs
    ) -> None:
        super(O365ConnectorCardHttpPOST, self).__init__(
            type=type, name=name, id=id, **kwargs
        )
        self.body = body


class O365ConnectorCardImage(Model):
    """O365 connector card image.

    :param image: URL for the image
    :type image: str
    :param title: Alternative text for the image
    :type title: str
    """

    _attribute_map = {
        "image": {"key": "image", "type": "str"},
        "title": {"key": "title", "type": "str"},
    }

    def __init__(self, *, image: str = None, title: str = None, **kwargs) -> None:
        super(O365ConnectorCardImage, self).__init__(**kwargs)
        self.image = image
        self.title = title


class O365ConnectorCardMultichoiceInput(O365ConnectorCardInputBase):
    """O365 connector card multiple choice input.

    :param type: Input type name. Possible values include: 'textInput',
     'dateInput', 'multichoiceInput'
    :type type: str
    :param id: Input Id. It must be unique per entire O365 connector card.
    :type id: str
    :param is_required: Define if this input is a required field. Default
     value is false.
    :type is_required: bool
    :param title: Input title that will be shown as the placeholder
    :type title: str
    :param value: Default value for this input field
    :type value: str
    :param choices: Set of choices whose each item can be in any subtype of
     O365ConnectorCardMultichoiceInputChoice.
    :type choices:
     list[~botframework.connector.teams.models.O365ConnectorCardMultichoiceInputChoice]
    :param style: Choice item rendering style. Default value is 'compact'.
     Possible values include: 'compact', 'expanded'
    :type style: str
    :param is_multi_select: Define if this input field allows multiple
     selections. Default value is false.
    :type is_multi_select: bool
    """

    _attribute_map = {
        "type": {"key": "@type", "type": "str"},
        "id": {"key": "id", "type": "str"},
        "is_required": {"key": "isRequired", "type": "bool"},
        "title": {"key": "title", "type": "str"},
        "value": {"key": "value", "type": "str"},
        "choices": {
            "key": "choices",
            "type": "[O365ConnectorCardMultichoiceInputChoice]",
        },
        "style": {"key": "style", "type": "str"},
        "is_multi_select": {"key": "isMultiSelect", "type": "bool"},
    }

    def __init__(
        self,
        *,
        type=None,
        id: str = None,
        is_required: bool = None,
        title: str = None,
        value: str = None,
        choices=None,
        style=None,
        is_multi_select: bool = None,
        **kwargs
    ) -> None:
        super(O365ConnectorCardMultichoiceInput, self).__init__(
            type=type,
            id=id,
            is_required=is_required,
            title=title,
            value=value,
            **kwargs
        )
        self.choices = choices
        self.style = style
        self.is_multi_select = is_multi_select


class O365ConnectorCardMultichoiceInputChoice(Model):
    """O365O365 connector card multiple choice input item.

    :param display: The text rendered on ActionCard.
    :type display: str
    :param value: The value received as results.
    :type value: str
    """

    _attribute_map = {
        "display": {"key": "display", "type": "str"},
        "value": {"key": "value", "type": "str"},
    }

    def __init__(self, *, display: str = None, value: str = None, **kwargs) -> None:
        super(O365ConnectorCardMultichoiceInputChoice, self).__init__(**kwargs)
        self.display = display
        self.value = value


class O365ConnectorCardOpenUri(O365ConnectorCardActionBase):
    """O365 connector card OpenUri action.

    :param type: Type of the action. Possible values include: 'ViewAction',
     'OpenUri', 'HttpPOST', 'ActionCard'
    :type type: str
    :param name: Name of the action that will be used as button title
    :type name: str
    :param id: Action Id
    :type id: str
    :param targets: Target os / urls
    :type targets:
     list[~botframework.connector.teams.models.O365ConnectorCardOpenUriTarget]
    """

    _attribute_map = {
        "type": {"key": "@type", "type": "str"},
        "name": {"key": "name", "type": "str"},
        "id": {"key": "@id", "type": "str"},
        "targets": {"key": "targets", "type": "[O365ConnectorCardOpenUriTarget]"},
    }

    def __init__(
        self, *, type=None, name: str = None, id: str = None, targets=None, **kwargs
    ) -> None:
        super(O365ConnectorCardOpenUri, self).__init__(
            type=type, name=name, id=id, **kwargs
        )
        self.targets = targets


class O365ConnectorCardOpenUriTarget(Model):
    """O365 connector card OpenUri target.

    :param os: Target operating system. Possible values include: 'default',
     'iOS', 'android', 'windows'
    :type os: str
    :param uri: Target url
    :type uri: str
    """

    _attribute_map = {
        "os": {"key": "os", "type": "str"},
        "uri": {"key": "uri", "type": "str"},
    }

    def __init__(self, *, os=None, uri: str = None, **kwargs) -> None:
        super(O365ConnectorCardOpenUriTarget, self).__init__(**kwargs)
        self.os = os
        self.uri = uri


class O365ConnectorCardSection(Model):
    """O365 connector card section.

    :param title: Title of the section
    :type title: str
    :param text: Text for the section
    :type text: str
    :param activity_title: Activity title
    :type activity_title: str
    :param activity_subtitle: Activity subtitle
    :type activity_subtitle: str
    :param activity_text: Activity text
    :type activity_text: str
    :param activity_image: Activity image
    :type activity_image: str
    :param activity_image_type: Describes how Activity image is rendered.
     Possible values include: 'avatar', 'article'
    :type activity_image_type: str or
     ~botframework.connector.teams.models.enum
    :param markdown: Use markdown for all text contents. Default value is
     true.
    :type markdown: bool
    :param facts: Set of facts for the current section
    :type facts:
     list[~botframework.connector.teams.models.O365ConnectorCardFact]
    :param images: Set of images for the current section
    :type images:
     list[~botframework.connector.teams.models.O365ConnectorCardImage]
    :param potential_action: Set of actions for the current section
    :type potential_action:
     list[~botframework.connector.teams.models.O365ConnectorCardActionBase]
    """

    _attribute_map = {
        "title": {"key": "title", "type": "str"},
        "text": {"key": "text", "type": "str"},
        "activity_title": {"key": "activityTitle", "type": "str"},
        "activity_subtitle": {"key": "activitySubtitle", "type": "str"},
        "activity_text": {"key": "activityText", "type": "str"},
        "activity_image": {"key": "activityImage", "type": "str"},
        "activity_image_type": {"key": "activityImageType", "type": "str"},
        "markdown": {"key": "markdown", "type": "bool"},
        "facts": {"key": "facts", "type": "[O365ConnectorCardFact]"},
        "images": {"key": "images", "type": "[O365ConnectorCardImage]"},
        "potential_action": {
            "key": "potentialAction",
            "type": "[O365ConnectorCardActionBase]",
        },
    }

    def __init__(
        self,
        *,
        title: str = None,
        text: str = None,
        activity_title: str = None,
        activity_subtitle: str = None,
        activity_text: str = None,
        activity_image: str = None,
        activity_image_type=None,
        markdown: bool = None,
        facts=None,
        images=None,
        potential_action=None,
        **kwargs
    ) -> None:
        super(O365ConnectorCardSection, self).__init__(**kwargs)
        self.title = title
        self.text = text
        self.activity_title = activity_title
        self.activity_subtitle = activity_subtitle
        self.activity_text = activity_text
        self.activity_image = activity_image
        self.activity_image_type = activity_image_type
        self.markdown = markdown
        self.facts = facts
        self.images = images
        self.potential_action = potential_action


class O365ConnectorCardTextInput(O365ConnectorCardInputBase):
    """O365 connector card text input.

    :param type: Input type name. Possible values include: 'textInput',
     'dateInput', 'multichoiceInput'
    :type type: str
    :param id: Input Id. It must be unique per entire O365 connector card.
    :type id: str
    :param is_required: Define if this input is a required field. Default
     value is false.
    :type is_required: bool
    :param title: Input title that will be shown as the placeholder
    :type title: str
    :param value: Default value for this input field
    :type value: str
    :param is_multiline: Define if text input is allowed for multiple lines.
     Default value is false.
    :type is_multiline: bool
    :param max_length: Maximum length of text input. Default value is
     unlimited.
    :type max_length: float
    """

    _attribute_map = {
        "type": {"key": "@type", "type": "str"},
        "id": {"key": "id", "type": "str"},
        "is_required": {"key": "isRequired", "type": "bool"},
        "title": {"key": "title", "type": "str"},
        "value": {"key": "value", "type": "str"},
        "is_multiline": {"key": "isMultiline", "type": "bool"},
        "max_length": {"key": "maxLength", "type": "float"},
    }

    def __init__(
        self,
        *,
        type=None,
        id: str = None,
        is_required: bool = None,
        title: str = None,
        value: str = None,
        is_multiline: bool = None,
        max_length: float = None,
        **kwargs
    ) -> None:
        super(O365ConnectorCardTextInput, self).__init__(
            type=type,
            id=id,
            is_required=is_required,
            title=title,
            value=value,
            **kwargs
        )
        self.is_multiline = is_multiline
        self.max_length = max_length


class O365ConnectorCardViewAction(O365ConnectorCardActionBase):
    """O365 connector card ViewAction action.

    :param type: Type of the action. Possible values include: 'ViewAction',
     'OpenUri', 'HttpPOST', 'ActionCard'
    :type type: str
    :param name: Name of the action that will be used as button title
    :type name: str
    :param id: Action Id
    :type id: str
    :param target: Target urls, only the first url effective for card button
    :type target: list[str]
    """

    _attribute_map = {
        "type": {"key": "@type", "type": "str"},
        "name": {"key": "name", "type": "str"},
        "id": {"key": "@id", "type": "str"},
        "target": {"key": "target", "type": "[str]"},
    }

    def __init__(
        self, *, type=None, name: str = None, id: str = None, target=None, **kwargs
    ) -> None:
        super(O365ConnectorCardViewAction, self).__init__(
            type=type, name=name, id=id, **kwargs
        )
        self.target = target


class SigninStateVerificationQuery(Model):
    """Signin state (part of signin action auth flow) verification invoke query.

    :param state:  The state string originally received when the signin web
     flow is finished with a state posted back to client via tab SDK
     microsoftTeams.authentication.notifySuccess(state)
    :type state: str
    """

    _attribute_map = {
        "state": {"key": "state", "type": "str"},
    }

    def __init__(self, *, state: str = None, **kwargs) -> None:
        super(SigninStateVerificationQuery, self).__init__(**kwargs)
        self.state = state


class TaskModuleResponseBase(Model):
    """Base class for Task Module responses.

    :param type: Choice of action options when responding to the task/submit
     message. Possible values include: 'message', 'continue'
    :type type: str
    """

    _attribute_map = {
        "type": {"key": "type", "type": "str"},
    }

    def __init__(self, *, type=None, **kwargs) -> None:
        super(TaskModuleResponseBase, self).__init__(**kwargs)
        self.type = type


class TaskModuleContinueResponse(TaskModuleResponseBase):
    """Task Module Response with continue action.

    :param value: The JSON for the Adaptive card to appear in the task module.
    :type value: ~botframework.connector.teams.models.TaskModuleTaskInfo
    """

    _attribute_map = {
        "type": {"key": "type", "type": "str"},
        "value": {"key": "value", "type": "TaskModuleTaskInfo"},
    }

    def __init__(self, *, value=None, **kwargs) -> None:
        super(TaskModuleContinueResponse, self).__init__(type="continue", **kwargs)
        self.value = value


class TaskModuleMessageResponse(TaskModuleResponseBase):
    """Task Module response with message action.

    :param value: Teams will display the value of value in a popup message
     box.
    :type value: str
    """

    _attribute_map = {
        "type": {"key": "type", "type": "str"},
        "value": {"key": "value", "type": "str"},
    }

    def __init__(self, *, value: str = None, **kwargs) -> None:
        super(TaskModuleMessageResponse, self).__init__(type="message", **kwargs)
        self.value = value


class TaskModuleRequestContext(Model):
    """Current user context, i.e., the current theme.

    :param theme:
    :type theme: str
    """

    _attribute_map = {
        "theme": {"key": "theme", "type": "str"},
    }

    def __init__(self, *, theme: str = None, **kwargs) -> None:
        super(TaskModuleRequestContext, self).__init__(**kwargs)
        self.theme = theme


class TaskModuleResponse(Model):
    """Envelope for Task Module Response.

    :param task: The JSON for the Adaptive card to appear in the task module.
    :type task: ~botframework.connector.teams.models.TaskModuleResponseBase
    :param cache_info: CacheInfo for this TaskModuleResponse.
    :type cache_info: ~botframework.connector.teams.models.CacheInfo
    """

    _attribute_map = {
        "task": {"key": "task", "type": "TaskModuleResponseBase"},
        "cache_info": {"key": "cacheInfo", "type": "CacheInfo"},
    }

    def __init__(self, *, task=None, cache_info=None, **kwargs) -> None:
        super(TaskModuleResponse, self).__init__(**kwargs)
        self.task = task
        self.cache_info = cache_info


class TaskModuleTaskInfo(Model):
    """Metadata for a Task Module.

    :param title: Appears below the app name and to the right of the app icon.
    :type title: str
    :param height: This can be a number, representing the task module's height
     in pixels, or a string, one of: small, medium, large.
    :type height: object
    :param width: This can be a number, representing the task module's width
     in pixels, or a string, one of: small, medium, large.
    :type width: object
    :param url: The URL of what is loaded as an iframe inside the task module.
     One of url or card is required.
    :type url: str
    :param card: The JSON for the Adaptive card to appear in the task module.
    :type card: ~botframework.connector.teams.models.Attachment
    :param fallback_url: If a client does not support the task module feature,
     this URL is opened in a browser tab.
    :type fallback_url: str
    :param completion_bot_id: If a client does not support the task module
     feature, this URL is opened in a browser tab.
    :type completion_bot_id: str
    """

    _attribute_map = {
        "title": {"key": "title", "type": "str"},
        "height": {"key": "height", "type": "object"},
        "width": {"key": "width", "type": "object"},
        "url": {"key": "url", "type": "str"},
        "card": {"key": "card", "type": "Attachment"},
        "fallback_url": {"key": "fallbackUrl", "type": "str"},
        "completion_bot_id": {"key": "completionBotId", "type": "str"},
    }

    def __init__(
        self,
        *,
        title: str = None,
        height=None,
        width=None,
        url: str = None,
        card=None,
        fallback_url: str = None,
        completion_bot_id: str = None,
        **kwargs
    ) -> None:
        super(TaskModuleTaskInfo, self).__init__(**kwargs)
        self.title = title
        self.height = height
        self.width = width
        self.url = url
        self.card = card
        self.fallback_url = fallback_url
        self.completion_bot_id = completion_bot_id


class TeamDetails(Model):
    """Details related to a team.

    :param id: Unique identifier representing a team
    :type id: str
    :param name: Name of team.
    :type name: str
    :param aad_group_id: Azure Active Directory (AAD) Group Id for the team.
    :type aad_group_id: str
    :param channel_count: The count of channels in the team.
    :type channel_count: int
    :param member_count: The count of members in the team.
    :type member_count: int
    """

    _attribute_map = {
        "id": {"key": "id", "type": "str"},
        "name": {"key": "name", "type": "str"},
        "aad_group_id": {"key": "aadGroupId", "type": "str"},
        "channel_count": {"key": "channelCount", "type": "int"},
        "member_count": {"key": "memberCount", "type": "int"},
    }

    def __init__(
        self,
        *,
        id: str = None,
        name: str = None,
        aad_group_id: str = None,
        member_count: int = None,
        channel_count: int = None,
        **kwargs
    ) -> None:
        super(TeamDetails, self).__init__(**kwargs)
        self.id = id
        self.name = name
        self.aad_group_id = aad_group_id
        self.channel_count = channel_count
        self.member_count = member_count


class TeamInfo(Model):
    """Describes a team.

    :param id: Unique identifier representing a team
    :type id: str
    :param name: Name of team.
    :type name: str
    :param name: Azure AD Teams group ID.
    :type name: str
    """

    _attribute_map = {
        "id": {"key": "id", "type": "str"},
        "name": {"key": "name", "type": "str"},
        "aad_group_id": {"key": "aadGroupId", "type": "str"},
    }

    def __init__(
        self, *, id: str = None, name: str = None, aad_group_id: str = None, **kwargs
    ) -> None:
        super(TeamInfo, self).__init__(**kwargs)
        self.id = id
        self.name = name
        self.aad_group_id = aad_group_id


class TeamsChannelAccount(ChannelAccount):
    """Teams channel account detailing user Azure Active Directory details.

    :param id: Channel id for the user or bot on this channel (Example:
     joe@smith.com, or @joesmith or 123456)
    :type id: str
    :param name: Display friendly name
    :type name: str
    :param given_name: Given name part of the user name.
    :type given_name: str
    :param surname: Surname part of the user name.
    :type surname: str
    :param email: Email Id of the user.
    :type email: str
    :param user_principal_name: Unique user principal name.
    :type user_principal_name: str
    :param tenant_id: Tenant Id of the user.
    :type tenant_id: str
    :param user_role: User Role of the user.
    :type user_role: str
    """

    _attribute_map = {
        "id": {"key": "id", "type": "str"},
        "name": {"key": "name", "type": "str"},
        "given_name": {"key": "givenName", "type": "str"},
        "surname": {"key": "surname", "type": "str"},
        "email": {"key": "email", "type": "str"},
        "user_principal_name": {"key": "userPrincipalName", "type": "str"},
        "aad_object_id": {"key": "aadObjectId", "type": "str"},
        "tenant_id": {"key": "tenantId", "type": "str"},
        "user_role": {"key": "userRole", "type": "str"},
    }

    def __init__(
        self,
        *,
        id: str = None,
        name: str = None,
        given_name: str = None,
        surname: str = None,
        email: str = None,
        user_principal_name: str = None,
        tenant_id: str = None,
        user_role: str = None,
        **kwargs
    ) -> None:
        super(TeamsChannelAccount, self).__init__(id=id, name=name, **kwargs)
        self.given_name = given_name
        self.surname = surname
        self.email = email
        self.user_principal_name = user_principal_name
        self.tenant_id = tenant_id
        self.user_role = user_role


class TeamsPagedMembersResult(PagedMembersResult):
    """Page of members for Teams.

    :param continuation_token: Paging token
    :type continuation_token: str
    :param members: The Teams Channel Accounts.
    :type members: list[~botframework.connector.models.TeamsChannelAccount]
    """

    _attribute_map = {
        "continuation_token": {"key": "continuationToken", "type": "str"},
        "members": {"key": "members", "type": "[TeamsChannelAccount]"},
    }

    def __init__(
        self,
        *,
        continuation_token: str = None,
        members: List[TeamsChannelAccount] = None,
        **kwargs
    ) -> None:
        super(TeamsPagedMembersResult, self).__init__(
            continuation_token=continuation_token, members=members, **kwargs
        )
        self.continuation_token = continuation_token
        self.members = members


class TeamsChannelData(Model):
    """Channel data specific to messages received in Microsoft Teams.

    :param channel: Information about the channel in which the message was
     sent
    :type channel: ~botframework.connector.teams.models.ChannelInfo
    :param event_type: Type of event.
    :type event_type: str
    :param team: Information about the team in which the message was sent
    :type team: ~botframework.connector.teams.models.TeamInfo
    :param notification: Notification settings for the message
    :type notification: ~botframework.connector.teams.models.NotificationInfo
    :param tenant: Information about the tenant in which the message was sent
    :type tenant: ~botframework.connector.teams.models.TenantInfo
    :param meeting: Information about the meeting in which the message was sent
    :type meeting: ~botframework.connector.teams.models.TeamsMeetingInfo
    """

    _attribute_map = {
        "channel": {"key": "channel", "type": "ChannelInfo"},
        "event_type": {"key": "eventType", "type": "str"},
        "team": {"key": "team", "type": "TeamInfo"},
        "notification": {"key": "notification", "type": "NotificationInfo"},
        "tenant": {"key": "tenant", "type": "TenantInfo"},
        "meeting": {"key": "meeting", "type": "TeamsMeetingInfo"},
    }

    def __init__(
        self,
        *,
        channel=None,
        event_type: str = None,
        team=None,
        notification=None,
        tenant=None,
        meeting=None,
        **kwargs
    ) -> None:
        super(TeamsChannelData, self).__init__(**kwargs)
        self.channel = channel
        # doing camel case here since that's how the data comes in
        self.event_type = event_type
        self.team = team
        self.notification = notification
        self.tenant = tenant
        self.meeting = meeting


class TenantInfo(Model):
    """Describes a tenant.

    :param id: Unique identifier representing a tenant
    :type id: str
    """

    _attribute_map = {
        "id": {"key": "id", "type": "str"},
    }

    def __init__(self, *, id: str = None, **kwargs) -> None:
        super(TenantInfo, self).__init__(**kwargs)
        self.id = id


class TeamsMeetingInfo(Model):
    """Describes a Teams Meeting.

    :param id: Unique identifier representing a meeting
    :type id: str
    """

    _attribute_map = {
        "id": {"key": "id", "type": "str"},
    }

    def __init__(self, *, id: str = None, **kwargs) -> None:
        super(TeamsMeetingInfo, self).__init__(**kwargs)
        self.id = id


class MeetingParticipantInfo(Model):
    """Teams meeting participant details.

    :param role: Role of the participant in the current meeting.
    :type role: str
    :param in_meeting: True, if the participant is in the meeting.
    :type in_meeting: bool
    """

    _attribute_map = {
        "role": {"key": "role", "type": "str"},
        "in_meeting": {"key": "inMeeting", "type": "bool"},
    }

    def __init__(self, *, role: str = None, in_meeting: bool = None, **kwargs) -> None:
        super(MeetingParticipantInfo, self).__init__(**kwargs)
        self.role = role
        self.in_meeting = in_meeting


class TeamsMeetingParticipant(Model):
    """Teams participant channel account detailing user Azure Active Directory and meeting participant details.

    :param user: Teams Channel Account information for this meeting participant
    :type user: TeamsChannelAccount
    :param meeting: >Information specific to this participant in the specific meeting.
    :type meeting: MeetingParticipantInfo
    :param conversation: Conversation Account for the meeting.
    :type conversation: ConversationAccount
    """

    _attribute_map = {
        "user": {"key": "user", "type": "TeamsChannelAccount"},
        "meeting": {"key": "meeting", "type": "MeetingParticipantInfo"},
        "conversation": {"key": "conversation", "type": "ConversationAccount"},
    }

    def __init__(
        self,
        *,
        user: TeamsChannelAccount = None,
        meeting: MeetingParticipantInfo = None,
        conversation: ConversationAccount = None,
        **kwargs
    ) -> None:
        super(TeamsMeetingParticipant, self).__init__(**kwargs)
        self.user = user
        self.meeting = meeting
        self.conversation = conversation


class TabContext(Model):
    """
    Current tab request context, i.e., the current theme.

    :param theme: Gets or sets the current user's theme.
    :type theme: str
    """

    _attribute_map = {
        "theme": {"key": "theme", "type": "str"},
    }

    def __init__(self, *, theme=None, **kwargs) -> None:
        super(TabContext, self).__init__(**kwargs)
        self.theme = theme
        self._custom_init()

    def _custom_init(self):
        return


class TabRequest(Model):
    """
    Invoke ('tab/fetch') request value payload.

    :param tab_entity_context: Gets or sets current tab entity request context.
    :type tab_entity_context:
     ~botframework.connector.teams.models.TabEntityContext
    :param context: Gets or sets current tab entity request context.
    :type context:
     ~botframework.connector.teams.models.TabContext
    :param state: Gets or sets state, which is the magic code for OAuth Flow.
    :type state: str
    """

    _attribute_map = {
        "tab_entity_context": {"key": "tabContext", "type": "TabEntityContext"},
        "context": {"key": "context", "type": "TabContext"},
        "state": {"key": "state", "type": "str"},
    }

    def __init__(
        self, *, tab_entity_context=None, context=None, state=None, **kwargs
    ) -> None:
        super(TabRequest, self).__init__(**kwargs)
        self.tab_entity_context = tab_entity_context
        self.context = context
        self.state = state
        self._custom_init()

    def _custom_init(self):
        return


class TabResponseCard(Model):
    """
    Envelope for cards for a Tab request.

    :param card: Gets or sets adaptive card for this card tab response.
    :type card: object
    """

    _attribute_map = {
        "card": {"key": "card", "type": "object"},
    }

    def __init__(self, *, card=None, **kwargs) -> None:
        super(TabResponseCard, self).__init__(**kwargs)
        self.card = card
        self._custom_init()

    def _custom_init(self):
        return


class TabResponseCards(Model):
    """
    Envelope for cards for a TabResponse.

    :param cards: Gets or sets adaptive card for this card tab response.
    :type cards:
    list[ ~botframework.connector.teams.models.TabResponseCard]
    """

    _attribute_map = {
        "cards": {"key": "cards", "type": "[TabResponseCard]"},
    }

    def __init__(self, *, cards=None, **kwargs) -> None:
        super(TabResponseCards, self).__init__(**kwargs)
        self.cards = cards
        self._custom_init()

    def _custom_init(self):
        return


class TabResponsePayload(Model):
    """
    Initializes a new instance of the TabResponsePayload class.

    :param type: Gets or sets choice of action options when responding to the
     tab/fetch message. Possible values include: 'continue', 'auth' or 'silentAuth'
    :type type: str
    :param value: Gets or sets the TabResponseCards when responding to
     tab/fetch activity with type of 'continue'.
    :type value: TabResponseCards
    :param suggested_actions: Gets or sets the Suggested Actions for this card tab.
    :type suggested_actions: TabSuggestedActions
    """

    _attribute_map = {
        "type": {"key": "type", "type": "str"},
        "value": {"key": "value", "type": "TabResponseCards"},
        "suggested_actions": {"key": "suggestedActions", "type": "TabSuggestedActions"},
    }

    def __init__(
        self, *, type=None, value=None, suggested_actions=None, **kwargs
    ) -> None:
        super(TabResponsePayload, self).__init__(**kwargs)
        self.type = type
        self.value = value
        self.suggested_actions = suggested_actions
        self._custom_init()

    def _custom_init(self):
        return


class TabResponse(Model):
    """
    Envelope for Card Tab Response Payload.

    :param tab: Possible values include: 'continue', 'auth' or 'silentAuth'
    :type type: ~botframework.connector.teams.models.TabResponsePayload
    """

    _attribute_map = {
        "tab": {"key": "tab", "type": "TabResponsePayload"},
    }

    def __init__(self, *, tab=None, **kwargs) -> None:
        super(TabResponse, self).__init__(**kwargs)
        self.tab = tab
        self._custom_init()

    def _custom_init(self):
        return


class TabSumit(Model):
    """
    Invoke ('tab/submit') request value payload.

    :param tab_entity_context: Gets or sets current tab entity request context.
    :type tab_entity_context:
     ~botframework.connector.teams.models.TabEntityContext
    :param context: Gets or sets current tab entity request context.
    :type context:
     ~botframework.connector.teams.models.TabContext
    :param data: User input data. Free payload containing properties of key-value pairs.
    :type data:
     ~botframework.connector.teams.models.TabSubmitData
    """

    _attribute_map = {
        "tab_entity_context": {"key": "tabContext", "type": "TabEntityContext"},
        "context": {"key": "context", "type": "TabContext"},
        "data": {"key": "data", "type": "TabSubmitData"},
    }

    def __init__(
        self, *, tab_entity_context=None, context=None, data=None, **kwargs
    ) -> None:
        super(TabSumit, self).__init__(**kwargs)
        self.tab_entity_context = tab_entity_context
        self.context = context
        self.data = data
        self._custom_init()

    def _custom_init(self):
        return


class TabSubmitData(Model):
    """
    Invoke ('tab/submit') request value payload data.

    :param type: Currently, 'tab/submit'.
    :type type: str
    :param properties: Gets or sets properties that are not otherwise defined by the TabSubmit
     type but that might appear in the serialized REST JSON object.
    :type properties: object
    """

    _attribute_map = {
        "type": {"key": "type", "type": "str"},
        "properties": {"key": "properties", "type": "{object}"},
    }

    def __init__(self, *, type=None, properties=None, **kwargs) -> None:
        super(TabSubmitData, self).__init__(**kwargs)
        self.type = type
        self.properties = properties
        self._custom_init()

    def _custom_init(self):
        return


class TabSubmit(Model):
    """
    Initializes a new instance of the TabSubmit class.

    :param tab_entity_context: Gets or sets current tab entity request context.
    :type tab_entity_context: ~botframework.connector.teams.models.TabEntityContext
    :param context: Gets or sets current user context, i.e., the current theme.
    :type context: ~botframework.connector.teams.models.TabContext
    :param data: User input data. Free payload containing properties of key-value pairs.
    :type data: ~botframework.connector.teams.models.TabSubmitData
    """

    _attribute_map = {
        "tab_entity_context": {"key": "tabContext", "type": "TabEntityContext"},
        "context": {"key": "context", "type": "TabContext"},
        "data": {"key": "data", "type": "TabSubmitData"},
    }

    def __init__(
        self, *, tab_entity_context=None, context=None, data=None, **kwargs
    ) -> None:
        super(TabSubmit, self).__init__(**kwargs)
        self.tab_entity_context = tab_entity_context
        self.context = context
        self.data = data
        self._custom_init()

    def _custom_init(self):
        return


class TabSuggestedActions(Model):
    """
    Tab SuggestedActions (Only when type is 'auth' or 'silentAuth').

    :param actions: Gets or sets adaptive card for this card tab response.
    :type actions: list[~botframework.connector.models.CardAction]
    """

    _attribute_map = {
        "actions": {"key": "actions", "type": "[CardAction]"},
    }

    def __init__(self, *, actions=None, **kwargs) -> None:
        super(TabSuggestedActions, self).__init__(**kwargs)
        self.actions = actions
        self._custom_init()

    def _custom_init(self):
        return


class TaskModuleCardResponse(TaskModuleResponseBase):
    """
    Tab Response to 'task/submit' from a tab.

    :param value: The JSON for the Adaptive cards to appear in the tab.
    :type value: ~botframework.connector.teams.models.TabResponse
    """

    _attribute_map = {
        "value": {"key": "value", "type": "TabResponse"},
    }

    def __init__(self, *, value=None, **kwargs) -> None:
        super(TaskModuleCardResponse, self).__init__("continue", **kwargs)
        self.value = value
        self._custom_init()

    def _custom_init(self):
        return


class MeetingDetailsBase(Model):
    """Specific details of a Teams meeting.

    :param id: The meeting's Id, encoded as a BASE64 string.
    :type id: str
    :param join_url: The URL used to join the meeting.
    :type join_url: str
    :param title: The title of the meeting.
    :type title: str
    """

    _attribute_map = {
        "id": {"key": "uniqueId", "type": "str"},
        "join_url": {"key": "joinUrl", "type": "str"},
        "title": {"key": "title", "type": "str"},
    }

    def __init__(
        self, *, id: str = None, join_url: str = None, title: str = None, **kwargs
    ) -> None:
        super(MeetingDetailsBase, self).__init__(**kwargs)
        self.id = id
        self.join_url = join_url
        self.title = title


class MeetingDetails(MeetingDetailsBase):
    """Specific details of a Teams meeting.

    :param ms_graph_resource_id: The MsGraphResourceId, used specifically for MS Graph API calls.
    :type ms_graph_resource_id: str
    :param scheduled_start_time: The meeting's scheduled start time, in UTC.
    :type scheduled_start_time: str
    :param scheduled_end_time: The meeting's scheduled end time, in UTC.
    :type scheduled_end_time: str
    :param type: The meeting's type.
    :type type: str
    """

    _attribute_map = {
        "ms_graph_resource_id": {"key": "msGraphResourceId", "type": "str"},
        "scheduled_start_time": {"key": "scheduledStartTime", "type": "str"},
        "scheduled_end_time": {"key": "scheduledEndTime", "type": "str"},
        "type": {"key": "type", "type": "str"},
    }

    def __init__(
        self,
        *,
        ms_graph_resource_id: str = None,
        scheduled_start_time: str = None,
        scheduled_end_time: str = None,
        type: str = None,
        **kwargs
    ) -> None:
        super(MeetingDetails, self).__init__(**kwargs)
        self.ms_graph_resource_id = ms_graph_resource_id
        self.scheduled_start_time = scheduled_start_time
        self.scheduled_end_time = scheduled_end_time
        self.type = type


class MeetingInfo(Model):
    """General information about a Teams meeting.

    :param details: The specific details of a Teams meeting.
    :type details: ~botframework.connector.teams.models.MeetingDetails
    :param conversation: The Conversation Account for the meeting.
    :type conversation: ~botbuilder.schema.models.ConversationAccount
    :param organizer: The meeting's scheduled start time, in UTC.
    :type organizer: ~botbuilder.schema.models.TeamsChannelAccount
    """

    _attribute_map = {
        "details": {"key": "details", "type": "object"},
        "conversation": {"key": "conversation", "type": "object"},
        "organizer": {"key": "organizer", "type": "object"},
    }

    def __init__(
        self,
        *,
        details: MeetingDetails = None,
        conversation: ConversationAccount = None,
        organizer: TeamsChannelAccount = None,
        **kwargs
    ) -> None:
        super(MeetingInfo, self).__init__(**kwargs)
        self.details = details
        self.conversation = conversation
        self.organizer = organizer


class MeetingEventDetails(MeetingDetailsBase):
    """Base class for Teams meting start and end events.

    :param meeting_type: The meeting's type.
    :type meeting_type: str
    """

    _attribute_map = {"meeting_type": {"key": "MeetingType", "type": "str"}}

    def __init__(self, *, meeting_type: str = None, **kwargs):
        super(MeetingEventDetails, self).__init__(**kwargs)
        self.meeting_type = meeting_type


class MeetingStartEventDetails(MeetingDetailsBase):
    """Specific details of a Teams meeting start event.

    :param start_time: Timestamp for meeting start, in UTC.
    :type start_time: str
    """

    _attribute_map = {"start_time": {"key": "StartTime", "type": "str"}}

    def __init__(self, *, start_time: str = None, **kwargs):
        super(MeetingStartEventDetails, self).__init__(**kwargs)
        self.start_time = start_time


class MeetingEndEventDetails(MeetingDetailsBase):
    """Specific details of a Teams meeting end event.

    :param end_time: Timestamp for meeting end, in UTC.
    :type end_time: str
    """

    _attribute_map = {"end_time": {"key": "EndTime", "type": "str"}}

    def __init__(self, *, end_time: str = None, **kwargs):
        super(MeetingEndEventDetails, self).__init__(**kwargs)
        self.end_time = end_time
