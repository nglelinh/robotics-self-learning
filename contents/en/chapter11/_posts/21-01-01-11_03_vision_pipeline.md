---
layout: post
title: "Basic vision pipeline for robots"
chapter: "11"
order: 3
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter11
lesson_type: required
draft: false
---

Estimated time: about 75 minutes when a USB camera enumerates as `/dev/video0`, and about 45 minutes when you document a missing device and still walk the pipeline on paper.

## Learning objectives

You can order the pipeline as light, then camera, then algorithm, and you will not retune thresholds while a window blows out the card. You can say what `usb_cam` publishes, compute a centroid, act once at 5 to 10 Hz instead of every frame, state how an optical frame differs from `camera_link` under REP-103, and record a missing `/dev/video0` as a result rather than a broken lab.

## Prerequisites

You can run a short Python script and you know that an image is an array. You have met `geometry_msgs/msg/Twist` in the Nav2 tour, so you know a velocity command has a linear part and an angular part. You do not need a depth camera, and this lesson never asks for a RealSense.

## Why this lesson sits on the path

The path is the Capstone base, then ROS 2 Jazzy, then Gazebo, then autonomy. The base already bridges `cmd_vel` to PWM. Jazzy is how a camera would publish `sensor_msgs/msg/Image` beside the lidar topics. A colored card on the desk shows thresholding fail in real light faster than a simulated camera. The autonomous act here is modest: yaw toward the card, or stop. That is the same Twist Nav2 publishes. A loop at 30 Hz fights the bridge. A loop at 5 to 10 Hz can share the robot with a later navigator.

## Concepts

Start with the light. A red card under a bare bulb and the same card in afternoon sun are different measurements. If your eyes cannot see a distinct patch, OpenCV will not save the demo. Move the lamp or kill the backlight before you edit hue limits. The camera comes second: a USB UVC device, often `/dev/video0`. `usb_cam` or `v4l2_camera` publishes `sensor_msgs/msg/Image`. The algorithm comes third, and here it is a color threshold plus a centroid, not a neural detector.

![A camera image becomes a threshold mask, then a centroid that can drive one slow yaw command]({{ site.imgurl }}/generated/ch11_vision.png)

On a Jazzy machine with the binary installed, the driver shape is:

```bash
sudo apt install ros-jazzy-usb-cam
source /opt/ros/jazzy/setup.bash
ros2 run usb_cam usb_cam_node_exe
```

`ros2 launch usb_cam camera.launch.py` adds a viewer. The image topic is commonly `/image_raw` of type `sensor_msgs/msg/Image`. If it is silent, fix the device path before any threshold. The lab does not require this node. It uses OpenCV directly.

HSV thresholding is more stable than a raw red channel, and still fragile. Freeze one lower bound, one upper bound, and the lighting you used. The mask is white on the card. Moments turn it into a centroid. For pixels $$(x_i, y_i)$$,

$$
c_x = \frac{\sum_i x_i}{N}, \qquad c_y = \frac{\sum_i y_i}{N},
$$

which is what `cv2.moments` computes when it divides `m10` by `m00` and `m01` by `m00`. Work a three-pixel mask by hand: white pixels at $$(100, 80)$$, $$(102, 80)$$, and $$(101, 82)$$. Then

$$
c_x = \frac{100 + 102 + 101}{3} = 101, \qquad c_y = \frac{80 + 80 + 82}{3} \approx 80.67.
$$

If the image is 320 pixels wide, the horizontal center is 160. The blob sits left of center. A forward-facing camera sees that as "target on the left," so a differential-drive base should yaw left, which is a positive `angular.z` in REP-103, until the centroid walks toward the center. If the area `m00` is tiny, there is no card. Publish nothing, or publish a zero twist, rather than chasing noise.

Act slowly. A camera may deliver 30 frames a second. The motors should not get 30 new twists. Decide at 5 to 10 Hz, emit one Twist or a stop, and hold it. Full frame rate chatters a gearbox.

