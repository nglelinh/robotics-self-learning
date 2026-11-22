---
layout: post
title: "Lab — nhấp LED, serial và nhịp tim robot"
chapter: "02"
order: 4
owner: "Nguyen Le Linh"
lang: vi
categories: [chapter02]
lesson_type: required
draft: false
---

## Mục tiêu

Bài thực hành này xác nhận bộ công cụ (toolchain) đã cài ở bài trước hoạt động ổn định, đồng thời thay thế đoạn mã nháy LED kiểu chặn (blocking) bằng một vòng lặp không chặn có thể xử lý nhiều tác vụ song song. Bạn sẽ đảo trạng thái LED mỗi 250 ms và in một dòng nhịp tim (heartbeat) mỗi 500 ms gồm mốc thời gian tính bằng mili giây và trạng thái LED. Vòng lặp được viết bằng `millis()` trên ESP32 hoặc `time.ticks_ms()` trên Pico, và bạn chỉ chạy đoạn mã dành cho bo mạch của mình. Qua bài này, bạn giải thích được vì sao không thể dùng `delay(1000)` hay `time.sleep` khi cần giám sát ngưỡng dừng an toàn 300 ms, đồng thời nhận diện được vòng lặp reset, lỗi chọn sai chân LED và lỗi đặt tốc độ monitor ở 9600 baud.

## Cần gì trước khi học

Nếu dùng ESP32, bạn cần đã nạp thành công chương trình từ bài PlatformIO hoặc Arduino IDE, xác định được tên cổng và đặt tốc độ 115200 baud ở cả hai phía. Nếu dùng Pico, bo mạch cần đã cài MicroPython, Thonny hoặc `mpremote` kết nối đúng cổng và đèn LED đã hoạt động với `Pin("LED")` hoặc GPIO 25. Chỉ cần chuẩn bị một trong hai hệ thống; chưa dùng mạch cầu H, pin hay khung xe. Nếu cáp USB có chất lượng kém, bài thực hành này sẽ làm lộ rõ vấn đề.

## Vì sao bài này gắn với Capstone A

Vòng lặp điều khiển từ xa (teleop) ở chương 07 có cấu trúc tương tự vòng nhịp tim này, chỉ thay việc bật tắt LED bằng việc cập nhật hệ số chu kỳ (duty) cho bánh trái và bánh phải qua TB6612. Mốc thời gian giúp bạn kiểm chứng vòng lặp đang chạy đúng chu kỳ thiết kế. Đồng thời, vòng lặp đó phải phát hiện được khoảng 300 ms không có lệnh mới để đưa cả hai duty về 0, và ở lần đầu cho phép duty khác 0, bánh xe phải được nhấc khỏi bàn. Nếu chương trình bị chặn bên trong `delay(1000)`, vi điều khiển không thể kiểm tra tình trạng mất lệnh cho đến khi `delay` kết thúc, khiến bánh xe tiếp tục quay theo mức PWM cũ thêm tới một giây sau khi người điều khiển đã thả nút. Đến chương 08, khi truyền lệnh qua Wi-Fi, cơ chế kiểm tra quá thời gian (timeout) vẫn dựa trên phép so sánh thời gian không chặn như bài này.

## Hai bộ định thời không chặn

Nhịp tim (heartbeat) là dòng thông điệp mà firmware tự động gửi ra theo chu kỳ cố định, bất kể bạn có nhập lệnh hay không. Trong bài này, LED đảo trạng thái mỗi 250 ms nên một chu kỳ sáng–tắt trọn vẹn là 500 ms, tương ứng tần số 2 Hz:

$$
T_{\text{nhấp}} = 2 \times 250\,\mathrm{ms} = 500\,\mathrm{ms}, \qquad f = \frac{1}{0{,}5\,\mathrm{s}} = 2\,\mathrm{Hz}.
$$

Dòng serial được in mỗi 500 ms với hai trường dữ liệu: thời gian mili giây hiện tại và trạng thái LED (`0` hoặc `1`). Trong 5 giây quan sát, bạn sẽ thấy khoảng 10 lần nháy trọn vẹn và khoảng 10 dòng dữ liệu in ra, vì chu kỳ in cũng bằng 500 ms.

