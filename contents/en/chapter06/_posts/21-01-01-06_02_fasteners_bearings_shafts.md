---
layout: post
title: "Fasteners, bearings, shafts, and couplings"
chapter: "06"
order: 2
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter06
lesson_type: required
draft: false
---

Estimated time: **70–90 minutes**, including sorting a small screw kit and photographing a nyloc next to a plain nut.

## Learning objectives

By the end of this lesson you can separate M2, M3, and M4 screws by measuring the thread diameter, choose a nyloc nut where a plain nut would walk off under vibration, and seat a set screw on the flat of a D-shaft. You can decide when a 608 ball bearing belongs on a printed idler and when the sleeve bearing already inside a TT gearbox should stay there, and you can match a coupler to the shaft diameters you actually bought.

## Prerequisites

You can use a caliper or, failing that, a known nut as a gauge (Chapter 01 measuring habits). You know the chassis from Lesson 01 has wheels on motor shafts, and that those shafts will be asked to report honest rotation to an encoder later.

## Why this matters for Capstone A and the ROS path

Capstone A’s odometry believes the wheel angle and the motor angle are the same angle, scaled by the gear ratio you will write down in Lesson 03. A set screw that misses the flat lets the wheel click while the encoder keeps a perfect count of the motor. The ROS pose then walks across the map while the robot hesitates on the tile. Fasteners are the reason that lie starts or never starts. A nyloc that stays put, a coupler that matches  the shaft, and a bearing that fits the job are the mechanical half of a trustworthy `odom` topic.

## Screws, nuts, and the one shaft flat that matters

Metric screws are named by the outer diameter of the thread. M3 means about 3 mm across the crests, and it is the default on this robot: motor mounts, sensor brackets, and the plate itself. Standard M3 coarse pitch is 0.5 mm, so one full turn of the screw advances it half a millimeter into the nut. M2 is the small screw on some sensor boards and is easy to round off. M4 is stouter and often too large for a TT-motor slot. The usual shopping error is a bag labeled “M3” that is actually a mix.

A plain nut is a hexagon with a clean thread. Vibration from a gearbox walks it off the screw over an afternoon of driving. A nyloc nut has a nylon insert at one end that grips the thread. Finger-start it until the insert bites, then finish with a driver. That grip is the plan for Capstone A. Medium (blue) threadlocker is a liquid backup for metal-on-metal threads you may never open. It is a poor plan for PLA: the solvent can crack the plastic. On a printed bracket, use a nyloc, or melt in a brass threaded insert and put the nyloc on the metal thread the insert gives you.

The motor shaft on a hobby gearmotor is usually a D-shaft: a cylinder with one flat. The wheel hub or the coupler carries a set screw, a small screw that bites the shaft from the side. That screw must land on the flat. On the round part it raises a burr, the hub buzzes under torque, and the encoder, which is watching the motor, still counts. Odometry then reports motion the floor did not see. After you tighten the set screw, try to twist the wheel on the shaft with your fingers. A seated screw on the flat holds. A screw on the crown slips with a click.

![A ball bearing: inner race, balls, outer race]({{ site.imgurl }}/wikimedia/Ball_bearing.jpg)

A ball bearing, like the one in the photo, has an inner race, a ring of balls, and an outer race. The common 608 is 8 mm bore, 22 mm outside diameter, and 7 mm wide, the skate bearing. It is a good printed idler for a belt, on an 8 mm shoulder or a printed axle that really is 8 mm. It is oversized for a yellow TT motor, whose shaft and whose gearbox were never designed around a 608. Cheap TT gearboxes ride on sleeve bearings, plain bushings. They are noisy and they are normal. Opening the gearbox mid-Capstone to “upgrade” them costs you the ratio stamp and a weekend. Leave them until the robot drives.

Shaft meets shaft through a coupling when the motor and the load do not share one piece of steel. A rigid coupler demands that the two shafts be collinear. A little angular error becomes a cyclic load, a hot bearing, and a wheel that wobbles. A jaw coupler, with an elastomer spider between two hubs, forgives a small misalignment and is the kinder choice on a student plate. The diameter engraved on the coupler has to match the shaft: 3 mm, 4 mm, and 6 mm are all common on metal gearmotors, and they are not interchangeable. A 6 mm coupler on a 4 mm shaft clamps down to an oval and still slips. Measure the shaft with a caliper before you order. TT wheels usually include a D-hole matched to that motor, so you often need no coupler at all on Capstone A’s drive wheels.

## Worked example

An M3 screw has pitch 0.5 mm. Four full turns, after the nut is started, take up

$$
4 \times 0.5 = 2.0\ \text{mm}
$$

of thread. That is the difference between a snug motor mount and a screw that has bottomed out and started to crack an acrylic hole. Stop when the parts are seated, then about a quarter turn. On the shaft side, suppose the set screw misses the flat and the wheel slips one full revolution while the encoder counts that revolution as motion. With the rolling radius $$r = 31.2$$ mm from Lesson 01, the odometry invents a distance

$$
s = 2\pi r = 2\pi \times 31.2 \approx 196\ \text{mm}
$$

that the robot never traveled. One missed flat, one phantom 20 cm, every time the torque reverses and the hub clicks.

## Lab: sort the screws and find the flat

