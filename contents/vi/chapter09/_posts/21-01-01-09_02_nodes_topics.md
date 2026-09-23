---
layout: post
title: "Node, topic và message"
chapter: "09"
order: 2
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter09
lesson_type: required
draft: false
---

Thời lượng: **~75 phút**.

## Mục tiêu

Bạn chạy talker và listener từ demo Jazzy, gọi tên topic và kiểu message nối chúng, và đọc tần số bằng `ros2 topic hz`. Bạn xuất bản một `geometry_msgs/Twist` bằng tay và chỉ vào hai trường mà khung vi sai thực sự dùng. Bạn cũng nói được gói interface là gì, để message bánh xe tự viết sau này là một gói, không phải dict Python mà bạn hy vọng node kia đoán được.

## Kiến thức cần trước

Bài 09-01: `printenv ROS_DISTRO` in `jazzy` trong terminal bạn sắp dùng. Động học chương 08: `linear.x` sẽ là $$v$$ và `angular.z` sẽ là $$\omega$$. Không cần robot.

## Vì sao bài này nằm trên lộ trình

Cầu nối Capstone là một node. `cmd_vel` là một topic. `Twist` là một message. Khi ba từ đó còn chưa nhàm, Gazebo, Nav2 và pipeline camera chỉ là thêm những node bạn không nhìn thấy. Policy “xuất bản action” là cùng một bức tranh với message khác. Không vẽ được đồ thị talker–topic–listener thì không gỡ được robot im lặng.

![Talker, topic, listener]({{ site.imgurl }}/generated/ch09_ros_graph.png)

## Khái niệm

Một **node** là một tiến trình (hoặc một đối tượng trong tiến trình) có tên trên đồ thị. Một **topic** là bus có tên. **Publisher** ghi message một kiểu lên bus đó. **Subscription** đọc chúng. Publisher không gọi subscriber theo tên. Nhiều subscriber có thể nghe, nên logger và cầu động cơ cùng nghe được `cmd_vel`.

Kiểu message là một phần hợp đồng. `std_msgs/msg/String` và `geometry_msgs/msg/Twist` là hai kiểu khác nhau. Subscriber của kiểu này không nối với publisher của kiểu kia, dù chuỗi tên topic trùng. Interface sống trong các gói. `ros2 interface show geometry_msgs/msg/Twist` in các trường. Với khóa này, trường đang sống là:

$$
v = \texttt{linear.x}, \qquad \omega = \texttt{angular.z}
$$

`linear.y` giữ 0. `linear.y` khác 0 là lời xin trượt ngang mà khung không làm được (bài 08-04).

Khám phá không phải phép màu tức thì trên mạng thù địch, nhưng trên một laptop các node demo hiện ra trong một giây. `ros2 node list`, `ros2 topic list`, `ros2 topic info /chatter` và `ros2 topic echo /chatter` là bốn lệnh bạn dùng đến khi thành phản xạ. `ros2 topic hz /chatter` cho thấy “đang xuất bản” có tần số, cùng kiểu bài 08-05 có chu kỳ.

## Tần số là một phần của hợp đồng

`ros2 topic hz /chatter` trên talker demo dừng gần 1 Hz. Con số đó không phải trang trí. Bài 08-05 đã dạy rằng vòng động cơ khai 50 Hz mà giao 12 Hz sẽ làm số hạng đạo hàm nói dối. Topic cũng cần sự trung thực đó. Khi cầu nối Capstone tồn tại, bạn sẽ subscribe `/cmd_vel` và cũng hỏi `hz`. Teleop bàn phím chỉ xuất bản khi phím đổi có thể ngồi ở 0 Hz lúc bạn không chạm. Watchdog firmware khi đó dừng bánh, đúng, và làm người ta ngạc nhiên vì họ tưởng “topic tồn tại” nghĩa là “lệnh còn tươi.”

Thử một lần khi talker đang chạy:

```bash
ros2 topic hz /chatter
ros2 topic bw /chatter
ros2 topic echo /chatter --field data
```

**Mong đợi:** `average rate: 1.000` hoặc rất gần, băng thông vài byte mỗi giây, và dạng `--field` chỉ in chuỗi, không có vỏ YAML. `bw` trên một `Twist` sau này cũng nhỏ. `bw` trên ảnh camera thì không. Nếu bạn từng bắc cầu ảnh qua đường truyền yếu, lệnh này cho bạn thấy trước khi đổ cho bộ phát hiện.

