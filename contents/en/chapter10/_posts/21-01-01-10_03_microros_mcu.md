---
layout: post
title: "micro-ROS on MCU (ESP32/Pico)"
chapter: "10"
order: 3
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter10
lesson_type: required
draft: false
---

Estimated time: **~75 minutes**.

Traditional embedded robots need a custom serial protocol on the MCU plus a hand-written Python bridge node on the host PC to translate bytes into ROS 2 topics. **micro-ROS** collapses that boundary: by running a lightweight XRCE-DDS client right on your ESP32 or RP2040, the microcontroller itself becomes a first-class ROS 2 node publishing `/odom` and subscribing to `/cmd_vel`.

## Learning objectives

You will describe XRCE-DDS as a client on the microcontroller plus an agent on the PC that is the actual DDS participant in the ROS 2 graph. You will predict, before you run anything, that `ros2 topic list` stays empty of MCU topics when the agent is down and still empty when the agent is up but no client has connected. You will start the Jazzy micro-ROS agent container for UDP and write the matching serial form with the device flags the agent README uses. You will state the course order out loud: the Python serial bridge in the next lesson comes first, and micro-ROS waits until that bridge’s units and the 300 ms watchdog already work. You will leave a written client topic plan that reuses `/cmd_vel`, telemetry out, and the same frame names as the simulator, even if you do not flash a board tonight.

## Prerequisites

Lesson 09-02’s picture of nodes and topics, lesson 08-01’s framed serial command, and lesson 10-01’s Jazzy shell. Docker is required for the agent command in the lab. You do not need a working micro-ROS firmware image tonight, and you should not rebuild the Capstone teleop around micro-ROS before lesson 10-04 passes. An ESP32 DevKit is the board this lesson talks about. A Pico may sit in a drawer; it is not the supported path below.


## Background Knowledge Map: XRCE-DDS Client–Agent Architecture, Static Memory, and Embedded Executors

Running ROS 2 on a 320 KB RAM microcontroller relies on three architectural adaptations:

- **XRCE-DDS (eXtremely Resource Constrained Environments):** Full DDS discovery and serialization are too heavy for an MCU. Instead, the MCU runs a tiny XRCE-DDS *client* over UART/Wi-Fi that talks to a host-side `micro-ros-agent`, which proxies topics into the standard ROS 2 DDS graph transparently.
- **Static Memory Allocation (`rclc`):** Dynamic `malloc`/`free` inside real-time firmware fragments RAM and causes unpredictable crashes after hours of operation. `rclc` pre-allocates fixed message buffers, executor handles, and timer slots at boot.
- **Deterministic Embedded Executor (`rclc_executor`):** A single-threaded executor polls subscriptions and periodic timers in a strict, bounded order—preserving real-time control timing while speaking native ROS 2 message types.
## Why this sits on the path

The Capstone firmware already accepts `V,left,right` and already drops torque when those frames stop. ROS 2 does not speak that frame, and this ESP32 does not speak full DDS. Lesson 10-04’s `rclpy` node is the translator you run first: ordinary Python, the protocol you already debugged, and a killed process still covered by the firmware watchdog. micro-ROS comes later. The client lives on the MCU, the agent on the PC turns XRCE into DDS, and `/cmd_vel` can reach the firmware without the Python scale function in between. Nav2 and a later learned policy still publish Twist either way. They will not debug an agent that never saw a client.

![micro-ROS client on the ESP32, agent on the PC, then the ROS 2 graph]({{ site.imgurl }}/generated/ch10_microros.png)

## Concepts

DDS is the middleware under ROS 2 topics. A normal `rclpy` node is a participant. A small microcontroller runs that stack only with pain and RAM. XRCE-DDS is the client profile for that constraint. The board runs a micro-ROS client, and the client does not appear on the ROS graph by itself. The agent, a process on the computer, is the participant. When the client creates a subscriber or a publisher, the agent creates the matching ROS 2 entity and forwards the bytes.

That fact is the empty topic list. With no agent, nothing acts for the board. With an agent that is only waiting, there is still no client session, so the entities were never created. Seeing only `/parameter_events` and `/rosout` means the agent is idle, not that the install failed.

The course agent is the Docker image tagged for this distro, `microros/micro-ros-agent:jazzy`. UDP on the laptop, which is the lab tonight because it needs no board, follows the agent README’s shape:

```bash
docker run -it --rm --net=host microros/micro-ros-agent:jazzy udp4 --port 8888
```

`--net=host` puts the container on the host network namespace so that, once a client does exist, DDS discovery on the laptop can see the agent. A bridge network without extra DDS configuration hides the agent from `ros2 topic list` even after a successful session. `--rm` deletes the container when you exit. Nothing is installed into the Jazzy underlay.

