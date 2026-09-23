---
layout: post
title: "Nhận diện module: HC-SR04, ToF, IMU, IR, encoder, camera"
chapter: "04"
order: 2
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter04
lesson_type: required
draft: false
---

Thời lượng: **60–80 phút**. Đây là bài nhận diện trên bàn. Bạn làm được với ảnh những module đang có, cộng một tab datasheet cho món chưa mua.

## Mục tiêu học

Bạn gọi tên module từ hình dáng và chữ trên chân trước khi nối dây, nêu được điện áp nuôi và loại bus (trig/echo, I2C, analog hay USB), và không đưa chân echo 5 V thẳng vào ESP32. Bạn lập một phiếu nhận diện để Capstone A dùng lại, nên phần đo khoảng cách và đếm bánh được chọn có chủ đích. Bạn cũng nói được món nào phải có trước Chương 07 và món nào để dành cho nhận thức ở Chương 11.

## Kiến thức cần có

Bài 04-01 (I2C, SPI, UART) và thói quen đọc pinout từ Chương 01. Một cái đồng hồ vạn năng. Không cần mọi module có mặt cùng lúc.

## Vì sao bài này quan trọng với Capstone A và ROS

Capstone A cần một cách biết robot sắp đâm tường, và một cách đếm vòng bánh nếu bạn muốn bài nghiệm thu hơn câu “nó có nhúc nhích”. HC-SR04 hoặc VL53L0X lo chuyện bức tường. Động cơ giảm tốc kèm encoder từ tính lo chuyện đếm. IMU không bắt buộc cho lần teleop đầu và sau này mới thành `sensor_msgs/Imu`. Camera là việc của Chương 11: nó ngốn băng thông USB và CPU mà ESP32 trần không có. Mua camera lúc robot còn chưa dừng khi mất lệnh là cách làm hết tiền.

![Phiếu nhận diện module cảm biến]({{ site.imgurl }}/generated/sensor_package_id.png)

## Mắt cần bắt được gì

Nhìn kim loại, cửa sổ quang, và số chân. Rồi đọc chữ in. Rồi tra điện áp. Đúng thứ tự đó. Một module “giống” HC-SR04 nhưng có năm chân có thể là RCWL-1601 hoặc US-100 có chế độ UART. Thư viện copy-dán không cứu được.

**HC-SR04.** Hai ống nhôm trên PCB nhỏ, bốn chân: VCC, TRIG, ECHO, GND. Nó cần 5 V. TRIG là xung vào khoảng 10 µs. ECHO là xung ra, độ rộng bằng thời gian đi và về, và trên module phổ biến xung đó là 5 V. GPIO của ESP32 không phải chân 5 V. Cầu chia (1 kΩ từ ECHO tới GPIO, 2 kΩ từ GPIO xuống mass) đưa 5 V xuống khoảng 3,3 V. Hai ống nhôm có nón âm rộng, cỡ 15 độ, nên khung cửa và tấm rèm không cho cùng một số.

**VL53L0X và họ hàng.** Cửa sổ đen rất nhỏ, thường trên breakout tím, chân VIN, GND, SCL, SDA, đôi khi thêm XSHUT và GPIO1. Hội thoại là I2C, địa chỉ mặc định `0x29`. Con số bạn đọc là milimét, chip đã tính sẵn. VIN của nhiều breakout chịu 3,3–5 V vì có ổn áp trên board; đường I2C vẫn phải khớp MCU. Hai board VL53L0X chưa sửa sẽ trùng địa chỉ và không trả lời đủ cả hai. Chân XSHUT để bạn bật từng con và gán địa chỉ mới.

**MPU-6050 / GY-521.** PCB phẳng nhỏ, thường màu xanh, chip có nắp kim loại, chân VCC, GND, SCL, SDA, XDA, XCL, AD0, INT. Địa chỉ I2C `0x68` hoặc `0x69` tùy AD0. Đây là gia tốc kế cộng con quay. Nó không đo khoảng cách. Người mới hay mua nhầm vì cả hai đều được gọi là “cảm biến robot”.

