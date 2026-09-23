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

Bạn đưa xacro chương 09 vào một world Harmonic đang chạy theo đúng thứ tự: bung mô hình, bật `robot_state_publisher`, launch `empty.sdf -r`, spawn bằng `ros_gz_sim create`, rồi bắc cầu `/clock` một chiều và `/cmd_vel` hai chiều. Bạn đặt tên joint bánh, khoảng cách và bán kính của plugin diff-drive trùng số trong xacro, theo ví dụ khóa học là khẩu độ 0,16 m và bán kính bánh 0,033 m. Bạn xuất bản một `Twist` chậm và nhìn bánh lăn trong chính world Gazebo. Bạn kể được năm kiểu bring-up hỏng để RViz vẫn đẹp trong khi robot mô phỏng không nhúc nhích hoặc rơi xuyên sàn. Bạn giữ `use_sim_time` khớp với đồng hồ đã bắc cầu để timer và TF dùng chung một mốc thời gian.

## Kiến thức cần trước

World trống bài 10-01 launch được và `gz topic -l` có `/clock`. Xacro bài 09-06 còn đó: thân hộp, bánh trụ, joint bánh kiểu `continuous`, có thẻ inertial. Động học nghịch bài 08-04 là nghĩa của `cmd_vel`: $$v$$ tiến và $$\omega$$ quanh $$+z$$. Mỗi terminal mới đều source Jazzy. RViz tối nay là tùy chọn; điều kiện đạt là chuyển động trong bộ mô phỏng.

## Vì sao bài này nằm trên lộ trình

Xacro vừa rồi là bản vẽ và một cây TF. Harmonic là lần đầu bản vẽ đó có khối lượng, tiếp xúc và đồng hồ. Nav2 sau này xuất bản `geometry_msgs/Twist` lên `/cmd_vel`. Trong mô phỏng, bên nghe là hệ diff-drive của Gazebo. Trên Capstone thật, cầu nối serial bài 10-04 là bên nghe thứ hai trên cùng topic. Plugin lệch khẩu độ hoặc bán kính so với xacro thì mọi bag sau kế thừa sai tỉ lệ đó. Thứ tự spawn mới là kỹ năng. Một đống terminal bật ngược trông như lỗi vật lý.

![Thứ tự từ xacro tới mô hình lăn trong Harmonic]({{ site.imgurl }}/generated/ch10_sim_bringup.png)

## Khái niệm

Bring-up là một thứ tự, không phải một lệnh.

Thứ nhất, mô tả. `xacro` bung property thành URDF mà cả `robot_state_publisher` và công cụ spawn đọc được. Mô hình khóa học dùng thân hộp, bánh trụ, joint `continuous` tên `left_wheel_joint` và `right_wheel_joint`, và `<inertial>` trên mọi link có va chạm. Khẩu độ 0,16 m, bán kính bánh 0,033 m. Hai số đó sắp được chép sang plugin. Chỉ sửa một chỗ thì hình vẽ và con lăn không còn là một.

Thứ hai, `robot_state_publisher`. Nó xuất bản cây TF từ URDF. Joint cố định vẫn hiện khi `joint_states` trống. Trong mô phỏng nó phải dùng đồng hồ Gazebo sau khi đồng hồ đã được bắc cầu, nếu không dấu thời gian của nó sống trên trục khác với scan và odometry bạn thêm sau.

Thứ ba, world. Launch `empty.sdf` với `-r` để server đang chạy, không tạm dừng. Tên world trong file đó là `empty`. Nhớ tên này.

Thứ tư, spawn. Công cụ create nhét URDF vào world đã chạy. Đối số world phải đúng tên đó:

```bash
ros2 run ros_gz_sim create -world empty -file /tmp/capstone.urdf -name capstone
```

`-world shapes` trong khi server đang chạy `empty.sdf` không tạo vũ trụ thứ hai. Nó không tìm thấy world. `-file` cần URDF đã bung, không phải file `.xacro` thô, trừ khi bạn đã bung sẵn. `-name capstone` là tên mô hình bạn sẽ tìm trên GUI.

