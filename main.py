from pawpal_system import Owner, Pet, Task, Scheduler

# --- Setup ---
owner = Owner(name="Jordan", available_time_minutes=120)

mochi = Pet(name="Mochi", species="dog", age=3)
luna  = Pet(name="Luna",  species="cat", age=2)

# Tasks added out of order intentionally to test sort_by_time
mochi.add_task(Task(title="Evening walk",    duration_minutes=25, priority="medium", category="walk",     start_time="18:00", frequency="daily"))
mochi.add_task(Task(title="Morning walk",    duration_minutes=30, priority="high",   category="walk",     start_time="07:00", frequency="daily"))
mochi.add_task(Task(title="Feeding",         duration_minutes=10, priority="high",   category="feeding",  start_time="07:30", frequency="daily"))
mochi.add_task(Task(title="Flea medication", duration_minutes=5,  priority="medium", category="meds",     start_time="08:00", frequency="weekly"))

luna.add_task(Task(title="Playtime",         duration_minutes=20, priority="medium", category="enrichment", start_time="17:00"))
luna.add_task(Task(title="Brush fur",        duration_minutes=15, priority="low",    category="grooming",   start_time="07:00"))  # same time as Mochi's morning walk — conflict!

owner.add_pet(mochi)
owner.add_pet(luna)

scheduler = Scheduler(owner=owner)

# --- 1. Generate plan (priority order) ---
print("=== Priority-Based Plan ===")
plan = scheduler.generate_plan()
print(scheduler.explain_plan(plan))

# --- 2. Sort all tasks by time ---
print("\n=== All Tasks Sorted by Start Time ===")
all_tasks = owner.get_all_tasks()
for t in scheduler.sort_by_time(all_tasks):
    time_tag = t.start_time if t.start_time else "unscheduled"
    print(f"  {time_tag} | {t.title} ({t.priority})")

# --- 3. Filter: only Mochi's incomplete tasks ---
print("\n=== Mochi's Incomplete Tasks ===")
mochi_tasks = scheduler.filter_tasks(all_tasks, pet_name="Mochi", only_incomplete=True)
for t in mochi_tasks:
    print(f"  {t.title} — {t.duration_minutes} min [{t.frequency}]")

# --- 4. Conflict detection ---
print("\n=== Conflict Check ===")
conflicts = scheduler.detect_conflicts(plan)
if conflicts:
    for warning in conflicts:
        print(f"  WARNING: {warning}")
else:
    print("  No conflicts found in the plan.")

# Also check all tasks (will catch Brush fur vs Morning walk both at 07:00)
print("\n=== Conflict Check (all tasks) ===")
all_conflicts = scheduler.detect_conflicts(scheduler.sort_by_time(all_tasks))
if all_conflicts:
    for warning in all_conflicts:
        print(f"  WARNING: {warning}")

# --- 5. Recurring task demo ---
print("\n=== Recurring Task Demo ===")
morning_walk = mochi.tasks[1]
print(f"  Completing: '{morning_walk.title}' (frequency: {morning_walk.frequency})")
next_task = morning_walk.mark_complete()
if next_task:
    print(f"  Next occurrence auto-created: '{next_task.title}' due {next_task.due_date}")
