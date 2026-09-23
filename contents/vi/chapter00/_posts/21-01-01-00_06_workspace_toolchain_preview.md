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

Dành khoảng 70 phút trên đúng máy bạn sẽ dùng cho firmware. Bạn cần câu lộ trình từ bài 00-02. Chưa cần robot, Ubuntu, hay một lần biên dịch thành công. Mục tiêu là cây thư mục và một nhật ký cài nói thật thứ gì đã được cài hôm nay.

## Mục tiêu học

Bạn sẽ **tạo** không gian làm việc với `notes/`, hoặc `firmware/esp32/` hoặc `firmware/pico/`, và một `ros_ws/` trống có câu giải thích vì sao trống. Bạn sẽ **chọn** đường ESP32 (Arduino IDE 2.x hoặc PlatformIO, lớp board `esp32dev`, serial 115200, cáp USB dữ liệu) hoặc đường Pico 2 (BOOTSEL, file UF2 MicroPython, Thonny hoặc `mpremote`). Bạn sẽ **ghi** phiên bản bạn thực sự thấy, kể cả dòng thành thật "chưa cài". Bạn sẽ **giải thích** vì sao ROS 2 Jazzy là bản cài Ubuntu 24.04 và vì sao Windows Subsystem cho Linux chưa phải lab robot. Bạn sẽ **gọi tên** Gazebo Harmonic mà không cài, và **ước lượng** một byte serial nhỏ thế nào so với timeout teleop 300 ms.

## Cần có trước

Bạn tạo được thư mục và dán chữ vào `notes/lab-notes.md`. Bài 00-01 tới 00-04 đã cho bạn các trường sổ, lộ trình, thẻ lên nguồn, và ảnh kiểm kê dụng cụ. Bài 00-05, hóa đơn vật tư, nên đã có dạng `bom.csv` hoặc một ghi chú có ngày; nếu chưa, viết `thiếu bom.csv` trong nhật ký cài thay vì bịa giá. Chưa cần đã hàn.

## Vì sao việc này dính tới Capstone

Timeout của Chương 07 sống trong firmware bạn build lại được, trên board mà cổng serial bạn đã thấy xuất hiện. Topic ROS 2, sau này, là lớp nhắn tin trên hành vi đó. Nếu `ros_ws/` là đống gói cài dở trên laptop Windows, bạn sẽ sửa lỗi apt trong khi chân PWM còn chưa được thử. Một thư mục trống kèm lý do viết ra là bạn lab tốt hơn một tutorial bạn không làm xong. Gazebo Harmonic có thể chờ tới khi có robot mà hành vi im lặng bạn đã tin đủ để mô phỏng.

## Thư mục, và mỗi thư mục được chứa gì

Đặt thư mục khóa ở chỗ bạn sẽ tìm lại. Các tên dưới đây là hợp đồng.

`notes/` giữ `lab-notes.md` và, khi bài 00-05 xong, một bản hoặc một đường chỉ tới `bom.csv`. Ảnh có thể nằm cạnh markdown hoặc trong `notes/img/`. Thư mục này không phải chỗ để thư viện bạn tải "phòng khi".

`firmware/esp32/` hoặc `firmware/pico/` giữ chương trình cho vi điều khiển bạn đã chọn. Tạo cái khớp câu lộ trình. Nếu vẫn đang phân vân, tạo cái bạn đã viết ở bài 00-02 và thêm dòng `chưa chốt — xem lại trước khi trả tiền`. Đừng tạo cả hai rồi gọi đó là kế hoạch, trừ khi bạn đã có cả hai board và đã nói board nào lái motor.

`ros_ws/` là workspace ROS 2. Hôm nay nó chứa một `README` và không gì khác. README nêu hệ điều hành của máy này và câu "Jazzy chưa cài ở đây" hoặc "Jazzy đã cài trên máy Ubuntu 24.04 này, chuỗi phiên bản ở dưới". Nó không chứa một bản clone Nav2, driver LiDAR, hay world Gazebo giải nén dở.

Cây ngắn cho sinh viên ESP32 trên Windows trông như sau.

```text
robot-course/
  notes/lab-notes.md
  notes/bom.csv
  firmware/esp32/README.md
  ros_ws/README.md
```

Sinh viên Pico dùng `firmware/pico/`. Tên nhàm có chủ đích. Các bài sau sẽ bảo bạn mở file nào.

