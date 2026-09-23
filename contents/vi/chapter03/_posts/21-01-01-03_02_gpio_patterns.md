---
layout: post
title: "Lab — mẫu GPIO cho nút nhấn và LED"
chapter: "03"
order: 2
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter03
lesson_type: required
draft: false
---

## Mục tiêu

Hết bài lab này, nút đấu từ GPIO xuống mass đọc mức cao khi nhả và mức thấp khi nhấn, vì chế độ chân là `INPUT_PULLUP` hoặc tương đương MicroPython. Bạn tính điện trở nối tiếp của LED trên rail 3,3 V, viết cùng một sketch chỉ in cạnh lên và cạnh xuống bằng Arduino C++ và bằng MicroPython, và chỉ chấp nhận đổi mức sau khi mẫu thô đã đứng yên 20 ms. Bạn nhận ra ba lỗi quen: chân nổi khi quên kéo lên, LED không có điện trở, và nút mắc giữa 3,3 V với chân mà không có kéo xuống nên lúc nào cũng đọc cao. Không sketch nào trong bài cấp điện cho động cơ.

## Kiến thức cần có

[Nhịp tim chương 02]({% multilang_post_url contents/chapter02/02_04_blink_serial_hello %}) đã chứng minh monitor serial khớp board ở 115200, và bạn đổi được chân LED khi GPIO 2 không phải đèn trên board của mình. Bài 1 chương này đã thay `delay(500)` bằng đồng hồ không chặn; các sketch dưới đây giữ thói quen đó. Bạn cần breadboard, một nút nhấn tức thời, một LED, điện trở gần 180 Ω, và dây nhảy. Chưa cần TB6612, pin, hay khung xe.

## Vì sao bài này quan trọng

Capstone A sẽ coi nút là một sự kiện của người: xóa lỗi, hoặc xác nhận rằng bạn muốn rời trạng thái dừng. Lệnh teleop sẽ tới sau dưới dạng byte rồi dưới dạng bản tin ROS, nhưng kiểu đấu dây dưới nút không đổi khi những byte đó xuất hiện. Chân nổi thì firmware bịa ra các lần nhấn và có thể xóa một lỗi bạn chưa thừa nhận. Nếu LED đang đóng vai câu "tôi đã thấy cạnh," thiếu điện trở nối tiếp biến vai đó thành một mối nối tắt. Bánh ở trên không, và động cơ không được móc vào GPIO, vì mạch cấp bánh là một chip khác. Bài này chỉ có ngõ vào và bóng đèn.

## Nội dung

GPIO là chân số, hoặc vào hoặc ra. Khi là ngõ vào và kéo lên nội được bật, chân bị kéo yếu lên 3,3 V. Đầu kia của nút đi xuống mass, không đi lên 3,3 V. Nút nhả thì tiếp điểm hở, điện trở kéo lên thắng, `digitalRead` trả về HIGH. Nút nhấn thì tiếp điểm là một mối nối mass, mạnh hơn kéo lên, và lần đọc trả về LOW. Sự đảo đó hay làm người mới bất ngờ, vì họ chờ "nhấn nghĩa là đúng nghĩa là cao." Với cách đấu này, nhấn nghĩa là thấp. Hãy viết comment trong sketch để lần sau bạn không "sửa" lại.

![Nút xuống mass, GPIO kéo lên]({{ site.imgurl }}/generated/gpio_pullup_button.png)

Nếu chip không có kéo lên nội, chép cùng ý ấy bằng điện trở 10 kΩ từ GPIO lên 3,3 V, và vẫn đấu nút từ GPIO xuống mass. Mười kilohm đủ cứng để ngón tay chạm dây không quyết định mức, và đủ dịu để khi nhấn nút chỉ phải hút $3{,}3 / 10000 = 0{,}33$ mA.

LED cần điện trở nối tiếp riêng. Một LED chỉ thị nhỏ rơi khoảng 2,0 V khi sáng, và 8 mA là mục tiêu sáng, an toàn, từ GPIO 3,3 V. Định luật Ohm trên điện trở, phần nhìn điện áp còn lại, là

$$
R = \frac{V_{CC} - V_F}{I_F} = \frac{3{,}3 - 2{,}0}{0{,}008} = 162{,}5\,\Omega.
$$

Món hay gặp trong bộ 1/4 W là 180 Ω, chạy LED thấp hơn mục tiêu một chút:

$$
I = \frac{3{,}3 - 2{,}0}{180} \approx 7{,}2\,\mathrm{mA}, \qquad P = I^2 R \approx 9\,\mathrm{mW}.
$$

Điện trở 1/4 W không hề ấm. Món 220 Ω cũng được, chỉ tối hơn chút. Bỏ điện trở là bắt GPIO tự giới hạn dòng. Nó không làm việc đó lịch sự: cái hỏng là LED hoặc đệm chân. Cathode LED đi về mass, anode về phía điện trở, điện trở về phía GPIO. GPIO là nguồn dòng. Ở trên rail 3,3 V. Chân ESP32 không phải chỗ để mắc chân 5 V, và cũng không phải chỗ để mắc động cơ.

![LED, điện trở nối tiếp, và mass]({{ site.imgurl }}/generated/led_series_resistor.png)

Tiếp điểm không đóng bằng một cạnh sạch. Bài sau sẽ nhìn sự nảy đó. Hôm nay bạn chỉ cần một luật trong vòng lặp: chưa tin một thay đổi cho tới khi bit thô đứng yên 20 ms. Giữ mẫu thô cuối và thời điểm nó đổi. Nếu giá trị thô mới, khởi động lại đồng hồ. Nếu giá trị thô đã tự khớp trong 20 ms và khác mức đã chấp nhận, thì chấp nhận và in một dòng. In mọi mẫu sẽ làm ngập monitor và giấu cạnh bạn cần. Log serial nên nói `press` ở cạnh xuống đã chấp nhận và `release` ở cạnh lên đã chấp nhận, mỗi cạnh một lần.

Cùng luật ấy là phần chống dội bạn sẽ dùng lại khi một ngắt chỉ đặt cờ. Làm trong vòng lặp lúc này để bạn lần được bằng một dòng in. Đừng `delay(20)` để thực hiện nó. Một khoảng chờ chặn đóng băng nhịp tim bài 1 suốt cửa sổ nảy, và khi đã có lệnh động cơ thì khoảng chờ đó lại là chuyện 200 ms, chỉ ngắn hơn. Hai mươi mili giây mù vẫn là hình sai. Phép thử mốc thời gian để vòng lặp được rảnh.

Ba lỗi xuất hiện mỗi khóa.

Chân nổi là cái bạn gặp khi nút xuống mass mà quên `INPUT_PULLUP` hoặc `Pin.PULL_UP`. Lúc nhả, sợi dây là anten. Monitor in press và release dù không ai chạm. Sửa chế độ chân trước khi viết lại phần chống dội.

LED không điện trở nối tiếp có thể sáng một lần, rất gắt, rồi không sáng nữa. Nếu nó sống sót, chân vẫn bị đòi dòng quá định mức đệm. Hãy đặt món 180 Ω nối tiếp dù đèn "trông vẫn ổn."

Nút đấu từ 3,3 V vào GPIO, kéo lên vẫn bật và không có kéo xuống mass, đọc HIGH khi nhả vì điện trở kéo lên và HIGH khi nhấn vì tiếp điểm nối 3,3 V. Không có cạnh. Sinh viên mô tả là "nút không làm gì." Chân không hỏng. Hai trạng thái cùng một điện áp. Chuyển tiếp điểm xuống mass, hoặc thêm kéo xuống và ngừng dùng kéo lên nội. Môn này dùng cách đấu xuống mass.

Đừng cấp động cơ, cuộn rơ-le, hay chân VM của TB6612 từ một GPIO. GPIO có thể ra tín hiệu PWM cho ngõ vào driver sau này. Nó không phải dòng của động cơ.

Arduino C++ cho ESP32. Nút ở GPIO 4, LED ở GPIO 18. Cả hai chân tránh nhóm chân strap sẽ nói ở bài PWM.

```cpp
const int BTN = 4;
const int LED = 18;
const uint32_t DEBOUNCE_MS = 20;

int lastRaw = HIGH;
int stable = HIGH;
uint32_t lastChange = 0;

void setup() {
  pinMode(BTN, INPUT_PULLUP);  // nhả thì cao, nhấn thì thấp
  pinMode(LED, OUTPUT);
  Serial.begin(115200);
  lastChange = millis();
  Serial.println("gpio edges");
}

void loop() {
  uint32_t now = millis();
  int raw = digitalRead(BTN);
  if (raw != lastRaw) {
    lastRaw = raw;
    lastChange = now;
  }
  if ((now - lastChange) >= DEBOUNCE_MS && raw != stable) {
    stable = raw;
    digitalWrite(LED, stable == LOW ? HIGH : LOW);  // LED sáng khi đang giữ
    Serial.println(stable == LOW ? "press" : "release");
  }
}
```

