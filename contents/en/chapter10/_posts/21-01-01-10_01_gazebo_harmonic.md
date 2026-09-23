---
layout: post
title: "Gazebo Harmonic intro and spawn"
chapter: "10"
order: 1
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter10
lesson_type: required
draft: false
---

Estimated time: **~70 minutes**.

## Learning objectives

You will start a Gazebo Harmonic world from a ROS 2 Jazzy terminal and tell `gz sim` apart from the old `gazebo` Classic binary. You will explain why this course pairs Jazzy with Harmonic, and why sourcing Humble or installing Classic packages sends you into a different simulator. You will use `gz topic -l` to see that a running world already publishes `/clock`, and you will connect the `-r` flag to the play button so a paused world is not mistaken for a broken install. You will read the direction symbols printed by `ros_gz_bridge` without leaving a bridge running. You will record either a GUI window or a headless server log as evidence that the empty world stayed up.

## Prerequisites

Lesson 09-01 is done: Ubuntu 24.04, ROS 2 Jazzy debs, and a terminal where `printenv ROS_DISTRO` prints `jazzy`. You can keep two terminals open and you know that Ctrl-C stops the foreground process. No robot, no URDF, and no micro-ROS firmware are required tonight. If `printenv ROS_DISTRO` prints `humble`, fix that before you install anything in this lesson.

## Why this sits on the path

Capstone A already drives from the Chapter 08 frame, and Chapter 09 put topics, TF, and a xacro on the laptop. This lesson opens the simulator Nav2 will plan in, and that a later learning stack will record against the floor. The seam is the `ros_gz` family, not Classic `gazebo_ros`. Learn the process names while the world is empty, so a failed spawn next lesson is a model problem rather than a second install of the wrong Gazebo.

![Gazebo Harmonic beside ROS 2 Jazzy, with ros_gz between them]({{ site.imgurl }}/generated/ch10_gazebo_stack.png)

## Concepts

Gazebo Classic and Gazebo Sim are different codebases that share a nickname. Classic is the `gazebo` command that old ROS 1 tutorials still show. Gazebo Sim is the current line: command `gz sim`, SDF worlds, topics you list with `gz topic`. Harmonic is the Gazebo Sim release Jazzy is built against. Humble’s match was Fortress. A tutorial that says `sudo apt install gazebo` or `ros-humble-gazebo-ros-pkgs` is not a tutorial for this chapter.

Jazzy’s apt name for the integration is one metapackage:

```bash
sudo apt install ros-jazzy-ros-gz
```

That pulls the pieces this course actually calls: `ros_gz_sim` to launch and spawn, and `ros_gz_bridge` to copy selected topics between the two graphs. Installing it does not start a world. It only puts the executables on the ROS path after you source Jazzy.

Two stock worlds matter this week. `shapes.sdf` is the getting-started world with a few primitive bodies, useful when you want to know that the renderer drew something. `empty.sdf` is the world the rest of Chapter 10 spawns the Capstone into. The launch shape from the `ros_gz` docs is:

```bash
ros2 launch ros_gz_sim gz_sim.launch.py gz_args:="empty.sdf -r"
```

The string inside `gz_args` is handed to `gz sim`. The token `-r` means run. Without it the server loads the world and waits: the play button stays paused, and simulated time does not move. With `-r` the world is already running. A paused world is still a successful launch, and it will make every later `use_sim_time` node look frozen because `/clock` stays at zero.

`/clock` is a Gazebo topic before it is a ROS topic. While the server is up, `gz topic -l` lists it whether or not any ROS bridge exists. Bridging is the next lesson. The bridge’s direction symbols are easy to invert, so read them once tonight and do not start a bridge:

```bash
ros2 run ros_gz_bridge parameter_bridge -h
```

You want the help text only. The symbol between the ROS type and the Gazebo type is the direction. The forms this course will use, copied from the `ros_gz_bridge` README, are a bidirectional command velocity and a one-way clock. Bidirectional:

```bash
ros2 run ros_gz_bridge parameter_bridge /cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist
```

Clock, Gazebo toward ROS only:

```bash
ros2 run ros_gz_bridge parameter_bridge /clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock
```

Do not swap those symbols “to see what happens” tonight. A second publisher on `/clock` fights the simulator. Lesson 2 is where those two lines actually run.

Simulated time and wall time are not the same quantity. The real-time factor is

$$
\mathrm{RTF} = \frac{\Delta t_{\mathrm{sim}}}{\Delta t_{\mathrm{wall}}}
$$

When the GUI reports a factor near 1, one simulated second takes about one wall-clock second. If the factor falls, a 0.2 m/s command still means 0.2 m per simulated second, but a stopwatch runs ahead. An empty world on a normal laptop should sit near 1.

Headless running is the same server without the GUI. If `printenv DISPLAY` is empty, the window cannot open. Add the server-only switch that `gz sim --help` documents, typically `-s`:

```bash
ros2 launch ros_gz_sim gz_sim.launch.py gz_args:="empty.sdf -r -s"
```

The lab passes on that log when the process stays up and `gz topic -l` lists `/clock`. The laptop is the lab machine. A Pi 5 can host a lighter stack later; it is the wrong place to learn whether the GUI starts.

## Worked example

Three checks, in order, tell you which Gazebo you are about to launch.

```bash
printenv ROS_DISTRO
gz sim --help
apt-cache policy ros-jazzy-ros-gz
```

The first line must be `jazzy`. The help text must belong to `gz sim`. If the shell says `gz: command not found`, source Jazzy and look at the apt policy. A missing candidate means the Jazzy apt source is absent or the machine is not Ubuntu 24.04. Do not “fix” that by installing the `gazebo` package. Classic will not load this chapter’s launch file.

