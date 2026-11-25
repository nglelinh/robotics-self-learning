---
layout: post
title: "Bánh xe, caster và sơ đồ cơ cấu vi sai"
chapter: "06"
order: 5
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter06
lesson_type: required
draft: false
---

Thời lượng ước tính: **70–90 phút**. Nếu robot đã lắp lăn được, khoảng 10 phút trong đó dùng để xoay thử bằng tay quanh trung điểm trục; nếu chưa, bạn dùng 10 phút đó để vẽ sơ đồ mũi tên vận tốc.

Tại sao gần như mọi robot hút bụi trong nhà lẫn xe giao hàng trong nhà kho đều chọn cấu hình **vi sai hai bánh chủ động + một bánh đa hướng (caster)** thay vì hệ thống lái kiểu ô tô (Ackermann)? Bí mật nằm ở khả năng **quay tại chỗ với bán kính bằng 0**: chỉ cần cho bánh trái lùi và bánh phải tiến cùng tốc độ, robot xoay gọn ngay giữa hành lang hẹp mà không cần lùi chuồng. Và tuyệt vời hơn nữa, toàn bộ động học của hệ vi sai nằm gọn trong hai phương trình cộng–trừ đơn giản đến bất ngờ!

## Kiến thức cần nhớ: Động học vi sai, Tâm quay tức thời (ICC) và Bánh Caster

### 1. Hai phương trình vàng của động học thuận vi sai (Forward Kinematics)
Gọi $$L$$ là khoảng cách giữa tâm hai bánh chủ động (*track width*), $$v_L$$ và $$v_R$$ là vận tốc tiếp tuyến của bánh trái và bánh phải (tính từ $$v = r\omega$$). Khi không trượt ngang, vận tốc tịnh tiến $$v$$ và vận tốc góc $$\omega$$ của tâm robot là:
$$v = \frac{v_R + v_L}{2}, \qquad \omega = \frac{v_R - v_L}{L}.$$
Từ đây suy ngay ra **động học ngược (Inverse Kinematics)** để đổi lệnh ROS `cmd_vel` $$(v, \omega)$$ thành tốc độ hai bánh:
$$v_R = v + \frac{\omega L}{2}, \qquad v_L = v - \frac{\omega L}{2}.$$

### 2. Tâm quay tức thời (ICC — Instantaneous Center of Curvature)
Mọi chuyển động của xe vi sai ở một thời điểm đều là một chuyển động tròn quanh điểm **ICC** nằm trên đường kéo dài của trục hai bánh, cách tâm robot một bán kính $$R = \frac{v}{\omega} = \frac{L}{2}\frac{v_R + v_L}{v_R - v_L}$$. Khi $$v_R = v_L$$, $$R \to \infty$$ (đi thẳng); khi $$v_R = -v_L$$, $$R = 0$$ (quay tại chỗ quanh tâm trục!).

### 3. Cái bẫy của bánh đa hướng (Swivel Caster vs. Ball Caster)
Bánh bi thép (*ball caster*) quay mọi hướng không bị giật nhưng hay kẹt tóc/bụi và ma sát cao trên thảm. Bánh xoay (*swivel caster*) lăn rất êm nhưng có khoảng lệch trục xoay (*caster offset*) — mỗi khi robot đột ngột đảo chiều từ tiến sang lùi, bánh xoay phải lật $$180^\circ$$, tạo ra một cú hích ngang làm lệch hướng khởi động!

### Giải thích: Cầm tay giải cả Động học thuận và Động học ngược cho robot vi sai

Xét robot vi sai có khoảng cách hai bánh **$$L = 0{,}20\text{ m}$$** (20 cm) và bán kính bánh **$$r = 0{,}035\text{ m}$$** (đường kính 7 cm):

