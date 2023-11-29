# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

# TODO: enable this in the future
# With python 3.7 the line below will allow to do Postponed Evaluation of Annotations. See PEP 563
# from __future__ import annotations

import asyncio
import inspect
import uuid
from datetime import datetime
from uuid import uuid4
from typing import Awaitable, Coroutine, Dict, List, Callable, Union
from copy import copy
from threading import Lock
from botframework.connector.auth import AppCredentials, ClaimsIdentity
from botframework.connector.token_api.models import (
    SignInUrlResponse,
    TokenExchangeResource,
    TokenExchangeRequest,
)
from botbuilder.schema import (
    ActivityTypes,
    Activity,
    ConversationAccount,
    ConversationReference,
    ChannelAccount,
    ResourceResponse,
    TokenResponse,
)
from ..bot_adapter import BotAdapter
from ..turn_context import TurnContext
from ..oauth.extended_user_token_provider import ExtendedUserTokenProvider


class UserToken:
    def __init__(
        self,
        connection_name: str = None,
        user_id: str = None,
        channel_id: str = None,
        token: str = None,
    ):
        self.connection_name = connection_name
        self.user_id = user_id
        self.channel_id = channel_id
        self.token = token

    def equals_key(self, rhs: "UserToken"):
        return (
            rhs is not None
            and self.connection_name == rhs.connection_name
            and self.user_id == rhs.user_id
            and self.channel_id == rhs.channel_id
        )


class ExchangeableToken(UserToken):
    def __init__(
        self,
        connection_name: str = None,
        user_id: str = None,
        channel_id: str = None,
        token: str = None,
        exchangeable_item: str = None,
    ):
        super(ExchangeableToken, self).__init__(
            connection_name=connection_name,
            user_id=user_id,
            channel_id=channel_id,
            token=token,
        )

        self.exchangeable_item = exchangeable_item

    def equals_key(self, rhs: "ExchangeableToken") -> bool:
        return (
            rhs is not None
            and self.exchangeable_item == rhs.exchangeable_item
            and super().equals_key(rhs)
        )

    def to_key(self) -> str:
        return self.exchangeable_item


class TokenMagicCode:
    def __init__(self, key: UserToken = None, magic_code: str = None):
        self.key = key
        self.magic_code = magic_code


