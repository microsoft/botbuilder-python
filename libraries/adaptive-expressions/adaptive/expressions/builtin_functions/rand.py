import math
import random
from ..expression_evaluator import ExpressionEvaluator
from ..expression_type import RAND
from ..function_utils import FunctionUtils
from ..return_type import ReturnType


class Rand(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            RAND,
            Rand.evaluator(),
            ReturnType.Number,
            FunctionUtils.validate_binary_number,
        )

    @staticmethod
    def evaluator():
        def anonymous_func(args: list):
            error: str = None
            if args[0] > args[1]:
                error = "Min value {} cannot be greater than max value {}.".format(
                    str(args[0]), str(args[1])
                )

            value = math.floor(random.uniform(0, 1) * (args[1] - args[0]) + args[0])

            return value, error

        return FunctionUtils.apply_with_error(
            anonymous_func, FunctionUtils.verify_integer
        )
