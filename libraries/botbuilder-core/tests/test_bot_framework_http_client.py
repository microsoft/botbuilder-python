import aiounittest
from botbuilder.integration.aiohttp import BotFrameworkHttpClient

# TODO: move this to integration aiohttp
class TestBotFrameworkHttpClient(aiounittest.AsyncTestCase):
    async def test_should_create_connector_client(self):
        with self.assertRaises(TypeError):
            BotFrameworkHttpClient(None)
