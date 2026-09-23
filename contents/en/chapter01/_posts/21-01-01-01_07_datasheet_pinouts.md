---
layout: post
title: "Reading datasheets and pinouts"
chapter: "01"
order: 7
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter01
lesson_type: required
draft: false
---

A datasheet is the only page allowed to permit a wire. This lesson fixes one reading order, then uses it on the TB6612FNG module the diff-drive cart buys and on the ESP32 pin that must not meet a 5 V echo pulse.

## Learning objectives

You will open an unfamiliar PDF and walk it in one order every time: absolute maximum ratings, pinout and pin names, recommended operating conditions, the electrical characteristics you will actually use, the typical application schematic, and the package drawing that locates pin 1. You will copy, for a TB6612-class module, the motor-supply window, the logic-supply window, the standby rule, and the continuous and peak current, and you will place AIN1, AIN2, PWMA, BIN1, BIN2, PWMB, AO1, AO2, BO1, and BO2 on a card. You will point at the ESP32 absolute-maximum row and say why an HC-SR04 echo wire is forbidden on a bare GPIO. You will treat a clone module's silkscreen as a rumor until a meter and the datasheet agree.

## Prerequisites

You need Ohm's law from lesson 01, the meter habits from lesson 02, and the polarity habit from lesson 04. You do not power a motor today. Bring a notebook page you will still have in Chapter 02.

## Why it matters

The capstone is a differential-drive cart: two TT gearmotors, a TB6612FNG module, and a 3.3 V ESP32 or Pico. VM comes from a separate motor battery. VCC may sit on the 3.3 V rail. The HC-SR04 echo pin is a 5 V output, and those GPIO pins are not 5 V inputs. Sticker-reading shows up later as wheels that never leave standby, or as a GPIO that dies when the ranger answers. The order below finds the one number that forbids the wire before you build it.

![What an H-bridge does with the motor output pins]({{ site.imgurl }}/generated/hbridge_concept.png)

Each motor sits between a pair of outputs. Direction is which output is high, speed is how often PWM allows that state, and none of it happens while standby holds the bridge off. Use the figure after you have the pin names, not instead of the table.

## A reading order you do not shuffle

**1. Absolute maximum ratings.** This table is the damage fence. Past it, the maker stops promising the part survives. It is not a recommended operating point. Copy the one cell that matches the wire you want: supply voltage, logic-pin voltage, or output current. If the plan crosses that cell, the plan is forbidden.

**2. Pinout and pin names.** The pin table is a dictionary. AO1 is not "left wheel" until you choose which plug lands on AO1. On a TB6612FNG module the names you must be able to touch with a pencil are AIN1, AIN2, PWMA, BIN1, BIN2, PWMB, AO1, AO2, BO1, and BO2, plus VM, VCC, GND, and STBY. Inputs are pins a GPIO may drive. Outputs are pins that may touch a motor. Mixing those groups puts motor current into the microcontroller.

**3. Recommended operating conditions.** The robot lives here, in the region where the other tables were measured. A module listing can be tighter than the bare die, because copper and headers are part of the object. When the listing is tighter, it wins.

**4. Electrical characteristics you will actually use.** Skip rows you cannot measure yet. For this driver, copy the minimum voltage that still counts as a logic high, the fact that STBY must be high or every other row is meaningless, and the continuous and peak output current.

**5. Typical application schematic.** Copy the idea: a capacitor near VM, a capacitor near VCC, one common ground, inputs driven by another chip. A breakout may already hold the small capacitors. An extra capacitor does not replace a missing ground.

**6. Package drawing, for pin 1.** The drawing is a top view: you look down on the plastic, pins pointing into the board. Pin 1 sits by the dot or the bevel. A bottom-view photo mirrors the row. If the dot and the silk disagree about AO1, the meter settles it.

Clone boards lie in ink. A "5V" label on a 3.3 V logic pin, GND swapped with VM, an ECHO arrow aimed at trigger: all of these ship. Power only that rail from a current-limited supply, black lead on ground, and write the volts on the card. The silkscreen does not vote after that.

## Worked walkthrough: the TB6612FNG

Use the module window this course buys, and the Toshiba behavior summarized on Pololu's carrier page in Further reading. If a cell on that page disagrees with this text, the page wins. If your own module listing is tighter than both, the listing wins.

