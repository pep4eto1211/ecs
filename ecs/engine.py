from typing import Any, Callable, Dict, Iterable, List, Set, Tuple

from ecs.entity import Entity
from ecs.system import _System


class Engine:
    def __init__(self) -> None:
        self.__latest_id: int = 0
        self._entities: Dict[int, Entity] = {}
        self._systems: List[_System] = []
        self.__selectors_map: Dict[Tuple, Set[str]] = {}

    def create_entity(self) -> Entity:
        return self.__create_new_entity()

    def create_entity(self, component: Any) -> Entity:
        new_entity: Entity = self.__create_new_entity()
        self.__add_component_to_entity(new_entity, component)
        return new_entity

    def create_entity(self, components: List[Any]) -> Entity:
        new_entity: Entity = self.__create_new_entity()
        for component in components:
            self.__add_component_to_entity(new_entity, component)
        return new_entity

    def delete_entity(self, entity_id: int):
        del self._entities[entity_id]

    def add_component(self, entity: Entity, component: Any):
        self.__add_component_to_entity(entity, component)

    def add_component(self, entity_id: int, component: Any):
        self.__add_component_to_entity(self._entities[entity_id], component)

    def remove_component(self, entity: Entity, component_name: str):
        del entity._components[component_name]

    def remove_component(self, entity_id: int, component_name: str):
        del self._entities[entity_id]._components[component_name]

    def add_system(self, name: str, components_selector: Tuple[str, ...], process: Callable):
        self.__create_new_system(name, components_selector, process)

    def tick(self):
        for system in self._systems:
            #TODO: This can be done in parallel
            for entity in self.__get_entities_for_selector(system._selector):
                system._process(self, entity[0], *entity[1])

    def __get_entities_for_selector(self, components_selector: Tuple[str, ...]) -> Iterable[Tuple[int, List[Any]]]:
        for key, value in self._entities.items():
            if self.__selectors_map[components_selector] <= set(value._components.keys()):
                yield(key, [value._components[x] for x in components_selector])

    def __create_new_system(self, name: str, components_selector: Tuple[str, ...], process: Callable) -> _System:
        new_system: _System = _System(name, components_selector, process)
        self._systems.append(new_system)
        self.__selectors_map[components_selector] = set(components_selector)
        return new_system

    def __add_component_to_entity(self, entity: Entity, component: Any):
        entity._components[type(component).__name__] = component

    def __create_new_entity(self) -> Entity:
        new_entity: Entity = Entity(self.__latest_id)
        self._entities[self.__latest_id] = new_entity
        self.__latest_id += 1
        return new_entity