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

Thời lượng ước tính: **70–90 phút**, bao gồm thời gian đo trực tiếp trên khung xe 2WD thực tế hoặc đo trên bản vẽ đúng tỉ lệ nếu bộ kit chưa về tới xưởng.

## Mục tiêu học

Sau bài này, các bạn xác định được hai kích thước hình học mà robot vi sai thực sự sử dụng khi di chuyển: khổ vết (track width) $$b$$ đo giữa hai tâm vết tiếp xúc của lốp (không phải giữa hai vỏ động cơ) và bán kính lăn $$r$$ tính từ phép lăn đúng một vòng khi lốp đã chịu tải. Từ một cặp vận tốc bánh xe, các bạn tính được vận tốc tịnh tiến và vận tốc góc quay của thân robot, biết cách bố trí pin sao cho bánh caster luôn bám sàn, và ghi lại $$b$$, $$r$$ theo đơn vị milimét để bài lắp ráp ở Chương 07 cũng như `diff_drive_controller` trong ROS sử dụng thống nhất.

## Kiến thức cần có

Các bạn biết đọc thước milimét và không nhầm lẫn giữa milimét với centimét khi ghi chép. Các bạn đã hiểu động cơ giảm tốc một chiều làm quay bánh xe (Chương 05) và xung encoder về sau sẽ đại diện cho góc quay của trục (Chương 04). Chưa cần cài đặt ROS; nếu chưa có khung xe trên bàn, một bản vẽ đúng tỉ lệ vẫn đủ để thực hành, miễn là ghi chú rõ số liệu lấy từ bản vẽ.

## Vì sao bài này quan trọng với Capstone A và ROS

Capstone A sử dụng đúng cấu hình khung này: hai bánh chủ động nằm trên cùng một trục và một bánh caster (hoặc đế trượt) giữ điểm tựa thứ ba để đầu khung không cày xuống sàn. Chương 08 sẽ trình bày đầy đủ mô hình động học. Trên ROS, bộ điều khiển `diff_drive_controller` chuyển đổi lệnh `cmd_vel` thành vận tốc hai bánh, đồng thời tính ngược odometry từ xung encoder bằng chính hai tham số $$b$$ và $$r$$ đo hôm nay. Tệp URDF ở Chương 09–10 cũng định vị các khâu bánh xe theo các kích thước này.

Nếu giá trị $$b$$ bị sai, sai số sẽ lập tức biểu hiện trên quỹ đạo thực tế: khi bạn ra lệnh đi thẳng, robot lại chạy theo đường cong vì bộ điều khiển liên tục hiệu chỉnh theo một hình học không đúng với phần cứng. Vì vậy, hãy đo cẩn thận ngay từ đầu, ghi rõ đơn vị milimét vào `lab-notes.md` và tránh thói quen làm tròn ước lượng kiểu “khoảng 15 cm” khi chuyển sang các bài sau. Các con số ước lượng đại khái là nguyên nhân phổ biến nhất gây lệch bản đồ ở những nhóm mới lắp khung robot.

## Hai bánh, một caster, hai chiều dài

Quan sát tấm khung từ phía trên: động cơ trái và động cơ phải hướng trục ra hai bên, hai bánh xe nằm trên cùng một đường trục chung. Robot không có cơ cấu lái vô-lăng mà chuyển hướng bằng cách tạo chênh lệch vận tốc giữa hai bánh. Điểm đỡ thứ ba là bánh caster xoay tự do hoặc đế trượt nhẵn, giúp mũi khung không chạm sàn. Capstone A dùng bánh caster xoay vì đế trượt tuy chấp nhận được trên xe nhẹ chạy trong nhà nhưng dễ gây ồn và để lại vết xước trên nền gạch men.

