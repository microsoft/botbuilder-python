# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
"""Package information."""
import os

__title__ = "functionaltestbot"
__version__ = (
    os.environ["packageVersion"] if "packageVersion" in os.environ else "0.0.1"
)
__uri__ = "https://www.github.com/Microsoft/botbuilder-python"
__author__ = "Microsoft"
__description__ = "Microsoft Bot Framework Bot Builder"
__summary__ = "Microsoft Bot Framework Bot Builder SDK for Python."
__license__ = "MIT"
