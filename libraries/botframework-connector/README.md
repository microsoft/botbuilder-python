Microsoft Azure SDK for Python
==============================

This is the Microsoft Azure BotFramework Connector Client Library.

This package has been tested with Python 2.7, 3.3, 3.4 and 3.5.

Compatibility
=============

**IMPORTANT**: If you have an earlier version of the azure package
(version < 1.0), you should uninstall it before installing this package.

You can check the version using pip:

.. code:: shell

    pip freeze

If you see azure==0.11.0 (or any version below 1.0), uninstall it first:

.. code:: shell

    pip uninstall azure


Features
========

- Conversations: Create new conversation, send to conversation, reply to activity, get conversation members, get activity members, update and delete activity (if the channel supports it) and upload an attachment to a conversation.
- Attachments: Get attachment info and get attachment content.


Installation
============

Download Package
----------------

To install via the Python Package Index (PyPI), type:

.. code:: shell

    pip install azure-botframework-connector


Download Source Code
--------------------

To get the source code of the SDK via **git** type:

.. code:: shell

    git clone https://github.com/Azure/azure-sdk-for-python.git
    cd azure-sdk-for-python
    cd azure-botframework-connector
    python setup.py install


Usage
=====

BotConnector Client
-------------------

Within the Bot Framework, the Bot Connector service enables your bot to exchange messages with users on channels that are configured in the Bot Framework Portal.

Authentication
~~~~~~~~~~~~~~

Your bot communicates with the Bot Connector service using HTTP over a secured channel (SSL/TLS). When your bot sends a request to the Connector service, it must include information that the Connector service can use to verify its identity.

To authenticate the requests, you'll need configure the Connector with the App ID and password that you obtained for your bot during registration and the SDK will handle the rest.

More information: https://docs.microsoft.com/en-us/bot-framework/rest-api/bot-framework-rest-connector-authentication

.. code:: python

    from azure.botframework.connectorauth import MicrosoftTokenAuthentication
    credentials = MicrosoftTokenAuthentication('<your-app-id>', '<your-app-password>')


Creating a Conversation and sending a message
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from azure.botframework.connector import BotConnector
    from azure.botframework.connectorauth import MicrosoftTokenAuthentication
    from azure.botframework.connector import models

    APP_ID = '<your-app-id>'
    APP_PASSWORD = '<your-app-password>'
    SERVICE_URL = 'https://slack.botframework.com'
    CHANNEL_ID = 'slack'
    BOT_ID = '<bot-id>'
    RECIPIENT_ID = '<user-id>'

    credentials = MicrosoftTokenAuthentication(APP_ID, APP_PASSWORD)
    connector = BotConnector(credentials, base_url=SERVICE_URL)

    conversation = connector.conversations.create_conversation(models.ConversationParameters(
                bot=models.ChannelAccount(id=BOT_ID),
                members=[models.ChannelAccount(id=RECIPIENT_ID)]))

    connector.conversations.send_to_conversation(conversation.id, models.Activity(
                type=models.ActivityType.message,
                channel_id=CHANNEL_ID,
                recipient=models.ChannelAccount(id=RECIPIENT_ID),
                from_property=models.ChannelAccount(id=BOT_ID),
                text='Hello World!'))


Need Help?
==========

Be sure to check out the Microsoft Azure `Developer Forums on Stack
Overflow <http://go.microsoft.com/fwlink/?LinkId=234489>`__ if you have
trouble with the provided code.


Contribute Code or Provide Feedback
===================================

If you would like to become an active contributor to this project please
follow the instructions provided in `Microsoft Azure Projects
Contribution
Guidelines <http://azure.github.io/guidelines.html>`__.

If you encounter any bugs with the library please file an issue in the
`Issues <https://github.com/Azure/azure-sdk-for-python/issues>`__
section of the project.


Learn More
==========

`Microsoft Bot Framework <https://dev.botframework.com/>`__

`About Bot Service <https://docs.microsoft.com/en-us/bot-framework/>`__

`Bot Service - API Reference <https://docs.microsoft.com/en-us/bot-framework/rest-api/bot-framework-rest-connector-api-reference>`__

`Microsoft Azure Python Developer
Center <http://azure.microsoft.com/en-us/develop/python/>`__
