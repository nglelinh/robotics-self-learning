---
layout: post
title: "Không gian làm việc và toolchain"
chapter: "00"
order: 6
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter00
lesson_type: required
draft: false
---

Hãy dành khoảng 70 phút thực hiện bài học này trên chính chiếc máy tính bạn sẽ dùng để lập trình firmware. Bạn cần mở lại phát biểu lộ trình từ bài 00-02. Lúc này chưa cần có robot, chưa cần Ubuntu và cũng chưa cần biên dịch thành công một chương trình nào; mục tiêu duy nhất là dựng cây thư mục chuẩn và ghi một bản nhật ký cài đặt trung thực với tình trạng hiện tại của máy.

## Mục tiêu học

Sau bài học này, bạn sẽ **khởi tạo** không gian làm việc gồm `notes/`, một trong hai thư mục `firmware/esp32/` hoặc `firmware/pico/`, và một thư mục `ros_ws/` trống kèm lời giải thích lý do. Bạn sẽ **chọn** công cụ lập trình phù hợp cho hướng ESP32 (Arduino IDE 2.x hoặc PlatformIO, nhóm board `esp32dev`, tốc độ serial 115200, cáp USB truyền dữ liệu) hoặc hướng Pico 2 (chế độ BOOTSEL, tệp UF2 MicroPython, Thonny hoặc `mpremote`). Bạn sẽ **ghi nhận** chính xác phiên bản phần mềm đang có (hoặc ghi thẳng `chưa cài`), **giải thích** vì sao ROS 2 Jazzy yêu cầu Ubuntu 24.04 và Windows Subsystem for Linux (WSL) chưa thay thế được bàn lab robot. Cuối cùng, bạn sẽ **nhận diện** vai trò của Gazebo Harmonic mà chưa cần cài đặt, đồng thời **ước lượng** thời gian truyền một byte serial nhỏ đến mức nào so với ngưỡng timeout teleop 300 ms.

## Cần có trước

Bạn chỉ cần biết tạo thư mục và cập nhật nội dung vào `notes/lab-notes.md`. Các bài từ 00-01 đến 00-04 đã chuẩn bị sẵn cấu trúc sổ lab, lộ trình, thẻ cấp nguồn và ảnh kiểm kê dụng cụ. Tệp `bom.csv` (hoặc ghi chú ngân sách có ngày) từ bài 00-05 nên đã hoàn thiện; nếu chưa xong, hãy ghi `thiếu bom.csv` vào nhật ký thay vì tự điền giá ước đoán. Hiện tại vẫn chưa cần kỹ năng hàn.

---

Trong tuần đầu làm dự án robot, bạn chỉ có một file `blink.ino` duy nhất nên lưu ở đâu cũng thấy gọn. Nhưng đến tuần thứ tám — khi đã có firmware đọc encoder, mã PID, file cấu hình chân, sơ đồ nối dây và nhật ký thử nghiệm — một thư mục lộn xộn kiểu `code_final_v3_fix2` sẽ khiến bạn nạp nhầm bản cũ làm xe chạy giật lùi mà không hiểu vì sao! Thiết lập **không gian làm việc (workspace) và chuỗi công cụ (toolchain)** bài bản ngay từ Chương 00 giúp mã nguồn của bạn tái lập được sau nhiều tháng.

## Bản đồ kiến thức nền: Chuỗi công cụ (Toolchain) Biên dịch Nhúng hoạt động ra sao?

