---
layout: post
title: "Serial protocols beyond println"
chapter: "08"
order: 1
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter08
lesson_type: required
draft: false
---

Estimated time: **~90 minutes**.

## Learning objectives

By the end of this lesson you can design a small wheel-command frame that survives a split USB read, implement it on the host in Python and on an ESP32 or Pico, and explain why a bare `println` of `"40,-15"` is not a protocol. You will compute a one-byte XOR check, name the timeout that must zero the motors, and record one captured frame plus one deliberate failure in `lab-notes.md`. That skill is the contract Chapter 10’s ROS 2 bridge will reuse, so `cmd_vel` never becomes “whatever bytes happened to be in the buffer.”

## Prerequisites

You can blink an LED and print a line from Chapter 02, and you have a Capstone A teleop sketch from Chapter 07, even if it still sends raw text. You know a byte is 8 bits and that `115200 8N1` means 115200 bits per second, 8 data bits, no parity, one stop bit. A laptop with Python 3 is enough for the dry run. An ESP32 or Pico is the hardware version of the same lab.

## Why this sits on the path

Chapter 07 proved the robot can move when you type on a serial line. Chapter 08 turns that line into something a program can trust. Chapter 09 will introduce ROS 2 topics, which are also framed messages with types. Chapter 10’s bridge node is only a translator: `geometry_msgs/Twist` in, this frame out. If the frame is ambiguous, every later stack (Nav2, a vision loop, a learned policy) inherits a robot that lunges when a byte is lost. Robot learning in Chapter 12 assumes the low-level command channel already fails safe.

![Serial frame fields]({{ site.imgurl }}/generated/ch08_serial_frame.png)

## Concepts

A UART moves bytes, not messages. The USB-serial chip delivers whatever has arrived, which may be half a line, two lines, or a fragment left over from the previous read. `Serial.println("40,-15")` looks fine in the Arduino Serial Monitor because the monitor waits for a newline and then shows you text. A parser in a tight loop does not get that courtesy. It must answer three questions: where does a message start, how long is it, and did it arrive intact?

Two framings are enough for this course. A **delimiter frame** ends on `\n` (byte `0x0A`) and is easy to read in a terminal. A **length frame** starts with a marker, then a count, then that many payload bytes, then a check. Length framing still works when the payload itself contains a newline or a comma. The Capstone bridge in Chapter 10 will speak the length frame. Keep the delimiter form as a debug view you can type by hand.

The text payload stays human-readable:

```text
V,40,-15
```

`V` means “velocity command,” `40` is the left wheel in the same −100…100 units as Chapter 07, and `-15` is the right wheel. Units belong in the comment at the top of both programs. Do not silently switch one side to metres per second.

The check in this lesson is an XOR of every payload byte, stored in one byte. It catches many single-bit errors and most truncated frames. It is not a security feature. A CRC would be the next step if you ever leave the lab bench; you do not need it to learn the state machine.

$$
c = b_0 \oplus b_1 \oplus \cdots \oplus b_{n-1}
$$

The wire image is `STX | LEN | payload | c | END`, with `STX = 0xAA` and `END = 0x0A`. `LEN` is the payload length, not the length of the whole frame. Reject `LEN` above 32 so a corrupted length cannot make you allocate a huge buffer on a microcontroller.

The receiver is a small state machine: hunt for `0xAA`, read `LEN`, read `LEN` bytes, read the check byte, read the end byte, compare the XOR, then apply the command. Any surprise returns to “hunt.” If no complete good frame arrives for 300 ms, the applied wheel command becomes `0,0`. That timeout is the safety property. A pretty parser without it will replay the last command forever when the USB cable falls out.

## Worked example

Build a frame for left = 40 and right = −15.

```python
def frame(left: int, right: int) -> bytes:
    if not (-100 <= left <= 100 and -100 <= right <= 100):
        raise ValueError("wheel command out of range")
    payload = f"V,{left},{right}".encode("ascii")
    xor = 0
    for b in payload:
        xor ^= b
    return bytes([0xAA, len(payload)]) + payload + bytes([xor, 0x0A])

raw = frame(40, -15)
print(raw.hex(" "))
print("payload", raw[2:-2])
```

You should see a line that starts with `aa` and ends with `0a`, and a payload that decodes to `V,40,-15`. Re-run with `frame(40, -15)` twice: the hex must be identical. Change the right wheel to `-16` and only the payload and the XOR byte should change. If you flip one payload byte by hand and recompute the XOR, the original check byte must no longer match. That is the test you will automate in the exercises.

On the microcontroller, do not use `delay()` while you wait for bytes. Append whatever `read()` returns into a small buffer and run the state machine once per loop. Chapter 08-05 measures that loop. For this lesson, correctness of the frame matters more than the rate.

Host side, with `pyserial`:

```python
import serial, time
ser = serial.Serial("/dev/ttyUSB0", 115200, timeout=0.05)

def send(left: int, right: int) -> None:
    ser.write(frame(left, right))
    ser.flush()

send(20, 20)
time.sleep(0.5)
send(0, 0)
```

