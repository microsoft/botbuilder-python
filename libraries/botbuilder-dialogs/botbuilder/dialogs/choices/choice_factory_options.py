# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.


class ChoiceFactoryOptions(object):
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

        self._inline_separator = inline_separator
        self._inline_or = inline_or
        self._inline_or_more = inline_or_more
        self._include_numbers = include_numbers

    @property
    def inline_separator(self) -> str:
        """
        Gets the character used to separate individual choices when there are more than 2 choices.
        The default value is `", "`. This is optional.

        Returns:
            str: The character used to separate individual choices when there are more than 2 choices.
        """

        return self._inline_separator

    @inline_separator.setter
    def inline_separator(self, value: str) -> None:
        """Sets the character used to separate individual choices when there are more than 2 choices.
        The default value is `", "`. This is optional.

        :param value: The character used to separate individual choices when there are more than 2 choices.
        :type value: str
        :return:
        :rtype: None
        """

        self._inline_separator = value

    @property
    def inline_or(self) -> str:
        """Gets the separator inserted between the choices when their are only 2 choices. The default
        value is `" or "`. This is optional.

        :return: The separator inserted between the choices when their are only 2 choices.
        :rtype: str
        """

        return self._inline_or

    @inline_or.setter
    def inline_or(self, value: str) -> None:
        """Sets the separator inserted between the choices when their are only 2 choices. The default
        value is `" or "`. This is optional.

        :param value: The separator inserted between the choices when their are only 2 choices.
        :type value: str
        :return:
        :rtype: None
        """

        self._inline_or = value

    @property
    def inline_or_more(self) -> str:
        """Gets the separator inserted between the last 2 choices when their are more than 2 choices.
        The default value is `", or "`. This is optional.

        :return: The separator inserted between the last 2 choices when their are more than 2 choices.
        :rtype: str
        """
        return self._inline_or_more

    @inline_or_more.setter
    def inline_or_more(self, value: str) -> None:
        """Sets the separator inserted between the last 2 choices when their are more than 2 choices.
        The default value is `", or "`. This is optional.

        :param value: The separator inserted between the last 2 choices when their are more than 2 choices.
        :type value: str
        :return:
        :rtype: None
        """

        self._inline_or_more = value

    @property
    def include_numbers(self) -> bool:
        """Gets a value indicating whether an inline and list style choices will be prefixed with the index of the
        choice as in "1. choice". If <see langword="false"/>, the list style will use a bulleted list instead.The default value is <see langword="true"/>.

        :return: A <c>true</c>if an inline and list style choices will be prefixed with the index of the
                 choice as in "1. choice"; otherwise a <c>false</c> and the list style will use a bulleted list instead.
        :rtype: bool
        """
        return self._include_numbers

    @include_numbers.setter
    def include_numbers(self, value: bool) -> None:
        """Sets a value indicating whether an inline and list style choices will be prefixed with the index of the
        choice as in "1. choice". If <see langword="false"/>, the list style will use a bulleted list instead.The default value is <see langword="true"/>.

        :param value: A <c>true</c>if an inline and list style choices will be prefixed with the index of the
                      choice as in "1. choice"; otherwise a <c>false</c> and the list style will use a bulleted list instead.
        :type value: bool
        :return:
        :rtype: None
        """

        self._include_numbers = value
