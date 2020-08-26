# pylint: disable=too-many-lines
import json
import aiounittest
from adaptive.expressions import Expression


class ExpressionParserTests(aiounittest.AsyncTestCase):
    scope = {
        "one": 1.0,
        "two": 2.0,
        "hello": "hello",
        "world": "world",
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
        "xmlStr": "<?xml version='1.0'?> <produce> <item>\
             <name>Gala</name> <type>apple</type> <count>20</count> </item>\
             <item> <name>Honeycrisp</name> <type>apple</type> <count>10</count> </item> </produce>",
        "invalidXml": "<?xml version='1.0'?> <produce> <item>\
             <name>Gala</name> <type>apple</type> <count>20</count> </item>\
             <item> <name>Honeycrisp</name> <type>apple</type> <count>10</count>",
        "json1": json.dumps({"Enabled": True, "Roles": ["User", "Admin"]}),
        "jarray1": "['a', 'b']",
        "relativeUri": "../catalog/shownew.htm?date=today",
    }

    # Invalid expressions
    invalid_expressions = [
        "hello world",
        "a+",
        "a+b*",
        "fun(a, b, c",
        "func(A,b,b,)",
        "\"hello'",
        "user.lists.{dialog.listName}",
        "'hello'.length()",
        "`hi` world",
    ]

    bad_expressions = [
        # General test
        "func()",  # no such func
        "length(func())",  # no such function in children
        "a.func()",  # no such function
        "(1.foreach)()",  # error func
        "('str'.foreach)()",  # error func
        "'hello'.length()",  # not support currently
        # Operators test
        "istrue + 1",  # params should be number or string
        "one + two + nullObj",  # Operator '+' or add cannot be applied to operands of type 'number' and null object.
        "'1' * 2",  # params should be number
        "'1' - 2",  # params should be number
        "'1' / 2",  # params should be number
        "'1' % 2",  # params should be number
        "'1' ^ 2",  # params should be number
        "1/0",  # can not divide 0
        # String functions test
        "length(one, 1)",  # length can only have one param
        "length(replace(hello))",  # children func error
        "replace(hello)",  # replace need three parameters
        "replace(one, 'l', 'k')",  # replace only accept string parameter
        "replace('hi', 1, 'k')",  # replace only accept string parameter
        "replace('hi', 'l', 1)",  # replace only accept string parameter
        "replace('hi', nullObj, 'k')",  # replace oldValue must string length not less than 1
        "replaceIgnoreCase(hello)",  # replaceIgnoreCase need three parameters
        "replaceIgnoreCase('HI', nullObj, 'k')",  # replaceIgnoreCase oldValue must string length not less than 1
        "replaceIgnoreCase(one, 'l', 'k')",  # replaceIgnoreCase only accept string parameter
        "replaceIgnoreCase('hi', 1, 'k')",  # replaceIgnoreCase only accept string parameter
        "replaceIgnoreCase('hi', 'l', 1)",  # replaceIgnoreCase only accept string parameter
        "split(hello, 'l',  'l')",  # split need one or two parameters
        "split(one, 'l')",  # split only accept string parameter
        "split(hello, 1)",  # split only accept string parameter
        "substring(hello, 0.5)",  # the second parameter of substring must be integer
        "substring(two, 0)",  # the first parameter of substring must be string or null
        "substring(hello, 10)",  # the start index is out of the range of the string length
        "substring(hello, 0, hello)",  # length is not integer
        "substring(hello, 0, 'hello')",  # length is not integer
        "substring(hello, 0, 10)",  # the length of substring is out of the range of the original string
        "toLower(one)",  # the parameter of toLower must be string
        "toLower('hi', 1)",  # should have 1 param
        "toUpper(one)",  # the parameter of toUpper must be string
        "toUpper('hi', 1)",  # should have 1 param
        "trim(one)",  # the parameter of trim must be string
        "trim('hi', 1)",  # should have 1 param
        "endsWith(hello, one)",  # should have string params
        "endsWith(one, hello)",  # should have string params
        "endsWith(hello)",  # should have two params
        "startsWith(hello, one)",  # should have string params
        "startsWith(one, hello)",  # should have string params
        "startsWith(hello)",  # should have two params
        "countWord(hello, 1)",  # should have one param
        "countWord(one)",  # should have string param
        "countWord(one)",  # should have string param
        "addOrdinal(one + 0.5)",  # should have Integer param
        "addOrdinal(one, two)",  # should have one param
        "newGuid(one)",  # should have no parameters
        "indexOf(hello)",  # should have two parameters
        "indexOf(hello, world, one)",  # should have two parameters
        "indexOf(hello, one)",  # second parameter should be string
        "indexOf(one, hello)",  # first parameter should be list or string
        "lastIndexOf(hello)",  # should have two parameters
        "lastIndexOf(hello, world, one)",  # should have two parameters
        "lastIndexOf(hello, one)",  # second parameter should be string
        "lastIndexOf(one, hello)",  # first parameter should be list or string
        "sentenceCase(hello, hello)",  # should have one parameters
        "sentenceCase(one)",  # first parameter should be string
        "titleCase(hello, hello)",  # should have one parameters
        "titleCase(one)",  # first parameter should be string
        # Logical comparison functions test
        "greater(one, hello)",  # string and integer are not comparable
        "greater(one)",  # greater need two parameters
        "greaterOrEquals(one, hello)",  # string and integer are not comparable
        "greaterOrEquals(one)",  # function need two parameters
        "less(false, true)",  # string or number parameters are needed
        "less(one, hello)",  # string and integer are not comparable
        "less(one)",  # function need two parameters
        "lessOrEquals(one, hello)",  # string and integer are not comparable
        "lessOrEquals(one)",  # function need two parameters
        "equals(one)",  # equals must accept two parameters
        "exists(1, 2)",  # function need one parameter
        # "if(!exists(one), one, hello)", # the second and third parameters of if must the same type
        "not(false, one)",  # function need one parameter
        # Math functions test
        "max(hello, one)",  # param should be number
        "max()",  # function need 1 or more than 1 parameters
        "min(hello, one)",  # param should be number
        "min()",  # function need 1 or more than 1 parameters
        "add(istrue, 2)",  # param should be number or string
        "add()",  # arg count doesn't match
        "add(one)",  # add function need two or more parameters
        "sub(hello, 2)",  # param should be number
        "sub()",  # arg count doesn't match
        "sub(five, six)",  # no such variables
        "sub(one)",  # sub function need two or more parameters
        "mul(hello, one)",  # param should be number
        "mul(one)",  # mul function need two or more parameters
        "div(one, 0)",  # one cannot be divided by zero
        "div(one)",  # div function need two or more parameters
        "div(hello, one)",  # string hello cannot be divided
        "exp(2, hello)",  # exp cannot accept parameter of string
        "mod(1, 0)",  # mod cannot accept zero as the second parameter
        "mod(5, 2.1 ,3)",  # need two params
        "rand(5, 6.1)",  #  param should be integer
        "rand(5)",  # need two params
        "rand(7, 6)",  #  minvalue cannot be greater than maxValue
        "sum(items)",  # should have number parameters
        "range(one)",  # should have two params
        "range(one, two, three)",  # should have two params
        "range(one, hello)",  # params should be integer
        "range(hello, one)",  # params should be integer
        "range(one, 0)",  # second param should be more than 0
        "floor(hello)",  # should have a numeric parameter
        "floor(1.2, 2)",  # should have only 1 numeric parameter
        "ceiling(hello)",  # should have a numeric parameter
        "ceiling(1.2, 2)",  # should have only 1 numeric parameter
        "round(hello)",  # should have numeric parameters
        "round(1.333, hello)",  # should have numeric parameters
        "ceiling(1.2, 2.1)",  # the second parameter should be integer
        "ceiling(1.2, -2)",  # the second parameter should be integer not less than 0
        "ceiling(1.2, 16)",  # the second parameter should be integer not greater than 15
        "ceiling(1.2, 12, 7)",  # should have one or two numeric parameters
        # collection functions test
        "sum(items, 'hello')",  # should have 1 parameter
        "sum('hello')",  # first param should be list
        "average(items, 'hello')",  # should have 1 parameter
        "average('hello')",  # first param should be list
        "average(hello)",  # first param should be list
        "contains('hello world', 'hello', 'new')",  # should have 2 parameter
        "count(items, 1)",  # should have 1 parameter
        "count(1)",  # first param should be string, array or map
        "empty(1,2)",  # should have two params
        "first(items,2)",  # should have 1 param
        "last(items,2)",  # should have 1 param
        "join(items, 'p1', 'p2','p3')",  # builtin function should have 2-3 params,
        "join(hello, 'hi')",  # first param must list
        "join(items, 1)",  # second param must string
        "join(items, '1', 2)",  # second param must string
        "foreach(hello, item, item)",  # first arg is not list or struture
        "foreach(items, item)",  # should have three parameters
        "foreach(items, item, item2, item3)",  # should have three parameters
        "foreach(items, add(1), item)",  # Second paramter of foreach is not an identifier
        "foreach(items, 1, item)",  # Second paramter error
        "foreach(items, x, sum(x))",  # third paramter error
        "select(hello, item, item)",  # first arg is not list
        "select(items, item)",  # should have three parameters
        "select(items, item, item2, item3)",  # should have three parameters
        "select(items, add(1), item)",  # second paramter of foreach is not an identifier
        "select(items, 1, item)",  # second paramter error
        "select(items, x, sum(x))",  # third paramter error
        "where(hello, item, item)",  # first arg is not list or structure
        "where(items, item)",  # should have three parameters
        "where(items, item, item2, item3)",  # should have three parameters
        "where(items, add(1), item)",  # Second paramter of where is not an identifier
        "where(items, 1, item)",  # Second paramter error
        "where(items, x, sum(x))",  # third paramter error
        "indicesAndValues(items, 1)",  # should only have one parameter
        "indicesAndValues(1)",  # shoud have array param
        "union(one, two)",  # should have collection param
        "intersection(one, two)",  # should have collection param
        "skip(hello)",  # should have two parameters
        "skip(hello, world, one)",  # should have two parameters
        "skip(hello, one)",  # first param should be array
        "skip(items, hello)",  # second param should be integer
        "skip(items, one + 0.5)",  # second param should be integer
        "take(hello)",  # should have two parameters
        "take(hello, world, one)",  # should have two parameters
        "take(one, two)",  # first param should be array or string
        "take(items, hello)",  # second param should be integer
        "take(hello, one + 0.5)",  # second param should be integer
        "subArray(hello)",  # should have 2 or 3 params
        "subArray(one, two, hello, world)",  # should have 2 or 3 params
        "subArray(hello, two)",  # first param should be array
        "subArray(items, hello)",  # second param should be integer
        "subArray(items, one, hello)",  # third param should be integer
        "sortBy(hello, 'x')",  # first param should be list
        "sortBy(createArray('H','e','l','l','o'), 1)",  # second param should be string
        "sortBy(createArray('H','e','l','l','o'), 'x', hi)",  # second param should be string
        # Memory access test
        "getProperty(bag, 1)",  # second param should be string
        "getProperty(1)",  # if getProperty contains only one parameter, the parameter should be string
        "Accessor(1)",  # first param should be string
        "Accessor(bag, 1)",  # second should be object
        "one[0]",  # one is not list
        "items[3]",  # index out of range
        "items[one+0.5]",  # index is not integer
        # Date and time function test
        "isDefinite(12345)",  # should hava a string or a TimexProperty parameter
        "isDefinite('world', 123445)",  # should have only one parameter
        "isTime(123445)",  # should hava a string or a TimexProperty parameter
        "isTime('world', 123445)",  # should have only one parameter
        "isDuration(123445)",  # should hava a string or a TimexProperty parameter
        "isDuration('world', 123445)",  # should have only one parameter
        "isDate(123445)",  # should hava a string or a TimexProperty parameter
        "isDate('world', 123445)",  # should have only one parameter
        "isTimeRange(123445)",  # should hava a string or a TimexProperty parameter
        "isTimeRange('world', 123445)",  # should have only one parameter
        "isDateRange(123445)",  # should hava a string or a TimexProperty parameter
        "isDateRange('world', 123445)",  # should have only one parameter
        "isPresent(123445)",  # should hava a string or a TimexProperty parameter
        "isPresent('world', 123445)",  # should have only one parameter
        "addDays('errortime', 1)",  # error datetime format
        "addDays(timestamp, 'hi')",  # second param should be integer
        "addDays(timestamp)",  # should have 2 or 3 params
        "addDays(timestamp, 1,'yyyy', 2)",  # should have 2 or 3 params
        "addDays(timestamp, 12345678901234)",  # the second parameter should be a 32-bit signed integer
        "addDays(notISOTimestamp, 1)",  # not ISO datetime format
        "addHours('errortime', 1)",  # error datetime format
        "addHours(timestamp, 'hi')",  # second param should be integer
        "addHours(timestamp)",  # should have 2 or 3 params
        "addHours(timestamp, 1,'yyyy', 2)",  # should have 2 or 3 params
        "addHours(timestamp, 12345678901234)",  # the second parameter should be a 32-bit signed integer
        "addHours(notISOTimestamp, 1)",  # not ISO datetime format
        "addMinutes('errortime', 1)",  # error datetime format
        "addMinutes(timestamp, 'hi')",  # second param should be integer
        "addMinutes(timestamp)",  # should have 2 or 3 params
        "addMinutes(timestamp, 1,'yyyy', 2)",  # should have 2 or 3 params
        "addMinutes(timestamp, 12345678901234)",  # the second parameter should be a 32-bit signed integer
        "addMinutes(notISOTimestamp, 1)",  # not ISO datetime format
        "addSeconds('errortime', 1)",  # error datetime format
        "addSeconds(timestamp, 'hi')",  # second param should be integer
        "addSeconds(timestamp)",  # should have 2 or 3 params
        "addSeconds(timestamp, 1,'yyyy', 2)",  # should have 2 or 3 params
        "addSeconds(notISOTimestamp, 1)",  # not ISO datetime format
        "addSeconds(timestamp, 12345678901234)",  # the second parameter should be a 32-bit signed integer
        "dayOfMonth('errortime')",  # error datetime format
        "dayOfMonth(timestamp, 1)",  # should have 1 param
        "dayOfMonth(notISOTimestamp)",  # not ISO datetime format
        "dayOfWeek('errortime')",  # error datetime format
        "dayOfWeek(timestamp, 1)",  # should have 1 param
        "dayOfWeek(notISOTimestamp)",  # not ISO datetime format
        "dayOfYear('errortime')",  # error datetime format
        "dayOfYear(timestamp, 1)",  # should have 1 param
        "dayOfYear(notISOTimestamp)",  # not ISO datetime format
        "month('errortime')",  # error datetime format
        "month(timestamp, 1)",  # should have 1 param
        "month(notISOTimestamp)",  # not ISO datetime format
        "date('errortime')",  # error datetime format
        "date(timestamp, 1)",  # should have 1 param
        "date(notISOTimestamp)",  # not ISO datetime format
        "year('errortime')",  # error datetime format
        "year(timestamp, 1)",  # should have 1 param
        "year(notISOTimestamp)",  # not ISO datetime format
        "formatDateTime('errortime')",  # error datetime format
        "formatDateTime(notValidTimestamp)",  # error datetime format
        "formatDateTime(notValidTimestamp2)",  # error datetime format
        "formatDateTime(notValidTimestamp3)",  # error datetime format
        "formatDateTime({})",  # error valid datetime
        "formatDateTime(timestamp, 1)",  # invalid format string
        "formatEpoch('time')",  # error string
        "formatEpoch(timestamp, 'yyyy', 1)",  # should have 1 or 2 params
        "formatTicks('string')",  # String is not valid
        "formatTicks(2.3)",  # float is not valid
        "formatTicks({})",  # object is not valid
        "subtractFromTime('errortime', 'yyyy', 1)",  # error datetime format
        "subtractFromTime(timestamp, 1, 'W')",  # error time unit
        "subtractFromTime(timestamp, timestamp, 'W')",  # error parameters format
        "subtractFromTime(timestamp, '1', 'Year')",  # second param should be integer
        "subtractFromTime(timestamp, 'yyyy')",  # should have 3 or 4 params
        "subtractFromTime(notISOTimestamp, 1, 'Year')",  # not ISO datetime format
        "dateReadBack('errortime', 'errortime')",  # error datetime format
        "dateReadBack(timestamp)",  # shold have two params
        "dateReadBack(notISOTimestamp, addDays(timestamp, 1))",  # not ISO datetime format
        "getTimeOfDay('errortime')",  # error datetime format
        "getTimeOfDay(timestamp, timestamp)",  # should have 1 param
        "getTimeOfDay(notISOTimestamp)",  # not ISO datetime format
        "getPastTime(1, 'W')",  # error time unit
        "getPastTime(timestamp, 'W')",  # error parameters format
        "getPastTime('yyyy', '1')",  # second param should be integer
        "getPastTime('yyyy')",  # should have 2 or 3 params
        "getFutureTime(1, 'W')",  # error time unit
        "getFutureTime(timestamp, 'W')",  # error parameters format
        "getFutureTime('yyyy', '1')",  # second param should be integer
        "getFutureTime('yyyy')",  # should have 2 or 3 params
        "convertFromUTC(notValidTimestamp, timezone)",  # not valid iso timestamp
        "convertFromUTC(timestamp, invalidTimezone,'D')",  # not valid timezone
        "convertFromUTC(timestamp, timezone, 'a')",  # not valid format
        "convertFromUTC(timestamp, timezone, 'D', hello)",  # should have 2 or 3 params
        "convertToUTC(notValidTimestamp, timezone)",  # not valid timestamp
        "convertToUTC(timestamp, invalidTimezone, 'D')",  # not valid timezone
        "convertToUTC(timestamp, timezone, 'a')",  # not valid format
        "convertToUTC(timestamp, timezone, 'D', hello)",  # should have 2 or 3 params
        "addToTime(notValidTimeStamp, one, 'day')",  # not valid timestamp
        "addToTime(timeStamp, hello, 'day')",  # interval should be integer
        "addToTime(timeStamp, one, 'decade', 'D')",  # not valid time unit
        "addToTime(timeStamp, one, 'week', 'A')",  # not valid format
        "addToTime(timeStamp, one, 'week', 'A', one)",  # should have 3 or 4 params
        "convertTimeZone(notValidTimeStamp, 'UTC', timezone)",  # not valid timestamp
        "convertTimeZone(timestamp2, invalidTimezone, timezone, 'D')",  # not valid source timezone
        "convertTimeZone(timestamp2, timezone, invalidTimezone, 'D')",  # not valid destination timezone
        "convertTimeZone(timestamp2, timezone, 'UTC', 'A')",  # not valid destination timezone
        "startOfDay(notValidTimeStamp)",  # not valid timestamp
        "startOfDay(timeStamp, 'A')",  # not valid format
        "startOfHour(notValidTimeStamp)",  # not valid timestamp
        "startOfHour(timeStamp, 'A')",  # not valid format
        "startOfMonth(notValidTimeStamp)",  # not valid timestamp
        "startOfMonth(timeStamp, 'A')",  # not valid format
        "ticks(notValidTimeStamp)",  # not valid timestamp
        "ticksToDays(12.12)",  # not an integer
        "ticksToHours(timestamp)",  # not an integer
        "ticksToMinutes(timestamp)",  # not an integer
        "dateTimeDiff(notValidTimeStamp,'2018-01-01T08:00:00.000Z')",  # the first parameter is not a valid timestamp
        "dateTimeDiff('2017-01-01T08:00:00.000Z',notValidTimeStamp)",  # the second parameter is not a valid timestamp
        "dateTimeDiff('2017-01-01T08:00:00.000Z','2018-01-01T08:00:00.000Z', 'years')",  # should only have 2 parametes
        # URI parsing functions
        "uriHost(12345)",  # should have 1 string parameter
        "uriHost('aaa', 12345)",  # should have 1 string parameter
        "uriPath(12345)",  # should have 1 string parameter
        "uriPath('acdc', 12345)",  # should have 1 string parameter
        "uriPathAndQuery(12345)",  # should have 1 string parameter
        "uriPathAndQuery('wsad', 12345)",  # should have 1 string parameter
        "uriPort(12345)",  # should have 1 string parameter
        "uriPort('wqq', 12345)",  # should have 1 string parameter
        "uriQuery(12345)",  # should have 1 string parameter
        "uriQuery('qwww', 12345)",  # should have 1 string parameter
        "uriScheme(12345)",  # should have 1 string parameter
        "uriScheme('pqq', 12345)",  # should have 1 string parameter
        # Object manipulation and construction functions
        "json(1,2)",  # should have 1 parameter
        "json(1)",  # should be string parameter
        'json(\'{"key1":value1"}\')',  # invalid json format string
        "addProperty(json('{\"key1\":\"value1\"}'), 'key2','value2','key3')",  # should have 3 parameter
        "addProperty(json('{\"key1\":\"value1\"}'), 1,'value2')",  # second param should be string
        "addProperty(json('{\"key1\":\"value1\"}'), 'key1', 3)",  # cannot add existing property
        "setProperty(json('{\"key1\":\"value1\"}'), 'key2','value2','key3')",  # should have 3 parameter
        "setProperty(json('{\"key1\":\"value1\"}'), 1,'value2')",  # second param should be string
        'removeProperty(json(\'{"key1":"value1","key2":"value2"}\'), 1))',  # second param should be string
        'removeProperty(json(\'{"key1":"value1","key2":"value2"}\'), \'1\', \'2\'))',  # should have 2 parameters
        "coalesce()",  # should have at least 1 parameter
        "xPath(invalidXml, ''sum(/produce/item/count)')",  # not a valid xml
        "xPath(xmlStr)",  # should have two params
        "xPath(xmlStr, 'getTotal')",  # invalid xpath query
        "jPath(hello,'Manufacturers[0].Products[0].Price')",  # not a valid json
        "jPath(hello,'Manufacturers[0]/Products[0]/Price')",  # not a valid path
        "jPath(jsonStr,'$..Products[?(@.Price >= 100)].Name')",  # no matched node
        "merge(json(json1))",  # should have at least two arguments
        "merge(json(json1), json(jarray1))",  # arguments should all be JSON objects
        "merge(json(jarray1), json(json1))",  # arguments should all be JSON objects
        # type checking
        "isString(hello, hello)",  # should have 1 parameter
        "isInteger(2, 3)",  # should have 1 parameter
        "isFloat(1.2, 3.1)",  # should have 1 parameter
        "isArray(createArray(1,2,3), 1)",  # should have 1 parameter
        "isObejct(emptyJObject, hello)",  # should have 1 parameter
        "isDateTime('2018-03-15T13:00:00.000Z', hello)",  # should have 1 parameter
        "isBoolean(false, false)",  # should have 1 parameter
        # isMatch
        "isMatch('^[a-z]+$')",  # should have 2 parameter
        "isMatch('abC', one)",  # second param should be string
        "isMatch(1, '^[a-z]+$')",  # first param should be string
        "isMatch('abC', '^[a-z+$')",  # bad regular expression
        # Conversion functions
        "float(hello)",  # param shoud be float format string
        "float(hello, 1)",  # shold have 1 param
        "int(hello)",  # param shoud be int format string
        "int(1, 1)",  # shold have 1 param
        "string(hello, 1)",  # shold have 1 param
        "bool(false, 1)",  # shold have 1 param
        "binary(hello, world)",  # shoule have 1 param
        "binary(one)",  # should have string param
        "DataUri(hello, world)",  # shoule have 1 param
        "DataUri(false)",  # should have string param
        "uriComponent(hello, world)",  # shoule have 1 param
        "uriComponent(false)",  # should have string param
        "uriComponentToString(hello, world)",  # shoule have 1 param
        "uriComponentToString(false)",  # should have string param
        "dataUriToBinary(hello, world)",  # shoule have 1 param
        "dataUriToBinary(false)",  # should have string param
        "dataUriToString(hello, world)",  # shoule have 1 param
        "dataUriToString(false)",  # should have string param
        "binary(hello, world)",  # shoule have 1 param
        "binary(one)",  # should have string param
        "base64(hello, world)",  # shoule have 1 param
        "base64ToBinary(hello, world)",  # shoule have 1 param
        "base64ToBinary(one)",  # should have string param
        "base64ToString(hello, world)",  # shoule have 1 param
        "base64ToString(false)",  # should have string param
    ]

    def test_exception_for_bad_expressions(self):
        for expression in self.bad_expressions:
            is_fail = False
            input = expression
            try:
                res = Expression.parse(input).try_evaluate(self.scope)
                if res[1] is None:
                    is_fail = True
                else:
                    print(res[1])
            except Exception as err:
                print(str(err))

            if is_fail:
                assert False, "Test method {} did not throw expected exception".format(
                    input
                )

    def test_exception_for_invalid_expressions(self):
        for expression in self.invalid_expressions:
            input = expression
            try:
                Expression.parse(input)
                assert (
                    False
                ), "Test expression {} did not throw expected exception".format(input)
            except Exception as err:
                print(str(err))
