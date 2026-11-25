---
layout: post
title: "Checklist lab chương 03"
chapter: "03"
order: 6
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter03
lesson_type: required
draft: false
---

## Mục tiêu

Bài kiểm tra này chốt lại chương 03 bằng các bằng chứng thực tế thay vì đánh dấu hoàn thành theo cảm tính. Bạn cần xuất trình được log serial của nút nhấn, các dòng duty PWM (hoặc ảnh LED ở hai mức độ sáng rõ rệt), kết quả đếm chống dội khớp số lần nhấn với sai số bằng 0, và sơ đồ máy trạng thái có mũi tên quá thời gian ghi rõ 300 ms. Bạn chỉ được ghi câu "PWM bằng không trong FAULT" khi mã nguồn thực sự ép ngõ ra về 0, và biết cách bác bỏ một bản báo cáo đánh dấu đạt PWM trong khi lệnh `ledcWrite` duy nhất chỉ nằm trong `setup()`.

## Kiến thức cần có

Danh sách này kiểm chứng kết quả từ bài 1 đến bài 5: vòng lặp không chặn (thay thế [nhịp tim chương 02]({% multilang_post_url contents/chapter02/02_04_blink_serial_hello %})), nút nhấn kéo lên, PWM bằng LEDC hoặc `duty_u16`, ISR ngắn gọn và máy trạng thái `IDLE` / `TELEOP` / `FAULT`. Nếu chưa có phần cứng, bạn chưa được tính đạt chương; chỉ được kiểm tra sơ bộ trên mã nguồn đã viết hoàn chỉnh khi trích dẫn được đúng dòng kiểm tra timeout và dòng ép duty về 0.

---

Chương 03 là bước ngoặt biến bo mạch thụ động thành một "bộ não nhúng" thực thụ biết đọc nút nhấn chống dội, phát xung PWM không rít, đếm xung ngắt tốc độ cao và chuyển trạng thái có kỷ luật. **Checklist Chương 03** giúp bạn kiểm chứng độ mượt thời gian thực (*jitter*, tốc độ đáp ứng) của toàn bộ tầng firmware trước khi nối các cảm biến bus số I2C/SPI/UART ở Chương 04.

## Kiến thức cần nhớ: Kiểm chứng Tính Thời gian thực của Firmware (Firmware Verification)

1. **Đo Độ giật Chu kỳ (Loop Jitter):** Một vòng lặp thiết kế ở 50 Hz ($$20\text{ ms}$$) chỉ đạt chuẩn khi khoảng cách giữa các lần thực thi thực tế tập trung chặt quanh $$20\text{ ms}$$ (sai lệch $$< 5\text{–}10\%$$) mà không có gai vọt bất thường.
2. **Kiểm chứng Xung & Ngắt Bằng Con số:** Kiểm tra tỷ lệ mất xung encoder khi quay tay đúng 1 vòng bánh xe (so sánh số xung đếm được với số khe đĩa lý thuyết).
3. **Kiểm thử Chuyển Trạng thái & Dừng Khẩn cấp (E-Stop):** Xác minh mọi mũi tên trong bảng FSM hoạt động đúng như thiết kế và trạng thái `ESTOP` luôn thắng mọi trạng thái khác.

### Ví dụ làm từng bước: Soi nhật ký Serial để phát hiện lỗi độ giật (Jitter) trong vòng lặp 50 Hz

Xét hai đoạn nhật ký dấu thời gian `t_ms` in ra từ hai bản firmware cùng đặt chu kỳ mục tiêu $$20\text{ ms}$$:
- **Firmware ĐẠT:** `t_ms = [1000, 1020, 1041, 1060, 1080]` → các khoảng chu kỳ $$\Delta t = [20,\ 21,\ 19,\ 20]\text{ ms}$$. Trung bình $$20.0\text{ ms}$$, độ giật cực đại chỉ **$$\pm 1\text{ ms}$$ (5%)**!
- **Firmware CHƯA ĐẠT:** `t_ms = [1000, 1020, 1185, 1205, 1225]` → xuất hiện một gai **$$\Delta t = 165\text{ ms}$$** (vọt gấp **8,25 lần** chu kỳ chuẩn!). Nguyên nhân thường là một hàm đọc cảm biến bị treo chờ timeout, một lần in Serial dài làm đầy bộ đệm, hoặc một câu lệnh `delay()` bị bỏ quên trong nhánh phụ!

