---
layout: post
title: "Tổng quan SLAM cho người mới"
chapter: "11"
order: 1
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter11
lesson_type: required
draft: false
---

Thời lượng ước tính: **~70 phút** nếu máy đã cài và nạp sẵn ROS 2 Jazzy, hoặc khoảng 50 phút nếu bạn dừng ở bước kiểm tra giao diện do chưa có lidar thật trên bàn.

## Mục tiêu học

Sau bài học này, bạn sẽ vẽ được chuỗi ba cạnh TF mà `slam_toolbox` yêu cầu, liệt kê đúng các topic phải tồn tại trước khi chạy `online_async_launch.py`, phân biệt được bản đồ hành lang bị cong do lỗi encoder với khu vực chưa được quét, và giải thích rõ vì sao cảm biến đơn điểm TF-Luna không thể cung cấp dữ liệu `sensor_msgs/msg/LaserScan`.

## Kiến thức cần có

Bạn sử dụng thành thạo `ros2 topic info` và nắm rõ cấu trúc cây tọa độ TF. Từ phần thực hành xe Capstone, bạn hiểu cách encoder tạo ra odometry và biết rằng chỉ cần một dấu dây bị đảo ngược là lệnh đi thẳng sẽ bị hiểu nhầm thành lệnh quay. Trong bài này, Gazebo chỉ đóng vai trò minh họa nguồn dữ liệu laser giả lập.

## Vì sao bài này nằm trên lộ trình

Lộ trình của khóa đi tuần tự từ khung xe vi sai Capstone, lên ROS 2 Jazzy, qua mô phỏng Gazebo rồi mới đến tự hành. Bản đồ là sản phẩm tự hành đầu tiên vượt ra ngoài việc gửi lệnh trực tiếp tới động cơ. Khi có dữ liệu lidar phẳng 2D, `slam_toolbox` vừa ước lượng vị trí robot vừa dựng bản đồ tường xung quanh. Gazebo có thể tạo luồng quét giả lập, còn xe Capstone cơ bản thì chưa có; nếu thiếu `LaserScan` hợp lệ và odometry chính xác, việc khởi chạy bộ dựng bản đồ chỉ báo thiếu giao diện. Nav2 ở bài sau sẽ dựa trên bản đồ này để dẫn đường chứ không tự vẽ bản đồ.

## Khái niệm

SLAM (Simultaneous Localization and Mapping) trong phạm vi bài này là bài toán định vị và dựng bản đồ đồng thời trên mặt phẳng 2D. Lidar đo khoảng cách theo nhiều góc quét quanh robot, còn odometry bánh xe ước lượng độ dịch chuyển của robot giữa hai khung quét liên tiếp. Bộ dựng bản đồ sẽ ghép các khung quét thành bản đồ lưới, đồng thời xuất bản phép hiệu chỉnh để bản đồ không bị méo dần do sai số tích lũy của encoder.

![SLAM mặt phẳng: một vòng quét lidar dựng bản đồ, biến đổi map tới odom kéo lại độ trôi của bánh xe]({{ site.imgurl }}/generated/ch11_slam.png)