**Bài toán 1 — Động học thuận (từ encoder bánh xe suy ra chuyển động robot):**
Encoder đo được bánh trái chạy $$v_L = 0{,}30\text{ m/s}$$, bánh phải chạy $$v_R = 0{,}50\text{ m/s}$$.
1. Vận tốc tịnh tiến của tâm robot:
   $$v = \frac{0{,}50 + 0{,}30}{2} = 0{,}40\text{ m/s}.$$
2. Vận tốc góc quay (quy ước dương = rẽ trái / ngược chiều kim đồng hồ):
   $$\omega = \frac{0{,}50 - 0{,}30}{0{,}20} = \frac{0{,}20}{0{,}20} = +1{,}00\text{ rad/s}\;(\approx 57{,}3^\circ/\text{s}).$$
3. Bán kính quỹ đạo cung tròn quanh tâm ICC:
   $$R = \frac{v}{\omega} = \frac{0{,}40}{1{,}00} = 0{,}40\text{ m}\;(40\text{ cm về phía bên trái robot}).$$

**Bài toán 2 — Động học ngược (từ lệnh `cmd_vel` tìm tốc độ góc từng bánh):**
Bộ điều hướng yêu cầu robot đi thẳng kết hợp rẽ phải: $$v = 0{,}50\text{ m/s},\; \omega = -2{,}0\text{ rad/s}$$.
- $$v_R = 0{,}50 + \frac{(-2{,}0)(0{,}20)}{2} = 0{,}50 - 0{,}20 = 0{,}30\text{ m/s} \implies \omega_R = \frac{0{,}30}{0{,}035} \approx 8{,}57\text{ rad/s}.$$
- $$v_L = 0{,}50 - \frac{(-2{,}0)(0{,}20)}{2} = 0{,}50 + 0{,}20 = 0{,}70\text{ m/s} \implies \omega_L = \frac{0{,}70}{0{,}035} = 20{,}0\text{ rad/s}.$$
Kiểm tra trực giác: bánh trái quay nhanh hơn bánh phải nên robot rẽ sang phải — khớp tuyệt đối!

## Mục tiêu học

Sau bài này, các bạn vẽ được sơ đồ vectơ vận tốc hai bánh cho ba trạng thái: đi thẳng, quẹo nhẹ và xoay tại chỗ, đồng thời tính được vận tốc góc xoay tại chỗ $$\omega = 2 v_r / b$$. Các bạn giải thích được vai trò của khoảng đuôi (trail) trên bánh caster, lý do caster lắp ngược bị rung lắc và vì sao cơ cấu bốn bánh cố định tiêu tốn dòng điện gần mức dòng kẹt (Chương 05). Cuối cùng, các bạn xác định đúng trung điểm trục làm tâm quay và liên hệ trực tiếp `cmd_vel` (`linear.x` và `angular.z`) với hai động cơ.

## Kiến thức cần có

Các bạn nắm vững định nghĩa từ Bài 01: khổ vết $$b$$ giữa hai tâm tiếp xúc, bán kính lăn $$r$$ từ phép lăn một vòng và cặp phương trình:

$$
v = \frac{v_r + v_l}{2}, \qquad \omega = \frac{v_r - v_l}{b}.
$$

Các bạn đã hiểu sai số ở $$b$$ sẽ khiến lệnh đi thẳng biến thành quỹ đạo cong, và tỉ số truyền bánh răng (Bài 03) quy đổi góc quay động cơ sang góc quay bánh xe.

## Vì sao bài này quan trọng với Capstone A và ROS

Capstone A sử dụng cấu hình hai bánh chủ động kết hợp một bánh caster. Trong ROS, lệnh điều khiển gửi qua thông điệp `geometry_msgs/Twist` với `linear.x` là $$v$$ và `angular.z` là $$\omega$$. Bộ điều khiển `diff_drive_controller` giải ngược hai phương trình trên để xuất lệnh tốc độ cho động cơ trái và động cơ phải.

