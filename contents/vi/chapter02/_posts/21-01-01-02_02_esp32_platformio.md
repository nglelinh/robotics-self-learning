---
layout: post
title: "Arduino IDE và PlatformIO với ESP32"
chapter: "02"
order: 2
owner: "Nguyen Le Linh"
lang: vi
categories: [chapter02]
lesson_type: required
draft: false
---

## Mục tiêu

Bạn cài một toolchain ESP32 và để đường kia yên cho đến khi có một lần nhấp LED đáng tin. Đường Arduino IDE 2: thêm chỉ mục board của Espressif, cài gói `esp32`, chọn mục Dev Module hoặc NodeMCU-32S khớp silk. Đường PlatformIO: viết `platformio.ini` với board `esp32dev` và monitor 115200. Bạn nhấp `LED_BUILTIN` khi core có định nghĩa macro đó, và chỉ dùng GPIO 2 sau khi đã kiểm tra board của mình thực sự mắc đèn ở đó. Bạn nhận ra cổng không xuất hiện, cáp chỉ sạc, driver CH340, và brownout vì nguồn motor vẫn còn nối trong lúc nạp.

## Cần gì trước khi học

Bài bản đồ phải đã ghi bo mạch ESP32 là vi điều khiển chính. Nếu bạn đã chốt Pico, hãy đọc trang này như một bản đồ rồi sang bài Pico. Cài cả hai toolchain trong một buổi chiều là cách để id board sai được lưu vào project. Cần laptop và một cáp USB từng copy file được. Danh mục đầy đủ vẫn là bài mua sắm chương 00 ([Hóa đơn linh kiện và cách mua]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %})).

## Vì sao bài này gắn với Capstone A

Teleop vi sai ở chương 07 là một file firmware trên chính con chip này: PWM trái và phải hướng tới TB6612, phép thử im lặng khoảng 300 ms, bánh nhấc khỏi bàn. File đó chưa đáng tin cho đến khi board này nhận binary, đảo một chân bạn đã chọn, và in một dòng ở baud bạn đã ghi. Teleop Wi-Fi ở chương 08 đi cùng đường nạp này. Board chỉ nhấp trong video của người khác thì chưa vào robot của bạn. Monitor serial, một cổng và 115200 baud, là console bạn tin trước khi radio được phép làm rối log.

## Chọn một đường cài

Hai đường dùng chung core Arduino của Espressif. Chọn đường máy lab đã có sẵn. Tuần này chưa yêu cầu ESP-IDF.

Arduino IDE 2 là đường bấm chuột. Cài IDE. Mở Preferences (hoặc Settings) và dán URL Additional Boards Manager này:

```text
https://espressif.github.io/arduino-esp32/package_esp32_index.json
```

Mở Boards Manager, tìm `esp32`, cài **esp32 by Espressif Systems**. Rồi mở menu board và chọn mục khớp silk. DevKit 30 chân hoặc 38 chân kiểu chung là **ESP32 Dev Module**. Board có silk NodeMCU-32S thì dùng mục **NodeMCU-32S** khi mục đó có trong danh sách. Chọn cổng là thiết bị serial vừa xuất hiện. Nếu lần nạp đầu báo lỗi sync hoặc timeout, đặt Upload Speed bằng 115200. IDE thường bắt đầu ở 921600, và cáp dài hoặc bản clone CH340 làm rơi byte ở tốc độ đó.

PlatformIO là đường có file để so diff. Cài Visual Studio Code, rồi extension PlatformIO IDE, và đợi lần tải đầu chạy xong. Tạo project và đặt đoạn này trong `platformio.ini`:

```ini
[env:esp32dev]
platform = espressif32
board = esp32dev
framework = arduino
monitor_speed = 115200
```

`esp32dev` là đích ESP32 cổ điển kiểu chung: module họ WROOM và một chip USB-serial. Nó khớp NodeMCU-32S và các DevKit V1 thường gặp trong môn. Nó sai với board ESP32-S3 dùng USB nội. Đó là lý do nữa để bài trước bảo mua dev board cổ điển, trừ khi bạn sẵn sàng đổi cả file này lẫn sơ đồ chân.

