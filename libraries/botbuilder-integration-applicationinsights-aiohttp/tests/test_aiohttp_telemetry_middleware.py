from asyncio import Future
from unittest.mock import Mock, MagicMock
from aiounittest import AsyncTestCase

from botbuilder.integration.applicationinsights.aiohttp import (
    bot_telemetry_middleware,
    aiohttp_telemetry_middleware,
)


class TestAiohttpTelemetryMiddleware(AsyncTestCase):
    # pylint: disable=protected-access
    async def test_bot_telemetry_middleware(self):
        req = Mock()
        req.headers = {"Content-Type": "application/json"}
        req.json = MagicMock(return_value=Future())
        req.json.return_value.set_result("mock body")

        async def handler(value):
            return value

        sut = await bot_telemetry_middleware(req, handler)

        assert "mock body" in aiohttp_telemetry_middleware._REQUEST_BODIES.values()
        aiohttp_telemetry_middleware._REQUEST_BODIES.clear()
        assert req == sut

    def test_retrieve_aiohttp_body(self):
        aiohttp_telemetry_middleware._REQUEST_BODIES = Mock()
        aiohttp_telemetry_middleware._REQUEST_BODIES.pop = Mock(
            return_value="test body"
        )
        assert aiohttp_telemetry_middleware.retrieve_aiohttp_body() == "test body"

        aiohttp_telemetry_middleware._REQUEST_BODIES = {}
