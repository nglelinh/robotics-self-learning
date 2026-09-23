---
layout: post
title: "Test thực địa, log và nghiệm thu"
chapter: "07"
order: 5
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter07
lesson_type: required
draft: false
---

Hết bài trên hộp. Bài này đặt robot xuống một làn trống, chạy bốn hướng ở PWM đã kẹp, và viết một log để chương sau tin được. Đạt là một tập quan sát, không phải cảm giác "cũng chạy được".

## Mục tiêu học

1. Chạy một chuỗi trên sàn, làn trống $$2~\mathrm{m}$$: tiến khoảng $$2~\mathrm{s}$$, dừng, lùi, quay trái, quay phải, tất cả trong khoảng $$\pm 180$$, tay cầm công tắc pin.
2. Cho thấy giết máy gửi hoặc rút USB, trong khi MCU còn ăn buck, làm chuyển động hết trong $$0{,}5~\mathrm{s}$$.
3. Ghi điện áp pin trước và sau lượt chạy, và coi sụt lớn là lỗi pack, dây, hoặc cầu chì.
4. Điền log gỡ lỗi (giờ, lệnh, robot làm gì, điện áp, giả thuyết lỗi) và chỉ nhận xe khi bảng dấu, timeout, pin đã buộc, và hình học chương 06 đều có trong ghi chú.

## Kiến thức cần có

Bài 07-01 đến 07-04 là cả phần bị điều khiển: pin buộc, cực dương có chì, buck 5,0 V, bảng dấu, giao thức chữ, bước kéo, và timeout. Chương 05 là stall và luật driver nóng. $$b$$ và $$r$$ chương 06 đã nằm trong `lab-notes.md` (ví dụ khóa học $$b = 0{,}15~\mathrm{m}$$ hoặc $$148~\mathrm{mm}$$ bạn đo, và $$r = 31{,}2~\mathrm{mm}$$). Bạn vẫn chưa publish Twist. Bạn được ghi quãng đường và thời gian. Bạn không được đóng chúng thành luật của PWM. Chương 08 mới được phép nói m/s.

## Vì sao bài này quan trọng với Capstone A và ROS

PID chương 08 giả định dấu đúng và lệnh mất thì bánh dừng. Bánh phải ngược làm số hạng tỉ lệ cộng thêm yaw sai. Chương 09 giả định đế an toàn khi publisher chết, và laptop ngủ chính là publisher ấy. Nghiệm thu là cổng: bốn hướng khớp bảng dấu, im lặng thì xe dừng, pin không rơi, và ghi chú có ảnh đi dây, đoạn giao thức, điện áp, cùng $$b$$ và $$r$$.

![Hình học log phải dẫn: $$b$$ giữa hai vết lốp, $$r$$ từ phép lăn]({{ site.imgurl }}/generated/chassis_measures.png)

![Tiến, quay, và trường hợp trộn mà bạn sắp xin bằng PWM, không bằng m/s]({{ site.imgurl }}/generated/diff_drive_kinematics.png)

Mũi tên trong hình thứ hai là các chuyển động. `V 80 80` là cả hai mũi tên tiến. `V -60 60` là vòng quay có mũi tên phải tiến và mũi tên trái lùi, yaw trái khi bảng dấu trung thực. Công thức trên hình ở đơn vị tốc độ. Lệnh của bạn ở đơn vị nấc.

## Làn, công tắc giết, và điện áp biết động

Dọn một làn $$2~\mathrm{m}$$, không có mép bàn trong khoảng phanh. Tay cầm công tắc pin. Máy chủ $$200~\mathrm{ms}$$, hạn firmware $$250~\mathrm{ms}$$, duty 60 hoặc 80, không phải 255.

Chuỗi, mỗi lệnh được gửi lại cho đến khi bạn chuyển lệnh:

1. `V 80 80` khoảng $$2~\mathrm{s}$$, cả hai lốp tiến, xe bám làn.
2. `V 0 0`, hoặc ngừng gửi để timeout nổ. Xe dừng.
3. `V -80 -80` khoảng $$2~\mathrm{s}$$, lùi thẳng.
4. `V -60 60` một vòng ngắn. Mũi sang trái.
5. `V 60 -60` một vòng ngắn. Mũi sang phải.

Rồi giết máy gửi, hoặc rút USB trong khi ESP32 còn ăn buck. Chuyển động hết trong $$0{,}5~\mathrm{s}$$. Bài 04 dự đoán khoảng $$330~\mathrm{ms}$$ sau `V 60 60` cuối. Lăn ba giây là trượt, dù bốn hướng trông đẹp.

Điện áp nghỉ trước và sau: một lượt ngắn khỏe có thể từ $$8{,}15~\mathrm{V}$$ xuống $$8{,}05~\mathrm{V}$$. Nếu đo được lúc có tải, lấy $$8{,}20~\mathrm{V}$$ lúc nghỉ và $$6{,}90~\mathrm{V}$$ ở khoảng $$0{,}60~\mathrm{A}$$:

$$
R \approx \frac{1{,}30}{0{,}60} \approx 2{,}2~\Omega.
$$

Khoảng $$2{,}2~\Omega$$ là lớn so với vài trăm miliohm của pack khỏe. Nghi cell mỏi, dây mỏng, polyfuse đang ấm, hoặc tiếp xúc đế. Sửa nguồn trước khi nhận đế. Chì sai hiện ra thành sụt, nhảy, hoặc reset giữa làn. `setup` đã ghi PWM 0 trước khi kéo STBY.

Một quãng có bấm giờ chỉ là quan sát. Đi $$1{,}6~\mathrm{m}$$ trong $$4{,}0~\mathrm{s}$$ là

$$
v_{obs} = \frac{1{,}6}{4{,}0} = 0{,}40~\mathrm{m/s}
$$

của lượt ấy, sàn ấy, duty ấy. Viết "ở PWM 80, lượt này, khoảng $$0{,}40~\mathrm{m/s}$$." Đừng viết "PWM 80 nghĩa là $$0{,}40~\mathrm{m/s}$$" như hằng số Twist.

## Log là dụng cụ nghiệm thu

Mỗi hàng là một sự kiện. Cột giả thuyết để trống khi sự kiện khớp bảng dấu. Bắt buộc điền khi có chuyện khác.

| Giờ | Lệnh | Robot làm gì | Điện áp | Giả thuyết |
|-----|------|--------------|---------|------------|
| 0:00 | nghỉ | đứng, pin đã buộc | 8,15 V | |
| 0:12 | `V 80 80` trong 2 s | thẳng theo làn | 7,9 V có tải | |
| 0:15 | giết máy gửi | dừng rõ trong 0,5 s | 8,12 V | |
| 0:30 | `V -60 60` | mũi trái | 8,0 V | |
| 0:40 | `V 60 -60` | mũi phải | 8,0 V | |

Đừng lấy trung bình một hàng xấu thành đạt. Máy gửi chết mà xe còn lăn tới băng dính thì timeout chưa được viết và PWM cuối còn trong LEDC. Đưa phép kiểm bài 04 trở lại, chứng minh dừng trên hộp, rồi chạy lại làn. `V 80 80` mà xe quay thì một dấu sai: đảo dây motor đó hoặc cực tính firmware, không cả hai. Chương 08 không bắt đầu khi một trong hai hàng còn mở.

Đạt nghĩa là tất cả các điều sau: bốn hướng khớp bảng dấu; dừng theo timeout hoạt động; pin được buộc, không có đầu lithium hàn trần; ghi chú có ảnh đi dây, đoạn giao thức (`V`, `S`, $$200~\mathrm{ms}$$, $$250~\mathrm{ms}$$), bảng dấu, các điện áp, và $$b$$ cùng $$r$$.

## Lab

### An toàn

Làn trống $$2~\mathrm{m}$$ cộng chỗ dừng, và bạn cầm công tắc pin. Duty ở mức đã tập. Xe lao về người hoặc về chỗ hụt thì ngắt công tắc. Stall vào tường là một giây, rồi ngắt. Có mùi hoặc lá không chạm được thì kết thúc.

### BOM

| Món | Việc |
|------|------|
| Cây nguồn và firmware đã nhận | Bài 01–04 |
| Sàn trống, băng ở $$2~\mathrm{m}$$ | Làn |
| Đồng hồ | Điện áp trước và sau |
| `lab-notes.md` | Log |
| Công tắc pin trong tay | Nút giết |

### Các bước

1. Xác nhận bánh đã xuống, caster chạm, pin buộc, ảnh đã có trong ghi chú. Đọc điện áp nghỉ.
2. Đứng với công tắc. Tiến khoảng $$2~\mathrm{s}$$, dừng, lùi, quay trái, quay phải. Đọc lệnh lúc gửi để log không bịa.
3. Giết máy gửi hoặc rút USB trong khi buck vẫn nuôi ESP32. Bấm giờ lần dừng. Phải trong $$0{,}5~\mathrm{s}$$.
4. Đọc lại điện áp nghỉ. Nếu thấy sụt sâu lúc có tải, ước lượng $$R$$ và viết giả thuyết.
5. Đánh đạt hoặc trượt theo bốn tiêu chí. Trượt thì chỉ một chỗ sửa, rồi chạy lại cả chuỗi.

### Kết quả mong đợi

Một log đã điền, một lần dừng trong nửa giây, điện áp nghỉ không sập, và chữ đạt chỉ khi hướng, timeout, pin, và ghi chú (ảnh, giao thức, bảng dấu, $$b$$, $$r$$) đều có. Tốc độ quan sát được ghi như một quan sát có nhãn. Nó không được nối vào giao thức.

