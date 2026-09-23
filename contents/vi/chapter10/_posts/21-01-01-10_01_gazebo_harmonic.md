---
layout: post
title: "Giới thiệu Gazebo Harmonic"
chapter: "10"
order: 1
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter10
lesson_type: required
draft: false
---

Thời lượng: **~70 phút**.

## Mục tiêu

Bạn mở được một world Gazebo Harmonic từ terminal ROS 2 Jazzy và phân biệt lệnh `gz sim` với binary Classic `gazebo`. Bạn giải thích được vì sao khóa học ghép Jazzy với Harmonic, và vì sao source Humble hoặc cài gói Classic đưa bạn sang bộ mô phỏng khác. Bạn dùng `gz topic -l` để thấy world đang chạy đã có `/clock`, và nối cờ `-r` với nút play để không tưởng một world đang tạm dừng là bản cài hỏng. Bạn đọc ký hiệu hướng do `ros_gz_bridge` in ra mà không để cầu nối chạy tiếp. Bạn lưu một cửa sổ GUI hoặc log server không màn hình làm bằng chứng world trống vẫn sống.

## Kiến thức cần trước

Bài 09-01 đã xong: Ubuntu 24.04, bản deb ROS 2 Jazzy, và một terminal mà `printenv ROS_DISTRO` in `jazzy`. Bạn giữ được hai terminal và biết Ctrl-C dừng tiến trình đang chiếm mặt trước. Tối nay không cần robot, không cần URDF, không cần firmware micro-ROS. Nếu `printenv ROS_DISTRO` in `humble`, sửa việc đó trước khi cài bất cứ thứ gì trong bài này.

## Vì sao bài này nằm trên lộ trình

Capstone A đã chạy bằng khung chương 08, chương 09 đã đặt topic, TF và một file xacro trên laptop. Bài này mở bộ mô phỏng mà Nav2 sẽ lập kế hoạch bên trong, và là nơi một stack học sau này ghi bag để đối chiếu với sàn nhà. Đường nối là họ `ros_gz`, không phải gói Classic `gazebo_ros`. Học đúng tên tiến trình khi world còn trống, để lần spawn hỏng ở bài sau là lỗi mô hình, không phải lần cài nhầm thêm một Gazebo nữa.

![Gazebo Harmonic cạnh ROS 2 Jazzy, ros_gz ở giữa]({{ site.imgurl }}/generated/ch10_gazebo_stack.png)

## Khái niệm

Gazebo Classic và Gazebo Sim là hai codebase khác nhau, chỉ trùng biệt danh. Classic là lệnh `gazebo` mà tutorial ROS 1 cũ vẫn chỉ. Gazebo Sim là dòng hiện tại: lệnh `gz sim`, world dạng SDF, topic liệt kê bằng `gz topic`. Harmonic là bản Gazebo Sim mà Jazzy được build cùng. Bản đi với Humble là Fortress. Tutorial bảo `sudo apt install gazebo` hoặc `ros-humble-gazebo-ros-pkgs` không phải tutorial của chương này.

Tên apt của phần ghép trên Jazzy là một metapackage:

```bash
sudo apt install ros-jazzy-ros-gz
```

Gói đó kéo những thứ khóa học thực sự gọi: `ros_gz_sim` để launch và spawn, `ros_gz_bridge` để chép một số topic giữa hai đồ thị. Cài xong không có nghĩa world đã chạy. Nó chỉ đặt executable lên đường dẫn ROS sau khi bạn source Jazzy.

Tuần này cần hai world có sẵn. `shapes.sdf` là world khởi đầu, vài khối hình học, dùng khi bạn muốn biết renderer có vẽ được không. `empty.sdf` là world các bài sau của chương 10 sẽ spawn Capstone vào. Dạng launch trong tài liệu `ros_gz`:

```bash
ros2 launch ros_gz_sim gz_sim.launch.py gz_args:="empty.sdf -r"
```

Chuỗi trong `gz_args` được đưa cho `gz sim`. Cờ `-r` nghĩa là chạy. Không có nó, server nạp world rồi chờ: nút play nằm ở trạng thái tạm dừng, thời gian mô phỏng không nhích. Có `-r` thì world đã chạy sẵn. World tạm dừng vẫn là lần launch thành công, và nó sẽ làm mọi node `use_sim_time` về sau trông như đông cứng vì `/clock` ở không.

`/clock` là topic của Gazebo trước khi là topic của ROS. Server còn sống thì `gz topic -l` liệt kê nó, có cầu nối ROS hay không. Cầu nối là bài sau. Ký hiệu hướng của cầu rất dễ đảo, nên tối nay chỉ đọc, không bật cầu:

```bash
ros2 run ros_gz_bridge parameter_bridge -h
```

