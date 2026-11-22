---
layout: post
title: "Giao diện cảm biến: I2C, SPI, UART"
chapter: "04"
order: 1
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter04
lesson_type: required
draft: false
---

Thời lượng: **70–90 phút**, bao gồm một lần quét địa chỉ I2C trên mạch thật. Nếu module chưa giao tới, bạn vẫn có thể hoàn thành bài bằng cách thực hành chuẩn bị (dry-run) đúng trình tự kiểm tra điện.

## Mục tiêu học

Sau bài này, bạn có thể chọn đúng chuẩn giao tiếp I2C, SPI hay UART dựa trên datasheet của cảm biến thay vì chọn theo thói quen. Bạn hiểu khi nào bus cực thu hở (open-drain) cần điện trở kéo lên và luôn chạy quét địa chỉ (chẳng hạn thu được `0x68`) trước khi tin vào thư viện. Bạn cũng giải thích được vì sao điều khiển từ xa (teleop) của Capstone A sử dụng UART, trong khi IMU và cảm biến ToF trên cùng robot có thể dùng chung một bus I2C, và vì sao một topic ROS 2 không thể thay thế cho việc đấu nối phần cứng chính xác.

## Kiến thức cần có

Bạn đã biết đo thông mạch và điện áp một chiều bằng đồng hồ vạn năng (Chương 01), nắm được các chân GPIO 3,3 V trên ESP32 hoặc Pico (Chương 02), và đã nạp thành công chương trình nháy LED (Chương 03). Bài này chưa cần cài ROS.

## Vì sao bài này quan trọng với Capstone A và ROS

Capstone A ở Chương 07 điều khiển robot vi sai từ laptop qua cổng serial — đó chính là giao tiếp UART với tốc độ baud cố định, cặp chân TX/RX đã được bắt chéo bên trong chip USB-serial và quy tắc tự dừng khi mất lệnh. Khi cơ chế dừng an toàn đã chạy ổn định, ta mới gắn thêm IMU và cảm biến ToF (thường là VL53L0X) dùng chung bus I2C. Đến Chương 09, các số đo này sẽ được xuất thành bản tin `sensor_msgs/Imu` và `sensor_msgs/Range` (hoặc đưa qua micro-ROS ở Chương 10). Nếu bus thiếu điện trở kéo lên hoặc sai địa chỉ, đồ thị ROS sẽ không có dữ liệu — nguyên nhân nằm ở phần đấu dây breadboard chứ không phải tệp launch.

## Ba chuẩn bus và nguyên tắc giao tiếp

Mỗi cảm biến số thực chất là một vi mạch giao tiếp theo giao thức được quy định sẵn trong datasheet. Nhiệm vụ của bạn là khớp đúng điện áp, sơ đồ dây và tốc độ, rồi xác nhận cảm biến có phản hồi trước khi đọc số đo khoảng cách hay góc.

**I2C** sử dụng hai đường tín hiệu `SDA` (dữ liệu) và `SCL` (xung nhịp), cùng dây nguồn và mass. Cả hai đường đều thuộc kiểu cực thu hở (open-drain): thiết bị chỉ kéo dây xuống mức thấp, còn điện trở kéo lên (pull-up) sẽ đưa dây về mức cao khi không có thiết bị nào truyền. Nhiều bo mạch breakout đã hàn sẵn điện trở kéo lên 4,7 kΩ hoặc 10 kΩ lên mức logic của mạch đó; khi ghép nhiều module song song, điện trở kéo tương đương giảm xuống (kéo mạnh hơn). Điện trở kéo lên nội của ESP32 khá yếu (vài chục kΩ), không đủ tin cậy ở tốc độ 400 kHz. Trên bus 3,3 V dây ngắn, giá trị khởi đầu thực tế là điện trở ngoài 4,7 kΩ kéo lên 3,3 V nếu module chưa tích hợp sẵn.

Mỗi thiết bị I2C có một địa chỉ 7-bit. Ví dụ, MPU-6050 dùng địa chỉ `0x68` khi chân `AD0` nối mass và `0x69` khi `AD0` kéo lên mức cao; VL53L0X mặc định ở `0x29`. Master gọi địa chỉ, slave phản hồi xác nhận (ACK) bằng cách kéo `SDA` xuống thấp, sau đó việc đọc thanh ghi mới hợp lệ. Tốc độ chế độ chuẩn (Standard Mode) là 100 kHz và chế độ nhanh (Fast Mode) là 400 kHz; không nên bắt đầu ở 1 MHz ngay lập tức.

