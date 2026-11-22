---
layout: post
title: "Capstone B: lab Nav2, sim rồi xe thật"
chapter: "11"
order: 7
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter11
lesson_type: required
draft: false
---

Thời lượng: **~120 phút** cho phần mô phỏng, thêm một buổi trên sàn nếu SLAM thật đã dựng được bản đồ không bị cong.

## Mục tiêu

Sau bài học này, bạn sẽ gửi được một mục tiêu điều hướng (goal) trong mô phỏng đang bật SLAM, quan sát `/cmd_vel` chuyển sang giá trị khác 0 và dừng hẳn khi hủy goal. Trên xe thật, bạn thực hiện tương tự với `navigation_launch.py` trong khi SLAM giữ cạnh `map → odom` (nhấc bánh khỏi mặt sàn ở lần thử đầu tiên) và lưu bản đồ bằng `map_saver_cli`. Trọng tâm là kiểm chứng toàn chuỗi hoạt động thay vì sa đà tinh chỉnh tham số MPPI khi lần gửi goal đầu gặp trục trặc.

## Kiến thức cần trước

Hoàn thành lab SLAM (11-06) với `/map` trong mô phỏng (hoặc log lỗi launch trên cùng máy đó) và bài tour Nav2 (11-02) để nắm rõ planner, controller cùng `Twist`. Firmware từ chương 07–08 vẫn phải đảm bảo tự đưa PWM về 0 khi `/cmd_vel` ngừng cập nhật.

## Vì sao bài này nằm trên lộ trình

Bản thân SLAM chỉ dựng bản đồ chứ không điều khiển xe di chuyển; Nav2 mới là tầng chuyển đổi một vị trí đích trên bản đồ thành lệnh `geometry_msgs/msg/Twist`. Xe Capstone chỉ thực thi đúng lệnh đó nếu cầu nối serial giữ đúng quy ước dấu. Bài lab này là lần đầu tiên goal điều hướng và cầu nối phần cứng phối hợp trực tiếp với nhau, nên bắt buộc nhấc bánh xe khỏi mặt sàn trong lần chạy thử đầu tiên.

## Khái niệm

Khi tách khỏi tệp launch gộp sẵn của TurtleBot3, hướng dẫn Nav2 trên Jazzy chia hệ thống thành ba phần riêng biệt: giao diện phần cứng robot, `navigation_launch.py` (không chạy kèm AMCL và map server vì SLAM đang cung cấp bản đồ) và `online_async_launch.py` của SLAM Toolbox. Trong mô phỏng, `tb3_simulation_launch.py slam:=True` đã gộp sẵn cả ba; còn trên xe thật bạn cần gọi riêng để tránh tình trạng AMCL và SLAM cùng tranh chấp cạnh `map → odom`.

Ngoài nút chọn trên RViz, bạn có thể gửi trực tiếp mục tiêu qua dòng lệnh:

```bash
ros2 topic pub /goal_pose geometry_msgs/msg/PoseStamped \
"{header: {stamp: {sec: 0}, frame_id: 'map'}, pose: {position: {x: 0.2, y: 0.0, z: 0.0}, orientation: {w: 1.0}}}"
```

Trong đó `frame_id` là `map`, `orientation: {w: 1.0}` biểu thị góc quay bằng 0, và $x = 0{,}2$ m là mục tiêu ngắn phù hợp cho lần thử đầu. Tùy cấu hình thời gian, dấu thời gian `sec: 0` có thể bị từ chối; khi đó hãy gửi lại bằng nút **Nav2 Goal** trên RViz sau khi kiểm tra đúng `use_sim_time` (`true` trong mô phỏng, `false` trên xe thật).

Theo dõi lệnh vận tốc trong lúc robot đang hướng về đích:

```bash
ros2 topic echo /cmd_vel
```

Bạn cần thấy `linear.x` hoặc `angular.z` khác 0 khi xe di chuyển và trở về gần 0 khi tới đích hoặc bị hủy. Trên xe thật, chỉ được có duy nhất một publisher điều khiển `/cmd_vel` đi vào cầu nối — nếu quên tắt node teleop bàn phím, cả teleop và Nav2 sẽ cùng tranh quyền lái.

Lưu bản đồ bằng lệnh tiêu chuẩn:

```bash
ros2 run nav2_map_server map_saver_cli -f ~/map
```

Tệp `.yaml` sinh ra sẽ trỏ tới ảnh `.pgm` tương ứng; trường `resolution` trong `.yaml` biểu thị kích thước mỗi ô lưới tính bằng mét (không tùy ý sửa giá trị này nếu chưa đo đạc đối chiếu thực tế).

Lưu ý rằng footprint mặc định của Nav2 không khớp chính xác kích thước khung xe Capstone, nên các mục tiêu sát cửa hẹp có thể bị từ chối. Chỉ nên tinh chỉnh tệp tham số sau khi đã chạy thành công một mục tiêu cơ bản ở khu vực trống.

## Lab

### An toàn

Luôn kiểm thử trong mô phỏng trước. Khi chuyển sang xe thật, giữ bánh nhấc khỏi mặt sàn cho đến khi xác nhận `/cmd_vel` về 0 lúc hủy goal; luôn giữ công tắc pin trong tầm tay, đặt giới hạn vận tốc ngay tại cầu nối (không chỉ phụ thuộc Nav2) và không đứng chắn trước mặt phẳng quét của lidar.

### Phần mô phỏng

