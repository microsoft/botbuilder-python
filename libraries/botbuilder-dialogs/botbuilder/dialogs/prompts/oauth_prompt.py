# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.dialogs import Dialog
from .oauth_prompt_settings import OAuthPromptSettings

class OAuthPrompt(Dialog):
    """
    Creates a new prompt that asks the user to sign in using the Bot Framework Single Sign On (SSO) service.

    The prompt will attempt to retrieve the users current token and if the user isn't signed in, it
    will send them an `OAuthCard` containing a button they can press to sign in. Depending on the channel,
    the user will be sent through one of two possible sign-in flows:

    - The automatic sign-in flow where once the user signs in, the SSO service will forward
    the bot the users access token using either an `event` or `invoke` activity.
    - The "magic code" flow where once the user signs in, they will be prompted by the SSO service
    to send the bot a six digit code confirming their identity. This code will be sent as a 
    standard `message` activity.

    Both flows are automatically supported by the `OAuthPrompt` and they only thing you need to be careful of
    is that you don't block the `event` and `invoke` activities that the prompt might be waiting on.

    Note:
    You should avaoid persisting the access token with your bots other state. The Bot Frameworks SSO service
    will securely store the token on your behalf. If you store it in your bots state,
    it could expire or be revoked in between turns.

    When calling the prompt from within a waterfall step, you should use the token within the step
    following the prompt and then let the token go out of scope at the end of your function

    Prompt Usage

    When used with your bots `DialogSet`, you can simply add a new instance of the prompt as a named dialog using `DialogSet.add()`.
    You can then start the prompt from a waterfall step using either `DialogContext.begin()` or `DialogContext.prompt()`.
    The user will be prompted to sign in as needed and their access token will be passed as an argument to the callers next waterfall step.
    """
    
    def __init__(self, dialog_id: str, settings: OAuthPromptSettings, validator=None):
        super().__init__(dialog_id)
        
        if not settings:
            raise TypeError('OAuthPrompt requires OAuthPromptSettings.')
        
        self._settings = settings
        self._validator = validator