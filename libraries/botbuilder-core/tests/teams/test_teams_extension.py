# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from uuid import uuid4
import aiounittest

from botbuilder.schema import Activity
from botbuilder.schema.teams import TeamInfo
from botbuilder.core.teams import (
    teams_get_channel_id,
    teams_get_selected_channel_id,
    teams_get_team_info,
    teams_notify_user,
)
from botbuilder.core.teams.teams_activity_extensions import (
    teams_get_meeting_info,
    teams_get_team_on_behalf_of,
)
from botbuilder.schema.teams._models_py3 import OnBehalfOf


class TestTeamsActivityHandler(aiounittest.AsyncTestCase):
    def test_teams_get_channel_id(self):
        # Arrange
        activity = Activity(
            channel_data={"channel": {"id": "id123", "name": "channel_name"}}
        )

        # Act
        result = teams_get_channel_id(activity)

        # Assert
        assert result == "id123"

    def test_teams_get_selected_channel_id(self):
        # Arrange
        activity = Activity(
            channel_data={
                "channel": {"id": "id123", "name": "channel_name"},
                "settings": {
                    "selectedChannel": {"id": "id12345", "name": "channel_name"}
                },
            }
        )

        # Act
        result = teams_get_selected_channel_id(activity)

        # Assert
        assert result == "id12345"

    def test_teams_get_selected_channel_id_with_no_selected_channel(self):
        # Arrange
        activity = Activity(
            channel_data={"channel": {"id": "id123", "name": "channel_name"}}
        )

        # Act
        result = teams_get_selected_channel_id(activity)

        # Assert
        assert result is None

    def test_teams_get_channel_id_with_no_channel(self):
        # Arrange
        activity = Activity(
            channel_data={"team": {"id": "id123", "name": "channel_name"}}
        )

        # Act
        result = teams_get_channel_id(activity)

        # Assert
        assert result is None

    def test_teams_get_channel_id_with_no_channel_id(self):
        # Arrange
        activity = Activity(channel_data={"team": {"name": "channel_name"}})

        # Act
        result = teams_get_channel_id(activity)

        # Assert
        assert result is None

    def test_teams_get_channel_id_with_no_channel_data(self):
        # Arrange
        activity = Activity(type="type")

        # Act
        result = teams_get_channel_id(activity)

        # Assert
        assert result is None

    def test_teams_get_channel_id_with_none_activity(self):
        # Arrange
        activity = None

        # Act
        result = teams_get_channel_id(activity)

        # Assert
        assert result is None

    def test_teams_get_team_info(self):
        # Arrange
        activity = Activity(
            channel_data={"team": {"id": "id123", "name": "channel_name"}}
        )

        # Act
        result = teams_get_team_info(activity)

        # Assert
        assert result == TeamInfo(id="id123", name="channel_name")

    def test_teams_get_team_info_with_no_channel_data(self):
        # Arrange
        activity = Activity(type="type")

        # Act
        result = teams_get_team_info(activity)

        # Assert
        assert result is None

    def test_teams_get_team_info_with_no_team_info(self):
        # Arrange
        activity = Activity(channel_data={"eventType": "eventType"})

        # Act
        result = teams_get_team_info(activity)

        # Assert
        assert result is None

    def test_teams_get_team_info_with_none_activity(self):
        # Arrange
        activity = None

        # Act
        result = teams_get_team_info(activity)

        # Assert
        assert result is None

    def test_teams_notify_user(self):
        # Arrange
        activity = Activity(channel_data={"eventType": "eventType"})

        # Act
        teams_notify_user(activity)

        # Assert
        assert activity.channel_data.notification.alert

    def test_teams_notify_user_alert_in_meeting(self):
        # Arrange
        activity = Activity()

        # Act
        teams_notify_user(activity, alert_in_meeting=True)

        # Assert
        assert activity.channel_data.notification.alert_in_meeting is True
        assert activity.channel_data.notification.alert is False

    def test_teams_notify_user_with_no_activity(self):
        # Arrange
        activity = None

        # Act
        teams_notify_user(activity)

        # Assert
        assert activity is None

    def test_teams_notify_user_with_preexisting_notification(self):
        # Arrange
        activity = Activity(channel_data={"notification": {"alert": False}})

        # Act
        teams_notify_user(activity)

        # Assert
        assert activity.channel_data.notification.alert

    def test_teams_notify_user_with_no_channel_data(self):
        # Arrange
        activity = Activity(id="id123")

        # Act
        teams_notify_user(activity)

        # Assert
        assert activity.channel_data.notification.alert
        assert activity.id == "id123"

    def test_teams_meeting_info(self):
        # Arrange
        activity = Activity(channel_data={"meeting": {"id": "meeting123"}})

        # Act
        meeting_id = teams_get_meeting_info(activity).id

        # Assert
        assert meeting_id == "meeting123"

    def test_teams_channel_data_existing_on_behalf_of(self):
        # Arrange
        on_behalf_of_list = [
            OnBehalfOf(
                display_name="onBehalfOfTest",
                item_id=0,
                mention_type="person",
                mri=str(uuid4()),
            )
        ]

        activity = Activity(channel_data={"onBehalfOf": on_behalf_of_list})

        # Act
        on_behalf_of_list = teams_get_team_on_behalf_of(activity)

        # Assert
        self.assertEqual(1, len(on_behalf_of_list))
        self.assertEqual("onBehalfOfTest", on_behalf_of_list[0].display_name)
