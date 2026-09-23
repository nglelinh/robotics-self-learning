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

Thời lượng ước tính: **80–100 phút**, gồm lúc đếm răng trên một hộp giảm tốc các bạn đang có, hoặc trên một ảnh rõ của hộp ấy.

## Mục tiêu học

Hết bài này, các bạn tính được tỉ số truyền từ số răng, dự đoán góc đầu ra cho một góc đầu vào cho trước, và giữ đúng dấu của mỗi cặp ăn ngoài. Các bạn nói được một cấp worm dùng để làm gì, nêu được tỉ số hành tinh trong sách trong khi vẫn tin con số đóng trên động cơ TT, và cảm được độ rơ (backlash) như chuyển động mất đi, hiện thành xung encoder khi robot đảo chiều.

## Kiến thức cần có

Các bạn đo được khổ vết và bán kính lăn (Bài 01) và biết vít cố định trục phải ngồi trên mặt vát chữ D (Bài 02). Số răng là số nguyên. Một phép chia trên máy tính là đủ.

## Vì sao bài này quan trọng với Capstone A và ROS

Encoder ở Chương 04 đếm trục động cơ, đôi khi đếm một trục nằm giữa đường trong hộp số. Bánh chạm sàn đã bị làm chậm bởi tỉ số truyền $$i$$. `diff_drive_controller` chỉ đổi xung thành mét sau khi cả tỉ số ấy và bán kính lăn đều đúng. Đổi chỗ bánh nào được gọi là đầu vào thì các bạn đảo $$i$$. Quãng đường trong odometry khi đó sai một thừa số $$i^2$$: tỉ số thật bằng 3 mà lưu thành $$1/3$$ sẽ kéo hoặc nén hành trình theo hệ số 9. Vòng tròn các bạn thấy vì khổ vết sai ở Bài 01 có một người anh em ở đây: robot có tỉ lệ bản đồ đơn giản là một con số sai. Ghi $$i$$ cạnh $$b$$ và $$r$$ trong `lab-notes.md`.

## Cặp ăn, worm, hành tinh, và vùng chết

Với một cặp bánh răng trụ, tỉ số truyền là

$$
i = \frac{N_{\text{out}}}{N_{\text{in}}} = \frac{\omega_{\text{in}}}{\omega_{\text{out}}}.
$$

$$N$$ là số răng. Mô-men ở đầu ra tăng khi tốc độ giảm, trừ ma sát trong cặp ăn và trong bạc đạn. Một bánh dẫn 12 răng kéo một bánh 36 răng có $$i = 36/12 = 3$$. Ba vòng động cơ cho một vòng bánh xe. Mô-men bánh xe vào khoảng ba lần mô-men bánh dẫn, rồi nhỏ hơn một chút, vì răng cọ vào nhau.

Mỗi cặp ăn ngoài đảo chiều. Bánh bị dẫn quay ngược bánh dẫn. Cặp ăn thứ hai, bánh dẫn vào bánh trung gian rồi vào đầu ra, đảo hai lần, nên đầu ra quay cùng chiều đầu vào. Một bánh trung gian đơn đổi chiều và để nguyên tỉ số, miễn nó là một bánh, không phải hai bánh khóa cùng nhau với số răng khác nhau. Bánh răng kép thì nhân tỉ số. Nếu các bạn còn có tỉ số hộp giảm tốc và tỉ số đai từ Bài 04, bánh xe thấy tích

$$
i_{\text{wheel}} = i_{\text{gearbox}} \cdot i_{\text{belt}}.
$$

Quên một trong hai thừa số là lỗi tỉ lệ kinh điển.

Cặp worm là một trục vít ăn với bánh vít. Tỉ số cao, thường hàng chục trên một trong một cấp, đó là lý do một cánh tay nhỏ giữ được tư thế khi nguồn động cơ sụt: nhiều cặp worm không bị dẫn ngược. Chúng cũng kém hiệu suất. Một phần lớn công suất điện các bạn đã dự trù ở Chương 05 thành nhiệt trong cặp ăn. Đó là trao đổi hợp lý trên một gắp phải giữ khép, và là trao đổi tệ trên bánh chủ động của Capstone A, nơi các bạn muốn pin thành chuyển động. Thử đầu ra worm: thường không xoay được từ phía bánh bằng ngón tay.

Một bộ hành tinh nhét mặt trời, các hành tinh trên cần mang, và vành răng vào trong đường kính của vành. Trong trường hợp sách giáo khoa, vành cố định, mặt trời là đầu vào, cần mang là đầu ra. Tỉ số là

$$
i = 1 + \frac{N_{\text{ring}}}{N_{\text{sun}}}.
$$

Công thức ấy là một cấp được vẽ trong sách. Hộp giảm tốc TT kim loại có thể là chồng hành tinh hoặc chồng bánh trụ, và con số đóng trên động cơ, thường 1:48 hoặc 1:90 hoặc 1:120, đã gồm mọi cấp nhà máy đặt bên trong. Tin dấu đóng cho động cơ ấy. Dùng công thức đếm răng khi nhìn thấy bánh răng, và dùng dấu đóng khi không nhìn thấy.

