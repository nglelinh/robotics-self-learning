---
layout: post
title: "Pinout, mức logic và nguồn board"
chapter: "02"
order: 5
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter02
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

![Headers and rails]({{ site.imgurl }}/generated/pcb_mcu_anatomy.png)

## Ý tưởng cốt lõi

GPIO 3.3 V; đổi mức; chung GND.



## Thứ tự bring-up

USB → blink → serial → GPIO → PWM không tải → rồi driver/pin.

<!--exp-->
## Gợi ý luyện

Giải thích “Pinout, mức logic và nguồn board” trong 3 phút và liệt kê phần cứng cần có trên bàn để minh họa.

## Bài tập

1. Tóm tắt 5 ý.
2. Làm lab (hoặc dry-run).
3. Vẽ lại một sơ đồ.
4. Hai lỗi cần tránh.
5. Ghi `lab-notes.md`.

## Đọc thêm

- [logic](https://learn.sparkfun.com/tutorials/logic-levels)
