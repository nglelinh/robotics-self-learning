---
layout: post
title: "Bản đồ MCU cho robot hobby"
chapter: "02"
order: 1
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

![MCU PCB anatomy]({{ site.imgurl }}/generated/pcb_mcu_anatomy.png)

![ESP32]({{ site.imgurl }}/wikimedia/ESP32_on_Lolin32_Lite_clone_board_cropped.jpg)

![Pico]({{ site.imgurl }}/wikimedia/Raspberry_Pi_Pico.jpg)

## Ý tưởng cốt lõi

ESP32 / Pico / Uno-class — chọn một MCU cho Capstone.



## Thứ tự bring-up

USB → blink → serial → GPIO → PWM không tải → rồi driver/pin.

<!--exp-->
## Gợi ý luyện

Giải thích “Bản đồ MCU cho robot hobby” trong 3 phút và liệt kê phần cứng cần có trên bàn để minh họa.

## Bài tập

1. Tóm tắt 5 ý.
2. Làm lab (hoặc dry-run).
3. Vẽ lại một sơ đồ.
4. Hai lỗi cần tránh.
5. Ghi `lab-notes.md`.

## Đọc thêm

- [esp32](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/)
- [pico](https://www.raspberrypi.com/documentation/microcontrollers/raspberry-pi-pico.html)
- [arduino](https://docs.arduino.cc/)
