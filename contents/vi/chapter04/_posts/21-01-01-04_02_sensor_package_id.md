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

Thời lượng: **60–80 phút**. Đây là bài thực hành nhận diện linh kiện trực tiếp trên bàn; bạn có thể kết hợp ảnh chụp các module đang có với tài liệu datasheet của những món chưa mua.

## Mục tiêu học

Sau bài này, bạn nhận diện được đúng loại cảm biến dựa trên hình dáng vật lý và nhãn chân trước khi cấp điện, xác định được điện áp nuôi và chuẩn giao tiếp (trig/echo, I2C, analog hay USB), đồng thời tuyệt đối không đưa tín hiệu Echo 5 V trực tiếp vào chân ESP32. Bạn lập được một phiếu nhận diện dùng lại cho Capstone A để chọn đúng cảm biến đo khoảng cách và encoder bánh xe, cũng như phân biệt rõ linh kiện cần chuẩn bị trước Chương 07 với các thiết bị thị giác để dành cho Chương 11.

## Kiến thức cần có

Bạn đã hoàn thành bài 04-01 (I2C, SPI, UART), nắm thói quen đọc sơ đồ chân từ Chương 01 và có sẵn đồng hồ vạn năng. Không bắt buộc phải có đầy đủ mọi loại cảm biến ngay trên bàn.

---

Trên bàn linh kiện robot, năm loại cảm biến phổ biến nhất — **siêu âm HC-SR04**, **laser ToF (VL53L0X)**, **IMU (MPU6050)**, **cảm biến hồng ngoại dò line (IR)** và **encoder bánh xe** — đều có kích thước chỉ bằng đồng xu, nhưng nguyên lý vật lý, điện áp làm việc và điểm mù của chúng lại khác nhau một trời một vực! Nhận diện đúng từng module bằng mắt thường và hiểu rõ giới hạn vật lý của nó giúp bạn chọn đúng "đôi mắt" cho từng nhiệm vụ.

## Kiến thức cần nhớ: Năm Giác quan Cốt lõi của Robot Di động

1. **Đo Khoảng cách (Siêu âm HC-SR04 vs. Laser ToF VL53L0X):** HC-SR04 phát sóng âm 40 kHz hình nón rộng (~$$15^\circ$$), hoạt động tốt với kính trong suốt nhưng dễ bị hấp thụ bởi rèm vải mềm và dùng logic **5 V**; VL53L0X đo thời gian bay của tia laser hồng ngoại chùm hẹp ($$t \sim$$ nano-giây), dùng **3,3 V I2C** và cực chính xác ở cự ly gần (< 1,2 m) nhưng kém hơn dưới ánh nắng gắt.
2. **Đo Chuyển động Nội tại (IMU 6 bậc tự do & Encoder):** IMU đo gia tốc tuyến tính ($$a_x, a_y, a_z$$) và vận tốc góc ($$\omega_x, \omega_y, \omega_z$$) trực tiếp trên thân xe; Encoder đếm số vòng quay từng bánh xe để tính quãng đường (odometry) nhưng bị sai khi bánh xe trượt trên sàn trơn!
3. **Cảm biến Gần / Dò vạch (Hồng ngoại phản xạ IR):** Phát tia hồng ngoại và đo cường độ phản xạ từ mặt sàn (màu trắng phản xạ mạnh, vạch đen hấp thụ) — rất nhạy với khoảng cách gầm xe và ánh sáng mặt trời.

### Ví dụ làm từng bước: Tính khoảng cách từ xung Echo của HC-SR04 và kiểm tra mạch hạ áp 5 V → 3,3 V

Cảm biến siêu âm HC-SR04 phát xung âm thanh với tốc độ trong không khí ở $$20^\circ\text{C}$$ là $$c = 343\text{ m/s} = \mathbf{0.0343\text{ cm}/\mu\text{s}}$$. Giả sử vi điều khiển đo được độ rộng xung `HIGH` trên chân Echo là **$$t = 1{,}166\ \mu\text{s}$$**:
1. Vì sóng âm phải bay từ cảm biến đến vật cản rồi **phản xạ quay ngược lại** (tổng quãng đường $$2d$$):
   $$
   d = \frac{c \cdot t}{2} = \frac{0.0343\text{ cm}/\mu\text{s} \times 1{,}166\ \mu\text{s}}{2} \approx \mathbf{20.0\text{ cm}}!
   $$
