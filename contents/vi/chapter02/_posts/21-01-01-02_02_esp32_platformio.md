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

Trong bài này, bạn sẽ cài đặt một bộ công cụ (toolchain) duy nhất cho ESP32 và tạm bỏ qua lựa chọn còn lại cho đến khi nạp thành công chương trình nháy LED ổn định. Với Arduino IDE 2, bạn thêm đường dẫn quản lý bo mạch của Espressif, cài gói `esp32` và chọn đúng mục ESP32 Dev Module hoặc NodeMCU-32S khớp với nhãn in trên mạch. Với PlatformIO, bạn cấu hình tệp `platformio.ini` với bo mạch `esp32dev` và tốc độ monitor 115200 baud. Bạn dùng macro `LED_BUILTIN` nếu gói phần mềm có định nghĩa sẵn, và chỉ dùng GPIO 2 sau khi đã xác minh bo mạch thực tế mắc đèn ở chân này. Bạn cũng nắm được cách nhận diện các lỗi phổ biến: không hiện cổng kết nối, cáp chỉ sạc, thiếu driver CH340 và sụt áp (brownout) do còn nối nguồn động cơ trong lúc nạp.

## Cần gì trước khi học

Bạn cần đã chốt bo mạch ESP32 làm vi điều khiển chính từ bài trước. Nếu bạn chọn dòng Pico, hãy đọc nhanh bài này để nắm tổng quan rồi chuyển sang bài về Pico. Cài đặt cả hai bộ công cụ trong cùng một buổi rất dễ dẫn đến nhầm lẫn cấu hình bo mạch trong dự án. Về phần cứng, bạn cần một laptop và một sợi cáp USB có hỗ trợ truyền dữ liệu. Danh mục linh kiện đầy đủ nằm ở bài mua sắm chương 00 ([Hóa đơn linh kiện và cách mua]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %})).

## Vì sao bài này gắn với Capstone A

Chương trình điều khiển từ xa (teleop) cho xe vi sai ở chương 07 chạy trực tiếp trên chính vi điều khiển này, thực hiện xuất PWM cho hai bánh qua TB6612, tự ngắt sau khoảng 300 ms không có lệnh và yêu cầu nhấc bánh khi thử nghiệm lần đầu. Firmware đó chỉ đáng tin cậy khi bo mạch của bạn đã nhận được tệp nạp (binary), điều khiển chính xác một chân GPIO đã chọn và gửi được dữ liệu lên máy tính ở đúng tốc độ baud. Phần teleop qua Wi-Fi ở chương 08 cũng sử dụng chung quy trình nạp này. Trước khi bật kết nối không dây, Serial Monitor ở tốc độ 115200 baud là công cụ quan sát chính để kiểm tra hoạt động của hệ thống.

## Chọn một bộ công cụ

Cả Arduino IDE 2 và PlatformIO đều sử dụng chung lõi (core) Arduino của Espressif. Hãy chọn công cụ đã được cài sẵn trên máy thực hành; tuần này chưa yêu cầu dùng ESP-IDF.

Arduino IDE 2 phù hợp nếu bạn ưu tiên thao tác qua giao diện đồ họa. Sau khi cài IDE, mở Preferences (hoặc Settings) và dán đường dẫn sau vào mục Additional Boards Manager URLs:

```text
https://espressif.github.io/arduino-esp32/package_esp32_index.json
```

Tiếp theo, mở Boards Manager, tìm từ khóa `esp32` và cài gói **esp32 by Espressif Systems**. Sau khi cài xong, mở danh sách bo mạch và chọn mục khớp với nhãn in trên mạch: các bản DevKit 30 chân hoặc 38 chân thông dụng chọn **ESP32 Dev Module**, còn bo mạch có nhãn NodeMCU-32S chọn **NodeMCU-32S** nếu có trong danh sách. Chọn đúng cổng serial vừa xuất hiện. Nếu lần nạp đầu báo lỗi đồng bộ (sync) hoặc quá thời gian chờ (timeout), hãy hạ Upload Speed xuống 115200 vì mức mặc định 921600 thường dễ rơi dữ liệu trên cáp dài hoặc một số bản mạch dùng chip CH340.

