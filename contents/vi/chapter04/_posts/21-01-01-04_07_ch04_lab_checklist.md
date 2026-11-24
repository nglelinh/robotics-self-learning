---
layout: post
title: "Checklist lab chương 04"
chapter: "04"
order: 7
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter04
lesson_type: required
draft: false
---

Thời lượng: **50–70 phút**. Đây là mốc kiểm tra hoàn thành chương, không bổ sung cảm biến mới. Bạn vượt qua chương 04 khi `lab-notes.md` chứa đầy đủ các bằng chứng đo kiểm bên dưới trước khi chuyển sang Chương 05.

Trước khi để robot tự chạy vòng kín trong phòng lab, một kỹ sư robotics kỳ cựu không bao giờ vội viết thuật toán điều hướng ngay — họ dành 15 phút để **kiểm định từng cảm biến lúc đứng yên và lúc chuyển động chậm**. Bởi nếu một dây encoder lỏng làm mất xung, một trục IMU bị đảo dấu, hay một cảm biến siêu âm nhiễu quá mức, thì bộ điều khiển thông minh nhất thế giới cũng sẽ lái robot đâm thẳng vào tường. Checklist Chương 04 đóng vai trò như "bảng kiểm trước giờ bay" giúp bạn tách biệt lỗi phần cứng/cảm biến khỏi lỗi thuật toán.

## Bản đồ kiến thức nền: Kiểm định cảm biến theo quy chuẩn đo lường

### 1. Độ chính xác (Accuracy) vs. Độ chụm (Precision / Noise Floor)
- **Độ chính xác (Accuracy):** trung bình các phép đo có nằm sát giá trị thực tế hay bị lệch hằng số (**bias**)? Bias sửa được bằng **hiệu chuẩn (calibration)**.
- **Độ chụm (Precision):** khi robot đứng yên tuyệt đối, các mẫu đo dao động quanh trung bình với độ lệch chuẩn $$\sigma$$ lớn cỡ nào? Độ phân tán $$\sigma$$ phản ánh **sàn nhiễu (noise floor)** của cảm biến.

### 2. Quy ước dấu và hệ tọa độ đồng nhất (REP-103)
Trong robotics (đặc biệt khi tiến lên ROS 2 ở các chương sau), quy ước chuẩn là hệ tọa độ tay phải: trục **X hướng về phía trước**, **Y sang trái**, **Z hướng lên trên**; quay ngược chiều kim đồng hồ nhìn từ trên xuống là **yaw dương (+)**. Kiểm tra dấu encoder và gyro ngay từ lab Chương 04 giúp bạn tránh hàng giờ gỡ lỗi ngược hướng về sau.

### 3. Đánh đổi giữa lọc nhiễu (Averaging) và độ trễ pha
Lấy trung bình trượt $$N$$ mẫu độc lập giúp giảm độ lệch chuẩn nhiễu đi $$\sqrt{N}$$ lần, nhưng đồng thời cộng thêm độ trễ trung bình $$\frac{N-1}{2}\Delta t$$. Trong vòng điều khiển nhanh, lọc quá tay sẽ làm robot phản ứng chậm và lắc qua lại.

### Khung giải thích: Cầm tay tính trung bình, độ lệch chuẩn sàn nhiễu và hiệu quả lọc trung bình 4 mẫu (nên đọc chậm)

Khi robot đứng yên cách tường phẳng đúng **$$20{,}0\text{ cm}$$**, bạn ghi lại 5 mẫu liên tiếp từ cảm biến khoảng cách (đơn vị cm):
$$[20{,}0,\quad 20{,}4,\quad 19{,}6,\quad 20{,}2,\quad 19{,}8].$$

