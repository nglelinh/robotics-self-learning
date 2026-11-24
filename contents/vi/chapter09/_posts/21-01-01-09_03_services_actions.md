---
layout: post
title: "Service và action"
chapter: "09"
order: 3
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter09
lesson_type: required
draft: false
---

Thời lượng: **~75 phút**.

Topic dạng dòng chảy liên tục rất tuyệt cho cảm biến LiDAR hay vận tốc bánh xe, nhưng lại cực kỳ bất tiện khi bạn muốn hỏi *"Lưu bản đồ này xong chưa?"* hoặc ra lệnh *"Hãy di chuyển tới phòng 302, báo tiến độ mỗi giây và dừng ngay nếu tôi bấm Hủy!"*. Đó là lý do ROS 2 cung cấp thêm hai mẫu giao tiếp bậc cao hơn: **Service** (hỏi–đáp đồng bộ ngắn) và **Action** (tác vụ dài có phản hồi tiến độ và hỗ trợ hủy).

## Bản đồ kiến thức nền: So sánh ba mẫu giao tiếp trong ROS 2

1. **Topic (Luồng một chiều, nhiều–nhiều)**:
   Dành cho dữ liệu liên tục có tần suất (cảm biến, odometry, `cmd_vel`). Không xác nhận đã nhận từng gói.
2. **Service (Yêu cầu – Phản hồi ngắn, 1–1)**:
   Dành cho thao tác nhanh, rời rạc cần kết quả xác nhận (reset odometry, đổi chế độ lái, bật/tắt rơ-le). Không được dùng cho tác vụ kéo dài nhiều giây vì sẽ chặn luồng xử lý.
3. **Action (Goal – Feedback – Result + Cancel)**:
   Xây dựng từ bộ ba kênh (gửi mục tiêu, nhận tiến độ định kỳ, nhận kết quả cuối và cho phép hủy ngang an toàn). Đây là chuẩn bắt buộc cho **Nav2** (`NavigateToPose`) và **MoveIt 2** (điều khiển cánh tay).

## Mục tiêu

Sau bài học này, bạn sẽ gọi được một service cộng hai số để nhận phản hồi trực tiếp, đồng thời gửi mục tiêu (goal) cho action Fibonacci và phân biệt rõ phản hồi tiến độ (feedback) với kết quả cuối cùng (result). Bạn cũng sẽ chọn đúng cơ chế topic, service hoặc action cho bốn tác vụ phổ biến: truyền liên tục vận tốc bánh xe, đặt lại bộ đếm encoder, di chuyển tới một tư thế (pose) đích và xuất bản dữ liệu quét laser. Nhờ đó, khi gặp action `NavigateToPose` của Nav2 ở chương sau, bạn sẽ nhận ra nó có cùng cấu trúc với ví dụ Fibonacci nhưng được bổ sung thêm bản đồ.

## Kiến thức cần trước

Đã làm quen với ví dụ `talker` ở bài 09-02 và biết cách chạy song song các tiến trình ở nhiều cửa sổ terminal khác nhau. Bài này chưa cần robot thật.

## Vì sao bài này nằm trên lộ trình

Việc truyền liên tục `cmd_vel` phù hợp với topic vì lệnh mới nhất luôn thay thế lệnh cũ và hệ thống không cần đợi phản hồi trước chu kỳ 50 ms kế tiếp. Ngược lại, bài toán "đã tới đích chưa?" sẽ rất bất tiện nếu dùng topic vì cần theo dõi tiến độ và hỗ trợ hủy giữa chừng — đó chính là lý do action ra đời và là cách Nav2 nhận mục tiêu di chuyển ở chương 11. Trong khi đó, service dành cho các tác vụ ngắn dạng hỏi-đáp: bật/tắt một cờ logic, kích hoạt hiệu chuẩn hoặc tính một tổng nhỏ. Nếu đặt một chuyến di chuyển kéo dài năm phút vào service, cách hủy duy nhất của bạn sẽ là ngắt cưỡng bức bằng Ctrl-C. Dù dùng cơ chế nào, watchdog của Capstone vẫn là lớp bảo vệ timeout trên firmware; khi hủy một action, hệ thống vẫn cần gửi kèm lệnh `Twist` bằng 0 để bánh xe không tiếp tục quay theo lệnh cũ.

