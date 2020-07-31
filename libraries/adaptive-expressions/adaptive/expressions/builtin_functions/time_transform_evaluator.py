from datetime import datetime
from typing import Callable
import numbers
from ..expression_evaluator import (
    ExpressionEvaluator,
    EvaluateExpressionDelegate,
)
from ..options import Options
from ..function_utils import FunctionUtils
from ..return_type import ReturnType

class TimeTransformEvaluator(ExpressionEvaluator):
    def __init__(
        self,
        expr_type: str,
        func: Callable[[datetime, int], datetime]
    ):
        super().__init__(
            expr_type,
            TimeTransformEvaluator.evaluator(func),
            ReturnType.String,
            TimeTransformEvaluator.validator
        )
    @staticmethod
    def validator(expression: object):
        FunctionUtils.validate_order(expression, [ReturnType.String], ReturnType.String, ReturnType.Number)

    @staticmethod
    def evaluator(func: Callable[[datetime, int], datetime]) -> EvaluateExpressionDelegate:
        def anonymous_function(expression: object, state, options: Options):
            value: object = None
            error: str = None
            args: list
            args, error = FunctionUtils.evaluate_children(expression, state, options)
            if error is None:
                if isinstance(args[1], numbers.Number):
                    format_string = args[2] if len(args) == 3 and isinstance(args[2], str) \
                         else FunctionUtils.default_date_time_format
                    def anonymous_func(date_time):
                        result = date_time
                        interval, err = FunctionUtils.parse_int(args[1])
                        if err is None:
                            result = func(date_time, interval)
                        return result, err
                    value, error = FunctionUtils.normalize_to_date_time(args[0], anonymous_func)
                    if error is None:
                        value = value.strftime(format_string)[:-4] + "Z"
                else:
                    error = "{" + expression.to_string() + \
                         "} should contain an ISO format timestamp and a time interval integer."
            return value, error
        return anonymous_function
