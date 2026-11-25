---
layout: post
title: "Linkages, cams, belts, and rack-and-pinion"
chapter: "06"
order: 4
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter06
lesson_type: required
draft: false
---

Estimated time: **80–100 minutes**, including a cardboard four-bar or a tooth count on a GT2 pulley if you have one.

Wheels are not the only way robots move parts through space. Open a 3D printer, a robotic gripper, or a walking mechanism and you will immediately meet four-bar linkages, synchronous timing belts, rack-and-pinion rails, and cam followers—each turning a rotary motor into a precisely shaped path without heavy, expensive gearboxes.

## Learning objectives

By the end of this lesson you can test a four-bar against Grashof’s condition and recognize a crank-rocker, compute a toothed-belt ratio from pulley teeth, and turn a pinion pitch diameter into rack travel per revolution. You can describe a cam rise and a dwell, and you can write down the extra encoder-to-wheel ratio a belt would insert before ROS ever sees the joint.

## Prerequisites

You can form a gear ratio $$i = N_{\text{out}}/N_{\text{in}}$$ (Lesson 03) and you know track width $$b$$ from Lesson 01. Cardboard, four brads, and a ruler are enough hardware. A GT2 pulley is optional.


## Key ideas: Planar Mechanisms, Mobility Analysis, and Synchronous Transmission

Designing non-wheel mechanisms rests on three foundational pillars of kinematics of machinery:

- **Planar Mobility (Grübler–Kutzbach Criterion):** A planar linkage with $$N$$ links (including the fixed ground frame), $$J_1$$ one-DOF joints (revolute pins or prismatic sliders), and $$J_2$$ two-DOF joints (cams/gears) has mobility $$M = 3(N-1) - 2J_1 - J_2$$. A standard four-bar linkage ($$N=4, J_1=4, J_2=0$$) has $$M = 3(3) - 8 = 1$$: a single motor uniquely determines the entire mechanism's pose.
- **Grashof's Law for Four-Bar Linkages:** Ordering the four link lengths from shortest $$s$$ to longest $$l$$ with intermediates $$p, q$$, at least one link can make a full $$360^\circ$$ rotation if and only if $$s + l \le p + q$$. Violating this turns a crank-rocker into a double-rocker that jams if driven by a continuous-rotation motor.
- **Synchronous Belts & Rack-and-Pinion Geometry:** Toothed timing belts (e.g., GT2 with pitch $$p = 2\ \text{mm}$$) eliminate slip by meshing pulley teeth with belt teeth, yielding exact linear travel $$\Delta x = N_{\text{teeth}} \cdot p$$ per revolution—the exact same kinematic relation as a rack-and-pinion.
## Why this matters for Capstone A and the ROS path

Capstone A’s drive is two geared wheels, not a linkage. The mechanisms in this lesson still decide whether you understand the joints you will describe later. In ROS a joint is a name, a type, and a pair of limits. A four-bar that can only rock must be given those limits or the controller will command a pose the cardboard already proved impossible. A GT2 belt between a motor and a wheel multiplies the gearbox ratio from Lesson 03. Forget the belt and the same tick count means the wrong wheel angle, so odometry scale drifts exactly as it did when $$i$$ was inverted. Cams show up in limit hardware and in some grippers. You do not need a cam to finish Capstone A. You do need the habit of writing every ratio between encoder and floor.

## Four bars, toothed belts, racks, and cams

A four-bar is four rigid links pinned in a loop. Call the shortest length $$s$$, the longest $$l$$, and the other two $$p$$ and $$q$$. Grashof’s condition for at least one link to be able to turn a full revolution relative to the others is

$$
s + l < p + q
$$

in the everyday case you want on the bench. Textbooks write $$\le$$. Equality is the change-point linkage: it can fold flat and jam, so treat equality as a design you measure twice before you depend on it. When the inequality holds and the shortest link is next to the grounded link, you have a crank-rocker. The short link spins; the opposite link rocks. A windshield wiper is that motion. If $$s + l$$ exceeds $$p + q$$, no link can spin all the way. The mechanism rocks, and a motor commanded through a full turn will stall against the pin.

![Four-bar: the crank spins, the rocker swings, the coupler connects them]({{ site.imgurl }}/generated/four_bar_linkage.png)

Read the figure as a loop. The ground link is the one screwed to the chassis. The crank is the link you would put on a motor. The rocker is the link that waves. The coupler is the floating link that joins them. Changing which link you bolt down changes the motion, even when the four lengths stay the same.

A toothed belt, GT2 on these robots, carries the ratio in the pulley teeth:

$$
i = \frac{N_{\text{driven}}}{N_{\text{driver}}}.
$$

