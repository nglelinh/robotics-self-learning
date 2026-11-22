---
layout: post
title: "Bring-up URDF trong mô phỏng"
chapter: "10"
order: 2
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter10
lesson_type: required
draft: false
---

Thời lượng: **~90 phút**.

## Mục tiêu

Sau bài học này, bạn sẽ đưa được mô hình `xacro` từ chương 09 vào một world Gazebo Harmonic đang chạy theo đúng trình tự: biên dịch `xacro` ra URDF, khởi chạy `robot_state_publisher`, mở `empty.sdf -r`, spawn mô hình bằng `ros_gz_sim create`, rồi bắc cầu `/clock` một chiều và `/cmd_vel` hai chiều. Bạn sẽ cấu hình tên khớp bánh xe, khoảng cách hai bánh (0,16 m) và bán kính bánh (0,033 m) trong plugin diff-drive khớp hoàn toàn với tệp `xacro`, sau đó gửi một lệnh `Twist` chậm để quan sát bánh xe lăn trực tiếp trong Gazebo. Đồng thời, bạn nắm được năm lỗi bring-up phổ biến (khiến RViz vẫn hiển thị bình thường nhưng robot trong mô phỏng đứng yên hoặc rơi xuyên sàn) và biết đồng bộ `use_sim_time` với `/clock` để timer và TF dùng chung một mốc thời gian.

## Kiến thức cần trước

Hoàn thành bài 10-01: world trống chạy ổn định và `gz topic -l` hiển thị `/clock`. Tệp `xacro` từ bài 09-06 đã sẵn sàng với thân hộp, hai bánh trụ, khớp `continuous` và đầy đủ thẻ `<inertial>`. Nắm lại phép động học nghịch ở bài 08-04 để hiểu ý nghĩa của `cmd_vel` ($$v$$ tiến và $$\omega$$ quay quanh $$+z$$). Mọi cửa sổ terminal mới đều phải nạp Jazzy; RViz chỉ là tùy chọn vì tiêu chí đạt yêu cầu nằm ở chuyển động thực tế trong Gazebo.

## Vì sao bài này nằm trên lộ trình

Ở chương 09, `xacro` mới chỉ cung cấp bản vẽ hình học và cây TF tĩnh; sang Harmonic, mô hình lần đầu tiên có khối lượng, va chạm vật lý và đồng hồ mô phỏng. Về sau, Nav2 sẽ xuất bản `geometry_msgs/Twist` lên `/cmd_vel`: trong mô phỏng, bộ nhận lệnh là plugin diff-drive của Gazebo, còn trên xe Capstone thật là cầu nối serial ở bài 10-04. Nếu thông số khoảng cách hai bánh hoặc bán kính trong plugin lệch với `xacro`, mọi dữ liệu bag ghi lại sau này đều bị sai tỉ lệ. Ngoài ra, thứ tự khởi chạy các tiến trình là kỹ năng cốt lõi vì việc bật ngược trình tự thường tạo ra hiện tượng giống hệt lỗi vật lý.

![Thứ tự từ xacro tới mô hình lăn trong Harmonic]({{ site.imgurl }}/generated/ch10_sim_bringup.png)

## Khái niệm

Bring-up là một quy trình theo đúng trình tự, không phải một câu lệnh đơn lẻ.

**Bước 1: Tạo mô tả URDF.** Công cụ `xacro` khai triển các thuộc tính thành tệp URDF chuẩn để cả `robot_state_publisher` lẫn công cụ spawn đọc được. Mô hình khóa học gồm thân hộp, hai bánh trụ với khớp `continuous` tên `left_wheel_joint` và `right_wheel_joint`, kèm thẻ `<inertial>` trên mọi link có va chạm. Hai kích thước chuẩn là khoảng cách hai bánh 0,16 m và bán kính bánh 0,033 m; các giá trị này phải đồng bộ giữa `xacro` và plugin để hình dáng hiển thị khớp với động học lăn.