Độ rơ (backlash) là chuyển động mất đi khi mô-men đảo chiều. Răng được cắt hơi mỏng để không kẹt, và khe ấy hiện ra như một khoảng dừng ở đầu cú quay. Lắc trục ra trong khi giữ trục vào: bánh dịch vài độ trước khi trục động cơ buộc phải động. Xung encoder ghi trong khoảng lắc ấy là một độ lệch, một số đếm nhỏ không tương ứng chuyển động trên sàn. Các bạn sẽ không loại được độ rơ khỏi hộp TT đúc. Các bạn sẽ đo nó, ước bằng mắt theo độ, và tránh những mẹo điều khiển đảo chiều vài miligiây một lần.

![Chuỗi bánh răng kép: số răng đặt tỉ số, mỗi cặp ăn ngoài đảo chiều]({{ site.imgurl }}/generated/gear_train_ratio.png)

Hình cho thấy vì sao phải gọi tên đầu vào trước khi chia. Đi theo mô-men từ động cơ tới bánh, nhân $$N_{\text{out}}/N_{\text{in}}$$ của từng cấp, và đếm số cặp ăn ngoài nếu các bạn cần biết bánh lăn chiều nào. Một bánh trung gian vẽ giữa hai bánh là bộ sửa chiều. Nó không phải thừa số thêm, trừ khi hai phía của nó khác số răng.

## Ví dụ tính tay

Bánh dẫn $$N_{\text{in}} = 12$$, bánh bị dẫn $$N_{\text{out}} = 36$$.

$$
i = \frac{36}{12} = 3.
$$

Xoay bánh dẫn $$90^\circ$$. Đầu ra xoay

$$
\theta_{\text{out}} = \frac{90^\circ}{3} = 30^\circ,
$$

theo chiều ngược, vì có một cặp ăn ngoài. Ba vòng đủ của động cơ, $$1080^\circ$$, đưa bánh xe đi đúng một vòng. Nếu đảo tên và lưu $$i = 12/36 = 1/3$$, một quãng đường bánh được lệnh sẽ sai theo

$$
i_{\text{true}}^{2} = 9.
$$

Dài gấp chín, hoặc ngắn còn một phần chín, tùy phía phần mềm nào đang nhân. Cách sửa là chỉ vào bánh dẫn, nói to “đầu vào”, rồi mới chia.

Tỉ số TT đóng dấu 1:48 là con số các bạn giữ, kể cả khi hình hành tinh trong đầu gợi $$1 + N_{\text{ring}}/N_{\text{sun}}$$. Dấu đóng đã làm phép tính ấy cho những cấp các bạn không nhìn thấy.

## Lab: đếm, dự đoán, đối chiếu

### An toàn

Nguồn tắt. Răng bánh kẹp ngón. Nếu mở hộp số, mỡ trơn và các phe nhỏ bắn ra; đếm qua một ảnh rõ là đủ cho bài này. Không chạy động cơ bằng pin khi ngón tay còn trong cặp ăn.

### BOM

| Hạng mục | Vai trò |
|------|------|
| Một hộp giảm tốc, một cặp bánh rời, hoặc một ảnh sắc của bánh các bạn có | Số răng |
| Bút và giấy | Tỉ số và góc |
| `lab-notes.md` | Con số ROS sẽ dùng lại |

### Các bước

1. Gọi tên bánh đầu vào, bánh phía động cơ. Gọi tên bánh đầu ra, bánh phía bánh xe.
2. Đếm răng. Trên động cơ TT kín, đọc dấu đóng (1:48 hoặc bất cứ số nào được in) và nói rõ là đang đọc dấu.
3. Tính $$i = N_{\text{out}}/N_{\text{in}}$$, hoặc chép dấu đóng. Ghi bao nhiêu cặp ăn ngoài đảo chiều.
4. Dự đoán góc đầu ra cho đầu vào $$90^\circ$$: $$\theta_{\text{out}} = 90^\circ / i$$.
5. Nếu bánh đang trong tay, xoay đầu vào khoảng một phần tư vòng dựa vào một kim chỉ và đối chiếu. Lắc đầu ra và ước độ rơ theo độ. Ước bằng mắt là đủ.
6. Nếu chỉ có bản vẽ, dự đoán trên giấy là sản phẩm nộp. Dán nhãn “bản vẽ”.

### Kết quả mong đợi

Một $$i$$ đã viết, một ghi chú chiều quay, và một góc dự đoán. Với cặp 12 và 36, $$i = 3$$ và $$\theta_{\text{out}} = 30^\circ$$ ngược chiều đầu vào. Răng đúc trên hộp thật nên rơi trong khoảng 10 phần trăm so với dấu đóng khi các bạn kiểm đúng cách ở Bài 08. Độ rơ vài độ tại bánh là chuyện bình thường.

### Lỗi thường gặp

