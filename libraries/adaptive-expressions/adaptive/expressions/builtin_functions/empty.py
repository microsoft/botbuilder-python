from .comparison_evaluator import ComparisonEvaluator
from ..expression_type import EMPTY
from ..function_utils import FunctionUtils


class Empty(ComparisonEvaluator):
    def __init__(self):
        super().__init__(
            EMPTY,
            Empty.function,
            FunctionUtils.validate_unary,
            FunctionUtils.verify_container,
        )

    @staticmethod
    def function(args: list):
        return Empty.is_empty(args[0])

    @staticmethod
    def is_empty(instance: object):
        result: bool
        if instance is None:
            result = True
        elif isinstance(instance, str):
            result = instance == ""
        elif isinstance(instance, (list, dict)):
            result = len(instance) == 0
        else:
            result = False

        return result
