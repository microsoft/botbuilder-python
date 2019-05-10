# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
import os
from setuptools import setup

NAME = "botframework-connector"
VERSION = os.environ["packageVersion"] if "packageVersion" in os.environ else "4.4.0b1"
REQUIRES = [
    "msrest>=0.6.6",
    "requests>=2.8.1",
    "cryptography>=2.1.4",
    "PyJWT>=1.5.3",
    "botbuilder-schema>=4.4.0b1"]

setup(
    name=NAME,
    version=VERSION,
    description="Microsoft Bot Framework Bot Builder SDK for Python.",
    author='Microsoft',
    url="https://www.github.com/Microsoft/botbuilder-python",
    keywords=["BotFrameworkConnector", "bots","ai", "botframework", "botbuilder"],
    install_requires=REQUIRES,
    packages=["botframework.connector",
              "botframework.connector.auth",
              "botframework.connector.async_mixin",
              "botframework.connector.operations",
              "botframework.connector.models",
              "botframework.connector.aio",
              "botframework.connector.aio.operations_async",
              "botframework.connector.token_api",
              "botframework.connector.token_api.aio",
              "botframework.connector.token_api.models",
              "botframework.connector.token_api.operations"
    ],
    include_package_data=True,
    long_description="Microsoft Bot Framework Bot Builder SDK for Python.",
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ]
)
