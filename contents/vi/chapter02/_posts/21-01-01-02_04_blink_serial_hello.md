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

Bạn chứng minh toolchain của lab trước vẫn sống, và bạn thay một lần nhấp chặn bằng một vòng lặp làm được nhiều hơn một việc. Bạn đảo LED mỗi 250 ms và in một dòng nhịp tim mỗi 500 ms, gồm thời gian mili giây và trạng thái LED. Bạn viết vòng đó bằng `millis()` trên ESP32 hoặc `time.ticks_ms()` trên Pico, và bạn chỉ chạy listing khớp board của mình. Bạn giải thích được vì sao `delay(1000)` hoặc `time.sleep` không được đứng chắn một lệnh dừng 300 ms sau này. Bạn nhận ra vòng reset, sai chân LED, và monitor còn để ở 9600.

## Cần gì trước khi học

Đường ESP32: một lần nạp đã xong từ bài PlatformIO hoặc Arduino IDE, một cổng bạn gọi được tên, và hai phía cùng 115200. Đường Pico: MicroPython đã ở trên board, Thonny hoặc `mpremote` nhằm đúng Pico, và một cái đèn đã trả lời `Pin("LED")` hoặc GPIO 25. Chỉ cần một trong hai. Không driver, không pin, không khung xe. Nếu cáp đang ở mức tạm được, lab này sẽ phơi nó ra.

## Vì sao bài này gắn với Capstone A

Vòng teleop chương 07 là nhịp tim này, với LED được thay bằng duty bánh trái và duty bánh phải trên TB6612. Mốc thời gian là cách bạn chứng minh vòng lặp đang chạy đúng tốc độ bạn tưởng. Cùng vòng đó phải nhận ra khoảng 300 ms không có lệnh mới và ghi cả hai duty về không. Lần đầu các duty được phép khác không, bánh phải nhấc lên. Sketch dành thời gian bên trong `delay(1000)` thì không thấy sự im lặng cho đến khi `delay` trả về, nên bánh giữ PWM cũ tới một giây sau khi người lái đã buông. Chương 08 có thể đưa cùng các lệnh đó lên Wi-Fi sau. Thời gian chờ vẫn phải là một phép so trong vòng lặp này, không phải một khoảng dừng.

## Hai bộ đếm, không chờ chặn

Nhịp tim ở đây là một dòng firmware phát theo lịch, dù bạn có đang gõ hay không. LED đổi mỗi 250 ms. Một chu kỳ sáng-tắt đủ vì thế là 500 ms, tức 2 Hz:

$$
T_{\text{nhấp}} = 2 \times 250\,\mathrm{ms} = 500\,\mathrm{ms}, \qquad f = \frac{1}{0{,}5\,\mathrm{s}} = 2\,\mathrm{Hz}.
$$

Dòng serial được in mỗi 500 ms và mang hai trường: đồng hồ mili giây, và trạng thái LED là 0 hoặc 1. Bạn sẽ thấy khoảng hai dòng mỗi giây. Nhìn đèn trong năm giây và đếm số lần nhấp trọn. Khoảng mười lần là nhịp 2 Hz. Khoảng mười dòng trong năm giây đó là tốc độ serial khớp, vì chu kỳ in cũng là 500 ms.

Có một cái bẫy lấy mẫu đáng thấy một lần. Chu kỳ in đúng bằng hai lần đảo. Nếu hai bộ đếm xuất phát cùng nhau và bạn in trạng thái ngay sau một lần đảo, cột in có thể lặp cùng một giá trị trong lúc đèn vẫn nhấp. Hãy nhìn đèn để xét nhịp. Hãy nhìn cột mili giây để xét bộ lập lịch: mỗi dòng phải tăng khoảng 500. Sketch dưới đây in theo bộ đếm 500 ms sau khi lần đảo 250 ms đã được áp. Log mẫu cho thấy một lần chạy thật trông thế nào. Nếu cột trạng thái của bạn đứng yên, cái đèn vẫn là bằng chứng của cạnh 250 ms. Sau này bạn có thể in trên mỗi lần đảo. Đừng “sửa” bằng cách nhét `delay`.

