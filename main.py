import ast
import astor
from dsl.PythonTransformer import PythonTransformer

def convert(filename, file_dest):
    with open(filename, "r") as f:
        tree = ast.parse(f.read())
        tree = PythonTransformer().visit(tree)
        tree = ast.fix_missing_locations(tree)
        with open("build.py", "w") as w:
            w.write(astor.to_source(tree))

convert("./example.py", None)