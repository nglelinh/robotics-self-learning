---
layout: post
title: "Interrupts, debouncing, and short ISRs"
chapter: "03"
order: 4
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter03
lesson_type: required
draft: false
---

If your main loop checks an encoder pin only once every 10 milliseconds, a spinning wheel will fire 50 pulses while the CPU is looking the other way — and your robot's odometry will think it barely moved. **Hardware interrupts** solve this by letting an electrical edge tap the CPU on the shoulder the microsecond it happens. Yet interrupts come with a famous trap: put a `Serial.print()` or a floating-point calculation inside an Interrupt Service Routine (ISR), and your microcontroller crashes with a watchdog panic.

This lesson teaches the physics of mechanical contact bounce, the discipline of ultra-short ISRs, and thread-safe data sharing via `volatile` and critical sections.r

---

## Learning objectives

By the end of this lesson you can separate a contact's mechanical bounce from a real press, and you can put only a flag update inside an interrupt service routine. You will attach a button on `CHANGE` or `FALLING`, let the main loop time a 20 ms stability window, and show that one physical press increments a counter by one. You will also explain why `delay()` inside that ISR freezes every other interrupt, and what a future encoder ISR is allowed to do: increment a `volatile uint32_t` and return.

## Prerequisites

The GPIO lab already wired a button from the pin to ground with the pull-up enabled, and it already rejected a change that had not been stable for 20 ms. That version polled. This lesson moves the "something happened" event into an interrupt and leaves the stability test in the loop you built in Lesson 1, the same non-blocking clock that replaced the [Chapter 02 `delay(500)` heartbeat]({% multilang_post_url contents/chapter02/02_04_blink_serial_hello %}). You need the button you already have. You do not need a new part, and you still do not connect a motor.

## Background Knowledge Map: Hardware Interrupts, Contact Bounce Physics, and Atomic Concurrency

Three low-level systems concepts keep interrupt-driven robot firmware rock-solid:

- **Polling vs. Edge-Triggered Interrupts:** Polling checks a pin on the CPU's schedule (fine for slow human buttons); hardware interrupts (`RISING`, `FALLING`, `CHANGE`) jump immediately into an ISR within microseconds (essential for high-speed encoders and safety limits).
- **Mechanical Switch Bounce:** Inside a pushbutton or limit switch, spring metal contacts physically rebound for $$2\text{–}15\text{ ms}$$ after impact, generating 5–20 spurious digital edges from a single press. Software debouncing (ignoring edges within a lockout window $$T_{\text{db}}$$) or an RC hardware filter turns that chatter into one clean event.
- **Atomicity, `volatile`, and Critical Sections:** Because an ISR can preempt the main loop between two assembly instructions, any shared variable must be declared `volatile` (preventing compiler caching in a register), and multi-byte reads/writes (like a 32-bit encoder count on an 8-bit CPU, or reading two encoder counts together) must happen inside a brief interrupt-disabled critical section.r

---

## Why it matters

Capstone A clears FAULT with a button and, later, counts wheel encoders while teleop duties are being updated. If the button ISR prints, allocates, or calls `delay`, it holds off the loop that is supposed to notice 300 ms of command silence and force both TB6612 channels to 0. A bouncing contact makes the opposite bug: one finger tap looks like five to thirty edges, so a "clear fault" gesture retriggers, or an encoder count runs away while the robot is standing still with its wheels up. The ISR has to be short enough that the timeout loop still gets the CPU, and the debounce has to live where a millisecond clock is legal.

## Core teaching

A mechanical switch does not close once. The contacts strike, rebound, and strike again. For the buttons in this course that chatter usually lasts somewhere in a 10 ms to 50 ms window, which is why the GPIO lab picked 20 ms as a default inside that range. During the window the pin can produce a burst of edges. An interrupt on each edge will run the ISR once per edge. A human still believes they pressed once.

![Contact bounce, then a stable level]({{ site.imgurl }}/generated/debounce_timeline.png)

