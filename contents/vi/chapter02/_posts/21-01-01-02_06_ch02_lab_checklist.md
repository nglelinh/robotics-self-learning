---
layout: post
title: "Checklist lab chương 02"
chapter: "02"
order: 6
owner: "Nguyen Le Linh"
lang: vi
categories: [chapter02]
lesson_type: required
draft: false
---

## Mục tiêu

Bài kiểm tra này dùng để chốt lại toàn bộ chương 02 dựa trên các bằng chứng thực tế có thể kiểm chứng trực tiếp. Bạn cần ghi rõ bộ công cụ (toolchain) cùng số phiên bản, xác nhận LED tích hợp nháy đúng chu kỳ đã chọn, dán đoạn log nhịp tim serial thay vì chỉ mô tả bằng lời, hoàn thiện thẻ sơ đồ chân cho đúng bo mạch trên bàn (gồm chân LED và chân ngõ ra an toàn), ghi chính xác hai giá trị đo đường nguồn (3,3 V và 5 V/VBUS), và ghi rõ câu xác nhận chưa dùng các chân nguồn động cơ (VM và pin). Nếu có mục nào chưa đạt, hãy quay lại bài học tương ứng để xử lý thay vì vội mua thêm bo mạch mới.

## Cần gì trước khi học

Bài này tổng hợp kết quả từ bài 1 đến bài 5: câu quyết định chọn vi điều khiển (ESP32 hoặc đúng phiên bản Pico), bộ công cụ tương ứng, log nhịp tim (hoặc ghi rõ đang chờ nếu chưa có mạch) và thẻ sơ đồ chân. Bạn cần có đồng hồ vạn năng cho mục đo nguồn. Danh sách linh kiện đầy đủ nằm ở chương 00 ([Hóa đơn linh kiện và cách mua]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %})). Cần đọc lại quy tắc nhấc bánh khỏi bàn từ bài nhịp tim để bảo đảm không đánh dấu đạt khi robot đang có nguy cơ tự lăn.

---

Trước khi viết các thuật toán điều khiển phức tạp như PWM động cơ, ngắt encoder hay máy trạng thái ở Chương 03, bạn cần chắc chắn 100% rằng nền móng vi điều khiển ở Chương 02 đã vững như bàn thạch: nạp code ổn định, không rớt cổng Serial, nhịp tim không chặn chạy đều tăm tắp và đường nguồn không bao giờ sụt áp. **Checklist Chương 02** là bài kiểm tra nghiệm thu nhanh giúp bạn bước sang Chương 03 không mang theo bất kỳ "quả bom nổ chậm" nào.

## Kiến thức cần nhớ: Nghiệm thu Tầng Vi điều khiển (MCU Bring-Up Verification)

1. **Tính ổn định Nạp & Giao tiếp:** Cắm rút USB 3 lần liên tiếp đều nhận đúng cổng, nạp firmware thành công ở lần đầu và log Serial hiển thị rõ ràng không rác ký tự.
2. **Định thời Chính xác & Không chặn:** Bộ đếm thời gian (`millis()` / `ticks_ms()`) giữ chu kỳ nhịp tim ổn định, không dùng `delay()` chặn CPU.
3. **An toàn Đường nguồn & Mức logic:** Có bảng Pinmap rõ ràng, tách biệt nguồn động lực với nguồn logic 3,3 V và xác minh không xảy ra `Brownout Reset`.

### Ví dụ làm từng bước: Bốn con số nghiệm thu đầu ra Chương 02

Hãy đối chiếu 4 chỉ số thực đo từ bo mạch của bạn với ngưỡng chuẩn sau:

| Hạng mục kiểm tra | Cách đo / Bằng chứng | Ngưỡng đạt chuẩn | Ví dụ thực đo ĐẠT |
|---|---|---|---|
| **1. Chu kỳ log nhịp tim (500 ms)** | Hiệu 2 dòng `t_ms` liên tiếp trên Serial | $$[495\text{ ms},\ 505\text{ ms}]$$ | `t_ms = 1000, 1500, 2001` ($$\Delta = 500\text{–}501\text{ ms}$$) |
| **2. Tỉ lệ lỗi khung Serial** | Quan sát 60 dòng log ở `115200 bps` | **0%** ký tự rác | 60/60 dòng sạch CSV |
| **3. Điện áp đường `3V3` chạy tải logic** | Đo DC V tại chân `3V3–GND` | $$[3.20\text{ V},\ 3.40\text{ V}]$$ | $$3.31\text{ V}$$ |
| **4. Số lần tự reset trong 5 phút** | Theo dõi dòng `BOOT` trên Serial | **0 lần** | 0 lần reset bất thường |

### Giải thích: 4 bước xử lý khi một mục trong Checklist Chương 02 chưa đạt

1. **Bước 1 — Cô lập phần cứng về cấu hình tối thiểu:** Tháo toàn bộ cảm biến/dây nối ngoài, chỉ giữ lại bo MCU trần cắm USB để xác định lỗi thuộc về bo mạch hay thuộc về ngoại vi.
2. **Bước 2 — Kiểm tra lại tốc độ baud và cáp USB:** 70% lỗi Serial rác hoặc không nạp được đến từ lệch baud rate hoặc cáp USB kém tiếp xúc.
3. **Bước 3 — Dùng đồng hồ đo lại nguồn trước khi nghi chip hỏng:** Vi điều khiển hiếm khi tự chết nếu chưa bị quá áp; thường do nguồn tụt áp hoặc chân `EN` bị chạm lỏng.
4. **Bước 4 — Lưu bản chụp log Serial và ảnh Pinmap vào sổ lab:** Đây là mốc tham chiếu cực quý giá nếu sau này lắp thêm động cơ mà bo đột ngột mất ổn định.

**Kiểm tra nhanh.** Nếu nhật ký Serial in `t_ms` nhảy từ `5000` thẳng về `120` giữa chừng mà bạn không hề bấm nút Reset, hiện tượng gì vừa xảy ra? Bo mạch vừa bị **tự khởi động lại (Watchdog reset hoặc Brownout reset)** — cần kiểm tra lại nguồn cấp hoặc vòng lặp bị treo!

---

## Vì sao bài này gắn với Capstone A

Chương 07 sử dụng vi điều khiển này để chạy chương trình điều khiển từ xa (teleop) cho xe vi sai với hai kênh PWM nối tới TB6612, nguồn pin cấp vào VM, cơ chế tự ngắt sau khoảng 300 ms mất lệnh và quy tắc nhấc bánh khi thử nghiệm. Chương 07 giả định mọi mục trong danh sách kiểm tra này đã hoàn tất. Nếu bước sang chương sau mà vẫn chưa xác định chắc chắn chân mass hay độ ổn định nguồn, bạn sẽ mất thời gian sửa mã nguồn timeout trong khi lỗi thật sự là chip đang bị reset. Đến chương 08, kết nối Wi-Fi trên ESP32 càng dễ lộ lỗi nếu nguồn sụt áp (brownout), biểu hiện như tín hiệu mạng chập chờn. Danh sách kiểm tra này giúp loại bỏ các lỗi phần cứng cơ bản trước khi đi sâu vào phần mềm.

## Sáu mục kiểm tra và bằng chứng tương ứng

Mỗi mục trong danh sách đòi hỏi bằng chứng cụ thể ghi trong `lab-notes.md`, không phải việc bạn nhớ mình đã đọc qua lý thuyết. Chương 02 gồm sáu mục; mỗi mục chỉ có hai trạng thái: **ĐẠT** (kèm bằng chứng rõ ràng) hoặc **MỞ** (chưa hoàn thành). Không có trạng thái trung gian như "gần đạt".

