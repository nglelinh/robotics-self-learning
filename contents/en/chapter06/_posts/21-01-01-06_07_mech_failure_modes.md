---
layout: post
title: "Mechanical failure modes and strain relief"
chapter: "06"
order: 7
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter06
lesson_type: required
draft: false
---

Estimated time: **60–80 minutes**, including a power-off tug test and one strain-relief fix with a before-and-after photo.

## Learning objectives

By the end of this lesson you can name the failure when a wheel clicks while the encoder still counts, when a plastic horn strips, when a solder joint breaks after the chassis flexes, and when a rubbing wheel smells like a stall. You can add strain relief so the joint sees no bend, leave a service loop, and write two failure modes you will check on Capstone day before you call the robot ready.

## Prerequisites

Lessons 01 through 06: $$b$$ and $$r$$, set screws on D-flats, gear ratio, caster trail, and a chassis material that can crack. Chapter 05 is where stall current became a number on your motor. This lab never applies that current. Power stays off.

## Why this matters for Capstone A and the ROS path

ROS will plot a smooth odometry trail from encoder ticks and from the $$i$$, $$b$$, and $$r$$ in your notes. Several mechanical failures leave those ticks perfect and the floor path wrong. A set screw off the flat, a stripped hub, a wheel that rubs, and a caster that lifts all look, on a topic monitor, like a tuning problem. They are hand problems. You fix them with the battery disconnected, then you earn the right to tune. Strain relief is the one that shows up an hour into a demo: the joint flexed every bump, the copper fatigued, and `cmd_vel` still publishes into a motor that is electrically gone.

## The failures you can find with your hands

Set screw off the D-flat. The hub clicks, the wheel pauses, the motor and its encoder keep turning. The robot barely moves for the current you hear. Odometry adds $$r \Delta\theta$$ as if the wheel had matched the motor. That is the classic odometry lie. Lesson 02 already seated the screw. This lesson is the re-check after transport, because a screw on the crown loosens.

Horn or hub stripped in plastic. Servo horns and cheap wheel hubs cut their own teeth in soft plastic. Once the teeth are gone, the screw still feels tight and the output just rounds out the hole. Replace the horn or the hub. Glue over stripped teeth is a one-demo fiction.

Wire fatigue at the solder joint. The chassis flexes, the joint is the stiff point, and the strand breaks inside the insulation a few millimeters from the shiny solder. The cable looks fine. Strain relief moves the bend away from that point: a zip tie, or a blob of hot glue, anchoring the wire to the plate so the solder sees no motion. Ahead of the anchor, leave a service loop, a deliberate slack curve. A wire pulled tight between a moving wheel pod and the controller has no loop to give, so the joint pays the bend. Do this on motor leads and on encoder leads. An encoder wire that fatigues looks like a dead sensor in Chapter 04’s firmware.

Wheel rubbing the chassis. The tread kisses the plate or a screw head. Speed falls, current rises toward the stall value from Chapter 05, and after a few seconds the motor smells hot. You can feel the rub with the battery out: turn the wheel by hand and listen for a scrape once per revolution. Space the wheel, or file the offender, before you call it a driver problem.

Caster shimmy at speed. The nose oscillates. Trail is reversed or too short, or the center of mass from Lesson 01 barely loads the caster, so the patch cannot settle. Fix trail and loading. A software damper will not invent trail.

Battery sliding. A loose pack shifts the center of mass, the support triangle is suddenly empty under that mass, and the caster tips up. Then one drive wheel unloads and the robot yaws. A printed strap or a zip-tied pocket, from the material plan in Lesson 06, keeps the pack where you measured $$b$$.

![The chassis regions these failures live in: wheels, axle line, caster, and the wires along the plate]({{ site.imgurl }}/generated/chassis_measures.png)

Use the figure as a map. Touch each region during the lab: both hubs, both wheel gaps, the caster fork, the battery footprint, and every wire that leaves a solder joint.

## Worked example

The encoder reports one full motor revolution at the wheel shaft after the ratio, and the set screw slips that whole revolution. With $$r = 31.2$$ mm,

$$
s_{\text{phantom}} = 2\pi r = 2\pi \times 31.2 \approx 196\ \text{mm}.
$$

The map gains about 20 cm the tile never gave. Two such slips per meter of commanded travel is a 40 cm scale error that no covariance setting will honestly cover. The repair is mechanical: flat under the screw, tug the wheel, photograph it.

A rubbing wheel is the thermal cousin. If the free-rolling motor in Chapter 05 drew a small no-load current and a rub pushes the operating point toward stall, the heat in the winding follows that current. You do not need a new number today. You need the scrape gone before voltage returns.

