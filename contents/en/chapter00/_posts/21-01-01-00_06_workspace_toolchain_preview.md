---
layout: post
title: "Workspace folders and a toolchain preview"
chapter: "00"
order: 6
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter00
lesson_type: required
draft: false
---

Plan about 70 minutes at the computer you will actually use for firmware. You need the track sentence from lesson 00-02. You do not need the robot, Ubuntu, or a successful compile. The point is a folder layout and an install log that tell the truth about what is installed today.

## Learning objectives

You will **create** a workspace with `notes/`, either `firmware/esp32/` or `firmware/pico/`, and an empty `ros_ws/` that says why it is empty. You will **choose** an ESP32 path (Arduino IDE 2.x or PlatformIO, board class `esp32dev`, serial 115200, a data USB cable) or a Pico 2 path (BOOTSEL, a MicroPython UF2, Thonny or `mpremote`). You will **record** versions you actually see, including the honest line "not installed." You will **explain** why ROS 2 Jazzy is an Ubuntu 24.04 install and why Windows Subsystem for Linux is not the robot lab yet. You will **name** Gazebo Harmonic without installing it, and you will **estimate** how small a serial byte is next to the 300 ms teleop timeout.

## Prerequisites

You can create directories and you can paste text into `notes/lab-notes.md`. Lessons 00-01 through 00-04 gave you the journal fields, the track, the power-up card, and the tool inventory. Lesson 00-05, the bill of materials, should already exist as `bom.csv` or as a dated note; if it does not, write `bom.csv missing` in the install log rather than inventing prices. You do not need to have soldered.

## Why it matters

The Chapter 07 timeout lives in firmware you can rebuild, on a board whose serial port you have already seen appear. A ROS 2 topic, later, is a messaging layer on that behaviour. If `ros_ws/` is a pile of half-installed packages on a Windows laptop, you will debug apt errors while the PWM pin is still untested. An empty workspace with a written reason is a better lab partner than a tutorial you cannot finish. Gazebo Harmonic can wait until there is a robot whose silence behaviour you trust enough to simulate.

## The folders, and what each one is allowed to contain

Put the course directory somewhere you will find it. The names below are the contract.

`notes/` holds `lab-notes.md` and, when lesson 00-05 is done, a copy or a pointer to `bom.csv`. Photos can live beside the markdown or in `notes/img/`. This folder is not for libraries you downloaded "in case."

`firmware/esp32/` or `firmware/pico/` holds the programs for the microcontroller you chose. Create the one that matches the track sentence. If you are still deciding, create the one you wrote down in lesson 00-02 and add a line `undecided — revisit before paying`. Do not create both and call that a plan, unless you already own both boards and you have named which one drives the motors.

`ros_ws/` is a ROS 2 workspace. Today it contains a `README` and nothing else. The README states the operating system of this computer and the sentence "Jazzy is not installed here" or "Jazzy is installed on this Ubuntu 24.04 machine, version string below." It does not contain a cloned Nav2 stack, a LiDAR driver, or a half-extracted Gazebo world.

A short tree for an ESP32 student on Windows looks like this.

```text
robot-course/
  notes/lab-notes.md
  notes/bom.csv
  firmware/esp32/README.md
  ros_ws/README.md
```

A Pico student uses `firmware/pico/` instead. The names are boring on purpose. Future lessons will tell you which file to open.

![What you are pointing a toolchain at: USB, regulator, 3.3 V pins, ground]({{ site.imgurl }}/generated/pcb_mcu_anatomy.png)

The anatomy drawing is the board as a set of jobs. USB brings power and a serial link. A regulator makes 3.3 V. GPIO pins speak logic. Ground is the common node from the safety lesson. The toolchain's only job today is to talk to that USB link, or to admit that the board is not here.

![An ESP32 module on a small dev board, the Wi-Fi-capable brain]({{ site.imgurl }}/wikimedia/ESP32_on_Lolin32_Lite_clone_board_cropped.jpg)

![A Raspberry Pi Pico, the USB-first MicroPython board]({{ site.imgurl }}/wikimedia/Raspberry_Pi_Pico.jpg)

The photographs are the two legal brains, not a third option you have to buy. An ESP32-class board is the one that can do Wi-Fi teleop later. A Pico-class board, including a Pico 2 if that is what lesson 00-05 sold you, is the one that starts as a USB device running MicroPython. Match the photo to your sentence. Do not match it to whichever listing is on sale tonight.

## The ESP32 path, previewed and not finished

