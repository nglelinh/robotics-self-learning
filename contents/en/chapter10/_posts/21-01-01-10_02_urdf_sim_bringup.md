---
layout: post
title: "URDF bring-up in simulation"
chapter: "10"
order: 2
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter10
lesson_type: required
draft: false
---

Estimated time: **~90 minutes**.

## Learning objectives

You will bring the Chapter 09 xacro into a running Harmonic world in a fixed order: expand the model, start `robot_state_publisher`, launch `empty.sdf -r`, spawn with `ros_gz_sim create`, then bridge `/clock` one way and `/cmd_vel` both ways. You will set the diff-drive plugin’s wheel joint names, separation, and radius to the same numbers as the xacro, using the course example of track 0.16 m and wheel radius 0.033 m. You will publish a slow `Twist` and watch the wheels roll in the Gazebo world itself. You will name five bring-up failures that leave a pretty RViz model while the simulated robot does nothing or falls through the floor. You will keep `use_sim_time` consistent with the bridged clock so timers and TF share one time base.

## Prerequisites

Lesson 10-01’s empty world launches and `gz topic -l` shows `/clock`. Lesson 09-06’s xacro exists, with a box body, cylindrical wheels, `continuous` wheel joints, and inertial tags. Lesson 08-04’s inverse kinematics is the meaning of `cmd_vel`: $$v$$ forward and $$\omega$$ about $$+z$$. You can source Jazzy in every new terminal. RViz is optional tonight; the pass condition is motion in the simulator.

## Why this sits on the path

The xacro was a drawing and a TF tree. Harmonic is the first time that drawing has mass, contact, and a clock. Nav2 will later publish `geometry_msgs/Twist` on `/cmd_vel`. In simulation the listener is Gazebo’s diff-drive system. On the real Capstone, lesson 10-04’s serial bridge is a second listener on the same topic. If the plugin’s track or radius disagrees with the xacro, every later bag inherits that scale error. Spawn order is the skill. A random stack of terminals looks like a physics bug.

![Order of operations from xacro to a rolling model in Harmonic]({{ site.imgurl }}/generated/ch10_sim_bringup.png)

## Concepts

Bring-up is an order, not a single command.

First the description. `xacro` expands properties into a URDF that both `robot_state_publisher` and the spawn tool can read. The course model uses a box body, cylindrical wheels, `continuous` joints named `left_wheel_joint` and `right_wheel_joint`, and an `<inertial>` on every link that collides. Track is 0.16 m and wheel radius is 0.033 m. Those two numbers are about to be copied into the plugin. Change only one place and the picture and the roller disagree.

Second, `robot_state_publisher`. It publishes the TF tree from the URDF. Fixed joints appear even when `joint_states` is empty. In simulation it should use the Gazebo clock once that clock is bridged, otherwise its stamps live on a different timeline from the scan and the odometry you will add later.

Third, the world. Launch `empty.sdf` with `-r` so the server is running, not paused. The world name inside that file is `empty`. Remember it.

Fourth, spawn. The create tool inserts the URDF into a world that is already running. The world argument has to be that same name:

```bash
ros2 run ros_gz_sim create -world empty -file /tmp/capstone.urdf -name capstone
```

`-world shapes` while the server is running `empty.sdf` does not create a second universe. It fails to find the world. `-file` wants the expanded URDF, not the raw `.xacro`, unless you have already expanded it. The `-name capstone` is the model name you will look for in the GUI.

Fifth, the bridges. Run the help once if lesson 10-01’s notes are gone:

```bash
ros2 run ros_gz_bridge parameter_bridge -h
```

Clock travels from Gazebo to ROS and must not be driven the other way. The README form is one way, Gazebo to ROS:

```bash
ros2 run ros_gz_bridge parameter_bridge /clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock
```

The `[` sits between the ROS type and the Gazebo type. Command velocity in this course uses the README’s bidirectional form, so a Twist published on the ROS graph is visible to the plugin and a Gazebo-side publisher would also be visible to ROS:

```bash
ros2 run ros_gz_bridge parameter_bridge /cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist
```

You can pass both arguments to one `parameter_bridge` process. Do not invent the opposite clock direction. A ROS node that publishes `/clock` while Gazebo also publishes it gives every `use_sim_time` node two opinions.

The plugin that turns `/cmd_vel` into wheel motion is Gazebo Sim’s diff-drive system, loaded from the model. Put a short block in the xacro and keep the numbers lined up with the properties. The fields this course relies on are the joint names, the separation, the radius, and a speed cap:

