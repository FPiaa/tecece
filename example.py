from dsl.dsl import precondition

@precondition("+B Teste(X, 1+1): 1+1, B teste, G oi(2, 3), better.call.saul(Bs, Bs)")
def foo(x, y):
    print("foo")