![Toolchain đang nói chuyện với cái gì: USB, ổn áp, chân 3,3 V, mass]({{ site.imgurl }}/generated/pcb_mcu_anatomy.png)

Hình giải phẫu là board như một tập việc. USB mang nguồn và đường serial. Ổn áp tạo 3,3 V. Chân GPIO nói logic. Mass là nút chung từ bài an toàn. Việc duy nhất của toolchain hôm nay là nói với đường USB đó, hoặc thú nhận board chưa có ở đây.

![Module ESP32 trên board nhỏ, não có Wi-Fi]({{ site.imgurl }}/wikimedia/ESP32_on_Lolin32_Lite_clone_board_cropped.jpg)

![Raspberry Pi Pico, board MicroPython bắt đầu bằng USB]({{ site.imgurl }}/wikimedia/Raspberry_Pi_Pico.jpg)

Hai bức ảnh là hai não hợp lệ, không phải lựa chọn thứ ba bạn phải mua. Board loại ESP32 là board làm teleop Wi-Fi sau được. Board loại Pico, kể cả Pico 2 nếu bài 00-05 bán cho bạn cái đó, là board bắt đầu như thiết bị USB chạy MicroPython. Khớp ảnh với câu của bạn. Đừng khớp với listing đang giảm giá tối nay.

## Đường ESP32, xem trước và chưa làm xong

Hai công cụ là hợp lệ. **Arduino IDE 2.x** là cái có giao diện, trình quản lý board, và serial monitor. **PlatformIO** là cái sống trong trình soạn như VS Code và ghim phiên bản trong một file. Chọn một cái cho nhật ký. Bạn được đổi sau. Bạn không được viết "cái nào cũng được" rồi để nhật ký trống.

Khi gói hỗ trợ board đã cài, mục board bạn muốn cho DevKit thông dụng thuộc lớp **`esp32dev`**: trong Arduino IDE thường ghi "ESP32 Dev Module"; trong PlatformIO id board là `esp32dev`. Nhãn menu đổi giữa các phiên bản gói. Id mới là thứ cần ghi. Baud serial monitor cho các sketch đầu của khóa là **115200**. Cáp chỉ sạc sẽ thắp đèn trên board và không bao giờ hiện cổng. Bằng chứng cáp dữ liệu là một thiết bị serial mới khi bạn cắm, và sự biến mất của nó khi bạn rút.

Bạn không bắt buộc biên dịch blink hôm nay. Nếu IDE đã cài, ghi chuỗi phiên bản từ hộp About hoặc từ `pio --version`. Nếu chưa cài, viết `chưa cài Arduino IDE` hoặc `chưa cài PlatformIO` và lý do. "Tôi đang trên máy lab tôi không được quyền cài" là một lý do. "Tôi chán" cũng là một lý do, và nó nên hiện để tuần sau thành thật.

Một byte trên đường serial 8N1 khoảng 10 lần bit. Ở 115200 bit/s,

$$
t_{\mathrm{byte}} \approx \frac{10}{115200}\,\mathrm{s} \approx 87\,\mu\mathrm{s}.
$$

Một lệnh ngắn bốn ký tự là dưới nửa mili giây. Timeout Chương 07 khoảng 300 ms, lớn hơn hàng trăm lần. Baud serial không phải công tắc người chết. Lệnh bị mất mới là. Biết điều đó bây giờ ngăn bạn "sửa" timeout bằng cách đổi baud sau này.

## Đường Pico, xem trước và chưa làm xong

Giữ nút **BOOTSEL**, cắm board vào cáp USB dữ liệu, rồi thả nút. Một ổ hiện ra, kiểu USB. Bạn chép một file **UF2 MicroPython** vào ổ đó. Board khởi động lại vào trình thông dịch MicroPython. **Thonny** là trình soạn đơn giản tìm được board. **`mpremote`** là công cụ dòng lệnh làm cùng việc từ terminal. Chọn một và ghi vào nhật ký.

Nếu không có ổ, nghi cáp trước, rồi nút, rồi cổng. Nếu board chưa tới, viết các bước thành kế hoạch và đừng tải UF2 ngẫu nhiên "cho sẵn" mà không ghi ngày và nguồn Raspberry Pi chính thức. UF2 từ một thread diễn đàn là cách người ta nạp nhầm chip.

