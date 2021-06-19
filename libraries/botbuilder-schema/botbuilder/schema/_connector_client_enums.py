# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from enum import Enum


class RoleTypes(str, Enum):

    user = "user"
    bot = "bot"
    skill = "skill"


class ActivityTypes(str, Enum):

    message = "message"
    contact_relation_update = "contactRelationUpdate"
    conversation_update = "conversationUpdate"
    typing = "typing"
    end_of_conversation = "endOfConversation"
    event = "event"
    invoke = "invoke"
    invoke_response = "invokeResponse"
    delete_user_data = "deleteUserData"
    message_update = "messageUpdate"
    message_delete = "messageDelete"
    installation_update = "installationUpdate"
    message_reaction = "messageReaction"
    suggestion = "suggestion"
    trace = "trace"
    handoff = "handoff"
    command = "command"
    command_result = "commandResult"


class TextFormatTypes(str, Enum):

    markdown = "markdown"
    plain = "plain"
    xml = "xml"


class AttachmentLayoutTypes(str, Enum):

    list = "list"
    carousel = "carousel"


class MessageReactionTypes(str, Enum):

    like = "like"
    plus_one = "plusOne"


class InputHints(str, Enum):

    accepting_input = "acceptingInput"
    ignoring_input = "ignoringInput"
    expecting_input = "expectingInput"


class ActionTypes(str, Enum):

    open_url = "openUrl"
    im_back = "imBack"
    post_back = "postBack"
    play_audio = "playAudio"
    play_video = "playVideo"
    show_image = "showImage"
    download_file = "downloadFile"
    signin = "signin"
    call = "call"
    message_back = "messageBack"


class EndOfConversationCodes(str, Enum):

    unknown = "unknown"
    completed_successfully = "completedSuccessfully"
    user_cancelled = "userCancelled"
    bot_timed_out = "botTimedOut"
    bot_issued_invalid_message = "botIssuedInvalidMessage"
    channel_failed = "channelFailed"


class ActivityImportance(str, Enum):

    low = "low"
    normal = "normal"
    high = "high"


class DeliveryModes(str, Enum):

    normal = "normal"
    notification = "notification"
    expect_replies = "expectReplies"
    ephemeral = "ephemeral"


class ContactRelationUpdateActionTypes(str, Enum):

    add = "add"
    remove = "remove"


class InstallationUpdateActionTypes(str, Enum):

    add = "add"
    remove = "remove"


class SemanticActionStates(str, Enum):

    start_action = "start"
    continue_action = "continue"
    done_action = "done"
