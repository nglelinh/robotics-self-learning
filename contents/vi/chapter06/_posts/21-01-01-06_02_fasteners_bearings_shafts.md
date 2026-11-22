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

Thời lượng ước tính: **70–90 phút**, bao gồm thời gian phân loại một bộ ốc nhỏ và chụp ảnh so sánh đai ốc nyloc với đai ốc thường.

## Mục tiêu học

Sau bài này, các bạn phân biệt được ốc M2, M3 và M4 thông qua việc đo đường kính ren, biết chọn đai ốc nyloc cho các mối ghép dễ tự tháo khi rung, và siết vít cố định trục (set screw) đúng vào mặt vát của trục chữ D. Các bạn cũng xác định được khi nào nên dùng bạc đạn bi 608 (cho con lăn in 3D), khi nào nên giữ nguyên bạc lót sẵn có trong hộp giảm tốc TT, và biết chọn khớp nối theo đúng đường kính trục đo thực tế thay vì dựa vào trí nhớ.

## Kiến thức cần có

Các bạn sử dụng được thước kẹp, hoặc dùng một đai ốc đã biết cỡ làm dưỡng kiểm tra khi không có thước (theo thói quen đo lường ở Chương 01). Các bạn đã biết ở Bài 01 rằng bánh xe gắn trực tiếp lên trục động cơ và các trục này cần truyền góc quay trung thực tới encoder.

## Vì sao bài này quan trọng với Capstone A và ROS

Hệ thống odometry của Capstone A hoạt động dựa trên giả định rằng góc quay của bánh xe và góc quay của trục động cơ liên hệ chặt chẽ qua tỉ số truyền (sẽ ghi ở Bài 03). Nếu vít cố định trục (set screw) trượt khỏi mặt vát, bánh xe sẽ trượt kèm tiếng tách trong khi encoder vẫn đếm đủ vòng quay của động cơ. Khi đó, tư thế robot trong ROS bị trôi trên bản đồ dù xe thực tế đang khựng lại trên sàn. Các chi tiết ghép nối cơ khí chính là yếu tố quyết định sai số này có xảy ra hay không: một đai ốc nyloc không tự lỏng, một khớp nối đúng cỡ trục và một bạc đạn dùng đúng chỗ tạo nên nửa cơ khí của topic `odom` đáng tin cậy. Nửa còn lại là tín hiệu xung encoder; nếu thiếu phần cơ khí vững chắc, mọi tinh chỉnh phần mềm chỉ tạo ra một quỹ đạo sai lệch.

## Ốc, đai ốc, và một mặt vát trên trục

Ốc hệ mét được đặt tên theo đường kính ngoài của phần ren. Ốc M3 có đường kính đỉnh ren khoảng 3 mm và là cỡ tiêu chuẩn cho robot trong môn học này, dùng cho giá động cơ, giá cảm biến và tấm khung. Bước ren thô chuẩn của M3 là 0,5 mm, tức mỗi vòng vặn đủ sẽ đưa ốc tiến thêm 0,5 mm vào đai ốc. Ốc M2 có kích thước nhỏ, thường gặp trên một số mạch cảm biến và rất dễ tòe đầu; còn M4 cứng cáp hơn nhưng thường quá lớn so với rãnh lắp động cơ TT. Một lỗi mua hàng hay gặp là túi linh kiện ghi nhãn “M3” nhưng bên trong lại lẫn nhiều cỡ khác nhau.

Đai ốc lục giác thông thường có ren trơn, nên rung động từ hộp giảm tốc dễ làm nó tự xoay và lỏng ra chỉ sau một buổi chạy thử. Đai ốc nyloc (đai ốc khóa nylon) có thêm vòng nhựa nylon ở một đầu để kẹp chặt ren: bạn vặn tay tới khi vòng nhựa bắt đầu bám, sau đó siết chặt bằng dụng cụ. Đây là lựa chọn tiêu chuẩn cho Capstone A. Keo khóa ren màu xanh (loại lực giữ trung bình) là phương án dự phòng dạng lỏng cho mối ghép kim loại–kim loại ít khi tháo lắp, nhưng không phù hợp trên nhựa PLA vì dung môi có thể làm giòn và nứt nhựa. Với các chi tiết in 3D, hãy dùng đai ốc nyloc hoặc ép nhiệt đai đồng cấy ren (threaded insert) rồi dùng nyloc trên phần ren kim loại đó.

