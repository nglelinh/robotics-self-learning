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

Nếu bạn viết toàn bộ mã đọc LiDAR, chạy SLAM, tính đường đi và điều khiển động cơ vào một tệp `main.py` khổng lồ, chỉ cần camera bị treo một nhịp là cả động cơ cũng đứng hình theo. **ROS 2** giải quyết triệt để vấn đề đó bằng kiến trúc đồ thị tính toán phân tán: chia robot thành hàng chục tiến trình nhỏ độc lập gọi là **Node**, nói chuyện với nhau qua các kênh dữ liệu có kiểu định nghĩa chặt chẽ gọi là **Topic**.

## Bản đồ kiến thức nền: Ba trụ cột của Node và Topic trong ROS 2

1. **Tách rời hoàn toàn (Decoupling) bằng Publish / Subscribe**:
   Node phát (`Publisher`) chỉ gửi thông điệp lên tên topic (ví dụ `/scan`) mà không cần biết có bao nhiêu node đang nghe; node nhận (`Subscriber`) đăng ký topic đó mà không phụ thuộc ngôn ngữ lập trình của bên phát (C++ nói chuyện tự nhiên với Python).
2. **Hợp đồng kiểu dữ liệu (Message Interface) & Tần số xuất bản**:
   Mỗi topic gắn chặt với một cấu trúc tin chuẩn (như `geometry_msgs/msg/Twist`, `sensor_msgs/msg/LaserScan`) và một tần số cam kết (Hz). Tần số là một phần của hợp đồng thời gian thực!
3. **Middleware DDS (Khám phá ngang hàng không cần `roscore`)**:
   Khác với ROS 1 phụ thuộc một máy chủ trung tâm dễ hỏng (`roscore`), ROS 2 chạy trên chuẩn công nghiệp **DDS** cho phép các node tự phát hiện lẫn nhau trong mạng LAN.

## Mục tiêu

Sau bài học này, bạn sẽ chạy được cặp node mẫu `talker` và `listener` trong ROS 2 Jazzy, xác định được tên topic cùng kiểu message kết nối chúng và đo tần số truyền tin bằng `ros2 topic hz`. Bạn cũng sẽ xuất bản thủ công một message `geometry_msgs/Twist`, chỉ ra đúng hai trường dữ liệu mà khung xe vi sai thực sự sử dụng, đồng thời hiểu vai trò của gói định nghĩa giao diện (interface package) để về sau các message bánh xe tự định nghĩa luôn có cấu trúc rõ ràng thay vì truyền dữ liệu kiểu `dict` Python rời rạc.

## Kiến thức cần trước

Hoàn thành bài 09-01 sao cho lệnh `printenv ROS_DISTRO` trả về `jazzy` trong terminal sắp dùng. Nắm lại mô hình động học ở chương 08: trường `linear.x` tương ứng với vận tốc dài $$v$$ và `angular.z` tương ứng với vận tốc góc $$\omega$$. Bài thực hành này chưa cần robot thật.

## Vì sao bài này nằm trên lộ trình

Trong hệ thống Capstone, cầu nối điều khiển là một node, `cmd_vel` là một topic và `Twist` là một kiểu message. Nếu chưa nắm vững ba khái niệm nền tảng này, bạn sẽ rất khó hình dung cách hoạt động của Gazebo, Nav2 hay pipeline xử lý ảnh camera (thực chất cũng chỉ là các node trao đổi dữ liệu qua topic). Ngay cả các mô hình học máy xuất bản hành động (action) cũng tuân theo cùng cơ chế này với kiểu message khác. Việc không vẽ được đồ thị kết nối giữa publisher, topic và subscriber sẽ khiến bạn lúng túng khi gỡ lỗi robot không phản hồi.

![Talker, topic, listener]({{ site.imgurl }}/generated/ch09_ros_graph.png)

## Khái niệm

