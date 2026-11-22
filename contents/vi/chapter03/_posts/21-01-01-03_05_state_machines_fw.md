---
layout: post
title: "Máy trạng thái trong firmware robot"
chapter: "03"
order: 5
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter03
lesson_type: required
draft: false
---

## Mục tiêu

Sau bài này, bạn xây dựng được máy trạng thái gồm ba trạng thái `IDLE`, `TELEOP` và `FAULT`, trong đó mỗi sự kiện (nhận lệnh mới, mất lệnh 300 ms, nhấn nút xác nhận) thực hiện đúng một chuyển trạng thái xác định. Tại `IDLE` và `FAULT`, cả hai kênh PWM đều bị ép về 0. Bạn triển khai được máy trạng thái này bằng `enum` và `switch` (hoặc điều kiện theo `enum`) trong C++, cũng như bằng chuỗi `if`/`elif` hoặc từ điển hàm trong MicroPython trên nền vòng lặp không chặn của bài 1, đồng thời loại bỏ hoàn toàn kiểu viết dùng nhiều biến cờ boolean rời rạc có thể cùng bật một lúc.

## Kiến thức cần có

Bạn đã biết tính thời gian trôi qua bằng `millis()` hoặc `time.ticks_diff()` từ bài 1 (thay thế nhịp tim chặn ở [bài serial chương 02]({% multilang_post_url contents/chapter02/02_04_blink_serial_hello %})), biết đọc cạnh nút nhấn và xuất PWM bằng `ledcWrite` hoặc `duty_u16` mà không dựa vào `analogWrite` mặc định. Trong bài này, đèn LED từ bài GPIO đóng vai trò chỉ báo "động cơ đang được phép chạy"; mạch TB6612 vẫn chưa được nối.

## Vì sao bài này quan trọng

Firmware điều khiển từ xa (teleop) của Capstone A không nên là tập hợp các câu lệnh `if` rời rạc. Tại mọi thời điểm, robot chỉ ở một trong ba tình huống: đang chờ (`IDLE`), đang chạy theo lệnh còn hạn (`TELEOP`), hoặc đã dừng an toàn do mất lệnh (`FAULT`). Tín hiệu PWM là ngõ ra phụ thuộc trực tiếp vào trạng thái hiện tại, tránh bị khối lệnh khác ghi đè ngoài ý muốn. Khi tích hợp với ROS ở các chương sau, cơ chế này bảo đảm cả hai kênh TB6612 luôn về duty 0 trong `IDLE` và `FAULT`. Ngược lại, cách viết dùng hai biến boolean độc lập (như cờ nháy đèn và cờ chạy động cơ) có thể để cả hai cùng bằng `true`, khiến robot vẫn chạy trong khi đèn báo trạng thái lỗi đang nháy.

## Nội dung

Máy trạng thái (state machine) gồm một biến duy nhất biểu diễn trạng thái hiện tại cùng bộ quy tắc chuyển trạng thái theo từng sự kiện. Firmware trong bài có ba trạng thái:

- **IDLE:** chưa cho phép chạy. Cả hai kênh PWM bằng 0 và LED chỉ báo tắt. Khi nhận được lệnh hợp lệ, máy chuyển sang `TELEOP`.
- **TELEOP:** đang nhận lệnh còn hiệu lực. Các kênh PWM cập nhật theo lệnh và mỗi lệnh mới làm mới mốc thời gian `lastCmd`. Nếu khoảng thời gian im lặng đạt 300 ms, máy chuyển sang `FAULT`.
- **FAULT:** đường truyền lệnh bị gián đoạn hoặc hệ thống đã ngắt an toàn. Cả hai kênh PWM bị ép về 0 và LED tắt. Để thoát khỏi `FAULT`, người vận hành bắt buộc phải nhấn nút xác nhận để quay về `IDLE` — không nhảy thẳng về `TELEOP`. Mọi lệnh gửi tới khi đang ở `FAULT` đều bị bỏ qua để tránh việc kết nối tự phục hồi làm robot bất ngờ chạy tiếp theo lệnh cũ.

![IDLE, TELEOP và FAULT, với mũi tên 300 ms]({{ site.imgurl }}/generated/firmware_state_machine.png)

Cấu trúc **cần tránh** dùng các cờ boolean độc lập:

```cpp
bool blinkMode = true;
bool motorsOn = true;

void loop() {
  if (blinkMode) { /* đảo LED */ }
  if (motorsOn) { ledcWrite(18, 200); }
}
```

