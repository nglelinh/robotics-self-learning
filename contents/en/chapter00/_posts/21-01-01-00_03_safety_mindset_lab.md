---
layout: post
title: "A safety practice for the robot lab"
chapter: "00"
order: 3
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter00
lesson_type: required
draft: false
---

Give this lesson 80 minutes. You can pass it with paper before any parcel arrives. If an iron or a lithium cell is already on the desk, the rules apply now.

## Learning objectives

You will **name** the three hazards that actually show up on this bench: stored energy, spinning wheels, and firmware that forgets to turn PWM off. You will **write** a one-page power-up card whose electrical order is common ground, then logic from USB, then signals, then motor VM last, with the wheels already up. You will **apply** the lithium rule: charge an 18650 one cell at a time to 4.2 V, and never clip a TP4056 across a 2S holder that is an 8.4 V pack when full. You will **reject** a plan that feeds motor voltage, or a 5 V echo, into a 3.3 V pin, knowing that the ESP32 absolute maximum on a GPIO is not 5 V. You will **run** a USB-only bring-up checklist with no motors connected, and you will **match** a symptom to a fix in the fault table rather than to a guess.

## Prerequisites

Lessons 00-01 and 00-02: you can say the 300 ms stop, and the journal has a Track A or Track B sentence. You do not need parts. A GPIO pin is a logic pin, not a power supply, and a wheel on the table becomes a winch the moment PWM is not zero.

## Why it matters

The Chapter 07 demo moves when you ask and goes quiet when commands stop. It is not trustworthy if the first power-up can walk off the desk or put a motor pack into a 3.3 V pin. The timeout runs only after the chip is alive. ROS 2 topics will not debug a pad you already destroyed.

## Three hazards, and the order that keeps them boring

**Stored energy** dumps current without asking: a USB port, AA cells, a pair of 18650s, a capacitor on a driver. The damage is heat in a trace, a pin, or a cell charged the wrong way. **Spinning wheels** pull a cable or walk off the desk the first time PWM comes up wrong. **Firmware that forgets to turn PWM off** is the teleop program that crashes after "forward," the serial window you closed, the laptop that sleeps. The 300 ms rule turns stale software into a stop. It does not protect the second before your program starts, and it does not protect a GPIO from overvoltage.

The ritual fits on one page. Do it every time, including the test you want to call quick. Common ground comes first: microcontroller ground, driver ground, and battery negative are one node, because motor current returns there. A signal connected before that ground can return through a GPIO and destroy it. Logic power is next, USB into the microcontroller, which makes 3.3 V for its pins. The driver's logic supply comes from that quiet rail, not from the motor battery. Signals come after: PWM, direction, and standby, already meaning stop if firmware is running. Motor VM is last, through a switch if you have one. The wheels are already up. Lifting them after the twitch is how a caster leaves the desk.

![Power comes up as common ground, logic, signals, motor supply last, wheels off the desk]({{ site.imgurl }}/generated/power_order.png)

Copy the boxes in that order. "Last" means the switch closes last. The wheels are already up.

![Logic at 3.3 V, USB 5 V, ground, and a separate motor rail]({{ site.imgurl }}/generated/power_rails_3v3.png)

Use the colours as a ban list. USB 5 V feeds the board, not two stalled TT motors. GPIO is a 3.3 V world. Ground is the node you share on purpose. The motor rail is a separate battery and never lands on a GPIO or on the 3.3 V pin.

## Lithium, in the specific way people get hurt

A single 18650 lithium-ion cell is about 3.6–3.7 V nominal and **4.2 V full**. You charge **one cell at a time** to 4.2 V, on a charger whose label says Li-ion or Li-ion 18650. Two cells in series, which is what a 2S holder does, are about 7.4 V nominal and **8.4 V full**. That series pair is a motor pack. It is not a charger input.

A TP4056 tries to bring one cell to 4.2 V. Clipping it across a 2S holder puts that charger across an 8.4 V pack. Do not. Take one cell out, charge it alone, then put it back.

A cell at about 2.1 V is far below the usual cutoff near 2.5–3.0 V. Charging it at a normal rate can plate metal inside and set up an internal short. Do not "wake" it with a TP4056. Recycle it. A swollen cell is already damaged: do not charge it, puncture it, or keep it "in case." A bare 18650 in a pocket with keys can weld a short. Cells live in a holder or a case. The first motor tests may use a AA holder so you learn VM versus logic before you own lithium. No cells yet is a safe state. An unmatched charger is not.

