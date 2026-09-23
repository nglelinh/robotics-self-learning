---
layout: post
title: "Lab — continuity, ohms, and lookalikes"
chapter: "01"
order: 10
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter01
lesson_type: required
draft: false
---

This hour is a bench session. The earlier lessons handed you a color code, a diode band, and an electrolytic stripe one part at a time. Today those parts share one unpowered breadboard, and the grade is a table of numbers you measured. A photograph of a parts pile is not a measurement. A color code you did not check with the meter is a guess you will later solder into the cart.

## Learning objectives

You will map which breadboard rows beep and which gap stays open, and you will photograph that map. You will decode five resistors and measure each one out of circuit, then keep or reject it against its tolerance. You will use diode mode on one LED and one diode, record the forward reading, and write which lead is the anode. You will separate three lookalike pairs in writing: a color-banded resistor and a color-banded inductor, a ceramic capacitor and a tantalum capacitor, a TO-92 transistor and a TO-92 regulator. You will name three measurement faults before they get into the table: ohms measured in-circuit, diode-mode probes that your particular meter has swapped, and a 5-band resistor read as 4-band.

## Prerequisites

Lessons 02 through 05 are the background: breadboard rows, the meter, resistor codes, capacitors, diodes, and LEDs. You need continuity, ohms, and diode mode. You do not need the iron, and you do not need the TB6612 powered. If a part is missing, write the step and mark the row dry-run. Do not borrow a classmate's numbers.

## Why it matters

The diff-drive cart is still a 3.3 V ESP32 or Pico, a TB6612, two TT motors on their own battery, and an HC-SR04 whose echo is 5 V. None of those modules excuse a wrong part in the harness around them. The status LED on a GPIO needs a resistor you measured, not a band you misread by a decade. The bulk capacitor on VM, 100–470 µF from lesson 09, is an aluminum electrolytic with a negative stripe; a tantalum bead uses a stripe that often means the opposite, and swapping that rule vents a part on the motor rail. A TO-92 regulator dropped into a transistor footprint, or the reverse, is how a 3.3 V rail dies while the motors are still innocent. The table from this lab is the evidence that you can tell those parts apart before any of them is buried in heat-shrink.

## What is on the bench

For this hour: one meter, one breadboard, five resistors, one aluminum electrolytic, one ceramic capacitor, one LED, one diode, and a handful of jumpers. Nothing else is required, and nothing is powered. The ceramic is the disc or the little block with no polarity mark. The electrolytic is the can. The diode is whatever number is printed on the part you actually have; write that number, and do not relabel a 1N4001 as a 1N4007 because the exercise said "diode."

![Color bands you will check, not trust]({{ site.imgurl }}/generated/resistor_color_code.png)

Keep the chart beside the five resistors while you fill the nominal column. The meter is allowed to disagree. When it does, you reread the bands, including the possibility that you treated five bands as four. You do not edit the meter to match the chart.

![Bodies that match and insides that do not]({{ site.imgurl }}/generated/component_lookalikes.png)

This figure is why the lookalike list exists. Same outline, different part. Your list names the pair, the test, and the result. "They look different to me" is not a test.

![An assortment, before any of it is in a circuit]({{ site.imgurl }}/wikimedia/resistors_assortment.jpg)

Pick five values you can decode, including at least one that is not 220 Ω and not 10 kΩ, so the hour cannot be passed from memory.

![Which lead of the capacitor is negative]({{ site.imgurl }}/generated/capacitor_polarity.png)

On the aluminum can in this kit, the stripe is negative. You will point at it. You will not apply that sentence to a tantalum bead.

![LED polarity is a meter question if the leads have been trimmed]({{ site.imgurl }}/wikimedia/LEDs.jpg)

The long lead is usually the anode, and the flat on the rim is usually the cathode. Trimmed leads and cheap lenses break the habit. Diode mode is the check you record.

## Procedure

Power stays off for the whole hour. No USB, no battery, no motor.

