# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.schema import HealthCheckResponse, HealthResults
from botbuilder.core.bot_framework_adapter import USER_AGENT
from botframework.connector import ConnectorClient


class HealthCheck:
    @staticmethod
    def create_healthcheck_response(
        connector_client: ConnectorClient,
    ) -> HealthCheckResponse:
        # A derived class may override this, however, the default is that the bot is healthy given
        # we have got to here.
        health_results = HealthResults(success=True)

        if connector_client:
            health_results.authorization = "{} {}".format(
                "Bearer", connector_client.config.credentials.get_access_token()
            )
            health_results.user_agent = USER_AGENT

        success_message = "Health check succeeded."
        health_results.messages = (
            [success_message]
            if health_results.authorization
            else [success_message, "Callbacks are not authorized."]
        )

        return HealthCheckResponse(health_results=health_results)