**Hồng ngoại phản xạ và vật cản.** Một LED trong và một phototransistor đen nằm cạnh nhau, ba chân: VCC, GND, và OUT hoặc AO. Board số nhảy mức khi phản xạ vượt ngưỡng chiết áp. Board analog (AO) cần chân ADC. Cảm biến dò line TCRT5000 thuộc họ này. Chúng không phải ToF laser, và chúng bão hòa dưới nắng gắt.

**Encoder bánh xe.** Hoặc đĩa có rãnh nằm giữa cặp quang trên trục motor, hoặc một viên từ nhỏ phía sau hộp số TT vàng với cảm biến Hall. Hai chân tín hiệu (A và B) nghĩa là quadrature và có chiều. Một chân tín hiệu chỉ cho tốc độ nếu bạn đã biết chiều từ driver. Đếm chân trước khi hứa đo odometry.

**Camera.** Cáp mềm bản rộng (FPC) cắm vào board lớn (ESP32-CAM, OV2640) hoặc cáp USB (webcam UVC). Thấy phích USB thì máy chủ là máy tính, không phải chân analog. ESP32-CAM là bộ não Capstone khá tệ: camera chiếm nhiều chân, ổn áp dễ sụt, và bạn vẫn nợ một driver motor. Để sau.

## Ví dụ tính tay: echo 5 V

Chân echo của HC-SR04 ở 5 V khi xung mức cao. Bạn dựng cầu chia với $$R_1 = 1~\mathrm{k}\Omega$$ từ ECHO tới chân ESP32 và $$R_2 = 2~\mathrm{k}\Omega$$ từ chân đó xuống mass. Điện áp tại chân là

$$
V_{pin} = 5 \times \frac{R_2}{R_1 + R_2} = 5 \times \frac{2}{3} \approx 3{,}33~\mathrm{V}.
$$

Mức đó nằm trong vùng ESP32 chịu được. Bỏ cầu chia “vì lần trước vẫn chạy” là cách biến một GPIO thành cục nóng. VL53L0X trên I2C không cần cầu chia này nếu breakout đã nói logic 3,3 V. Module khác, quy tắc khác. Ghi quy tắc đó lên phiếu, cạnh ảnh.

## Lab: phiếu nhận diện một trang

### An toàn

Nhận diện lúc chưa cấp nguồn. Khi có cấp nguồn, chỉ USB vào MCU. Không nối VCC 5 V của cảm biến vào chân 3,3 V của ESP32, và không nối ECHO vào GPIO khi chưa có cầu chia.

### BOM

| Món | Vai trò |
|-----|---------|
| Bất kỳ hai trong: HC-SR04, module VL53, GY-521, board IR, motor encoder, webcam | Thứ bạn sẽ mua thật |
| Camera điện thoại | Phiếu |
| Đồng hồ | Kiểm VCC sau khi cấp nguồn |
| Tab datasheet | Điện áp và bus |

### Các bước

1. Chưa cấp nguồn, chụp từng module sao cho đọc được chân.
2. Điền một dòng: tên, chữ chân nhìn thấy, bus đoán, điện áp đoán, “dùng cho Capstone ngay / để sau”.
3. Mở datasheet hoặc sơ đồ người bán và sửa dòng đó. Đánh dấu chỗ đoán sai.
4. Chỉ cấp nguồn cho module I2C 3,3 V như bài 04-01, hoặc dừng ở phiếu giấy nếu hàng còn đang giao.
5. Cất phiếu trong `lab-notes.md`. Chương 07 sẽ hỏi đến.

### Kết quả mong đợi

Ít nhất hai module đã được sửa đúng điện áp và bus. Một câu ghi HC-SR04 ECHO là 5 V và VL53L0X là I2C ở `0x29`. Một quyết định: đã chọn cảm biến khoảng cách, camera để sau.

### Lỗi thường gặp

| Nhầm | Hệ quả |
|------|--------|
| Cứ cửa sổ đen là IMU | Quét I2C một cảm biến khoảng cách, hoặc đòi đọc mét từ con quay |
| 5 V vào ESP32 | Chân nóng, kẹt input, hoặc chết GPIO |
| Hai board VL53, không tính XSHUT | Quét ra một địa chỉ hoặc không ra gì |
| Encoder một kênh | Không phân biệt tiến và lùi |
| Mua ESP32-CAM làm não Capstone | Chân motor và sụt áp đánh nhau với camera |