1. **Bộ công cụ (Toolchain):** ghi rõ số phiên bản cụ thể. Với Arduino IDE: phiên bản trong hộp thoại About kèm phiên bản gói `esp32` trong Boards Manager. Với PlatformIO: kết quả lệnh `pio --version` cùng xác nhận dòng `board = esp32dev` trong `platformio.ini`. Với Pico: phiên bản Thonny hoặc `mpremote` kèm tên tệp UF2 (nêu rõ `RPI_PICO`, `RPI_PICO2` hay bản W). Ghi chung chung "đã cài rồi" là không đạt.
2. **Nháy LED tích hợp:** xác nhận trực quan LED tích hợp nháy đúng chu kỳ đã chọn (bài nhịp tim là 500 ms, đảo mỗi 250 ms, tức 2 Hz; nếu chọn chu kỳ khác thì ghi rõ con số đó). Đèn báo nguồn không được tính, và `LED_BUILTIN` chỉ hợp lệ sau khi đã đối chiếu với nhãn trên mạch. Sổ tay cần ghi rõ số chân GPIO hoặc bí danh Pico (`"LED"` hay `25`).
3. **Log nhịp tim serial:** dán trực tiếp 10 dòng log từ lần chạy thật, có duy nhất một dòng tiêu đề `heartbeat`, mốc mili giây tăng đều xấp xỉ chu kỳ khai báo, không bị chèn dòng khởi động lại ở giữa. Mỗi dòng thể hiện thời gian và trạng thái. Ghi "đếm ổn" sẽ không đạt vì sau này cần đúng dãy số đó để đối chiếu khi kiểm tra sụt áp. Với ESP32, tốc độ baud phải ghi 115200; để monitor ở 9600 là chưa đạt dù đèn vẫn nháy.
4. **Thẻ sơ đồ chân:** bản vẽ hoặc bảng Markdown lập cho chính bo mạch đang có (không chép từ ảnh của biến thể khác), ghi rõ chân LED, các chân `GND` và ít nhất một chân ngõ ra an toàn (không phải chân strapping đang cần kéo mức đặc biệt, không phải chân UART của chip USB-serial và không phải chân nguồn). Trên Pico W, không được ghi GPIO 25 là LED tích hợp.
5. **Đo nguồn bằng đồng hồ (chỉ cắm USB, không nối pin):** ghi chính xác hai con số thực đo — khoảng 4,7 V đến 5,1 V trên đường 5 V hoặc `VBUS`, và khoảng 3,25 V đến 3,35 V trên đường `3V3` (ví dụ 4,82 V sau diode là đạt nếu ghi rõ số liệu; viết "5 V ổn" là không đạt). Nếu chân `3V3` đo được 4,9 V, phải rút cáp ngay để kiểm tra vì mạch đang bị lỗi nguồn.
6. **Xác nhận chân động cơ chưa sử dụng:** ghi rõ câu xác nhận: "Chân VM trên TB6612 và pin 2S vẫn để hở. Pin không được chạm vào GPIO, 3V3, 5V/VIN, VSYS hay VBUS", kèm quy tắc nhấc bánh khỏi bàn. Ghi chung chung "động cơ để sau" mà không gọi tên cụ thể VM và pin là chưa đạt.

![Checklist dừng trước nguồn motor]({{ site.imgurl }}/generated/power_order.png)

Sơ đồ nhắc lại giới hạn của chương 02: nguồn USB, nháy LED và nhịp tim serial xác nhận phần logic hoạt động ổn định; toàn bộ phần driver và pin nằm ở phía bên phải vạch ngăn cách và chưa được nối ở chương này.

Trình tự khởi chạy ở bài 1 gồm: nhận USB, nháy LED tích hợp, serial 115200 baud, đọc nút nhấn, xuất PWM không tải, sau đó mới tới driver và pin. Sáu mục trên dừng lại trước bước đấu driver; ngay cả khi hoàn thành danh sách này, vẫn không được nối trực tiếp động cơ vào chân GPIO.

Nếu linh kiện vẫn đang trên đường giao, bạn có thể chuẩn bị trước phiên bản bộ công cụ và lập trước thẻ sơ đồ chân dựa trên đúng mẫu sản phẩm đã đặt, còn các mục nháy LED, log serial và đo điện áp ghi rõ trạng thái `đang chờ`. Không được điền số liệu giả định. Đây là bước chuẩn bị trước khi có phần cứng, chưa tính là đã hoàn thành chương.

