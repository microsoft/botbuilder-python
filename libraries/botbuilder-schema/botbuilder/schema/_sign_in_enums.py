# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from enum import Enum


class SignInConstants(str, Enum):
    # Name for the signin invoke to verify the 6-digit authentication code as part of sign-in.
    verify_state_operation_name = "signin/verifyState"
    # Name for signin invoke to perform a token exchange.
    token_exchange_operation_name = "signin/tokenExchange"
    # The EventActivity name when a token is sent to the bot.
    token_response_event_name = "tokens/response"
