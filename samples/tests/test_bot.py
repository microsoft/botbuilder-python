

"""
Test Suite

"""

import pytest

from application import app
from tests.adapters import pax_string_test_struc


@pytest.fixture()
def client(request):
    """
    Web Client Fixture used by Flask based tests

    :param request: Provided Flask Fixture
    """

    test_client = app.test_client()

    def teardown():
        pass  # databases and resources have to be freed at the end. But so far we don't have anything

    request.addfinalizer(teardown)
    return test_client


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
