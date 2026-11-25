---
layout: post
title: "Cơ cấu thanh, cam, đai và bánh răng-thanh răng"
chapter: "06"
order: 4
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter06
lesson_type: required
draft: false
---

Thời lượng ước tính: **80–100 phút**, bao gồm thực hành dựng cơ cấu bốn thanh bằng bìa cứng hoặc đếm răng pulley GT2 nếu bạn có sẵn linh kiện.

Động cơ chỉ biết làm một việc duy nhất: **quay tròn**. Nhưng robot trong đời thực lại cần gắp đồ song song, nâng hạ thẳng đứng, bước đi như chân nhện, hoặc truyền lực từ động cơ đặt gọn trong thân ra tận khớp cổ tay cách đó 30 centimet. Khoảng trống giữa *chuyển động quay tròn đơn điệu của động cơ* và *mọi quỹ đạo phức tạp của robot* được lấp đầy bởi bốn họ cơ cấu kinh điển: **cơ cấu thanh (linkages), đai răng (timing belts), cam và bánh răng–thanh răng (rack-and-pinion)**.

## Kiến thức cần nhớ: Biến đổi chuyển động trong thiết kế cơ cấu robot

### 1. Cơ cấu 4 khâu (Four-Bar Linkage) và định lý Grashof
Cơ cấu 4 khâu là "viên gạch Lego" linh hoạt nhất của cơ học máy: dùng để tạo tay kẹp song song, chân robot biết bước (cơ cấu Klann/Jansen) hoặc tay nâng không bị nghiêng góc. Gọi độ dài khâu ngắn nhất là $$s$$, dài nhất là $$l$$, hai khâu còn lại là $$p, q$$. **Điều kiện Grashof** phát biểu rằng ít nhất một khâu có thể quay tròn liên tục $$360^\circ$$ khi và chỉ khi:
$$s + l \le p + q.$$

### 2. Đai răng (GT2 Timing Belt) và Truyền động bánh răng–thanh răng
- **Đai răng (như GT2, bước răng $$2\text{ mm}$$):** truyền lực êm, không trượt, gần như không có backlash và cho phép đặt động cơ nặng ở sát gốc (giảm quán tính cánh tay!).
- **Bánh răng – thanh răng (Rack & Pinion):** biến chuyển động quay trực tiếp thành tịnh tiến dọc thanh răng, chịu tải lớn và dễ kéo dài hành trình hơn trục vitme.

### 3. Cơ cấu Cam — "bộ nhớ cơ khí" lập trình sẵn quỹ đạo
Một đĩa cam được cắt biên dạng phi tròn có thể biến tốc độ quay đều thành chuyển động nâng–dừng–hạ phức tạp mà không cần thêm cảm biến hay phần mềm — rất hữu ích cho các cơ cấu kẹp nhanh hoặc nạp đạn lặp đi lặp lại trong thi đấu robotics.

### Giải thích: Cầm tay tính hành trình đai răng GT2 và kiểm tra điều kiện Grashof

**Phần A — Tính bước dịch chuyển tuyến tính của hệ truyền động đai GT2:**
Một trục trượt tuyến tính (giống trục X/Y máy in 3D) dùng đai răng **GT2** (bước răng $$p = 2{,}0\text{ mm}$$) kéo bởi puly **$$Z = 20$$ răng**, gắn trên động cơ bước chạy vi bước **1/16** ($$3\,200\text{ vi bước/vòng}$$):
1. **Quãng đường tịnh tiến mỗi vòng quay động cơ:**
   $$S_{\text{vòng}} = Z \times p = 20 \times 2{,}0 = 40{,}0\text{ mm/vòng}.$$
2. **Độ phân giải tuyến tính lý thuyết mỗi vi bước:**
   $$\Delta x = \frac{40{,}0\text{ mm}}{3\,200} = 0{,}0125\text{ mm/vi bước}\;(12{,}5\,\mu\text{m}!).$$
