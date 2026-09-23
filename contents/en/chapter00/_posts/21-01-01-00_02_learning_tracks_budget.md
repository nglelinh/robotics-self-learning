---
layout: post
title: "Two tracks: a budget MCU robot and ROS 2 later"
chapter: "00"
order: 2
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter00
lesson_type: required
draft: false
---

Plan about an hour. You need the Capstone sentence from the welcome lesson and an honest description of the computer you actually own. Prices in this lesson are shapes of a budget, not a cart. The cart is [lesson 00-05]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %}).

## Learning objectives

You leave this lesson able to **choose** Track A or Track B in a sentence that names your laptop's operating system, a money ceiling in VND, and a two-month goal. You can **specify** a Track A robot as an ESP32 or a Pico 2, TT gear motors, a TB6612FNG rather than an L298N, and an HC-SR04, with no Ubuntu required for Capstone A. You can **compute** the voltage a Darlington driver throws away, about 2 V, and say what that does to a 7.4 V pack. You can **place** Ubuntu 24.04, ROS 2 Jazzy, Gazebo Harmonic, and micro-ROS after the same robot already moves, with a Raspberry Pi only as a later option. You can **refuse** a LiDAR purchase before Capstone A acceptance, in writing.

## Prerequisites

Lesson 00-01: you can state the wheels-up teleop test and the 300 ms PWM stop, and you have a journal with the six fields. You do not need Ubuntu, ROS, or a paid order. If you already own a Raspberry Pi, or a laptop that dual-boots Linux, you still start from the same chassis. Ownership is not a reason to skip the firmware robot.

## Why it matters

Capstone A does not link against ROS. It needs a microcontroller that can time about 300 ms and a driver that can take PWM and then let go. If the first month is spent partitioning a disk, the motor wires are still untested. Track B is real. It is the path to Jazzy topics, Gazebo Harmonic, and micro-ROS. Those topics are a messaging layer on physics you already trust. Choosing the track now is how you stop a shopping tab from choosing it for you, and how you stop a LiDAR from arriving before the timeout exists.

## Two legal paths, one moving robot

**Track A** is the budget microcontroller path, and it is enough for Capstone A. The brain is either an ESP32 development board or a Raspberry Pi Pico 2. The ESP32 is the board you pick when you want Wi-Fi teleop later: a phone or laptop on the same desk sends commands without a USB cable in the final demo. The Pico 2 is the board you pick when you want MicroPython and a USB cable first. Both speak 3.3 V logic. Both can run the 300 ms stop. Neither requires Ubuntu.

The mechanics are TT gear motors on a small chassis, two driven wheels and a caster. The driver you want is a **TB6612FNG** module, a MOSFET H-bridge. The module people buy because a video used it is often an **L298N**, a Darlington bridge. At motor current the Darlington pair drops on the order of 2 V between the battery and the motor. The MOSFET bridge drops a few tenths of a volt. For a two-cell pack sitting near 7.4 V,

$$
V_{\mathrm{L298}} \approx 7.4\,\mathrm{V} - 2.0\,\mathrm{V} = 5.4\,\mathrm{V},
$$

$$
V_{\mathrm{TB6612}} \approx 7.4\,\mathrm{V} - 0.3\,\mathrm{V} = 7.1\,\mathrm{V}.
$$

A TT motor is already a small, lossy gearbox. Starving it of another 2 V is why "the same battery" feels weak on an L298N and ordinary on a TB6612. Pololu's TB6612 carrier, [product 713](https://www.pololu.com/product/713), is the clearest public explanation of that chip if you want a second schematic style. You are allowed to buy a different module that uses the same chip. You are not required to import that exact carrier. A DRV8833 is a smaller MOSFET substitute when the TB6612 is out of stock. It is still not an L298N.

The range sensor on the first cart is an HC-SR04 ultrasonic module. Its echo pin swings to 5 V, so it must not land directly on a 3.3 V GPIO. Lesson 00-05 includes a level shifter for that wire. Track A does not install Ubuntu. Serial teleop from Windows, macOS, or whatever Linux you already have is enough for acceptance.