### Safety

Power stays off. Set screws are small and like to launch off a hex key; point the hub away from your eyes. Threadlocker is optional and stays capped; do not sniff it, and do not drip it onto plastic “to be sure.”

### BOM

| Item | Role |
|------|------|
| Mixed M2/M3/M4 screws and nuts, even a cheap assortment | The sort |
| One nyloc and one plain nut | The comparison |
| Caliper, or one nut of each size you trust | The gauge |
| A D-shaft hub or a photo of one you own | The flat |
| Phone | The photo for `lab-notes.md` |

### Steps

1. Measure the crest diameter of each screw, or try it in a known nut. M2 will not start in an M3 nut. M4 will not start in an M3 nut. M3 runs in smoothly.
2. Separate the pile into three cups. Write the count of M3 screws you actually have; Capstone A eats them.
3. Photograph a nyloc beside a plain nut. On the photo, mark the nylon ring.
4. If you have a wheeled hub, loosen the set screw, seat the D-shaft so the flat faces the screw, and tighten. Twist the wheel by hand. Record whether it holds.
5. If you have a 608, measure 8 × 22 × 7 mm and write one sentence on where it may live (a printed idler) and where it does not (inside the TT gearbox).

### Expected results

Three labeled groups, a photo of nyloc versus plain nut, and a sentence in `lab-notes.md` that names the shaft diameter you will shop for. A seated set screw holds the wheel against finger torque.

### Faults

| What you see | What it usually means |
|--------------|------------------------|
| Screw almost starts, then jams | Wrong size, or a crossed thread; back it out |
| Nut spins on forever under vibration | Plain nut, and no nyloc on that joint |
| Wheel buzzes, encoder still counts | Set screw is on the round of the D-shaft |
| Coupler clamps hard and still slips | Bore is a size larger than the shaft |
| Plastic boss cracks the day after threadlocker | The locker was the plan for PLA; switch to a nyloc or an insert |

## Mua ở Việt Nam / Where to buy in Vietnam

An M3 assortment plus a small bag of M3 nylocs covers Capstone A. Buy a 608 only when you are printing an idler. Buy a jaw coupler only when two shafts must meet, and only after the caliper reading.

| What | Keywords | Rough band (VND) | Notes |
|------|----------|------------------|-------|
| M3 screw kit | `ốc M3` | 25.000–70.000 | Assortment of lengths; check for a hex key |
| Nyloc nuts | `đai ốc nyloc M3` | 15.000–40.000 a bag | Nylon insert visible at one end |
| 608 bearing | `bạc đạn 608` | 5.000–20.000 each | 8×22×7 mm, for an idler |
| Jaw coupler | `khớp nối trục 4mm` | 15.000–45.000 | Match the measured shaft, 3 mm or 4 mm or 6 mm |

Search, and compare two sellers. Prices move.

- [Hshop: ốc M3](https://hshop.vn/search?q=%E1%BB%91c+M3)
- [Shopee: đai ốc nyloc M3](https://shopee.vn/search?keyword=%C4%91ai%20%E1%BB%91c%20nyloc%20M3)
- [Lazada: bạc đạn 608](https://www.lazada.vn/catalog/?q=b%E1%BA%A1c%20%C4%91%E1%BA%A1n%20608)
- [Thế Giới IC: ốc vít](https://www.thegioiic.com/search?q=%E1%BB%91c%20v%C3%ADt)

## Exercises

1. A screw measures 2.9 mm across the crests and advances 0.5 mm per turn. What designation is it, and how far does it advance in six turns?
2. You have a plain nut on a motor mount that you will drive every lab session. What do you replace it with, and why is blue threadlocker the wrong first plan if that mount is PLA?
3. The wheel hub clicks when you twist it, and the encoder count still increases when the motor is powered later with the wheels up. Where is the set screw sitting?
4. Your caliper reads 4.0 mm on a metal gearmotor shaft. Which coupler bore do you order, and what happens with a 6 mm bore?
5. A friend wants to press 608 bearings into a yellow TT gearbox “so it rolls better.” What do you tell them to do with the sleeve bearings during Capstone A?

### Answer guidance

1. M3, because the crest is about 3 mm and the pitch is the standard 0.5 mm. Six turns advance $$6 \times 0.5 = 3.0$$ mm. 2. A nyloc. Blue threadlocker can crack PLA; an insert plus a nyloc keeps the chemistry on metal. 3. On the round of the D-shaft, not on the flat. Loosen, rotate the flat under the screw, retighten, and twist-test. 4. A 4 mm bore. A 6 mm bore clamps to an oval and slips under torque. 5. Leave the sleeve bearings in place. A 608 is 8×22×7 mm and belongs on a printed idler, not inside that gearbox.

## Further reading

- [McMaster-Carr catalog](https://www.mcmaster.com/) — look up screw, nyloc, shaft collar, and jaw coupling by name so you learn the dimensions. Use it as a picture dictionary. Ordering from overseas is outside this course.
- [RepRap threaded inserts](https://reprap.org/wiki/Threaded_insert) — heat-set brass inserts for printed plastic, which is the durable way to put an M3 thread in PLA.
- [Ball bearing (overview)](https://en.wikipedia.org/wiki/Ball_bearing) — races and the 608 size in context.
