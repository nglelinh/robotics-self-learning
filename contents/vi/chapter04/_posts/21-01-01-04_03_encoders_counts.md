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

Thời lượng: **75–90 phút**. Phần lớn thời gian dành cho việc tự quay bánh bằng tay đúng một vòng để đo số xung thực tế, rồi quy đổi sang quãng đường theo mét.

Nếu bạn nhắm mắt bước đi trong phòng tối, làm sao bạn biết mình đã đi được bao xa? Bạn đếm số bước chân của chính mình! Với robot di động, **encoder** gắn sau đuôi trục động cơ chính là "bộ đếm bước chân" cơ điện tử đó: mỗi khi bánh xe quay thêm một góc nhỏ li ti, encoder phát ra một xung điện để vi điều khiển cộng dồn thành quãng đường và vận tốc (**odometry**). Tuy nhiên, giống như việc đi trên sàn trơn khiến số bước chân không còn khớp với quãng đường thực, hiểu sâu về encoder nghĩa là nắm cả độ phân giải xung lẫn nguyên nhân khiến sai số odometry tích lũy dần theo thời gian.

## Kiến thức cần nhớ: Từ xung vuông cầu phương đến odometry bánh xe

### 1. Giải mã cầu phương (Quadrature Decoding 4×) và chiều quay
Một encoder quang học hoặc từ tính (Hall) chuẩn có hai kênh **A** và **B** lệch pha nhau đúng $$90^\circ$$ (một phần tư chu kỳ). Nếu chỉ đếm cạnh lên của kênh A, bạn không biết bánh đang tiến hay lùi. Khi kết hợp cả hai kênh A và B: kênh A đi trước B báo hiệu quay thuận, B đi trước A báo hiệu quay nghịch. Đếm cả cạnh lên lẫn cạnh xuống trên cả A và B (**chế độ 4×**) giúp tăng độ phân giải góc lên gấp **4 lần** so với chỉ số PPR gốc trên trục động cơ.

### 2. Nhân độ phân giải qua hộp số và bẫy tràn số nguyên (Integer Overflow)
Đặt encoder ở *trục động cơ* (trước hộp số giảm tốc tỉ số $$G$$) thay vì trục bánh xe giúp tăng mật độ xung lên $$G$$ lần, cho phép đo vận tốc cực mượt ở tốc độ thấp. Nhưng mật độ xung cao cũng kéo theo hai rủi ro phần mềm: phải dùng **ngắt phần cứng (hardware interrupt / timer encoder mode)** để không mất xung ở tốc độ cao, và phải tính hiệu $$\Delta N$$ theo số học bù hai an toàn khi bộ đếm 16-bit hoặc 32-bit quay vòng.

### 3. Bản chất tích phân của Odometry và sai số trôi tích lũy
Từ số xung $$\Delta N$$, ta tính quãng đường bánh xe $$\Delta s = \frac{\Delta N}{N_{\text{rev}}} \pi D$$. Vì vị trí $$(x, y, \theta)$$ là tổng tích phân của hàng nghìn bước nhỏ liên tiếp, chỉ cần sai số đường kính bánh xe $$1\%$$ hay một cú trượt bánh thoáng qua cũng khiến sai số vị trí lệch hàng chục centimet sau vài mét — lý do odometry luôn cần kết hợp thêm IMU hoặc LiDAR/camera.

### Giải thích: Cầm tay tính độ phân giải odometry và vận tốc bánh xe từ số xung thực

Giả sử robot dùng động cơ DC có encoder **11 PPR** gắn ở trục sau động cơ, qua hộp số giảm tốc tỉ số **$$G = 30{:}1$$**, chạy giải mã cầu phương **4×**, lắp bánh xe đường kính **$$D = 65\text{ mm}$$**:

1. **Tổng số xung trên 1 vòng quay hoàn chỉnh của bánh xe:**
   $$N_{\text{rev}} = 11\text{ PPR} \times 4 \times 30 = 1\,320\text{ xung/vòng bánh}.$$
2. **Chu vi bánh xe và độ phân giải tuyến tính mỗi xung:**
   $$C = \pi D = \pi \times 65 \approx 204{,}2\text{ mm} \implies \Delta s_{\text{1 xung}} = \frac{204{,}2}{1\,320} \approx 0{,}155\text{ mm/xung}.$$
