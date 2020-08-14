from ..options import Options
from ..expression_type import SETPATHTOVALUE
from ..function_utils import FunctionUtils
from ..return_type import ReturnType
from ..expression_evaluator import ExpressionEvaluator


class SetPathToValue(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            SETPATHTOVALUE,
            SetPathToValue.evaluator,
            ReturnType.Object,
            FunctionUtils.validate_binary,
        )

    @staticmethod
    def evaluator(expression: object, state, options: Options):
        path, left, error = FunctionUtils.try_accumulate_path(
            expression.children[0], state, options
        )
        if error is not None:
            return None, error
        if left is not None:
            # the expression can't be fully merged as a path
            return (
                None,
                "{"
                + expression.children[0].to_string()
                + "is not a valid path to set value.",
            )
        value, err = expression.children[1].try_evaluate(state, options)
        if err is not None:
            return None, err
        state.set_value(path, value)
        return value, None
