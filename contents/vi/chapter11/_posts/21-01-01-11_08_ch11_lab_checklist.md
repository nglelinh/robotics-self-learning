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

Thời lượng: **~50 phút**. Capstone B đã có hai lab. Cửa này hỏi bằng chứng, không hỏi lại định nghĩa SLAM.

## Mục tiêu

Bạn ký: tour khái niệm đã có câu TF, lab SLAM có ảnh bản đồ hoặc log `/map`, lab Nav2 có một goal và một `Twist`, và bạn tách được phần sim khỏi phần robot thật. Thiếu lidar thật không làm trượt phần sim. Im lặng về phần thật thì trượt, vì thiếu câu hoãn.

## Kiến thức cần trước

Bài 11-01 đến 11-07. Odometry chương 08 đã có dấu đúng nếu bạn đã ký chương đó. Lidar là LD06 hoặc RPLIDAR A1 khi bạn làm phần sàn.

## Vì sao bài này nằm trên lộ trình

Chương 12 sẽ nói policy. Policy không dựng `/map` hộ bạn. Cửa này chặn việc gọi một video TurtleBot là "robot nhà đã tự hành".

## Đạt và trượt

**Khái niệm.** Một câu có `map` → `odom` → `base_link` và một câu vì sao một tia ToF không phải `LaserScan`.

**SLAM sim.** Ảnh hoặc mô tả lưới khi `slam:=True` trên launch TurtleBot3 của Nav2 Jazzy, hoặc log nói launch fail kèm dòng lỗi gốc. "Không chạy vì máy yếu" không kèm lệnh là trượt.

**SLAM thật.** Ảnh bản đồ phòng, hoặc câu hoãn có ngày và lý do (chưa có lidar). Bản đồ cong như quả chuối mà không nhắc dấu encoder là trượt nếu bạn đã có xe.

**Nav2.** Một goal trong sim tạo `cmd_vel` khác 0, rồi robot dừng khi goal hủy hoặc khi bạn gửi 0. Trên sàn: cùng chuyện với bánh nhấc ở lần đầu, rồi mới hạ bánh. Chưa ra sàn: câu hoãn.

**An toàn.** Lần đầu trên sàn có người đứng ở công tắc pin. Thiếu câu đó mà bạn đã hạ bánh là trượt cả cửa Nav2 thật.

## Lab

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

| Bạn thấy | Cần kiểm |
| --- | --- |
| Costmap trống, Gazebo vẫn có tia | QoS scan, hoặc sai `frame_id` |
| Bản đồ quay khi xe đi thẳng | Dấu encoder hoặc trái/phải |
| Goal xong mà bánh thật không dừng | `cmd_vel` còn publisher khác, hoặc watchdog firmware |

## Bài tập

1. Cửa nào đạt nếu bạn chỉ có ảnh TurtleBot3 và một câu hoãn lidar ghi ngày?
2. Vì sao ảnh RViz không thay được câu "công tắc pin"?
3. Hai bản đồ, một cong một thẳng. Bạn ký bản nào, và việc sửa nằm ở chương nào?

### Gợi ý đáp án

1. Sim đạt, thật đạt theo đường hoãn, với điều kiện câu hoãn có ngày. 2. Ảnh không ngắt nguồn. Công tắc là phần cứng. 3. Ký bản thẳng sau khi đã sửa dấu. Sửa ở odometry chương 08, không phải ở tham số SLAM.

## Đọc thêm

- [Nav2 với SLAM, tài liệu Jazzy](https://docs.nav2.org/jazzy/tutorials/general_tutorials/navigation2_with_slam/navigation2_with_slam/)
- [slam_toolbox](https://github.com/SteveMacenski/slam_toolbox)
