---
layout: post
title: "Cameras for robots: USB, CSI, bandwidth"
chapter: "04"
order: 6
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter04
lesson_type: required
draft: false
---

Estimated time: **60–75 minutes**. The required work is a bandwidth budget. A camera on the desk is optional, and Chapter 07 does not wait for one.

## Learning objectives

You will compute uncompressed and MJPEG bandwidth for a stated width, height, and frame rate, and you will compare that number with what USB 2.0 actually delivers once it is shared. You will distinguish a UVC webcam (USB, the laptop is the host), a CSI camera (a ribbon that never enters the USB controller), and an ESP32-CAM (JPEG on a board that is a poor Capstone brain). You will write one sentence that defers the camera until perception work, and that sentence will contain the 147 Mbit/s figure so the checklist can see you did the arithmetic.

## Prerequisites

Lesson 04-02’s identification sheet already has a row for “USB plug versus flex cable versus two metal cans.” Chapter 02 is the ESP32 and the Pico, so you know which board is allowed to be the robot’s computer. You can multiply. You do not need OpenCV, a GPU, or a ROS image pipeline. If those words are new, leave them new until Chapter 11.

## Why this matters for Capstone A and the ROS path

Capstone A does not need a camera. Chapter 07’s firmware teleops two wheels from a serial command and stops on a timeout or a range reading. A USB video stream on that same laptop is a different project: it competes for USB bandwidth, for CPU, and for your week. Students who block the motor lab on a camera order finish neither.

When perception does start, the usual ROS 2 path is `usb_cam` or another V4L2 node publishing `sensor_msgs/Image` for raw pixels and `sensor_msgs/CompressedImage` for JPEG. The encoding field (`yuyv`, `rgb8`, `jpeg`) is the same choice as the byte-per-pixel term in the formula below. A CSI camera on a Pi never crosses that USB link, so it does not change the 147 Mbit/s sum, but it also does not plug into an ESP32. Write the deferral sentence now, with the number in it, and keep shopping for the rangefinder and the encoder motors.

![Which package is a camera: USB plug or flex, not the two cans]({{ site.imgurl }}/generated/sensor_package_id.png)

The figure is the identification sheet from Lesson 04-02. The camera row is the wide connector: a USB plug, or a flat flex into a large module. The two aluminum cans are the ultrasonic sensor from the previous lesson. The tiny window is ToF or an IMU, not a scene camera. If your sheet still calls every black rectangle a camera, fix the row before you read a bandwidth number as if it were a distance.

## Bytes per second, then megabits

Uncompressed image bandwidth is

$$
B \approx w \times h \times \mathrm{fps} \times (\text{bytes per pixel}).
$$

YUYV is a 4:2:2 format: two bytes per pixel, no JPEG. A 640×480 stream at 30 frames per second is

$$
B = 640 \times 480 \times 2 \times 30 = 18{,}432{,}000~\mathrm{bytes/s}.
$$

Times 8,

$$
18{,}432{,}000 \times 8 = 147{,}456{,}000~\mathrm{bit/s} \approx 147~\mathrm{Mbit/s}.
$$

USB 2.0’s theoretical ceiling is 480 Mbit/s. Shared with a serial adapter, a hub, and protocol overhead, practical video throughput is often closer to 280–300 Mbit/s. One raw 640×480 stream is already about half of that practical budget. A second raw stream does not fit. Video on USB is isochronous: a late packet is dropped, and you see a torn frame rather than a clean retry.

MJPEG at about 10:1 on that same frame is

$$
147 / 10 \approx 15~\mathrm{Mbit/s}.
$$

That sits comfortably beside a serial console. You pay the cost in decoder CPU on the host. RGB at three bytes per pixel is heavier than YUYV: $$640 \times 480 \times 3 \times 30 = 27{,}648{,}000$$ bytes/s, about 221 Mbit/s, which is a single stream already arguing with the rest of the bus.

## Three ways a robot “has a camera”

**USB UVC.** A webcam speaks USB Video Class. On a laptop, `lsusb` lists it, and a later V4L2 node opens `/dev/video0`. The host is the computer, not a GPIO. This is the sensible camera for Chapter 11 if the robot’s brain is a Pi or a PC and the ESP32 is only the motor board. It is the stream whose 147 Mbit/s you just computed, unless you ask the camera for MJPEG.

**CSI.** A Raspberry Pi camera rides a ribbon into the Pi’s CSI connector. Those pixels do not pass through the USB host controller, so they do not add to the 480 Mbit/s account. They also do not exist on an ESP32 DevKit or a Pico. A Pi camera bought “for the robot” while the robot’s only computer is an ESP32 is a camera with nowhere to plug in.

**ESP32-CAM, OV2640.** The module produces JPEG, which is why the wire-level bandwidth looks solved, and then the board itself becomes the problem. The camera claims a large set of pins, the onboard regulator browns out when the radio and the sensor peak together, and you still owe the chassis a motor driver. It can be a side experiment. It is an awkward brain for Capstone A. Do not replace the ESP32 devkit you already blink with this module in order to “be ready for vision.”

The ESP32 in the course photos is a devkit with USB for serial and free GPIO for TRIG, ECHO, and later PWM. It is not a CSI host. Treat it that way until a later chapter gives you a different computer.

## Lab: the budget is the assignment

### Safety

No motors. If you plug in a USB camera, use the laptop’s USB port, not a GPIO. Do not power an ESP32-CAM from the ESP32 devkit’s 3.3 V pin; the camera board wants its own 5 V and still browns out easily. Do not look for a laser in a webcam. This lab does not include the VL53L0X.

### BOM

