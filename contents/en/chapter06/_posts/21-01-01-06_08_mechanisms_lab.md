---
layout: post
title: "Lab: gear ratio measurement and assembly checklist"
chapter: "06"
order: 8
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter06
lesson_type: required
draft: false
---

Estimated time: **80–110 minutes**. This lesson is the hands-on. Power stays off for every mechanical check.

## Learning objectives

By the end of this lesson you have a gear ratio you both predicted and checked, a backlash estimate at the wheel in degrees, and a written assembly checklist you can run before any voltage in Chapter 07. You can tell a simple idler from a ratio change, and you can multiply a gearbox stamp by an external belt when both exist.

## Prerequisites

Lessons 01–07. You need $$b$$, $$r$$, an M3 habit, the ratio definition $$i = N_{\text{out}}/N_{\text{in}} = \omega_{\text{in}}/\omega_{\text{out}}$$, and the strain-relief tug. A cardboard pointer and a protractor, or a paper protractor, are enough instruments.

## Why this matters for Capstone A and the ROS path

Chapter 07 is the first time this chassis is allowed to see voltage. The checklist below is the gate. A wheel that scrapes, a battery that slides, or a set screw on the round will waste that lab on a failure Lesson 07 already named. The ratio you measure is the ratio `diff_drive_controller` will turn into meters. A result within about 10 percent of the nameplate is what molded teeth can support. If the kit is still in transit, the drawing prediction is the deliverable and you label it as a drawing. You do not invent a measured angle you did not take.

## What you are checking

Count teeth if you can see them, or read the stamp on the gearbox. The stamp is the prediction. The check is kinematic: a pointer on the input, a pointer on the output, a known input motion, a measured output angle. For a ratio $$i$$, three turns of the input should produce

$$
\theta_{\text{out}} = \frac{3}{i} \times 360^\circ.
$$

Hold the input still afterward and rock the wheel. The angle it moves before the input pointer must move is the backlash you will quote. Eyeball is enough. A few degrees at the wheel is ordinary molded gearing. Tens of degrees means a loose set screw or a skipped belt tooth, which is a different fault.

A simple idler reverses direction and does not change $$i$$. Count it as a mesh for the sign, not as a factor, unless it is a compound idler with two different tooth counts locked together. If a belt sits outside the gearbox, the wheel ratio is the product. Students lose a factor of two here more often than they mis-count a pinion.

Then run the assembly list with the battery on the bench, not on the connector. Fasteners tight. Set screws on flats. Wheels clear of the plate. Caster spins and trails. Wires have a service loop and the solder does not bend. Battery cannot slide in its future pocket. Both motors turn by hand with similar drag. A motor that feels gritty or much stiffer than its twin gets a note before Chapter 07, not a higher PWM.

![Name the input before you divide: the figure is the prediction, the pointers are the check]({{ site.imgurl }}/generated/gear_train_ratio.png)

## Worked example

A TT motor is stamped 1:48. Three input turns should give

$$
\theta_{\text{out}} = \frac{3}{48} \times 360^\circ = 22.5^\circ.
$$

You measure $$24^\circ$$ at the wheel pointer. The relative error is

$$
\frac{24 - 22.5}{22.5} \approx 0.067,
$$

about 7 percent, inside the 10 percent band for molded teeth and a handmade pointer. You write $$i = 48$$ and “checked, 24° versus 22.5°.” If the pointer had landed near $$45^\circ$$, the error is a factor of two: a missed 2:1 belt, or a stamp you halved. If it had landed near $$67.5^\circ$$, you used $$i = 16$$ or you turned the wrong shaft. Backlash measured by rocking the wheel, say $$5^\circ$$, is recorded next to the ratio and is not “fixed” by tightening the mesh until it binds.

Direction: one external mesh, or an odd number of them, reverses the wheel relative to the motor. Your firmware sign in Lesson 05 has to agree with this observation, still with power off, by turning the shaft the way the motor will turn.

## Lab: pointers, then the list

### Safety

Power remains off. Battery is disconnected and sitting where a tug cannot land it on the terminals. Gear teeth pinch; turn shafts from the pointer, not from inside the mesh. If a shaft will not move, stop and look for a rub. Do not add voltage to “free” it.

### BOM

| Item | Role |
|------|------|
| Gearmotor or a scale gear drawing | The ratio |
| Two pointers: tape flags or cardboard arrows | Input and output |
| Protractor, or a printed one | Output angle and backlash |
| Hex key for the set screws | The flat |
| Zip tie | Service loop, if a wire is already on the motor |
| `lab-notes.md` | Prediction, measurement, checklist |

### Steps

