---
layout: post
title: "Lab — GPIO patterns for buttons and LEDs"
chapter: "03"
order: 2
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter03
lesson_type: required
draft: false
---

## Learning objectives

By the end of this lab a button wired from a GPIO to ground reads HIGH when released and LOW when pressed, because the pin mode is `INPUT_PULLUP` or the MicroPython equivalent. You will size the LED's series resistor from the 3.3 V rail, build the same edge-printing sketch in Arduino C++ and in MicroPython, and accept a level change only after the raw reading has been stable for 20 ms. You will recognize three classic faults: a floating input when the pull-up was forgotten, an LED with no resistor, and a button hung between 3.3 V and the pin with no pull-down so the reading never leaves HIGH. Nothing in the sketch drives a motor.

## Prerequisites

The [Chapter 02 heartbeat]({% multilang_post_url contents/chapter02/02_04_blink_serial_hello %}) already proved that your serial monitor matches the board at 115200 and that you can change an LED pin when GPIO 2 is not the lamp on your silk. Lesson 1 of this chapter replaced `delay(500)` with a non-blocking clock; the sketches below keep that habit. You need a breadboard, a momentary button, one LED, a resistor near 180 Ω, and jumpers. You do not need the TB6612, a battery, or the chassis.

## Why it matters

Capstone A will treat a button as a human event: clear a fault, or confirm that you meant to leave the stopped state. Teleop commands will arrive later as bytes and then as ROS messages, but the electrical pattern under the button does not change when those bytes show up. If the pin floats, the firmware invents presses and can clear a fault you never acknowledged. If the LED is the stand-in for "I saw the edge," a missing series resistor makes that stand-in a short. The wheels stay up, and the motor stays off the GPIO, because a wheel driver is a separate chip. This lab is the input and the lamp only.

## Core teaching

A GPIO is a digital pin that is either an input or an output. As an input with the internal pull-up enabled, the pin is weakly tied to 3.3 V. The button's other side goes to ground, not to 3.3 V. While the button is released the switch is open, the pull-up wins, and `digitalRead` returns HIGH. While the button is pressed the switch is a short to ground, which is stronger than the pull-up, and the read returns LOW. That inversion surprises people who expect "pressed means true means HIGH." In this wiring, pressed means LOW. Write the comment in the sketch so future you does not "fix" it.

![Button to ground with the GPIO pull-up]({{ site.imgurl }}/generated/gpio_pullup_button.png)

If the chip has no internal pull-up, copy the same idea with a 10 kΩ resistor from the GPIO to 3.3 V, and still wire the button from the GPIO to ground. Ten kilohms is stiff enough that a finger on the wire does not define the level, and gentle enough that a pressed button only has to sink $3.3 / 10000 = 0.33$ mA.

The LED needs its own series resistor. A small indicator LED drops about 2.0 V when it is lit, and 8 mA is a bright, safe target from a 3.3 V GPIO. Ohm's law on the resistor, which sees the leftover voltage, is

$$
R = \frac{V_{CC} - V_F}{I_F} = \frac{3.3 - 2.0}{0.008} = 162.5\,\Omega.
$$

The common part in a 1/4 W kit is 180 Ω, which runs the LED a little under the target:

$$
I = \frac{3.3 - 2.0}{180} \approx 7.2\,\mathrm{mA}, \qquad P = I^2 R \approx 9\,\mathrm{mW}.
$$

A 1/4 W resistor is nowhere near warm. A 220 Ω part is also fine and only slightly dimmer. Leaving the resistor out asks the GPIO to limit the current by itself. It will not do that politely: the LED or the pin pad is what fails. The cathode of the LED goes toward ground, the anode toward the resistor, and the resistor toward the GPIO. The GPIO sources the current. Stay on the 3.3 V rail. ESP32 pins are not a place to attach the 5 V pin, and they are not a place to attach a motor.

![LED, series resistor, and ground]({{ site.imgurl }}/generated/led_series_resistor.png)

Contacts do not close in one clean edge. The next lesson photographs that chatter. Today you only need a loop rule that refuses to believe a change until the raw bit has held still for 20 ms. Keep the last raw sample and the time it changed. If the raw value is new, restart the timer. If the raw value has matched itself for 20 ms and it differs from the accepted level, accept it and print one line. Printing every sample floods the monitor and hides the edge you care about. The serial log should say `press` on the falling accepted edge and `release` on the rising accepted edge, once each.

