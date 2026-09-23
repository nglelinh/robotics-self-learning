---
layout: post
title: "Teleop serial: thiết kế giao thức"
chapter: "07"
order: 3
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter07
lesson_type: required
draft: false
---

Bài 02 đã nói một số dương làm gì với từng lốp. Bài này đặt tên cho các byte mang hai số ấy. Bạn viết dòng. Vòng firmware là bài 04.

## Mục tiêu học

1. Đặc tả giao thức chữ UTF-8, kết thúc bằng xuống dòng, 115200 8N1: `V <trái> <phải>` với hai số nguyên, và `S` là dừng khẩn.
2. Nêu khoảng kẹp firmware sẽ áp, $$-180$$ đến $$+180$$, và vì sao lúc học không dùng hết thang $$0$$–$$255$$.
3. Bắt máy chủ gửi lại ít nhất mỗi $$200~\mathrm{ms}$$, hạn firmware $$250~\mathrm{ms}$$, để im lặng thành PWM 0 chứ không giữ lệnh cũ.
4. Bỏ cả dòng sai dạng, và với năm khung cụ thể chỉ ra chuyển động nào dưới quy ước dấu bài 02.

## Kiến thức cần có

Bài 07-01 là khung đã có nguồn và đất chung. Bài 07-02 là bảng dấu đã viết: lệnh dương, cả hai lốp về mũi, chỉ sửa bằng một cách đảo. Chương 05 là cách những dấu ấy thành điện áp. Hình học chương 06 vẫn là

$$
v = \frac{v_r + v_l}{2}, \qquad \omega = \frac{v_r - v_l}{b},
$$

với $$b$$ là bề rộng bạn đã đo (ví dụ $$b = 0{,}15~\mathrm{m}$$, $$r = 31{,}2~\mathrm{mm}$$). Bạn mở được serial monitor. Bài 04 mới viết parser. Bạn chưa publish topic ROS.

## Vì sao bài này quan trọng với Capstone A và ROS

Teleop là cuộc nói chuyện khép đầu tiên với hai motor. Chữ là cuộc nói chuyện đọc được trên serial monitor; nhị phân để sau, khi dòng đã chán và đúng. Cùng ý ấy sau này là `geometry_msgs/Twist`: `linear.x` là tốc độ tiến, `angular.z` là yaw, và driver tách chúng bằng hai phương trình trên. Trong chương này hai số nguyên là nấc PWM, không phải m/s. Chương 08 mới hiệu chuẩn. Viết "`V 80 80` nghĩa là $$0{,}2~\mathrm{m/s}$$" là hiệu chuẩn giả.

![Dòng `V` hợp lệ thì chạy; quá 250 ms hoặc dòng `S` thì dừng]({{ site.imgurl }}/generated/teleop_states.png)

Đọc hình như một hợp đồng. IDLE là motor tắt, đang chờ. Dòng `V` hợp lệ vào RUN và làm mới hạn. STOP là tuổi lệnh quá $$250~\mathrm{ms}$$, hoặc dòng `S`. PWM về 0. Một `V` hợp lệ mới có thể trở lại RUN. Im lặng không được để duty cuối cùng chạy tiếp.

## Byte, khoảng kẹp, và hạn

Cổng là 115200 baud, 8 bit dữ liệu, không parity, 1 stop. Mỗi dòng là chữ UTF-8 kết thúc bằng `\n`. `\r` đứng trước newline là nhiễu parser có thể bỏ; nó không phải lệnh thứ hai.

`V <trái> <phải>` mang hai số nguyên. Firmware bài sau kẹp từng số vào $$-180..180$$. Trần này có chủ đích. Thang 255 trên pack 2S mới là cú nhảy chưa đáng, và những vòng đầu của bài 02 sống ở 60–80. Một trăm tám mươi nấc là

$$
D = \frac{180}{255} \approx 0{,}706
$$

nguồn cầu, đủ cho thử sàn và chưa phải cú đạp vào tường. `S` đưa cả hai target về 0 ngay, như dừng khẩn. `V 0 0` cũng là dừng, nhưng là lệnh thường chứ không phải hoảng.

Máy chủ gửi dòng mới ít nhất mỗi $$200~\mathrm{ms}$$ khi còn muốn chuyển động. Firmware coi $$250~\mathrm{ms}$$ không có `V` hoặc `S` hợp lệ là máy chủ chết và ép target về 0. Khoảng $$50~\mathrm{ms}$$ chịu một gói USB đến muộn, không chịu một laptop đã ngủ. Im lặng nghĩa là PWM 0. Duty còn dính ở 80 sau khi cáp im là hạn bị hỏng.

