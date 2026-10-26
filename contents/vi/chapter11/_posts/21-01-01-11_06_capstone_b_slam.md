---
layout: post
title: "Capstone B: lab SLAM, sim rồi lidar thật"
chapter: "11"
order: 6
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter11
lesson_type: required
draft: false
---

Thời lượng: **~150 phút** cho phần mô phỏng, thêm một buổi nếu lidar và xe đã ở trên sàn. Lần đầu trên sàn bánh có thể nhấc khi bạn chỉ kiểm `/scan`.

## Mục tiêu

Bạn chạy SLAM Toolbox trong mô phỏng TurtleBot3 theo đúng tutorial Nav2 cho Jazzy, rồi lặp lại trên xe của bạn với LD06 hoặc RPLIDAR A1. Bạn chứng minh `/scan` là `sensor_msgs/msg/LaserScan`, cây TF có cạnh tới frame của tia, và `map` → `odom` do SLAM publish. Chưa có lidar thì phần sim vẫn phải xong, phần sàn là giấy hoãn có ngày.

## Kiến thức cần trước

Bài tổng quan SLAM (11-01) và tour Nav2 (11-02). Chương 10 đã có một world Harmonic và một `cmd_vel` có dấu đúng. Odometry chương 08 không còn đảo bánh. Trên máy: `printenv ROS_DISTRO` là `jazzy`.

## Vì sao bài này nằm trên lộ trình

Capstone A chứng minh xe chạy khi bạn gửi vận tốc. Capstone B chứng minh xe biết mình đang ở đâu đủ để một goal có nghĩa. Policy chương 12 không thay bản đồ này. Làm sim trước để khi bản đồ thật cong, bạn còn một lần chạy đúng để so.

![Ba bước: sim, lidar, Nav2]({{ site.imgurl }}/generated/ch11_capstone_b.png)

## Khái niệm

`slam_toolbox` cần một `LaserScan` và một odometry không nhảy. Nó publish `/map` và transform `map` → `odom`. Robot, hoặc Gazebo, publish `odom` → `base_link`. URDF publish `base_link` → frame laser. Thiếu một cạnh thì các tia vẽ ở gốc tọa độ.

