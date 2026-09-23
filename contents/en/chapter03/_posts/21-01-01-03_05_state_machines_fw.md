---
layout: post
title: "State machines for robot firmware"
chapter: "03"
order: 5
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter03
lesson_type: required
draft: false
---

## Learning objectives

By the end of this lesson you can implement three firmware states, IDLE, TELEOP, and FAULT, so that a command, a 300 ms silence, and a button each do one defined thing. In IDLE and in FAULT both PWM channels are commanded to 0. You will write the machine as an `enum` and a `switch` in C++, and as an `if`/`elif` chain or a dictionary of functions in MicroPython, using the non-blocking clock from Lesson 1 rather than a sleep that stands in for a state. You will also reject the pattern where a blink flag and a motor flag can be true at the same time.

## Prerequisites

You can measure command age with `millis()` or `time.ticks_diff()`, which is the skill Lesson 1 put in place of the blocking heartbeat in the [Chapter 02 blink and serial lab]({% multilang_post_url contents/chapter02/02_04_blink_serial_hello %}). You can print a button edge, and you can write a duty with `ledcWrite` or `duty_u16` without believing that `analogWrite` is always 0–255 on an ESP32. The LED from the GPIO lab will stand in for "motors enabled." The TB6612 is still not wired. The timeout math you are encoding is the same 300 ms rule whose 200 ms sleep failure you already calculated.

## Why it matters

Capstone A teleop is not a pile of independent `if` statements. A differential-drive base is either waiting, driving from a fresh command, or stopped because commands died. Those are states, and the PWM pins are outputs of the state, not a side effect that some other block might overwrite. When ROS later delivers velocity commands, the firmware you want already knows what to do with "a command arrived" and with "nothing arrived for 300 ms": both TB6612 channels go to duty 0 in FAULT, and they stay 0 in IDLE. The wheels stay up while you prove that on an LED. A sketch that blinks a lamp and also writes a motor duty, using two booleans that can both be true, will drive and blink during the state you thought was a fault.

## Core teaching

A state machine is a variable that names exactly one situation, plus a rule for how events change that name. This firmware has three names.

IDLE means no drive is allowed. Both PWM channels are 0. The LED that stands in for "motors enabled" is off. A valid command is the event that leaves IDLE.

TELEOP means a command has been seen recently. The duties follow that command. Every new command refreshes a timestamp. If the age of that timestamp reaches 300 ms, the event is silence, and the next state is FAULT.

FAULT means the link looks dead, or you have decided the drive is not allowed. Both PWM channels are 0 again. The LED is off. The event that leaves FAULT is a button press, and it returns to IDLE, not directly to TELEOP. A command that arrives during FAULT does not start the wheels. The operator has to acknowledge with the button, then send a new command from IDLE. That extra step is deliberate: a reconnecting joystick must not resume the last motion by itself.

![IDLE, TELEOP, and FAULT, with the 300 ms arrow]({{ site.imgurl }}/generated/firmware_state_machine.png)

The illegal structure looks shorter and fails in combination:

```cpp
bool blinkMode = true;
bool motorsOn = true;

void loop() {
  if (blinkMode) { /* toggle the LED */ }
  if (motorsOn) { ledcWrite(18, 200); }
}
```

Nothing keeps `motorsOn` and a fault in opposite states, because they are not one variable. Both conditions can be true on the same pass, so the lamp blinks while a duty of 200 is still being written. After you add a third flag for the timeout, the truth table has eight rows and you will not test them. One `enum` has three rows. The `switch` writes PWM in one place.

C++ for the ESP32 Arduino core. The LED on GPIO 18 is bright only in TELEOP. A second channel is computed and printed so the "both channels" rule is visible, but only one physical LED is required. Serial commands are a single letter: `F` means forward at duty 40, `S` means an operator stop that returns to IDLE with duty 0. Silence is not `S`. Silence is the absence of either letter.

