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

Một robot tự hành thực thụ thường có từ 8 đến 20 node chạy song song. Bạn không thể mở 15 cửa sổ terminal để gõ tay từng lệnh `ros2 run` kèm chục tham số mỗi lần khởi động! **Launch files** (viết bằng Python/YAML), hệ thống **Parameters** động và chính sách chất lượng dịch vụ **QoS (Quality of Service)** chính là bộ ba công cụ biến các node rời rạc thành một hệ thống robot vận hành tin cậy chỉ bằng một lệnh duy nhất.

## Kiến thức cần nhớ: Ba trụ cột Vận hành Hệ thống ROS 2

1. **Launch System (Khởi chạy đồng bộ & Remapping)**:
   Khởi chạy nhiều node, nạp tệp cấu hình YAML chung và đổi tên topic (*remapping*) mà không phải sửa lại mã nguồn C++/Python.
2. **Parameters (Tham số hóa động)**:
   Tách toàn bộ hằng số tinh chỉnh (bán kính bánh $$r$$, hệ số PID, ngưỡng vận tốc tối đa) ra tệp YAML để có thể hiệu chỉnh ngay tại hiện trường mà không cần biên dịch lại.
3. **Chính sách QoS (Reliability, Durability, History)**:
   Quyết định hành vi truyền tin trên mạng không hoàn hảo: dữ liệu cảm biến tần số cao ưu tiên `BEST_EFFORT` (thà bỏ 1 khung cũ còn hơn chờ truyền lại làm trễ khung mới), còn bản đồ `/map` hay lệnh cấu hình cần `RELIABLE` + `TRANSIENT_LOCAL` (người nghe vào sau vẫn nhận được bản đồ!).

## Mục tiêu

Sau bài học này, bạn sẽ khởi chạy được hai node cùng lúc từ một tệp launch Python, ghi đè một tham số (parameter) từ cả tệp launch lẫn dòng lệnh, và chủ động tạo ra sự không tương thích QoS để quan sát tình huống `/chatter` vẫn hoạt động nhưng `ros2 topic echo` không nhận được dữ liệu. Bạn cũng sẽ đọc được đầu ra của `ros2 topic info -v` để xác định bên nào đang dùng chính sách `best_effort` và bên nào yêu cầu `reliable` — kỹ năng chẩn đoán quan trọng khi kết nối driver lidar với RViz ở chương 11.

## Kiến thức cần trước

Hoàn thành bài 09-01 và 09-02: môi trường Jazzy đã được nạp và bạn đã chạy thử `echo /chatter` với `demo_nodes_cpp`. Bạn cần biết tạo tệp bên trong `~/ros2_ws/src`; bài này chưa cần robot thật. Lưu ý rằng "parameter" trong bài là biến cấu hình có tên gắn với một node (ví dụ `use_sim_time`, cổng serial, chiều rộng trục bánh), không phải tùy chọn dòng lệnh của `apt`.

## Vì sao bài này nằm trên lộ trình

Chạy riêng lẻ `ros2 run` ở nhiều terminal chỉ phù hợp cho các ví dụ thử nghiệm ban đầu, không phải cách vận hành khung xe Capstone. Cầu nối điều khiển, `robot_state_publisher`, teleop và sau này là Nav2 cần được khởi động đồng bộ, trong đó khoảng cách hai bánh đo ở bài 08-04 được khai báo dưới dạng parameter tập trung thay vì ghi cứng rải rác ở nhiều tệp.

Mảnh ghép còn lại là QoS (Quality of Service). Dữ liệu quét laser là luồng liên tục có thể chấp nhận mất gói nhỏ, còn bản đồ là dữ liệu cần truyền đủ tới nơi. ROS 2 không tự động ghép một publisher `best_effort` với một subscriber `reliable`, và sự từ chối kết nối này thường diễn ra âm thầm. Rất nhiều người mất hàng giờ gỡ lỗi Nav2 trong khi nguyên nhân thực sự chỉ là hai đầu topic không tương thích QoS. Thực hành trước hiện tượng này trên `/chatter` sẽ giúp bạn nhận ra ngay khi gặp lại trên `/scan`.

![QoS tương thích và không tương thích]({{ site.imgurl }}/generated/ch09_qos.png)

## Khái niệm

**Tệp launch** mô tả tập hợp các tiến trình cần khởi chạy cùng nhau. Trong ROS 2 Jazzy, khóa học viết tệp launch bằng Python với hai thư viện `launch` và `launch_ros` để khởi chạy node, truyền parameter và lồng ghép các tệp launch khác. Dù định dạng XML vẫn được hỗ trợ, Python là chuẩn trong tài liệu nhập môn chính thức và cho phép ghép đường dẫn động bằng `PathJoinSubstitution` thay vì phụ thuộc vào đường dẫn tương đối dễ lỗi sau khi biên dịch bằng `colcon`.

