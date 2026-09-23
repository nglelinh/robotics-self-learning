---
layout: post
title: "Ngắt, chống dội tiếp điểm và ISR ngắn"
chapter: "03"
order: 4
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter03
lesson_type: required
draft: false
---

## Mục tiêu

Hết bài này bạn tách được nảy cơ khí của tiếp điểm khỏi một lần nhấn thật, và bạn chỉ đặt một lần gán cờ bên trong hàm phục vụ ngắt. Bạn gắn nút theo `CHANGE` hoặc `FALLING`, để vòng lặp chính canh cửa sổ đứng yên 20 ms, và cho thấy một lần nhấn vật lý chỉ tăng bộ đếm thêm một. Bạn cũng giải thích vì sao `delay()` trong ISR đó đóng băng mọi ngắt khác, và một ISR encoder sau này được phép làm gì: tăng một `volatile uint32_t` rồi trở về.

## Kiến thức cần có

Bài GPIO đã đấu nút từ chân xuống mass với kéo lên bật, và đã từ chối một thay đổi chưa đứng yên 20 ms. Bản đó hỏi liên tục. Bài này chuyển sự kiện "có chuyện" vào một ngắt và để phép thử đứng yên trong vòng lặp bạn dựng ở bài 1, cùng đồng hồ không chặn đã thay [nhịp `delay(500)` của chương 02]({% multilang_post_url contents/chapter02/02_04_blink_serial_hello %}). Bạn dùng nút đã có. Không linh kiện mới, và vẫn không nối động cơ.

## Vì sao bài này quan trọng

Capstone A xóa FAULT bằng một nút và, về sau, đếm encoder bánh trong lúc duty teleop đang được cập nhật. Nếu ISR của nút in, cấp phát, hoặc gọi `delay`, nó giữ vòng lặp lẽ ra phải nhận ra 300 ms im lặng và buộc cả hai kênh TB6612 về 0. Tiếp điểm nảy gây lỗi ngược lại: một cú chạm trông như năm đến ba mươi cạnh, nên cử chỉ "xóa lỗi" kích lại nhiều lần, hoặc số encoder chạy mất trong lúc robot đứng yên, bánh nhấc lên. ISR phải đủ ngắn để vòng timeout vẫn nhận được CPU, và phần chống dội phải sống ở nơi đồng hồ mili giây là hợp lệ.

## Nội dung

Công tắc cơ khí không đóng một lần. Tiếp điểm chạm, bật lại, rồi chạm nữa. Với các nút trong môn này, khoảng nảy thường nằm đâu đó từ 10 ms đến 50 ms, đó là lý do bài GPIO chọn 20 ms làm mặc định trong khoảng ấy. Trong cửa sổ, chân có thể sinh một chùm cạnh. Ngắt trên mỗi cạnh sẽ chạy ISR một lần mỗi cạnh. Người nhấn vẫn tin mình chỉ nhấn một lần.

![Tiếp điểm nảy, rồi một mức ổn]({{ site.imgurl }}/generated/debounce_timeline.png)

