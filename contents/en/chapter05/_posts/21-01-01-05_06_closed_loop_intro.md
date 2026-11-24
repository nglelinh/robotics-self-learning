---
layout: post
title: "Lab: closed-loop intro sense → compute → act"
chapter: "05"
order: 6
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter05
lesson_type: required
draft: false
---

In 1788, James Watt bolted two spinning brass balls onto a steam engine — the centrifugal flyball governor. When the engine sped up, the balls swung outward and pinched the steam valve shut; when it slowed down under load, they dropped and opened the valve wider. Without a single line of code, Watt had harnessed the most powerful idea in all of engineering: **negative feedback**. On your robot, open-loop PWM ("set duty = 50%") fails the instant the battery drains or the floor shifts from tile to carpet; **closed-loop control** (*sense → compute → act*) measures actual speed every 10 milliseconds and automatically compensates.

This culminating lab of Chapter 05 brings every chapter together — electronics, MCU timers, encoders, H-bridges, and feedback control — into one living closed-loop wheel controller.r

---

Every later controller on this robot is the same three boxes: sense, compute, act. This lab closes them with the rudest computer that still counts: if the range is inside 20 cm, the wheel PWM is zero; otherwise a modest forward PWM is allowed. That law is bang-bang. PID arrives in Chapter 08. What you practice now is the safety shape those later laws must keep: a failed sensor means stop.

## Learning objectives

1. Draw the sense, compute, and act loop for a range sensor and one motor command.
2. Implement a bang-bang rule at 20 cm, with a timeout that forces PWM to zero.
3. Add a simple hysteresis band so the motor does not chatter at the threshold.
4. Say where a ROS 2 subscriber of `/cmd_vel` will sit in this diagram, and which stop must remain in firmware.

## Prerequisites

You need a range reading from the ultrasonic or time-of-flight lesson in Chapter 04, in millimetres or in centimetres you can convert. You need one motor channel whose forward truth table you wrote in lesson 05-01, on a driver you can name from lesson 05-02. Wheels come off the ground before they touch the floor. A cardboard target and a power switch you can hit with your hand are part of the apparatus.

## Background Knowledge Map: Open-Loop vs. Closed-Loop Control, Proportional–Integral Action, and Anti-Windup

Four control-theory pillars turn a spinning motor into a precision velocity actuator:

- **Error-Driven Feedback ($$e_k = r_k - y_k$$):** At each discrete tick $$k$$ (period $$\Delta t$$), the controller compares desired wheel velocity $$r_k$$ against encoder-measured velocity $$y_k$$ and computes command $$u_k$$.
- **Proportional (P) vs. Integral (I) Action:** Pure proportional control $$u_k = K_p e_k$$ responds instantly to error, yet **always leaves steady-state error** against constant friction or gravity (if $$e = 0$$, $$u = 0$$, so the wheel stops!). Adding an integral term $$I_k = I_{k-1} + K_i e_k \Delta t$$ accumulates persistent error until steady-state error reaches **exact zero**.
- **Feedforward + Feedback:** Combining a rough open-loop model $$u_{\text{ff}} = k_v r_k$$ with PI feedback lets the feedback loop handle only *disturbances* (battery droop, carpet friction), cutting rise time in half.
- **Actuator Saturation & Integrator Anti-Windup:** PWM is bounded to $$[-u_{\max}, +u_{\max}]$$. If a wheel jams while the integrator keeps summing error blindly, the integral term grows enormous (*windup*) and causes violent overshoot once released. Clamping the integrator whenever output saturates eliminates windup cleanly.r

---

## Why this matters for Capstone A and the ROS path

Capstone A will drive toward things and, more importantly, stop before it hits them. Chapter 07 assembles two signed PWMs. Chapter 08 replaces this on/off compute block with a PID that can hold a speed or a heading. The sense and act blocks stay. When ROS 2 is introduced, a subscriber to `/cmd_vel` is another way to fill the compute block: some other process proposes a twist, and your node turns it into left and right PWM. The range stop does not move out into that topic. Firmware still owns the last look at the sensor. If the topic says "forward" and the range says "too close" or "I have no idea," the wheels stop. A planner that goes silent must not be interpreted as a clear hallway.

## Bang-bang, in one sentence

