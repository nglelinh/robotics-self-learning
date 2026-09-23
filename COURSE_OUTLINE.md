# COURSE_OUTLINE — Robotics Self-Learning
**EN title:** Build & Program Robots: From Embedded Systems to ROS 2 and Robot Learning
**VI title:** Lắp ráp & lập trình robot: Từ hệ thống nhúng đến ROS 2 và Robot Learning
**Author:** Nguyen Le Linh `<nglelinh@gmail.com>`
**Site:** https://nglelinh.github.io/robotics-self-learning/

## Chapter map

| Ch | EN | VI | Lessons |
|----|----|----|--------:|
| 00 | Introduction, Tracks, Kits & Safety | Giới thiệu, lộ trình, bộ kit & an toàn | 7 |
| 01 | Electronics, Component ID & Lab Safety | Điện tử, nhận diện linh kiện & an toàn lab | 11 |
| 02 | Microcontrollers: Arduino, ESP32, Pico | Vi điều khiển: Arduino, ESP32, Pico | 6 |
| 03 | Embedded Programming Patterns for Robots | Mẫu lập trình nhúng cho robot | 6 |
| 04 | Sensors & Sensor Package Identification | Cảm biến & nhận diện module cảm biến | 7 |
| 05 | Actuators, Drivers & Identification | Cơ cấu chấp hành, driver & nhận diện | 7 |
| 06 | Mechanical Mechanisms, Assembly & CAD-lite | Cơ cấu cơ khí, lắp ráp & CAD nhẹ | 9 |
| 07 | Capstone A: Diff-Drive + Teleop Firmware | Capstone A: Robot vi sai + firmware teleop | 6 |
| 08 | Communications & Control Loops | Truyền thông & vòng điều khiển | 5 |
| 09 | ROS 2 Jazzy Foundations | Nền tảng ROS 2 Jazzy | 6 |
| 10 | Simulation & micro-ROS | Mô phỏng & micro-ROS | 5 |
| 11 | Autonomy & Perception Intro | Tự hành & nhận thức mở đầu | 5 |
| 12 | Modern Robot Learning & Next Paths | Robot learning hiện đại & hướng đi tiếp | 5 |

**Total EN lessons:** 85 (×2 with VI ≈ 170 files)

## Emphasis added (2026 refresh)

### Component identification track
Ch.00 tooling catalog → Ch.01 resistor/cap/diode/transistor/connector/driver/MCU ID + lab → Ch.04 sensor packages → Ch.05 motor driver boards.

### Mechanisms track
Ch.06 fasteners/bearings, gear ratios & backlash, linkages/belts/cams, wheels/casters/diff-drive diagrams, materials, failure modes + measurement lab.

### Image-heavy labs
Diagrams in `img/generated/` (color codes, Ohm triangle, breadboard, H-bridge, diff-drive, gears, four-bar, sensor ID sheet, lookalikes, kit overview). Commons photos in `img/wikimedia/` with `IMAGE_CREDITS.md`.

## Emphasis added (2026 refresh)
- Ch.00 kit catalog & tooling labs
- Ch.01 deep component identification + ID lab
- Ch.04–05 sensor/driver package ID
- Ch.06 mechanisms: gears, linkages, belts, bearings, failure modes
- Generated educational diagrams under `img/generated/`
- Wikimedia Commons photos under `img/wikimedia/` (see IMAGE_CREDITS.md)

## References (public)
- ros2: https://docs.ros.org/en/jazzy/
- ros2t: https://docs.ros.org/en/jazzy/Tutorials.html
- nav2: https://docs.nav2.org/
- gazebo: https://gazebosim.org/docs/harmonic/
- microros: https://micro.ros.org/
- esp32: https://docs.espressif.com/projects/esp-idf/en/latest/esp32/
- pico: https://www.raspberrypi.com/documentation/microcontrollers/raspberry-pi-pico.html
- arduino: https://docs.arduino.cc/
- pio: https://docs.platformio.org/
- lerobot: https://github.com/huggingface/lerobot
- hf: https://huggingface.co/docs/lerobot
- duck: https://docs.duckietown.com/
- mit: https://manipulation.mit.edu/
- moveit: https://moveit.picknik.ai/main/index.html
- urdf: https://docs.ros.org/en/jazzy/Tutorials/Intermediate/URDF/URDF-Main.html
- tf2: https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-TF2.html
- lino: https://github.com/linorobot/linorobot2
- logic: https://learn.sparkfun.com/tutorials/logic-levels
- pololu: https://www.pololu.com/docs/0J44
- pid: https://www.ni.com/en/shop/labview/pid-theory-explained.html
- mqtt: https://mqtt.org/
- cv: https://docs.opencv.org/4.x/
- act: https://tonyzhaozh.github.io/aloha/
- dp: https://diffusion-policy.cs.columbia.edu/
- rt1: https://robotics-transformer1.github.io/
- openx: https://robotics-transformer-x.github.io/
- bt: https://www.behaviortree.dev/
- slam: https://github.com/SteveMacenski/slam_toolbox

