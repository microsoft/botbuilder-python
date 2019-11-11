# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Callable, Awaitable, List

from botbuilder.core import Middleware, UserState, TurnContext
from botbuilder.schema import Activity, ActivityTypes

from translation import MicrosoftTranslator
from translation.translation_settings import TranslationSettings

"""
Middleware for translating text between the user and bot.
Uses the Microsoft Translator Text API.
"""


class TranslationMiddleware(Middleware):
    def __init__(self, translator: MicrosoftTranslator, user_state: UserState):
        self.translator = translator
        self.language_preference_accessor = user_state.create_property("LanguagePreference")

    async def on_turn(
            self, turn_context: TurnContext, logic: Callable[[TurnContext], Awaitable]
    ):
        """
        Processes an incoming activity.
        :param turn_context:
        :param logic:
        :return:
        """
        translate = await self._should_translate(turn_context)
        if translate and turn_context.activity.type == ActivityTypes.message:
            turn_context.activity.text = await self.translator.translate(
                turn_context.activity.text, TranslationSettings.default_language.value
            )

        async def aux_on_send(
                context: TurnContext, activities: List[Activity], next_send: Callable
        ):
            user_language = await self.language_preference_accessor.get(
                context, TranslationSettings.default_language.value
            )
            should_translate = user_language != TranslationSettings.default_language.value

            # Translate messages sent to the user to user language
            if should_translate:
                for activity in activities:
                    await self._translate_message_activity(activity, user_language)

            return await next_send()

        async def aux_on_update(
                context: TurnContext, activity: Activity, next_update: Callable
        ):
            user_language = await self.language_preference_accessor.get(
                context, TranslationSettings.default_language.value
            )
            should_translate = user_language != TranslationSettings.default_language.value

            # Translate messages sent to the user to user language
            if should_translate and activity.type == ActivityTypes.message:
                await self._translate_message_activity(activity, user_language)

            return await next_update()

        turn_context.on_send_activities(aux_on_send)
        turn_context.on_update_activity(aux_on_update)

        await logic()

    async def _should_translate(self, turn_context: TurnContext) -> bool:
        user_language = await self.language_preference_accessor.get(turn_context, TranslationSettings.default_language.value)
        return user_language != TranslationSettings.default_language.value

    async def _translate_message_activity(self, activity: Activity, target_locale: str):
        if activity.type == ActivityTypes.message:
            activity.text = await self.translator.translate(activity.text, target_locale)
