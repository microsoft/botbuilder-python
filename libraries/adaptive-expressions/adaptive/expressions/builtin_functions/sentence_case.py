from ..expression_type import SENTENCECASE
from .string_transform_evaluator import StringTransformEvaluator


class SentenceCase(StringTransformEvaluator):
    def __init__(self):
        super().__init__(SENTENCECASE, SentenceCase.func)

    @staticmethod
    def func(args: list):
        input_str = str(args[0])
        if input_str is None or len(input_str) == 0:
            return ""
        return input_str[0:1].upper() + input_str[1:].lower()