Cần lưu ý một hiện tượng lấy mẫu dễ gặp: vì chu kỳ in (500 ms) đúng bằng hai lần chu kỳ đảo đèn (250 ms), nếu hai bộ đếm khởi tạo cùng thời điểm và trạng thái được in ngay sau bước đảo đèn, giá trị ở cột trạng thái có thể lặp lại cùng một số (luôn là `0` hoặc luôn là `1`) dù ngoài thực tế đèn vẫn nháy đều. Hãy quan sát trực tiếp đèn LED để kiểm tra nhịp nháy, và kiểm tra cột mili giây để đánh giá bộ định thời: hiệu giữa hai dòng liên tiếp phải xấp xỉ 500 ms. Nếu cột trạng thái đứng yên nhưng đèn vẫn nháy đúng 2 Hz, chương trình vẫn hoạt động bình thường; không nên chèn thêm `delay` để cố thay đổi cột này.

Hàm lấy thời gian khác nhau tùy nền tảng nhưng cùng một nguyên lý. Trên core Arduino của ESP32, `millis()` đếm số mili giây kể từ lúc khởi động và sẽ tràn bộ đếm (quay vòng về 0) sau:

$$
2^{32}\,\mathrm{ms} \approx 49{,}7\,\text{ngày}.
$$

Phép trừ số nguyên không dấu `now - last` vẫn cho kết quả chính xác ngay cả khi bộ đếm tràn, miễn cả hai biến đều thuộc kiểu `uint32_t`. Trên Pico, `time.ticks_ms()` cũng đếm mili giây, và cần dùng hàm `time.ticks_diff(now, last)` để tính hiệu thời gian thay vì phép trừ thông thường của Python (vốn sẽ sai khi bộ đếm quay vòng). Ở cả hai nền tảng, mốc thời gian tăng đều khoảng 500 ms mỗi dòng là bằng chứng vòng lặp chạy ổn định; ngược lại, nếu con số đột ngột nhảy về giá trị nhỏ — đặc biệt kèm theo dòng tiêu đề khởi động lặp lại — chip đã bị reset.

Bài này loại bỏ hoàn toàn kiểu viết dùng `delay(1000)` hay `time.sleep(1)`. Trong suốt thời gian CPU dừng ở hàm chặn, phép kiểm tra `now - lastCmdMs > 300` không được thực thi: nếu ngưỡng timeout xảy ra sau 50 ms kể từ khi vào `delay(1000)`, lệnh dừng bánh sẽ bị trễ tới 950 ms. Với vòng lặp không chặn, điều kiện được kiểm tra ở mỗi vòng lặp, nên độ trễ sau timeout chỉ bằng thời gian của một chu kỳ vòng lặp — rất nhỏ so với 300 ms. Trong mã mẫu dưới đây, dòng điều khiển động cơ chỉ để dạng chú thích vì trên bàn chưa nối driver.

Chỉ chạy đoạn mã dành cho bo mạch của bạn; đoạn mã còn lại chỉ dùng để đọc tham khảo.

**ESP32 (core Arduino):** đổi hằng số chân nếu nhãn trên mạch không dùng GPIO 2 (hoặc dùng `LED_BUILTIN` nếu đã đối chiếu khớp với bo mạch).

```cpp
const int kLedPin = 2;  // DevKit V1 thường dùng GPIO 2; đối chiếu silk
const uint32_t TOGGLE_MS = 250;
const uint32_t BEAT_MS = 500;

bool ledOn = false;
uint32_t lastToggle = 0;
uint32_t lastBeat = 0;

void setup() {
  pinMode(kLedPin, OUTPUT);
  Serial.begin(115200);
  lastToggle = millis();
  lastBeat = millis();
  Serial.println("heartbeat");
}

void loop() {
  uint32_t now = millis();

  if (now - lastToggle >= TOGGLE_MS) {
    lastToggle = now;
    ledOn = !ledOn;
    digitalWrite(kLedPin, ledOn ? HIGH : LOW);
  }

  if (now - lastBeat >= BEAT_MS) {
    lastBeat = now;
    // ms, state. Sau này cả hai duty bánh đi theo đồng hồ này.
    // Timeout lệnh 300 ms là một phép so ở đây, không phải delay.
    Serial.printf("%lu,%d\n", static_cast<unsigned long>(now), ledOn ? 1 : 0);
  }

  // Capstone A, không phải hôm nay:
  // if (now - lastCmdMs > 300) { cả hai duty TB6612 = 0; }
}
```

**Raspberry Pi Pico (MicroPython):** `"LED"` dùng cho Pico W và Pico 2 W; nhánh dự phòng GPIO 25 dùng cho Pico bản gốc và Pico 2 không W khi firmware chưa hỗ trợ bí danh `"LED"`.

