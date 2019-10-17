# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.


class ChoiceFactoryOptions:
    def __init__(
        self,
        inline_separator: str = None,
        inline_or: str = None,
        inline_or_more: str = None,
        include_numbers: bool = None,
    ) -> None:
        """Initializes a new instance.
        Refer to the code in the ConfirmPrompt for an example of usage.

        :param object:
        :type object:
        :param inline_separator: The inline seperator value, defaults to None
        :param inline_separator: str, optional
        :param inline_or: The inline or value, defaults to None
        :param inline_or: str, optional
        :param inline_or_more: The inline or more value, defaults to None
        :param inline_or_more: str, optional
        :param includeNumbers: Flag indicating whether to include numbers as a choice, defaults to None
        :param includeNumbers: bool, optional
        :return:
        :rtype: None
        """

        self.inline_separator = inline_separator
        self.inline_or = inline_or
        self.inline_or_more = inline_or_more
        self.include_numbers = include_numbers
