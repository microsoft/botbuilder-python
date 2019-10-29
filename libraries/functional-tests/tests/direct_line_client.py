# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Tuple

import requests
from requests import Response


class DirectLineClient:
    """A direct line client that sends and receives messages."""

    def __init__(self, direct_line_secret: str):
        self._direct_line_secret: str = direct_line_secret
        self._base_url: str = "https://directline.botframework.com/v3/directline"
        self._set_headers()
        self._start_conversation()
        self._watermark: str = ""

    def send_message(self, text: str, retry_count: int = 3) -> Response:
        """Send raw text to bot framework using direct line api"""

        url = "/".join(
            [self._base_url, "conversations", self._conversation_id, "activities"]
        )
        json_payload = {
            "conversationId": self._conversation_id,
            "type": "message",
            "from": {"id": "user1"},
            "text": text,
        }

        success = False
        current_retry = 0
        bot_response = None
        while not success and current_retry < retry_count:
            bot_response = requests.post(url, headers=self._headers, json=json_payload)
            current_retry += 1
            if bot_response.status_code == 200:
                success = True

        return bot_response

    def get_message(self, retry_count: int = 3) -> Tuple[Response, str]:
        """Get a response message back from the bot framework using direct line api"""

        url = "/".join(
            [self._base_url, "conversations", self._conversation_id, "activities"]
        )
        url = url + "?watermark=" + self._watermark

        success = False
        current_retry = 0
        bot_response = None
        while not success and current_retry < retry_count:
            bot_response = requests.get(
                url,
                headers=self._headers,
                json={"conversationId": self._conversation_id},
            )
            current_retry += 1
            if bot_response.status_code == 200:
                success = True
                json_response = bot_response.json()

                if "watermark" in json_response:
                    self._watermark = json_response["watermark"]

                if "activities" in json_response:
                    activities_count = len(json_response["activities"])
                    if activities_count > 0:
                        return (
                            bot_response,
                            json_response["activities"][activities_count - 1]["text"],
                        )
                    return bot_response, "No new messages"
        return bot_response, "error contacting bot for response"

    def _set_headers(self) -> None:
        headers = {"Content-Type": "application/json"}
        value = " ".join(["Bearer", self._direct_line_secret])
        headers.update({"Authorization": value})
        self._headers = headers

    def _start_conversation(self) -> None:
        # Start conversation and get us a conversationId to use
        url = "/".join([self._base_url, "conversations"])
        bot_response = requests.post(url, headers=self._headers)

        # Extract the conversationID for sending messages to bot
        json_response = bot_response.json()
        self._conversation_id = json_response["conversationId"]