There is no slip while the belt is tensioned and the teeth stay engaged. Direction reverses once, the same as one external gear mesh, unless an idler pulley flips it back. The belt length fixes the center distance. You do not “adjust the ratio” by sliding the motors apart. A belt that is too tight eats the sleeve bearings you decided to leave alone in Lesson 02. A belt that is loose skips a tooth under torque. The skip looks like backlash: a dead zone, then a jump, and the encoder never saw the jump because the motor pulley did move. Pluck the belt. A taut low note is the target. A ringing high note is too tight. A flop is too loose.

![GT2 belt and pulleys: tooth counts set the ratio, tension sets whether the teeth stay engaged]({{ site.imgurl }}/generated/belt_pulley.png)

Rack and pinion turn rotation into a straight line. For one revolution of the pinion, rack travel is the pitch circumference,

$$
x = \pi d,
$$

where $$d$$ is the pitch diameter of the pinion, the diameter where the teeth effectively roll. A linear slide on a small arm, or a scanner carriage, is this device. Capstone A does not need one. The arithmetic is the same arithmetic as rolling radius: path length along the pitch circle.

A cam is a shaped rotor against a follower. A rise lifts the follower. A dwell holds it still while the cam keeps turning. Robots meet cams in mechanical limiters and in a few grippers that must pause closed. The dwell is a hard motion limit. In a URDF you would express that pause as a joint limit or as a mechanism that is simply not a free joint. You will not design a cam for Capstone A.

Whatever you add between the encoder and the tire, write the ratio. Gearbox 48, belt 2, wheel sees $$i = 96$$. That product is what `diff_drive_controller` must use. A joint in ROS is not a place to hide a forgotten pulley.

## Worked example

Grashof first. Lengths $$s = 30$$ mm, $$p = 55$$ mm, $$q = 70$$ mm, $$l = 90$$ mm.

$$
s + l = 120\ \text{mm}, \qquad p + q = 125\ \text{mm}.
$$

$$120 < 125$$, so at least one link can revolve fully. Ground a 70 mm side and drive the 30 mm crank, and the opposite link rocks: a wiper. Change the long link to 110 mm and $$s + l = 140$$ while $$p + q = 125$$. The inequality fails. The cardboard will bind before a full turn. That bind is a joint limit, felt in your fingers.

Rack next. A pinion with pitch diameter 12 mm moves the rack, per turn,

$$
x = \pi \times 12 \approx 37.7\ \text{mm}.
$$

Half a turn is about 18.8 mm. If your drawing’s pinion is the outside diameter and the pitch diameter is smaller, the travel shrinks with it. Use the pitch diameter, and say which diameter you measured.

Belt, for the notes: a 20-tooth motor pulley and a 60-tooth wheel pulley give $$i = 3$$, same structure as the 12-into-36 gear pair. Three motor turns, one wheel turn, plus the gearbox that sits in front of the motor pulley.

### Explanation: Hand-Checking Grashof's Condition and GT2 Belt Resolution

Before cutting brackets or ordering pulleys, verify both mechanism feasibility and linear resolution with five lines of arithmetic:

1. **Test a four-bar gripper linkage with Grashof's law:** Suppose ground $$L_1 = 60\ \text{mm}$$, input crank $$L_2 = 20\ \text{mm}$$, coupler $$L_3 = 55\ \text{mm}$$, and output rocker $$L_4 = 45\ \text{mm}$$.
   - Shortest $$s = 20$$, longest $$l = 60$$, remaining $$p = 45,\ q = 55$$.
   - Compare sums: $$s + l = 20 + 60 = 80 \le p + q = 45 + 55 = 100$$.
   - Because $$s + l < p + q$$ and the shortest link is the input crank, it is a valid **crank-rocker**: the motor can spin continuously $$360^\circ$$ without ever locking up.
2. **Compute GT2 timing-belt linear travel and stepper resolution:** Suppose a 20-tooth GT2 pulley (pitch $$p = 2\ \text{mm}$$) is mounted on a 200-step/rev motor running at $$16\times$$ microstepping ($$3200\ \text{microsteps/rev}$$):
   - Linear travel per full revolution: $$\Delta x_{\text{rev}} = 20 \times 2\ \text{mm} = 40\ \text{mm/rev}$$.
   - Theoretical step resolution: $$\delta x = \frac{40\ \text{mm}}{3200} = 0.0125\ \text{mm/microstep}$$ ($$12.5\ \mu\text{m}$$).
   - If the motor delivers $$\tau = 0.40\ \text{N}\cdot\text{m}$$ on pitch radius $$r_p = \frac{40}{2\pi} \approx 6.37\ \text{mm}$$, peak belt tension force is $$F = \tau / r_p = 0.40 / 0.00637 \approx 62.8\ \text{N}$$.

## Lab: cardboard, or a pulley, or a sketch

### Safety

Brads and thumbtacks are sharp. Keep them on the cardboard, not in a pocket. If you tension a real GT2 belt, power stays off and you keep fingers out of the pulleys. A too-tight belt can fling a loose set screw.

### BOM

