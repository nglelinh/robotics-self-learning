---
layout: post
title: "Checklist lab chương 10"
chapter: "10"
order: 6
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter10
lesson_type: required
draft: false
---

Thời lượng: **~60 phút**. Sau khi bài 10-05 đã đối chiếu giữa mô phỏng và thực tế, bài kiểm tra cuối chương này tổng hợp toàn bộ kết quả của chương 10: Gazebo Harmonic có `/clock`, spawn thành công URDF, cầu nối serial hoặc micro-ROS, và ba dòng kiểm định sim-to-real.

Hoàn thành Chương 10 nghĩa là bạn đã dựng xong "cặp song sinh số" (Digital Twin) cho robot của mình: một phiên bản chạy trên Gazebo Harmonic và một phiên bản chạy trên phần cứng thật, cùng chia sẻ chung một giao diện ROS 2. Bảng nghiệm thu này giúp xác nhận cả hai phiên bản hoạt động đồng nhất trước khi bước vào bài toán tự hành SLAM và Nav2 ở Chương 11.

## Bản đồ kiến thức nền: Ba tiêu chuẩn nghiệm thu Mô phỏng & Cầu nối (Chương 10)

1. **Chạy song song sạch trên Gazebo Harmonic (`sim_bringup`)**:
   Xe sinh ra đúng tư thế trên mặt đất (không lún, không nổ), RTF ổn định ($$\ge 0{,}7$$), `/clock` hoạt động chuẩn và toàn bộ cảm biến giả lập phát đúng hệ tọa độ TF2.
2. **Cầu nối Phần cứng Tin cậy (`real_bringup`)**:
   Lệnh `/cmd_vel` điều khiển mượt trên xe thật, Watchdog ngắt động cơ đúng hạn khi rút cáp/tắt node, và sai số odometry vòng hở nằm trong ngưỡng đã hiệu chuẩn.
3. **Ghi nhận Hồ sơ Sim-to-Real**:
   Lưu trữ rõ các thông số sai lệch đo được giữa mô phỏng và xe thật (deadzone, ma sát, độ trễ) để làm đầu vào tinh chỉnh cho bộ lập kế hoạch Nav2 ở Chương 11.

## Mục tiêu

Bạn cần hoàn thành và xác nhận đủ năm tiêu chí kèm log hoặc ảnh minh chứng: world Harmonic hoạt động, mô hình robot spawn thành công, lệnh `Twist` làm bánh xe mô phỏng lăn tiến, cầu nối tới firmware hoạt động (hoặc có ghi chú hoãn micro-ROS kèm ngày cụ thể) và bảng kiểm sim-to-real đã điền đủ. Nếu thiếu `/clock` thì dù đã mở được cửa sổ Gazebo vẫn chưa đạt.

## Kiến thức cần trước

Hoàn thành các bài từ 10-01 đến 10-05 với `printenv ROS_DISTRO` trả về `jazzy`. Lưu ý bản Classic `gazebo` không thể thay thế cho `gz sim`.

## Vì sao bài này nằm trên lộ trình

Capstone B ở chương 11 sẽ sử dụng chính môi trường mô phỏng và topic `/cmd_vel` của chương này. Nếu chương 10 chỉ dừng ở một cửa sổ world trống chưa kiểm chứng, các lỗi phát sinh về sau rất dễ bị đổ nhầm cho SLAM.

## Tiêu chí đạt và không đạt

**Môi trường mô phỏng (World).** Câu lệnh launch sử dụng `empty.sdf` (hoặc tên world khác được ghi rõ), có cờ `-r` (hoặc giải thích rõ lý do giữ trạng thái tạm dừng), và `gz topic -l` liệt kê được `/clock`. Chỉ chụp ảnh cửa sổ GUI mà không ghi tên world là chưa đủ.

**Mô hình (Model).** Spawn thành công từ tệp URDF hoặc `xacro` của bạn, cây TF có `base_link`. Nếu mô hình bị rơi xuyên mặt sàn thì chưa đạt cho đến khi ghi rõ đã sửa yếu tố nào (khối lượng, collision hoặc plugin) và spawn lại thành công.

**Lệnh điều khiển.** Giá trị `linear.x` dương phải làm mô hình tiến dọc theo trục $+x$ của nó. Ghi rõ giá trị đã xuất bản (ví dụ $0{,}2$ m/s) và hướng di chuyển quan sát được.

