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

Thời lượng: **70–90 phút**, kể cả một lần quét địa chỉ I2C trên mạch thật. Nếu module chưa về, bạn vẫn làm được bài bằng cách dry-run đúng thứ tự kiểm tra điện.

## Mục tiêu học

Hết bài này, bạn chọn được I2C, SPI hay UART từ datasheet của cảm biến, không chọn theo thói quen. Bạn biết khi nào bus hở cực (open-drain) cần điện trở kéo lên, và bạn chạy một lần quét địa chỉ ra kết quả kiểu `0x68` trước khi tin thư viện. Bạn cũng giải thích được vì sao teleop của Capstone A là một cuộc nói chuyện UART, trong khi IMU và cảm biến ToF trên cùng con robot lại muốn chung một bus I2C, và vì sao một topic ROS 2 không thay được những sợi dây đó.

## Kiến thức cần có

Bạn đã đo được thông mạch và điện áp một chiều bằng đồng hồ (Chương 01), biết chân GPIO 3,3 V trên ESP32 hoặc Pico (Chương 02), và đã nháy được LED từ firmware (Chương 03). Bài này chưa cần cài ROS.

## Vì sao bài này quan trọng với Capstone A và ROS

Capstone A ở Chương 07 cho robot vi sai chạy theo lệnh từ laptop qua cổng serial. Đường đó là UART: tốc độ baud, cặp TX/RX được đảo trong chip USB, và quy ước im lặng nghĩa là dừng. Khi con robot đã dừng được một cách đáng tin, người ta mới gắn thêm IMU I2C và thường là VL53L0X cũng I2C. Chương 09 sẽ xuất các số đó thành `sensor_msgs/Imu` và `sensor_msgs/Range`; Chương 10 có thể mang chúng qua micro-ROS. Nếu bus thiếu điện trở kéo lên hoặc sai địa chỉ, đồ thị ROS trống không phải vì file launch, mà vì breadboard. Học sợi dây trước.

## Ba bus, ba hợp đồng

Cảm biến số là một máy tính nhỏ với cuộc hội thoại đã được công bố. Datasheet đặt tên cuộc hội thoại. Việc của bạn là khớp điện áp, dây và tốc độ, rồi chứng minh linh kiện có trả lời trước khi hỏi nó về mét hay độ.

**I2C** dùng hai tín hiệu SDA và SCL, cùng nguồn và mass. Cả hai dây là open-drain: thiết bị chỉ được kéo dây xuống, điện trở kéo dây lên khi không ai nói. Nhiều mạch ra chân đã gắn sẵn 4,7 kΩ hoặc 10 kΩ lên điện áp logic của chính nó. Hai module song song làm lực kéo mạnh hơn (các điện trở mắc song song). Điện trở kéo bên trong ESP32 yếu, cỡ vài chục kiloohm, không đáng tin ở 400 kHz. Trên bus 3,3 V ngắn, điểm xuất phát thực tế là 4,7 kΩ ngoài lên 3,3 V nếu module chưa có sẵn.

Mỗi thiết bị có địa chỉ 7 bit. MPU-6050 trả lời ở `0x68` khi AD0 xuống mass và `0x69` khi AD0 lên cao. VL53L0X thường ở `0x29`. Master gọi địa chỉ, slave ACK bằng cách kéo SDA xuống, rồi việc đọc thanh ghi mới có nghĩa. Chế độ chuẩn là 100 kHz; chế độ nhanh là 400 kHz. Đừng mở đầu ở 1 MHz chỉ vì một sketch mẫu làm vậy.

**SPI** thêm xung nhịp và một chân chọn chip cho mỗi thiết bị: SCLK, MOSI, MISO và CS, cộng nguồn và mass. Bus này song công và nhanh hơn nhiều, nên một số IMU có cả SPI lẫn I2C. Mode là cặp bit CPOL và CPHA. Mode 0 nghĩa là clock nghỉ ở mức thấp và slave được lấy mẫu ở cạnh lên. Sai mode trông như cảm biến “có mặt” nhưng trả về số vô nghĩa. SPI không có byte địa chỉ; chân CS *chính là* địa chỉ. Để CS mức cao với những thiết bị bạn không đang nói chuyện.

