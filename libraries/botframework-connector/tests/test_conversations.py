import pytest
from azure_devtools.scenario_tests import ReplayableTest

from botbuilder.schema import *
from botframework.connector import ConnectorClient
from botframework.connector.auth import MicrosoftAppCredentials

from .authentication_stub import MicrosoftTokenAuthenticationStub

SERVICE_URL = 'https://slack.botframework.com'
CHANNEL_ID = 'slack'
BOT_NAME = 'botbuilder-pc-bot'
BOT_ID = 'B21UTEF8S:T03CWQ0QB'
RECIPIENT_ID = 'U19KH8EHJ:T03CWQ0QB'
CONVERSATION_ID = 'B21UTEF8S:T03CWQ0QB:D2369CT7C'


def get_auth_token():
    try:
        from .app_creds_real import MICROSOFT_APP_ID, MICROSOFT_APP_PASSWORD
        # Define a "app_creds_real.py" file with your bot credentials as follows:
        # MICROSOFT_APP_ID = '...'
        # MICROSOFT_APP_PASSWORD = '...'
        return MicrosoftAppCredentials(
            MICROSOFT_APP_ID,
            MICROSOFT_APP_PASSWORD).get_access_token()
    except ImportError:
        return 'STUB_ACCESS_TOKEN'


auth_token = get_auth_token()


