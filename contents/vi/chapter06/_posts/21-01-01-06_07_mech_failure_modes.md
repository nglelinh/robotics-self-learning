---
layout: post
title: "Hỏng hóc cơ khí và chống kéo dây"
chapter: "06"
order: 7
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter06
lesson_type: required
draft: false
---

Thời lượng ước tính: **60–80 phút**, gồm một lần giật thử khi đã cắt nguồn và một lần làm giảm lực kéo dây (strain relief), có ảnh trước và sau.

## Mục tiêu học

Hết bài này, các bạn gọi tên được dạng hỏng khi bánh kêu tách mà encoder vẫn đếm, khi càng nhựa bị mòn răng, khi mối hàn đứt sau lúc khung uốn, và khi bánh cà có mùi động cơ kẹt. Các bạn thêm giảm lực kéo dây (strain relief) để mối hàn không còn bị bẻ, chừa một vòng dây dự phòng, và viết hai dạng hỏng sẽ kiểm vào ngày Capstone trước khi gọi robot là sẵn sàng.

## Kiến thức cần có

Bài 01 đến Bài 06: $$b$$ và $$r$$, vít cố định trục trên mặt vát chữ D, tỉ số truyền, khoảng đuôi bánh caster, và một vật liệu khung có thể nứt. Chương 05 là nơi dòng kẹt trở thành một con số trên động cơ của các bạn. Lab này không bao giờ đặt dòng ấy lên dây. Nguồn tắt.

## Vì sao bài này quan trọng với Capstone A và ROS

ROS sẽ vẽ một vệt odometry trơn từ xung encoder và từ $$i$$, $$b$$, $$r$$ trong sổ. Một số hỏng cơ khí để những xung ấy hoàn hảo trong khi đường trên sàn sai. Vít cố định trục trượt khỏi mặt vát, moay-ơ mòn răng, bánh cà khung, và bánh caster nhấc lên, tất cả nhìn trên màn hình topic giống một bài toán chỉnh tham số. Chúng là bài toán của bàn tay. Các bạn sửa chúng khi pin đã ngắt, rồi mới có quyền chỉnh. Giảm lực kéo dây là dạng hiện ra sau một giờ demo: mối hàn uốn mỗi cú xóc, đồng mỏi, và `cmd_vel` vẫn được xuất bản vào một động cơ đã mất điện.

## Những hỏng tìm được bằng tay

Vít cố định trục trượt khỏi mặt vát chữ D. Moay-ơ kêu tách, bánh khựng, động cơ và encoder của nó vẫn quay. Robot gần như không nhích so với dòng các bạn nghe thấy. Odometry cộng $$r \Delta\theta$$ như thể bánh đã đi theo động cơ. Đó là lời nói dối odometry kinh điển. Bài 02 đã đặt ốc đúng chỗ. Bài này là lần kiểm lại sau khi vận chuyển, vì một ốc ngồi trên đỉnh tròn sẽ lỏng dần.

Càng servo hoặc moay-ơ bị mòn răng trong nhựa. Càng servo và moay-ơ bánh rẻ tự cắt răng trong nhựa mềm. Khi răng đã mất, ốc vẫn cảm thấy chặt và đầu ra chỉ làm tròn lỗ. Thay càng hoặc thay moay-ơ. Keo trát lên răng đã mòn là chuyện giả cho một buổi demo.

Mỏi dây tại mối hàn. Khung uốn, mối hàn là điểm cứng, và sợi đồng đứt trong lớp cách điện, cách mối hàn bóng vài milimét. Sợi cáp nhìn vẫn lành. Giảm lực kéo dây (strain relief) chuyển chỗ bẻ ra khỏi điểm ấy: một dây rút, hoặc một giọt keo nến, neo dây vào tấm để mối hàn không thấy chuyển động. Phía trước điểm neo, chừa một vòng dây dự phòng, một cung chùng có chủ đích. Một sợi kéo căng giữa cụm bánh di động và mạch điều khiển không có vòng để nhường, nên mối hàn phải trả cái bẻ. Làm việc này trên dây động cơ và trên dây encoder. Một dây encoder mỏi trông như cảm biến chết trong firmware Chương 04.

Bánh cà khung. Mặt lốp hôn tấm hoặc đầu ốc. Tốc độ tụt, dòng leo về phía giá trị kẹt của Chương 05, và sau vài giây động cơ có mùi nóng. Các bạn cảm được chỗ cà khi pin đã rút: xoay bánh bằng tay và nghe một tiếng cạo mỗi vòng. Dịch bánh ra, hoặc giũa vật gây cạ, trước khi gọi đó là lỗi mạch cầu.

