---
layout: post
title: "Transistors, MOSFETs, regulators, and IC packages"
chapter: "01"
order: 5
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter01
lesson_type: required
draft: false
---

## Learning objectives

By the end of this lesson you will be able to refuse a pinout that was guessed from the package shape. A TO-92 or a TO-220 can be a 2N2222, a BC547, a 2N3904, an AMS1117, a 7805, or a small MOSFET, and only the printing knows which. You will number a DIP from the dot or notch, counterclockwise. You will explain why a MOSFET gate is not a current-driven base, and why $V_{GS(th)}$ is not the voltage at which a motor switch is fully on. You will compare a 2N2222 used as a lamp switch with the TB6612 the robot actually needs, and you will say why 12 V must not be poured into an ESP32 5 V pin in the hope that the onboard regulator will cope.

## Prerequisites

You can tell a diode's cathode by its band, and you can use diode mode on an unpowered part. You know a GPIO is a 12 mA to 40 mA object and a stalled TT motor is an ampere-class object. This lesson is identification, plus the two ratings that stop a smoked part: pin order, and heat while dropping voltage.

## Why this matters on the diff-drive robot

The ESP32 board hides an AMS1117-3.3, or something in that family, between USB 5 V and the 3.3 V rail. The Pico has its own regulator between VBUS and 3V3. Those parts are why the board can speak 3.3 V logic to a TB6612, whose logic range is about 2.7 V to 5.5 V. They are not permission to feed a 12 V pack into the pin marked 5V.

A small transistor looks like a way to switch one TT motor from a GPIO. The motor is inductive, so it needs a flyback path when the switch opens, and stall current sits near or above what a 2N2222 wants to carry. A MOSFET chosen because its threshold is "only 2 V" may still be half-on at 3.3 V and hot. The TB6612 already solves this for two channels, at 1.2 A continuous and 3.2 A peak. This lesson is how you recognize the packages so you do not install a regulator where a transistor was drawn.

## Packages, and why the printing wins

TO-92 is the little black blob with three leads. TO-220 is the larger tabbed package. Both shapes are shared by different silicon. A 2N2222, a BC547, and a 2N3904 are small bipolars with different pin orders. The P2N2222 and the 2N2222 are a famous pair: same family, different lead order. An AMS1117 and a 7805 are regulators, not switches. A small MOSFET in TO-92 will not survive being wired from a 2N2222 pinout you memorized.

![Several packages that share a silhouette and not a pinout]({{ site.imgurl }}/generated/component_lookalikes.png)

Read the printing on the flat face, then open that exact datasheet. If the marking is rubbed off, the part is unknown. Do not try pin orders on a live GPIO.

A dual-inline package is numbered from the notch or the dot. Notch at the top, pin 1 is upper left. Numbers run down the left side, then up the right side: counterclockwise as you look at the top. The same rule matters when a level-shifter chip straddles the breadboard trench.

## Bipolar switch, MOSFET, and the number $V_{GS(th)}$ is not

An NPN used as a switch wants base current, often on the order of a tenth of the collector current, through a resistor from the GPIO. For a 150 mA load that is already about 15 mA, most of a cautious GPIO budget. For an 800 mA stall the same rule wants about 80 mA, which a GPIO does not have, and the 2N2222's own rating is then the next limit. When the switch opens, motor current does not stop instantly. It needs a flyback diode, band toward the motor supply, or the spike lands on the collector.

A MOSFET gate is different. In normal switching you do not push a continuous gate current. You charge the gate up to a voltage, and the channel's resistance is set by how far that voltage sits above the source. $V_{GS(th)}$, the threshold, is the gate voltage where the manufacturer measured a tiny test current, often a quarter of a milliamp. It is the start of conduction, not a promise of low $R_{DS(on)}$. A datasheet might list threshold anywhere from about 2 V to 4 V and then specify $R_{DS(on)}$ only at $V_{GS} = 4.5\ \mathrm{V}$ or $10\ \mathrm{V}$. Drive the gate at "just threshold" and the FET stays in its linear region: it drops volts, it gets hot, and the motor is slow.

