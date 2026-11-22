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

Sau bài này, bạn phân biệt được hiện tượng dội cơ khí (bounce) của tiếp điểm với một lần nhấn thật, đồng thời thiết kế hàm phục vụ ngắt (ISR) thật ngắn chỉ làm nhiệm vụ đặt cờ. Bạn cấu hình ngắt nút nhấn theo chế độ `CHANGE` hoặc `FALLING`, để vòng lặp chính xử lý cửa sổ chống dội 20 ms và xác nhận mỗi lần nhấn vật lý chỉ tăng bộ đếm đúng 1 đơn vị. Bạn cũng giải thích được vì sao gọi `delay()` bên trong ISR sẽ làm đóng băng các ngắt khác, và nắm rõ giới hạn của một ISR đọc encoder về sau: chỉ tăng một biến `volatile uint32_t` rồi thoát ngay.

## Kiến thức cần có

Ở bài GPIO, bạn đã đấu nút nhấn từ chân GPIO xuống mass với kéo lên nội và lọc tín hiệu ổn định 20 ms bằng cách đọc liên tục trong vòng lặp. Bài này chuyển việc phát hiện sự kiện cạnh sang ngắt ngoài, còn bước kiểm tra thời gian ổn định vẫn nằm trong vòng lặp không chặn của bài 1 (thay thế kiểu [nhịp tim `delay(500)` của chương 02]({% multilang_post_url contents/chapter02/02_04_blink_serial_hello %})). Bạn dùng lại nút nhấn sẵn có, chưa cần thêm linh kiện hay nối động cơ.

## Vì sao bài này quan trọng

Trên Capstone A, nút nhấn dùng để xóa trạng thái lỗi (FAULT), còn ngắt phần cứng về sau dùng để đếm xung encoder bánh xe trong lúc firmware vẫn đang cập nhật PWM. Nếu một ISR in dữ liệu serial, cấp phát bộ nhớ hoặc gọi `delay()`, nó sẽ chiếm dụng CPU khiến vòng lặp chính không kịp kiểm tra ngưỡng mất lệnh 300 ms để đưa hai kênh TB6612 về 0. Ở chiều ngược lại, nếu không chống dội, một lần nhấn nút có thể tạo ra 5 đến 30 cạnh tín hiệu khiến thao tác xóa lỗi kích hoạt lặp lại nhiều lần. Do đó, ISR phải thật ngắn gọn để vòng giám sát luôn có CPU, còn mọi thao tác chờ theo thời gian phải nằm trong vòng lặp chính.

## Nội dung

Tiếp điểm cơ khí không đóng dứt khoát một lần duy nhất mà thường chạm, nảy ra rồi đóng lại nhiều lần. Với các nút nhấn thông dụng trong môn học, thời gian dội thường kéo dài khoảng 10 ms đến 50 ms — đó là lý do ta chọn ngưỡng lọc mặc định 20 ms. Nếu gắn ngắt trực tiếp lên chân nút mà không lọc, phần cứng sẽ gọi ISR cho từng cạnh dội dù người dùng chỉ nhấn một lần.

![Tiếp điểm nảy, rồi một mức ổn]({{ site.imgurl }}/generated/debounce_timeline.png)

