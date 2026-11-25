---
layout: post
title: "Vòng teleop firmware (chưa ROS)"
chapter: "07"
order: 4
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter07
lesson_type: required
draft: false
---

Bài 03 đã chốt đặc tả khung lệnh. Bài này trình bày chương trình (sketch) cho ESP32 để đọc chuỗi lệnh, kẹp giá trị an toàn, tăng giảm PWM mượt theo bước (slew rate) và tự động đưa về 0 khi máy chủ ngừng gửi. Hệ thống vẫn chưa dùng ROS và hai bánh xe vẫn phải kê trên không.

Viết phần mềm cho robot khác hoàn toàn với viết một ứng dụng web hay bài tập cấu trúc dữ liệu: trên vi điều khiển, **thời gian thực là luật thép**. Nếu bạn đặt một lệnh `delay(500)` trong hàm `loop()` để chờ chớp đèn LED, robot của bạn sẽ "điếc" hoàn toàn trong nửa giây — không đọc encoder, không nhận lệnh dừng khẩn cấp, và lao thẳng vào chân bàn! Bài học về **vòng lặp teleop firmware** giới thiệu kiến trúc chuẩn công nghiệp trên vi điều khiển (trước khi bước sang ROS): vòng lặp không chặn (**non-blocking loop**), máy trạng thái an toàn và cơ chế **chó canh cửa (watchdog timeout)** tự dừng xe khi mất kết nối.

## Kiến thức cần nhớ: Lập trình thời gian thực không chặn trên vi điều khiển

### 1. Vòng lặp không chặn (Non-Blocking Scheduler với `millis()` / `micros()`)
Thay vì gọi `delay()`, firmware chia công việc theo các chu kỳ cố định dựa trên đồng hồ phần cứng: đọc bộ đệm UART liên tục ở mỗi vòng lặp, chạy vòng điều khiển động cơ ở chu kỳ cứng $$50\text{–}100\text{ Hz}$$ (10–20 ms), và gửi bản tin telemetry ở $$10\text{–}20\text{ Hz}$$ (50–100 ms). Nhờ vậy, không tác vụ nào làm nghẽn phản xạ an toàn của robot.

### 2. Cơ chế Watchdog Timeout (Dead-Man's Switch)
Trong điều khiển từ xa (teleop), câu hỏi quan trọng nhất không phải là *"nhấn W xe có chạy không?"* mà là ***"nếu máy tính treo, Wi-Fi rớt hoặc cáp USB tuột giữa lúc xe đang lao đi, chuyện gì xảy ra?"***. Watchdog lưu mốc thời gian `last_cmd_ms` của gói lệnh hợp lệ gần nhất; hễ `now - last_cmd_ms > T_wd` (thường 200–500 ms), firmware lập tức chuyển sang trạng thái `SAFE_STOP` và đưa PWM cả hai bánh về 0!

### 3. Giới hạn gia tốc (Slew-Rate Limiter) bảo vệ hộp số và nguồn pin
Nhảy vọt lệnh từ tiến 100% sang lùi -100% trong 1 mili-giây sẽ tạo dòng xung ngược cực lớn làm reset nguồn và vỡ bánh răng nhựa. Một bộ giới hạn tốc độ thay đổi (*slew-rate limiter*) ép vận tốc tăng/giảm tối đa $$\Delta v_{\max} = a_{\max} \cdot \Delta t$$ mỗi chu kỳ, giúp xe đề-pa và phanh mượt mà.

### Giải thích: Cầm tay tính quãng đường dừng khẩn cấp khi mất kết nối theo ngưỡng Watchdog

Giả sử robot Capstone đang chạy thẳng với vận tốc **$$v = 0{,}80\text{ m/s}$$**, máy tính gửi lệnh teleop ở tần số $$20\text{ Hz}$$ (mỗi $$50\text{ ms}$$ một gói), và gia tốc phanh an toàn của xe là **$$a_{\text{phanh}} = 2{,}0\text{ m/s}^2$$**. Đột ngột đường truyền bị đứt hoàn toàn! Hãy so sánh quãng đường xe lao đi với hai cấu hình thời gian Watchdog:

