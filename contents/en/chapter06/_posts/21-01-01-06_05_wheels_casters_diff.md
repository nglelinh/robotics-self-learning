---
layout: post
title: "Wheels, casters, and diff-drive mechanism diagrams"
chapter: "06"
order: 5
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter06
lesson_type: required
draft: false
---

Estimated time: **70–90 minutes**. If the robot already rolls, ten of those minutes are a hand rotation about the axle midpoint. If it does not, they are a velocity-arrow sketch.

Push a shopping cart forward and its front wheels immediately swing neatly behind their pivots; push it backward and they momentarily shudder sideways before flipping around. That tiny offset between the swivel pin and the tire contact patch—called **caster trail**—is the difference between a mobile robot that glides predictably and one that scrubs sideways and corrupts its own odometry.

## Learning objectives

By the end of this lesson you can draw the wheel-speed arrows for straight motion, a gentle turn, and a spin in place, and you can compute the spin-in-place yaw rate $$\omega = 2 v_r / b$$. You can explain caster trail, why a reversed caster shimmies, and why four fixed wheels waste the stall current you sized in Chapter 05. You can point at the axle midpoint as the pivot and connect `cmd_vel` linear.x and angular.z to the two motors.

## Prerequisites

Lesson 01’s definitions: $$b$$ between contact centers, $$r$$ from a roll test, and

$$
v = \frac{v_r + v_l}{2}, \qquad \omega = \frac{v_r - v_l}{b}.
$$

You know a bad $$b$$ draws a circle on a straight command. Gears (Lesson 03) already set how motor radians become wheel radians.


## Key ideas: Instantaneous Center of Curvature, Caster Trail, and Rolling Constraints

Wheeled mobility rests on three geometric ideas that bridge mechanism diagrams and mobile-robot kinematics:

- **Instantaneous Center of Curvature (ICC):** For any rigid body moving in a plane without lateral tire slip, the wheel axes of all fixed-axis wheels must intersect at a single point called the ICC. For a differential-drive robot, both driven wheels share one axle line, so the ICC can lie anywhere along that axle at signed distance $$R = v/\omega$$ from the chassis midpoint.
- **Caster Trail & Self-Alignment:** A swivel caster offsets its wheel contact patch behind the vertical swivel axis by trail distance $$d_{\text{trail}} > 0$$. Floor friction acting at the contact patch creates a restoring torque $$\tau = F_{\text{lat}} d_{\text{trail}}$$ that aligns the caster wheel with the local velocity vector—just like a weathervane.
- **Wheel Scrub & Skid-Steer Trade-offs:** Whenever two fixed-axis wheels are placed on *parallel, non-collinear* axles (as in a 4WD skid-steer robot), their axes never intersect at a finite ICC during a turn. Turning therefore requires deliberate lateral tire scrub, increasing torque demand and degrading pure wheel-encoder odometry.
## Why this matters for Capstone A and the ROS path

Capstone A is two driven wheels plus one caster. ROS will send `geometry_msgs/Twist` with linear.x as $$v$$ and angular.z as $$\omega$$. `diff_drive_controller` inverts the two equations and commands a left motor and a right motor. A sign error on one motor is a mechanical fact the controller cannot see: both wheels “forward” in software, one wheel backward on the floor, and the path is a circle about the slower side. You will find that sign in Chapter 07 with the wheels in the air, then confirm it on the floor, where the caster and the rubber finally matter. The arrows you draw today are the picture you will debug against.

## Arrows, trail, and the wheel that scrubs

Straight ahead, both contact patches move forward at the same speed. Then $$v_r = v_l$$, so $$v$$ equals that speed and $$\omega = 0$$. The instantaneous center of the motion sits infinitely far to the side: the axle is not rotating about a nearby point.

A gentle left turn keeps both wheels forward and makes the right one faster. $$\omega$$ is positive in the usual robot frame, x ahead and z up, which is a left yaw. The robot rotates about a point on the axle line, outside the left wheel. The caster swivels to follow.

A spin in place is the pure case. Set $$v_l = -v_r$$. Then

$$
v = \frac{v_r + (-v_r)}{2} = 0, \qquad \omega = \frac{v_r - (-v_r)}{b} = \frac{2 v_r}{b}.
$$

The body speed is zero and the pivot is the midpoint of the axle, halfway between the contact centers. Mark that point on the plate. If you rotate the robot by hand on a smooth floor, the mark should stay put while the wheels orbit it. A mark at the caster, or a mark between the motor cans, walks in a circle and tells you the geometric center and the kinematic center were different points.

Caster trail is why the third wheel behaves. On a swivel caster the contact patch sits behind the swivel axis, along the direction of travel. Drag at the patch pulls the wheel into line, the way a shopping-cart wheel settles. Trail is that offset. Mount the caster backwards and the contact patch leads the pivot. The wheel is then unstable and it shimmies, especially as speed rises. A ball caster has essentially no trail: the contact is on the swivel axis. It scuffs instead of aligning, adds friction you did not budget, and still holds the nose up. Capstone A wants a swivel caster with a visible trail, installed so the patch trails.

