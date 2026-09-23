---
layout: post
title: "Lab — blink, serial, and a robot heartbeat"
chapter: "02"
order: 4
owner: "Nguyen Le Linh"
lang: en
categories: [chapter02]
lesson_type: required
draft: false
---

## Objectives

You will show that the toolchain from the previous lab is still alive, and you will replace a blocking blink with a loop that can do more than one job. You will toggle an LED every 250 ms and print a heartbeat line every 500 ms containing the millisecond time and the LED state. You will write that loop with `millis()` on an ESP32 or `time.ticks_ms()` on a Pico, and you will run only the listing that matches your board. You will explain why `delay(1000)` or `time.sleep` cannot sit in the way of a later 300 ms stop. You will recognize a reset loop, a wrong LED pin, and a monitor left at 9600.

## Prerequisites

ESP32 track: a finished upload from the PlatformIO or Arduino IDE lesson, a port you can name, and 115200 agreed on both sides. Pico track: MicroPython on the board, Thonny or `mpremote` aimed at the Pico, and a lamp that already answered to `Pin("LED")` or GPIO 25. You need one of those two setups. No driver, no battery, no chassis. If your cable was marginal, this is the lab that will show it.

## Why it matters for Capstone A

Chapter 07’s teleop loop is this heartbeat with the LED replaced by a left-wheel duty and a right-wheel duty on a TB6612. The timestamp is how you prove the loop is running at the rate you think. The same loop has to notice that no fresh command arrived for about 300 ms and write both duties to zero. Wheels stay up the first time those duties are allowed to be non-zero. A sketch that spends its time inside `delay(1000)` cannot see the silence until the delay returns, so the wheels keep the last PWM for up to a second after the operator has already let go. Chapter 08 can move the same commands onto Wi-Fi later. The timeout still has to be a comparison in this loop, not a pause.

## Two timers, no blocking wait

A heartbeat here is a line the firmware emits on a schedule whether or not you are typing. The LED changes every 250 ms. A full on-off cycle is therefore 500 ms, which is 2 Hz:

$$
T_{\text{blink}} = 2 \times 250\,\mathrm{ms} = 500\,\mathrm{ms}, \qquad f = \frac{1}{0.5\,\mathrm{s}} = 2\,\mathrm{Hz}.
$$

The serial line is printed every 500 ms and carries two fields: the millisecond clock, and the LED state as 0 or 1. You should see about two lines per second. Watch the lamp for five seconds and count complete flashes. About ten flashes is the 2 Hz blink. About ten lines in those five seconds is the matching serial rate, because the print period is also 500 ms.

There is a sampling catch worth seeing once. The print period is exactly two toggles. If both timers start together and you print the state just after a toggle, the printed column can repeat the same value even while the lamp is flashing. Judge the blink with your eyes. Judge the scheduler with the millisecond column: it should climb by about 500 each line. The sketch below prints on the 500 ms timer after the 250 ms toggle has been applied, and the worked log shows what that looks like on a real run. If your state column sits still, the lamp is still the evidence of the 250 ms edge. You can move the print onto every toggle later; do not “fix” it by inserting `delay`.

The clock source differs by board and the meaning does not. On the ESP32 Arduino core, `millis()` counts milliseconds since boot. It wraps after

$$
2^{32}\,\mathrm{ms} \approx 49.7\,\text{days},
$$

which you will not hit this week. Unsigned subtraction `now - last` still works across that wrap if both values are `uint32_t`. On the Pico, `time.ticks_ms()` also counts milliseconds, and the legal subtraction is `time.ticks_diff(now, last)`. A raw Python minus will lie when the counter wraps. Either number, climbing by roughly 500 each printed line, is the evidence you want. A number that jumps back to a small value, especially if a boot banner is printed again, means the chip reset.

`delay(1000)` is the pattern this lab retires. While `delay` runs, the CPU does not evaluate `now - lastCmdMs > 300`. A stop that became due 50 ms into the delay is applied 950 ms late. The same is true of `time.sleep(1)` on the Pico. The non-blocking loop checks the inequality every pass. The extra motion after a timeout is one pass through `loop`, far under 300 ms, instead of the length of the sleep. The motor line is still a comment. There is no driver on the bench.

Run the listing for your board. Reading the other listing tells you what the other bench is seeing. Flashing both onto two boards in one sitting is how notes get crossed.

ESP32, Arduino core. Change the pin if your silk disagrees with GPIO 2. If the board package defines `LED_BUILTIN` and that macro is the real lamp, you may use it; the constant below is the explicit form.