1. **Cấu hình an toàn ($$T_{\text{wd}} = 300\text{ ms} = 0{,}30\text{ s}$$, tương đương 6 gói mất liên tiếp):**
   - Quãng đường trôi trong lúc chờ Watchdog kích hoạt:
     $$d_{\text{chờ}} = v \cdot T_{\text{wd}} = 0{,}80 \times 0{,}30 = 0{,}24\text{ m}\;(24\text{ cm}).$$
   - Quãng đường giảm tốc về 0 sau khi phanh kích hoạt:
     $$d_{\text{phanh}} = \frac{v^2}{2 a_{\text{phanh}}} = \frac{0{,}80^2}{2 \times 2{,}0} = \frac{0{,}64}{4{,}0} = 0{,}16\text{ m}\;(16\text{ cm}).$$
   - **Tổng quãng đường dừng:** $$d_{\text{tổng}} = 0{,}24 + 0{,}16 = 0{,}40\text{ m}\;(40\text{ cm})$$.

2. **Cấu hình quá lỏng ($$T_{\text{wd}} = 2{,}0\text{ s}$$):**
   - $$d_{\text{chờ}} = 0{,}80 \times 2{,}0 = 1{,}60\text{ m} \implies d_{\text{tổng}} = 1{,}60 + 0{,}16 = 1{,}76\text{ m}!$$
   Chỉ một tham số cấu hình sai lệch đã biến cú dừng gọn trong 40 cm thành cú đâm tường ở cách đó gần 2 mét!

## Mục tiêu học

1. Phân tích lệnh `V` và `S` bằng `sscanf`, kẹp từng giá trị mục tiêu vào khoảng $$\pm 180$$ và bỏ qua hoàn toàn các dòng sai cú pháp.
2. Tự động đặt cả hai mục tiêu về 0 sau $$250~\mathrm{ms}$$ không nhận lệnh mới, đồng thời điều chỉnh PWM thực tế tiến dần về mục tiêu tối đa 15 nấc mỗi $$20~\mathrm{ms}$$.
3. Điều khiển hai kênh cầu H với chân `STBY` ở mức cao, và cập nhật số chân ví dụ khớp với bảng dấu đã lập ở Bài 02.
4. Gửi lệnh `V l r\n` từ Python, ngắt tiến trình đột ngột và xác nhận cả hai lốp dừng hẳn trong vòng $$0{,}5~\mathrm{s}$$ trong khi vi điều khiển vẫn được cấp nguồn từ mạch buck.

## Kiến thức cần có

Cây nguồn từ Bài 07-01, bảng dấu từ Bài 07-02 và giao thức từ Bài 07-03 (115200 8N1, văn bản kết thúc bằng `\n`, chu kỳ máy chủ $$200~\mathrm{ms}$$, quá hạn firmware $$250~\mathrm{ms}$$, kẹp $$-180..180$$). Trên TB6612, khi `STBY` ở mức thấp thì ngõ ra bị ngắt; khi `STBY` cao, việc đặt PWM bằng 0 (khi hai chân `IN` khác mức) sẽ hãm ngắn mạch, còn đặt cả hai chân `IN` xuống thấp sẽ ngắt cầu (trở kháng cao). Hai kích thước $$b$$ và $$r$$ từ Chương 06 được lưu sẵn trong sổ tay nhưng chưa dùng trong sketch này. Quy ước dương vẫn là chiều lốp lăn về phía mũi xe. Thông điệp `Twist` (`linear.x`, `angular.z`) sẽ được tích hợp sau khi hiệu chuẩn ở Chương 08 và mở topic ở Chương 09; hôm nay chưa tạo workspace ROS.

## Vì sao bài này quan trọng với Capstone A và ROS

Lỗi nguy hiểm nhất khi điều khiển robot là lệnh bị giữ kẹt: máy chủ ngừng hoạt động nhưng thanh ghi PWM (LEDC) vẫn duy trì mức duty cũ khiến xe tiếp tục chạy bằng nguồn pin. Cơ chế quá hạn (timeout) bắt buộc phải nằm trực tiếp trong firmware. Về sau, luồng `Twist` trên ROS 2 cũng đòi hỏi đúng cơ chế dừng này khi node phát bị tắt; Chương 09 chỉ thay bộ phân tích chuỗi bằng bộ nhận topic chứ không bỏ cơ chế dừng an toàn.

Trong sơ đồ vòng lặp cảm biến – tính toán – chấp hành dưới đây, khối cảm biến (encoder) và khối tính toán (PID) sẽ học ở chương sau; bài này hoàn thiện khối chấp hành gồm xuất PWM và ép về 0 khi quá hạn.

![Hành động là PWM tới driver; timeout ép về không đã nằm trong ô ấy]({{ site.imgurl }}/generated/sense_compute_act.png)