**Track B** is Track A plus a later software stack. The robot is the same chassis, the same driver, the same timeout. When teleop is reliable, you use a machine running **Ubuntu 24.04** and install **ROS 2 Jazzy** there. **Gazebo Harmonic** is the simulator that belongs with that release, and it is Chapter 10 work. **micro-ROS** lets the microcontroller speak ROS 2 to that machine. It is a transport added on top of PWM you have already watched work. A Raspberry Pi can appear later as an optional companion computer. It is not the device that first spins the motors, and it is not a reason to buy a LiDAR so the Pi "has something to do."

People who install micro-ROS on a board that has never turned a wheel debug two failures at once. A topic with no messages and a motor with no voltage look identical from the chair. The course therefore puts the message graph after the bench.

![Track A on the left, Track B as a later layer on the same robot]({{ site.imgurl }}/generated/tracks_mcu_ros.png)

Read the left side of the figure as this month's robot and the right side as software you earn. "No Ubuntu required" is the Track A permission for Capstone A. "Buy LiDAR only after Capstone A is reliable" is the shared spending rule. A spinning LiDAR is a different power problem, a different ROS tutorial, and often a few million đồng. It does not make the 300 ms timeout more correct.

## The decision table

Use this as a worksheet. Copy one row into the journal and strike the others, or mark a single row "mine."

| Your situation this month | Track | Do now | Leave for later |
| --- | --- | --- | --- |
| Any laptop OS; about 1.5–2.0 million VND; goal is "it drives when I type" | A | ESP32 or Pico 2, TT motors, TB6612FNG, HC-SR04, shifter, tools, battery plan from lesson 00-05 | Ubuntu, Pi, LiDAR, Nav2, Jazzy install |
| Windows or macOS, and you want ROS eventually | A now, B after Chapter 07 | The same robot; write "Ubuntu 24.04 lab PC later" | Do not wipe the laptop; do not buy LiDAR to justify a future Pi |
| You already run Ubuntu 24.04 and you want ROS literacy | B, but build the Track A robot first | Same electronics; you may install Jazzy on that PC in parallel | Do not block Chapter 07 on a Gazebo world; do not skip the bench |
| The budget is mostly a Pi plus a LiDAR kit from a video | Stop and recompute | Rewrite the goal as wheels-up teleop | That kit does not implement a 300 ms stop or a MOSFET drop |

A LiDAR at 4,000,000 ₫ next to a Track A core near 800,000 ₫ is

$$
\frac{4{,}000{,}000}{800{,}000} = 5
$$

times the core, and it does not flash the first LED. The ratio is the reason for the ban before acceptance.

Price hygiene belongs in the same note. A number without a date is gossip. Lesson 00-05 holds the dated Hshop snapshots for the parts you will actually order. This lesson does not rebuild that table. If a board moves by a hundred thousand đồng, your track does not change. The track changes only when the operating system, the ceiling, or the goal changes.

## Lab: write the track sentence

Open `notes/lab-notes.md`. Under today's date, write three lines: the laptop operating system, the money ceiling in VND for the next 30 days, and a one-sentence goal. If the goal mentions maps, SLAM, or Nav2, add the clause "after Capstone A."

Pick the microcontroller in words. Either "ESP32 dev board, Wi-Fi teleop later, USB serial first" or "Pico 2, MicroPython, USB first." You may change this before you pay. You may not leave it blank.

Write this sentence and put your name after it: "I will not buy a LiDAR before my Capstone A wheels-up teleop passes, including the 300 ms PWM stop."

Add one line that points at lesson 00-05 as the only shopping list. Do not paste a second cart here. If you already know you will use a shared lab PC for Ubuntu, name that machine as "lab Ubuntu, not my laptop."

**What you should see.** A later reader can tell which track you chose, which MCU you lean toward, and which expensive objects you refused. Ubuntu is either "not now," "lab PC later," or "already installed, bench still first."

**When it goes wrong.** You chose Track B and ordered only a Pi. The motors are still driven by the ESP32 or the Pico 2; add those rows by opening lesson 00-05, not by inventing a new kit. You chose Track A and then started a Jazzy install "just to try" on Windows. Bookmark the install page under "after Chapter 07" and close it. Windows Subsystem for Linux is not the robot lab. Your budget is a single undated number. Split "robot core" from "tools" and date the estimate.

## Worked example

