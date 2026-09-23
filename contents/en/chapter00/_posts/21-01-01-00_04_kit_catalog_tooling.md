---
layout: post
title: "The bench catalog: tools you can trust"
chapter: "00"
order: 4
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter00
lesson_type: required
draft: false
---

Plan about 90 minutes. If you already have a meter, prove it on a known short and put it away. If you do not, finish the Wave 1 inventory and photograph the gaps. Do not heat an iron in this lesson.

## Learning objectives

You will **say** what each Wave 1 tool is for, and **state** the observation that proves it works. You will **select** DC volts and continuity on a meter, and you will **refuse** a resistance measurement on a rail that is still powered. You will **describe** a solder joint as the result of heating the parts, not of melting a blob onto cold metal, using 0.8 mm Sn63 and a stand. You will **distinguish** a breadboard, which is for signals, from a path that must carry motor current. You will **separate** side cutters from strippers by the damage each one avoids. You will **inventory** the bench against Wave 1, photograph it, and write the gaps down so lesson 00-05 is a shopping list rather than a guess.

## Prerequisites

The power-up card from lesson 00-03 exists, at least on paper. You know motor VM is not the 3.3 V pin, and you know an iron needs a stand and eye protection before it needs a plug. Chapter 01 is where probing becomes a measured lab. Today you are learning which tool answers which question, so that lab is not a walk to the shop in the middle of an exercise.

## Why it matters

Chapter 07 fails in boring ways: a jumper that looks seated and is open inside the crimp, a ground you "measured" while the meter was still in ohms on a live rail, a motor wire asked to live in a breadboard spring. Those failures look like firmware bugs. They will send you into ROS 2 tutorials that cannot beep a wire. The tools in this catalog are how you separate "the PWM timeout is wrong" from "the wire is wrong" before a topic graph exists to confuse you further.

## What "works" means for each tool

Wave 1, copied from the bill of materials so this lesson and lesson 00-05 agree, is the bench that lets Chapter 01 start: a multimeter, a 60 W iron with a stand, solder, side cutters, a solderless breadboard, jumper wires, a data-capable USB cable, the microcontroller, a few LEDs, and a tactile button. Wave 2 is the chassis, the TB6612FNG, and the HC-SR04. Wave 3 is the cells and a charger that charges one cell at a time. This lesson is Wave 1's tools. The microcontroller itself is a line on the inventory, not a tool you learn to swing.

![A family portrait of the bench, not a branded kit]({{ site.imgurl }}/generated/kit_catalog_overview.png)

The drawing is kinds of objects. The meter, the iron, the breadboard, and the hand tools are the must-have wave. A bench supply and a logic analyzer, if the picture includes them as later instruments, are not today's purchase. The bottom row, the board and the robot, is bought from lesson 00-05 when you are ready, not duplicated here.

### The meter

A digital multimeter answers three questions you will ask constantly, and one question you must not ask by accident.

**DC volts** measures a difference. The dial is on V with a straight line. Black on ground, red on the point you care about. A healthy USB 5 V pin is near 5 V. A healthy 3.3 V pin is roughly 3.2–3.4 V. A reading of 0.00 V means off, wrong pin, or not actually on ground. It does not mean the meter is broken until continuity has proved the leads.

**Continuity** beeps when the resistance between the probes is very small. Touch the probes together. You should hear a beep and see a display near 0 Ω, sometimes a few tenths of an ohm of lead resistance. That beep is the proof the meter works. A good short jumper beeps. **OL** means the meter cannot see a path.

**Ohms** keeps a number when there is no beep. Measure resistance only on an **unpowered** part. The meter injects a small current. On a powered rail that current fights the supply, the reading is nonsense, and you can damage the meter or the board. Never ohms on a powered rail.

Current mode is the trap. The red lead moves to a jack marked A or mA, and the meter becomes a near short. Probing a voltage that way shorts the source. Look at the jack before every voltage measurement.

![A handheld meter; the jacks matter as much as the dial]({{ site.imgurl }}/wikimedia/Digital_Multimeter_Aka.jpg)

Yours may be a UNI-T UT33D+ or a Wadfow. Either is enough if it beeps and reads DC volts. The proof of life is that beep, before you trust a number on the robot.

### The iron, the stand, and the solder

A joint is a metallurgical event between the pad and the pin. You heat those two pieces, then you let a little solder flow onto the hot metal. If you melt a blob on the tip and dab it onto a cold pin, you get a ball that looks occupied and falls off next week. That is the whole technique this lesson needs. Chapter 01 will ask you to solder; today you only need to know what "good" will look like: the solder wet both surfaces, the joint is shiny rather than a sphere sitting on top, and the neighbouring pad did not bridge.

