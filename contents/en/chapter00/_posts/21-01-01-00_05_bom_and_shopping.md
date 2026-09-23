---
layout: post
title: "Bill of materials and how to buy the kit in Vietnam"
chapter: "00"
order: 5
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter00
lesson_type: required
draft: false
---

Estimated time: **90–120 minutes**, including the spreadsheet lab. Prices below were read from public Hshop product pages on **23 September 2026**. They will move. Treat every đồng figure as a snapshot, then confirm the live listing before you pay.

## Learning objectives

By the end of this lesson you can build a Track A bill of materials for the differential-drive capstone, choose between an ESP32 dev board and a Raspberry Pi Pico using ratings rather than a flash sale, reject an L298N for 3–6 V TT motors and say why in volts, match a lithium cell to a charger that cannot set the pack on fire, and fill `bom.csv` with a vendor, a search keyword, a substitute, and a received/not-received flag for every line.

## Prerequisites

You only need the habit of writing things down. Lesson 00-02 (which track you are on) helps you decide whether Wi-Fi has to be on the microcontroller now. You do not need Ohm's law yet; the driver and battery sections teach the two numbers you must not get wrong. A phone camera is the inspection tool until the multimeter arrives.

## Why it matters

Chapter 07 teleop dies in boring ways: a motor driver that eats two volts, a USB port asked to spin the wheels, a 5 V echo wired into a 3.3 V pin, or a charger that tries to push 4.2 V into an 8.4 V pack. ROS 2 later does not fix any of those. The bill of materials is the parts list that makes the physics match the firmware. Buy the ratings, then the robot.

![Kit families you are shopping for]({{ site.imgurl }}/generated/kit_catalog_overview.png)

![Power comes up in this order: common ground, logic, signals, motor supply last, wheels off the desk]({{ site.imgurl }}/generated/power_order.png)

## What you are actually buying

A bill of materials is a table with one row per physical thing that must exist on the bench, including the screwdriver you already own. It is not a screenshot of a shopping cart. Each row answers six questions: what the part is, how many, what electrical or mechanical rating makes it acceptable, what it does on this robot, what you will accept as a substitute, and where you will buy it. If a row has no rating, you cannot tell a good substitute from a cheaper lookalike.

The default robot in this course is a **differential-drive** platform. Two driven wheels, one idle caster, a 3.3 V microcontroller, a MOSFET motor driver, a ranging sensor, and a motor battery that never shares its current with the microcontroller's 3.3 V pin. Optional rows (IMU, wheel encoders, time-of-flight) wait until the base cart moves under command. Track B adds an Ubuntu 24.04 computer later for ROS 2 Jazzy. Do not buy a LiDAR to feel ready.

```
USB 5 V ---- ESP32 / Pico logic (3.3 V GPIO)
                 |
                GND -------- common with driver GND
                 |
2S 18650 ~7.4 V ---- VM on TB6612 ---- two TT motors
                 |
                 +-- not wired to the 3.3 V pin, ever
```

![Logic rail, USB 5 V, and the separate motor rail]({{ site.imgurl }}/generated/power_rails_3v3.png)

## The default Track A list

Buy in three waves so a delayed chassis does not stop Chapter 01.

**Wave 1, bench (start Chapter 01 this week).** Multimeter, temperature-aware or at least a 60 W iron with a stand, solder, side cutters, solderless breadboard, jumper wires, a data-capable USB cable, the microcontroller, a few LEDs, and a tactile button.

**Wave 2, motion (before Chapter 05).** Chassis or the loose TT motors plus brackets and a caster, TB6612FNG (DRV8833 only as a smaller substitute), HC-SR04, and a 3.3 V / 5 V level shifter for the echo pin.

**Wave 3, energy (after you can measure voltage).** Two 18650 cells in a plausible capacity band, a holder, and a charger that charges **one cell at a time** to 4.2 V. The series holder on the robot is not a charger.

Leave these off the first invoice: RPLiDAR, Raspberry Pi 5, a bench oscilloscope, a 12 V 10 A supply, and any "robot kit" whose driver is an L298N glued to a 4×AA holder with no documentation.

### Consolidated kit table

