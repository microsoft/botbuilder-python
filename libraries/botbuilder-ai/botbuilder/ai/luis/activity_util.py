# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from datetime import datetime

from botbuilder.schema import (
    Activity,
    ActivityTypes,
    ChannelAccount,
    ConversationAccount,
)


class ActivityUtil:
    @staticmethod
    def create_trace(
        turn_activity: Activity,
        name: str,
        value: object = None,
        value_type: str = None,
        label: str = None,
    ) -> Activity:
        """Creates a trace activity based on this activity.

        :param turn_activity:
        :type turn_activity: Activity
        :param name: The value to assign to the trace activity's <see cref="Activity.name"/> property.
        :type name: str
        :param value: The value to assign to the trace activity's <see cref="Activity.value"/> property., defaults
         to None
        :param value: object, optional
        :param value_type: The value to assign to the trace activity's <see cref="Activity.value_type"/> property,
         defaults to None
        :param value_type: str, optional
        :param label: The value to assign to the trace activity's <see cref="Activity.label"/> property, defaults
         to None
        :param label: str, optional
        :return: The created trace activity.
        :rtype: Activity
        """

        from_property = (
            ChannelAccount(
                id=turn_activity.recipient.id, name=turn_activity.recipient.name
            )
            if turn_activity.recipient is not None
            else ChannelAccount()
        )
        if value_type is None and value is not None:
            value_type = type(value).__name__

        reply = Activity(
            type=ActivityTypes.trace,
            timestamp=datetime.utcnow(),
            from_property=from_property,
            recipient=ChannelAccount(
                id=turn_activity.from_property.id, name=turn_activity.from_property.name
            ),
            reply_to_id=turn_activity.id,
            service_url=turn_activity.service_url,
            channel_id=turn_activity.channel_id,
            conversation=ConversationAccount(
                is_group=turn_activity.conversation.is_group,
                id=turn_activity.conversation.id,
                name=turn_activity.conversation.name,
            ),
            name=name,
            label=label,
            value_type=value_type,
            value=value,
        )
        return reply
