from urllib.parse import urlparse
from ..options import Options
from ..expression_type import URIPATH
from ..function_utils import FunctionUtils
from ..return_type import ReturnType
from ..expression_evaluator import ExpressionEvaluator


class UriPath(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            URIPATH,
            UriPath.evaluator,
            ReturnType.String,
            FunctionUtils.validate_unary_string,
        )

    @staticmethod
    def evaluator(expression: object, state, options: Options):
        value: object = None
        error: str = None
        args: list
        args, error = FunctionUtils.evaluate_children(expression, state, options)
        if error is None:
            if isinstance(args[0], str):
                parsed = urlparse(args[0])
                value = parsed.path
                if not bool(parsed.netloc):
                    error = "invalid operation, input uri should be an absolute URI"
            else:
                error = "{} should be a string.".format(str(args[0]))
        return value, error
