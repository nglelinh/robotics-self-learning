---
layout: post
title: "ESD, polarity, fuses, and brownouts"
chapter: "01"
order: 9
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter01
lesson_type: required
draft: false
---

Three accidents get blamed on "random" firmware. A static zap wounds a pin before you flash anything. A backwards battery destroys a driver as the connector clicks. A motor stall sags the 5 V rail, the ESP32 reboots, and the log looks haunted. This lesson separates the three and ends with a hypothesis you will test when the motors exist.

## Learning objectives

You will handle a board by the edges after touching grounded metal, without turning ESD into theatre and without shrugging it off. You will state how reverse polarity kills an electrolytic and a TB6612 VM pin, and you will check polarity with a meter before the first power-up rather than trusting wire color. You will size a polyfuse or a 2–3 A fuse so it sits above the light running current of two TT motors and below a current that smokes the battery lead. You will explain brownout as the shared 5 V rail collapsing under stall, and you will write the fix: a separate motor battery, common ground only, a 100–470 µF capacitor on VM with the stripe correct, thick motor wires, wheels up, and firmware that forces PWM to 0 if the supply sags or if commands stop for about 300 ms.

## Prerequisites

Lesson 04's electrolytic stripe and lesson 07's split between VM and VCC are assumed. Ohm's law from lesson 01 is the only arithmetic. You will meter a USB rail today. You will not spin a wheel, and you will not connect a motor battery.

## Why it matters

The capstone cart is a 3.3 V ESP32 or Pico, a TB6612, two TT motors, and an HC-SR04. The motors will stall against a curb or a hand. If VM is secretly the same 5 V pin that feeds the board, stall current pulls that rail down, the 3.3 V regulator follows, and the chip resets mid-command. That looks like a logic bug. A second version of the same confusion is the HC-SR04 echo pin, a 5 V output aimed at a GPIO that lesson 07 already forbade. Neither fault is fixed by editing the loop. A separate motor battery, joined to the logic supply by ground and by nothing else, is what makes the next failure interpretable.

![Logic rail beside the motor rail]({{ site.imgurl }}/generated/power_rails_3v3.png)

Two supplies meet only at ground. The 3.3 V rail feeds the microcontroller and the driver logic pin. The motor rail feeds VM. USB drawn into the motor rail is the brownout in advance. The HC-SR04 may take 5 V on its own supply; echo still does not enter a GPIO.

![Order of power, wheels still off the desk]({{ site.imgurl }}/generated/power_order.png)

Logic may come up on USB. The motor chain stays off in this lab. STBY stays inactive until both rails exist and the program is ready.

## ESD, in proportion

Electrostatic discharge is a spark you often cannot see. A carpet walk and then a finger on a bare Pico pad or a MOSFET gate is enough to puncture oxide. The habit is dull and enough: touch grounded metal, such as a plugged-in computer chassis, then pick the board up by the edges; keep bare boards bagged until you are seated; do not hand a loose board across the room. Skip the balloon theatrics. Do not shrug because the last board survived. A soldered module is tougher than a loose transistor, and the same sequence still applies. A wrist strap is optional, not the pass condition.

## Polarity, now and later

Reverse polarity on an aluminum electrolytic heats the can until it vents, and it can take the copper with it. Reverse polarity on VM does the same class of damage inside the driver. The stripe is the negative lead and it goes to ground. Battery positive goes to VM, never to a GPIO, and never "just to see."

A series Schottky in the positive lead, or a keyed XT30, is the right later improvement. The Schottky costs a few tenths of a volt at motor current, so it is a decision, not a reflex, and you do not add it today unless it is already in the kit. Today you meter the battery before it touches the driver: red on the wire you believe is positive, black on the other. A positive reading matches that belief. A minus sign means you stop. Two red wires are not a polarity system.

The HC-SR04 has a polarity that is not a battery. Its VCC is 5 V, trig is an input, and echo is a 5 V output. Swapping sensor VCC and GND is reverse polarity on a small board. Landing echo on a GPIO is the forbid from lesson 07. Check both on the pin card before the sensor is plugged in.

## The numbers that make USB fail as a motor supply

The TT 1:48 listing this course buys quotes about 110–150 mA no-load. Two motors, wheels in the air, draw about

