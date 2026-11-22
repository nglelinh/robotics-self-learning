---
layout: post
title: "Checklist lab chương 06"
chapter: "06"
order: 9
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter06
lesson_type: required
draft: false
---

Thời lượng ước tính: **50–70 phút** để tổng hợp các ghi chép đã làm và bổ sung những mục còn thiếu. Đây là bài kiểm tra tổng kết (cổng qua chương), không giới thiệu cơ cấu mới.

## Mục tiêu học

Sau bài này, tệp `lab-notes.md` của bạn có đầy đủ: khổ vết $$b$$ và bán kính lăn $$r$$, kết quả nhận dạng cỡ ốc, tỉ số truyền đã dự đoán và đo kiểm, một phép tính cơ cấu bốn thanh (Grashof), đai hoặc thanh răng, ảnh giảm lực kéo dây (hoặc kế hoạch có ngày thực hiện) và danh sách linh kiện còn thiếu cho Chương 07. Bạn cũng chốt được trong một câu rõ ràng rằng mình đã đạt cổng trên phần cứng thực tế hay trên bản vẽ có dán nhãn.

## Kiến thức cần có

Nội dung từ Bài 01 đến Bài 08. Nếu có bài thực hành nào chưa xong, checklist này đóng vai trò mục lục giúp bạn mở lại đúng bài đó. Hãy sử dụng đúng sổ tay đã ghi các số đo milimét từ đầu chương.

## Vì sao bài này quan trọng với Capstone A và ROS

Chương 07 sẽ bắt đầu cấp điện cho khung robot và Chương 08 sẽ lập trình các phương trình động học. Cả `diff_drive_controller` lẫn tệp URDF trong ROS đều cần lấy các tham số $$b$$, $$r$$ và $$i$$ từ một nguồn thống nhất: trang tổng hợp có ghi ngày và phương pháp đo này. Việc thiếu bánh caster hay thiếu túi đai ốc nyloc nên nằm trong danh sách mua sắm từ bây giờ thay vì trở thành sự cố bất ngờ lúc lắp ráp. Điều kiện qua chương là bằng chứng ghi rõ trong sổ tay — không thể dựa vào trí nhớ ước chừng để sang Chương 07.

## Cổng

Chép bảng dưới đây vào `lab-notes.md` và điền cột bằng chứng bằng số đo cụ thể, tên tệp ảnh, hoặc ghi chú “bản vẽ, chưa phải phần cứng”.

| Cổng | “Xong” trông như thế nào | Bằng chứng |
|------|------------------------|----------|
| Khổ vết $$b$$ | Milimét giữa các tâm tiếp xúc của mặt lốp | |
| Bán kính lăn $$r$$ | Từ $$s/(2\pi)$$, cả hai bánh | |
| Nhận dạng ốc | M3 được gọi tên, nyloc được phân biệt với đai ốc thường | Ảnh |
| Tỉ số truyền | Dự đoán và một phép kiểm trong khoảng 10 phần trăm, hoặc một dự đoán trên giấy đã dán nhãn | |
| Cơ cấu thanh, đai, hoặc thanh răng | Một phép thử Grashof, hoặc một tỉ số răng GT2, hoặc một hành trình thanh răng | |
| Giảm lực kéo dây | Ảnh trước/sau, hoặc một kế hoạch viết ra nếu chưa có dây | |
| Linh kiện còn thiếu | Danh sách tường minh cho buổi lắp Chương 07 | |

**Điều kiện đạt:** Mọi hàng đều có bằng chứng cụ thể; hàng tỉ số truyền nêu rõ cách kiểm chứng; hàng linh kiện còn thiếu ghi rõ “không” hoặc liệt kê danh sách đặt mua trong tuần. Nếu mới chỉ làm trên bản vẽ, bạn vẫn đạt cổng lập luận. Tuy nhiên, trạng thái “sẵn sàng phần cứng” là một xác nhận riêng trên cùng trang đó, chỉ được ghi khi tấm khung, hai bánh xe, bánh caster và hai động cơ đều đã có sẵn trên bàn và hoàn thành kiểm tra ở Bài 08. Chương 07 chỉ bắt đầu khi đạt trạng thái sẵn sàng phần cứng.

![Hai chiều dài mà cổng không nhận là số đoán]({{ site.imgurl }}/generated/chassis_measures.png)

![Tỉ số mà cổng muốn đứng cạnh những chiều dài ấy]({{ site.imgurl }}/generated/gear_train_ratio.png)

## Ví dụ tính tay

Một sinh viên lăn thử bánh thứ nhất được quãng đường $$s = 188$$ mm, suy ra:

$$
r = \frac{188}{2\pi} \approx 29.9\ \text{mm}.
$$

