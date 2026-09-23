---
layout: post
title: "Teleop over serial: protocol design"
chapter: "07"
order: 3
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter07
lesson_type: required
draft: false
---

Lesson 02 defined what a positive number does to each tire. This lesson names the bytes. The firmware loop is lesson 04.

## Learning objectives

1. Specify a UTF-8, newline-terminated text protocol at 115200 8N1: `V <left> <right>` with integer wheel commands, and `S` as an emergency stop.
2. State the clamp that firmware will apply, $$-180$$ to $$+180$$, and explain why the learning range is not the full $$0$$–$$255$$ duty.
3. Require a host refresh at least every $$200~\mathrm{ms}$$ against a firmware deadline of $$250~\mathrm{ms}$$, so silence becomes PWM 0 rather than a latched command.
4. Reject a malformed line entirely, and show with five concrete frames which motion each legal line requests under the lesson 02 sign convention.

## Prerequisites

Lesson 07-01 is a powered chassis with a common ground and no PWM habit yet. Lesson 07-02 is a written sign map: positive command, both tires toward the nose, corrected by one inversion method only. Chapter 05's H-bridge is how those signs become voltage. Chapter 06's geometry is still

$$
v = \frac{v_r + v_l}{2}, \qquad \omega = \frac{v_r - v_l}{b},
$$

with $$b$$ the track you measured (example $$b = 0.15~\mathrm{m}$$, $$r = 31.2~\mathrm{mm}$$). You can open a serial monitor. Lesson 04 writes the parser. You are not publishing ROS topics.

## Why this matters for Capstone A and the ROS path

Teleop is the first closed conversation with the two motors. Text is the conversation you can read in a serial monitor; binary can wait until the line is boring and correct. Later the same idea is a `geometry_msgs/Twist`: `linear.x` is forward speed, `angular.z` is yaw rate, and a driver splits them with the equations above. In this chapter the integers are PWM counts, not m/s. Chapter 08 calibrates. Writing "`V 80 80` means $$0.2~\mathrm{m/s}$$" is a false calibration.

![A legal `V` line runs; age over 250 ms or an `S` line stops]({{ site.imgurl }}/generated/teleop_states.png)

Read the figure as the contract. IDLE is motors off, waiting. A valid `V` line enters RUN and refreshes a deadline. STOP is command age greater than $$250~\mathrm{ms}$$, or a line that is `S`. PWM goes to 0. A new valid `V` may return to RUN. Silence must not leave the last duty running.

## The bytes, the clamp, and the deadline

Port settings are 115200 baud, 8 data bits, no parity, 1 stop bit. Each line is UTF-8 text ending in a newline, `\n`. A carriage return before the newline is noise the parser may strip; it is not a second command.

`V <left> <right>` carries two integers. Firmware in the next lesson clamps each of them into $$-180..180$$. The cap is deliberate. Full-scale 255 on a fresh 2S pack is a jump you have not earned, and lesson 02's first spins lived at 60–80. One hundred eighty counts is

$$
D = \frac{180}{255} \approx 0.706
$$

of the bridge supply, which is plenty for a floor test and still short of a hard start into a wall. `S` sets both targets to 0 immediately as an emergency stop. `V 0 0` is also a stop, requested as an ordinary command rather than as a panic.

The host sends a fresh line at least every $$200~\mathrm{ms}$$ while it wants motion. Firmware treats $$250~\mathrm{ms}$$ without a valid `V` or `S` as a dead host and forces the targets to 0. The $$50~\mathrm{ms}$$ gap covers a late USB packet, not a laptop that slept. Silence means PWM 0. A duty that stays at 80 after the cable goes quiet is a broken deadline.

A line that does not match is ignored: previous legal targets stay until the deadline, and garbage must not become a spin. `V 80` is missing a wheel. `V 80 foo` is not a zero on the right. The letter is `V`, not `v`.

## Worked frames under one sign convention

Positive on a wheel is forward, the nose direction from lesson 02. Right faster than left is a left yaw, the same sign as Chapter 06, because

$$
\omega = \frac{v_r - v_l}{b}
$$

is positive when $$v_r > v_l$$. The symbols in that display are speeds. The numbers in the frames below are PWM counts. The sign pattern matches. The units do not.

| Line | Left PWM | Right PWM | What you asked |
|------|----------|-----------|----------------|
| `V 80 80` | $$+80$$ | $$+80$$ | Both forward, straight |
| `V -80 -80` | $$-80$$ | $$-80$$ | Both backward |
| `V -60 60` | $$-60$$ | $$+60$$ | Spin left (right tire forward, left tire back) |
| `V 0 0` | $$0$$ | $$0$$ | Stop |
| `S` | targets 0 | targets 0 | Emergency stop |

`V 60 -60` is the opposite yaw, a spin to the right, when the sign map is honest. A forgotten inversion from lesson 02 yaws the wrong way. Fix it there, once.

Count `V -60 60\n`: `V`, space, `-`, `6`, `0`, space, `6`, `0`, newline, nine bytes. At 115200 8N1 each byte is 10 bit-times:

$$
t \approx \frac{9 \times 10}{115200} \approx 0.78~\mathrm{ms}.
$$

The wire time is under a millisecond. The $$200~\mathrm{ms}$$ refresh exists so firmware can notice a dead host. Binary would not have made the UART the bottleneck, and you would lose the ability to type `S`.

Do not pretend the body-speed formula has already been measured. Forcing PWM 80 to mean $$0.20~\mathrm{m/s}$$ on both wheels gives

$$
v = \frac{0.20+0.20}{2} = 0.20~\mathrm{m/s}, \qquad \omega = 0,
$$

the arithmetic is tidy and the physics is invented. Chapter 08 may time a measured meter and only then claim a speed. Until then, `V 80 80` means forward on the sign map, at 80 counts.

