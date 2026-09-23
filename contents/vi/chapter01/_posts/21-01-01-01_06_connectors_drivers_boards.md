---
layout: post
title: "Connector, driver motor và nhận diện board MCU"
chapter: "01"
order: 6
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter01
lesson_type: required
draft: false
---

Thời lượng: **~60 phút**.

## Mục tiêu học

1. Giải thích ý bài bằng lời bạn.
2. Làm lab/nhận diện nếu có.
3. Liên hệ Capstone A hoặc ROS.
4. Ghi hai chế độ hỏng.
5. Lưu link đọc thêm.

## Kế hoạch 60 phút

| Phút | Việc |
|-----:|------|
| 0–5 | Mục tiêu + hình |
| 5–25 | Đọc / toán |
| 25–45 | Lab hoặc nhận diện |
| 45–55 | Bài tập |
| 55–60 | Ghi chú + link |

## Hình minh họa

![H-bridge concept]({{ site.imgurl }}/generated/hbridge_concept.png)

![L298N-style driver]({{ site.imgurl }}/wikimedia/Dosmotorsl298n.jpg)

![MCU board anatomy]({{ site.imgurl }}/generated/pcb_mcu_anatomy.png)

![ESP32-class board]({{ site.imgurl }}/wikimedia/ESP32_on_Lolin32_Lite_clone_board_cropped.jpg)

![Raspberry Pi Pico]({{ site.imgurl }}/wikimedia/Raspberry_Pi_Pico.jpg)

## Ý tưởng cốt lõi

Không lẫn connector. Driver L298N vs TB6612/DRV8833. Board ESP32 vs Pico.


## Ghi chú lab

**An toàn:** nhấc bánh; nguồn sau cùng; pin lithium có người trông.
**Quy trình:** làm theo phần ý tưởng cốt lõi; chụp ảnh đấu dây.
**Ghi:** số đo / serial / số răng vào `lab-notes.md`.
**Sai thường gặp:** thiếu GND chung; USB nuôi motor; đảo dây motor.


## Quy trình nhận diện

1. Nhìn (vỏ, chữ, sọc cực). 2. Đo an toàn. 3. Datasheet. 4. Chụp ảnh module.

## An toàn khi đo

Không đo ohm khi mạch đang cấp nguồn. Với nguồn lạ hãy bắt đầu thang điện áp cao.


## BOM lab (điển hình)

| Mục | Ghi chú |
|-----|---------|
| Đồng hồ vạn năng | Thông mạch + V DC + Ω |
| Breadboard / dây | Theo bước lab |
| Linh kiện của bài | Xem phần ý tưởng cốt lõi |
| Sổ / ảnh | Chụp dây + số đo |

## Quan sát kỳ vọng

Có ít nhất một **số đo** hoặc kiểm tra chuyển động đạt/không đạt trong `lab-notes.md`.

<!--exp-->
## Gợi ý luyện

Giải thích “Connector, driver motor và nhận diện board MCU” trong 3 phút và liệt kê phần cứng cần có trên bàn để minh họa.

## Bài tập

1. Tóm tắt 5 ý.
2. Làm lab (hoặc dry-run).
3. Vẽ lại một sơ đồ.
4. Hai lỗi cần tránh.
5. Ghi `lab-notes.md`.

## Đọc thêm

- Xem COURSE_OUTLINE.md
