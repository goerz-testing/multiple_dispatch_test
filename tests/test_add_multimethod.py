"""Test functionality of add.multimethod submodule."""
from multiple_dispatch.add.multimethod import addprint


def test_addprint():
    """Test correctness of addprint multimethod."""
    assert addprint(1, 2) == 'base addprint(x=1, y=2): 3'
    assert (
        addprint('1', 1.34) == "str_float addprint(x='1', y=1.34): '1 + 1.3'"
    )
    assert (
        addprint(1.34, '1') == "float_str addprint(x=1.34, y='1'): '1.3 + 1'"
    )