![Một trả lời service so với dòng thời gian action]({{ site.imgurl }}/generated/ch09_svc_action.png)

## Khái niệm

**Service** hoạt động theo mô hình yêu cầu – phản hồi (request – response): client gửi một message yêu cầu, server xử lý rồi trả về một message kết quả và kết thúc lời gọi. Ví dụ `example_interfaces/srv/AddTwoInts` nhận hai số `a`, `b` và trả về `sum`. Cơ chế này chỉ phù hợp cho các tác vụ ngắn mà bên gọi có thể chờ; tuyệt đối không dùng cho luồng dữ liệu liên tục, vì một lời gọi service bị chặn bên trong vòng điều khiển động cơ sẽ làm trượt chu kỳ thời gian thực của bài 08-05.

**Action** bao gồm mục tiêu (goal), luồng phản hồi tiến độ (feedback), kết quả cuối (result) và cơ chế hủy (cancel). Trong ví dụ Fibonacci, client gửi giá trị `order` và nhận liên tục dãy số đang được tính dần; nếu quá lâu, client có thể gửi yêu cầu hủy. Action điều hướng của Nav2 có cấu trúc hoàn toàn tương tự: đầu vào là pose đích, dọc đường trả về feedback (quãng đường còn lại, pose hiện tại) và cuối cùng trả về kết quả (thành công hoặc bị hủy). Các hành vi phục hồi sự cố (recovery) nằm trong cây hành vi (behavior tree) sẽ được giới thiệu sơ lược ở chương 11, nhưng bạn không cần đến nó để hiểu vai trò của action.

Bảng phân loại thực tế cho robot trong khóa học:

| Tác vụ | Cơ chế phù hợp | Lý do |
| --- | --- | --- |
| Gửi lệnh vận tốc bánh ở 10–50 Hz | Topic `cmd_vel` | Chỉ cần lệnh mới nhất, không cần phản hồi từng gói |
| Dữ liệu quét laser (Laser scan) | Topic | Luồng dữ liệu liên tục, thường dùng QoS best-effort |
| "Xóa bộ đếm encoder" | Service | Một yêu cầu, một phản hồi, hoàn thành trong vài mili giây |
| "Chạy tới pose đích này" | Action | Kéo dài nhiều giây hoặc phút, cần theo dõi tiến độ và hủy được |
| Điện áp pin | Topic | Luồng dữ liệu định kỳ, tần số thấp vẫn phù hợp |

Lưu ý rằng việc hủy một action không tự động ngắt dòng điện cấp cho động cơ. Cầu nối điều khiển vẫn phải coi trạng thái "không có lệnh `Twist` mới" là lệnh dừng — quy tắc này vốn đã được cài đặt trong timeout serial và cần được giữ nguyên khi `Twist` bắt đầu đến từ bộ điều khiển của action server thay vì bàn phím.

## Hủy tác vụ là một message hợp lệ, không phải ngắt cưỡng bức

Server Fibonacci sẽ tiếp tục tính toán cho đến khi hoàn thành mục tiêu hoặc nhận được lệnh hủy. Khi bạn gửi `order: 20` và quan sát cửa sổ server, dãy số feedback sẽ dài dần. Nhấn Ctrl-C trên cửa sổ *client* sẽ gửi yêu cầu hủy goal qua dòng lệnh, trong khi tiến trình server vẫn chạy bình thường và lệnh `ros2 action list` vẫn thấy `/fibonacci`. Nếu cách duy nhất để dừng một tác vụ là tắt hẳn tiến trình server, hệ thống đó không có cơ chế hủy mà chỉ đang bị sập (crash).

