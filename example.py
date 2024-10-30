from dsl.dsl import precondition

@precondition("where 1 < 2 = 3 != 4 ")
def foo(x, y):
    print("foo")


