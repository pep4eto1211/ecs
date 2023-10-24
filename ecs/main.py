from dataclasses import dataclass
from typing import List
from ecs.engine import Engine

@dataclass
class ToDoComponent:
    title: str = ''
    is_done: bool = False

@dataclass
class DeleteFlagComponent:
    pass

@dataclass
class WelcomeHousekeepingComponent:
    pass

@dataclass
class FinalHousekeepingComponent:
    pass

done_tasks: List[str] = []

def print_pending(engine: Engine, entity_id: int, todo_component: ToDoComponent):
    if not todo_component.is_done:
        print(f'You have to {todo_component.title} today')

def print_welcome(engine: Engine, entity_id: int, _: WelcomeHousekeepingComponent):
    print('This is what you have planned for today and tomorrow:')

def mark_for_deletion(engine: Engine, entity_id: int, todo_component: ToDoComponent):
    if todo_component.is_done:
        engine.add_component(entity_id, DeleteFlagComponent())

def report_preparation(engine: Engine, entity_id: int, delete_flag: DeleteFlagComponent, todo_component: ToDoComponent):
    done_tasks.append(todo_component.title)

def delete_done(engine: Engine, entity_id: int, delete_flag: DeleteFlagComponent):
    engine.delete_entity(entity_id)

def report_done_tasks(engine: Engine, entity_id: int, final_housekeeping: FinalHousekeepingComponent):
    for done_task in done_tasks:
        print(f'{done_task} task has been done')
    done_task = []

def main():
    engine: Engine = Engine()

    # Housekeeping entities
    engine.create_entity([WelcomeHousekeepingComponent()])
    engine.create_entity([FinalHousekeepingComponent()])

    engine.create_entity([ToDoComponent('Buy cheese')])
    engine.create_entity([ToDoComponent('Clean house')])
    engine.create_entity([ToDoComponent('Sleep', True)])
    engine.create_entity([ToDoComponent('Change socks')])

    engine.add_system('Housekeeping', ('WelcomeHousekeepingComponent',), print_welcome)
    engine.add_system('PrintPending', ('ToDoComponent',), print_pending)
    engine.add_system('MarkForDeletion', ('ToDoComponent',), mark_for_deletion)
    engine.add_system('ReportPreparation', ('DeleteFlagComponent','ToDoComponent'), report_preparation)
    #engine.add_system('DeleteCompleted', ('DeleteFlagComponent',), delete_done)
    engine.add_system('ReportDone', ('FinalHousekeepingComponent',), report_done_tasks)

    engine.tick()
