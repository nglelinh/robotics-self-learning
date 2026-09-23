---
layout: post
title: "Current limits, stalls, and thermal care"
chapter: "05"
order: 5
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter05
lesson_type: required
draft: false
---

A motor datasheet has two currents that matter on a small robot, and they are not close to each other. No-load current is what you measure with the wheels in the air. Stall current is what the copper will draw when the shaft stops and the back-EMF collapses. This lesson turns that stall number into watts, into a driver heatsink, into a fuse in the battery lead, and into the brownout that makes a robot run away.

## Learning objectives

1. Distinguish no-load current from stall current, and use stall current to size the driver and the fuse.
2. From a rated voltage and a stall current, estimate winding resistance and the watts dissipated in a stalled motor.
3. Estimate heat in an L298N from its voltage drop, and say why a TB6612 stays cooler at the same current.
4. Place a fuse in the battery positive lead, and treat a supply sag that resets the microcontroller as a control bug.

## Prerequisites

Ohm's law and $$P = I^2 R$$ are the whole mathematical toolkit. Lesson 05-01's back-EMF story is the reason stall current is large. Lesson 05-02's driver identification tells you whether your heat is landing in a Darlington with a bolted heatsink or in a MOSFET bridge. You need a bench supply with a current knob, or a series ammeter, if you will measure a real motor. The arithmetic path is available if you cannot stall safely.

## Why this matters for Capstone A and the ROS path

Chapter 07 puts a battery and a fuse on the chassis because a USB port cannot feed two stalled TT motors. A weak 18650 pair also droops when both wheels start together. If the microcontroller resets, the GPIO pins go back through boot, and a half-initialized H-bridge can drive a wheel before your code reaches the line that sets PWM to zero. Brownout is a control bug, not only a power bug. ROS 2 will later stream `cmd_vel` as if the base were awake. Firmware still has to fail safe when the supply sags or the sensor task stops: motors off, and stay off, until a fresh setup has run. The numbers in this lesson are how you choose a fuse that survives normal driving and still opens when a wire shorts.

## Two currents on one curve

The figure for this lesson sketches current against speed. At no load the shaft spins fast, back-EMF cancels most of the supply, and current is small: often a few hundred milliamps or less for a yellow TT motor, sometimes only tens of milliamps for a bare can. At stall, speed is zero, back-EMF is zero, and

$$
I_{stall} \approx \frac{V}{R}
$$

The datasheet stall current, at the rated voltage, is the number you show the driver and the fuse. Running current on a smooth floor sits between the two, closer to no-load until you climb, push, or hit a carpet edge. A gearbox binding against a chair leg is electrically a stall even though your PWM still says "forward."

## Watts in a thumb-sized can

Those watts leave as heat in the winding. A stalled motor has almost no mechanical output, so nearly all of $$I \times V$$ heats the copper and the brushes. A second or two of measurement is a data point. Holding the shaft "to feel the torque" for half a minute cooks the enamel. Two motors stalled together draw about twice one motor's stall current, before wiring losses. A USB port limited near 0.5 A cannot supply that. The port folds, the microcontroller resets, and you learn the brownout with the wheels still on the desk if you are lucky.

## Heat in the driver and sag in the pack

An L298N drops about 2 V at 1 A. The chip, not the motor, dissipates about

$$
P \approx 2~\mathrm{V} \times 1~\mathrm{A} = 2~\mathrm{W}
$$

in that channel. Two channels working hard can double it. The bolted heatsink is required equipment, and the module still needs air. A TB6612 drops far less at the same current, so the board stays cooler, and it still has a thermal limit and a current limit. Cooler is not infinite. If the TB6612 package becomes painful, the motor is stalled or the continuous rating (about 1.2 A per channel) has been ignored.

