---
layout: post
title: "Chapter 07 capstone checklist"
chapter: "07"
order: 6
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter07
lesson_type: required
draft: false
---

This is the sign-off for the first moving base. You have evidence for four behaviors, or you have one named repair and you are not starting Chapter 08.

## Learning objectives

1. Judge a lab notebook against four definition-of-done lines: teleop in four directions, stop on host timeout, battery secured with no bare lithium leads, and notes that hold a photo, the protocol, the sign map, and the voltages.
2. Read one failed acceptance (a robot that keeps rolling after the laptop sleeps, or a right wheel that is reversed) and name the single fix that must land before PID or ROS topics.
3. Separate a real pass from a notebook that has the right headings and empty measurements.
4. List only the parts still missing to close this capstone, with the same shops as the rest of the chapter.

## Prerequisites

Lessons 07-01 through 07-05 are the evidence: assembly, wheels-up sign map, `V` and `S`, timeout and slew, floor log. Chapter 05 is the H-bridge, STBY, the 7805 jumper, and the stall current behind the 2–3 A fuse. Chapter 06 is $$b$$ and $$r$$ (examples $$0.15~\mathrm{m}$$ or your $$148~\mathrm{mm}$$, and $$31.2~\mathrm{mm}$$). Chapter 08 is PID. Chapter 09 replaces the text line with a `geometry_msgs/Twist` (`linear.x`, `angular.z`). Neither chapter repairs a missing timeout or a reversed tire. This checklist does not implement ROS.

## Why this matters for Capstone A and the ROS path

PID amplifies the plant. A reversed right wheel turns a positive error into a larger wrong command. A topic graph has the same stuck-PWM bug as serial if firmware keeps the last duty when messages stop. Twist replaces the text line only after the four done-lines below are true. Until Chapter 08 calibrates, PWM 80 is not $$0.2~\mathrm{m/s}$$.

## Definition of done

All four lines are required.

Teleop matches the lesson 02 sign map. Forward is two positive counts inside $$\pm 180$$, both tires toward the nose. Back is both negative. Left spin is `V -60 60` because right-faster is a left yaw. Right spin is `V 60 -60`. The host refreshes at least every $$200~\mathrm{ms}$$.

Host timeout works. After $$250~\mathrm{ms}$$ without a valid line the targets go to 0, and the slew of 15 counts per $$20~\mathrm{ms}$$ walks the duty down. From a last command of 60 that is about $$330~\mathrm{ms}$$, inside the $$0.5~\mathrm{s}$$ you measured with the MCU still on the buck. The battery switch was in your hand on the floor. The switch does not replace the timeout, and the timeout does not replace the switch.

The battery is strapped between the axle and the caster. Lithium is in a holder or a BMS pack, with no dangling soldered bare leads. Positive goes switch, then 2–3 A fuse, then VM and the buck. The buck was $$5.0~\mathrm{V}$$ before the ESP32 was attached. Motor wires are on screws. Battery negative, driver GND, buck GND, and MCU GND are one node.

`lab-notes.md` holds the wiring photo, a protocol snippet (`V`, `S`, 115200 8N1, $$200~\mathrm{ms}$$, $$250~\mathrm{ms}$$), the sign map, unloaded pack voltage, buck output, and $$b$$ and $$r$$. A blank cell is a missing measurement.

## A notebook that fails, and the fix that blocks Chapter 08

Here is a log that must not be signed.

| Time | Command | What the robot did | Voltage | Fault hypothesis |
|------|---------|--------------------|---------|------------------|
| 0:10 | `V 80 80` | straight for 2 s | 8.10 V rest, 7.95 V after | |
| 0:20 | laptop lid closed | kept rolling, hit the far tape | 7.9 V | timeout never written; LEDC held 80 |

The straight row can be fine while the second row is fatal. Chapter 08 and Chapter 09 both stream commands from a host that may die. Until the $$250~\mathrm{ms}$$ test is in the sketch, killing the sender leaves the last duty applied. Put the test back, confirm on the box that `V 60 60` dies within $$0.5~\mathrm{s}$$, then repeat the lane. Unplugging the battery by habit is not the design.

