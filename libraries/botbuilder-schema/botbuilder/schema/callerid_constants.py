# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from enum import Enum


class CallerIdConstants(str, Enum):
    public_azure_channel = "urn:botframework:azure"
    """
    The caller ID for any Bot Framework channel.
    """

    us_gov_channel = "urn:botframework:azureusgov"
    """
    The caller ID for any Bot Framework US Government cloud channel.
    """

    bot_to_bot_prefix = "urn:botframework:aadappid:"
    """
    The caller ID prefix when a bot initiates a request to another bot.
    This prefix will be followed by the Azure Active Directory App ID of the bot that initiated the call.
    """