```cpp
const int LED = 18;
const int BTN = 4;
const uint32_t TIMEOUT_MS = 300;

enum class Mode : uint8_t { Idle, Teleop, Fault };
Mode mode = Mode::Idle;

uint32_t lastCmd = 0;
int duty = 0;  // 0..255 stand-in for both TB6612 channels

void setup() {
  pinMode(LED, OUTPUT);
  pinMode(BTN, INPUT_PULLUP);
  Serial.begin(115200);
  Serial.println("state IDLE duty 0");
}

void apply() {
  bool enabled = (mode == Mode::Teleop) && duty > 0;
  digitalWrite(LED, enabled ? HIGH : LOW);
  // Later: ledcWrite(PWMA, enabled ? duty : 0); ledcWrite(PWMB, enabled ? duty : 0);
}

void loop() {
  uint32_t now = millis();
  static int prevBtn = HIGH;
  int btn = digitalRead(BTN);
  bool btnPress = (btn == LOW && prevBtn == HIGH);
  prevBtn = btn;

  if (Serial.available()) {
    char c = Serial.read();
    if (c == 'F' || c == 'S') {
      if (mode == Mode::Idle) {
        mode = Mode::Teleop;
      }
      if (mode == Mode::Teleop) {
        lastCmd = now;
        duty = (c == 'F') ? 102 : 0;  // about 40% of 255, or commanded stop
        if (c == 'S') mode = Mode::Idle;
      }
      // In FAULT the character is ignored on purpose.
    }
  }

  if (mode == Mode::Teleop && (now - lastCmd) >= TIMEOUT_MS) {
    mode = Mode::Fault;
    duty = 0;
  }
  if (mode == Mode::Fault && btnPress) {
    mode = Mode::Idle;
    duty = 0;
  }
  apply();
}
```

Read `apply` before you read the transitions. IDLE and FAULT cannot light the LED, because `enabled` requires TELEOP. A duty value left over from the last `F` is forced out of the pin by that condition, and the timeout also stores 0 so a later bug cannot revive it. The button edge here is the simple poll from the GPIO lesson; you already know how to move it behind a 20 ms stability test. Keep that test if the button double-fires. Do not add `delay` to the FAULT branch.

MicroPython can store the same transitions as functions in a dictionary. Each function updates `state` and `duty` itself. The loop calls only `HANDLERS[state]`, so two states cannot run on the same pass.

```python
from machine import Pin
import time

led = Pin(18, Pin.OUT)
btn = Pin(4, Pin.IN, Pin.PULL_UP)
TIMEOUT_MS = 300

state = "IDLE"
last_cmd = time.ticks_ms()
duty = 0
prev_btn = 1

def apply():
    enabled = state == "TELEOP" and duty > 0
    led.value(1 if enabled else 0)

def on_idle(now, cmd, pressed):
    global state, last_cmd, duty
    if cmd == "F":
        state, duty, last_cmd = "TELEOP", 40, now
    elif cmd == "S":
        duty = 0

def on_teleop(now, cmd, pressed):
    global state, last_cmd, duty
    if cmd == "F":
        duty, last_cmd = 40, now
    elif cmd == "S":
        state, duty = "IDLE", 0
    elif time.ticks_diff(now, last_cmd) >= TIMEOUT_MS:
        state, duty = "FAULT", 0

def on_fault(now, cmd, pressed):
    global state, duty
    duty = 0
    if pressed:
        state = "IDLE"

HANDLERS = {"IDLE": on_idle, "TELEOP": on_teleop, "FAULT": on_fault}

while True:
    now = time.ticks_ms()
    cmd = None
    # A teaching serial port can be sys.stdin; the lab section shows one pattern.
    level = btn.value()
    pressed = level == 0 and prev_btn == 1
    prev_btn = level
    HANDLERS[state](now, cmd, pressed)
    apply()
    time.sleep_ms(1)
```

The dictionary is the point of the Python version: `HANDLERS[state]` is one function. An `if`/`elif` on `state` is equally acceptable and sometimes easier to read in a first draft. What is not acceptable is a `SLEEP` state whose body calls `time.sleep` or `delay`. Sleep is not a state of the robot. It is a hole in the clock. The exercise at the bottom asks you to notice that trap before it lands in the driving sketch.

Command letters stay small on purpose. `F` is "both wheels forward at the practice duty," which on a differential-drive base is a straight line. `S` is "I asked you to stop," which is IDLE, not FAULT. FAULT is reserved for the case where the operator's stream vanished. Mixing those up makes a deliberate stop look like a fault that then needs a button, or it makes a dead radio look like a clean park. The trace in the next section uses the longer phrase `F 40` so the duty is visible in the sentence; the lab's single letter `F` is that same command with the 40% baked in, because typing on a serial monitor is clumsy enough.

