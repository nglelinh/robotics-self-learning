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

Mục tiêu tối thượng của một kiến trúc phần mềm robot chuyên nghiệp là **tính trong suốt giữa mô phỏng và phần cứng thật (Sim/Real Parity)**: cùng một lệnh `ros2 topic pub /cmd_vel ...` hay cùng một ngăn xếp Nav2 phía trên phải chạy y hệt nhau mà *không cần biết* bên dưới là Gazebo Harmonic hay chiếc xe Capstone thật đặt trên sàn phòng lab. Bài học này xây dựng hoàn chỉnh tầng cầu nối (`bridge_capstone`) biến điều đó thành hiện thực.

## Bản đồ kiến thức nền: Ba trụ cột của Cầu nối Phần cứng Capstone

1. **Hợp đồng Giao diện Đồng nhất (Identical Topic & TF Contract)**:
   Cả `sim_bringup` lẫn `real_bringup` đều nhận đúng `/cmd_vel` (`Twist`), xuất đúng `/odom` (`Odometry`) và phát đúng cây TF `odom → base_link` theo chuẩn REP-103/105.
2. **Đóng gói Giao thức & Xử lý lỗi Kết nối (Reconnection & Watchdog)**:
   Node cầu nối trên SBC kiểm soát mở/đóng cổng serial an toàn, phát hiện mất gói tin, tự gửi lệnh vận tốc `0` khi tắt node (`on_shutdown`) và xuất trạng thái chẩn đoán (`/diagnostics`).
3. **Hoán đổi tầng thấp bằng Launch Argument (`use_sim:=true/false`)**:
   Tách rạch ròi tầng phần cứng/mô phỏng khỏi tầng định vị và điều hướng, giúp bạn phát triển thuật toán ở nhà trên Gazebo rồi sáng hôm sau chạy thẳng trên xe thật tại phòng lab.

## Mục tiêu

Sau bài học này, bạn sẽ chạy được một node `rclpy` đăng ký nhận `/cmd_vel`, chuyển đổi `linear.x` và `angular.z` thành vận tốc dài vành bánh trái và bánh phải với khoảng cách hai bánh $$L = 0.16$$ m, rồi ánh xạ sang dải số nguyên của chương 08. Bạn khai báo tập trung hệ số quy đổi (0,5 m/s tương ứng số nguyên 100) để kiểm chứng rằng lệnh chạy thẳng 0,2 m/s tạo ra payload `V,40,40`, đóng gói thành khung dữ liệu chuẩn (`STX 0xAA`, byte độ dài, payload ASCII, byte kiểm tra XOR và `0x0A`), đồng thời tự động gửi `V,0,0` khi quá 0,3 s không nhận được `Twist` mới. Bạn kiểm thử toàn bộ node mà không cần robot thật thông qua cặp cổng giả lập PTY (`socat`) cùng một bộ giải mã (parser) nhỏ, phân biệt được cơ chế nào vẫn dừng động cơ nếu tiến trình cầu nối bị tắt đột ngột, và luôn nhấc bánh xe khỏi mặt đất khi thử với phần cứng thật.

## Kiến thức cần trước

Nắm lại cấu trúc khung serial và watchdog firmware 300 ms ở bài 08-01, động học nghịch ở bài 08-04 và có sẵn môi trường Jazzy cài `rclpy`. Cài đặt thư viện `pyserial` qua `apt` (`python3-serial`) để dùng chung trình thông dịch Python với ROS, cùng công cụ `socat` để tạo cặp cổng serial ảo. Bài này không cần chạy Gazebo và không để micro-ROS serial agent chiếm giữ cổng. Thử nghiệm với xe Capstone thật là bước tùy chọn ở cuối bài (bắt buộc nhấc bánh khỏi sàn).

## Vì sao bài này nằm trên lộ trình

Node cầu nối này là điểm giao nhau đầu tiên giữa đồ thị ROS 2 và firmware Capstone A. Mô phỏng Gazebo đã lắng nghe `/cmd_vel`; về sau, cả Nav2 lẫn các mô hình học máy cũng xuất bản đúng kiểu message này mà không cần biết đến khung byte `0xAA`, trong khi firmware ESP32 hiện tại không hiểu `Twist`. Cầu nối đóng vai trò điểm chuyển đổi duy nhất từ vận tốc mét/giây sang số nguyên −100…100. Chỉ sau khi cầu nối này chạy ổn định với log kiểm chứng từ parser (đúng tên topic, đúng hệ số quy đổi và đúng hành vi watchdog), bạn mới nên chuyển sang micro-ROS.

