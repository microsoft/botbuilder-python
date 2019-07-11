# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from enum import Enum


class Channels(str, Enum):
    """
    Ids of channels supported by the Bot Builder.
    """

    console = "console"
    """Console channel."""

    cortana = "cortana"
    """Cortana channel."""

    direct_line = "directline"
    """Direct Line channel."""

    email = "email"
    """Email channel."""

    emulator = "emulator"
    """Emulator channel."""

    facebook = "facebook"
    """Facebook channel."""

    groupme = "groupme"
    """Group Me channel."""

    kik = "kik"
    """Kik channel."""

    line = "line"
    """Line channel."""

    ms_teams = "msteams"
    """MS Teams channel."""

    skype = "skype"
    """Skype channel."""

    skype_for_business = "skypeforbusiness"
    """Skype for Business channel."""

    slack = "slack"
    """Slack channel."""

    sms = "sms"
    """SMS (Twilio) channel."""

    telegram = "telegram"
    """Telegram channel."""

    webchat = "webchat"
    """WebChat channel."""
