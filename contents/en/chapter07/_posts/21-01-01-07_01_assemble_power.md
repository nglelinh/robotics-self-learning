---
layout: post
title: "Assemble chassis, motors, and power"
chapter: "07"
order: 1
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter07
lesson_type: required
draft: false
---

You bolt the motors, trail the caster, strap the battery, and prove the power tree with a meter. No PWM yet.

## Learning objectives

1. Mount both TT motors so the tires clear the plate, set the caster so its contact trails, and strap the battery so the center of gravity sits between the axle and the caster.
2. Wire battery positive through a switch and a 2–3 A fuse, then split that node to driver VM and to an LM2596 whose output you set to 5.0 V before the ESP32 is attached.
3. Tie battery negative, driver GND, buck GND, and MCU GND into one node, and keep motor current on the driver screw terminals.
4. Record unloaded battery voltage and buck output in `lab-notes.md`, with a wiring photo, and refuse USB as a motor supply.

## Prerequisites

Chapter 04 taught you that a sensor and a microcontroller share one ground. Chapter 05 taught the H-bridge: a TB6612 stays asleep while STBY is low, and an L298N's onboard 7805 is not an ESP32 supply. Chapter 06 left two lengths in the notes, track width $$b$$ between the tire contact centers and rolling radius $$r$$ from a one-revolution roll. A typical bench here has $$b = 0.15~\mathrm{m}$$ and $$r = 31.2~\mathrm{mm}$$. Copy them into today's notes. This lesson has no ROS node and no PWM.

## Why this matters for Capstone A and the ROS path

ROS 2 is not in this chapter. Later a `geometry_msgs/Twist` will carry `linear.x` as forward speed and `angular.z` as yaw rate, and some node will split that twist into two wheel commands. The split is useless if the nose lifts, the buck was never set, or the microcontroller browns out when the motors start. Lessons 03 and 04 use a text line as a stand-in for that twist. A Twist message cannot strap a battery.

## Where the mass has to sit

Tires must clear the acrylic, and the caster patch must trail the swivel pin. A rubbing tire is a stall. A reversed fork shimmies. Strap the pack so it cannot slide. From the side, the center of gravity has to sit between the axle and the caster; behind the axle the nose lifts.

Take the axle as $$x = 0$$ and the caster contact as $$x = +90~\mathrm{mm}$$ toward the nose. Suppose the plate and motors are $$220~\mathrm{g}$$ with their own center at $$x = +15~\mathrm{mm}$$, and the pack is $$90~\mathrm{g}$$. The combined center is

$$
x_{cg} = \frac{220 \times 15 + 90 \times x_b}{310}.
$$

Strap the pack behind the axle at $$x_b = -40~\mathrm{mm}$$ and

$$
x_{cg} = \frac{3300 - 3600}{310} \approx -1.0~\mathrm{mm}.
$$

The mass is on the wrong side of the axle. The caster is unloaded and the nose lifts as soon as you accelerate. Strap the same pack between the axle and the caster at $$x_b = +35~\mathrm{mm}$$ and

$$
x_{cg} = \frac{3300 + 3150}{310} \approx 20.8~\mathrm{mm},
$$

which sits between $$0$$ and $$90~\mathrm{mm}$$. The caster then carries about $$(20.8/90)\times 310~\mathrm{g} \approx 72~\mathrm{g}$$. The nose stays down, and the axle still holds most of the weight. Write your own $$x_b$$ beside $$b$$ and $$r$$.

![Track width $$b$$ and the caster you must keep loaded]({{ site.imgurl }}/generated/chassis_measures.png)

## The power tree, measured before the MCU is attached

Motor current and logic current share a battery and a ground, not a regulator and not a breadboard row.

![Battery, fuse, driver VM, and a buck set to 5.0 V before the MCU]({{ site.imgurl }}/generated/power_tree.png)

Battery positive goes to a switch, then a 2–3 A fuse, then splits to driver VM and to the LM2596 input. Battery negative, driver GND, buck GND, and MCU GND are one node. Motor leads run from the driver screws to the motor tabs and never through a breadboard: those contacts are a few hundred milliamps, and a stall is amperes.

