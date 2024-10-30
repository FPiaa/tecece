from dsl.dsl import precondition


def foo(x, y):
    if not 1 < 2 == 3 != 4:
        print('Condição false')
        return False
    print('foo')
