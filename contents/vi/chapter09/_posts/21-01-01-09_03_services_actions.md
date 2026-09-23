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

## Mục tiêu

Bạn gọi service cộng hai số và đọc một phản hồi, rồi gửi goal action Fibonacci và chỉ ra feedback khác kết quả cuối chỗ nào. Bạn chọn topic, service hoặc action cho bốn việc: stream tốc độ bánh, xóa encoder, chạy tới một pose, và xuất bản laser scan. `NavigateToPose` của Nav2 nên giống demo Fibonacci có thêm bản đồ, không phải một tôn giáo mới.

## Kiến thức cần trước

Talker của bài 09-02 đã quen. Bạn để một tiến trình chạy ở một terminal và gõ ở terminal khác. Không cần robot.

## Vì sao bài này nằm trên lộ trình

Stream `cmd_vel` trên topic là công cụ đúng vì lệnh mới thay lệnh cũ và không ai phải đợi trả lời trước tick 50 ms kế. “Đã tới đích chưa?” là topic tệ nếu bạn còn cần hủy và tiến độ. Đó là action, và đó là cách Nav2 nhận một pose ở chương 11. Service là câu hỏi ngắn: đặt một bool, kích hoạt hiệu chuẩn, trả về một tổng. Người đặt chuyến đi năm phút lên service sẽ thấy Ctrl-C là cách hủy duy nhất. Watchdog Capstone vẫn là timeout firmware dù bạn chọn gì; hủy action cũng nên xuất bản Twist 0, nếu không bánh giữ lệnh cuối.

![Một trả lời service so với dòng thời gian action]({{ site.imgurl }}/generated/ch09_svc_action.png)

## Khái niệm

**Service** là một yêu cầu và một trả lời. Client gửi một message, server gửi một message, lời gọi trở về. `example_interfaces/srv/AddTwoInts` nhận `a` và `b` rồi trả `sum`. Dùng khi việc ngắn và bên gọi chờ được. Đừng dùng cho stream. Server service mà kẹt trong vòng động cơ sẽ trượt hạn của bài 08-05.

**Action** là goal, dòng feedback, và một kết quả, cộng thêm hủy. Tutorial Fibonacci gửi `order` và phản hồi dãy khi nó dài ra. Bạn hủy được goal đang quá lâu. Action điều hướng của Nav2 cùng hình dạng: pose đích đi vào, feedback (quãng còn lại, pose hiện tại) dọc đường, kết quả (thành công hoặc hủy bỏ) ở cuối. Recovery nằm trong behavior tree, chương 11 chỉ nhìn lướt. Bạn không cần cây đó để thấy vì sao action tồn tại.

Cách chia thực tế cho robot này:

| Việc | Dùng | Vì sao |
| --- | --- | --- |
| Lệnh bánh ở 10–50 Hz | Topic `cmd_vel` | Message mới nhất thắng. Không cần trả lời |
| Laser scan | Topic | Stream. Thường QoS best-effort |
| “Xóa bộ đếm encoder” | Service | Một câu, một lời, vài mili giây |
| “Chạy tới pose này” | Action | Vài phút, hủy được, có feedback |
| Điện áp pin | Topic | Stream, chậm cũng được |

Hủy action không tự cắt cổng MOSFET. Cầu nối phải coi “không có Twist mới” là dừng. Luật đó đã có trong timeout serial. Giữ nó khi Twist bắt đầu đến từ controller của action server thay vì bàn phím.

## Hủy là một message, không phải một ước muốn

Server Fibonacci tiếp tục tính đến khi goal xong hoặc một lệnh hủy tới. Nhìn terminal server trong lúc bạn gửi `order: 20`. Dãy feedback dài ra. Ctrl-C trên *client* hủy goal đó trong CLI; tiến trình server phải còn sống và `ros2 action list` vẫn phải thấy `/fibonacci`. Nếu cách duy nhất bạn biết để dừng một goal là giết server, bạn không có hủy, bạn có một cú crash.

```bash
ros2 action send_goal /fibonacci action_tutorials_interfaces/action/Fibonacci "{order: 20}"
```

Ngắt nó. Rồi ngay:

```bash
ros2 action list
ros2 node list
```