Message cụ thể thứ hai, cái bạn đã gặp như lần xuất bản một phát, cần một tần số kéo dài. Một terminal:

```bash
ros2 topic pub -r 5 /cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 0.0}, angular: {z: 0.0}}"
```

Terminal kia:

```bash
ros2 topic hz /cmd_vel
```

**Mong đợi:** khoảng 5 Hz, và robot vẫn không chạy, vì chưa có gì subscribe kèm động cơ. Để chạy mười giây rồi Ctrl-C. Ghi tần số. Cầu nối chương 10 sẽ coi “không có message trong 300 ms” là dừng. Ở 5 Hz khoảng cách giữa các message là 200 ms, nằm trong cửa sổ đó. Ở 1 Hz khoảng cách là 1000 ms và watchdog sẽ chặt lệnh thành từng nhịp. Đó là lỗi động học và thời gian bạn đoán được mà không cần robot trên sàn.

## Lab

Terminal A, sau khi source Jazzy:

```bash
ros2 run demo_nodes_cpp talker
```

**Mong đợi**, lặp lại:

```text
[INFO] [talker]: Publishing: 'Hello World: 1'
[INFO] [talker]: Publishing: 'Hello World: 2'
```

Terminal B:

```bash
ros2 topic echo /chatter
```

**Mong đợi:**

```text
data: 'Hello World: 3'
---
```

Terminal C:

```bash
ros2 node list
ros2 topic info /chatter
ros2 topic hz /chatter
```

**Hình dạng mong đợi:**

```text
/talker
Type: std_msgs/msg/String
average rate: 1.000
```

Talker xuất bản khoảng 1 Hz. Nếu `hz` nói `no messages`, bạn echo sai tên hoặc terminal talker đã chết.

Dừng talker bằng Ctrl-C. Xuất bản một Twist, bản chạy khô của cầu nối:

```bash
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 0.20, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.10}}"
ros2 topic echo --once /cmd_vel
```

Không có gì chuyển động. Chưa có subscriber nào cầm động cơ. Sự im lặng đó là đúng. Ghi chú: “0,20 m/s tiến, 0,10 rad/s trái, chưa có cầu.”

**Khi hỏng thì thường vì**

| Bạn thấy | Nguyên nhân hay gặp |
| --- | --- |
| `Package 'demo_nodes_cpp' not found` | Thiếu bản desktop, hoặc shell này chưa source |
| Echo không in | Sai tên topic, hoặc lệch QoS (bài sau). Demo khớp nhau |
| `hz` lệch xa 1 | Publisher khác trên `/chatter`, hoặc máy ảo quá tải |
| Lỗi YAML khi pub Twist | Dấu nháy. Chép lệnh thành một dòng |
| Bạn mong ESP32 giật | Nó chưa ở trên đồ thị này. Chương 10 mới xây subscriber |

## Mua ở Việt Nam

Không phần cứng. Tùy chọn sau: Pi 5 của bài 09-01 nếu bạn muốn đồ thị này rời laptop. Đừng mua “kit robot ROS” tuần này chỉ để thấy `/chatter`.

## Bài tập

1. Một câu: vì sao hai terminal cùng echo `/chatter` được? Gợi ý: topic là bus, không phải cuộc gọi.
2. Trường nào của `Twist` phải gần 0 trên khung Capstone, và vì sao? Gợi ý: `linear.y`. Cơ cấu không có tốc độ ngang.
3. `ros2 topic info /cmd_vel` sau lệnh `--once` không thấy publisher. Có phải lỗi? Gợi ý: `--once` thoát. Info là ảnh những ai còn sống lúc đó.
4. Phác đồ thị tương lai: `teleop_twist_keyboard` → `/cmd_vel` → `capstone_bridge` → khung serial. Message trên topic tên là gì? Gợi ý: `geometry_msgs/msg/Twist`.
5. `ros2 interface show` bảo vệ bạn khỏi điều gì? Gợi ý: đoán tên trường. `angular.z` là yaw, không phải `angular.yaw`.

## Đọc thêm

- [Tìm hiểu node](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Nodes/Understanding-ROS2-Nodes.html).
- [Tìm hiểu topic](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Topics/Understanding-ROS2-Topics.html).
- [`geometry_msgs/Twist`](https://docs.ros.org/en/jazzy/p/geometry_msgs/msg/Twist.html).
- Bài 08-04 của khóa cho phép nghịch biến message này thành tốc độ bánh.
