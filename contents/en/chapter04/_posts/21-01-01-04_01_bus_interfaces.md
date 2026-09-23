---
layout: post
title: "Sensor interfaces: I2C, SPI, UART"
chapter: "04"
order: 1
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter04
lesson_type: required
draft: false
---

Estimated time: **70–90 minutes**, including one I2C scan on a real board or a careful dry-run if the module has not arrived.

## Learning objectives

By the end of this lesson you can choose I2C, SPI, or UART for a sensor from its datasheet rather than from habit, wire the shared ground and the pull-ups an open-drain bus actually needs, and run an address scan that prints something like `0x68` before you trust a library. You can also explain why Capstone A teleop is a UART conversation, while the IMU and time-of-flight sensor that show up later on the same robot want a shared I2C bus, and why a ROS 2 topic does not replace either of those wires.

## Prerequisites

You can use a multimeter for continuity and DC voltage (Chapter 01), you know which pins on your ESP32 or Pico are 3.3 V GPIO (Chapter 02), and you can blink an LED from firmware (Chapter 03). You do not need ROS installed for this lesson.

## Why this matters for Capstone A and the ROS path

Capstone A, in Chapter 07, drives a differential robot from a laptop serial line. That line is UART: a baud rate, a crossed TX/RX pair inside the USB chip, and a rule that silence means stop. The same robot, once it is trustworthy, grows an I2C IMU and often an I2C VL53L0X. Chapter 09 will publish those readings as `sensor_msgs/Imu` and `sensor_msgs/Range`, and Chapter 10 may carry them through micro-ROS. If the bus is missing a pull-up or the address is wrong, the ROS graph looks empty for a reason that lives on the breadboard, not in the launch file. Learn the wire first.

## Three buses, three contracts

A digital sensor is a small computer with a published conversation. The datasheet names the conversation. Your job is to match voltage, wires, and speed, then prove the part answers before you ask it for meters or degrees.

**I2C** uses two signals, SDA and SCL, plus power and ground. Both lines are open-drain: a device may pull a line down, and a resistor pulls it up when nobody is talking. Many breakout boards already include 4.7 kΩ or 10 kΩ pull-ups to their own logic voltage. Two modules in parallel make the pull stronger (the resistances combine in parallel). The ESP32’s internal pull-ups are weak, on the order of tens of kilohms, and are a poor substitute at 400 kHz. A practical starting point on a short 3.3 V bus is external 4.7 kΩ to 3.3 V if the modules do not already provide them.

Each device has a 7-bit address. The MPU-6050 answers at `0x68` when AD0 is low and `0x69` when AD0 is high. A VL53L0X usually answers at `0x29`. The master speaks an address, the slave ACKs by pulling SDA low, and only then does a register read mean anything. Standard mode is 100 kHz; fast mode is 400 kHz. Do not start at 1 MHz because an example sketch did.

**SPI** adds a clock and a chip-select per device: SCLK, MOSI, MISO, and CS, plus power and ground. It is full duplex and much faster, which is why some IMUs offer SPI as well as I2C. The mode is a pair of bits, CPOL and CPHA. Mode 0 means the clock idles low and the slave is sampled on the rising edge. A wrong mode looks like a sensor that is present but returns nonsense. Unlike I2C, SPI has no address byte; the CS pin *is* the address. Leave CS high for devices you are not talking to.

**UART** has no clock. You agree a baud rate (115200 is the Capstone A default), a frame (8 data bits, no parity, 1 stop bit), and you cross the wires: the host’s TX goes to the MCU’s RX. USB adapters hide that cross inside the cable, which is why a serial monitor “just works” until you wire two boards and connect TX to TX. Ground is still shared. Only one driver should sit on a given TX wire.

![I2C, SPI, and UART wiring contracts]({{ site.imgurl }}/generated/bus_i2c_spi_uart.png)

## Worked example: one bus, two sensors

You want a GY-521 (MPU-6050) and a VL53L0X on an ESP32 DevKit. Both are I2C. Both can run from 3.3 V logic. Wire both SDA pins to GPIO 21, both SCL pins to GPIO 22 (confirm the silkscreen; clones differ), both grounds to ESP32 GND, and both VCC pins to 3.3 V. Do not power the VL53 module from 5 V “just in case” if the breakout’s I2C lines are not level-shifted; many small purple modules are 3.3 V parts with a regulator, and the datasheet of *that board* decides.

A scan should print two addresses. If you see only `0x68`, the time-of-flight board is unpowered, its SDA/SCL are swapped, or its address was changed and you are scanning the wrong range. If you see nothing, check that both modules share ground with the ESP32 before you change a library.

The same ESP32’s USB port is a separate UART used later for teleop. It does not occupy SDA/SCL. You can scan I2C and still print the result to the serial monitor. That split — I2C for chips on the robot, UART for the human — is the architecture Capstone A keeps.

## Lab: scan before you decode

### Safety

Modules in this lab draw tens of milliamps. Do not connect a motor driver to the same breadboard rails yet. If a module becomes hot in a few seconds, unplug USB; a swapped VCC and GND is the usual cause.

### BOM

| Item | Role |
|------|------|
| ESP32 devkit or Raspberry Pi Pico | I2C master |
| GY-521 MPU-6050, or any I2C module you already own | Known address |
| 4.7 kΩ resistors ×2 | Pull-ups, if the module has none |
| Breadboard and dupont wires | Short bus |
| Multimeter | Continuity on GND, voltage on VCC |

