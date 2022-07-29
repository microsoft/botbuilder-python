# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
import base64
import json
from abc import ABC, abstractmethod
from _sha256 import sha256


class TelemetryProcessor(ABC):
    """Application Insights Telemetry Processor base class for Bot"""

    @property
    def activity_json(self) -> json:
        """Retrieve the request body as json (Activity)."""
        body_text = self.get_request_body()
        if body_text:
            return body_text if isinstance(body_text, dict) else json.loads(body_text)
        return None

    @abstractmethod
    def can_process(self) -> bool:
        """Whether the processor can process the request body.
        :return: True if the request body can be processed, False otherwise.
        :rtype: bool
        """
        return False

    @abstractmethod
    def get_request_body(self) -> str:  # pylint: disable=inconsistent-return-statements
        """Retrieve the request body from flask/django middleware component."""
        raise NotImplementedError()

    def __call__(self, data, context) -> bool:
        """Traditional Web user and session ID's don't apply for Bots.  This processor
        replaces the identifiers to be consistent with Bot Framework's notion of
        user and session id's.

        Each event that gets logged (with this processor added) will contain additional
        properties.

        The following properties are replaced:
        - context.user.id    - The user ID that Application Insights uses to identify
        a unique user.
        - context.session.id - The session ID that APplication Insights uses to
        identify a unique session.

        In addition, the additional data properties are added:
        - activityId - The Bot Framework's Activity ID which represents a unique
        message identifier.
        - channelId - The Bot Framework "Channel" (ie, slack/facebook/directline/etc)
        - activityType - The Bot Framework message classification (ie, message)

        :param data: Data from Application Insights
        :type data: telemetry item
        :param context: Context from Application Insights
        :type context: context object
        :returns:  bool -- determines if the event is passed to the server (False = Filtered).
        """

        post_data = self.activity_json
        if post_data is None:
            # If there is no body (not a BOT request or not configured correctly).
            # We *could* filter here, but we're allowing event to go through.
            return True

        # Override session and user id
        from_prop = post_data["from"] if "from" in post_data else None
        user_id = from_prop["id"] if from_prop is not None else None
        channel_id = post_data["channelId"] if "channelId" in post_data else None
        conversation = (
            post_data["conversation"] if "conversation" in post_data else None
        )

        session_id = ""
        if "id" in conversation:
            conversation_id = conversation["id"]
            session_id = base64.b64encode(
                sha256(conversation_id.encode("utf-8")).digest()
            ).decode()

        # Set the user id on the Application Insights telemetry item.
        context.user.id = channel_id + user_id

        # Set the session id on the Application Insights telemetry item.
        # Hashed ID is used due to max session ID length for App Insights session Id
        context.session.id = session_id

        # Set the activity id:
        # https://github.com/Microsoft/botframework-obi/blob/master/botframework-activity/botframework-activity.md#id
        if "id" in post_data:
            data.properties["activityId"] = post_data["id"]

        # Set the channel id:
        # https://github.com/Microsoft/botframework-obi/blob/master/botframework-activity/botframework-activity.md#channel-id
        if "channelId" in post_data:
            data.properties["channelId"] = post_data["channelId"]

        # Set the activity type:
        # https://github.com/Microsoft/botframework-obi/blob/master/botframework-activity/botframework-activity.md#type
        if "type" in post_data:
            data.properties["activityType"] = post_data["type"]

        return True
