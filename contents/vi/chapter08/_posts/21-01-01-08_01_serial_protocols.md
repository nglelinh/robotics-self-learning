---
layout: post
title: "Giao thức serial ngoài println"
chapter: "08"
order: 1
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter08
lesson_type: required
draft: false
---

Thời lượng ước tính: **~90 phút**.

## Mục tiêu

Sau bài này, bạn thiết kế được một định dạng khung lệnh bánh xe bền vững ngay cả khi cổng USB giao dữ liệu bị cắt mảnh, cài đặt được phía gửi bằng Python và phía nhận trên ESP32/Pico, đồng thời giải thích được vì sao dùng `println` gửi chuỗi `"40,-15"` chưa phải là một giao thức tin cậy. Bạn cũng tính được byte kiểm tra XOR, xác định ngưỡng timeout để đưa động cơ về 0, và ghi lại cả một khung hợp lệ lẫn một khung cố ý làm hỏng vào `lab-notes.md`. Đây chính là giao ước truyền thông mà node cầu nối ROS 2 ở Chương 10 sẽ sử dụng để `cmd_vel` không bao giờ biến thành các byte rời rạc trong bộ đệm.

## Kiến thức cần trước

Bạn đã biết điều khiển LED và in dữ liệu qua cổng nối tiếp (Chương 02), cũng như hoàn thiện phiên bản teleop Capstone A ở Chương 07. Bạn hiểu 1 byte gồm 8 bit và cấu hình `115200 8N1` nghĩa là tốc độ 115200 bit/giây, 8 bit dữ liệu, không bit chẵn lẻ, 1 bit dừng. Máy tính cài Python 3 là đủ cho phần chạy mô phỏng (dry-run); bo ESP32 hoặc Pico dùng cho phiên bản có phần cứng.

## Vì sao bài này nằm trên lộ trình

Chương 07 chứng minh robot có thể chạy khi người dùng gõ lệnh qua cổng nối tiếp. Chương 08 nâng cấp đường truyền đó thành giao thức mà chương trình máy tính có thể vận hành tự động và tin cậy. Sang Chương 09, ROS 2 giới thiệu các topic cũng dựa trên thông điệp có cấu trúc và kiểu dữ liệu rõ ràng; node cầu nối ở Chương 10 chỉ làm nhiệm vụ phiên dịch `geometry_msgs/Twist` thành đúng khung lệnh này. Nếu khung truyền thiếu chặt chẽ, mọi tầng phía trên như Nav2, vòng thị giác hay chính sách điều khiển học máy (Chương 12) đều sẽ gặp tình trạng robot giật cục mỗi khi rơi mất một byte.

![Các trường của khung serial]({{ site.imgurl }}/generated/ch08_serial_frame.png)

## Khái niệm

Giao tiếp UART truyền từng byte riêng lẻ chứ không tự động gom theo gói tin. Chip chuyển đổi USB-serial trả về bất kỳ lượng dữ liệu nào đã đến bộ đệm: có thể là nửa dòng, hai dòng dính liền hoặc phần dư từ lần đọc trước. Lệnh `Serial.println("40,-15")` nhìn có vẻ ổn trên Serial Monitor chỉ vì phần mềm đó chờ ký tự xuống dòng mới hiển thị; còn bộ phân tích (parser) trong vòng lặp điều khiển tốc độ cao buộc phải trả lời rõ ba câu hỏi: bản tin bắt đầu ở đâu, dài bao nhiêu byte và dữ liệu có toàn vẹn không.

Khóa học này sử dụng hai kiểu đóng khung: **khung phân cách** (kết thúc bằng ký tự `\n` — byte `0x0A`, tiện gõ tay trên terminal) và **khung theo độ dài** (gồm byte mở đầu, byte độ dài, đúng số byte tải tương ứng và byte kiểm tra). Khung theo độ dài vẫn hoạt động chính xác kể cả khi phần tải chứa dấu phẩy hay ký tự xuống dòng. Node cầu nối ở Chương 10 sẽ dùng khung theo độ dài, còn khung phân cách có thể giữ lại để gỡ lỗi thủ công.

Phần tải (payload) vẫn giữ dạng văn bản dễ đọc bằng mắt:

```text
V,40,-15
```

Trong đó `V` là mã lệnh vận tốc, `40` là lệnh bánh trái và `-15` là lệnh bánh phải (theo thang −100…100). Quy ước đơn vị phải được ghi rõ ở chú thích đầu cả hai chương trình, tránh việc một bên tự ý đổi sang m/s mà bên kia không biết.

Phép kiểm tra toàn vẹn trong bài này là phép XOR tất cả các byte trong phần tải thành một byte duy nhất, giúp phát hiện phần lớn lỗi lật bit đơn và khung bị cắt thiếu. Đây là cơ chế kiểm tra lỗi truyền dẫn chứ không phải mã hóa bảo mật (nếu triển khai ngoài môi trường lab, bạn có thể nâng cấp lên CRC sau khi đã làm chủ máy trạng thái):

$$
c = b_0 \oplus b_1 \oplus \cdots \oplus b_{n-1}
$$

