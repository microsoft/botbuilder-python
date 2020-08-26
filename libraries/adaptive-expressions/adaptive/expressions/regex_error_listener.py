from antlr4.error import ErrorListener

# pylint: disable=inherit-non-class
class RegexErrorListener(ErrorListener.ErrorListener):
    # pylint: disable=invalid-name
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise Exception("Regular expression is invalid.")
