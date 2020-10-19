# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.schema import Activity
from botbuilder.schema.teams import (
    NotificationInfo,
    TeamsChannelData,
    TeamInfo,
    TeamsMeetingInfo,
)


def teams_get_channel_data(activity: Activity) -> TeamsChannelData:
    if not activity:
        return None

    if activity.channel_data:
        return TeamsChannelData().deserialize(activity.channel_data)

    return None


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


def teams_notify_user(
    activity: Activity, alert_in_meeting: bool = None, external_resource_url: str = None
):
    if not activity:
        return

    if not activity.channel_data:
        activity.channel_data = {}

    channel_data = TeamsChannelData().deserialize(activity.channel_data)
    channel_data.notification = NotificationInfo(alert=True)
    channel_data.notification.alert_in_meeting = alert_in_meeting
    channel_data.notification.external_resource_url = external_resource_url
    activity.channel_data = channel_data


def teams_get_meeting_info(activity: Activity) -> TeamsMeetingInfo:
    if not activity:
        return None

    if activity.channel_data:
        channel_data = TeamsChannelData().deserialize(activity.channel_data)
        return channel_data.meeting

    return None
