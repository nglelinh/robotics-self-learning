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

Mọi bộ điều khiển robot về sau đều tuân theo chung một vòng lặp ba khối: **cảm nhận** (sense), **tính toán** (compute) và **tác động** (act). Bài thực hành này khép kín vòng lặp đó bằng luật điều khiển đơn giản nhất (điều khiển bật/tắt hay bang-bang): nếu khoảng cách nhỏ hơn 20 cm thì đưa PWM bánh xe về 0, ngược lại cho phép chạy tiến ở mức PWM vừa phải. Bộ điều khiển PID sẽ học ở Chương 08; trọng tâm của bài hôm nay là thiết lập nguyên tắc an toàn bắt buộc cho mọi luật điều khiển sau này: **cảm biến lỗi hoặc mất tín hiệu thì phải dừng**.

Nếu bạn đặt hai bánh xe robot cùng một mức PWM 60% và thả chạy thẳng trên hành lang, chuyện gì sẽ xảy ra? Chỉ sau 2 mét, robot sẽ lượn cong sang một bên! Lý do rất đời thường: không có hai động cơ nào giống hệt nhau 100% về ma sát, điện áp pin giảm dần mỗi phút, và mặt sàn chỗ trơn chỗ nhám. **Điều khiển vòng kín (closed-loop control)** biến một cỗ máy "mù" chạy theo lệnh cố định thành một hệ thống biết tự sửa sai liên tục qua chu trình 3 bước kinh điển: **Cảm nhận (Sense) → Tính sai số (Compute) → Tác động (Act)**.

## Bản đồ kiến thức nền: Vòng hở vs. Vòng kín và Tư duy phản hồi âm

### 1. Hạn chế cố hữu của vòng hở (Open-Loop)
Trong hệ vòng hở, lệnh điều khiển $$u$$ chỉ phụ thuộc vào mục tiêu $$r$$ mà không hề nhìn xem đầu ra thực tế $$y$$ đang ở đâu. Bất kỳ **nhiễu loạn ngoài (disturbance)** nào — như robot leo lên thảm dày, chở thêm tải, hay pin tụt từ 8,4 V xuống 7,2 V — đều truyền thẳng 100% thành sai số đầu ra.

### 2. Phản hồi âm (Negative Feedback) và sức mạnh khử nhiễu
Hệ vòng kín đo đầu ra thực tế $$y$$ (ví dụ vận tốc bánh từ encoder), tính sai số $$e = r - y$$, rồi điều chỉnh lệnh tác động $$u = K_p e$$ ngược chiều sai số: nếu bánh chạy chậm hơn mục tiêu ($$e > 0$$), tăng PWM lên; nếu chạy lố ($$e < 0$$), giảm PWM xuống. Chính cơ chế phản hồi âm này tự động nén ảnh hưởng của nhiễu loạn và sai lệch phần cứng xuống $$(1 + K_p)$$ lần!

### 3. Độ trễ lấy mẫu và ranh giới mất ổn định
Phản hồi âm không thể vặn hệ số $$K_p$$ lớn vô hạn. Vì mọi vòng điều khiển số đều có chu kỳ lấy mẫu $$\Delta t$$ và quán tính cơ khí, tăng $$K_p$$ quá cao sẽ khiến robot liên tục sửa "quá tay" sang trái rồi lại quá tay sang phải — sinh ra **dao động (oscillation)** hoặc mất ổn định. Đây chính là tiền đề dẫn tới bộ điều khiển PID ở Chương 08.

### Khung giải thích: Cầm tay chứng minh phản hồi âm nén sai số nhiễu loạn giảm đi 5 lần (nên đọc chậm)

Xét một bánh xe robot có mô hình tĩnh đơn giản: ở trạng thái xác lập, tốc độ bánh bằng lệnh điều khiển cộng với nhiễu tải (ví dụ khi leo lên thảm dày làm hụt tốc độ $$d = -0{,}30\text{ m/s}$$):
$$v = u + d, \qquad \text{mục tiêu } v^* = 1{,}00\text{ m/s}.$$

