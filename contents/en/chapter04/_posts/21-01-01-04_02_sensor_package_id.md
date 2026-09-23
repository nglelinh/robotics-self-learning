---
layout: post
title: "Sensor package ID: HC-SR04, ToF, IMU, IR, encoders, cameras"
chapter: "04"
order: 2
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter04
lesson_type: required
draft: false
---

Estimated time: **60–80 minutes**. This is a bench identification lesson. You can finish it with photos of modules you already own, plus one datasheet tab per module you still need to buy.

## Learning objectives

You will name a module from its shape and pin labels before you wire it, state its supply voltage and its bus (trigger/echo, I2C, analog, or USB), and refuse to power a 5 V echo pin straight into an ESP32. You will fill an ID sheet that Capstone A can reuse, so the robot’s ranging and wheel-count parts are chosen on purpose. You will also say which of these parts must exist before Chapter 07 and which can wait until perception in Chapter 11.

## Prerequisites

Lesson 04-01 (I2C, SPI, UART) and the habit of reading a pinout from Chapter 01. A multimeter. You do not need every module on the desk at once.

## Why this matters for Capstone A and the ROS path

Capstone A needs a way to see that the robot is about to hit a wall, and a way to count wheel rotation if you want the acceptance test to be more than “it moved.” An HC-SR04 or a VL53L0X covers the wall. A geared motor with a magnetic encoder covers the counts. An IMU is optional for the first teleop and becomes `sensor_msgs/Imu` later. A camera is a Chapter 11 problem: it consumes USB bandwidth and CPU that a bare ESP32 does not have. Buying a camera now, before the robot stops on a timeout, is how budgets disappear.

![Sensor package identification sheet]({{ site.imgurl }}/generated/sensor_package_id.png)

## What your eyes should catch

Look at the metal, the window, and the number of pins. Then read the silkscreen. Then look up the voltage. In that order. A module that “looks like” an HC-SR04 but has five pins may be an RCWL-1601 or a US-100 with a UART mode. The library you paste will not save you.

**HC-SR04.** Two aluminum cans on a small PCB, four pins: VCC, TRIG, ECHO, GND. It wants 5 V. TRIG is an input pulse of about 10 µs. ECHO is an output pulse whose width is the round-trip time, and on the common module that pulse is 5 V. An ESP32 GPIO is not a 5 V pin. A divider (1 kΩ from ECHO to the GPIO, 2 kΩ from the GPIO to ground) brings 5 V down to about 3.3 V. The cans are a wide acoustic cone, roughly 15 degrees, so a door frame and a curtain do not read the same.

**VL53L0X and cousins.** A tiny black optical window, often on a purple breakout, pins VIN, GND, SCL, SDA, sometimes XSHUT and GPIO1. The conversation is I2C, default address `0x29`. The number you read is millimeters, already computed inside the chip. VIN on many breakouts accepts 3.3–5 V because a regulator is on the board; the I2C lines still have to match the MCU. Two unmodified VL53L0X boards on one bus share an address and will not both answer. XSHUT exists so you can boot them one at a time and assign new addresses.

**MPU-6050 / GY-521.** A small flat PCB, often green, with a metal-can chip and the pins VCC, GND, SCL, SDA, XDA, XCL, AD0, INT. I2C address `0x68` or `0x69` depending on AD0. It is an accelerometer plus a gyroscope. It does not measure distance. Students buy it when they meant to buy a rangefinder because both are “robot sensors.”

**IR reflectance and obstacle boards.** A clear LED and a black phototransistor side by side, three pins: VCC, GND, and OUT or AO. Digital boards snap high or low when a reflection crosses a potentiometer threshold. Analog boards (AO) need an ADC pin. TCRT5000 line sensors are this family. They are not laser time-of-flight, and they saturate in direct sun.

**Wheel encoders.** Either a slotted disk between an optical pair on the motor shaft, or a tiny magnetic puck on the back of a yellow TT gearbox with a Hall sensor. Two signal pins (A and B) mean quadrature and direction. One signal pin means speed only if you already know the sign from the motor driver. Count the pins before you promise odometry.

**Cameras.** A wide flex cable (FPC) into a large board (ESP32-CAM, OV2640) or a USB cable (UVC webcam). If you see a USB plug, the host is a computer, not an analog pin. ESP32-CAM boards are awkward Capstone brains: the camera uses many pins, the regulator is easy to brown out, and you still owe the robot a motor driver. Leave them for later.

## Worked example: the 5 V echo

An HC-SR04 echo pin sits at 5 V while the pulse is high. You build a divider with $$R_1 = 1~\mathrm{k}\Omega$$ from ECHO to the ESP32 pin and $$R_2 = 2~\mathrm{k}\Omega$$ from that pin to ground. The pin voltage is

$$
V_{pin} = 5 \times \frac{R_2}{R_1 + R_2} = 5 \times \frac{2}{3} \approx 3.33~\mathrm{V}.
$$

That is inside what an ESP32 input accepts. Skipping the divider “because it worked once” is how a GPIO becomes a heater. A VL53L0X on I2C does not need this divider if the breakout already speaks 3.3 V logic. Different module, different rule. Write the rule on the ID sheet next to the photo.