A logic-level MOSFET is one whose low on-resistance is specified at a logic-sized $V_{GS}$, sometimes 4.5 V and sometimes 2.5 V. Even a good one, used as a low-side switch for a single TT motor, still needs a flyback diode. Two motors, two directions, and PWM are why the cart uses a TB6612 instead of a transistor you identified today. The driver is still a set of MOSFETs. You are just not hand-wiring their gates on a breadboard for the capstone.

## Regulators, and the watt you throw away

A linear regulator such as the 7805 holds its output at 5 V by dropping the excess input voltage as heat. The power in the regulator is the drop times the current:

$$
P = (V_\mathrm{in} - V_\mathrm{out}) \, I
$$

Work a mild case. A 9 V supply, a 5 V output, and 200 mA of load:

$$
P = (9 - 5) \times 0.2 = 0.8\ \mathrm{W}
$$

A TO-220 with a little copper or a small tab can do that. It will be warm. Now imagine 12 V poured into the 5 V pin of an ESP32 board whose AMS1117-3.3 then makes 3.3 V for a board that draws 150 mA once Wi-Fi is up:

$$
P = (12 - 3.3) \times 0.15 \approx 1.3\ \mathrm{W}
$$

That is a lot for a small SOT-223 sitting on a thin module, and it assumes the only victim is the regulator. On many dev boards the pin marked 5V is also the USB 5 V node. Twelve volts there can reach the USB socket and the USB-serial chip. The AMS1117's own absolute maximum is not a promise about the rest of the board. Power the ESP32 or the Pico from USB while you are on the bench. Put the motor pack on TB6612 VM only, inside about 4.5 V to 10 V. Share ground. Do not hope.

## Worked example: sort the marking, then the junction

Suppose the tray contains four parts whose bodies you must not trust: a TO-92 printed BC547, a TO-92 printed 2N2222, a TO-220 printed 7805, and a small MOSFET whose marking you can actually read as a MOSFET. The families are: BC547 and 2N2222 are NPN bipolars with different pinouts; the 7805 is a 5 V linear regulator; the MOSFET is a voltage-controlled switch. Nothing in that sentence tells you which lead is the emitter. The printing plus the datasheet does.

Out of circuit and unpowered, diode mode on a bipolar junction is a sanity check, not a full pinout. The base-emitter junction and the base-collector junction each behave like a diode, near 0.6 V one way and open the other. The emitter-collector path should not beep like a wire in both directions. If you find two junctions that share a common lead, that common lead is a candidate for the base. Stop there. Do not declare the emitter versus the collector from one afternoon of probing, and do not install the part on a GPIO until the datasheet agrees. A regulator will not show two tidy diode drops that match a 2N2222, which is useful: if your "transistor" does not diode-test like a transistor, it may be the 7805 you were about to wire as a switch.

The robot still does not get a 2N2222 on the TT motor after a successful diode test. Direction and braking want an H-bridge. The TB6612 module we use is rated 1.2 A continuous and 3.2 A peak, with logic that accepts 3.3 V. That is the switch.

## Hands-on lab

1. If you have loose parts, sort them by the printed marking into bipolar, MOSFET, regulator, or unknown. If you only have the photographs in this lesson and the boards in the kit, sort those pictures the same way and write the family next to each.
2. On any DIP you can see, find the notch or dot and number pin 1. Confirm the count runs down one side and up the other.
3. On the ESP32 board, find the small regulator near the USB connector if the silk or the body shows an AMS1117-class marking. Do not apply 12 V to test it. Note which pin is labeled 5V and which is 3V3.
4. Unpowered, out of circuit, diode-test one known diode and one known bipolar transistor if you have them. Record the two junctions. If you do not have a loose transistor, skip the probe and keep the written sort from step 1. Do not diode-test a part that is still soldered to a powered board.

You should end with a labeled list, not with a motor that spins. A successful diode test shows about 0.5 V to 0.7 V on two junctions that share a pin, and no short from emitter to collector. The 7805 does not join that list.

