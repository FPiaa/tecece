from dsl.dsl import precondition

@precondition("+B Teste(1, 1+1): B batata(X, Y), X = Y, B teste(X), self.inner_function(X * 3) = Y")
def foo(x, y):
    print("foo")


