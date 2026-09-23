---
layout: post
title: "Imitation learning and ACT overview"
chapter: "12"
order: 2
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter12
lesson_type: required
draft: false
---

Estimated time: **~70 minutes**. Most of that is a slow read of one abstract and a numerical note about 0.2 s of open-loop motion. None of it is a training run.

## Learning objectives

You will define behavior cloning as a map from observation to action, fitted on demonstrations rather than on a reward. You will state what ACT (Zhao et al., RSS 2023) actually outputs: a chunk of $$k$$ future actions from a transformer, trained as a conditional variational autoencoder so more than one style of demonstration can exist. You will compute the open-loop window for $$k = 10$$ at 50 Hz, connect that window to the Chapter 08 watchdog, and explain temporal ensemble as an average of overlapping chunks without re-deriving the paper.

## Prerequisites

Lesson 12-01's dataset card is in your notes: camera, $$v$$ in m/s, $$\omega$$ in rad/s, one fps. You know the firmware zeros the motors 300 ms after the last good frame. You can read an abstract. You do not need a GPU, the ALOHA hardware, or a working install of the policy. If a classmate's machine reports that it ran out of memory, that classmate started the wrong assignment.

## Why this sits on the path

Up through Nav2's tour, the command on `cmd_vel` was one `Twist` per tick, produced by a controller you could name. A learned policy changes the shape of that command. ACT does not emit "the next 20 ms." It emits a short list of future actions and then lets the robot execute them while the network is not being asked again. That list is a burst of open-loop motion. The Capstone bridge can forward the burst. It cannot make the burst safe. The 300 ms timeout still matters, and it is not enough on its own: a timeout fires when frames stop arriving, and a live policy keeps frames arriving for the rest of a bad chunk. This lesson is how you read that burst before anyone suggests you train it.

## Concepts

Behavior cloning fits a map from observation to the action a person sent. There is no reward in the definition. The map is only as good as the log: units, clock, and the timeout from lesson 12-01. Cloning $$(v, \omega)$$ onto a robot that accepts $$(v, \omega)$$ is aimed at the Capstone. Cloning an SO-101 joint vector onto that same base is still the wrong body.

A squared-error head fails when demonstrations disagree. One person passes a cup on the left, another on the right, and the average points at the cup. Zhao, Kumar, Levine, and Finn train ACT as a conditional variational autoencoder so a latent can pick a style. A transformer decoder then predicts actions consistent with that style, the images, and the joint state. At playback the encoder is gone and the latent is taken from the prior, often at the prior's center. The latent is permission to commit to one way of doing the task. It is not a collision check.

The transformer outputs a **chunk** of $$k$$ future actions. That is the "action chunking" in the paper. At 50 Hz the control period is 20 ms. A network that needs 80 ms has already missed four deadlines if it must answer every period. A chunk of ten actions covers that gap, so the base executes a list while the next list is computed. The list is open-loop until you replan. ALOHA, the paper's hardware, is a low-cost bimanual leader-follower rig for collecting those demonstrations. You are not building it. You are asking what a chunk does to a diff-drive that already has a watchdog.

Temporal ensemble averages overlapping chunks at playback. Newer predictions get more weight. The paper's decay constant can wait. The average hides small jitter. It does not stop the robot: the mean of "forward" and "stop" is "creep." The stop is a zero you publish on purpose, or a timeout because publishing ceased.

Chapter 08 clears the motors when no valid frame arrives for 300 ms. That covers a dead process or a fallen cable. It does not cover a live process posting the rest of a chunk that still says forward after a person steps in. Those frames look fresh. The abort belongs where the chunk is unpacked: drop the remaining steps and publish $$(0, 0)$$. Asking the network only when the chunk ends makes the whole chunk the open-loop window. Asking more often retires a bad prediction sooner, and you still need an explicit zero when the scene has changed.

## The figure

![ACT turns images and joint state into a chunk]({{ site.imgurl }}/generated/ch12_act.png)

The left box is images and joint state. On the Capstone that is the camera plus measured $$(v, \omega)$$, not a six-joint vector. The middle box is the chunk. The right box says execute, then replan. The red line is the part a summary skips: the chunk is open-loop and still needs a timeout and a stop. The footer cites Zhao et al., ACT / ALOHA, 2023. That is a citation, not a parts list.

## Worked reading example

Use a teaching chunk, not the hyperparameter table from the paper. Take $$k = 10$$ and a control rate of 50 Hz:

$$
T_{\text{open}} = \frac{k}{f} = \frac{10}{50} = 0.2\,\text{s}
$$

