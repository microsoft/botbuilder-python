# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import traceback

from http import HTTPStatus
from typing import Awaitable, Callable
from botframework.connector.channels import Channels

from botframework.connector.token_api.models import (
    TokenResponse,
    TokenExchangeRequest,
)
from botbuilder.schema import (
    Activity,
    ActivityTypes,
    SignInConstants,
    TokenExchangeInvokeRequest,
    TokenExchangeInvokeResponse,
)
from botbuilder.core import (
    ExtendedUserTokenProvider,
    Middleware,
    InvokeResponse,
    Storage,
    StoreItem,
    TurnContext,
)


class _TokenStoreItem(StoreItem):
    def __init__(self, **kwargs):
        self.e_tag: str = None
        super().__init__(**kwargs)

    @staticmethod
    def get_storage_key(turn_context: TurnContext):
        activity = turn_context.activity
        if not activity.channel_id:
            raise TypeError("invalid activity-missing channel_id")

        if not activity.conversation or not activity.conversation.id:
            raise TypeError("invalid activity-missing conversation.id")

        channel_id = activity.channel_id
        conversation_id = activity.conversation.id

        value = activity.value
        if not value or "id" not in value:
            raise Exception("Invalid signin/tokenExchange. Missing activity.value[id]")

        return f"{channel_id}/{conversation_id}/{value['id']}"


class TeamsSSOTokenExchangeMiddleware(Middleware):
    """
    If the activity name is signin/tokenExchange, self middleware will attempt to
    exchange the token, and deduplicate the incoming call, ensuring only one
    exchange request is processed.

    .. remarks::
        If a user is signed into multiple Teams clients, the Bot could receive a
        "signin/tokenExchange" from each client. Each token exchange request for a
        specific user login will have an identical Activity.Value.Id.

        Only one of these token exchange requests should be processed by the bot.
        The others return <see cref="System.Net.HttpStatusCode.PreconditionFailed"/>.
        For a distributed bot in production, self requires a distributed storage
        ensuring only one token exchange is processed. self middleware supports
        CosmosDb storage found in Microsoft.Bot.Builder.Azure, or MemoryStorage for
        local development. IStorage's ETag implementation for token exchange activity
        deduplication.
    """

    def __init__(self, storage: Storage, connection_name: str):
        """
        Initializes a instance of the <see cref="TeamsSSOTokenExchangeMiddleware"/> class.

        :param storage: The Storage to use for deduplication.
        :param connection_name: The connection name to use for the single
        sign on token exchange.
        """
        if storage is None:
            raise TypeError("storage cannot be None")

        if connection_name is None:
            raise TypeError("connection name cannot be None")

        self._oauth_connection_name = connection_name
        self._storage = storage

    async def on_turn(
        self, context: TurnContext, logic: Callable[[TurnContext], Awaitable]
    ):
        if (
            context.activity.channel_id == Channels.ms_teams
            and context.activity.name == SignInConstants.token_exchange_operation_name
        ):
            # If the TokenExchange is NOT successful, the response will have already been sent by _exchanged_token
            if not await self._exchanged_token(context):
                return

            # Only one token exchange should proceed from here. Deduplication is performed second because in the case
            # of failure due to consent required, every caller needs to receive the
            if not await self._deduplicated_token_exchange_id(context):
                # If the token is not exchangeable, do not process this activity further.
                return

        await logic()

    async def _deduplicated_token_exchange_id(self, turn_context: TurnContext) -> bool:
        # Create a StoreItem with Etag of the unique 'signin/tokenExchange' request
        store_item = _TokenStoreItem(e_tag=turn_context.activity.value.get("id", None))

        store_items = {_TokenStoreItem.get_storage_key(turn_context): store_item}
        try:
            # Writing the IStoreItem with ETag of unique id will succeed only once
            await self._storage.write(store_items)
        except Exception as error:
            # Memory storage throws a generic exception with a Message of 'Etag conflict. [other error info]'
            # CosmosDbPartitionedStorage throws: ex.Message.Contains("precondition is not met")
            if "Etag conflict" in str(error) or "precondition is not met" in str(error):
                # Do NOT proceed processing self message, some other thread or machine already has processed it.

                # Send 200 invoke response.
                await self._send_invoke_response(turn_context)
                return False

            raise error

        return True

    async def _send_invoke_response(
        self,
        turn_context: TurnContext,
        body: object = None,
        http_status_code=HTTPStatus.OK,
    ):
        await turn_context.send_activity(
            Activity(
                type=ActivityTypes.invoke_response,
                value=InvokeResponse(status=http_status_code, body=body),
            )
        )

    async def _exchanged_token(self, turn_context: TurnContext) -> bool:
        token_exchange_response: TokenResponse = None
        aux_dict = {}
        if turn_context.activity.value:
            for prop in ["id", "connection_name", "token", "properties"]:
                aux_dict[prop] = turn_context.activity.value.get(prop)
        token_exchange_request = TokenExchangeInvokeRequest(
            id=aux_dict["id"],
            connection_name=aux_dict["connection_name"],
            token=aux_dict["token"],
            properties=aux_dict["properties"],
        )
        try:
            adapter = turn_context.adapter
            if isinstance(turn_context.adapter, ExtendedUserTokenProvider):
                token_exchange_response = await adapter.exchange_token(
                    turn_context,
                    self._oauth_connection_name,
                    turn_context.activity.from_property.id,
                    TokenExchangeRequest(token=token_exchange_request.token),
                )
            else:
                raise Exception(
                    "Not supported: Token Exchange is not supported by the current adapter."
                )
        except:
            traceback.print_exc()
        if not token_exchange_response or not token_exchange_response.token:
            # The token could not be exchanged (which could be due to a consent requirement)
            # Notify the sender that PreconditionFailed so they can respond accordingly.

            invoke_response = TokenExchangeInvokeResponse(
                id=token_exchange_request.id,
                connection_name=self._oauth_connection_name,
                failure_detail="The bot is unable to exchange token. Proceed with regular login.",
            )

            await self._send_invoke_response(
                turn_context, invoke_response, HTTPStatus.PRECONDITION_FAILED
            )

            return False

        return True
