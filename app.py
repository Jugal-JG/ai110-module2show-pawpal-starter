import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")
st.caption("A smart daily planner for your pet's care tasks.")

# --- Session state ---
if "owner" not in st.session_state:
    st.session_state.owner = None

# --- Owner Info ---
st.subheader("Owner Info")
col1, col2 = st.columns(2)
with col1:
    owner_name = st.text_input("Your name", value="Jordan")
with col2:
    available_time = st.number_input("Free time today (minutes)", min_value=10, max_value=480, value=90)

if st.button("Set / Update Owner"):
    if st.session_state.owner is None:
        st.session_state.owner = Owner(name=owner_name, available_time_minutes=available_time)
    else:
        st.session_state.owner.name = owner_name
        st.session_state.owner.set_available_time(available_time)
    st.success(f"Owner set: {owner_name} ({available_time} min available today)")

st.divider()

# --- Add a Pet ---
st.subheader("Add a Pet")
col1, col2, col3 = st.columns(3)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "other"])
with col3:
    age = st.number_input("Age (years)", min_value=0, max_value=30, value=3)

if st.button("Add Pet"):
    if st.session_state.owner is None:
        st.warning("Set an owner first.")
    else:
        st.session_state.owner.add_pet(Pet(name=pet_name, species=species, age=age))
        st.success(f"Added {pet_name} the {species}!")

if st.session_state.owner and st.session_state.owner.pets:
    st.markdown("**Pets registered:**")
    for p in st.session_state.owner.pets:
        st.write(f"- {p.name} ({p.species}, age {p.age})")

st.divider()

# --- Add a Task ---
st.subheader("Add a Task")
pet_names = [p.name for p in st.session_state.owner.pets] if st.session_state.owner else []

if not pet_names:
    st.info("Add a pet above before adding tasks.")
else:
    col1, col2, col3 = st.columns(3)
    with col1:
        selected_pet = st.selectbox("For which pet?", pet_names)
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
    with col3:
        start_time = st.text_input("Start time (HH:MM, optional)", value="")
        frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])

    if st.button("Add Task"):
        pet_obj = next(p for p in st.session_state.owner.pets if p.name == selected_pet)
        pet_obj.add_task(Task(
            title=task_title,
            duration_minutes=int(duration),
            priority=priority,
            start_time=start_time.strip(),
            frequency=frequency,
        ))
        st.success(f"'{task_title}' added to {selected_pet}.")

    # Show tasks sorted by time
    all_tasks = st.session_state.owner.get_all_tasks() if st.session_state.owner else []
    if all_tasks:
        scheduler = Scheduler(owner=st.session_state.owner)
        sorted_tasks = scheduler.sort_by_time(all_tasks)
        st.markdown("**All tasks (sorted by start time):**")
        st.table([
            {
                "title": t.title,
                "priority": t.priority,
                "duration (min)": t.duration_minutes,
                "start time": t.start_time if t.start_time else "—",
                "frequency": t.frequency,
                "done": "yes" if t.completed else "no",
            }
            for t in sorted_tasks
        ])

st.divider()

# --- Generate Schedule ---
st.subheader("Generate Today's Schedule")

if st.button("Generate Schedule"):
    if st.session_state.owner is None:
        st.warning("Set an owner first.")
    elif not st.session_state.owner.get_all_tasks():
        st.warning("Add some tasks first.")
    else:
        scheduler = Scheduler(owner=st.session_state.owner)
        plan = scheduler.generate_plan()

        # Conflict warnings
        conflicts = scheduler.detect_conflicts(plan)
        if conflicts:
            for warning in conflicts:
                st.warning(f"Scheduling conflict: {warning}")

        # Schedule table
        if plan:
            st.success(f"Scheduled {len(plan)} task(s) — {sum(t.duration_minutes for t in plan)} / {st.session_state.owner.available_time_minutes} min used")
            st.table([
                {
                    "task": t.title,
                    "priority": t.priority,
                    "start time": t.start_time if t.start_time else "—",
                    "duration (min)": t.duration_minutes,
                    "frequency": t.frequency,
                }
                for t in plan
            ])
        else:
            st.error("No tasks fit in the available time. Try increasing free time or shortening tasks.")
