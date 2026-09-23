---
layout: post
title: "Gears: spur, worm, planetary, ratio, backlash"
chapter: "06"
order: 3
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter06
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

![Gear ratio]({{ site.imgurl }}/generated/gear_train_ratio.png)

## Core ideas

Ratio \(i=N_2/N_1\); torque↑ speed↓; backlash on reverse; worm/planetary options.


## Hands-on lab notes

**Safety:** wheels up for motion; power last; lithium attended.
**Procedure:** follow the numbered guidance in Core ideas; photograph wiring.
**Record:** meter readings / serial lines / tooth counts in `lab-notes.md`.
**Common mistakes:** missing common GND; USB powering motors; swapped motor leads; floating buttons without pull-ups.


## Mechanism checklists

After assembly: spin shafts by hand (binding?), check set screws, verify gear mesh backlash isn’t catastrophic, add threadlocker only where intentional, route cables with service loops.


## Lab BOM (typical)

| Item | Notes |
|------|-------|
| Multimeter | Continuity + DC V + Ω |
| Breadboard / harness | As required by steps |
| Target parts for this lesson | See Core ideas |
| Notebook / phone camera | Wire photos + readings |

## Expected observations

You should obtain at least one **numeric** reading or a **pass/fail** motion check, written into `lab-notes.md` with date.


## Ratio lab math

If pinion \(N_1=12\) and wheel \(N_2=36\), \(i=3\). One turn of pinion → 1/3 turn of wheel. Torque scales ~×3 ignoring losses; speed scales ~÷3. Backlash shows up when reversing direction—mark a tooth with a marker and watch lost motion.

<!--exp-->
## Backlash & planetary/worm

Backlash is lost motion on reverse—plastic TT gearboxes show it clearly. Planetary stages pack ratio into small volume. Worm drives can be high-ratio and often resist back-driving—useful for arms, annoying for compliant wheels.

## Lab calculation

Measure motor free speed roughly (phone tach apps are approximate) and estimate wheel RPM after gearbox: \(\omega_{out}\approx\omega_{in}/i\).

## Exercises

1. Five-bullet summary.
2. Do (or dry-run) the lab; paste results.
3. Sketch one diagram from memory.
4. List two mistakes to avoid.
5. Date an entry in `lab-notes.md`.

## Further reading

- See COURSE_OUTLINE.md
