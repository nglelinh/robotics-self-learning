---
layout: post
title: "Curated next paths and full references"
chapter: "12"
order: 5
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter12
lesson_type: required
draft: false
---

Estimated time: **~60 minutes**. Ten minutes on the figure, twenty on picking a path, thirty on a one-month plan you can reread without buying anything tonight.

## Learning objectives

You will choose one path for the next month, not three. Path A stays on the field base: Nav2, a lidar when you are ready, and linorobot2 as a reference diff-drive stack while your own bridge remains the motor path. Path B is an arm and a LeRobot dataset, only if you later decide to buy hardware. Path C is theory: Modern Robotics, which is free, and the MIT manipulation course. You will write a plan that names the Capstone you already have and one safety habit you will not drop. You will leave the reference list as a map, not as five papers to finish over a weekend.

## Prerequisites

Chapters 08 through 11 are behind you in the course sequence, even if some labs are still rough. You can say what the 300 ms timeout does, what `cmd_vel` carries, and why a policy from another gripper is not a controller for your wheels. You have the dataset-card habit from lesson 12-01. You do not need a new board, a new sensor, or a clean build of Nav2 to write the plan. The plan comes first so the shopping tab does not write it for you.

## Why this sits on the path

The course ran from a diff-drive you can hold to papers that publish actions for robots you do not have. The honest ending is one thread for a month. A weekend that opens RT-2, Diffusion Policy, a Nav2 tutorial, a gripper listing, and a Jetson listing finishes none of them. One path for a month beats five papers in a weekend. Timeouts, units, notes, and a power switch still apply on every path.

## Concepts

Three paths. You will write one of them into the lab. You still need to recognize the other two, so a forum post does not drag you sideways in week one.