Nếu một động cơ bị đấu ngược chiều, bộ điều khiển phần mềm không thể tự biết: cả hai bánh cùng nhận lệnh “tiến” nhưng trên sàn một bánh lại chạy lùi, khiến robot xoay tròn thay vì đi thẳng. Ở Chương 07, bạn sẽ kiểm tra dấu chiều quay khi nhấc bánh khỏi sàn rồi mới xác nhận lại trên mặt đất — nơi bánh caster và độ bám lốp bắt đầu phát huy tác dụng. Sơ đồ mũi tên vận tốc hôm nay là chuẩn đối chiếu trực tiếp khi gỡ lỗi.

## Mũi tên, khoảng đuôi, và bánh bị cà

Khi đi thẳng, hai vết tiếp xúc chuyển động cùng vận tốc ($$v_r = v_l$$), do đó $$v$$ bằng vận tốc bánh và $$\omega = 0$$. Tâm quay tức thời nằm ở vô cực trên đường kéo dài của trục bánh.

Khi quẹo trái nhẹ, cả hai bánh vẫn tiến về phía trước nhưng bánh phải nhanh hơn bánh trái. Trong hệ tọa độ robot chuẩn (trục $$x$$ hướng về phía mũi, trục $$z$$ hướng lên trên), $$\omega > 0$$ tương ứng với chuyển động quay sang trái quanh một tâm nằm trên đường trục, phía ngoài bánh trái. Bánh caster lúc này tự xoay theo quỹ đạo.

Xoay tại chỗ là trường hợp đặc biệt khi hai bánh quay ngược chiều với cùng độ lớn vận tốc: $$v_l = -v_r$$. Khi đó:

$$
v = \frac{v_r + (-v_r)}{2} = 0, \qquad \omega = \frac{v_r - (-v_r)}{b} = \frac{2 v_r}{b}.
$$

Vận tốc tịnh tiến bằng không và tâm quay trùng với trung điểm đoạn nối hai tâm tiếp xúc. Hãy đánh dấu điểm này lên tấm khung: khi xoay robot chậm bằng tay trên sàn nhẵn, dấu này phải đứng yên tại một điểm trên sàn trong lúc hai bánh lăn quanh nó. Nếu bạn đánh dấu sai vị trí (ví dụ đặt tại bánh caster hoặc giữa hai vỏ động cơ), điểm dấu sẽ vẽ thành một vòng tròn, cho thấy tâm hình học bạn chọn không trùng với tâm động học thực tế.

Khoảng đuôi (trail) của bánh caster là yếu tố giúp điểm tựa thứ ba tự ổn định hướng. Trên bánh caster xoay, vết tiếp xúc nằm lùi phía sau trục xoay dọc theo chiều chuyển động; lực cản lăn tại vết tiếp xúc sẽ tự động kéo bánh thẳng hàng theo hướng đi (giống bánh xe đẩy siêu thị). Nếu lắp ngược caster khiến vết tiếp xúc nằm phía trước chốt xoay, bánh sẽ mất ổn định và rung lắc mạnh, đặc biệt khi tăng tốc. Bánh bi đa hướng hầu như không có khoảng đuôi vì điểm tiếp xúc nằm ngay trên trục xoay, nên dễ bị trượt cà làm tăng ma sát ngoài dự kiến dù vẫn đỡ được mũi xe. Capstone A ưu tiên dùng bánh caster xoay có khoảng đuôi rõ ràng và lắp sao cho vết tiếp xúc đi sau chốt xoay.

Cơ cấu lái trượt (skid-steer) sử dụng bốn bánh cố định không xoay hướng. Mỗi khi chuyển hướng, lốp xe buộc phải trượt ngang trên sàn. Ma sát trượt ngang đòi hỏi động cơ kéo dòng điện rất lớn — tiệm cận mức dòng kẹt mà Chương 05 đã cảnh báo là rủi ro quá nhiệt. Capstone A tránh tổn hao này bằng cách dùng hai bánh chủ động kết hợp một bánh caster có đuôi để mọi cú quay đều dựa trên chuyển động lăn.

