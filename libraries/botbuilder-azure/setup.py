# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os
from setuptools import setup

REQUIRES = [
    "azure-cosmos==3.2.0",
    "azure-storage-blob==12.7.0",
    "botbuilder-schema==4.13.0",
    "botframework-connector==4.13.0",
    "jsonpickle>=1.2,<1.5",
]
TEST_REQUIRES = ["aiounittest==1.3.0"]

root = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(root, "botbuilder", "azure", "about.py")) as f:
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
    keywords=["BotBuilderAzure", "bots", "ai", "botframework", "botbuilder", "azure"],
    long_description=long_description,
    long_description_content_type="text/x-rst",
    license=package_info["__license__"],
    packages=["botbuilder.azure"],
    install_requires=REQUIRES + TEST_REQUIRES,
    tests_require=TEST_REQUIRES,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
