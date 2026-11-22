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

Sau bài này, bạn có thể viết cùng một chương trình nhịp tim không chặn (non-blocking) bằng cả C++ và MicroPython, đồng thời chỉ ra chính xác dòng lệnh nào làm trễ ngưỡng dừng an toàn 300 ms. Bạn sử dụng `millis()` trên lõi Arduino và cặp `time.ticks_ms()` cùng `time.ticks_diff()` trong MicroPython để thay thế cho `delay(500)` của bài [nhịp tim chương 02]({% multilang_post_url contents/chapter02/02_04_blink_serial_hello %}). Bạn cũng tính được vì sao một lệnh chờ 200 ms làm lỡ mốc 300 ms trên xe vi sai, từ đó biết cách chọn ngôn ngữ phù hợp khi thử nghiệm cảm biến mới và khi vận hành robot thực tế.

## Kiến thức cần có

Bạn cần đã có bo mạch in ra mốc thời gian mili giây tăng đều và nháy được một đèn LED từ bài nhịp tim chương 02 (nhánh ESP32 dùng PlatformIO, nhánh Pico dùng REPL MicroPython). Bạn biết đổi số chân LED khi mã mẫu không khớp với nhãn in trên bo mạch. Bài này chưa dùng PWM, ngắt hay mạch cầu H; thói quen cần bỏ là dùng `delay(500)` hoặc `sleep` kéo dài nửa giây, vốn chỉ phù hợp khi chương trình không phải giám sát thêm tác vụ nào khác.

## Vì sao bài này quan trọng

Capstone A sử dụng khung xe hai bánh vi sai: các lệnh điều khiển từ xa (teleop) được chuyển thành hai kênh PWM đưa tới mạch cầu H TB6612, và chính firmware phải chủ động đưa cả hai kênh về 0 khi ngừng nhận lệnh. Quy tắc an toàn rất rõ ràng: sau 300 ms không có lệnh mới, cả hai duty phải về 0 (và bánh xe luôn được nhấc khỏi bàn trong lần kiểm chứng đầu tiên). Bất kỳ chương trình nào không thể kiểm tra đồng hồ trong khoảng thời gian đó sẽ giữ nguyên mức PWM cũ sau khi người điều khiển đã thả nút. Cả MicroPython và C++ đều đáp ứng được Capstone A; điều bài học này loại bỏ là những lệnh chờ chặn như 200 ms, đủ dài để vượt quá mốc 300 ms.

## Nội dung

Cả hai ngôn ngữ đều chạy trên cùng vi điều khiển bạn đã chuẩn bị ở chương 02, dùng chung sơ đồ chân GPIO, đường nguồn logic 3,3 V và cổng serial USB. Yêu cầu cốt lõi của Capstone A không nằm ở sở thích ngôn ngữ mà ở khả năng liên tục kiểm tra xem lệnh gần nhất đã quá hạn hay chưa.

MicroPython duy trì môi trường tương tác đọc–thực thi–in (REPL) trực tiếp trên chip: bạn có thể dán một hàm, gọi thử, xem kết quả ngay rồi mới lưu vào `main.py`. Chu kỳ thử nghiệm ngắn này rất tiện khi đang kiểm tra đấu dây cảm biến mới. Đánh đổi nằm ở trình thực thi: bộ thu gom rác (garbage collector) đôi lúc tạm dừng chương trình trong vài mili giây — thỉnh thoảng vài chục mili giây — ngoài lịch bạn chủ động thiết lập. Tần số gửi lệnh teleop thủ công trong môn học nằm quanh 20 đến 50 Hz, tương ứng chu kỳ:

$$
T_{20} = \frac{1}{20} = 50\,\mathrm{ms}, \qquad T_{50} = \frac{1}{50} = 20\,\mathrm{ms}.
$$

Một lần thu gom rác ngắn có thể làm giật nhẹ một chu kỳ điều khiển, nhưng không tự nó kích hoạt nhầm ngưỡng 300 ms miễn vòng lặp kiểm tra lại mốc thời gian ngay khi chạy tiếp. Tuy nhiên, độ trễ bất ngờ này không phù hợp cho các giao thức tự tạo xung bằng phần mềm (bit-bang) tốc độ cao như UART mềm hay đọc chuỗi xung cảm biến dày đặc vì sẽ làm mất cạnh tín hiệu. Không dùng MicroPython cho các tác vụ đó; ngược lại, nó hoàn toàn dùng tốt cho teleop ở tốc độ thao tác của con người nếu không chèn lệnh ngủ dài.

C++ trên lõi Arduino (biên dịch bằng PlatformIO như chương 02) tạo tệp nhị phân trên máy tính rồi nạp xuống chip. Chương trình không có bộ thu gom rác, còn hàm phục vụ ngắt (ISR) gắn trực tiếp với các cờ kích phần cứng cụ thể nên rất dễ kiểm soát thời gian thực khi đọc encoder về sau. Đánh đổi là mỗi lần sửa mã đều phải chờ biên dịch và nạp lại. Mức chờ này hoàn toàn chấp nhận được khi hoàn thiện firmware chạy robot, và không phải lý do để giữ `delay()` trong vòng điều khiển.

