from msrest.serialization import Model



class RecognizerResult(Model):
    _attribute_map = {
        'text': {'key': 'text', 'type': 'str'},
        'altered_text': {'key': 'alteredText', 'type': 'str'},
        'intents': {'key': 'intents', 'type': '{IntentScore}'},
        'entities': {'key': 'entities', 'type': 'object'},
        'properties': {'key': 'properties', 'type': '{object}'},
    }

    def __init__(self, **kwargs):
        self.text = kwargs.get('text')
        self.altered_text = kwargs.get('altered_text') or kwargs.get('alteredText')
        self.intents = kwargs.get('intents')
        self.entities =
        self.properties = kwargs.get('properties')


class TokenExchangeState(Model):
    _attribute_map = {
        'connection_name': {'key': 'connectionName', 'type': 'str'},
        'conversation': {'key': 'conversation', 'type': 'ConversationReference'},
        'bot_url': {'key': 'botUrl', 'type': 'str'},
        'ms_app_id': {'key': 'msAppId', 'type': 'str'},
    }

    def __init__(self, *, connection_name: str = None, conversation: ConversationReference = None, bot_url: str = None,
                 ms_app_id: str = None, **kwargs) -> None:
        super(TokenExchangeState, self).__init__(**kwargs)
        self.connection_name = connection_name
        self.conversation = conversation
        self.bot_url = bot_url
        self.ms_app_id = ms_app_id
