---
layout: post
title: "Breadboards, multimeters, and safe probing"
chapter: "01"
order: 2
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter01
lesson_type: required
draft: false
---

## Learning objectives

By the end of this lesson you will be able to point to a five-hole terminal strip, the center trench, and a power rail, and say which holes are actually the same wire. You will predict that many full-size breadboards split each power rail in the middle, and you will prove the split with a continuity beep rather than with a guess. You will put the meter on DC volts in parallel, refuse to measure current through a USB charger in this lab, and measure resistance only on an unpowered part. You will also start every voltage reading on a range above the voltage you expect, with your fingers off the probe tips.

## Prerequisites

You should know a volt from an ampere, and that a status LED needs a series resistor. This lesson does not derive Ohm's law again. It teaches which holes are one node, and which meter setting reads voltage rather than shorting the source. A multimeter and one solderless breadboard are enough.

## Why this matters on the diff-drive robot

On the capstone the ESP32 or Pico, the TB6612, and the TT motor leads meet on a breadboard or on Dupont pins that obey one rule: five holes in a column are one node, and the trench is a wall. A rail split in the middle, a jumper that missed the spring, or a meter lead left in the current jack looks like a dead robot when the chip never received power. The TB6612 logic is 3.3 V from the microcontroller, while VM is a separate motor supply. If you "fix" a silent bridge by jumpering 5 V onto a GPIO, a measurement mistake becomes a damaged pin. The HC-SR04 echo is a 5 V output; you will not discover that safely by poking at random. This lesson is the beep and the voltage check, done while the robot is still parts in a tray.

## How a breadboard is actually wired

A solderless breadboard is a grid of spring clips under colored plastic. A lead pressed into a hole is tied to every other hole on the same clip. You do not get a gas-tight joint. A lead that is too short or dirty can look inserted and still be open, so the meter decides whether a node exists.

The long rows along the edges are the power rails, usually marked red and blue or black. Every hole along one unbroken colored line is the same conductor. The top red rail is not the bottom red rail. On many full-size boards, including a typical 830-point board, the clips also stop at a gap in the middle, and the colored line is printed broken there. Feed 5 V into the left end and the right end stays dark until you jumper across that gap. Some mini boards have no gap. Measure yours.

![Breadboard anatomy: rails, five-hole strips, and the center trench]({{ site.imgurl }}/generated/breadboard_anatomy.png)

The center field is the terminal strips. Each column has five holes above the trench and five holes below it. Those five holes are shorted vertically. The next column over is a different net. The trench running the long way down the middle is an insulator: a hole on the near side is not connected to the hole with the same column number on the far side. That gap exists so a DIP chip can straddle the trench without its own pins shorting together. If you probe "both sides of the same column" and expect a beep, you are asking the trench to be a wire.

Landing both LED leads in the same five-hole column shorts the LED. Landing them on opposite sides of the trench, with nothing joining the sides, opens the circuit. Both mistakes look tidy.

![A solderless breadboard, rails along the edges]({{ site.imgurl }}/wikimedia/breadboard.jpg)

## What the meter dial is actually asking

Three habits prevent almost every blown fuse in a student lab. The black lead lives in COM for every measurement in this course. The red lead lives in the jack marked V, Ω, or similar whenever you measure voltage, resistance, or continuity. The red lead moves to a current jack only for a current measurement, and it moves back when you are done. Leaving it in the current jack and then "measuring voltage" places the meter's current shunt straight across the supply. That is nearly a short. The mA fuse opens. Voltage readings still work afterwards, which hides the damage until the day you need current.

![A digital multimeter: dial, display, and lead jacks]({{ site.imgurl }}/wikimedia/Digital_Multimeter_Aka.jpg)

DC voltage is measured in parallel. The circuit stays connected. You touch the two points whose difference you want. Swapped leads on a digital meter give a minus sign, not a broken part. The dial sits on a DC range above the voltage you expect: 20 V covers USB 5 V and a 2S pack near 8.4 V. An autoranging meter still needs the DC volts symbol, not ohms. You are looking across a part, not inserting yourself into the current.

Current is measured in series. You break one wire so the current flows through the meter, and only after the red lead is in the current jack. This lesson does not measure current on a USB charger or on a GPIO. A charger will try to feed an amp or more into a meter placed across its output, and stall current from a TT motor can open a cheap mA fuse in one twitch. Resistance and continuity require an unpowered circuit, because the meter applies its own small test voltage. Continuity beeps on a wire or a closed spring. A 180 Ω resistor is silence on many continuity settings: continuity means "almost a short," not "any connection." Use ohms when you want the number.

## Worked example: the rail that looks powered and is not

A USB charger is jumpered to the left-hand red and blue rails of an 830-point board. Nothing else is plugged in. No ESP32, no GPIO. The meter is on the 20 V DC range, black in COM, red in the voltage jack.

On the left red rail, relative to the left blue rail, the meter reads 5.08 V. That is a healthy charger, a little above the nameplate 5 V, which is normal. Move the red probe to the right-hand red rail, past the printed break in the colored line, and keep black on the left blue rail. The meter reads 0.02 V. That is not "a bit of loss in the wire." It is an open circuit. Set the charger aside, power everything down, and switch to continuity. Probing along the red rail across the middle gap is silence. One short jumper across the red gap, and another across the blue gap, and the right-hand rail then reads 5.07 V with the charger restored.

The current jack is nearly a short, which is why this lab never uses it on that charger. A rough picture of a 10 A shunt, on the order of a hundredth of an ohm, gives

$$
I \approx \frac{5}{0.01} = 500\ \mathrm{A}
$$

