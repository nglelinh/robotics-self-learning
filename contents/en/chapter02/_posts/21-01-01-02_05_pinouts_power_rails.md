---
layout: post
title: "Pinouts, levels, and board power rails"
chapter: "02"
order: 5
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter02
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

## Figures

![Headers and rails]({{ site.imgurl }}/generated/pcb_mcu_anatomy.png)

## Core ideas

3.3 V GPIO; level-shift 5 V sensors; shared GND with drivers.



## Bring-up order

USB enumerate → blink → serial hello → GPIO read → PWM unloaded → then drivers/battery. Skipping ahead causes “random” brownout bugs that look like software.

<!--exp-->
## Practice prompt

Teach-back: explain “Pinouts, levels, and board power rails” to a friend in 3 minutes, then list what hardware you’d put on the desk to demonstrate it.

## Exercises

1. Five-bullet summary.
2. Do (or dry-run) the lab; paste results.
3. Sketch one diagram from memory.
4. List two mistakes to avoid.
5. Date an entry in `lab-notes.md`.

## Further reading

- [logic](https://learn.sparkfun.com/tutorials/logic-levels)