Bạn chỉ cần phần trợ giúp. Ký hiệu nằm giữa kiểu ROS và kiểu Gazebo là hướng. Hai dạng khóa học sẽ dùng, chép từ README của `ros_gz_bridge`, là vận tốc lệnh hai chiều và đồng hồ một chiều. Hai chiều:

```bash
ros2 run ros_gz_bridge parameter_bridge /cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist
```

Đồng hồ, chỉ từ Gazebo sang ROS:

```bash
ros2 run ros_gz_bridge parameter_bridge /clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock
```

Đừng đảo hai ký hiệu “cho biết” tối nay. Publisher thứ hai trên `/clock` tranh với bộ mô phỏng. Bài 2 mới là chỗ hai dòng đó thực sự chạy.

Thời gian mô phỏng và thời gian tường không phải cùng một đại lượng. Hệ số thời gian thực:

$$
\mathrm{RTF} = \frac{\Delta t_{\mathrm{sim}}}{\Delta t_{\mathrm{wall}}}
$$

GUI báo hệ số gần 1 thì một giây mô phỏng tốn khoảng một giây đồng hồ. Hệ số tụt thì lệnh 0,2 m/s vẫn là 0,2 m trên mỗi giây mô phỏng, nhưng đồng hồ bấm giờ chạy trước. World trống trên laptop bình thường phải nằm gần 1.

Chạy không màn hình là cùng server, không GUI. `printenv DISPLAY` rỗng thì cửa sổ không mở được. Thêm cờ chỉ-server mà `gz sim --help` ghi, thường là `-s`:

```bash
ros2 launch ros_gz_sim gz_sim.launch.py gz_args:="empty.sdf -r -s"
```

Lab đạt trên log đó khi tiến trình không thoát và `gz topic -l` có `/clock`. Máy lab là laptop. Pi 5 có thể gánh stack nhẹ hơn về sau; đây không phải chỗ để học GUI có lên hay không.

## Ví dụ làm từng bước

Ba phép kiểm, đúng thứ tự, cho biết bạn sắp launch Gazebo nào.

```bash
printenv ROS_DISTRO
gz sim --help
apt-cache policy ros-jazzy-ros-gz
```

Dòng đầu phải là `jazzy`. Phần trợ giúp phải thuộc `gz sim`. Shell báo `gz: command not found` thì source Jazzy rồi xem policy apt. Không có candidate nghĩa là thiếu nguồn apt Jazzy, hoặc máy không phải Ubuntu 24.04. Đừng “sửa” bằng cách cài gói `gazebo`. Classic không nạp file launch của chương này.

Policy đã có bản cài thì mở world trống ở một terminal và để đó:

```bash
source /opt/ros/jazzy/setup.bash
ros2 launch ros_gz_sim gz_sim.launch.py gz_args:="empty.sdf -r"
```

Terminal thứ hai, source Jazzy lần nữa rồi liệt kê topic Gazebo:

```bash
source /opt/ros/jazzy/setup.bash
gz topic -l
```

Bạn tìm `/clock`. `ros2 topic list` có thể gần như trống, vì chưa có gì bắc cầu hai đồ thị. Gazebo đang xuất bản trên đồ thị của nó. Ctrl-C terminal launch thì danh sách topic Gazebo chết theo server. Ảnh một cửa sổ đã đóng không phải world đang chạy.

## Lab

1. Kiểm distro bằng `printenv ROS_DISTRO`. Không phải `jazzy` thì dừng, source `/opt/ros/jazzy/setup.bash`, kiểm lại. Cài cả Humble lẫn Jazzy thì lần `source` sau cùng thắng.
2. Cài metapackage: `sudo apt install ros-jazzy-ros-gz`. Từ chối mọi lệnh tiếp theo cài gói tên `gazebo` hoặc `ros-humble-gazebo-ros-pkgs`.
3. Ở terminal A, launch world trống với `gz_args:="empty.sdf -r"`. Để tiến trình đó ở mặt trước.
4. Không thấy cửa sổ thì chạy `printenv DISPLAY`. Rỗng thì dừng launch và chạy lại, thêm `-s` vào `gz_args` như dòng không màn hình ở trên.
5. Ở terminal B, source Jazzy và chạy `gz topic -l`. Xác nhận có `/clock`. Đừng bật `parameter_bridge`.
6. Chạy `ros2 run ros_gz_bridge parameter_bridge -h`, ghi ký hiệu nào là hai chiều và ký hiệu nào là Gazebo sang ROS. Rồi thoát phần trợ giúp. `ros2 topic list` vẫn không cần có `/clock` đã bắc cầu.
7. Năm phút tùy chọn: launch `shapes.sdf` một lần thay cho `empty.sdf`, nhìn các khối, rồi trở lại `empty.sdf -r`. Bài sau spawn world tên `empty`, nên đó là server bạn để chạy nếu học tiếp tối nay.

