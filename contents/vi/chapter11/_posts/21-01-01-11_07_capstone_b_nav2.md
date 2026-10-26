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

Thời lượng: **~120 phút** trong sim, thêm một buổi trên sàn nếu SLAM thật đã có bản đồ không cong.

## Mục tiêu

Bạn gửi một goal trong mô phỏng đã bật SLAM và thấy `cmd_vel` khác không, rồi robot dừng khi bạn hủy goal. Trên xe, bạn làm cùng việc với `navigation_launch.py` trong lúc SLAM đang giữ `map` → `odom`, bánh nhấc ở lần đầu. Bạn lưu bản đồ bằng `map_saver_cli`. Bạn không chỉnh MPPI cả chiều chỉ vì goal đầu thất bại.

## Kiến thức cần trước

Lab SLAM (11-06) đã có `/map` trong sim, hoặc một log lỗi launch bạn sẽ dùng lại cùng máy này. Tour Nav2 (11-02) đã gọi tên planner, controller, và `Twist`. Firmware chương 07 và 08 vẫn đưa PWM về 0 khi `cmd_vel` im.

## Vì sao bài này nằm trên lộ trình

SLAM không làm xe đi. Nav2 là chỗ một pose trên bản đồ thành `geometry_msgs/msg/Twist`. Xe của bạn chỉ hiểu twist đó nếu cầu serial còn đúng dấu. Lab này là lần đầu goal và cầu đứng cạnh nhau. Lần đó bánh nhấc.

## Khái niệm

Tutorial Jazzy tách ba việc khi không dùng launch gộp của TurtleBot3: giao diện robot, `navigation_launch.py` (không kèm AMCL và map server, vì SLAM đang giữ bản đồ), và `online_async_launch.py`. Trên sim, `tb3_simulation_launch.py slam:=True` đã gộp chúng. Trên xe bạn gọi riêng, nếu không AMCL và SLAM cùng kể chuyện `map` → `odom`.

Goal trong tutorial, để bạn thấy CLI chứ không chỉ nút RViz:

```bash
ros2 topic pub /goal_pose geometry_msgs/msg/PoseStamped \
"{header: {stamp: {sec: 0}, frame_id: 'map'}, pose: {position: {x: 0.2, y: 0.0, z: 0.0}, orientation: {w: 1.0}}}"
```

`frame_id` là `map`. Orientation `w: 1` là quaternion không quay. $x = 0{,}2$ m là một goal ngắn, đúng để lần đầu. Stamp 0 có thể bị từ chối tùy cấu hình thời gian. Nếu controller bỏ qua goal, gửi lại từ nút Nav2 Goal trong RViz sau khi đã đặt `use_sim_time` đúng chỗ: true trong sim, false trên xe.

Trong lúc goal chạy:

```bash
ros2 topic echo /cmd_vel
```

Bạn cần thấy `linear.x` hoặc `angular.z` khác 0, rồi về gần 0 khi tới nơi hoặc khi bạn hủy. Trên xe, topic đó phải vào đúng một cầu. Hai publisher `cmd_vel` (teleop quên tắt, và Nav2) là hai người lái.

Lưu bản đồ, đúng lệnh tutorial:

```bash
ros2 run nav2_map_server map_saver_cli -f ~/map
```

File yaml trỏ tới pgm. Mở yaml và đọc `resolution`. Giá trị đó là mét mỗi ô. Đừng sửa cho "đẹp" nếu bạn chưa đo hành lang.

Footprint trong Nav2 mặc định không phải hình chữ nhật của xe bạn. Goal đâm vào cửa hẹp có thể là footprint khai to hơn xe. Việc đó đến sau khi một goal trên sàn trống đã chạy. Lab này không yêu cầu bạn viết file params hoàn chỉnh.

## Lab

### An toàn

Sim trước. Trên sàn: bánh nhấc cho đến khi `cmd_vel` về 0 khi bạn hủy goal. Công tắc pin trong tay. Tốc độ giới hạn ở cầu, không chỉ ở Nav2. Một người không đứng trước lidar.

### Phần sim

