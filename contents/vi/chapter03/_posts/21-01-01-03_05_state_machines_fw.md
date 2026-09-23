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

Hết bài này bạn dựng được ba trạng thái firmware, IDLE, TELEOP và FAULT, sao cho một lệnh, một khoảng im 300 ms, và một nút mỗi thứ làm đúng một việc. Ở IDLE và ở FAULT, cả hai kênh PWM bị ra lệnh về 0. Bạn viết máy đó bằng `enum` và `switch` trong C++, và bằng chuỗi `if`/`elif` hoặc một từ điển các hàm trong MicroPython, dùng đồng hồ không chặn của bài 1 chứ không dùng một giấc ngủ đóng vai trạng thái. Bạn cũng bỏ kiểu cờ nhấp LED và cờ động cơ có thể cùng đúng một lúc.

## Kiến thức cần có

Bạn đo được tuổi lệnh bằng `millis()` hoặc `time.ticks_diff()`, đúng kỹ năng bài 1 đã đặt vào chỗ nhịp tim chặn của [lab serial chương 02]({% multilang_post_url contents/chapter02/02_04_blink_serial_hello %}). Bạn in được một cạnh nút, và ghi được một duty bằng `ledcWrite` hoặc `duty_u16` mà không tin `analogWrite` luôn là 0–255 trên ESP32. LED của bài GPIO sẽ đứng vai "động cơ đang được phép." TB6612 vẫn chưa đấu. Phép toán timeout bạn đang mã hóa là cùng quy tắc 300 ms mà bài 1 đã tính cho ca ngủ 200 ms bị trễ.

## Vì sao bài này quan trọng

Teleop Capstone A không phải một đống `if` độc lập. Đế vi sai hoặc đang chờ, hoặc đang chạy theo một lệnh còn tươi, hoặc đang dừng vì lệnh đã chết. Đó là các trạng thái, và các chân PWM là ngõ ra của trạng thái, không phải hiệu ứng phụ mà một khối khác có thể ghi đè. Khi ROS sau này giao lệnh vận tốc, firmware bạn muốn đã biết làm gì với "một lệnh vừa tới" và với "không có gì tới trong 300 ms": cả hai kênh TB6612 về duty 0 trong FAULT, và chúng ở 0 trong IDLE. Bánh nhấc lên trong lúc bạn chứng minh điều đó trên một LED. Một sketch vừa nhấp đèn vừa ghi duty động cơ, bằng hai boolean có thể cùng đúng, sẽ vừa chạy vừa nhấp trong trạng thái bạn tưởng là lỗi.

## Nội dung

Máy trạng thái là một biến gọi đúng một tình huống, cộng một luật cho từng sự kiện đổi cái tên đó. Firmware này có ba tên.

IDLE nghĩa là chưa được phép chạy. Cả hai kênh PWM bằng 0. LED đứng vai "động cơ đang được phép" thì tắt. Một lệnh hợp lệ là sự kiện rời IDLE.

TELEOP nghĩa là vừa có lệnh, còn mới. Các duty đi theo lệnh đó. Mỗi lệnh mới làm tươi một mốc thời gian. Nếu tuổi của mốc ấy đạt 300 ms, sự kiện là im lặng, và trạng thái kế là FAULT.

FAULT nghĩa là đường truyền trông đã chết, hoặc bạn đã quyết định chưa cho chạy. Cả hai kênh PWM lại bằng 0. LED tắt. Sự kiện rời FAULT là một lần nhấn nút, và nó về IDLE, không nhảy thẳng vào TELEOP. Lệnh tới trong FAULT không làm bánh chuyển. Người vận hành phải xác nhận bằng nút, rồi gửi lệnh mới từ IDLE. Bước thừa đó là cố ý: một cần điều khiển vừa nối lại không được tự tiếp tục chuyển động cuối.

![IDLE, TELEOP và FAULT, với mũi tên 300 ms]({{ site.imgurl }}/generated/firmware_state_machine.png)

Cấu trúc cấm trông ngắn hơn và hỏng khi ghép:

```cpp
bool blinkMode = true;
bool motorsOn = true;

void loop() {
  if (blinkMode) { /* đảo LED */ }
  if (motorsOn) { ledcWrite(18, 200); }
}
```

