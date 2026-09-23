---
layout: post
title: "Chapter 03 lab checklist"
chapter: "03"
order: 6
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter03
lesson_type: required
draft: false
---

## Learning objectives

By the end of this lesson you can close Chapter 03 with evidence rather than with a column of hopeful ticks. You will point at a button serial log, at PWM duty lines or a photograph of the LED at two duties, at a debounce count that matches your presses with error zero, and at a state diagram whose silence arrow is labeled 300 ms. You will write the sentence "PWM is zero in FAULT" only if the code makes that sentence true, and you will reject a checklist that marks PWM done when the only duty write sits in `setup()`.

## Prerequisites

Lessons 1 through 5 are the work this page gates. You need the non-blocking heartbeat that replaced the [Chapter 02 blink]({% multilang_post_url contents/chapter02/02_04_blink_serial_hello %}), the pull-up button, the LEDC or `duty_u16` breathe, the short ISR, and the IDLE / TELEOP / FAULT machine. Hardware that has not arrived yet does not earn a pass: a dry reading of your own source is allowed only if the files exist and you can quote the timeout and the duty-zero lines from them. "I will add the timeout when the chassis shows up" is a fail.

## Why it matters

Later chapters will talk as if the differential-drive firmware already accepts a teleop command and already drops both PWM channels when that command goes silent for 300 ms. A ROS graph will publish twists on top of that assumption. It will not notice that your button log is a flood of samples, that the duty was written once at boot, or that FAULT still leaves the last `ledcWrite` in place. The wheels stay up until those facts are in the notes. This checklist is the contract those chapters are allowed to assume, and a tick without an artifact is not a line in the contract.

## Core teaching

Each gate is an observation plus the artifact that proves it. A feeling that the button "basically works" is not a gate. The serial monitor is the gate. Work in the language you will keep for Capstone A. You do not have to repeat every listing in the other language today, but the file you submit has to be the non-blocking style from Lesson 1. A checklist that passes on `delay(1000)` has missed the chapter even if an LED happens to change.

The button gate is a paste of the GPIO lab log: one `press` and one `release` per gesture, not a line every millisecond. Pin numbers and the words `INPUT_PULLUP` or `Pin.PULL_UP` sit next to the paste. If the released pin was floating in your first attempt, the notes can say so, and the log you submit is the one from after the pull-up returned.

The PWM gate is either a photograph of the same LED visibly dim and visibly bright, or three serial lines whose duties are about 25%, 50%, and 90% of the scale you actually configured. Because ESP32 Arduino 3.x does not promise that `analogWrite` is 8-bit, the note names `ledcAttach` with its resolution, or it names `duty_u16`. A line that says "PWM works" and a sketch that never prints the count are not this gate. The load in the photo is the LED and its series resistor. A motor in the photo fails the gate, even if the motor spun, because this chapter does not attach a motor to a GPIO and does not require VM wired.

The debounce gate is a pair of numbers. You pressed $N$ times. The counter printed $N$, so the error is

$$
e = N_{\mathrm{printed}} - N_{\mathrm{pressed}} = 0.
$$

The burst log from the interrupt lesson, the one that jumped by something in the 5–30 range when the stability window was removed, can sit underneath as a contrast. It is not a substitute for $e = 0$. If your best debounced run still gains two counts per press, the checklist item stays open and you return to the 20 ms test.

The state-diagram gate is a drawing in the notes, not a screenshot of the lesson figure alone. Copying the figure is fine as a template. The arrow from TELEOP to FAULT has to be labeled with the timeout you compiled, 300 ms, and IDLE and FAULT both have to be marked duty 0. The sentence in the notes is exactly the claim the code makes: "PWM is zero in FAULT." If your `apply` function lights the LED whenever `duty` is nonzero, regardless of state, you are not allowed to write that sentence yet.

![Bring-up order: logic first, motor supply later, wheels up]({{ site.imgurl }}/generated/power_order.png)

The power-order figure is the boundary of this chapter. USB powers the microcontroller. The 3.3 V rail powers the button pull-up and the LED. The motor supply, VM on a TB6612, is a later box in that figure, and it stays empty today. Wheels up is the posture for the first day VM is connected, which is not a Chapter 03 signature. Signing the checklist does not authorize a motor wire.

## Worked example: a checklist that lies

A submitted note ticks "button," "PWM," "debounce," and "state machine." The only source attached is this:

```cpp
const int PIN = 18;

void setup() {
  Serial.begin(115200);
  ledcAttach(PIN, 1000, 8);
  ledcWrite(PIN, 180);
  Serial.println("PWM done");
}

void loop() {
  delay(1000);
  Serial.println("still on");
}
```