Minh has a Windows laptop and a ceiling of about 1.5–2.0 million VND for the month. The goal he first wrote was "learn ROS and SLAM." He rewrites it to "drive a two-wheel robot from serial, with a 300 ms stop, and only then use a lab Ubuntu PC for Jazzy." The table puts him on Track A now. He chooses an ESP32 because he wants Wi-Fi teleop as a later Chapter 07 variant, while the first commands will still be USB serial. He does not buy a Pico 2 as well. He does not buy a LiDAR. He writes that Track B will happen on a university lab machine that already has Ubuntu 24.04, not by repartitioning the Windows disk this week. The shopping list he will copy is lesson 00-05, not a forum kit.

A second student, Lan, already runs Ubuntu 24.04 on her own laptop. She is allowed to follow the [Jazzy installation page](https://docs.ros.org/en/jazzy/Installation.html) in parallel, in a separate sitting, and to record the version string in her journal. She is not allowed to skip the bench. Her robot is still TT motors, a TB6612FNG, an HC-SR04, and firmware that zeros PWM when packets stop. If Jazzy installs cleanly and the motors are still in a bag, she is not ahead. She has a messaging layer and no physics. Gazebo Harmonic stays named and unopened until the chassis has passed wheels-up teleop at least once. micro-ROS stays a link, [micro.ros.org](https://micro.ros.org/), until the same board has moved the wheels without it.

Minh sketches the Darlington loss so the driver choice is not a brand preference. At 7.4 V with about 2 V dropped, the motor sees 5.4 V. A MOSFET drop of about 0.3 V leaves 7.1 V. He writes "TB6612FNG, not L298N" in the track sentence. Both students end the entry with the LiDAR refusal. Neither opens a second spreadsheet. Lesson 00-05 is the cart.

## Exercises

1. Your laptop is Windows, your ceiling is 1,800,000 ₫, and you want the robot to move this month. Which track, which MCU if you care about Wi-Fi later, and which driver? What do you do with Ubuntu this week?
2. You already have Ubuntu 24.04. Why is the first build still the Track A chassis if you are allowed to install Jazzy in parallel?
3. A 6 V battery of four AA cells feeds an L298N that drops about 2 V. What voltage reaches the motor? Why is that a poor match for a TT motor whose useful range starts near 3 V but is already weak at 4 V?
4. A listing adds a 3,500,000 ₫ LiDAR to a Track A plan "for only a bit more." Does Capstone A acceptance get easier? Where does the LiDAR sit relative to the acceptance test?
5. Where does micro-ROS sit relative to the first day the wheels respond to a serial command? What would a [linorobot2](https://github.com/linorobot/linorobot2) repository tempt you to skip?

<details>
<summary>Suggested answers</summary>

1. Track A now. Choose an ESP32 if Wi-Fi teleop is the later goal; choose a Pico 2 if you want MicroPython over USB first and accept Wi-Fi as someone else's problem for now. The driver is a TB6612FNG. Ubuntu waits. Do not install Jazzy on Windows and call it the lab.
2. Jazzy can show topics on a PC. It cannot show that your VM wiring, the stall behaviour, and the 300 ms timeout work on the hardware you will later describe with those topics. Parallel install is allowed. Skipping the bench is not.
3. $6 - 2 = 4$ V at the motor. Four volts is the weak end of a small TT gearbox, before load. The robot crawls or stalls, and the symptom looks like "bad motors."
4. Acceptance does not get easier. The LiDAR does not implement the timeout or the MOSFET driver. It belongs after Capstone A, if it belongs at all.
5. micro-ROS comes after the wheels already respond. linorobot2 is a picture of a differential-drive robot described for ROS 2. Opening it before you have a driver and a timeout tempts you to debug a URDF while the bench is still empty.

</details>

## Further reading

- [linorobot2](https://github.com/linorobot/linorobot2) — one concrete differential-drive stack for ROS 2. Read it as a picture of Track B's destination, not as this month's parts list.
- [micro-ROS](https://micro.ros.org/) — what it is. Bring the tutorials back after the chassis moves without it.
- [Install ROS 2 Jazzy](https://docs.ros.org/en/jazzy/Installation.html) — Ubuntu 24.04 is the supported path. If your daily machine is Windows, this page is a later lab-PC task.
- [Pololu TB6612FNG carrier, product 713](https://www.pololu.com/product/713) — why a MOSFET carrier is the driver to compare against a Darlington module.

Shopping stays in [lesson 00-05]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %}). Do not rebuild the cart from these four links.