When the policy shows an installed candidate, start the empty world in one terminal and leave it there:

```bash
source /opt/ros/jazzy/setup.bash
ros2 launch ros_gz_sim gz_sim.launch.py gz_args:="empty.sdf -r"
```

In a second terminal, source Jazzy again and list Gazebo topics:

```bash
source /opt/ros/jazzy/setup.bash
gz topic -l
```

You are looking for `/clock`. `ros2 topic list` may be almost empty, because nothing has bridged the two graphs. Gazebo is publishing on its own graph. Ctrl-C the launch and the Gazebo topic list dies with the server. A picture of a closed window is not a running world.

## Lab

1. Confirm the distro with `printenv ROS_DISTRO`. Stop if it is not `jazzy`, source `/opt/ros/jazzy/setup.bash`, and check again. If both Humble and Jazzy are installed, the last `source` wins.
2. Install the integration metapackage: `sudo apt install ros-jazzy-ros-gz`. Refuse any follow-up command that installs a package named `gazebo` or `ros-humble-gazebo-ros-pkgs`.
3. In terminal A, launch the empty world with `gz_args:="empty.sdf -r"`. Leave that process in the foreground.
4. If no window appears, print `printenv DISPLAY`. When it is empty, stop the launch and start it again with `-s` added inside `gz_args`, as in the headless line above.
5. In terminal B, source Jazzy and run `gz topic -l`. Confirm `/clock` is present. Do not start `parameter_bridge`.
6. Run `ros2 run ros_gz_bridge parameter_bridge -h` and write down which symbol is bidirectional and which symbol is Gazebo-to-ROS. Then quit the help. `ros2 topic list` should still not show a bridged `/clock`.
7. Optional five-minute detour: launch `shapes.sdf` instead of `empty.sdf` once, see the primitives, then return to `empty.sdf -r`. The next lesson’s spawn names the world `empty`, so that is the server you leave running if you continue tonight.

**Expected**

A window titled as a Gazebo Sim session, already running because of `-r`, or a server process that does not exit when you started with `-s`. The second terminal prints a topic list that includes `/clock`. No `parameter_bridge` process is left running.

```text
/clock
/stats
```

Your list will be longer. `/clock` is the line that matters. `ros2 topic list` without a bridge does not need to show `/clock`.

**Failure modes**

| What you see | Likely cause |
| --- | --- |
| `Unable to locate package ros-jazzy-ros-gz` | Ubuntu is not 24.04, or the Jazzy apt source from the install guide was never added |
| `gazebo` starts a different window, `gz sim` is missing | Classic packages on `PATH`. Remove that habit; this chapter uses `gz sim` |
| Launch exits, or the GUI never appears | `DISPLAY` is empty. Use the server-only `-s` form, or run on a machine with a screen |
| `printenv ROS_DISTRO` prints `humble` | The shell sourced Humble last. Jazzy’s `ros_gz` will not load in that environment |
| `gz topic -l` cannot connect | The launch terminal was closed. The server is not running |
| Play button is paused and time stays at 0 | `-r` was left off. Press play once to see time move, then relaunch with `-r` |

## Where to buy this in Vietnam

This lab is software on the laptop you already use for Jazzy. No sensor and no ESP32 are required. A Raspberry Pi 5 is an optional later robot computer, not tonight’s GUI machine. The low-RAM board on Hshop has recently started around 2.4 million VND; that is a 2026 estimate, so recheck before you pay. Board: [Raspberry Pi 5 made in UK](https://hshop.vn/may-tinh-raspberry-pi-5-made-in-uk). Kit: [basic kit](https://hshop.vn/combo-raspberry-pi-5-ram-4-8gb-basic-kit). If the slugs move, search [hshop.vn](https://hshop.vn/) for “Raspberry Pi 5”. Shopee or Lazada keyword: `Raspberry Pi 5 4GB`, same 2026 caution. A listing far under the Hshop board usually omits the supply.

## Exercises

1. Run `printenv ROS_DISTRO` and `gz sim --help`. In two sentences, say why a missing `gazebo` binary is acceptable on this laptop. Guidance: the simulator for Jazzy is `gz sim` from the Harmonic line, and the `gazebo` binary is Classic.
2. Launch `empty.sdf` once without `-r` and once with `-r`. Write what the play control does in each case and whether simulated time moves. Guidance: without `-r` the server loads the world paused, so `/clock` does not advance until you press play.
3. Simulated time moves 2.0 s while your stopwatch moves 4.0 s. Compute the real-time factor and say whether an empty world on your laptop should look like that. Guidance: RTF is simulated time divided by wall time, so the value is 0.5, and an empty world should be nearer to 1.
4. Name the apt package this lesson installs and two package names that would pull the wrong simulator. Guidance: install `ros-jazzy-ros-gz`; do not install `gazebo` or a `ros-humble-gazebo-ros` package.
5. Copy the exact launch command you will need in the next lesson, including the world file and `-r`. Guidance: `gz_args` must contain `empty.sdf -r`, because the spawn tool will look up a world named `empty`.

## Further reading

- [Gazebo Harmonic getting started](https://gazebosim.org/docs/harmonic/getstarted/) shows `gz sim`, the shapes world, and the play control this lesson uses.
- [Gazebo Harmonic with ROS](https://gazebosim.org/docs/harmonic/ros_installation/) is the pairing note: Jazzy with Harmonic, and the `ros_gz` packages.
- [Jazzy Ubuntu deb install](https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html) is the apt-source page you need when `ros-jazzy-ros-gz` cannot be located.
- [ros_gz_bridge README](https://github.com/gazebosim/ros_gz/blob/ros2/ros_gz_bridge/README.md) is the source of the `@` and `[` command lines. Read it before lesson 2 runs them.