Skid steering puts a motor on four fixed wheels, or locks the wheels so none can swivel. Any yaw requires the tires to scrub sideways. Scrub is sliding friction, and it asks the motors for current up near the stall value Chapter 05 treated as a thermal event, not as a normal turn. Capstone A spends that current on rolling. Two driven wheels and one trailing caster are the mechanism.

The rubber diameter on the bag is still not the rolling radius. Reuse the paper roll from Lesson 01 whenever you change tires, load, or inflation of a soft tire. A larger right-hand radius on an otherwise straight command is a gentle turn you did not ask for.

![Where to put the ruler: contact centers and compressed radius]({{ site.imgurl }}/generated/chassis_measures.png)

![Equal arrows, unequal arrows, and the spin that parks the pivot on the axle midpoint]({{ site.imgurl }}/generated/diff_drive_kinematics.png)

Use the two figures together. The first keeps $$b$$ and $$r$$ honest. The second is the arrow language: forward, spin, and the mixed case. When you wire motors in Chapter 07, label the wires to match these arrows before you trust a positive PWM to mean “forward.”

## Worked example

Take the Lesson 01 chassis, $$b = 0.15$$ m, and command a spin with $$v_r = 0.20$$ m/s and $$v_l = -0.20$$ m/s.

$$
v = 0, \qquad \omega = \frac{2 \times 0.20}{0.15} = 2.667\ \text{rad/s}.
$$

A full revolution is $$2\pi$$ radians, so the time to spin once is

$$
T = \frac{2\pi}{2.667} \approx 2.36\ \text{s},
$$

provided the wheels really reach 0.20 m/s and do not scrub. With $$r = 31.2$$ mm the wheel angular speed has magnitude

$$
\dot{\theta} = \frac{0.20}{0.0312} \approx 6.41\ \text{rad/s},
$$

opposite signs on the two motors. If one motor lead is flipped, the command $$v = 0.20$$, $$\omega = 0$$ (both software speeds “positive”) becomes $$v_l = 0.20$$ and $$v_r = -0.20$$ on the floor. That is this spin, not a straight line. Wheels-up in Chapter 07: positive command, both tires forward. Floor test: the axle midpoint stays put only when you asked for a spin.

### Explanation: Computing ICC Distance, Wheel Speeds, and Caster Heading

Let us trace the velocity vector of every contact patch on a 2WD robot with track width $$b = 0.16\ \text{m}$$ and a rear swivel caster mounted $$d_c = 0.10\ \text{m}$$ directly behind the axle midpoint.

1. **Locate the ICC:** Command $$v = 0.24\ \text{m/s}$$ and $$\omega = 0.60\ \text{rad/s}$$ (left turn). The ICC lies to the left of the axle midpoint at distance:
   $$R = \frac{v}{\omega} = \frac{0.24}{0.60} = 0.40\ \text{m}.$$
2. **Verify the two driven-wheel speeds from the ICC:**
   - Inner (left) wheel is at radius $$R_L = R - b/2 = 0.40 - 0.08 = 0.32\ \text{m} \implies v_L = \omega R_L = 0.60 \times 0.32 = 0.192\ \text{m/s}$$.
   - Outer (right) wheel is at radius $$R_R = R + b/2 = 0.40 + 0.08 = 0.48\ \text{m} \implies v_R = \omega R_R = 0.60 \times 0.48 = 0.288\ \text{m/s}$$.
   - Check: $$(v_R + v_L)/2 = 0.24\ \text{m/s}$$ and $$(v_R - v_L)/b = 0.096 / 0.16 = 0.60\ \text{rad/s}$$.
3. **Find the steady-state caster swivel angle:** The caster pivot sits at $$(x, y) = (-0.10,\ 0)$$ in the body frame, while the ICC is at $$(0,\ +0.40)$$. The vector from the ICC to the caster pivot is $$(-0.10,\ -0.40)$$, so its perpendicular velocity vector points along $$(+0.40,\ -0.10)$$. The caster therefore swings outward by angle:
   $$\psi = \arctan\!\left(\frac{d_c}{R}\right) = \arctan\!\left(\frac{0.10}{0.40}\right) = \arctan(0.25) \approx 14.0^\circ.$$
   If the caster were fixed straight ahead instead of swiveling, it would scrub sideways at $$14^\circ$$ throughout the entire turn.

## Lab: find the pivot, or draw the arrows

### Safety

If you rotate a built robot by hand, the battery is disconnected so a back-driven motor cannot put voltage on a driver. Fingers stay out of the gears. On a hard floor, spin slowly; a finger under a caster is a pinch.

### BOM

| Item | Role |
|------|------|
| Chassis from Lesson 01, or a scale top-view drawing | The mechanism |
| Tape and a pen | The predicted pivot |
| `lab-notes.md` | Arrow sketch or the hand-test note |

