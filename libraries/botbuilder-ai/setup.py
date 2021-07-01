# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os
from setuptools import setup

REQUIRES = [
    "azure-cognitiveservices-language-luis==0.2.0",
    "botbuilder-schema==4.15.0",
    "botbuilder-core==4.15.0",
    "aiohttp>=3.6.2,<3.8.0",
]

TESTS_REQUIRES = ["aiounittest>=1.1.0"]

root = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(root, "botbuilder", "ai", "about.py")) as f:
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
    keywords="botbuilder-ai LUIS QnAMaker bots ai botframework botbuilder",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    license=package_info["__license__"],
    packages=[
        "botbuilder.ai",
        "botbuilder.ai.qna",
        "botbuilder.ai.luis",
        "botbuilder.ai.qna.models",
        "botbuilder.ai.qna.utils",
        "botbuilder.ai.qna.dialogs",
    ],
    install_requires=REQUIRES + TESTS_REQUIRES,
    tests_require=TESTS_REQUIRES,
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