**Path A, field base.** You already have the robot. Chapter 11 toured a map, a planner, and a controller on Jazzy and did not finish them. The matching tutorial is the [Nav2 getting started guide for Jazzy](https://docs.nav2.org/jazzy/getting_started/). Those pages expect a `LaserScan` from a small 360° lidar, not a single-point ranger. Budget 1.5–3.5 million VND and recheck when you are ready. Buying this week is not required to choose the path. [linorobot2](https://github.com/linorobot/linorobot2) is a reference for how a bringup, a URDF, and a Nav2 config sit together. You do not flash it over your firmware. Your bridge, your serial frame, and the 300 ms timeout stay. Two writers on the motors is a bug. One writer, yours, keeps the timeout in the process that writes PWM.

**Path B, arm and data.** LeRobot is the software entry if you later want joint-space demonstrations. SO-100-class arms, Koch, and LeKiwi are that project's bodies. A dataset card comes before a payment: keys, units, fps, and the timeout still in firmware. An arm, a lidar, and a second computer do not arrive together. A leader-follower kit is often many millions of VND. These notes do not invent a shop URL. If you cannot name the action vector, you are not ready to shop.

**Path C, theory.** [Modern Robotics](https://hades.mech.northwestern.edu/index.php/Modern_Robotics) (Lynch and Park) is free on that site. A month is one chapter tied to the base, not the book. Copy the wheeled-mobile title you see on the page, the chapter that speaks $$v$$ and $$\omega$$. The [MIT manipulation course](https://manipulation.csail.mit.edu/) explains why VLA papers care about grippers you do not own. Read the notes. Buying a 6-DOF arm to follow the videos spends Path B's money for Path C's reason.

The failure mode is a 6-DOF arm, a lidar, and a Jetson-class board in the same week. None of those removes the timeout on the Capstone, the only robot whose cutoff you have tested. The purchase that can wait, waits.

Safety habits that are not optional on any path:

- The 300 ms command timeout stays in the firmware you flash.
- The first motion test of any new publisher is wheels-up, or the chassis on a stand, until the command is the command you think it is.
- A hardware E-stop or a power switch you can hit without a keyboard stays in reach. A policy, a planner, and a typed "stop" can all fail with the node still alive.

Units stay on the path too. Path A speaks `Twist`. Path B will speak joint targets the day an arm exists, and those targets do not overwrite $$v$$ and $$\omega$$ in the same column. Path C's derivatives are only useful if you still know which number is radians per second on the wire.

## The figure

![Three paths for the next month]({{ site.imgurl }}/generated/ch12_paths.png)

Three boxes, one month, one choice. The green box is the field base: Nav2, a lidar, linorobot2 as a reference. The yellow box is arm and data: LeRobot and an SO-100-class arm, later. The blue box is theory: Modern Robotics and the MIT course. Under them: timeouts, units, notes, and a power switch still apply on every path. The bold line is the pace. You may read the title of a paper on a path you did not choose. You may not make that paper the second project.

## Worked reading example

A plan that can be checked, unlike "path A and a bit of B, be careful, buy a lidar and an arm":

```text
path: A
robot I already have: Capstone diff-drive, the one with the serial bridge
safety habit I will not drop: 300 ms with no fresh frame sets v = 0 and w = 0
also still true: wheels-up before any new publisher; power switch in reach
this month I will not buy: an arm, a Jetson-class board
first page I will open: https://docs.nav2.org/jazzy/getting_started/
lidar: not this week. If the base still tracks cmd_vel in a month, recheck a small 360 unit in the 1.5–3.5 million VND band
reference I will read and not flash over my firmware: https://github.com/linorobot/linorobot2
```

That plan names one path, the Capstone, and a 300 ms habit. linorobot2 is a reading reference, not a new motor driver. A small 360° lidar is about 1.5–3.5 million VND. A Pi 5, if the laptop is outgrown, starts near 2.4 million VND for a low-RAM board at [Hshop](https://hshop.vn/may-tinh-raspberry-pi-5-made-in-uk). Recheck the variant. An arm is the expensive optional path and is not priced here. Lidar or Pi, not both on day one, and not beside an arm.

## Lab

Write the plan into `lab-notes.md` as a block you can follow for four weeks. Required lines:

```text
path: A or B or C
robot I already have: Capstone diff-drive
safety habit I will not drop: <one of: 300 ms timeout, wheels-up first motion, hardware E-stop>
this month I will not buy:
first link I will actually open:
what I will have in my notes after week one:
```

Week-one evidence depends on the letter. Path A: which Nav2 page you opened, and which part of linorobot2 you refused to copy onto the motor driver. Path B: a dataset card for an arm you do not own, joint units marked unknown until a servo datasheet, and $$v$$, $$\omega$$ kept on their own keys. Path C: a chapter or lecture title copied from the site, plus one relation you can tie to the base, or the question you will ask next week. Do not invent a title.

**Expected.** Exactly one path letter. The robot line says Capstone, not "a mobile robot." The safety line has a concrete habit, and the 300 ms timeout is either that habit or is still listed as remaining in force. The "will not buy" line includes at least the two items that are not on your path. There is no cart screenshot.

**Failure modes**

| Plan | Problem |
| --- | --- |
| Path "A+B+C, lightly" | That is the five-papers weekend in disguise. Pick one letter |
| First action is an arm, a lidar, and a Jetson in one order | You bought three paths. The lab asked for a month on one |
| Path C, and the timeout is "not relevant because I am only reading" | Reading does not delete the firmware on the robot in the corner. The habit stays in force the next time you flash |
| linorobot2 flashed as the motor driver on day two | You replaced a timeout you understand with a stack you have not read. Read it. Keep your bridge |
| Week-one note is "watch some videos" | Name the page and the paragraph you will be able to summarize |

## Exercises

Each answer names a path. A sentence that could apply to all three paths is not done.

1. Path A. Name one thing you will copy from a reading of linorobot2, and one thing you will not replace. Guidance: a fair copy is the shape of a bringup launch or the way a URDF names `base_link`. The thing you will not replace is your serial bridge and the 300 ms cutoff in the firmware that writes PWM. "I will use their stack" is the wrong answer.
2. Path B. Write the action keys you would insist on seeing before you pay for an SO-100-class arm. Guidance: joint names, units from the servo datasheet (radians or encoder counts, not a shrug), fps, and a camera key. Add a line that $$v$$ and $$\omega$$ of the Capstone are absent from those joint columns. If you cannot write the keys, the path is a later month.
3. Path C. From the Modern Robotics site, copy the wheeled-mobile title you will open, and name the Capstone quantity it should explain. Guidance: $$v$$ and $$\omega$$, or wheel rates into that pair. A chapter on grasps is the wrong click. The MIT course may replace the book if you quote its lecture title and still name $$v$$ and $$\omega$$.
4. Path A budget. You have not earned a lidar until `cmd_vel` matches the bridge, wheels-down, with the timeout proven. What VND band will you recheck, and what if the listing is above it? Guidance: 1.5–3.5 million VND for a small 360° unit. Above the band, you wait. You do not add an arm to "complete the set."
5. Write the week-four check for the path you chose, as a yes/no question your notes can answer. Guidance: Path A asks whether you can point at the Nav2 page that consumes your `cmd_vel` and at the firmware line that still times out at 300 ms. Path B asks whether the card uses one unit system and whether you bought nothing. Path C asks whether you can restate the wheeled relation and whether the timeout is still in the last firmware you flashed.

## Curated references

The links the course actually uses, gathered so a later month does not depend on a search. Open the one that matches your path. Skim titles of the rest.

**The stack you already started**

- [ROS 2 Jazzy documentation](https://docs.ros.org/en/jazzy/)
- [Nav2 getting started, Jazzy](https://docs.nav2.org/jazzy/getting_started/)
- [Installing Gazebo with ROS, Harmonic](https://gazebosim.org/docs/harmonic/ros_installation). Jazzy's paired simulator in that guide is Gazebo Harmonic.
- [slam_toolbox](https://github.com/SteveMacenski/slam_toolbox)
- [linorobot2](https://github.com/linorobot/linorobot2), a reference diff-drive stack. Keep your own bridge.

**Learning libraries and papers, for reading**

- [LeRobot docs](https://huggingface.co/docs/lerobot/index) and [huggingface/lerobot](https://github.com/huggingface/lerobot)
- [Zhao et al., ACT, arXiv:2304.13705](https://arxiv.org/abs/2304.13705)
- [Chi et al., Diffusion Policy, arXiv:2303.04137](https://arxiv.org/abs/2303.04137) and the [project page](https://diffusion-policy.cs.columbia.edu/)
- [RT-1](https://robotics-transformer1.github.io/) and [arXiv:2212.06817](https://arxiv.org/abs/2212.06817)
- [RT-2, arXiv:2307.15818](https://arxiv.org/abs/2307.15818)
- [Open X-Embodiment](https://robotics-transformer-x.github.io/)
- [OpenVLA, arXiv:2406.09246](https://arxiv.org/abs/2406.09246) and [openvla.github.io](https://openvla.github.io/)
- [pi0](https://www.physicalintelligence.company/blog/pi0)

**Theory, free to read**

- [Modern Robotics](https://hades.mech.northwestern.edu/index.php/Modern_Robotics)
- [MIT manipulation](https://manipulation.csail.mit.edu/)

**A computer, only when Path A outgrows the laptop**

- [Raspberry Pi 5 at Hshop](https://hshop.vn/may-tinh-raspberry-pi-5-made-in-uk). Low-RAM boards have been listed from about 2.4 million VND. Recheck the variant.
