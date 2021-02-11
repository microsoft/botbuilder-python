# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from botframework.connector.auth import AppCredentials


class OAuthPromptSettings:
    def __init__(
        self,
        connection_name: str,
        title: str,
        text: str = None,
        timeout: int = None,
        oauth_app_credentials: AppCredentials = None,
        end_on_invalid_message: bool = False,
    ):
        """
        Settings used to configure an `OAuthPrompt` instance.
         Parameters:
            connection_name (str): Name of the OAuth connection being used.
            title (str): The title of the cards signin button.
            text (str): (Optional) additional text included on the signin card.
            timeout (int): (Optional) number of milliseconds the prompt will wait for the user to authenticate.
                `OAuthPrompt` defaults value to `900,000` ms (15 minutes).
            oauth_app_credentials (AppCredentials): (Optional) AppCredentials to use for OAuth.  If None,
            the Bots credentials are used.
            end_on_invalid_message (bool): (Optional) value indicating whether the OAuthPrompt should end upon
            receiving an invalid message.  Generally the OAuthPrompt will ignore incoming messages from the
            user during the auth flow, if they are not related to the auth flow.  This flag enables ending the
            OAuthPrompt rather than ignoring the user's message.  Typically, this flag will be set to 'true',
            but is 'false' by default for backwards compatibility.
        """
        self.connection_name = connection_name
        self.title = title
        self.text = text
        self.timeout = timeout
        self.oath_app_credentials = oauth_app_credentials
        self.end_on_invalid_message = end_on_invalid_message
