---
layout: post
title: "Differential-drive chassis anatomy"
chapter: "06"
order: 1
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter06
lesson_type: required
draft: false
---

Estimated time: **70–90 minutes**, including a ruler measurement on a real 2WD chassis or on a careful scale drawing if the kit has not arrived.

## Learning objectives

By the end of this lesson you can point to the two lengths a differential-drive robot actually uses: track width $$b$$, taken between the tire contact centers, and rolling radius $$r$$, taken from a one-revolution roll test. You can turn a pair of wheel speeds into body speed and yaw rate, place the battery so the caster stays on the floor, and write $$b$$ and $$r$$ in millimeters so Chapter 07 assembly and the later ROS `diff_drive_controller` inherit the same geometry.

## Prerequisites

You can read a millimeter ruler. You know a DC gearmotor turns a wheel (Chapter 05) and that encoder ticks will later stand in for wheel rotation (Chapter 04). You do not need ROS installed, and you do not need the chassis on the bench if you can draw it to scale.

## Why this matters for Capstone A and the ROS path

Capstone A is this chassis: two driven wheels on one axis, plus a caster or a skid that holds the third corner down. Chapter 08 expands the kinematics. The controller you meet on the ROS path, `diff_drive_controller`, converts `cmd_vel` into two wheel commands and converts encoder ticks back into odometry using the same $$b$$ and $$r$$ you measure here. The URDF in Chapter 09–10 places the wheel links with those lengths. A wrong $$b$$ shows up as a circle when you command a straight line, because the controller spends the whole motion “correcting” a turn that the geometry invented. Measure once, write the millimeters in `lab-notes.md`, and refuse to round them into “about 15 cm” later.

## Two wheels, one caster, two lengths

Look at the plate from above. The left motor and the right motor face outward, and the tires sit on a common axle line. The robot steers by making those tires travel at different speeds. A third support, a swivel caster or a smooth skid, stops the plate from dragging its nose. Capstone A uses the caster. A skid is acceptable on a tiny indoor plate and noisy on tile.

Track width $$b$$ is the distance between the tire contact centers, the middle of each rubber patch that actually touches the ground. The gap between the motor bodies is a mounting dimension for the plate drawing. Kinematics leaves it unused. If you measure from the outside of one tire to the outside of the other, you have included a tread width. Slide each end of the ruler to the middle of the tread, with the robot loaded the way it will roll, and record millimeters.

Rolling radius $$r$$ is the radius the floor sees after the rubber compresses. The number printed on a wheel bag is a free diameter. Under the battery it shrinks. Mark the tire, roll it exactly one revolution along paper, measure the path length $$s$$, and compute

$$
r = \frac{s}{2\pi}.
$$

A wheel labeled 65 mm that rolls 196 mm in one turn has

$$
r = \frac{196}{2\pi} \approx 31.2\ \text{mm},
$$

while half the label is 32.5 mm. That gap is a few percent of every meter your odometry will claim. Weigh the wheel with something close to its share of the robot, or roll the whole chassis straight if both wheels can turn freely. Repeat for the other tire. The two radii should agree within about a millimeter. A larger split means one tire is seated crooked, and a straight command will already yaw.

The support triangle is the two contact patches plus the caster. The vertical through the center of mass has to land inside that triangle. A battery stood up behind the axle, or a pack hung past the wheels, walks that point out of the triangle. The nose wheelies on acceleration, or the caster, barely loaded, shimmies because its trail never settles. Sit the pack low, between the wheels or a little ahead of the axle, and press the caster mount: it should take a steady share of the weight while both drive wheels stay down.

## Worked example

Use $$b = 0.15$$ m, $$v_l = 0.20$$ m/s, and $$v_r = 0.30$$ m/s. Wheel speeds are linear speeds of the contact patches, positive forward. Body speed and yaw rate are

$$
v = \frac{v_r + v_l}{2} = \frac{0.30 + 0.20}{2} = 0.25\ \text{m/s},
$$

$$
\omega = \frac{v_r - v_l}{b} = \frac{0.30 - 0.20}{0.15} = 0.667\ \text{rad/s}.
$$

In one second the midpoint of the axle travels 25 cm along the heading and the heading changes by $$0.667 \times 180/\pi \approx 38^\circ$$. Positive $$\omega$$ here means the right wheel is faster, so the robot yaws left when left and right match the nose. If the same wheel speeds are paired with a track width of 0.18 m, because someone measured across the motor cans, the reported yaw rate falls to $$0.556$$ rad/s. The controller that trusts 0.18 m will command a wheel-speed difference to cancel a turn the real 0.15 m robot is already making, and the floor path closes into a circle.

![Track width between contact centers, and the roll that gives rolling radius]({{ site.imgurl }}/generated/chassis_measures.png)

![Body speed and yaw rate drawn from the two wheel velocities]({{ site.imgurl }}/generated/diff_drive_kinematics.png)

The first figure is the ruler picture: $$b$$ from tread center to tread center, $$r$$ from the compressed tire. The second figure is the velocity picture behind the two equations. Equal forward arrows give $$\omega = 0$$. Unequal arrows yaw the robot about a point that still lies on the axle line. Chapter 08 names that point and the turning radius. Today you only need $$b$$, $$r$$, $$v$$, and $$\omega$$ written down.

## Lab: measure b and r

### Safety

