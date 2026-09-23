---
layout: post
title: "Services and actions"
chapter: "09"
order: 3
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter09
lesson_type: required
draft: false
---

Estimated time: **~75 minutes**.

## Learning objectives

You will call an add-two-ints service and read a single response, then send a Fibonacci action goal and point at feedback versus the final result. You will choose among topic, service, and action for four robot jobs: streaming wheel speed, zeroing encoders, driving to a pose, and publishing a laser scan. Nav2’s `NavigateToPose` should feel like the Fibonacci demo with a map attached, not like a new religion.

## Prerequisites

Lesson 09-02’s talker is comfortable. You can leave a process running in one terminal and type in another. No robot.

## Why this sits on the path

Streaming `cmd_vel` on a topic is the right tool because a newer command should replace an older one and nobody should wait for a reply before the next 50 ms tick. “Are you at the goal?” is a bad topic if you also need cancel and progress. That is an action, and it is how Nav2 will take a pose in Chapter 11. A service is the short question: set a bool, trigger a calibration, return a sum. People who put a five-minute drive on a service discover that Ctrl-C is their only cancel. The Capstone watchdog stays a firmware timeout either way; an action cancel should also publish a zero Twist, or the wheels keep the last command.

![Service reply versus an action timeline]({{ site.imgurl }}/generated/ch09_svc_action.png)

## Concepts

A **service** is a request and a response. The client sends one message, the server sends one message, the call returns. `example_interfaces/srv/AddTwoInts` takes `a` and `b` and returns `sum`. Use it when the work is short and the caller can wait. Do not use it for a stream. A service server that blocks inside a motor loop will miss the deadline from lesson 08-05.

An **action** is a goal, a stream of feedback, and one result, plus cancel. The Fibonacci tutorial sends an `order` and feeds back the sequence as it grows. You can cancel a goal that is taking too long. Nav2’s navigate action has the same shape: goal pose in, feedback (distance remaining, current pose) along the way, result (success or abort) at the end. Recoveries live inside the behavior tree, which Chapter 11 only peeks at. You do not need that tree to see why an action exists.

A practical split for this robot:

| Job | Use | Why |
| --- | --- | --- |
| Wheel command at 10–50 Hz | Topic `cmd_vel` | Latest message wins. No reply required |
| Laser scan | Topic | Stream. Often best-effort QoS |
| “Zero the encoder counters” | Service | One question, one answer, milliseconds |
| “Drive to this pose” | Action | Minutes, cancel, feedback |
| Battery voltage | Topic | Stream, slow is fine |

Cancelling an action does not by itself cut MOSFET gates. Your bridge must treat “no recent Twist” as stop. That rule already exists in the serial timeout. Keep it when the Twist starts coming from an action server’s controller instead of your keyboard.

## Cancel is a message, not a wish

The Fibonacci server keeps computing until the goal finishes or a cancel arrives. Watch the server terminal while you send `order: 20`. The feedback sequence grows. Ctrl-C on the *client* cancels that goal in the CLI; the server process should still be alive and `ros2 action list` should still show `/fibonacci`. If the only way you know to stop a goal is to kill the server, you do not have cancel, you have a crash.

```bash
ros2 action send_goal /fibonacci action_tutorials_interfaces/action/Fibonacci "{order: 20}"
```

Interrupt it. Then immediately:

```bash
ros2 action list
ros2 node list
```

**Expected:** `/fibonacci` remains, and the server node remains. A second short goal, `order: 5`, should still return a result. That is the behavior you want from Nav2 later: one failed or cancelled navigate does not require you to restart the whole stack. It is also the behavior you do *not* get from a service. There is no `ros2 service cancel`. The client waits, or you kill it, and the server may still be inside the call.

Put the motor consequence in the same note. Cancelling `NavigateToPose` stops the action server from sending new feedback. It does not, by itself, force the last `Twist` to zero unless the controller or your bridge does that. The 300 ms firmware timeout from Chapter 08 is the backstop. An action-aware bridge publishes zeros on cancel *and* on silence. Writing only one of those is how a robot creeps after you pressed stop in RViz.

## Lab

Service, two terminals. Tutorial: [Understanding services](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Services/Understanding-ROS2-Services.html).

```bash
ros2 run demo_nodes_cpp add_two_ints_server
```

```bash
ros2 service list
ros2 service type /add_two_ints
ros2 service call /add_two_ints example_interfaces/srv/AddTwoInts "{a: 2, b: 3}"
```

**Expected:**

```text
example_interfaces/srv/AddTwoInts
requester: making request: example_interfaces.srv.AddTwoInts_Request(a=2, b=3)
response:
example_interfaces.srv.AddTwoInts_Response(sum=5)
```

If the server terminal is not running, the call waits. That wait is the reason a lost motor service feels like a hung teleop. Ctrl-C the client.

Action, two terminals. Tutorial: [Understanding actions](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Actions/Understanding-ROS2-Actions.html).

```bash
ros2 run action_tutorials_py fibonacci_action_server
```

```bash
ros2 action list
ros2 action info /fibonacci
ros2 action send_goal /fibonacci action_tutorials_interfaces/action/Fibonacci "{order: 5}"
```

**Expected:** feedback lines with a growing `sequence`, then a result whose last numbers are the fifth Fibonacci step (the sequence includes the partial sums the server defines; read the result block rather than memorising a blog’s list). `ros2 action send_goal` also prints a goal id. Send order 20 and cancel is the point: in another terminal, `ros2 action list` still shows `/fibonacci`, and you can interrupt the client. The server terminal should not have to be killed to stop one goal.

**Failure modes**

| What you see | Likely cause |
| --- | --- |
| Service call sits forever | Server not running, or wrong service name |
| `package 'action_tutorials_py' not found` | Desktop metapackage incomplete. `sudo apt install ros-jazzy-action-tutorials-py` |
| Feedback never arrives, result does | You used a client that hides feedback. The CLI `send_goal` shows it |
| You mapped “drive 2 m” to a service | Cancel and progress have nowhere to live. Make it an action, and still timeout the motors |

## Where to buy this in Vietnam

Nothing. This is a laptop lab.

## Exercises

1. Classify “publish battery voltage ten times a second.” Guidance: topic.
2. Classify “Nav2, go to the kitchen.” Guidance: action. Name you will look up later: `NavigateToPose`.
3. Your service call hangs for 30 seconds. What is the first process you check? Guidance: the server, with `ros2 service list` and the server terminal, before you reinstall ROS.
4. Why must an action cancel still produce a zero Twist on the Capstone? Guidance: the firmware holds the last wheel command until the 300 ms watchdog. Cancel has to be followed by silence or an explicit zero, or the robot coasts on the old PWM until the watchdog saves you.
5. Fibonacci `order: 5` is a stand-in. What is the “order” field analogous to on a mobile base? Guidance: the goal pose, not the PWM.

## Further reading

- [Understanding services](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Services/Understanding-ROS2-Services.html).
- [Understanding actions](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Actions/Understanding-ROS2-Actions.html).
- [Nav2 getting started (Jazzy)](https://docs.nav2.org/jazzy/getting_started/) for the navigate action you are not running yet.
- The interface definition `action_tutorials_interfaces/action/Fibonacci` via `ros2 interface show`.
