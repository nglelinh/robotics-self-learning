---
layout: post
title: "Teleop serial: thiết kế giao thức"
chapter: "07"
order: 3
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter07
lesson_type: required
draft: false
---

Bài 02 đã chốt ý nghĩa chiều quay của giá trị dương trên từng bánh xe. Bài này thiết kế định dạng bản tin (giao thức) để gửi hai con số đó qua cổng nối tiếp; phần lập trình vòng lặp firmware sẽ thực hiện ở Bài 04.

## Mục tiêu học

1. Đặc tả giao thức văn bản UTF-8 kết thúc bằng ký tự xuống dòng trên chuẩn 115200 8N1: lệnh `V <trái> <phải>` gồm hai số nguyên và lệnh `S` dùng để dừng khẩn cấp.
2. Nêu rõ khoảng giới hạn (kẹp giá trị) mà firmware sẽ áp dụng là $$-180$$ đến $$+180$$, và giải thích vì sao trong giai đoạn học tập không dùng toàn thang $$0$$–$$255$$.
3. Quy định máy chủ phải gửi lặp lại lệnh tối thiểu mỗi $$200~\mathrm{ms}$$ và ngưỡng quá hạn (timeout) của firmware là $$250~\mathrm{ms}$$, đảm bảo khi mất tín hiệu thì động cơ tự động về PWM 0 thay vì giữ nguyên tốc độ cũ.
4. Loại bỏ hoàn toàn các dòng sai cú pháp, đồng thời xác định đúng chuyển động tương ứng với năm khung lệnh mẫu theo quy ước dấu của Bài 02.

## Kiến thức cần có

Bài 07-01 đã hoàn chỉnh nguồn và mass chung; Bài 07-02 đã chốt bảng dấu (lệnh dương đẩy cả hai lốp tiến về phía mũi xe, chỉ đảo chiều ở một nơi duy nhất). Chương 05 giải thích cách các giá trị này chuyển thành điện áp cầu H, còn Chương 06 cung cấp hai phương trình hình học:

$$
v = \frac{v_r + v_l}{2}, \qquad \omega = \frac{v_r - v_l}{b},
$$

với khổ vết $$b$$ đã đo (ví dụ $$b = 0{,}15~\mathrm{m}$$, $$r = 31{,}2~\mathrm{mm}$$). Bạn chỉ cần biết mở Serial Monitor; phần viết bộ phân tích (parser) nằm ở Bài 04 và bài này chưa dùng ROS.

## Vì sao bài này quan trọng với Capstone A và ROS

Teleop qua cổng nối tiếp là kênh giao tiếp khép kín đầu tiên với hai động cơ. Giao thức dạng văn bản giúp bạn dễ dàng đọc, quan sát và tự gõ thử trên Serial Monitor; định dạng nhị phân chỉ nên cân nhắc sau này khi hệ thống đã ổn định. Về bản chất, cơ chế này tương đồng với `geometry_msgs/Twist` trong ROS: `linear.x` là vận tốc tiến, `angular.z` là tốc độ quay yaw và driver tách thành lệnh cho hai bánh theo hai phương trình trên. Tuy nhiên, trong chương này hai số nguyên vẫn chỉ là nấc PWM chứ chưa phải m/s — bước hiệu chuẩn sang m/s sẽ thực hiện ở Chương 08. Gán vội "`V 80 80` tương đương $$0{,}2~\mathrm{m/s}$$" khi chưa đo là hiệu chuẩn giả.

![Dòng `V` hợp lệ thì chạy; quá 250 ms hoặc dòng `S` thì dừng]({{ site.imgurl }}/generated/teleop_states.png)

Hãy đọc sơ đồ trạng thái trên như một bản hợp đồng vận hành: ở trạng thái `IDLE`, động cơ tắt và chờ lệnh. Khi nhận dòng `V` hợp lệ, hệ thống chuyển sang `RUN` và đặt lại bộ đếm thời gian quá hạn. Nếu quá $$250~\mathrm{ms}$$ không có lệnh mới hoặc nhận được lệnh `S`, hệ thống lập tức chuyển về `STOP` và đưa PWM về 0. Một dòng `V` hợp lệ mới sẽ đưa xe trở lại `RUN`. Khi đường truyền im lặng, mạch tuyệt đối không được duy trì mức duty cũ.

## Byte, khoảng kẹp, và hạn

Cấu hình cổng nối tiếp là 115200 baud, 8 bit dữ liệu, không bit chẵn lẻ, 1 bit dừng (8N1). Mỗi khung lệnh là một dòng văn bản UTF-8 kết thúc bằng `\n`. Ký tự `\r` (nếu có trước `\n`) chỉ là nhiễu định dạng mà bộ phân tích cần bỏ qua, không xem như lệnh thứ hai.