A tired 18650 pair has internal resistance. When both motors start, VM sags. The buck that feeds the microcontroller sags with it if they share the pack. The ESP32 brownout detector resets the chip. During reset the motor pins are not yet your safe values. Firmware that sets PWM to 0 as the first act in `setup`, and that refuses to re-enable the bridge until a known delay and a known input state, turns a brownout into a stop. Firmware that leaves enable floating turns a brownout into a short drive across the room.

## The fuse is a conversation with the short

Put the fuse in the battery positive lead, close to the pack, so a short anywhere downstream has to pass through it. A 2–3 A fuse on a small 2S pack is a starting conversation, not a law. It has to sit above the normal running current of both motors plus logic, and it has to open on a dead short. If each TT motor runs near 0.3 A and logic is near 0.2 A, a 2 A fuse has margin for driving and will still discuss a hard stall or a pinched wire. A polyfuse is acceptable: it warms, opens, and recovers after it cools. Give it that cooling time. Do not wrap it in tape inside a hot enclosure and then expect the hold current printed on the bag.

## Worked example

A seller rates a motor at 6 V with a stall current of 1.2 A. The winding resistance is about

$$
R \approx \frac{6}{1.2} = 5~\Omega
$$

At stall on that rated voltage the copper dissipates

$$
P = I^2 R = (1.2)^2 \times 5 = 1.44 \times 5 = 7.2~\mathrm{W}
$$

You can check the same result as $$P = I \times V = 1.2 \times 6 = 7.2~\mathrm{W}$$. Seven watts in a motor the size of your thumb is why the stall test lasts about one second and then you release. Two such motors stalled together are about 2.4 A before wiring losses. A USB port at 0.5 A will brown out or reset the board. That is why Chapter 07 uses a battery and a fuse.

If your meter later shows 0.15 A no-load at a modest PWM, keep both numbers. The gap between 0.15 A and 1.2 A is the headroom the fuse and the driver must survive when the wheel stops against a wall.

## Figures

![Stall current versus speed: small current while spinning, large current when the shaft is stopped]({{ site.imgurl }}/generated/stall_current.png)

Read the left side of the curve as the datasheet stall number and the right side as the no-load current you are allowed to measure for more than a second.

