---
layout: post
title: "Checklist capstone chương 07"
chapter: "07"
order: 6
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter07
lesson_type: required
draft: false
---

Đây là biên bản nghiệm thu cho giai đoạn hoàn thiện khung robot vận hành đầu tiên. Bạn chỉ chuyển sang Chương 08 khi có đủ bằng chứng cho cả bốn nhóm tiêu chí, hoặc ghi rõ một lỗi cụ thể cần khắc phục trước khi tiếp tục.

Capstone Chương 07 là cột mốc chuyển giao quan trọng nhất của nửa đầu khóa học: lần đầu tiên bạn sở hữu một con robot vật lý hoàn chỉnh có thể chạy ổn định, nhận lệnh có kiểm soát và tự dừng an toàn khi có sự cố — sẵn sàng để ở Chương 08–10 ta lắp thêm toán học TF2, điều khiển PID và hệ điều hành ROS 2 lên trên. Checklist Capstone giúp bạn nghiệm thu toàn diện cả 4 mặt: **an toàn điện, cơ khí, truyền thông teleop và hồ sơ log**.

## Kiến thức cần nhớ: Đánh giá độ tin cậy hệ thống tích hợp (System Integration)

### 1. Thống kê độ tin cậy kênh truyền thông (Packet Delivery Ratio & Jitter)
Trong hệ thống điều khiển không dây hoặc qua cáp USB gần động cơ DC, tỷ lệ mất gói trung bình (PDR) chưa kể hết câu chuyện — thứ gây kích hoạt Watchdog giả là **độ trễ biến thiên (jitter)** và số gói mất *liên tiếp* tối đa. Theo dõi cả PDR lẫn khoảng trống tối đa giữa hai gói (`max_gap_ms`) cho bức tranh sức khỏe kênh truyền đầy đủ.

### 2. Kiểm tra ranh giới an toàn kép (Phần cứng + Phần mềm)
Một robot Capstone đạt chuẩn luôn vượt qua đồng thời hai bài thử: (1) rút nguồn / gạt công tắc E-Stop vật lý ngắt toàn bộ động cơ ngay lập tức, và (2) đóng cửa sổ chương trình điều khiển trên máy tính thì Watchdog phần mềm tự phanh xe trong chưa đầy nửa giây.

### 3. Tính tái lập (Reproducibility) và tài liệu bàn giao
Một hệ thống chỉ thực sự "xong" khi người khác (hoặc chính bạn sau 1 tháng) đọc sơ đồ nối dây, bảng phân chân GPIO và tệp cấu hình là có thể bật lên chạy lại y hệt trong 5 phút.

### Giải thích: Cầm tay kiểm tra chỉ số chất lượng kênh Teleop từ tệp log 10 giây

Trong bài chạy nghiệm thu kéo dài **10 giây**, máy tính gửi lệnh ở tần số **20 Hz** (chu kỳ danh định $$50\text{ ms}$$, tổng cộng **200 gói** đã gửi). Firmware đặt ngưỡng Watchdog **$$T_{\text{wd}} = 300\text{ ms}$$** và ghi nhận từ tệp log:
- Tổng số gói hợp lệ (đúng checksum) nhận được: **198 gói** (mất 2 gói riêng lẻ không liên tiếp).
- Khoảng thời gian dài nhất đo được giữa hai gói hợp lệ liên tiếp: **`max_gap_ms = 104 ms`**.

Đánh giá định lượng 2 tiêu chí nghiệm thu:
1. **Tỷ lệ nhận gói thành công (Packet Delivery Ratio — PDR):**
   $$\mathrm{PDR} = \frac{198}{200} = 99{,}0\% \ge 98\% \implies \textbf{ĐẠT}.$$
2. **Biên an toàn chống kích hoạt Watchdog giả:**
   $$\frac{T_{\text{wd}}}{\text{max\_gap\_ms}} = \frac{300\text{ ms}}{104\text{ ms}} \approx 2{,}88\times$$
   *(Khoảng trống lớn nhất chỉ bằng $$35\%$$ ngưỡng Watchdog, chứng tỏ hệ thống còn dư biên chịu đựng gần 3 lần — vừa đủ nhạy để dừng an toàn khi đứt mạng thật, vừa không bị giật cục do kích hoạt nhầm!)*

## Mục tiêu học