1. **Trường hợp 1 — Điều khiển vòng hở (Open-Loop):**
   Ta đặt cứng lệnh $$u = v^* = 1{,}00$$. Khi gặp thảm dày ($$d = -0{,}30$$):
   $$v_{\text{hở}} = 1{,}00 - 0{,}30 = 0{,}70\text{ m/s} \implies \text{Sai số } e_{\text{hở}} = 1{,}00 - 0{,}70 = 0{,}30\text{ m/s}\;(30\%!).$$

2. **Trường hợp 2 — Điều khiển vòng kín tỷ lệ với $$u = u_{\text{ff}} + K_p(v^* - v)$$ (đặt $$u_{\text{ff}} = 1{,}00$$, độ lợi $$K_p = 4$$):**
   Thay vào phương trình $$v = u_{\text{ff}} + K_p(v^* - v) + d$$:
   $$v = 1{,}00 + 4(1{,}00 - v) - 0{,}30 \implies v + 4v = 4{,}70 \implies 5v = 4{,}70 \implies v_{\text{kín}} = 0{,}94\text{ m/s}!$$
   Sai số còn lại chỉ là:
   $$e_{\text{kín}} = 1{,}00 - 0{,}94 = 0{,}06\text{ m/s} = \frac{0{,}30}{1 + K_p} = \frac{0{,}30}{5}!$$

Không cần biết trước tấm thảm dày bao nhiêu hay pin yếu đi mấy volt, chỉ riêng một vòng phản hồi tỷ lệ với $$K_p = 4$$ đã tự động nén sai số tốc độ từ **30% xuống còn 6%** (giảm đúng **5 lần**) — và đó mới chỉ là khởi đầu trước khi ta thêm thành phần tích phân (I) để kéo sai số về đúng $$0$$!

## Mục tiêu học

Sau bài này, bạn vẽ được sơ đồ vòng kín cảm nhận–tính–tác động nối cảm biến khoảng cách với lệnh điều khiển động cơ. Bạn triển khai được luật bang-bang tại ngưỡng 20 cm có xử lý timeout ép PWM về 0, đồng thời bổ sung vùng trễ (hysteresis) để động cơ không đóng ngắt liên tục quanh ngưỡng. Bạn cũng xác định được vị trí của subscriber ROS 2 `/cmd_vel` trên sơ đồ và giải thích vì sao cơ chế dừng an toàn vẫn phải giữ lại ở tầng firmware.

## Kiến thức cần có

Bạn cần hàm đọc khoảng cách đã kiểm chứng từ Chương 04 (siêu âm hoặc ToF, quy đổi sang milimét hoặc centimét), một kênh động cơ có bảng chân lý rõ ràng từ bài 05-01 trên mạch cầu H đã nhận diện ở bài 05-02. Luôn thử nghiệm với bánh nhấc khỏi mặt bàn trước khi hạ xuống sàn; chuẩn bị sẵn một tấm bìa carton và công tắc cắt nguồn động cơ trong tầm tay.

## Vì sao bài này quan trọng với Capstone A và ROS

Capstone A cần vừa tiến về phía trước vừa dừng lại kịp thời trước vật cản. Sang Chương 07 ta mở rộng ra hai kênh PWM có dấu, và sang Chương 08 ta thay khối tính bật/tắt bằng PID để giữ tốc độ hoặc hướng, nhưng cấu trúc cảm nhận và tác động giữ nguyên. Khi tích hợp ROS 2, một subscriber lắng nghe `/cmd_vel` sẽ cung cấp vận tốc mong muốn cho khối tính, nhưng quyền ngắt khẩn cấp theo cảm biến vẫn phải thuộc về firmware: nếu `/cmd_vel` yêu cầu đi tới trong khi cảm biến báo quá gần hoặc mất dữ liệu, bánh xe vẫn bắt buộc dừng.

