---
layout: post
title: "Choosing a microcontroller for a small robot"
chapter: "02"
order: 1
owner: "Nguyen Le Linh"
lang: en
categories: [chapter02]
lesson_type: required
draft: false
---

## Objectives

By the end of this lesson you can compare three honest brains for a small diff-drive robot: a classic ESP32 dev board, a Raspberry Pi Pico or Pico 2, and an Arduino Uno-class board. You can say what each one does with logic voltage, radio, and the first language you will actually type. You can choose the ESP32 NodeMCU-32S when phone teleop is coming, and you can say why a bare module and a Pico without Wi-Fi are different purchases. You can write the bring-up order that stops a brownout from looking like a random bug in the sketch. You can also compute a classroom threshold for a 3.3 V logic high and use it to refuse a 5 V signal on a GPIO.

## Prerequisites

You can set a meter to DC volts, and you know a GPIO is a pin the chip can drive or read. A series resistor in front of an LED, from Chapter 01, is enough. You do not need to have flashed firmware. The full cart stays in the Chapter 00 shopping lesson ([BOM and shopping]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %})). This page only chooses the brain and the cable.

## Why it matters for Capstone A

Capstone A, in Chapter 07, is a differential-drive base: two driven wheels, a caster, and firmware that turns a command into PWM for a TB6612 later. The command stream is not trusted forever. If fresh commands stop for about 300 ms, both wheel duties go to zero while the chassis is still wheels-up on the bench. That loop has to live on one microcontroller you already trust. Chapter 08 then has a Wi-Fi and MQTT lab, which is how the same teleop can leave the USB cable and reach a phone or a laptop. An ESP32 already has 2.4 GHz Wi-Fi and BLE on the module, so it is the course default. A Pico without a W suffix can still run the Chapter 07 firmware over USB, and it is a fine fast-iteration board, but it cannot join the Chapter 08 radio lab until you buy a different board. The choice you write down today is the pin map, the toolchain, and the radio story for the rest of the semester.

## Three boards, three different jobs

An ESP32 in this course means a classic dual-core Xtensa module on a dev board, with Wi-Fi and BLE in the metal can and GPIO at 3.3 V. Buy a board that already has a USB connector, a 3.3 V regulator, a USB-serial chip, a BOOT button, and headers. The serial chip is usually a CH340, very common on boards sold in Vietnam, or a CP2102, which the operating system often recognizes with no extra driver. A bare module has none of that. The NodeMCU-32S with CH340 is the shape of the default. The Vietduino ESP32 listing is another finished dev board. The ESP32-S3-WROOM-1 line is a bare module and stays off the starter list even though the price is lower.

A Raspberry Pi Pico or Pico 2 is the fast-iteration alternate. The original Pico uses an RP2040. Pico 2 uses an RP2350. Both run GPIO at 3.3 V and both answer you in a MicroPython REPL. The original Pico and the Pico 2 without a W have no built-in Wi-Fi. Pico W and Pico 2 W add a radio. Write the exact silk in your notes, because the LED pin and the firmware file change with that suffix. Choose this family when the REPL is what you want to learn first, and when Chapter 08’s Wi-Fi lab can wait for a W board or a switch to the ESP32.

An Arduino Uno-class board, the ATmega328P and its clones, is 5 V logic. It is worth recognizing so you do not confuse it with the robot brain. It has no Wi-Fi, and a 5 V high does not belong on a 3.3 V input. An HC-SR04 echo or an Uno pin marked “just a signal” can destroy an ESP32 or Pico pin. Keep an Uno as a known 5 V reference if you already own one. Leave it out of the Capstone A socket.

![Anatomy of a dev board: USB, regulator, headers, and the module]({{ site.imgurl }}/generated/pcb_mcu_anatomy.png)

The USB connector is how the laptop enumerates the board. The regulator makes 3.3 V. The headers are the only pins you wire. A bare module in a tray has the can and none of the rest.

![ESP32 module on a small dev-board clone]({{ site.imgurl }}/wikimedia/ESP32_on_Lolin32_Lite_clone_board_cropped.jpg)

Match your own board to the metal can, the USB socket, and the headers before you trust a pinout drawn for a different clone.

![Raspberry Pi Pico, the MicroPython alternate]({{ site.imgurl }}/wikimedia/Raspberry_Pi_Pico.jpg)

BOOTSEL, the micro-USB plug, and the labels `3V3`, `VSYS`, and `VBUS` are the landmarks. This photograph is an original Pico: no radio, onboard LED on GPIO 25.

## Logic voltage is a number

Inside a CMOS input, “high” is a voltage relative to that chip’s own supply. A classroom reading rule, not a datasheet $$V_{IH}$$, is that you treat a pin as high only when the voltage is at least about $$0.7$$ times the supply:

$$
0.7 \times 3.3\,\mathrm{V} \approx 2.3\,\mathrm{V}.
$$

On the ESP32 and the Pico that teaching threshold is about 2.3 V. The real $$V_{IL}$$ and $$V_{IH}$$ live in the electrical-characteristics table and they move with $$V_{DD}$$. You will look them up when a divider is close to the edge. Until then the operating rule is stricter than the formula: GPIO in this course is 3.3 V only.

The damage threshold is why the Uno is awkward next to those pins. A 3.3 V GPIO’s absolute maximum is only a little above the rail, on the order of

$$
3.3\,\mathrm{V} + 0.3\,\mathrm{V} = 3.6\,\mathrm{V}.
$$

Five volts is above that. The protection diode conducts, the pin heats, and the chip can die on the first connection. A 5 V HC-SR04 echo is the same problem in a smaller package. Level shifting waits for the pinout lesson; the decision to keep 5 V off the GPIO header is made now.

## Bring-up order

Most “random” firmware bugs in the first week are a rail that sagged. The chip resets, the counter returns to zero, and the sketch you just edited looks guilty. Each step below adds one new thing, so the signature stays obvious.

The laptop must see the board first. On an ESP32 that is a serial port. On a Pico, when you ask for the bootloader, it is a drive named `RPI-RP2`. Then the onboard LED blinks under your program, so a clock and a pin you chose are alive. Then a line of serial at 115200 baud shows that the cable carries data. Then you read a button or a jumper to ground, so an input is real. Then you produce PWM on a pin that has nothing attached except perhaps an LED and a resistor. Only after those five observations do you connect a motor driver and a battery. A TT motor can pull the USB supply down when it stalls. Students who clip the driver on day one spend a week rewriting a loop that was never wrong.

![From a microcontroller sketch toward later ROS work]({{ site.imgurl }}/generated/tracks_mcu_ros.png)

The left side of the figure is this chapter: one microcontroller, a blink, a serial line. Capstone A’s teleop sits further along, still on this chip, with PWM aimed at a TB6612 only after the driver wiring is legal. Later ROS work assumes this bring-up already happened.

## Worked example

An wants a phone to drive a two-wheel robot later in the semester. Chapter 07 is the firmware teleop: PWM toward a TB6612, a timeout near 300 ms, wheels up the first time they may turn. Chapter 08 is where that teleop can use Wi-Fi. An writes: “Primary MCU is an ESP32 NodeMCU-32S with CH340, because I need Wi-Fi in Chapter 08 and a 3.3 V board I can flash this week.”

The bare ESP32-S3-WROOM-1 is cheaper and it does not plug into the laptop. A Pico 2 without W has excellent MicroPython and no radio, so the phone waits. An buys one brain. The line under the sentence is the bring-up order: USB port, onboard LED, `hello` at 115200, a button that reads low when pressed, PWM on an unloaded pin, and only then a TB6612 and a battery, chassis lifted. The Uno stays a 5 V reference.

## Lab

You can do this lab on paper before the parcel arrives.

1. Draw a three-row table. Rows: Uno-class, ESP32 dev board, Pico or Pico 2. Columns: GPIO voltage, built-in wireless, first language you will type, and whether it is the Capstone A brain.
2. Circle one primary row. Under the table write the six bring-up steps in order: USB enumerates, onboard LED, serial at 115200, button read, PWM on an unloaded pin, driver and battery.
3. Add one sentence that names brownout: a sagging rail resets the chip and imitates a software bug.
4. If you are buying this week, copy the exact product name and the price you saw into `lab-notes.md` with the date. If the board is already on the desk, write its silk and its USB-serial chip if one is printed, and do not flash it yet.

You should observe a note that a classmate can audit. A pass names one primary MCU, says what the other two families are for, and lists bring-up in the order above. “I will try both and see” does not pass.

A listing photo of a metal can with no USB socket is a module. A charge-only phone lead lights a power LED and never creates a port. Fix the listing before you fix a driver.

Safety: do not connect a battery, a motor, or a 5 V sensor while you are still choosing the board. The only electrical act today is reading a label.

## Exercises

1. Fill the comparison for Uno-class, ESP32, and Pico, including original Pico versus Pico W and Pico 2 versus Pico 2 W. One cell has to say “5 V GPIO.”
2. A classmate clips a driver and a 2S pack before any serial line works, then says the counter “randomly restarts.” Name the electrical event and the bring-up step they skipped.
3. Compute $$0.7 \times 3.3$$ and $$3.3 + 0.3$$ in volts. In two sentences, say what each number is for, and why a 5 V echo still may not touch the pin.
4. Write your Capstone decision sentence. If you pick the ESP32, name the dev board and say you are not buying a bare WROOM. If you pick a Pico, say how Wi-Fi arrives later.
5. A friend says a Raspberry Pi 5 should be the brain because “robots use Linux.” What does Capstone A actually run on, this semester?

