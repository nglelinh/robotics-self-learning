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

Thời lượng ước tính: **70–90 phút**. Nếu robot đã lăn được, mười phút trong số đó là xoay tay quanh trung điểm trục. Nếu chưa lăn, mười phút ấy là một phác họa mũi tên vận tốc.

## Mục tiêu học

Hết bài này, các bạn vẽ được mũi tên vận tốc bánh cho chuyển động thẳng, cho một cú quay nhẹ, và cho một cú xoay tại chỗ, đồng thời tính được vận tốc góc khi xoay tại chỗ $$\omega = 2 v_r / b$$. Các bạn giải thích được khoảng đuôi của bánh caster, vì sao caster lắp ngược thì lắc, và vì sao bốn bánh cố định lãng phí dòng kẹt mà các bạn đã tính ở Chương 05. Các bạn chỉ được trung điểm trục như tâm quay, và nối `cmd_vel` linear.x cùng angular.z với hai động cơ.

## Kiến thức cần có

Định nghĩa của Bài 01: $$b$$ giữa hai tâm tiếp xúc, $$r$$ từ phép lăn, và

$$
v = \frac{v_r + v_l}{2}, \qquad \omega = \frac{v_r - v_l}{b}.
$$

Các bạn biết một $$b$$ sai vẽ thành vòng tròn trên lệnh đi thẳng. Bánh răng (Bài 03) đã đặt cách radian động cơ trở thành radian bánh.

## Vì sao bài này quan trọng với Capstone A và ROS

Capstone A là hai bánh chủ động cộng một bánh caster. ROS sẽ gửi `geometry_msgs/Twist` với linear.x là $$v$$ và angular.z là $$\omega$$. `diff_drive_controller` đảo hai phương trình và ra lệnh một động cơ trái, một động cơ phải. Sai dấu trên một động cơ là sự thật cơ khí mà bộ điều khiển không nhìn thấy: cả hai bánh “tiến” trong phần mềm, một bánh lùi trên sàn, và quỹ đạo là vòng tròn quanh phía chậm hơn. Các bạn sẽ tìm dấu ấy ở Chương 07 khi bánh được nhấc lên, rồi xác nhận trên sàn, nơi bánh caster và cao su cuối cùng mới có tiếng nói. Những mũi tên vẽ hôm nay là bức tranh các bạn sẽ đối chiếu khi gỡ lỗi.

## Mũi tên, khoảng đuôi, và bánh bị cà

Đi thẳng, cả hai vết tiếp xúc tiến cùng tốc độ. Khi đó $$v_r = v_l$$, nên $$v$$ bằng tốc độ ấy và $$\omega = 0$$. Tâm tức thời của chuyển động nằm vô cùng về một bên: trục không quay quanh một điểm gần.

Một cú quẹo trái nhẹ giữ cả hai bánh tiến và làm bánh phải nhanh hơn. $$\omega$$ dương trong hệ robot thông thường, trục x hướng mũi và trục z hướng lên, tức quay trái. Robot quay quanh một điểm trên đường trục, nằm ngoài bánh trái. Bánh caster xoay để đi theo.

Xoay tại chỗ là trường hợp thuần. Đặt $$v_l = -v_r$$. Khi đó

$$
v = \frac{v_r + (-v_r)}{2} = 0, \qquad \omega = \frac{v_r - (-v_r)}{b} = \frac{2 v_r}{b}.
$$

Vận tốc thân bằng không và tâm quay là trung điểm trục, nằm giữa hai tâm tiếp xúc. Đánh dấu điểm ấy trên tấm. Nếu xoay robot bằng tay trên sàn nhẵn, dấu phải đứng yên trong khi hai bánh quay quanh nó. Một dấu đặt tại caster, hoặc một dấu đặt giữa hai vỏ động cơ, sẽ đi thành vòng tròn và nói rằng tâm hình học các bạn chọn với tâm động học là hai điểm khác nhau.

Khoảng đuôi của bánh caster là lý do bánh thứ ba biết cư xử. Trên bánh caster xoay, vết tiếp xúc ngồi phía sau trục xoay, dọc theo hướng đi. Lực cản tại vết kéo bánh vào thẳng hàng, giống bánh xe đẩy siêu thị tự chỉnh. Khoảng đuôi chính là độ lệch ấy. Lắp caster ngược thì vết tiếp xúc dẫn trước chốt xoay. Bánh khi đó mất ổn định và lắc, nhất là khi tốc độ tăng. Bánh bi gần như không có khoảng đuôi: điểm tiếp xúc nằm trên trục xoay. Nó cà thay vì tự chỉnh, thêm ma sát các bạn chưa dự trù, và vẫn đỡ được mũi. Capstone A muốn một bánh caster xoay có khoảng đuôi nhìn thấy được, lắp sao cho vết tiếp xúc đi sau.

Lái bằng trượt đặt động cơ lên bốn bánh cố định, hoặc khóa bánh để không bánh nào xoay được. Mọi cú quay đều buộc lốp cà ngang. Cà là ma sát trượt, và nó đòi động cơ một dòng gần giá trị kẹt mà Chương 05 đã coi là sự cố nhiệt, không phải một cú quay bình thường. Capstone A dành dòng ấy cho việc lăn. Hai bánh chủ động và một bánh caster có đuôi là cơ cấu ấy.