**Bước 2: Chạy `robot_state_publisher`.** Node này xuất bản cây TF từ URDF (các khớp cố định vẫn hiển thị dù `joint_states` chưa có dữ liệu). Trong môi trường mô phỏng, node này cần sử dụng đồng hồ Gazebo sau khi `/clock` đã được bắc cầu, tránh tình trạng dấu thời gian lệch pha so với dữ liệu cảm biến và odometry thêm vào sau này.

**Bước 3: Mở world mô phỏng.** Khởi chạy `empty.sdf` kèm cờ `-r` để server chạy ngay thay vì tạm dừng. Tên nội bộ của world trong tệp này là `empty`.

**Bước 4: Spawn mô hình.** Công cụ `create` đưa tệp URDF vào world đang chạy, trong đó tham số `-world` phải khớp chính xác tên world:

```bash
ros2 run ros_gz_sim create -world empty -file /tmp/capstone.urdf -name capstone
```

Nếu truyền `-world shapes` khi server đang chạy `empty.sdf`, lệnh sẽ báo lỗi không tìm thấy world. Tham số `-file` yêu cầu tệp URDF đã khai triển chứ không nhận trực tiếp tệp `.xacro` thô, còn `-name capstone` là tên mô hình hiển thị trong giao diện Gazebo.

**Bước 5: Bắc cầu topic.** Nếu cần kiểm tra lại ký hiệu chiều truyền từ bài 10-01, chạy:

```bash
ros2 run ros_gz_bridge parameter_bridge -h
```

Đồng hồ chỉ đi một chiều từ Gazebo sang ROS (dùng ký hiệu `[` giữa kiểu ROS và kiểu Gazebo):

```bash
ros2 run ros_gz_bridge parameter_bridge /clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock
```

Lệnh vận tốc dùng dạng hai chiều (`@`) để `Twist` phát từ ROS đi tới plugin và dữ liệu từ phía Gazebo cũng phản hồi được về ROS:

```bash
ros2 run ros_gz_bridge parameter_bridge /cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist
```

Bạn có thể truyền cả hai đối số vào chung một tiến trình `parameter_bridge`. Không bao giờ dùng cầu nối hai chiều cho `/clock` để tránh tình trạng một node ROS khác phát đè mốc thời gian lên đồng hồ của Gazebo.

Để chuyển đổi `/cmd_vel` thành chuyển động quay của bánh xe trong Gazebo Sim, ta thêm khối plugin `DiffDrive` vào tệp `xacro` với các thông số khớp hoàn toàn với thuộc tính mô hình:

```xml
<gazebo>
  <plugin filename="gz-sim-diff-drive-system" name="gz::sim::systems::DiffDrive">
    <left_joint>left_wheel_joint</left_joint>
    <right_joint>right_wheel_joint</right_joint>
    <wheel_separation>0.16</wheel_separation>
    <wheel_radius>0.033</wheel_radius>
    <max_linear_velocity>0.5</max_linear_velocity>
  </plugin>
</gazebo>
```

Lưu ý `left_joint` và `right_joint` phải là tên **joint** trong URDF (không phải tên link), `wheel_separation` là khoảng cách hai bánh $$L$$ ở bài 08-04, còn `wheel_radius` là bán kính bánh xe. Nếu bản Harmonic bạn cài sử dụng tên thẻ khác đôi chút, hãy giữ nguyên ý nghĩa tương ứng và tránh sao chép thêm các khối cấu hình odometry dài dòng chưa cần thiết.

Plugin tính toán vận tốc hai bánh theo cùng mô hình động học nghịch của cầu nối firmware:

$$
v_R = v + \omega \frac{L}{2}, \qquad v_L = v - \omega \frac{L}{2}
$$

với $$L = 0.16$$. Quãng đường đi được sau mỗi vòng quay bánh là:

$$
s = 2 \pi r
$$

với $$r = 0.033$$, tương đương khoảng 0,207 m mỗi vòng. Nếu khai báo `wheel_radius` là 0,05 trong plugin trong khi hình trụ URDF có bán kính 0,033, quãng đường di chuyển thực tế trong mô phỏng sẽ sai lệch hoàn toàn so với tính toán từ URDF.

