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

Sau bài học này, bạn sẽ giải thích được kiến trúc XRCE-DDS gồm một client chạy trên vi điều khiển (MCU) kết hợp với một agent trên máy tính — trong đó agent mới là thực thể (participant) DDS trực tiếp tham gia đồ thị ROS 2. Bạn sẽ dự đoán chính xác rằng `ros2 topic list` không hiển thị topic của MCU khi agent tắt, và vẫn chưa hiển thị khi agent đã bật nhưng chưa có client kết nối. Bạn khởi chạy được container micro-ROS agent phiên bản Jazzy qua giao thức UDP, viết đúng cú pháp lệnh tương ứng cho chế độ serial theo tài liệu của agent, đồng thời nắm rõ lộ trình khóa học: hoàn thiện cầu nối serial bằng Python ở bài 10-04 trước, sau đó mới chuyển sang micro-ROS khi đơn vị vận tốc và watchdog 300 ms đã được kiểm chứng. Cuối bài, bạn lập bản kế hoạch topic cho client (dùng lại `/cmd_vel`, topic telemetry và tên frame đồng bộ với mô phỏng) ngay cả khi chưa nạp mạch thật.

## Kiến thức cần trước

Nắm vững mô hình node – topic ở bài 09-02, khung dữ liệu serial ở bài 08-01 và môi trường Jazzy ở bài 10-01. Bài lab yêu cầu cài sẵn Docker để chạy container agent. Trong buổi này bạn chưa cần tệp firmware micro-ROS hoàn chỉnh và không nên vội viết lại phần teleop của Capstone sang micro-ROS trước khi hoàn tất bài 10-04. Bo mạch được hỗ trợ trong bài là ESP32 DevKit (không áp dụng cho Raspberry Pi Pico).

## Vì sao bài này nằm trên lộ trình

Firmware Capstone hiện tại nhận khung dữ liệu `V,left,right` và tự động ngắt lực động cơ khi mất tín hiệu. ROS 2 không hiểu trực tiếp định dạng khung đó, còn ESP32 không đủ tài nguyên để chạy toàn bộ ngăn xếp DDS đầy đủ. Vì vậy, node cầu nối `rclpy` ở bài 10-04 là bước triển khai đầu tiên: dễ gỡ lỗi bằng Python, tái sử dụng giao thức đã kiểm chứng và vẫn có watchdog trên firmware bảo vệ nếu tiến trình cầu bị tắt đột ngột. micro-ROS là bước nâng cấp tiếp theo: client chạy ngay trên MCU, agent trên máy tính chuyển đổi XRCE-DDS sang DDS, cho phép `/cmd_vel` đi thẳng tới firmware mà không cần lớp quy đổi Python trung gian. Dù dùng cách nào, Nav2 và các mô hình học máy sau này vẫn chỉ xuất bản `Twist` — tuy nhiên chúng không thể giúp bạn gỡ lỗi một agent chưa từng kết nối với client.

![Client micro-ROS trên ESP32, agent trên máy tính, rồi đồ thị ROS 2]({{ site.imgurl }}/generated/ch10_microros.png)

## Khái niệm

DDS là lớp middleware nằm bên dưới các topic ROS 2, và mỗi node `rclpy` thông thường là một DDS participant đầy đủ. Các vi điều khiển tài nguyên hạn chế không thể chạy trực tiếp ngăn xếp này một cách hiệu quả về RAM và CPU. Chuẩn XRCE-DDS ra đời để giải quyết giới hạn đó: vi điều khiển chạy một micro-ROS client nhẹ và không tự xuất hiện trên đồ thị ROS; thay vào đó, tiến trình **agent** trên máy tính đóng vai trò participant đại diện. Khi client tạo subscriber hoặc publisher, agent sẽ khởi tạo thực thể ROS 2 tương ứng và chuyển tiếp dữ liệu giữa hai bên.

Cơ chế này giải thích vì sao danh sách topic ban đầu bị trống: khi agent chưa chạy thì không có đại diện nào cho MCU; còn khi agent đã bật nhưng ở trạng thái chờ, chưa có phiên làm việc (session) nào từ client nên các topic của MCU chưa được tạo. Việc chỉ thấy `/parameter_events` và `/rosout` chứng tỏ agent đang chờ bình thường chứ không phải lỗi cài đặt.