![Twist đi vào, khung chương 08 đi ra, telemetry quay lại]({{ site.imgurl }}/generated/ch10_serial_bridge.png)

## Khái niệm

Message `geometry_msgs/Twist` chứa một vector vận tốc dài và một vector vận tốc góc, nhưng khung xe vi sai chỉ sử dụng hai trong sáu thành phần đó: vận tốc tiến $$v$$ là `linear.x` (m/s) và vận tốc góc yaw $$\omega$$ là `angular.z` (rad/s, dương khi quay sang trái theo REP-103). Thành phần `linear.y` biểu thị chuyển động trượt ngang mà cơ cấu vi sai không thực hiện được, nên hàm callback sẽ bỏ qua trường này thay vì trộn vào lệnh bánh xe.

Áp dụng công thức động học nghịch từ bài 08-04 với khoảng cách hai bánh $$L$$ (m):

$$
v_R = v + \omega \frac{L}{2}, \qquad v_L = v - \omega \frac{L}{2}
$$

Với khung xe khóa học có $$L = 0.16$$ m ($$L/2 = 0.08$$ m), $$v_L$$ và $$v_R$$ là vận tốc tiếp tuyến của hai bánh (m/s, dương khi tiến), chưa phải giá trị PWM hay số nguyên truyền trên dây.

Để đưa về dải số nguyên −100…100 của chương 08, ta định nghĩa hằng số quy đổi toàn thang (full scale) bằng 0,5 m/s:

$$
n = \mathrm{clip}\left(\mathrm{round}\left(v_{\mathrm{wheel}} \cdot \frac{100}{0.5}\right), -100, 100\right)
$$

Theo đó, 0,5 m/s tương ứng 100 và 0,2 m/s tương ứng 40. Hằng số `0.5` được khai báo rõ ở đầu tệp; nếu phép đo thực tế ở chương 07 cho tốc độ vành bánh khác tại mức 100, hãy cập nhật đồng thời hằng số và ghi chú ở cả hai phía. Tránh lỗi ép kiểu `int` trước khi nhân tỉ lệ (`int(0.2)` bằng `0`), vì khi đó robot sẽ đứng yên dù dữ liệu trên topic hoàn toàn đúng.

Payload có định dạng ASCII `V,{left},{right}` (bánh trái đứng trước), bọc trong khung cố định gồm byte mở đầu `0xAA`, một byte độ dài payload, chuỗi payload, một byte checksum XOR trên toàn bộ payload và byte kết thúc `0x0A`:

$$
c = b_0 \oplus b_1 \oplus \cdots \oplus b_{n-1}
$$

Cầu nối gửi lặp lại khung lệnh mới nhất ở tần số khoảng 20 Hz. Do firmware có timeout 300 ms, việc chỉ gửi một khung duy nhất rồi ngừng sẽ khiến mạch tự dừng dù ROS vẫn muốn xe tiếp tục chạy. Đồng thời, một timer bên trong cầu nối theo dõi thời điểm nhận `Twist` gần nhất: nếu quá 0,3 s không có lệnh mới, khung gửi đi sẽ tự động chuyển thành `V,0,0`.

Cả hai lớp bảo vệ đều bắt buộc phải có: nếu node teleop tắt nhưng cầu nối vẫn chạy, cầu nối chịu trách nhiệm gửi `V,0,0`; nếu chính cầu nối bị tắt đột ngột hoặc cáp USB bị rút, watchdog trên firmware sẽ dừng động cơ (khối `finally` của Python sẽ không kịp chạy khi tiến trình bị ngắt cưỡng bức hoặc mất cáp). Khi kiểm thử, cần phân biệt rõ phép thử dừng publisher với phép thử rút cáp.

