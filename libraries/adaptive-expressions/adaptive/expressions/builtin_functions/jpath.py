import json
import jsonpath
from ..expression_type import JPATH
from ..function_utils import FunctionUtils
from ..return_type import ReturnType
from ..expression_evaluator import ExpressionEvaluator, EvaluateExpressionDelegate


class JPath(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            JPATH, JPath.evaluator(), ReturnType.Object, JPath.validator,
        )

    @staticmethod
    def evaluator() -> EvaluateExpressionDelegate:
        def anonymous_function(args: list):
            return JPath.eval_jpath(args[0], args[1])

        return FunctionUtils.apply_with_error(anonymous_function)

    @staticmethod
    def eval_jpath(json_entity: object, jpath: str):
        result: object = None
        error: str = None
        evaled: object = None
        json_obj: object = None
        if isinstance(json_entity, str):
            try:
                json_obj = json.loads(json_entity)
            except:
                error = "{" + json_entity + "} is not a valid json string."
        elif isinstance(json_entity, object):
            json_obj = json_entity
        else:
            error = "the first parameter should be either an object or a string."
        if not error:
            evaled = jsonpath.jsonpath(json_obj, jpath)
        if len(evaled) == 1:
            result = evaled[0]
        else:
            result = evaled
        return result, error

    @staticmethod
    def validator(expression: object):
        FunctionUtils.validate_order(
            expression, None, ReturnType.Object, ReturnType.String
        )