## Kẹp, hạn, và bước kéo đếm được

Giá trị **target** là mục tiêu mà dòng lệnh hợp lệ gần nhất yêu cầu (sau khi đã kẹp trong $$\pm 180$$). Giá trị **đang áp** (`applied`) là mức PWM thực tế đang cấp cho mạch cầu, được phép thay đổi từ từ theo sau `target`. Cứ mỗi $$20~\mathrm{ms}$$, giá trị đang áp tiến thêm tối đa 15 nấc về phía `target`:

$$
\text{số bước} = \left\lceil \frac{|\text{target} - \text{đang áp}|}{15} \right\rceil, \qquad t = \text{số bước} \times 20~\mathrm{ms}.
$$

Như vậy, tăng từ 0 lên 60 cần 4 bước ($$80~\mathrm{ms}$$), còn từ 0 lên 180 cần 12 bước ($$240~\mathrm{ms}$$), giúp tránh sốc dòng đột ngột lên cuộn dây động cơ và nguồn pin.

Nếu khoảng thời gian tính từ `millis()` đến mốc nhận dòng hợp lệ cuối cùng vượt quá $$250~\mathrm{ms}$$, cả hai `target` lập tức đặt về 0 và bộ giới hạn tốc độ thay đổi (slew) sẽ hạ dần duty về 0. Ví dụ, sau lệnh `V 60 60` cuối cùng mà không có lệnh mới, `target` rơi về 0 ở mốc $$250~\mathrm{ms}$$ và PWM thực tế về 0 sau thêm $$80~\mathrm{ms}$$:

$$
250~\mathrm{ms} + 4 \times 20~\mathrm{ms} = 330~\mathrm{ms}.
$$

Thời gian này nằm gọn trong giới hạn dừng $$0{,}5~\mathrm{s}$$ của bài thực hành. Ngay cả khi đang chạy ở trần 180, tổng thời gian dừng cũng chỉ là $$250 + 240 = 490~\mathrm{ms}$$ — đó là lý do trần kẹp và bước kéo được chọn đồng bộ với nhau. Lệnh `S` lập tức đặt `target` về 0 để giảm tốc mềm về dừng, còn các dòng sai cú pháp bị bỏ qua và không làm mới bộ đếm thời gian quá hạn.

Các chân ví dụ trong mã nguồn (bạn cần chỉnh lại theo bảng dấu Bài 02): `STBY = 4`, `AIN1 = 16`, `AIN2 = 17`, `PWMA = 18`, `BIN1 = 19`, `BIN2 = 21`, `PWMB = 22`. Nếu cần đảo chiều một bánh, chỉ đảo cặp `IN` trong mã nguồn hoặc đảo dây trên cầu vít động cơ, không làm cả hai. Lưu ý sự khác biệt phiên bản: Arduino-ESP32 core 3.x dùng `ledcAttach(pin, freq, resolution)`, trong khi core 2.x dùng `ledcSetup` và `ledcAttachPin` (cả hai đều có chú thích trong mã). Hàm `Serial.setTimeout(10)` đảm bảo `readBytesUntil` không làm treo vòng lặp bước kéo tới 1 giây nếu thiếu ký tự xuống dòng.

