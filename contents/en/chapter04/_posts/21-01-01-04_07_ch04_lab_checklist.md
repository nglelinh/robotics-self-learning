---
layout: post
title: "Chapter 04 lab checklist"
chapter: "04"
order: 7
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter04
lesson_type: required
draft: false
---

Sensors are only trustworthy after they have been **calibrated, sign-checked, and logged**. In Chapter 04 you wired buses, encoders, an IMU, and range sensors. This sign-off checklist validates every sensor stream quantitatively — ensuring right-handed coordinate frames, accurate scale factors, and healthy sample rates before Chapter 05 closes the feedback loop onto motors.r

---

Estimated time: **50–70 minutes**. This is a sign-off, not a new sensor. You pass when `lab-notes.md` holds the evidence below. A memory of having “basically done the lab” does not open Chapter 05.

## Learning objectives

You will judge your own Chapter 04 notes against pass/fail measurements: an I2C address with a photo, an encoder $$N$$ from one wheel revolution and the matching meters per count, an at-rest IMU reading or a dated waiver, a ranging table or the 5.8 ms dry-run, and a camera sentence that contains 147 Mbit/s. You will paste a block a classmate could check without asking you what you meant. You will name two failure modes you personally hit or deliberately simulated, and you will recognize a filled log that still fails.

## Prerequisites

Lessons 04-01 through 04-06 are the work being signed. You need your `lab-notes.md`, the ID sheet from Lesson 04-02, and the numbers those lessons already computed: $$N$$ and $$r = 0.0325~\mathrm{m}$$ if you used the teaching wheel, the complementary step that lands on 9.889 degrees, the echo of 5.8 ms that is 99.5 cm, the divider at 3.33 V, and the 147 Mbit/s camera budget. Chapter 05 starts motors and H-bridges. It assumes this page is already honest, because a 5 V echo on a GPIO will still be a 5 V echo after a motor driver is wired beside it.

## Key ideas: Right-Handed Coordinate Frames (REP-103), Calibration, and Multi-Sensor Synchronization

Three robotics standards make Chapter 04 sensor data seamlessly compatible with both Capstone A and ROS 2:

- **ROS REP-103 Right-Handed Frame Convention:** `+X` forward, `+Y` left, `+Z` up; positive yaw `ω_z` rotates **counter-clockwise** (left turn). Checking sign conventions now prevents inverted steering bugs in Chapter 05 and SLAM.
- **Scale & Bias Calibration:** Rolling the robot straight along a 1.00 m tape measure calibrates effective wheel circumference `m_per_count`; rotating 360° in place calibrates effective track width `L_eff` (accounting for tire scrub!); holding still calibrates IMU gyro bias.
- **Health & Rate Verification:** Confirming actual achieved publish/log rates (e.g., encoders at 100 Hz, IMU at 100 Hz, ToF at 20–30 Hz) with zero `NaN` or stuck readings completes sensor readiness.r

---

## Why this matters for Capstone A and the ROS path

Chapter 07’s teleop firmware commands two wheels and stops on a timeout or a range reading. That range is only as good as the table you sign here, and the optional wheel count in the acceptance log is only as good as $$N$$. ROS 2 later publishes the same quantities as `sensor_msgs/Range`, `nav_msgs/Odometry`, then `sensor_msgs/Imu` and `sensor_msgs/Image`. A doubled $$N$$ makes odometry report half the hallway. A timeout stored as 0 cm says the robot is inside the wall. The camera sentence keeps Chapter 11 from arriving as a surprise 147 Mbit/s USB load.

![The ID sheet this gate checks: bus, voltage, and which module can wait]({{ site.imgurl }}/generated/sensor_package_id.png)

## What you paste into `lab-notes.md`

Copy this block, replace the blanks with your evidence, and delete any row you cannot support. A blank you leave in place is a fail.

```
## Chapter 04 sign-off
Date:
I2C: addresses seen = ____ ; photo file = ____
Encoder: N = ____ counts per output rev (three trials: __, __, __)
         r = ____ m ; meters per count = ____
         forward lead: channel ____  (or "single channel, no direction")
IMU: |a| = ____ g ; at-rest axis = ____ sign ____
     gyro bias deg/s = (__, __, __)
     OR waiver date ____ and complementary result 9.889 deg checked
Range: 20 cm -> __ cm (err __) ; 40 -> __ (err __) ; 80 -> __ (err __)
       OR dry-run: 5.8 ms -> 99.5 cm ; divider 5*(2/3) = 3.33 V
Camera: deferred to ch.11 ; 640x480 YUYV 30 fps ≈ 147 Mbit/s
Failure 1:
Failure 2:
```