Ratings in this table are from the manufacturer's usual datasheet or from the Hshop listing cited in the shopping section. Confirm the silk on the part you receive.

| Line | Qty | Acceptable rating | Role on the capstone | Preferred part | Substitute |
|------|----:|-------------------|----------------------|----------------|------------|
| MCU | 1 | 3.3 V GPIO, USB-UART, ≥20 usable pins | Firmware, later Wi-Fi teleop | ESP32 dev board, 30-pin class, CH340 or CP2102 | Pico 2 if you accept USB teleop first and Wi-Fi later |
| Chassis | 1 | Two driven wheels, deck for boards | Diff-drive body | 2WD acrylic TT kit, or Hshop 4WD kit used as two driven wheels plus caster | Loose TT motors, two wheels, two brackets, one caster, any stiff deck |
| TT motor | 2 driven | 3–9 V, gearbox about 1:48 | Left and right drive | Motors included with the chassis | Hshop TT 1:48, 20 000 ₫ each on the listing date |
| Driver | 1 | MOSFET H-bridge, VM about 5–10 V, ≥1 A continuous per channel | Direction and PWM | TB6612FNG module, VM 4.5–10 V, 1.2 A continuous / 3.2 A peak | DRV8833, VM 2.7–10.8 V, 1.5 A max per channel on the Hshop listing; watch heat when stalled |
| Range | 1 | HC-SR04 or a small ToF | Obstacle distance | HC-SR04 | VL53L0X module if you want I²C and 3.3 V from the start |
| Level shift | 1 | 4-channel 3.3 V ↔ 5 V | HC-SR04 echo into ESP32 | MOSFET shifter module | A resistor divider on echo only (not on trig if the module is unreliable at 3.3 V) |
| Motor pack | 2 cells | Li-ion 18650, capacity claim ≤ 3500 mAh | VM through the driver | Cells you charge **outside** the robot | 6×AA (~9 V) if you refuse lithium; do not use a 9 V rectangular battery |
| Charger | 1 | 4.2 V per cell, stops when full | Charge cells one by one | 4-bay 18650 USB charger | A single TP4056 **only** for one cell, never across a 2S holder |
| Meter | 1 | DC volts, ohms, continuity beep | Prove the wiring | UNI-T UT33D+ or a cheaper true-RMS hobby meter | Any meter with a continuity beeper; avoid a meter with no current fuse if you will measure amps |
| Iron | 1 | ~60 W, stand, 0.8 mm solder | Harnesses | Fixed 60 W iron is enough for Dupont and headers | A station later; not required to start |
| Prototype | 1 | 830-tie breadboard, M-M and M-F jumpers | Chapters 01–03 | — | 400-tie board if you keep leads short |
| Fasteners | 1 set | M3 screws, nylon standoffs | Hold the MCU off the metal | Often included with the chassis | A small M3 assortment from any hardware stall |

## Why the driver row is not "any H-bridge"

The L298N module on Hshop is the same **45 000 ₫** as the TB6612FNG module (SKUs HS0695V and HS2458V on the day this lesson was written). The price is not the difference. The L298N is a Darlington bridge. At motor current it drops roughly 1.8 V to 2.5 V between the battery and the motor. The TB6612FNG is a MOSFET bridge; the motor sees nearly the full motor supply.

$$
V_{motor} \approx V_{bat} - V_{drop}
$$

Work the two cases for a 2-cell pack at 7.4 V nominal and a 2.0 V Darlington drop versus a 0.3 V MOSFET drop:

$$
V_{L298} \approx 7.4 - 2.0 = 5.4\,\text{V}
$$

$$
V_{TB6612} \approx 7.4 - 0.3 = 7.1\,\text{V}
$$

The Hshop TT motor listing (ratio 1:48) recommends **3–9 V**, quotes no-load current **110–150 mA**, and quotes about **200–208 rpm at 5–6 V** with **0.8 kg·cm at 6 V**. Five volts is already the slow, weak end of that listing. A fresh 4×AA pack is only 6 V before the L298N drop, so the motor can be left near 4 V and the robot crawls. The same module also carries a 7805 regulator that you must not use to feed an ESP32 when the motor supply is above 12 V; our pack stays under 10 V, and you still do not power the microcontroller from that regulator. Logic for the TB6612FNG is **2.7–5.5 V**, so a 3.3 V GPIO is a valid high. Tie STBY high or the bridge stays asleep.

