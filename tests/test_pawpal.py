from pawpal_system import Task, Pet


def test_task_completion():
    # Create a task
    task = Task(
        task_id=1,
        title="Feed Pet",
        description="Give food",
        duration=10,
        priority=3,
        frequency="daily",
        task_type="feeding"
    )

    # Initially should not be completed
    assert task.completed is False

    # Mark complete
    task.mark_complete()

    # Now should be completed
    assert task.completed is True


def test_add_task_to_pet():
    # Create a pet
    pet = Pet(pet_id=1, name="Bella", species="Dog", age=4)

    # Initially no tasks
    assert len(pet.tasks) == 0

    # Create task
    task = Task(
        task_id=1,
        title="Walk",
        description="Go outside",
        duration=20,
        priority=4,
        frequency="daily",
        task_type="walk"
    )

    # Add task
    pet.add_task(task)

    # Now pet should have 1 task
    assert len(pet.tasks) == 1