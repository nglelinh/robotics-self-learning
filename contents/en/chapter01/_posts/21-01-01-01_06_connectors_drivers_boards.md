---
layout: post
title: "Connectors, motor drivers, and MCU boards"
chapter: "01"
order: 6
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter01
lesson_type: required
draft: false
---

## Learning objectives

By the end of this lesson you will be able to tell a 2.54 mm Dupont jumper, which is a signal wire, from a connector that is allowed to carry motor current. You will refuse to force a JST-XH housing onto a servo plug or an XT30 onto an XT60. You will compute the voltage a TT motor actually sees from a 7.4 V pack through a TB6612 versus through an L298N, and you will name the DRV8833 as the smaller substitute with a 1.5 A ceiling that gets hot in a stall. You will distinguish an ESP32 dev board from a bare WROOM module, point at VBUS versus 3V3 on a Pico, and explain why an HC-SR04 echo must not land raw on a 3.3 V GPIO.

## Prerequisites

You can measure DC voltage in parallel, you know a GPIO is a few tens of milliamperes, and you know a stalled TT motor is not. You do not need to PWM a motor yet. This lesson stops at chip markings, pin names, and one voltage-drop calculation before the first wheel turns.

## Why this matters on the diff-drive robot

The capstone is two TT gearmotors, a TB6612, an ESP32 or Pico at 3.3 V, and an HC-SR04. Dupont leads are the right wire for AIN1, AIN2, PWMA, and STBY. They are a poor way to carry stall current into VM, and a worse way to pretend a GPIO is VM.

A 2S pack is about 7.4 V nominal. A MOSFET bridge drops a few tenths of a volt. An L298N, the same price on the day we checked, drops about two volts, so the motors live at the slow end of their range. The HC-SR04 echo pin is a 5 V output, and an ESP32 or Pico GPIO is not a 5 V input. The level shifter is a 10 000 ₫ part. None of this requires firmware. It requires reading the silk before the pack is plugged in.

## Connectors: pitch is not a suggestion

Dupont, the loose square-pin jumper, is built on a 2.54 mm pitch. It is perfect for a breadboard and for logic signals into the TB6612. The contact and the thin wire behind it are not a motor connector. A stall near an ampere warms a tired crimp and drops voltage you already calculated carefully at the driver. Use Dupont for signals. Use a heavier pair of wires, properly secured, for motor current and for the pack leads into VM.

JST-XH is a different family. The pitch is 2.50 mm, not 2.54 mm, which is close enough to tempt a forced fit and different enough to bend the pins. It shows up on balance leads and on small battery pigtails. A hobby servo uses a three-pin JR-style plug, again near 2.54 mm, with a polarity key that is easy to defeat if you shave the shoulder. XT30 and XT60 are bullet connectors for higher current. They do not mate with each other, and they do not mate with JST. If it does not slide home with a firm click and no bent metal, stop. Forcing a housing is how a pack gets reversed onto VM.

## The driver drop, worked at 7.4 V

An H-bridge steers motor current. It does not manufacture that current. The microcontroller tells the bridge which way to close the switches. The pack on VM supplies the amperes.

![The microcontroller steers the bridge; the pack supplies the motor current]({{ site.imgurl }}/generated/hbridge_concept.png)

The TB6612FNG module in the cart is a MOSFET bridge. Hshop's listing, read on 23 September 2026, allows VM from 4.5 V to 10 V, logic from 2.7 V to 5.5 V, 1.2 A continuous and 3.2 A peak. A 3.3 V GPIO is a legal high. A reasonable voltage drop for that style of bridge, at modest current, is a few tenths of a volt. Take 0.3 V as the worked figure:

$$
V_\mathrm{motor} \approx 7.4 - 0.3 = 7.1\ \mathrm{V}
$$

The L298N module was the same 45 000 ₫ and is the part we do not make the default. It is a Darlington bridge. Budget about 2 V of drop at motor current:

$$
V_\mathrm{motor} \approx 7.4 - 2.0 = 5.4\ \mathrm{V}
$$

The TT motors in this course are the 3 V to 9 V class. Five-point-four volts still spins them. It spins them more slowly and with less torque than 7.1 V, and a pack that is no longer fresh makes the gap worse. You also do not use the L298N module's onboard 5 V regulator to run the ESP32.

![An L298N-style module: capable, and a large voltage drop]({{ site.imgurl }}/wikimedia/Dosmotorsl298n.jpg)

