---
layout: post
title: "Chapter 02 lab checklist"
chapter: "02"
order: 6
owner: "Nguyen Le Linh"
lang: en
categories: [chapter02]
lesson_type: required
draft: false
---

## Objectives

You will close Chapter 02 only with evidence you can point at. You will record the toolchain and its version string. You will show that the onboard LED blinks at a period you chose, and you will paste the serial heartbeat rather than describe it. You will finish a pin card for the board on the desk: which GPIO is the LED, and which pins are safe outputs. You will write the two rail measurements, 3.3 V and 5 V or VBUS. You will add one sentence that names the motor pins you will not use yet, VM and the battery. If a tick fails, you will reopen the lesson that taught it instead of buying a second board.

## Prerequisites

Lessons 1 through 5 are the evidence this page consumes. You need the decision sentence (ESP32 dev board or a named Pico), the toolchain that matches it, the heartbeat log or an honest blank, and the pin card. A meter is required for the rail tick. The full cart remains Chapter 00 ([BOM and shopping]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %})). Re-read the wheels-up sentence in the heartbeat sketch so this checklist does not “pass” a robot that can already roll.

## Why it matters for Capstone A

Chapter 07 asks this microcontroller to teleoperate a differential-drive base: two PWM channels toward a TB6612, a battery on VM, and wheels that stay off the ground until you are ready. If commands stop for about 300 ms, both duties go to zero. That chapter assumes the ticks on this page were passed with notes. A student who arrives still unsure which pin is ground will debug a timeout while the chip is resetting. Chapter 08 can carry the same teleop over Wi-Fi on an ESP32, and it will happily transport a stream from a board that browns out. The graph then shows a link that “flakes.” The flake was a skipped meter reading or a VM wire that was never supposed to be attached. This checklist is the pause that keeps later software from hiding an electrical problem.

## Six ticks, each with a token

A tick is a condition with evidence, not a topic you remember reading. Chapter 02 has six. Each one is either passed with a pointer into `lab-notes.md` or left open. A half-tick (“it mostly worked”) is an open tick.

The toolchain tick is a version you wrote down. Arduino IDE: the version from the About box, plus the installed `esp32` package version from Boards Manager. PlatformIO: the string from `pio --version`, and the line `board = esp32dev` still present in `platformio.ini`. Pico: the Thonny version or the `mpremote` version, and the UF2 filename, including whether it was `RPI_PICO` or `RPI_PICO2`. “I installed something” is not a version.

The blink tick is an onboard LED you watched, at a period you chose and wrote as a number. The heartbeat lab’s period is 500 ms, a toggle every 250 ms, 2 Hz. If you chose a different period on purpose, write that number. The power LED does not count. `LED_BUILTIN` does not count until you have checked it against the silk. The note records the GPIO or the Pico alias (`"LED"` or 25).

The serial tick is the heartbeat paste. Ten lines, millisecond stamps climbing by about the period you claimed, one banner, no second boot line inside the block. The fields are time and state. A sentence that says “it counted fine” fails, because the later brownout comparison needs the actual staircase. The baud in the notes is 115200 if you are on the ESP32 sketch from this chapter. A monitor left at 9600 is a failed tick even when the LED is flashing.

The pin-card tick is a drawing or a markdown table for the board you have, not for a random image. It names the LED GPIO, at least one safe output you have checked (not a strap you intend to pull hard, not the UART pins the USB chip is using, not a power pin), and the grounds. Labels copied from a different clone fail when they disagree with your header. On a Pico W the safe-output list must not call GPIO 25 the onboard LED.

The meter tick is two numbers, USB only, battery absent. About 4.7 V to 5.1 V on the 5 V pin or on VBUS, and about 3.25 V to 3.35 V on 3V3. Write the numbers. A diode-dropped 4.82 V is a pass with the digits visible. “5 V ok” is a fail. A 3V3 pin at 4.9 V is an unplug, not a pass.

The motor-pin tick is one sentence that names what you will not use yet. A passing sentence: “VM on the TB6612 and the 2S battery stay disconnected; the pack must not touch GPIO, 3V3, 5V/VIN, VSYS, or VBUS.” Wheels-up belongs in the same note. A tick that says “motors later” without naming VM and the battery is still open.

![The checklist stops before the motor supply]({{ site.imgurl }}/generated/power_order.png)