Read the range. If it is under 20 cm, command PWM 0. If it is clearly farther, command PWM 80 in the forward direction from your truth table. Eighty on an 8-bit scale is a slow creep, which is what you want while a hand is still the target.

$$
\mathrm{PWM} =
\begin{cases}
0 & \text{if range} < 20~\mathrm{cm} \\
80 & \text{otherwise, when the reading is valid}
\end{cases}
$$

The "otherwise" is the dangerous word. A sensor that times out, returns a maximum sentinel, or returns 0 because the echo never came, is not a valid "otherwise." Those readings take the stop branch. A failed sensor must not mean "the path is clear, full speed."

Hysteresis keeps the shaft from buzzing when you hold a hand near 20 cm. Stop when the range falls below 20 cm. Stay stopped until the range rises above 25 cm. Between those two numbers, keep the previous command. The motor then switches a little less often, and the gearbox stops clicking at the boundary.

## Where the three boxes are in the code

Sense is the function you already trust from Chapter 04, wrapped so that a timeout comes back as a negative number or an explicit invalid flag. Compute is the `if` below. Act is the pair of direction pins plus one PWM write. Put the pin numbers in named constants at the top so the lab write-up can say which GPIO moved.

```cpp
const int PIN_IN1  = 25;   // edit to your forward pair
const int PIN_IN2  = 26;
const int PIN_PWM  = 27;
const int PIN_TRIG = 5;    // ultrasonic; ignore for ToF
const int PIN_ECHO = 18;

const int PWM_FORWARD = 80;
const int STOP_MM = 200;   // 20 cm
const int GO_MM   = 250;   // 25 cm, hysteresis release

void setup() {
  pinMode(PIN_IN1, OUTPUT);
  pinMode(PIN_IN2, OUTPUT);
  pinMode(PIN_PWM, OUTPUT);
  digitalWrite(PIN_IN1, HIGH);   // forward, from YOUR truth table
  digitalWrite(PIN_IN2, LOW);
  analogWrite(PIN_PWM, 0);       // safe act, before any sensor read
}

void loop() {
  int mm = readRangeMm();        // Chapter 04; negative means timeout / invalid
  if (mm < 0 || mm <= STOP_MM) {
    analogWrite(PIN_PWM, 0);
  } else if (mm >= GO_MM) {
    analogWrite(PIN_PWM, PWM_FORWARD);
  }
  // between 200 and 250 mm, hold the previous PWM
  delay(50);
}
```

`readRangeMm` is the function you adapt from your ultrasonic or ToF sketch. On a timeout it returns a negative value. A literal 0 also stops, because $$0 \le 200$$. Direction is set once, from the truth table, so this first loop only has to decide speed. When you later mix in a reverse escape, you will change IN1 and IN2 on purpose, in the act block, with the same "invalid means stop" rule still above them.

Wheels-up procedure: hold your hand in front of the sensor. Far hand, the wheel spins forward slowly. Hand inside about 20 cm, the wheel stops. Cover the sensor or unplug the echo wire for a moment and confirm the wheel stops, because the read failed. Only after that do you put the robot on the floor, point it at cardboard, and keep your hand on a switch that removes motor power. The floor run is short. You are checking the stop, not racing the hallway.

## Worked example

Thresholds: stop at 200 mm, go at 250 mm and above.

A reading of 180 mm is below 200 mm, so PWM becomes 0. A reading of 900 mm is a clear hallway, so PWM becomes 80 forward. A reading of 0, or a timeout returned as −1, takes the stop branch even though 0 is "less distance" and a timeout is "no distance." The compute block refuses to treat either as permission to move.

Walk the hysteresis. The hand approaches: 400 mm (forward), 260 mm (still forward, because 260 is above 250), 220 mm (hold forward, inside the band), 180 mm (stop). The hand backs away: 220 mm (stay stopped, inside the band), 260 mm (forward again). Without the band, 190 mm and 210 mm of sensor noise would click the gearbox on every loop.

## Figures

![Sense, compute, act: the range reading enters, a decision is made, a motor command leaves]({{ site.imgurl }}/generated/sense_compute_act.png)

Label the boxes with your own nouns: ultrasonic or ToF, the bang-bang `if`, and the H-bridge PWM. Draw a second arrow into compute and write `/cmd_vel` on it, then draw the stop still sitting in firmware after that arrow.

## Lab

### Safety