3. **Tính quãng đường và vận tốc khi đọc được $$\Delta N = 660$$ xung trong $$\Delta t = 0{,}5\text{ s}$$:**
   - Số vòng quay: $$660 / 1\,320 = 0{,}5\text{ vòng}$$.
   - Quãng đường bánh đi được: $$\Delta s = 0{,}5 \times 204{,}2 = 102{,}1\text{ mm} = 0{,}1021\text{ m}$$.
   - Vận tốc tuyến tính: $$v = \frac{0{,}1021}{0{,}5} = 0{,}2042\text{ m/s}$$.

Nếu lốp cao su bị mòn hoặc non hơi làm đường kính thực giảm từ $$65\text{ mm}$$ xuống $$63{,}7\text{ mm}$$ (chỉ lệch $$2\%$$), sau $$10\text{ m}$$ chạy thẳng, odometry sẽ báo nhầm tới $$20\text{ cm}$$ — đó là lý do bước hiệu chuẩn đường kính bánh thực tế luôn bắt buộc trước khi chạy điều hướng!

## Mục tiêu học

Sau bài này, bạn đọc được hai sóng vuông lệch pha (quadrature) của encoder hai kênh A và B để xác định kênh nào dẫn trước, từ đó phân biệt chiều tiến và chiều lùi. Bạn không tin mù quáng vào thông số "PPR" trên trang bán hàng mà tự đo số xung thực tế trên một vòng trục ra của bánh theo đúng chế độ giải mã trong firmware. Bạn quy đổi được số đếm thành cung tròn với bánh đường kính 65 mm, rồi từ quãng đường hai bánh tính được một bước ước lượng vị trí (dead reckoning): quãng đường tịnh tiến của tâm trục và góc quay theo radian — nền tảng trực tiếp của `nav_msgs/Odometry`.

## Kiến thức cần có

Bạn đã biết đếm cạnh xung trên GPIO và in ra màn hình serial (Chương 03), đồng thời phân biệt được đĩa từ Hall trên hộp số TT vàng với đĩa quang có rãnh (Bài 04-02). Encoder tín hiệu số không dùng I2C như Bài 04-01; UART chỉ dùng để gửi số đếm lên máy tính. Luôn dùng đồng hồ vạn năng đo mức cao của tín hiệu encoder trước khi nối vào GPIO 3,3 V. Bài này chưa cần ROS và không cần cấp điện cho động cơ ở bước đo chính.

## Vì sao bài này quan trọng với Capstone A và ROS

Capstone A ở Chương 07 chạy teleop xe vi sai qua cổng serial và tự dừng khi hết hạn lệnh. Bản chạy thử đó vẫn hoạt động được khi chưa có encoder, nhưng nhật ký kiểm thử sẽ đáng tin cậy hơn nhiều khi có thêm số đếm bánh để đối chiếu trực tiếp với thước đo thực tế.

Trong ROS 2, `diff_drive_controller` áp dụng đúng các công thức hình học này: firmware hoặc lớp giao tiếp phần cứng (`ros2_control`) đổi số xung thành góc quay bánh nhờ hằng số $$N$$ (số xung trên một vòng trục ra sau giải mã); bộ điều khiển đổi góc quay thành mét qua tham số `wheel_radius` ($$r$$) và thành góc quay hướng (yaw) qua `wheel_separation` (khẩu độ $$b$$), rồi xuất bản tin `nav_msgs/Odometry` (còn `sensor_msgs/JointState` mang chính vị trí góc bánh theo radian). Nếu khai báo $$N$$ lớn gấp đôi thực tế, odometry sẽ báo quãng đường chỉ bằng một nửa thực tế dù bán kính bánh hoàn toàn đúng. Vì vậy, luôn đo $$N$$ trực tiếp trên bánh thật thay vì chép từ tiêu đề quảng cáo.

![Hai kênh quadrature A và B: cạnh nào lên trước thì đó là chiều]({{ site.imgurl }}/generated/encoder_quadrature.png)

## Hai sóng vuông lệch pha

