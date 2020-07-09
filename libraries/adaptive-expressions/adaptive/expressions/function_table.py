import expression_evaluator as expr_eval
import expression_functions as expr_functions

class FunctionTable:
    def get(self, key: str) -> expr_eval.ExpressionEvaluator:
        function = expr_functions.ExpressionFunctions.standard_functions.get(key)
        if function:
            return function

        return None
