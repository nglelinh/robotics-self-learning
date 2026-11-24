---
layout: post
title: "Nodes, topics, and messages"
chapter: "09"
order: 2
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter09
lesson_type: required
draft: false
---

Estimated time: **~75 minutes**.

Imagine an orchestra where the violinist never waits for the drummer to finish a bar before reading the sheet music, yet everyone stays tightly synchronized through a shared tempo. That is the ROS 2 computation graph: independent **nodes** publishing typed **messages** over named **topics**, decoupled in both time and code so you can swap a real LiDAR for a Gazebo simulator without changing a single line of your planner.

## Learning objectives

You will start a talker and a listener from the Jazzy demos, name the topic and the message type that connect them, and read a rate with `ros2 topic hz`. You will publish one `geometry_msgs/Twist` by hand and point at the two fields a differential-drive base actually uses. You will also say what an interface package is, so a later custom wheel message is a package and not a Python dict you hope the other node guesses.

## Prerequisites

Lesson 09-01: `printenv ROS_DISTRO` prints `jazzy` in the terminal you are about to use. Chapter 08’s kinematics: `linear.x` will mean $$v$$ and `angular.z` will mean $$\omega$$. No robot is required.


## Background Knowledge Map: Computation Graphs, Strongly Typed Messages, and Rate Contracts

ROS 2 topics formalize three architectural ideas that scale from a 2-node rover to a 200-node autonomous car:

- **Directed Computation Graph:** Nodes are independent OS processes (or composable threads); topics are named, many-to-many asynchronous buses. Because publishers and subscribers never hold direct pointers to each other, any node can be recorded (`ros2 bag`), replayed, or replaced live.
- **Strongly Typed IDL Interfaces:** Standard messages like `geometry_msgs/msg/Twist` or `sensor_msgs/msg/LaserScan` enforce exact field names, types, and SI units (metres, radians, seconds — REP-103), eliminating the ad-hoc CSV parsing bugs of custom scripts.
- **Rate & Latency Contracts:** Every topic carries an implicit timing contract: control commands (`cmd_vel` at 20–50 Hz), odometry (`odom` at 20–50 Hz), and scans (`scan` at 5–20 Hz). Knowing message size and publish rate lets you calculate network load before saturating Wi-Fi.
## Why this sits on the path

The Capstone bridge is a node. `cmd_vel` is a topic. `Twist` is a message. Until those three words are boring, Gazebo, Nav2, and a camera pipeline are just more nodes you cannot see. A learned policy that “publishes actions” is the same picture with a different message. If you cannot draw the talker–topic–listener graph, you cannot debug a silent robot.

![Talker, topic, listener]({{ site.imgurl }}/generated/ch09_ros_graph.png)

## Concepts

A **node** is one process (or one object inside a process) with a name in a graph. A **topic** is a named bus. A **publisher** writes messages of one type onto that bus. A **subscription** reads them. Publishers do not call subscribers by name. Many subscribers may listen, which is why a logger and a motor bridge can both hear `cmd_vel`.

The message type is part of the contract. `std_msgs/msg/String` and `geometry_msgs/msg/Twist` are different types. A subscriber of one will not connect to a publisher of the other, even if the topic string matches. Interfaces live in packages. `ros2 interface show geometry_msgs/msg/Twist` prints the fields. For this course the living fields are:

$$
v = \texttt{linear.x}, \qquad \omega = \texttt{angular.z}
$$

`linear.y` stays 0. A non-zero `linear.y` is a sideways request the base cannot perform (lesson 08-04).

Discovery is not instant magic across a hostile network, but on one laptop the demo nodes appear in a second. `ros2 node list`, `ros2 topic list`, `ros2 topic info /chatter`, and `ros2 topic echo /chatter` are the four commands you will use until they are muscle memory. `ros2 topic hz /chatter` is how you learn that “it is publishing” has a rate, the same way lesson 08-05 had a period.

## A rate is part of the contract

`ros2 topic hz /chatter` on the demo talker settles near 1 Hz. That number is not decoration. Lesson 08-05 already taught you that a motor loop which claims 50 Hz and delivers 12 Hz makes the derivative term lie. A topic has the same kind of honesty. When the Capstone bridge exists, you will subscribe to `/cmd_vel` and you will also ask `hz`. A teleop keyboard that publishes only when a key changes can sit at 0 Hz while you are not touching it. The firmware watchdog then stops the wheels, which is correct, and it surprises people who thought “the topic exists” meant “the command is fresh.”

Try this once the talker is running:

```bash
ros2 topic hz /chatter
ros2 topic bw /chatter
ros2 topic echo /chatter --field data
```

**Expected:** `average rate: 1.000` or very near it, a bandwidth of a few bytes per second, and the `--field` form printing only the string, without the YAML wrapper. `bw` on a `Twist` later will be small too. `bw` on a camera image will not. If you ever bridge images over a weak link, this command is how you notice before you blame the detector.

A second concrete message, which you already met as a one-shot publish, deserves a sustained rate. In a terminal:

```bash
ros2 topic pub -r 5 /cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 0.0}, angular: {z: 0.0}}"
```

In another:

```bash
ros2 topic hz /cmd_vel
```

