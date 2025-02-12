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
    ctx_functions = []

    def visit_ClassDef(self, node: ast.ClassDef) -> Any:
        self.generic_visit(node)
        node.body = [*self.ctx_functions, *node.body]
        return node
    
    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        precondition_found = [
            x
            for x in node.decorator_list
            if isinstance(x, ast.Call)
            and (
                (isinstance(x.func, ast.Name) and x.func.id == "pl")
                or (isinstance(x.func, ast.Attribute) and x.func.attr == "pl")
            )
        ]

        if not precondition_found:
            return node

        if not isinstance(precondition_found[0].args[0], ast.Constant):
            return node

        precondition = dsl.parse(precondition_found[0].args[0].value, node.name)
        # print(ast.dump(precondition[2], indent=4))
        # early return
        
        print(astor.to_source(precondition[2]))
        for x in node.decorator_list:
            print("in decorator")
            if isinstance(x, ast.Call) and (isinstance(x.func, ast.Name) and x.func.id == 'pl' or isinstance(x.func, ast.Attribute) and x.func.attr == 'pl'):
                call = ast.Name(id=precondition[2].name, ctx=ast.Load())
                x.args = [precondition[0], precondition[1], call]
                self.ctx_functions.append(precondition[2])
        print(ast.dump(node, indent=4))
        return node


with open("example.py", "r") as f:
    tree = ast.parse(f.read())
    tree = DslToPython().visit(tree)
    tree = ast.fix_missing_locations(tree)
    with open("build.py", "w") as f:
        f.write(astor.to_source(tree))
    # exec(compile(tree, "<ast>", mode="exec"))
    print()