Power stays off. If a battery is already strapped on, disconnect it before a metal ruler crosses the plate, so a motor lead cannot short. This lab has no spinning shaft under voltage.

### BOM

| Item | Role |
|------|------|
| 2WD chassis, or a scale drawing of the kit you ordered | The object you measure |
| Ruler or caliper, in millimeters | Track width |
| Paper, tape, pen | One-revolution roll for $$r$$ |
| `lab-notes.md` | The numbers Chapter 07 and ROS will copy |

### Steps

1. Sit the chassis on a flat table the way it will roll. Put the battery in its future place if you already have it.
2. Mark the center of each tread. Measure $$b$$ between those marks. Write millimeters, and write beside it the motor-can gap you deliberately left out of the controller.
3. Mark one tire and the paper. Roll exactly one revolution under about that wheel’s share of the weight. Measure $$s$$.
4. Compute $$r = s / (2\pi)$$ and keep one decimal place in millimeters. Repeat for the other wheel.
5. Press at the caster. Note whether it carries weight. If the battery is still in a box, sketch where it must sit so the mass stays inside the support triangle.
6. If the kit has not arrived, do steps 2–5 on a careful scale drawing and title the note “drawing, not hardware.”

### Expected results

A dated pair in `lab-notes.md`, for example $$b = 148$$ mm and $$r = 31.2$$ mm, with the two wheels agreeing on $$r$$ within about 1 mm. The note says whether the numbers came from hardware or from a drawing.

### Faults

| What went wrong | What it does later |
|-----------------|-------------------|
| $$b$$ taken between motor bodies | A straight `cmd_vel` drives a circle |
| $$r$$ copied as half the label diameter | Odometry distance runs long or short on every meter |
| Battery perched behind the axle | Wheelie, or a caster that shimmies |
| Left and right radii differ by several millimeters | A straight command already yaws |

## Mua ở Việt Nam / Where to buy in Vietnam

Buy a finished 2WD acrylic chassis so Capstone A can be built this month. Print small brackets later (Lesson 06). A plate with TT-motor slots and a caster hole is the usual student kit. Rubber wheels and the caster are often separate lines on the same listing.

| What | Keywords | Rough band (VND) | Notes |
|------|----------|------------------|-------|
| 2WD chassis | `khung xe robot 2 bánh` | 80.000–200.000 | Acrylic plate, motor slots, caster hole |
| Rubber wheel | `bánh xe cao su 65mm` | 15.000–45.000 each | The label diameter is the start of the roll test, not $$r$$ |
| Swivel caster | `bánh caster robot` | 12.000–40.000 | A trailing swivel wheel for Capstone A |

Search pages, because shop slugs change and street prices move:

- [Hshop](https://hshop.vn/search?q=khung+xe+robot)
- [Shopee](https://shopee.vn/search?keyword=khung%20xe%20robot%202%20b%C3%A1nh)
- [Lazada](https://www.lazada.vn/catalog/?q=khung%20xe%20robot%202%20b%C3%A1nh)
- [Thế Giới IC](https://www.thegioiic.com/search?q=khung%20xe%20robot)

Check that the motor slots match a TT gearbox and that a caster is included or sold next to the plate.

## Exercises

1. A roll test gives $$s = 200$$ mm. Compute $$r$$ in millimeters to one decimal place.
2. With $$b = 0.16$$ m, $$v_l = 0.25$$ m/s, and $$v_r = 0.25$$ m/s, find $$v$$ and $$\omega$$. What does the robot do?
3. Same $$b$$, with $$v_l = 0.10$$ m/s and $$v_r = 0.30$$ m/s. Find $$v$$ and $$\omega$$.
4. A classmate measured from the outside of the left tire to the outside of the right tire and got 180 mm. Each tread is 20 mm wide. What $$b$$ belongs in the controller?
5. The pack sits on a tower behind the axle and the caster lifts when you push the robot forward. Where do you move the pack, and what path does a straight ROS command draw if you leave the tower in place?

### Answer guidance

1. $$r = 200/(2\pi) \approx 31.8$$ mm. 2. $$v = 0.25$$ m/s and $$\omega = 0$$, so the robot drives straight. 3. $$v = 0.20$$ m/s and $$\omega = (0.30-0.10)/0.16 = 1.25$$ rad/s, a left yaw when the right wheel is the fast one. 4. Each contact center lies half a tread in from the outside face, so subtract one full tread width: $$b = 160$$ mm. 5. Move the pack low and inside the support triangle, a little ahead of the axle if the caster was light. Left on the tower, the caster unloads, heading wanders, and a straight command looks crooked on the floor.

## Further reading

- [diff_drive_controller in ros2_controllers](https://github.com/ros-controls/ros2_controllers/tree/master/diff_drive_controller) — wheel separation and wheel radius are parameters of this package. Jazzy’s controller docs are generated from this tree; the package index also lives under [docs.ros.org/en/jazzy](https://docs.ros.org/en/jazzy/index.html).
- [ROS 1 diff_drive_controller wiki](https://wiki.ros.org/diff_drive_controller) — parameter names in plain language. The page is ROS 1; the geometry it asks for is the geometry ROS 2 still uses.
- [Nav2 odometry setup](https://navigation.ros.org/setup_guides/odom/setup_odom.html) — how a bad odometry source shows up once you leave teleop and ask the robot to navigate.
