# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os
from setuptools import setup

NAME = "botbuilder-schema"
VERSION = os.environ["packageVersion"] if "packageVersion" in os.environ else "4.4.0b1"
REQUIRES = ["msrest==0.6.10"]

root = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(root, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name=NAME,
    version=VERSION,
    description="BotBuilder Schema",
    author="Microsoft",
    url="https://github.com/Microsoft/botbuilder-python",
    keywords=["BotBuilderSchema", "bots", "ai", "botframework", "botbuilder"],
    long_description=long_description,
    long_description_content_type="text/x-rst",
    license="MIT",
    install_requires=REQUIRES,
    packages=["botbuilder.schema"],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
