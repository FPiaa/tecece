from _ast import (
    Call,
    Expr,
    Module,
)
import astor
import ast
from typing import Any
from ast import (
    ImportFrom,
    Not,
    And,
    BinOp,
    BoolOp,
    Compare,
    If,
    Import,
    Lt,
    LtE,
    Mult,
    Name,
    FunctionDef,
    Return,
    UnaryOp,
    alias,
    arguments,
    arg,
    Load,
    Constant,
)

from dsl import dsl

class DslToPython(ast.NodeTransformer):

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        precondition_found = [
            x
            for x in node.decorator_list
            if isinstance(x, ast.Call)
            and (
                (isinstance(x.func, ast.Name) and x.func.id == "precondition")
                or (isinstance(x.func, ast.Attribute) and x.func.attr == "precondition")
            )
        ]

        if not precondition_found:
            return node
        node.decorator_list = [
            x
            for x in node.decorator_list
            if not (
                isinstance(x, ast.Call)
                and (
                    (isinstance(x.func, ast.Name) and x.func.id == "precondition")
                    or (
                        isinstance(x.func, ast.Attribute)
                        and x.func.attr == "precondition"
                    )
                )
            )
        ]

        if not isinstance(precondition_found[0].args[0], ast.Constant):
            return node

        precondition = dsl.parse(precondition_found[0].args[0].value, node.name)
        # print(ast.dump(precondition[2], indent=4))
        # early return
        
        node.body = [*precondition[2:][0], *node.body]
        return node


with open("example.py", "r") as f:
    tree = ast.parse(f.read())
    tree = DslToPython().visit(tree)
    tree = ast.fix_missing_locations(tree)
    with open("build.py", "w") as f:
        f.write(astor.to_source(tree))
    exec(compile(tree, "<ast>", mode="exec"))
    print()
