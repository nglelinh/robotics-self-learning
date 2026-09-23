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

Thời lượng ước tính: **50–70 phút** để gom các ghi chú các bạn đã viết và lấp chỗ trống. Đây là cổng của chương, không phải một cơ cấu mới.

## Mục tiêu học

Hết bài này, `lab-notes.md` của các bạn giữ một khổ vết và một bán kính lăn, một cỡ ốc đã nhận dạng, một tỉ số truyền đã dự đoán và đã kiểm, một phép tính Grashof hoặc đai hoặc thanh răng, một ảnh giảm lực kéo dây hoặc một kế hoạch có ngày, và một danh sách linh kiện còn thiếu trước Chương 07. Các bạn nói được, trong một câu, mình đã đạt trên phần cứng hay trên một bản vẽ đã dán nhãn.

## Kiến thức cần có

Bài 01 đến Bài 08. Nếu một lab trong số đó chưa xong, checklist này là mục lục chỉ lab nào cần mở lại. Các bạn cần đúng cuốn sổ đã ghi milimét từ đầu chương.

## Vì sao bài này quan trọng với Capstone A và ROS

Chương 07 đặt điện áp lên khung này. Chương 08 viết các phương trình động học thành mã. `diff_drive_controller` của ROS và URDF sẽ chép $$b$$, $$r$$ và $$i$$ từ một nơi nào đó; nơi ấy phải là trang này, có ngày, có phương pháp đứng cạnh con số. Một bánh caster còn thiếu hoặc một túi nyloc còn thiếu là một dòng mua hàng, không phải một bất ngờ lúc bring-up. Điều kiện đạt là bằng chứng trong sổ. Ký ức “cơ bản là đã đo” không mở được Chương 07.

## Cổng

Chép bảng này vào `lab-notes.md` và điền cột bằng chứng bằng một con số, một tên file ảnh, hoặc các chữ “bản vẽ, chưa phải phần cứng”.

| Cổng | “Xong” trông như thế nào | Bằng chứng |
|------|------------------------|----------|
| Khổ vết $$b$$ | Milimét giữa các tâm tiếp xúc của mặt lốp | |
| Bán kính lăn $$r$$ | Từ $$s/(2\pi)$$, cả hai bánh | |
| Nhận dạng ốc | M3 được gọi tên, nyloc được phân biệt với đai ốc thường | Ảnh |
| Tỉ số truyền | Dự đoán và một phép kiểm trong khoảng 10 phần trăm, hoặc một dự đoán trên giấy đã dán nhãn | |
| Cơ cấu thanh, đai, hoặc thanh răng | Một phép thử Grashof, hoặc một tỉ số răng GT2, hoặc một hành trình thanh răng | |
| Giảm lực kéo dây | Ảnh trước/sau, hoặc một kế hoạch viết ra nếu chưa có dây | |
| Linh kiện còn thiếu | Danh sách tường minh cho buổi lắp Chương 07 | |

Đạt, viết thành văn: mọi hàng có bằng chứng, hàng tỉ số nói cách nó được kiểm, và hàng linh kiện thiếu hoặc là “không” hoặc là một danh sách mua được trong tuần này. Con đường chỉ có bản vẽ vẫn đạt cổng lập luận. Sẵn sàng phần cứng là một câu thứ hai trên cùng trang, và các bạn chỉ viết câu ấy khi tấm khung, cả hai bánh, bánh caster, và cả hai động cơ đã ở trong tay cho các phép kiểm của Bài 08. Chương 07 bắt đầu từ sẵn sàng phần cứng.

![Hai chiều dài mà cổng không nhận là số đoán]({{ site.imgurl }}/generated/chassis_measures.png)

![Tỉ số mà cổng muốn đứng cạnh những chiều dài ấy]({{ site.imgurl }}/generated/gear_train_ratio.png)

## Ví dụ tính tay

Một sinh viên lăn một bánh được $$s = 188$$ mm.

$$
r = \frac{188}{2\pi} \approx 29.9\ \text{mm}.
$$

