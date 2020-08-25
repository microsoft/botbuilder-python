# pylint: disable=too-many-lines
import math
import json
import platform
from datetime import datetime
import numbers
from dateutil import tz
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
import aiounittest
from datatypes_timex_expression import Timex
from adaptive.expressions import Expression


class ExpressionParserTests(aiounittest.AsyncTestCase):
    scope = {
        "a:b": "stringa:b",
        "$index": "index",
        "alist": [{"Name": "item1"}, {"Name": "item2"}],
        "one": 1.0,
        "two": 2.0,
        "hello": "hello",
        "world": "world",
        "nullObj": None,
        "null": None,
        "bag": {"three": 3.0, "name": "mybag", "index": 3,},
        "items": ["zero", "one", "two"],
        "emptyObject": {},
        "nestedItems": [{"x": 1}, {"x": 2}, {"x": 3},],
        "user": {
            "income": 110.0,
            "outcome": 120.0,
            "nickname": "John",
            "lists": {"todo": ["todo1", "todo2", "todo3"]},
            "listType": "todo",
        },
        "dialog": {
            "x": 3,
            "instance": {"xxx": "instance", "yyy": {"instanceY": "instanceY"}},
            "options": {"xxx": "options", "yyy": ["optionY1", "optionY2"]},
            "title": "Dialog Title",
            "subTitle": "Dialog Sub Title",
        },
        "timestamp": "2018-03-15T13:00:00.000Z",
        "notISOTimestamp": "2018/03/15 13:00:00",
        "timestampObj": parse("2018-03-15T13:00:00.000Z").replace(
            tzinfo=tz.gettz("UTC")
        ),
        "timestampObj2": parse("2018-01-02T02:00:00.000Z").replace(
            tzinfo=tz.gettz("UTC")
        ),
        "timestampObj3": parse("2018-01-01T08:00:00.000Z").replace(
            tzinfo=tz.gettz("UTC")
        ),
        "unixTimestamp": 1521118800,
        "unixTimestampFraction": 1521118800.5,
        "ticks": 637243624200000000,
        "timex": "2020-08-04",
        "validFullDateTimex": Timex("2020-02-20"),
        "invalidFullDateTimex": Timex("xxxx-02-20"),
        "validHourTimex": Timex(timex="2012-12-20T13:40"),
        "invalidHourTimex": Timex("2001-02-20"),
        "validTimeRange": Timex(timex="TEV"),
        "validNow": Timex(timex="PRESENT_REF"),
        "doubleNestedItems": [[{"x": 1}, {"x: 2"}], [{"x": 3}]],
        "xmlStr": "<?xml version='1.0'?> <produce> \
             <item> <name>Gala</name> <type>apple</type> <count>20</count> </item> \
             <item> <name>Honeycrisp</name> <type>apple</type> <count>10</count> </item> </produce>",
        "path": {"array": [1]},
        "jsonStr": json.dumps(
            {
                "Stores": ["Lambton Quay", "Willis Street"],
                "Manufacturers": [
                    {"Name": "Acme Co", "Products": [{"Name": "Anvil", "Price": 50}]},
                    {
                        "Name": "Contoso",
                        "Products": [
                            {"Name": "Elbow Grease", "Price": 99.95},
                            {"Name": "Headlight Fluid", "Price": 4},
                        ],
                    },
                ],
            }
        ),
        "json1": json.dumps(
            {
                "FirstName": "John",
                "LastName": "Smith",
                "Enabled": False,
                "Roles": ["User"],
            }
        ),
        "json2": json.dumps({"Enabled": True, "Roles": ["Customer", "Admin"]}),
        "json3": json.dumps({"Age": 36}),
    }

    data_source = [
        # Accessor and element
        ["$index", "index"],
        ["`hi\\``", "hi`"],  # `hi\`` -> hi`
        ["`hi\\y`", "hi\\y"],  # `hi\y` -> hi\y
        ["`\\${a}`", "${a}"],  # `\${a}` -> ${a}
        ['"ab\\"cd"', 'ab"cd'],  # "ab\"cd" -> ab"cd
        ['"ab`cd"', "ab`cd"],  # "ab`cd" -> ab`cd
        ['"ab\\ncd"', "ab\ncd"],  # "ab\ncd" -> ab[newline] cd
        ['"ab\\ycd"', "ab\\ycd"],  # "ab\ycd" -> ab\ycd
        ["'ab\\'cd'", "ab'cd"],  # 'ab\'cd' -> ab'cd
        ["alist[0].Name", "item1"],
        # String interpolation test
        ["`hi`", "hi"],
        ["`hi\\``", "hi`"],
        ["`${world}`", "world"],
        ["`hi ${string('jack`')}`", "hi jack`"],
        ["`\\${world}`", "${world}"],
        ["length(`hello ${world}`)", 11],
        ['json(`{"foo":"${hello}","item":"${world}"}`).foo', "hello"],
        ["`{expr: hello all}`", "{expr: hello all}"],
        ['json(`{"foo":${{text:"hello"}},"item": "${world}"}`).foo.text', "hello"],
        [
            'json(`{"foo":${{text:"hello", cool: "hot", obj:{new: 123}}},"item": "${world}"}`).foo.text',
            "hello",
        ],
        ["`hi\\`[1,2,3]`", "hi`[1,2,3]"],
        ["`hi ${join(['jack\\`', 'queen', 'king'], ',')}`", "hi jack\\`,queen,king"],
        ['`abc ${concat("[", "]")}`', "abc []"],
        ['`[] ${concat("[]")}`', "[] []"],
        ['`hi ${count(["a", "b", "c"])}`', "hi 3"],
        ["`hello ${world}` == 'hello world'", True],
        ["`hello ${world}` != 'hello hello'", True],
        ["`hello ${user.nickname}` == 'hello John'", True],
        ["`hello ${user.nickname}` != 'hello Dong'", True],
        ["`hello ${string({obj:  1})}`", "hello {'obj': 1}"],
        ['`hello ${string({obj:  "${not expr}"})}`', "hello {'obj': '${not expr}'}"],
        ["`hello ${string({obj:  {a: 1}})}`", "hello {'obj': {'a': 1}}"],
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
        ["replace('hello', 'l', 'k')", "hekko"],
        ["replace('hello', 'L', 'k')", "hello"],
        ["replace(nullObj, 'L', 'k')", ""],
        ["replace('hello', 'L', nullObj)", "hello"],
        ['replace("hello\'", "\'", \'"\')', 'hello"'],
        ["replace('hello\"', '\"', \"'\")", "hello'"],
        ["replace('hello\"', '\"', '\n')", "hello\n"],
        ["replace('hello\n', '\n', '\\\\')", "hello\\"],
        ["replace('hello\\\\', '\\\\', '\\\\\\\\')", "hello\\\\"],
        # replaceIgnoreCase
        ["replaceIgnoreCase('hello', 'L', 'k')", "hekko"],
        ["replaceIgnoreCase(nullObj, 'L', 'k')", ""],
        ["replaceIgnoreCase('hello', 'L', nullObj)", "heo"],
        # split
        ['split("hello", "e")', ["h", "llo"]],
        ['split("hello")', ["h", "e", "l", "l", "o"]],
        ['split("", "e")', [""]],
        ['split("", "")', []],
        ['split("hello", "")', ["h", "e", "l", "l", "o"]],
        # substring
        ["substring(concat('na','me','more'), 0, length('name'))", "name"],
        ["substring('hello', 0, 5)", "hello"],
        ["substring('hello', 0, 3)", "hel"],
        ["substring('hello', 3)", "lo"],
        ["substring(nullObj, 0, 3)", ""],
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
        # type checking functions
        # isBoolean
        ["isBoolean(None)", False],
        ["isBoolean(2 + 3)", False],
        ["isBoolean(2 > 1)", True],
        # isString
        ["isString('abc')", True],
        ["isString(123)", False],
        ["isString(None)", False],
        # isInteger
        ["isInteger('abc')", False],
        ["isInteger(123)", True],
        ["isInteger(None)", False],
        # isFloat
        ["isFloat('abc')", False],
        ["isFloat(123.234)", True],
        ["isFloat(None)", False],
        # isArray
        ["isArray(createArray(1,2,3))", True],
        ["isArray(123.234)", False],
        ["isArray(None)", False],
        # isObject
        ["isObject(None)", False],
        ["isObject(emptyObject)", True],
        ["isObject(dialog)", True],
        ["isObject(123.234)", False],
        # isDateTime
        ["isDateTime(2)", False],
        ["isDateTime(null)", False],
        ["isDateTime(timestamp)", True],
        ["isDateTime(timestampObj)", True],
        # Datetime functions
        # addDays
        ["addDays('2018-03-15T13:00:00.000Z', 1)", "2018-03-16T13:00:00.000Z"],
        ["addDays(timestamp, 1)", "2018-03-16T13:00:00.000Z"],
        ["addDays(timestampObj, 1)", "2018-03-16T13:00:00.000Z"],
        ["addDays(timestamp, 1,'%m-%d-%y')", "03-16-18"],
        # addHours
        ["addHours('2018-03-15T13:00:00.000Z', 1)", "2018-03-15T14:00:00.000Z"],
        ["addHours(timestamp, 1)", "2018-03-15T14:00:00.000Z"],
        ["addHours(timestampObj, 1)", "2018-03-15T14:00:00.000Z"],
        ["addHours(timestamp, 1,'%m-%d-%y %I-%M')", "03-15-18 02-00"],
        # AddMinutes
        ["addMinutes('2018-03-15T13:00:00.000Z', 1)", "2018-03-15T13:01:00.000Z"],
        ["addMinutes(timestamp, 1)", "2018-03-15T13:01:00.000Z"],
        ["addMinutes(timestampObj, 1)", "2018-03-15T13:01:00.000Z"],
        ["addMinutes(timestamp, 1,'%m-%d-%y %I-%M')", "03-15-18 01-01"],
        # addSeconds
        ["addSeconds('2018-03-15T13:00:00.000Z', 1)", "2018-03-15T13:00:01.000Z"],
        ["addSeconds(timestamp, 1)", "2018-03-15T13:00:01.000Z"],
        ["addSeconds(timestampObj, 1)", "2018-03-15T13:00:01.000Z"],
        ["addSeconds(timestamp, 1,'%m-%d-%y %I-%M-%S')", "03-15-18 01-00-01"],
        # dayOfMonth
        ["dayOfMonth('2018-03-15T13:00:00.000Z')", 15],
        ["dayOfMonth(timestamp)", 15],
        ["dayOfMonth(timestampObj)", 15],
        # dayOfWeek
        ["dayOfWeek('2018-03-15T13:00:00.000Z')", 4],
        ["dayOfWeek(timestamp)", 4],
        ["dayOfWeek(timestampObj)", 4],
        # dayOfYear
        ["dayOfYear('2018-03-15T13:00:00.000Z')", 74],
        ["dayOfYear(timestamp)", 74],
        ["dayOfYear(timestampObj)", 74],
        # month
        ["month('2018-03-15T13:00:00.000Z')", 3],
        ["month(timestamp)", 3],
        ["month(timestampObj)", 3],
        # date
        ["date('2018-03-15T13:00:00.000Z')", "3/15/2018"],
        ["date(timestamp)", "3/15/2018"],
        ["date(timestampObj)", "3/15/2018"],
        # year
        ["year('2018-03-15T13:00:00.000Z')", 2018],
        ["year(timestamp)", 2018],
        ["year(timestampObj)", 2018],
        # utcNow
        ["length(utcNow())", 24],
        ["utcNow('%m-%d-%Y')", datetime.utcnow().strftime("%m-%d-%Y")],
        # formatDateTime
        ["formatDateTime('2018-03-15')", "2018-03-15T00:00:00.000Z"],
        ["formatDateTime(notISOTimestamp)", "2018-03-15T13:00:00.000Z"],
        ["formatDateTime(notISOTimestamp, '%m-%d-%y')", "03-15-18"],
        ["formatDateTime(timestampObj)", "2018-03-15T13:00:00.000Z"],
        # formatEpoch
        ["formatEpoch(unixTimestamp)", "2018-03-15T13:00:00.000Z"],
        ["formatEpoch(unixTimestampFraction)", "2018-03-15T13:00:00.500Z"],
        # formatTicks
        ["formatTicks(ticks)", "2020-05-06T11:47:00.000Z"],
        # subtractFromTime
        ["subtractFromTime(timestamp, 1, 'Year')", "2017-03-15T13:00:00.000Z"],
        ["subtractFromTime(timestampObj, 1, 'Year')", "2017-03-15T13:00:00.000Z"],
        ["subtractFromTime(timestamp, 1, 'Month')", "2018-02-15T13:00:00.000Z"],
        ["subtractFromTime(timestamp, 1, 'Week')", "2018-03-08T13:00:00.000Z"],
        ["subtractFromTime(timestamp, 1, 'Day')", "2018-03-14T13:00:00.000Z"],
        ["subtractFromTime(timestamp, 1, 'Hour')", "2018-03-15T12:00:00.000Z"],
        ["subtractFromTime(timestamp, 1, 'Minute')", "2018-03-15T12:59:00.000Z"],
        ["subtractFromTime(timestamp, 1, 'Second')", "2018-03-15T12:59:59.000Z"],
        # dateReadBack
        ["dateReadBack(timestamp, addDays(timestamp, 1))", "tomorrow"],
        ["dateReadBack(timestampObj, addDays(timestamp, 1))", "tomorrow"],
        ["dateReadBack(addDays(timestamp, 1),timestamp)", "yesterday"],
        # getTimeOfDay
        ["getTimeOfDay('2018-03-15T00:00:00.000Z')", "midnight"],
        ["getTimeOfDay(timestampObj)", "afternoon"],
        ["getTimeOfDay('2018-03-15T08:00:00.000Z')", "morning"],
        ["getTimeOfDay('2018-03-15T12:00:00.000Z')", "noon"],
        ["getTimeOfDay('2018-03-15T13:00:00.000Z')", "afternoon"],
        ["getTimeOfDay('2018-03-15T18:00:00.000Z')", "evening"],
        ["getTimeOfDay('2018-03-15T22:00:00.000Z')", "evening"],
        ["getTimeOfDay('2018-03-15T23:00:00.000Z')", "night"],
        # getPastTime
        [
            "getPastTime(1,'Year','%m-%d-%y')",
            (datetime.utcnow() + relativedelta(years=-1)).strftime("%m-%d-%y"),
        ],
        [
            "getPastTime(1,'Month','%m-%d-%y')",
            (datetime.utcnow() + relativedelta(months=-1)).strftime("%m-%d-%y"),
        ],
        [
            "getPastTime(1,'Week','%m-%d-%y')",
            (datetime.utcnow() + relativedelta(weeks=-1)).strftime("%m-%d-%y"),
        ],
        [
            "getPastTime(1,'Day','%m-%d-%y')",
            (datetime.utcnow() + relativedelta(days=-1)).strftime("%m-%d-%y"),
        ],
        # convertFromUTC
        [
            "convertFromUTC('2018-01-02T02:00:00.000Z',\
           'Pacific Standard Time', '%A, %d %B %Y')",
            "Monday, 01 January 2018",
        ],
        [
            "convertFromUTC('2018-01-02T01:00:00.000Z',\
           'America/Los_Angeles', '%A, %d %B %Y')",
            "Monday, 01 January 2018",
        ],
        [
            "convertFromUTC(timestampObj2, 'Pacific Standard Time', '%A, %d %B %Y')",
            "Monday, 01 January 2018",
        ],
        # convertToUTC
        [
            "convertToUTC('01/01/2018 00:00:00', 'Pacific Standard Time')",
            "2018-01-01T08:00:00.000Z",
        ],
        # addToTime
        [
            "addToTime('2018-01-01T08:00:00.000Z', 1, 'Day', '%A, %d %B %Y')",
            "Tuesday, 02 January 2018",
        ],
        [
            "addToTime('2018-01-01T00:00:00.000Z', 1, 'Week')",
            "2018-01-08T00:00:00.000Z",
        ],
        ["addToTime(timestampObj2, 1, 'Week')", "2018-01-09T02:00:00.000Z"],
        # startOfDay
        ["startOfDay('2018-03-15T13:30:30.000Z')", "2018-03-15T00:00:00.000Z"],
        ["startOfDay(timestampObj2)", "2018-01-02T00:00:00.000Z"],
        # startOfHour
        ["startOfHour('2018-03-15T13:30:30.000Z')", "2018-03-15T13:00:00.000Z"],
        ["startOfHour(timestampObj)", "2018-03-15T13:00:00.000Z"],
        # startOfMonth
        ["startOfMonth('2018-03-15T13:30:30.000Z')", "2018-03-01T00:00:00.000Z"],
        ["startOfMonth(timestampObj)", "2018-03-01T00:00:00.000Z"],
        # ticks
        ["ticks('2018-01-01T08:00:00.000Z')", 636503904000000000],
        ["ticks(timestampObj3)", 636503904000000000],
        # ticksToDays
        ["ticksToDays(2193385800000000)", 2538.64097222],
        # ticksToHours
        ["ticksToHours(2193385800000000)", 60927.383333333331],
        # ticksToMinutes
        ["ticksToMinutes(2193385811100000)", 3655643.0185],
        # dateTimeDiff
        [
            "dateTimeDiff('2019-01-01T08:00:00.000Z','2018-01-01T08:00:00.000Z')",
            315360000000000,
        ],
        [
            "dateTimeDiff('2017-01-01T08:00:00.000Z','2018-01-01T08:00:00.000Z')",
            -315360000000000,
        ],
        ["dateTimeDiff(timestampObj,timestampObj2)", 62604000000000],
        # Timex functions
        # isDefinite
        ["isDefinite('helloworld')", False],
        ["isDefinite('2012-12-21')", True],
        ["isDefinite('xxxx-12-21')", False],
        ["isDefinite(validFullDateTimex)", True],
        ["isDefinite(invalidFullDateTimex)", False],
        # isTime
        ["isTime(validHourTimex)", True],
        ["isTime(invalidHourTimex)", False],
        # isDuration
        ["isDuration('PT30M')", True],
        ["isDuration('2012-12-21T12:30')", False],
        # isDate
        ["isDate('PT30M')", False],
        ["isDate('2012-12-21T12:30')", True],
        # isTimeRange
        ["isTimeRange('PT30M')", False],
        ["isTimeRange(validTimeRange)", True],
        # isDateRange
        ["isDateRange('PT30M')", False],
        ["isDateRange('2012-02')", True],
        # isPresent
        ["isPresent('PT30M')", False],
        ["isPresent(validNow)", True],
        # URI parsing functions
        # uriHost
        ["uriHost('https://www.localhost.com:8080')", "www.localhost.com"],
        [
            "uriPath('http://www.contoso.com/catalog/shownew.htm?date=today')",
            "/catalog/shownew.htm",
        ],
        [
            "uriPathAndQuery('http://www.contoso.com/catalog/shownew.htm?date=today')",
            "/catalog/shownew.htm?date=today",
        ],
        ["uriPort('http://www.localhost:8080')", 8080],
        [
            "uriQuery('http://www.contoso.com/catalog/shownew.htm?date=today')",
            "?date=today",
        ],
        ["uriScheme('http://www.contoso.com/catalog/shownew.htm?date=today')", "http"],
        # Object manipulation and construction functions
        # json
        ['indexOf(json(\'["a", "b"]\'), "a")', 0],
        ["indexOf(json('[\"a\", \"b\"]'), 'c')", -1],
        ['lastIndexOf(json(\'["a", "b", "a"]\'), "a")', 2],
        ["lastIndexOf(json('[\"a\", \"b\"]'), 'c')", -1],
        ['json(`{"foo":"${hello}","item":"${world}"}`).foo', "hello"],
        # getProperty
        ["getProperty(bag, concat('na','me'))", "mybag"],
        ["getProperty('bag').index", 3],
        ["getProperty('a:b')", "stringa:b"],
        ["getProperty(concat('he', 'llo'))", "hello"],
        # addProperty
        [
            "addProperty(json('{\"key1\":\"value1\"}'), 'key2','value2')",
            {"key1": "value1", "key2": "value2"},
        ],
        ['foreach(items, x, addProperty({}, "a", x))[0].a', "zero"],
        ['foreach(items, x => addProperty({}, "a", x))[0].a', "zero"],
        [
            "addProperty({\"key1\":\"value1\"}, 'key2','value2')",
            {"key1": "value1", "key2": "value2"},
        ],
        # removeProperty
        [
            'removeProperty(json(\'{"key1":"value1","key2":"value2"}\'), \'key2\')',
            {"key1": "value1"},
        ],
        # setProperty
        [
            "setProperty(json('{\"key1\":\"value1\"}'), 'key1','value2')",
            {"key1": "value2"},
        ],
        ["setProperty({\"key1\":\"value1\"}, 'key1','value2')", {"key1": "value2"}],
        ["setProperty({}, 'key1','value2')", {"key1": "value2"}],
        ["setProperty({}, 'key1','value2{}')", {"key1": "value2{}"}],
        # coalesce
        ["coalesce(nullObj,'hello',nullObj)", "hello"],
        ["coalesce(nullObj, false, 'hello')", False],
        # xPath
        [
            "xPath(xmlStr,'//produce//item//name')",
            ["<name>Gala</name>", "<name>Honeycrisp</name>"],
        ],
        ["xPath(xmlStr,'sum(//produce//item//count)')", 30],
        # setPathToValue
        ["setPathToValue(path.simple, 3) + path.simple", 6],
        ["setPathToValue(path.simple, 5) + path.simple", 10],
        ["setPathToValue(path.array[0], 7) + path.array[0]", 14],
        ["setPathToValue(path.array[1], 9) + path.array[1]", 18],
        # jPath
        ["jPath(jsonStr,'Manufacturers[0].Products[0].Price')", 50],
        [
            "jPath(jsonStr,'$..Products[?(@.Price >= 50)].Name')",
            ["Anvil", "Elbow Grease"],
        ],
        # merge
        [
            "merge(json(json1), json(json2))",
            {
                "FirstName": "John",
                "LastName": "Smith",
                "Enabled": True,
                "Roles": ["Customer", "Admin"],
            },
        ],
        [
            "merge(json(json1), json(json2), json(json3))",
            {
                "FirstName": "John",
                "LastName": "Smith",
                "Enabled": True,
                "Roles": ["Customer", "Admin"],
                "Age": 36,
            },
        ],
        # Memory access tests
        # Regular expression
        # isMatch
        [
            "isMatch('abc', '^[ab]+$')",
            False,
        ],  # simple character classes ([abc]), "+" (one or more)
        ["isMatch('abb', '^[ab]+$')", True],  # simple character classes ([abc])
        [
            "isMatch('123', '^[^abc]+$')",
            True,
        ],  # complemented character classes ([^abc])
        [
            "isMatch('12a', '^[^abc]+$')",
            False,
        ],  # complemented character classes ([^abc])
        [
            "isMatch('123', '^[^a-z]+$')",
            True,
        ],  # complemented character classes ([^a-z])
        [
            "isMatch('12a', '^[^a-z]+$')",
            False,
        ],  # complemented character classes ([^a-z])
        ["isMatch('a1', '^[a-z]?[0-9]$')", True],  # "?" (zero or one)
        ["isMatch('1', '^[a-z]?[0-9]$')", True],  # "?" (zero or one)
        ["isMatch('1', '^[a-z]*[0-9]$')", True],  # "*" (zero or more)
        ["isMatch('abc1', '^[a-z]*[0-9]$')", True],  # "*" (zero or more)
        ["isMatch('ab', '^[a-z]{1}$')", False],  # "{x}" (exactly x occurrences)
        [
            "isMatch('ab', '^[a-z]{1,2}$')",
            True,
        ],  # "{x,y}" (at least x, at most y, occurrences)
        ["isMatch('abc', '^[a-z]{1,}$')", True],  # "{x,}" (x occurrences or more)
        ["isMatch('Name', '^(?i)name$')", True],  # "(?i)x" (x ignore case)
        ["isMatch('FORTUNE', '(?i)fortune|future')", True],  # "x|y" (alternation)
        ["isMatch('FUTURE', '(?i)fortune|future')", True],  # "x|y" (alternation)
        ["isMatch('A', '(?i)fortune|future')", False],  # "x|y" (alternation)
        ["isMatch('abacaxc', 'ab.+?c')", True],  # "+?" (lazy versions)
        ["isMatch('abacaxc', 'ab.*?c')", True],  # "*?" (lazy versions)
        ["isMatch('abacaxc', 'ab.??c')", True],  # "??" (lazy versions)
        [
            "isMatch('12abc34', '([0-9]+)([a-z]+)([0-9]+)')",
            True,
        ],  # "(...)" (simple group)
        [
            "isMatch('12abc', '([0-9]+)([a-z]+)([0-9]+)')",
            False,
        ],  # "(...)" (simple group)
        ["isMatch('a', '\\w{1}')", True],  # "\w" (match [a-zA-Z0-9_])
        ["isMatch('1', '\\d{1}')", True],  # "\d" (match [0-9])
        ["isMatch('12.5', '[0-9]+(\\.5)')", True],  # "\." (match .)
        ["isMatch('12x5', '[0-9]+(\\.5)')", False],  # "\." (match .)
    ]

    def test_expression_parser_functions(self):
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
