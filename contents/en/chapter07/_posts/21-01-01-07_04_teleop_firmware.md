---
layout: post
title: "Firmware teleop loop (no ROS yet)"
chapter: "07"
order: 4
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter07
lesson_type: required
draft: false
---

Lesson 03 specified the lines. This lesson is the ESP32 sketch that parses them, clamps them, slews them, and drops them to zero when the host goes quiet. ROS is still not in the loop. The wheels stay in the air.

## Learning objectives

1. Parse `V` and `S` with `sscanf`, clamp each target to $$\pm 180$$, and ignore a bad line.
2. Zero both targets after $$250~\mathrm{ms}$$ of silence, and slew the applied PWM by 15 counts every $$20~\mathrm{ms}$$.
3. Drive two channels with STBY high, and edit the example pins to the lesson 02 sign map.
4. Send `V l r\n` from Python, kill the process, and see both tires stop within $$0.5~\mathrm{s}$$ while the MCU stays on the buck.

## Prerequisites

You need lesson 07-01's power tree, lesson 07-02's sign map, and lesson 07-03's grammar: 115200 8N1, newline-terminated text, host refresh $$200~\mathrm{ms}$$, firmware deadline $$250~\mathrm{ms}$$, clamp $$-180..180$$. On a TB6612, STBY low keeps the outputs off, and PWM 0 with STBY high is a short brake, not a high-Z coast. Chapter 06's $$b$$ and $$r$$ stay in the notes; this sketch does not read them. Positive still means that tire toward the nose. Twist, with `linear.x` and `angular.z`, comes after Chapter 08 calibrates and Chapter 09 carries topics. No ROS workspace today.

## Why this matters for Capstone A and the ROS path

The bug that matters is a command that sticks: the host dies and the last LEDC duty keeps the robot rolling on battery power. The timeout belongs in firmware. A later Twist stream needs the same deadline. Chapter 09 replaces the parser, not the stop.

The figure's sense and compute boxes are the encoder and the PID you do not have yet. This lesson is the act box: PWM, and a timeout that forces zero.

![Act is PWM to the driver; the timeout that forces zero is already part of the box]({{ site.imgurl }}/generated/sense_compute_act.png)

## Clamp, timeout, and a slew you can count

Targets are what the last legal line asked for, after the clamp. Applied PWM is what the bridge is receiving, and it is allowed to trail the target. Every $$20~\mathrm{ms}$$ the applied value steps at most 15 counts toward the target:

$$
\text{steps} = \left\lceil \frac{|\text{target} - \text{applied}|}{15} \right\rceil, \qquad t_{slew} = \text{steps} \times 20~\mathrm{ms}.
$$

From 0 to 60 is 4 steps, $$80~\mathrm{ms}$$. From 0 to 180 is 12 steps, $$240~\mathrm{ms}$$. The windings never see a full step.

If `millis()` minus the last valid line exceeds $$250~\mathrm{ms}$$, both targets become 0 and the slew walks the duty down. After an unrefreshed `V 60 60`, targets fall at $$250~\mathrm{ms}$$ and applied PWM hits 0 about $$80~\mathrm{ms}$$ later:

$$
250~\mathrm{ms} + 4 \times 20~\mathrm{ms} = 330~\mathrm{ms}.
$$

That lands inside the $$0.5~\mathrm{s}$$ stop. A command of 180 takes $$250+240=490~\mathrm{ms}$$, which is why the clamp and the slew were chosen together. `S` zeros the targets immediately; the slew still softens the brake. An illegal line does not refresh the deadline.

Example pins, which you must edit to the lesson 02 map: STBY 4, AIN1 16, AIN2 17, PWMA 18, BIN1 19, BIN2 21, PWMB 22. Swap an IN pair in code or the motor screws, not both. Arduino-ESP32 3.x uses `ledcAttach(pin, freq, resolution)`; 2.x uses `ledcSetup` and `ledcAttachPin`, and the sketch shows both. `Serial.setTimeout(10)` keeps the slew from blocking.

