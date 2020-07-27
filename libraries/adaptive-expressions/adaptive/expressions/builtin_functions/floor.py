import math
from ..expression_type import FLOOR
from .number_transform_evaluator import NumberTransformEvaluator


class Floor(NumberTransformEvaluator):
    def __init__(self):
        super().__init__(FLOOR, Floor.function)

    @staticmethod
    def function(args: list):
        return math.floor(args[0])