3. **Để trượt chính xác $$150\text{ mm}$$:** vi điều khiển cần phát đúng $$\frac{150}{0{,}0125} = 12\,000$$ xung `STEP`.

**Phần B — Kiểm tra nhanh một cơ cấu 4 khâu có quay tròn liên tục được không?**
Giả sử bạn thiết kế cơ cấu 4 khâu với chiều dài các thanh (cm): $$s = 3,\; l = 10,\; p = 7,\; q = 8$$:
- Tổng ngắn nhất + dài nhất: $$s + l = 3 + 10 = 13\text{ cm}$$.
- Tổng hai khâu còn lại: $$p + q = 7 + 8 = 15\text{ cm}$$.
- Vì $$13 \le 15$$, cơ cấu **thỏa điều kiện Grashof** — cố định một khâu kề khâu ngắn nhất $$s = 3$$ sẽ cho ta cơ cấu tay quay–con lắc (*crank-rocker*) quay trọn $$360^\circ$$ mượt mà không bị kẹt chết!

## Mục tiêu học

Sau bài này, các bạn kiểm tra được cơ cấu bốn thanh bằng điều kiện Grashof để nhận diện dạng maniven – cần lắc, tính được tỉ số truyền của bộ truyền đai răng từ số răng pulley, và quy đổi đường kính vòng chia của bánh răng dẫn thành hành trình thanh răng trên mỗi vòng quay. Các bạn cũng mô tả được đoạn nâng và đoạn dừng của cam, đồng thời biết nhân gộp tỉ số truyền của đai (nếu có) vào tỉ số tổng từ encoder tới bánh xe trước khi cấu hình ROS.

## Kiến thức cần có

Các bạn đã biết tính tỉ số truyền $$i = N_{\text{out}}/N_{\text{in}}$$ (Bài 03) và nắm rõ khổ vết $$b$$ (Bài 01). Vật liệu thực hành chỉ cần bìa cứng, bốn đinh ghim và thước kẻ; pulley GT2 là linh kiện tùy chọn.

## Vì sao bài này quan trọng với Capstone A và ROS

Hệ truyền động của Capstone A dùng hai bánh xe gắn qua hộp giảm tốc chứ không dùng cơ cấu thanh. Tuy nhiên, các cơ cấu trong bài này giúp bạn hiểu bản chất các loại khớp sẽ mô tả trong ROS về sau. Trong ROS, mỗi khớp được định nghĩa bằng tên, loại khớp và cặp giới hạn chuyển động. Một cơ cấu bốn thanh chỉ có thể lắc qua lại bắt buộc phải được khai báo giới hạn góc tương ứng; nếu không, bộ điều khiển sẽ ra lệnh tư thế vượt quá khả năng cơ khí mà mô hình bìa cứng đã chỉ ra.

Nếu bạn đặt thêm bộ truyền đai GT2 giữa động cơ và bánh xe, tỉ số của đai sẽ nhân thêm vào tỉ số hộp giảm tốc ở Bài 03. Bỏ quên tỉ số đai sẽ khiến cùng một số xung encoder tương ứng với góc bánh sai lệch, làm tỉ lệ odometry sai giống hệt trường hợp đảo ngược $$i$$. Cơ cấu cam thường xuất hiện ở công tắc hành trình hoặc một số tay kẹp; dù không cần cam để hoàn thành Capstone A, bạn cần hình thành thói quen ghi đầy đủ mọi tỉ số truyền nằm giữa encoder và mặt sàn.

## Bốn thanh, đai răng, thanh răng, và cam

Cơ cấu bốn thanh gồm bốn khâu cứng liên kết bằng các khớp bản lề tạo thành một vòng kín. Gọi chiều dài khâu ngắn nhất là $$s$$, khâu dài nhất là $$l$$, hai khâu còn lại là $$p$$ và $$q$$. Điều kiện Grashof để ít nhất một khâu có thể quay tròn đủ một vòng tương đối so với các khâu khác (trường hợp vận hành ổn định) là:

$$
s + l < p + q.
$$