```xml
<gazebo>
  <plugin filename="gz-sim-diff-drive-system" name="gz::sim::systems::DiffDrive">
    <left_joint>left_wheel_joint</left_joint>
    <right_joint>right_wheel_joint</right_joint>
    <wheel_separation>0.16</wheel_separation>
    <wheel_radius>0.033</wheel_radius>
    <max_linear_velocity>0.5</max_linear_velocity>
  </plugin>
</gazebo>
```

`left_joint` and `right_joint` must be the URDF joint names, not the link names. `wheel_separation` is the track $$L$$ from lesson 08-04. `wheel_radius` is the rolling radius. If the installed Harmonic demo uses a different tag set, copy those tag names and keep these meanings. Do not paste a long plugin of odometry fields you have not read.

The kinematics the plugin is approximating are the same inverse map as the firmware bridge:

$$
v_R = v + \omega \frac{L}{2}, \qquad v_L = v - \omega \frac{L}{2}
$$

with $$L = 0.16$$. Distance per revolution of one wheel is

$$
s = 2 \pi r
$$

with $$r = 0.033$$, so one revolution is about 0.207 m of tread. If the plugin’s `wheel_radius` is 0.05 while the cylinder you drew is 0.033, the drawn wheel and the contact radius are different objects. The robot will not travel the distance you compute from the URDF.

`use_sim_time` is a contract with `/clock`. After the clock bridge is up, start `robot_state_publisher` with `-p use_sim_time:=true`, and put simulator sensors on that clock too. A node left on wall time stamps messages the simulator does not share: TF extrapolation errors, or a robot that moved in Gazebo while RViz is stale. The opposite mistake, `use_sim_time` true before any `/clock` exists, freezes timers. Bridge the clock, echo it, then turn the parameter on.

RViz is a camera, not the plant. RobotModel draws the URDF even when spawn failed. The pass condition is the model in the Gazebo window, wheels rotating when `/cmd_vel` is published. With no display, use the odometry topic `gz topic -l` shows and confirm its position changes during the Twist. Do not require RViz to prove the physics.

Collision and inertia are what keep the body on the ground plane. A link with a visual and no collision does not touch the floor. A link with collision and no inertia is rejected or blows up the step. The chassis needs both, and each wheel needs both, because the wheels are the contact patches.

## Worked example

Assume the xacro from lesson 09-06 is at `~/ros2_ws/src/capstone_description/urdf/capstone.urdf.xacro`, with the plugin block added, `track` 0.16, and `wheel_r` 0.033. Expand it:

```bash
source /opt/ros/jazzy/setup.bash
xacro ~/ros2_ws/src/capstone_description/urdf/capstone.urdf.xacro > /tmp/capstone.urdf
```

Terminal A, description, using the Gazebo clock:

```bash
source /opt/ros/jazzy/setup.bash
ros2 run robot_state_publisher robot_state_publisher --ros-args \
  -p use_sim_time:=true \
  -p robot_description:="$(cat /tmp/capstone.urdf)"
```

Terminal B, world:

```bash
source /opt/ros/jazzy/setup.bash
ros2 launch ros_gz_sim gz_sim.launch.py gz_args:="empty.sdf -r"
```

Terminal C, after the window or the server log is up:

```bash
source /opt/ros/jazzy/setup.bash
ros2 run ros_gz_sim create -world empty -file /tmp/capstone.urdf -name capstone
```

You should see the box and two cylinders in the world, sitting on the plane, not sinking. Then the bridges, one process, clock first in the argument list so you remember which symbol is one-way:

```bash
source /opt/ros/jazzy/setup.bash
ros2 run ros_gz_bridge parameter_bridge \
  /clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock \
  /cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist
```

Check the clock from a fifth shell:

```bash
source /opt/ros/jazzy/setup.bash
ros2 topic echo /clock --once
```

The seconds field should be greater than zero because `-r` is set. If it is zero, the world is paused.

A slow straight command, held briefly:

```bash
ros2 topic pub --times 20 /cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 0.2, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"
```

Twenty messages is a short roll, not a drive across the room. In the Gazebo window the base moves along its $$+x$$ and both wheels spin. When the publisher ends, the model must stop being driven. `linear.y` stays 0 because a diff-drive cannot sideslip. With $$L/2 = 0.08$$, $$v = 0.2$$ and $$\omega = 0$$ ask both treads for 0.2 m/s. You need to see both wheels turn the same way.

## Lab

