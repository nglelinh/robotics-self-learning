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

Thời lượng ước tính: **~60 phút**. Đây là bài tổng kết nghiệm thu (cổng qua chương), không giới thiệu giao thức mới. Bạn chỉ nên chuyển sang Chương 09 khi cả năm hạng mục dưới đây đều có bằng chứng cụ thể, hoặc đã chỉ rõ lỗi cần khắc phục mà không bỏ qua.

## Mục tiêu

Bạn tự đánh giá sổ tay Chương 08 theo năm tiêu chí: toán biến đổi TF chạy kiểm chứng thành công, khung truyền serial có timeout an toàn, vòng PID có tệp log CSV, động học vi sai có khổ vết đo thực tế, và vòng điều khiển có số đo chu kỳ định thời. Mỗi tiêu chí chỉ chấm đạt hoặc trượt — mọi ô để trống đều tính là trượt.

## Kiến thức cần trước

Toàn bộ kết quả từ Bài 08-00 đến Bài 08-05. Bạn cần chuẩn bị sẵn `lab-notes.md`, tệp `math_tf_lab.py`, dữ liệu CSV của PID (nếu đã có encoder) và số đo khổ vết $L$ bằng thước. Nếu chưa có phần cứng encoder, tiêu chí PID trên xe thật có thể được ghi hoãn có ngày kèm kết quả mô phỏng, tuyệt đối không thay thế bằng nhận xét cảm tính “bánh quay thấy đều”.

## Vì sao bài này nằm trên lộ trình

Chương 09 sẽ ánh xạ $v$ và $\omega$ sang `linear.x` và `angular.z` của ROS 2, dựa trên giả định rằng quy ước dấu hai bánh và đơn vị mét đã chuẩn xác từ chương này. Chẳng hạn, ghi nhầm quaternion cho yaw $90^\circ$ thành $(0, 0, 1, 0)$ sẽ xoay ngược khung LiDAR tới $180^\circ$. Hoàn tất nghiệm thu trước khi mở workspace ROS 2 Jazzy giúp bạn tránh nhầm lẫn giữa lỗi toán hình học và lỗi truyền thông DDS.

## Đạt và trượt

**1. Toán TF:** Tệp `math_tf_lab.py` chạy không lỗi, in ra quaternion xấp xỉ $(0,\ 0,\ 0{,}7071,\ 0{,}7071)$ và tọa độ điểm $(0{,}30,\ 0)$ khi LiDAR đặt tại $x = 0{,}10$ m với điểm quét cách $0{,}20$ m. Thiếu kiểm tra `assert` hoặc thiếu trường hợp yaw $\pi$ tính là trượt.

**2. Giao thức serial:** Nhật ký ghi nhận rõ trường hợp bên nhận bỏ qua khung lỗi/quá hạn và đưa PWM về 0. Việc chỉ dùng `println` in ra Serial Monitor cho dễ đọc không đạt chuẩn giao thức.

**3. Vòng điều khiển PID:** Tệp CSV lưu đủ cột thời gian `t`, setpoint, tốc độ đo và tín hiệu lệnh. Khi kê bánh trên không, lệnh phải dương lúc tốc độ thấp hơn setpoint. Nếu chưa có encoder thật, bắt buộc có dòng ghi hoãn kèm ngày thực hiện, đồng thời chạy thành công đoạn mã mô phỏng và dán kết quả đỉnh bộ P xấp xỉ $0{,}29$ m/s; thiếu cả CSV lẫn mô phỏng là trượt.

**4. Động học vi sai:** Khổ vết $L$ được đo ba lần giữa hai tâm vết tiếp xúc và lưu theo đơn vị mét. Hàm `wheel_speeds` chuyển đổi một lệnh thử thành tốc độ hai bánh rồi tính ngược lại khớp đúng lệnh ban đầu. Dùng chiều ngang tấm mica làm $L$ tính là trượt.

**5. Định thời vòng lặp:** Có số đo chu kỳ thực tế (p50, p95, max), hoặc có cấu trúc định thời rõ ràng chứng minh vòng PID không chạy tùy tiện theo nhịp `loop()` ngẫu nhiên. Thiếu cả số đo lẫn cấu trúc định thời là trượt.

## Một sổ trông xong mà vẫn trượt

```text
PID: bánh quay ổn, không cần CSV.
L = 16 cm. Hàm dùng 16 vì thước ghi vậy.
Quaternion: z = 1 cho góc vuông, cho dễ nhớ.
```

Cả ba dòng trên đều trượt: “quay ổn” không phải bằng chứng đo đạc; nhập $16$ vào công thức đơn vị mét tương đương khổ vết $16$ m; và $z = 1$ (với $w = 0$) là góc quay $180^\circ$ chứ không phải $90^\circ$.

## Lab

1. Chép đủ năm tiêu chí vào `lab-notes.md`, chấm rõ “đạt” hoặc “trượt” kèm tên tệp bằng chứng tương ứng.
2. Với mỗi tiêu chí trượt, viết một câu cụ thể nêu rõ hành động khắc phục (không ghi chung chung kiểu “sẽ xem lại”).
3. Chỉ ghi xác nhận “đủ điều kiện bắt đầu Chương 09” khi cả năm tiêu chí đều đạt (hoặc bốn tiêu chí đạt kèm mục hoãn encoder có ngày cụ thể và đã chạy đạt phần mô phỏng PID).

### Lỗi thường gặp

| Bạn thấy | Cần kiểm |
| --- | --- |
| Đủ đề mục, không có file | Chưa làm. Dán đường dẫn file thật |
| $L = 16$ | Đổi thành $0{,}16$ nếu thước là 16 cm, rồi chạy lại assert |
| CSV toàn số 0 | Encoder chưa vào ngắt, hoặc $\Delta t$ sai đơn vị |
| Mô phỏng P không vọt | Bạn đang chạy plant khác bài. Chạy lại script của bài PID |

## Video tham khảo

- **Xem trước:** [PID Control - A brief introduction](https://www.youtube.com/watch?v=UR0hOmjaHp0) — Brian Douglas, tiếng Anh. Ôn lại đặc tính đáp ứng bước nhảy của PID trước khi hoàn tất checklist kiểm tra chương này.

## Bài tập

1. Tiêu chí nào bị trượt nếu quaternion yaw $90^\circ$ đã đúng nhưng tọa độ điểm ứng với góc yaw $\pi$ vẫn ra số dương?
2. Khổ vết thực đo được $L = 0{,}158$ m nhưng trong mã nguồn nhập nhầm thành $15{,}8$. Bán kính quay $R = v/\omega$ bị sai lệch khoảng bao nhiêu lần?
3. Vì sao tiêu chí PID trên phần cứng thật có thể tạm hoãn có ngày (kèm mô phỏng), còn tiêu chí động học thì không?

### Gợi ý đáp án

1. Tiêu chí Toán TF bị trượt vì phép quay $180^\circ$ chưa được áp dụng đúng vào ma trận biến đổi.
2. Sai lệch 100 lần, vì $15{,}8 / 0{,}158 = 100$.
3. PID trên xe thật phụ thuộc phần cứng encoder (có thể thay thế tạm bằng mô phỏng đã kiểm chứng), còn động học chỉ cần thước đo khung xe và viết hàm Python nên không có lý do để trì hoãn.

## Đọc thêm

- [Bài toán TF]({% multilang_post_url contents/chapter08/08_00_math_for_tf %})
- [Bài PID]({% multilang_post_url contents/chapter08/08_03_pid_tuning %})
- [Bài động học]({% multilang_post_url contents/chapter08/08_04_diff_kinematics %})
