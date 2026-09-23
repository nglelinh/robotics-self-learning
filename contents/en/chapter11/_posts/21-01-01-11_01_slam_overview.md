---
layout: post
title: "SLAM overview for beginners"
chapter: "11"
order: 1
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter11
lesson_type: required
draft: false
---

Estimated time: about 70 minutes with ROS 2 Jazzy already sourced, or about 50 minutes if you stop at the written interface contract because no lidar is on the desk.

## Learning objectives

You can draw the three-edge transform chain `slam_toolbox` expects, name the topics that must exist before `online_async_launch.py`, tell a bent hallway caused by a reversed encoder from a hallway that was never scanned, and say why a TF-Luna cannot fill `sensor_msgs/msg/LaserScan`.

## Prerequisites

You can use `ros2 topic info` and you know a transform tree is named frames, not a picture of the room. From the Capstone base, wheel encoders produce odometry, and a sign error on one motor makes a straight command look like a turn. Gazebo is only a mental picture of a simulated laser here.

## Why this lesson sits on the path

The course path runs from the Capstone differential-drive base, through ROS 2 Jazzy, through Gazebo, and only then into autonomy. A map is the first autonomy artifact that is not a motor command. `slam_toolbox` estimates where the robot is and what the walls are, at the same time, once a planar lidar exists. Gazebo can publish a pretend scan. The Capstone robot cannot. Until a real `LaserScan` and honest odometry exist, launching the mapper only reports missing interfaces. Later, Nav2 will consume this map. It will not draw it for you.

## Concepts

SLAM here means localization and mapping together in a plane. The lidar measures ranges along many bearings. Wheel odometry says how the base thinks it moved between scans. The mapper stitches scans into a grid and publishes a correction so encoder error does not slowly twist the map.

![Planar SLAM: a lidar sweep builds a map while the map-to-odom transform corrects wheel drift]({{ site.imgurl }}/generated/ch11_slam.png)

