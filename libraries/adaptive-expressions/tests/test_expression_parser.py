import math
import aiounittest
from adaptive.expressions import Expression


class ExpressionParserTests(aiounittest.AsyncTestCase):
    # Math
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

    def test_mod(self):
        parsed = Expression.parse("3 % 2")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == 1
        assert error is None

        parsed = Expression.parse("(4+1) % 2")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == 1
        assert error is None

        parsed = Expression.parse("(4+1.5) % 2")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == 1.5
        assert error is None

        parsed = Expression.parse("mod(8, 3)")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == 2
        assert error is None

    def test_average(self):
        parsed = Expression.parse("average(createArray(3, 2))")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == 2.5
        assert error is None

        parsed = Expression.parse("average(createArray(5, 2))")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == 3.5
        assert error is None

        parsed = Expression.parse("average(createArray(4, 2))")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == 3
        assert error is None

        parsed = Expression.parse("average(createArray(8, -3))")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == 2.5
        assert error is None

    def test_sum(self):
        parsed = Expression.parse("sum(createArray(3, 2))")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == 5
        assert error is None

        parsed = Expression.parse("sum(createArray(5.2, 2.8))")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == 8
        assert error is None

        parsed = Expression.parse("sum(createArray(4.2, 2))")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == 6.2
        assert error is None

        parsed = Expression.parse("sum(createArray(8.5, -3))")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == 5.5
        assert error is None

    def test_range(self):
        parsed = Expression.parse("range(1, 4)")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        print(value)
        assert value == [1, 2, 3, 4]
        assert error is None

        parsed = Expression.parse("range(-1, 6)")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == [-1, 0, 1, 2, 3, 4]
        assert error is None

    def test_floor(self):
        parsed = Expression.parse("floor(3.51)")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        print(value)
        assert value == 3
        assert error is None

        parsed = Expression.parse("floor(4.00)")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == 4
        assert error is None

    def test_ceiling(self):
        parsed = Expression.parse("ceiling(3.51)")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        print(value)
        assert value == 4
        assert error is None

        parsed = Expression.parse("ceiling(4.00)")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == 4
        assert error is None

    def test_round(self):
        parsed = Expression.parse("round(3.51)")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        print(value)
        assert value == 4
        assert error is None

        # please notice that 5 will not round up
        parsed = Expression.parse("round(3.55, 1)")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == 3.5
        assert error is None

        # it will round up only if value is more than 5
        parsed = Expression.parse("round(3.56, 1)")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == 3.6
        assert error is None

        parsed = Expression.parse("round(3.12134, 3)")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == 3.121

    # Comparisons
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

        parsed = Expression.parse('"123" == "132"')
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

        parsed = Expression.parse("(1+2) >= (4-1)")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value is True
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

        parsed = Expression.parse("\'hello\' != \'hello\'")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value is False
        assert error is None

        parsed = Expression.parse("\'hello\' != \'world\'")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value is True
        assert error is None

    # TODO: add exists test

    # Logic
    def test_not(self):
        parsed = Expression.parse("!(1 >= 2)")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value is True
        assert error is None

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

    # String
    def test_concat(self):
        parsed = Expression.parse("concat(createArray(1,2), createArray(2,3))")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == [1, 2, 2, 3]
        assert error is None

        parsed = Expression.parse('concat("hello", "world")')
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == "helloworld"
        assert error is None

    def test_length(self):
        parsed = Expression.parse("length(concat('[]', 'abc'))")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == 5
        assert error is None

        parsed = Expression.parse('length("hello")')
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == 5
        assert error is None

    def test_replace(self):
        parsed = Expression.parse('replace("hello", "l", "k")')
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == "hekko"
        assert error is None

        parsed = Expression.parse('replace("hello", "L", "k")')
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == "hello"
        assert error is None

        parsed = Expression.parse('replace("hello", "l", "")')
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == "heo"
        assert error is None

        parsed = Expression.parse("replace('hello\n', '\n', '\\\\')")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == r"hello\\"
        assert error is None

        parsed = Expression.parse(r"replace('hello\\', '\\', '\\\\')")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == r"hello\\\\"
        assert error is None

    def test_replace_ignore_case(self):
        parsed = Expression.parse('replaceIgnoreCase("hello", "L", "K")')
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == "hekko"
        assert error is None

    def test_split(self):
        parsed = Expression.parse('split("hello", "e")')
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == ["h", "llo"]
        assert error is None

        parsed = Expression.parse('split("hello")')
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == ["h", "e", "l", "l", "o"]
        assert error is None

        parsed = Expression.parse('split("", "e")')
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == [""]
        assert error is None

        parsed = Expression.parse('split("", "")')
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == []
        assert error is None

        parsed = Expression.parse('split("hello", "")')
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == ["h", "e", "l", "l", "o"]
        assert error is None
