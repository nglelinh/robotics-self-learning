---
layout: post
title: "Lab — mẫu GPIO cho nút nhấn và LED"
chapter: "03"
order: 2
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter03
lesson_type: required
draft: false
---

## Mục tiêu

Sau bài thực hành này, bạn đấu nối được nút nhấn từ chân GPIO xuống mass (GND) sao cho trạng thái nhả đọc mức cao và trạng thái nhấn đọc mức thấp nhờ cấu hình kéo lên nội (`INPUT_PULLUP` hoặc tương đương trong MicroPython). Bạn biết tính điện trở nối tiếp cho LED trên đường nguồn 3,3 V, viết được chương trình chỉ in cạnh lên và cạnh xuống bằng Arduino C++ và MicroPython, đồng thời chỉ xác nhận thay đổi trạng thái sau khi tín hiệu thô ổn định trong 20 ms. Bạn cũng nhận diện được ba lỗi phổ biến: chân để nổi khi quên kéo lên, LED thiếu điện trở hạn dòng và nút mắc vào 3,3 V mà không có kéo xuống khiến chân luôn đọc mức cao. Bài này chưa cấp điện cho động cơ.

## Kiến thức cần có

Từ bài [nhịp tim chương 02]({% multilang_post_url contents/chapter02/02_04_blink_serial_hello %}), bạn đã thiết lập được Serial Monitor ở 115200 baud và biết đổi chân LED nếu nhãn mạch không dùng GPIO 2. Bài 1 chương này đã thay `delay(500)` bằng đồng hồ không chặn, và các chương trình dưới đây tiếp tục giữ nguyên tắc đó. Linh kiện cần chuẩn bị gồm breadboard, một nút nhấn nhả (tức thời), một LED, điện trở quanh mức 180 Ω và dây nối; chưa cần TB6612, pin hay khung xe.

---

Nghe tưởng chừng quá đơn giản: nối một chiếc nút nhấn vào chân GPIO rồi đọc `digitalRead()` xem là `0` hay `1`! Thế nhưng ngay lần đầu thử trên breadboard, rất nhiều người sửng sốt thấy màn hình Serial tự động nhảy `0, 1, 1, 0, 1` điên cuồng dù ngón tay **chưa hề chạm vào nút nhấn**! Hiện tượng ma quái đó gọi là **chân thả nổi (floating input)** — và cách khắc phục nó chỉ cần đúng một điện trở kéo lên (`INPUT_PULLUP`) và tư duy *logic tích cực mức thấp (active-low)*.

## Bản đồ kiến thức nền: Trạng thái Điện của Chân GPIO (Push-Pull, Floating và Pull-Up)

1. **Chân Thả nổi (Floating Input):** Một chân GPIO ở chế độ `INPUT` có trở kháng đầu vào cực lớn (~hàng chục mega-ohm); khi nút nhấn nhả ra, sợi dây cắm hoạt động y hệt một chiếc **ăng-ten** thu nhiễu điện từ 50 Hz từ lưới điện phòng học, làm điện áp dao động lung tung giữa 0 V và 3,3 V!
2. **Điện trở Kéo lên Nội bộ (`INPUT_PULLUP`) & Logic Active-Low:** Kéo chân GPIO lên 3,3 V qua một điện trở nội bộ ($$R_{\text{pull}} \approx 45\text{ k}\Omega$$ trên ESP32, ~$$50\text{ k}\Omega$$ trên Pico) và nối nút nhấn xuống `GND`. Khi **nhả nút**, chân ổn định ở `HIGH (1)`; khi **nhấn nút**, chân nối thẳng xuống `GND` đọc `LOW (0)` (*active-low*) — loại bỏ hoàn toàn nhiễu thả nổi mà không cần thêm điện trở ngoài!
3. **Ngõ ra Đẩy–Kéo (Push-Pull) & Ranh giới Dòng Cấp/Hút (Source/Sink):** Chân `OUTPUT` dùng cặp MOSFET đẩy lên 3,3 V (`HIGH`) hoặc kéo xuống 0 V (`LOW`); tổng dòng qua tất cả các chân GPIO cùng lúc không được vượt quá giới hạn của cả chip.

