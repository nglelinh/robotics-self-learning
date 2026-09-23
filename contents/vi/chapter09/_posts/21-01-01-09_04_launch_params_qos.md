---
layout: post
title: "Launch, parameter và QoS"
chapter: "09"
order: 4
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter09
lesson_type: required
draft: false
---

Thời lượng: **~90 phút**.

## Mục tiêu

Bạn khởi động hai node từ một file launch Python, ghi đè một parameter từ file đó và từ dòng lệnh, rồi cố ý tạo lệch QoS để `/chatter` trông như còn sống trong khi `ros2 topic echo` im thin. Bạn đọc `ros2 topic info -v` đủ để nói bên nào chào best-effort và bên nào đòi reliable. Đó là chẩn đoán bạn sẽ dùng lại khi driver lidar và RViz không gặp nhau ở chương 11.

## Kiến thức cần trước

Bài 09-01 và 09-02: Jazzy đã được source, và bạn đã echo `/chatter` từ `demo_nodes_cpp`. Bạn tạo được file trong `~/ros2_ws/src`. Không cần robot. Parameter trong bài này là một giá trị có tên thuộc về một node (`use_sim_time`, cổng serial, khẩu độ bánh), không phải cờ dòng lệnh của `apt`.

## Vì sao bài này nằm trên lộ trình

Gõ `ros2 run` bốn lần là cách một demo bắt đầu. Đó không phải cách khung Capstone bắt đầu. Cầu nối, `robot_state_publisher`, teleop twist, và sau này Nav2 phải lên cùng nhau, với khẩu độ bài 08-04 ghi thành parameter thay vì số ma ở ba file. QoS là nửa kia. Laser scan là dòng có thể rơi gói. Bản đồ là tài liệu phải tới nơi. ROS 2 không giao scan best-effort cho subscriber reliable, và thường im. Người ta “sửa” Nav2 cả buổi chiều trong khi đồ thị chỉ đơn giản là không tương thích. Hãy học sự im lặng trên `/chatter` trước khi gặp nó trên `/scan`.

![QoS tương thích và không tương thích]({{ site.imgurl }}/generated/ch09_qos.png)

## Khái niệm

**File launch** mô tả một đồ thị tiến trình. Ở Jazzy file bạn viết là Python, dùng `launch` và `launch_ros`. Nó khởi động node, truyền parameter, và kéo theo launch khác. Launch XML vẫn còn; khóa này dùng Python vì tutorial nhập môn chính thức dùng vậy, và vì bạn tính được đường dẫn bằng `PathJoinSubstitution` thay vì hy vọng đường tương đối sống sót qua `colcon`.

**Parameter** là giá trị có kiểu trên một node: bool, int, double, string, hoặc mảng của chúng. `ros2 param list /talker` cho thấy node đó đã khai báo gì. `ros2 param get` đọc một giá trị. Đặt parameter từ dòng lệnh (`--ros-args -p name:=value`) chỉ ghi đè mặc định của tiến trình đó. File YAML là cách giữ một bộ ghi đè cho một robot:

```yaml
capstone_bridge:
  ros__parameters:
    port: /dev/ttyUSB0
    baud: 115200
    track_width: 0.16
    cmd_timeout_ms: 300
```

Khóa `ros__parameters` là bắt buộc. File chỉ có `track_width: 0.16` ở tầng trên cùng sẽ không rơi vào node. Tên node phải khớp. $$L$$ đã đo ở bài 08-04 thuộc về đây, một lần, và cầu nối đọc nó. Hai bản sao, một bản bằng centimét, là bài tập của bài đó vì một lý do.

**QoS** là hợp đồng trên publisher và trên subscription. Các chính sách hay cắn người mới là reliability, durability và độ sâu history.

