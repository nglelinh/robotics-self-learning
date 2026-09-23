---
layout: post
title: "Nối Capstone A với ROS 2"
chapter: "10"
order: 4
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter10
lesson_type: required
draft: false
---

Thời lượng: **~90 phút**.

## Mục tiêu

Bạn chạy một node `rclpy` subscribe `/cmd_vel`, đổi `linear.x` và `angular.z` thành tốc độ vành trái và phải với khẩu độ $$L = 0.16$$ m, rồi ánh xạ các tốc độ đó sang số nguyên chương 08. Bạn ghi tỉ lệ ở một chỗ, 0,5 m/s vành thành số 100, và chỉ ra lệnh thẳng 0,2 m/s thành payload `V,40,40`. Bạn viết payload đó thành khung có độ dài: `STX 0xAA`, độ dài, payload ASCII, XOR, `0x0A`, và ép `V,0,0` lên dây khi 0,3 s không có Twist. Bạn chứng minh node bằng một cặp PTY `socat` và một parser nhỏ, nên lab không cần robot. Bạn nói được cái gì vẫn dừng động cơ nếu chính tiến trình cầu bị giết, và giữ bánh trên không nếu driver thật đang nối.

## Kiến thức cần trước

Khung bài 08-01 và timeout firmware 300 ms, động học nghịch bài 08-04, và một shell Jazzy có `rclpy`. Gói Python `pyserial` lấy từ apt dưới tên `python3-serial`, để nó ở cùng trình thông dịch với ROS. `socat` tạo cổng serial giả. Không cần Gazebo đang chạy, và đừng để agent serial micro-ROS giữ cổng. Capstone thật là tùy chọn và để cuối, bánh nhấc lên.

## Vì sao bài này nằm trên lộ trình

Node này là lần đầu đồ thị ROS và firmware Capstone dùng chung một lệnh. Mô phỏng đã nghe `/cmd_vel`. Nav2, và một policy học về sau, nên xuất bản đúng kiểu đó. Cả hai không biết `0xAA` nghĩa là gì, và firmware ESP32 hiện tại không biết Twist là gì. Cầu nối là chỗ duy nhất mét trên giây thành số nguyên −100…100. micro-ROS chỉ được phép sau khi file này chạy: cùng tên topic, cùng tỉ lệ, cùng câu chuyện watchdog, với log parser làm bằng chứng.

![Twist đi vào, khung chương 08 đi ra, telemetry quay lại]({{ site.imgurl }}/generated/ch10_serial_bridge.png)

## Khái niệm

`geometry_msgs/Twist` mang một vectơ tuyến tính và một vectơ góc. Khung vi sai chỉ tôn trọng hai trong sáu số đó. Tốc độ tiến $$v$$ là `linear.x`, mét trên giây. Tốc độ yaw $$\omega$$ là `angular.z`, radian trên giây, dương là cua trái theo REP-103. `linear.y` sẽ là trượt ngang. Cơ cấu không làm được việc đó, nên callback bỏ `linear.y` thay vì trộn trộm vào bánh.

Bản đồ nghịch từ bài 08-04, khẩu độ $$L$$ tính bằng mét:

$$
v_R = v + \omega \frac{L}{2}, \qquad v_L = v - \omega \frac{L}{2}
$$

Khung khóa học dùng $$L = 0.16$$, nên $$L/2 = 0.08$$. $$v_L$$ và $$v_R$$ là tốc độ vành, mét trên giây, dương là tiến. Chúng không phải PWM, và không phải số nguyên trên dây.

Dây vẫn là số nguyên chương 08, −100…100. Một hằng tỉ lệ nối hai thế giới. Bài này định full scale là 0,5 m/s vành:

$$
n = \mathrm{clip}\left(\mathrm{round}\left(v_{\mathrm{wheel}} \cdot \frac{100}{0.5}\right), -100, 100\right)
$$

Vậy 0,5 m/s thành 100, và 0,2 m/s thành 40. Hằng số 0,5 là một lựa chọn viết ở đầu file. Phép quay chương 07 cho tốc độ vành khác tại số 100 thì đổi hằng số và chú thích cùng lúc, cả hai phía. Ép mét thành `int` trước khi nhân tỉ lệ là lỗi khác: `int(0.2)` bằng 0, robot ngồi im trong khi topic trông đúng.

Payload là ASCII, `V,{left},{right}`, bánh trái trước. Khung quanh nó không đổi: byte `0xAA`, một byte độ dài bằng độ dài payload, payload, một XOR của mọi byte payload, và `0x0A`.

$$
c = b_0 \oplus b_1 \oplus \cdots \oplus b_{n-1}
$$