Serial is the transport you would use when the ESP32 enumerates as a USB serial device. Docker must be allowed to see the host device nodes. The agent README’s shape is a privileged container with `/dev` mounted, then the agent’s own serial arguments, including the device path:

```bash
docker run -it --rm --privileged -v /dev:/dev --net=host \
  microros/micro-ros-agent:jazzy serial --dev /dev/ttyUSB0 -b 115200
```

Flags before the image name are Docker. Arguments after `serial` are the agent: device and baud, matching Chapter 08. If a flag disagrees, the agent README wins. Do not run this container together with lesson 10-04’s Python bridge. One process may own `/dev/ttyUSB0`.

ESP32 is the board class micro-ROS treats as supported, with an ESP-IDF path aimed at this agent. The Pico has community ports: a tutorial may track another distro, and nothing promises that `microros/micro-ros-agent:jazzy` is the other end. Keep a Pico for MicroPython. Use an ESP32 DevKit for this agent.

The client you eventually flash should use the simulator’s ROS names. It subscribes to `/cmd_vel` as `geometry_msgs/msg/Twist` and publishes `std_msgs/msg/String` on `/capstone_telem`. If it publishes odometry, the frames are `odom` and `base_link`, the REP-105 names from lesson 09-05. Wheel commands inside the firmware stay in the −100…100 integers after the same scale lesson 10-04 writes down. micro-ROS does not repeal kinematics.

The watchdog does not move into the agent. The agent can crash, Docker can lose the device, and Wi-Fi UDP can go quiet. The firmware must still force the wheel command to zero when no fresh command arrives for 300 ms:

$$
\Delta t > 0.3\,\mathrm{s} \Rightarrow (n_L, n_R) = (0, 0)
$$

That is the same number as the serial bridge. A client that applies the last Twist forever, because “DDS is reliable,” fails open. Reliability here is a property of the transport you hope to have. The stop is a property of the board.

Do not power the motor driver from the USB port that flashes the ESP32 or carries the agent. The laptop supply sags, the chip resets, and the session dies mid-command. Motors stay on the fused pack, with a common ground, on the day you leave the dry run. Tonight you do not need that pack.

## Worked example

Write the topic plan on paper before you start Docker. One paragraph is enough, and it is half of the lab credit:

```text
Node name I will look for: /capstone_mcu
Subscribes: /cmd_vel   geometry_msgs/msg/Twist
Publishes:  /capstone_telem   std_msgs/msg/String
Frames if odometry is added later: odom -> base_link
Local rule: no fresh command for 300 ms => wheel integers 0,0
Not expected tonight: that node name in ros2 node list
```

Then start the agent with no board attached:

```bash
printenv ROS_DISTRO
docker run -it --rm --net=host microros/micro-ros-agent:jazzy udp4 --port 8888
```

`ROS_DISTRO` must be `jazzy` in the shell where you inspect the graph. Leave the container in the foreground. A healthy idle agent stays running and names `udp4` and port `8888`. It does not print a client session, because you did not start one.

Second terminal:

```bash
source /opt/ros/jazzy/setup.bash
ros2 node list
ros2 topic list
```

`/capstone_mcu` must not be on the list. Absence of the MCU node is the observation. A random demo publisher does not establish the Capstone contract. Skip it, or do not leave it as the robot’s interface.

Stop the container with Ctrl-C so the next run does not find port 8888 already taken. When a real client connects later, the agent log gains a session and `ros2 node list` gains the node you named. Write that prediction in the notes tonight; the next hardware session checks it.

### Deep-Dive Explanation (Read Slowly): Estimating RAM & UART Overhead of a micro-ROS Node

Before choosing between micro-ROS and a thin custom serial bridge on an MCU with $$264\ \text{KB}$$ SRAM (such as RP2040) or $$320\ \text{KB}$$ usable DRAM (ESP32), check the exact resource footprint:

1. **Static memory budget for a minimal 2-topic node (`/cmd_vel` sub + `/odom` pub):**
   - `rclc` + Micro-XRCE-DDS client static buffers (MTU = 512 B, 4 history slots): $$\approx 32\text{–}48\ \text{KB}$$ RAM.
   - `nav_msgs/msg/Odometry` struct (pose + twist + two $$6\times 6$$ `float64` covariance matrices = $$72 \times 8 = 576\ \text{bytes}$$ plus headers): $$\approx 0.72\ \text{KB}$$ per message.
   - Total static footprint stays comfortably under $$64\ \text{KB}$$ (~20% of ESP32 DRAM).