First session: chassis on a stand, wheels in the air, current limit or fuse in place, USB on the microcontroller only. Second session: short floor run toward cardboard, one person, hand on a switch that cuts motor power. Keep PWM at 80, not 255. If the sensor stream stops, the wheel must already be stopped by your timeout branch. Do not "fix" a timeout by commenting that branch out.

### BOM

| Item | Role |
|------|------|
| Microcontroller plus the range sensor from Chapter 04 | Sense |
| One motor and the identified driver | Act |
| Battery or limited supply for VM, common ground | Motor power |
| Cardboard target | A surface the sensor can see |
| Power switch you can reach | The human fuse |
| Notebook | The three test readings and the timeout test |

### Steps

1. Confirm `readRangeMm` against a ruler at about 20 cm and about 50 cm before the motor is enabled. Fix the sensor first.
2. Enter the constants and the `loop` above. Set direction from your truth table. PWM stays 0 until the first valid far reading.
3. Wheels up. Present a hand at roughly 40 cm, then 15 cm, then cover the sensor. Record PWM behavior for each.
4. Optional floor run: cardboard at the end of a short lane, hand on the switch, PWM 80. The robot should creep and stop near 20 cm. If it does not stop, cut power. Do not raise PWM.
5. Write the hysteresis story in two lines: the distance where it stopped, and the distance where it started again.

### Expected results

A note with three cases (far → forward, near → stop, timeout or 0 → stop) and, if you drove on the floor, the approximate stopping distance. A sentence that names `/cmd_vel` as a future compute input that does not get to override this stop.

### Faults

| What you see | What to check |
|--------------|----------------|
| Wheel runs when the sensor is unplugged | Timeout is falling through to the forward branch. Return a negative code and test `mm < 0`. |
| Wheel chatters at the boundary | The go and stop thresholds are equal. Separate them (200 mm and 250 mm). |
| Wheel runs backward | IN1 and IN2 do not match the forward row of your truth table. |
| Robot never starts | Every read is inside the stop band, the target is too close, or STBY / enable is low. |
| Floor run does not stop | Wrong units (cm compared with 200), or the sensor is aimed over the cardboard. Cut power. |

## Deep-Dive Explanation (Read Slowly): Hand-Stepping 3 Ticks of a Discrete PI Wheel Velocity Controller

Before tuning gains on your robot, trace three consecutive 100 Hz control ticks ($$\Delta t = 0.01\text{ s}$$) of a discrete **PI velocity controller** by hand:

1. **Write the discrete PI update equations:**
   $$e_k = r_k - y_k, \qquad I_k = \operatorname{clamp}\bigl(I_{k-1} + K_i e_k \Delta t,\; -u_{\max}, +u_{\max}\bigr), \qquad u_k = \operatorname{clamp}\bigl(K_p e_k + I_k,\; -u_{\max}, +u_{\max}\bigr).$$
2. **Initialize state cleanly:** $$I_0 = 0$$, command range $$u \in [-1.0, +1.0]$$ (normalized PWM duty).
3. **Update error, integral, and PWM at each tick** using actual encoder feedback $$y_k$$.
4. **Watch the integral term carry the friction load** as error shrinks toward zero!

### Concrete Worked Example: 3 Control Ticks with $$K_p = 1.2\text{ s/m}$$, $$K_i = 8.0\text{ m}^{-1}$$, Target $$r = 0.40\text{ m/s}$$

Suppose the robot commands $$r = 0.40\text{ m/s}$$ from rest ($$\Delta t = 0.01\text{ s}$$, so $$K_i \Delta t = 0.08$$, $$I_0 = 0$$), and the encoder measures $$y_1 = 0.00$$, $$y_2 = 0.15$$, $$y_3 = 0.30\text{ m/s}$$:

| Tick $$k$$ | Meas $$y_k$$ (m/s) | Error $$e_k = 0.40 - y_k$$ | P-term $$1.2 e_k$$ | Integrator $$I_k = I_{k-1} + 0.08 e_k$$ | Output $$u_k = P + I_k$$ (PWM %) |
| --- | --- | --- | --- | --- | --- |
| $$1$$ | $$0.00$$ | $$+0.40$$ | $$+0.480$$ | $$0 + 0.032 = 0.032$$ | $$0.512$$ (51.2%) |
| $$2$$ | $$0.15$$ | $$+0.25$$ | $$+0.300$$ | $$0.032 + 0.020 = 0.052$$ | $$0.352$$ (35.2%) |
| $$3$$ | $$0.30$$ | $$+0.10$$ | $$+0.120$$ | $$0.052 + 0.008 = 0.060$$ | $$0.180$$ (18.0%) |

