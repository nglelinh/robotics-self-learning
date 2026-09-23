---
layout: post
title: "Capacitors, diodes, and LEDs"
chapter: "01"
order: 4
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter01
lesson_type: required
draft: false
---

## Learning objectives

By the end of this lesson you will be able to point at the stripe on an aluminum electrolytic and say that it marks the negative lead, and you will treat a ceramic disc or chip capacitor as non-polar unless the body says otherwise. You will read a ceramic code such as 104 as 100 nF. You will name the cathode of a diode by its band, and you will check an LED with the meter's diode mode instead of trusting the long lead alone. You will also explain why a 100 µF capacitor across a motor driver's VM pin softens short spikes and still does not replace a separate motor supply for two TT motors.

## Prerequisites

You can use $V = IR$ and you can size the series resistor for a red LED on 3.3 V. You know that diode mode belongs on an unpowered part, with the red lead out of the current jack. If the kit has not arrived, the photographs still carry the polarity rules. The lab is a diode test, not a powered experiment.

## Why this matters on the diff-drive robot

The ESP32 or Pico runs at 3.3 V. The TB6612 takes motor power on VM, about 4.5 V to 10 V, and logic on VCC that is happy at 3.3 V. A 100 µF electrolytic across VM is a local reservoir for PWM spikes from the TT motors. It is not the battery. The energy in 100 µF is gone in a fraction of a millisecond at stall current, so the pack still has to exist, and it still must not be wired to a GPIO.

The status lamp is an LED plus a resistor. A flyback diode, later, is a 1N4007-class part with the band toward the positive motor terminal. An electrolytic backwards on a live pack can vent. This lesson is how you tell capacitors, diodes, and LEDs apart before any of those wires are hot.

## Capacitors: stripe, code, and what 100 µF can actually do

An aluminum electrolytic is polarized. The stripe down one side, usually with minus signs in it, marks the negative lead. On a single-supply rail that lead goes to ground and the other lead goes to the rail you are stiffening. The voltage rating on the can must sit above the highest voltage that rail will see. A 2S pack is about 8.4 V full, so 16 V or 25 V is comfortable and 6.3 V is not.

![Electrolytic polarity: the stripe is the negative lead]({{ site.imgurl }}/generated/capacitor_polarity.png)

![An aluminum electrolytic, stripe marking the negative side]({{ site.imgurl }}/wikimedia/Electrolytic_capacitor.jpg)

Ceramic capacitors in this course are usually non-polar. A disc with no stripe, or a small brown SMD rectangle with no printed polarity mark, may go in either way. Do not invent a polarity for it because the electrolytic next to it had one. Some tantalum capacitors are polarized and use a different mark; if you did not buy a tantalum, do not assume every beige rectangle is one.

Through-hole ceramics often use a three-digit code in picofarads. The first two digits are significant figures and the third is a power of ten, the same pattern as an SMD resistor, but the unit is pF. A part marked 104 is

$$
10 \times 10^{4}\ \mathrm{pF} = 100000\ \mathrm{pF} = 100\ \mathrm{nF} = 0.1\ \mu\mathrm{F}
$$

A 103 is 10 nF. The code is not the capacitance in nanofarads. Electrolytics usually print the value in plain text, such as 100 µF 16 V, because 100 µF would be an absurd picofarad code.

Here is the motor-rail number that keeps the capacitor honest. Energy in a capacitor is

$$
E = \frac{1}{2} C V^2
$$

For $C = 100\ \mu\mathrm{F} = 100 \times 10^{-6}\ \mathrm{F}$ at a 7.4 V nominal pack,

$$
E = \frac{1}{2} \times 100 \times 10^{-6} \times (7.4)^2 \approx 0.0027\ \mathrm{J}
$$

A single stalled TT motor near 0.8 A at 7.4 V is about 6 W. The time that 100 µF can supply that power is roughly $0.0027 / 6 \approx 0.5\ \mathrm{ms}$. Half a millisecond of stall energy is useful against a PWM edge and against the inductance of long battery leads. It is not a power source for wheels. Two motors make the reservoir even smaller relative to the load. Put the 100 µF across VM and GND, stripe to GND, and still give the TB6612 a real pack. Do not hang that pack on the Pico or ESP32 3V3 pin and call the capacitor a solution.