Khổ vết (track width) $$b$$ là khoảng cách giữa hai tâm vết tiếp xúc — tức giữa hai điểm chính giữa mặt lốp chạm đất. Khoảng cách giữa hai vỏ động cơ chỉ là kích thước lắp đặt trên bản vẽ tấm khung, không dùng trong phương trình động học. Nếu đo từ mép ngoài lốp trái sang mép ngoài lốp phải, bạn đã vô tình cộng thêm bề rộng một mặt lốp vào $$b$$. Hãy đặt khung ở trạng thái chịu tải thực tế (có lắp pin), trượt đầu thước vào chính giữa mỗi mặt lốp rồi ghi kết quả bằng milimét. Dưới tải trọng, lốp hơi phình ngang nên khổ vết khi chưa lắp pin và khi đã lắp pin có thể lệch nhau vài milimét.

Bán kính lăn $$r$$ là bán kính hiệu dụng khi cao su bị nén dưới trọng lượng xe. Con số ghi trên túi linh kiện chỉ là đường kính tự do khi bánh chưa chịu tải. Khi lắp pin, lốp lún nhẹ làm bán kính giảm xuống. Để đo chính xác, hãy đánh dấu một điểm trên lốp, lăn đúng một vòng trên mặt giấy, đo chiều dài quãng đường $$s$$ rồi tính:

$$
r = \frac{s}{2\pi}.
$$

Chẳng hạn, một bánh ghi nhãn đường kính 65 mm nhưng lăn một vòng được 196 mm sẽ có bán kính lăn:

$$
r = \frac{196}{2\pi} \approx 31.2\ \text{mm},
$$

nhỏ hơn đáng kể so với một nửa đường kính danh nghĩa (32,5 mm). Mức chênh lệch vài phần trăm này sẽ tích lũy trên mỗi mét di chuyển, khiến quãng đường odometry và bản đồ dài hơn hoặc ngắn hơn thực tế vài centimét. Khi đo, hãy đè lên bánh một lực tương đương tải trọng thực tế, hoặc lăn thẳng cả khung xe nếu hai bánh quay tự do. Thực hiện tương tự cho bánh còn lại; hai bán kính nên khớp nhau trong phạm vi 1 mm. Nếu lệch nhiều hơn, nhiều khả năng một lốp đang lắp lệch tâm trên trục, khiến robot tự lệch hướng khi chạy thẳng ngay cả khi firmware không có lỗi.

Tam giác đỡ của khung xe được tạo bởi hai vết tiếp xúc của bánh chủ động và điểm chạm đất của bánh caster. Đường thẳng đứng đi qua trọng tâm của robot phải rơi vào bên trong tam giác này. Nếu đặt pin dựng đứng phía sau trục bánh hoặc nhô ra ngoài phạm vi tam giác đỡ, mũi xe dễ bị bốc đầu khi tăng tốc; ngược lại, nếu bánh caster gần như không chịu tải, nó sẽ rung lắc vì khoảng đuôi (trail) không ổn định. Hãy đặt khối pin thấp, nằm giữa hai bánh hoặc hơi dịch về phía trước trục, sau đó dùng tay ấn nhẹ vào giá đỡ caster để kiểm tra: bánh caster cần chịu một phần trọng lượng ổn định trong khi cả hai bánh chủ động vẫn bám chắc mặt sàn. Nếu ấn nhẹ vào caster mà mũi xe nhấc lên, pin đang đặt quá lùi về sau; nếu caster không chịu lực, pin đang đặt quá cao hoặc quá lệch về phía trước.

## Ví dụ tính tay

Xét khung xe có $$b = 0.15$$ m, vận tốc thẳng tại vết tiếp xúc của bánh trái là $$v_l = 0.20$$ m/s và bánh phải là $$v_r = 0.30$$ m/s (chiều dương là chiều tiến). Vận tốc tịnh tiến $$v$$ và vận tốc góc $$\omega$$ của thân robot là:

$$
v = \frac{v_r + v_l}{2} = \frac{0.30 + 0.20}{2} = 0.25\ \text{m/s},
$$