Absolute maximum ratings come first so a reversed pack or an over-voltage battery is rejected before the connector mates. That table is the fence. The next paragraphs are where you are allowed to live.

Pin names come second. Motor A is commanded by AIN1 and AIN2, and its speed pin is PWMA. Motor B is BIN1, BIN2, and PWMB. The pads that touch the motor leads are AO1 and AO2, or BO1 and BO2. STBY is not a spare GPIO. On this chip it is the off switch for both bridges. The control table contains no motion until STBY is high. Many modules pull STBY down on the board, so a forgotten wire leaves both wheels stopped while your notes say "forward."

Recommended conditions come third. For the module this course treats as the buy, VM is 4.5–10 V. A single lithium cell near 3.7 V is under that floor. A pack that sits above 10 V when charged is over the module ceiling even if a bare-die PDF looks kinder. Logic VCC is 2.7–5.5 V, so a 3.3 V rail is a legal logic supply. USB 5 V is inside that logic window and is still a bad motor supply, which is lesson 09. VM and VCC are different pins on purpose.

The rows you will use come fourth. Continuous current is about 1.2 A per channel and peak is about 3.2 A. Two TT motors free-running sit well under 1.2 A. Stall does not. Park a stall on that continuous rating and the driver becomes the fuse. Also copy the logic-high rule. Many printings set

$$
V_{IH,\min} = 0.7 \times V_{CC}
$$

At $$V_{CC} = 3.3\,\mathrm{V}$$ that is $$2.31\,\mathrm{V}$$. A GPIO driven to 3.3 V clears it. The same fraction at 5 V is $$3.5\,\mathrm{V}$$, and a 3.3 V GPIO does not clear 3.5 V. That single number forbids "power the logic pin from 5 V because the silk says so, then drive the inputs from the ESP32." Feed VCC from 3.3 V. Do not live in the gap and hope the input "mostly" works.

The schematic comes fifth. VM to the motor battery, VCC to 3.3 V, grounds joined, motors on AO1/AO2 and BO1/BO2, four GPIOs on AIN1, AIN2, PWMA, and STBY. A bulk capacitor goes across VM, stripe correct; lesson 09 sizes it. The package drawing comes sixth: mark pin 1 even if you only touch headers.

"Clockwise" in the datasheet follows the motor leads, not the nose of the chassis. With STBY high, opposite levels on AIN1 and AIN2 plus PWMA high runs the motor; swapping AIN1 and AIN2 reverses it; STBY low forces standby anyway. The first later motion test is STBY high, the direction pins different, and a modest PWM.

## The ESP32 GPIO is not a place to live at 5 V

Open the Espressif PDF and use the same order. The absolute-maximum voltage on a GPIO sits at the 3.3 V rail, a few hundred millivolts above it, not at 5 V. Recommended operation is that 3.3 V I/O supply. The absolute-maximum row is the fence, not a place to live. A 5 V pulse is outside the fence.

The HC-SR04 makes the fence concrete. Powered from 5 V, its echo wire swings to about 5 V when the pulse returns. That absolute-maximum cell forbids a direct connection to any ESP32 GPIO. Trigger is an input on the sensor and can usually be driven from 3.3 V. Echo cannot. A divider is later work; today the card says "echo not direct" and quotes the voltage. A Pico matches this limit: the Raspberry Pi documentation describes 3.3 V pins that are not 5 V tolerant, and code uses the GP numbers, not a count of pads from the USB end.

If a clone board prints "5V" beside a hole you hoped was a GPIO, measure it with USB plugged in and nothing else attached. A hole that sits near 5 V is a supply pin. It is not an echo input, and it is not an LED pin without a resistor.

## Lab

Nothing spins. You file two cards.

1. Title two pages, "MCU pinout" and "driver pinout." Date them. If the board has not arrived, build the MCU card from the ESP32 PDF and write "board not purchased."
2. On the driver card, show all six steps. Copy VM 4.5–10 V, VCC 2.7–5.5 V, "STBY must be high," 1.2 A continuous, and 3.2 A peak. Sketch the header and label AIN1, AIN2, PWMA, BIN1, BIN2, PWMB, AO1, AO2, BO1, BO2, VM, VCC, GND, and STBY. If the silk differs, keep two columns.
3. On the MCU card, copy the GPIO absolute-maximum voltage and the table name. Write that HC-SR04 echo is a 5 V output and does not land on a GPIO. Assign legal outputs to AIN1, AIN2, PWMA, and STBY. On a typical ESP32 module, skip flash pins and input-only pins.
4. Leave VM unpowered. If you can feed only logic from a current-limited 3.3 V source, measure silk "5V" and silk "3V3" with black on ground. Otherwise write the meter steps and mark "dry-run."
5. File both cards. `ch01-07-mcu-card` and `ch01-07-driver-card` are enough if Chapter 02 can still read them.

