---
layout: post
title: "Resistor ID: THT color bands and SMD codes"
chapter: "01"
order: 3
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

![Resistor color code chart]({{ site.imgurl }}/generated/resistor_color_code.png)

![Resistor assortment (Commons)]({{ site.imgurl }}/wikimedia/resistors_assortment.jpg)

## Core ideas

4-band: digits + multiplier + tolerance. Brown-Blue-Orange-Gold = 16 kΩ ±5%. SMD `103` = 10 kΩ. Lab: decode five parts by eye, confirm with meter.


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


## Worked color-code examples

| Bands | Decode | Ohmmeter expectation |
|-------|--------|----------------------|
| Brown-Black-Red-Gold | 10×100=1 kΩ ±5% | ~0.95–1.05 kΩ |
| Yellow-Violet-Orange-Gold | 47 kΩ ±5% | mid tens of kΩ |
| Brown-Black-Black-Gold | 10 Ω ±5% | meter lead resistance matters |

SMD `472` → 47×10²=4.7 kΩ. If unmarked brown chip → suspect capacitor; do not assume.

<!--exp-->
## Multiplier & tolerance bands (quick)

Black×1, Brown×10, Red×100, Orange×1k, Yellow×10k, Green×100k, Blue×1M; Gold×0.1, Silver×0.01. Gold tolerance ±5%, Silver ±10%, Brown ±1% (5-band often).

## Pitfalls

- Counting bands left-to-right from the closer-grouped end.
- Mistaking blue for violet under warm light—measure.
- Assuming SMD zero-ohm jumpers (`0` / `000`) are “broken shorts”.

## Exercises

1. Five-bullet summary.
2. Do (or dry-run) the lab; paste results.
3. Sketch one diagram from memory.
4. List two mistakes to avoid.
5. Date an entry in `lab-notes.md`.

## Further reading

- See COURSE_OUTLINE.md
