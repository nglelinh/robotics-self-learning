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

Hết bài này bạn khép chương 03 bằng chứng cứ chứ không bằng một cột dấu tick đầy hy vọng. Bạn chỉ được một log serial của nút, các dòng duty PWM hoặc một tấm ảnh LED ở hai mức duty, một số đếm chống dội khớp số lần nhấn với sai số không, và một sơ đồ trạng thái có mũi tên im lặng ghi 300 ms. Bạn chỉ viết câu "PWM bằng không trong FAULT" khi code làm câu đó thành thật, và bạn bác một checklist đánh dấu PWM xong trong khi lệnh duty duy nhất nằm trong `setup()`.

## Kiến thức cần có

Bài 1 đến bài 5 là phần việc trang này gác cổng. Bạn cần nhịp tim không chặn đã thay [nhịp chương 02]({% multilang_post_url contents/chapter02/02_04_blink_serial_hello %}), nút kéo lên, nhịp thở LEDC hoặc `duty_u16`, ISR ngắn, và máy IDLE / TELEOP / FAULT. Phần cứng chưa về không được tính đạt: được phép đọc khô mã của chính mình chỉ khi file đã có và bạn trích được dòng timeout cùng dòng duty về không từ chúng. "Tôi sẽ thêm timeout khi khung xe tới" là không đạt.

## Vì sao bài này quan trọng

Các chương sau sẽ nói như thể firmware vi sai đã nhận một lệnh teleop và đã thả cả hai kênh PWM khi lệnh đó im 300 ms. Một đồ thị ROS sẽ phát twist bên trên giả định ấy. Nó sẽ không nhận ra log nút của bạn là một dòng chảy mẫu, rằng duty chỉ được ghi một lần lúc boot, hoặc FAULT vẫn để nguyên `ledcWrite` cuối. Bánh ở trên không cho tới khi những sự thật đó nằm trong sổ. Checklist này là hợp đồng các chương sau được phép giả định, và một dấu tick không kèm hiện vật thì không phải một dòng trong hợp đồng.

## Nội dung

Mỗi cổng là một quan sát cộng hiện vật chứng minh nó. Cảm giác nút "cơ bản là chạy" không phải một cổng. Monitor serial mới là cổng. Làm bằng ngôn ngữ bạn sẽ giữ cho Capstone A. Hôm nay bạn không phải lặp mọi listing ở ngôn ngữ kia, nhưng file bạn nộp phải là kiểu không chặn của bài 1. Một checklist đạt trên `delay(1000)` là đã trượt chương dù LED có đổi.

Cổng nút là một đoạn dán từ log lab GPIO: một `press` và một `release` mỗi cử chỉ, không phải một dòng mỗi mili giây. Số chân và chữ `INPUT_PULLUP` hoặc `Pin.PULL_UP` đứng cạnh đoạn dán. Nếu lần đầu chân nhả bị nổi, sổ được nói vậy, và log bạn nộp là log sau khi kéo lên đã trở lại.

Cổng PWM là một tấm ảnh cùng LED rõ tối và rõ sáng, hoặc ba dòng serial có duty khoảng 25%, 50% và 90% của đúng thang bạn đã cấu hình. Vì ESP32 Arduino 3.x không hứa `analogWrite` là 8 bit, ghi chú phải nêu `ledcAttach` cùng độ phân giải, hoặc nêu `duty_u16`. Một dòng "PWM chạy" và một sketch không in con số thì không phải cổng này. Tải trong ảnh là LED và điện trở nối tiếp. Một động cơ trong ảnh làm cổng này trượt, kể cả khi motor đã quay, vì chương này không gắn motor vào GPIO và không đòi VM đã đấu.

Cổng chống dội là một cặp số. Bạn nhấn $N$ lần. Bộ đếm in $N$, nên sai số là

$$
e = N_{\mathrm{in}} - N_{\mathrm{nhấn}} = 0.
$$

