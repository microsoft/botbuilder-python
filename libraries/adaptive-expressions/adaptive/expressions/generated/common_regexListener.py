# Generated from common_regex.g4 by ANTLR 4.8
from antlr4 import *

if __name__ is not None and "." in __name__:
    from .common_regexParser import common_regexParser
else:
    from common_regexParser import common_regexParser

# This class defines a complete listener for a parse tree produced by common_regexParser.
class common_regexListener(ParseTreeListener):

    # Enter a parse tree produced by common_regexParser#parse.
    def enterParse(self, ctx: common_regexParser.ParseContext):
        pass

    # Exit a parse tree produced by common_regexParser#parse.
    def exitParse(self, ctx: common_regexParser.ParseContext):
        pass

    # Enter a parse tree produced by common_regexParser#alternation.
    def enterAlternation(self, ctx: common_regexParser.AlternationContext):
        pass

    # Exit a parse tree produced by common_regexParser#alternation.
    def exitAlternation(self, ctx: common_regexParser.AlternationContext):
        pass

    # Enter a parse tree produced by common_regexParser#expr.
    def enterExpr(self, ctx: common_regexParser.ExprContext):
        pass

    # Exit a parse tree produced by common_regexParser#expr.
    def exitExpr(self, ctx: common_regexParser.ExprContext):
        pass

    # Enter a parse tree produced by common_regexParser#element.
    def enterElement(self, ctx: common_regexParser.ElementContext):
        pass

    # Exit a parse tree produced by common_regexParser#element.
    def exitElement(self, ctx: common_regexParser.ElementContext):
        pass

    # Enter a parse tree produced by common_regexParser#quantifier.
    def enterQuantifier(self, ctx: common_regexParser.QuantifierContext):
        pass

    # Exit a parse tree produced by common_regexParser#quantifier.
    def exitQuantifier(self, ctx: common_regexParser.QuantifierContext):
        pass

    # Enter a parse tree produced by common_regexParser#quantifier_type.
    def enterQuantifier_type(self, ctx: common_regexParser.Quantifier_typeContext):
        pass

    # Exit a parse tree produced by common_regexParser#quantifier_type.
    def exitQuantifier_type(self, ctx: common_regexParser.Quantifier_typeContext):
        pass

    # Enter a parse tree produced by common_regexParser#character_class.
    def enterCharacter_class(self, ctx: common_regexParser.Character_classContext):
        pass

    # Exit a parse tree produced by common_regexParser#character_class.
    def exitCharacter_class(self, ctx: common_regexParser.Character_classContext):
        pass

    # Enter a parse tree produced by common_regexParser#capture.
    def enterCapture(self, ctx: common_regexParser.CaptureContext):
        pass

    # Exit a parse tree produced by common_regexParser#capture.
    def exitCapture(self, ctx: common_regexParser.CaptureContext):
        pass

    # Enter a parse tree produced by common_regexParser#non_capture.
    def enterNon_capture(self, ctx: common_regexParser.Non_captureContext):
        pass

    # Exit a parse tree produced by common_regexParser#non_capture.
    def exitNon_capture(self, ctx: common_regexParser.Non_captureContext):
        pass

    # Enter a parse tree produced by common_regexParser#option.
    def enterOption(self, ctx: common_regexParser.OptionContext):
        pass

    # Exit a parse tree produced by common_regexParser#option.
    def exitOption(self, ctx: common_regexParser.OptionContext):
        pass

    # Enter a parse tree produced by common_regexParser#option_flag.
    def enterOption_flag(self, ctx: common_regexParser.Option_flagContext):
        pass

    # Exit a parse tree produced by common_regexParser#option_flag.
    def exitOption_flag(self, ctx: common_regexParser.Option_flagContext):
        pass

    # Enter a parse tree produced by common_regexParser#atom.
    def enterAtom(self, ctx: common_regexParser.AtomContext):
        pass

    # Exit a parse tree produced by common_regexParser#atom.
    def exitAtom(self, ctx: common_regexParser.AtomContext):
        pass

    # Enter a parse tree produced by common_regexParser#cc_atom.
    def enterCc_atom(self, ctx: common_regexParser.Cc_atomContext):
        pass

    # Exit a parse tree produced by common_regexParser#cc_atom.
    def exitCc_atom(self, ctx: common_regexParser.Cc_atomContext):
        pass

    # Enter a parse tree produced by common_regexParser#shared_atom.
    def enterShared_atom(self, ctx: common_regexParser.Shared_atomContext):
        pass

    # Exit a parse tree produced by common_regexParser#shared_atom.
    def exitShared_atom(self, ctx: common_regexParser.Shared_atomContext):
        pass

    # Enter a parse tree produced by common_regexParser#literal.
    def enterLiteral(self, ctx: common_regexParser.LiteralContext):
        pass

    # Exit a parse tree produced by common_regexParser#literal.
    def exitLiteral(self, ctx: common_regexParser.LiteralContext):
        pass

    # Enter a parse tree produced by common_regexParser#cc_literal.
    def enterCc_literal(self, ctx: common_regexParser.Cc_literalContext):
        pass

    # Exit a parse tree produced by common_regexParser#cc_literal.
    def exitCc_literal(self, ctx: common_regexParser.Cc_literalContext):
        pass

    # Enter a parse tree produced by common_regexParser#shared_literal.
    def enterShared_literal(self, ctx: common_regexParser.Shared_literalContext):
        pass

    # Exit a parse tree produced by common_regexParser#shared_literal.
    def exitShared_literal(self, ctx: common_regexParser.Shared_literalContext):
        pass

    # Enter a parse tree produced by common_regexParser#number.
    def enterNumber(self, ctx: common_regexParser.NumberContext):
        pass

    # Exit a parse tree produced by common_regexParser#number.
    def exitNumber(self, ctx: common_regexParser.NumberContext):
        pass

    # Enter a parse tree produced by common_regexParser#octal_char.
    def enterOctal_char(self, ctx: common_regexParser.Octal_charContext):
        pass

    # Exit a parse tree produced by common_regexParser#octal_char.
    def exitOctal_char(self, ctx: common_regexParser.Octal_charContext):
        pass

    # Enter a parse tree produced by common_regexParser#octal_digit.
    def enterOctal_digit(self, ctx: common_regexParser.Octal_digitContext):
        pass

    # Exit a parse tree produced by common_regexParser#octal_digit.
    def exitOctal_digit(self, ctx: common_regexParser.Octal_digitContext):
        pass

    # Enter a parse tree produced by common_regexParser#digits.
    def enterDigits(self, ctx: common_regexParser.DigitsContext):
        pass

    # Exit a parse tree produced by common_regexParser#digits.
    def exitDigits(self, ctx: common_regexParser.DigitsContext):
        pass

    # Enter a parse tree produced by common_regexParser#digit.
    def enterDigit(self, ctx: common_regexParser.DigitContext):
        pass

    # Exit a parse tree produced by common_regexParser#digit.
    def exitDigit(self, ctx: common_regexParser.DigitContext):
        pass

    # Enter a parse tree produced by common_regexParser#name.
    def enterName(self, ctx: common_regexParser.NameContext):
        pass

    # Exit a parse tree produced by common_regexParser#name.
    def exitName(self, ctx: common_regexParser.NameContext):
        pass

    # Enter a parse tree produced by common_regexParser#alpha_nums.
    def enterAlpha_nums(self, ctx: common_regexParser.Alpha_numsContext):
        pass

    # Exit a parse tree produced by common_regexParser#alpha_nums.
    def exitAlpha_nums(self, ctx: common_regexParser.Alpha_numsContext):
        pass

    # Enter a parse tree produced by common_regexParser#non_close_parens.
    def enterNon_close_parens(self, ctx: common_regexParser.Non_close_parensContext):
        pass

    # Exit a parse tree produced by common_regexParser#non_close_parens.
    def exitNon_close_parens(self, ctx: common_regexParser.Non_close_parensContext):
        pass

    # Enter a parse tree produced by common_regexParser#non_close_paren.
    def enterNon_close_paren(self, ctx: common_regexParser.Non_close_parenContext):
        pass

    # Exit a parse tree produced by common_regexParser#non_close_paren.
    def exitNon_close_paren(self, ctx: common_regexParser.Non_close_parenContext):
        pass

    # Enter a parse tree produced by common_regexParser#letter.
    def enterLetter(self, ctx: common_regexParser.LetterContext):
        pass

    # Exit a parse tree produced by common_regexParser#letter.
    def exitLetter(self, ctx: common_regexParser.LetterContext):
        pass


del common_regexParser