The DRV8833 is the smaller substitute, listed at 25 000 ₫, with VM from 2.7 V to 10.8 V and 1.5 A maximum per channel on that Hshop listing. One TT motor per channel is a fair use. A prolonged stall heats a small package quickly. Do not parallel both drive motors onto one DRV8833 channel and call it a spare plan. On the TB6612, STBY must be held high or the bridge stays asleep and the motors sit still while the firmware looks perfect.

## Boards: where 5 V is allowed to exist

An ESP32 development board has a USB socket, a USB-serial chip such as a CH340 or a CP2102 near that socket, a 3.3 V regulator, and a metal-can module. A bare ESP32-WROOM module is the can and the pads, with no USB and no regulator you can plug a cable into. If the part in the bag has no USB connector, you did not buy the dev board the cart asked for, even if the can says ESP32.

![An ESP32 on a small development board, USB and regulator included]({{ site.imgurl }}/wikimedia/ESP32_on_Lolin32_Lite_clone_board_cropped.jpg)

![What to look for on a microcontroller board: USB, regulator, module, headers]({{ site.imgurl }}/generated/pcb_mcu_anatomy.png)

A Raspberry Pi Pico has a dual-row header and no separate metal-can Wi-Fi module on the original part. VBUS is the USB 5 V rail when the board is plugged into a host. 3V3 is the regulated output. GPIO logic is 3.3 V. Do not power the TT motors from 3V3, and do not treat VBUS as a GPIO.

![Raspberry Pi Pico: dual-row header, 3.3 V logic]({{ site.imgurl }}/wikimedia/Raspberry_Pi_Pico.jpg)

![Logic at 3.3 V, USB at 5 V, motor supply kept off that rail]({{ site.imgurl }}/generated/power_rails_3v3.png)

The HC-SR04's trigger pin will usually accept a 3.3 V high. Its echo pin drives out at about 5 V. That echo must not go straight into an ESP32 or Pico GPIO. A 4-channel level shifter, the 10 000 ₫ module on the cart, is the straightforward fix: 3.3 V side toward the microcontroller, 5 V side toward the sensor, grounds common. A resistor divider on echo only is the other option. Two resistors, 10 kΩ on top and 20 kΩ on the bottom, give

$$
V_\mathrm{out} = 5 \times \frac{20}{10 + 20} \approx 3.3\ \mathrm{V}
$$

which a 3.3 V pin can accept. Do not put that divider on a pin the sensor is trying to read as a 5 V input unless you have checked that 3.3 V is a valid high for it. Trig from a GPIO is usually fine without the divider. Echo is the one that bites.

## Hands-on lab

Do this with the pack disconnected and the motors unplugged. Identification first.

1. Photograph the motor-driver chip, close enough that the marking can be read. Write TB6612FNG, DRV8833, or L298N, whichever is actually printed. If the marking is a module vendor's sticker and not the silicon, say so.
2. Photograph the microcontroller's USB-serial chip. CH340 and CP2102 are the common ones on the ESP32 boards in this course. If there is no USB socket and no serial chip, you have a bare module.
3. From the Hshop TB6612 description, label a sketch with AIN1, AIN2, PWMA, STBY, VM, VCC, and GND. Match those names to the silk on your module if you already have it. VM is the motor supply, about 4.5 V to 10 V. VCC is logic, 2.7 V to 5.5 V, so the ESP32 or Pico 3.3 V pin may feed it. GND is the common ground with the microcontroller. STBY must be driven high or the outputs stay off.
4. On the Pico or the ESP32, point at 3V3, at the USB 5 V node (VBUS or the pin marked 5V), and at one GPIO. Say out loud which of those three is allowed to touch an HC-SR04 echo pin. The answer is none of them, until echo has been shifted or divided.

You should finish with two photographs and a labeled sketch, and with every motor lead still in the bag. A correct sketch shows VM and VCC as different pins. If your module ties them together, you have not found a shortcut; you have found a module that cannot take a 7.4 V pack without also forcing that voltage onto the logic pin. Do not power it that way.

| What you see | Likely cause | What to change |
| --- | --- | --- |
| Motors silent, firmware convinced it is driving | STBY left floating or low | Tie STBY high with the logic supply, through the pin the silk names. |
| Robot crawls on a fresh 7.4 V pack | L298N drop, motor seeing about 5.4 V | Use the TB6612. Do not raise the pack above the driver's VM rating to compensate. |
| Dupont connector hot at VM | Signal jumper carrying motor current | Move pack and motor current to heavier wire. Leave Dupont on AIN1, AIN2, PWMA, STBY. |
| GPIO dead after the HC-SR04 was plugged in | Echo at 5 V into a 3.3 V pin | Add the level shifter or the echo divider before the sensor returns. |
| Housing will not mate without force | JST-XH, JR, XT30, and XT60 are different families | Stop. Match the family. Do not shave a key. |

