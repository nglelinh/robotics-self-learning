---
layout: post
title: "Sensor package ID: HC-SR04, ToF, IMU, IR, encoders, cameras"
chapter: "04"
order: 2
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter04
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

![Sensor ID sheet]({{ site.imgurl }}/generated/sensor_package_id.png)

## Core ideas

ID sheet: HC-SR04 twin cans; VL53 ToF; MPU6050; IR pair; encoder; camera FPC.


## Hands-on lab notes

**Safety:** wheels up for motion; power last; lithium attended.
**Procedure:** follow the numbered guidance in Core ideas; photograph wiring.
**Record:** meter readings / serial lines / tooth counts in `lab-notes.md`.
**Common mistakes:** missing common GND; USB powering motors; swapped motor leads; floating buttons without pull-ups.


## Sensor hygiene

Shared GND with MCU. Decoupling caps near modules. Cable strain relief. Log raw units first; convert later. Calibrate on a meterstick when possible.


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
## Bench tell-tales

| Module | Tell |
|--------|------|
| HC-SR04 | Two metal cans, 4-pin header |
| VL53L0X | Tiny optical window, I2C pads |
| MPU6050 | Flat IMU board, often 0x68 |
| IR reflectance | LED + phototransistor pair |
| Wheel encoder | Slotted disk / Hall on motor |
| ESP32-CAM style | FPC camera + large board |

Ask: voltage (3.3 vs 5), bus (I2C/UART/analog), and mounting holes before wiring.

## Exercises

1. Five-bullet summary.
2. Do (or dry-run) the lab; paste results.
3. Sketch one diagram from memory.
4. List two mistakes to avoid.
5. Date an entry in `lab-notes.md`.

## Further reading

- See COURSE_OUTLINE.md
