---
layout: post
title: "Lab: bring-up driver và test quay"
chapter: "07"
order: 2
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter07
lesson_type: required
draft: false
---

Mạch buck đã được chỉnh ổn định ở 5,0 V. Đây là lần đầu tiên bánh xe quay bằng nguồn điện: đặt xe lên giá kê sao cho bánh rời khỏi mặt bàn, chạy thử từng động cơ một cho tới khi lệnh PWM dương làm cả hai lốp quay tiến về phía mũi xe.

Trong kỹ thuật nhúng và robotics, **bring-up** là nghệ thuật đưa một phần cứng mới lắp vào hoạt động từng bước nhỏ có kiểm soát — không bao giờ nạp ngay cả bộ firmware 1.000 dòng rồi cầu nguyện mọi thứ chạy đúng. Ở bài lab bring-up driver, bạn kiểm tra tách biệt từng kênh động cơ, xác nhận cực tính tiến–lùi, đo đối xứng hai bánh và kiểm chứng dấu xung encoder ngay trên bàn kê bánh để mọi tầng điều khiển phía trên đứng trên nền móng 100% tin cậy.

## Kiến thức cần nhớ: Quy trình Bring-Up từng tầng và Chẩn đoán cực tính

### 1. Tách lớp kiểm thử: Điện áp tĩnh → Lệnh đơn kênh → Phản hồi encoder
Thay vì chạy cả hai bánh cùng lúc, hãy chạy từng bánh ở mức PWM thấp (25% → 50%) trong 1–2 giây. Nếu bánh trái quay tiến khi lệnh dương nhưng bánh phải lại quay lùi (rất thường gặp vì hai động cơ gắn đối xứng gương hai bên khung!), bạn sửa ngay bằng cách đảo cặp dây động cơ `OUT3/OUT4` hoặc đảo hằng số cực tính trong phần mềm — đừng để nhầm lẫn dấu lan lên tầng động học!

### 2. Đồng bộ dấu giữa Động cơ và Encoder
Một lỗi siêu nguy hiểm khi sang điều khiển vòng kín PID: lệnh PWM dương làm bánh quay tiến, nhưng dây kênh A/B của encoder lại cắm ngược khiến bộ đếm chạy **âm**! Lúc đó phản hồi âm biến thành **phản hồi dương**, đẩy PWM vọt ngay lên 100% và làm xe phóng mất kiểm soát! Luôn xác nhận: *PWM dương $$\implies$$ bánh tiến $$\implies$$ encoder tăng dương*.

### 3. Bất đối xứng hở vòng tự nhiên giữa hai động cơ
Hai động cơ cùng mã sản xuất vẫn thường chênh nhau $$2\%\text{–}8\%$$ tốc độ ở cùng mức PWM do dung sai chổi than và hộp số. Bring-up ghi nhận mức chênh lệch này để xác nhận động cơ khỏe mạnh (nếu chênh trên 20% thì cần kiểm tra kẹt cơ khí hoặc dây tiếp xúc kém!).

### Giải thích: Cầm tay phân tích log bài test Bring-Up 2 giây trên bàn kê bánh

Bạn kê bánh robot lên không, đặt `PWM = 128` (50% của 8-bit `255`) cho cả hai kênh trong đúng **$$2{,}0\text{ giây}$$** và đọc số xung encoder tích lũy được:
- **Bánh trái:** $$\Delta N_L = +2\,640$$ xung (bánh quay thuận chiều tiến).
- **Bánh phải:** $$\Delta N_R = -2\,580$$ xung (bánh đang quay **ngược** chiều lùi!).

Phân tích ngay 3 kết luận kỹ thuật từ 2 con số này:
1. **Lỗi cực tính bánh phải:** Vì bánh phải quay ngược chiều lùi, bạn đảo hai dây nguồn vào động cơ phải (hoặc đảo cờ `RIGHT_MOTOR_DIR = -1` trong code), rồi kiểm tra lại để đảm bảo $$\Delta N_R$$ đổi thành $$+2\,580$$ xung dương!
2. **Độ bất đối xứng hai bánh ở vòng hở:**
   - Trung bình hai bánh: $$\bar{N} = \frac{2\,640 + 2\,580}{2} = 2\,610\text{ xung}$$.
   - Sai lệch tương đối: $$\frac{\vert 2\,640 - 2\,580 \vert}{2\,610} = \frac{60}{2\,610} \approx 2{,}30\%.$$
   Mức chênh $$2{,}3\%$$ là hoàn toàn bình thường ở vòng hở — đủ tốt để xác nhận cơ khí không kẹt và sẵn sàng bước sang bước thiết kế giao thức teleop!