1. Khởi chạy lại `tb3_simulation_launch.py slam:=True` với `TURTLEBOT3_MODEL=waffle` như ở bài 11-06.
2. Đặt một mục tiêu cách trước mặt robot khoảng 0,5 m trong RViz (hoặc gửi bằng `/goal_pose` nếu khoảng trống cho phép).
3. Chạy `ros2 topic echo /cmd_vel` và ghi lại khoảng mười dòng vào sổ (gồm cả dòng khác 0 khi đang chạy và dòng về 0 sau khi dừng).
4. Hủy goal hoặc đóng cửa sổ và xác nhận `cmd_vel` trở về 0; nếu vẫn có giá trị khác 0, dùng `ros2 topic info /cmd_vel -v` để tìm publisher còn sót lại.

### Phần xe thật

Nếu chưa có bản đồ thực tế, ghi chú kế hoạch hoãn có ngày cụ thể rồi dừng lại.

1. Nhấc bánh khỏi sàn, khởi chạy SLAM trực tuyến như bài 11-06, sau đó mở riêng tầng điều hướng:

```bash
ros2 launch nav2_bringup navigation_launch.py
```

Tuyệt đối không bật kèm AMCL; nếu tệp launch trên vô tình khởi động thêm map server chiếm `/map`, hãy dừng lại kiểm tra cấu hình vì SLAM phải là nguồn duy nhất phát `/map` và `map → odom`.

2. Theo dõi `ros2 topic echo /cmd_vel` khi gửi một goal ngắn: hai bánh (đang nhấc trên không) phải quay đúng chiều theo bài động học (lệnh tiến làm cả hai bánh quay về phía mũi xe).
3. Hủy goal và ghi rõ bánh dừng nhờ Nav2 gửi `0` hay nhờ watchdog trên firmware (hoặc cả hai).
4. Hạ xe xuống khoảng trống, gửi goal ngắn 0,3 m với một người túc trực sẵn ở công tắc nguồn; dừng ngay nếu xe đi sai hướng.
5. Lưu bản đồ bằng `map_saver_cli -f ~/capstone_nav_map` sau khi chạy chậm một vòng.

### Kết quả mong đợi

Sổ thực hành phần mô phỏng có mẫu log `/cmd_vel` thể hiện rõ trạng thái khác 0 khi chạy và về 0 khi dừng. Phần xe thật có kết quả tương ứng hoặc ghi chú hoãn có ngày, kèm tệp `.yaml` nếu đã lưu bản đồ.

### Lỗi thường gặp

| Hiện tượng | Hướng kiểm tra |
| --- | --- |
| Goal bị bỏ qua | `frame_id` không phải `map`, hoặc cây TF chưa có `map` |
| Costmap trống | Lệch QoS của `/scan` hoặc frame laser chưa nối tới `base_link` |
| Mô phỏng quay đúng nhưng xe thật quay ngược | Sai dấu trong cầu nối serial (không phải lỗi planner) |
| `/cmd_vel` không trở về 0 | Còn node teleop đang chạy song song; tắt node đó |
| Controller báo lỗi liên quan đến footprint | Thường gặp khi đặt goal quá sát tường; chọn goal ở khoảng trống trước khi sửa tham số |

## Video tham khảo

- **Xem trước:** [Making robot navigation easy with Nav2 and ROS!](https://www.youtube.com/watch?v=jkoGkAd0GYk) — Articulated Robotics (tiếng Anh). Minh họa gửi goal và bám quỹ đạo trong mô phỏng trước khi triển khai xuống xe thật.
- [ROS2 Nav2 - Generate a Map with slam_toolbox](https://www.youtube.com/watch?v=hMTxb8Y2cxI) — Robotics Back-End (tiếng Anh). Ôn lại bước dựng và lưu bản đồ nếu robot không phản hồi khi gửi goal.

## Bài tập

1. Vì sao bài lab cấm chạy AMCL cùng lúc với `slam_toolbox` (`online_async`)?
2. RViz vẽ ra tuyến đường dẫn nhưng `ros2 topic echo /cmd_vel` toàn số 0. Bạn nên kiểm tra gì tiếp theo?
3. Với watchdog 300 ms và tần số gửi `/cmd_vel` của Nav2 là mỗi 50 ms, watchdog có ngắt động cơ trong lúc xe đang bám goal không?
4. Tệp `.yaml` ghi `resolution: 0.05`. Một hành lang dài 2 m tương ứng bao nhiêu ô lưới nếu tỉ lệ bản đồ chính xác?
5. Trong lần đầu hạ bánh chạy tự hành trên sàn, vị trí đứng an toàn là ở đâu?

### Gợi ý đáp án

1. Cả hai đều xuất bản cạnh `map → odom`, gây xung đột vì mỗi cạnh TF chỉ được có một nguồn phát.
2. Kiểm tra tên topic và namespace mà cầu nối hoặc controller đang dùng bằng `ros2 topic info -v`.
3. Không, miễn là luồng lệnh cập nhật đều đặn mỗi 50 ms — watchdog chỉ kích hoạt khi mất tín hiệu quá 300 ms.
4. $2 / 0{,}05 = 40$ ô lưới theo chiều dài (nếu tỉ lệ odometry chuẩn).
5. Đứng sát công tắc ngắt nguồn pin của xe để kịp thời can thiệp, không ngồi cố định sau laptop.

## Đọc thêm

- [Nav2 với SLAM (Jazzy)](https://docs.nav2.org/jazzy/tutorials/general_tutorials/navigation2_with_slam/navigation2_with_slam/)
- [Tài liệu Nav2](https://docs.nav2.org/)
- [Twist trong Jazzy](https://docs.ros.org/en/jazzy/p/geometry_msgs/interfaces/msg/Twist.html)
- [Lab SLAM]({% multilang_post_url contents/chapter11/11_06_capstone_b_slam %})
