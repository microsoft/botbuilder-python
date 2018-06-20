import pytest

from botframework.connector.auth import EndorsementsValidator

class TestEndorsmentsValidator:
    def test_none_channel_id_parameter_should_pass(self):
        is_endorsed = EndorsementsValidator.validate(None, [])
        assert is_endorsed

    def test_none_endorsements_parameter_should_throw(self):
        with pytest.raises(ValueError) as excinfo:
            EndorsementsValidator.validate('foo', None)
            assert 'endorsements' in excinfo

    def test_unendorsed_channel_id_should_fail(self):
        is_endorsed = EndorsementsValidator.validate('channelOne', [])
        assert not is_endorsed

    def test_mismatched_endorsements_channel_id_should_fail(self):
        is_endorsed = EndorsementsValidator.validate('right', ['wrong'])
        assert not is_endorsed

    def test_endorsed_channel_id_should_pass(self):
        is_endorsed = EndorsementsValidator.validate('right', ['right'])
        assert is_endorsed

    def test_endorsed_channel_id_should_pass_with_two_endorsements(self):
        is_endorsed = EndorsementsValidator.validate('right', ['right', 'wrong'])
        assert is_endorsed

    def test_unaffinitized_activity_should_pass(self):
        is_endorsed = EndorsementsValidator.validate('', ['right', 'wrong'])
        assert is_endorsed
