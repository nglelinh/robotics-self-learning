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

Thời lượng: **~60 phút**. Bài 10-05 đã đối chiếu sim với sàn. Cửa này gom cả chương: Harmonic có `/clock`, URDF spawn, micro-ROS hoặc cầu serial, và ba dòng đạt/trượt của sim-to-real.

## Mục tiêu

Bạn ký năm cửa có log hoặc ảnh: world Harmonic chạy, model xuất hiện, một lệnh `Twist` làm bánh mô phỏng tiến, cầu tới firmware hoặc một giấy hoãn micro-ROS có ngày, và checklist sim-to-real đã điền. Thiếu `/clock` mà vẫn kể là "đã mở Gazebo" thì trượt.

## Kiến thức cần trước

Bài 10-01 đến 10-05. `printenv ROS_DISTRO` là `jazzy`. Classic `gazebo` không thay `gz sim`.

## Vì sao bài này nằm trên lộ trình

Capstone B chương 11 dùng cùng một world và cùng một `cmd_vel`. Nếu chương 10 chỉ có ảnh cửa sổ trống, SLAM sẽ bị đổ lỗi oan.

## Đạt và trượt

**World.** Lệnh launch có `empty.sdf` hoặc world khác bạn ghi tên, cờ `-r` hoặc bạn nói rõ vì sao tạm dừng. `gz topic -l` có `/clock`. Ảnh GUI một mình là chưa đủ nếu không có tên world.

**Model.** Spawn từ URDF hoặc xacro của bạn, `tf` có `base_link`. Model rơi xuyên đất là trượt cho đến khi có một dòng sửa (khối lượng, collision, hoặc plugin) và một lần spawn lại.

**Lệnh.** `linear.x` dương làm model đi theo $+x$ của nó. Ghi số bạn đã publish, ví dụ $0{,}2$ m/s, và hướng nhìn thấy.

**Cầu.** Trên phần cứng: một dòng serial hoặc agent micro-ROS đổi `Twist` thành bánh trên không, rồi về 0 khi publisher dừng. Chưa có xe: giấy hoãn, nhưng cửa lệnh trong sim vẫn phải đạt.

**Sim-to-real.** Ba dòng đạt hoặc không đạt từ bài 10-05, kèm một số đo hoặc một câu từ chối `use_sim_time` trên robot thật.

## Lab

```text
## Ky duyet chuong 10
World + /clock:
Model + base_link:
Twist da gui:
Cau serial/micro-ROS hoac giay hoan:
use_sim_time tren robot that: khong
```

### Lỗi thường gặp

| Bạn thấy | Cần kiểm |
| --- | --- |
| World đứng im, `/clock` là 0 | Thiếu `-r` hoặc nút play |
| Có hai Gazebo | Một Classic, một Harmonic. Tắt Classic |
| Bánh sim quay ngược | Dấu joint hoặc dấu plugin, sửa một chỗ |
| Robot thật cũng `use_sim_time:=true` | Bỏ. Đồng hồ tường là đồng hồ của sàn |

## Video tham khảo

- **Xem trước:** [Correctly Install Gazebo Harmonic Inside of ROS2 Jazzy Installation -Fix Gazebo Installation Issues](https://www.youtube.com/watch?v=dY8JxldcuqA) — Aleksandar Haber PhD, tiếng Anh. Checklist mô phỏng bắt đầu bằng gz sim mở được trong môi trường Jazzy.

## Bài tập

1. Cửa nào vẫn trượt nếu GUI hiện model nhưng `gz topic -l` không có `/clock`?
2. Vì sao giấy hoãn micro-ROS không được miễn cửa Twist trong sim?
3. Publisher `cmd_vel` dừng mà bánh thật còn quay. Cửa nào trượt?

### Gợi ý đáp án

1. Cửa world. GUI không chứng minh server đang tích thời gian. 2. Sim là nơi lệnh có nghĩa trước khi có firmware. Hoãn chỉ áp vào cầu phần cứng. 3. Cửa cầu, và bài 10-05. Watchdog chưa về 0.

## Đọc thêm

- [Gazebo Harmonic, bắt đầu](https://gazebosim.org/docs/harmonic/getstarted/)
- [ros_gz](https://github.com/gazebosim/ros_gz)
- [Bài sim-to-real]({% multilang_post_url contents/chapter10/10_05_sim_to_real %})
