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

Thời lượng ước tính: **80–100 phút**, gồm một cơ cấu bốn thanh bằng bìa, hoặc một lần đếm răng pulley GT2 nếu các bạn có sẵn.

## Mục tiêu học

Hết bài này, các bạn kiểm một cơ cấu bốn thanh với điều kiện Grashof và nhận ra kiểu maniven-cần lắc, tính tỉ số đai răng từ số răng pulley, và đổi đường kính vòng chia của bánh dẫn thành hành trình thanh răng trên mỗi vòng. Các bạn mô tả được đoạn nâng và đoạn dừng của một cam, và viết được tỉ số thêm từ encoder tới bánh mà một đai sẽ chen vào trước khi ROS nhìn thấy khớp.

## Kiến thức cần có

Các bạn lập được tỉ số truyền $$i = N_{\text{out}}/N_{\text{in}}$$ (Bài 03) và biết khổ vết $$b$$ từ Bài 01. Bìa cứng, bốn đinh ghim và một thước là đủ phần cứng. Pulley GT2 là tùy chọn.

## Vì sao bài này quan trọng với Capstone A và ROS

Truyền động của Capstone A là hai bánh đã qua hộp giảm tốc, không phải một cơ cấu thanh. Những cơ cấu trong bài này vẫn quyết định các bạn có hiểu các khớp sẽ mô tả về sau hay không. Trong ROS, một khớp là một cái tên, một kiểu, và một cặp giới hạn. Cơ cấu bốn thanh chỉ lắc được thì phải được gán những giới hạn ấy, nếu không bộ điều khiển sẽ ra lệnh một tư thế mà tấm bìa đã chứng minh là không thể. Một đai GT2 nằm giữa động cơ và bánh nhân thêm tỉ số hộp giảm tốc từ Bài 03. Quên đai thì cùng một số xung lại nghĩa là góc bánh sai, nên tỉ lệ odometry trôi đúng như khi $$i$$ bị đảo. Cam xuất hiện trong cơ cấu hành trình và trong một số gắp. Các bạn không cần cam để xong Capstone A. Các bạn cần thói quen ghi mọi tỉ số nằm giữa encoder và sàn.

## Bốn thanh, đai răng, thanh răng, và cam

Cơ cấu bốn thanh là bốn khâu cứng được chốt thành một vòng kín. Gọi chiều ngắn nhất là $$s$$, chiều dài nhất là $$l$$, hai chiều còn lại là $$p$$ và $$q$$. Điều kiện Grashof để ít nhất một khâu quay được đủ một vòng tương đối với các khâu kia, trong trường hợp các bạn muốn trên bàn, là

$$
s + l < p + q.
$$

Sách giáo khoa viết $$\le$$. Dấu bằng là cơ cấu điểm đổi: nó gập phẳng và kẹt, nên hãy coi dấu bằng là một thiết kế phải đo hai lần trước khi tin. Khi bất đẳng thức đúng và khâu ngắn nhất nằm cạnh khâu cố định, các bạn có maniven-cần lắc. Khâu ngắn quay tròn; khâu đối diện lắc. Gạt mưa kính chắn gió là chuyển động ấy. Nếu $$s + l$$ lớn hơn $$p + q$$, không khâu nào quay hết vòng. Cơ cấu chỉ lắc, và một động cơ bị lệnh quay đủ một vòng sẽ chết tải vào chốt.

![Cơ cấu bốn thanh: maniven quay, cần lắc đung đưa, thanh nối ghép chúng]({{ site.imgurl }}/generated/four_bar_linkage.png)

Đọc hình như một vòng kín. Khâu nền là khâu bắt vào khung. Maniven là khâu các bạn sẽ gắn vào động cơ. Cần lắc là khâu vẫy. Thanh nối là khâu nổi ghép hai khâu ấy. Đổi khâu nào được bắt chết sẽ đổi chuyển động, dù bốn chiều dài vẫn y nguyên.

Đai răng, trên các robot này là GT2, mang tỉ số trong số răng pulley:

$$
i = \frac{N_{\text{driven}}}{N_{\text{driver}}}.
$$

Không có trượt khi đai đã căng và răng còn ăn. Chiều quay đảo một lần, giống một cặp bánh răng ăn ngoài, trừ khi một pulley trung gian đảo lại. Chiều dài đai cố định khoảng cách tâm. Các bạn không “chỉnh tỉ số” bằng cách kéo hai động cơ ra xa nhau. Đai quá căng ăn bạc lót mà Bài 02 đã quyết định để yên. Đai lỏng nhảy răng dưới mô-men. Cú nhảy trông giống độ rơ: một vùng chết, rồi một bước nhảy, và encoder không thấy bước nhảy ấy vì pulley động cơ vẫn quay. Búng đai. Một nốt trầm căng vừa là đích. Một nốt cao ngân là quá căng. Đai oặt là quá lỏng.

![Đai GT2 và pulley: số răng đặt tỉ số, độ căng quyết định răng có còn ăn]({{ site.imgurl }}/generated/belt_pulley.png)

