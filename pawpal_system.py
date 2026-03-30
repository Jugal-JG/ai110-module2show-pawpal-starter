from dataclasses import dataclass, field
from typing import List

PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


@dataclass
class Task:
    """Represents a single pet care activity."""
    title: str
    duration_minutes: int
    priority: str          # "low", "medium", "high"
    category: str = ""
    completed: bool = False

    def mark_complete(self):
        """Mark this task as done."""
        self.completed = True

    def is_high_priority(self) -> bool:
        """Return True if this task is high priority."""
        return self.priority == "high"


@dataclass
class Pet:
    """Stores a pet's details and its care tasks."""
    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        """Add a care task to this pet."""
        self.tasks.append(task)

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks assigned to this pet."""
        return self.tasks


@dataclass
class Owner:
    """Manages the pet owner's info and their pets."""
    name: str
    available_time_minutes: int
    preferences: List[str] = field(default_factory=list)
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet):
        """Add a pet to this owner's list."""
        self.pets.append(pet)

    def set_available_time(self, minutes: int):
        """Update how much free time the owner has today."""
        self.available_time_minutes = minutes

    def get_all_tasks(self) -> List[Task]:
        """Gather every task from all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_all_tasks())
        return all_tasks


@dataclass
class Scheduler:
    """The brain — picks and orders tasks that fit the owner's day."""
    owner: Owner

    def sort_by_priority(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks high to low, shortest first within the same priority."""
        return sorted(tasks, key=lambda t: (PRIORITY_ORDER.get(t.priority, 99), t.duration_minutes))

    def generate_plan(self) -> List[Task]:
        """Return tasks that fit within the owner's available time."""
        all_tasks = self.owner.get_all_tasks()
        sorted_tasks = self.sort_by_priority(all_tasks)
        plan = []
        time_used = 0
        for task in sorted_tasks:
            if time_used + task.duration_minutes <= self.owner.available_time_minutes:
                plan.append(task)
                time_used += task.duration_minutes
        return plan

    def explain_plan(self, plan: List[Task]) -> str:
        """Return a readable summary of the scheduled tasks."""
        if not plan:
            return "No tasks fit in the available time today."
        lines = ["Today's Schedule", "-" * 32]
        time_used = 0
        for task in plan:
            time_used += task.duration_minutes
            lines.append(f"  [{task.priority.upper():6}] {task.title} — {task.duration_minutes} min")
        lines.append("-" * 32)
        lines.append(f"Total: {time_used} / {self.owner.available_time_minutes} min available")
        return "\n".join(lines)
