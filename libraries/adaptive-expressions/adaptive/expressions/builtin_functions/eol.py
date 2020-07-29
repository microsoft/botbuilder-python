import os
from ..expression_evaluator import ExpressionEvaluator, EvaluateExpressionDelegate
from ..expression_type import EOL
from ..function_utils import FunctionUtils
from ..return_type import ReturnType


class Eol(ExpressionEvaluator):
    def __init__(self):
        super().__init__(EOL, Eol.evaluator(), ReturnType.String, Eol.validator)

    @staticmethod
    def evaluator() -> EvaluateExpressionDelegate:
        # pylint: disable = W0613
        def anonymous_function(args):
            return os.linesep

        return FunctionUtils.apply(anonymous_function)

    @staticmethod
    def validator(expression: object):
        FunctionUtils.validate_arity_and_any_type(expression, 0, 0)
