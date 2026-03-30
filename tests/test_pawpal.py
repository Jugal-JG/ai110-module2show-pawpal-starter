from datetime import date, timedelta
from pawpal_system import Task, Pet, Owner, Scheduler


# --- Existing tests ---

def test_mark_complete_changes_status():
    task = Task(title="Walk", duration_minutes=20, priority="high")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_count():
    pet = Pet(name="Mochi", species="dog", age=3)
    assert len(pet.tasks) == 0
    pet.add_task(Task(title="Feeding", duration_minutes=10, priority="high"))
    assert len(pet.tasks) == 1


# --- Sorting correctness ---

def test_sort_by_time_returns_chronological_order():
    owner = Owner(name="Jordan", available_time_minutes=120)
    pet = Pet(name="Mochi", species="dog", age=3)
    owner.add_pet(pet)

    pet.add_task(Task(title="Evening walk", duration_minutes=25, priority="medium", start_time="18:00"))
    pet.add_task(Task(title="Feeding",      duration_minutes=10, priority="high",   start_time="07:30"))
    pet.add_task(Task(title="Morning walk", duration_minutes=30, priority="high",   start_time="07:00"))

    scheduler = Scheduler(owner=owner)
    sorted_tasks = scheduler.sort_by_time(pet.get_all_tasks())

    assert sorted_tasks[0].start_time == "07:00"
    assert sorted_tasks[1].start_time == "07:30"
    assert sorted_tasks[2].start_time == "18:00"


# --- Recurrence logic ---

def test_daily_task_creates_next_occurrence():
    task = Task(title="Morning walk", duration_minutes=30, priority="high", frequency="daily")
    next_task = task.mark_complete()

    assert task.completed is True
    assert next_task is not None
    assert next_task.title == "Morning walk"
    assert next_task.due_date == str(date.today() + timedelta(days=1))


def test_weekly_task_creates_next_occurrence():
    task = Task(title="Bath time", duration_minutes=20, priority="medium", frequency="weekly")
    next_task = task.mark_complete()

    assert next_task is not None
    assert next_task.due_date == str(date.today() + timedelta(weeks=1))


def test_once_task_returns_no_next_occurrence():
    task = Task(title="Vet visit", duration_minutes=60, priority="high", frequency="once")
    next_task = task.mark_complete()

    assert next_task is None


# --- Conflict detection ---

def test_detect_conflicts_flags_duplicate_start_times():
    owner = Owner(name="Jordan", available_time_minutes=120)
    pet = Pet(name="Mochi", species="dog", age=3)
    owner.add_pet(pet)

    t1 = Task(title="Morning walk", duration_minutes=30, priority="high",   start_time="07:00")
    t2 = Task(title="Brush fur",    duration_minutes=15, priority="low",    start_time="07:00")
    pet.add_task(t1)
    pet.add_task(t2)

    scheduler = Scheduler(owner=owner)
    warnings = scheduler.detect_conflicts([t1, t2])

    assert len(warnings) == 1
    assert "07:00" in warnings[0]


def test_no_conflict_when_times_are_different():
    owner = Owner(name="Jordan", available_time_minutes=120)
    pet = Pet(name="Mochi", species="dog", age=3)
    owner.add_pet(pet)

    t1 = Task(title="Morning walk", duration_minutes=30, priority="high", start_time="07:00")
    t2 = Task(title="Feeding",      duration_minutes=10, priority="high", start_time="07:30")
    pet.add_task(t1)
    pet.add_task(t2)

    scheduler = Scheduler(owner=owner)
    warnings = scheduler.detect_conflicts([t1, t2])

    assert len(warnings) == 0


# --- Time budget ---

def test_generate_plan_respects_time_budget():
    owner = Owner(name="Jordan", available_time_minutes=30)
    pet = Pet(name="Mochi", species="dog", age=3)
    owner.add_pet(pet)

    pet.add_task(Task(title="Long walk",  duration_minutes=25, priority="high"))
    pet.add_task(Task(title="Feeding",    duration_minutes=10, priority="high"))  # 25+10=35 > 30, so this gets dropped

    scheduler = Scheduler(owner=owner)
    plan = scheduler.generate_plan()

    total = sum(t.duration_minutes for t in plan)
    assert total <= 30


# --- Filtering ---

def test_filter_incomplete_tasks_only():
    owner = Owner(name="Jordan", available_time_minutes=120)
    pet = Pet(name="Mochi", species="dog", age=3)
    owner.add_pet(pet)

    done_task = Task(title="Morning walk", duration_minutes=30, priority="high", completed=True)
    todo_task = Task(title="Feeding",      duration_minutes=10, priority="high", completed=False)
    pet.add_task(done_task)
    pet.add_task(todo_task)

    scheduler = Scheduler(owner=owner)
    incomplete = scheduler.filter_tasks(pet.get_all_tasks(), only_incomplete=True)

    assert len(incomplete) == 1
    assert incomplete[0].title == "Feeding"
