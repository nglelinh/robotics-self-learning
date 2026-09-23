---
layout: post
title: "Encoder và đếm odometry thô"
chapter: "04"
order: 3
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter04
lesson_type: required
draft: false
---

Thời lượng: **75–90 phút**. Phần lớn thời gian là một vòng quay tay cho đúng vạch, rồi đổi số đếm đó ra mét.

## Mục tiêu học

Hết bài này, bạn nhìn hai sóng vuông của encoder quadrature (hai kênh lệch pha, thường gọi A và B) và chỉ được kênh nào lên trước, tức là phân biệt được tiến và lùi. Bạn không lấy số “PPR” trên trang bán làm chân lý cho đến khi tự đếm số xung trên một vòng trục ra của bánh, đúng cách giải mã mà firmware sẽ dùng. Bạn đổi số đếm thành cung tròn với bánh đường kính 65 mm, rồi từ quãng đường hai bánh suy ra một bước dead reckoning (ước lượng vị trí bằng cách cộng dồn): tâm trục đi được bao nhiêu mét, và hướng quay bao nhiêu radian. Hai số đó chính là phần lõi của `nav_msgs/Odometry` sau này.

## Kiến thức cần có

Bạn đã đếm được cạnh xung trên GPIO và in ra màn hình (Chương 03), và đã phân biệt được đĩa Hall trên hộp số TT vàng với đĩa xẻ rãnh (Bài 04-02). Encoder thô không phải thiết bị I2C của Bài 04-01; UART chỉ là đường đưa số đếm ra khỏi board. Dùng đồng hồ Chương 01 đo mức cao của encoder trước khi cho dây đó chạm GPIO. Bài này chưa cần ROS, cũng chưa cần cấp nguồn cho bánh.

## Vì sao bài này quan trọng với Capstone A và ROS

Capstone A ở Chương 07 là teleop robot vi sai qua cổng serial, hết thời gian im lặng thì dừng động cơ. Bản demo đó chạy được dù không có encoder. Nhật ký nghiệm thu chắc hơn nếu cùng lượt chạy đó có thêm số đếm bánh, vì “nó có chạy” trở thành một con số đem so với thước. Công thức hôm nay là công thức của dòng nhật ký đó.

`diff_drive_controller` không nghĩ ra một hình học mới. Firmware, hoặc hardware interface của ros2_control, đổi số đếm thành góc bánh bằng $$N$$, tức số xung trên một vòng sau khi giải mã. Controller đổi góc đó thành mét bằng tham số `wheel_radius` (chính là $$r$$ của bài này) và thành góc yaw bằng `wheel_separation` (khẩu độ $$b$$). Nó xuất `nav_msgs/Odometry`. Nhân đôi $$N$$ thì odometry báo một nửa hành lang dù bán kính đã đúng. `sensor_msgs/JointState` là cùng số đếm đó, viết dưới dạng vị trí bánh tính bằng radian. Lấy $$N$$ từ bánh đang cầm trên tay, không lấy từ tiêu đề sản phẩm.

![Hai kênh quadrature A và B: cạnh nào lên trước thì đó là chiều]({{ site.imgurl }}/generated/encoder_quadrature.png)

## Hai sóng vuông

Encoder quadrature phát hai sóng vuông A và B, lệch nhau khoảng một phần tư chu kỳ. Chiều quay là cạnh nào dẫn trước. Một quy ước bạn vẫn phải kiểm trên mạch của mình: A lên trong khi B còn thấp thì tính một bước tiến; B lên trong khi A còn thấp thì tính lùi. Đảo hai dây là đảo dấu. Đó là chuyện nối dây, không phải chuyện bộ lọc.

Một kênh đơn không có bạn đồng hành. Tốc độ suy từ chân đó chỉ đáng tin khi lệnh động cơ đã cho sẵn dấu, và nó nói dối khi bánh trôi hoặc trục giật ngược lúc phanh.

