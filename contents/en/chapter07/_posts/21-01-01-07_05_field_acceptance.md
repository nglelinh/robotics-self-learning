---
layout: post
title: "Field test, debug log, and acceptance"
chapter: "07"
order: 5
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter07
lesson_type: required
draft: false
---

The box test is over. This lesson puts the robot on the floor in a clear lane, runs four directions at the clamped PWM, and writes a log that a later chapter can trust. Passing is a set of observations, not a feeling that it "sort of drove."

## Learning objectives

1. Run a scripted floor sequence in a clear $$2~\mathrm{m}$$ lane: forward about $$2~\mathrm{s}$$, stop, back, spin left, spin right, all inside the $$\pm 180$$ clamp, with a hand on the battery switch.
2. Show that killing the sender or unplugging USB, while the MCU stays on the buck, ends motion within $$0.5~\mathrm{s}$$.
3. Record battery voltage before the run and after it, and treat a large sag as a pack, wiring, or fuse problem.
4. Fill a debug log (time, command, what the robot did, voltage, fault hypothesis) and accept the robot only when the sign map, the timeout, the strapped battery, and the Chapter 06 geometry are all in the notes.

## Prerequisites

Lessons 07-01 through 07-04 are the plant: strapped pack, fused positive lead, buck at 5.0 V, sign map, text protocol, slew, and timeout. Chapter 05 is the stall and the hot-driver rule. Chapter 06's $$b$$ and $$r$$ are already in `lab-notes.md` (course examples $$b = 0.15~\mathrm{m}$$ or your $$148~\mathrm{mm}$$, and $$r = 31.2~\mathrm{mm}$$). You still do not publish Twist. You may record distance and time. You may not stamp them onto PWM as a law. Chapter 08 earns m/s.

## Why this matters for Capstone A and the ROS path

Chapter 08's PID assumes the sign is right and that a lost command stops the wheels. A reversed right tire makes the proportional term add the wrong yaw. Chapter 09 assumes the base is safe when the publisher dies, and a sleeping laptop is that publisher. Acceptance is the gate: four directions match the sign map, silence stops the robot, the battery cannot fall off, and the notes hold a wiring photo, the protocol, the voltages, and $$b$$ and $$r$$.

![The geometry the log must cite: $$b$$ between contact centers, $$r$$ from the roll test]({{ site.imgurl }}/generated/chassis_measures.png)

![Forward, spin, and the mixed case you are about to request with PWM, not with m/s]({{ site.imgurl }}/generated/diff_drive_kinematics.png)

The arrows in the second figure are the motions. `V 80 80` is both arrows forward. `V -60 60` is the spin whose right arrow is forward and whose left arrow is back, a left yaw when the sign map is honest. The figure's formulas stay in speed units. Your commands stay in counts.

## A lane, a kill switch, and voltages that move

Clear a $$2~\mathrm{m}$$ lane with no table edge in the braking space. Hold the battery switch. Host refresh $$200~\mathrm{ms}$$, firmware deadline $$250~\mathrm{ms}$$, duties at 60 or 80, not 255.

Sequence, each command refreshed until you ask for the next:

1. `V 80 80` for about $$2~\mathrm{s}$$, both tires forward, robot tracks the lane.
2. `V 0 0` or simply stop refreshing and let the timeout fire. The robot stops.
3. `V -80 -80` for about $$2~\mathrm{s}$$, straight back.
4. `V -60 60` for a short spin. The nose goes left.
5. `V 60 -60` for a short spin. The nose goes right.

Then kill the sender, or unplug USB while the ESP32 stays on the buck. Motion ends within $$0.5~\mathrm{s}$$. Lesson 04 predicts about $$330~\mathrm{ms}$$ after a last `V 60 60`. Three seconds of rolling is a fail, even if the directions looked fine.

