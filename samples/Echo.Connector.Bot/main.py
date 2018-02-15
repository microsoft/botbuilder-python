import json

from flask import Flask, request, Response
from microsoft.botframework.connector import ConnectorClient
from microsoft.botframework.connector.auth import MicrosoftTokenAuthentication
from microsoft.botbuilder.schema import *

APP_ID = ''
APP_PW = ''

app = Flask(__name__)
app.connector = None
app.credentials = MicrosoftTokenAuthentication(APP_ID, APP_PW)


@app.route("/api/messages", methods=['Post'])
def messages():
    activity = json.loads(request.data)
    if app.connector is None:
        app.connector = ConnectorClient(app.credentials, base_url=activity['serviceUrl'])

    if activity['type'] == 'message':
        response_activity = Activity(
            type=ActivityTypes.message,
            channel_id=activity['channelId'],
            recipient=ChannelAccount(id=activity['from']['id'], name=activity['from']['name']),
            from_property=ChannelAccount(id=activity['recipient']['id'], name=activity['recipient']['name']),
            text='You said "%s"' % activity['text']
            )
        app.connector.conversations.send_to_conversation(activity['conversation']['id'], response_activity)
        return Response("{}", status=200, mimetype='application/json')
    elif activity['type'] == 'conversationUpdate':
        message = 'Conversation update!'
        if 'membersAdded' in activity:
            message = 'Conversation update!\n\n"%s" (id: %s) joined the conversation.' %\
                      (activity['membersAdded'][0]['name'],
                       activity['membersAdded'][0]['id'])
        elif 'membersRemoved' in activity:
            message = 'Conversation update!\n\nid: "%s" left the conversation.' % activity['membersRemoved'][0]['id']
        response_activity = Activity(
            type=ActivityTypes.message,
            channel_id=activity['channelId'],
            recipient=ChannelAccount(id=activity['from']['id'], name=activity['from']['name']),
            from_property=ChannelAccount(id=activity['recipient']['id'], name=activity['recipient']['name']),
            text=message
            )
        app.connector.conversations.send_to_conversation(activity['conversation']['id'], response_activity)
        return Response("{}", status=202, mimetype='application/json')
    else:
        return Response("{}", status=202, mimetype='application/json')