1. **Tính giá trị trung bình mẫu ($$\bar{x}$$):**
   $$\bar{x} = \frac{20{,}0 + 20{,}4 + 19{,}6 + 20{,}2 + 19{,}8}{5} = \frac{100{,}0}{5} = 20{,}0\text{ cm}$$
   *(Bias $$\approx 0$$ — cảm biến đã được hiệu chuẩn tốt!)*

2. **Tính phương sai mẫu ($$s^2$$) và độ lệch chuẩn sàn nhiễu ($$s$$):**
   Các độ lệch $$(x_i - \bar{x})$$: $$[0,\; +0{,}4,\; -0{,}4,\; +0{,}2,\; -0{,}2]$$.
   $$s^2 = \frac{0^2 + 0{,}4^2 + (-0{,}4)^2 + 0{,}2^2 + (-0{,}2)^2}{5 - 1} = \frac{0 + 0{,}16 + 0{,}16 + 0{,}04 + 0{,}04}{4} = \frac{0{,}40}{4} = 0{,}10\text{ cm}^2.$$
   $$s = \sqrt{0{,}10} \approx 0{,}316\text{ cm}.$$

3. **Nếu gom trung bình $$N = 4$$ mẫu ở tần số đo $$20\text{ Hz}$$ ($$\Delta t = 50\text{ ms}$$):**
   - Sàn nhiễu giảm xuống còn: $$s_{\text{mới}} = \frac{0{,}316}{\sqrt{4}} = 0{,}158\text{ cm}$$ (mịn gấp đôi!).
   - Cái giá phải trả: độ trễ trung bình tăng thêm $$\frac{4-1}{2} \times 50\text{ ms} = 75\text{ ms}$$ — hoàn toàn chấp nhận được cho robot chạy chậm $$0{,}2\text{ m/s}$$ (chỉ đi thêm $$1{,}5\text{ cm}$$), nhưng sẽ quá chậm cho drone bay nhanh!

## Mục tiêu học

Bạn tự đánh giá sổ thực hành Chương 04 theo tiêu chí đạt/trượt rõ ràng: có địa chỉ I2C kèm ảnh đấu dây, có giá trị $$N$$ đo bằng tay cho encoder cùng mét trên mỗi xung, có số đo IMU lúc nằm yên (hoặc ghi chú hoãn có ngày kèm tính tay), có bảng sai số đo khoảng cách (hoặc bản dry-run 5,8 ms và 3,33 V), và có câu quyết định hoãn camera chứa con số 147 Mbit/s. Bạn trình bày gọn gàng trong một khối mẫu để người khác dễ kiểm tra, ghi nhận hai lỗi thực tế đã gặp (hoặc chủ động tái hiện để kiểm chứng) và phân biệt được một bản ghi chép kín chữ nhưng vẫn không đạt yêu cầu.

## Kiến thức cần có

Bài này tổng hợp kết quả từ Bài 04-01 đến 04-06 trong `lab-notes.md` cùng phiếu nhận diện Bài 04-02 và các con số kiểm chuẩn đã tính: $$N$$ và $$r = 0{,}0325~\mathrm{m}$$ (với bánh ví dụ), bước lọc bổ trợ $9{,}889^\circ$, xung Echo 5,8 ms tương ứng 99,5 cm, cầu chia áp 3,33 V và băng thông camera 147 Mbit/s. Chương 05 sẽ bắt đầu đấu động cơ và mạch cầu H nên mọi sai sót về điện áp hay hệ số đếm cần được xử lý dứt điểm tại đây.

## Vì sao bài này quan trọng với Capstone A và ROS

Firmware teleop ở Chương 07 dựa trực tiếp vào cảm biến khoảng cách để dừng an toàn và dùng hằng số $$N$$ để tính quãng đường bánh xe. Về sau, ROS 2 xuất đúng các đại lượng này thành `sensor_msgs/Range`, `nav_msgs/Odometry`, `sensor_msgs/Imu` và `sensor_msgs/Image`. Nếu $$N$$ bị nhân đôi, odometry sẽ sai một nửa; nếu timeout của siêu âm bị lưu thành 0 cm, hệ thống sẽ báo nhầm là đang chạm tường; còn câu quyết định camera giúp tránh phát sinh tải USB 147 Mbit/s ngoài kế hoạch trước Chương 11.