## Diodes and LEDs

A silicon diode conducts easily one way and blocks the other. The band on a 1N4007 marks the cathode, the end conventional current leaves when the diode is forward biased. The other end is the anode. A red LED plays the same role in a lamp, with a forward drop near 2 V instead of about 0.7 V.

An LED's longer lead is often the anode, and the flat on the rim is often the cathode. "Often" is the whole problem. Cheap assortments are cut to length, and a previous student may already have trimmed the leads. Trust the meter. Diode mode, on an unpowered part, shows a forward drop in one direction and an open circuit the other way. For a silicon diode that drop is roughly 0.5 V to 0.7 V. For a red LED it is often near 1.6 V to 2.0 V, and the LED may glow faintly because the meter is pushing a small test current through it. If both directions read like a short, the part is dead. If both read open, it is dead or it is not a diode.

![LEDs of several colors; lead length is a hint, not a guarantee]({{ site.imgurl }}/wikimedia/LEDs.jpg)

![Packages that look alike until you read the marks]({{ site.imgurl }}/generated/component_lookalikes.png)

A blank brown SMD rectangle is often a capacitor; a rectangle with a three-digit code is often a resistor. Verify. The status LED is the one in series with about 180 Ω from 3.3 V. A flyback diode beside a bare transistor has its band at the positive end of the motor, so the current that wants to keep flowing when the switch opens does not go through the transistor. The TB6612 already includes that path. You still need to recognize a 1N4007 when it falls out of the kit.

## Worked example: diode-mode readings you should expect

Take an unpowered 1N4007 and a red LED, out of circuit. Diode mode applies a small current and displays the voltage it needed.

One way on the 1N4007 you might see about 0.62 V. Swap the probes and the display should show over-range, often "OL" or a blank of the same kind. The band end was the cathode: the reading appeared when the red probe was on the anode (the end without the band) and the black probe was on the band. Conventional current in diode test leaves the red probe.

One way on the red LED you might see about 1.8 V and a faint glow. The other way is over-range. The lead that was under the red probe during the 1.8 V reading is the anode. If that lead is also the longer one, the manufacturer and the meter agree. If they disagree, believe the meter and mark the anode with a pen before you trim the leads.

The LED wants a series resistor because its voltage barely moves while current runs away. The capacitor's voltage does move, which is why $E = \tfrac{1}{2}CV^2$ is the right question for the 100 µF part. Neither part is a motor you may hang on a GPIO.

## Hands-on lab

This lab stays unpowered on purpose. You will not reverse an electrolytic on a live rail.

1. Collect one electrolytic, one ceramic marked 104 if you have it, one 1N4007 or any banded diode, and one LED. Leave every battery and USB cable unplugged.
2. On the electrolytic, find the stripe. Write down which lead is negative. Read the voltage rating. If it is below 16 V, it is a poor choice for an 8.4 V pack even though this lab will not apply that pack.
3. If the ceramic says 104, write $10 \times 10^4\ \mathrm{pF} = 100\ \mathrm{nF}$ before you look it up.
4. Diode mode, red lead in the voltage/ohms jack, black in COM. Probe the 1N4007 both ways. Record which orientation shows a voltage near 0.5 V to 0.7 V, and confirm that orientation puts black on the band.
5. Probe the LED both ways. Record the forward reading and which lead was under the red probe. Compare with lead length and with the flat, and note any disagreement.

You should see one direction of each diode conduct and the other block. The LED may glow faintly in the conducting direction. The electrolytic is identified by eye in this lab; you do not charge it and you do not measure its capacitance unless your meter has a capacitance range and the part is out of circuit.

| What you see | Likely cause | What to change |
| --- | --- | --- |
| Both directions of the diode read OL | Probes not making contact, or the part is open | Reclean the leads and retry. If it stays open, set it aside. |
| Both directions read near 0 V | The part is shorted, or you are still on continuity across a wire | Check the dial. A healthy diode is not a beep both ways. |
| LED lights in diode mode but the long lead was the cathode | The leads were trimmed, or the batch is odd | Mark the anode from the meter. Do not argue with a faint glow. |
| You are tempted to "see what reverse bias does" on the electrolytic | That is the failure this lab refuses to demonstrate | Stop. Read the note below. Do not power it backwards. |