Reliability: `reliable` gửi lại, `best_effort` thì không. Subscription reliable tương thích với publisher reliable. Subscription best-effort tương thích với cả hai. Subscription reliable **không** tương thích với publisher best-effort. Driver cảm biến (`sensor_msgs/LaserScan`, `Image`) thường xuất bản best-effort với hàng đợi nhỏ, profile người ta gọi là sensor data. Display LaserScan của RViz đôi khi mặc định reliable. Cách sửa là đổi QoS của display hoặc của subscription, không phải reboot lidar.

Durability: `volatile` không giữ lịch sử cho node đến muộn. `transient_local` thì có, đó là cách một bản đồ xuất bản một lần vẫn được node khởi động sau nhìn thấy. Publisher volatile không thỏa subscriber transient-local.

Độ sâu history là chiều dài hàng đợi. Độ sâu 1 nghĩa là “chỉ scan mới nhất đáng kể,” đúng với lidar 10 Hz và không đúng với một loạt lệnh ngắn nếu bạn cũng không cho watchdog hết hạn chúng.

`ros2 topic info /scan -v` in profile được chào và được yêu cầu cạnh nhau. Đầu cuối không tương thích hiện ra như publisher và subscription không liệt kê nhau là đã ghép. Echo với QoS mặc định có thể ngồi đó không in gì. Đó là lab.

## Ví dụ làm từng bước

Tạo gói và file launch. Từ workspace đã source:

```bash
cd ~/ros2_ws/src
ros2 pkg create capstone_bringup --build-type ament_python --dependencies launch_ros
mkdir -p capstone_bringup/launch capstone_bringup/config
```

`capstone_bringup/launch/talker_listener.launch.py`:

```python
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package="demo_nodes_cpp",
            executable="talker",
            name="talker",
            parameters=[{"use_sim_time": False}],
            output="screen",
        ),
        Node(
            package="demo_nodes_cpp",
            executable="listener",
            name="listener",
            output="screen",
        ),
    ])
```

Luật cài đặt: trong `setup.py`, danh sách `data_files` phải gồm thư mục launch, nếu không `ros2 launch` không thấy file sau `colcon build`. Mục điển hình:

```python
import os
from glob import glob
# bên trong data_files:
(os.path.join("share", package_name, "launch"), glob("launch/*.launch.py")),
```

Rồi:

```bash
cd ~/ros2_ws
colcon build --packages-select capstone_bringup
source install/setup.bash
ros2 launch capstone_bringup talker_listener.launch.py
```

**Mong đợi:** một terminal in `Publishing: 'Hello World: N'` và `I heard: [Hello World: N]`. Ctrl-C dừng cả hai node. Đó là ý của launch.

Kiểm parameter, talker vẫn chạy:

```bash
ros2 param get /talker use_sim_time
```

**Mong đợi:** `Boolean value is: False`.

Phá QoS, bạn làm cố ý. Terminal A xuất bản best-effort:

```bash
ros2 topic pub /chatter std_msgs/msg/String "{data: hi}" --qos-reliability best_effort
```

Terminal B echo với mặc định, tức reliable:

```bash
ros2 topic echo /chatter
```

**Mong đợi:** publisher đếm message, echo không in gì. Xác nhận:

```bash
ros2 topic info /chatter -v
```

Bạn sẽ thấy reliability của publisher là best effort và của subscription là reliable, và không có dấu chúng đã nối. Echo lại với chính sách khớp:

```bash
ros2 topic echo /chatter --qos-reliability best_effort
```

**Mong đợi:** `data: hi` bắt đầu hiện. Chép cặp lệnh đó vào `lab-notes.md`. Nó là mẫu cho câu “RViz không có scan.”

## Lab

