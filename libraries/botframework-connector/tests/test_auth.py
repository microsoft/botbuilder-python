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
            await JwtTokenValidation.assert_valid_activity(activity, header, credentials, '')
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
            await JwtTokenValidation.assert_valid_activity(activity, header, credentials, '')

    @pytest.mark.asyncio
    async def test_emulator_msa_header_correct_app_id_and_service_url_should_validate(self):
        activity = Activity(service_url = '')
        header = 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6IlRpb0d5d3dsaHZkRmJYWjgxM1dwUGF5OUFsVSIsImtpZCI6IlRpb0d5d3dsaHZkRmJYWjgxM1dwUGF5OUFsVSJ9.eyJhdWQiOiJodHRwczovL2FwaS5ib3RmcmFtZXdvcmsuY29tIiwiaXNzIjoiaHR0cHM6Ly9zdHMud2luZG93cy5uZXQvZDZkNDk0MjAtZjM5Yi00ZGY3LWExZGMtZDU5YTkzNTg3MWRiLyIsImlhdCI6MTUyOTM0ODI2NiwibmJmIjoxNTI5MzQ4MjY2LCJleHAiOjE1MjkzNTIxNjYsImFpbyI6IlkyZGdZR2k2dWZEWXpxbk84eGRKcm5TU09IanpDQUE9IiwiYXBwaWQiOiIyY2Q4Nzg2OS0zOGEwLTQxODItOTI1MS1kMDU2ZThmMGFjMjQiLCJhcHBpZGFjciI6IjEiLCJpZHAiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC9kNmQ0OTQyMC1mMzliLTRkZjctYTFkYy1kNTlhOTM1ODcxZGIvIiwidGlkIjoiZDZkNDk0MjAtZjM5Yi00ZGY3LWExZGMtZDU5YTkzNTg3MWRiIiwidXRpIjoiN21QU1BoSHZkMG0wbGVKdWhZb3RBQSIsInZlciI6IjEuMCJ9.q3IZF2nDItR1p5C-uhmCPf6Vs-AfnmT9TjpOSZG7nplwViBiSvv6lJDkeJTQgMSKxc5LHQaRNRRlLLBhj5ORIiFT7Arqd1r8dUa7KlKrY9vR15ZnTPbiW3lEsMxQ9VIkQlUcvb0DP83UPWA2JMc7EQsO4joxngFNTmPv3cABOrGbE0HQqExK-Ovd1CGF8ud2cYnp8HsS874pxY_tK8E4ytw6AtDhXt_U3L9TwMmW-9IvoV9oWfN2zbr1WNhlf1zMH0f-H885tlr5gMfG6QSjc7okf3iJee-jJu51s7BdThzN2Lc__xQACEl3_FMvOLymKlv-O5U6ebBT0404-bAmmg'
        credentials = SimpleCredentialProvider('2cd87869-38a0-4182-9251-d056e8f0ac24', '')
        try:
            await JwtTokenValidation.assert_valid_activity(activity, header, credentials, '')
        except:
            pytest.fail("Unexpected error")

    @pytest.mark.asyncio
    async def test_emulator_msa_header_and_no_credential_should_not_validate(self):
        activity = Activity(service_url = '') 
        header = 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IkdDeEFyWG9OOFNxbzdQd2VBNy16NjVkZW5KUSIsIng1dCI6IkdDeEFyWG9OOFNxbzdQd2VBNy16NjVkZW5KUSJ9.eyJzZXJ2aWNldXJsIjoiaHR0cHM6Ly93ZWJjaGF0LmJvdGZyYW1ld29yay5jb20vIiwiaXNzIjoiaHR0cHM6Ly9hcGkuYm90ZnJhbWV3b3JrLmNvbSIsImF1ZCI6IjM5NjE5YTU5LTVhMGMtNGY5Yi04N2M1LTgxNmM2NDhmZjM1NyIsImV4cCI6MTUxNjczNzUyMCwibmJmIjoxNTE2NzM2OTIwfQ.TBgpxbDS-gx1wm7ldvl7To-igfskccNhp-rU1mxUMtGaDjnsU--usH4OXZfzRsZqMlnXWXug_Hgd_qOr5RH8wVlnXnMWewoZTSGZrfp8GOd7jHF13Gz3F1GCl8akc3jeK0Ppc8R_uInpuUKa0SopY0lwpDclCmvDlz4PN6yahHkt_666k-9UGmRt0DDkxuYjbuYG8EDZxyyAhr7J6sFh3yE2UGRpJjRDB4wXWqv08Cp0Gn9PAW2NxOyN8irFzZH5_YZqE3DXDAYZ_IOLpygXQR0O-bFIhLDVxSz6uCeTBRjh8GU7XJ_yNiRDoaby7Rd2IfRrSnvMkBRsB8MsWN8oXg'
        credentials = SimpleCredentialProvider('00000000-0000-0000-0000-000000000000', '')
        with pytest.raises(Exception):
            await JwtTokenValidation.assert_valid_activity(activity, header, credentials, '')

    @pytest.mark.asyncio
    async def test_empty_header_and_no_credential_should_validate(self):
        activity = Activity(service_url = '') 
        header = ''
        credentials = SimpleCredentialProvider('', '')
        try:
            await JwtTokenValidation.assert_valid_activity(activity, header, credentials, '')
        except:
            pytest.fail("Unexpected error")
