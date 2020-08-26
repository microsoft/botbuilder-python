from antlr4.error import ErrorListener

# pylint: disable=inherit-non-class
class ParseErrorListener(ErrorListener.ErrorListener):
    # pylint: disable=invalid-name
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise Exception("syntax error at line {}:{} {}".format(line, column, msg))
