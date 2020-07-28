from ..expression_type import TRIM
from .string_transform_evaluator import StringTransformEvaluator


class Trim(StringTransformEvaluator):
    def __init__(self):
        super().__init__(TRIM, Trim.func)

    @staticmethod
    def func(args: list):
        if args[0] is None:
            return ""
        return str(args[0]).strip()
