# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import re
from datetime import datetime, timedelta
from http import HTTPStatus
from typing import Union, Awaitable, Callable

from botframework.connector import Channels
from botframework.connector.auth import (
    ClaimsIdentity,
    SkillValidation,
    JwtTokenValidation,
)
from botbuilder.core import (
    CardFactory,
    MessageFactory,
    InvokeResponse,
    TurnContext,
    BotAdapter,
)
from botbuilder.core.bot_framework_adapter import TokenExchangeRequest
from botbuilder.dialogs import Dialog, DialogContext, DialogTurnResult
from botbuilder.schema import (
    Activity,
    ActivityTypes,
    ActionTypes,
    CardAction,
    InputHints,
    SigninCard,
    SignInConstants,
    OAuthCard,
    TokenResponse,
    TokenExchangeInvokeRequest,
    TokenExchangeInvokeResponse,
)

from .prompt_options import PromptOptions
from .oauth_prompt_settings import OAuthPromptSettings
from .prompt_validator_context import PromptValidatorContext
from .prompt_recognizer_result import PromptRecognizerResult

from .._user_token_access import _UserTokenAccess


class CallerInfo:
    def __init__(self, caller_service_url: str = None, scope: str = None):
        self.caller_service_url = caller_service_url
        self.scope = scope


