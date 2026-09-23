---
layout: post
title: "Chapter 00 lab checklist: the bench is ready"
chapter: "00"
order: 7
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter00
lesson_type: required
draft: false
---

This is the exit gate for Chapter 00. Plan 60–90 minutes, mostly checking evidence from lessons 00-01 through 00-06. A tick without a file, a photo, or a pasted line does not count. Chapter 01 will ask you to measure real parts. Do not start it on a vibe.

## Learning objectives

You will **audit** the bench with a written procedure, one item at a time. You will **attach** evidence to each item: a `bom.csv` sum, a meter beep on a known short, a serial port or an explicit plan if the board has not arrived, a Track A or Track B sentence, a charger photo or a note that cells are not purchased yet, and the power-up card from lesson 00-03. You will **separate** a missing tool that blocks Chapter 01 from a missing chassis that does not. You will **predict** which missing line would make the first electronics lab unsafe. You will **list** only the gaps you will buy, using lesson 00-05 as the cart rather than a new one.

## Prerequisites

You need the journal, the track sentence, the power-up card, the Wave 1 inventory photo, and whatever `bom.csv` lesson 00-05 asked you to build. If one of those was skipped, the audit records the skip. You do not need a moving robot, ROS 2, or a soldered joint. You do need to be willing to leave a box unticked.

## Why it matters

Capstone A stops the wheels when commands go silent for about 300 ms. That behaviour needs a bench that can tell a ground from a wish. Later ROS 2 topics will describe the same robot. They will not repair a Chapter 01 session that measured ohms on a live rail, or a lithium cell that arrived with no charger decision. This gate finds, while the parts are still in bags, which missing evidence would make the next chapter unsafe.

![The order on the power-up card is one of the items this audit must see]({{ site.imgurl }}/generated/power_order.png)

If you cannot find the card, you do not redraw it from memory during the audit and call it old. You redo lesson 00-03's page and then you photograph it. The figure is a reminder of the sequence: common ground, logic, signals, motor supply last, wheels up.

## What counts as evidence

A tick is a claim that a specific artifact exists. The artifact has to be something you could hand to another student.

The **bill of materials** counts when `bom.csv` (or the same table in the journal) has a sum you wrote yourself, with a date. A screenshot of a shop homepage with no total is not a sum. If lesson 00-05 is unfinished, the line is open, and you finish that lesson before you pretend Chapter 00 is closed.

The **meter** counts when the journal says the probes were touched together and the meter beeped, or when it records the failure ("no beep; fuse or battery"). A photo of a meter in a shopping cart does not beep. If the meter has not arrived, the line stays open. Chapter 01's continuity work is blocked until it closes. That is the correct outcome, not a negotiated pass.

The **USB cable** counts in one of two ways. A serial port appeared when the board was plugged in, and the name is pasted in the journal, and it disappeared when you unplugged. Or the board has not arrived, and the journal contains a written plan: USB only, no motor supply, record the port, unplug. A cable that only lights an LED has not proved data. Write `unproven` rather than ticking the line.

The **track sentence** counts when it names Track A or Track B, the MCU (ESP32 or Pico 2), and the refusal to buy a LiDAR before Capstone A. "I like robots" is not a track.

The **charger** counts when a photo shows a label you can read (Li-ion, 4.2 V, one cell), or when the journal says `cells not purchased yet`. A bare cell with no note is an open safety item, not a neutral. A TP4056 pictured while clipped across a 2S holder is evidence of a problem, not a tick.

The **power-up card** counts when the photo or the page itself shows common ground, USB logic, signals, VM last, wheels up, the 300 ms PWM stop, and the ban on motor voltage and 5 V echo into a 3.3 V GPIO. A card that starts with the battery fails the item even if the paper exists.

The **workspace** from lesson 00-06 counts when the directories exist and the install log has versions or the words `not installed`. An empty `ros_ws/` with that honesty is a pass. A `ros_ws/` full of clones you did not mean to keep is a mess you clean before you tick.

## The audit procedure

Do this in order. Do not skip to the items you know you passed.

Open the journal and add a heading `Chapter 00 exit`. Copy the seven evidence items above as lines you will mark `pass` or `open`.