in a fantasy where the charger could supply it. A real charger folds back to an amp or two, which is already enough to open a 200 mA fuse and is not a measurement of "how much current the robot needs." You learned in the previous lesson that two stalled TT motors want on the order of an ampere each. You will measure that later, in series, on the motor supply, for a short pulse, with the red lead in a jack rated for it. You will not learn it by shorting a USB port.

## Hands-on lab

1. Unplug every supply. Seat black in COM and red in the voltage/ohms jack. Turn the dial to continuity.
2. Beep a jumper from metal end to metal end. You should hear a beep. Press one end into the red rail and the other into a five-hole row. Beep from another hole in that same row back to a second hole on the rail: beep. Beep from that row to the neighboring row: silence.
3. Beep across the center trench at the same column number. Expect silence. The trench is not a wire.
4. Find the rail break. Beep from a hole on the left half of the red rail to a hole on the right half. On a typical 830-point board this is silence, and the colored line is printed with a gap. Bridge the gap with one jumper and beep again. Expect a beep. Do the same for the blue rail.
5. Only then measure voltage. Use a USB phone charger or power bank, not a GPIO and not the 3V3 pin. If you have a USB breakout, land 5 V and GND on the rail you just proved. If you are probing a loose cable, use the charger end you understand, red on 5 V and black on GND. Dial on a DC range above 5 V, commonly 20 V. Read the display.

You should hear a beep through a good jumper and through one row, silence across the trench, and silence across the middle of the rail until you add the bridge. The charger reading should sit near 4.7 V to 5.3 V. A reading near 0 V after continuity already beeped means you are not on the rail you think, or the charger is not the source you think.

| What you see | Likely cause | What to change |
| --- | --- | --- |
| No beep through a jumper that looks seated | The pin missed the spring, or that clip is bent | Move to another hole in the same column. If the whole column is dead, abandon it. |
| Left rail reads about 5 V, right rail reads about 0 V | The middle break is open | Add one jumper across the red gap and one across the blue gap, then measure again. |
| Continuity beeps while the charger is still plugged in | You measured ohms or continuity on a live circuit | Unplug first. The ohms circuit is not a voltage meter. |
| Display flashes, then every mA reading is zero while DC volts still works | Red lead was in the current jack and got placed across the charger | The mA fuse opened. This lab does not replace that fuse by trying the same short again. |

Safety: start on a voltage range above what you expect, so a 2S pack near 8 V is not first met on the 200 mV scale. Keep your fingers off the probe tips whenever you measure a pack or a charger; the tip is the only metal that should touch the circuit. Do not measure current on USB in this lesson. Do not land the charger on an ESP32 or Pico GPIO to "see if 5 V is there."

## Exercises

1. A board has 30 columns on each side of the trench, and both the top and bottom power-rail pairs are split once in the middle. How many separate five-hole nodes are in the terminal field? How many separate rail segments are there?
2. You want the voltage across a 180 Ω resistor that is already lighting an LED from 3.3 V. Which jack, which dial position, and do you disconnect the LED?
3. A jumper beeps from metal end to metal end and reads about 0.3 Ω. Once pressed into a hole, that hole does not beep to the other end of the wire. Where is the open?
4. A classmate tried to "measure USB current" by placing the meter across 5 V and GND, saw a flash, and now the mA range reads zero while the 20 V range still shows the charger. What failed?
5. Why is a beep on the continuity setting not a sufficient check that a 180 Ω LED resistor is the right part?

<details>
<summary>Suggested answers</summary>

1. Each side of each column is one node, so $30 \times 2 = 60$ five-hole nodes. Top red, top blue, bottom red, and bottom blue, each split in two, is 8 rail segments.
2. Black in COM, red in the voltage/ohms jack, dial on DC volts above 3.3 V. Probes go across the resistor, in parallel, while the LED stays in the circuit. Disconnecting the LED opens the loop and the resistor voltage collapses.
3. The wire is intact. The open is between the pin and the spring. Move the pin to another hole in that column. Do not throw away a jumper that already beeps end to end.
4. The mA fuse opened. The meter was being used as a short across the charger. Voltage readings survive because they do not use that fuse. Do not repeat the measurement to "confirm."
5. Continuity is a near-short detector. A 180 Ω part is usually silent, and so is a 100 kΩ part. Only the ohms range, on an unpowered resistor, tells those two apart.

</details>

## Further reading

SparkFun's breadboard tutorial matches the rails, strips, and trench in the figure above: [How to use a breadboard](https://learn.sparkfun.com/tutorials/how-to-use-a-breadboard). Their meter tutorial is the jack discipline with a photograph of each function: [How to use a multimeter](https://learn.sparkfun.com/tutorials/how-to-use-a-multimeter). Read the current section, then look again at which jack your red lead is in before you close a circuit.

## Where to buy in Vietnam

The full robot cart, including the ESP32 or Pico, the TB6612, the TT motors, and the HC-SR04, is in [Bill of materials and how to buy the kit in Vietnam]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %}). This lesson only adds the bench tools if they are not already on that list.

Prices below were read on Hshop on 23 September 2026. Confirm the live listing before you pay.

An 830-point breadboard was 35 000 ₫: [test board CAMMB-102](https://hshop.vn/test-board-cammb-102). Male-to-male jumpers, 40 wires, were 30 000 ₫: [dây cắm breadboard đực-đực](https://hshop.vn/day-cam-breadboard-duc-duc-20cm-cap-det-40-soi-m-m-jumper-wire). The UNI-T UT33D+ meter was 285 000 ₫: [đồng hồ vạn năng UNI-T UT33D+](https://hshop.vn/dong-ho-van-nang-dien-tu-digital-multimeter-uni-t-ut33d-chinh-hang). Any substitute meter still needs a continuity beeper and a fused milliamp range you promise not to short across USB.
