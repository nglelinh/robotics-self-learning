---
layout: post
title: "Bill of materials and shopping strategy"
chapter: "00"
order: 5
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

## Figures

![BOM families]({{ site.imgurl }}/generated/kit_catalog_overview.png)

## Core ideas

Default robot: ESP32 (or Pico) + diff TT chassis + driver + HC-SR04/ToF + optional IMU/encoders + matched battery/charger. Prefer efficient drivers when possible ([Pololu motor driver guide](https://www.pololu.com/docs/0J44)). Buy by ratings (stall current, voltage), not by fading sale prices.



## Mindset

Robotics rewards **slow reliability**: power discipline, labeled wires, and notes beat clever one-off hacks.

## Capstone foreshadow

Everything in early chapters exists to make Chapter 07 teleop boringly reliable—then ROS 2 is a messaging layer on top of physics you already trust.

<!--exp-->
## Practice prompt

Teach-back: explain “Bill of materials and shopping strategy” to a friend in 3 minutes, then list what hardware you’d put on the desk to demonstrate it.

## Exercises

1. Five-bullet summary.
2. Do (or dry-run) the lab; paste results.
3. Sketch one diagram from memory.
4. List two mistakes to avoid.
5. Date an entry in `lab-notes.md`.

## Further reading

- [pololu](https://www.pololu.com/docs/0J44)
