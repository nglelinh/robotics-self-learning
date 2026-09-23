---
layout: post
title: "Launch files, parameters, and QoS"
chapter: "09"
order: 4
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter09
lesson_type: required
draft: false
---

Estimated time: **~90 minutes**.

## Learning objectives

You will start two nodes from one Python launch file, override a parameter from that file and from the command line, and produce a QoS incompatibility on purpose so `/chatter` looks alive while `ros2 topic echo` stays silent. You will read `ros2 topic info -v` well enough to say which side offered best-effort and which side demanded reliable. That diagnosis is the one you will reuse when a lidar driver and RViz refuse to meet in Chapter 11.

## Prerequisites

Lessons 09-01 and 09-02: Jazzy is sourced, and you have already echoed `/chatter` from `demo_nodes_cpp`. You can create a file under `~/ros2_ws/src`. You do not need the robot. A parameter, for this lesson, is a named value that belongs to a node (`use_sim_time`, a serial port, a track width), not a command-line flag of `apt`.

## Why this sits on the path

Typing `ros2 run` four times is how a demo starts. It is not how a Capstone base starts. The bridge, `robot_state_publisher`, the twist teleop, and later Nav2 all have to come up together, with the track width from lesson 08-04 written down as a parameter instead of a magic number in three files. QoS is the other half. A laser scan is a stream that may drop a packet. A map is a document that must arrive. ROS 2 will not deliver a best-effort scan to a reliable subscriber, and it often fails quietly. People then “fix” Nav2 for an afternoon when the graph was simply incompatible. Learn the quiet failure on `/chatter` before you meet it on `/scan`.

![Compatible and incompatible QoS]({{ site.imgurl }}/generated/ch09_qos.png)

## Concepts

A **launch file** describes a process graph. In Jazzy the file you will write is Python, using `launch` and `launch_ros`. It can start nodes, pass parameters, and include other launch files. XML launch still exists; this course uses Python because the official beginner tutorials do, and because you can compute a path with `PathJoinSubstitution` instead of hoping a relative path survives `colcon`.

A **parameter** is a typed value on a node: bool, int, double, string, or arrays of those. `ros2 param list /talker` shows what that node declared. `ros2 param get` reads one. Setting a parameter from the command line (`--ros-args -p name:=value`) overrides the default for that process only. A YAML file is how you keep a set of overrides for a robot:

```yaml
capstone_bridge:
  ros__parameters:
    port: /dev/ttyUSB0
    baud: 115200
    track_width: 0.16
    cmd_timeout_ms: 300
```

The key `ros__parameters` is required. A file that is just `track_width: 0.16` at the top level does not land on the node. The node name must match. Lesson 08-04’s measured $$L$$ belongs here, once, and the bridge reads it. Two copies, one in centimetres, was an exercise in that lesson for a reason.

**QoS** is a contract on a publisher and on a subscription. The policies that bite beginners are reliability, durability, and history depth.

Reliability: `reliable` retries, `best_effort` does not. A reliable subscription is compatible with a reliable publisher. A best-effort subscription is compatible with both. A reliable subscription is **not** compatible with a best-effort publisher. Sensor drivers (`sensor_msgs/LaserScan`, `Image`) usually publish best-effort with a small queue, the profile people call sensor data. RViz’s default LaserScan display has, at times, expected reliable. The fix is to change the display QoS or the subscription, not to reboot the lidar.

Durability: `volatile` keeps no history for late joiners. `transient_local` does, which is how a map published once can still be seen by a node that starts later. A volatile publisher does not satisfy a transient-local subscriber.

History depth is the queue length. Depth 1 means “only the latest scan matters,” which is what you want for a 10 Hz lidar and what you do not want for a burst of short commands if you also refuse to let the watchdog expire them.

`ros2 topic info /scan -v` prints the offered and requested profiles side by side. Incompatible endpoints show up as publishers and subscriptions that do not list each other as matched. Echo with the default QoS can sit there printing nothing. That is the lab.

## Worked example

Create a package and a launch file. From the sourced workspace:

```bash
cd ~/ros2_ws/src
ros2 pkg create capstone_bringup --build-type ament_python --dependencies launch_ros
mkdir -p capstone_bringup/launch capstone_bringup/config
```

`capstone_bringup/launch/talker_listener.launch.py`:

```python
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package="demo_nodes_cpp",
            executable="talker",
            name="talker",
            parameters=[{"use_sim_time": False}],
            output="screen",
        ),
        Node(
            package="demo_nodes_cpp",
            executable="listener",
            name="listener",
            output="screen",
        ),
    ])
```

Install rule: in `setup.py`, the `data_files` list must include the launch directory, or `ros2 launch` will not see the file after `colcon build`. A typical entry is:

```python
import os
from glob import glob
# inside data_files:
(os.path.join("share", package_name, "launch"), glob("launch/*.launch.py")),
```