Dữ liệu telemetry phản hồi dạng văn bản từ MCU (nếu có) sẽ được node đọc không chặn và xuất bản thành `std_msgs/String` lên `/capstone_telem`, đảm bảo không làm trễ nhịp gửi 20 Hz. Trong bước chạy thử nghiệm với `socat`, parser chỉ đọc một chiều nên bằng chứng kiểm thử là các dòng `OK` in ra trên terminal parser.

Lưu mã nguồn sau thành `capstone_bridge.py`. Hai tham số cấu hình là `port` và `baud`: khi chạy thử không có xe, trỏ `port` vào một đầu PTY; khi nối mạch thật, trỏ vào `/dev/ttyUSB0` (sau khi đã thêm user vào nhóm `dialout`). Giữ `use_sim_time` ở mặc định (`False`) để phép đo timeout 0,3 s chạy theo đồng hồ thực thay vì bị treo chờ `/clock`.

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

Lưu ý rằng lệnh đi thẳng không phát hiện được lỗi đảo chiều trái/phải vì hai bánh có cùng giá trị; cần kiểm tra thêm bằng lệnh quay với `angular.z` dương (giá trị bánh phải phải lớn hơn bánh trái).

## Ví dụ làm từng bước

Khi chạy thẳng ($$v = 0.2$$, $$\omega = 0$$, $$L = 0.16$$):

$$
v_L = v_R = 0.2
$$

$$
n = \mathrm{round}\left(0.2 \cdot \frac{100}{0.5}\right) = 40
$$

Payload thu được là `V,40,40`. Khi quay trái tại chỗ ($$v = 0$$, $$\omega = +0.5$$):

$$
v_L = -0.5 \times 0.08 = -0.04, \qquad v_R = 0.04
$$

$$
n_L = \mathrm{round}(-0.04 \times 200) = -8, \qquad n_R = 8
$$

Payload thu được là `V,-8,8`. Nếu parser hiển thị ngược thành `V,8,-8`, thứ tự trả về trong `wheel_ints` đang bị đảo và xe sẽ quay sai chiều trên thực tế.

Tạo cặp cổng serial ảo bằng `socat`:

```bash
sudo apt install socat python3-serial
socat -d -d pty,raw,echo=0 pty,raw,echo=0
```

`socat` sẽ in ra hai đường dẫn PTY (ví dụ `/dev/pts/3` và `/dev/pts/4`). Trỏ cầu nối vào một đầu và dùng parser từ bài 08-01 lắng nghe ở đầu kia. Lưu mã parser thành `pty_parser.py`:

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

Chạy parser trên đầu PTY thứ hai:

```bash
python3 pty_parser.py /dev/pts/4
```

Chạy cầu nối trên đầu PTY thứ nhất:

```bash
source /opt/ros/jazzy/setup.bash
python3 capstone_bridge.py --ros-args -p port:=/dev/pts/3
```

Mở terminal thứ tư và gửi một lệnh `Twist`:

```bash
source /opt/ros/jazzy/setup.bash
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 0.2, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"
```

Parser phải in ra `OK V,40,40` vài lần ở nhịp 20 Hz, sau đó (trong vòng chưa đầy một giây kể từ khi ngừng gửi) tự chuyển sang `OK V,0,0`. Log của node cầu nối cũng hiển thị chính xác hai chuỗi này khi giá trị thay đổi.

### Khung giải thích (nên đọc chậm): Kiểm chứng độ trễ khứ hồi (Round-Trip Latency) trên cầu nối SBC ↔ MCU

Để biết cầu nối phần cứng có đủ nhanh cho vòng điều hướng 20 Hz (`50 ms/nhịp`) hay không, ta cộng từng chặng trễ của 1 lệnh `/cmd_vel`:

| Chặng xử lý trên đường đi của lệnh | Độ trễ ước lượng |
| :--- | :---: |
| 1. ROS 2 DDS truyền `/cmd_vel` nội bộ trên SBC | ~`0,5 ms` |
| 2. Node cầu nối Python đóng gói khung tin + ghi xuống USB-Serial (`115200 bps`, 30 byte) | ~`3,0 ms` |
| 3. MCU chờ đến nhịp vòng lặp điều khiển tiếp theo (50 Hz, trung bình $$T_s/2$$) | ~`10,0 ms` |
| 4. MCU gửi ngược số đếm encoder (30 byte) về lại SBC và xuất `/odom` | ~`3,5 ms` |
| **Tổng độ trễ khứ hồi (Round-Trip)** | **~`17,0 ms`** (< `50 ms` → Đạt chuẩn!) |

