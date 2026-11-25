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

Thời lượng: **~40 phút**. Bất kỳ tệp checkpoint nào tải về cũng không thay thế được phần phân tích bằng văn bản trong sổ thực hành.

Danh sách nghiệm thu cuối cùng của khóa học tổng kết toàn bộ quy trình thực hành **Robot Learning** ở Chương 12 — từ việc kiểm tra vòng teleoperation ổn định, xuất bản bộ dữ liệu chuẩn `LeRobotDataset`, huấn luyện thành công chính sách bắt chước (ACT hoặc Diffusion Policy) cho tới đánh giá định lượng tỷ lệ thành công trên các lần thử nghiệm độc lập.

## Kiến thức cần nhớ: Ba tiêu chuẩn nghiệm thu Robot Learning (Chương 12)

1. **Dữ liệu Chuẩn hóa & Tái lập được**:
   Dataset ghi đủ số lượt trình diễn yêu cầu, tần số khung hình ổn định, không lệch đồng bộ giữa camera và góc khớp, và đọc lại sạch bằng trình xem của `LeRobot`.
2. **Huấn luyện Hội tụ & Theo dõi Loss Minh bạch**:
   Lưu đầy đủ tệp cấu hình siêu tham số, đường cong hàm mất mát (loss curve) và checkpoint mô hình để bất kỳ ai cũng có thể đánh giá lại.
3. **Đánh giá Định lượng Công bằng (Multi-Trial Evaluation)**:
   Không chỉ quay 1 video "chọn lọc lúc thành công": phải chạy đủ số lượt kiểm thử liên tiếp (ví dụ 10 lượt ở các vị trí vật thể khác nhau), ghi rõ tỷ lệ thành công và phân tích nguyên nhân các lượt thất bại.

## Mục tiêu

Bạn cần hoàn thành và xác nhận bốn tiêu chí đọc hiểu cùng một tiêu chí thực hành tay SO-101: dataset card, đoạn phân tích đa phương án (diffusion), bảng đối chiếu VLA, kế hoạch lộ trình tháng tới và log lab tay SO-101 (hoặc ghi chú hoãn có ngày). Việc chạy huấn luyện thành công trên GPU không bù đắp được cho một dataset card thiếu đơn vị.

## Kiến thức cần trước

Hoàn thành các bài từ 12-01 đến 12-06. Xe Capstone vẫn giữ cặp hành động $(v, \omega)$ trừ khi dataset card chỉ rõ đang mô tả cánh tay 6 khớp.

## Vì sao bài này nằm trên lộ trình

Đây là chốt kiểm tra cuối cùng của toàn khóa học, giúp bạn tránh nhầm lẫn khi ghép kênh đầu ra của OpenVLA sang PWM xe vi sai, đồng thời không hiểu nhầm lỗi thiếu bộ nhớ CUDA khi chạy `lerobot-train` là trượt bài lab.

## Tiêu chí đạt và không đạt

**Dataset card.** Ghi đầy đủ `fps`, tên khóa ảnh, tên khóa hành động và đơn vị. Card cho xe Capstone dùng m/s và rad/s; card cho SO-101 ghi đúng số trục thực tế (6 khớp trên follower) và chỉ ghi đơn vị nếu metadata dataset có khai báo (tuyệt đối không tự bịa đơn vị).

**Diffusion Policy.** Đoạn phân tích nêu rõ hai phiên mẫu đi hai phía, chứng minh lệnh trung bình đâm vào vật cản và có câu xác nhận không huấn luyện. Đoạn chỉ khen chung chung "xử lý đa mode tốt" là chưa đạt.

**Bảng VLA.** Điền đủ hai dòng bảng so sánh, không có dòng nào trả lời "có" cho việc huấn luyện tại nhà, kèm một dòng đối chiếu SO-101 khẳng định vector 6 khớp không trùng với hành động của RT-1 hay OpenVLA.