[REP-103](https://www.ros.org/reps/rep-0103.html) gives the body `x` forward, `y` left, `z` up. An optical frame is different: `z` out of the lens, `x` right in the image, `y` down in the image. `camera_link` is usually a body-style mount. `camera_optical_frame` is what should be stamped on the image. The usual fixed joint from a body-style `camera_link` uses roll $$-\pi/2$$ and yaw $$-\pi/2$$. Read the joint in your URDF anyway. A pixel centroid is not a point in `base_link` until that rotation and a camera model exist. This lesson does not require the projection. Yaw toward the pixel.

## Worked example

The following script is the whole algorithm without ROS. It opens the first camera, thresholds a broad orange band in HSV, and prints one centroid. Orange is only an example. If your card is blue, change the bounds and write the new numbers in your notes. Run it from a directory where you can see the terminal:

```bash
python3 card_centroid.py
```

```python
import sys
import cv2
import numpy as np

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("error: cannot open /dev/video0")
    sys.exit(1)

ok, frame = cap.read()
cap.release()
if not ok:
    print("error: camera opened but read failed")
    sys.exit(1)

hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
lower = np.array([5, 120, 80])
upper = np.array([25, 255, 255])
mask = cv2.inRange(hsv, lower, upper)
moments = cv2.moments(mask)
area = moments["m00"]
if area < 500:
    print("centroid none area=0")
else:
    u = int(moments["m10"] / area)
    v = int(moments["m01"] / area)
    print(f"centroid u={u} v={v} area={int(area)}")
```

Hold an orange card in front of the lens under a steady lamp. A healthy print looks like:

```text
centroid u=312 v=248 area=1840
```

Your integers will differ. `u` grows as the card moves right. `area` grows as it comes closer. `centroid none area=0` means the bounds miss this lamp: change the light, then the bounds. `error: cannot open /dev/video0` is a valid lab line. Record it. Do not invent a centroid.

A later ROS node decides at 5 or 10 Hz. If `area` is below 500, publish a zero Twist. If `u` is left of center, publish `angular.z` near 0.3. If `u` is right of center, publish `angular.z` near -0.3. Hold that command until the next tick. Enough to twitch the bridge toward a card. Not a navigator.

## Lab

Save the script as `card_centroid.py` and run it. Pick the expected output that matches the machine you actually have.

If a camera is present and the card is in view, the expected line matches this pattern, with your own integers:

```text
centroid u=312 v=248 area=1840
```

If the camera is present and the mask is empty, the expected line is:

```text
centroid none area=0
```

If no camera enumerates, the expected line is:

```text
error: cannot open /dev/video0
```

If the device is missing, also paste the complaint from `ls /dev/video*`. Then write four sentences: light, device, threshold, centroid, and why Twist is not published at frame rate.

| What you see | Likely cause | What to check |
| --- | --- | --- |
| `error: cannot open /dev/video0` | No UVC device, or the cable is charge-only | `ls /dev/video*` and a different port |
| Camera opens, `centroid none` forever | Hue bounds fight the lamp, or the card is out of frame | Look at the card with your eyes, then the bounds |
| Centroid jitters by tens of pixels on a still card | Mixed sun and indoor light, or a tiny mask | One lamp, raise the area cutoff |
| Wheels buzz when you later connect Twist | You published at frame rate | Timer at 5 to 10 Hz, one command per tick |
| Card moves right in the world but `u` moves left | Image is mirrored, or you swapped the yaw sign | Trust `u` increasing to the right in the array |
| You tried to aim with `camera_link` axes | Optical `y` is down, body `z` is up | REP-103 optical versus body |

## Buying a camera in Vietnam

A depth camera is out of scope. Search Shopee for `camera USB UVC`. Ordinary webcams have recently been about 150 to 450 thousand VND. Recheck, and avoid charge-only cables.

An IMX219-class Pi camera is the other common choice, often a few hundred thousand dong. A Waveshare IMX219-77 has been listed near 432.000 VND. Recheck the current page before you order. Either camera can feed the script or a ROS image topic. Neither has to be a RealSense.

## Exercises

### Exercise 1

The card vanishes from the mask whenever a window opens, and it returns when you close the curtain, with the same hue numbers. Which stage do you debug, and which stage do you leave alone?

**Guidance.** Light is first. Do not rewrite the moment formula. Say what you would change in the room.

### Exercise 2

A mask has white pixels only at $$(10, 10)$$, $$(14, 10)$$, $$(12, 16)$$, and $$(12, 12)$$. Compute $$c_x$$ and $$c_y$$. The image width is 64. Is the blob left or right of center?

**Guidance.** Average the four `x` values and the four `y` values. Center is 32. Compare $$c_x$$ to 32.

### Exercise 3

Your camera publishes 30 images each second. Explain why the bridge should see a new Twist only 5 to 10 times each second, using the Capstone motors as the reason.

**Guidance.** Talk about chatter and about sharing `cmd_vel` with a later navigator. One sentence on a timer is enough.

### Exercise 4

State the three axis directions of an optical frame, and the three axis directions of a REP-103 body frame. Say which frame should be stamped on the image.

**Guidance.** Optical: `z` out of the lens, `x` right, `y` down. Body: `x` forward, `y` left, `z` up. The image uses the optical frame.

### Exercise 5

The script prints `error: cannot open /dev/video0`. List three checks that teach you something without buying a camera, and state what you still owe in writing.

**Guidance.** `ls` the device directory, try another USB port, record the exact error. You still owe the four-sentence pipeline note from the lab.

## Further reading

- The OpenCV [thresholding tutorial](https://docs.opencv.org/4.x/d7/d4d/tutorial_py_thresholding.html) is the reference for `inRange` style segmentation and for looking at a mask before you trust a centroid.
- [usb_cam](https://github.com/ros-drivers/usb_cam) documents `usb_cam_node_exe` and `camera.launch.py` for a V4L2 camera on ROS 2.
- [REP-103](https://www.ros.org/reps/rep-0103.html) is the standard that separates body axes from the optical frame used on images.