class OAuthPrompt(Dialog):
    PERSISTED_OPTIONS = "options"
    PERSISTED_STATE = "state"
    PERSISTED_EXPIRES = "expires"
    PERSISTED_CALLER = "caller"

    """
    Creates a new prompt that asks the user to sign in, using the Bot Framework Single Sign On (SSO) service.

    .. remarks::
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

        You should avoid persisting the access token with your bots other state. The Bot Frameworks SSO service
        will securely store the token on your behalf. If you store it in your bots state,
        it could expire or be revoked in between turns.
        When calling the prompt from within a waterfall step, you should use the token within the step
        following the prompt and then let the token go out of scope at the end of your function.

        When used with your bots :class:`DialogSet`, you can simply add a new instance of the prompt as a named
        dialog using :meth`DialogSet.add()`.
        You can then start the prompt from a waterfall step using either :meth:`DialogContext.begin()` or
        :meth:`DialogContext.prompt()`.
        The user will be prompted to sign in as needed and their access token will be passed as an argument to
        the callers next waterfall step.
    """

    def __init__(
        self,
        dialog_id: str,
        settings: OAuthPromptSettings,
        validator: Callable[[PromptValidatorContext], Awaitable[bool]] = None,
    ):
        """
        Creates a new instance of the :class:`OAuthPrompt` class.

        :param dialog_id: The Id to assign to this prompt.
        :type dialog_id: str
        :param settings: Additional authentication settings to use with this instance of the prompt
        :type settings: :class:`OAuthPromptSettings`
        :param validator: Optional, contains additional, custom validation for this prompt
        :type validator: :class:`PromptValidatorContext`

        .. remarks::
            The value of :param dialogId: must be unique within the :class:`DialogSet`or :class:`ComponentDialog`
            to which the prompt is added.
        """
        super().__init__(dialog_id)
        self._validator = validator

        if not settings:
            raise TypeError(
                "OAuthPrompt.__init__(): OAuthPrompt requires OAuthPromptSettings."
            )

        self._settings = settings
        self._validator = validator

    async def begin_dialog(
        self, dialog_context: DialogContext, options: PromptOptions = None
    ) -> DialogTurnResult:
        """
        Starts an authentication prompt dialog. Called when an authentication prompt dialog is pushed onto the
        dialog stack and is being activated.

        :param dialog_context: The dialog context for the current turn of the conversation
        :type dialog_context:  :class:`DialogContext`
        :param options: Optional, additional information to pass to the prompt being started
        :type options: :class:`PromptOptions`

        :return: Dialog turn result
        :rtype: :class`:`DialogTurnResult`

        .. remarks::

            If the task is successful, the result indicates whether the prompt is still active after the turn
            has been processed.
        """
        if dialog_context is None:
            raise TypeError(
                f"OAuthPrompt.begin_dialog(): Expected DialogContext but got NoneType instead"
            )

        options = options or PromptOptions()

        # Ensure prompts have input hint set
        if options.prompt and not options.prompt.input_hint:
            options.prompt.input_hint = InputHints.accepting_input

        if options.retry_prompt and not options.retry_prompt.input_hint:
            options.retry_prompt.input_hint = InputHints.accepting_input

        # Initialize prompt state
        timeout = (
            self._settings.timeout
            if isinstance(self._settings.timeout, int)
            else 900000
        )
        state = dialog_context.active_dialog.state
        state[OAuthPrompt.PERSISTED_STATE] = {}
        state[OAuthPrompt.PERSISTED_OPTIONS] = options
        state[OAuthPrompt.PERSISTED_EXPIRES] = datetime.now() + timedelta(
            seconds=timeout / 1000
        )
        state[OAuthPrompt.PERSISTED_CALLER] = OAuthPrompt.__create_caller_info(
            dialog_context.context
        )

        output = await _UserTokenAccess.get_user_token(
            dialog_context.context, self._settings, None
        )

        if output is not None:
            # Return token
            return await dialog_context.end_dialog(output)

        await self._send_oauth_card(dialog_context.context, options.prompt)
        return Dialog.end_of_turn

    async def continue_dialog(self, dialog_context: DialogContext) -> DialogTurnResult:
        """
        Continues a dialog. Called when a prompt dialog is the active dialog and the user replied with a new activity.

        :param dialog_context: The dialog context for the current turn of the conversation
        :type dialog_context:  :class:`DialogContext`

        :return: Dialog turn result
        :rtype: :class:`DialogTurnResult`

        .. remarks::
            If the task is successful, the result indicates whether the dialog is still
            active after the turn has been processed by the dialog.
            The prompt generally continues to receive the user's replies until it accepts the
            user's reply as valid input for the prompt.
        """
        # Check for timeout
        state = dialog_context.active_dialog.state
        is_message = dialog_context.context.activity.type == ActivityTypes.message
        is_timeout_activity_type = (
            is_message
            or OAuthPrompt._is_token_response_event(dialog_context.context)
            or OAuthPrompt._is_teams_verification_invoke(dialog_context.context)
            or OAuthPrompt._is_token_exchange_request_invoke(dialog_context.context)
        )

        has_timed_out = is_timeout_activity_type and (
            datetime.now() > state[OAuthPrompt.PERSISTED_EXPIRES]
        )

        if has_timed_out:
            return await dialog_context.end_dialog(None)

        if state["state"].get("attemptCount") is None:
            state["state"]["attemptCount"] = 1
        else:
            state["state"]["attemptCount"] += 1

        # Recognize token
        recognized = await self._recognize_token(dialog_context)

        # Validate the return value
        is_valid = False
        if self._validator is not None:
            is_valid = await self._validator(
                PromptValidatorContext(
                    dialog_context.context,
                    recognized,
                    state[OAuthPrompt.PERSISTED_STATE],
                    state[OAuthPrompt.PERSISTED_OPTIONS],
                )
            )
        elif recognized.succeeded:
            is_valid = True

        # Return recognized value or re-prompt
        if is_valid:
            return await dialog_context.end_dialog(recognized.value)
        if is_message and self._settings.end_on_invalid_message:
            # If EndOnInvalidMessage is set, complete the prompt with no result.
            return await dialog_context.end_dialog(None)

        # Send retry prompt
        if (
            not dialog_context.context.responded
            and is_message
            and state[OAuthPrompt.PERSISTED_OPTIONS].retry_prompt is not None
        ):
            await dialog_context.context.send_activity(
                state[OAuthPrompt.PERSISTED_OPTIONS].retry_prompt
            )

        return Dialog.end_of_turn

    async def get_user_token(
        self, context: TurnContext, code: str = None
    ) -> TokenResponse:
        """
        Gets the user's tokeN.

        :param context: Context for the current turn of conversation with the user
        :type context:  :class:`TurnContext`
        :param code: (Optional) Optional user entered code to validate.
        :type code: str

        :return: A response that includes the user's token
        :rtype: :class:`TokenResponse`

        .. remarks::
            If the task is successful and the user already has a token or the user successfully signs in,
            the result contains the user's token.
        """
        return await _UserTokenAccess.get_user_token(context, self._settings, code)

    async def sign_out_user(self, context: TurnContext):
        """
        Signs out the user

        :param context: Context for the current turn of conversation with the user
        :type context:  :class:`TurnContext`
        :return: A task representing the work queued to execute

        .. remarks::
            If the task is successful and the user already has a token or the user successfully signs in,
            the result contains the user's token.
        """
        return await _UserTokenAccess.sign_out_user(context, self._settings)

    @staticmethod
    def __create_caller_info(context: TurnContext) -> CallerInfo:
        bot_identity = context.turn_state.get(BotAdapter.BOT_IDENTITY_KEY)
        if bot_identity and SkillValidation.is_skill_claim(bot_identity.claims):
            return CallerInfo(
                caller_service_url=context.activity.service_url,
                scope=JwtTokenValidation.get_app_id_from_claims(bot_identity.claims),
            )

        return None

    async def _send_oauth_card(
        self, context: TurnContext, prompt: Union[Activity, str] = None
    ):
        if not isinstance(prompt, Activity):
            prompt = MessageFactory.text(prompt or "", None, InputHints.accepting_input)
        else:
            prompt.input_hint = prompt.input_hint or InputHints.accepting_input

        prompt.attachments = prompt.attachments or []

        if OAuthPrompt._channel_suppports_oauth_card(context.activity.channel_id):
            if not any(
                att.content_type == CardFactory.content_types.oauth_card
                for att in prompt.attachments
            ):
                card_action_type = ActionTypes.signin
                sign_in_resource = await _UserTokenAccess.get_sign_in_resource(
                    context, self._settings
                )
                link = sign_in_resource.sign_in_link
                bot_identity: ClaimsIdentity = context.turn_state.get(
                    BotAdapter.BOT_IDENTITY_KEY
                )

                # use the SignInLink when in speech channel or bot is a skill or
                # an extra OAuthAppCredentials is being passed in
                if (
                    (
                        bot_identity
                        and SkillValidation.is_skill_claim(bot_identity.claims)
                    )
                    or not context.activity.service_url.startswith("http")
                    or self._settings.oath_app_credentials
                ):
                    if context.activity.channel_id == Channels.emulator:
                        card_action_type = ActionTypes.open_url
                elif not OAuthPrompt._channel_requires_sign_in_link(
                    context.activity.channel_id
                ):
                    link = None

                json_token_ex_resource = (
                    sign_in_resource.token_exchange_resource.as_dict()
                    if sign_in_resource.token_exchange_resource
                    else None
                )
                prompt.attachments.append(
                    CardFactory.oauth_card(
                        OAuthCard(
                            text=self._settings.text,
                            connection_name=self._settings.connection_name,
                            buttons=[
                                CardAction(
                                    title=self._settings.title,
                                    text=self._settings.text,
                                    type=card_action_type,
                                    value=link,
                                )
                            ],
                            token_exchange_resource=json_token_ex_resource,
                        )
                    )
                )
        else:
            if not any(
                att.content_type == CardFactory.content_types.signin_card
                for att in prompt.attachments
            ):
                if not hasattr(context.adapter, "get_oauth_sign_in_link"):
                    raise Exception(
                        "OAuthPrompt._send_oauth_card(): get_oauth_sign_in_link() not supported by the current adapter"
                    )

                link = await context.adapter.get_oauth_sign_in_link(
                    context,
                    self._settings.connection_name,
                    None,
                    self._settings.oath_app_credentials,
                )
                prompt.attachments.append(
                    CardFactory.signin_card(
                        SigninCard(
                            text=self._settings.text,
                            buttons=[
                                CardAction(
                                    title=self._settings.title,
                                    value=link,
                                    type=ActionTypes.signin,
                                )
                            ],
                        )
                    )
                )

        # Send prompt
        await context.send_activity(prompt)

    async def _recognize_token(
        self, dialog_context: DialogContext
    ) -> PromptRecognizerResult:
        context = dialog_context.context
        token = None
        if OAuthPrompt._is_token_response_event(context):
            token = context.activity.value

            # fixup the turnContext's state context if this was received from a skill host caller
            state: CallerInfo = dialog_context.active_dialog.state[
                OAuthPrompt.PERSISTED_CALLER
            ]
            if state:
                # set the ServiceUrl to the skill host's Url
                dialog_context.context.activity.service_url = state.caller_service_url
                claims_identity = context.turn_state.get(BotAdapter.BOT_IDENTITY_KEY)
                connector_client = await _UserTokenAccess.create_connector_client(
                    context,
                    dialog_context.context.activity.service_url,
                    claims_identity,
                    state.scope,
                )

                context.turn_state[BotAdapter.BOT_CONNECTOR_CLIENT_KEY] = (
                    connector_client
                )

        elif OAuthPrompt._is_teams_verification_invoke(context):
            code = context.activity.value["state"]
            try:
                token = await _UserTokenAccess.get_user_token(
                    context, self._settings, code
                )
                if token is not None:
                    await context.send_activity(
                        Activity(
                            type="invokeResponse",
                            value=InvokeResponse(status=HTTPStatus.OK),
                        )
                    )
                else:
                    await context.send_activity(
                        Activity(
                            type="invokeResponse",
                            value=InvokeResponse(status=HTTPStatus.NOT_FOUND),
                        )
                    )
            except Exception:
                await context.send_activity(
                    Activity(
                        type="invokeResponse",
                        value=InvokeResponse(status=HTTPStatus.INTERNAL_SERVER_ERROR),
                    )
                )
        elif self._is_token_exchange_request_invoke(context):
            if isinstance(context.activity.value, dict):
                context.activity.value = TokenExchangeInvokeRequest().from_dict(
                    context.activity.value
                )

            if not (
                context.activity.value
                and self._is_token_exchange_request(context.activity.value)
            ):
                # Received activity is not a token exchange request.
                await context.send_activity(
                    self._get_token_exchange_invoke_response(
                        int(HTTPStatus.BAD_REQUEST),
                        "The bot received an InvokeActivity that is missing a TokenExchangeInvokeRequest value."
                        " This is required to be sent with the InvokeActivity.",
                    )
                )
            elif (
                context.activity.value.connection_name != self._settings.connection_name
            ):
                # Connection name on activity does not match that of setting.
                await context.send_activity(
                    self._get_token_exchange_invoke_response(
                        int(HTTPStatus.BAD_REQUEST),
                        "The bot received an InvokeActivity with a TokenExchangeInvokeRequest containing a"
                        " ConnectionName that does not match the ConnectionName expected by the bots active"
                        " OAuthPrompt. Ensure these names match when sending the InvokeActivityInvalid"
                        " ConnectionName in the TokenExchangeInvokeRequest",
                    )
                )
            else:
                # No errors. Proceed with token exchange.
                token_exchange_response = None
                try:
                    token_exchange_response = await _UserTokenAccess.exchange_token(
                        context,
                        self._settings,
                        TokenExchangeRequest(token=context.activity.value.token),
                    )
                except:
                    # Ignore Exceptions
                    # If token exchange failed for any reason, tokenExchangeResponse above stays null, and
                    # hence we send back a failure invoke response to the caller.
                    pass

                if not token_exchange_response or not token_exchange_response.token:
                    await context.send_activity(
                        self._get_token_exchange_invoke_response(
                            int(HTTPStatus.PRECONDITION_FAILED),
                            "The bot is unable to exchange token. Proceed with regular login.",
                        )
                    )
                else:
                    await context.send_activity(
                        self._get_token_exchange_invoke_response(
                            int(HTTPStatus.OK), None, context.activity.value.id
                        )
                    )
                    token = TokenResponse(
                        channel_id=token_exchange_response.channel_id,
                        connection_name=token_exchange_response.connection_name,
                        token=token_exchange_response.token,
                        expiration=None,
                    )
        elif context.activity.type == ActivityTypes.message and context.activity.text:
            match = re.match(r"(?<!\d)\d{6}(?!\d)", context.activity.text)
            if match:
                token = await _UserTokenAccess.get_user_token(
                    context, self._settings, match[0]
                )

        return (
            PromptRecognizerResult(True, token)
            if token is not None
            else PromptRecognizerResult()
        )

    def _get_token_exchange_invoke_response(
        self, status: int, failure_detail: str, identifier: str = None
    ) -> Activity:
        return Activity(
            type=ActivityTypes.invoke_response,
            value=InvokeResponse(
                status=status,
                body=TokenExchangeInvokeResponse(
                    id=identifier,
                    connection_name=self._settings.connection_name,
                    failure_detail=failure_detail,
                ),
            ),
        )

    @staticmethod
    def _is_token_response_event(context: TurnContext) -> bool:
        activity = context.activity

        return (
            activity.type == ActivityTypes.event
            and activity.name == SignInConstants.token_response_event_name
        )

    @staticmethod
    def _is_teams_verification_invoke(context: TurnContext) -> bool:
        activity = context.activity

        return (
            activity.type == ActivityTypes.invoke
            and activity.name == SignInConstants.verify_state_operation_name
        )

    @staticmethod
    def _channel_suppports_oauth_card(channel_id: str) -> bool:
        if channel_id in [
            Channels.cortana,
            Channels.skype,
            Channels.skype_for_business,
        ]:
            return False

        return True

    @staticmethod
    def _channel_requires_sign_in_link(channel_id: str) -> bool:
        if channel_id in [Channels.ms_teams]:
            return True

        return False

    @staticmethod
    def _is_token_exchange_request_invoke(context: TurnContext) -> bool:
        activity = context.activity

        return (
            activity.type == ActivityTypes.invoke
            and activity.name == SignInConstants.token_exchange_operation_name
        )

    @staticmethod
    def _is_token_exchange_request(obj: TokenExchangeInvokeRequest) -> bool:
        return bool(obj.connection_name) and bool(obj.token)