## Pins, iron, and eyes

The ESP32 absolute maximum on a GPIO is **not** 5 V. The pad sits a few tenths of a volt above the 3.3 V rail, not at 5 V and not at motor voltage. A Pico pin is the same kind of 3.3 V input. An HC-SR04 echo is about 5 V when high. The pack is often 7–8 V. A level shifter belongs on the echo. The pack belongs on VM only.

Wear eye protection when you cut leads and when you solder. Leads fly. Rosin fumes need moving air, not a closed room and a face over the joint. The iron lives in a stand, not on the cable. You are not soldering today. You are writing that rule where your hands will see it.

The software half of the ritual is the timeout you already wrote:

$$
t_{\mathrm{silence}} > 300\,\mathrm{ms} \implies \text{PWM duty} = 0.
$$

You cannot flash that loop today. Refuse to call a setup ready if the only stop is pulling the USB plug after the robot has left the mat. A silent teleop link must be a stop, not a hold-last-speed cruise.

## Faults you should recognise before you have them

| What you see or were about to do | What it usually is | What you do |
| --- | --- | --- |
| Serial port vanishes when the motors are tied to the board's 5 V pin | The USB port cannot feed two stalled motors; the 3.3 V rail collapses | Motors on a separate VM, common ground, logic from USB only |
| A GPIO is dead after the ultrasonic echo was connected | 5 V into a pin whose absolute maximum is not 5 V | Stop; that pin may be ruined; shifter on echo before any retry |
| A TP4056 is clipped across a 2S holder | A 4.2 V charger on an 8.4 V pack | Remove it; charge one cell at a time, off the robot |
| A cell measures about 2.1 V, or the jacket is swollen | Over-discharged or damaged lithium | Do not charge; do not pocket it; recycle |
| Wheels on the desk, new firmware, you are "just checking" | Unexpected motion, and PWM may be nonzero before your loop runs | Wheels up first; VM last; timeout still required once code runs |
| The iron is lying on its cable, or your eyes are unprotected while you cut leads | A burn, a melted cord, or a lead in an eye | Stand, glasses, ventilation; unplug if the setup is already wrong |

## Lab: the card, then a USB-only bring-up

Perform this with motors **out of the circuit**. If you have no board yet, write the card anyway and put `board not arrived` where a port name would go.

Cut or tear a page. Title it `POWER UP`. Number four lines: (1) common GND, (2) logic from USB, (3) signals, PWM and direction, already meaning stop, (4) motor VM last. Under them write `WHEELS UP BEFORE VM`, `SILENCE > 300 ms → PWM 0`, `NEVER: battery or 5 V echo on a 3.3 V GPIO`, and `18650: one cell, 4.2 V, never a TP4056 across a 2S holder`. Tape the page where your hands will work. If you have no tape, put it under the keyboard you use for notes.

Then run the USB-only checklist, in this order.

Look at the desk and confirm there is no motor, no motor battery, and no VM wire. Disconnect a battery before USB goes in. Wheels, if you own them, are not on a powered driver and are not part of this test. Plug in only the microcontroller, on a cable you believe can carry data. Look for a serial port or, on a Pico in BOOTSEL, a drive. Paste the port name, or write `none — board not arrived` and the plan "when it arrives, USB only, no VM, record the port, then unplug." Unplug. Do not attach motors to celebrate.

If you already own lithium cells, photograph the charger label and type the chemistry words you can read. A missing label means `will not charge`. No lithium means `cells not purchased yet`. If you own an iron, confirm the stand before you ever turn it on, and note whether eye protection is on the bench.

**What you should see.** The card is visible without opening the lesson. The journal has a photo or sketch of the card, a serial field that is a real port name or an explicit plan, and a charger decision: "matches," "will not charge," or "cells not purchased yet." No motor was connected.

**When it goes wrong.** If VM is listed first, rewrite the card. Wheels stay up for the first test of new firmware, including on the desk. A video that powers motors from the DevKit 5 V pin is `forbidden`. A charger clipped on because the connector fit comes off. One cell at a time.

## Worked example

A classmate wants the wheels down "just to see the new sketch." PWM has not been shown to start at 0, and the 300 ms timer cannot run until setup finishes. Keep the wheels up, VM open, USB logic only, then a first run in the air. Wheels down can drag the board off the desk before that line executes.