Bánh còn lại cho kết quả 30,4 mm. Sinh viên ghi cả hai số đo, kiểm tra lại độ đồng tâm của lốp để xác nhận sai lệch nằm trong 1 mm rồi lấy giá trị trung bình làm việc là 30,2 mm. Khổ vết đo giữa hai tâm tiếp xúc là $$b = 152$$ mm. Hộp số đóng dấu 1:48; sau 3 vòng đầu vào, góc đo được là $$23^\circ$$ so với dự đoán:

$$
\frac{3}{48}\times 360^\circ = 22.5^\circ,
$$

sai lệch khoảng 2%, đạt yêu cầu. Mục Grashof ghi đúng ví dụ Bài 04 ($$s + l = 120$$ mm, $$p + q = 125$$ mm). Ảnh giảm lực kéo dây thể hiện rõ dây rút và vòng dây dự phòng. Mục linh kiện còn thiếu ghi: một túi đai ốc nyloc. Như vậy, trang ghi chép này đạt cổng phần cứng (có thể thực hiện bước thử nhấc bánh nếu giá động cơ đã đủ hai đai ốc nyloc, dù chưa thể kết luận toàn bộ mối ốc đã hoàn tất cho tới khi mua đủ túi nyloc).

## Lab: điền cổng từ bằng chứng đang có

### An toàn

Buổi tổng hợp này không cấp nguồn điện. Nếu cần lặp lại phép xoay tay hoặc kiểm tra lực kéo dây, pin phải được ngắt hoàn toàn như hướng dẫn ở Bài 05 và Bài 07. Không “kích thử 5 V” để kiểm tra một động cơ bị nặng tay khi xoay.

### BOM

| Hạng mục | Vai trò |
|------|------|
| `lab-notes.md` và các ảnh của chương này | Bằng chứng |
| Khung và dụng cụ, nếu các bạn đang đóng các lỗ hổng phần cứng | Chỉ những hàng không đạt |
| Danh sách mua | Hàng linh kiện còn thiếu |

### Các bước

1. Mở lại ghi chú của Bài 01, 02, 03 (hoặc 08), 04 và 07; chép chính xác số liệu đã đo thay vì nhập lại theo trí nhớ.
2. Điền đầy đủ bảng cổng: ghi tên tệp ảnh ở các mục yêu cầu ảnh, hoặc ghi “bản vẽ” nếu bộ kit chưa về.
3. Tính lại một phép kiểm tra theo mẫu ví dụ ($$r$$ từ $$s$$ hoặc $$\theta_{\text{out}}$$ từ $$i$$) để loại bỏ sai sót do chép nhầm số.
4. Viết câu xác nhận đạt cổng và (nếu đủ điều kiện) câu xác nhận sẵn sàng phần cứng.
5. Chuyển mục linh kiện còn thiếu thành danh sách mua sắm cụ thể; chỉ đưa bộ đai GT2 vào nếu truyền động của bạn thực sự dùng đai.

### Kết quả mong đợi

Một bảng cổng điền đầy đủ kèm hai câu xác nhận rõ ràng, đủ để một đồng đội khác có thể bắt tay vào phần cơ khí Chương 07 dựa trên sổ tay của bạn mà không cần hỏi lại giá trị $$b$$. Nếu dùng đường bản vẽ, câu xác nhận nêu rõ điều này và liệt kê phần cứng cần bổ sung.

### Lỗi thường gặp

| Các bạn thấy | Thường nghĩa là |
|--------------|------------------------|
| $$b$$ trông như một số tròn 150 không có phương pháp | Nó được nhớ lại; đo lại giữa các tâm tiếp xúc |
| Tỉ số không có góc dự đoán đứng cạnh | Phép kiểm bị bỏ; chạy Bài 08 |
| Tuyên bố sẵn sàng phần cứng từ một bản vẽ | Tách thành hai câu |
| Hàng linh kiện thiếu để trống | Nó vẫn là một hàng, kể cả khi danh sách là “không” |
| Thiếu $$r$$ của một bánh | Đo nó; hai bán kính lệch làm lệnh đi thẳng bị quay ngang |

## Mua ở Việt Nam / Where to buy in Vietnam

Chỉ đặt mua đúng những hạng mục còn thiếu trong bảng tổng hợp. Không cần mua dự phòng thêm khung xe thứ hai trước khi vào Chương 07, và chỉ mua đai GT2 khi thiết kế ở Bài 04 có dùng đai.

