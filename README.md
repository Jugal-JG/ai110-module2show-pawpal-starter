# PawPal+ (Module 2 Project)

A smart pet care planner built with Python and Streamlit. Helps a busy pet owner schedule daily tasks for their pets based on priority, available time, and start times.

## Demo

<a href="/course_images/ai110/your_screenshot_name.png" target="_blank"><img src='/course_images/ai110/your_screenshot_name.png' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>

---

## Features

- **Owner + pet setup** — enter your name, free time for the day, and register multiple pets
- **Task management** — add care tasks (walks, feeding, meds, etc.) with duration, priority, start time, and frequency
- **Priority-based scheduling** — `generate_plan()` fits the most important tasks into your available time first
- **Sort by time** — tasks are displayed in chronological order by `start_time` (HH:MM)
- **Conflict warnings** — the scheduler detects and flags two tasks booked at the same time
- **Recurring tasks** — daily and weekly tasks auto-generate their next occurrence when marked complete
- **Filtering** — filter tasks by pet name or completion status

---

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Run the app

```bash
streamlit run app.py
```

### Run the CLI demo

```bash
python main.py
```

---

## Testing PawPal+

```bash
python -m pytest
```

The suite covers 10 tests across these behaviors:

| Test | What it checks |
|---|---|
| Task completion | `mark_complete()` flips `completed` to True |
| Task addition | Adding a task increases the pet's task count |
| Sort by time | Tasks come back in HH:MM chronological order |
| Daily recurrence | Completing a daily task creates one for tomorrow |
| Weekly recurrence | Completing a weekly task creates one 7 days out |
| One-time task | A `frequency="once"` task returns no next occurrence |
| Conflict detection | Two tasks at the same time trigger a warning |
| No false conflicts | Different start times produce zero warnings |
| Time budget | `generate_plan()` never exceeds available minutes |
| Filtering | `filter_tasks()` returns only incomplete tasks |

**Confidence level: ⭐⭐⭐⭐** — happy paths and key edge cases are covered. Overlapping duration detection (e.g. 07:00 + 30 min overlaps with 07:15) is not yet tested and would be the next thing to add.

---

## Smarter Scheduling

The scheduler has been upgraded with the following features:

- **Sort by time** — tasks can carry an optional `start_time` (HH:MM) and be sorted chronologically
- **Filter tasks** — filter by pet name or completion status to get focused views
- **Recurring tasks** — tasks marked as `daily` or `weekly` auto-generate their next occurrence when completed, with the due date calculated using `timedelta`
- **Conflict detection** — the scheduler warns if two tasks share the same `start_time`, preventing accidental double-booking

---

## Project structure

```
pawpal_system.py   # Core logic: Owner, Pet, Task, Scheduler classes
app.py             # Streamlit UI
main.py            # CLI demo script
tests/
  test_pawpal.py   # Automated test suite
reflection.md      # Design decisions and retrospective
```

---

## Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
