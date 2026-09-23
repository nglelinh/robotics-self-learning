---
layout: post
title: "Ốc vít, bạc đạn, trục và khớp nối"
chapter: "06"
order: 2
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter06
lesson_type: required
draft: false
---

Thời lượng ước tính: **70–90 phút**, gồm lúc phân loại một bộ ốc nhỏ và chụp ảnh đai ốc nyloc đặt cạnh đai ốc thường.

## Mục tiêu học

Hết bài này, các bạn tách được ốc M2, M3 và M4 bằng cách đo đường kính ren, chọn đai ốc nyloc ở những mối mà đai ốc thường sẽ tự tháo dưới rung, và siết vít cố định trục (set screw) đúng vào mặt vát của trục chữ D. Các bạn quyết định được khi nào bạc đạn bi 608 thuộc về con lăn in 3D, khi nào bạc lót sẵn trong hộp giảm tốc TT phải được để yên, và chọn khớp nối khớp đường kính trục đã mua thật, không khớp đường kính ghi trong trí nhớ.

## Kiến thức cần có

Các bạn dùng được thước kẹp, hoặc khi không có thước thì dùng một đai ốc đã biết cỡ làm dưỡng (thói quen đo của Chương 01). Các bạn biết khung ở Bài 01 có bánh ngồi trên trục động cơ, và những trục ấy về sau phải báo góc quay trung thực cho encoder.

## Vì sao bài này quan trọng với Capstone A và ROS

Odometry của Capstone A tin rằng góc bánh và góc động cơ là cùng một góc, chỉ nhân với tỉ số truyền các bạn sẽ ghi ở Bài 03. Vít cố định trục (set screw) trượt khỏi mặt vát thì bánh kêu tách trong khi encoder vẫn đếm một vòng hoàn hảo của động cơ. Tư thế ROS sau đó đi lang thang trên bản đồ trong lúc robot ngập ngừng trên nền gạch. Ốc vít là lý do lời nói dối ấy bắt đầu, hoặc không bao giờ bắt đầu. Một đai ốc nyloc đứng yên, một khớp nối đúng trục, và một bạc đạn đúng việc, là nửa cơ khí của một topic `odom` đáng tin. Nửa kia là xung encoder. Thiếu nửa cơ khí thì hiệu chỉnh phần mềm chỉ làm đẹp một quỹ đạo không có thật.

## Ốc, đai ốc, và một mặt vát trên trục

Ốc hệ mét được gọi theo đường kính ngoài của ren. M3 nghĩa là khoảng 3 mm đo qua đỉnh ren, và đó là cỡ mặc định trên robot này: giá động cơ, giá cảm biến, và chính tấm khung. Bước ren thô chuẩn của M3 là 0,5 mm, nên một vòng đủ của ốc tiến thêm nửa milimét vào đai ốc. M2 là ốc nhỏ trên một số mạch cảm biến, dễ tòe đầu. M4 khỏe hơn và thường quá lớn so với rãnh động cơ TT. Lỗi mua hàng quen thuộc là một túi ghi “M3” nhưng bên trong là hỗn hợp nhiều cỡ.

Đai ốc thường là lục giác với ren sạch. Rung từ hộp giảm tốc làm nó tự đi ra khỏi ốc sau một buổi chiều chạy xe. Đai ốc nyloc có một vòng nhựa nylon ở một đầu, vòng ấy kẹp ren. Vặn tay đến khi vòng nhựa cắn, rồi siết nốt bằng tô-vít. Độ bám ấy là phương án cho Capstone A. Keo khóa ren xanh (loại trung bình) là phương án dự phòng dạng lỏng cho ren kim loại ăn kim loại mà các bạn có thể không bao giờ tháo. Đó là phương án kém trên nhựa PLA: dung môi có thể làm nứt nhựa. Trên giá in, dùng nyloc, hoặc nóng chảy một đai đồng có ren rồi đặt nyloc lên ren kim loại mà đai đồng tạo ra.

Trục động cơ giảm tốc sở thích thường là trục chữ D: một hình trụ có một mặt vát. Moay-ơ bánh hoặc khớp nối mang một vít cố định trục (set screw), tức một ốc nhỏ cắn trục từ bên hông. Ốc ấy phải rơi đúng mặt vát. Cắn vào phần tròn, nó đẩy một gờ, moay-ơ kêu vo vo dưới mô-men, và encoder, vốn đang nhìn động cơ, vẫn đếm. Odometry khi đó báo chuyển động mà sàn không thấy. Sau khi siết vít, thử vặn bánh trên trục bằng ngón tay. Vít ngồi đúng mặt vát thì giữ. Vít ngồi trên đỉnh tròn thì trượt kèm một tiếng tách.

![Bạc đạn bi: vòng trong, bi, vòng ngoài]({{ site.imgurl }}/wikimedia/Ball_bearing.jpg)