Bánh răng và thanh răng đổi quay thành đường thẳng. Trong một vòng của bánh dẫn, hành trình thanh răng là chu vi vòng chia,

$$
x = \pi d,
$$

trong đó $$d$$ là đường kính vòng chia của bánh dẫn, đường kính nơi răng thực sự lăn. Một ray thẳng trên cánh tay nhỏ, hoặc bệ đầu quét, là thiết bị này. Capstone A không cần. Phép tính cùng họ với bán kính lăn: chiều dài cung trên vòng chia.

Cam là một rô-to tạo hình tỳ vào con đội. Đoạn nâng nâng con đội. Đoạn dừng giữ con đội đứng yên trong khi cam vẫn quay. Robot gặp cam ở bộ hạn chế cơ khí và ở vài gắp phải dừng ở trạng thái khép. Đoạn dừng là một giới hạn chuyển động cứng. Trong URDF, các bạn diễn khoảng dừng ấy thành giới hạn khớp, hoặc thành một cơ cấu đơn giản không phải khớp tự do. Các bạn sẽ không thiết kế cam cho Capstone A.

Bất cứ thứ gì các bạn thêm vào giữa encoder và lốp, hãy ghi tỉ số. Hộp số 48, đai 2, bánh xe thấy $$i = 96$$. Tích ấy là thứ `diff_drive_controller` phải dùng. Một khớp trong ROS không phải chỗ giấu một pulley bị quên.

## Ví dụ tính tay

Grashof trước. Các chiều $$s = 30$$ mm, $$p = 55$$ mm, $$q = 70$$ mm, $$l = 90$$ mm.

$$
s + l = 120\ \text{mm}, \qquad p + q = 125\ \text{mm}.
$$

$$120 < 125$$, nên ít nhất một khâu quay đủ vòng. Cố định cạnh 70 mm và dẫn maniven 30 mm, khâu đối diện lắc: một cái gạt. Đổi khâu dài thành 110 mm thì $$s + l = 140$$ trong khi $$p + q = 125$$. Bất đẳng thức thất bại. Tấm bìa sẽ kẹt trước khi quay đủ vòng. Cú kẹt ấy là giới hạn khớp, cảm được bằng ngón tay.

Thanh răng tiếp theo. Một bánh dẫn có đường kính vòng chia 12 mm đẩy thanh răng, mỗi vòng,

$$
x = \pi \times 12 \approx 37.7\ \text{mm}.
$$

Nửa vòng khoảng 18,8 mm. Nếu bánh dẫn trên bản vẽ là đường kính ngoài và đường kính vòng chia nhỏ hơn, hành trình co theo. Dùng đường kính vòng chia, và nói các bạn đã đo đường kính nào.

Đai, để ghi sổ: pulley động cơ 20 răng và pulley bánh 60 răng cho $$i = 3$$, cùng cấu trúc với cặp bánh 12 vào 36. Ba vòng động cơ, một vòng bánh, cộng hộp giảm tốc ngồi trước pulley động cơ.

## Lab: bìa, hoặc pulley, hoặc phác họa

### An toàn

Đinh ghim nhọn. Giữ chúng trên bìa, không cho vào túi. Nếu căng một đai GT2 thật, nguồn tắt và ngón tay ra khỏi pulley. Đai quá căng có thể bắn một vít cố định trục đang lỏng.

### BOM

| Hạng mục | Vai trò |
|------|------|
| Bìa, bốn đinh ghim hoặc chốt, thước | Cơ cấu bốn thanh |
| Hoặc một cặp pulley GT2 và đai | Đếm răng |
| Bút chì | Phác cơ cấu không thỏa Grashof và số thanh răng |
| `lab-notes.md` | Chiều dài, $$i$$, hoặc hành trình thanh răng |

### Các bước

1. Cắt bốn thanh. Dùng các chiều trong ví dụ: 30, 55, 70, 90 mm giữa tâm lỗ. Ghim chúng thành vòng, cố định thanh 70 mm xuống bàn, và quay maniven 30 mm. Quan sát cần lắc.
2. Dựng lại với khâu dài nhất 110 mm, các chiều còn lại như ví dụ thất bại, và cảm cú kẹt. Phác cả hai và ghi cái nào thỏa $$s + l < p + q$$.
3. Nếu có phần cứng GT2, đếm răng pulley dẫn và pulley bị dẫn, tính $$i$$, và ghi đai đang oặt, đang ngân, hay búng được một nốt trầm. Bỏ bước bìa nếu lần đếm pulley là phép đo giàu hơn, nhưng vẫn phác một vòng thỏa Grashof và một vòng không thỏa, có chiều dài ghi trên từng khâu.
4. Nếu không có pulley cũng không có đinh ghim, tính ví dụ thanh răng 12 mm và vẽ cả hai cơ cấu bốn thanh đúng tỉ lệ. Dán nhãn trang là “bản vẽ”.
5. Viết một câu: tỉ số từ encoder tới bánh của Capstone A, chỉ gồm đai nếu robot của các bạn có đai.