```bash
ros2 action send_goal /fibonacci action_tutorials_interfaces/action/Fibonacci "{order: 20}"
```

Ngắt lệnh trên bằng Ctrl-C, rồi kiểm tra ngay:

```bash
ros2 action list
ros2 node list
```

**Kết quả mong đợi:** `/fibonacci` và node server vẫn tồn tại. Nếu bạn gửi tiếp một goal ngắn hơn (`order: 5`), server vẫn phải tính và trả về kết quả bình thường. Đây chính là đặc tính cần có ở Nav2 sau này: một lượt điều hướng bị hủy hoặc thất bại không buộc bạn phải khởi động lại toàn bộ hệ thống. Service không có khả năng này — không tồn tại lệnh `ros2 service cancel`; client hoặc phải chờ, hoặc bị tắt ngang trong khi server có thể vẫn đang kẹt giữa chừng.

Ghi chú thêm về hệ quả đối với động cơ: hủy `NavigateToPose` chỉ làm action server ngừng gửi feedback mới, chứ không tự động đặt `Twist` cuối về 0 nếu bộ điều khiển hoặc cầu nối không chủ động làm việc đó. Watchdog 300 ms trên firmware (chương 08) đóng vai trò lưới an toàn cuối cùng. Một cầu nối thiết kế tốt sẽ chủ động xuất bản `Twist` bằng 0 cả khi nhận lệnh hủy *lẫn* khi mất luồng dữ liệu, tránh tình trạng xe vẫn tiếp tục trôi sau khi bạn bấm nút dừng trên RViz.

### Khung giải thích (nên đọc chậm): Chọn đúng mẫu giao tiếp cho 4 tình huống thực tế trên robot

| Yêu cầu trên robot | Chọn mẫu nào? | Lý do kỹ thuật |
| :--- | :---: | :--- |
| Đọc góc nghiêng từ cảm biến IMU ở 100 Hz | **Topic** | Dữ liệu liên tục tần suất cao, nhiều node (EKF, điều khiển) cùng cần nghe |
| Xóa sạch bộ đếm odometry về `(0, 0, 0)` trước khi chạy test | **Service** | Thao tác rời rạc dưới 5 ms, cần biết chắc MCU đã thực hiện xong |
| Ra lệnh robot tự hành đi 15 mét qua hành lang tới phòng lab | **Action** | Kéo dài 30 giây, cần xem khoảng cách còn lại (`feedback`) và phải hủy được ngay khi gặp sự cố |
| Nhấn nút dừng khẩn cấp (E-Stop) | **Phần cứng ngắt nguồn + Topic ưu tiên** | Không bao giờ chờ phản hồi đồng bộ khi cần cắt điện khẩn cấp! |

## Lab

Thực hành service trên hai cửa sổ terminal theo hướng dẫn [Tìm hiểu service](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Services/Understanding-ROS2-Services.html):

```bash
ros2 run demo_nodes_cpp add_two_ints_server
```

```bash
ros2 service list
ros2 service type /add_two_ints
ros2 service call /add_two_ints example_interfaces/srv/AddTwoInts "{a: 2, b: 3}"
```

**Kết quả mong đợi:**

```text
example_interfaces/srv/AddTwoInts
response:
example_interfaces.srv.AddTwoInts_Response(sum=5)
```

Nếu terminal chạy server chưa được bật, lệnh gọi service sẽ bị treo chờ phản hồi — đó cũng là lý do nếu đặt lệnh động cơ vào service, chỉ cần server gặp sự cố là cả hệ thống điều khiển sẽ bị đứng. Nhấn Ctrl-C để dừng client.

Thực hành action trên hai cửa sổ terminal theo hướng dẫn [Tìm hiểu action](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Actions/Understanding-ROS2-Actions.html):

