# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license.

from botbuilder.core import BotTelemetryClient, NullTelemetryClient


class LuisPredictionOptions(object):
    """
    Optional parameters for a LUIS prediction request.
    """

    def __init__(
        self,
        bing_spell_check_subscription_key: str = None,
        include_all_intents: bool = None,
        include_instance_data: bool = None,
        log: bool = None,
        spell_check: bool = None,
        staging: bool = None,
        timeout: float = 100000,
        timezone_offset: float = None,
        telemetry_client: BotTelemetryClient = NullTelemetryClient(),
        log_personal_information: bool = False,
    ):
        self._bing_spell_check_subscription_key: str = bing_spell_check_subscription_key
        self._include_all_intents: bool = include_all_intents
        self._include_instance_data: bool = include_instance_data
        self._log: bool = log
        self._spell_check: bool = spell_check
        self._staging: bool = staging
        self._timeout: float = timeout
        self._timezone_offset: float = timezone_offset
        self._telemetry_client: BotTelemetryClient = telemetry_client
        self._log_personal_information: bool = log_personal_information

    @property
    def bing_spell_check_subscription_key(self) -> str:
        """Gets the Bing Spell Check subscription key.
        
        :return: The Bing Spell Check subscription key.
        :rtype: str
        """

        return self._bing_spell_check_subscription_key

    @bing_spell_check_subscription_key.setter
    def bing_spell_check_subscription_key(self, value: str) -> None:
        """Sets the Bing Spell Check subscription key.
        
        :param value: The Bing Spell Check subscription key.
        :type value: str
        :return:
        :rtype: None
        """

        self._bing_spell_check_subscription_key = value

    @property
    def include_all_intents(self) -> bool:
        """Gets whether all intents come back or only the top one.
        
        :return: True for returning all intents.
        :rtype: bool
        """

        return self._include_all_intents

    @include_all_intents.setter
    def include_all_intents(self, value: bool) -> None:
        """Sets whether all intents come back or only the top one.
        
        :param value: True for returning all intents.
        :type value: bool
        :return:
        :rtype: None
        """

        self._include_all_intents = value

    @property
    def include_instance_data(self) -> bool:
        """Gets a value indicating whether or not instance data should be included in response.
        
        :return: A value indicating whether or not instance data should be included in response.
        :rtype: bool
        """

        return self._include_instance_data

    @include_instance_data.setter
    def include_instance_data(self, value: bool) -> None:
        """Sets a value indicating whether or not instance data should be included in response.
        
        :param value: A value indicating whether or not instance data should be included in response.
        :type value: bool
        :return:
        :rtype: None
        """

        self._include_instance_data = value

    @property
    def log(self) -> bool:
        """Gets if queries should be logged in LUIS.
        
        :return: If queries should be logged in LUIS.
        :rtype: bool
        """

        return self._log

    @log.setter
    def log(self, value: bool) -> None:
        """Sets if queries should be logged in LUIS.
        
        :param value: If queries should be logged in LUIS.
        :type value: bool
        :return:
        :rtype: None
        """

        self._log = value

    @property
    def spell_check(self) -> bool:
        """Gets whether to spell check queries.
        
        :return: Whether to spell check queries.
        :rtype: bool
        """

        return self._spell_check

    @spell_check.setter
    def spell_check(self, value: bool) -> None:
        """Sets whether to spell check queries.
        
        :param value: Whether to spell check queries.
        :type value: bool
        :return:
        :rtype: None
        """

        self._spell_check = value

    @property
    def staging(self) -> bool:
        """Gets whether to use the staging endpoint.
        
        :return: Whether to use the staging endpoint.
        :rtype: bool
        """

        return self._staging

    @staging.setter
    def staging(self, value: bool) -> None:
        """Sets whether to use the staging endpoint.

        
        :param value: Whether to use the staging endpoint.
        :type value: bool
        :return:
        :rtype: None
        """

        self._staging = value

    @property
    def timeout(self) -> float:
        """Gets the time in milliseconds to wait before the request times out.
        
        :return: The time in milliseconds to wait before the request times out. Default is 100000 milliseconds.
        :rtype: float
        """

        return self._timeout

    @timeout.setter
    def timeout(self, value: float) -> None:
        """Sets the time in milliseconds to wait before the request times out.
        
        :param value: The time in milliseconds to wait before the request times out. Default is 100000 milliseconds.
        :type value: float
        :return:
        :rtype: None
        """

        self._timeout = value

    @property
    def timezone_offset(self) -> float:
        """Gets the time zone offset.
        
        :return: The time zone offset.
        :rtype: float
        """

        return self._timezone_offset

    @timezone_offset.setter
    def timezone_offset(self, value: float) -> None:
        """Sets the time zone offset.
        
        :param value: The time zone offset.
        :type value: float
        :return:
        :rtype: None
        """

        self._timezone_offset = value

    @property
    def telemetry_client(self) -> BotTelemetryClient:
        """Gets the BotTelemetryClient used to log the LuisResult event.
        
        :return: The client used to log telemetry events.
        :rtype: BotTelemetryClient
        """

        return self._telemetry_client

    @telemetry_client.setter
    def telemetry_client(self, value: BotTelemetryClient) -> None:
        """Sets the BotTelemetryClient used to log the LuisResult event.
        
        :param value: The client used to log telemetry events.
        :type value: BotTelemetryClient
        :return:
        :rtype: None
        """

        self._telemetry_client = value

    @property
    def log_personal_information(self) -> bool:
        """Gets a value indicating whether to log personal information that came from the user to telemetry.
        
        :return: If true, personal information is logged to Telemetry; otherwise the properties will be filtered.
        :rtype: bool
        """

        return self._log_personal_information

    @log_personal_information.setter
    def log_personal_information(self, value: bool) -> None:
        """Sets a value indicating whether to log personal information that came from the user to telemetry.
        
        :param value: If true, personal information is logged to Telemetry; otherwise the properties will be filtered.
        :type value: bool
        :return:
        :rtype: None
        """

        self.log_personal_information = value