## Mục tiêu học

1. Kê khung robot lên hộp sao cho cả hai lốp rời hoàn toàn mặt bàn, và chạy thử từng động cơ riêng lẻ với mức PWM giới hạn trong khoảng 60–80 trên thang 255.
2. Kéo chân STBY của TB6612 lên mức cao trước khi tìm lỗi phần mềm, sau đó ghi lại cặp mức logic IN làm bánh trái tiến và cặp làm bánh phải tiến.
3. Nếu một bánh quay ngược chiều, xử lý bằng cách đảo hai dây động cơ đó **hoặc** ghi chú đảo dấu trong firmware — tuyệt đối không làm cả hai cùng lúc.
4. Đo dòng không tải, chỉ thử giữ kẹt (stall) tối đa 1 giây nếu cần đo, và ngắt nguồn ngay nếu mạch driver có mùi khét hoặc tản nhiệt quá nóng không chạm tay được.

## Kiến thức cần có

Bài 07-01 đã hoàn thiện mass chung, cầu chì trên cực dương và mạch buck 5,0 V đo trước khi gắn ESP32. Chương 05 đã trình bày bảng sự thật của cầu H: một cặp mức logic cho chiều tiến, cặp ngược lại cho chiều lùi, và không để ngắn mạch trên cùng một nhánh. Bạn cần phân biệt được các chân của TB6612 (`STBY`, `PWMA`, `PWMB`, `AIN`, `BIN`) hoặc L298N (`ENA`, `ENB`, `INx`, tản nhiệt, jumper 5 V). Chương 06 cung cấp $$b$$, $$r$$ và quy ước chiều tiến là hướng mũi xe, quay trái (yaw dương) khi bánh phải nhanh hơn bánh trái. Quy ước dấu xác định hôm nay sẽ được dùng xuyên suốt cho bộ điều khiển PID ở Chương 08 và các topic ROS ở Chương 09. Bài này chưa dùng ROS.

## Vì sao bài này quan trọng với Capstone A và ROS

Về sau, thông điệp `geometry_msgs/Twist` gửi `linear.x` (vận tốc tiến) và `angular.z` (vận tốc quay yaw), rồi bộ điều khiển tách thành lệnh cho bánh trái và bánh phải. Nếu chiều “dương” của bánh phải thực tế lại làm xe chạy lùi, mọi lệnh `linear.x` dương sẽ biến thành cú xoay tại chỗ, và vòng PID ở Chương 08 sẽ không thể sửa nổi lỗi đấu dây này. Việc kiểm tra dấu chiều quay ngay khi bánh được kê trên không đảm bảo an toàn, tránh việc xe lao khỏi bàn. Ở Bài 03, chúng ta mới đặt tên cho hai con số lệnh này (dưới dạng nấc PWM, chưa phải đơn vị m/s).

## Một kênh, duty nhỏ, STBY phải thức

Đặt khung xe lên một chiếc hộp hoặc chồng sách sao cho cả hai lốp treo lơ lửng, không chạm hộp lẫn mặt bàn. Cấp PWM lần đầu khi bánh đang chạm bàn rất dễ làm robot vọt rơi khỏi bàn.

Chỉ cấp lệnh cho từng động cơ một trong khi động cơ kia giữ PWM bằng 0. Mức duty ban đầu chỉ nên nằm trong khoảng 60–80 trên thang 255, không mở tối đa 255. Với điện áp pack đang ở $$7{,}6~\mathrm{V}$$:

$$
D = \frac{70}{255} \approx 0{,}275, \qquad V_{avg} \approx 0{,}275 \times 7{,}6~\mathrm{V} \approx 2{,}09~\mathrm{V}
$$

(chưa tính sụt áp trên mạch cầu). TB6612 dùng cầu MOSFET có sụt áp rất nhỏ nên truyền gần trọn 2 V tới chổi than, giúp lốp quay chậm vừa đủ để quan sát chiều quay. Trong khi đó, L298N dùng cặp transistor Darlington bị sụt khoảng $$1{,}5$$–$$2~\mathrm{V}$$ nên ở cùng mức duty, động cơ có thể quay rất chậm hoặc chưa thắng nổi ma sát. Đó là lý do TB6612 được ưu tiên hơn; nếu dùng L298N và phải tăng duty mới thấy bánh quay, hãy tăng từng nấc nhỏ và tuân thủ chặt chẽ quy tắc an toàn dòng kẹt bên dưới.

