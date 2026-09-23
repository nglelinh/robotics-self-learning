---
layout: post
title: "Bridging Capstone A firmware to ROS 2"
chapter: "10"
order: 4
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter10
lesson_type: required
draft: false
---

Estimated time: **~90 minutes**.

## Learning objectives

You will run an `rclpy` node that subscribes to `/cmd_vel`, converts `linear.x` and `angular.z` into left and right tread speeds with track $$L = 0.16$$ m, and maps those speeds onto the Chapter 08 integers. You will document the scale in one place, 0.5 m/s of tread to the integer 100, and you will show that a straight 0.2 m/s command becomes the payload `V,40,40`. You will write that payload as the length-delimited frame `STX 0xAA`, length, ASCII payload, XOR, `0x0A`, and you will force `V,0,0` onto the wire when no Twist has arrived for 0.3 s. You will prove the node with a `socat` PTY pair and a tiny parser, so the lab does not need a robot. You will state what still stops the motors if the bridge process itself is killed, and you will keep the wheels off the ground if a real driver is connected.

## Prerequisites

Lesson 08-01’s frame and 300 ms firmware timeout, lesson 08-04’s inverse kinematics, and a Jazzy shell with `rclpy`. Python package `pyserial` comes from apt as `python3-serial`, so it stays on the same interpreter as ROS. `socat` provides the fake serial port. You do not need Gazebo running, and you should not have the micro-ROS serial agent holding a port. The real Capstone is optional and comes last, wheels up.

## Why this sits on the path

This node is the first time the ROS graph and the Capstone firmware share a command. Simulation already listens to `/cmd_vel`. Nav2, and a learned policy later, should publish that same type. Neither knows what `0xAA` means, and the current ESP32 firmware does not know what a Twist is. The bridge is the only place where metres per second become the −100…100 integers. micro-ROS is allowed only after this file works: same topic names, same scale, same watchdog, with a parser log as evidence.

![Twist in, Chapter 08 frame out, telemetry back]({{ site.imgurl }}/generated/ch10_serial_bridge.png)

## Concepts

`geometry_msgs/Twist` carries a linear vector and an angular vector. A differential-drive base honours two of those six numbers. Forward speed $$v$$ is `linear.x`, in metres per second. Yaw rate $$\omega$$ is `angular.z`, in radians per second, positive for a left turn under REP-103. `linear.y` would be a sideways slide. The mechanism cannot do that, so the callback ignores `linear.y` instead of secretly mixing it into the wheels.

The inverse map from lesson 08-04, with track $$L$$ in metres:

$$
v_R = v + \omega \frac{L}{2}, \qquad v_L = v - \omega \frac{L}{2}
$$

The course base uses $$L = 0.16$$, so $$L/2 = 0.08$$. $$v_L$$ and $$v_R$$ are tread speeds in metres per second, positive forward. They are not PWM, and they are not the integers on the wire.

The wire is still the Chapter 08 integer, −100…100. One scale constant joins the two worlds. This lesson defines full scale as 0.5 m/s of tread:

$$
n = \mathrm{clip}\left(\mathrm{round}\left(v_{\mathrm{wheel}} \cdot \frac{100}{0.5}\right), -100, 100\right)
$$

So 0.5 m/s becomes 100, and 0.2 m/s becomes 40. The constant 0.5 is a choice written at the top of the file. If the Chapter 07 spin test showed a different tread speed at integer 100, change the constant and the comment together, on both sides. Casting metres to `int` before scaling is a different bug: `int(0.2)` is 0, and the robot sits still while the topic looks correct.

The payload is ASCII, `V,{left},{right}`, left wheel first. The frame around it is unchanged: byte `0xAA`, one length byte equal to the payload length, the payload, one XOR of every payload byte, and `0x0A`.

$$
c = b_0 \oplus b_1 \oplus \cdots \oplus b_{n-1}
$$

The bridge repeats the latest frame about 20 times a second. The firmware timeout is 300 ms without a good frame, so a single frame followed by silence would stop the board even while ROS still wanted motion. A second timer inside the bridge watches the Twist. If none arrives for 0.3 s, the repeated command becomes `V,0,0`.

You need both stops. If teleop dies and the bridge stays up, the bridge sends the zeros. If the bridge dies or the USB cable leaves, the firmware watchdog is the only stop left, and only if the firmware implements it. A `finally` block does not run when the process is killed or the cable is pulled. Test the quiet publisher, and do not claim you tested the killed process.

Telemetry may come back as text. The node publishes it as `std_msgs/String` on `/capstone_telem` when bytes arrive, and otherwise just logs. Do not block the 20 Hz tick waiting for a line. The dry-run parser does not answer, so the evidence is the parser’s `OK` line.

Save the node as `capstone_bridge.py`. Parameters are `port` and `baud`, as in the Jazzy parameter guide. The dry run points `port` at a PTY. The real board uses `/dev/ttyUSB0` after your user is in group `dialout`. Leave `use_sim_time` unset so the 0.3 s check uses the wall clock. Sim time without a `/clock` freezes that check.

