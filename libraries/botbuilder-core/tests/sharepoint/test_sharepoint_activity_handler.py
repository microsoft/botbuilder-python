# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

# pylint: disable=too-many-lines
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from typing import List
import aiounittest
from botbuilder.schema.sharepoint import AceRequest
from botbuilder.core import TurnContext
from botbuilder.core.sharepoint import SharePointActivityHandler
from botbuilder.schema import (
    Activity,
    ActivityTypes,
)
from simple_adapter import SimpleAdapter


class TestingSharePointActivityHandler(SharePointActivityHandler):
    __test__ = False

    def __init__(self):
        self.record: List[str] = []

    async def on_sharepoint_task_get_card_view(
        self, turn_context: TurnContext, request: AceRequest
    ):
        self.record.append("on_sharepoint_task_get_card_view")
        return await super().on_sharepoint_task_get_card_view(turn_context, request)

    async def on_sharepoint_task_get_property_pane_configuration(
        self, turn_context: TurnContext, request: AceRequest
    ):
        self.record.append("on_sharepoint_task_get_property_pane_configuration")
        return await super().on_sharepoint_task_get_property_pane_configuration(
            turn_context, request
        )

    async def on_sharepoint_task_get_quick_view(
        self, turn_context: TurnContext, request: AceRequest
    ):
        self.record.append("on_sharepoint_task_get_quick_view")
        return await super().on_sharepoint_task_get_quick_view(turn_context, request)

    async def on_sharepoint_task_set_property_pane_configuration(
        self, turn_context: TurnContext, request: AceRequest
    ):
        self.record.append("on_sharepoint_task_set_property_pane_configuration")
        return await super().on_sharepoint_task_set_property_pane_configuration(
            turn_context, request
        )

    async def on_sharepoint_task_handle_action(
        self, turn_context: TurnContext, request: AceRequest
    ):
        self.record.append("on_sharepoint_task_handle_action")
        return await super().on_sharepoint_task_handle_action(turn_context, request)


class TestSharePointActivityHandler(aiounittest.AsyncTestCase):
    async def test_on_sharepoint_task_get_card_view(self):
        # Arrange
        activity = Activity(
            type=ActivityTypes.invoke,
            name="cardExtension/getCardView",
            value=AceRequest(),
        )
        turn_context = TurnContext(SimpleAdapter(), activity)

        # Act
        bot = TestingSharePointActivityHandler()
        await bot.on_turn(turn_context)

        # Assert
        self.assertEqual(1, len(bot.record))
        self.assertEqual(bot.record, ["on_sharepoint_task_get_card_view"])

    async def test_on_sharepoint_task_get_property_pane_configuration(self):
        # Arrange
        activity = Activity(
            type=ActivityTypes.invoke,
            name="cardExtension/getPropertyPaneConfiguration",
            value=AceRequest(),
        )
        turn_context = TurnContext(SimpleAdapter(), activity)

        # Act
        bot = TestingSharePointActivityHandler()
        await bot.on_turn(turn_context)

        # Assert
        self.assertEqual(1, len(bot.record))
        self.assertEqual(
            bot.record, ["on_sharepoint_task_get_property_pane_configuration"]
        )

    async def test_on_sharepoint_task_get_quick_view(self):
        # Arrange
        activity = Activity(
            type=ActivityTypes.invoke,
            name="cardExtension/getQuickView",
            value=AceRequest(),
        )
        turn_context = TurnContext(SimpleAdapter(), activity)

        # Act
        bot = TestingSharePointActivityHandler()
        await bot.on_turn(turn_context)

        # Assert
        self.assertEqual(1, len(bot.record))
        self.assertEqual(bot.record, ["on_sharepoint_task_get_quick_view"])

    async def test_on_sharepoint_task_set_property_pane_configuration(self):
        # Arrange
        activity = Activity(
            type=ActivityTypes.invoke,
            name="cardExtension/setPropertyPaneConfiguration",
            value=AceRequest(),
        )
        turn_context = TurnContext(SimpleAdapter(), activity)

        # Act
        bot = TestingSharePointActivityHandler()
        await bot.on_turn(turn_context)

        # Assert
        self.assertEqual(1, len(bot.record))
        self.assertEqual(
            bot.record, ["on_sharepoint_task_set_property_pane_configuration"]
        )

    async def test_on_sharepoint_task_handle_action(self):
        # Arrange
        activity = Activity(
            type=ActivityTypes.invoke,
            name="cardExtension/handleAction",
            value=AceRequest(),
        )
        turn_context = TurnContext(SimpleAdapter(), activity)

        # Act
        bot = TestingSharePointActivityHandler()
        await bot.on_turn(turn_context)

        # Assert
        self.assertEqual(1, len(bot.record))
        self.assertEqual(bot.record, ["on_sharepoint_task_handle_action"])
