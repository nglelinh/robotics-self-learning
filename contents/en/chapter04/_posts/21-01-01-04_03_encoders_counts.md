---
layout: post
title: "Encoders and raw odometry counts"
chapter: "04"
order: 3
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter04
lesson_type: required
draft: false
---

Estimated time: **75–90 minutes**, most of it one careful hand revolution and the arithmetic that turns the count into meters.

## Learning objectives

By the end of this lesson you can look at the two square waves from a quadrature encoder and say which channel leads, which is how you tell forward from reverse. You can refuse a seller’s “PPR” until you have measured counts per output-shaft revolution with the same decoding your firmware will use. You can turn a count into arc length for a 65 mm wheel, and you can turn a pair of wheel distances into a dead-reckoning step: how far the axle midpoint moved, and by how many radians the heading changed. Those two numbers are what a later `nav_msgs/Odometry` message is built from.

## Prerequisites

You can count edges on a GPIO and print them (Chapter 03), and you can tell a Hall puck on a yellow TT gearbox from a slotted disk (Lesson 04-02). A raw encoder is not the I2C bus from Lesson 04-01; UART is only how the count will leave the board. Use the Chapter 01 multimeter on the encoder’s high level before that wire touches a GPIO. You do not need ROS, and you do not need the wheels powered.

## Why this matters for Capstone A and the ROS path

Capstone A in Chapter 07 is differential-drive teleop over a serial line, with a timeout that stops the motors. That demo can roll with no encoders at all. The acceptance log is stronger if the same run also records a wheel count, because “it moved” becomes a number you can compare with a tape. The conversion you practice today is the one that log needs.

`diff_drive_controller` does not invent a new geometry. Firmware, or a ros2_control hardware interface, turns counts into a wheel angle using $$N$$, the counts per revolution after decoding. The controller turns that angle into meters with `wheel_radius` (this lesson’s $$r$$) and into a yaw with `wheel_separation` (the track $$b$$). It publishes `nav_msgs/Odometry`. A doubled $$N$$ makes that odometry report half the hallway even when the radius is right. `sensor_msgs/JointState` is the same counts as a wheel position in radians. Get $$N$$ from the wheel in your hand, not from a product title.

![Quadrature channels A and B: the leading edge is the direction]({{ site.imgurl }}/generated/encoder_quadrature.png)

## Two square waves

A quadrature encoder puts out two square waves, A and B, about a quarter cycle apart. Direction is which edge leads. A rule you still have to check on your own hardware: if A rises while B is low, call the step forward; if B rises while A is low, call it reverse. Swapping the two wires swaps the sign. That is wiring, not a filter problem.

A single channel has no partner. Speed from that pin is trustworthy only while the motor command already supplies the sign, and it lies when the wheel coasts or the shaft kicks back during braking.

## What “PPR” might mean

Sometimes PPR means cycles per revolution of one channel: one high and one low, one slot. Sometimes it means counts after decoding. Four-times (4×) decoding counts every edge of both channels, so

$$
N \approx 4 \times (\text{cycles per revolution of one channel}).
$$

Many yellow TT motors put the magnetic disk on the motor shaft, behind the gearbox. Listings often say 11 pulses times a gear ratio, or a Hall count “per shaft revolution,” without naming which shaft. Eleven rising edges per motor turn, counted 1×, through a 1:48 gearbox, produce

$$
N = 11 \times 48 = 528
$$

counts per output-shaft revolution. Use 11 in the distance formula and every published meter is 48 times too long. The honest $$N$$ is a marked tire, turned by hand, through the decoder your code actually runs.

## Distance per count

Without slip, one revolution moves the contact patch by $$2\pi r$$:

$$
\Delta s = \frac{2\pi r}{N}\Delta c.
$$

A wheel of diameter 65 mm has $$r = 0.0325~\mathrm{m}$$ and circumference

$$
2\pi r \approx 2 \times 3.1416 \times 0.0325 = 0.2042~\mathrm{m}.
$$

If this wheel is a simple slot disk and the firmware counts $$N = 20$$ edges per output revolution, one count is

