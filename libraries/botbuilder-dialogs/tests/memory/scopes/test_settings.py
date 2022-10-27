# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os


class DefaultConfig:
    """Bot Configuration"""

    STRING = os.environ.get("STRING", "test")
    INT = os.environ.get("INT", 3)
    LIST = os.environ.get("LIST", ["zero", "one", "two", "three"])
    NOT_TO_BE_OVERRIDDEN = os.environ.get("NOT_TO_BE_OVERRIDDEN", "one")
    TO_BE_OVERRIDDEN = os.environ.get("TO_BE_OVERRIDDEN", "one")
