# Robotics Self-Learning / Tự học Robotics

**EN:** Build & Program Robots: From Embedded Systems to ROS 2 and Robot Learning  
**VI:** Lắp ráp & lập trình robot: Từ hệ thống nhúng đến ROS 2 và Robot Learning  

Author: **Nguyen Le Linh** (`nglelinh@gmail.com`)  
GitHub Pages: https://nglelinh.github.io/robotics-self-learning/

## How to study

1. Read Chapter 00 (tracks, safety, **kit catalog**).
2. Chapter 01 heavily covers **component identification** + labs.
3. Chapters 02–05: MCU, firmware patterns, sensors/actuators (with package ID).
4. Chapter 06: **mechanical mechanisms** (gears, linkages, bearings…).
5. Chapter 07: Capstone A teleop (no ROS).
6. Chapters 08–11: control, ROS 2 Jazzy, sim/micro-ROS, autonomy peek.
7. Chapter 12: LeRobot / ACT / Diffusion / VLA literacy + references.

Keep `lab-notes.md`. Prefer one working subsystem over many unfinished tutorials.

## Default BOM (Track A)

ESP32 **or** Pico · TT diff chassis · TB6612/DRV8833-class driver · HC-SR04 or ToF · optional IMU/encoders · matched battery+charger · meter + iron + breadboard kit (see Ch.00).

Optional later: Raspberry Pi 5 for onboard ROS 2.

## Images

- `img/generated/` — labeled educational diagrams created for this course
- `img/wikimedia/` — openly licensed photos; see `IMAGE_CREDITS.md`

## Build locally

```bash
bundle install
bundle exec jekyll serve
```

## Mac sync

This tree may be built on the agent box. To place it on the Mac teaching folder, see `MAC_SYNC.md`.