Optional advanced: MIT Manipulation (Drake) — not required.

## Chapter 00: Introduction, Tracks, Kits & Safety / Giới thiệu, lộ trình, bộ kit & an toàn

- **EN** 00-01 Welcome, outcomes, and how to study
  **VI** Chào mừng, mục tiêu và cách học
- **EN** 00-02 Learning tracks: budget MCU vs ROS path
  **VI** Hai lộ trình: MCU tiết kiệm vs ROS
- **EN** 00-03 Safety mindset for robot labs (lab)
  **VI** Tư duy an toàn trong lab robot
- **EN** 00-04 Lab kit catalog: tools and bench equipment (lab)
  **VI** Danh mục kit lab: dụng cụ và thiết bị bàn
- **EN** 00-05 Bill of materials and shopping strategy
  **VI** BOM và chiến lược mua linh kiện
- **EN** 00-06 Workspace, tools, and toolchain preview
  **VI** Không gian làm việc và toolchain
- **EN** 00-07 Chapter 00 lab checklist: bench ready (lab)
  **VI** Checklist lab chương 00: sẵn sàng bàn làm việc

## Chapter 01: Electronics, Component ID & Lab Safety / Điện tử, nhận diện linh kiện & an toàn lab

- **EN** 01-01 Voltage, current, power, and Ohm's law
  **VI** Điện áp, dòng, công suất và định luật Ohm
- **EN** 01-02 Breadboards, multimeters, and probing (lab)
  **VI** Breadboard, đồng hồ vạn năng và đo
- **EN** 01-03 Resistor ID: THT color bands and SMD codes (lab)
  **VI** Nhận diện điện trở: màu THT và mã SMD
- **EN** 01-04 Capacitors, diodes, and LEDs identification (lab)
  **VI** Nhận diện tụ, diode và LED
- **EN** 01-05 Transistors, MOSFETs, regulators, and IC packages (lab)
  **VI** Transistor, MOSFET, ổn áp và package IC
- **EN** 01-06 Connectors, motor drivers, and MCU board ID (lab)
  **VI** Connector, driver motor và nhận diện board MCU
- **EN** 01-07 Reading datasheets and pinouts
  **VI** Đọc datasheet và sơ đồ chân
- **EN** 01-08 Soldering basics for robot harnesses (lab)
  **VI** Hàn cơ bản cho dây robot
- **EN** 01-09 ESD, polarity, fuses, and brownouts
  **VI** ESD, cực tính, cầu chì và sụt áp
- **EN** 01-10 Lab: continuity, ohmmeter ID, and lookalikes (lab)
  **VI** Lab: thông mạch, đo ohm và linh kiện dễ nhầm
- **EN** 01-11 Chapter 01 lab checklist (lab)
  **VI** Checklist lab chương 01

## Chapter 02: Microcontrollers: Arduino, ESP32, Pico / Vi điều khiển: Arduino, ESP32, Pico

- **EN** 02-01 MCU landscape for hobby robots
  **VI** Bản đồ MCU cho robot hobby
- **EN** 02-02 Arduino IDE / PlatformIO for ESP32 (lab)
  **VI** Arduino IDE / PlatformIO với ESP32
- **EN** 02-03 Raspberry Pi Pico & MicroPython setup (lab)
  **VI** Pico và cài đặt MicroPython
- **EN** 02-04 Lab: first blink, serial, and hello robot (lab)
  **VI** Lab: blink, serial và hello robot
- **EN** 02-05 Pinouts, levels, and board power rails
  **VI** Pinout, mức logic và nguồn board
- **EN** 02-06 Chapter 02 lab checklist (lab)
  **VI** Checklist lab chương 02

