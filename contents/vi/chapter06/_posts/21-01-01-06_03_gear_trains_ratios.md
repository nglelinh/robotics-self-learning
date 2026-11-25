---
layout: post
title: "Bánh răng: trụ, worm, hành tinh, tỉ số, backlash"
chapter: "06"
order: 3
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter06
lesson_type: required
draft: false
---

Thời lượng ước tính: **80–100 phút**, bao gồm thời gian đếm răng trực tiếp trên hộp giảm tốc bạn đang có hoặc trên một ảnh chụp rõ nét của hộp số đó.

Một động cơ DC nhỏ thường quay tít mù ở tốc độ $$6\,000\text{ RPM}$$ nhưng lại yếu đến mức chỉ cần hai ngón tay bóp nhẹ là đứng khựng lại. Làm sao biến sự "nhanh mà yếu" đó thành chuyển động "chậm mà khỏe" đủ đẩy cả con robot leo dốc? Câu trả lời cổ điển nhất của kỹ thuật cơ khí là **hộp số bánh răng (gear train)** — bộ biến áp cơ học đánh đổi trực tiếp tốc độ góc lấy mô-men xoắn theo định luật bảo toàn công suất.

## Kiến thức cần nhớ: Các họ bánh răng, Tỉ số truyền và Độ rơ (Backlash)

### 1. Bánh răng trụ (Spur), Trục vít (Worm) và Hành tinh (Planetary)
- **Bánh răng trụ (Spur):** dễ chế tạo, hiệu suất cao (~90%–95% mỗi cấp), nhưng ồn ở tốc độ cao và tốn diện tích khi cần tỉ số lớn.
- **Trục vít – bánh vít (Worm):** đạt tỉ số truyền cực lớn (20:1 đến 60:1) trong 1 cấp và có tính **tự hãm (self-locking)** khi mất điện (tay robot không bị rơi tự do), nhưng hiệu suất thấp (40%–70%) do ma sát trượt lớn.
- **Bánh răng hành tinh (Planetary):** đồng trục, chia tải đều lên 3–4 bánh răng vệ tinh nên cực gọn, chịu mô-men rất lớn và độ rơ thấp — tiêu chuẩn vàng cho khớp cánh tay robot và xe tự hành hiệu suất cao.

### 2. Tỉ số truyền $$G$$ và hiệu suất nối tiếp $$\eta$$
Khi bánh chủ động có $$Z_{\text{in}}$$ răng ăn khớp với bánh bị động $$Z_{\text{out}}$$ răng, tỉ số truyền là $$G = Z_{\text{out}} / Z_{\text{in}}$$. Tốc độ giảm $$G$$ lần ($$\omega_{\text{out}} = \omega_{\text{in}} / G$$), còn mô-men tăng lên $$\tau_{\text{out}} = \tau_{\text{in}} \cdot G \cdot \eta$$ (với $$\eta < 1$$ là hiệu suất do ma sát). Nhiều cấp nối tiếp thì **nhân** cả tỉ số truyền lẫn hiệu suất!

### 3. Độ rơ bánh răng (Backlash) — kẻ thù thầm lặng của độ chính xác
Giữa hai răng ăn khớp luôn phải có một khe hở nhỏ để bôi trơn và tránh kẹt nhiệt. Khi động cơ đảo chiều, trục ra đứng yên một khoảnh khắc nhỏ trước khi răng bên kia chạm vào — góc rơ tự do đó gọi là **backlash**. Trên cánh tay robot dài, chỉ $$1^\circ$$ backlash ở khớp vai đã tạo ra sai số vài milimet ở đầu kẹp!

### Giải thích: Cầm tay tính hộp số 2 cấp và sai số đầu tay kẹp do Backlash

**Phần A — Hộp số bánh răng trụ 2 cấp:**
- Cấp 1: bánh dẫn $$Z_1 = 12$$ răng ăn khớp bánh bị dẫn $$Z_2 = 36$$ răng $$\implies G_1 = 36/12 = 3{:}1$$.
- Cấp 2: bánh dẫn $$Z_3 = 12$$ răng ăn khớp bánh bị dẫn $$Z_4 = 48$$ răng $$\implies G_2 = 48/12 = 4{:}1$$.
- **Tổng tỉ số truyền:** $$G_{\text{tổng}} = G_1 \times G_2 = 3 \times 4 = 12{:}1$$.

