"""Tests for `multiple_dispatch` package."""

import pytest
from pkg_resources import parse_version

import multiple_dispatch


def test_valid_version():
    """Check that the package defines a valid ``__version__``."""
    v_curr = parse_version(multiple_dispatch.__version__)
    v_orig = parse_version("0.1.0-dev")
    assert v_curr >= v_orig
