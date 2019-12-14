import aiounittest
from botbuilder.core import BotFrameworkHttpClient


class TestBotFrameworkHttpClient(aiounittest.AsyncTestCase):
    async def test_should_create_connector_client(self):
        with self.assertRaises(TypeError):
            BotFrameworkHttpClient(None)