Trục của các động cơ giảm tốc phổ thông thường có dạng chữ D — hình trụ được vát phẳng một mặt. Moay-ơ bánh xe hoặc khớp nối có một vít cố định trục (set screw) siết từ bên hông vào trục. Vít này bắt buộc phải tỳ vuông góc lên mặt vát. Nếu tỳ lên phần mặt tròn, vít chỉ tạo một vết cấn nhỏ; khi có mô-men tải, moay-ơ sẽ trượt trên trục trong khi encoder gắn phía động cơ vẫn đếm xung bình thường, làm odometry báo quãng đường không hề xảy ra trên sàn. Sau khi siết vít, hãy dùng ngón tay vặn thử bánh xe: nếu vít nằm đúng mặt vát thì bánh giữ chắc, còn nếu nằm trên mặt tròn thì bánh sẽ trượt kèm tiếng tách.

![Bạc đạn bi: vòng trong, bi, vòng ngoài]({{ site.imgurl }}/wikimedia/Ball_bearing.jpg)

Bạc đạn bi (như trong ảnh) gồm vòng trong, dãy viên bi và vòng ngoài. Cỡ 608 phổ biến có đường kính lỗ 8 mm, đường kính ngoài 22 mm và bề dày 7 mm — giống bạc đạn dùng trên ván trượt. Loại này phù hợp cho con lăn dẫn hướng đai in 3D lắp trên vai trục 8 mm, nhưng quá cỡ so với động cơ TT vỏ vàng, vốn không được thiết kế cho bạc 608. Hộp giảm tốc TT giá rẻ sử dụng bạc lót (ống trượt trơn); chúng chạy hơi ồn nhưng hoàn toàn bình thường. Việc tự ý tháo hộp số giữa chừng Capstone để “nâng cấp” bạc đạn dễ làm mất dấu tỉ số truyền in trên vỏ và tốn cả cuối tuần lắp lại. Hãy giữ nguyên hộp số cho tới khi robot đã vận hành ổn định.

Khi động cơ và trục tải không liền khối, ta nối chúng bằng khớp nối. Khớp nối cứng yêu cầu hai trục phải đồng tâm tuyệt đối; chỉ một độ lệch góc nhỏ cũng tạo ra tải tuần hoàn làm nóng bạc đạn và khiến bánh xe đảo. Khớp nối hàm (jaw coupling) có miếng đệm đàn hồi hình sao ở giữa giúp bù sai lệch nhỏ và phù hợp hơn với khung xe do sinh viên gia công. Đường kính lỗ khắc trên khớp phải khớp chính xác với trục: các cỡ 3 mm, 4 mm và 6 mm đều phổ biến trên động cơ giảm tốc kim loại và không thể thay thế lẫn nhau. Lắp khớp 6 mm lên trục 4 mm sẽ làm lỗ kẹp bị méo thành hình ô-van và vẫn trượt khi chịu tải. Hãy đo trục bằng thước kẹp trước khi đặt mua. Riêng bánh xe TT thường đã đúc sẵn lỗ chữ D khớp trục động cơ nên bánh chủ động của Capstone A thường không cần khớp nối riêng.

## Ví dụ tính tay

Ốc M3 có bước ren 0,5 mm. Sau khi đai ốc đã vào ren, bốn vòng vặn đủ sẽ ăn sâu một đoạn:

$$
4 \times 0.5 = 2.0\ \text{mm}.
$$

Khoảng cách 2 mm này đủ tạo ra sự khác biệt giữa một giá động cơ vừa khít và một con ốc bị siết kịch đáy làm nứt lỗ mica. Quy tắc thực hành là dừng tay ngay khi các chi tiết đã áp sát, rồi siết thêm khoảng một phần tư vòng.

Xét ở phía trục bánh xe: giả sử vít cố định trục bị trượt khỏi mặt vát khiến bánh xe đứng yên mất đúng một vòng trong khi encoder vẫn đếm đủ vòng quay đó. Với bán kính lăn $$r = 31.2$$ mm từ Bài 01, odometry sẽ ghi nhận một quãng đường ảo:

$$
s = 2\pi r = 2\pi \times 31.2 \approx 196\ \text{mm}.
$$

Chỉ một lần trượt trục đã tạo ra sai số gần 20 cm, và sai số này sẽ lặp lại mỗi khi mô-men đảo chiều làm moay-ơ trượt.

## Lab: phân loại ốc và tìm mặt vát

### An toàn

Đảm bảo đã tắt nguồn. Vít cố định trục rất nhỏ và dễ văng khỏi đầu khóa lục giác, vì vậy luôn hướng moay-ơ ra xa mắt khi thao tác. Keo khóa ren là vật tư tùy chọn; luôn đậy nắp khi không dùng, tránh hít hơi keo và không nhỏ lên chi tiết nhựa.

