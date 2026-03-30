# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Testing PawPal+

Run the test suite with:

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

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
