from pawpal_system import Owner, Pet, Task, Scheduler

# Set up owner
owner = Owner(name="Jordan", available_time_minutes=90)

# Two pets
mochi = Pet(name="Mochi", species="dog", age=3)
luna = Pet(name="Luna", species="cat", age=2)

# Tasks for Mochi
mochi.add_task(Task(title="Morning walk",     duration_minutes=30, priority="high",   category="walk"))
mochi.add_task(Task(title="Feeding",          duration_minutes=10, priority="high",   category="feeding"))
mochi.add_task(Task(title="Flea medication",  duration_minutes=5,  priority="medium", category="meds"))

# Tasks for Luna
luna.add_task(Task(title="Playtime",          duration_minutes=20, priority="medium", category="enrichment"))
luna.add_task(Task(title="Brush fur",         duration_minutes=15, priority="low",    category="grooming"))

# Register pets
owner.add_pet(mochi)
owner.add_pet(luna)

# Generate and print schedule
scheduler = Scheduler(owner=owner)
plan = scheduler.generate_plan()
print(scheduler.explain_plan(plan))
