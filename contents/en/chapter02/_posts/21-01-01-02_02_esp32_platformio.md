---
layout: post
title: "Arduino IDE and PlatformIO on ESP32"
chapter: "02"
order: 2
owner: "Nguyen Le Linh"
lang: en
categories: [chapter02]
lesson_type: required
draft: false
---

## Objectives

You will install one ESP32 toolchain and ignore the other until you have a blink you trust. Along the Arduino IDE 2 path you will add Espressif’s board index, install the `esp32` package, and select a Dev Module or NodeMCU-32S entry that matches the silk. Along the PlatformIO path you will write a `platformio.ini` whose board is `esp32dev` and whose monitor is 115200. You will blink `LED_BUILTIN` when the core defines it, and GPIO 2 only after you have checked that your board actually wires the lamp there. You will recognize a missing port, a charge-only cable, a CH340 driver, and a brownout caused by a motor supply that was still connected during upload.

## Prerequisites

The landscape lesson should already name an ESP32 dev board as your primary microcontroller. If you committed to a Pico, read this page as a map and do the Pico lesson next; installing both toolchains in one afternoon is how the wrong board id gets saved. You need a laptop and a USB cable that has copied files before. The full parts list remains the Chapter 00 shopping lesson ([BOM and shopping]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %})).

## Why it matters for Capstone A

Chapter 07’s diff-drive teleop is a firmware image on this same chip: left and right PWM toward a TB6612, a silence test of about 300 ms, wheels off the table. None of that image can be believed until this board accepts a binary, toggles a pin you chose, and prints a line at a baud rate you wrote down. Chapter 08’s Wi-Fi teleop uses the same upload path. A board that only blinks in someone else’s video has not joined your robot. The serial monitor, one port and 115200 baud, is the console you will trust before any radio is allowed to complicate the log.

## Pick one install

Two roads share Espressif’s Arduino core. Pick the one your lab machine already has. You are not asked to start on ESP-IDF this week.

Arduino IDE 2 is the click-through path. Install the IDE. Open Preferences (or Settings) and paste this Additional Boards Manager URL:

```text
https://espressif.github.io/arduino-esp32/package_esp32_index.json
```

Open the Boards Manager, search `esp32`, and install **esp32 by Espressif Systems**. Then open the board menu and select the entry that matches the silk. A generic 30-pin or 38-pin DevKit is **ESP32 Dev Module**. A board whose silk says NodeMCU-32S should use the **NodeMCU-32S** entry when that entry exists. Set the port to the new serial device. If the first upload fails with a sync or timeout error, set Upload Speed to 115200. The IDE often starts at 921600, and a long cable or a CH340 clone drops bytes at that rate.

PlatformIO is the path with a file you can diff. Install Visual Studio Code, then the PlatformIO IDE extension, and let the first-run download finish. Create a project and put this in `platformio.ini`:

```ini
[env:esp32dev]
platform = espressif32
board = esp32dev
framework = arduino
monitor_speed = 115200
```

`esp32dev` is the generic classic-ESP32 target: a WROOM-class module and a USB-serial adapter. It matches the NodeMCU-32S and the common DevKit V1 boards in this course. It is the wrong id for an ESP32-S3 native-USB board. That is another reason the landscape lesson told you to buy a classic dev board unless you are ready to change this file and the pin map together.

## The lamp and the port

`LED_BUILTIN` is a macro some board variants define. If your selected board defines it, use it for the first blink. If the header does not define it, use GPIO 2. GPIO 2 is the onboard LED on many DevKit V1 boards, and it is a common wiring on NodeMCU-32S clones. It is not a promise. Some boards put the lamp on another GPIO, and some have only a power LED that firmware cannot blink. Read the silk or the vendor diagram, write the number in your notes, and change the constant if GPIO 2 stays dark. Do not reinstall the IDE because a macro was optimistic.

A short sketch that matches this lab:

```cpp
#ifndef LED_BUILTIN
#define LED_BUILTIN 2  // common on DevKit V1; confirm your pinout
#endif

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(115200);
  Serial.println("hello");
}

void loop() {
  digitalWrite(LED_BUILTIN, HIGH);
  Serial.println("high");
  delay(400);
  digitalWrite(LED_BUILTIN, LOW);
  Serial.println("low");
  delay(400);
}
```