1. **Map the rows that beep.** Continuity mode. Beep a group of five holes in the center and confirm they are one node. Beep across the center trench and confirm it is open. Beep each supply rail from end to end. If the beep stops halfway, the rail is split; mark the break on a sketch. This sketch is part of the grade. A later "the LED is dead" includes the possibility that you were never on one node.
2. **Decode, then measure, five resistors.** For each, write the colors, the nominal ohms, and the tolerance. Measure out of circuit, legs not pinched in your fingers if the value is large, because skin is a resistor too. A 5% part passes only inside

$$
R_{\mathrm{nom}}(1 - 0.05) \le R_{\mathrm{meas}} \le R_{\mathrm{nom}}(1 + 0.05)
$$

Gold as the last band is 5%. If the code and the meter disagree, the meter starts a second look at the bands. A part outside the window is set aside. It does not go back into the known-good bag. Short the meter leads once and write that offset, often a few tenths of an ohm. It matters for a 10 Ω part and it does not matter for a 10 kΩ part.
3. **Diode mode on the LED and on the diode.** Record the forward reading and which physical lead was on the red probe when you got it. That lead is the anode for this measurement, after you have confirmed how your meter is wired. Also record the open or overload reading with the probes swapped, and the feature you can see: flat, short lead, or cathode band. A red LED often shows roughly 1.6–2.2 V and may glow faintly. A silicon diode often shows roughly 0.5–0.8 V. "OL" in both directions on an LED can mean a dead part or a meter whose diode voltage cannot light that color. Say which you believe, and why.
4. **Lookalike list, three pairs.** Write them into the notes even if you only have one side of the pair on the bench. Say what you would measure.

A resistor and a small inductor can wear the same color bands. The resistor measures near its code. The inductor, a coil of wire, measures near a short, a few ohms or less, far below a 1 kΩ or 10 kΩ code. Do not install the coil as the LED's series resistor. You will current-limit nothing and you may cook the LED or the GPIO.

A ceramic disc has no polarity. A tantalum capacitor is polarized, and the stripe or bar on many tantalum beads marks the positive lead, which is the opposite of the aluminum can in the polarity figure. If you are not sure which family a bead belongs to, it does not go across VM. The aluminum rule and the tantalum rule are not interchangeable.

A TO-92 transistor and a TO-92 regulator share the half-cylinder body. The marking decides. A code such as 78L05 is a regulator, with a pinout in the family of input, ground, and output. A code such as S8050 or BC547 is a transistor, with some order of emitter, base, and collector that you look up rather than guess. A rubbed-off marking goes to the unknown bag. It does not power the ESP32.

## Faults that manufacture bad numbers

Measuring ohms in-circuit reads the network, not the part. A 220 Ω resistor beside other parts can show 80 Ω and still be a good 220 Ω part. Lift one leg. If you cannot, you are not measuring that resistor.

Some meters swap the sense of diode mode, or a probe has been parked in the wrong jack since yesterday. The red lead is positive on most digitals and not on all of them. Prove yours once: the lead that produces the forward reading on a known diode is the anode side of that diode. Write "red = anode source" or "red is swapped" at the top of the table. A reversed assumption labels every cathode in the notebook backwards, including the LED you will hang on a 3.3 V pin.

Reading a 5-band resistor as a 4-band part moves the multiplier. Five bands are three digits, then multiplier, then tolerance. Four bands are two digits, then multiplier, then tolerance. Brown-black-black-red-brown is not the same recipe as brown-black-black-gold. When the meter disagrees by about ten or a hundred, recount the bands before you condemn the part.

## The table the notes must contain

Copy this and fill it. Expected ranges are there so a blank "ok" cannot pass.

| # | Part | What you read | Nominal or polarity | Measured | Pass? |
|---|------|---------------|---------------------|----------|-------|
| 1 | five-hole row | which holes | one node | beep or open | |
| 2 | center trench | across the gap | open | beep or open | |
| 3 | red rail | end to end | continuous or split | where it stops | |
| 4–8 | five resistors | colors | Ω and % | Ω | yes/no |
| 9 | LED | anode lead | long lead or not | forward V | |
| 10 | diode | anode lead | band is cathode | forward V | |
| 11 | electrolytic | stripe | negative | photo name | |

A resistor row passes only with both a decoded value and a measured value. An LED row passes only with a number and the word anode attached to a lead. File it as `ch01-10-id-table`.

## Worked example

