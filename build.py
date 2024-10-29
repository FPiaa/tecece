from dsl.dsl import precondition


def foo(x, y):
    if not (x < y and x * y <= 100):
        print('Condição false')
        return False
    print('FOO')


def blah(a, b):
    if a < b and b <= a:
        print()
        return 2


def example():
    print('DOC STRING 1')
    print('HELLO WORLD')
    print('DOC STRING 2')
    foo(1, 2)
    foo(2, 1)
    foo(2, 51)


example()
