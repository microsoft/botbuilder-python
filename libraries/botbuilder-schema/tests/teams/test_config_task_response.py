# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import aiounittest
from botbuilder.schema.teams import ConfigTaskResponse


class TestConfigTaskResponse(aiounittest.AsyncTestCase):
    def test_config_task_response_init_with_no_args(self):
        config_task_response = ConfigTaskResponse()

        self.assertIsNotNone(config_task_response)
        self.assertIsInstance(config_task_response, ConfigTaskResponse)
        self.assertEqual("config", config_task_response.response_type)