### Giải thích: 4 bước nghiệm thu sạch tầng Firmware Chương 03

1. **Bước 1 — Chạy kiểm thử xoay bánh xe 1 vòng thủ công:** Đánh dấu 1 vạch bút trắng trên bánh xe, xoay tay đúng 1 vòng $$360^\circ$$ và kiểm tra biến `ticks` khớp số xung lý thuyết (ví dụ 20 hoặc 80 xung) với sai số $$\le 1$$ xung.
2. **Bước 2 — Kiểm tra chống dội bằng 10 lần bấm nhanh liên tiếp:** Đếm trên Serial phải tăng đúng từ 0 lên 10, không nhảy cóc thành 13 hay 17.
3. **Bước 3 — Kiểm tra PWM bằng LED hoặc động cơ ở 3 mức (0%, 50%, 100%):** Xác minh tần số 20 kHz không rít và mức 0% tắt hẳn hoàn toàn.
4. **Bước 4 — Thử bấm `ESTOP` ngay giữa trạng thái `RUN` và `AVOID`:** Đảm bảo log in chuyển về `ESTOP` tức thì và bánh xe cắt điện ngay lập tức.

**Kiểm tra nhanh.** Khi xoay tay bánh xe đúng **5 vòng**, encoder có 20 khe (đọc 1 cạnh) lý thuyết phải đếm được $$5 \times 20 = 100$$ xung, nhưng firmware chỉ đếm được `92` xung (mất 8%). Bạn nên kiểm tra gì đầu tiên? Kiểm tra xem có vô tình đặt hàm `debounce` quá lớn lên chân encoder, hoặc có đặt `Serial.print()` trong ISR làm trễ mất xung hay không!

---

## Vì sao bài này quan trọng

Các chương tiếp theo mặc định rằng firmware vi sai của bạn đã nhận lệnh teleop và tự động ngắt cả hai kênh PWM khi mất lệnh 300 ms. Hệ thống ROS ở tầng trên sẽ gửi lệnh vận tốc dựa trên giả định đó và không thể phát hiện ra việc nút nhấn bị nhiễu, duty chỉ ghi một lần khi khởi động, hay trạng thái `FAULT` quên ghi 0 ra chân PWM. Quy tắc nhấc bánh khỏi bàn vẫn được duy trì cho đến khi toàn bộ các mục kiểm chứng này được ghi nhận đầy đủ trong sổ thực hành.

## Nội dung

Mỗi mục kiểm tra yêu cầu một kết quả quan sát cụ thể kèm bằng chứng (log hoặc ảnh) trong sổ lab. Bạn chỉ cần thực hiện bằng ngôn ngữ mình chọn cho Capstone A (C++ hoặc MicroPython), nhưng mã nguồn bắt buộc phải tuân theo cấu trúc vòng lặp không chặn ở bài 1; bất kỳ bài nộp nào còn dùng `delay(1000)` trong vòng điều khiển đều không đạt dù đèn LED có sáng tắt.

- **Mục nút nhấn:** dán đoạn log từ bài GPIO thể hiện đúng một `press` và một `release` cho mỗi lần thao tác (không in liên tục mỗi mili giây), ghi kèm số chân GPIO và cấu hình `INPUT_PULLUP` hoặc `Pin.PULL_UP`. Nếu có thử nghiệm chân nổi trước đó, cần ghi rõ log nộp là kết quả sau khi đã bật kéo lên.
- **Mục PWM:** ảnh chụp cùng một đèn LED ở hai mức tối và sáng rõ rệt, hoặc ba dòng log serial thể hiện duty khoảng 25%, 50% và 90% theo đúng độ phân giải đã cấu hình (ghi rõ `ledcAttach` kèm số bit, hoặc `duty_u16`). Tải trong ảnh phải là LED nối tiếp điện trở; gắn động cơ trực tiếp vào GPIO là không đạt ngay cả khi động cơ quay.
- **Mục chống dội:** ghi rõ số lần nhấn thực tế $N$ và số lần bộ đếm in ra khớp nhau với sai số bằng 0:

$$
e = N_{\mathrm{in}} - N_{\mathrm{nhấn}} = 0.
$$

Có thể đính kèm log thử nghiệm khi bỏ bộ lọc (nhảy 5–30 nhịp mỗi lần nhấn) ở bên dưới để đối chiếu, nhưng không thay thế được kết quả $e = 0$. Nếu vẫn bị đếm thừa, cần quay lại chỉnh bộ lọc 20 ms.