```python
from machine import Pin
import time

try:
    led = Pin("LED", Pin.OUT)   # Pico W, Pico 2 W
except ValueError:
    led = Pin(25, Pin.OUT)      # Pico gốc, Pico 2

TOGGLE_MS = 250
BEAT_MS = 500
led_on = False
last_toggle = time.ticks_ms()
last_beat = time.ticks_ms()

print("heartbeat")
while True:
    now = time.ticks_ms()
    if time.ticks_diff(now, last_toggle) >= TOGGLE_MS:
        last_toggle = now
        led_on = not led_on
        led.value(1 if led_on else 0)
    if time.ticks_diff(now, last_beat) >= BEAT_MS:
        last_beat = now
        # ms, state. Timeout 300 ms đứng cạnh phép thử này.
        print(now, led_on)
    # sau: if time.ticks_diff(now, last_cmd) > 300: cả hai duty = 0
```

Hãy ghi sẵn quy tắc "nhấc bánh khỏi bàn" vào sổ tay ngay từ bây giờ dù chưa lắp khung xe: bất cứ khi nào nạp hoặc thử nghiệm lệnh có thể làm động cơ quay, lốp xe không được chạm mặt bàn để tránh robot tự chạy rơi khỏi bàn. Hiện tại, mạch TB6612 và pin vẫn để nguyên trong hộp linh kiện.

![Thứ tự nguồn: logic trước, nguồn motor sau, bánh nhấc lên]({{ site.imgurl }}/generated/power_order.png)

Sơ đồ minh họa đúng trình tự đang thực hành: nguồn USB và đường 3,3 V ổn định đi trước, được kiểm chứng bằng bài nháy LED và dòng nhịp tim serial; phần driver và pin nằm ở giai đoạn sau.

## Đọc và kiểm tra log

Sau một dòng tiêu đề `heartbeat` duy nhất, hãy chép lại 10 dòng kế tiếp. Dưới đây là mẫu log hoạt động bình thường trên ESP32 (thời gian tính bằng mili giây):

```text
heartbeat
1840,0
2342,0
2843,0
3344,0
3846,0
4347,0
4848,0
5349,0
5851,0
6352,0
```

Giá trị tuyệt đối của dòng đầu tiên phụ thuộc vào thời gian khởi động `setup` và độ trễ mở cổng USB. Điều quan trọng là hiệu giữa các dòng liên tiếp phải xấp xỉ 500 ms (sai lệch vài mili giây là bình thường). Do hai bộ đếm khởi phát cùng lúc và 500 ms đúng bằng hai lần 250 ms, lần in luôn rơi vào cùng một trạng thái nên cột thứ hai lặp lại giá trị `0`; miễn đèn LED vẫn nháy 2 Hz thì đây không phải lỗi kẹt chân. Ngược lại, nếu mốc thời gian quay về số nhỏ hoặc xuất hiện thêm dòng `heartbeat` thứ hai giữa 10 dòng, chip đã bị reset và bài thực hành chưa đạt cho đến khi thu được chuỗi 10 dòng tăng đơn điệu.

Khi không nối động cơ mà bo mạch vẫn reset, hãy kiểm tra cáp USB hoặc các điểm chạm chập (như dây nối vô tình chập từ `3V3` xuống `GND`). Cáp sạc mỏng, kém chất lượng có thể khiến cổng kết nối chập chờn rồi sụt áp. Hãy tháo hết dây nối ngoài, đổi cáp tốt và ghi lại một khối log sạch. Nếu monitor hiển thị toàn ký tự rác trong khi LED vẫn nháy 2 Hz, nguyên nhân là lệch tốc độ baud (chẳng hạn monitor để 9600 còn chương trình là 115200). Nếu cột mili giây tăng đều nhưng đèn không sáng, hãy kiểm tra lại hằng số chân LED theo nhãn mạch (và trên Pico W thì dùng `Pin("LED")` thay vì GPIO 25).

## Ví dụ đã làm

Dũng sử dụng bo mạch ESP32 DevKit cổ điển (LED ở GPIO 2, chip CH340), nạp đoạn mã C++ và mở monitor ở 115200 baud. Lần chạy đầu in hai dòng `heartbeat` trong vòng 6 giây kèm mốc thời gian tụt về gần 200 ms dù không nối động cơ. Nguyên nhân là sợi cáp chỉ sạc hoạt động chập chờn. Sau khi đổi sang cáp dữ liệu, log chỉ hiện một dòng `heartbeat` duy nhất và mốc thời gian tăng đều khoảng 501 ms mỗi dòng, đèn nháy 2 Hz. Dũng dán 10 dòng log vào `lab-notes.md` kèm ghi chú: "Nhấc bánh khỏi bàn trước mọi lệnh điều khiển TB6612; chưa nối VM và pin."