Đường kính cao su trên túi vẫn không phải bán kính lăn. Dùng lại phép lăn trên giấy của Bài 01 mỗi khi đổi lốp, đổi tải, hoặc đổi độ phồng của lốp mềm. Bán kính bên phải lớn hơn trên một lệnh đi thẳng vốn đều sẽ thành một cú quẹo nhẹ mà các bạn không hề xin.

![Đặt thước ở đâu: tâm tiếp xúc và bán kính đã nén]({{ site.imgurl }}/generated/chassis_measures.png)

![Mũi tên bằng nhau, mũi tên lệch nhau, và cú xoay đặt tâm quay đúng trung điểm trục]({{ site.imgurl }}/generated/diff_drive_kinematics.png)

Dùng hai hình cùng lúc. Hình thứ nhất giữ $$b$$ và $$r$$ trung thực. Hình thứ hai là ngôn ngữ mũi tên: tiến, xoay tại chỗ, và trường hợp trộn. Khi đi dây động cơ ở Chương 07, dán nhãn dây cho khớp các mũi tên này trước khi tin một PWM dương nghĩa là “tiến”.

## Ví dụ tính tay

Lấy khung của Bài 01, $$b = 0.15$$ m, và ra lệnh xoay tại chỗ với $$v_r = 0.20$$ m/s và $$v_l = -0.20$$ m/s.

$$
v = 0, \qquad \omega = \frac{2 \times 0.20}{0.15} = 2.667\ \text{rad/s}.
$$

Một vòng đủ là $$2\pi$$ radian, nên thời gian xoay một vòng là

$$
T = \frac{2\pi}{2.667} \approx 2.36\ \text{s},
$$

miễn là bánh thực sự đạt 0,20 m/s và không cà. Với $$r = 31.2$$ mm, tốc độ góc của bánh có độ lớn

$$
\dot{\theta} = \frac{0.20}{0.0312} \approx 6.41\ \text{rad/s},
$$

hai động cơ ngược dấu. Nếu một dây động cơ bị đảo, lệnh $$v = 0.20$$, $$\omega = 0$$ (cả hai tốc độ phần mềm đều “dương”) trở thành $$v_l = 0.20$$ và $$v_r = -0.20$$ trên sàn. Đó chính là cú xoay này, không phải đường thẳng. Nhấc bánh ở Chương 07: lệnh dương, cả hai lốp tiến. Thử trên sàn: trung điểm trục chỉ đứng yên khi các bạn đã xin một cú xoay.

## Lab: tìm tâm quay, hoặc vẽ mũi tên

### An toàn

Nếu xoay một robot đã lắp bằng tay, pin phải được ngắt để động cơ bị dẫn ngược không đưa điện áp lên mạch cầu. Ngón tay ra khỏi bánh răng. Trên sàn cứng, xoay chậm; một ngón dưới bánh caster là một điểm kẹp.

### BOM

| Hạng mục | Vai trò |
|------|------|
| Khung từ Bài 01, hoặc bản vẽ nhìn từ trên đúng tỉ lệ | Cơ cấu |
| Băng dính và bút | Tâm quay dự đoán |
| `lab-notes.md` | Phác mũi tên hoặc ghi chú thử bằng tay |

### Các bước

1. Đánh dấu trung điểm của đoạn nối hai tâm tiếp xúc. Đó là tâm xoay dự đoán.
2. Nếu robot lăn được, ngắt pin. Xoay khung chậm tại chỗ bằng tay. Nhìn dấu. Một phép đo $$b$$ tốt cho thấy dấu đứng trên một điểm sàn trong khi cả hai bánh quay quanh nó.
3. Ghi xem bánh caster có đuôi không. Nhìn từ bên: vết tiếp xúc phải ngồi sau chốt xoay theo hướng các bạn đẩy. Nếu càng bị ngược, ghi vào sổ và xoay lại trước Chương 07.
4. Nếu chưa có khung lăn, vẽ ba hình nhìn từ trên. Tiến: hai mũi tên bằng nhau. Xoay tại chỗ: hai mũi tên ngược chiều, có đánh dấu tâm. Quẹo trái nhẹ: cả hai mũi tên tiến, mũi tên phải dài hơn. Ghi $$v$$ và $$\omega$$ trên mỗi hình.
5. Viết quy ước dấu các bạn sẽ dùng trong firmware: bánh trái dương và bánh phải dương đều đẩy robot tiến.

### Kết quả mong đợi

Một dấu đứng yên trong cú xoay tay cẩn thận, hoặc ba bản vẽ mũi tên đã dán nhãn. Ghi chú nói hướng caster các bạn sẽ lắp: vết tiếp xúc đi sau chốt xoay. Câu quy ước dấu là thứ Chương 07 kiểm được khi bánh được nhấc lên.

### Lỗi thường gặp