PlatformIO phù hợp khi bạn muốn quản lý cấu hình bằng tệp văn bản để dễ theo dõi thay đổi (diff). Cài Visual Studio Code, thêm tiện ích PlatformIO IDE và chờ quá trình tải các gói khởi đầu hoàn tất. Tạo dự án mới và cấu hình tệp `platformio.ini` như sau:

```ini
[env:esp32dev]
platform = espressif32
board = esp32dev
framework = arduino
monitor_speed = 115200
```

Đích `esp32dev` áp dụng cho các bo mạch ESP32 cổ điển gồm module họ WROOM và một chip USB-serial rời, tương thích với NodeMCU-32S và hầu hết DevKit V1 dùng trong môn học. Cấu hình này không đúng cho các bo mạch ESP32-S3 sử dụng USB tích hợp sẵn trong chip. Đây cũng là lý do bài trước khuyến nghị mua bo mạch ESP32 cổ điển, trừ khi bạn chủ động điều chỉnh lại cả tệp cấu hình lẫn sơ đồ chân.

## Đèn LED và cổng giao tiếp

`LED_BUILTIN` là macro được định nghĩa sẵn cho một số biến thể bo mạch. Nếu bo mạch bạn chọn có macro này, hãy dùng nó cho bài thử nháy LED đầu tiên; nếu không, dùng GPIO 2 — chân LED tích hợp phổ biến trên nhiều bản DevKit V1 và NodeMCU-32S. Tuy nhiên, đây không phải quy chuẩn bắt buộc cho mọi nhà sản xuất: một số mạch gắn đèn ở chân khác, thậm chí chỉ có đèn báo nguồn không thể điều khiển bằng phần mềm. Hãy đọc nhãn in trên mạch hoặc tra sơ đồ của hãng, ghi số chân vào sổ tay và đổi hằng số nếu GPIO 2 không sáng, thay vì vội cài lại IDE.

Đoạn mã ngắn dưới đây dùng cho bài thực hành này:

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

Tốc độ trong `Serial.begin(115200)` phải khớp với tốc độ trên Serial Monitor. Khi lệch tốc độ baud, màn hình sẽ không im lặng mà hiển thị các ký tự lỗi (rác). Chương trình này tạm dùng `delay` để dễ quan sát ở lần chạy đầu tiên; sang bài nhịp tim, chúng ta sẽ bỏ cấu trúc này vì lệnh dừng an toàn không thể bị chặn bên trong `delay` khi cần kiểm tra ngưỡng 300 ms.

Con chip nằm sát cổng USB không phải ESP32 mà là chip chuyển đổi USB-serial, thường là CH340 hoặc CP2102 trên các bo mạch cổ điển. CP2102 thường được hệ điều hành tự nhận diện. Với CH340 trên Windows, bạn thường phải cài thêm driver CH340 của hãng WCH để cổng COM mới xuất hiện trong Device Manager. Trên Linux, các chip này xuất hiện dưới dạng `/dev/ttyUSB0` (hoặc `ttyUSB1` nếu cắm thêm thiết bị); trên Windows là `COM3`, `COM4` hoặc một tên `COMx` mới. Trên Linux, tài khoản người dùng cần thuộc nhóm `dialout`, và thay đổi này chỉ có hiệu lực sau khi đăng xuất rồi đăng nhập lại.

Cáp USB chỉ sạc không thể dùng để kết nối máy tính: đèn báo nguồn trên mạch vẫn có thể sáng vì dây nguồn còn, nhưng không có dây dữ liệu. Hãy thay bằng cáp từng dùng để chép tệp dữ liệu thành công.