Lưu ý rằng đường kính cao su ghi trên bao bì vẫn không phải là bán kính lăn thực tế. Hãy lặp lại phép lăn một vòng trên giấy (Bài 01) mỗi khi thay lốp hoặc thay đổi tải trọng. Nếu bán kính lăn của bánh phải lớn hơn bánh trái, một lệnh đi thẳng đều sẽ khiến robot tự quẹo nhẹ sang trái.

![Đặt thước ở đâu: tâm tiếp xúc và bán kính đã nén]({{ site.imgurl }}/generated/chassis_measures.png)

![Mũi tên bằng nhau, mũi tên lệch nhau, và cú xoay đặt tâm quay đúng trung điểm trục]({{ site.imgurl }}/generated/diff_drive_kinematics.png)

Hãy đối chiếu đồng thời cả hai hình: hình đầu tiên giúp đo đúng $$b$$ và $$r$$, còn hình thứ hai minh họa ngôn ngữ vectơ vận tốc cho ba trạng thái tiến, xoay tại chỗ và quẹo. Khi đấu dây động cơ ở Chương 07, hãy dán nhãn dây theo đúng quy ước mũi tên này trước khi mặc định tín hiệu PWM dương luôn làm xe chạy tiến.

## Ví dụ tính tay

Lấy khung xe ở Bài 01 với $$b = 0.15$$ m, ra lệnh xoay tại chỗ ở $$v_r = 0.20$$ m/s và $$v_l = -0.20$$ m/s:

$$
v = 0, \qquad \omega = \frac{2 \times 0.20}{0.15} = 2.667\ \text{rad/s}.
$$

Một vòng quay đầy đủ là $$2\pi$$ radian, nên thời gian hoàn thành một vòng là:

$$
T = \frac{2\pi}{2.667} \approx 2.36\ \text{s},
$$

giả sử hai bánh đạt đúng vận tốc 0,20 m/s và không bị trượt. Với bán kính lăn $$r = 31.2$$ mm, độ lớn vận tốc góc của mỗi bánh xe là:

$$
\dot{\theta} = \frac{0.20}{0.0312} \approx 6.41\ \text{rad/s},
$$

trong đó hai động cơ quay ngược dấu nhau. Nếu một dây động cơ bị đấu ngược, lệnh đi thẳng $$v = 0.20$$ m/s, $$\omega = 0$$ (phần mềm xuất hai giá trị dương) sẽ biến thành $$v_l = 0.20$$ m/s và $$v_r = -0.20$$ m/s trên sàn — tức là robot xoay tại chỗ thay vì đi thẳng. Vì vậy, bước thử nhấc bánh ở Chương 07 là bắt buộc để đảm bảo lệnh dương làm cả hai bánh cùng quay tiến.

## Lab: tìm tâm quay, hoặc vẽ mũi tên

### An toàn

Khi xoay robot đã lắp bằng tay, luôn ngắt kết nối pin để tránh việc động cơ bị dẫn ngược phát điện áp ngược về mạch cầu H. Giữ ngón tay tránh xa bánh răng và khe dưới bánh caster khi xoay trên sàn cứng để không bị kẹp tay.

### BOM

| Hạng mục | Vai trò |
|------|------|
| Khung từ Bài 01, hoặc bản vẽ nhìn từ trên đúng tỉ lệ | Cơ cấu |
| Băng dính và bút | Tâm quay dự đoán |
| `lab-notes.md` | Phác mũi tên hoặc ghi chú thử bằng tay |

### Các bước