Two tools are legal. **Arduino IDE 2.x** is the one with a GUI, a board manager, and a serial monitor. **PlatformIO** is the one that lives in an editor such as VS Code and pins versions in a file. Pick one for the install log. You may switch later. You may not write "both, whichever" and leave the log blank.

When the board support is installed, the board entry you want for a common DevKit is in the **`esp32dev`** class: in Arduino IDE that is often labelled "ESP32 Dev Module"; in PlatformIO the board id is `esp32dev`. The exact menu label moves between package versions. The id is the thing to write down. The serial monitor baud for this course's first sketches is **115200**. A charge-only USB cable will power a lamp on the board and will never show a port. The proof of a data cable is a new serial device when you plug in, and its disappearance when you unplug.

You are not required to compile blink today. If the IDE is installed, record the version string from the About dialog or from `pio --version`. If it is not installed, write `Arduino IDE not installed` or `PlatformIO not installed` and the reason. "I am on a lab PC I do not control" is a reason. "I got bored" is also a reason, and it should be visible so next week is honest.

A single byte on an 8N1 serial link is about 10 bit times. At 115200 bit/s,

$$
t_{\mathrm{byte}} \approx \frac{10}{115200}\,\mathrm{s} \approx 87\,\mu\mathrm{s}.
$$

A short command of four characters is under half a millisecond. The Chapter 07 timeout is about 300 ms, hundreds of times longer. Serial baud is not the dead-man switch. Dropped commands are. Knowing that now stops you from "fixing" a timeout by changing the baud later.

## The Pico path, previewed and not finished

Hold the **BOOTSEL** button, plug the board into a data USB cable, and release the button. A drive appears, the way a USB stick would. You copy a **MicroPython UF2** onto that drive. The board reboots into the MicroPython interpreter. **Thonny** is the simple editor that can find the board. **`mpremote`** is the command-line tool that can do the same job from a terminal. Pick one and write it in the log.

If no drive appears, the cable is the first suspect, then the button, then the port. If the board has not arrived, write the steps as a plan and do not download random UF2 files "to be ready" without noting the date and the official Raspberry Pi source. A UF2 from a forum thread is how people flash the wrong chip.

The Pico path does not use `esp32dev` and does not use 115200 as a requirement of MicroPython's REPL, though a later UART you wire yourself might. Do not mix the two install logs. A student who chose the Pico still leaves `ros_ws/` empty for the same reason the ESP32 student does.

## ROS 2 Jazzy and Gazebo Harmonic, named only

**ROS 2 Jazzy** is the distribution this course uses, and the supported desktop install is **Ubuntu 24.04**. If this computer is Windows, do not pretend that Windows Subsystem for Linux is the robot lab. WSL can be a place to read documentation. It is not where you will plug the motor driver's ground and watch a wheel. Write the install as **later**, on an Ubuntu 24.04 machine: your own, if you have one, or a lab PC, as in the track lesson. The install page is [docs.ros.org/en/jazzy/Installation.html](https://docs.ros.org/en/jazzy/Installation.html). Following it today is allowed only when the operating system is actually Ubuntu 24.04, and only as a parallel sitting that does not replace the firmware folder.

**Gazebo Harmonic** is the simulator that pairs with that stack. Its name goes in the README. Its packages do not get installed today. A world file you cannot connect to a robot you have not built is a second project.

micro-ROS, when it comes, is firmware on the same ESP32 or Pico-class board plus an agent on the Ubuntu machine. It belongs after `firmware/` already contains a program that can zero PWM. The empty `ros_ws/` is how you remember that order.

## Lab: folders, README, install log

Create the tree in the previous section. In `firmware/esp32/README.md` or `firmware/pico/README.md`, write three lines: the track (A, or B-after-A), the chosen MCU in words, and the tool you will use (Arduino IDE 2.x, PlatformIO, Thonny, or mpremote). If the tool is not installed, say so in the same file.

Create `ros_ws/README.md` with the operating system name and the sentence that Jazzy and Gazebo Harmonic are not installed today, or the version string if you are on Ubuntu 24.04 and you did install Jazzy. Do not paste a tutorial's `apt` transcript you did not run.

Add an **install log** section to today's journal entry. Each line is a tool, a version or `not installed`, and a date. Example lines, which you must edit to match your machine:

```text
2026-09-23  OS: Windows 11
2026-09-23  Arduino IDE: not installed — will use lab time on Thursday
2026-09-23  PlatformIO: not installed
2026-09-23  serial plan: 115200, board id esp32dev, cable not yet proved
2026-09-23  ROS 2 Jazzy: not installed — Ubuntu 24.04 lab PC later
2026-09-23  Gazebo Harmonic: named only
```

