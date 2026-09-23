---
layout: post
title: "C++ vs MicroPython for robots"
chapter: "03"
order: 1
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter03
lesson_type: required
draft: false
---

Estimated time: **~60 minutes**.

## Learning objectives

1. Explain the lesson ideas in your own words.
2. Complete lab/ID tasks if present.
3. Connect this lesson to Capstone A or ROS path.
4. Note two failure modes.
5. Save further-reading links.

## 60-minute plan

| Min | Activity |
|----:|----------|
| 0–5 | Objectives + figures |
| 5–25 | Core reading / math |
| 25–45 | Lab or ID practice |
| 45–55 | Exercises |
| 55–60 | Notes + links |

## Core ideas

MicroPython iterates fast; C++ tighter timing—both OK for Capstone A.



## Real-time habits

Keep `loop()`/`while True` predictable. Long blocking calls break debounce and control. Prefer millis()/ticks scheduling over deep delay stacks.

<!--exp-->
## Practice prompt

Teach-back: explain “C++ vs MicroPython for robots” to a friend in 3 minutes, then list what hardware you’d put on the desk to demonstrate it.

## Exercises

1. Five-bullet summary.
2. Do (or dry-run) the lab; paste results.
3. Sketch one diagram from memory.
4. List two mistakes to avoid.
5. Date an entry in `lab-notes.md`.

## Further reading

- See COURSE_OUTLINE.md