Giáo trình thường viết dưới dạng $$\le$$, nhưng trường hợp dấu bằng tạo ra cơ cấu điểm đổi (change-point): các khâu có thể duỗi thẳng hàng rồi kẹt hoặc đổi nhánh chuyển động, nên cần kiểm tra kích thước rất kỹ trước khi sử dụng. Khi bất đẳng thức $$s + l < p + q$$ thỏa mãn và khâu ngắn nhất nằm liền kề khâu cố định (khâu nền), ta thu được cơ cấu maniven – cần lắc: khâu ngắn quay tròn liên tục, còn khâu đối diện lắc qua lại (tương tự cần gạt mưa ô tô). Ngược lại, nếu $$s + l > p + q$$, không khâu nào quay hết vòng; cơ cấu chỉ lắc trong một góc giới hạn và động cơ sẽ bị kẹt tải nếu bị lệnh quay tròn.

![Cơ cấu bốn thanh: maniven quay, cần lắc đung đưa, thanh nối ghép chúng]({{ site.imgurl }}/generated/four_bar_linkage.png)

Hãy quan sát sơ đồ như một mạch kín: khâu nền gắn cố định vào khung, maniven nối với động cơ, cần lắc dao động qua lại và thanh nối liên kết hai khâu đó. Chỉ cần đổi khâu nào được cố định làm khâu nền, kiểu chuyển động của cả cơ cấu sẽ thay đổi dù chiều dài bốn thanh giữ nguyên.

Bộ truyền đai răng (phổ biến nhất trên robot nhỏ là chuẩn GT2) có tỉ số truyền xác định trực tiếp từ số răng hai pulley:

$$
i = \frac{N_{\text{driven}}}{N_{\text{driver}}}.
$$

Khi đai đủ căng và răng ăn khớp tốt, bộ truyền hầu như không bị trượt. Ở cấu hình đai hở thông thường (đai vòng quanh hai pulley mà không bắt chéo), hai pulley quay cùng chiều nhau; chiều quay chỉ đảo ngược khi đai được dẫn qua mặt lưng của một pulley trung gian. Chiều dài dây đai cố định khoảng cách tâm giữa hai trục, nên không thể thay đổi tỉ số truyền bằng cách kéo giãn hai động cơ ra xa nhau. Đai quá căng sẽ làm mòn nhanh bạc lót (vốn đã quyết định giữ nguyên ở Bài 02), còn đai quá lỏng sẽ bị nhảy răng khi chịu mô-men. Hiện tượng nhảy răng gây ra lỗi giống độ rơ — có khoảng trễ rồi nhảy bậc — mà encoder trên trục động cơ không hề phát hiện. Để kiểm tra độ căng, hãy búng nhẹ vào nhánh đai: âm trầm và căng vừa là đạt, âm ngân cao là quá căng, còn dây chùng nhão là quá lỏng.

![Đai GT2 và pulley: số răng đặt tỉ số, độ căng quyết định răng có còn ăn]({{ site.imgurl }}/generated/belt_pulley.png)

Cơ cấu bánh răng – thanh răng biến chuyển động quay thành chuyển động tịnh tiến thẳng. Sau mỗi vòng quay của bánh răng dẫn, thanh răng dịch chuyển một đoạn đúng bằng chu vi vòng chia:

$$
x = \pi d,
$$

trong đó $$d$$ là đường kính vòng chia của bánh dẫn (đường kính tại vị trí răng thực sự ăn khớp lăn). Cơ cấu này thường dùng cho ray trượt thẳng trên tay máy nhỏ hoặc bệ cảm biến, không bắt buộc cho Capstone A, nhưng có cùng bản chất tính toán với bán kính lăn của bánh xe.