### Steps

1. Mark the midpoint of the segment that joins the two contact centers. That is the predicted spin pivot.
2. If the robot rolls, disconnect the battery. Rotate the chassis slowly in place by hand. Watch the mark. A good $$b$$ measurement shows the mark staying on one spot of floor while both wheels circle it.
3. Note whether the caster trails. Look from the side: the patch should sit behind the swivel pin in the direction you push. If the fork is reversed, say so in the notes and turn it around before Chapter 07.
4. If you have no rolling chassis yet, draw three top views. Forward: equal arrows. Spin: opposite arrows, pivot marked. Gentle left: both arrows forward, right arrow longer. Label $$v$$ and $$\omega$$ on each.
5. Write the sign convention you will use in firmware: positive left wheel and positive right wheel both move the robot forward.

### Expected results

A mark that stays put during a careful hand spin, or three labeled arrow drawings. The notes say which caster orientation you will assemble, trail behind the swivel. The sign sentence is something Chapter 07 can test with the wheels up.

### Faults

| What you see | What it usually means |
|--------------|------------------------|
| The “midpoint” walks in a circle | The mark was between the motor bodies, or one wheel was skidding |
| Caster chatters as soon as you push | Fork reversed, or almost no weight on the caster |
| Ball caster scuffs and yaws the plate | No trail; fit a swivel caster for Capstone A |
| Forward command draws a circle once powered | One motor sign is flipped; confirm wheels-up in Chapter 07 |
| Straight line bends gently with equal commands | The two rolling radii disagree |

## Mua ở Việt Nam / Where to buy in Vietnam

Lesson 01 bought the plate. This lesson is the wheel and the caster, if those lines were missing. A ball caster is a useful spare to feel “no trail” once. The robot you hand in uses a swivel caster.

| What | Keywords | Rough band (VND) | Notes |
|------|----------|------------------|-------|
| Rubber wheel | `bánh xe cao su 65mm` | 15.000–45.000 each | Then roll-test $$r$$ |
| Swivel caster | `bánh caster robot` | 12.000–40.000 | Trail visible behind the pin |
| Ball caster | `bánh đa hướng bi` | 15.000–40.000 | Optional contrast; it scuffs |

Search pages:

- [Hshop](https://hshop.vn/search?q=b%C3%A1nh+xe+cao+su)
- [Shopee](https://shopee.vn/search?keyword=b%C3%A1nh%20xe%20cao%20su%2065mm)
- [Lazada](https://www.lazada.vn/catalog/?q=b%C3%A1nh%20caster%20robot)
- [Thế Giới IC](https://www.thegioiic.com/search?q=b%C3%A1nh%20xe%20robot)

Prices move. Match the hub to the TT D-shaft, or to the coupler bore you measured in Lesson 02.

## Exercises

1. $$b = 0.18$$ m, $$v_r = 0.15$$ m/s, $$v_l = -0.15$$ m/s. Find $$v$$, $$\omega$$, and the time for one full spin.
2. Both wheels at $$+0.22$$ m/s, $$b = 0.15$$ m. Find $$v$$ and $$\omega$$, and where the pivot is.
3. You push the robot and the caster wheel flips around and oscillates. What is wrong with the trail, and what do you change mechanically?
4. A four-fixed-wheel robot turns in place on carpet. Why does the current climb toward stall, and what mechanism does Capstone A use so a turn can roll?
5. linear.x = 0.2 and angular.z = 0 leave the robot circling. You have not changed $$b$$. What single wiring fact do you test with the wheels up?

### Answer guidance

1. $$v = 0$$, $$\omega = 2\times 0.15/0.18 = 1.667$$ rad/s, $$T = 2\pi/1.667 \approx 3.77$$ s. 2. $$v = 0.22$$ m/s, $$\omega = 0$$. The pivot is not a nearby point on the axle; the heading is constant. 3. The contact patch is leading the swivel, so the caster is reversed or the fork has no trail. Remount it so the patch trails. 4. The tires must scrub sideways, and scrub demands stall-level torque. Capstone A uses two driven wheels and one trailing caster so the idle wheel swivels. 5. One motor’s sign is reversed. Wheels up, a positive command should spin both tires in the forward direction you defined in the lab.

## Further reading

- [diff_drive_controller (ROS 2)](https://github.com/ros-controls/ros2_controllers/tree/master/diff_drive_controller) — linear.x and angular.z become two wheel velocities through the equations in this lesson.
- [Nav2 odometry setup](https://navigation.ros.org/setup_guides/odom/setup_odom.html) — what you publish after the arrows are honest.
- [ROS 1 diff_drive_controller wiki](https://wiki.ros.org/diff_drive_controller) — the same split into left and right wheel joints, documented for ROS 1 and still the right picture.

Siegwart, Nourbakhsh, and Scaramuzza, *Introduction to Autonomous Mobile Robots*, is the book-length treatment of this kinematics. Use the links above for the parameters your ROS distro actually reads.
