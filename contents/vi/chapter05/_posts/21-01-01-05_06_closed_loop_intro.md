---
layout: post
title: "Lab: vòng kín cảm nhận → tính → tác động"
chapter: "05"
order: 6
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter05
lesson_type: required
draft: false
---

Mọi bộ điều khiển về sau trên robot này là cùng ba hộp: cảm nhận, tính, tác động. Lab này khép chúng bằng cái máy tính thô nhất mà vẫn đếm được: nếu khoảng cách nằm trong 20 cm thì PWM bánh bằng không; nếu không, một PWM tiến vừa phải được phép. Luật đó là bang-bang. PID đến ở Chương 08. Điều bạn tập bây giờ là hình an toàn mà các luật sau phải giữ: cảm biến hỏng thì dừng.

## Mục tiêu học

Hết bài, bạn vẽ được vòng cảm nhận, tính và tác động cho một cảm biến khoảng cách cùng một lệnh motor. Bạn triển khai luật bang-bang ở 20 cm, với một timeout ép PWM về không. Bạn thêm một dải trễ đơn giản để motor không kêu lạch cạch ở ngưỡng. Bạn nói được subscriber ROS 2 của `/cmd_vel` sẽ ngồi ở đâu trong sơ đồ này, và cú dừng nào phải ở lại trong firmware.

## Kiến thức cần có

Bạn cần một số đọc khoảng cách từ bài siêu âm hoặc time-of-flight ở Chương 04, bằng milimét hoặc bằng centimét bạn đổi được. Bạn cần một kênh motor mà bảng chân lý tiến đã viết ở bài 05-01, trên một driver bạn gọi tên được từ bài 05-02. Bánh rời mặt đất trước khi chạm sàn. Một bia carton và một công tắc nguồn bạn với tay tắt được là một phần của dụng cụ.

## Vì sao bài này quan trọng với Capstone A và ROS

Capstone A sẽ chạy về phía vật, và quan trọng hơn, dừng trước khi đâm. Chương 07 lắp hai PWM có dấu. Chương 08 thay khối tính bật/tắt này bằng một PID giữ được tốc độ hoặc hướng. Khối cảm nhận và khối tác động ở lại. Khi ROS 2 được đưa vào, một subscriber của `/cmd_vel` là một cách khác để điền khối tính: một tiến trình khác đề xuất một twist, và node của bạn biến nó thành PWM trái và phải. Cú dừng theo khoảng cách không dời ra topic đó. Firmware vẫn sở hữu cái nhìn cuối vào cảm biến. Nếu topic nói “tiến” mà khoảng cách nói “quá gần” hoặc “tôi không biết”, bánh dừng. Một planner im lặng không được hiểu là hành lang trống.

## Bang-bang, trong một câu

Đọc khoảng cách. Nếu dưới 20 cm, lệnh PWM 0. Nếu rõ ràng xa hơn, lệnh PWM 80 theo chiều tiến trong bảng chân lý của bạn. Tám mươi trên thang 8 bit là một cú bò chậm, đúng thứ bạn muốn khi tay vẫn là bia.

$$
\mathrm{PWM} =
\begin{cases}
0 & \text{nếu khoảng cách} < 20~\mathrm{cm} \\
80 & \text{còn lại, khi số đọc hợp lệ}
\end{cases}
$$

Chữ “otherwise” là chữ nguy hiểm. Một cảm biến timeout, trả về một sentinel cực đại, hoặc trả về 0 vì tiếng vọng không bao giờ về, không phải một “otherwise” hợp lệ. Những số đọc đó đi nhánh dừng. Cảm biến hỏng không được có nghĩa “đường trống, hết ga”.

Dải trễ giữ trục khỏi kêu khi bạn giữ tay gần 20 cm. Dừng khi khoảng cách xuống dưới 20 cm. Ở dừng cho đến khi khoảng cách lên trên 25 cm. Giữa hai số đó, giữ lệnh trước. Motor khi ấy đổi trạng thái ít hơn một chút, và hộp số hết kêu ở biên.

## Ba hộp nằm ở đâu trong code

Cảm nhận là hàm bạn đã tin từ Chương 04, bọc lại sao cho timeout trở về một số âm hoặc một cờ không hợp lệ tường minh. Tính là khối `if` bên dưới. Tác động là cặp chân hướng cộng một lần ghi PWM. Đặt số chân vào các hằng có tên ở đầu, để bài viết lab nói được GPIO nào đã cử động.

