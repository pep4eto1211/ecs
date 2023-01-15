from typing import Any, Dict, List


class Entity:
    def __init__(self, id: int) -> None:
        self._id: int = id
        self._components: Dict[str, Any] = {}

@property
def id(self) -> int:
    return self._id