Bánh caster lắc khi chạy nhanh. Mũi dao động. Khoảng đuôi bị ngược hoặc quá ngắn, hoặc trọng tâm từ Bài 01 gần như không đè caster, nên vết tiếp xúc không ổn định được. Sửa khoảng đuôi và tải. Một bộ giảm chấn phần mềm sẽ không bịa ra khoảng đuôi.

Pin trượt. Một cục pin lỏng dịch chuyển trọng tâm, tam giác đỡ đột ngột trống dưới khối lượng ấy, và bánh caster bật lên. Rồi một bánh chủ động mất tải và robot quay ngang. Một đai in hoặc một túi buộc bằng dây rút, theo phương án vật liệu của Bài 06, giữ cục pin ở chỗ các bạn đã đo $$b$$.

![Những vùng khung mà các dạng hỏng này sống: bánh, đường trục, caster, và dây chạy dọc tấm]({{ site.imgurl }}/generated/chassis_measures.png)

Dùng hình như một bản đồ. Chạm từng vùng trong lab: cả hai moay-ơ, cả hai khe bánh, càng caster, vết đặt pin, và mọi sợi dây rời một mối hàn.

## Ví dụ tính tay

Encoder báo một vòng đủ của động cơ tại trục bánh sau khi qua tỉ số, và vít cố định trục trượt cả vòng ấy. Với $$r = 31.2$$ mm,

$$
s_{\text{phantom}} = 2\pi r = 2\pi \times 31.2 \approx 196\ \text{mm}.
$$

Bản đồ được cộng khoảng 20 cm mà viên gạch không hề cho. Hai lần trượt như thế trên mỗi mét hành trình được lệnh là một lỗi tỉ lệ 40 cm mà không chỉnh hiệp phương sai nào che cho trung thực. Cách sửa là cơ khí: mặt vát nằm dưới ốc, giật bánh, chụp ảnh.

Bánh cà là người anh em nhiệt. Nếu động cơ lăn tự do ở Chương 05 chỉ rút một dòng không tải nhỏ, và chỗ cà đẩy điểm làm việc về phía kẹt, nhiệt trong cuộn dây đi theo dòng ấy. Hôm nay không cần một con số mới. Cần tiếng cạo biến mất trước khi điện áp trở lại.

## Lab: giật thử và một điểm neo

### An toàn

Pin ngắt, mạch cầu rút phích, USB rút nếu mạch đang nằm trên robot. Phép giật là phép thử bằng tay. Keo nến là nguồn nhiệt duy nhất: giữ đầu súng khỏi lớp cách điện các bạn còn cần, và khỏi ngón tay. Đừng thử giảm lực kéo dây bằng cách cấp điện cho động cơ rồi túm bánh.

### BOM

| Hạng mục | Vai trò |
|------|------|
| Khung, hoặc một dây động cơ trên bàn nếu tấm chưa về | Các mối |
| Dây rút, hoặc một cây keo nến và súng | Một điểm giảm lực kéo dây |
| Điện thoại | Trước và sau |
| `lab-notes.md` | Hai mục kiểm ngày Capstone |

### Các bước

1. Khi nguồn đã tắt, giật từng giắc dọc theo vỏ giắc, không giật bằng dây. Giắc nào trườn ra thì cắm lại và, nếu vỏ cho phép, một giọt keo chỉ trên vỏ.
2. Uốn từng dây tại mối hàn. Nếu mối hàn bị bẻ, chỗ giảm lực kéo dây đang thiếu.
3. Chụp mối tệ nhất. Thêm một dây rút hoặc một điểm neo keo sao cho chỗ bẻ bắt đầu cách mối hàn ít nhất một centimét. Chừa một vòng dây dự phòng. Chụp lại.
4. Vặn từng bánh. Xác nhận vít cố định trục giữ và mặt lốp không cạo.
5. Thử trượt pin. Nếu nó dịch, ghi đai các bạn còn nợ.
6. Viết hai dạng hỏng các bạn sẽ kiểm vào ngày Capstone, theo thứ tự sẽ kiểm, trước khi bất kỳ ai xuất bản `cmd_vel`.

### Kết quả mong đợi

Một ảnh trước và một ảnh sau của một mối đã được neo, cùng hai mục kiểm đã viết. Một cặp tốt là: vít cố định trục trên mặt vát, và không có tiếng cạo khi xoay bánh bằng tay. Mối hàn của dây đứng yên khi các bạn lắc vòng dây dự phòng.