## Chữ “PPR” dễ hiểu nhầm

Có lúc PPR nghĩa là số chu kỳ trên một vòng của một kênh: một nhịp cao và một nhịp thấp, một rãnh. Có lúc nó nghĩa là số đếm sau khi giải mã. Giải mã bốn lần (4×) đếm mọi cạnh của cả hai kênh, nên

$$
N \approx 4 \times (\text{số chu kỳ trên một vòng của một kênh}).
$$

Nhiều động cơ TT vàng đặt đĩa từ trên trục motor, phía sau hộp số. Người bán hay ghi 11 xung nhân tỉ số hộp số, hoặc “số xung Hall trên một vòng trục” mà không nói trục nào. Mười một cạnh lên trên một vòng trục motor, đếm 1×, qua hộp số 1:48, cho

$$
N = 11 \times 48 = 528
$$

xung trên một vòng trục ra. Đem 11 thế vào công thức quãng đường thì mọi mét bạn công bố dài gấp 48 lần. $$N$$ đứng đắn là một vạch trên lốp, quay bằng tay, qua đúng bộ đếm mà code đang chạy.

## Quãng đường trên mỗi xung

Không trượt thì một vòng đưa vết tiếp xúc đi hết chu vi $$2\pi r$$:

$$
\Delta s = \frac{2\pi r}{N}\Delta c.
$$

Bánh đường kính 65 mm có $$r = 0{,}0325~\mathrm{m}$$ và chu vi

$$
2\pi r \approx 2 \times 3{,}1416 \times 0{,}0325 = 0{,}2042~\mathrm{m}.
$$

Nếu đây là đĩa rãnh đơn giản và firmware đếm $$N = 20$$ cạnh trên một vòng trục ra, một xung là

$$
\frac{0{,}2042}{20} = 0{,}01021~\mathrm{m} \approx 1{,}021~\mathrm{cm}.
$$

Một trăm bốn mươi xung tương ứng

$$
\Delta s = 140 \times 0{,}01021 \approx 1{,}43~\mathrm{m}.
$$

$$N = 20$$ là đĩa để học, không phải lời hứa của một tin đăng TT. Vòng quay tay của bạn in ra 360, 528 hay 1440 thì số đó thay cho 20.

## Một bước dead reckoning

Cùng một cặp công thức sẽ gặp lại ở Chương 06 và trong controller:

$$
\Delta s = \frac{\Delta s_r + \Delta s_l}{2}, \qquad \Delta \theta = \frac{\Delta s_r - \Delta s_l}{b}.
$$

$$b$$ là khoảng cách giữa hai vết bánh, không phải đường kính bánh. Với $$\Delta s_r = 0{,}10~\mathrm{m}$$, $$\Delta s_l = 0{,}06~\mathrm{m}$$ và $$b = 0{,}15~\mathrm{m}$$,

$$
\Delta s = \frac{0{,}10 + 0{,}06}{2} = 0{,}08~\mathrm{m}, \qquad \Delta \theta = \frac{0{,}04}{0{,}15} = 0{,}267~\mathrm{rad} \approx 15{,}3^\circ.
$$

Tâm trục bò 8 cm và quay khoảng 15 độ về phía bánh chậm hơn. Công thức không chứa trượt. Đảo A và B chỉ ở encoder bánh phải thì sổ ghi $$\Delta s_r = -0{,}10~\mathrm{m}$$ trong khi lốp đã đi tới. Bài tập bắt bạn tính xem sai dấu nặng đến đâu.

## Lab: một vòng, cầm trên tay

### An toàn

Lượt đếm không cấp điện cho motor. Bánh TT trên mặt bàn sẽ tự bò. Nếu bạn đã có driver và muốn thử chiều khi có điện, kê bánh lên không, xung thật ngắn, tay tránh nan hoa. Mức cao của Hall đo được 5 V thì phải có cầu chia 1 kΩ / 2 kΩ như echo ở Bài 04-02 trước khi chạm GPIO của ESP32. Đo mức cao trước.

