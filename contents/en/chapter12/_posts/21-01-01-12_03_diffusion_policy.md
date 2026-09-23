---
layout: post
title: "Diffusion Policy intuition"
chapter: "12"
order: 3
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter12
lesson_type: required
draft: false
---

Estimated time: **~65 minutes**. You will read a project page, stare at one average, and write a paragraph. You will not denoise anything on a GPU.

## Learning objectives

You will explain why a diffusion policy generates an action trajectory by iterative denoising instead of emitting one regression. You will show, with two Capstone demonstrations around a chair, that the mean action drives into the chair. You will read the sketch $$x_{t-1} = f(x_t, \text{observation})$$ as a picture of a learned denoiser, not as the paper's update equation. You will contrast that picture with ACT in two paragraphs: one forward pass of a chunked CVAE, versus many steps that clean a trajectory.

## Prerequisites

Lessons 12-01 and 12-02 are done. You can say what a dataset key is, and you can say that an ACT chunk is open-loop for $$k/f$$ seconds. The chair in this lesson is furniture, not a new robot. No GPU, no conda environment, no checkpoint. The project page is public.

## Why this sits on the path

Nav2 picks one path and a controller tracks it. Diffusion Policy is a different proposal for where a path comes from when two drivers did not agree. In a corridor they pass a chair on two sides. The average of those drives aims at the chair. Jazzy will publish that average as a `Twist`, and the firmware will turn it into PWM. Nothing in Chapters 08 through 11 computes "this is the mean of two good ideas." You notice the mean in the data. The 0.2 s abort from ACT still applies when the burst was denoised rather than regressed.

## Concepts

A regression policy looks at the observation and emits the action, or a chunk of actions, in one shot. Training nudges that output toward the demonstrated numbers. When the demonstrations share one solution, this works. When they split, squared error is a compromise. The compromise is not one of the demonstrated solutions.

Chi, Feng, Du, Xu, Cousineau, Burchfiel, and Song frame the policy as conditional denoising. You start with a trajectory-shaped blob of noise. A network, conditioned on the observation, takes a small step toward a trajectory that could have come from the demonstrations. You repeat the step. The figure's four boxes are those repeats: noise, less noise, almost an action, a trajectory. Early steps have no business being sent to motors. Later steps are a time series of $$(v, \omega)$$, or of joint targets, in the units of whatever robot produced the log. The observation is an input at every step even though the drawing only shows the action getting cleaner. Cover the camera and the denoiser has no reason to prefer the left pass over the right pass.

The update you are allowed to memorize for this course is a sketch:

$$
x_{t-1} = f(x_t, \text{observation})
$$

Here $$x_t$$ is the noisy trajectory at step $$t$$, and $$t$$ counts denoising steps, not control ticks. The letter $$f$$ stands for a learned denoiser. The paper's real update predicts noise, mixes it with a schedule, and adds randomness so that two runs can choose two modes. If you implement the letter $$f$$ as "subtract a constant," you have not implemented Diffusion Policy. You have implemented the picture. That is the right depth for tonight.

The object being cleaned is a short trajectory, and the training distribution can put probability on both ways around the chair. You execute one sample, not the average of a left sample and a right sample. Denoising is expensive, so implementations execute a prefix and denoise again. Ten steps at 100 ms followed by eight actions at 50 Hz is a prefix of $$8/50 = 0.16$$ s, the same order as the ACT window. The watchdog still only notices silence.

ACT asks a transformer once for a chunk. A CVAE latent selects a demonstration style, and the chunk is a regression given that style. Latency is one network call per query, plus the open-loop prefix. Ensemble can still average a new "stop" with an old "go."

Diffusion Policy does not emit that chunk in one regression. It starts from noise and applies a learned denoiser until the trajectory matches a mode the demonstrations support. Different draws can fall left or right of the chair, instead of into a latent you set to zero. You pay with many network calls per replan. Either method can still drive into the chair if you execute the wrong sample, average two samples, or drop the timeout. Choosing between them this week is reading, not a training bake-off.

## The figure

![From noise to a trajectory]({{ site.imgurl }}/generated/ch12_diffusion.png)

Left to right: a red box of noise, a yellow box of less noise, a pale box that is almost an action, a green box that is a trajectory. The arrows are denoising steps, not time along the robot's path. Under the boxes the caption states the lesson's arithmetic in words: a mean of "left or right" is straight into the obstacle. The footer names Chi et al., Diffusion Policy, 2023, and tells you to read it rather than train it as tonight's lab. Believe the footer.

## Worked reading example

Two demonstrations, one decision point, Capstone units. The chair is 0.40 m ahead of the camera, centered. Both drivers keep a modest forward speed and disagree only in yaw.

| Demo | $$v$$ (m/s) | $$\omega$$ (rad/s) | Intent |
| --- | --- | --- | --- |
| L | 0.15 | $$+0.50$$ | pass on the left |
| R | 0.15 | $$-0.50$$ | pass on the right |
| Mean | 0.15 | $$0.00$$ | aimed at the chair |

