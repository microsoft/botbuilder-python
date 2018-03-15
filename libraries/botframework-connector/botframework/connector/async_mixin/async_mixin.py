# --------------------------------------------------------------------------
#
# Copyright (c) Microsoft Corporation. All rights reserved.
#
# The MIT License (MIT)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the ""Software""), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED *AS IS*, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#
# --------------------------------------------------------------------------

import asyncio
import functools
import logging

from oauthlib import oauth2
import requests

from msrest.exceptions import (
    TokenExpiredError,
    ClientRequestError,
    raise_with_traceback,
)


_LOGGER = logging.getLogger(__name__)

class AsyncServiceClientMixin:

    async def async_send_formdata(self, request, headers=None, content=None, stream=True, **config):
        """Send data as a multipart form-data request.

        We only deal with file-like objects or strings at this point.
        The requests is not yet streamed.

        :param ClientRequest request: The request object to be sent.
        :param dict headers: Any headers to add to the request.
        :param dict content: Dictionary of the fields of the formdata.
        :param config: Any specific config overrides.
        """
        files = self._prepare_send_formdata(request, headers, content)
        return await self.async_send(request, headers, files=files, stream=stream, **config)

    async def async_send(self, request, headers=None, content=None, stream=True, **config):
        """Prepare and send request object according to configuration.

        :param ClientRequest request: The request object to be sent.
        :param dict headers: Any headers to add to the request.
        :param content: Any body data to add to the request.
        :param config: Any specific config overrides
        """
        response = None
        session = self.creds.signed_session()
        kwargs = self._configure_session(session, **config)
        kwargs['stream'] = stream
        loop = asyncio.get_event_loop()

        request.add_headers(headers if headers else {})
        if not kwargs.get('files'):
            request.add_content(content)
        try:

            try:
                future = loop.run_in_executor(
                    None,
                    functools.partial(
                        session.request,
                        request.method,
                        request.url,
                        data=request.data,
                        headers=request.headers,
                        **kwargs
                    )
                )
                return await future

            except (oauth2.rfc6749.errors.InvalidGrantError,
                    oauth2.rfc6749.errors.TokenExpiredError) as err:
                error = "Token expired or is invalid. Attempting to refresh."
                _LOGGER.warning(error)

            try:
                session = self.creds.refresh_session()
                kwargs = self._configure_session(session)

                future = loop.run_in_executor(
                    None,
                    functools.partial(
                        session.request,
                        request.method,
                        request.url,
                        data=request.data,
                        headers=request.headers,
                        **kwargs
                    )
                )
                return await future
            except (oauth2.rfc6749.errors.InvalidGrantError,
                    oauth2.rfc6749.errors.TokenExpiredError) as err:
                msg = "Token expired or is invalid."
                raise_with_traceback(TokenExpiredError, msg, err)

        except (requests.RequestException,
                oauth2.rfc6749.errors.OAuth2Error) as err:
            msg = "Error occurred in request."
            raise_with_traceback(ClientRequestError, msg, err)
        finally:
            if not response or not stream:
                session.close()
