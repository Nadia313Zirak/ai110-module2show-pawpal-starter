from dataclasses import dataclass, field
from typing import List, Optional
from datetime import date, timedelta


@dataclass
class Task:
    """Dataclass representing a pet care task."""
    task_id: int
    title: str
    description: str
    time: str
    due_date: date
    duration: int
    priority: int
    frequency: str
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
    available_time: int
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
        """Initialize scheduler with owner's tasks and available time."""
        self.owner = owner
        self.available_time = owner.available_time

    def get_all_tasks(self) -> List[Task]:
        """Retrieve all tasks from the owner."""
        return self.owner.get_all_tasks()

    def sort_tasks(self) -> List[Task]:
        """Sort incomplete tasks by priority and duration."""
        tasks = [task for task in self.get_all_tasks() if not task.completed]
        return sorted(tasks, key=lambda t: (-t.priority, t.duration))

    def sort_by_time(self) -> List[Task]:
        """Sort incomplete tasks by due date and time."""
        tasks = [task for task in self.get_all_tasks() if not task.completed]
        return sorted(tasks, key=lambda task: (task.due_date, task.time))

    def filter_tasks(
        self,
        completed: Optional[bool] = None,
        pet_name: Optional[str] = None
    ) -> List[Task]:
        """Filter tasks by completion status and/or pet name."""
        filtered_tasks = []

        for pet in self.owner.pets:
            if pet_name is not None and pet.name.lower() != pet_name.lower():
                continue

            for task in pet.tasks:
                if completed is None or task.completed == completed:
                    filtered_tasks.append(task)

        return filtered_tasks

    def complete_task(self, task_id: int, pet_name: str) -> bool:
        """Mark a task complete and create the next recurring task if needed."""
        pet = next((p for p in self.owner.pets if p.name.lower() == pet_name.lower()), None)
        if pet is None:
            return False

        task = next((t for t in pet.tasks if t.task_id == task_id), None)
        if task is None or task.completed:
            return False

        task.mark_complete()

        if task.frequency.lower() == "daily":
            next_due_date = task.due_date + timedelta(days=1)
        elif task.frequency.lower() == "weekly":
            next_due_date = task.due_date + timedelta(days=7)
        else:
            return True

        next_task_id = max((t.task_id for t in self.owner.get_all_tasks()), default=0) + 1

        new_task = Task(
            task_id=next_task_id,
            title=task.title,
            description=task.description,
            time=task.time,
            due_date=next_due_date,
            duration=task.duration,
            priority=task.priority,
            frequency=task.frequency,
            task_type=task.task_type,
            completed=False
        )

        pet.add_task(new_task)
        return True

    def detect_conflicts(self) -> List[str]:
        """Detect tasks that share the same date and time and return warning messages."""
        warnings = []
        scheduled_items = []

        for pet in self.owner.pets:
            for task in pet.tasks:
                if not task.completed:
                    scheduled_items.append((pet.name, task))

        scheduled_items.sort(key=lambda item: (item[1].due_date, item[1].time))

        for i in range(len(scheduled_items)):
            pet1, task1 = scheduled_items[i]
            for j in range(i + 1, len(scheduled_items)):
                pet2, task2 = scheduled_items[j]

                if task1.due_date == task2.due_date and task1.time == task2.time:
                    warnings.append(
                        f"Warning: Conflict detected on {task1.due_date} at {task1.time} "
                        f"between '{task1.title}' for {pet1} and '{task2.title}' for {pet2}."
                    )

        return warnings

    def generate_daily_plan(self) -> List[Task]:
        """Generate a daily plan for tasks due today within available time."""
        today = date.today()
        tasks_due_today = [
            task for task in self.get_all_tasks()
            if not task.completed and task.due_date <= today
        ]
        sorted_tasks = sorted(tasks_due_today, key=lambda t: (-t.priority, t.time))

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
                f"{idx}. {task.title} on {task.due_date} at {task.time} "
                f"({task.duration} min) - Priority: {task.priority}\n"
            )
            total_time += task.duration

        explanation += (
            f"\nTotal time needed: {total_time} minutes out of "
            f"{self.available_time} available."
        )
        return explanation