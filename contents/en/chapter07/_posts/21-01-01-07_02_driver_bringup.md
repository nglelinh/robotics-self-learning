---
layout: post
title: "Lab: motor driver bring-up and spin test"
chapter: "07"
order: 2
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter07
lesson_type: required
draft: false
---

This is the first powered spin: wheels in the air, one motor at a time, until positive PWM rolls both tires toward the nose.

## Learning objectives

1. Bring the robot up on a box so both tires are clear of the table, and spin one motor at a time with PWM held to 60–80 counts out of 255.
2. Drive TB6612 STBY high before you blame the sketch, and record the IN pair that makes the left tire forward and the IN pair that makes the right tire forward.
3. Correct a backward tire by swapping that motor's leads or by planning a firmware sign flip, and refuse to do both.
4. Measure no-load current, treat a stall as a one-second measurement, and stop if the driver smells or the tab is too hot to touch.

## Prerequisites

Lesson 07-01 left you a common ground, a fuse in the battery positive lead, and a buck at 5.0 V measured before the ESP32 was attached. Chapter 05 is the truth table: an H-bridge has a forward pair and a reverse pair, and both switches in one leg are a short. You can identify a TB6612 (STBY, PWMA, PWMB, AIN, BIN) or an L298N (ENA, ENB, INx, heatsink, 5 V jumper). Chapter 06 gave you $$b$$ and $$r$$, and it defined forward as the nose direction. A positive yaw in that chapter is the right wheel faster than the left, so the sign you discover today is the sign Chapter 08's PID and Chapter 09's topics will inherit. No ROS node is part of this lab.

## Why this matters for Capstone A and the ROS path

A later `geometry_msgs/Twist` carries `linear.x` forward and `angular.z` as yaw. Those become a left command and a right command. If the right tire's positive is physically backward, every positive `linear.x` is a spin, and Chapter 08's PID will try to cancel a wiring error. Find the sign here, wheels in the air. Lesson 03 only names the two numbers. They are not meters per second.

## One channel, a small duty, STBY awake

Put the chassis on a box or a stack of books. Both tires must be in free air. A tire on the table at the first PWM is how a robot leaves the bench.

Command one motor. Leave the other at PWM 0. The first duty is 60, 70, or at most 80 counts out of 255, not 255. On a pack sitting at $$7.6~\mathrm{V}$$,

$$
D = \frac{70}{255} \approx 0.275, \qquad V_{avg} \approx 0.275 \times 7.6~\mathrm{V} \approx 2.09~\mathrm{V}
$$

before the bridge drop. A TB6612 is a MOSFET bridge and gives most of that 2 V to the brushes, so the tire turns slowly and you can see the direction. An L298N may drop $$1.5$$–$$2~\mathrm{V}$$ and the same duty may only creep; that is a reason to prefer the TB6612, not a reason to start at full scale. If you must raise the duty to see motion on an L298N, do it in small steps and keep the stall rule below.

On a TB6612, STBY has to be high or both bridges stay in standby no matter what the IN pins and the PWM pins do. A floating STBY is the usual "the sketch is perfect and nothing moves" fault. Set it high with a wire to VCC for this lab, or with a GPIO you will drive high in lesson 04. On an L298N the matching trap is ENA or ENB left low, or the 5 V jumper removed while the logic pin has no other 5 V.

![Forward is one diagonal of the H; the other diagonal is reverse]({{ site.imgurl }}/generated/hbridge_concept.png)

![L298N module: screw terminals for the motors, heatsink on the Darlingtons]({{ site.imgurl }}/wikimedia/Dosmotorsl298n.jpg)

Watch the left tire against the nose. Record the IN pair that rolls it forward, then do the right tire alone. An example you must replace: left forward is AIN1 high, AIN2 low, PWMA 70; right forward is BIN1 high, BIN2 low, PWMB 70. If the right tire rolls backward, swap that motor's two screws once, or leave the screws and invert the right-hand sign in lesson 04. Do not do both. Two inversions cancel, and lesson 05's straight command becomes a spin.

## No-load current, and a stall you do not hold

With one tire in the air at PWM 70, a yellow TT motor often draws on the order of $$0.10$$–$$0.20~\mathrm{A}$$. Write the number your meter shows, in series with that motor or at the battery lead with the other motor off. Two motors later add. They do not multiply the stall rating into the no-load reading.

![No-load current is the low end of the curve; stall is the high end]({{ site.imgurl }}/generated/stall_current.png)

If you need a stall point, pinch the tire for one second, read the meter, and release. A seller stall of $$1.2~\mathrm{A}$$ at $$6~\mathrm{V}$$ is the order of magnitude, not a value to hold. At PWM 70 the stall current is lower than the full-voltage stall, and it still heats the winding and the tab. If the package smells, or you cannot touch the L298N tab or the TB6612, open the switch. The sentence for the next lesson: with your IN map, positive PWM rolls both tires forward, negative reverses them, and PWM 0 stops. That is the sign map.

## Lab

### Safety

Tires are off the table. One motor at a time for the first spins. PWM stays in 60–80 out of 255 until the direction is obvious. The battery switch is your kill, and it is in reach. Stall measurements last one second. A hot tab or a smell ends the lab. Motor current still comes from the fused battery, not from USB. Fingers stay off the pinion.

### BOM