## Cái đèn và cái cổng

`LED_BUILTIN` là macro mà một số biến thể board có định nghĩa. Nếu board bạn chọn có macro đó, dùng nó cho lần nhấp đầu. Nếu header không định nghĩa, dùng GPIO 2. GPIO 2 là LED onboard trên nhiều DevKit V1, và cũng là cách mắc hay gặp trên bản clone NodeMCU-32S. Đó không phải lời hứa. Có board để đèn ở GPIO khác, và có board chỉ có LED nguồn mà firmware không nhấp được. Đọc silk hoặc sơ đồ hãng, ghi số vào sổ, và đổi hằng số nếu GPIO 2 vẫn tối. Đừng cài lại IDE chỉ vì một macro lạc quan.

Sketch ngắn khớp lab này:

```cpp
#ifndef LED_BUILTIN
#define LED_BUILTIN 2  // hay gặp trên DevKit V1; đối chiếu pinout của bạn
#endif

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(115200);
  Serial.println("hello");
}

void loop() {
  digitalWrite(LED_BUILTIN, HIGH);
  Serial.println("high");
  delay(400);
  digitalWrite(LED_BUILTIN, LOW);
  Serial.println("low");
  delay(400);
}
```

`Serial.begin(115200)` phải khớp monitor. Lệch baud trông không giống im lặng. Nó trông như những ký tự suýt là chữ. Sketch này dùng `delay` để lần thành công đầu dễ thấy. Bài nhịp tim sẽ bỏ cấu trúc đó, vì lệnh dừng sau này không thể ngồi trong `delay` để đợi ngưỡng 300 ms.

Con chip sát phích USB không phải ESP32. Trên dev board cổ điển nó là CH340 hoặc CP2102. Cổng CP2102 thường hiện bằng driver có sẵn của hệ điều hành. Board CH340 trên Windows thường biến mất cho đến khi bạn cài driver CH340 của WCH; Device Manager lúc đó mới có cổng COM mới. Trên Linux các chip này hiện thành `/dev/ttyUSB0` (rồi `ttyUSB1` nếu cắm thêm một adapter). Trên Windows tên là `COM3`, `COM4`, hoặc một `COMx` khác chưa có trước lúc cắm cáp. Tài khoản Linux cần nằm trong nhóm `dialout`, và quyền đó chỉ có hiệu lực sau khi đăng xuất rồi đăng nhập lại.

Cáp USB chỉ sạc không được máy tính nhận. LED nguồn vẫn có thể sáng, vì dây nguồn còn và dây dữ liệu không có. Đổi sang cáp từng dùng để copy file. Sợi trong mục mua hàng là dạng đã biết cho các board micro-USB này.

Chế độ nạp là chuyện cái nút. GPIO 0 được lấy mẫu mức thấp lúc reset thì ESP32 cổ điển vào bootloader serial. Nút BOOT (đôi khi ghi IO0) giữ chân đó. EN, RST, hoặc RESET khởi động lại chip. Nhiều dev board tự vào bootloader qua dây DTR và RTS của chip USB-serial. Khi mạch đó không có, lần nạp bị timeout. Giữ BOOT, bắt đầu nạp, và thả BOOT khi log báo đang connecting. Nếu khó thao tác, giữ BOOT, chạm EN, thả BOOT, rồi nạp trong lúc chip còn ở chế độ đó.

## Lần nạp hỏng thường là gì

Ba lỗi phủ gần hết các báo “board chết” của lab này.

Menu board sai. Mục S3 hoặc C3, hoặc một mục “ESP32 Pico Kit” ngẫu nhiên, không khớp NodeMCU-32S. Lần nạp kêu, hoặc tưởng thành công mà chân bạn nhấp không phải chân bạn tưởng. Đặt Dev Module hoặc NodeMCU-32S, hoặc `board = esp32dev`, cho khớp silk.

