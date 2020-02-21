# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

# SPECIAL_CHARS
# closing ')', '}' and ']'
# '-' (a range in character set)
# '&', '~', (extended character set operations)
# '#' (comment) and WHITESPACE (ignored) in verbose mode
SPECIAL_CHARS_MAP = {i: "\\" + chr(i) for i in b"()[]{}?*+-|^$\\.&~# \t\n\r\v\f"}


def escape(pattern):
    """
    Escape special characters in a string.

    This is a copy of the re.escape function in Python 3.8.  This was done
    because the 3.6.x version didn't escape in the same way and handling
    bot names with regex characters in it would fail in TurnContext.remove_mention_text
    without escaping the text.
    """
    if isinstance(pattern, str):
        return pattern.translate(SPECIAL_CHARS_MAP)

    pattern = str(pattern, "latin1")
    return pattern.translate(SPECIAL_CHARS_MAP).encode("latin1")