Encoder quadrature xuất hai chuỗi sóng vuông A và B lệch nhau khoảng một phần tư chu kỳ ($90^\circ$). Chiều quay được xác định bởi kênh nào chuyển mức trước: theo một quy ước thường dùng (cần kiểm chứng lại trên mạch thực tế), nếu cạnh lên của A xuất hiện khi B đang ở mức thấp thì tính là chiều tiến, còn nếu cạnh lên của B xuất hiện khi A đang ở mức thấp thì tính là chiều lùi. Đảo hai dây A và B sẽ làm đảo dấu bộ đếm.

Ngược lại, encoder một kênh chỉ đếm được số xung mà không tự biết chiều quay; việc suy đoán dấu theo lệnh điều khiển động cơ sẽ sai lệch khi bánh bị trôi quán tính hoặc giật ngược lúc phanh.

## Tránh hiểu nhầm thông số "PPR"

Trên các trang bán linh kiện, "PPR" (Pulses Per Revolution) có thể chỉ số chu kỳ mỗi vòng của một kênh, nhưng đôi khi lại chỉ tổng số cạnh sau khi giải mã. Khi dùng chế độ giải mã 4× (đếm cả cạnh lên và cạnh xuống của cả hai kênh A và B):

$$
N \approx 4 \times (\text{số chu kỳ trên một vòng của một kênh}).
$$

Ngoài ra, nhiều động cơ TT vàng gắn đĩa nam châm trực tiếp lên trục động cơ (phía trước hộp số). Nếu đĩa tạo 11 cạnh lên mỗi vòng trục động cơ (đếm 1×) đi qua hộp số tỉ số 1:48, thì số xung trên một vòng trục ra gắn bánh là:

$$
N = 11 \times 48 = 528.
$$

Nếu lấy nhầm số 11 thay vào công thức quãng đường, mọi khoảng cách tính ra sẽ bị phóng đại gấp 48 lần. Cách chắc chắn nhất để xác định $$N$$ là vạch dấu trên lốp, quay tay đúng một vòng và đọc trực tiếp từ bộ đếm của chính firmware đang chạy.

## Quãng đường ứng với mỗi xung

Giả sử bánh không trượt, mỗi vòng quay đưa tâm bánh đi một đoạn đúng bằng chu vi $$2\pi r$$, nên với $$\Delta c$$ xung đếm được:

$$
\Delta s = \frac{2\pi r}{N}\Delta c.
$$

Với bánh đường kính 65 mm, bán kính $$r = 0{,}0325~\mathrm{m}$$ và chu vi là:

$$
2\pi r \approx 2 \times 3{,}1416 \times 0{,}0325 = 0{,}2042~\mathrm{m}.
$$

Nếu dùng đĩa quang đơn giản với firmware đếm $$N = 20$$ xung trên một vòng trục ra, mỗi xung tương ứng:

$$
\frac{0{,}2042}{20} = 0{,}01021~\mathrm{m} \approx 1{,}021~\mathrm{cm}.
$$

Khi đếm được 140 xung, quãng đường là:

$$
\Delta s = 140 \times 0{,}01021 \approx 1{,}43~\mathrm{m}.
$$

Lưu ý $$N = 20$$ chỉ là ví dụ cho đĩa rãnh học tập; nếu lần quay tay thực tế trên động cơ của bạn cho ra 360, 528 hay 1440, hãy thay đúng con số đó vào công thức.

## Một bước ước lượng vị trí (dead reckoning)

Cặp công thức động học vi sai sau sẽ được dùng lại ở Chương 06 và trong bộ điều khiển:

$$
\Delta s = \frac{\Delta s_r + \Delta s_l}{2}, \qquad \Delta \theta = \frac{\Delta s_r - \Delta s_l}{b}.
$$

Trong đó $$b$$ là khoảng cách giữa tâm hai vết bánh (wheel separation), không phải đường kính bánh. Ví dụ với $$\Delta s_r = 0{,}10~\mathrm{m}$$, $$\Delta s_l = 0{,}06~\mathrm{m}$$ và $$b = 0{,}15~\mathrm{m}$$:

$$
\Delta s = \frac{0{,}10 + 0{,}06}{2} = 0{,}08~\mathrm{m}, \qquad \Delta \theta = \frac{0{,}04}{0{,}15} = 0{,}267~\mathrm{rad} \approx 15{,}3^\circ.
$$

Tâm trục xe dịch chuyển 8 cm và quay khoảng $15{,}3^\circ$ về phía bánh chậm hơn (bánh trái). Công thức chưa tính đến độ trượt của bánh. Nếu chỉ đảo nhầm dây A và B ở encoder bánh phải, sổ ghi sẽ nhận $$\Delta s_r = -0{,}10~\mathrm{m}$$ dù bánh thực tế đi tới, làm sai lệch hoàn toàn cả $$\Delta s$$ lẫn $$\Delta \theta$$.

## Lab: quay tay một vòng để đo $$N$$

### An toàn

Thực hiện phép đếm khi **không cấp điện** cho động cơ. Nếu đã có mạch cầu H và muốn thực hiện bước tùy chọn kiểm tra chiều khi cấp điện, bắt buộc kê bánh xe nhấc khỏi bàn, chỉ cấp xung ngắn và giữ tay tránh xa nan hoa. Nếu đo thấy mức logic cao của cảm biến Hall là 5 V, phải lắp cầu chia áp 1 kΩ / 2 kΩ (tương tự chân Echo ở Bài 04-02) trước khi nối vào GPIO của ESP32.

### BOM

| Món | Vai trò |
|------|---------|
| Một động cơ giảm tốc có encoder, hoặc đĩa quang rãnh rời | Trục cần đo số xung |
| ESP32 hoặc Pico | Đọc và đếm cạnh xung |
| Bút đánh dấu | Kẻ vạch mốc trên lốp và vỏ hộp số |
| Sổ tay | Ghi $$N$$, bán kính và mét trên mỗi xung |
| Mạch cầu H và pin | Chỉ dùng cho bước kiểm tra chiều tùy chọn (bánh nhấc khỏi bàn) |

### Các bước

1. Kẻ một vạch mốc trên lốp và một vạch tương ứng trên vỏ hộp số để xác định chính xác một vòng quay.
2. Không cấp nguồn động cơ; đưa bộ đếm về 0.
3. Quay tay trục ra đúng một vòng trở lại vạch mốc rồi ghi số đếm. Lặp lại ba lần; ba kết quả nên lệch nhau không quá 1 xung.
4. Giá trị thu được chính là $$N$$ cho chế độ giải mã đang chạy. Tính $$2\pi r / N$$ theo đúng bán kính chiếc lốp đã đo.
5. Vẫn không cấp điện động cơ, quay bánh theo chiều tiến của robot và xác định kênh nào lên trước (dùng máy phân tích logic hoặc in sự kiện "A lên", "B lên" ra serial). Nếu chỉ có encoder một kênh, ghi rõ: "một kênh, chiều phụ thuộc lệnh động cơ".
6. *(Tùy chọn, bánh nhấc khỏi bàn)* Cấp một xung điện ngắn theo chiều tiến và xác nhận cùng kênh đó dẫn trước; nếu ngược dấu, đảo hai dây A và B rồi kiểm tra lại.

### Kết quả mong đợi

Ba lần quay tay cho kết quả $$N$$ thống nhất, giá trị quãng đường trên mỗi xung tính theo mét và ghi chú kênh dẫn trước khi đi tiến được lưu đầy đủ vào `lab-notes.md`.

### Lỗi thường gặp

| Hiện tượng | Nguyên nhân thường gặp |
|------------|------------------------|
| Số đếm đột ngột tăng gấp đôi | Đổi chế độ giải mã từ 1× sang 2× hoặc 4× nhưng quên cập nhật $$N$$ |
| Trang bán ghi 40 PPR nhưng quay tay ra 20 | Trang bán tính tổng số cạnh nhiều hơn số cạnh mã nguồn đang đếm |
| Ra lệnh tiến nhưng số đếm giảm | Đảo hai dây A/B hoặc đảo ngược cực dây động cơ (chỉ sửa từng thứ một) |
| Bánh đứng yên nhưng số đếm vẫn tăng | Nhiễu/dội tín hiệu, chân để nổi hoặc chưa nối chung mass |
| Quãng đường tính ra dài gấp vài chục lần thực tế | Dùng nhầm số xung của trục động cơ mà quên nhân tỉ số hộp số |

