---
layout: post
title: "Raspberry Pi Pico and MicroPython"
chapter: "02"
order: 3
owner: "Nguyen Le Linh"
lang: en
categories: [chapter02]
lesson_type: required
draft: false
---

## Objectives

You will put a Pico or Pico 2 into BOOTSEL mode so a drive named `RPI-RP2` appears, and you will copy the MicroPython UF2 that matches that chip. You will point Thonny, or `mpremote`, at the board and get a REPL that answers `1 + 1`. You will blink the onboard LED at 2 Hz and print a counter, using `Pin("LED")` on a Pico W or Pico 2 W and GPIO 25 on an original Pico. You will refuse an RP2040 UF2 on a Pico 2. You will keep every GPIO at 3.3 V and leave motors unwired.

## Prerequisites

You either chose a Pico-family board in the landscape lesson or you are learning the other bench’s toolchain once. You can copy a file onto a USB drive. You do not need PlatformIO for this page; that file belongs to the ESP32 track. A data-capable micro-USB cable is part of the setup. The shopping list for the whole robot is still Chapter 00 ([BOM and shopping]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %})).

## Why it matters for Capstone A

If the Pico is your brain, this UF2 and this REPL are the language of the Chapter 07 teleop firmware: two wheel commands, PWM that will later land on a TB6612, and a loop that must notice about 300 ms of silence and force both duties to zero. Wheels stay up the first time that command exists. MicroPython is the short path into that loop, because you can ask the chip a question before you trust a file. A non-W Pico has no Wi-Fi, so Chapter 08’s radio lab is a Pico W, a Pico 2 W, or a switch to the ESP32. Choosing a friendly interpreter does not close that door, and it does not mean you install ROS today.

## BOOTSEL and the right UF2

The RP2040 and the RP2350 both boot from an on-chip boot ROM when you ask. The ask is mechanical. Unplug the board completely. Hold the BOOTSEL button. Plug the USB cable in while the button is still down. Release BOOTSEL. A mass-storage drive named `RPI-RP2` appears, the way a small USB stick would. That name is the bootloader, not your notebook’s disk. Both the original Pico and the Pico 2 use the same volume name, so the label does not tell you which chip you are holding. The filename of the UF2 does.

