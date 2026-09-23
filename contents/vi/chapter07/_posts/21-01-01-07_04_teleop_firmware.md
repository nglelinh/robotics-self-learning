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

Bài 03 đã chốt các dòng. Bài này là sketch ESP32 đọc chúng, kẹp chúng, kéo chúng dần, và đưa về không khi máy chủ im. ROS vẫn chưa có trong vòng. Bánh ở trên không.

## Mục tiêu học

1. Tách `V` và `S` bằng `sscanf`, kẹp từng target vào $$\pm 180$$, và bỏ dòng sai.
2. Đưa cả hai target về 0 sau $$250~\mathrm{ms}$$ im lặng, và kéo PWM đang áp tiến 15 nấc mỗi $$20~\mathrm{ms}$$.
3. Đẩy hai kênh cầu H với STBY cao, rồi sửa các chân ví dụ cho khớp bảng dấu bài 02.
4. Gửi `V l r\n` từ Python, giết tiến trình, và thấy cả hai lốp dừng trong $$0{,}5~\mathrm{s}$$ trong khi MCU vẫn ăn buck.

## Kiến thức cần có

Cần cây nguồn bài 07-01, bảng dấu bài 07-02, và ngữ pháp bài 07-03: 115200 8N1, chữ kết thúc newline, máy chủ $$200~\mathrm{ms}$$, hạn firmware $$250~\mathrm{ms}$$, kẹp $$-180..180$$. Trên TB6612, STBY thấp thì ngõ ra tắt, và PWM 0 trong khi STBY vẫn cao là thắng ngắn, không phải thả trôi trở kháng cao. $$b$$ và $$r$$ của chương 06 nằm trong ghi chú; sketch này không đọc chúng. Dương vẫn nghĩa là lốp ấy về phía mũi. Twist, với `linear.x` và `angular.z`, đến sau khi chương 08 hiệu chuẩn và chương 09 mang topic. Hôm nay không tạo workspace ROS.

## Vì sao bài này quan trọng với Capstone A và ROS

Lỗi đáng sợ là lệnh bị dính: máy chủ chết mà duty cuối trong LEDC vẫn kéo robot bằng pin. Hạn nằm trong firmware. Luồng Twist sau này cần cùng hạn khi bản tin ngừng. Chương 09 thay parser, không thay cái dừng.

Ô cảm và ô tính trong hình là encoder và PID bạn chưa có. Bài này là ô hành động: PWM, và timeout ép về không.

![Hành động là PWM tới driver; timeout ép về không đã nằm trong ô ấy]({{ site.imgurl }}/generated/sense_compute_act.png)

## Kẹp, hạn, và bước kéo đếm được

Target là điều dòng hợp lệ cuối xin, sau khi kẹp. PWM đang áp là thứ cầu đang nhận, và được phép đi sau target. Mỗi $$20~\mathrm{ms}$$, giá trị đang áp bước tối đa 15 nấc về phía target:

$$
\text{số bước} = \left\lceil \frac{|\text{target} - \text{đang áp}|}{15} \right\rceil, \qquad t = \text{số bước} \times 20~\mathrm{ms}.
$$

Từ 0 lên 60 là 4 bước, $$80~\mathrm{ms}$$. Từ 0 lên 180 là 12 bước, $$240~\mathrm{ms}$$. Cuộn dây không bị đạp một bậc đầy.

Nếu `millis()` trừ mốc dòng hợp lệ cuối vượt $$250~\mathrm{ms}$$, cả hai target về 0 và bước kéo đưa duty xuống. Sau `V 60 60` không được gửi lại, target rơi ở $$250~\mathrm{ms}$$ và PWM đang áp về 0 khoảng $$80~\mathrm{ms}$$ sau:

$$
250~\mathrm{ms} + 4 \times 20~\mathrm{ms} = 330~\mathrm{ms}.
$$

Con số ấy nằm trong mức dừng $$0{,}5~\mathrm{s}$$ của lab. Lệnh 180 mất $$250+240 = 490~\mathrm{ms}$$, nên trần kẹp và bước kéo được chọn cùng nhau. `S` đưa target về 0 ngay; bước kéo vẫn làm thắng mềm. Dòng sai không làm mới hạn.

Chân ví dụ, bạn phải sửa theo bảng dấu bài 02: STBY 4, AIN1 16, AIN2 17, PWMA 18, BIN1 19, BIN2 21, PWMB 22. Đảo cặp IN trong code hoặc đảo vít motor, không cả hai. Arduino-ESP32 3.x dùng `ledcAttach(pin, freq, resolution)`; core 2.x dùng `ledcSetup` và `ledcAttachPin`. Sketch ghi cả hai. `Serial.setTimeout(10)` để `readBytesUntil` không chặn bước kéo cả một giây.

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

Mở cổng thường reset ESP32 qua DTR. `setup` đưa PWM về 0 trước khi STBY cao, nên reset ấy là một lần dừng. Đừng tin DTR lúc đóng cổng. Timeout dừng robot khi MCU còn ăn buck. Rút USB chỉ là bài kiểm hạn nếu buck đang nuôi ESP32. Nuôi chỉ bằng USB thì rút dây làm chân nổi.

Dùng cổng chương 02, `/dev/ttyUSB0` hoặc `/dev/ttyACM0`. `sleep(0.2)` là nhịp $$200~\mathrm{ms}$$, và `close()` là im lặng.

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

Lần chạy thứ hai ghi `V 60 -60\n` trong một giây. Trái tiến, phải lùi là yaw phải theo bảng dấu bài 02. Cờ không khớp thì sửa cặp IN của kênh đó, không đảo vít trong phiên này.