## Chapter 03: Embedded Programming Patterns for Robots / Mẫu lập trình nhúng cho robot

- **EN** 03-01 C++ vs MicroPython for robots
  **VI** C++ vs MicroPython cho robot
- **EN** 03-02 Lab: GPIO digital I/O patterns (lab)
  **VI** Lab: mẫu GPIO digital I/O
- **EN** 03-03 PWM, timers, and motor drive signals (lab)
  **VI** PWM, timer và tín hiệu motor
- **EN** 03-04 Interrupts, debouncing, and ISRs (lab)
  **VI** Ngắt, chống dội và ISR
- **EN** 03-05 State machines for robot firmware
  **VI** Máy trạng thái trong firmware
- **EN** 03-06 Chapter 03 lab checklist (lab)
  **VI** Checklist lab chương 03

## Chapter 04: Sensors & Sensor Package Identification / Cảm biến & nhận diện module cảm biến

- **EN** 04-01 Sensor interfaces: I2C, SPI, UART
  **VI** Giao diện cảm biến: I2C, SPI, UART
- **EN** 04-02 Sensor package ID: HC-SR04, ToF, IMU, IR, encoders, cameras (lab)
  **VI** Nhận diện module: HC-SR04, ToF, IMU, IR, encoder, camera
- **EN** 04-03 Encoders and raw odometry counts (lab)
  **VI** Encoder và đếm odometry thô
- **EN** 04-04 IMU: accelerometer, gyro, fusion intro (lab)
  **VI** IMU: gia tốc, gyro, fusion
- **EN** 04-05 Lab: ultrasonic and Time-of-Flight ranging (lab)
  **VI** Lab: siêu âm và đo khoảng cách ToF
- **EN** 04-06 Cameras for robots: USB, CSI, bandwidth
  **VI** Camera cho robot: USB, CSI, băng thông
- **EN** 04-07 Chapter 04 lab checklist (lab)
  **VI** Checklist lab chương 04

## Chapter 05: Actuators, Drivers & Identification / Cơ cấu chấp hành, driver & nhận diện

- **EN** 05-01 DC motors and H-bridges
  **VI** Motor DC và cầu H
- **EN** 05-02 Motor driver board ID: L298N, TB6612, DRV8833 (lab)
  **VI** Nhận diện driver: L298N, TB6612, DRV8833
- **EN** 05-03 Hobby servos, PWM, and torque limits (lab)
  **VI** Servo hobby, PWM và mô-men
- **EN** 05-04 Steppers and microstepping intuition
  **VI** Stepper và microstep
- **EN** 05-05 Current limits, stalls, and thermal care
  **VI** Giới hạn dòng, stall và nhiệt
- **EN** 05-06 Lab: closed-loop intro sense → compute → act (lab)
  **VI** Lab: vòng kín cảm nhận → tính → tác động
- **EN** 05-07 Chapter 05 lab checklist (lab)
  **VI** Checklist lab chương 05

## Chapter 06: Mechanical Mechanisms, Assembly & CAD-lite / Cơ cấu cơ khí, lắp ráp & CAD nhẹ

- **EN** 06-01 Differential-drive chassis anatomy
  **VI** Giải phẫu khung robot vi sai
- **EN** 06-02 Fasteners, bearings, shafts, and couplings
  **VI** Ốc vít, bạc đạn, trục và khớp nối
- **EN** 06-03 Gears: spur, worm, planetary, ratio, backlash (lab)
  **VI** Bánh răng: trụ, worm, hành tinh, tỉ số, backlash
- **EN** 06-04 Linkages, cams, belts, and rack-and-pinion
  **VI** Cơ cấu thanh, cam, đai và bánh răng-thanh răng
- **EN** 06-05 Wheels, casters, and diff-drive mechanism diagrams
  **VI** Bánh xe, caster và sơ đồ cơ cấu vi sai
- **EN** 06-06 Chassis materials: 3D-print vs laser-cut
  **VI** Vật liệu khung: in 3D vs cắt laser
- **EN** 06-07 Mechanical failure modes and strain relief
  **VI** Hỏng hóc cơ khí và chống kéo dây
- **EN** 06-08 Lab: gear ratio measurement and assembly checklist (lab)
  **VI** Lab: đo tỉ số truyền và checklist lắp
- **EN** 06-09 Chapter 06 lab checklist (lab)
  **VI** Checklist lab chương 06