Cầu lặp khung mới nhất khoảng 20 lần một giây. Timeout firmware là 300 ms không có khung tốt, nên một khung rồi im sẽ dừng board kể cả khi ROS vẫn muốn chuyển động. Một timer thứ hai trong cầu nhìn Twist. 0,3 s không có Twist thì lệnh lặp lại thành `V,0,0`.

Cần cả hai cái dừng. Teleop chết mà cầu còn sống thì cầu là bên gửi số không. Cầu chết hoặc cáp USB rời thì watchdog firmware là cái dừng còn lại, và chỉ khi firmware có implement. Khối `finally` không chạy khi tiến trình bị giết hoặc cáp bị rút. Hãy thử publisher im, và đừng nhận là đã thử tiến trình bị giết.

Telemetry có thể trở về dạng chữ. Node publish nó thành `std_msgs/String` trên `/capstone_telem` khi có byte, không thì chỉ log. Đừng chặn nhịp 20 Hz để đợi một dòng. Parser chạy khô không trả lời, nên bằng chứng là dòng `OK` của parser.

Lưu node thành `capstone_bridge.py`. Tham số là `port` và `baud`, như hướng dẫn tham số Jazzy. Buổi chạy khô trỏ `port` vào một PTY. Board thật dùng `/dev/ttyUSB0` sau khi user ở nhóm `dialout`. Để `use_sim_time` không đặt, để phép kiểm 0,3 s dùng đồng hồ tường. Thời gian mô phỏng mà không có `/clock` sẽ đông cứng phép kiểm đó.

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

Lệnh thẳng không bắt được đảo trái/phải, vì hai số nguyên trùng nhau. `angular.z` dương phải cho số nguyên bánh phải lớn hơn bánh trái. Đó là phép kiểm dấu trong lab.

## Ví dụ làm từng bước

Đi thẳng, $$v = 0.2$$, $$\omega = 0$$, $$L = 0.16$$:

$$
v_L = v_R = 0.2
$$

$$
n = \mathrm{round}\left(0.2 \cdot \frac{100}{0.5}\right) = 40
$$

Payload `V,40,40`. Một cú cua trái nhẹ, $$v = 0$$, $$\omega = +0.5$$:

$$
v_L = -0.5 \times 0.08 = -0.04, \qquad v_R = 0.04
$$

$$
n_L = \mathrm{round}(-0.04 \times 200) = -8, \qquad n_R = 8
$$

Payload `V,-8,8`. Parser hiện `V,8,-8` thì thứ tự trả về trong `wheel_ints` bị ngược, robot sẽ cua sai chiều trên sàn.

Dây chạy khô là một cặp pseudo-terminal:

```bash
sudo apt install socat python3-serial
socat -d -d pty,raw,echo=0 pty,raw,echo=0
```

`socat` in hai đường, ví dụ `/dev/pts/3` và `/dev/pts/4`. Tham số `port` của cầu là một trong hai. Parser lấy từ bài 08-01 nghe đầu kia. Lưu thành `pty_parser.py`:

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

Rồi từ shell thứ tư:

```bash
source /opt/ros/jazzy/setup.bash
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 0.2, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"
```

Parser phải in `OK V,40,40` vài lần, khoảng 20 Hz, và trong khoảng một giây im phải in `OK V,0,0`. Log cầu phải hiện cùng hai chuỗi khi số nguyên đổi. Cặp đó là lab.

## Lab

1. Cài `socat` và `python3-serial`. Source Jazzy. Xác nhận `printenv ROS_DISTRO` là `jazzy`.
2. Bật `socat` như ví dụ. Ghi cả hai đường PTY. Để `socat` chạy.
3. Bật `pty_parser.py` trên đường thứ hai.
4. Bật `capstone_bridge.py` với `-p port:=` trỏ đường thứ nhất. Node phải đứng vững. Traceback lúc mở nghĩa là bạn đảo đường hoặc `socat` đã thoát.
5. Xuất bản một Twist với `linear.x` 0,2 và `angular.z` 0, bằng lệnh ở trên. Nhìn parser.
6. Đợi khoảng một giây không xuất bản nữa. Parser phải chuyển từ `V,40,40` sang `V,0,0` dù tiến trình cầu vẫn sống.
7. Xuất bản `angular.z` 0,5 với `linear.x` 0. Xác nhận `OK V,-8,8`. Thấy `V,8,-8` thì sửa `wheel_ints` trước khi động cơ thật quay.
8. Chỉ khi Capstone ở trên bàn: bánh nhấc khỏi mặt đất, driver ăn pack robot, USB chỉ để serial. Thêm user vào `dialout` nếu `python3` không mở được `/dev/ttyUSB0`, rồi đăng xuất và đăng nhập lại. Chạy cùng node với `-p port:=/dev/ttyUSB0`. Cả hai bánh phải nhích tiến cho lệnh thẳng và im sau khi bạn ngừng xuất bản. Rút cáp là phép thử riêng, làm một lần, bánh trên không: rút USB và xác nhận firmware, không phải cầu, là bên đưa PWM về không.