**Mong đợi:** `/fibonacci` còn, node server còn. Một goal ngắn thứ hai, `order: 5`, vẫn phải trả kết quả. Đó là hành vi bạn muốn ở Nav2 sau này: một lần điều hướng thất bại hoặc bị hủy không đòi bạn khởi động lại cả stack. Đó cũng là hành vi bạn *không* có từ service. Không có `ros2 service cancel`. Client chờ, hoặc bạn giết nó, và server có thể vẫn đang ở trong lời gọi.

Viết hệ quả động cơ vào cùng ghi chú. Hủy `NavigateToPose` làm action server ngừng gửi feedback mới. Nó không, tự thân, ép `Twist` cuối về 0 trừ khi controller hoặc cầu nối của bạn làm việc đó. Timeout firmware 300 ms từ chương 08 là lưới sau cùng. Cầu nối hiểu action thì xuất bản số 0 khi hủy *và* khi im lặng. Chỉ viết một trong hai là cách robot vẫn bò sau khi bạn bấm dừng trong RViz.

## Lab

Service, hai terminal. Tutorial: [Tìm hiểu service](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Services/Understanding-ROS2-Services.html).

```bash
ros2 run demo_nodes_cpp add_two_ints_server
```

```bash
ros2 service list
ros2 service type /add_two_ints
ros2 service call /add_two_ints example_interfaces/srv/AddTwoInts "{a: 2, b: 3}"
```

**Mong đợi:**

```text
example_interfaces/srv/AddTwoInts
response:
example_interfaces.srv.AddTwoInts_Response(sum=5)
```

Nếu terminal server không chạy, lời gọi ngồi chờ. Sự chờ đó là lý do một service động cơ bị mất cảm giác như teleop treo. Ctrl-C client.

Action, hai terminal. Tutorial: [Tìm hiểu action](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Actions/Understanding-ROS2-Actions.html).

```bash
ros2 run action_tutorials_py fibonacci_action_server
```

```bash
ros2 action list
ros2 action info /fibonacci
ros2 action send_goal /fibonacci action_tutorials_interfaces/action/Fibonacci "{order: 5}"
```

**Mong đợi:** các dòng feedback với `sequence` dài dần, rồi một kết quả. Đọc khối result thay vì học thuộc dãy trên blog. `send_goal` cũng in goal id. Gửi order 20 rồi hủy mới là ý: terminal khác vẫn thấy `/fibonacci` trong `ros2 action list`, và bạn ngắt client được. Không cần giết server để dừng một goal.

**Khi hỏng thì thường vì**

| Bạn thấy | Nguyên nhân hay gặp |
| --- | --- |
| Lời gọi service ngồi mãi | Server không chạy, hoặc sai tên |
| `package 'action_tutorials_py' not found` | Thiếu gói. `sudo apt install ros-jazzy-action-tutorials-py` |
| Không có feedback, chỉ có kết quả | Client giấu feedback. CLI `send_goal` thì hiện |
| Bạn gắn “đi 2 m” vào service | Hủy và tiến độ không có chỗ ở. Làm thành action, và vẫn timeout động cơ |

## Mua ở Việt Nam

Không có gì. Đây là lab laptop.

## Bài tập

1. Xếp loại “xuất bản điện áp pin mười lần một giây.” Gợi ý: topic.
2. Xếp loại “Nav2, đi tới bếp.” Gợi ý: action. Tên bạn sẽ tra sau: `NavigateToPose`.
3. Lời gọi service treo 30 giây. Tiến trình đầu tiên bạn kiểm là gì? Gợi ý: server, bằng `ros2 service list` và terminal server, trước khi cài lại ROS.
4. Vì sao hủy action vẫn phải tạo Twist 0 trên Capstone? Gợi ý: firmware giữ lệnh bánh cuối đến khi watchdog 300 ms. Hủy phải được nối bằng im lặng hoặc số 0 tường minh, nếu không robot trôi trên PWM cũ đến khi watchdog cứu.
5. Fibonacci `order: 5` là vật thế. Trường “order” tương tự cái gì trên xe? Gợi ý: pose đích, không phải PWM.

## Đọc thêm

- [Tìm hiểu service](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Services/Understanding-ROS2-Services.html).
- [Tìm hiểu action](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Actions/Understanding-ROS2-Actions.html).
- [Bắt đầu với Nav2 (Jazzy)](https://docs.nav2.org/jazzy/getting_started/) cho action điều hướng bạn chưa chạy.
- Định nghĩa `action_tutorials_interfaces/action/Fibonacci` qua `ros2 interface show`.