The same rule is the debounce you will reuse when an interrupt merely sets a flag. Doing it in the loop now means you can single-step it with a print. Do not `delay(20)` to implement it. A blocking wait freezes the heartbeat from Lesson 1 for the whole bounce window, and once a motor command exists that wait is the 200 ms problem again, only shorter. Twenty milliseconds of blind time is still the wrong shape. The timestamp test leaves the loop free.

Three faults show up every term.

A floating pin is what you get when the button goes to ground and you forget `INPUT_PULLUP` or `Pin.PULL_UP`. Released, the wire is an antenna. The monitor prints press and release with nobody touching it. Fix the mode before you rewrite the debounce.

An LED with no series resistor may light once, very brightly, and then never again. If it survives, the pin is still being asked for more current than the pad is rated for. Put the 180 Ω part in series even if the lamp "looks fine."

A button wired from 3.3 V to the GPIO, with the pull-up left on and no pull-down to ground, reads HIGH when released because of the pull-up and HIGH when pressed because the switch connects 3.3 V. There is no edge. Students describe this as "the button does nothing." The pin is not broken. Both states are the same voltage. Move the switch to ground, or add a pull-down and stop using the internal pull-up. This course uses the ground wiring.

Do not drive a motor, a relay coil, or the TB6612's VM pin from a GPIO. A GPIO can signal a driver's PWM input later. It cannot be the motor current.

Arduino C++ for an ESP32. Button on GPIO 4, LED on GPIO 18. Both pins avoid the strapping set discussed in the PWM lesson.

```cpp
const int BTN = 4;
const int LED = 18;
const uint32_t DEBOUNCE_MS = 20;

int lastRaw = HIGH;
int stable = HIGH;
uint32_t lastChange = 0;

void setup() {
  pinMode(BTN, INPUT_PULLUP);  // released HIGH, pressed LOW
  pinMode(LED, OUTPUT);
  Serial.begin(115200);
  lastChange = millis();
  Serial.println("gpio edges");
}

void loop() {
  uint32_t now = millis();
  int raw = digitalRead(BTN);
  if (raw != lastRaw) {
    lastRaw = raw;
    lastChange = now;
  }
  if ((now - lastChange) >= DEBOUNCE_MS && raw != stable) {
    stable = raw;
    digitalWrite(LED, stable == LOW ? HIGH : LOW);  // LED on while held
    Serial.println(stable == LOW ? "press" : "release");
  }
}
```

The LED in this listing follows the held state so you can see the button. The print happens only on the accepted edge.

MicroPython, same pins if you are on an ESP32 board. On a Pico, move the numbers to free GP pins and keep the pull-up.

```python
from machine import Pin
import time

btn = Pin(4, Pin.IN, Pin.PULL_UP)
led = Pin(18, Pin.OUT)
DEBOUNCE_MS = 20

last_raw = btn.value()
stable = last_raw
last_change = time.ticks_ms()
print("gpio edges")

while True:
    now = time.ticks_ms()
    raw = btn.value()
    if raw != last_raw:
        last_raw = raw
        last_change = now
    if time.ticks_diff(now, last_change) >= DEBOUNCE_MS and raw != stable:
        stable = raw
        led.value(1 if stable == 0 else 0)
        print("press" if stable == 0 else "release")
    time.sleep_ms(1)
```

## Worked example

You press the button at $t = 1000$ ms and release it at $t = 1600$ ms. The raw pin chatters for 8 ms after each mechanical event and is then steady. The 20 ms rule waits until $t = 1020$ ms before it accepts LOW, prints `press`, and turns the LED on. It waits until $t = 1620$ ms before it accepts HIGH, prints `release`, and turns the LED off. Samples at 1 ms resolution never appear in the log. The monitor shows

```
gpio edges
press
release
```

and nothing else for that gesture. If your log instead shows dozens of lines for one click, the stability test is not wrapped around the print. If it shows nothing, measure the pin: released near 3.3 V, pressed near 0 V. A released pin that wanders between 0.8 V and 2 V is floating.

Suppose the forward voltage is 2.1 V and you want 5 mA from the same 3.3 V rail. The resistor is

$$
R = \frac{3.3 - 2.1}{0.005} = 240\,\Omega,
$$

so a 220 Ω or 270 Ω part from the kit is the honest choice. Reusing 180 Ω would run nearer $(3.3-2.1)/180 \approx 6.7$ mA, which is still safe and a bit brighter than you asked. The calculation is the point, not a single catalog number.

## Hands-on lab

Power the board from USB only. Do not connect a battery pack, and do not let any jumper touch a 5 V header.

