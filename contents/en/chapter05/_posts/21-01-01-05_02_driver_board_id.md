---
layout: post
title: "Motor driver board ID: L298N, TB6612, DRV8833"
chapter: "05"
order: 2
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter05
lesson_type: required
draft: false
---

The silkscreen on a red module is part of the circuit. Before you trust a tutorial pinout, you identify which chip is actually soldered on your board, because the L298N, the TB6612, and the DRV8833 disagree about voltage drop, logic supply, standby, and how much current a TT gearmotor may ask for at stall. This lesson teaches you to name the board in your hand and to measure its rails before a microcontroller pin ever touches it.

## Learning objectives

1. Identify an L298N module, a TB6612 module, and a DRV8833 breakout from the chip body, the heatsink, and the pin names.
2. State what the L298N 5 V jumper does, when it must come off, and why that regulator is a poor supply for an ESP32 radio.
3. Explain why STBY on a TB6612 has to be driven high, and why a DRV8833 is a small-motor part on a 1S–2S pack under 10 V.
4. Measure VM and the logic rail with a meter before connecting a GPIO, and record every screw terminal in your lab notes.

## Prerequisites

You can use the DC volts range of a multimeter and you know which probe is black. Lesson 05-01's H-bridge vocabulary (forward path, reverse path, shoot-through, PWM on enable) is the map you are now matching to a physical board. You also know that motor current does not come from USB.

## Why this matters for Capstone A and the ROS path

Capstone A rolls on two yellow TT gearmotors from a 2S pack. The driver under those motors sets how much of the battery reaches the brushes and whether a forgotten pin leaves both wheels asleep. Chapter 07's signed left and right PWM assumes a live bridge with a known truth table. ROS 2 does not repair a regulator that sags when Wi-Fi transmits: the microcontroller resets, the last PWM value or a floating input remains, and the chassis can creep. Choosing the TB6612 as the default, and knowing how to live safely with an L298N if that is what the shop sold you, is part of making `cmd_vel` mean motion you intended.

## What you see on the desk

An L298N module is the chunky red or green board with a bolted metal heatsink on a large DIP package and a small jumper near a 5 V regulator. Screw terminals take VM, GND, and the two motors. The logic header is usually IN1, IN2, ENA, IN3, IN4, ENB, plus a 5 V pin.

A TB6612 module is smaller. The Toshiba TB6612FNG is a MOSFET bridge. The pins you should be able to point to are VM, VCC, GND, AIN1, AIN2, PWMA, BIN1, BIN2, PWMB, and STBY. Two motors share the chip. There is often no large bolted heatsink, because the drop is much smaller than a Darlington's.

A DRV8833 breakout is tiny. The TI DRV8833 is a dual bridge whose motor supply is about 2.7–10.6 V. Many hobby boards run it in IN/IN mode, where the two inputs of a channel encode direction and PWM. You rarely see a big heatsink. The part is comfortable with small motors and with a 1S or 2S pack that stays under 10 V. A pair of TT motors at stall asks for more current than this small bridge is happy to hold.

## The L298N and its 5 V jumper

The L298N output stage is bipolar Darlington. While current flows, the bridge drops roughly 2 V, and that product of drop and current becomes heat in the chip. The bolted heatsink is doing real work. Logic on this module is a 5 V world: the chip's logic supply pin wants about 5 V.

The onboard 7805, when the jumper is fitted, steals its input from the motor supply and produces that 5 V. If the motor supply is above 12 V, the regulator dissipates too much and cooks. Pull the jumper off in that case and feed 5 V from a separate regulator. Even at 12 V and below, do not power an ESP32 Wi-Fi radio from that 7805. The radio's current bursts sag the little regulator, the ESP32 browns out, and the robot reboots mid-command. Use a separate buck for logic, and keep a common ground with VM.

A 3.3 V GPIO is usually enough to be seen as a high on the L298 inputs, whose input-high threshold is about 2.3 V, provided the logic supply pin itself is a solid 5 V and the grounds are common. The jumper and the 5 V pin are about powering the chip's logic, not about "borrowing 5 V for the whole robot."

## TB6612, the Capstone default

