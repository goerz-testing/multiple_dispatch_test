"""Implementation of a :func:`addprint` function with ``multimethod``.

This is mainly to investigate how ``multimethod`` interacts with Sphinx.

Specifically, we want to ensure that :func:`addprint` is categorized as a
function in the summary, and that the RST code

::

    :func:`addprint`

works.
"""
from ..multiple_dispatch import multiple_dispatch


@multiple_dispatch
def addprint(x: int, y: int):
    """Print and "added" representation of `x` and `y`."""
    expr = x + y
    return "base addprint(x=%r, y=%r): %r" % (x, y, expr)


@addprint.register
def addprint(x: str, y: float):
    """Implementation for (str, float)."""
    expr = "%s + %.1f" % (x, y)
    return "str_float addprint(x=%r, y=%r): %r" % (x, y, expr)


@addprint.register(float, str)
def _(x, y):
    """Implementation for (float, str)."""
    expr = "%.1f + %s" % (x, y)
    return "float_str addprint(x=%r, y=%r): %r" % (x, y, expr)
