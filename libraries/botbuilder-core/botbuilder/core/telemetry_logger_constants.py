# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License


class TelemetryLoggerConstants:
    """The Telemetry Logger Event names."""

    # The name of the event when a new message is received from the user.
    BOT_MSG_RECEIVE_EVENT: str = "BotMessageReceived"

    # The name of the event when logged when a message is sent from the bot to the user.
    BOT_MSG_SEND_EVENT: str = "BotMessageSend"

    # The name of the event when a message is updated by the bot.
    BOT_MSG_UPDATE_EVENT: str = "BotMessageUpdate"

    # The name of the event when a message is deleted by the bot.
    BOT_MSG_DELETE_EVENT: str = "BotMessageDelete"
