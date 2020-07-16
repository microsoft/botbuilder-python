from .expression_type import ADD
from .builtin_functions.add import Add


def get_standard_functions() -> dict:
    functions = []
    functions.append(Add())

    lookup = dict()
    for function in functions:
        lookup[function.expr_type] = function

    lookup["add"] = lookup[ADD]

    return lookup


class ExpressionFunctions:
    standard_functions = staticmethod(get_standard_functions())