Dòng không khớp ngữ pháp thì bỏ. Target hợp lệ trước đó giữ đến khi hết hạn, và rác không được thành một vòng quay. `V 80` thiếu một bánh. `V 80 foo` không phải số 0 bên phải. Chữ cái là `V`, không phải `v`.

## Năm khung, một quy ước dấu

Dương trên một bánh là tiến, hướng mũi của bài 02. Phải nhanh hơn trái là yaw trái, cùng dấu chương 06, vì

$$
\omega = \frac{v_r - v_l}{b}
$$

dương khi $$v_r > v_l$$. Các ký hiệu ấy là tốc độ. Các số trong khung dưới là nấc PWM. Dấu khớp. Đơn vị thì không.

| Dòng | PWM trái | PWM phải | Bạn đang xin |
|------|----------|----------|----------------|
| `V 80 80` | $$+80$$ | $$+80$$ | Cả hai tiến, thẳng |
| `V -80 -80` | $$-80$$ | $$-80$$ | Cả hai lùi |
| `V -60 60` | $$-60$$ | $$+60$$ | Quay trái (phải tiến, trái lùi) |
| `V 0 0` | $$0$$ | $$0$$ | Dừng |
| `S` | target 0 | target 0 | Dừng khẩn |

`V 60 -60` là yaw ngược lại, quay phải, khi bảng dấu trung thực. Quên một lần đảo từ bài 02 thì các khung này quay sai chiều. Sửa ở bài ấy, một lần.

Đếm `V -60 60\n`: `V`, cách, `-`, `6`, `0`, cách, `6`, `0`, xuống dòng, chín byte. Ở 115200 8N1 mỗi byte là 10 lần bit:

$$
t \approx \frac{9 \times 10}{115200} \approx 0{,}78~\mathrm{ms}.
$$

Thời gian trên dây dưới một mili giây. Nhịp $$200~\mathrm{ms}$$ tồn tại để firmware biết máy chủ chết. Nhị phân không làm UART thành nút thắt, và bạn mất khả năng gõ `S`.

Đừng giả bộ công thức tốc độ thân đã được đo. Ép PWM 80 thành $$0{,}20~\mathrm{m/s}$$ trên cả hai bánh thì

$$
v = \frac{0{,}20+0{,}20}{2} = 0{,}20~\mathrm{m/s}, \qquad \omega = 0,
$$

phép tính gọn và vật lý bị bịa. Chương 08 có thể bấm giờ một mét đo được rồi mới tuyên bố tốc độ. Trước đó, `V 80 80` nghĩa là tiến theo bảng dấu, ở 80 nấc.

## Lab

### An toàn

Bạn đang gõ, không đang lái. Nếu ESP32 còn sketch cũ và dây motor còn gắn, ngắt công tắc pin trước khi mở serial monitor. Sản phẩm của bài là năm dòng. Bài 04 mới là sketch đầu tiên hành động, và bánh phải ở trên không.

### BOM

| Món | Việc |
|------|------|
| `lab-notes.md` hoặc serial monitor | Nơi năm khung nằm |
| Bảng dấu bài 07-02 | Nghĩa của dương |
| ESP32 tùy chọn, USB, không VM | Để thấy ký tự vọng |
| Máy tính | Kiểm tra thời gian 9 byte |

### Các bước

1. Ghi dòng cổng: 115200 8N1, UTF-8, kết thúc newline, kẹp $$-180..180$$, chu kỳ máy chủ $$200~\mathrm{ms}$$, hạn firmware $$250~\mathrm{ms}$$.
2. Dưới bảng dấu, viết năm khung: `V 80 80`, `V -80 -80`, `V -60 60`, `V 0 0`, `S`. Cạnh mỗi khung: thẳng, lùi, quay trái, dừng, dừng khẩn.
3. Bịa hai dòng cấm, ví dụ `V 80` và `V 80 foo`. Cạnh mỗi dòng viết "bỏ, không quay một bánh".
4. Nếu mở monitor, gõ năm dòng hợp lệ và đọc lại được. Không bật driver.
5. Tính thời gian truyền `V -60 60\n` như ví dụ, để cạnh luật $$200~\mathrm{ms}$$ cho hai thang thời gian không lẫn.

### Kết quả mong đợi

Ghi chú có năm khung, câu "dương là tiến trên cả hai bánh", khoảng kẹp, cả hai mốc thời gian ($$200~\mathrm{ms}$$ máy chủ, $$250~\mathrm{ms}$$ firmware), và một câu rõ rằng nấc PWM không phải mét trên giây. Ảnh monitor là tùy chọn. Robot chạy không phải kết quả của bài này.

### Lỗi thường gặp

