---
layout: post
title: "micro-ROS trên MCU"
chapter: "10"
order: 3
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter10
lesson_type: required
draft: false
---

Thời lượng: **~75 phút**.

## Mục tiêu

Bạn mô tả XRCE-DDS như một client trên vi điều khiển cộng một agent trên máy tính, và agent mới là participant DDS thật trong đồ thị ROS 2. Bạn đoán trước, trước khi chạy gì, rằng `ros2 topic list` không có topic của MCU khi agent tắt, và vẫn không có khi agent đã bật nhưng chưa client nào nối. Bạn khởi động container agent micro-ROS bản Jazzy theo UDP và viết dạng serial tương ứng với các cờ thiết bị trong README agent. Bạn nói được thứ tự khóa học: cầu nối Python serial ở bài sau đi trước, micro-ROS chờ đến khi đơn vị của cầu đó và watchdog 300 ms đã chạy. Bạn để lại một kế hoạch topic của client, dùng lại `/cmd_vel`, telemetry đi ra, và cùng tên frame với bộ mô phỏng, kể cả khi tối nay không nạp board.

## Kiến thức cần trước

Hình node và topic của bài 09-02, khung serial bài 08-01, và shell Jazzy bài 10-01. Lab cần Docker cho lệnh agent. Tối nay không cần ảnh firmware micro-ROS chạy được, và đừng dựng lại teleop Capstone quanh micro-ROS trước khi bài 10-04 đạt. ESP32 DevKit là board bài này nói tới. Pico có thể nằm trong ngăn kéo; đó không phải đường được hỗ trợ ở dưới.

## Vì sao bài này nằm trên lộ trình

Firmware Capstone đã nhận `V,left,right` và đã nhả mô-men khi những khung đó ngừng. ROS 2 không nói khung đó, và ESP32 trong khóa học không nói DDS đầy đủ. Node `rclpy` bài 10-04 là bộ dịch bạn chạy trước: Python thường, giao thức bạn đã gỡ lỗi, và tiến trình bị giết vẫn được watchdog firmware che. micro-ROS đến sau. Client sống trên MCU, agent trên máy tính đổi XRCE thành DDS, rồi `/cmd_vel` tới firmware mà không cần hàm tỉ lệ Python đứng giữa. Nav2 và một policy học sau này vẫn xuất bản Twist theo cả hai cách. Chúng sẽ không gỡ một agent chưa từng thấy client.

![Client micro-ROS trên ESP32, agent trên máy tính, rồi đồ thị ROS 2]({{ site.imgurl }}/generated/ch10_microros.png)

## Khái niệm

DDS là middleware dưới topic ROS 2. Node `rclpy` bình thường là một participant. Vi điều khiển nhỏ chỉ chạy stack đó với nhiều đau và nhiều RAM. XRCE-DDS là profile client cho ràng buộc đó. Board chạy client micro-ROS, và client không tự hiện trên đồ thị ROS. Agent, một tiến trình trên máy tính, mới là participant. Client tạo subscriber hoặc publisher thì agent tạo thực thể ROS 2 tương ứng và chuyển byte.

Sự kiện đó chính là danh sách topic trống. Không có agent thì không ai đứng cho board. Agent chỉ đang chờ thì vẫn chưa có phiên client, nên các thực thể chưa từng được tạo. Chỉ thấy `/parameter_events` và `/rosout` nghĩa là agent đang nghỉ, không phải bản cài hỏng.

Agent của khóa học là image Docker gắn thẻ distro này, `microros/micro-ros-agent:jazzy`. UDP trên laptop, lab tối nay vì không cần board, theo dạng README của agent:

```bash
docker run -it --rm --net=host microros/micro-ros-agent:jazzy udp4 --port 8888
```

`--net=host` đặt container vào namespace mạng của máy chủ để sau này, khi đã có client, DDS trên laptop nhìn thấy agent. Mạng bridge không có cấu hình DDS thêm sẽ giấu agent khỏi `ros2 topic list` kể cả sau phiên thành công. `--rm` xóa container khi bạn thoát. Không có gì được cài vào underlay Jazzy.

Serial là đường bạn dùng khi ESP32 hiện thành thiết bị USB-serial. Docker phải được phép thấy node thiết bị của máy chủ. Dạng README là container có quyền, gắn `/dev`, rồi đến đối số serial của chính agent, gồm đường thiết bị:

```bash
docker run -it --rm --privileged -v /dev:/dev --net=host \
  microros/micro-ros-agent:jazzy serial --dev /dev/ttyUSB0 -b 115200
```

