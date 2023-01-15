from typing import Callable, Tuple


class _System:
    def __init__(self, name: str, selector: Tuple, process: Callable) -> None:
        self._name: str = name
        self._selector: Tuple[str, ...] = selector
        self._process: Callable = process