**Parameter** là biến cấu hình có kiểu dữ liệu rõ ràng thuộc về một node (bool, int, double, string hoặc mảng của các kiểu này). Lệnh `ros2 param list /talker` liệt kê các tham số mà node đã khai báo, còn `ros2 param get` đọc giá trị hiện tại. Truyền tham số qua dòng lệnh (`--ros-args -p name:=value`) chỉ ghi đè giá trị mặc định cho riêng phiên chạy đó. Để quản lý toàn bộ cấu hình cho một robot, ta lưu chúng trong tệp YAML:

```yaml
capstone_bridge:
  ros__parameters:
    port: /dev/ttyUSB0
    baud: 115200
    track_width: 0.16
    cmd_timeout_ms: 300
```

Khóa `ros__parameters` là bắt buộc; nếu đặt thẳng `track_width: 0.16` ở cấp cao nhất, node sẽ không nạp được giá trị này, và tên node ở dòng đầu tiên phải khớp chính xác. Giá trị khoảng cách hai bánh $$L$$ đo ở bài 08-04 chỉ cần khai báo một lần duy nhất tại đây để cầu nối đọc vào, tránh tình trạng lưu trùng lặp ở nhiều nơi dẫn đến sai lệch đơn vị.

**QoS** là tập quy ước truyền thông gắn trên từng publisher và subscriber. Ba chính sách người mới thường gặp vướng mắc nhất là độ tin cậy (reliability), độ bền dữ liệu (durability) và độ sâu lịch sử (history depth).

Về **reliability**: `reliable` đảm bảo gửi lại gói tin nếu mất, còn `best_effort` thì không. Một subscriber `reliable` chỉ ghép được với publisher `reliable`; subscriber `best_effort` nhận được từ cả hai; còn subscriber `reliable` **không** tương thích với publisher `best_effort`. Các driver cảm biến (`sensor_msgs/LaserScan`, `Image`) thường phát theo chế độ `best_effort` với hàng đợi ngắn (hồ sơ *sensor data*), trong khi hiển thị LaserScan trên RViz đôi khi mặc định `reliable`. Khi gặp lỗi này, cách xử lý là điều chỉnh lại QoS của hiển thị hoặc subscriber thay vì khởi động lại lidar.

Về **durability**: `volatile` không lưu lại message cũ cho các node tham gia muộn, còn `transient_local` có giữ lại bản ghi gần nhất — nhờ đó bản đồ chỉ cần xuất bản một lần nhưng các node khởi động sau vẫn nhận được. Một publisher `volatile` sẽ không đáp ứng được subscriber yêu cầu `transient_local`.

Về **history depth**: đây là kích thước hàng đợi lưu message. Độ sâu bằng 1 nghĩa là chỉ giữ lại dữ liệu mới nhất — rất hợp lý với cảm biến lidar 10 Hz, nhưng không phù hợp cho một chuỗi lệnh ngắn liên tiếp nếu hệ thống không có cơ chế watchdog xử lý hết hạn.

Lệnh `ros2 topic info /scan -v` sẽ hiển thị song song hồ sơ QoS mà publisher cung cấp và subscriber yêu cầu. Nếu hai bên không tương thích, chúng sẽ không ghép nối với nhau và lệnh `echo` dùng QoS mặc định sẽ không in ra bất kỳ dữ liệu nào.

## Ví dụ làm từng bước

Tạo gói mới và tệp launch trong workspace đã nạp môi trường:

```bash
cd ~/ros2_ws/src
ros2 pkg create capstone_bringup --build-type ament_python --dependencies launch_ros
mkdir -p capstone_bringup/launch capstone_bringup/config
```

Tạo tệp `capstone_bringup/launch/talker_listener.launch.py`:

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

Quy tắc đóng gói: trong `setup.py`, danh sách `data_files` bắt buộc phải khai báo thư mục `launch`, nếu không `ros2 launch` sẽ không tìm thấy tệp sau khi chạy `colcon build`. Cú pháp tiêu chuẩn như sau:

```python
import os
from glob import glob
# bên trong data_files:
(os.path.join("share", package_name, "launch"), glob("launch/*.launch.py")),
```

Tiếp theo, biên dịch, nạp overlay và khởi chạy:

```bash
cd ~/ros2_ws
colcon build --packages-select capstone_bringup
source install/setup.bash
ros2 launch capstone_bringup talker_listener.launch.py
```

