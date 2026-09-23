---
layout: post
title: "Welcome, outcomes, and how to study"
chapter: "00"
order: 1
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter00
lesson_type: required
draft: false
---

Set aside about ninety minutes. You need a text editor and a calendar. A robot is not required, and neither is Ubuntu. The work is writing a map you will still use when the chassis rolls.

## Learning objectives

By the end you can **state** the course spine, from component literacy through Chapter 07 teleoperation to a later reading of robot-learning papers. You can **compute** a load of 4–6 hours a week across 12–16 weeks and place the chapter checkpoints. You can **open** a lab journal with six fields: date, photo, wiring sketch, serial snippet, what broke, and what fixed it. You can **judge** a note as evidence, using a missing serial snippet or a missing failure as the test. You can **locate** the Vietnamese twin by chapter and order, and you can **postpone** LiDAR, Nav2, and a full ROS 2 install until a differential-drive robot already stops when commands go quiet.

## Prerequisites

You can read a technical page slowly and you can create a folder. You do not need a meter, an iron, or a prior robotics course. Ohm's law waits for Chapter 01, where it is measured. What you do need is a note that records the failure. "Started the course" will not help in week nine.

## Why it matters

Chapter 07 is Capstone A: two driven wheels and a caster, teleoperated with the wheels off the table. Teleoperation means you drive it yourself. If commands stop for about 300 ms, PWM duty goes to 0. ROS 2 Jazzy comes after that test. A topic is a named stream of messages, a messaging layer on physics you already trust. It does not create torque. Gazebo Harmonic and micro-ROS are the same idea in simulation and on the microcontroller. If you cannot say the 300 ms rule now, a later install is a way of avoiding the bench.

## The spine, said in the order you will live it

The course is one path, with optional rooms at the end.

You begin with component literacy: a breadboard row, a motor driver, a USB cable that only charges, a cell whose charger does not match the label. Chapter 00 is the bench habit. Chapter 01 turns voltage, current, and resistance into numbers you measured.

Firmware comes next, on an ESP32 or a Raspberry Pi Pico. Chapter 02 gets a program onto the chip. Chapter 03 makes it behave like robot code: pins, timing, and PWM. PWM, pulse-width modulation, is a pin that is high for a fraction of a short period. The motor driver turns that fraction into how hard a motor is asked to turn.

Chapters 04 through 06 add sensors, the driver, and the mechanics of two driven wheels. Chapter 07 is the acceptance test. You send forward, spin, or stop, over USB serial or, later, a small Wi-Fi page if you chose an ESP32. The wheels stay in the air. A timer remembers the last valid command. Let $t_{\mathrm{last}}$ be that timestamp and $t_{\mathrm{now}}$ the time in the control loop. Silence is

$$
t_{\mathrm{silence}} = t_{\mathrm{now}} - t_{\mathrm{last}}.
$$

The stop rule for this course is

$$
t_{\mathrm{silence}} > 300\,\mathrm{ms} \implies \text{PWM duty} = 0.
$$

The inequality is strict, so a command that lands exactly on 300 ms still counts as fresh. You will not flash this loop today. At a slow hobby speed of $0.3\,\mathrm{m/s}$ the robot can creep about 9 cm during that window:

$$
s \approx 0.3\,\mathrm{m/s} \times 0.3\,\mathrm{s} = 0.09\,\mathrm{m}.
$$

Nine centimetres will also yank a USB cable, which is why acceptance is wheels-up.

Only after that demo is repeatable do you add the messaging layer. Chapter 08 is communication and simple loops on hardware you have seen move. Chapter 09 installs ROS 2 Jazzy, and only on Ubuntu 24.04. A velocity topic is useful because you already know what the firmware does when messages stop. Chapter 10 names Gazebo Harmonic, the simulator paired with Jazzy, and micro-ROS, a way for the same microcontroller to speak ROS 2. micro-ROS is interesting after the board can move the chassis without it. A silent topic and a silent motor are otherwise the same symptom.

Chapters 11 and 12 are optional. They ask for a careful reading. LeRobot is a Hugging Face library of robot datasets and learned policies. ACT, action chunking with transformers, predicts a short chunk of future actions rather than a single twitch. A diffusion policy generates an action by iterative denoising. A vision-language-action model, a VLA, maps camera images and language onto robot actions. None of these replace a driver that can turn PWM off. Read the claim, the data, and the limit. A repository does not make the first chassis a research platform.