The same afternoon an 18650 reads 2.1 V and someone offers a TP4056 "recovery." The cell is below a sane cutoff. The note says it will not be charged, pocketed, or clipped across the 2S holder. A healthy cell, if they have one, is charged alone to 4.2 V and only then placed in the holder.

The echo wire in the same pile was about to land on an ESP32 GPIO. Absolute maximum on that pad is not 5 V, so the wire waits for a level shifter. Motor voltage is the same ban, only larger.

## Exercises

These are situations. Write the action, not a definition.

1. A classmate has the chassis on the desk, wheels down, and wants to upload firmware "just for a second." What has to be true before VM is allowed to close, and why is the 300 ms rule not enough on that first upload?
2. A cell on the bench reads 2.1 V. Someone offers a TP4056. What do you do with the cell, and what do you refuse to do with the 2S holder?
3. The echo wire of an HC-SR04 is about to go straight to an ESP32 GPIO. What voltage is that wire when the sensor answers, and why is "the ESP32 is tough" not a rating?
4. You find a TP4056 already clipped across a holder that contains two cells in series. The holder is the one that will later feed VM. What do you disconnect, and how will those cells be charged if they are healthy?
5. Teleop was working, then the laptop slept. The firmware has no silence timer. What do the wheels do, and what single assignment belongs in the control loop?

<details>
<summary>Suggested answers</summary>

1. Wheels up, ground then logic then signals already done, VM still open until you can watch the wheels in the air. The timeout runs only after firmware is executing. Reset can drive a pin first, and a wheel on the desk can pull the board off.
2. Do not charge the cell, pocket it, or clip a TP4056 to it or to the 2S holder. Recycle it.
3. The echo is about 5 V when high. The ESP32 absolute maximum on a GPIO is not 5 V. The wire needs a level shifter. The pin may already be damaged.
4. Disconnect the TP4056 now. Charge each healthy cell alone to 4.2 V, off the robot. The holder is only a pack for VM after that.
5. The wheels keep the last command. The loop must set PWM duty to 0 when silence exceeds about 300 ms.

</details>

## Further reading

- [SparkFun logic levels](https://learn.sparkfun.com/tutorials/logic-levels) — why 5 V and 3.3 V are not interchangeable, which is the echo-pin problem in miniature.
- [Battery University, BU-409, charging lithium-ion](https://batteryuniversity.com/article/bu-409-charging-lithium-ion) — the 4.2 V full-charge idea and why a lithium-ion cell is not a generic "rechargeable."

## Where to buy in Vietnam / Mua ở Việt Nam

The robot cart is [lesson 00-05]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %}). Prices here are Hshop snapshots from **23 September 2026**. Buy one meter: the [UNI-T UT33D+](https://hshop.vn/dong-ho-van-nang-dien-tu-digital-multimeter-uni-t-ut33d-chinh-hang) at 285000 ₫ or the [Wadfow WDM1501](https://hshop.vn/dong-ho-van-nang-ky-thuat-so-vom-wadfow-wdm1501-digital-multimeter-true-rms) at 185000 ₫. The iron and the stand are a pair: [Wadfow 60 W](https://hshop.vn/mo-han-60w-wadfow-wel3616-soldering-iron) at 75000 ₫ and a [round stand](https://hshop.vn/de-gac-mo-han-tron-b-2-co-khay-roi) at 40000 ₫. An iron without the stand fails the rule you just wrote. Solder, cutters, and the breadboard are in lesson 00-04.

Eye protection and a one-cell charger are searches, not invented product slugs. [Shopee, kính bảo hộ](https://shopee.vn/search?keyword=k%C3%ADnh%20b%E1%BA%A3o%20h%E1%BB%99), [Lazada, kính bảo hộ](https://www.lazada.vn/catalog/?q=k%C3%ADnh%20b%E1%BA%A3o%20h%E1%BB%99), [Shopee, sạc pin 18650](https://shopee.vn/search?keyword=s%E1%BA%A1c%20pin%2018650), [Lazada, sạc pin 18650](https://www.lazada.vn/catalog/?q=s%E1%BA%A1c%20pin%2018650). Those URLs are search pages. Buy a charger only if the label says one Li-ion cell to 4.2 V. [Thế Giới IC](https://www.thegioiic.com/) and [IC Đây Rồi](https://icdayroi.com/) are shop homepages, not product links. Do not buy a LiDAR from these searches.
