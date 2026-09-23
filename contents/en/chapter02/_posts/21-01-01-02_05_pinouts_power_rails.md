---
layout: post
title: "Pinouts, logic levels, and power rails"
chapter: "02"
order: 5
owner: "Nguyen Le Linh"
lang: en
categories: [chapter02]
lesson_type: required
draft: false
---

## Objectives

You will name, on your own board, the USB 5 V pin and the regulated 3.3 V pin, and you will measure both with USB only. You will treat every ESP32 and Pico GPIO as a 3.3 V pin that 5 V can kill. You will place a 2S pack on the TB6612 VM pin in a drawing, and you will list the header pins that pack must never touch. You will level-shift an HC-SR04 echo on paper, with a common ground, before any sensor is wired. You will leave the battery disconnected for the whole lab.

## Prerequisites

The heartbeat lab has already proved the board enumerates and that you know which LED pin you own. You can set a meter to DC volts and put the black lead on a ground you can name. Chapter 01’s resistor divider is the only circuit math required. No motor supply is connected. The full cart, including the driver and the pack, is the Chapter 00 shopping lesson ([BOM and shopping]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %})). You are not buying the pack in order to finish this page.

## Why it matters for Capstone A

Chapter 07’s firmware teleop fails in ways that look nothing like a bad `if`. A 5 V ultrasonic echo lands on a 3.3 V GPIO. A motor return never shares ground with the logic, so a “PWM” pin floats relative to the driver and the TB6612 reads nonsense. A 7.4 V pack is clipped to the pin marked 5V or 3V3 because the label looked generous. The chip resets, or a pin dies, the first time the robot is asked to move. The timeout of about 300 ms and the wheels-up rule still matter, and they cannot save a pin that has already seen the battery. The card you draw here is the map you will hold when Chapter 05’s driver and Chapter 07’s PWM are finally legal. Chapter 08’s Wi-Fi does not add a tougher GPIO.

## Two rails, and a third that is not on this header

ESP32 and Pico GPIO pins are 3.3 V logic. Five volts on a GPIO can kill the pin. On the ESP32 the absolute maximum is only a diode drop above the rail:

$$
V_{DD} + 0.3\,\mathrm{V} = 3.3\,\mathrm{V} + 0.3\,\mathrm{V} = 3.6\,\mathrm{V}.
$$

The Pico’s limit is the same kind of number, a few tenths above 3.3 V. Five volts is past either limit.

A hobby reading rule, separate from that damage line, says a high should be at least about $$0.7 \times 3.3\,\mathrm{V} \approx 2.3\,\mathrm{V}$$ before you trust it. Real $$V_{IL}$$ and $$V_{IH}$$ are in the datasheet. The operating rule is simpler than either formula: do not feed a GPIO from a 5 V pin.

On a classic ESP32 dev board the pin marked 5V or VIN is USB 5 V, often through a Schottky diode, so the header sits a few tenths below the laptop’s 5 V. It can power a small sensor while you are still on the bench. It cannot power TT motors. A single TT motor’s no-load current on the course listing is already about 110 mA to 150 mA, and stall is many times that. Two motors plus a Wi-Fi peak collapse a USB port. The refusal arrives as a disconnect or as a brownout reset, the same repeating banner you learned in the heartbeat lab. The pin marked 3V3 is the regulator output. It feeds the module. A motor does not belong on it.

The Pico names the same ideas more honestly. VBUS is USB 5 V and is present when the cable is plugged in. VSYS is the system input. USB reaches VSYS through a diode, and an external supply on VSYS itself is limited to about 1.8 V to 5.5 V. 3V3 is the regulated rail and it is an output. Do not feed 7.4 V into 3V3. Do not feed 7.4 V into VSYS. Both are outside what those pins are for, and 7.4 V on 3V3 is a direct hit on the regulator output.

![USB 5 V, regulated 3.3 V, and a motor rail that stays off the header]({{ site.imgurl }}/generated/power_rails_3v3.png)

Read the drawing as a promise about current as well as voltage. The 5 V rail comes from USB and may be borrowed lightly. The 3.3 V rail is for logic. Ground is common. The motor rail is not one of those two pins.

![Board anatomy: probe the header, not the module]({{ site.imgurl }}/generated/pcb_mcu_anatomy.png)

The USB connector explains VBUS or the dev-board 5V pin. The regulator explains 3V3. The meter lands on the header. The metal can is not a test point.

Common ground with the driver is mandatory. The TB6612 measures your PWM against its own logic ground. If that ground is not the microcontroller’s ground, the driver does not see a reliable high, even when the GPIO voltage looks correct on a meter referenced to the wrong place. When the driver arrives, its GND pin ties to a GND pin on the ESP32 or the Pico. The motor supply does not.

## The echo pin

The HC-SR04’s echo output is a 5 V pulse. That pulse must be level-shifted before it reaches an ESP32 or Pico input. A shifter module is the robust tool: the low-voltage side is the board’s 3V3, the high-voltage side is the sensor’s 5 V, and the grounds are tied together. Echo travels from the high side to the low side and into the GPIO. Many modules accept a 3.3 V high on the trigger pin; that is a property of the sensor’s input, and it is not permission to skip the echo translation. You will confirm trigger behavior in the sensor chapter. You will not discover it by sacrificing a GPIO today.

A resistor divider is the calculation that shows why a raw 5 V echo is illegal. With $$1\,\mathrm{k}\Omega$$ from echo to the GPIO node and $$2\,\mathrm{k}\Omega$$ from that node to GND:

$$
V_{\mathrm{GPIO}} = 5\,\mathrm{V} \times \frac{2}{1 + 2} \approx 3.33\,\mathrm{V}.
$$