Trên TB6612, chân `STBY` bắt buộc phải kéo lên mức cao; nếu để thấp hoặc bỏ nổi, cả hai kênh đều bị khóa ở trạng thái ngủ bất kể tín hiệu `IN` và `PWM`. Chân `STBY` bỏ nổi là nguyên nhân phổ biến nhất của tình trạng “code đúng nhưng bánh đứng im”. Bạn có thể nối trực tiếp `STBY` lên VCC trong bài thực hành này, hoặc điều khiển bằng một chân GPIO ở Bài 04. Trên L298N, lỗi tương tự xảy ra khi `ENA`/`ENB` đang ở mức thấp hoặc đã rút jumper 5 V mà chưa cấp nguồn 5 V ngoài cho chân logic.

![Tiến là một đường chéo của chữ H; đường kia là lùi]({{ site.imgurl }}/generated/hbridge_concept.png)

![Module L298N: vít motor, tản nhiệt trên cặp Darlington]({{ site.imgurl }}/wikimedia/Dosmotorsl298n.jpg)

Quan sát chiều quay của lốp trái so với hướng mũi xe và ghi lại cặp mức `IN` giúp bánh quay tiến; sau đó lặp lại riêng cho bánh phải. Ví dụ mẫu (cần thay bằng kết quả thực tế trên xe của bạn): bánh trái tiến khi `AIN1` cao, `AIN2` thấp, `PWMA = 70`; bánh phải tiến khi `BIN1` cao, `BIN2` thấp, `PWMB = 70`. Nếu bánh phải quay lùi với mẫu này, bạn có thể đảo hai đầu dây motor phải trên cầu đấu vít **hoặc** giữ nguyên dây và đảo dấu lệnh bên phải trong firmware ở Bài 04 — chỉ chọn **một** trong hai cách. Thực hiện cả hai sẽ làm hai lần đảo triệt tiêu nhau và khiến lệnh đi thẳng ở Bài 05 lại biến thành xoay tròn.

## Dòng không tải, và stall không được giữ

Khi bánh treo trên không ở mức PWM 70, một động cơ TT vỏ vàng thường tiêu thụ dòng không tải khoảng $$0{,}10$$–$$0{,}20~\mathrm{A}$$. Hãy mắc ampe kế nối tiếp vào nhánh động cơ đó (hoặc trên dây nguồn pin khi động cơ kia đang tắt) và ghi lại số đo. Khi chạy đồng thời hai động cơ, dòng tiêu thụ sẽ cộng lại.

![Dòng không tải là đầu thấp của đường cong; stall là đầu cao]({{ site.imgurl }}/generated/stall_current.png)

Nếu muốn ghi nhận một điểm dòng kẹt (stall), chỉ giữ chặt bánh tối đa 1 giây để đọc đồng hồ rồi thả ngay. Thông số dòng kẹt $$1{,}2~\mathrm{A}$$ tại $$6~\mathrm{V}$$ mà người bán ghi chỉ là bậc độ lớn tham khảo, không phải mức dòng cho phép duy trì liên tục. Ngay cả ở PWM 70, dòng kẹt tuy thấp hơn mức toàn áp nhưng vẫn làm nóng nhanh cuộn dây động cơ và tản nhiệt driver. Nếu ngửi thấy mùi khét hoặc không thể chạm ngón tay vào lá tản nhiệt L298N (hay thân IC TB6612), hãy ngắt công tắc nguồn ngay.

Kết thúc bước này, bạn chốt bảng dấu cho các bài sau: với cấu hình chân `IN` đã ghi, PWM dương làm cả hai lốp quay tiến, PWM âm làm lùi và PWM 0 là dừng.

## Lab

### An toàn

Hai lốp phải rời hoàn toàn mặt bàn. Lần chạy thử đầu tiên chỉ cấp điện cho một động cơ với mức PWM giới hạn trong 60–80 trên 255 cho tới khi xác định rõ chiều quay. Công tắc nguồn pin đóng vai trò nút dừng khẩn cấp và phải luôn nằm trong tầm với. Nếu đo dòng kẹt, chỉ giữ tối đa 1 giây; ngừng thí nghiệm ngay nếu mạch quá nóng hoặc có mùi khét. Dòng động cơ bắt buộc lấy từ pin qua cầu chì (không lấy từ USB), và giữ ngón tay tránh xa bánh răng.

