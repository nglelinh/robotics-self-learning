---
layout: post
title: "Raspberry Pi Pico và MicroPython"
chapter: "02"
order: 3
owner: "Nguyen Le Linh"
lang: vi
categories: [chapter02]
lesson_type: required
draft: false
---

## Mục tiêu

Bạn đưa Pico hoặc Pico 2 vào chế độ BOOTSEL để ổ tên `RPI-RP2` hiện ra, và bạn chép đúng file UF2 MicroPython của con chip đó. Bạn trỏ Thonny, hoặc `mpremote`, vào board và có REPL trả lời `1 + 1`. Bạn nhấp LED onboard ở 2 Hz và in một bộ đếm, dùng `Pin("LED")` trên Pico W hoặc Pico 2 W và GPIO 25 trên Pico gốc. Bạn từ chối file UF2 của RP2040 trên Pico 2. Mọi GPIO giữ ở 3,3 V, và motor chưa được đi dây.

## Cần gì trước khi học

Bạn đã chọn board họ Pico ở bài bản đồ, hoặc bạn đang học toolchain của bàn bên một lần. Bạn copy được file vào ổ USB. Trang này không cần PlatformIO. File đó thuộc đường ESP32. Cần một cáp micro-USB có dây dữ liệu. Giỏ cả robot vẫn là chương 00 ([Hóa đơn linh kiện và cách mua]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %})).

## Vì sao bài này gắn với Capstone A

Nếu Pico là bộ não, file UF2 này và REPL này là ngôn ngữ của firmware teleop chương 07: hai lệnh bánh, PWM sau này sẽ rơi vào TB6612, và một vòng lặp phải nhận ra khoảng 300 ms im lặng rồi ép cả hai duty về không. Lần đầu lệnh đó tồn tại, bánh phải nhấc lên. MicroPython là đường ngắn vào vòng lặp đó, vì bạn hỏi được con chip trước khi tin một file. Pico không có W thì không có Wi-Fi, nên bài radio chương 08 là Pico W, Pico 2 W, hoặc một lần chuyển sang ESP32. Chọn một trình thông dịch dễ chịu không đóng cánh cửa đó, và cũng không có nghĩa hôm nay phải cài ROS.

## BOOTSEL và đúng file UF2

Cả RP2040 lẫn RP2350 đều boot từ ROM trên chip khi bạn yêu cầu. Cách yêu cầu là cơ khí. Rút hẳn board. Giữ nút BOOTSEL. Cắm cáp USB trong lúc nút vẫn đang giữ. Thả BOOTSEL. Một ổ nhớ tên `RPI-RP2` hiện ra, giống một USB nhỏ. Tên đó là bootloader, không phải ổ của laptop. Pico gốc và Pico 2 dùng cùng tên ổ, nên nhãn không cho biết bạn đang cầm chip nào. Tên file UF2 mới cho biết.