![Phiếu nhận diện mà cửa này kiểm: bus, điện áp, và module nào được hoãn]({{ site.imgurl }}/generated/sensor_package_id.png)

## Mẫu khối ghi nhận trong `lab-notes.md`

Chép mẫu dưới đây vào `lab-notes.md`, điền đầy đủ bằng chứng thực tế và xóa bỏ các dòng chưa có dữ liệu xác thực (giữ lại dòng để trống sẽ bị tính chưa đạt):

```
## Ky duyet chuong 04
Ngay:
I2C: dia chi thay = ____ ; file anh = ____
Encoder: N = ____ xung moi vong truc ra (ba lan: __, __, __)
         r = ____ m ; met moi xung = ____
         kenh dan khi tien: ____  (hoac "mot kenh, khong biet chieu")
IMU: |a| = ____ g ; truc luc de yen = ____ dau ____
     lech gyro deg/s = (__, __, __)
     HOAC giay hoan ngay ____ va da kiem buoc loc 9.889 deg
Do tam: 20 cm -> __ cm (sai __) ; 40 -> __ (sai __) ; 80 -> __ (sai __)
       HOAC dry-run: 5.8 ms -> 99.5 cm ; cau chia 5*(2/3) = 3.33 V
Camera: hoan den chuong 11 ; YUYV 640x480 30 fps xap xi 147 Mbit/s
Hong 1:
Hong 2:
```

## Tiêu chí đạt và trượt

- **I2C:** ghi tối thiểu một địa chỉ quét được (như `0x68`, `0x69` hoặc `0x29`) kèm ảnh chụp rõ module và dây nối. Ghi chung chung "quét ổn, không lỗi" mà thiếu địa chỉ và ảnh là trượt.
- **Encoder:** $$N$$ phải đo từ ba lần quay tay trục ra (lệch nhau không quá 1 xung), kèm giá trị $$2\pi r / N$$ tính theo mét (ví dụ với $$r = 0{,}0325~\mathrm{m}$$, chu vi $$\approx 0{,}2042~\mathrm{m}$$ và $$N = 20$$ thì mỗi xung là $$0{,}01021~\mathrm{m}$$). Chép thông số PPR của người bán khi kết quả quay tay khác đi là trượt. Với encoder một kênh, chỉ đạt khi ghi rõ không xác định được chiều từ tín hiệu chân đó.
- **IMU:** ghi độ lớn gia tốc khi nằm yên (gần 1 g), tên trục và dấu, cùng sai lệch tĩnh gyro tính bằng độ/giây sau khi đã chia thang datasheet — hoặc ghi chú hoãn có ngày kèm đủ hai phép tính tay: bước lọc bổ trợ $$\theta = 9{,}889~\mathrm{deg}$$ và độ trôi $$0{,}5~\mathrm{deg/s} \times 60~\mathrm{s} = 30~\mathrm{deg}$$. In số nguyên LSB thô như độ sẽ bị tính trượt.
- **Đo khoảng cách:** có đủ bảng 20 / 40 / 80 cm kèm sai số có dấu (ở 40 cm trên bìa phẳng, sai số trong khoảng 5 cm là đạt; nếu lớn hơn phải giải thích được nguyên nhân). Thiếu bất kỳ mốc nào là trượt. Nếu chưa có cảm biến, bản dry-run chỉ đạt khi có đủ phép tính $$5{,}8~\mathrm{ms} \rightarrow 99{,}5~\mathrm{cm}$$ và cầu chia $$5 \times 2/3 \approx 3{,}33~\mathrm{V}$$.
- **Camera:** ghi rõ quyết định hoãn camera đến Chương 11 kèm số liệu luồng YUYV 640×480 ở 30 fps xấp xỉ 147 Mbit/s. Thiếu con số này là trượt.
- **Hai lỗi thực tế:** mỗi lỗi nêu rõ hiện tượng quan sát được và cách đã sửa (hoặc sẽ sửa). Ghi "không có lỗi" sẽ không đạt; có thể ghi nhận trường hợp thử nghiệm đảo dây A/B hoặc đo tấm vải mất Echo nếu có số liệu kèm theo.