The mean is not a cautious blend. Yaw cancels. Forward speed does not. Time to reach a chair 0.40 m ahead, if nobody yaws and the speed holds, is

$$
\frac{0.40}{0.15} \approx 2.7\,\text{s}
$$

You do not get 2.7 s of warning inside a 0.16 s open-loop prefix. The prefix that carries the mean action is already pointed at the obstacle. A denoiser that has seen both demonstrations, conditioned on an image that shows the chair, should move a noise draw toward demo L or toward demo R. It should not be asked to output both and then averaged by your bridge. If you are unsure which mode you sampled, the safe command is $$v = 0$$, not the mean.

Hold the sketch next to those numbers. At a late denoising step, $$x_t$$ might be a short sequence whose first action is near $$(0.15, 0.48)$$, a noisy left pass. Then $$f$$, given the image, pulls it toward $$(0.15, 0.50)$$. At an early step, $$x_t$$ is not yet a pass around anything, and sending it as `cmd_vel` is how you drive on pure noise. The index $$t$$ in the sketch is not the 50 Hz tick. Mixing those clocks is how a student executes step "noise" as if it were step "trajectory."

## Lab

Open the project page [diffusion-policy.cs.columbia.edu](https://diffusion-policy.cs.columbia.edu/) and the paper's abstract at [arXiv:2303.04137](https://arxiv.org/abs/2303.04137). You are looking for the claim that the policy models a distribution over action sequences, and for any figure that shows a trajectory emerging or a multimodal task. Do not follow a "train" or "download checkpoint" link beyond reading that it exists.

Then write one paragraph in `lab-notes.md` on multimodality, using the Capstone. The scene is two demonstrations of passing a chair on different sides. The paragraph has to include the mean action, and it has to say that the mean hits the chair. Use the numbers from the worked example, or change them and recompute the time-to-contact so the new numbers still hit. End the paragraph with an explicit statement that you did not train a model and did not load weights.

**Expected.** A paragraph a classmate can check without watching a video. It contains two sides, a cancelled yaw, a nonzero forward speed, the chair, and a refusal to train. A paragraph that says only "diffusion is better at multimodality" is not done, because it never mentions the mean.

**Failure modes**

| Mistake | Why the paragraph fails |
| --- | --- |
| You average the two demonstrations into one "neutral" episode and call the dataset cleaner | You deleted both successful passes and inserted the collision |
| You treat a missing GPU, or an out-of-memory error, as a failed lab | The lab is the paragraph. Closing a training process is the recovery, not a result |
| You write that diffusion is safer because it is iterative | Iteration produces a sample. The sample can say forward. Safety is still the timeout plus an explicit zero when the prefix is wrong |
| You send an early denoising step to the motors because it already has the shape of $$(v, \omega)$$ | Early steps are noise with that shape. Only a finished trajectory is even a candidate command, and only in the dataset's units |

## Exercises

1. Demo L is $$(v, \omega) = (0.20, +0.80)$$ and demo R is $$(0.20, -0.40)$$, both in m/s and rad/s. What is the mean action, and which way does it yaw? Guidance: mean $$v = 0.20$$, mean $$\omega = +0.20$$. The yaw does not cancel. The mean still need not be either demonstration. Say whether you would execute it toward a centered chair.
2. In the sketch, what does the subscript $$t$$ count? Guidance: denoising steps. It does not count 20 ms control periods. Write one sentence that keeps the two clocks apart.
3. You execute a prefix of 8 actions at 50 Hz after the trajectory is clean. How long is that prefix, and does the 300 ms watchdog expire during it if you keep publishing? Guidance: $$8/50 = 0.16$$ s. The watchdog does not expire, because publishing continues. Name the command you publish if the prefix points at the chair.
4. ACT commits with a latent and one forward pass. Diffusion Policy commits by drawing a trajectory out of noise. Give one cost of the second choice that the first choice does not pay on every replan. Guidance: many denoiser evaluations per replan, instead of one transformer pass. The cost is latency, not a license to skip the stop command.
5. Your paragraph claimed the mean hits the chair. Change the chair to sit 0.15 m ahead and keep $$v = 0.15$$ with $$\omega = 0$$. How soon is contact, and is that longer than a 0.16 s prefix? Guidance: $$0.15/0.15 = 1.0$$ s of travel if the speed holds. One second is longer than the prefix, which means the prefix alone does not finish the crash, and it also means the prefix has already committed you to the bad direction. The fix is a zero, not a shorter essay.

## Further reading

- [Diffusion Policy project page](https://diffusion-policy.cs.columbia.edu/). Read the abstract of the idea and the figures. Leave the training commands unread in the practical sense: you are not running them.
- [Chi et al., arXiv:2303.04137](https://arxiv.org/abs/2303.04137). The abstract is enough to confirm the authors and the claim. The noise schedule in the paper is the learned denoiser's real machinery, beyond the sketch $$f$$.
