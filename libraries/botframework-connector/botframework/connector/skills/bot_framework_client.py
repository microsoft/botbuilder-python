# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from abc import ABC, abstractmethod

# TODO: add InvokeResponse to botbuilder-schema or rethink dependencies
from botbuilder.schema import Activity


class BotFrameworkClient(ABC):
    @abstractmethod
    async def post_activity(
        self,
        from_bot_id: str,
        to_bot_id: str,
        to_url: str,
        service_url: str,
        conversation_id: str,
        activity: Activity,
    ) -> "botbuilder.core.InvokeResponse":
        """
        Forwards an activity to a another bot.

        :param from_bot_id: The MicrosoftAppId of the bot sending the activity.
        :param to_bot_id: The MicrosoftAppId of the bot receiving the activity.
        :param to_url: The URL of the bot receiving the activity.
        :param service_url: The callback Url for the skill host.
        :param conversation_id: A conversation ID to use for the conversation with the skill.
        :param activity: Activity to forward.
        """
        raise NotImplementedError()