LED trong listing đi theo trạng thái giữ để bạn nhìn thấy nút. Dòng in chỉ xảy ra ở cạnh đã chấp nhận.

MicroPython, cùng số chân nếu bạn đang ở board ESP32. Trên Pico, chuyển số sang các GP còn trống và giữ kéo lên.

```python
from machine import Pin
import time

btn = Pin(4, Pin.IN, Pin.PULL_UP)
led = Pin(18, Pin.OUT)
DEBOUNCE_MS = 20

last_raw = btn.value()
stable = last_raw
last_change = time.ticks_ms()
print("gpio edges")

while True:
    now = time.ticks_ms()
    raw = btn.value()
    if raw != last_raw:
        last_raw = raw
        last_change = now
    if time.ticks_diff(now, last_change) >= DEBOUNCE_MS and raw != stable:
        stable = raw
        led.value(1 if stable == 0 else 0)
        print("press" if stable == 0 else "release")
    time.sleep_ms(1)
```

## Ví dụ tính tay

Bạn nhấn nút lúc $t = 1000$ ms và nhả lúc $t = 1600$ ms. Chân thô nảy 8 ms sau mỗi sự kiện cơ khí rồi đứng yên. Luật 20 ms đợi tới $t = 1020$ ms mới chấp nhận LOW, in `press`, và bật LED. Nó đợi tới $t = 1620$ ms mới chấp nhận HIGH, in `release`, và tắt LED. Các mẫu cách 1 ms không xuất hiện trong log. Monitor hiện

```
gpio edges
press
release
```

và không có gì khác cho cử chỉ đó. Nếu log của bạn hiện hàng chục dòng cho một cú nhấn, phép thử đứng yên chưa bọc quanh lệnh in. Nếu không hiện gì, hãy đo chân: nhả gần 3,3 V, nhấn gần 0 V. Chân nhả mà lang thang giữa 0,8 V và 2 V là chân nổi.

Giả sử điện áp thuận là 2,1 V và bạn muốn 5 mA từ cùng rail 3,3 V. Điện trở là

$$
R = \frac{3{,}3 - 2{,}1}{0{,}005} = 240\,\Omega,
$$

nên món 220 Ω hoặc 270 Ω trong bộ là lựa chọn thật. Dùng lại 180 Ω sẽ chạy gần $(3{,}3-2{,}1)/180 \approx 6{,}7$ mA, vẫn an toàn và sáng hơn mức bạn xin một chút. Cái cần là phép tính, không phải một mã catalog duy nhất.

## Bài lab

Cấp board từ USB. Đừng nối bộ pin, và đừng để dây chạm header 5 V.

1. Rút USB. Đặt nút sao một chân là GPIO 4 và chân đối diện là GND. Đặt LED và điện trở 180 Ω nối tiếp giữa GPIO 18 và GND, anode về phía GPIO. Đọc lại hai hình trước khi cắm USB.
2. Nạp sketch C++ hoặc lưu script MicroPython. Mở monitor serial ở 115200. Bạn muốn một dòng `gpio edges`, rồi im.
3. Nhấn và nhả một lần, chậm. Log mong đợi: `press` rồi `release`. LED chỉ sáng khi nút đang giữ. Nhấn năm lần. Bạn muốn năm cặp, không phải một dòng chảy.
4. Cố tình xóa kéo lên, chạy lại, và nhìn log bịa cạnh. Bật kéo lên lại. Thí nghiệm mười giây đó chính là lỗi chân nổi, và nó phải vào sổ.
5. Ghi số chân, trị số điện trở, và dán một cặp press/release sạch. Chụp breadboard nếu được. Checklist cuối chương hỏi đúng log này.

Nếu LED tối trong khi `press` vẫn in, LED bị ngược hoặc sai chân. Tin dòng serial trước, rồi xoay LED. Nếu `press` không bao giờ in và chân đo 3,3 V ở cả hai vị trí, bạn đã dựng lỗi luôn-cao: công tắc nằm phía 3,3 V.

## Bài tập