Read it against the gates. There is no button, so the press log cannot exist. `ledcWrite` runs once, in `setup`, at a fixed 180, which is about 70% and never 0. Nothing in `loop` reads `millis()`, so a 300 ms silence cannot change the pin. `delay(1000)` is the Lesson 1 failure mode: the first time the loop could even look at a timestamp, the deadline has been missed three times over. The print `PWM done` is a caption, not a measurement. Ticking the PWM box because the letters `ledcWrite` appear is how this chapter gets a robot that boots already driving.

The audit rewrites the tick into four failures. PWM is not demonstrated across duties, and it is not demonstrated at 0. The timeout is absent, so FAULT cannot be entered and the sentence "PWM is zero in FAULT" would be false: there is no FAULT, and the pin is not zero. The loop is blocked for a full second, which is longer than the cutoff

$$
1000\,\mathrm{ms} > 300\,\mathrm{ms}.
$$

A repaired sketch writes the duty from the state machine every pass, logs the duty when it changes, and uses the Lesson 1 clock. The checklist item flips only after those lines are in the file you just flashed, and after you have watched the LED go dark when typing stops.

The same audit catches a subtler cousin: the state machine is real, but `setup` ends with `ledcWrite(PIN, 180)` and FAULT forgets to write 0 because the author believed "we are not calling ledcWrite, so the motor is off." PWM peripherals hold the last duty. Not calling the function leaves the old pulses running. FAULT has to write zero explicitly, every pass, for both channels you will later connect to the TB6612.

## What you turn in

Work down this list in your lab notes. An item without its artifact stays open.

1. Button log. Paste a press and a release, name the GPIO, and name the pull-up. One pair per gesture.
2. PWM evidence. Photograph the LED at two brightnesses or paste duties near 25%, 50%, and 90%, and write the API (`ledcAttach` resolution, or `duty_u16`). Include a line that is duty 0.
3. Debounce count. Write $N$ pressed and $N$ printed. Error zero. Mention the burst you saw when the filter was off, as a contrast, if you ran that step.
4. State diagram. Three states, the 300 ms arrow into FAULT, duty 0 marked on IDLE and on FAULT. The sentence "PWM is zero in FAULT" appears in the notes and matches `apply`.
5. Language and loop. Name C++ or MicroPython, and confirm the control path does not call `delay` or `sleep` longer than a few milliseconds. Quote the timeout constant from the file.
6. Motor boundary. Write "no motor on a GPIO, VM not connected, wheels up when a driver is added later." If you do not own a driver yet, that sentence is still required. Buying one is the TB6612 module at 45000₫, VM about 4.5 V to 10 V, about 1.2 A continuous, from the [hshop TB6612 listing](https://hshop.vn/mach-dieu-khien-dong-co-dc-tb6612fng-dc-motor-driver), and it is not part of today's wiring.

A missing board is not item 6. If the hardware is late, items 1–3 stay open. Items 4 and 5 can be drafted from source you have actually compiled or syntax-checked, and they stay marked "source only" until the LED has performed them.

## Exercises

1. Audit the worked-example sketch as if you were the reviewer. List the checklist items it fails, and quote the line that makes "PWM is zero in FAULT" false.
2. A partner's diagram shows IDLE, TELEOP, and FAULT, but the silence arrow is drawn from IDLE to FAULT and labeled "1 s." What does the arrow get wrong about who can time out, and about the constant in Lesson 5?
3. The debounce log says you pressed 10 times and the last line is `presses=12`. Is the gate closed? What single code change from Lesson 4 is the first place you look?
4. `setup` writes duty 200, and the FAULT branch only sets a variable `duty = 0` without calling `ledcWrite`. After 300 ms of silence, what is on the pin, and what line has to move into `apply`?

<details>
<summary>Hints</summary>

1. It fails the button log, the multi-duty PWM evidence, the zero duty, the debounce count, and the state diagram. `ledcWrite(PIN, 180)` in `setup`, with no later write of 0, is the false sentence. `delay(1000)` is the blocked loop.
2. Silence is tested in TELEOP, not in IDLE. IDLE is already duty 0. The constant is 300 ms, not 1 s.
3. The gate stays open because $e = 2$, not 0. Look first at the 20 ms stability test around the increment, and at whether a CHANGE interrupt is also counting the release.
4. The pin keeps pulsing at duty 200. `apply` has to call `ledcWrite` with 0 whenever the mode is FAULT or IDLE, on every pass.

</details>

## Further reading

- [`millis()`](https://www.arduino.cc/reference/en/language/functions/time/millis/) is the function you expect to find in any sketch that claims the 300 ms arrow is real.
- [ESP32 Arduino LEDC](https://docs.espressif.com/projects/arduino-esp32/en/latest/api/ledc.html) is how you check that a duty write in the submitted file matches the resolution the author attached.
- [micro-ROS](https://micro.ros.org/) will sit on top of a firmware image that has already passed this list. It does not replace the FAULT write of duty 0.