**Kết quả mong đợi:** trong cùng một terminal xuất hiện cả `Publishing: 'Hello World: N'` lẫn `I heard: [Hello World: N]`, và nhấn Ctrl-C sẽ dừng đồng thời cả hai node.

Kiểm tra tham số khi `talker` đang chạy:

```bash
ros2 param get /talker use_sim_time
```

**Kết quả mong đợi:** `Boolean value is: False`.

Thử nghiệm cố ý tạo lệch QoS: mở Terminal A và xuất bản theo chế độ `best_effort`:

```bash
ros2 topic pub /chatter std_msgs/msg/String "{data: hi}" --qos-reliability best_effort
```

Mở Terminal B và chạy `echo` với cấu hình mặc định (`reliable`):

```bash
ros2 topic echo /chatter
```

**Kết quả mong đợi:** phía publisher vẫn đếm số lần gửi nhưng phía `echo` hoàn toàn im lặng. Kiểm tra chi tiết bằng lệnh:

```bash
ros2 topic info /chatter -v
```

Bạn sẽ thấy reliability của publisher là `BEST_EFFORT`, của subscription là `RELIABLE`, và hai đầu không ghép nối được với nhau. Bây giờ chạy lại `echo` với chính sách khớp:

```bash
ros2 topic echo /chatter --qos-reliability best_effort
```

**Kết quả mong đợi:** chuỗi `data: hi` lập tức xuất hiện. Hãy ghi lại cặp lệnh này vào `lab-notes.md` để làm mẫu chẩn đoán cho tình huống "RViz không hiển thị dữ liệu quét laser" về sau.

### Giải thích: Ma trận tương thích QoS — Vì sao hai node cùng tên Topic nhưng KHÔNG nhận được tin?

Một lỗi "tàng hình" rất hay gặp trong ROS 2 là Publisher và Subscriber trùng tên topic 100%, không báo lỗi biên dịch, nhưng hoàn toàn không truyền tin cho nhau do **xung đột QoS Reliability**:

| Publisher (Bên phát) | Subscriber (Bên nhận) | Kết nối có khớp không? | Giải thích |
| :---: | :---: | :---: | :--- |
| `RELIABLE` | `RELIABLE` | **KHỚP** | Cả hai cam kết truyền tin cậy có gửi lại gói mất |
| `RELIABLE` | `BEST_EFFORT` | **KHỚP** | Bên phát cho chất lượng cao hơn mức bên nhận yêu cầu |
| `BEST_EFFORT` | `BEST_EFFORT` | **KHỚP** | Cả hai ưu tiên độ trễ thấp (chuẩn `SensorDataQoS` cho LiDAR/Camera) |
| **`BEST_EFFORT`** | **`RELIABLE`** | **KHÔNG KHỚP (TỊT!)** | Bên nhận đòi hỏi tin cậy tuyệt đối nhưng bên phát không đảm bảo → DDS từ chối ghép kênh! |

Mẹo chẩn đoán trong 3 giây: gõ `ros2 topic info /scan --verbose` để xem trực tiếp bảng QoS của cả Publisher và Subscriber!

## Lab

1. Biên dịch gói `capstone_bringup` và chạy tệp launch gồm `talker` và `listener`. Lưu lại đoạn log xác nhận `listener` đã nhận được dữ liệu từ `talker`.
2. Tạo tệp `capstone_bringup/config/bridge.yaml` chứa bốn khóa cấu hình như ở phần khái niệm (`port`, `baud`, `track_width`, `cmd_timeout_ms`). Ở bước này chưa cần node cầu nối; kiểm tra cú pháp YAML từ thư mục gói bằng lệnh `python3 -c "import yaml; print(yaml.safe_load(open('config/bridge.yaml')))"`. **Kết quả mong đợi:** một từ điển Python có khóa cấp cao nhất duy nhất là `capstone_bridge`, bên trong chứa `ros__parameters`.
3. Thực hiện thí nghiệm lệch QoS giữa `best_effort` và `reliable`. Ghi lại kết quả `ros2 topic info -v` cho cả trường hợp lỗi lẫn trường hợp đã sửa khớp.
4. *(Tùy chọn)* Chạy `ros2 topic hz /chatter` khi đang `echo`. Nếu không có cờ `--rate`, `ros2 topic pub` gửi khá chậm; hãy thêm `-r 10` và kiểm tra xem tần số đo được có gần 10 Hz hay không.

**Các lỗi thường gặp**

