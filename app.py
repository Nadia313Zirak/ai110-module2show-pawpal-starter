import streamlit as st
from datetime import date
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

# Session state setup
if "owner" not in st.session_state:
    st.session_state.owner = Owner(
        owner_id=1,
        name="",
        available_time=120,
        preferences=""
    )

if "next_pet_id" not in st.session_state:
    st.session_state.next_pet_id = 1

if "next_task_id" not in st.session_state:
    st.session_state.next_task_id = 1

owner = st.session_state.owner
scheduler = Scheduler(owner)

st.markdown(
    """
Welcome to the PawPal+ app.

This app helps a pet owner manage pets, add care tasks, and generate a daily schedule
based on available time, task priority, recurrence, and conflict warnings.
"""
)

with st.expander("Scenario", expanded=False):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.
"""
    )

# Owner information
st.subheader("Owner Information")

owner.name = st.text_input("Owner name", value=owner.name)
owner.available_time = st.number_input(
    "Available time per day (minutes)",
    min_value=1,
    max_value=600,
    value=owner.available_time
)
owner.preferences = st.text_input("Owner preferences", value=owner.preferences)

st.divider()

# Add pet
st.subheader("Add a Pet")

pet_name = st.text_input("Pet name")
species = st.selectbox("Species", ["dog", "cat", "other"])
pet_age = st.number_input("Pet age", min_value=0, max_value=50, value=1)

if st.button("Add pet"):
    if pet_name.strip():
        new_pet = Pet(
            pet_id=st.session_state.next_pet_id,
            name=pet_name,
            species=species,
            age=int(pet_age)
        )
        owner.add_pet(new_pet)
        st.session_state.next_pet_id += 1
        st.success(f"{new_pet.name} was added successfully.")
    else:
        st.error("Please enter a pet name.")

if owner.pets:
    st.write("### Current Pets")
    pet_rows = [
        {"Pet ID": pet.pet_id, "Name": pet.name, "Species": pet.species, "Age": pet.age}
        for pet in owner.pets
    ]
    st.table(pet_rows)
else:
    st.info("No pets added yet.")

st.divider()

# Add task
st.subheader("Add a Task")

if owner.pets:
    selected_pet_name = st.selectbox("Select pet", [pet.name for pet in owner.pets])

    task_title = st.text_input("Task title", value="Morning walk")
    task_description = st.text_input("Task description", value="Take pet outside")
    task_time = st.text_input("Task time (HH:MM)", value="08:00")
    task_due_date = st.date_input("Due date", value=date.today())
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    priority_label = st.selectbox("Priority", ["low", "medium", "high"], index=2)
    frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])
    task_type = st.selectbox(
        "Task type",
        ["walk", "feeding", "medication", "grooming", "enrichment"]
    )

    priority_map = {"low": 1, "medium": 3, "high": 5}
    priority = priority_map[priority_label]

    if st.button("Add task"):
        selected_pet = next((pet for pet in owner.pets if pet.name == selected_pet_name), None)

        if selected_pet:
            new_task = Task(
                task_id=st.session_state.next_task_id,
                title=task_title,
                description=task_description,
                time=task_time,
                due_date=task_due_date,
                duration=int(duration),
                priority=priority,
                frequency=frequency,
                task_type=task_type
            )
            selected_pet.add_task(new_task)
            st.session_state.next_task_id += 1
            st.success(f"Task '{new_task.title}' added to {selected_pet.name}.")
else:
    st.info("Add a pet first before creating tasks.")

st.divider()

# Filter tasks
st.subheader("View and Filter Tasks")

filter_pet = st.selectbox(
    "Filter by pet",
    ["All Pets"] + [pet.name for pet in owner.pets]
)

filter_status = st.selectbox(
    "Filter by status",
    ["All", "Pending", "Completed"]
)

selected_completed = None
if filter_status == "Pending":
    selected_completed = False
elif filter_status == "Completed":
    selected_completed = True

selected_pet_name = None if filter_pet == "All Pets" else filter_pet

filtered_tasks = scheduler.filter_tasks(
    completed=selected_completed,
    pet_name=selected_pet_name
)

if filtered_tasks:
    task_rows = []
    for pet in owner.pets:
        for task in pet.tasks:
            if task in filtered_tasks:
                task_rows.append({
                    "Pet": pet.name,
                    "Task": task.title,
                    "Date": task.due_date,
                    "Time": task.time,
                    "Type": task.task_type,
                    "Duration": task.duration,
                    "Priority": task.priority,
                    "Frequency": task.frequency,
                    "Status": "Done" if task.completed else "Pending"
                })
    st.table(task_rows)
else:
    st.info("No tasks match the current filters.")

st.divider()

# Show sorted tasks
st.subheader("Tasks Sorted by Date and Time")

sorted_tasks = scheduler.sort_by_time()

if sorted_tasks:
    sorted_rows = []
    for pet in owner.pets:
        for task in pet.tasks:
            if task in sorted_tasks:
                sorted_rows.append({
                    "Pet": pet.name,
                    "Task": task.title,
                    "Date": task.due_date,
                    "Time": task.time,
                    "Priority": task.priority,
                    "Status": "Done" if task.completed else "Pending"
                })
    st.table(sorted_rows)
else:
    st.info("No pending tasks to sort.")

st.divider()

# Conflict warnings
st.subheader("Conflict Warnings")

conflicts = scheduler.detect_conflicts()
if conflicts:
    for warning in conflicts:
        st.warning(warning)
else:
    st.success("No task conflicts detected.")

st.divider()

# Complete task
st.subheader("Complete a Task")

all_task_options = []
for pet in owner.pets:
    for task in pet.tasks:
        if not task.completed:
            all_task_options.append((pet.name, task.task_id, task.title, task.due_date, task.time))

if all_task_options:
    task_labels = [
        f"{pet_name} - {title} ({due_date} {time}) [ID: {task_id}]"
        for pet_name, task_id, title, due_date, time in all_task_options
    ]

    selected_task_label = st.selectbox("Choose a task to complete", task_labels)

    if st.button("Mark selected task complete"):
        selected_index = task_labels.index(selected_task_label)
        pet_name, task_id, _, _, _ = all_task_options[selected_index]

        success = scheduler.complete_task(task_id=task_id, pet_name=pet_name)

        if success:
            st.success("Task completed. Recurring task created if applicable.")
        else:
            st.error("Task could not be completed.")
else:
    st.info("No incomplete tasks available.")

st.divider()

# Generate schedule
st.subheader("Build Schedule")

if st.button("Generate schedule"):
    daily_plan = scheduler.generate_daily_plan()

    if daily_plan:
        st.success("Schedule generated successfully.")

        schedule_rows = []
        for task in daily_plan:
            pet_name = "Unknown"
            for pet in owner.pets:
                if task in pet.tasks:
                    pet_name = pet.name
                    break

            schedule_rows.append({
                "Pet": pet_name,
                "Task": task.title,
                "Date": task.due_date,
                "Time": task.time,
                "Duration": f"{task.duration} min",
                "Priority": task.priority
            })

        st.write("### Today's Schedule")
        st.table(schedule_rows)

        st.write("### Why this plan was chosen")
        st.text(scheduler.explain_plan())
    else:
        st.warning("No tasks could be scheduled for today.")