The DRV8833 module is **25 000 ₫** and the Hshop listing allows VM **2.7–10.8 V** with **1.5 A maximum per channel**. That is a fair substitute for one TT motor per channel. It has less copper and a smaller package than a TB6612 carrier, so a prolonged stall smells like hot plastic sooner. Do not parallel two motors on one DRV8833 channel.

Stall current is not the no-load number. The listing does not publish stall current. Budget roughly several times 150 mA and **measure** it later with the wheels in the air and the meter in series for a short pulse. If you only buy a driver because the sticker says 2 A, you have not finished the row.

![H-bridge idea: the microcontroller steers current, it does not supply the motor current]({{ site.imgurl }}/generated/hbridge_concept.png)

## Cells, holders, and chargers are one decision

A single 18650 is about 3.6–3.7 V nominal and **4.2 V full**. Two in series, which is what a "2×18650 nối tiếp" holder does, are about **7.4 V nominal and 8.4 V full**. That voltage belongs on the driver VM pin. It does not belong on a GPIO, and it does not belong on a TP4056.

The TP4056 boards on Hshop (the USB-C module at 10 000 ₫ and the mini-USB module at 2 000 ₫) are **single-cell** chargers. They try to bring one cell to 4.2 V at about 1 A. If you clip one across a series pair, you are asking a 4.2 V charger to operate on an 8.4 V stack, or you are charging only a fraction of the pack while the cells drift apart. Either way the row is wrong. Charge each cell by itself in a bay charger, check that the open-circuit voltage sits between about 3.6 V and 4.20 V, then insert the cells into the holder. The 4-bay USB charger on Hshop was **68 000 ₫** (listing title: 14500 / 18650 / 21700). Use one bay until you trust it.

Capacity claims have a physical ceiling. A real 18650 is rarely above about 3500 mAh, and honest mid cells sit nearer 2000–3000 mAh. Hshop's Sunpower cells were listed at **2000 mAh for 35 000 ₫** and **2500 mAh for 45 000 ₫**. A marketplace listing that says 9900 mAh or 12000 mAh for a similar price is fiction. The "10C" marking on those Sunpower titles is a discharge-rate claim, not a capacity. Do not believe a C-rating without a datasheet; two TT motors do not need a fantasy C-rating anyway.

These hobby cells often arrive **without** a protection PCB. A screwdriver across the terminals can dump tens of amps. Do not carry loose cells in a pocket with keys. Do not charge them on a bed. Stop if a cell is swollen, below about 2.5 V, or hot. A 9 V rectangular battery is the other classic mistake: its internal resistance collapses as soon as a motor stalls, and the microcontroller resets while the driver is still commanded on.

During bench work, power the microcontroller from USB. Common the USB ground with the driver ground. Switch the motor battery on last, and only with the wheels off the table.

## Buying strategy

Buy the rating, not the thumbnail. A 30 % sticker on an L298N bundle is still the wrong bridge. Read voltage, continuous current, logic level, and connector gender before you read the discount.

Order Wave 1 from one shop so a missing USB cable does not wait on a second parcel. In Vietnam, Hshop (hshop.vn, shop at 269/20 Lý Thường Kiệt, Phường Phú Thọ, TP.HCM) publishes a technical listing and a SKU. Their own note says a SKU ending in **V** is a company invoice price that already includes VAT. They also ask you to film the unboxing within seven days if you want their basic warranty. Shopee and Lazada are search markets: sort by shop rating, read whether the listing is a module or a dev board, and prefer shops that show the chip marking. Thế Giới IC (thegioiic.com) and IC Đây Rồi (icdayroi.com, Thủ Đức) are component counters. They are excellent for an ESP32 **module** or a loose regulator, and easy to misread as a USB dev board.

Pay the electronics shop after they confirm stock if you are transferring. Marketplace escrow is fine for jumpers and chassis kits. Do not pay a stranger on social media for "tested 18650 cells" with no return path.