1. **Biên dịch chéo (Cross-Compilation):** Máy tính của bạn dùng CPU x86_64/ARM64, còn robot dùng vi điều khiển kiến trúc Xtensa/RISC-V (ESP32) hoặc ARM Cortex-M0+ (RP2040). Toolchain (PlatformIO / `arm-none-eabi-gcc` / `xtensa-esp32-elf-gcc`) biên dịch mã C++ trên PC thành tệp nhị phân `.bin` chạy được trên chip nhỏ.
2. **Giao tiếp Nạp & Gỡ lỗi (USB-to-UART & Bootloader):** Khi bấm `Upload`, PC kéo chân `BOOT`/`EN` đưa chip vào chế độ Bootloader, bơm từng gói nhị phân qua cổng nối tiếp UART ở tốc độ baud cao rồi khởi động lại MCU.
3. **Quản lý Phiên bản & Cây thư mục Chuẩn hóa:** Tách bạch rõ `firmware/`, `docs/` (sơ đồ chân, sổ lab), `cad/` và `ros2_ws/` giúp bạn đối chiếu ngay mã nguồn nào đã tạo ra kết quả đo nào.

### Ví dụ cầm tay chỉ việc: Tính thời gian nạp Firmware qua cổng USB-UART

Giả sử dự án ESP32 của bạn biên dịch ra tệp nhị phân `firmware.bin` có dung lượng **$$650\text{ KB}$$** ($$650 \times 1{,}024 = 665{,}600\text{ byte}$$). Giao thức UART chuẩn `8N1` cần **10 bit** cho mỗi byte (1 bit start + 8 bit dữ liệu + 1 bit stop):
- Nếu nạp ở tốc độ mặc định chậm **115.200 bps** ($$11{,}520\text{ byte/s}$$):
  $$
  t_{\text{nạp}} = \frac{665{,}600}{11{,}520} \approx \mathbf{57.8\text{ giây}} \quad (\text{rất lâu mỗi lần sửa 1 dòng code!}).
  $$
- Tăng `upload_speed = 460800` bps trong `platformio.ini` ($$46{,}080\text{ byte/s}$$):
  $$
  t_{\text{nạp}} = \frac{665{,}600}{46{,}080} \approx \mathbf{14.4\text{ giây}} \quad (\text{nhanh gấp }\mathbf{4\times}\text{!}).
  $$

### Khung giải thích: 4 bước dựng Workspace bền vững cho cả khóa học (nên đọc chậm)

1. **Bước 1 — Dùng một thư mục gốc cố định không dấu, không khoảng trắng:** Ví dụ `robotics_lab/` thay vì `Đồ án Robot (mới)/` — nhiều công cụ CMake/PlatformIO và ROS 2 bị lỗi đường dẫn khi gặp khoảng trắng hoặc ký tự tiếng Việt có dấu.
2. **Bước 2 — Khóa phiên bản thư viện trong `platformio.ini`:** Ghi rõ phiên bản thư viện cảm biến để 3 tháng sau mở lại dự án vẫn biên dịch ra đúng tệp nhị phân ban đầu.
3. **Bước 3 — Tách nhánh ESP32 (PlatformIO) và Pico (MicroPython) rõ ràng:** Mỗi bo mạch có trình nạp và giao diện serial riêng; ghi chép đúng tên cổng (`COM3` / `/dev/ttyUSB0`) vào `README.md`.
4. **Bước 4 — Giữ ROS 2 Jazzy & Gazebo ở chế độ "nhận diện trước":** Chương 00 chỉ cần biết vai trò của chúng trên bản đồ tổng thể; chưa cần cài đặt nặng máy ngay từ tuần đầu.

**Kiểm tra nhanh.** Vì sao giao thức UART `8N1` cần **10 bit** đường truyền để gửi **8 bit** (1 byte) dữ liệu thực? Vì mỗi khung byte luôn kèm thêm 1 bit bắt đầu (`Start bit = 0`) và 1 bit kết thúc (`Stop bit = 1`) để bên nhận đồng bộ nhịp đồng hồ mà không cần dây xung nhịp riêng!

---

## Vì sao bài này gắn liền với Capstone