Hai đoạn mã dưới đây thực hiện cùng một hành vi nhịp tim: đảo LED mỗi 500 ms, còn các lượt lặp chưa đến hạn sẽ đi thẳng qua để các kiểm tra lệnh phía sau luôn được thực thi. Trong Arduino C++, `millis()` trả về số nguyên 32-bit không dấu (`uint32_t`), quay vòng sau khoảng 49,7 ngày; phép trừ hai biến `uint32_t` luôn cho hiệu đúng kể cả lúc tràn bộ đếm (không lưu mốc thời gian trong `int` có dấu). Trong MicroPython, `time.ticks_ms()` cũng quay vòng theo chu kỳ nội bộ nên bắt buộc dùng `time.ticks_diff(now, last)` để tính khoảng thời gian.

Trên nhiều bản MicroPython cho ESP32, vòng `while True` chạy kín liên tục có thể làm nghẽn tác vụ nền và kích hoạt bộ định thời giám sát (watchdog). Đặt `time.sleep_ms(1)` ở cuối vòng lặp là cách nhường CPU hợp lý, khác hoàn toàn với `time.sleep(0.2)`, `time.sleep(1)` hay `delay(200)`. Khi đã điều khiển động cơ, vòng lặp không được bị chặn quá vài mili giây: nhường 1 ms vẫn cho phép kiểm tra ngưỡng 300 ms hàng trăm lần, còn ngủ 200 ms sẽ bỏ lỡ hạn dừng.

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

Cấu trúc của hai đoạn mã hoàn toàn tương ứng: lưu mốc thời gian gần nhất, trừ an toàn khi tràn bộ đếm, chỉ đảo LED khi đủ hạn và tiếp tục vòng lặp ở mọi lượt còn lại. Phần chạy tiếp đó chính là nơi đặt phép kiểm tra 300 ms. Một cách phân công hiệu quả là dùng MicroPython khi cần thử nhanh cảm biến mới, và chuyển sang C++ khi hệ thống vận hành chính thức hoặc đòi hỏi tính định thời chặt chẽ hơn. Cả hai ngôn ngữ đều hợp lệ cho Capstone A miễn phép kiểm tra quá thời gian thực sự hoạt động trong vòng lặp.

## Ví dụ tính tay

Điều kiện ngắt an toàn của Capstone A là:

$$
\text{cắt cả hai kênh PWM nếu } t - t_{\text{cmd}} \ge 300\,\mathrm{ms}.
$$

Nếu đặt một lệnh ngủ 200 ms ở cuối vòng lặp, điều kiện trên chỉ được kiểm tra tại các mốc bội số của 200 ms. Giả sử lệnh cuối tới lúc $t = 0$ (cập nhật $t_{\text{cmd}} = 0$), sau đó vòng lặp ngủ. Các thời điểm kiểm tra kế tiếp là 200 ms, 400 ms, 600 ms. Tại 200 ms, thời gian im lặng vẫn nhỏ hơn 300 ms nên TB6612 giữ nguyên mức PWM cũ. Lần kiểm tra tiếp theo rơi vào 400 ms:

$$
t_{\text{dừng}} = \left\lceil \frac{300}{200} \right\rceil \times 200 = 400\,\mathrm{ms}.
$$

Chương trình đã bỏ qua mốc 300 ms và chỉ dừng khi đã trễ:

$$
400 - 300 = 100\,\mathrm{ms}.
$$

Trong 100 ms thừa đó, cả hai bánh vẫn chạy theo tốc độ cũ — đúng tình huống cơ chế timeout cần ngăn chặn. So sánh 200 ms với 300 ms rồi cho rằng "ngủ ngắn hơn timeout nên an toàn" là sai lầm. Độ trễ mỗi vòng lặp chỉ nên ở mức vài mili giây, nhỏ hơn nhiều so với chu kỳ 20 ms của luồng lệnh 50 Hz; riêng một giấc ngủ 200 ms đã làm lỡ tới:

$$
\frac{200\,\mathrm{ms}}{20\,\mathrm{ms}} = 10
$$

chu kỳ lệnh liên tiếp.

Ngược lại, một lần thu gom rác kéo dài khoảng 15 ms trên vòng lặp MicroPython có nhường CPU chỉ làm chậm một chu kỳ teleop mà không che lấp mốc 300 ms, vì điều kiện timeout được kiểm tra lại ngay khi trình thực thi chạy tiếp. Do đó, khoảng dừng ngắn của bộ thu gom rác có thể chấp nhận được ở tần số 20–50 Hz, còn lệnh ngủ 200 ms thì không.

## Bài lab

Tiếp tục sử dụng đèn LED từ chương 02; không gắn động cơ và không nối TB6612. Mục tiêu là đo khả năng phản hồi theo đồng hồ của vòng lặp.