Tham số `use_sim_time` là cam kết đồng bộ với `/clock`. Sau khi cầu nối `/clock` đã hoạt động, hãy bật `robot_state_publisher` với `-p use_sim_time:=true` để mọi cảm biến mô phỏng dùng chung một trục thời gian. Nếu một node dùng đồng hồ thực trong khi Gazebo dùng thời gian mô phỏng, bạn sẽ gặp lỗi ngoại suy TF hoặc thấy xe chạy trong Gazebo nhưng đứng yên trên RViz. Ngược lại, nếu bật `use_sim_time:=true` trước khi `/clock` tồn tại, mọi timer sẽ bị đứng chờ. Do đó luôn bắc cầu `/clock`, kiểm tra bằng `echo` rồi mới dùng tham số này.

Cần phân biệt rõ: RViz chỉ là công cụ hiển thị, không phải bộ mô phỏng vật lý — `RobotModel` vẫn vẽ URDF bình thường ngay cả khi quá trình spawn vào Gazebo thất bại. Tiêu chí kiểm chứng của bài là robot thực sự lăn bánh trong cửa sổ Gazebo (hoặc nếu chạy headless, kiểm tra topic odometry từ `gz topic -l` thấy vị trí thay đổi khi gửi `Twist`).

Cuối cùng, va chạm và quán tính là hai yếu tố giữ robot đứng vững trên mặt sàn. Một link chỉ có `visual` sẽ rơi xuyên qua sàn; một link có `collision` nhưng thiếu `<inertial>` sẽ bị bộ mô phỏng từ chối hoặc gây mất ổn định số học. Do đó cả thân xe và hai bánh đều bắt buộc có đủ hai thẻ này.

## Ví dụ làm từng bước

Giả sử tệp `xacro` ở bài 09-06 đặt tại `~/ros2_ws/src/capstone_description/urdf/capstone.urdf.xacro`, đã bổ sung khối plugin `DiffDrive` với `track = 0.16` và `wheel_r = 0.033`. Khai triển ra URDF:

```bash
source /opt/ros/jazzy/setup.bash
xacro ~/ros2_ws/src/capstone_description/urdf/capstone.urdf.xacro > /tmp/capstone.urdf
```

Terminal A — chạy `robot_state_publisher` với đồng hồ mô phỏng:

```bash
source /opt/ros/jazzy/setup.bash
ros2 run robot_state_publisher robot_state_publisher --ros-args \
  -p use_sim_time:=true \
  -p robot_description:="$(cat /tmp/capstone.urdf)"
```

Terminal B — khởi chạy world trống:

```bash
source /opt/ros/jazzy/setup.bash
ros2 launch ros_gz_sim gz_sim.launch.py gz_args:="empty.sdf -r"
```

Terminal C — sau khi cửa sổ hoặc log server đã sẵn sàng, spawn mô hình:

```bash
source /opt/ros/jazzy/setup.bash
ros2 run ros_gz_sim create -world empty -file /tmp/capstone.urdf -name capstone
```

Bạn sẽ thấy khối hộp thân xe cùng hai bánh trụ xuất hiện và đứng vững trên mặt phẳng mà không bị lún. Tiếp theo, bật cầu nối `parameter_bridge` (đặt `/clock` trước để dễ nhớ ký hiệu một chiều `[`):

```bash
source /opt/ros/jazzy/setup.bash
ros2 run ros_gz_bridge parameter_bridge \
  /clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock \
  /cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist
```

Mở một terminal khác kiểm tra đồng hồ:

```bash
source /opt/ros/jazzy/setup.bash
ros2 topic echo /clock --once
```

Trường giây (`sec`) phải lớn hơn 0 nhờ cờ `-r`; nếu bằng 0 nghĩa là world vẫn đang tạm dừng.

Gửi một đợt lệnh chạy thẳng tốc độ chậm:

```bash
ros2 topic pub --times 20 /cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 0.2, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"
```