1. Đánh giá sổ tay `lab-notes.md` theo đủ bốn tiêu chí hoàn thành: điều khiển teleop bốn hướng, dừng an toàn khi máy chủ quá hạn, cố định pin an toàn không có đầu hàn lithium trần, và đầy đủ hồ sơ ghi chú (ảnh đi dây, giao thức, bảng dấu, điện áp).
2. Phân tích một biên bản trượt (ví dụ xe vẫn trôi sau khi laptop ngủ, hoặc bánh phải ngược chiều) và chỉ rõ đúng một hạng mục bắt buộc phải sửa trước khi học PID hoặc ROS.
3. Phân biệt rõ một bản nghiệm thu đạt thực sự với một sổ tay chép đủ tiêu đề nhưng bỏ trống số liệu đo.
4. Liệt kê gọn đúng các linh kiện còn thiếu để hoàn tất Capstone A kèm nguồn mua tham khảo của cả chương.

## Kiến thức cần có

Toàn bộ bằng chứng từ Bài 07-01 đến 07-05: lắp ráp nguồn, bảng dấu trên hộp kê, khung lệnh `V`/`S`, bước kéo PWM và timeout, cùng nhật ký chạy thực địa. Chương 05 cung cấp nền tảng cầu H, chân `STBY`, jumper 7805 và dòng kẹt sau cầu chì 2–3 A; Chương 06 cung cấp $$b$$ và $$r$$ (ví dụ $$b = 0{,}15~\mathrm{m}$$ hoặc $$148~\mathrm{mm}$$ đo thực tế, và $$r = 31{,}2~\mathrm{mm}$$). Chương 08 sẽ xây dựng vòng điều khiển PID và Chương 09 chuyển sang `geometry_msgs/Twist` (`linear.x`, `angular.z`). Không chương sau nào tự sửa hộ lỗi thiếu timeout hay ngược cực động cơ. Bài này chưa cài đặt ROS.

## Vì sao bài này quan trọng với Capstone A và ROS

Bộ điều khiển PID khuếch đại phản hồi từ phần cứng: nếu bánh phải bị ngược chiều, sai số dương sẽ biến thành lực đẩy sai hướng ngày càng lớn. Trên ROS, nếu firmware vẫn giữ mức PWM cuối khi mất gói tin, việc phát topic `Twist` cũng gặp đúng rủi ro như cổng serial. Do đó, `Twist` chỉ được phép thay thế giao thức văn bản sau khi toàn bộ bốn tiêu chí dưới đây đều đạt. Đồng thời, trước khi sang Chương 08, tuyệt đối không gán cứng PWM 80 tương đương $$0{,}2~\mathrm{m/s}$$.

## Định nghĩa xong việc

Cả bốn tiêu chí sau đều bắt buộc:

1. **Teleop khớp bảng dấu (Bài 02):** Hai nấc dương trong khoảng $$\pm 180$$ đẩy cả hai lốp tiến về phía mũi xe; hai nấc âm làm xe lùi; `V -60 60` quay trái (bánh phải nhanh hơn cho yaw dương); `V 60 -60` quay phải. Máy chủ gửi lặp lại ít nhất mỗi $$200~\mathrm{ms}$$.
2. **Cơ chế quá hạn (timeout) hoạt động thực sự:** Sau $$250~\mathrm{ms}$$ không nhận dòng hợp lệ, mục tiêu lập tức về 0 và bộ bước kéo (15 nấc mỗi $$20~\mathrm{ms}$$) hạ duty xuống 0 (khoảng $$330~\mathrm{ms}$$ từ lệnh cuối bằng 60, nằm gọn trong $$0{,}5~\mathrm{s}$$ khi ESP32 vẫn ăn nguồn từ mạch buck). Công tắc nguồn pin luôn sẵn sàng trong tay khi chạy trên sàn — công tắc vật lý và timeout bổ trợ cho nhau, cái này không thay thế cái kia.
3. **Nguồn và pin an toàn:** Pin được cố định chắc chắn giữa trục bánh và bánh caster, đặt trong đế pin hoặc pack có BMS, không để đầu hàn trần lòng thòng. Cực dương đi qua công tắc, cầu chì 2–3 A rồi tách sang VM và mạch buck. Đầu ra buck đã chỉnh $$5{,}0~\mathrm{V}$$ trước khi gắn ESP32; dây động cơ bắt trực tiếp trên cầu đấu vít; cực âm pin, GND driver, GND buck và GND MCU nối chung về một nút.
4. **Hồ sơ `lab-notes.md` đầy đủ:** Có ảnh đi dây, đặc tả giao thức (`V`, `S`, 115200 8N1, $$200~\mathrm{ms}$$, $$250~\mathrm{ms}$$), bảng dấu, điện áp pack không tải, điện áp đầu ra buck và kích thước $$b$$, $$r$$. Mọi ô để trống đều tính là thiếu bằng chứng.

