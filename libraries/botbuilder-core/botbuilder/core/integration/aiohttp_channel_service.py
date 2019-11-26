# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from aiohttp.web import RouteTableDef, Request, Response

from botbuilder.schema import Activity

from .channel_service_handler import ChannelServiceHandler


async def deserialize_activity(request: Request) -> Activity:
    if "application/json" in request.headers["Content-Type"]:
        body = await request.json()
    else:
        return Response(status=415)

    return Activity().deserialize(body)


def channel_service_routes(handler: ChannelServiceHandler) -> RouteTableDef:
    routes = RouteTableDef()

    @routes.post("/{conversation_id}/activities")
    async def send_to_conversation(request: Request):
        activity = await deserialize_activity(request)
        return await handler.handle_send_to_conversation(
            request.headers.get("Authorization"),
            request.match_info["conversation_id"],
            activity,
        )

    @routes.post("/{conversation_id}/activities/{activity_id}")
    async def reply_to_activity(request: Request):
        activity = await deserialize_activity(request)
        return await handler.handle_reply_to_activity(
            request.headers.get("Authorization"),
            request.match_info["conversation_id"],
            request.match_info["activity_id"],
            activity,
        )

    @routes.put("/{conversation_id}/activities/{activity_id}")
    async def update_activity(request: Request):
        activity = await deserialize_activity(request)
        return await handler.handle_update_activity(
            request.headers.get("Authorization"),
            request.match_info["conversation_id"],
            request.match_info["activity_id"],
            activity,
        )

    @routes.delete("/{conversation_id}/activities/{activity_id}")
    async def delete_activity(request: Request):
        return await handler.handle_delete_activity(
            request.headers.get("Authorization"),
            request.match_info["conversation_id"],
            request.match_info["activity_id"],
        )

    @routes.get("/{conversation_id}/activities/{activity_id}/members")
    async def get_activity_members(request: Request):
        raise NotImplementedError("get_activity_members is not supported")

    @routes.post("/")
    async def create_conversation(request: Request):
        raise NotImplementedError("create_conversation is not supported")

    @routes.get("/")
    async def get_conversation(request: Request):
        raise NotImplementedError("get_conversation is not supported")

    @routes.get("/{conversation_id}/members")
    async def get_conversation_members(request: Request):
        raise NotImplementedError("get_activity_members is not supported")

    @routes.get("/{conversation_id}/pagedmembers")
    async def get_conversation_paged_members(request: Request):
        raise NotImplementedError("get_conversation_paged_members is not supported")

    @routes.delete("/{conversation_id}/members/{member_id}")
    async def delete_conversation_members(request: Request):
        raise NotImplementedError("delete_conversation_members is not supported")

    @routes.post("/{conversation_id}/activities/history")
    async def get_conversation_history(request: Request):
        raise NotImplementedError("get_conversation_history is not supported")

    @routes.post("/{conversation_id}/attachments")
    async def upload_attachment(request: Request):
        raise NotImplementedError("upload_attachment is not supported")

    return routes
