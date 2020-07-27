import numbers
from ..expression_type import DIVIDE
from ..function_utils import FunctionUtils
from .multi_variate_numeric_evaluator import MultivariateNumericEvaluator


class Divide(MultivariateNumericEvaluator):
    def __init__(self):
        super().__init__(DIVIDE, Divide.evaluator, Divide.verify)

    @staticmethod
    def evaluator(args: []):
        return Divide.eval_divide(args[0], args[1])

    @staticmethod
    def verify(val: object, expression: object, pos: int):
        error = FunctionUtils.verify_number(val, expression, pos)
        if error is None and pos > 0 and val == 0:
            error = "Cannot divide by 0 from " + expression

        return error

    @staticmethod
    def eval_divide(num_a: numbers.Number, num_b: numbers.Number):
        if num_a is None or num_b is None:
            raise Exception("Argument null exception.")

        return num_a / num_b