**UART** không có clock. Hai bên thỏa thuận baud (Capstone A dùng 115200), khung truyền (8 bit dữ liệu, không parity, 1 stop bit), và phải đảo dây: TX của máy này vào RX của máy kia. Cáp USB giấu việc đảo đó trong adapter, nên Serial Monitor “tự nhiên chạy” cho đến khi bạn nối hai board mà lại nối TX với TX. Mass vẫn phải chung. Mỗi dây TX chỉ nên có một bên phát.

![Ba hợp đồng nối dây I2C, SPI và UART]({{ site.imgurl }}/generated/bus_i2c_spi_uart.png)

## Ví dụ tính và nối: một bus, hai cảm biến

Bạn muốn gắn GY-521 (MPU-6050) và VL53L0X lên ESP32 DevKit. Cả hai đều I2C và chạy được với logic 3,3 V. Nối cả hai chân SDA vào GPIO 21, cả hai SCL vào GPIO 22 (đối chiếu chữ in trên board vì bản clone hay đổi chân), cả hai mass vào GND của ESP32, cả hai VCC vào 3,3 V. Đừng cấp 5 V cho module VL53 “cho chắc” nếu mạch đó không có dịch mức; nhiều board tím nhỏ là linh kiện 3,3 V có sẵn ổn áp, và datasheet của *đúng tấm mạch đó* mới quyết định.

Lần quét phải in hai địa chỉ. Nếu chỉ thấy `0x68`, board ToF chưa có nguồn, SDA/SCL bị đảo, hoặc địa chỉ đã bị đổi mà bạn quét sai dải. Nếu không thấy gì, kiểm tra mass chung trước khi đổi thư viện.

Cổng USB của chính ESP32 là một UART khác, dùng cho teleop sau này. Nó không chiếm SDA/SCL. Bạn vừa quét I2C vừa in kết quả ra Serial Monitor. Sự tách đó — I2C cho chip trên robot, UART cho người — là kiến trúc mà Capstone A giữ lại.

## Lab: quét trước khi giải mã

### An toàn

Module trong lab này chỉ tiêu thụ vài chục miliampe. Chưa gắn driver motor lên cùng thanh nguồn breadboard. Nếu module nóng sau vài giây, rút USB; nguyên nhân hay gặp là đảo VCC và GND.

### BOM

| Món | Vai trò |
|-----|---------|
| ESP32 devkit hoặc Raspberry Pi Pico | Master I2C |
| GY-521 MPU-6050, hoặc bất kỳ module I2C bạn đang có | Địa chỉ đã biết |
| Điện trở 4,7 kΩ ×2 | Kéo lên, nếu module chưa có |
| Breadboard và dây dupont | Bus ngắn |
| Đồng hồ vạn năng | Thông mạch GND, điện áp VCC |

### Các bước

1. Đo thông mạch giữa GND module và GND MCU trước khi cấp nguồn.
2. Đo VCC tại module khi đã cắm USB. Bạn muốn khoảng 3,3 V, không phải 5 V, trên breakout chỉ chịu 3,3 V.
3. Nạp chương trình quét. Với ESP32 trên Arduino:

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

Trên Pico với MicroPython, ý tương đương là `I2C(0, sda=Pin(0), scl=Pin(1), freq=100_000)` rồi `i2c.scan()`.

4. Ghi các địa chỉ tìm được vào `lab-notes.md`, kèm ảnh dây.
5. Nếu có module I2C thứ hai, gắn thêm và xác nhận cả hai ACK vẫn hiện. Hai thiết bị trùng địa chỉ sẽ không trả lời sạch; đó là chuyện datasheet, không phải chuyện ROS.

### Kết quả mong đợi

Một module: một địa chỉ ổn định (`0x68` với GY-521 điển hình khi AD0 xuống mass). Hai module khác nhau: hai địa chỉ. Rút USB cắm lại, lần quét vẫn ra cùng kết quả.

### Lỗi thường gặp

| Bạn thấy | Thường là |
|----------|-----------|
| Không ACK | Chưa chung mass, đảo SDA/SCL, hoặc mất VCC |
| Địa chỉ lúc có lúc mất | Dupont lỏng, hoặc kéo lên nhầm điện áp |
| Mọi địa chỉ đều ACK | SDA bị chập xuống mass |
| 100 kHz được, 400 kHz hỏng | Dây dài hoặc thiếu kéo lên |
| Thư viện báo không thấy chip nhưng scan có | Thư viện dùng địa chỉ khác hoặc chân khác |