`Serial.begin(115200)` must match the monitor. A mismatch does not look like silence. It looks like characters that are almost letters. This sketch uses `delay` so the first success is obvious. The heartbeat lesson replaces that structure, because a later stop command cannot wait inside `delay` for a 300 ms timeout.

The chip near the USB plug is not the ESP32. On classic dev boards it is a CH340 or a CP2102. CP2102 ports usually appear with the operating system’s own driver. CH340 boards on Windows often stay invisible until you install the WCH CH340 driver; Device Manager then shows a new COM port. On Linux the same chips appear as `/dev/ttyUSB0` (then `ttyUSB1` if a second adapter is plugged in). On Windows the name is `COM3`, `COM4`, or another `COMx` that was not there before you plugged the cable in. Your account on Linux needs to be in the `dialout` group, and the group membership applies only after you log out and back in.

A charge-only USB cable enumerates nothing. The power LED can still glow, because power wires are present and data wires are not. Swap in a cable you have used to copy a file. The [data cable in the shopping section](#where-to-buy-in-vietnam) is the known-good shape for these micro-USB boards.

Download mode is a button story. GPIO 0 sampled low at reset puts a classic ESP32 into the serial bootloader. The BOOT button (sometimes IO0) holds that pin. EN, RST, or RESET restarts the chip. Many dev boards enter the bootloader automatically through the USB-serial chip’s DTR and RTS lines. When that circuit is missing, the upload times out. Hold BOOT, start the upload, and release BOOT when the log says it is connecting. If that is awkward, hold BOOT, tap EN, release BOOT, and upload while the chip stays in that mode.

## What a failed upload usually is

Three faults cover almost every “the board is dead” report in this lab.

The board menu is wrong. An S3 or C3 entry, or a random “ESP32 Pico Kit” entry, does not match a NodeMCU-32S. The upload complains, or it appears to succeed and the pin you blink is not the pin you think. Set Dev Module or NodeMCU-32S, or `board = esp32dev`, to match the silk.

No port appears. Start with the cable. Then the driver: CH340 on Windows, and `dialout` on Linux. A port left over from yesterday’s Pico (`/dev/ttyACM0` while the ESP32 is `/dev/ttyUSB0`) is the same class of mistake.

The chip resets while the bootloader is talking. If a motor, or a driver whose VM pin is still tied to the board’s 5 V pin, is attached, the current spike browns the rail out and the download dies mid-way. Unplug VM. Unplug every motor wire. Upload again with only the USB cable. The heartbeat lesson will show you the same reset as a repeating `hello` once the sketch is running; during upload it looks like a timeout instead.

GPIO 1 and GPIO 3 are the UART pins the USB-serial chip is already using. A blink on those pins turns the console into noise. Leave them alone today.

## Worked example

Bình’s board is the Hshop NodeMCU-32S, CH340, on a Windows laptop. The first plug lights the power LED and Device Manager gains nothing. A CH340 driver install produces `COM5`. The sketch above is pasted into Arduino IDE 2 with the NodeMCU-32S board entry and upload speed 115200. The first upload still fails. A TB6612 from a previous bench session has VM jumpered to the dev board’s 5 V pin. Bình unplugs that VM wire, holds BOOT, and uploads again. The monitor at 115200 prints `hello`, then `high` and `low` in time with the lamp. GPIO 2 matches the silk on this board, so the `#ifndef` fallback and the real LED are the same pin. Changing only the monitor to 9600 fills the pane with garbage while the LED keeps blinking, which separates a baud mistake from a dead chip.

## Lab

1. Choose Arduino IDE 2 or PlatformIO. Install that one path using the URL or the `platformio.ini` above.
2. Plug in the data cable. Confirm a new port: `/dev/ttyUSB0` on Linux or a new `COMx` on Windows. Write the name down.
3. Select ESP32 Dev Module or NodeMCU-32S, or `board = esp32dev`. Set the monitor to 115200.
4. Paste the sketch. If your silk’s LED is not GPIO 2 and `LED_BUILTIN` is dark, change the pin and write the new number in `lab-notes.md`.
5. Upload. If the log times out, hold BOOT and retry once. If a motor or a VM wire is attached, unplug VM and retry.
6. Open the monitor at 115200. You should see one `hello` and then `high` / `low` lines while the onboard LED blinks. Copy eight lines into your notes with the port name and the USB chip (CH340 or CP2102).

A pass is a lamp you watched and a log you pasted. A power LED that is on whenever USB is plugged in does not count.

Safety: USB only. No battery, no motor, no VM connection. The 5 V pin is not a motor supply, and a stall during upload is exactly the brownout this lab is teaching you to remove.

## Exercises

1. Write the four `platformio.ini` keys this lesson requires, and write the Arduino IDE boards URL from memory.
2. `LED_BUILTIN` leaves the board dark, and the monitor still prints `high` and `low`. What do you check on the silk, and why is “GPIO 2” a hypothesis rather than a fact?
3. Upload works only while BOOT is held. Which pin is that button, and what do you do with EN?
4. The log prints `hello` over and over and never stays in `loop`. A motor driver is still on the desk, VM tied to the 5 V pin. What do you unplug, and what electrical event was resetting the chip?
5. The LED blinks and the monitor shows garbage. Name the two baud numbers that disagree. Why is the chip itself still fine?

<details>
<summary>Answers</summary>

1. `platform = espressif32`, `board = esp32dev`, `framework = arduino`, `monitor_speed = 115200`. The boards URL is `https://espressif.github.io/arduino-esp32/package_esp32_index.json`, then the package **esp32 by Espressif Systems**.
2. Find the onboard LED’s GPIO on your board’s pinout. GPIO 2 is the lamp on many DevKit V1 boards and on many NodeMCU-32S clones, and other boards differ. Change the constant to the pin the silk names, and record it.
3. BOOT pulls GPIO 0 low so reset enters the serial bootloader. Hold BOOT, tap EN (reset), release BOOT, and upload while the chip remains in that mode. Boards with a working auto-reset circuit hide this.
4. Unplug VM, and unplug any motor. The extra current sagged the rail (a brownout) and the bootloader reset before the download finished.
5. The sketch is at 115200 and the monitor is at something else, often 9600. The LED is toggling, so the program is running. Fix the monitor speed; do not reinstall the toolchain.

</details>

## Where to buy in Vietnam

If the landscape lesson’s dev board and data cable already enumerate, buy nothing. If the port never appears, replace the cable before you replace the board. Prices were read from public Hshop listings on 23 September 2026.

Default board: [ESP32 NodeMCU-32S CH340, 190 000 ₫](https://hshop.vn/kit-rf-thu-phat-wifi-ble-esp32-nodemcu-32s-ch340-ai-thinker). Alternate finished board: [Vietduino ESP32, 265 000 ₫](https://hshop.vn/mach-phat-trien-vietduino-esp32). The [ESP32-S3-WROOM-1 at 135 000 ₫](https://hshop.vn/mach-thu-phat-wifi-ble-soc-esp32-s3-esp32-s3-wroom-1-chinh-hang-espressif) is a bare module and will not appear as `/dev/ttyUSB0` or `COMx` by itself. Cable: [Ugreen Micro-USB 1 m, 54 000 ₫](https://hshop.vn/cap-micro-usb-to-usb-2-0-dai-1m-cao-cap-60136-chinh-hang-ugreen).

Shop searches if you compare: [Shopee ESP32 DevKit CH340](https://shopee.vn/search?keyword=esp32%20devkit%20ch340). [Thế Giới IC’s DevKitC-32U page](https://www.thegioiic.com/esp32-devkitc-32u-module-wifi-bluetooth-2-4ghz) is a board-style listing; confirm it is a USB dev board and note whether the antenna is the U.FL version. [IC Đây Rồi](https://icdayroi.com/) is a component counter, not the place to grab a bare module and call it this lab’s starter. The rest of the robot cart is still [Chapter 00]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %}).

## Further reading

- [PlatformIO `esp32dev` board page](https://docs.platformio.org/en/latest/boards/espressif32/esp32dev.html) — the board id in this lesson’s ini file.
- [Installing the Arduino ESP32 core](https://docs.espressif.com/projects/arduino-esp32/en/latest/installing.html) — the boards URL and the IDE steps, from Espressif.
- [Espressif document downloads](https://www.espressif.com/en/support/download/documents) — datasheets and hardware design guides when a clone’s LED pin disagrees with GPIO 2.
