---
layout: post
title: "Learning tracks: budget MCU vs ROS path"
chapter: "00"
order: 2
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter00
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

**Track A — budget MCU:** ESP32 or Pico + TT chassis + TB6612/DRV8833-class driver + ranging. Capstone A works without ROS.

**Track B — ROS:** same hardware + Ubuntu 24.04 for Jazzy; optional Pi 5 later.

Do not buy LiDAR before Capstone A acceptance. Optional architecture reference: [linorobot2](https://github.com/linorobot/linorobot2).



## Mindset

Robotics rewards **slow reliability**: power discipline, labeled wires, and notes beat clever one-off hacks.

## Capstone foreshadow

Everything in early chapters exists to make Chapter 07 teleop boringly reliable—then ROS 2 is a messaging layer on top of physics you already trust.

<!--exp-->
## Practice prompt

Teach-back: explain “Learning tracks: budget MCU vs ROS path” to a friend in 3 minutes, then list what hardware you’d put on the desk to demonstrate it.

## Exercises

1. Five-bullet summary.
2. Do (or dry-run) the lab; paste results.
3. Sketch one diagram from memory.
4. List two mistakes to avoid.
5. Date an entry in `lab-notes.md`.

## Further reading

- [lino](https://github.com/linorobot/linorobot2)
- [microros](https://micro.ros.org/)
- [pio](https://docs.platformio.org/)
