# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import http.server
import json
import asyncio
from microsoft.botbuilder.schema import (Activity, ActivityTypes, ChannelAccount)
from microsoft.botframework.connector import ConnectorClient
from microsoft.botframework.connector.auth import (MicrosoftAppCredentials,
                                                   JwtTokenValidation, SimpleCredentialProvider)

APP_ID = ''
APP_PASSWORD = ''

class MyHandler(http.server.BaseHTTPRequestHandler):
    credential_provider = SimpleCredentialProvider(APP_ID, APP_PASSWORD)

    def __handle_conversation_update_activity(self, activity):
        self.send_response(202)
        self.end_headers()
        if activity.members_added[0].id != activity.recipient.id:
            credentials = MicrosoftAppCredentials(APP_ID, APP_PASSWORD)
            connector = ConnectorClient(credentials, base_url=activity.service_url)
            reply = Activity(
                type=ActivityTypes.message,
                channel_id=activity.channel_id,
                recipient=ChannelAccount(
                    id=activity.from_property.id,
                    name=activity.from_property.name),
                from_property=ChannelAccount(
                    id=activity.recipient.id,
                    name=activity.recipient.name),
                text='Hello and welcome to the echo bot!')
            connector.conversations.send_to_conversation(activity.conversation.id, reply)

    def __handle_message_activity(self, activity):
        self.send_response(200)
        self.end_headers()
        credentials = MicrosoftAppCredentials(APP_ID, APP_PASSWORD)
        connector = ConnectorClient(credentials, base_url=activity.service_url)
        reply = Activity(
            type=ActivityTypes.message,
            channel_id=activity.channel_id,
            recipient=ChannelAccount(id=activity.from_property.id),
            from_property=ChannelAccount(id=activity.recipient.id),
            text='You said: %s' % activity.text)
        connector.conversations.send_to_conversation(activity.conversation.id, reply)

    def __handle_authentication(self, activity):
        loop = asyncio.new_event_loop()
        try:
            loop.run_until_complete(JwtTokenValidation.assert_valid_activity(
                activity, self.headers.get("Authorization"), MyHandler.credential_provider))
            return True
        except Exception as ex:
            self.send_response(401, ex)
            self.end_headers()
            return False
        finally:
            loop.close()

    def __unhandled_activity(self):
        self.send_response(404)
        self.end_headers()

    def do_POST(self):
        body = self.rfile.read(int(self.headers['Content-Length']))
        data = json.loads(str(body, 'utf-8'))
        activity = Activity.deserialize(data)

        if not self.__handle_authentication(activity):
            return

        if activity.type == ActivityTypes.conversation_update.value:
            self.__handle_conversation_update_activity(activity)
        elif activity.type == ActivityTypes.message.value:
            self.__handle_message_activity(activity)
        else:
            self.__unhandled_activity()

try:
    SERVER = http.server.HTTPServer(('localhost', 9000), MyHandler)
    print('Started http server')
    SERVER.serve_forever()
except KeyboardInterrupt:
    print('^C received, shutting down server')
    SERVER.socket.close()