Bands brown, black, red, gold. That is 1, 0, two zeros, 5%, so $$1.0\,\mathrm{k}\Omega \pm 5\%$$.

$$
1000 \times 0.95 = 950,\qquad 1000 \times 1.05 = 1050
$$

The meter shows 1027 Ω. The row passes. A second part, coded 220 Ω, is still sitting in a breadboard next to an LED circuit and the meter shows 86 Ω. That reading is discarded. One leg is lifted. The new reading is 218 Ω, inside $$220 \times 0.95$$ to $$220 \times 1.05$$, and the row passes. The 86 Ω was the network.

A third part has five bands and was first written down as if it had four, producing 1000 Ω on paper and about 100 Ω on the meter. Recounting as three digits plus a multiplier removes the decade error. The part was never bad.

On the diode, the banded end is the cathode, so the anode is the other lead. Red probe on the anode, black on the band, the display shows 0.62 V. Probes swapped, the display shows OL. On the red LED, red on the long lead shows 1.85 V and a faint glow, so that long lead is the anode today. Those two voltages in one table are how you prove the parts were not swapped: about 0.6 V is the diode, about 1.8 V is the red LED.

## Exercises

1. A 470 Ω, gold-band resistor measures 502 Ω. Compute the 5% window and give the verdict.
2. Diode mode shows OL with red on the long LED lead and 1.9 V with red on the short lead. Your meter was already proven to put positive on red. Which lead is the anode, and what did OL mean?
3. A 1 kΩ resistor in an unpowered board reads 120 Ω. What is the first correction, and why is "the code is wrong" not that correction?
4. An unmarked banded part coded like 10 kΩ measures 1.2 Ω. What is the more likely identity, and may it be the series resistor for a 3.3 V LED?
5. A TO-92 part's marking is gone. Write the lookalike entry, and say whether it may feed the ESP32.

<details markdown="1">
<summary>Hints and answers</summary>

1. The window is $$470 \times 0.95 = 446.5\,\Omega$$ to $$470 \times 1.05 = 493.5\,\Omega$$. 502 Ω is outside. Fail, and set it aside.
2. The anode is the short lead, because that is where a positive red probe produced 1.9 V. OL was the reverse direction, not automatically a dead LED. The long-lead habit failed, which is why the meter is in the procedure.
3. Lift one leg and measure again. Parallel paths read low. Judge the color code only after the part is alone. The board was unpowered, which is required and still not enough.
4. A steady reading near a short, against a 10 kΩ code, is the inductor lookalike (or a destroyed part). It must not be the LED resistor. A real 10 kΩ part would measure near 10 kΩ.
5. "TO-92, marking illegible, transistor or regulator unknown, pinout unknown." It may not feed the ESP32. Unknown function plus unknown pinout is how rails get shorted.

</details>

## Further reading

- [SparkFun: how to use a multimeter](https://learn.sparkfun.com/tutorials/how-to-use-a-multimeter) — continuity, ohms, and diode mode, which are the only three functions this lab allows.
- [SparkFun: resistor color codes](https://learn.sparkfun.com/tutorials/resistors/resistor-color-code) — 4-band and 5-band on one page, for the recount in step 2.
- [ESP32 datasheet (PDF)](https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf) — the 3.3 V rail your LED resistor must respect, from lesson 07.

## Where to buy in Vietnam

If the Chapter 00 kit is already on the bench, buy nothing. The list is lesson 05, [Bill of materials and how to buy the kit in Vietnam]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %}).

Two pages are enough when something on the BOM above is missing. The breadboard, 35,000₫ on 23 September 2026, is [Hshop test board CAMMB-102](https://hshop.vn/test-board-cammb-102). The meter, live price on the page, is the [UNI-T UT33D at Hshop](https://hshop.vn/dong-ho-van-nang-dien-tu-digital-multimeter-uni-t-ut33d-chinh-hang). Loose resistors, one LED, one diode, and one electrolytic can come from the shop fronts [Hshop](https://hshop.vn/), [Thế Giới IC](https://www.thegioiic.com/), and [IC Đầy Rồi](https://icdayroi.com/). This lesson does not invent slugs for them. Write the number printed on the diode you received.