### Ví dụ cầm tay chỉ việc: Tính dòng rò qua điện trở kéo lên nội bộ (`INPUT_PULLUP`)

Giả sử bạn dùng chân GPIO 3,3 V của ESP32 với điện trở kéo lên nội bộ $$R_{\text{pull}} = 45\text{ k}\Omega$$ nối tới một nút nhấn khẩn cấp (đầu kia nối `GND`):
- **Khi nhả nút:** mạch hở, dòng tiêu thụ $$I = \mathbf{0\ \mu\text{A}}$$, điện áp tại chân GPIO là $$3.3\text{ V}$$ (`HIGH`).
- **Khi giữ nút nhấn:** dòng chạy từ đường 3,3 V qua $$45\text{ k}\Omega$$ xuống `GND` là:
  $$
  I = \frac{3.3\text{ V}}{45{,}000\ \Omega} \approx \mathbf{73.3\ \mu\text{A}} \quad (0.073\text{ mA}!),
  $$
  công suất tiêu tán chỉ $$3.3 \times 73.3\ \mu\text{A} \approx \mathbf{0.24\text{ mW}}$$ — vừa chống nhiễu tuyệt đối, vừa gần như không tốn pin!
- **Bẫy sai lầm phổ biến:** nếu bạn nối nút nhấn trực tiếp giữa `3V3` và `GND` mà quên đặt qua điện trở, bấm nút là gây **ngắn mạch trực tiếp** làm sập nguồn toàn bộ bo mạch!

### Khung giải thích: 4 mẫu thiết kế GPIO sạch cho firmware robot (nên đọc chậm)

1. **Bước 1 — Luôn dùng `INPUT_PULLUP` cho nút nhấn và công tắc hành trình:** Vừa gọn dây (chỉ cần kéo dây nút nhấn về `GND`, không cần kéo đường nguồn `3V3` ra vỏ khung kim loại dễ chập), vừa chống nhiễu thả nổi triệt để.
2. **Bước 2 — Đọc trạng thái bằng hàm bọc có tên rõ nghĩa:** Viết `bool is_button_pressed() { return digitalRead(PIN_BTN) == LOW; }` để không bao giờ bị loạn đầu giữa mức điện `LOW` và ý nghĩa logic "đang nhấn".
3. **Bước 3 — Tách rõ phát hiện *mức* (level) với phát hiện *cạnh* (edge):** Muốn chuyển chế độ mỗi lần bấm 1 cái, phải so sánh `pressed && !prev_pressed` (bắt cạnh nhấn) thay vì chỉ kiểm tra `if (pressed)` (sẽ đảo chế độ 500 lần mỗi giây!).
4. **Bước 4 — Luôn định nghĩa trạng thái ban đầu an toàn trong `setup()`:** Ghi mức tắt động cơ/LED ngay khi cấu hình `pinMode(..., OUTPUT)` để tránh giật bánh xe lúc mới bật nguồn.

**Kiểm tra nhanh.** Một công tắc hành trình cản trước của xe robot dùng `INPUT_PULLUP` (active-low). Nếu sợi dây nối công tắc bị đứt giữa chừng khi xe đang chạy, chân GPIO sẽ đọc mức gì? Nó sẽ kéo lên `HIGH` (không nhấn) — đó là lý do trong hệ thống an toàn công nghiệp, **nút dừng khẩn cấp (E-Stop)** luôn dùng tiếp điểm *thường đóng (NC)*: dây đứt lập tức báo dừng xe an toàn!

---

## Vì sao bài này quan trọng

Trên Capstone A, nút nhấn đại diện cho thao tác xác nhận của người vận hành — chẳng hạn xóa trạng thái lỗi (FAULT) hoặc cho phép robot thoát trạng thái dừng. Nếu chân nút bị để nổi, nhiễu điện sẽ tạo ra các lần nhấn giả và có thể tự ý xóa lỗi mà bạn chưa kiểm tra. Tương tự, khi LED đóng vai trò đèn báo trạng thái, thiếu điện trở hạn dòng sẽ gây quá dòng cho chân GPIO. Mọi thử nghiệm trong bài chỉ làm việc với tín hiệu vào và LED chỉ thị; động cơ tuyệt đối không nối trực tiếp vào GPIO mà phải đi qua mạch cầu H riêng ở các chương sau.

