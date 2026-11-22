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