class ConversationTest(ReplayableTest):
    def __init__(self, method_name):
        super(ConversationTest, self).__init__(method_name)

    @property
    def credentials(self):
        return MicrosoftTokenAuthenticationStub(auth_token)

    def test_conversations_create_conversation(self):
        to = ChannelAccount(id=RECIPIENT_ID)
        create_conversation = ConversationParameters(
            bot=ChannelAccount(id=BOT_ID),
            members=[to],
            activity = Activity(
                type=ActivityTypes.message,
                channel_id=CHANNEL_ID,
                from_property=ChannelAccount(id=BOT_ID),
                recipient=to,
                text='Hi there!'))

        connector = ConnectorClient(self.credentials, base_url=SERVICE_URL)
        conversation = connector.conversations.create_conversation(create_conversation)

        assert conversation.id is not None

    def test_conversations_create_conversation_with_invalid_bot_id_fails(self):
        to = ChannelAccount(id=RECIPIENT_ID)
        create_conversation = ConversationParameters(
            bot=ChannelAccount(id='INVALID'),
            members=[to],
            activity = Activity(
                type=ActivityTypes.message,
                channel_id=CHANNEL_ID,
                from_property=ChannelAccount(id='INVALID'),
                recipient=to,
                text='Hi there!'))

        with pytest.raises(ErrorResponseException) as excinfo:
            connector = ConnectorClient(self.credentials, base_url=SERVICE_URL)
            connector.conversations.create_conversation(create_conversation)

        assert excinfo.value.error.error.code == 'ServiceError'
        assert ('Invalid userId' in str(excinfo.value.error.error.message))

    def test_conversations_create_conversation_without_members_fails(self):
        create_conversation = ConversationParameters(
            bot=ChannelAccount(id=BOT_ID),
            activity=Activity(
                type=ActivityTypes.message,
                channel_id=CHANNEL_ID,
                from_property=ChannelAccount(id=BOT_ID),
                text='Hi there!'),
            members=[])

        with pytest.raises(ErrorResponseException) as excinfo:
            connector = ConnectorClient(self.credentials, base_url=SERVICE_URL)
            connector.conversations.create_conversation(create_conversation)

        assert excinfo.value.error.error.code == 'BadArgument'
        assert ('Conversations' in str(excinfo.value.error.error.message))

    def test_conversations_create_conversation_with_bot_as_only_member_fails(self):
        to = ChannelAccount(id=BOT_ID)
        sender = ChannelAccount(id=BOT_ID)
        create_conversation = ConversationParameters(
            bot=sender,
            members=[to],
            activity = Activity(
                type=ActivityTypes.message,
                channel_id=CHANNEL_ID,
                from_property=sender,
                recipient=to,
                text='Hi there!'))

        with pytest.raises(ErrorResponseException) as excinfo:
            connector = ConnectorClient(self.credentials, base_url=SERVICE_URL)
            connector.conversations.create_conversation(create_conversation)

        assert excinfo.value.error.error.code == 'BadArgument'
        assert ('Bots cannot IM other bots' in str(excinfo.value.error.error.message))

    def test_conversations_send_to_conversation(self):
        activity = Activity(
            type=ActivityTypes.message,
            channel_id=CHANNEL_ID,
            recipient=ChannelAccount(id=RECIPIENT_ID),
            from_property=ChannelAccount(id=BOT_ID),
            text='Hello again!')

        connector = ConnectorClient(self.credentials, base_url=SERVICE_URL)
        response = connector.conversations.send_to_conversation(
            CONVERSATION_ID, activity)

        assert response is not None

    def test_conversations_send_to_conversation_with_attachment(self):
        card1 = HeroCard(
            title='A static image',
            text='JPEG image',
            images=[
                CardImage(url='https://docs.com/en-us/bot-framework/media/designing-bots/core/dialogs-screens.png')
            ])

        card2 = HeroCard(
            title='An animation',
            subtitle='GIF image',
            images=[
                CardImage(url='http://i.giphy.com/Ki55RUbOV5njy.gif')
            ])

        activity = Activity(
            type=ActivityTypes.message,
            channel_id=CHANNEL_ID,
            recipient=ChannelAccount(id=RECIPIENT_ID),
            from_property=ChannelAccount(id=BOT_ID),
            attachment_layout=AttachmentLayoutTypes.list,
            attachments=[
                Attachment(content_type='application/vnd.card.hero', content=card1),
                Attachment(content_type='application/vnd.card.hero', content=card2),
            ])

        connector = ConnectorClient(self.credentials, base_url=SERVICE_URL)
        response = connector.conversations.send_to_conversation(CONVERSATION_ID, activity)

        assert response is not None

    def test_conversations_send_to_conversation_with_invalid_conversation_id_fails(self):
        activity = Activity(
            type=ActivityTypes.message,
            channel_id=CHANNEL_ID,
            recipient=ChannelAccount(id=RECIPIENT_ID),
            from_property=ChannelAccount(id=BOT_ID),
            text='Error!')

        with pytest.raises(ErrorResponseException) as excinfo:
            connector = ConnectorClient(self.credentials, base_url=SERVICE_URL)
            connector.conversations.send_to_conversation('123', activity)

        assert excinfo.value.error.error.code == 'ServiceError'
        assert ('cannot send messages to this id' in str(excinfo.value.error.error.message)
                or 'Invalid ConversationId' in str(excinfo.value.error.error.message))

    def test_conversations_get_conversation_members(self):
        connector = ConnectorClient(self.credentials, base_url=SERVICE_URL)
        members = connector.conversations.get_conversation_members(CONVERSATION_ID)

        assert len(members) == 2
        assert members[0].name == BOT_NAME
        assert members[0].id == BOT_ID

    def test_conversations_get_conversation_members_invalid_id_fails(self):
        with pytest.raises(ErrorResponseException) as excinfo:
            connector = ConnectorClient(self.credentials, base_url=SERVICE_URL)
            members = connector.conversations.get_conversation_members('INVALID_ID')

        assert excinfo.value.error.error.code == 'ServiceError'
        assert ('cannot send messages to this id' in str(excinfo.value.error.error.message)
                or 'Invalid ConversationId' in str(excinfo.value.error.error.message))

    def test_conversations_update_activity(self):
        activity = Activity(
            type=ActivityTypes.message,
            channel_id=CHANNEL_ID,
            recipient=ChannelAccount(id=RECIPIENT_ID),
            from_property=ChannelAccount(id=BOT_ID),
            text='Updating activity...')

        activity_update = Activity(
            type=ActivityTypes.message,
            channel_id=CHANNEL_ID,
            recipient=ChannelAccount(id=RECIPIENT_ID),
            from_property=ChannelAccount(id=BOT_ID),
            text='Activity updated.')

        connector = ConnectorClient(self.credentials, base_url=SERVICE_URL)
        response = connector.conversations.send_to_conversation(CONVERSATION_ID, activity)
        activity_id = response.id
        response = connector.conversations.update_activity(CONVERSATION_ID, activity_id, activity_update)

        assert response is not None
        assert response.id == activity_id

    def test_conversations_update_activity_invalid_conversation_id_fails(self):
        activity = Activity(
            type=ActivityTypes.message,
            channel_id=CHANNEL_ID,
            recipient=ChannelAccount(id=RECIPIENT_ID),
            from_property=ChannelAccount(id=BOT_ID),
            text='Updating activity...')

        activity_update = Activity(
            type=ActivityTypes.message,
            channel_id=CHANNEL_ID,
            recipient=ChannelAccount(id=RECIPIENT_ID),
            from_property=ChannelAccount(id=BOT_ID),
            text='Activity updated.')

        with pytest.raises(ErrorResponseException) as excinfo:
            connector = ConnectorClient(self.credentials, base_url=SERVICE_URL)
            response = connector.conversations.send_to_conversation(CONVERSATION_ID, activity)
            activity_id = response.id
            connector.conversations.update_activity('INVALID_ID', activity_id, activity_update)

        assert excinfo.value.error.error.code == 'ServiceError'
        assert ('Invalid ConversationId' in str(excinfo.value.error.error.message))

    def test_conversations_reply_to_activity(self):
        activity = Activity(
            type=ActivityTypes.message,
            channel_id=CHANNEL_ID,
            recipient=ChannelAccount(id=RECIPIENT_ID),
            from_property=ChannelAccount(id=BOT_ID),
            text='Thread activity')

        child_activity = Activity(
            type=ActivityTypes.message,
            channel_id=CHANNEL_ID,
            recipient=ChannelAccount(id=RECIPIENT_ID),
            from_property=ChannelAccount(id=BOT_ID),
            text='Child activity.')

        connector = ConnectorClient(self.credentials, base_url=SERVICE_URL)
        response = connector.conversations.send_to_conversation(CONVERSATION_ID, activity)
        activity_id = response.id
        response = connector.conversations.reply_to_activity(CONVERSATION_ID, activity_id, child_activity)

        assert response is not None
        assert response.id != activity_id

    def test_conversations_reply_to_activity_with_invalid_conversation_id_fails(self):
        child_activity = Activity(
            type=ActivityTypes.message,
            channel_id=CHANNEL_ID,
            recipient=ChannelAccount(id=RECIPIENT_ID),
            from_property=ChannelAccount(id=BOT_ID),
            text='Child activity.')

        with pytest.raises(ErrorResponseException) as excinfo:
            connector = ConnectorClient(self.credentials, base_url=SERVICE_URL)
            connector.conversations.reply_to_activity('INVALID_ID', 'INVALID_ID', child_activity)

        assert excinfo.value.error.error.code == 'ServiceError'
        assert ('Invalid ConversationId' in str(excinfo.value.error.error.message))

    def test_conversations_delete_activity(self):
        activity = Activity(
            type=ActivityTypes.message,
            channel_id=CHANNEL_ID,
            recipient=ChannelAccount(id=RECIPIENT_ID),
            from_property=ChannelAccount(id=BOT_ID),
            text='Activity to be deleted..')

        connector = ConnectorClient(self.credentials, base_url=SERVICE_URL)
        response = connector.conversations.send_to_conversation(CONVERSATION_ID, activity)
        activity_id = response.id
        response = connector.conversations.delete_activity(CONVERSATION_ID, activity_id)

        assert response is None

    def test_conversations_delete_activity_with_invalid_conversation_id_fails(self):
        with pytest.raises(ErrorResponseException) as excinfo:
            connector = ConnectorClient(self.credentials, base_url=SERVICE_URL)
            connector.conversations.delete_activity('INVALID_ID', 'INVALID_ID')

        assert excinfo.value.error.error.code == 'ServiceError'
        assert ('Invalid ConversationId' in str(excinfo.value.error.error.message))

    def test_conversations_get_activity_members(self):
        activity = Activity(
            type=ActivityTypes.message,
            channel_id=CHANNEL_ID,
            recipient=ChannelAccount(id=RECIPIENT_ID),
            from_property=ChannelAccount(id=BOT_ID),
            text='Test Activity')

        connector = ConnectorClient(self.credentials, base_url=SERVICE_URL)
        response = connector.conversations.send_to_conversation(CONVERSATION_ID, activity)
        members = connector.conversations.get_activity_members(CONVERSATION_ID, response.id)

        assert len(members) == 2
        assert members[0].name == BOT_NAME
        assert members[0].id == BOT_ID

    def test_conversations_get_activity_members_invalid_conversation_id_fails(self):
        activity = Activity(
            type=ActivityTypes.message,
            channel_id=CHANNEL_ID,
            recipient=ChannelAccount(id=RECIPIENT_ID),
            from_property=ChannelAccount(id=BOT_ID),
            text='Test Activity')

        with pytest.raises(ErrorResponseException) as excinfo:
            connector = ConnectorClient(self.credentials, base_url=SERVICE_URL)
            response = connector.conversations.send_to_conversation(CONVERSATION_ID, activity)
            connector.conversations.get_activity_members('INVALID_ID', response.id)

        assert excinfo.value.error.error.code == 'ServiceError'
        assert 'Invalid ConversationId' in str(excinfo.value.error.error.message)