**SPI** sử dụng bốn đường tín hiệu gồm xung nhịp `SCLK`, dữ liệu `MOSI` (Master Out Slave In), `MISO` (Master In Slave Out) và chân chọn chip `CS` riêng cho từng thiết bị, cùng nguồn và mass. SPI truyền song công (full-duplex) và tốc độ cao hơn nhiều nên một số IMU hỗ trợ cả SPI lẫn I2C. Chế độ SPI (Mode 0–3) xác định bởi cặp bit `CPOL` và `CPHA` (Mode 0 có xung nhịp nghỉ ở mức thấp và lấy mẫu ở cạnh lên); chọn sai mode sẽ khiến cảm biến trả về dữ liệu vô nghĩa dù đấu dây đúng. SPI không dùng địa chỉ dạng byte — chân `CS` chính là tín hiệu chọn thiết bị, và phải giữ `CS` ở mức cao đối với các thiết bị không được truy cập.

**UART** truyền không đồng bộ (không có dây xung nhịp). Hai bên phải thống nhất tốc độ baud (Capstone A dùng 115200), cấu hình khung truyền (thường là 8N1: 8 bit dữ liệu, không parity, 1 bit dừng) và bắt chéo dây: `TX` bên này nối `RX` bên kia. Trên bo mạch có chip USB-serial, việc bắt chéo này đã làm sẵn bên trong mạch nên Serial Monitor hoạt động ngay; nhưng khi nối trực tiếp hai bo mạch với nhau, nối nhầm `TX` với `TX` sẽ làm mất giao tiếp. Hai thiết bị vẫn bắt buộc nối chung mass và mỗi đường `TX` chỉ nên có một thiết bị phát.

![Ba hợp đồng nối dây I2C, SPI và UART]({{ site.imgurl }}/generated/bus_i2c_spi_uart.png)

## Ví dụ tính và đấu nối: một bus, hai cảm biến

Giả sử bạn cần gắn cả GY-521 (MPU-6050) và VL53L0X lên ESP32 DevKit. Cả hai đều hỗ trợ I2C và hoạt động với logic 3,3 V. Bạn nối chung chân `SDA` của cả hai vào GPIO 21, chung `SCL` vào GPIO 22 (đối chiếu lại nhãn mạch vì một số biến thể có thể khác), nối chung `GND` với ESP32 và cấp nguồn 3,3 V. Không tự ý cấp 5 V cho module VL53L0X nếu chưa kiểm tra rõ bo mạch có mạch ổn áp và chuyển mức trên board hay không.

Khi chạy chương trình quét I2C, kết quả phải hiện đủ hai địa chỉ (`0x68` và `0x29`). Nếu chỉ thấy `0x68`, cần kiểm tra nguồn của bo mạch ToF, xem dây `SDA`/`SCL` có bị đảo hoặc địa chỉ có bị thay đổi hay không. Nếu không thấy địa chỉ nào, hãy kiểm tra dây mass chung trước khi nghi ngờ thư viện.

Cổng USB của ESP32 sử dụng một bộ UART riêng (dùng cho teleop về sau), hoàn toàn tách biệt với `SDA`/`SCL`. Do đó bạn có thể vừa quét bus I2C vừa in kết quả lên Serial Monitor — mô hình tách biệt "I2C cho cảm biến trên xe, UART cho giao tiếp với máy tính" này sẽ được giữ nguyên trong Capstone A.

## Lab: quét địa chỉ trước khi giải mã

### An toàn

Các module trong bài chỉ tiêu thụ vài chục miliampe. Không gắn mạch cầu H động cơ chung trên cùng thanh nguồn breadboard. Nếu cảm biến nóng lên sau vài giây cấp điện, rút cáp USB ngay vì khả năng cao đã đấu ngược `VCC` và `GND`.

### BOM

| Món | Vai trò |
|-----|---------|
| ESP32 devkit hoặc Raspberry Pi Pico | Master I2C |
| GY-521 MPU-6050, hoặc bất kỳ module I2C bạn đang có | Thiết bị có địa chỉ xác định |
| Điện trở 4,7 kΩ ×2 | Điện trở kéo lên (nếu module chưa hàn sẵn) |
| Breadboard và dây dupont | Tạo bus dây ngắn |
| Đồng hồ vạn năng | Đo thông mạch GND và kiểm tra điện áp VCC |