| Hiện tượng | Nguyên nhân thường gặp |
| --- | --- |
| Báo `file not found` khi chạy launch | Tệp `setup.py` chưa cài thư mục `launch/`, hoặc quên nạp lại overlay sau khi build |
| `listener` không in gì dù không lệch QoS | Khai báo nhầm thành hai node `talker`, hoặc `listener` bị thoát do sai kiểu parameter |
| Tệp YAML hợp lệ nhưng node bỏ qua `track_width` | Thiếu khóa `ros__parameters`, hoặc tên node trong YAML không khớp tên thực tế |
| `echo` chạy ở terminal này nhưng không chạy ở terminal kia | Một bên có truyền cờ `--qos-reliability` khác với mặc định |
| Đặt `use_sim_time` bằng `True` khiến node bị đứng về sau | Không có node nào xuất bản `/clock`; cần giữ `False` cho đến khi dùng Gazebo ở chương 10 |

## Mua ở Việt Nam

Bài thực hành này không cần linh kiện mới; laptop từ bài 09-01 là đủ. Nếu bạn đã chuẩn bị sẵn Raspberry Pi 5 cho robot, hãy hoàn thành bài lab trên laptop trước rồi mới lặp lại bước kiểm tra `printenv ROS_DISTRO` trên Pi, tránh phải gỡ đồng thời cả lỗi QoS lẫn sự cố thẻ nhớ microSD.

## Video tham khảo

- **Xem trước:** [ROS2 - Create a Launch File with Python](https://www.youtube.com/watch?v=xJ3WAs8GndA) — Robotics Back-End (tiếng Anh). Hướng dẫn viết tệp launch Python để khởi chạy nhiều node cùng lúc, tương ứng với cấu trúc trong bài.
- [ROS 2 on Two Computers: Connect Laptop and Robot with DDS + QoS | 08](https://www.youtube.com/watch?v=HEKwLJC5a2o) — Adaptive AgroTech (tiếng Anh). Giải thích cấu hình DDS, `ROS_DOMAIN_ID` và chính sách reliability của QoS khi kết nối hai máy tính trên cùng mạng.

## Bài tập

1. Tệp YAML của cầu nối đặt `cmd_timeout_ms: 300` và firmware trên MCU cũng có watchdog 300 ms. Nếu tiến trình trên laptop bị treo đột ngột nhưng cáp USB vẫn cắm, cơ chế nào sẽ dừng động cơ? *Gợi ý:* watchdog trên firmware. Timeout trong YAML chỉ giúp cầu nối quyết định chủ động *gửi* lệnh 0; khi cầu nối đã ngừng hoạt động thì nó không gửi được gì nữa, và bộ định thời trên MCU mới là lớp bảo vệ dừng bánh xe.
2. Một bạn cùng lớp xuất bản `/scan` ở chế độ `best_effort` nhưng mở RViz với cấu hình `reliable`. Thông tin nào trong `ros2 topic info -v` chứng minh ngay nguyên nhân? *Gợi ý:* publisher báo `BEST_EFFORT`, subscription báo `RELIABLE`, và hai đầu không kết nối được với nhau.
3. Vì sao chính sách `transient_local` phù hợp cho `/map` nhưng lại nguy hiểm nếu dùng cho `/cmd_vel`? *Gợi ý:* RViz mở sau vẫn cần nhận lại bản đồ mới nhất, nhưng cầu nối động cơ khởi động sau tuyệt đối không nên thực thi lại một lệnh vận tốc `Twist` từ mười phút trước.
4. Nếu bạn muốn tệp launch từ chối khởi chạy khi thiếu `track_width`, đây có phải vấn đề của QoS không? *Gợi ý:* không, đây là cơ chế khai báo parameter. Node cần khai báo bắt buộc `track_width` thay vì gán ngầm giá trị mặc định `1.0`, hoặc tệp launch phải truyền rõ tham số này.
5. Hãy xác định trong `capstone.launch.py` về sau (gồm cầu nối serial, `robot_state_publisher`, `teleop_twist_keyboard`), thông số nào bắt buộc phải đưa ra thành parameter thay vì ghi cứng? *Gợi ý:* cổng serial và chiều rộng trục bánh (`track_width`); riêng teleop chỉ xuất bản lệnh nên có thể khởi động sau.

## Đọc thêm

- [Launch nhiều node](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Launch/Launch-Main.html) và hướng dẫn [tạo file launch](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Launch/Creating-Launch-Files.html)
- [Tìm hiểu parameter](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Parameters/Understanding-ROS2-Parameters.html)
- [Về thiết lập Quality of Service](https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Quality-of-Service-Settings.html) — nên đọc kỹ bảng tương thích giữa các chính sách, không chỉ đọc tên.
- Chạy `ros2 topic echo -h` trực tiếp trên máy để xem đầy đủ các cờ QoS đã dùng trong bài lab.
