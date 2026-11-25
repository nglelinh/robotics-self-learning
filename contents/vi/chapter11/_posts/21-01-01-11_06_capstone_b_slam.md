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

Thời lượng: **~150 phút** cho phần mô phỏng, cộng thêm một buổi nếu đã có sẵn lidar và xe trên sàn (trong lần kiểm tra `/scan` đầu tiên trên xe thật, có thể nhấc bánh xe khỏi sàn).

Mọi mảnh ghép từ Chương 08 đến Bài 11-01 hội tụ tại đây: lần đầu tiên chiếc xe Capstone của bạn tự chạy quanh một không gian chưa biết (trong Gazebo hoặc phòng lab thật), quét LiDAR liên tục và **tự dựng nên tấm bản đồ 2D hoàn chỉnh** bằng `slam_toolbox`. Đây là bài kiểm chứng khắt khe nhất cho chất lượng odometry, cây TF2 và cách lái thu thập dữ liệu của bạn.

## Kiến thức cần nhớ: Ba trụ cột Thực chiến Dựng bản đồ SLAM (Capstone B)

1. **Chuỗi Dữ liệu Đầu vào Sạch (`/scan` + `/odom` + `/tf`)**:
   `slam_toolbox` yêu cầu tia `/scan` gắn đúng khung `laser_frame` đã nối vào `base_link`, odometry không bị ngược dấu $$\omega$$ và đồng bộ thời gian chuẩn (`use_sim_time`).
2. **Chiến lược Lái tạo Đóng vòng lặp (Loop-Closure Driving Pattern)**:
   Lái chậm và đều ($$v \le 0{,}25\text{ m/s}$$, $$\omega \le 0{,}5\text{ rad/s}$$), tránh xoay giật cục tại chỗ, và luôn chủ động lái quay lại ít nhất một đoạn hành lang cũ để kích hoạt tối ưu hóa đồ thị tư thế.
3. **Lưu trữ & Kiểm định Bản đồ (`map_saver_cli`)**:
   Xuất cặp tệp `map.pgm` (ảnh xám lưới chiếm dụng) + `map.yaml` (độ phân giải `resolution`, gốc tọa độ `origin` và ngưỡng chiếm dụng) và đối chiếu kích thước phòng đo trên bản đồ với thước dây thực tế.

## Mục tiêu

Sau bài học này, bạn sẽ chạy thành công SLAM Toolbox trong mô phỏng TurtleBot3 theo đúng hướng dẫn Nav2 cho Jazzy, rồi áp dụng quy trình tương tự lên xe thật dùng cảm biến LD06 hoặc RPLIDAR A1. Bạn sẽ xác minh `/scan` có kiểu `sensor_msgs/msg/LaserScan`, cây TF đầy đủ cạnh tới frame laser và cạnh `map → odom` do SLAM xuất bản. Nếu chưa có lidar thật, bạn vẫn bắt buộc hoàn thành phần mô phỏng và ghi chú kế hoạch hoãn có ngày cụ thể cho phần cứng.

## Kiến thức cần trước

Hoàn thành bài tổng quan SLAM (11-01) và tour Nav2 (11-02). Chương 10 đã có world Gazebo Harmonic chạy ổn định cùng lệnh `/cmd_vel` đúng dấu; odometry chương 08 đã kiểm tra không đảo chiều bánh; `printenv ROS_DISTRO` trả về `jazzy`.

## Vì sao bài này nằm trên lộ trình

Capstone A chứng minh xe di chuyển chính xác theo lệnh vận tốc, còn Capstone B chứng minh xe biết định vị bản thân trong không gian để các mục tiêu điều hướng có ý nghĩa. Các mô hình học máy ở chương 12 không thay thế được bản đồ này. Việc chạy thông suốt phần mô phỏng trước giúp bạn có một chuẩn đối chiếu tin cậy mỗi khi bản đồ thực tế bị méo.

![Ba bước: sim, lidar, Nav2]({{ site.imgurl }}/generated/ch11_capstone_b.png)

## Khái niệm

`slam_toolbox` yêu cầu hai đầu vào cốt lõi: dữ liệu `LaserScan` và odometry liên tục (không nhảy gián đoạn). Nó xuất bản bản đồ `/map` cùng phép biến đổi `map → odom`; robot (hoặc Gazebo) xuất bản `odom → base_link`; còn URDF xuất bản phép biến đổi tĩnh `base_link → khung laser`. Thiếu bất kỳ cạnh nào, toàn bộ tia quét sẽ dồn về gốc tọa độ.