class TestAdapter(BotAdapter, ExtendedUserTokenProvider):
    __test__ = False
    __EXCEPTION_EXPECTED = "ExceptionExpected"

    def __init__(
        self,
        logic: Coroutine = None,
        template_or_conversation: Union[Activity, ConversationReference] = None,
        send_trace_activities: bool = False,
    ):
        """
        Creates a new TestAdapter instance.
        :param logic:
        :param conversation: A reference to the conversation to begin the adapter state with.
        """
        super(TestAdapter, self).__init__()
        self.logic = logic
        self._next_id: int = 0
        self._user_tokens: List[UserToken] = []
        self._magic_codes: List[TokenMagicCode] = []
        self._conversation_lock = Lock()
        self.exchangeable_tokens: Dict[str, ExchangeableToken] = {}
        self.activity_buffer: List[Activity] = []
        self.updated_activities: List[Activity] = []
        self.deleted_activities: List[ConversationReference] = []
        self.send_trace_activities = send_trace_activities

        self.template = (
            template_or_conversation
            if isinstance(template_or_conversation, Activity)
            else Activity(
                channel_id="test",
                service_url="https://test.com",
                from_property=ChannelAccount(id="User1", name="user"),
                recipient=ChannelAccount(id="bot", name="Bot"),
                conversation=ConversationAccount(id="Convo1"),
            )
        )

        if isinstance(template_or_conversation, ConversationReference):
            self.template.channel_id = template_or_conversation.channel_id

    async def process_activity(
        self, activity: Activity, logic: Callable[[TurnContext], Awaitable]
    ):
        self._conversation_lock.acquire()
        try:
            # ready for next reply
            if activity.type is None:
                activity.type = ActivityTypes.message

            activity.channel_id = self.template.channel_id
            activity.from_property = self.template.from_property
            activity.recipient = self.template.recipient
            activity.conversation = self.template.conversation
            activity.service_url = self.template.service_url

            activity.id = str((self._next_id))
            self._next_id += 1
        finally:
            self._conversation_lock.release()

        activity.timestamp = activity.timestamp or datetime.utcnow()
        await self.run_pipeline(self.create_turn_context(activity), logic)

    async def send_activities(
        self, context, activities: List[Activity]
    ) -> List[ResourceResponse]:
        """
        INTERNAL: called by the logic under test to send a set of activities. These will be buffered
        to the current `TestFlow` instance for comparison against the expected results.
        :param context:
        :param activities:
        :return:
        """

        def id_mapper(activity):
            self.activity_buffer.append(activity)
            self._next_id += 1
            return ResourceResponse(id=str(self._next_id))

        return [
            id_mapper(activity)
            for activity in activities
            if self.send_trace_activities or activity.type != "trace"
        ]

    async def delete_activity(self, context, reference: ConversationReference):
        """
        INTERNAL: called by the logic under test to delete an existing activity. These are simply
        pushed onto a [deletedActivities](#deletedactivities) array for inspection after the turn
        completes.
        :param reference:
        :return:
        """
        self.deleted_activities.append(reference)

    async def update_activity(self, context, activity: Activity):
        """
        INTERNAL: called by the logic under test to replace an existing activity. These are simply
        pushed onto an [updatedActivities](#updatedactivities) array for inspection after the turn
        completes.
        :param activity:
        :return:
        """
        self.updated_activities.append(activity)

    async def continue_conversation(
        self,
        reference: ConversationReference,
        callback: Callable,
        bot_id: str = None,
        claims_identity: ClaimsIdentity = None,  # pylint: disable=unused-argument
        audience: str = None,
    ):
        """
        The `TestAdapter` just calls parent implementation.
        :param reference:
        :param callback:
        :param bot_id:
        :param claims_identity:
        :return:
        """
        await super().continue_conversation(
            reference, callback, bot_id, claims_identity, audience
        )

    async def create_conversation(  # pylint: disable=arguments-differ
        self, channel_id: str, callback: Callable  # pylint: disable=unused-argument
    ):
        self.activity_buffer.clear()
        update = Activity(
            type=ActivityTypes.conversation_update,
            members_added=[],
            members_removed=[],
            channel_id=channel_id,
            conversation=ConversationAccount(id=str(uuid.uuid4())),
        )
        context = self.create_turn_context(update)
        return await callback(context)

    async def receive_activity(self, activity):
        """
        INTERNAL: called by a `TestFlow` instance to simulate a user sending a message to the bot.
        This will cause the adapters middleware pipe to be run and it's logic to be called.
        :param activity:
        :return:
        """
        if isinstance(activity, str):
            activity = Activity(type="message", text=activity)
        # Initialize request.
        request = copy(self.template)

        for key, value in vars(activity).items():
            if value is not None and key != "additional_properties":
                setattr(request, key, value)

        request.type = request.type or ActivityTypes.message
        if not request.id:
            self._next_id += 1
            request.id = str(self._next_id)

        # Create context object and run middleware.
        context = self.create_turn_context(request)
        return await self.run_pipeline(context, self.logic)

    def get_next_activity(self) -> Activity:
        if len(self.activity_buffer) > 0:
            return self.activity_buffer.pop(0)
        return None

    async def send(self, user_says) -> object:
        """
        Sends something to the bot. This returns a new `TestFlow` instance which can be used to add
        additional steps for inspecting the bots reply and then sending additional activities.
        :param user_says:
        :return: A new instance of the TestFlow object
        """
        return TestFlow(await self.receive_activity(user_says), self)

    async def test(
        self, user_says, expected, description=None, timeout=None
    ) -> "TestFlow":
        """
        Send something to the bot and expects the bot to return with a given reply. This is simply a
        wrapper around calls to `send()` and `assertReply()`. This is such a common pattern that a
        helper is provided.
        :param user_says:
        :param expected:
        :param description:
        :param timeout:
        :return:
        """
        test_flow = await self.send(user_says)
        test_flow = await test_flow.assert_reply(expected, description, timeout)
        return test_flow

    async def tests(self, *args):
        """
        Support multiple test cases without having to manually call `test()` repeatedly. This is a
        convenience layer around the `test()`. Valid args are either lists or tuples of parameters
        :param args:
        :return:
        """
        for arg in args:
            description = None
            timeout = None
            if len(arg) >= 3:
                description = arg[2]
                if len(arg) == 4:
                    timeout = arg[3]
            await self.test(arg[0], arg[1], description, timeout)

    @staticmethod
    def create_conversation_reference(
        name: str, user: str = "User1", bot: str = "Bot"
    ) -> ConversationReference:
        return ConversationReference(
            channel_id="test",
            service_url="https://test.com",
            conversation=ConversationAccount(
                is_group=False,
                conversation_type=name,
                id=name,
            ),
            user=ChannelAccount(
                id=user.lower(),
                name=user.lower(),
            ),
            bot=ChannelAccount(
                id=bot.lower(),
                name=bot.lower(),
            ),
        )

    def add_user_token(
        self,
        connection_name: str,
        channel_id: str,
        user_id: str,
        token: str,
        magic_code: str = None,
    ):
        key = UserToken()
        key.channel_id = channel_id
        key.connection_name = connection_name
        key.user_id = user_id
        key.token = token

        if not magic_code:
            self._user_tokens.append(key)
        else:
            code = TokenMagicCode()
            code.key = key
            code.magic_code = magic_code
            self._magic_codes.append(code)

    async def get_user_token(
        self,
        context: TurnContext,
        connection_name: str,
        magic_code: str = None,
        oauth_app_credentials: AppCredentials = None,  # pylint: disable=unused-argument
    ) -> TokenResponse:
        key = UserToken()
        key.channel_id = context.activity.channel_id
        key.connection_name = connection_name
        key.user_id = context.activity.from_property.id

        if magic_code:
            magic_code_record = list(
                filter(lambda x: key.equals_key(x.key), self._magic_codes)
            )
            if magic_code_record and magic_code_record[0].magic_code == magic_code:
                # Move the token to long term dictionary.
                self.add_user_token(
                    connection_name,
                    key.channel_id,
                    key.user_id,
                    magic_code_record[0].key.token,
                )

                # Remove from the magic code list.
                idx = self._magic_codes.index(magic_code_record[0])
                self._magic_codes = [self._magic_codes.pop(idx)]

        match = [token for token in self._user_tokens if key.equals_key(token)]

        if match:
            return TokenResponse(
                connection_name=match[0].connection_name,
                token=match[0].token,
                expiration=None,
            )
        # Not found.
        return None

    async def sign_out_user(
        self,
        context: TurnContext,
        connection_name: str = None,
        user_id: str = None,
        oauth_app_credentials: AppCredentials = None,  # pylint: disable=unused-argument
    ):
        channel_id = context.activity.channel_id
        user_id = context.activity.from_property.id

        new_records = []
        for token in self._user_tokens:
            if (
                token.channel_id != channel_id
                or token.user_id != user_id
                or (connection_name and connection_name != token.connection_name)
            ):
                new_records.append(token)
        self._user_tokens = new_records

    async def get_oauth_sign_in_link(
        self,
        context: TurnContext,
        connection_name: str,
        final_redirect: str = None,  # pylint: disable=unused-argument
        oauth_app_credentials: AppCredentials = None,  # pylint: disable=unused-argument
    ) -> str:
        return (
            f"https://fake.com/oauthsignin"
            f"/{connection_name}/{context.activity.channel_id}/{context.activity.from_property.id}"
        )

    async def get_token_status(
        self,
        context: TurnContext,
        connection_name: str = None,
        user_id: str = None,
        include_filter: str = None,
        oauth_app_credentials: AppCredentials = None,
    ) -> Dict[str, TokenResponse]:
        return None

    async def get_aad_tokens(
        self,
        context: TurnContext,
        connection_name: str,
        resource_urls: List[str],
        user_id: str = None,  # pylint: disable=unused-argument
        oauth_app_credentials: AppCredentials = None,  # pylint: disable=unused-argument
    ) -> Dict[str, TokenResponse]:
        return None

    def add_exchangeable_token(
        self,
        connection_name: str,
        channel_id: str,
        user_id: str,
        exchangeable_item: str,
        token: str,
    ):
        key = ExchangeableToken(
            connection_name=connection_name,
            channel_id=channel_id,
            user_id=user_id,
            exchangeable_item=exchangeable_item,
            token=token,
        )
        self.exchangeable_tokens[key.to_key()] = key

    def throw_on_exchange_request(
        self,
        connection_name: str,
        channel_id: str,
        user_id: str,
        exchangeable_item: str,
    ):
        key = ExchangeableToken(
            connection_name=connection_name,
            channel_id=channel_id,
            user_id=user_id,
            exchangeable_item=exchangeable_item,
            token=TestAdapter.__EXCEPTION_EXPECTED,
        )

        self.exchangeable_tokens[key.to_key()] = key

    async def get_sign_in_resource_from_user(
        self,
        turn_context: TurnContext,
        connection_name: str,
        user_id: str,
        final_redirect: str = None,
    ) -> SignInUrlResponse:
        return await self.get_sign_in_resource_from_user_and_credentials(
            turn_context, None, connection_name, user_id, final_redirect
        )

    async def get_sign_in_resource_from_user_and_credentials(
        self,
        turn_context: TurnContext,
        oauth_app_credentials: AppCredentials,
        connection_name: str,
        user_id: str,
        final_redirect: str = None,
    ) -> SignInUrlResponse:
        return SignInUrlResponse(
            sign_in_link=f"https://fake.com/oauthsignin/{connection_name}/{turn_context.activity.channel_id}/{user_id}",
            token_exchange_resource=TokenExchangeResource(
                id=str(uuid4()),
                provider_id=None,
                uri=f"api://{connection_name}/resource",
            ),
        )

    async def exchange_token(
        self,
        turn_context: TurnContext,
        connection_name: str,
        user_id: str,
        exchange_request: TokenExchangeRequest,
    ) -> TokenResponse:
        return await self.exchange_token_from_credentials(
            turn_context, None, connection_name, user_id, exchange_request
        )

    async def exchange_token_from_credentials(
        self,
        turn_context: TurnContext,
        oauth_app_credentials: AppCredentials,
        connection_name: str,
        user_id: str,
        exchange_request: TokenExchangeRequest,
    ) -> TokenResponse:
        exchangeable_value = exchange_request.token or exchange_request.uri

        key = ExchangeableToken(
            channel_id=turn_context.activity.channel_id,
            connection_name=connection_name,
            exchangeable_item=exchangeable_value,
            user_id=user_id,
        )

        token_exchange_response = self.exchangeable_tokens.get(key.to_key())
        if token_exchange_response:
            if token_exchange_response.token == TestAdapter.__EXCEPTION_EXPECTED:
                raise Exception("Exception occurred during exchanging tokens")

            return TokenResponse(
                channel_id=key.channel_id,
                connection_name=key.connection_name,
                token=token_exchange_response.token,
                expiration=None,
            )

        return None

    def create_turn_context(self, activity: Activity) -> TurnContext:
        return TurnContext(self, activity)


