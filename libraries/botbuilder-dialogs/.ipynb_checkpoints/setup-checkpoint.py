# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os
from setuptools import setup

REQUIRES = [
    "regex<=2019.08.19",
    "emoji==1.7.0",
    "recognizers-text-date-time>=1.0.2a1",
    "recognizers-text-number-with-unit>=1.0.2a1",
    "recognizers-text-number>=1.0.2a1",
    "recognizers-text>=1.0.2a1",
    "recognizers-text-choice>=1.0.2a1",
    "babel==2.9.1",
    "botbuilder-schema==4.15.0",
    "botframework-connector==4.15.0",
    "botbuilder-core==4.15.0",
]

TEST_REQUIRES = ["aiounittest==1.3.0"]

root = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(root, "botbuilder", "dialogs", "about.py")) as f:
    package_info = {}
    info = f.read()
    exec(info, package_info)

with open(os.path.join(root, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name=package_info["__title__"],
    version=package_info["__version__"],
    url=package_info["__uri__"],
    author=package_info["__author__"],
    description=package_info["__description__"],
    keywords=["BotBuilderDialogs", "bots", "ai", "botframework", "botbuilder"],
    long_description=long_description,
    long_description_content_type="text/x-rst",
    license=package_info["__license__"],
    packages=[
        "botbuilder.dialogs",
        "botbuilder.dialogs.prompts",
        "botbuilder.dialogs.choices",
        "botbuilder.dialogs.skills",
        "botbuilder.dialogs.memory",
        "botbuilder.dialogs.memory.path_resolvers",
        "botbuilder.dialogs.memory.scopes",
    ],
    install_requires=REQUIRES + TEST_REQUIRES,
    tests_require=TEST_REQUIRES,
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