Bạc đạn bi, như trong ảnh, có vòng trong, một vòng bi, và vòng ngoài. Cỡ 608 thông dụng có lỗ 8 mm, đường kính ngoài 22 mm, dày 7 mm, chính là bạc đạn ván trượt. Nó hợp với con lăn in cho đai, ngồi trên vai 8 mm hoặc trên một trục in thực sự là 8 mm. Nó quá cỡ với động cơ TT vàng, vì trục và hộp số của loại ấy không được thiết kế quanh bạc 608. Hộp giảm tốc TT rẻ chạy trên bạc lót, tức ống trượt trơn. Chúng ồn, và chúng là bình thường. Mở hộp giữa chừng Capstone để “nâng cấp” sẽ mất dấu tỉ số in trên vỏ và mất cả một cuối tuần. Để yên cho đến khi robot chạy được.

Trục gặp trục qua một khớp nối khi động cơ và tải không chung một đoạn thép. Khớp cứng đòi hai trục thẳng hàng. Một chút lệch góc trở thành tải tuần hoàn, bạc nóng, và bánh lắc. Khớp hàm, với một đệm đàn hồi hình sao giữa hai moay-ơ, tha thứ một độ lệch nhỏ và là lựa chọn dịu hơn trên tấm của sinh viên. Đường kính khắc trên khớp phải khớp trục: 3 mm, 4 mm và 6 mm đều phổ biến trên động cơ giảm tốc kim loại, và chúng không thay thế cho nhau. Khớp 6 mm trên trục 4 mm kẹp thành hình ô-van rồi vẫn trượt. Đo trục bằng thước kẹp trước khi đặt hàng. Bánh TT thường có sẵn lỗ chữ D đúng động cơ ấy, nên trên bánh chủ động của Capstone A các bạn thường không cần khớp nối.

## Ví dụ tính tay

Ốc M3 có bước 0,5 mm. Bốn vòng đủ, sau khi đai ốc đã vào ren, ăn

$$
4 \times 0.5 = 2.0\ \text{mm}
$$

ren. Đó là chênh lệch giữa một giá động cơ đã khít và một con ốc đã chạm đáy rồi bắt đầu nứt lỗ mica. Dừng khi các chi tiết đã ngồi, rồi thêm khoảng một phần tư vòng. Phía trục, giả sử vít cố định trục trượt khỏi mặt vát và bánh trượt đúng một vòng trong lúc encoder đếm vòng ấy như chuyển động thật. Với bán kính lăn $$r = 31.2$$ mm từ Bài 01, odometry bịa ra một quãng đường

$$
s = 2\pi r = 2\pi \times 31.2 \approx 196\ \text{mm}
$$

mà robot không hề đi. Một mặt vát bị trượt, một đoạn ma khoảng 20 cm, mỗi lần mô-men đảo chiều và moay-ơ kêu tách.

## Lab: phân loại ốc và tìm mặt vát

### An toàn

Nguồn tắt. Vít cố định trục nhỏ và hay bắn ra khỏi lục giác; hướng moay-ơ ra xa mắt. Keo khóa ren là tùy chọn và phải đậy nắp; không hít, và không nhỏ lên nhựa “cho chắc”.

### BOM

| Hạng mục | Vai trò |
|------|------|
| Ốc và đai ốc lẫn M2/M3/M4, kể cả bộ rẻ | Đống cần phân loại |
| Một đai ốc nyloc và một đai ốc thường | Mẫu so sánh |
| Thước kẹp, hoặc một đai ốc mỗi cỡ mà các bạn tin | Dưỡng |
| Một moay-ơ trục chữ D, hoặc ảnh moay-ơ các bạn đang có | Mặt vát |
| Điện thoại | Ảnh cho `lab-notes.md` |

### Các bước

1. Đo đường kính đỉnh ren của từng ốc, hoặc thử vào một đai ốc đã biết. M2 không vào được đai ốc M3. M4 không vào được đai ốc M3. M3 chạy trơn.
2. Chia đống thành ba cốc. Ghi số ốc M3 các bạn thực sự có; Capstone A ăn loại này.
3. Chụp một đai ốc nyloc cạnh một đai ốc thường. Trên ảnh, đánh dấu vòng nylon.
4. Nếu có moay-ơ bánh, nới vít cố định trục, đặt trục chữ D sao cho mặt vát hướng vào ốc, rồi siết. Vặn bánh bằng tay. Ghi xem nó có giữ không.
5. Nếu có bạc 608, đo 8 × 22 × 7 mm và viết một câu về chỗ nó được sống (con lăn in) và chỗ nó không được sống (bên trong hộp giảm tốc TT).

### Kết quả mong đợi

Ba nhóm đã dán nhãn, một ảnh nyloc đối chiếu đai ốc thường, và một câu trong `lab-notes.md` nêu đường kính trục các bạn sẽ đi mua. Vít cố định trục đã ngồi đúng thì giữ bánh trước mô-men ngón tay.

### Lỗi thường gặp