<details>
<summary>Answers</summary>

1. Uno-class: 5 V GPIO, no built-in Wi-Fi, Arduino C++ as the usual first language, poor fit as the Capstone brain next to 3.3 V sensors. ESP32 dev board: 3.3 V GPIO, Wi-Fi and BLE, Arduino via the ESP32 core or MicroPython later, course default when Chapter 08 should use the radio. Original Pico and Pico 2 (no W): 3.3 V GPIO, no built-in Wi-Fi, MicroPython is the fast path. Pico W and Pico 2 W: same 3.3 V family with a radio added.
2. The supply sagged and the chip reset (a brownout). They skipped the chain that ends only after USB, blink, serial, a button, and unloaded PWM have been seen. The restarting counter is the boot path running again.
3. $$0.7 \times 3.3 = 2.31\,\mathrm{V}$$, about 2.3 V, a classroom threshold for “is this high enough to count as high?”. $$3.3 + 0.3 = 3.6\,\mathrm{V}$$, about the absolute maximum region of a 3.3 V pin. A 5 V echo is above 3.6 V, so it can damage the pin even though 5 V is a perfectly normal high on an Uno.
4. A passing ESP32 sentence names a USB dev board (NodeMCU-32S or another DevKit with CH340 or CP2102), Wi-Fi for Chapter 08, and refuses the bare module. A passing Pico sentence names MicroPython, states that the non-W board has no Wi-Fi, and names a later W board or a later switch to the ESP32.
5. Capstone A’s teleop firmware runs on the ESP32 or the Pico. A Pi 5 is a separate Linux computer and does not replace that chip, the data cable, or the bring-up order.

</details>

## Where to buy in Vietnam

The full cart, including the TB6612, motors, and sensors, lives in the Chapter 00 shopping lesson. Buy the brain and a data cable here. Prices below were read from public Hshop listings on 23 September 2026. Read the live page before you pay.

The default dev board is the [ESP32 NodeMCU-32S CH340, 190 000 ₫](https://hshop.vn/kit-rf-thu-phat-wifi-ble-esp32-nodemcu-32s-ch340-ai-thinker). It has USB and a CH340. A second finished board, if you want that listing, is the [Vietduino ESP32, 265 000 ₫](https://hshop.vn/mach-phat-trien-vietduino-esp32). The [ESP32-S3-WROOM-1, 135 000 ₫](https://hshop.vn/mach-thu-phat-wifi-ble-soc-esp32-s3-esp32-s3-wroom-1-chinh-hang-espressif) is a bare module. It is not the starter, even though it costs less.

For the MicroPython track, the verified search [raspberry pi pico](https://hshop.vn/search?q=raspberry+pi+pico) showed a Pico 2 at 195 000 ₫ and a Pico 2 W at 275 000 ₫ on that date. Product pages: [Pico 2 (RP2350)](https://hshop.vn/mach-raspberry-pi-pico-2-rp2350) and [Pico 2 W](https://hshop.vn/mach-raspberry-pi-pico-2-w-rp2350). The non-W Pico 2 has no Wi-Fi.

The cable that matches these micro-USB boards is the [Ugreen Micro-USB 1 m, 54 000 ₫](https://hshop.vn/cap-micro-usb-to-usb-2-0-dai-1m-cao-cap-60136-chinh-hang-ugreen). A charge-only lead enumerates nothing.

Shopee searches, if you compare shops: [ESP32 DevKit CH340](https://shopee.vn/search?keyword=esp32%20devkit%20ch340) and [Raspberry Pi Pico 2](https://shopee.vn/search?keyword=raspberry%20pi%20pico%202). Read whether the photo shows a USB socket. [Thế Giới IC’s ESP32-DevKitC-32U page](https://www.thegioiic.com/esp32-devkitc-32u-module-wifi-bluetooth-2-4ghz) is a dev-board style listing; check whether the antenna is the U.FL version and whether a cable is included. [IC Đây Rồi](https://icdayroi.com/) is a component counter in Thủ Đức, useful later for passives, and easy to misread as a source of a finished USB board.

## Further reading

- [ESP32 datasheet (PDF)](https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf) — GPIO voltage, strapping pins, and the electrical table behind the 2.3 V classroom rule.
- [Raspberry Pi Pico datasheet](https://datasheets.raspberrypi.com/pico/pico-datasheet.pdf) — which board has GPIO 25 as the LED, and what VBUS, VSYS, and 3V3 mean.
- [Raspberry Pi microcontroller documentation](https://www.raspberrypi.com/documentation/microcontrollers/) — Pico, Pico W, Pico 2, and Pico 2 W as a family.
