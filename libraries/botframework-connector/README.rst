
==================================
Microsoft Bot Framework Connector for Python
==================================

.. image:: https://travis-ci.org/Microsoft/botbuilder-python.svg?branch=master
   :target:  https://travis-ci.org/Microsoft/botbuilder-python
   :align: right
   :alt: Travis status for master branch
.. image:: https://fuselabs.visualstudio.com/SDK_v4/_apis/build/status/SDK_v4-Python-package-CI?branchName=master
   :target:  https://fuselabs.visualstudio.com/SDK_v4/_apis/build/status/SDK_v4-Python-package-CI
   :align: right
   :alt: Azure DevOps status for master branch
.. image:: https://badge.fury.io/py/botframework-connector.svg
   :target: https://badge.fury.io/py/botframework-connector
   :alt: Latest PyPI package version

Within the Bot Framework, the Bot Connector service enables your bot to exchange messages with users on channels that are configured in the Bot Framework Portal.

How to Install
==============

.. code-block:: python
  
  pip install botframework-connector

How to Use
==========

Authentication
==============

Your bot communicates with the Bot Connector service using HTTP over a secured channel (SSL/TLS). When your bot sends a request to the Connector service, it must include information that the Connector service can use to verify its identity.

To authenticate the requests, you'll need configure the Connector with the App ID and password that you obtained for your bot during registration and the Connector will handle the rest.

More information: https://docs.microsoft.com/en-us/bot-framework/rest-api/bot-framework-rest-connector-authentication

Example
=======

Client creation (with authentication), conversation initialization and activity send to user.

.. code-block:: python

  from microsoft.botbuilder.schema import *
  from microsoft.botframework.connector import ConnectorClient
  from microsoft.botframework.connector.auth import MicrosoftTokenAuthentication

  APP_ID = '<your-app-id>'
  APP_PASSWORD = '<your-app-password>'
  SERVICE_URL = 'https://slack.botframework.com'
  CHANNEL_ID = 'slack'
  BOT_ID = '<bot-id>'
  RECIPIENT_ID = '<user-id>'

  credentials = MicrosoftTokenAuthentication(APP_ID, APP_PASSWORD)
  connector = ConnectorClient(credentials, base_url=SERVICE_URL)

  conversation = connector.conversations.create_conversation(ConversationParameters(
              bot=ChannelAccount(id=BOT_ID),
              members=[ChannelAccount(id=RECIPIENT_ID)]))

  connector.conversations.send_to_conversation(conversation.id, Activity(
              type=ActivityTypes.message,
              channel_id=CHANNEL_ID,
              recipient=ChannelAccount(id=RECIPIENT_ID),
              from_property=ChannelAccount(id=BOT_ID),
              text='Hello World!'))


Rest API Documentation
======================

For the Connector Service API Documentation, please see our `API reference`_.

Documentation/Wiki
==================

You can find more information on the botbuilder-python project by visiting our `Wiki`_.

Requirements
============

* `Python >= 3.6.4`_


Source Code
===========
The latest developer version is available in a github repository:
https://github.com/Microsoft/botbuilder-python/


Contributing
============

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.microsoft.com.

When you submit a pull request, a CLA-bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., label, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the `Microsoft Open Source Code of Conduct`_.
For more information see the `Code of Conduct FAQ`_ or
contact `opencode@microsoft.com`_ with any additional questions or comments.

Reporting Security Issues
=========================

Security issues and bugs should be reported privately, via email, to the Microsoft Security
Response Center (MSRC) at `secure@microsoft.com`_. You should
receive a response within 24 hours. If for some reason you do not, please follow up via
email to ensure we received your original message. Further information, including the
`MSRC PGP`_ key, can be found in
the `Security TechCenter`_.

License
=======

Copyright (c) Microsoft Corporation. All rights reserved.

Licensed under the MIT_ License.

.. _API Reference: https://docs.microsoft.com/en-us/Bot-Framework/rest-api/bot-framework-rest-connector-api-reference
.. _Wiki: https://github.com/Microsoft/botbuilder-python/wiki
.. _Python >= 3.6.4: https://www.python.org/downloads/
.. _MIT: https://github.com/Microsoft/vscode/blob/master/LICENSE.txt
.. _Microsoft Open Source Code of Conduct: https://opensource.microsoft.com/codeofconduct/
.. _Code of Conduct FAQ: https://opensource.microsoft.com/codeofconduct/faq/
.. _opencode@microsoft.com: mailto:opencode@microsoft.com
.. _secure@microsoft.com: mailto:secure@microsoft.com
.. _MSRC PGP: https://technet.microsoft.com/en-us/security/dn606155
.. _Security TechCenter: https://github.com/Microsoft/vscode/blob/master/LICENSE.txt

.. <https://technet.microsoft.com/en-us/security/default>`_