![Multimeter in series or on the supply's current display, used for one motor with the wheel in the air]({{ site.imgurl }}/wikimedia/Digital_Multimeter_Aka.jpg)

If you insert the meter, use the high-current jack, start at PWM 0, and do not stall the motor through a meter fuse you cannot afford to replace. A bench supply's own current readout is the calmer instrument.

## Lab

### Safety

Wheels up, off the chassis, one motor only. A one-second stall is allowed only when the supply current limit is set near 2 A so a wiring mistake cannot become a fire. If you do not have a limit you trust, do not stall: use the seller's stall current and compute the watts. Do not hold a spinning pinion. Do not power the motor from USB. Common ground if a microcontroller is producing the PWM.

### BOM

| Item | Role |
|------|------|
| One brushed motor | The device under test |
| Bench supply with a current limit, or a battery plus a series ammeter | The source and the reading |
| H-bridge or direct supply leads | Apply a known voltage |
| Multimeter | Volts, and amps if that is your method |
| Notebook | No-load amps, and stall amps or computed watts |

### Steps

1. Set the supply current limit near 2 A if you have one. Set voltage to the motor's rated voltage or to a modest value you record.
2. Run the motor unloaded at a modest PWM (or straight from the supply). Record voltage and current after one second. That is no-load at that voltage.
3. Optional: stall the shaft for about one second only, read current, release. If the limit folds immediately, write "supply limited" and stop. Do not repeat.
4. If you skipped the stall, copy the seller's stall current, compute $$R \approx V/I_{stall}$$ and $$P = I^2 R$$, and label them as datasheet estimates.
5. Write one sentence on the fuse you would put in the battery positive lead for two of these motors, and why it is above running current.

### Expected results

Two numbers in `lab-notes.md`: a measured no-load current, and either a measured one-second stall current or a computed stall power from the seller's figure. A fuse sentence with a current (2 A or 3 A is a reasonable start for a small 2S TT robot) and the running-current estimate that sits under it.

### Faults

| What you see | What to check |
|--------------|----------------|
| Current reads almost 0 and the shaft spins | The meter is in parallel with the motor, or it is on the voltage jack while you think you are measuring amps. |
| Supply voltage collapses and the MCU resets | USB or a tiny pack is feeding a stall. Move to a battery and a limit, wheels up. |
| L298N heatsink is too hot to touch after a short run | Drop times current is a couple of watts. Shorter stall, more air, or a TB6612. |
| Polyfuse opens and stays open for minutes | It is doing its job. Let it cool. Do not raise the trip point until the short is gone. |
| Robot lurches after a reset | `setup` is not forcing PWM to 0 and a known direction before anything else. |

## Mua ở Việt Nam / Where to buy in Vietnam

The gap to fill is a fuse and, if you still lack them, a driver and a TT motor. A blade fuse, a glass fuse, or a polyfuse near 2–3 A, plus a holder you can actually solder or plug, is enough. Prices move. Rough bands: a small fuse and holder about 5.000–25.000 VND, a TT motor about 25.000–45.000 VND, an L298N module about 35.000–70.000 VND.

- Verified L298N page, about 45.000 VND: [hshop.vn/mach-dieu-khien-dong-co-dc-l298](https://hshop.vn/mach-dieu-khien-dong-co-dc-l298)
- HShop: [cầu chì](https://hshop.vn/search?q=cau%20chi), [motor TT](https://hshop.vn/search?q=motor%20TT), [TB6612](https://hshop.vn/search?q=TB6612)
- Shopee: [cầu chì](https://shopee.vn/search?keyword=cau%20chi), [polyfuse](https://shopee.vn/search?keyword=polyfuse), [motor TT](https://shopee.vn/search?keyword=motor%20TT)
- Lazada: [cầu chì](https://www.lazada.vn/catalog/?q=cau%20chi), [motor TT](https://www.lazada.vn/catalog/?q=motor%20TT)
- Thế Giới IC: [cầu chì](https://www.thegioiic.com/search?q=cau%20chi), [L298N](https://www.thegioiic.com/search?q=L298N)

## Exercises

1. A 6 V motor stalls at 1.2 A. What are $$R$$ and the stall watts?
2. Two of those motors stall together. What current do you plan for, and why is a 0.5 A USB port the wrong source?
3. An L298N drops 2 V while carrying 0.8 A in one channel. How many watts heat that channel?
4. Both wheels run at 0.35 A and the logic draws 0.15 A. Is a 2 A fuse in the battery positive lead above that running total?
5. The ESP32 resets when the motors start, then the robot creeps. What do you change in hardware and in the first lines of `setup`?

### Answer guidance

$$R \approx 5~\Omega$$ and $$P = 7.2~\mathrm{W}$$. Two motors are about 2.4 A at stall, well above a 0.5 A USB port, so Chapter 07 uses a battery and a fuse. An L298N channel at 2 V and 0.8 A heats about 1.6 W. Running total is $$0.35 + 0.35 + 0.15 = 0.85~\mathrm{A}$$, so a 2 A fuse sits above normal running. Hardware wants a stiffer pack and a fuse; `setup` must drive PWM to 0 and a safe direction before the bridge can move.

## Further reading

- SparkFun, motors and the stall-current number: [https://learn.sparkfun.com/tutorials/motors-and-selecting-the-right-one/all](https://learn.sparkfun.com/tutorials/motors-and-selecting-the-right-one/all)
- ST L298 datasheet, for the drop that becomes heat: [https://www.st.com/resource/en/datasheet/l298.pdf](https://www.st.com/resource/en/datasheet/l298.pdf)
- Pololu TB6612FNG carrier, for a cooler bridge at TT currents: [https://www.pololu.com/product/713](https://www.pololu.com/product/713)
