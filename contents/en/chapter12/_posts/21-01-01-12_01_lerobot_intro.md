---
layout: post
title: "LeRobot / Hugging Face robotics intro"
chapter: "12"
order: 1
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter12
lesson_type: required
draft: false
---

Estimated time: **~70 minutes**. About 25 minutes on the docs and the repository, 30 minutes on a dataset card, 15 minutes on the exercises.

## Learning objectives

You will name the three things the LeRobot project keeps on one contract: a dataset, a policy, and a robot. You will point at the SO-100 family, Koch v1.1, and LeKiwi as that project's own low-cost arms and mobile bases, and you will say why none of them is the Capstone diff-drive. You will write a one-page dataset card for a fake episode whose keys are a camera, forward speed $$v$$, and yaw rate $$\omega$$, with units that match at record time and at play time. You will copy the repository's one-sentence description from the README into `lab-notes.md`, with the date you read it.

## Prerequisites

You can open a browser and a terminal. The Capstone already takes a forward speed in metres per second and a yaw rate in radians per second, and Chapter 08 still zeros the motors if no fresh frame arrives for 300 ms. Chapter 09's `geometry_msgs/Twist` is the same pair: `linear.x` and `angular.z`. You do not need a graphics card, a leader arm, or a second robot. If `pip` is painful on your network, skip it. The graded artifacts are a quotation and a card.

## Why this sits on the path

Capstone A made a diff-drive base that moves when firmware accepts $$v$$ and $$\omega$$. ROS 2 Jazzy gave those two numbers a topic. A learning library does not replace that stack. It adds a file. The file has to contain the observation the robot can actually produce later, and the action the firmware will actually accept later. If one note says the action is motor PWM and another says it is radians, you have logged one robot and played the log on another. Lessons 12-02 and 12-03 assume the keys exist and then argue about how a policy fills them. Lesson 12-04 is the same mistake at the scale of a published checkpoint. Lesson 12-05 asks you to pick a month; the month is optional, this contract is not.

## Concepts