### BOM

| Món | Việc |
|------|------|
| Robot bài 07-01 | Cây nguồn đã đo |
| TB6612 hoặc L298N | Cầu đang thử |
| ESP32 hoặc ba sợi dây | STBY hoặc ENA cao, cặp IN, PWM |
| Ampe kế | Không tải, và stall một giây nếu đo |
| Băng dính trên mỗi lốp | Hướng nhìn từ mũi |
| `lab-notes.md` | Bảng dấu |

### Các bước

1. Đặt khung robot lên hộp kê sao cho cả hai bánh treo tự do, không chạm hộp lẫn mặt bàn.
2. Kéo `STBY` lên cao (trên TB6612) hoặc đảm bảo `ENA`/`ENB` sẵn sàng (trên L298N), đặt PWM về 0 rồi bật công tắc pin.
3. Chạy thử riêng động cơ trái ở PWM 70, thử lần lượt hai cặp mức logic `IN` khác nhau (không để cả hai cùng cao) và ghi lại cặp làm bánh lăn về phía mũi xe.
4. Lặp lại quy trình tương tự cho động cơ phải. Nếu bánh quay ngược, đảo hai dây động cơ đó trên cầu vít hoặc ghi chú “đảo dấu trong firmware” (chỉ chọn một cách).
5. Đo dòng không tải của từng động cơ ở PWM 70 (tùy chọn: giữ kẹt 1 giây để đọc dòng rồi thả ngay). Ghi rõ kết luận “PWM dương → cả hai bánh tiến” kèm tên chân thực tế vào sổ.

### Kết quả mong đợi

Một bảng dấu ghi rõ mức logic từng chân, dòng không tải của từng động cơ (ví dụ: trái $$0{,}12~\mathrm{A}$$, phải $$0{,}15~\mathrm{A}$$ tại PWM 70 — giá trị thực tế có thể khác) và xác nhận `STBY` (hoặc `ENA`/`ENB`) đã ở mức cao. Khi nhìn từ đuôi xe và gửi lệnh dương, mảnh băng dính dán trên cả hai lốp đều quay hướng về mũi xe. Sổ tay xác nhận không xảy ra lỗi đảo kép (vừa đảo dây vừa đảo code).

### Lỗi thường gặp

| Bạn thấy | Thường là |
|----------|-----------|
| Cả hai motor chết, code trông đúng | STBY thấp hoặc nổi; ENA/ENB thấp trên L298N |
| Chỉ một motor quay | Chân PWM, cặp IN, hoặc vít kênh đó hở |
| Lốp quay rồi driver có mùi | Duty quá cao hoặc giữ stall quá lâu; ngắt nguồn |
| Trái tiến, phải lùi, cùng mẫu IN | Đảo dây motor phải hoặc dấu firmware, một lần |
| Dòng gần stall dù lốp "tự do" | Lốp cà tấm, hoặc hộp số kẹt |

## Mua ở Việt Nam / Where to buy in Vietnam

Thông thường bạn đã có mạch driver từ Bài 07-01; nếu chưa có, hãy ưu tiên mua TB6612. Mạch L298N có thể dùng thay thế tạm thời nhưng tỏa nhiệt nhiều hơn (cần giữ nguyên lá tản nhiệt và vẫn cấp nguồn ESP32 qua mạch buck). Giá tham khảo khoảng năm 2026 (có thể thay đổi): module TB6612 25.000–70.000 đồng, động cơ TT 25.000–45.000 đồng/chiếc, L298N khoảng 45.000 đồng. Lưu ý module DRV8833 chỉ phù hợp với động cơ rất nhỏ, dễ bị quá tải nếu hai động cơ TT gặp tình huống kẹt bánh.