Một **node** là một tiến trình (hoặc một thực thể độc lập bên trong tiến trình) có tên xác định trên đồ thị ROS. Một **topic** hoạt động như một kênh truyền dữ liệu (bus) có tên riêng. **Publisher** gửi các message theo một kiểu dữ liệu cố định lên kênh đó, còn **subscription** (subscriber) đăng ký nhận dữ liệu từ kênh. Publisher không cần gọi đích danh subscriber và nhiều subscriber có thể cùng lắng nghe một topic, nhờ vậy cả bộ ghi nhật ký (logger) lẫn cầu nối động cơ đều có thể nhận đồng thời `/cmd_vel`.

Kiểu message là một phần của giao ước dữ liệu. Ví dụ `std_msgs/msg/String` và `geometry_msgs/msg/Twist` là hai kiểu hoàn toàn khác nhau; subscriber của kiểu này sẽ không thể kết nối với publisher của kiểu kia dù tên topic giống hệt nhau. Các định nghĩa giao diện nằm trong những gói riêng, và lệnh `ros2 interface show geometry_msgs/msg/Twist` sẽ liệt kê chi tiết các trường dữ liệu. Với khung xe vi sai trong khóa học, hai trường được sử dụng là:

$$
v = \texttt{linear.x}, \qquad \omega = \texttt{angular.z}
$$

Trường `linear.y` luôn giữ bằng 0, vì giá trị khác 0 biểu thị yêu cầu chuyển động trượt ngang mà cơ cấu vi sai không thể thực hiện (bài 08-04).

Trên một máy tính cục bộ, quá trình khám phá node thường diễn ra trong khoảng một giây (trừ trường hợp mạng bị tường lửa hoặc cấu hình chặn). Bốn lệnh cần luyện thành thói quen gồm `ros2 node list`, `ros2 topic list`, `ros2 topic info /chatter` và `ros2 topic echo /chatter`. Bên cạnh đó, `ros2 topic hz /chatter` cho biết tần số xuất bản thực tế, tương tự việc kiểm tra chu kỳ vòng lặp ở bài 08-05.

## Tần số là một phần của giao ước truyền tin

Khi chạy `ros2 topic hz /chatter` với node `talker` mẫu, tần số đo được xấp xỉ 1 Hz. Con số này mang ý nghĩa kỹ thuật trực tiếp: ở bài 08-05, ta đã thấy vòng điều khiển động cơ thiết kế cho 50 Hz nhưng thực tế chỉ chạy ở 12 Hz sẽ làm sai lệch thành phần đạo hàm. Các topic ROS cũng đòi hỏi sự đảm bảo tương tự về tần số. Khi xây dựng cầu nối Capstone, bạn sẽ đăng ký nghe `/cmd_vel` và kiểm tra tần số bằng `hz`. Nếu dùng bộ điều khiển từ bàn phím (teleop) chỉ gửi message khi phím thay đổi, tần số có thể rơi về 0 Hz lúc bạn không thao tác; khi đó watchdog trên firmware sẽ dừng bánh xe, dễ gây nhầm lẫn nếu bạn cho rằng "topic vẫn tồn tại" đồng nghĩa với "lệnh điều khiển vẫn đang được cập nhật liên tục".

Hãy thử các lệnh sau khi `talker` đang chạy:

```bash
ros2 topic hz /chatter
ros2 topic bw /chatter
ros2 topic echo /chatter --field data
```

**Kết quả mong đợi:** `average rate: 1.000` (hoặc rất gần 1 Hz), băng thông chỉ vài byte mỗi giây, và tùy chọn `--field data` chỉ in nội dung chuỗi mà không kèm cấu trúc YAML bao ngoài. Về sau, băng thông của một topic `Twist` cũng rất nhỏ, nhưng băng thông của luồng ảnh camera thì rất lớn; dùng `ros2 topic bw` giúp bạn phát hiện sớm hiện tượng nghẽn đường truyền trước khi vội kết luận lỗi nằm ở thuật toán nhận diện.

Tiếp theo, hãy thử xuất bản liên tục message `Twist` ở một tần số xác định. Mở terminal thứ nhất:

```bash
ros2 topic pub -r 5 /cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 0.0}, angular: {z: 0.0}}"
```