```cpp
// Edit pins and IN polarity to the lesson 07-02 sign map.
// Positive rolls that tire toward the nose.

const int PIN_STBY = 4;
const int PIN_AIN1 = 16;
const int PIN_AIN2 = 17;
const int PIN_PWMA = 18;
const int PIN_BIN1 = 19;
const int PIN_BIN2 = 21;
const int PIN_PWMB = 22;

const int PWM_FREQ = 20000;
const int PWM_RES  = 8;
const int PWM_LIM  = 180;
const unsigned long TIMEOUT_MS = 250;
const int SLEW_STEP = 15;
const unsigned long SLEW_MS = 20;

int targetL = 0, targetR = 0;
int appliedL = 0, appliedR = 0;
unsigned long lastRx = 0;
unsigned long lastSlew = 0;

int approach(int applied, int target) {
  if (applied < target) return min(applied + SLEW_STEP, target);
  if (applied > target) return max(applied - SLEW_STEP, target);
  return applied;
}

void drive(int in1, int in2, int pwmPin, int cmd) {
  int mag = abs(cmd);
  if (cmd > 0) {
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
  } else if (cmd < 0) {
    digitalWrite(in1, LOW);
    digitalWrite(in2, HIGH);
  } else {
    digitalWrite(in1, LOW);
    digitalWrite(in2, LOW);
  }
  ledcWrite(pwmPin, mag);
}

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(10);
  pinMode(PIN_STBY, OUTPUT);
  pinMode(PIN_AIN1, OUTPUT);
  pinMode(PIN_AIN2, OUTPUT);
  pinMode(PIN_BIN1, OUTPUT);
  pinMode(PIN_BIN2, OUTPUT);
  digitalWrite(PIN_AIN1, LOW);
  digitalWrite(PIN_AIN2, LOW);
  digitalWrite(PIN_BIN1, LOW);
  digitalWrite(PIN_BIN2, LOW);
  // Arduino-ESP32 3.x:
  ledcAttach(PIN_PWMA, PWM_FREQ, PWM_RES);
  ledcAttach(PIN_PWMB, PWM_FREQ, PWM_RES);
  // Core 2.x: đừng gọi ledcAttach / ledcWrite(pin, duty).
  // ledcSetup(0, PWM_FREQ, PWM_RES); ledcAttachPin(PIN_PWMA, 0);
  // ledcSetup(1, PWM_FREQ, PWM_RES); ledcAttachPin(PIN_PWMB, 1);
  // rồi ledcWrite(0, duty) và ledcWrite(1, duty) — số kênh, không phải số chân.
  ledcWrite(PIN_PWMA, 0);
  ledcWrite(PIN_PWMB, 0);
  digitalWrite(PIN_STBY, HIGH);
  lastRx = millis();
  lastSlew = millis();
}

void loop() {
  if (Serial.available()) {
    char line[32];
    size_t n = Serial.readBytesUntil('\n', line, sizeof(line) - 1);
    line[n] = '\0';
    if (n > 0 && line[n - 1] == '\r') line[n - 1] = '\0';
    int L = 0, R = 0;
    if (line[0] == 'S' && (line[1] == '\0' || line[1] == ' ')) {
      targetL = 0;
      targetR = 0;
      lastRx = millis();
    } else if (sscanf(line, "V %d %d", &L, &R) == 2) {
      targetL = constrain(L, -PWM_LIM, PWM_LIM);
      targetR = constrain(R, -PWM_LIM, PWM_LIM);
      lastRx = millis();
    }
    // Any other line is ignored.
  }

  if (millis() - lastRx > TIMEOUT_MS) {
    targetL = 0;
    targetR = 0;
  }

  if (millis() - lastSlew >= SLEW_MS) {
    lastSlew = millis();
    appliedL = approach(appliedL, targetL);
    appliedR = approach(appliedR, targetR);
    drive(PIN_AIN1, PIN_AIN2, PIN_PWMA, appliedL);
    drive(PIN_BIN1, PIN_BIN2, PIN_PWMB, appliedR);
  }
}
```

Khi máy tính mở cổng nối tiếp, tín hiệu DTR thường làm ESP32 khởi động lại. Vì hàm `setup()` luôn đặt PWM về 0 trước khi kéo `STBY` lên cao, lần khởi động lại đó luôn an toàn. Tuy nhiên, không được trông chờ vào DTR khi đóng cổng; việc dừng robot khi máy chủ ngừng gửi phải do cơ chế timeout thực hiện trong lúc ESP32 vẫn đang được nuôi bởi mạch buck. Rút cáp USB chỉ kiểm chứng đúng cơ chế timeout nếu ESP32 đang ăn nguồn buck — nếu chỉ nuôi qua USB, rút dây sẽ làm mất nguồn MCU và các chân tín hiệu bị thả nổi.

Trên máy tính, dùng đúng tên cổng từ Chương 02 (`/dev/ttyUSB0` hoặc `/dev/ttyACM0`). Lệnh `sleep(0.2)` tạo nhịp gửi $$200~\mathrm{ms}$$ và `close()` sẽ ngắt chuỗi lệnh:

```python
import time
import serial

port = serial.Serial("/dev/ttyUSB0", 115200, timeout=0.1)
time.sleep(2.0)

t0 = time.time()
while time.time() - t0 < 1.0:
    port.write(b"V 60 60\n")
    time.sleep(0.2)

port.close()
```

Ở lượt chạy thứ hai, đổi lệnh thành `V 60 -60\n` trong 1 giây: bánh trái tiến, bánh phải lùi tương ứng với quay phải theo bảng dấu Bài 02. Nếu chiều quay thực tế không khớp, hãy sửa cặp chân `IN` của kênh đó trong mã nguồn, không đảo thêm dây trên cầu vít.