Cam là một chi tiết quay có biên dạng tạo hình tỳ lên con đội. Đoạn nâng (rise) đẩy con đội dịch chuyển, còn đoạn dừng (dwell) giữ con đội đứng yên dù cam vẫn đang quay. Trong robot, cam đôi khi xuất hiện ở cơ cấu giới hạn hành trình hoặc tay kẹp cần giữ trạng thái đóng. Đoạn dừng đóng vai trò như một giới hạn chuyển động cứng; trong URDF, bạn thường mô tả nó bằng giới hạn khớp hoặc giản lược thành một cơ cấu đơn giản. Capstone A không yêu cầu thiết kế cam.

Bất kỳ tầng truyền động nào đặt giữa encoder và lốp xe đều phải được ghi nhận vào tỉ số truyền tổng. Chẳng hạn, hộp số 1:48 kết hợp với bộ đai tỉ số 2 cho tỉ số tổng tại bánh xe là $$i = 96$$. Đây chính là giá trị mà `diff_drive_controller` cần nhận để tính odometry chính xác.

## Ví dụ tính tay

**1. Kiểm tra điều kiện Grashof:** Cho bốn khâu có chiều dài $$s = 30$$ mm, $$p = 55$$ mm, $$q = 70$$ mm và $$l = 90$$ mm. Ta có:

$$
s + l = 120\ \text{mm}, \qquad p + q = 125\ \text{mm}.
$$

Vì $$120 < 125$$, ít nhất một khâu quay được đủ vòng. Nếu cố định khâu 70 mm và dẫn động khâu 30 mm (maniven), khâu đối diện sẽ lắc qua lại. Ngược lại, nếu tăng khâu dài nhất lên 110 mm thì $$s + l = 140 > 125$$: điều kiện Grashof không thỏa mãn, mô hình bìa cứng sẽ bị kẹt trước khi quay hết vòng — đó chính là giới hạn khớp cảm nhận trực tiếp bằng tay.

**2. Hành trình thanh răng:** Một bánh răng dẫn có đường kính vòng chia 12 mm sẽ đẩy thanh răng đi được sau mỗi vòng quay là:

$$
x = \pi \times 12 \approx 37.7\ \text{mm}.
$$

Nửa vòng quay tương ứng hành trình khoảng 18,8 mm. Lưu ý phải dùng đường kính vòng chia thay vì đường kính đỉnh răng ngoài (lớn hơn), và luôn ghi rõ đường kính nào đã được đo.

**3. Bộ truyền đai:** Pulley gắn động cơ có 20 răng kéo pulley phía bánh xe 60 răng cho tỉ số $$i = 60/20 = 3$$, tương tự cặp bánh răng 12 và 36 răng. Nếu có hộp giảm tốc phía trước pulley động cơ, cần nhân thêm tỉ số hộp số vào kết quả này.

## Lab: bìa, hoặc pulley, hoặc phác họa

### An toàn

Đinh ghim có đầu nhọn; luôn cắm gọn trên bìa, không bỏ vào túi áo quần. Nếu thao tác căng dây đai GT2 thật, đảm bảo đã tắt nguồn và giữ ngón tay tránh xa vùng ăn khớp pulley vì đai quá căng có thể làm bật vít cố định trục bị lỏng.

### BOM

| Hạng mục | Vai trò |
|------|------|
| Bìa, bốn đinh ghim hoặc chốt, thước | Cơ cấu bốn thanh |
| Hoặc một cặp pulley GT2 và đai | Đếm răng |
| Bút chì | Phác cơ cấu không thỏa Grashof và số thanh răng |
| `lab-notes.md` | Chiều dài, $$i$$, hoặc hành trình thanh răng |

### Các bước

