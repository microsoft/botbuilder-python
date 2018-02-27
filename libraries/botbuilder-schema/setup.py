# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from setuptools import setup

NAME = "botbuilder-schema"
VERSION = "4.0.0-a0"
REQUIRES = ["msrest>=0.2.0"]

setup(
    name=NAME,
    version=VERSION,
    description="BotBouilder Schema",
    author="Microsoft",
    url="https://github.com/Microsoft/botbuilder-python",
    keywords=["BotBuilderSchema", "bots","ai", "botframework", "botbuilder"],
    long_description="This package contains the schema classes for using the Bot Framework.",
    license='MIT',
    install_requires=REQUIRES,
    packages=["botbuilder.schema"],
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python',
        'Intended Audience :: Bot Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ]
)