### BOM

| Món | Vai trò |
|------|---------|
| Một động cơ hộp số có encoder, hoặc một đĩa rãnh rời | Trục bạn sẽ quay |
| ESP32 hoặc Pico | Bộ đếm cạnh |
| Bút | Vạch mốc trên lốp |
| Sổ | $$N$$, bán kính, mét trên mỗi xung |
| Driver và pin | Chỉ cho bước thử chiều tùy chọn, bánh trên không |

### Các bước

1. Đánh dấu lốp và một điểm tương ứng trên hộp số. Hai vạch đó là một vòng.
2. Không cấp điện motor. Xóa bộ đếm.
3. Quay trục ra bằng tay đúng một vòng, về lại vạch. Ghi số đếm. Làm lại hai lần. Ba số nên lệch nhau không quá một xung.
4. Số đó là $$N$$ của cách giải mã vừa chạy. Tính $$2\pi r / N$$ với đúng chiếc lốp đã đánh dấu. Con số 1,021 cm chỉ xuất hiện khi $$N = 20$$ và đường kính 65 mm.
5. Vẫn không cấp điện, xem kênh nào lên trước khi bạn quay lốp theo chiều robot sẽ tiến. Máy phân tích logic là đẹp nhất. In “A lên” và “B lên” là đủ. Chỉ một kênh thì ghi “dấu chỉ đến từ lệnh động cơ”.
6. Tùy chọn, bánh trên không: một nhịp có điện ngắn phải làm cùng kênh đó dẫn trước. Nếu không, đảo A và B trong sổ rồi thử lại một lần.

### Kết quả mong đợi

Ba vòng quay tay, một $$N$$ thống nhất, quãng đường trên mỗi xung tính bằng mét, và một câu nói kênh nào dẫn khi robot tiến. Dán khối đó vào `lab-notes.md`. Dòng kiểu “140 xung, khoảng 1,43 m” ở Chương 07 chỉ được viết khi $$N$$ đo được đúng là 20.

### Lỗi thường gặp

| Bạn thấy | Thường là |
|----------|-----------|
| Số đếm nhân đôi sau khi đổi chế độ giải mã | Đã chuyển từ 1× sang 2× hoặc 4× mà giữ $$N$$ cũ |
| Tin đăng ghi 40 PPR, quay tay được 20 | Trang bán đếm những cạnh mà code của bạn không đếm |
| Lệnh tiến làm số đếm giảm | A và B đảo, hoặc dây motor ngược; mỗi lần chỉ sửa một thứ |
| Bánh đứng yên mà số vẫn tăng | Dội xung, chân để nổi, hoặc không chung mass |
| Quãng đường dài gấp vài chục lần | $$N$$ là xung trên vòng trục motor; quên hộp số |

## Mua ở Việt Nam / Where to buy in Vietnam

Mua một cặp động cơ TT đã có encoder Hall, để hai bánh cùng một kiểu hộp số. Giá thay đổi.

| Món | Từ khóa | Khoảng giá (VND) | Thay thế |
|------|---------|------------------|----------|
| Động cơ TT có encoder Hall | `động cơ TT encoder Hall` | 40.000–90.000 một cái | N20 có encoder nếu lỗ bắt và trục (3 mm hoặc 4 mm) khớp khung |
| Đĩa rãnh và cặp quang | `đĩa encoder quang` | 15.000–40.000 | Đủ để học $$N$$, khó làm truyền động Capstone |
| 1 kΩ và 2 kΩ | `điện trở 1k 2k` | 10.000–20.000 một vỉ | Chỉ khi mức cao của Hall đo được 5 V |

