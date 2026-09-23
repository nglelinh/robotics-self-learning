---
layout: post
title: "Giải phẫu khung robot vi sai"
chapter: "06"
order: 1
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter06
lesson_type: required
draft: false
---

Thời lượng ước tính: **70–90 phút**, tính cả lúc lấy thước trên khung 2WD thật, hoặc đo trên bản vẽ đúng tỉ lệ nếu bộ kit chưa về tới xưởng.

## Mục tiêu học

Hết bài này, các bạn chỉ được hai chiều dài mà robot vi sai thực sự dùng khi lăn. Khổ vết (track width) $$b$$ lấy giữa hai tâm vết tiếp xúc của lốp, không lấy giữa hai vỏ động cơ. Bán kính lăn $$r$$ lấy từ phép lăn đúng một vòng, sau khi cao su đã chịu tải. Từ một cặp vận tốc bánh, các bạn tính được vận tốc thân và vận tốc góc quay, đặt pin sao cho bánh caster vẫn bám sàn, rồi ghi $$b$$ và $$r$$ bằng milimét để bài lắp Chương 07 và `diff_drive_controller` trên ROS kế thừa đúng hình học ấy.

## Kiến thức cần có

Các bạn đọc được thước milimét và phân biệt được milimét với centimét khi ghi sổ. Các bạn đã biết động cơ giảm tốc một chiều quay bánh xe (Chương 05), và biết xung encoder về sau sẽ đứng thay cho góc quay của trục (Chương 04). Chưa cần cài ROS. Nếu khung chưa có trên bàn, một bản vẽ tỉ lệ cẩn thận vẫn đủ để làm lab, miễn là ghi chú nói rõ đó là bản vẽ.

## Vì sao bài này quan trọng với Capstone A và ROS

Capstone A chính là khung này: hai bánh chủ động nằm trên một đường trục, cộng một bánh caster hoặc một đế trượt giữ góc thứ ba không cày sàn. Chương 08 sẽ khai triển động học đầy đủ. Bộ điều khiển các bạn gặp trên đường ROS, `diff_drive_controller`, đổi `cmd_vel` thành hai lệnh bánh, rồi đổi xung encoder trở lại thành odometry bằng đúng $$b$$ và $$r$$ đo hôm nay. URDF ở Chương 09–10 đặt khâu bánh bằng những chiều dài ấy. Một $$b$$ sai không nằm im trong file tham số. Nó hiện ra thành đường tròn khi các bạn ra lệnh đi thẳng, vì bộ điều khiển suốt quãng đường “sửa” một cú quay mà hình học đã bịa sẵn. Đo một lần, ghi milimét vào `lab-notes.md`, và từ chối làm tròn thành “khoảng 15 cm” khi sang bài sau. Con số tròn trong đầu là nguồn lệch bản đồ hay gặp nhất của nhóm sinh viên cơ khí mới lắp khung.

## Hai bánh, một caster, hai chiều dài

Nhìn tấm khung từ phía trên. Động cơ trái và động cơ phải quay mặt ra ngoài, hai lốp ngồi trên một đường trục chung. Robot không có vô-lăng. Nó lái bằng cách cho hai lốp đi với vận tốc khác nhau. Điểm đỡ thứ ba, một bánh caster xoay hoặc một đế trượt nhẵn, ngăn mũi tấm cày xuống sàn. Capstone A dùng bánh caster, tức bánh tự do có chốt xoay. Đế trượt chấp nhận được trên tấm nhỏ chạy trong nhà, và sẽ ồn, để lại vết, trên nền gạch men.

Khổ vết (track width) $$b$$ là khoảng cách giữa hai tâm vết tiếp xúc, tức giữa hai miếng cao su thực sự chạm đất. Khe giữa hai thân động cơ là kích thước lắp cho bản vẽ tấm. Động học không dùng số đó. Nếu đo từ mép ngoài lốp trái đến mép ngoài lốp phải, các bạn đã cộng thêm bề rộng mặt lốp vào $$b$$. Trượt mỗi đầu thước vào giữa mặt lốp, robot chịu tải đúng cách nó sẽ lăn, rồi ghi milimét. Tải làm lốp phình ngang một chút, nên khổ vết khi khung không có pin và khổ vết khi pin đã ngồi đúng chỗ không trùng nhau từng milimét.