## Lab: one-page ID sheet

### Safety

Identification is done unpowered first. When you do apply power, USB to the MCU only. Do not tie a 5 V sensor VCC to the ESP32 3.3 V pin, and do not tie ECHO to a GPIO until the divider exists.

### BOM

| Item | Role |
|------|------|
| Any two of: HC-SR04, VL53 module, GY-521, IR board, encoder motor, webcam | The parts you will actually buy |
| Phone camera | The ID sheet |
| Multimeter | VCC check after power |
| Datasheet tab | Voltage and bus |

### Steps

1. Unpowered, photograph each module so the pins are readable.
2. Fill a row: name, pin labels you can see, guessed bus, guessed voltage, “Capstone now / later”.
3. Open the datasheet or the seller’s schematic and correct the row. Mark what you guessed wrong.
4. Power only a 3.3 V I2C module as in lesson 04-01, or stop at the paper sheet if the part is still in the mail.
5. Store the sheet in `lab-notes.md`. Chapter 07 will ask for it.

### Expected results

At least two modules with corrected voltage and bus. A written note that HC-SR04 ECHO is 5 V and VL53L0X is I2C at `0x29`. A decision: ranging sensor chosen, camera deferred.

### Faults

| Mistake | What breaks |
|---------|-------------|
| Calling every black window an IMU | You I2C-scan a rangefinder, or you try to read distance from a gyro |
| 5 V into ESP32 | Hot pin, stuck input, or a dead GPIO |
| Two VL53 boards, no XSHUT plan | Scan shows one address or none |
| Encoder with one channel | You cannot tell forward from back |
| Buying ESP32-CAM as the Capstone brain | Motor pins and brownouts fight the camera |

## Mua ở Việt Nam / Where to buy in Vietnam

Buy the ranging sensor and, if the budget allows, TT motors that already include encoders. Skip the camera until Chapter 11.

| Part | Keywords | Rough band (VND) | Substitute |
|------|----------|------------------|------------|
| HC-SR04 | `cảm biến siêu âm HC-SR04` | 15.000–40.000 | [Hshop HC-SR04](https://hshop.vn/cam-bien-sieu-am-srf04) has listed about 20.000. US-100 is a substitute only if you read its UART/GPIO mode. |
| VL53L0X module | `VL53L0X ToF` | 35.000–90.000 | [Hshop VL53L0X](https://hshop.vn/cam-bien-khoang-cach-tof-laser-radar-vl53l0x). VL53L1X is longer range and a different library. |
| GY-521 | `MPU6050 GY-521` | 35.000–90.000 | MPU6500 if the example code matches. |
| IR obstacle or TCRT5000 | `cảm biến hồng ngoại vật cản` | 8.000–25.000 | Fine for a line, poor as the only bumper |
| TT motor + encoder | `động cơ TT encoder Hall` | 40.000–90.000 each | N20 metal-gear with encoder if the chassis holes match; check 3 mm vs 4 mm shaft |
| Logic divider resistors | `điện trở 1k 2k` | 10.000–20.000 a strip | Thế Giới IC for loose resistors |

Searches:

- [Hshop HC-SR04 search](https://hshop.vn/search?q=HC-SR04)
- [Shopee encoder motor](https://shopee.vn/search?keyword=dong%20co%20TT%20encoder)
- [Lazada VL53L0X](https://www.lazada.vn/catalog/?q=VL53L0X)
- [Thế Giới IC modules](https://www.thegioiic.com/search?q=HC-SR04)

## Exercises

1. A board has two metal cans and the pins VCC, TRIG, ECHO, GND. What voltage does ECHO reach, and what two resistors do you add for an ESP32?
2. A purple board has a black window and SCL/SDA. Which family is it, and what address do you expect the first time you scan?
3. You need to know whether the left wheel rolled forward or backward. Will a single Hall sensor be enough? What do you buy instead?
4. Sort these into “before Capstone A” and “after the robot already teleops”: HC-SR04, USB camera, encoder motor, ESP32-CAM, VL53L0X.
5. Two VL53L0X modules both stay at `0x29`. What pin exists to untangle that, and what does a scan look like before you use it?

### Answer guidance

1. About 5 V; 1 kΩ and 2 kΩ as the divider above, about 3.3 V at the pin. 2. Time-of-flight, usually `0x29`. 3. No; buy a quadrature pair (A and B) or accept that direction comes only from the motor command, which misses coasting. 4. Before: HC-SR04 or VL53L0X, and encoders if you want counts. After: USB camera and ESP32-CAM. 5. XSHUT; the scan shows one address or a messy bus until you power them separately and reassign.

## Further reading

- [HC-SR04 datasheet mirror (SparkFun)](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf)
- [ST VL53L0X datasheet](https://www.st.com/resource/en/datasheet/vl53l0x.pdf)
- [TDK MPU-6000/6050 datasheet](https://invensense.tdk.com/wp-content/uploads/2015/02/MPU-6000-Datasheet1.pdf)
- [Pololu VL53L0X carrier notes](https://www.pololu.com/product/2490) — address and level behavior, useful even if you buy a different breakout.
