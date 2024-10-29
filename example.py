from dsl.dsl import precondition

"""doc string 1"""

print("hello world")
"""doc string 2"""


@precondition("x < y e x * y <= 100")
def foo(x, y):
    print("foo")


def blah(a, b):
    if a < b and b <= a:
        print()
        return 2


foo(1, 2)
foo(2, 1)
foo(2, 51)
