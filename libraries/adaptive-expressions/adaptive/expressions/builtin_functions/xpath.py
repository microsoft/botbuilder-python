from lxml import etree
from ..expression_type import XPATH
from ..function_utils import FunctionUtils
from ..return_type import ReturnType
from ..expression_evaluator import ExpressionEvaluator, EvaluateExpressionDelegate


class XPath(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            XPATH, XPath.evaluator(), ReturnType.Object, XPath.validator,
        )

    @staticmethod
    def evaluator() -> EvaluateExpressionDelegate:
        def anonymous_function(args: list):
            return XPath.eval_xpath(args[0], args[1])

        return FunctionUtils.apply_with_error(anonymous_function)

    @staticmethod
    def eval_xpath(xml_obj: str, xpath: str):
        value: object = None
        result: object = None
        error: str = None
        try:
            # pylint:disable = c-extension-no-member)
            selector = etree.HTML(xml_obj)
        except:
            error = "not valid xml input"

        if error is None:
            node_list = []
            try:
                value = selector.xpath(xpath)
                if isinstance(value, list):
                    for i in value:
                        # pylint:disable = c-extension-no-member)
                        node_list.append(bytes.decode(etree.tostring(i)).strip())
                    if len(node_list) == 0:
                        error = "there is no matched nodes in the xml."
            except:
                error = "cannot evaluate the xpath query expression: {" + xpath + "}"
            if error is None:
                if len(node_list) >= 1:
                    result = node_list
                else:
                    result = value
        return result, error

    @staticmethod
    def validator(expression: object):
        FunctionUtils.validate_order(
            expression, None, ReturnType.Object, ReturnType.String
        )