## Lab

### An toàn

Kê cả hai lốp rời khỏi mặt bàn, đặt xe xa mép bàn và giữ một tay trong tầm công tắc pin. Lệnh thử đầu tiên là `V 60 60`, không dùng 255; bài này chưa đặt robot xuống sàn. Ngắt công tắc ngay nếu có mùi khét hoặc tản nhiệt quá nóng. Không để đầu dây pin lithium trần trên bàn trong khi thử nghiệm.

### BOM

| Món | Việc |
|------|------|
| Robot đã lắp, bánh trên không | Phần bị điều khiển |
| ESP32 ăn buck 5,0 V, USB để nạp | Logic còn sống khi giết script |
| Bảng dấu bài 07-02 | Cực tính chân |
| Python 3 và pyserial | Máy chủ |
| Đồng hồ hoặc phép millis | Mức dừng 0,5 s |

### Các bước

1. Cập nhật số chân và cực tính `IN` trong sketch khớp với bảng dấu Bài 02 rồi nạp vào ESP32. Xác nhận `STBY` cao và PWM khởi đầu bằng 0.
2. Đảm bảo bánh treo trên không, chạy script Python gửi `V 60 60` trong khoảng 1 giây và quan sát cả hai mảnh băng dính đều quay về phía mũi xe.
3. Ngắt tiến trình Python (hoặc để script đóng cổng). Xác nhận cả hai bánh dừng hẳn trong vòng $$0{,}5~\mathrm{s}$$ trong khi công tắc nguồn pin vẫn đang bật.
4. Chạy lại với lệnh `V 60 -60` trong 1 giây, xác nhận chiều quay phải (trái tiến, phải lùi) khớp bảng dấu rồi ngắt tiến trình để kiểm tra dừng.
5. Gửi thử `S`, sau đó gửi riêng `V 60`. Xác nhận `S` dừng xe ngay, còn dòng thiếu tham số `V 60` không làm giật hay quay riêng một bánh.

### Kết quả mong đợi

Sổ tay `lab-notes.md` ghi rõ sơ đồ chân thực tế đã dùng, thời gian dừng đo được (khoảng $$330~\mathrm{ms}$$ sau lệnh `V 60 60` cuối cùng) và chiều quay của `V 60 -60`. Robot vẫn đặt trên hộp kê trong suốt bài. Nếu bánh vẫn tiếp tục quay sau khi tiến trình Python kết thúc, bài thực hành chưa đạt.

### Lỗi thường gặp

| Bạn thấy | Thường là |
|----------|-----------|
| Không gì chuyển động | STBY còn thấp, sai chân PWM, hoặc VM tắt |
| Còn chạy sau khi giết Python | Thiếu timeout, hoặc MCU không thực sự còn chạy |
| Chỉ lốp trái khớp bảng | Cặp IN phải lệch bài 02; sửa firmware hoặc vít, không cả hai |
| `V 60` giật một bánh | Không bắt `sscanf` trả về 2 |
| Lỗi biên dịch `ledcAttach` | Core 2.x; dùng `ledcSetup` và `ledcAttachPin` |

## Mua ở Việt Nam / Where to buy in Vietnam

Không cần mua thêm linh kiện nếu đã hoàn thành đầy đủ Bài 01 và 02; thứ hay thiếu nhất ở bước này chỉ là cáp USB có đường truyền dữ liệu (data) hoặc thư viện `pyserial`. Giá tham khảo (có thể thay đổi): ESP32 devkit 70.000–150.000 đồng, TB6612 25.000–70.000 đồng, L298N khoảng 45.000 đồng (nếu dùng L298N, nối `ENA`/`ENB` vào chân PWM và vẫn cấp nguồn ESP32 qua mạch buck).