Bánh kia cho 30,4 mm. Họ ghi cả hai và chỉ dùng 30,2 mm như trung bình làm việc sau khi đã ngồi lại lốp và lần đo thứ hai khớp trong một milimét. Khổ vết là $$b = 152$$ mm giữa các tâm tiếp xúc. Dấu đóng hộp số là 1:48, ba vòng đầu vào đo được $$23^\circ$$ so với dự đoán

$$
\frac{3}{48}\times 360^\circ = 22.5^\circ,
$$

cao khoảng 2 phần trăm, nằm trong dải. Dòng Grashof của họ là cặp của Bài 04: $$s + l = 120$$ mm, $$p + q = 125$$ mm. Ảnh giảm lực kéo dây cho thấy một dây rút và một vòng. Linh kiện thiếu: một túi nyloc. Trang ấy là một lần đạt trên phần cứng, với một dòng mua hàng không chặn cú xoay khi bánh được nhấc nếu hai đai ốc nyloc đã nằm trên giá động cơ. Nó sẽ chặn lời tuyên bố rằng mọi mối ốc đã xong.

## Lab: điền cổng từ bằng chứng đang có

### An toàn

Buổi này không cấp nguồn. Nếu các bạn lặp một cú xoay tay hoặc một phép giật, pin vẫn ngắt, như ở Bài 05 và Bài 07. Đừng “chạm thử 5 V” để xem một động cơ đã trượt mục lực cản tay có tự thoát không.

### BOM

| Hạng mục | Vai trò |
|------|------|
| `lab-notes.md` và các ảnh của chương này | Bằng chứng |
| Khung và dụng cụ, nếu các bạn đang đóng các lỗ hổng phần cứng | Chỉ những hàng không đạt |
| Danh sách mua | Hàng linh kiện còn thiếu |

### Các bước

1. Mở ghi chú của Bài 01, 02, 03 hoặc 08, 04, và 07. Chép số; đừng gõ lại từ trí nhớ nếu dòng gốc vẫn còn.
2. Điền bảng. Chỗ nào có ảnh, ghi tên file. Chỗ nào kit về muộn, viết “bản vẽ”.
3. Tính lại một phép kiểm theo kiểu ví dụ để một lỗi chép số chết ở đây: $$r$$ từ $$s$$, hoặc $$\theta_{\text{out}}$$ từ $$i$$.
4. Viết câu đạt và, nếu điều đó đúng, câu sẵn sàng phần cứng.
5. Biến hàng linh kiện thiếu thành danh sách mua bên dưới. GT2 chỉ xuất hiện nếu tỉ số của các bạn có đai.

### Kết quả mong đợi

Một bảng đã điền và hai câu. Một bạn cùng lớp làm được phần chuẩn bị cơ khí của Chương 07 từ sổ của các bạn mà không phải hỏi $$b$$. Ghi chú chỉ có bản vẽ nói điều đó trong câu đạt, và liệt kê phần cứng còn cần cho câu thứ hai.

### Lỗi thường gặp

| Các bạn thấy | Thường nghĩa là |
|--------------|------------------------|
| $$b$$ trông như một số tròn 150 không có phương pháp | Nó được nhớ lại; đo lại giữa các tâm tiếp xúc |
| Tỉ số không có góc dự đoán đứng cạnh | Phép kiểm bị bỏ; chạy Bài 08 |
| Tuyên bố sẵn sàng phần cứng từ một bản vẽ | Tách thành hai câu |
| Hàng linh kiện thiếu để trống | Nó vẫn là một hàng, kể cả khi danh sách là “không” |
| Thiếu $$r$$ của một bánh | Đo nó; hai bán kính lệch làm lệnh đi thẳng bị quay ngang |

## Mua ở Việt Nam / Where to buy in Vietnam

Chỉ mua các lỗ hổng trên hàng linh kiện thiếu của các bạn. Một bàn đã đủ không cần khung thứ hai “để dự phòng” trước Chương 07. GT2 nằm trong danh sách này chỉ khi tỉ số của Bài 04 dùng đai.