## Luật điều khiển bang-bang và vùng trễ

Ở mức cơ bản nhất, nếu khoảng cách nhỏ hơn 20 cm thì xuất `PWM = 0`; nếu lớn hơn rõ rệt và số đọc hợp lệ thì xuất `PWM = 80` (thang 8-bit, tốc độ chậm an toàn) theo chiều tiến đã ghi trong bảng chân lý:

$$
\mathrm{PWM} =
\begin{cases}
0 & \text{nếu khoảng cách} < 20~\mathrm{cm} \\
80 & \text{còn lại, khi số đọc hợp lệ}
\end{cases}
$$

Điều kiện "khi số đọc hợp lệ" cực kỳ quan trọng: nếu cảm biến bị timeout, trả về giá trị lỗi hoặc trả về 0 do mất sóng phản hồi, hệ thống bắt buộc rẽ vào nhánh dừng. Tuyệt đối không để lỗi cảm biến bị hiểu nhầm là "đường trống".

Để tránh hiện tượng động cơ đóng ngắt lạch cạch khi vật cản đứng sát mốc 20 cm (nhiễu dao động quanh 19–21 cm), ta thêm một **vùng trễ (hysteresis)**: dừng khi khoảng cách xuống dưới 20 cm (200 mm) và chỉ cho chạy lại khi khoảng cách vượt trên 25 cm (250 mm); trong khoảng từ 200 mm đến 250 mm, giữ nguyên trạng thái PWM hiện tại.

## Cấu trúc ba khối trong mã nguồn

Khối **cảm nhận** là hàm `readRangeMm()` từ Chương 04 được bọc lại để trả về số âm khi timeout hoặc lỗi; khối **tính** là cấu trúc điều kiện `if`/`else if`; khối **tác động** điều khiển các chân hướng và PWM.

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

Khi `readRangeMm()` timeout, giá trị âm làm điều kiện `mm < 0` đúng và ép PWM về 0; giá trị 0 cũng thỏa $$0 \le 200$$ nên lập tức dừng.

Quy trình kiểm thử: đặt xe trên giá (bánh nhấc khỏi bàn), đưa tay ra xa để thấy bánh quay chậm, đưa tay vào trong 20 cm để thấy bánh dừng, sau đó che kín cảm biến hoặc rút tạm dây Echo để xác nhận bánh tự dừng khi mất tín hiệu. Chỉ sau khi vượt qua bài thử này mới đặt robot xuống sàn hướng về tấm bìa carton (chạy đoạn ngắn, tay sẵn sàng trên công tắc nguồn động cơ).

## Ví dụ minh họa vùng trễ

Với ngưỡng dừng 200 mm và ngưỡng chạy lại 250 mm:
- Đọc được 180 mm (< 200 mm) $\rightarrow$ `PWM = 0`.
- Đọc được 900 mm ($\ge 250$ mm) $\rightarrow$ `PWM = 80` (tiến).
- Đọc được 0 hoặc timeout ($-1$) $\rightarrow$ `PWM = 0` (dừng an toàn).

Theo dõi chuỗi tiến lại gần rồi lùi ra xa:
- Tay tiến lại: 400 mm (tiến) $\rightarrow$ 260 mm (vẫn tiến) $\rightarrow$ 220 mm (trong vùng trễ, giữ tiến) $\rightarrow$ 180 mm (dừng).
- Tay lùi ra: 220 mm (trong vùng trễ, vẫn dừng) $\rightarrow$ 260 mm (chạy tiến trở lại).

Nhờ khoảng đệm 50 mm này, nhiễu đo quanh mốc 200 mm (chẳng hạn nhảy giữa 190 mm và 210 mm) không còn làm hộp số bật tắt liên tục.

## Hình minh họa

![Cảm nhận, tính, tác động: số đọc khoảng cách vào, một quyết định được đưa, một lệnh motor ra]({{ site.imgurl }}/generated/sense_compute_act.png)

