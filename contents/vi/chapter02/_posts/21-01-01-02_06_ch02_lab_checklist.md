---
layout: post
title: "Checklist lab chương 02"
chapter: "02"
order: 6
owner: "Nguyen Le Linh"
lang: vi
categories: [chapter02]
lesson_type: required
draft: false
---

## Mục tiêu

Bạn chỉ khép chương 02 bằng chứng cứ chỉ được bằng tay. Bạn ghi toolchain và chuỗi phiên bản của nó. Bạn cho thấy LED onboard nhấp theo một chu kỳ bạn đã chọn, và bạn dán nhịp tim serial thay vì kể lại. Bạn hoàn thành thẻ chân cho đúng board trên bàn: GPIO nào là LED, và những chân nào là ngõ ra an toàn. Bạn viết hai số đo ray, 3,3 V và 5 V hoặc VBUS. Bạn thêm một câu gọi tên những chân motor chưa được dùng, VM và pin. Nếu một ô trượt, bạn mở lại bài đã dạy nó, thay vì mua một board thứ hai.

## Cần gì trước khi học

Bài 1 đến bài 5 là chứng cứ trang này tiêu thụ. Bạn cần câu quyết định (bo mạch ESP32 hoặc một Pico đã gọi đúng tên), toolchain khớp nó, log nhịp tim hoặc một chỗ trống thành thật, và thẻ chân. Đồng hồ là bắt buộc cho ô đo ray. Giỏ đầy đủ vẫn là chương 00 ([Hóa đơn linh kiện và cách mua]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %})). Đọc lại câu bánh nhấc lên trong sketch nhịp tim để checklist này không “đạt” một robot đã có thể lăn.

## Vì sao bài này gắn với Capstone A

Chương 07 nhờ vi điều khiển này teleop một đế vi sai: hai kênh PWM hướng tới TB6612, pin trên VM, và bánh ở trên không cho đến khi bạn sẵn sàng. Nếu lệnh ngừng khoảng 300 ms, cả hai duty về không. Chương đó giả định các ô trên trang này đã qua với sổ tay. Một sinh viên tới nơi vẫn chưa chắc chân nào là mass sẽ sửa timeout trong lúc chip đang reset. Chương 08 có thể mang cùng teleop đó qua Wi-Fi trên ESP32, và nó sẵn sàng vận chuyển một luồng từ board đang brownout. Đồ thị lúc đó hiện một liên kết “lúc được lúc không.” Cái lúc không là một lần đo bị bỏ, hoặc một sợi VM lẽ ra không được gắn. Checklist này là khoảng dừng để phần mềm sau không giấu một vấn đề điện.

## Sáu ô, mỗi ô một tín vật

Một ô là một điều kiện có chứng cứ, không phải một chủ đề bạn nhớ đã đọc. Chương 02 có sáu ô. Mỗi ô hoặc đạt với một con trỏ vào `lab-notes.md`, hoặc còn mở. Nửa ô (“gần được”) là ô đang mở.

Ô toolchain là một phiên bản bạn đã viết ra. Arduino IDE: phiên bản trong hộp About, cộng phiên bản gói `esp32` đã cài trong Boards Manager. PlatformIO: chuỗi từ `pio --version`, và dòng `board = esp32dev` vẫn còn trong `platformio.ini`. Pico: phiên bản Thonny hoặc `mpremote`, và tên file UF2, kể cả đó là `RPI_PICO` hay `RPI_PICO2`. “Tôi đã cài cái gì đó” không phải phiên bản.

Ô nhấp là một LED onboard bạn đã nhìn, ở một chu kỳ bạn chọn và viết thành số. Chu kỳ của lab nhịp tim là 500 ms, đảo mỗi 250 ms, 2 Hz. Nếu bạn cố ý chọn chu kỳ khác, viết số đó. LED nguồn không được tính. `LED_BUILTIN` không được tính cho đến khi đã đối chiếu silk. Sổ ghi GPIO hoặc bí danh Pico (`"LED"` hoặc 25).

Ô serial là bản dán nhịp tim. Mười dòng, mốc mili giây tăng khoảng bằng chu kỳ bạn đã khai, một banner, không có dòng boot thứ hai trong khối. Các trường là thời gian và trạng thái. Câu “đếm ổn” thì trượt, vì lần so brownout sau này cần đúng cái cầu thang đó. Baud trong sổ là 115200 nếu bạn đang dùng sketch ESP32 của chương này. Monitor còn để 9600 là ô trượt dù LED vẫn nhấp.