## Cùng mức PWM, vì sao xe vẫn chạy lệch?

Ngay cả khi gửi cùng một mức PWM cho cả hai bánh, xe vi sai vẫn thường bị lệch sang một bên. Hai động cơ giảm tốc TT vàng không bao giờ đồng nhất tuyệt đối: độ rơ bánh răng, ma sát và sai số chế tạo khiến một trục quay nhanh hơn trục kia vài phần trăm. Điều khiển vòng hở không có phản hồi nên không thể tự bù sai lệch này.

Encoder cung cấp tín hiệu phản hồi tốc độ để thấy ngay độ lệch đó. Đĩa quang 20 rãnh (ví dụ $$N = 20$$) đủ để học nguyên lý đếm, còn trên robot Capstone A nên dùng cặp động cơ TT có sẵn encoder Hall đọc bằng ESP32/Pico và lái bằng TB6612 (lưu ý các video minh họa dùng Arduino và L298N không phải bộ kit mặc định của khóa học).

Ví dụ khi đếm đồng thời hai bánh trong cùng một khoảng chạy: bánh trái đạt 519 xung, bánh phải đạt 552 xung. Bánh phải nhanh hơn bánh trái $$552 - 519 = 33$$ xung, tương đương:

$$
\frac{33}{519} \approx 6{,}4\%.
$$

Với độ lệch này, lệnh "đi thẳng" ở vòng hở sẽ tạo thành quỹ đạo cong. Bạn có thể thử nhanh (nhấc bánh khỏi bàn): xuất cùng một mức duty vừa phải cho hai kênh trong 3 giây, so sánh hai bộ đếm và ghi cặp số vào `lab-notes.md`.

Giải pháp căn cơ không phải chỉnh tay một hệ số bù cố định rồi bỏ đó, mà là điều khiển vòng kín tốc độ từng bánh bằng PID ở [bài 08-03]({% multilang_post_url contents/chapter08/08_03_pid_tuning %}) và phân tích động học vi sai ở [bài 08-04]({% multilang_post_url contents/chapter08/08_04_diff_kinematics %}).