- L298N đã kiểm, khoảng 45.000 đồng: [hshop.vn/mach-dieu-khien-dong-co-dc-l298](https://hshop.vn/mach-dieu-khien-dong-co-dc-l298)
- [Hshop TB6612](https://hshop.vn/search?q=TB6612), [motor TT](https://hshop.vn/search?q=motor%20TT)
- [Shopee TB6612](https://shopee.vn/search?keyword=TB6612), [motor TT](https://shopee.vn/search?keyword=motor%20TT)
- [Lazada TB6612](https://www.lazada.vn/catalog/?q=TB6612), [L298N](https://www.lazada.vn/catalog/?q=L298N)
- [Thế Giới IC TB6612](https://www.thegioiic.com/search?q=TB6612), [L298N](https://www.thegioiic.com/search?q=L298N)

## Video tham khảo

- **Xem trước:** [TB6612FNG H-Bridge Motor Controller - Better than L298N?](https://www.youtube.com/watch?v=JPPTRj0KWbg) — DroneBot Workshop, tiếng Anh. Minh họa cách cấp PWM và tín hiệu chiều quay cho TB6612; thực hiện khi bánh kê lên khỏi bàn đúng quy trình bài này.
- [Driving DC motors, part 3/3:  H-bridges (Kevin Lynch)](https://www.youtube.com/watch?v=fVgnUWIWzZ8) — Northwestern Robotics, tiếng Anh. Giải thích nguyên lý đảo chiều trên cầu H để sửa đúng một chỗ khi động cơ quay ngược.

## Bài tập

1. Với nguồn VM là $$8{,}0~\mathrm{V}$$ và mức lệnh ban đầu là 80 trên thang 255, tính hệ số duty $$D$$ và điện áp trung bình $$V_{avg}$$ trước sụt áp cầu. Nếu L298N sụt thêm $$1{,}8~\mathrm{V}$$, điện áp còn lại đặt lên chổi than là bao nhiêu?
2. Dòng không tải ở PWM 70 đo được $$0{,}14~\mathrm{A}$$, còn khi giữ kẹt 1 giây lên tới $$0{,}95~\mathrm{A}$$. Giải thích vì sao hai số đo này phù hợp với đặc tuyến động cơ và tại sao phải thả tay ngay.
3. Trên TB6612, chân `STBY` đang bỏ nổi, `AIN1` mức cao, `AIN2` mức thấp, PWM 80 nhưng bánh vẫn đứng yên. Cần bổ sung kết nối nào đầu tiên?
4. Bánh phải quay ngược chiều tiến. Bạn vừa đảo hai dây động cơ đó vừa nhân thêm $$-1$$ vào lệnh bánh phải trong firmware. Khi gửi lệnh PWM dương trên sàn, robot sẽ chuyển động thế nào?
5. Bánh trái quay tiến khi `AIN1 = 1, AIN2 = 0`, còn bánh phải quay tiến (trước khi chỉnh sửa) khi `BIN1 = 0, BIN2 = 1`. Hãy viết quy ước bảng dấu cho firmware Bài 04 mà không cần đảo thêm dây.

### Gợi ý đáp án

1. $$D = 80/255 \approx 0{,}314$$ và $$V_{avg} \approx 0{,}314 \times 8{,}0 \approx 2{,}51~\mathrm{V}$$. Sau khi trừ sụt áp $$1{,}8~\mathrm{V}$$ trên L298N, điện áp đặt lên chổi than chỉ còn khoảng $$0{,}7~\mathrm{V}$$, thường chưa đủ thắng ma sát tĩnh. Đây là lý do nên ưu tiên TB6612 thay vì vội tăng PWM lên 255.
2. Khi chạy không tải, sức phản điện động (back-EMF) gần cân bằng nguồn nên dòng điện nhỏ. Khi kẹp giữ bánh, tốc độ về 0 làm sức phản điện động biến mất và dòng vọt về gần dòng kẹt; chỉ giữ tối đa 1 giây để tránh quá nhiệt cuộn dây và mạch cầu.
3. Kéo chân `STBY` lên mức cao (VCC hoặc GPIO mức cao), vì nếu `STBY` thấp hoặc bỏ nổi thì TB6612 ở trạng thái ngủ.
4. Hai lần đảo chiều triệt tiêu lẫn nhau nên bánh phải vẫn quay lùi khi nhận lệnh dương, khiến robot xoay tròn thay vì chạy thẳng. Chỉ được thực hiện một trong hai cách sửa.
5. Lệnh trái dương: `AIN1 = 1, AIN2 = 0`; lệnh phải dương: `BIN1 = 0, BIN2 = 1`. Khi lệnh âm, đảo ngược mức logic từng cặp tương ứng và giữ nguyên đấu dây trên cầu vít.

## Đọc thêm

- [Pololu TB6612FNG](https://www.pololu.com/product/713)
- [Datasheet L298 của ST](https://www.st.com/resource/en/datasheet/l298.pdf)
- [geometry_msgs/Twist (Jazzy)](https://docs.ros.org/en/jazzy/p/geometry_msgs/interfaces/msg/Twist.html)
- [Arduino `Serial`](https://www.arduino.cc/reference/en/language/functions/communication/serial/)
