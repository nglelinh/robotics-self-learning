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

Thời lượng: **~90 phút** (có thể lâu hơn nếu bạn vừa cài mới Ubuntu).

## Mục tiêu

Sau bài học này, bạn sẽ cài đặt được ROS 2 Jazzy Jalisco trên Ubuntu 24.04 từ gói `.deb` chính thức, tạo workspace overlay bằng `colcon` và kiểm chứng rằng lệnh `ros2 topic list` chỉ hoạt động trong terminal mới sau khi nạp (source) đúng thứ tự underlay rồi đến overlay. Bạn cũng sẽ nhận diện được lỗi trộn môi trường giữa Humble và Jazzy qua thông báo hệ thống, đồng thời xác định rõ vai trò của máy tính chạy ROS so với vi điều khiển (MCU) trên xe Capstone.

## Kiến thức cần trước

Nếu máy tính đặt trên xe của bạn là Raspberry Pi 5 hoặc Jetson, hãy thực hiện bài [Linux trên máy tính của robot]({% multilang_post_url contents/chapter09/09_00_linux_on_sbc %}) trước hoặc song song: hệ điều hành phải là Ubuntu 24.04, và mạch Jetson đang chạy Jammy (22.04) thì chưa thể cài Jazzy. Bạn cần biết dùng các lệnh terminal cơ bản như `cd`, `sudo apt` và một trình soạn thảo văn bản. Ubuntu 24.04 (Noble) là nền tảng hỗ trợ bậc 1 (Tier-1) của Jazzy; một máy ảo hoặc máy tính mini cũ là đủ để thực hành. Lưu ý rằng ESP32 từ chương 02–08 nằm trên robot và không chạy `colcon`; máy tính này sẽ giao tiếp với ESP32 qua khung dữ liệu serial của chương 08 ở các bài sau. Ở bài này bạn chưa cần lidar hay Raspberry Pi.

## Vì sao bài này nằm trên lộ trình

Capstone A đã chứng minh khung xe vận hành ổn định bằng firmware. ROS 2 Jazzy đóng vai trò là lớp truyền thông và công cụ hỗ trợ đặt phía trên, không thay thế cơ chế watchdog bảo vệ động cơ trên vi điều khiển. Mọi câu lệnh từ chương 09 đến chương 12 đều giả định một bản ROS đã được nạp đúng cách. Nếu workspace bị lẫn lộn giữa Humble và Jazzy, bạn sẽ mất rất nhiều thời gian gỡ lỗi thay vì tập trung vào TF và cầu nối điều khiển. Phần mô phỏng ở chương 10 cũng sử dụng chính bản cài đặt này kết hợp với `ros-jazzy-ros-gz`. Trước khi chuyển sang Nav2 hay LeRobot, việc thao tác thành thạo với môi trường và lệnh `ros2 topic list` là bước nền tảng bắt buộc.

## Khái niệm

ROS 2 là tập hợp các thư viện và công cụ dòng lệnh xây dựng trên nền tảng truyền thông DDS. Mỗi **distro** là một phiên bản phát hành cố định theo hệ điều hành: Jazzy Jalisco dành cho Ubuntu 24.04, còn Humble dành cho Ubuntu 22.04. Hai bản này không thể thay thế lẫn nhau, và việc nạp đồng thời cả hai trong cùng một shell sẽ làm hỏng môi trường làm việc.

**Underlay** là thư mục `/opt/ros/jazzy` do `apt` cài đặt. **Overlay** là workspace cá nhân mà bạn biên dịch bằng `colcon`, thường đặt tại `~/ros2_ws`. Bạn luôn phải nạp underlay trước rồi mới nạp overlay; tệp `setup.bash` của overlay sẽ ghi nhớ underlay tại thời điểm nó được biên dịch. Khi mở một cửa sổ terminal mới, môi trường sẽ quay về trạng thái trống cho đến khi tệp `.bashrc` tự động nạp lại các thiết lập này.

