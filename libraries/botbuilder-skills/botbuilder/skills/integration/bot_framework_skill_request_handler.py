# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from typing import Awaitable, Callable, Tuple

from requests import Request

from botbuilder.core import Bot, BotAdapter
from botframework.connector.auth import ClaimsIdentity

from ..bot_framework_skill_client import BotFrameworkSkillClient

RouteAction = Callable[
    [BotAdapter, BotFrameworkSkillClient, Bot, ClaimsIdentity, Request, Tuple[str]],
    Awaitable[object],
]