- **Mục sơ đồ máy trạng thái:** tự vẽ lại sơ đồ trong sổ (không chỉ chụp lại hình bài giảng) gồm đủ ba trạng thái, mũi tên từ `TELEOP` sang `FAULT` ghi đúng 300 ms, và cả `IDLE` lẫn `FAULT` đều đánh dấu duty 0. Ghi câu "PWM bằng không trong FAULT" chỉ khi hàm `apply()` thực sự khóa ngõ ra về 0 ngoài trạng thái `TELEOP`.

![Thứ tự cấp nguồn: logic trước, nguồn motor sau, bánh nhấc]({{ site.imgurl }}/generated/power_order.png)

Sơ đồ thứ tự cấp nguồn nhắc lại giới hạn của chương 03: USB nuôi vi điều khiển, đường 3,3 V nuôi nút kéo lên và LED, còn nguồn động cơ (`VM` trên TB6612) vẫn để trống. Hoàn thành checklist chương 03 không đồng nghĩa với việc đã được đấu dây động cơ.

## Ví dụ tính tay: phát hiện một checklist chưa đạt

Xét một bài nộp đánh dấu hoàn thành cả bốn mục (nút nhấn, PWM, chống dội, máy trạng thái) nhưng mã nguồn đính kèm chỉ gồm:

```cpp
const int PIN = 18;

void setup() {
  Serial.begin(115200);
  ledcAttach(PIN, 1000, 8);
  ledcWrite(PIN, 180);
  Serial.println("PWM done");
}

void loop() {
  delay(1000);
  Serial.println("still on");
}
```

Khi đối chiếu với các tiêu chí: không có nút nhấn nên không thể có log nhấn hay kết quả chống dội; `ledcWrite` chỉ chạy một lần duy nhất trong `setup()` ở mức cố định 180 (khoảng 70%) và không bao giờ đưa về 0; `loop()` không đọc `millis()` và bị chặn bởi `delay(1000)`, lớn hơn nhiều so với ngưỡng cắt:

$$
1000\,\mathrm{ms} > 300\,\mathrm{ms}.
$$

Dòng in `PWM done` chỉ là chuỗi văn bản cố định, không phải bằng chứng đo kiểm. Nếu chấp nhận bài nộp này, khi lắp động cơ vào robot sẽ chạy ngay lập tức lúc khởi động và không thể dừng khi mất lệnh. Bài chỉ đạt sau khi mã nguồn cập nhật duty từ máy trạng thái mỗi vòng lặp, không chặn `loop()`, có mức duty 0 và tắt LED khi ngừng gõ lệnh.

Một lỗi tinh vi hơn cũng cần kiểm tra: chương trình có máy trạng thái đầy đủ, nhưng `setup()` đã gọi `ledcWrite(PIN, 180)` và nhánh `FAULT` chỉ gán biến `duty = 0` mà không gọi lại `ledcWrite(PIN, 0)`. Ngoại vi PWM phần cứng vẫn giữ nguyên xung cũ cho đến khi được ghi giá trị mới, nên hàm `apply()` phải gọi tường minh lệnh ghi 0 cho cả hai kênh PWM mỗi khi ở `IDLE` hoặc `FAULT`.

## Nội dung cần nộp trong sổ lab

Kiểm tra lần lượt sáu mục sau trong `lab-notes.md`; mục nào thiếu bằng chứng cụ thể thì giữ ở trạng thái chưa hoàn thành:

1. **Log nút nhấn:** dán một cặp `press`/`release` sạch cho mỗi thao tác, ghi rõ chân GPIO và cấu hình kéo lên.
2. **Bằng chứng PWM:** ảnh LED ở hai mức sáng hoặc log các mức duty quanh 25%, 50%, 90% kèm một dòng duty bằng 0; nêu rõ API (`ledcAttach` + độ phân giải, hoặc `duty_u16`).
3. **Kết quả chống dội:** ghi số lần nhấn $N$ và số lần in $N$ ($e = 0$); có thể ghi thêm số nhịp khi bỏ lọc để đối chiếu.
4. **Sơ đồ máy trạng thái:** đủ ba trạng thái, mũi tên 300 ms sang `FAULT`, đánh dấu duty 0 ở `IDLE` và `FAULT`, kèm câu "PWM bằng không trong FAULT" khớp với hàm `apply()`.
5. **Ngôn ngữ và cấu trúc vòng lặp:** nêu rõ C++ hay MicroPython, xác nhận vòng điều khiển không gọi `delay` hay `sleep` dài hơn vài mili giây và trích hằng số timeout từ mã nguồn.
6. **Xác nhận giới hạn động cơ:** ghi rõ "không nối động cơ vào GPIO, chưa nối VM, luôn nhấc bánh khi lắp driver về sau." (Tham khảo trước cho chương sau: module TB6612 giá 45000₫, dải VM 4,5 V – 10 V, dòng liên tục khoảng 1,2 A tại [Hshop](https://hshop.vn/mach-dieu-khien-dong-co-dc-tb6612fng-dc-motor-driver), nhưng chưa đấu dây trong chương này.)

Nếu bo mạch chưa giao tới, mục 1–3 để trạng thái mở; mục 4 và 5 có thể chuẩn bị trước trên mã nguồn đã biên dịch hoặc kiểm tra cú pháp và ghi nhãn "chỉ mã nguồn" cho đến khi kiểm chứng trên LED thật.

## Video tham khảo

- **Xem trước:** [Understanding State Machines, Part 1: What Are They?](https://www.youtube.com/watch?v=-Yicg2TTMPs) — MATLAB, tiếng Anh. Ôn lại cấu trúc trạng thái và chuyển đổi để đối chiếu với sơ đồ nộp trong checklist.

## Bài tập

1. Đóng vai người chấm bài cho đoạn mã ví dụ ở trên: liệt kê các mục checklist bị trượt và chỉ ra dòng mã khiến câu "PWM bằng không trong FAULT" không đúng sự thật.
2. Sơ đồ của một sinh viên có đủ `IDLE`, `TELEOP` và `FAULT`, nhưng mũi tên quá thời gian lại vẽ từ `IDLE` sang `FAULT` với nhãn "1 s". Sơ đồ này sai ở hai điểm nào?
3. Log chống dội ghi nhận 10 lần nhấn nhưng dòng cuối in `presses=12`. Mục chống dội đã đạt chưa, và cần kiểm tra điểm nào trong mã nguồn của bài 4 trước tiên?
4. `setup()` xuất duty 200, còn nhánh `FAULT` chỉ gán `duty = 0` mà không gọi `ledcWrite`. Sau 300 ms im lặng, tín hiệu thực tế trên chân GPIO là gì và cần sửa gì trong `apply()`?

<details>
<summary>Gợi ý</summary>

1. Trượt các mục: log nút nhấn, bằng chứng PWM nhiều mức và mức 0, kết quả chống dội, sơ đồ máy trạng thái và vòng lặp không chặn (`delay(1000)`). Dòng `ledcWrite(PIN, 180)` trong `setup()` mà không có lệnh ghi 0 nào về sau làm câu "PWM bằng không trong FAULT" sai.
2. Sai thứ nhất: kiểm tra mất lệnh chỉ áp dụng khi đang ở `TELEOP` (vì `IDLE` vốn đã có duty 0). Sai thứ hai: ngưỡng timeout quy định là 300 ms, không phải 1 s.
3. Chưa đạt vì sai số $e = 2 \neq 0$. Cần kiểm tra bộ lọc ổn định 20 ms bao quanh lệnh tăng bộ đếm và xem cấu hình ngắt `CHANGE` có đang đếm nhầm cạnh nhả hay không.
4. Chân GPIO vẫn tiếp tục phát xung PWM ở mức duty 200. Hàm `apply()` phải gọi tường minh `ledcWrite` với giá trị 0 mỗi khi trạng thái là `FAULT` hoặc `IDLE`.

</details>

## Đọc thêm

- [`millis()`](https://www.arduino.cc/reference/en/language/functions/time/millis/) — hàm định thời dùng để kiểm chứng mũi tên timeout 300 ms trong mã nộp.
- [LEDC trên Arduino ESP32](https://docs.espressif.com/projects/arduino-esp32/en/latest/api/ledc.html) — tài liệu đối chiếu giá trị ghi duty với độ phân giải đã cấu hình.
- [micro-ROS](https://micro.ros.org/) — tầng giao tiếp sẽ tích hợp lên firmware đã qua checklist này, nhưng vẫn giữ nguyên yêu cầu ép PWM về 0 tại `FAULT`.
