"""A class hierarchy to test multiple dispatch on parent-classes.

::

          ┌─┐                           ┌─┐
          │A│                           │B│
          └┬┘                           └┬┘
           │                             │
       ┌───┴──┬────────────┬─────────────┤
       │      │            │             │
     ┌─▼─┐  ┌─▼─┐      ┌───▼───┐       ┌─▼─┐
     │A_1│  │A_2│      │ AB_1  │       │B_1│
     └─┬─┘  └───┘      └───┬───┘       └─┬─┘
       │                   │             │
    ┌──▼──┐            ┌───▼───┐      ┌──▼──┐
    │A_1_1│            │AB_1_1 │      │B_1_1│
    └─────┘            └───────┘      └─────┘

"""


class A:
    """Wrapper class around a value."""

    def __init__(self, val):
        self.val = val


class B:
    """Dummy class."""


class A_1(A):
    """Subclass of :class:`A`."""


class A_2(A):
    """Subclass of :class:`A`."""


class A_1_1(A_1):
    """Subclass of :class:`A_1`."""


class B_1(B):
    """Subclass of :class:`B`."""


class B_1_1(B_1):
    """Subclass of :class:`B_1`."""


class AB_1(A, B):
    """Subclass of both :class:`A` and :class:`B`."""


class AB_1_1(AB_1):
    """Subclass of :class:`AB_1`."""