```cpp
// Edit pins and IN polarity to the lesson 07-02 sign map.
// Positive rolls that tire toward the nose.

const int PIN_STBY = 4;
const int PIN_AIN1 = 16;
const int PIN_AIN2 = 17;
const int PIN_PWMA = 18;
const int PIN_BIN1 = 19;
const int PIN_BIN2 = 21;
const int PIN_PWMB = 22;

const int PWM_FREQ = 20000;
const int PWM_RES  = 8;
const int PWM_LIM  = 180;
const unsigned long TIMEOUT_MS = 250;
const int SLEW_STEP = 15;
const unsigned long SLEW_MS = 20;

int targetL = 0, targetR = 0;
int appliedL = 0, appliedR = 0;
unsigned long lastRx = 0;
unsigned long lastSlew = 0;

int approach(int applied, int target) {
  if (applied < target) return min(applied + SLEW_STEP, target);
  if (applied > target) return max(applied - SLEW_STEP, target);
  return applied;
}

void drive(int in1, int in2, int pwmPin, int cmd) {
  int mag = abs(cmd);
  if (cmd > 0) {
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
  } else if (cmd < 0) {
    digitalWrite(in1, LOW);
    digitalWrite(in2, HIGH);
  } else {
    digitalWrite(in1, LOW);
    digitalWrite(in2, LOW);
  }
  ledcWrite(pwmPin, mag);
}

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(10);
  pinMode(PIN_STBY, OUTPUT);
  pinMode(PIN_AIN1, OUTPUT);
  pinMode(PIN_AIN2, OUTPUT);
  pinMode(PIN_BIN1, OUTPUT);
  pinMode(PIN_BIN2, OUTPUT);
  digitalWrite(PIN_AIN1, LOW);
  digitalWrite(PIN_AIN2, LOW);
  digitalWrite(PIN_BIN1, LOW);
  digitalWrite(PIN_BIN2, LOW);
  // Arduino-ESP32 3.x:
  ledcAttach(PIN_PWMA, PWM_FREQ, PWM_RES);
  ledcAttach(PIN_PWMB, PWM_FREQ, PWM_RES);
  // Older 2.x cores, instead of ledcAttach / ledcWrite(pin, duty):
  // ledcSetup(0, PWM_FREQ, PWM_RES); ledcAttachPin(PIN_PWMA, 0);
  // ledcSetup(1, PWM_FREQ, PWM_RES); ledcAttachPin(PIN_PWMB, 1);
  // then ledcWrite(0, duty) and ledcWrite(1, duty) — the channel, not the pin.
  ledcWrite(PIN_PWMA, 0);
  ledcWrite(PIN_PWMB, 0);
  digitalWrite(PIN_STBY, HIGH);
  lastRx = millis();
  lastSlew = millis();
}

void loop() {
  if (Serial.available()) {
    char line[32];
    size_t n = Serial.readBytesUntil('\n', line, sizeof(line) - 1);
    line[n] = '\0';
    if (n > 0 && line[n - 1] == '\r') line[n - 1] = '\0';
    int L = 0, R = 0;
    if (line[0] == 'S' && (line[1] == '\0' || line[1] == ' ')) {
      targetL = 0;
      targetR = 0;
      lastRx = millis();
    } else if (sscanf(line, "V %d %d", &L, &R) == 2) {
      targetL = constrain(L, -PWM_LIM, PWM_LIM);
      targetR = constrain(R, -PWM_LIM, PWM_LIM);
      lastRx = millis();
    }
    // Any other line is ignored.
  }

  if (millis() - lastRx > TIMEOUT_MS) {
    targetL = 0;
    targetR = 0;
  }

  if (millis() - lastSlew >= SLEW_MS) {
    lastSlew = millis();
    appliedL = approach(appliedL, targetL);
    appliedR = approach(appliedR, targetR);
    drive(PIN_AIN1, PIN_AIN2, PIN_PWMA, appliedL);
    drive(PIN_BIN1, PIN_BIN2, PIN_PWMB, appliedR);
  }
}
```

Opening the port often resets the ESP32 through DTR. `setup` drives PWM 0 before STBY goes high, so the reset is a stop. Do not trust DTR on close. The timeout stops the robot while the MCU stays on the buck. Unplugging USB tests that only if the buck, not USB, is powering the ESP32. USB-only power floats the pins and is not a timeout test.

Use the Chapter 02 port, `/dev/ttyUSB0` or `/dev/ttyACM0`. `sleep(0.2)` is the $$200~\mathrm{ms}$$ refresh, and `close()` is silence.

```python
import time
import serial

port = serial.Serial("/dev/ttyUSB0", 115200, timeout=0.1)
time.sleep(2.0)

t0 = time.time()
while time.time() - t0 < 1.0:
    port.write(b"V 60 60\n")
    time.sleep(0.2)

port.close()
```

A second run writes `V 60 -60\n` for one second. Left forward and right back is a right yaw on the lesson 02 map. If the flags disagree, edit that channel's IN pins, not the screws, in this session.

## Lab

### Safety