`ros2` là công cụ dòng lệnh chính; lệnh `topic list` giao tiếp với một tiến trình nền (daemon) làm nhiệm vụ khám phá các node trong mạng. Danh sách rỗng vẫn là kết quả hợp lệ (chỉ cho thấy chưa có topic nào đang hoạt động chứ không phải lỗi cài đặt), miễn là `ros2 doctor` hoặc ví dụ talker ở bài tiếp theo chạy bình thường.

Hệ thống cần được thiết lập bảng mã UTF-8 trước khi thêm kho gói `apt` của ROS. Nếu `locale` đang là POSIX, quá trình cài đặt chính thức sẽ dừng sớm với thông báo lỗi rõ ràng, do đó hãy cấu hình dứt điểm một lần ngay từ đầu.

![Underlay rồi mới overlay]({{ site.imgurl }}/generated/ch09_workspace.png)

Khóa học này không hỗ trợ gỡ lỗi trên Windows hay macOS. Nếu bạn chỉ có máy tính Windows, hãy cài Ubuntu 24.04 trong máy ảo (tối thiểu 4 GB RAM và 30 GB ổ cứng) hoặc dùng một máy tính phụ. WSL2 có thể chạy được nhưng thường phát sinh nhiều vấn đề ngoài phạm vi bài học (như đồ họa, truyền cổng serial USB, Gazebo). Cài trực tiếp Ubuntu là phương án khớp hoàn toàn với tài liệu thực hành.

## Lab

Kiểm tra phiên bản hệ điều hành và thiết lập ngôn ngữ trước khi cài ROS:

```bash
. /etc/os-release
echo "$VERSION_ID"
locale
```

Giá trị `VERSION_ID` bắt buộc phải là `24.04`. Nếu máy trả về `22.04`, hãy dừng lại: hệ thống đó chỉ phù hợp với Humble hoặc cần cài lại Ubuntu 24.04, không nên ép cài Jazzy.

Cấu hình UTF-8 theo hướng dẫn [bản cài deb Ubuntu](https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html):

```bash
sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8
```

Mở một cửa sổ terminal mới để thiết lập locale có hiệu lực, sau đó thêm nguồn `apt` và cài bản desktop. Vì lệnh cài gói `ros2-apt-source` có thể thay đổi khi trang chính thức cập nhật, hãy sao chép đúng khối lệnh từ trang cài đặt Jazzy tại thời điểm bạn thực hành. Quy trình tổng quát như sau:

```bash
sudo apt install curl -y
# làm đúng khối "ros2-apt-source" trên trang cài Jazzy
sudo apt update
sudo apt upgrade
sudo apt install ros-jazzy-desktop
sudo apt install python3-colcon-common-extensions python3-rosdep
```

Gói `ros-jazzy-desktop` bao gồm RViz, các ví dụ mẫu và công cụ dòng lệnh. Gói `ros-jazzy-ros-base` gọn nhẹ hơn, phù hợp cho máy tính trên robot không gắn màn hình. Với máy tính dùng để học, hãy cài bản desktop.

Nạp môi trường và lưu vào `~/.bashrc` để tự động kích hoạt mỗi khi mở terminal mới:

```bash
echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
source ~/.bashrc
printenv ROS_DISTRO
```

**Kết quả mong đợi:** `jazzy`.

Tạo workspace theo hướng dẫn [bài tạo workspace](https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Creating-A-Workspace/Creating-A-Workspace.html):

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws
colcon build
echo "source \$HOME/ros2_ws/install/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

Dấu gạch chéo ngược trước `$HOME` trong cặp ngoặc kép giúp giữ nguyên biến `$HOME` thay vì ghi cứng một đường dẫn tĩnh vào `.bashrc` (cả đường dẫn tuyệt đối lẫn biến `$HOME` được thoát đúng cách đều hoạt động ổn định). Kiểm tra lại cuối tệp `.bashrc`:

```bash
tail -n 5 ~/.bashrc
```

Dòng nạp underlay (`/opt/ros/jazzy/setup.bash`) bắt buộc phải nằm **phía trên** dòng nạp overlay (`ros2_ws/install/setup.bash`).

Kiểm tra khả năng khám phá topic:

```bash
ros2 topic list
```

**Kết quả mong đợi** khi chưa chạy node nào khác:

```text
/parameter_events
/rosout
```

Một số bản cài đặt chỉ hiển thị hai topic mặc định trên, và daemon mới khởi động có thể trả về danh sách trống trong giây lát. Hãy chạy lại lệnh lần thứ hai, rồi kiểm tra thêm:

```bash
ros2 pkg list | head
which ros2
```

Lệnh `which ros2` phải trả về `/opt/ros/jazzy/bin/ros2`.

**Các lỗi thường gặp**

| Hiện tượng | Nguyên nhân thường gặp |
| --- | --- |
| `Unable to locate package ros-jazzy-desktop` | Không phải Ubuntu 24.04, hoặc bỏ qua bước thêm nguồn `apt` của ROS |
| `ROS_DISTRO` bị trống ở terminal mới | Tệp `.bashrc` không tự chạy; thêm dòng tương ứng vào `.profile` hoặc mở lại terminal từ menu hệ thống |
| `echo $CMAKE_PREFIX_PATH` chứa cả `humble` và `jazzy` | Đã nạp lẫn hai bản ROS; đóng toàn bộ terminal và chỉ giữ lại một dòng `source` duy nhất |
| `colcon: command not found` | Chưa cài `python3-colcon-common-extensions`, hoặc chạy build trước khi nạp `/opt/ros/jazzy` |
| `ros2 topic list` bị treo | Do tường lửa hoặc daemon cũ bị kẹt; chạy `ros2 daemon stop` rồi thử lại |
| Hết dung lượng đĩa khi `apt install` | Bản desktop cần vài gigabyte trống; giải phóng ổ đĩa hoặc chuyển sang `ros-jazzy-ros-base` |

Kiểm tra tổng thể môi trường (tùy chọn):

```bash
ros2 doctor
```

Trên laptop, một vài cảnh báo liên quan đến card mạng là bình thường, nhưng không được có lỗi liên quan đến phiên bản ROS distro.

## Mua ở Việt Nam

Ở bài này bạn chưa cần mua phần cứng mới, trừ khi muốn chuẩn bị sớm máy tính độc lập cho robot thay vì dùng laptop. Một chiếc PC văn phòng cũ cài Ubuntu 24.04 là phương án tiết kiệm nhất để học. Khi cần gắn máy tính lên robot, khóa học chọn Raspberry Pi 5 (bản 4 GB đủ dùng cho Jazzy và camera; bản 8 GB thoải mái hơn khi chạy Nav2 về sau).

