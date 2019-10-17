# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import logging
import os

import django
from applicationinsights.channel import (
    AsynchronousSender,
    NullSender,
    SenderBase,
    SynchronousQueue,
    TelemetryChannel,
)
from applicationinsights.channel.SenderBase import (
    DEFAULT_ENDPOINT_URL as DEFAULT_ENDPOINT,
)
from botbuilder.applicationinsights.django import common
from django.test import TestCase, modify_settings, override_settings
from rest_framework.test import RequestsClient


# Note: MIDDLEWARE_CLASSES for django.VERSION <= (1, 10)
MIDDLEWARE_NAME = "MIDDLEWARE"
TEST_IKEY = "12345678-1234-5678-9012-123456789abc"
TEST_ENDPOINT = "https://test.endpoint/v2/track"
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))


class AITestCase(TestCase):
    def plug_sender(self):
        # Reset saved objects
        common.saved_clients = {}
        common.saved_channels = {}

        # Create a client and mock out the sender
        client = common.create_client()
        sender = MockSender()
        client._channel = TelemetryChannel(None, SynchronousQueue(sender))
        # client.add_telemetry_processor(bot_telemetry_processor)
        self.events = sender.events
        self.channel = client.channel

    def get_events(self, count):
        self.channel.flush()
        self.assertEqual(
            len(self.events),
            count,
            "Expected %d event(s) in queue (%d actual)" % (count, len(self.events)),
        )
        if count == 1:
            return self.events[0]
        return self.events