2. **Kiểm tra an toàn điện áp chân Echo cho ESP32/Pico (3,3 V):** HC-SR04 bản chuẩn cấp nguồn 5 V sẽ đẩy chân Echo lên **5,0 V**. Dùng cặp điện trở phân áp $$R_1 = 1\text{ k}\Omega$$ (nối từ Echo) và $$R_2 = 2\text{ k}\Omega$$ (nối xuống GND):
   $$
   V_{\text{GPIO}} = 5.0 \times \frac{2}{1 + 2} = \mathbf{3.33\text{ V}} \quad (\text{an toàn tuyệt đối!}).
   $$

### Giải thích: 4 bước nhận diện nhanh một module cảm biến mới trước khi cắm dây

1. **Bước 1 — Đọc kỹ chữ in lụa (silkscreen) quanh hàng chân:** Kiểm tra ngay ghi chú điện áp (`3V3` hay `5V` hay `VIN 3-5V`), tên bus (`SDA/SCL` = I2C, `TRIG/ECHO` = siêu âm, `A0/D0` = cảm biến IR/analog).
2. **Bước 2 — Soi chiều trục tọa độ in trên bo IMU:** Các module MPU6050/ICM-20948 đều in mũi tên trục $$+X, +Y$$ ngay trên mặt PCB — gắn lệch $$90^\circ$$ mà không đổi dấu trong code sẽ làm xe quay ngược chiều!
3. **Bước 3 — Kiểm tra xem trên module đã có sẵn IC ổn áp và điện trở kéo lên chưa:** Nhiều module GY-521 (MPU6050) đã hàn sẵn LDO 3,3 V và pull-up I2C, trong khi cảm biến trần cần cấp đúng 3,3 V sạch.
4. **Bước 4 — Kết hợp đa cảm biến (Sensor Fusion) để bù điểm mù cho nhau:** Siêu âm + ToF bù nhau trước kính và vải; Encoder + IMU (con quay hồi chuyển) bù nhau chống trượt bánh và trôi góc!

**Kiểm tra nhanh.** Nếu đặt vật cản cách cảm biến HC-SR04 đúng **1,00 mét** ($$100\text{ cm}$$), xung Echo sẽ kéo dài khoảng bao nhiêu mili-giây? Ta có $$t = \dfrac{2 \times 100}{0.0343} \approx \mathbf{5{,}831\ \mu\text{s} \approx 5.83\text{ ms}}$$ — và nếu vật cản ở quá xa (4 m), chờ `pulseIn()` không đặt `timeout` có thể làm kẹt vòng lặp chính tới hàng chục mili-giây!

---

## Vì sao bài này quan trọng với Capstone A và ROS

Capstone A cần một cảm biến phát hiện vật cản phía trước và (nếu muốn kiểm chứng định lượng tốt hơn) encoder đếm vòng quay bánh xe. Cảm biến siêu âm HC-SR04 hoặc laser ToF VL53L0X đảm nhiệm việc đo khoảng cách; động cơ giảm tốc có encoder từ tính đảm nhiệm việc đếm xung. IMU chưa bắt buộc cho lần chạy teleop đầu tiên và sẽ được dùng sau cho `sensor_msgs/Imu`. Riêng camera thuộc phạm vi Chương 11 vì đòi hỏi băng thông USB và năng lực xử lý vượt quá khả năng của ESP32 thuần; mua camera quá sớm khi robot chưa dừng an toàn được chỉ gây lãng phí ngân sách.

![Phiếu nhận diện module cảm biến]({{ site.imgurl }}/generated/sensor_package_id.png)

## Cách nhận diện bằng mắt thường

Hãy quan sát theo đúng trình tự: hình dáng vật lý (vỏ kim loại, cửa sổ quang học, số chân), sau đó đọc chữ in cạnh hàng chân, cuối cùng tra điện áp và giao thức trong datasheet. Một module có hình dáng tương tự HC-SR04 nhưng có 5 chân có thể là RCWL-1601 hoặc US-100 hỗ trợ UART — việc sao chép mã nguồn mẫu mà không kiểm tra nhãn chân sẽ không hoạt động.