Không có cổng. Bắt đầu từ cáp. Rồi tới driver: CH340 trên Windows, và `dialout` trên Linux. Cổng còn sót từ Pico hôm qua (`/dev/ttyACM0` trong khi ESP32 là `/dev/ttyUSB0`) cùng một lớp lỗi.

Chip reset trong lúc bootloader đang nói chuyện. Nếu còn động cơ, hoặc driver có chân VM vẫn buộc vào chân 5 V của board, xung dòng làm sụt ray và bản nạp chết giữa chừng. Rút VM. Rút mọi dây motor. Nạp lại chỉ với cáp USB. Bài nhịp tim sẽ cho bạn thấy cùng kiểu reset dưới dạng chữ `hello` lặp lại khi sketch đã chạy. Trong lúc nạp, nó trông như timeout.

GPIO 1 và GPIO 3 là chân UART mà chip USB-serial đang dùng. Nhấp LED trên hai chân đó biến console thành nhiễu. Hôm nay để yên.

## Ví dụ đã làm

Board của Bình là NodeMCU-32S của Hshop, CH340, trên laptop Windows. Lần cắm đầu làm sáng LED nguồn và Device Manager không thêm gì. Cài driver CH340 thì có `COM5`. Sketch ở trên được dán vào Arduino IDE 2, mục board NodeMCU-32S, tốc độ nạp 115200. Lần nạp đầu vẫn hỏng. Một TB6612 từ ca trước còn VM nhảy sang chân 5 V của dev board. Bình rút sợi VM đó, giữ BOOT, nạp lại. Monitor ở 115200 in `hello`, rồi `high` và `low` cùng nhịp với đèn. GPIO 2 khớp silk board này, nên nhánh `#ifndef` và LED thật là cùng một chân. Chỉ đổi monitor xuống 9600 thì khung đầy ký tự rác trong lúc LED vẫn nhấp, tách được lỗi baud khỏi chip chết.

## Lab

1. Chọn Arduino IDE 2 hoặc PlatformIO. Cài đúng một đường, bằng URL hoặc bằng `platformio.ini` ở trên.
2. Cắm cáp dữ liệu. Xác nhận cổng mới: `/dev/ttyUSB0` trên Linux hoặc một `COMx` mới trên Windows. Ghi tên đó.
3. Chọn ESP32 Dev Module hoặc NodeMCU-32S, hoặc `board = esp32dev`. Đặt monitor 115200.
4. Dán sketch. Nếu LED trên silk không phải GPIO 2 và `LED_BUILTIN` vẫn tối, đổi chân và ghi số mới vào `lab-notes.md`.
5. Nạp. Nếu log timeout, giữ BOOT và thử lại một lần. Nếu còn motor hoặc dây VM, rút VM rồi thử lại.
6. Mở monitor ở 115200. Bạn phải thấy một dòng `hello` rồi các dòng `high` / `low` trong lúc LED onboard nhấp. Chép tám dòng vào sổ, kèm tên cổng và chip USB (CH340 hoặc CP2102).

Đạt khi có cái đèn bạn đã nhìn và một đoạn log đã dán. LED nguồn sáng mỗi khi cắm USB không được tính.

An toàn: chỉ USB. Không pin, không motor, không nối VM. Chân 5 V không phải nguồn motor, và một lần kẹt bánh trong lúc nạp đúng là brownout mà lab này bảo bạn gỡ ra.

## Bài tập

1. Viết bốn khóa `platformio.ini` bài này yêu cầu, và viết URL board của Arduino IDE theo trí nhớ.
2. `LED_BUILTIN` để board tối, còn monitor vẫn in `high` và `low`. Bạn kiểm gì trên silk, và vì sao “GPIO 2” là giả thuyết chứ không phải sự thật?
3. Nạp chỉ chạy khi đang giữ BOOT. Nút đó là chân nào, và EN dùng thế nào?
4. Log in `hello` liên tục và không ở lại trong `loop`. Driver motor vẫn trên bàn, VM buộc vào chân 5 V. Rút cái gì, và sự kiện điện nào đang reset chip?
5. LED nhấp và monitor toàn rác. Hai số baud nào đang lệch? Vì sao bản thân chip vẫn ổn?