Giả sử động cơ đầu vào quay **$$3\,600\text{ RPM}$$** với mô-men **$$0{,}05\text{ N}\cdot\text{m}$$**, mỗi cấp ăn khớp đạt hiệu suất **$$\eta = 90\% = 0{,}90$$**:
1. **Tốc độ trục ra:** $$\omega_{\text{out}} = \frac{3\,600}{12} = 300\text{ RPM}$$.
2. **Tổng hiệu suất 2 cấp:** $$\eta_{\text{tổng}} = 0{,}90 \times 0{,}90 = 0{,}81\;(81\%)$$.
3. **Mô-men trục ra thực tế:** $$\tau_{\text{out}} = 0{,}05 \times 12 \times 0{,}81 = 0{,}486\text{ N}\cdot\text{m}$$ (mạnh hơn gần **10 lần** động cơ gốc!).

**Phần B — Tác động của $$1{,}0^\circ$$ backlash lên cánh tay dài $$L = 200\text{ mm}$$:**
Đổi $$1{,}0^\circ$$ sang radian: $$\Delta\theta = 1{,}0 \times \frac{\pi}{180} \approx 0{,}01745\text{ rad}$$.
Độ rơ lắc tự do ngay tại đầu gắp:
$$\Delta x = L \cdot \Delta\theta = 200 \times 0{,}01745 \approx 3{,}49\text{ mm}!$$
Thấy rõ ngay: dù encoder trục động cơ chính xác tới $$0{,}01^\circ$$, độ rơ cơ khí $$1^\circ$$ trong hộp số vẫn làm đầu tay kẹp lệch gần $$3{,}5\text{ mm}$$ nếu bạn không đặt encoder ở trục ra hoặc dùng hộp số độ rơ thấp!

## Mục tiêu học

Sau bài này, các bạn tính được tỉ số truyền từ số răng của từng cặp bánh răng, dự đoán góc quay đầu ra tương ứng với một góc quay đầu vào cho trước, và xác định đúng chiều quay qua mỗi cặp ăn khớp ngoài. Các bạn cũng phân biệt được công dụng của bộ truyền trục vít – bánh vít (worm), nắm được công thức tỉ số truyền hành tinh trong giáo trình đồng thời biết tin vào tỉ số đóng dấu trên vỏ động cơ TT, và nhận diện độ rơ (backlash) như phần chuyển động bị trễ xuất hiện dưới dạng xung encoder khi robot đảo chiều.

## Kiến thức cần có

Các bạn đã biết đo khổ vết và bán kính lăn (Bài 01) và hiểu vít cố định trục phải tỳ đúng vào mặt vát trục chữ D (Bài 02). Số răng là số nguyên, nên chỉ cần các phép nhân chia cơ bản trên máy tính bỏ túi.

## Vì sao bài này quan trọng với Capstone A và ROS

Encoder (Chương 04) thường đếm số vòng quay trên trục động cơ hoặc một trục trung gian trong hộp số, trong khi bánh xe chạm sàn đã được giảm tốc qua tỉ số truyền $$i$$. Bộ điều khiển `diff_drive_controller` chỉ quy đổi chính xác số xung thành mét khi cả tỉ số truyền $$i$$ và bán kính lăn $$r$$ đều đúng.

Nếu nhầm lẫn giữa bánh đầu vào và bánh đầu ra, bạn sẽ đảo ngược giá trị $$i$$. Khi đó, quãng đường odometry bị sai lệch theo hệ số $$i^2$$: chẳng hạn tỉ số thật bằng 3 nhưng lưu nhầm thành $$1/3$$ sẽ làm quãng đường ước lượng bị kéo giãn hoặc co ngắn tới 9 lần. Tương tự như lỗi khổ vết ở Bài 01 khiến xe chạy lệch thành đường cong, lỗi tỉ số truyền sẽ làm toàn bộ tỉ lệ bản đồ bị sai lệch. Hãy ghi $$i$$ ngay cạnh $$b$$ và $$r$$ trong `lab-notes.md`.

