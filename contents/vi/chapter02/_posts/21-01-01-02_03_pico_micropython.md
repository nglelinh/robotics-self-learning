---
layout: post
title: "Raspberry Pi Pico và MicroPython"
chapter: "02"
order: 3
owner: "Nguyen Le Linh"
lang: vi
categories: [chapter02]
lesson_type: required
draft: false
---

## Mục tiêu

Sau bài này, bạn biết cách đưa Raspberry Pi Pico hoặc Pico 2 vào chế độ BOOTSEL để ổ bootloader (`RPI-RP2` trên Pico/RP2040 hoặc `RP2350` trên Pico 2/RP2350) xuất hiện, rồi chép đúng tệp firmware UF2 MicroPython cho từng phiên bản. Bạn cấu hình được Thonny hoặc `mpremote` kết nối tới bo mạch và kiểm tra REPL trả lời phép tính `1 + 1`. Bạn lập trình nháy LED tích hợp ở tần số 2 Hz kèm in bộ đếm, phân biệt rõ `Pin("LED")` trên Pico W / Pico 2 W với GPIO 25 trên Pico bản gốc / Pico 2 không W, đồng thời tránh nạp nhầm tệp UF2 của RP2040 lên Pico 2. Toàn bộ GPIO giữ ở mức 3,3 V và chưa đấu nối động cơ.

## Cần gì trước khi học

Bạn cần đã chọn dòng bo mạch Pico ở bài trước, hoặc muốn tìm hiểu nhanh quy trình làm việc của dòng mạch này. Bạn chỉ cần biết thao tác chép tệp vào ổ đĩa USB và chuẩn bị một cáp micro-USB có truyền dữ liệu. Bài này không sử dụng PlatformIO (công cụ dành cho hướng ESP32). Danh sách linh kiện đầy đủ của robot vẫn nằm ở chương 00 ([Hóa đơn linh kiện và cách mua]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %})).

---

Nếu C++ giống như tự tay điều khiển hộp số sàn để vắt từng mili-giây hiệu năng, thì **Raspberry Pi Pico + MicroPython** giống như việc mở thẳng cửa sổ trò chuyện trực tiếp với phần cứng! Cắm Pico vào máy tính qua chế độ `BOOTSEL`, kéo thả đúng một tệp `.uf2`, và chỉ 10 giây sau bạn đã có dấu nhắc **REPL (`>>>`)** để bật tắt chân GPIO, đọc cảm biến I2C hay thử nghiệm công thức điều khiển ngay lập tức mà không cần chờ biên dịch lại!

## Bản đồ kiến thức nền: Kiến trúc RP2040 và Thực thi MicroPython trên Pico

1. **Bootloader USB Mass Storage (`BOOTSEL`):** Chip RP2040 tích hợp sẵn bootloader trong ROM không bao giờ hỏng: giữ nút `BOOTSEL` khi cắm USB, Pico hiện ra như một ổ USB `RPI-RP2` để kéo thả tệp firmware `.uf2` (phân biệt rõ bản **Pico thường** vs **Pico W** có chip Wi-Fi!).
2. **Thông dịch tương tác (REPL) & Hệ thống tệp nội bộ:** MicroPython chạy trực tiếp trình thông dịch trên RAM/Flash của RP2040; tệp lưu với tên `main.py` trên Pico sẽ tự động chạy ngay khi cấp nguồn độc lập bằng pin (không cần cắm máy tính).
3. **Định thời Không tràn số (`ticks_ms` / `ticks_diff`) & Đường nguồn `VSYS`:** Khác với Python trên PC dùng số nguyên độ chính xác vô hạn, MicroPython dùng bộ đếm 30-bit cho `ticks_ms()` để chạy nhanh không cấp phát bộ nhớ; về nguồn điện, chân **`VSYS`** (1,8 V – 5,5 V) là đầu vào chuẩn cho nguồn pin ngoài qua diode chống ngược tích hợp!

### Ví dụ cầm tay chỉ việc: Tránh lỗi tràn bộ đếm 30-bit trên MicroPython bằng `ticks_diff()`