Vì `blinkMode` và `motorsOn` là hai biến tách biệt, không có cơ chế nào ngăn chúng cùng mang giá trị `true` trong cùng một vòng lặp, dẫn đến đèn báo nháy trong khi chân PWM vẫn xuất 200. Khi thêm cờ thứ ba cho timeout, số tổ hợp trạng thái tăng lên 8 và rất khó kiểm thử hết. Dùng một `enum` duy nhất giới hạn hệ thống trong đúng 3 trạng thái và gom toàn bộ việc xuất PWM về một chỗ duy nhất.

**C++ cho lõi Arduino ESP32:** LED trên GPIO 18 chỉ sáng khi ở `TELEOP` với `duty > 0` (kênh thứ hai được mô phỏng bằng chú thích để giữ đúng nguyên tắc "cả hai kênh"). Lệnh qua serial rút gọn thành một ký tự: `F` là tiến ở mức 40% thang (102/255), `S` là lệnh dừng chủ động từ người vận hành để về `IDLE` với duty 0. Sự im lặng (không có ký tự mới sau 300 ms) khác hoàn toàn với `S`.

```cpp
const int LED = 18;
const int BTN = 4;
const uint32_t TIMEOUT_MS = 300;

enum class Mode : uint8_t { Idle, Teleop, Fault };
Mode mode = Mode::Idle;

uint32_t lastCmd = 0;
int duty = 0;  // 0..255, vai cả hai kênh TB6612

void setup() {
  pinMode(LED, OUTPUT);
  pinMode(BTN, INPUT_PULLUP);
  Serial.begin(115200);
  Serial.println("state IDLE duty 0");
}

void apply() {
  bool enabled = (mode == Mode::Teleop) && duty > 0;
  digitalWrite(LED, enabled ? HIGH : LOW);
  // Sau này: ledcWrite(PWMA, enabled ? duty : 0); ledcWrite(PWMB, enabled ? duty : 0);
}

void loop() {
  uint32_t now = millis();
  static int prevBtn = HIGH;
  int btn = digitalRead(BTN);
  bool btnPress = (btn == LOW && prevBtn == HIGH);
  prevBtn = btn;

  if (Serial.available()) {
    char c = Serial.read();
    if (c == 'F' || c == 'S') {
      if (mode == Mode::Idle) {
        mode = Mode::Teleop;
      }
      if (mode == Mode::Teleop) {
        lastCmd = now;
        duty = (c == 'F') ? 102 : 0;  // khoảng 40% của 255, hoặc lệnh dừng
        if (c == 'S') mode = Mode::Idle;
      }
      // Trong FAULT, ký tự bị bỏ qua có chủ đích.
    }
  }

  if (mode == Mode::Teleop && (now - lastCmd) >= TIMEOUT_MS) {
    mode = Mode::Fault;
    duty = 0;
  }
  if (mode == Mode::Fault && btnPress) {
    mode = Mode::Idle;
    duty = 0;
  }
  apply();
}
```

Trong hàm `apply()`, điều kiện `enabled` yêu cầu trạng thái phải là `Mode::Teleop`, nên `IDLE` và `FAULT` không bao giờ bật LED (hoặc xuất PWM khác 0). Khi hết hạn 300 ms, `duty` cũng được gán về 0 để không lưu giá trị cũ. Cạnh nút ở đoạn mã trên viết gọn để tập trung vào máy trạng thái; trong thực tế bạn nên kết hợp với bộ lọc chống dội 20 ms của bài GPIO và tuyệt đối không thêm `delay` vào nhánh `FAULT`.

**MicroPython:** có thể ánh xạ mỗi trạng thái tới một hàm xử lý thông qua từ điển `HANDLERS`. Mỗi vòng lặp chỉ gọi đúng một hàm `HANDLERS[state]` nên hai trạng thái không thể chạy đồng thời.

