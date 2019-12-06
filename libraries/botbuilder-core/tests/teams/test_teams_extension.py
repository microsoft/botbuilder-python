import aiounittest

from botbuilder.schema import Activity
from botbuilder.schema.teams import TeamInfo
from botbuilder.core.teams import (
    teams_get_channel_id,
    teams_get_team_info,
    teams_notify_user,
)


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
