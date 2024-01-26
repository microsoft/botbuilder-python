# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
import asyncio
from uuid import UUID, uuid4

from botframework.streaming.payloads import (
    PayloadAssemblerManager,
    RequestManager,
    SendOperations,
    StreamManager,
)
from botframework.streaming.payloads.assemblers import PayloadStreamAssembler
from botframework.streaming.payload_transport import PayloadSender, PayloadReceiver

from .receive_request import ReceiveRequest
from .receive_response import ReceiveResponse
from .request_handler import RequestHandler
from .streaming_request import StreamingRequest


class ProtocolAdapter:
    def __init__(
        self,
        request_handler: RequestHandler,
        request_manager: RequestManager,
        payload_sender: PayloadSender,
        payload_receiver: PayloadReceiver,
        handler_context: object = None,
    ):
        self._request_handler = request_handler
        self._request_manager = request_manager
        self._payload_sender = payload_sender
        self._payload_receiver = payload_receiver
        self._handler_context = handler_context

        self._send_operations = SendOperations(self._payload_sender)
        # TODO: might be able to remove
        self._stream_manager = StreamManager(self._on_cancel_stream)
        self._assembler_manager = PayloadAssemblerManager(
            self._stream_manager, self._on_receive_request, self._on_receive_response
        )

        self._payload_receiver.subscribe(
            self._assembler_manager.get_payload_stream,
            self._assembler_manager.on_receive,
        )

    async def send_request(self, request: StreamingRequest) -> ReceiveResponse:
        if not request:
            raise TypeError(
                f"'request: {request.__class__.__name__}' argument can't be None"
            )

        request_id = uuid4()
        response_task = self._request_manager.get_response(request_id)
        request_task = self._send_operations.send_request(request_id, request)

        [_, response] = await asyncio.gather(request_task, response_task)

        return response

    async def _on_receive_request(self, identifier: UUID, request: ReceiveRequest):
        # request is done, we can handle it
        if self._request_handler:
            response = await self._request_handler.process_request(
                request, None, self._handler_context
            )

            if response:
                await self._send_operations.send_response(identifier, response)

    async def _on_receive_response(self, identifier: UUID, response: ReceiveResponse):
        # we received the response to something, signal it
        await self._request_manager.signal_response(identifier, response)

    def _on_cancel_stream(self, content_stream_assembler: PayloadStreamAssembler):
        # TODO: on original C# code content_stream_assembler is typed as IAssembler
        task = asyncio.create_task(
            self._send_operations.send_cancel_stream(
                content_stream_assembler.identifier
            )
        )