1. Write the prediction. Tooth counts if visible, otherwise the stamp. Compute $$\theta_{\text{out}}$$ for exactly three input turns.
2. Tape a pointer to the input and one to the output. Mark a zero on the bench.
3. Turn the input exactly three revolutions. Measure the output angle. Compare with the prediction and write the percent difference.
4. Hold the input. Rock the output. Estimate backlash in degrees at the wheel.
5. Walk the checklist and tick each line in the notes: fasteners tight; set screws on flats; wheels not rubbing; caster spins and trails; service loop, solder joint quiet; battery cannot slide; both motors turn by hand with similar drag.
6. If you only have a drawing, do steps 1 and the sketches, write “drawing, paper result is the deliverable,” and still draft the checklist as the procedure you will run when the box arrives.

### Expected results

A ratio within about 10 percent of the nameplate when hardware is present, or a clearly labeled paper prediction when it is not. Backlash quoted in degrees. Every checklist line marked pass, fail, or “not on the bench yet.” Failed lines name the fix, not a plan to discover it during the powered lab.

### Faults

| What you see | What it usually means |
|--------------|------------------------|
| Angle is the reciprocal of the prediction | Input and output names were swapped |
| Angle is half or double | Gearbox and an external belt were not multiplied, or one of them was applied twice |
| Direction wrong, ratio right | An idler was treated as a ratio change, or a mesh was left out of the sign count |
| Output flops tens of degrees | Set screw, stripped hub, or a skipped belt tooth |
| One motor much stiffer by hand | Rub, or a damaged gearbox; do not power it to confirm |

## Mua ở Việt Nam / Where to buy in Vietnam

Buy only what the checklist proved missing. A protractor app is enough if you can sight along the pointer. A TT motor with a visible stamp is the part that makes step 1 a reading instead of a guess.

| What | Keywords | Rough band (VND) | Notes |
|------|----------|------------------|-------|
| TT gearmotor | `động cơ giảm tốc TT encoder` | 45.000–120.000 each | Stamp is the prediction |
| M3 kit, if the sort in Lesson 02 was short | `ốc M3` | 25.000–70.000 | Fasteners line on the checklist |
| Caster, if the nose still drags | `bánh caster robot` | 12.000–40.000 | Must trail |

Search pages:

- [Hshop](https://hshop.vn/search?q=%C4%91%E1%BB%99ng+c%C6%A1+gi%E1%BA%A3m+t%E1%BB%91c+TT)
- [Shopee](https://shopee.vn/search?keyword=%C4%91%E1%BB%99ng%20c%C6%A1%20gi%E1%BA%A3m%20t%E1%BB%91c%20TT%20encoder)
- [Lazada](https://www.lazada.vn/catalog/?q=%E1%BB%91c%20M3)
- [Thế Giới IC](https://www.thegioiic.com/search?q=%E1%BB%91c%20M3)

Prices move. Do not buy a second gearbox to avoid measuring the first one.

## Exercises

1. Stamp 1:90. Predict the output angle for three input turns.
2. You measure $$12^\circ$$ after those three turns on a 1:48 motor. Is that inside 10 percent of 22.5°? What do you check next?
3. A 20-tooth pinion drives a 20-tooth idler, which drives a 40-tooth gear. Give $$i$$ and the direction of the output relative to the pinion.
4. Gearbox 1:48 and a GT2 stage with 20 teeth on the motor pulley and 40 teeth on the wheel pulley. What $$i$$ does the wheel see? What is $$\theta_{\text{out}}$$ for three motor turns?
5. List the seven checklist lines and star the two that, if skipped, most directly invent phantom odometry.

### Answer guidance

1. $$\theta_{\text{out}} = 3/90 \times 360^\circ = 12^\circ$$. 2. $$|12 - 22.5|/22.5 \approx 47$$ percent, well outside the band. Check that you turned the motor shaft three times, that you read 1:48 and not a different stamp, and that a belt was not left out or added. 3. $$i = 40/20 = 2$$. The simple idler does not change the ratio. Two external meshes restore direction, so the output matches the pinion. 4. $$i = 48 \times (40/20) = 96$$. Three motor turns give $$3/96 \times 360^\circ = 11.25^\circ$$ at the wheel. 5. Fasteners tight; set screws on flats; wheels not rubbing; caster spins and trails; service loop with a quiet solder joint; battery cannot slide; similar hand drag. Star the set screw and the rub: both leave the encoder happy while the floor disagrees.

## Further reading

- [Gear ratio](https://en.wikipedia.org/wiki/Gear_ratio) — compound trains, which is the gearbox-times-belt case.
- [SDP-SI gear technology](https://www.sdp-si.com/resources/elements-of-metric-gear-technology/index.php) — backlash as a designed gap, in catalog language.
- [diff_drive_controller](https://github.com/ros-controls/ros2_controllers/tree/master/diff_drive_controller) — where your measured $$i$$, $$b$$, and $$r$$ will be typed in.