Stop if a pin gets hot, or if a hole you were about to call a GPIO measures near 5 V.

## Exercises

Each answer names one number, the table it came from, and the wire that number forbids.

1. Someone wires HC-SR04 ECHO straight to ESP32 GPIO 4 and says the absolute-maximum table will cover it. Which number forbids the wire, and what would you write down if you measured the echo pulse with the sensor powered from 5 V?
2. Driver silk says the logic pin wants 5 V. The ESP32 high is 3.3 V. Compute $$0.7 \times 5$$ and $$0.7 \times 3.3$$. Which result forbids driving those inputs from the ESP32, and which VCC removes the forbid?
3. Both TT motors are about to be tied to the ESP32 5 V pin "just for a test." USB is budgeted near 500 mA. The driver is rated 1.2 A continuous. Which number fails first, and why is the larger one not permission to use USB as VM?
4. STBY is unconnected and the sketch never drives it. Which chip behavior forbids PWM from turning a wheel, and what one GPIO action removes it?
5. A DRV8833 board shows up instead of a TB6612. What forbids copying AIN1, PWMA, and STBY from today's card onto that silk, and which further-reading page do you open?

<details markdown="1">
<summary>Hints and answers</summary>

1. The forbid is the ESP32 GPIO absolute maximum, a limit sitting at the 3.3 V rail, not at 5 V. Echo pulses to about the sensor supply, near 5 V. Write that measured high next to the cell. The direct wire is already illegal; a divider is later work.
2. $$0.7 \times 5 = 3.5\,\mathrm{V}$$, which a 3.3 V GPIO does not reach, so VCC at 5 V is forbidden for those inputs. $$0.7 \times 3.3 = 2.31\,\mathrm{V}$$, which the GPIO does reach. Feed VCC from 3.3 V.
3. The 500 mA USB budget fails first. Stall current of even one TT motor is far above that, and two motors are worse. The 1.2 A figure is the driver's continuous ceiling, not a promise that USB can source it. VM stays on the motor battery.
4. STBY held low, including an undriven pin that the chip or the module pulls down, keeps both bridges in standby. Drive STBY high and hold it there while motion is allowed.
5. Names do not transfer across driver families. Open the TI DRV8833 page and repeat the six steps. Label whatever that datasheet actually prints.

</details>

## Further reading

- [Pololu TB6612FNG carrier](https://www.pololu.com/product/713) — Toshiba behavior in short English: logic range, standby, and the 1.2 A / 3.2 A story. Let this page correct the lesson if a cell differs, and let your module listing win when it is tighter.
- [ESP32 datasheet (PDF)](https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf) — absolute maximum ratings and the GPIO list for the echo question.
- [TI DRV8833](https://www.ti.com/product/DRV8833) — the other driver the chapter checklist allows you to label. Start here if the chip in the photo is not a TB6612.
- [Raspberry Pi Pico documentation](https://www.raspberrypi.com/documentation/microcontrollers/raspberry-pi-pico.html) — 3.3 V I/O, pin 1, and the GP numbers the code must use.

## Where to buy in Vietnam

The ESP32 or Pico, the TB6612-class module, the TT motors, and the HC-SR04 are already on the kit list in Chapter 00, lesson 05, [Bill of materials and how to buy the kit in Vietnam]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %}). Buy them from that lesson. Do not start a second kit here, and do not buy a loose fine-pitch TB6612FNG to hand-solder for the capstone.

If you still have no meter, the silkscreen check needs one. A known page is the UNI-T UT33D at [Hshop](https://hshop.vn/dong-ho-van-nang-dien-tu-digital-multimeter-uni-t-ut33d-chinh-hang). Read the live price. Comparing shops is fine at [Hshop](https://hshop.vn/), [Thế Giới IC](https://www.thegioiic.com/), and [IC Đầy Rồi](https://icdayroi.com/).