Cờ đứng trước tên image là của Docker. Đối số sau chữ `serial` là của agent: thiết bị và baud, khớp chương 08. Cờ nào lệch thì README agent thắng. Đừng chạy container này cùng lúc với cầu Python bài 10-04. Một tiến trình được sở hữu `/dev/ttyUSB0`.

ESP32 là lớp board micro-ROS coi là được hỗ trợ, có đường ESP-IDF nhắm vào agent này. Pico có cổng cộng đồng: tutorial có thể theo distro khác, và không ai hứa `microros/micro-ros-agent:jazzy` là đầu kia. Giữ Pico cho MicroPython. Dùng ESP32 DevKit cho agent này.

Client bạn nạp sau này phải dùng tên ROS của bộ mô phỏng. Nó subscribe `/cmd_vel` kiểu `geometry_msgs/msg/Twist` và publish `std_msgs/msg/String` lên `/capstone_telem`. Nếu nó publish odometry, frame là `odom` và `base_link`, tên REP-105 của bài 09-05. Lệnh bánh trong firmware vẫn là số nguyên −100…100 sau đúng tỉ lệ bài 10-04 ghi. micro-ROS không bãi bỏ động học.

Watchdog không dọn sang agent. Agent có thể sập, Docker có thể mất thiết bị, UDP Wi-Fi có thể im. Firmware vẫn phải ép lệnh bánh về không khi 300 ms không có lệnh mới:

$$
\Delta t > 0.3\,\mathrm{s} \Rightarrow (n_L, n_R) = (0, 0)
$$

Đó là cùng con số với cầu serial. Client áp Twist cuối mãi vì “DDS đáng tin” là hỏng theo hướng mở. Độ tin ở đây là tính chất của đường truyền bạn hy vọng còn. Cái dừng là tính chất của board.

Đừng nuôi driver động cơ từ cổng USB đang nạp ESP32 hoặc đang mang agent. Nguồn laptop sụt, chip reset, phiên chết giữa lệnh. Động cơ ở trên pack có cầu chì, mass chung, vào ngày bạn rời buổi chạy khô. Tối nay không cần pack đó.

## Ví dụ làm từng bước

Viết kế hoạch topic ra giấy trước khi bật Docker. Một đoạn là đủ, và đó là nửa điểm lab:

```text
Node name I will look for: /capstone_mcu
Subscribes: /cmd_vel   geometry_msgs/msg/Twist
Publishes:  /capstone_telem   std_msgs/msg/String
Frames if odometry is added later: odom -> base_link
Local rule: no fresh command for 300 ms => wheel integers 0,0
Not expected tonight: that node name in ros2 node list
```

Rồi bật agent, không gắn board:

```bash
printenv ROS_DISTRO
docker run -it --rm --net=host microros/micro-ros-agent:jazzy udp4 --port 8888
```

`ROS_DISTRO` phải là `jazzy` ở shell bạn dùng để soi đồ thị. Để container ở mặt trước. Agent nghỉ lành mạnh thì tiếp tục chạy và nêu `udp4` cùng cổng `8888`. Nó không in phiên client, vì bạn không mở phiên nào.

Terminal thứ hai:

```bash
source /opt/ros/jazzy/setup.bash
ros2 node list
ros2 topic list
```

`/capstone_mcu` không được có trong danh sách. Vắng node MCU chính là quan sát. Một publisher demo ngẫu nhiên không lập hợp đồng Capstone. Bỏ qua, hoặc đừng để nó thành giao diện của robot.

Ctrl-C để dừng container, kẻo lần sau cổng 8888 đã bị giữ. Khi client thật nối về sau, log agent thêm một phiên và `ros2 node list` thêm đúng node bạn đã đặt tên. Viết câu dự đoán đó vào ghi chú tối nay; buổi phần cứng sau sẽ kiểm.

## Lab

1. Đọc kiến trúc bài này một lần, README agent mở bên cạnh. Xác nhận thẻ image là `jazzy`, không phải `humble` hay `iron`.
2. Chép kế hoạch topic trong ví dụ vào `lab-notes.md`, gồm luật dừng cục bộ 300 ms và tên frame `odom`, `base_link`.
3. Chạy container agent UDP đúng như đã viết. Đợi log nghỉ trên `udp4` cổng `8888`. Lần kéo image đầu có thể lâu; để nó xong.
4. Terminal khác, source Jazzy, chạy `ros2 node list` và `ros2 topic list`. Chép cả hai vào ghi chú. Viết một câu: node MCU đã định vắng mặt vì chưa có phiên client.
5. Đừng nạp firmware tối nay trừ khi bạn đã có ảnh micro-ROS và muốn làm thêm. Không nạp được thì lab vẫn đạt: log agent đang chờ cộng kế hoạch viết tay là bài nộp.
6. Dừng container. Nếu bạn cũng phác lệnh serial, ghi chú phải có `--privileged`, `-v /dev:/dev`, và `--dev /dev/ttyUSB0`, cùng câu không chạy lệnh đó cùng cầu Python.