Look at what happens as $$y_k \to 0.40\text{ m/s}$$: the proportional term smoothly tapers to `0`, while the integral term $$I_k$$ climbs and settles at the exact steady-state PWM needed to overcome motor friction and battery level — locking the wheel onto $$0.40\text{ m/s}$$ automatically!

**Common Pitfall:** Using **positive feedback** by accident (wiring the encoder backward or writing `e = y - r` instead of `e = r - y`) — instead of braking when too fast, the controller slams PWM to `100%` and runs away uncontrollably! Always test with wheels lifted off the desk first.

**Quick Check:** If steady-state cruise at $$0.40\text{ m/s}$$ requires $$u = 0.36$$ PWM and you run *pure P-control* ($$K_i = 0, K_p = 1.2$$), the wheel can never reach $$0.40\text{ m/s}$$ — it stalls at $$e_{\text{ss}} = 0.36 / 1.2 = 0.30\text{ m/s}$$ error (only $$y = 0.10\text{ m/s}$$!). That single division proves why integral action or feedforward is essential.

---

## Mua ở Việt Nam / Where to buy in Vietnam

This lab uses the sensor and the driver you already have. Buy only the gap: a TB6612 or L298N if lesson 05-02 is still short a board, a TT motor if you have no shaft to watch, an HC-SR04 or a small ToF if Chapter 04 was done on a classmate's bench. Prices move. Rough bands: HC-SR04 about 15.000–35.000 VND, TT motor about 25.000–45.000 VND, L298N module about 35.000–70.000 VND.

- Verified L298N page, about 45.000 VND: [hshop.vn/mach-dieu-khien-dong-co-dc-l298](https://hshop.vn/mach-dieu-khien-dong-co-dc-l298)
- HShop: [HC-SR04](https://hshop.vn/search?q=HC-SR04), [TB6612](https://hshop.vn/search?q=TB6612), [motor TT](https://hshop.vn/search?q=motor%20TT)
- Shopee: [HC-SR04](https://shopee.vn/search?keyword=HC-SR04), [TB6612](https://shopee.vn/search?keyword=TB6612)
- Lazada: [HC-SR04](https://www.lazada.vn/catalog/?q=HC-SR04), [VL53L0X](https://www.lazada.vn/catalog/?q=VL53L0X)
- Thế Giới IC: [HC-SR04](https://www.thegioiic.com/search?q=HC-SR04), [L298N](https://www.thegioiic.com/search?q=L298N)

## Exercises

1. Range reads 180 mm, then 900 mm, then a timeout. What PWM do you command in each case if stop is 200 mm and go is 250 mm?
2. Why does a reading of 0 take the stop branch?
3. The wheel clicks on and off with the hand held still near 20 cm. Which two constants do you separate?
4. A `/cmd_vel` message says forward at the same moment the range is 12 cm. What does firmware do?
5. PID is Chapter 08. What is the compute block you ship today, in one sentence?

### Answer guidance

180 mm stops, 900 mm commands PWM 80 forward, and a timeout stops. A 0 reading is invalid or inside the stop threshold, so it must not count as a clear path. Separate the stop and go thresholds, for example 200 mm and 250 mm, and hold the previous command inside the band. Firmware stops on the 12 cm reading even if `/cmd_vel` says forward. Today's compute block is bang-bang: PWM 0 when the range is under 20 cm or the sensor has failed, and PWM 80 forward when the range is valid and beyond the hysteresis release.

## Further reading

- Control Guru, on/off control and how the output responds when the measurement crosses a setpoint: [https://controlguru.com/the-on-off-controller-output-response-to-set-point-changes/](https://controlguru.com/the-on-off-controller-output-response-to-set-point-changes/)
- ROS 2 topics, the pipe a later `/cmd_vel` subscriber will listen on. `geometry_msgs/Twist` itself is introduced in Chapter 09: [https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Topics/Understanding-ROS2-Topics.html](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Topics/Understanding-ROS2-Topics.html)