Bán kính lăn $$r$$ là bán kính mà sàn nhìn thấy sau khi cao su bị nén. Con số in trên túi bánh là đường kính tự do, đo khi bánh chưa đè sàn. Dưới pin, lốp lún, bán kính co lại. Đánh dấu lốp, lăn đúng một vòng trên giấy, đo chiều dài quãng đường $$s$$, rồi tính

$$
r = \frac{s}{2\pi}.
$$

Một bánh ghi nhãn 65 mm mà lăn được 196 mm trong một vòng có

$$
r = \frac{196}{2\pi} \approx 31.2\ \text{mm},
$$

trong khi một nửa nhãn là 32.5 mm. Khoảng lệch ấy là vài phần trăm trên mỗi mét mà odometry sẽ khai. Đi một mét thật, bản đồ có thể dài thêm hoặc ngắn đi vài centimét, và lỗi ấy cộng dồn. Hãy đè bánh bằng vật gần bằng phần tải của nó, hoặc lăn cả khung đi thẳng nếu hai bánh quay tự do. Làm lại với lốp kia. Hai bán kính nên khớp nhau trong khoảng một milimét. Lệch hơn thế nghĩa là một lốp ngồi lệch trên trục, và lệnh đi thẳng đã bắt đầu quay ngang trước khi firmware có lỗi.

Tam giác đỡ là hai vết tiếp xúc cộng điểm chạm của bánh caster. Đường thẳng đứng qua trọng tâm phải rơi vào trong tam giác ấy. Pin dựng đứng phía sau trục, hoặc cục pin treo thò ra ngoài bánh, đẩy điểm ấy ra khỏi tam giác. Mũi bốc đầu khi tăng tốc, hoặc bánh caster gần như không chịu tải sẽ lắc vì khoảng đuôi của nó không bao giờ ổn định. Đặt cục pin thấp, giữa hai bánh hoặc hơi phía trước trục, rồi ấn giá đỡ caster: nó phải gánh một phần trọng lượng ổn định trong khi cả hai bánh chủ động vẫn bám sàn. Nếu ấn caster mà mũi nhấc hẳn, pin đang quá về phía sau. Nếu ấn caster mà nó không chịu lực, pin đang quá về phía trước hoặc quá cao.

## Ví dụ tính tay

Lấy $$b = 0.15$$ m, $$v_l = 0.20$$ m/s và $$v_r = 0.30$$ m/s. Vận tốc bánh là vận tốc thẳng của vết tiếp xúc, chiều dương là tiến. Vận tốc thân và vận tốc góc là

$$
v = \frac{v_r + v_l}{2} = \frac{0.30 + 0.20}{2} = 0.25\ \text{m/s},
$$

$$
\omega = \frac{v_r - v_l}{b} = \frac{0.30 - 0.20}{0.15} = 0.667\ \text{rad/s}.
$$

Trong một giây, trung điểm trục đi 25 cm dọc theo hướng mũi, và hướng mũi đổi $$0.667 \times 180/\pi \approx 38^\circ$$. Ở quy ước này, $$\omega$$ dương nghĩa là bánh phải nhanh hơn, nên robot quay trái khi “trái” và “phải” khớp với mũi xe. Nếu cùng cặp vận tốc bánh mà khổ vết bị ghi là 0.18 m, vì ai đó đo qua vỏ động cơ, vận tốc góc báo về tụt xuống $$0.556$$ rad/s. Bộ điều khiển tin 0.18 m sẽ ra lệnh một độ chênh vận tốc bánh để hủy cú quay mà robot thật, với $$b = 0.15$$ m, đang thực hiện. Quỹ đạo trên sàn khép thành vòng tròn dù `cmd_vel` chỉ xin đi thẳng. Đó là lý do milimét trên thước quan trọng hơn cảm giác “khung cỡ này thì khoảng 15 cm”.

![Khổ vết giữa hai tâm tiếp xúc, và vòng lăn cho bán kính lăn]({{ site.imgurl }}/generated/chassis_measures.png)

