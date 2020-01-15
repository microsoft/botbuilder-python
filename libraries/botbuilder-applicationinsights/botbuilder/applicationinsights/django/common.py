# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
"""Common utilities for Django middleware."""
import collections

from applicationinsights import TelemetryClient
from applicationinsights.channel import (
    AsynchronousQueue,
    AsynchronousSender,
    NullSender,
    SynchronousQueue,
    TelemetryChannel,
)

from ..processor.telemetry_processor import TelemetryProcessor
from .django_telemetry_processor import DjangoTelemetryProcessor


ApplicationInsightsSettings = collections.namedtuple(
    "ApplicationInsightsSettings",
    [
        "ikey",
        "channel_settings",
        "use_view_name",
        "record_view_arguments",
        "log_exceptions",
    ],
)

ApplicationInsightsChannelSettings = collections.namedtuple(
    "ApplicationInsightsChannelSettings", ["send_interval", "send_time", "endpoint"]
)


def load_settings():
    from django.conf import settings  # pylint: disable=import-outside-toplevel

    if hasattr(settings, "APPLICATION_INSIGHTS"):
        config = settings.APPLICATION_INSIGHTS
    elif hasattr(settings, "APPLICATIONINSIGHTS"):
        config = settings.APPLICATIONINSIGHTS
    else:
        config = {}

    if not isinstance(config, dict):
        config = {}

    return ApplicationInsightsSettings(
        ikey=config.get("ikey"),
        use_view_name=config.get("use_view_name", False),
        record_view_arguments=config.get("record_view_arguments", False),
        log_exceptions=config.get("log_exceptions", True),
        channel_settings=ApplicationInsightsChannelSettings(
            endpoint=config.get("endpoint"),
            send_interval=config.get("send_interval"),
            send_time=config.get("send_time"),
        ),
    )


saved_clients = {}  # pylint: disable=invalid-name
saved_channels = {}  # pylint: disable=invalid-name


def get_telemetry_client_with_processor(
    key: str, channel: TelemetryChannel, telemetry_processor: TelemetryProcessor = None
) -> TelemetryClient:
    """Gets a telemetry client instance with a telemetry processor.

    :param key: instrumentation key
    :type key: str
    :param channel: Telemetry channel
    :type channel: TelemetryChannel
    :param telemetry_processor: use an existing telemetry processor from caller.
    :type telemetry_processor: TelemetryProcessor
    :return: a telemetry client with telemetry processor.
    :rtype: TelemetryClient
    """
    client = TelemetryClient(key, channel)
    processor = (
        telemetry_processor
        if telemetry_processor is not None
        else DjangoTelemetryProcessor()
    )
    client.add_telemetry_processor(processor)
    return client


def create_client(aisettings=None, telemetry_processor: TelemetryProcessor = None):
    global saved_clients, saved_channels  # pylint: disable=invalid-name, global-statement

    if aisettings is None:
        aisettings = load_settings()

    if aisettings in saved_clients:
        return saved_clients[aisettings]

    channel_settings = aisettings.channel_settings

    if channel_settings in saved_channels:
        channel = saved_channels[channel_settings]
    else:
        sender = AsynchronousSender(service_endpoint_uri=channel_settings.endpoint)

        if channel_settings.send_time is not None:
            sender.send_time = channel_settings.send_time
        if channel_settings.send_interval is not None:
            sender.send_interval = channel_settings.send_interval

        queue = AsynchronousQueue(sender)
        channel = TelemetryChannel(None, queue)
        saved_channels[channel_settings] = channel

    ikey = aisettings.ikey
    if ikey is None:
        return dummy_client("No ikey specified", telemetry_processor)

    client = get_telemetry_client_with_processor(
        aisettings.ikey, channel, telemetry_processor
    )
    saved_clients[aisettings] = client
    return client


def dummy_client(
    reason: str, telemetry_processor: TelemetryProcessor = None
):  # pylint: disable=unused-argument
    """Creates a dummy channel so even if we're not logging telemetry, we can still send
    along the real object to things that depend on it to exist"""

    sender = NullSender()
    queue = SynchronousQueue(sender)
    channel = TelemetryChannel(None, queue)
    client = get_telemetry_client_with_processor(
        "00000000-0000-0000-0000-000000000000", channel, telemetry_processor
    )
    return client