| Linh kiện | Nơi mua | Ghi chú | Khoảng giá 2026 |
| --- | --- | --- | --- |
| Raspberry Pi 5 | [Hshop, board sản xuất tại Anh](https://hshop.vn/may-tinh-raspberry-pi-5-made-in-uk) | Chọn dung lượng RAM trên trang; giá thay đổi theo phiên bản | Từ khoảng 2,4 triệu đồng cho bản RAM nhỏ; bản 4 GB và 8 GB cao hơn (cần kiểm tra lại giá hiện tại) |
| Bộ kit Pi 5 (nguồn, vỏ, quạt, thẻ nhớ) | [Kit cơ bản trên Hshop](https://hshop.vn/combo-raspberry-pi-5-ram-4-8gb-basic-kit) | Nguồn USB-C 27 W rất quan trọng vì sạc điện thoại thường dễ gây sụt áp | Cao hơn mua mạch trần |
| Thẻ microSD 64 GB chuẩn A2 | Shopee/Lazada (`thẻ nhớ microSD 64GB A2`) | Dùng cho Pi, không cần cho bài lab trên laptop | Khoảng 150.000–350.000 đồng |

Nếu Hshop hết hàng, bạn có thể tìm trên Shopee với từ khóa `Raspberry Pi 5 4GB chính hãng` và lưu ý tránh các tin đăng chỉ bán vỏ hộp (case). Trong kiến trúc hệ thống, ESP32 vẫn đảm nhiệm điều khiển động cơ, còn Pi sẽ đóng vai trò máy tính chạy ROS về sau.

## Video tham khảo

- **Xem trước:** [How to Correctly Install ROS2 Jazzy Jalisco in Linux Ubuntu 24.04 (Noble) - ROS2 Tutorial](https://www.youtube.com/watch?v=08o46x5SfJM) — Aleksandar Haber PhD (tiếng Anh). Hướng dẫn cài đặt Jazzy trên Ubuntu 24.04; đối chiếu từng lệnh `apt` với bài học và không nạp thêm distro khác.
- [ROS 2 Jazzy + Ubuntu 24.04: Complete Installation Guide!](https://www.youtube.com/watch?v=CSsp7LcBD-Y) — Robotics Unboxed (tiếng Anh). Nội dung tương tự nhưng ngắn gọn hơn, hữu ích để kiểm tra thứ tự `source` trước khi tạo workspace.

## Bài tập

1. Dán kết quả lệnh `printenv ROS_DISTRO` và `which ros2` vào `lab-notes.md`. *Gợi ý:* kết quả phải hiển thị `jazzy` và đường dẫn `/opt/ros/jazzy/...`.
2. Nếu `.bashrc` chỉ nạp `~/ros2_ws/install/setup.bash` mà chưa từng nạp `/opt/ros/jazzy` thì vấn đề gì sẽ xảy ra? *Gợi ý:* tệp `setup.bash` của overlay liên kết với underlay tại thời điểm biên dịch; nếu biên dịch khi chưa nạp Jazzy, chuỗi liên kết sẽ rỗng và hệ thống không tìm thấy lệnh `ros2`. Cách sửa là nạp underlay, biên dịch lại rồi mới nạp overlay.
3. Một người bạn đang dùng Ubuntu 22.04 muốn sao chép bộ lệnh cài đặt của bạn. Bạn sẽ khuyên họ thế nào? *Gợi ý:* các lệnh này dành riêng cho Ubuntu 24.04 và ROS 2 Jazzy; Ubuntu 22.04 phải dùng ROS 2 Humble, không cài lẫn.
4. Vì sao mạch ESP32 không "nằm trong workspace" này? *Gợi ý:* workspace là cây thư mục biên dịch của `colcon` trên Linux, còn vi điều khiển chạy firmware từ chương 08. Đến chương 10 chúng ta mới kết nối hai bên qua cầu nối serial hoặc micro-ROS.
5. Sau khi khởi động lại máy, terminal đầu tiên mở lên không nhận diện được lệnh `ros2`. Bạn cần kiểm tra tệp nào? *Gợi ý:* kiểm tra `~/.bashrc` và xác minh xem terminal có tự động đọc tệp này khi mở hay không.

## Đọc thêm

- [Gói deb Ubuntu cho Jazzy](https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html) — sử dụng khối lệnh `ros2-apt-source` trên trang này thay vì dòng `sources.list` cũ trên các bài blog.
- [Tạo workspace](https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Creating-A-Workspace/Creating-A-Workspace.html)
- [REP-2000](https://www.ros.org/reps/rep-2000.html) — bảng tương thích giữa các phiên bản ROS 2 và Ubuntu.
- [Tài liệu colcon](https://colcon.readthedocs.io/en/released/user/quick-start.html) — tham khảo tùy chọn `colcon build --symlink-install`, rất hữu ích khi làm việc với các gói Python.