### BOM

| Hạng mục | Vai trò |
|------|------|
| Ốc và đai ốc lẫn M2/M3/M4, kể cả bộ rẻ | Đống cần phân loại |
| Một đai ốc nyloc và một đai ốc thường | Mẫu so sánh |
| Thước kẹp, hoặc một đai ốc mỗi cỡ mà các bạn tin | Dưỡng |
| Một moay-ơ trục chữ D, hoặc ảnh moay-ơ các bạn đang có | Mặt vát |
| Điện thoại | Ảnh cho `lab-notes.md` |

### Các bước

1. Đo đường kính đỉnh ren của từng con ốc bằng thước kẹp, hoặc thử vặn vào đai ốc mẫu đã biết cỡ. Ốc M2 sẽ lỏng trong đai ốc M3, ốc M4 không vặn vào được, còn ốc M3 sẽ ăn ren trơn tru.
2. Phân loại toàn bộ vào ba cốc riêng (M2, M3, M4) và ghi lại số lượng ốc M3 hiện có — đây là cỡ chính cho Capstone A.
3. Chụp ảnh một đai ốc nyloc đặt cạnh một đai ốc thường, sau đó chú thích rõ phần vòng nhựa nylon trên ảnh.
4. Nếu có moay-ơ bánh xe, nới vít cố định trục, xoay mặt vát của trục chữ D hướng thẳng vào đầu vít rồi siết chặt. Dùng tay vặn thử bánh xe và ghi lại xem mối ghép có giữ chắc không.
5. Nếu có bạc đạn 608, đo kiểm kích thước 8 × 22 × 7 mm và ghi ngắn gọn một câu phân biệt nơi nên dùng (con lăn in 3D) với nơi không nên dùng (bên trong hộp giảm tốc TT).

### Kết quả mong đợi

Ba nhóm ốc đã được phân loại và dán nhãn rõ ràng, một ảnh so sánh đai ốc nyloc với đai ốc thường, và một ghi chú trong `lab-notes.md` nêu chính xác đường kính trục cần mua linh kiện. Vít cố định trục sau khi lắp đúng mặt vát phải giữ chặt bánh xe khi vặn thử bằng tay.

### Lỗi thường gặp

| Các bạn thấy | Thường nghĩa là |
|--------------|------------------------|
| Ốc gần như vào rồi kẹt | Sai cỡ, hoặc ren bắt chéo; tháo ra |
| Đai ốc quay mãi dưới rung | Đai ốc thường, và mối ấy chưa có nyloc |
| Bánh kêu vo vo, encoder vẫn đếm | Vít cố định trục đang nằm trên phần tròn của trục chữ D |
| Khớp nối kẹp rất chặt mà vẫn trượt | Lỗ lớn hơn trục một cỡ |
| Gờ nhựa nứt vào hôm sau khi bôi keo khóa ren | Keo khóa ren không phù hợp với nhựa PLA; chuyển sang nyloc hoặc đai đồng cấy ren |

## Mua ở Việt Nam / Where to buy in Vietnam

Một bộ ốc M3 kèm một túi nhỏ đai ốc nyloc M3 là đủ dùng cho Capstone A. Chỉ mua bạc đạn 608 khi bạn có kế hoạch in con lăn, và chỉ mua khớp nối hàm khi cần nối hai trục sau khi đã đo chính xác đường kính bằng thước kẹp.

| Mua gì | Từ khóa | Khoảng giá (VND) | Ghi chú |
|------|----------|------------------|-------|
| Bộ ốc M3 | `ốc M3` | 25.000–70.000 | Nhiều chiều dài; kiểm tra có lục giác kèm không |
| Đai ốc nyloc | `đai ốc nyloc M3` | 15.000–40.000 một túi | Vòng nylon nhìn thấy ở một đầu |
| Bạc đạn 608 | `bạc đạn 608` | 5.000–20.000 mỗi cái | 8×22×7 mm, cho con lăn |
| Khớp nối hàm | `khớp nối trục 4mm` | 15.000–45.000 | Khớp trục đã đo: 3 mm, 4 mm hoặc 6 mm |

Nên tìm và so sánh ít nhất hai nhà bán vì giá linh kiện có thể thay đổi:

- [Hshop: ốc M3](https://hshop.vn/search?q=%E1%BB%91c+M3)
- [Shopee: đai ốc nyloc M3](https://shopee.vn/search?keyword=%C4%91ai%20%E1%BB%91c%20nyloc%20M3)
- [Lazada: bạc đạn 608](https://www.lazada.vn/catalog/?q=b%E1%BA%A1c%20%C4%91%E1%BA%A1n%20608)
- [Thế Giới IC: ốc vít](https://www.thegioiic.com/search?q=%E1%BB%91c%20v%C3%ADt)

## Video tham khảo

- **Xem trước:** [How to Measure Screws & Bolts - US & Metric Sizing | Fasteners 101](https://www.youtube.com/watch?v=78R1QXL9ijM) — Albany County Fasteners, tiếng Anh. Hướng dẫn đo đường kính ren và chiều dài ốc, đồng thời phân biệt hệ inch và hệ mét để không lắp nhầm vào cùng một lỗ ren.
- [What is Bearing? Types of Bearings and How they Work?](https://www.youtube.com/watch?v=8q25EUszBSI) — The Engineers Post, tiếng Anh. Giải thích nguyên lý hoạt động và các loại bạc đạn giúp giữ trục quay ổn định trước khi lắp khớp nối.
- [How to Identify Thread Pitch and Size | Tech Tips | Swagelok (2020)](https://www.youtube.com/watch?v=Gdvtw0pTAOs) — Swagelok, tiếng Anh. Cách nhận diện bước ren khi hai con ốc có cùng đường kính nhưng không vặn vừa cùng một đai ốc.

## Bài tập

1. Một con ốc đo được 2,9 mm qua đỉnh ren và tiến thêm 0,5 mm sau mỗi vòng vặn. Đó là cỡ ốc nào và sau sáu vòng nó tiến sâu thêm bao nhiêu milimét?
2. Bạn đang dùng đai ốc thường cho giá động cơ chạy mỗi buổi lab. Nên thay bằng loại nào, và vì sao keo khóa ren xanh không phải lựa chọn đầu tiên nếu giá động cơ in bằng nhựa PLA?
3. Moay-ơ bánh xe phát ra tiếng tách khi vặn bằng tay, và khi cấp điện (nhấc bánh khỏi sàn), số xung encoder vẫn tăng dù bánh trượt. Vít cố định trục đang tỳ vào vị trí nào?
4. Thước kẹp đo được 4,0 mm trên trục động cơ giảm tốc kim loại. Bạn cần đặt khớp nối lỗ cỡ bao nhiêu, và điều gì xảy ra nếu dùng lỗ 6 mm?
5. Một người bạn định ép bạc đạn 608 vào hộp giảm tốc TT vỏ vàng để “quay êm hơn”. Trong phạm vi Capstone A, bạn nên khuyên họ xử lý bạc lót sẵn có thế nào?

### Gợi ý đáp án

1. Ốc M3, vì đường kính đỉnh ren xấp xỉ 3 mm và bước ren chuẩn là 0,5 mm. Sau sáu vòng, ốc tiến thêm $$6 \times 0.5 = 3.0$$ mm.
2. Thay bằng đai ốc nyloc. Keo khóa ren xanh có thể làm nứt nhựa PLA; nếu muốn dùng khóa ren chắc trên nhựa in, hãy ép nhiệt đai đồng cấy ren rồi dùng nyloc trên phần ren kim loại.
3. Vít cố định trục đang tỳ lên phần tròn của trục chữ D thay vì mặt vát. Cần nới vít, xoay mặt vát về đúng vị trí dưới đầu vít, siết lại rồi vặn thử bằng tay.
4. Đặt khớp nối lỗ 4 mm. Nếu dùng lỗ 6 mm, khớp sẽ bị kẹp méo thành hình ô-van và trượt khi chịu mô-men.
5. Nên giữ nguyên bạc lót sẵn có. Bạc đạn 608 có kích thước 8×22×7 mm, chỉ phù hợp cho con lăn in 3D chứ không lắp vừa vào bên trong hộp giảm tốc TT.

## Đọc thêm

- [Danh mục McMaster-Carr](https://www.mcmaster.com/) — tra cứu ốc, đai ốc nyloc, vòng chặn trục và khớp nối hàm theo tên để học quy cách kích thước (chỉ dùng như tài liệu tra cứu, không cần đặt hàng từ nước ngoài).
- [Đai ren nhiệt trên RepRap](https://reprap.org/wiki/Threaded_insert) — hướng dẫn sử dụng đai đồng cấy ren bằng nhiệt cho chi tiết in 3D, giúp tạo ren M3 bền vững trên nhựa PLA.
- [Bạc đạn bi (tổng quan)](https://en.wikipedia.org/wiki/Ball_bearing) — tổng quan về cấu tạo vòng bi và kích thước tiêu chuẩn 608.