Cài đặt các gói cho Jazzy theo [tutorial Nav2 với SLAM](https://docs.nav2.org/jazzy/tutorials/general_tutorials/navigation2_with_slam/navigation2_with_slam/):

```bash
sudo apt install ros-jazzy-slam-toolbox ros-jazzy-nav2-bringup \
  ros-jazzy-turtlebot3 ros-jazzy-turtlebot3-msgs ros-jazzy-turtlebot3-bringup
```

Chạy mô phỏng với biến môi trường `TURTLEBOT3_MODEL=waffle`:

```bash
source /opt/ros/jazzy/setup.bash
export TURTLEBOT3_MODEL=waffle
ros2 launch nav2_bringup tb3_simulation_launch.py slam:=True
```

Câu lệnh này khởi chạy trọn bộ mô phỏng gồm bringup, Nav2 và SLAM. Nếu gặp lỗi liên quan đến Gazebo, dán nguyên văn dòng lỗi đầu tiên vào sổ — tuyệt đối không cài thêm bản `gazebo` Classic vì lộ trình chương 10 đã thống nhất dùng Harmonic. Trường hợp phần cứng máy tính không đủ tải world 3D, bạn có thể hoàn thành bước mô phỏng bằng log lỗi gốc kèm kế hoạch chạy lại trên máy khác thay vì bỏ qua.

Trên robot thật, tuyệt đối không sao chép `use_sim_time:=true` (hệ thống phải dùng đồng hồ thực). Sau khi `/scan` và cây TF đã hoạt động, khởi chạy riêng SLAM Toolbox:

```bash
ros2 launch slam_toolbox online_async_launch.py
```

Hai dòng lidar phổ thông phù hợp cho bài thực hành (tự tra giá hiện tại khi mua):

**LD06** (cùng họ LD19 trong kho mã nguồn chính thức của LDRobot). Biên dịch workspace theo hướng dẫn [ldlidar_stl_ros2](https://github.com/ldrobotSensorTeam/ldlidar_stl_ros2) rồi chạy:

```bash
ros2 launch ldlidar_stl_ros2 ld06.launch.py
```

Tệp launch mặc định đặt `topic_name` là `scan`, `frame_id` là `base_laser`, tốc độ baud **230400**, và một phép biến đổi tĩnh `base_link → base_laser` với `z = 0.18`. Giá trị 0,18 m chỉ là ví dụ của hãng — bạn phải chỉnh lại `arguments` của `static_transform_publisher` trong `ld06.launch.py` theo kích thước đo thực tế (tính bằng mét) trên xe mình. Ngoài ra, dù README đề cập `chmod 777` cho cổng serial, khóa học thống nhất dùng nhóm `dialout` và luật `udev` như bài Linux chương 09 (chỉ dùng `chmod` tạm thời trên đúng cổng đã kiểm tra nếu chưa kịp tạo rule và ghi chú rõ trong sổ).

**RPLIDAR A1.** Lấy mã nguồn từ [Slamtec rplidar_ros nhánh `ros2`](https://github.com/Slamtec/rplidar_ros):

```bash
git clone -b ros2 https://github.com/Slamtec/rplidar_ros.git
```

Biên dịch bằng `colcon` sau khi đã nạp Jazzy. Lưu ý README gốc liệt kê đến Humble chứ chưa ghi chính thức Jazzy; nếu quá trình biên dịch phát sinh lỗi API, hãy dán log lỗi và dừng lại (không tự sửa API trong bài lab này). Lệnh khởi chạy kèm RViz theo README:

```bash
ros2 launch rplidar_ros view_rplidar_a1_launch.py
```

Kiểm tra ảnh hướng trục quét (`rplidar-frame.png`) trong kho mã nguồn và đảm bảo frame laser được phát lên TF. Lưu ý README có lỗi chính tả `rpldiar_ros` ở đường dẫn script `udev`, nên hãy mở trực tiếp thư mục `scripts/` trong bản bạn vừa clone để chạy đúng tệp.

Kiểm tra dữ liệu quét bằng `ros2 topic echo /scan --once`: message hợp lệ phải có `angle_min`, `angle_increment` và mảng `ranges`. Việc xuất hiện một số giá trị `inf` là bình thường (tia vượt quá tầm đo tối đa); ngược lại, nếu toàn bộ mảng là `inf` hoặc toàn `0` thì cần kiểm tra lại cáp, tốc độ baud hoặc xem cửa sổ quét có bị che chắn không.

### Giải thích: Đọc nhanh tệp `map.yaml` và kiểm tra sai số tỉ lệ bản đồ bằng tay

Sau khi lưu bản đồ bằng `map_saver_cli`, bạn nhận được `lab_map.pgm` (kích thước `400 × 300 pixel`) và `lab_map.yaml` với `resolution: 0.05` (mỗi pixel = `5 cm`):
- Chiều rộng vật lý của vùng bản đồ: $$400 \times 0{,}05 = \mathbf{20{,}0\text{ m}}$$.
- Nếu bạn đo hành lang phòng lab ngoài đời rộng **3,00 m**, thì khoảng cách giữa hai vạch tường đen trên ảnh `.pgm` phải là $$\frac{3{,}00}{0{,}05} = \mathbf{60\text{ pixel}}$$.
- **Chẩn đoán lỗi tức thì:** Nếu hai bức tường song song bị vẽ *chập thành hai đường chéo lệch nhau* (double walls), nguyên nhân thường là: (1) ngược dấu $$\omega$$ trong odometry, (2) sai góc lắp `laser_frame` trong URDF, hoặc (3) lái xoay quá nhanh vượt tần số quét LiDAR!

## Lab

### An toàn

Phần mô phỏng không dùng pin. Khi thử trên xe thật, lần kiểm tra `/scan` đầu tiên cần nhấc bánh khỏi sàn hoặc ngắt nguồn động cơ VM; khi hạ bánh và đẩy xe quét bản đồ, luôn có người sẵn sàng ở công tắc nguồn. Lidar có phần quay cơ học và phát tia laser — giữ tóc, dây điện tránh xa bộ phận quay và không nhìn thẳng vào cửa sổ phát tia.

### Các bước thực hiện — phần mô phỏng

1. Cài đặt đầy đủ các gói ở trên (có thể ghi lại phiên bản `ros-jazzy-slam-toolbox` bằng `apt-cache policy` làm minh chứng).
2. Khởi chạy `tb3_simulation_launch.py slam:=True` với `TURTLEBOT3_MODEL=waffle`.
3. Điều khiển robot chạy một vòng ngắn trong môi trường mô phỏng (qua mục tiêu Nav2 hoặc teleop đi kèm), sau đó chụp ảnh `/map` trong RViz hoặc kiểm tra `ros2 topic echo /map --once` thấy `width` khác 0.
4. Lưu bản đồ:

```bash
ros2 run nav2_map_server map_saver_cli -f ~/tb3_map
```

Ghi lại đường dẫn hai tệp `~/tb3_map.yaml` và `~/tb3_map.pgm` vào sổ khi lệnh thành công.

### Các bước thực hiện — phần phần cứng thật

Nếu chưa có lidar, bỏ qua mục này và ghi rõ vào sổ: `hoãn SLAM thật, ngày, lý do`.

1. Lắp lidar lên khung xe, đo chính xác tọa độ $x$ và $z$ so với `base_link`, cập nhật TF và kiểm tra bằng `ros2 run tf2_ros tf2_echo base_link base_laser` (với LD06) hoặc tên frame của driver A1; tên này phải khớp hoàn toàn với `frame_id` trong `/scan`.
2. Chạy `ros2 topic echo /scan --once` và dán các trường `angle_min`, `angle_max`, `frame_id` vào sổ.
3. Đảm bảo node odometry đang xuất bản `odom → base_link` và không bật `use_sim_time:=true` (kiểm tra bằng `ros2 param get` hoặc xem tệp launch).
4. Khởi chạy `ros2 launch slam_toolbox online_async_launch.py`, đẩy chậm xe đi một vòng hành lang và chụp ảnh bản đồ. Nếu hành lang thẳng nhưng bản đồ bị cong, dừng SLAM ngay để sửa dấu encoder trước.
5. Lưu bản đồ bằng `map_saver_cli -f ~/capstone_map`.

### Kết quả mong đợi

Phần mô phỏng: tệp bản đồ `.yaml`/`.pgm` đã lưu (hoặc log lỗi launch nguyên văn nếu máy không tải được Gazebo). Phần phần cứng thật: ảnh bản đồ thực tế hoặc ghi chú hoãn có ngày. Tên `frame_id` trong `/scan` khớp với cây TF.

### Lỗi thường gặp

| Hiện tượng | Hướng kiểm tra |
| --- | --- |
| Các tia quét dồn thành một cụm tại gốc RViz | Thiếu cạnh TF nối `frame_id` của laser với `base_link` |
| Bản đồ bị xoắn cong khi đẩy xe đi thẳng | Ngược dấu encoder, đảo trái/phải, hoặc một bánh bị trượt |
| Topic `/scan` không có dữ liệu | Sai tốc độ baud (LD06 dùng 230400), sai cổng serial hoặc lỗi luật `udev` |
| SLAM không xuất bản `map → odom` | Đang chạy đồng thời AMCL gây xung đột cạnh; tắt AMCL khi đang dựng bản đồ |
| Bật nhầm `use_sim_time` trên xe thật | Dấu thời gian không khớp đồng hồ thực; tắt `use_sim_time` |

## Video tham khảo

- **Xem trước:** [Easy SLAM with ROS using slam_toolbox](https://www.youtube.com/watch?v=ZaiA3hWaRzE) — Articulated Robotics (tiếng Anh). Hướng dẫn dùng `slam_toolbox` dựng bản đồ từ `/scan` (giữ đúng tên gói `apt` của Jazzy như trong bài).
- [ROS2 Nav2 - Generate a Map with slam_toolbox](https://www.youtube.com/watch?v=hMTxb8Y2cxI) — Robotics Back-End (tiếng Anh). Quy trình lưu bản đồ bằng `map_saver` sau khi chạy một vòng, khớp với bước cuối phần mô phỏng.

## Bài tập

1. Nếu tệp launch LD06 để mặc định `z = 0.18` trong khi lidar trên xe thực tế chỉ cao 0,06 m, hiện tượng sai lệch nào có thể xuất hiện trên bản đồ?
2. Vì sao khóa học không chọn `chmod 777` làm cách phân quyền cổng serial mặc định?
3. Khi mảng `ranges` trả về toàn giá trị `0`, bạn nên kiểm tra tốc độ baud hay cây TF trước?
4. Nếu phần mô phỏng đã đạt nhưng xe chưa có lidar, tiêu chí nào trong checklist chương 11 vẫn đang chờ xử lý?
5. Khi có hai node cùng xuất bản cạnh `odom → base_link`, bạn cần xử lý gì trước khi nghĩ đến việc tinh chỉnh tham số bộ giải (solver) của SLAM?

### Gợi ý đáp án

1. Mặt phẳng tia quét bị khai báo sai độ cao, có thể khiến bản đồ nhận nhầm mép bàn hoặc thiếu chi tiết tường; cần sửa lại đúng số đo mét trong tệp launch.
2. `chmod 777` cấp quyền đọc/ghi cho mọi người dùng trên hệ thống; chuẩn an toàn hơn là thêm user vào nhóm `dialout` kết hợp luật `udev`.
3. Kiểm tra baud và cổng serial trước: sai TF vẫn có dữ liệu khoảng cách (chỉ vẽ sai vị trí), còn toàn `0` chứng tỏ chưa đọc được mẫu hợp lệ từ phần cứng.
4. Tiêu chí SLAM trên phần cứng thật (có thể đóng tạm bằng ghi chú hoãn có ngày cụ thể).
5. Tắt ngay publisher bị trùng lặp — xung đột hai nguồn phát trên cùng một cạnh TF không thể khắc phục bằng tham số SLAM.

## Đọc thêm

- [Nav2: Navigating while Mapping (Jazzy)](https://docs.nav2.org/jazzy/tutorials/general_tutorials/navigation2_with_slam/navigation2_with_slam/)
- [slam_toolbox](https://github.com/SteveMacenski/slam_toolbox)
- [ldlidar_stl_ros2](https://github.com/ldrobotSensorTeam/ldlidar_stl_ros2)
- [rplidar_ros nhánh ros2](https://github.com/Slamtec/rplidar_ros)
- [Trang A1 của Slamtec](https://www.slamtec.com/en/Lidar/A1)
