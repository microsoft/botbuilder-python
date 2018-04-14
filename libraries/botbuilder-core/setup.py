# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from setuptools import setup

NAME = "botbuilder-core"
VERSION = "4.0.0.a2"
REQUIRES = [
    "botbuilder-schema>=4.0.0.a2",
    "botframework-connector>=4.0.0.a2"]

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
        'Programming Language :: Python :: 3.6',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ]
)
