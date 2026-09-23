---
layout: post
title: "Lab: đo tỉ số truyền và checklist lắp"
chapter: "06"
order: 8
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter06
lesson_type: required
draft: false
---

Thời lượng ước tính: **80–110 phút**. Bài này là phần làm tay. Nguồn tắt cho mọi mục kiểm cơ khí.

## Mục tiêu học

Hết bài này, các bạn có một tỉ số truyền vừa dự đoán vừa kiểm, một ước lượng độ rơ tại bánh theo độ, và một checklist lắp viết ra được để chạy trước bất kỳ điện áp nào ở Chương 07. Các bạn phân biệt được bánh trung gian đơn với một lần đổi tỉ số, và nhân được dấu đóng của hộp giảm tốc với một đai ngoài khi cả hai đều tồn tại.

## Kiến thức cần có

Bài 01 đến Bài 07. Các bạn cần $$b$$, $$r$$, thói quen M3, định nghĩa tỉ số $$i = N_{\text{out}}/N_{\text{in}} = \omega_{\text{in}}/\omega_{\text{out}}$$, và phép giật giảm lực kéo dây. Một kim chỉ bằng bìa và một thước đo góc, hoặc một thước đo góc in trên giấy, là đủ dụng cụ.

## Vì sao bài này quan trọng với Capstone A và ROS

Chương 07 là lần đầu khung này được phép nhìn thấy điện áp. Checklist bên dưới là cổng. Một bánh cà, một cục pin trượt, hoặc một vít cố định trục nằm trên phần tròn sẽ đốt buổi lab ấy vào một dạng hỏng mà Bài 07 đã gọi tên. Tỉ số các bạn đo là tỉ số `diff_drive_controller` sẽ đổi thành mét. Một kết quả nằm trong khoảng 10 phần trăm so với nhãn là điều răng đúc chịu được. Nếu kit vẫn đang trên đường, dự đoán trên bản vẽ là sản phẩm nộp và các bạn dán nhãn đó là bản vẽ. Đừng bịa một góc đo mà các bạn không đo.

## Các bạn đang kiểm gì

Đếm răng nếu nhìn thấy, hoặc đọc dấu đóng trên hộp giảm tốc. Dấu đóng là dự đoán. Phép kiểm là động học: một kim trên đầu vào, một kim trên đầu ra, một chuyển động đầu vào đã biết, một góc đầu ra đã đo. Với tỉ số $$i$$, ba vòng đầu vào phải cho

$$
\theta_{\text{out}} = \frac{3}{i} \times 360^\circ.
$$

Sau đó giữ đầu vào đứng yên và lắc bánh. Góc bánh dịch trước khi kim đầu vào buộc phải động chính là độ rơ các bạn sẽ nêu. Ước bằng mắt là đủ. Vài độ tại bánh là bánh đúc bình thường. Hàng chục độ nghĩa là vít cố định trục lỏng hoặc đai nhảy răng, đó là một lỗi khác.

Một bánh trung gian đơn đảo chiều và không đổi $$i$$. Đếm nó như một cặp ăn cho dấu, không đếm như một thừa số, trừ khi nó là bánh trung gian kép với hai số răng khác nhau khóa cùng nhau. Nếu một đai ngồi ngoài hộp giảm tốc, tỉ số bánh là tích. Sinh viên mất một thừa số hai ở đây thường hơn là đếm sai một bánh dẫn.

Rồi chạy danh sách lắp với pin nằm trên bàn, không nằm trên giắc. Ốc chặt. Vít cố định trục trên mặt vát. Bánh không chạm tấm. Caster quay và có đuôi. Dây có vòng dự phòng và mối hàn không bị bẻ. Pin không trượt trong túi tương lai của nó. Cả hai động cơ xoay bằng tay với lực cản tương đương. Động cơ nào cảm thấy sạn hoặc cứng hơn hẳn người anh em thì được ghi chú trước Chương 07, không được một PWM cao hơn.

![Gọi tên đầu vào trước khi chia: hình là dự đoán, hai kim là phép kiểm]({{ site.imgurl }}/generated/gear_train_ratio.png)

## Ví dụ tính tay

Một động cơ TT đóng dấu 1:48. Ba vòng đầu vào phải cho

$$
\theta_{\text{out}} = \frac{3}{48} \times 360^\circ = 22.5^\circ.
$$

Các bạn đo $$24^\circ$$ tại kim bánh. Sai số tương đối là

