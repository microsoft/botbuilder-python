# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
import uuid
from botbuilder.schema import (
    Activity,
    ActivityEventNames,
    ActivityTypes,
    ConversationReference,
)


def get_continuation_activity(reference: ConversationReference) -> Activity:
    return Activity(
        type=ActivityTypes.event,
        name=ActivityEventNames.continue_conversation,
        id=str(uuid.uuid1()),
        channel_id=reference.channel_id,
        service_url=reference.service_url,
        conversation=reference.conversation,
        recipient=reference.bot,
        from_property=reference.user,
        relates_to=reference,
    )
