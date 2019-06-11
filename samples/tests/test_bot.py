

"""
Test Suite

"""

import pytest

from tests.adapters import string_test_struc


@pytest.mark.asyncio
async def test_main():
    """
    Test lost item on most recent trip
    """

    msgs = [
        "I lost something",
        "it’s a yellow Kate spade purse."]
    answers = [
        "Sorry to hear that. I can help. "
        "Can you describe to me the item? What is it? What color is it?\n",
        "Let me check.\n"
    ]
    await string_test_struc(msgs, answers, "simple")