## Cặp ăn, worm, hành tinh, và vùng chết

Với một cặp bánh răng trụ ăn khớp, tỉ số truyền được định nghĩa là:

$$
i = \frac{N_{\text{out}}}{N_{\text{in}}} = \frac{\omega_{\text{in}}}{\omega_{\text{out}}}.
$$

Trong đó $$N$$ là số răng. Khi tốc độ góc giảm, mô-men xoắn ở đầu ra tăng lên tương ứng (sau khi trừ tổn hao ma sát tại bề mặt răng và bạc đạn). Ví dụ, bánh dẫn 12 răng ăn khớp với bánh bị dẫn 36 răng cho tỉ số $$i = 36/12 = 3$$: động cơ quay ba vòng thì bánh xe quay một vòng, và mô-men tại bánh xe xấp xỉ gấp ba lần mô-men trục dẫn (thực tế nhỏ hơn một chút do ma sát).

Mỗi cặp bánh răng ăn khớp ngoài sẽ làm đảo chiều quay, tức bánh bị dẫn quay ngược chiều bánh dẫn. Khi nối tiếp cặp ăn khớp thứ hai (bánh dẫn qua bánh trung gian rồi sang bánh ra), chiều quay bị đảo hai lần nên đầu ra quay cùng chiều với đầu vào. Một bánh trung gian đơn chỉ có tác dụng đổi chiều quay mà không làm thay đổi tỉ số truyền. Tuy nhiên, nếu hai bánh có số răng khác nhau được cố định trên cùng một trục (bánh răng kép), tỉ số truyền của các cấp sẽ nhân với nhau. Tương tự, nếu hệ truyền động có thêm bộ truyền đai (Bài 04) sau hộp giảm tốc, tỉ số truyền tổng tại bánh xe là:

$$
i_{\text{wheel}} = i_{\text{gearbox}} \cdot i_{\text{belt}}.
$$

Bỏ sót một trong hai thừa số là lỗi sai tỉ lệ thường gặp nhất.

Bộ truyền trục vít – bánh vít (worm) gồm một trục vít ăn khớp với bánh vít. Cơ cấu này đạt tỉ số truyền rất cao (thường hàng chục lần chỉ trong một cấp) và nhiều cặp có tính tự hãm (không thể xoay ngược từ phía bánh vít), giúp tay máy nhỏ giữ nguyên tư thế ngay cả khi mất nguồn động cơ. Nhược điểm là hiệu suất thấp: phần lớn năng lượng điện dự trù ở Chương 05 bị chuyển thành nhiệt do ma sát trượt. Vì vậy, bộ truyền worm thích hợp cho cơ cấu kẹp cần giữ chặt, nhưng không phù hợp cho bánh chủ động của Capstone A — nơi ta cần chuyển tối đa năng lượng pin thành chuyển động. Bạn có thể thử xoay trục đầu ra của một bộ worm bằng tay: thông thường bánh vít sẽ không quay được.

Bộ truyền bánh răng hành tinh gom bánh răng mặt trời (sun), các bánh răng hành tinh trên cần mang (carrier) và vành răng ngoài (ring) vào gọn trong cùng một đường kính. Trong cấu hình cơ bản ở giáo trình (vành răng cố định, đầu vào là bánh mặt trời, đầu ra là cần mang), tỉ số truyền là:

$$
i = 1 + \frac{N_{\text{ring}}}{N_{\text{sun}}}.
$$

Công thức trên áp dụng cho một cấp hành tinh đơn. Các hộp giảm tốc TT hoặc hộp số kim loại thực tế có thể gồm nhiều cấp bánh răng trụ hoặc nhiều tầng hành tinh xếp chồng, và con số đóng dấu trên vỏ (như 1:48, 1:90 hay 1:120) đã tính gộp tất cả các cấp bên trong. Hãy dùng công thức đếm răng khi bạn quan sát trực tiếp được bánh răng, và tin vào tỉ số đóng dấu khi hộp số đóng kín.

