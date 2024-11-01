from dsl.dsl import precondition

@precondition("+B Teste(X, 1+1): not 2 | 3 & 4, not ((2 | 3) & 4)")
def foo(x, y):
    print("foo")


