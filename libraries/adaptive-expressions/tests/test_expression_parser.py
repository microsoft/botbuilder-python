# pylint: disable=too-many-lines
import math
import platform
import aiounittest
from adaptive.expressions import Expression


class ExpressionParserTests(aiounittest.AsyncTestCase):
    scope = {
        "hello": "hello",
        "nullObj": None,
        "bag": {"three": 3.0},
        "items": ["zero", "one", "two"],
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

    # TODO: test of substring

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

        # TODO: the following four cases
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