Không gì giữ `motorsOn` và một lỗi ở hai phía đối lập, vì chúng không phải một biến. Cả hai điều kiện có thể đúng trên cùng một vòng, nên đèn nhấp trong lúc duty 200 vẫn đang được ghi. Sau khi bạn thêm cờ thứ ba cho timeout, bảng chân trị có tám hàng và bạn sẽ không thử hết. Một `enum` có ba hàng. `switch` ghi PWM ở một chỗ.

C++ cho lõi Arduino ESP32. LED trên GPIO 18 chỉ sáng trong TELEOP. Kênh thứ hai được tính và in để luật "cả hai kênh" hiện ra, nhưng chỉ cần một LED thật. Lệnh serial là một chữ: `F` nghĩa là tiến ở duty 40, `S` nghĩa là người vận hành bảo dừng và máy về IDLE với duty 0. Im lặng không phải `S`. Im lặng là sự vắng mặt của cả hai chữ.

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

Đọc `apply` trước khi đọc các chuyển trạng thái. IDLE và FAULT không thể thắp LED, vì `enabled` đòi TELEOP. Một duty còn sót từ lần `F` trước bị đẩy ra khỏi chân bởi điều kiện đó, và timeout cũng cất 0 để một lỗi sau không hồi sinh nó. Cạnh nút ở đây là lần hỏi đơn giản của bài GPIO; bạn đã biết cách đưa nó ra sau phép thử đứng yên 20 ms. Giữ phép thử đó nếu nút kích đôi. Đừng thêm `delay` vào nhánh FAULT.

MicroPython có thể cất cùng các chuyển trạng thái thành các hàm trong một từ điển. Mỗi hàm tự sửa `state` và `duty`. Vòng lặp chỉ gọi `HANDLERS[state]`, nên hai trạng thái không thể chạy trong cùng một vòng.

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

Từ điển là điểm của bản Python: `HANDLERS[state]` là một hàm. Một chuỗi `if`/`elif` trên `state` cũng chấp nhận được và đôi khi dễ đọc hơn ở bản nháp đầu. Cái không chấp nhận là một trạng thái `SLEEP` mà thân nó gọi `time.sleep` hoặc `delay`. Ngủ không phải một trạng thái của robot. Nó là một lỗ trên đồng hồ. Bài tập cuối bài nhờ bạn nhận cái bẫy đó trước khi nó lọt vào sketch chạy xe.

Các chữ lệnh cố ý nhỏ. `F` là "cả hai bánh tiến ở duty tập," trên đế vi sai thì đó là đi thẳng. `S` là "tôi bảo bạn dừng," tức là IDLE, không phải FAULT. FAULT dành cho trường hợp dòng lệnh của người vận hành biến mất. Trộn hai thứ đó thì một lần dừng có chủ đích trông như lỗi rồi cần nút, hoặc một radio chết trông như đã đỗ sạch. Vết ở mục sau dùng cụm `F 40` để duty hiện trong câu; chữ `F` một mình của lab là cùng lệnh ấy với 40% đã nướng sẵn, vì gõ trên monitor serial đã đủ vụng.