## Pass and fail

**I2C.** At least one address is written (`0x68`, `0x69`, or `0x29` are the usual ones) and a photo shows the module and the wires. “It scanned fine,” with no address and no photo, fails.

**Encoder.** $$N$$ is one hand revolution of the output shaft, three trials within one count. Meters per count is $$2\pi r / N$$. Teaching wheel: $$r = 0.0325~\mathrm{m}$$, circumference $$\approx 0.2042~\mathrm{m}$$, so $$N = 20$$ means $$0.01021~\mathrm{m}$$ per count. The seller’s PPR fails when the counter printed a different integer. A single channel passes only if the notes say direction is unknown.

**IMU.** Resting magnitude near 1 g, with axis, sign, and gyro bias in deg/s after the datasheet scale, or a dated waiver. The waiver still shows the complementary step (next $$\theta = 9.889~\mathrm{deg}$$) and $$0.5~\mathrm{deg/s} \times 60~\mathrm{s} = 30~\mathrm{deg}$$. Raw LSB printed as degrees fails both paths.

**Ranging.** A 20 / 40 / 80 cm table with signed errors. At 40 cm, within 5 cm on flat cardboard is a clean pass; a larger error passes only if the notes name the cause. A missing station fails. A mail-delay dry-run passes only with $$5.8~\mathrm{ms} \rightarrow 99.5~\mathrm{cm}$$ and $$5 \times 2/3 \approx 3.33~\mathrm{V}$$. “Works to 4 m” is not that page.

**Camera.** One sentence: the camera waits until Chapter 11, and a 640×480 YUYV stream at 30 fps is about 147 Mbit/s. Omitting the number fails the row. Buying an ESP32-CAM this week does not pass it.

**Two failures.** Each names what you saw and what you changed or will change. “None, everything worked” fails the gate even if the other rows are perfect. Simulating a swapped A/B in the notes, or a cloth target with no echo, counts if you write the numbers.

## A log that feels finished and still fails

This is the kind of page that gets returned. The student was not lazy. The student measured the wrong thing, and Chapter 05 would inherit it.

```
# lab-notes.md — example that does NOT pass
Date: 12 Sep

I2C: scanned fine, no errors. (no address, no photo)

Encoder: seller says 40 PPR so N = 40.
One hand turn looked like about 20 blinks but I kept 40.
r = 0.0325 m
meters per count = 0.2042/40 = 0.0051 m

IMU: flat on the desk, az = 16384 degrees. Gyro 70.

Range: ECHO to GPIO18, no resistors, VCC 5 V.
Readings jumped. I will average them in software.
20 cm station not done. 40 cm sometimes 80.

Camera: ordering ESP32-CAM so Chapter 07 can see the hallway.

Failures: none.
```

The I2C row has no address and no photo. The encoder saw about 20 counts and wrote $$N = 40$$, so meters per count is half of $$0.01021~\mathrm{m}$$: 140 counts become $$0.71~\mathrm{m}$$ in the log instead of $$1.43~\mathrm{m}$$. The IMU prints LSB as degrees. At $$\pm 2~\mathrm{g}$$, 16384 is $$+1~\mathrm{g}$$; a gyro raw 70 at $$\pm 250~\mathrm{deg/s}$$ is $$70/131 \approx 0.53~\mathrm{deg/s}$$. ECHO at 5 V with no divider sits outside the GPIO rating; the fix is 1 kΩ / 2 kΩ, about 3.33 V, then a real 20/40/80 table. The camera line never says 147 Mbit/s, and “no failures” hides the doubled $$N$$ and the bare echo pin that are already on the page.

## What to repair before Chapter 05

Chapter 05 adds motor current and a driver that can reset the microcontroller. Do not begin it on a GPIO that has already seen 5 V, or with an $$N$$ you know is doubled. Before you sign: put the divider on ECHO (1 kΩ / 2 kΩ, about 3.33 V) or disconnect ECHO; rewrite $$N$$ from the hand count and recompute meters per count; rewrite the IMU line in g and deg/s, or file the dated waiver with 9.889 deg and 30 deg of drift; finish the ranging table or the dry-run; replace the camera sentence and leave any ESP32-CAM in the bag; fill two failure lines from what you actually undid. Chapter 05 will not re-ask the echo voltage.

