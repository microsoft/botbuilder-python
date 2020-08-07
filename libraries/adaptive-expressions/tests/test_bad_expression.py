# pylint: disable=too-many-lines
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