## Một sổ trượt, và chỗ sửa chặn chương 08

Dưới đây là một ví dụ nhật ký **không được ký nghiệm thu**:

| Giờ | Lệnh | Robot làm gì | Điện áp | Giả thuyết |
|-----|------|--------------|---------|------------|
| 0:10 | `V 80 80` | thẳng 2 s | nghỉ 8,10 V, sau 7,95 V | |
| 0:20 | gập laptop | còn lăn, chạm băng cuối | 7,9 V | timeout chưa viết; LEDC giữ 80 |

Hàng đi thẳng có thể rất tốt, nhưng hàng thứ hai đã đánh trượt toàn bộ biên bản. Cả Chương 08 và Chương 09 đều nhận lệnh từ một máy chủ có thể treo hoặc mất kết nối bất kỳ lúc nào. Nếu thiếu đoạn kiểm tra $$250~\mathrm{ms}$$ trong firmware, thanh ghi LEDC sẽ giữ nguyên mức duty cuối. Bạn cần bổ sung timeout, kiểm chứng lại trên hộp kê rằng `V 60 60` dừng trong $$0{,}5~\mathrm{s}$$ khi ngắt máy gửi rồi mới chạy lại trên sàn; thói quen nhanh tay rút pin không thể thay thế cơ chế an toàn phần mềm.

**Lỗi chặn thứ hai:** Lệnh `V 80 80` làm xe xoay tròn và quan sát trên hộp kê cho thấy bánh phải quay ngược. Cách khắc phục là đảo hai dây động cơ phải **hoặc** đảo cực tính chân `IN` bên phải (chỉ làm một lần và ghi rõ vào sổ). Nếu làm cả hai, dấu $$-1$$ vẫn còn nguyên, khiến PID cộng sai chiều và Chương 09 hiểu sai hướng `linear.x`.

**Lỗi chặn thứ ba:** Hai cell 18650 có đầu hàn trần chỉ dán băng dính lên khung. Một cú chạm chập xảy ra trước cầu chì (hoặc khi không có cầu chì) sẽ vượt ngoài khả năng can thiệp của timeout. Bắt buộc phải lắp đế pin hoặc pack 2S có BMS, công tắc nguồn, cầu chì 2–3 A và chụp ảnh xác nhận. Lưu ý không dùng mạch sạc 1S TP4056 (đầy gần $$4{,}2~\mathrm{V}$$) cho pack 2S (đầy gần $$8{,}4~\mathrm{V}$$).

Chỉ ký nghiệm thu khi nhật ký mới ghi đủ bốn hướng, thời gian dừng dưới $$0{,}5~\mathrm{s}$$, điện áp nghỉ trước và sau ổn định (ví dụ $$8{,}15~\mathrm{V}$$ xuống $$8{,}05~\mathrm{V}$$ sau lượt ngắn), ảnh đi dây và số đo hình học. Nếu điện áp pack sụt từ $$8{,}20~\mathrm{V}$$ xuống $$6{,}90~\mathrm{V}$$ ở dòng $$0{,}60~\mathrm{A}$$:

$$
R \approx \frac{1{,}30}{0{,}60} \approx 2{,}2~\Omega,
$$

bạn chưa được ký nghiệm thu vì đây là lỗi phần cứng nguồn cần khắc phục ngay.

## Chương 08 và chương 09 được phép giả định gì

Chương 08 mặc định rằng lệnh trái dương và lệnh phải dương đều đẩy xe tiến về phía mũi, PWM 0 làm xe dừng và hai thông số $$b$$, $$r$$ đã có sẵn trong sổ tay. Chương 08 tập trung xây dựng vòng điều khiển tốc độ, không quay lại dò chân `IN`.

Chương 09 mặc định rằng khung xe tự dừng khi luồng lệnh bị ngắt. Thông điệp `Twist` mang `linear.x` và `angular.z` sẽ thay cho hai nấc PWM, quy đổi qua phương trình Chương 06 và phép hiệu chuẩn Chương 08 (không ghi “80 nấc = $$0{,}2~\mathrm{m/s}$$” vào biên bản). Đặc tả giao thức trong sổ tay chính là chuẩn tối thiểu mà lớp tích hợp ROS sau này phải duy trì: quan sát được, có giới hạn an toàn và dừng khi mất kết nối máy chủ.

![Chỉ chạy khi lệnh còn tươi; im lặng là dừng]({{ site.imgurl }}/generated/teleop_states.png)

Nếu nhật ký chưa có số đo thực tế chứng minh hệ thống chuyển sang trạng thái `STOP` khi quá hạn thì checklist chưa hoàn thành.

## Lab