@modify_settings(
    **{
        MIDDLEWARE_NAME: {
            "append": "botbuilder.applicationinsights.django.ApplicationInsightsMiddleware",
            "prepend": "botbuilder.applicationinsights.django.BotTelemetryMiddleware",
        }
    }
)
@override_settings(
    APPLICATION_INSIGHTS={"ikey": TEST_IKEY},
    # Templates for 1.7
    TEMPLATE_DIRS=(PROJECT_ROOT,),
    TEMPLATE_LOADERS=("django.template.loaders.filesystem.Loader",),
    # Templates for 1.8 and up
    TEMPLATES=[
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [PROJECT_ROOT],
        }
    ],
)
class MiddlewareTests(AITestCase):
    def setUp(self):
        self.plug_sender()

    def test_basic_request(self):
        """Tests that hitting a simple view generates a telemetry item with the correct properties"""
        response = self.invoke_post("")
        assert response.status_code == 200

        event = self.get_events(1)
        tags = event["tags"]
        data = event["data"]["baseData"]
        self.assertEqual(
            event["name"], "Microsoft.ApplicationInsights.Request", "Event type"
        )
        self.assertEqual(event["iKey"], TEST_IKEY)
        self.assertEqual(tags["ai.operation.name"], "POST /", "Operation name")
        self.assertEqual(data["name"], "POST /", "Request name")
        self.assertEqual(data["responseCode"], 200, "Status code")
        self.assertEqual(data["success"], True, "Success value")
        self.assertEqual(data["url"], "http://testserver/", "Request url")
        self.assertEqual(tags["ai.user.id"], "SLACKFROMID")
        self.assertEqual(tags["ai.session.id"], "CONVERSATIONID")
        self.assertEqual(data["properties"]["channelId"], "SLACK", "channelId=SLACK")
        self.assertEqual(
            data["properties"]["activityId"], "bf3cc9a2f5de...", "activityID is set"
        )
        self.assertEqual(
            data["properties"]["activityType"], "message", "activityType == message"
        )

    def test_bot_event(self):
        """Tests that traces logged from inside of a view are submitted and parented to the request telemetry item"""
        response = self.invoke_post("botlog_event")
        assert response.status_code == 200

        logev, reqev = self.get_events(2)

        # Check request event (minimal, since we validate this elsewhere)
        tags = reqev["tags"]
        data = reqev["data"]["baseData"]
        reqid = tags["ai.operation.id"]
        self.assertEqual(
            reqev["name"], "Microsoft.ApplicationInsights.Request", "Event type"
        )
        self.assertEqual(data["id"], reqid, "Request id")
        self.assertEqual(data["name"], "POST /botlog_event", "Operation name")
        self.assertEqual(data["url"], "http://testserver/botlog_event", "Request url")

        self.assertTrue(reqid, "Request id not empty")

        # Check log event
        tags = logev["tags"]
        data = logev["data"]["baseData"]
        self.assertEqual(
            logev["name"], "Microsoft.ApplicationInsights.Event", "Event type"
        )
        self.assertEqual(logev["iKey"], TEST_IKEY)
        self.assertEqual(data["name"], "botevent", "validate event name")
        self.assertEqual(data["properties"]["foo"], "bar", "foo=bar")
        self.assertEqual(data["properties"]["moo"], "cow", "moo=cow")
        # Test TelemetryProcessor properties
        self.assertEqual(tags["ai.user.id"], "SLACKFROMID")
        self.assertEqual(tags["ai.session.id"], "CONVERSATIONID")
        self.assertEqual(data["properties"]["channelId"], "SLACK", "channelId=SLACK")
        self.assertEqual(
            data["properties"]["activityId"], "bf3cc9a2f5de...", "activityID is set"
        )
        self.assertEqual(
            data["properties"]["activityType"], "message", "activityType == message"
        )

    def test_logger(self):
        """Tests that traces logged from inside of a view are submitted and parented to the request telemetry item"""
        response = self.invoke_post("logger")
        self.assertEqual(response.status_code, 200)

        logev, reqev = self.get_events(2)

        # Check request event (minimal, since we validate this elsewhere)
        tags = reqev["tags"]
        data = reqev["data"]["baseData"]
        reqid = tags["ai.operation.id"]
        self.assertEqual(
            reqev["name"], "Microsoft.ApplicationInsights.Request", "Event type"
        )
        self.assertEqual(data["id"], reqid, "Request id")
        self.assertEqual(data["name"], "POST /logger", "Operation name")
        self.assertEqual(data["url"], "http://testserver/logger", "Request url")
        self.assertTrue(reqid, "Request id not empty")
        self.assertEqual(tags["ai.user.id"], "SLACKFROMID")
        self.assertEqual(tags["ai.session.id"], "CONVERSATIONID")
        self.assertEqual(data["properties"]["channelId"], "SLACK", "channelId=SLACK")
        self.assertEqual(
            data["properties"]["activityId"], "bf3cc9a2f5de...", "activityID is set"
        )
        self.assertEqual(
            data["properties"]["activityType"], "message", "activityType == message"
        )

        # Check log event
        tags = logev["tags"]
        data = logev["data"]["baseData"]
        self.assertEqual(
            logev["name"], "Microsoft.ApplicationInsights.Message", "Event type"
        )
        self.assertEqual(logev["iKey"], TEST_IKEY)
        self.assertEqual(tags["ai.operation.parentId"], reqid, "Parent id")
        self.assertEqual(data["message"], "Logger message", "Log message")
        self.assertEqual(data["properties"]["property"], "value", "Property=value")
        self.assertEqual(tags["ai.user.id"], "SLACKFROMID")
        self.assertEqual(tags["ai.session.id"], "CONVERSATIONID")
        self.assertEqual(data["properties"]["channelId"], "SLACK", "channelId=SLACK")
        self.assertEqual(
            data["properties"]["activityId"], "bf3cc9a2f5de...", "activityID is set"
        )
        self.assertEqual(
            data["properties"]["activityType"], "message", "activityType == message"
        )

    def test_thrower(self):
        """Tests that unhandled exceptions generate an exception telemetry item parented to the request telemetry item"""
        response = self.invoke_post("thrower")
        self.assertEqual(response.status_code, 500)

        errev, reqev = self.get_events(2)
        # reqev = self.get_events(1)

        # Check request event
        tags = reqev["tags"]
        data = reqev["data"]["baseData"]
        reqid = tags["ai.operation.id"]
        self.assertEqual(
            reqev["name"], "Microsoft.ApplicationInsights.Request", "Event type"
        )
        self.assertEqual(reqev["iKey"], TEST_IKEY)
        self.assertEqual(data["id"], reqid, "Request id")
        self.assertEqual(data["responseCode"], 500, "Response code")
        self.assertEqual(data["success"], False, "Success value")
        self.assertEqual(data["name"], "POST /thrower", "Request name")
        self.assertEqual(data["url"], "http://testserver/thrower", "Request url")
        self.assertTrue(reqid, "Request id not empty")
        self.assertEqual(tags["ai.user.id"], "SLACKFROMID")
        self.assertEqual(tags["ai.session.id"], "CONVERSATIONID")
        self.assertEqual(data["properties"]["channelId"], "SLACK", "channelId=SLACK")
        self.assertEqual(
            data["properties"]["activityId"], "bf3cc9a2f5de...", "activityID is set"
        )
        self.assertEqual(
            data["properties"]["activityType"], "message", "activityType == message"
        )

        # Check exception event
        tags = errev["tags"]
        data = errev["data"]["baseData"]
        self.assertEqual(
            errev["name"], "Microsoft.ApplicationInsights.Exception", "Event type"
        )
        self.assertEqual(tags["ai.operation.parentId"], reqid, "Exception parent id")
        self.assertEqual(len(data["exceptions"]), 1, "Exception count")
        exc = data["exceptions"][0]
        self.assertEqual(exc["typeName"], "ValueError", "Exception type")
        self.assertEqual(exc["hasFullStack"], True, "Has full stack")
        self.assertEqual(
            exc["parsedStack"][0]["method"], "thrower", "Stack frame method name"
        )
        self.assertEqual(tags["ai.user.id"], "SLACKFROMID")
        self.assertEqual(tags["ai.session.id"], "CONVERSATIONID")
        self.assertEqual(data["properties"]["channelId"], "SLACK", "channelId=SLACK")
        self.assertEqual(
            data["properties"]["activityId"], "bf3cc9a2f5de...", "activityID is set"
        )
        self.assertEqual(
            data["properties"]["activityType"], "message", "activityType == message"
        )

    def test_error(self):
        """Tests that Http404 exception does not generate an exception event
        and the request telemetry item properly logs the failure"""

        response = self.invoke_post("errorer")
        self.assertEqual(response.status_code, 404)

        event = self.get_events(1)
        tags = event["tags"]
        data = event["data"]["baseData"]
        self.assertEqual(
            event["name"], "Microsoft.ApplicationInsights.Request", "Event type"
        )
        self.assertEqual(tags["ai.operation.name"], "POST /errorer", "Operation name")
        self.assertEqual(data["responseCode"], 404, "Status code")
        self.assertEqual(data["success"], False, "Success value")
        self.assertEqual(data["url"], "http://testserver/errorer", "Request url")

    def test_template(self):
        """Tests that views using templates operate correctly and that template data is logged"""
        response = self.invoke_post("templater/ctx")
        self.assertEqual(response.status_code, 200)

        event = self.get_events(1)
        data = event["data"]["baseData"]
        self.assertEqual(
            event["name"], "Microsoft.ApplicationInsights.Request", "Event type"
        )
        self.assertEqual(data["success"], True, "Success value")
        self.assertEqual(data["responseCode"], 200, "Status code")
        self.assertEqual(
            data["properties"]["template_name"], "template.html", "Template name"
        )

    def test_no_view_arguments(self):
        """Tests that view id logging is off by default"""
        self.plug_sender()
        # response = self.client.get('/getid/24')
        response = self.invoke_post("getid/24")
        self.assertEqual(response.status_code, 200)

        event = self.get_events(1)
        data = event["data"]["baseData"]
        self.assertEqual(
            event["name"], "Microsoft.ApplicationInsights.Request", "Event type"
        )
        self.assertTrue(
            "properties" not in data or "view_arg_0" not in data["properties"]
        )

    def test_no_view(self):
        """Tests that requests to URLs not backed by views are still logged"""
        # response = self.client.get('/this/view/does/not/exist')
        response = self.invoke_post("this/view/does/not/exist")
        self.assertEqual(response.status_code, 404)

        event = self.get_events(1)
        tags = event["tags"]
        data = event["data"]["baseData"]
        self.assertEqual(
            event["name"], "Microsoft.ApplicationInsights.Request", "Event type"
        )
        self.assertEqual(data["responseCode"], 404, "Status code")
        self.assertEqual(data["success"], False, "Success value")
        self.assertEqual(data["name"], "POST /this/view/does/not/exist", "Request name")
        self.assertEqual(
            data["url"], "http://testserver/this/view/does/not/exist", "Request url"
        )

    def test_401_success(self):
        """Tests that a 401 status code is considered successful"""
        # response = self.client.get("/returncode/401")
        response = self.invoke_post("returncode/405")
        self.assertEqual(response.status_code, 405)

        event = self.get_events(1)
        tags = event["tags"]
        data = event["data"]["baseData"]
        self.assertEqual(
            event["name"], "Microsoft.ApplicationInsights.Request", "Event type"
        )
        self.assertEqual(
            tags["ai.operation.name"], "POST /returncode/405", "Operation name"
        )
        self.assertEqual(data["responseCode"], 405, "Status code")
        self.assertEqual(data["success"], False, "Success value")
        self.assertEqual(data["url"], "http://testserver/returncode/405", "Request url")

    def invoke_post(self, first_level_directory: str):
        client = RequestsClient()
        return client.post(
            f"http://localhost/{first_level_directory}",
            json={
                "type": "message",
                "id": "bf3cc9a2f5de...",
                "timestamp": "2016-10-19T20:17:52.2891902Z",
                "serviceUrl": "https://smba.trafficmanager.net/apis",
                "channelId": "SLACK",
                "from": {"id": "FROMID", "name": "user's name"},
                "conversation": {"id": "CONVERSATIONID", "name": "conversation's name"},
                "recipient": {"id": "RECIPIENTID", "name": "bot's name"},
                "text": "Haircut on Saturday",
            },
        )


