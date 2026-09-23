---
layout: post
title: "Differential-drive kinematics"
chapter: "08"
order: 4
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter08
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

![Kinematics]({{ site.imgurl }}/generated/diff_drive_kinematics.png)

## Core ideas

\(v=(v_R+v_L)/2\), \(\omega=(v_R-v_L)/L\); map joystick→wheel speeds.



## Control notes

Start open-loop teleop; add encoder PID only after counts are trustworthy. Log loop period. MQTT/Wi-Fi adds latency—keep a local serial failsafe.

<!--exp-->
## Practice prompt

Teach-back: explain “Differential-drive kinematics” to a friend in 3 minutes, then list what hardware you’d put on the desk to demonstrate it.

## Exercises

1. Five-bullet summary.
2. Do (or dry-run) the lab; paste results.
3. Sketch one diagram from memory.
4. List two mistakes to avoid.
5. Date an entry in `lab-notes.md`.

## Further reading

- See COURSE_OUTLINE.md
