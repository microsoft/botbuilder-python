# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os
from setuptools import setup

REQUIRES = [
    "botbuilder-schema>=4.7.0",
    "botframework-connector>=4.7.0",
    "botbuilder-core>=4.7.0",
]

TEST_REQUIRES = ["aiounittest==1.3.0"]

root = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(root, "botbuilder", "adapters", "slack", "about.py")) as f:
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
    keywords=["BotBuilderAdapters", "bots", "ai", "botframework", "botbuilder"],
    long_description=long_description,
    long_description_content_type="text/x-rst",
    license=package_info["__license__"],
    packages=[
        "botbuilder.adapters",
        "botbuilder.adapters.slack",
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