Để nạp chương trình, ESP32 cổ điển cần vào chế độ bootloader serial bằng cách kéo chân GPIO 0 xuống mức thấp tại thời điểm reset. Nút BOOT (đôi khi ghi IO0) điều khiển chân này, còn nút EN, RST hoặc RESET dùng để khởi động lại chip. Phần lớn bo mạch phát triển có mạch tự động kích hoạt chế độ nạp qua tín hiệu DTR và RTS của chip USB-serial. Nếu bo mạch không tự vào chế độ nạp và quá trình nạp bị timeout, hãy giữ nút BOOT, bấm nạp và thả BOOT khi màn hình log báo đang kết nối (`connecting`). Nếu thao tác chưa ổn định, hãy giữ BOOT, nhấn nhả EN, thả BOOT rồi tiến hành nạp ngay sau đó.

## Các nguyên nhân thường gặp khi nạp lỗi

Ba nhóm lỗi sau chiếm phần lớn các trường hợp tưởng nhầm là "bo mạch hỏng" trong bài thực hành này:

- **Chọn sai bo mạch:** Chọn nhầm mục ESP32-S3, C3 hoặc một biến thể khác như "ESP32 Pico Kit" không khớp với NodeMCU-32S sẽ khiến quá trình nạp báo lỗi, hoặc nạp xong nhưng chân điều khiển không đúng như mong đợi. Hãy chọn đúng ESP32 Dev Module, NodeMCU-32S hoặc `board = esp32dev` theo nhãn mạch.
- **Không hiện cổng kết nối:** Kiểm tra cáp trước tiên, sau đó kiểm tra driver CH340 trên Windows hoặc quyền nhóm `dialout` trên Linux. Cũng cần tránh chọn nhầm cổng còn sót lại từ thiết bị khác (chẳng hạn `/dev/ttyACM0` của Pico trong khi ESP32 là `/dev/ttyUSB0`).
- **Chip tự reset trong lúc nạp:** Nếu động cơ hoặc chân VM của mạch cầu H vẫn đang nối vào chân 5 V của bo mạch, dòng tải đột ngột sẽ làm sụt nguồn và ngắt quá trình nạp giữa chừng. Hãy rút hoàn toàn dây VM cùng mọi dây động cơ, chỉ giữ lại cáp USB rồi nạp lại. Trong lúc chạy chương trình (bài nhịp tim), hiện tượng này sẽ làm chữ `hello` in lặp lại liên tục; còn trong lúc nạp, nó biểu hiện thành lỗi timeout.

Lưu ý thêm: GPIO 1 và GPIO 3 là hai chân UART mà chip USB-serial đang sử dụng. Điều khiển nháy LED trên hai chân này sẽ gây nhiễu dữ liệu hiển thị trên Serial Monitor, vì vậy không sử dụng chúng trong bài này.

## Ví dụ đã làm

Bình dùng bo mạch NodeMCU-32S (chip CH340) mua từ Hshop trên laptop Windows. Lần cắm đầu tiên, đèn nguồn sáng nhưng Device Manager không xuất hiện cổng mới. Sau khi cài driver CH340, cổng `COM5` hiện ra. Bình dán đoạn mã ở trên vào Arduino IDE 2, chọn bo mạch NodeMCU-32S và tốc độ nạp 115200, nhưng lần nạp đầu vẫn thất bại do một mạch TB6612 từ ca thực hành trước còn dây VM nối vào chân 5 V của bo mạch. Bình rút dây VM, giữ nút BOOT và nạp lại thành công. Serial Monitor ở 115200 baud in `hello`, sau đó luân phiên `high` và `low` đồng bộ với đèn LED. Vì GPIO 2 khớp với nhãn trên mạch này, nhánh `#ifndef` điều khiển đúng đèn tích hợp. Khi thử đổi tốc độ monitor xuống 9600, màn hình hiện toàn ký tự rác trong khi LED vẫn nháy đều — giúp phân biệt rõ lỗi tốc độ baud với lỗi hỏng chip.

## Lab