```python
from machine import Pin
import time

led = Pin(18, Pin.OUT)
btn = Pin(4, Pin.IN, Pin.PULL_UP)
TIMEOUT_MS = 300

state = "IDLE"
last_cmd = time.ticks_ms()
duty = 0
prev_btn = 1

def apply():
    enabled = state == "TELEOP" and duty > 0
    led.value(1 if enabled else 0)

def on_idle(now, cmd, pressed):
    global state, last_cmd, duty
    if cmd == "F":
        state, duty, last_cmd = "TELEOP", 40, now
    elif cmd == "S":
        duty = 0

def on_teleop(now, cmd, pressed):
    global state, last_cmd, duty
    if cmd == "F":
        duty, last_cmd = 40, now
    elif cmd == "S":
        state, duty = "IDLE", 0
    elif time.ticks_diff(now, last_cmd) >= TIMEOUT_MS:
        state, duty = "FAULT", 0

def on_fault(now, cmd, pressed):
    global state, duty
    duty = 0
    if pressed:
        state = "IDLE"

HANDLERS = {"IDLE": on_idle, "TELEOP": on_teleop, "FAULT": on_fault}

while True:
    now = time.ticks_ms()
    cmd = None
    # Cổng serial bài dạy có thể là sys.stdin; phần lab nêu một kiểu.
    level = btn.value()
    pressed = level == 0 and prev_btn == 1
    prev_btn = level
    HANDLERS[state](now, cmd, pressed)
    apply()
    time.sleep_ms(1)
```

Ngoài cách dùng từ điển hàm, một chuỗi `if`/`elif` theo `state` cũng hợp lệ. Điều cần tránh là tạo một trạng thái `SLEEP` rồi gọi `time.sleep` hoặc `delay` bên trong: ngủ chặn không phải là trạng thái vận hành mà là khoảng mù khiến đồng hồ không được kiểm tra.

Phân biệt rõ `S` và `FAULT`: `S` là lệnh dừng chủ động (về `IDLE`, không cần nhấn nút xác nhận), còn `FAULT` dành cho trường hợp mất kết nối hoặc mất luồng lệnh (bắt buộc nhấn nút mới được phép nhận lệnh lại). Trong ví dụ tính tay bên dưới, ký hiệu `F 40` thể hiện rõ mức 40%; khi thực hành trên Serial Monitor, gõ gọn một chữ `F` đã gắn sẵn mức 40% đó.