- L298N đã kiểm, khoảng 45.000 đồng: [hshop.vn/mach-dieu-khien-dong-co-dc-l298](https://hshop.vn/mach-dieu-khien-dong-co-dc-l298)
- [Hshop ESP32](https://hshop.vn/search?q=ESP32), [TB6612](https://hshop.vn/search?q=TB6612)
- [Shopee ESP32](https://shopee.vn/search?keyword=ESP32%20devkit), [TB6612](https://shopee.vn/search?keyword=TB6612)
- [Lazada cáp USB](https://www.lazada.vn/catalog/?q=cap%20micro%20USB%20data), [ESP32](https://www.lazada.vn/catalog/?q=ESP32)
- [Thế Giới IC ESP32](https://www.thegioiic.com/search?q=ESP32)

## Video tham khảo

- **Xem trước:** [Understanding UART](https://www.youtube.com/watch?v=sTHckUyxwp8) — Rohde & Schwarz, tiếng Anh. Giải thích cách truyền byte từ máy tính xuống vi điều khiển; firmware bài này chỉ chấp nhận khung đúng cú pháp và tự tắt PWM khi mất tín hiệu.
- [TB6612FNG H-Bridge Motor Controller - Better than L298N?](https://www.youtube.com/watch?v=JPPTRj0KWbg) — DroneBot Workshop, tiếng Anh. Minh họa cách PWM điều khiển tốc độ cầu H ở đầu cuối của vòng teleop.

Các video ngắn (Facebook Reel) dưới đây của Hoàng Quân (Cơ điện tử ICTU, [chinbi.com](https://chinbi.com)):

- [Test hệ thống điều khiển Chinbi](https://www.facebook.com/reel/1092867967065031) — Chú thích: test hệ thống điều khiển Chinbi Robot. Đối chiếu với firmware bài này ở cơ chế nhận lệnh chạy và tự đưa lệnh về 0 khi ngừng điều khiển.
- [Demo robot](https://www.facebook.com/reel/1057849570224248) — Chú thích: “Demo robot”. Minh họa bước đưa robot ra chạy thử sau khi vòng teleop đã có cơ chế quá hạn an toàn.

## Bài tập

1. PWM đang áp là 0 và mục tiêu đổi thành 180. Cần bao nhiêu bước kéo và bao nhiêu miligiây để mạch cầu đạt mức 180?
2. Lệnh `V 60 60` cuối cùng đến tại $$t = 0$$ và sau đó máy chủ ngừng gửi. Tại thời điểm nào `target` về 0, và tại thời điểm nào PWM đang áp về hẳn 0?
3. Khi nhận dòng `V 200 -300`, hàm `constrain` lưu giá trị mục tiêu nào? Sau đó nếu nhận thêm dòng `V 60`, hai giá trị mục tiêu bị ảnh hưởng ra sao?
4. Giả sử bạn xóa phần kiểm tra timeout nhưng vẫn giữ bộ bước kéo. Nếu tiến trình Python bị tắt đột ngột mà cổng serial không reset chip, bánh xe sẽ làm gì và vì sao Bài 05 sẽ đánh trượt lỗi này?
5. Theo bảng dấu Bài 02, bánh phải tiến khi `BIN1` thấp và `BIN2` cao. Bạn cần sửa phần nào trong firmware, và vì sao phải giữ nguyên dây trên cầu vít động cơ?

### Gợi ý đáp án

1. Cần $$180/15 = 12$$ bước, tương ứng $$12 \times 20 = 240~\mathrm{ms}$$.
2. `target` về 0 tại $$t = 250~\mathrm{ms}$$; PWM đang áp cần thêm 4 bước ($$80~\mathrm{ms}$$) nên về hẳn 0 vào khoảng $$330~\mathrm{ms}$$.
3. `constrain` kẹp thành $$180$$ và $$-180$$. Dòng `V 60` sai cú pháp nên bị bỏ qua hoàn toàn, hai mục tiêu giữ nguyên cho tới khi hết hạn timeout.
4. Mức duty cuối cùng vẫn được giữ nguyên trong thanh ghi PWM nên bánh xe tiếp tục quay vô thời hạn. Bài 05 sẽ đánh trượt tiêu chí dừng an toàn khi ngắt máy gửi.
5. Đảo mức ghi `HIGH`/`LOW` của `BIN1` và `BIN2` trong hàm `drive()` (hoặc truyền lệnh đảo dấu cho kênh phải) và giữ nguyên hai dây trên cầu vít động cơ; nếu đảo cả dây lẫn code thì hai lần đảo sẽ triệt tiêu nhau.

## Đọc thêm

- [Arduino `Serial`](https://www.arduino.cc/reference/en/language/functions/communication/serial/)
- [pySerial, phần mở đầu](https://pyserial.readthedocs.io/en/latest/shortintro.html)
- [Pololu TB6612FNG](https://www.pololu.com/product/713)
- [geometry_msgs/Twist (Jazzy)](https://docs.ros.org/en/jazzy/p/geometry_msgs/interfaces/msg/Twist.html)