## Chapter 07: Capstone A: Diff-Drive + Teleop Firmware / Capstone A: Robot vi sai + firmware teleop

- **EN** 07-01 Assemble chassis, motors, and power (lab)
  **VI** Lắp khung, motor và nguồn
- **EN** 07-02 Lab: motor driver bring-up and spin test (lab)
  **VI** Lab: bring-up driver và test quay
- **EN** 07-03 Teleop over serial: protocol design (lab)
  **VI** Teleop serial: thiết kế giao thức
- **EN** 07-04 Firmware teleop loop (no ROS yet) (lab)
  **VI** Vòng teleop firmware (chưa ROS)
- **EN** 07-05 Field test, debug log, and acceptance (lab)
  **VI** Test thực địa, log và nghiệm thu
- **EN** 07-06 Chapter 07 capstone checklist (lab)
  **VI** Checklist capstone chương 07

## Chapter 08: Communications & Control Loops / Truyền thông & vòng điều khiển

- **EN** 08-01 Serial protocols beyond println
  **VI** Giao thức serial ngoài println
- **EN** 08-02 Lab: Wi-Fi and MQTT on ESP32 (lab)
  **VI** Lab: Wi-Fi và MQTT trên ESP32
- **EN** 08-03 PID intuition and tuning practice (lab)
  **VI** Trực giác PID và chỉnh tham số
- **EN** 08-04 Differential-drive kinematics
  **VI** Động học robot dẫn động vi sai
- **EN** 08-05 Control-loop timing and jitter
  **VI** Timing vòng điều khiển và jitter

## Chapter 09: ROS 2 Jazzy Foundations / Nền tảng ROS 2 Jazzy

- **EN** 09-01 Install ROS 2 Jazzy and a workspace (lab)
  **VI** Cài ROS 2 Jazzy và workspace
- **EN** 09-02 Nodes, topics, and messages (lab)
  **VI** Node, topic và message
- **EN** 09-03 Services and actions
  **VI** Service và action
- **EN** 09-04 Launch files, parameters, and QoS
  **VI** Launch, parameter và QoS
- **EN** 09-05 TF2 and coordinate frames
  **VI** TF2 và hệ tọa độ
- **EN** 09-06 URDF / xacro robot model basics
  **VI** URDF / xacro cơ bản

## Chapter 10: Simulation & micro-ROS / Mô phỏng & micro-ROS

- **EN** 10-01 Gazebo Harmonic intro and spawn (lab)
  **VI** Giới thiệu Gazebo Harmonic
- **EN** 10-02 URDF bring-up in simulation (lab)
  **VI** Bring-up URDF trong mô phỏng
- **EN** 10-03 micro-ROS on MCU (ESP32/Pico)
  **VI** micro-ROS trên MCU
- **EN** 10-04 Bridging Capstone A firmware to ROS 2 (lab)
  **VI** Nối Capstone A với ROS 2
- **EN** 10-05 Sim-to-real checklist (lab)
  **VI** Checklist sim-to-real

## Chapter 11: Autonomy & Perception Intro / Tự hành & nhận thức mở đầu

- **EN** 11-01 SLAM overview for beginners
  **VI** Tổng quan SLAM cho người mới
- **EN** 11-02 Nav2 stack tour
  **VI** Tour stack Nav2
- **EN** 11-03 Basic vision pipeline for robots
  **VI** Pipeline thị giác cơ bản
- **EN** 11-04 Behavior trees peek (Nav2 BT)
  **VI** Nhìn nhanh Behavior Tree
- **EN** 11-05 MoveIt 2 optional peek
  **VI** Nhìn nhanh MoveIt 2

## Chapter 12: Modern Robot Learning & Next Paths / Robot learning hiện đại & hướng đi tiếp

- **EN** 12-01 LeRobot / Hugging Face robotics intro
  **VI** Giới thiệu LeRobot / HF robotics
- **EN** 12-02 Imitation learning and ACT overview
  **VI** Học bắt chước và tổng quan ACT
- **EN** 12-03 Diffusion Policy intuition
  **VI** Trực giác Diffusion Policy
- **EN** 12-04 Vision-Language-Action models overview
  **VI** Tổng quan Vision-Language-Action
- **EN** 12-05 Curated next paths and full references
  **VI** Lộ trình tiếp theo và tài liệu
