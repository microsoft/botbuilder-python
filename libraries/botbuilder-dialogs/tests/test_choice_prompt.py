# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List

import aiounittest
from recognizers_text import Culture

from botbuilder.core import CardFactory, ConversationState, MemoryStorage, TurnContext
from botbuilder.core.adapters import TestAdapter
from botbuilder.dialogs import (
    DialogSet,
    DialogTurnResult,
    DialogTurnStatus,
    ChoiceRecognizers,
    FindChoicesOptions,
)
from botbuilder.dialogs.choices import Choice, ChoiceFactoryOptions, ListStyle
from botbuilder.dialogs.prompts import (
    ChoicePrompt,
    PromptCultureModel,
    PromptOptions,
    PromptValidatorContext,
)
from botbuilder.schema import Activity, ActivityTypes

_color_choices: List[Choice] = [
    Choice(value="red"),
    Choice(value="green"),
    Choice(value="blue"),
]

_answer_message: Activity = Activity(text="red", type=ActivityTypes.message)
_invalid_message: Activity = Activity(text="purple", type=ActivityTypes.message)


class ChoicePromptTest(aiounittest.AsyncTestCase):
    def test_choice_prompt_with_empty_id_should_fail(self):
        empty_id = ""

        with self.assertRaises(TypeError):
            ChoicePrompt(empty_id)

    def test_choice_prompt_with_none_id_should_fail(self):
        none_id = None

        with self.assertRaises(TypeError):
            ChoicePrompt(none_id)

    async def test_should_call_choice_prompt_using_dc_prompt(self):
        async def exec_test(turn_context: TurnContext):
            dialog_context = await dialogs.create_context(turn_context)

            results: DialogTurnResult = await dialog_context.continue_dialog()

            if results.status == DialogTurnStatus.Empty:
                options = PromptOptions(
                    prompt=Activity(
                        type=ActivityTypes.message, text="Please choose a color."
                    ),
                    choices=_color_choices,
                )
                await dialog_context.prompt("ChoicePrompt", options)
            elif results.status == DialogTurnStatus.Complete:
                selected_choice = results.result
                await turn_context.send_activity(selected_choice.value)

            await convo_state.save_changes(turn_context)

        # Initialize TestAdapter.
        adapter = TestAdapter(exec_test)

        # Create new ConversationState with MemoryStorage and register the state as middleware.
        convo_state = ConversationState(MemoryStorage())

        # Create a DialogState property, DialogSet, and ChoicePrompt.
        dialog_state = convo_state.create_property("dialogState")
        dialogs = DialogSet(dialog_state)
        choice_prompt = ChoicePrompt("ChoicePrompt")
        dialogs.add(choice_prompt)

        step1 = await adapter.send("hello")
        step2 = await step1.assert_reply(
            "Please choose a color. (1) red, (2) green, or (3) blue"
        )
        step3 = await step2.send(_answer_message)
        await step3.assert_reply("red")

    async def test_should_call_choice_prompt_with_custom_validator(self):
        async def exec_test(turn_context: TurnContext):
            dialog_context = await dialogs.create_context(turn_context)

            results: DialogTurnResult = await dialog_context.continue_dialog()

            if results.status == DialogTurnStatus.Empty:
                options = PromptOptions(
                    prompt=Activity(
                        type=ActivityTypes.message, text="Please choose a color."
                    ),
                    choices=_color_choices,
                )
                await dialog_context.prompt("prompt", options)
            elif results.status == DialogTurnStatus.Complete:
                selected_choice = results.result
                await turn_context.send_activity(selected_choice.value)

            await convo_state.save_changes(turn_context)

        adapter = TestAdapter(exec_test)

        convo_state = ConversationState(MemoryStorage())
        dialog_state = convo_state.create_property("dialogState")
        dialogs = DialogSet(dialog_state)

        async def validator(prompt: PromptValidatorContext) -> bool:
            assert prompt

            return prompt.recognized.succeeded

        choice_prompt = ChoicePrompt("prompt", validator)

        dialogs.add(choice_prompt)

        step1 = await adapter.send("Hello")
        step2 = await step1.assert_reply(
            "Please choose a color. (1) red, (2) green, or (3) blue"
        )
        step3 = await step2.send(_invalid_message)
        step4 = await step3.assert_reply(
            "Please choose a color. (1) red, (2) green, or (3) blue"
        )
        step5 = await step4.send(_answer_message)
        await step5.assert_reply("red")

    async def test_should_send_custom_retry_prompt(self):
        async def exec_test(turn_context: TurnContext):
            dialog_context = await dialogs.create_context(turn_context)

            results: DialogTurnResult = await dialog_context.continue_dialog()

            if results.status == DialogTurnStatus.Empty:
                options = PromptOptions(
                    prompt=Activity(
                        type=ActivityTypes.message, text="Please choose a color."
                    ),
                    retry_prompt=Activity(
                        type=ActivityTypes.message,
                        text="Please choose red, blue, or green.",
                    ),
                    choices=_color_choices,
                )
                await dialog_context.prompt("prompt", options)
            elif results.status == DialogTurnStatus.Complete:
                selected_choice = results.result
                await turn_context.send_activity(selected_choice.value)

            await convo_state.save_changes(turn_context)

        adapter = TestAdapter(exec_test)

        convo_state = ConversationState(MemoryStorage())
        dialog_state = convo_state.create_property("dialogState")
        dialogs = DialogSet(dialog_state)
        choice_prompt = ChoicePrompt("prompt")
        dialogs.add(choice_prompt)

        step1 = await adapter.send("Hello")
        step2 = await step1.assert_reply(
            "Please choose a color. (1) red, (2) green, or (3) blue"
        )
        step3 = await step2.send(_invalid_message)
        step4 = await step3.assert_reply(
            "Please choose red, blue, or green. (1) red, (2) green, or (3) blue"
        )
        step5 = await step4.send(_answer_message)
        await step5.assert_reply("red")

    async def test_should_send_ignore_retry_prompt_if_validator_replies(self):
        async def exec_test(turn_context: TurnContext):
            dialog_context = await dialogs.create_context(turn_context)

            results: DialogTurnResult = await dialog_context.continue_dialog()

            if results.status == DialogTurnStatus.Empty:
                options = PromptOptions(
                    prompt=Activity(
                        type=ActivityTypes.message, text="Please choose a color."
                    ),
                    retry_prompt=Activity(
                        type=ActivityTypes.message,
                        text="Please choose red, blue, or green.",
                    ),
                    choices=_color_choices,
                )
                await dialog_context.prompt("prompt", options)
            elif results.status == DialogTurnStatus.Complete:
                selected_choice = results.result
                await turn_context.send_activity(selected_choice.value)

            await convo_state.save_changes(turn_context)

        adapter = TestAdapter(exec_test)

        convo_state = ConversationState(MemoryStorage())
        dialog_state = convo_state.create_property("dialogState")
        dialogs = DialogSet(dialog_state)

        async def validator(prompt: PromptValidatorContext) -> bool:
            assert prompt

            if not prompt.recognized.succeeded:
                await prompt.context.send_activity("Bad input.")

            return prompt.recognized.succeeded

        choice_prompt = ChoicePrompt("prompt", validator)

        dialogs.add(choice_prompt)

        step1 = await adapter.send("Hello")
        step2 = await step1.assert_reply(
            "Please choose a color. (1) red, (2) green, or (3) blue"
        )
        step3 = await step2.send(_invalid_message)
        step4 = await step3.assert_reply("Bad input.")
        step5 = await step4.send(_answer_message)
        await step5.assert_reply("red")

    async def test_should_use_default_locale_when_rendering_choices(self):
        async def exec_test(turn_context: TurnContext):
            dialog_context = await dialogs.create_context(turn_context)

            results: DialogTurnResult = await dialog_context.continue_dialog()

            if results.status == DialogTurnStatus.Empty:
                options = PromptOptions(
                    prompt=Activity(
                        type=ActivityTypes.message, text="Please choose a color."
                    ),
                    choices=_color_choices,
                )
                await dialog_context.prompt("prompt", options)
            elif results.status == DialogTurnStatus.Complete:
                selected_choice = results.result
                await turn_context.send_activity(selected_choice.value)

            await convo_state.save_changes(turn_context)

        adapter = TestAdapter(exec_test)

        convo_state = ConversationState(MemoryStorage())
        dialog_state = convo_state.create_property("dialogState")
        dialogs = DialogSet(dialog_state)

        async def validator(prompt: PromptValidatorContext) -> bool:
            assert prompt

            if not prompt.recognized.succeeded:
                await prompt.context.send_activity("Bad input.")

            return prompt.recognized.succeeded

        choice_prompt = ChoicePrompt(
            "prompt", validator, default_locale=Culture.Spanish
        )

        dialogs.add(choice_prompt)

        step1 = await adapter.send(Activity(type=ActivityTypes.message, text="Hello"))
        step2 = await step1.assert_reply(
            "Please choose a color. (1) red, (2) green, o (3) blue"
        )
        step3 = await step2.send(_invalid_message)
        step4 = await step3.assert_reply("Bad input.")
        step5 = await step4.send(Activity(type=ActivityTypes.message, text="red"))
        await step5.assert_reply("red")

    async def test_should_use_context_activity_locale_when_rendering_choices(self):
        async def exec_test(turn_context: TurnContext):
            dialog_context = await dialogs.create_context(turn_context)

            results: DialogTurnResult = await dialog_context.continue_dialog()

            if results.status == DialogTurnStatus.Empty:
                options = PromptOptions(
                    prompt=Activity(
                        type=ActivityTypes.message, text="Please choose a color."
                    ),
                    choices=_color_choices,
                )
                await dialog_context.prompt("prompt", options)
            elif results.status == DialogTurnStatus.Complete:
                selected_choice = results.result
                await turn_context.send_activity(selected_choice.value)

            await convo_state.save_changes(turn_context)

        adapter = TestAdapter(exec_test)

        convo_state = ConversationState(MemoryStorage())
        dialog_state = convo_state.create_property("dialogState")
        dialogs = DialogSet(dialog_state)

        async def validator(prompt: PromptValidatorContext) -> bool:
            assert prompt

            if not prompt.recognized.succeeded:
                await prompt.context.send_activity("Bad input.")

            return prompt.recognized.succeeded

        choice_prompt = ChoicePrompt("prompt", validator)
        dialogs.add(choice_prompt)

        step1 = await adapter.send(
            Activity(type=ActivityTypes.message, text="Hello", locale=Culture.Spanish)
        )
        step2 = await step1.assert_reply(
            "Please choose a color. (1) red, (2) green, o (3) blue"
        )
        step3 = await step2.send(_answer_message)
        await step3.assert_reply("red")

    async def test_should_use_context_activity_locale_over_default_locale_when_rendering_choices(
        self,
    ):
        async def exec_test(turn_context: TurnContext):
            dialog_context = await dialogs.create_context(turn_context)

            results: DialogTurnResult = await dialog_context.continue_dialog()

            if results.status == DialogTurnStatus.Empty:
                options = PromptOptions(
                    prompt=Activity(
                        type=ActivityTypes.message, text="Please choose a color."
                    ),
                    choices=_color_choices,
                )
                await dialog_context.prompt("prompt", options)
            elif results.status == DialogTurnStatus.Complete:
                selected_choice = results.result
                await turn_context.send_activity(selected_choice.value)

            await convo_state.save_changes(turn_context)

        adapter = TestAdapter(exec_test)

        convo_state = ConversationState(MemoryStorage())
        dialog_state = convo_state.create_property("dialogState")
        dialogs = DialogSet(dialog_state)

        async def validator(prompt: PromptValidatorContext) -> bool:
            assert prompt

            if not prompt.recognized.succeeded:
                await prompt.context.send_activity("Bad input.")

            return prompt.recognized.succeeded

        choice_prompt = ChoicePrompt(
            "prompt", validator, default_locale=Culture.Spanish
        )
        dialogs.add(choice_prompt)

        step1 = await adapter.send(
            Activity(type=ActivityTypes.message, text="Hello", locale=Culture.English)
        )
        step2 = await step1.assert_reply(
            "Please choose a color. (1) red, (2) green, or (3) blue"
        )
        step3 = await step2.send(_answer_message)
        await step3.assert_reply("red")

    async def test_should_default_to_english_locale(self):
        async def exec_test(turn_context: TurnContext):
            dialog_context = await dialogs.create_context(turn_context)

            results: DialogTurnResult = await dialog_context.continue_dialog()

            if results.status == DialogTurnStatus.Empty:
                options = PromptOptions(
                    prompt=Activity(
                        type=ActivityTypes.message, text="Please choose a color."
                    ),
                    choices=_color_choices,
                )
                await dialog_context.prompt("prompt", options)
            elif results.status == DialogTurnStatus.Complete:
                selected_choice = results.result
                await turn_context.send_activity(selected_choice.value)

            await convo_state.save_changes(turn_context)

        async def validator(prompt: PromptValidatorContext) -> bool:
            assert prompt

            if not prompt.recognized.succeeded:
                await prompt.context.send_activity("Bad input.")

            return prompt.recognized.succeeded

        locales = [None, "", "not-supported"]

        for locale in locales:
            adapter = TestAdapter(exec_test)

            convo_state = ConversationState(MemoryStorage())
            dialog_state = convo_state.create_property("dialogState")
            dialogs = DialogSet(dialog_state)

            choice_prompt = ChoicePrompt("prompt", validator)
            dialogs.add(choice_prompt)

            step1 = await adapter.send(
                Activity(type=ActivityTypes.message, text="Hello", locale=locale)
            )
            step2 = await step1.assert_reply(
                "Please choose a color. (1) red, (2) green, or (3) blue"
            )
            step3 = await step2.send(_answer_message)
            await step3.assert_reply("red")

    async def test_should_recognize_locale_variations_of_correct_locales(self):
        def cap_ending(locale: str) -> str:
            return f"{locale.split('-')[0]}-{locale.split('-')[1].upper()}"

        def title_ending(locale: str) -> str:
            return locale[:3] + locale[3].upper() + locale[4:]

        def cap_two_letter(locale: str) -> str:
            return locale.split("-")[0].upper()

        def lower_two_letter(locale: str) -> str:
            return locale.split("-")[0].upper()

        async def exec_test_for_locale(valid_locale: str, locale_variations: List):
            # Hold the correct answer from when a valid locale is used
            expected_answer = None

            def inspector(activity: Activity, description: str):
                nonlocal expected_answer

                assert not description

                if valid_locale == test_locale:
                    expected_answer = activity.text
                else:
                    # Ensure we're actually testing a variation.
                    assert activity.locale != valid_locale

                assert activity.text == expected_answer
                return True

            async def exec_test(turn_context: TurnContext):
                dialog_context = await dialogs.create_context(turn_context)

                results: DialogTurnResult = await dialog_context.continue_dialog()

                if results.status == DialogTurnStatus.Empty:
                    options = PromptOptions(
                        prompt=Activity(
                            type=ActivityTypes.message, text="Please choose a color."
                        ),
                        choices=_color_choices,
                    )
                    await dialog_context.prompt("prompt", options)
                elif results.status == DialogTurnStatus.Complete:
                    selected_choice = results.result
                    await turn_context.send_activity(selected_choice.value)

                await convo_state.save_changes(turn_context)

            async def validator(prompt: PromptValidatorContext) -> bool:
                assert prompt

                if not prompt.recognized.succeeded:
                    await prompt.context.send_activity("Bad input.")

                return prompt.recognized.succeeded

            test_locale = None
            for test_locale in locale_variations:
                adapter = TestAdapter(exec_test)

                convo_state = ConversationState(MemoryStorage())
                dialog_state = convo_state.create_property("dialogState")
                dialogs = DialogSet(dialog_state)

                choice_prompt = ChoicePrompt("prompt", validator)
                dialogs.add(choice_prompt)

                step1 = await adapter.send(
                    Activity(
                        type=ActivityTypes.message, text="Hello", locale=test_locale
                    )
                )
                await step1.assert_reply(inspector)

        locales = [
            "zh-cn",
            "nl-nl",
            "en-us",
            "fr-fr",
            "de-de",
            "it-it",
            "ja-jp",
            "ko-kr",
            "pt-br",
            "es-es",
            "tr-tr",
            "de-de",
        ]

        locale_tests = []
        for locale in locales:
            locale_tests.append(
                [
                    locale,
                    cap_ending(locale),
                    title_ending(locale),
                    cap_two_letter(locale),
                    lower_two_letter(locale),
                ]
            )

        # Test each valid locale
        for locale_tests in locale_tests:
            await exec_test_for_locale(locale_tests[0], locale_tests)

    async def test_should_recognize_and_use_custom_locale_dict(
        self,
    ):
        async def exec_test(turn_context: TurnContext):
            dialog_context = await dialogs.create_context(turn_context)

            results: DialogTurnResult = await dialog_context.continue_dialog()

            if results.status == DialogTurnStatus.Empty:
                options = PromptOptions(
                    prompt=Activity(
                        type=ActivityTypes.message, text="Please choose a color."
                    ),
                    choices=_color_choices,
                )
                await dialog_context.prompt("prompt", options)
            elif results.status == DialogTurnStatus.Complete:
                selected_choice = results.result
                await turn_context.send_activity(selected_choice.value)

            await convo_state.save_changes(turn_context)

        async def validator(prompt: PromptValidatorContext) -> bool:
            assert prompt

            if not prompt.recognized.succeeded:
                await prompt.context.send_activity("Bad input.")

            return prompt.recognized.succeeded

        adapter = TestAdapter(exec_test)

        convo_state = ConversationState(MemoryStorage())
        dialog_state = convo_state.create_property("dialogState")
        dialogs = DialogSet(dialog_state)

        culture = PromptCultureModel(
            locale="custom-locale",
            no_in_language="customNo",
            yes_in_language="customYes",
            separator="customSeparator",
            inline_or="customInlineOr",
            inline_or_more="customInlineOrMore",
        )

        custom_dict = {
            culture.locale: ChoiceFactoryOptions(
                inline_or=culture.inline_or,
                inline_or_more=culture.inline_or_more,
                inline_separator=culture.separator,
                include_numbers=True,
            )
        }

        choice_prompt = ChoicePrompt("prompt", validator, choice_defaults=custom_dict)
        dialogs.add(choice_prompt)

        step1 = await adapter.send(
            Activity(type=ActivityTypes.message, text="Hello", locale=culture.locale)
        )
        await step1.assert_reply(
            "Please choose a color. (1) redcustomSeparator(2) greencustomInlineOrMore(3) blue"
        )

    async def test_should_not_render_choices_if_list_style_none_is_specified(self):
        async def exec_test(turn_context: TurnContext):
            dialog_context = await dialogs.create_context(turn_context)

            results: DialogTurnResult = await dialog_context.continue_dialog()

            if results.status == DialogTurnStatus.Empty:
                options = PromptOptions(
                    prompt=Activity(
                        type=ActivityTypes.message, text="Please choose a color."
                    ),
                    choices=_color_choices,
                    style=ListStyle.none,
                )
                await dialog_context.prompt("prompt", options)
            elif results.status == DialogTurnStatus.Complete:
                selected_choice = results.result
                await turn_context.send_activity(selected_choice.value)

            await convo_state.save_changes(turn_context)

        adapter = TestAdapter(exec_test)

        convo_state = ConversationState(MemoryStorage())
        dialog_state = convo_state.create_property("dialogState")
        dialogs = DialogSet(dialog_state)

        choice_prompt = ChoicePrompt("prompt")

        dialogs.add(choice_prompt)

        step1 = await adapter.send("Hello")
        step2 = await step1.assert_reply("Please choose a color.")
        step3 = await step2.send(_answer_message)
        await step3.assert_reply("red")

    async def test_should_create_prompt_with_inline_choices_when_specified(self):
        async def exec_test(turn_context: TurnContext):
            dialog_context = await dialogs.create_context(turn_context)

            results: DialogTurnResult = await dialog_context.continue_dialog()

            if results.status == DialogTurnStatus.Empty:
                options = PromptOptions(
                    prompt=Activity(
                        type=ActivityTypes.message, text="Please choose a color."
                    ),
                    choices=_color_choices,
                )
                await dialog_context.prompt("prompt", options)
            elif results.status == DialogTurnStatus.Complete:
                selected_choice = results.result
                await turn_context.send_activity(selected_choice.value)

            await convo_state.save_changes(turn_context)

        adapter = TestAdapter(exec_test)

        convo_state = ConversationState(MemoryStorage())
        dialog_state = convo_state.create_property("dialogState")
        dialogs = DialogSet(dialog_state)

        choice_prompt = ChoicePrompt("prompt")
        choice_prompt.style = ListStyle.in_line

        dialogs.add(choice_prompt)

        step1 = await adapter.send("Hello")
        step2 = await step1.assert_reply(
            "Please choose a color. (1) red, (2) green, or (3) blue"
        )
        step3 = await step2.send(_answer_message)
        await step3.assert_reply("red")

    async def test_should_create_prompt_with_list_choices_when_specified(self):
        async def exec_test(turn_context: TurnContext):
            dialog_context = await dialogs.create_context(turn_context)

            results: DialogTurnResult = await dialog_context.continue_dialog()

            if results.status == DialogTurnStatus.Empty:
                options = PromptOptions(
                    prompt=Activity(
                        type=ActivityTypes.message, text="Please choose a color."
                    ),
                    choices=_color_choices,
                )
                await dialog_context.prompt("prompt", options)
            elif results.status == DialogTurnStatus.Complete:
                selected_choice = results.result
                await turn_context.send_activity(selected_choice.value)

            await convo_state.save_changes(turn_context)

        adapter = TestAdapter(exec_test)

        convo_state = ConversationState(MemoryStorage())
        dialog_state = convo_state.create_property("dialogState")
        dialogs = DialogSet(dialog_state)

        choice_prompt = ChoicePrompt("prompt")
        choice_prompt.style = ListStyle.list_style

        dialogs.add(choice_prompt)

        step1 = await adapter.send("Hello")
        step2 = await step1.assert_reply(
            "Please choose a color.\n\n   1. red\n   2. green\n   3. blue"
        )
        step3 = await step2.send(_answer_message)
        await step3.assert_reply("red")

    async def test_should_create_prompt_with_suggested_action_style_when_specified(
        self,
    ):
        async def exec_test(turn_context: TurnContext):
            dialog_context = await dialogs.create_context(turn_context)

            results: DialogTurnResult = await dialog_context.continue_dialog()

            if results.status == DialogTurnStatus.Empty:
                options = PromptOptions(
                    prompt=Activity(
                        type=ActivityTypes.message, text="Please choose a color."
                    ),
                    choices=_color_choices,
                    style=ListStyle.suggested_action,
                )
                await dialog_context.prompt("prompt", options)
            elif results.status == DialogTurnStatus.Complete:
                selected_choice = results.result
                await turn_context.send_activity(selected_choice.value)

            await convo_state.save_changes(turn_context)

        adapter = TestAdapter(exec_test)

        convo_state = ConversationState(MemoryStorage())
        dialog_state = convo_state.create_property("dialogState")
        dialogs = DialogSet(dialog_state)

        choice_prompt = ChoicePrompt("prompt")

        dialogs.add(choice_prompt)

        step1 = await adapter.send("Hello")
        step2 = await step1.assert_reply("Please choose a color.")
        step3 = await step2.send(_answer_message)
        await step3.assert_reply("red")

    async def test_should_create_prompt_with_auto_style_when_specified(self):
        async def exec_test(turn_context: TurnContext):
            dialog_context = await dialogs.create_context(turn_context)

            results: DialogTurnResult = await dialog_context.continue_dialog()

            if results.status == DialogTurnStatus.Empty:
                options = PromptOptions(
                    prompt=Activity(
                        type=ActivityTypes.message, text="Please choose a color."
                    ),
                    choices=_color_choices,
                    style=ListStyle.auto,
                )
                await dialog_context.prompt("prompt", options)
            elif results.status == DialogTurnStatus.Complete:
                selected_choice = results.result
                await turn_context.send_activity(selected_choice.value)

            await convo_state.save_changes(turn_context)

        adapter = TestAdapter(exec_test)

        convo_state = ConversationState(MemoryStorage())
        dialog_state = convo_state.create_property("dialogState")
        dialogs = DialogSet(dialog_state)

        choice_prompt = ChoicePrompt("prompt")

        dialogs.add(choice_prompt)

        step1 = await adapter.send("Hello")
        step2 = await step1.assert_reply(
            "Please choose a color. (1) red, (2) green, or (3) blue"
        )
        step3 = await step2.send(_answer_message)
        await step3.assert_reply("red")

    async def test_should_recognize_valid_number_choice(self):
        async def exec_test(turn_context: TurnContext):
            dialog_context = await dialogs.create_context(turn_context)

            results: DialogTurnResult = await dialog_context.continue_dialog()

            if results.status == DialogTurnStatus.Empty:
                options = PromptOptions(
                    prompt=Activity(
                        type=ActivityTypes.message, text="Please choose a color."
                    ),
                    choices=_color_choices,
                )
                await dialog_context.prompt("prompt", options)
            elif results.status == DialogTurnStatus.Complete:
                selected_choice = results.result
                await turn_context.send_activity(selected_choice.value)

            await convo_state.save_changes(turn_context)

        adapter = TestAdapter(exec_test)

        convo_state = ConversationState(MemoryStorage())
        dialog_state = convo_state.create_property("dialogState")
        dialogs = DialogSet(dialog_state)

        choice_prompt = ChoicePrompt("prompt")

        dialogs.add(choice_prompt)

        step1 = await adapter.send("Hello")
        step2 = await step1.assert_reply(
            "Please choose a color. (1) red, (2) green, or (3) blue"
        )
        step3 = await step2.send("1")
        await step3.assert_reply("red")

    async def test_should_display_choices_on_hero_card(self):
        size_choices = ["large", "medium", "small"]

        async def exec_test(turn_context: TurnContext):
            dialog_context = await dialogs.create_context(turn_context)

            results: DialogTurnResult = await dialog_context.continue_dialog()

            if results.status == DialogTurnStatus.Empty:
                options = PromptOptions(
                    prompt=Activity(
                        type=ActivityTypes.message, text="Please choose a size."
                    ),
                    choices=size_choices,
                )
                await dialog_context.prompt("prompt", options)
            elif results.status == DialogTurnStatus.Complete:
                selected_choice = results.result
                await turn_context.send_activity(selected_choice.value)

            await convo_state.save_changes(turn_context)

        def assert_expected_activity(
            activity: Activity, description
        ):  # pylint: disable=unused-argument
            assert len(activity.attachments) == 1
            assert (
                activity.attachments[0].content_type
                == CardFactory.content_types.hero_card
            )
            assert activity.attachments[0].content.text == "Please choose a size."

        adapter = TestAdapter(exec_test)

        convo_state = ConversationState(MemoryStorage())
        dialog_state = convo_state.create_property("dialogState")
        dialogs = DialogSet(dialog_state)

        choice_prompt = ChoicePrompt("prompt")

        # Change the ListStyle of the prompt to ListStyle.none.
        choice_prompt.style = ListStyle.hero_card

        dialogs.add(choice_prompt)

        step1 = await adapter.send("Hello")
        step2 = await step1.assert_reply(assert_expected_activity)
        step3 = await step2.send("1")
        await step3.assert_reply(size_choices[0])

    async def test_should_display_choices_on_hero_card_with_additional_attachment(self):
        size_choices = ["large", "medium", "small"]
        card = CardFactory.adaptive_card(
            {
                "type": "AdaptiveCard",
                "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                "version": "1.2",
                "body": [],
            }
        )
        card_activity = Activity(attachments=[card])

        async def exec_test(turn_context: TurnContext):
            dialog_context = await dialogs.create_context(turn_context)

            results: DialogTurnResult = await dialog_context.continue_dialog()

            if results.status == DialogTurnStatus.Empty:
                options = PromptOptions(prompt=card_activity, choices=size_choices)
                await dialog_context.prompt("prompt", options)
            elif results.status == DialogTurnStatus.Complete:
                selected_choice = results.result
                await turn_context.send_activity(selected_choice.value)

            await convo_state.save_changes(turn_context)

        def assert_expected_activity(
            activity: Activity, description
        ):  # pylint: disable=unused-argument
            assert len(activity.attachments) == 2
            assert (
                activity.attachments[0].content_type
                == CardFactory.content_types.adaptive_card
            )
            assert (
                activity.attachments[1].content_type
                == CardFactory.content_types.hero_card
            )

        adapter = TestAdapter(exec_test)

        convo_state = ConversationState(MemoryStorage())
        dialog_state = convo_state.create_property("dialogState")
        dialogs = DialogSet(dialog_state)

        choice_prompt = ChoicePrompt("prompt")

        # Change the ListStyle of the prompt to ListStyle.none.
        choice_prompt.style = ListStyle.hero_card

        dialogs.add(choice_prompt)

        step1 = await adapter.send("Hello")
        await step1.assert_reply(assert_expected_activity)

    async def test_should_not_find_a_choice_in_an_utterance_by_ordinal(self):
        found = ChoiceRecognizers.recognize_choices(
            "the first one please",
            _color_choices,
            FindChoicesOptions(recognize_numbers=False, recognize_ordinals=False),
        )
        assert not found

    async def test_should_not_find_a_choice_in_an_utterance_by_numerical_index(self):
        found = ChoiceRecognizers.recognize_choices(
            "one",
            _color_choices,
            FindChoicesOptions(recognize_numbers=False, recognize_ordinals=False),
        )
        assert not found