The TB6612FNG uses MOSFETs, so the voltage left for the motor is much closer to VM than it was on the L298N. VCC, the logic supply, accepts about 2.7–5.5 V, which means a 3.3 V ESP32 can power the logic pin directly. VM may run up to about 15 V; stay inside the range your particular board lists, and a 2S pack near 7.4–8.4 V is a comfortable match. Continuous current is about 1.2 A per channel, which is a fair budget for one TT motor if you respect stall time.

STBY must be driven high or the bridges stay asleep. A floating STBY pin is the classic "my code is perfect and the wheels are dead" bug. Tie it to VCC if you want the chip awake whenever logic power is present, or drive it from a GPIO you set high in `setup` and low when you want a hardware coast. PWMA and PWMB take the speed chops. AIN1 and AIN2, and the B pair, take direction. Read the Pololu or Toshiba table, then confirm coast versus brake on the bench as you did in lesson 05-01.

## DRV8833 and the boards that are too small

The DRV8833 is a good dual bridge for a small mechanism, a tiny robot on 1S, or a 2S experiment whose motors stall well below what a TT pair demands. Many breakouts expose IN1/IN2 and IN3/IN4 and expect you to PWM one input while holding the other. There is often a sleep pin that must be held awake, in the same spirit as STBY. If your only motors are the Capstone TT pair, pick the TB6612.

MX1508 and L9110 modules show up in the same search results. They are fine for a very small motor on a desk demo. They are the wrong bridge for a 2S TT robot: the current and the thermal mass are both too small, and a stall becomes a melted package. If that is the board in the drawer, use it to learn pin names on a tiny motor, then buy a TB6612 before the chassis goes together.

## Worked example

Suppose the motor supply is 12 V and the L298N jumper is still on, so the 7805 drops $$12 - 5 = 7~\mathrm{V}$$. Take $$0.20~\mathrm{A}$$ as a round figure for a busy ESP32 radio (a real Wi-Fi burst can be higher).

$$
P_{7805} \approx (12 - 5) \times 0.20 = 1.4~\mathrm{W}
$$

That heat sits in a small regulator with almost no copper. The 5 V rail sags, the microcontroller resets, and any PWM that happens to be on becomes a surprise. Above 12 V the product is worse, which is why the jumper comes off. The same 1 A through an L298N channel that drops about 2 V puts about $$2~\mathrm{W}$$ in the Darlington chip, which is why the bolted heatsink is not decoration. A TB6612 on 2S avoids both of these heaters for the Capstone motors.

## Figures

![L298N dual H-bridge module with a bolted heatsink]({{ site.imgurl }}/wikimedia/Dosmotorsl298n.jpg)

Look for the large package under the metal, the screw terminals for the motors and VM, and the jumper that feeds the onboard regulator. If your board matches this shape, treat it as an L298N until the chip marking says otherwise.

![A digital multimeter used to measure VM and the logic rail before any GPIO is connected]({{ site.imgurl }}/wikimedia/Digital_Multimeter_Aka.jpg)

Black on the driver ground, red on VM, then red on the logic 5 V or 3.3 V pin. Write the numbers down. A pin that is already at battery voltage is not a GPIO destination.

## Lab

### Safety

Motor supply off while you probe with the continuity function. When you measure VM, use the volts range, start with one hand, and do not let the probe slip from VM onto a logic pin. Do not connect an ESP32 pin until both rails are known. Wheels stay off the ground if a motor is attached.

### BOM

| Item | Role |
|------|------|
| The driver module you actually own | The object of the identification |
| Multimeter | DC volts, then continuity if you wish |
| Your phone | A labeled photo |
| Optional: 2S pack or bench supply | VM source, current-limited |
| Notebook | Pin list and the two measured voltages |

### Steps

1. Photograph the board top and bottom. Circle the chip marking if you can see it.
2. In `lab-notes.md`, label every screw terminal and every logic pin with the name on the silk (VM, VCC, GND, ENA, STBY, and so on).
3. If a 5 V jumper exists, write what it connects. State whether it stays on for your pack voltage.
4. Apply VM from the battery or bench supply with the microcontroller still disconnected. Measure VM and measure the logic rail. Record both.
5. Point at STBY or at the L298 jumper and say aloud what that part does. If you have a DRV8833, point at the sleep or fault pin and say what "awake" means on that board.
6. Only then wire VCC or 5 V logic, common ground, and the input pins.