1. Chọn Arduino IDE 2 hoặc PlatformIO và chỉ cài đặt đúng một công cụ theo đường dẫn hoặc tệp `platformio.ini` ở trên.
2. Cắm cáp dữ liệu và xác nhận tên cổng mới xuất hiện (`/dev/ttyUSB0` trên Linux hoặc `COMx` trên Windows), ghi lại tên cổng.
3. Chọn bo mạch ESP32 Dev Module, NodeMCU-32S hoặc cấu hình `board = esp32dev`; đặt tốc độ monitor ở 115200 baud.
4. Dán đoạn mã mẫu. Nếu LED theo nhãn mạch không nằm ở GPIO 2 và `LED_BUILTIN` không sáng, sửa lại số chân và ghi chú vào `lab-notes.md`.
5. Tiến hành nạp chương trình. Nếu quá trình nạp bị timeout, giữ nút BOOT và thử lại; nếu còn nối động cơ hoặc dây VM, rút ra hoàn toàn rồi mới nạp lại.
6. Mở Serial Monitor ở 115200 baud. Quan sát một dòng `hello` tiếp theo là các dòng `high` / `low` đồng bộ với nhịp nháy của LED tích hợp. Chép tám dòng log vào sổ tay kèm tên cổng và loại chip USB-serial (CH340 hoặc CP2102).

Bài thực hành đạt khi đèn LED tích hợp nháy theo chương trình bạn nạp và có đoạn log dán kèm; đèn báo nguồn sáng sẵn khi cắm USB không được tính.

An toàn: chỉ cấp nguồn qua cổng USB; không nối pin, động cơ hay dây VM. Chân 5 V trên bo mạch không dùng để cấp nguồn cho động cơ, và dòng kẹt bánh trong lúc nạp chính là nguyên nhân gây sụt áp cần tránh.

## Video tham khảo

