# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import hashlib
import hmac
import json
from io import IOBase
from typing import List, Union

import aiohttp
from aiohttp.web_request import Request

from slack.web.client import WebClient
from slack.web.slack_response import SlackResponse

from botbuilder.schema import Activity
from botbuilder.adapters.slack.slack_client_options import SlackClientOptions
from botbuilder.adapters.slack.slack_message import SlackMessage

POST_MESSAGE_URL = "https://slack.com/api/chat.postMessage"
POST_EPHEMERAL_MESSAGE_URL = "https://slack.com/api/chat.postEphemeral"


class SlackClient(WebClient):
    """
    Slack client that extends https://github.com/slackapi/python-slackclient.
    """

    def __init__(self, options: SlackClientOptions):
        if not options or not options.slack_bot_token:
            raise Exception("SlackAdapterOptions and bot_token are required")

        if (
            not options.slack_verification_token
            and not options.slack_client_signing_secret
        ):
            warning = (
                "\n****************************************************************************************\n"
                "* WARNING: Your bot is operating without recommended security mechanisms in place.     *\n"
                "* Initialize your adapter with a clientSigningSecret parameter to enable               *\n"
                "* verification that all incoming webhooks originate with Slack:                        *\n"
                "*                                                                                      *\n"
                "* adapter = new SlackAdapter({clientSigningSecret: <my secret from slack>});           *\n"
                "*                                                                                      *\n"
                "****************************************************************************************\n"
                ">> Slack docs: https://api.slack.com/docs/verifying-requests-from-slack"
            )
            raise Exception(
                warning
                + "Required: include a verificationToken or clientSigningSecret to verify incoming Events API webhooks"
            )

        super().__init__(token=options.slack_bot_token, run_async=True)

        self.options = options
        self.identity = None

    async def login_with_slack(self):
        if self.options.slack_bot_token:
            self.identity = await self.test_auth()
        elif (
            not self.options.slack_client_id
            or not self.options.slack_client_secret
            or not self.options.slack_redirect_uri
            or not self.options.slack_scopes
        ):
            raise Exception(
                "Missing Slack API credentials! Provide SlackClientId, SlackClientSecret, scopes and SlackRedirectUri "
                "as part of the SlackAdapter options."
            )

    def is_logged_in(self):
        return self.identity is not None

    async def test_auth(self) -> str:
        auth = await self.auth_test()
        return auth.data["user_id"]

    async def channels_list_ex(self, exclude_archived: bool = True) -> SlackResponse:
        args = {"exclude_archived": "1" if exclude_archived else "0"}
        return await self.channels_list(**args)

    async def users_counts(self) -> SlackResponse:
        return await self.api_call("users.counts")

    async def im_history_ex(
        self,
        channel: str,
        latest_timestamp: str = None,
        oldest_timestamp: str = None,
        count: int = None,
        unreads: bool = None,
    ) -> SlackResponse:
        args = {}
        if latest_timestamp:
            args["latest"] = latest_timestamp
        if oldest_timestamp:
            args["oldest"] = oldest_timestamp
        if count:
            args["count"] = str(count)
        if unreads:
            args["unreads"] = "1" if unreads else "0"

        return await self.im_history(channel=channel, **args)

    async def files_info_ex(
        self, file_id: str, page: int = None, count: int = None
    ) -> SlackResponse:
        args = {"count": str(count), "page": str(page)}
        return await self.files_info(file=file_id, **args)

    async def files_list_ex(
        self,
        user_id: str = None,
        date_from: str = None,
        date_to: str = None,
        count: int = None,
        page: int = None,
        types: List[str] = None,
    ) -> SlackResponse:
        args = {}

        if user_id:
            args["user"] = user_id

        if date_from:
            args["ts_from"] = date_from
        if date_to:
            args["ts_to"] = date_to

        if count:
            args["count"] = str(count)
        if page:
            args["page"] = str(page)

        if types:
            args["types"] = ",".join(types)

        return await self.files_list(**args)

    async def groups_history_ex(
        self, channel: str, latest: str = None, oldest: str = None, count: int = None
    ) -> SlackResponse:
        args = {}

        if latest:
            args["latest"] = latest
        if oldest:
            args["oldest"] = oldest

        if count:
            args["count"] = count

        return await self.groups_history(channel=channel, **args)

    async def groups_list_ex(self, exclude_archived: bool = True) -> SlackResponse:
        args = {"exclude_archived": "1" if exclude_archived else "0"}
        return await self.groups_list(**args)

    async def get_preferences(self) -> SlackResponse:
        return await self.api_call("users.prefs.get", http_verb="GET")

    async def stars_list_ex(
        self, user: str = None, count: int = None, page: int = None
    ) -> SlackResponse:
        args = {}

        if user:
            args["user"] = user
        if count:
            args["count"] = str(count)
        if page:
            args["page"] = str(page)

        return await self.stars_list(**args)

    async def groups_close(self, channel: str) -> SlackResponse:
        args = {"channel": channel}
        return await self.api_call("groups.close", params=args)

    async def chat_post_ephemeral_ex(
        self,
        channel: str,
        text: str,
        target_user: str,
        parse: str = None,
        link_names: bool = False,
        attachments: List[str] = None,  # pylint: disable=unused-argument
        as_user: bool = False,
    ) -> SlackResponse:
        args = {
            "text": text,
            "link_names": "1" if link_names else "0",
            "as_user": "1" if as_user else "0",
        }

        if parse:
            args["parse"] = parse

        # TODO: attachments (see PostEphemeralMessageAsync)
        # See: https://api.slack.com/messaging/composing/layouts#attachments
        # See: https://github.com/Inumedia/SlackAPI/blob/master/SlackAPI/Attachment.cs

        return await self.chat_postEphemeral(channel=channel, user=target_user, **args)

    async def chat_post_message_ex(
        self,
        channel: str,
        text: str,
        bot_name: str = None,
        parse: str = None,
        link_names: bool = False,
        blocks: List[str] = None,  # pylint: disable=unused-argument
        attachments: List[str] = None,  # pylint: disable=unused-argument
        unfurl_links: bool = False,
        icon_url: str = None,
        icon_emoji: str = None,
        as_user: bool = False,
    ) -> SlackResponse:
        args = {
            "text": text,
            "link_names": "1" if link_names else "0",
            "as_user": "1" if as_user else "0",
        }

        if bot_name:
            args["username"] = bot_name

        if parse:
            args["parse"] = parse

        if unfurl_links:
            args["unfurl_links"] = "1" if unfurl_links else "0"

        if icon_url:
            args["icon_url"] = icon_url

        if icon_emoji:
            args["icon_emoji"] = icon_emoji

        # TODO: blocks and attachments (see PostMessageAsync)
        # the blocks and attachments are combined into a single dict
        # See: https://api.slack.com/messaging/composing/layouts#attachments
        # See: https://github.com/Inumedia/SlackAPI/blob/master/SlackAPI/Attachment.cs

        return await self.chat_postMessage(channel=channel, **args)

    async def search_all_ex(
        self,
        query: str,
        sorting: str = None,
        direction: str = None,
        enable_highlights: bool = False,
        count: int = None,
        page: int = None,
    ) -> SlackResponse:
        args = {"highlight": "1" if enable_highlights else "0"}

        if sorting:
            args["sort"] = sorting

        if direction:
            args["sort_dir"] = direction

        if count:
            args["count"] = str(count)

        if page:
            args["page"] = str(page)

        return await self.search_all(query=query, **args)

    async def search_files_ex(
        self,
        query: str,
        sorting: str = None,
        direction: str = None,
        enable_highlights: bool = False,
        count: int = None,
        page: int = None,
    ) -> SlackResponse:
        args = {"highlight": "1" if enable_highlights else "0"}

        if sorting:
            args["sort"] = sorting

        if direction:
            args["sort_dir"] = direction

        if count:
            args["count"] = str(count)

        if page:
            args["page"] = str(page)

        return await self.search_files(query=query, **args)

    async def search_messages_ex(
        self,
        query: str,
        sorting: str = None,
        direction: str = None,
        enable_highlights: bool = False,
        count: int = None,
        page: int = None,
    ) -> SlackResponse:
        args = {"highlight": "1" if enable_highlights else "0"}

        if sorting:
            args["sort"] = sorting

        if direction:
            args["sort_dir"] = direction

        if count:
            args["count"] = str(count)

        if page:
            args["page"] = str(page)

        return await self.search_messages(query=query, **args)

    async def chat_update_ex(
        self,
        timestamp: str,
        channel: str,
        text: str,
        bot_name: str = None,
        parse: str = None,
        link_names: bool = False,
        attachments: List[str] = None,  # pylint: disable=unused-argument
        as_user: bool = False,
    ):
        args = {
            "text": text,
            "link_names": "1" if link_names else "0",
            "as_user": "1" if as_user else "0",
        }

        if bot_name:
            args["username"] = bot_name

        if parse:
            args["parse"] = parse

        # TODO: attachments (see PostEphemeralMessageAsync)
        # See: https://api.slack.com/messaging/composing/layouts#attachments
        # See: https://github.com/Inumedia/SlackAPI/blob/master/SlackAPI/Attachment.cs

        return await self.chat_update(channel=channel, ts=timestamp)

    async def files_upload_ex(
        self,
        file: Union[str, IOBase] = None,
        content: str = None,
        channels: List[str] = None,
        title: str = None,
        initial_comment: str = None,
        file_type: str = None,
    ):
        args = {}

        if channels:
            args["channels"] = ",".join(channels)

        if title:
            args["title"] = title

        if initial_comment:
            args["initial_comment"] = initial_comment

        if file_type:
            args["filetype"] = file_type

        return await self.files_upload(file=file, content=content, **args)

    async def get_bot_user_identity(
        self, activity: Activity  # pylint: disable=unused-argument
    ) -> str:
        return self.identity

    def verify_signature(self, req: Request, body: str) -> bool:
        timestamp = req.headers["X-Slack-Request-Timestamp"]
        message = ":".join(["v0", timestamp, body])

        computed_signature = "V0=" + hmac.new(
            bytes(self.options.slack_client_signing_secret, "utf-8"),
            msg=bytes(message, "utf-8"),
            digestmod=hashlib.sha256,
        ).hexdigest().upper().replace("-", "")

        received_signature = req.headers["X-Slack-Signature"].upper()

        return computed_signature == received_signature

    async def post_message(self, message: SlackMessage) -> SlackResponse:
        if not message:
            return None

        request_content = {
            "token": self.options.slack_bot_token,
            "channel": message.channel,
            "text": message.text,
        }

        if message.thread_ts:
            request_content["thread_ts"] = message.thread_ts

        if message.blocks:
            request_content["blocks"] = json.dumps(message.blocks)

        session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
        )

        http_verb = "POST"
        api_url = POST_EPHEMERAL_MESSAGE_URL if message.ephemeral else POST_MESSAGE_URL
        req_args = {"data": request_content}

        async with session.request(http_verb, api_url, **req_args) as res:
            response_content = {}
            try:
                response_content = await res.json()
            except aiohttp.ContentTypeError:
                pass

            response_data = {
                "data": response_content,
                "headers": res.headers,
                "status_code": res.status,
            }

            data = {
                "client": self,
                "http_verb": http_verb,
                "api_url": api_url,
                "req_args": req_args,
            }
            response = SlackResponse(**{**data, **response_data}).validate()

        await session.close()

        return response
