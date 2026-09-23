---
layout: post
title: "Chapter 01 lab checklist"
chapter: "01"
order: 11
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter01
lesson_type: required
draft: false
---

Chapter 01 ends when seven pieces of evidence are in the notes, each one able to fail in a way you can point at. A tick beside "I understand pinouts" is not evidence. This lesson is the audit: what a real pass looks like, what a weak tick looks like, and the short path back when a row is thin. You may close the gates in any order. You may not replace a missing photo with a classmate's.

## Learning objectives

You will score seven gates against artifacts, not against a feeling of being done: an LED resistor calculation at 3.3 V, a breadboard rail-map photo, five resistors that were both decoded and measured, one polarity call confirmed in diode mode, a driver photo labeled TB6612 or DRV8833 rather than "H-bridge," one solder-joint photo or a dated make-up if you still have no iron, and a brownout paragraph that names the separate motor battery. You will recognize a weak tick, such as a checkmark with no number or a photo of the wrong chip, and you will name the single lesson that repairs it. You will take a sloppy lab note and say which gate it fails.

## Prerequisites

Lessons 07 through 10 produced the artifacts this page inspects, and lesson 01 produced the LED arithmetic. The shopping list, when a row is blocked by a missing object, is Chapter 00 lesson 05. You need your notes and your photos. You still do not need a moving robot. Wheels stay up. No motor is connected to celebrate a pass.

## Why it matters

The capstone is a differential-drive cart on a 3.3 V ESP32 or Pico, a TB6612 or a DRV8833, two TT motors on their own battery, and an HC-SR04 whose echo pin is 5 V. Chapter 02 will start attaching those pieces. If the rail map is a blank breadboard photo, the first dark LED is an afternoon. If the driver photo says only "H-bridge," STBY never gets driven and the wheels sit still. If the brownout paragraph was never written, a reset when the motors share USB looks like a haunted sketch. The audit is how you notice those gaps while the only thing powered is the notebook.

## How to audit a row

A gate has an artifact and a test you can apply without asking what the instructor meant. The artifact is a calculation with units, a labeled photo, or a paragraph that contains a number. The test is a comparison: inside a tolerance window, the stripe called negative, the chip name readable, the paragraph containing the words "separate motor battery." A weak tick has the checkmark and is missing the comparison. "Done" with no ohms, "photo taken" of an unlabeled board, and "understood brownout" with no sentence are the three weak ticks this chapter actually produces. They score as open. They do not score as almost.

The remediation path is short on purpose. Reopen the one lesson named on the gate, repeat only the step that produces the artifact, and date the new file. Do not rewrite the whole chapter, and do not start Chapter 02 motion while the brownout paragraph or the driver label is still a weak tick. Those two are the ones that destroy parts or masquerade as software. A missing iron is the exception: you may schedule a make-up, and the schedule is the artifact until the joint exists.

## The seven gates

**1. LED calculation at 3.3 V.** Write the arithmetic for the status LED that will hang on a GPIO. Pick a forward drop and show it. For a red LED, $$V_F = 2.0\,\mathrm{V}$$ is fair if lesson 10 did not measure one. With a 220 Ω resistor,

$$
I = \frac{3.3 - 2.0}{220} = \frac{1.3}{220} \approx 5.9\,\mathrm{mA}
$$

Pass: the expression, the substitution, the result in milliamperes, and one sentence that this current is in the 5–10 mA band a small LED and a 3.3 V GPIO can live with. Using your measured $$V_F$$ from lesson 10 is better, if you show it. Dividing 3.3 by the resistor and forgetting $$V_F$$ fails, however neat the handwriting. A result near zero for a blue LED passes only if you then say the LED will be dim and you choose a different color or a smaller resistor.

**2. Breadboard rail map.** A photo or a sketch from lesson 10 that shows a five-hole node, the open trench, and whether each supply rail is continuous or split. Pass: another person could place a jumper using only that sheet and land on the node you meant. An unlabeled photo of an empty board fails.

**3. Five resistors, decoded and measured.** Five rows, each with colors, nominal, tolerance, and an out-of-circuit measurement, marked pass or fail against the window. A color code with no meter reading fails. A meter reading with no colors fails. A value taken while the resistor was still in a circuit fails. Four good rows and a blank fifth is not "mostly."