$$
\frac{24 - 22.5}{22.5} \approx 0.067,
$$

khoảng 7 phần trăm, nằm trong dải 10 phần trăm của răng đúc và một kim làm tay. Các bạn ghi $$i = 48$$ và “đã kiểm, 24° so với 22,5°”. Nếu kim rơi gần $$45^\circ$$, sai số là một thừa số hai: một đai 2:1 bị bỏ quên, hoặc một dấu đóng bị chia đôi. Nếu rơi gần $$67.5^\circ$$, các bạn đã dùng $$i = 16$$ hoặc đã xoay nhầm trục. Độ rơ đo bằng cách lắc bánh, chẳng hạn $$5^\circ$$, được ghi cạnh tỉ số và không được “sửa” bằng cách siết cặp ăn đến lúc kẹt.

Chiều quay: một cặp ăn ngoài, hoặc một số lẻ các cặp ấy, đảo bánh so với động cơ. Dấu firmware ở Bài 05 phải khớp quan sát này, vẫn khi nguồn tắt, bằng cách xoay trục theo chiều động cơ sẽ quay.

## Lab: hai kim, rồi danh sách

### An toàn

Nguồn vẫn tắt. Pin ngắt và đặt ở chỗ một cú giật không thể đẩy nó vào cực. Răng bánh kẹp; xoay trục từ kim, không xoay từ trong cặp ăn. Nếu một trục không chịu động, dừng và tìm chỗ cà. Đừng thêm điện áp để “phá kẹt”.

### BOM

| Hạng mục | Vai trò |
|------|------|
| Động cơ giảm tốc hoặc một bản vẽ bánh răng đúng tỉ lệ | Tỉ số |
| Hai kim: cờ băng dính hoặc mũi tên bìa | Đầu vào và đầu ra |
| Thước đo góc, hoặc một thước in | Góc đầu ra và độ rơ |
| Lục giác cho vít cố định trục | Mặt vát |
| Dây rút | Vòng dự phòng, nếu dây đã có trên động cơ |
| `lab-notes.md` | Dự đoán, phép đo, checklist |

### Các bước

1. Viết dự đoán. Số răng nếu nhìn thấy, nếu không thì dấu đóng. Tính $$\theta_{\text{out}}$$ cho đúng ba vòng đầu vào.
2. Dán một kim vào đầu vào và một kim vào đầu ra. Đánh dấu mốc không trên bàn.
3. Xoay đầu vào đúng ba vòng. Đo góc đầu ra. Đối chiếu với dự đoán và ghi phần trăm chênh lệch.
4. Giữ đầu vào. Lắc đầu ra. Ước độ rơ theo độ tại bánh.
5. Đi checklist và tick từng dòng trong sổ: ốc chặt; vít cố định trục trên mặt vát; bánh không cà; caster quay và có đuôi; vòng dây dự phòng, mối hàn yên; pin không trượt; cả hai động cơ xoay bằng tay với lực cản tương đương.
6. Nếu chỉ có bản vẽ, làm bước 1 và các phác họa, viết “bản vẽ, kết quả trên giấy là sản phẩm nộp”, và vẫn soạn checklist như quy trình các bạn sẽ chạy khi thùng hàng về.

### Kết quả mong đợi

Một tỉ số nằm trong khoảng 10 phần trăm so với nhãn khi có phần cứng, hoặc một dự đoán trên giấy được dán nhãn rõ khi chưa có. Độ rơ nêu theo độ. Mỗi dòng checklist đánh dấu đạt, không đạt, hoặc “chưa có trên bàn”. Dòng không đạt nêu cách sửa, không nêu kế hoạch phát hiện nó trong buổi lab có điện.

### Lỗi thường gặp

| Các bạn thấy | Thường nghĩa là |
|--------------|------------------------|
| Góc là nghịch đảo của dự đoán | Tên đầu vào và đầu ra bị đảo |
| Góc bằng một nửa hoặc gấp đôi | Hộp giảm tốc và đai ngoài chưa được nhân, hoặc một trong hai bị áp hai lần |
| Chiều sai, tỉ số đúng | Một bánh trung gian bị tính như đổi tỉ số, hoặc một cặp ăn bị bỏ khỏi phép đếm dấu |
| Đầu ra oặt hàng chục độ | Vít cố định trục, moay-ơ mòn răng, hoặc đai nhảy răng |
| Một động cơ cứng hơn nhiều khi xoay tay | Chỗ cà, hoặc hộp số hỏng; đừng cấp điện để xác nhận |