## Cách xử lý khi có mục chưa đạt

Khi một mục chưa đạt, hãy mở lại đúng bài học tương ứng để khắc phục:

- **Thiếu phiên bản bộ công cụ:** mở hộp thoại About, chạy `pio --version` hoặc kiểm tra thông tin phiên bản MicroPython trong REPL rồi ghi lại (xem lại bài cài đặt ESP32 hoặc Pico).
- **Đèn không nháy hoặc sai chân:** xem lại bài nạp ESP32 hoặc bài nạp UF2 cho Pico, sau đó xem bài nhịp tim. Đối chiếu nhãn in trên mạch vì GPIO 2 không áp dụng cho mọi bản mạch, còn Pico W phải dùng `Pin("LED")`.
- **Mất serial, ký tự rác hoặc lặp dòng tiêu đề:** xem bài nhịp tim. Đặt đúng 115200 baud; nếu tiêu đề lặp lại khi không có động cơ, đổi cáp USB và tháo các dây nối ngoài trước khi sửa mã nguồn. Nếu còn nối dây VM, rút ngay để tránh sụt áp.
- **Thiếu thẻ sơ đồ chân hoặc sai biến thể:** xem bài sơ đồ chân, vẽ lại đủ đường 5 V/VBUS, 3V3, GND, chân LED và một chân ngõ ra an toàn.
- **Thiếu số đo điện áp hoặc chỉ ghi "ổn":** thực hiện phép đo khi chỉ cắm USB theo bài sơ đồ chân. Nếu `3V3` lệch xa 3,3 V, dừng lại kiểm tra và tuyệt đối không gắn pin.
- **Thiếu câu xác nhận về động cơ:** bổ sung ngay theo ví dụ mẫu ở bài sơ đồ chân, nhấn mạnh pin 2S chỉ nối vào VM, không chạm hàng chân vi điều khiển.

Lưu ý: việc mua thêm một bo mạch ESP32 thứ hai khi có mục chưa đạt thường chỉ lặp lại đúng lỗi cáp ban đầu; hãy ưu tiên thay cáp chỉ sạc trước.

## Ví dụ đã làm

Dưới đây là hai ví dụ ghi chép trung thực:

Bo mạch của Hà đã giao từ tuần trước. Sổ ghi: Arduino IDE 2.3.2 kèm gói `esp32` 3.0.7; NodeMCU-32S dùng CH340 ở `COM5`; LED tích hợp tại GPIO 2 (đã đối chiếu nhãn mạch), đảo trạng thái mỗi 250 ms; 10 dòng nhịp tim bước nhảy từ 498 ms đến 505 ms dưới một dòng tiêu đề duy nhất ở 115200 baud; thẻ sơ đồ chân gồm 5V, 3V3, GND, LED GPIO 2 và ngõ ra an toàn GPIO 4; đo bằng đồng hồ khi chỉ cắm USB được 4,91 V và 3,31 V; kèm câu xác nhận "VM và pin 2S để hở, dương pin không chạm 5V, 3V3 hay bất kỳ GPIO nào." Cả sáu mục đều đạt, động cơ TT vẫn để trong hộp và quy tắc nhấc bánh đã được ghi nhận.

Pico 2 của Khoa vẫn đang vận chuyển. Sổ ghi: đã cài Thonny 4.1.4, ghi sẵn tên tệp UF2 từ trang `RPI_PICO2` để tránh nạp nhầm bản RP2040, lập trước thẻ sơ đồ chân theo ảnh sản phẩm gồm VBUS, VSYS, 3V3, GND, LED GP25 và ngõ ra an toàn GP16, kèm ghi chú "không đưa 5 V vào chân GP; VM và pin không có trong kiện này." Các mục nháy LED, serial và đo điện áp ghi rõ `đang chờ`, và Khoa chưa đánh dấu hoàn thành chương.

Một mẫu sổ thứ ba (chưa đạt) được dùng làm đề phân tích trong phần bài tập bên dưới.

## Lab

