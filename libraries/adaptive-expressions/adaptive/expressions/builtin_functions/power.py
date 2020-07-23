import math
from ..expression_type import POWER
from ..function_utils import FunctionUtils
from .multi_variate_numeric_evaluator import MultivariateNumericEvaluator


class Power(MultivariateNumericEvaluator):
    def __init__(self):
        super().__init__(
            POWER, Power.evaluator, FunctionUtils.verify_numeric_list_or_number
        )

    @staticmethod
    def evaluator(args: []):
        return math.pow(args[0], args[1])