Resting voltage before and after: a healthy short run might move from $$8.15~\mathrm{V}$$ to $$8.05~\mathrm{V}$$. If you can measure under load, take $$8.20~\mathrm{V}$$ at rest and $$6.90~\mathrm{V}$$ at about $$0.60~\mathrm{A}$$:

$$
R \approx \frac{1.30}{0.60} \approx 2.2~\Omega.
$$

About $$2.2~\Omega$$ is huge next to a few hundred milliohms. Suspect tired cells, thin wire, a warming polyfuse, or a holder. Fix that before you accept the base. A bad fuse shows up as sag, a trip, or a mid-lane reset. `setup` already writes PWM 0 before STBY rises.

A timed leg is an observation only. Covering $$1.6~\mathrm{m}$$ in $$4.0~\mathrm{s}$$ is

$$
v_{obs} = \frac{1.6}{4.0} = 0.40~\mathrm{m/s}
$$

on that run, that floor, that duty. Write "at PWM 80, this run, about $$0.40~\mathrm{m/s}$$." Do not write "PWM 80 means $$0.40~\mathrm{m/s}$$" as a Twist constant.

## The log is the acceptance instrument

Each row is one event. The hypothesis column stays empty when the event matched the sign map. It is mandatory when something else happened.

| Time | Command | What the robot did | Voltage | Fault hypothesis |
|------|---------|--------------------|---------|------------------|
| 0:00 | rest | stopped, pack strapped | 8.15 V | |
| 0:12 | `V 80 80` for 2 s | straight along the lane | 7.9 V under load | |
| 0:15 | sender killed | stopped in well under 0.5 s | 8.12 V | |
| 0:30 | `V -60 60` | nose left | 8.0 V | |
| 0:40 | `V 60 -60` | nose right | 8.0 V | |

Do not average a bad row into a pass. If the sender dies and the robot rolls into the tape, the timeout was never coded and the last PWM stayed in LEDC. Put lesson 04's check back, prove the box stop, then repeat the lane. If `V 80 80` yaws, one sign is wrong: swap that motor's leads or the firmware polarity, not both. Chapter 08 does not start while either row is still open.

Pass means all of these: four directions match the sign map; the timeout stop works; the battery is strapped, with no bare soldered lithium leads; the notes include the wiring photo, a protocol snippet (`V`, `S`, $$200~\mathrm{ms}$$, $$250~\mathrm{ms}$$), the sign map, the voltages, and $$b$$ and $$r$$.

## Lab

### Safety

The lane is clear for $$2~\mathrm{m}$$ plus room to stop, and you hold the battery switch. Duties stay at the practice values. If the robot heads for a person or a drop, open the switch. A wall stall is one second, then the switch. A smell or a tab you cannot touch ends the session.

### BOM

| Item | Role |
|------|------|
| Accepted power tree and firmware | Lessons 01–04 |
| Clear floor, tape at $$2~\mathrm{m}$$ | The lane |
| Multimeter | Before and after voltage |
| `lab-notes.md` | The log |
| Battery switch in your hand | The kill |

### Steps

1. Confirm wheels are back on, caster down, pack strapped, photo already in the notes. Read the resting voltage.
2. Stand with the switch. Run forward about $$2~\mathrm{s}$$, stop, back, spin left, spin right. Speak the command as you send it so the log stays honest.
3. Kill the sender or unplug USB with the buck still powering the ESP32. Time the stop. It must be within $$0.5~\mathrm{s}$$.
4. Read the resting voltage again. If you saw a deep sag under load, estimate $$R$$ and write the hypothesis.
5. Mark pass or fail against the four criteria. A fail points at one repair, then a full repeat.

### Expected results

A filled log, a stop inside half a second, resting voltages that did not collapse, and the word pass only if directions, timeout, battery, and notes (photo, protocol, sign map, $$b$$, $$r$$) are all present. An observed speed may appear as a labeled observation. It is not wired into the protocol.

### Faults

