# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from setuptools import setup

NAME = "botframework-connector"
VERSION = "4.0.0-a0"
REQUIRES = [
    "msrest>=0.2.0",
    "requests>=2.8.1",
    "cryptography>=2.1.4",
    "PyJWT>=1.5.3",
    "botbuilder-schema"]

setup(
    name=NAME,
    version=VERSION,
    description="Microsoft Bot Framework Bot Builder SDK for Python.",
    author='Microsoft',
    url="https://www.github.com/Microsoft/botbuilder-python",
    keywords=["BotFrameworkConnector", "bots","ai", "botframework", "botbuilder"],
    install_requires=REQUIRES,
    packages=["botframework.connector", "botframework.connector.auth", "botframework.connector.operations", "botframework.connector.models"],
    include_package_data=True,
    long_description="Microsoft Bot Framework Bot Builder SDK for Python.",
    license='MIT',
    classifiers=[
        'Programming Language :: Python',
        'Intended Audience :: Bot Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ]
)