$$
\omega = \frac{v_r - v_l}{b} = \frac{0.30 - 0.20}{0.15} = 0.667\ \text{rad/s}.
$$

Trong một giây, trung điểm trục bánh đi được 25 cm theo hướng mũi xe, đồng thời hướng mũi xoay một góc $$0.667 \times 180/\pi \approx 38^\circ$$. Theo quy ước này, $$\omega > 0$$ khi bánh phải nhanh hơn bánh trái, tức robot quay sang trái.

Nếu cùng cặp vận tốc bánh đó nhưng khổ vết bị nhập sai thành 0,18 m (do đo qua hai vỏ động cơ), vận tốc góc tính ra sẽ giảm xuống chỉ còn $$0.556$$ rad/s. Bộ điều khiển tin theo giá trị 0,18 m sẽ tạo ra độ chênh vận tốc sai để bù cho góc quay thực tế (ứng với $$b = 0.15$$ m), khiến robot chạy thành đường cong dù lệnh `cmd_vel` yêu cầu đi thẳng. Vì vậy, từng milimét đo được trên thước quan trọng hơn nhiều so với ước lượng cảm tính “khung cỡ này chắc khoảng 15 cm”.

![Khổ vết giữa hai tâm tiếp xúc, và vòng lăn cho bán kính lăn]({{ site.imgurl }}/generated/chassis_measures.png)

![Vận tốc thân và vận tốc góc vẽ từ hai vận tốc bánh]({{ site.imgurl }}/generated/diff_drive_kinematics.png)

Hình thứ nhất minh họa cách đặt thước: $$b$$ đo giữa hai tâm mặt lốp và $$r$$ lấy từ bán kính lốp khi đã chịu nén. Hình thứ hai biểu diễn trực quan hai phương trình vận tốc: hai vectơ vận tốc tiến bằng nhau cho $$\omega = 0$$, còn khi hai vectơ khác nhau, robot quay quanh một tâm nằm trên đường kéo dài của trục bánh. Chương 08 sẽ định nghĩa rõ tâm quay tức thời và bán kính quỹ đạo này. Trong bài hôm nay, các bạn chỉ cần ghi đầy đủ $$b$$, $$r$$, $$v$$ và $$\omega$$ kèm đơn vị vào sổ tay, đồng thời nêu rõ số liệu đo từ phần cứng hay bản vẽ.

## Lab: đo b và r

### An toàn

Đảm bảo đã tắt nguồn hoàn toàn. Nếu pin đang gắn sẵn trên khung, hãy tháo pin trước khi đưa thước kim loại lại gần tấm khung để tránh làm chập các đầu dây động cơ. Bài thực hành này không cần cấp điện và không có trục quay dưới điện áp; không cần cấp nguồn để kiểm tra độ tròn của bánh xe.

### BOM

| Hạng mục | Vai trò |
|------|------|
| Khung 2WD, hoặc bản vẽ tỉ lệ của bộ kit đã đặt | Vật được đo |
| Thước hoặc thước kẹp, đơn vị milimét | Khổ vết |
| Giấy, băng dính, bút | Lăn một vòng để lấy $$r$$ |
| `lab-notes.md` | Các số Chương 07 và ROS sẽ chép |

### Các bước