### An toàn

Chỉ chạy lại chuỗi thử nghiệm trên sàn sau khi đã khắc phục xong lỗi bị trượt; nếu không, chỉ rà soát nhật ký trên giấy. Luôn giữ công tắc pin trong tầm với mỗi khi lốp chạm sàn. Không ký nghiệm thu cho robot chưa kiểm chứng dừng bằng timeout và ngừng thao tác ngay nếu phát hiện đầu pin lithium trần.

### BOM

| Món | Việc |
|------|------|
| `lab-notes.md` bài 01–05 | Bằng chứng |
| Robot, chỉ khi một hàng phải chạy lại | Lượt thử lại |
| Đồng hồ | Kiểm buck 5,0 V và điện áp pack nếu ảnh đã cũ |
| Checklist này | Bốn dòng bạn ký tắt |

### Các bước

1. Kiểm tra lại ảnh đi dây trong sổ: phải thấy rõ công tắc, cầu chì, dây buộc pin, điểm mass chung, dây động cơ bắt vít và số đo mạch buck xấp xỉ $$5{,}0~\mathrm{V}$$ trước khi gắn ESP32.
2. Ký xác nhận bốn hướng (tiến, lùi, quay trái, quay phải) chỉ khi dòng nhật ký khớp đúng với lệnh đã gửi.
3. Đối chiếu hàng kiểm tra timeout: ngắt máy gửi hoặc rút USB trong khi MCU vẫn ăn nguồn buck, xe dừng hẳn trong $$0{,}5~\mathrm{s}$$. Thiếu dòng này đồng nghĩa chương chưa xong.
4. Rà soát sự có mặt của $$b$$, $$r$$, đặc tả giao thức và các mức điện áp. Ghi rõ ngày đủ điều kiện bắt đầu Chương 08, hoặc ghi tên một lỗi cụ thể đang chặn.
5. Nếu phải chạy lại, tuân thủ đúng quy trình làn sàn của Bài 05: sửa đúng một nguyên nhân, chạy lại toàn bộ chuỗi và ghi nhật ký mới.

### Kết quả mong đợi

Một đoạn xác nhận ngắn gọn trong sổ tay gồm: ngày đạt đủ bốn hướng, thời gian dừng timeout đo được, điện áp pack, giá trị $$b$$ và $$r$$, kèm kết luận “đủ điều kiện bắt đầu Chương 08” hoặc tên lỗi cụ thể đang cần xử lý. Các bảng để trống không được tính.

### Lỗi thường gặp

| Bạn thấy | Thường là |
|----------|-----------|
| Đề mục chép đủ, ô trống | Chương chưa làm; điền từ một lượt thật |
| "Dừng" chỉ vì rút pin | Timeout chưa được thử; rút pin là nút giết, không phải hạn |
| Cả dây lẫn firmware đều "đã sửa" | Hai lần đảo triệt nhau; quay về một lần |
| Thiếu hình học | Chương 08 sẽ bịa bề rộng |
| PWM 80 bị viết thành $$0{,}2~\mathrm{m/s}$$ | Hiệu chuẩn giả; xóa trước PID |

## Mua ở Việt Nam / Where to buy in Vietnam

Chỉ đặt mua đúng các hạng mục còn thiếu trong bảng nghiệm thu. Giá tham khảo khoảng năm 2026 (có thể thay đổi): khung 2WD 60.000–150.000 đồng, động cơ TT 25.000–45.000 đồng/chiếc, TB6612 25.000–70.000 đồng, mạch buck LM2596 10.000–25.000 đồng, pack 2S hoặc đế 18650 80.000–180.000 đồng, công tắc 8.000–20.000 đồng, đế chì kèm chì 2–3 A 10.000–25.000 đồng, ESP32 devkit 70.000–150.000 đồng. Có thể dùng L298N thay TB6612 khi hết hàng; lưu ý không mua TP4056 để sạc pack 2S.