### Các bước

1. Đo thông mạch giữa `GND` của module và `GND` của vi điều khiển trước khi cấp nguồn.
2. Cắm USB và đo điện áp `VCC` ngay tại chân module; bảo đảm đạt khoảng 3,3 V (không phải 5 V đối với breakout chỉ chịu 3,3 V).
3. Nạp chương trình quét I2C. Với ESP32 trên nền tảng Arduino:

```cpp
#include <Wire.h>
void setup() {
  Serial.begin(115200);
  Wire.begin(21, 22); // SDA, SCL — khớp board của bạn
}
void loop() {
  Serial.println("scan");
  for (uint8_t addr = 1; addr < 127; ++addr) {
    Wire.beginTransmission(addr);
    if (Wire.endTransmission() == 0) {
      Serial.printf("ACK 0x%02X\n", addr);
    }
  }
  delay(2000);
}
```

Trên Pico dùng MicroPython, thao tác tương đương là khởi tạo `I2C(0, sda=Pin(0), scl=Pin(1), freq=100_000)` rồi gọi `i2c.scan()`.

4. Ghi lại các địa chỉ quét được vào `lab-notes.md` kèm ảnh chụp cách đấu dây.
5. Nếu có module I2C thứ hai, gắn thêm vào bus và xác nhận cả hai địa chỉ đều phản hồi ACK. Hai thiết bị trùng địa chỉ sẽ gây xung đột trên bus — cần xử lý theo datasheet trước khi nghĩ đến phần mềm.

### Kết quả mong đợi

Với một module: quét ra một địa chỉ ổn định (ví dụ `0x68` cho GY-521 khi `AD0` nối mass). Với hai module khác địa chỉ: quét ra đủ hai địa chỉ. Sau khi rút và cắm lại USB, kết quả quét vẫn giữ nguyên.

### Lỗi thường gặp

| Hiện tượng | Nguyên nhân thường gặp |
|------------|------------------------|
| Không nhận được ACK | Chưa nối chung mass, đảo `SDA`/`SCL`, hoặc mất nguồn `VCC` |
| Địa chỉ lúc hiện lúc mất | Dây dupont tiếp xúc lỏng, hoặc kéo lên sai mức điện áp |
| Mọi địa chỉ đều báo ACK | Đường `SDA` bị chập xuống mass |
| 100 kHz chạy được, 400 kHz lỗi | Dây quá dài hoặc thiếu điện trở kéo lên phù hợp |
| Quét thấy địa chỉ nhưng thư viện báo không tìm thấy chip | Thư viện cấu hình sai địa chỉ hoặc sai cặp chân I2C |

## Mua ở Việt Nam

Bạn cần ít nhất một module I2C để hoàn thành bài lab và vài điện trở 4,7 kΩ nếu chưa có sẵn. Mạch chuyển mức logic (loại dùng MOSFET BSS138, 4 hoặc 8 kênh) nên mua sẵn cho các bài sau khi ghép ngoại vi 5 V với ESP32 3,3 V, nhưng chưa bắt buộc cho GY-521 chạy 3,3 V.

