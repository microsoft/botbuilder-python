from ..expression_type import TOUPPER
from .string_transform_evaluator import StringTransformEvaluator


class ToUpper(StringTransformEvaluator):
    def __init__(self):
        super().__init__(TOUPPER, ToUpper.func)

    @staticmethod
    def func(args: list):
        if args[0] is None:
            return ""
        return str(args[0]).upper()