## Mua ở Việt Nam / Where to buy in Vietnam

Mua cảm biến khoảng cách và, nếu ví cho phép, motor TT đã kèm encoder. Để camera tới Chương 11.

| Món | Từ khóa | Khoảng giá (VND) | Thay thế |
|-----|---------|------------------|----------|
| HC-SR04 | `cảm biến siêu âm HC-SR04` | 15.000–40.000 | [Hshop HC-SR04](https://hshop.vn/cam-bien-sieu-am-srf04) từng niêm yết khoảng 20.000. US-100 chỉ thay khi bạn đọc rõ chế độ UART/GPIO của nó. |
| Module VL53L0X | `VL53L0X ToF` | 35.000–90.000 | [Hshop VL53L0X](https://hshop.vn/cam-bien-khoang-cach-tof-laser-radar-vl53l0x). VL53L1X xa hơn và khác thư viện. |
| GY-521 | `MPU6050 GY-521` | 35.000–90.000 | MPU6500 nếu code mẫu khớp. |
| IR vật cản hoặc TCRT5000 | `cảm biến hồng ngoại vật cản` | 8.000–25.000 | Hợp dò line, yếu nếu là cảm biến va chạm duy nhất |
| Motor TT + encoder | `động cơ TT encoder Hall` | 40.000–90.000 một cái | N20 hộp số kim loại kèm encoder nếu lỗ khung khớp; kiểm tra trục 3 mm hay 4 mm |
| Trở cầu chia | `điện trở 1k 2k` | 10.000–20.000 một thanh | Thế Giới IC cho điện trở rời |

Ô tìm kiếm:

- [Hshop, từ khóa HC-SR04](https://hshop.vn/search?q=HC-SR04)
- [Shopee, motor encoder](https://shopee.vn/search?keyword=dong%20co%20TT%20encoder)
- [Lazada, VL53L0X](https://www.lazada.vn/catalog/?q=VL53L0X)
- [Thế Giới IC](https://www.thegioiic.com/search?q=HC-SR04)

## Bài tập

1. Board có hai ống kim loại và chân VCC, TRIG, ECHO, GND. ECHO lên bao nhiêu vôn, và bạn thêm hai điện trở nào cho ESP32?
2. Board tím có cửa sổ đen và SCL/SDA. Họ nào, địa chỉ lần quét đầu thường là gì?
3. Bạn cần biết bánh trái quay tới hay quay lui. Một cảm biến Hall có đủ không? Phải mua gì?
4. Chia thành “trước Capstone A” và “sau khi robot đã teleop”: HC-SR04, camera USB, motor encoder, ESP32-CAM, VL53L0X.
5. Hai module VL53L0X đều nằm ở `0x29`. Chân nào gỡ rối, và lần quét trông thế nào khi bạn chưa dùng chân đó?

### Gợi ý đáp án

1. Khoảng 5 V; 1 kΩ và 2 kΩ như cầu chia ở trên, khoảng 3,3 V tại chân MCU. 2. ToF, thường `0x29`. 3. Không đủ; mua cặp quadrature A và B, hoặc chấp nhận chiều chỉ lấy từ lệnh motor và sẽ mất đoạn trôi bánh. 4. Trước: HC-SR04 hoặc VL53L0X, và encoder nếu muốn đếm. Sau: camera USB và ESP32-CAM. 5. XSHUT; lần quét chỉ ra một địa chỉ hoặc bus rối cho đến khi bạn cấp nguồn tách và gán lại.

## Đọc thêm

- [Datasheet HC-SR04 (bản SparkFun lưu)](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf)
- [Datasheet ST VL53L0X](https://www.st.com/resource/en/datasheet/vl53l0x.pdf)
- [Datasheet TDK MPU-6000/6050](https://invensense.tdk.com/wp-content/uploads/2015/02/MPU-6000-Datasheet1.pdf)
- [Ghi chú board Pololu VL53L0X](https://www.pololu.com/product/2490) — địa chỉ và mức logic, dùng được dù bạn mua breakout khác.
