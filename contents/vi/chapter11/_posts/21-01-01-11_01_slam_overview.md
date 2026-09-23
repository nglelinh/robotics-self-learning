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

Thời lượng ước tính: khoảng 70 phút nếu máy đã source ROS 2 Jazzy, hoặc khoảng 50 phút nếu bạn dừng ở bản hợp đồng giao diện vì trên bàn không có lidar.

## Mục tiêu học

Bạn vẽ được chuỗi ba cạnh TF mà `slam_toolbox` cần, gọi tên topic phải có trước `online_async_launch.py`, phân biệt hành lang cong vì encoder với hành lang chưa được quét, và nói vì sao TF-Luna không điền được `sensor_msgs/msg/LaserScan`.

## Kiến thức cần có

Bạn dùng được `ros2 topic info` và biết cây TF là các khung có tên. Từ đế Capstone, encoder tạo odometry, và một dấu dây sai khiến lệnh đi thẳng trông như lệnh quay. Gazebo ở đây chỉ là hình dung một laser giả lập.

## Vì sao bài này nằm trên lộ trình

Lộ trình đi từ đế vi sai Capstone, qua ROS 2 Jazzy, qua Gazebo, rồi mới tới tự hành. Bản đồ là sản phẩm tự hành đầu tiên không phải lệnh động cơ. `slam_toolbox` vừa ước lượng chỗ robot đứng, vừa ghi tường, khi đã có lidar mặt phẳng. Gazebo phát được scan giả. Capstone thì không. Chưa có `LaserScan` thật và odometry trung thực thì launch mapper chỉ báo thiếu giao diện. Nav2 sẽ dùng bản đồ này, không vẽ hộ bạn.

## Khái niệm

SLAM trong bài này là định vị và dựng bản đồ cùng lúc trên mặt phẳng. Lidar đo khoảng cách theo nhiều phương. Odometry bánh xe nói robot nghĩ mình đã dịch chuyển bao nhiêu giữa hai lần quét. Bộ dựng bản đồ ghép các scan thành lưới, đồng thời công bố một hiệu chỉnh để bản đồ không xoắn dần vì sai số encoder.

![SLAM mặt phẳng: một vòng quét lidar dựng bản đồ, biến đổi map tới odom kéo lại độ trôi của bánh xe]({{ site.imgurl }}/generated/ch11_slam.png)

