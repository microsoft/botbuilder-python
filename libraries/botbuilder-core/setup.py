# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from setuptools import setup

NAME = "botbuilder-core"
VERSION = "4.0.0-a0"
REQUIRES = [
    "botbuilder-schema",
    "botframework-connector"]

setup(
    name=NAME,
    version=VERSION,
    url='https://www.github.com/Microsoft/botbuilder-python',
    author='Microsoft',
    description='Microsoft Bot Framework Bot Builder',
    keywords=["BotBuilderCore", "bots","ai", "botframework", "botbuilder"],
    long_description='Microsoft Bot Framework Bot Builder SDK for Python.',
    license='MIT',
    packages=["botbuilder.core"],
    install_requires=REQUIRES,
    classifiers=[
        'Programming Language :: Python',
        'Intended Audience :: Bot Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ]
)