| Lỗ hổng | Từ khóa | Khoảng giá (VND) | Khi nào |
|-----|----------|------------------|------|
| Khung | `khung xe robot 2 bánh` | 80.000–200.000 | Chưa có tấm |
| Bộ ốc M3 và nyloc | `ốc M3` | 25.000–70.000 | Lần phân loại Bài 02 bị thiếu |
| Bánh caster | `bánh caster robot` | 12.000–40.000 | Mũi chưa có bánh có đuôi |
| Đai và pulley GT2 | `dây đai GT2` | 15.000–40.000 cho một đai | Chỉ khi truyền động của các bạn dùng đai |

Các trang tìm mua:

- [Hshop: khung](https://hshop.vn/search?q=khung+xe+robot)
- [Shopee: ốc M3](https://shopee.vn/search?keyword=%E1%BB%91c%20M3)
- [Lazada: bánh caster](https://www.lazada.vn/catalog/?q=b%C3%A1nh%20caster)
- [Thế Giới IC: ốc](https://www.thegioiic.com/search?q=%E1%BB%91c%20M3)

Giá bán có thể thay đổi theo thời điểm. Hãy đặt sớm các linh kiện còn thiếu trước buổi lab Chương 07 và giữ thông tin đơn hàng để đối chiếu đúng cỡ đã đo khi nhận hàng.

## Video tham khảo

- **Xem trước:** [Gear Train Design - How to calculate gear trains mechanical engineering](https://www.youtube.com/watch?v=aGHrhm-Rcp0) — The Engineering Mindset, tiếng Anh. Ôn lại cách tính và nhân tỉ số truyền trước khi đánh dấu hoàn thành checklist cơ khí.

## Bài tập

1. Hai phép lăn một vòng cho kết quả 196 mm và 191 mm. Tính bán kính lăn của cả hai bánh; đã nên lấy trung bình ngay chưa?
2. Với hộp số đóng dấu 1:34, sau ba vòng đầu vào đo được góc đầu ra $$33^\circ$$. Tính góc dự đoán, phần trăm sai số và cho biết kết quả này đạt hay cần đo lại.
3. Một thành viên ghi khổ vết $$b$$ là “khoảng cách giữa hai động cơ, 140 mm”. Bạn cần yêu cầu họ đo lại kích thước nào, và việc đó giúp tránh triệu chứng gì trên ROS?
4. Ô giảm lực kéo dây ghi “để sau”. Cổng lập luận và trạng thái sẵn sàng phần cứng có đạt không?
5. Tự viết câu xác nhận đạt cổng bằng số liệu thực tế bạn có (ghi rõ “bản vẽ” nếu chưa có phần cứng).

### Gợi ý đáp án

1. Hai bán kính lần lượt là $$r \approx 31.2$$ mm và $$30.4$$ mm. Dù chênh lệch bán kính là 0,8 mm (gần sát ngưỡng 1 mm), chênh lệch quãng lăn tới 5 mm cho thấy lốp có thể lắp chưa đều; nên lắp chỉnh lại lốp và đo kiểm tra thêm một lần nữa trước khi lấy trung bình.
2. Góc dự đoán: $$\frac{3}{34} \times 360^\circ \approx 31.8^\circ$$. Sai số tương đối: $$|33 - 31.8|/31.8 \approx 4\%$$, nằm gọn trong ngưỡng 10% nên đạt.
3. Yêu cầu đo lại khoảng cách giữa hai tâm tiếp xúc của mặt lốp. Việc này tránh hiện tượng gửi lệnh `cmd_vel` đi thẳng nhưng robot lại chạy cong thành vòng tròn.
4. Cổng lập luận chưa đạt cho tới khi có ảnh chụp hoặc một kế hoạch cụ thể có ngày thực hiện. Trạng thái sẵn sàng phần cứng cũng chỉ đạt sau khi hoàn thiện giảm lực kéo dây thực tế cùng toàn bộ checklist Bài 08.
5. Câu xác nhận cần nêu đầy đủ $$b$$, $$r$$, $$i$$, kết quả mục cơ cấu thanh/đai/thanh răng và loại bằng chứng (phần cứng hay bản vẽ), tuyệt đối không dùng số ước đoán.

## Đọc thêm

- [diff_drive_controller](https://github.com/ros-controls/ros2_controllers/tree/master/diff_drive_controller) — tệp cấu hình nơi các tham số $$b$$, $$r$$ và số xung mỗi vòng của bảng tổng hợp này sẽ được nhập vào.
- [Wiki diff_drive_controller ROS 1](https://wiki.ros.org/diff_drive_controller) — tổng hợp tên tham số trên một trang (tài liệu ROS 1 nhưng giữ nguyên mô hình hình học).
- [Thiết lập odometry trên Nav2](https://navigation.ros.org/setup_guides/odom/setup_odom.html) — hệ thống tiêu thụ trực tiếp dữ liệu odometry sinh ra từ các tham số trên.