- **HC-SR04:** có hai đầu thu phát siêu âm vỏ nhôm hình trụ gắn trên bo mạch nhỏ với bốn chân `VCC`, `TRIG`, `ECHO`, `GND`. Module dùng nguồn 5 V; chân `TRIG` nhận xung kích khoảng 10 µs, còn chân `ECHO` xuất xung có độ rộng tỉ lệ với thời gian sóng âm đi và về. Trên bản phổ biến, mức cao của `ECHO` là 5 V, vượt giới hạn chịu áp của ESP32 nên phải hạ áp qua cầu chia (1 kΩ từ `ECHO` tới GPIO, 2 kΩ từ GPIO xuống mass để đưa về khoảng 3,3 V). Chùm sóng âm có góc mở khá rộng (khoảng 15°), nên bề mặt cứng như khung cửa và bề mặt mềm như rèm vải sẽ cho kết quả rất khác nhau.
- **VL53L0X và họ cảm biến ToF:** đặc trưng bởi cửa sổ quang màu đen rất nhỏ (thường đặt trên bo mạch breakout màu tím), gồm các chân `VIN`, `GND`, `SCL`, `SDA`, đôi khi có thêm `XSHUT` và `GPIO1`. Giao tiếp bằng I2C với địa chỉ mặc định `0x29`, trả về trực tiếp khoảng cách tính bằng milimét do chip tự tính toán. Nhiều bo breakout có sẵn ổn áp nên `VIN` nhận 3,3–5 V, nhưng mức logic I2C vẫn phải khớp với vi điều khiển. Khi dùng hai module VL53L0X trên cùng bus, chúng sẽ trùng địa chỉ `0x29` trừ khi dùng chân `XSHUT` để bật từng con và gán địa chỉ mới.
- **MPU-6050 / GY-521:** bo mạch phẳng nhỏ (thường màu xanh dương) với hàng chân `VCC`, `GND`, `SCL`, `SDA`, `XDA`, `XCL`, `AD0`, `INT`, giao tiếp I2C ở địa chỉ `0x68` hoặc `0x69` tùy mức chân `AD0`. Đây là cảm biến quán tính gồm gia tốc kế và con quay hồi chuyển, không dùng để đo khoảng cách.
- **Cảm biến hồng ngoại phản xạ / vật cản:** gồm một LED phát trong suốt và một phototransistor thu màu đen đặt cạnh nhau, thường có ba chân `VCC`, `GND` và `OUT` (hoặc `AO`). Loại ngõ ra số chuyển mức khi ánh sáng phản xạ vượt ngưỡng chỉnh bằng biến trở; loại ngõ ra tương tự (`AO`) cần nối vào chân ADC. Cảm biến dò line TCRT5000 cũng thuộc nhóm này — chúng không phải cảm biến ToF laser và dễ bị bão hòa dưới ánh nắng mạnh.
- **Encoder bánh xe:** thường gặp hai dạng là đĩa có rãnh đi qua cặp thu phát quang, hoặc đĩa nam châm nhỏ gắn phía sau trục động cơ TT vàng đi kèm cảm biến Hall. Loại có hai kênh tín hiệu `A` và `B` (quadrature) cho biết cả tốc độ lẫn chiều quay; loại chỉ có một kênh tín hiệu chỉ đo được tốc độ và không tự phân biệt được chiều tiến hay lùi.
- **Camera:** nhận diện dễ dàng qua cáp dẹt mềm bản rộng (FPC) cắm trên bo mạch như ESP32-CAM (OV2640), hoặc cáp USB của webcam chuẩn UVC. Webcam USB kết nối với máy tính chủ (laptop/Pi), không nối vào GPIO. ESP32-CAM không phù hợp làm bộ điều khiển chính cho Capstone A vì camera chiếm phần lớn chân GPIO, mạch ổn áp dễ sụt nguồn và không thuận tiện ghép thêm mạch cầu H động cơ.

## Ví dụ tính tay: hạ áp chân Echo 5 V

Khi phát xung phản hồi, chân `ECHO` của HC-SR04 ở mức 5 V. Mắc cầu chia áp gồm $$R_1 = 1~\mathrm{k}\Omega$$ từ `ECHO` tới chân ESP32 và $$R_2 = 2~\mathrm{k}\Omega$$ từ chân đó xuống mass, điện áp tại chân vi điều khiển là:

$$
V_{pin} = 5 \times \frac{R_2}{R_1 + R_2} = 5 \times \frac{2}{3} \approx 3{,}33~\mathrm{V}.
$$

Mức 3,33 V nằm trong giới hạn an toàn của ESP32. Bỏ qua cầu chia áp sẽ khiến chân GPIO chịu quá áp, nóng lên và hỏng. Ngược lại, VL53L0X dùng bus I2C 3,3 V không cần cầu chia này nếu bo mạch breakout đã hỗ trợ mức logic 3,3 V. Mỗi loại module có yêu cầu điện riêng và cần ghi chú rõ trên phiếu nhận diện.