Độ rơ (backlash) là khoảng chuyển động bị mất khi mô-men đảo chiều. Răng bánh răng luôn được chế tạo có khe hở nhỏ để tránh kẹt khi ăn khớp, và khe hở này tạo thành một khoảng trễ mỗi khi đổi chiều quay. Nếu giữ cố định trục động cơ rồi lắc nhẹ trục đầu ra, bạn sẽ thấy bánh xe dịch chuyển vài độ trước khi trục động cơ bắt đầu chịu lực. Các xung encoder sinh ra trong khoảng rơ này gây ra một độ lệch nhỏ không tương ứng với chuyển động thực trên sàn. Ta không thể loại bỏ hoàn toàn độ rơ ở hộp số TT nhựa đúc; thay vào đó, cần ước lượng góc rơ bằng mắt để ghi nhận và tránh các thuật toán điều khiển đảo chiều liên tục trong thời gian vài miligiây.

![Chuỗi bánh răng kép: số răng đặt tỉ số, mỗi cặp ăn ngoài đảo chiều]({{ site.imgurl }}/generated/gear_train_ratio.png)

Hình trên cho thấy tầm quan trọng của việc xác định đúng bánh đầu vào trước khi chia. Hãy lần theo đường truyền mô-men từ động cơ ra bánh xe, nhân lần lượt $$N_{\text{out}}/N_{\text{in}}$$ qua từng cấp và đếm số cặp ăn khớp ngoài để biết chiều quay cuối cùng. Một bánh trung gian đơn nằm giữa hai bánh chỉ giúp đảo chiều, không thêm thừa số vào tỉ số truyền trừ khi nó là bánh răng kép có hai vòng răng khác số răng.

## Ví dụ tính tay

Xét cặp bánh răng có bánh dẫn $$N_{\text{in}} = 12$$ và bánh bị dẫn $$N_{\text{out}} = 36$$:

$$
i = \frac{36}{12} = 3.
$$

Khi xoay bánh dẫn một góc $$90^\circ$$, bánh đầu ra sẽ quay:

$$
\theta_{\text{out}} = \frac{90^\circ}{3} = 30^\circ,
$$

theo chiều ngược lại vì đây là một cặp ăn khớp ngoài. Ba vòng đầy đủ của động cơ ($$1080^\circ$$) tạo ra đúng một vòng quay bánh xe. Nếu gọi nhầm tên đầu vào/đầu ra và lưu $$i = 12/36 = 1/3$$, quãng đường tính toán sẽ lệch theo hệ số:

$$
i_{\text{true}}^{2} = 9,
$$

tức dài gấp 9 lần hoặc ngắn chỉ còn $$1/9$$ tùy bước nhân chia trong phần mềm. Cách tránh nhầm lẫn đơn giản nhất là luôn chỉ rõ bánh phía động cơ là “đầu vào” trước khi lập tỉ số.

Với động cơ TT đóng dấu 1:48, hãy ghi trực tiếp giá trị 48 vào sổ tay dù bạn biết công thức hành tinh $$1 + N_{\text{ring}}/N_{\text{sun}}$$, vì con số nhà sản xuất đã gộp toàn bộ các tầng giảm tốc bên trong.

## Lab: đếm, dự đoán, đối chiếu

### An toàn

Đảm bảo đã tắt nguồn. Răng bánh răng có thể kẹp ngón tay khi quay. Nếu mở hộp số, mỡ bôi trơn và các phe cài nhỏ rất dễ rơi bắn, nên đếm răng qua ảnh chụp sắc nét là đủ cho bài này. Tuyệt đối không cấp nguồn pin cho động cơ khi tay đang chạm vào cặp bánh răng.

### BOM

| Hạng mục | Vai trò |
|------|------|
| Một hộp giảm tốc, một cặp bánh rời, hoặc một ảnh sắc của bánh các bạn có | Số răng |
| Bút và giấy | Tỉ số và góc |
| `lab-notes.md` | Con số ROS sẽ dùng lại |

### Các bước