```bash
ros2 run action_tutorials_py fibonacci_action_server
```

```bash
ros2 action list
ros2 action info /fibonacci
ros2 action send_goal /fibonacci action_tutorials_interfaces/action/Fibonacci "{order: 5}"
```

**Kết quả mong đợi:** các dòng feedback hiển thị dãy `sequence` tăng dần độ dài, sau đó trả về kết quả cuối cùng kèm `goal id`. Hãy đọc trực tiếp khối `result` in ra trên terminal. Tiếp theo, gửi `order: 20` rồi nhấn Ctrl-C ở client để hủy: kiểm tra lại từ một terminal khác sẽ thấy `/fibonacci` vẫn hiển thị trong `ros2 action list`, chứng tỏ bạn có thể hủy mục tiêu mà không cần tắt server.

**Các lỗi thường gặp**

| Hiện tượng | Nguyên nhân thường gặp |
| --- | --- |
| Lệnh gọi service bị treo mãi | Server chưa chạy, hoặc gõ sai tên service |
| `package 'action_tutorials_py' not found` | Thiếu gói mẫu; cài thêm bằng `sudo apt install ros-jazzy-action-tutorials-py` |
| Chỉ thấy kết quả cuối mà không thấy feedback | Client không bật chế độ in feedback; công cụ CLI `send_goal` mặc định hiển thị đầy đủ |
| Đưa tác vụ "đi 2 m" vào service | Không có cơ chế hủy và báo tiến độ; cần chuyển sang dùng action và vẫn duy trì timeout động cơ |

## Mua ở Việt Nam

Không cần mua thêm phần cứng. Đây là bài thực hành hoàn toàn trên laptop.

## Video tham khảo

- **Xem trước:** [ROS/ROS 2 - What are messages, services and actions?](https://www.youtube.com/watch?v=WzOopOkrowA) — Hummingbird (tiếng Anh). So sánh sự khác biệt giữa message, service và action dựa trên việc có cần chờ kết quả hay không, khớp với bảng phân loại trong bài.

## Bài tập

1. Tác vụ "xuất bản điện áp pin mười lần mỗi giây" nên dùng cơ chế nào? *Gợi ý:* topic.
2. Tác vụ "yêu cầu Nav2 di chuyển vào bếp" nên dùng cơ chế nào? *Gợi ý:* action (tên cụ thể bạn sẽ gặp ở chương sau là `NavigateToPose`).
3. Một lệnh gọi service bị treo suốt 30 giây. Bước kiểm tra đầu tiên bạn nên làm là gì? *Gợi ý:* kiểm tra tiến trình server qua `ros2 service list` và cửa sổ terminal của server, thay vì vội cài lại ROS.
4. Vì sao khi hủy action, hệ thống Capstone vẫn cần gửi lệnh `Twist` bằng 0? *Gợi ý:* firmware giữ vận tốc bánh theo lệnh cuối cho tới khi hết thời gian chờ 300 ms của watchdog; việc gửi rõ giá trị 0 (hoặc ngắt luồng kịp thời) giúp xe dừng ngay thay vì tiếp tục trôi theo mức PWM cũ.
5. Trong ví dụ minh họa Fibonacci, trường `order: 5` tương ứng với khái niệm nào trên robot thực tế? *Gợi ý:* tương ứng với pose đích cần di chuyển tới, không phải giá trị PWM trực tiếp.

## Đọc thêm

- [Tìm hiểu service](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Services/Understanding-ROS2-Services.html)
- [Tìm hiểu action](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Actions/Understanding-ROS2-Actions.html)
- [Bắt đầu với Nav2 (Jazzy)](https://docs.nav2.org/jazzy/getting_started/) — giới thiệu action điều hướng sẽ dùng ở chương sau.
- Xem trực tiếp định nghĩa `action_tutorials_interfaces/action/Fibonacci` bằng lệnh `ros2 interface show`.
