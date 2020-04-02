# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import platform
from datetime import datetime
from logging import Logger
from typing import Dict

from botbuilder.core import Bot
from botbuilder.streaming import RequestHandler, __title__, __version__
from botbuilder.streaming.transport.web_socket import WebSocket

from .streaming_activity_processor import StreamingActivityProcessor


class StreamingRequestHandler(RequestHandler):
    def __init__(self, bot: Bot, activity_processor: StreamingActivityProcessor, web_socket: WebSocket, logger: Logger = None):
        if not bot:
            raise TypeError("'bot' argument can not be None")
        if not activity_processor:
            raise TypeError("'activity_processor' argument can not be None")

        self._bot = bot
        self._activity_processor = activity_processor
        self._logger = logger
        self._conversations: Dict[str, datetime] = {}
        self._user_agent = StreamingRequestHandler._get_user_agent()
        self._server =

    @staticmethod
    def _get_user_agent() -> str:
        package_user_agent = f"{__title__}/{__version__}"
        uname = platform.uname()
        os_version = f"{uname.machine}-{uname.system}-{uname.version}"
        py_version = f"Python,Version={platform.python_version()}"
        platform_user_agent = f"({os_version}; {py_version})"
        user_agent = f"{package_user_agent} {platform_user_agent}"
        return user_agent
