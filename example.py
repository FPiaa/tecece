from dsl.dsl import precondition

@precondition("+B Teste(X, 1+1): foo(1,2,3)")
def foo(x, y):
    print("foo")


