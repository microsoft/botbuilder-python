# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import aiounittest
from botframework.connector.auth import (
    AppCredentials,
    AuthenticationConstants,
    GovernmentConstants,
    CertificateServiceClientCredentialsFactory,
    CertificateAppCredentials,
    CertificateGovernmentAppCredentials
)


class CertificateServiceClientCredentialsFactoryTests(aiounittest.AsyncTestCase):
    test_appid = "test_appid"
    test_tenant_id = "test_tenant_id"
    test_audience = "test_audience"
    login_endpoint = AuthenticationConstants.TO_CHANNEL_FROM_BOT_LOGIN_URL_PREFIX
    gov_login_endpoint = GovernmentConstants.TO_CHANNEL_FROM_BOT_LOGIN_URL_PREFIX
    private_login_endpoint = "https://login.privatecloud.com"

    async def test_can_create_public_credentials(self):
        factory = CertificateServiceClientCredentialsFactory(
            app_id=CertificateServiceClientCredentialsFactoryTests.test_appid,
            certificate_thumbprint="thumbprint",
            certificate_private_key="private_key",
        )

        credentials = await factory.create_credentials(
            CertificateServiceClientCredentialsFactoryTests.test_appid,
            CertificateServiceClientCredentialsFactoryTests.test_audience,
            CertificateServiceClientCredentialsFactoryTests.login_endpoint,
            True,
        )

        assert isinstance(credentials, CertificateAppCredentials)

    async def test_can_create_gov_credentials(self):
        factory = CertificateServiceClientCredentialsFactory(
            app_id=CertificateServiceClientCredentialsFactoryTests.test_appid,
            certificate_thumbprint="thumbprint",
            certificate_private_key="private_key",
        )

        credentials = await factory.create_credentials(
            CertificateServiceClientCredentialsFactoryTests.test_appid,
            CertificateServiceClientCredentialsFactoryTests.test_audience,
            CertificateServiceClientCredentialsFactoryTests.gov_login_endpoint,
            True,
        )

        assert isinstance(credentials, CertificateGovernmentAppCredentials)

    async def test_can_create_private_credentials(self):
        factory = CertificateServiceClientCredentialsFactory(
            app_id=CertificateServiceClientCredentialsFactoryTests.test_appid,
            certificate_thumbprint="thumbprint",
            certificate_private_key="private_key",
        )

        credentials = await factory.create_credentials(
            CertificateServiceClientCredentialsFactoryTests.test_appid,
            CertificateServiceClientCredentialsFactoryTests.test_audience,
            CertificateServiceClientCredentialsFactoryTests.private_login_endpoint,
            True,
        )

        assert isinstance(credentials, CertificateAppCredentials)
        assert credentials.oauth_endpoint == CertificateServiceClientCredentialsFactoryTests.private_login_endpoint