Nguồn đồng hồ khác nhau theo board, ý nghĩa thì không. Trên core Arduino của ESP32, `millis()` đếm mili giây từ lúc boot. Nó quay vòng sau

$$
2^{32}\,\mathrm{ms} \approx 49{,}7\,\text{ngày},
$$

tuần này bạn không chạm tới. Phép trừ không dấu `now - last` vẫn đúng qua lần quay đó nếu cả hai giá trị là `uint32_t`. Trên Pico, `time.ticks_ms()` cũng đếm mili giây, và phép trừ hợp lệ là `time.ticks_diff(now, last)`. Phép trừ Python trần sẽ nói dối khi bộ đếm quay vòng. Một trong hai số, mỗi dòng in tăng khoảng 500, là bằng chứng bạn cần. Một số nhảy về giá trị nhỏ, nhất là khi banner boot in lại, có nghĩa chip đã reset.

`delay(1000)` là mẫu mà lab này cho nghỉ. Trong lúc `delay` chạy, CPU không xét `now - lastCmdMs > 300`. Một lệnh dừng đến hạn sau 50 ms kể từ lúc vào `delay` sẽ bị áp trễ 950 ms. `time.sleep(1)` trên Pico cũng vậy. Vòng không chặn kiểm bất đẳng thức mỗi vòng. Phần chuyển động thêm sau timeout là một lần đi qua `loop`, rất nhỏ so với 300 ms, thay vì bằng độ dài của sleep. Dòng motor vẫn là chú thích. Trên bàn không có driver.

Chạy listing của board bạn. Đọc listing kia để biết bàn bên đang thấy gì. Nạp cả hai lên hai board trong một buổi là cách để sổ tay bị tráo.

ESP32, core Arduino. Đổi chân nếu silk không đồng ý với GPIO 2. Nếu gói board định nghĩa `LED_BUILTIN` và macro đó đúng là cái đèn, bạn được dùng. Hằng số dưới đây là dạng viết rõ.

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

Pico, MicroPython. `"LED"` phủ Pico W và Pico 2 W. GPIO 25 phủ Pico gốc và Pico 2 không W khi bí danh không có.

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

Bánh nhấc lên là một câu bạn ghi vào sổ ngay bây giờ, khi chưa có bánh nào được gắn. Nghĩa là lốp không chạm mặt bàn khi có một lệnh có thể làm chúng quay. Robot “chỉ giật một cái” trên bàn sẽ tự đi khỏi bàn. TB6612 và pin ở trong hộp linh kiện.

![Thứ tự nguồn: logic trước, nguồn motor sau, bánh nhấc lên]({{ site.imgurl }}/generated/power_order.png)

Hình là chuỗi mà nhịp tim này đang tập. USB và ray 3,3 V yên lặng đi trước. Một lần nhấp và một dòng serial là bằng chứng. Driver và pin nằm bên phải một vạch bạn chưa bước qua.

## Một log đọc lại được

Sau đúng một banner `heartbeat`, chép mười dòng. Một log ESP32 từ lần chạy khỏe, thời gian theo mili giây:

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

Giá trị tuyệt đối của mốc đầu phụ thuộc `setup` và adapter USB đã trễ bao lâu. Hiệu giữa các dòng phải ngồi gần 500 ms. Vài mili giây trôi là bình thường. Hai bộ đếm trong sketch xuất phát cùng lúc, và 500 ms đúng bằng hai lần đảo, nên lần in cứ rơi vào cùng một cạnh và cột trạng thái lặp lại. Đèn vẫn phải nhấp hai lần mỗi giây. Cột lặp như vậy là đạt khi đèn đúng. Đó không phải chân bị kẹt. Mốc thời gian trở về số nhỏ, hoặc một banner `heartbeat` thứ hai xen giữa mười dòng, có nghĩa bạn đã ghi một lần reset. Lab chưa đạt cho đến khi một đoạn mười dòng sau đó tăng đơn điệu.