Later, a micro-ROS client can deliver the same events this machine already understands. A velocity topic is just a source of `F`-like commands with a richer payload. The firmware does not need a new timeout story when that client arrives; it needs the client to refresh `lastCmd` and the states you wrote here to keep forcing PWM to 0. The project site [micro.ros.org](https://micro.ros.org/) is where that client is documented. One sentence of foreshadow is enough until the ROS chapter.

## Worked example

Start in IDLE. The LED is off, and both conceptual channels are duty 0. At $t = 0$ the monitor receives `F 40`. The command event fires, the state becomes TELEOP, `lastCmd` is 0, and the duty becomes 40% of full scale. On the 8-bit LEDC range that is $0.40 \times 255 = 102$. The LED turns on. Channel A and channel B would both be 102 if the driver were attached. It is not.

No further characters arrive. The age of the command is $t - 0$. The timeout comparison uses the same threshold as Lesson 1:

$$
t - t_{\text{cmd}} \ge 300\,\mathrm{ms}.
$$

On the first loop pass where that predicate is true, the state becomes FAULT and the duty is stored as 0. The LED turns off. A late `F` typed during FAULT does not leave FAULT and does not restore 102. The operator presses the button. The button event moves the machine to IDLE. Duty is still 0, so the LED stays off until a new `F` arrives while the machine is in IDLE.

If the loop had called `delay(200)` inside TELEOP, the worked example of Lesson 1 applies unchanged: the first chance to notice 300 ms is at 400 ms, and the LED (and later the TB6612) would stay at duty 102 for that extra 100 ms. The state diagram's arrow is labeled 300 ms. The code has to be able to see that arrow, which means the loop keeps running.

## Hands-on lab

No motor, no VM, no battery. The LED is "motors enabled." The serial monitor is the joystick.

1. Flash the C++ listing, or extend the Python handlers with the USB serial read you already used in Chapter 02 so a typed letter fills `cmd`. Confirm the boot line says IDLE and the LED is dark.
2. Type `F`. The LED lights, and a print you add should say TELEOP and show duty 102, or 40 in the Python version. Type `S`. The LED goes dark and the state returns to IDLE. That is an operator stop, not a fault.
3. Type `F` again and then type nothing. Within about 300 ms the LED must go dark and the state must read FAULT. If it stays lit, the timestamp is not being read, or a sleep is longer than the timeout. Type `F` during FAULT and confirm the LED stays dark.
4. Press the button. The state returns to IDLE and the duty remains 0. Only a new `F` after that may light the LED.
5. In your notes, sketch the three bubbles and the silence arrow, and write the sentence "PWM is zero in FAULT." The checklist asks for both.

If the LED turns on the moment the sketch boots, `apply` is not gated on TELEOP, or `setup` wrote a duty and the loop never rewrote it. That bug is the subject of the chapter checklist.

## Exercises

1. Walk this trace and name the state and the duty after each event: boot; `F`; 300 ms of silence; `F` again with no button; button; `F`.
2. A classmate adds `Mode::Sleep` and calls `delay(1000)` inside that branch "so the robot rests." Explain which event the machine can no longer see, and what the TB6612 does during the delay if the last duty was nonzero.
3. Why must a command received in FAULT be ignored, instead of treated as proof that the link is healthy?
4. Rewrite the two-boolean loop so a single variable makes "blink while driving" impossible. You only need to describe the variable and which state, if any, owns the LED.

<details>
<summary>Hints</summary>

1. IDLE duty 0; TELEOP duty 102 (or 40%); FAULT duty 0; still FAULT duty 0 after the second `F`; IDLE duty 0 after the button; TELEOP duty 102 after the last `F`.
2. During `delay(1000)` the 300 ms silence arrow is not evaluated. If SLEEP does not force duty 0 before sleeping, both channels keep the previous command for a full second.
3. FAULT means a human must acknowledge. A burst of bytes after a dropout would otherwise resume motion with nobody holding the joystick.
4. One `Mode` value, with the LED written only in the TELEOP branch of `apply`. Delete `blinkMode` and `motorsOn`.

</details>

## Further reading

- [`millis()`](https://www.arduino.cc/reference/en/language/functions/time/millis/) is the clock inside the C++ timeout comparison. Unsigned subtraction is what makes `now - lastCmd` honest across wrap.
- [micro-ROS](https://micro.ros.org/) is the client that will eventually deliver the commands this machine already treats as events. The timeout stays on the microcontroller.
