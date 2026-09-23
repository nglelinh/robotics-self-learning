---
layout: post
title: "Nhận diện driver: L298N, TB6612, DRV8833"
chapter: "05"
order: 2
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter05
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

![H-bridge]({{ site.imgurl }}/generated/hbridge_concept.png)

![L298N module]({{ site.imgurl }}/wikimedia/Dosmotorsl298n.jpg)

## Ý tưởng cốt lõi

Lab ghi nhãn chân driver.


## Ghi chú lab

**An toàn:** nhấc bánh; nguồn sau cùng; pin lithium có người trông.
**Quy trình:** làm theo phần ý tưởng cốt lõi; chụp ảnh đấu dây.
**Ghi:** số đo / serial / số răng vào `lab-notes.md`.
**Sai thường gặp:** thiếu GND chung; USB nuôi motor; đảo dây motor.


## Vệ sinh actuator

Nhấc bánh; giới hạn dòng; nhớ dòng stall; ghi nhãn trái/phải trong firmware.


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
## So nhanh driver

L298N: tản nhiệt to. TB6612/DRV8833: nhỏ, hiệu quả hơn. Luôn nhận VMOT/GND/PWM từ tài liệu module.

## Bài tập

1. Tóm tắt 5 ý.
2. Làm lab (hoặc dry-run).
3. Vẽ lại một sơ đồ.
4. Hai lỗi cần tránh.
5. Ghi `lab-notes.md`.

## Đọc thêm

- Xem COURSE_OUTLINE.md
