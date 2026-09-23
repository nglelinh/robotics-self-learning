---
layout: post
title: "C++ and MicroPython on a robot"
chapter: "03"
order: 1
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter03
lesson_type: required
draft: false
---

## Learning objectives

By the end of this lesson you can keep one heartbeat alive in both C++ and MicroPython without parking the CPU inside a long sleep, and you can point at the exact line that would make a 300 ms command timeout late. You will use `millis()` on the Arduino core and `time.ticks_ms()` together with `time.ticks_diff()` in MicroPython, which replaces the blocking `delay(500)` heartbeat from the [Chapter 02 blink and serial lesson]({% multilang_post_url contents/chapter02/02_04_blink_serial_hello %}). You will compute how a 200 ms sleep hides a 300 ms silence limit on a differential-drive base, and you will decide, for a new sensor versus the driving robot, which language you want while the timeout is still present in either one.

## Prerequisites

You already have a board that prints a climbing millisecond stamp and toggles an LED, from the Chapter 02 heartbeat. ESP32 students did that from PlatformIO; Pico students did it from the MicroPython REPL. You can change a pin number when the listing does not match the silk. You do not need PWM, interrupts, or a motor driver yet. What you are retiring is the habit at the bottom of that heartbeat: `delay(500)` or `time.sleep` for half a second was acceptable only while the sketch had nothing else to notice.

## Why it matters

Capstone A is a two-wheel differential-drive base. A teleop command eventually becomes two PWM signals on a TB6612, one for each wheel, and the firmware is the only place that can force both of those signals to zero when the commands stop. The rule you will implement later is short: if nothing valid arrives for 300 ms, both channels are commanded to 0, and the wheels stay up until that behavior has been watched. A language that cannot see the clock during that window will keep the last duty after the joystick has gone quiet. MicroPython and C++ can both finish Capstone A. The failure this lesson is about is a sleep that is "only" 200 ms, which is already long enough to step over the 300 ms mark.

## Core teaching

Both languages run on the microcontroller you flashed in Chapter 02. They share GPIO numbers, the 3.3 V logic rail, and the USB serial port. Capstone A does not require you to pick a personality. It requires a loop that keeps asking how old the last command is.

MicroPython keeps a read-eval-print loop on the chip. You paste a function, call it, and read the print before you commit to `main.py`. That edit cycle is the right tool while a sensor's wiring is still a guess. The cost sits in the runtime. A garbage collector sometimes pauses the program to reclaim memory. Those pauses are often a few milliseconds and sometimes a few tens of milliseconds. They are not a schedule you wrote. Joystick teleop in this course sits around 20 to 50 Hz. The periods are

$$
T_{20} = \frac{1}{20} = 50\,\mathrm{ms}, \qquad T_{50} = \frac{1}{50} = 20\,\mathrm{ms}.
$$

A short collector pause jitters one of those periods. It does not, by itself, pretend that 300 ms of silence has passed, provided the loop checks the timestamp again as soon as it runs. The same pause is a poor fit for bit-banged protocols at a high rate: a software-timed serial link or a tight sensor clock will drop edges while the collector runs. Do not use MicroPython for that job. Do use it for human-rate teleop if you refuse long sleeps.

C++ on the Arduino core, built in PlatformIO the way Chapter 02 did, compiles on your laptop and uploads a binary. There is no garbage collector in the language you are writing, and an interrupt is a function with a trigger you can name. That is why a later encoder is easier to reason about in C++. The cost is the edit cycle: a one-line change waits on a compile and an upload. That wait is acceptable for the driving robot. It is a bad reason to keep `delay()` in the control loop "because the upload already took long enough."

The heartbeat below is the same behavior in both languages. An LED toggles every 500 ms, and every other pass falls through so a future command check still runs. Arduino stores timestamps in an unsigned 32-bit count from `millis()`. Subtracting two `uint32_t` values is wrap-safe across the rollover at about 49.7 days. Do not put those timestamps in a signed `int`. MicroPython's `time.ticks_ms()` also wraps, on a modulus you must not guess, so the only legal elapsed-time question is `time.ticks_diff(now, last)`.

On many ESP32 MicroPython ports a completely tight `while True` starves the runtime and can trip the watchdog. A one-millisecond `time.sleep_ms(1)` at the bottom of the loop is a yield. It is not the bug. The bug is `time.sleep(0.2)`, `time.sleep(1)`, or `delay(200)`. Once motors exist, the control loop may block for only a few milliseconds. A 1 ms yield still evaluates a 300 ms timeout hundreds of times inside the window. A 200 ms sleep evaluates it on a grid that skips the deadline.

```cpp
const int LED_PIN = 2;  // the pin you already blinked in Chapter 02
const uint32_t BLINK_MS = 500;

uint32_t lastBlink = 0;
bool ledOn = false;

void setup() {
  pinMode(LED_PIN, OUTPUT);
  Serial.begin(115200);
  lastBlink = millis();
  Serial.println("heartbeat, non-blocking");
}

void loop() {
  uint32_t now = millis();
  if (now - lastBlink >= BLINK_MS) {
    lastBlink = now;
    ledOn = !ledOn;
    digitalWrite(LED_PIN, ledOn ? HIGH : LOW);
    Serial.printf("t=%lu led=%d\n", (unsigned long)now, ledOn ? 1 : 0);
  }
  // Command-age check belongs on this pass, including passes that do not toggle.
}
```