1. Đặt khung xe lên mặt bàn phẳng đúng tư thế vận hành. Nếu đã có pin, đặt pin vào vị trí dự kiến trên khung.
2. Đánh dấu tâm mặt lốp ở cả hai bánh rồi đo khổ vết $$b$$ giữa hai dấu này. Ghi kết quả theo milimét; đo riêng khoảng cách giữa hai vỏ động cơ để đối chiếu và ghi chú rõ là không đưa vào bộ điều khiển.
3. Đánh dấu một điểm trên lốp và điểm tương ứng trên tờ giấy. Lăn bánh đúng một vòng dưới tải trọng xấp xỉ tải thực tế của bánh đó, rồi đo chiều dài quãng đường $$s$$.
4. Tính $$r = s / (2\pi)$$, làm tròn đến một chữ số thập phân theo milimét. Lặp lại quy trình với bánh còn lại.
5. Dùng tay ấn nhẹ tại vị trí bánh caster để kiểm tra độ chịu tải. Nếu chưa có pin, phác thảo vị trí đặt pin sao cho trọng tâm nằm gọn trong tam giác đỡ.
6. Nếu bộ kit chưa về, thực hiện các bước 2–5 trên bản vẽ đúng tỉ lệ và ghi rõ tiêu đề: “bản vẽ, chưa phải phần cứng”.

### Kết quả mong đợi

Một cặp số liệu có ghi ngày trong `lab-notes.md` (ví dụ $$b = 148$$ mm và $$r = 31.2$$ mm), trong đó bán kính lăn $$r$$ của hai bánh chênh lệch không quá 1 mm. Ghi chú nêu rõ nguồn đo (phần cứng hay bản vẽ), và khoảng cách hai vỏ động cơ được tách riêng, không nhầm lẫn với $$b$$.

### Lỗi thường gặp

| Chuyện gì sai | Hệ quả về sau |
|-----------------|-------------------|
| $$b$$ đo giữa hai thân động cơ | `cmd_vel` đi thẳng lại chạy thành vòng tròn |
| $$r$$ chép bằng nửa đường kính trên nhãn | Quãng đường odometry dài hoặc ngắn trên mỗi mét |
| Pin kê phía sau trục | Bốc đầu, hoặc bánh caster lắc |
| Bán kính trái và phải lệch vài milimét | Lệnh đi thẳng đã quay ngang |

## Mua ở Việt Nam / Where to buy in Vietnam

Nên mua sẵn khung mica 2WD đã cắt gia công để kịp lắp ráp Capstone A trong tháng này; các giá đỡ nhỏ có thể in 3D sau ở Bài 06. Tấm khung có sẵn rãnh lắp động cơ TT và lỗ bắt bánh caster là bộ kit phổ biến trên các sàn thương mại điện tử. Lưu ý rằng bánh cao su và bánh caster thường được bán tách rời trong cùng tin đăng, nên cần kiểm tra kỹ thay vì mặc định chúng có sẵn trong hộp khung.

| Mua gì | Từ khóa | Khoảng giá (VND) | Ghi chú |
|------|----------|------------------|-------|
| Khung 2WD | `khung xe robot 2 bánh` | 80.000–200.000 | Tấm mica, rãnh động cơ, lỗ caster |
| Bánh cao su | `bánh xe cao su 65mm` | 15.000–45.000 mỗi cái | Đường kính trên nhãn chỉ là điểm bắt đầu của phép lăn, không phải $$r$$ |
| Bánh caster xoay | `bánh caster robot` | 12.000–40.000 | Bánh xoay có đuôi cho Capstone A |

Tìm trên các trang sau (vì đường dẫn cửa hàng và giá bán thay đổi theo thời điểm):