**4. One polarity call in diode mode.** Either the LED or the diode, with a forward voltage and a sentence of the form "this lead is the anode." Pass: a stranger could connect that LED from 3.3 V through the resistor in gate 1, anode toward the GPIO, cathode toward ground, without asking you. A photo with no words fails. Calling the stripe on an electrolytic "probably negative" does not satisfy this gate; this gate is the diode-mode call. The electrolytic stripe still belongs in your notes from lesson 10, and lesson 09 will not accept a backwards VM capacitor.

**5. Driver photo, named.** A photo of the motor-driver module on which you have written TB6612 or DRV8833, plus the pin names from that chip's own page: for a TB6612, at least AIN1, AIN2, PWMA, and STBY. "H-bridge," "motor driver," or "the small board" fails even if the picture is sharp. If the module has not arrived, the row is a dated dry-run that names which chip you ordered. A rectangle with no chip name is a weak tick.

**6. Solder joint, or a make-up.** A photo of your joint from lesson 08, continuity noted, compared with the good fillet in the joint figure. A beep plus a ball fails. A pretty open joint fails. If you have no iron yet, write the date you will do the lab and the stand-and-glasses line you will follow. That schedule is an honest delay. A photo of a factory joint on a bought module, claimed as yours, is not a delay. It is a fail.

**7. Brownout paragraph.** The note from lesson 09, containing your USB-only 5 V and 3.3 V readings if you could take them, the hypothesis that a later reset is the motors sagging a shared rail, and the fix: separate motor battery, common ground only, 100–470 µF on VM, thick wires, wheels up, PWM to 0 if the rail sags or commands stop for about 300 ms. A paragraph that powers the TT motors from the ESP32 5 V pin fails even if the grammar is tidy. The HC-SR04 echo forbid, 5 V into a 3.3 V GPIO, may sit in the same note; its absence does not by itself fail this gate, and its presence does not excuse a missing battery sentence.

## What a weak tick looks like

Compare these with the gates. "Resistors: yes" fails gate 3, because nothing was decoded and nothing was measured. "Polarity OK" fails gate 4, because no lead was named the anode and no voltage was written. "Driver: H-bridge from the kit" fails gate 5, because Chapter 02 cannot tell STBY from a sleep pin on a DRV8833. "Soldering understood" fails gate 6, because there is neither a photo nor a date. "Brownout: motors use a lot of current" fails gate 7, because the separate battery, the common ground, and the 300 ms PWM cut are missing. The repair is not a longer adjective. The repair is the artifact the gate already named.

Remediation stays inside one sitting when the part is on the bench. Gate 3 is a remeasure, not a new theory chapter. Gate 6 with no iron is a purchase from the lesson 08 list and a date on the calendar, not a rewritten definition of a fillet. Gate 5 with the wrong name is ten minutes with the Pololu page or the TI page and a new label. Do not open a motion lab to "catch up."

## Lab

This lab is the audit. Build a new circuit only to replace a failed artifact.

1. Open the notes and make seven rows, one per gate.
2. For gate 1, write the 3.3 V LED arithmetic on a fresh line, even if a similar line exists in lesson 01.
3. Attach the rail map, the five-resistor table, and the diode-mode polarity line. If a row fails its test, fix it before you score it.
4. Label the driver photo with the chip name. If the board is absent, write the dry-run and the date you expect it.
5. Re-inspect the joint photo in daylight. If the fillet is a ball, rework it before it scores, or write the make-up date if you still have no iron.
6. Read the brownout paragraph once and underline "separate," "common ground," and "300 ms." If any of those are missing, add them from lesson 09 rather than inventing a softer sentence.
7. Mark each gate pass or fail. Date the page `ch01-11-audit`. A fail names the lesson you will reopen.

No wheel turns during the audit.

## Worked example

A note says: "LED resistor done. Breadboard photo attached, no marks. Three resistors measured, two looked right. Polarity: stripe is negative I think. Driver is an H-bridge. Solder next week maybe. Brownout: don't stall the motors."

Gate 1 fails, or is at best incomplete, because no arithmetic is on the page. "Done" is the weak tick. Gate 2 fails: an unmarked breadboard photo is not a rail map. Gate 3 fails: three measurements are not five, and "looked right" is not a decode plus a meter reading. Gate 4 fails: a guess about an electrolytic stripe is not a diode-mode anode call. Gate 5 fails: "H-bridge" is the forbidden label. Gate 6 is not yet a pass; "next week maybe" becomes a pass of the make-up rule only if a real date replaces "maybe." Gate 7 fails: there is no separate battery, no common ground, no capacitor, and no 300 ms cut. The note does not scrape a pass by being sincere. The next hour is gates 1, 3, and 4 at the bench, plus a rewritten paragraph for gate 7. Gates 2 and 5 need a pencil on a photo. Gate 6 needs a date.

