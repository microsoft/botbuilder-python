# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from msrest.pipeline import AsyncPipeline, AsyncHTTPPolicy, SansIOHTTPPolicy
from msrest.universal_http.async_requests import AsyncRequestsHTTPSender as Driver
from msrest.pipeline.async_requests import (
    AsyncRequestsCredentialsPolicy,
    AsyncPipelineRequestsHTTPSender,
)
from msrest.pipeline.universal import RawDeserializer

from .bot_framework_sdk_client_async import BotFrameworkConnectorConfiguration


class AsyncBfPipeline(AsyncPipeline):
    def __init__(self, config: BotFrameworkConnectorConfiguration):
        creds = config.credentials

        policies = [
            config.user_agent_policy,  # UserAgent policy
            RawDeserializer(),  # Deserialize the raw bytes
            config.http_logger_policy,  # HTTP request/response log
        ]  # type: List[Union[AsyncHTTPPolicy, SansIOHTTPPolicy]]
        if creds:
            if isinstance(creds, (AsyncHTTPPolicy, SansIOHTTPPolicy)):
                policies.insert(1, creds)
            else:
                # Assume this is the old credentials class, and then requests. Wrap it.
                policies.insert(1, AsyncRequestsCredentialsPolicy(creds))

        sender = config.sender or AsyncPipelineRequestsHTTPSender(
            config.driver or Driver(config)
        )
        super().__init__(policies, sender)
