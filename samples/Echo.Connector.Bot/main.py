# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import http.server
import json
from microsoft.botbuilder.schema import (Activity, ActivityTypes, ChannelAccount)
from microsoft.botframework.connector import ConnectorClient
from microsoft.botframework.connector.auth import (MicrosoftAppCredentials,
                                                   JwtTokenValidation, SimpleCredentialProvider)

APP_ID = ''
APP_PASSWORD = ''

class MyHandler(http.server.BaseHTTPRequestHandler):

    def __handle_conversation_update_activity(self, data):
        self.send_response(202)
        self.end_headers()
        if data['membersAdded'][0]['id'] != data['recipient']['id']:
            credentials = MicrosoftAppCredentials(APP_ID, APP_PASSWORD)
            connector = ConnectorClient(credentials, base_url=data['serviceUrl'])
            activity = Activity(
                type=ActivityTypes.message,
                channel_id=data['channelId'],
                recipient=ChannelAccount(id=data['from']['id'], name=data['from']['name']),
                from_property=ChannelAccount(
                    id=data['recipient']['id'],
                    name=data['recipient']['name']),
                text='Hello and welcome to the echo bot!')
            connector.conversations.send_to_conversation(data['conversation']['id'], activity)

    def __handle_message_activity(self, data):
        self.send_response(200)
        self.end_headers()
        credentials = MicrosoftAppCredentials(APP_ID, APP_PASSWORD)
        connector = ConnectorClient(credentials, base_url=data['serviceUrl'])
        activity = Activity(
            type=ActivityTypes.message,
            channel_id=data['channelId'],
            recipient=ChannelAccount(id=data['from']['id']),
            from_property=ChannelAccount(id=data['recipient']['id']),
            text='You said: %s' % data['text'])
        connector.conversations.send_to_conversation(data['conversation']['id'], activity)

    def __unhandled_activity(self):
        self.send_response(404)
        self.end_headers()

    def do_POST(self):
        body = self.rfile.read(int(self.headers['Content-Length']))
        data = json.loads(str(body, 'utf-8'))
        if data['type'] == 'conversationUpdate':
            self.__handle_conversation_update_activity(data)
        elif data['type'] == 'message':
            self.__handle_message_activity(data)
        else:
            self.__unhandled_activity()

try:
    SERVER = http.server.HTTPServer(('localhost', 9000), MyHandler)
    print('Started http server')
    SERVER.serve_forever()
except KeyboardInterrupt:
    print('^C received, shutting down server')
    SERVER.socket.close()
