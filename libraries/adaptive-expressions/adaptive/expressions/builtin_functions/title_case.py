from ..expression_type import TITLECASE
from .string_transform_evaluator import StringTransformEvaluator


class TitleCase(StringTransformEvaluator):
    def __init__(self):
        super().__init__(TITLECASE, TitleCase.func)

    @staticmethod
    def func(args: list):
        input_str = str(args[0])
        if input_str is None or len(input_str) == 0:
            return ""
        return input_str.title()
