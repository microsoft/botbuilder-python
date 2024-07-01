# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from .certificate_app_credentials import CertificateAppCredentials
from .government_constants import GovernmentConstants


class CertificateGovernmentAppCredentials(CertificateAppCredentials):
    """
    GovernmentAppCredentials implementation using a certificate.
    """

    def __init__(
        self,
        app_id: str,
        certificate_thumbprint: str,
        certificate_private_key: str,
        channel_auth_tenant: str = None,
        oauth_scope: str = None,
        certificate_public: str = None,
    ):
        """
        AppCredentials implementation using a certificate.

        :param app_id:
        :param certificate_thumbprint:
        :param certificate_private_key:
        :param channel_auth_tenant:
        :param oauth_scope:
        :param certificate_public: public_certificate (optional) is public key certificate which will be sent
        through ‘x5c’ JWT header only for subject name and issuer authentication to support cert auto rolls.
        """

        # super will set proper scope and endpoint.
        super().__init__(
            app_id=app_id,
            channel_auth_tenant=channel_auth_tenant,
            oauth_scope=oauth_scope,
            certificate_thumbprint=certificate_thumbprint,
            certificate_private_key=certificate_private_key,
            certificate_public=certificate_public,
        )

    def _get_default_channelauth_tenant(self) -> str:
        return GovernmentConstants.DEFAULT_CHANNEL_AUTH_TENANT

    def _get_to_channel_from_bot_loginurl_prefix(self) -> str:
        return GovernmentConstants.TO_CHANNEL_FROM_BOT_LOGIN_URL_PREFIX

    def _get_to_channel_from_bot_oauthscope(self) -> str:
        return GovernmentConstants.TO_CHANNEL_FROM_BOT_OAUTH_SCOPE