Lệnh `V <trái> <phải>` chứa hai số nguyên. Firmware ở Bài 04 sẽ kẹp từng giá trị vào khoảng $$-180..180$$. Ngưỡng trần này được đặt có chủ đích: mở hết thang 255 trên pack 2S đầy làm xe vọt quá nhanh khi mới thử nghiệm (những vòng chạy đầu ở Bài 02 chỉ dùng mức 60–80). Mức 180 tương ứng hệ số duty:

$$
D = \frac{180}{255} \approx 0{,}706
$$

đủ mạnh để thử trên sàn nhưng vẫn kiểm soát được an toàn. Lệnh `S` lập tức đặt cả hai mục tiêu về 0 để dừng khẩn cấp; lệnh `V 0 0` cũng dừng xe nhưng mang ý nghĩa lệnh điều khiển bình thường.

Trong lúc muốn xe tiếp tục chạy, máy chủ phải gửi lại lệnh ít nhất mỗi $$200~\mathrm{ms}$$. Nếu quá $$250~\mathrm{ms}$$ mà firmware không nhận được lệnh `V` hoặc `S` hợp lệ, hệ thống coi kết nối máy chủ đã mất và tự ép mục tiêu về 0. Khoảng dự phòng $$50~\mathrm{ms}$$ đủ dung sai cho độ trễ nhất thời của gói USB, nhưng không để xe chạy tự do khi laptop bị treo hoặc rơi vào chế độ ngủ. Nếu rút cáp hoặc ngừng gửi mà PWM vẫn giữ nguyên ở mức 80 thì cơ chế quá hạn đang bị lỗi.

Mọi dòng không đúng cú pháp đều bị loại bỏ hoàn toàn: mục tiêu hợp lệ trước đó giữ nguyên cho đến khi hết hạn, và dữ liệu rác không bao giờ được gây ra chuyển động ngoài ý muốn. Cụ thể, `V 80` thiếu tham số bánh phải, `V 80 foo` không được tự suy diễn thành 0 cho bánh phải, và ký tự lệnh phải là chữ hoa `V` (không chấp nhận `v`).

## Năm khung, một quy ước dấu

Giá trị dương trên mỗi bánh tương ứng chiều tiến về phía mũi xe (Bài 02). Khi bánh phải nhanh hơn bánh trái, robot quay sang trái (yaw dương, khớp với Chương 06) vì:

$$
\omega = \frac{v_r - v_l}{b}
$$

dương khi $$v_r > v_l$$. Lưu ý rằng dấu chiều quay hoàn toàn khớp, nhưng các con số trong bảng dưới đây là nấc PWM chứ chưa phải vận tốc m/s:

| Dòng | PWM trái | PWM phải | Bạn đang xin |
|------|----------|----------|----------------|
| `V 80 80` | $$+80$$ | $$+80$$ | Cả hai tiến, thẳng |
| `V -80 -80` | $$-80$$ | $$-80$$ | Cả hai lùi |
| `V -60 60` | $$-60$$ | $$+60$$ | Quay trái (phải tiến, trái lùi) |
| `V 0 0` | $$0$$ | $$0$$ | Dừng |
| `S` | target 0 | target 0 | Dừng khẩn |

Tương tự, `V 60 -60` cho chuyển động quay phải khi bảng dấu đã chính xác. Nếu bỏ sót bước chỉnh dấu ở Bài 02, các khung lệnh trên sẽ quay sai hướng — hãy sửa đúng một lần ở Bài 02.

Tính thử thời gian truyền cho khung `V -60 60\n`: chuỗi gồm 9 byte (`V`, khoảng trắng, `-`, `6`, `0`, khoảng trắng, `6`, `0`, `\n`). Ở tốc độ 115200 8N1 (10 bit cho mỗi byte tính cả bit start và stop), thời gian truyền trên đường dây là:

$$
t \approx \frac{9 \times 10}{115200} \approx 0{,}78~\mathrm{ms}.
$$

Thời gian truyền chỉ chưa tới 1 miligiây, rất nhỏ so với nhịp gửi lại $$200~\mathrm{ms}$$. Do đó, giao thức văn bản hoàn toàn không gây nghẽn đường truyền UART, trong khi đổi sang nhị phân sẽ làm mất đi sự tiện lợi khi quan sát và gõ trực tiếp lệnh `S`.

