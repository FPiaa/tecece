from antlr4 import CommonTokenStream, InputStream
from .grammar.ExprLexer import ExprLexer
from .grammar.ExprParser import ExprParser
from .DslToPythonTransformer import DslTransformer
from io import StringIO


def parse(input):
    lexer = ExprLexer(InputStream(input))
    stream = CommonTokenStream(lexer)
    parser = ExprParser(stream)
    tree = parser.expr()
    return DslTransformer().visit(tree)


def precondition(guard):
    def inner(function):
        print()

    return inner


def talk(input):
    print("do something")
