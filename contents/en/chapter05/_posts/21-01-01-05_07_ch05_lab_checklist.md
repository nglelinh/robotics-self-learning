---
layout: post
title: "Chapter 05 lab checklist"
chapter: "05"
order: 7
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter05
lesson_type: required
draft: false
---

This lesson is a gate. Chapter 06 will put your drive on a chassis, and Chapter 07 will assemble signed left and right PWM, a battery, and a fuse. You pass the gate when the table below is filled with your own evidence: a named driver, a truth table, a motor supply that is not USB, a stall or no-load note, a servo-pulse calculation even if you skipped the horn, a bang-bang stop you can describe, a wiring photo, and two failure modes you either hit or deliberately rehearsed. A blank row means you are still in Chapter 05.

## Learning objectives

1. Complete the sign-off table with measured or computed evidence, not with a retelling of the lesson titles.
2. Show a wiring photo where motor current and USB are separate supplies that share a ground.
3. State a pass condition you could explain out loud to a lab partner before you start Chapter 06 mechanics.
4. List only the parts you still lack (driver, TT motor, fuse) and the search you will use to buy them.

## Prerequisites

Lessons 05-01 through 05-06 are the source of every row. You need `lab-notes.md` open, the multimeter, and the photo you took when the wires were actually on the driver. If a hardware row was impossible, the row still needs the written calculation this checklist names. "I will do it later" is not a pass.

## Why this matters for Capstone A and the ROS path

Capstone A is a two-wheel robot whose later ROS 2 base receives a twist and emits two wheel efforts. That software is only as honest as the signs you recorded here. A truth table copied from a classmate, a servo pulse you have never calculated, or a stall current you have never compared with your fuse, becomes a robot that yaws the wrong way, browns out, or drives through a timeout. The gate is deliberately boring. Chapter 06's brackets and Chapter 07's harness assume these answers already exist in your notebook.

## What each row is asking

**Driver identified.** Write the chip, not the color of the PCB: L298N, TB6612, or DRV8833. Add the one pin that bites people on that chip. For a TB6612 that sentence is "STBY must be high or the motors stay asleep." For an L298N it is "the 5 V jumper comes off if VM is above 12 V, and the ESP32 is not fed from the onboard 7805." For a DRV8833 it is the motor range, about 2.7–10.6 V, and the fact that a TT pair at stall is a lot to ask.

**Truth table recorded.** Four rows, or the rows your chip actually documents, with IN1, IN2, PWM, and what the shaft did. Circle the forward triple Chapter 07 will call positive. If both inputs equal produced a brake on your board, say so. That row is not optional color.

**Motor supply separated from USB.** The photo should show a battery or a bench supply on VM, USB on the microcontroller only, and a ground wire between them. A caption that says "common ground" without the wire in frame does not pass.

**Stall or no-load note.** A measured no-load current for one motor, plus either a one-second stall reading taken under a current limit or the computed watts from the seller's stall current. The fuse sentence sits in this same note: the fuse value is above running current and is there to open on a short.

**Servo pulse.** If you swept a horn, paste the three angles. If you had no servo, write

$$
\frac{1.5~\mathrm{ms}}{20~\mathrm{ms}} = 7.5\%
$$

and one sentence: a 7.5% duty on a 1 kHz pin is a 75 µs pulse, so the command you will use is `writeMicroseconds(1500)` from a servo library.

**Bang-bang behavior.** Three cases in your own numbers: a far reading, a reading under 20 cm, and a timeout or 0. All three named, with PWM 80 forward only on the valid far reading. Say that a future `/cmd_vel` does not override the stop.

**Wiring photo.** One image, pins readable enough that a partner can find VM, ground, and the PWM wire.

**Two failure modes.** These must be yours. Hitting them counts. Rehearsing them counts: unplugging the echo wire and watching the stop, or computing the USB stall current and writing "I will not power VM from USB" because 2.4 A is not 0.5 A. A copied list from this page, with no verb you performed, does not count.

## Worked example

A notebook claims: TB6612, STBY tied to 3.3 V, forward is IN1 = 1, IN2 = 0, PWM > 0, VM from 2S, USB only on the ESP32, no-load 0.18 A at 7.4 V, seller stall 1.2 A at 6 V. Check the stall arithmetic before you accept the row.

$$
R \approx \frac{6}{1.2} = 5~\Omega
$$

$$
P = I^2 R = (1.2)^2 \times 5 = 7.2~\mathrm{W}
$$

The note "about 7 W if stalled at the rated 6 V" matches. Two motors would be about 2.4 A at that stall. A running guess of 0.2 A per motor plus 0.1 A of logic is 0.5 A, so a 2 A fuse in the battery positive lead sits above running current and still has a job during a dead short. Their servo row says $$1500/20000 = 0.075$$. Their bang-bang row says 180 mm stops, 900 mm runs at PWM 80, timeout stops. They rehearsed a floating STBY (wheels dead until the wire was added) and a timeout that they had first treated as "far," then fixed. That notebook passes. A notebook with the chip name and empty measurement cells does not.

## Figures

Use these three as the pictures you should be able to narrate while you sign the table.

![H-bridge path you traced when you wrote the truth table]({{ site.imgurl }}/generated/hbridge_concept.png)

![Stall versus no-load, the curve behind your current note]({{ site.imgurl }}/generated/stall_current.png)

![Sense, compute, act, including the stop that a failed read must take]({{ site.imgurl }}/generated/sense_compute_act.png)

## Lab

### Safety

This sign-off does not ask you to repeat every experiment at full power. If a row is missing because a stall would have been unsafe, compute it and say why you refused the stall. Do not plug VM into USB "just for the photo." Wheels stay up if you re-run a truth-table row. Hand on the power switch if you re-run the floor stop.