Không nên tự gán giá trị tốc độ vật lý khi chưa đo đạc thực tế. Ví dụ, nếu tự giả định PWM 80 bằng $$0{,}20~\mathrm{m/s}$$ trên cả hai bánh để tính:

$$
v = \frac{0{,}20+0{,}20}{2} = 0{,}20~\mathrm{m/s}, \qquad \omega = 0,
$$

phép tính tuy gọn nhưng số liệu vật lý là tự suy diễn. Ở Chương 08, bạn sẽ đo thời gian chạy trên quãng đường 1 mét để hiệu chuẩn tốc độ thực; còn hiện tại, `V 80 80` chỉ mang nghĩa chạy tiến ở mức 80 nấc PWM theo bảng dấu.

## Lab

### An toàn

Bài này chỉ thiết kế và gõ thử văn bản, chưa chạy động cơ. Nếu trên ESP32 vẫn còn nạp chương trình cũ và dây động cơ đã gắn sẵn, hãy ngắt công tắc nguồn pin trước khi mở Serial Monitor. Sản phẩm của bài này là đặc tả năm khung lệnh; sang Bài 04 mới nạp firmware điều khiển và khi đó bánh xe vẫn phải kê trên không.

### BOM

| Món | Việc |
|------|------|
| `lab-notes.md` hoặc serial monitor | Nơi năm khung nằm |
| Bảng dấu bài 07-02 | Nghĩa của dương |
| ESP32 tùy chọn, USB, không VM | Để thấy ký tự vọng |
| Máy tính | Kiểm tra thời gian 9 byte |

### Các bước

1. Ghi đầy đủ thông số giao thức vào sổ tay: 115200 8N1, UTF-8, kết thúc bằng `\n`, khoảng kẹp $$-180..180$$, chu kỳ gửi lại của máy chủ $$200~\mathrm{ms}$$, thời gian quá hạn của firmware $$250~\mathrm{ms}$$.
2. Ngay dưới bảng dấu, viết năm khung lệnh chuẩn (`V 80 80`, `V -80 -80`, `V -60 60`, `V 0 0`, `S`) kèm ý nghĩa chuyển động tương ứng: đi thẳng, lùi, quay trái, dừng, dừng khẩn.
3. Tạo hai dòng lệnh sai cú pháp (ví dụ `V 80` và `V 80 foo`) và ghi chú bên cạnh: “bỏ qua hoàn toàn, không làm quay một bánh”.
4. Nếu có kết nối Serial Monitor (đã ngắt nguồn driver), gõ thử năm dòng hợp lệ để kiểm tra ký tự hiển thị.
5. Tính lại thời gian truyền khung `V -60 60\n` như ví dụ và đặt cạnh chu kỳ $$200~\mathrm{ms}$$ để phân biệt rõ hai thang thời gian.

### Kết quả mong đợi

Sổ tay `lab-notes.md` ghi đầy đủ năm khung lệnh mẫu, câu khẳng định “dương là tiến trên cả hai bánh”, khoảng kẹp giá trị, hai mốc thời gian ($$200~\mathrm{ms}$$ máy chủ và $$250~\mathrm{ms}$$ firmware) và lưu ý rõ nấc PWM chưa phải đơn vị m/s. Ảnh chụp Serial Monitor là tùy chọn; bài này chưa yêu cầu robot chạy.

### Lỗi thường gặp

| Bạn thấy | Thường là |
|----------|-----------|
| `V -60 60` bị mô tả là quay phải | Quy ước dấu bị lật; phải nhanh hơn là yaw trái |
| Một số được nhận thành chỉ bánh trái | Ngữ pháp bị áp một nửa; bỏ cả dòng |
| Hạn ghi 2 s "cho an toàn" | Máy ngủ sẽ còn kéo xe vài giây; dùng $$250~\mathrm{ms}$$ |
| `V 80 80` dán nhãn $$0{,}2~\mathrm{m/s}$$ | Hiệu chuẩn giả; chương 08 chưa tới |
| Chép struct nhị phân từ blog | Không gõ được, và không thấy nó hỏng |

## Mua ở Việt Nam / Where to buy in Vietnam

Bài này không phát sinh linh kiện bắt buộc mới. Nếu bạn chưa có ESP32 để thực hành, chỉ cần mua thêm một bo ESP32 devkit (giá tham khảo khoảng năm 2026: 70.000–150.000 đồng, bản dùng chip nạp CP2102 hoặc CH340 đều phù hợp). Chỉ nên đổi sang Raspberry Pi Pico nếu bạn tự viết lại phần cấu hình PWM LEDC ở Bài 04 vì mã nguồn mẫu viết cho Arduino-ESP32.