## Nội dung

GPIO là chân tín hiệu số có thể cấu hình làm ngõ vào hoặc ngõ ra. Khi bật điện trở kéo lên nội (internal pull-up) cho ngõ vào, chân được kéo yếu lên mức 3,3 V; đầu còn lại của nút nhấn nối xuống mass (GND), không nối lên 3,3 V. Khi nhả nút, mạch hở nên điện trở kéo lên giữ chân ở mức `HIGH`. Khi nhấn nút, tiếp điểm đóng thẳng xuống mass (mạnh hơn điện trở kéo lên nội) nên chân đọc mức `LOW`. Với người mới, logic đảo này ("nhấn = LOW") đôi khi gây ngược trực giác, vì vậy hãy ghi chú rõ ngay trong mã nguồn để tránh nhầm lẫn về sau.

![Nút xuống mass, GPIO kéo lên]({{ site.imgurl }}/generated/gpio_pullup_button.png)

Nếu vi điều khiển không có kéo lên nội, bạn dùng điện trở ngoài 10 kΩ nối từ GPIO lên 3,3 V và vẫn nối nút từ GPIO xuống mass. Giá trị 10 kΩ đủ nhỏ để chống nhiễu khi chạm tay vào dây, nhưng đủ lớn để khi giữ nút chỉ tiêu thụ dòng $3{,}3 / 10000 = 0{,}33$ mA.

Mỗi đèn LED chỉ thị cần một điện trở nối tiếp riêng. Một LED thông dụng có điện áp thuận khoảng 2,0 V và dòng làm việc an toàn, đủ sáng từ chân GPIO 3,3 V là 8 mA. Áp dụng định luật Ohm cho phần điện áp rơi trên điện trở:

$$
R = \frac{V_{CC} - V_F}{I_F} = \frac{3{,}3 - 2{,}0}{0{,}008} = 162{,}5\,\Omega.
$$

Giá trị tiêu chuẩn gần nhất phổ biến trong bộ điện trở 1/4 W là 180 Ω, cho dòng thực tế thấp hơn mục tiêu một chút:

$$
I = \frac{3{,}3 - 2{,}0}{180} \approx 7{,}2\,\mathrm{mA}, \qquad P = I^2 R \approx 9\,\mathrm{mW}.
$$

Công suất 9 mW rất nhỏ so với định mức 250 mW của điện trở 1/4 W nên linh kiện hoàn toàn không nóng; giá trị 220 Ω cũng dùng tốt, chỉ tối hơn một chút. Nếu bỏ qua điện trở nối tiếp, dòng không được giới hạn sẽ dễ làm cháy LED hoặc hỏng tầng đệm chân GPIO. Khi đấu dây, cực âm (cathode) của LED nối về mass, cực dương (anode) nối qua điện trở về chân GPIO (hoạt động trên đường nguồn 3,3 V).

![LED, điện trở nối tiếp, và mass]({{ site.imgurl }}/generated/led_series_resistor.png)

Tiếp điểm cơ khí không đóng ngắt dứt khoát trong một lần mà bị dội (bounce) trong thời gian ngắn; bài sau sẽ phân tích kỹ hiện tượng này. Trong bài này, ta áp dụng quy tắc lọc đơn giản trong vòng lặp: chỉ công nhận trạng thái mới khi tín hiệu thô giữ nguyên không đổi suốt 20 ms. Lưu mẫu thô gần nhất và mốc thời gian thay đổi; mỗi khi tín hiệu thô đổi mức thì đặt lại đồng hồ. Khi tín hiệu thô giữ ổn định đủ 20 ms và khác với trạng thái đã xác nhận trước đó, ta cập nhật trạng thái và in ra đúng một dòng (`press` ở cạnh xuống, `release` ở cạnh lên). Không in ở mọi vòng lặp để tránh làm ngập màn hình serial.

Tuyệt đối không dùng `delay(20)` để chống dội, vì hàm chặn sẽ làm đứng nhịp tim và làm giảm khả năng đáp ứng của vòng lặp điều khiển; kiểm tra theo mốc thời gian giúp vòng lặp luôn rảnh để xử lý tác vụ khác.