## Mua ở Việt Nam / Where to buy in Vietnam

Chỉ mua thứ checklist đã chứng minh là thiếu. Một ứng dụng thước đo góc là đủ nếu các bạn ngắm được dọc kim. Một động cơ TT có dấu đóng nhìn thấy được là chi tiết biến bước 1 thành một lần đọc, không phải một lần đoán.

| Mua gì | Từ khóa | Khoảng giá (VND) | Ghi chú |
|------|----------|------------------|-------|
| Động cơ giảm tốc TT | `động cơ giảm tốc TT encoder` | 45.000–120.000 mỗi cái | Dấu đóng là dự đoán |
| Bộ ốc M3, nếu lần phân loại ở Bài 02 bị thiếu | `ốc M3` | 25.000–70.000 | Dòng ốc trên checklist |
| Bánh caster, nếu mũi vẫn cày | `bánh caster robot` | 12.000–40.000 | Phải có đuôi |

Các trang tìm:

- [Hshop](https://hshop.vn/search?q=%C4%91%E1%BB%99ng+c%C6%A1+gi%E1%BA%A3m+t%E1%BB%91c+TT)
- [Shopee](https://shopee.vn/search?keyword=%C4%91%E1%BB%99ng%20c%C6%A1%20gi%E1%BA%A3m%20t%E1%BB%91c%20TT%20encoder)
- [Lazada](https://www.lazada.vn/catalog/?q=%E1%BB%91c%20M3)
- [Thế Giới IC](https://www.thegioiic.com/search?q=%E1%BB%91c%20M3)

Giá dịch chuyển. Đừng mua hộp giảm tốc thứ hai để tránh đo hộp thứ nhất.

## Bài tập

1. Dấu đóng 1:90. Dự đoán góc đầu ra cho ba vòng đầu vào.
2. Các bạn đo $$12^\circ$$ sau ba vòng ấy trên một động cơ 1:48. Số đó có nằm trong 10 phần trăm của 22,5° không? Kiểm gì tiếp theo?
3. Một bánh dẫn 20 răng kéo một bánh trung gian 20 răng, bánh ấy kéo một bánh 40 răng. Cho $$i$$ và chiều đầu ra so với bánh dẫn.
4. Hộp giảm tốc 1:48 và một cấp GT2 với 20 răng trên pulley động cơ, 40 răng trên pulley bánh. Bánh xe thấy $$i$$ bao nhiêu? $$\theta_{\text{out}}$$ cho ba vòng động cơ là bao nhiêu?
5. Liệt kê bảy dòng checklist và đánh sao hai dòng mà nếu bỏ qua thì trực tiếp bịa odometry ma nhất.

### Gợi ý đáp án

1. $$\theta_{\text{out}} = 3/90 \times 360^\circ = 12^\circ$$. 2. $$|12 - 22.5|/22.5 \approx 47$$ phần trăm, nằm xa ngoài dải. Kiểm rằng các bạn đã xoay trục động cơ ba vòng, rằng các bạn đọc 1:48 chứ không phải một dấu khác, và rằng một đai không bị bỏ quên hoặc bị thêm vào. 3. $$i = 40/20 = 2$$. Bánh trung gian đơn không đổi tỉ số. Hai cặp ăn ngoài trả lại chiều, nên đầu ra cùng chiều bánh dẫn. 4. $$i = 48 \times (40/20) = 96$$. Ba vòng động cơ cho $$3/96 \times 360^\circ = 11.25^\circ$$ tại bánh. 5. Ốc chặt; vít cố định trục trên mặt vát; bánh không cà; caster quay và có đuôi; vòng dây dự phòng với mối hàn yên; pin không trượt; lực cản tay tương đương. Đánh sao vít cố định trục và chỗ cà: cả hai để encoder vui trong khi sàn không đồng ý.

## Đọc thêm

- [Gear ratio](https://en.wikipedia.org/wiki/Gear_ratio) — chuỗi bánh kép, chính là trường hợp hộp số nhân đai.
- [Công nghệ bánh răng SDP-SI](https://www.sdp-si.com/resources/elements-of-metric-gear-technology/index.php) — độ rơ như một khe được thiết kế, viết bằng ngôn ngữ danh mục.
- [diff_drive_controller](https://github.com/ros-controls/ros2_controllers/tree/master/diff_drive_controller) — nơi $$i$$, $$b$$ và $$r$$ các bạn đo sẽ được gõ vào.
