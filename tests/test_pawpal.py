from datetime import date, timedelta
from pawpal_system import Owner, Pet, Task, Scheduler


def test_task_completion():
    task = Task(
        task_id=1,
        title="Feed Pet",
        description="Give food",
        time="08:00",
        due_date=date.today(),
        duration=10,
        priority=3,
        frequency="once",
        task_type="feeding"
    )

    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_to_pet():
    pet = Pet(pet_id=1, name="Bella", species="Dog", age=4)

    assert len(pet.tasks) == 0

    task = Task(
        task_id=1,
        title="Walk",
        description="Go outside",
        time="09:00",
        due_date=date.today(),
        duration=20,
        priority=4,
        frequency="daily",
        task_type="walk"
    )

    pet.add_task(task)

    assert len(pet.tasks) == 1


def test_sort_by_time_orders_tasks_correctly():
    owner = Owner(
        owner_id=1,
        name="Nadia",
        available_time=180,
        preferences="Morning"
    )

    pet = Pet(pet_id=1, name="Bella", species="Dog", age=4)
    owner.add_pet(pet)

    task1 = Task(
        task_id=1,
        title="Evening Walk",
        description="Walk Bella",
        time="18:00",
        due_date=date.today(),
        duration=30,
        priority=5,
        frequency="daily",
        task_type="walk"
    )

    task2 = Task(
        task_id=2,
        title="Breakfast",
        description="Feed Bella",
        time="08:00",
        due_date=date.today(),
        duration=10,
        priority=4,
        frequency="daily",
        task_type="feeding"
    )

    task3 = Task(
        task_id=3,
        title="Medication",
        description="Give medicine",
        time="07:30",
        due_date=date.today(),
        duration=5,
        priority=5,
        frequency="daily",
        task_type="medication"
    )

    pet.add_task(task1)
    pet.add_task(task2)
    pet.add_task(task3)

    scheduler = Scheduler(owner)
    sorted_tasks = scheduler.sort_by_time()

    assert [task.title for task in sorted_tasks] == [
        "Medication",
        "Breakfast",
        "Evening Walk"
    ]


def test_daily_task_completion_creates_next_day_task():
    owner = Owner(
        owner_id=1,
        name="Nadia",
        available_time=180,
        preferences="Morning"
    )

    pet = Pet(pet_id=1, name="Bella", species="Dog", age=4)
    owner.add_pet(pet)

    original_task = Task(
        task_id=1,
        title="Morning Walk",
        description="Walk Bella",
        time="08:00",
        due_date=date.today(),
        duration=20,
        priority=5,
        frequency="daily",
        task_type="walk"
    )

    pet.add_task(original_task)

    scheduler = Scheduler(owner)
    result = scheduler.complete_task(task_id=1, pet_name="Bella")

    assert result is True
    assert original_task.completed is True
    assert len(pet.tasks) == 2

    new_task = pet.tasks[1]
    assert new_task.title == original_task.title
    assert new_task.completed is False
    assert new_task.due_date == date.today() + timedelta(days=1)


def test_conflict_detection_flags_duplicate_times():
    owner = Owner(
        owner_id=1,
        name="Nadia",
        available_time=180,
        preferences="Morning"
    )

    dog = Pet(pet_id=1, name="Bella", species="Dog", age=4)
    cat = Pet(pet_id=2, name="Luna", species="Cat", age=2)

    owner.add_pet(dog)
    owner.add_pet(cat)

    task1 = Task(
        task_id=1,
        title="Morning Walk",
        description="Walk Bella",
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
        description="Feed Luna",
        time="08:00",
        due_date=date.today(),
        duration=10,
        priority=4,
        frequency="once",
        task_type="feeding"
    )

    dog.add_task(task1)
    cat.add_task(task2)

    scheduler = Scheduler(owner)
    warnings = scheduler.detect_conflicts()

    assert len(warnings) == 1
    assert "Conflict detected" in warnings[0]
    assert "Morning Walk" in warnings[0]
    assert "Breakfast Feeding" in warnings[0]