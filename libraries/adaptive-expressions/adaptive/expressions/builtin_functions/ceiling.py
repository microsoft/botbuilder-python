import math
from ..expression_type import CEILING
from .number_transform_evaluator import NumberTransformEvaluator


class Ceiling(NumberTransformEvaluator):
    def __init__(self):
        super().__init__(CEILING, Ceiling.function)

    @staticmethod
    def function(args: list):
        return math.ceil(args[0])