[REP-105](https://www.ros.org/reps/rep-0105.html) keeps three frames apart. `map` may jump when the mapper closes a loop. `odom`, integrated from the wheels, may drift and must not jump, or a controller following it will lurch. `base_link` is the body. For this course, SLAM publishes `map` to `odom`, the robot publishes `odom` to `base_link` from wheel odometry, and the URDF publishes a static `base_link` to the laser frame. The lidar driver does not invent that mount.

Composed, the pose of the body in the map is

$$
T_{\mathrm{map}\rightarrow\mathrm{base}} = T_{\mathrm{map}\rightarrow\mathrm{odom}} \, T_{\mathrm{odom}\rightarrow\mathrm{base}}.
$$

If the middle transform is a lie, the left transform cannot save the map. Consider a concrete sign error. Track width $$b = 0.20$$ m. Both wheels truly rolled one meter forward, so the robot went straight. The right encoder is wired with the wrong sign, so the odometry node sees $$\Delta s_l = 1.0$$ m and $$\Delta s_r = -1.0$$ m. With the usual planar model, forward travel and yaw are

$$
\Delta s = \frac{\Delta s_r + \Delta s_l}{2}, \qquad \Delta \theta = \frac{\Delta s_r - \Delta s_l}{b}.
$$

That substitution gives $$\Delta s = 0$$ and $$\Delta \theta = -10$$ rad. The robot drove down the hallway. The odometry says it spun in place. Scan matching then drags the walls along that phantom spin, and the hallway in the map bends. Fix the encoder sign, or the left/right assignment, before you touch SLAM parameters. A scale error looks different: both wheels too large by the same factor make a straight hallway that is too long, not a banana.

`sensor_msgs/msg/LaserScan` carries `angle_min`, `angle_max`, `angle_increment`, the range limits, a `ranges` array, and a `frame_id` that is already in TF. A 360-degree lidar at half-degree steps has on the order of 720 ranges. A TF-Luna has one range along one ray. It can warn a bumper. It cannot feed `slam_toolbox`.

An MPU6050 can later help a filter hold yaw between scans. It still does not paint walls. Lidar drivers usually publish best effort, because a late scan is worse than a dropped one. A subscriber that demands reliable delivery sits silent beside that publisher. Use the Jazzy QoS page when `ros2 topic echo` shows samples and the mapper still says it sees nothing.

## Worked example

Install the Jazzy binary, source the distro, and look at the launch line that this course treats as the shape of the command:

```bash
sudo apt install ros-jazzy-slam-toolbox
source /opt/ros/jazzy/setup.bash
ros2 launch slam_toolbox online_async_launch.py
```

That launch starts the online async mapper with the package default parameters. It will not build a map without `/scan` and TF. A missing scan topic, a missing `odom` to `base_link` transform, or an unknown laser frame means the interface is absent. Stop the node. Do not invent a fake scan.

Before you launch it on any robot, including a future Capstone bringup, the dry checks are:

```bash
source /opt/ros/jazzy/setup.bash
ros2 topic info /scan -v
ros2 topic info /odom -v
ros2 run tf2_ros tf2_echo odom base_link
```

`/scan` should be `sensor_msgs/msg/LaserScan` with a publisher count of at least one. `/odom` should be `nav_msgs/msg/Odometry`, `frame_id` `odom`, `child_frame_id` `base_link`. Pushing the robot forward should change translation, and rotating it should change yaw. Only then does the launch have a chance. Healthy SLAM adds `map` to `odom` (`ros2 run tf2_ros tf2_echo map odom`). That third echo is an outcome, not a transform you publish yourself.

## Lab

This lab is an interface contract, not a mapping contest. Copy the following requirement list into your notes and mark each line present, absent, or impossible with the sensor you actually own.

1. `/scan` exists, type `sensor_msgs/msg/LaserScan`, `frame_id` is the laser frame, and `ranges` covers a wide planar sweep rather than one number.
2. `/odom` exists, type `nav_msgs/msg/Odometry`, and a straight push moves `x` without inventing a large yaw.
3. TF contains `odom` to `base_link` from the robot and `base_link` to the laser frame as a static mount. `map` to `odom` is reserved for SLAM.
4. If the only ranger on the robot is a TF-Luna, write the sentence "this sensor cannot feed slam_toolbox" and stop. Do not launch the mapper and call the empty window a map.

Run the dry plan even when you expect failure:

```bash
source /opt/ros/jazzy/setup.bash
ros2 topic info /scan -v
ros2 topic info /odom -v
```

Expected output when nothing is publishing, which is the honest result on a machine with no lidar driver:

```text
Unknown topic '/scan'
Unknown topic '/odom'
```

Record that text. Both publishers are absent, so the launch is not a failed demo. If a driver or a bag is up, paste the block that names the message type and the publisher count next to the matching contract line.

| What you see | Likely cause | What to check |
| --- | --- | --- |
| Hallway bends like a banana | One encoder sign is flipped, or left and right are swapped | Drive straight and watch yaw in `/odom` |
| Hallway is straight but the wrong length | Wheel radius or track width | Compare one floor meter with odom `x` |
| Launch prints TF errors and the map stays empty | No `/scan`, no `odom` to `base_link`, or no laser frame | The three commands above |
| Echo shows scans but SLAM stays quiet | Reliable subscriber, best-effort publisher | `ros2 topic info /scan -v` |
| The "lidar" message is one distance | TF-Luna or any single-point ToF | Do not connect it to `slam_toolbox` |

## Buying parts in Vietnam

Buy a scanner only when you are ready to map. Student-scale planar lidars in the LD19, LD06, and YDLIDAR X2 class have recently sat around 1.5 to 3.5 million VND. Search Shopee with `lidar LD19 robot`, read the current listing, and prefer a documented serial protocol. That is the first buy if you buy anything.

The [RPLIDAR S2 on Hshop](https://hshop.vn/cam-bien-khoang-cach-dtof-lidar-rplidar-s2m1-r2e-30m-360-laser-range-scanner) is the expensive step up: 360 degrees, an Ethernet-style link, longer range. Recheck the live price. It is not the first student buy.

A Raspberry Pi 5 class board is the computer that can run the mapper on the robot. [Hshop's Pi 5 listing](https://hshop.vn/may-tinh-raspberry-pi-5-made-in-uk) has started near 2.4 million VND for low-RAM boards. Recheck. The Pi does not replace the lidar. Open the [TF-Luna page](https://hshop.vn/cam-bien-khoang-cach-dfrobot-tf-luna-tof-micro-single-point-ranging-lidar) and read "single-point" in the name: useful as a bumper, wrong for this lesson. The [MPU6050](https://hshop.vn/cam-bien-6-dof-bac-tu-do-gy-521-mpu6050) is optional for a later filter, not a substitute for the laser, and not required for the contract lab.

## Exercises

### Exercise 1

Draw the TF tree for a robot that is mapping a straight corridor. Label the publisher of each edge: SLAM, wheel odometry, or static URDF.

**Guidance.** Three edges are enough: `map` to `odom`, `odom` to `base_link`, `base_link` to the laser frame. If you add a fourth edge, say why it is static.

### Exercise 2

Using the sign-error numbers in the concepts section, recompute $$\Delta s$$ and $$\Delta \theta$$ if the right encoder is correct and the left encoder is the one that flipped sign. Say whether the phantom yaw changes direction.

**Guidance.** Keep $$b = 0.20$$ m. Only $$\Delta s_l$$ changes sign relative to the worked numbers. You do not need a robot.

### Exercise 3

Write the `/scan` contract you would hand to a teammate whose only ranger is a TF-Luna. Include message type, what `ranges` must contain, and the explicit refusal.

**Guidance.** One short paragraph. Name `sensor_msgs/msg/LaserScan`. State that one float is not an array of bearings.

### Exercise 4

A straight one-meter push changes odometry `x` by about one meter and changes yaw by less than a degree. The map hallway is still curved. Where do you look next, and where do you not look?

**Guidance.** Honest odometry moves suspicion onto the laser mount yaw and onto TF. Do not start by buying an IMU.

### Exercise 5

Write the exact `ros2 topic info` commands you will run before `online_async_launch.py`, and state what publisher count 0 means for the launch.

**Guidance.** Two commands, `/scan` and `/odom`, with `-v`. Publisher count 0 means the launch has nothing to fuse, so you stop.

## Further reading

- [slam_toolbox](https://github.com/SteveMacenski/slam_toolbox) documents the online async launch and its scan plus odometry assumptions.
- [REP-105](https://www.ros.org/reps/rep-0105.html) defines `map`, `odom`, and `base_link`.
- [Quality of service in Jazzy](https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Quality-of-Service-Settings.html) explains a reliable subscriber missing a best-effort scan.
- The [TF-Luna listing](https://hshop.vn/cam-bien-khoang-cach-dfrobot-tf-luna-tof-micro-single-point-ranging-lidar) shows the single-point wording on the product page.