Log chùm của bài ngắt, bản nhảy một lượng trong khoảng 5–30 khi cửa sổ đứng yên bị bỏ, có thể nằm bên dưới như một đối chiếu. Nó không thay cho $e = 0$. Nếu lần chống dội khá nhất của bạn vẫn tăng hai nhịp mỗi cú nhấn, mục checklist còn mở và bạn quay lại phép thử 20 ms.

Cổng sơ đồ là một hình trong sổ, không phải chỉ một ảnh chụp hình của bài. Chép hình bài làm khung thì được. Mũi tên từ TELEOP sang FAULT phải ghi timeout bạn đã biên dịch, 300 ms, và cả IDLE lẫn FAULT phải được đánh duty 0. Câu trong sổ đúng là điều code khẳng định: "PWM bằng không trong FAULT." Nếu hàm `apply` của bạn thắp LED mỗi khi `duty` khác không, bất kể trạng thái, bạn chưa được viết câu đó.

![Thứ tự cấp nguồn: logic trước, nguồn motor sau, bánh nhấc]({{ site.imgurl }}/generated/power_order.png)

Hình thứ tự nguồn là biên của chương này. USB nuôi vi điều khiển. Rail 3,3 V nuôi kéo lên của nút và nuôi LED. Nguồn motor, VM trên TB6612, là một ô sau trong hình đó, và hôm nay ô ấy để trống. Bánh nhấc lên là tư thế của ngày đầu VM được nối, và ngày đó không phải chữ ký của chương 03. Ký checklist không cho phép một sợi dây motor.

## Ví dụ tính tay: một checklist nói dối

Một sổ nộp đánh dấu "nút," "PWM," "chống dội," và "máy trạng thái." Mã nguồn kèm theo chỉ có thế này:

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

Đọc nó theo các cổng. Không có nút, nên log nhấn không thể tồn tại. `ledcWrite` chạy một lần, trong `setup`, ở mức 180 cố định, khoảng 70%, và không bao giờ là 0. Không gì trong `loop` đọc `millis()`, nên im lặng 300 ms không đổi được chân. `delay(1000)` là kiểu hỏng của bài 1: lần đầu vòng lặp kịp nhìn một mốc thời gian thì hạn đã bị trễ gấp ba. Dòng in `PWM done` là một chú thích, không phải một phép đo. Đánh dấu ô PWM vì các chữ `ledcWrite` xuất hiện là cách chương này đẻ ra một robot vừa boot đã chạy.

Buổi soi lại viết dấu tick thành bốn lần trượt. PWM không được chứng minh qua nhiều duty, và không được chứng minh ở 0. Timeout vắng mặt, nên không vào được FAULT và câu "PWM bằng không trong FAULT" sẽ sai: không có FAULT, và chân không ở không. Vòng lặp bị chặn cả giây, dài hơn ngưỡng cắt

$$
1000\,\mathrm{ms} > 300\,\mathrm{ms}.
$$

Một sketch đã sửa ghi duty từ máy trạng thái mỗi vòng, log duty khi nó đổi, và dùng đồng hồ bài 1. Mục checklist chỉ lật sau khi những dòng đó nằm trong file bạn vừa nạp, và sau khi bạn đã thấy LED tắt khi ngừng gõ.

Cùng cách soi bắt một bản tinh hơn: máy trạng thái là thật, nhưng `setup` kết thúc bằng `ledcWrite(PIN, 180)` và FAULT quên ghi 0 vì tác giả tin "mình không gọi ledcWrite nữa thì motor tắt." Ngoại vi PWM giữ duty cuối. Không gọi hàm nghĩa là các xung cũ vẫn chạy. FAULT phải ghi không một cách tường minh, mỗi vòng, cho cả hai kênh bạn sau này sẽ nối vào TB6612.

## Cái bạn nộp

Đi xuống danh sách này trong sổ lab. Mục nào không có hiện vật thì còn mở.

