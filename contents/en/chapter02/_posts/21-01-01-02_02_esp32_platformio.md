---
layout: post
title: "Arduino IDE / PlatformIO for ESP32"
chapter: "02"
order: 2
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

## Core ideas

Install PlatformIO or Arduino-ESP32; select board; 115200 serial. Lab: blink.


## Hands-on lab notes

**Safety:** wheels up for motion; power last; lithium attended.
**Procedure:** follow the numbered guidance in Core ideas; photograph wiring.
**Record:** meter readings / serial lines / tooth counts in `lab-notes.md`.
**Common mistakes:** missing common GND; USB powering motors; swapped motor leads; floating buttons without pull-ups.


## Bring-up order

USB enumerate → blink → serial hello → GPIO read → PWM unloaded → then drivers/battery. Skipping ahead causes “random” brownout bugs that look like software.


## Lab BOM (typical)

| Item | Notes |
|------|-------|
| Multimeter | Continuity + DC V + Ω |
| Breadboard / harness | As required by steps |
| Target parts for this lesson | See Core ideas |
| Notebook / phone camera | Wire photos + readings |

## Expected observations

You should obtain at least one **numeric** reading or a **pass/fail** motion check, written into `lab-notes.md` with date.

<!--exp-->
## Practice prompt

Teach-back: explain “Arduino IDE / PlatformIO for ESP32” to a friend in 3 minutes, then list what hardware you’d put on the desk to demonstrate it.

## Exercises

1. Five-bullet summary.
2. Do (or dry-run) the lab; paste results.
3. Sketch one diagram from memory.
4. List two mistakes to avoid.
5. Date an entry in `lab-notes.md`.

## Further reading

- [pio](https://docs.platformio.org/)
- [esp32](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/)
