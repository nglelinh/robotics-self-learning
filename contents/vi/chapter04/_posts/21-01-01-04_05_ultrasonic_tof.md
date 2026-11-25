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

Thời lượng: **80–100 phút**. Đây là bài thực hành đo khoảng cách với thước mét, tấm bìa phẳng và bảng đánh giá sai số; không gắn bánh xe trong bài này.

Dơi bay trong hang tối bằng sóng siêu âm, còn những chiếc robot tự hành hiện đại lại chiếu những xung tia hồng ngoại siêu ngắn rồi bấm đồng hồ đo thời gian ánh sáng dội ngược về — đó là hai gương mặt kinh điển của nguyên lý **Time-of-Flight (ToF)**: đo khoảng cách bằng cách đo *thời gian bay đi và về* của một làn sóng. Dù cùng dùng đúng một công thức $$d = \frac{v \cdot t}{2}$$, sự chênh lệch gần một triệu lần giữa tốc độ âm thanh ($$343\text{ m/s}$$) và tốc độ ánh sáng ($$3 \times 10^8\text{ m/s}$$) tạo ra hai thế giới cảm biến hoàn toàn khác nhau về độ rộng chùm tia, tần số lấy mẫu và dạng lỗi vật lý.

## Kiến thức cần nhớ: Vật lý truyền sóng trong đo khoảng cách robot

### 1. Siêu âm (HC-SR04) — nón sóng rộng, phản xạ gương và ảnh hưởng nhiệt độ
Cảm biến siêu âm phát chùm sóng $$40\text{ kHz}$$ mở rộng theo hình nón góc khoảng $$15^\circ\text{–}30^\circ$$. Ưu điểm là rẻ và phát hiện tốt cả kính trong suốt; nhưng nhược điểm chí mạng là **phản xạ gương (specular reflection)**: nếu sóng đập xiên góc vào tường phẳng nhẵn, sóng nảy đi nơi khác không quay về đầu thu, khiến robot tưởng phía trước trống không! Ngoài ra, tốc độ âm thanh phụ thuộc nhiệt độ không khí theo $$v(T) \approx 331{,}3 + 0{,}606\,T\;(^\circ\text{C})$$.

### 2. Quang học ToF (VL53L0X / VL53L1X) — tia laser hẹp và bộ đếm nano-giây
Cảm biến ToF hồng ngoại dùng diode phát VCSEL (940 nm) chiếu một chùm sáng hẹp kết hợp mảng diode đơn photon (SPAD) đo thời gian bay ở mức **pico-giây đến nano-giây**. Nhờ tia hẹp, nó đo cực sắc nét qua khe cửa hẹp và không bị nhiễu chéo (crosstalk) giữa các cảm biến cạnh nhau như siêu âm, nhưng lại bị suy yếu dưới ánh nắng mặt trời gắt hoặc bề mặt đen hấp thụ hồng ngoại.

### 3. Chu kỳ đo tối đa và lọc nhiễu ngoại lai (Median Filter)
Với siêu âm, phải chờ tiếng vang dội xong (thường tối thiểu $$30\text{–}60\text{ ms}$$ mỗi lần bắn) để tránh thu nhầm tiếng vang của xung trước đó (*ghost echo*). Trong cả hai loại cảm biến, một **bộ lọc trung vị (median filter)** 3–5 mẫu luôn đánh bại trung bình cộng vì nó vứt sạch các cú đo lỗi đột ngột về `0` hoặc `max_range`.

### Giải thích: Cầm tay tính khoảng cách Siêu âm vs. Quang học ToF và sai số nhiệt độ

Xét một vật cản đặt cách robot đúng **$$d = 20{,}0\text{ cm} = 0{,}200\text{ m}$$**:

1. **Cảm biến siêu âm HC-SR04 ở nhiệt độ phòng $$20^\circ\text{C}$$ ($$v = 343\text{ m/s}$$):**
   Thời gian xung `ECHO` đo được (đi và về tổng $$0{,}400\text{ m}$$):
   $$t_{\text{echo}} = \frac{2d}{v} = \frac{0{,}400}{343} \approx 1{,}166 \times 10^{-3}\text{ s} = 1\,166\,\mu\text{s}.$$
   Kiểm tra ngược: $$d = \frac{343 \times 1\,166 \times 10^{-6}}{2} \approx 0{,}200\text{ m}$$.