Cơ chế timeout 300 ms của Chương 07 nằm trong firmware mà bạn có thể biên dịch lại bất cứ lúc nào trên một mạch đã nhận đúng cổng serial. Các topic ROS 2 về sau chỉ là lớp truyền thông đặt lên trên nền tảng đó. Nếu thư mục `ros_ws/` trên laptop Windows chứa đầy các gói cài đặt dang dở, bạn sẽ mất thời gian sửa lỗi phần mềm trong khi chân PWM chưa từng được kiểm tra. Một thư mục `ros_ws/` trống kèm lý do rõ ràng luôn hữu ích hơn một hướng dẫn cài đặt bỏ dở. Gazebo Harmonic hoàn toàn có thể chờ đến khi robot thực tế đã có hành vi dừng tin cậy để mô phỏng.

## Cấu trúc thư mục và quy ước lưu trữ

Hãy đặt thư mục gốc của khóa học ở nơi dễ tìm trên máy tính và tuân thủ đúng tên các thư mục con sau:

- `notes/`: lưu tệp `lab-notes.md` và tệp `bom.csv` (khi hoàn thành bài 00-05). Ảnh chụp thực hành có thể để cùng thư mục hoặc đặt trong `notes/img/`. Không dùng thư mục này để lưu các thư viện tải sẵn "phòng khi dùng".
- `firmware/esp32/` hoặc `firmware/pico/`: chứa mã nguồn cho vi điều khiển bạn đã chọn theo câu lộ trình. Nếu vẫn đang cân nhắc, hãy tạo thư mục khớp với lựa chọn ở bài 00-02 kèm ghi chú `chưa chốt — xem lại trước khi trả tiền`. Tránh tạo cả hai thư mục nếu bạn không thực sự dùng song song hai loại mạch.
- `ros_ws/`: không gian làm việc cho ROS 2. Ở thời điểm hiện tại, thư mục này chỉ chứa duy nhất một tệp `README.md` nêu rõ hệ điều hành máy tính cùng trạng thái "Jazzy chưa cài ở đây" (hoặc "Jazzy đã cài trên Ubuntu 24.04 này" kèm chuỗi phiên bản cụ thể). Không sao chép sẵn kho mã nguồn Nav2, driver LiDAR hay tệp bản đồ Gazebo vào đây.

Cây thư mục mẫu cho người học dùng ESP32 trên Windows có dạng như sau:

```text
robot-course/
  notes/lab-notes.md
  notes/bom.csv
  firmware/esp32/README.md
  ros_ws/README.md
```

Nếu dùng Raspberry Pi Pico, bạn thay `firmware/esp32/` bằng `firmware/pico/`. Cách đặt tên đơn giản và cố định giúp bạn dễ theo dõi chỉ dẫn ở các chương sau.

![Toolchain đang nói chuyện với cái gì: USB, ổn áp, chân 3,3 V, mass]({{ site.imgurl }}/generated/pcb_mcu_anatomy.png)

Hãy hình dung cấu tạo mạch theo chức năng từng khối: cổng USB truyền dữ liệu serial và cấp nguồn vào, mạch ổn áp tạo ra đường 3,3 V, các chân GPIO đảm nhiệm tín hiệu logic, và mass là điểm tham chiếu chung từ bài an toàn. Ở bước hôm nay, nhiệm vụ duy nhất của bộ công cụ (toolchain) là giao tiếp được với đường USB đó — hoặc ghi nhận rõ rằng bạn chưa có mạch trên bàn.

![Module ESP32 trên board nhỏ, não có Wi-Fi]({{ site.imgurl }}/wikimedia/ESP32_on_Lolin32_Lite_clone_board_cropped.jpg)

![Raspberry Pi Pico, board MicroPython bắt đầu bằng USB]({{ site.imgurl }}/wikimedia/Raspberry_Pi_Pico.jpg)

Hai bức ảnh trên đại diện cho hai lựa chọn vi điều khiển chính của khóa học. Mạch ESP32 thuận tiện nếu bạn định triển khai teleop qua Wi-Fi về sau, còn mạch dòng Pico (bao gồm Pico 2) phù hợp để bắt đầu ngay với MicroPython qua kết nối USB. Hãy chọn đúng theo mục tiêu đã viết trong lộ trình thay vì chạy theo sản phẩm đang giảm giá.