When the parcel arrives, do this before you celebrate:

1. Film the opening. Count bags against `bom.csv`.
2. Meter: continuity beeps on a shorted probe pair, then about 5 V on a USB charger you already trust.
3. Microcontroller: plug the **data** cable into your computer. A new serial port must appear. A charge-only cable gives silence and looks like a dead board.
4. With only USB connected, the 3.3 V pin reads about 3.3 V. If it reads 5 V, stop.
5. Driver: the chip text matches TB6612FNG or DRV8833, not L298N.
6. Motors: shafts turn by hand without grit. Gearbox ratio on the bag matches the row you paid for.
7. Cells: not swollen, voltage of each cell between about 3.4 V and 4.2 V. Do not series them until both readings exist.

## Where to buy in Vietnam / Mua ở Việt Nam

Links below are either a **product page that returned a price on 23 September 2026** or a **search page**. Search pages are labeled. Do not treat a search URL as a promise that the first hit is the right part. Shopee keyword links are search pages. Lazada's public catalog search is `https://www.lazada.vn/catalog/?q=` plus the keyword; an automated browser sometimes hits a captcha, a normal browser shows listings.

### Microcontroller

Search: `ESP32 NodeMCU 38 chân CH340`, `ESP32 DevKit V1`, `Raspberry Pi Pico 2`.