**Expected:** about 5 Hz, and the robot still does not move, because nothing subscribes with a motor. Leave this running for ten seconds and then Ctrl-C. Write down the rate. Chapter 10’s bridge will treat “no message for 300 ms” as stop. At 5 Hz the gap between messages is 200 ms, inside that window. At 1 Hz the gap is 1000 ms and the watchdog will chop the command into pulses. That is a kinematics-and-timing bug you can now predict without the robot on the floor.

### Deep-Dive Explanation (Read Slowly): Hand-Calculating Topic Bandwidth for Telemetry vs. Sensors

Before streaming topics over Wi-Fi between an onboard SBC and a laptop, estimate their exact wire throughput:

1. **Command topic `/cmd_vel` (`geometry_msgs/msg/Twist`):** Contains 6 `float64` fields ($$6 \times 8 = 48\ \text{bytes}$$ payload, $$\approx 80\ \text{bytes}$$ with DDS headers). At $$50\ \text{Hz}$$:
   $$\text{BW}_{\text{cmd}} = 80 \times 50 = 4\,000\ \text{B/s} = 32\ \text{kbps}$$
   — virtually zero load on Wi-Fi.
2. **2D LiDAR `/scan` (`sensor_msgs/msg/LaserScan`):** Suppose 720 range floats + 720 intensity floats ($$1440 \times 4 = 5\,760\ \text{bytes}$$) at $$10\ \text{Hz}$$:
   $$\text{BW}_{\text{scan}} = 5\,760 \times 10 \approx 57.6\ \text{kB/s} \approx 0.46\ \text{Mbps}$$
   — still easy for Wi-Fi.
3. **Raw RGB camera `/image_raw` (640×480×3 bytes = 921,600 bytes/frame) at $$30\ \text{Hz}$$:**
   $$\text{BW}_{\text{raw}} = 921\,600 \times 30 = 27.65\ \text{MB/s} = 221\ \text{Mbps}!$$
   That single uncompressed camera topic will saturate typical 2.4 GHz Wi-Fi and starve `/cmd_vel`—proving why raw images should stay local on the robot or use `compressed` transport.

## Lab

Terminal A, after sourcing Jazzy:

```bash
ros2 run demo_nodes_cpp talker
```

**Expected**, repeating:

```text
[INFO] [talker]: Publishing: 'Hello World: 1'
[INFO] [talker]: Publishing: 'Hello World: 2'
```

Terminal B:

```bash
ros2 topic echo /chatter
```

**Expected:**

```text
data: 'Hello World: 3'
---
```

Terminal C:

```bash
ros2 node list
ros2 topic info /chatter
ros2 topic hz /chatter
```

**Expected shape:**

```text
/talker
/listener   # only if you also ran demo_nodes_cpp listener
Type: std_msgs/msg/String
average rate: 1.000
```

The talker publishes about 1 Hz. If `hz` says `no messages`, you echoed the wrong name or the talker’s terminal died.

Stop the talker with Ctrl-C. Publish a single Twist, which is the dry run of the bridge:

```bash
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 0.20, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.10}}"
ros2 topic echo --once /cmd_vel
```

Nothing moves. There is no subscriber with a motor. That silence is correct. Write in your notes: “0.20 m/s forward, 0.10 rad/s left, no bridge yet.”

**Failure modes**

| What you see | Likely cause |
| --- | --- |
| `Package 'demo_nodes_cpp' not found` | Desktop install missing, or this shell is not sourced |
| Echo never prints | Topic name typo, or QoS mismatch (next lessons). Demos match each other |
| `hz` is far from 1 | Another publisher on `/chatter`, or a overloaded VM |
| Twist pub errors on YAML | Quotes. Copy the command as one line. Colons and braces are YAML |
| You expected the ESP32 to twitch | It is not on this graph yet. Chapter 10 builds the subscriber |

## Where to buy this in Vietnam

No hardware. Optional later: the Pi 5 from lesson 09-01 if you want this graph off the laptop. Do not buy a “ROS robot kit” this week to see `/chatter`.

## Exercises

1. In one sentence, why can two terminals echo `/chatter` at the same time? Guidance: a topic is a bus, not a phone call.
2. Which field of `Twist` must stay near zero on the Capstone base, and why? Guidance: `linear.y`. The mechanism has no sideways speed.
3. `ros2 topic info /cmd_vel` after your `--once` pub shows no publisher. Is that a bug? Guidance: `--once` exits. The info is a snapshot of who is alive now.
4. Sketch the future graph: `teleop_twist_keyboard` → `/cmd_vel` → `capstone_bridge` → serial frame. Name the message on the topic. Guidance: `geometry_msgs/msg/Twist`.
5. What does `ros2 interface show` protect you from? Guidance: guessing field names. `angular.z` is yaw, not `angular.yaw`.

## Further reading

- [Understanding nodes](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Nodes/Understanding-ROS2-Nodes.html).
- [Understanding topics](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Topics/Understanding-ROS2-Topics.html).
- [`geometry_msgs/Twist`](https://docs.ros.org/en/jazzy/p/geometry_msgs/msg/Twist.html).
- Lesson 08-04 in this course for the inverse that turns this message into wheel speeds.