**Lộ trình tiếp theo.** Chọn duy nhất một hướng cho tháng tới từ bài 12-05, ghi rõ một đường dẫn đầu tiên sẽ mở và nêu ít nhất một món sẽ không mua theo cảm tính.

**Thực hành tay SO-101.** Theo bài 12-06: có log cổng kết nối cùng một lần hiệu chỉnh/teleop, hoặc có ghi chú hoãn ghi rõ ngày (do chưa có phần cứng) đi kèm dataset card trên giấy. Việc mua tay máy không phải điều kiện bắt buộc để đạt.

### Giải thích: Cách báo cáo kết quả đánh giá chính sách Robot Learning đúng chuẩn khoa học

Giả sử bạn đánh giá chính sách ACT vừa huấn luyện trên **10 lượt thử liên tiếp** (đặt khối vật thể ở 5 vị trí trong tập huấn luyện và 5 vị trí dịch lệch mới):

| Nhóm kiểm thử | Số lượt thành công / tổng | Tỷ lệ thành công | Ghi chú phân tích lỗi |
| :--- | :---: | :---: | :--- |
| Trong vùng vị trí huấn luyện (In-Distribution) | `4 / 5` | **80%** | 1 lượt kẹp hơi lệch mép khi bóng đèn chiếu chói |
| Vị trí mới dịch lệch 5 cm (Out-of-Distribution) | `2 / 5` | **40%** | Cần bổ sung thêm 20 lượt trình diễn phủ rộng biên bàn |
| **Tổng hợp báo cáo** | **`6 / 10`** | **60%** | Trung thực, có hướng cải thiện dữ liệu rõ ràng! |

Thói quen đánh giá tách biệt In-Distribution và Out-of-Distribution này là tiêu chuẩn vàng trong mọi bài báo và sản phẩm Robot Learning hiện đại.

## Lab

Sao chép mẫu sau vào sổ thực hành và điền đầy đủ kết quả:

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

| Hiện tượng | Hướng kiểm tra |
| --- | --- |
| Card ghi hành động là PWM nhưng chú thích lại ghi rad/s | Lệch đơn vị giữa hai hệ khác nhau; chọn thống nhất một hệ |
| Dán lỗi `CUDA out of memory` vào mục kết quả đạt | Bài lab không chấm GPU; hoàn thiện đúng phần phân tích văn bản |
| Điền "có" vào cột `Twist` trong bảng VLA | Xem lại khái niệm hình thái phần cứng (embodiment) và sửa lại thành "không" |

## Video tham khảo

- **Xem trước:** [How to Train an AI Robotic Arm With No Code (Hugging Face LeRobot + SO-101)](https://www.youtube.com/watch?v=7tGT8hqRSAo) — Brogan M. Pratt (tiếng Anh). Quan sát trực quan cấu trúc tay SO-101 trước khi xác nhận lộ trình phần cứng hoặc lập dataset card.

## Bài tập

1. Nếu đoạn phân tích Diffusion Policy đạt chuẩn nhưng dataset card lại thiếu `fps`, tiêu chí nào chưa đạt?
2. Một ghi chú hoãn thực hành tay SO-101 nhưng không ghi ngày cụ thể có được tính là đạt không?
3. Vì sao việc tải thành công một checkpoint OpenVLA vẫn không làm tiêu chí thực hành tay SO-101 đạt yêu cầu?

### Gợi ý đáp án

1. Tiêu chí Dataset card chưa đạt, vì đoạn phân tích lý thuyết không thay thế được thông số tần số lấy mẫu của dữ liệu.
2. Không — ghi chú hoãn bắt buộc có ngày cụ thể và lý do rõ ràng.
3. Checkpoint tải về không chứng minh bạn đã hiệu chỉnh servo STS3215 hay khớp đúng không gian hành động 6 chiều của SO-101.

## Đọc thêm

- [LeRobot](https://huggingface.co/docs/lerobot/index)
- [SO-101](https://huggingface.co/docs/lerobot/so101)
- [Lab tay]({% multilang_post_url contents/chapter12/12_06_so101_arm_lab %})
