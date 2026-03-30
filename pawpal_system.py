from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import List, Optional

PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


@dataclass
class Task:
    """Represents a single pet care activity."""
    title: str
    duration_minutes: int
    priority: str            # "low", "medium", "high"
    category: str = ""
    completed: bool = False
    start_time: str = ""     # "HH:MM" format, empty means unscheduled
    frequency: str = "once"  # "once", "daily", "weekly"
    due_date: str = ""       # ISO format YYYY-MM-DD

    def mark_complete(self) -> Optional["Task"]:
        """Mark this task done. Returns the next occurrence if it's a recurring task."""
        self.completed = True
        if self.frequency == "daily":
            next_date = date.today() + timedelta(days=1)
            return Task(
                title=self.title,
                duration_minutes=self.duration_minutes,
                priority=self.priority,
                category=self.category,
                start_time=self.start_time,
                frequency=self.frequency,
                due_date=str(next_date),
            )
        if self.frequency == "weekly":
            next_date = date.today() + timedelta(weeks=1)
            return Task(
                title=self.title,
                duration_minutes=self.duration_minutes,
                priority=self.priority,
                category=self.category,
                start_time=self.start_time,
                frequency=self.frequency,
                due_date=str(next_date),
            )
        return None

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
    """The brain — picks, sorts, filters, and validates tasks for the owner's day."""
    owner: Owner

    def sort_by_priority(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks high to low, shortest first within the same priority."""
        return sorted(tasks, key=lambda t: (PRIORITY_ORDER.get(t.priority, 99), t.duration_minutes))

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by start_time in HH:MM format. Unscheduled tasks go to the end."""
        return sorted(tasks, key=lambda t: t.start_time if t.start_time else "99:99")

    def filter_tasks(self, tasks: List[Task], pet_name: str = "", only_incomplete: bool = False) -> List[Task]:
        """Filter tasks by pet name and/or completion status."""
        result = tasks
        if pet_name:
            pet = next((p for p in self.owner.pets if p.name == pet_name), None)
            result = pet.get_all_tasks() if pet else []
        if only_incomplete:
            result = [t for t in result if not t.completed]
        return result

    def detect_conflicts(self, plan: List[Task]) -> List[str]:
        """Return warning messages for any two tasks sharing the same start_time."""
        warnings = []
        seen = {}
        for task in plan:
            if not task.start_time:
                continue
            if task.start_time in seen:
                warnings.append(
                    f"Conflict at {task.start_time}: '{seen[task.start_time]}' and '{task.title}' overlap."
                )
            else:
                seen[task.start_time] = task.title
        return warnings

    def generate_plan(self) -> List[Task]:
        """Return tasks that fit within the owner's available time, sorted by priority."""
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
        lines = ["Today's Schedule", "-" * 36]
        time_used = 0
        for task in plan:
            time_used += task.duration_minutes
            time_tag = f" @ {task.start_time}" if task.start_time else ""
            freq_tag = f" [{task.frequency}]" if task.frequency != "once" else ""
            lines.append(f"  [{task.priority.upper():6}] {task.title}{time_tag}{freq_tag} — {task.duration_minutes} min")
        lines.append("-" * 36)
        lines.append(f"Total: {time_used} / {self.owner.available_time_minutes} min available")
        return "\n".join(lines)