The alloy on the course list is 0.8 mm Sn63/Pb37. The diameter is small enough for a header pin. The stand is not optional: a 60 W tip left on a cable will end the lab. Eye protection stays on when leads are cut, because the offcut is a projectile. Flux fumes are a reason to open a window, not a reason to hover.

![An iron without a stand is a picture of the hazard, not the setup you want]({{ site.imgurl }}/wikimedia/Soldering_iron.jpg)

Read the photograph as a bare iron, which is the hazard. Your iron goes in the stand. You will know the pair works when the iron stays put while you reach for solder. Chapter 00 does not require a practice joint.

### The breadboard is not a motor path

A solderless breadboard is a grid of spring clips under plastic. Holes in the same numbered row are connected. A trench down the middle lets a dual-inline chip straddle the board without shorting its two sides. The long strips along the edge are power rails, and on many 830-point boards those rails are **split in the middle**. A rail that does not beep from one end to the other is not a mystery. It is the gap the plastic already told you about.

![A solderless breadboard: fine for signals, wrong for motor current]({{ site.imgurl }}/wikimedia/breadboard.jpg)

The breadboard works when a jumper beeps from one end of a row to the other, and stays silent across the centre trench. Motor current does not belong in those springs. A stalled TT motor is a large fraction of an ampere, and the clip's resistance turns that into heat and a voltage drop. Signals live on the breadboard. Motor leads wait for the TB6612FNG screw terminals.

### Cutters and strippers

Side cutters shear a lead. They are the 170-size cutter on the shopping list. They work when a lead comes off cleanly and the offcut is caught. They nick copper if you use them as strippers, and the wire breaks later at the nick. Strippers remove insulation without biting the conductor. A knife is a worse substitute and belongs on the gap list. Jumpers also fail inside the crimp while the plastic looks fine, so a silent motor with a pretty PWM wire is a beep test.

### Later, and not now

A current-limited supply, a logic analyzer, and an oscilloscope make later debugging faster. None of them is required to pass Chapter 00, and none of them repairs a missing common ground. Write them down as later.

## Lab: inventory against Wave 1

Clear a corner of the desk. Lay out every Wave 1 item you actually possess. Do not borrow objects into the photo from another room "so it looks complete."

The lines are: multimeter, iron, stand, solder, side cutters, breadboard, jumper wires, data-capable USB cable, microcontroller, at least one LED, at least one tactile button. For each line write `here` or `gap`. Photograph the layout. Put the photo in the journal. In the serial-snippet field, write either the port name if the board enumerates on USB alone, or `cable unproven — board not here` or `cable unproven — no port appeared`.

Then prove the meter if you have one. Probes touching: beep. Record "beep on known short." No beep means the meter is not a tool yet. Do not measure ohms on anything plugged in. No meter means `meter missing`, and Chapter 01's measurement labs wait. If you have a breadboard, beep one row and confirm the centre trench is silent. If you have an iron, confirm the stand and leave the iron unplugged. The inventory does not need a hot tip.

**What you should see.** A photo, a gap list, and a beep or an explicit missing-meter line.

**When it goes wrong.** A friend's meter in the photo does not count. A beep on a powered board is not an ohms test; unplug first. Motor wires in the breadboard come out. One meter is the line, not two.

## Worked example

Quân's photo shows a Wadfow meter, a 60 W iron, no stand, a coil of 0.8 mm solder, cutters, no breadboard, a charge-only USB cable he has not proved, and no microcontroller. He writes gaps: stand, breadboard, jumpers, data cable, MCU, LED, button. He touches the meter probes together and gets a beep, so the meter line is `here`, with the evidence "beep on known short." He does not ohm-test the USB port while the cable is plugged into the laptop.

He prices only tool gaps, using the 23 September 2026 Hshop snapshots, and leaves the MCU to lesson 00-05. He already owns the iron, the solder, and the cutters. His gap today is the stand and the breadboard:

$$
40000 + 35000 = 75000
$$

đồng, plus jumpers and a data cable from lesson 00-05, plus the board. A full tool set for someone with an empty drawer, one meter not two, is the UT33D+ at 285000 ₫, or the Wadfow at 185000 ₫, plus iron 75000 ₫, stand 40000 ₫, solder 24000 ₫, cutters 35000 ₫, and an 830-point breadboard at 35000 ₫. With the Wadfow meter that sum is

$$
185000 + 75000 + 40000 + 24000 + 35000 + 35000 = 394000
$$

