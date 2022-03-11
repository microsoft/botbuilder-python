# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os
from setuptools import setup

NAME = "botframework-connector"
VERSION = os.environ["packageVersion"] if "packageVersion" in os.environ else "4.15.0"
REQUIRES = [
    "msrest==0.6.19",
    "requests>=2.23.0,<2.26",
    "PyJWT>=1.5.3,<2.0.0",
    "botbuilder-schema==4.15.0",
    "msal==1.17.0",
]

root = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(root, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name=NAME,
    version=VERSION,
    description="Microsoft Bot Framework Bot Builder SDK for Python.",
    author="Microsoft",
    url="https://www.github.com/Microsoft/botbuilder-python",
    keywords=["BotFrameworkConnector", "bots", "ai", "botframework", "botbuilder"],
    install_requires=REQUIRES,
    packages=[
        "botframework.connector",
        "botframework.connector.auth",
        "botframework.connector.async_mixin",
        "botframework.connector.operations",
        "botframework.connector.models",
        "botframework.connector.aio",
        "botframework.connector.aio.operations_async",
        "botframework.connector.skills",
        "botframework.connector.teams",
        "botframework.connector.teams.operations",
        "botframework.connector.token_api",
        "botframework.connector.token_api.aio",
        "botframework.connector.token_api.aio.operations_async",
        "botframework.connector.token_api.models",
        "botframework.connector.token_api.operations",
    ],
    include_package_data=True,
    long_description=long_description,
    long_description_content_type="text/x-rst",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
