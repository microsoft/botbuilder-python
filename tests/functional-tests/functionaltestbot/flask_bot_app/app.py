# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

"""Bot app with Flask routing."""

from flask import Response

from .bot_app import BotApp


APP = BotApp()


@APP.flask.route("/api/messages", methods=["POST"])
def messages() -> Response:
    return APP.messages()


@APP.flask.route("/api/test", methods=["GET"])
def test() -> Response:
    return APP.test()
