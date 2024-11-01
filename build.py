from dsl.dsl import precondition


def foo(x, y):
    if not (not 2 or 3 and 4):
        pass
    if not not ((2 or 3) and 4):
        pass
    print('foo')