A reversed aluminum electrolytic on a live rail does not sit there politely. The oxide film breaks down, leakage current heats the electrolyte, pressure rises, and the scored vent on the can opens or the can ruptures. The failed part often becomes a short. On a motor pack that short can dump the cells. We describe it so you can recognize a vented can. We do not build it.

Safety: diode mode only, parts out of circuit, USB unplugged, no VM connected. Do not discharge a large capacitor by shorting it with your fingers or with a probe tip you are holding. The 100 µF parts in this kit are small; the habit still matters when a later board is not.

## Exercises

1. A ceramic is marked 104 and another is marked 223. Give both values in nF.
2. A 100 µF capacitor sits at 7.4 V. Compute the stored energy. How long could that energy run a 6 W stall, at least as a rough $E/P$ estimate?
3. Diode mode shows 0.58 V on a 1N4007 with black on the banded end, and OL when the probes swap. Which end is the cathode, and which probe was on the anode during the 0.58 V reading?
4. An LED assortment has had every lead cut to the same length. Describe the unpowered test that still finds the anode, and say what you would refuse to do in order to "make the test more obvious."
5. A classmate puts the 100 µF electrolytic across the ESP32 3V3 pin and GND, stripe correct, and then connects two TT motors to that same 3V3 pin because "the capacitor will supply the stall." What is wrong with the energy argument, and what should VM be connected to instead?

<details>
<summary>Suggested answers</summary>

1. 104 is $10 \times 10^4\ \mathrm{pF} = 100\ \mathrm{nF}$. 223 is $22 \times 10^3\ \mathrm{pF} = 22\ \mathrm{nF}$.
2. $E = \tfrac{1}{2} \times 100 \times 10^{-6} \times 7.4^2 \approx 0.0027\ \mathrm{J}$. Time is about $0.0027 / 6 \approx 0.45\ \mathrm{ms}$. That is a spike, not a cruise.
3. The banded end is the cathode, because black was on it during the forward reading. The red probe was on the anode.
4. Unpowered diode mode. The anode is the lead under the red probe when you see a forward drop and, often, a faint glow. Do not apply 5 V or a GPIO with no series resistor to make the glow brighter.
5. At stall the capacitor holds well under a millisecond of energy, so the 3V3 regulator is still asked for about an ampere and will brown out or fail. VM on the TB6612 should see the motor pack, in the module's 4.5 V to 10 V range, with ground shared and the GPIO used only as logic.

</details>

## Further reading

SparkFun's capacitor note is the polarity and the code in a shorter page: [Capacitors](https://learn.sparkfun.com/tutorials/capacitors). The diode page covers the band and forward drop: [Diodes](https://learn.sparkfun.com/tutorials/diodes). The LED page is the same one the resistor lesson already earned: [Light-emitting diodes](https://learn.sparkfun.com/tutorials/light-emitting-diodes-leds).

## Where to buy in Vietnam

The full cart, including the microcontroller, the TB6612, and the TT motors that justify the 100 µF story, is in [Bill of materials and how to buy the kit in Vietnam]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %}). Buy those there. This lesson does not add another driver.

If the LED assortment is not already in the cart, Hshop listed a 3 mm pack at 20 000 ₫ on 23 September 2026: [bộ 5 loại LED 3 mm](https://hshop.vn/bo-5-loai-led-sieu-sang-3mm-thong-dung-5-kind-3mm-transparent-color-led). Confirm the live price.

A 1N4007 and a 100 µF, 16 V or 25 V electrolytic were not a single verified Hshop product link in this lesson's source list. Use search pages and read the voltage rating yourself: [Shopee search for 1N4007](https://shopee.vn/search?keyword=1N4007) and [Shopee search for tụ 100uF](https://shopee.vn/search?keyword=t%E1%BB%A5%20100uF). Both of those are search pages, not products. [Thế Giới IC](https://www.thegioiic.com/) and [IC Đây Rồi](https://icdayroi.com/) are component counters if you would rather buy two loose parts than a kit. Do not power any of them until the stripe and the band have been written down.
