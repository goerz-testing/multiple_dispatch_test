import functools
import inspect
import types
from typing import Callable

from multimethod import (
    signature,
    subtype,
    get_type,
    groupby,
    DispatchError,
    get_types,
    overload,
    multimethod,
)


class multiple_dispatch(multimethod):
    """A callable directed acyclic graph of methods."""

    pending = None  # type: set

    def __new__(cls, func):
        namespace = inspect.currentframe().f_back.f_locals
        self = functools.update_wrapper(dict.__new__(cls), func)
        self.pending = set()
        self.get_type = type  # default type checker
        return namespace.get(func.__name__, self)

    def __init__(self, func: Callable):
        try:
            self[get_types(func)] = func
        except NameError:
            self.pending.add(func)

    def register(self, *args):
        """Decorator for registering a function.

        Optionally call with types to return a decorator for unannotated
        functions.
        """
        if len(args) == 1 and hasattr(args[0], '__annotations__'):
            return overload.register(self, *args)
        return lambda func: self.__setitem__(args, func) or func

    def __get__(self, instance, owner):
        return self if instance is None else types.MethodType(self, instance)

    def parents(self, types: tuple) -> set:
        """Find immediate parents of potential key."""
        parents = {
            key for key in self if isinstance(key, signature) and key < types
        }
        return parents - {
            ancestor for parent in parents for ancestor in parent.parents
        }

    def clean(self):
        """Empty the cache."""
        for key in list(self):
            if not isinstance(key, signature):
                super().__delitem__(key)

    def __setitem__(self, types: tuple, func: Callable):
        self.clean()
        types = signature(types)
        parents = types.parents = self.parents(types)
        for key in self:
            if types < key and (not parents or parents & key.parents):
                key.parents -= parents
                key.parents.add(types)
        if any(map(subtype.subcheck, types)):
            self.get_type = get_type  # switch to slower generic type checker
        super().__setitem__(types, func)
        self.__doc__ = self.docstring

    def __delitem__(self, types: tuple):
        self.clean()
        super().__delitem__(types)
        for key in self:
            if types in key.parents:
                key.parents = self.parents(key)
        self.__doc__ = self.docstring

    def __missing__(self, types: tuple) -> Callable:
        """Find and cache the next applicable method of given types."""
        self.evaluate()
        if types in self:
            return self[types]
        groups = groupby(signature(types).__sub__, self.parents(types))
        keys = groups[min(groups)] if groups else []
        funcs = {self[key] for key in keys}
        if len(funcs) == 1:
            return self.setdefault(types, *funcs)
        msg = f"{self.__name__}: {len(keys)} methods found"  # type: ignore
        raise DispatchError(msg, types, keys)

    def __call__(self, *args, **kwargs):
        """Resolve and dispatch to best method."""
        return self[tuple(map(self.get_type, args))](*args, **kwargs)

    def evaluate(self):
        """Evaluate any pending forward references.

        This can be called explicitly when using forward references,
        otherwise cache misses will evaluate.
        """
        while self.pending:
            func = self.pending.pop()
            self[get_types(func)] = func

    @property
    def docstring(self):
        """A descriptive docstring of all registered functions."""
        docs = []
        for func in set(self.values()):
            try:
                sig = inspect.signature(func)
            except ValueError:
                sig = ''
            doc = func.__doc__ or ''
            docs.append(f'{func.__name__}{sig}\n    {doc}')
        return '\n\n'.join(docs)