A second fail: `V 80 80` yaws, and the wheels-up photo shows the right flag backward. One inversion only, either the right motor's screws or the right IN polarity, and write which. Both cancels. That wheel is a plant gain of $$-1$$. PID will add effort the wrong way, and Chapter 09 will publish it as if `linear.x` were honest.

A third fail: two 18650 cells with soldered bare leads taped to the plate. A snag shorts upstream of a missing fuse, and the timeout never gets a vote. Fit a holder or a 2S BMS pack, a switch, and a 2–3 A fuse, and photograph them. A TP4056 is still the wrong charger: 1S, full near $$4.2~\mathrm{V}$$, while the pack is full near $$8.4~\mathrm{V}$$.

Sign when a fresh log shows four directions, a stop inside $$0.5~\mathrm{s}$$, resting voltage before and after (a short session might read $$8.15~\mathrm{V}$$ then $$8.05~\mathrm{V}$$), the photo, and the geometry. If the pack fell from $$8.20~\mathrm{V}$$ to $$6.90~\mathrm{V}$$ at $$0.60~\mathrm{A}$$,

$$
R \approx \frac{1.30}{0.60} \approx 2.2~\Omega,
$$

you do not sign. That sag is a supply repair, not a software waiver.

## What Chapter 08 and Chapter 09 are allowed to assume

Chapter 08 may assume positive left and positive right both roll forward, that you have seen PWM 0 stop the robot, and that $$b$$ and $$r$$ are the numbers in the notes. It builds a speed loop. It does not rediscover your IN pins.

Chapter 09 may assume the base stops when the stream stops. Twist will carry `linear.x` and `angular.z` instead of the two PWM integers, converted with Chapter 06's equations and Chapter 08's calibration. Do not write "80 counts = $$0.2~\mathrm{m/s}$$" into the sign-off. The protocol snippet is the spec that adapter has to beat: visible, clamped, and dead-host safe.

![Run only while the command is fresh; silence is stop]({{ site.imgurl }}/generated/teleop_states.png)

If the log cannot point at that STOP box with a measurement, the checklist is not done.

## Lab

### Safety

Repeat the floor sequence only after a failed row is repaired. Otherwise review the paper log. The battery switch stays in reach if the tires can touch the floor. Do not sign a robot you have not stopped with the timeout. Bare lithium leads stop the work.

### BOM

| Item | Role |
|------|------|
| `lab-notes.md` from lessons 01–05 | The evidence |
| Robot, only if a row must be re-run | The retest |
| Meter | Recheck buck 5.0 V and pack voltage if the photo is old |
| This checklist | The four lines you initial |

### Steps

1. Find the wiring photo: switch, fuse, strap, common ground, motor wires on screws, buck near $$5.0~\mathrm{V}$$ before the ESP32 was attached.
2. Initial forward, back, left, and right only where the log words match the commands.
3. Find the timeout row: sender killed or USB unplugged, MCU still on the buck, stop within $$0.5~\mathrm{s}$$. A missing row means the chapter is not done.
4. Find $$b$$, $$r$$, the protocol snippet, and the voltages. Date the moment Chapter 08 may start, or name the one repair that blocks it.
5. A re-run uses the lesson 05 lane. One repair, then the whole sequence, then a new log.

### Expected results

A short sign-off paragraph in the notes: four directions passed on a stated date, stop time you measured, pack voltages, $$b$$, $$r$$, and the sentence "Chapter 08 may start" or a single blocking repair. Empty tables do not count.

### Faults

| What you see | What it usually means |
|--------------|------------------------|
| Headings copied, cells blank | The chapter was not done; fill them from a real run |
| Stop "passes" only by pulling the battery | Timeout was never tested; pull-the-pack is the kill, not the deadline |
| Both leads and firmware were "fixed" | The two inversions cancel; return to one |
| Geometry missing | Chapter 08 will invent a track width |
| PWM 80 written as $$0.2~\mathrm{m/s}$$ | False calibration; delete it before PID |