## Lab: the sign-off itself

### Safety

You are editing notes. If you power the board for a new photo, USB only, wheels off the floor, ECHO through the divider. Describe the 5 V fault in writing. Do not reproduce it on a live GPIO.

### BOM

| Item | Role |
|------|------|
| `lab-notes.md` | The document you sign |
| ID photo from Lesson 04-02 | Address row |
| Lesson 04-05 notes | Error table or dry-run |
| Calculator | $$2\pi r/N$$ and the 5.8 ms echo, recomputed on this page |

### Steps

1. Paste the sign-off block into `lab-notes.md` and fill it from the lesson where you measured each row. A late module uses the dated waiver or the dry-run, not a blank.
2. On the same page, recompute meters per count and $$343 \times 0.0058 / 2 = 0.995~\mathrm{m}$$.
3. Hold your page next to the failing sample. Any sentence that matches it gets rewritten before you tick the row.
4. Write two failures in the first person, each with a number. Stop there. Motor wiring waits until every row passes.

### Expected results

A classmate finds an address, an $$N$$, a g-vector or a waiver, a range table or 99.5 cm, the 147 Mbit/s sentence, and two failures, without asking you a question.

### Faults

| What you see | What it usually is |
|--------------|--------------------|
| Every cell says “yes” | The gate wants a number, an address, or a file name |
| $$N$$ copied from the product title | The hand count was not allowed to win |
| Waiver with no 9.889 and no 30 deg | The IMU row is empty |
| Dry-run with no 3.33 V | The divider was skipped on paper too |
| Camera sentence with no bit rate | The row fails |

## Explanation: Calibrating Wheel Radius and Track Width with a 1-Meter Tape Measure

Even caliper-measured wheel diameters differ slightly from effective rolling diameters under chassis weight and tire compression. Calibrate your robot's true kinematic constants in four exact steps:

1. **Linear calibration (1.000 m straight push):** Push the robot straight along a ruler for exact distance $$D_{\text{true}} = 1.000\text{ m}$$ and record average encoder counts $$\bar{c} = (c_L + c_R)/2$$.
2. **Compute calibrated meters-per-count:** $$m_{\text{cal}} = D_{\text{true}} / \bar{c}$$.
3. **Angular calibration (exact $$360^\circ = 2\pi\text{ rad}$$ spin):** Rotate the robot in place one full turn ($$2\pi$$ rad) and record $$\Delta s_R - \Delta s_L = (c_R - c_L)\,m_{\text{cal}}$$.
4. **Compute effective track width:** $$L_{\text{eff}} = \frac{\Delta s_R - \Delta s_L}{2\pi}$$.

### Concrete Worked Example: Empirical Odometry Calibration on a Desk Robot

- **Step 1 — Straight 1.000 m roll:** Encoders record $$c_L = 4\,910$$ and $$c_R = 4\,890$$ counts ($$\bar{c} = 4\,900$$):
  $$m_{\text{cal}} = \frac{1.000\text{ m}}{4\,900\text{ counts}} = 0.00020408\text{ m/count}.$$
  (If caliper prediction had been $$0.0002000\text{ m/count}$$, this single 10-second calibration eliminates a **2.0%** distance error!)
- **Step 2 — Exact $$360^\circ$$ counter-clockwise spin in place:** Encoders record $$c_R = +2\,540$$ and $$c_L = -2\,520$$:
  $$\Delta s_R - \Delta s_L = (2540 - (-2520)) \times 0.00020408 = 5\,060 \times 0.00020408 = 1.0326\text{ m}.$$
  $$L_{\text{eff}} = \frac{1.0326}{2\pi} = \frac{1.0326}{6.2832} \approx 0.1643\text{ m} \;\; (164.3\text{ mm}).$$
  Notice $$L_{\text{eff}} = 164.3\text{ mm}$$ is slightly wider than the caliper-measured `160 mm` because wide rubber tires scrub during pivots — using $$L_{\text{eff}}$$ makes turning accuracy dramatically sharper!