| Các bạn thấy | Thường nghĩa là |
|--------------|------------------------|
| Tỉ số ra nhỏ hơn 1 trên hộp số lẽ ra phải làm chậm động cơ | Các bạn đã gọi bánh phía xe là đầu vào |
| Chiều bánh xe làm các bạn ngạc nhiên | Quên một cặp ăn ngoài, hoặc đếm bánh trung gian như một lần đổi tỉ số |
| Đầu ra dịch vài độ trước khi đầu vào buộc phải động | Độ rơ; ghi lại, đừng “sửa” bằng keo |
| Dấu đóng nói 1:48 mà công thức một cấp của các bạn ra 4 | Các bạn đang nhìn một cấp của một chồng; tin dấu đóng |

## Mua ở Việt Nam / Where to buy in Vietnam

Chuỗi bánh răng của Capstone A đã nằm trong động cơ giảm tốc TT. Mua động cơ có tỉ số in trên vỏ, và có encoder nếu mua được, để xung của Chương 04 có trục để đếm. Bánh răng nhựa rời dùng cho lab đếm răng nếu động cơ của các bạn bị kín.

| Mua gì | Từ khóa | Khoảng giá (VND) | Ghi chú |
|------|----------|------------------|-------|
| Động cơ giảm tốc TT có encoder | `động cơ giảm tốc TT encoder` | 45.000–120.000 mỗi cái | Đọc dấu đóng: 1:48 là phổ biến |
| Bộ bánh răng nhựa | `bánh răng nhựa robot` | 20.000–60.000 | Hữu ích khi hộp kín mà vẫn muốn đếm răng |

Các trang tìm:

- [Hshop](https://hshop.vn/search?q=%C4%91%E1%BB%99ng+c%C6%A1+gi%E1%BA%A3m+t%E1%BB%91c+TT)
- [Shopee](https://shopee.vn/search?keyword=%C4%91%E1%BB%99ng%20c%C6%A1%20gi%E1%BA%A3m%20t%E1%BB%91c%20TT%20encoder)
- [Lazada](https://www.lazada.vn/catalog/?q=%C4%91%E1%BB%99ng%20c%C6%A1%20TT%20encoder)
- [Thế Giới IC](https://www.thegioiic.com/search?q=%C4%91%E1%BB%99ng%20c%C6%A1%20gi%E1%BA%A3m%20t%E1%BB%91c)

Giá dịch chuyển. Khớp trục với bánh đã mua ở Bài 01 trước khi trả tiền.

## Bài tập

1. Một bánh dẫn 15 răng kéo một bánh 60 răng. Tìm $$i$$, góc đầu ra cho một vòng động cơ, và chiều so với động cơ.
2. Cặp ấy được nối tiếp bởi một bánh trung gian đơn 20 răng rồi mới tới bánh 60 răng, nên bánh dẫn chỉ ăn với bánh trung gian. $$i$$ bây giờ là bao nhiêu, và đầu ra quay chiều nào so với bánh dẫn?
3. Một cấp hành tinh vành cố định có $$N_{\text{sun}} = 12$$ và $$N_{\text{ring}} = 36$$. Tính $$i$$ theo sách. Động cơ TT của các bạn đóng dấu 1:48. Số nào đi vào `lab-notes.md` cho động cơ ấy?
4. Các bạn lưu $$i = 1/4$$ cho một hộp số có tỉ số thật bằng 4. Quãng đường odometry sai theo hệ số nào?
5. Các bạn giữ trục động cơ mà bánh vẫn lắc khoảng $$8^\circ$$. Chuyển động ấy gọi là gì, và nó làm gì với số xung lấy lúc robot bắt đầu một cú quay?

### Gợi ý đáp án

1. $$i = 60/15 = 4$$. Một vòng động cơ cho $$360^\circ/4 = 90^\circ$$ ở đầu ra, ngược chiều động cơ, một cặp ăn ngoài. 2. Bánh trung gian đơn để $$i = 4$$ và thêm một lần đảo chiều, nên đầu ra quay cùng chiều bánh dẫn. 3. Cấp theo sách: $$i = 1 + 36/12 = 4$$. Với động cơ đã đóng dấu, ghi 48. Dấu đóng gồm cả chồng bánh. 4. Theo $$i^2 = 16$$. 5. Độ rơ (backlash). Những độ ấy có thể hiện thành xung, hoặc thành một khoảng dừng trước khi xung làm bánh dịch, nên đầu cú quay bị lệch. Ghi góc; đừng dán keo vào cặp ăn.

## Đọc thêm

- [SDP-SI, Elements of Metric Gear Technology](https://www.sdp-si.com/resources/elements-of-metric-gear-technology/index.php) — hình học răng, tỉ số và độ rơ từ một danh mục bánh răng vừa bán vừa dạy.
- [Gear ratio](https://en.wikipedia.org/wiki/Gear_ratio) — định nghĩa $$N_{\text{out}}/N_{\text{in}}$$ và chuỗi bánh kép.
- [Worm drive](https://en.wikipedia.org/wiki/Worm_drive) — tỉ số cao, hiệu suất, và vì sao nhiều cặp worm không chịu bị dẫn ngược.
