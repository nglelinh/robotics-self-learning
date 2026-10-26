---
layout: post
title: "Checklist lab chương 12"
chapter: "12"
order: 7
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter12
lesson_type: required
draft: false
---

Thời lượng: **~40 phút**. Không có checkpoint nào được phép là bằng chứng thay cho một đoạn văn.

## Mục tiêu

Bạn ký năm cửa đọc và một cửa tay SO-101: dataset card, đoạn đa mode, bảng VLA, câu lộ trình tháng tới, và lab tay hoặc giấy hoãn có ngày. Train xong trên GPU không bù một card thiếu đơn vị.

## Kiến thức cần trước

Bài 12-01 đến 12-06. Capstone vẫn là $(v, \omega)$ trừ khi card nói khác và bạn đang nói về tay.

## Vì sao bài này nằm trên lộ trình

Đây là cửa cuối của khóa. Nó giữ bạn khỏi gán một ô action của OpenVLA lên PWM của xe, và khỏi gọi một lần `lerobot-train` lỗi CUDA là bài trượt.

## Đạt và trượt

**Card.** Có `fps`, tên khóa ảnh, tên khóa action, đơn vị. Card xe dùng m/s và rad/s. Card SO-101 dùng đúng số trục bạn đếm được (sáu trên follower) và không ghi đơn vị nếu file dataset không ghi. Bịa đơn vị là trượt.

**Diffusion.** Đoạn có hai demonstration, một trung bình đâm vào vật, và một câu không train. Đoạn chỉ khen "đa mode" là trượt.

**VLA.** Hai dòng bảng, không dòng nào nói train ở nhà là có. Một dòng SO-101 nói vector 6 khớp không phải action của RT-1 hay OpenVLA.

**Lộ trình.** Bài 12-05 có một tháng bạn chọn, một link đã mở, và một việc bạn sẽ không làm (không mua lidar chỉ vì một bài báo).

**Tay.** Lab 12-06: hoặc log cổng và một lần calibrate / teleop, hoặc giấy hoãn vì chưa có tay, kèm dataset card giấy. Mua tay trong tuần này không phải điều kiện đạt.

## Lab

```text
## Ky duyet chuong 12
Card (file):
Doan diffusion (dat/truot):
Bang VLA (2 dong, dat/truot):
Thang toi:
SO-101: log / giay hoan ngay
Train tai nha: khong
```

### Lỗi thường gặp

| Bạn thấy | Cần kiểm |
| --- | --- |
| Card action là PWM nhưng lời ghi là rad/s | Hai robot. Chọn một |
| "CUDA out of memory" trong ô đạt | Lab không chấm GPU. Viết đoạn văn |
| Bảng VLA để Twist là có | Đọc lại embodiment. Viết không |

## Bài tập

1. Cửa nào trượt nếu đoạn diffusion đúng nhưng card không có `fps`?
2. Giấy hoãn SO-101 không ghi ngày. Bạn ký không?
3. Vì sao một checkpoint OpenVLA tải được vẫn không làm cửa tay đạt?

### Gợi ý đáp án

1. Cửa card. Đoạn văn không điền đơn vị của log. 2. Không. Hoãn không ngày là im lặng. 3. Checkpoint đó không chứng minh bạn đã calibrate STS3215, cũng không chứng minh action 6 số khớp.

## Đọc thêm

- [LeRobot](https://huggingface.co/docs/lerobot/index)
- [SO-101](https://huggingface.co/docs/lerobot/so101)
- [Lab tay]({% multilang_post_url contents/chapter12/12_06_so101_arm_lab %})