Cấu trúc đầy đủ trên đường dây là `STX | LEN | payload | c | END`, với `STX = 0xAA` và `END = 0x0A`. Trường `LEN` chỉ độ dài của riêng phần `payload` (không tính các byte khung) và cần giới hạn tối đa 32 byte để một byte nhiễu không khiến vi điều khiển cấp phát bộ đệm quá lớn.

Bên nhận được cài đặt như một máy trạng thái gọn: tìm byte mở đầu `0xAA`, đọc `LEN`, đọc đủ `LEN` byte tải, đọc byte kiểm tra `c`, đọc byte kết thúc `END`, đối chiếu giá trị XOR rồi mới áp dụng lệnh. Bất kỳ sai lệch nào đều đưa máy trạng thái quay về bước tìm `0xAA`. Quan trọng nhất là cơ chế an toàn: nếu quá 300 ms không nhận được khung hợp lệ nào, lệnh động cơ phải tự động đặt về `0,0`. Một bộ phân tích khung đẹp nhưng thiếu timeout sẽ để robot chạy mãi theo lệnh cuối khi tuột cáp USB.

## Ví dụ làm từng bước

Đoạn mã Python sau dựng khung truyền cho lệnh bánh trái = 40 và bánh phải = −15:

```python
def frame(left: int, right: int) -> bytes:
    if not (-100 <= left <= 100 and -100 <= right <= 100):
        raise ValueError("wheel command out of range")
    payload = f"V,{left},{right}".encode("ascii")
    xor = 0
    for b in payload:
        xor ^= b
    return bytes([0xAA, len(payload)]) + payload + bytes([xor, 0x0A])

raw = frame(40, -15)
print(raw.hex(" "))
print("payload", raw[2:-2])
```

Kết quả in ra bắt đầu bằng `aa`, kết thúc bằng `0a`, và phần tải giải mã thành `V,40,-15`. Khi gọi `frame(40, -15)` hai lần, chuỗi hex thu được phải giống hệt nhau. Nếu đổi bánh phải thành `-16`, chỉ phần tải và byte XOR thay đổi; nếu tự ý sửa một byte tải mà giữ nguyên byte XOR cũ, phép kiểm tra sẽ phát hiện sai lệch ngay.

Trên vi điều khiển, tuyệt đối không dùng `delay()` để chờ đủ byte. Hãy gom các byte đọc được từ `read()` vào một bộ đệm nhỏ và chạy máy trạng thái trong mỗi chu kỳ vòng lặp (tốc độ vòng lặp này sẽ được đo ở Bài 08-05).

Ở phía máy tính, gửi khung bằng `pyserial`:

```python
import serial, time
ser = serial.Serial("/dev/ttyUSB0", 115200, timeout=0.05)

def send(left: int, right: int) -> None:
    ser.write(frame(left, right))
    ser.flush()

send(20, 20)
time.sleep(0.5)
send(0, 0)
```

Nếu chưa nối robot thật, bạn có thể thay tên cổng bằng cặp thiết bị giả lập PTY tạo bởi `socat` trong phần Lab. Khi đã nối mạch driver động cơ thật, luôn kê bánh xe rời khỏi mặt bàn.

## Lab

Thực hành chạy khô trên máy tính (chưa cần phần cứng robot):

```bash
python3 -m pip install pyserial
socat -d -d pty,raw,echo=0 pty,raw,echo=0
```

Lệnh `socat` sẽ in ra hai tên thiết bị nối thông nhau (ví dụ `/dev/pts/3` và `/dev/pts/4`). Bên gửi mở một cổng, bộ phân tích mở cổng còn lại:

```python
import serial
ser = serial.Serial("/dev/pts/4", 115200, timeout=0.05)
buf = bytearray()

def xor_of(data: bytes) -> int:
    x = 0
    for b in data:
        x ^= b
    return x

while True:
    buf += ser.read(64)
    while True:
        if not buf:
            break
        if buf[0] != 0xAA:
            del buf[0]
            continue
        if len(buf) < 2:
            break
        n = buf[1]
        if n > 32:
            del buf[0]
            continue
        if len(buf) < 2 + n + 2:
            break
        payload, check, end = bytes(buf[2:2+n]), buf[2+n], buf[3+n]
        del buf[:4+n]
        if end != 0x0A or check != xor_of(payload):
            print("DROP", payload, hex(check))
            continue
        print("OK", payload.decode())
```

**Kết quả mong đợi** sau khi gọi `send(40, -15)` từ cổng PTY bên kia:

```text
OK V,40,-15
```

Hãy gửi liên tiếp 10 khung hợp lệ: kết quả phải hiện đủ 10 dòng `OK` và không có dòng `DROP`. Sau đó thử gửi một khung bị cắt thiếu byte kiểm tra như `b"\xAA\x05V,40"`: bộ phân tích tuyệt đối không được in `OK`. Để mô phỏng tình huống rút cáp, hãy ngừng bên gửi; trên firmware thực tế, nhật ký serial phải ghi nhận hai kênh PWM tự đưa về 0 trong khoảng 300 ms.

**Khi hỏng thì thường vì**

