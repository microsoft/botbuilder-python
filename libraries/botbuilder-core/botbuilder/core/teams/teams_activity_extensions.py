from botbuilder.schema import Activity
from botbuilder.schema.teams import NotificationInfo, TeamsChannelData, TeamInfo

def teams_get_channel_id(activity: Activity) -> str:
    if not activity:
        return None

    if activity.channel_data:
        channel_data = TeamsChannelData().deserialize(activity.channel_data)
        return channel_data.channel.id if channel_data.channel else None

    return None


def teams_get_team_info(activity: Activity) -> TeamInfo:
    if not activity:
        return None

    if activity.channel_data:
        channel_data = TeamsChannelData().deserialize(activity.channel_data)
        return channel_data.team

    return None


def teams_notify_user(activity: Activity):
    if not activity:
        return

    if not activity.channel_data:
        activity.channel_data = {}

    channel_data = TeamsChannelData().deserialize(activity.channel_data)
    channel_data.notification = NotificationInfo(alert=True)
    activity.channel_data = channel_data