@modify_settings(
    **{
        MIDDLEWARE_NAME: {
            "append": "botbuilder.applicationinsights.django.ApplicationInsightsMiddleware"
        }
    }
)
class RequestSettingsTests(AITestCase):
    # This type needs to plug the sender during the test -- doing it in setUp would have nil effect
    # because each method's override_settings wouldn't have happened by then.

    @override_settings(APPLICATION_INSIGHTS={"ikey": TEST_IKEY, "use_view_name": True})
    def test_use_view_name(self):
        """Tests that request names are set to view names when use_view_name=True"""
        self.plug_sender()
        self.client.get("/")
        event = self.get_events(1)
        self.assertEqual(
            event["data"]["baseData"]["name"], "GET aitest.views.home", "Request name"
        )
        self.assertEqual(
            event["tags"]["ai.operation.name"],
            "GET aitest.views.home",
            "Operation name",
        )

    @override_settings(APPLICATION_INSIGHTS={"ikey": TEST_IKEY, "use_view_name": False})
    def test_use_view_name_off(self):
        """Tests that request names are set to URLs when use_view_name=False"""
        self.plug_sender()
        self.client.get("/")
        event = self.get_events(1)
        self.assertEqual(event["data"]["baseData"]["name"], "GET /", "Request name")
        self.assertEqual(event["tags"]["ai.operation.name"], "GET /", "Operation name")

    @override_settings(APPLICATION_INSIGHTS={"ikey": TEST_IKEY, "use_view_name": True})
    def test_view_name_class(self):
        """Tests that classes can be correctly identified when use_view_name=True"""
        self.plug_sender()
        self.client.get("/class")
        event = self.get_events(1)
        self.assertEqual(
            event["data"]["baseData"]["name"],
            "GET aitest.views.classview",
            "Request name",
        )
        self.assertEqual(
            event["tags"]["ai.operation.name"],
            "GET aitest.views.classview",
            "Operation name",
        )

    @override_settings(APPLICATION_INSIGHTS=None)
    def test_appinsights_still_supplied(self):
        """Tests that appinsights is still added to requests even if APPLICATION_INSIGHTS is unspecified"""
        # This uses request.appinsights -- it will crash if it's not there.
        response = self.invoke_post("logger")
        self.assertEqual(response.status_code, 200)

    @override_settings(
        APPLICATION_INSIGHTS={"ikey": TEST_IKEY, "record_view_arguments": True}
    )
    def test_view_id(self):
        """Tests that view arguments are logged when record_view_arguments=True"""
        self.plug_sender()
        response = self.invoke_post("getid/24")
        self.assertEqual(response.status_code, 200)

        event = self.get_events(1)
        props = event["data"]["baseData"]["properties"]
        self.assertEqual(
            event["name"], "Microsoft.ApplicationInsights.Request", "Event type"
        )
        self.assertEqual(props["view_arg_0"], "24", "View argument")

    @override_settings(
        APPLICATION_INSIGHTS={"ikey": TEST_IKEY, "log_exceptions": False}
    )
    def test_log_exceptions_off(self):
        """Tests that exceptions are not logged when log_exceptions=False"""
        self.plug_sender()
        response = self.invoke_post("thrower")
        self.assertEqual(response.status_code, 500)

        event = self.get_events(1)
        data = event["data"]["baseData"]
        self.assertEqual(
            event["name"], "Microsoft.ApplicationInsights.Request", "Event type"
        )
        self.assertEqual(data["responseCode"], 500, "Response code")

    def invoke_post(self, first_level_directory: str):
        client = RequestsClient()
        return client.post(
            f"http://localhost/{first_level_directory}",
            json={
                "type": "message",
                "id": "bf3cc9a2f5de...",
                "timestamp": "2016-10-19T20:17:52.2891902Z",
                "serviceUrl": "https://smba.trafficmanager.net/apis",
                "channelId": "SLACK",
                "from": {"id": "FROMID", "name": "user's name"},
                "conversation": {"id": "CONVERSATIONID", "name": "conversation's name"},
                "recipient": {"id": "RECIPIENTID", "name": "bot's name"},
                "text": "Haircut on Saturday",
            },
        )