Thứ năm, cầu nối. Hết ghi chú bài 10-01 thì chạy trợ giúp một lần:

```bash
ros2 run ros_gz_bridge parameter_bridge -h
```

Đồng hồ đi từ Gazebo sang ROS và không được đẩy ngược. Dạng README là một chiều, Gazebo sang ROS:

```bash
ros2 run ros_gz_bridge parameter_bridge /clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock
```

Dấu `[` nằm giữa kiểu ROS và kiểu Gazebo. Vận tốc lệnh trong khóa học dùng dạng hai chiều của README, để Twist xuất bản trên đồ thị ROS tới được plugin, và publisher phía Gazebo cũng hiện lên ROS:

```bash
ros2 run ros_gz_bridge parameter_bridge /cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist
```

Có thể đưa cả hai đối số vào một tiến trình `parameter_bridge`. Đừng bịa chiều ngược cho đồng hồ. Một node ROS xuất bản `/clock` trong khi Gazebo cũng xuất bản nó thì mọi node `use_sim_time` có hai ý kiến.

Plugin biến `/cmd_vel` thành chuyển động bánh là hệ diff-drive của Gazebo Sim, nạp từ mô hình. Đặt một khối ngắn vào xacro và giữ số khớp property. Các trường khóa học dựa vào là tên joint, khoảng cách, bán kính, và trần tốc độ:

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

`left_joint` và `right_joint` phải là tên joint trong URDF, không phải tên link. `wheel_separation` là khẩu độ $$L$$ của bài 08-04. `wheel_radius` là bán kính lăn. Bản demo Harmonic đang cài dùng bộ thẻ khác thì chép tên thẻ đó và giữ các nghĩa này. Đừng dán một plugin dài đầy trường odometry bạn chưa đọc.

Động học mà plugin đang xấp xỉ là cùng bản đồ nghịch với cầu nối firmware:

$$
v_R = v + \omega \frac{L}{2}, \qquad v_L = v - \omega \frac{L}{2}
$$

với $$L = 0.16$$. Quãng đường một vòng của một bánh là

$$
s = 2 \pi r
$$

với $$r = 0.033$$, nên một vòng khoảng 0,207 m vành. `wheel_radius` trong plugin là 0,05 trong khi trụ bạn vẽ là 0,033 thì bánh vẽ và bán kính tiếp xúc là hai vật khác nhau. Robot sẽ không đi đúng quãng đường bạn tính từ URDF.

`use_sim_time` là hợp đồng với `/clock`. Cầu đồng hồ đã lên thì bật `robot_state_publisher` với `-p use_sim_time:=true`, và để cảm biến mô phỏng theo đồng hồ đó. Node còn đồng hồ tường đóng dấu thông điệp mà bộ mô phỏng không chia sẻ: lỗi ngoại suy TF, hoặc robot đã chạy trong Gazebo mà RViz đứng im. Ngược lại, `use_sim_time` đúng trước khi có `/clock` thì timer đông cứng. Bắc cầu đồng hồ, echo một lần, rồi mới bật tham số.

RViz là camera, không phải đối tượng vật lý. RobotModel vẽ URDF kể cả khi spawn thất bại. Điều kiện đạt là mô hình trong cửa sổ Gazebo, bánh quay khi có `/cmd_vel`. Không có màn hình thì dùng topic odometry mà `gz topic -l` hiện và xác nhận vị trí đổi trong lúc Twist được gửi. Đừng bắt RViz chứng minh vật lý.

Va chạm và quán tính giữ thân trên mặt sàn. Link chỉ có visual thì không chạm sàn. Link có collision mà không có inertia bị từ chối hoặc làm nổ bước thời gian. Khung và mỗi bánh đều cần cả hai, vì bánh là vết tiếp xúc.

## Ví dụ làm từng bước

Giả sử xacro bài 09-06 nằm ở `~/ros2_ws/src/capstone_description/urdf/capstone.urdf.xacro`, đã thêm khối plugin, `track` 0,16 và `wheel_r` 0,033. Bung ra:

```bash
source /opt/ros/jazzy/setup.bash
xacro ~/ros2_ws/src/capstone_description/urdf/capstone.urdf.xacro > /tmp/capstone.urdf
```

Terminal A, mô tả, dùng đồng hồ Gazebo:

```bash
source /opt/ros/jazzy/setup.bash
ros2 run robot_state_publisher robot_state_publisher --ros-args \
  -p use_sim_time:=true \
  -p robot_description:="$(cat /tmp/capstone.urdf)"
```

Terminal B, world:

```bash
source /opt/ros/jazzy/setup.bash
ros2 launch ros_gz_sim gz_sim.launch.py gz_args:="empty.sdf -r"
```

Terminal C, sau khi cửa sổ hoặc log server đã lên:

```bash
source /opt/ros/jazzy/setup.bash
ros2 run ros_gz_sim create -world empty -file /tmp/capstone.urdf -name capstone
```

Bạn phải thấy hộp và hai trụ trong world, nằm trên mặt phẳng, không lún. Rồi cầu nối, một tiến trình, đồng hồ đứng trước trong danh sách đối số để bạn nhớ ký hiệu nào là một chiều:

```bash
source /opt/ros/jazzy/setup.bash
ros2 run ros_gz_bridge parameter_bridge \
  /clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock \
  /cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist
```

Kiểm đồng hồ từ một shell nữa:

```bash
source /opt/ros/jazzy/setup.bash
ros2 topic echo /clock --once
```

Trường giây phải lớn hơn không vì có `-r`. Bằng không thì world đang tạm dừng.

Một lệnh thẳng, chậm, giữ ngắn:

```bash
ros2 topic pub --times 20 /cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 0.2, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"
```

Hai mươi thông điệp là một cú lăn ngắn, không phải băng qua phòng. Trong cửa sổ Gazebo, khung đi dọc $$+x$$ và cả hai bánh quay. Hết publisher thì mô hình không còn bị dẫn. `linear.y` giữ 0 vì khung vi sai không trượt ngang. Với $$L/2 = 0.08$$, $$v = 0.2$$ và $$\omega = 0$$ đòi cả hai vành 0,2 m/s. Bạn cần thấy hai bánh quay cùng chiều.

## Lab

1. Thêm khối diff-drive ngắn vào xacro. Đặt `wheel_separation` bằng property khẩu độ và `wheel_radius` bằng property bán kính. Mỗi lần sửa, chạy lại `xacro` ra `/tmp/capstone.urdf`.
2. Bật `robot_state_publisher` với `use_sim_time:=true` và bản mô tả đã bung.
3. Launch `empty.sdf -r`. Xác nhận `gz topic -l` vẫn có `/clock`.
4. Spawn với `-world empty`, `-file /tmp/capstone.urdf`, và `-name capstone`. Nhìn khung hình Gazebo, không chỉ RViz. Thân phải nằm trên mặt phẳng.
5. Bật một `parameter_bridge` với đối số đồng hồ dùng `[` và đối số `cmd_vel` dùng `@`, đúng như ví dụ. Echo `/clock` một lần và xác nhận đồng hồ đang chạy.
6. Xuất bản `linear.x` 0,2 trong một cụm ngắn (`--times 20` hoặc vài giây). Nhìn world.
7. Dừng publisher. Mô hình phải hết bị dẫn. Ctrl-C cầu nối rồi xuất bản lại: mô hình phải đứng yên, chứng tỏ chuyển động phụ thuộc cầu nối.

**Kết quả mong đợi**

Mô hình tên `capstone` hiện trong world Harmonic, phía trên mặt sàn. Trong cụm lệnh, cả hai bánh lăn trong world đó và khung tiến về phía trước. Hết cụm, nó không còn bị cấp lực. `/clock` echo thời gian khác không. Chuyển động chỉ có trong RobotModel của RViz, trong khi mô hình Gazebo ngồi im hoặc vắng mặt, là không đạt.