Nếu tổng độ trễ vượt quá `40–50 ms` (ví dụ do `time.sleep()` chặn luồng hoặc buffer USB bị tích tụ), xe thật sẽ xuất hiện hiện tượng *lắc đuôi (oscillation)* khi Nav2 cố bám đường cong!

## Lab

1. Cài `socat` và `python3-serial`, nạp môi trường Jazzy và xác nhận `printenv ROS_DISTRO` là `jazzy`.
2. Khởi chạy `socat` như ví dụ, ghi lại hai đường dẫn PTY và giữ tiến trình hoạt động.
3. Chạy `pty_parser.py` trên đường dẫn PTY thứ hai.
4. Chạy `capstone_bridge.py` với `-p port:=` trỏ vào đường dẫn PTY thứ nhất. Nếu gặp traceback khi mở cổng, kiểm tra xem bạn có nhập nhầm đường dẫn hay `socat` đã thoát chưa.
5. Xuất bản một message `Twist` với `linear.x = 0.2` và `angular.z = 0`, theo dõi đầu ra của parser.
6. Chờ khoảng một giây không gửi thêm lệnh nào: parser phải chuyển từ `V,40,40` về `V,0,0` trong khi cầu nối vẫn chạy bình thường.
7. Xuất bản `angular.z = 0.5` với `linear.x = 0` và xác nhận parser in `OK V,-8,8` (nếu hiện `V,8,-8`, sửa ngay hàm `wheel_ints` trước khi thử với động cơ thật).
8. *(Tùy chọn với phần cứng thật)* Đặt xe Capstone lên bàn với hai bánh nhấc khỏi mặt đất, cấp nguồn động cơ từ pin riêng và chỉ dùng cáp USB cho serial. Nếu Python báo lỗi quyền mở `/dev/ttyUSB0`, thêm user vào nhóm `dialout` rồi đăng xuất/đăng nhập lại. Chạy cầu nối với `-p port:=/dev/ttyUSB0`: hai bánh phải nhích tiến khi có lệnh thẳng rồi dừng ngay sau khi ngừng gửi. Kiểm tra thêm một lần tình huống rút cáp USB (vẫn giữ bánh trên không) để xác nhận watchdog firmware tự đưa PWM về 0.

**Kết quả mong đợi**

Ngay sau lệnh chạy thẳng, parser in:

```text
OK V,40,40
```

Khoảng một giây sau khi ngừng gửi (cầu nối vẫn hoạt động):

```text
OK V,0,0
```

Phép kiểm tra góc quay in `OK V,-8,8`. Khi thử trên phần cứng thật, cả hai bánh chỉ quay tiến trong chưa đầy một giây rồi dừng hẳn, không được tiếp tục quay sau khi publisher kết thúc.

**Các lỗi thường gặp**

| Hiện tượng | Nguyên nhân thường gặp |
| --- | --- |
| In `OK V,8,-8` khi `angular.z` dương | Bị đảo thứ tự trái/phải trong `wheel_ints` hoặc trong chuỗi payload |
| In `OK V,0,0` (hoặc `V,20,20`) cho lệnh 0,2 m/s | Ép vận tốc mét/giây sang `int` quá sớm, hoặc đặt sai hệ số full scale là 1,0 m/s thay vì 0,5 m/s |
| Parser tiếp tục in `V,40,40` sau khi ngừng gửi | Logic watchdog của cầu nối không nằm trong vòng `tick` gửi khung (và firmware cũng sẽ chạy mãi nếu thiếu timeout) |
| Bánh vẫn quay sau khi tắt cầu nối | Watchdog trên firmware chưa hoạt động hoặc có ngưỡng thời gian lớn hơn 300 ms |
| Báo `Permission denied` khi mở `/dev/ttyUSB0` | Tài khoản chưa thuộc nhóm `dialout` hoặc chưa đăng nhập lại sau khi cập nhật nhóm |
| Parser không in gì dù cầu nối đang chạy | Mở nhầm cùng một đường PTY, hoặc `socat` thiếu `echo=0` / có tiến trình khác đang đọc chung cổng |