## Mua ở Việt Nam / Where to buy in Vietnam

Bạn cần một module I2C để xong lab, và vài con trở 4,7 kΩ nếu hộp linh kiện đang trống. Mạch dịch mức (kiểu BSS138, 4 hoặc 8 kênh) đáng mua trước khi trộn ngoại vi 5 V lên ESP32 3,3 V, nhưng chưa cần cho GY-521 chạy 3,3 V.

| Món | Từ khóa | Khoảng giá (VND) | Ghi chú |
|-----|---------|------------------|---------|
| GY-521 MPU-6050 | `MPU6050 GY-521` | 35.000–90.000 | [Trang Hshop](https://hshop.vn/cam-bien-6-dof-bac-tu-do-gy-521-mpu6050) từng niêm yết khoảng 85.000. MPU6500 thay được nếu thư viện khớp. |
| Trở 4,7 kΩ | `điện trở 4.7k 1/4W` | 10.000–25.000 một thanh | Thế Giới IC hợp để mua điện trở rời. |
| Mạch dịch mức | `logic level shifter 3.3 5` | 8.000–25.000 | Dùng cho tín hiệu, không dùng làm nguồn. |
| Dây dupont | `dây dupont đực cái` | 15.000–40.000 | |

Tìm bằng ô search, đừng bấm vào ảnh sản phẩm lạ trên mạng:

- [Tìm trên Hshop](https://hshop.vn/search?q=MPU6050)
- [Tìm trên Shopee](https://shopee.vn/search?keyword=MPU6050%20GY-521)
- [Tìm trên Lazada](https://www.lazada.vn/catalog/?q=MPU6050)
- [Tìm trên Thế Giới IC](https://www.thegioiic.com/search?q=tr%E1%BB%9F%20k%C3%A9o)

Giá chợ đổi. So hai người bán và ưu tiên module có chữ chân in trên PCB.

## Bài tập

1. Một board ghi SDA, SCL, GND, VCC và dòng chữ “I2C 0x29”. Đó là bus nào, có thể cần thêm linh kiện gì, và lần quét phải in gì?
2. Lần quét trống. Kể ba phép kiểm tra điện bạn làm trước khi sửa code, theo đúng thứ tự.
3. Hai board GY-521 đều buộc AD0 xuống mass. Chuyện gì xảy ra trên một bus I2C, và cách sửa rẻ tiền là gì?
4. Teleop Capstone dùng 115200, 8N1. Bạn nối TX của adapter USB-serial vào TX của ESP32. ESP32 nhận được gì, và khi nối UART rời giữa hai board thì phải làm sao?
5. Vì sao “topic `/imu/data` im re” không phải bước gỡ lỗi đầu tiên trên robot bạn chưa từng quét bus?

### Gợi ý đáp án

1. I2C; điện trở kéo lên rail logic nếu module chưa có; in `0x29`. 2. Mass chung, VCC có mặt và đúng điện áp, SDA/SCL không bị đảo. 3. Chúng đụng nhau ở `0x68`; kéo AD0 của một con lên VCC để thành `0x69` và sửa địa chỉ trong thư viện. 4. Không nhận được khung có nghĩa; UART rời phải chéo TX–RX và chung mass. Cáp USB đã chéo sẵn, nên đừng “sửa” một cổng USB đang chạy bằng cách đảo chân trong code trước. 5. Vì chip có thể chưa từng ACK. Quét đã, rồi hãy publish.

## Đọc thêm

- [NXP UM10204, đặc tả bus I2C](https://www.nxp.com/docs/en/user-guide/UM10204.pdf) — open-drain, địa chỉ và timing từ nguồn gốc.
- [Bài I2C của SparkFun](https://learn.sparkfun.com/tutorials/i2c/all) — kéo lên và địa chỉ, có ảnh dây.
- [Bài SPI của SparkFun](https://learn.sparkfun.com/tutorials/serial-peripheral-interface-spi/all) — mode và chân CS.
- [Truyền serial của SparkFun](https://learn.sparkfun.com/tutorials/serial-communication/all) — khung UART và baud.
- [Ghi chú driver I2C của Espressif](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/peripherals/i2c.html) — ngoại vi ESP32 thực sự làm được gì.