| Bạn thấy | Thường là |
|----------|-----------|
| `V -60 60` bị mô tả là quay phải | Quy ước dấu bị lật; phải nhanh hơn là yaw trái |
| Một số được nhận thành chỉ bánh trái | Ngữ pháp bị áp một nửa; bỏ cả dòng |
| Hạn ghi 2 s "cho an toàn" | Máy ngủ sẽ còn kéo xe vài giây; dùng $$250~\mathrm{ms}$$ |
| `V 80 80` dán nhãn $$0{,}2~\mathrm{m/s}$$ | Hiệu chuẩn giả; chương 08 chưa tới |
| Chép struct nhị phân từ blog | Không gõ được, và không thấy nó hỏng |

## Mua ở Việt Nam / Where to buy in Vietnam

Bài này không thêm linh kiện bắt buộc. Nếu vẫn chưa có ESP32 để gõ thử, devkit là chỗ thiếu. Giá đổi. Khoảng 2026: ESP32 devkit 70.000–150.000 đồng. Board CP2102 hoặc CH340 đều được. Pico chỉ thay khi bạn đã viết lại lệnh LEDC của bài 04; sketch bài ấy là Arduino-ESP32. Đừng mua thêm driver để "giao thức nhanh hơn".

- L298N đã kiểm, khoảng 45.000 đồng, chỉ khi vẫn thiếu cầu: [hshop.vn/mach-dieu-khien-dong-co-dc-l298](https://hshop.vn/mach-dieu-khien-dong-co-dc-l298)
- [Hshop ESP32](https://hshop.vn/search?q=ESP32)
- [Shopee ESP32](https://shopee.vn/search?keyword=ESP32%20devkit)
- [Lazada ESP32](https://www.lazada.vn/catalog/?q=ESP32)
- [Thế Giới IC ESP32](https://www.thegioiic.com/search?q=ESP32)

## Bài tập

1. `V -60 60\n` có bao nhiêu byte, và khung ấy dài bao lâu ở 115200 8N1?
2. Dòng hợp lệ cuối ở $$t = 0$$. Laptop ngủ. Firmware phải ép target về 0 lúc nào, và vì sao máy chủ phải nói mỗi $$200~\mathrm{ms}$$?
3. Monitor nhận `V 80` rồi `V 200 -90`. Dòng nào bất hợp lệ, và bài 04 kẹp dòng hợp lệ thành gì?
4. Vì sao `V -60 60` là quay trái? Với $$b = 0{,}15~\mathrm{m}$$ chỉ để kiểm dấu, $$(\mathrm{phải} - \mathrm{trái})$$ dương hay âm, và vì sao kết quả vẫn chưa phải rad/s?
5. Một người gói hai số thành hai `int16` "cho nhanh". Mất gì trên serial monitor, và $$0{,}78~\mathrm{ms}$$ có biện hộ cho việc đó không?

### Gợi ý đáp án

1. Chín byte (`V`, cách, `-`, `6`, `0`, cách, `6`, `0`, `\n`). Thời gian $$\approx 9 \times 10 / 115200 \approx 0{,}78~\mathrm{ms}$$. 2. Target về 0 tại $$250~\mathrm{ms}$$. Chu kỳ $$200~\mathrm{ms}$$ chừa khoảng $$50~\mathrm{ms}$$ để máy chủ còn sống nhưng trễ không bị cắt. 3. `V 80` bất hợp lệ và bị bỏ. `V 200 -90` hợp lệ, sẽ bị kẹp thành $$180$$ và $$-90$$. 4. Trái $$-60$$, phải $$+60$$: lốp phải tiến, lốp trái lùi, mũi quay trái. Hiệu $$(\mathrm{phải}-\mathrm{trái})$$ dương, cùng dấu $$\omega$$ chương 06, nhưng cả hai số là nấc PWM. Chia cho $$b$$ không tạo ra rad/s. 5. Mất khả năng nhìn và gõ lệnh. Khung chữ đã dưới $$1~\mathrm{ms}$$, rất nhỏ so với nhịp $$200~\mathrm{ms}$$, nên nhị phân không sửa được chuyện máy chủ còn sống hay không.

## Đọc thêm

- [Arduino `Serial`](https://www.arduino.cc/reference/en/language/functions/communication/serial/)
- [pySerial, phần mở đầu](https://pyserial.readthedocs.io/en/latest/shortintro.html)
- [geometry_msgs/Twist (Jazzy)](https://docs.ros.org/en/jazzy/p/geometry_msgs/interfaces/msg/Twist.html)
- [Mục lục gói geometry_msgs (Jazzy)](https://docs.ros.org/en/jazzy/p/geometry_msgs/)
