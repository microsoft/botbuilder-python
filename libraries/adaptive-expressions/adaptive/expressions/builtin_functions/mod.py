import numbers
from ..expression_type import MOD
from ..function_utils import FunctionUtils
from ..expression_evaluator import ExpressionEvaluator
from ..return_type import ReturnType


class Mod(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            MOD,
            Mod.evaluator(),
            ReturnType.Number,
            FunctionUtils.validate_binary_number,
        )

    @staticmethod
    def evaluator():
        def anonymous_function(args: list):
            value: object = None
            error: str
            if args[1] == 0:
                error = "Cannot mod by 0"
            else:
                error = None
                value = Mod.eval_mod(args[0], args[1])

            return value, error

        return FunctionUtils.apply_with_error(
            anonymous_function, FunctionUtils.verify_integer
        )

    @staticmethod
    def eval_mod(num_a: numbers.Number, num_b: numbers.Number):
        if num_a is None or num_b is None:
            raise Exception("Argument null exception.")

        return num_a % num_b