**Common Pitfall:** Calibrating only one wheel and assuming left and right motors/tires are identical — a 1% tire-diameter mismatch causes a robot driving "straight" to drift into a slow curve unless you compare `c_L` vs. `c_R` separately.

**Quick Check:** Turn the robot $$90^\circ$$ left (counter-clockwise) by hand: right encoder should increase (`+`), left encoder should decrease (`-`), and IMU `gyro_z` should spike **positive** (`+`). If `gyro_z` goes negative, negate it in software so all sensors share one right-handed frame!

---

## Mua ở Việt Nam / Where to buy in Vietnam

Close the chapter with the parts the sign-off still lacks. Skip the camera. Prices move.

| Part | Keywords | Rough band (VND) | Substitute |
|------|----------|------------------|------------|
| HC-SR04 | `HC-SR04` | 15.000–40.000 | [Hshop listing](https://hshop.vn/cam-bien-sieu-am-srf04), often about 20.000 |
| VL53L0X, optional | `VL53L0X` | 35.000–90.000 | [Hshop VL53L0X](https://hshop.vn/cam-bien-khoang-cach-tof-laser-radar-vl53l0x). Ultrasonic alone can pass the gate. |
| MPU-6050 GY-521 | `MPU6050` | 35.000–90.000 | [Hshop GY-521](https://hshop.vn/cam-bien-6-dof-bac-tu-do-gy-521-mpu6050), often about 85.000. MPU6500 if the library matches. |
| TT motor with encoder, a pair | `động cơ TT encoder` | 40.000–90.000 each | Measure $$N$$; do not trust the title |

- [Hshop: HC-SR04](https://hshop.vn/search?q=HC-SR04)
- [Shopee: MPU6050](https://shopee.vn/search?keyword=MPU6050%20GY-521)
- [Lazada: động cơ TT encoder](https://www.lazada.vn/catalog/?q=dong%20co%20TT%20encoder)
- [Thế Giới IC: VL53L0X](https://www.thegioiic.com/search?q=VL53L0X)

## Exercises

Use the failing log and the lesson numbers. Short answers.

1. The failing log sets $$N = 40$$ with $$r = 0.0325~\mathrm{m}$$ after the hand turn showed about 20 counts. What meters per count did they write, what should they write, and how far would 140 counts be in each story?
2. ECHO is on a GPIO with no divider. What voltage hits the pin while the echo is high, what two resistors fix it, and what is $$V_{\mathrm{pin}}$$?
3. The IMU waiver says only “module later.” Does it pass? What two results must be written on that dated line?
4. A dry-run ranging page shows “5.8 ms → 99.5 cm” and does not mention the divider. Pass or fail, and what voltage is missing?
5. Which single camera sentence passes, and which sentence in the sample fails it?

### Answer guidance

1. They wrote $$0.0051~\mathrm{m}$$ per count; the hand count $$N = 20$$ gives $$0.01021~\mathrm{m}$$. One hundred forty counts are $$0.71~\mathrm{m}$$ in their log and $$1.43~\mathrm{m}$$ in the corrected one. 2. 5 V; 1 kΩ from ECHO to the pin and 2 kΩ to ground; $$\approx 3.33~\mathrm{V}$$. 3. It fails. The waiver needs the complementary result $$9.889~\mathrm{deg}$$ and the drift $$0.5 \times 60 = 30~\mathrm{deg}$$. 4. Fail. The missing number is $$3.33~\mathrm{V}$$ from $$5 \times 2/3$$. 5. A pass defers the camera to Chapter 11 and includes about 147 Mbit/s. “Ordering ESP32-CAM so Chapter 07 can see” fails.

## Further reading

- [HC-SR04 datasheet (SparkFun mirror)](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf) — why ECHO is a 5 V pulse.
- [MPU-6050 datasheet](https://invensense.tdk.com/wp-content/uploads/2015/02/MPU-6000-Datasheet1.pdf) — the scale that turns 16384 into 1 g.
- [`sensor_msgs/Range`](https://docs.ros.org/en/humble/p/sensor_msgs/msg/Range.html) and [`nav_msgs/Odometry`](https://docs.ros.org/en/humble/p/nav_msgs/msg/Odometry.html) — the two messages this sign-off is protecting.
- [Espressif I2C](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/peripherals/i2c.html) — the scan the photo is supposed to match.