1. Chạy lại `tb3_simulation_launch.py slam:=True` như bài 11-06, model waffle.
2. Đặt goal khoảng 0,5 m phía trước trong RViz, hoặc dùng `goal_pose` ở trên nếu world còn chỗ.
3. Echo `/cmd_vel` mười dòng vào sổ. Ghi một dòng khác 0 và một dòng sau khi dừng.
4. Hủy goal hoặc đóng cửa sổ và xác nhận echo về 0. Nếu không về 0, bạn còn một publisher. `ros2 topic info /cmd_vel -v`.

### Phần thật

Chưa có bản đồ thật thì ghi hoãn có ngày và dừng. Đừng đưa waffle sim ra thảm.

1. Bánh nhấc. SLAM online như bài 11-06. Rồi:

```bash
ros2 launch nav2_bringup navigation_launch.py
```

Không chạy thêm AMCL. Nếu launch này cũng bật map server và giành `/map`, dừng và đọc file launch bạn vừa gọi. Tutorial giả định SLAM là nguồn duy nhất của `/map` và của `map` → `odom`.

2. Echo `/cmd_vel` trong khi gửi goal ngắn. Bánh trên không phải quay đúng dấu bài động học: tiến là cả hai bánh về mũi.
3. Hủy goal. Bánh dừng vì Nav2 gửi 0 hoặc vì watchdog firmware, bạn ghi là cái nào. Cả hai cùng đúng thì ghi cả hai.
4. Hạ bánh ở chỗ trống, goal 0,3 m, một người ở công tắc. Dừng nếu xe không đi hướng goal.
5. `map_saver_cli -f ~/capstone_nav_map` sau một vòng chậm.

### Kết quả mong đợi

Sổ sim có mười dòng echo hoặc một đoạn rút gọn trong đó có số khác 0 và số 0. Sổ thật có cùng việc hoặc giấy hoãn. Một file yaml nếu lưu được.

### Lỗi thường gặp

| Bạn thấy | Cần kiểm |
| --- | --- |
| Goal không được nhận | `frame_id` không phải `map`, hoặc TF `map` chưa có |
| Costmap trống | Scan QoS, hoặc laser frame không nối `base_link` |
| Xe quay đúng trong sim, quay ngược trên sàn | Dấu cầu serial, không phải dấu planner |
| `cmd_vel` không về 0 | Teleop còn publish. Tắt node đó |
| Controller báo footprint | Bình thường với goal sát tường. Đưa goal ra chỗ trống trước khi sửa params |

## Bài tập

1. Vì sao lab cấm chạy AMCL trong lúc `online_async` đang chạy?
2. Echo toàn 0 nhưng RViz vẽ một đường. Bạn kiểm topic nào kế tiếp?
3. Watchdog 300 ms và Nav2 gửi `cmd_vel` mỗi 50 ms. Watchdog có cắt bánh khi goal đang chạy không?
4. `resolution: 0.05` trong yaml. Một hành lang dài 2 m trên giấy là bao nhiêu ô, nếu bản đồ không bị co?
5. Lần hạ bánh đầu bạn đứng ở đâu?

### Gợi ý đáp án

1. Cả hai muốn publish `map` → `odom`. Cây TF không có hai chủ một cạnh. 2. Đúng tên topic cầu đang subscribe. Có thể là `/cmd_vel` khác namespace. `ros2 topic info -v`. 3. Không, nếu bản tin còn đều. Watchdog chỉ thấy im lặng. 4. $2 / 0{,}05 = 40$ ô theo chiều dài, nếu tỉ lệ encoder đúng. 5. Cạnh công tắc pin, không phải sau laptop.

## Đọc thêm

- [Nav2 với SLAM (Jazzy)](https://docs.nav2.org/jazzy/tutorials/general_tutorials/navigation2_with_slam/navigation2_with_slam/)
- [Tài liệu Nav2](https://docs.nav2.org/)
- [Twist trong Jazzy](https://docs.ros.org/en/jazzy/p/geometry_msgs/interfaces/msg/Twist.html)
- [Lab SLAM]({% multilang_post_url contents/chapter11/11_06_capstone_b_slam %})
