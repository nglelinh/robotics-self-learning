---
layout: post
title: "Lab: ultrasonic and Time-of-Flight ranging"
chapter: "04"
order: 5
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter04
lesson_type: required
draft: false
---

Estimated time: **80–100 minutes**. This is the ranging lab: a meterstick, a cardboard target, and a table of errors. Wheels stay off the bench.

## Learning objectives

You will compute distance from an echo pulse width with $$d = vt/2$$ at $$343~\mathrm{m/s}$$, and with the microsecond shortcut $$d_{\mathrm{cm}} \approx t_{\mu\mathrm{s}} \times 0.01715$$. You will bring a 5 V HC-SR04 echo down to about 3.33 V before it touches an ESP32 pin, and you will say what a missing echo means (unknown, not zero centimeters). You will explain why two unmodified VL53L0X boards both at `0x29` cannot share a bus, and you will fill a 20 / 40 / 80 cm error table against tape, or a dry-run sheet that still contains the 5.8 ms example and the divider.

## Prerequisites

Lesson 04-02 identified the two cans and the tiny black window, including the voltage and the bus. Lesson 04-01 is the I2C scan you will need if a VL53L0X is on the bench. Chapter 03 can time a pulse or at least print a number from a library you have read. Chapter 01 is the multimeter on the echo pin. You do not need the motor chapter, and you should not be holding a wheel.

## Why this matters for Capstone A and the ROS path

Chapter 07’s teleop firmware is allowed to drive only because something can tell it to stop. On Capstone A that something is a range check in the same loop as the motor command: too close, or no reading, and the PWM goes to zero. The number in that comparison is born here, at a meterstick, not inside a ROS node.

Later the same reading is a `sensor_msgs/Range`: `radiation_type` ultrasonic or infrared, `min_range` and `max_range` set from what you actually trust, and `range` in meters. A 0 in that field must not mean “the wall is touching the bumper” if your HC-SR04 code uses 0 for a timeout. Write the sentinel down now. Two VL53L0X units become two range topics only after XSHUT has given them two addresses. A camera does not replace this lab. The robot has to stop before it can see.

![Round-trip echo time, and a ToF reading already in millimeters]({{ site.imgurl }}/generated/range_echo_tof.png)

## Sound goes out and comes back

An HC-SR04 burst travels to the target and back, so the distance is half the path:

$$
d = \frac{v t}{2}.
$$

At room temperature take $$v \approx 343~\mathrm{m/s}$$. An echo that stays high for $$5.8~\mathrm{ms} = 0.0058~\mathrm{s}$$ gives

$$
d = \frac{343 \times 0.0058}{2} = 343 \times 0.0029 = 0.995~\mathrm{m} \approx 99.5~\mathrm{cm}.
$$

Divide $$343 / 2$$ by $$10^{6}$$ to work in microseconds and centimeters:

$$
d_{\mathrm{cm}} \approx t_{\mu\mathrm{s}} \times 0.01715.
$$

Check the same pulse: $$5800 \times 0.01715 = 99.5~\mathrm{cm}$$. One centimeter of range is about $$58~\mu\mathrm{s}$$ of echo. A timer that jitters by $$100~\mu\mathrm{s}$$ already moves the reading by roughly $$1.7~\mathrm{cm}$$. That is a useful size when your 40 cm station is off by a centimeter and you are tempted to blame the meterstick.

Speed of sound rises about $$0.6~\mathrm{m/s}$$ per degree Celsius. The 343 figure is a 20 °C number. At 30 °C, $$v \approx 349~\mathrm{m/s}$$, and a formula that still multiplies by 0.01715 reads a true 80 cm target a little short. The exercise at the end makes you compute how short. For this lab, stay with 343 and write the room temperature next to the table if you know it.

## HC-SR04, the pulse, and the pin it must not touch

VCC is 5 V. You raise TRIG for about $$10~\mu\mathrm{s}$$. The module emits a short 40 kHz burst and raises ECHO until the echo returns. On the common board, ECHO high is 5 V. An ESP32 GPIO is not a 5 V input. A divider with $$1~\mathrm{k}\Omega$$ from ECHO to the pin and $$2~\mathrm{k}\Omega$$ from the pin to ground sets

