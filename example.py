from dsl.dsl import precondition

@precondition("where a.b.cfoo()")
def foo(x, y):
    print("foo")