Đối chiếu ba khối với phần cứng của bạn: cảm biến siêu âm/ToF $\rightarrow$ khối điều kiện bang-bang $\rightarrow$ PWM cầu H. Khi bổ sung `/cmd_vel` từ ROS vào khối tính về sau, nhánh dừng khẩn cấp theo cảm biến vẫn phải nằm chặn phía sau trong firmware.

## Lab

### An toàn

Giai đoạn 1: kê khung xe để bánh quay tự do trên không, có giới hạn dòng hoặc cầu chì, USB chỉ cấp cho vi điều khiển. Giai đoạn 2 *(tùy chọn)*: chạy thử đoạn ngắn trên sàn hướng về tấm bìa carton, giữ `PWM = 80` (không đặt 255) và để tay sẵn trên công tắc nguồn động cơ. Không được bỏ qua nhánh kiểm tra timeout.

### BOM

| Món | Vai trò |
|------|------|
| Vi điều khiển và cảm biến khoảng cách (Chương 04) | Khối cảm nhận |
| Một động cơ và mạch cầu H đã nhận diện | Khối tác động |
| Pin hoặc nguồn có giới hạn dòng cho `VM`, mass chung | Nguồn động cơ |
| Tấm bìa carton | Vật cản thử nghiệm |
| Công tắc nguồn trong tầm tay | Ngắt khẩn cấp bằng tay |
| Sổ tay | Ghi ba trường hợp thử và kết quả timeout |

### Các bước

1. Kiểm tra lại hàm `readRangeMm()` bằng thước tại mốc 20 cm và 50 cm trước khi bật động cơ.
2. Nạp mã nguồn trên với đúng chân hướng từ bảng chân lý của bạn, bảo đảm `PWM = 0` lúc khởi động.
3. Với bánh nhấc khỏi bàn, thử lần lượt ba tình huống: đưa tay ở ~40 cm, đưa tay vào ~15 cm và che cảm biến/rút dây tín hiệu để kiểm tra timeout; ghi hành vi PWM tương ứng.
4. *(Tùy chọn)* Đặt robot xuống sàn hướng về tấm bìa carton với `PWM = 80` để xác nhận xe tự dừng gần mốc 20 cm; ngắt công tắc ngay nếu xe không dừng.
5. Ghi lại cơ chế vùng trễ trong hai dòng: khoảng cách dừng (200 mm) và khoảng cách chạy lại (250 mm).

### Kết quả mong đợi

Sổ tay ghi rõ ba trường hợp (xa $\rightarrow$ tiến, gần $\rightarrow$ dừng, timeout/0 $\rightarrow$ dừng), khoảng cách dừng thực tế (nếu có chạy sàn) và câu khẳng định `/cmd_vel` về sau không được phép ghi đè lệnh dừng an toàn này.

### Lỗi thường gặp

| Hiện tượng | Cần kiểm tra |
|------------|--------------|
| Bánh vẫn quay khi rút cảm biến | Nhánh timeout bị rơi sang nhánh tiến; cần trả số âm và kiểm `mm < 0` |
| Bánh đóng ngắt lạch cạch quanh 20 cm | Ngưỡng dừng và ngưỡng chạy lại trùng nhau; tách thành 200 mm và 250 mm |
| Bánh quay lùi | `IN1`/`IN2` ngược với dòng tiến trong bảng chân lý |
| Bánh không bao giờ quay | Vật cản quá gần, mọi số đọc lỗi hoặc quên kéo cao chân `STBY`/`Enable` |
| Xe không dừng khi chạy trên sàn | Nhầm đơn vị (so sánh cm với 200 mm) hoặc cảm biến đặt lệch khỏi bìa; ngắt nguồn ngay |

## Mua ở Việt Nam

Bài thực hành tận dụng lại cảm biến từ Chương 04 và mạch cầu H từ bài 05-02; chỉ mua bổ sung món còn thiếu (giá tham khảo: HC-SR04 khoảng 15.000–35.000 VND, động cơ TT khoảng 25.000–45.000 VND, L298N khoảng 35.000–70.000 VND):

