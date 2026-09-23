---
layout: post
title: "C++ và MicroPython trên robot"
chapter: "03"
order: 1
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter03
lesson_type: required
draft: false
---

## Mục tiêu

Hết bài này bạn viết được cùng một nhịp tim không chặn trong cả C++ lẫn MicroPython, và chỉ ra đúng dòng lệnh nào khiến ngưỡng im lặng 300 ms bị trễ. Bạn dùng `millis()` trên lõi Arduino và cặp `time.ticks_ms()` với `time.ticks_diff()` trong MicroPython, thay cho `delay(500)` của [nhịp tim chương 02]({% multilang_post_url contents/chapter02/02_04_blink_serial_hello %}). Bạn tính được vì sao một lần ngủ 200 ms làm mốc 300 ms biến mất trên đế vi sai, rồi chọn ngôn ngữ khi thử cảm biến mới và khi cho robot chạy, với điều kiện timeout vẫn nằm trong vòng lặp.

## Kiến thức cần có

Bạn đã có board in mốc mili giây đang tăng và đảo một LED, từ nhịp tim chương 02. Nhánh ESP32 làm việc đó bằng PlatformIO; nhánh Pico làm từ REPL MicroPython. Bạn đổi được số chân khi listing không khớp chữ in trên board. Chưa cần PWM, ngắt, hay mạch cầu. Thói quen cần bỏ nằm ở cuối nhịp tim cũ: `delay(500)` hoặc `sleep` nửa giây chỉ ổn khi sketch không còn việc gì khác phải để ý.

## Vì sao bài này quan trọng

Capstone A là đế hai bánh vi sai. Lệnh teleop sau này thành hai tín hiệu PWM đưa vào TB6612, mỗi bánh một kênh, và chỉ firmware mới buộc cả hai kênh về 0 khi lệnh ngừng tới. Quy tắc sẽ gắn sau rất ngắn: im lặng 300 ms thì cả hai duty bằng 0, và bánh phải được nhấc lên cho tới khi bạn nhìn thấy điều đó. Ngôn ngữ nào không đọc được đồng hồ trong khoảng ấy sẽ giữ nguyên duty cuối sau khi tay điều khiển đã buông. MicroPython và C++ đều làm xong Capstone A. Cái bài này chặn là một lần ngủ "chỉ" 200 ms, đủ dài để bước qua mốc 300 ms.

## Nội dung

Hai ngôn ngữ cùng chạy trên vi điều khiển bạn đã nạp ở chương 02. Chúng dùng chung số GPIO, rail logic 3,3 V, và cổng serial USB. Capstone A không bắt bạn chọn tính cách. Nó bắt vòng lặp cứ hỏi lệnh cuối đã bao nhiêu tuổi.

MicroPython giữ vòng đọc-thực-thi-in ngay trên chip. Bạn dán một hàm, gọi nó, xem dòng in, rồi mới ghi `main.py`. Chu kỳ sửa đó hợp khi dây cảm biến còn đang đoán. Cái giá nằm ở runtime. Bộ thu gom rác thỉnh thoảng dừng chương trình để lấy lại bộ nhớ. Những lần dừng thường vài mili giây, đôi khi vài chục mili giây, và không phải lịch bạn viết. Teleop bằng tay trong môn này nằm quanh 20 đến 50 Hz. Chu kỳ là

$$
T_{20} = \frac{1}{20} = 50\,\mathrm{ms}, \qquad T_{50} = \frac{1}{50} = 20\,\mathrm{ms}.
$$

Một lần thu gom ngắn làm giật một chu kỳ. Bản thân nó không giả vờ rằng đã im lặng đủ 300 ms, miễn là vòng lặp kiểm lại mốc thời gian ngay khi được chạy tiếp. Cùng một khoảng dừng lại rất dở cho giao thức bit-bang tốc độ cao: UART viết bằng phần mềm, hoặc xung cảm biến dày, sẽ rơi cạnh trong lúc bộ thu gom chạy. Đừng dùng MicroPython cho việc đó. Cứ dùng cho teleop tốc độ người nếu bạn không ngủ dài.

C++ trên lõi Arduino, build bằng PlatformIO như chương 02, biên dịch trên laptop rồi nạp một file nhị phân. Ngôn ngữ bạn đang viết không có bộ thu gom rác, và một ngắt là một hàm với cờ kích bạn gọi tên được. Vì vậy encoder sau này dễ suy luận hơn trong C++. Cái giá là chu kỳ sửa: một dòng đổi cũng phải chờ biên dịch và nạp. Sự chờ đó chấp nhận được với robot đang chạy. Nó không phải lý do để giữ `delay()` trong vòng điều khiển "vì nạp đã lâu rồi."

