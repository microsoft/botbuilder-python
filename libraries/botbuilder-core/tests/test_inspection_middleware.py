# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import aiounittest
from requests import Session
#from requests_mock import Adapter

from botbuilder.core import MemoryStorage, MessageFactory, TurnContext
from botbuilder.core.adapters import TestAdapter
from botbuilder.core.inspection import InspectionMiddleware, InspectionState


class TestConversationState(aiounittest.AsyncTestCase):
    def setUp(self):
        self.session = Session()
        self.mock_adapter = Adapter()
        self.session.mount("mock", self.mock_adapter)

    async def test_scenario_with_inspection_middlware_passthrough(self):
        inspection_state = InspectionState(MemoryStorage())
        inspection_middleware = InspectionMiddleware(inspection_state)

        adapter = TestAdapter()
        adapter.use(inspection_middleware)

        inbound_activity = MessageFactory.text("hello")

        async def aux_func(context: TurnContext):
            await context.send_activity(MessageFactory.text("hi"))

        await adapter.process_activity(inbound_activity, aux_func)

        outbound_activity = adapter.activity_buffer.pop(0)

        assert outbound_activity.text, "hi"

