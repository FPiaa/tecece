import ast
import astor
from dsl.PythonTransformer import PythonTransformer

with open("example.py", "r") as f:
    tree = ast.parse(f.read())
    tree = PythonTransformer().visit(tree)
    tree = ast.fix_missing_locations(tree)
    with open("build.py", "w") as f:
        f.write(astor.to_source(tree))
    # exec(compile(tree, "<ast>", mode="exec"))
    print()