Chuẩn [REP-105](https://www.ros.org/reps/rep-0105.html) tách biệt ba hệ tọa độ chính: `map` được phép nhảy đột ngột khi khép vòng (loop closure) để hiệu chỉnh sai số; `odom` (tích phân từ bánh xe) được phép trôi dần nhưng không được nhảy gián đoạn để tránh làm giật bộ điều khiển bám quỹ đạo; `base_link` gắn cố định vào thân xe. Trong kiến trúc này, SLAM xuất bản `map → odom`, odometry của robot xuất bản `odom → base_link`, còn URDF xuất bản phép biến đổi tĩnh `base_link → khung laser` (driver lidar không tự định nghĩa vị trí giá đỡ).

Tổng hợp lại, tư thế của thân robot trong hệ tọa độ bản đồ là:

$$
T_{\mathrm{map}\rightarrow\mathrm{base}} = T_{\mathrm{map}\rightarrow\mathrm{odom}} \, T_{\mathrm{odom}\rightarrow\mathrm{base}}.
$$

Nếu phép biến đổi ở giữa (`odom → base_link`) bị sai lệch nghiêm trọng, phép hiệu chỉnh từ bản đồ khó có thể cứu vãn. Xét một ví dụ lỗi ngược dấu: giả sử khoảng cách hai bánh $$b = 0{,}20$$ m, robot đi thẳng 1 m nhưng encoder bánh phải bị ngược dấu, khiến node odometry đọc được $$\Delta s_l = 1{,}0$$ m và $$\Delta s_r = -1{,}0$$ m. Theo mô hình vi sai tiêu chuẩn:

$$
\Delta s = \frac{\Delta s_r + \Delta s_l}{2}, \qquad \Delta \theta = \frac{\Delta s_r - \Delta s_l}{b}.
$$

Thay số ta thu được $$\Delta s = 0$$ và $$\Delta \theta = -10$$ rad: robot thực tế đã đi thẳng dọc hành lang, nhưng odometry lại báo nó đang đứng yên xoay tại chỗ. Thuật toán ghép quét sẽ kéo bức tường xoay theo góc quay ảo này, khiến hành lang trên bản đồ bị uốn cong. Do đó luôn phải kiểm tra và sửa dấu encoder (hoặc thứ tự trái/phải) trước khi tinh chỉnh tham số SLAM. Ngược lại, lỗi hệ số tỉ lệ (cả hai bánh cùng sai một hệ số nhân) tạo ra biểu hiện khác: hành lang vẫn thẳng nhưng chiều dài trên bản đồ bị kéo giãn hoặc co ngắn so với thực tế.

Message `sensor_msgs/msg/LaserScan` chứa các trường `angle_min`, `angle_max`, `angle_increment`, giới hạn tầm đo, mảng khoảng cách `ranges` và `frame_id` đã khai báo trên cây TF. Một cảm biến lidar 360° với độ phân giải góc 0,5° cung cấp khoảng 720 điểm đo mỗi vòng quét. Trong khi đó, TF-Luna chỉ đo duy nhất một khoảng cách dọc một tia — phù hợp để phát hiện vật cản phía trước, nhưng không thể cấp dữ liệu đầu vào cho `slam_toolbox`.

Cảm biến quán tính MPU6050 có thể hỗ trợ bộ lọc giữ ổn định góc yaw giữa các khung quét, nhưng không thể tự vẽ tường. Ngoài ra, driver lidar thường xuất bản theo chính sách QoS `best_effort`; nếu subscriber yêu cầu `reliable`, hai bên sẽ không ghép nối được — hãy kiểm tra lại cấu hình QoS của Jazzy khi `ros2 topic echo` vẫn có dữ liệu nhưng bộ dựng bản đồ không nhận được gì.

## Ví dụ làm từng bước

Cài gói `slam_toolbox` trên Jazzy, nạp môi trường và nắm cú pháp khởi chạy chuẩn:

```bash
sudo apt install ros-jazzy-slam-toolbox
source /opt/ros/jazzy/setup.bash
ros2 launch slam_toolbox online_async_launch.py
```

Lệnh này mở bộ dựng bản đồ ở chế độ trực tuyến bất đồng bộ (online async) với tham số mặc định. Nếu chưa có `/scan` và cây TF hoàn chỉnh thì hệ thống không thể tạo bản đồ; khi thiếu `/scan`, thiếu `odom → base_link` hoặc thiếu frame laser, hãy dừng node thay vì tạo dữ liệu giả.

Trước khi khởi chạy SLAM trên bất kỳ robot nào (kể cả khi tích hợp Capstone về sau), luôn thực hiện ba lệnh kiểm tra đầu vào:

```bash
source /opt/ros/jazzy/setup.bash
ros2 topic info /scan -v
ros2 topic info /odom -v
ros2 run tf2_ros tf2_echo odom base_link
```

Topic `/scan` phải có kiểu `sensor_msgs/msg/LaserScan` với ít nhất một publisher. Topic `/odom` phải có kiểu `nav_msgs/msg/Odometry` với `frame_id` là `odom` và `child_frame_id` là `base_link`; khi đẩy thẳng robot, tọa độ tịnh tiến phải tăng tương ứng, còn khi xoay tại chỗ góc yaw phải thay đổi đúng chiều. Khi các điều kiện này thỏa mãn và SLAM hoạt động bình thường, chính SLAM sẽ tự động xuất bản thêm cạnh `map → odom` (kiểm tra bằng `ros2 run tf2_ros tf2_echo map odom` — đây là đầu ra của SLAM, không phải cạnh bạn tự phát tĩnh).

## Lab

Bài thực hành này tập trung vào kiểm tra giao ước đầu vào thay vì chạy đua dựng bản đồ. Chép danh sách sau vào sổ thực hành và đánh dấu từng mục theo tình trạng thực tế (**có**, **chưa có**, hoặc **không khả thi với cảm biến hiện tại**):

1. `/scan` tồn tại với kiểu `sensor_msgs/msg/LaserScan`, `frame_id` khớp frame laser và mảng `ranges` quét theo một góc rộng chứ không chỉ một điểm.
2. `/odom` tồn tại với kiểu `nav_msgs/msg/Odometry`; khi đẩy thẳng robot, tọa độ `x` tăng lên mà không xuất hiện góc yaw ảo lớn.
3. Cây TF có cạnh `odom → base_link` từ robot và cạnh tĩnh `base_link → laser` từ URDF; cạnh `map → odom` để trống cho SLAM đảm nhiệm.
4. Nếu cảm biến đo khoảng cách duy nhất bạn có là TF-Luna, ghi rõ "cảm biến này không thể cấp dữ liệu cho `slam_toolbox`" rồi dừng lại, không chạy bộ dựng bản đồ trên cửa sổ trống.

Thực hiện kiểm tra giao diện ngay cả khi bạn biết trước chưa có cảm biến chạy:

```bash
source /opt/ros/jazzy/setup.bash
ros2 topic info /scan -v
ros2 topic info /odom -v
```

Kết quả mong đợi (và trung thực) trên máy chưa chạy driver lidar hoặc bag:

```text
Unknown topic '/scan'
Unknown topic '/odom'
```

Ghi nguyên văn kết quả này vào sổ để xác nhận cả hai publisher đang vắng mặt. Nếu bạn đang chạy driver hoặc phát lại tệp bag, dán đầy đủ phần kiểu message và số lượng publisher vào cạnh từng mục tương ứng.

| Hiện tượng | Nguyên nhân thường gặp | Hướng kiểm tra |
| --- | --- | --- |
| Hành lang trên bản đồ bị uốn cong | Ngược dấu encoder một bánh hoặc đấu nhầm trái/phải | Đẩy thẳng xe và quan sát góc yaw trong `/odom` |
| Hành lang thẳng nhưng sai chiều dài | Sai bán kính bánh hoặc khoảng cách hai bánh | Đẩy xe đúng 1 m ngoài sàn và đối chiếu với `x` của `/odom` |
| Launch báo lỗi TF, bản đồ trống | Thiếu `/scan`, thiếu `odom → base_link`, hoặc thiếu frame laser | Chạy lại ba lệnh kiểm tra đầu vào ở trên |
| `echo` thấy dữ liệu quét nhưng SLAM không nhận | Lệch QoS (subscriber `reliable`, publisher `best_effort`) | Kiểm tra bằng `ros2 topic info /scan -v` |
| Cảm biến chỉ trả về một giá trị khoảng cách | Đang dùng TF-Luna hoặc cảm biến ToF đơn điểm | Không dùng làm đầu vào cho `slam_toolbox` |

## Mua linh kiện ở Việt Nam

Chỉ nên mua cảm biến quét khi bạn sẵn sàng thực hành dựng bản đồ. Các dòng lidar 2D phổ thông phù hợp sinh viên như LD19, LD06 hoặc YDLIDAR X2 có giá tham khảo khoảng 1,5–3,5 triệu đồng (tìm từ khóa `lidar LD19 robot` trên Shopee, đọc kỹ mô tả mới nhất và ưu tiên loại có tài liệu giao thức serial rõ ràng).

Dòng [RPLIDAR S2 trên Hshop](https://hshop.vn/cam-bien-khoang-cach-dtof-lidar-rplidar-s2m1-r2e-30m-360-laser-range-scanner) là phương án nâng cấp cao cấp hơn (quét 360°, kết nối Ethernet, tầm đo xa) nhưng giá thành cao, không phù hợp làm lựa chọn khởi đầu.

Máy tính chạy thuật toán dựng bản đồ trên xe là Raspberry Pi 5 ([Trang Pi 5 của Hshop](https://hshop.vn/may-tinh-raspberry-pi-5-made-in-uk), giá tham khảo gần 2,4 triệu đồng cho bản RAM thấp — kiểm tra lại giá hiện tại), nhưng Pi không thể thay thế cảm biến lidar. Tham khảo [trang TF-Luna](https://hshop.vn/cam-bien-khoang-cach-dfrobot-tf-luna-tof-micro-single-point-ranging-lidar) để thấy rõ đặc tính đơn điểm (*single-point* — chỉ phù hợp tránh va chạm, không dùng cho SLAM). Cảm biến [MPU6050](https://hshop.vn/cam-bien-6-dof-bac-tu-do-gy-521-mpu6050) chỉ là tùy chọn hỗ trợ bộ lọc về sau, không thay thế lidar và chưa cần cho bài lab kiểm tra giao diện này.

## Video tham khảo

- **Xem trước:** [SLAM - 5 Minutes with Cyrill](https://www.youtube.com/watch?v=BuRCJ2fegcc) — Cyrill Stachniss (tiếng Anh). Tóm tắt nguyên lý cốt lõi của SLAM (vừa định vị vừa dựng bản đồ) trong 5 phút.
- [SLAM Robot Mapping - Computerphile](https://www.youtube.com/watch?v=-XU54IsG8Vo) — Computerphile (tiếng Anh). Giải thích trực quan lý do robot cần tự dựng bản đồ khi hoạt động trong môi trường chưa biết trước (không phụ thuộc phiên bản ROS).

## Bài tập

### Bài 1

Vẽ cây TF của một robot đang dựng bản đồ dọc hành lang thẳng và ghi rõ thành phần nào chịu trách nhiệm xuất bản từng cạnh (SLAM, odometry bánh xe hay URDF tĩnh).

**Gợi ý.** Tối thiểu cần ba cạnh: `map → odom`, `odom → base_link`, và `base_link → khung laser`; nếu thêm cạnh thứ tư, giải thích vì sao đó là biến đổi tĩnh.

### Bài 2

Dùng lại số liệu ở mục Khái niệm, tính lại $$\Delta s$$ và $$\Delta \theta$$ trong trường hợp encoder bánh phải đúng chiều còn encoder bánh trái bị ngược dấu. Góc yaw ảo có đổi chiều không?

**Gợi ý.** Giữ nguyên $$b = 0{,}20$$ m, chỉ đảo dấu $$\Delta s_l$$ so với phép tính mẫu.

### Bài 3

Viết một đoạn mô tả ngắn về giao ước đầu vào `/scan` dành cho người chỉ có cảm biến TF-Luna, gồm tên kiểu message, yêu cầu của mảng `ranges` và lý do từ chối.

**Gợi ý.** Nêu rõ kiểu `sensor_msgs/msg/LaserScan` yêu cầu một mảng khoảng cách theo nhiều góc quét, không thể thay bằng một số thực đơn lẻ.

### Bài 4

Khi đẩy thẳng robot 1 m, giá trị `x` của odometry tăng khoảng 1 m và góc yaw lệch dưới 1°, nhưng hành lang trên bản đồ SLAM vẫn bị cong. Bạn cần kiểm tra yếu tố nào tiếp theo và không nên vội làm gì?

**Gợi ý.** Khi odometry đã chính xác, hãy kiểm tra góc lắp (yaw) của lidar và phép biến đổi TF tĩnh `base_link → laser` thay vì vội mua thêm IMU.

### Bài 5

Viết đầy đủ các lệnh `ros2 topic info` cần chạy trước khi khởi động `online_async_launch.py` và giải thích ý nghĩa khi `Publisher count` bằng 0.

**Gợi ý.** Hai lệnh kiểm tra `/scan` và `/odom` kèm cờ `-v`; `Publisher count: 0` đồng nghĩa không có dữ liệu đầu vào để ghép bản đồ nên cần dừng trước khi launch.

## Đọc thêm

- [slam_toolbox](https://github.com/SteveMacenski/slam_toolbox) — tài liệu về chế độ `online_async` và các yêu cầu đối với dữ liệu quét cùng odometry.
- [REP-105](https://www.ros.org/reps/rep-0105.html) — quy chuẩn định nghĩa `map`, `odom` và `base_link`.
- [Quality of service trên Jazzy](https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Quality-of-Service-Settings.html) — giải thích sự không tương thích giữa subscriber `reliable` và publisher `best_effort`.
- [Trang TF-Luna](https://hshop.vn/cam-bien-khoang-cach-dfrobot-tf-luna-tof-micro-single-point-ranging-lidar) — thông số kỹ thuật xác nhận đây là cảm biến đo đơn điểm.
