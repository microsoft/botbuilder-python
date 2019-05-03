# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os
from setuptools import setup

REQUIRES = [
    'applicationinsights>=0.11.9',
    'botbuilder-schema>=4.4.0b1',
    'botframework-connector>=4.4.0b1',
    'botbuilder-core>=4.4.0b1'
    ]
TESTS_REQUIRES = [
    'aiounittest>=1.1.0',
    'django>=2.2', # For samples
    'djangorestframework>=3.9.2', # For samples
    'flask>=1.0.2' # For samples
    ]

root = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(root, 'botbuilder', 'applicationinsights', 'about.py')) as f:
    package_info = {}
    info = f.read()
    exec(info, package_info)

setup(
    name=package_info['__title__'],
    version=package_info['__version__'],
    url=package_info['__uri__'],
    author=package_info['__author__'],
    description=package_info['__description__'],
    keywords=['BotBuilderApplicationInsights', 'bots', 'ai', 'botframework', 'botbuilder'],
    long_description=package_info['__summary__'],
    license=package_info['__license__'],
    packages=['botbuilder.applicationinsights','botbuilder.applicationinsights.django' ],
    install_requires=REQUIRES + TESTS_REQUIRES,
    tests_require=TESTS_REQUIRES,
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ]
)