**Kết quả mong đợi**

Một cửa sổ phiên Gazebo Sim, đã chạy vì có `-r`, hoặc một tiến trình server không thoát khi bạn dùng `-s`. Terminal thứ hai in danh sách topic có `/clock`. Không còn tiến trình `parameter_bridge`.

```text
/clock
/stats
```

Danh sách của bạn dài hơn. Dòng cần có là `/clock`. `ros2 topic list` khi chưa bắc cầu không cần hiện `/clock`.

**Khi hỏng thì thường vì**

| Bạn thấy | Nguyên nhân hay gặp |
| --- | --- |
| `Unable to locate package ros-jazzy-ros-gz` | Ubuntu không phải 24.04, hoặc chưa thêm nguồn apt Jazzy theo hướng dẫn cài |
| `gazebo` mở cửa sổ khác, không có `gz sim` | Gói Classic nằm trên `PATH`. Chương này dùng `gz sim` |
| Launch thoát, hoặc GUI không hiện | `DISPLAY` rỗng. Dùng dạng `-s`, hoặc chạy trên máy có màn hình |
| `printenv ROS_DISTRO` in `humble` | Shell source Humble sau cùng. `ros_gz` của Jazzy không nạp trong môi trường đó |
| `gz topic -l` không kết nối được | Terminal launch đã đóng. Server không chạy |
| Nút play đang tạm dừng, thời gian ở 0 | Quên `-r`. Bấm play một lần để thấy thời gian chạy, rồi launch lại có `-r` |

## Mua ở Việt Nam

Lab này là phần mềm trên laptop bạn đã dùng cho Jazzy. Không cần cảm biến, không cần ESP32. Raspberry Pi 5 là máy tính robot tùy chọn về sau, không phải máy GUI tối nay. Bản RAM thấp trên Hshop gần đây khởi điểm khoảng 2,4 triệu đồng; đó là ước lượng 2026, kiểm tra lại trước khi trả. Board: [Raspberry Pi 5 made in UK](https://hshop.vn/may-tinh-raspberry-pi-5-made-in-uk). Kit: [basic kit](https://hshop.vn/combo-raspberry-pi-5-ram-4-8gb-basic-kit). Slug đổi thì tìm “Raspberry Pi 5” trên [hshop.vn](https://hshop.vn/). Từ khóa Shopee hoặc Lazada: `Raspberry Pi 5 4GB`, cùng lời nhắc 2026. Tin rẻ hơn nhiều so với board Hshop thường thiếu nguồn.

## Bài tập

1. Chạy `printenv ROS_DISTRO` và `gz sim --help`. Viết hai câu vì sao máy này thiếu binary `gazebo` vẫn chấp nhận được. Gợi ý: bộ mô phỏng của Jazzy là `gz sim` thuộc dòng Harmonic, còn binary `gazebo` là Classic.
2. Launch `empty.sdf` một lần không `-r` và một lần có `-r`. Ghi nút play làm gì mỗi lần và thời gian mô phỏng có chạy không. Gợi ý: không có `-r` thì server nạp world ở trạng thái tạm dừng, `/clock` không tiến đến khi bạn bấm play.
3. Thời gian mô phỏng đi 2,0 s trong khi đồng hồ bấm giờ đi 4,0 s. Tính hệ số thời gian thực và nói world trống trên laptop của bạn có nên trông như vậy không. Gợi ý: RTF là thời gian mô phỏng chia thời gian tường, nên giá trị là 0,5, và world trống phải gần 1 hơn.
4. Nêu gói apt bài này cài và hai tên gói sẽ kéo nhầm bộ mô phỏng. Gợi ý: cài `ros-jazzy-ros-gz`; đừng cài `gazebo` hoặc gói `ros-humble-gazebo-ros`.
5. Chép đúng lệnh launch bạn sẽ cần ở bài sau, gồm file world và `-r`. Gợi ý: `gz_args` phải chứa `empty.sdf -r`, vì công cụ spawn sẽ tìm world tên `empty`.

## Đọc thêm

- [Bắt đầu với Gazebo Harmonic](https://gazebosim.org/docs/harmonic/getstarted/) cho thấy `gz sim`, world hình khối, và nút play của bài này.
- [Gazebo Harmonic với ROS](https://gazebosim.org/docs/harmonic/ros_installation/) là ghi chú ghép đôi: Jazzy với Harmonic, và các gói `ros_gz`.
- [Cài deb Jazzy trên Ubuntu](https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html) là trang nguồn apt khi không tìm thấy `ros-jazzy-ros-gz`.
- [README ros_gz_bridge](https://github.com/gazebosim/ros_gz/blob/ros2/ros_gz_bridge/README.md) là nguồn của các dòng `@` và `[`. Đọc trước khi bài 2 chạy chúng.