Khóa học dùng image Docker chính thức gắn đúng thẻ phiên bản `microros/micro-ros-agent:jazzy`. Trong bài lab không cần mạch thật, ta chạy agent theo giao thức UDP trên laptop:

```bash
docker run -it --rm --net=host microros/micro-ros-agent:jazzy udp4 --port 8888
```

Cờ `--net=host` đưa container vào chung không gian mạng của máy chủ để khi có client kết nối, hệ thống DDS trên laptop nhận diện được agent (mạng bridge mặc định của Docker sẽ ẩn agent khỏi `ros2 topic list` nếu không cấu hình DDS bổ sung). Cờ `--rm` tự dọn container sau khi thoát và không can thiệp vào hệ thống ROS Jazzy cài trên máy.

Khi kết nối ESP32 thật qua cổng USB-serial, Docker cần được cấp quyền truy cập thiết bị của máy chủ (`/dev`) và truyền tham số serial cho agent:

```bash
docker run -it --rm --privileged -v /dev:/dev --net=host \
  microros/micro-ros-agent:jazzy serial --dev /dev/ttyUSB0 -b 115200
```

Các cờ đứng trước tên image thuộc về Docker, còn các tham số sau từ khóa `serial` thuộc về agent (đường dẫn cổng và tốc độ baud khớp với chương 08; nếu có thay đổi cú pháp, ưu tiên theo README chính thức của agent). Tuyệt đối không chạy đồng thời container này với cầu nối Python ở bài 10-04 vì tại một thời điểm chỉ một tiến trình được quyền mở `/dev/ttyUSB0`.

Về phần cứng, ESP32 nằm trong nhóm vi điều khiển được micro-ROS hỗ trợ chính thức thông qua ESP-IDF. Ngược lại, Raspberry Pi Pico chỉ có bản chuyển đổi từ cộng đồng (thường theo distro khác và không đảm bảo tương thích với `microros/micro-ros-agent:jazzy`). Hãy dành Pico cho MicroPython và dùng ESP32 DevKit cho micro-ROS.

Khi nạp client về sau, cần giữ đồng nhất quy ước tên ROS với môi trường mô phỏng: subscribe `/cmd_vel` (`geometry_msgs/msg/Twist`), publish dữ liệu phản hồi lên `/capstone_telem` (`std_msgs/msg/String`), và nếu xuất bản odometry thì dùng đúng cặp frame `odom` và `base_link` theo REP-105 (bài 09-05). Bên trong firmware, lệnh bánh xe vẫn quy đổi về số nguyên trong đoạn −100…100 theo đúng hệ số ở bài 10-04; micro-ROS không làm thay đổi mô hình động học.

Quan trọng nhất, cơ chế watchdog không được chuyển lên agent. Agent có thể sập, Docker có thể mất quyền thiết bị hoặc mạng Wi-Fi UDP có thể gián đoạn; do đó firmware trên MCU vẫn bắt buộc đưa vận tốc bánh về 0 nếu quá 300 ms không nhận được lệnh mới:

$$
\Delta t > 0.3\,\mathrm{s} \Rightarrow (n_L, n_R) = (0, 0)
$$

Đây là cùng một ngưỡng an toàn như cầu nối serial. Việc giữ nguyên lệnh `Twist` cuối chỉ vì tin rằng "DDS đáng tin cậy" sẽ dẫn đến trạng thái hỏng nguy hiểm khi mất kết nối: độ tin cậy là đặc tính của kênh truyền, còn dừng an toàn phải là trách nhiệm tại chỗ của vi điều khiển.

Ngoài ra, không bao giờ cấp nguồn cho mạch điều khiển động cơ từ cổng USB đang nạp ESP32 hoặc chạy agent, vì sụt áp sẽ làm chip khởi động lại và ngắt phiên làm việc giữa chừng. Khi chuyển sang chạy phần cứng thật, động cơ phải dùng khối pin riêng có cầu chì và nối chung mass (GND).

## Ví dụ làm từng bước