- Trang L298N đã kiểm tra, khoảng 45.000 VND: [hshop.vn/mach-dieu-khien-dong-co-dc-l298](https://hshop.vn/mach-dieu-khien-dong-co-dc-l298)
- HShop: [HC-SR04](https://hshop.vn/search?q=HC-SR04), [TB6612](https://hshop.vn/search?q=TB6612), [motor TT](https://hshop.vn/search?q=motor%20TT)
- Shopee: [HC-SR04](https://shopee.vn/search?keyword=HC-SR04), [TB6612](https://shopee.vn/search?keyword=TB6612)
- Lazada: [HC-SR04](https://www.lazada.vn/catalog/?q=HC-SR04), [VL53L0X](https://www.lazada.vn/catalog/?q=VL53L0X)
- Thế Giới IC: [HC-SR04](https://www.thegioiic.com/search?q=HC-SR04), [L298N](https://www.thegioiic.com/search?q=L298N)

## Video tham khảo

- **Xem trước:** [Control Systems Lectures - Closed Loop Control](https://www.youtube.com/watch?v=O-OqgFE9SD4) — Brian Douglas, tiếng Anh. Giới thiệu nguyên lý vòng kín (đo, so sánh với mục tiêu và hiệu chỉnh lệnh), khớp với cấu trúc bài thực hành.
- [PID Control - A brief introduction](https://www.youtube.com/watch?v=UR0hOmjaHp0) — Brian Douglas, tiếng Anh. Tổng quan về PID như bước phát triển tiếp theo của khối tính toán ở Chương 08.

## Bài tập

1. Với ngưỡng dừng 200 mm và ngưỡng chạy lại 250 mm, hệ thống xuất mức PWM nào khi cảm biến lần lượt báo 180 mm, 900 mm và timeout?
2. Vì sao giá trị đo bằng 0 phải đi vào nhánh dừng?
3. Động cơ đóng ngắt liên tục khi giữ tay quanh mốc 20 cm. Cần tách hai hằng số nào để khắc phục?
4. Một bản tin `/cmd_vel` yêu cầu đi tới đúng lúc cảm biến đo được 12 cm. Firmware phải xử lý ra sao?
5. Tóm tắt trong một câu vai trò của khối tính toán bang-bang triển khai trong bài hôm nay (trước khi học PID ở Chương 08).

### Gợi ý đáp án

1. 180 mm $\rightarrow$ `PWM = 0` (dừng); 900 mm $\rightarrow$ `PWM = 80` (tiến); timeout $\rightarrow$ `PWM = 0` (dừng).
2. Giá trị 0 hoặc biểu thị lỗi timeout hoặc khoảng cách sát bằng 0 — cả hai đều không được coi là đường trống.
3. Tách ngưỡng dừng (`STOP_MM = 200`) và ngưỡng chạy lại (`GO_MM = 250`), giữ nguyên trạng thái trong khoảng giữa.
4. Firmware bắt buộc dừng động cơ vì khoảng cách 12 cm vi phạm ngưỡng an toàn, không cho `/cmd_vel` ghi đè.
5. Khối tính bang-bang xuất `PWM = 0` khi khoảng cách dưới 20 cm hoặc cảm biến lỗi/timeout, và xuất `PWM = 80` tiến khi khoảng cách hợp lệ vượt ngưỡng nhả của vùng trễ.

## Đọc thêm

- Control Guru — điều khiển bật/tắt (on/off) và đáp ứng ngõ ra quanh điểm đặt: [https://controlguru.com/the-on-off-controller-output-response-to-set-point-changes/](https://controlguru.com/the-on-off-controller-output-response-to-set-point-changes/)
- Topic ROS 2 (cơ chế truyền tin mà subscriber `/cmd_vel` sẽ sử dụng ở Chương 09): [https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Topics/Understanding-ROS2-Topics.html](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Topics/Understanding-ROS2-Topics.html)