```cpp
const int kLedPin = 2;  // DevKit V1 often uses GPIO 2; confirm the silk
const uint32_t TOGGLE_MS = 250;
const uint32_t BEAT_MS = 500;

bool ledOn = false;
uint32_t lastToggle = 0;
uint32_t lastBeat = 0;

void setup() {
  pinMode(kLedPin, OUTPUT);
  Serial.begin(115200);
  lastToggle = millis();
  lastBeat = millis();
  Serial.println("heartbeat");
}

void loop() {
  uint32_t now = millis();

  if (now - lastToggle >= TOGGLE_MS) {
    lastToggle = now;
    ledOn = !ledOn;
    digitalWrite(kLedPin, ledOn ? HIGH : LOW);
  }

  if (now - lastBeat >= BEAT_MS) {
    lastBeat = now;
    // ms, state. Later, both wheel duties follow this same clock.
    // A 300 ms command timeout is another comparison here, not a delay.
    Serial.printf("%lu,%d\n", static_cast<unsigned long>(now), ledOn ? 1 : 0);
  }

  // Capstone A, not today:
  // if (now - lastCmdMs > 300) { both TB6612 duties = 0; }
}
```

Pico, MicroPython. `"LED"` covers Pico W and Pico 2 W. GPIO 25 covers an original Pico and a non-W Pico 2 when the alias is missing.

```python
from machine import Pin
import time

try:
    led = Pin("LED", Pin.OUT)   # Pico W, Pico 2 W
except ValueError:
    led = Pin(25, Pin.OUT)      # original Pico, Pico 2

TOGGLE_MS = 250
BEAT_MS = 500
led_on = False
last_toggle = time.ticks_ms()
last_beat = time.ticks_ms()

print("heartbeat")
while True:
    now = time.ticks_ms()
    if time.ticks_diff(now, last_toggle) >= TOGGLE_MS:
        last_toggle = now
        led_on = not led_on
        led.value(1 if led_on else 0)
    if time.ticks_diff(now, last_beat) >= BEAT_MS:
        last_beat = now
        # ms, state. A 300 ms timeout belongs beside this test.
        print(now, led_on)
    # later: if time.ticks_diff(now, last_cmd) > 300: both duties = 0
```

Wheels-up is a sentence you write in the notes now, while no wheel is attached. It means the tires are not touching the desk when a command that could spin them is present. A robot that “just twitches” on the table walks off the table. The TB6612 and the battery stay in the parts box.

![Power order: logic first, motor supply last, wheels up]({{ site.imgurl }}/generated/power_order.png)

The figure is the sequence this heartbeat is rehearsing. USB and a quiet 3.3 V rail come first. A blink and a serial line are the proof. A driver and a battery are to the right of a line you have not crossed.

## A log you can audit

After the single `heartbeat` banner, copy ten lines. An ESP32 log from a healthy run, times in milliseconds:

```text
heartbeat
1840,0
2342,0
2843,0
3344,0
3846,0
4347,0
4848,0
5349,0
5851,0
6352,0
```

The absolute value of the first stamp depends on how long `setup` and the USB adapter delayed. The difference between lines should sit near 500 ms. A few milliseconds of jitter is normal. Both timers in the sketch start together, and 500 ms is exactly two toggles, so this print keeps landing on the same edge and the state column repeats. The lamp must still flash twice a second. That repeated column is a pass when the lamp is right. It is not a stuck pin. A return to a small timestamp, or a second `heartbeat` banner in the middle of the ten lines, means you recorded a reset. The lab is not passed until a later stretch of ten lines stays monotonic.

If the board resets and no motor is connected, suspect the cable or a short, not a driver you have not wired. A thin charge-only lead can make the port appear and then sag. A stray jumper from 3V3 to GND is a short and does the same thing. Unplug every jumper, swap the cable, and capture a clean block. Baud 9600 against a sketch at 115200 leaves the LED blinking and the pane full of garbage. Fix the monitor. A dark LED with a healthy millisecond column is the pin constant, not the toolchain: read the silk, and on a Pico W stop writing GPIO 25.

## Worked example

Dũng’s primary board is a classic ESP32 DevKit, silk LED on GPIO 2, CH340, monitor at 115200. The sketch is the C++ listing. The first session prints `heartbeat` twice in six seconds and the timestamps restart near 200 ms. No motor is attached. The cable is a charge-only lead that only sometimes enumerates. A data cable produces one banner and a staircase of about 501 ms. The lamp flashes twice a second. Ten lines go into `lab-notes.md`, plus the sentence “wheels up before any TB6612 command; VM and the battery are not connected.”

On the Pico bench the MicroPython listing is the one that runs. `Pin("LED")` works on a Pico W. `ticks_ms` climbs by about 500. The note says “Pico W, alias LED, GPIO 25 not used, wheels up, no motor.” Both benches have satisfied the gate. Neither bench flashes the other bench’s firmware.

The arithmetic Dũng writes in the margin is the reason `delay(1000)` left the file. A command that goes silent at $$t = 0$$ must force PWM to zero when $$t > 300\,\mathrm{ms}$$. Inside `delay(1000)` the comparison cannot run, so the last duty can survive until $$t = 1000\,\mathrm{ms}$$. The non-blocking loop evaluates the comparison on the next pass after 300 ms.

