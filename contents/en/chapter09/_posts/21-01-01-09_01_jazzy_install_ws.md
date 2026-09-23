---
layout: post
title: "Install ROS 2 Jazzy and a workspace"
chapter: "09"
order: 1
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter09
lesson_type: required
draft: false
---

Estimated time: **~90 minutes**, longer if Ubuntu itself is new.

## Learning objectives

You will install ROS 2 Jazzy Jalisco on Ubuntu 24.04 from the official deb packages, create an overlay workspace with `colcon`, and show that `ros2 topic list` works in a fresh terminal only after you source the underlay and the overlay in the right order. You will recognise a mixed Humble/Jazzy environment from the error text, and you will write a one-line note about where this laptop sits relative to the Capstone MCU.

## Prerequisites

You can use a terminal: `cd`, `sudo apt`, and a text editor. Ubuntu 24.04 (Noble) is the Tier-1 platform for Jazzy. A virtual machine or a second-hand mini PC is enough. The ESP32 from Chapters 02–08 stays on the robot; it does not run `colcon`. Chapter 08’s serial frame is the thing this computer will speak later. You do not need a lidar or a Pi for this lesson.

## Why this sits on the path

Capstone A proved the base moves under firmware. Jazzy is the messaging and tooling layer you will put beside that firmware, not a replacement for the motor watchdog. Every later command in Chapters 09–12 assumes one sourced distro. A workspace that sometimes sees Humble messages and sometimes Jazzy messages wastes a weekend that should have gone to TF and the bridge. Simulation in Chapter 10 uses the same install plus `ros-jazzy-ros-gz`. Nav2 and LeRobot do not get a turn until `ros2 topic list` is boring.

## Concepts

ROS 2 is a set of libraries and command-line tools on top of DDS. A **distro** is a frozen snapshot. Jazzy Jalisco targets Ubuntu 24.04. Humble targets 22.04. They are not drop-in substitutes, and sourcing both in one shell is a broken shell.

The **underlay** is `/opt/ros/jazzy`, installed by apt. The **overlay** is a workspace you build with `colcon`, usually `~/ros2_ws`. You source the underlay first, then the overlay. The overlay’s `setup.bash` remembers the underlay it was built against. Open a new terminal and you are back to a naked shell until your `.bashrc` sources them again.

`ros2` is the command. `topic list` talks to a daemon that discovers nodes. An empty list is a valid result: it means “no topics yet,” not “install failed,” as long as `ros2 doctor` or a talker from the next lesson can run.

Locale must be UTF-8 before you add the apt source. The official install fails early, with a clear message, when `locale` is POSIX. Fix that once.

![Underlay then overlay]({{ site.imgurl }}/generated/ch09_workspace.png)

Windows and macOS are not the path this course debugs. If your only machine is Windows, install Ubuntu 24.04 in a virtual machine with at least 4 GB of RAM and 30 GB of disk, or use a spare PC. WSL2 can work and also fails in ways this lesson will not chase (GUI, USB serial, Gazebo). A native Ubuntu install is the lab that matches the docs.

## Lab

Check the OS before any ROS command:

```bash
. /etc/os-release
echo "$VERSION_ID"
locale
```

`VERSION_ID` must be `24.04`. If it is `22.04`, stop. That machine gets Humble or a reinstall, not a force-installed Jazzy.

UTF-8, from the [Ubuntu deb install](https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html):

```bash
sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8
```

Open a new terminal so the locale sticks. Then the apt source and the desktop install. The repository line changes when `ros2-apt-source` updates, so copy it from the official page the week you install. The shape is:

```bash
sudo apt install curl -y
# follow the current "ros2-apt-source" block on the Jazzy install page
sudo apt update
sudo apt upgrade
sudo apt install ros-jazzy-desktop
sudo apt install python3-colcon-common-extensions python3-rosdep
```

`ros-jazzy-desktop` includes RViz, demos, and the CLI. `ros-jazzy-ros-base` is the smaller install for a robot PC that has no screen. Use desktop on the learning machine.

Source it, and make the source survive new terminals:

```bash
echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
source ~/.bashrc
printenv ROS_DISTRO
```

**Expected:** `jazzy`.

Workspace, from the [creating a workspace tutorial](https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Creating-A-Workspace/Creating-A-Workspace.html):

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws
colcon build
echo "source \$HOME/ros2_ws/install/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

The backslash before `$HOME` matters inside double quotes, or `.bashrc` stores a frozen path. Either a frozen absolute path or a correctly escaped `$HOME` is fine. Look at the file:

