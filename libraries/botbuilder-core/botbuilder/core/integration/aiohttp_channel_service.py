# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
import json
from typing import List, Union, Type

from aiohttp.web import RouteTableDef, Request, Response
from msrest.serialization import Model

from botbuilder.schema import (
    Activity,
    AttachmentData,
    ConversationParameters,
    Transcript,
)

from botbuilder.core import ChannelServiceHandler


async def deserialize_from_body(
    request: Request, target_model: Type[Model]
) -> Activity:
    if "application/json" in request.headers["Content-Type"]:
        body = await request.json()
    else:
        return Response(status=415)

    return target_model().deserialize(body)


def get_serialized_response(model_or_list: Union[Model, List[Model]]) -> Response:
    if isinstance(model_or_list, Model):
        json_obj = model_or_list.serialize()
    else:
        json_obj = [model.serialize() for model in model_or_list]

    return Response(body=json.dumps(json_obj), content_type="application/json")


def aiohttp_channel_service_routes(
    handler: ChannelServiceHandler, base_url: str = ""
) -> RouteTableDef:
    # pylint: disable=unused-variable
    routes = RouteTableDef()

    @routes.post(base_url + "/v3/conversations/{conversation_id}/activities")
    async def send_to_conversation(request: Request):
        activity = await deserialize_from_body(request, Activity)
        result = await handler.handle_send_to_conversation(
            request.headers.get("Authorization"),
            request.match_info["conversation_id"],
            activity,
        )

        return get_serialized_response(result)

    @routes.post(
        base_url + "/v3/conversations/{conversation_id}/activities/{activity_id}"
    )
    async def reply_to_activity(request: Request):
        activity = await deserialize_from_body(request, Activity)
        result = await handler.handle_reply_to_activity(
            request.headers.get("Authorization"),
            request.match_info["conversation_id"],
            request.match_info["activity_id"],
            activity,
        )

        return get_serialized_response(result)

    @routes.put(
        base_url + "/v3/conversations/{conversation_id}/activities/{activity_id}"
    )
    async def update_activity(request: Request):
        activity = await deserialize_from_body(request, Activity)
        result = await handler.handle_update_activity(
            request.headers.get("Authorization"),
            request.match_info["conversation_id"],
            request.match_info["activity_id"],
            activity,
        )

        return get_serialized_response(result)

    @routes.delete(
        base_url + "/v3/conversations/{conversation_id}/activities/{activity_id}"
    )
    async def delete_activity(request: Request):
        await handler.handle_delete_activity(
            request.headers.get("Authorization"),
            request.match_info["conversation_id"],
            request.match_info["activity_id"],
        )

        return Response()

    @routes.get(
        base_url
        + "/v3/conversations/{conversation_id}/activities/{activity_id}/members"
    )
    async def get_activity_members(request: Request):
        result = await handler.handle_get_activity_members(
            request.headers.get("Authorization"),
            request.match_info["conversation_id"],
            request.match_info["activity_id"],
        )

        return get_serialized_response(result)

    @routes.post(base_url + "/")
    async def create_conversation(request: Request):
        conversation_parameters = deserialize_from_body(request, ConversationParameters)
        result = await handler.handle_create_conversation(
            request.headers.get("Authorization"), conversation_parameters
        )

        return get_serialized_response(result)

    @routes.get(base_url + "/")
    async def get_conversation(request: Request):
        # TODO: continuation token?
        result = await handler.handle_get_conversations(
            request.headers.get("Authorization")
        )

        return get_serialized_response(result)

    @routes.get(base_url + "/v3/conversations/{conversation_id}/members")
    async def get_conversation_members(request: Request):
        result = await handler.handle_get_conversation_members(
            request.headers.get("Authorization"), request.match_info["conversation_id"],
        )

        return get_serialized_response(result)

    @routes.get(base_url + "/v3/conversations/{conversation_id}/pagedmembers")
    async def get_conversation_paged_members(request: Request):
        # TODO: continuation token? page size?
        result = await handler.handle_get_conversation_paged_members(
            request.headers.get("Authorization"), request.match_info["conversation_id"],
        )

        return get_serialized_response(result)

    @routes.delete(base_url + "/v3/conversations/{conversation_id}/members/{member_id}")
    async def delete_conversation_member(request: Request):
        result = await handler.handle_delete_conversation_member(
            request.headers.get("Authorization"),
            request.match_info["conversation_id"],
            request.match_info["member_id"],
        )

        return get_serialized_response(result)

    @routes.post(base_url + "/v3/conversations/{conversation_id}/activities/history")
    async def send_conversation_history(request: Request):
        transcript = deserialize_from_body(request, Transcript)
        result = await handler.handle_send_conversation_history(
            request.headers.get("Authorization"),
            request.match_info["conversation_id"],
            transcript,
        )

        return get_serialized_response(result)

    @routes.post(base_url + "/v3/conversations/{conversation_id}/attachments")
    async def upload_attachment(request: Request):
        attachment_data = deserialize_from_body(request, AttachmentData)
        result = await handler.handle_upload_attachment(
            request.headers.get("Authorization"),
            request.match_info["conversation_id"],
            attachment_data,
        )

        return get_serialized_response(result)

    return routes
