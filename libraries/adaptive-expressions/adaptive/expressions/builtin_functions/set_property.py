from ..expression_type import SETPROPERTY
from ..function_utils import FunctionUtils
from ..return_type import ReturnType
from ..expression_evaluator import ExpressionEvaluator, EvaluateExpressionDelegate


class SetProperty(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            SETPROPERTY,
            SetProperty.evaluator(),
            ReturnType.Object,
            SetProperty.validator,
        )

    @staticmethod
    def evaluator() -> EvaluateExpressionDelegate:
        def anonymous_function(args: list):
            new_obj = args[0]
            new_obj[args[1]] = args[2]
            return new_obj

        return FunctionUtils.apply(anonymous_function)

    @staticmethod
    def validator(expression: object):
        FunctionUtils.validate_order(
            expression, None, ReturnType.Object, ReturnType.String, ReturnType.Object
        )