Videos treat several things as step one that this course postpones. You will not buy a LiDAR in this chapter, run Nav2, or install ROS 2 this week unless you are only reading the install page on a machine that already runs Ubuntu 24.04. The bench still comes first. A robot that rolled for a second is not autonomous. Motor-battery voltage does not belong on a 3.3 V pin.

## Cadence: four to six hours, for twelve to sixteen weeks

The design load is **4–6 hours per week** for about **12–16 weeks**. Fourteen weeks at five hours is

$$
5 \times 14 = 70
$$

hours. Twelve weeks at six hours is 72. Sixteen weeks at four hours is 64, enough for Chapters 00 through 10 if one sitting each week touches the bench, or the paper rituals before the parcel arrives. A five-hour week is about 90 minutes of reading, 120 minutes on the bench, and 90 minutes cleaning the note. One Sunday of twelve hours, then three quiet weeks, throws the wiring out of memory.

The chapter checkpoints are the spine with dates on it.

| Weeks | Chapters | You can show this evidence |
|------:|----------|----------------------------|
| 1–3 | 00 and 01 | A power-up card, a meter that beeps on a known short, and a journal entry with a voltage or an honest "none" |
| 4–6 | 02 and 03 | Firmware on an ESP32 or Pico, and a serial snippet pasted into the journal |
| 7–11 | 04 through 07 | Wheels-up teleop; PWM duty 0 if commands are silent for more than about 300 ms |
| 12–14 | 08 through 10 | A ROS 2 topic on Ubuntu 24.04 that describes motion you already trust; Gazebo Harmonic and micro-ROS named from a lab note, not from a thumbnail |
| Later, optional | 11 and 12 | A reading note on LeRobot, ACT, a diffusion policy, or a VLA that says what was claimed and what was not measured on your robot |

If a week collapses, slip a checkpoint. Do not skip the wheels-up test to catch up to Jazzy.

## The lab journal

Keep one running file, `notes/lab-notes.md`. Every entry has six fields, in this order. The **date** is the day you touched the work. The **photo** is a camera-roll name or an image of the bench; write `none` on purpose when there is nothing to shoot. The **wiring sketch** can be pencil on paper; before any circuit exists, write "no circuit yet" rather than leaving the field out. The **serial snippet** is pasted text from a serial monitor, a Thonny shell, or a later ROS 2 echo. Before any board is plugged in, the legal text is `none — no board yet`. **What broke** names a symptom you could see or measure, such as "the serial port disappeared when both motors were tied to the USB 5 V pin," not "motor bad." **What fixed it** names the change, including "nothing was powered; I wrote the stop rule before buying parts." An empty field makes the entry a mood.

The site is bilingual. The language switch matches **chapter** and **order**, not the title. This page is chapter `00`, order `1`, and so is its Vietnamese twin. If a paragraph is muddy, switch for that section. Keep GPIO, PWM, breadboard, Capstone, and ROS 2 stable in both languages.

## Figures

![Families of parts and tools the course will ask you to recognise]({{ site.imgurl }}/generated/kit_catalog_overview.png)

The drawing is a family portrait, not a cart. Lesson 00-05 is the bill of materials. Buying from the picture alone is how a LiDAR arrives before a meter.

![Two study tracks sharing one robot]({{ site.imgurl }}/generated/tracks_mcu_ros.png)

Track A finishes Capstone A from firmware, with no Ubuntu. Track B is that same robot plus Ubuntu 24.04, ROS 2 Jazzy, Gazebo Harmonic, and micro-ROS after the chassis moves. Both tracks share one acceptance test. LiDAR stays off the list until that test is reliable.

## Lab: the journal and the next fourteen weeks

Create a course folder and `notes/lab-notes.md`. Fill all six fields under today's date. In the sketch field, write the Capstone A sentence: two driven wheels, wheels up, serial or simple Wi-Fi, PWM duty 0 if silence exceeds 300 ms. In the serial field, write `none — no board yet` unless a port is already present. Do not invent a log line.

Place three calendar blocks in the next seven days that add up to 4–6 hours, named Read, Bench, and Notes. Until parts arrive, Bench may be "write the power-up card," which is the safety lesson after you choose a track. Copy the checkpoint table into the note and put a real week beside weeks 1–3, 4–6, 7–11, and 12–14. If travel deletes a week, slip the later checkpoint. Do not delete Chapter 07 to catch up. List three things you will not buy this month: a LiDAR, a computer bought only "for ROS," and a charger whose label you have not read. The cart, when you are ready, is [lesson 00-05]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %}).

