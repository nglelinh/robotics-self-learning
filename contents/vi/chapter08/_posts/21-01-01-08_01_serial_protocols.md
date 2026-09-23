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

Thời lượng: **~90 phút**.

## Mục tiêu

Hết bài này bạn thiết kế được một khung lệnh bánh xe còn nguyên vẹn dù USB giao từng mẩu, viết được phía máy tính bằng Python và phía ESP32 hoặc Pico, và giải thích được vì sao `println` chuỗi `"40,-15"` chưa phải giao thức. Bạn tính được byte XOR, chỉ ra khoảng timeout phải đưa động cơ về 0, và lưu một khung đúng cùng một khung cố ý hỏng vào `lab-notes.md`. Đây là hợp đồng mà cầu nối ROS 2 ở chương 10 sẽ dùng lại, để `cmd_vel` không biến thành “vài byte tình cờ nằm trong bộ đệm.”

## Kiến thức cần trước

Bạn đã nhấp nháy LED và in một dòng ở chương 02, và đã có bản teleop Capstone A ở chương 07, kể cả khi bản đó vẫn gửi chữ thô. Bạn biết một byte là 8 bit và `115200 8N1` nghĩa là 115200 bit/giây, 8 bit dữ liệu, không parity, một bit dừng. Máy tính có Python 3 là đủ cho buổi chạy khô. ESP32 hoặc Pico là bản có phần cứng của cùng lab đó.

## Vì sao bài này nằm trên lộ trình

Chương 07 cho thấy robot chạy được khi bạn gõ trên cổng serial. Chương 08 biến đường đó thành thứ một chương trình có thể tin. Chương 09 giới thiệu topic ROS 2, cũng là thông điệp có khung và có kiểu. Node cầu nối ở chương 10 chỉ là bộ dịch: `geometry_msgs/Twist` đi vào, khung này đi ra. Khung mơ hồ thì Nav2, vòng thị giác, hay một policy học được ở chương 12 đều kế thừa một robot giật khi mất một byte. Phần robot learning giả định kênh lệnh tầng dưới đã hỏng theo hướng an toàn.

![Các trường của khung serial]({{ site.imgurl }}/generated/ch08_serial_frame.png)

## Khái niệm

UART chuyển byte, không chuyển thông điệp. Chip USB-serial đưa những gì đã tới, có thể là nửa dòng, hai dòng, hoặc mẩu sót từ lần đọc trước. `Serial.println("40,-15")` trông ổn trên Serial Monitor vì cửa sổ đó đợi ký tự xuống dòng rồi mới vẽ chữ. Parser trong vòng lặp nhanh không được ưu đãi đó. Nó phải trả lời ba câu: thông điệp bắt đầu ở đâu, dài bao nhiêu, và có đến nguyên vẹn không.

Khóa học này dùng hai cách đóng khung. **Khung ngăn cách** kết thúc bằng `\n` (byte `0x0A`), dễ gõ trên terminal. **Khung độ dài** mở bằng một dấu, rồi một số đếm, rồi đúng bấy nhiêu byte tải, rồi một byte kiểm. Cách thứ hai vẫn đúng khi phần tải chứa dấu phẩy hoặc dấu xuống dòng. Cầu nối chương 10 nói khung độ dài. Giữ khung ngăn cách làm cửa sổ gỡ lỗi bạn gõ tay được.

Phần tải vẫn đọc được bằng mắt:

```text
V,40,-15
```

`V` là lệnh vận tốc, `40` là bánh trái theo thang −100…100 của chương 07, `-15` là bánh phải. Đơn vị nằm trong chú thích đầu cả hai chương trình. Đừng lặng lẽ đổi một phía sang mét trên giây.

Phép kiểm của bài này là XOR mọi byte tải, gói trong một byte. Nó bắt nhiều lỗi một bit và hầu hết khung bị cắt. Nó không phải tính năng bảo mật. CRC là bước sau nếu bạn rời bàn lab; chưa cần CRC để học máy trạng thái.

$$
c = b_0 \oplus b_1 \oplus \cdots \oplus b_{n-1}
$$

Ảnh trên dây là `STX | LEN | payload | c | END`, với `STX = 0xAA` và `END = 0x0A`. `LEN` là độ dài phần tải, không phải độ dài cả khung. Từ chối `LEN` lớn hơn 32 để một byte hỏng không bắt vi điều khiển cấp phát bộ đệm khổng lồ.

Bên nhận là máy trạng thái nhỏ: săn `0xAA`, đọc `LEN`, đọc đúng `LEN` byte, đọc byte kiểm, đọc byte kết thúc, so XOR, rồi mới áp lệnh. Bất ngờ nào cũng quay về trạng thái săn. Nếu 300 ms không có khung tốt, lệnh bánh xe đang áp dụng trở thành `0,0`. Timeout đó mới là tính chất an toàn. Parser đẹp mà không có timeout sẽ phát lại lệnh cuối mãi khi rút cáp USB.

## Ví dụ làm từng bước

Dựng khung cho bánh trái = 40 và bánh phải = −15.

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

Bạn sẽ thấy một dòng bắt đầu bằng `aa` và kết thúc bằng `0a`, phần tải giải mã thành `V,40,-15`. Gọi `frame(40, -15)` hai lần: chuỗi hex phải y hệt. Đổi bánh phải thành `-16` thì chỉ phần tải và byte XOR đổi. Tự sửa một byte tải rồi tính lại XOR: byte kiểm cũ không còn khớp. Đó là bài kiểm bạn sẽ tự động hóa ở phần bài tập.