- [Hshop](https://hshop.vn/search?q=khung+xe+robot)
- [Shopee](https://shopee.vn/search?keyword=khung%20xe%20robot%202%20b%C3%A1nh)
- [Lazada](https://www.lazada.vn/catalog/?q=khung%20xe%20robot%202%20b%C3%A1nh)
- [Thế Giới IC](https://www.thegioiic.com/search?q=khung%20xe%20robot)

Trước khi thanh toán, hãy xác nhận rãnh bắt động cơ khớp với hộp giảm tốc TT và bánh caster đã đi kèm trong bộ hoặc được đặt mua cùng đơn. Một tấm khung không có lỗ gắn caster sẽ khiến phần mũi của Capstone A cày trực tiếp xuống sàn.

## Video tham khảo

- **Xem trước:** [Differential Drive & Odometry Explained: How It Works](https://www.youtube.com/watch?v=2QE3LG5h2tw) — Netizen Robotics, tiếng Anh. Trình bày cấu tạo hai bánh chủ động và khoảng cách giữa hai bánh của khung vi sai mà bài này yêu cầu đo.
- [PART1: Building Low-Cost Differential Wheeled Robot For Machine Learning, SLAM, and ROS](https://www.youtube.com/watch?v=RsZBxfpcLu8) — Aleksandar Haber PhD, tiếng Anh. Quá trình dựng một khung robot giá thấp; hãy đối chiếu vị trí đặt động cơ, bánh xe và pin với sơ đồ trong bài.

## Bài tập

1. Phép lăn một vòng cho quãng đường $$s = 200$$ mm. Tính bán kính lăn $$r$$ theo milimét, làm tròn một chữ số thập phân.
2. Với $$b = 0.16$$ m, $$v_l = 0.25$$ m/s và $$v_r = 0.25$$ m/s, hãy tính $$v$$ và $$\omega$$. Robot chuyển động như thế nào?
3. Giữ nguyên $$b = 0.16$$ m, với $$v_l = 0.10$$ m/s và $$v_r = 0.30$$ m/s, hãy tính $$v$$ và $$\omega$$.
4. Một sinh viên đo từ mép ngoài lốp trái đến mép ngoài lốp phải được 180 mm, biết mỗi mặt lốp rộng 20 mm. Giá trị $$b$$ nào cần nhập vào bộ điều khiển?
5. Khối pin được đặt trên một giá cao phía sau trục bánh, khiến bánh caster nhấc khỏi sàn khi đẩy robot tiến tới. Cần dời pin đến đâu, và nếu giữ nguyên vị trí đó thì lệnh đi thẳng trong ROS sẽ tạo ra quỹ đạo gì?

### Gợi ý đáp án

1. $$r = 200/(2\pi) \approx 31.8$$ mm.
2. $$v = 0.25$$ m/s và $$\omega = 0$$, robot đi thẳng.
3. $$v = 0.20$$ m/s và $$\omega = (0.30-0.10)/0.16 = 1.25$$ rad/s, robot quay sang trái vì bánh phải chạy nhanh hơn.
4. Mỗi tâm tiếp xúc nằm lùi vào trong bằng một nửa bề rộng mặt lốp so với mép ngoài, do đó cần trừ đúng một bề rộng mặt lốp: $$b = 180 - 20 = 160$$ mm.
5. Cần dời pin xuống thấp và đưa vào bên trong tam giác đỡ, hơi dịch về phía trước trục nếu bánh caster đang quá nhẹ tải. Nếu giữ nguyên pin trên giá cao phía sau, caster sẽ mất tải, hướng mũi xe không ổn định và lệnh đi thẳng sẽ tạo ra quỹ đạo cong trên sàn.

## Đọc thêm

- [diff_drive_controller trong ros2_controllers](https://github.com/ros-controls/ros2_controllers/tree/master/diff_drive_controller) — khoảng cách hai bánh và bán kính bánh là các tham số trực tiếp của gói này. Tài liệu bộ điều khiển bản Jazzy được sinh từ cây mã nguồn này; chỉ mục gói nằm tại [docs.ros.org/en/jazzy](https://docs.ros.org/en/jazzy/index.html).
- [Wiki diff_drive_controller ROS 1](https://wiki.ros.org/diff_drive_controller) — giải thích tên tham số bằng ngôn ngữ trực quan. Dù là trang của ROS 1, mô hình hình học vẫn giống hệt ROS 2.
- [Thiết lập odometry trên Nav2](https://navigation.ros.org/setup_guides/odom/setup_odom.html) — minh họa cách sai số odometry ảnh hưởng khi chuyển từ điều khiển tay (teleop) sang điều hướng tự hành.
