import numbers
from ..expression_type import MULTIPLY
from .multi_variate_numeric_evaluator import MultivariateNumericEvaluator


class Multiply(MultivariateNumericEvaluator):
    def __init__(self):
        super().__init__(MULTIPLY, Multiply.evaluator)

    @staticmethod
    def evaluator(args: []):
        return Multiply.eval_multiply(args[0], args[1])

    @staticmethod
    def eval_multiply(num_a: numbers.Number, num_b: numbers.Number):
        if num_a is None or num_b is None:
            raise Exception("Argument null exception.")

        return num_a * num_b