Trên Raspberry Pi Pico, hàm `time.ticks_ms()` đếm từ $$0$$ đến $$2^{30} - 1 = 1{,}073{,}741{,}823\text{ ms}$$ ($$\approx \mathbf{12.43\text{ ngày}}$$) rồi quay về `0` (*wrap-around*).
- Giả sử ngay trước khi tràn, `t_start = 1_073_741_800`, và $$50\text{ ms}$$ sau bộ đếm quay vòng về `t_now = 26`.
- Nếu bạn viết phép trừ ngây thơ `t_now - t_start`:
  $$
  26 - 1{,}073{,}741{,}800 = \mathbf{-1{,}073{,}741{,}774\text{ ms}} \quad (\text{số âm khổng lồ → vòng lặp treo cứng!}).
  $$
- Dùng chuẩn `time.ticks_diff(t_now, t_start)`: hàm thực hiện phép trừ modulo $$2^{30}$$ có dấu và trả về chính xác **$$+50\text{ ms}$$**!

### Khung giải thích: 4 bước làm chủ Raspberry Pi Pico và MicroPython trên robot (nên đọc chậm)

1. **Bước 1 — Chọn đúng tệp `.uf2` theo phần cứng (Pico vs. Pico W):** Trên Pico thường, LED trên bo nối vào `GP25`; trên **Pico W**, LED nối qua chip Wi-Fi nên phải gọi `Pin("LED", Pin.OUT)` — nạp nhầm bản `.uf2` sẽ không điều khiển được LED!
2. **Bước 2 — Tận dụng REPL để kiểm thử từng linh kiện rời:** Trước khi viết chương trình dài, gõ 3 dòng trực tiếp trong REPL (Thonny) để quét địa chỉ I2C hoặc thử quay từng bánh xe giúp tiết kiệm hàng giờ gỡ lỗi.
3. **Bước 3 — Luôn cấp nguồn pin ngoài vào chân `VSYS`, không cấp vào `3V3`:** Chân `VSYS` đi qua mạch Buck-Boost nội bộ của Pico tạo ra nguồn 3,3 V sạch và có diode bảo vệ khi cắm đồng thời cáp USB (`VBUS`).
4. **Bước 4 — Chừa đường thoát an toàn trong `main.py`:** Chèn `time.sleep(1)` ở đầu `main.py` để nếu code lỡ kẹt vòng lặp vô hạn, bạn vẫn kịp bấm `Ctrl+C` trong Thonny giành lại quyền điều khiển REPL!

**Kiểm tra nhanh.** Một bộ nguồn hạ áp Buck ngoài cấp $$5.0\text{ V}$$ vào chân `VSYS` của Pico, đồng thời bạn cắm cáp USB vào máy tính để xem log. Điều gì bảo vệ dòng điện không chảy ngược từ pin vào cổng USB máy tính? Diode Schottky tích hợp giữa `VBUS` và `VSYS` trên bo Pico sẽ chặn dòng chảy ngược (nhưng nếu cấp nguồn vào chân `VBUS` thay vì `VSYS`, bạn sẽ bỏ qua diode bảo vệ này!).

---

## Vì sao bài này gắn với Capstone A

Nếu chọn Pico làm bộ điều khiển chính, tệp UF2 MicroPython và cửa sổ REPL này sẽ là môi trường phát triển cho firmware điều khiển từ xa (teleop) ở chương 07: nhận lệnh hai bánh, xuất PWM tới mạch cầu H TB6612 và chạy vòng lặp giám sát để đưa cả hai duty về 0 sau khoảng 300 ms không có lệnh mới (với quy tắc nhấc bánh khỏi bàn ở lần thử đầu tiên). MicroPython rút ngắn thời gian kiểm thử vì bạn có thể tương tác trực tiếp với vi điều khiển trước khi chạy tệp hoàn chỉnh. Lưu ý rằng các bản Pico không có chữ W không tích hợp Wi-Fi, nên đến bài kết nối không dây ở chương 08, bạn sẽ cần Pico W, Pico 2 W hoặc chuyển sang ESP32.

## Chế độ BOOTSEL và chọn đúng tệp UF2

Cả RP2040 lẫn RP2350 đều có thể khởi động từ bộ nhớ ROM nạp sẵn (bootloader) thông qua thao tác vật lý: rút hẳn cáp khỏi bo mạch, nhấn giữ nút BOOTSEL, cắm cáp USB vào máy tính trong khi vẫn giữ nút, sau đó thả nút BOOTSEL. Máy tính sẽ nhận diện một ổ đĩa gắn ngoài tương tự USB nhỏ: trên Pico bản gốc và Pico W (chip RP2040), ổ có tên `RPI-RP2`; trên Pico 2 và Pico 2 W (chip RP2350), ổ có tên `RP2350`. Dù tên ổ phân biệt được thế hệ chip RP2040 với RP2350, nó vẫn không phân biệt bản không W với bản có W trong cùng thế hệ, nên bạn luôn phải đối chiếu tên tệp UF2 với đúng nhãn in trên bo mạch.