![Vận tốc thân và vận tốc góc vẽ từ hai vận tốc bánh]({{ site.imgurl }}/generated/diff_drive_kinematics.png)

Hình thứ nhất là hình thước: $$b$$ từ tâm mặt lốp đến tâm mặt lốp, $$r$$ từ lốp đã nén. Hình thứ hai là hình vận tốc đứng sau hai phương trình. Hai mũi tên tiến bằng nhau cho $$\omega = 0$$. Hai mũi tên lệch nhau làm robot quay quanh một điểm vẫn nằm trên đường trục bánh. Chương 08 sẽ đặt tên điểm ấy và bán kính quay. Hôm nay các bạn chỉ cần ghi $$b$$, $$r$$, $$v$$ và $$\omega$$ vào sổ, kèm đơn vị, kèm câu nói số lấy từ phần cứng hay từ bản vẽ.

## Lab: đo b và r

### An toàn

Nguồn tắt. Nếu pin đã buộc sẵn trên khung, tháo pin trước khi thước kim loại đi ngang tấm, kẻo đầu dây động cơ chập vào thước. Lab này không có trục quay dưới điện áp. Không cần cấp nguồn để “xem bánh có tròn không”.

### BOM

| Hạng mục | Vai trò |
|------|------|
| Khung 2WD, hoặc bản vẽ tỉ lệ của bộ kit đã đặt | Vật được đo |
| Thước hoặc thước kẹp, đơn vị milimét | Khổ vết |
| Giấy, băng dính, bút | Lăn một vòng để lấy $$r$$ |
| `lab-notes.md` | Các số Chương 07 và ROS sẽ chép |

### Các bước

1. Đặt khung lên bàn phẳng đúng tư thế nó sẽ lăn. Đặt pin vào chỗ dự định nếu pin đã có.
2. Đánh dấu tâm mỗi mặt lốp. Đo $$b$$ giữa hai dấu ấy. Ghi milimét, và ghi bên cạnh khe giữa hai vỏ động cơ mà các bạn cố ý không đưa vào bộ điều khiển.
3. Đánh dấu một lốp và tờ giấy. Lăn đúng một vòng dưới khoảng phần tải của bánh ấy. Đo $$s$$.
4. Tính $$r = s / (2\pi)$$ và giữ một chữ số thập phân theo milimét. Lặp lại với bánh kia.
5. Ấn tại bánh caster. Ghi xem nó có chịu tải không. Nếu pin còn trong hộp, phác chỗ pin phải ngồi để khối lượng nằm trong tam giác đỡ.
6. Nếu kit chưa về, làm bước 2–5 trên bản vẽ tỉ lệ cẩn thận và đặt tiêu đề ghi chú là “bản vẽ, chưa phải phần cứng.”

### Kết quả mong đợi

Một cặp số có ngày trong `lab-notes.md`, ví dụ $$b = 148$$ mm và $$r = 31.2$$ mm, hai bánh khớp $$r$$ trong khoảng 1 mm. Ghi chú nói rõ số lấy từ phần cứng hay từ bản vẽ. Khe vỏ động cơ được ghi riêng, không bị trộn vào $$b$$.

### Lỗi thường gặp

| Chuyện gì sai | Hệ quả về sau |
|-----------------|-------------------|
| $$b$$ đo giữa hai thân động cơ | `cmd_vel` đi thẳng lại chạy thành vòng tròn |
| $$r$$ chép bằng nửa đường kính trên nhãn | Quãng đường odometry dài hoặc ngắn trên mỗi mét |
| Pin kê phía sau trục | Bốc đầu, hoặc bánh caster lắc |
| Bán kính trái và phải lệch vài milimét | Lệnh đi thẳng đã quay ngang |

## Mua ở Việt Nam / Where to buy in Vietnam

Mua khung mica 2WD đã gia công để Capstone A lắp được trong tháng này. Giá đỡ nhỏ thì in sau, ở Bài 06. Tấm có rãnh động cơ TT và lỗ bánh caster là bộ kit sinh viên thường gặp trên các sàn. Bánh cao su và bánh caster thường là dòng hàng riêng trên cùng một tin đăng, đừng giả định chúng đã nằm trong hộp khung.

