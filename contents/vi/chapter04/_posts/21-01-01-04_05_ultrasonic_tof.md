---
layout: post
title: "Lab: siêu âm và đo khoảng cách ToF"
chapter: "04"
order: 5
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter04
lesson_type: required
draft: false
---

Thời lượng: **80–100 phút**. Đây là lab đo khoảng cách: một thước mét, một tấm bìa, và một bảng sai số. Bánh xe không lên bàn.

## Mục tiêu học

Bạn tính khoảng cách từ độ rộng xung echo bằng $$d = vt/2$$ với $$343~\mathrm{m/s}$$, và bằng lối tắt micro giây $$d_{\mathrm{cm}} \approx t_{\mu\mathrm{s}} \times 0{,}01715$$. Bạn hạ echo 5 V của HC-SR04 xuống khoảng 3,33 V trước khi nó chạm chân ESP32, và bạn nói được echo mất hút nghĩa là không biết, không phải 0 cm. Bạn giải thích vì sao hai board VL53L0X chưa sửa, cùng địa chỉ `0x29`, không sống chung một bus, và bạn điền bảng sai số 20 / 40 / 80 cm so với thước, hoặc một tờ dry-run vẫn chứa ví dụ 5,8 ms và cầu chia điện áp.

## Kiến thức cần có

Bài 04-02 đã nhận diện hai ống nhôm và cửa sổ đen nhỏ, kể cả điện áp và loại bus. Bài 04-01 là lần quét I2C bạn sẽ cần nếu trên bàn có VL53L0X. Chương 03 đo được độ rộng xung, hoặc ít nhất in được một số từ thư viện bạn đã đọc. Chương 01 là đồng hồ kẹp lên chân echo. Chưa cần chương động cơ, và bạn không nên cầm bánh xe trong lab này.

## Vì sao bài này quan trọng với Capstone A và ROS

Firmware teleop Chương 07 chỉ được phép chạy vì có thứ bảo nó dừng. Trên Capstone A, thứ đó là một lần so khoảng cách trong cùng vòng lặp với lệnh motor: quá gần, hoặc không có số đọc, thì PWM về không. Con số trong phép so đó sinh ra ở đây, cạnh thước mét, không sinh ra trong một node ROS.

Sau này cùng số đọc đó là một `sensor_msgs/Range`: `radiation_type` là siêu âm hoặc hồng ngoại, `min_range` và `max_range` lấy từ khoảng bạn thực sự tin, `range` tính bằng mét. Số 0 trong trường đó không được hiểu là “tường đang chạm cản” nếu code HC-SR04 dùng 0 cho timeout. Ghi ký hiệu đặc biệt đó ngay bây giờ. Hai VL53L0X thành hai topic khoảng cách chỉ sau khi XSHUT đã cho chúng hai địa chỉ. Camera không thay lab này. Robot phải dừng được trước khi nó nhìn.

![Thời gian echo đi và về, và số ToF đã là milimét ngay trong chip]({{ site.imgurl }}/generated/range_echo_tof.png)

## Âm thanh đi và về

Chùm của HC-SR04 đi tới bia rồi quay lại, nên khoảng cách là một nửa quãng đường:

$$
d = \frac{v t}{2}.
$$

Ở nhiệt độ phòng lấy $$v \approx 343~\mathrm{m/s}$$. Echo giữ mức cao trong $$5{,}8~\mathrm{ms} = 0{,}0058~\mathrm{s}$$ cho

$$
d = \frac{343 \times 0{,}0058}{2} = 343 \times 0{,}0029 = 0{,}995~\mathrm{m} \approx 99{,}5~\mathrm{cm}.
$$

Chia $$343 / 2$$ cho $$10^{6}$$ để làm việc bằng micro giây và centimét:

$$
d_{\mathrm{cm}} \approx t_{\mu\mathrm{s}} \times 0{,}01715.
$$

Kiểm cùng xung đó: $$5800 \times 0{,}01715 = 99{,}5~\mathrm{cm}$$. Một centimét tầm tương ứng khoảng $$58~\mu\mathrm{s}$$ echo. Timer jitter $$100~\mu\mathrm{s}$$ đã đẩy số đọc khoảng $$1{,}7~\mathrm{cm}$$. Đó là cỡ sai số đáng nhớ khi mốc 40 cm lệch một centimét và bạn đang muốn đổ lỗi cho thước.

Tốc độ âm tăng khoảng $$0{,}6~\mathrm{m/s}$$ mỗi độ C. Số 343 là số của 20 °C. Ở 30 °C, $$v \approx 349~\mathrm{m/s}$$, và công thức vẫn nhân 0,01715 sẽ đọc một bia 80 cm thật hơi ngắn. Bài tập cuối bắt bạn tính ngắn bao nhiêu. Trong lab này cứ dùng 343, và ghi nhiệt độ phòng cạnh bảng nếu bạn biết.

## HC-SR04, xung, và chân không được chạm