Set the buck with the microcontroller unplugged. A fresh 2S pack often reads about $$8.2~\mathrm{V}$$ unloaded (the window is roughly $$7.4$$–$$8.4~\mathrm{V}$$). Turn the potentiometer until the output is $$5.0~\mathrm{V}$$; $$5.02~\mathrm{V}$$ open-circuit is the number you want. Only then do you offer that pin to the ESP32, or you leave the ESP32 on USB for programming and still share ground. Do not feed VM into the 5 V or 3.3 V pin. Do not power motors from USB: a port is about $$500~\mathrm{mA}$$, and two stalled TT motors are on the order of $$2.4~\mathrm{A}$$.

On an L298N the 5 V jumper enables the onboard 7805 from VM. On a 2S pack that is tolerable for the chip's own tiny logic, and it is a bad ESP32 supply once Wi-Fi transmits. Prefer the buck. If VM is above $$12~\mathrm{V}$$, remove the jumper. A quick heat check at the high end of 2S, with $$0.25~\mathrm{A}$$ imagined through that 7805, is

$$
P \approx (8.4 - 5.0) \times 0.25 = 0.85~\mathrm{W}
$$

in a small regulator. At $$12~\mathrm{V}$$ the same current is $$1.75~\mathrm{W}$$. The buck feeds the ESP32 either way.

Lithium stays in a holder or a pack with a BMS. No dangling soldered bare leads. Charge with the matching charger, attended. A TP4056 is 1S only, full near $$4.2~\mathrm{V}$$. One TP4056 on a 2S pack will not make $$8.4~\mathrm{V}$$ and will not balance the cells.

## Lab

### Safety

No PWM in this lab, so the tires may rest on the bench. Keep the battery disconnected until the fuse, switch, and grounds are in. Lithium lives in a holder or a BMS pack. Charge it with the matching charger, attended. One TP4056 must not span a 2S pack. If the buck smells, open the switch.

### BOM

| Item | Role |
|------|------|
| 2WD acrylic chassis, two TT motors, tires, caster | The plant from Chapter 06 |
| 2S pack or 18650 holder with BMS | Motor and logic source |
| Switch, fuse holder, 2–3 A fuse | The series path in the positive lead |
| TB6612 (preferred) or L298N | Driver VM only; outputs unused today |
| LM2596 buck | 5.0 V logic, adjusted before the MCU |
| ESP32 devkit | Attached only after the buck is 5.0 V |
| Multimeter, straps or screws, `lab-notes.md` | The measurement |

### Steps

1. Bolt both motors. Spin each tire by hand so it clears the plate.
2. Mount the caster with the patch trailing. Copy $$b$$ and $$r$$ into today's notes.
3. Strap the battery between the axle and the caster. Estimate $$x_{cg}$$ and write it down.
4. Wire battery positive to the switch, the fuse, then VM and the buck input. Join the four grounds. Motor wires stay on the driver screws.
5. MCU absent, battery on. Measure pack voltage and buck output, set the buck to $$5.0~\mathrm{V}$$, photograph the wiring, and only then attach the ESP32 to that 5 V rail or to USB.

### Expected results

`lab-notes.md` has a date, unloaded pack voltage (a healthy 2S example is $$8.15~\mathrm{V}$$), buck output within a few tens of millivolts of $$5.0~\mathrm{V}$$ before the MCU is attached, your $$b$$ and $$r$$, and a line that motor wires do not enter the breadboard. The photo shows the switch, the fuse, the strap, and the common ground. No wheel has been commanded.

### Faults

| What you see | What it usually means |
|--------------|------------------------|
| Nose lifts when you set the robot down | Pack is behind the axle; move it toward the caster |
| Tire scrapes the acrylic | Motor or wheel spacer is wrong; that scrape is a stall later |
| Buck reads 8 V, or 12 V, on the output | Pot still at the end stop; do not attach the ESP32 |
| ESP32 reboots when you touch VM | Logic is on the 7805, or grounds are not one node |
| You reached for a TP4056 | That board is 1S; use a 2S charger and a BMS |

## Mua ở Việt Nam / Where to buy in Vietnam