Hàm phục vụ ngắt (ISR — Interrupt Service Routine) được phần cứng tự động gọi ngay khi chân GPIO xuất hiện cạnh khớp với cấu hình, tạm ngắt ngang vòng lặp chính. Nhờ vậy, các xung ngắn không bị bỏ sót giữa hai lượt kiểm tra của vòng lặp. Tuy nhiên, trong lúc ISR chạy, các ngắt khác phải chờ và vòng lặp chính bị tạm dừng (trên lõi đơn). Vì thế, ISR phải thật ngắn: chỉ đặt một cờ `volatile` hoặc tăng một biến đếm `volatile` rồi thoát ngay. Từ khóa `volatile` báo cho trình biên dịch biết biến có thể thay đổi bất ngờ bên ngoài luồng chính nên phải luôn đọc lại từ bộ nhớ. Tuyệt đối không gọi `Serial.print`, không cấp phát bộ nhớ hay tạo đối tượng `String` trong ISR. Với MicroPython, [quy tắc ISR của MicroPython](https://docs.micropython.org/en/latest/reference/isr_rules.html) nghiêm cấm cấp phát bộ nhớ heap bên trong hàm xử lý ngắt; nguyên tắc tương tự trong Arduino giúp tránh xung đột với ngắt UART của `Serial`.

Vòng lặp chính là nơi xử lý thời gian: xóa cờ ngắt rồi áp dụng quy tắc ổn định 20 ms giống bài GPIO để xác nhận lần nhấn. Với nút kéo lên nối xuống mass, chế độ `FALLING` bắt cạnh xuống khi nhấn, còn `CHANGE` bắt cả cạnh xuống khi nhấn lẫn cạnh lên khi nhả (khi đó bộ lọc ổn định sẽ loại bỏ cả xung dội lúc nhả).

Khi làm việc với encoder về sau, ISR chỉ nên thực hiện đúng một thao tác tăng biến đếm:

```cpp
volatile uint32_t encCount = 0;

void IRAM_ATTR onEnc() {
  encCount++;
}
```

Không tính toán tốc độ bằng số thực, không in serial và không chống dội bằng `delay` trong ISR; vòng lặp chính sẽ sao chép `encCount` sang biến cục bộ để tính tốc độ và cập nhật PWM. Trên lõi Arduino ESP32, thuộc tính `IRAM_ATTR` đặt hàm ISR vào bộ nhớ RAM nội để tránh bị gián đoạn khi hệ thống truy cập bộ nhớ flash.

Dưới đây là kiểu viết **sai cần tránh** — chống dội bằng `delay` ngay trong ISR:

```cpp
void IRAM_ATTR badIsr() {
  delay(20);              // chặn lõi; các ISR khác phải chờ
  if (digitalRead(BTN) == LOW) {
    pressFlag = true;
  }
}
```

Hàm `delay` vốn dựa vào ngắt định thời hệ thống; gọi nó bên trong một ISR sẽ làm treo hoặc trì hoãn toàn bộ các ngắt khác (như UART hay kênh encoder còn lại). Ngay cả một vòng lặp chờ bận 20 ms trong ISR cũng làm vòng lặp chính không kiểm tra được timeout 300 ms và khiến encoder mất xung. Tách thành cờ trong ISR và lọc thời gian trong vòng lặp chính giúp ISR thoát chỉ trong vài micro giây mà vẫn không chặn hệ thống.

**Arduino C++ (ESP32):** bộ đếm chỉ tăng sau khi tín hiệu giữ ổn định ở mức `LOW` đủ 20 ms sau cạnh xuống trên GPIO 4.

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

Ngắt chỉ ghi nhận đã có cạnh xuống, còn việc lọc và in kết quả nằm trong `loop()`. Để thấy rõ tác dụng của bộ lọc, bạn có thể tạm bỏ kiểm tra `DEBOUNCE_MS` và tăng `presses` trực tiếp mỗi khi cờ `fell` bật: một lần nhấn trên nút cơ khí thông thường sẽ làm bộ đếm nhảy vọt khoảng 5 đến 30 đơn vị.

**MicroPython:** cấu trúc tương tự — callback chỉ gán một biến cờ toàn cục đã khởi tạo sẵn, không tạo danh sách hay chuỗi định dạng bên trong handler.

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

Trong MicroPython, `Pin.IRQ_FALLING` tương ứng với `FALLING`, còn `Pin.IRQ_RISING | Pin.IRQ_FALLING` tương ứng với `CHANGE`. Nếu đặt lệnh `print` trong `on_fall`, chương trình rất dễ báo lỗi cấp phát bộ nhớ hoặc hoạt động thiếu ổn định.

## Ví dụ tính tay

Giả sử một lần nhấn tạo ra các cạnh xuống tại $t = 0, 3, 7, 12$ ms rồi giữ ổn định ở mức `LOW` cho đến khi nhả. Nếu không chống dội, ISR `FALLING` chạy 4 lần (và với nút dội mạnh hơn có thể lên 5–30 lần trong cửa sổ 10–50 ms), khiến bộ đếm tăng sai nhiều lần cho một thao tác bấm duy nhất. Với bộ lọc 20 ms, ba cạnh đầu chỉ đặt lại mốc thời gian; cạnh cuối xảy ra lúc 12 ms nên mức `LOW` được xác nhận lúc $12 + 20 = 32$ ms và `presses` chỉ tăng đúng 1.

Xung dội lúc nhả không làm tăng bộ đếm vì mã chỉ đếm khi trạng thái ổn định chuyển sang `LOW`. Ngược lại, nếu đặt `delay(20)` trong ISR ngay tại $t = 0$, CPU bị giữ suốt 20 ms, bỏ lỡ mọi ngắt khác và làm trễ vòng kiểm tra timeout 300 ms. Với encoder có các cạnh xung chỉ cách nhau khoảng 200 µs, một khoảng chặn 20 ms sẽ làm mất hàng trăm xung — đó là lý do ISR encoder chỉ được phép tăng biến đếm rồi thoát.

## Bài lab

Giữ nguyên mạch nút nhấn từ bài GPIO, chỉ cấp nguồn USB và không nối động cơ.

1. Nạp chương trình đã có chống dội. Nhấn nút đúng 10 lần (khoảng 1 lần mỗi giây). Serial Monitor phải in lần lượt từ `presses=1` đến `presses=10`, sai số bằng 0. Nếu lệch, kiểm tra lại logic lọc hoặc xem có đếm nhầm cạnh nhả hay không.
2. Tạm bỏ bộ lọc 20 ms để mỗi lần cờ `fell` bật đều tăng bộ đếm. Nhấn dứt khoát một lần và quan sát bộ đếm nhảy vọt (thường từ 5 đến 30 nhịp). Dán cả hai đoạn log (có lọc và không lọc) vào sổ tay để đối chiếu.
3. Không sửa hiện tượng dội bằng cách đặt `delay(20)` trong `onFall`. Ghi rõ vào sổ: phần chờ chống dội phải đặt cạnh `millis()` hoặc `ticks_diff()` trong vòng lặp chính, không đặt trong ISR.
4. *(Tùy chọn)* Đổi chế độ ngắt sang `CHANGE` và xác nhận rằng dù có dội lúc nhả, bộ đếm vẫn chỉ tăng 1 mỗi lần nhấn nếu chỉ đếm khi mức `LOW` đã ổn định.

## Video tham khảo

- **Xem trước:** [What is Switch Bounce and How to Debounce – ATM | Digi-Key Electronics](https://www.youtube.com/watch?v=IvU8m_30iK0) — DigiKey, tiếng Anh. Quan sát dạng sóng dội tiếp điểm trước khi viết ISR.
- [ESP32 LED + Push Button Tutorial for Beginners | ESP32 GPIO Input & Output](https://www.youtube.com/watch?v=zCzchrkpHzk) — Alvin Pribadi, tiếng Anh. Ví dụ nút nhấn trên GPIO ESP32; lưu ý hàm ISR trong bài này phải ngắn gọn hơn các ví dụ xử lý trực tiếp.

## Bài tập

1. Một lần nhấn tạo ra các cạnh xuống tại 0, 2, 5, 9, 14 và 18 ms rồi giữ ổn định ở `LOW`. Nếu không lọc, ISR đếm thành bao nhiêu lần? Với bộ lọc 20 ms, lần nhấn được xác nhận tại thời điểm nào và số đếm sau lọc là bao nhiêu?
2. Vì sao gọi `Serial.println` bên trong `onFall` vi phạm nguyên tắc "ISR ngắn" dù chương trình có thể vẫn chạy được vài lần nhấn đầu?
3. Với một encoder cầu phương (quadrature) ở các chương sau, thao tác nào sau đây được phép đặt trong ISR: tăng biến `volatile uint32_t`, tính tốc độ vòng/phút bằng số thực, hay gọi `ledcWrite`?
4. Hai nút A và B đều gắn ngắt, trong đó ISR của nút A gọi `delay(20)`. Một cạnh xuống xuất hiện trên nút B sau nút A 4 ms. ISR của nút B bị trễ bao lâu, và điều này ảnh hưởng thế nào đến phép kiểm tra timeout 300 ms trong vòng lặp chính?

<details>
<summary>Gợi ý</summary>

1. Không có bộ lọc, 6 cạnh xuống tạo thành 6 lần đếm. Với bộ lọc 20 ms, cạnh cuối ở 18 ms nên trạng thái `LOW` được xác nhận lúc $18 + 20 = 38$ ms và số đếm là 1.
2. `Serial` sử dụng bộ đệm và thường phụ thuộc vào ngắt UART; gọi trong ISR kéo dài thời gian xử lý và có nguy cơ gây khóa chết (deadlock) với chính ngắt UART. Chỉ đặt cờ trong ISR và in ở `loop()`.
3. Chỉ thao tác tăng biến `volatile uint32_t` thuộc về ISR; mọi phép tính tốc độ và lệnh xuất PWM phải thực hiện trong vòng lặp chính.
4. ISR của nút B phải đợi `delay(20)` của nút A kết thúc nên chạy trễ khoảng 16 ms. Toàn bộ vòng lặp chính — bao gồm phép kiểm tra mất lệnh 300 ms — cũng bị chặn suốt 20 ms đó.

</details>

## Đọc thêm

- [`attachInterrupt`](https://www.arduino.cc/reference/en/language/functions/external-interrupts/attachinterrupt/) — tài liệu Arduino về các chế độ `FALLING`, `RISING`, `CHANGE` và yêu cầu giữ ISR ngắn gọn.
- [Quy tắc ISR của MicroPython](https://docs.micropython.org/en/latest/reference/isr_rules.html) — hướng dẫn tránh cấp phát heap và đưa phần xử lý chính về vòng lặp.