Tải tệp firmware cho Pico bản gốc (RP2040) tại trang chính thức [MicroPython cho RPI_PICO](https://micropython.org/download/RPI_PICO/), còn Pico 2 (RP2350) dùng tệp riêng tại [MicroPython cho RPI_PICO2](https://micropython.org/download/RPI_PICO2/). Trang tổng hợp [micropython.org/download](https://micropython.org/download/) cũng liệt kê riêng bản dành cho Pico W và Pico 2 W. Hãy chép tệp `.uf2` vào đúng ổ bootloader đó. Ngay sau khi chép xong, ổ đĩa sẽ tự ngắt kết nối và chip khởi động lại vào môi trường MicroPython. Ổ đĩa sẽ không xuất hiện lại trừ khi bạn lặp lại thao tác giữ nút BOOTSEL; việc ổ tự biến mất là dấu hiệu nạp thành công.

Tuyệt đối không nạp tệp của RP2040 lên Pico 2. Bootloader vẫn có thể cho phép chép tệp, nhưng sau đó bo mạch sẽ đứng im và không tạo được cổng REPL. Nếu lỡ nạp nhầm, hãy thực hiện lại thao tác rút cáp, giữ BOOTSEL, cắm cáp rồi chép đúng tệp UF2 của RP2350. Tương tự, nạp nhầm tệp của bản Pico W lên bản không W (hoặc ngược lại) cũng gây lỗi; hãy luôn đối chiếu với dòng chữ in trực tiếp trên bo mạch của bạn.

![Pico gốc: BOOTSEL, USB, LED GPIO 25]({{ site.imgurl }}/wikimedia/Raspberry_Pi_Pico.jpg)

Trước khi chép firmware, hãy xác định ba vị trí mốc trên ảnh và trên mạch thực tế: cổng micro-USB, nút BOOTSEL và đèn LED tích hợp nằm gần cổng USB. Ảnh minh họa là Pico bản gốc với đèn LED nối ở GPIO 25; trên Pico W, đèn không nằm ở chân này.

## Kết nối REPL và điều khiển LED

Thonny là trình soạn thảo thuận tiện vì hiển thị rõ trình thông dịch đang dùng. Sau khi cài đặt và mở Thonny, chọn trình thông dịch **MicroPython (Raspberry Pi Pico)** cùng cổng kết nối tương ứng với bo mạch vừa khởi động lại. Lỗi phổ biến nhất là trình thông dịch vẫn đang trỏ vào Python cục bộ trên laptop: khi đó lệnh `print` vẫn chạy nhưng `import machine` sẽ báo lỗi, dễ gây nhầm lẫn là Pico bị hỏng.

Nếu quen làm việc trên dòng lệnh, bạn có thể dùng `mpremote` (cài qua `pip` trong môi trường cục bộ) để mở cùng phiên REPL đó. Chỉ dùng một trong hai công cụ tại một thời điểm để tránh tranh chấp cổng serial.

Nhấp vào cửa sổ Shell và gõ:

```python
1 + 1
```

Nếu kết quả trả về `2` kèm dấu nhắc mới, kết nối đã sẵn sàng. Trong chế độ Pico của Thonny không cần gọi `Serial.begin`; nếu sau này bạn dùng phần mềm terminal serial thông thường, cổng USB REPL của MicroPython vẫn hoạt động như một thiết bị serial với tốc độ chuẩn 115200 baud.

Chân LED tích hợp là điểm dễ gây nhầm lẫn nhất giữa các phiên bản Pico:

- **Pico bản gốc (RP2040):** LED nối với GPIO 25. Các bản MicroPython gần đây cũng hỗ trợ bí danh `"LED"` cho chân này; nếu `Pin("LED")` báo lỗi `ValueError`, hãy dùng trực tiếp GPIO 25.
- **Pico W:** LED được nối vào chip không dây CYW43439 chứ không nối vào GPIO 25 (lúc này GPIO 25 là chân I/O thông thường). Bắt buộc dùng `Pin("LED")` để bật tắt đèn tích hợp.
- **Pico 2 (RP2350, không W):** giữ cách mắc như bản gốc, đèn người dùng nằm ở GPIO 25.
- **Pico 2 W:** giống Pico W, phải dùng bí danh `"LED"`, không dùng GPIO 25.

Quy tắc thực hành là đọc kỹ nhãn in trên bo mạch trước khi chọn tham số khởi tạo `Pin`.

Bài thực hành yêu cầu tần số nháy 2 Hz: bật 250 ms và tắt 250 ms, tổng chu kỳ là 500 ms:

$$
f = \frac{1}{0{,}250\,\mathrm{s} + 0{,}250\,\mathrm{s}} = 2\,\mathrm{Hz}.
$$

```python
from machine import Pin
import time

# Pico W / Pico 2 W: đèn là Pin("LED"), không phải GPIO 25.
# Pico gốc và Pico 2 (không W): đèn là GPIO 25.
try:
    led = Pin("LED", Pin.OUT)
except ValueError:
    led = Pin(25, Pin.OUT)

n = 0
while True:
    led.value(1)
    time.sleep(0.25)
    led.value(0)
    time.sleep(0.25)
    n += 1
    print(n)
```

Hãy chạy thử trực tiếp từ trình soạn thảo và quan sát đèn trước khi lưu thành `main.py`. Một tệp `main.py` bị lỗi hoặc vòng lặp khóa cứng sẽ tự chạy mỗi lần cấp nguồn, khiến bo mạch có vẻ như bị treo; nếu gặp tình huống này, bạn phải đưa mạch vào lại chế độ BOOTSEL hoặc ngắt chương trình để sửa. Ở bài nháy LED đầu tiên này, dùng `time.sleep` là chấp nhận được vì chỉ cần quan sát nhịp 2 Hz và bộ đếm; sang bài sau, chúng ta sẽ bỏ hàm chặn này để vòng lặp theo dõi được ngưỡng mất lệnh 300 ms.

## Tóm tắt nhanh về đường nguồn

`VBUS` là đường nguồn 5 V trực tiếp từ cổng USB khi đang cắm cáp. `VSYS` là ngõ vào nguồn hệ thống của bo mạch, chấp nhận dải điện áp khoảng 1,8 V đến 5,5 V (nguồn USB đi tới `VSYS` qua một diode). `3V3` là đường nguồn đã ổn áp (ngõ ra). Mọi chân GP đều hoạt động ở mức logic 3,3 V. Đưa tín hiệu 5 V vào chân GP có thể làm hỏng chip, và tuyệt đối không nối pin 2S (7,4 V) vào chân `3V3` hay `VSYS`. Bạn sẽ đo kiểm các đường nguồn này ở bài sơ đồ chân; hôm nay chỉ cấp nguồn qua USB.

## Ví dụ đã làm

Chi sử dụng Pico bản gốc cùng một sợi cáp điện thoại cũ chưa từng dùng để chép dữ liệu. Lần cắm đầu tiên, dù giữ nút BOOTSEL đúng cách, máy tính vẫn không hiện ổ `RPI-RP2`. Sau khi đổi sang cáp dữ liệu Ugreen, ổ đĩa lập tức xuất hiện. Chi suýt chép nhầm tệp UF2 của Pico 2 có sẵn trong thư mục tải về, nhưng kịp kiểm tra lại nhãn in trên mạch ghi "Pico" nên đã tải đúng tệp từ trang RPI_PICO. Sau khi chép, ổ tự biến mất. Mở Thonny, ban đầu trình thông dịch vẫn trỏ vào Python trên laptop nên lệnh `import machine` báo lỗi. Chuyển sang **MicroPython (Raspberry Pi Pico)** thì dấu nhắc REPL hiện ra, gõ `1 + 1` trả về `2`. `Pin("LED")` hoạt động trên bản firmware này, đèn xanh nháy hai lần mỗi giây và bộ đếm tăng đều trong cửa sổ Shell. Chi ghi vào sổ: "Pico gốc, UF2 RP2040, bí danh LED chạy được, GPIO 25 cùng chân đèn, không Wi-Fi, không nối động cơ."

Ở bàn bên cạnh là một bo mạch Pico 2 W (ổ bootloader hiện `RP2350`). Nạp tệp RP2040 sẽ sai họ chip; sau khi nạp đúng UF2 cho Pico 2 W, `Pin("LED")` bật được đèn và GPIO 25 được ghi chú là chân trống, không phải chân LED.

## Lab

1. Rút hẳn cáp khỏi bo mạch, nhấn giữ nút BOOTSEL, cắm cáp dữ liệu rồi thả nút. Xác nhận ổ bootloader xuất hiện (`RPI-RP2` trên Pico/Pico W hoặc `RP2350` trên Pico 2/Pico 2 W).
2. Tải đúng tệp UF2 khớp với bo mạch: [RPI_PICO](https://micropython.org/download/RPI_PICO/) cho Pico gốc, [RPI_PICO2](https://micropython.org/download/RPI_PICO2/) cho Pico 2, hoặc bản có W tương ứng từ [trang tải chính thức](https://micropython.org/download/). Chép tệp vào ổ bootloader và đợi ổ tự biến mất.
3. Mở Thonny chọn **MicroPython (Raspberry Pi Pico)** (hoặc chạy `mpremote`), gõ `1 + 1` và xác nhận kết quả `2`.
4. Chạy đoạn mã nháy LED ở trên. Kiểm tra đèn nháy hai lần mỗi giây và bộ đếm tăng liên tục 1, 2, 3 mà không bị khởi động lại.
5. Ghi vào `lab-notes.md` đúng tên in trên mạch (Pico, Pico W, Pico 2 hoặc Pico 2 W), nguồn tải tệp UF2 đã dùng và tham số đã bật sáng đèn (`"LED"` hay `25`).

Bài đạt khi cửa sổ REPL kết nối đúng vào Pico (không phải Python của laptop) và bạn quan sát trực tiếp nhịp nháy 2 Hz.

Các lỗi thường gặp: thả nút BOOTSEL trước khi cắm cáp nên mạch chạy thẳng vào firmware cũ; dùng cáp chỉ sạc nên không hiện cả ổ đĩa lẫn cổng serial; chọn sai họ UF2 (nạp ảnh RP2040 lên Pico 2 hoặc nạp nhầm bản W/không W); hoặc quên chuyển trình thông dịch trong Thonny nên báo không tìm thấy mô-đun `machine`.

An toàn: mọi chân GP chỉ chịu tối đa 3,3 V. Không nối pin, động cơ hay cảm biến 5 V trong bài này; `3V3` là ngõ ra ổn áp và `VSYS` không chịu được điện áp pin 2S.

## Video tham khảo

- **Xem trước:** [Raspberry Pi PICO | Starting With MicroPython + Examples | I2C OLED, ADC, PWM](https://www.youtube.com/watch?v=zlKJ5hvfs6s) — Electronoobs, tiếng Anh. Hướng dẫn dùng MicroPython trên Pico qua REPL kèm ví dụ PWM và ADC (phần I2C để dành cho chương 04).
- [Raspberry Pi Pico - A Beginners Guide](https://www.youtube.com/watch?v=L03jT5slWnw) — Tinkernut, tiếng Anh. Minh họa thao tác nạp firmware và lần cắm USB đầu tiên trước khi lập trình.

## Bài tập

1. Nêu bốn thao tác để vào chế độ BOOTSEL và tên ổ đĩa bootloader xuất hiện trên Pico (RP2040) cũng như Pico 2 (RP2350). Vì sao chỉ dựa vào tên ổ đĩa vẫn chưa đủ để chọn đúng tệp UF2 cho mọi phiên bản?
2. Đoạn mã dùng `Pin(25)` trên Pico W nhưng đèn tích hợp không sáng. Hãy viết lại dòng khởi tạo đúng và cho biết GPIO 25 trên Pico W thực chất là chân gì.
3. Bạn lỡ chép tệp `RPI_PICO-....uf2` lên Pico 2, ổ đĩa biến mất nhưng không thấy cổng REPL. Cần thay bằng tệp nào và tệp cũ thuộc dòng chip nào?
4. Thonny báo không tìm thấy mô-đun `machine`. Nguyên nhân cấu hình nằm ở đâu?
5. Vì sao bài này cấm đưa tín hiệu 5 V vào chân GP, kể cả chỉ là một đường dây Echo từ cảm biến?

<details>
<summary>Đáp án</summary>

1. Bốn bước: rút hẳn cáp, nhấn giữ BOOTSEL, cắm cáp USB khi vẫn đang giữ nút, sau đó thả BOOTSEL. Ổ đĩa hiện tên `RPI-RP2` trên Pico/Pico W (RP2040) và `RP2350` trên Pico 2/Pico 2 W (RP2350). Dù phân biệt được hai thế hệ chip, tên ổ vẫn giống nhau giữa bản không W và bản có W trong cùng thế hệ, nên vẫn phải đối chiếu tên tệp UF2 với đúng nhãn trên mạch.
2. Đổi thành `led = Pin("LED", Pin.OUT)`. Trên Pico W và Pico 2 W, LED tích hợp nối với chip không dây, còn GPIO 25 là một chân GPIO thông thường.
3. Đưa bo mạch vào lại chế độ BOOTSEL và chép đúng tệp UF2 tải từ trang `RPI_PICO2` (hoặc `RPI_PICO2_W` nếu là bản W). Tệp `RPI_PICO-...` là firmware dành cho chip RP2040 của Pico bản gốc, không chạy được trên RP2350 của Pico 2.
4. Trình thông dịch của Thonny đang trỏ vào Python cục bộ trên laptop hoặc chọn sai cổng kết nối. Cần chuyển sang **MicroPython (Raspberry Pi Pico)** hoặc dùng `mpremote` trỏ đúng cổng của Pico.
5. Chân GP của Pico dùng mức logic 3,3 V; tín hiệu 5 V vượt ngưỡng chịu đựng và có thể làm hỏng chân chip. Nguồn động cơ và pin 2S cũng phải đi qua mạch cầu H ở bài sau, không nối trực tiếp vào bo mạch.

</details>

## Mua ở Việt Nam

Chỉ cần mua một bo mạch họ Pico và một cáp micro-USB truyền dữ liệu nếu bạn chưa có. Giá dưới đây được ghi nhận công khai trên Hshop ngày 23 tháng 9 năm 2026: trang tìm kiếm [raspberry pi pico](https://hshop.vn/search?q=raspberry+pi+pico) hiển thị Pico 2 giá 195 000 ₫ và Pico 2 W giá 275 000 ₫. Trang sản phẩm chi tiết: [Pico 2, RP2350](https://hshop.vn/mach-raspberry-pi-pico-2-rp2350) và [Pico 2 W](https://hshop.vn/mach-raspberry-pi-pico-2-w-rp2350) (Pico 2 không tích hợp Wi-Fi, còn Pico 2 W có sẵn). Cáp dữ liệu tương thích: [Ugreen Micro-USB 1 m, 54 000 ₫](https://hshop.vn/cap-micro-usb-to-usb-2-0-dai-1m-cao-cap-60136-chinh-hang-ugreen).

Nếu tham khảo thêm trên Shopee: [Raspberry Pi Pico 2](https://shopee.vn/search?keyword=raspberry%20pi%20pico%202). Nếu vẫn đang cân nhắc phương án ESP32 mặc định, bo mạch hoàn chỉnh gồm [NodeMCU-32S giá 190 000 ₫](https://hshop.vn/kit-rf-thu-phat-wifi-ble-esp32-nodemcu-32s-ch340-ai-thinker) và [Vietduino ESP32 giá 265 000 ₫](https://hshop.vn/mach-phat-trien-vietduino-esp32), tránh mua module trần [ESP32-S3-WROOM-1 giá 135 000 ₫](https://hshop.vn/mach-thu-phat-wifi-ble-soc-esp32-s3-esp32-s3-wroom-1-chinh-hang-espressif). Có thể tham khảo thêm [DevKitC-32U của Thế Giới IC](https://www.thegioiic.com/esp32-devkitc-32u-module-wifi-bluetooth-2-4ghz); [IC Đây Rồi](https://icdayroi.com/) là cửa hàng linh kiện rời. Danh sách linh kiện đầy đủ nằm ở [chương 00]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %}).

## Đọc thêm

- [MicroPython trên Raspberry Pi Pico](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html) — hướng dẫn cài đặt chính thức từ Raspberry Pi.
- [Datasheet Pico](https://datasheets.raspberrypi.com/pico/pico-datasheet.pdf) — thông tin về GPIO 25, các đường nguồn VBUS, VSYS, 3V3 và điện áp cực đại cho phép.
- [Trang tải MicroPython](https://micropython.org/download/) — danh mục phân tách rõ tệp UF2 cho RP2040 và RP2350; nên tải trực tiếp từ trang chính thức theo đúng bo mạch thay vì lấy tệp chia sẻ lại trên diễn đàn.