### Lỗi thường gặp

| Các bạn thấy | Thường nghĩa là |
|--------------|------------------------|
| Bánh kêu tách, trục không theo | Vít cố định trục trượt khỏi mặt vát, hoặc moay-ơ mòn răng |
| Sợi đứt ngay cạnh một mối nhìn vẫn đẹp | Mỏi; thêm giảm lực kéo dây trên mối thay thế |
| Một tiếng cạo mỗi vòng, và trí nhớ về mùi động cơ ở Chương 05 | Bánh cà |
| Caster đập trái phải | Khoảng đuôi hoặc trọng tâm |
| Pin dịch khi nghiêng tấm | Thiếu đai; caster sẽ mất tải ở lần tăng tốc đầu |

## Mua ở Việt Nam / Where to buy in Vietnam

Các bạn cần một túi dây rút và một cây keo nến hơn là một động cơ mới. Chỉ mua moay-ơ dự phòng nếu cái đang có đã bị làm tròn lỗ.

| Mua gì | Từ khóa | Khoảng giá (VND) | Ghi chú |
|------|----------|------------------|-------|
| Dây rút | `dây rút nhựa` | 10.000–30.000 | Giảm lực kéo dây và đai pin tạm |
| Keo nến | `keo nến` | 15.000–40.000 | Neo dây, giữ keo khỏi tiếp điểm |
| Bánh TT dự phòng | `bánh xe cao su 65mm` | 15.000–45.000 | Nếu moay-ơ đã mòn răng |

Các trang tìm:

- [Shopee: dây rút](https://shopee.vn/search?keyword=d%C3%A2y%20r%C3%BAt%20nh%E1%BB%B1a)
- [Lazada: keo nến](https://www.lazada.vn/catalog/?q=keo%20n%E1%BA%BFn)
- [Hshop: bánh xe](https://hshop.vn/search?q=b%C3%A1nh+xe+cao+su)
- [Thế Giới IC](https://www.thegioiic.com/search?q=d%C3%A2y%20%C4%91i%E1%BB%87n)

Giá dịch chuyển. Một giắc rơi ra là việc hàn của Chương 01, không phải việc của phần mềm.

## Bài tập

1. Robot bò tới trên sàn trong khi số đếm encoder chạy rất nhanh. Gọi tên dạng hỏng và phép kiểm bằng tay.
2. Răng nhựa của một càng servo đã bị làm tròn. Ốc vẫn chặt. Các bạn thay gì, và vì sao keo là phương án yếu?
3. Dây động cơ được hàn và kéo thẳng tới mạch cầu, không chùng. Các bạn thêm gì, và mối hàn phải cảm thấy thế nào khi lắc dây?
4. Dòng cao, tốc độ thấp, có mùi nóng. Vít cố định trục vẫn giữ. Các bạn tìm sự cản cơ khí nào?
5. Viết hai mục kiểm ngày Capstone thành câu đầy đủ mà một đồng đội làm được khi pin vẫn đang ngắt.

### Gợi ý đáp án

1. Bánh đang trượt trên trục: vít cố định trục trượt khỏi mặt vát, hoặc moay-ơ mòn răng. Vặn bánh bằng tay khi nguồn tắt; nó không được kêu tách. 2. Thay càng. Keo trên răng đã tròn để lần kẹt kế tiếp hoàn tất cái lỗ. 3. Một dây rút hoặc điểm neo keo nến, cộng một vòng dây dự phòng. Mối hàn phải đứng yên. 4. Bánh cà khung hoặc đầu ốc. Xoay bằng tay và loại tiếng cạo. 5. Bất kỳ hai mục nào trong bài này, làm khi nguồn tắt: ốc trên mặt vát, không có tiếng cạo, caster có đuôi và có tải, pin không trượt, mỗi mối hàn đã được giảm lực kéo dây. Các câu phải nói “đạt” trông như thế nào.

## Đọc thêm

- [Adafruit, dây và giắc](https://learn.adafruit.com/wires-and-connectors/wire) — dây, mối nối, và vì sao sợi đứt ngay cạnh mối hàn.
- [SparkFun, căn bản giắc nối](https://learn.sparkfun.com/tutorials/connector-basics/all) — vỏ giắc các bạn giật bằng vỏ, không giật bằng lõi dẫn.
- [Gỡ lỗi in trên RepRap](https://reprap.org/wiki/Print_Troubleshooting) — moay-ơ nhựa mòn răng và nứt lớp, nếu chi tiết hỏng là chi tiết in.
