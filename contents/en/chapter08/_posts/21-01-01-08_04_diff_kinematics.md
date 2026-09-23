---
layout: post
title: "Differential-drive kinematics"
chapter: "08"
order: 4
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter08
lesson_type: required
draft: false
---

Estimated time: **~75 minutes**.

## Learning objectives

You will measure the track width of your Capstone base, convert a body velocity $$(v, \omega)$$ into left and right tread speeds, and convert those speeds back to check the arithmetic. You will predict the turning radius of a joystick command before the robot moves, and you will explain why a differential-drive base cannot slide sideways. Those two equations are the body of every `cmd_vel` callback from Chapter 10 onward.

## Prerequisites

You can identify which wheel is left when you sit on the robot looking forward. Chapter 07’s open-loop teleop already spins those wheels. A ruler or a tailor’s tape is the only new tool. PID from lesson 08-03 is optional here: kinematics produces speed targets, and open-loop PWM can still demonstrate the shape of a turn with the wheels in the air.

## Why this sits on the path

`geometry_msgs/Twist` is not a left motor and a right motor. Nav2, teleop_twist_keyboard, and any later policy publish forward speed and yaw rate in the robot’s body frame. Someone must invert that into two wheel speeds. If that someone uses the wrong track width, every map in Chapter 11 is scaled wrong even when the SLAM software is perfect. If the sign of $$\omega$$ is flipped, the robot turns away from the goal and the planner “fails” for a mechanical reason. Write the inverse once, with units, and call it from the serial bridge.

![Top view of track width and wheel speeds]({{ site.imgurl }}/generated/ch08_diff_kinematics.png)

## Concepts

REP-103 puts $$+x$$ forward, $$+y$$ left, and $$+z$$ up. Positive yaw rate $$\omega$$ is a left turn: the right wheel is faster than the left. Wheel speeds $$v_R$$ and $$v_L$$ are tread speeds in metres per second, positive forward. $$L$$ is the track width in metres, the distance between the two contact patches, not the width of the acrylic plate and not the distance between motor shafts if the tires bulge.

The forward map, from wheels to the body:

$$
v = \frac{v_R + v_L}{2}
$$

$$
\omega = \frac{v_R - v_L}{L}
$$

The inverse map, from a Twist to the wheels:

$$
v_R = v + \omega \frac{L}{2}
$$

$$
v_L = v - \omega \frac{L}{2}
$$

If $$v = 0$$ and $$\omega \neq 0$$, the wheels are equal and opposite and the robot spins about its centre. The turning radius for $$v \neq 0$$ is

$$
R = \frac{v}{\omega}
$$

with the centre of the turn a distance $$R$$ to the left of the robot when $$\omega > 0$$ and $$v > 0$$. There is no $$v_y$$. A command that asks the base to slide sideways is not a small error; the mechanism cannot do it. Controllers that ignore that fact oscillate. You will see the same sentence again in the Nav2 tour.

Wheel radius $$r$$ enters only when you need shaft rate or encoder counts:

$$
\dot{\theta} = \frac{v_{\text{wheel}}}{r}
$$

Keep $$r$$ out of the $$v, \omega$$ formulas. A common bug is to mix revolutions per second with metres per second in the same variable.

Joystick axes are not metres per second. Pick a scale on purpose, for example full stick forward means $$v = 0.3$$ m/s and full stick yaw means $$\omega = 1.0$$ rad/s, and write the scale next to the equations. Lesson 08-01’s −100…100 integers are a third scale. One function converts m/s of tread into that integer after the inverse kinematics, using the speed you observed at PWM 100 during the Chapter 07 spin test. Do not hide the scale inside “it felt right.”

## Worked example

Tape measurement: contact patch to contact patch, $$L = 0.16$$ m. Wheel radius $$r = 0.033$$ m, used only at the end. Command: $$v = 0.20$$ m/s, $$\omega = 0.50$$ rad/s (a gentle left turn).

$$
\frac{L}{2} = 0.08
$$

$$
v_R = 0.20 + 0.50 \times 0.08 = 0.24 \text{ m/s}
$$

$$
v_L = 0.20 - 0.50 \times 0.08 = 0.16 \text{ m/s}
$$

Check:

$$
v = \frac{0.24 + 0.16}{2} = 0.20
$$

$$
\omega = \frac{0.24 - 0.16}{0.16} = 0.50
$$

Turning radius $$R = 0.20 / 0.50 = 0.40$$ m. On the floor, a piece of tape at the geometric centre of the axle should travel a circle of radius about 0.40 m. The right tire travels a larger circle than the left, which is why it is faster.

Shaft rate of the right wheel, if you need it for PID:

$$
\dot{\theta}_R = \frac{0.24}{0.033} \approx 7.27 \text{ rad/s}
$$