Trước khi chạy Docker, hãy viết bản kế hoạch topic ra sổ thực hành (đây là một nửa yêu cầu của bài lab):

```text
Node name I will look for: /capstone_mcu
Subscribes: /cmd_vel   geometry_msgs/msg/Twist
Publishes:  /capstone_telem   std_msgs/msg/String
Frames if odometry is added later: odom -> base_link
Local rule: no fresh command for 300 ms => wheel integers 0,0
Not expected tonight: that node name in ros2 node list
```

Tiếp theo, kiểm tra phiên bản ROS và khởi chạy agent không gắn mạch:

```bash
printenv ROS_DISTRO
docker run -it --rm --net=host microros/micro-ros-agent:jazzy udp4 --port 8888
```

Đảm bảo `ROS_DISTRO` là `jazzy` và giữ container chạy ở cửa sổ chính. Agent hoạt động bình thường sẽ báo đang lắng nghe trên `udp4` cổng `8888` và không hiển thị phiên client nào.

Mở terminal thứ hai để kiểm tra đồ thị ROS:

```bash
source /opt/ros/jazzy/setup.bash
ros2 node list
ros2 topic list
```

Kết quả không được chứa `/capstone_mcu` — sự vắng mặt này chính là bằng chứng cho thấy agent chưa tạo thực thể khi chưa có client kết nối.

Nhấn Ctrl-C để dừng container, tránh chiếm giữ cổng 8888 cho các lần chạy sau. Khi kết nối mạch thật ở buổi thực hành phần cứng, log của agent sẽ ghi nhận phiên mới và `ros2 node list` sẽ hiện đúng tên node bạn đã lên kế hoạch.

## Lab

1. Đọc lại kiến trúc micro-ROS kèm README của agent; xác nhận sử dụng đúng thẻ image `jazzy` (không dùng `humble` hay `iron`).
2. Chép bản kế hoạch topic mẫu vào `lab-notes.md`, đảm bảo ghi rõ luật dừng cục bộ 300 ms và cặp frame `odom`, `base_link`.
3. Chạy container agent UDP theo đúng lệnh đã nêu và chờ log xác nhận đang lắng nghe trên `udp4` cổng `8888` (lần đầu tải image có thể mất vài phút).
4. Mở terminal khác, nạp Jazzy, chạy `ros2 node list` và `ros2 topic list`, dán kết quả vào sổ kèm câu giải thích vì sao node MCU chưa xuất hiện.
5. Chưa cần nạp firmware trong buổi này (trừ khi bạn đã có sẵn ảnh micro-ROS muốn thử thêm); log agent đang chờ kèm bản kế hoạch là đủ tiêu chuẩn hoàn thành lab.
6. Dừng container. Nếu ghi chú thêm lệnh chạy chế độ serial, phải liệt kê đủ `--privileged`, `-v /dev:/dev`, `--dev /dev/ttyUSB0` và lưu ý không chạy song song với cầu nối Python.

**Kết quả mong đợi**

Container chạy ổn định ở foreground, log xác nhận lắng nghe UDP cổng 8888 và chưa có client; `ros2 node list` không chứa `/capstone_mcu`; sổ thực hành ghi đầy đủ thông tin subscribe, publish và quy tắc watchdog 300 ms:

```text
agent waiting on udp4 port 8888
ros2 node list: no MCU node
lab-notes: cmd_vel in, capstone_telem out, frames odom and base_link
```

**Các lỗi thường gặp**

| Hiện tượng | Nguyên nhân thường gặp |
| --- | --- |
| `docker: command not found` | Chưa cài đặt Docker Engine trên máy |
| Lỗi từ chối quyền truy cập socket Docker | User chưa thuộc nhóm `docker` hoặc chưa đăng nhập lại (có thể dùng tạm `sudo`) |
| Kéo nhầm thẻ image `humble` | Không tương thích phiên bản ROS trên laptop; đổi sang thẻ `:jazzy` |
| Không thấy node MCU trong `ros2 node list` nên cài lại ROS | Chưa có client kết nối — trạng thái trống là hoàn toàn bình thường |
| Cả agent serial và cầu Python cùng mở `/dev/ttyUSB0` | Xung đột quyền chiếm cổng serial; phải tắt một trong hai tiến trình |
| ESP32 tự reset khi cấp lệnh quay bánh | Động cơ lấy chung nguồn USB với mạch; cần tách sang nguồn pin riêng của xe |
| Lỗi biên dịch theo hướng dẫn micro-ROS cho Pico | Pico chỉ có bản hỗ trợ không chính thức từ cộng đồng, không thuộc lộ trình ESP32 |