```cpp
const int PIN_IN1  = 25;   // sửa thành cặp tiến của bạn
const int PIN_IN2  = 26;
const int PIN_PWM  = 27;
const int PIN_TRIG = 5;    // siêu âm; bỏ qua nếu dùng ToF
const int PIN_ECHO = 18;

const int PWM_FORWARD = 80;
const int STOP_MM = 200;   // 20 cm
const int GO_MM   = 250;   // 25 cm, nhả trễ

void setup() {
  pinMode(PIN_IN1, OUTPUT);
  pinMode(PIN_IN2, OUTPUT);
  pinMode(PIN_PWM, OUTPUT);
  digitalWrite(PIN_IN1, HIGH);   // tiến, theo bảng chân lý CỦA BẠN
  digitalWrite(PIN_IN2, LOW);
  analogWrite(PIN_PWM, 0);       // tác động an toàn, trước mọi lần đọc cảm biến
}

void loop() {
  int mm = readRangeMm();        // Chương 04; âm nghĩa là timeout / không hợp lệ
  if (mm < 0 || mm <= STOP_MM) {
    analogWrite(PIN_PWM, 0);
  } else if (mm >= GO_MM) {
    analogWrite(PIN_PWM, PWM_FORWARD);
  }
  // giữa 200 và 250 mm, giữ PWM trước đó
  delay(50);
}
```

`readRangeMm` là hàm bạn chuyển từ sketch siêu âm hoặc ToF của mình. Khi timeout nó trả một giá trị âm. Số 0 đúng nghĩa cũng dừng, vì $$0 \le 200$$. Hướng được đặt một lần, từ bảng chân lý, nên vòng đầu này chỉ phải quyết tốc độ. Khi sau này bạn trộn một cú lùi thoát, bạn sẽ đổi IN1 và IN2 có chủ đích, trong khối tác động, với cùng luật “không hợp lệ thì dừng” vẫn đứng trên chúng.

Quy trình bánh trên không: giơ tay trước cảm biến. Tay xa, bánh quay tiến chậm. Tay trong khoảng 20 cm, bánh dừng. Che cảm biến hoặc rút dây echo một lát và xác nhận bánh dừng, vì lần đọc đã hỏng. Chỉ sau đó bạn mới đặt robot xuống sàn, chĩa vào carton, và giữ tay trên công tắc cắt nguồn motor. Lượt chạy sàn thì ngắn. Bạn đang kiểm cú dừng, không phải đua hành lang.

## Ví dụ tính

Ngưỡng: dừng ở 200 mm, đi từ 250 mm trở lên.

Số đọc 180 mm nằm dưới 200 mm, nên PWM thành 0. Số đọc 900 mm là hành lang trống, nên PWM thành 80 tiến. Số đọc 0, hoặc timeout trả về −1, đi nhánh dừng dù 0 là “ít khoảng cách” và timeout là “không có khoảng cách”. Khối tính từ chối coi cả hai là giấy phép để chạy.

Đi dải trễ. Tay tiến lại: 400 mm (tiến), 260 mm (vẫn tiến, vì 260 trên 250), 220 mm (giữ tiến, nằm trong dải), 180 mm (dừng). Tay lùi ra: 220 mm (ở dừng, nằm trong dải), 260 mm (tiến lại). Không có dải, nhiễu cảm biến 190 mm và 210 mm sẽ kêu hộp số mỗi vòng lặp.

## Hình

![Cảm nhận, tính, tác động: số đọc khoảng cách vào, một quyết định được đưa, một lệnh motor ra]({{ site.imgurl }}/generated/sense_compute_act.png)

Gắn nhãn các hộp bằng danh từ của bạn: siêu âm hoặc ToF, khối `if` bang-bang, và PWM của cầu H. Vẽ một mũi tên thứ hai vào khối tính và viết `/cmd_vel` lên đó, rồi vẽ cú dừng vẫn ngồi trong firmware sau mũi tên ấy.

## Lab

### An toàn

Buổi đầu: khung trên giá, bánh trên không, giới hạn dòng hoặc cầu chì đã có, USB chỉ trên vi điều khiển. Buổi sau: lượt sàn ngắn về phía carton, một người, tay trên công tắc cắt nguồn motor. Giữ PWM ở 80, không phải 255. Nếu dòng cảm biến dừng, bánh phải đã dừng nhờ nhánh timeout của bạn. Đừng “sửa” timeout bằng cách comment nhánh đó đi.

### BOM

| Món | Vai trò |
|------|------|
| Vi điều khiển cộng cảm biến khoảng cách từ Chương 04 | Cảm nhận |
| Một motor và driver đã nhận diện | Tác động |
| Pin hoặc nguồn có giới hạn cho VM, mass chung | Nguồn motor |
| Bia carton | Một mặt cảm biến nhìn thấy |
| Công tắc nguồn với tới được | Cầu chì bằng tay người |
| Sổ | Ba số đọc thử và bài timeout |

### Các bước

1. Đối chiếu `readRangeMm` với thước ở khoảng 20 cm và khoảng 50 cm trước khi enable motor. Sửa cảm biến trước.
2. Nhập các hằng và `loop` ở trên. Đặt hướng từ bảng chân lý của bạn. PWM ở 0 cho đến số đọc xa hợp lệ đầu tiên.
3. Bánh trên không. Đưa tay khoảng 40 cm, rồi 15 cm, rồi che cảm biến. Ghi hành vi PWM cho mỗi trường hợp.
4. Lượt sàn tùy chọn: carton ở cuối một làn ngắn, tay trên công tắc, PWM 80. Robot phải bò và dừng gần 20 cm. Nếu nó không dừng, cắt nguồn. Đừng tăng PWM.
5. Viết câu chuyện dải trễ trong hai dòng: khoảng cách nó dừng, và khoảng cách nó chạy lại.

