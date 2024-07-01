# ![Bot Framework SDK v4 Python](./doc/media/FrameWorkPython.png)

This repository contains code for the Python version of the [Microsoft Bot Framework SDK](https://github.com/Microsoft/botframework-sdk), which is part of the Microsoft Bot Framework - a comprehensive framework for building enterprise-grade conversational AI experiences.

This SDK enables developers to model conversation and build sophisticated bot applications using Python. SDKs for [JavaScript](https://github.com/Microsoft/botbuilder-js) and [.NET](https://github.com/Microsoft/botbuilder-dotnet) are also available.

To get started building bots using the SDK, see the [Azure Bot Service Documentation](https://docs.microsoft.com/en-us/azure/bot-service/?view=azure-bot-service-4.0).

For more information jump to a section below.

* [Build status](#build-status)
* [Packages](#packages)
* [Getting started](#getting-started)
* [Getting support and providing feedback](#getting-support-and-providing-feedback)
* [Contributing and our code of conduct](contributing-and-our-code-of-conduct)
* [Reporting security issues](#reporting-security-issues)

## Build Status

| Branch | Description        | Build Status | Coverage Status | Code Style |
 |----|---------------|--------------|-----------------|--|
| Main | 4.17.0 Builds | [![Build Status](https://fuselabs.visualstudio.com/SDK_v4/_apis/build/status/Python/Python-CI-PR-yaml?branchName=main)](https://fuselabs.visualstudio.com/SDK_v4/_build/latest?definitionId=771&branchName=main) | [![Coverage Status](https://coveralls.io/repos/github/microsoft/botbuilder-python/badge.svg?branch=HEAD)](https://coveralls.io/github/microsoft/botbuilder-python?branch=HEAD) | [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) |

## Packages

| Build | Released Package |
 |----|---------------|
| botbuilder-ai | [![PyPI version](https://badge.fury.io/py/botbuilder-ai.svg)](https://pypi.org/project/botbuilder-ai/) |
| botbuilder-applicationinsights | [![PyPI version](https://badge.fury.io/py/botbuilder-applicationinsights.svg)](https://pypi.org/project/botbuilder-applicationinsights/) |
| botbuilder-azure | [![PyPI version](https://badge.fury.io/py/botbuilder-azure.svg)](https://pypi.org/project/botbuilder-azure/) |
| botbuilder-core | [![PyPI version](https://badge.fury.io/py/botbuilder-core.svg)](https://pypi.org/project/botbuilder-core/) |
| botbuilder-dialogs | [![PyPI version](https://badge.fury.io/py/botbuilder-dialogs.svg)](https://pypi.org/project/botbuilder-dialogs/) |
| botbuilder-schema | [![PyPI version](https://badge.fury.io/py/botbuilder-schema.svg)](https://pypi.org/project/botbuilder-schema/) |
| botframework-connector | [![PyPI version](https://badge.fury.io/py/botframework-connector.svg)](https://pypi.org/project/botframework-connector/) |
|

## Getting Started
To get started building bots using the SDK, see the [Azure Bot Service Documentation](https://docs.microsoft.com/en-us/azure/bot-service/?view=azure-bot-service-4.0).

The [Bot Framework Samples](https://github.com/microsoft/botbuilder-samples) includes a rich set of samples repository.

If you want to debug an issue, would like to [contribute](#contributing-code), or understand how the Bot Builder SDK works, instructions for building and testing the SDK are below.

### Prerequisites
- [Git](https://git-scm.com/downloads)
- [Python 3.8.17 - 3.11.x](https://www.python.org/downloads/)

Python "Virtual Environments" allow Python packages to be installed in an isolated location for a particular application, rather than being installed globally, as such it is common practice to use them. Click [here](https://packaging.python.org/tutorials/installing-packages/#creating-virtual-environments) to learn more about creating _and activating_ Virtual Environments in Python.

### Clone
Clone a copy of the repo:
```bash
git clone https://github.com/Microsoft/botbuilder-python.git
```
Change to the SDK's directory:
```bash
cd botbuilder-python
```

### Using the SDK locally

To use a local copy of the SDK you can link to these packages with the pip -e option.

```bash
pip install -e ./libraries/botbuilder-schema
pip install -e ./libraries/botframework-connector
pip install -e ./libraries/botframework-streaming
pip install -e ./libraries/botbuilder-core
pip install -e ./libraries/botbuilder-ai
pip install -e ./libraries/botbuilder-applicationinsights
pip install -e ./libraries/botbuilder-dialogs
pip install -e ./libraries/botbuilder-azure
pip install -e ./libraries/botbuilder-integration-applicationinsights-aiohttp
pip install -e ./libraries/botbuilder-adapters-slack
pip install -e ./libraries/botbuilder-integration-aiohttp
pip install -e ./libraries/botbuilder-testing
```

### Running unit tests
First execute the following command from the root level of the repo:
```bash
pip install -r ./libraries/botframework-connector/tests/requirements.txt
pip install -r ./libraries/botbuilder-core/tests/requirements.txt
pip install -r ./libraries/botbuilder-ai/tests/requirements.txt
```

Then enter run pytest by simply typing it into your CLI:

```bash
pytest
```

This is the expected output:
```bash
============================= test session starts =============================
platform win32 -- Python 3.8.2, pytest-3.4.0, py-1.5.2, pluggy-0.6.0
rootdir: C:\projects\botbuilder-python, inifile:
plugins: cov-2.5.1
...
```

## Getting support and providing feedback
Below are the various channels that are available to you for obtaining support and providing feedback. Please pay carful attention to which channel should be used for which type of content. e.g. general "how do I..." questions should be asked on Stack Overflow, Twitter or Gitter, with GitHub issues being for feature requests and bug reports.

### Github issues
[Github issues](https://github.com/Microsoft/botbuilder-python/issues) should be used for bugs and feature requests.

### Stack overflow
[Stack Overflow](https://stackoverflow.com/questions/tagged/botframework) is a great place for getting high-quality answers. Our support team, as well as many of our community members are already on Stack Overflow providing answers to 'how-to' questions.

### Azure Support
If you issues relates to [Azure Bot Service](https://azure.microsoft.com/en-gb/services/bot-service/), you can take advantage of the available [Azure support options](https://azure.microsoft.com/en-us/support/options/).

### Twitter
We use the [@msbotframework](https://twitter.com/msbotframework) account on twitter for announcements and members from the development team watch for tweets for [@msbotframework](https://twitter.com/msbotframework).

### Gitter Chat Room
The [Gitter Channel](https://gitter.im/Microsoft/BotBuilder) provides a place where the Community can get together and collaborate.

## Contributing and our code of conduct
We welcome contributions and suggestions. Please see our [contributing guidelines](./contributing.md) for more information.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).

For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or contact
 [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

### Contributing Code

In order to create pull requests, submitted code must pass ```pylint``` and ```black``` checks.  Run both tools on every file you've changed.

For more information and installation instructions, see:

* [black](https://pypi.org/project/black/)
* [pylint](https://pylint.org/)

## Reporting Security Issues
Security issues and bugs should be reported privately, via email, to the Microsoft Security Response Center (MSRC)
at [secure@microsoft.com](mailto:secure@microsoft.com).  You should receive a response within 24 hours.  If for some
 reason you do not, please follow up via email to ensure we received your original message. Further information,
 including the [MSRC PGP](https://technet.microsoft.com/en-us/security/dn606155) key, can be found in the
[Security TechCenter](https://technet.microsoft.com/en-us/security/default).

Copyright (c) Microsoft Corporation. All rights reserved.

Licensed under the [MIT](./LICENSE) License.


