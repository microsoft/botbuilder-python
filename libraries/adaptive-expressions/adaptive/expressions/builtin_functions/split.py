from ..expression_evaluator import ExpressionEvaluator
from ..expression_type import SPLIT
from ..function_utils import FunctionUtils
from ..return_type import ReturnType


class Split(ExpressionEvaluator):
    def __init__(self):
        super().__init__(SPLIT, Split.evaluator(), ReturnType.Array, Split.validator)

    @staticmethod
    def evaluator():
        def anonymous_function(args: list):
            input_str = ""
            seperator = ""
            if len(args) == 1:
                if isinstance(args[0], str):
                    input_str = args[0]
            else:
                if isinstance(args[0], str):
                    input_str = args[0]
                if isinstance(args[1], str):
                    seperator = args[1]
            if len(seperator) == 0:
                return [s for s in input_str]
            res = [input_str]
            for sep in seperator:
                temp = []
                for input_s in res:
                    temp += input_s.split(sep)
                res = temp
            return res

        return FunctionUtils.apply(
            anonymous_function, FunctionUtils.verify_string_or_null
        )

    @staticmethod
    def validator(expression: object):
        FunctionUtils.validate_arity_and_any_type(expression, 1, 2, ReturnType.String)
