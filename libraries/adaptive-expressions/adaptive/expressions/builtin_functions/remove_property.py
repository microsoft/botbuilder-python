from ..expression_type import REMOVEPROPERTY
from ..function_utils import FunctionUtils
from ..return_type import ReturnType
from ..expression_evaluator import ExpressionEvaluator, EvaluateExpressionDelegate


class RemoveProperty(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            REMOVEPROPERTY,
            RemoveProperty.evaluator(),
            ReturnType.Object,
            RemoveProperty.validator,
        )

    @staticmethod
    def evaluator() -> EvaluateExpressionDelegate:
        def anonymous_function(args: list):
            new_obj = args[0]
            if args[1] in new_obj:
                del new_obj[args[1]]
            return new_obj

        return FunctionUtils.apply(anonymous_function)

    @staticmethod
    def validator(expression: object):
        FunctionUtils.validate_order(
            expression, None, ReturnType.Object, ReturnType.String
        )