- L298N đã kiểm, khoảng 45.000 đồng, chỉ khi vẫn thiếu cầu: [hshop.vn/mach-dieu-khien-dong-co-dc-l298](https://hshop.vn/mach-dieu-khien-dong-co-dc-l298)
- [Hshop ESP32](https://hshop.vn/search?q=ESP32)
- [Shopee ESP32](https://shopee.vn/search?keyword=ESP32%20devkit)
- [Lazada ESP32](https://www.lazada.vn/catalog/?q=ESP32)
- [Thế Giới IC ESP32](https://www.thegioiic.com/search?q=ESP32)

## Video tham khảo

- **Xem trước:** [Understanding UART](https://www.youtube.com/watch?v=sTHckUyxwp8) — Rohde & Schwarz, tiếng Anh. Giải thích cấu trúc khung truyền UART gồm bit start, dữ liệu và bit stop — lớp truyền dẫn cho giao thức teleop của bài này.

## Bài tập

1. Chuỗi `V -60 60\n` gồm bao nhiêu byte và mất bao lâu để truyền xong ở tốc độ 115200 8N1?
2. Dòng lệnh hợp lệ cuối cùng đến tại thời điểm $$t = 0$$, sau đó máy tính chuyển sang chế độ ngủ. Khi nào firmware phải ép mục tiêu về 0, và vì sao máy chủ cần gửi lặp lại mỗi $$200~\mathrm{ms}$$?
3. Serial Monitor gửi lần lượt `V 80` rồi `V 200 -90`. Dòng nào sai cú pháp, và firmware Bài 04 sẽ kẹp dòng hợp lệ thành cặp giá trị nào?
4. Vì sao `V -60 60` tương ứng với chuyển động quay trái? Với $$b = 0{,}15~\mathrm{m}$$ (chỉ dùng để kiểm tra dấu), hiệu $$(\mathrm{phải} - \mathrm{trái})$$ dương hay âm, và tại sao phép chia cho $$b$$ vẫn chưa cho ra đơn vị rad/s?
5. Một người đề xuất đóng gói hai giá trị thành hai biến `int16` nhị phân để “truyền nhanh hơn”. Cách làm đó làm mất lợi ích gì trên Serial Monitor, và thời gian truyền $$0{,}78~\mathrm{ms}$$ có đủ lý do để chuyển sang nhị phân không?

### Gợi ý đáp án

1. Gồm 9 byte (`V`, khoảng trắng, `-`, `6`, `0`, khoảng trắng, `6`, `0`, `\n`). Thời gian truyền xấp xỉ $$9 \times 10 / 115200 \approx 0{,}78~\mathrm{ms}$$.
2. Firmware phải ép mục tiêu về 0 tại $$t = 250~\mathrm{ms}$$. Chu kỳ gửi lại $$200~\mathrm{ms}$$ chừa ra $$50~\mathrm{ms}$$ dự phòng để độ trễ nhỏ của đường truyền không làm ngắt lệnh ngoài ý muốn.
3. `V 80` không hợp lệ và bị loại bỏ hoàn toàn. `V 200 -90` hợp lệ và sẽ được kẹp thành $$180$$ và $$-90$$.
4. Bánh trái $$-60$$ (lùi), bánh phải $$+60$$ (tiến) nên mũi xe quay sang trái. Hiệu $$(\mathrm{phải} - \mathrm{trái}) = 60 - (-60) = +120 > 0$$, khớp dấu dương của $$\omega$$ ở Chương 06, nhưng đây là nấc PWM nên chia cho $$b$$ không ra đơn vị rad/s.
5. Mất khả năng quan sát trực tiếp và tự gõ lệnh kiểm thử trên Serial Monitor. Thời gian truyền dạng chữ chưa tới $$1~\mathrm{ms}$$, rất nhỏ so với chu kỳ $$200~\mathrm{ms}$$, nên chuyển sang nhị phân không giải quyết được vấn đề thời gian thực hay kiểm tra kết nối máy chủ.

## Đọc thêm

- [Arduino `Serial`](https://www.arduino.cc/reference/en/language/functions/communication/serial/)
- [pySerial, phần mở đầu](https://pyserial.readthedocs.io/en/latest/shortintro.html)
- [geometry_msgs/Twist (Jazzy)](https://docs.ros.org/en/jazzy/p/geometry_msgs/interfaces/msg/Twist.html)
- [Mục lục gói geometry_msgs (Jazzy)](https://docs.ros.org/en/jazzy/p/geometry_msgs/)