| Item | Role |
|------|------|
| Cardboard, four brads or pins, ruler | Four-bar |
| Or one GT2 pulley pair and belt | Tooth count |
| Pencil | The non-Grashof sketch and the rack number |
| `lab-notes.md` | Lengths, $$i$$, or rack travel |

### Steps

1. Cut four strips. Use the worked lengths 30, 55, 70, 90 mm between hole centers. Pin them in a loop, ground the 70 mm strip to the table, and turn the 30 mm crank. Watch the rocker.
2. Rebuild with a 110 mm longest link, same other lengths as the failing example, and feel the bind. Sketch both and label which one satisfies $$s + l < p + q$$.
3. If you have GT2 hardware, count teeth on the driver and the driven pulley, compute $$i$$, and note whether the belt flops, sings, or plucks. Skip the cardboard if the pulley count is the richer measurement, but still sketch one Grashof and one non-Grashof loop with lengths written on the links.
4. If you have neither pulleys nor brads, compute the 12 mm rack example and draw both four-bars to scale. Label the page “drawing.”
5. Write one sentence: encoder-to-wheel ratio for Capstone A, including a belt only if your robot has one.

### Expected results

Two labeled sketches, one that cranks and one that binds, or a GT2 ratio plus those sketches. The rack number 37.7 mm per turn is in the notes if you did the arithmetic. The encoder-to-wheel sentence matches Lesson 03’s stamp unless a belt multiplies it.

### Faults

| What you see | What it usually means |
|--------------|------------------------|
| “Crank” will not spin | $$s + l$$ is larger than $$p + q$$, or the holes are so far from the ends that the real lengths differ from the labels |
| Belt skips under a finger torque | Too loose, or teeth that do not match the belt pitch |
| Bearings get hot and the belt rings | Too tight |
| Wheel angle from ticks is half what the floor shows | A 2:1 belt was left out of $$i$$ |

## Mua ở Việt Nam / Where to buy in Vietnam

Cardboard finishes the lab. Buy GT2 only if your drive or a later axis uses a belt. Capstone A’s two TT wheels usually do not.

| What | Keywords | Rough band (VND) | Notes |
|------|----------|------------------|-------|
| GT2 belt | `dây đai GT2` | 15.000–40.000 | State the length and the width, often 6 mm |
| GT2 pulley | `pulley GT2` | 8.000–30.000 | Tooth count is the ratio; match the shaft bore |
| Rack and pinion set | `thanh răng bánh răng` | 30.000–90.000 | Optional; pitch diameter enters $$x = \pi d$$ |

Search pages:

- [Hshop](https://hshop.vn/search?q=d%C3%A2y+%C4%91ai+GT2)
- [Shopee](https://shopee.vn/search?keyword=d%C3%A2y%20%C4%91ai%20GT2)
- [Lazada](https://www.lazada.vn/catalog/?q=d%C3%A2y%20%C4%91ai%20GT2)
- [Thế Giới IC](https://www.thegioiic.com/search?q=GT2)

Prices move. A pulley listing that hides the tooth count is not yet a ratio.

## Exercises

1. Links 25 mm, 40 mm, 45 mm, and 60 mm. Does $$s + l < p + q$$ hold? If you ground a 45 mm link and drive the 25 mm link, what motion do you expect?
2. Links 40 mm, 50 mm, 55 mm, and 120 mm. Does a full crank exist?
3. Motor pulley 16 teeth, wheel pulley 48 teeth, gearbox stamped 1:30 in front of the motor pulley. What is $$i$$ from motor shaft to wheel?
4. Pinion pitch diameter 20 mm. How far does the rack move in one turn, and in a quarter turn?
5. A cam has a rise over $$90^\circ$$ and a dwell over the next $$180^\circ$$. What does the follower do during the dwell, and do you need this part for Capstone A?

### Answer guidance

1. $$s + l = 85$$, $$p + q = 85$$. Equality is the change-point case; a full relative turn is only the borderline Grashof linkage, and it can fold flat. Treat it as fragile. Driving the short link still wants to be a crank, and you should lengthen a side link slightly if you need a reliable spinner. 2. $$s + l = 160$$, $$p + q = 105$$. No link can fully rotate. 3. Belt $$i = 48/16 = 3$$, times gearbox 30, so $$i = 90$$. 4. $$x = \pi \times 20 \approx 62.8$$ mm per turn, about 15.7 mm per quarter turn. 5. The follower holds still while the cam turns through that dwell. Capstone A does not need a cam.

## Further reading

- [Four-bar linkage](https://en.wikipedia.org/wiki/Four-bar_linkage) — crank-rocker, and what changes when a different link is grounded.
- [Grashof’s law](https://en.wikipedia.org/wiki/Grashof%27s_law) — the $$s + l$$ test, including the equality case.
- [Timing belt (toothed belt)](https://en.wikipedia.org/wiki/Timing_belt_(camshaft)) — tooth engagement and why a slack belt skips. The page is written about engines; the mesh idea is the one on your GT2 pulleys.