$$
V_{\mathrm{pin}} = 5 \times \frac{2}{3} \approx 3.33~\mathrm{V}.
$$

The acoustic cone is roughly 15 degrees. At 80 cm the spot radius is about $$80 \tan 7.5^\circ \approx 10~\mathrm{cm}$$, so a door frame inside that spot returns instead of the cardboard you aimed at. Soft cloth swallows 40 kHz and the echo never comes. A corner multipaths. The blanking distance is about 2 cm. Practical readings you will trust on this robot sit under about 1 m, whatever the listing says about 4 m. Four meters is a hard wall, a quiet room, and a fresh 5 V supply.

If ECHO never rises, the library often returns 0. That 0 means “I do not know,” and Chapter 05’s stop behavior will treat “I do not know” as motors off. Do not clamp a timeout to 400 cm so the number looks friendly.

## VL53L0X: millimeters, already computed

The VL53L0X times a 940 nm laser on the die and hands you millimeters over I2C, default address `0x29`. The field of view is about 25 degrees. A white card is readable out to something like 1.2–2 m; black fabric and sunlit glass are worse. Sunlight adds photons the chip did not send. Glass returns the pane, not the hallway behind it. The figure’s second path is this sensor: there is no echo pin for you to time.

Two unmodified boards both answer at `0x29`. They will ACK on top of each other and the scan shows one address or a dead bus. XSHUT exists so you can hold one chip in reset, assign the other a new address, then release the first. Buying a second module without a spare GPIO for XSHUT does not buy you a second range.

## Lab: three distances, one target

### Safety

Cardboard, not a person and not a window. Do not stare into the VL53L0X aperture and do not put a phone lens or a magnifier in front of it. The laser is low-power 940 nm, which is a reason to be boring about it, not a reason to look. HC-SR04 VCC is 5 V from a supply that can provide it; do not feed that 5 V into the ESP32’s 3.3 V pin. Wheels are not part of this setup. If a motor driver is already wired, leave it unpowered.

### BOM

| Item | Role |
|------|------|
| HC-SR04 | The echo you time |
| 1 kΩ and 2 kΩ | Divider on ECHO |
| ESP32 or Pico | TRIG out, ECHO in through the divider |
| Meterstick and cardboard about A4 or larger | Truth and target |
| VL53L0X breakout | Optional second column |
| `lab-notes.md` | The error table |

### Steps

1. Build the divider before ECHO touches a GPIO. Measure the high level at the pin if you can catch a pulse, or at least measure that the bottom resistor really goes to GND.
2. TRIG gets a 10 µs pulse. Print echo time in microseconds and distance in centimeters using 0.01715. Print them both, so a bad scale is obvious.
3. Tape the meterstick to the bench. Stand the cardboard at 20 cm, then 40 cm, then 80 cm, measured to the face of the cans, not to the breadboard edge. Hold still. Record five readings and write the middle one.
4. Subtract tape from sensor. A column of signed errors is the result. A single “pretty close” is not.
5. If you own a VL53L0X, power it at the logic voltage the breakout allows, confirm `0x29`, and add a column at the same three stations. If you do not own one, the ultrasonic table is the lab. A dry-run, if the module is still in the mail, still computes the 5.8 ms echo (99.5 cm) and the divider (3.33 V) on the same page as the empty table.
6. One extra target: a folded cloth at 40 cm. Write what the ultrasonic reading does. That row is allowed to be “no echo.”

### Expected results

A table shaped like this, with your numbers in it:

| Tape (cm) | Ultrasonic (cm) | Error (cm) | ToF (cm), if any |
|----------:|----------------:|-----------:|-----------------:|
| 20 |  |  |  |
| 40 |  |  |  |
| 80 |  |  |  |

On flat cardboard, a healthy HC-SR04 is often within a few centimeters at 40 cm and a bit worse at 80 cm. An error you can explain (aim, cone, cloth, 4.6 V sagging VCC) passes. A missing row does not. Timeout printed as 0 is labeled “timeout,” not “0.0 cm to the wall.”