Nếu board reset mà không có motor nối, nghi cáp hoặc một chỗ chập, không nghi driver bạn chưa đi dây. Cáp chỉ sạc mỏng có thể làm cổng hiện rồi sụt. Một sợi nhảy từ 3V3 xuống GND là chập và gây cùng việc. Rút mọi jumper, đổi cáp, và lấy một khối log sạch. Baud 9600 đối sketch 115200 để LED vẫn nhấp và khung đầy rác. Sửa monitor. LED tối mà cột mili giây vẫn khỏe là hằng số chân, không phải toolchain: đọc silk, và trên Pico W thì ngừng ghi GPIO 25.

## Ví dụ đã làm

Board chính của Dũng là DevKit ESP32 cổ điển, LED silk ở GPIO 2, CH340, monitor 115200. Sketch là listing C++. Ca đầu in `heartbeat` hai lần trong sáu giây và mốc thời gian khởi động lại gần 200 ms. Không có motor. Cáp là loại chỉ sạc, chỉ thỉnh thoảng được nhận. Một cáp dữ liệu cho một banner và một cầu thang khoảng 501 ms. Đèn nhấp hai lần mỗi giây. Mười dòng vào `lab-notes.md`, cộng câu “bánh nhấc lên trước mọi lệnh TB6612; VM và pin chưa nối.”

Bàn Pico chạy listing MicroPython. `Pin("LED")` chạy trên Pico W. `ticks_ms` tăng khoảng 500. Sổ ghi “Pico W, bí danh LED, không dùng GPIO 25, bánh nhấc, không motor.” Cả hai bàn đã qua cổng. Không bàn nào nạp firmware của bàn kia.

Phép tính Dũng ghi bên lề là lý do `delay(1000)` đã ra khỏi file. Một lệnh im từ $$t = 0$$ phải ép PWM về không khi $$t > 300\,\mathrm{ms}$$. Bên trong `delay(1000)` phép so không chạy, nên duty cuối có thể sống đến $$t = 1000\,\mathrm{ms}$$. Vòng không chặn xét phép so ở vòng kế tiếp sau 300 ms.

## Lab

1. Mở project đã nạp được, hoặc phiên MicroPython đã nhấp được. Thay lần nhấp chặn bằng listing của board bạn. Đừng dán ngôn ngữ kia “cho có.”
2. Xác nhận chân LED: GPIO 2 hoặc `LED_BUILTIN` chỉ khi silk đồng ý. `Pin("LED")` hoặc GPIO 25 như bài Pico.
3. Mở monitor hoặc REPL ở 115200 nơi có baud. Bạn phải thấy một banner `heartbeat`, rồi các dòng cách nhau khoảng 500 ms, và đèn nhấp hai lần mỗi giây.
4. Chép mười dòng vào `lab-notes.md`. Cùng trang đó ghi chân LED, tên board, và câu bánh nhấc lên. Gọi tên VM và pin là những chân và món bạn chưa dùng.
5. Nếu banner lặp, dừng và sửa cáp hoặc chỗ chập trước khi sửa câu lệnh in.

Dừng ở đó. Đừng thêm Wi-Fi, driver, hay pin để log “thật hơn.”

## Bài tập

1. Một nhịp đủ là 500 ms và LED đảo mỗi 250 ms. Trong 4 giây bạn chờ bao nhiêu lần nhấp trọn, và bao nhiêu dòng nhịp tim?
2. Vì sao một cột trạng thái cứ đứng ở `1` vẫn có thể là một lần nhấp đạt? Bạn nhìn cái gì thay vào?
3. Lệnh dừng đến hạn 300 ms sau gói cuối. Vòng lặp đang ở trong `delay(1000)`. Muộn nhất là bao lâu thì duty thực sự về không, tính từ lúc timeout trở thành đúng?
4. Một log có banner `heartbeat` thứ hai giữa dòng 4 và dòng 5, và trường mili giây rơi từ 2600 xuống 180. Không có motor. Nêu hai nguyên nhân hợp và một nguyên nhân chưa hợp.
5. Monitor còn để 9600. LED vẫn nhấp 2 Hz. Bạn đổi gì, và vì sao cài lại core là nước đi đầu sai?