## Lab

### Safety

You are typing, not driving. If an old sketch is still flashed and a motor lead is attached, open the battery switch before the serial monitor. The deliverable is five lines. Lesson 04 is the first sketch that acts on them, wheels up.

### BOM

| Item | Role |
|------|------|
| `lab-notes.md` and a pen, or a serial monitor | Where the five frames go |
| Sign map from lesson 07-02 | The meaning of positive |
| Optional ESP32, USB, no VM | So you can see characters echo |
| Calculator | The 9-byte timing check |

### Steps

1. Write the port line in the notes: 115200 8N1, UTF-8, newline terminated, clamp $$-180..180$$, host period $$200~\mathrm{ms}$$, firmware deadline $$250~\mathrm{ms}$$.
2. Under your sign map, write the five frames: `V 80 80`, `V -80 -80`, `V -60 60`, `V 0 0`, `S`. Next to each, write straight, back, spin left, stop, emergency stop.
3. Invent two illegal lines, for example `V 80` and `V 80 foo`. Next to each write "ignore, do not spin one wheel."
4. If you open a monitor, type the five legal lines and confirm you can read them. Do not enable the driver.
5. Compute the transmit time of `V -60 60\n` the way the worked example did, and file it beside the $$200~\mathrm{ms}$$ rule so the two timescales stay distinct.

### Expected results

The notes contain the five frames, the sign sentence "positive is forward on both wheels," the clamp, both times ($$200~\mathrm{ms}$$ host, $$250~\mathrm{ms}$$ firmware), and an explicit remark that PWM counts are not meters per second. A photo of the monitor is optional. A moving robot is not a result of this lesson.

### Faults

| What you see | What it usually means |
|--------------|------------------------|
| `V -60 60` described as spin right | The sign convention was flipped; right-faster is left yaw |
| A single number accepted as left-only | The grammar is being half-applied; ignore the whole line |
| Deadline written as 2 s "to be safe" | A sleep then drives the robot for seconds; use $$250~\mathrm{ms}$$ |
| `V 80 80` labeled $$0.2~\mathrm{m/s}$$ | False calibration; Chapter 08 has not happened |
| Binary struct copied from a blog | You cannot type it, and you cannot see it fail |

## Mua ở Việt Nam / Where to buy in Vietnam

This lesson adds no required part. If you still have no ESP32 to type against, the devkit is the gap. Prices move. Rough 2026 band: ESP32 devkit $$70.000$$–$$150.000$$ VND. A CP2102 or CH340 board is fine. A Pico is a substitute only if you already rewrote the later sketch's LEDC calls; this course's lesson 04 is Arduino-ESP32. Do not buy a second motor driver to "make the protocol faster."

- Verified L298N, about $$45.000$$ VND, only if you still lack a bridge: [hshop.vn/mach-dieu-khien-dong-co-dc-l298](https://hshop.vn/mach-dieu-khien-dong-co-dc-l298)
- [Hshop ESP32](https://hshop.vn/search?q=ESP32)
- [Shopee ESP32](https://shopee.vn/search?keyword=ESP32%20devkit)
- [Lazada ESP32](https://www.lazada.vn/catalog/?q=ESP32)
- [Thế Giới IC ESP32](https://www.thegioiic.com/search?q=ESP32)

## Exercises

1. How many bytes are in `V -60 60\n`, and how long is that frame at 115200 8N1?
2. The last legal line is at $$t = 0$$. The laptop sleeps. At what time must firmware force the targets to 0, and why was the host supposed to speak every $$200~\mathrm{ms}$$?
3. The monitor receives `V 80` and then `V 200 -90`. Which line is illegal, and what clamp will lesson 04 apply to the legal one?
4. Under the sign convention, why is `V -60 60` a left spin? Using $$b = 0.15~\mathrm{m}$$ only as a symbol check, what is the sign of $$(\mathrm{right} - \mathrm{left})$$, and why is the result still not a yaw rate in rad/s?
5. A friend packs the same two integers as two `int16` bytes "to be faster." What do you lose in the serial monitor, and does the $$0.78~\mathrm{ms}$$ frame time justify it?

### Answer guidance

1. Nine bytes (`V`, space, `-`, `6`, `0`, space, `6`, `0`, `\n`). Time $$\approx 9 \times 10 / 115200 \approx 0.78~\mathrm{ms}$$. 2. Targets go to 0 at $$250~\mathrm{ms}$$. The host period of $$200~\mathrm{ms}$$ leaves about $$50~\mathrm{ms}$$ of slack so a late but living host does not trip the stop. 3. `V 80` is illegal and ignored. `V 200 -90` is legal and will be clamped to $$180$$ and $$-90$$. 4. Left command $$-60$$, right $$+60$$, so the right tire is forward and the left tire is backward: nose yaws left. The difference $$(\mathrm{right}-\mathrm{left})$$ is positive, matching the sign of $$\omega$$ in Chapter 06, but both numbers are PWM counts. Dividing by $$b$$ does not create rad/s. 5. You lose the ability to see and type the command. The text frame is already under $$1~\mathrm{ms}$$, far below the $$200~\mathrm{ms}$$ refresh, so binary does not fix liveness.

## Further reading

- [Arduino `Serial`](https://www.arduino.cc/reference/en/language/functions/communication/serial/)
- [pySerial short introduction](https://pyserial.readthedocs.io/en/latest/shortintro.html)
- [geometry_msgs/Twist (Jazzy)](https://docs.ros.org/en/jazzy/p/geometry_msgs/interfaces/msg/Twist.html)
- [geometry_msgs package index (Jazzy)](https://docs.ros.org/en/jazzy/p/geometry_msgs/)