| Mua gì | Từ khóa | Khoảng giá (VND) | Ghi chú |
|------|----------|------------------|-------|
| Khung 2WD | `khung xe robot 2 bánh` | 80.000–200.000 | Tấm mica, rãnh động cơ, lỗ caster |
| Bánh cao su | `bánh xe cao su 65mm` | 15.000–45.000 mỗi cái | Đường kính trên nhãn chỉ là điểm bắt đầu của phép lăn, không phải $$r$$ |
| Bánh caster xoay | `bánh caster robot` | 12.000–40.000 | Bánh xoay có đuôi cho Capstone A |

Tìm trên các trang sau, vì đường dẫn cửa hàng đổi và giá chợ động:

- [Hshop](https://hshop.vn/search?q=khung+xe+robot)
- [Shopee](https://shopee.vn/search?keyword=khung%20xe%20robot%202%20b%C3%A1nh)
- [Lazada](https://www.lazada.vn/catalog/?q=khung%20xe%20robot%202%20b%C3%A1nh)
- [Thế Giới IC](https://www.thegioiic.com/search?q=khung%20xe%20robot)

Trước khi thanh toán, kiểm tra rãnh động cơ khớp hộp giảm tốc TT, và bánh caster đã gồm trong kit hoặc được bán ngay cạnh tấm. Một tấm đẹp mà không có lỗ caster sẽ biến Capstone A thành xe cày mũi.

## Bài tập

1. Phép lăn cho $$s = 200$$ mm. Tính $$r$$ bằng milimét, lấy một chữ số thập phân.
2. Với $$b = 0.16$$ m, $$v_l = 0.25$$ m/s và $$v_r = 0.25$$ m/s, tìm $$v$$ và $$\omega$$. Robot làm gì?
3. Cùng $$b$$, với $$v_l = 0.10$$ m/s và $$v_r = 0.30$$ m/s. Tìm $$v$$ và $$\omega$$.
4. Một bạn đo từ mép ngoài lốp trái đến mép ngoài lốp phải được 180 mm. Mỗi mặt lốp rộng 20 mm. $$b$$ nào thuộc về bộ điều khiển?
5. Cục pin ngồi trên một tháp phía sau trục, và bánh caster nhấc lên khi các bạn đẩy robot về phía trước. Pin phải chuyển đi đâu, và lệnh ROS đi thẳng sẽ vẽ quỹ đạo gì nếu để nguyên tháp?

### Gợi ý đáp án

1. $$r = 200/(2\pi) \approx 31.8$$ mm. 2. $$v = 0.25$$ m/s và $$\omega = 0$$, robot đi thẳng. 3. $$v = 0.20$$ m/s và $$\omega = (0.30-0.10)/0.16 = 1.25$$ rad/s, quay trái khi bánh phải là bánh nhanh. 4. Mỗi tâm tiếp xúc nằm vào trong nửa bề rộng mặt lốp so với mặt ngoài, nên trừ đúng một bề rộng mặt lốp: $$b = 160$$ mm. 5. Chuyển pin xuống thấp và vào trong tam giác đỡ, hơi phía trước trục nếu caster đang nhẹ. Để nguyên trên tháp thì caster mất tải, hướng mũi lang thang, và lệnh đi thẳng nhìn trên sàn thành đường cong.

## Đọc thêm

- [diff_drive_controller trong ros2_controllers](https://github.com/ros-controls/ros2_controllers/tree/master/diff_drive_controller) — khoảng cách hai bánh và bán kính bánh là tham số của gói này. Tài liệu bộ điều khiển Jazzy được sinh từ cây mã ấy; chỉ mục gói cũng nằm dưới [docs.ros.org/en/jazzy](https://docs.ros.org/en/jazzy/index.html).
- [Wiki diff_drive_controller ROS 1](https://wiki.ros.org/diff_drive_controller) — tên tham số viết bằng lời thường. Trang thuộc ROS 1; hình học nó hỏi chính là hình học ROS 2 vẫn dùng.
- [Thiết lập odometry trên Nav2](https://navigation.ros.org/setup_guides/odom/setup_odom.html) — nguồn odometry xấu hiện ra thế nào khi các bạn rời teleop và yêu cầu robot dẫn đường.