## Lab

1. Open the project that already uploads, or the MicroPython session that already blinks. Replace the blocking blink with the listing for your board. Do not paste the other language “as well.”
2. Confirm the LED pin: GPIO 2 or `LED_BUILTIN` only if the silk agrees; `Pin("LED")` or GPIO 25 as in the Pico lesson.
3. Start the monitor or the REPL at 115200 where a baud exists. You should see one `heartbeat` banner, then lines about every 500 ms, and a lamp flashing twice a second.
4. Copy ten lines into `lab-notes.md`. On the same page write the LED pin, the board name, and the wheels-up sentence. Name VM and the battery as pins and parts you are not using.
5. If the banner repeats, stop and fix the cable or a short before you edit the print.

Stop there. Do not add Wi-Fi, a driver, or a battery in order to make the log “more real.”

## Exercises

1. A full blink is 500 ms and the LED toggles every 250 ms. How many complete flashes do you expect in 4 seconds, and how many heartbeat lines?
2. Why can a state column that stays at `1` still be a passing blink? What do you watch instead?
3. A stop command is due 300 ms after the last packet. The loop is inside `delay(1000)`. What is the latest time at which the duties can actually reach zero, measured from the moment the timeout became true?
4. A log shows a second `heartbeat` between line 4 and line 5, and the millisecond field drops from 2600 to 180. No motor is wired. Name two causes that fit, and one cause that does not.
5. The monitor was left at 9600. The LED still flashes at 2 Hz. What do you change, and why is reinstalling the core the wrong first move?

<details>
<summary>Answers</summary>

1. Four seconds contain $$4 / 0.5 = 8$$ complete flashes, and $$4 / 0.5 = 8$$ heartbeat lines. The first line can be slightly late because of `setup` or the REPL. The spacing is the measurement.
2. The print period is an integer multiple of the toggle period, so a phase-locked sample can repeat one state. The lamp has to flash twice a second. The millisecond column has to step by about 500.
3. The comparison cannot run during the delay, so the write of zero can be as late as 1000 ms after the timeout became true. The non-blocking loop does that write on the first pass after 300 ms of silence.
4. Reset loop. On an unloaded board, suspect the cable or a short from a jumper, or an EN button that is bouncing. A motor on VM is not a cause you have earned yet, because VM is not connected.
5. Set the monitor to 115200 to match `Serial.begin`. The LED proves the sketch is running. Garbage at the wrong baud is not a failed chip.

</details>

## Where to buy in Vietnam

This lab buys nothing if the board and a data cable already work. If the heartbeat resets and the lead has never copied a file, replace it with the [Ugreen Micro-USB 1 m, 54 000 ₫](https://hshop.vn/cap-micro-usb-to-usb-2-0-dai-1m-cao-cap-60136-chinh-hang-ugreen). The dev board, if you still lack one, is the [NodeMCU-32S at 190 000 ₫](https://hshop.vn/kit-rf-thu-phat-wifi-ble-esp32-nodemcu-32s-ch340-ai-thinker) or the [Vietduino ESP32 at 265 000 ₫](https://hshop.vn/mach-phat-trien-vietduino-esp32), not the [bare ESP32-S3-WROOM-1 at 135 000 ₫](https://hshop.vn/mach-thu-phat-wifi-ble-soc-esp32-s3-esp32-s3-wroom-1-chinh-hang-espressif). Pico track: the search [raspberry pi pico](https://hshop.vn/search?q=raspberry+pi+pico) showed Pico 2 at 195 000 ₫ and Pico 2 W at 275 000 ₫ on 23 September 2026 ([Pico 2](https://hshop.vn/mach-raspberry-pi-pico-2-rp2350), [Pico 2 W](https://hshop.vn/mach-raspberry-pi-pico-2-w-rp2350)). Shopee: [ESP32 DevKit CH340](https://shopee.vn/search?keyword=esp32%20devkit%20ch340), [Pico 2](https://shopee.vn/search?keyword=raspberry%20pi%20pico%202). The full cart is [Chapter 00]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %}).

## Further reading

- [PlatformIO `esp32dev`](https://docs.platformio.org/en/latest/boards/espressif32/esp32dev.html) — the board id behind the Arduino listing, if that is your track.
- [arduino-esp32 installation](https://docs.espressif.com/projects/arduino-esp32/en/latest/installing.html) — the core that provides `millis` and `Serial`.
- [MicroPython on Pico](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html) — `machine.Pin` and `time.ticks_ms`.
- [Pico datasheet](https://datasheets.raspberrypi.com/pico/pico-datasheet.pdf) — confirm GPIO 25 before you trust a fallback on a non-W board.