### Lỗi thường gặp

| Bạn thấy | Thường là |
|----------|-----------|
| Lệnh thẳng mà xe vẽ vòng | Một dấu còn ngược; sửa một lần |
| Còn lăn sau khi laptop ngủ | Sketch không có timeout |
| Mũi nhấc lúc tăng tốc | Khối pin nằm sau trục; quay lại bài 01 |
| Điện áp sụt một volt trở lên ở dòng vừa phải | Cell, đế, dây, hoặc polyfuse |
| Chỉ dừng khi rút USB đồng thời reset chip | Buck không phải nguồn logic; thử lại khi MCU còn nuôi |

## Mua ở Việt Nam / Where to buy in Vietnam

Nghiệm thu hay trượt vì thiếu dây buộc, đế mỏi, hoặc cầu chì chưa mua. Giá đổi. Khoảng 2026: pack 2S hoặc đế 80.000–180.000 đồng, công tắc 8.000–20.000, đế chì và chì 2–3 A 10.000–25.000, LM2596 10.000–25.000, TB6612 25.000–70.000. L298N đã kiểm khoảng 45.000 đồng chỉ là cầu thay thế. Đừng mua khung mới để tránh đảo một dây motor.

- L298N đã kiểm, khoảng 45.000 đồng: [hshop.vn/mach-dieu-khien-dong-co-dc-l298](https://hshop.vn/mach-dieu-khien-dong-co-dc-l298)
- [Hshop cầu chì](https://hshop.vn/search?q=cau+chi), [LM2596](https://hshop.vn/search?q=LM2596)
- [Shopee pin 2S](https://shopee.vn/search?keyword=pin%202S%2018650), [công tắc](https://shopee.vn/search?keyword=c%C3%B4ng%20t%E1%BA%AFc%20ngu%E1%BB%93n)
- [Lazada holder 18650](https://www.lazada.vn/catalog/?q=holder%2018650%202S)
- [Thế Giới IC cầu chì](https://www.thegioiic.com/search?q=cau%20chi)

## Bài tập

1. Pack nghỉ $$8{,}20~\mathrm{V}$$, lúc cả hai motor chạy $$6{,}90~\mathrm{V}$$ ở khoảng $$0{,}60~\mathrm{A}$$. Ước lượng $$R$$. Nguồn ấy đạt, hay là sụt phải dừng?
2. Quãng tiến đi $$1{,}6~\mathrm{m}$$ trong $$4{,}0~\mathrm{s}$$ ở PWM 80. Bạn ghi tốc độ quan sát nào, và câu nào bị cấm ghi vào ghi chú Twist?
3. USB rút, ESP32 còn ăn buck, xe lăn khoảng $$3~\mathrm{s}$$. Dòng nghiệm thu nào trượt, và code bài nào thiếu?
4. Xe đã chạy làn, ghi chú có điện áp và ảnh, nhưng $$b$$ và $$r$$ trống. Vì sao vẫn trượt trước chương 08?
5. `V 60 -60` làm mũi quay trái. Nêu một chỗ sửa. Thay đổi thứ hai nào sẽ hủy chỗ sửa ấy?

### Gợi ý đáp án

1. $$R \approx 1{,}30/0{,}60 \approx 2{,}2~\Omega$$. Lớn so với pack khỏe vài trăm miliohm. Dừng, và nghi cell, đế, dây mỏng, hoặc polyfuse đang ấm. 2. $$v_{obs} = 1{,}6/4{,}0 = 0{,}40~\mathrm{m/s}$$ chỉ cho lượt này. Không viết "PWM 80 = $$0{,}40~\mathrm{m/s}$$" như hằng số bộ chuyển. Chương 08 hiệu chuẩn. 3. Dòng dừng theo timeout trượt. Hạn $$250~\mathrm{ms}$$ của bài 04 thiếu hoặc không tới, nên PWM cuối còn đó. 4. Động học và PID chương 08 cần bề rộng và bán kính lăn. Hình học trống nghĩa là bộ điều khiển sẽ bịa $$b$$. Nghiệm thu đã đòi hai số ấy từ chương 06. 5. Đảo dây motor phải hoặc dấu firmware bên phải, một trong hai. Làm cả hai thì yaw trái quay lại. Rồi chạy lại bốn hướng.

## Đọc thêm

- [geometry_msgs/Twist (Jazzy)](https://docs.ros.org/en/jazzy/p/geometry_msgs/interfaces/msg/Twist.html)
- [Pololu TB6612FNG](https://www.pololu.com/product/713)
- [Datasheet L298 của ST](https://www.st.com/resource/en/datasheet/l298.pdf)
- [pySerial, phần mở đầu](https://pyserial.readthedocs.io/en/latest/shortintro.html)