| Bạn thấy | Nguyên nhân hay gặp |
| --- | --- |
| Rác vô hạn, không có `OK` | Lệch baud, thường 9600 với 115200, hoặc mở trùng một PTY |
| Không bao giờ `OK`, bộ đệm phình | `LEN` không khớp phần tải thực sự gửi |
| Động cơ chạy tiếp sau khi rút cáp | Chưa có timeout; lệnh cuối bị giữ |
| Serial Monitor được, Python thì không | Monitor tự thêm xuống dòng; script quên `END` hoặc `flush` |
| ESP32 reset khi động cơ quay | Động cơ ăn nguồn USB. Dùng pack chương 07 và mass chung |

## Mua ở Việt Nam

Phần thực hành chạy khô chỉ cần máy tính; phần chạy mạch thật sử dụng lại đúng bo mạch của Capstone A.

| Món | Cửa hàng | Từ khóa Shopee hoặc Lazada | Khoảng giá 2026, kiểm tra lúc mua |
| --- | --- | --- | --- |
| ESP32 DevKit V1 (30 chân, WROOM-32) | Tìm “ESP32” trên [hshop.vn](https://hshop.vn/) | `ESP32 DevKit V1 30 chân` | khoảng 80.000–180.000 đồng |
| USB-TTL CP2102 hoặc CH340, mức 3,3 V | cùng chỗ | `CP2102 USB TTL 3.3V` | khoảng 25.000–60.000 đồng |
| Pico hoặc Pico W nếu bạn ở MicroPython | [hshop.vn](https://hshop.vn/) tìm “Raspberry Pi Pico” | `Raspberry Pi Pico` | khoảng 120.000–250.000 đồng |

Lưu ý: mạch chuyển USB-TTL cấp nguồn 5 V vẫn phải xuất mức logic 3,3 V khi nối vào chân RX của ESP32. Nguồn động cơ luôn lấy từ pack pin robot, không lấy từ cổng USB máy tính. Khoảng giá trên chỉ mang tính tham khảo và có thể thay đổi theo thời điểm.

## Video tham khảo

- **Xem trước:** [Understanding UART](https://www.youtube.com/watch?v=sTHckUyxwp8) — Rohde & Schwarz, tiếng Anh. Giải thích cấu trúc khung byte trên đường truyền UART để thấy sự khác biệt với việc gửi chuỗi `println` đơn thuần.
- [Serial Communications Explained: UART, I2C, and SPI](https://www.youtube.com/watch?v=IyGwvGzrqp8) — Electronoobs, tiếng Anh. Đặt UART cạnh I2C và SPI để hiểu vì sao giao tiếp teleop giữa máy tính và vi điều khiển chọn UART.

## Bài tập

1. Tính tay giá trị XOR của các byte ASCII trong chuỗi `V,0,0`, sau đó đối chiếu với hàm `frame()`. Gợi ý: phép XOR có tính giao hoán nên thứ tự không đổi kết quả, và kết quả luôn nằm trong một byte `0x00`–`0xFF`.
2. Viết ba câu mô tả một tình huống mà bộ phân tích theo ký tự xuống dòng chấp nhận nhầm dữ liệu nhưng bộ phân tích theo độ dài sẽ từ chối. Gợi ý: phần tải chứa sẵn ký tự `\n` hoặc hai khung bị dính vào nhau trước khi kịp đọc xong khung đầu.
3. Nhật ký hiển thị `OK V,40,-15` rồi im lặng suốt 2 giây nhưng bánh xe vẫn quay. Firmware đang thiếu thành phần nào? Gợi ý: lưu mốc thời gian của khung hợp lệ cuối cùng và so sánh với `millis()`.
4. Nếu sửa giao thức sao cho các lệnh nằm ngoài dải −100…100 bị loại bỏ hoàn toàn thay vì kẹp giá trị, bên nào bắt buộc phải kiểm tra chặn — máy tính hay vi điều khiển? Gợi ý: vi điều khiển bắt buộc phải chặn để đảm bảo an toàn phần cứng; kiểm tra ở phía máy tính chỉ mang tính hỗ trợ.
5. Viết một câu chú thích rõ ràng để dán vào đầu mã nguồn cầu nối Chương 10, nêu đủ: đơn vị trên đường truyền serial, đơn vị trong ROS và thời gian timeout. Gợi ý: phía ROS dùng m/s và rad/s, đường truyền serial vẫn giữ thang −100…100 cho tới khi được quy đổi tập trung trong một hàm duy nhất.

## Đọc thêm

- [Tài liệu pyserial](https://pyserial.readthedocs.io/en/latest/shortintro.html) về mở cổng, thiết lập timeout và hàm `flush`.
- [Tham chiếu Serial của Arduino](https://www.arduino.cc/reference/en/language/functions/communication/serial/) dành cho firmware Capstone viết bằng C++.
- [REP-103](https://www.ros.org/reps/rep-0103.html) về quy ước chiều trục tọa độ sẽ ánh xạ lên khung lệnh này.
- Ghi chú giao thức teleop ở Chương 07 và Bài 04 Chương 10 — nơi trực tiếp tiêu thụ khung truyền bạn vừa thiết kế.