### Steps

1. Continuity-check that module GND and MCU GND are the same node before you apply power.
2. Measure VCC at the module with USB plugged in. You want about 3.3 V, not 5 V, on a 3.3 V-only breakout.
3. Flash the scan. On ESP32 Arduino:

```cpp
#include <Wire.h>
void setup() {
  Serial.begin(115200);
  Wire.begin(21, 22); // SDA, SCL — match your board
}
void loop() {
  Serial.println("scan");
  for (uint8_t addr = 1; addr < 127; ++addr) {
    Wire.beginTransmission(addr);
    if (Wire.endTransmission() == 0) {
      Serial.printf("ACK 0x%02X\n", addr);
    }
  }
  delay(2000);
}
```

On Pico MicroPython the same idea is `I2C(0, sda=Pin(0), scl=Pin(1), freq=100_000)` and `i2c.scan()`.

4. Write the addresses you found into `lab-notes.md` next to a photo of the wiring.
5. If you have a second I2C device, add it and confirm both ACKs still appear. Two devices with the same address will not both answer cleanly; that is a datasheet problem, not a ROS problem.

### Expected results

One module: a single stable address (`0x68` for a typical GY-521 with AD0 grounded). Two different modules: two addresses. The scan still works after you unplug and replug USB.

### Faults

| What you see | What it usually means |
|--------------|------------------------|
| No ACK | GND not shared, SDA/SCL swapped, or VCC dead |
| Address appears, then vanishes | Loose dupont, or a pull-up to the wrong voltage |
| Every address ACKs | SDA shorted to GND |
| Works at 100 kHz, fails at 400 kHz | Long wires or missing pull-ups |
| Library says “device not found” but scan works | Library uses a different address or different pins |

## Mua ở Việt Nam / Where to buy in Vietnam

You need one I2C module to finish the lab, plus a handful of 4.7 kΩ resistors if your junk box is empty. A logic-level shifter (BSS138 style, four or eight channels) is worth having before you mix a 5 V peripheral onto a 3.3 V ESP32, but you do not need it for a 3.3 V GY-521.

| What | Search keywords | Rough band (VND) | Notes |
|------|-----------------|------------------|-------|
| GY-521 MPU-6050 | `MPU6050 GY-521` | 35.000–90.000 | [Hshop listing](https://hshop.vn/cam-bien-6-dof-bac-tu-do-gy-521-mpu6050) has been around 85.000. MPU6500 is a fine substitute if the library matches. |
| 4.7 kΩ resistors | `điện trở 4.7k 1/4W` | 10.000–25.000 for a strip | Thế Giới IC is the better counter for bare resistors. |
| Level shifter | `logic level shifter 3.3 5` | 8.000–25.000 | Use on 5 V I2C, not as a power supply. |
| Dupont wires | `dây dupont đực cái` | 15.000–40.000 | |

Search, do not trust a random product photo:

- [Hshop search](https://hshop.vn/search?q=MPU6050)
- [Shopee search](https://shopee.vn/search?keyword=MPU6050%20GY-521)
- [Lazada search](https://www.lazada.vn/catalog/?q=MPU6050)
- [Thế Giới IC search](https://www.thegioiic.com/search?q=tr%E1%BB%9F%20k%C3%A9o)

Street prices move. Compare two sellers and prefer a module with pin labels printed on the PCB.

## Exercises

1. A board shows SDA, SCL, GND, VCC, and the text “I2C 0x29”. Which bus is it, which single extra part might the bus need, and what should a scan print?
2. Your scan is empty. List the three electrical checks you do before you change a line of code, in order.
3. Two GY-521 boards both have AD0 tied to GND. What happens on one I2C bus, and what is the cheap hardware fix?
4. Capstone teleop uses 115200 baud, 8N1. A friend connects the USB serial adapter’s TX to the ESP32’s TX. What does the ESP32 receive, and how do you fix a *discrete* UART between two boards?
5. Why is “the ROS topic `/imu/data` is silent” not the first debugging step on a robot you have not scanned?

### Answer guidance

1. I2C, pull-ups to the logic rail if the module lacks them, and `0x29`. 2. Shared GND, VCC actually present and at the right voltage, SDA/SCL not swapped. 3. They collide at `0x68`; lift one AD0 to VCC so it becomes `0x69`, and tell the library. 4. It receives nothing useful; cross TX to RX and share GND. The USB cable already crosses, so do not “fix” a working USB serial by swapping pins in software first. 5. Because the driver may never have ACKed. Scan, then publish.

## Further reading

- [NXP UM10204, the I2C-bus specification](https://www.nxp.com/docs/en/user-guide/UM10204.pdf) — open-drain, addressing, and timing in the primary source.
- [SparkFun I2C tutorial](https://learn.sparkfun.com/tutorials/i2c/all) — pull-ups and addresses with wiring photos.
- [SparkFun SPI tutorial](https://learn.sparkfun.com/tutorials/serial-peripheral-interface-spi/all) — modes and chip-select.
- [SparkFun serial communication](https://learn.sparkfun.com/tutorials/serial-communication/all) — UART frames and baud.
- [Espressif I2C driver notes](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/peripherals/i2c.html) — what the ESP32 peripheral actually implements.
