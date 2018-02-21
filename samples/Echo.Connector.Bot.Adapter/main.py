# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import http.server
import json
import asyncio
from microsoft.botbuilder.schema import (Activity, ActivityTypes, ChannelAccount)

from bot_framework_adapter import BotFrameworkAdapter
from receive_delegate import ReceiveDelegate

APP_ID = ''
APP_PASSWORD = ''


class MyHandler(http.server.BaseHTTPRequestHandler):

    @staticmethod
    def __create_reply_activity(request_activity: Activity, text: str):
        return Activity(
            type=ActivityTypes.message,
            channel_id=request_activity.channel_id,
            conversation=request_activity.conversation,
            recipient=ChannelAccount(
                id=request_activity.from_property.id,
                name=request_activity.from_property.name),
            from_property=ChannelAccount(
                id=request_activity.recipient.id,
                name=request_activity.recipient.name),
            text=text,
            service_url=request_activity.service_url)

    def __handle_conversation_update_activity(self, activity: Activity):
        self.send_response(202)
        self.end_headers()
        if activity.members_added[0].id != activity.recipient.id:
            self._adapter.send([MyHandler.__create_reply_activity(activity, 'Hello and welcome to the echo bot!')])

    def __handle_message_activity(self, activity: Activity):
        self.send_response(200)
        self.end_headers()
        self._adapter.send([MyHandler.__create_reply_activity(activity, 'You said: %s' % activity.text)])

    def __unhandled_activity(self):
        self.send_response(404)
        self.end_headers()

    def receive(self, activity: Activity):
        if activity.type == ActivityTypes.conversation_update.value:
            self.__handle_conversation_update_activity(activity)
        elif activity.type == ActivityTypes.message.value:
            self.__handle_message_activity(activity)
        else:
            self.__unhandled_activity()

    def do_POST(self):
        body = self.rfile.read(int(self.headers['Content-Length']))
        data = json.loads(str(body, 'utf-8'))
        activity = Activity.deserialize(data)
        self._adapter = BotFrameworkAdapter(APP_ID, APP_PASSWORD)
        self._adapter.on_receive = ReceiveDelegate(self)
        self._adapter.receive(self.headers.get("Authorization"), activity)


try:
    SERVER = http.server.HTTPServer(('localhost', 9000), MyHandler)
    print('Started http server')
    SERVER.serve_forever()
except KeyboardInterrupt:
    print('^C received, shutting down server')
    SERVER.socket.close()