Python you can paste into the bridge later:

```python
def wheel_speeds(v: float, omega: float, track: float) -> tuple[float, float]:
    half = 0.5 * track
    return v - omega * half, v + omega * half  # left, right

def body_from_wheels(v_l: float, v_r: float, track: float) -> tuple[float, float]:
    return 0.5 * (v_r + v_l), (v_r - v_l) / track

assert abs(body_from_wheels(*wheel_speeds(0.2, 0.5, 0.16), 0.16)[1] - 0.5) < 1e-9
```

A pure spin, $$v = 0$$, $$\omega = 1.0$$, $$L = 0.16$$: $$v_R = 0.08$$, $$v_L = -0.08$$. If both numbers come out positive, you added $$\omega L$$ to both wheels instead of splitting the sign.

## Lab

1. Put the robot on a table, wheels up or a stand. Measure $$L$$ three times and record the mean in metres.
2. Mark the tyre with chalk. Command equal wheel speeds for two seconds and confirm both marks move forward. That fixes the sign of $$v_L$$ and $$v_R$$ in your firmware.
3. Command the pure spin above at low PWM (map 0.08 m/s to whatever duty was “slow forward” in Chapter 07). The left wheel must turn backward.
4. Optional floor test, clear space, slow speed: drive $$v = 0.2$$, $$\omega = 0.5$$ for a quarter turn and compare the tape-measure radius with 0.40 m scaled by your real $$L$$. Recompute $$R = v/\omega$$ with your numbers before you drive.
5. Save the function and the measured $$L$$ in the same file you will import from the Chapter 10 bridge.

**Expected notes**

```text
L_mean = 0.158 m
equal command: both wheels forward
v=0, w>0: right forward, left backward
R predicted = 0.40 m, R taped = 0.45 m  (slip, do not "fix" with a random gain)
```

A 10 percent radius error on carpet is slip and scrub, not a failed formula. A reversed left wheel is a failed sign.

**Failure modes**

| What you see | Likely cause |
| --- | --- |
| Robot curves the wrong way | $$\omega$$ sign, or left/right swapped in the tuple |
| Straight command drives a circle | One wheel’s PWM scale is softer, or one tyre is smaller. Kinematics will not hide that; PID might |
| Radius is half of what you predicted | You used the plate width, or you used diameter as $$L$$ |
| Both wheels reverse on a left turn | You set $$v_L = v + \omega L/2$$ |
| Later, the map scale is nonsense | $$L$$ or $$r$$ was in centimetres inside a metre formula |

## Where to buy this in Vietnam

No new electronics. A 3 m tailor tape from any stationery stall is enough (about 15.000–40.000 VND on Shopee, keyword `thước dây 3m`). If a tyre is oval or the foam tyre has flattened, replace the pair so $$r$$ matches: search `bánh xe robot cao su 65mm` and expect roughly 20.000–60.000 VND per wheel. Buy both wheels together. Mixing diameters is a fake kinematics bug.

## Exercises

1. Your track is 0.20 m. Joystick asks for $$v = 0$$, $$\omega = -0.8$$ rad/s. Compute $$v_L$$ and $$v_R$$ and name the turn. Guidance: right wheel negative, left wheel positive, a right turn (negative yaw).
2. Both wheels at 0.3 m/s. What are $$v$$ and $$\omega$$? Guidance: $$v = 0.3$$, $$\omega = 0$$, regardless of $$L$$.
3. Why can you not satisfy $$v_x = 0$$, $$v_y = 0.2$$, $$\omega = 0$$ with any $$v_L, v_R$$? Guidance: both formulas only produce motion along $$x$$ and yaw. $$v_y$$ is identically zero.
4. You measured $$L = 15.5$$ cm and typed `0.155` in one file and `15.5` in the bridge. Which symptom shows up in $$R$$? Guidance: the radius is wrong by a factor of 100, which looks like “the robot pivots in place no matter what.”
5. Where does this function sit relative to PID? Guidance: Twist → this function → two m/s setpoints → two PID loops → two PWMs. Skipping PID means the m/s numbers are only hopes.

## Further reading

- [REP-103, Standard Units of Measure and Coordinate Conventions](https://www.ros.org/reps/rep-0103.html).
- [REP-105](https://www.ros.org/reps/rep-0105.html) for `base_link`, which is the frame these equations live in.
- [Modern Robotics, Chapter 13](https://hades.mech.northwestern.edu/index.php/Modern_Robotics) (free online) if you want the wheeled-robot chapter after the two-line model feels small.
- `geometry_msgs/Twist` in the [Jazzy message docs](https://docs.ros.org/en/jazzy/p/geometry_msgs/msg/Twist.html): `linear.x` is $$v$$, `angular.z` is $$\omega$$, and the other four fields stay near zero on this base.