## Mua ở Việt Nam

Buổi chạy thử nghiệm này chỉ cần Docker trên laptop, không cần phần cứng mới. Khi chuyển sang nạp mạch thật, dùng đúng bo ESP32 DevKit của Capstone A (tìm từ khóa "ESP32" trên [hshop.vn](https://hshop.vn/) hoặc `ESP32 DevKit V1 30 chân` trên Shopee/Lazada, giá tham khảo 2026 khoảng 80.000–180.000 đồng — tránh mua module trần không có chip USB). Không mua Pico cho bài này và không cấp nguồn động cơ từ cáp USB.

## Video tham khảo

- **Xem trước:** [Intro to micro-ROS](https://www.youtube.com/watch?v=aD3Lf-9cb0A) — Marine Robotics Group at Georgia Tech (tiếng Anh). Giải thích tổng quan cách MCU giao tiếp DDS thông qua agent.
- [How to start develop micro-ROS on ESP32 quickly!](https://www.youtube.com/watch?v=48SxC6LBVs8) — stepbystep-robotics (tiếng Anh). Thực hành micro-ROS trên ESP32 và agent; nếu video dùng thẻ image khác `jazzy`, hãy giữ đúng thẻ của bài học này.

## Bài tập

1. Khi container agent đang chạy nhưng bạn chưa nạp firmware cho mạch, `ros2 topic list` chắc chắn không hiển thị điều gì và vì sao? *Gợi ý:* không hiển thị các topic của MCU, vì agent chỉ khởi tạo chúng sau khi thiết lập được phiên làm việc với client.
2. Dù bài này nằm trước bài 10-04 về thứ tự đánh số, vì sao khóa học vẫn khuyến nghị hoàn thiện cầu nối serial Python trước? *Gợi ý:* firmware Capstone đã hỗ trợ sẵn khung truyền chương 08; xây dựng cầu nối Python giúp kiểm chứng đơn vị vận tốc và watchdog 300 ms trước khi chuyển sang tầng phức tạp hơn là micro-ROS.
3. Viết lệnh `docker run` cho agent serial trên `/dev/ttyUSB0` và phân biệt rõ những cờ nào thuộc về Docker, những cờ nào thuộc về agent. *Gợi ý:* `--privileged`, `-v /dev:/dev` và `--net=host` thuộc Docker; `--dev` và `-b` đứng sau từ khóa `serial` thuộc về agent.
4. Tóm tắt giao ước của client trong bốn dòng: topic subscribe, topic publish, tên frame và timeout. *Gợi ý:* subscribe `/cmd_vel` (`Twist`), publish `/capstone_telem` (`String`), frame `odom` và `base_link`, đưa lệnh về 0 sau 300 ms không có dữ liệu mới.
5. Nếu một người bạn muốn tận dụng bo Raspberry Pi Pico có sẵn để làm bài micro-ROS này, bạn sẽ nhận xét ngắn gọn trong hai câu như thế nào? *Gợi ý:* ESP32 là dòng mạch được hỗ trợ chính thức cho agent Jazzy của khóa học; Pico chỉ có bản chuyển đổi cộng đồng nên không đảm bảo tương thích và không nằm trong lộ trình bài thực hành.

## Đọc thêm

- [micro-ROS](https://micro.ros.org/) — tài liệu tổng quan về kiến trúc client – XRCE-DDS – agent.
- [Kho agent micro-ROS](https://github.com/micro-ROS/micro-ROS-Agent) — nơi lưu các câu lệnh Docker chuẩn cho cả `udp4` và `serial` (ưu tiên kiểm tra tại đây nếu cú pháp cờ thay đổi).
- [REP-105](https://www.ros.org/reps/rep-0105.html) — chuẩn tên frame cần giữ đồng nhất giữa mô phỏng và vi điều khiển.
