from .expression_type import ADD, SUBTRACT, MULTIPLY, DIVIDE
from .builtin_functions.add import Add
from .builtin_functions.subtract import Subtract
from .builtin_functions.multiply import Multiply
from .builtin_functions.divide import Divide
from .builtin_functions.min import Min


def get_standard_functions() -> dict:
    functions = []
    functions.append(Add())
    functions.append(Subtract())
    functions.append(Multiply())
    functions.append(Divide())
    functions.append(Min())

    lookup = dict()
    for function in functions:
        lookup[function.expr_type] = function

    lookup["add"] = lookup[ADD]
    lookup["subtract"] = lookup[SUBTRACT]
    lookup["multiply"] = lookup[MULTIPLY]
    lookup["divide"] = lookup[DIVIDE]

    return lookup


class ExpressionFunctions:
    standard_functions = staticmethod(get_standard_functions())