Read `bom.csv` and write the total in đồng on the exit heading, plus the date the prices were copied. If you cannot find the file, mark `open` and stop claiming the shopping lesson is done. Open the Wave 1 photo from lesson 00-04 and check it against the lines: meter, iron, stand, solder, cutters, breadboard, jumpers, data cable, MCU, LED, button. Mark each `here` or `gap`. The chassis and the driver are Wave 2. Their absence does not fail Chapter 00. Their presence does not excuse a missing meter.

Perform the beep test again, even if you did it last week. Probes together, meter in continuity, circuit unpowered. Write "beep" or what happened instead. If you are about to measure a powered USB rail in ohms because the beep failed, stop. That is the fault the rule exists to prevent.

Check the USB evidence. If the board is on the desk, plug it in with no motor battery connected, paste the port name, and unplug. If the board is not on the desk, read the written plan and confirm it forbids VM on that first plug-in. If there is no plan and no port, the item is open.

Read the track sentence aloud. Confirm it mentions the 300 ms stop and names TB6612FNG rather than an L298N if a driver is already in the spreadsheet. If the spreadsheet says L298N, the shopping lesson's voltage-drop arithmetic has not been applied. Mark the driver line `open` even if the rest of the track sentence sounds confident.

Look at the charger evidence. Either the photo's label matches one cell at 4.2 V, or the note says cells are not purchased yet. If a 2S holder and a TP4056 are in the same photo and connected, disconnect them before you continue the audit, and do not tick the line.

Find the power-up card. Compare it to the figure at the top of this lesson. If VM is not last, rewrite the card. Photograph the version you would actually follow.

Open the firmware folder and `ros_ws/README.md`. Confirm the install log matches the computer in front of you. Delete nothing you still need, but remove the claim that Jazzy is installed if the machine is Windows.

**What you should see when the gate is honest.** The exit heading lists pass or open for every item. The sum, the beep, the port or the plan, the track sentence, the cell decision, and the card are each a real artifact. Open items name the lesson that closes them: 00-04 for a missing stand, 00-05 for a missing sum, 00-03 for a missing card, 00-06 for a missing folder.

**What you should see when someone is rushing.** Every line says pass, and the only attachment is "looks good." Put `open` back on any line you cannot point at in a minute.

## Worked example

My's exit note, written after she actually looked, reads as follows. `bom.csv` sum 1,620,000 ₫, prices dated 23 Sep 2026, file in `notes/`. Meter: beep on a known short, repeated today. USB: board not arrived; plan is "USB only, no VM, paste the port, unplug; cable in the drawer is unproven until that port appears." Track: "Track A, ESP32, TB6612FNG, no LiDAR before wheels-up teleop with a 300 ms stop. Track B on the lab Ubuntu PC after Chapter 07." Cells: `not purchased yet`. Power-up card: photographed, VM last, wheels-up line present. Install log: Arduino IDE not installed on the laptop, Jazzy not installed, Gazebo Harmonic named only.

She ticks the written plan, not a proved cable, and leaves `cable unproven` visible. Gaps: a stand (40000 ₫ on the 23 Sep 2026 snapshot) and jumpers. The missing chassis is Wave 2 and does not block Chapter 01. The missing stand blocks soldering, so a hot iron stays off the desk. Metering and identification may start.

A second student, Khoa, has a beep, a card, and a track sentence, and also a photograph of a TP4056 wired across two cells because "the connector fit." His charger line is `open`, and the photo is evidence of a fault, not of readiness. He disconnects the module, writes that each cell will be charged alone to 4.2 V or not at all, and only then may he reconsider the tick. His `bom.csv` has no sum. He goes back to lesson 00-05 before he calls the gate passed. A messaging stack on Ubuntu would not have caught either miss.

## Exercises

These ask you to find the unsafe gap. They are about your audit, or about the audits below, not about restating the chapter.

1. Chapter 01's first measurement lab asks for continuity and DC volts. Which single open item in your exit list makes that lab dishonest or unsafe, and what evidence would close it?
2. A student ticks "USB cable proved" because the board's LED lights. No port name is written. Why is the tick false, and what could go wrong in Chapter 02 if they keep it?
3. The power-up card is missing, and the student says Chapter 01 has no motors so the card can wait. Name one Chapter 01 action (probing, soldering, or a lithium cell already on the shelf) that the card was supposed to constrain anyway.
4. `bom.csv` lists an L298N and a 2S holder, the sum is blank, and the track sentence says "ROS first." Which of those three facts would make a later motor test unsafe even if Chapter 01's resistor lab is fine? Explain with the roughly 2 V drop or with the charger rule.
5. Cells are not purchased, the meter beeps, the card exists, and `ros_ws/` is empty on Windows with that fact written down. May this student start Chapter 01's unpowered identification labs? What are they still forbidden to do?