## Ví dụ một sổ ghi chép chưa đạt

Mẫu dưới đây trông có vẻ đã điền kín các mục nhưng thực chất vi phạm nhiều tiêu chí quan trọng:

```
# lab-notes.md — vi du KHONG dat
Ngay: 12/9

I2C: quet on, khong loi. (khong dia chi, khong anh)

Encoder: nguoi ban ghi 40 PPR nen N = 40.
Quay tay mot vong thay khoang 20 nhay nhung minh giu 40.
r = 0.0325 m
met moi xung = 0.2042/40 = 0.0051 m

IMU: de phang, az = 16384 do. Gyro 70.

Do tam: ECHO vao GPIO18, khong dien tro, VCC 5 V.
So nhay. Minh se lay trung binh trong code.
Chua lam moc 20 cm. Moc 40 cm doi khi ra 80.

Camera: dang dat ESP32-CAM de Chuong 07 nhin thay hanh lang.

Loi: khong co.
```

Phân tích các lỗi: mục I2C thiếu cả địa chỉ lẫn ảnh; mục Encoder đo tay ra 20 nhưng vẫn giữ $$N = 40$$ khiến mét trên mỗi xung chỉ còn một nửa (140 xung bị tính thành $$0{,}71~\mathrm{m}$$ thay vì $$1{,}43~\mathrm{m}$$); mục IMU in giá trị LSB thô như độ (đúng ra ở $$\pm 2~\mathrm{g}$$, 16384 là $$+1~\mathrm{g}$$, và ở $$\pm 250~\mathrm{deg/s}$$, 70 tương ứng $$70/131 \approx 0{,}53~\mathrm{deg/s}$$); mục đo tầm nối thẳng `ECHO` 5 V vào GPIO18 không qua cầu chia 1 kΩ / 2 kΩ (3,33 V) và bỏ sót mốc 20 cm; mục camera thiếu con số 147 Mbit/s và chọn sai ESP32-CAM cho Chương 07; cuối cùng dòng "không có lỗi" đã che lấp chính những sai sót nghiêm trọng ngay trên trang.

## Cần khắc phục gì trước khi sang Chương 05

Chương 05 sẽ bổ sung nguồn động cơ và mạch cầu H có dòng tải lớn. Trước khi chốt Chương 04, cần bảo đảm: lắp cầu chia áp 1 kΩ / 2 kΩ (~3,33 V) cho chân `ECHO` hoặc tháo dây `ECHO` ra; cập nhật $$N$$ theo kết quả quay tay và tính lại mét trên mỗi xung; quy đổi dữ liệu IMU sang g và độ/giây (hoặc dùng ghi chú hoãn có ngày kèm $9{,}889^\circ$ và $30^\circ$); hoàn thiện bảng đo tầm hoặc bản dry-run; sửa lại câu hoãn camera (không dùng ESP32-CAM cho Chương 07); và ghi rõ hai lỗi thực tế đã xử lý.

## Lab

### An toàn

Bài này tập trung rà soát sổ thực hành. Nếu cần cấp nguồn chụp lại ảnh, chỉ dùng USB, giữ bánh xe nhấc khỏi bàn và đảm bảo chân `ECHO` đi qua cầu chia áp; không cố tình tái hiện lỗi nối thẳng 5 V lên GPIO thật.

### BOM