đồng. With the UT33D+ the empty-drawer total is 494000 ₫. Quân writes both figures, dated 23 Sep 2026, and does not order a scope.

## Exercises

1. The probes are touching and the meter is silent. May you measure the 3.3 V pin and trust the number? What do you check first?
2. You want the resistance of a 10 kΩ resistor that is still plugged into a powered ESP32 rail. Why is that measurement refused, and what do you do instead?
3. A solder joint looks like a ball sitting on the pin. Which step was skipped: heating the joint, or adding solder? How does 0.8 mm Sn63 change the amount you need?
4. A stalled motor lead is pushed into a breadboard hole because the screw terminal is in another room. What fails, electrically, and where should that wire wait?
5. Your Wave 1 photo has a meter and an iron and no stand, no solder, and no cutters. Which of those gaps can burn you or the cable before Chapter 01 even asks you to measure a resistor?

<details>
<summary>Suggested answers</summary>

1. No. A silent meter with the probes touching has not proved continuity. Check the dial, the lead jacks, and the battery before you trust a voltage.
2. Ohms mode injects current into a live rail. Unplug the board, lift one leg of the resistor if it is in circuit, and measure the part unpowered.
3. The pin and the pad were not heated; solder was dropped on as a blob. Thinner 0.8 mm wire lets you feed a small amount onto a hot joint instead of flooding it.
4. The spring clip is a poor, resistive contact for motor current. It heats and drops voltage. The wire waits for the driver screw terminal or a proper harness. Signals may use the breadboard.
5. The missing stand. A hot iron on the table or on its own cable is the immediate hazard. Missing solder and cutters block joints and lead trimming; they do not replace the stand.

</details>

## Further reading

- [How to use a multimeter (SparkFun)](https://learn.sparkfun.com/tutorials/how-to-use-a-multimeter) — volts, continuity, and the current-jack trap, with pictures.
- [Arduino language reference](https://docs.arduino.cc/) — not a tool manual. It is where the LED and the button on your Wave 1 list will be exercised once the board arrives. Do not start a motor tutorial from the homepage.

## Where to buy in Vietnam / Mua ở Việt Nam

Buy the gaps, not a second copy of what the photo already shows. The full robot cart remains [lesson 00-05]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %}). Prices below are Hshop snapshots from **23 September 2026**.

| Tool | Snapshot | Page |
| --- | ---: | --- |
| UNI-T UT33D+ meter | 285000 ₫ | [UT33D+](https://hshop.vn/dong-ho-van-nang-dien-tu-digital-multimeter-uni-t-ut33d-chinh-hang) |
| Wadfow WDM1501 meter | 185000 ₫ | [WDM1501](https://hshop.vn/dong-ho-van-nang-ky-thuat-so-vom-wadfow-wdm1501-digital-multimeter-true-rms) |
| Wadfow 60 W iron | 75000 ₫ | [WEL3616](https://hshop.vn/mo-han-60w-wadfow-wel3616-soldering-iron) |
| Round iron stand | 40000 ₫ | [stand](https://hshop.vn/de-gac-mo-han-tron-b-2-co-khay-roi) |
| Sunchi 0.8 mm Sn63/Pb37 | 24000 ₫ | [solder](https://hshop.vn/thiec-han-sunchi-kp26-0-8mm-sn63-pb37-solder-wire) |
| 170 side cutters | 35000 ₫ | [cutters](https://hshop.vn/kim-cat-day-dien-nho-170-cat-chan-linh-kien-dien-tu) |
| 830-point breadboard | 35000 ₫ | [breadboard](https://hshop.vn/test-board-cammb-102) |

Pick one meter. Jumpers, LEDs, buttons, and a data USB cable are searches, because this lesson does not invent extra Hshop product slugs. [Shopee, dây cắm breadboard](https://shopee.vn/search?keyword=d%C3%A2y%20c%E1%BA%AFm%20breadboard) and [Lazada, dây jumper đực đực](https://www.lazada.vn/catalog/?q=d%C3%A2y%20jumper%20%C4%91%E1%BB%B1c%20%C4%91%E1%BB%B1c) are search pages. Strippers, if they are the gap the cutters cannot fill: [Shopee, kìm tuốt dây](https://shopee.vn/search?keyword=k%C3%ACm%20tu%E1%BB%91t%20d%C3%A2y). [Thế Giới IC](https://www.thegioiic.com/) and [IC Đây Rồi](https://icdayroi.com/) are shop homepages for a counter visit, not a SKU. A scope, a logic analyzer, and a current-limited supply stay off this invoice.