<details>
<summary>Suggested answers</summary>

1. An open meter line: no beep on a known short means every later "0 Ω" or "3.3 V" is untrustworthy, and a student who then tries current or ohms at random can short a port. Close it with a beep, probes touching, written in the journal. A missing chassis does not do this damage.
2. The LED only shows that power arrived. A charge-only cable never enumerates a serial port, so Chapter 02's upload fails in a way that looks like a bad board. The tick needs a port name that appears and disappears with the plug, or an explicit unproven plan.
3. Soldering still needs the stand, glasses, and ventilation. A cell on the shelf still needs "one cell, 4.2 V, never across 2S." Probing USB 5 V with the red lead in the current jack is the same family of mistake.
4. The L298N will drop about 2 V and make a weak motor look like a software bug, and a 2S holder next to an unnamed charger is how a TP4056 gets clipped across 8.4 V. "ROS first" skips the timeout that should zero PWM. Any one of the three is enough to call the motor test unsafe. The blank sum means they also do not know what they think they bought.
5. Yes, for unpowered identification and for continuity on parts that are not connected to a supply, provided the meter beep is real. They are still forbidden to solder without a stand, to connect a motor supply, to charge lithium, and to treat the empty `ros_ws/` as a reason to skip the bench later.

</details>

## Further reading

The gate does not add a new theory reading. Open these again only for the line that is still open.

- [How to use a multimeter](https://learn.sparkfun.com/tutorials/how-to-use-a-multimeter) — if the beep test failed and you need the dial and the jacks explained again.
- [Logic levels](https://learn.sparkfun.com/tutorials/logic-levels) — if the power-up card's 5 V ban is the line you rewrote.
- [ROS 2 Jazzy install](https://docs.ros.org/en/jazzy/Installation.html) — only to confirm you are not installing it on the wrong operating system. An empty `ros_ws/` on Windows is the correct Chapter 00 result.

## Where to buy in Vietnam / Mua ở Việt Nam

Buy the gaps the audit wrote down, then stop. The master cart is [lesson 00-05]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %}). Tool pages below are Hshop snapshots from **23 September 2026**. Search URLs are searches.

| If the audit says this gap | Snapshot | Link |
| --- | ---: | --- |
| No meter, or the meter will not beep and you are replacing it | 285000 ₫ or 185000 ₫ | [UT33D+](https://hshop.vn/dong-ho-van-nang-dien-tu-digital-multimeter-uni-t-ut33d-chinh-hang), [Wadfow WDM1501](https://hshop.vn/dong-ho-van-nang-ky-thuat-so-vom-wadfow-wdm1501-digital-multimeter-true-rms) |
| No iron | 75000 ₫ | [60 W Wadfow](https://hshop.vn/mo-han-60w-wadfow-wel3616-soldering-iron) |
| No stand | 40000 ₫ | [stand](https://hshop.vn/de-gac-mo-han-tron-b-2-co-khay-roi) |
| No 0.8 mm solder | 24000 ₫ | [Sn63 wire](https://hshop.vn/thiec-han-sunchi-kp26-0-8mm-sn63-pb37-solder-wire) |
| No side cutters | 35000 ₫ | [170 cutters](https://hshop.vn/kim-cat-day-dien-nho-170-cat-chan-linh-kien-dien-tu) |
| No breadboard | 35000 ₫ | [830-point board](https://hshop.vn/test-board-cammb-102) |

One meter, not both. Jumpers and a data cable, if those are the open lines: [Shopee search, cáp USB data](https://shopee.vn/search?keyword=c%C3%A1p%20usb%20data) and [Lazada search, dây jumper](https://www.lazada.vn/catalog/?q=d%C3%A2y%20jumper). Eye protection if the card says it is missing: [Shopee search, kính bảo hộ](https://shopee.vn/search?keyword=k%C3%ADnh%20b%E1%BA%A3o%20h%E1%BB%99). [Thế Giới IC](https://www.thegioiic.com/) and [IC Đây Rồi](https://icdayroi.com/) are shop homepages, useful if you are standing at a counter with the gap list in your hand. Do not add a LiDAR, a Pi, or a scope to close Chapter 00.