| Các bạn thấy | Thường nghĩa là |
|--------------|------------------------|
| Ốc gần như vào rồi kẹt | Sai cỡ, hoặc ren bắt chéo; tháo ra |
| Đai ốc quay mãi dưới rung | Đai ốc thường, và mối ấy chưa có nyloc |
| Bánh kêu vo vo, encoder vẫn đếm | Vít cố định trục đang nằm trên phần tròn của trục chữ D |
| Khớp nối kẹp rất chặt mà vẫn trượt | Lỗ lớn hơn trục một cỡ |
| Gờ nhựa nứt vào hôm sau khi bôi keo khóa ren | Keo ấy là phương án cho PLA; chuyển sang nyloc hoặc đai đồng |

## Mua ở Việt Nam / Where to buy in Vietnam

Một bộ ốc M3 cộng một túi nhỏ đai ốc nyloc M3 là đủ cho Capstone A. Chỉ mua bạc 608 khi các bạn đang in con lăn. Chỉ mua khớp hàm khi hai trục phải gặp nhau, và chỉ sau khi đã có số đọc thước kẹp.

| Mua gì | Từ khóa | Khoảng giá (VND) | Ghi chú |
|------|----------|------------------|-------|
| Bộ ốc M3 | `ốc M3` | 25.000–70.000 | Nhiều chiều dài; kiểm tra có lục giác kèm không |
| Đai ốc nyloc | `đai ốc nyloc M3` | 15.000–40.000 một túi | Vòng nylon nhìn thấy ở một đầu |
| Bạc đạn 608 | `bạc đạn 608` | 5.000–20.000 mỗi cái | 8×22×7 mm, cho con lăn |
| Khớp nối hàm | `khớp nối trục 4mm` | 15.000–45.000 | Khớp trục đã đo: 3 mm, 4 mm hoặc 6 mm |

Tìm và so hai người bán. Giá dịch chuyển.

- [Hshop: ốc M3](https://hshop.vn/search?q=%E1%BB%91c+M3)
- [Shopee: đai ốc nyloc M3](https://shopee.vn/search?keyword=%C4%91ai%20%E1%BB%91c%20nyloc%20M3)
- [Lazada: bạc đạn 608](https://www.lazada.vn/catalog/?q=b%E1%BA%A1c%20%C4%91%E1%BA%A1n%20608)
- [Thế Giới IC: ốc vít](https://www.thegioiic.com/search?q=%E1%BB%91c%20v%C3%ADt)

## Bài tập

1. Một con ốc đo 2,9 mm qua đỉnh ren và tiến 0,5 mm mỗi vòng. Tên gọi của nó là gì, và sáu vòng nó tiến bao xa?
2. Các bạn đang dùng đai ốc thường trên giá động cơ, và sẽ chạy giá ấy mỗi buổi lab. Thay bằng gì, và vì sao keo khóa ren xanh không phải phương án đầu nếu giá ấy là nhựa PLA?
3. Moay-ơ bánh kêu tách khi vặn, và số đếm encoder vẫn tăng khi về sau cấp điện cho động cơ trong lúc bánh được nhấc lên. Vít cố định trục đang ngồi ở đâu?
4. Thước kẹp đọc 4,0 mm trên trục động cơ giảm tốc kim loại. Đặt lỗ khớp nối cỡ nào, và lỗ 6 mm sẽ xảy ra chuyện gì?
5. Một người bạn muốn ép bạc đạn 608 vào hộp giảm tốc TT vàng “cho lăn êm hơn”. Trong Capstone A, các bạn bảo họ làm gì với bạc lót sẵn có?

### Gợi ý đáp án

1. M3, vì đỉnh ren khoảng 3 mm và bước ren là chuẩn 0,5 mm. Sáu vòng tiến $$6 \times 0.5 = 3.0$$ mm. 2. Một đai ốc nyloc. Keo khóa ren xanh có thể làm nứt PLA; đai đồng cộng nyloc giữ hóa chất trên kim loại. 3. Trên phần tròn của trục chữ D, không trên mặt vát. Nới ra, xoay mặt vát vào dưới ốc, siết lại, rồi thử vặn. 4. Lỗ 4 mm. Lỗ 6 mm kẹp thành ô-van và trượt dưới mô-men. 5. Để nguyên bạc lót. Bạc 608 là 8×22×7 mm và thuộc về con lăn in, không thuộc về bên trong hộp số ấy.

## Đọc thêm

- [Danh mục McMaster-Carr](https://www.mcmaster.com/) — tra ốc, nyloc, vòng chặn trục và khớp hàm theo tên để học kích thước. Dùng như từ điển hình. Đặt hàng từ nước ngoài nằm ngoài môn này.
- [Đai ren nhiệt trên RepRap](https://reprap.org/wiki/Threaded_insert) — đai đồng nóng chảy cho nhựa in, cách bền để đặt ren M3 vào PLA.
- [Bạc đạn bi (tổng quan)](https://en.wikipedia.org/wiki/Ball_bearing) — vòng bi và cỡ 608 trong ngữ cảnh.
