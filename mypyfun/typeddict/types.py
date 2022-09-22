
from types import GenericAlias
from queue import Queue

from typing import TypeVar

T = TypeVar('T')

# There are just place holders, the magic is done by mypy and plugin

class Partial(Generic[T]):
    ...

class Required(Generic[T]):
    ...

class Omit(Generic[T]):
    ...

class Pick(Generic[T]):
    ...
