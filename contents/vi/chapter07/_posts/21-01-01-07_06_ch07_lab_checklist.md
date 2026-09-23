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

Đây là biên bản ký cho đế biết chạy lần đầu. Có bằng chứng cho bốn hành vi, hoặc có một chỗ sửa được gọi tên và chưa được vào chương 08.

## Mục tiêu học

1. Chấm một sổ lab theo bốn dòng xong việc: teleop bốn hướng, dừng khi máy chủ hết hạn, pin được buộc và không có đầu lithium trần, và ghi chú có ảnh, giao thức, bảng dấu, cùng các điện áp.
2. Đọc một biên bản trượt (xe còn lăn sau khi laptop ngủ, hoặc bánh phải ngược) và gọi tên một chỗ sửa phải xong trước PID hoặc topic ROS.
3. Tách một lần đạt thật khỏi một sổ có đúng các đề mục mà ô đo thì trống.
4. Liệt kê chỉ những món còn thiếu để khép capstone này, cùng các cửa hàng của cả chương.

## Kiến thức cần có

Bài 07-01 đến 07-05 là bằng chứng: lắp ráp, bảng dấu bánh trên không, `V` và `S`, timeout và bước kéo, log trên sàn. Chương 05 là cầu H, STBY, jumper 7805, và dòng stall đứng sau cầu chì 2–3 A. Chương 06 là $$b$$ và $$r$$ (ví dụ $$0{,}15~\mathrm{m}$$ hoặc $$148~\mathrm{mm}$$ bạn đo, và $$31{,}2~\mathrm{mm}$$). Chương 08 là PID. Chương 09 thay dòng chữ bằng `geometry_msgs/Twist` (`linear.x`, `angular.z`). Không chương nào sửa hộ timeout thiếu hoặc lốp ngược. Checklist này không cài ROS.

## Vì sao bài này quan trọng với Capstone A và ROS

PID khuếch đại phần bị điều khiển. Bánh phải ngược biến sai số dương thành lệnh sai lớn hơn. Đồ thị topic dính PWM giống cổng serial nếu firmware giữ duty cuối khi bản tin ngừng. Twist chỉ thay dòng chữ sau bốn dòng xong việc bên dưới. Trước chương 08, PWM 80 không phải $$0{,}2~\mathrm{m/s}$$.

## Định nghĩa xong việc

Cả bốn dòng đều bắt buộc.

Teleop khớp bảng dấu bài 02. Tiến là hai nấc dương trong $$\pm 180$$, cả hai lốp về mũi. Lùi là cả hai âm. Quay trái là `V -60 60` vì phải nhanh hơn thì yaw trái. Quay phải là `V 60 -60`. Máy chủ gửi lại ít nhất mỗi $$200~\mathrm{ms}$$.

Timeout máy chủ có tác dụng. Sau $$250~\mathrm{ms}$$ không có dòng hợp lệ, target về 0, và bước kéo 15 nấc mỗi $$20~\mathrm{ms}$$ đưa duty xuống. Từ lệnh cuối bằng 60, khoảng $$330~\mathrm{ms}$$, nằm trong $$0{,}5~\mathrm{s}$$ bạn đã đo khi MCU còn ăn buck. Công tắc pin ở trong tay lúc trên sàn. Công tắc không thay timeout, và timeout không thay công tắc.

Pin được buộc giữa trục và caster. Lithium ở trong đế hoặc pack có BMS, không có đầu hàn trần lòng thòng. Cực dương đi công tắc, rồi chì 2–3 A, rồi VM và buck. Buck đã là $$5{,}0~\mathrm{V}$$ trước khi gắn ESP32. Dây motor ở vít. Cực âm pin, GND driver, GND buck và GND MCU là một nút.

`lab-notes.md` có ảnh đi dây, đoạn giao thức (`V`, `S`, 115200 8N1, $$200~\mathrm{ms}$$, $$250~\mathrm{ms}$$), bảng dấu, điện áp pack không tải, đầu ra buck, và $$b$$ cùng $$r$$. Ô trống là số đo còn thiếu.

## Một sổ trượt, và chỗ sửa chặn chương 08

Đây là log không được ký.

| Giờ | Lệnh | Robot làm gì | Điện áp | Giả thuyết |
|-----|------|--------------|---------|------------|
| 0:10 | `V 80 80` | thẳng 2 s | nghỉ 8,10 V, sau 7,95 V | |
| 0:20 | gập laptop | còn lăn, chạm băng cuối | 7,9 V | timeout chưa viết; LEDC giữ 80 |

Hàng thẳng có thể ổn trong khi hàng thứ hai là chết. Chương 08 và chương 09 đều rót lệnh từ một máy chủ có quyền chết. Khi phép $$250~\mathrm{ms}$$ chưa có trong sketch, giết máy gửi để duty cuối còn áp. Đưa phép kiểm trở lại, trên hộp xác nhận `V 60 60` chết trong $$0{,}5~\mathrm{s}$$, rồi chạy lại làn. Quen tay rút pin không phải thiết kế.