Ô thẻ chân là một bản vẽ hoặc một bảng markdown cho board bạn đang có, không phải cho một ảnh ngẫu nhiên. Nó ghi GPIO của LED, ít nhất một ngõ ra an toàn bạn đã kiểm (không phải chân strap bạn định kéo mạnh, không phải chân UART mà chip USB đang dùng, không phải chân nguồn), và các mass. Nhãn chép từ một bản clone khác thì trượt khi chúng lệch header của bạn. Trên Pico W, danh sách ngõ ra an toàn không được gọi GPIO 25 là LED onboard.

Ô đồng hồ là hai con số, chỉ USB, không có pin. Khoảng 4,7 V đến 5,1 V trên chân 5 V hoặc trên VBUS, và khoảng 3,25 V đến 3,35 V trên 3V3. Viết các số. 4,82 V sau diode là một lần đạt khi các chữ số còn nhìn thấy. “5 V ổn” là trượt. Chân 3V3 ở 4,9 V là rút điện, không phải đạt.

Ô chân motor là một câu gọi tên thứ bạn chưa dùng. Câu đạt: “VM trên TB6612 và pin 2S vẫn để hở. Pin không được chạm GPIO, 3V3, 5V/VIN, VSYS, hay VBUS.” Bánh nhấc lên thuộc cùng ghi chú đó. Ô ghi “motor để sau” mà không gọi tên VM và pin thì vẫn mở.

![Checklist dừng trước nguồn motor]({{ site.imgurl }}/generated/power_order.png)

Hình là chuỗi mà các ô đang giữ. USB, một lần nhấp, và một nhịp tim serial là bằng chứng ray logic còn sống. Driver và pin nằm bên phải một vạch chương này không bước qua.

Thứ tự có giá. Thứ tự đưa lên của bài bản đồ là USB, LED onboard, serial 115200, một nút, PWM trên chân không tải, rồi mới driver và pin. Sáu ô của chương này dừng trước driver đó. PWM không tải có thể là bài tập sau. Nó không phải giấy phép kẹp motor vào GPIO vì checklist đã xong.

Nếu kiện hàng chưa tới, bạn được ghi phiên bản toolchain và một thẻ chân canh từ đúng listing đã trả tiền. Để trống nhấp, serial, và hai điện áp, ghi chữ đang chờ. Đừng dán serial tưởng tượng. Một trang khô là cách dùng thời gian chờ hàng. Nó không phải chương đã đạt.

## Khi một ô trượt

Ô trượt thì mở lại bài đã dạy phần chứng cứ còn thiếu.

Không có chuỗi phiên bản: mở About, hoặc chạy `pio --version`, hoặc in implementation của MicroPython từ REPL, rồi viết chữ đó ra. Đó là bài toolchain, ESP32 hoặc Pico, tùy board.

Không nhấp, hoặc nhấp trên một chân chưa nhận dạng: quay lại bài nạp ESP32 hoặc bài UF2 của Pico, rồi tới bài nhịp tim. Đọc silk. GPIO 2 hay gặp trên DevKit V1 và sai trên board khác. Pico W dùng `Pin("LED")`, không dùng GPIO 25.

Serial mất, thành rác, hoặc banner lặp: bài nhịp tim. Đặt 115200. Nếu banner lặp mà không có motor, đổi cáp và gỡ jumper trước khi viết lại câu in. Nếu VM vẫn đang nối, rút VM. Brownout đó không phải lỗi phần mềm.

Thiếu thẻ chân, hoặc chép từ họ board kia: bài sơ đồ chân. Vẽ 5 V hoặc VBUS, 3V3, GND, chân LED, và một ngõ ra an toàn.

Thiếu điện áp, hoặc viết “ổn”: bài sơ đồ chân, chỉ USB. Nếu 3V3 cách xa 3,3 V, dừng. Đừng gắn pin để biết thêm.

Thiếu câu về motor: viết ngay, từ ví dụ đã làm của bài sơ đồ chân. Pin 2S được chạm VM. Nó không được chạm header của vi điều khiển.