2. **Điều gì xảy ra nếu robot chạy ngoài sân nắng nóng $$40^\circ\text{C}$$ nhưng code vẫn gán cứng $$v = 343\text{ m/s}$$?**
   Ở $$40^\circ\text{C}$$, tốc độ âm thanh thực là $$v(40) \approx 331{,}3 + 0{,}606 \times 40 = 355{,}5\text{ m/s}$$. Sóng bay nhanh hơn nên xung về sớm hơn:
   $$t_{\text{thực}} = \frac{0{,}400}{355{,}5} \approx 1\,125\,\mu\text{s}.$$
   Code gán cứng $$343\text{ m/s}$$ sẽ tính nhầm khoảng cách thành $$\frac{343 \times 1\,125 \times 10^{-6}}{2} \approx 19{,}3\text{ cm}$$ (lệch $$-3{,}5\%$$!).

3. **So sánh với cảm biến laser ToF (VL53L0X) ở cùng khoảng cách $$20{,}0\text{ cm}$$ ($$c = 3 \times 10^8\text{ m/s}$$):**
   $$t_{\text{ánh sáng}} = \frac{0{,}400}{3 \times 10^8} \approx 1{,}33 \times 10^{-9}\text{ s} = 1{,}33\text{ nano-giây!}$$
   Con số $$1{,}33\text{ ns}$$ giải thích vì sao bạn không bao giờ đo ToF quang học bằng hàm `pulseIn()` trên vi điều khiển mà phải dùng chip chuyên dụng có bộ đếm thời gian lượng tử bên trong!

## Mục tiêu học

Sau bài này, bạn tính được khoảng cách từ độ rộng xung Echo theo công thức $$d = vt/2$$ với vận tốc âm $$343~\mathrm{m/s}$$, cũng như công thức rút gọn theo micro giây $$d_{\mathrm{cm}} \approx t_{\mu\mathrm{s}} \times 0{,}01715$$. Bạn biết hạ mức Echo 5 V của HC-SR04 xuống khoảng 3,33 V trước khi đưa vào ESP32 và hiểu rõ việc mất tín hiệu Echo (timeout) nghĩa là không xác định được khoảng cách chứ không phải 0 cm. Bạn giải thích được vì sao hai module VL53L0X mặc định (cùng địa chỉ `0x29`) không thể hoạt động song song nếu chưa đổi địa chỉ, đồng thời hoàn thành bảng sai số tại ba mốc 20 / 40 / 80 cm so với thước đo (hoặc bản chuẩn bị dry-run kèm phép tính 5,8 ms và cầu chia áp).

## Kiến thức cần có

Bạn đã nhận diện được HC-SR04 và VL53L0X ở Bài 04-02, biết quét địa chỉ I2C từ Bài 04-01 (nếu có VL53L0X), biết đo độ rộng xung hoặc đọc thư viện từ Chương 03 và có đồng hồ vạn năng để kiểm tra điện áp chân Echo. Chưa cần động cơ hay mạch cầu H.

## Vì sao bài này quan trọng với Capstone A và ROS

Firmware teleop ở Chương 07 chỉ an toàn khi có điều kiện tự dừng: trong cùng vòng lặp điều khiển động cơ, nếu khoảng cách quá gần hoặc không đọc được tín hiệu hợp lệ, hệ thống phải đưa PWM về 0. Ngưỡng dừng đó được kiểm chứng trực tiếp bằng thước đo trong bài này.

Ở các chương ROS 2 sau này, kết quả đo sẽ được xuất thành bản tin `sensor_msgs/Range` với loại bức xạ (`radiation_type`: siêu âm hoặc hồng ngoại), giới hạn tin cậy `min_range`, `max_range` và giá trị `range` tính bằng mét. Không được để giá trị 0 của trạng thái timeout bị hiểu nhầm thành "khoảng cách 0 cm"; cần quy ước ký hiệu lỗi rõ ràng ngay từ bây giờ. Nếu dùng hai cảm biến VL53L0X, phải dùng chân `XSHUT` tách địa chỉ trước khi xuất thành hai topic riêng biệt.

![Thời gian echo đi và về, và số ToF đã là milimét ngay trong chip]({{ site.imgurl }}/generated/range_echo_tof.png)

## Thời gian bay của sóng âm

Chùm sóng siêu âm của HC-SR04 đi từ đầu phát đến vật cản rồi phản xạ ngược về đầu thu, nên khoảng cách bằng một nửa tổng quãng đường truyền:

$$
d = \frac{v t}{2}.
$$

Ở nhiệt độ phòng ($20\,^\circ\mathrm{C}$), lấy $$v \approx 343~\mathrm{m/s}$$. Nếu xung Echo ở mức cao trong $$5{,}8~\mathrm{ms} = 0{,}0058~\mathrm{s}$$, khoảng cách là:

$$
d = \frac{343 \times 0{,}0058}{2} = 343 \times 0{,}0029 = 0{,}995~\mathrm{m} \approx 99{,}5~\mathrm{cm}.
$$

Quy đổi sang đơn vị centimét và micro giây (chia $$343 / 2$$ cho $$10^{4}$$ hay chia mét cho $$10^{6}$$ rồi đổi ra cm):

$$
d_{\mathrm{cm}} \approx t_{\mu\mathrm{s}} \times 0{,}01715.
$$

Kiểm tra lại với cùng xung trên: $$5800 \times 0{,}01715 = 99{,}5~\mathrm{cm}$$. Mỗi 1 cm tương ứng khoảng $$58~\mu\mathrm{s}$$ độ rộng xung; do đó sai lệch định thời (jitter) cỡ $$100~\mu\mathrm{s}$$ đã làm kết quả lệch khoảng $$1{,}7~\mathrm{cm}$$.

Vận tốc âm trong không khí tăng khoảng $$0{,}6~\mathrm{m/s}$$ cho mỗi độ C. Ở $30\,^\circ\mathrm{C}$, $$v \approx 349~\mathrm{m/s}$$, nên nếu firmware vẫn cố định hệ số 0,01715 thì số đo sẽ ngắn hơn thực tế một chút. Trong bài lab này cứ dùng 343 m/s và ghi chú thêm nhiệt độ phòng cạnh bảng nếu biết.

## HC-SR04: xung kích, góc mở và hạ áp Echo

Module cấp nguồn `VCC = 5 V`. Khi tạo xung kích mức cao khoảng $$10~\mu\mathrm{s}$$ ở chân `TRIG`, module phát chùm sóng 40 kHz và giữ chân `ECHO` ở mức cao cho tới khi nhận sóng phản hồi. Trên bản phổ biến, mức cao của `ECHO` là 5 V, cần hạ áp qua cầu chia $$1~\mathrm{k}\Omega$$ (từ `ECHO` tới GPIO) và $$2~\mathrm{k}\Omega$$ (từ GPIO xuống mass):

$$
V_{\mathrm{pin}} = 5 \times \frac{2}{3} \approx 3{,}33~\mathrm{V}.
$$

Chùm sóng âm có góc mở khoảng $15^\circ$: tại khoảng cách 80 cm, bán kính vùng quét đã đạt $$80 \tan 7{,}5^\circ \approx 10~\mathrm{cm}$$, nên các vật gần bên như chân ghế hay khung cửa có thể phản xạ trước tấm bìa mục tiêu. Bề mặt vải mềm hấp thụ sóng 40 kHz khiến không có tín hiệu phản hồi, còn góc tường có thể gây phản xạ nhiều lần. Khoảng mù tối thiểu khoảng 2 cm. Dù thông số quảng cáo ghi tới 4 m (trong điều kiện tường cứng, phòng yên tĩnh và nguồn 5 V ổn định), trên robot thực tế chỉ nên tin cậy vùng đo dưới khoảng 1 m.

Khi quá thời gian chờ (timeout) mà không nhận được xung phản hồi, nhiều thư viện trả về giá trị 0. Giá trị 0 này mang nghĩa "không xác định được khoảng cách" — logic an toàn phải coi đó là trạng thái dừng động cơ chứ không gán bừa thành 400 cm.

## VL53L0X: đo trực tiếp theo milimét qua I2C

VL53L0X đo thời gian bay của tia laser hồng ngoại 940 nm ngay bên trong cảm biến và trả kết quả theo milimét qua bus I2C tại địa chỉ mặc định `0x29`. Góc nhìn khoảng $25^\circ$; trên bề mặt trắng có thể đo được khoảng 1,2–2 m, nhưng hiệu năng giảm rõ trên vật liệu màu đen, mặt kính hoặc dưới ánh nắng mạnh (vì ánh sáng mặt trời chứa bức xạ hồng ngoại gây nhiễu).

Hai module VL53L0X mặc định đều dùng địa chỉ `0x29` nên sẽ xung đột nếu nối song song trực tiếp. Cần dành riêng một chân GPIO nối vào `XSHUT` để giữ một cảm biến ở trạng thái reset trong lúc đổi địa chỉ I2C cho cảm biến còn lại, sau đó mới bật lại cảm biến thứ nhất.

## Lab: đo kiểm tại ba mốc khoảng cách

### An toàn