1. Build `capstone_bringup` và launch talker cùng listener. Lưu dòng log chứng minh listener đã nghe talker.
2. Thêm `capstone_bringup/config/bridge.yaml` với bốn khóa ở phần khái niệm (`port`, `baud`, `track_width`, `cmd_timeout_ms`). Chưa có node cầu. Kiểm YAML đọc được: `python3 -c "import yaml; print(yaml.safe_load(open('config/bridge.yaml')))"` từ thư mục gói. **Mong đợi:** dict có khóa tầng trên duy nhất là `capstone_bridge`, bên trong là `ros__parameters`.
3. Chạy thí nghiệm best-effort với reliable. Ghi `ros2 topic info -v` cho ca hỏng và cho echo đã sửa.
4. Tùy chọn: `ros2 topic hz /chatter` trên echo đang chạy. `topic pub` không có `--rate` thì chậm. Thêm `-r 10` và kỳ vọng tần số gần 10.

**Khi hỏng thì thường vì**

| Bạn thấy | Nguyên nhân hay gặp |
| --- | --- |
| `file not found` khi launch | `setup.py` không cài `launch/`, hoặc quên source overlay sau build |
| Listener im, talker ổn, không phải QoS | Bạn launch hai talker và không có listener, hoặc listener chết vì sai kiểu parameter |
| YAML “đọc được” nhưng node bỏ qua `track_width` | Thiếu `ros__parameters`, hoặc tên node trong file không khớp |
| Echo chạy ở terminal này, không chạy ở terminal kia | Một trong hai có `--qos-reliability`. Mặc định khác điều bạn tưởng |
| `use_sim_time` true và talker đông cứng về sau | Không ai xuất bản `/clock`. Để false đến khi Gazebo vào ở chương 10 |

## Mua ở Việt Nam

Không linh kiện. Laptop của bài 09-01 là dụng cụ. Nếu bạn đã mua Pi 5 để làm máy robot, hãy làm lab này trên laptop trước, rồi lặp `printenv ROS_DISTRO` trên Pi. Đừng gỡ QoS và thẻ microSD chập chờn trong cùng một buổi chiều.

## Bài tập

1. YAML cầu nối đặt `cmd_timeout_ms: 300` và firmware cũng dùng 300 ms. Cái nào cắt nếu tiến trình laptop chết nhưng cáp USB vẫn cắm? Gợi ý: watchdog firmware. Timeout trong YAML chỉ giúp cầu quyết định *gửi* số 0. Cầu đã chết thì nó không gửi gì, và timer trên MCU mới là thứ dừng bánh.
2. Bạn cùng lớp xuất bản `/scan` best-effort và mở RViz với reliability là reliable. Dòng `topic info -v` nào kết thúc cuộc cãi? Gợi ý: publisher BEST_EFFORT, subscription RELIABLE, hai đầu không ghép.
3. Vì sao transient-local hợp với `/map` và tệ với `/cmd_vel`? Gợi ý: RViz đến muộn vẫn nên thấy bản đồ cuối. Cầu nối đến muộn không nên hành động theo Twist của mười phút trước.
4. Bạn muốn file launch từ chối khởi động khi thiếu `track_width`. Đó có phải lỗi QoS? Gợi ý: không. Đó là khai báo parameter. Node nên khai `track_width` mà không có mặc định im lặng `1.0`, hoặc file launch phải truyền nó ra.
5. Xếp thứ tự trong `capstone.launch.py` tương lai: cầu serial, `robot_state_publisher`, `teleop_twist_keyboard`. Cái gì phải là parameter, không phải chuỗi đóng cứng? Gợi ý: cổng serial và khẩu độ. Teleop có thể lên sau; nó chỉ xuất bản.

## Đọc thêm

- [Launch nhiều node](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Launch/Launch-Main.html) và tutorial [tạo file launch](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Launch/Creating-Launch-Files.html).
- [Tìm hiểu parameter](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Parameters/Understanding-ROS2-Parameters.html).
- [Về thiết lập Quality of Service](https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Quality-of-Service-Settings.html). Đọc bảng tương thích, không chỉ đọc tên.
- `ros2 topic echo -h` trên máy của bạn. Các cờ QoS trong help đó là những cờ lab đã dùng.
