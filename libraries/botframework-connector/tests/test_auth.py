import pytest

from botbuilder.schema import Activity
from botframework.connector.auth import JwtTokenValidation
from botframework.connector.auth import SimpleCredentialProvider
from botframework.connector.auth import EmulatorValidation
from botframework.connector.auth import ChannelValidation


class TestAuth:
    EmulatorValidation.TO_BOT_FROM_EMULATOR_TOKEN_VALIDATION_PARAMETERS.ignore_expiration = True
    ChannelValidation.TO_BOT_FROM_CHANNEL_TOKEN_VALIDATION_PARAMETERS.ignore_expiration = True
    
    @pytest.mark.asyncio
    async def test_connector_auth_header_correct_app_id_and_service_url_should_validate(self):
        activity = Activity(service_url = 'https://webchat.botframework.com/') 
        header = 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IkdDeEFyWG9OOFNxbzdQd2VBNy16NjVkZW5KUSIsIng1dCI6IkdDeEFyWG9OOFNxbzdQd2VBNy16NjVkZW5KUSJ9.eyJzZXJ2aWNldXJsIjoiaHR0cHM6Ly93ZWJjaGF0LmJvdGZyYW1ld29yay5jb20vIiwiaXNzIjoiaHR0cHM6Ly9hcGkuYm90ZnJhbWV3b3JrLmNvbSIsImF1ZCI6IjM5NjE5YTU5LTVhMGMtNGY5Yi04N2M1LTgxNmM2NDhmZjM1NyIsImV4cCI6MTUxNjczNzUyMCwibmJmIjoxNTE2NzM2OTIwfQ.TBgpxbDS-gx1wm7ldvl7To-igfskccNhp-rU1mxUMtGaDjnsU--usH4OXZfzRsZqMlnXWXug_Hgd_qOr5RH8wVlnXnMWewoZTSGZrfp8GOd7jHF13Gz3F1GCl8akc3jeK0Ppc8R_uInpuUKa0SopY0lwpDclCmvDlz4PN6yahHkt_666k-9UGmRt0DDkxuYjbuYG8EDZxyyAhr7J6sFh3yE2UGRpJjRDB4wXWqv08Cp0Gn9PAW2NxOyN8irFzZH5_YZqE3DXDAYZ_IOLpygXQR0O-bFIhLDVxSz6uCeTBRjh8GU7XJ_yNiRDoaby7Rd2IfRrSnvMkBRsB8MsWN8oXg'
        credentials = SimpleCredentialProvider('39619a59-5a0c-4f9b-87c5-816c648ff357', '')
        try:
            await JwtTokenValidation.assert_valid_activity(activity, header, credentials)
        except:
            pytest.fail("Unexpected error")

    @pytest.mark.asyncio
    async def test_connector_auth_header_with_different_bot_app_id_should_not_validate(self):
        activity = Activity(service_url = 'https://webchat.botframework.com/') 
        header = 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IkdDeEFyWG9OOFNxbzdQd2VBNy16NjVkZW5KUSIsIng1dCI6IkdDeEFyWG9OOFNxbzdQd2VBNy16NjVkZW5KUSJ9.eyJzZXJ2aWNldXJsIjoiaHR0cHM6Ly93ZWJjaGF0LmJvdGZyYW1ld29yay5jb20vIiwiaXNzIjoiaHR0cHM6Ly9hcGkuYm90ZnJhbWV3b3JrLmNvbSIsImF1ZCI6IjM5NjE5YTU5LTVhMGMtNGY5Yi04N2M1LTgxNmM2NDhmZjM1NyIsImV4cCI6MTUxNjczNzUyMCwibmJmIjoxNTE2NzM2OTIwfQ.TBgpxbDS-gx1wm7ldvl7To-igfskccNhp-rU1mxUMtGaDjnsU--usH4OXZfzRsZqMlnXWXug_Hgd_qOr5RH8wVlnXnMWewoZTSGZrfp8GOd7jHF13Gz3F1GCl8akc3jeK0Ppc8R_uInpuUKa0SopY0lwpDclCmvDlz4PN6yahHkt_666k-9UGmRt0DDkxuYjbuYG8EDZxyyAhr7J6sFh3yE2UGRpJjRDB4wXWqv08Cp0Gn9PAW2NxOyN8irFzZH5_YZqE3DXDAYZ_IOLpygXQR0O-bFIhLDVxSz6uCeTBRjh8GU7XJ_yNiRDoaby7Rd2IfRrSnvMkBRsB8MsWN8oXg'
        credentials = SimpleCredentialProvider('00000000-0000-0000-0000-000000000000', '')
        with pytest.raises(Exception):
            await JwtTokenValidation.assert_valid_activity(activity, header, credentials)

    @pytest.mark.asyncio
    async def test_connector_auth_header_and_no_credential_should_not_validate(self):
        activity = Activity(service_url = 'https://webchat.botframework.com/') 
        header = 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IkdDeEFyWG9OOFNxbzdQd2VBNy16NjVkZW5KUSIsIng1dCI6IkdDeEFyWG9OOFNxbzdQd2VBNy16NjVkZW5KUSJ9.eyJzZXJ2aWNldXJsIjoiaHR0cHM6Ly93ZWJjaGF0LmJvdGZyYW1ld29yay5jb20vIiwiaXNzIjoiaHR0cHM6Ly9hcGkuYm90ZnJhbWV3b3JrLmNvbSIsImF1ZCI6IjM5NjE5YTU5LTVhMGMtNGY5Yi04N2M1LTgxNmM2NDhmZjM1NyIsImV4cCI6MTUxNjczNzUyMCwibmJmIjoxNTE2NzM2OTIwfQ.TBgpxbDS-gx1wm7ldvl7To-igfskccNhp-rU1mxUMtGaDjnsU--usH4OXZfzRsZqMlnXWXug_Hgd_qOr5RH8wVlnXnMWewoZTSGZrfp8GOd7jHF13Gz3F1GCl8akc3jeK0Ppc8R_uInpuUKa0SopY0lwpDclCmvDlz4PN6yahHkt_666k-9UGmRt0DDkxuYjbuYG8EDZxyyAhr7J6sFh3yE2UGRpJjRDB4wXWqv08Cp0Gn9PAW2NxOyN8irFzZH5_YZqE3DXDAYZ_IOLpygXQR0O-bFIhLDVxSz6uCeTBRjh8GU7XJ_yNiRDoaby7Rd2IfRrSnvMkBRsB8MsWN8oXg'
        credentials = SimpleCredentialProvider('', '')
        with pytest.raises(Exception):
            await JwtTokenValidation.assert_valid_activity(activity, header, credentials)

    @pytest.mark.asyncio
    async def test_emulator_msa_header_correct_app_id_and_service_url_should_validate(self):
        activity = Activity(service_url = '')
        header = 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6IkZTaW11RnJGTm9DMHNKWEdtdjEzbk5aY2VEYyIsImtpZCI6IkZTaW11RnJGTm9DMHNKWEdtdjEzbk5aY2VEYyJ9.eyJhdWQiOiJodHRwczovL2FwaS5ib3RmcmFtZXdvcmsuY29tIiwiaXNzIjoiaHR0cHM6Ly9zdHMud2luZG93cy5uZXQvZDZkNDk0MjAtZjM5Yi00ZGY3LWExZGMtZDU5YTkzNTg3MWRiLyIsImlhdCI6MTUyMTgzNzQwMywibmJmIjoxNTIxODM3NDAzLCJleHAiOjE1MjE4NDEzMDMsImFpbyI6IlkyTmdZRmd0SmRpNlErSjVqMGxtOVovaWJwVTJBQT09IiwiYXBwaWQiOiIyM2MzNDFiZi0zMTAwLTRhMDktYTlmMi05YTI5YmY2MzRjMWQiLCJhcHBpZGFjciI6IjEiLCJpZHAiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC9kNmQ0OTQyMC1mMzliLTRkZjctYTFkYy1kNTlhOTM1ODcxZGIvIiwidGlkIjoiZDZkNDk0MjAtZjM5Yi00ZGY3LWExZGMtZDU5YTkzNTg3MWRiIiwidXRpIjoicm0tb3ItRkU2ME9yZkQ2azBDWURBQSIsInZlciI6IjEuMCJ9.DnQgEoxlQFfMJTUEVAECfRuY4wSvL_aTHXfpnWScOOQrnjwWnJw9s1clcs8-XAuHnBHkqv19SBkNSyoo_Mgeh9dHBvjNmjflwo_GRzpKmDW5i3xF4pal0vTRmn6RHmORB72N9V_OqAmtId_bQeo9qqUbWER6zmZjwX85knhlCE_Ib-id2mDj9edvQuxKjTGjTi9XNbX7WqQ3tstENTFBw1z3uRfcqCGEPnFgvYD-Yd8LA9j28jQoVY0Mn6K0cfKXhBWOqvCLesnVtK07CCXiVS7-jZmBLlXKCgWIHGJM8yuMt_A7nXZbwL9Dx4h-7OerxH5iGEgIg6qayPpidH8CTA'
        credentials = SimpleCredentialProvider('23c341bf-3100-4a09-a9f2-9a29bf634c1d', '')
        try:
            await JwtTokenValidation.assert_valid_activity(activity, header, credentials)
        except:
            pytest.fail("Unexpected error")

    @pytest.mark.asyncio
    async def test_emulator_msa_header_and_no_credential_should_not_validate(self):
        activity = Activity(service_url = '') 
        header = 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IkdDeEFyWG9OOFNxbzdQd2VBNy16NjVkZW5KUSIsIng1dCI6IkdDeEFyWG9OOFNxbzdQd2VBNy16NjVkZW5KUSJ9.eyJzZXJ2aWNldXJsIjoiaHR0cHM6Ly93ZWJjaGF0LmJvdGZyYW1ld29yay5jb20vIiwiaXNzIjoiaHR0cHM6Ly9hcGkuYm90ZnJhbWV3b3JrLmNvbSIsImF1ZCI6IjM5NjE5YTU5LTVhMGMtNGY5Yi04N2M1LTgxNmM2NDhmZjM1NyIsImV4cCI6MTUxNjczNzUyMCwibmJmIjoxNTE2NzM2OTIwfQ.TBgpxbDS-gx1wm7ldvl7To-igfskccNhp-rU1mxUMtGaDjnsU--usH4OXZfzRsZqMlnXWXug_Hgd_qOr5RH8wVlnXnMWewoZTSGZrfp8GOd7jHF13Gz3F1GCl8akc3jeK0Ppc8R_uInpuUKa0SopY0lwpDclCmvDlz4PN6yahHkt_666k-9UGmRt0DDkxuYjbuYG8EDZxyyAhr7J6sFh3yE2UGRpJjRDB4wXWqv08Cp0Gn9PAW2NxOyN8irFzZH5_YZqE3DXDAYZ_IOLpygXQR0O-bFIhLDVxSz6uCeTBRjh8GU7XJ_yNiRDoaby7Rd2IfRrSnvMkBRsB8MsWN8oXg'
        credentials = SimpleCredentialProvider('00000000-0000-0000-0000-000000000000', '')
        with pytest.raises(Exception):
            await JwtTokenValidation.assert_valid_activity(activity, header, credentials)

    @pytest.mark.asyncio
    async def test_empty_header_and_no_credential_should_validate(self):
        activity = Activity(service_url = '') 
        header = ''
        credentials = SimpleCredentialProvider('', '')
        try:
            await JwtTokenValidation.assert_valid_activity(activity, header, credentials)
        except:
            pytest.fail("Unexpected error")
