# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
import sys
import traceback
from applicationinsights import TelemetryClient
from botbuilder.core.bot_telemetry_client import BotTelemetryClient, TelemetryDataPointType
from typing import Dict

class AppinsightsBotTelemetryClient(BotTelemetryClient):

    def __init__(self, instrumentation_key:str):
        self._instrumentation_key = instrumentation_key

        self._context = TelemetryContext()
        context.instrumentation_key = self._instrumentation_key
        # context.user.id = 'BOTID'        # telemetry_channel.context.session.
        # context.session.id = 'BOTSESSION'

        # set up channel with context
        self._channel = TelemetryChannel(context)
        # telemetry_channel.context.properties['my_property'] = 'my_value'

        self._client = TelemetryClient(self._instrumentation_key, self._channel)
        
    
    def track_pageview(self, name: str, url:str, duration: int = 0, properties : Dict[str, object]=None, 
                        measurements: Dict[str, object]=None) -> None:
        """
        Send information about the page viewed in the application (a web page for instance).
        :param name: the name of the page that was viewed.
        :param url: the URL of the page that was viewed.
        :param duration: the duration of the page view in milliseconds. (defaults to: 0)
        :param properties: the set of custom properties the client wants attached to this data item. (defaults to: None)
        :param measurements: the set of custom measurements the client wants to attach to this data item. (defaults to: None)
        """
        self._client.track_pageview(name, url, duration, properties, measurements)
    
    def track_exception(self, type_exception: type = None, value : Exception =None, tb : traceback =None, 
                        properties: Dict[str, object]=None, measurements: Dict[str, object]=None) -> None:
        """ 
        Send information about a single exception that occurred in the application.
        :param type_exception: the type of the exception that was thrown.
        :param value: the exception that the client wants to send.
        :param tb: the traceback information as returned by :func:`sys.exc_info`.
        :param properties: the set of custom properties the client wants attached to this data item. (defaults to: None)
        :param measurements: the set of custom measurements the client wants to attach to this data item. (defaults to: None)
        """
        self._client.track_exception(type_exception, value, tb, properties, measurements)

    def track_event(self, name: str, properties: Dict[str, object] = None, 
                    measurements: Dict[str, object] = None) -> None:
        """ 
        Send information about a single event that has occurred in the context of the application.
        :param name: the data to associate to this event.
        :param properties: the set of custom properties the client wants attached to this data item. (defaults to: None)
        :param measurements: the set of custom measurements the client wants to attach to this data item. (defaults to: None)
        """
        self._client.track_event(name, properties, measurements)

    def track_metric(self, name: str, value: float, type: TelemetryDataPointType =None, 
                    count: int =None, min: float=None, max: float=None, std_dev: float=None,
                    properties: Dict[str, object]=None) -> NotImplemented:
        """
        Send information about a single metric data point that was captured for the application.
        :param name: The name of the metric that was captured.
        :param value: The value of the metric that was captured.
        :param type: The type of the metric. (defaults to: TelemetryDataPointType.aggregation`)
        :param count: the number of metrics that were aggregated into this data point. (defaults to: None)
        :param min: the minimum of all metrics collected that were aggregated into this data point. (defaults to: None)
        :param max: the maximum of all metrics collected that were aggregated into this data point. (defaults to: None)
        :param std_dev: the standard deviation of all metrics collected that were aggregated into this data point. (defaults to: None)
        :param properties: the set of custom properties the client wants attached to this data item. (defaults to: None)
        """
        self._client.track_metric(name, value, type, count, min, max, std_dev, properties)

    def track_trace(self, name: str, properties: Dict[str, object]=None, severity=None):
        """
        Sends a single trace statement.
        :param name: the trace statement.\n
        :param properties: the set of custom properties the client wants attached to this data item. (defaults to: None)\n
        :param severity: the severity level of this trace, one of DEBUG, INFO, WARNING, ERROR, CRITICAL
        """
        self._client.track_trace(name, properties, severity)

    def track_request(self, name: str, url: str, success: bool, start_time: str=None, 
                    duration: int=None, response_code: str =None, http_method: str=None, 
                    properties: Dict[str, object]=None, measurements: Dict[str, object]=None, 
                    request_id: str=None):
        """
        Sends a single request that was captured for the application.
        :param name: The name for this request. All requests with the same name will be grouped together.
        :param url: The actual URL for this request (to show in individual request instances).
        :param success: True if the request ended in success, False otherwise.
        :param start_time: the start time of the request. The value should look the same as the one returned by :func:`datetime.isoformat()` (defaults to: None)
        :param duration: the number of milliseconds that this request lasted. (defaults to: None)
        :param response_code: the response code that this request returned. (defaults to: None)
        :param http_method: the HTTP method that triggered this request. (defaults to: None)
        :param properties: the set of custom properties the client wants attached to this data item. (defaults to: None)
        :param measurements: the set of custom measurements the client wants to attach to this data item. (defaults to: None)
        :param request_id: the id for this request. If None, a new uuid will be generated. (defaults to: None)
        """
        self._client.track_request(name, url, success, start_time, duration, response_code, http_method, properties,
                                    measurements, request_id)

    def track_dependency(self, name:str, data:str, type:str=None, target:str=None, duration:int=None, 
                        success:bool=None, result_code:str=None, properties:Dict[str, object]=None, 
                        measurements:Dict[str, object]=None, dependency_id:str=None):
        """
        Sends a single dependency telemetry that was captured for the application.
        :param name: the name of the command initiated with this dependency call. Low cardinality value. Examples are stored procedure name and URL path template.
        :param data: the command initiated by this dependency call. Examples are SQL statement and HTTP URL with all query parameters.
        :param type: the dependency type name. Low cardinality value for logical grouping of dependencies and interpretation of other fields like commandName and resultCode. Examples are SQL, Azure table, and HTTP. (default to: None)
        :param target: the target site of a dependency call. Examples are server name, host address. (default to: None)
        :param duration: the number of milliseconds that this dependency call lasted. (defaults to: None)
        :param success: true if the dependency call ended in success, false otherwise. (defaults to: None)
        :param result_code: the result code of a dependency call. Examples are SQL error code and HTTP status code. (defaults to: None)
        :param properties: the set of custom properties the client wants attached to this data item. (defaults to: None)
        :param measurements: the set of custom measurements the client wants to attach to this data item. (defaults to: None)
        :param id: the id for this dependency call. If None, a new uuid will be generated. (defaults to: None)
        """
        self._client.track_dependency(name, data, type, target, duration, success, result_code, properties,
                                        measurements, dependency_id)