Safety: wheels off the table even though this lab does not spin them. Pack disconnected. Do not probe a pack with your fingers on the metal of the tips. The 7.4 V arithmetic is done on paper until a later lesson measures VM with the meter on a range above 10 V.

## Exercises

1. A pack is 7.4 V. Repeat the drop calculation for a 0.3 V MOSFET bridge and a 2.0 V Darlington bridge. Which voltage does the TT motor prefer, and why is the answer not "buy the L298N because it was also 45 000 ₫"?
2. The DRV8833 listing says 1.5 A maximum per channel. A stall lasts several seconds and the chip is too hot to touch. What limit did you meet, and why is "maximum" not a continuous plan for two motors on one channel?
3. Name three pins on a TB6612 module that a Dupont jumper may carry, and one net it should not.
4. A bag contains a bare ESP32-WROOM and a NodeMCU-32S board. Which one appears as a USB serial port when you plug in a cable, and what chip near the USB socket should you photograph?
5. An HC-SR04 echo wire is landed on a Pico GPIO. What voltage is that wire trying to be, what is VBUS, and what part from the cart goes between them?

<details>
<summary>Suggested answers</summary>

1. MOSFET bridge: $7.4 - 0.3 = 7.1\ \mathrm{V}$. Darlington: $7.4 - 2.0 = 5.4\ \mathrm{V}$. The motor prefers 7.1 V, inside the 3 V to 9 V class with more speed and torque. Equal price does not equal voltage at the terminals.
2. You met the thermal limit of a small package, and you are at the 1.5 A maximum. Maximum is a ceiling, not a cruise. One motor per channel, and a stall that is allowed to sit there will still get hot. Do not parallel both drive wheels on one channel.
3. Dupont is appropriate for AIN1, AIN2, PWMA, and STBY. It should not be the sustained path for VM motor current.
4. The NodeMCU-32S has USB. Photograph the CH340 or CP2102 beside the socket. The bare WROOM has no USB-serial chip until you add one.
5. Echo wants to be about 5 V. VBUS is the Pico's USB 5 V input, not a GPIO and not a place to land echo. The 4-channel level shifter goes between echo and the GPIO, with grounds common. A divider on echo only is the other fix.

</details>

## Further reading

Pololu's TB6612FNG carrier page is the clean statement of what the chip is for, separate from any one marketplace listing: [Pololu TB6612FNG carrier](https://www.pololu.com/product/713). TI's product page for the smaller substitute is [DRV8833](https://www.ti.com/product/DRV8833). SparkFun's logic-level tutorial is the 3.3 V versus 5 V problem the HC-SR04 creates: [Logic levels](https://learn.sparkfun.com/tutorials/logic-levels). The ESP32 numbers behind the GPIO warning live in Espressif's datasheet: [ESP32 datasheet](https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf).

## Where to buy in Vietnam

The rest of the robot, including the chassis, the cells, and the meter, is in [Bill of materials and how to buy the kit in Vietnam]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %}). Prices below are Hshop listings as read on 23 September 2026. Confirm them before you pay.

The default driver was 45 000 ₫: [TB6612FNG](https://hshop.vn/mach-dieu-khien-dong-co-dc-tb6612fng-dc-motor-driver), VM 4.5–10 V, logic 2.7–5.5 V, 1.2 A continuous and 3.2 A peak. The smaller substitute was 25 000 ₫: [DRV8833](https://hshop.vn/mach-dieu-khien-dong-co-drv8833-dc-motor-driver), VM 2.7–10.8 V, 1.5 A maximum per channel. The L298N was also 45 000 ₫ and is not the default, because of the drop you just calculated: [L298N module](https://hshop.vn/mach-dieu-khien-dong-co-dc-l298).

The level shifter for the HC-SR04 echo was 10 000 ₫: [mạch chuyển mức 4 kênh](https://hshop.vn/mach-chuyen-muc-tin-hieu-logic-4-kenh). The ESP32 dev board with USB was 190 000 ₫: [NodeMCU-32S CH340](https://hshop.vn/kit-rf-thu-phat-wifi-ble-esp32-nodemcu-32s-ch340-ai-thinker). A Pico is a search page on Hshop, not a single slug in this list: [search for Raspberry Pi Pico](https://hshop.vn/search?q=raspberry+pi+pico). On 23 September 2026 that search showed a Pico 2 at 195 000 ₫ and a Pico 2 W at 275 000 ₫. Read the current titles before you add one to the cart. Buy a board with USB, not a bare module, unless you already have a programmer.