Ba lỗi đấu nối thường gặp nhất:

- **Chân để nổi (floating pin):** đấu nút xuống mass nhưng quên cấu hình `INPUT_PULLUP` hoặc `Pin.PULL_UP`. Khi nhả nút, sợi dây hoạt động như một anten thu nhiễu khiến serial tự in `press`/`release` liên tục dù không ai chạm. Hãy kiểm tra lại chế độ chân trước khi sửa phần chống dội.
- **LED thiếu điện trở nối tiếp:** LED có thể lóe sáng gắt rồi hỏng, hoặc buộc chân GPIO cấp dòng vượt định mức. Luôn lắp điện trở khoảng 180 Ω nối tiếp dù LED trông có vẻ vẫn sáng.
- **Nút luôn đọc mức cao:** đấu nút giữa 3,3 V và GPIO trong khi vẫn bật kéo lên nội (và không có kéo xuống). Khi nhả, kéo lên đưa chân về `HIGH`; khi nhấn, nút nối thẳng lên 3,3 V cũng là `HIGH`, nên không bao giờ xuất hiện cạnh tín hiệu. Hãy chuyển đầu nút sang GND theo chuẩn của môn học.

Không cấp nguồn động cơ, cuộn dây rơ-le hay chân VM của TB6612 từ GPIO. GPIO chỉ xuất tín hiệu logic điều khiển, không cấp dòng công suất.

**Arduino C++ cho ESP32:** nút nhấn tại GPIO 4, LED tại GPIO 18 (cả hai đều tránh nhóm chân strapping sẽ đề cập ở bài PWM).

```cpp
const int BTN = 4;
const int LED = 18;
const uint32_t DEBOUNCE_MS = 20;

int lastRaw = HIGH;
int stable = HIGH;
uint32_t lastChange = 0;

void setup() {
  pinMode(BTN, INPUT_PULLUP);  // nhả thì cao, nhấn thì thấp
  pinMode(LED, OUTPUT);
  Serial.begin(115200);
  lastChange = millis();
  Serial.println("gpio edges");
}

void loop() {
  uint32_t now = millis();
  int raw = digitalRead(BTN);
  if (raw != lastRaw) {
    lastRaw = raw;
    lastChange = now;
  }
  if ((now - lastChange) >= DEBOUNCE_MS && raw != stable) {
    stable = raw;
    digitalWrite(LED, stable == LOW ? HIGH : LOW);  // LED sáng khi đang giữ
    Serial.println(stable == LOW ? "press" : "release");
  }
}
```

Trong đoạn mã trên, đèn LED sáng trong suốt thời gian giữ nút để dễ quan sát, còn cổng serial chỉ in ra đúng tại các cạnh đã xác nhận.

**MicroPython:** giữ cùng số chân nếu dùng ESP32; trên Pico, đổi sang các chân GP trống tương ứng và giữ nguyên `Pin.PULL_UP`.

```python
from machine import Pin
import time

btn = Pin(4, Pin.IN, Pin.PULL_UP)
led = Pin(18, Pin.OUT)
DEBOUNCE_MS = 20

last_raw = btn.value()
stable = last_raw
last_change = time.ticks_ms()
print("gpio edges")

while True:
    now = time.ticks_ms()
    raw = btn.value()
    if raw != last_raw:
        last_raw = raw
        last_change = now
    if time.ticks_diff(now, last_change) >= DEBOUNCE_MS and raw != stable:
        stable = raw
        led.value(1 if stable == 0 else 0)
        print("press" if stable == 0 else "release")
    time.sleep_ms(1)
```

## Ví dụ tính tay

Giả sử bạn nhấn nút tại $t = 1000$ ms và nhả tại $t = 1600$ ms; tiếp điểm dội trong 8 ms sau mỗi thao tác rồi ổn định. Theo luật 20 ms (tính từ cạnh cuối của đợt dội ở $t = 1008$ ms và $t = 1608$ ms, hoặc tại $t = 1020$ ms và $t = 1620$ ms nếu không có dội thêm sau mốc nhấn/nhả), chương trình xác nhận mức `LOW`, in `press` và bật LED, sau đó xác nhận mức `HIGH`, in `release` và tắt LED. Màn hình chỉ hiển thị:

```
gpio edges
press
release
```

Nếu một lần nhấn tạo ra hàng chục dòng liên tiếp, điều kiện lọc ổn định chưa bọc đúng lệnh in. Nếu màn hình không in gì, hãy dùng đồng hồ đo điện áp tại chân nút: nhả gần 3,3 V và nhấn gần 0 V; nếu trạng thái nhả dao động bất định quanh 0,8 V đến 2 V thì chân đang bị nổi.

Xét thêm một LED có điện áp thuận $V_F = 2{,}1$ V cần dòng 5 mA từ nguồn 3,3 V:

$$
R = \frac{3{,}3 - 2{,}1}{0{,}005} = 240\,\Omega.
$$

Trong bộ linh kiện thông dụng, bạn chọn 220 Ω hoặc 270 Ω. Nếu dùng sẵn điện trở 180 Ω, dòng qua LED khoảng $(3{,}3 - 2{,}1) / 180 \approx 6{,}7$ mA — vẫn nằm trong ngưỡng an toàn và sáng hơn một chút.

## Bài lab

Chỉ cấp nguồn cho bo mạch qua cổng USB; không nối pin và không để dây chạm vào chân 5 V.

1. Rút cáp USB trước khi cắm dây. Nối một chân nút nhấn vào GPIO 4 và chân đối diện vào GND. Mắc nối tiếp LED và điện trở 180 Ω giữa GPIO 18 và GND (anode phía GPIO, cathode phía GND). Kiểm tra lại sơ đồ trước khi cắm USB.
2. Nạp mã C++ hoặc chạy kịch bản MicroPython, mở Serial Monitor ở 115200 baud. Màn hình chỉ nên hiện một dòng `gpio edges` rồi đứng yên.
3. Nhấn và nhả nút chậm một lần: log phải hiện đúng một cặp `press` và `release`, đồng thời LED chỉ sáng khi đang giữ nút. Thử nhấn 5 lần và xác nhận thu được đúng 5 cặp.
4. Thử tạm bỏ kéo lên nội (`INPUT` thay vì `INPUT_PULLUP`), chạy lại để quan sát hiện tượng chân nổi tạo ra các cạnh giả, ghi nhận vào sổ rồi khôi phục lại kéo lên.
5. Ghi vào sổ số chân đã dùng, giá trị điện trở và dán một cặp `press`/`release` sạch (kèm ảnh chụp breadboard nếu có) để dùng cho checklist cuối chương.

Nếu serial in `press` bình thường nhưng LED không sáng, kiểm tra lại cực tính LED (có thể bị cắm ngược) hoặc số chân. Nếu serial không in gì và đồng hồ đo thấy 3,3 V ở cả hai trạng thái nhấn/nhả, nút đang bị mắc nhầm lên đường 3,3 V thay vì GND.

## Video tham khảo