| Món | Từ khóa | Khoảng giá (VND) | Ghi chú |
|-----|---------|------------------|---------|
| GY-521 MPU-6050 | `MPU6050 GY-521` | 35.000–90.000 | [Trang Hshop](https://hshop.vn/cam-bien-6-dof-bac-tu-do-gy-521-mpu6050) từng niêm yết khoảng 85.000. Có thể thay bằng MPU6500 nếu thư viện tương thích. |
| Trở 4,7 kΩ | `điện trở 4.7k 1/4W` | 10.000–25.000 một thanh | Thế Giới IC phù hợp để mua điện trở rời. |
| Mạch dịch mức | `logic level shifter 3.3 5` | 8.000–25.000 | Chỉ dùng cho đường tín hiệu, không dùng làm nguồn công suất. |
| Dây dupont | `dây dupont đực cái` | 15.000–40.000 | |

Nên tìm trực tiếp bằng từ khóa trên trang bán hàng uy tín:

- [Tìm trên Hshop](https://hshop.vn/search?q=MPU6050)
- [Tìm trên Shopee](https://shopee.vn/search?keyword=MPU6050%20GY-521)
- [Tìm trên Lazada](https://www.lazada.vn/catalog/?q=MPU6050)
- [Tìm trên Thế Giới IC](https://www.thegioiic.com/search?q=tr%E1%BB%9F%20k%C3%A9o)

Giá thị trường thay đổi theo thời điểm; hãy so sánh vài nhà bán và ưu tiên module in rõ ký hiệu chân trên bo mạch.

## Video tham khảo

- **Xem trước:** [Serial Communications Explained: UART, I2C, and SPI](https://www.youtube.com/watch?v=IyGwvGzrqp8) — Electronoobs, tiếng Anh. So sánh trực quan UART, I2C và SPI theo số dây và cơ chế xung nhịp, khớp với ba chuẩn giao tiếp trong bài.

## Bài tập

1. Một module in nhãn `SDA`, `SCL`, `GND`, `VCC` kèm dòng chữ "I2C 0x29". Đây là chuẩn bus nào, có thể cần thêm linh kiện gì nếu mạch chưa hàn sẵn, và chương trình quét phải in ra kết quả gì?
2. Chương trình quét I2C không trả về địa chỉ nào. Nêu ba bước kiểm tra phần cứng cần làm theo đúng thứ tự trước khi sửa mã nguồn.
3. Hai bo mạch GY-521 đều nối chân `AD0` xuống mass và gắn chung trên một bus I2C. Điều gì sẽ xảy ra, và cách khắc phục đơn giản nhất là gì?
4. Hệ thống teleop Capstone A dùng chuẩn 115200, 8N1. Nếu nối trực tiếp `TX` của bộ chuyển đổi USB-serial vào `TX` của ESP32, ESP32 sẽ nhận được gì? Khi nối UART rời giữa hai bo mạch cần đấu dây thế nào?
5. Vì sao kiểm tra lỗi "topic `/imu/data` không có dữ liệu" trên ROS không phải là bước gỡ lỗi đầu tiên đối với một robot chưa từng quét bus I2C?

### Gợi ý đáp án

1. Chuẩn I2C; có thể cần điện trở kéo lên (4,7 kΩ lên 3,3 V) nếu module chưa tích hợp sẵn; chương trình quét phải in `0x29`.
2. Kiểm tra lần lượt: nối chung mass (`GND`), điện áp `VCC` có mặt và đúng định mức, dây `SDA`/`SCL` không bị đấu ngược.
3. Cả hai xung đột tại cùng địa chỉ `0x68`. Cách khắc phục đơn giản nhất là kéo chân `AD0` của một module lên `VCC` để đổi địa chỉ sang `0x69`, rồi cấu hình lại địa chỉ tương ứng trong mã nguồn.
4. ESP32 không nhận được dữ liệu hợp lệ vì hai đầu phát nối vào nhau. Khi nối UART rời giữa hai bo mạch, phải bắt chéo `TX` với `RX` và nối chung mass (riêng cáp USB tích hợp trên devkit đã bắt chéo sẵn).
5. Vì có khả năng cảm biến chưa hề giao tiếp được ở tầng phần cứng (chưa ACK). Cần quét xác nhận địa chỉ I2C thành công trước khi kiểm tra tầng xuất dữ liệu ROS.

## Đọc thêm

- [NXP UM10204, đặc tả bus I2C](https://www.nxp.com/docs/en/user-guide/UM10204.pdf) — tài liệu chuẩn về cực thu hở, địa chỉ và định thời I2C.
- [Bài I2C của SparkFun](https://learn.sparkfun.com/tutorials/i2c/all) — minh họa chi tiết điện trở kéo lên, địa chỉ và sơ đồ đấu dây.
- [Bài SPI của SparkFun](https://learn.sparkfun.com/tutorials/serial-peripheral-interface-spi/all) — giải thích các chế độ SPI (CPOL/CPHA) và chân chọn chip `CS`.
- [Truyền serial của SparkFun](https://learn.sparkfun.com/tutorials/serial-communication/all) — tổng quan khung truyền UART và tốc độ baud.
- [Ghi chú driver I2C của Espressif](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/peripherals/i2c.html) — đặc tính phần cứng của ngoại vi I2C trên ESP32.