Nhịp tim dưới đây là cùng một hành vi ở cả hai ngôn ngữ. LED đảo mỗi 500 ms, và những vòng không đảo thì rơi thẳng xuống để chỗ kiểm lệnh sau này vẫn chạy. Arduino giữ mốc trong bộ đếm 32 bit không dấu từ `millis()`. Trừ hai giá trị `uint32_t` vẫn đúng khi bộ đếm quay vòng sau khoảng 49,7 ngày. Đừng cất mốc đó trong `int` có dấu. `time.ticks_ms()` của MicroPython cũng quay vòng, theo modulo bạn không được đoán, nên câu hỏi khoảng thời gian hợp lệ duy nhất là `time.ticks_diff(now, last)`.

Trên nhiều bản MicroPython cho ESP32, một `while True` kín hoàn toàn làm runtime đói và có thể kích watchdog. `time.sleep_ms(1)` ở đáy vòng là một nhịp nhường. Đó không phải lỗi. Lỗi là `time.sleep(0.2)`, `time.sleep(1)`, hoặc `delay(200)`. Khi đã có động cơ, vòng điều khiển chỉ được chặn vài mili giây. Nhường 1 ms vẫn xét timeout 300 ms hàng trăm lần trong cửa sổ. Ngủ 200 ms thì xét nó trên một lưới bỏ qua hạn.

```cpp
const int LED_PIN = 2;  // chân LED bạn đã nhấp ở chương 02
const uint32_t BLINK_MS = 500;

uint32_t lastBlink = 0;
bool ledOn = false;

void setup() {
  pinMode(LED_PIN, OUTPUT);
  Serial.begin(115200);
  lastBlink = millis();
  Serial.println("heartbeat, non-blocking");
}

void loop() {
  uint32_t now = millis();
  if (now - lastBlink >= BLINK_MS) {
    lastBlink = now;
    ledOn = !ledOn;
    digitalWrite(LED_PIN, ledOn ? HIGH : LOW);
    Serial.printf("t=%lu led=%d\n", (unsigned long)now, ledOn ? 1 : 0);
  }
  // Chỗ kiểm tuổi lệnh nằm ở vòng này, kể cả vòng không đảo LED.
}
```

```python
from machine import Pin
import time

led = Pin(2, Pin.OUT)  # đổi thành LED chương 02 bạn đã tin
BLINK_MS = 500
last = time.ticks_ms()
led_on = False

print("heartbeat, non-blocking")
while True:
    now = time.ticks_ms()
    if time.ticks_diff(now, last) >= BLINK_MS:
        last = now
        led_on = not led_on
        led.value(1 if led_on else 0)
        print("t", now, "led", 1 if led_on else 0)
    time.sleep_ms(1)  # chỉ nhường; đừng sleep(0.2) khi đã có timeout
```

Đọc hai listing cho tới khi sự tương ứng trở nên nhàm. Mỗi bên cất một mốc, hỏi một câu trừ an toàn khi quay vòng, chỉ đảo khi câu trả lời là có, còn không thì rơi xuống. Chỗ rơi xuống ấy là nơi phép thử 300 ms sẽ ở. Cách chia việc ổn trên bàn này: thử cảm biến mới bằng MicroPython khi dây còn xê dịch, và giao robot chạy bằng C++ nếu thời gian bắt đầu trượt. Ngôn ngữ nào cũng chấp nhận được cho Capstone A khi timeout thực sự nằm trong vòng lặp.

## Ví dụ tính tay

Điều kiện cắt của Capstone A là

$$
\text{cắt cả hai kênh PWM nếu } t - t_{\text{cmd}} \ge 300\,\mathrm{ms}.
$$

Đặt một lần ngủ 200 ms ở đáy vòng thì điều kiện đó chỉ được xét trên lưới 200 ms. Lệnh tới lúc $t = 0$, làm mới $t_{\text{cmd}}$. Vòng lặp ngủ. Các mốc xét là 200 ms, 400 ms, 600 ms. Ở 200 ms tuổi lệnh vẫn dưới ngưỡng, nên TB6612 giữ duty cũ. Lần nhìn kế tiếp là 400 ms:

$$
t_{\text{dừng}} = \left\lceil \frac{300}{200} \right\rceil \times 200 = 400\,\mathrm{ms}.
$$

Code không nhìn thấy mốc 300 ms. Nó tỉnh dậy khi đã trễ

$$
400 - 300 = 100\,\mathrm{ms}.
$$

Trong 100 ms thừa ấy cả hai bánh vẫn mang lệnh tốc độ cuối, đúng ca mà timeout sinh ra để chặn. So 200 với 300 rồi kết luận "ngủ ngắn hơn nên an toàn" là so nhầm cặp. Lần ngủ phải vài mili giây, ngắn bên cạnh chu kỳ 20 ms của dòng 50 Hz, chứ không phải "chỉ cần ngắn hơn timeout." Mười chu kỳ lệnh bị bỏ lỡ nằm gọn trong một giấc 200 ms:

$$
\frac{200\,\mathrm{ms}}{20\,\mathrm{ms}} = 10.
$$

Một lần thu gom rác khoảng 15 ms trên vòng MicroPython còn biết nhường là chuyện khác. Nó kéo dài một chu kỳ teleop. Nó không giấu mốc 300 ms, vì phép kiểm chạy lại ngay khi lần dừng kết thúc. Vì vậy một khoảng dừng của bộ thu gom chấp nhận được ở 20–50 Hz, còn một giấc 200 ms thì không.

## Bài lab

Ở lại LED của chương 02. Đừng thêm động cơ, và đừng đấu TB6612 trong bài này. Bạn đang đo xem vòng lặp có thấy đồng hồ hay không.

1. Nạp listing đúng với board. Trên MicroPython, chạy từ REPL trước khi lưu `main.py`. Cần một dòng boot, rồi các dòng `t=...` khoảng mỗi 500 ms, LED đi theo trường `led`. Thêm một dòng boot nữa nghĩa là reset; chương 02 đã dạy coi đó là lỗi, không phải nhịp nháy.
2. Thêm bộ đếm vòng, in một lần mỗi giây bằng cùng kiểu kiểm không chặn, rồi xóa. Ghi con số vào sổ. Đó là tốc độ của sketch này, không phải hằng số vũ trụ. Vòng MicroPython nhường 1 ms sẽ rơi gần 1000, và đó đúng là nhịp nhường bạn yêu cầu.
3. Nhét `delay(200)` hoặc `time.sleep(0.2)` mỗi vòng. Nhìn LED và bộ đếm. Nhịp vòng lặp sụp, và im lặng 300 ms chỉ được nhận ra trên lưới 200 ms của ví dụ trên.
4. Gỡ lệnh 200 ms trước khi rời bàn. File bạn giữ là nhịp tim không chặn. Trong sổ, ghi ngôn ngữ, số chân, số vòng mỗi giây, và câu "ngủ 200 ms thì robot dừng ở 400 ms."

## Bài tập

1. Vòng không chặn của bạn hoàn thành 25000 lượt trong một giây. Một lần `delay(200)` xóa bao nhiêu lượt, và lần đầu tiên phép thử im lặng 300 ms có thể đúng là lúc nào nếu nó chỉ được xét sau mỗi lần ngủ như vậy?
2. Nhịp MicroPython của một bạn là `time.sleep(0.5)`, đọc serial sau khi ngủ. Kể tên hai lời gọi đồng hồ để LED vẫn đảo mỗi 500 ms trong khi byte serial được xem ở mọi vòng.
3. Lệnh được gửi ở 40 Hz và một lần thu gom khoảng 12 ms xảy ra đúng một lần. Lần dừng đó, một mình nó, có buộc phải dừng robot không? Bạn có chấp nhận cùng khoảng dừng khi bit-bang một giao thức mà mỗi bit rộng 8 µs không?
4. Chiều nay bạn đem lên một cảm biến khoảng cách mới; tuần sau robot chạy bắt đầu trượt mốc 300 ms khi có tải. Mỗi buổi bạn với ngôn ngữ nào, và điều gì phải đã đúng ở cả hai?

<details>
<summary>Gợi ý</summary>

1. Mỗi lượt dài $1/25000$ giây, nên 0,2 s xóa $0{,}2 \times 25000$ lượt. Phép thử trên lưới 200 ms lần đầu đúng ở 400 ms, cùng phép trần trong ví dụ.
2. Cất `last = time.ticks_ms()`. Đảo khi `time.ticks_diff(time.ticks_ms(), last) >= 500`, và đọc byte ở những vòng không đảo. `sleep_ms(1)` là tùy chọn. `sleep(0.5)` là dòng cần xóa.
3. Mười hai mili giây còn xa 300 ms, nên một lần dừng không có nghĩa đường truyền chết. Một bit 8 µs không sống sót qua 12 ms. Đó là ca bit-bang mà MicroPython là công cụ sai.
4. Thử cảm biến bằng MicroPython. Chuyển vòng chạy sang C++ nếu mốc cắt đã trượt. Ở cả hai buổi, timeout phải là một phép so với mốc thời gian, không phải một comment.

</details>

## Đọc thêm

- [Quy tắc ISR của MicroPython](https://docs.micropython.org/en/latest/reference/isr_rules.html) là ràng buộc bạn đụng ngay khi một callback thay REPL. Cùng trang ấy là lý do bài ngắt sau cấm cấp phát trong hàm xử lý.
- [`millis()`](https://www.arduino.cc/reference/en/language/functions/time/millis/) mô tả đồng hồ mili giây không dấu của nhịp C++, kể cả lần quay vòng khoảng 49,7 ngày.
- [PlatformIO](https://docs.platformio.org/) là đường build chương 02 đã dùng cho sketch ESP32. Lần biên dịch dài hơn là cái giá khi bạn rời REPL.