**Cầu nối phần cứng.** Nếu có xe thật: cầu nối serial hoặc micro-ROS agent chuyển `Twist` thành chuyển động bánh xe (nhấc trên không) rồi tự về 0 khi ngừng gửi lệnh. Nếu chưa có xe: ghi chú hoãn có ngày cụ thể, nhưng tiêu chí gửi lệnh trong mô phỏng vẫn bắt buộc đạt.

**Đối chiếu sim-to-real.** Điền đủ ba dòng đạt/không đạt theo bài 10-05, kèm ít nhất một số đo thực tế hoặc xác nhận loại bỏ `use_sim_time` trên tệp launch robot thật.

### Khung giải thích (nên đọc chậm): Bài test "Đổi công tắc không đổi mã" (Sim/Real Parity Check)

Để chứng minh kiến trúc Chương 10 đã đạt chuẩn, hãy thực hiện đúng bài test 3 bước với cùng một script chạy hình vuông (`square_test.py` chỉ gửi `/cmd_vel` và đọc `/odom`):
1. Chạy `sim_bringup` → chạy `square_test.py` → xác nhận xe vẽ hình vuông trong Gazebo và quay về gần điểm xuất phát.
2. Tắt mô phỏng, bật `real_bringup` trên xe thật → chạy **chính xác cùng tệp `square_test.py` không sửa một ký tự nào**!
3. Đo khoảng cách lệch giữa điểm đầu và điểm cuối trên sàn thật (ví dụ lệch `12 cm` và lệch góc `8°`) rồi ghi vào sổ lab làm mốc chuẩn trước khi bật SLAM ở Chương 11.

## Lab

Sao chép mẫu sau vào sổ thực hành và điền đầy đủ thông tin:

```text
## Ky duyet chuong 10
World + /clock:
Model + base_link:
Twist da gui:
Cau serial/micro-ROS hoac giay hoan:
use_sim_time tren robot that: khong
```

### Lỗi thường gặp

| Hiện tượng | Hướng kiểm tra |
| --- | --- |
| World đứng yên, `/clock` bằng 0 | Thiếu cờ `-r` hoặc chưa bấm nút play |
| Máy có hai phiên bản Gazebo | Trùng lặp giữa Classic và Harmonic; tắt hẳn bản Classic |
| Bánh xe mô phỏng quay ngược | Sai dấu khớp hoặc dấu trong plugin; sửa nhất quán tại một chỗ |
| Robot thật bật `use_sim_time:=true` | Gỡ bỏ ngay; robot thật dùng đồng hồ thực |

## Video tham khảo

- **Xem trước:** [Correctly Install Gazebo Harmonic Inside of ROS2 Jazzy Installation -Fix Gazebo Installation Issues](https://www.youtube.com/watch?v=dY8JxldcuqA) — Aleksandar Haber PhD (tiếng Anh). Danh sách kiểm tra mô phỏng bắt đầu từ việc đảm bảo `gz sim` khởi chạy đúng trong môi trường Jazzy.

## Bài tập

1. Tiêu chí nào vẫn chưa đạt nếu GUI hiển thị được mô hình nhưng `gz topic -l` không có `/clock`?
2. Vì sao việc ghi chú hoãn micro-ROS vẫn không miễn trừ tiêu chí kiểm thử `Twist` trong mô phỏng?
3. Nếu ngừng gửi `cmd_vel` nhưng bánh xe thật vẫn tiếp tục quay, tiêu chí nào đang không đạt?

### Gợi ý đáp án

1. Tiêu chí World không đạt, vì ảnh GUI không chứng minh server mô phỏng đang chạy đồng hồ thời gian.
2. Mô phỏng là môi trường kiểm chứng lệnh điều khiển trước khi nối xuống firmware; việc hoãn chỉ áp dụng cho cầu nối phần cứng.
3. Tiêu chí Cầu nối (và mục an toàn bài 10-05) không đạt do cơ chế watchdog chưa đưa vận tốc về 0.

## Đọc thêm

- [Gazebo Harmonic, bắt đầu](https://gazebosim.org/docs/harmonic/getstarted/)
- [ros_gz](https://github.com/gazebosim/ros_gz)
- [Bài sim-to-real]({% multilang_post_url contents/chapter10/10_05_sim_to_real %})