Mở terminal thứ hai:

```bash
ros2 topic hz /cmd_vel
```

**Kết quả mong đợi:** tần số xấp xỉ 5 Hz và robot không di chuyển vì chưa có node điều khiển động cơ nào đăng ký nghe topic này. Để chạy khoảng mười giây rồi nhấn Ctrl-C để dừng và ghi lại tần số đo được. Cầu nối ở chương 10 sẽ quy ước dừng xe nếu không nhận được message nào trong 300 ms. Ở tần số 5 Hz, chu kỳ giữa hai message là 200 ms — nằm gọn trong ngưỡng an toàn; ngược lại, ở 1 Hz chu kỳ lên tới 1000 ms khiến watchdog liên tục ngắt lệnh làm xe chạy giật cục. Đây là bài toán về thời gian và động học mà bạn hoàn toàn có thể kiểm chứng trước khi đặt robot xuống sàn.

### Khung giải thích (nên đọc chậm): Tính tay ngân sách băng thông mạng Wi-Fi cho đồ thị 3 Topic của robot

Giả sử robot phát đồng thời 3 topic về laptop giám sát qua Wi-Fi:

| Topic | Kiểu thông điệp | Kích thước / tin | Tần số | Lưu lượng (KB/s) |
| :--- | :--- | :---: | :---: | :---: |
| `/cmd_vel` | `geometry_msgs/Twist` | 48 byte | 20 Hz | $$48 \times 20 \approx \mathbf{1\text{ KB/s}}$$ |
| `/odom` | `nav_msgs/Odometry` | ~700 byte | 50 Hz | $$700 \times 50 = \mathbf{35\text{ KB/s}}$$ |
| `/scan` | `sensor_msgs/LaserScan` (720 tia) | ~6 KB | 10 Hz | $$6 \times 10 = \mathbf{60\text{ KB/s}}$$ |
| **Tổng cộng** | | | | **~96 KB/s (< 0,8 Mbps)** |

Toàn bộ dữ liệu điều khiển và LiDAR 2D chỉ tốn chưa tới **1 Mbps** — cực kỳ nhẹ nhàng trên Wi-Fi 5 GHz. Ngược lại, chỉ cần mở thêm 1 topic ảnh thô `/camera/image_raw` (~27 MB/s = 216 Mbps) là toàn bộ mạng Wi-Fi tắc nghẽn ngay lập tức!

## Lab

Mở Terminal A (sau khi đã nạp môi trường Jazzy):

```bash
ros2 run demo_nodes_cpp talker
```

**Kết quả mong đợi** (in lặp lại):

```text
[INFO] [talker]: Publishing: 'Hello World: 1'
[INFO] [talker]: Publishing: 'Hello World: 2'
```

Mở Terminal B:

```bash
ros2 topic echo /chatter
```

**Kết quả mong đợi:**

```text
data: 'Hello World: 3'
---
```

Mở Terminal C:

```bash
ros2 node list
ros2 topic info /chatter
ros2 topic hz /chatter
```

**Kết quả mong đợi có dạng:**

```text
/talker
Type: std_msgs/msg/String
average rate: 1.000
```

Node `talker` xuất bản ở tần số khoảng 1 Hz. Nếu lệnh `hz` báo `no messages`, hãy kiểm tra lại tên topic hoặc xem terminal chạy `talker` có bị tắt hay không.

Dừng `talker` bằng Ctrl-C, sau đó xuất bản thử một message `Twist` duy nhất (bước chạy thử nghiệm trước khi có cầu nối):

```bash
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 0.20, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.10}}"
ros2 topic echo --once /cmd_vel
```

Chưa có thiết bị nào chuyển động vì chưa có subscriber điều khiển động cơ — trạng thái yên tĩnh này là hoàn toàn bình thường. Ghi vào sổ thực hành: "0,20 m/s tiến, 0,10 rad/s quay trái, chưa có cầu nối."

**Các lỗi thường gặp**