Trên vi điều khiển, đừng `delay()` trong lúc đợi byte. Nối những gì `read()` trả về vào bộ đệm nhỏ và chạy máy trạng thái một lần mỗi vòng. Bài 08-05 đo vòng đó. Bài này cần khung đúng trước đã.

Phía máy tính, với `pyserial`:

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

Khi robot không ở trên bàn, thay cổng bằng PTY của `socat` trong lab. Hễ driver động cơ đã nối thì bánh xe phải được nhấc khỏi mặt đất.

## Lab

Chạy khô, chưa cần robot.

```bash
python3 -m pip install pyserial
socat -d -d pty,raw,echo=0 pty,raw,echo=0
```

`socat` in hai tên thiết bị, ví dụ `/dev/pts/3` và `/dev/pts/4`. Bên gửi dùng một cổng, parser dùng cổng kia.

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

**Kết quả mong đợi** sau `send(40, -15)` từ PTY bên kia:

```text
OK V,40,-15
```

Gửi mười khung. Phải có mười dòng `OK` và không có `DROP`. Rồi gửi một khung hỏng `b"\xAA\x05V,40"` thiếu byte kiểm: parser không được in `OK`. Rút cáp được giả lập bằng cách ngừng bên gửi: ghi chú firmware phải nói lệnh cuối hết hạn. Trên mạch thật, log serial phải cho thấy hai chân PWM tắt trong khoảng 300 ms.

**Khi hỏng thì thường vì**

| Bạn thấy | Nguyên nhân hay gặp |
| --- | --- |
| Rác vô hạn, không có `OK` | Lệch baud, thường 9600 với 115200, hoặc mở trùng một PTY |
| Không bao giờ `OK`, bộ đệm phình | `LEN` không khớp phần tải thực sự gửi |
| Động cơ chạy tiếp sau khi rút cáp | Chưa có timeout; lệnh cuối bị giữ |
| Serial Monitor được, Python thì không | Monitor tự thêm xuống dòng; script quên `END` hoặc `flush` |
| ESP32 reset khi động cơ quay | Động cơ ăn nguồn USB. Dùng pack chương 07 và mass chung |

## Mua ở Việt Nam

Buổi chạy khô chỉ cần laptop. Bản có mạch dùng đúng board Capstone A.

| Món | Cửa hàng | Từ khóa Shopee hoặc Lazada | Khoảng giá 2026, kiểm tra lúc mua |
| --- | --- | --- | --- |
| ESP32 DevKit V1 (30 chân, WROOM-32) | Tìm “ESP32” trên [hshop.vn](https://hshop.vn/) | `ESP32 DevKit V1 30 chân` | khoảng 80.000–180.000 đồng |
| USB-TTL CP2102 hoặc CH340, mức 3,3 V | cùng chỗ | `CP2102 USB TTL 3.3V` | khoảng 25.000–60.000 đồng |
| Pico hoặc Pico W nếu bạn ở MicroPython | [hshop.vn](https://hshop.vn/) tìm “Raspberry Pi Pico” | `Raspberry Pi Pico` | khoảng 120.000–250.000 đồng |

Module USB-TTL 5 V vẫn phải nói logic 3,3 V vào chân RX của ESP32. Nguồn động cơ lấy từ pack robot, không lấy từ cổng USB laptop. Giá đổi; khoảng trên chỉ để kiểm tra túi tiền, không phải báo giá.

## Bài tập

1. Tính tay XOR các byte ASCII của `V,0,0`, rồi đối chiếu với hàm `frame()`. Gợi ý: XOR giao hoán, thứ tự byte không đổi kết quả, và kết quả là một byte trong `0x00`–`0xFF`.
2. Viết ba câu về một tình huống parser theo dấu xuống dòng nhận một lệnh mà parser theo độ dài từ chối. Gợi ý: phần tải có sẵn `\n`, hoặc hai lệnh dính vào nhau trước khi bạn đọc xong lệnh đầu.
3. Log có `OK V,40,-15` rồi im 2 giây trong khi bánh vẫn quay. Firmware thiếu dòng nào? Gợi ý: mốc thời gian của khung tốt cuối và so với `millis()`.
4. Sửa giao thức để lệnh ngoài −100…100 bị bỏ, không bị kẹp. Phía nào phải chặn, máy tính hay MCU? Gợi ý: MCU phải chặn. Phía máy tính chỉ là tiện.
5. Viết câu bạn sẽ dán vào chú thích cầu nối chương 10: đơn vị trên dây, đơn vị trong ROS, và timeout. Gợi ý: phía ROS sau này là m/s và rad/s; dây này vẫn là −100…100 cho đến khi bài đó quy đổi trong một hàm.

## Đọc thêm

- [Tài liệu pyserial](https://pyserial.readthedocs.io/en/latest/shortintro.html) về cổng, timeout và `flush`.
- [Tham chiếu Serial của Arduino](https://www.arduino.cc/reference/en/language/functions/communication/serial/) nếu firmware Capstone viết bằng C++.
- [REP-103](https://www.ros.org/reps/rep-0103.html) về chiều trục mà sau này bạn ánh xạ lên khung này.
- Ghi chú teleop chương 07 trong khóa, và bài 04 chương 10, nơi tiêu thụ khung bạn vừa chốt.