### Expected results

You can name the chip, you have a pin-labeled photo, and you have two meter readings written down (VM and logic). You can say what STBY or the 5 V jumper does without reading the silkscreen again. A DRV8833 owner can state the 2.7–10.6 V motor range and whether their pack fits inside it.

### Faults

| What you see | What to check |
|--------------|----------------|
| Logic 5 V reads 0 with the jumper on | VM is missing, the jumper is seated on the wrong pins, or the 7805 has already failed. |
| ESP32 resets when Wi-Fi starts | The radio is fed from the module 7805. Move logic power to a separate buck. |
| TB6612 outputs stay dead | STBY is low or floating. Drive it high and remeasure. |
| DRV8833 shuts down on a TT motor | Stall current is above what the small bridge can hold. Change the motor or the driver. |
| MX1508 gets too hot to touch | The motor is too large for that board. Remove power. |

## Mua ở Việt Nam / Where to buy in Vietnam

Buy the chip you can identify, not the first red board in the photo. For Capstone TT motors on 2S, search TB6612 first. An L298N is a valid lab board if you accept the drop and the heatsink. A DRV8833 fits smaller motors. Prices move. Rough bands: L298N module about 35.000–70.000 VND, TB6612 module about 40.000–120.000 VND, DRV8833 breakout about 30.000–80.000 VND.

- Verified L298N page, about 45.000 VND: [hshop.vn/mach-dieu-khien-dong-co-dc-l298](https://hshop.vn/mach-dieu-khien-dong-co-dc-l298)
- HShop: [TB6612](https://hshop.vn/search?q=TB6612), [DRV8833](https://hshop.vn/search?q=DRV8833), [L298N](https://hshop.vn/search?q=L298N)
- Shopee: [TB6612](https://shopee.vn/search?keyword=TB6612), [DRV8833](https://shopee.vn/search?keyword=DRV8833)
- Lazada: [TB6612](https://www.lazada.vn/catalog/?q=TB6612), [DRV8833](https://www.lazada.vn/catalog/?q=DRV8833)
- Thế Giới IC: [TB6612](https://www.thegioiic.com/search?q=TB6612), [DRV8833](https://www.thegioiic.com/search?q=DRV8833)

## Exercises

1. Your module has a bolted heatsink and a 5 V jumper. Motor supply is a 3S pack at 12.6 V. What do you do with the jumper, and where does ESP32 power come from?
2. A TB6612 program sets AIN1, AIN2, and PWMA correctly, and the shaft never moves. Which pin is the first one you check?
3. VM on a DRV8833 board measures 11.1 V from a 3S pack. Is that inside about 2.7–10.6 V?
4. At 1 A, an L298N channel drops 2 V. How much power is the chip turning into heat in that channel?
5. A seller photo shows an MX1508 for a two-TT robot on 2S. What board do you buy for the chassis?

### Answer guidance

Pull the L298N jumper off above 12 V and power the ESP32 from a separate buck with a common ground. On a silent TB6612, check STBY and drive it high. An 11.1 V pack is above the DRV8833's about 10.6 V motor range, so that pack does not belong on that chip. One L298N channel at 2 V and 1 A dissipates about 2 W. A two-TT robot on 2S wants a TB6612, not an MX1508 or L9110.

## Further reading

- TI DRV8833 datasheet (VM range and IN/IN interface): [https://www.ti.com/lit/ds/symlink/drv8833.pdf](https://www.ti.com/lit/ds/symlink/drv8833.pdf)
- Pololu TB6612FNG carrier (STBY, VM, and current): [https://www.pololu.com/product/713](https://www.pololu.com/product/713)
- Pololu DRV8833 carrier: [https://www.pololu.com/product/2130](https://www.pololu.com/product/2130)
- ST L298 datasheet: [https://www.st.com/resource/en/datasheet/l298.pdf](https://www.st.com/resource/en/datasheet/l298.pdf)
