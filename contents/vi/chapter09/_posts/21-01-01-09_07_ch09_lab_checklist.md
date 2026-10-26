---
layout: post
title: "Checklist lab chương 09"
chapter: "09"
order: 7
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter09
lesson_type: required
draft: false
---

Thời lượng: **~70 phút**. Cửa này hỏi bằng chứng rằng Jazzy sống trên Ubuntu 24.04, graph có topic, và cây TF có một cạnh tĩnh bạn giải thích được.

## Mục tiêu

Bạn ký sáu cửa: Ubuntu đúng bản, workspace đã source, một topic echo được, một service hoặc action đã gọi, `ROS_DOMAIN_ID` nếu có SBC, và `tf2_echo` của cạnh `base_link` tới frame cảm biến. Thiếu log là trượt.

## Kiến thức cần trước

Bài 09-00 đến 09-06. Laptop hoặc SBC đã có `printenv ROS_DISTRO`. Sổ chương 08 đã ký, hoặc bạn ghi rõ chương 08 còn cửa nào trượt. TF không sửa khẩu độ sai.

## Vì sao bài này nằm trên lộ trình

Gazebo Harmonic ở chương 10 spawn vào một graph đã có. `use_sim_time` dán lên một cài hỏng chỉ nhân đôi số topic lạ. Ký graph khi world còn trống.

## Đạt và trượt

**Bản cài.** `printenv ROS_DISTRO` là `jazzy` và `lsb_release -sc` là `noble` trên máy sẽ chạy apt. Jetson còn `jammy` thì cửa này trượt cho đến khi bạn không còn cài Jazzy trên đó. Ảnh chụp terminal là bằng chứng.

**Workspace.** Một gói trong `~/ros2_ws` build bằng `colcon`, terminal mới source underlay rồi overlay. `ros2 pkg list` không thấy gói của bạn sau khi mở terminal mới là trượt, trừ khi `.bashrc` đã source và bạn dán dòng đó.

**Topic.** Talker hoặc node của bạn, `ros2 topic echo` một lần, có kiểu message. Danh sách rỗng cộng một talker bạn chưa chạy là chưa làm, không phải "DDS hỏng".

**Service hoặc action.** Một lời gọi thành công, hoặc một lỗi bạn đọc được và sửa. Không có lệnh trong sổ là trượt.

**SBC.** Nếu bạn có Pi hoặc Jetson: `/dev/esp32` hoặc câu hoãn có ngày, unit systemd đã `status`, hai máy cùng domain. Không có SBC: câu "chỉ laptop" là đạt cửa này.

**TF.** `ros2 run tf2_ros tf2_echo base_link <frame>` in một tịnh tiến theo mét. Hai publisher trên cùng cạnh là trượt. Quaternion yaw $90^\circ$ phải gần $(0,\ 0,\ 0{,}707,\ 0{,}707)$ nếu bạn cố ý quay $90^\circ$.

## Lab

Dán vào sổ khối sau, điền hoặc xóa dòng không có bằng chứng.

```text
## Ky duyet chuong 09
Ngay:
ROS_DISTRO=
Ubuntu codename=
pkg da build=
topic echo (lenh + 1 dong):
service/action:
SBC: co / khong. DOMAIN=
tf2_echo base_link -> :
```

### Lỗi thường gặp

| Bạn thấy | Cần kiểm |
| --- | --- |
| `humble` và `jazzy` cùng shell | Xóa một `source` trong `.bashrc` |
| Echo không có data | Publisher chưa chạy, khác domain, hoặc QoS không khớp |
| `tf2_echo` chờ mãi | Sai tên frame. `ros2 run tf2_tools view_frames` |
| Pi chạy Ubuntu 26.04 | Ngoài apt Jazzy. Ghi lại 24.04 hoặc dừng cửa bản cài |

## Video tham khảo

- **Xem trước:** [The ROS Transform System (TF) | Getting Ready to Build Robots with ROS #6](https://www.youtube.com/watch?v=QyvHhY4Y_Y8) — Articulated Robotics, tiếng Anh. Checklist chương hỏi một cây frame nhìn được. Video TF là hình cần có trước khi tick.

## Bài tập

1. Cửa nào trượt khi topic thấy nhau nhưng `lsb_release` là `jammy`?
2. `tf2_echo` ra $x = 10$. Đơn vị nào đang sai nếu lidar chỉ cách tâm 10 cm?
3. Vì sao "chỉ laptop" vẫn đạt cửa SBC?

### Gợi ý đáp án

1. Cửa bản cài. Topic không chứng minh distro. 2. Mét. $10$ m là khai $10$ thay vì $0{,}10$. 3. SBC là máy trên xe, không phải điều kiện để học graph. Câu hoãn thành thật được ký. Im lặng thì không.

## Đọc thêm

- [Cài Jazzy](https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html)
- [Về TF2](https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-TF2.html)
- [Bài Linux trên SBC]({% multilang_post_url contents/chapter09/09_00_linux_on_sbc %})