**Kết quả mong đợi**

Container ở lại mặt trước. Log chỉ UDP cổng 8888 và không nhận đã có client. `ros2 node list` không chứa `/capstone_mcu` hay tên bạn đã giữ trong kế hoạch. Ghi chú có subscription, publication, và luật 300 ms.

```text
agent waiting on udp4 port 8888
ros2 node list: no MCU node
lab-notes: cmd_vel in, capstone_telem out, frames odom and base_link
```

**Khi hỏng thì thường vì**

| Bạn thấy | Nguyên nhân hay gặp |
| --- | --- |
| `docker: command not found` | Chưa cài Docker. Lab cần engine, không cần thêm một bản ROS |
| Từ chối quyền trên socket Docker | User không ở nhóm `docker`, hoặc chưa đăng nhập lại sau khi thêm nhóm. `sudo` là lối tạm |
| Kéo và chạy thẻ image `humble` | Agent đó nói kiểu của distro khác. Dùng `:jazzy` cho khớp laptop |
| `ros2 node list` không có node MCU, và bạn cài lại ROS | Chưa client nào nối. Danh sách trống đó là kết quả nghỉ đúng |
| Agent serial và cầu Python cùng mở `/dev/ttyUSB0` | Hai chủ một thiết bị. Dừng một bên |
| Board reset khi ra lệnh bánh | Động cơ ăn cùng đường USB với agent serial. Dùng pack robot, không dùng cổng laptop |
| Cờ build của tutorial Pico thất bại với image này | micro-ROS trên Pico là vùng cổng cộng đồng, không phải đường ESP32 được hỗ trợ |

## Mua ở Việt Nam

Buổi chạy khô cần Docker trên laptop, không cần PCB mới. Khi nạp, dùng ESP32 DevKit cùng lớp với Capstone A. Tìm “ESP32” trên [hshop.vn](https://hshop.vn/). Từ khóa Shopee hoặc Lazada: `ESP32 DevKit V1 30 chân`. Khoảng 2026 khoảng 80.000–180.000 đồng; kiểm tra trước khi trả, và bỏ module trần không chip USB nếu bạn muốn DevKit. Đừng mua Pico cho bài này, và đừng nuôi động cơ từ cáp USB.

## Bài tập

1. Container agent đang chạy và bạn chưa nạp gì. `ros2 topic list` phải từ chối hiện cái gì, và vì sao? Gợi ý: nó phải từ chối topic của MCU, vì agent chỉ tạo các thực thể đó sau một phiên client.
2. File này đánh số trước bài cầu serial. Vì sao khóa học vẫn bảo làm xong cầu đó trước? Gợi ý: firmware Capstone đã nói khung chương 08, và micro-ROS là bước sau khi đơn vị và watchdog 300 ms đã được chứng minh.
3. Viết dòng `docker run` cho agent serial trên `/dev/ttyUSB0` và đánh dấu cờ nào thuộc Docker. Gợi ý: `--privileged` và `-v /dev:/dev` là Docker; `--dev` và baud thuộc agent, đứng sau chữ `serial`.
4. Phác hợp đồng client trong bốn dòng: topic và kiểu subscribe, topic và kiểu publish, frame id, timeout. Gợi ý: `/cmd_vel` kiểu Twist đi vào, `/capstone_telem` kiểu String đi ra, frame `odom` và `base_link`, về không sau 300 ms.
5. Bạn học muốn lấy Pico làm board micro-ROS vì nó đang nằm trên bàn. Bạn nói gì về mức hỗ trợ, trong hai câu? Gợi ý: ESP32 là lớp được hỗ trợ cho agent này; cổng Pico là việc cộng đồng và không phải đường bài này bảo mua hoặc nạp.

## Đọc thêm

- [micro-ROS](https://micro.ros.org/) là tổng quan dự án: client trên MCU, agent trên máy tính, XRCE-DDS ở giữa.
- [Kho agent micro-ROS](https://github.com/micro-ROS/micro-ROS-Agent) giữ các lệnh Docker bài này chép, gồm vận chuyển `udp4` và `serial`. Ưu tiên kho đó nếu một cờ trôi.
- [REP-105](https://www.ros.org/reps/rep-0105.html) là hợp đồng tên frame mà kế hoạch client dùng lại, để mô phỏng và board không bịa hai cây.
