import aiounittest
from adaptive.expressions import Expression


class ExpressionParserTests(aiounittest.AsyncTestCase):
    def test_add(self):
        parsed = Expression.parse("1+1")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == 2
        assert error is None

        parsed = Expression.parse("1+1+2")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == 4
        assert error is None

        parsed = Expression.parse("add(2, 3)")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == 5
        assert error is None

        parsed = Expression.parse("add(2, 3, 4)")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == 9
        assert error is None
