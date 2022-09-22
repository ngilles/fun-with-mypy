from __future__ import annotations

from typing import TypedDict, Final, Type, Literal
from mypyfun.typeddict.types import Partial, Required, Omit, Pick

class Foo(TypedDict, total=True):
    a: int
    b: int

class Bar(TypedDict, total=False):
    a: int
    b: int



d11: Foo = {"a": 1, "b": 2}
d12: Foo = {"a": 1}
d13: Foo = {"b": 2}

d21: Bar = {"a": 1, "b": 2}
d22: Bar = {"a": 1}
d23: Bar = {"b": 2}

d31: Partial[Foo] = {"a": 1, "b": 2}
d32: Partial[Foo] = {"a": 1}
d33: Partial[Foo] = {"b": 2}

d41: Required[Bar] = {"a": 1, "b": 2}
d42: Required[Bar] = {"a": 1}
d43: Required[Bar] = {"b": 2}