**Kết quả mong đợi**

Sau lần xuất bản thẳng, parser in:

```text
OK V,40,40
```

Khoảng một giây sau khi publisher im, cầu vẫn sống:

```text
OK V,0,0
```

Phép kiểm yaw in `OK V,-8,8`. Trên board thật, cả hai bánh quay tiến trong thời gian ngắn hơn một giây rồi dừng. Chúng không được quay tiếp sau khi publisher đã dừng.

**Khi hỏng thì thường vì**

| Bạn thấy | Nguyên nhân hay gặp |
| --- | --- |
| `OK V,8,-8` khi yaw dương | Trái và phải bị đảo trong `wheel_ints` hoặc trong thứ tự payload |
| `OK V,0,0` trong lệnh 0,2 m/s, hoặc `V,20,20` | Mét bị ép thành int, hoặc full scale là 1,0 m/s thay vì 0,5 m/s |
| Parser giữ `V,40,40` sau khi bạn ngừng xuất bản | Watchdog của cầu không nằm trong tick ghi khung; firmware cũng sẽ chạy tiếp nếu timeout của nó thiếu |
| Bánh chạy tiếp sau khi bạn giết cầu | Watchdog firmware là cái dừng còn lại, và nó chưa có hoặc chậm hơn nhiều so với 300 ms |
| `Permission denied` trên `/dev/ttyUSB0` | User không ở nhóm `dialout`, hoặc phiên đăng nhập có trước lúc đổi nhóm |
| Parser không in gì, cầu vẫn sống | Hai chương trình cùng một PTY, hoặc `socat` thiếu `echo=0` và một reader khác lấy mất byte |

## Mua ở Việt Nam

Không có linh kiện mới. Buổi chạy khô là `socat` và Python. Bản phần cứng dùng Capstone và cáp USB bạn đã có. Chỉ tìm “ESP32” trên [hshop.vn](https://hshop.vn/) nếu board đó đã chết. DevKit thay trên Shopee là `ESP32 DevKit V1 30 chân`, khoảng 2026 khoảng 80.000–180.000 đồng, kiểm tra trước khi trả. Đừng nuôi động cơ từ cáp USB đó.

## Bài tập

1. Tính số nguyên trên dây cho $$v = 0.2$$ m/s và $$\omega = 0.5$$ rad/s với $$L = 0.16$$ và tỉ lệ 0,5 m/s. Gợi ý: vành trái 0,16 m/s thành 32, vành phải 0,24 m/s thành 48, nên payload là `V,32,48`.
2. Publisher dừng, tiến trình cầu vẫn sống, một giây trôi qua. Payload trên dây là gì, và timer nào đặt nó lên đó? Gợi ý: `V,0,0` từ watchdog Twist 0,3 s của cầu, không phải từ firmware, vì khung vẫn đang tới.
3. Tiến trình cầu bị giết khi động cơ đã cấp và bánh trên không. Cái gì dừng chúng, và theo hạn nào? Gợi ý: watchdog firmware chương 08, khoảng 300 ms sau khung tốt cuối, vì khối `finally` của cầu không chạy.
4. `ls -l /dev/ttyUSB0` hiện nhóm `dialout` và Python ném `Permission denied`. Bạn đổi gì, và vì sao phải đăng nhập lại? Gợi ý: thêm user vào `dialout`; tư cách nhóm được áp lúc đăng nhập, nên shell mới trong phiên cũ là chưa đủ.
5. Một Twist tới với `linear.y = 0.3` và `linear.x = 0`. Bạn gửi số nguyên nào, và bỏ thành phần nào? Gợi ý: gửi số không chỉ từ $$v$$ và $$\omega$$; `linear.y` là trượt ngang mà khung vi sai không tạo được.

## Đọc thêm

- [Tham số Jazzy](https://docs.ros.org/en/jazzy/How-To-Guides/Using-ros2-param.html) là giao diện đằng sau `-p port:=` và `declare_parameter`.
- [REP-103](https://www.ros.org/reps/rep-0103.html) chốt dấu của `angular.z` mà `wheel_ints` thực hiện.
- [REP-105](https://www.ros.org/reps/rep-0105.html) là cách đặt tên frame bạn giữ khi cùng Twist này được dùng trong mô phỏng và trên cầu.
- [micro-ROS](https://micro.ros.org/) là đường truyền về sau. Quay lại chỉ sau khi parser này hiện `OK V,40,40` và dòng watchdog.
