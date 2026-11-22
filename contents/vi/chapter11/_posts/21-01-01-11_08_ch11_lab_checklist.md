---
layout: post
title: "Checklist lab chương 11"
chapter: "11"
order: 8
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter11
lesson_type: required
draft: false
---

Thời lượng: **~50 phút**. Sau hai bài lab Capstone B, mục kiểm tra này yêu cầu minh chứng thực tế cho các kết quả đã chạy, không lặp lại định nghĩa lý thuyết SLAM.

## Mục tiêu

Bạn cần xác nhận đủ các hạng mục: câu tóm tắt chuỗi TF từ phần khái niệm, ảnh bản đồ hoặc log `/map` từ lab SLAM, một lượt gửi goal sinh `Twist` từ lab Nav2, và sự tách bạch rõ ràng giữa phần mô phỏng với phần xe thật. Việc chưa có lidar thật không làm trượt phần mô phỏng, nhưng bỏ trống không ghi chú kế hoạch hoãn cho phần xe thật thì chưa đạt.

## Kiến thức cần trước

Hoàn thành các bài từ 11-01 đến 11-07. Đảm bảo odometry chương 08 đã đúng dấu nếu bạn triển khai trên xe thật, và chuẩn bị lidar LD06 hoặc RPLIDAR A1 khi chạy trên sàn.

## Vì sao bài này nằm trên lộ trình

Chương 12 sẽ chuyển sang các chính sách học máy (policy), nhưng policy không tự dựng `/map` thay cho tầng điều hướng. Checklist này giúp phân biệt rạch ròi giữa việc chạy thành công mô phỏng TurtleBot3 với việc xe tự chế đã sẵn sàng tự hành ngoài thực tế.

## Tiêu chí đạt và không đạt

**Khái niệm.** Một câu mô tả đúng chuỗi `map → odom → base_link` và một câu giải thích vì sao cảm biến ToF đơn điểm không thay thế được `LaserScan`.

**SLAM mô phỏng.** Ảnh chụp hoặc mô tả lưới bản đồ khi chạy `slam:=True` với mô phỏng TurtleBot3 của Nav2 Jazzy (hoặc log lỗi launch nguyên văn nếu máy không đủ tài nguyên). Ghi chung chung "không chạy vì máy yếu" mà không kèm lệnh và log là chưa đạt.

**SLAM thực tế.** Ảnh bản đồ phòng thực tế, hoặc ghi chú hoãn có ngày cụ thể và lý do (ví dụ chưa có lidar). Nếu đã chạy trên xe thật mà bản đồ bị cong nhưng không ghi nhận nguyên nhân dấu encoder thì chưa đạt.

**Nav2.** Một mục tiêu gửi trong mô phỏng tạo ra `/cmd_vel` khác 0 rồi dừng khi hủy goal hoặc gửi lệnh 0. Trên sàn thực tế: thực hiện tương tự với bước nhấc bánh ban đầu trước khi hạ xuống sàn (nếu chưa chạy sàn thì ghi chú hoãn).

**An toàn.** Ghi nhận rõ có người túc trực ở công tắc nguồn pin trong lần đầu hạ bánh chạy tự hành; nếu đã hạ bánh mà thiếu xác nhận này thì tiêu chí Nav2 thực tế chưa đạt.

## Lab

Sao chép mẫu sau vào sổ thực hành và điền đầy đủ kết quả:

```text
## Ky duyet chuong 11
TF ba canh:
SLAM sim (lenh + ket qua):
SLAM that hoac giay hoan:
Nav2 goal sim:
Nav2 that hoac giay hoan:
Cong tat pin khi ha banh: co / chua ha
```

### Lỗi thường gặp

| Hiện tượng | Hướng kiểm tra |
| --- | --- |
| Costmap trống dù Gazebo vẫn hiển thị tia laser | Kiểm tra QoS của `/scan` hoặc lệch `frame_id` |
| Bản đồ bị xoay cong khi xe chạy thẳng | Kiểm tra dấu encoder hoặc thứ tự trái/phải |
| Hoàn thành goal nhưng bánh xe thật không dừng | Còn publisher khác phát lên `/cmd_vel` hoặc watchdog firmware chưa hoạt động |

## Video tham khảo

- **Xem trước:** [Making robot navigation easy with Nav2 and ROS!](https://www.youtube.com/watch?v=jkoGkAd0GYk) — Articulated Robotics (tiếng Anh). Minh họa trực quan tuyến đường điều hướng trong mô phỏng cần đạt trước khi xác nhận checklist.

## Bài tập

1. Nếu bạn chỉ có ảnh chạy mô phỏng TurtleBot3 và một ghi chú hoãn lidar có ngày cụ thể, những tiêu chí nào được tính là đạt?
2. Vì sao ảnh chụp RViz không thể thay thế cho xác nhận "có người đứng ở công tắc pin"?
3. Giữa hai bản đồ thu được (một bản bị cong, một bản thẳng), bạn xác nhận bản nào và bước khắc phục bản bị cong nằm ở chương nào?

### Gợi ý đáp án

1. Phần mô phỏng đạt và phần thực tế đạt theo diện hoãn hợp lệ (với điều kiện ghi rõ ngày và lý do).
2. RViz chỉ là giao diện hiển thị, không thể ngắt nguồn điện động cơ khi có sự cố; công tắc pin là lớp bảo vệ phần cứng bắt buộc.
3. Xác nhận bản đồ thẳng sau khi đã sửa lỗi dấu; phần khắc phục nằm ở odometry chương 08, không phải ở tham số SLAM.

## Đọc thêm

- [Nav2 với SLAM, tài liệu Jazzy](https://docs.nav2.org/jazzy/tutorials/general_tutorials/navigation2_with_slam/navigation2_with_slam/)
- [slam_toolbox](https://github.com/SteveMacenski/slam_toolbox)