VCC là 5 V. Bạn kéo TRIG lên khoảng $$10~\mu\mathrm{s}$$. Module phát một chùm 40 kHz ngắn và kéo ECHO lên cho đến khi echo trở về. Trên board phổ biến, ECHO mức cao là 5 V. GPIO của ESP32 không phải ngõ vào 5 V. Cầu chia với $$1~\mathrm{k}\Omega$$ từ ECHO tới chân và $$2~\mathrm{k}\Omega$$ từ chân xuống mass đặt

$$
V_{\mathrm{pin}} = 5 \times \frac{2}{3} \approx 3{,}33~\mathrm{V}.
$$

Nón âm khoảng 15 độ. Ở 80 cm, bán kính vệt khoảng $$80 \tan 7{,}5^\circ \approx 10~\mathrm{cm}$$, nên khung cửa nằm trong vệt sẽ trả lời thay cho tấm bìa bạn đang nhắm. Vải mềm nuốt 40 kHz và echo không về. Góc tường phản xạ nhiều lần. Khoảng mù khoảng 2 cm. Số bạn sẽ tin trên robot này nằm dưới khoảng 1 m, dù tin đăng có nói 4 m. Bốn mét là tường cứng, phòng yên, và nguồn 5 V còn khỏe.

ECHO không lên thì thư viện thường trả 0. Số 0 đó nghĩa là “tôi không biết”, và cách dừng ở Chương 05 sẽ coi “không biết” là tắt motor. Đừng kẹp timeout thành 400 cm cho số trông hiền.

## VL53L0X: milimét, chip đã tính xong

VL53L0X đo thời gian bay của laser 940 nm ngay trên đế và đưa milimét qua I2C, địa chỉ mặc định `0x29`. Góc nhìn khoảng 25 độ. Tấm trắng đọc được cỡ 1,2–2 m; vải đen và kính dưới nắng tệ hơn. Nắng thêm photon mà chip không gửi. Kính trả về tấm kính, không phải hành lang phía sau. Đường thứ hai trên hình là cảm biến này: không có chân echo để bạn tự canh thời gian.

Hai board chưa sửa đều trả lời ở `0x29`. Chúng ACK đè lên nhau và lần quét thấy một địa chỉ hoặc một bus chết. Chân XSHUT để bạn giữ một chip ở trạng thái reset, gán địa chỉ mới cho chip kia, rồi thả chip đầu. Mua module thứ hai mà không dành một GPIO cho XSHUT thì chưa mua được tầm thứ hai.

## Lab: ba khoảng cách, một bia

### An toàn

Bìa cứng, không phải người, không phải cửa kính. Đừng nhìn vào lỗ VL53L0X và đừng đặt ống kính điện thoại hay kính lúp phía trước. Laser công suất thấp 940 nm là lý do để cư xử nhàm chán, không phải lý do để nhìn. VCC của HC-SR04 là 5 V từ nguồn chịu nổi dòng đó; đừng đổ 5 V ấy vào chân 3,3 V của ESP32. Bánh không thuộc bố trí này. Driver motor nếu đã nối thì để mất nguồn.

### BOM

| Món | Vai trò |
|------|---------|
| HC-SR04 | Echo bạn sẽ đo thời gian |
| 1 kΩ và 2 kΩ | Cầu chia trên ECHO |
| ESP32 hoặc Pico | TRIG ra, ECHO vào qua cầu chia |
| Thước mét và bìa cỡ A4 trở lên | Sự thật và bia |
| Mạch VL53L0X | Cột thứ hai, nếu có |
| `lab-notes.md` | Bảng sai số |

### Các bước

1. Dựng cầu chia trước khi ECHO chạm GPIO. Đo mức cao tại chân nếu bắt được xung, hoặc ít nhất đo điện trở phía dưới thực sự về GND.
2. TRIG nhận xung 10 µs. In thời gian echo theo micro giây và khoảng cách theo centimét với 0,01715. In cả hai, để thang sai hiện ra ngay.
3. Dán thước lên bàn. Dựng bìa ở 20 cm, rồi 40 cm, rồi 80 cm, đo tới mặt ống nhôm, không đo tới mép breadboard. Giữ yên. Ghi năm lần đọc và lấy lần ở giữa.
4. Lấy số cảm biến trừ số thước. Cột sai số có dấu mới là kết quả. Một chữ “khá gần” không tính.
5. Nếu có VL53L0X, cấp đúng điện áp logic mà mạch cho phép, xác nhận `0x29`, thêm một cột ở cùng ba mốc. Chưa có thì bảng siêu âm là cả lab. Dry-run khi hàng còn trên đường vẫn phải tính echo 5,8 ms (99,5 cm) và cầu chia (3,33 V) trên cùng trang với bảng để trống.
6. Thêm một bia: vải gấp ở 40 cm. Ghi siêu âm đọc thành gì. Dòng này được phép là “không có echo”.

### Kết quả mong đợi

Một bảng dạng này, điền số của bạn:

| Thước (cm) | Siêu âm (cm) | Sai số (cm) | ToF (cm), nếu có |
|-----------:|-------------:|------------:|-----------------:|
| 20 |  |  |  |
| 40 |  |  |  |
| 80 |  |  |  |