### BOM

| Item | Role |
|------|------|
| `lab-notes.md` and the wiring photo | The evidence |
| Multimeter | Only if a voltage cell is still blank |
| The driver, one motor, the range sensor | Only to fill a row you skipped |
| Fuse and holder, if none is in the kit | The Chapter 07 part you can buy now |

### Steps

1. Copy the sign-off table into `lab-notes.md`.
2. Fill each cell from notes you already have. Where a cell is empty, do the smallest measurement or calculation that makes it true.
3. Attach or link the wiring photo. Caption it with the chip name and "VM source: …".
4. Read the pass paragraph below out loud. If you hesitate on a row, that row is not done.
5. Write the buy list only for gaps: driver, TT motor, fuse. Skip parts you already own.

### Expected results

A completed table and a one-paragraph pass statement in your own words. Your partner, shown only the photo and the table, can point to the forward motor state and to the sensor condition that forces PWM 0.

### Faults

| What you see | What to check |
|--------------|----------------|
| Every cell says "yes" with no number | Replace "yes" with a voltage, a current, a pulse width, or a distance. |
| Truth table has no brake/coast row | Go back to lesson 05-01 and record the both-inputs-equal state on your chip. |
| Photo shows one USB cable and no battery | Motor supply is not separated. Retake the photo with VM on the pack. |
| Servo row blank because you had no horn | Write the 7.5% calculation and the 75 µs contrast at 1 kHz. |
| Failure modes are the textbook list | Name two you caused or rehearsed, including what the shaft did. |

### Sign-off table

| Row | Your evidence | Done |
|-----|----------------|------|
| Driver chip and the pin that bites (STBY, 7805 jumper, or VM range) | | |
| Truth table: IN1, IN2, PWM, direction, including coast or brake | | |
| Motor supply separated from USB, common ground (photo) | | |
| No-load current, and stall amps or computed stall watts | | |
| Servo: angles, or $$1.5/20 = 7.5\%$$ and `writeMicroseconds(1500)` | | |
| Bang-bang: far, under 20 cm, timeout/0 | | |
| Wiring photo filed | | |
| Two failure modes you hit or rehearsed | | |

**Pass means** every row above is filled, the photo matches the supply story, and you can say what the shaft does when the range sensor times out. With that, you may start Chapter 06 mechanics and you are ready for Chapter 07 to trust your forward sign, your fuse, and your habit of setting PWM to 0 before anything else.

## Mua ở Việt Nam / Where to buy in Vietnam

Buy only the gap. The usual gaps at this gate are a driver (TB6612 preferred, L298N acceptable), one or two TT gearmotors, and a 2–3 A fuse with a holder in the battery positive lead. Prices move. Rough bands: L298N module about 35.000–70.000 VND, TB6612 module about 40.000–120.000 VND, TT motor about 25.000–45.000 VND, fuse and holder about 5.000–25.000 VND.

- Verified L298N page, about 45.000 VND: [hshop.vn/mach-dieu-khien-dong-co-dc-l298](https://hshop.vn/mach-dieu-khien-dong-co-dc-l298)
- HShop: [TB6612](https://hshop.vn/search?q=TB6612), [motor TT](https://hshop.vn/search?q=motor%20TT), [cầu chì](https://hshop.vn/search?q=cau%20chi)
- Shopee: [TB6612](https://shopee.vn/search?keyword=TB6612), [motor TT](https://shopee.vn/search?keyword=motor%20TT), [cầu chì](https://shopee.vn/search?keyword=cau%20chi)
- Lazada: [L298N](https://www.lazada.vn/catalog/?q=L298N), [motor TT](https://www.lazada.vn/catalog/?q=motor%20TT)
- Thế Giới IC: [TB6612](https://www.thegioiic.com/search?q=TB6612), [L298N](https://www.thegioiic.com/search?q=L298N)

## Exercises

1. Which single cell, if left as the word "yes," fails the gate even when the other cells are numeric?
2. Your stall note says 1.2 A at 6 V. Compute $$R$$ and $$P$$ and say whether "about 7 W" would pass.
3. You had no servo. Write the exact calculation and the function call that belong in that row.
4. Name the three bang-bang cases the row must contain.
5. Chapter 06 starts when which spoken sentence is true? Include the timeout behavior.

### Answer guidance

A cell that says only "yes" fails that row; the gate wants a number, a pin name, or a photo. $$R \approx 5~\Omega$$ and $$P = 7.2~\mathrm{W}$$, so "about 7 W" passes the arithmetic. With no servo, write $$1.5/20 = 7.5\%$$ and `writeMicroseconds(1500)`. The three cases are a valid far reading (PWM 80 forward), a reading under 20 cm (PWM 0), and a timeout or 0 (PWM 0). You may start Chapter 06 when you can say that a timed-out range sensor forces the motors off, and the rest of the table is filled with your own evidence.

## Further reading

- ST L298 datasheet: [https://www.st.com/resource/en/datasheet/l298.pdf](https://www.st.com/resource/en/datasheet/l298.pdf)
- Pololu TB6612FNG: [https://www.pololu.com/product/713](https://www.pololu.com/product/713)
- SparkFun motor selection (stall versus no-load): [https://learn.sparkfun.com/tutorials/motors-and-selecting-the-right-one/all](https://learn.sparkfun.com/tutorials/motors-and-selecting-the-right-one/all)
- ROS 2 topics, the later home of `/cmd_vel`: [https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Topics/Understanding-ROS2-Topics.html](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Topics/Understanding-ROS2-Topics.html)
