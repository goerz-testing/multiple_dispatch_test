from multimethod import multimethod

import pytest


@multimethod
def func(x: int, y: int):
    expr = x + y
    return "base func(x=%r, y=%r): %r" % (x, y, expr)


@func.register
def func_for_str_float(x: str, y: float):
    expr = "%s + %.1f" % (x, y)
    return "str_float func(x=%r, y=%r): %r" % (x, y, expr)


def test_base_func():
    """Test the base `func`."""
    assert func(1, 2) == 'base func(x=1, y=2): 3'
    with pytest.raises(TypeError):
        assert func('1', '2')
    with pytest.raises(TypeError):
        func('1', 2)


def test_multi_func():
    """Test that we can invoke the registered multi-method."""
    assert func('1', 1.34) == "str_float func(x='1', y=1.34): '1 + 1.3'"
    with pytest.raises(TypeError):
        func(1.34, '1')


def test_local_register():
    """Test that we can register and invoke a multi-method locally."""

    @func.register(float, str)
    def func_for_str_float(x, y):  # same name as other registered function
        """Implementation for (str, float)."""
        expr = "%.1f + %s" % (x, y)
        return "float_str func(x=%r, y=%r): %r" % (x, y, expr)

    assert func(1.34, '1') == "float_str func(x=1.34, y='1'): '1.3 + 1'"
    assert len(func) == 3