## Exercises

Each item is a fragment from a sloppy note. Say which gate fails, what is missing, and the smallest repair.

1. "$$3.3 / 180 = 18\,\mathrm{mA}$$, LED will be bright." Which gate, and what term did the arithmetic drop?
2. "Five resistors: 220, 1k, 10k, 330, 470. All good." Which gate, and which half of the evidence is absent?
3. "Diode mode: it beeped, so polarity is fine." Which gate, and why is a beep the wrong function?
4. "Module photo saved as driver.jpg. It is the H-bridge from Shopee, pins wired like the video." Which gate fails, and what two words would have passed the label?
5. "Joint looks okay, no photo, iron is at the shop until Friday 3 pm. Brownout paragraph says both TT motors share the ESP32 5 V pin so the wiring stays simple, echo goes straight to GPIO 4." Which gates fail, which gate can be a scheduled make-up, and which sentence is unsafe rather than merely incomplete?

<details markdown="1">
<summary>Hints and answers</summary>

1. Gate 1 fails. The LED forward drop was omitted, so 18 mA is not the current in the resistor. Rewrite as $$I = (3.3 - V_F) / 180$$ with a stated $$V_F$$. At $$V_F = 2.0\,\mathrm{V}$$ the current is about $$7.2\,\mathrm{mA}$$, which is a believable pass.
2. Gate 3 fails. The nominal values are there and the measurements are not. "All good" does not replace five ohm readings taken out of circuit.
3. Gate 4 fails. Continuity beep is not diode mode. The repair is a forward voltage and a named anode. A beep only says the leads are not open.
4. Gate 5 fails. The passing labels are TB6612 or DRV8833, plus that chip's own pin names. "H-bridge" and "like the video" do not identify STBY or nSLEEP.
5. Gate 6 may be the make-up if "Friday 3 pm" is written as the date and the joint photo is still required then. Gate 7 fails, and the sentence is unsafe: TT motors do not share the ESP32 5 V pin, and echo does not land on GPIO 4. Repair the paragraph from lesson 09 and the echo forbid from lesson 07. Do not treat that sentence as a near miss.

</details>

## Further reading

- [Pololu TB6612FNG carrier](https://www.pololu.com/product/713) — the label and the pin names gate 5 needs when the chip is a TB6612.
- [TI DRV8833](https://www.ti.com/product/DRV8833) — the other legal label. Do not mix its pin names with the TB6612 card.
- [ESP32 datasheet (PDF)](https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf) — the 3.3 V limit behind gates 1 and 7.
- [Adafruit soldering guide](https://learn.adafruit.com/adafruit-guide-excellent-soldering) — the fillet standard for gate 6, next to this course's joint figure.

## Where to buy in Vietnam

Do not build a second kit. Compare the open gates with Chapter 00, lesson 05, [Bill of materials and how to buy the kit in Vietnam]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %}), and buy only the gaps.

Gate 6, if the iron is the gap, uses the lesson 08 pages and the 23 September 2026 prices: the [60 W iron](https://hshop.vn/mo-han-60w-wadfow-wel3616-soldering-iron) at 75,000₫, the [stand](https://hshop.vn/de-gac-mo-han-tron-b-2-co-khay-roi) at 40,000₫, and the [0.8 mm Sn63 reel](https://hshop.vn/thiec-han-sunchi-kp26-0-8mm-sn63-pb37-solder-wire) at 24,000₫. Gate 2, if you have no breadboard, is the [CAMMB-102](https://hshop.vn/test-board-cammb-102) at 35,000₫. A missing meter, for gates 3 and 4, is the [UNI-T UT33D](https://hshop.vn/dong-ho-van-nang-dien-tu-digital-multimeter-uni-t-ut33d-chinh-hang). Shop fronts for a single resistor or LED, without a new slug invented here: [Hshop](https://hshop.vn/), [Thế Giới IC](https://www.thegioiic.com/), [IC Đầy Rồi](https://icdayroi.com/).