```bash
tail -n 5 ~/.bashrc
```

You want the underlay line **above** the overlay line.

Discovery check:

```bash
ros2 topic list
```

**Expected** on a quiet machine:

```text
/parameter_events
/rosout
```

Some installs show only those two, and a brand-new daemon can show an empty list for a moment. Run it twice. Then:

```bash
ros2 pkg list | head
which ros2
```

`which ros2` should print `/opt/ros/jazzy/bin/ros2`.

**Failure modes**

| What you see | Likely cause |
| --- | --- |
| `Unable to locate package ros-jazzy-desktop` | Not Ubuntu 24.04, or the apt source step was skipped |
| `ROS_DISTRO` empty in a new terminal | `.bashrc` was not sourced; on Ubuntu the terminal may be a login shell that skips it. Add the same line to `.profile` or reopen the terminal from the menu |
| `humble` and `jazzy` both appear in `echo $CMAKE_PREFIX_PATH` | You sourced two distros. Close every terminal. Keep one `source` line |
| `colcon: command not found` | `python3-colcon-common-extensions` missing, or you built before sourcing `/opt/ros/jazzy` |
| `ros2 topic list` hangs | Firewall or a stale daemon. `ros2 daemon stop` then try again |
| Disk full during `apt install` | Desktop wants several gigabytes. Free space or use `ros-jazzy-ros-base` |

Optional environment check:

```bash
ros2 doctor
```

Warnings about network interfaces are common on laptops. Errors about the distro are not.

## Where to buy this in Vietnam

Software only, until you want a robot computer that is not your laptop. A used office PC that already runs Ubuntu 24.04 is the cheapest host. When you outgrow the laptop, the board this course points at is a Raspberry Pi 5 (4 GB is a fair start for Jazzy plus a camera; 8 GB is kinder to Nav2 later).

| Item | Shop | Notes | 2026 band |
| --- | --- | --- | --- |
| Raspberry Pi 5 | [Hshop, UK-made board](https://hshop.vn/may-tinh-raspberry-pi-5-made-in-uk) | Pick RAM on the page. The listed price moves with the variant | from about 2.4 million VND for the small-RAM board; 4 GB and 8 GB cost more. Recheck |
| Pi 5 kit (PSU, case, fan, card) | [Hshop basic kit](https://hshop.vn/combo-raspberry-pi-5-ram-4-8gb-basic-kit) | The 27 W USB-C supply matters. A phone charger is a brownout | kit price is above the bare board |
| microSD 64 GB A2 | Shopee/Lazada `thẻ nhớ microSD 64GB A2` | For the Pi, not for the laptop lab | about 150.000–350.000 VND |

Shopee keyword if Hshop is out of stock: `Raspberry Pi 5 4GB chính hãng`. Avoid listings that are “vỏ case” only. The ESP32 stays the motor computer. The Pi, later, is the ROS computer.

## Exercises

1. Paste the output of `printenv ROS_DISTRO` and `which ros2` into `lab-notes.md`. Guidance: both must say jazzy and `/opt/ros/jazzy/...`.
2. What is wrong with a `.bashrc` that sources `~/ros2_ws/install/setup.bash` and never sources `/opt/ros/jazzy`? Guidance: the overlay setup usually chains the underlay it was built with. If you built before Jazzy existed in the environment, the chain is empty and `ros2` disappears. Source the underlay, rebuild, then source the overlay.
3. A friend on Ubuntu 22.04 asks you to paste your install commands. What do you tell them? Guidance: those commands are for 24.04 and Jazzy. Humble is the matching distro for 22.04. Do not mix.
4. Why is the ESP32 not “in the workspace”? Guidance: the workspace is a Linux colcon tree. The MCU keeps Chapter 08’s firmware. Chapter 10 connects them with a bridge or micro-ROS, which is a later install.
5. After a reboot, the first terminal cannot find `ros2`. Name the file you open. Guidance: `~/.bashrc`, and confirm the terminal actually reads it.

## Further reading

- [Ubuntu (deb packages) for Jazzy](https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html). Use this page’s apt-source block, not a blog’s old `sources.list` line.
- [Creating a workspace](https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Creating-A-Workspace/Creating-A-Workspace.html).
- [REP-2000](https://www.ros.org/reps/rep-2000.html) for which distro matches which Ubuntu.
- [colcon documentation](https://colcon.readthedocs.io/en/released/user/quick-start.html) for `colcon build --symlink-install`, which you will want once packages contain Python.
