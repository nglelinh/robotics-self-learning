---
layout: post
title: "ESD, polarity, fuses, and brownouts"
chapter: "01"
order: 9
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter01
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

ESD discipline; reverse polarity kills drivers; motor stall current browns out MCU—common ground, bulk capacitance, separate motor supply when possible.



## Bench ID workflow

1. Look (package, markings, polarity stripe).
2. Meter (continuity / diode / Ω) when safe.
3. Datasheet / module wiki for pin names.
4. Photograph both sides of modules for your notes.

## Safety with meters

Do not measure resistance on a powered circuit. Start with a high voltage range when probing unknown supplies. Keep one hand away from high-energy packs.

<!--exp-->
## Practice prompt

Teach-back: explain “ESD, polarity, fuses, and brownouts” to a friend in 3 minutes, then list what hardware you’d put on the desk to demonstrate it.

## Exercises

1. Five-bullet summary.
2. Do (or dry-run) the lab; paste results.
3. Sketch one diagram from memory.
4. List two mistakes to avoid.
5. Date an entry in `lab-notes.md`.

## Further reading

- [logic](https://learn.sparkfun.com/tutorials/logic-levels)
