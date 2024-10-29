from dsl.dsl import precondition

@precondition("where {1: 1, 2: 2}")
def foo(x, y):
    print("foo")


