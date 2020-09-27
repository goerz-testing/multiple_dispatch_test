"""Set up the environment for doctests

This file is automatically evaluated by py.test. It ensures that we can write
doctests without distracting import statements in the doctest.
"""
import pytest

import multiple_dispatch


@pytest.fixture(autouse=True)
def set_doctest_env(doctest_namespace):
    doctest_namespace['multiple_dispatch'] = multiple_dispatch