### Faults

| What you see | What it usually is |
|--------------|--------------------|
| GPIO warm, readings stuck | ECHO wired at 5 V with no divider |
| 20 cm station reads ~40 cm | You forgot the divide-by-two |
| Random spikes near a chair leg | The 15-degree cone found a closer object |
| Cloth reads nothing or doubles | Absorption, or a weak multipath |
| Two VL53 boards, one address | Both still at `0x29`; use XSHUT |
| Always 0 indoors, open space | Timeout, not a crash. Do not drive on that 0 |

## Mua ở Việt Nam / Where to buy in Vietnam

The ultrasonic module is the one Capstone A should not start without. The ToF board is the better second sensor if the budget allows, not a replacement you must wait for. Prices move.

| Part | Keywords | Rough band (VND) | Substitute |
|------|----------|------------------|------------|
| HC-SR04 | `cảm biến siêu âm HC-SR04` | 15.000–40.000 | [Hshop HC-SR04](https://hshop.vn/cam-bien-sieu-am-srf04) has listed about 20.000. A US-100 is a substitute only after you read whether the pin is GPIO or UART. |
| VL53L0X | `VL53L0X ToF` | 35.000–90.000 | [Hshop VL53L0X](https://hshop.vn/cam-bien-khoang-cach-tof-laser-radar-vl53l0x). VL53L1X is a different library and a longer range. |
| 1 kΩ, 2 kΩ | `điện trở 1k 2k` | 10.000–20.000 a strip | Do not skip these because the module “worked once” |

- [Hshop: HC-SR04](https://hshop.vn/search?q=HC-SR04)
- [Shopee: VL53L0X](https://shopee.vn/search?keyword=VL53L0X)
- [Lazada: cảm biến siêu âm](https://www.lazada.vn/catalog/?q=cam%20bien%20sieu%20am%20HC-SR04)
- [Thế Giới IC: HC-SR04](https://www.thegioiic.com/search?q=HC-SR04)

## Exercises

1. ECHO is high for 5.8 ms. Find $$d$$ in meters and in centimeters, using $$343~\mathrm{m/s}$$.
2. A 40 cm station produces an echo of $$2320~\mu\mathrm{s}$$. What does $$t \times 0.01715$$ report, in centimeters?
3. ECHO swings to 5 V and the pin is an ESP32 GPIO. What voltage reaches the pin with no divider, and what voltage reaches it with 1 kΩ on top and 2 kΩ to ground?
4. Two VL53L0X boards are wired in parallel, neither XSHUT used. Why does the scan fail to show two sensors, and which pin fixes it?
5. Room temperature is 30 °C, so $$v \approx 349~\mathrm{m/s}$$. The true distance is 80 cm. How long is the echo, and what distance does a firmware constant of 0.01715 cm/µs report?

### Answer guidance

1. $$d = 0.995~\mathrm{m} \approx 99.5~\mathrm{cm}$$; $$5800 \times 0.01715 = 99.5$$. 2. $$2320 \times 0.01715 \approx 39.8~\mathrm{cm}$$. 3. 5 V with no divider; $$5 \times 2/3 \approx 3.33~\mathrm{V}$$ with the divider. 4. Both ship at `0x29` and answer together; hold one in reset with XSHUT, readdress the other, then release. 5. $$t = 2 \times 0.80 / 349 \approx 4.58~\mathrm{ms} = 4585~\mu\mathrm{s}$$, and $$4585 \times 0.01715 \approx 78.6~\mathrm{cm}$$, about 1.4 cm short.

## Further reading

- [HC-SR04 datasheet (SparkFun mirror)](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf) — TRIG width, the echo, and the 5 V supply.
- [ST VL53L0X datasheet](https://www.st.com/resource/en/datasheet/vl53l0x.pdf) — ranging in millimeters, field of view, and the address.
- [Pololu VL53L0X carrier](https://www.pololu.com/product/2490) — XSHUT and level behavior, useful even on a different breakout.
- [`sensor_msgs/Range`](https://docs.ros.org/en/humble/p/sensor_msgs/msg/Range.html) — the message Chapter 09 will publish from this table.