Về sau, một client micro-ROS có thể giao đúng các sự kiện máy này đã hiểu. Một topic vận tốc chỉ là một nguồn các lệnh kiểu `F` với tải phong phú hơn. Firmware không cần một câu chuyện timeout mới khi client đó tới; nó cần client làm tươi `lastCmd` và các trạng thái bạn viết ở đây tiếp tục ép PWM về 0. Trang [micro.ros.org](https://micro.ros.org/) là nơi client đó được ghi. Một câu báo trước là đủ cho tới chương ROS.

## Ví dụ tính tay

Bắt đầu ở IDLE. LED tắt, và cả hai kênh ta đang hình dung đều duty 0. Tại $t = 0$ monitor nhận `F 40`. Sự kiện lệnh xảy ra, trạng thái thành TELEOP, `lastCmd` là 0, và duty thành 40% thang đầy. Trên thang LEDC 8 bit đó là $0{,}40 \times 255 = 102$. LED bật. Kênh A và kênh B sẽ cùng là 102 nếu driver đã được gắn. Nó chưa được gắn.

Không còn ký tự nào tới. Tuổi lệnh là $t - 0$. Phép so timeout dùng cùng ngưỡng bài 1:

$$
t - t_{\text{cmd}} \ge 300\,\mathrm{ms}.
$$

Ở vòng đầu tiên điều kiện đó đúng, trạng thái thành FAULT và duty được cất bằng 0. LED tắt. Một `F` gõ muộn trong FAULT không rời FAULT và không trả lại 102. Người vận hành nhấn nút. Sự kiện nút đưa máy về IDLE. Duty vẫn là 0, nên LED tắt cho tới khi một `F` mới tới trong lúc máy đang ở IDLE.

Nếu vòng lặp đã gọi `delay(200)` bên trong TELEOP, ví dụ tính tay của bài 1 áp dụng nguyên: cơ hội đầu để thấy 300 ms là ở 400 ms, và LED (rồi sau này là TB6612) sẽ ở duty 102 thêm 100 ms đó. Mũi tên trên sơ đồ trạng thái ghi 300 ms. Code phải nhìn thấy mũi tên ấy, nghĩa là vòng lặp tiếp tục chạy.

## Bài lab

Không motor, không VM, không pin. LED là "động cơ đang được phép." Monitor serial là cần điều khiển.

1. Nạp listing C++, hoặc nối các handler Python với lần đọc serial USB bạn đã dùng ở chương 02 để một chữ gõ vào điền `cmd`. Xác nhận dòng boot nói IDLE và LED tối.
2. Gõ `F`. LED sáng, và một dòng in bạn thêm nên nói TELEOP cùng duty 102, hoặc 40 ở bản Python. Gõ `S`. LED tắt và trạng thái về IDLE. Đó là người bảo dừng, không phải lỗi.
3. Gõ `F` lần nữa rồi không gõ gì. Trong khoảng 300 ms LED phải tắt và trạng thái phải đọc FAULT. Nếu nó còn sáng, mốc thời gian không được đọc, hoặc một lần ngủ dài hơn timeout. Gõ `F` trong FAULT và xác nhận LED vẫn tối.
4. Nhấn nút. Trạng thái về IDLE và duty vẫn 0. Chỉ một `F` mới sau đó mới được thắp LED.
5. Trong sổ, phác ba bong bóng và mũi tên im lặng, rồi viết câu "PWM bằng không trong FAULT." Checklist hỏi cả hai.

Nếu LED bật ngay khi sketch vừa khởi động, `apply` không bị chặn bởi TELEOP, hoặc `setup` đã ghi một duty và vòng lặp không ghi lại. Lỗi đó là chủ đề của checklist chương.

## Bài tập

1. Đi vết này và nêu trạng thái cùng duty sau mỗi sự kiện: vừa boot; `F`; im 300 ms; `F` lần nữa mà không có nút; nút; `F`.
2. Một bạn thêm `Mode::Sleep` và gọi `delay(1000)` trong nhánh đó "để robot nghỉ." Giải thích sự kiện nào máy không còn thấy, và TB6612 làm gì suốt `delay` nếu duty cuối khác không.
3. Vì sao một lệnh nhận trong FAULT phải bị bỏ qua, thay vì bị coi là bằng chứng đường truyền đã khỏe?
4. Viết lại vòng hai boolean sao cho một biến duy nhất khiến "nhấp đèn trong lúc đang chạy" là không thể. Bạn chỉ cần mô tả biến đó và trạng thái nào, nếu có, sở hữu LED.

<details>
<summary>Gợi ý</summary>

1. IDLE duty 0; TELEOP duty 102 (hoặc 40%); FAULT duty 0; vẫn FAULT duty 0 sau `F` thứ hai; IDLE duty 0 sau nút; TELEOP duty 102 sau `F` cuối.
2. Trong `delay(1000)` mũi tên im lặng 300 ms không được xét. Nếu SLEEP không ép duty về 0 trước khi ngủ, cả hai kênh giữ lệnh trước suốt một giây.
3. FAULT nghĩa là một người phải xác nhận. Một chùm byte sau khi rớt sóng nếu không sẽ cho xe chạy lại khi không ai đang cầm cần.
4. Một giá trị `Mode`, LED chỉ được ghi trong nhánh TELEOP của `apply`. Xóa `blinkMode` và `motorsOn`.

</details>

## Đọc thêm

- [`millis()`](https://www.arduino.cc/reference/en/language/functions/time/millis/) là đồng hồ bên trong phép so timeout của bản C++. Phép trừ không dấu làm `now - lastCmd` còn thật khi bộ đếm quay vòng.
- [micro-ROS](https://micro.ros.org/) là client rồi sẽ giao các lệnh mà máy này đã coi là sự kiện. Timeout ở lại trên vi điều khiển.
