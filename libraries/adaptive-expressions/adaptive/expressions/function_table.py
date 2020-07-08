from expression_evaluator import ExpressionEvaluator
from expression_functions import ExpressionFunctions

class FunctionTable:
    def get(self, key: str) -> ExpressionEvaluator:
        function = ExpressionFunctions.standard_functions.get(key)
        if not function:
            return function

        return None