<details>
<summary>Đáp án</summary>

1. `platform = espressif32`, `board = esp32dev`, `framework = arduino`, `monitor_speed = 115200`. URL board là `https://espressif.github.io/arduino-esp32/package_esp32_index.json`, rồi gói **esp32 by Espressif Systems**.
2. Tìm GPIO của LED onboard trên pinout board của bạn. GPIO 2 là đèn trên nhiều DevKit V1 và nhiều bản clone NodeMCU-32S, board khác thì khác. Đổi hằng số sang chân mà silk ghi, rồi ghi lại.
3. BOOT kéo GPIO 0 xuống thấp để lúc reset chip vào bootloader serial. Giữ BOOT, chạm EN (reset), thả BOOT, và nạp khi chip còn ở chế độ đó. Board có mạch auto-reset chạy tốt thì giấu thao tác này.
4. Rút VM, và rút mọi motor. Dòng thêm làm sụt ray (brownout) và bootloader reset trước khi nạp xong.
5. Sketch ở 115200 còn monitor ở số khác, thường là 9600. LED đang đảo, nên chương trình đang chạy. Sửa tốc độ monitor. Đừng cài lại toolchain.

</details>

## Mua ở Việt Nam

Nếu bo mạch và cáp dữ liệu của bài trước đã được máy tính nhận, không mua thêm. Nếu cổng không bao giờ hiện, thay cáp trước khi thay board. Giá đọc từ listing công khai của Hshop ngày 23 tháng 9 năm 2026.

Board mặc định: [ESP32 NodeMCU-32S CH340, 190 000 ₫](https://hshop.vn/kit-rf-thu-phat-wifi-ble-esp32-nodemcu-32s-ch340-ai-thinker). Board hoàn chỉnh khác: [Vietduino ESP32, 265 000 ₫](https://hshop.vn/mach-phat-trien-vietduino-esp32). [ESP32-S3-WROOM-1 giá 135 000 ₫](https://hshop.vn/mach-thu-phat-wifi-ble-soc-esp32-s3-esp32-s3-wroom-1-chinh-hang-espressif) là module trần và tự nó không hiện thành `/dev/ttyUSB0` hay `COMx`. Cáp: [Ugreen Micro-USB 1 m, 54 000 ₫](https://hshop.vn/cap-micro-usb-to-usb-2-0-dai-1m-cao-cap-60136-chinh-hang-ugreen).

Nếu so shop: [Shopee ESP32 DevKit CH340](https://shopee.vn/search?keyword=esp32%20devkit%20ch340). [Trang DevKitC-32U của Thế Giới IC](https://www.thegioiic.com/esp32-devkitc-32u-module-wifi-bluetooth-2-4ghz) là listing kiểu board; xác nhận đó là dev board có USB và xem anten có phải bản U.FL. [IC Đây Rồi](https://icdayroi.com/) là quầy linh kiện, không phải chỗ lấy module trần rồi gọi là bộ khởi đầu của lab này. Phần còn lại của giỏ robot vẫn ở [chương 00]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %}).

## Đọc thêm

- [Trang board `esp32dev` của PlatformIO](https://docs.platformio.org/en/latest/boards/espressif32/esp32dev.html) — id board trong file ini của bài này.
- [Cài core Arduino cho ESP32](https://docs.espressif.com/projects/arduino-esp32/en/latest/installing.html) — URL board và các bước IDE, từ Espressif.
- [Trang tải tài liệu Espressif](https://www.espressif.com/en/support/download/documents) — datasheet và hướng dẫn thiết kế khi chân LED của bản clone không phải GPIO 2.