Two tenths of a second is the open-loop burst if you execute the whole chunk before you look again. Steps are 0.02 s. The early steps command $$v = 0.25$$ m/s and $$\omega = 0$$. By step 9, at 0.18 s, $$v$$ has tapered to 0.05 m/s. Nothing in the list yaws.

At $$t = 0.08$$ s a person steps in front of the camera. Six steps remain, 0.12 s of leftover command. A rough distance, using 0.20 m/s as a stand-in, is

$$
0.20 \times 0.12 = 0.024\,\text{m}
$$

about 2.4 cm of commanded travel, before the wheels' own stopping distance. The watchdog does not fire at 0.08 s: the bridge is still delivering fresh steps. Publish zeros for the rest of the window. Waiting out 300 ms is the slower option.

Chunks discussed for ALOHA-style ACT are often nearer a hundred steps at 50 Hz:

$$
\frac{100}{50} = 2.0\,\text{s}
$$

of open loop if you do not replan early. Two seconds of committed forward motion does not belong on the Capstone in a hallway. Knowing the paper uses chunking is not the same as accepting the paper's chunk length on your base.

Temporal ensemble on one overlapping instant: an older chunk still says $$v = 0.25$$ at $$t = 0.20$$, and a newer chunk, queried after the person appeared, says $$v = 0.00$$. A plain average is $$0.125$$ m/s. That is not a stop. Even a weighted average that leans toward the new chunk, say three quarters of the new value and one quarter of the old, is $$0.0625$$ m/s, still forward. Ensemble reduces the command. It does not replace the zero.

## Lab

Reading only. Do not clone a training configuration, do not download weights, and do not start a job because a GPU happens to be free in a lab you do not have.

Open the paper's abstract page: [Zhao et al., arXiv:2304.13705](https://arxiv.org/abs/2304.13705). From the abstract and the title, write four lines in `lab-notes.md`:

1. The authors and the venue line you can see (RSS 2023 is the venue these notes use; keep whatever the abstract page shows if you want a direct quotation).
2. What the method predicts: a chunk of future actions, not a single next command. The phrase "action chunking" should appear because you found it, not because you copied this sentence blindly. If you paraphrase, say so.
3. What the hardware in the title is for: low-cost bimanual demonstration hardware (ALOHA), which you are not buying and not assembling.
4. Your chunk-length implication for the Capstone, with the arithmetic visible: $$k = 10$$, 50 Hz, $$T_{\text{open}} = 0.2$$ s, and one sentence that names who cuts a bad chunk. The watchdog cuts it when the publisher dies. A live publisher of a bad chunk has to be cut by an explicit zero.

**Expected.** A note of about half a page. The number 0.2 s appears, with the division that produced it. The stop command is named separately from the timeout. There is no training log.

**Failure modes**

| What happened | What you should do |
| --- | --- |
| You launched a train script and the process died with an out-of-memory error | Close it. That error is not the assignment, and it is not evidence you "almost" trained ACT. A laptop without a serious GPU was never going to finish this paper's training |
| The note says "the watchdog handles the chunk" and stops there | Rewrite the sentence. A watchdog handles silence. A chunk that keeps streaming is not silence |
| You copied a chunk length from a random config file and skipped the division | The lab is the implication in seconds, on your control rate. A unitless $$k$$ does not tell you how far the base can travel |
| The note treats ALOHA as the next purchase | ALOHA is the paper's data-collection rig. Your robot for this course remains the Capstone |

## Exercises

1. Write behavior cloning as one sentence that uses your keys. Guidance: the map takes the camera and returns the commanded $$v$$ and $$\omega$$ the demonstrator sent. Reward is not in the sentence.
2. Two demonstrations pass a cup on opposite sides and a squared-error head averages them. What does the CVAE latent buy? Guidance: a commitment to one side. It does not buy a range sensor.
3. Recompute the open-loop time for $$k = 100$$ at 50 Hz. Would you execute that whole chunk on the Capstone in a corridor? Guidance: $$100/50 = 2.0$$ s, and the corridor answer is no.
4. An older chunk predicts $$v = 0.25$$ and a newer chunk predicts $$v = 0$$ at the same instant. You send the mean. Are the wheels stopped? Guidance: no. The mean is $$0.125$$ m/s. Publish zero if a person is in the camera.
5. The bridge emits a fresh serial frame every 20 ms for a chunk that still says forward, after you have seen an obstacle. Does the 300 ms timer expire? Guidance: no. Publish zeros or stop the publisher.

## Further reading

- [Zhao et al., Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware](https://arxiv.org/abs/2304.13705). Read the abstract and the method figures. Training instructions in the paper's repository are outside this lab.
- [LeRobot docs](https://huggingface.co/docs/lerobot/index). ACT is named there as a policy you can read about. Naming it is the whole use of that page tonight.