Trên bìa phẳng, HC-SR04 còn khỏe thường lệch vài centimét ở 40 cm và tệ hơn một chút ở 80 cm. Sai số giải thích được (nhắm, nón âm, vải, VCC sụt còn 4,6 V) vẫn qua. Thiếu một mốc thì không. Timeout in ra 0 phải ghi “timeout”, không ghi “cách tường 0,0 cm”.

### Lỗi thường gặp

| Bạn thấy | Thường là |
|----------|-----------|
| GPIO ấm, số đọc đứng cứng | ECHO 5 V, không cầu chia |
| Mốc 20 cm đọc khoảng 40 cm | Quên chia đôi |
| Nhảy số gần chân ghế | Nón 15 độ bắt vật gần hơn |
| Vải không đọc hoặc đọc gấp đôi | Hấp thụ, hoặc phản xạ yếu nhiều đường |
| Hai board VL53, một địa chỉ | Cả hai vẫn `0x29`; dùng XSHUT |
| Trong nhà mà lúc nào cũng 0 | Timeout, không phải va chạm. Đừng chạy theo số 0 đó |

## Mua ở Việt Nam / Where to buy in Vietnam

Module siêu âm là món Capstone A không nên khởi hành khi thiếu. Board ToF là cảm biến thứ hai đáng tiền nếu còn ngân sách, không phải món bắt buộc phải đợi. Giá thay đổi.

| Món | Từ khóa | Khoảng giá (VND) | Thay thế |
|------|---------|------------------|----------|
| HC-SR04 | `cảm biến siêu âm HC-SR04` | 15.000–40.000 | [Hshop HC-SR04](https://hshop.vn/cam-bien-sieu-am-srf04) từng niêm yết khoảng 20.000. US-100 chỉ thay được sau khi bạn đọc chân đó là GPIO hay UART. |
| VL53L0X | `VL53L0X ToF` | 35.000–90.000 | [Hshop VL53L0X](https://hshop.vn/cam-bien-khoang-cach-tof-laser-radar-vl53l0x). VL53L1X là thư viện khác và tầm xa hơn. |
| 1 kΩ, 2 kΩ | `điện trở 1k 2k` | 10.000–20.000 một vỉ | Đừng bỏ qua chỉ vì module “đã chạy một lần” |

- [Hshop: HC-SR04](https://hshop.vn/search?q=HC-SR04)
- [Shopee: VL53L0X](https://shopee.vn/search?keyword=VL53L0X)
- [Lazada: cảm biến siêu âm](https://www.lazada.vn/catalog/?q=cam%20bien%20sieu%20am%20HC-SR04)
- [Thế Giới IC: HC-SR04](https://www.thegioiic.com/search?q=HC-SR04)

## Bài tập

1. ECHO cao trong 5,8 ms. Tìm $$d$$ theo mét và theo centimét, với $$343~\mathrm{m/s}$$.
2. Mốc 40 cm cho echo $$2320~\mu\mathrm{s}$$. $$t \times 0{,}01715$$ báo bao nhiêu centimét?
3. ECHO lên 5 V và chân nhận là GPIO của ESP32. Không cầu chia thì chân chịu bao nhiêu vôn, và với 1 kΩ phía trên, 2 kΩ xuống mass thì bao nhiêu?
4. Hai VL53L0X mắc song song, không dùng XSHUT. Vì sao lần quét không ra hai cảm biến, và chân nào gỡ được?
5. Phòng 30 °C nên $$v \approx 349~\mathrm{m/s}$$. Khoảng cách thật 80 cm. Echo dài bao lâu, và firmware dùng hằng số 0,01715 cm/µs sẽ báo bao nhiêu?

### Gợi ý đáp án

1. $$d = 0{,}995~\mathrm{m} \approx 99{,}5~\mathrm{cm}$$; $$5800 \times 0{,}01715 = 99{,}5$$. 2. $$2320 \times 0{,}01715 \approx 39{,}8~\mathrm{cm}$$. 3. 5 V khi không chia; $$5 \times 2/3 \approx 3{,}33~\mathrm{V}$$ khi có cầu chia. 4. Cả hai xuất xưởng ở `0x29` và trả lời cùng lúc; giữ một con ở reset bằng XSHUT, đổi địa chỉ con kia, rồi thả. 5. $$t = 2 \times 0{,}80 / 349 \approx 4{,}58~\mathrm{ms} = 4585~\mu\mathrm{s}$$, và $$4585 \times 0{,}01715 \approx 78{,}6~\mathrm{cm}$$, ngắn khoảng 1,4 cm.

## Đọc thêm

- [Datasheet HC-SR04 (bản SparkFun)](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf) — độ rộng TRIG, echo, và nguồn 5 V.
- [Datasheet ST VL53L0X](https://www.st.com/resource/en/datasheet/vl53l0x.pdf) — đo bằng milimét, góc nhìn, và địa chỉ.
- [Mạch Pololu VL53L0X](https://www.pololu.com/product/2490) — XSHUT và mức logic, vẫn hữu ích khi bạn mua breakout khác.
- [`sensor_msgs/Range`](https://docs.ros.org/en/humble/p/sensor_msgs/msg/Range.html) — message Chương 09 sẽ xuất từ bảng lab này.
