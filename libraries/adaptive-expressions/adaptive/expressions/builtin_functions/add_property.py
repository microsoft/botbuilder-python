from ..expression_type import ADDPROPERTY
from ..function_utils import FunctionUtils
from ..return_type import ReturnType
from ..expression_evaluator import ExpressionEvaluator, EvaluateExpressionDelegate


class AddProperty(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            ADDPROPERTY,
            AddProperty.evaluator(),
            ReturnType.Object,
            AddProperty.validator,
        )

    @staticmethod
    def evaluator() -> EvaluateExpressionDelegate:
        def anonymous_function(args: list):
            new_obj = args[0]
            prop = args[1]
            error: str = None
            if prop in new_obj:
                error = "{" + prop + "} already exists"
            else:
                new_obj[prop] = args[2]
            return new_obj, error

        return FunctionUtils.apply_with_error(anonymous_function)

    @staticmethod
    def validator(expression: object):
        FunctionUtils.validate_order(
            expression, None, ReturnType.Object, ReturnType.String, ReturnType.Object
        )