1. Cắt bốn thanh bìa với khoảng cách tâm lỗ đúng như ví dụ: 30, 55, 70 và 90 mm. Ghim chúng thành vòng kín, cố định thanh 70 mm xuống mặt bàn rồi xoay maniven 30 mm để quan sát chuyển động lắc của khâu đối diện.
2. Thay khâu dài nhất thành 110 mm (giữ nguyên ba khâu kia) và thử xoay để cảm nhận vị trí kẹt. Phác họa cả hai cơ cấu vào sổ và ghi rõ trường hợp nào thỏa mãn $$s + l < p + q$$.
3. Nếu có sẵn phần cứng GT2, đếm số răng pulley dẫn và pulley bị dẫn, tính tỉ số $$i$$ và ghi nhận độ căng khi búng đai (chùng, ngân cao hay trầm vừa). Bạn có thể bỏ bước cắt bìa nếu thực hành trên pulley, nhưng vẫn cần phác họa một cơ cấu thỏa và một cơ cấu không thỏa Grashof kèm kích thước từng khâu.
4. Nếu không có cả pulley lẫn đinh ghim, hãy tính ví dụ thanh răng đường kính 12 mm và vẽ đúng tỉ lệ cả hai cơ cấu bốn thanh trên giấy, dán nhãn “bản vẽ”.
5. Viết một câu kết luận về tỉ số truyền tổng từ encoder tới bánh xe của Capstone A (chỉ nhân thêm tỉ số đai nếu robot của bạn thực sự dùng đai).

### Kết quả mong đợi

Hai hình phác họa có dán nhãn rõ ràng (một cơ cấu quay đủ vòng và một cơ cấu bị kẹt), hoặc tỉ số GT2 kèm hai hình phác họa đó. Số liệu hành trình thanh răng 37,7 mm/vòng được ghi chú nếu bạn thực hiện bước tính này. Tỉ số encoder-tới-bánh khớp với dấu đóng ở Bài 03 (hoặc nhân thêm tỉ số đai nếu có).

### Lỗi thường gặp

| Các bạn thấy | Thường nghĩa là |
|--------------|------------------------|
| “Maniven” không quay hết | $$s + l$$ lớn hơn $$p + q$$, hoặc lỗ cách đầu thanh quá xa nên chiều dài thật khác nhãn |
| Đai nhảy răng dưới mô-men ngón tay | Quá lỏng, hoặc răng không khớp bước đai |
| Bạc nóng và đai ngân | Quá căng |
| Góc bánh từ xung chỉ bằng một nửa những gì sàn cho thấy | Một đai 2:1 bị bỏ khỏi $$i$$ |

## Mua ở Việt Nam / Where to buy in Vietnam

Bìa cứng là đủ cho bài thực hành này. Chỉ nên mua đai và pulley GT2 nếu thiết kế truyền động của bạn thực sự dùng đai; hai bánh động cơ TT tiêu chuẩn của Capstone A thường không cần.

| Mua gì | Từ khóa | Khoảng giá (VND) | Ghi chú |
|------|----------|------------------|-------|
| Đai GT2 | `dây đai GT2` | 15.000–40.000 | Nêu chiều dài và bề rộng, thường 6 mm |
| Pulley GT2 | `pulley GT2` | 8.000–30.000 | Số răng là tỉ số; khớp lỗ trục |
| Bộ thanh răng và bánh răng | `thanh răng bánh răng` | 30.000–90.000 | Tùy chọn; đường kính vòng chia đi vào $$x = \pi d$$ |

Các trang tìm mua:

- [Hshop](https://hshop.vn/search?q=d%C3%A2y+%C4%91ai+GT2)
- [Shopee](https://shopee.vn/search?keyword=d%C3%A2y%20%C4%91ai%20GT2)
- [Lazada](https://www.lazada.vn/catalog/?q=d%C3%A2y%20%C4%91ai%20GT2)
- [Thế Giới IC](https://www.thegioiic.com/search?q=GT2)

Giá bán có thể thay đổi theo thời điểm. Tránh mua các tin đăng pulley không ghi rõ số răng và đường kính lỗ trục.

## Video tham khảo

- **Xem trước:** [Four-Bar Linkage and Its Three Possible Motions](https://www.youtube.com/watch?v=EBqrDj-Wkiw) — mecademie, tiếng Anh. Giới thiệu cơ cấu bốn thanh và ba kiểu chuyển động đặc trưng; hãy đếm số khâu trước khi dự đoán quỹ đạo đầu khâu.
- [Basic Mechanisms:  4 Bar Linkage](https://www.youtube.com/watch?v=1Ty_1LF3Qv0) — Mr. Dillman's Tech Channel, tiếng Anh. Video ngắn minh họa cơ cấu bốn thanh hoạt động thực tế để dễ nhận diện khâu cố định.

Các video ngắn (Facebook Reel) dưới đây của Hoàng Quân (Cơ điện tử ICTU, [chinbi.com](https://chinbi.com)):

- [Test thiết kế chân](https://www.facebook.com/reel/1615249330240344) — Chú thích: test thiết kế chân. Minh họa việc kiểm tra cơ cấu chân trực tiếp trên bàn trước khi ghép thành chuỗi động học hoàn chỉnh.
- [Một chân, ba bậc tự do](https://www.facebook.com/reel/2974137376266883) — Chú thích: một chân có 3 bậc tự do. Ba khớp tương ứng với ba biến khớp; phần biến đổi sang quỹ đạo đầu chân sẽ được học ở các chương sau.

## Bài tập

1. Cho cơ cấu bốn thanh có chiều dài các khâu lần lượt là 25 mm, 40 mm, 45 mm và 60 mm. Điều kiện $$s + l < p + q$$ có thỏa mãn không? Nếu cố định khâu 45 mm và dẫn động khâu 25 mm, bạn dự đoán chuyển động gì?
2. Cho bốn khâu dài 40 mm, 50 mm, 55 mm và 120 mm. Cơ cấu này có khâu maniven nào quay đủ vòng không?
3. Một hệ truyền động gồm hộp giảm tốc đóng dấu 1:30 nối tiếp với pulley động cơ 16 răng kéo pulley bánh xe 48 răng. Tính tỉ số truyền tổng $$i$$ từ trục động cơ tới bánh xe.
4. Đường kính vòng chia của bánh răng dẫn là 20 mm. Thanh răng dịch chuyển bao xa trong một vòng quay và trong một phần tư vòng quay?
5. Một cam có đoạn nâng kéo dài $$90^\circ$$ và đoạn dừng kéo dài $$180^\circ$$ tiếp theo. Con đội làm gì trong đoạn dừng, và Capstone A có cần cơ cấu này không?

### Gợi ý đáp án

1. Ta có $$s + l = 25 + 60 = 85$$ mm và $$p + q = 40 + 45 = 85$$ mm. Trường hợp dấu bằng là cơ cấu điểm đổi (sat biên Grashof), dễ bị duỗi phẳng và kẹt. Khâu ngắn vẫn có xu hướng làm maniven nhưng thiếu ổn định; nên tăng nhẹ chiều dài một khâu trung gian nếu cần cơ cấu quay tin cậy.
2. Ta có $$s + l = 160$$ mm và $$p + q = 105$$ mm ($$s + l > p + q$$), nên không khâu nào quay được đủ vòng.
3. Tỉ số bộ đai là $$i_{\text{belt}} = 48/16 = 3$$; nhân với hộp giảm tốc 30 cho tỉ số tổng $$i = 90$$.
4. Hành trình mỗi vòng là $$x = \pi \times 20 \approx 62.8$$ mm; một phần tư vòng tương ứng khoảng 15,7 mm.
5. Trong đoạn dừng, con đội đứng yên dù cam vẫn đang quay. Capstone A không cần cơ cấu cam.

## Đọc thêm

- [Four-bar linkage](https://en.wikipedia.org/wiki/Four-bar_linkage) — phân loại maniven – cần lắc và sự thay đổi chuyển động khi đổi khâu cố định.
- [Grashof’s law](https://en.wikipedia.org/wiki/Grashof%27s_law) — chi tiết phép thử điều kiện $$s + l$$, bao gồm trường hợp dấu bằng.
- [Timing belt (đai răng)](https://en.wikipedia.org/wiki/Timing_belt_(camshaft)) — nguyên lý ăn khớp răng và lý do đai chùng bị nhảy răng (bài viết dùng ví dụ động cơ đốt trong nhưng nguyên lý ăn khớp tương tự đai GT2).