## Nhánh ESP32: tổng quan công cụ

Có hai môi trường phát triển phù hợp cho ESP32. **Arduino IDE 2.x** trực quan với giao diện đồ họa, trình quản lý board tích hợp và cửa sổ Serial Monitor sẵn có. **PlatformIO** hoạt động trong trình soạn thảo như VS Code và cho phép cố định phiên bản thư viện trong tệp cấu hình. Bạn có thể chọn một trong hai để ghi vào nhật ký (và hoàn toàn có thể đổi sau này), nhưng không nên viết chung chung "cái nào cũng được" rồi bỏ trống nhật ký.

Sau khi cài gói hỗ trợ ESP32, cấu hình phổ biến cho các mạch DevKit thông dụng thuộc nhóm **`esp32dev`** (trong Arduino IDE thường hiển thị là "ESP32 Dev Module", còn trong PlatformIO mã board là `esp32dev`). Tên hiển thị trên menu có thể thay đổi theo từng phiên bản gói, nhưng mã nhận diện thì ổn định nên cần ghi lại. Tốc độ baud mặc định của Serial Monitor cho các chương trình đầu tiên trong khóa là **115200**. Lưu ý rằng cáp USB chỉ sạc vẫn có thể làm sáng đèn nguồn trên mạch nhưng không bao giờ tạo ra cổng serial; bằng chứng duy nhất của cáp dữ liệu là một cổng serial mới xuất hiện khi cắm và biến mất khi rút.

Hôm nay bạn chưa bắt buộc phải biên dịch chương trình nhấp nháy LED. Nếu IDE đã được cài đặt, hãy ghi chính xác phiên bản lấy từ mục About hoặc từ lệnh `pio --version`. Nếu chưa cài, hãy ghi `chưa cài Arduino IDE` hoặc `chưa cài PlatformIO` kèm lý do thực tế (ví dụ: đang dùng máy phòng lab chưa có quyền cài).

Trên đường truyền serial cấu hình 8N1, mỗi byte cần khoảng 10 chu kỳ bit. Ở tốc độ 115200 bit/s, thời gian truyền một byte là:

$$
t_{\mathrm{byte}} \approx \frac{10}{115200}\,\mathrm{s} \approx 87\,\mu\mathrm{s}.
$$

Một lệnh điều khiển ngắn gồm 4 ký tự chỉ mất chưa tới nửa mili giây — nhỏ hơn hàng trăm lần so với ngưỡng timeout 300 ms của Chương 07. Nói cách khác, tốc độ baud không phải là cơ chế tự dừng khi mất tín hiệu (dead-man switch); nguyên nhân kích hoạt timeout là việc mất gói lệnh. Nắm rõ tỷ lệ này ngay từ đầu giúp bạn tránh việc "sửa" lỗi timeout bằng cách đổi tốc độ baud về sau.

## Nhánh Pico: tổng quan công cụ

Với dòng Raspberry Pi Pico, bạn giữ nút **BOOTSEL**, cắm cáp USB truyền dữ liệu vào máy tính rồi thả nút ra để máy nhận diện mạch như một ổ đĩa USB. Sau đó, bạn sao chép tệp **UF2 MicroPython** vào ổ đĩa này; mạch sẽ tự khởi động lại vào môi trường MicroPython. Để lập trình và tương tác, bạn có thể chọn **Thonny** (trình soạn thảo đơn giản, tự nhận mạch) hoặc **`mpremote`** (công cụ dòng lệnh trên terminal). Hãy chọn một công cụ và ghi vào nhật ký.

Nếu ổ đĩa không xuất hiện, hãy kiểm tra lần lượt cáp USB, thao tác giữ nút BOOTSEL và cổng USB trên máy tính. Khi chưa có mạch, bạn chỉ cần ghi lại các bước này thành kế hoạch; không tải sẵn tệp UF2 từ các diễn đàn không rõ nguồn gốc vì rất dễ nạp nhầm phiên bản cho sai dòng chip. Hãy luôn lấy tệp từ trang tài liệu MicroPython chính thức của Raspberry Pi.