An interrupt service routine, the ISR, is the function the hardware calls when the pin matches the trigger you armed. It preempts the main loop. That is the feature: a short pulse cannot hide between two polls if the poll period is longer than the pulse. It is also the constraint. While the ISR runs, other interrupt work waits, and on a single core your loop does not. The routine therefore stays tiny. Set a `volatile` flag or increment a `volatile` counter, and return. `volatile` tells the compiler that the main loop must actually reload the variable, because the ISR writes it behind the compiler's back. Do not call `Serial.print` in the ISR. Do not allocate, do not build a `String`, and do not touch Python objects if you are on MicroPython. The [MicroPython ISR rules](https://docs.micropython.org/en/latest/reference/isr_rules.html) are blunt about heap allocation inside a handler, and the same discipline saves the Arduino sketch from a print that needs the UART interrupt you are currently blocking.

The main loop is where time is allowed to pass. It clears the flag, then applies the same 20 ms stability rule as the GPIO lab: the raw reading must hold still before a press is counted. Arm the pin on `FALLING` if you only care about the press of a pull-up button, or on `CHANGE` if you also want the release. `FALLING` matches pressed-means-LOW. `CHANGE` will also see the bounce on the way up, which the stability test then has to reject.

A future encoder can count in the ISR, and that is a good use of the mechanism, provided the ISR only does

```cpp
volatile uint32_t encCount = 0;

void IRAM_ATTR onEnc() {
  encCount++;
}
```

No floating-point speed estimate, no serial, no debounce-by-delay. The loop reads `encCount` into a local, computes speed, and updates PWM. `IRAM_ATTR` on ESP32 places the ISR in internal RAM so a flash operation cannot stall it. Use it on the Arduino ESP32 core.

The bug to refuse is debounce performed inside the ISR with `delay`:

```cpp
void IRAM_ATTR badIsr() {
  delay(20);              // blocks the core; other ISRs wait
  if (digitalRead(BTN) == LOW) {
    pressFlag = true;
  }
}
```

`delay` itself depends on the timekeeping interrupt. Calling it from an ISR stops the clock that `delay` is waiting on, or at best freezes every handler that would have noticed a command pin, a UART byte, or the other encoder channel. Even a "working" busy-wait of 20 ms inside the ISR means the 300 ms silence check cannot run during the bounce, and two encoders will lose edges for the whole wait. The flag-and-loop split exists so the ISR returns in a microsecond and the loop does the waiting without disabling the rest of the chip.

Arduino C++. The counter increases only after the line has been LOW, stably, for 20 ms following a falling interrupt. GPIO 4 is the button from the GPIO lab.

```cpp
const int BTN = 4;
const uint32_t DEBOUNCE_MS = 20;

volatile bool fell = false;

int stable = HIGH;
uint32_t lastChange = 0;
uint32_t presses = 0;

void IRAM_ATTR onFall() {
  fell = true;  // nothing else
}

void setup() {
  pinMode(BTN, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(BTN), onFall, FALLING);
  Serial.begin(115200);
  lastChange = millis();
  Serial.println("presses=0");
}

void loop() {
  uint32_t now = millis();
  int raw = digitalRead(BTN);

  static int lastRaw = HIGH;
  if (raw != lastRaw) {
    lastRaw = raw;
    lastChange = now;
  }

  if (fell) {
    fell = false;  // consumed; the stability test still decides
  }

  if ((now - lastChange) >= DEBOUNCE_MS && raw != stable) {
    stable = raw;
    if (stable == LOW) {
      presses++;
      Serial.printf("presses=%lu\n", (unsigned long)presses);
    }
  }
}
```

The interrupt's job is to record that a falling edge was seen. The count is printed from the loop, one line per accepted press. If you want the ugly comparison, comment out the `DEBOUNCE_MS` test and increment on every consumed `fell` flag. One click then prints several times. Students on this hardware commonly see a burst of about 5 to 30 counts for a single press when the stability window is removed. Your button may land anywhere in that band. Write the number you actually see.

MicroPython's handler has the same shape. The callback sets a global flag and does not allocate. Debounce stays in the loop. Prefer a preallocated integer and a boolean; do not build a list or a formatted string inside the handler.