The drawing is the sequence the ticks enforce. USB, a blink, and a serial heartbeat are the proof the logic rail is alive. The driver and the battery are to the right of a line this chapter does not cross.

Order matters. The landscape lesson’s bring-up was USB, onboard LED, serial at 115200, a button, PWM on an unloaded pin, and only then a driver and a battery. This chapter’s six ticks stop before that driver. Unloaded PWM can be a later exercise. It is not permission to clip a motor onto a GPIO because the checklist is done.

If the parcel has not arrived, you may record the toolchain version and a pin card traced from the exact listing you paid for. Leave blink, serial, and the two voltages blank and labeled pending. Do not paste imagined serial output. A dry page is a way to use the waiting time. It is not a passed chapter.

## Remediation

When a tick fails, reopen the lesson that taught the missing evidence.

No version string: open About, or run `pio --version`, or print the MicroPython implementation from the REPL, and write the text. That is the tooling lesson, ESP32 or Pico, depending on the board.

No blink, or a blink on a pin you have not identified: return to the ESP32 upload lesson or the Pico UF2 lesson, then to the heartbeat lesson. Read the silk. GPIO 2 is common on DevKit V1 boards and wrong on others. Pico W uses `Pin("LED")`, not GPIO 25.

Serial missing, garbage, or a repeating banner: heartbeat lesson. Set 115200. If the banner repeats and no motor is connected, swap the cable and remove jumpers before you rewrite the print. If VM is still wired, unplug VM. That brownout is not a software bug.

Pin card missing or copied from the other family’s board: pinout lesson. Draw 5 V or VBUS, 3V3, GND, the LED pin, and one safe output.

Voltages missing or written as “ok”: pinout lesson, USB only. If 3V3 is far from 3.3 V, stop. Do not attach the pack to learn more.

The motor sentence missing: write it now, from the pinout lesson’s worked example. The 2S pack may touch VM. It must not touch the microcontroller header.

Buying a second ESP32 because a tick is open usually duplicates the same cable mistake. Replace a charge-only lead first.

## Worked example

Two notebooks, both honest.

Hà’s board arrived last week. The notes read: Arduino IDE 2.3.2 with esp32 package 3.0.7; NodeMCU-32S; CH340 as `COM5`; onboard LED on GPIO 2, confirmed on the silk, toggling every 250 ms; ten heartbeat lines stepping by 498 ms to 505 ms under one banner, monitor at 115200; pin card with 5V, 3V3, GND, LED GPIO 2, safe output GPIO 4; meter 4.91 V and 3.31 V, USB only; sentence “VM and the 2S battery stay off; pack positive never touches 5V, 3V3, or any GPIO.” All six ticks pass. The TT motors stay in the box. Wheels, when the chassis exists, stay up.

Khoa’s Pico 2 is on a truck. The notes read: Thonny 4.1.4 installed, UF2 name copied from the RPI_PICO2 page so the RP2040 image is not the one that gets flashed, pin card traced from the listing photo with VBUS, VSYS, 3V3, GND, LED GP25, safe output GP16, and the sentence “no 5 V on GP pins; VM and the battery are not in this parcel.” Blink, serial, and the two voltages are the word `pending`. Khoa does not tick the chapter complete.

A third note, rejected, is the one the exercises use.

## Lab

Open `lab-notes.md`. Create a section titled with the date and “Chapter 02 gates.” For each of the six ticks, write PASS plus the evidence, or OPEN plus the lesson you will repeat. If the board is absent, mark blink, serial, and the meter as pending in those words. Read the section once. Any tick you cannot point at with a finger — a version string, a line of serial, a voltage, a pin number, the words VM and battery — becomes OPEN before you save.

A chapter pass is all six ticks PASS, wheels-up sentence present, no motor connected. A dry run is toolchain, decision, and a photo-traced pin card, with the three measured ticks explicitly pending. There is no third state called “close enough.”

## Exercises

Use this fake note. It is not a pass.

```text
Date: 23 Sep 2026
Board: ESP32 NodeMCU
Toolchain: Arduino IDE installed
LED: GPIO 2, it blinked I think
Monitor baud: 9600
Serial: saw some characters, did not copy them
Rails: 5V ok, 3.3 ok
Next: PWM the motor from GPIO 2, battery soon
```

