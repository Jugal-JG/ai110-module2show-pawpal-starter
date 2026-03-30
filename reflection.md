# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

Three core actions a user should be able to do in PawPal+:
1. Add a pet — give it a name, species, and age
2. Add care tasks — things like walks, feeding, or meds, each with a duration and priority
3. Generate a daily schedule — have the app figure out what fits in the day and in what order

I went with four classes: Owner, Pet, Task, and Scheduler. Owner holds the user's name and how much free time they have in a day. Pet belongs to an Owner and keeps a list of Tasks. Task is the smallest unit — one care activity with a duration and priority level. Scheduler takes everything and produces an ordered daily plan that respects the time budget.

**b. Design changes**

The biggest change from the initial skeleton was adding `start_time`, `frequency`, and `due_date` fields to Task. The original design had no concept of when a task happens during the day or whether it repeats — just what it is and how long it takes. Once conflict detection and recurring tasks became requirements, those fields had to go on Task directly rather than being managed externally. Keeping them on Task made the Scheduler logic simpler and kept each class responsible for its own data.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers two main constraints: the owner's available time for the day, and each task's priority level. High priority tasks always get scheduled first regardless of duration. Within the same priority level, shorter tasks get picked first to fit more into the day. Time was the obvious hard constraint — you can't schedule more than the day allows. Priority felt more important than duration alone because some things (like meds) just can't be skipped.

**b. Tradeoffs**

The conflict detector only flags tasks with the exact same `start_time` string — it doesn't check for overlapping durations. So a 30-minute task at 07:00 and a 10-minute task at 07:15 won't trigger a warning even though they'd overlap in real life. This is a conscious simplification: exact-time conflict detection is straightforward and catches the obvious cases. Handling overlapping durations would need proper time arithmetic and is something to tackle in a future iteration.

---

## 3. AI Collaboration

**a. How you used AI**

AI was used throughout — for the initial UML brainstorm, generating class skeletons from that UML, drafting test cases, and connecting the backend to Streamlit. The most useful prompts were specific ones that gave context: referencing the actual file and asking about a concrete behavior (like "how should Scheduler retrieve tasks from Owner's pets") rather than vague requests. Asking for one thing at a time also helped — generating stubs first, then logic, kept the output manageable and easier to review.

**b. Judgment and verification**

At one point the AI suggested storing tasks directly on Scheduler rather than on Pet. The reasoning was that scheduling is Scheduler's job, so it should own the data it works with. That felt wrong — a pet's care needs exist independently of who's doing the scheduling. If you swap out the Scheduler or run it differently, the pet's tasks shouldn't disappear. Keeping tasks on Pet made the design more sensible and the tests easier to write, since each Pet was self-contained.

---

## 4. Testing and Verification

**a. What you tested**

Ten behaviors were tested: task completion status, task addition count, chronological sort order, daily and weekly recurrence, one-time task (no next occurrence), conflict detection with duplicates, no false positives on different times, time budget enforcement, and incomplete-only filtering. The recurrence and conflict tests were the most important — those are the features most likely to have subtle bugs that only show up in edge cases.

**b. Confidence**

Confidence level is 4/5. The core scheduling behaviors are solid and well-covered. The main gap is overlapping duration detection — the current conflict check only catches exact `start_time` matches, not cases where one task's duration bleeds into another's start time. That would be the first thing to add in a next iteration, along with a test for a pet that has zero tasks.

---

## 5. Reflection

**a. What went well**

The cleanest part of the project was the class structure. Keeping Owner, Pet, Task, and Scheduler as separate, focused classes made every phase easier — adding features in Phase 4 didn't require touching the UI, and writing tests in Phase 5 didn't require spinning up Streamlit. The separation paid off.

**b. What you would improve**

The conflict detection is the most obvious thing to improve — upgrading from exact-time matching to duration-overlap checking would make it actually useful for real scheduling. I'd also add a way to mark tasks complete from inside the Streamlit UI and have the recurring next-occurrence show up automatically, rather than that only working in the CLI demo.

**c. Key takeaway**

AI is most useful as a fast first draft — it gets you to something runnable quickly, but you still have to understand every line and make the architectural calls yourself. The moments where I pushed back on an AI suggestion (like where tasks should live) were the moments that kept the design coherent. Being the "lead architect" means the AI handles speed, and you handle judgment.