```python
from machine import Pin
import time

fell = False

def on_fall(pin):
    global fell
    fell = True

btn = Pin(4, Pin.IN, Pin.PULL_UP)
btn.irq(trigger=Pin.IRQ_FALLING, handler=on_fall)

DEBOUNCE_MS = 20
last_raw = 1
stable = 1
last_change = time.ticks_ms()
presses = 0
print("presses=0")

while True:
    now = time.ticks_ms()
    raw = btn.value()
    if raw != last_raw:
        last_raw = raw
        last_change = now
    if fell:
        fell = False
    if time.ticks_diff(now, last_change) >= DEBOUNCE_MS and raw != stable:
        stable = raw
        if stable == 0:
            presses += 1
            print("presses", presses)
    time.sleep_ms(1)
```

`Pin.IRQ_FALLING` is the MicroPython spelling of the same trigger. `Pin.IRQ_RISING | Pin.IRQ_FALLING` is `CHANGE`. Printing inside `on_fall` looks convenient and will eventually throw or corrupt the heap. If a lab partner says the interrupt "randomly dies," look for an allocation in the handler before you look for a bad solder joint.

## Worked example

A press produces edges at $t = 0, 3, 7, 12$ ms and is then solidly LOW until the release. Without a stability test the `FALLING` ISR runs four times, and a chatty switch in the 5–30 band simply has more edges in that same 10–50 ms window. The counter prints 4, or 17, or 30, for one finger motion. With the 20 ms rule the raw level is not accepted until it has been constant since the last edge. The last falling edge is at 12 ms, so the level is trusted at 32 ms, and `presses` increases by 1. The three earlier edges restarted the timer and never became their own counts.

Release chatter is ignored for the count because the listing only increments on a stable LOW. It still must not block. A `delay(20)` inside the ISR at $t = 0$ would sit in the handler until 20 ms, missing any other interrupt in that window and postponing the loop's 300 ms command check by the same 20 ms plus whatever else was queued. Twenty milliseconds is not the full timeout, but it is a hole you punched in the only loop allowed to cut PWM. The encoder version of this arithmetic is stricter: edges 200 µs apart cannot wait behind a 20 ms debounce delay, which is why the encoder ISR only increments.

## Hands-on lab

Use the button wiring from the GPIO lesson. USB only. No motor terminal on the pin.

1. Flash the debounced listing. Press ten times at about one press a second. The serial log should show `presses=1` through `presses=10`, and the final number should match your finger with error zero. If you are off by one, you double-counted a release or the contact never went stable.
2. Bypass the 20 ms test so each consumed falling flag increments the counter. Press once, firmly. Expect a jump of several counts, typically somewhere from 5 to 30. Paste both logs into your notes: the matched count, and the burst.
3. Do not "fix" the burst by putting `delay(20)` in `onFall`. Read the bad listing in the core section again and write one sentence in your notes: the wait belongs next to `millis()` or `ticks_diff`, not in the ISR.
4. Optional: move the trigger to `CHANGE` and confirm that a sloppy stability test now also reacts to the release burst. The count should still grow by one per press if you only increment on stable LOW.

## Deep-Dive Explanation (Read Slowly): Designing a Crash-Proof Encoder ISR and Software Debouncer

Follow these four ironclad rules whenever you write an ISR in robotics firmware:

1. **Keep the ISR under ~2–5 microseconds:** Increment/decrement a counter, record a timestamp, or set a `volatile bool` flag — *never* call `Serial.print()`, `delay()`, `malloc()`, or I2C reads inside an ISR.
2. **Place ESP32 ISRs in RAM (`IRAM_ATTR`):** Flash cache can be disabled during flash writes; marking the ISR `IRAM_ATTR` keeps it executable from SRAM at all times.
3. **Copy and zero/snapshot atomically in the main loop:** Briefly disable interrupts (`noInterrupts()` / `portENTER_CRITICAL`), copy `int32_t c = enc_count;`, and re-enable interrupts immediately.
4. **Separate button debouncing from encoders:** Optical/Hall encoders do *not* bounce mechanically (never add a 20 ms debounce to an encoder, or you will cap wheel speed below 50 pulses/s!).

