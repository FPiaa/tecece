from antlr4 import CommonTokenStream, InputStream
from .grammar.DslLexer import DslLexer
from .grammar.DslParser import DslParser
from .DslToPythonTransformer import DslTransformer
from io import StringIO


def parse(input, name):
    lexer = DslLexer(InputStream(input))
    stream = CommonTokenStream(lexer)
    parser = DslParser(stream)
    tree = parser.plan()
    transformer = DslTransformer(name)
    return transformer.visit(tree), transformer.symbol_list


def parse_structure(input):
    lexer = DslLexer(InputStream(input))
    stream = CommonTokenStream(lexer)
    parser = DslParser(stream)
    tree = parser.knowledge()
    return DslTransformer("knowledge").visit(tree)