## Lab: lập phiếu nhận diện một trang

### An toàn

Thực hiện bước nhận diện khi chưa cấp điện. Khi cấp nguồn kiểm tra, chỉ cấp qua cổng USB cho vi điều khiển; không nối đường `VCC` 5 V của cảm biến vào chân `3V3` của ESP32 và không nối chân `ECHO` vào GPIO khi chưa có cầu chia áp.

### BOM

| Món | Vai trò |
|-----|---------|
| Bất kỳ hai loại nào trong: HC-SR04, VL53L0X, GY-521, module IR, động cơ encoder, webcam | Linh kiện thực tế cần nhận diện |
| Điện thoại chụp ảnh | Lưu hình vào phiếu |
| Đồng hồ vạn năng | Đo kiểm `VCC` sau khi cấp nguồn |
| Datasheet tương ứng | Xác minh điện áp và chuẩn giao tiếp |

### Các bước

1. Khi chưa cấp nguồn, chụp cận cảnh từng module sao cho đọc rõ nhãn in tại hàng chân.
2. Ghi vào bảng nháp cho mỗi module: tên gọi, các nhãn chân nhìn thấy, chuẩn giao tiếp dự đoán, điện áp dự đoán và phân loại ("dùng ngay cho Capstone A" hoặc "để sau").
3. Mở datasheet hoặc sơ đồ của nhà sản xuất để kiểm tra lại, sửa và đánh dấu rõ các điểm ban đầu dự đoán sai.
4. Nếu đã có module I2C 3,3 V, cấp nguồn và kiểm tra lại như bài 04-01; nếu linh kiện đang vận chuyển, dừng ở bước hoàn thiện phiếu giấy.
5. Lưu phiếu vào `lab-notes.md` để đối chiếu lại ở Chương 07.

### Kết quả mong đợi

Tối thiểu hai module được xác minh chính xác điện áp và chuẩn bus; có câu ghi chú rõ `ECHO` của HC-SR04 ở mức 5 V và VL53L0X dùng I2C tại `0x29`; nêu rõ lựa chọn cảm biến khoảng cách và quyết định hoãn camera sang chương sau.

### Lỗi thường gặp

| Nhầm lẫn | Hệ quả |
|----------|--------|
| Thấy cửa sổ đen nhỏ đều tưởng là IMU | Quét I2C nhầm cảm biến khoảng cách, hoặc cố đọc mét từ con quay hồi chuyển |
| Đưa thẳng 5 V vào chân ESP32 | Chân GPIO quá nhiệt, treo trạng thái hoặc hỏng vĩnh viễn |
| Nối hai bo VL53L0X mà không dùng `XSHUT` | Quét chỉ thấy một địa chỉ hoặc xung đột bus |
| Dùng encoder một kênh | Không tự phân biệt được chiều tiến và lùi |
| Chọn ESP32-CAM làm bộ điều khiển Capstone A | Thiếu chân điều khiển động cơ và dễ sụt nguồn |

## Mua ở Việt Nam

Ưu tiên mua cảm biến khoảng cách và (nếu ngân sách cho phép) cặp động cơ TT có gắn sẵn encoder; để dành camera cho Chương 11.