## Mua ở Việt Nam

Bài thực hành không cần mua thêm linh kiện mới: phần chạy thử dùng `socat` và Python, phần kiểm thử thật dùng xe Capstone và cáp USB sẵn có. Chỉ cần tìm mua thay thế bo "ESP32" trên [hshop.vn](https://hshop.vn/) hoặc `ESP32 DevKit V1 30 chân` trên Shopee (giá tham khảo 2026 khoảng 80.000–180.000 đồng) nếu mạch cũ bị hỏng. Tuyệt đối không nuôi động cơ từ nguồn cổng USB.

## Video tham khảo

- **Xem trước:** [How to start develop micro-ROS on ESP32 quickly!](https://www.youtube.com/watch?v=48SxC6LBVs8) — stepbystep-robotics (tiếng Anh). Minh họa kết nối giữa firmware ESP32 và đồ thị ROS 2, tương ứng với phía vi điều khiển của Capstone A.
- [What Is ROS2? - Framework Overview](https://www.youtube.com/watch?v=7TVWlADXwRw) — Raymond Andrade (tiếng Anh). Nhắc lại cơ chế truyền nhận topic `/cmd_vel`, giúp kiểm tra đồ thị trước khi nghi ngờ lỗi động cơ.

## Bài tập

1. Tính cặp số nguyên truyền trên dây khi $$v = 0.2$$ m/s, $$\omega = 0.5$$ rad/s với $$L = 0.16$$ m và hệ số toàn thang 0,5 m/s. *Gợi ý:* vận tốc vành trái là 0,16 m/s (tương ứng 32), vành phải là 0,24 m/s (tương ứng 48), nên payload là `V,32,48`.
2. Sau khi publisher dừng một giây trong khi cầu nối vẫn chạy, payload nào đang được truyền trên dây và bộ định thời nào phát ra nó? *Gợi ý:* `V,0,0`, phát ra từ watchdog 0,3 s theo dõi `Twist` trong cầu nối (không phải từ firmware, vì các khung serial vẫn đến đều ở 20 Hz).
3. Nếu tiến trình cầu nối bị tắt đột ngột khi động cơ đang quay (bánh nhấc trên không), cơ chế nào sẽ dừng bánh và sau bao lâu? *Gợi ý:* watchdog trên firmware chương 08 sẽ ngắt sau khoảng 300 ms kể từ khung hợp lệ cuối cùng, vì khối `finally` của cầu nối không kịp thực thi.
4. Lệnh `ls -l /dev/ttyUSB0` hiển thị nhóm `dialout` nhưng Python vẫn báo `Permission denied`. Bạn cần xử lý thế nào và vì sao phải đăng nhập lại? *Gợi ý:* thêm user vào nhóm `dialout`; danh sách nhóm của người dùng chỉ được nạp lại khi bắt đầu phiên đăng nhập mới nên mở terminal mới trong phiên cũ chưa có tác dụng.
5. Khi nhận một `Twist` có `linear.y = 0.3` và `linear.x = 0`, cầu nối sẽ gửi giá trị số nguyên nào và bỏ qua thành phần nào? *Gợi ý:* gửi `0, 0` vì chỉ tính từ $$v$$ và $$\omega$$; thành phần `linear.y` bị bỏ qua do cơ cấu vi sai không thể trượt ngang.

## Đọc thêm

- [Tham số Jazzy](https://docs.ros.org/en/jazzy/How-To-Guides/Using-ros2-param.html) — hướng dẫn chi tiết đằng sau cờ `-p port:=` và `declare_parameter`.
- [REP-103](https://www.ros.org/reps/rep-0103.html) — chuẩn quy ước dấu của `angular.z` được cài đặt trong `wheel_ints`.
- [REP-105](https://www.ros.org/reps/rep-0105.html) — chuẩn tên frame giữ thống nhất khi dùng chung `Twist` giữa mô phỏng và cầu nối thực tế.
- [micro-ROS](https://micro.ros.org/) — giải pháp thay thế cầu nối về sau, chỉ nên quay lại sau khi parser đã xác nhận `OK V,40,40` và hành vi watchdog.