Lỗi thứ hai: `V 80 80` làm xe quay, và ảnh bánh trên không cho thấy cờ phải đi ngược. Chỉ một lần đảo, hoặc hai vít motor phải, hoặc cực IN phải, và ghi bạn đã làm cách nào. Làm cả hai thì triệt. Bánh ấy là hệ số $$-1$$. PID sẽ cộng lực sai chiều, và chương 09 sẽ publish chiều sai ấy như thể `linear.x` trung thực.

Lỗi thứ ba: hai cell 18650 hàn đầu trần, dán băng lên tấm. Một cú vướng chập phía trước cầu chì bị quên, và timeout không có phiếu bầu. Lắp đế hoặc pack 2S có BMS, một công tắc, và chì 2–3 A, rồi chụp ảnh. TP4056 vẫn là sạc sai: 1S, đầy gần $$4{,}2~\mathrm{V}$$, trong khi pack đầy gần $$8{,}4~\mathrm{V}$$.

Ký khi log mới có bốn hướng, dừng trong $$0{,}5~\mathrm{s}$$, điện áp nghỉ trước và sau (phiên ngắn có thể $$8{,}15~\mathrm{V}$$ rồi $$8{,}05~\mathrm{V}$$), ảnh, và hình học. Nếu pack rơi từ $$8{,}20~\mathrm{V}$$ xuống $$6{,}90~\mathrm{V}$$ ở $$0{,}60~\mathrm{A}$$,

$$
R \approx \frac{1{,}30}{0{,}60} \approx 2{,}2~\Omega,
$$

bạn không ký. Sụt ấy là sửa nguồn, không phải giấy miễn cho phần mềm.

## Chương 08 và chương 09 được phép giả định gì

Chương 08 được giả định lệnh trái dương và lệnh phải dương đều lăn tiến, rằng bạn đã thấy PWM 0 dừng xe, và $$b$$ cùng $$r$$ là các số trong ghi chú. Nó xây vòng tốc độ. Nó không đi tìm lại chân IN.

Chương 09 được giả định đế dừng khi dòng lệnh dừng. Twist sẽ mang `linear.x` và `angular.z` thay cho hai số PWM, đổi bằng phương trình chương 06 và hiệu chuẩn chương 08. Đừng viết "80 nấc = $$0{,}2~\mathrm{m/s}$$" vào biên bản. Đoạn giao thức trong ghi chú là đặc tả mà bộ thích nghi ấy phải vượt: nhìn thấy được, có kẹp, và an toàn khi máy chủ chết.

![Chỉ chạy khi lệnh còn tươi; im lặng là dừng]({{ site.imgurl }}/generated/teleop_states.png)

Log không chỉ vào ô STOP bằng một số đo thì checklist chưa xong.

## Lab

### An toàn

Chỉ chạy lại chuỗi trên sàn sau khi hàng trượt đã được sửa. Không thì đọc log giấy. Công tắc pin trong tầm tay nếu lốp chạm được sàn. Đừng ký robot chưa từng dừng bằng timeout. Đầu lithium trần thì dừng việc.

### BOM

| Món | Việc |
|------|------|
| `lab-notes.md` bài 01–05 | Bằng chứng |
| Robot, chỉ khi một hàng phải chạy lại | Lượt thử lại |
| Đồng hồ | Kiểm buck 5,0 V và điện áp pack nếu ảnh đã cũ |
| Checklist này | Bốn dòng bạn ký tắt |

### Các bước

1. Tìm ảnh đi dây: công tắc, chì, dây buộc, đất chung, dây motor trên vít, buck gần $$5{,}0~\mathrm{V}$$ trước khi gắn ESP32.
2. Ký tắt tiến, lùi, trái, phải chỉ ở hàng nào lời log khớp lệnh.
3. Tìm hàng timeout: máy gửi bị giết hoặc USB rút, MCU còn ăn buck, dừng trong $$0{,}5~\mathrm{s}$$. Thiếu hàng ấy thì chương chưa xong.
4. Tìm $$b$$, $$r$$, đoạn giao thức, và các điện áp. Ghi ngày chương 08 được bắt đầu, hoặc gọi tên một chỗ sửa đang chặn.
5. Lượt chạy lại dùng luật làn của bài 05. Một chỗ sửa, rồi cả chuỗi, rồi một log mới.

### Kết quả mong đợi

Một đoạn ký ngắn: bốn hướng đạt ngày nào, thời gian dừng, điện áp pack, $$b$$, $$r$$, và câu "chương 08 được bắt đầu" hoặc một chỗ sửa đang chặn. Bảng trống không tính.

### Lỗi thường gặp

| Bạn thấy | Thường là |
|----------|-----------|
| Đề mục chép đủ, ô trống | Chương chưa làm; điền từ một lượt thật |
| "Dừng" chỉ vì rút pin | Timeout chưa được thử; rút pin là nút giết, không phải hạn |
| Cả dây lẫn firmware đều "đã sửa" | Hai lần đảo triệt nhau; quay về một lần |
| Thiếu hình học | Chương 08 sẽ bịa bề rộng |
| PWM 80 bị viết thành $$0{,}2~\mathrm{m/s}$$ | Hiệu chuẩn giả; xóa trước PID |

