# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import aiounittest
from botbuilder.schema.teams import ReadReceiptInfo


class TestReadReceiptInfo(aiounittest.AsyncTestCase):
    def test_read_receipt_info(self):
        # Arrange
        test_cases = [
            ("1000", "1000", True),
            ("1001", "1000", True),
            ("1000", "1001", False),
            ("1000", None, False),
            (None, "1000", False),
        ]

        for last_read, compare, is_read in test_cases:
            # Act
            info = ReadReceiptInfo(last_read_message_id=last_read)

            # Assert
            self.assertEqual(info.last_read_message_id, last_read)
            self.assertEqual(info.is_message_read_instance(compare), is_read)
            self.assertEqual(
                ReadReceiptInfo.is_message_read(compare, last_read), is_read
            )