1. Unplug USB. Place the button so one leg is GPIO 4 and the opposite leg is GND. Place the LED and the 180 Ω resistor in series between GPIO 18 and GND, anode toward the GPIO. Re-read the two figures before you plug USB back in.
2. Flash the C++ sketch or save the MicroPython script. Open the serial monitor at 115200. You want one `gpio edges` line, then silence.
3. Press and release once, slowly. Expected log: `press` then `release`. The LED lights only while the button is down. Press five times. You want five pairs, not a stream.
4. Delete the pull-up on purpose, run again, and watch the log invent edges. Put the pull-up back. That ten-second experiment is the floating-pin fault, and it belongs in your notes.
5. Record the pin numbers, the resistor value, and a paste of one clean press/release pair. Photograph the breadboard if you can. The checklist at the end of the chapter asks for this log.

If the LED is dark while `press` prints, the LED is backwards or on the wrong pin. Trust the serial line first, then turn the LED around. If `press` never prints and the pin measures 3.3 V in both positions, you have built the always-high fault: the switch is on the 3.3 V side.

## Exercises

1. A red LED is specified at $V_F = 1.8$ V and you budget $I_F = 6$ mA from 3.3 V. Compute $R$, then name the nearest common value you would actually solder, choosing the one that does not exceed 6 mA.
2. The stable level changes from HIGH to LOW at $t = 250$ ms and back to HIGH at $t = 900$ ms, with the 20 ms test already satisfied. Write the serial lines and the LED state in each interval. What must not appear between them?
3. A classmate wires the button from 3.3 V to GPIO 4, calls `pinMode(4, INPUT_PULLUP)`, and reports that the lamp never changes. State the voltage in both switch positions and the one wire you move.
4. The internal pull-up is unavailable. You have a 10 kΩ resistor and the same button. Describe the two nodes the resistor joins, and the current it carries while the button is held.

<details>
<summary>Hints</summary>

1. $R = (3.3 - 1.8) / 0.006 = 250\,\Omega$. A 270 Ω part stays under 6 mA. A 220 Ω part runs a little over the budget.
2. The log gains `press` at the first accepted edge and `release` at the second. The LED is on only while the accepted level is LOW. Samples between 250 and 900 ms do not print.
3. Both positions sit near 3.3 V, so the accepted level never changes. Move the button's far side from 3.3 V to GND and leave the pull-up enabled.
4. The resistor joins GPIO to 3.3 V. Held current is about $3.3/10\,\mathrm{k}\Omega = 0.33$ mA. The button's other side is still GND.

</details>

## Further reading

- [Arduino `pinMode`](https://www.arduino.cc/reference/en/language/functions/digital-io/pinmode/) lists `INPUT_PULLUP`, which is the whole reason a released button in this lab reads HIGH.
- [MicroPython `machine.Pin`](https://docs.micropython.org/en/latest/library/machine.Pin.html) documents `Pin.PULL_UP` and the `value()` levels used in the second listing.
- The full course kit, if you have not ordered a board yet, is still the [Chapter 00 bill of materials]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %}). This lesson only adds the small parts below.

## Parts for this lab

Prices are the hshop shelf tags checked for this course, in đồng, and they move. The button is a 12 mm round PBS-11B with leads, 10000₫, at [hshop.vn/nut-nhan-nha-tron-pbs-11b-12mm-kem-cap](https://hshop.vn/nut-nhan-nha-tron-pbs-11b-12mm-kem-cap). Any momentary normally-open switch with two legs is the same electrically. The LED pack is 20000₫ at [hshop.vn/bo-5-loai-led-sieu-sang-3mm-thong-dung-5-kind-3mm-transparent-color-led](https://hshop.vn/bo-5-loai-led-sieu-sang-3mm-thong-dung-5-kind-3mm-transparent-color-led). A 3 mm or 5 mm LED both work with the 180 Ω calculation; only the forward voltage changes, and you recompute.

The breadboard is [hshop.vn/test-board-cammb-102](https://hshop.vn/test-board-cammb-102). Male-to-male jumpers, 40 wires, 20 cm, are [hshop.vn/day-cam-breadboard-duc-duc-20cm-cap-det-40-soi-m-m-jumper-wire](https://hshop.vn/day-cam-breadboard-duc-duc-20cm-cap-det-40-soi-m-m-jumper-wire). The 1/4 W resistor assortment, which is where the 180 Ω part lives, is a Shopee search rather than a single stable product page: [bộ điện trở 1/4W](https://shopee.vn/search?keyword=b%E1%BB%99%20%C4%91i%E1%BB%87n%20tr%E1%BB%9F%201%2F4W). Pick 180 Ω or 220 Ω out of that kit. Do not buy a motor for this chapter, and do not connect any motor you already own to a GPIO.
