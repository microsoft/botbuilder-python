# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List

from recognizers_text import Culture


class PromptCultureModel:
    """
    Culture model used in Choice and Confirm Prompts.
    """

    def __init__(
        self,
        locale: str,
        separator: str,
        inline_or: str,
        inline_or_more: str,
        yes_in_language: str,
        no_in_language: str,
    ):
        """

        :param locale: Culture Model's Locale. Example: "en-US".
        :param separator: Culture Model's Inline Separator. Example: ", ".
        :param inline_or: Culture Model's Inline Or. Example: " or ".
        :param inline_or_more Culture Model's Inline Or More. Example: ", or ".
        :param yes_in_language: Equivalent of "Yes" in Culture Model's Language. Example: "Yes".
        :param no_in_language: Equivalent of "No" in Culture Model's Language. Example: "No".
        """
        self.locale = locale
        self.separator = separator
        self.inline_or = inline_or
        self.inline_or_more = inline_or_more
        self.yes_in_language = yes_in_language
        self.no_in_language = no_in_language


class PromptCultureModels:
    """
    Class container for currently-supported Culture Models in Confirm and Choice Prompt.
    """

    Chinese = PromptCultureModel(
        locale=Culture.Chinese,
        inline_or=" 要么 ",
        inline_or_more="， 要么 ",
        separator="， ",
        no_in_language="不",
        yes_in_language="是的",
    )

    Dutch = PromptCultureModel(
        locale=Culture.Dutch,
        inline_or=" of ",
        inline_or_more=", of ",
        separator=", ",
        no_in_language="Nee",
        yes_in_language="Ja",
    )

    English = PromptCultureModel(
        locale=Culture.English,
        inline_or=" or ",
        inline_or_more=", or ",
        separator=", ",
        no_in_language="No",
        yes_in_language="Yes",
    )

    French = PromptCultureModel(
        locale=Culture.French,
        inline_or=" ou ",
        inline_or_more=", ou ",
        separator=", ",
        no_in_language="Non",
        yes_in_language="Oui",
    )

    German = PromptCultureModel(
        # TODO: Replace with Culture.German after Recognizers-Text package updates.
        locale="de-de",
        inline_or=" oder ",
        inline_or_more=", oder ",
        separator=", ",
        no_in_language="Nein",
        yes_in_language="Ja",
    )

    Italian = PromptCultureModel(
        locale=Culture.Italian,
        inline_or=" o ",
        inline_or_more=" o ",
        separator=", ",
        no_in_language="No",
        yes_in_language="Si",
    )

    Japanese = PromptCultureModel(
        locale=Culture.Japanese,
        inline_or=" または ",
        inline_or_more="、 または ",
        separator="、 ",
        no_in_language="いいえ",
        yes_in_language="はい",
    )

    Korean = PromptCultureModel(
        locale=Culture.Korean,
        inline_or=" 또는 ",
        inline_or_more=" 또는 ",
        separator=", ",
        no_in_language="아니",
        yes_in_language="예",
    )

    Portuguese = PromptCultureModel(
        locale=Culture.Portuguese,
        inline_or=" ou ",
        inline_or_more=", ou ",
        separator=", ",
        no_in_language="Não",
        yes_in_language="Sim",
    )

    Spanish = PromptCultureModel(
        locale=Culture.Spanish,
        inline_or=" o ",
        inline_or_more=", o ",
        separator=", ",
        no_in_language="No",
        yes_in_language="Sí",
    )

    Turkish = PromptCultureModel(
        locale=Culture.Turkish,
        inline_or=" veya ",
        inline_or_more=" veya ",
        separator=", ",
        no_in_language="Hayır",
        yes_in_language="Evet",
    )

    @classmethod
    def map_to_nearest_language(cls, culture_code: str) -> str:
        """
        Normalize various potential locale strings to a standard.
        :param culture_code: Represents locale. Examples: "en-US, en-us, EN".
        :return: Normalized locale.
        :rtype: str

        .. remarks::
            In our other SDKs, this method is a copy/paste of the ones from the Recognizers-Text library.
            However, that doesn't exist in Python.
        """
        if culture_code:
            culture_code = culture_code.lower()
            supported_culture_codes = cls._get_supported_locales()

            if culture_code not in supported_culture_codes:
                culture_prefix = culture_code.split("-")[0]

                for supported_culture_code in supported_culture_codes:
                    if supported_culture_code.startswith(culture_prefix):
                        culture_code = supported_culture_code

        return culture_code

    @classmethod
    def get_supported_cultures(cls) -> List[PromptCultureModel]:
        """
        Gets a list of the supported culture models.
        """
        return [
            cls.Chinese,
            cls.German,
            cls.Dutch,
            cls.English,
            cls.French,
            cls.Italian,
            cls.Japanese,
            cls.Korean,
            cls.Portuguese,
            cls.Spanish,
            cls.Turkish,
        ]

    @classmethod
    def _get_supported_locales(cls) -> List[str]:
        return [c.locale for c in cls.get_supported_cultures()]
