from dsl.dsl import precondition

@precondition("+B Teste(X, 1+1): 1+1")
def foo(x, y):
    print("foo")