Chỉ dùng tấm bìa cứng làm vật cản, không hướng vào người hay cửa kính. Dù VL53L0X dùng laser 940 nm công suất thấp, vẫn tuân thủ nguyên tắc an toàn: không nhìn trực tiếp vào lỗ phát và không đặt ống kính hay kính lúp chắn sát phía trước. Cấp nguồn 5 V đúng chuẩn cho HC-SR04, tuyệt đối không để 5 V chạm vào đường 3,3 V của ESP32. Không cấp nguồn cho động cơ trong bài thực hành này.

### BOM

| Món | Vai trò |
|------|---------|
| HC-SR04 | Cảm biến siêu âm đo thời gian Echo |
| Điện trở 1 kΩ và 2 kΩ | Cầu chia áp bảo vệ chân GPIO |
| ESP32 hoặc Pico | Xuất `TRIG`, đọc `ECHO` qua cầu chia |
| Thước mét và tấm bìa cứng cỡ A4 trở lên | Mốc chuẩn và bia phản xạ |
| Module VL53L0X | Cột đo đối chiếu (nếu có) |
| `lab-notes.md` | Bảng ghi sai số |

### Các bước

1. Lắp hoàn chỉnh cầu chia áp trước khi nối chân `ECHO` vào GPIO; kiểm tra chắc chắn điện trở 2 kΩ nối đúng về `GND`.
2. Xuất xung `TRIG` 10 µs và in đồng thời cả độ rộng xung theo micro giây lẫn khoảng cách tính bằng hệ số 0,01715 để dễ phát hiện lỗi quy đổi.
3. Cố định thước mét trên bàn, lần lượt đặt tấm bìa vuông góc tại 20 cm, 40 cm và 80 cm (đo tính từ mặt đầu thu phát siêu âm). Tại mỗi mốc, ghi 5 lần đọc liên tiếp và lấy giá trị trung vị.
4. Tính cột sai số có dấu (số cảm biến trừ số thước). Ghi số cụ thể, không mô tả chung chung.
5. Nếu có VL53L0X, xác nhận địa chỉ `0x29` và bổ sung cột đo ToF tại cùng ba mốc. Nếu linh kiện chưa giao tới, thực hiện bản dry-run gồm bảng để trống kèm hai phép tính tay: Echo 5,8 ms (99,5 cm) và cầu chia áp (3,33 V).
6. Đặt thêm một tấm vải gấp ở mốc 40 cm và ghi nhận kết quả siêu âm (có thể ghi "không có echo" nếu bị hấp thụ).

### Kết quả mong đợi

Điền đầy đủ bảng theo mẫu sau vào `lab-notes.md`:

| Thước (cm) | Siêu âm (cm) | Sai số (cm) | ToF (cm), nếu có |
|-----------:|-------------:|------------:|-----------------:|
| 20 |  |  |  |
| 40 |  |  |  |
| 80 |  |  |  |

Trên tấm bìa phẳng, HC-SR04 hoạt động tốt thường sai lệch vài centimét ở mốc 40 cm và tăng nhẹ ở mốc 80 cm. Các trường hợp timeout trả về 0 phải ghi rõ là `timeout`, không ghi `0,0 cm`.

### Lỗi thường gặp

| Hiện tượng | Nguyên nhân thường gặp |
|------------|------------------------|
| Chân GPIO nóng, số đọc treo cứng | Đưa thẳng `ECHO` 5 V không qua cầu chia áp |
| Mốc 20 cm đọc ra khoảng 40 cm | Quên chia đôi thời gian đi và về |
| Số đo nhảy bất thường gần đồ vật | Chùm sóng $15^\circ$ bắt phải vật cản gần hơn ở bên cạnh |
| Đo vải không ra số hoặc sai gấp đôi | Sóng bị hấp thụ hoặc phản xạ đa đường yếu |
| Hai cảm biến VL53L0X chỉ hiện một địa chỉ | Trùng địa chỉ `0x29`, chưa dùng chân `XSHUT` |
| Luôn báo 0 khi đo trong phòng | Trạng thái timeout, không phải vật cản chạm sát |

## Mua ở Việt Nam

Cảm biến siêu âm HC-SR04 là lựa chọn tối thiểu cần có trước Capstone A; VL53L0X là lựa chọn bổ sung hữu ích nếu ngân sách cho phép.