| Món | Từ khóa | Khoảng giá (VND) | Thay thế |
|-----|---------|------------------|----------|
| HC-SR04 | `cảm biến siêu âm HC-SR04` | 15.000–40.000 | [Hshop HC-SR04](https://hshop.vn/cam-bien-sieu-am-srf04) từng niêm yết khoảng 20.000. Chỉ thay bằng US-100 khi đã kiểm tra rõ chế độ UART/GPIO. |
| Module VL53L0X | `VL53L0X ToF` | 35.000–90.000 | [Hshop VL53L0X](https://hshop.vn/cam-bien-khoang-cach-tof-laser-radar-vl53l0x). Lưu ý VL53L1X đo xa hơn nhưng dùng thư viện khác. |
| GY-521 | `MPU6050 GY-521` | 35.000–90.000 | MPU6500 nếu mã mẫu tương thích thanh ghi. |
| IR vật cản hoặc TCRT5000 | `cảm biến hồng ngoại vật cản` | 8.000–25.000 | Phù hợp dò line, không đủ tin cậy làm cảm biến tránh va chạm duy nhất. |
| Motor TT + encoder | `động cơ TT encoder Hall` | 40.000–90.000 một cái | Có thể dùng N20 hộp số kim loại có encoder nếu khớp lỗ gá khung (kiểm tra đường kính trục 3 mm hay 4 mm). |
| Trở cầu chia | `điện trở 1k 2k` | 10.000–20.000 một thanh | Thế Giới IC phù hợp mua điện trở rời. |

Liên kết tìm kiếm nhanh:

- [Hshop, từ khóa HC-SR04](https://hshop.vn/search?q=HC-SR04)
- [Shopee, motor encoder](https://shopee.vn/search?keyword=dong%20co%20TT%20encoder)
- [Lazada, VL53L0X](https://www.lazada.vn/catalog/?q=VL53L0X)
- [Thế Giới IC](https://www.thegioiic.com/search?q=HC-SR04)

## Video tham khảo

- **Xem trước:** [HC-SR04 Ultrasonic Distance Sensor and Arduino (Lesson #9)](https://www.youtube.com/watch?v=n-gJ00GTsNg) — Science Buddies, tiếng Anh. Giải thích nguyên lý hai chân `TRIG` và `ECHO` của HC-SR04 (không phải I2C).
- [What is an Inertial Measurement Unit (IMU)?](https://www.youtube.com/watch?v=qS9GwaekLW4) — Phidgets Inc., tiếng Anh. Tổng quan cấu tạo IMU gồm gia tốc kế và con quay hồi chuyển.
- [How Rotary Encoder Works and How To Use It with Arduino](https://www.youtube.com/watch?v=v4BbSzJ-hz4) — How To Mechatronics, tiếng Anh. Minh họa cấu tạo hai kênh của encoder quay, phân biệt với biến trở.

## Bài tập

1. Một bo mạch có hai đầu hình trụ bằng nhôm cùng bốn chân `VCC`, `TRIG`, `ECHO`, `GND`. Chân `ECHO` xuất mức cao bao nhiêu vôn và cần thêm cặp điện trở nào khi nối với ESP32?
2. Một bo mạch màu tím có cửa sổ quang nhỏ màu đen cùng hai chân `SCL`, `SDA`. Đây thuộc dòng cảm biến nào và địa chỉ I2C mặc định là gì?
3. Bạn cần biết bánh trái đang quay tiến hay quay lùi. Một cảm biến Hall đơn kênh có đủ không? Bạn cần chọn loại nào?
4. Phân loại các linh kiện sau vào hai nhóm "cần trước Capstone A" và "để sau khi robot đã chạy teleop": HC-SR04, camera USB, động cơ có encoder, ESP32-CAM, VL53L0X.
5. Hai module VL53L0X đều có địa chỉ mặc định `0x29`. Chân nào dùng để xử lý xung đột địa chỉ, và kết quả quét sẽ ra sao nếu chưa sử dụng chân đó?

### Gợi ý đáp án

1. Khoảng 5 V; cần cầu chia áp 1 kΩ (từ `ECHO` tới GPIO) và 2 kΩ (từ GPIO xuống mass) để hạ xuống xấp xỉ 3,33 V.
2. Cảm biến khoảng cách ToF (như VL53L0X), địa chỉ mặc định thường là `0x29`.
3. Không đủ; cần encoder hai kênh lệch pha (quadrature A và B), nếu không thì chiều quay chỉ suy đoán từ lệnh điều khiển động cơ và không phát hiện được lúc bánh tự trôi.
4. Trước Capstone A: HC-SR04 hoặc VL53L0X, và động cơ có encoder (nếu muốn đo quãng đường). Để sau: camera USB và ESP32-CAM.
5. Chân `XSHUT`. Nếu không dùng `XSHUT` để tắt/bật riêng từng chip và đổi địa chỉ, quá trình quét sẽ bị xung đột (chỉ hiện một địa chỉ hoặc lỗi bus).

## Đọc thêm

- [Datasheet HC-SR04 (bản SparkFun lưu)](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf)
- [Datasheet ST VL53L0X](https://www.st.com/resource/en/datasheet/vl53l0x.pdf)
- [Datasheet TDK MPU-6000/6050](https://invensense.tdk.com/wp-content/uploads/2015/02/MPU-6000-Datasheet1.pdf)
- [Ghi chú board Pololu VL53L0X](https://www.pololu.com/product/2490) — thông tin về địa chỉ và mức logic có thể tham khảo cho cả các bo breakout khác.