$$
\frac{0.2042}{20} = 0.01021~\mathrm{m} \approx 1.021~\mathrm{cm}.
$$

One hundred forty counts have moved

$$
\Delta s = 140 \times 0.01021 \approx 1.43~\mathrm{m}.
$$

That $$N = 20$$ is a teaching disk, not a promise about a TT listing. If your hand revolution prints 360, or 528, or 1440, that integer replaces 20.

## One dead-reckoning step

The same pair shows up in Chapter 06 and inside the controller:

$$
\Delta s = \frac{\Delta s_r + \Delta s_l}{2}, \qquad \Delta \theta = \frac{\Delta s_r - \Delta s_l}{b}.
$$

$$b$$ is the track between contact patches, not a wheel diameter. With $$\Delta s_r = 0.10~\mathrm{m}$$, $$\Delta s_l = 0.06~\mathrm{m}$$, and $$b = 0.15~\mathrm{m}$$,

$$
\Delta s = \frac{0.10 + 0.06}{2} = 0.08~\mathrm{m}, \qquad \Delta \theta = \frac{0.04}{0.15} = 0.267~\mathrm{rad} \approx 15.3^\circ.
$$

The axle crept 8 cm and yawed about 15 degrees toward the slower wheel. Slip is absent from the formula. Swap A and B on the right encoder only, and the log shows $$\Delta s_r = -0.10~\mathrm{m}$$ for a tire that went forward. The exercises compute how bad that sign error gets.

## Lab: one revolution, in the hand

### Safety

Do not power the motors for the counting pass. A TT wheel on a bench will walk. If you already own a driver and you want a powered direction check, put both tires in the air, use a short pulse, and keep fingers off the spokes. If the Hall high level measures 5 V, it needs the same 1 kΩ / 2 kΩ divider Lesson 04-02 used for an echo pin before it may touch an ESP32 GPIO. Measure the high level first.

### BOM

| Item | Role |
|------|------|
| One geared motor with an encoder, or a loose slot disk | The shaft you turn |
| ESP32 or Pico | Edge counter |
| Marker | The index mark on the tire |
| Notebook | $$N$$, radius, meters per count |
| Driver and battery | Optional in-air direction check only |

### Steps

1. Mark the tire and a matching point on the gearbox. That pair is one revolution.
2. Leave the motor unpowered. Reset the counter.
3. Turn the output shaft by hand through one revolution, back to the marks. Write the count. Repeat twice. The three integers should agree within one count.
4. That integer is $$N$$ for the decoding you just ran. Compute $$2\pi r / N$$ with the tire you marked. The 1.021 cm figure appears only when $$N = 20$$ and the diameter is 65 mm.
5. Still unpowered, watch which channel rises first while you turn the tire the way the robot would roll forward. A logic analyzer is ideal. Printing “A rise” and “B rise” is enough. One channel means you write “sign comes only from the motor command.”
6. Optional, wheels off the ground: a brief powered spin should make the same channel lead. If it does not, swap A and B in the notes and repeat once.

### Expected results

Three hand revolutions, one agreed $$N$$, a distance-per-count in meters, and one sentence on which channel leads for forward. Paste that block into `lab-notes.md`. A Chapter 07 line such as “140 counts, about 1.43 m” is allowed only when your measured $$N$$ really is 20.

### Faults

| What you see | What it usually is |
|--------------|--------------------|
| Count doubles after a decode-mode change | You moved from 1× to 2× or 4× and kept the old $$N$$ |
| Listing says 40 PPR, hand turn says 20 | The listing counted edges your code does not count |
| Forward command decreases the count | A and B are swapped, or the motor wires are backwards; change one |
| Count climbs while the wheel is still | Bounce, a floating pin, or no common ground |
| Distance looks tens of times too long | $$N$$ is pulses per motor turn; the gearbox was left out |

## Mua ở Việt Nam / Where to buy in Vietnam

Buy a pair of TT gearmotors that already include a Hall encoder, so both wheels share a gearbox. Prices move.