<details>
<summary>Đáp án</summary>

1. Bốn giây chứa $$4 / 0{,}5 = 8$$ lần nhấp trọn, và $$4 / 0{,}5 = 8$$ dòng nhịp tim. Dòng đầu có thể trễ nhẹ vì `setup` hoặc REPL. Khoảng cách giữa các dòng mới là số đo.
2. Chu kỳ in là bội nguyên của chu kỳ đảo, nên một mẫu khóa pha có thể lặp một trạng thái. Đèn phải nhấp hai lần mỗi giây. Cột mili giây phải bước khoảng 500.
3. Phép so không chạy trong lúc delay, nên lần ghi số không có thể muộn tới 1000 ms sau khi timeout đã đúng. Vòng không chặn ghi số không ở vòng đầu tiên sau 300 ms im lặng.
4. Vòng reset. Trên board không tải, nghi cáp hoặc một jumper chập, hoặc nút EN đang nảy. Motor trên VM chưa phải nguyên nhân bạn được phép kết luận, vì VM chưa nối.
5. Đặt monitor 115200 cho khớp `Serial.begin`. LED chứng minh sketch đang chạy. Rác ở sai baud không phải chip hỏng.

</details>

## Mua ở Việt Nam

Lab này không mua gì nếu board và một cáp dữ liệu đã chạy. Nếu nhịp tim bị reset và sợi cáp chưa từng copy file, thay bằng [Ugreen Micro-USB 1 m, 54 000 ₫](https://hshop.vn/cap-micro-usb-to-usb-2-0-dai-1m-cao-cap-60136-chinh-hang-ugreen). Nếu vẫn thiếu board: [NodeMCU-32S giá 190 000 ₫](https://hshop.vn/kit-rf-thu-phat-wifi-ble-esp32-nodemcu-32s-ch340-ai-thinker) hoặc [Vietduino ESP32 giá 265 000 ₫](https://hshop.vn/mach-phat-trien-vietduino-esp32), không phải [ESP32-S3-WROOM-1 trần giá 135 000 ₫](https://hshop.vn/mach-thu-phat-wifi-ble-soc-esp32-s3-esp32-s3-wroom-1-chinh-hang-espressif). Đường Pico: trang tìm [raspberry pi pico](https://hshop.vn/search?q=raspberry+pi+pico) hiện Pico 2 giá 195 000 ₫ và Pico 2 W giá 275 000 ₫ ngày 23 tháng 9 năm 2026 ([Pico 2](https://hshop.vn/mach-raspberry-pi-pico-2-rp2350), [Pico 2 W](https://hshop.vn/mach-raspberry-pi-pico-2-w-rp2350)). Shopee: [ESP32 DevKit CH340](https://shopee.vn/search?keyword=esp32%20devkit%20ch340), [Pico 2](https://shopee.vn/search?keyword=raspberry%20pi%20pico%202). Giỏ đầy đủ là [chương 00]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %}).

## Đọc thêm

- [PlatformIO `esp32dev`](https://docs.platformio.org/en/latest/boards/espressif32/esp32dev.html) — id board đứng sau listing Arduino, nếu bạn đi đường đó.
- [Cài arduino-esp32](https://docs.espressif.com/projects/arduino-esp32/en/latest/installing.html) — core cung cấp `millis` và `Serial`.
- [MicroPython trên Pico](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html) — `machine.Pin` và `time.ticks_ms`.
- [Datasheet Pico](https://datasheets.raspberrypi.com/pico/pico-datasheet.pdf) — xác nhận GPIO 25 trước khi tin nhánh dự phòng trên board không W.
