from ..expression_type import TOLOWER
from .string_transform_evaluator import StringTransformEvaluator

class ToLower(StringTransformEvaluator):
    def __init__(self):
        super().__init__(TOLOWER, ToLower.func)

    @staticmethod
    def func(args: list):
        if args[0] is None:
            return ""
        return str(args[0]).lower()