| Hiện tượng | Nguyên nhân thường gặp |
| --- | --- |
| `Package 'demo_nodes_cpp' not found` | Chưa cài bản `ros-jazzy-desktop`, hoặc terminal hiện tại chưa nạp môi trường ROS |
| `echo` không in dữ liệu | Gõ sai tên topic, hoặc cấu hình QoS không tương thích (xem bài sau; các ví dụ mẫu đã khớp sẵn) |
| Tần số `hz` lệch xa 1 Hz | Có publisher khác cùng gửi lên `/chatter`, hoặc máy ảo đang quá tải |
| Báo lỗi cú pháp YAML khi pub `Twist` | Sai dấu nháy; hãy gộp toàn bộ lệnh thành một dòng duy nhất |
| Chờ ESP32 quay bánh nhưng không thấy phản ứng | ESP32 chưa được nối vào đồ thị ROS; phần subscriber cầu nối sẽ được xây dựng ở chương 10 |

## Mua ở Việt Nam

Bài này không yêu cầu phần cứng. Tùy chọn về sau là Raspberry Pi 5 (đã nêu ở bài 09-01) nếu bạn muốn đưa đồ thị ROS ra khỏi laptop. Không cần mua các bộ "kit robot ROS" chỉ để chạy thử `/chatter`.

## Video tham khảo

- **Xem trước:** [What Is ROS2? - Framework Overview](https://www.youtube.com/watch?v=7TVWlADXwRw) — Raymond Andrade (tiếng Anh). Giải thích rõ hai khái niệm node và topic cùng cách hoạt động của một publisher và một subscriber.
- [ROS2 & F1TENTH #01 | ROS2 là gì? Workspace, Package, Node](https://www.youtube.com/watch?v=UJ7zkUJnVKw) — Nhat Tran (tiếng Việt). Giới thiệu workspace, package và node bằng tiếng Việt; lưu ý bản ROS bạn đang cài trên máy vẫn là Jazzy.
- [ROS 2 Series #4 | Viết template ROS2 Python section | TeslaEdison](https://www.youtube.com/watch?v=03kUlBnH7gg) — TeslaEdison (tiếng Việt). Hướng dẫn tạo khung một node Python; giữ đúng API `rclpy` của Jazzy nếu video dùng cú pháp phiên bản cũ hơn.

## Bài tập

1. Giải thích ngắn gọn trong một câu: vì sao hai cửa sổ terminal có thể cùng chạy `echo /chatter` một lúc? *Gợi ý:* topic hoạt động theo cơ chế bus phát tán, không phải lời gọi điểm-tới-điểm.
2. Trường nào trong `Twist` phải giữ bằng 0 trên khung xe Capstone và vì sao? *Gợi ý:* `linear.y`, vì cơ cấu xe vi sai không có khả năng di chuyển ngang.
3. Sau khi chạy lệnh `--once`, kiểm tra `ros2 topic info /cmd_vel` không thấy publisher nào. Đây có phải là lỗi không? *Gợi ý:* không, vì lệnh `--once` tự kết thúc ngay sau khi gửi, còn `info` chỉ phản ánh các node đang hoạt động tại thời điểm truy vấn.
4. Vẽ sơ đồ đồ thị ROS dự kiến: `teleop_twist_keyboard` → `/cmd_vel` → `capstone_bridge` → khung serial. Kiểu message truyền trên topic này là gì? *Gợi ý:* `geometry_msgs/msg/Twist`.
5. Lệnh `ros2 interface show` giúp bạn tránh sai sót nào khi lập trình? *Gợi ý:* tránh đoán mò tên trường dữ liệu (ví dụ góc quay quanh trục đứng là `angular.z`, không phải `angular.yaw`).

## Đọc thêm

- [Tìm hiểu node](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Nodes/Understanding-ROS2-Nodes.html)
- [Tìm hiểu topic](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Topics/Understanding-ROS2-Topics.html)
- [`geometry_msgs/Twist`](https://docs.ros.org/en/jazzy/p/geometry_msgs/msg/Twist.html)
- Bài 08-04 của khóa học về phép động học nghịch chuyển đổi message `Twist` thành vận tốc hai bánh xe.
