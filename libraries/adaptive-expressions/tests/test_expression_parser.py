import math
import aiounittest
from adaptive.expressions import Expression


class ExpressionParserTests(aiounittest.AsyncTestCase):
    def test_add(self):
        parsed = Expression.parse("1+1.5")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == 2.5
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

        parsed = Expression.parse("add(2, 3, 4.5)")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == 9.5
        assert error is None

    def test_subtract(self):
        parsed = Expression.parse("1-1")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == 0
        assert error is None

        parsed = Expression.parse("5-3-1.2")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == 0.8
        assert error is None

        parsed = Expression.parse("sub(1, 1)")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == 0
        assert error is None

        parsed = Expression.parse("sub(5, 3, 1.2)")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == 0.8
        assert error is None

    def test_multiply(self):
        parsed = Expression.parse("1*2")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == 2
        assert error is None

        parsed = Expression.parse("2*3*1.1")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert math.isclose(value, 6.6, rel_tol=1e-9)
        assert error is None

        parsed = Expression.parse("mul(1, 2)")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == 2
        assert error is None

        parsed = Expression.parse("mul(2, 3, 1.1)")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert math.isclose(value, 6.6, rel_tol=1e-9)
        assert error is None

    def test_divide(self):
        parsed = Expression.parse("2/1")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == 2
        assert error is None

        parsed = Expression.parse("6/2/2")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == 1.5
        assert error is None

        parsed = Expression.parse("div(2, 2)")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == 1
        assert error is None

        parsed = Expression.parse("div(6, 2, 0.3)")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == 10
        assert error is None

    def test_min(self):
        parsed = Expression.parse("min(2, 1)")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == 1
        assert error is None

        parsed = Expression.parse("min(3, 4.5, 1.5)")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == 1.5
        assert error is None

        parsed = Expression.parse("min(2, 100, -10.5)")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == -10.5
        assert error is None

        parsed = Expression.parse("min(6, 0.3, 0.3)")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == 0.3
        assert error is None

    def test_max(self):
        parsed = Expression.parse("max(2, 1)")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == 2
        assert error is None

        parsed = Expression.parse("max(3, 4.5, 1.5)")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == 4.5
        assert error is None

        parsed = Expression.parse("max(2, 100, -10.5)")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == 100
        assert error is None

        parsed = Expression.parse("max(6.2, 6.2, 0.3)")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == 6.2
        assert error is None

    def test_power(self):
        parsed = Expression.parse("2^3")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == 8
        assert error is None

        parsed = Expression.parse("3^2^2")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == 81
        assert error is None

    def test_equal(self):
        parsed = Expression.parse("1 == 2")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value is False
        assert error is None

        parsed = Expression.parse("3 == 3")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value is True
        assert error is None

        parsed = Expression.parse("(1 + 2) == (4 - 1)")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value is True
        assert error is None

        parsed = Expression.parse("(1 + 2) ==\r\n (4 - 1)")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value is True
        assert error is None

        parsed = Expression.parse("\"123\" == \"132\"")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value is False

    def test_lessthan(self):
        parsed = Expression.parse("1 < 2")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value is True
        assert error is None

        parsed = Expression.parse("3 < 1")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value is False
        assert error is None

        parsed = Expression.parse("1.1 < 2")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value is True
        assert error is None

        parsed = Expression.parse("3.5 < 1")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value is False
        assert error is None

    def test_lessthanorequal(self):
        parsed = Expression.parse("1 <= 2")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value is True
        assert error is None

        parsed = Expression.parse("3.3 <= 1")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value is False
        assert error is None

        parsed = Expression.parse("2 <= 2")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value is True
        assert error is None

    def test_greatthan(self):
        parsed = Expression.parse("1 > 2")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value is False
        assert error is None

        parsed = Expression.parse("3.3 > 1")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value is True
        assert error is None

        parsed = Expression.parse("2 > 2")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value is False
        assert error is None

    def test_greatthanorequal(self):
        parsed = Expression.parse("1 >= 2")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value is False
        assert error is None

        parsed = Expression.parse("3.3 >= 1")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value is True
        assert error is None

        parsed = Expression.parse("2 >= 2")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value is True
        assert error is None

    def test_not(self):
        parsed = Expression.parse("!(1 >= 2)")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value is True
        assert error is None

    def test_not_equal(self):
        parsed = Expression.parse("1 != 2")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value is True
        assert error is None

        parsed = Expression.parse("2 != 2")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value is False
        assert error is None

    # def test_exist(self):
    #     parsed = Expression.parse("exists(one)")
    #     assert parsed is not None

    #     value, error = parsed.try_evaluate({})
    #     assert value == True
    #     assert error is None

    def test_or(self):
        parsed = Expression.parse("(1 != 2) || (1!=1)")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value is True
        assert error is None

        parsed = Expression.parse("(1 == 2) || (1!=1)")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value is False
        assert error is None

    def test_and(self):
        parsed = Expression.parse("(1 != 2) && (1!=1)")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value is False
        assert error is None

        parsed = Expression.parse("(1 != 2) || (1==1)")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value is True
        assert error is None
