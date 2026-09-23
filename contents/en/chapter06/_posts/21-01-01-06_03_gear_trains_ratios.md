---
layout: post
title: "Gears: spur, worm, planetary, ratio, backlash"
chapter: "06"
order: 3
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter06
lesson_type: required
draft: false
---

Estimated time: **80–100 minutes**, including a tooth count on a gearbox you own or on a clear photo of one.

## Learning objectives

By the end of this lesson you can compute a gear ratio from tooth counts, predict the output angle for a given input angle, and keep the sign of each external mesh straight. You can say what a worm stage is for, quote the textbook planetary ratio while trusting the number stamped on a TT motor, and feel backlash as lost motion that shows up in encoder ticks when the robot reverses.

## Prerequisites

You can measure track width and rolling radius (Lesson 01) and you know a set screw must sit on a D-flat (Lesson 02). Tooth counts are integers. A calculator for one division is enough.

## Why this matters for Capstone A and the ROS path

The encoder in Chapter 04 counts the motor shaft, or sometimes a shaft partway down the gearbox. The wheel that touches the floor has been slowed by the ratio $$i$$. `diff_drive_controller` turns ticks into meters only after that ratio, and the rolling radius, are both right. Swap which gear you call the input and you invert $$i$$. Distances in odometry are then wrong by $$i^2$$: a true ratio of 3 that you store as $$1/3$$ stretches or shrinks travel by a factor of 9. The circle you saw from a bad track width in Lesson 01 has a cousin here, a robot whose map scale is simply the wrong number. Write $$i$$ next to $$b$$ and $$r$$ in `lab-notes.md`.

## Meshes, worms, planetaries, and the dead zone

For a pair of spur gears the ratio is

$$
i = \frac{N_{\text{out}}}{N_{\text{in}}} = \frac{\omega_{\text{in}}}{\omega_{\text{out}}}.
$$

$$N$$ is a tooth count. Torque at the output rises as speed falls, minus friction in the mesh and in the bearings. A 12-tooth pinion driving a 36-tooth gear has $$i = 36/12 = 3$$. Three turns of the motor give one turn of the wheel. The wheel torque is about three times the pinion torque, and then a bit less, because teeth rub.

Each external mesh reverses direction. The wheel gear turns opposite the pinion. A second mesh, pinion into an idler into the output, reverses twice, so the output turns the same way as the input. A simple idler changes direction and leaves the ratio alone, as long as it is one gear, not two gears locked together with different tooth counts. Compound gears multiply. If you also have the gearbox ratio and a belt ratio from Lesson 04, the wheel sees the product

$$
i_{\text{wheel}} = i_{\text{gearbox}} \cdot i_{\text{belt}}.
$$

Forgetting either factor is the classic scale error.

A worm mesh is a screw against a worm wheel. Ratios are high, often tens to one in a single stage, which is why a small arm can hold its pose when the motor power drops: many worm pairs cannot be back-driven. They are also inefficient. A lot of the electrical power you budgeted in Chapter 05 becomes heat in the mesh. That is a fair trade on a gripper that must stay shut, and a bad trade on Capstone A’s drive wheels, where you want the battery to become motion. Feel a worm output: you often cannot turn it from the wheel side with your fingers.

A planetary set packs a sun, planets on a carrier, and a ring into the diameter of the ring. In the textbook case the ring is fixed, the sun is the input, and the carrier is the output. The ratio is

$$
i = 1 + \frac{N_{\text{ring}}}{N_{\text{sun}}}.
$$

That formula is the one stage drawn in textbooks. A metal TT gearbox may be a planetary stack or a spur stack, and the number stamped on the motor, often 1:48 or 1:90 or 1:120, already includes every stage the factory put inside. Trust the stamp for that motor. Use the tooth-count formula when you can see the gears, and the stamp when you cannot.

Backlash is the lost motion when torque reverses. Teeth are cut a little thin so they do not bind, and the gap shows up as a pause at the start of a turn. Rock the output shaft with the input held: the wheel moves a few degrees before the motor shaft must move. Encoder ticks recorded across that rock are a bias, a small count that does not correspond to floor motion. You will not remove backlash from a molded TT gearbox. You will measure it, eyeball it in degrees, and avoid control tricks that reverse direction every few milliseconds.

![A compound gear train: tooth counts set the ratio, each external mesh flips direction]({{ site.imgurl }}/generated/gear_train_ratio.png)

The figure shows why you name the input before you divide. Follow torque from the motor to the wheel, multiply each stage’s $$N_{\text{out}}/N_{\text{in}}$$, and count the external meshes if you care which way the wheel rolls. An idler drawn between two gears is a direction fixer. It is not an extra factor unless its two sides differ.

## Worked example

Pinion $$N_{\text{in}} = 12$$, gear $$N_{\text{out}} = 36$$.

$$
i = \frac{36}{12} = 3.
$$

Turn the pinion $$90^\circ$$. The output turns

$$
\theta_{\text{out}} = \frac{90^\circ}{3} = 30^\circ,
$$

in the opposite direction, because there is one external mesh. Three full turns of the motor, $$1080^\circ$$, bring the wheel around once. If you reverse the names and store $$i = 12/36 = 1/3$$, a commanded wheel distance is wrong by

$$
i_{\text{true}}^{2} = 9.
$$

Nine times too long, or nine times too short, depending on which side of the software multiplies. The fix is to point at the pinion, say “input” out loud, and only then divide.

A stamped TT ratio of 1:48 is the number you keep even if a planetary picture in your head suggests $$1 + N_{\text{ring}}/N_{\text{sun}}$$. The stamp already did that arithmetic for the stages you cannot see.