class SettingsTests(TestCase):
    def setUp(self):
        # Just clear out any cached objects
        common.saved_clients = {}
        common.saved_channels = {}

    def test_no_app_insights(self):
        """Tests that events are swallowed when APPLICATION_INSIGHTS is unspecified"""
        client = common.create_client()
        self.assertTrue(type(client.channel.sender) is NullSender)

    @override_settings(APPLICATION_INSIGHTS={"ikey": TEST_IKEY})
    def test_default_endpoint(self):
        """Tests that the default endpoint is used when endpoint is unspecified"""
        client = common.create_client()
        self.assertEqual(client.channel.sender.service_endpoint_uri, DEFAULT_ENDPOINT)

    @override_settings(
        APPLICATION_INSIGHTS={"ikey": TEST_IKEY, "endpoint": TEST_ENDPOINT}
    )
    def test_overridden_endpoint(self):
        """Tests that the endpoint is used when specified"""
        client = common.create_client()
        self.assertEqual(client.channel.sender.service_endpoint_uri, TEST_ENDPOINT)

    @override_settings(APPLICATION_INSIGHTS={"ikey": TEST_IKEY, "send_time": 999})
    def test_send_time(self):
        """Tests that send_time is propagated to sender"""
        client = common.create_client()
        self.assertEqual(client.channel.sender.send_time, 999)

    @override_settings(APPLICATION_INSIGHTS={"ikey": TEST_IKEY, "send_interval": 999})
    def test_send_interval(self):
        """Tests that send_interval is propagated to sender"""
        client = common.create_client()
        self.assertEqual(client.channel.sender.send_interval, 999)

    @override_settings(APPLICATION_INSIGHTS={"ikey": TEST_IKEY})
    def test_default_send_time(self):
        """Tests that send_time is equal to the default when it is unspecified"""
        client = common.create_client()
        self.assertEqual(
            client.channel.sender.send_time, AsynchronousSender().send_time
        )

    @override_settings(APPLICATION_INSIGHTS={"ikey": TEST_IKEY})
    def test_default_send_interval(self):
        """Tests that send_interval is equal to the default when it is unspecified"""
        client = common.create_client()
        self.assertEqual(
            client.channel.sender.send_interval, AsynchronousSender().send_interval
        )