1. Xác định rõ bánh đầu vào (phía động cơ) và bánh đầu ra (phía bánh xe).
2. Đếm số răng của từng bánh. Với động cơ TT vỏ kín, đọc tỉ số đóng dấu (ví dụ 1:48) và ghi chú rõ là số liệu đọc từ nhãn vỏ.
3. Tính $$i = N_{\text{out}}/N_{\text{in}}$$ hoặc chép lại tỉ số đóng dấu, đồng thời đếm số cặp ăn khớp ngoài để xác định chiều quay.
4. Dự đoán góc quay đầu ra khi trục vào quay $$90^\circ$$ theo công thức $$\theta_{\text{out}} = 90^\circ / i$$.
5. Nếu có bánh răng thực tế, xoay trục đầu vào khoảng một phần tư vòng (dựa theo vạch đánh dấu) để đối chiếu với dự đoán. Sau đó giữ trục vào, lắc nhẹ trục ra và ước lượng độ rơ theo độ.
6. Nếu chỉ làm việc trên bản vẽ hoặc ảnh chụp, bản tính dự đoán trên giấy là kết quả nộp; nhớ ghi chú nhãn “bản vẽ”.

### Kết quả mong đợi

Một giá trị $$i$$ cụ thể, ghi chú chiều quay và góc dự đoán trong sổ tay. Với cặp 12 và 36 răng, kết quả là $$i = 3$$ và $$\theta_{\text{out}} = 30^\circ$$ ngược chiều đầu vào. Ở hộp số nhựa đúc thực tế, tỉ số đo thực nghiệm ở Bài 08 thường sai lệch không quá 10% so với dấu đóng, và độ rơ vài độ tại trục bánh là bình thường.

### Lỗi thường gặp

| Các bạn thấy | Thường nghĩa là |
|--------------|------------------------|
| Tỉ số ra nhỏ hơn 1 trên hộp số lẽ ra phải làm chậm động cơ | Các bạn đã gọi bánh phía xe là đầu vào |
| Chiều bánh xe làm các bạn ngạc nhiên | Quên một cặp ăn ngoài, hoặc đếm bánh trung gian như một lần đổi tỉ số |
| Đầu ra dịch vài độ trước khi đầu vào buộc phải động | Độ rơ; ghi lại, đừng “sửa” bằng keo |
| Dấu đóng nói 1:48 mà công thức một cấp của các bạn ra 4 | Các bạn đang nhìn một cấp của một chồng; tin dấu đóng |

## Mua ở Việt Nam / Where to buy in Vietnam

Bộ truyền bánh răng của Capstone A đã tích hợp sẵn bên trong động cơ giảm tốc TT. Hãy chọn mua động cơ có ghi rõ tỉ số truyền trên vỏ và có sẵn encoder (nếu tìm được) để kết nối với mạch đếm xung của Chương 04. Bộ bánh răng nhựa rời chỉ cần thiết nếu bạn muốn thực hành đếm răng trực tiếp khi hộp số động cơ bị kín.

| Mua gì | Từ khóa | Khoảng giá (VND) | Ghi chú |
|------|----------|------------------|-------|
| Động cơ giảm tốc TT có encoder | `động cơ giảm tốc TT encoder` | 45.000–120.000 mỗi cái | Đọc dấu đóng: 1:48 là phổ biến |
| Bộ bánh răng nhựa | `bánh răng nhựa robot` | 20.000–60.000 | Hữu ích khi hộp kín mà vẫn muốn đếm răng |

Các trang tìm mua:

- [Hshop](https://hshop.vn/search?q=%C4%91%E1%BB%99ng+c%C6%A1+gi%E1%BA%A3m+t%E1%BB%91c+TT)
- [Shopee](https://shopee.vn/search?keyword=%C4%91%E1%BB%99ng%20c%C6%A1%20gi%E1%BA%A3m%20t%E1%BB%91c%20TT%20encoder)
- [Lazada](https://www.lazada.vn/catalog/?q=%C4%91%E1%BB%99ng%20c%C6%A1%20TT%20encoder)
- [Thế Giới IC](https://www.thegioiic.com/search?q=%C4%91%E1%BB%99ng+c%C6%A1+gi%E1%BA%A3m+t%E1%BB%91c)

Giá bán có thể thay đổi theo thời điểm. Hãy kiểm tra đường kính và kiểu trục khớp với bánh xe đã mua ở Bài 01 trước khi đặt hàng.

## Video tham khảo

- **Xem trước:** [Gear Train Design - How to calculate gear trains mechanical engineering](https://www.youtube.com/watch?v=aGHrhm-Rcp0) — The Engineering Mindset, tiếng Anh. Cách tính tỉ số truyền của một chuỗi bánh răng bằng cách nhân từng cặp, khớp với phương pháp trong bài.
- [Compound Gears Explained:  Calculate Gear Ratio](https://www.youtube.com/watch?v=NmUq2TQ8m2M) — INTEGRAL PHYSICS, tiếng Anh. Giải thích bánh răng kép và cách xác định hai bánh nào nằm chung một trục — vị trí rất dễ đếm nhầm.
- [Worm Gears Explained, Calculated & Modeled](https://www.youtube.com/watch?v=K8HQA1Uz1sE) — INTEGRAL PHYSICS, tiếng Anh. Nguyên lý truyền một chiều và tỉ số truyền lớn của trục vít – bánh vít.

## Bài tập

1. Một bánh dẫn 15 răng ăn khớp với bánh bị dẫn 60 răng. Tính tỉ số truyền $$i$$, góc quay đầu ra khi động cơ quay đúng một vòng và chiều quay so với động cơ.
2. Nếu chèn thêm một bánh trung gian đơn 20 răng giữa bánh 15 răng và bánh 60 răng (bánh dẫn chỉ ăn khớp với bánh trung gian), tỉ số $$i$$ và chiều quay đầu ra thay đổi thế nào?
3. Một cấp bánh răng hành tinh có vành cố định, $$N_{\text{sun}} = 12$$ và $$N_{\text{ring}} = 36$$. Tính $$i$$ theo công thức giáo trình. Nếu động cơ TT của bạn đóng dấu 1:48, con số nào cần ghi vào `lab-notes.md`?
4. Nếu bạn lưu nhầm $$i = 1/4$$ cho một hộp số có tỉ số thực bằng 4, quãng đường odometry sẽ sai lệch theo hệ số nào?
5. Khi giữ cố định trục động cơ, bánh xe vẫn lắc được khoảng $$8^\circ$$. Hiện tượng này gọi là gì và nó ảnh hưởng ra sao đến số xung đo được khi robot bắt đầu quay?

### Gợi ý đáp án

1. $$i = 60/15 = 4$$. Một vòng động cơ tạo ra góc đầu ra $$360^\circ/4 = 90^\circ$$, ngược chiều động cơ (do có một cặp ăn khớp ngoài).
2. Bánh trung gian đơn giữ nguyên $$i = 4$$ nhưng thêm một lần đảo chiều, nên đầu ra quay cùng chiều với bánh dẫn.
3. Theo công thức một cấp hành tinh: $$i = 1 + 36/12 = 4$$. Với động cơ TT đã đóng dấu, ghi giá trị 48 vì dấu đóng đã tính gộp toàn bộ các tầng bánh răng bên trong.
4. Sai lệch theo hệ số $$i^2 = 16$$.
5. Đó là độ rơ (backlash). Góc rơ này có thể sinh xung ảo hoặc tạo khoảng trễ trước khi bánh thực sự dịch chuyển, làm sai lệch giai đoạn đầu của cú quay. Cần ghi nhận góc rơ, không đổ keo vào bánh răng để cố khử.

## Đọc thêm

- [SDP-SI, Elements of Metric Gear Technology](https://www.sdp-si.com/resources/elements-of-metric-gear-technology/index.php) — tài liệu chuyên sâu về hình học răng, tỉ số truyền và độ rơ từ nhà sản xuất bánh răng.
- [Gear ratio](https://en.wikipedia.org/wiki/Gear_ratio) — định nghĩa tỉ số truyền $$N_{\text{out}}/N_{\text{in}}$$ và cách tính chuỗi bánh răng kép.
- [Worm drive](https://en.wikipedia.org/wiki/Worm_drive) — đặc điểm tỉ số truyền cao, hiệu suất và cơ chế tự hãm của bộ truyền trục vít – bánh vít.