1. List every tick this note fails, and the evidence token that is missing for each.
2. The sketch from the heartbeat lesson calls `Serial.begin(115200)`. What does a monitor at 9600 show, and what single change repairs the serial tick?
3. “GPIO 2, it blinked I think” is unverified. What must be true on the silk before GPIO 2 can be the blink tick, and what do you write if the lamp is on another pin?
4. Rewrite the rails line and the motor line so those two ticks could pass. Invent no voltages you did not measure; use the form the tick requires and mark numbers pending if the meter has not been used.
5. Which lesson do you reopen first, and why is a second dev board the wrong purchase?

<details>
<summary>Answers</summary>

1. Toolchain: no version string. Blink: “I think” is not a period you chose and not a silk check. Serial: no pasted lines, and the baud is 9600. Meter: “ok” is not two numbers. Motor pins: the note plans to PWM a motor from GPIO 2 and attach a battery, which is the opposite of naming VM and the battery as unused. The pin card is missing entirely, so the safe-output tick is open too.
2. The pane fills with garbage or with characters that are almost letters, while the LED can still blink. Set the monitor to 115200. Do not change the sketch to 9600 to match a habit from an Uno tutorial.
3. The silk or the vendor diagram has to show the onboard LED on GPIO 2. Many DevKit V1 boards do; some boards do not. If the lamp is elsewhere, write that GPIO, watch it blink at the period you chose, and leave GPIO 2 off the card until you know what it is. `LED_BUILTIN` still needs the same check.
4. A passing rails line has digits, for example “USB only, 5V pin ____ V, 3V3 pin ____ V, battery not connected,” with the blanks filled from the meter. A passing motor line: “VM and the 2S battery stay disconnected; the pack must not touch GPIO, 3V3, or 5V/VIN.” GPIO 2 is not a motor pin.
5. Reopen the heartbeat lesson first if the baud and the missing paste are the blockers, and the pinout lesson for the rails and the VM sentence. A second board repeats the same missing notes. A charge-only cable, if the port itself is absent, is the part to replace.

</details>

## Where to buy in Vietnam

Buy only what an open tick needs. A missing data cable: [Ugreen Micro-USB 1 m, 54 000 ₫](https://hshop.vn/cap-micro-usb-to-usb-2-0-dai-1m-cao-cap-60136-chinh-hang-ugreen). A missing brain: [ESP32 NodeMCU-32S CH340, 190 000 ₫](https://hshop.vn/kit-rf-thu-phat-wifi-ble-esp32-nodemcu-32s-ch340-ai-thinker) or [Vietduino ESP32, 265 000 ₫](https://hshop.vn/mach-phat-trien-vietduino-esp32). The [ESP32-S3-WROOM-1 at 135 000 ₫](https://hshop.vn/mach-thu-phat-wifi-ble-soc-esp32-s3-esp32-s3-wroom-1-chinh-hang-espressif) is a bare module and does not close the toolchain tick. Pico track, prices read on 23 September 2026 from [the Pico search](https://hshop.vn/search?q=raspberry+pi+pico): Pico 2 at 195 000 ₫ ([product page](https://hshop.vn/mach-raspberry-pi-pico-2-rp2350)) and Pico 2 W at 275 000 ₫ ([product page](https://hshop.vn/mach-raspberry-pi-pico-2-w-rp2350)). Shopee: [ESP32 DevKit CH340](https://shopee.vn/search?keyword=esp32%20devkit%20ch340), [Pico 2](https://shopee.vn/search?keyword=raspberry%20pi%20pico%202). [DevKitC-32U at Thế Giới IC](https://www.thegioiic.com/esp32-devkitc-32u-module-wifi-bluetooth-2-4ghz) is a board-style page; confirm USB. [IC Đây Rồi](https://icdayroi.com/) is a component counter. Do not buy a motor or a TB6612 to finish Chapter 02. Those lines live in the [Chapter 00 cart]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %}).

## Further reading

- [PlatformIO `esp32dev`](https://docs.platformio.org/en/latest/boards/espressif32/esp32dev.html) — the board id the ESP32 toolchain tick expects by default.
- [Installing arduino-esp32](https://docs.espressif.com/projects/arduino-esp32/en/latest/installing.html) — where the package version in your notes comes from.
- [MicroPython downloads](https://micropython.org/download/) — the UF2 filename the Pico tick must name, RP2040 and RP2350 separated.
- [ESP32 datasheet](https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf) — check a “safe output” against the electrical table before you believe a blog pinout.