Đường Pico không dùng `esp32dev` và không bắt buộc 115200 cho REPL của MicroPython, dù một UART bạn tự nối sau này có thể dùng baud đó. Đừng trộn hai nhật ký. Sinh viên chọn Pico vẫn để `ros_ws/` trống vì cùng lý do với sinh viên ESP32.

## ROS 2 Jazzy và Gazebo Harmonic, chỉ gọi tên

**ROS 2 Jazzy** là bản phân phối khóa này dùng, và bản cài desktop được hỗ trợ là **Ubuntu 24.04**. Nếu máy này là Windows, đừng giả vờ Windows Subsystem cho Linux là lab robot. WSL có thể là chỗ đọc tài liệu. Nó không phải chỗ bạn cắm mass của driver và nhìn một bánh. Viết việc cài là **sau**, trên máy Ubuntu 24.04: máy của bạn, nếu có, hoặc máy lab, như trong bài lộ trình. Trang cài là [docs.ros.org/en/jazzy/Installation.html](https://docs.ros.org/en/jazzy/Installation.html). Làm theo hôm nay chỉ được khi hệ điều hành thực sự là Ubuntu 24.04, và chỉ như một buổi song song, không thay thư mục firmware.

**Gazebo Harmonic** là bộ mô phỏng đi với stack đó. Tên của nó vào README. Gói của nó không được cài hôm nay. Một file world bạn không nối được với robot bạn chưa lắp là một dự án thứ hai.

micro-ROS, khi tới, là firmware trên cùng board ESP32 hoặc loại Pico cộng một agent trên máy Ubuntu. Nó thuộc về sau khi `firmware/` đã chứa chương trình đưa PWM về 0. `ros_ws/` trống là cách bạn nhớ thứ tự đó.

## Lab: thư mục, README, nhật ký cài

Tạo cây ở mục trước. Trong `firmware/esp32/README.md` hoặc `firmware/pico/README.md`, viết ba dòng: lộ trình (A, hoặc B-sau-A), MCU đã chọn bằng lời, và công cụ bạn sẽ dùng (Arduino IDE 2.x, PlatformIO, Thonny, hoặc mpremote). Nếu công cụ chưa cài, nói vậy trong cùng file.

Tạo `ros_ws/README.md` với tên hệ điều hành và câu rằng Jazzy cùng Gazebo Harmonic chưa cài hôm nay, hoặc chuỗi phiên bản nếu bạn đang trên Ubuntu 24.04 và đã cài Jazzy. Đừng dán transcript `apt` của một tutorial bạn không chạy.

Thêm mục **nhật ký cài** vào mục sổ hôm nay. Mỗi dòng là một công cụ, một phiên bản hoặc `chưa cài`, và một ngày. Các dòng ví dụ, bạn phải sửa cho khớp máy mình:

```text
2026-09-23  OS: Windows 11
2026-09-23  Arduino IDE: chưa cài — sẽ dùng giờ lab thứ Năm
2026-09-23  PlatformIO: chưa cài
2026-09-23  kế hoạch serial: 115200, board id esp32dev, cáp chưa chứng minh
2026-09-23  ROS 2 Jazzy: chưa cài — máy lab Ubuntu 24.04 sau
2026-09-23  Gazebo Harmonic: chỉ gọi tên
```

Nhật ký Pico ghi BOOTSEL và UF2 thay cho `esp32dev`. Dán nhật ký vào trường serial nếu bạn chưa có board, để trường không trống. Nếu cổng đã hiện, dán tên cổng phía trên nhật ký.

**Bạn sẽ thấy gì.** Ba thư mục tồn tại. README firmware nêu lộ trình và MCU. README của ROS không nhận Ubuntu bạn không có. Nhật ký có ngày và chữ `chưa cài` ở chỗ đó là sự thật.

**Khi lệch.** Bạn tạo `ros_ws/src` đầy clone vì một video bắt đầu như vậy. Xóa các clone cho tới khi README là file duy nhất; bạn clone lại khi Chương 09 bảo. Bạn viết "WSL Ubuntu" như thể đó là lab robot. Sửa README: WSL không phải bàn lab. Bạn đặt baud 9600 vì một sketch Arduino cũ. Serial monitor của khóa cho sketch ESP32 là 115200. Bạn chép UF2 từ link ngẫu nhiên. Thay kế hoạch bằng tài liệu MicroPython chính thức của Raspberry Pi và đừng nạp cho tới khi nói được file đó dành cho chip nào.

## Ví dụ làm sẵn

Trang dùng Windows, lộ trình A, ESP32, trần tiền đã chốt ở bài 00-02. Cô tạo `firmware/esp32/` và `ros_ws/`. Cô không cài IDE trong buổi này vì máy lab ở trường đã có Arduino IDE 2.3 và cô muốn học một lần cài. Nhật ký ghi `Arduino IDE: không có trên laptop này; máy lab trường, xác nhận phiên bản thứ Năm`. README firmware nói "Lộ trình A, ESP32, teleop Wi-Fi sau, công cụ Arduino IDE 2.x, lớp board esp32dev, serial 115200". Cô tính thời gian một byte, khoảng 87 µs, và viết "timeout 300 ms khoảng 3000 lần thời gian byte; baud không phải lớp an toàn". `ros_ws/README.md` của cô nói "Laptop này là Windows 11. Jazzy chờ máy lab Ubuntu 24.04. Gazebo Harmonic chưa cài. WSL sẽ không được dùng làm lab robot".

Một bạn trên Ubuntu 24.04 có thể cài Jazzy ở giờ khác và dán chuỗi phiên bản thật. Bạn đó vẫn nợ cùng thư mục firmware. Trang không chép một phiên bản cô không chạy.

## Bài tập

1. Câu lộ trình của bạn nói Pico 2 và MicroPython. Bạn tạo thư mục nào, BOOTSEL phải làm gì trước khi có file được chép, và hai công cụ nào hợp lệ cho REPL?
2. LED board sáng nhờ cáp USB, và không có cổng serial. Bạn nghi vật nào, và bằng chứng nào sẽ đổi ý bạn?
3. Bạn đang trên Windows và một blog bảo cài Jazzy trong WSL tối nay. Bạn viết gì trong `ros_ws/README.md`, và hệ điều hành nào thực sự được yêu cầu?
4. Ở 115200 bit/s, 8N1, ước lượng thời gian một byte và một lệnh 4 byte. Thời gian đó có phải một phần đáng kể của 300 ms không?
5. Nhật ký cài nói "PlatformIO latest" không phiên bản không ngày. Bạn thêm gì để dòng đó thành bằng chứng?

<details>
<summary>Gợi ý đáp án</summary>

1. Tạo `firmware/pico/`. Giữ BOOTSEL khi cắm cáp dữ liệu để ổ hiện ra, rồi chép UF2 MicroPython. Thonny hoặc `mpremote` nói chuyện với board sau đó.
2. Nghi cáp chỉ sạc. Cáp dữ liệu được chứng minh khi cổng serial hoặc ổ BOOTSEL hiện và mất theo phích cắm. LED sáng chỉ chứng minh có điện.
3. Viết rằng Jazzy chưa cài, WSL không phải lab robot, và việc cài chờ Ubuntu 24.04. Đường desktop Jazzy của khóa này là Ubuntu 24.04.
4. Một byte khoảng $10/115200 \approx 87\,\mu\mathrm{s}$. Bốn byte khoảng $0{,}35\,\mathrm{ms}$. Đó khoảng một phần nghìn của 300 ms. Timeout là về lệnh bị mất, không phải về baud.
5. Thêm ngày, đầu ra của `pio --version` hoặc chuỗi About của IDE, và `chưa cài` nếu bạn chưa chạy. "Latest" không phải phiên bản.

</details>

## Đọc thêm

- [Tài liệu PlatformIO](https://docs.platformio.org/) — đường ESP32 trong trình soạn, kể cả id board `esp32dev`.
- [Tài liệu Arduino](https://docs.arduino.cc/) — Arduino IDE 2.x và serial monitor.
- [ESP-IDF cho ESP32](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/) — framework của Espressif. Bạn không bắt buộc dùng nó cho Capstone A. Đó là chỗ tra khi gói hỗ trợ board không khớp blog.
- [MicroPython cho Pico](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html) — BOOTSEL và UF2 chính thức, kế hoạch nạp duy nhất bài này tin.
- [Tutorial ROS 2 Jazzy](https://docs.ros.org/en/jazzy/Tutorials.html) — lướt danh sách để thấy nó giả định đã cài. Bản cài đó là Ubuntu 24.04, sau này.
- [Gazebo Harmonic](https://gazebosim.org/docs/harmonic/) — tên và tài liệu của bộ mô phỏng. Đừng cài từ bài này.