[REP-105](https://www.ros.org/reps/rep-0105.html) tách ba khung. `map` được phép nhảy khi khép vòng. `odom`, tích phân từ bánh xe, được phép trôi nhưng không được nhảy, kẻo bộ điều khiển bám nó sẽ giật. `base_link` là thân. Trong môn này SLAM công bố `map` tới `odom`, robot công bố `odom` tới `base_link` từ odometry, và URDF công bố `base_link` tới khung laser là biến đổi tĩnh. Driver lidar không bịa giá đỡ.

Hợp lại, tư thế thân trong bản đồ là

$$
T_{\mathrm{map}\rightarrow\mathrm{base}} = T_{\mathrm{map}\rightarrow\mathrm{odom}} \, T_{\mathrm{odom}\rightarrow\mathrm{base}}.
$$

Nếu biến đổi ở giữa là nói dối, biến đổi bên trái không cứu được bản đồ. Xét một lỗi dấu cụ thể. Khoảng cách hai bánh $$b = 0{,}20$$ m. Cả hai bánh thực sự lăn tới một mét, robot đi thẳng. Encoder bánh phải bị ngược dấu, nên node odometry thấy $$\Delta s_l = 1{,}0$$ m và $$\Delta s_r = -1{,}0$$ m. Mô hình vi sai thông thường:

$$
\Delta s = \frac{\Delta s_r + \Delta s_l}{2}, \qquad \Delta \theta = \frac{\Delta s_r - \Delta s_l}{b}.
$$

Thay số được $$\Delta s = 0$$ và $$\Delta \theta = -10$$ rad. Robot đã đi dọc hành lang. Odometry bảo nó đứng yên và quay. Khớp scan kéo bức tường theo cú quay ma đó, hành lang trên bản đồ bị bẻ cong. Sửa dấu encoder, hoặc sửa việc gán nhầm trái phải, trước khi đụng tham số SLAM. Lỗi tỉ lệ trông khác: cả hai bánh cùng lớn hơn một hệ số thì hành lang vẫn thẳng nhưng dài hơn thực tế, không cong như quả chuối.

`sensor_msgs/msg/LaserScan` mang `angle_min`, `angle_max`, `angle_increment`, các giới hạn tầm, mảng `ranges`, và `frame_id` đã có trong TF. Lidar 360 độ bước nửa độ có cỡ 720 khoảng cách. TF-Luna có một khoảng cách trên một tia. Nó báo cản va. Nó không nuôi được `slam_toolbox`.

MPU6050 có thể giúp bộ lọc giữ yaw giữa các lần quét. Nó vẫn không vẽ tường. Driver lidar thường phát best effort. Subscriber đòi reliable sẽ ngồi im. Đọc trang QoS của Jazzy khi `ros2 topic echo` có mẫu mà mapper vẫn bảo không thấy gì.

## Ví dụ làm từng bước

Cài gói Jazzy, source distro, và xem dòng launch mà môn này coi là hình dạng lệnh:

```bash
sudo apt install ros-jazzy-slam-toolbox
source /opt/ros/jazzy/setup.bash
ros2 launch slam_toolbox online_async_launch.py
```

Launch đó mở mapper online async với tham số mặc định. Không có `/scan` và TF thì không có bản đồ. Thiếu topic scan, thiếu `odom` tới `base_link`, hoặc thiếu khung laser nghĩa là giao diện vắng mặt. Dừng node. Đừng bịa scan.

Trước khi launch trên bất kỳ robot nào, kể cả lần bringup Capstone sau này, ba lệnh kiểm tra khô là:

```bash
source /opt/ros/jazzy/setup.bash
ros2 topic info /scan -v
ros2 topic info /odom -v
ros2 run tf2_ros tf2_echo odom base_link
```

`/scan` phải là `sensor_msgs/msg/LaserScan` với publisher count ít nhất một. `/odom` phải là `nav_msgs/msg/Odometry`, `frame_id` là `odom`, `child_frame_id` là `base_link`. Đẩy robot tới thì đổi tịnh tiến, xoay tại chỗ thì đổi yaw. Khi đó launch mới có cơ hội. SLAM khỏe thì thêm `map` tới `odom` (`ros2 run tf2_ros tf2_echo map odom`). Echo đó là kết quả, không phải biến đổi bạn tự công bố.

## Lab

Lab này là hợp đồng giao diện, không phải cuộc thi dựng bản đồ. Chép danh sách sau vào vở và đánh dấu từng dòng: có, không có, hoặc không thể với cảm biến bạn đang sở hữu.

1. `/scan` tồn tại, kiểu `sensor_msgs/msg/LaserScan`, `frame_id` là khung laser, và `ranges` phủ một quạt phẳng rộng chứ không phải một số.
2. `/odom` tồn tại, kiểu `nav_msgs/msg/Odometry`, và một cú đẩy thẳng làm `x` tăng mà không bịa một yaw lớn.
3. TF có `odom` tới `base_link` từ robot, và `base_link` tới khung laser là giá đỡ tĩnh. `map` tới `odom` để dành cho SLAM.
4. Nếu ranger duy nhất là TF-Luna, viết câu "cảm biến này không nuôi được slam_toolbox" rồi dừng. Đừng launch mapper rồi gọi cửa sổ trống là bản đồ.

Chạy kế hoạch khô cả khi bạn đoán trước là thất bại:

```bash
source /opt/ros/jazzy/setup.bash
ros2 topic info /scan -v
ros2 topic info /odom -v
```

Kết quả mong đợi khi không có ai đang phát, và đó là kết quả trung thực trên máy không có driver lidar:

```text
Unknown topic '/scan'
Unknown topic '/odom'
```

Ghi lại đúng chữ đó. Cả hai publisher vắng mặt, nên launch không phải demo hỏng. Nếu driver hoặc bag đang chạy, dán khối chữ ghi kiểu bản tin và publisher count cạnh dòng hợp đồng tương ứng.

| Bạn thấy | Nguyên nhân hay gặp | Việc cần kiểm |
| --- | --- | --- |
| Hành lang cong như quả chuối | Dấu encoder một bánh ngược, hoặc trái phải bị tráo | Đi thẳng, xem yaw trong `/odom` |
| Hành lang thẳng nhưng sai độ dài | Bán kính bánh hoặc khoảng cách hai bánh | So một mét trên sàn với `x` của odom |
| Launch in lỗi TF, bản đồ trống | Không có `/scan`, không có `odom` tới `base_link`, hoặc thiếu khung laser | Ba lệnh ở trên |
| Echo có scan nhưng SLAM im | Subscriber reliable, publisher best effort | `ros2 topic info /scan -v` |
| "Lidar" chỉ là một khoảng cách | TF-Luna hoặc ToF một điểm | Không nối vào `slam_toolbox` |

## Mua linh kiện ở Việt Nam

Chỉ mua máy quét khi bạn sẵn sàng dựng bản đồ. Lidar mặt phẳng cỡ sinh viên, loại LD19, LD06, YDLIDAR X2, gần đây thường nằm khoảng 1,5 đến 3,5 triệu đồng. Tìm trên Shopee bằng từ khóa `lidar LD19 robot`, tự đọc listing mới nhất, và ưu tiên hàng có giao thức serial được mô tả hơn board bí ẩn. Đó là món mua đầu nếu bạn mua.

[RPLIDAR S2 trên Hshop](https://hshop.vn/cam-bien-khoang-cach-dtof-lidar-rplidar-s2m1-r2e-30m-360-laser-range-scanner) là bước nâng cấp đắt: 360 độ, nối kiểu Ethernet, tầm xa hơn. Xem lại giá. Không phải món đầu của sinh viên.

Máy tính chạy mapper là Raspberry Pi 5. [Trang Pi 5 của Hshop](https://hshop.vn/may-tinh-raspberry-pi-5-made-in-uk) từng gần 2,4 triệu đồng cho bản RAM thấp. Xem lại. Pi không thay lidar. Mở [trang TF-Luna](https://hshop.vn/cam-bien-khoang-cach-dfrobot-tf-luna-tof-micro-single-point-ranging-lidar) và đọc chữ single-point: hữu ích làm cản va, sai cho bài này. [MPU6050](https://hshop.vn/cam-bien-6-dof-bac-tu-do-gy-521-mpu6050) là tùy chọn cho bộ lọc sau, không thay laser, và không cần cho lab hợp đồng.

## Bài tập

### Bài 1

Vẽ cây TF của robot đang dựng bản đồ một hành lang thẳng. Ghi ai công bố từng cạnh: SLAM, odometry bánh xe, hay URDF tĩnh.

**Gợi ý.** Ba cạnh là đủ: `map` tới `odom`, `odom` tới `base_link`, `base_link` tới khung laser. Nếu thêm cạnh thứ tư, nói vì sao nó tĩnh.

### Bài 2

Với số ở mục khái niệm, tính lại $$\Delta s$$ và $$\Delta \theta$$ khi encoder phải đúng còn encoder trái bị ngược dấu. Yaw ma đổi chiều hay không?

**Gợi ý.** Giữ $$b = 0{,}20$$ m. Chỉ $$\Delta s_l$$ đổi dấu so với số đã làm. Không cần robot.

### Bài 3

Viết hợp đồng `/scan` bạn giao cho người chỉ có TF-Luna. Gồm kiểu bản tin, `ranges` phải chứa gì, và câu từ chối rõ.

**Gợi ý.** Một đoạn ngắn. Nêu `sensor_msgs/msg/LaserScan`. Một số thực không phải mảng các phương.

### Bài 4

Đẩy thẳng một mét làm `x` của odometry tăng khoảng một mét và yaw đổi dưới một độ. Hành lang trên bản đồ vẫn cong. Nhìn chỗ nào tiếp, và không nhìn chỗ nào?

**Gợi ý.** Odometry đã trung thực thì nghi ngờ yaw của giá laser và TF. Đừng bắt đầu bằng việc mua IMU.

### Bài 5

Viết đúng các lệnh `ros2 topic info` bạn sẽ chạy trước `online_async_launch.py`, và nói publisher count bằng 0 nghĩa là gì với lần launch đó.

**Gợi ý.** Hai lệnh, `/scan` và `/odom`, có `-v`. Publisher count bằng 0 nghĩa là launch không có gì để ghép, nên bạn dừng.

## Đọc thêm

- [slam_toolbox](https://github.com/SteveMacenski/slam_toolbox) mô tả launch online async và giả định về scan cùng odometry.
- [REP-105](https://www.ros.org/reps/rep-0105.html) định nghĩa `map`, `odom`, và `base_link`.
- [Quality of service trên Jazzy](https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Quality-of-Service-Settings.html) giải thích subscriber reliable bỏ lỡ scan best effort.
- [Trang TF-Luna](https://hshop.vn/cam-bien-khoang-cach-dfrobot-tf-luna-tof-micro-single-point-ranging-lidar) ghi single-point ngay trên tên hàng.
