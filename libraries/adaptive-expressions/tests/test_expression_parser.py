# pylint: disable=too-many-lines
import math
import platform
import numbers
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
        "doubleNestedItems": [[{"x": 1}, {"x: 2"}], [{"x": 3}]],
    }

    data_source = [
        # Math functions
        # add
        ["1+1.5", 2.5],
        ["1+1+2", 4],
        ["add(2, 3)", 5],
        ["add(2, 3, 4.5)", 9.5],
        # subtract
        ["1-1", 0],
        ["5-3-1.2", 0.8],
        ["sub(1, 1)", 0],
        ["sub(5, 3, 1.2)", 0.8],
        # multiply
        ["1*2", 2],
        ["2*3*1.1", 6.6],
        ["mul(1, 2)", 2],
        ["mul(2, 3, 1.1)", 6.6],
        # divide
        ["2/1", 2],
        ["6/2/2", 1.5],
        ["div(2, 2)", 1],
        ["div(6, 2, 0.3)", 10],
        # min
        ["min(2, 1)", 1],
        ["min(3, 4.5, 1.5)", 1.5],
        ["min(2, 100, -10.5)", -10.5],
        ["min(6, 0.3, 0.3)", 0.3],
        # max
        ["max(2, 1)", 2],
        ["max(3, 4.5, 1.5)", 4.5],
        ["max(2, 100, -10.5)", 100],
        ["max(6.2, 6.2, 0.3)", 6.2],
        # power
        ["2^3", 8],
        ["3^2^2", 81],
        # mod
        ["3 % 2", 1],
        ["(4+1) % 2", 1],
        ["(4+1.5) % 2", 1.5],
        ["mod(8, 3)", 2],
        # average
        ["average(createArray(3, 2))", 2.5],
        ["average(createArray(5, 2))", 3.5],
        ["average(createArray(4, 2))", 3],
        ["average(createArray(8, -3))", 2.5],
        # sum
        ["sum(createArray(3, 2))", 5],
        ["sum(createArray(5.2, 2.8))", 8],
        ["sum(createArray(4.2, 2))", 6.2],
        ["sum(createArray(8.5, -3))", 5.5],
        # range
        ["range(1, 4)", [1, 2, 3, 4]],
        ["range(-1, 6)", [-1, 0, 1, 2, 3, 4]],
        # floor
        ["floor(3.51)", 3],
        ["floor(4.00)", 4],
        # ceiling
        ["ceiling(3.51)", 4],
        ["ceiling(4.00)", 4],
        # round
        ["round(3.51)", 4],
        ["round(3.55, 1)", 3.5],
        ["round(3.56, 1)", 3.6],
        ["round(3.12134, 3)", 3.121],
        # Comparisons functions
        # equal
        ["1 == 2", False],
        ["3 == 3", True],
        ["(1 + 2) == (4 - 1)", True],
        ["(1 + 2) ==\r\n (4 - 1)", True],
        ['"123" == "132"', False],
        # lessThan
        ["1 < 2", True],
        ["3 < 1", False],
        ["1.1 < 2", True],
        ["3.5 < 1", False],
        # lessThanOrEqual
        ["1 <= 2", True],
        ["3.3 <= 1", False],
        ["2 <= 2", True],
        # greatThan
        ["1 > 2", False],
        ["3.3 > 1", True],
        ["2 > 2", False],
        # greatThanOrEqual
        ["1 >= 2", False],
        ["(1+2) >= (4-1)", True],
        ["3.3 >= 1", True],
        ["2 >= 2", True],
        # notEqual
        ["1 != 2", True],
        ["2 != 2", False],
        ["'hello' != 'hello'", False],
        ["'hello' != 'world'", True],
        # exists
        ["exists(one)", True],
        ["exists(xxx)", False],
        ["exists(one.xxx)", False],
        # Logic functions
        # not
        ["!(1 >= 2)", True],
        # or
        ["(1 != 2) || (1!=1)", True],
        ["(1 == 2) || (1!=1)", False],
        # and
        ["(1 != 2) && (1!=1)", False],
        ["(1 != 2) || (1==1)", True],
        # String functions
        # concat
        ["concat(createArray(1,2), createArray(2,3))", [1, 2, 2, 3]],
        ['concat("hello", "world")', "helloworld"],
        # length
        ["length(concat('[]', 'abc'))", 5],
        ['length("hello")', 5],
        # replace
        ['replace("hello", "l", "k")', "hekko"],
        ['replace("hello", "L", "k")', "hello"],
        ['replace("hello", "l", "")', "heo"],
        ["replace('hello\n', '\n', '\\\\')", r"hello\\"],
        [r"replace('hello\\', '\\', '\\\\')", r"hello\\\\"],
        # replaceIgnoreCase
        ['replaceIgnoreCase("hello", "L", "K")', "hekko"],
        # split
        ['split("hello", "e")', ["h", "llo"]],
        ['split("hello")', ["h", "e", "l", "l", "o"]],
        ['split("", "e")', [""]],
        ['split("", "")', []],
        ['split("hello", "")', ["h", "e", "l", "l", "o"]],
        # TODO: test of substring function
        # lower
        ['toLower("UpCase")', "upcase"],
        # upper
        ['toUpper("UpCase")', "UPCASE"],
        ['toUpper(toLower("UpCase"))', "UPCASE"],
        # trim
        ['trim("  hello  ")', "hello"],
        ['trim(" hello")', "hello"],
        ['trim("")', ""],
        ["trim(nullObj)", ""],
        # endsWith
        ['endsWith("hello", "o")', True],
        ['endsWith("hello", "e")', False],
        ['endsWith(hello, "o")', True],
        ['endsWith(hello, "a")', False],
        ['endsWith(nullObj, "o")', False],
        ["endsWith(hello, nullObj)", True],
        # startsWith
        ['startsWith("hello", "h")', True],
        ['startsWith("hello", "a")', False],
        ['startsWith(nullObj, "o")', False],
        ['endsWith("hello", nullObj)', True],
        # countWord
        ['countWord("hello")', 1],
        ['countWord(concat("hello", " ", "world"))', 2],
        ["countWord(nullObj)", 0],
        # addOrdinal
        ["addOrdinal(11)", "11th"],
        ["addOrdinal(11+1)", "12th"],
        ["addOrdinal(11+2)", "13th"],
        ["addOrdinal(11+10)", "21st"],
        ["addOrdinal(11+11)", "22nd"],
        ["addOrdinal(11+12)", "23rd"],
        ["addOrdinal(11+13)", "24th"],
        ["addOrdinal(-1)", "-1"],
        # newGuid
        ["length(newGuid())", 36],
        # indexOf
        ["indexOf('hello', '-')", -1],
        ["indexOf('hello', 'h')", 0],
        ["indexOf(createArray('abc', 'def', 'ghi'), 'def')", 1],
        ["indexOf(createArray('abc', 'def', 'ghi'), 'klm')", -1],
        # lastIndexOf
        ["lastIndexOf('hello', '-')", -1],
        ["lastIndexOf('hello', 'l')", 3],
        ["lastIndexOf(createArray('abc', 'def', 'ghi', 'def'), 'def')", 3],
        ["lastIndexOf(createArray('abc', 'def', 'ghi'), 'klm')", -1],
        ["lastIndexOf(newGuid(), '-')", 23],
        # eol
        ["EOL()", "\r\n" if platform.system() == "Windows" else "\n"],
        # sentenceCase
        ["sentenceCase('abc')", "Abc"],
        ["sentenceCase('aBc')", "Abc"],
        ["sentenceCase('a')", "A"],
        # titleCase
        ["titleCase('a')", "A"],
        ["titleCase('abc dEF')", "Abc Def"],
        # Collection functions
        # count
        ["count('hello')", 5],
        ['count("hello")', 5],
        ["count(createArray('h', 'e', 'l', 'l', 'o'))", 5],
        # contains
        ["contains('hello world', 'hello')", True],
        ["contains('hello world', 'hellow')", False],
        ["contains('hello world',\r\n 'hellow')", False],
        ["contains(items, 'zero')", True],
        ["contains(items, 'hi')", False],
        ["contains(bag, 'three')", True],
        ["contains(bag, 'xxx')", False],
        # empty
        ["empty('')", True],
        ["empty('a')", False],
        ["empty(bag)", False],
        ["empty(items)", False],
        # join
        ["join(items, ',')", "zero,one,two"],
        ["join(createArray('a', 'b', 'c'), '.')", "a.b.c"],
        ["join(createArray('a', 'b', 'c'), ',', ' and ')", "a,b and c"],
        ["join(createArray('a', 'b'), ',', ' and ')", "a and b"],
        ["join(createArray(\r\n'a',\r\n 'b'), ','\r\n,\r\n ' and ')", "a and b"],
        # first
        ["first(items)", "zero"],
        ["first('hello')", "h"],
        ["first(createArray(0, 1, 2))", 0],
        ["first(1)", None],
        ["first(nestedItems).x", 1],
        # last
        ["last(items)", "two"],
        ["last('hello')", "o"],
        ["last(createArray(0, 1, 2))", 2],
        ["last(1)", None],
        ["last(nestedItems).x", 3],
        # foreach
        [
            "join(foreach(dialog, item, item.key), ',')",
            "x,instance,options,title,subTitle",
        ],
        [
            "join(foreach(dialog, item => item.key), ',')",
            "x,instance,options,title,subTitle",
        ],
        ["foreach(dialog, item, item.value)[1].xxx", "instance"],
        ["foreach(dialog, item=>item.value)[1].xxx", "instance"],
        ["join(foreach(items, item, item), ',')", "zero,one,two"],
        ["join(foreach(items, item=>item), ',')", "zero,one,two"],
        ["join(foreach(nestedItems, i, i.x + first(nestedItems).x), ',')", "2,3,4"],
        [
            "join(foreach(items, item, concat(item, string(count(items)))), ',')",
            "zero3,one3,two3",
        ],
        # select
        ["join(select(items, item, item), ',')", "zero,one,two"],
        ["join(select(items, item=> item), ',')", "zero,one,two"],
        ["join(select(nestedItems, i, i.x + first(nestedItems).x), ',')", "2,3,4"],
        [
            "join(select(items, item, concat(item, string(count(items)))), ',')",
            "zero3,one3,two3",
        ],
        # where
        ["join(where(items, item, item == 'two'), ',')", "two"],
        ["join(where(items, item => item == 'two'), ',')", "two"],
        [
            "string(where(dialog, item, item.value=='Dialog Title'))",
            "{'title': 'Dialog Title'}",
        ],
        [
            "join(foreach(where(nestedItems, item, item.x > 1), result, result.x), ',')",
            "2,3",
        ],
        [
            "count(where(doubleNestedItems, items, count(where(items, item, item.x == 1)) == 1))",
            1,
        ],
        [
            "count(where(doubleNestedItems, items, count(where(items, item, count(items) == 1)) == 1))",
            1,
        ],
        # union
        [
            'union(["a", "b", "c"], ["d", ["e", "f"], "g"][1])',
            ["a", "b", "c", "e", "f"],
        ],
        ['union(["a", "b", "c"], ["d", ["e", "f"], "g"][1])[1]', "b"],
        ["count(union(createArray('a', 'b')))", 2],
        [
            "count(union(createArray('a', 'b'), createArray('b', 'c'), createArray('b', 'd')))",
            4,
        ],
        # intersection
        ['count(intersection(createArray("a", "b")))', 2],
        [
            'count(intersection(createArray("a", "b"), createArray("b", "c"), createArray("b", "d")))',
            1,
        ],
        # skip
        ["skip(createArray('H','e','l','l','0'),2)", ["l", "l", "0"]],
        # take
        ["take(hello, two)", "he"],
        ["take(createArray('a', 'b', 'c', 'd'), one)", ["a"]],
        # subArray
        ["subArray(createArray('a', 'b', 'c', 'd'), 1, 3)", ["b", "c"]],
        ["subArray(createArray('a', 'b', 'c', 'd'), 1)", ["b", "c", "d"]],
        # sortBy
        ["sortBy(items)", ["one", "two", "zero"]],
        ["sortBy(nestedItems, 'x')[0].x", 1],
        # sortByDescending
        ["sortByDescending(items)", ["zero", "two", "one"]],
        ["sortByDescending(nestedItems, 'x')[0].x", 3],
        # indicesAndValues
        ["first(where(indicesAndValues(items), elt, elt.index > 1)).value", "two"],
        ['first(where(indicesAndValues(bag), elt, elt.index == "three")).value', 3],
        [
            'join(foreach(indicesAndValues(items), item, item.value), ",")',
            "zero,one,two",
        ],
        [
            'join(foreach(indicesAndValues(items), item=>item.value), ",")',
            "zero,one,two",
        ],
        # flatten
        [
            "flatten(createArray(1,createArray(2),createArray(createArray(3, 4), createArray(5,6))))",
            [1, 2, 3, 4, 5, 6],
        ],
        [
            "flatten(createArray(1,createArray(2),createArray(createArray(3, 4), createArray(5,6))), 1)",
            [1, 2, [3, 4], [5, 6]],
        ],
        # unique
        ["unique(createArray(1, 5, 1))", [1, 5]],
        ["unique(createArray(5, 5, 1, 2))", [1, 2, 5]],
    ]

    def test_expression_parser_functional(self):
        for data in self.data_source:
            input = str(data[0])
            parsed = Expression.parse(input)
            assert parsed is not None

            value, error = parsed.try_evaluate(self.scope)

            assert (
                error is None
            ), "input: {0}, Has error: {1}, with expression {0}".format(input, error)

            if isinstance(value, numbers.Number) and isinstance(
                data[1], numbers.Number
            ):
                assert math.isclose(
                    value, data[1], rel_tol=1e-9
                ), "actual is: {}, expected is {}, with expression {}".format(
                    value, data[1], input
                )
            else:
                assert (
                    value == data[1]
                ), "actual is: {}, expected is {}, with expression {}".format(
                    value, data[1], input
                )