| Món | Vai trò |
|------|---------|
| `lab-notes.md` | Tài liệu rà soát và ký duyệt |
| Ảnh phiếu Bài 04-02 | Đối chiếu địa chỉ và sơ đồ chân |
| Sổ Bài 04-05 | Bảng sai số hoặc bản dry-run |
| Máy tính cầm tay | Kiểm tra lại $$2\pi r/N$$ và phép tính Echo 5,8 ms |

### Các bước

1. Dán khối mẫu ký duyệt vào `lab-notes.md` và điền đầy đủ từ kết quả thực đo của các bài trước (dùng ghi chú hoãn hoặc dry-run có ngày đối với linh kiện chưa giao).
2. Kiểm tra lại trực tiếp phép tính mét trên mỗi xung và $$343 \times 0{,}0058 / 2 = 0{,}995~\mathrm{m}$$.
3. Đối chiếu trang sổ của bạn với ví dụ chưa đạt ở trên để sửa mọi mục còn sơ sài hoặc sai đơn vị.
4. Ghi rõ hai lỗi đã gặp kèm số liệu cụ thể trước khi chuyển sang Chương 05.

### Kết quả mong đợi

Bất kỳ bạn cùng lớp nào đọc `lab-notes.md` cũng thấy ngay: một địa chỉ I2C kèm ảnh, một giá trị $$N$$ đo tay, số đo IMU theo g và độ/giây (hoặc ghi chú hoãn đủ số), bảng đo khoảng cách (hoặc 99,5 cm và 3,33 V), câu 147 Mbit/s và hai lỗi có số liệu.

### Lỗi thường gặp

| Hiện tượng | Nguyên nhân thường gặp |
|------------|------------------------|
| Các mục chỉ ghi "có" hoặc "đã làm" | Thiếu con số đo, địa chỉ cụ thể hoặc tên tệp ảnh |
| Chép $$N$$ từ tiêu đề bán hàng | Bỏ qua kết quả tự quay tay để xác định $$N$$ |
| Ghi chú hoãn IMU thiếu 9,889 và 30 độ | Chưa hoàn thành phần tính tay bắt buộc |
| Bản dry-run đo tầm thiếu 3,33 V | Bỏ quên phép tính cầu chia áp trên giấy |
| Câu camera không ghi tốc độ bit | Thiếu số liệu 147 Mbit/s theo yêu cầu |

## Mua ở Việt Nam

Chỉ mua bổ sung các cảm biến còn thiếu cho mốc hoàn thành chương; chưa mua camera.