Mua ESP32 thứ hai vì một ô đang mở thường chỉ nhân đôi cùng một lỗi cáp. Hãy thay cáp chỉ sạc trước.

## Ví dụ đã làm

Hai sổ, cả hai thành thật.

Board của Hà tới từ tuần trước. Sổ ghi: Arduino IDE 2.3.2 với gói esp32 3.0.7; NodeMCU-32S; CH340 là `COM5`; LED onboard ở GPIO 2, đã đối silk, đảo mỗi 250 ms; mười dòng nhịp tim bước 498 ms đến 505 ms dưới một banner, monitor 115200; thẻ chân có 5V, 3V3, GND, LED GPIO 2, ngõ ra an toàn GPIO 4; đồng hồ 4,91 V và 3,31 V, chỉ USB; câu “VM và pin 2S để hở. Dương pin không chạm 5V, 3V3, hay bất kỳ GPIO nào.” Cả sáu ô đạt. Động cơ TT ở trong hộp. Bánh, khi đã có khung, được nhấc.

Pico 2 của Khoa đang trên xe tải. Sổ ghi: đã cài Thonny 4.1.4, tên UF2 chép từ trang RPI_PICO2 để ảnh RP2040 không phải file sẽ được nạp, thẻ chân canh từ ảnh listing với VBUS, VSYS, 3V3, GND, LED GP25, ngõ ra an toàn GP16, và câu “không có 5 V trên chân GP. VM và pin không nằm trong kiện này.” Nhấp, serial, và hai điện áp là chữ `đang chờ`. Khoa không đánh dấu chương đã xong.

Một sổ thứ ba, bị loại, là sổ bài tập dùng.

## Lab

Mở `lab-notes.md`. Tạo một mục ghi ngày và “cổng chương 02.” Với mỗi ô trong sáu ô, viết ĐẠT cộng chứng cứ, hoặc MỞ cộng bài bạn sẽ làm lại. Nếu chưa có board, đánh dấu nhấp, serial, và đồng hồ là đang chờ, bằng đúng những chữ đó. Đọc mục một lần. Ô nào không chỉ được bằng ngón tay — một chuỗi phiên bản, một dòng serial, một điện áp, một số chân, các chữ VM và pin — thì thành MỞ trước khi lưu.

Chương đạt khi cả sáu ô ĐẠT, có câu bánh nhấc lên, không có motor nối. Lượt khô là toolchain, câu quyết định, và thẻ chân canh từ ảnh, với ba ô đo ghi rõ đang chờ. Không có trạng thái thứ ba tên là “gần đủ.”

## Bài tập

Dùng sổ giả này. Nó không phải một lần đạt.

```text
Ngày: 23 Sep 2026
Board: ESP32 NodeMCU
Toolchain: đã cài Arduino IDE
LED: GPIO 2, hình như có nhấp
Baud monitor: 9600
Serial: thấy vài ký tự, không chép
Ray: 5V ổn, 3.3 ổn
Tiếp: PWM motor từ GPIO 2, sắp gắn pin
```

1. Liệt kê mọi ô sổ này trượt, và tín vật còn thiếu của từng ô.
2. Sketch nhịp tim gọi `Serial.begin(115200)`. Monitor ở 9600 hiện gì, và một thay đổi nào sửa được ô serial?
3. “GPIO 2, hình như có nhấp” là chưa kiểm. Silk phải đúng điều gì thì GPIO 2 mới được là ô nhấp, và bạn viết gì nếu đèn ở chân khác?
4. Viết lại dòng ray và dòng motor để hai ô đó có thể đạt. Đừng bịa điện áp bạn chưa đo. Dùng dạng ô yêu cầu, và đánh dấu số đang chờ nếu chưa dùng đồng hồ.
5. Bạn mở lại bài nào trước, và vì sao một dev board thứ hai là món mua sai?

<details>
<summary>Đáp án</summary>