Hai mươi message chỉ đủ cho xe lăn một đoạn ngắn. Trong cửa sổ Gazebo, khung xe sẽ tiến dọc theo $$+x$$ với cả hai bánh quay cùng chiều, và khi publisher kết thúc, xe không còn nhận lực dẫn động nữa. Trường `linear.y` giữ bằng 0 vì xe vi sai không trượt ngang; với $$L/2 = 0.08$$, $$v = 0.2$$ và $$\omega = 0$$, vận tốc dài vành hai bánh đều bằng 0,2 m/s.

## Lab

1. Thêm khối plugin `DiffDrive` vào tệp `xacro`, gán `wheel_separation` bằng thuộc tính khẩu độ và `wheel_radius` bằng thuộc tính bán kính bánh. Sau mỗi lần chỉnh sửa, chạy lại `xacro` để cập nhật `/tmp/capstone.urdf`.
2. Khởi chạy `robot_state_publisher` với `use_sim_time:=true` và tệp URDF đã khai triển.
3. Mở world bằng `empty.sdf -r` và xác nhận `gz topic -l` có `/clock`.
4. Spawn mô hình với `-world empty`, `-file /tmp/capstone.urdf` và `-name capstone`. Quan sát trực tiếp trong Gazebo (không chỉ nhìn RViz) để chắc chắn xe nằm vững trên sàn.
5. Chạy một tiến trình `parameter_bridge` với `[` cho `/clock` và `@` cho `/cmd_vel`, rồi `echo /clock --once` xác nhận thời gian đang chạy.
6. Xuất bản `linear.x = 0.2` trong một cụm ngắn (`--times 20` hoặc vài giây) và quan sát xe di chuyển trong Gazebo.
7. Dừng publisher và xác nhận xe ngừng được dẫn động. Sau đó nhấn Ctrl-C tắt cầu nối rồi thử xuất bản lại: xe phải đứng yên hoàn toàn, chứng minh luồng điều khiển đi qua cầu nối.

**Kết quả mong đợi**

Mô hình `capstone` hiển thị trên mặt sàn trong world Harmonic; khi gửi lệnh, cả hai bánh lăn đều và thân xe tiến về trước; khi dừng lệnh, xe không còn lực đẩy và `/clock` trả về thời gian lớn hơn 0. Nếu chỉ thấy mô hình hiển thị trong RViz còn trong Gazebo xe đứng yên hoặc không tồn tại thì bài lab chưa đạt.

```text
capstone visible in the empty world
/clock sec > 0
wheels rolling in Gazebo while linear.x is 0.2
```

**Các lỗi thường gặp**

| Hiện tượng | Nguyên nhân thường gặp |
| --- | --- |
| Lỗi spawn hoặc không thấy mô hình | Sai tên world (`shapes` thay vì `empty`), hoặc truyền tệp `.xacro` thô cho `create` thay vì URDF đã khai triển |
| Mô hình rơi xuyên qua mặt sàn | Link chỉ có `visual` mà thiếu `collision`, không có bề mặt tiếp xúc |
| Mô hình văng ra hoặc bị từ chối nạp | Có `collision` nhưng thiếu `<inertial>`, hoặc ma trận quán tính bằng 0 |
| Bánh quay ngang như đồng xu hoặc xe trượt không lăn | Khai báo sai trục `<axis>` của khớp; với khớp đã xoay `rpy="-1.5708 0 0"` ở bài 09-06, trục đúng là `<axis xyz="0 0 1"/>` |
| `cmd_vel` xuất hiện trên ROS nhưng xe trong Gazebo không chạy | Cầu nối chưa chạy, hoặc tên khớp trong plugin không khớp `left_wheel_joint` và `right_wheel_joint` |
| Dữ liệu TF cũ hoặc node `use_sim_time` bị đứng | Chưa bắc cầu `/clock`, world bị tạm dừng vì thiếu `-r`, hoặc chỉ một phần hệ thống bật thời gian mô phỏng |

## Mua ở Việt Nam