1. Add the short diff-drive block to the xacro. Set `wheel_separation` to the track property and `wheel_radius` to the wheel radius property. Re-run `xacro` into `/tmp/capstone.urdf` after every edit.
2. Start `robot_state_publisher` with `use_sim_time:=true` and the expanded description.
3. Launch `empty.sdf -r`. Confirm `gz topic -l` still shows `/clock`.
4. Spawn with `-world empty`, `-file /tmp/capstone.urdf`, and `-name capstone`. Look at the Gazebo view, not only at RViz. The body should rest on the plane.
5. Start one `parameter_bridge` with the clock argument using `[` and the `cmd_vel` argument using `@`, exactly as in the worked example. Echo `/clock` once and confirm the clock is moving.
6. Publish `linear.x` 0.2 for a short burst (`--times 20` or a couple of seconds). Watch the world.
7. Stop the publisher. The model must stop being driven. Ctrl-C the bridge and publish again: the model should sit still, which proves the motion depended on the bridge.

**Expected**

The model named `capstone` is visible in the Harmonic world, above the ground plane. During the burst, both wheels roll in that world and the base translates forward. After the burst, it is no longer under power. `/clock` echoes a non-zero time. Motion that exists only in an RViz RobotModel, while the Gazebo model sits or is absent, does not pass.

```text
capstone visible in the empty world
/clock sec > 0
wheels rolling in Gazebo while linear.x is 0.2
```

**Failure modes**

| What you see | Likely cause |
| --- | --- |
| Spawn errors, or the model never appears | World name mismatch (`shapes` versus `empty`), or `create` was pointed at the `.xacro` instead of the expanded URDF |
| Model falls through the floor | A link has visual geometry and no collision, so nothing rests on the plane |
| Instant explosion, or the model is rejected | Collision without `<inertial>`, or an inertia of zero |
| Wheels spin like coins, or the base slides without rolling | Joint axis is not the axle. Lesson 09-06 used `<axis xyz="0 1 0"/>` after the cylinder roll |
| `cmd_vel` echoes in ROS, Gazebo never moves | Bridge not running, or the plugin joint names are not `left_wheel_joint` and `right_wheel_joint` |
| TF is stale, or a node with `use_sim_time` never ticks | Clock not bridged, world paused because `-r` was omitted, or only some nodes are on sim time |

## Where to buy this in Vietnam

Software only. The lab runs on the same Ubuntu 24.04 laptop as lesson 10-01. You do not need a new board, a lidar, or a robot on the desk. The physical Capstone stays powered down; this lesson never talks to a serial port.

## Exercises

1. The xacro track is 0.16 and the plugin `wheel_separation` is 0.20. Which number does the rolling contact use, and what do you change? Guidance: the plugin’s separation drives the sim kinematics, so edit it to 0.16 and respawn rather than “fixing” it in RViz.
2. You send $$v = 0$$ and $$\omega = +0.5$$ rad/s. Which wheel command is larger under the course sign convention? Guidance: the right wheel, because positive yaw is a left turn when $$+x$$ is forward and $$+y$$ is left.
3. The launch uses `empty.sdf` and `create` is called with `-world shapes`. What fails, and which flag do you edit? Guidance: `create` looks up a running world by name, so `-world` must be `empty` while that SDF is the one you launched.
4. Duplicate the URDF, delete the chassis `<inertial>`, and spawn the copy. Record the simulator’s complaint, then restore the tag. Guidance: Harmonic cannot integrate a colliding body that has no mass properties; the visual box is not a substitute.
5. Why is `/clock` bridged with `[` rather than with a second `@`? Guidance: `parameter_bridge -h` marks `[` as Gazebo to ROS, and a bidirectional clock would let some other node publish a second time base.

## Further reading

- [ros_gz_bridge README](https://github.com/gazebosim/ros_gz/blob/ros2/ros_gz_bridge/README.md) is the authority for the `@` and `[` forms used above. Re-read it if a bridge starts and the topic types do not match.
- [Gazebo Harmonic getting started](https://gazebosim.org/docs/harmonic/getstarted/) covers the world process this spawn attaches to.
- [Gazebo with ROS](https://gazebosim.org/docs/harmonic/ros_installation/) documents the `ros_gz_sim` launch and the Jazzy pairing.
- [REP-103](https://www.ros.org/reps/rep-0103.html) is the axis convention behind “positive yaw means left.”
- [REP-105](https://www.ros.org/reps/rep-0105.html) is the frame chain `robot_state_publisher` is already publishing from the URDF.