### Kết quả mong đợi

Một ghi chú với ba trường hợp (xa → tiến, gần → dừng, timeout hoặc 0 → dừng) và, nếu bạn đã chạy sàn, khoảng cách dừng xấp xỉ. Một câu gọi `/cmd_vel` là ngõ vào tính trong tương lai, và ngõ vào đó không được quyền ghi đè cú dừng này.

### Lỗi thường gặp

| Bạn thấy | Cần kiểm |
|--------------|----------------|
| Bánh chạy khi cảm biến bị rút | Timeout đang rơi xuống nhánh tiến. Trả một mã âm và kiểm `mm < 0`. |
| Bánh kêu ở biên | Ngưỡng đi và ngưỡng dừng bằng nhau. Tách chúng (200 mm và 250 mm). |
| Bánh chạy lùi | IN1 và IN2 không khớp dòng tiến của bảng chân lý. |
| Robot không bao giờ khởi động | Mọi số đọc nằm trong dải dừng, bia quá gần, hoặc STBY / enable đang thấp. |
| Lượt sàn không dừng | Sai đơn vị (cm đem so với 200), hoặc cảm biến chĩa qua carton. Cắt nguồn. |

## Mua ở Việt Nam / Where to buy in Vietnam

Lab này dùng cảm biến và driver bạn đã có. Chỉ mua chỗ thiếu: một TB6612 hoặc L298N nếu bài 05-02 vẫn thiếu board, một motor TT nếu bạn không có trục để nhìn, một HC-SR04 hoặc một ToF nhỏ nếu Chương 04 làm trên bàn bạn học. Giá chạy. Khoảng thô: HC-SR04 khoảng 15.000–35.000 VND, motor TT khoảng 25.000–45.000 VND, module L298N khoảng 35.000–70.000 VND.

- Trang L298N đã kiểm, khoảng 45.000 VND: [hshop.vn/mach-dieu-khien-dong-co-dc-l298](https://hshop.vn/mach-dieu-khien-dong-co-dc-l298)
- HShop: [HC-SR04](https://hshop.vn/search?q=HC-SR04), [TB6612](https://hshop.vn/search?q=TB6612), [motor TT](https://hshop.vn/search?q=motor%20TT)
- Shopee: [HC-SR04](https://shopee.vn/search?keyword=HC-SR04), [TB6612](https://shopee.vn/search?keyword=TB6612)
- Lazada: [HC-SR04](https://www.lazada.vn/catalog/?q=HC-SR04), [VL53L0X](https://www.lazada.vn/catalog/?q=VL53L0X)
- Thế Giới IC: [HC-SR04](https://www.thegioiic.com/search?q=HC-SR04), [L298N](https://www.thegioiic.com/search?q=L298N)

## Bài tập

1. Khoảng cách đọc 180 mm, rồi 900 mm, rồi một timeout. Bạn lệnh PWM bao nhiêu trong mỗi trường hợp nếu dừng là 200 mm và đi là 250 mm?
2. Vì sao số đọc 0 đi nhánh dừng?
3. Bánh kêu bật tắt khi tay giữ yên gần 20 cm. Hai hằng nào bạn phải tách?
4. Một bản tin `/cmd_vel` nói tiến đúng lúc khoảng cách là 12 cm. Firmware làm gì?
5. PID là Chương 08. Khối tính bạn giao hôm nay là gì, trong một câu?

### Gợi ý đáp án

180 mm thì dừng, 900 mm lệnh PWM 80 tiến, và timeout thì dừng. Số đọc 0 là không hợp lệ hoặc nằm trong ngưỡng dừng, nên không được tính là đường trống. Tách ngưỡng dừng và ngưỡng đi, ví dụ 200 mm và 250 mm, và giữ lệnh trước trong dải. Firmware dừng trên số đọc 12 cm dù `/cmd_vel` nói tiến. Khối tính hôm nay là bang-bang: PWM 0 khi khoảng cách dưới 20 cm hoặc cảm biến đã hỏng, và PWM 80 tiến khi khoảng cách hợp lệ và đã qua điểm nhả của dải trễ.

## Đọc thêm

- Control Guru, điều khiển on/off và ngõ ra đáp lại khi phép đo vượt setpoint: [https://controlguru.com/the-on-off-controller-output-response-to-set-point-changes/](https://controlguru.com/the-on-off-controller-output-response-to-set-point-changes/)
- Topic ROS 2, đường ống mà subscriber `/cmd_vel` về sau sẽ nghe. Bản thân `geometry_msgs/Twist` được giới thiệu ở Chương 09: [https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Topics/Understanding-ROS2-Topics.html](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Topics/Understanding-ROS2-Topics.html)
