from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str          # "low", "medium", "high"
    category: str = ""     # e.g. "walk", "feeding", "meds", "grooming"
    completed: bool = False

    def mark_complete(self):
        pass

    def is_high_priority(self) -> bool:
        pass


@dataclass
class Pet:
    name: str
    species: str           # "dog", "cat", "other"
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        pass

    def get_all_tasks(self) -> List[Task]:
        pass


@dataclass
class Owner:
    name: str
    available_time_minutes: int
    preferences: List[str] = field(default_factory=list)
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet):
        pass

    def set_available_time(self, minutes: int):
        pass


@dataclass
class Scheduler:
    owner: Owner
    pet: Pet
    time_budget: int = 0   # filled from owner.available_time_minutes

    def generate_plan(self) -> List[Task]:
        pass

    def explain_plan(self, plan: List[Task]) -> str:
        pass

    def sort_by_priority(self, tasks: List[Task]) -> List[Task]:
        pass