```python
from machine import Pin
import time

led = Pin(2, Pin.OUT)  # change to the Chapter 02 LED you already trust
BLINK_MS = 500
last = time.ticks_ms()
led_on = False

print("heartbeat, non-blocking")
while True:
    now = time.ticks_ms()
    if time.ticks_diff(now, last) >= BLINK_MS:
        last = now
        led_on = not led_on
        led.value(1 if led_on else 0)
        print("t", now, "led", 1 if led_on else 0)
    time.sleep_ms(1)  # yield only; never sleep(0.2) once a timeout exists
```

Read the two listings until the match is boring. Each stores a timestamp, asks a wrap-safe question, toggles only when the answer is yes, and otherwise falls through. That fall-through is where the 300 ms test will live. A practical split that has held up on this bench: prototype a new sensor in MicroPython while the wiring is still moving, and ship the driving robot in C++ if the timing gets flaky. Either language is acceptable for Capstone A when the timeout is actually in the loop.

## Worked example

The safety predicate for Capstone A is

$$
\text{cut both PWM channels if } t - t_{\text{cmd}} \ge 300\,\mathrm{ms}.
$$

Put a 200 ms sleep at the bottom of the loop and the predicate is only evaluated on a 200 ms grid. A command arrives at $t = 0$, which refreshes $t_{\text{cmd}}$. The loop then sleeps. The sample instants are 200 ms, 400 ms, 600 ms. At 200 ms the age is still under the limit, so the TB6612 keeps the previous duty. The next look is at 400 ms:

$$
t_{\text{stop}} = \left\lceil \frac{300}{200} \right\rceil \times 200 = 400\,\mathrm{ms}.
$$

The code does not observe the 300 ms mark. It wakes up already late by

$$
400 - 300 = 100\,\mathrm{ms}.
$$

During those extra 100 ms both wheels still have the last speed command, which is exactly the case the timeout exists to prevent. Comparing 200 with 300 and concluding "the sleep is shorter, so it is safe" compares the wrong pair. The sleep has to be a few milliseconds, short next to the 20 ms period of a 50 Hz stream, not merely shorter than the timeout. Ten missed command periods fit inside one 200 ms nap:

$$
\frac{200\,\mathrm{ms}}{20\,\mathrm{ms}} = 10.
$$

A garbage-collection pause of about 15 ms on an otherwise cooperative MicroPython loop is a different story. It can stretch one teleop period. It does not hide the 300 ms boundary, because the check runs again as soon as the pause ends. That is why a collector pause is acceptable at 20–50 Hz and a 200 ms sleep is not.

## Hands-on lab

Stay on the LED from Chapter 02. Do not add a motor, and do not wire a TB6612 in this lesson. You are measuring whether the loop can see a clock.

1. Load the listing that matches your board. On MicroPython, run it from the REPL before you save it as `main.py`. Confirm one boot line, then `t=...` lines about every 500 ms, with the LED following the `led` field. A second boot line means a reset, which Chapter 02 already taught you to treat as a fault rather than a blink.
2. Add a pass counter that prints once per second using the same non-blocking test, then clears. Write the count in your notes. That number is this sketch's iteration rate, not a universal constant. A MicroPython loop that yields 1 ms will land near 1000, and that is the yield you asked for.
3. Insert `delay(200)` or `time.sleep(0.2)` once per pass. Watch the LED and the counter. The cooperative rate collapses, and a 300 ms silence can only be noticed on the 200 ms grid from the worked example.
4. Remove the 200 ms call before you leave the bench. The file you keep is the non-blocking heartbeat. In your notes, record language, pin, iterations per second, and the sentence "a 200 ms sleep stops the robot at 400 ms."

## Exercises

1. Your cooperative loop completes 25000 passes in one second. How many of those passes disappear during a single `delay(200)`, and what is the first time at which a 300 ms silence test can succeed if it is only evaluated after each such delay?
2. A classmate's MicroPython blink is `time.sleep(0.5)` with a serial read after the sleep. Name the two clock calls that let the LED still toggle every 500 ms while the serial byte is inspected on every pass.
3. Commands are sent at 40 Hz and a collector pause of about 12 ms occurs once. Does that pause by itself force the stop rule? Would you accept the same pause while bit-banging a protocol whose bits are 8 µs wide?
4. You are bringing up a new distance sensor this afternoon, and the driving robot next week has started to miss its 300 ms cutoff under load. Which language do you reach for in each sitting, and what must already be true in both?

<details>
<summary>Hints</summary>

1. Pass time is $1/25000$ seconds, so a 0.2 s block erases $0.2 \times 25000$ passes. The silence test on a 200 ms grid first succeeds at 400 ms, the same ceiling used in the worked example.
2. Store `last = time.ticks_ms()`. Toggle when `time.ticks_diff(time.ticks_ms(), last) >= 500`, and read the byte on the passes that do not toggle. A `sleep_ms(1)` yield is optional. `sleep(0.5)` is the line you delete.
3. Twelve milliseconds is far under 300 ms, so one pause does not mean the link died. An 8 µs bit cannot survive a 12 ms stall. That is the bit-bang case MicroPython is the wrong tool for.
4. Prototype the sensor in MicroPython. Move the driving loop to C++ if the cutoff is already flaky. In both sittings the timeout has to be a real comparison against a timestamp, not a comment.

</details>

## Further reading

- [MicroPython ISR rules](https://docs.micropython.org/en/latest/reference/isr_rules.html) are the constraint you will hit the moment a callback replaces the REPL. The same page is why a later interrupt lesson forbids allocating inside the handler.
- [`millis()`](https://www.arduino.cc/reference/en/language/functions/time/millis/) documents the unsigned millisecond clock used in the C++ heartbeat, including the wrap at about 49.7 days.
- [PlatformIO](https://docs.platformio.org/) is the build path Chapter 02 already used for the ESP32 sketch. The longer compile is the trade you accept when you leave the REPL.
