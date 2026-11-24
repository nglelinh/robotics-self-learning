---
layout: post
title: "Chapter 06 lab checklist"
chapter: "06"
order: 9
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter06
lesson_type: required
draft: false
---

Estimated time: **50–70 minutes** to assemble the notes you already took and to fill the gaps. This is the chapter gate, not a new mechanism.

At the end of Chapter 06, your robot still has no firmware running—and that is intentional. Experienced roboticists never debug mechanical wobble and software bugs at the same time; they close the mechanical gate first so that when the robot drifts in Chapter 07, they know with certainty whether to reach for a wrench or a keyboard.

## Learning objectives

By the end of this lesson your `lab-notes.md` holds a track width and a rolling radius, an identified screw size, a gear ratio that was predicted and checked, one Grashof or belt or rack calculation, a strain-relief photo or a dated plan, and a list of parts still missing before Chapter 07. You can say, in a sentence, whether you passed on hardware or on a labeled drawing.

## Prerequisites

Lessons 01 through 08. If one of those labs is unfinished, this checklist is the index that tells you which one to reopen. You need the same notebook you have been writing millimeters into.


## Background Knowledge Map: Mechanical Integration Gates, Tolerance Stacking, and Configuration Management

Closing the mechanical chapter builds three disciplined habits used in every real robotics lab:

- **Fault Isolation (Decoupling Mechanical vs. Software Bugs):** If a robot pulls left under equal PWM, the root cause could be wheel-radius mismatch, axle binding, asymmetric gear friction, or a firmware sign bug. Signing off mechanical symmetry *before* writing teleop code eliminates half the search space immediately.
- **Tolerance Stacking & Concentricity:** Small errors across motor brackets, shaft couplings, and wheel hubs add up. Checking runout (wobble), caster load sharing, and fastener retention verifies that the physical assembly matches the ideal kinematic model within acceptable bounds.
- **Single Source of Truth (`lab-notes.md`):** Storing dated, measured values of $$b$$, $$r$$, $$G$$, mass, and CoM location in one versioned note guarantees that Chapter 07 firmware, Chapter 08 kinematics, and Chapter 09 URDF files all share the exact same physical constants.
## Why this matters for Capstone A and the ROS path

Chapter 07 applies voltage to this chassis. Chapter 08 writes the kinematic equations in code. The ROS `diff_drive_controller` and the URDF will copy $$b$$, $$r$$, and $$i$$ from somewhere; the somewhere should be this page, dated, with the method beside the number. A missing caster or a missing nyloc is a shopping line, not a surprise during bring-up. The pass condition is evidence in the notes. A memory of having “basically measured it” does not open Chapter 07.

## The gate

Copy this table into `lab-notes.md` and fill the evidence column with a number, a file name of a photo, or the words “drawing, not hardware.”

| Gate | What “done” looks like | Evidence |
|------|------------------------|----------|
| Track width $$b$$ | Millimeters between tread contact centers | |
| Rolling radius $$r$$ | From $$s/(2\pi)$$, both wheels | |
| Screw identity | M3 called out, nyloc distinguished from a plain nut | Photo |
| Gear ratio | Prediction and a check within about 10 percent, or a labeled paper prediction | |
| Linkage or belt or rack | One Grashof test, or a GT2 tooth ratio, or a rack travel | |
| Strain relief | Before/after photo, or a written plan if no wires exist yet | |
| Missing parts | Explicit list for Chapter 07 assembly | |

Pass, in prose: every row has evidence, the ratio row says how it was checked, and the missing-parts row is either “none” or a list you can buy this week. A drawing-only path passes the reasoning gate. Hardware-ready is a second sentence on the same page, and you write it only when the plate, both wheels, the caster, and both motors have been in your hands for the checks in Lesson 08. Chapter 07 starts from hardware-ready.

![The two lengths the gate will not accept as guesses]({{ site.imgurl }}/generated/chassis_measures.png)

![The ratio the gate wants next to those lengths]({{ site.imgurl }}/generated/gear_train_ratio.png)

## Worked example

A student rolls one wheel $$s = 188$$ mm.

$$
r = \frac{188}{2\pi} \approx 29.9\ \text{mm}.
$$

The other wheel gives 30.4 mm. They record both and use 30.2 mm as a working average only after they reseat the tires and the second test agrees within a millimeter. Track width is $$b = 152$$ mm between contact centers. The gearbox stamp is 1:48, three input turns measured $$23^\circ$$ against a prediction of

$$
\frac{3}{48}\times 360^\circ = 22.5^\circ,
$$

which is about 2 percent high, inside the band. Their Grashof line is the Lesson 04 pair $$s + l = 120$$ mm, $$p + q = 125$$ mm. The strain-relief photo shows a zip tie and a loop. Missing parts: one nyloc bag. That page is a pass on hardware, with a shopping line that does not block a wheels-up spin if two nylocs are already on the motor mounts. It would block a claim that every fastener is done.

### Deep-Dive Explanation (Read Slowly): Quantifying Straight-Line Drift from a 1 mm Wheel-Radius Mismatch

Why does the Chapter 06 gate insist that left and right rolling radii $$r_L, r_R$$ agree within ~1 mm? Let us calculate the open-loop path curvature caused by a tiny radius mismatch.

1. **Setup:** Suppose both wheels spin at the exact same angular rate $$\dot\phi_L = \dot\phi_R = 10\ \text{rad/s}$$, track width is $$b = 0.150\ \text{m}$$, left radius is $$r_L = 0.0310\ \text{m}$$, and right radius is $$r_R = 0.0320\ \text{m}$$ (just a 1.0 mm difference!).
2. **Resulting wheel linear speeds:**
   $$v_L = 10 \times 0.0310 = 0.310\ \text{m/s}, \qquad v_R = 10 \times 0.0320 = 0.320\ \text{m/s}.$$