| Part | Keywords | Rough band (VND) | Substitute |
|------|----------|------------------|------------|
| TT motor with Hall encoder | `động cơ TT encoder Hall` | 40.000–90.000 each | N20 with encoder if the hole and the shaft (3 mm or 4 mm) match the chassis |
| Slot disk and optical pair | `đĩa encoder quang` | 15.000–40.000 | Fine for learning $$N$$, awkward as the Capstone drive |
| 1 kΩ and 2 kΩ | `điện trở 1k 2k` | 10.000–20.000 a strip | Only if the Hall high level measures 5 V |

- [Hshop: động cơ encoder](https://hshop.vn/search?q=dong%20co%20encoder)
- [Shopee: động cơ TT encoder](https://shopee.vn/search?keyword=dong%20co%20TT%20encoder)
- [Lazada: encoder Hall TT](https://www.lazada.vn/catalog/?q=encoder%20Hall%20TT)
- [Thế Giới IC: encoder](https://www.thegioiic.com/search?q=encoder)

Read which shaft the listing’s pulse count belongs to. Then check it with the hand revolution.

## Exercises

Use $$r = 0.0325~\mathrm{m}$$ and circumference $$\approx 0.2042~\mathrm{m}$$ unless a problem says otherwise.

1. $$N = 20$$ counts per output revolution. How far does the wheel roll in 140 counts?
2. A hand revolution of that same firmware produced 20 counts, but the student enters the seller’s “40 PPR” as $$N$$. What distance do they report for 140 counts, and what is the true distance?
3. The tires really moved $$\Delta s_r = 0.10~\mathrm{m}$$ and $$\Delta s_l = 0.06~\mathrm{m}$$, with $$b = 0.15~\mathrm{m}$$. A and B on the right encoder are swapped, so the log shows $$-0.10~\mathrm{m}$$ and $$+0.06~\mathrm{m}$$. Compute the reported $$\Delta s$$ and $$\Delta \theta$$, against the true $$0.08~\mathrm{m}$$ and $$0.267~\mathrm{rad}$$.
4. One channel counts 80 rising edges forward and 80 more as the wheel rolls back to the start. For that channel, $$N = 20$$. What net distance does quadrature report, and what distance do you get if you treat all 160 edges as forward?
5. A TT motor gives 11 rising edges per motor-shaft turn through a 1:48 gearbox, and your code counts those edges (1×) on the wheel shaft’s output. What is $$N$$? If someone uses 11, by what factor is every distance too large?

### Answer guidance

1. $$0.01021~\mathrm{m}$$ per count, times 140, is $$1.43~\mathrm{m}$$. 2. $$N = 40$$ reports $$0.715~\mathrm{m}$$, half of the true $$1.43~\mathrm{m}$$. 3. Reported $$\Delta s = -0.02~\mathrm{m}$$ and $$\Delta \theta = -1.067~\mathrm{rad}$$ (about $$-61^\circ$$), instead of $$+0.08~\mathrm{m}$$ and $$+15.3^\circ$$. 4. Quadrature net count is 0, so net distance is 0. Treating 160 edges as forward gives $$1.63~\mathrm{m}$$. 5. $$N = 528$$. Using 11 stretches every distance by 48.

## Further reading

- [SparkFun rotary encoder hookup](https://learn.sparkfun.com/tutorials/rotary-encoder-breakout-hookup-guide/all) — which edge leads, and why one channel is only a speed hint.
- [Pololu magnetic encoder pair](https://www.pololu.com/product/3081) — a datasheet that names counts per motor-shaft revolution, which you still multiply by the gearbox.
- [`nav_msgs/Odometry`](https://docs.ros.org/en/humble/p/nav_msgs/msg/Odometry.html) — the pose is the sum of dead-reckoning steps like the one above.
- [`diff_drive_controller`](https://control.ros.org/humble/doc/ros2_controllers/diff_drive_controller/doc/userdoc.html) — `wheel_radius` and `wheel_separation` are $$r$$ and $$b$$; $$N$$ belongs in the hardware interface that feeds wheel position.