Replace the port with the `socat` PTY from the lab when the robot is not on the bench. Wheels stay off the ground whenever a real motor driver is connected.

## Lab

Dry run, no robot required.

```bash
python3 -m pip install pyserial
socat -d -d pty,raw,echo=0 pty,raw,echo=0
```

`socat` prints two device names, for example `/dev/pts/3` and `/dev/pts/4`. Point the sender at one and the parser at the other. Parser sketch:

```python
import serial
ser = serial.Serial("/dev/pts/4", 115200, timeout=0.05)
buf = bytearray()

def xor_of(data: bytes) -> int:
    x = 0
    for b in data:
        x ^= b
    return x

while True:
    buf += ser.read(64)
    while True:
        if not buf:
            break
        if buf[0] != 0xAA:
            del buf[0]
            continue
        if len(buf) < 2:
            break
        n = buf[1]
        if n > 32:
            del buf[0]
            continue
        if len(buf) < 2 + n + 2:
            break
        payload, check, end = bytes(buf[2:2+n]), buf[2+n], buf[3+n]
        del buf[:4+n]
        if end != 0x0A or check != xor_of(payload):
            print("DROP", payload, hex(check))
            continue
        print("OK", payload.decode())
```

**Expected output** after `send(40, -15)` from the other PTY:

```text
OK b'V,40,-15' decoded as V,40,-15
```

Send ten frames in a loop. You should see ten `OK` lines and zero `DROP` lines. Then corrupt one frame by writing `b"\xAA\x05V,40"` with no check: the parser must not print `OK`. Unplug is simulated by simply stopping the sender: your firmware notes should say the last command expires. On a real board, confirm with a serial log that both PWM pins go inactive within about 300 ms.

**Failure modes**

| What you see | Likely cause |
| --- | --- |
| Endless garbage, no `OK` | Baud mismatch, often 9600 vs 115200, or you opened the same PTY twice |
| `OK` never arrives, buffer grows | `LEN` does not match the payload you actually sent |
| Motors run after the cable is pulled | Timeout not implemented; last command latched |
| Works in Serial Monitor, fails in Python | Monitor adds a newline; your script forgot `END` or `flush` |
| ESP32 resets when motors start | Motors powered from USB. Use the Chapter 07 pack and a common ground |

## Where to buy this in Vietnam

The dry run needs only a laptop. The hardware version uses the same board as Capstone A.

| Item | Shop | Search on Shopee or Lazada | 2026 band, check before paying |
| --- | --- | --- | --- |
| ESP32 DevKit V1 (30-pin, WROOM-32) | Search “ESP32” on [hshop.vn](https://hshop.vn/) | `ESP32 DevKit V1 30 chân` | about 80.000–180.000 VND |
| USB-TTL CP2102 or CH340, 3.3 V | same | `CP2102 USB TTL 3.3V` | about 25.000–60.000 VND |
| Pico or Pico W, if you stay on MicroPython | [hshop.vn](https://hshop.vn/) search “Raspberry Pi Pico” | `Raspberry Pi Pico` | about 120.000–250.000 VND |

A 5 V USB-TTL module must still speak 3.3 V logic into an ESP32 RX pin. Power the motors from the robot pack, not from the laptop USB port. Prices move; the band is a budget check, not a quote.

## Exercises

1. Compute the XOR of the ASCII bytes in `V,0,0` by hand, then confirm with the `frame()` function. Guidance: XOR is commutative, so order of bytes does not matter, and the result is a single byte in `0x00`–`0xFF`.
2. Explain, in three sentences, a case where a newline-delimited parser accepts a command the length-frame parser rejects. Guidance: a payload that contains an embedded `\n`, or a second command glued on before you finish the first, is the situation to describe.
3. Your log shows `OK V,40,-15` then 2 seconds of silence while the wheels keep spinning. What line is missing in the firmware? Guidance: a timestamp of the last good frame and a comparison with `millis()`.
4. Change the protocol so a command outside −100…100 is dropped rather than clamped. Which side should enforce that, host or MCU? Guidance: the MCU must enforce it. The host check is only a convenience.
5. Write the sentence you will put in the Chapter 10 bridge comments: units on the wire, units in ROS, and the timeout. Guidance: ROS side is m/s and rad/s later; this wire is still −100…100 until that lesson converts them in one function.

## Further reading

- [pyserial documentation](https://pyserial.readthedocs.io/en/latest/shortintro.html) for ports, timeouts, and `flush`.
- [Arduino Serial reference](https://www.arduino.cc/reference/en/language/functions/communication/serial/) if your Capstone firmware is C++ rather than MicroPython.
- [REP-103](https://www.ros.org/reps/rep-0103.html) for the axis directions you will eventually map onto this frame.
- Chapter 07 teleop notes in this course, and Chapter 10 lesson 04, which consumes the frame you just froze.
