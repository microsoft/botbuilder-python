from .expression_type import ADD, SUBTRACT, MULTIPLY, DIVIDE, EQUAL, LESSTHAN, LESSTHANOREQUAL
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

    return lookup


class ExpressionFunctions:
    standard_functions = staticmethod(get_standard_functions())
