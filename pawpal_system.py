from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    """Dataclass representing a pet care task."""
    task_id: int
    title: str
    description: str
    duration: int  # in minutes
    priority: int  # 1-5, where 5 is highest
    frequency: str  # e.g., "daily", "weekly", "once"
    task_type: str
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark the task as completed."""
        self.completed = True


@dataclass
class Pet:
    """Dataclass representing a pet."""
    pet_id: int
    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a new task to the pet's task list."""
        self.tasks.append(task)

    def edit_task(self, task_id: int, **kwargs) -> bool:
        """Edit an existing task by task_id."""
        for task in self.tasks:
            if task.task_id == task_id:
                for key, value in kwargs.items():
                    if hasattr(task, key):
                        setattr(task, key, value)
                return True
        return False

    def get_pending_tasks(self) -> List[Task]:
        """Return a list of incomplete tasks for this pet."""
        return [task for task in self.tasks if not task.completed]

    def get_pet_info(self) -> str:
        """Return information about the pet."""
        return f"{self.name} ({self.species}), Age: {self.age}"


@dataclass
class Owner:
    """Dataclass representing a pet owner."""
    owner_id: int
    name: str
    available_time: int  # in minutes per day
    preferences: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's pet list."""
        self.pets.append(pet)

    def get_all_tasks(self) -> List[Task]:
        """Retrieve all tasks from all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks

    def update_preferences(self, new_preferences: str) -> None:
        """Update the owner's preferences."""
        self.preferences = new_preferences


class Scheduler:
    """Class responsible for scheduling pet care tasks."""

    def __init__(self, owner: Owner) -> None:
        self.owner = owner
        self.available_time = owner.available_time

    def get_all_tasks(self) -> List[Task]:
        """Retrieve all tasks from the owner."""
        return self.owner.get_all_tasks()

    def sort_tasks(self) -> List[Task]:
        """Sort incomplete tasks by priority (highest first) and then by duration."""
        tasks = [task for task in self.get_all_tasks() if not task.completed]
        return sorted(tasks, key=lambda t: (-t.priority, t.duration))

    def generate_daily_plan(self) -> List[Task]:
        """Generate an organized daily plan based on available time and task priorities."""
        sorted_tasks = self.sort_tasks()
        daily_plan = []
        total_duration = 0

        for task in sorted_tasks:
            if total_duration + task.duration <= self.available_time:
                daily_plan.append(task)
                total_duration += task.duration

        return daily_plan

    def explain_plan(self) -> str:
        """Generate a human-readable explanation of the daily plan."""
        daily_plan = self.generate_daily_plan()

        if not daily_plan:
            return "No tasks scheduled for today."

        explanation = "Today's Pet Care Plan:\n"
        total_time = 0

        for idx, task in enumerate(daily_plan, 1):
            explanation += (
                f"{idx}. {task.title} ({task.duration} min) - Priority: {task.priority}\n"
            )
            total_time += task.duration

        explanation += (
            f"\nTotal time needed: {total_time} minutes out of "
            f"{self.available_time} available."
        )
        return explanation