Take the original Pico (RP2040) image from the official board page [MicroPython for RPI_PICO](https://micropython.org/download/RPI_PICO/). Pico 2 is an RP2350 and uses a different file, from [MicroPython for RPI_PICO2](https://micropython.org/download/RPI_PICO2/). The index at [micropython.org/download](https://micropython.org/download/) lists Pico W and Pico 2 W separately as well. Copy the UF2 onto `RPI-RP2` and only onto that volume. The drive ejects itself and the chip reboots into MicroPython. It will not come back as a drive unless you hold BOOTSEL again. That disappearance is success.

Do not flash the RP2040 image onto a Pico 2. The bootloader may still accept the copy, because it is a file drop, and the board then sits there with no working REPL. The fix is the same gesture: unplug, hold BOOTSEL, plug in, and copy the RP2350 UF2. A Pico W image on an original Pico, or the reverse, is the same class of mistake. Match the silk printed on the board, not the file a classmate just used.

![Original Raspberry Pi Pico: BOOTSEL, USB, GPIO 25 LED]({{ site.imgurl }}/wikimedia/Raspberry_Pi_Pico.jpg)

Find three landmarks on the photograph and on your board before you copy firmware: the micro-USB plug, the BOOTSEL button, and the onboard LED near the USB connector. This picture is an original Pico. GPIO 25 is the lamp. A Pico W does not use that pin for the lamp.

## REPL, then the lamp

Thonny is the editor whose interpreter menu tells the truth. Install it, open it, and choose **MicroPython (Raspberry Pi Pico)**. The port underneath should be the board that just rebooted. Leave that setting for tomorrow. The usual “it worked yesterday” failure is a menu still aimed at the Python on the laptop. The laptop’s Python accepts `print` and then fails on `import machine`, which feels like a broken Pico.

If you prefer a terminal, `mpremote` (install it with `pip` in a local environment) opens the same REPL. Either tool is enough. Do not run both against the port at once.

Click the shell and type:

```python
1 + 1
```

You should see `2` and a new prompt. That is this track’s serial hello. There is no `Serial.begin` inside Thonny’s Pico backend. If you later use a raw terminal, MicroPython’s USB REPL is still a serial device and 115200 is the usual speed.

The onboard LED is the part students copy wrong.

On the original Pico the lamp is GPIO 25. Recent MicroPython also accepts the alias `"LED"` for that pin. If `Pin("LED")` raises `ValueError`, use GPIO 25.

On the Pico W the lamp is wired to the CYW43439 wireless chip, not to GPIO 25. GPIO 25 is an ordinary I/O pin. Lighting the onboard LED means `Pin("LED")`. Writing GPIO 25 will not light it, and it may later be a pin you meant to keep free.

Pico 2, the RP2350 board without W, follows the original wiring: the user LED is GPIO 25. Pico 2 W follows the Pico W idea: the alias `"LED"` is the lamp, and GPIO 25 is not that lamp. The practical rule is to read the silk, then pick the constructor. Do not “fix” a dark LED by moving a wire onto a motor driver.

The lab blink is 2 Hz: on for 250 ms, off for 250 ms, so the full period is 500 ms.

$$
f = \frac{1}{0.250\,\mathrm{s} + 0.250\,\mathrm{s}} = 2\,\mathrm{Hz}.
$$

```python
from machine import Pin
import time

# Pico W / Pico 2 W: the lamp is Pin("LED"), not GPIO 25.
# Original Pico and Pico 2 (no W): the lamp is GPIO 25.
try:
    led = Pin("LED", Pin.OUT)
except ValueError:
    led = Pin(25, Pin.OUT)

n = 0
while True:
    led.value(1)
    time.sleep(0.25)
    led.value(0)
    time.sleep(0.25)
    n += 1
    print(n)
```

Run it from the editor and watch the lamp before you save anything as `main.py`. A `main.py` with a syntax error runs at every power-up and feels like a dead board. If that happens, hold BOOTSEL, get back to a prompt, and remove or edit the file. `time.sleep` is acceptable in this first blink because the only job is to see 2 Hz and a counter. The next lesson drops the sleep so the loop can also watch a 300 ms command timeout.

## Power, in one paragraph

`VBUS` is 5 V from USB when the cable is plugged in. `VSYS` is the board input and can take roughly 1.8 V to 5.5 V; USB reaches it through a diode. `3V3` is the regulated output. GP pins are 3.3 V. Five volts on a GP pin is how Picos die, and 7.4 V from a 2S pack does not belong on `3V3` or on `VSYS`. You will measure the rails in the pinout lesson. You will not feed them from a battery today.

## Worked example

Chi has an original Pico and a phone cable that has never copied a file. The first plug, BOOTSEL held correctly, produces no `RPI-RP2` drive. A Ugreen data cable produces the drive. Chi almost drops a Pico 2 UF2 on it because that was the file open in the downloads folder. The silk says Pico, not Pico 2, so the file comes from the RPI_PICO page instead. The drive vanishes. Thonny still says the local Python, and `import machine` fails. Switching the interpreter to MicroPython (Raspberry Pi Pico) yields a prompt. `1 + 1` prints `2`. `Pin("LED")` works on this firmware and the green lamp flashes twice a second. The counter in the shell climbs once per flash. The note says: “original Pico, RP2040 UF2, LED alias worked, GPIO 25 is the same lamp, no Wi-Fi, no motors.”

On the next bench a Pico 2 W shows the same drive name. The RP2040 file would have been the wrong family. `Pin("LED")` lights the lamp, and GPIO 25 is written down as a free pin, not as the LED.

## Lab

1. Unplug the board. Hold BOOTSEL. Plug the data cable in. Release BOOTSEL. Confirm the volume is named `RPI-RP2`.
2. Download the matching UF2: [RPI_PICO](https://micropython.org/download/RPI_PICO/) for an original Pico, [RPI_PICO2](https://micropython.org/download/RPI_PICO2/) for a Pico 2, or the matching W file from the [download index](https://micropython.org/download/). Copy it onto `RPI-RP2` only. Wait until the drive disappears.
3. Open Thonny on MicroPython (Raspberry Pi Pico), or run `mpremote`. Type `1 + 1`. You should see `2`.
4. Run the blink above. The LED should flash twice a second and the counter should climb: 1, 2, 3, without the prompt vanishing into a reboot.
5. In `lab-notes.md` record the silk (Pico, Pico W, Pico 2, or Pico 2 W), the UF2 page you used, and whether `"LED"` or `25` lit the lamp.

A pass is a REPL that is the Pico, not the laptop, and a 2 Hz blink you watched. A copy onto a different removable disk does not pass, even if the file “succeeded.”

Faults. BOOTSEL was released before the plug went in, so no drive appears and the board jumps straight to whatever was already installed. The cable is charge-only, so neither the drive nor a serial port appears. The UF2 family is wrong: an RP2040 image on a Pico 2, or a W image on a non-W board. Thonny is still on local Python, so `machine` does not exist.

Safety: 3.3 V only on every GP pin. Do not connect a battery, a motor, or a 5 V sensor in this lab. `3V3` is an output. `VSYS` is not a place for a 2S pack.

## Exercises

1. Write the BOOTSEL sequence as four physical actions, and name the drive that must appear. Why does that name fail to tell a Pico from a Pico 2?
2. Your blink uses `Pin(25)` on a Pico W and the onboard lamp stays off. Give the replacement and say what GPIO 25 actually is on that board.
3. You copied `RPI_PICO-....uf2` onto a Pico 2. The drive disappeared and the REPL never comes back. What file replaces it, and what chip does the wrong file belong to?
4. Thonny says `machine` does not exist. What is the interpreter set to?
5. Why does this lesson forbid 5 V on a GP pin even for “just an echo wire”?

<details>
<summary>Answers</summary>

1. Unplug fully. Hold BOOTSEL. Plug USB in while holding. Release BOOTSEL. The drive is named `RPI-RP2`. Original Pico and Pico 2 both use that label. The UF2 filename is what selects RP2040 or RP2350.
2. `led = Pin("LED", Pin.OUT)`. On a Pico W and a Pico 2 W the lamp is on the wireless chip. GPIO 25 is a normal GPIO and will not light the onboard LED.
3. Re-enter BOOTSEL and copy the UF2 from the RPI_PICO2 page. The file you used is the RP2040 image for the original Pico. Pico 2 is an RP2350.
4. It is aimed at the laptop’s local Python, or at the wrong port. Set MicroPython (Raspberry Pi Pico), or use `mpremote` on the Pico’s port.
5. GP pins are 3.3 V. A 5 V echo can destroy the pin. Motors and the 2S pack wait for a driver and for the rail lesson; they are not a way to test a dark LED.

</details>

## Where to buy in Vietnam

Buy a Pico-family board and a data micro-USB cable if you do not already have them. Prices below are the public Hshop readings from 23 September 2026. The verified search [raspberry pi pico](https://hshop.vn/search?q=raspberry+pi+pico) showed a Pico 2 at 195 000 ₫ and a Pico 2 W at 275 000 ₫ that day. Product pages: [Pico 2, RP2350](https://hshop.vn/mach-raspberry-pi-pico-2-rp2350) and [Pico 2 W](https://hshop.vn/mach-raspberry-pi-pico-2-w-rp2350). The Pico 2 has no built-in Wi-Fi. The Pico 2 W does. Cable: [Ugreen Micro-USB 1 m, 54 000 ₫](https://hshop.vn/cap-micro-usb-to-usb-2-0-dai-1m-cao-cap-60136-chinh-hang-ugreen).

Shopee, if you compare shops: [Raspberry Pi Pico 2](https://shopee.vn/search?keyword=raspberry%20pi%20pico%202). If you are still deciding against the ESP32 default, the finished boards are the [NodeMCU-32S at 190 000 ₫](https://hshop.vn/kit-rf-thu-phat-wifi-ble-esp32-nodemcu-32s-ch340-ai-thinker) and the [Vietduino ESP32 at 265 000 ₫](https://hshop.vn/mach-phat-trien-vietduino-esp32), not the [bare ESP32-S3-WROOM-1 at 135 000 ₫](https://hshop.vn/mach-thu-phat-wifi-ble-soc-esp32-s3-esp32-s3-wroom-1-chinh-hang-espressif). [Thế Giới IC’s DevKitC-32U page](https://www.thegioiic.com/esp32-devkitc-32u-module-wifi-bluetooth-2-4ghz) is the other track. [IC Đây Rồi](https://icdayroi.com/) is a component counter. The full cart stays in [Chapter 00]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %}).

## Further reading

- [MicroPython on Raspberry Pi Pico](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html) — Raspberry Pi’s own setup notes for this firmware.
- [Pico datasheet](https://datasheets.raspberrypi.com/pico/pico-datasheet.pdf) — GPIO 25, VBUS, VSYS, 3V3, and absolute maximum pin voltage.
- [MicroPython downloads](https://micropython.org/download/) — the index that separates RP2040 and RP2350 UF2 files. Use the board page, not a forum attachment.