- **Xem trước:** [ESP32 LED + Push Button Tutorial for Beginners | ESP32 GPIO Input & Output](https://www.youtube.com/watch?v=zCzchrkpHzk) — Alvin Pribadi, tiếng Anh. Minh họa thao tác đọc nút nhấn và điều khiển LED trên GPIO, đối chiếu với mẫu `INPUT_PULLUP` và `OUTPUT` trong bài.
- [What is Switch Bounce and How to Debounce – ATM | Digi-Key Electronics](https://www.youtube.com/watch?v=IvU8m_30iK0) — DigiKey, tiếng Anh. Giải thích hiện tượng dội cơ học của nút nhấn gây ra nhiều cạnh tín hiệu nếu chưa chống dội.

## Bài tập

1. Một LED đỏ có $V_F = 1{,}8$ V và bạn muốn dòng $I_F = 6$ mA từ nguồn 3,3 V. Tính giá trị điện trở $R$, rồi chọn giá trị tiêu chuẩn gần nhất sao cho dòng thực tế không vượt quá 6 mA.
2. Trạng thái ổn định chuyển từ `HIGH` sang `LOW` tại $t = 250$ ms và trở lại `HIGH` tại $t = 900$ ms (đã qua bộ lọc 20 ms). Hãy liệt kê các dòng serial in ra và trạng thái LED trong từng khoảng thời gian. Những gì không được phép xuất hiện giữa hai mốc này?
3. Một sinh viên nối nút giữa 3,3 V và GPIO 4, khai báo `pinMode(4, INPUT_PULLUP)` rồi thắc mắc vì sao LED không đổi trạng thái. Cho biết điện áp tại chân GPIO 4 ở cả hai trạng thái nút và dây cần thay đổi.
4. Nếu vi điều khiển không có kéo lên nội và bạn chỉ có một điện trở 10 kΩ cùng nút nhấn, điện trở này nối giữa hai điểm nào và dòng qua nó khi đang giữ nút là bao nhiêu?

<details>
<summary>Gợi ý</summary>

1. $R = (3{,}3 - 1{,}8) / 0{,}006 = 250\,\Omega$. Chọn giá trị tiêu chuẩn 270 Ω để dòng nhỏ hơn 6 mA (220 Ω sẽ vượt nhẹ mức 6 mA).
2. Log in `press` tại cạnh xác nhận đầu (250 ms) và `release` tại cạnh sau (900 ms). LED chỉ sáng trong khoảng trạng thái ổn định là `LOW`. Không được in thêm các mẫu lặp lại giữa 250 ms và 900 ms.
3. Cả khi nhả lẫn khi nhấn, chân GPIO 4 đều ở gần 3,3 V nên không có cạnh tín hiệu. Cần chuyển đầu nút đang nối 3,3 V sang GND và giữ nguyên `INPUT_PULLUP`.
4. Điện trở 10 kΩ nối giữa GPIO và nguồn 3,3 V; đầu còn lại của nút nối xuống GND. Khi giữ nút, dòng qua điện trở là $3{,}3 / 10\,\mathrm{k}\Omega = 0{,}33$ mA.

</details>

## Đọc thêm

- [`pinMode` của Arduino](https://www.arduino.cc/reference/en/language/functions/digital-io/pinmode/) — giải thích chế độ `INPUT_PULLUP` dùng cho nút nhấn kéo lên trong bài.
- [`machine.Pin` của MicroPython](https://docs.micropython.org/en/latest/library/machine.Pin.html) — tài liệu về `Pin.PULL_UP` và phương thức `value()`.
- Nếu chưa chuẩn bị bo mạch chính, xem danh mục đầy đủ tại [bài mua sắm chương 00]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %}).

## Linh kiện cho bài lab

Mức giá dưới đây tham khảo từ Hshop (tính bằng đồng Việt Nam và có thể thay đổi theo thời điểm): nút nhấn tròn 12 mm PBS-11B kèm dây giá 10000₫ tại [hshop.vn/nut-nhan-nha-tron-pbs-11b-12mm-kem-cap](https://hshop.vn/nut-nhan-nha-tron-pbs-11b-12mm-kem-cap) (bất kỳ nút nhấn nhả thường hở hai chân nào đều tương đương về mặt điện); bộ LED giá 20000₫ tại [hshop.vn/bo-5-loai-led-sieu-sang-3mm-thong-dung-5-kind-3mm-transparent-color-led](https://hshop.vn/bo-5-loai-led-sieu-sang-3mm-thong-dung-5-kind-3mm-transparent-color-led) (LED 3 mm hay 5 mm đều áp dụng cùng công thức tính điện trở nối tiếp theo $V_F$).

Breadboard: [hshop.vn/test-board-cammb-102](https://hshop.vn/test-board-cammb-102). Dây cắm đực–đực 20 cm (40 sợi): [hshop.vn/day-cam-breadboard-duc-duc-20cm-cap-det-40-soi-m-m-jumper-wire](https://hshop.vn/day-cam-breadboard-duc-duc-20cm-cap-det-40-soi-m-m-jumper-wire). Bộ điện trở 1/4 W (có sẵn giá trị 180 Ω và 220 Ω) có thể tìm trên Shopee: [bộ điện trở 1/4W](https://shopee.vn/search?keyword=b%E1%BB%99%20%C4%91i%E1%BB%87n%20tr%E1%BB%9F%201%2F4W). Chưa cần mua động cơ cho chương này và tuyệt đối không nối động cơ vào GPIO.