- **Xem trước:** [Get started with PlatformIO and the ESP 32](https://www.youtube.com/watch?v=3ATDCi4ApY4) — John Green Dev, tiếng Anh. Hướng dẫn tạo dự án PlatformIO, chọn bo mạch ESP32 và nạp chương trình — đúng bộ công cụ trong bài.
- [Lập trình ESP32 - Bài 1 - Cách nạp chương trình cho ESP32 bằng Arduino IDE - Tự học lập trình IOT](https://www.youtube.com/watch?v=sJtJJU3c3xE) — Điện thông minh E-smart, tiếng Việt. Hướng dẫn nạp chương trình cho ESP32 bằng Arduino IDE bằng tiếng Việt để đối chiếu quy trình kiểm tra bo mạch hoạt động.

## Bài tập

1. Viết lại bốn dòng cấu hình chính trong `platformio.ini` theo yêu cầu của bài và ghi lại đường dẫn quản lý bo mạch ESP32 cho Arduino IDE.
2. Dùng `LED_BUILTIN` nhưng đèn trên mạch không sáng, trong khi Serial Monitor vẫn in `high` và `low`. Bạn cần kiểm tra thông tin gì trên bo mạch, và vì sao "GPIO 2" chỉ là giả thuyết ban đầu chứ không phải mặc định cho mọi mạch?
3. Quá trình nạp chỉ thành công khi giữ nút BOOT. Nút này nối với chân nào, và nút EN đóng vai trò gì trong thao tác nạp thủ công?
4. Serial Monitor in `hello` lặp lại liên tục mà không chạy ổn định trong `loop`, trong khi mạch cầu H vẫn nối dây VM vào chân 5 V. Bạn cần tháo dây nào và hiện tượng điện nào đang khiến chip reset?
5. Đèn LED vẫn nháy bình thường nhưng Serial Monitor toàn ký tự rác. Hai thông số baud nào đang bị lệch nhau, và vì sao có thể kết luận bản thân chip vẫn hoạt động bình thường?

<details>
<summary>Đáp án</summary>

1. Bốn khóa cấu hình: `platform = espressif32`, `board = esp32dev`, `framework = arduino`, `monitor_speed = 115200`. Đường dẫn cho Arduino IDE là `https://espressif.github.io/arduino-esp32/package_esp32_index.json`, sau đó cài gói **esp32 by Espressif Systems**.
2. Cần tra cứu chân GPIO nối với LED tích hợp trên nhãn mạch hoặc sơ đồ chân (pinout) của đúng bo mạch đang dùng. GPIO 2 phổ biến trên nhiều bản DevKit V1 và NodeMCU-32S nhưng không giống nhau trên mọi biến thể. Hãy đổi hằng số sang chân thực tế và ghi chú lại.
3. Nút BOOT kéo chân GPIO 0 xuống mức thấp để chip vào chế độ bootloader serial khi reset. Thao tác thủ công là giữ BOOT, nhấn nhả EN (reset), thả BOOT rồi nạp trong lúc chip đang chờ. Các bo mạch có mạch tự động reset (auto-reset) hoạt động tốt sẽ tự thực hiện bước này.
4. Cần rút dây VM và toàn bộ dây động cơ. Dòng tải làm sụt đường nguồn (brownout), khiến chip reset liên tục trước khi chạy ổn định hoặc nạp xong.
5. Tốc độ baud trong chương trình là 115200, còn tốc độ trên Serial Monitor đang đặt ở giá trị khác (thường là 9600). Việc đèn LED nháy đều chứng tỏ chương trình đang chạy bình thường; chỉ cần chỉnh lại tốc độ trên monitor mà không cần cài lại bộ công cụ.

</details>

## Mua ở Việt Nam

Nếu bo mạch và cáp dữ liệu từ bài trước đã kết nối ổn định với máy tính, bạn không cần mua thêm gì. Nếu cổng kết nối không xuất hiện, hãy ưu tiên thay cáp trước khi nghĩ đến việc đổi bo mạch. Mức giá dưới đây được ghi nhận từ trang công khai của Hshop vào ngày 23 tháng 9 năm 2026.

Bo mạch mặc định: [ESP32 NodeMCU-32S CH340, 190 000 ₫](https://hshop.vn/kit-rf-thu-phat-wifi-ble-esp32-nodemcu-32s-ch340-ai-thinker). Lựa chọn bo mạch hoàn chỉnh khác: [Vietduino ESP32, 265 000 ₫](https://hshop.vn/mach-phat-trien-vietduino-esp32). Lưu ý [ESP32-S3-WROOM-1 giá 135 000 ₫](https://hshop.vn/mach-thu-phat-wifi-ble-soc-esp32-s3-esp32-s3-wroom-1-chinh-hang-espressif) là module trần, không thể tự hiển thị thành `/dev/ttyUSB0` hay `COMx`. Cáp dữ liệu: [Ugreen Micro-USB 1 m, 54 000 ₫](https://hshop.vn/cap-micro-usb-to-usb-2-0-dai-1m-cao-cap-60136-chinh-hang-ugreen).

Nếu so sánh thêm ở các cửa hàng khác: [Shopee ESP32 DevKit CH340](https://shopee.vn/search?keyword=esp32%20devkit%20ch340). [Trang DevKitC-32U của Thế Giới IC](https://www.thegioiic.com/esp32-devkitc-32u-module-wifi-bluetooth-2-4ghz) là mẫu bo mạch phát triển; cần xác nhận có cổng USB và kiểm tra chuẩn đầu nối anten U.FL. [IC Đây Rồi](https://icdayroi.com/) là cửa hàng linh kiện, không nên mua module trần tại đây để dùng làm bộ khởi đầu cho bài thực hành này. Các linh kiện còn lại của robot nằm ở [chương 00]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %}).

## Đọc thêm

- [Trang board `esp32dev` của PlatformIO](https://docs.platformio.org/en/latest/boards/espressif32/esp32dev.html) — tài liệu về mã bo mạch dùng trong tệp `platformio.ini` của bài này.
- [Cài core Arduino cho ESP32](https://docs.espressif.com/projects/arduino-esp32/en/latest/installing.html) — đường dẫn quản lý bo mạch và các bước cài đặt chính thức từ Espressif.
- [Trang tải tài liệu Espressif](https://www.espressif.com/en/support/download/documents) — datasheet và tài liệu thiết kế để tra cứu khi chân LED trên mạch không phải GPIO 2.
