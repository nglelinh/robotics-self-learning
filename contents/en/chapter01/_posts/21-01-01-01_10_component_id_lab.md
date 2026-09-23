---
layout: post
title: "Lab: continuity, ohmmeter ID, and lookalikes"
chapter: "01"
order: 10
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

![Color code]({{ site.imgurl }}/generated/resistor_color_code.png)

![Lookalikes]({{ site.imgurl }}/generated/component_lookalikes.png)

![Resistors]({{ site.imgurl }}/wikimedia/resistors_assortment.jpg)

## Core ideas

BOM: assort resistors, electrolytic, ceramic, LED, diode, jumpers, meter. Procedure: map breadboard continuity; decode+measure resistors; diode-mode polarity; write lookalike list.


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


## Lab procedure (timed)

1. (10 min) Continuity-map one breadboard column vs adjacent.
2. (15 min) Decode 5 THT resistors; measure; table errors.
3. (10 min) LED + diode polarity via meter.
4. (10 min) Sort lookalikes; write 3 traps.
5. (5 min) Photo + commit notes.

<!--exp-->
## Acceptance criteria

- Continuity map sketched
- ≥5 resistors within ~10% of decode (or explain meter lead error on low R)
- LED & diode polarity demonstrated
- Three lookalike traps written
- Photos attached to notes

## Exercises

1. Five-bullet summary.
2. Do (or dry-run) the lab; paste results.
3. Sketch one diagram from memory.
4. List two mistakes to avoid.
5. Date an entry in `lab-notes.md`.

## Further reading

- See COURSE_OUTLINE.md
