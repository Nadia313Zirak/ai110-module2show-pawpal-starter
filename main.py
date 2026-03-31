from pawpal_system import Owner, Pet, Task, Scheduler


def main():
    # Create Owner
    owner = Owner(owner_id=1, name="Nadia", available_time=120, preferences="Morning routine")

    # Create Pets
    dog = Pet(pet_id=1, name="Bella", species="Dog", age=4)
    cat = Pet(pet_id=2, name="Luna", species="Cat", age=2)

    # Add pets to owner
    owner.add_pet(dog)
    owner.add_pet(cat)

    # Create Tasks (different times simulated via priority + duration)
    task1 = Task(
        task_id=1,
        title="Morning Walk",
        description="Walk Bella around the park",
        duration=30,
        priority=5,
        frequency="daily",
        task_type="walk"
    )

    task2 = Task(
        task_id=2,
        title="Feed Luna",
        description="Give Luna breakfast",
        duration=10,
        priority=4,
        frequency="daily",
        task_type="feeding"
    )

    task3 = Task(
        task_id=3,
        title="Play Time",
        description="Play with Bella",
        duration=20,
        priority=3,
        frequency="daily",
        task_type="enrichment"
    )

    # Assign tasks to pets
    dog.add_task(task1)
    dog.add_task(task3)
    cat.add_task(task2)

    # Create Scheduler
    scheduler = Scheduler(owner)

    # Generate plan
    daily_plan = scheduler.generate_daily_plan()

    # Print schedule
    print("\n=== Today's Schedule ===\n")

    if not daily_plan:
        print("No tasks scheduled.")
    else:
        for i, task in enumerate(daily_plan, 1):
            print(f"{i}. {task.title}")
            print(f"   Description: {task.description}")
            print(f"   Duration: {task.duration} minutes")
            print(f"   Priority: {task.priority}")
            print(f"   Type: {task.task_type}")
            print()


if __name__ == "__main__":
    main()