A Pico log names BOOTSEL and the UF2 instead of `esp32dev`. Paste the log into the serial-snippet field if you have no board, so the field is not empty. If a port did appear, paste the port name above the log.

**What you should see.** The three directories exist. The firmware README names a track and an MCU. The ROS README does not claim Ubuntu you do not have. The install log has dates and the words `not installed` where that is true.

**When it goes wrong.** You created `ros_ws/src` full of clones because a video started that way. Delete the clones until the README is the only file; you can re-clone when Chapter 09 says so. You wrote "WSL Ubuntu" as if it were the robot lab. Correct the README: WSL is not the bench. You set the baud to 9600 because an old Arduino sketch did. The course serial monitor for ESP32 sketches is 115200. You copied a UF2 from a random link. Replace the plan with the official Raspberry Pi MicroPython documentation and do not flash it until you can say which chip the file is for.

## Worked example

Trang is on Windows, Track A, ESP32, ceiling already decided in lesson 00-02. She creates `firmware/esp32/` and `ros_ws/`. She does not install the IDE in this sitting because the lab PC at school already has Arduino IDE 2.3 and she would rather learn one install. Her log says `Arduino IDE: not on this laptop; school lab PC, confirm version Thursday`. The firmware README says "Track A, ESP32, Wi-Fi teleop later, tool is Arduino IDE 2.x, board class esp32dev, serial 115200." She computes the byte time, about 87 µs, and writes "300 ms timeout is about 3000 byte-times; baud is not the safety layer." Her `ros_ws/README.md` says "This laptop is Windows 11. Jazzy waits for the Ubuntu 24.04 lab PC. Gazebo Harmonic is not installed. WSL will not be used as the robot lab."

A classmate on Ubuntu 24.04 may install Jazzy in another hour and paste a real version string. That classmate still owes the same firmware folder. Trang does not copy a version she did not run.

## Exercises

1. Your track sentence says Pico 2 and MicroPython. Which directory do you create, what does BOOTSEL have to do before any file is copied, and which two tools are legal for the REPL?
2. The board LED lights from a USB cable, and no serial port appears. Which object do you suspect, and what evidence would change your mind?
3. You are on Windows and a blog says to install Jazzy inside WSL tonight. What do you write in `ros_ws/README.md`, and which operating system is actually required?
4. At 115200 bit/s, 8N1, estimate the time for one byte and for a 4-byte command. Is that time a meaningful fraction of 300 ms?
5. Your install log says "PlatformIO latest" with no version and no date. What would you add so the line is evidence?

<details>
<summary>Suggested answers</summary>

1. Create `firmware/pico/`. Hold BOOTSEL while plugging in a data cable so a drive appears, then copy the MicroPython UF2. Thonny or `mpremote` may talk to the board afterwards.
2. Suspect a charge-only cable. A data cable is proved when a serial port or a BOOTSEL drive appears and disappears with the plug. A glowing LED only proves power.
3. Write that Jazzy is not installed, that WSL is not the robot lab, and that the install waits for Ubuntu 24.04. Jazzy's supported desktop path for this course is Ubuntu 24.04.
4. One byte is about $10/115200 \approx 87\,\mu\mathrm{s}$. Four bytes are about $0.35\,\mathrm{ms}$. That is roughly a thousandth of 300 ms. The timeout is about missing commands, not about baud.
5. Add the date, the output of `pio --version` or the IDE About string, and `not installed` if you have not run it. "Latest" is not a version.

</details>

## Further reading

- [PlatformIO docs](https://docs.platformio.org/) — the editor-based ESP32 path, including the `esp32dev` board id.
- [Arduino docs](https://docs.arduino.cc/) — Arduino IDE 2.x and the serial monitor.
- [ESP-IDF for ESP32](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/) — Espressif's own framework. You are not required to use it for Capstone A. It is the reference when a board-support package disagrees with a blog.
- [Raspberry Pi Pico MicroPython](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html) — BOOTSEL and the official UF2, which is the only flash plan this lesson trusts.
- [ROS 2 Jazzy tutorials](https://docs.ros.org/en/jazzy/Tutorials.html) — skim the list so you can see it assumes an install. That install is Ubuntu 24.04, later.
- [Gazebo Harmonic](https://gazebosim.org/docs/harmonic/) — the simulator's name and docs. Do not install it from this lesson.