1. Nạp đoạn mã phù hợp với bo mạch của bạn (trên MicroPython, chạy thử qua REPL trước khi lưu `main.py`). Kiểm tra màn hình chỉ hiện một dòng khởi động duy nhất, tiếp theo là các dòng `t=...` cách nhau khoảng 500 ms đồng bộ với đèn LED. Nếu dòng khởi động xuất hiện lại, đó là lỗi reset cần xử lý như ở chương 02.
2. Thêm một biến đếm số lượt lặp và in ra mỗi giây một lần bằng cùng kỹ thuật không chặn, ghi con số vào sổ rồi xóa phần đếm này đi. (Với MicroPython có `time.sleep_ms(1)`, số lượt mỗi giây sẽ quanh mức 1000.)
3. Chèn thử `delay(200)` hoặc `time.sleep(0.2)` vào cuối vòng lặp rồi quan sát lại tốc độ vòng lặp và đèn LED. Tần suất vòng lặp giảm mạnh, và ngưỡng 300 ms giờ chỉ còn được kiểm tra trên lưới 200 ms như ví dụ tính tay.
4. Xóa lệnh ngủ 200 ms trước khi kết thúc buổi thực hành để giữ lại bản nhịp tim không chặn. Ghi vào sổ ngôn ngữ đã dùng, số chân LED, số lượt lặp mỗi giây và câu ghi nhớ: "ngủ 200 ms thì robot dừng ở 400 ms."

## Video tham khảo

- **Xem trước:** [Get started with PlatformIO and the ESP 32](https://www.youtube.com/watch?v=3ATDCi4ApY4) — John Green Dev, tiếng Anh. Minh họa quy trình biên dịch và nạp C++ qua PlatformIO.
- [Raspberry Pi PICO | Starting With MicroPython + Examples | I2C OLED, ADC, PWM](https://www.youtube.com/watch?v=zlKJ5hvfs6s) — Electronoobs, tiếng Anh. Minh họa chạy trực tiếp tệp MicroPython trên Pico không qua bước biên dịch.

## Bài tập

1. Giả sử vòng lặp không chặn của bạn thực hiện được 25000 lượt mỗi giây. Một lệnh `delay(200)` làm mất bao nhiêu lượt lặp, và nếu phép kiểm tra mất lệnh 300 ms chỉ chạy sau mỗi lần ngủ như vậy thì thời điểm sớm nhất nó kích hoạt là khi nào?
2. Một chương trình MicroPython dùng `time.sleep(0.5)` rồi mới đọc cổng serial. Hãy nêu tên hai hàm đồng hồ cần dùng để LED vẫn đảo mỗi 500 ms trong khi dữ liệu serial được kiểm tra ở mọi lượt lặp.
3. Lệnh điều khiển gửi ở tần số 40 Hz và xảy ra một lần thu gom rác đơn lẻ kéo dài 12 ms. Khoảng dừng đó tự nó có buộc robot phải vào trạng thái dừng an toàn không? Nếu đổi sang bài toán bit-bang một giao thức có độ rộng mỗi bit 8 µs, liệu khoảng dừng 12 ms có chấp nhận được không?
4. Chiều nay bạn cần thử nghiệm nhanh một cảm biến khoảng cách mới; tuần sau robot vận hành thực tế bắt đầu có dấu hiệu trễ mốc 300 ms khi tải nặng. Bạn chọn ngôn ngữ nào cho mỗi tình huống, và điều kiện bắt buộc chung cho cả hai là gì?

<details>
<summary>Gợi ý</summary>

1. Mỗi lượt kéo dài $1/25000$ giây, nên 0,2 s làm mất $0{,}2 \times 25000 = 5000$ lượt lặp. Khi kiểm tra trên lưới 200 ms, mốc đầu tiên thỏa điều kiện $\ge 300$ ms là 400 ms.
2. Lưu `last = time.ticks_ms()`, đảo LED khi `time.ticks_diff(time.ticks_ms(), last) >= 500`, và kiểm tra dữ liệu serial ở mọi vòng lặp (có thể dùng `sleep_ms(1)` nhưng phải xóa `sleep(0.5)`).
3. 12 ms nhỏ hơn nhiều so với 300 ms nên một lần dừng đơn lẻ không làm kích hoạt timeout. Ngược lại, một bit rộng 8 µs chắc chắn bị hỏng khi chương trình dừng 12 ms — đây là trường hợp không dùng MicroPython cho bit-bang.
4. Dùng MicroPython để thử nhanh cảm biến mới và chuyển vòng điều khiển chính sang C++ khi cần định thời ổn định dưới tải. Ở cả hai trường hợp, timeout bắt buộc phải được viết thành phép so sánh thời gian thực sự trong vòng lặp.

</details>

## Đọc thêm

- [Quy tắc ISR của MicroPython](https://docs.micropython.org/en/latest/reference/isr_rules.html) — các ràng buộc cần nắm khi dùng callback ngắt, đồng thời giải thích lý do bài ngắt sắp tới cấm cấp phát bộ nhớ trong ISR.
- [`millis()`](https://www.arduino.cc/reference/en/language/functions/time/millis/) — tài liệu về bộ đếm mili giây không dấu trong Arduino C++ và chu kỳ tràn khoảng 49,7 ngày.
- [PlatformIO](https://docs.platformio.org/) — công cụ biên dịch đã thiết lập từ chương 02 cho ESP32.