Xem thêm: video ngắn của LPPS - 1 Robotics Team, [cùng PWM, sao xe không đi thẳng](https://www.facebook.com/reel/1851960802892543).

## Mua ở Việt Nam

Nên mua theo cặp động cơ TT có sẵn encoder Hall để hai bánh đồng bộ về tỉ số truyền hộp số.

| Món | Từ khóa | Khoảng giá (VND) | Thay thế |
|------|---------|------------------|----------|
| Động cơ TT có encoder Hall | `động cơ TT encoder Hall` | 40.000–90.000 một cái | Động cơ N20 có encoder nếu khớp lỗ gá và trục (3 mm hoặc 4 mm) |
| Đĩa rãnh và cặp quang | `đĩa encoder quang` | 15.000–40.000 | Phù hợp để học cách đo $$N$$, ít chắc chắn hơn cho khung Capstone |
| 1 kΩ và 2 kΩ | `điện trở 1k 2k` | 10.000–20.000 một vỉ | Chỉ cần khi mức cao của cảm biến Hall đo được 5 V |

- [Hshop: động cơ encoder](https://hshop.vn/search?q=dong%20co%20encoder)
- [Shopee: động cơ TT encoder](https://shopee.vn/search?keyword=dong%20co%20TT%20encoder)
- [Lazada: encoder Hall TT](https://www.lazada.vn/catalog/?q=encoder%20Hall%20TT)
- [Thế Giới IC: encoder](https://www.thegioiic.com/search?q=encoder)

Cần đọc kỹ thông số xung là tính trên trục động cơ hay trục ra, sau đó luôn kiểm chứng lại bằng cách tự quay tay một vòng.

## Video tham khảo

- **Xem trước:** [How Rotary Encoder Works and How To Use It with Arduino](https://www.youtube.com/watch?v=v4BbSzJ-hz4) — How To Mechatronics, tiếng Anh. Giải thích hai kênh A, B và cách thứ tự cạnh xác định chiều quay.
- [Modern Robotics, Chapter 13.4:  Odometry](https://www.youtube.com/watch?v=eQ9E0Zvp9jw) — Northwestern Robotics, tiếng Anh. Tổng quan cách tích hợp các bước đếm encoder thành tư thế robot (sẽ triển khai chi tiết ở Chương 08).

## Bài tập

Lấy $$r = 0{,}0325~\mathrm{m}$$ và chu vi $$\approx 0{,}2042~\mathrm{m}$$ nếu đề không nêu khác.

1. Với $$N = 20$$ xung trên một vòng trục ra, bánh xe lăn được bao xa sau 140 xung?
2. Cùng firmware đó, quay tay một vòng thu được 20 xung nhưng bạn lại nhập thông số "40 PPR" của người bán vào công thức. Chương trình sẽ báo quãng đường bao nhiêu cho 140 xung, so với quãng đường đúng?
3. Bánh xe thực tế đi được $$\Delta s_r = 0{,}10~\mathrm{m}$$ và $$\Delta s_l = 0{,}06~\mathrm{m}$$ với khẩu độ $$b = 0{,}15~\mathrm{m}$$. Do đảo dây A và B ở encoder bánh phải, sổ ghi nhận $$-0{,}10~\mathrm{m}$$ và $$+0{,}06~\mathrm{m}$$. Tính $$\Delta s$$ và $$\Delta \theta$$ sai lệch so với giá trị đúng ($$0{,}08~\mathrm{m}$$ và $$0{,}267~\mathrm{rad}$$).
4. Một kênh đếm 80 cạnh lên khi đi tới và 80 cạnh lên nữa khi lăn lùi về đúng vạch xuất phát (với $$N = 20$$). Encoder quadrature báo quãng đường thực bằng bao nhiêu, còn nếu cộng dồn 160 cạnh như chỉ đi tới thì kết quả là bao nhiêu?
5. Một động cơ TT phát 11 cạnh lên trên mỗi vòng trục động cơ, qua hộp số 1:48, mã nguồn đếm 1× ở trục ra. Hỏi $$N$$ bằng bao nhiêu, và nếu dùng nhầm 11 thì quãng đường tính ra sai lệch gấp mấy lần?

### Gợi ý đáp án

1. Mỗi xung tương ứng $$0{,}01021~\mathrm{m}$$; sau 140 xung được $$1{,}43~\mathrm{m}$$.
2. Với $$N = 40$$, chương trình báo $$0{,}715~\mathrm{m}$$, chỉ bằng một nửa giá trị đúng $$1{,}43~\mathrm{m}$$.
3. Sổ báo $$\Delta s = -0{,}02~\mathrm{m}$$ và $$\Delta \theta = -1{,}067~\mathrm{rad}$$ (xấp xỉ $$-61^\circ$$), thay vì $$+0{,}08~\mathrm{m}$$ và $$+15{,}3^\circ$$.
4. Encoder quadrature có tổng đại số bằng 0 nên quãng đường thực bằng 0; nếu cộng dồn cả 160 cạnh sẽ ra $$1{,}63~\mathrm{m}$$.
5. $$N = 11 \times 48 = 528$$; dùng nhầm 11 sẽ làm mọi quãng đường phóng đại gấp 48 lần.

## Đọc thêm

- [SparkFun: nối rotary encoder](https://learn.sparkfun.com/tutorials/rotary-encoder-breakout-hookup-guide/all) — giải thích thứ tự cạnh và giới hạn của encoder một kênh.
- [Pololu: cặp encoder từ](https://www.pololu.com/product/3081) — ví dụ thực tế về việc datasheet ghi số xung theo trục động cơ và cần nhân tỉ số hộp số.
- [`nav_msgs/Odometry`](https://docs.ros.org/en/jazzy/p/nav_msgs/msg/Odometry.html) — chuẩn bản tin ROS 2 tổng hợp từ các bước ước lượng dead reckoning.
- [`diff_drive_controller`](https://control.ros.org/jazzy/doc/ros2_controllers/diff_drive_controller/doc/userdoc.html) — cách `wheel_radius` ($$r$$) và `wheel_separation` ($$b$$) kết hợp với số đếm đã quy đổi từ $$N$$.
