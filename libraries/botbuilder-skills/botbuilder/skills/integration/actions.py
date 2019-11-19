# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from typing import Dict

from flask import Request

from botbuilder.core import Bot, BotAdapter
from botbuilder.schema import (
    Activity,
    AttachmentData,
    ConversationParameters,
    Transcript,
)

from botframework.connector.auth import ClaimsIdentity

from ..bot_framework_skill_client import BotFrameworkClient
from ..http_helper import HttpHelper


async def get_activity_members_action(
    adapter: BotAdapter,
    skill_client: BotFrameworkClient,
    bot: Bot,
    claims_identity: ClaimsIdentity,
    request: Request,  # pylint: disable=unused-argument
    parameters: Dict[str, str],
):
    return await skill_client.get_activity_members(
        adapter,
        bot,
        claims_identity,
        parameters["conversation_id"],
        parameters["activity_id"],
    )


async def send_conversation_history_action(
    adapter: BotAdapter,
    skill_client: BotFrameworkClient,
    bot: Bot,
    claims_identity: ClaimsIdentity,
    request: Request,
    parameters: Dict[str, str],
):
    history: Transcript = HttpHelper.read_request(Transcript, request)
    return await skill_client.send_conversation_history(
        adapter, bot, claims_identity, parameters["conversation_id"], history,
    )


async def reply_to_activity_action(
    adapter: BotAdapter,
    skill_client: BotFrameworkClient,
    bot: Bot,
    claims_identity: ClaimsIdentity,
    request: Request,
    parameters: Dict[str, str],
):
    reply_to_activity: Activity = HttpHelper.read_request(Activity, request)
    return await skill_client.reply_to_activity(
        adapter,
        bot,
        claims_identity,
        reply_to_activity.conversation.id,
        parameters["activity_id"],
        reply_to_activity,
    )


async def update_activity_action(
    adapter: BotAdapter,
    skill_client: BotFrameworkClient,
    bot: Bot,
    claims_identity: ClaimsIdentity,
    request: Request,
    parameters: Dict[str, str],
):
    update_activity: Activity = HttpHelper.read_request(Activity, request)
    return await skill_client.update_activity(
        adapter,
        bot,
        claims_identity,
        parameters["conversation_id"],
        parameters["activity_id"],
        update_activity,
    )


async def delete_activity_action(
    adapter: BotAdapter,
    skill_client: BotFrameworkClient,
    bot: Bot,
    claims_identity: ClaimsIdentity,
    request: Request,  # pylint: disable=unused-argument
    parameters: Dict[str, str],
):
    await skill_client.delete_activity(
        adapter,
        bot,
        claims_identity,
        parameters["conversation_id"],
        parameters["activity_id"],
    )
    return None


async def send_to_conversaiton_action(
    adapter: BotAdapter,
    skill_client: BotFrameworkClient,
    bot: Bot,
    claims_identity: ClaimsIdentity,
    request: Request,
    parameters: Dict[str, str],
):
    send_to_conversation_act: Activity = HttpHelper.read_request(Activity, request)
    return await skill_client.send_to_conversation(
        adapter,
        bot,
        claims_identity,
        parameters["conversation_id"],
        send_to_conversation_act,
    )


async def delete_conversation_member_action(
    adapter: BotAdapter,
    skill_client: BotFrameworkClient,
    bot: Bot,
    claims_identity: ClaimsIdentity,
    request: Request,  # pylint: disable=unused-argument
    parameters: Dict[str, str],
):
    await skill_client.delete_conversation_member(
        adapter,
        bot,
        claims_identity,
        parameters["conversation_id"],
        parameters["member_id"],
    )
    return None


async def upload_attachment_action(
    adapter: BotAdapter,
    skill_client: BotFrameworkClient,
    bot: Bot,
    claims_identity: ClaimsIdentity,
    request: Request,
    parameters: Dict[str, str],
):
    upload_attachment: AttachmentData = HttpHelper.read_request(AttachmentData, request)
    return await skill_client.upload_attachment(
        adapter, bot, claims_identity, parameters["conversation_id"], upload_attachment,
    )


async def get_conversation_members_action(
    adapter: BotAdapter,
    skill_client: BotFrameworkClient,
    bot: Bot,
    claims_identity: ClaimsIdentity,
    request: Request,  # pylint: disable=unused-argument
    parameters: Dict[str, str],
):
    return await skill_client.get_conversation_members(
        adapter, bot, claims_identity, parameters["conversation_id"],
    )


async def get_conversation_paged_members_action(
    adapter: BotAdapter,
    skill_client: BotFrameworkClient,
    bot: Bot,
    claims_identity: ClaimsIdentity,
    request: Request,  # pylint: disable=unused-argument
    parameters: Dict[str, str],
):
    page_size = -1 if not parameters.get("page_size") else int(parameters["page_size"])
    return await skill_client.get_conversation_paged_members(
        adapter,
        bot,
        claims_identity,
        parameters["conversation_id"],
        page_size,
        parameters["continuation_token"],
    )


async def get_conversations_action(
    adapter: BotAdapter,
    skill_client: BotFrameworkClient,
    bot: Bot,
    claims_identity: ClaimsIdentity,
    request: Request,  # pylint: disable=unused-argument
    parameters: Dict[str, str],
):
    return await skill_client.get_conversations(
        adapter, bot, claims_identity, parameters["conversation_id"],
    )


async def create_conversation_action(
    adapter: BotAdapter,
    skill_client: BotFrameworkClient,
    bot: Bot,
    claims_identity: ClaimsIdentity,
    request: Request,
    parameters: Dict[str, str],
):
    conversation_parameters: ConversationParameters = HttpHelper.read_request(
        ConversationParameters, request
    )
    return await skill_client.create_conversation(
        adapter,
        bot,
        claims_identity,
        parameters["conversation_id"],
        conversation_parameters,
    )