Ở bàn Pico, sinh viên chạy đoạn mã MicroPython với `Pin("LED")` trên Pico W. Giá trị `ticks_ms` tăng đều khoảng 500 ms mỗi dòng, sổ ghi rõ: "Pico W, dùng bí danh LED, không dùng GPIO 25, nhấc bánh khi thử động cơ, chưa nối động cơ."

Dũng cũng ghi thêm phép đối chiếu bên lề giải thích lý do bỏ `delay(1000)`: nếu mất lệnh từ thời điểm $$t = 0$$, hệ thống phải đưa PWM về 0 ngay khi $$t > 300\,\mathrm{ms}$$. Trong `delay(1000)`, điều kiện không được kiểm tra nên mức duty cũ có thể duy trì tới $$t = 1000\,\mathrm{ms}$$, trong khi vòng lặp không chặn sẽ ngắt ngay ở vòng kế tiếp sau mốc 300 ms.

## Lab

1. Mở dự án đã nạp thành công (hoặc phiên MicroPython đang chạy) từ bài trước. Thay chương trình nháy LED kiểu chặn bằng đoạn mã không chặn tương ứng với bo mạch của bạn.
2. Kiểm tra lại chân LED: dùng GPIO 2 hoặc `LED_BUILTIN` nếu khớp nhãn mạch trên ESP32; dùng `Pin("LED")` hoặc GPIO 25 tùy phiên bản Pico.
3. Mở Serial Monitor hoặc REPL ở tốc độ 115200 baud (nếu nền tảng yêu cầu chọn baud). Xác nhận xuất hiện một dòng `heartbeat`, tiếp theo là các dòng cách nhau khoảng 500 ms và đèn nháy 2 Hz.
4. Chép 10 dòng log vào `lab-notes.md`, ghi kèm tên bo mạch, chân LED, quy tắc nhấc bánh và xác nhận chưa nối chân VM hay pin.
5. Nếu dòng `heartbeat` lặp lại, dừng lại kiểm tra cáp hoặc chạm chập phần cứng trước khi chỉnh sửa mã nguồn.

Hoàn thành đến đây là đủ; không gắn thêm Wi-Fi, mạch cầu H hay pin trong bài thực hành này.

## Video tham khảo