Mở `lab-notes.md`, tạo một mục mới ghi ngày thực hiện và tiêu đề "kiểm tra hoàn thành chương 02". Với từng mục trong sáu mục, ghi **ĐẠT** kèm bằng chứng cụ thể, hoặc **MỞ** kèm tên bài cần làm lại. Nếu chưa nhận được bo mạch, ghi rõ `đang chờ` cho các mục nháy LED, serial và đo nguồn. Kiểm tra lại toàn bộ một lượt: bất kỳ mục nào thiếu bằng chứng xác thực (số phiên bản, dòng log serial, số đo điện áp, số chân cụ thể, xác nhận về VM và pin) đều phải chuyển về trạng thái **MỞ** trước khi lưu.

Chương 02 chỉ hoàn thành khi cả sáu mục đều **ĐẠT**, có ghi quy tắc nhấc bánh và chưa nối động cơ. Bản chuẩn bị trước khi có phần cứng phải ghi rõ ba mục đo kiểm ở trạng thái `đang chờ`.

## Video tham khảo

- **Xem trước:** [Lập trình ESP32 - Bài 1 - Cách nạp chương trình cho ESP32 bằng Arduino IDE - Tự học lập trình IOT](https://www.youtube.com/watch?v=sJtJJU3c3xE) — Điện thông minh E-smart, tiếng Việt. Minh họa quy trình nạp để bảo đảm LED nháy từ chính chương trình bạn viết chứ không phải từ đèn báo nguồn có sẵn.

## Bài tập

Xét mẫu ghi chép chưa đạt dưới đây:

```text
Ngày: 23 Sep 2026
Board: ESP32 NodeMCU
Toolchain: đã cài Arduino IDE
LED: GPIO 2, hình như có nhấp
Baud monitor: 9600
Serial: thấy vài ký tự, không chép
Ray: 5V ổn, 3.3 ổn
Tiếp: PWM motor từ GPIO 2, sắp gắn pin
```

1. Liệt kê tất cả các mục chưa đạt trong mẫu sổ trên và chỉ ra bằng chứng còn thiếu của từng mục.
2. Chương trình nhịp tim đặt `Serial.begin(115200)`, còn monitor đang để 9600. Màn hình sẽ hiển thị gì, và cần thay đổi thông số nào để khắc phục?
3. Ghi chú "GPIO 2, hình như có nhấp" chưa đạt yêu cầu kiểm chứng. Cần xác nhận điều gì trên bo mạch để công nhận GPIO 2, và phải ghi thế nào nếu đèn thực tế nằm ở chân khác?
4. Viết lại hai dòng về đường nguồn và động cơ cho đúng định dạng yêu cầu mà không tự bịa số liệu chưa đo (dùng trạng thái đang chờ nếu chưa đo bằng đồng hồ).
5. Với mẫu sổ trên, cần mở lại những bài học nào trước tiên, và vì sao mua thêm một bo mạch mới là cách xử lý sai?

<details>
<summary>Đáp án</summary>

1. Toàn bộ sáu mục đều chưa đạt: **Toolchain** thiếu số phiên bản IDE và gói `esp32`; **Nháy LED** ghi "hình như", thiếu chu kỳ và chưa đối chiếu nhãn mạch; **Serial** thiếu 10 dòng log dán kèm và sai tốc độ baud (9600); **Đo nguồn** chỉ ghi "ổn" thay vì hai số đo thực tế; **Chân động cơ** dự định xuất PWM động cơ thẳng từ GPIO 2 và gắn pin, trái ngược yêu cầu để hở VM và pin; **Thẻ sơ đồ chân** bị bỏ sót hoàn toàn nên mục ngõ ra an toàn cũng chưa đạt.
2. Màn hình sẽ hiện toàn ký tự lỗi (rác) trong khi đèn LED vẫn có thể nháy bình thường. Chỉ cần chỉnh tốc độ Serial Monitor lên 115200 baud cho khớp chương trình, không hạ tốc độ trong mã nguồn xuống 9600.
3. Nhãn in trên mạch hoặc sơ đồ hãng phải xác nhận LED tích hợp nối với GPIO 2 (phổ biến trên DevKit V1 nhưng không phải mọi mạch). Nếu đèn nằm ở chân khác, ghi đúng số chân GPIO đó, xác nhận đèn nháy theo chu kỳ đã chọn và không liệt kê GPIO 2 là chân LED; `LED_BUILTIN` cũng cần kiểm chứng tương tự.
4. Dòng đo nguồn đúng định dạng: "chỉ USB, chân 5V ____ V, chân 3V3 ____ V, pin chưa nối (đang chờ đo đồng hồ)". Dòng động cơ đúng định dạng: "VM và pin 2S để hở; pin không chạm GPIO, 3V3 hay 5V/VIN; không điều khiển động cơ trực tiếp từ GPIO 2."
5. Mở lại bài nhịp tim trước để sửa tốc độ baud và thu thập log, sau đó mở bài sơ đồ chân để đo đường nguồn và lập thẻ chân kèm ghi chú về VM. Mua bo mạch thứ hai không giải quyết được lỗi cấu hình và thiếu ghi chép; nếu không thấy cổng kết nối thì cần kiểm tra và thay cáp dữ liệu trước.

</details>

## Mua ở Việt Nam

Chỉ mua bổ sung những món còn thiếu cho mục chưa đạt. Thiếu cáp dữ liệu: [Ugreen Micro-USB 1 m, 54 000 ₫](https://hshop.vn/cap-micro-usb-to-usb-2-0-dai-1m-cao-cap-60136-chinh-hang-ugreen). Thiếu bo mạch chính: [ESP32 NodeMCU-32S CH340, 190 000 ₫](https://hshop.vn/kit-rf-thu-phat-wifi-ble-esp32-nodemcu-32s-ch340-ai-thinker) hoặc [Vietduino ESP32, 265 000 ₫](https://hshop.vn/mach-phat-trien-vietduino-esp32) — không mua module trần [ESP32-S3-WROOM-1 giá 135 000 ₫](https://hshop.vn/mach-thu-phat-wifi-ble-soc-esp32-s3-esp32-s3-wroom-1-chinh-hang-espressif) vì không dùng làm bo mạch khởi đầu. Hướng Pico (giá ghi nhận ngày 23 tháng 9 năm 2026 từ [trang tìm Pico](https://hshop.vn/search?q=raspberry+pi+pico)): Pico 2 giá 195 000 ₫ ([trang sản phẩm](https://hshop.vn/mach-raspberry-pi-pico-2-rp2350)) và Pico 2 W giá 275 000 ₫ ([trang sản phẩm](https://hshop.vn/mach-raspberry-pi-pico-2-w-rp2350)). Tham khảo thêm trên Shopee: [ESP32 DevKit CH340](https://shopee.vn/search?keyword=esp32%20devkit%20ch340), [Pico 2](https://shopee.vn/search?keyword=raspberry%20pi%20pico%202). [DevKitC-32U ở Thế Giới IC](https://www.thegioiic.com/esp32-devkitc-32u-module-wifi-bluetooth-2-4ghz) là mẫu bo mạch phát triển (kiểm tra kỹ cổng USB); [IC Đây Rồi](https://icdayroi.com/) là cửa hàng linh kiện rời. Chưa cần mua động cơ hay TB6612 để hoàn thành chương 02; các món này nằm trong [giỏ hàng chương 00]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %}).

## Đọc thêm

- [PlatformIO `esp32dev`](https://docs.platformio.org/en/latest/boards/espressif32/esp32dev.html) — mã bo mạch mặc định cho mục toolchain ESP32.
- [Cài arduino-esp32](https://docs.espressif.com/projects/arduino-esp32/en/latest/installing.html) — nguồn cung cấp phiên bản gói phần mềm cần ghi vào sổ tay.
- [Trang tải MicroPython](https://micropython.org/download/) — nơi tra cứu chính xác tên tệp UF2 riêng cho RP2040 và RP2350.
- [Datasheet ESP32](https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf) — tài liệu đối chiếu bảng đặc tính điện để chọn chân ngõ ra an toàn thay vì chỉ tin sơ đồ trên blog.
