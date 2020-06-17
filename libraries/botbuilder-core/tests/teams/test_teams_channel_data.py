# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import aiounittest

from botbuilder.schema import Activity
from botbuilder.schema.teams import TeamsChannelData
from botbuilder.core.teams import teams_get_team_info


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