Ảnh cho Pico gốc (RP2040) lấy từ trang chính thức [MicroPython cho RPI_PICO](https://micropython.org/download/RPI_PICO/). Pico 2 là RP2350 và dùng file khác, từ [MicroPython cho RPI_PICO2](https://micropython.org/download/RPI_PICO2/). Chỉ mục tại [micropython.org/download](https://micropython.org/download/) cũng liệt kê riêng Pico W và Pico 2 W. Chép UF2 vào `RPI-RP2` và chỉ vào ổ đó. Ổ tự rút và chip khởi động lại vào MicroPython. Nó không trở lại thành ổ trừ khi bạn giữ BOOTSEL lần nữa. Việc ổ biến mất là thành công.

Đừng nạp ảnh RP2040 lên Pico 2. Bootloader vẫn có thể nhận bản copy, vì đó chỉ là thả file, rồi board ngồi im không có REPL chạy được. Cách sửa là cùng một cử chỉ: rút, giữ BOOTSEL, cắm, và chép UF2 của RP2350. Ảnh Pico W trên Pico gốc, hoặc ngược lại, cùng một lớp sai. Khớp dòng chữ in trên board, không khớp file bạn cùng lớp vừa dùng.

![Pico gốc: BOOTSEL, USB, LED GPIO 25]({{ site.imgurl }}/wikimedia/Raspberry_Pi_Pico.jpg)

Tìm ba mốc trên ảnh và trên board của bạn trước khi chép firmware: phích micro-USB, nút BOOTSEL, và LED onboard gần cổng USB. Ảnh này là Pico gốc. GPIO 25 là cái đèn. Pico W không dùng chân đó cho đèn.

## REPL, rồi tới cái đèn

Thonny là trình soạn mà menu interpreter nói thật. Cài, mở, và chọn **MicroPython (Raspberry Pi Pico)**. Cổng bên dưới phải là board vừa khởi động lại. Để nguyên thiết lập đó cho ngày mai. Lỗi “hôm qua còn chạy” thường gặp là menu vẫn nhằm vào Python trên laptop. Python của laptop nhận `print` rồi thất bại ở `import machine`, và cảm giác giống Pico hỏng.

Nếu thích terminal, `mpremote` (cài bằng `pip` trong một môi trường cục bộ) mở cùng REPL đó. Một trong hai công cụ là đủ. Đừng để cả hai giữ cổng cùng lúc.

Bấm vào khung shell và gõ:

```python
1 + 1
```

Bạn phải thấy `2` và một dấu nhắc mới. Đó là lời chào serial của đường này. Trong backend Pico của Thonny không có `Serial.begin`. Nếu sau này dùng terminal thô, REPL USB của MicroPython vẫn là thiết bị serial và 115200 là tốc độ thường dùng.

LED onboard là chỗ sinh viên chép sai.

Trên Pico gốc, đèn là GPIO 25. MicroPython gần đây cũng nhận bí danh `"LED"` cho chân đó. Nếu `Pin("LED")` ném `ValueError`, dùng GPIO 25.

Trên Pico W, đèn mắc vào chip vô tuyến CYW43439, không mắc vào GPIO 25. GPIO 25 là chân I/O thường. Muốn sáng LED onboard thì `Pin("LED")`. Ghi GPIO 25 sẽ không thắp đèn, và sau này đó có thể là chân bạn định để trống.

Pico 2, board RP2350 không có W, đi theo cách mắc gốc: LED người dùng là GPIO 25. Pico 2 W đi theo ý Pico W: bí danh `"LED"` mới là đèn, GPIO 25 không phải đèn đó. Quy tắc thực hành là đọc silk rồi chọn constructor. Đừng “sửa” đèn tối bằng cách đưa dây sang driver motor.

Nhịp lab là 2 Hz: sáng 250 ms, tắt 250 ms, nên chu kỳ đủ là 500 ms.

$$
f = \frac{1}{0{,}250\,\mathrm{s} + 0{,}250\,\mathrm{s}} = 2\,\mathrm{Hz}.
$$

```python
from machine import Pin
import time

# Pico W / Pico 2 W: đèn là Pin("LED"), không phải GPIO 25.
# Pico gốc và Pico 2 (không W): đèn là GPIO 25.
try:
    led = Pin("LED", Pin.OUT)
except ValueError:
    led = Pin(25, Pin.OUT)

n = 0
while True:
    led.value(1)
    time.sleep(0.25)
    led.value(0)
    time.sleep(0.25)
    n += 1
    print(n)
```

Chạy từ trình soạn và nhìn đèn trước khi lưu bất cứ thứ gì thành `main.py`. Một `main.py` lỗi cú pháp chạy mỗi lần cấp nguồn và cảm giác như board chết. Nếu gặp, giữ BOOTSEL, lấy lại dấu nhắc, rồi xóa hoặc sửa file. `time.sleep` chấp nhận được trong lần nhấp đầu này vì việc duy nhất là thấy 2 Hz và một bộ đếm. Bài sau bỏ sleep để vòng lặp còn canh được thời gian chờ lệnh 300 ms.

## Nguồn, trong một đoạn

`VBUS` là 5 V từ USB khi cáp đang cắm. `VSYS` là ngõ vào của board và nhận được khoảng 1,8 V đến 5,5 V. USB tới đó qua một diode. `3V3` là ray đã ổn áp. Chân GP là 3,3 V. Năm vôn trên chân GP là cách Pico chết, và 7,4 V từ pin 2S không được đặt lên `3V3` hay `VSYS`. Bạn sẽ đo các ray ở bài sơ đồ chân. Hôm nay không nuôi chúng bằng pin.

## Ví dụ đã làm

Chi có Pico gốc và một cáp điện thoại chưa từng copy file. Lần cắm đầu, BOOTSEL giữ đúng, vẫn không có ổ `RPI-RP2`. Cáp dữ liệu Ugreen làm ổ hiện ra. Chi suýt thả file UF2 của Pico 2 vì đó là file đang mở trong thư mục tải về. Silk ghi Pico, không phải Pico 2, nên file lấy từ trang RPI_PICO. Ổ biến mất. Thonny vẫn báo Python cục bộ, và `import machine` hỏng. Đổi interpreter sang MicroPython (Raspberry Pi Pico) thì có dấu nhắc. `1 + 1` in `2`. `Pin("LED")` chạy trên firmware này và đèn xanh nhấp hai lần mỗi giây. Bộ đếm trong shell tăng một lần mỗi nhịp. Sổ ghi: “Pico gốc, UF2 RP2040, bí danh LED chạy được, GPIO 25 là cùng cái đèn, không Wi-Fi, không motor.”

Bàn bên là Pico 2 W, cùng tên ổ. File RP2040 sẽ sai họ. `Pin("LED")` thắp đèn, và GPIO 25 được ghi là chân trống, không phải LED.

## Lab

1. Rút board. Giữ BOOTSEL. Cắm cáp dữ liệu. Thả BOOTSEL. Xác nhận ổ tên `RPI-RP2`.
2. Tải UF2 khớp board: [RPI_PICO](https://micropython.org/download/RPI_PICO/) cho Pico gốc, [RPI_PICO2](https://micropython.org/download/RPI_PICO2/) cho Pico 2, hoặc file W tương ứng từ [chỉ mục tải](https://micropython.org/download/). Chỉ chép vào `RPI-RP2`. Đợi ổ biến mất.
3. Mở Thonny ở MicroPython (Raspberry Pi Pico), hoặc chạy `mpremote`. Gõ `1 + 1`. Bạn phải thấy `2`.
4. Chạy đoạn nhấp ở trên. LED phải nhấp hai lần mỗi giây và bộ đếm phải tăng: 1, 2, 3, không biến mất vào một lần reboot.
5. Trong `lab-notes.md` ghi silk (Pico, Pico W, Pico 2, hoặc Pico 2 W), trang UF2 đã dùng, và `"LED"` hay `25` đã thắp đèn.

Đạt khi REPL là Pico, không phải laptop, và bạn đã nhìn nhịp 2 Hz. Copy sang một ổ rời khác không đạt, dù file “đã chép xong.”

Các lỗi. BOOTSEL được thả trước khi cắm, nên không có ổ và board nhảy thẳng vào firmware cũ. Cáp chỉ sạc, nên không có ổ cũng không có cổng serial. Sai họ UF2: ảnh RP2040 trên Pico 2, hoặc ảnh W trên board không W. Thonny vẫn ở Python cục bộ, nên `machine` không tồn tại.

An toàn: mọi chân GP chỉ 3,3 V. Lab này không nối pin, motor, hay cảm biến 5 V. `3V3` là ngõ ra. `VSYS` không phải chỗ cho pin 2S.

## Bài tập

1. Viết chuỗi BOOTSEL thành bốn thao tác, và tên ổ phải hiện. Vì sao tên đó không phân biệt được Pico với Pico 2?
2. Đoạn nhấp dùng `Pin(25)` trên Pico W và đèn onboard vẫn tắt. Viết dòng thay, và GPIO 25 trên board đó thực sự là gì?
3. Bạn đã chép `RPI_PICO-....uf2` lên Pico 2. Ổ biến mất và REPL không trở lại. File nào thay vào, và file sai thuộc chip nào?
4. Thonny báo `machine` không tồn tại. Interpreter đang đặt ở đâu?
5. Vì sao bài này cấm 5 V trên chân GP, kể cả “chỉ một sợi echo”?

<details>
<summary>Đáp án</summary>

1. Rút hẳn. Giữ BOOTSEL. Cắm USB trong lúc đang giữ. Thả BOOTSEL. Ổ tên `RPI-RP2`. Pico gốc và Pico 2 đều dùng nhãn đó. Tên file UF2 mới chọn RP2040 hay RP2350.
2. `led = Pin("LED", Pin.OUT)`. Trên Pico W và Pico 2 W, đèn nằm ở chip vô tuyến. GPIO 25 là GPIO thường và không thắp LED onboard.
3. Vào lại BOOTSEL và chép UF2 từ trang RPI_PICO2. File bạn đã dùng là ảnh RP2040 cho Pico gốc. Pico 2 là RP2350.
4. Nó đang nhằm vào Python cục bộ của laptop, hoặc nhằm sai cổng. Đặt MicroPython (Raspberry Pi Pico), hoặc dùng `mpremote` trên cổng của Pico.
5. Chân GP là 3,3 V. Echo 5 V có thể phá chân. Motor và pin 2S chờ driver và chờ bài đường nguồn. Chúng không phải cách thử một cái đèn tối.

</details>

## Mua ở Việt Nam

Mua một board họ Pico và một cáp micro-USB dữ liệu nếu chưa có. Giá dưới đây là lần đọc công khai trên Hshop ngày 23 tháng 9 năm 2026. Trang tìm đã kiểm [raspberry pi pico](https://hshop.vn/search?q=raspberry+pi+pico) hôm đó hiện Pico 2 giá 195 000 ₫ và Pico 2 W giá 275 000 ₫. Trang sản phẩm: [Pico 2, RP2350](https://hshop.vn/mach-raspberry-pi-pico-2-rp2350) và [Pico 2 W](https://hshop.vn/mach-raspberry-pi-pico-2-w-rp2350). Pico 2 không có Wi-Fi sẵn. Pico 2 W thì có. Cáp: [Ugreen Micro-USB 1 m, 54 000 ₫](https://hshop.vn/cap-micro-usb-to-usb-2-0-dai-1m-cao-cap-60136-chinh-hang-ugreen).

Shopee, nếu so shop: [Raspberry Pi Pico 2](https://shopee.vn/search?keyword=raspberry%20pi%20pico%202). Nếu vẫn đang cân ESP32 mặc định, board hoàn chỉnh là [NodeMCU-32S giá 190 000 ₫](https://hshop.vn/kit-rf-thu-phat-wifi-ble-esp32-nodemcu-32s-ch340-ai-thinker) và [Vietduino ESP32 giá 265 000 ₫](https://hshop.vn/mach-phat-trien-vietduino-esp32), không phải [ESP32-S3-WROOM-1 trần giá 135 000 ₫](https://hshop.vn/mach-thu-phat-wifi-ble-soc-esp32-s3-esp32-s3-wroom-1-chinh-hang-espressif). [Trang DevKitC-32U của Thế Giới IC](https://www.thegioiic.com/esp32-devkitc-32u-module-wifi-bluetooth-2-4ghz) là đường kia. [IC Đây Rồi](https://icdayroi.com/) là quầy linh kiện. Giỏ đầy đủ nằm ở [chương 00]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %}).

## Đọc thêm

- [MicroPython trên Raspberry Pi Pico](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html) — ghi chú cài đặt của chính Raspberry Pi cho firmware này.
- [Datasheet Pico](https://datasheets.raspberrypi.com/pico/pico-datasheet.pdf) — GPIO 25, VBUS, VSYS, 3V3, và điện áp cực đại của chân.
- [Trang tải MicroPython](https://micropython.org/download/) — chỉ mục tách file UF2 của RP2040 và RP2350. Dùng trang board, không dùng file đính kèm trên diễn đàn.