- **Xem trước:** [Lập trình ESP32 - Bài 1 - Cách nạp chương trình cho ESP32 bằng Arduino IDE - Tự học lập trình IOT](https://www.youtube.com/watch?v=sJtJJU3c3xE) — Điện thông minh E-smart, tiếng Việt. Hướng dẫn nạp chương trình nháy LED trên ESP32; bước in dòng serial nhịp tim trong bài này là bước tiếp nối ngay sau đó.
- [ESP32 LED + Push Button Tutorial for Beginners | ESP32 GPIO Input & Output](https://www.youtube.com/watch?v=zCzchrkpHzk) — Alvin Pribadi, tiếng Anh. Ví dụ kết hợp nút nhấn và LED trên GPIO, tương ứng với các thao tác vào/ra cơ bản tiếp theo.

## Bài tập

1. Với chu kỳ nháy 500 ms (đảo LED mỗi 250 ms) và chu kỳ in nhịp tim 500 ms, trong 4 giây bạn sẽ quan sát được bao nhiêu chu kỳ nháy trọn vẹn và bao nhiêu dòng nhịp tim?
2. Vì sao cột trạng thái trong log luôn hiển thị `1` nhưng bài thực hành vẫn có thể đạt yêu cầu? Bạn cần kiểm tra những yếu tố nào để xác nhận?
3. Giả sử lệnh dừng an toàn cần kích hoạt sau 300 ms kể từ gói lệnh cuối, nhưng vòng lặp lại dùng `delay(1000)`. Tính từ lúc điều kiện quá thời gian (timeout) trở thành đúng, lệnh đưa duty về 0 có thể bị trễ tối đa bao lâu?
4. Một đoạn log có dòng `heartbeat` thứ hai chen vào giữa dòng 4 và dòng 5, đồng thời cột mili giây tụt từ 2600 xuống 180 dù không nối động cơ. Nêu hai nguyên nhân hợp lý và một nguyên nhân chưa phù hợp để kết luận.
5. Monitor đang đặt ở 9600 baud, màn hình toàn ký tự rác nhưng đèn LED vẫn nháy đều 2 Hz. Bạn cần chỉnh thông số nào, và vì sao không nên vội cài lại core?

<details>
<summary>Đáp án</summary>

1. Trong 4 giây có $$4 / 0{,}5 = 8$$ chu kỳ nháy trọn vẹn và $$4 / 0{,}5 = 8$$ dòng nhịp tim. Dòng đầu tiên có thể trễ nhẹ do thời gian khởi tạo `setup` hoặc REPL, nhưng khoảng cách giữa các dòng liên tiếp phải xấp xỉ 500 ms.
2. Vì chu kỳ in (500 ms) là bội số nguyên của chu kỳ đảo đèn (250 ms), thời điểm lấy mẫu luôn rơi vào cùng một pha nên trạng thái in ra bị lặp lại. Để xác nhận đạt, hãy nhìn trực tiếp đèn LED xem có nháy 2 Hz không và kiểm tra cột mili giây có tăng đều khoảng 500 ms hay không.
3. Trong lúc thực thi `delay(1000)`, phép kiểm tra không chạy nên thời điểm đưa duty về 0 có thể bị trễ tối đa tới 1000 ms sau khi điều kiện timeout đã đúng. Ngược lại, vòng lặp không chặn sẽ xử lý ngay ở lượt lặp đầu tiên sau mốc 300 ms.
4. Chip đang bị reset. Khi không có tải động cơ, hai nguyên nhân hợp lý là cáp USB kém/chập chờn, dây nối ngoài gây chạm chập nguồn (hoặc nút EN bị chạm/nhiễu). Không thể kết luận lỗi do động cơ kéo sụt chân VM vì hiện tại chưa nối dây VM hay động cơ.
5. Chỉnh tốc độ Serial Monitor lên 115200 baud cho khớp với `Serial.begin(115200)`. Đèn LED nháy đều chứng tỏ chương trình đã nạp và đang chạy bình thường; ký tự rác chỉ do lệch tốc độ baud, không phải lỗi hỏng chip hay hỏng core.

</details>

## Mua ở Việt Nam

Bạn không cần mua thêm linh kiện nếu bo mạch và cáp dữ liệu đã hoạt động ổn định. Nếu mạch liên tục reset do dùng cáp chưa rõ nguồn gốc, hãy thay bằng cáp dữ liệu [Ugreen Micro-USB 1 m, 54 000 ₫](https://hshop.vn/cap-micro-usb-to-usb-2-0-dai-1m-cao-cap-60136-chinh-hang-ugreen). Nếu vẫn chưa có bo mạch: [NodeMCU-32S giá 190 000 ₫](https://hshop.vn/kit-rf-thu-phat-wifi-ble-esp32-nodemcu-32s-ch340-ai-thinker) hoặc [Vietduino ESP32 giá 265 000 ₫](https://hshop.vn/mach-phat-trien-vietduino-esp32), tránh chọn module trần [ESP32-S3-WROOM-1 giá 135 000 ₫](https://hshop.vn/mach-thu-phat-wifi-ble-soc-esp32-s3-esp32-s3-wroom-1-chinh-hang-espressif). Với hướng Pico, kết quả tìm kiếm [raspberry pi pico](https://hshop.vn/search?q=raspberry+pi+pico) ngày 23 tháng 9 năm 2026 hiển thị Pico 2 giá 195 000 ₫ và Pico 2 W giá 275 000 ₫ ([Pico 2](https://hshop.vn/mach-raspberry-pi-pico-2-rp2350), [Pico 2 W](https://hshop.vn/mach-raspberry-pi-pico-2-w-rp2350)). Tham khảo thêm trên Shopee: [ESP32 DevKit CH340](https://shopee.vn/search?keyword=esp32%20devkit%20ch340), [Pico 2](https://shopee.vn/search?keyword=raspberry%20pi%20pico%202). Danh sách linh kiện đầy đủ nằm ở [chương 00]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %}).

## Đọc thêm

- [PlatformIO `esp32dev`](https://docs.platformio.org/en/latest/boards/espressif32/esp32dev.html) — cấu hình bo mạch dùng cho đoạn mã C++ trong bài.
- [Cài arduino-esp32](https://docs.espressif.com/projects/arduino-esp32/en/latest/installing.html) — gói thư viện lõi cung cấp hàm `millis()` và `Serial`.
- [MicroPython trên Pico](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html) — tài liệu về `machine.Pin` và `time.ticks_ms()`.
- [Datasheet Pico](https://datasheets.raspberrypi.com/pico/pico-datasheet.pdf) — đối chiếu thông tin GPIO 25 trước khi sử dụng nhánh dự phòng trên các bản không có W.