Gói cài trên Jazzy, đúng câu trong [tutorial Nav2 với SLAM](https://docs.nav2.org/jazzy/tutorials/general_tutorials/navigation2_with_slam/navigation2_with_slam/):

```bash
sudo apt install ros-jazzy-slam-toolbox ros-jazzy-nav2-bringup \
  ros-jazzy-turtlebot3 ros-jazzy-turtlebot3-msgs ros-jazzy-turtlebot3-bringup
```

Tutorial đó dùng `TURTLEBOT3_MODEL=waffle` và

```bash
source /opt/ros/jazzy/setup.bash
export TURTLEBOT3_MODEL=waffle
ros2 launch nav2_bringup tb3_simulation_launch.py slam:=True
```

Một lệnh này là phần sim của lab: bringup, Nav2, và SLAM. Nếu launch báo lỗi Gazebo, dán nguyên dòng đầu tiên vào sổ. Đừng cài thêm `gazebo` Classic để "cho có". Chương 10 đã chọn Harmonic. Tutorial Jazzy là nguồn sự thật của lệnh. Máy không chịu world thì cửa sim đạt bằng log lỗi gốc cộng câu bạn sẽ chạy lại trên máy khác, không đạt bằng cách bỏ qua.

Trên xe thật, đừng copy `use_sim_time:=true`. Đồng hồ là đồng hồ tường. Launch SLAM riêng, sau khi `/scan` và TF đã sống:

```bash
ros2 launch slam_toolbox online_async_launch.py
```

Hai lidar rẻ mà khóa này chấp nhận. Giá để trống đến khi bạn mở listing.

**LD06** (cùng họ LD19 trong repo chính thức của LDRobot). README [ldlidar_stl_ros2](https://github.com/ldrobotSensorTeam/ldlidar_stl_ros2) build workspace rồi:

```bash
ros2 launch ldlidar_stl_ros2 ld06.launch.py
```

File launch đặt `topic_name` là `scan`, `frame_id` là `base_laser`, baud **230400**, và một TF tĩnh `base_link` → `base_laser` với `z = 0.18`. Con số 0,18 m là ví dụ của hãng, không phải xe bạn. Sửa `arguments` của `static_transform_publisher` trong `ld06.launch.py` thành mét bạn đo: trước tâm bao nhiêu, cao bao nhiêu. README còn bảo `chmod 777` cổng serial. Khóa này dùng nhóm `dialout` và udev, như bài Linux chương 09. Chỉ `chmod` tạm trên cổng bạn vừa `ls` nếu bạn chưa có rule, rồi ghi vào sổ là tạm.

**RPLIDAR A1.** Repo [Slamtec rplidar_ros nhánh `ros2`](https://github.com/Slamtec/rplidar_ros):

```bash
git clone -b ros2 https://github.com/Slamtec/rplidar_ros.git
```

Build bằng `colcon` sau khi source Jazzy. README liệt kê Humble và các distro cũ hơn, không liệt kê Jazzy. Nếu build fail, dán lỗi và dừng. Đừng vá API trong lab này. Lệnh xem A1 mà README ghi là:

```bash
ros2 launch rplidar_ros view_rplidar_a1_launch.py
```

Lệnh đó mở cả RViz. Frame phải được broadcast. Ảnh trục trong repo (`rplidar-frame.png`) là hướng quét. README có script udev. Đường dẫn trong README gõ nhầm `rpldiar_ros`. Hãy mở thư mục `scripts/` của bản bạn clone và chạy script có thật ở đó.

`ros2 topic echo /scan --once` phải có `angle_min`, `angle_increment`, và một mảng `ranges`. Một số `inf` là hết tầm, không phải driver chết. Toàn `inf` hoặc toàn `0` thì mới là chết: cáp, baud, hoặc frame bị che.

## Lab

### An toàn

Sim không có pin. Trên sàn, lần kiểm `/scan` đầu tiên để bánh nhấc hoặc để VM ngắt. Người đứng cạnh công tắc khi bánh hạ và khi bạn đẩy xe để quét. Lidar quay: tóc, dây, và mắt không vào mặt phẳng tia. Nhìn tem công suất. Đừng nhìn vào cửa sổ laser.

### Các bước, phần sim

1. Cài các gói ở trên. Ghi phiên bản `ros-jazzy-slam-toolbox` bằng `apt-cache policy` nếu bạn muốn một dòng bằng chứng.
2. Chạy launch `slam:=True` với `TURTLEBOT3_MODEL=waffle`.
3. Đưa robot đi một vòng ngắn trong world (Nav2 goal hoặc teleop mà launch đã mở). Ảnh `/map` trong RViz, hoặc `ros2 topic echo /map --once` cho thấy `width` khác 0.
4. Lưu:

```bash
ros2 run nav2_map_server map_saver_cli -f ~/tb3_map
```

Sổ ghi đường dẫn `~/tb3_map.yaml` và `~/tb3_map.pgm` nếu lệnh thành công.

### Các bước, phần thật

Bỏ qua cả khối nếu chưa có lidar. Viết `hoãn SLAM thật, ngày, lý do`.

1. Gắn lidar, đo $x$ và $z$ tới `base_link`, sửa TF. `ros2 run tf2_ros tf2_echo base_link base_laser` (LD06) hoặc frame mà driver A1 đang dùng. Tên phải trùng `frame_id` trong `/scan`.
2. `ros2 topic echo /scan --once`. Dán `angle_min`, `angle_max`, `frame_id`.
3. Odometry vẫn publish `odom` → `base_link`. `use_sim_time` không được true. Kiểm `ros2 param get` trên node odom của bạn, hoặc nhìn launch.
4. `ros2 launch slam_toolbox online_async_launch.py`. Đẩy xe chậm một vòng hành lang. Ảnh bản đồ. Nếu hành lang cong trong khi xe đi thẳng, dừng SLAM và sửa dấu encoder trước.
5. `map_saver_cli -f ~/capstone_map`.

### Kết quả mong đợi

Phần sim: một file yaml hoặc một log lỗi launch nguyên văn. Phần thật: ảnh bản đồ, hoặc giấy hoãn. TF và `/scan` cùng `frame_id`.

### Lỗi thường gặp

| Bạn thấy | Cần kiểm |
| --- | --- |
| Tia nằm một đống ở gốc RViz | Không có TF từ `frame_id` lên `base_link` |
| Bản đồ xoắn khi đi thẳng | Dấu encoder, trái/phải, hoặc trượt một bánh |
| `/scan` im | Sai baud LD06 (230400), sai cổng, hoặc rule udev |
| SLAM không ra `map` → `odom` | Đang chạy AMCL cùng lúc và giành cạnh. Tắt AMCL khi đang map |
| `use_sim_time` trên xe | Các stamp không khớp đồng hồ tường. Tắt |

## Bài tập

1. LD06 để `z = 0.18` trong khi lidar của bạn cao 0,06 m. Triệu chứng trên bản đồ là gì?
2. Vì sao `chmod 777` không được ghi là cách làm mặc định của khóa?
3. `ranges` toàn 0. Bạn kiểm baud hay kiểm TF trước?
4. Sim đạt, xe chưa có lidar. Checklist chương 11 còn cửa nào mở?
5. Hai node cùng publish `odom` → `base_link`. Bạn tắt cái nào trước khi chỉnh tham số solver?

### Gợi ý đáp án

1. Tia cắt tường ở sai độ cao, bản đồ thủng hoặc thấy mặt bàn. Sửa mét trong launch. 2. Quyền rộng cho mọi user trên cổng. Dùng `dialout`. 3. Baud và cổng trước. TF sai vẫn có số khoảng cách, chỉ vẽ sai chỗ. Toàn 0 là chưa có mẫu. 4. Cửa SLAM thật, với giấy hoãn có ngày thì cửa đó đóng theo đường hoãn. 5. Tắt publisher thừa. Hai nguồn trên một cạnh không phải chuyện tham số SLAM.

## Đọc thêm

- [Nav2: Navigating while Mapping (Jazzy)](https://docs.nav2.org/jazzy/tutorials/general_tutorials/navigation2_with_slam/navigation2_with_slam/)
- [slam_toolbox](https://github.com/SteveMacenski/slam_toolbox)
- [ldlidar_stl_ros2](https://github.com/ldrobotSensorTeam/ldlidar_stl_ros2)
- [rplidar_ros nhánh ros2](https://github.com/Slamtec/rplidar_ros)
- [Trang A1 của Slamtec](https://www.slamtec.com/en/Lidar/A1)