| Lỗ hổng | Từ khóa | Khoảng giá (VND) | Khi nào |
|-----|----------|------------------|------|
| Khung | `khung xe robot 2 bánh` | 80.000–200.000 | Chưa có tấm |
| Bộ ốc M3 và nyloc | `ốc M3` | 25.000–70.000 | Lần phân loại Bài 02 bị thiếu |
| Bánh caster | `bánh caster robot` | 12.000–40.000 | Mũi chưa có bánh có đuôi |
| Đai và pulley GT2 | `dây đai GT2` | 15.000–40.000 cho một đai | Chỉ khi truyền động của các bạn dùng đai |

Các trang tìm:

- [Hshop: khung](https://hshop.vn/search?q=khung+xe+robot)
- [Shopee: ốc M3](https://shopee.vn/search?keyword=%E1%BB%91c%20M3)
- [Lazada: bánh caster](https://www.lazada.vn/catalog/?q=b%C3%A1nh%20caster)
- [Thế Giới IC: ốc](https://www.thegioiic.com/search?q=%E1%BB%91c%20M3)

Giá dịch chuyển. Đặt dòng còn thiếu trước khi đăng ký bàn Chương 07, và giữ hóa đơn cạnh sổ để chi tiết về tới đúng cỡ các bạn đã đo.

## Bài tập

1. Hai quãng lăn của các bạn là 196 mm và 191 mm. Tính cả hai bán kính. Đã được lấy trung bình chưa?
2. Ba vòng, dấu đóng 1:34, góc đầu ra đo được $$33^\circ$$. Dự đoán, phần trăm sai số, và đạt hay phải làm lại?
3. $$b$$ của một đồng đội là “khoảng cách động cơ, 140 mm”. Các bạn yêu cầu họ đo lại cái gì, và triệu chứng ROS nào các bạn đang tránh?
4. Ô giảm lực kéo dây ghi “để sau”. Cổng lập luận có đạt không? Sẵn sàng phần cứng có đạt không?
5. Viết câu đạt của chính các bạn bằng những số các bạn thực sự có, gồm chữ “bản vẽ” nếu đó là sự thật.

### Gợi ý đáp án

1. $$r \approx 31.2$$ mm và $$30.4$$ mm. Độ lệch là vài milimét, nên ngồi lại lốp và đo lại trước khi lấy trung bình. 2. Dự đoán $$3/34 \times 360^\circ \approx 31.8^\circ$$. Sai số $$|33-31.8|/31.8 \approx 4$$ phần trăm, nằm trong 10 phần trăm, nên hàng tỉ số có thể đạt. 3. Yêu cầu khoảng cách giữa các tâm tiếp xúc của mặt lốp. Các bạn đang tránh một `cmd_vel` đi thẳng lại chạy thành vòng tròn. 4. Lập luận chưa đạt cho đến khi có ảnh hoặc một kế hoạch viết có ngày. Sẵn sàng phần cứng cũng chờ kế hoạch ấy được thực hiện khi dây đã có, cộng phần còn lại của Bài 08. 5. Câu phải nêu $$b$$, $$r$$, $$i$$, kết quả cơ cấu thanh hoặc đai hoặc thanh răng, và kiểu bằng chứng. Không có con số nào các bạn không đo.

## Đọc thêm

- [diff_drive_controller](https://github.com/ros-controls/ros2_controllers/tree/master/diff_drive_controller) — file nơi $$b$$, $$r$$ và số xung mỗi vòng của bảng này cuối cùng sẽ đi vào.
- [Wiki diff_drive_controller ROS 1](https://wiki.ros.org/diff_drive_controller) — tên tham số trên một trang. Văn bản ROS 1, cùng hình học.
- [Thiết lập odometry trên Nav2](https://navigation.ros.org/setup_guides/odom/setup_odom.html) — bên tiêu thụ odometry mà những tham số ấy tạo ra.
