# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List

from botbuilder.core import BotAdapter, TurnContext
from botbuilder.schema import Activity, ConversationReference, ResourceResponse


class NullAdapter(BotAdapter):
    """
    This is a BotAdapter that does nothing on the Send operation, equivalent to piping to /dev/null.
    """

    # pylint: disable=unused-argument

    async def send_activities(
        self, context: TurnContext, activities: List[Activity]
    ) -> List[ResourceResponse]:
        return [ResourceResponse()]

    async def update_activity(self, context: TurnContext, activity: Activity):
        raise NotImplementedError()

    async def delete_activity(
        self, context: TurnContext, reference: ConversationReference
    ):
        raise NotImplementedError()