| Món | Từ khóa | Khoảng giá (VND) | Thay thế |
|------|---------|------------------|----------|
| HC-SR04 | `cảm biến siêu âm HC-SR04` | 15.000–40.000 | [Hshop HC-SR04](https://hshop.vn/cam-bien-sieu-am-srf04) từng niêm yết khoảng 20.000. Chỉ thay bằng US-100 khi đọc rõ chế độ GPIO/UART. |
| VL53L0X | `VL53L0X ToF` | 35.000–90.000 | [Hshop VL53L0X](https://hshop.vn/cam-bien-khoang-cach-tof-laser-radar-vl53l0x). Lưu ý VL53L1X dùng thư viện khác. |
| 1 kΩ, 2 kΩ | `điện trở 1k 2k` | 10.000–20.000 một vỉ | Bắt buộc dùng cho đường Echo 5 V. |

- [Hshop: HC-SR04](https://hshop.vn/search?q=HC-SR04)
- [Shopee: VL53L0X](https://shopee.vn/search?keyword=VL53L0X)
- [Lazada: cảm biến siêu âm](https://www.lazada.vn/catalog/?q=cam%20bien%20sieu%20am%20HC-SR04)
- [Thế Giới IC: HC-SR04](https://www.thegioiic.com/search?q=HC-SR04)

## Video tham khảo

- **Xem trước:** [Using the HC-SR04 Ultrasonic Distance Sensor with Arduino - Everything you need to know!](https://www.youtube.com/watch?v=6F1B_N6LuKw) — DroneBot Workshop, tiếng Anh. Giải thích chi tiết cách đổi thời gian Echo sang khoảng cách (tập trung vào phần tính toán thời gian bay của âm thanh).
- [VL53l0x: Time-of-Flight Distance Sensor (ESP32 + Arduino series)](https://www.youtube.com/watch?v=SWBI6_rxmT8) — Simply Explained, tiếng Anh. Minh họa cảm biến VL53L0X đo thời gian bay của ánh sáng và đọc kết quả trực tiếp qua I2C.

## Bài tập

1. Chân `ECHO` giữ mức cao trong 5,8 ms. Tính khoảng cách $$d$$ theo mét và centimét với $$v = 343~\mathrm{m/s}$$.
2. Tại mốc 40 cm, cảm biến trả về xung Echo dài $$2320~\mu\mathrm{s}$$. Công thức $$t \times 0{,}01715$$ cho kết quả bao nhiêu centimét?
3. Chân `ECHO` ở mức cao 5 V nối về GPIO của ESP32. Khi không có cầu chia áp thì chân chịu bao nhiêu vôn, và khi mắc cầu chia 1 kΩ (phía trên) / 2 kΩ (xuống mass) thì điện áp tại chân là bao nhiêu?
4. Hai cảm biến VL53L0X nối song song mà không dùng `XSHUT`. Vì sao quét I2C không thấy đủ hai cảm biến và xử lý bằng chân nào?
5. Ở nhiệt độ phòng $30\,^\circ\mathrm{C}$, vận tốc âm $$v \approx 349~\mathrm{m/s}$$. Với khoảng cách thật 80 cm, xung Echo kéo dài bao lâu, và firmware dùng hằng số cố định 0,01715 cm/µs sẽ báo kết quả bao nhiêu?

### Gợi ý đáp án

1. $$d = 0{,}995~\mathrm{m} \approx 99{,}5~\mathrm{cm}$$ (kiểm tra lại: $$5800 \times 0{,}01715 = 99{,}5~\mathrm{cm}$$).
2. $$2320 \times 0{,}01715 \approx 39{,}8~\mathrm{cm}$$.
3. Không cầu chia: 5 V; có cầu chia 1 kΩ / 2 kΩ: $$5 \times 2/3 \approx 3{,}33~\mathrm{V}$$.
4. Cả hai đều có địa chỉ mặc định `0x29` nên trả lời đè lên nhau; dùng chân `XSHUT` để giữ một chip ở trạng thái reset, đổi địa chỉ chip còn lại rồi bật lại chip đầu.
5. $$t = 2 \times 0{,}80 / 349 \approx 4{,}58~\mathrm{ms} = 4585~\mu\mathrm{s}$$; nhân với 0,01715 cho $$78{,}6~\mathrm{cm}$$, ngắn hơn thực tế khoảng 1,4 cm.

## Đọc thêm

- [Datasheet HC-SR04 (bản SparkFun)](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf) — thông số xung `TRIG`, `ECHO` và nguồn 5 V.
- [Datasheet ST VL53L0X](https://www.st.com/resource/en/datasheet/vl53l0x.pdf) — chi tiết phép đo milimét, góc nhìn và địa chỉ I2C.
- [Mạch Pololu VL53L0X](https://www.pololu.com/product/2490) — tài liệu về `XSHUT` và chuyển mức logic.
- [`sensor_msgs/Range`](https://docs.ros.org/en/jazzy/p/sensor_msgs/msg/Range.html) — định dạng bản tin ROS 2 cho dữ liệu khoảng cách ở Chương 09.
