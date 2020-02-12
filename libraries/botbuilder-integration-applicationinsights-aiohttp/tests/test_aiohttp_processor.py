from unittest.mock import Mock
from aiounittest import AsyncTestCase

import aiohttp  # pylint: disable=unused-import

from botbuilder.integration.applicationinsights.aiohttp import (
    aiohttp_telemetry_middleware,
    AiohttpTelemetryProcessor,
)


class TestAiohttpTelemetryProcessor(AsyncTestCase):
    # pylint: disable=protected-access
    def test_can_process(self):
        assert AiohttpTelemetryProcessor.detect_aiohttp()
        assert AiohttpTelemetryProcessor().can_process()

    def test_retrieve_aiohttp_body(self):
        aiohttp_telemetry_middleware._REQUEST_BODIES = Mock()
        aiohttp_telemetry_middleware._REQUEST_BODIES.pop = Mock(
            return_value="test body"
        )
        assert aiohttp_telemetry_middleware.retrieve_aiohttp_body() == "test body"

        assert AiohttpTelemetryProcessor().get_request_body() == "test body"
        aiohttp_telemetry_middleware._REQUEST_BODIES = {}