### Kết quả mong đợi

Hai phác họa đã dán nhãn, một cái quay được và một cái kẹt, hoặc một tỉ số GT2 kèm những phác họa ấy. Số thanh răng 37,7 mm mỗi vòng nằm trong ghi chú nếu các bạn đã tính. Câu encoder-tới-bánh khớp dấu đóng của Bài 03, trừ khi một đai nhân thêm vào.

### Lỗi thường gặp

| Các bạn thấy | Thường nghĩa là |
|--------------|------------------------|
| “Maniven” không quay hết | $$s + l$$ lớn hơn $$p + q$$, hoặc lỗ cách đầu thanh quá xa nên chiều dài thật khác nhãn |
| Đai nhảy răng dưới mô-men ngón tay | Quá lỏng, hoặc răng không khớp bước đai |
| Bạc nóng và đai ngân | Quá căng |
| Góc bánh từ xung chỉ bằng một nửa những gì sàn cho thấy | Một đai 2:1 bị bỏ khỏi $$i$$ |

## Mua ở Việt Nam / Where to buy in Vietnam

Bìa cứng là đủ cho lab. Chỉ mua GT2 nếu truyền động của các bạn, hoặc một trục về sau, dùng đai. Hai bánh TT của Capstone A thường không dùng.

| Mua gì | Từ khóa | Khoảng giá (VND) | Ghi chú |
|------|----------|------------------|-------|
| Đai GT2 | `dây đai GT2` | 15.000–40.000 | Nêu chiều dài và bề rộng, thường 6 mm |
| Pulley GT2 | `pulley GT2` | 8.000–30.000 | Số răng là tỉ số; khớp lỗ trục |
| Bộ thanh răng và bánh răng | `thanh răng bánh răng` | 30.000–90.000 | Tùy chọn; đường kính vòng chia đi vào $$x = \pi d$$ |

Các trang tìm:

- [Hshop](https://hshop.vn/search?q=d%C3%A2y+%C4%91ai+GT2)
- [Shopee](https://shopee.vn/search?keyword=d%C3%A2y%20%C4%91ai%20GT2)
- [Lazada](https://www.lazada.vn/catalog/?q=d%C3%A2y%20%C4%91ai%20GT2)
- [Thế Giới IC](https://www.thegioiic.com/search?q=GT2)

Giá dịch chuyển. Một tin pulley giấu số răng thì chưa phải một tỉ số.

## Bài tập

1. Các khâu 25 mm, 40 mm, 45 mm và 60 mm. $$s + l < p + q$$ có đúng không? Nếu cố định khâu 45 mm và dẫn khâu 25 mm, các bạn chờ chuyển động gì?
2. Các khâu 40 mm, 50 mm, 55 mm và 120 mm. Có maniven quay đủ vòng không?
3. Pulley động cơ 16 răng, pulley bánh 48 răng, hộp giảm tốc đóng dấu 1:30 ngồi trước pulley động cơ. $$i$$ từ trục động cơ tới bánh là bao nhiêu?
4. Đường kính vòng chia của bánh dẫn là 20 mm. Thanh răng đi bao xa trong một vòng, và trong một phần tư vòng?
5. Một cam có đoạn nâng trên $$90^\circ$$ và đoạn dừng trên $$180^\circ$$ kế tiếp. Con đội làm gì trong đoạn dừng, và Capstone A có cần chi tiết này không?

### Gợi ý đáp án

1. $$s + l = 85$$, $$p + q = 85$$. Dấu bằng là trường hợp điểm đổi; một vòng tương đối đủ chỉ là cơ cấu Grashof sát biên, và nó có thể gập phẳng. Coi nó là dễ vỡ. Dẫn khâu ngắn vẫn muốn thành maniven, và các bạn nên kéo dài một khâu bên một chút nếu cần một khâu quay đáng tin. 2. $$s + l = 160$$, $$p + q = 105$$. Không khâu nào quay đủ vòng. 3. Đai $$i = 48/16 = 3$$, nhân hộp số 30, nên $$i = 90$$. 4. $$x = \pi \times 20 \approx 62.8$$ mm mỗi vòng, khoảng 15,7 mm mỗi phần tư vòng. 5. Con đội đứng yên trong khi cam quay qua đoạn dừng ấy. Capstone A không cần cam.

## Đọc thêm

- [Four-bar linkage](https://en.wikipedia.org/wiki/Four-bar_linkage) — maniven-cần lắc, và chuyện gì đổi khi một khâu khác được cố định.
- [Grashof’s law](https://en.wikipedia.org/wiki/Grashof%27s_law) — phép thử $$s + l$$, kể cả trường hợp dấu bằng.
- [Timing belt (đai răng)](https://en.wikipedia.org/wiki/Timing_belt_(camshaft)) — răng ăn khớp và vì sao đai chùng thì nhảy răng. Trang viết về động cơ đốt trong; ý cặp ăn chính là ý trên pulley GT2 của các bạn.