- Hshop product (verified): [ESP32 NodeMCU-32S CH340 Ai-Thinker, 190 000 ₫](https://hshop.vn/kit-rf-thu-phat-wifi-ble-esp32-nodemcu-32s-ch340-ai-thinker). This is a USB dev board. Buy this class of board.
- Hshop product (verified, more expensive): [Vietduino ESP32, 265 000 ₫](https://hshop.vn/mach-phat-trien-vietduino-esp32).
- Hshop product (verified, **not** what you want as the only computer): [ESP32-S3-WROOM-1 module, 135 000 ₫](https://hshop.vn/mach-thu-phat-wifi-ble-soc-esp32-s3-esp32-s3-wroom-1-chinh-hang-espressif). A module has no USB-UART until you add one.
- Hshop search (verified search page): [raspberry pi pico](https://hshop.vn/search?q=raspberry+pi+pico) listed Pico 2 at 195 000 ₫ and Pico 2 W at 275 000 ₫.
- Thế Giới IC product (verified page exists): [ESP32-DevKitC-32U](https://www.thegioiic.com/esp32-devkitc-32u-module-wifi-bluetooth-2-4ghz). Read whether the antenna is the U.FL version (DevKitC-32U) and whether a cable is included.
- Shopee search: [ESP32 DevKit](https://shopee.vn/search?keyword=esp32%20devkit%20ch340).
- Avoid a picture of a bare metal can with no USB socket if the title says "kit phát triển".

### Chassis, motors, caster

Search: `khung xe robot 2 bánh TT`, `động cơ giảm tốc TT 1:48`, `bánh đa hướng`.

- Hshop did **not** show a cheap 2WD acrylic kit on the searches run for this lesson. It did show the [MKE-R01 4WD TT chassis at 245 000 ₫](https://hshop.vn/khung-xe-mke-r01-4wd-robot-car-chassis-tt-motor). Use two of its motors for the capstone and keep two as spares, and add a caster, **or** run left wheels together and right wheels together only after you have measured current.
- Loose parts, verified: [TT motor 1:48, 20 000 ₫](https://hshop.vn/dong-co-dc-giam-toc-tt-motor-ti-so-1-48), [65 mm wheel, 8 000 ₫](https://hshop.vn/banh-xe-dong-co-dc-giam-toc-v1-plastic-geared-tt-motor-65mm), [bracket, 10 000 ₫](https://hshop.vn/ga-bat-dong-co-dc-giam-toc-tt-motor-mounting-bracket), [caster, 15 000 ₫](https://hshop.vn/banh-xe-nhua-da-huong-3pi-ball-caster-wheel).
- Shopee search (search page, price not fetched): [khung xe 2 bánh TT](https://shopee.vn/search?keyword=khung%20xe%20robot%202%20b%C3%A1nh%20TT). Street listings are often in a **90 000–180 000 ₫** band; confirm the photo shows two motors, a caster, and a battery box.
- Lazada search: [khung xe robot](https://www.lazada.vn/catalog/?q=khung%20xe%20robot%202%20banh).
- Avoid a "robot kit" that only shows an L298N and a 4×AA box and calls itself complete.

### Motor driver

Search: `TB6612FNG`, `DRV8833`, not `module L298 giá rẻ` as the default.

- Verified: [TB6612FNG, 45 000 ₫, SKU HS2458V](https://hshop.vn/mach-dieu-khien-dong-co-dc-tb6612fng-dc-motor-driver). VM 4.5–10 V, logic 2.7–5.5 V, 1.2 A continuous, 3.2 A peak, 20×20 mm.
- Verified substitute: [DRV8833, 25 000 ₫](https://hshop.vn/mach-dieu-khien-dong-co-drv8833-dc-motor-driver). VM 2.7–10.8 V, 1.5 A max per channel on that listing.
- Verified part to **not** make the default: [L298N module, also 45 000 ₫](https://hshop.vn/mach-dieu-khien-dong-co-dc-l298). Buy it only if you already understand the drop and your motors are 12 V class.
- Shopee search: [TB6612FNG](https://shopee.vn/search?keyword=tb6612fng).
- Pololu's carrier is a trustworthy reference design if you later import one: [Pololu 713](https://www.pololu.com/product/713).

### Sensors

Search: `HC-SR04`, `VL53L0X`, `MPU6050 GY-521`, `đĩa encoder TT 20 xung`.

- Verified: [HC-SR04, 27 000 ₫](https://hshop.vn/cam-bien-sieu-am-srf04). Echo is a 5 V output. Buy the shifter with it.
- Verified shifter: [4-channel logic level, 10 000 ₫](https://hshop.vn/mach-chuyen-muc-tin-hieu-logic-4-kenh).
- Verified later row: [GY-521 MPU6050, 85 000 ₫](https://hshop.vn/cam-bien-6-dof-bac-tu-do-gy-521-mpu6050). I²C, 3.3–5 V supply on that listing, 3.3 V logic. Not required to blink an LED.
- Verified ToF substitute: [VL53L0X module, 115 000 ₫](https://hshop.vn/cam-bien-khoang-cach-tof-laser-radar-vl53l0x).
- Encoder disc, verified but easy to lose: [20-count disc, 1 000 ₫](https://hshop.vn/dia-encoder-20-xung-dong-co-dc-giam-toc-v1). The sensor module is a separate row; search `cảm biến tốc độ encoder hồng ngoại`.
- Shopee: [HC-SR04](https://shopee.vn/search?keyword=hc-sr04).

### Power

Search: `pin 18650 2500mAh`, `sạc 18650 4 ngăn`, `TP4056` only if you know it is one cell.

- Verified cells: [Sunpower 2500 mAh, 45 000 ₫](https://hshop.vn/pin-sac-18650-li-ion-rechargeable-battery-3-7v-2500mah-10c-sunpower), [2000 mAh, 35 000 ₫](https://hshop.vn/pin-sac-18650-li-ion-rechargeable-battery-3-7v-2000mah-10c-sunpower).
- Verified holder, solder tabs: [2×18650 holder, 4 000 ₫](https://hshop.vn/hop-pin-2-co-18650). The chassis kit may already include a spring holder. Do not buy both and then series four cells.
- Verified solderless holder: [DIY 18650 holder, 10 000 ₫](https://hshop.vn/hop-pin-ghep-noi-diy-solderless-18650-battery-holder).
- Verified bay charger: [4-bay USB charger, 68 000 ₫](https://hshop.vn/bo-sac-pin-18650-li-ion-usb-battery-charger-yh-18650-4).
- Verified single-cell board, **not** for the 2S pack: [TP4056 USB-C, 10 000 ₫](https://hshop.vn/mach-sac-pin-tp4056-lithium-battery-charge-controller-usb-c).
- Shopee search: [sạc pin 18650](https://shopee.vn/search?keyword=s%E1%BA%A1c%20pin%2018650%204%20ng%C4%83n).
- Avoid "sạc nhanh 2A" boards with no current resistor you can see, and any cell whose label exceeds 3500 mAh.

### Bench tools and prototype

Search: `đồng hồ vạn năng`, `mỏ hàn 60W`, `breadboard 830`, `dây breadboard đực cái`.

- Verified meters: [UNI-T UT33D+, 285 000 ₫](https://hshop.vn/dong-ho-van-nang-dien-tu-digital-multimeter-uni-t-ut33d-chinh-hang), [Wadfow WDM1501, 185 000 ₫](https://hshop.vn/dong-ho-van-nang-ky-thuat-so-vom-wadfow-wdm1501-digital-multimeter-true-rms). The UT136C+ at 560 000 ₫ is a later upgrade, not the student default.
- Verified iron: [Wadfow WEL3616 60 W, 75 000 ₫](https://hshop.vn/mo-han-60w-wadfow-wel3616-soldering-iron), [stand, 40 000 ₫](https://hshop.vn/de-gac-mo-han-tron-b-2-co-khay-roi), [0.8 mm Sn63 solder, 24 000 ₫](https://hshop.vn/thiec-han-sunchi-kp26-0-8mm-sn63-pb37-solder-wire).
- Verified cutters: [170 mm flush cutter, 35 000 ₫](https://hshop.vn/kim-cat-day-dien-nho-170-cat-chan-linh-kien-dien-tu). Stripper, if you want one tool that does not nick the copper: [Wadfow WBQ8401, 130 000 ₫](https://hshop.vn/kim-tuot-day-dien-da-nang-wadfow-wbq8401-wire-stripper).
- Verified prototype: [830-point breadboard, 35 000 ₫](https://hshop.vn/test-board-cammb-102), [M-M jumpers, 30 000 ₫](https://hshop.vn/day-cam-breadboard-duc-duc-20cm-cap-det-40-soi-m-m-jumper-wire), [M-F jumpers, 30 000 ₫](https://hshop.vn/day-cam-breadboard-duc-cai-20cm-cap-det-40-soi-m-f-jumper-wire), [breadboard power module, 25 000 ₫](https://hshop.vn/mach-cap-nguon-cho-breadboard-400-830-lo-mb-102). Skip the power module until you know which rail is 3.3 V and which is 5 V.
- Verified cable: [Ugreen Micro-USB 1 m, 54 000 ₫](https://hshop.vn/cap-micro-usb-to-usb-2-0-dai-1m-cao-cap-60136-chinh-hang-ugreen). A 30 cm cable at 27 000 ₫ exists and is annoyingly short on a robot. Match USB-C if your board is USB-C.
- Verified small parts: [3 mm LED assortment, 20 000 ₫](https://hshop.vn/bo-5-loai-led-sieu-sang-3mm-thong-dung-5-kind-3mm-transparent-color-led), [round pushbutton, 10 000 ₫](https://hshop.vn/nut-nhan-nha-tron-pbs-11b-12mm-kem-cap), [red/black wire, 1 m, 8 000 ₫](https://hshop.vn/day-dien-do-den).
- Resistor assortments were **not** on the first Hshop page for `điện trở` (that search returned shunts and LCDs). Use Shopee search [bộ điện trở 1/4W](https://shopee.vn/search?keyword=b%E1%BB%99%20%C4%91i%E1%BB%87n%20tr%E1%BB%9F%201%2F4W) and expect roughly **30 000–80 000 ₫**. You want 220 Ω, 330 Ω, 1 kΩ, and 10 kΩ in the mix.
- Shopee tool search: [mỏ hàn 60W](https://shopee.vn/search?keyword=m%E1%BB%8F%20h%C3%A0n%2060W), [đồng hồ vạn năng](https://shopee.vn/search?keyword=%C4%91%E1%BB%93ng%20h%E1%BB%93%20v%E1%BA%A1n%20n%C4%83ng).
- IC Đây Rồi for passives if you are in Thủ Đức: [icdayroi.com](https://icdayroi.com/). Thế Giới IC: [thegioiic.com](https://www.thegioiic.com/).

Dupont jumpers are signal wires. Motor current belongs on the thicker red/black lead, screwed or soldered to the driver terminals, not on a breadboard row.

## Worked cart: Lan's Track A under 2 000 000 ₫

Lan is on Track A. She wants Wi-Fi teleop in Chapter 08, so the microcontroller is the ESP32 NodeMCU-32S, not the Pico. She has no lithium experience, so the cart includes a bay charger and forbids a TP4056 across the holder. She will pull two motors out of the 4WD kit, fit a caster, and keep the other two motors as spares. Prices are the Hshop snapshots above.

| Line | Qty | Unit (₫) | Line (₫) |
|------|----:|----------:|----------:|
| ESP32 NodeMCU-32S CH340 | 1 | 190 000 | 190 000 |
| MKE-R01 4WD chassis (use 2 motors) | 1 | 245 000 | 245 000 |
| Caster | 1 | 15 000 | 15 000 |
| TB6612FNG | 1 | 45 000 | 45 000 |
| HC-SR04 | 1 | 27 000 | 27 000 |
| 4-channel level shifter | 1 | 10 000 | 10 000 |
| Breadboard 830 | 1 | 35 000 | 35 000 |
| Jumper M-M and M-F | 2 | 30 000 | 60 000 |
| Ugreen Micro-USB 1 m | 1 | 54 000 | 54 000 |
| UNI-T UT33D+ | 1 | 285 000 | 285 000 |
| Iron 60 W + stand | 1+1 | 75 000 + 40 000 | 115 000 |
| Solder 0.8 mm | 1 | 24 000 | 24 000 |
| Flush cutter | 1 | 35 000 | 35 000 |
| 18650 2500 mAh | 2 | 45 000 | 90 000 |
| 4-bay charger | 1 | 68 000 | 68 000 |
| MPU6050 (optional, she keeps it) | 1 | 85 000 | 85 000 |
| LED assortment + button + 1 m wire | 1 | 20 000 + 10 000 + 8 000 | 38 000 |
| **Parts** | | | **1 421 000** |

A resistor assortment at a stated Shopee band of 50 000 ₫, plus a typical inner-city ship of 30 000 ₫, lands near **1 500 000 ₫**. That is inside a 1 500 000–2 500 000 ₫ student budget with room for M3 standoffs and a second USB cable. Swapping the meter for the Wadfow at 185 000 ₫ saves 100 000 ₫. Swapping the ESP32 for a Pico 2 at 195 000 ₫ does not save money and postpones Wi-Fi. Adding a second TB6612 instead of the caster, and driving all four motors as two pairs, is a different robot; Lan writes that as a rejected alternate, not as a silent edit.

She does not add an L298N "because it is also 45 000". At 7.4 V and a 2.0 V drop the motors would see 5.4 V. On the Hshop motor listing, 5–6 V is 200 rpm and 0.8 kg·cm at 6 V. She wants the 7 V side of that curve, so the MOSFET driver stays.

## Lab: build `bom.csv` and inspect the idea of the kit

Create `bom.csv` in your notes folder with this header:

```text
part_id,name,qty,role,rating,vendor,url_or_search,unit_vnd,line_vnd,substitute,wave,received,photo,notes
```

**Procedure**

1. Copy every line from Lan's table, then delete or defer the MPU6050 if it blows your budget. Add a resistor-assortment row whose price is "Shopee band, confirm listing" until you have a real number.
2. Add three columns you will actually use: `received` (yes/no), `photo` (filename), and `notes` (chip marking you can read).
3. For the driver row, write the VM range and the sentence "not L298N" in `notes`.
4. For the charger row, write "one cell per bay, never across 2S holder".
5. If the parcel has not arrived, set `received` to no and still finish the sheet. Photograph the meter and the board the day they do arrive.
6. Compute the column sum in a spreadsheet. If it exceeds 2 500 000 ₫, the first cuts are the IMU, the stripper, and the breadboard power module, in that order. Do not cut the meter or the driver.

**You should see**

A sum you can explain to a classmate in one minute, a driver row whose substitute is DRV8833 and whose rejected part is L298N, and a charger row that cannot be satisfied by a TP4056 on a series holder.

**Faults**

| What you notice | What it usually means | Fix |
|-----------------|----------------------|-----|
| Cart looks cheap but the driver is L298N | Drop was ignored | Replace the row; do not "fix" it in software |
| ESP32 row links to a WROOM module | No USB | Replace with a dev board that has a USB socket |
| Two cells plus one TP4056 | Charger voltage is 4.2 V, pack is 8.4 V | Bay charger, cells charged alone |
| 9900 mAh in the capacity column | Counterfeit claim | Refuse the listing |
| Sum uses a 30 cm cable | Robot USB tether will not reach | Buy the 1 m data cable |
| Motors on Dupont wires in the notes | Breadboard will brown out or melt | Screw terminals and the red/black lead |

**Safety.** Lithium cells are the hazard in this lesson, not the spreadsheet. Charge where you can see the cell. Do not short the holder. Do not connect VM to the ESP32 5 V or 3.3 V pin to "test the battery".

## Exercises

1. A 2S pack sits at 8.0 V. The L298N drops 2.2 V and the TB6612 path drops 0.4 V. What voltage reaches one TT motor in each case, and which one is inside the comfortable middle of the 3–9 V motor listing?
2. Your holder is marked nối tiếp. You own one TP4056. Describe the exact sequence that charges both cells without putting the charger across the series pair.
3. A Shopee title says "ESP32 WiFi Bluetooth" and the photo is a metal-covered module with castellated edges and no USB connector. What row of the BOM is this, and what extra part is still missing?
4. HC-SR04 echo is 5 V. Your GPIO is 3.3 V. Name the part you add, and name one measurement that proves you have not connected echo straight to the pin.
5. The parts sum is 1 420 000 ₫ before shipping. Shipping is 35 000 ₫ and a resistor kit is 55 000 ₫. Is Lan still inside a 2 000 000 ₫ cap if she also adds a second TB6612 at 45 000 ₫? Show the arithmetic.

<details>
<summary>Suggested answers</summary>

1. L298 path: $$8.0 - 2.2 = 5.8\,\text{V}$$. TB6612 path: $$8.0 - 0.4 = 7.6\,\text{V}$$. Both are inside 3–9 V. 7.6 V is the stronger, faster point on the listing's 6 V torque figure; 5.8 V is the sluggish end.
2. Remove the cells. Charge cell A in one bay until the charger stops near 4.2 V. Repeat for cell B. Measure both. Only then insert them into the series holder. The TP4056 may charge one loose cell; it must not be clipped to the two holder terminals.
3. It is a bare module, not the MCU dev-board row. You still need a dev board or a USB-UART programmer and a 3.3 V regulator. Do not start the course on a bare module.
4. Add the 4-channel level shifter (or a divider on echo). With the sensor powered and echo not yet on the GPIO, a meter on the echo pin during a ranging pulse must not be wired to the ESP32. The safe check is continuity: echo net and GPIO net are not the same net until the shifter low-voltage side is in between.
5. $$1\,420\,000 + 35\,000 + 55\,000 + 45\,000 = 1\,555\,000$$. Yes, still under 2 000 000 ₫. The second driver is a design change (four motors), not a free spare, so the notes column should say so.

</details>

## Further reading

- [TB6612FNG product page and ratings, Pololu 713](https://www.pololu.com/product/713) — MOSFET carrier the Hshop module is copying.
- [TI DRV8833 product folder](https://www.ti.com/product/DRV8833) — current limits and VM range for the cheap substitute.
- [Pololu brushed DC motor driver comparison](https://www.pololu.com/category/11/brushed-dc-motor-drivers) — why "2 A" on a Darlington board is not the whole story.
- [SparkFun logic levels](https://learn.sparkfun.com/tutorials/logic-levels) — 5 V echo versus 3.3 V GPIO.
- [Battery University, BU-409 charging lithium-ion](https://batteryuniversity.com/article/bu-409-charging-lithium-ion) — 4.20 V per cell, why series packs need a charger that understands series.
- [Espressif ESP32 datasheet](https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf) — absolute maximum on a GPIO is not 5 V.
- [HC-SR04 module note, SparkFun](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf) — trigger and echo timing; treat echo as 5 V.
