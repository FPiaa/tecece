from antlr4 import CommonTokenStream, InputStream
from .grammar.DslLexer import DslLexer
from .grammar.DslParser import DslParser
from .DslToPythonTransformer import DslTransformer
from io import StringIO


def parse(input):
    lexer = DslLexer(InputStream(input))
    stream = CommonTokenStream(lexer)
    parser = DslParser(stream)
    tree = parser.prog()
    return DslTransformer().visit(tree)


def precondition(guard):
    def inner(function):
        print()

    return inner


def talk(input):
    print("do something")