- L298N đã kiểm, khoảng 45.000 đồng: [hshop.vn/mach-dieu-khien-dong-co-dc-l298](https://hshop.vn/mach-dieu-khien-dong-co-dc-l298)
- [Hshop TB6612](https://hshop.vn/search?q=TB6612), [LM2596](https://hshop.vn/search?q=LM2596), [ESP32](https://hshop.vn/search?q=ESP32)
- [Shopee khung 2WD](https://shopee.vn/search?keyword=khung%20xe%202WD), [cầu chì](https://shopee.vn/search?keyword=c%E1%BA%A7u%20ch%C3%AC%202A), [pin 2S](https://shopee.vn/search?keyword=pin%202S%2018650)
- [Lazada TB6612](https://www.lazada.vn/catalog/?q=TB6612), [ESP32](https://www.lazada.vn/catalog/?q=ESP32)
- [Thế Giới IC LM2596](https://www.thegioiic.com/search?q=LM2596), [L298N](https://www.thegioiic.com/search?q=L298N)

## Video tham khảo

- **Xem trước:** [TB6612FNG H-Bridge Motor Controller - Better than L298N?](https://www.youtube.com/watch?v=JPPTRj0KWbg) — DroneBot Workshop, tiếng Anh. Ôn lại việc kiểm soát chiều và tốc độ động cơ qua cầu H — yêu cầu nền tảng tối thiểu của checklist Capstone A.

## Bài tập

1. Nhật ký ghi nhận lệnh `V 80 80` đi thẳng tốt, nhưng xe vẫn tiếp tục lăn sau khi gập laptop. Tiêu chí hoàn thành nào bị trượt, và cần chứng minh điều gì trên hộp kê trước khi chuyển sang Chương 08 hoặc 09?
2. Bốn hướng chạy thử trước đó đều đạt, nhưng ghi chú bánh phải cho thấy người lắp vừa đảo dây vừa đảo thêm dấu trong firmware “cho chắc”. Lệnh PWM dương hiện tại sẽ làm bánh phải quay thế nào và cần gỡ bước nào?
3. Điện áp nghỉ đo được $$8{,}20~\mathrm{V}$$, khi có tải $$0{,}60~\mathrm{A}$$ sụt còn $$6{,}90~\mathrm{V}$$, đồng thời ảnh chụp cho thấy hai cell pin có đầu hàn trần. Tiêu chí nào bị trượt và nội trở ước lượng $$R$$ bằng bao nhiêu?
4. Một sinh viên tự đặt PWM 80 bằng $$0{,}20~\mathrm{m/s}$$ rồi áp cùng hệ số đó cho lệnh `V -60 60` với $$b = 0{,}15~\mathrm{m}$$. Họ tính ra $$\omega$$ bằng bao nhiêu, và vì sao hệ số quy đổi này không hợp lệ?
5. Từ lệnh PWM 60, xe mất $$1{,}2~\mathrm{s}$$ mới dừng hẳn sau khi ngắt máy gửi. Với bước kéo 15 nấc mỗi $$20~\mathrm{ms}$$ và hạn timeout $$250~\mathrm{ms}$$, thời gian dừng đúng thiết kế phải là bao nhiêu?

### Gợi ý đáp án

1. Tiêu chí “dừng khi máy chủ quá hạn” bị trượt. Cần kê xe lên hộp, gửi `V 60 60` rồi ngắt máy gửi và xác nhận cả hai lốp dừng trong $$0{,}5~\mathrm{s}$$ (khi MCU vẫn ăn nguồn buck) trước khi chạy lại trên sàn.
2. Hai lần đảo triệt tiêu nhau khiến lệnh dương vẫn làm bánh phải quay lùi. Cần kê bánh trên không và gỡ bỏ một trong hai lần đảo.
3. Đầu hàn trần làm trượt tiêu chí an toàn pin, và tổng trở $$R \approx 1{,}30/0{,}60 \approx 2{,}2~\Omega$$ làm trượt tiêu chí nguồn. Cần lắp đế pin hoặc pack có BMS, công tắc nguồn và cầu chì 2–3 A.
4. Hệ số $$0{,}20/80 = 0{,}0025$$ m/s mỗi nấc cho $$v_l = -0{,}15$$ m/s và $$v_r = +0{,}15$$ m/s, suy ra $$v = 0$$ và $$\omega = 0{,}30/0{,}15 = 2$$ rad/s. Con số này không hợp lệ vì hệ số quy đổi chỉ là tự gán, chưa hề đo hiệu chuẩn.
5. Thời gian dừng đúng thiết kế phải là $$250 + 4\times 20 = 330~\mathrm{ms}$$. Việc xe trôi tới $$1{,}2~\mathrm{s}$$ cho thấy cơ chế timeout đang bị thiếu hoặc đặt quá dài — không được ký nghiệm thu.

## Đọc thêm

- [geometry_msgs/Twist (Jazzy)](https://docs.ros.org/en/jazzy/p/geometry_msgs/interfaces/msg/Twist.html)
- [Mục lục gói geometry_msgs (Jazzy)](https://docs.ros.org/en/jazzy/p/geometry_msgs/)
- [Pololu TB6612FNG](https://www.pololu.com/product/713)
- [Datasheet L298 của ST](https://www.st.com/resource/en/datasheet/l298.pdf)
