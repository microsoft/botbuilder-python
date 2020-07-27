from .expression_type import ADD, SUBTRACT, MULTIPLY, DIVIDE, MOD

# math
from .builtin_functions.add import Add
from .builtin_functions.subtract import Subtract
from .builtin_functions.multiply import Multiply
from .builtin_functions.divide import Divide
from .builtin_functions.min import Min
from .builtin_functions.max import Max
from .builtin_functions.power import Power
from .builtin_functions.mod import Mod
from .builtin_functions.average import Average
from .builtin_functions.sum import Sum
from .builtin_functions.range import Range
from .builtin_functions.floor import Floor
from .builtin_functions.ceiling import Ceiling
from .builtin_functions.round import Round

# memory
from .builtin_functions.create_array import CreateArray


def get_standard_functions() -> dict:
    functions = []

    # math
    functions.append(Add())
    functions.append(Subtract())
    functions.append(Multiply())
    functions.append(Divide())
    functions.append(Min())
    functions.append(Max())
    functions.append(Power())
    functions.append(Mod())
    functions.append(Average())
    functions.append(Sum())
    functions.append(Range())
    functions.append(Floor())
    functions.append(Ceiling())
    functions.append(Round())

    # memory
    functions.append(CreateArray())

    lookup = dict()
    for function in functions:
        lookup[function.expr_type] = function

    lookup["add"] = lookup[ADD]
    lookup["sub"] = lookup[SUBTRACT]
    lookup["mul"] = lookup[MULTIPLY]
    lookup["div"] = lookup[DIVIDE]
    lookup["mod"] = lookup[MOD]

    return lookup


class ExpressionFunctions:
    standard_functions = staticmethod(get_standard_functions())