| Món | Từ khóa | Khoảng giá (VND) | Thay thế |
|------|---------|------------------|----------|
| HC-SR04 | `HC-SR04` | 15.000–40.000 | [Trang Hshop](https://hshop.vn/cam-bien-sieu-am-srf04), thường khoảng 20.000 |
| VL53L0X (tùy chọn) | `VL53L0X` | 35.000–90.000 | [Hshop VL53L0X](https://hshop.vn/cam-bien-khoang-cach-tof-laser-radar-vl53l0x). Chỉ dùng siêu âm vẫn đủ đạt chương. |
| MPU-6050 GY-521 | `MPU6050` | 35.000–90.000 | [Hshop GY-521](https://hshop.vn/cam-bien-6-dof-bac-tu-do-gy-521-mpu6050), thường khoảng 85.000. Có thể dùng MPU6500 nếu khớp thư viện. |
| Động cơ TT có encoder (một cặp) | `động cơ TT encoder` | 40.000–90.000 một cái | Luôn tự đo $$N$$ bằng tay thay vì tin tiêu đề |

- [Hshop: HC-SR04](https://hshop.vn/search?q=HC-SR04)
- [Shopee: MPU6050](https://shopee.vn/search?keyword=MPU6050%20GY-521)
- [Lazada: động cơ TT encoder](https://www.lazada.vn/catalog/?q=dong%20co%20TT%20encoder)
- [Thế Giới IC: VL53L0X](https://www.thegioiic.com/search?q=VL53L0X)

## Video tham khảo

- **Xem trước:** [Serial Communications Explained: UART, I2C, and SPI](https://www.youtube.com/watch?v=IyGwvGzrqp8) — Electronoobs, tiếng Anh. Ôn nhanh ba chuẩn giao tiếp để kiểm tra lại toàn bộ đấu dây trước khi chốt Chương 04.

## Bài tập

Dựa trên mẫu sổ chưa đạt và các con số trong bài để trả lời ngắn gọn:

1. Sổ mẫu đặt $$N = 40$$ với $$r = 0{,}0325~\mathrm{m}$$ dù quay tay thu được khoảng 20 xung. Họ đã tính ra bao nhiêu mét mỗi xung, giá trị đúng phải là bao nhiêu, và 140 xung tương ứng bao xa trong hai trường hợp?
2. Chân `ECHO` nối thẳng vào GPIO không qua cầu chia áp. Khi Echo ở mức cao, chân GPIO phải chịu bao nhiêu vôn? Cần mắc cặp điện trở nào và điện áp sau chia $$V_{\mathrm{pin}}$$ bằng bao nhiêu?
3. Ghi chú hoãn IMU chỉ viết "module để sau" có đạt không? Hai kết quả tính tay nào bắt buộc phải có trên dòng đó?
4. Bản dry-run đo khoảng cách ghi "5,8 ms → 99,5 cm" nhưng không nhắc đến cầu chia áp. Đạt hay trượt, và còn thiếu con số điện áp nào?
5. Viết một câu quyết định camera đạt yêu cầu và chỉ ra câu nào trong sổ mẫu làm mục này bị trượt.

### Gợi ý đáp án

1. Họ tính ra $$0{,}0051~\mathrm{m}$$ mỗi xung; với số đo tay $$N = 20$$, giá trị đúng là $$0{,}01021~\mathrm{m}$$. Sau 140 xung, sổ sai báo $$0{,}71~\mathrm{m}$$ còn giá trị đúng là $$1{,}43~\mathrm{m}$$.
2. Chân chịu 5 V; cần mắc 1 kΩ từ `ECHO` tới GPIO và 2 kΩ từ GPIO xuống mass để hạ $$V_{\mathrm{pin}} \approx 3{,}33~\mathrm{V}$$.
3. Trượt; ghi chú hoãn bắt buộc có ngày, kết quả lọc bổ trợ $$9{,}889~\mathrm{deg}$$ và độ trôi $$0{,}5 \times 60 = 30~\mathrm{deg}$$.
4. Trượt; thiếu kết quả điện áp cầu chia $$5 \times 2/3 \approx 3{,}33~\mathrm{V}$$.
5. Câu đạt: hoãn camera đến Chương 11 kèm số liệu khoảng 147 Mbit/s; câu làm trượt trong sổ mẫu là "đang đặt ESP32-CAM để Chương 07 nhìn thấy hành lang".

## Đọc thêm

- [Datasheet HC-SR04 (bản SparkFun)](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf) — xác nhận đặc tính xung `ECHO` 5 V.
- [Datasheet MPU-6050](https://invensense.tdk.com/wp-content/uploads/2015/02/MPU-6000-Datasheet1.pdf) — bảng hệ số quy đổi 16384 LSB/g thành 1 g.
- [`sensor_msgs/Range`](https://docs.ros.org/en/jazzy/p/sensor_msgs/msg/Range.html) và [`nav_msgs/Odometry`](https://docs.ros.org/en/jazzy/p/nav_msgs/msg/Odometry.html) — hai loại bản tin ROS 2 tương ứng với các mục kiểm chứng trong chương này.
- [I2C của Espressif](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/peripherals/i2c.html) — tài liệu ngoại vi I2C dùng cho bước quét địa chỉ.