## Mua ở Việt Nam / Where to buy in Vietnam

Chỉ mua dòng còn trống. Giá đổi. Khoảng 2026: khung 60.000–150.000 đồng, motor TT 25.000–45.000 một cái, TB6612 25.000–70.000, LM2596 10.000–25.000, pack 2S hoặc đế 18650 80.000–180.000, công tắc 8.000–20.000, đế chì và chì 2–3 A 10.000–25.000, ESP32 70.000–150.000. L298N thay TB6612 khi hết hàng. TP4056 không phải sạc 2S.

- L298N đã kiểm, khoảng 45.000 đồng: [hshop.vn/mach-dieu-khien-dong-co-dc-l298](https://hshop.vn/mach-dieu-khien-dong-co-dc-l298)
- [Hshop TB6612](https://hshop.vn/search?q=TB6612), [LM2596](https://hshop.vn/search?q=LM2596), [ESP32](https://hshop.vn/search?q=ESP32)
- [Shopee khung 2WD](https://shopee.vn/search?keyword=khung%20xe%202WD), [cầu chì](https://shopee.vn/search?keyword=c%E1%BA%A7u%20ch%C3%AC%202A), [pin 2S](https://shopee.vn/search?keyword=pin%202S%2018650)
- [Lazada TB6612](https://www.lazada.vn/catalog/?q=TB6612), [ESP32](https://www.lazada.vn/catalog/?q=ESP32)
- [Thế Giới IC LM2596](https://www.thegioiic.com/search?q=LM2596), [L298N](https://www.thegioiic.com/search?q=L298N)

## Bài tập

1. Log có một `V 80 80` thẳng, rồi xe còn lăn sau khi laptop ngủ. Dòng xong việc nào trượt, và trên hộp điều gì phải đúng trước khi đụng chương 08 hoặc 09?
2. Bốn hướng đã đạt. Ghi chú bên phải nói đã đảo dây và còn đảo dấu firmware "cho chắc". PWM dương bây giờ làm gì, và bạn gỡ cái nào?
3. Điện áp nghỉ $$8{,}20~\mathrm{V}$$, có tải $$6{,}90~\mathrm{V}$$ ở $$0{,}60~\mathrm{A}$$, ảnh có đầu cell hàn trần. Dòng nào trượt, và $$R$$ bằng bao nhiêu?
4. Một bạn đặt PWM 80 bằng $$0{,}20~\mathrm{m/s}$$ rồi nhân `V -60 60` cùng hệ số ấy, $$b = 0{,}15~\mathrm{m}$$. Họ tính nhầm $$\omega$$ bao nhiêu, và vì sao hệ số ấy bất hợp pháp?
5. Từ lệnh 60, xe mất $$1{,}2~\mathrm{s}$$ mới dừng sau khi máy gửi chết. Bước kéo 15 nấc mỗi $$20~\mathrm{ms}$$, hạn $$250~\mathrm{ms}$$. Thời gian dừng đáng lẽ là bao nhiêu?

### Gợi ý đáp án

1. Dòng "dừng khi máy chủ hết hạn" trượt. Trên hộp, `V 60 60` rồi giết máy gửi: cả hai lốp dừng trong $$0{,}5~\mathrm{s}$$ khi MCU còn ăn buck. Sau đó mới chạy lại làn. 2. Hai lần đảo triệt nhau, nên dương vẫn làm lốp ấy lùi. Gỡ một lần, bánh trên không. 3. Đầu trần làm trượt dòng pin, và $$R \approx 1{,}30/0{,}60 \approx 2{,}2~\Omega$$ làm trượt nguồn. Lắp đế hoặc pack BMS, công tắc, và chì 2–3 A. 4. Hệ số $$0{,}20/80 = 0{,}0025$$ m/s mỗi nấc biến trái thành $$-0{,}15$$ và phải thành $$+0{,}15$$, nên $$v = 0$$ và $$\omega = 0{,}30/0{,}15 = 2$$ rad/s. Hệ số chưa từng được đo. 5. Dừng đáng lẽ là $$250 + 4\times 20 = 330~\mathrm{ms}$$. Lăn $$1{,}2~\mathrm{s}$$ nghĩa là hạn thiếu hoặc dài hơn nhiều so với $$250~\mathrm{ms}$$. Đừng ký.

## Đọc thêm

- [geometry_msgs/Twist (Jazzy)](https://docs.ros.org/en/jazzy/p/geometry_msgs/interfaces/msg/Twist.html)
- [Mục lục gói geometry_msgs (Jazzy)](https://docs.ros.org/en/jazzy/p/geometry_msgs/)
- [Pololu TB6612FNG](https://www.pololu.com/product/713)
- [Datasheet L298 của ST](https://www.st.com/resource/en/datasheet/l298.pdf)
