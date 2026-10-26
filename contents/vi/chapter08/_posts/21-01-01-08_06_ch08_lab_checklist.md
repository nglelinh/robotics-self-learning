---
layout: post
title: "Checklist lab chương 08"
chapter: "08"
order: 6
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter08
lesson_type: required
draft: false
---

Thời lượng: **~60 phút**. Đây là cửa ký, không phải giao thức mới. Chương 09 được mở khi năm dòng dưới có bằng chứng, hoặc khi một chỗ hỏng được gọi tên và chưa bị bỏ qua.

## Mục tiêu

Bạn chấm sổ chương 08 theo năm cửa: toán TF chạy được, khung serial có timeout, PID có CSV, động học có khẩu độ đo được, và vòng lặp có chu kỳ. Mỗi cửa đạt hoặc trượt. Ô trống là trượt.

## Kiến thức cần trước

Bài 08-00 đến 08-05 là việc đang ký. Bạn cần `lab-notes.md`, file `math_tf_lab.py`, CSV PID nếu đã có encoder, và số $L$ đo bằng thước. Chưa có encoder thì cửa PID được hoãn bằng một câu ngày, không được thay bằng cảm giác "bánh quay đều".

## Vì sao bài này nằm trên lộ trình

Chương 09 sẽ gọi $v$ và $\omega$ là `linear.x` và `angular.z`. Nó giả định dấu bánh và mét đã đúng từ chương này. Một quaternion yaw $90^\circ$ ghi thành $(0, 0, 1, 0)$ sẽ làm frame laser quay $180^\circ$ so với ý bạn. Ký trước khi mở workspace Jazzy cho đỡ lẫn lỗi toán với lỗi DDS.

## Đạt và trượt

**Toán.** `math_tf_lab.py` chạy, dòng in có quaternion gần $(0,\ 0,\ 0{,}7071,\ 0{,}7071)$ và điểm $(0{,}30,\ 0)$ khi lidar ở $x = 0{,}10$ và điểm quét ở $0{,}20$. Thiếu assertion hoặc thiếu trường hợp yaw $\pi$ là trượt.

**Serial.** Nhật ký có một khung lệnh mà phía nhận bỏ qua khi quá hạn, và duty về 0. "In ra serial cho dễ xem" không phải giao thức.

**PID.** CSV có `t`, setpoint, tốc độ đo, và lệnh. Bánh trên không: lệnh dương khi tốc độ còn dưới setpoint. Chưa có encoder: một đoạn hoãn có ngày, cộng bài mô phỏng đã chạy và đã dán đỉnh P khoảng $0{,}29$ m/s. Không có cả CSV lẫn mô phỏng là trượt.

**Động học.** $L$ là mét, đo vết tiếp xúc, ba lần. Hàm `wheel_speeds` đổi một twist thử thành hai tốc độ, rồi đổi ngược lại ra đúng twist. $L$ bằng chiều ngang tấm mica là trượt.

**Chu kỳ.** Một số đo chu kỳ vòng lặp, hoặc một câu nói vòng PID không gọi theo `loop()` ngẫu nhiên. Thiếu số và thiếu câu là trượt.

## Một sổ trông xong mà vẫn trượt

```text
PID: bánh quay ổn, không cần CSV.
L = 16 cm. Hàm dùng 16 vì thước ghi vậy.
Quaternion: z = 1 cho góc vuông, cho dễ nhớ.
```

Cả ba dòng trượt. Ổn không phải là số. $16$ trong công thức mét là khẩu độ $16$ m. $z = 1$ là quay $180^\circ$.

## Lab

1. Chép năm cửa vào sổ, ghi đạt hoặc trượt, kèm tên file bằng chứng.
2. Với mỗi cửa trượt, viết một việc sửa dài một câu. Không viết "sẽ xem lại".
3. Chỉ ghi "chương 09 được bắt đầu" khi không còn cửa trượt, hoặc khi cửa hoãn encoder có ngày và bốn cửa kia đạt.

### Lỗi thường gặp

| Bạn thấy | Cần kiểm |
| --- | --- |
| Đủ đề mục, không có file | Chưa làm. Dán đường dẫn file thật |
| $L = 16$ | Đổi thành $0{,}16$ nếu thước là 16 cm, rồi chạy lại assert |
| CSV toàn số 0 | Encoder chưa vào ngắt, hoặc $\Delta t$ sai đơn vị |
| Mô phỏng P không vọt | Bạn đang chạy plant khác bài. Chạy lại script của bài PID |

## Video tham khảo

- **Xem trước:** [PID Control - A brief introduction](https://www.youtube.com/watch?v=UR0hOmjaHp0) — Brian Douglas, tiếng Anh. Checklist chương hỏi một bước nhảy và một tư thế từ encoder. Xem lại hình PID trước khi tick.

## Bài tập

1. Cửa nào trượt nếu quaternion đúng nhưng điểm yaw $\pi$ vẫn dương?
2. $L$ đo $0{,}158$ m, code để $15{,}8$. $R = v/\omega$ sai khoảng bao nhiêu lần?
3. Vì sao cửa PID được hoãn bằng ngày, còn cửa động học thì không?

### Gợi ý đáp án

1. Cửa toán. Quay $180^\circ$ chưa vào ma trận. 2. Khoảng 100 lần, vì $15{,}8 / 0{,}158 = 100$. 3. PID cần xung thật hoặc một mô phỏng thay thế đã chấm. Động học chỉ cần thước và hàm. Không có lý do hoãn thước.

## Đọc thêm

- [Bài toán TF]({% multilang_post_url contents/chapter08/08_00_math_for_tf %})
- [Bài PID]({% multilang_post_url contents/chapter08/08_03_pid_tuning %})
- [Bài động học]({% multilang_post_url contents/chapter08/08_04_diff_kinematics %})