## Mua ở Việt Nam / Where to buy in Vietnam

Buy only the line that is still empty. Prices move. Rough 2026 bands: chassis 60–150k VND, TT motor 25–45k each, TB6612 25–70k, LM2596 10–25k, 2S pack or 18650 holder 80–180k, switch 8–20k, fuse holder and 2–3 A fuse 10–25k, ESP32 70–150k. L298N substitutes for a missing TB6612. A TP4056 is not a 2S charger.

- Verified L298N, about $$45.000$$ VND: [hshop.vn/mach-dieu-khien-dong-co-dc-l298](https://hshop.vn/mach-dieu-khien-dong-co-dc-l298)
- [Hshop TB6612](https://hshop.vn/search?q=TB6612), [LM2596](https://hshop.vn/search?q=LM2596), [ESP32](https://hshop.vn/search?q=ESP32)
- [Shopee khung 2WD](https://shopee.vn/search?keyword=khung%20xe%202WD), [cầu chì](https://shopee.vn/search?keyword=c%E1%BA%A7u%20ch%C3%AC%202A), [pin 2S](https://shopee.vn/search?keyword=pin%202S%2018650)
- [Lazada TB6612](https://www.lazada.vn/catalog/?q=TB6612), [ESP32](https://www.lazada.vn/catalog/?q=ESP32)
- [Thế Giới IC LM2596](https://www.thegioiic.com/search?q=LM2596), [L298N](https://www.thegioiic.com/search?q=L298N)

## Exercises

1. The log shows a straight `V 80 80` and then a robot that keeps rolling after the laptop sleeps. Which done-line fails, and what exactly has to be true on the box before you touch Chapter 08 or Chapter 09?
2. Four directions passed. The right-hand notes say the leads were swapped and the firmware sign was inverted "to be sure." What does positive PWM do now, and what do you undo?
3. Rest voltage $$8.20~\mathrm{V}$$, loaded $$6.90~\mathrm{V}$$ at $$0.60~\mathrm{A}$$, photo shows bare soldered cell leads. Which done-lines fail, and what is $$R$$?
4. A classmate sets PWM 80 equal to $$0.20~\mathrm{m/s}$$ and scales `V -60 60` the same way, with $$b = 0.15~\mathrm{m}$$. What $$\omega$$ do they falsely get, and why is the slope illegal?
5. From a command of 60 the robot took $$1.2~\mathrm{s}$$ to stop after the sender died. Slew is 15 counts per $$20~\mathrm{ms}$$ and the deadline is $$250~\mathrm{ms}$$. What stop time should you have seen?

### Answer guidance

1. "Stops on host timeout" fails. On the box, `V 60 60` then kill the sender: both tires stop within $$0.5~\mathrm{s}$$ with the MCU still on the buck. Then repeat the lane. 2. The two inversions cancel, so positive still rolls that tire backward. Undo one, wheels up. 3. Bare leads fail the battery line, and $$R \approx 1.30/0.60 \approx 2.2~\Omega$$ fails the supply. Fit a holder or BMS pack, a switch, and a 2–3 A fuse. 4. Slope $$0.20/80 = 0.0025$$ m/s per count makes left $$-0.15$$ and right $$+0.15$$, so $$v = 0$$ and $$\omega = 0.30/0.15 = 2$$ rad/s. The slope was never measured. 5. Expected stop is $$250 + 4\times 20 = 330~\mathrm{ms}$$. A $$1.2~\mathrm{s}$$ roll means the deadline is missing or far longer than $$250~\mathrm{ms}$$. Do not sign.

## Further reading

- [geometry_msgs/Twist (Jazzy)](https://docs.ros.org/en/jazzy/p/geometry_msgs/interfaces/msg/Twist.html)
- [geometry_msgs package index (Jazzy)](https://docs.ros.org/en/jazzy/p/geometry_msgs/)
- [Pololu TB6612FNG](https://www.pololu.com/product/713)
- [ST L298 datasheet](https://www.st.com/resource/en/datasheet/l298.pdf)