1. Đánh dấu trung điểm của đoạn nối hai tâm tiếp xúc mặt lốp — đây là tâm xoay dự đoán.
2. Nếu khung xe đã lăn được, ngắt pin rồi xoay chậm khung tại chỗ bằng tay. Quan sát điểm đánh dấu: nếu đo $$b$$ chính xác và bánh không trượt, điểm dấu sẽ đứng yên tại một vị trí trên sàn.
3. Kiểm tra khoảng đuôi của bánh caster từ góc nhìn ngang: vết tiếp xúc phải nằm sau chốt xoay theo chiều đẩy tiến. Nếu càng bị lắp ngược, ghi chú để xoay lại trước Chương 07.
4. Nếu chưa có khung xe thực tế, vẽ ba sơ đồ nhìn từ trên xuống: đi thẳng (hai mũi tên tiến bằng nhau), xoay tại chỗ (hai mũi tên ngược chiều bằng nhau, có đánh dấu tâm xoay) và quẹo trái nhẹ (cả hai mũi tên tiến, mũi tên phải dài hơn). Ghi rõ $$v$$ và $$\omega$$ trên từng hình.
5. Ghi quy ước dấu sẽ áp dụng trong firmware vào sổ tay: giá trị dương cho bánh trái và bánh phải đều đẩy robot tiến về phía trước.

### Kết quả mong đợi

Điểm đánh dấu đứng yên khi xoay thử cẩn thận bằng tay, hoặc bộ ba sơ đồ mũi tên đã ghi chú đầy đủ. Ghi chú trong `lab-notes.md` nêu rõ hướng lắp caster (vết tiếp xúc đi sau chốt xoay) và quy ước dấu chiều quay để kiểm chứng khi nhấc bánh ở Chương 07.

### Lỗi thường gặp

| Các bạn thấy | Thường nghĩa là |
|--------------|------------------------|
| “Trung điểm” đi thành vòng tròn | Dấu nằm giữa hai vỏ động cơ, hoặc một bánh đang trượt |
| Caster kêu lạch cạch ngay khi đẩy | Càng lắp ngược, hoặc gần như không có tải trên caster |
| Bánh bi cà và làm tấm quay ngang | Không có khoảng đuôi; lắp bánh caster xoay cho Capstone A |
| Lệnh tiến vẽ thành vòng tròn sau khi có điện | Một dấu động cơ bị đảo; xác nhận khi nhấc bánh ở Chương 07 |
| Đường thẳng cong nhẹ dù lệnh đều | Hai bán kính lăn không khớp nhau |

## Mua ở Việt Nam / Where to buy in Vietnam

Khung xe đã được đề cập ở Bài 01; bài này bổ sung bánh xe và bánh caster nếu bộ kit của bạn chưa có sẵn. Bạn có thể mua thêm một bánh bi đa hướng (tùy chọn) để trực tiếp cảm nhận sự khác biệt khi không có khoảng đuôi, nhưng xe nộp cho Capstone A vẫn dùng bánh caster xoay.

| Mua gì | Từ khóa | Khoảng giá (VND) | Ghi chú |
|------|----------|------------------|-------|
| Bánh cao su | `bánh xe cao su 65mm` | 15.000–45.000 mỗi cái | Rồi làm phép lăn để lấy $$r$$ |
| Bánh caster xoay | `bánh caster robot` | 12.000–40.000 | Khoảng đuôi nhìn thấy phía sau chốt |
| Bánh bi đa hướng | `bánh đa hướng bi` | 15.000–40.000 | Để đối chiếu, tùy chọn; nó cà |

Các trang tìm mua:

- [Hshop](https://hshop.vn/search?q=b%C3%A1nh+xe+cao+su)
- [Shopee](https://shopee.vn/search?keyword=b%C3%A1nh%20xe%20cao%20su%2065mm)
- [Lazada](https://www.lazada.vn/catalog/?q=b%C3%A1nh%20caster%20robot)
- [Thế Giới IC](https://www.thegioiic.com/search?q=b%C3%A1nh%20xe%20robot)

Giá bán có thể thay đổi theo thời điểm. Hãy kiểm tra moay-ơ bánh khớp với trục chữ D của động cơ TT hoặc khớp với lỗ khớp nối đã đo ở Bài 02.

## Video tham khảo

- **Xem trước:** [Differential Drive & Odometry Explained: How It Works](https://www.youtube.com/watch?v=2QE3LG5h2tw) — Netizen Robotics, tiếng Anh. Giải thích cơ cấu vi sai chuyển đổi vận tốc hai bánh thành tiến và quay; lưu ý bánh caster không phải bánh chủ động.
- [Modern Robotics, Chapter 13.4:  Odometry](https://www.youtube.com/watch?v=eQ9E0Zvp9jw) — Northwestern Robotics, tiếng Anh. Trình bày cách tính odometry từ bánh xe, nhấn mạnh sự tách biệt giữa bán kính bánh và khổ vết.

## Bài tập

1. Cho $$b = 0.18$$ m, $$v_r = 0.15$$ m/s và $$v_l = -0.15$$ m/s. Tính $$v$$, $$\omega$$ và thời gian xoay đủ một vòng.
2. Cả hai bánh cùng chạy ở $$+0.22$$ m/s với $$b = 0.15$$ m. Tính $$v$$, $$\omega$$ và cho biết tâm quay nằm ở đâu.
3. Khi đẩy robot tiến tới, bánh caster bị lật vòng rồi rung lắc liên tục. Khoảng đuôi đang gặp vấn đề gì và cách khắc phục cơ khí ra sao?
4. Một robot bốn bánh cố định xoay tại chỗ trên thảm khiến dòng điện tăng sát mức dòng kẹt. Giải thích nguyên nhân và cho biết Capstone A dùng cơ cấu nào để tránh tình trạng này.
5. Khi gửi lệnh `linear.x = 0.2` và `angular.z = 0` mà chưa thay đổi $$b$$, robot lại chạy xoay tròn. Cần kiểm tra chi tiết đấu dây nào khi nhấc bánh khỏi sàn?

### Gợi ý đáp án

1. $$v = 0$$, $$\omega = 2\times 0.15/0.18 = 1.667$$ rad/s, thời gian một vòng $$T = 2\pi/1.667 \approx 3.77$$ s.
2. $$v = 0.22$$ m/s, $$\omega = 0$$. Tâm quay nằm ở vô cực trên đường kéo dài của trục bánh; hướng mũi xe không thay đổi.
3. Vết tiếp xúc đang đi trước chốt xoay (caster lắp ngược hoặc càng không có khoảng đuôi). Cần xoay và lắp lại để vết tiếp xúc nằm phía sau chốt xoay.
4. Bốn bánh cố định buộc lốp phải trượt cà ngang khi quay, tạo ma sát trượt lớn đòi hỏi mô-men và dòng điện gần mức kẹt. Capstone A dùng hai bánh chủ động kết hợp một bánh caster có đuôi để bánh tự xoay theo hướng lăn.
5. Một trong hai động cơ bị đấu ngược cực (đảo dấu). Cần nhấc bánh khỏi sàn và kiểm tra sao cho lệnh dương làm cả hai bánh cùng quay theo chiều tiến đã quy ước.

## Đọc thêm

- [diff_drive_controller (ROS 2)](https://github.com/ros-controls/ros2_controllers/tree/master/diff_drive_controller) — cách chuyển đổi `linear.x` và `angular.z` thành vận tốc hai bánh theo các phương trình trong bài.
- [Thiết lập odometry trên Nav2](https://navigation.ros.org/setup_guides/odom/setup_odom.html) — hướng dẫn xuất bản odometry sau khi các quy ước dấu và thông số bánh đã chính xác.
- [Wiki diff_drive_controller ROS 1](https://wiki.ros.org/diff_drive_controller) — trình bày tương tự về việc tách khớp bánh trái và bánh phải (dù viết cho ROS 1 nhưng mô hình vẫn áp dụng đúng).

Tài liệu tham khảo chuyên sâu hơn là cuốn *Introduction to Autonomous Mobile Robots* của Siegwart, Nourbakhsh và Scaramuzza; với các tham số cụ thể cho phiên bản ROS đang dùng, hãy ưu tiên các liên kết tài liệu ở trên.