That sits near the top of the allowed range, which is why a shifter is the kinder part once the robot has to be reliable. Tolerances and a long cable move the node. Build nothing with the sensor in this lab. Write the fraction on the pin card so the later wiring has a number attached.

## Worked example

A 2S pack of 18650 cells sits near 7.4 V nominal, higher when full, lower when empty. Hà draws the only legal landing for the red lead: the TB6612 VM terminal. The Hshop-style module in the Chapter 00 notes accepts a motor supply in the range that includes 7.4 V. The black lead lands on the driver GND, and a separate wire joins that GND to the microcontroller GND.

The pack’s positive lead has a list of pins it must never touch. On the ESP32 header: any GPIO, the 3V3 pin, and the 5V/VIN pin. That 5V pin is USB 5 V; a 2S pack there can back-feed the laptop. On the Pico: any GP pin, 3V3, VSYS, and VBUS. VSYS’s allowed window is about 1.8 V to 5.5 V, and 7.4 V is outside it. 3V3 is an output on both boards. The driver’s logic VCC, the small pin that expects 3.3 V or 5 V, is not VM. Hà writes “VM only” next to the pack and “logic VCC from 3V3, not from the pack” next to the driver.

No wire is connected. The drawing is the worked example. The meter work is a different, smaller act: USB only.

## Lab

USB cable only. Battery unplugged, driver unplugged, sensor unplugged.

1. Red lead in the voltage jack, black lead on a GND pin you can name, meter on DC volts.
2. Measure the 5 V rail: the dev-board pin marked 5V or VIN, or Pico VBUS. Write the number.
3. Measure 3.3 V: the pin marked 3V3, or Pico 3V3(OUT). Write the number.
4. Draw a pin card: those two rails, GND, the heartbeat LED pin, one free GPIO you have checked against the silk, and a forbidden list. The forbidden list includes “5 V never on a GPIO” and the sentence “the 2S pack touches VM and driver GND only.”
5. On the same card, sketch the HC-SR04 echo through a level shifter or the 1 kΩ / 2 kΩ divider. Do not connect the sensor.

You should read about 4.7 V to 5.1 V on the USB rail and about 3.25 V to 3.35 V on 3.3 V. A diode-dropped ESP32 5V pin near 4.7 V to 4.9 V is still a healthy USB rail; write the number rather than rounding it to “5 V.” A 3.3 V reading outside that window is a stop. A reading above 3.6 V on 3V3 means something is leaking 5 V in: unplug and find it. Do not connect the battery in this lab, not to “see what VM would be.”

![Order of connections: common ground, logic, signals, motor supply last, wheels up]({{ site.imgurl }}/generated/power_order.png)

The figure is the order the card is enforcing. You are still on the USB step. Motor supply is the last block, and the wheels are up when it finally becomes legal.

Faults. Black lead on the 5V pin and red lead on GND produces a negative number or a confusing zero; swap the leads and name GND again. Probing the metal can, or a capacitor, is not a rail measurement. A 0 V reading on 3V3 with a live USB port is a wrong pin, a missing ground, or a dead regulator. Stop. A classmate who powers a TT motor from the 5V pin will brown the board out the moment the motor stalls. That pin is USB 5 V.

Safety: the pack stays in the bag. Do not series the meter in current mode across 5V and GND. That is a short through the meter.

## Exercises

1. Compute the divider output for 5 V with $$1\,\mathrm{k}\Omega$$ on top and $$2\,\mathrm{k}\Omega$$ on the bottom. If both resistors are 5 percent high, does the ratio change?
2. Which terminal of a 2S 7.4 V pack may touch the TB6612, and which ESP32 header pins must it never touch?
3. A Pico is on the bench. Which label is USB 5 V, which label can accept about 1.8 V to 5.5 V, and which label is the regulated output? Where does 7.4 V do the most immediate damage?
4. Your meter reads 4.86 V and 3.29 V with USB only. Is that inside the window? What extra sentence does the pin card still need about VM?
5. Echo of an HC-SR04 is wired straight to GPIO 18 “just to see.” What voltage hits the pin, and what part should have been in series with that wire?

<details>
<summary>Answers</summary>

1. $$5 \times 2 / 3 \approx 3.33\,\mathrm{V}$$. If both resistors scale by 1.05 the ratio is unchanged, so the ideal node stays about 3.33 V. Unequal errors do not cancel. That is one reason a shifter is kinder than a divider built from leftover parts.
2. Pack positive may touch VM. Pack negative touches driver GND, and that GND must be common with the microcontroller. The pack must not touch any ESP32 GPIO, 3V3, or the 5V/VIN pin.
3. VBUS is USB 5 V. VSYS is the input that can take about 1.8 V to 5.5 V, with USB arriving through a diode. 3V3 is the regulated output. 7.4 V on 3V3 hits the regulator output directly; 7.4 V on VSYS is also outside the allowed window.
4. 4.86 V is inside about 4.7 V to 5.1 V, and 3.29 V is inside about 3.25 V to 3.35 V. The card still needs an explicit sentence that the 2S pack touches VM and driver ground only, and that the battery was not connected for the measurement.
5. The echo pin drives about 5 V into a 3.3 V GPIO, above the roughly 3.6 V absolute-maximum region. A level shifter (or, as a calculated compromise, the divider) belongs on that wire, with grounds tied. Unplug the echo before any further experiments.

</details>

## Further reading

- [SparkFun logic levels](https://learn.sparkfun.com/tutorials/logic-levels) — why a 5 V high and a 3.3 V input need a translator.
- [Pico datasheet](https://datasheets.raspberrypi.com/pico/pico-datasheet.pdf) — VBUS, VSYS, 3V3, and the allowed VSYS window.
- [ESP32 datasheet (PDF)](https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf) — GPIO electrical characteristics and absolute maximum ratings.