Then:

```bash
cd ~/ros2_ws
colcon build --packages-select capstone_bringup
source install/setup.bash
ros2 launch capstone_bringup talker_listener.launch.py
```

**Expected:** one terminal prints `Publishing: 'Hello World: N'` and `I heard: [Hello World: N]`. Ctrl-C stops both nodes. That is the point of launch.

Parameter check, talker still running in another launch or via `ros2 run`:

```bash
ros2 param get /talker use_sim_time
```

**Expected:** `Boolean value is: False`.

QoS break, which you do on purpose. Terminal A publishes best-effort:

```bash
ros2 topic pub /chatter std_msgs/msg/String "{data: hi}" --qos-reliability best_effort
```

Terminal B echoes with the default, which is reliable:

```bash
ros2 topic echo /chatter
```

**Expected:** the publisher counts messages, the echo prints nothing. Confirm:

```bash
ros2 topic info /chatter -v
```

You should see a publisher reliability of best effort and a subscription reliability of reliable, and no indication that they are connected. Now echo with a matching policy:

```bash
ros2 topic echo /chatter --qos-reliability best_effort
```

**Expected:** `data: hi` starts appearing. Put that pair of commands in `lab-notes.md`. It is the template for “RViz shows no scan.”

## Lab

1. Build `capstone_bringup` and launch the talker and listener together. Save the log line that proves the listener heard the talker.
2. Add `capstone_bringup/config/bridge.yaml` with the four keys in the concepts section (`port`, `baud`, `track_width`, `cmd_timeout_ms`). You will not have the bridge node yet. Validate the YAML loads as text: `python3 -c "import yaml; print(yaml.safe_load(open('config/bridge.yaml')))"` from the package directory. **Expected:** a dict whose only top key is `capstone_bridge`, and inside it `ros__parameters`.
3. Run the best-effort versus reliable experiment. Record `ros2 topic info -v` for the broken case and for the fixed echo.
4. Optional: `ros2 topic hz /chatter` on the working echo. A `topic pub` without `--rate` is slow. Pass `-r 10` and expect a rate near 10.

**Failure modes**

| What you see | Likely cause |
| --- | --- |
| `file not found` on launch | `setup.py` does not install `launch/`, or you forgot to source the overlay after the build |
| Listener silent, talker fine, QoS not the issue | You launched two talkers and no listener, or the listener node crashed on a parameter type error |
| YAML “loads” but the node ignores `track_width` | Missing `ros__parameters`, or the node name in the file does not match |
| Echo works in one terminal and not another | One of them passed `--qos-reliability`. Defaults differ from what you think |
| `use_sim_time` true and the talker freezes later | Nothing is publishing `/clock`. Leave it false until Gazebo is in Chapter 10 |

## Where to buy this in Vietnam

No parts. The laptop from lesson 09-01 is the instrument. If you already bought a Pi 5 to be the robot computer, do this lab on the laptop first, then repeat `printenv ROS_DISTRO` on the Pi. Do not debug QoS and a flaky microSD card on the same afternoon.

## Exercises

1. Your bridge YAML sets `cmd_timeout_ms: 300` and the firmware also uses 300 ms. Which one fires if the laptop process dies but the USB cable stays plugged in? Guidance: the firmware watchdog. The YAML timeout only helps the bridge decide to *send* zeros. If the bridge process is dead, it sends nothing, and the MCU timer is the one that stops the wheels.
2. A classmate publishes `/scan` best-effort and opens RViz with reliability set to reliable. Quote the `topic info -v` line that settles the argument. Guidance: publisher reliability BEST_EFFORT, subscription RELIABLE, endpoints not matched.
3. Why is transient-local a reasonable durability for `/map` and a poor one for `/cmd_vel`? Guidance: a late RViz should still see the last map. A late bridge should not act on a Twist from ten minutes ago.
4. You want the launch file to refuse to start when `track_width` is missing. Is that a QoS problem? Guidance: no. It is a parameter declaration. The node should declare `track_width` without a silent default of `1.0`, or the launch file should pass it explicitly.
5. Order these in a future `capstone.launch.py`: serial bridge, `robot_state_publisher`, `teleop_twist_keyboard`. What must be a parameter, not a hard-coded string? Guidance: the serial port and the track width. Teleop can start last; it only publishes.

## Further reading

- [Launching multiple nodes](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Launch/Launch-Main.html) and the [creating a launch file](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Launch/Creating-Launch-Files.html) tutorial.
- [Understanding parameters](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Parameters/Understanding-ROS2-Parameters.html).
- [About Quality of Service settings](https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Quality-of-Service-Settings.html). Read the compatibility tables, not only the names.
- `ros2 topic echo -h` on your machine. The QoS flags in that help text are the ones the lab used.
