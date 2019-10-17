# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import json
import unittest
from typing import List, Tuple
from uuid import uuid4

from botbuilder.ai.luis import LuisApplication


class LuisApplicationTest(unittest.TestCase):
    endpoint: str = "https://westus.api.cognitive.microsoft.com"

    def test_luis_application_construction(self) -> None:
        model = LuisApplicationTest.get_valid_model()
        self.assertIsNotNone(model)

        construction_data: List[Tuple[str, str]] = [
            (None, str(uuid4())),
            ("", str(uuid4())),
            ("0000", str(uuid4())),
            (str(uuid4()), None),
            (str(uuid4()), ""),
            (str(uuid4()), "000"),
        ]

        for app_id, key in construction_data:
            with self.subTest(app_id=app_id, key=key):
                with self.assertRaises(ValueError):
                    LuisApplication(app_id, key, LuisApplicationTest.endpoint)

        luis_app = LuisApplication(
            str(uuid4()), str(uuid4()), LuisApplicationTest.endpoint
        )
        self.assertEqual(LuisApplicationTest.endpoint, luis_app.endpoint)

    @unittest.skip("revisit")
    def test_luis_application_serialization(self) -> None:
        model = LuisApplicationTest.get_valid_model()
        serialized = json.dumps(model)
        deserialized = json.loads(serialized)

        self.assertIsNotNone(deserialized)
        self.assertEqual(model, deserialized)

    def test_list_application_from_luis_endpoint(self) -> None:
        # Arrange
        # Note this is NOT a real LUIS application ID nor a real LUIS subscription-key
        # theses are GUIDs edited to look right to the parsing and validation code.
        endpoint = (
            "https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/"
            "b31aeaf3-3511-495b-a07f-571fc873214b?verbose=true&timezoneOffset=-360"
            "&subscription-key=048ec46dc58e495482b0c447cfdbd291&q="
        )

        # Act
        app = LuisApplication.from_application_endpoint(endpoint)

        # Assert
        self.assertEqual("b31aeaf3-3511-495b-a07f-571fc873214b", app.application_id)
        self.assertEqual("048ec46dc58e495482b0c447cfdbd291", app.endpoint_key)
        self.assertEqual("https://westus.api.cognitive.microsoft.com", app.endpoint)

    def test_list_application_from_luis_endpoint_bad_arguments(self) -> None:
        application_endpoint_data: List[str] = [
            "this.is.not.a.uri",
            "https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/"
            "b31aeaf3-3511-495b-a07f-571fc873214b?verbose=true&timezoneOffset=-360&q=",
            "https://westus.api.cognitive.microsoft.com?"
            "verbose=true&timezoneOffset=-360&subscription-key=048ec46dc58e495482b0c447cfdbd291&q=",
        ]

        for application_endpoint in application_endpoint_data:
            with self.subTest(application_endpoint=application_endpoint):
                with self.assertRaises(ValueError):
                    LuisApplication.from_application_endpoint(application_endpoint)

    @staticmethod
    def get_valid_model() -> LuisApplication:
        return LuisApplication(str(uuid4()), str(uuid4()), LuisApplicationTest.endpoint)
