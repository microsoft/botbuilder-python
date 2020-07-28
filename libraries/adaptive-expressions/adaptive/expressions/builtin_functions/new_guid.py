import uuid
from ..expression_evaluator import ExpressionEvaluator, EvaluateExpressionDelegate
from ..expression_type import NEWGUID
from ..function_utils import FunctionUtils
from ..return_type import ReturnType


class NewGuid(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            NEWGUID, NewGuid.evaluator(), ReturnType.String, NewGuid.validator
        )

    @staticmethod
    def evaluator() -> EvaluateExpressionDelegate:
        # pylint: disable = W0613
        def anonymous_function(args):
            return str(uuid.uuid1())

        return FunctionUtils.apply(anonymous_function)

    @staticmethod
    def validator(expression: object):
        FunctionUtils.validate_arity_and_any_type(expression, 0, 0)
