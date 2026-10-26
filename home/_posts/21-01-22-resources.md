---
layout: post
title: "Tài nguyên"
chapter: home
order: 7
owner: Nguyen Le Linh
---

## Tài nguyên

Link dưới đây trả về trang khi kiểm tra tháng 10 năm 2026. Trang shop là cổng tìm kiếm hoặc trang chủ: kết quả đổi theo tồn kho, không phải một món đã chốt giá. Giá điền vào BOM khi bạn mở listing. Đường ROS trên khóa là rclpy và rclcpp. [rclgo](https://github.com/tiiuae/rclgo) là đường phụ.

## Tài liệu chính

[ROS 2 Jazzy](https://docs.ros.org/en/jazzy/) là bản đi với Ubuntu 24.04. Cài bằng [Ubuntu deb packages](https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html), rồi làm [tutorials](https://docs.ros.org/en/jazzy/Tutorials.html). Trên Pi, đọc [Installing ROS 2 on a Raspberry Pi](https://docs.ros.org/en/jazzy/How-To-Guides/Installing-on-Raspberry-Pi.html) sau khi máy đã là Ubuntu 24.04, không phải Raspberry Pi OS. Ảnh Ubuntu 24.04 nằm ở [cdimage 24.04](https://cdimage.ubuntu.com/ubuntu/releases/24.04/release/). Trang [Ubuntu cho Raspberry Pi](https://ubuntu.com/download/raspberry-pi) và [hướng dẫn cài](https://ubuntu.com/tutorials/how-to-install-ubuntu-on-your-raspberry-pi) có thể đề 26.04; khóa này vẫn dùng 24.04 vì kho Jazzy.

Khung và thời gian: [About TF2](https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-TF2.html), [ROS_DOMAIN_ID](https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Domain-ID.html), [URDF](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/URDF/URDF-Main.html), [REP-103](https://www.ros.org/reps/rep-0103.html), [REP-105](https://www.ros.org/reps/rep-0105.html).

Mô phỏng: [Gazebo Harmonic, bắt đầu](https://gazebosim.org/docs/harmonic/getstarted/), [cài với ROS](https://gazebosim.org/docs/harmonic/ros_installation), mã [ros_gz](https://github.com/gazebosim/ros_gz). Docker: [ảnh ros](https://hub.docker.com/_/ros) (chọn tag Jazzy đang liệt kê), [hai node trong container](https://docs.ros.org/en/jazzy/How-To-Guides/Run-2-nodes-in-single-or-separate-docker-containers.html), [Docker Engine trên Ubuntu](https://docs.docker.com/engine/install/ubuntu/).

Định vị và đi: [Nav2](https://docs.nav2.org/), tutorial Jazzy [Navigation2 with SLAM](https://docs.nav2.org/jazzy/tutorials/general_tutorials/navigation2_with_slam/navigation2_with_slam/), mã [navigation2](https://github.com/ros-navigation/navigation2), [slam_toolbox](https://github.com/SteveMacenski/slam_toolbox). Tay và điều khiển khớp: [MoveIt 2](https://moveit.picknik.ai/main/index.html), [ros2_control](https://control.ros.org/), [ros2_controllers](https://github.com/ros-controls/ros2_controllers). Xe mẫu: [linorobot2](https://github.com/linorobot/linorobot2).

micro-ROS: [micro.ros.org](https://micro.ros.org/), [micro-ROS-Agent](https://github.com/micro-ROS/micro-ROS-Agent), [micro_ros_setup](https://github.com/micro-ROS/micro_ros_setup). Đừng giả định gói `ros-jazzy-micro-ros-agent` có trên apt; tìm bằng `apt-cache`, không có thì build agent. Unit systemd: [systemd.service](https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html).

Nhúng: [ESP-IDF get started](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/get-started/index.html), [PlatformIO](https://docs.platformio.org/), [Arduino docs](https://docs.arduino.cc/), [MQTT](https://mqtt.org/). Mức logic: [SparkFun logic levels](https://learn.sparkfun.com/tutorials/logic-levels). Driver tham chiếu: [Pololu 713, TB6612FNG](https://www.pololu.com/product/713).

SBC NVIDIA: [Orin Nano quick start](https://docs.nvidia.com/jetson/orin-nano-devkit/user-guide/latest/quick_start.html), [JetPack install](https://docs.nvidia.com/jetson/jetpack/install-setup/index.html). Chủ đề diễn đàn [Jazzy với JetPack 7.2.1 trên Ubuntu 24.04](https://forums.developer.nvidia.com/t/is-ros2-jazzy-the-correct-version-to-use-with-jetpack-7-2-1-ubuntu-24-04/382439) (tháng 9 năm 2026) nói Jazzy là bản ROS khớp JetPack 7. JetPack 6 vẫn là Ubuntu 22.04.

Lidar rẻ trong Capstone B: [RPLIDAR A1](https://www.slamtec.com/en/Lidar/A1), driver [rplidar_ros nhánh ros2](https://github.com/Slamtec/rplidar_ros), [LD06 / ldlidar_stl_ros2](https://github.com/ldrobotSensorTeam/ldlidar_stl_ros2), trang [LDRobot](https://www.ldrobot.com/). README Slamtec liệt kê Humble, Galactic, Foxy; nếu colcon lỗi trên Jazzy thì dừng và ghi log.

Pin: [BU-205 các loại Li-ion](https://batteryuniversity.com/article/bu-205-types-of-lithium-ion), [BU-409 sạc Li-ion](https://batteryuniversity.com/article/bu-409-charging-lithium-ion), [BU-409b sạc LiFePO4](https://batteryuniversity.com/article/bu-409b-charging-lithium-iron-phosphate).

## Khóa và sách mở

[Modern Robotics](https://modernrobotics.northwestern.edu/) và bản wiki [Modern Robotics](https://hades.mech.northwestern.edu/index.php/Modern_Robotics) cho động học, trước và sau bài toán chương 08. [MIT Manipulation](https://manipulation.mit.edu/) và [Underactuated Robotics](https://underactuated.mit.edu/) là đọc thêm, không nằm trong 24 tuần. PID thực hành: [Control Guru, mục lục](https://controlguru.com/table-of-contents/). Cây hành vi: [BehaviorTree.CPP](https://www.behaviortree.dev/). Duckietown đổi tài liệu sang [docs.duckietown.com/ente](https://docs.duckietown.com/ente/).

## Robot learning

[LeRobot](https://github.com/huggingface/lerobot), [cài đặt](https://huggingface.co/docs/lerobot/installation), [SO-101](https://huggingface.co/docs/lerobot/so101), [imitation trên robot](https://huggingface.co/docs/lerobot/il_robots). Trang imitation dùng `--policy.type=act` trong ví dụ train. [ALOHA / ACT](https://tonyzhaozh.github.io/aloha/), [Diffusion Policy](https://diffusion-policy.cs.columbia.edu/), bài [arxiv 2303.04137](https://arxiv.org/abs/2303.04137). VLA: [RT-1](https://robotics-transformer1.github.io/), [RT-2, arXiv:2307.15818](https://arxiv.org/abs/2307.15818), [Open X-Embodiment](https://robotics-transformer-x.github.io/), [OpenVLA](https://openvla.github.io/) và [arXiv:2406.09246](https://arxiv.org/abs/2406.09246), [π0](https://www.pi.website/blog/pi0).

## YouTube

Kênh giữ cho tên gói và bản phát hành: [ROS](https://www.youtube.com/@ROSOrg), [Gazebo](https://www.youtube.com/@gazebosim), [NVIDIA Developer](https://www.youtube.com/@NVIDIADeveloper), [Raspberry Pi](https://www.youtube.com/@raspberrypi), [Hugging Face](https://www.youtube.com/@HuggingFace). Đi từng bước Jazzy trên xe nhỏ: [Articulated Robotics](https://www.youtube.com/c/ArticulatedRobotics) và trang [articulatedrobotics.xyz](https://articulatedrobotics.xyz/). Video không thay lệnh trong bài; khi lệch bản distro, tin docs và bài lab.

## Cửa hàng linh kiện ở Việt Nam

Mở trang, đối chiếu ảnh và thông số, rồi tự điền giá. Đã mở được tháng 10 năm 2026:

- [Hshop](https://hshop.vn/) — tìm [Raspberry Pi](https://hshop.vn/search?q=raspberry+pi), [lidar](https://hshop.vn/search?q=lidar), [LiPo](https://hshop.vn/search?q=lipo). Giá một số món bàn lab trong BOM là snapshot ngày 23 tháng 9 năm 2026 trên chính listing đó.
- [Thế Giới IC](https://www.thegioiic.com/), [IC Đây Rồi](https://icdayroi.com/), [Điện Tử 4U](https://dientu4u.com/), [Bán Linh Kiện](https://banlinhkien.com/).
- [Shopee](https://shopee.vn/): [Raspberry Pi 5](https://shopee.vn/search?keyword=raspberry%20pi%205), [Jetson Orin Nano](https://shopee.vn/search?keyword=jetson%20orin%20nano), [lidar](https://shopee.vn/search?keyword=lidar), [BMS 2S](https://shopee.vn/search?keyword=bms%202s).
- [Lazada](https://www.lazada.vn/): [BMS 2S](https://www.lazada.vn/catalog/?q=bms%202s), [lidar](https://www.lazada.vn/catalog/?q=lidar).

Đối chiếu hóa học pin trên tem với sạc. LiFePO4 không sạc bằng hồ sơ 4,20 V/cell của Li-ion.

## Video theo chương

Mỗi chương một video nên xem trước. Tiêu đề và kênh lấy từ oEmbed ngày 26 tháng 10 năm 2026. Các bài trong chương có thêm một đến ba video ở mục Video tham khảo.

- Chương 00: [What Is ROS2? - Framework Overview](https://www.youtube.com/watch?v=7TVWlADXwRw) — Raymond Andrade. Giới thiệu ROS 2 trước khi chọn lộ trình.
- Chương 01: [Ohms Law Explained - The basics circuit theory](https://www.youtube.com/watch?v=HsLLq6Rm5tU) — The Engineering Mindset. Định luật Ôm, nền của chương điện.
- Chương 02: [Lập trình ESP32 - Bài 1 - Cách nạp chương trình cho ESP32 bằng Arduino IDE - Tự học lập trình IOT](https://www.youtube.com/watch?v=sJtJJU3c3xE) — Điện thông minh E-smart. Nạp chương trình nhấp LED cho ESP32, tiếng Việt.
- Chương 03: [Understanding State Machines, Part 1: What Are They?](https://www.youtube.com/watch?v=-Yicg2TTMPs) — MATLAB. Máy trạng thái, hình của firmware chương 03.
- Chương 04: [Serial Communications Explained: UART, I2C, and SPI](https://www.youtube.com/watch?v=IyGwvGzrqp8) — Electronoobs. UART, I2C, SPI trên một video.
- Chương 05: [TB6612FNG H-Bridge Motor Controller - Better than L298N?](https://www.youtube.com/watch?v=JPPTRj0KWbg) — DroneBot Workshop. TB6612 cạnh L298N, đúng bài nhận driver.
- Chương 06: [Differential Drive & Odometry Explained: How It Works](https://www.youtube.com/watch?v=2QE3LG5h2tw) — Netizen Robotics. Vi sai và odometry, khung của chương cơ khí.
- Chương 07: [BMS (Battery Management System) || DIY or Buy || Properly protecting Li-Ion/Li-Po Battery Packs](https://www.youtube.com/watch?v=rT-1gvkFj60) — GreatScott!. BMS và pack lithium trước khi lắp xe.
- Chương 08: [PID Control - A brief introduction](https://www.youtube.com/watch?v=UR0hOmjaHp0) — Brian Douglas. PID, bài chỉnh số của chương.
- Chương 09: [The ROS Transform System (TF) | Getting Ready to Build Robots with ROS #6](https://www.youtube.com/watch?v=QyvHhY4Y_Y8) — Articulated Robotics. Cây TF2, cửa sang chương mô phỏng.
- Chương 10: [Correctly Install Gazebo Harmonic Inside of ROS2 Jazzy Installation -Fix Gazebo Installation Issues](https://www.youtube.com/watch?v=dY8JxldcuqA) — Aleksandar Haber PhD. Gazebo Harmonic trong môi trường Jazzy.
- Chương 11: [Making robot navigation easy with Nav2 and ROS!](https://www.youtube.com/watch?v=jkoGkAd0GYk) — Articulated Robotics. Nav2, tour rồi lab Capstone B.
- Chương 12: [How to Train an AI Robotic Arm With No Code (Hugging Face LeRobot + SO-101)](https://www.youtube.com/watch?v=7tGT8hqRSAo) — Brogan M. Pratt. LeRobot và tay SO-101.

## Video Việt Nam: Chinbi Robot (ICTU)

Hoàng Quân, giảng viên Cơ điện tử ICTU, đăng các Facebook Reel ngắn của dự án robot bốn chân Chinbi. Trang dự án ghi trong chú thích là [chinbi.com](https://chinbi.com), đã mở được tháng 10 năm 2026. Cột ngày trong danh sách nguồn để trống, nên trang này không ghi ngày đăng. Mỗi dòng dưới đây là một reel đã đưa vào một bài. Câu xem-cái-gì nằm trong bài đó, và chỉ bám chú thích.

Ba reel không đưa vào khóa: bài đăng lại về công ty robot nước ngoài, chuyến tham quan nhà máy ô tô, và phỏng vấn về startup làm mát trung tâm dữ liệu.

- [Cơ điện tử học làm robot](https://www.facebook.com/reel/1746806056360278) — bài chào mừng, chương 00.
- [Sinh viên lập trình robot thông minh](https://www.facebook.com/reel/1381152347317660), [Robocon Bắc Ninh 2026](https://www.facebook.com/reel/2015462409114750), [Robocon Bắc Ninh tháng 8 năm 2026](https://www.facebook.com/reel/4471403513091271) — máy trạng thái, chương 03.
- [Test thiết kế chân](https://www.facebook.com/reel/1615249330240344), [một chân ba bậc tự do](https://www.facebook.com/reel/2974137376266883) — cơ cấu thanh, chương 06.
- [Test pin drone, ESC cháy](https://www.facebook.com/reel/931720623225817) — pin và an toàn nguồn, chương 07.
- [Test hệ thống điều khiển](https://www.facebook.com/reel/1092867967065031), [demo robot](https://www.facebook.com/reel/1057849570224248) — firmware teleop, chương 07.
- [Flight controller, muốn bay ngay](https://www.facebook.com/reel/976436878550867) — PID, chương 08.
- [Thả ra là bay](https://www.facebook.com/reel/2056881368258089), [UAV vận tải](https://www.facebook.com/reel/1038211995413233), [bước đầu drone vận tải](https://www.facebook.com/reel/1004870148832135) — chu kỳ vòng điều khiển, chương 08.
- [Dữ liệu 3D từ một vị trí trên trái đất](https://www.facebook.com/reel/2078352426052273) — Gazebo Harmonic, chương 10.
- [MuJoCo recovery](https://www.facebook.com/reel/1773957523904144), [training bậc thang rồi sim-to-real](https://www.facebook.com/reel/2246938909200876) — checklist sim-to-real, chương 10.
- [Thuật toán về nhà](https://www.facebook.com/reel/1391050009535827) — tour Nav2, chương 11.
- [Đi bộ có tải, reinforcement learning](https://www.facebook.com/reel/4089347134533915), [đứng hai chân](https://www.facebook.com/reel/1624642749368249), [hai chân trước / handstand](https://www.facebook.com/reel/2292393271597807), [trèo bậc / nhảy lên cầu thang](https://www.facebook.com/reel/2191042771623926) — mở đầu robot learning, chương 12.