Both tires stay in the air, clear of the table edge, and one hand can open the battery switch. The first command is `V 60 60`, not 255. This lesson does not go on the floor. A smell or a tab you cannot touch means open the switch. No bare lithium leads on an armed bench.

### BOM

| Item | Role |
|------|------|
| Assembled robot, wheels up | The plant |
| ESP32 on the 5.0 V buck, USB for the program | Logic stays up when you kill the script |
| Sign map from lesson 07-02 | Pin polarity |
| Python 3 with pyserial | The host |
| Phone timer or the millis arithmetic | The 0.5 s stop |

### Steps

1. Edit pins and IN polarity so positive matches lesson 02. Flash. STBY high, duties start at 0.
2. Wheels up. Send `V 60 60` for about one second. Both flags move toward the nose.
3. Kill the script. Both tires stop within $$0.5~\mathrm{s}$$ with the battery switch still on.
4. Send `V 60 -60` for one second. Yaw matches the map (right spin: left forward, right back). Kill the sender again.
5. Type `S`, then `V 60` alone. `S` stops. The broken line does not move one wheel.

### Expected results

Notes record the pins you used, the stop time (about $$330~\mathrm{ms}$$ after the last `V 60 60`), and the yaw for `V 60 -60`. The robot is still on the box. A stuck duty after the process dies fails the lab.

### Faults

| What you see | What it usually means |
|--------------|------------------------|
| Nothing moves | STBY still low, wrong PWM pins, or VM off |
| Motion continues after you kill Python | Timeout missing, or the MCU was not actually running |
| Only the left tire matches the map | Right IN pair disagrees with lesson 02; fix firmware or the screws, not both |
| A one-wheel twitch on `V 60` | `sscanf` was not required to return 2 |
| Compile error on `ledcAttach` | Core is 2.x; use `ledcSetup` and `ledcAttachPin` |

## Mua ở Việt Nam / Where to buy in Vietnam

No new part if lessons 01 and 02 were real. A data-capable USB cable, or pyserial, is the usual gap. ESP32 devkit roughly 70–150k VND, TB6612 25–70k, L298N about 45.000 VND if you map ENA/ENB to the PWM pins and keep the buck. Prices move.

- Verified L298N, about $$45.000$$ VND: [hshop.vn/mach-dieu-khien-dong-co-dc-l298](https://hshop.vn/mach-dieu-khien-dong-co-dc-l298)
- [Hshop ESP32](https://hshop.vn/search?q=ESP32), [TB6612](https://hshop.vn/search?q=TB6612)
- [Shopee ESP32](https://shopee.vn/search?keyword=ESP32%20devkit), [TB6612](https://shopee.vn/search?keyword=TB6612)
- [Lazada cáp USB](https://www.lazada.vn/catalog/?q=cap%20micro%20USB%20data), [ESP32](https://www.lazada.vn/catalog/?q=ESP32)
- [Thế Giới IC ESP32](https://www.thegioiic.com/search?q=ESP32)

## Exercises

1. Applied PWM is 0 and the target becomes 180. How many slew steps, and how many milliseconds, until the bridge sees 180?
2. The last `V 60 60` arrives at $$t = 0$$ and nothing follows. When do the targets become 0, and when does applied PWM reach 0?
3. The line `V 200 -300` parses. What targets does `constrain` store? What does `V 60` do to those targets?
4. You delete only the timeout test and leave the slew. The Python process is killed and the port does not reset the chip. What do the tires do, and why is that the bug lesson 05 will refuse?
5. Lesson 02 says positive right is BIN1 low, BIN2 high. Which lines do you change, and why do the motor screws stay put?

### Answer guidance

1. $$180/15 = 12$$ steps, $$240~\mathrm{ms}$$. 2. Targets become 0 at $$250~\mathrm{ms}$$; applied PWM needs 4 more steps, so it is 0 at about $$330~\mathrm{ms}$$. 3. Targets become $$180$$ and $$-180$$. `V 60` is ignored, so the targets stay. 4. The last duty remains and the tires keep spinning. Lesson 05 then fails the kill-the-sender stop. 5. Swap the BIN1 and BIN2 writes for a positive right command. Leave the screws. A second inversion undoes the fix.

## Further reading

- [Arduino `Serial`](https://www.arduino.cc/reference/en/language/functions/communication/serial/)
- [pySerial short introduction](https://pyserial.readthedocs.io/en/latest/shortintro.html)
- [Pololu TB6612FNG](https://www.pololu.com/product/713)
- [geometry_msgs/Twist (Jazzy)](https://docs.ros.org/en/jazzy/p/geometry_msgs/interfaces/msg/Twist.html)