1. Toolchain: không có chuỗi phiên bản. Nhấp: “hình như” không phải chu kỳ đã chọn và không phải lần đối silk. Serial: không có dòng đã dán, và baud là 9600. Đồng hồ: “ổn” không phải hai con số. Chân motor: sổ định PWM motor từ GPIO 2 và gắn pin, tức là ngược với việc gọi tên VM và pin như những thứ chưa dùng. Thẻ chân vắng mặt hoàn toàn, nên ô ngõ ra an toàn cũng mở.
2. Khung đầy rác hoặc những ký tự suýt là chữ, trong lúc LED vẫn có thể nhấp. Đặt monitor 115200. Đừng sửa sketch xuống 9600 cho khớp thói quen từ tutorial Uno.
3. Silk hoặc sơ đồ hãng phải cho thấy LED onboard ở GPIO 2. Nhiều DevKit V1 thì đúng vậy. Một số board thì không. Nếu đèn ở chỗ khác, viết GPIO đó, nhìn nó nhấp đúng chu kỳ bạn chọn, và để GPIO 2 ra khỏi thẻ cho đến khi bạn biết nó là gì. `LED_BUILTIN` vẫn cần cùng một lần kiểm.
4. Dòng ray đạt thì có chữ số, ví dụ “chỉ USB, chân 5V ____ V, chân 3V3 ____ V, pin chưa nối,” chỗ trống điền từ đồng hồ. Dòng motor đạt: “VM và pin 2S để hở. Pin không được chạm GPIO, 3V3, hay 5V/VIN.” GPIO 2 không phải chân motor.
5. Mở bài nhịp tim trước nếu baud và bản dán còn thiếu là chỗ nghẽn, và bài sơ đồ chân cho các ray cùng câu VM. Board thứ hai lặp lại cùng những ghi chú còn thiếu. Nếu bản thân cổng không có, cáp chỉ sạc mới là món cần thay.

</details>

## Mua ở Việt Nam

Chỉ mua thứ một ô đang mở còn cần. Thiếu cáp dữ liệu: [Ugreen Micro-USB 1 m, 54 000 ₫](https://hshop.vn/cap-micro-usb-to-usb-2-0-dai-1m-cao-cap-60136-chinh-hang-ugreen). Thiếu bộ não: [ESP32 NodeMCU-32S CH340, 190 000 ₫](https://hshop.vn/kit-rf-thu-phat-wifi-ble-esp32-nodemcu-32s-ch340-ai-thinker) hoặc [Vietduino ESP32, 265 000 ₫](https://hshop.vn/mach-phat-trien-vietduino-esp32). [ESP32-S3-WROOM-1 giá 135 000 ₫](https://hshop.vn/mach-thu-phat-wifi-ble-soc-esp32-s3-esp32-s3-wroom-1-chinh-hang-espressif) là module trần và không khép ô toolchain. Đường Pico, giá đọc ngày 23 tháng 9 năm 2026 từ [trang tìm Pico](https://hshop.vn/search?q=raspberry+pi+pico): Pico 2 giá 195 000 ₫ ([trang sản phẩm](https://hshop.vn/mach-raspberry-pi-pico-2-rp2350)) và Pico 2 W giá 275 000 ₫ ([trang sản phẩm](https://hshop.vn/mach-raspberry-pi-pico-2-w-rp2350)). Shopee: [ESP32 DevKit CH340](https://shopee.vn/search?keyword=esp32%20devkit%20ch340), [Pico 2](https://shopee.vn/search?keyword=raspberry%20pi%20pico%202). [DevKitC-32U ở Thế Giới IC](https://www.thegioiic.com/esp32-devkitc-32u-module-wifi-bluetooth-2-4ghz) là trang kiểu board; xác nhận có USB. [IC Đây Rồi](https://icdayroi.com/) là quầy linh kiện. Đừng mua motor hay TB6612 để xong chương 02. Những dòng đó nằm trong [giỏ chương 00]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %}).

## Đọc thêm

- [PlatformIO `esp32dev`](https://docs.platformio.org/en/latest/boards/espressif32/esp32dev.html) — id board mà ô toolchain ESP32 chờ theo mặc định.
- [Cài arduino-esp32](https://docs.espressif.com/projects/arduino-esp32/en/latest/installing.html) — chỗ phiên bản gói trong sổ của bạn xuất phát.
- [Trang tải MicroPython](https://micropython.org/download/) — tên file UF2 mà ô Pico phải ghi, RP2040 và RP2350 tách riêng.
- [Datasheet ESP32](https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf) — đối một “ngõ ra an toàn” với bảng điện trước khi tin pinout trên blog.
