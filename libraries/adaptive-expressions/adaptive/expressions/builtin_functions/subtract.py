import numbers
from ..expression_type import SUBTRACT
from .multi_variate_numeric_evaluator import MultivariateNumericEvaluator


class Subtract(MultivariateNumericEvaluator):
    def __init__(self):
        super().__init__(SUBTRACT, Subtract.evaluator)

    @staticmethod
    def evaluator(args: []):
        return Subtract.eval_subtract(args[0], args[1])

    @staticmethod
    def eval_subtract(num_a: numbers.Number, num_b: numbers.Number):
        if num_a is None or num_b is None:
            raise Exception("Argument null exception.")

        return num_a - num_b