## Lab: tug test and one relief

### Safety

Battery disconnected, driver unplugged, USB unplugged if the board is on the robot. The tug test is a hand test. Hot glue is the only heat: keep the nozzle off insulation you care about, and off your fingers. Do not test strain relief by powering the motor and grabbing the wheel.

### BOM

| Item | Role |
|------|------|
| The chassis, or a motor lead on the bench if the plate is late | The joints |
| Zip ties, or a hot-glue stick and gun | One strain relief |
| Phone | Before and after |
| `lab-notes.md` | Two Capstone-day checks |

### Steps

1. With power off, tug every connector along its housing, not by the wire. A connector that creeps out gets reseated and, if the housing allows, a drop of glue on the housing only.
2. Flex each wire at the solder joint. If the joint bends, the relief is missing.
3. Photograph the worst joint. Add a zip tie or a glue anchor so the bend starts at least a centimeter away from the solder. Leave a service loop. Photograph again.
4. Twist each wheel. Confirm the set screw holds and the tread does not scrape.
5. Try to slide the battery. If it moves, note the strap you still owe.
6. Write two failure modes you will check on Capstone day, in the order you will check them, before anyone publishes `cmd_vel`.

### Expected results

A before photo and an after photo of one relieved joint, and two written checks. A good pair is: set screw on the flat, and no scrape when the wheel turns by hand. The wire’s solder joint stays still while you wag the service loop.

### Faults

| What you see | What it usually means |
|--------------|------------------------|
| Wheel clicks, shaft does not | Set screw off the flat, or a stripped hub |
| Strand broken next to a perfect-looking joint | Fatigue; add relief on the replacement joint |
| Scrape once per turn, motor smell in your memory of Chapter 05 | Wheel rub |
| Caster slaps side to side | Trail or center of mass |
| Battery shifts when you tilt the plate | Strap missing; caster will unload on the first accel |

## Mua ở Việt Nam / Where to buy in Vietnam

You need a bag of zip ties and a hot-glue stick more than a new motor. Buy a spare hub only if the one you have is already rounded out.

| What | Keywords | Rough band (VND) | Notes |
|------|----------|------------------|-------|
| Zip ties | `dây rút nhựa` | 10.000–30.000 | Strain relief and a temporary battery strap |
| Hot glue | `keo nến` | 15.000–40.000 | Anchor the wire, keep glue off the contacts |
| Spare TT wheel | `bánh xe cao su 65mm` | 15.000–45.000 | If the hub is stripped |

Search pages:

- [Shopee: dây rút](https://shopee.vn/search?keyword=d%C3%A2y%20r%C3%BAt%20nh%E1%BB%B1a)
- [Lazada: keo nến](https://www.lazada.vn/catalog/?q=keo%20n%E1%BA%BFn)
- [Hshop: bánh xe](https://hshop.vn/search?q=b%C3%A1nh+xe+cao+su)
- [Thế Giới IC](https://www.thegioiic.com/search?q=d%C3%A2y%20%C4%91i%E1%BB%87n)

Prices move. A connector that fell off is a Chapter 01 soldering job, not a software issue.

## Exercises

1. The robot creeps forward on the floor while the encoder count races. Name the failure and the hand check.
2. A servo horn’s plastic teeth are rounded. The screw is tight. What do you replace, and why is glue a weak plan?
3. Motor leads are soldered and pulled straight to the driver with no slack. What do you add, and what must the solder joint feel when you shake the wire?
4. Current is high and the speed is low, with a hot smell. The set screw holds. What mechanical interference do you look for?
5. Write your two Capstone-day checks as full sentences a teammate can perform with the battery still disconnected.

### Answer guidance

1. The wheel is slipping on the shaft: set screw off the flat or a stripped hub. Twist the wheel by hand with power off; it should not click. 2. Replace the horn. Glue on rounded teeth lets the next stall finish the hole. 3. A zip tie or hot-glue anchor plus a service loop. The solder joint should stay still. 4. The wheel rubbing the chassis or a screw head. Turn it by hand and remove the scrape. 5. Any two from this lesson, performed power-off: screw on the flat, no scrape, caster trails and is loaded, battery does not slide, each solder joint has relief. The sentences should say what “pass” looks like.

## Further reading

- [Adafruit, wires and connectors](https://learn.adafruit.com/wires-and-connectors/wire) — wire, joints, and why the strand fails next to the solder.
- [SparkFun connector basics](https://learn.sparkfun.com/tutorials/connector-basics/all) — housings you tug by the shell, not by the conductor.
- [RepRap print troubleshooting](https://reprap.org/wiki/Print_Troubleshooting) — stripped plastic hubs and layer cracks, if the failed part was printed.
