---
layout: post
title: "Lab kit catalog: tools and bench equipment"
chapter: "00"
order: 4
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

![Beginner bench kit families]({{ site.imgurl }}/generated/kit_catalog_overview.png)

![Digital multimeter (Commons)]({{ site.imgurl }}/wikimedia/Digital_Multimeter_Aka.jpg)

![Soldering iron (Commons)]({{ site.imgurl }}/wikimedia/Soldering_iron.jpg)

![Breadboard (Commons)]({{ site.imgurl }}/wikimedia/breadboard.jpg)

## Core ideas

### Must-have families
Multimeter, temperature-controlled iron + solder/flux/wick, breadboard + Dupont, strippers/cutters, hex drivers, heat-shrink, calipers.

### Later lab upgrades
Current-limited bench PSU, USB logic analyzer, entry oscilloscope.

Beginner kit = measure + solder + prototype. Lab kit = measure currents safely and debug timing. See figures for layout.


## Hands-on lab notes

**Safety:** wheels up for motion; power last; lithium attended.
**Procedure:** follow the numbered guidance in Core ideas; photograph wiring.
**Record:** meter readings / serial lines / tooth counts in `lab-notes.md`.
**Common mistakes:** missing common GND; USB powering motors; swapped motor leads; floating buttons without pull-ups.


## Mindset

Robotics rewards **slow reliability**: power discipline, labeled wires, and notes beat clever one-off hacks.

## Capstone foreshadow

Everything in early chapters exists to make Chapter 07 teleop boringly reliable—then ROS 2 is a messaging layer on top of physics you already trust.


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
## Choosing beginner vs lab kit

| Need | Beginner kit | Lab upgrade |
|------|--------------|-------------|
| See continuity/voltage | Meter | Meter + current-limited PSU |
| Make harnesses | Basic iron | Better tips, flux, wick, fume awareness |
| Prototype | Breadboard + Dupont | Organizers + labeled bins |
| Debug protocols | Later | USB logic analyzer |
| See waveforms | Later | Entry oscilloscope |

## Tool use vignettes

- Meter continuity: find broken jumper before blaming code.
- Iron: heat pad+lead together; shiny cone ≠ blob.
- Calipers: measure shaft vs hub bore before printing adapters.

## Exercises

1. Five-bullet summary.
2. Do (or dry-run) the lab; paste results.
3. Sketch one diagram from memory.
4. List two mistakes to avoid.
5. Date an entry in `lab-notes.md`.

## Further reading

- [arduino](https://docs.arduino.cc/)
- [pololu](https://www.pololu.com/docs/0J44)
