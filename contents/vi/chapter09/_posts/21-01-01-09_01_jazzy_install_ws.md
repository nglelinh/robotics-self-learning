---
layout: post
title: "Cài ROS 2 Jazzy và workspace"
chapter: "09"
order: 1
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter09
lesson_type: required
draft: false
---

Thời lượng: **~90 phút**, lâu hơn nếu Ubuntu còn mới.

## Mục tiêu

Bạn cài ROS 2 Jazzy Jalisco trên Ubuntu 24.04 từ gói deb chính thức, tạo workspace overlay bằng `colcon`, và chứng minh `ros2 topic list` chỉ chạy ở terminal mới sau khi source underlay rồi overlay đúng thứ tự. Bạn nhận ra môi trường trộn Humble/Jazzy từ dòng lỗi, và viết một câu về chỗ cái laptop này đứng so với MCU của Capstone.

## Kiến thức cần trước

Bạn dùng được terminal: `cd`, `sudo apt`, và một trình soạn thảo. Ubuntu 24.04 (Noble) là nền tảng Tier-1 của Jazzy. Máy ảo hoặc PC mini cũ là đủ. ESP32 của chương 02–08 ở trên robot; nó không chạy `colcon`. Khung serial chương 08 là thứ máy này sẽ nói sau. Bài này chưa cần lidar hay Pi.

## Vì sao bài này nằm trên lộ trình

Capstone A đã chứng minh khung xe chạy bằng firmware. Jazzy là lớp tin nhắn và công cụ đặt cạnh firmware đó, không phải bản thay cho watchdog động cơ. Mọi lệnh sau ở chương 09–12 giả định một distro đã được source. Workspace lúc thấy Humble lúc thấy Jazzy sẽ đốt một cuối tuần đáng ra dành cho TF và cầu nối. Mô phỏng chương 10 dùng đúng bản cài này cộng `ros-jazzy-ros-gz`. Nav2 và LeRobot chưa đến lượt khi `ros2 topic list` còn chưa nhàm.

## Khái niệm

ROS 2 là bộ thư viện và công cụ dòng lệnh nằm trên DDS. Một **distro** là ảnh đóng băng. Jazzy Jalisco nhắm Ubuntu 24.04. Humble nhắm 22.04. Chúng không thay thế lẫn nhau, và source cả hai trong một shell là một shell hỏng.

**Underlay** là `/opt/ros/jazzy`, apt cài. **Overlay** là workspace bạn build bằng `colcon`, thường là `~/ros2_ws`. Source underlay trước, overlay sau. `setup.bash` của overlay nhớ underlay lúc nó được build. Mở terminal mới là bạn trở về shell trần cho đến khi `.bashrc` source lại.

`ros2` là lệnh. `topic list` nói chuyện với một daemon khám phá node. Danh sách rỗng là kết quả hợp lệ: nghĩa là “chưa có topic,” không phải “cài hỏng,” miễn là `ros2 doctor` hoặc talker ở bài sau chạy được.

Locale phải là UTF-8 trước khi thêm nguồn apt. Bản cài chính thức dừng sớm, với thông báo rõ, khi `locale` là POSIX. Sửa một lần.

![Underlay rồi mới overlay]({{ site.imgurl }}/generated/ch09_workspace.png)

Windows và macOS không phải con đường khóa này gỡ lỗi. Máy duy nhất là Windows thì cài Ubuntu 24.04 trong máy ảo, ít nhất 4 GB RAM và 30 GB đĩa, hoặc dùng PC dư. WSL2 có thể chạy và cũng hỏng theo những kiểu bài này không đuổi (giao diện, serial USB, Gazebo). Ubuntu cài trực tiếp là lab khớp tài liệu.

## Lab

Kiểm tra hệ điều hành trước mọi lệnh ROS:

```bash
. /etc/os-release
echo "$VERSION_ID"
locale
```

`VERSION_ID` phải là `24.04`. Nếu là `22.04`, dừng. Máy đó dùng Humble hoặc cài lại, không ép Jazzy.

UTF-8, theo [bản cài deb Ubuntu](https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html):

```bash
sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8
```

Mở terminal mới để locale dính. Rồi nguồn apt và bản desktop. Dòng kho thay đổi khi `ros2-apt-source` cập nhật, nên chép từ trang chính thức đúng tuần bạn cài. Hình dạng là:

```bash
sudo apt install curl -y
# làm đúng khối "ros2-apt-source" trên trang cài Jazzy
sudo apt update
sudo apt upgrade
sudo apt install ros-jazzy-desktop
sudo apt install python3-colcon-common-extensions python3-rosdep
```

`ros-jazzy-desktop` gồm RViz, demo và CLI. `ros-jazzy-ros-base` là bản nhỏ cho máy robot không màn hình. Máy học thì dùng desktop.

Source, và để lần source sống sau terminal mới:

```bash
echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
source ~/.bashrc
printenv ROS_DISTRO
```

**Mong đợi:** `jazzy`.

Workspace, theo [bài tạo workspace](https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Creating-A-Workspace/Creating-A-Workspace.html):

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws
colcon build
echo "source \$HOME/ros2_ws/install/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

Dấu gạch chéo ngược trước `$HOME` quan trọng trong ngoặc kép, nếu không `.bashrc` cất một đường dẫn đã đóng băng. Đường dẫn tuyệt đối đóng băng hoặc `$HOME` được thoát đúng đều ổn. Nhìn file:

```bash
tail -n 5 ~/.bashrc
```

Dòng underlay phải **ở trên** dòng overlay.

Kiểm tra khám phá:

```bash
ros2 topic list
```

**Mong đợi** trên máy yên:

```text
/parameter_events
/rosout
```

Có bản cài chỉ hiện hai topic đó, và daemon mới có thể hiện danh sách rỗng trong chốc lát. Chạy hai lần. Rồi:

```bash
ros2 pkg list | head
which ros2
```

`which ros2` phải in `/opt/ros/jazzy/bin/ros2`.

**Khi hỏng thì thường vì**

| Bạn thấy | Nguyên nhân hay gặp |
| --- | --- |
| `Unable to locate package ros-jazzy-desktop` | Không phải Ubuntu 24.04, hoặc bỏ bước nguồn apt |
| `ROS_DISTRO` trống ở terminal mới | `.bashrc` không được source. Thêm cùng dòng vào `.profile` hoặc mở lại terminal từ menu |
| Cả `humble` và `jazzy` trong `echo $CMAKE_PREFIX_PATH` | Source hai distro. Đóng hết terminal. Giữ một dòng `source` |
| `colcon: command not found` | Thiếu `python3-colcon-common-extensions`, hoặc build trước khi source `/opt/ros/jazzy` |
| `ros2 topic list` treo | Tường lửa hoặc daemon cũ. `ros2 daemon stop` rồi thử lại |
| Hết đĩa khi `apt install` | Desktop cần vài gigabyte. Giải phóng hoặc dùng `ros-jazzy-ros-base` |

Kiểm tra môi trường, tùy chọn:

```bash
ros2 doctor
```

Cảnh báo card mạng trên laptop là thường. Lỗi về distro thì không.

## Mua ở Việt Nam

Chỉ phần mềm, cho đến khi bạn muốn một máy robot không phải laptop. PC văn phòng cũ đã chạy Ubuntu 24.04 là máy chủ rẻ nhất. Khi laptop không còn đủ, board khóa này chỉ là Raspberry Pi 5 (4 GB là mức khởi đầu ổn cho Jazzy cộng camera; 8 GB dễ thở hơn với Nav2 sau này).

| Món | Cửa hàng | Ghi chú | Khoảng giá 2026 |
| --- | --- | --- | --- |
| Raspberry Pi 5 | [Hshop, board sản xuất tại Anh](https://hshop.vn/may-tinh-raspberry-pi-5-made-in-uk) | Chọn RAM trên trang. Giá niêm yết đổi theo phiên bản | từ khoảng 2,4 triệu đồng cho bản RAM nhỏ; 4 GB và 8 GB đắt hơn. Xem lại |
| Bộ kit Pi 5 (nguồn, vỏ, quạt, thẻ) | [Kit cơ bản trên Hshop](https://hshop.vn/combo-raspberry-pi-5-ram-4-8gb-basic-kit) | Nguồn USB-C 27 W quan trọng. Sạc điện thoại dễ gây sụt áp | kit cao hơn board trần |
| microSD 64 GB A2 | Shopee/Lazada `thẻ nhớ microSD 64GB A2` | Cho Pi, không cho lab laptop | khoảng 150.000–350.000 đồng |

Từ khóa Shopee nếu Hshop hết: `Raspberry Pi 5 4GB chính hãng`. Tránh tin chỉ bán “vỏ case.” ESP32 vẫn là máy động cơ. Pi, về sau, là máy ROS.

## Bài tập

1. Dán kết quả `printenv ROS_DISTRO` và `which ros2` vào `lab-notes.md`. Gợi ý: cả hai phải nói jazzy và `/opt/ros/jazzy/...`.
2. `.bashrc` source `~/ros2_ws/install/setup.bash` mà không bao giờ source `/opt/ros/jazzy` thì sai chỗ nào? Gợi ý: setup của overlay thường xâu underlay lúc build. Build khi môi trường chưa có Jazzy thì xâu đó rỗng và `ros2` biến mất. Source underlay, build lại, rồi source overlay.
3. Bạn trên Ubuntu 22.04 xin chép lệnh cài. Bạn nói gì? Gợi ý: các lệnh đó cho 24.04 và Jazzy. Humble là distro khớp 22.04. Đừng trộn.
4. Vì sao ESP32 không “nằm trong workspace”? Gợi ý: workspace là cây colcon trên Linux. MCU giữ firmware chương 08. Chương 10 nối chúng bằng cầu hoặc micro-ROS, đó là lần cài sau.
5. Sau khi reboot, terminal đầu không thấy `ros2`. Bạn mở file nào? Gợi ý: `~/.bashrc`, và kiểm tra terminal có thực sự đọc nó.

## Đọc thêm

- [Gói deb Ubuntu cho Jazzy](https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html). Dùng khối apt-source của trang này, không dùng dòng `sources.list` cũ trên blog.
- [Tạo workspace](https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Creating-A-Workspace/Creating-A-Workspace.html).
- [REP-2000](https://www.ros.org/reps/rep-2000.html) về distro nào khớp Ubuntu nào.
- [Tài liệu colcon](https://colcon.readthedocs.io/en/released/user/quick-start.html) cho `colcon build --symlink-install`, thứ bạn sẽ muốn khi gói chứa Python.