| What you see | Likely cause | What to change |
| --- | --- | --- |
| Two TO-92 parts, one pinout assumed for both | Different markings, or 2N2222 versus P2N2222 | Read the print. Open that datasheet. Do not copy the first pin order. |
| Diode test shows a short both ways on every pin | Part damaged, or probes on a soldered circuit that is not empty | Lift the part. If it is still a short, discard it. |
| Regulator gets hot on 12 V into a 5 V pin | Linear drop times board current, and 12 V on a USB-named rail | Remove 12 V. Power the board from USB. Motor pack goes to VM only. |
| MOSFET barely warm at the gate, motor slow and FET hot | Gate held near $V_{GS(th)}$, channel not fully on | This is why the capstone uses a TB6612, not a threshold-biased FET. |

Safety: no motor supply in this lab, no 12 V experiments, diode mode only on loose parts. A TO-220 tab on a regulator can be electrically live and hot on a finished board; do not grab it to see if the robot is working.

## Exercises

1. A DIP has a notch. Looking down, where is pin 1, and which way do the numbers run?
2. A MOSFET datasheet lists $V_{GS(th)}$ from 2 V to 4 V at $250\ \mu\mathrm{A}$, and $R_{DS(on)}$ only at $V_{GS} = 10\ \mathrm{V}$. Why is "the threshold is 2 V, and my GPIO is 3.3 V" not a motor-drive design?
3. Compute the heat in a 7805 that drops 12 V to 5 V at 300 mA. Would you bolt that tab to something?
4. A 2N2222 is proposed as the low-side switch for one TT motor at 0.8 A stall, with base current "a tenth of collector current" from a GPIO. Estimate the base current and say what else the motor still needs when the transistor turns off.
5. Why is an unmarked TO-92 a worse spare than no spare at all for the ESP32's 3.3 V regulator?

<details>
<summary>Suggested answers</summary>

1. Pin 1 is at the upper left of the notch. Numbers run down the left side, then up the right side: counterclockwise as you look at the top.
2. Threshold is where a tiny test current begins. $R_{DS(on)}$ at 10 V says nothing reliable about 3.3 V. The FET may be only partly on, hot, and dropping voltage the motor needed. A logic-level part specifies on-resistance at a low $V_{GS}$, and the capstone still uses a driver.
3. $P = (12 - 5) \times 0.3 = 2.1\ \mathrm{W}$. Yes. A bare TO-220 at 2 W is a burn, and it is still the wrong way to power an ESP32.
4. Base current on that rule is about $0.8 / 10 = 80\ \mathrm{mA}$, far above a 12 mA to 40 mA GPIO. The motor also needs a flyback diode. Use the TB6612.
5. An unmarked TO-92 might be a bipolar transistor, a MOSFET, or something else. Installing it in place of an AMS1117 can short 5 V onto the 3.3 V rail. An unknown part is not a regulator until the marking says so.

</details>

## Further reading

SparkFun's transistor tutorial is the bipolar and MOSFET picture without a homemade motor stage: [Transistors](https://learn.sparkfun.com/tutorials/transistors). The 7805 family, including the dropout you just turned into heat, is documented on TI's product page: [LM7805](https://www.ti.com/product/LM7805). Read the marking on your part before you borrow either pinout.

## Where to buy in Vietnam

You do not need a loose transistor to finish the diff-drive robot. The switch is the TB6612 already on the cart in [Bill of materials and how to buy the kit in Vietnam]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %}). Buy the driver, the ESP32 or Pico, and the motors there, not a grab-bag of TO-92 parts.

If you want one known diode and one known bipolar transistor for the unpowered junction lab, buy them from a counter that prints the part number on the bag, such as [Thế Giới IC](https://www.thegioiic.com/) or [IC Đây Rồi](https://icdayroi.com/). This lesson has no verified single-product slug for a 2N2222, so do not invent one. A search page, if you use a marketplace, should be treated as a search page: [Shopee search for 2N2222](https://shopee.vn/search?keyword=2N2222). Read the marking when it arrives, and do not pay a fantasy price for an unlabeled strip. The ESP32 board you already need was 190 000 ₫ on Hshop on 23 September 2026 and already carries its own 3.3 V regulator: [ESP32 NodeMCU-32S](https://hshop.vn/kit-rf-thu-phat-wifi-ble-esp32-nodemcu-32s-ch340-ai-thinker).