3. **Induced yaw rate and turning radius:**
   $$v = \frac{0.320 + 0.310}{2} = 0.315\ \text{m/s}, \qquad \omega = \frac{0.320 - 0.310}{0.150} = 0.0667\ \text{rad/s},$$
   $$R = \frac{v}{\omega} = \frac{0.315}{0.0667} = 4.725\ \text{m}.$$
4. **Lateral drift over a 2-meter hallway test:** For small angles, lateral deviation is $$\Delta y \approx \frac{L^2}{2R} = \frac{2.0^2}{2 \times 4.725} = 0.42\ \text{m}$$! Even a 1 mm tire seating error makes an open-loop robot drift 42 cm off centerline in just 2 meters—proving why mechanical verification must precede firmware.

## Lab: fill the gate from evidence you have

### Safety

This session does not apply power. If you repeat a hand spin or a tug test, the battery stays disconnected, as in Lessons 05 and 07. Do not “just tap 5 V” to see if a motor that failed the hand-drag check will free itself.

### BOM

| Item | Role |
|------|------|
| `lab-notes.md` and the photos from this chapter | The evidence |
| Chassis and tools, if you are closing hardware gaps | Only the failed rows |
| Shopping list | The missing-parts row |

### Steps

1. Open the notes from Lessons 01, 02, 03 or 08, 04, and 07. Copy numbers; do not retype them from memory if the original line is still there.
2. Fill the table. Where a photo exists, name the file. Where the kit was late, write “drawing.”
3. Recompute one check in the worked-example style so a transcription error dies here: $$r$$ from $$s$$, or $$\theta_{\text{out}}$$ from $$i$$.
4. Write the pass sentence and, if it is true, the hardware-ready sentence.
5. Turn the missing-parts row into the buy list below. GT2 appears only if your ratio includes a belt.

### Expected results

A completed table and two sentences. A classmate can perform Chapter 07’s mechanical setup from your notes without asking you for $$b$$. Drawing-only notes say so in the pass sentence and list the hardware still required for the second sentence.

### Faults

| What you see | What it usually means |
|--------------|------------------------|
| $$b$$ looks like a round 150 with no method | It was remembered; remeasure between contact centers |
| Ratio with no predicted angle beside it | The check was skipped; run Lesson 08 |
| Hardware-ready claimed from a drawing | Split the two sentences |
| Missing-parts row blank | It is a row, even when the list is “none” |
| One wheel’s $$r$$ missing | Measure it; mismatched radii yaw a straight command |

## Mua ở Việt Nam / Where to buy in Vietnam

Buy only the gaps on your missing-parts row. A complete bench does not need a second chassis “as spare” before Chapter 07. GT2 is on this list only if Lesson 04’s ratio uses a belt.

| Gap | Keywords | Rough band (VND) | When |
|-----|----------|------------------|------|
| Chassis | `khung xe robot 2 bánh` | 80.000–200.000 | No plate yet |
| M3 kit and nylocs | `ốc M3` | 25.000–70.000 | Lesson 02 sort came up short |
| Caster | `bánh caster robot` | 12.000–40.000 | Nose has no trailing wheel |
| GT2 belt and pulley | `dây đai GT2` | 15.000–40.000 for a belt | Only if your drive uses one |

Search pages:

- [Hshop: khung](https://hshop.vn/search?q=khung+xe+robot)
- [Shopee: ốc M3](https://shopee.vn/search?keyword=%E1%BB%91c%20M3)
- [Lazada: bánh caster](https://www.lazada.vn/catalog/?q=b%C3%A1nh%20caster)
- [Thế Giới IC: ốc](https://www.thegioiic.com/search?q=%E1%BB%91c%20M3)

Prices move. Order the missing line before you book a Chapter 07 bench, and keep the receipt next to the notes so the part that arrives is the size you measured.

## Exercises

1. Your roll lengths are 196 mm and 191 mm. Compute both radii. Do you average them yet?
2. Three turns, stamp 1:34, measured output $$33^\circ$$. Prediction, percent error, and pass or revisit?
3. A teammate’s $$b$$ is “the motor spacing, 140 mm.” What do you ask them to remeasure, and which ROS symptom are you avoiding?
4. The strain-relief cell says “later.” Does the reasoning gate pass? Does hardware-ready pass?
5. Write your own pass sentence using the numbers you actually have, including the words “drawing” if that is the truth.

### Answer guidance

1. $$r \approx 31.2$$ mm and $$30.4$$ mm. The split is several millimeters, so you reseat and remeasure before you average. 2. Prediction $$3/34 \times 360^\circ \approx 31.8^\circ$$. Error $$|33-31.8|/31.8 \approx 4$$ percent, inside 10 percent, so the ratio row can pass. 3. Ask for the distance between tread contact centers. You are avoiding a straight `cmd_vel` that drives a circle. 4. Reasoning fails until a photo or a dated written plan exists. Hardware-ready also waits on that plan being executed once wires exist, plus the rest of Lesson 08. 5. The sentence should name $$b$$, $$r$$, $$i$$, the linkage or belt or rack result, and the evidence type. No number you did not take.

## Further reading

- [diff_drive_controller](https://github.com/ros-controls/ros2_controllers/tree/master/diff_drive_controller) — the file where this table’s $$b$$, $$r$$, and wheel ticks-per-revolution eventually go.
- [ROS 1 diff_drive_controller wiki](https://wiki.ros.org/diff_drive_controller) — parameter names in one page. ROS 1 text, same geometry.
- [Nav2 odometry setup](https://navigation.ros.org/setup_guides/odom/setup_odom.html) — the consumer of the odometry those parameters create.