Buy the gap, not a second robot. Prices move. Rough 2026 bands: 2WD acrylic chassis 60–150k VND, TT motor 25–45k each, TB6612 25–70k, LM2596 10–25k, 2S pack or 18650 holder 80–180k, switch 8–20k, fuse holder and a 2–3 A fuse 10–25k, ESP32 devkit 70–150k. Verified L298N about 45.000 VND if there is no TB6612. The buck still feeds the ESP32. A 1S holder is not a 2S pack.

- Verified L298N, about $$45.000$$ VND: [hshop.vn/mach-dieu-khien-dong-co-dc-l298](https://hshop.vn/mach-dieu-khien-dong-co-dc-l298)
- [Hshop chassis](https://hshop.vn/search?q=khung+xe+2wd), [buck](https://hshop.vn/search?q=LM2596), [ESP32](https://hshop.vn/search?q=ESP32)
- [Shopee khung 2WD](https://shopee.vn/search?keyword=khung%20xe%202WD%20acrylic), [LM2596](https://shopee.vn/search?keyword=LM2596), [cầu chì](https://shopee.vn/search?keyword=c%E1%BA%A7u%20ch%C3%AC%202A)
- [Lazada ESP32](https://www.lazada.vn/catalog/?q=ESP32), [pin 18650](https://www.lazada.vn/catalog/?q=pin%2018650%202S)
- [Thế Giới IC LM2596](https://www.thegioiic.com/search?q=LM2596), [ESP32](https://www.thegioiic.com/search?q=ESP32)

## Exercises

1. Plate and motors $$220~\mathrm{g}$$ at $$x = +15~\mathrm{mm}$$, pack $$90~\mathrm{g}$$ at $$x_b = -20~\mathrm{mm}$$, caster at $$+90~\mathrm{mm}$$. Find $$x_{cg}$$. Does the nose stay down?
2. Unloaded buck output is $$5.02~\mathrm{V}$$. After the ESP32 joins, the same pin reads $$4.15~\mathrm{V}$$. What do you check before you call the board dead?
3. A classmate wires one TP4056 across a 2S pack "so it can charge from USB." What is wrong with the cell count, and what charger belongs there?
4. VM is $$8.4~\mathrm{V}$$ and the L298N 5 V jumper is fitted. Estimate 7805 heat at $$0.25~\mathrm{A}$$. Why is the buck still the ESP32 supply at this voltage?
5. Two motor leads are pushed into a breadboard, then into the driver. The fuse is on the buck output instead of the battery positive. Rewrite the path battery → switch → fuse → loads, and say what the breadboard cannot carry.

### Answer guidance

1. $$x_{cg} = (3300 - 1800)/310 \approx 4.8~\mathrm{mm}$$, still between axle and caster, so the nose stays down, but the caster is light. If it chatters, move the pack toward $$+35~\mathrm{mm}$$. 2. Check common ground, check that USB and the buck are not both shoved into the 5 V pin, and look for a thin wire or a buck that sags under load. Do not turn the pot up with the MCU attached. 3. A TP4056 is 1S, full near $$4.2~\mathrm{V}$$. A 2S pack is full near $$8.4~\mathrm{V}$$ and needs a 2S charger plus a BMS. 4. $$P \approx (8.4-5)\times 0.25 = 0.85~\mathrm{W}$$. Wi-Fi bursts exceed a quiet 0.25 A and the 7805 sags. The jumper may feed the L298's own logic on 2S; the ESP32 stays on the buck. Remove the jumper above $$12~\mathrm{V}$$. 5. Battery positive, switch, 2–3 A fuse, then VM and the buck input. Motor current stays on screws. A fuse downstream of the buck does not protect a VM short.

## Further reading

- [ST L298 datasheet](https://www.st.com/resource/en/datasheet/l298.pdf)
- [Pololu TB6612FNG carrier](https://www.pololu.com/product/713)
- [geometry_msgs/Twist (Jazzy)](https://docs.ros.org/en/jazzy/p/geometry_msgs/interfaces/msg/Twist.html)
- [Arduino `Serial`](https://www.arduino.cc/reference/en/language/functions/communication/serial/)