| What you see | What it usually means |
|--------------|------------------------|
| Straight command draws a circle | One sign is still flipped; one fix only |
| Keeps rolling after the laptop sleeps | Timeout not in the sketch |
| Nose lifts as it accelerates | Pack mass is behind the axle; return to lesson 01 |
| Voltage sags by a volt or more at modest current | Cells, holder, wire, or polyfuse |
| Stop works only when USB unplug also resets the chip | Buck was not the logic supply; retest with the MCU still powered |

## Mua ở Việt Nam / Where to buy in Vietnam

Acceptance often fails on a missing strap, a tired holder, or a fuse you never bought. Prices move. Rough 2026 bands: 2S pack or holder 80–180k VND, switch 8–20k, fuse holder and 2–3 A fuse 10–25k, LM2596 10–25k, TB6612 25–70k. A verified L298N at about 45.000 VND is only the substitute bridge. Do not buy a new chassis to avoid swapping one motor lead.

- Verified L298N, about $$45.000$$ VND: [hshop.vn/mach-dieu-khien-dong-co-dc-l298](https://hshop.vn/mach-dieu-khien-dong-co-dc-l298)
- [Hshop cầu chì](https://hshop.vn/search?q=cau+chi), [LM2596](https://hshop.vn/search?q=LM2596)
- [Shopee pin 2S](https://shopee.vn/search?keyword=pin%202S%2018650), [công tắc](https://shopee.vn/search?keyword=c%C3%B4ng%20t%E1%BA%AFc%20ngu%E1%BB%93n)
- [Lazada holder 18650](https://www.lazada.vn/catalog/?q=holder%2018650%202S)
- [Thế Giới IC cầu chì](https://www.thegioiic.com/search?q=cau%20chi)

## Exercises

1. Resting pack $$8.20~\mathrm{V}$$, under both motors $$6.90~\mathrm{V}$$ at about $$0.60~\mathrm{A}$$. Estimate $$R$$. Is that a passable supply or a sag you stop for?
2. The forward leg covers $$1.6~\mathrm{m}$$ in $$4.0~\mathrm{s}$$ at PWM 80. What observed speed do you write, and what sentence are you forbidden to write into the Twist notes?
3. USB is unplugged, the ESP32 is still on the buck, and the robot rolls for about $$3~\mathrm{s}$$. Which acceptance line fails, and which lesson's code is missing?
4. The robot drove the lane, and the notes have voltages and a photo, but $$b$$ and $$r$$ are blank. Why is that still a fail before Chapter 08?
5. `V 60 -60` yaws the nose left. Name the single repair. What second change would cancel it?

### Answer guidance

1. $$R \approx 1.30/0.60 \approx 2.2~\Omega$$. That is huge next to a healthy pack at a few hundred milliohms. Stop, and suspect cells, a holder, thin wire, or a warming polyfuse. 2. $$v_{obs} = 1.6/4.0 = 0.40~\mathrm{m/s}$$ for this run only. You do not write "PWM 80 = $$0.40~\mathrm{m/s}$$" as a converter constant. Chapter 08 calibrates. 3. The timeout stop fails. Lesson 04's $$250~\mathrm{ms}$$ deadline is missing or not reached, so the last PWM stays. 4. Chapter 08's kinematics and PID need the track width and the rolling radius. A blank geometry means the controller will invent $$b$$. Acceptance asked for those numbers from Chapter 06. 5. Swap the right motor leads or the right firmware sign, one of them. Doing both returns the left yaw. Then repeat the four directions.

## Further reading

- [geometry_msgs/Twist (Jazzy)](https://docs.ros.org/en/jazzy/p/geometry_msgs/interfaces/msg/Twist.html)
- [Pololu TB6612FNG](https://www.pololu.com/product/713)
- [ST L298 datasheet](https://www.st.com/resource/en/datasheet/l298.pdf)
- [pySerial short introduction](https://pyserial.readthedocs.io/en/latest/shortintro.html)