class TestFlow:
    __test__ = False

    def __init__(self, previous: Callable, adapter: TestAdapter):
        """
        INTERNAL: creates a TestFlow instance.
        :param previous:
        :param adapter:
        """
        self.previous = previous
        self.adapter = adapter

    async def test(
        self, user_says, expected, description=None, timeout=None
    ) -> "TestFlow":
        """
        Send something to the bot and expects the bot to return with a given reply. This is simply a
        wrapper around calls to `send()` and `assertReply()`. This is such a common pattern that a
        helper is provided.
        :param user_says:
        :param expected:
        :param description:
        :param timeout:
        :return:
        """
        test_flow = await self.send(user_says)
        return await test_flow.assert_reply(
            expected, description or f'test("{user_says}", "{expected}")', timeout
        )

    async def send(self, user_says) -> "TestFlow":
        """
        Sends something to the bot.
        :param user_says:
        :return:
        """

        async def new_previous():
            nonlocal self, user_says
            if callable(self.previous):
                await self.previous()
            await self.adapter.receive_activity(user_says)

        return TestFlow(await new_previous(), self.adapter)

    async def assert_reply(
        self,
        expected: Union[str, Activity, Callable[[Activity, str], None]],
        description=None,
        timeout=None,  # pylint: disable=unused-argument
        is_substring=False,
    ) -> "TestFlow":
        """
        Generates an assertion if the bots response doesn't match the expected text/activity.
        :param expected:
        :param description:
        :param timeout:
        :param is_substring:
        :return:
        """

        # TODO: refactor method so expected can take a Callable[[Activity], None]
        def default_inspector(reply, description=None):
            if isinstance(expected, Activity):
                validate_activity(reply, expected)
            else:
                assert reply.type == "message", description + f" type == {reply.type}"
                if is_substring:
                    assert expected in reply.text.strip(), (
                        description + f" text == {reply.text}"
                    )
                else:
                    assert reply.text.strip() == expected.strip(), (
                        description + f" text == {reply.text}"
                    )

        if description is None:
            description = ""

        inspector = expected if callable(expected) else default_inspector

        async def test_flow_previous():
            nonlocal timeout
            if not timeout:
                timeout = 3000
            start = datetime.now()
            adapter = self.adapter

            async def wait_for_activity():
                nonlocal expected, timeout
                current = datetime.now()
                if (current - start).total_seconds() * 1000 > timeout:
                    if isinstance(expected, Activity):
                        expecting = expected.text
                    elif callable(expected):
                        expecting = inspect.getsourcefile(expected)
                    else:
                        expecting = str(expected)
                    raise RuntimeError(
                        f"TestAdapter.assert_reply({expecting}): {description} Timed out after "
                        f"{current - start}ms."
                    )
                if adapter.activity_buffer:
                    reply = adapter.activity_buffer.pop(0)
                    try:
                        await inspector(reply, description)
                    except Exception:
                        inspector(reply, description)

                else:
                    await asyncio.sleep(0.05)
                    await wait_for_activity()

            await wait_for_activity()

        return TestFlow(await test_flow_previous(), self.adapter)

    async def assert_no_reply(
        self,
        description=None,
        timeout=None,  # pylint: disable=unused-argument
    ) -> "TestFlow":
        """
        Generates an assertion if the bot responds when no response is expected.
        :param description:
        :param timeout:
        """
        if description is None:
            description = ""

        async def test_flow_previous():
            nonlocal timeout
            if not timeout:
                timeout = 3000
            start = datetime.now()
            adapter = self.adapter

            async def wait_for_activity():
                nonlocal timeout
                current = datetime.now()

                if (current - start).total_seconds() * 1000 > timeout:
                    # operation timed out and recieved no reply
                    return

                if adapter.activity_buffer:
                    reply = adapter.activity_buffer.pop(0)
                    raise RuntimeError(
                        f"TestAdapter.assert_no_reply(): '{reply.text}' is responded when waiting for no reply."
                    )

                await asyncio.sleep(0.05)
                await wait_for_activity()

            await wait_for_activity()

        return TestFlow(await test_flow_previous(), self.adapter)


def validate_activity(activity, expected) -> None:
    """
    Helper method that compares activities
    :param activity:
    :param expected:
    :return:
    """
    iterable_expected = vars(expected).items()

    for attr, value in iterable_expected:
        if value is not None and attr != "additional_properties":
            assert value == getattr(activity, attr)