1. Một LED đỏ ghi $V_F = 1{,}8$ V và bạn dự trù $I_F = 6$ mA từ 3,3 V. Tính $R$, rồi nêu giá trị thông dụng gần nhất bạn sẽ hàn, chọn món không vượt 6 mA.
2. Mức ổn định đổi từ HIGH sang LOW lúc $t = 250$ ms và về HIGH lúc $t = 900$ ms, phép thử 20 ms đã thỏa. Viết các dòng serial và trạng thái LED từng khoảng. Cái gì không được xuất hiện giữa chúng?
3. Một bạn đấu nút từ 3,3 V vào GPIO 4, gọi `pinMode(4, INPUT_PULLUP)`, và báo đèn không đổi. Nêu điện áp ở cả hai vị trí công tắc, và sợi dây bạn chuyển.
4. Không có kéo lên nội. Bạn có điện trở 10 kΩ và cùng một nút. Mô tả hai nút mạch mà điện trở nối, và dòng nó chịu khi nút đang giữ.

<details>
<summary>Gợi ý</summary>

1. $R = (3{,}3 - 1{,}8) / 0{,}006 = 250\,\Omega$. Món 270 Ω nằm dưới 6 mA. Món 220 Ω chạy hơi quá ngân sách.
2. Log thêm `press` ở cạnh chấp nhận đầu và `release` ở cạnh sau. LED chỉ sáng khi mức đã chấp nhận là LOW. Các mẫu giữa 250 và 900 ms không in.
3. Cả hai vị trí nằm gần 3,3 V, nên mức chấp nhận không đổi. Chuyển đầu xa của nút từ 3,3 V xuống GND và để kéo lên vẫn bật.
4. Điện trở nối GPIO với 3,3 V. Dòng khi giữ khoảng $3{,}3/10\,\mathrm{k}\Omega = 0{,}33$ mA. Đầu kia của nút vẫn là GND.

</details>

## Đọc thêm

- [`pinMode` của Arduino](https://www.arduino.cc/reference/en/language/functions/digital-io/pinmode/) liệt kê `INPUT_PULLUP`, lý do nút nhả trong lab này đọc mức cao.
- [`machine.Pin` của MicroPython](https://docs.micropython.org/en/latest/library/machine.Pin.html) mô tả `Pin.PULL_UP` và các mức `value()` trong listing thứ hai.
- Bộ kit cả môn, nếu bạn chưa đặt board, vẫn là [danh mục chương 00]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %}). Bài này chỉ thêm các món nhỏ bên dưới.

## Linh kiện cho bài lab

Giá là giá kệ hshop đã đối chiếu cho môn này, tính bằng đồng, và có lúc đổi. Nút là loại tròn 12 mm PBS-11B kèm dây, 10000₫, tại [hshop.vn/nut-nhan-nha-tron-pbs-11b-12mm-kem-cap](https://hshop.vn/nut-nhan-nha-tron-pbs-11b-12mm-kem-cap). Nút thường hở, nhấn là đóng, hai chân, thì về điện là cùng một thứ. Bộ LED giá 20000₫ tại [hshop.vn/bo-5-loai-led-sieu-sang-3mm-thong-dung-5-kind-3mm-transparent-color-led](https://hshop.vn/bo-5-loai-led-sieu-sang-3mm-thong-dung-5-kind-3mm-transparent-color-led). LED 3 mm hay 5 mm đều chạy với phép tính 180 Ω; chỉ điện áp thuận đổi, và bạn tính lại.

Breadboard là [hshop.vn/test-board-cammb-102](https://hshop.vn/test-board-cammb-102). Dây đực-đực, 40 sợi, 20 cm, là [hshop.vn/day-cam-breadboard-duc-duc-20cm-cap-det-40-soi-m-m-jumper-wire](https://hshop.vn/day-cam-breadboard-duc-duc-20cm-cap-det-40-soi-m-m-jumper-wire). Bộ điện trở 1/4 W, chỗ món 180 Ω nằm, là một trang tìm Shopee chứ không phải một link sản phẩm đứng yên: [bộ điện trở 1/4W](https://shopee.vn/search?keyword=b%E1%BB%99%20%C4%91i%E1%BB%87n%20tr%E1%BB%9F%201%2F4W). Lấy 180 Ω hoặc 220 Ω trong bộ đó. Đừng mua động cơ cho chương này, và đừng nối động cơ bạn đã có vào một GPIO.