## Lab

### An toàn

Cả hai lốp ở trên không, xa mép bàn, và một tay với tới công tắc pin. Lệnh đầu là `V 60 60`, không phải 255. Bài này không xuống sàn. Có mùi hoặc lá không chạm được thì ngắt công tắc. Không để đầu pin lithium trần trên bàn khi script đã nạp.

### BOM

| Món | Việc |
|------|------|
| Robot đã lắp, bánh trên không | Phần bị điều khiển |
| ESP32 ăn buck 5,0 V, USB để nạp | Logic còn sống khi giết script |
| Bảng dấu bài 07-02 | Cực tính chân |
| Python 3 và pyserial | Máy chủ |
| Đồng hồ hoặc phép millis | Mức dừng 0,5 s |

### Các bước

1. Sửa chân và cực IN cho dương khớp bài 02. Nạp. STBY cao, duty bắt đầu từ 0.
2. Bánh trên không. Gửi `V 60 60` khoảng một giây. Cả hai cờ đi về mũi.
3. Giết script. Cả hai lốp dừng trong $$0{,}5~\mathrm{s}$$ trong khi công tắc pin vẫn bật.
4. Gửi `V 60 -60` một giây. Yaw khớp bảng (quay phải: trái tiến, phải lùi). Giết máy gửi lần nữa.
5. Gõ `S`, rồi gõ riêng `V 60`. `S` dừng. Dòng gãy không kéo một bánh.

### Kết quả mong đợi

Ghi chú có chân thật sự dùng, thời gian dừng (khoảng $$330~\mathrm{ms}$$ sau `V 60 60` cuối), và hướng yaw của `V 60 -60`. Robot vẫn trên hộp. Duty còn dính sau khi tiến trình chết là lab hỏng.

### Lỗi thường gặp

| Bạn thấy | Thường là |
|----------|-----------|
| Không gì chuyển động | STBY còn thấp, sai chân PWM, hoặc VM tắt |
| Còn chạy sau khi giết Python | Thiếu timeout, hoặc MCU không thực sự còn chạy |
| Chỉ lốp trái khớp bảng | Cặp IN phải lệch bài 02; sửa firmware hoặc vít, không cả hai |
| `V 60` giật một bánh | Không bắt `sscanf` trả về 2 |
| Lỗi biên dịch `ledcAttach` | Core 2.x; dùng `ledcSetup` và `ledcAttachPin` |

## Mua ở Việt Nam / Where to buy in Vietnam

Không thêm đồ nếu bài 01 và 02 đã làm thật. Chỗ thiếu thường là cáp USB có data, hoặc pyserial. ESP32 devkit khoảng 70.000–150.000 đồng, TB6612 25.000–70.000, L298N khoảng 45.000 nếu bạn map ENA/ENB vào chân PWM và vẫn giữ buck. Giá đổi.

- L298N đã kiểm, khoảng 45.000 đồng: [hshop.vn/mach-dieu-khien-dong-co-dc-l298](https://hshop.vn/mach-dieu-khien-dong-co-dc-l298)
- [Hshop ESP32](https://hshop.vn/search?q=ESP32), [TB6612](https://hshop.vn/search?q=TB6612)
- [Shopee ESP32](https://shopee.vn/search?keyword=ESP32%20devkit), [TB6612](https://shopee.vn/search?keyword=TB6612)
- [Lazada cáp USB](https://www.lazada.vn/catalog/?q=cap%20micro%20USB%20data), [ESP32](https://www.lazada.vn/catalog/?q=ESP32)
- [Thế Giới IC ESP32](https://www.thegioiic.com/search?q=ESP32)

## Bài tập

1. PWM đang áp là 0 và target thành 180. Bao nhiêu bước, bao nhiêu mili giây, thì cầu thấy 180?
2. `V 60 60` cuối đến ở $$t = 0$$ và không còn gì theo sau. Target về 0 lúc nào, và PWM đang áp về 0 lúc nào?
3. Dòng `V 200 -300` được tách. `constrain` cất target nào? `V 60` làm gì với các target ấy?
4. Bạn xóa mỗi phép kiểm timeout và giữ bước kéo. Tiến trình Python chết và cổng không reset chip. Lốp làm gì, và vì sao bài 05 từ chối lỗi này?
5. Bài 02 nói phải dương là BIN1 thấp, BIN2 cao. Sửa dòng nào, và vì sao vít motor giữ nguyên?

### Gợi ý đáp án

1. $$180/15 = 12$$ bước, $$240~\mathrm{ms}$$. 2. Target về 0 tại $$250~\mathrm{ms}$$; PWM đang áp cần thêm 4 bước, nên về 0 khoảng $$330~\mathrm{ms}$$. 3. Target thành $$180$$ và $$-180$$. `V 60` bị bỏ, target giữ nguyên. 4. Duty cuối còn đó và lốp quay tiếp. Bài 05 khi ấy trượt bài dừng bằng cách giết máy gửi. 5. Đổi cách ghi BIN1 và BIN2 cho lệnh phải dương. Giữ vít. Đảo thêm lần nữa sẽ phá chỗ sửa.

## Đọc thêm

- [Arduino `Serial`](https://www.arduino.cc/reference/en/language/functions/communication/serial/)
- [pySerial, phần mở đầu](https://pyserial.readthedocs.io/en/latest/shortintro.html)
- [Pololu TB6612FNG](https://www.pololu.com/product/713)
- [geometry_msgs/Twist (Jazzy)](https://docs.ros.org/en/jazzy/p/geometry_msgs/interfaces/msg/Twist.html)
