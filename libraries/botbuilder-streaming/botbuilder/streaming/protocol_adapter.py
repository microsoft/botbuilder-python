# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.streaming.payloads import RequestManager
from botbuilder.streaming.payload_transport import PayloadSender, PayloadReceiver

from .request_handler import RequestHandler


class ProtocolAdapter:
    def __init__(
        self,
        request_handler: RequestHandler,
        request_manager: RequestManager,
        payload_sender: PayloadSender,
        payload_receiver: PayloadReceiver,
    ):
        self._request_handler = request_handler
        self._request_manager = request_manager
        self._payload_sender = payload_sender
        self._payload_receiver = payload_receiver

        self._send_operations