**What you should see.** A stranger finds all six fields in a minute. The sentence contains 300. The calendar shows repeated sittings.

**When it goes wrong.** Blank fields get `none`. Split a single six-hour Sunday. A Nav2 bookmark is labelled "after Chapter 07." Loose lithium cells wait until lesson 00-05 matches a charger to a chemistry.

## Worked example

Hà starts on a Wednesday night with a Windows laptop and no parts. She computes two calendars before she picks one. A compressed plan of 6 hours a week for 12 weeks is $6 \times 12 = 72$ hours, but week 8 is a family trip, so Chapter 07 would land on a week she is not home. A 5-hour week for 14 weeks is 70 hours and still finishes Chapters 00–10 if she keeps the bench sitting. She writes the checkpoints as: weeks 1–3 Chapters 00–01, weeks 4–6 Chapters 02–03, weeks 7–11 Chapters 04–07, weeks 12–14 Chapters 08–10, Chapters 11–12 optional after the robot stops on silence.

She copies the 300 ms stop into the same note, without pretending to flash it. The serial field says `none — no board yet`. The photo field says `none`. What broke: nothing powered. What fixed it: she wrote the week numbers before opening a shop tab. Thursday 20:00–21:30 is Bench, labelled "safety card, still no soldering." That file is a pass. She has not flashed a board.

## Exercises

1. Write your Capstone A sentence. It must include two driven wheels, wheels up, serial or simple Wi-Fi, and PWM forced off when silence exceeds about 300 ms. Then write the week range in which that sentence becomes a demo you could film.
2. Compare two calendars. Plan P is 4 hours a week for 16 weeks. Plan Q is 6 hours a week for 12 weeks. Compute the total hours of each. Which one still has a honest place for Chapters 11 and 12 without stealing the week of the wheels-up test?
3. A journal entry has a date, a photo of a glowing LED, and the words "it worked." The serial snippet is missing and "what broke" is missing. Name the two facts a later debugging session cannot recover from this entry.
4. A friend wants to start week 2 with a LeRobot ACT training notebook. Which checkpoint does that skip, and what physical behaviour of your future robot will the notebook not have tested?
5. Commands are sent every $100\,\mathrm{ms}$. How many consecutive missed commands does it take until $t_{\mathrm{silence}} > 300\,\mathrm{ms}$? After exactly three missed periods, are the motors required to be off?

<details>
<summary>Suggested answers</summary>

1. One acceptable sentence: "Capstone A passes when my two-wheel differential-drive robot, wheels off the table, follows teleop from serial or a simple Wi-Fi page, and the firmware sets PWM duty to 0 if no new command arrives for more than 300 ms." That demo sits in weeks 7–11, with Chapter 07 as the gate.
2. Plan P is $4 \times 16 = 64$ hours. Plan Q is $6 \times 12 = 72$ hours. Plan P can hold Chapters 11 and 12 after Chapters 00–10. Plan Q has no spare week inside the 12, so the wheels-up test still owns weeks 7–11.
3. You cannot recover the text the board actually printed, and you cannot recover what failed before the LED glowed. A later "it broke again" has nothing to compare.
4. It skips firmware, the driver, and Chapter 07. The notebook does not test a 300 ms stop, and it does not test that motor voltage stayed off the 3.3 V pins.
5. Three missed periods are $300\,\mathrm{ms}$, which is not yet over the limit. The fourth makes $400\,\mathrm{ms}$, and PWM must be 0. After exactly three missed periods the motors may still run.

</details>

## Further reading

- [ROS 2 Jazzy documentation](https://docs.ros.org/en/jazzy/) — the later messaging layer. Read the introduction if you want a picture of topics. Do not start an install from this lesson.
- [LeRobot](https://github.com/huggingface/lerobot) — the library Chapters 11 and 12 will ask you to read carefully. Cloning it this week does not build the chassis.
- [Duckietown docs](https://docs.duckietown.com/) — a teaching robot with a published stack, useful as a picture of how a small wheeled robot is documented. It is not this course's bill of materials.
- [MIT manipulation course](https://manipulation.mit.edu/) — a rigorous look at manipulation and learned policies. Treat it as a destination for careful reading after your own robot can stop.