@override_settings(
    LOGGING={
        "version": 1,
        "handlers": {
            "appinsights": {
                "class": "botbuilder.applicationinsights.django.LoggingHandler",
                "level": "INFO",
            }
        },
        "loggers": {__name__: {"handlers": ["appinsights"], "level": "INFO"}},
    },
    APPLICATION_INSIGHTS={"ikey": TEST_IKEY},
)
class LoggerTests(AITestCase):
    def setUp(self):
        self.plug_sender()

    def test_log_error(self):
        """Tests an error trace telemetry is properly sent"""
        django.setup()
        logger = logging.getLogger(__name__)
        msg = "An error log message"
        logger.error(msg)

        event = self.get_events(1)
        data = event["data"]["baseData"]
        props = data["properties"]
        self.assertEqual(
            event["name"], "Microsoft.ApplicationInsights.Message", "Event type"
        )
        self.assertEqual(event["iKey"], TEST_IKEY)
        self.assertEqual(data["message"], msg, "Log message")
        self.assertEqual(data["severityLevel"], 3, "Severity level")
        self.assertEqual(props["fileName"], "tests.py", "Filename property")
        self.assertEqual(props["level"], "ERROR", "Level property")
        self.assertEqual(props["module"], "tests", "Module property")

    def test_log_info(self):
        """Tests an info trace telemetry is properly sent"""
        django.setup()
        logger = logging.getLogger(__name__)
        msg = "An info message"
        logger.info(msg)

        event = self.get_events(1)
        data = event["data"]["baseData"]
        props = data["properties"]
        self.assertEqual(
            event["name"], "Microsoft.ApplicationInsights.Message", "Event type"
        )
        self.assertEqual(event["iKey"], TEST_IKEY)
        self.assertEqual(data["message"], msg, "Log message")
        self.assertEqual(data["severityLevel"], 1, "Severity level")
        self.assertEqual(props["fileName"], "tests.py", "Filename property")
        self.assertEqual(props["level"], "INFO", "Level property")
        self.assertEqual(props["module"], "tests", "Module property")


class MockSender(SenderBase):
    def __init__(self):
        SenderBase.__init__(self, DEFAULT_ENDPOINT)
        self.events = []

    def send(self, data):
        self.events.extend(a.write() for a in data)