Bài này hoàn toàn là mô phỏng phần mềm trên laptop Ubuntu 24.04 từ bài 10-01. Không cần mua thêm mạch, lidar hay kết nối robot thật (hãy tắt nguồn Capstone và không cắm cáp serial).

## Video tham khảo

- **Xem trước:** [How do we describe a robot? With URDF! | Getting Ready to Build Robots with ROS #7](https://www.youtube.com/watch?v=CwdbsvcpOHM) — Articulated Robotics (tiếng Anh). Giải thích cấu trúc khớp trong URDF cần khớp chính xác trước khi đưa vào Gazebo.
- [ROS2 Jazzy Tutorial: Develop and Control Gazebo Model of Mobile Robot in ROS2 and Python](https://www.youtube.com/watch?v=campHHAPtyg) — Aleksandar Haber PhD (tiếng Anh). Hướng dẫn đưa mô hình vào world trên Jazzy và gửi lệnh điều khiển; đối chiếu tên topic với lệnh launch trong bài.
- [ROS2 - Create a Xacro Macro](https://www.youtube.com/watch?v=XH6Fvv7p5n0) — Robotics Back-End (tiếng Anh). Cách dùng macro `xacro` cho từng bánh xe để tránh lặp mã khi mô hình phức tạp hơn.

## Bài tập

1. Nếu `xacro` khai báo khoảng cách hai bánh là 0,16 m nhưng plugin `DiffDrive` lại đặt `wheel_separation` là 0,20 m, mô phỏng sẽ dùng thông số nào và cần sửa ở đâu? *Gợi ý:* động học mô phỏng chạy theo thông số trong plugin; cần sửa lại về 0,16 m rồi spawn lại chứ không điều chỉnh trên RViz.
2. Khi gửi lệnh $$v = 0$$ và $$\omega = +0.5$$ rad/s, bánh nào nhận vận tốc lớn hơn theo quy ước dấu của khóa học? *Gợi ý:* bánh phải, vì với trục $$+x$$ hướng trước và $$+y$$ sang trái, góc yaw dương tương ứng quay sang trái.
3. World đang chạy là `empty.sdf` nhưng lệnh `create` lại truyền `-world shapes`. Lỗi gì xảy ra và cần sửa cờ nào? *Gợi ý:* `create` tìm world theo đúng tên đang hoạt động, nên phải đổi `-world` thành `empty`.
4. Tạo một bản sao URDF, xóa thẻ `<inertial>` của thân xe rồi thử spawn để đọc thông báo lỗi của bộ mô phỏng, sau đó khôi phục lại thẻ này. *Gợi ý:* Harmonic không thể tính tích phân động lực học cho vật có va chạm nhưng không có khối lượng; thẻ `visual` không thể thay thế.
5. Vì sao `/clock` dùng ký hiệu cầu nối một chiều `[` thay vì hai chiều `@`? *Gợi ý:* theo `parameter_bridge -h`, ký hiệu `[` chỉ cho phép dữ liệu đi từ Gazebo sang ROS, ngăn chặn việc một node ROS khác vô tình xuất bản thêm mốc thời gian gây xung đột.

## Đọc thêm

- [README ros_gz_bridge](https://github.com/gazebosim/ros_gz/blob/ros2/ros_gz_bridge/README.md) — tài liệu chuẩn về cú pháp `@` và `[` khi bắc cầu topic.
- [Bắt đầu với Gazebo Harmonic](https://gazebosim.org/docs/harmonic/getstarted/) — tổng quan về tiến trình world nơi mô hình được spawn.
- [Gazebo với ROS](https://gazebosim.org/docs/harmonic/ros_installation/) — hướng dẫn launch `ros_gz_sim` và tích hợp với Jazzy.
- [REP-103](https://www.ros.org/reps/rep-0103.html) — chuẩn quy ước hệ trục tọa độ và chiều quay yaw dương.
- [REP-105](https://www.ros.org/reps/rep-0105.html) — chuẩn hệ thống frame mà `robot_state_publisher` xuất bản từ URDF.