Nhánh Pico không sử dụng mã `esp32dev` và không bắt buộc đặt tốc độ 115200 cho giao diện REPL của MicroPython (dù các kết nối UART tự đấu về sau vẫn có thể dùng tốc độ này). Không trộn lẫn ghi chú của hai nhánh, và người học Pico vẫn để trống `ros_ws/` với cùng lý do như nhánh ESP32.

## ROS 2 Jazzy và Gazebo Harmonic: chỉ ghi nhận tên

**ROS 2 Jazzy** là bản phân phối chính thức của khóa học, với hệ điều hành desktop được hỗ trợ là **Ubuntu 24.04**. Nếu bạn đang dùng Windows, đừng coi Windows Subsystem for Linux (WSL) là môi trường thực hành robot; WSL có thể hỗ trợ đọc tài liệu, nhưng không phù hợp để kết nối phần cứng và quan sát chuyển động thực tế. Hãy ghi kế hoạch cài đặt là **để sau** trên máy chạy Ubuntu 24.04 (máy cá nhân hoặc máy phòng lab). Đường dẫn cài đặt chính thức là [docs.ros.org/en/jazzy/Installation.html](https://docs.ros.org/en/jazzy/Installation.html); bạn chỉ nên cài đặt song song hôm nay nếu máy tính thực sự đang chạy Ubuntu 24.04 và vẫn ưu tiên thư mục firmware.

**Gazebo Harmonic** là bộ mô phỏng đồng bộ với ROS 2 Jazzy. Ở bài này bạn chỉ cần ghi tên công cụ vào `README.md` chứ chưa cài đặt gói phần mềm; xây dựng một không gian mô phỏng khi chưa lắp khung xe thực tế rất dễ biến thành một dự án lạc hướng.

Tương tự, **micro-ROS** (gồm firmware trên ESP32/Pico và agent trên máy Ubuntu) chỉ nên triển khai sau khi thư mục `firmware/` đã có chương trình biết đưa PWM về 0 an toàn. Giữ `ros_ws/` trống là cách nhắc nhở trực quan nhất về trình tự này.

## Thực hành: tạo cây thư mục, README và nhật ký cài đặt

Khởi tạo cây thư mục như hướng dẫn ở trên. Trong `firmware/esp32/README.md` hoặc `firmware/pico/README.md`, viết ngắn gọn ba thông tin: lộ trình đã chọn (A, hoặc B sau khi xong A), loại vi điều khiển, và công cụ lập trình dự kiến (Arduino IDE 2.x, PlatformIO, Thonny hoặc `mpremote`), kèm trạng thái đã cài hay chưa.

Tạo tệp `ros_ws/README.md` ghi rõ hệ điều hành hiện tại của máy tính và khẳng định ROS 2 Jazzy cùng Gazebo Harmonic chưa được cài hôm nay (hoặc ghi rõ chuỗi phiên bản nếu bạn đang dùng Ubuntu 24.04 và đã cài Jazzy). Không sao chép log cài đặt `apt` từ các hướng dẫn mà bạn chưa thực sự chạy.

Thêm mục **Nhật ký cài đặt** vào sổ lab hôm nay. Mỗi dòng gồm tên công cụ, phiên bản thực tế (hoặc `chưa cài`) và ngày ghi nhận. Dưới đây là mẫu tham khảo để bạn điều chỉnh cho đúng với máy của mình:

```text
2026-09-23  OS: Windows 11
2026-09-23  Arduino IDE: chưa cài — sẽ dùng giờ lab thứ Năm
2026-09-23  PlatformIO: chưa cài
2026-09-23  kế hoạch serial: 115200, board id esp32dev, cáp chưa chứng minh
2026-09-23  ROS 2 Jazzy: chưa cài — máy lab Ubuntu 24.04 sau
2026-09-23  Gazebo Harmonic: chỉ gọi tên
```

Nếu theo nhánh Pico, hãy ghi rõ kế hoạch BOOTSEL và UF2 thay cho `esp32dev`. Bạn có thể dán trực tiếp nhật ký này vào trường đoạn serial trong sổ lab khi chưa có mạch để tránh để trống trường; nếu mạch đã nhận cổng serial, hãy dán tên cổng lên phía trên nhật ký.

**Kết quả cần đạt:** Đủ ba thư mục theo đúng quy ước; tệp README trong `firmware/` nêu rõ lộ trình và vi điều khiển; tệp README trong `ros_ws/` phản ánh trung thực hệ điều hành; nhật ký có ngày cụ thể và ghi thẳng `chưa cài` ở các mục chưa thực hiện.

**Cách xử lý khi lệch chuẩn:** Nếu bạn đã tạo `ros_ws/src` và tải sẵn nhiều kho mã nguồn theo video hướng dẫn, hãy xóa bớt để giữ lại duy nhất tệp README cho tới Chương 09. Nếu bạn đang ghi "WSL Ubuntu" như môi trường thực hành chính, hãy sửa lại vì WSL không thay thế được máy Ubuntu thực tế. Nếu đặt tốc độ baud 9600 theo thói quen Arduino cũ, hãy chuyển về 115200 cho các bài ESP32 của khóa. Nếu đã tải tệp UF2 từ nguồn không rõ ràng, hãy xóa và chuyển sang dùng đường dẫn tài liệu MicroPython chính thức của Raspberry Pi.

## Ví dụ làm sẵn

Trang dùng máy Windows, chọn Lộ trình A với ESP32 và đã chốt ngân sách ở bài 00-02. Cô tạo hai thư mục `firmware/esp32/` và `ros_ws/`. Cô chưa cài IDE trên laptop cá nhân vì máy phòng lab ở trường đã cài sẵn Arduino IDE 2.3 và cô muốn dùng chung một môi trường trước; nhật ký ghi rõ `Arduino IDE: chưa cài trên laptop cá nhân; sẽ kiểm tra phiên bản trên máy lab trường vào thứ Năm`. Tệp README trong thư mục firmware ghi: "Lộ trình A, ESP32, mở rộng teleop Wi-Fi sau, công cụ Arduino IDE 2.x, nhóm board esp32dev, serial 115200". Cô tính thời gian truyền một byte khoảng 87 µs và ghi nhận: "ngưỡng timeout 300 ms lớn gấp hơn 3000 lần thời gian truyền một byte, nên tốc độ baud không phải lớp bảo vệ an toàn". Tệp `ros_ws/README.md` nêu rõ: "Máy chạy Windows 11. ROS 2 Jazzy chờ máy lab Ubuntu 24.04. Chưa cài Gazebo Harmonic. Không dùng WSL làm môi trường lab robot".

Một bạn khác dùng Ubuntu 24.04 có thể cài Jazzy ở buổi riêng và ghi chuỗi phiên bản thực tế vào sổ, nhưng vẫn phải chuẩn bị đầy đủ thư mục `firmware/` tương tự. Trang không bao giờ sao chép số phiên bản từ máy khác vào nhật ký của mình.

## Video tham khảo

- **Xem trước:** [Get started with PlatformIO and the ESP 32](https://www.youtube.com/watch?v=3ATDCi4ApY4) — John Green Dev, tiếng Anh. Giới thiệu nhanh quy trình mở dự án và nạp chương trình ESP32 bằng PlatformIO — bộ công cụ sẽ cài đặt ở Chương 02.
- [Breadboard tutorial: How to use a breadboard (for beginners)](https://www.youtube.com/watch?v=W6mixXsn-Vc) — LeftyMaker, tiếng Anh. Giải thích cấu tạo hàng lỗ thông nhau trên breadboard phục vụ các bài thực hành đầu tiên.

## Bài tập

1. Nếu lộ trình của bạn chọn Pico 2 và MicroPython, bạn cần tạo thư mục firmware nào, thao tác với nút BOOTSEL thực hiện ra sao trước khi chép tệp, và hai công cụ nào hợp lệ để tương tác với REPL?
2. Khi cắm cáp USB, đèn LED trên mạch phát sáng nhưng máy tính không hiện cổng serial nào. Bạn cần nghi ngờ bộ phận nào trước tiên, và dấu hiệu nào chứng minh cáp đó truyền được dữ liệu?
3. Bạn đang dùng Windows và thấy một bài viết hướng dẫn cài ROS 2 Jazzy trên WSL ngay tối nay. Bạn nên viết gì vào `ros_ws/README.md`, và hệ điều hành nào thực sự được khuyến nghị?
4. Ở tốc độ 115200 bit/s (cấu hình 8N1), hãy ước lượng thời gian truyền 1 byte và một lệnh gồm 4 byte. Khoảng thời gian này có chiếm tỷ lệ đáng kể so với ngưỡng 300 ms không?
5. Một dòng nhật ký ghi "PlatformIO latest" mà không có số phiên bản hay ngày tháng. Bạn cần bổ sung thông tin gì để dòng này trở thành bằng chứng hợp lệ?

<details>
<summary>Gợi ý đáp án</summary>

1. Tạo thư mục `firmware/pico/`. Giữ nút BOOTSEL trong lúc cắm cáp USB truyền dữ liệu để máy tính nhận diện ổ đĩa rồi chép tệp UF2 MicroPython vào đó. Sau khi mạch khởi động lại, dùng Thonny hoặc `mpremote` để giao tiếp với REPL.
2. Nghi ngờ cáp USB chỉ có chức năng sạc. Cáp truyền dữ liệu chỉ được chứng minh khi cổng serial (hoặc ổ đĩa BOOTSEL) xuất hiện lúc cắm và biến mất lúc rút; đèn nguồn sáng chỉ chứng tỏ có điện áp 5 V.
3. Ghi rõ trong `ros_ws/README.md` rằng ROS 2 Jazzy chưa được cài đặt, WSL không thay thế được môi trường thực hành robot, và việc cài đặt sẽ thực hiện sau trên Ubuntu 24.04 (hệ điều hành desktop được khóa học hỗ trợ).
4. Một byte mất khoảng $10/115200 \approx 87\,\mu\mathrm{s}$, nên 4 byte mất khoảng $0{,}35\,\mathrm{ms}$ — chỉ xấp xỉ một phần nghìn của ngưỡng 300 ms. Điều này cho thấy timeout liên quan đến việc mất lệnh chứ không phải tốc độ baud.
5. Bổ sung ngày kiểm tra và chuỗi phiên bản cụ thể lấy từ lệnh `pio --version` hoặc hộp thoại About của IDE (hoặc ghi thẳng `chưa cài` nếu chưa cài đặt). Chữ "latest" không mang giá trị truy vết.

</details>

## Đọc thêm

- [Tài liệu PlatformIO](https://docs.platformio.org/) — hướng dẫn lập trình ESP32 trên trình soạn thảo, bao gồm cấu hình mã board `esp32dev`.
- [Tài liệu Arduino](https://docs.arduino.cc/) — tài liệu chính thức về Arduino IDE 2.x và công cụ Serial Monitor.
- [ESP-IDF cho ESP32](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/) — bộ framework gốc của Espressif; chưa bắt buộc cho Capstone A nhưng hữu ích để tra cứu khi gặp sai khác ở gói hỗ trợ board.
- [MicroPython cho Pico](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html) — hướng dẫn chính thức về BOOTSEL và tệp UF2 cho dòng Raspberry Pi Pico.
- [Tutorial ROS 2 Jazzy](https://docs.ros.org/en/jazzy/Tutorials.html) — có thể xem lướt để hình dung cấu trúc bài học sau khi cài trên Ubuntu 24.04.
- [Gazebo Harmonic](https://gazebosim.org/docs/harmonic/) — tài liệu giới thiệu bộ mô phỏng; chưa cần cài đặt từ bài này.
