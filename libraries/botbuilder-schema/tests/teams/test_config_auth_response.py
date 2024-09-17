# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import aiounittest
from botbuilder.schema.teams import ConfigAuthResponse


class TestConfigAuthResponse(aiounittest.AsyncTestCase):
    def test_config_auth_response_init_with_no_args(self):
        config_auth_response = ConfigAuthResponse()

        self.assertIsNotNone(config_auth_response)
        self.assertIsInstance(config_auth_response, ConfigAuthResponse)
        self.assertEqual("config", config_auth_response.response_type)
