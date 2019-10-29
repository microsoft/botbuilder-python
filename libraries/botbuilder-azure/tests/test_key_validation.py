from unittest import TestCase
from botbuilder.azure import CosmosDbKeyEscape


class TestKeyValidation(TestCase):
    def test_should_not_change_a_valid_key(self):
        valid_key = "Abc12345"
        sanitized_key = CosmosDbKeyEscape.sanitize_key(valid_key)
        assert (
            valid_key == sanitized_key
        ), f"{valid_key} should be equal to {sanitized_key}"

    def test_should_escape_illegal_characters_case_1(self):
        # Ascii code of "?" is "3f"
        sanitized_key = CosmosDbKeyEscape.sanitize_key("?test?")
        assert sanitized_key == "*63test*63"

    def test_should_escape_illegal_characters_case_2(self):
        # Ascii code of "/" is "2f"
        sanitized_key = CosmosDbKeyEscape.sanitize_key("/test/")
        assert sanitized_key == "*47test*47"

    def test_should_escape_illegal_characters_case_3(self):
        # Ascii code of "\" is "5c"
        sanitized_key = CosmosDbKeyEscape.sanitize_key("\\test\\")
        assert sanitized_key == "*92test*92"

    def test_should_escape_illegal_characters_case_4(self):
        # Ascii code of "#" is "23"
        sanitized_key = CosmosDbKeyEscape.sanitize_key("#test#")
        assert sanitized_key == "*35test*35"

    def test_should_escape_illegal_characters_case_5(self):
        # Ascii code of "*" is "2a".
        sanitized_key = CosmosDbKeyEscape.sanitize_key("*test*")
        assert sanitized_key == "*42test*42"

    def test_should_escape_illegal_characters_compound_key(self):
        # Check a compound key
        compoundsanitized_key = CosmosDbKeyEscape.sanitize_key("?#/")
        assert compoundsanitized_key, "*3f*23*2f"

    def test_should_handle_possible_collisions(self):
        valid_key1 = "*2atest*2a"
        valid_key2 = "*test*"

        escaped1 = CosmosDbKeyEscape.sanitize_key(valid_key1)
        escaped2 = CosmosDbKeyEscape.sanitize_key(valid_key2)

        assert escaped1 != escaped2, f"{escaped1} should be different that {escaped2}"

    def test_should_truncate_longer_keys(self):
        # create an extra long key
        # limit is 255
        long_key = "x" * 300
        fixed = CosmosDbKeyEscape.sanitize_key(long_key)

        assert len(fixed) <= 255, "long key was not properly truncated"

    def test_should_not_truncate_short_key(self):
        # create a short key
        short_key = "x" * 16
        fixed2 = CosmosDbKeyEscape.sanitize_key(short_key)

        assert len(fixed2) == 16, "short key was truncated improperly"

    def test_should_create_sufficiently_different_truncated_keys_of_similar_origin(
        self,
    ):
        # create 2 very similar extra long key where the difference will definitely be trimmed off by truncate function
        long_key = "x" * 300 + "1"
        long_key2 = "x" * 300 + "2"

        fixed = CosmosDbKeyEscape.sanitize_key(long_key)
        fixed2 = CosmosDbKeyEscape.sanitize_key(long_key2)

        assert len(fixed) != fixed2, "key truncation failed to create unique key"

    def test_should_properly_truncate_keys_with_special_chars(self):
        # create a short key
        long_key = "*" * 300
        fixed = CosmosDbKeyEscape.sanitize_key(long_key)

        assert len(fixed) <= 255, "long key with special char was truncated improperly"

        # create a short key
        short_key = "#" * 16
        fixed2 = CosmosDbKeyEscape.sanitize_key(short_key)

        assert (
            len(fixed2) <= 255
        ), "short key with special char was truncated improperly"
