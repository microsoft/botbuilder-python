# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from uuid import uuid4
import aiounittest

from botbuilder.schema import Activity
from botbuilder.schema.teams import TeamsChannelData
from botbuilder.core.teams import teams_get_team_info
from botbuilder.schema.teams._models_py3 import (
    ChannelInfo,
    NotificationInfo,
    OnBehalfOf,
    TeamInfo,
    TeamsChannelDataSettings,
    TeamsMeetingInfo,
    TenantInfo,
)


class TestTeamsChannelData(aiounittest.AsyncTestCase):
    def test_teams_aad_group_id_deserialize(self):
        # Arrange
        raw_channel_data = {"team": {"aadGroupId": "teamGroup123"}}

        # Act
        channel_data = TeamsChannelData().deserialize(raw_channel_data)

        # Assert
        assert channel_data.team.aad_group_id == "teamGroup123"

    def test_teams_get_team_info(self):
        # Arrange
        activity = Activity(channel_data={"team": {"aadGroupId": "teamGroup123"}})

        # Act
        team_info = teams_get_team_info(activity)

        # Assert
        assert team_info.aad_group_id == "teamGroup123"

    def test_teams_channel_data_inits(self):
        # Arrange
        channel = ChannelInfo(id="general", name="General")
        event_type = "eventType"
        team = TeamInfo(id="supportEngineers", name="Support Engineers")
        notification = NotificationInfo(alert=True)
        tenant = TenantInfo(id="uniqueTenantId")
        meeting = TeamsMeetingInfo(id="BFSE Stand Up")
        settings = TeamsChannelDataSettings(selected_channel=channel)
        on_behalf_of = [
            OnBehalfOf(
                display_name="onBehalfOfTest",
                item_id=0,
                mention_type="person",
                mri=str(uuid4()),
            )
        ]

        # Act
        channel_data = TeamsChannelData(
            channel=channel,
            event_type=event_type,
            team=team,
            notification=notification,
            tenant=tenant,
            meeting=meeting,
            settings=settings,
            on_behalf_of=on_behalf_of,
        )

        # Assert
        self.assertIsNotNone(channel_data)
        self.assertIsInstance(channel_data, TeamsChannelData)
        self.assertEqual(channel, channel_data.channel)
        self.assertEqual(event_type, channel_data.event_type)
        self.assertEqual(team, channel_data.team)
        self.assertEqual(notification, channel_data.notification)
        self.assertEqual(tenant, channel_data.tenant)
        self.assertEqual(meeting, channel_data.meeting)
        self.assertEqual(settings, channel_data.settings)
        self.assertEqual(on_behalf_of, channel_data.on_behalf_of)
        self.assertEqual(on_behalf_of[0].display_name, "onBehalfOfTest")
        self.assertEqual(on_behalf_of[0].mention_type, "person")
        self.assertIsNotNone(on_behalf_of[0].mri)
        self.assertEqual(on_behalf_of[0].item_id, 0)
