# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.


class SlackAdapterOptions:
    """
    Defines the implementation of the SlackAdapter options.
    """

    def __init__(
        self,
        slack_verification_token: str,
        slack_bot_token: str,
        slack_client_signing_secret: str,
    ):
        """
        Initializes a new instance of SlackAdapterOptions.

        :param slack_verification_token: A token for validating the origin of incoming webhooks.
        :type slack_verification_token: str
        :param slack_bot_token: A token for a bot to work on a single workspace.
        :type slack_bot_token: str
        :param slack_client_signing_secret: The token used to validate that incoming webhooks originated from Slack.
        :type slack_client_signing_secret: str
        """
        self.slack_verification_token = slack_verification_token
        self.slack_bot_token = slack_bot_token
        self.slack_client_signing_secret = slack_client_signing_secret
        self.slack_client_id = None
        self.slack_client_secret = None
        self.slack_redirect_uri = None
        self.slack_scopes = [str]

    async def get_token_for_team(self, team_id: str) -> str:
        """
        Receives a Slack team ID and returns the bot token associated with that team. Required for multi-team apps.

        :param team_id: The team ID.
        :type team_id: str
        :raises: :func:`NotImplementedError`
        """
        raise NotImplementedError()

    async def get_bot_user_by_team(self, team_id: str) -> str:
        """
        A method that receives a Slack team ID and returns the bot user ID associated with that team. Required for
         multi-team apps.

        :param team_id: The team ID.
        :type team_id: str
        :raises: :func:`NotImplementedError`
        """
        raise NotImplementedError()
