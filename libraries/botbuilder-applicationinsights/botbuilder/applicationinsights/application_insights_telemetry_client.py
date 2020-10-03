# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
"""Application Insights Telemetry Client for Bots."""

import traceback
from typing import Dict, Callable

from applicationinsights import TelemetryClient  # pylint: disable=no-name-in-module
from botbuilder.core.bot_telemetry_client import (
    BotTelemetryClient,
    Severity,
    TelemetryDataPointType,
)

from .bot_telemetry_processor import BotTelemetryProcessor


def bot_telemetry_processor(data, context) -> bool:
    """Bot Telemetry Processor as a method for backward compatibility. Refer to
    callable object :class:`BotTelemetryProcessor` for details.

    :param data: Data from Application Insights
    :type data: telemetry item
    :param context: Context from Application Insights
    :type context: context object
    :return: determines if the event is passed to the server (False = Filtered).
    :rtype: bool
    """
    processor = BotTelemetryProcessor()
    return processor(data, context)


class ApplicationInsightsTelemetryClient(BotTelemetryClient):
    """Application Insights Telemetry Client."""

    def __init__(
        self,
        instrumentation_key: str,
        telemetry_client: TelemetryClient = None,
        telemetry_processor: Callable[[object, object], bool] = None,
        client_queue_size: int = None,
    ):
        self._instrumentation_key = instrumentation_key

        self._client = (
            telemetry_client
            if telemetry_client is not None
            else TelemetryClient(self._instrumentation_key)
        )
        if client_queue_size:
            self._client.channel.queue.max_queue_length = client_queue_size

        # Telemetry Processor
        processor = (
            telemetry_processor
            if telemetry_processor is not None
            else bot_telemetry_processor
        )
        self._client.add_telemetry_processor(processor)

    def track_pageview(
        self,
        name: str,
        url: str,
        duration: int = 0,
        properties: Dict[str, object] = None,
        measurements: Dict[str, object] = None,
    ) -> None:
        """
        Send information about the page viewed in the application (a web page for instance).

        :param name: the name of the page that was viewed.
        :type name: str
        :param url: the URL of the page that was viewed.
        :type url: str
        :param duration: the duration of the page view in milliseconds. (defaults to: 0)
        :duration: int
        :param properties: the set of custom properties the client wants attached to this data item. (defaults to: None)
        :type properties: :class:`typing.Dict[str, object]`
        :param measurements: the set of custom measurements the client wants to attach to this data item. (defaults to:
         None)
        :type measurements: :class:`typing.Dict[str, object]`
        """
        self._client.track_pageview(name, url, duration, properties, measurements)

    def track_exception(
        self,
        exception_type: type = None,
        value: Exception = None,
        trace: traceback = None,
        properties: Dict[str, object] = None,
        measurements: Dict[str, object] = None,
    ) -> None:
        """
        Send information about a single exception that occurred in the application.

        :param exception_type: the type of the exception that was thrown.
        :param value: the exception that the client wants to send.
        :param trace: the traceback information as returned by :func:`sys.exc_info`.
        :param properties: the set of custom properties the client wants attached to this data item. (defaults to: None)
        :type properties: :class:`typing.Dict[str, object]`
        :param measurements: the set of custom measurements the client wants to attach to this data item. (defaults to:
         None)
        :type measurements: :class:`typing.Dict[str, object]`
        """
        self._client.track_exception(
            exception_type, value, trace, properties, measurements
        )

    def track_event(
        self,
        name: str,
        properties: Dict[str, object] = None,
        measurements: Dict[str, object] = None,
    ) -> None:
        """
        Send information about a single event that has occurred in the context of the application.

        :param name: the data to associate to this event.
        :type name: str
        :param properties: the set of custom properties the client wants attached to this data item. (defaults to: None)
        :type properties: :class:`typing.Dict[str, object]`
        :param measurements: the set of custom measurements the client wants to attach to this data item. (defaults to:
         None)
        :type measurements: :class:`typing.Dict[str, object]`
        """
        self._client.track_event(name, properties=properties, measurements=measurements)

    def track_metric(
        self,
        name: str,
        value: float,
        tel_type: TelemetryDataPointType = None,
        count: int = None,
        min_val: float = None,
        max_val: float = None,
        std_dev: float = None,
        properties: Dict[str, object] = None,
    ) -> NotImplemented:
        """
        Send information about a single metric data point that was captured for the application.

        :param name: The name of the metric that was captured.
        :type name: str
        :param value: The value of the metric that was captured.
        :type value: float
        :param tel_type: The type of the metric. (defaults to: TelemetryDataPointType.aggregation`)
        :param count: the number of metrics that were aggregated into this data point. (defaults to: None)
        :type count: int
        :param min_val: the minimum of all metrics collected that were aggregated into this data point. (defaults to:
         None)
        :type min_val: float
        :param max_val: the maximum of all metrics collected that were aggregated into this data point. (defaults to:
         None)
        :type max_val: float
        :param std_dev: the standard deviation of all metrics collected that were aggregated into this data point.
         (defaults to: None)
        :type std_dev: float
        :param properties: the set of custom properties the client wants attached to this data item. (defaults to: None)
        :type properties: :class:`typing.Dict[str, object]`
        """
        self._client.track_metric(
            name, value, tel_type, count, min_val, max_val, std_dev, properties
        )

    def track_trace(
        self, name: str, properties: Dict[str, object] = None, severity: Severity = None
    ):
        """
        Sends a single trace statement.

        :param name: the trace statement.
        :type name: str
        :param properties: the set of custom properties the client wants attached to this data item. (defaults to: None)
        :type properties: :class:`typing.Dict[str, object]`
        :param severity: the severity level of this trace, one of DEBUG, INFO, WARNING, ERROR, CRITICAL
        """
        self._client.track_trace(name, properties, severity)

    def track_request(
        self,
        name: str,
        url: str,
        success: bool,
        start_time: str = None,
        duration: int = None,
        response_code: str = None,
        http_method: str = None,
        properties: Dict[str, object] = None,
        measurements: Dict[str, object] = None,
        request_id: str = None,
    ):
        """
        Sends a single request that was captured for the application.

        :param name: The name for this request. All requests with the same name will be grouped together.
        :type name: str
        :param url: The actual URL for this request (to show in individual request instances).
        :type url: str
        :param success: True if the request ended in success, False otherwise.
        :type success: bool
        :param start_time: the start time of the request. The value should look the same as the one returned by
         :func:`datetime.isoformat`. (defaults to: None)
        :type start_time: str
        :param duration: the number of milliseconds that this request lasted. (defaults to: None)
        :type duration: int
        :param response_code: the response code that this request returned. (defaults to: None)
        :type response_code: str
        :param http_method: the HTTP method that triggered this request. (defaults to: None)
        :type http_method: str
        :param properties: the set of custom properties the client wants attached to this data item. (defaults to: None)
        :type properties: :class:`typing.Dict[str, object]`
        :param measurements: the set of custom measurements the client wants to attach to this data item. (defaults to:
         None)
        :type measurements: :class:`typing.Dict[str, object]`
        :param request_id: the id for this request. If None, a new uuid will be generated. (defaults to: None)
        :type request_id: str
        """
        self._client.track_request(
            name,
            url,
            success,
            start_time,
            duration,
            response_code,
            http_method,
            properties,
            measurements,
            request_id,
        )

    def track_dependency(
        self,
        name: str,
        data: str,
        type_name: str = None,
        target: str = None,
        duration: int = None,
        success: bool = None,
        result_code: str = None,
        properties: Dict[str, object] = None,
        measurements: Dict[str, object] = None,
        dependency_id: str = None,
    ):
        """
        Sends a single dependency telemetry that was captured for the application.

        :param name: the name of the command initiated with this dependency call. Low cardinality value.
         Examples are stored procedure name and URL path template.
        :type name: str
        :param data: the command initiated by this dependency call. Examples are SQL statement and HTTP URL with all
         query parameters.
        :type data: str
        :param type_name: the dependency type name. Low cardinality value for logical grouping of dependencies and
         interpretation of other fields like commandName and resultCode. Examples are SQL, Azure table, and HTTP.
          (default to: None)
        :type type_name: str
        :param target: the target site of a dependency call. Examples are server name, host address. (default to: None)
        :type target: str
        :param duration: the number of milliseconds that this dependency call lasted. (defaults to: None)
        :type duration: int
        :param success: true if the dependency call ended in success, false otherwise. (defaults to: None)
        :type success: bool
        :param result_code: the result code of a dependency call. Examples are SQL error code and HTTP status code.
         (defaults to: None)
        :type result_code: str
        :param properties: the set of custom properties the client wants attached to this data item.
         (defaults to: None)
        :type properties: :class:`typing.Dict[str, object]`
        :param measurements: the set of custom measurements the client wants to attach to this data item.
         (defaults to: None)
        :type measurements: :class:`typing.Dict[str, object]`
        :param dependency_id: the id for this dependency call. If None, a new uuid will be generated.
         (defaults to: None)
        :type dependency_id: str
        """
        self._client.track_dependency(
            name,
            data,
            type_name,
            target,
            duration,
            success,
            result_code,
            properties,
            measurements,
            dependency_id,
        )

    def flush(self):
        """Flushes data in the queue. Data in the queue will be sent either immediately irrespective of what sender is
        being used.
        """
        self._client.flush()