1. Log nút. Dán một press và một release, nêu GPIO, và nêu kéo lên. Một cặp mỗi cử chỉ.
2. Chứng cứ PWM. Chụp LED ở hai độ sáng hoặc dán các duty gần 25%, 50% và 90%, và ghi API (`ledcAttach` cùng độ phân giải, hoặc `duty_u16`). Có một dòng duty bằng 0.
3. Số chống dội. Viết $N$ lần nhấn và $N$ lần in. Sai số không. Nếu bạn đã chạy bước bỏ lọc, nhắc chùm bạn thấy, như một đối chiếu.
4. Sơ đồ trạng thái. Ba trạng thái, mũi tên 300 ms vào FAULT, duty 0 được đánh trên IDLE và trên FAULT. Câu "PWM bằng không trong FAULT" xuất hiện trong sổ và khớp `apply`.
5. Ngôn ngữ và vòng lặp. Nêu C++ hoặc MicroPython, và xác nhận đường điều khiển không gọi `delay` hay `sleep` dài hơn vài mili giây. Trích hằng timeout từ file.
6. Biên giới motor. Viết "không có motor trên GPIO, VM chưa nối, bánh nhấc lên khi sau này thêm driver." Nếu bạn chưa có driver, câu đó vẫn bắt buộc. Mua thì là module TB6612 giá 45000₫, VM khoảng 4,5 V đến 10 V, khoảng 1,2 A liên tục, từ [trang hshop TB6612](https://hshop.vn/mach-dieu-khien-dong-co-dc-tb6612fng-dc-motor-driver), và nó không thuộc dây hôm nay.

Board chưa về không phải mục 6. Nếu phần cứng trễ, mục 1–3 còn mở. Mục 4 và 5 có thể phác từ mã bạn đã thực sự biên dịch hoặc đã kiểm cú pháp, và chúng giữ nhãn "chỉ mã nguồn" cho tới khi LED đã làm được chúng.

## Bài tập

1. Soi sketch trong ví dụ như thể bạn là người chấm. Liệt kê các mục checklist nó trượt, và trích dòng làm câu "PWM bằng không trong FAULT" thành sai.
2. Sơ đồ của một bạn có IDLE, TELEOP và FAULT, nhưng mũi tên im lặng vẽ từ IDLE sang FAULT và ghi "1 s." Mũi tên sai ở chỗ nào về việc ai được phép hết giờ, và về hằng số của bài 5?
3. Log chống dội nói bạn nhấn 10 lần và dòng cuối là `presses=12`. Cổng đã khép chưa? Thay đổi mã nào của bài 4 là chỗ bạn nhìn trước?
4. `setup` ghi duty 200, và nhánh FAULT chỉ gán biến `duty = 0` mà không gọi `ledcWrite`. Sau 300 ms im lặng, trên chân là gì, và dòng nào phải chuyển vào `apply`?

<details>
<summary>Gợi ý</summary>

1. Nó trượt log nút, chứng cứ PWM nhiều mức, duty không, số chống dội, và sơ đồ trạng thái. `ledcWrite(PIN, 180)` trong `setup`, không có lần ghi 0 về sau, là câu sai. `delay(1000)` là vòng bị chặn.
2. Im lặng được xét trong TELEOP, không phải trong IDLE. IDLE vốn đã duty 0. Hằng số là 300 ms, không phải 1 s.
3. Cổng còn mở vì $e = 2$, không phải 0. Nhìn trước vào phép thử đứng yên 20 ms quanh lệnh tăng, và vào việc một ngắt CHANGE có đang đếm cả cú nhả hay không.
4. Chân tiếp tục phát xung ở duty 200. `apply` phải gọi `ledcWrite` với 0 mỗi khi mode là FAULT hoặc IDLE, ở mọi vòng.

</details>

## Đọc thêm

- [`millis()`](https://www.arduino.cc/reference/en/language/functions/time/millis/) là hàm bạn chờ thấy trong bất kỳ sketch nào khẳng định mũi tên 300 ms là thật.
- [LEDC trên Arduino ESP32](https://docs.espressif.com/projects/arduino-esp32/en/latest/api/ledc.html) là cách kiểm một lần ghi duty trong file nộp có khớp độ phân giải tác giả đã gắn hay không.
- [micro-ROS](https://micro.ros.org/) sẽ ngồi trên một ảnh firmware đã qua danh sách này. Nó không thay lần ghi duty 0 của FAULT.