Hàm phục vụ ngắt, ISR, là hàm phần cứng gọi khi chân khớp cờ kích bạn đã vũ trang. Nó chen trước vòng lặp chính. Đó là tính năng: một xung ngắn không thể trốn giữa hai lần hỏi nếu chu kỳ hỏi dài hơn xung. Đó cũng là ràng buộc. Trong lúc ISR chạy, việc ngắt khác phải chờ, và trên một lõi thì vòng lặp của bạn không chạy. Vì vậy hàm này ở rất nhỏ. Đặt một cờ `volatile` hoặc tăng một bộ đếm `volatile`, rồi trở về. `volatile` bảo trình biên dịch rằng vòng chính phải thực sự nạp lại biến, vì ISR ghi nó sau lưng trình biên dịch. Đừng gọi `Serial.print` trong ISR. Đừng cấp phát, đừng dựng `String`, và đừng đụng đối tượng Python nếu bạn đang ở MicroPython. [Quy tắc ISR của MicroPython](https://docs.micropython.org/en/latest/reference/isr_rules.html) nói thẳng về cấp phát heap trong handler, và cùng kỷ luật ấy cứu sketch Arduino khỏi một lệnh in cần ngắt UART mà bạn đang chặn.

Vòng lặp chính là nơi thời gian được phép trôi. Nó xóa cờ, rồi áp cùng luật đứng yên 20 ms của bài GPIO: lần đọc thô phải giữ nguyên trước khi một lần nhấn được đếm. Vũ trang chân theo `FALLING` nếu bạn chỉ cần cú nhấn của nút kéo lên, hoặc `CHANGE` nếu bạn cũng muốn cú nhả. `FALLING` khớp với "nhấn nghĩa là thấp." `CHANGE` cũng sẽ thấy nảy trên đường lên, và phép thử đứng yên phải loại phần đó.

Encoder sau này có thể đếm trong ISR, và đó là một chỗ dùng cơ chế này cho đúng, miễn ISR chỉ làm

```cpp
volatile uint32_t encCount = 0;

void IRAM_ATTR onEnc() {
  encCount++;
}
```

Không ước lượng tốc độ bằng số thực, không serial, không chống dội bằng `delay`. Vòng lặp đọc `encCount` vào một biến cục bộ, tính tốc độ, và cập nhật PWM. `IRAM_ATTR` trên ESP32 đặt ISR trong RAM nội để một thao tác flash không làm nó khựng. Hãy dùng nó trên lõi Arduino ESP32.

Lỗi cần từ chối là chống dội làm bên trong ISR bằng `delay`:

```cpp
void IRAM_ATTR badIsr() {
  delay(20);              // chặn lõi; các ISR khác phải chờ
  if (digitalRead(BTN) == LOW) {
    pressFlag = true;
  }
}
```

Bản thân `delay` phụ thuộc ngắt giữ giờ. Gọi nó từ một ISR thì dừng cái đồng hồ mà `delay` đang chờ, hoặc ít nhất đóng băng mọi handler lẽ ra nhận một chân lệnh, một byte UART, hoặc kênh encoder kia. Kể cả một vòng chờ bận 20 ms "có vẻ chạy" bên trong ISR cũng có nghĩa phép kiểm im lặng 300 ms không chạy trong lúc nảy, và hai encoder sẽ mất cạnh suốt khoảng chờ. Cách chia cờ và vòng lặp tồn tại để ISR trở về trong một micro giây và vòng lặp làm việc chờ mà không tắt phần còn lại của chip.

Arduino C++. Bộ đếm chỉ tăng sau khi đường đã ở mức thấp, ổn định, trong 20 ms sau một ngắt cạnh xuống. GPIO 4 là nút của bài GPIO.

```cpp
const int BTN = 4;
const uint32_t DEBOUNCE_MS = 20;

volatile bool fell = false;

int stable = HIGH;
uint32_t lastChange = 0;
uint32_t presses = 0;

void IRAM_ATTR onFall() {
  fell = true;  // không gì khác
}

void setup() {
  pinMode(BTN, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(BTN), onFall, FALLING);
  Serial.begin(115200);
  lastChange = millis();
  Serial.println("presses=0");
}

void loop() {
  uint32_t now = millis();
  int raw = digitalRead(BTN);

  static int lastRaw = HIGH;
  if (raw != lastRaw) {
    lastRaw = raw;
    lastChange = now;
  }

  if (fell) {
    fell = false;  // đã lấy; phép thử đứng yên vẫn là người quyết
  }

  if ((now - lastChange) >= DEBOUNCE_MS && raw != stable) {
    stable = raw;
    if (stable == LOW) {
      presses++;
      Serial.printf("presses=%lu\n", (unsigned long)presses);
    }
  }
}
```

Việc của ngắt là ghi rằng đã thấy một cạnh xuống. Số đếm được in từ vòng lặp, một dòng mỗi lần nhấn đã chấp nhận. Nếu muốn bản xấu để so, hãy comment phép thử `DEBOUNCE_MS` và tăng mỗi khi cờ `fell` được lấy. Một cú nhấn khi đó in nhiều lần. Trên phần cứng này, sinh viên thường thấy một chùm khoảng 5 đến 30 nhịp cho một lần nhấn khi cửa sổ đứng yên bị bỏ. Nút của bạn có thể rơi bất kỳ chỗ nào trong dải đó. Hãy ghi con số bạn thực thấy.

Handler MicroPython có cùng hình. Callback đặt một cờ toàn cục và không cấp phát. Chống dội ở lại trong vòng lặp. Ưu tiên một số nguyên và một boolean đã có sẵn; đừng dựng list hay chuỗi định dạng bên trong handler.

```python
from machine import Pin
import time

fell = False

def on_fall(pin):
    global fell
    fell = True

btn = Pin(4, Pin.IN, Pin.PULL_UP)
btn.irq(trigger=Pin.IRQ_FALLING, handler=on_fall)

DEBOUNCE_MS = 20
last_raw = 1
stable = 1
last_change = time.ticks_ms()
presses = 0
print("presses=0")

while True:
    now = time.ticks_ms()
    raw = btn.value()
    if raw != last_raw:
        last_raw = raw
        last_change = now
    if fell:
        fell = False
    if time.ticks_diff(now, last_change) >= DEBOUNCE_MS and raw != stable:
        stable = raw
        if stable == 0:
            presses += 1
            print("presses", presses)
    time.sleep_ms(1)
```

`Pin.IRQ_FALLING` là cách MicroPython viết cùng một cờ kích. `Pin.IRQ_RISING | Pin.IRQ_FALLING` là `CHANGE`. In bên trong `on_fall` trông tiện và rồi sẽ ném lỗi hoặc làm hỏng heap. Nếu một bạn cùng bàn nói ngắt "tự chết ngẫu nhiên," hãy tìm chỗ cấp phát trong handler trước khi tìm mối hàn.

## Ví dụ tính tay

Một lần nhấn sinh các cạnh ở $t = 0, 3, 7, 12$ ms rồi giữ LOW chắc tới lúc nhả. Không có phép thử đứng yên thì ISR `FALLING` chạy bốn lần, và một công tắc lắm chuyện trong dải 5–30 chỉ có nhiều cạnh hơn trong cùng cửa sổ 10–50 ms. Bộ đếm in 4, hoặc 17, hoặc 30, cho một cử động ngón. Với luật 20 ms, mức thô chưa được chấp nhận cho tới khi nó không đổi kể từ cạnh cuối. Cạnh xuống cuối ở 12 ms, nên mức được tin ở 32 ms, và `presses` tăng 1. Ba cạnh trước đó khởi động lại đồng hồ và không thành các lần đếm riêng.

Nảy lúc nhả bị bỏ qua với bộ đếm vì listing chỉ tăng khi LOW đã ổn. Nó vẫn không được chặn. Một `delay(20)` trong ISR tại $t = 0$ sẽ ngồi trong handler tới 20 ms, bỏ lỡ mọi ngắt khác trong cửa sổ đó và hoãn phép kiểm lệnh 300 ms của vòng lặp cùng 20 ms ấy cộng với những gì đang xếp hàng. Hai mươi mili giây không phải cả timeout, nhưng là một lỗ bạn đục trên vòng lặp duy nhất được phép cắt PWM. Bản encoder của phép tính này khắt khe hơn: các cạnh cách nhau 200 µs không thể đứng sau một `delay` chống dội 20 ms, đó là lý do ISR encoder chỉ tăng biến.

## Bài lab

Dùng dây nút của bài GPIO. Chỉ USB. Không có cực motor trên chân.

1. Nạp bản đã chống dội. Nhấn mười lần, khoảng một lần một giây. Log serial phải hiện `presses=1` tới `presses=10`, và số cuối khớp ngón tay với sai số không. Nếu lệch một, bạn đã đếm đôi một cú nhả hoặc tiếp điểm chưa bao giờ ổn.
2. Vượt qua phép thử 20 ms để mỗi cờ cạnh xuống được lấy thì tăng bộ đếm. Nhấn một lần, dứt khoát. Chờ một cú nhảy vài nhịp, thường đâu đó từ 5 đến 30. Dán cả hai log vào sổ: bản khớp số, và bản chùm.
3. Đừng "sửa" chùm bằng cách đặt `delay(20)` trong `onFall`. Đọc lại listing xấu ở phần nội dung và viết một câu trong sổ: khoảng chờ nằm cạnh `millis()` hoặc `ticks_diff`, không nằm trong ISR.
4. Tùy chọn: chuyển cờ kích sang `CHANGE` và xác nhận một phép thử đứng yên lỏng cũng phản ứng với chùm lúc nhả. Số đếm vẫn chỉ nên tăng một mỗi lần nhấn nếu bạn chỉ tăng khi LOW đã ổn.

## Bài tập

1. Một lần nhấn sinh cạnh xuống ở 0, 2, 5, 9, 14 và 18 ms, rồi giữ LOW. ISR trần sinh bao nhiêu nhịp đếm, và luật 20 ms chấp nhận lần nhấn vào lúc nào?
2. Vì sao `Serial.println` trong `onFall` phá luật "ISR ngắn" dù sketch có vẻ chạy được vài cú nhấn?
3. Một encoder vuông góc sau này cần một bộ đếm. Cái nào thuộc về ISR: cộng một vào `volatile uint32_t`, tính vòng trên phút bằng số thực, hay gọi `ledcWrite`?
4. Hai nút được vũ trang, và ISR của nút A gọi `delay(20)`. Một cạnh xuống tới nút B sau đó 4 ms. ISR của B chạy khi nào, và điều đó nói gì với ngưỡng cắt PWM 300 ms đang sống trong vòng chính?

<details>
<summary>Gợi ý</summary>

1. Sáu cạnh xuống thành sáu nhịp nếu không có bộ lọc. Cạnh cuối ở 18 ms, nên LOW ổn được chấp nhận ở 38 ms và số đã lọc là 1.
2. `Serial` cần bộ đệm và thường cần ngắt UART. Làm việc đó trong ISR của nút kéo dài handler và có thể khóa chết với chính ngắt nó cần. Đặt cờ; in trong `loop`.
3. Chỉ phép tăng thuộc về ISR. Phép toán tốc độ và lệnh PWM đọc bộ đếm từ vòng lặp.
4. B chờ tới khi `delay(20)` của A trở về, nên B chạy trễ khoảng 16 ms. Vòng chính, kể cả phép kiểm im lặng, cũng bị đứng suốt 20 ms đó.

</details>

## Đọc thêm

- [`attachInterrupt`](https://www.arduino.cc/reference/en/language/functions/external-interrupts/attachinterrupt/) mô tả `FALLING`, `RISING` và `CHANGE`, cùng yêu cầu hàm phục vụ phải ngắn.
- [Quy tắc ISR của MicroPython](https://docs.micropython.org/en/latest/reference/isr_rules.html) là ràng buộc tương ứng cho bản callback: không heap, không việc dài, hãy xếp việc thật vào vòng chính.
