# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import aiounittest
from botbuilder.schema.teams import ConfigResponse


class TestConfigResponse(aiounittest.AsyncTestCase):
    def test_config_response_inits_with_no_args(self):
        config_response = ConfigResponse()

        self.assertIsNotNone(config_response)
        self.assertIsInstance(config_response, ConfigResponse)
