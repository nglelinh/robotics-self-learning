---
layout: post
title: "Motor driver board ID: L298N, TB6612, DRV8833"
chapter: "05"
order: 2
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter05
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

![H-bridge]({{ site.imgurl }}/generated/hbridge_concept.png)

![L298N module]({{ site.imgurl }}/wikimedia/Dosmotorsl298n.jpg)

## Core ideas

Lab: label VMOT/GND/PWM/EN from module docs on a photo.


## Hands-on lab notes

**Safety:** wheels up for motion; power last; lithium attended.
**Procedure:** follow the numbered guidance in Core ideas; photograph wiring.
**Record:** meter readings / serial lines / tooth counts in `lab-notes.md`.
**Common mistakes:** missing common GND; USB powering motors; swapped motor leads; floating buttons without pull-ups.


## Actuator hygiene

Wheels up for first spins. Current-limit when you have a PSU. Expect stall current spikes. Heat-sink older H-bridge modules. Label motor left/right in firmware constants.


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
## Driver comparison cheat-sheet

| Board | Clues | Notes |
|-------|-------|-------|
| L298N | Big heatsink, 5V jumper | Higher drop; hotter |
| TB6612 | Smaller module | Efficient for small robots |
| DRV8833 | Tiny breakout | Low-voltage motors |

Always identify **VMOT**, **logic VCC**, **GND**, **IN/PWM**, **O1/O2** from the module silkscreen + PDF—not from memory.

## Exercises

1. Five-bullet summary.
2. Do (or dry-run) the lab; paste results.
3. Sketch one diagram from memory.
4. List two mistakes to avoid.
5. Date an entry in `lab-notes.md`.

## Further reading

- See COURSE_OUTLINE.md