$$
2 \times 130\,\mathrm{mA} \approx 0.26\,\mathrm{A}
$$

Call it $$0.3\,\mathrm{A}$$. A USB port is often budgeted at 500 mA, so light running looks as if it fits:

$$
0.50 - 0.30 = 0.20\,\mathrm{A}
$$

of apparent headroom. Stall is much higher. Do not invent a precise stall ampere you have not measured. Write that stall is several times no-load, already more than a 500 mA port for one TT motor. USB cannot be the motor supply. The TB6612's 1.2 A continuous rating is a ceiling for the chip, not a source. The source is the battery on VM.

## Brownout, and the fix you will actually build

A shared 5 V rail has resistance in the cable and the connector. Stall current through that resistance is a sag:

$$
\Delta V = I_{\mathrm{stall}} \times R_{\mathrm{path}}
$$

You do not need a measured stall current to see the shape. When the 5 V pin droops, the regulator that makes 3.3 V runs out of headroom, the ESP32 resets, and the sketch starts again mid-command. A Pico can brown out the same way. A boot banner where you expected a speed report is this bug.

The hardware fix, in the order you should design it:

The motors get their own battery, inside the 4.5–10 V VM window from lesson 07. Logic stays on USB for now. The supplies share one ground wire and nothing else. Do not force that ground to carry motor current along a thin breadboard rail.

A bulk aluminum electrolytic, 100–470 µF, sits across VM, close to the driver, rated 16 V or 25 V under that 10 V ceiling. The stripe is negative and goes to ground. Reversing it is the vent from the previous section, now on the motor rail. The capacitor covers the sharp edge of a stall so the leads do not have to.

Motor wires are thicker than signal jumpers. Wheels stay up whenever a motor is connected and you are not deliberately driving. A wheel on the desk is a stall you caused.

Firmware, when it exists, forces PWM to 0 if the supply sags, and also if commands stop for about 300 ms. That is long enough to ignore one late packet and short enough that a dead sender does not leave the last speed on the wheels. STBY may drop too. Lesson 07 required STBY high for motion; this lesson requires a way back to off.

## The fuse

A polyfuse or a 2–3 A fuse in the battery lead is cheap insurance. Size it above the light-running current, about $$0.3\,\mathrm{A}$$, so a normal drive does not open it, and below the current that smokes the battery wire. A dead short can be tens of amperes; the fuse is for that, not for a gentle stall. A part under $$0.3\,\mathrm{A}$$ is simply wrong. The fuse does not replace the separate battery and it does not know polarity. Put it in the positive lead, close to the pack, and still do the meter check.

## Lab

USB only. Motors unplugged. Battery disconnected. If a wheel is already on the shaft, leave it in the air.

1. Touch grounded metal, then pick the board up by the edges. Write that you did.
2. USB and nothing else. DC volts, black on ground. Record the 5 V pin, then the 3.3 V pin. Write the numbers, not the word "fine."
3. From the lesson 07 card, or a four-pin sketch if the sensor is absent, circle HC-SR04 Echo and write the forbid: 5 V output, not a GPIO.
4. Write the Chapter 02 hypothesis in this shape, with your readings filled in: "On USB alone the board showed ___ V on 5 V and ___ V on 3.3 V. If it later resets when the TT motors share that 5 V rail, the hypothesis is stall current sagging the rail into brownout. The fix is a separate motor battery, common ground only, 100–470 µF on VM with the stripe to ground, thick motor wires, wheels up, and PWM forced to 0 if the rail sags or if commands stop for about 300 ms. A 2–3 A fuse goes in the battery lead."
5. Do not connect the motors to test the paragraph. The pass is the two voltages plus that paragraph, filed as `ch01-09-brownout`.

If the 5 V reading is far from 5 V with only USB attached, stop and say so. A board that is already sick does not need a motor to explain a reset.

## Worked example

Two TT 1:48 motors at mid-band no-load:

$$
I_{\mathrm{run}} = 2 \times 0.130 = 0.26\,\mathrm{A}
$$