- [Hshop: động cơ encoder](https://hshop.vn/search?q=dong%20co%20encoder)
- [Shopee: động cơ TT encoder](https://shopee.vn/search?keyword=dong%20co%20TT%20encoder)
- [Lazada: encoder Hall TT](https://www.lazada.vn/catalog/?q=encoder%20Hall%20TT)
- [Thế Giới IC: encoder](https://www.thegioiic.com/search?q=encoder)

Đọc kỹ vòng quay trong tin đăng là vòng của trục nào. Rồi kiểm bằng một vòng quay tay.

## Bài tập

Lấy $$r = 0{,}0325~\mathrm{m}$$ và chu vi $$\approx 0{,}2042~\mathrm{m}$$ nếu đề không nói khác.

1. $$N = 20$$ xung trên một vòng trục ra. Bánh lăn bao xa sau 140 xung?
2. Cùng firmware đó, quay tay một vòng được 20 xung, nhưng bạn gõ “40 PPR” của người bán vào công thức. Họ báo quãng đường bao nhiêu cho 140 xung, và quãng đường đúng là bao nhiêu?
3. Lốp thật sự đi $$\Delta s_r = 0{,}10~\mathrm{m}$$ và $$\Delta s_l = 0{,}06~\mathrm{m}$$, $$b = 0{,}15~\mathrm{m}$$. A và B của encoder phải bị đảo, sổ ghi $$-0{,}10~\mathrm{m}$$ và $$+0{,}06~\mathrm{m}$$. Tính $$\Delta s$$ và $$\Delta \theta$$ mà sổ báo, so với giá trị đúng $$0{,}08~\mathrm{m}$$ và $$0{,}267~\mathrm{rad}$$.
4. Một kênh đếm 80 cạnh lên lúc đi tới và 80 cạnh nữa lúc lăn về vạch xuất phát. Với kênh đó $$N = 20$$. Quadrature báo quãng đường thực bao nhiêu, và nếu cộng cả 160 cạnh như thể toàn đi tới thì được bao nhiêu?
5. Động cơ TT cho 11 cạnh lên trên một vòng trục motor, hộp số 1:48, code đếm các cạnh đó (1×) ở đầu ra gắn bánh. $$N$$ bằng bao nhiêu? Dùng 11 thì mọi quãng đường bị phóng bao nhiêu lần?

### Gợi ý đáp án

1. $$0{,}01021~\mathrm{m}$$ mỗi xung, nhân 140, được $$1{,}43~\mathrm{m}$$. 2. $$N = 40$$ báo $$0{,}715~\mathrm{m}$$, bằng một nửa của $$1{,}43~\mathrm{m}$$. 3. Sổ báo $$\Delta s = -0{,}02~\mathrm{m}$$ và $$\Delta \theta = -1{,}067~\mathrm{rad}$$ (khoảng $$-61^\circ$$), thay vì $$+0{,}08~\mathrm{m}$$ và $$+15{,}3^\circ$$. 4. Quadrature có tổng xung bằng 0 nên quãng đường thực bằng 0. Coi 160 cạnh là đi tới thì được $$1{,}63~\mathrm{m}$$. 5. $$N = 528$$. Dùng 11 thì mọi quãng đường dài gấp 48 lần.

## Đọc thêm

- [SparkFun: nối rotary encoder](https://learn.sparkfun.com/tutorials/rotary-encoder-breakout-hookup-guide/all) — cạnh nào dẫn trước, và vì sao một kênh chỉ là gợi ý tốc độ.
- [Pololu: cặp encoder từ](https://www.pololu.com/product/3081) — datasheet ghi số xung trên vòng trục motor; bạn vẫn phải nhân với hộp số.
- [`nav_msgs/Odometry`](https://docs.ros.org/en/humble/p/nav_msgs/msg/Odometry.html) — tư thế là tổng các bước dead reckoning như bước ở trên.
- [`diff_drive_controller`](https://control.ros.org/humble/doc/ros2_controllers/diff_drive_controller/doc/userdoc.html) — `wheel_radius` và `wheel_separation` là $$r$$ và $$b$$; $$N$$ nằm ở hardware interface đưa vị trí bánh vào controller.