| Item | Role |
|------|------|
| Paper or `lab-notes.md` | The required bandwidth worksheet |
| A USB webcam, if you already own one | Optional `lsusb` |
| Laptop | Host for that optional camera |
| ESP32-CAM | Not required, and not the Capstone brain |

### Steps

1. Compute $$640 \times 480 \times 2 \times 30$$ in bytes per second and in Mbit/s. You should land on 18,432,000 bytes/s and about 147 Mbit/s. Show the multiplication in the notes.
2. Divide by 10 for a rough MJPEG stream and write about 15 Mbit/s. State that USB 2.0 practical budget is about 280–300 Mbit/s, shared.
3. Decide, in one sentence, that the camera waits until Chapter 11. The sentence must include 147 Mbit/s. An example that passes: “Camera deferred until Chapter 11; one 640×480 YUYV stream is already about 147 Mbit/s.”
4. Optional, only if a camera is plugged in: run `lsusb` and write the line that appeared. If you can see the connector, say USB-A, micro-USB, or a CSI ribbon. If no camera is present, stop at step 3. That is a complete lab.
5. On the Lesson 04-02 ID sheet, point at the camera row and write the connector type you would actually buy later, or “none yet.”

### Expected results

The three numbers (18,432,000 bytes/s, 147 Mbit/s, ~15 Mbit/s MJPEG) and the deferral sentence are in `lab-notes.md`. A missing camera is not a missing lab. A purchased ESP32-CAM is not extra credit toward Chapter 07.

### Faults

| What you see | What it usually is |
|--------------|--------------------|
| Bandwidth written as 18 million bits | You forgot the ×8 from bytes to bits |
| “USB 2.0 is 480, so two raw streams fit” | You used the theoretical ceiling, not ~300 Mbit/s shared |
| Torn frames once the serial adapter is on the same hub | The practical budget was already tight |
| Pi camera and an ESP32, nothing on `/dev/video` | CSI does not plug into that devkit |
| Chapter 07 blocked on a camera shipment | This lesson’s decision was ignored |

## Mua ở Việt Nam / Where to buy in Vietnam

Do not buy a camera to finish Chapter 04 or to start Chapter 07. If you already know you want one for Chapter 11, a plain UVC webcam is the boring correct purchase. Prices move.

| Part | Keywords | Rough band (VND) | Substitute |
|------|----------|------------------|------------|
| USB webcam | `camera usb robot` | 80.000–200.000 | Any UVC camera the laptop already sees. Resolution claims above 720p do not change the Capstone plan. |
| ESP32-CAM | `ESP32-CAM` | 70.000–140.000 | Optional side board only. Not a substitute for the devkit that drives the motors. |

- [Hshop: camera USB](https://hshop.vn/search?q=camera%20usb)
- [Shopee: camera usb robot](https://shopee.vn/search?keyword=camera%20usb%20robot)
- [Lazada: ESP32-CAM](https://www.lazada.vn/catalog/?q=ESP32-CAM)
- [Thế Giới IC: ESP32-CAM](https://www.thegioiic.com/search?q=ESP32-CAM)

## Exercises

1. Compute the byte rate and the bit rate of 640×480 YUYV at 30 fps.
2. The same frames as MJPEG at about 10:1. Does ~15 Mbit/s fit on a practical 300 Mbit/s USB 2.0 bus that is also carrying a 12 Mbit/s serial link? Does a second raw 147 Mbit/s stream fit beside the first?
3. A smaller mode is 320×240, RGB (3 bytes/pixel), 15 fps. What is $$B$$ in Mbit/s, and how does it compare with the 147 Mbit/s stream?
4. Why does a Pi CSI camera not reduce the USB budget, and why is an ESP32-CAM still a poor Chapter 07 brain even though its JPEG is small?
5. Write the one-sentence camera decision the Chapter 04 checklist will look for. Include the 147 Mbit/s figure.

### Answer guidance

1. $$18{,}432{,}000$$ bytes/s, which is $$147.5~\mathrm{Mbit/s}$$ (about 147). 2. $$15 + 12$$ fits easily. Two raw streams are about 295 Mbit/s before the serial link, which does not fit in a 280–300 Mbit/s practical budget. 3. $$320 \times 240 \times 3 \times 15 = 3{,}456{,}000$$ bytes/s $$\approx 27.6~\mathrm{Mbit/s}$$, about one fifth of the 640×480 YUYV stream. 4. CSI never enters the USB host, so the USB sum is unchanged, and a Pi ribbon has no socket on an ESP32. ESP32-CAM JPEG is small and the board still spends pins and regulator current the motor brain needs. 5. Any sentence that defers the camera until Chapter 11 and states that 640×480 YUYV at 30 fps is about 147 Mbit/s.

## Further reading

- [V4L2 YUYV pixel format](https://www.kernel.org/doc/html/latest/userspace-api/media/v4l/pixfmt-yuyv.html) — two bytes per pixel, the 2 in the formula.
- [`usb_cam` on ROS 2](https://index.ros.org/p/usb_cam/) — the usual node behind a UVC webcam, publishing images rather than distances.
- [`sensor_msgs/Image`](https://docs.ros.org/en/humble/p/sensor_msgs/msg/Image.html) and [`sensor_msgs/CompressedImage`](https://docs.ros.org/en/humble/p/sensor_msgs/msg/CompressedImage.html) — raw versus JPEG, which is the 147 versus 15 choice.
- [Raspberry Pi camera documentation](https://www.raspberrypi.com/documentation/accessories/camera.html) — CSI ribbons, and why they are not an ESP32 peripheral.
- [Espressif `esp32-camera` component](https://components.espressif.com/components/espressif/esp32-camera) — what the OV2640 path actually involves if you ever do use an ESP32-CAM on purpose.
