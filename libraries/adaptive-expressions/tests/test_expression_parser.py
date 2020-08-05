# pylint: disable=too-many-lines
import math
import platform
from datetime import datetime
from dateutil import tz
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
import aiounittest
from adaptive.expressions import Expression


class ExpressionParserTests(aiounittest.AsyncTestCase):
    scope = {
        "one": 1.0,
        "two": 2.0,
        "hello": "hello",
        "nullObj": None,
        "bag": {"three": 3.0},
        "items": ["zero", "one", "two"],
        "nestedItems": [{"x": 1}, {"x": 2}, {"x": 3},],
        "dialog": {
            "x": 3,
            "instance": {"xxx": "instance", "yyy": {"instanceY": "instanceY"}},
            "options": {"xxx": "options", "yyy": ["optionY1", "optionY2"]},
            "title": "Dialog Title",
            "subTitle": "Dialog Sub Title",
        },
        "timestamp": "2018-03-15T13:00:00.000Z",
        "notISOTimestamp": "2018/03/15 13:00:00",
        "timestampObj": parse("2018-03-15T13:00:00.000Z").replace(tzinfo=tz.gettz("UTC")),
        "timestampObj2": parse("2018-01-02T02:00:00.000Z").replace(tzinfo=tz.gettz("UTC")),
        "unixTimestamp": 1521118800,
        "unixTimestampFraction": 1521118800.5,
        "ticks": 637243624200000000,
        "doubleNestedItems": [[{"x": 1}, {"x: 2"}], [{"x": 3}]],
    }

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

        parsed = Expression.parse("'hello' != 'hello'")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value is False
        assert error is None

        parsed = Expression.parse("'hello' != 'world'")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value is True
        assert error is None

    def test_exists(self):
        parsed = Expression.parse("exists(one)")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert value
        assert error is None

        parsed = Expression.parse("exists(xxx)")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert not value
        assert error is None

        parsed = Expression.parse("exists(one.xxx)")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert not value
        assert error is None

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

        # TODO: escape sign, the following two cases is different from C#!

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

    def test_substring(self):
        parsed = Expression.parse("substring(concat('na','me','more'), 0, length('name'))")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == "name"
        assert error is None

        parsed = Expression.parse("substring('hello', 0, 5)")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == "hello"
        assert error is None

        parsed = Expression.parse("substring('hello', 0, 3)")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == "hel"
        assert error is None

        parsed = Expression.parse("substring('hello', 3)")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == "lo"
        assert error is None

        parsed = Expression.parse("substring(nullObj, 0, 3)")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert value == ""
        assert error is None

    def test_to_lower(self):
        parsed = Expression.parse('toLower("UpCase")')
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == "upcase"
        assert error is None

    def test_to_upper(self):
        parsed = Expression.parse('toUpper("UpCase")')
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == "UPCASE"
        assert error is None

        parsed = Expression.parse('toUpper(toLower("UpCase"))')
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == "UPCASE"
        assert error is None

    def test_trim(self):
        parsed = Expression.parse('trim("  hello  ")')
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == "hello"
        assert error is None

        parsed = Expression.parse('trim(" hello")')
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == "hello"
        assert error is None

        parsed = Expression.parse('trim("")')
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == ""
        assert error is None

        parsed = Expression.parse("trim(nullObj)")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert value == ""
        assert error is None

    def test_ends_with(self):
        parsed = Expression.parse('endsWith("hello", "o")')
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value is True
        assert error is None

        parsed = Expression.parse('endsWith("hello", "e")')
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value is False
        assert error is None

        parsed = Expression.parse('endsWith(hello, "o")')
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert value is True
        assert error is None

        parsed = Expression.parse('endsWith(hello, "a")')
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert value is False
        assert error is None

        parsed = Expression.parse('endsWith(nullObj, "o")')
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert value is False
        assert error is None

        parsed = Expression.parse("endsWith(hello, nullObj)")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert value is True
        assert error is None

    def test_starts_with(self):
        parsed = Expression.parse('startsWith("hello", "h")')
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value is True
        assert error is None

        parsed = Expression.parse('startsWith("hello", "a")')
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value is False
        assert error is None

        parsed = Expression.parse('startsWith(nullObj, "o")')
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert value is False
        assert error is None

        parsed = Expression.parse('endsWith("hello", nullObj)')
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert value is True
        assert error is None

    def test_count_word(self):
        parsed = Expression.parse('countWord("hello")')
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == 1
        assert error is None

        parsed = Expression.parse('countWord(concat("hello", " ", "world"))')
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == 2
        assert error is None

        parsed = Expression.parse("countWord(nullObj)")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert value == 0
        assert error is None

    def test_add_ordinal(self):
        parsed = Expression.parse("addOrdinal(11)")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == "11th"
        assert error is None

        parsed = Expression.parse("addOrdinal(11+1)")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == "12th"
        assert error is None

        parsed = Expression.parse("addOrdinal(11+2)")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == "13th"
        assert error is None

        parsed = Expression.parse("addOrdinal(11+10)")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == "21st"
        assert error is None

        parsed = Expression.parse("addOrdinal(11+11)")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == "22nd"
        assert error is None

        parsed = Expression.parse("addOrdinal(11+12)")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == "23rd"
        assert error is None

        parsed = Expression.parse("addOrdinal(11+13)")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == "24th"
        assert error is None

        parsed = Expression.parse("addOrdinal(-1)")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == "-1"
        assert error is None

    def test_new_guid(self):
        parsed = Expression.parse("length(newGuid())")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == 36
        assert error is None

    def test_index_of(self):
        parsed = Expression.parse("indexOf('hello', '-')")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == -1
        assert error is None

        parsed = Expression.parse("indexOf('hello', 'h')")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == 0
        assert error is None

        parsed = Expression.parse("indexOf(createArray('abc', 'def', 'ghi'), 'def')")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == 1
        assert error is None

        parsed = Expression.parse("indexOf(createArray('abc', 'def', 'ghi'), 'klm')")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == -1
        assert error is None

    def test_last_index_of(self):
        parsed = Expression.parse("lastIndexOf('hello', '-')")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == -1
        assert error is None

        parsed = Expression.parse("lastIndexOf('hello', 'l')")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == 3
        assert error is None

        parsed = Expression.parse(
            "lastIndexOf(createArray('abc', 'def', 'ghi', 'def'), 'def')"
        )
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == 3
        assert error is None

        parsed = Expression.parse(
            "lastIndexOf(createArray('abc', 'def', 'ghi'), 'klm')"
        )
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == -1
        assert error is None

        parsed = Expression.parse("lastIndexOf(newGuid(), '-')")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == 23
        assert error is None

    def test_eol(self):
        parsed = Expression.parse("EOL()")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == "\r\n" if platform.system() == "Windows" else "\n"
        assert error is None

    def test_sentence_case(self):
        parsed = Expression.parse("sentenceCase('abc')")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == "Abc"
        assert error is None

        parsed = Expression.parse("sentenceCase('aBc')")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == "Abc"
        assert error is None

        parsed = Expression.parse("sentenceCase('a')")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == "A"
        assert error is None

    def test_title_case(self):
        parsed = Expression.parse("titleCase('a')")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == "A"
        assert error is None

        parsed = Expression.parse("titleCase('abc dEF')")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == "Abc Def"
        assert error is None

    # Collection
    def test_count(self):
        parsed = Expression.parse("count('hello')")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == 5
        assert error is None

        parsed = Expression.parse('count("hello")')
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == 5
        assert error is None

        parsed = Expression.parse("count(createArray('h', 'e', 'l', 'l', 'o'))")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == 5
        assert error is None

    def test_contains(self):
        parsed = Expression.parse("contains('hello world', 'hello')")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value
        assert error is None

        parsed = Expression.parse("contains('hello world', 'hellow')")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert not value
        assert error is None

        parsed = Expression.parse("contains('hello world',\r\n 'hellow')")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert not value
        assert error is None

        parsed = Expression.parse("contains(items, 'zero')")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert value
        assert error is None

        parsed = Expression.parse("contains(items, 'hi')")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert not value
        assert error is None

        parsed = Expression.parse("contains(bag, 'three')")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert value
        assert error is None

        parsed = Expression.parse("contains(bag, 'xxx')")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert not value
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

    def test_empty(self):
        parsed = Expression.parse("empty('')")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value
        assert error is None

        parsed = Expression.parse("empty('a')")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert not value
        assert error is None

        parsed = Expression.parse("empty(bag)")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert not value
        assert error is None

        parsed = Expression.parse("empty(items)")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert not value
        assert error is None

    def test_join(self):
        parsed = Expression.parse("join(items, ',')")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert value == "zero,one,two"
        assert error is None

        parsed = Expression.parse("join(createArray('a', 'b', 'c'), '.')")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == "a.b.c"
        assert error is None

        parsed = Expression.parse("join(createArray('a', 'b', 'c'), ',', ' and ')")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == "a,b and c"
        assert error is None

        parsed = Expression.parse("join(createArray('a', 'b'), ',', ' and ')")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == "a and b"
        assert error is None

        parsed = Expression.parse(
            "join(createArray(\r\n'a',\r\n 'b'), ','\r\n,\r\n ' and ')"
        )
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == "a and b"
        assert error is None

    def test_first(self):
        parsed = Expression.parse("first(items)")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert value == "zero"
        assert error is None

        parsed = Expression.parse("first('hello')")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == "h"
        assert error is None

        parsed = Expression.parse("first(createArray(0, 1, 2))")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == 0
        assert error is None

        parsed = Expression.parse("first(1)")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value is None
        assert error is None

        parsed = Expression.parse("first(nestedItems).x")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert value == 1
        assert error is None

    def test_last(self):
        parsed = Expression.parse("last(items)")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert value == "two"
        assert error is None

        parsed = Expression.parse("last('hello')")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == "o"
        assert error is None

        parsed = Expression.parse("last(createArray(0, 1, 2))")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == 2
        assert error is None

        parsed = Expression.parse("last(1)")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value is None
        assert error is None

        parsed = Expression.parse("last(nestedItems).x")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert value == 3
        assert error is None

    def test_foreach(self):
        parsed = Expression.parse("join(foreach(dialog, item, item.key), ',')")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert value == "x,instance,options,title,subTitle"
        assert error is None

        parsed = Expression.parse("join(foreach(dialog, item => item.key), ',')")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert value == "x,instance,options,title,subTitle"
        assert error is None

        parsed = Expression.parse("foreach(dialog, item, item.value)[1].xxx")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert value == "instance"
        assert error is None

        parsed = Expression.parse("foreach(dialog, item=>item.value)[1].xxx")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert value == "instance"
        assert error is None

        parsed = Expression.parse("join(foreach(items, item, item), ',')")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert value == "zero,one,two"
        assert error is None

        parsed = Expression.parse("join(foreach(items, item=>item), ',')")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert value == "zero,one,two"
        assert error is None

        parsed = Expression.parse(
            "join(foreach(nestedItems, i, i.x + first(nestedItems).x), ',')"
        )
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert value == "2,3,4"
        assert error is None

        parsed = Expression.parse(
            "join(foreach(items, item, concat(item, string(count(items)))), ',')"
        )
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert value == "zero3,one3,two3"
        assert error is None

    def test_select(self):
        parsed = Expression.parse("join(select(items, item, item), ',')")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert value == "zero,one,two"
        assert error is None

        parsed = Expression.parse("join(select(items, item=> item), ',')")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert value == "zero,one,two"
        assert error is None

        parsed = Expression.parse(
            "join(select(nestedItems, i, i.x + first(nestedItems).x), ',')"
        )
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert value == "2,3,4"
        assert error is None

        parsed = Expression.parse(
            "join(select(items, item, concat(item, string(count(items)))), ',')"
        )
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert value == "zero3,one3,two3"
        assert error is None

    def test_where(self):
        parsed = Expression.parse("join(where(items, item, item == 'two'), ',')")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert value == "two"
        assert error is None

        parsed = Expression.parse("join(where(items, item => item == 'two'), ',')")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert value == "two"
        assert error is None

        parsed = Expression.parse(
            "string(where(dialog, item, item.value=='Dialog Title'))"
        )
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert value == "{'title': 'Dialog Title'}"
        assert error is None

        parsed = Expression.parse(
            "join(foreach(where(nestedItems, item, item.x > 1), result, result.x), ',')"
        )
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert value == "2,3"
        assert error is None

        parsed = Expression.parse(
            "count(where(doubleNestedItems, items, count(where(items, item, item.x == 1)) == 1))"
        )
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert value == 1
        assert error is None

        parsed = Expression.parse(
            "count(where(doubleNestedItems, items, count(where(items, item, count(items) == 1)) == 1))"
        )
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert value == 1
        assert error is None

    def test_union(self):
        parsed = Expression.parse('union(["a", "b", "c"], ["d", ["e", "f"], "g"][1])')
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == ["a", "b", "c", "e", "f"]
        assert error is None

        parsed = Expression.parse(
            'union(["a", "b", "c"], ["d", ["e", "f"], "g"][1])[1]'
        )
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == "b"
        assert error is None

        parsed = Expression.parse("count(union(createArray('a', 'b')))")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == 2
        assert error is None

        parsed = Expression.parse(
            "count(union(createArray('a', 'b'), createArray('b', 'c'), createArray('b', 'd')))"
        )
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == 4
        assert error is None

    def test_intersection(self):
        parsed = Expression.parse('count(intersection(createArray("a", "b")))')
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == 2
        assert error is None

        parsed = Expression.parse(
            'count(intersection(createArray("a", "b"), createArray("b", "c"), createArray("b", "d")))'
        )
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == 1
        assert error is None

    def test_skip(self):
        parsed = Expression.parse("skip(createArray('H','e','l','l','0'),2)")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == ["l", "l", "0"]
        assert error is None

    def test_take(self):
        parsed = Expression.parse("take(hello, two)")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert value == "he"
        assert error is None

        parsed = Expression.parse("take(createArray('a', 'b', 'c', 'd'), one)")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert value == ["a"]
        assert error is None

    def test_sub_array(self):
        parsed = Expression.parse("subArray(createArray('a', 'b', 'c', 'd'), 1, 3)")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == ["b", "c"]
        assert error is None

        parsed = Expression.parse("subArray(createArray('a', 'b', 'c', 'd'), 1)")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert value == ["b", "c", "d"]
        assert error is None

    # Datetime
    def test_add_days(self):
        parsed = Expression.parse("addDays('2018-03-15T13:00:00.000Z', 1)")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == "2018-03-16T13:00:00.000Z"
        assert error is None

        parsed = Expression.parse("addDays(timestamp, 1)")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert value == "2018-03-16T13:00:00.000Z"
        assert error is None

        parsed = Expression.parse("addDays(timestampObj, 1)")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert value == "2018-03-16T13:00:00.000Z"
        assert error is None

        parsed = Expression.parse("addDays(timestamp, 1,'%m-%d-%y')")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert value == "03-16-18"
        assert error is None

    def test_add_hours(self):
        parsed = Expression.parse("addHours('2018-03-15T13:00:00.000Z', 1)")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == "2018-03-15T14:00:00.000Z"
        assert error is None

        parsed = Expression.parse("addHours(timestamp, 1)")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert value == "2018-03-15T14:00:00.000Z"
        assert error is None

        parsed = Expression.parse("addHours(timestampObj, 1)")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert value == "2018-03-15T14:00:00.000Z"
        assert error is None

        parsed = Expression.parse("addHours(timestamp, 1,'%m-%d-%y %I-%M')")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert value == "03-15-18 02-00"
        assert error is None

    def test_add_minutes(self):
        parsed = Expression.parse("addMinutes('2018-03-15T13:00:00.000Z', 1)")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == "2018-03-15T13:01:00.000Z"
        assert error is None

        parsed = Expression.parse("addMinutes(timestamp, 1)")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert value == "2018-03-15T13:01:00.000Z"
        assert error is None

        parsed = Expression.parse("addMinutes(timestampObj, 1)")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert value == "2018-03-15T13:01:00.000Z"
        assert error is None

        parsed = Expression.parse("addMinutes(timestamp, 1,'%m-%d-%y %I-%M')")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert value == "03-15-18 01-01"
        assert error is None

    def test_add_seconds(self):
        parsed = Expression.parse("addSeconds('2018-03-15T13:00:00.000Z', 1)")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == "2018-03-15T13:00:01.000Z"
        assert error is None

        parsed = Expression.parse("addSeconds(timestamp, 1)")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert value == "2018-03-15T13:00:01.000Z"
        assert error is None

        parsed = Expression.parse("addSeconds(timestampObj, 1)")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert value == "2018-03-15T13:00:01.000Z"
        assert error is None

        parsed = Expression.parse("addSeconds(timestamp, 1,'%m-%d-%y %I-%M-%S')")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert value == "03-15-18 01-00-01"
        assert error is None

    def test_day_of_month(self):
        parsed = Expression.parse("dayOfMonth('2018-03-15T13:00:00.000Z')")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == 15
        assert error is None

        parsed = Expression.parse("dayOfMonth(timestamp)")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert value == 15
        assert error is None

        parsed = Expression.parse("dayOfMonth(timestampObj)")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert value == 15
        assert error is None

    def test_day_of_week(self):
        parsed = Expression.parse("dayOfWeek('2018-03-15T13:00:00.000Z')")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == 4
        assert error is None

        parsed = Expression.parse("dayOfWeek(timestamp)")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert value == 4
        assert error is None

        parsed = Expression.parse("dayOfWeek(timestampObj)")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert value == 4
        assert error is None

    def test_day_of_year(self):
        parsed = Expression.parse("dayOfYear('2018-03-15T13:00:00.000Z')")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == 74
        assert error is None

        parsed = Expression.parse("dayOfYear(timestamp)")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert value == 74
        assert error is None

        parsed = Expression.parse("dayOfYear(timestampObj)")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert value == 74
        assert error is None

    def test_month(self):
        parsed = Expression.parse("month('2018-03-15T13:00:00.000Z')")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert error is None
        assert value == 3

        parsed = Expression.parse("month(timestamp)")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert value == 3
        assert error is None

        parsed = Expression.parse("month(timestampObj)")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert value == 3
        assert error is None

    def test_date(self):
        parsed = Expression.parse("date('2018-03-15T13:00:00.000Z')")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert error is None
        assert value == "3/15/2018"

        parsed = Expression.parse("date(timestamp)")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert value == "3/15/2018"
        assert error is None

        parsed = Expression.parse("date(timestampObj)")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert value == "3/15/2018"
        assert error is None

    def test_year(self):
        parsed = Expression.parse("year('2018-03-15T13:00:00.000Z')")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert error is None
        assert value == 2018

        parsed = Expression.parse("year(timestamp)")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert value == 2018
        assert error is None

        parsed = Expression.parse("year(timestampObj)")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert value == 2018
        assert error is None

    def test_utc_now(self):
        parsed = Expression.parse("length(utcNow())")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert error is None
        assert value == 24

        parsed = Expression.parse("utcNow('%m-%d-%Y')")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert value == datetime.utcnow().strftime('%m-%d-%Y')

    def test_format_date_time(self):
        parsed = Expression.parse("formatDateTime('2018-03-15')")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert error is None
        assert value == "2018-03-15T00:00:00.000Z"

        parsed = Expression.parse("formatDateTime(notISOTimestamp)")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert error is None
        assert value == "2018-03-15T13:00:00.000Z"

        parsed = Expression.parse("formatDateTime(notISOTimestamp, '%m-%d-%y')")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert error is None
        assert value == "03-15-18"

        parsed = Expression.parse("formatDateTime(timestampObj)")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert error is None
        assert value == "2018-03-15T13:00:00.000Z"

    def test_format_epoch(self):
        parsed = Expression.parse("formatEpoch(unixTimestamp)")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert error is None
        assert value == "2018-03-15T13:00:00.000Z"

        parsed = Expression.parse("formatEpoch(unixTimestampFraction)")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert error is None
        assert value == "2018-03-15T13:00:00.500Z"

    def test_format_ticks(self):
        parsed = Expression.parse("formatTicks(ticks)")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert error is None
        assert value == "2020-05-06T11:47:00.000Z"

    def test_subtract_from_time(self):
        parsed = Expression.parse("subtractFromTime(timestamp, 1, 'Year')")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert error is None
        assert value == "2017-03-15T13:00:00.000Z"

        parsed = Expression.parse("subtractFromTime(timestampObj, 1, 'Year')")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert error is None
        assert value == "2017-03-15T13:00:00.000Z"

        parsed = Expression.parse("subtractFromTime(timestamp, 1, 'Month')")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert error is None
        assert value == "2018-02-15T13:00:00.000Z"

        parsed = Expression.parse("subtractFromTime(timestamp, 1, 'Week')")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert error is None
        assert value == "2018-03-08T13:00:00.000Z"

        parsed = Expression.parse("subtractFromTime(timestamp, 1, 'Day')")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert error is None
        assert value == "2018-03-14T13:00:00.000Z"

        parsed = Expression.parse("subtractFromTime(timestamp, 1, 'Hour')")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert error is None
        assert value == "2018-03-15T12:00:00.000Z"

        parsed = Expression.parse("subtractFromTime(timestamp, 1, 'Minute')")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert error is None
        assert value == "2018-03-15T12:59:00.000Z"

        parsed = Expression.parse("subtractFromTime(timestamp, 1, 'Second')")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert error is None
        assert value == "2018-03-15T12:59:59.000Z"

    def test_date_read_back(self):
        parsed = Expression.parse("dateReadBack(timestamp, addDays(timestamp, 1))")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert error is None
        assert value == "tomorrow"

        parsed = Expression.parse("dateReadBack(timestampObj, addDays(timestamp, 1))")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert error is None
        assert value == "tomorrow"

        parsed = Expression.parse("dateReadBack(addDays(timestamp, 1),timestamp)")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert error is None
        assert value == "yesterday"

    def test_get_time_of_day(self):
        parsed = Expression.parse("getTimeOfDay('2018-03-15T00:00:00.000Z')")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert error is None
        assert value == "midnight"

        parsed = Expression.parse("getTimeOfDay(timestampObj)")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert error is None
        assert value == "afternoon"

        parsed = Expression.parse("getTimeOfDay('2018-03-15T08:00:00.000Z')")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert error is None
        assert value == "morning"

        parsed = Expression.parse("getTimeOfDay('2018-03-15T12:00:00.000Z')")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert error is None
        assert value == "noon"

        parsed = Expression.parse("getTimeOfDay('2018-03-15T13:00:00.000Z')")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert error is None
        assert value == "afternoon"

        parsed = Expression.parse("getTimeOfDay('2018-03-15T18:00:00.000Z')")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert error is None
        assert value == "evening"

        parsed = Expression.parse("getTimeOfDay('2018-03-15T22:00:00.000Z')")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert error is None
        assert value == "evening"

        parsed = Expression.parse("getTimeOfDay('2018-03-15T23:00:00.000Z')")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert error is None
        assert value == "night"

    def test_get_past_time(self):
        parsed = Expression.parse("getPastTime(1,'Year','%m-%d-%y')")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert error is None
        assert value == (datetime.utcnow() + relativedelta(years=-1)).strftime("%m-%d-%y")

        parsed = Expression.parse("getPastTime(1,'Month','%m-%d-%y')")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert error is None
        assert value == (datetime.utcnow() + relativedelta(months=-1)).strftime("%m-%d-%y")

        parsed = Expression.parse("getPastTime(1,'Week','%m-%d-%y')")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert error is None
        assert value == (datetime.utcnow() + relativedelta(weeks=-1)).strftime("%m-%d-%y")

        parsed = Expression.parse("getPastTime(1,'Day','%m-%d-%y')")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert error is None
        assert value == (datetime.utcnow() + relativedelta(days=-1)).strftime("%m-%d-%y")

    def test_convert_from_utc(self):
        parsed = Expression.parse("convertFromUTC('2018-01-02T02:00:00.000Z', 'Pacific Standard Time', '%A, %d %B %Y')")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert error is None
        assert value == "Monday, 01 January 2018"

        parsed = Expression.parse("convertFromUTC('2018-01-02T01:00:00.000Z', 'America/Los_Angeles', '%A, %d %B %Y')")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert error is None
        assert value == "Monday, 01 January 2018"

        parsed = Expression.parse("convertFromUTC(timestampObj2, 'Pacific Standard Time', '%A, %d %B %Y')")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert error is None
        assert value == "Monday, 01 January 2018"

    def test_convert_to_utc(self):
        parsed = Expression.parse("convertToUTC('01/01/2018 00:00:00', 'Pacific Standard Time')")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert error is None
        assert value == "2018-01-01T08:00:00.000Z"

    def test_add_to_time(self):
        parsed = Expression.parse("addToTime('2018-01-01T08:00:00.000Z', 1, 'Day', '%A, %d %B %Y')")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert error is None
        assert value == "Tuesday, 02 January 2018"

        parsed = Expression.parse("addToTime('2018-01-01T00:00:00.000Z', 1, 'Week')")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert error is None
        assert value == "2018-01-08T00:00:00.000Z"

        parsed = Expression.parse("addToTime(timestampObj2, 1, 'Week')")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert error is None
        assert value == "2018-01-09T02:00:00.000Z"

    def test_start_of_day(self):
        parsed = Expression.parse("startOfDay('2018-03-15T13:30:30.000Z')")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert error is None
        assert value == "2018-03-15T00:00:00.000Z"

        parsed = Expression.parse("startOfDay(timestampObj2)")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert error is None
        assert value == "2018-01-02T00:00:00.000Z"

    def test_start_of_hour(self):
        parsed = Expression.parse("startOfHour('2018-03-15T13:30:30.000Z')")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert error is None
        assert value == "2018-03-15T13:00:00.000Z"

        parsed = Expression.parse("startOfHour(timestampObj)")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert error is None
        assert value == "2018-03-15T13:00:00.000Z"

    def test_start_of_month(self):
        parsed = Expression.parse("startOfMonth('2018-03-15T13:30:30.000Z')")
        assert parsed is not None

        value, error = parsed.try_evaluate({})
        assert error is None
        assert value == "2018-03-01T00:00:00.000Z"

        parsed = Expression.parse("startOfMonth(timestampObj)")
        assert parsed is not None

        value, error = parsed.try_evaluate(self.scope)
        assert error is None
        assert value == "2018-03-01T00:00:00.000Z"
