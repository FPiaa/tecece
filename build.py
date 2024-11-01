from dsl.dsl import precondition


def foo(x, y):
    if not foo(1, 2, 3):
        pass
    print('foo')