USB is $$0.50\,\mathrm{A}$$. Headroom with the wheels in the air is about $$0.24\,\mathrm{A}$$, which is the whole of the false confidence. Stall $$\gg 0.3\,\mathrm{A}$$, and one stalled motor is already an unfair request of a 500 mA port. The redraw: USB for the ESP32 or Pico and for TB6612 logic at 3.3 V; a separate pack inside 4.5–10 V on VM; one ground point; 220 µF or 470 µF, stripe on ground; a 2 A or 3 A fuse in the positive lead. The notes already say PWM returns to 0 if commands are quiet for about 300 ms.

A 0.5 A fuse "so stall cannot happen" sits on the light-running current and opens during an ordinary drive. People then bypass fuses. Choose 2 A or 3 A, and let the timeout handle stall.

## Exercises

1. Two motors at 150 mA no-load, and a USB port at 500 mA. Compute the light-running sum and the leftover budget. Why does that leftover not mean USB may feed VM once the wheels touch the ground?
2. The 5 V pin reads 4.95 V and the 3.3 V pin reads 3.28 V on USB alone. In Chapter 02 the serial monitor prints the boot banner every time both motors are plugged into that same 5 V pin. Write the one-sentence hypothesis, and name the supply change that tests it.
3. A 470 µF capacitor is on VM with the stripe away from ground. What fails, and which lead must move?
4. Commands stop because the laptop slept, and the last PWM was "both wheels forward." What must the firmware do within about 300 ms, and why is a fuse of 3 A not a substitute for that line of code?
5. Echo on the HC-SR04 is wired to a Pico GP pin "because the sensor works from 5 V and the Pico has a 5 V pin nearby." Which lesson 07 number forbids it, and which of today's checks would have caught the swap of sensor VCC and GND?

<details markdown="1">
<summary>Hints and answers</summary>

1. $$2 \times 0.150 = 0.30\,\mathrm{A}$$, so about $$0.20\,\mathrm{A}$$ remains on a 500 mA port. Stall is much higher than no-load and does not fit in that leftover. USB stays off VM.
2. The hypothesis is that motor current sagged the shared 5 V rail and the 3.3 V rail followed it into brownout. The test is to move the motors to a separate battery, keep one common ground, and see whether the boot banner stops appearing on the same command.
3. A reversed aluminum electrolytic on a battery can vent. The stripe is negative and belongs on ground. Move that lead, and do not power the rail to "confirm" the vent.
4. Firmware sets PWM to 0, and may release STBY, about 300 ms after commands stop. A 3 A fuse will not open at ordinary motor current, so the wheels keep the last command until something else stops them.
5. The GPIO absolute maximum, near the 3.3 V rail and not 5 V, forbids echo on the GP pin. A meter check of sensor VCC against GND, before plugging in, catches a reversed sensor supply. The nearby 5 V pin is a supply, not a logic input.

</details>

## Further reading

- [SparkFun logic levels](https://learn.sparkfun.com/tutorials/logic-levels) — why a 5 V echo and a 3.3 V GPIO are not the same "high," which is the datasheet fence from lesson 07 in plain language.
- [Battery University, BU-409](https://batteryuniversity.com/article/bu-409-charging-lithium-ion) — charging limits for the lithium pack you may later put on VM. Read it before you invent a charger.
- [Pololu TB6612FNG carrier](https://www.pololu.com/product/713) — logic supply and motor supply as separate pins, which is the hardware half of the brownout fix.

## Where to buy in Vietnam

The motor battery, the TT motors, the driver, and the HC-SR04 are on the kit list in Chapter 00, lesson 05, [Bill of materials and how to buy the kit in Vietnam]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %}). Do not buy a second set from this page.

This lab needs a meter if you do not have one. The UNI-T UT33D listing is [on Hshop](https://hshop.vn/dong-ho-van-nang-dien-tu-digital-multimeter-uni-t-ut33d-chinh-hang); read the live price, which this lesson does not freeze. Shop fronts for a 100–470 µF, 16 V or 25 V electrolytic, when you are ready to build the VM capacitor and not before, are [Hshop](https://hshop.vn/), [Thế Giới IC](https://www.thegioiic.com/), and [IC Đầy Rồi](https://icdayroi.com/). This page does not invent a capacitor slug. Confirm the can's voltage and which lead the stripe marks before you solder it.
