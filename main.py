from datetime import date
from pawpal_system import Owner, Pet, Task, Scheduler


def print_task_list(title, tasks):
    print(f"\n=== {title} ===")
    if not tasks:
        print("No tasks found.")
        return

    for task in tasks:
        status = "Done" if task.completed else "Pending"
        print(
            f"{task.title} | Date: {task.due_date} | Time: {task.time} | "
            f"Duration: {task.duration} min | Priority: {task.priority} | Status: {status}"
        )


def main():
    owner = Owner(
        owner_id=1,
        name="Nadia",
        available_time=180,
        preferences="Morning routine"
    )

    dog = Pet(pet_id=1, name="Bella", species="Dog", age=4)
    cat = Pet(pet_id=2, name="Luna", species="Cat", age=2)

    owner.add_pet(dog)
    owner.add_pet(cat)

    # Two tasks at the same time to test conflicts
    task1 = Task(
        task_id=1,
        title="Morning Walk",
        description="Walk Bella outside",
        time="08:00",
        due_date=date.today(),
        duration=30,
        priority=5,
        frequency="daily",
        task_type="walk"
    )

    task2 = Task(
        task_id=2,
        title="Breakfast Feeding",
        description="Feed Luna breakfast",
        time="08:00",
        due_date=date.today(),
        duration=10,
        priority=4,
        frequency="once",
        task_type="feeding"
    )

    task3 = Task(
        task_id=3,
        title="Medication",
        description="Give Bella medicine",
        time="07:30",
        due_date=date.today(),
        duration=5,
        priority=5,
        frequency="weekly",
        task_type="medication"
    )

    task4 = Task(
        task_id=4,
        title="Play Time",
        description="Play with Luna",
        time="15:00",
        due_date=date.today(),
        duration=20,
        priority=2,
        frequency="daily",
        task_type="enrichment"
    )

    dog.add_task(task1)
    dog.add_task(task3)
    cat.add_task(task2)
    cat.add_task(task4)

    scheduler = Scheduler(owner)

    print_task_list("All Tasks Sorted by Time", scheduler.sort_by_time())

    print("\n=== Conflict Warnings ===")
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        for warning in conflicts:
            print(warning)
    else:
        print("No conflicts detected.")

    print("\n=== Today's Schedule ===")
    today_plan = scheduler.generate_daily_plan()
    if today_plan:
        for i, task in enumerate(today_plan, 1):
            print(
                f"{i}. {task.title} | Date: {task.due_date} | Time: {task.time} | "
                f"Priority: {task.priority}"
            )
    else:
        print("No tasks scheduled for today.")


if __name__ == "__main__":
    main()