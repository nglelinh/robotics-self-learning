---
layout: post
title: "Capacitors, diodes, and LEDs identification"
chapter: "01"
order: 4
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

## Figures

![Capacitor polarity]({{ site.imgurl }}/generated/capacitor_polarity.png)

![Electrolytic capacitor]({{ site.imgurl }}/wikimedia/Electrolytic_capacitor.jpg)

![LEDs]({{ site.imgurl }}/wikimedia/LEDs.jpg)

![Lookalike components]({{ site.imgurl }}/generated/component_lookalikes.png)

## Core ideas

Electrolytic stripe = negative. Ceramic usually non-polar. LED flat/short lead often cathode; diode band = cathode. SMD blank brown often cap; coded often resistor—verify.


## Hands-on lab notes

**Safety:** wheels up for motion; power last; lithium attended.
**Procedure:** follow the numbered guidance in Core ideas; photograph wiring.
**Record:** meter readings / serial lines / tooth counts in `lab-notes.md`.
**Common mistakes:** missing common GND; USB powering motors; swapped motor leads; floating buttons without pull-ups.


## Bench ID workflow

1. Look (package, markings, polarity stripe).
2. Meter (continuity / diode / Ω) when safe.
3. Datasheet / module wiki for pin names.
4. Photograph both sides of modules for your notes.

## Safety with meters

Do not measure resistance on a powered circuit. Start with a high voltage range when probing unknown supplies. Keep one hand away from high-energy packs.


## Lab BOM (typical)

| Item | Notes |
|------|-------|
| Multimeter | Continuity + DC V + Ω |
| Breadboard / harness | As required by steps |
| Target parts for this lesson | See Core ideas |
| Notebook / phone camera | Wire photos + readings |

## Expected observations

You should obtain at least one **numeric** reading or a **pass/fail** motion check, written into `lab-notes.md` with date.


## Polarity drill

Electrolytic: stripe/minus toward ground in single-supply decoupling (typical). LED: confirm with diode mode (one direction conducts). Putting an electrolytic in backwards on a battery rail can vent—double-check before power.

<!--exp-->
## Practice prompt

Teach-back: explain “Capacitors, diodes, and LEDs identification” to a friend in 3 minutes, then list what hardware you’d put on the desk to demonstrate it.

## Exercises

1. Five-bullet summary.
2. Do (or dry-run) the lab; paste results.
3. Sketch one diagram from memory.
4. List two mistakes to avoid.
5. Date an entry in `lab-notes.md`.

## Further reading

- See COURSE_OUTLINE.md
