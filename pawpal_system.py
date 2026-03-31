from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Owner:
    owner_id: int
    name: str
    available_time: int
    preferences: str

    def update_preferences(self, new_preferences: str) -> None:
        pass


@dataclass
class Pet:
    pet_id: int
    name: str
    species: str
    age: int

    def get_pet_info(self) -> str:
        pass


@dataclass
class Task:
    task_id: int
    title: str
    duration: int
    priority: int
    task_type: str
    completed: bool = False

    def mark_complete(self) -> None:
        pass


class Scheduler:
    def __init__(self, tasks: Optional[List[Task]] = None, available_time: int = 0) -> None:
        self.tasks = tasks if tasks is not None else []
        self.available_time = available_time

    def generate_daily_plan(self) -> List[Task]:
        pass

    def sort_tasks(self) -> List[Task]:
        pass

    def explain_plan(self) -> str:
        pass


class PawPalSystem:
    def __init__(
        self,
        owner: Optional[Owner] = None,
        pet: Optional[Pet] = None,
        tasks: Optional[List[Task]] = None,
        scheduler: Optional[Scheduler] = None
    ) -> None:
        self.owner = owner
        self.pet = pet
        self.tasks = tasks if tasks is not None else []
        self.scheduler = scheduler

    def add_pet(self, pet: Pet) -> None:
        pass

    def add_task(self, task: Task) -> None:
        pass

    def edit_task(self, task_id: int, **kwargs) -> None:
        pass

    def get_daily_plan(self) -> List[Task]:
        pass