Về sau, một client [micro-ROS](https://micro.ros.org/) có thể gửi trực tiếp các lệnh vận tốc vào chính máy trạng thái này: mỗi bản tin mới sẽ làm tươi `lastCmd`, còn logic chuyển sang `FAULT` và ép PWM về 0 vẫn giữ nguyên trên vi điều khiển.

## Ví dụ tính tay

Hệ thống khởi động ở trạng thái `IDLE`: LED tắt, hai kênh PWM bằng 0. Tại $t = 0$, cổng serial nhận `F 40`: máy chuyển sang `TELEOP`, cập nhật `lastCmd = 0` và đặt duty 40% (tương đương $0{,}40 \times 255 = 102$ trên thang LEDC 8-bit). LED bật sáng; nếu đã nối driver thì cả hai kênh A và B đều nhận mức 102.

Sau đó không có ký tự nào gửi thêm. Tuổi lệnh là $t - 0$, và điều kiện quá thời gian là:

$$
t - t_{\text{cmd}} \ge 300\,\mathrm{ms}.
$$

Ngay ở lượt lặp đầu tiên thỏa điều kiện này, máy chuyển sang `FAULT`, gán `duty = 0` và tắt LED. Nếu gõ thêm `F` trong lúc đang ở `FAULT`, lệnh bị bỏ qua và duty vẫn bằng 0. Khi người vận hành nhấn nút xác nhận, máy chuyển về `IDLE` với duty vẫn bằng 0; chỉ khi nhận một lệnh `F` mới ở trạng thái `IDLE`, LED mới sáng trở lại.

Nếu trong `TELEOP` có chèn `delay(200)`, kết quả tính tay từ bài 1 lặp lại y nguyên: lần đầu vòng lặp phát hiện quá hạn là tại 400 ms, khiến LED (và về sau là TB6612) duy trì mức 102 thêm 100 ms ngoài giới hạn cho phép.

## Bài lab

Không nối động cơ, không nối VM và không nối pin. LED đại diện cho trạng thái "động cơ được phép chạy", còn Serial Monitor đóng vai trò tay điều khiển.

1. Nạp mã C++ (hoặc nối các hàm MicroPython với luồng đọc serial để ký tự gõ vào gán cho `cmd`). Xác nhận lúc mới khởi động màn hình báo `IDLE` và LED tắt.
2. Gõ `F`: LED sáng và log (nếu in thêm) báo `TELEOP` với duty 102 (hoặc 40 ở bản Python). Gõ `S`: LED tắt và trạng thái quay về `IDLE`.
3. Gõ `F` lần nữa rồi ngừng gõ. Trong khoảng 300 ms, LED phải tự tắt và máy chuyển sang `FAULT`. Nếu LED vẫn sáng, kiểm tra xem đồng hồ có bị bỏ qua hoặc có lệnh ngủ dài hơn 300 ms hay không. Thử gõ `F` khi đang ở `FAULT` và xác nhận LED vẫn tắt.
4. Nhấn nút xác nhận: trạng thái chuyển về `IDLE`, duty vẫn bằng 0. Chỉ khi gõ thêm một chữ `F` mới thì LED mới sáng lại.
5. Vẽ lại sơ đồ ba trạng thái cùng mũi tên timeout 300 ms vào sổ tay và ghi rõ câu "PWM bằng không trong FAULT" để phục vụ checklist cuối chương.

Nếu LED sáng ngay khi vừa khởi động, hãy kiểm tra xem `apply()` có bị bỏ sót điều kiện `TELEOP` hay `setup()` đã xuất sẵn một mức PWM cố định hay không.

## Video tham khảo

- **Xem trước:** [Understanding State Machines, Part 1: What Are They?](https://www.youtube.com/watch?v=-Yicg2TTMPs) — MATLAB, tiếng Anh. Trình bày khái niệm trạng thái, sự kiện và chuyển trạng thái — khớp trực tiếp với ba trạng thái chờ, chạy và lỗi của firmware teleop.
- [Finite State Machines: The Embedded Trick That Changes Everything](https://www.youtube.com/watch?v=CbNXEyYL_f8) — AsabreTech, tiếng Anh. Ứng dụng máy trạng thái hữu hạn từ góc nhìn lập trình firmware nhúng.

## Bài tập

1. Lần theo chuỗi sự kiện sau và ghi lại trạng thái cùng giá trị duty sau mỗi bước: vừa khởi động; nhận `F`; im lặng 300 ms; nhận `F` khi chưa nhấn nút; nhấn nút; nhận `F`.
2. Một sinh viên thêm trạng thái `Mode::Sleep` và gọi `delay(1000)` bên trong "để robot nghỉ". Sự kiện nào bị bỏ lỡ trong khoảng thời gian đó, và TB6612 sẽ phản ứng ra sao nếu duty trước khi ngủ khác 0?
3. Vì sao mọi lệnh nhận được khi đang ở trạng thái `FAULT` phải bị bỏ qua thay vì coi là tín hiệu cho thấy kết nối đã khôi phục?
4. Hãy đề xuất cách viết lại đoạn mã hai biến boolean (`blinkMode` và `motorsOn`) thành một biến duy nhất sao cho tình huống "vừa nháy đèn lỗi vừa chạy động cơ" không thể xảy ra.

<details>
<summary>Gợi ý</summary>

1. `IDLE` (duty 0) $\rightarrow$ `TELEOP` (duty 102 hoặc 40%) $\rightarrow$ `FAULT` (duty 0) $\rightarrow$ vẫn `FAULT` (duty 0) sau lệnh `F` thứ hai $\rightarrow$ `IDLE` (duty 0) sau khi nhấn nút $\rightarrow$ `TELEOP` (duty 102) sau lệnh `F` cuối.
2. Trong suốt `delay(1000)`, điều kiện im lặng 300 ms không được kiểm tra. Nếu không ép duty về 0 trước khi ngủ, cả hai kênh PWM vẫn giữ mức cũ suốt 1 giây.
3. `FAULT` đòi hỏi xác nhận chủ động từ con người để bảo đảm an toàn; nếu tự động chạy lại ngay khi gói tin đến trở lại sau sự cố mất sóng, robot có thể di chuyển bất ngờ khi không ai kiểm soát.
4. Xóa bỏ `blinkMode` và `motorsOn`, thay bằng một biến `Mode` duy nhất (`Idle`, `Teleop`, `Fault`) và chỉ cho phép bật ngõ ra trong nhánh `Teleop` của hàm `apply()`.

</details>

## Đọc thêm

- [`millis()`](https://www.arduino.cc/reference/en/language/functions/time/millis/) — bộ định thời cho phép so sánh timeout trong bản C++, đảm bảo phép trừ `now - lastCmd` luôn đúng khi tràn bộ đếm.
- [micro-ROS](https://micro.ros.org/) — nền tảng giao tiếp ROS cho vi điều khiển sẽ cung cấp các sự kiện lệnh cho máy trạng thái này ở các chương sau.