[LeRobot](https://huggingface.co/docs/lerobot/index) is a Python library, a dataset format, and hardware configs maintained with Hugging Face. The index describes four verbs: teleoperate, record, train, deploy. A person drives, the log stores synchronized video plus the actions they sent, a policy imitates those actions, and deploy writes actions back to the robot. This course stops before train. The verbs are how you read the docs, not a homework script.

A **dataset** lines up an image, a state, and an action on one clock. The project calls the file a LeRobotDataset. An arm log uses `observation.images.<camera>`, joint positions, and joint targets. A diff-drive log uses a camera and a two-vector action. The format stores either. It will not warn you that you mixed them.

A **policy** reads an observation and writes an action. ACT is the policy the next lesson reads. Weights expect a length and a meaning per entry. The right length in the wrong units is the wrong robot.

A **robot** here is a body plus a config: motors, cameras, and the keys they fill. On the docs, SO-101 is the flagship low-cost arm and SO-100 is the earlier arm in that family. Koch v1.1 is a community arm they still document. LeKiwi is a mobile base with an arm. Those are the project's embodiments. The Capstone is two driven wheels, no gripper, action $$(v,\omega)$$, and your timeout. SO-101 joint targets do not publish `cmd_vel`. LeKiwi's action includes the arm, so "mobile" does not merge the keys.

Record time is a person driving while the logger writes. Play time is the policy writing while firmware applies the command. Same names, same units, both times. A camera 15 cm lower, or a flipped yaw sign, keeps the column `w` and changes the motion. `fps: 10` means actions are 0.1 s apart. A 30 Hz camera dumped in without alignment pairs an image with the wrong command. The 300 ms timeout stays while you record. Commenting it out logs a robot you are not allowed to run. A late link that fills the log with $$(0, 0)$$ is the other bug: mark those frames, do not delete the watchdog.

## The figure

![Dataset, policy, and robot share keys]({{ site.imgurl }}/generated/ch12_lerobot.png)

Three boxes, two arrows. The dataset box holds observation and action. The arrow through the policy is play time: a row goes in, an action comes out, the robot executes it. The blue arrow labeled record runs the other way: the human drives the robot and the logger stores the same keys. The red line under the boxes is the rule you are enforcing with the card. The gray line says to read that card before a training run. Tonight the run does not start. The card does.

## Worked reading example

This card describes a fake Capstone episode. It is not a file from the Hub, and it is not a format exporter you have to install. Two seconds, ten frames per second, twenty rows. The card sits at the top of the folder so a later script is not allowed to guess.

```text
robot_name: capstone_diff
fps: 10
episode_length_s: 2.0
observation.images.cam: RGB video, 480x640, 10 Hz, same clock as action
observation.state: [v_meas_m_s, w_meas_rad_s]
action: [v_cmd_m_s, w_cmd_rad_s]
```

Row 0 is action $$(0.20, 0.00)$$: 0.20 m/s forward, no yaw, about 2 cm in one 0.1 s period if the wheels are down. Row 8, a chair on the left of the image, is $$(0.10, -0.40)$$: slower, and $$-0.40$$ rad/s. With $$z$$ up, negative yaw is a right turn. Row 19 is $$(0.00, 0.00)$$, a driver stop, not a timeout.

The same twenty rows become a different robot if the units drift. Suppose the teleop script still writes Chapter 07's PWM-style commands in $$[-100, 100]$$, and the note you hand to a policy says the vector is m/s and rad/s. A later loader trusts the note. It reads 70 from the log and treats it as 70 m/s. No layer in a network checks that. The card is finished only when that contradiction is impossible: one `names` line, one unit, and both the logger and the playback bridge import that line.

The row count is an arithmetic check, not a slogan:

$$
N = \text{fps} \times T = 10 \times 2.0 = 20
$$

Twenty images with `fps: 30` on the card are not a 2.0 s episode. Somebody will stretch the turn. Write the count you can verify by listing the folder.

## Lab

Software only. The base can stay on the shelf. `lab-notes.md` gets two artifacts: a dated quotation, and a dataset card.

**Docs map.** Open the [LeRobot docs index](https://huggingface.co/docs/lerobot/index). Copy the four verbs in order: teleoperate, record, train, deploy. Under them write: this course stops before train. Then list the headings you actually open for install, datasets, imitation learning, and robots. Date the note. If a heading was renamed, write the new name. Do not invent one to match this lesson.

**One sentence from the repository.** Open [huggingface/lerobot](https://github.com/huggingface/lerobot). Under the repository name there is a one-line description. Copy that sentence into `lab-notes.md` in quotation marks, with the date. Do not paraphrase it. If the line has changed since these notes were written, today's line is the correct quotation.

**Dataset card.** Rewrite the worked example so it is clearly yours. Change one number and keep the arithmetic consistent. A fair edit is `fps: 5` and `episode_length_s: 3.0`, which is 15 rows. Keep the keys `observation.images.cam`, $$v$$ in m/s, and $$\omega$$ in rad/s. Add one row of numbers and one sentence that says those numbers are the same pair as `linear.x` and `angular.z` on the Capstone bridge.

Installing the library is optional. The only command this lesson accepts, if you want a terminal line in the notes, is a version listing:

```bash
pip index versions lerobot
```

**Expected from the command.** A short list headed by the package name, or an error about the network, permissions, or an old `pip`. Both are acceptable. A version list is not a trained policy. If the command works, stop. Do not continue into a train entrypoint because the install happened to succeed.

**Expected from the writing.** Every mention of `action` on your card is m/s and rad/s, including the row you invented. The README line is in quotation marks. The docs snapshot has a date. There is no loss curve and no checkpoint path in the notes.

**Failure modes**

| What you produced | What it actually means |
| --- | --- |
| Logger comment says PWM, policy note says radians | Play time applies the policy to a different robot than record time |
| `fps` times seconds does not equal the image count | The turn is stretched. A gentle avoidance becomes a snap, or the reverse |
| Teleop recorded with the 300 ms timeout removed | The log is of a base that keeps the last command when the link dies. Your real firmware will not do that, and you drove without the safety property |
| Timeout still compiled in, link stalls, log full of sudden zeros | The policy will copy the stops. Fix the link or mark the frames |
| A train command, because the docs list train as step three | Close it. The assignment is the card and the quotation |

## Optional hardware, not this week

This lesson buys nothing. An SO-100-class arm is an imported kit. With servos and shipping it is often many millions of VND in Vietnam. Recheck a listing the week you shop. These notes do not link a shop for an arm. The course does not require one. The card describes the Capstone you already have.

## Exercises

1. On your card, which two numbers are the action, and what is the unit of each? Guidance: $$v$$ in m/s and $$\omega$$ in rad/s, the same pair as `Twist`. If a column still says PWM, the card is not done.
2. An SO-101 action is joint targets. Your bridge publishes two scalars. Why is "take the first two joints and call them $$v$$ and $$\omega$$" not an adapter? Guidance: those entries are joint units on another body. Truncating the arm does not create a diff-drive.
3. You set fps to 5 and the episode to 3.0 s. How many rows? A classmate has 15 images and writes `fps: 10`. How long does that card claim if the camera really ran at 5 Hz? Guidance: $$5 \times 3.0 = 15$$ rows. Their card claims $$15/10 = 1.5$$ s, so a 3.0 s folder is labeled at half its real duration and the yaw looks twice as fast.
4. The serial link drops for 0.5 s while recording. Timeout is 300 ms and still in the firmware. What does the log show, and what would it show if the timeout had been removed? Guidance: zeros after about 300 ms with the timeout; the last nonzero command held for the whole gap without it. Only the first log matches playback.
5. Paste the README sentence you quoted, then add one clause of your own. Guidance: the quotation is the line on the repository today, not a paraphrase. Your clause should say you are not training this week.

## Further reading

- [LeRobot documentation](https://huggingface.co/docs/lerobot/index). Use the index, then the sidebar you actually see. The train step is described there and is not this assignment.
- [huggingface/lerobot on GitHub](https://github.com/huggingface/lerobot). The one-line description under the title is part of the lab.