| Các bạn thấy | Thường nghĩa là |
|--------------|------------------------|
| “Trung điểm” đi thành vòng tròn | Dấu nằm giữa hai vỏ động cơ, hoặc một bánh đang trượt |
| Caster kêu lạch cạch ngay khi đẩy | Càng lắp ngược, hoặc gần như không có tải trên caster |
| Bánh bi cà và làm tấm quay ngang | Không có khoảng đuôi; lắp bánh caster xoay cho Capstone A |
| Lệnh tiến vẽ thành vòng tròn sau khi có điện | Một dấu động cơ bị đảo; xác nhận khi nhấc bánh ở Chương 07 |
| Đường thẳng cong nhẹ dù lệnh đều | Hai bán kính lăn không khớp nhau |

## Mua ở Việt Nam / Where to buy in Vietnam

Bài 01 đã mua tấm khung. Bài này là bánh xe và bánh caster, nếu hai dòng ấy còn thiếu. Một bánh bi là phụ tùng hữu ích để cảm một lần “không có đuôi”. Robot các bạn nộp dùng bánh caster xoay.

| Mua gì | Từ khóa | Khoảng giá (VND) | Ghi chú |
|------|----------|------------------|-------|
| Bánh cao su | `bánh xe cao su 65mm` | 15.000–45.000 mỗi cái | Rồi làm phép lăn để lấy $$r$$ |
| Bánh caster xoay | `bánh caster robot` | 12.000–40.000 | Khoảng đuôi nhìn thấy phía sau chốt |
| Bánh bi đa hướng | `bánh đa hướng bi` | 15.000–40.000 | Để đối chiếu, tùy chọn; nó cà |

Các trang tìm:

- [Hshop](https://hshop.vn/search?q=b%C3%A1nh+xe+cao+su)
- [Shopee](https://shopee.vn/search?keyword=b%C3%A1nh%20xe%20cao%20su%2065mm)
- [Lazada](https://www.lazada.vn/catalog/?q=b%C3%A1nh%20caster%20robot)
- [Thế Giới IC](https://www.thegioiic.com/search?q=b%C3%A1nh%20xe%20robot)

Giá dịch chuyển. Khớp moay-ơ với trục chữ D của TT, hoặc với lỗ khớp nối đã đo ở Bài 02.

## Bài tập

1. $$b = 0.18$$ m, $$v_r = 0.15$$ m/s, $$v_l = -0.15$$ m/s. Tìm $$v$$, $$\omega$$, và thời gian cho một vòng xoay đủ.
2. Cả hai bánh ở $$+0.22$$ m/s, $$b = 0.15$$ m. Tìm $$v$$ và $$\omega$$, và tâm quay nằm ở đâu.
3. Các bạn đẩy robot và bánh caster lật vòng rồi dao động. Khoảng đuôi sai ở chỗ nào, và các bạn sửa cơ khí thế nào?
4. Một robot bốn bánh cố định xoay tại chỗ trên thảm. Vì sao dòng leo tới gần dòng kẹt, và Capstone A dùng cơ cấu nào để một cú quay vẫn lăn được?
5. linear.x = 0,2 và angular.z = 0 mà robot vẫn chạy vòng. Các bạn chưa đổi $$b$$. Sự thật đi dây nào cần thử khi bánh được nhấc lên?

### Gợi ý đáp án

1. $$v = 0$$, $$\omega = 2\times 0.15/0.18 = 1.667$$ rad/s, $$T = 2\pi/1.667 \approx 3.77$$ s. 2. $$v = 0.22$$ m/s, $$\omega = 0$$. Tâm quay không phải một điểm gần trên trục; hướng mũi không đổi. 3. Vết tiếp xúc đang dẫn trước chốt xoay, nên caster bị ngược hoặc càng không có khoảng đuôi. Lắp lại để vết đi sau. 4. Lốp phải cà ngang, và cà đòi mô-men mức kẹt. Capstone A dùng hai bánh chủ động và một bánh caster có đuôi để bánh tự do xoay theo. 5. Dấu của một động cơ bị đảo. Nhấc bánh, một lệnh dương phải làm cả hai lốp quay theo chiều tiến đã định trong lab.

## Đọc thêm

- [diff_drive_controller (ROS 2)](https://github.com/ros-controls/ros2_controllers/tree/master/diff_drive_controller) — linear.x và angular.z trở thành hai vận tốc bánh qua các phương trình của bài này.
- [Thiết lập odometry trên Nav2](https://navigation.ros.org/setup_guides/odom/setup_odom.html) — thứ các bạn xuất bản sau khi các mũi tên đã trung thực.
- [Wiki diff_drive_controller ROS 1](https://wiki.ros.org/diff_drive_controller) — cùng cách tách thành khớp bánh trái và bánh phải, viết cho ROS 1 và vẫn là bức tranh đúng.

Siegwart, Nourbakhsh và Scaramuzza, *Introduction to Autonomous Mobile Robots*, là bản xử lý dài bằng cả cuốn sách cho động học này. Dùng các liên kết phía trên cho những tham số bản ROS của các bạn thực sự đọc.
