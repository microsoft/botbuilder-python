from .expression_type import ADD, SUBTRACT, MULTIPLY, DIVIDE, EQUAL
from .expression_type import (
    LESSTHAN,
    LESSTHANOREQUAL,
    GREATERTHAN,
    GREATERTHANOREQUAL,
    NOT,
    OR,
    AND,
    CONCAT,
)
from .builtin_functions.add import Add
from .builtin_functions.subtract import Subtract
from .builtin_functions.multiply import Multiply
from .builtin_functions.divide import Divide
from .builtin_functions.min import Min
from .builtin_functions.max import Max
from .builtin_functions.power import Power
from .builtin_functions.equal import Equal
from .builtin_functions.less_than import LessThan
from .builtin_functions.less_than_or_equal import LessThanOrEqual
from .builtin_functions.greater_than import GreaterThan
from .builtin_functions.greater_than_or_equal import GreaterThanOrEqual
from .builtin_functions.not_equal import NotEqual
from .builtin_functions.exist import Exist

from .builtin_functions.not_function import Not
from .builtin_functions.or_function import Or
from .builtin_functions.and_function import And

from .builtin_functions.concat import Concat
from .builtin_functions.length import Length
from .builtin_functions.replace import Replace
from .builtin_functions.replace_ignore_case import ReplaceIgnoreCase
from .builtin_functions.split import Split


def get_standard_functions() -> dict:
    functions = []

    # Math
    functions.append(Add())
    functions.append(Subtract())
    functions.append(Multiply())
    functions.append(Divide())
    functions.append(Min())
    functions.append(Max())
    functions.append(Power())

    # comparison
    functions.append(Equal())
    functions.append(LessThan())
    functions.append(LessThanOrEqual())
    functions.append(GreaterThan())
    functions.append(GreaterThanOrEqual())
    functions.append(NotEqual())
    functions.append(Exist())

    # logic
    functions.append(Not())
    functions.append(Or())
    functions.append(And())

    # string
    functions.append(Concat())
    functions.append(Length())
    functions.append(Replace())
    functions.append(ReplaceIgnoreCase())
    functions.append(Split())
    # TODO: substring, skipped

    lookup = dict()
    for function in functions:
        lookup[function.expr_type] = function

    # Math aliases
    lookup["add"] = lookup[ADD]
    lookup["sub"] = lookup[SUBTRACT]
    lookup["mul"] = lookup[MULTIPLY]
    lookup["div"] = lookup[DIVIDE]

    # Comparison aliases
    lookup["equals"] = lookup[EQUAL]
    lookup["less"] = lookup[LESSTHAN]
    lookup["lessOrEuqals"] = lookup[LESSTHANOREQUAL]
    lookup["greater"] = lookup[GREATERTHAN]
    lookup["greaterOrEquals"] = lookup[GREATERTHANOREQUAL]

    # Logic aliases
    lookup["not"] = lookup[NOT]
    lookup["or"] = lookup[OR]
    lookup["and"] = lookup[AND]

    lookup["&"] = lookup[CONCAT]

    return lookup


class ExpressionFunctions:
    standard_functions = staticmethod(get_standard_functions())