### Concrete Worked Example: Why a 20 ms Debounce Destroys an Encoder — and How to Snapshot Safely

Suppose your wheel encoder outputs $$2\,000\text{ pulses/s}$$ at cruising speed, while a front bumper microswitch bounces for up to $$8\text{ ms}$$:

- **Step 1 — Time between consecutive encoder edges:**
  $$\Delta t_{\text{enc}} = \frac{1}{2\,000\text{ Hz}} = 0.5\text{ ms} = 500\,\mu\text{s}.$$
  If you accidentally applied a $$20\text{ ms}$$ software debounce to that encoder pin, it would discard 39 out of every 40 real edges (capturing at most $$1/0.02 = 50\text{ edges/s}$$ — losing **97.5%** of your robot's distance!).
- **Step 2 — Correct bumper switch debounce window:**
  Choosing $$T_{\text{db}} = 20\text{ ms} > 8\text{ ms}$$ (2.5× the worst-case bounce duration) filters 100% of switch chatter, while a robot cruising at $$0.30\text{ m/s}$$ moves only $$0.30 \times 0.02 = 6\text{ mm}$$ during confirmation.
- **Step 3 — Atomic delta calculation in a 100 Hz control loop ($$\Delta t = 0.01\text{ s}$$):**
  At tick $$k-1$$, snapshot `c_prev = 10420`. At tick $$k$$, snapshot `c_now = 10440`.
  $$\Delta c = 10\,440 - 10\,420 = 20\text{ counts} \implies \text{rate} = \frac{20}{0.01} = 2\,000\text{ counts/s}.$$
  Notice that taking differences (`c_now - c_prev`) *without* resetting `enc_count = 0` avoids losing an edge that arrives between reading and zeroing!

**Common Pitfall:** Writing `count = enc_count; enc_count = 0;` outside a critical section — if an encoder edge fires right between those two lines, that tick is silently erased forever. Always snapshot without zeroing and subtract `c_now - c_prev`.

**Quick Check:** An `int32_t` encoder counter holds up to $$\pm 2.147 \times 10^9$$ counts. At $$10\,000\text{ counts/s}$$, it would take $$2.147 \times 10^9 / 10\,000 \approx 2.48\text{ days}$$ of nonstop full-speed spinning in one direction to overflow!

---

## Exercises

1. One press produces falling edges at 0, 2, 5, 9, 14, and 18 ms, then stays LOW. How many counts does the bare ISR produce, and at what time does the 20 ms rule accept the press?
2. Why does `Serial.println` inside `onFall` break the "short ISR" rule even when the sketch appears to work for a few clicks?
3. A quadrature encoder will later need a count. Which of these belongs in the ISR: adding one to a `volatile uint32_t`, computing revolutions per minute with floating point, or calling `ledcWrite`?
4. Two buttons are armed, and button A's ISR calls `delay(20)`. A falling edge arrives on button B 4 ms later. When does B's ISR run, and what does that imply for a 300 ms PWM cutoff that lives in the main loop?

<details>
<summary>Hints</summary>

1. Six falling edges become six counts if nothing filters them. The last edge is at 18 ms, so the stable LOW is accepted at 38 ms and the filtered count is 1.
2. `Serial` needs buffers and often the UART interrupt. Doing that work inside the button ISR lengthens the handler and can deadlock against the interrupt it needs. Set a flag; print in `loop`.
3. Only the increment belongs in the ISR. Speed math and PWM updates read the counter from the loop.
4. B waits until A's `delay(20)` returns, so B runs about 16 ms late. The main loop, including the silence check, is also stalled for those 20 ms.

</details>

## Further reading

- [`attachInterrupt`](https://www.arduino.cc/reference/en/language/functions/external-interrupts/attachinterrupt/) documents `FALLING`, `RISING`, and `CHANGE`, and the requirement that the service routine be short.
- [MicroPython ISR rules](https://docs.micropython.org/en/latest/reference/isr_rules.html) are the matching constraint for the callback version: no heap, no long work, schedule the real handling in the main loop.