## Lab: count, predict, compare

### Safety

Power stays off. Gear teeth pinch. If you open a gearbox, the grease is slippery and the tiny clips spring off; counting through a clear photo is enough for this lesson. Do not run the motor from a battery while your fingers are in the mesh.

### BOM

| Item | Role |
|------|------|
| A gearbox, a loose gear pair, or a sharp photo of gears you own | Tooth counts |
| Pencil and paper | The ratio and the angle |
| `lab-notes.md` | The number ROS will reuse |

### Steps

1. Name the input gear, the one on the motor side. Name the output gear, the one toward the wheel.
2. Count teeth. On a closed TT motor, read the stamp (1:48 or whatever is printed) and say so.
3. Compute $$i = N_{\text{out}}/N_{\text{in}}$$, or copy the stamp. Note how many external meshes reverse the direction.
4. Predict the output angle for a $$90^\circ$$ input: $$\theta_{\text{out}} = 90^\circ / i$$.
5. If the gears are in your hands, turn the input about a quarter turn against a pointer and compare. Rock the output and estimate backlash in degrees. Eyeball is enough.
6. If you only have a drawing, the paper prediction is the deliverable. Label it “drawing.”

### Expected results

A written $$i$$, a direction note, and a predicted angle. For the 12-and-36 pair, $$i = 3$$ and $$\theta_{\text{out}} = 30^\circ$$ opposite the input. Molded teeth on a real gearbox should land within about 10 percent of the stamp when you check them properly in Lesson 08. Backlash of a few degrees at the wheel is ordinary.

### Faults

| What you see | What it usually means |
|--------------|------------------------|
| Ratio came out below 1 on a gearbox that is supposed to slow the motor | You called the wheel gear the input |
| Direction of the wheel surprises you | You forgot one external mesh, or you counted an idler as a ratio change |
| Output moves a few degrees before the input must move | Backlash; record it, do not “fix” it with glue |
| Stamp says 1:48 and your single-stage formula says 4 | You are looking at one stage of a stack; trust the stamp |

## Mua ở Việt Nam / Where to buy in Vietnam

The gear train for Capstone A is already inside a TT gearmotor. Buy the motor with the ratio printed on it, and with an encoder if you can, so Chapter 04’s ticks have a shaft to count. Loose plastic gears are for the tooth-count lab if your motor is sealed.

| What | Keywords | Rough band (VND) | Notes |
|------|----------|------------------|-------|
| TT gearmotor with encoder | `động cơ giảm tốc TT encoder` | 45.000–120.000 each | Read the stamp: 1:48 is common |
| Plastic gear pack | `bánh răng nhựa robot` | 20.000–60.000 | Useful when the gearbox is sealed and you still want to count teeth |

Search pages:

- [Hshop](https://hshop.vn/search?q=%C4%91%E1%BB%99ng+c%C6%A1+gi%E1%BA%A3m+t%E1%BB%91c+TT)
- [Shopee](https://shopee.vn/search?keyword=%C4%91%E1%BB%99ng%20c%C6%A1%20gi%E1%BA%A3m%20t%E1%BB%91c%20TT%20encoder)
- [Lazada](https://www.lazada.vn/catalog/?q=%C4%91%E1%BB%99ng%20c%C6%A1%20TT%20encoder)
- [Thế Giới IC](https://www.thegioiic.com/search?q=%C4%91%E1%BB%99ng%20c%C6%A1%20gi%E1%BA%A3m%20t%E1%BB%91c)

Prices move. Match the shaft to the wheel you bought in Lesson 01 before you pay.

## Exercises

1. A 15-tooth pinion drives a 60-tooth gear. Find $$i$$, the output angle for one motor revolution, and the direction relative to the motor.
2. That pair is followed by a simple 20-tooth idler and then the 60-tooth gear, so the pinion meshes only with the idler. What is $$i$$ now, and which way does the output turn relative to the pinion?
3. A fixed-ring planetary stage has $$N_{\text{sun}} = 12$$ and $$N_{\text{ring}} = 36$$. Compute the textbook $$i$$. Your TT motor is stamped 1:48. Which number goes into `lab-notes.md` for that motor?
4. You stored $$i = 1/4$$ for a gearbox whose true ratio is 4. By what factor are odometry distances wrong?
5. You hold the motor shaft and the wheel still rocks about $$8^\circ$$. What is that motion called, and what does it do to a tick count taken while the robot starts a turn?

### Answer guidance

1. $$i = 60/15 = 4$$. One motor revolution gives $$360^\circ/4 = 90^\circ$$ at the output, opposite the motor, one external mesh. 2. A simple idler leaves $$i = 4$$ and adds a second reversal, so the output turns the same way as the pinion. 3. Textbook stage: $$i = 1 + 36/12 = 4$$. For the stamped motor, write 48. The stamp includes the whole stack. 4. By $$i^2 = 16$$. 5. Backlash. Those degrees can show up as ticks, or as a pause before ticks move the wheel, so the start of the turn is biased. Record the angle; do not glue the mesh.

## Further reading

- [SDP-SI, Elements of Metric Gear Technology](https://www.sdp-si.com/resources/elements-of-metric-gear-technology/index.php) — tooth geometry, ratio, and backlash from a gear catalog that teaches while it sells.
- [Gear ratio](https://en.wikipedia.org/wiki/Gear_ratio) — the $$N_{\text{out}}/N_{\text{in}}$$ definition and compound trains.
- [Worm drive](https://en.wikipedia.org/wiki/Worm_drive) — high ratio, efficiency, and why many worms refuse to be back-driven.