```python
#!/usr/bin/env python3
"""Capstone A bridge: Twist in, chapter 08 frame out.

Scale: 0.5 m/s of tread speed -> integer 100. Track L = 0.16 m.
No Twist for 0.3 s -> V,0,0 on the wire. Firmware watchdog is the
backup if this process dies.
"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import String
import serial

TRACK_M = 0.16
FULL_SCALE_MPS = 0.5
WATCHDOG_S = 0.3


def frame(left: int, right: int) -> bytes:
    payload = f"V,{left},{right}".encode("ascii")
    xor_byte = 0
    for b in payload:
        xor_byte ^= b
    return bytes([0xAA, len(payload)]) + payload + bytes([xor_byte, 0x0A])


def wheel_ints(v: float, w: float) -> tuple[int, int]:
    half = TRACK_M / 2.0
    v_l = v - w * half
    v_r = v + w * half

    def to_int(speed: float) -> int:
        n = int(round(speed / FULL_SCALE_MPS * 100.0))
        return max(-100, min(100, n))

    return to_int(v_l), to_int(v_r)


class CapstoneBridge(Node):
    def __init__(self) -> None:
        super().__init__("capstone_bridge")
        self.declare_parameter("port", "/dev/ttyUSB0")
        self.declare_parameter("baud", 115200)
        port = self.get_parameter("port").get_parameter_value().string_value
        baud = self.get_parameter("baud").get_parameter_value().integer_value
        self.ser = serial.Serial(port, baud, timeout=0.0)
        self.left = 0
        self.right = 0
        self.last_twist = self.get_clock().now()
        self.last_logged = (0, 0)
        self.create_subscription(Twist, "cmd_vel", self.on_twist, 10)
        self.telem = self.create_publisher(String, "capstone_telem", 10)
        self.create_timer(0.05, self.tick)

    def on_twist(self, msg: Twist) -> None:
        self.left, self.right = wheel_ints(msg.linear.x, msg.angular.z)
        self.last_twist = self.get_clock().now()

    def tick(self) -> None:
        age = (self.get_clock().now() - self.last_twist).nanoseconds * 1e-9
        if age > WATCHDOG_S:
            self.left, self.right = 0, 0
        self.ser.write(frame(self.left, self.right))
        if (self.left, self.right) != self.last_logged:
            self.get_logger().info(f"wire V,{self.left},{self.right}")
            self.last_logged = (self.left, self.right)
        raw = self.ser.read(128)
        if not raw:
            return
        text = raw.decode("ascii", errors="replace").strip()
        if text:
            self.telem.publish(String(data=text))


def main() -> None:
    rclpy.init()
    node = CapstoneBridge()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        try:
            node.ser.write(frame(0, 0))
        except Exception:
            pass
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
```

A straight command does not catch a left/right swap, because both integers match. Positive `angular.z` must produce a larger right integer than left. That is the sign check in the lab.

## Worked example

Straight, $$v = 0.2$$, $$\omega = 0$$, $$L = 0.16$$:

$$
v_L = v_R = 0.2
$$

$$
n = \mathrm{round}\left(0.2 \cdot \frac{100}{0.5}\right) = 40
$$

Payload `V,40,40`. A mild left turn, $$v = 0$$, $$\omega = +0.5$$:

$$
v_L = -0.5 \times 0.08 = -0.04, \qquad v_R = 0.04
$$

$$
n_L = \mathrm{round}(-0.04 \times 200) = -8, \qquad n_R = 8
$$

Payload `V,-8,8`. If the parser shows `V,8,-8`, the return order in `wheel_ints` is backwards and the robot will turn the wrong way on the floor.

The dry-run wiring is a pair of pseudo-terminals:

```bash
sudo apt install socat python3-serial
socat -d -d pty,raw,echo=0 pty,raw,echo=0
```

`socat` prints two paths, for example `/dev/pts/3` and `/dev/pts/4`. The bridge parameter `port` is one of them. A parser adapted from lesson 08-01 listens on the other. Save it as `pty_parser.py`:

```python
import serial, sys
ser = serial.Serial(sys.argv[1], 115200, timeout=0.2)
buf = bytearray()

def xor_of(data: bytes) -> int:
    x = 0
    for b in data:
        x ^= b
    return x

while True:
    buf += ser.read(64)
    while buf:
        if buf[0] != 0xAA:
            del buf[0]
            continue
        if len(buf) < 2:
            break
        n = buf[1]
        if n > 32:
            del buf[0]
            continue
        if len(buf) < 4 + n:
            break
        payload, check, end = bytes(buf[2:2+n]), buf[2+n], buf[3+n]
        del buf[:4+n]
        if end != 0x0A or check != xor_of(payload):
            print("DROP", payload)
            continue
        print("OK", payload.decode())
```

```bash
python3 pty_parser.py /dev/pts/4
```

```bash
source /opt/ros/jazzy/setup.bash
python3 capstone_bridge.py --ros-args -p port:=/dev/pts/3
```

Then, from a fourth shell:

```bash
source /opt/ros/jazzy/setup.bash
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 0.2, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"
```

The parser should print `OK V,40,40` several times, about 20 Hz, and within a second of silence it should print `OK V,0,0`. The bridge log should show the same two strings when the integers change. That pair is the lab.

## Lab

1. Install `socat` and `python3-serial`. Source Jazzy. Confirm `printenv ROS_DISTRO` is `jazzy`.
2. Start `socat` as in the worked example. Write down both PTY paths. Leave `socat` running.
3. Start `pty_parser.py` on the second path.
4. Start `capstone_bridge.py` with `-p port:=` set to the first path. The node must stay up. A traceback on open means you swapped the paths or `socat` has exited.
5. Publish one Twist with `linear.x` 0.2 and `angular.z` 0, using the command above. Watch the parser.
6. Wait about a second without publishing again. The parser must move from `V,40,40` to `V,0,0` even though the bridge process is still running.
7. Publish `angular.z` 0.5 with `linear.x` 0. Confirm `OK V,-8,8`. If you see `V,8,-8`, fix `wheel_ints` before any real motor turns.
8. Only if a Capstone is on the bench: wheels off the ground, driver powered from the robot pack, USB only for serial. Add your user to `dialout` if `python3` cannot open `/dev/ttyUSB0`, then log out and back in. Run the same node with `-p port:=/dev/ttyUSB0`. Both wheels must nudge forward for the straight command and go quiet after you stop publishing. Unplug is a separate test you do once, with the wheels up: pull USB and confirm the firmware, not the bridge, is what zeros the PWM.

**Expected**

After the straight publish, the parser prints:

```text
OK V,40,40
```

About a second after that publisher goes quiet, still with the bridge alive:

```text
OK V,0,0
```

The yaw check prints `OK V,-8,8`. On a real board, both wheels turn forward for well under a second and then stop. They must not keep spinning after the publisher has stopped.

**Failure modes**

| What you see | Likely cause |
| --- | --- |
| `OK V,8,-8` on a positive yaw | Left and right are swapped in `wheel_ints` or in the payload order |
| `OK V,0,0` during the 0.2 m/s command, or `V,20,20` | Metres were cast to int, or full scale is 1.0 m/s instead of 0.5 m/s |
| Parser stays on `V,40,40` after you stop publishing | The bridge watchdog is not in the tick that writes the frame; the firmware would also keep going if its own timeout is missing |
| Wheels run on after you kill the bridge | The firmware watchdog is the only remaining stop, and it is not implemented or is much slower than 300 ms |
| `Permission denied` on `/dev/ttyUSB0` | The user is not in group `dialout`, or the login session predates the group change |
| Parser prints nothing, bridge is up | The two programs are on the same PTY, or `socat` was started without `echo=0` and a second reader stole the bytes |

## Where to buy this in Vietnam

No new parts. The dry run is `socat` and Python. The hardware version uses the Capstone and the USB cable you already have. Search [hshop.vn](https://hshop.vn/) for “ESP32” only if that board has died. A replacement DevKit on Shopee is `ESP32 DevKit V1 30 chân`, 2026 band about 80.000–180.000 VND, recheck before paying. Do not power the motors from that USB cable.

## Exercises

1. Compute the wire integers for $$v = 0.2$$ m/s and $$\omega = 0.5$$ rad/s with $$L = 0.16$$ and the 0.5 m/s scale. Guidance: left tread 0.16 m/s becomes 32, right tread 0.24 m/s becomes 48, so the payload is `V,32,48`.
2. The publisher stops, the bridge process stays up, and one second passes. What payload is on the wire, and which timer put it there? Guidance: `V,0,0` from the bridge’s 0.3 s Twist watchdog, not from the firmware, because frames are still arriving.
3. The bridge process is killed with the motors armed and the wheels up. What stops them, and on what deadline? Guidance: the Chapter 08 firmware watchdog, about 300 ms after the last good frame, because the bridge’s `finally` block does not run.
4. `ls -l /dev/ttyUSB0` shows group `dialout` and Python raises `Permission denied`. What do you change, and why is a new login required? Guidance: add your user to `dialout`; group membership is applied at login, so a new shell in the old session is not enough.
5. A Twist arrives with `linear.y = 0.3` and `linear.x = 0`. What integers do you send, and which component did you ignore? Guidance: send zeros from $$v$$ and $$\omega$$ only; `linear.y` is a sideslip the diff-drive cannot produce.

## Further reading

- [Jazzy parameters](https://docs.ros.org/en/jazzy/How-To-Guides/Using-ros2-param.html) is the interface behind `-p port:=` and `declare_parameter`.
- [REP-103](https://www.ros.org/reps/rep-0103.html) fixes the sign of `angular.z` that `wheel_ints` implements.
- [REP-105](https://www.ros.org/reps/rep-0105.html) is the frame naming you keep when this same Twist is used in simulation and on the bridge.
- [micro-ROS](https://micro.ros.org/) is the later transport. Come back to it only after this parser shows `OK V,40,40` and the watchdog line.