2. **Serial wire budget at 115,200 baud ($$11.52\ \text{kB/s}$$):**
   - Publishing a full `Odometry` message ($$\approx 720\ \text{B}$$ with XRCE framing) at $$20\ \text{Hz}$$ demands $$720 \times 20 = 14.4\ \text{kB/s}$$ — **exceeding** 115,200 baud!
   - Solution: bump UART to $$460\,800$$ or $$921\,600$$ baud ($$92.1\ \text{kB/s}$$), or publish compact wheel ticks (`Int32MultiArray`, ~40 B) at 50 Hz ($$2.0\ \text{kB/s}$$) and compute full `Odometry` on the host.

## Lab

1. Read this lesson’s architecture once with the agent README open beside it. Confirm the image tag is `jazzy`, not `humble` and not `iron`.
2. Write the topic plan in the worked example into `lab-notes.md`, including the 300 ms local stop and the frame names `odom` and `base_link`.
3. Run the UDP agent container exactly as written. Wait until the log is idle on `udp4` port `8888`. If the image pull starts, let it finish; the first pull is the slow part.
4. In another terminal, source Jazzy and run `ros2 node list` and `ros2 topic list`. Copy both into the notes. State in one sentence that the planned MCU node is absent because no client session exists.
5. Do not flash firmware tonight unless you already have a micro-ROS image and you want extra credit. If you cannot flash, the lab still passes: the idle agent log plus the written plan are the deliverable.
6. Stop the container. If you also sketched the serial command, include `--privileged`, `-v /dev:/dev`, and `--dev /dev/ttyUSB0` in the notes, and write “do not run this together with the Python bridge.”

**Expected**

The container remains in the foreground. The log identifies UDP port 8888 and does not claim a connected client. `ros2 node list` does not contain `/capstone_mcu` or whatever name you reserved in the plan. Your notes contain the subscription, the publication, and the 300 ms rule.

```text
agent waiting on udp4 port 8888
ros2 node list: no MCU node
lab-notes: cmd_vel in, capstone_telem out, frames odom and base_link
```

**Failure modes**

| What you see | Likely cause |
| --- | --- |
| `docker: command not found` | Docker is not installed. The lab needs the engine, not a second ROS install |
| Permission denied on the Docker socket | Your user is not in the `docker` group, or you did not start a new login after adding it. `sudo` is a temporary way through |
| Image tag `humble` pulls and runs | That agent speaks a different distro’s types. Use `:jazzy` to match the laptop |
| `ros2 node list` empty of MCU nodes, and you start reinstalling ROS | No client has connected. That empty list is the correct idle result |
| Serial agent and the Python bridge both open `/dev/ttyUSB0` | Two owners of one device. Stop one of them |
| Board resets when wheels are commanded | Motors were powered from the same USB link as the serial agent. Use the robot pack, not the laptop port |
| A Pico tutorial’s build flags fail against this image | Pico micro-ROS is community-port territory, not the supported ESP32 path |

## Where to buy this in Vietnam

The dry run needs Docker on the laptop, not a new PCB. When you flash, use an ESP32 DevKit like Capstone A. Search “ESP32” on [hshop.vn](https://hshop.vn/). Shopee or Lazada keyword: `ESP32 DevKit V1 30 chân`. The 2026 band is about 80.000–180.000 VND; recheck before you pay, and skip a bare module with no USB chip if you wanted a DevKit. Do not buy a Pico for this lesson, and do not power motors from the USB cable.

## Exercises

1. The agent container is running and you have not flashed anything. What must `ros2 topic list` refuse to show, and why? Guidance: it must refuse the MCU’s topics, because the agent only creates those entities after a client session.
2. This file is numbered before the serial-bridge lesson. Why does the course still tell you to finish that bridge first? Guidance: the Capstone firmware already speaks the Chapter 08 frame, and micro-ROS is the step after the units and the 300 ms watchdog are proven.
3. Write the `docker run` line for a serial agent on `/dev/ttyUSB0` and mark which flags belong to Docker. Guidance: `--privileged` and `-v /dev:/dev` are Docker; `--dev` and the baud belong to the agent after the word `serial`.
4. Draft the client contract in four lines: subscribed topic and type, published topic and type, frame ids, timeout. Guidance: `/cmd_vel` as Twist in, `/capstone_telem` as String out, frames `odom` and `base_link`, zeros after 300 ms.
5. A classmate wants the Pico to be the micro-ROS board because it is already on the bench. What do you tell them about support, in two sentences? Guidance: ESP32 is the supported class for this agent; Pico ports are community work and are not the path this lesson asks you to buy or flash.

## Further reading

- [micro-ROS](https://micro.ros.org/) is the project overview: client on the MCU, agent on the computer, XRCE-DDS in between.
- [micro-ROS agent repository](https://github.com/micro-ROS/micro-ROS-Agent) holds the Docker commands this lesson copies, including the `udp4` and `serial` transports. Prefer it if a flag drifts.
- [REP-105](https://www.ros.org/reps/rep-0105.html) is the frame-name contract the client plan reuses, so simulation and the board do not invent two trees.
