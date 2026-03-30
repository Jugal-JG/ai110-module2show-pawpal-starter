# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

Three core actions a user should be able to do in PawPal+:
1. Add a pet — give it a name, species, and age
2. Add care tasks — things like walks, feeding, or meds, each with a duration and priority
3. Generate a daily schedule — have the app figure out what fits in the day and in what order

I went with four classes: Owner, Pet, Task, and Scheduler. Owner holds the user's name and how much free time they have in a day. Pet belongs to an Owner and keeps a list of Tasks. Task is the smallest unit — one care activity with a duration and priority level. Scheduler takes everything and produces an ordered daily plan that respects the time budget.

**b. Design changes**

Nothing's been changed yet since this is the initial skeleton. One thing I'm already questioning is whether `tasks` should live on `Pet` or on `Scheduler` directly — keeping them on `Pet` feels cleaner right now since a pet's needs shouldn't depend on who's scheduling them.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers two main constraints: the owner's available time for the day, and each task's priority level. High priority tasks always get scheduled first regardless of duration. Within the same priority level, shorter tasks get picked first to fit more into the day. Time was the obvious hard constraint — you can't schedule more than the day allows. Priority felt more important than duration alone because some things (like meds) just can't be skipped.

**b. Tradeoffs**

The conflict detector only flags tasks with the exact same `start_time` string — it doesn't check for overlapping durations. So a 30-minute task at 07:00 and a 10-minute task at 07:15 won't trigger a warning even though they'd overlap in real life. This is a conscious simplification: exact-time conflict detection is straightforward and catches the obvious cases. Handling overlapping durations would need proper time arithmetic and is something to tackle in a future iteration.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