| Item | Role |
|------|------|
| Robot from lesson 07-01 | Power tree already measured |
| TB6612 or L298N | The bridge under test |
| ESP32 or three jumpers | STBY or ENA high, IN pair, PWM |
| Ammeter or multimeter in series | No-load, and a one-second stall if you take one |
| Tape flag on each tire | Direction you can see from the nose |
| `lab-notes.md` | The sign map |

### Steps

1. Box under the chassis. Confirm both tires clear the box and the table.
2. STBY high on a TB6612, or ENA/ENB available on an L298N. PWM 0. Battery on.
3. Left motor only. PWM 70. Try the two IN combinations that are not both-high. Record which pair rolls the tire toward the nose.
4. Repeat for the right motor. If a tire is backward, swap that motor's two screws or mark "invert in firmware," not both.
5. Measure no-load current at PWM 70 for each motor. Optional: one-second stall, then release. Write "positive PWM → both wheels forward" in your own pin names.

### Expected results

A sign map with pin levels, a no-load current for each motor (example shape: left $$0.12~\mathrm{A}$$, right $$0.15~\mathrm{A}$$ at PWM 70 — your numbers will differ), and a note that STBY or enable was high. Both flags, viewed from behind the robot, travel the nose direction when the command is positive. Nothing in the notes says the tire was fixed by swapping leads and by inverting code.

### Faults

| What you see | What it usually means |
|--------------|------------------------|
| Both motors dead, code looks right | STBY low or floating; ENA/ENB low on an L298N |
| Only one motor turns | That channel's PWM pin, IN pair, or screw is open |
| Tire turns, then the driver smells | Duty too high or a stall held too long; switch off |
| Left forward, right backward, same IN pattern | Swap the right motor leads or the firmware sign, once |
| Current stays near stall in "free" air | Tire rubbing the plate, or gearbox binding |

## Mua ở Việt Nam / Where to buy in Vietnam

You should already own the driver. If lesson 07-01 left you with motors and no bridge, buy a TB6612 first. An L298N is an acceptable substitute and runs hotter; keep its heatsink, and still use the buck for the ESP32. Prices move. Rough 2026 bands: TB6612 module $$25.000$$–$$70.000$$ VND, TT motor $$25.000$$–$$45.000$$ VND each, L298N about $$45.000$$ VND on the verified page below. A DRV8833 is fine for a much smaller motor and is a weak substitute for a TT pair at stall.

- Verified L298N, about $$45.000$$ VND: [hshop.vn/mach-dieu-khien-dong-co-dc-l298](https://hshop.vn/mach-dieu-khien-dong-co-dc-l298)
- [Hshop TB6612](https://hshop.vn/search?q=TB6612), [motor TT](https://hshop.vn/search?q=motor%20TT)
- [Shopee TB6612](https://shopee.vn/search?keyword=TB6612), [motor TT](https://shopee.vn/search?keyword=motor%20TT)
- [Lazada TB6612](https://www.lazada.vn/catalog/?q=TB6612), [L298N](https://www.lazada.vn/catalog/?q=L298N)
- [Thế Giới IC TB6612](https://www.thegioiic.com/search?q=TB6612), [L298N](https://www.thegioiic.com/search?q=L298N)

## Exercises

1. VM is $$8.0~\mathrm{V}$$ and the first command is 80 counts out of 255. Compute $$D$$ and $$V_{avg}$$ before bridge drop. If an L298N then drops $$1.8~\mathrm{V}$$, what is left for the brushes?
2. No-load at PWM 70 is $$0.14~\mathrm{A}$$. A one-second pinch reads $$0.95~\mathrm{A}$$. Why are both numbers plausible on the stall curve, and why do you release?
3. STBY is floating, AIN1 is high, AIN2 is low, PWM is 80. The tire is still. What is the first wire you add?
4. The right tire is backward. You swap its leads and you also multiply the right command by $$-1$$ in the sketch you are about to write. What does positive PWM do on the floor?
5. Left forward is AIN1 = 1, AIN2 = 0. Right forward, before any fix, is BIN1 = 0, BIN2 = 1. Write the sign-map sentence lesson 04 must implement, without a second inversion.

### Answer guidance

1. $$D = 80/255 \approx 0.314$$, $$V_{avg} \approx 0.314 \times 8.0 \approx 2.51~\mathrm{V}$$. After a $$1.8~\mathrm{V}$$ drop the brushes see about $$0.7~\mathrm{V}$$, which may not overcome friction. That is a TB6612 argument, not a reason to start at 255. 2. No-load is the low-current end, where back-EMF cancels most of the supply. The pinch collapses back-EMF and current rises toward stall. One second, then release; a hot tab or a smell means stop. 3. Drive STBY high. Until that pin is high the TB6612 stays in standby and the IN pins do not matter. 4. The two inversions cancel. Positive PWM still rolls that tire backward, the notebook says you "fixed" it, and a straight command spins. Do only one of the two fixes. 5. Positive left command: AIN1 high, AIN2 low. Positive right command: BIN1 low, BIN2 high. Negative swaps each pair. Do not also swap the right-hand screws.

## Further reading

- [Pololu TB6612FNG](https://www.pololu.com/product/713)
- [ST L298 datasheet](https://www.st.com/resource/en/datasheet/l298.pdf)
- [geometry_msgs/Twist (Jazzy)](https://docs.ros.org/en/jazzy/p/geometry_msgs/interfaces/msg/Twist.html)
- [Arduino `Serial`](https://www.arduino.cc/reference/en/language/functions/communication/serial/)
