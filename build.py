from dsl.dsl import precondition


def foo(x, y):
    if not a.b.cfoo():
        print('Condição false')
        return False
    print('foo')