```text
capstone visible in the empty world
/clock sec > 0
wheels rolling in Gazebo while linear.x is 0.2
```

**Khi hỏng thì thường vì**

| Bạn thấy | Nguyên nhân hay gặp |
| --- | --- |
| Lỗi spawn, hoặc mô hình không hiện | Lệch tên world (`shapes` với `empty`), hoặc `create` trỏ vào `.xacro` thay vì URDF đã bung |
| Mô hình rơi xuyên sàn | Link có visual mà không có collision, nên không có gì tựa lên mặt phẳng |
| Nổ ngay, hoặc mô hình bị từ chối | Có collision mà không có `<inertial>`, hoặc quán tính bằng không |
| Bánh quay như đồng xu, hoặc khung trượt không lăn | Trục joint không phải trục bánh. Bài 09-06 dùng `<axis xyz="0 1 0"/>` sau khi lăn trụ |
| `cmd_vel` echo được trong ROS, Gazebo không nhúc nhích | Cầu nối không chạy, hoặc tên joint plugin không phải `left_wheel_joint` và `right_wheel_joint` |
| TF cũ, hoặc node `use_sim_time` không tick | Chưa bắc cầu đồng hồ, world tạm dừng vì quên `-r`, hoặc chỉ một phần node dùng thời gian mô phỏng |

## Mua ở Việt Nam

Chỉ phần mềm. Lab chạy trên cùng laptop Ubuntu 24.04 của bài 10-01. Không cần board mới, không cần lidar, không cần robot trên bàn. Capstone thật để tắt nguồn; bài này không đụng cổng serial.

## Bài tập

1. Khẩu độ xacro là 0,16 còn `wheel_separation` của plugin là 0,20. Tiếp xúc lăn dùng số nào, và bạn sửa gì? Gợi ý: khoảng cách trong plugin điều khiển động học mô phỏng, nên sửa nó về 0,16 rồi spawn lại, đừng “sửa” trong RViz.
2. Bạn gửi $$v = 0$$ và $$\omega = +0.5$$ rad/s. Lệnh bánh nào lớn hơn theo quy ước dấu của khóa học? Gợi ý: bánh phải, vì yaw dương là cua trái khi $$+x$$ ở trước và $$+y$$ ở bên trái.
3. Launch dùng `empty.sdf` còn `create` được gọi với `-world shapes`. Cái gì hỏng, và bạn sửa cờ nào? Gợi ý: `create` tìm world đang chạy theo tên, nên `-world` phải là `empty` khi SDF bạn launch là file đó.
4. Nhân đôi URDF, xóa `<inertial>` của khung, spawn bản sao. Ghi lời bộ mô phỏng phàn nàn, rồi trả thẻ lại. Gợi ý: Harmonic không tích phân được vật va chạm không có khối lượng; hộp visual không thay thế được.
5. Vì sao `/clock` được bắc cầu bằng `[` chứ không bằng một `@` thứ hai? Gợi ý: `parameter_bridge -h` đánh dấu `[` là Gazebo sang ROS, và đồng hồ hai chiều sẽ cho node khác xuất bản một mốc thời gian thứ hai.

## Đọc thêm

- [README ros_gz_bridge](https://github.com/gazebosim/ros_gz/blob/ros2/ros_gz_bridge/README.md) là chỗ quyết định các dạng `@` và `[` ở trên. Đọc lại nếu cầu đã chạy mà kiểu topic không khớp.
- [Bắt đầu với Gazebo Harmonic](https://gazebosim.org/docs/harmonic/getstarted/) nói về tiến trình world mà lần spawn này gắn vào.
- [Gazebo với ROS](https://gazebosim.org/docs/harmonic/ros_installation/) ghi launch `ros_gz_sim` và cách ghép với Jazzy.
- [REP-103](https://www.ros.org/reps/rep-0103.html) là quy ước trục đằng sau câu “yaw dương nghĩa là trái.”
- [REP-105](https://www.ros.org/reps/rep-0105.html) là chuỗi frame mà `robot_state_publisher` đã xuất bản từ URDF.
