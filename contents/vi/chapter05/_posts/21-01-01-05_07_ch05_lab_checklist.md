---
layout: post
title: "Checklist lab chương 05"
chapter: "05"
order: 7
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter05
lesson_type: required
draft: false
---

Bài này là một cổng. Chương 06 sẽ đặt hệ dẫn động của bạn lên khung, và Chương 07 sẽ lắp PWM trái và phải có dấu, một pin, và một cầu chì. Bạn qua cổng khi bảng dưới đây được điền bằng chứng cứ của chính bạn: một driver đã gọi tên, một bảng chân lý, một nguồn motor không phải USB, một ghi chú stall hoặc không tải, một phép tính xung servo dù bạn đã bỏ qua càng, một cú dừng bang-bang bạn mô tả được, một ảnh dây, và hai chế độ hỏng bạn hoặc đã gặp hoặc đã diễn tập có chủ đích. Một dòng trống nghĩa là bạn vẫn đang ở Chương 05.

## Mục tiêu học

Hết bài, bạn hoàn thành bảng ký bằng chứng cứ đã đo hoặc đã tính, không phải bằng cách kể lại tên bài. Bạn đưa một ảnh dây trong đó dòng motor và USB là hai nguồn tách nhau nhưng mass chung. Bạn nêu một điều kiện đạt mà có thể nói to cho bạn lab trước khi bắt đầu cơ khí Chương 06. Bạn chỉ liệt kê những món còn thiếu (driver, motor TT, cầu chì) và từ khóa tìm để mua.

## Kiến thức cần có

Các bài 05-01 đến 05-06 là nguồn của mọi dòng. Bạn cần `lab-notes.md` đang mở, đồng hồ, và tấm ảnh chụp khi dây thực sự nằm trên driver. Nếu một dòng phần cứng không làm được, dòng đó vẫn cần phép tính mà checklist này gọi tên. “Để sau” không phải là đạt.

## Vì sao bài này quan trọng với Capstone A và ROS

Capstone A là robot hai bánh mà đế ROS 2 về sau nhận một twist và phát hai nỗ lực bánh. Phần mềm đó chỉ trung thực bằng các dấu bạn đã ghi ở đây. Một bảng chân lý chép của bạn học, một xung servo bạn chưa từng tính, hoặc một dòng stall bạn chưa từng đem so với cầu chì, thành một robot yaw sai chiều, brownout, hoặc chạy xuyên một timeout. Cổng này cố tình nhàm. Giá đỡ Chương 06 và bộ dây Chương 07 giả định các câu trả lời này đã có trong sổ.

## Mỗi dòng đang hỏi gì

**Driver đã nhận diện.** Viết tên chip, không viết màu PCB: L298N, TB6612, hoặc DRV8833. Thêm một chân hay cắn người trên chip đó. Với TB6612, câu ấy là “STBY phải cao, nếu không motor ngủ”. Với L298N, câu ấy là “jumper 5 V phải rút nếu VM trên 12 V, và ESP32 không được nuôi từ 7805 onboard”. Với DRV8833, đó là dải motor khoảng 2,7–10,6 V, và việc một cặp TT lúc stall là đòi hỏi lớn.

**Bảng chân lý đã ghi.** Bốn dòng, hoặc các dòng chip của bạn thực sự ghi trong tài liệu, với IN1, IN2, PWM, và trục đã làm gì. Khoanh bộ ba tiến mà Chương 07 sẽ gọi là dương. Nếu hai ngõ vào bằng nhau tạo hãm trên board của bạn, hãy nói vậy. Dòng đó không phải màu trang trí.

**Nguồn motor tách khỏi USB.** Ảnh phải cho thấy pin hoặc nguồn bàn trên VM, USB chỉ trên vi điều khiển, và một dây mass giữa chúng. Một chú thích nói “mass chung” mà không có sợi dây trong khung thì không đạt.

**Ghi chú stall hoặc không tải.** Một dòng không tải đã đo cho một motor, cộng hoặc một số stall một giây lấy dưới giới hạn dòng, hoặc số watt đã tính từ dòng stall của người bán. Câu cầu chì ngồi trong cùng ghi chú này: giá trị cầu chì nằm trên dòng chạy và có mặt để đứt khi chập.

**Xung servo.** Nếu bạn đã quét càng, dán ba góc. Nếu không có servo, viết

$$
\frac{1.5~\mathrm{ms}}{20~\mathrm{ms}} = 7.5\%
$$

và một câu: duty 7,5% trên chân 1 kHz là xung 75 µs, nên lệnh bạn sẽ dùng là `writeMicroseconds(1500)` từ thư viện servo.

**Hành vi bang-bang.** Ba trường hợp bằng số của bạn: một số đọc xa, một số đọc dưới 20 cm, và một timeout hoặc 0. Cả ba được gọi tên, với PWM 80 tiến chỉ trên số đọc xa hợp lệ. Nói rằng một `/cmd_vel` tương lai không ghi đè cú dừng.

**Ảnh dây.** Một ảnh, chân đọc được đủ để bạn lab tìm VM, mass, và dây PWM.

**Hai chế độ hỏng.** Chúng phải là của bạn. Gặp chúng thì tính. Diễn tập chúng thì tính: rút dây echo và nhìn cú dừng, hoặc tính dòng stall qua USB và viết “tôi sẽ không cấp VM từ USB” vì 2,4 A không phải 0,5 A. Một danh sách chép từ trang này, không có động từ bạn đã làm, không tính.

## Ví dụ sổ đã điền

Một cuốn sổ khai: TB6612, STBY nối vào 3,3 V, tiến là IN1 = 1, IN2 = 0, PWM > 0, VM từ 2S, USB chỉ trên ESP32, không tải 0,18 A ở 7,4 V, người bán ghi stall 1,2 A ở 6 V. Kiểm số stall trước khi nhận dòng đó.

$$
R \approx \frac{6}{1.2} = 5~\Omega
$$

$$
P = I^2 R = (1.2)^2 \times 5 = 7.2~\mathrm{W}
$$

Ghi chú “khoảng 7 W nếu stall ở 6 V định mức” khớp. Hai motor sẽ khoảng 2,4 A ở stall đó. Một ước lượng chạy 0,2 A mỗi motor cộng 0,1 A logic là 0,5 A, nên cầu chì 2 A trên dây dương pin nằm trên dòng chạy và vẫn có việc khi chập chết. Dòng servo của họ nói $$1500/20000 = 0.075$$. Dòng bang-bang nói 180 mm thì dừng, 900 mm chạy ở PWM 80, timeout thì dừng. Họ đã diễn tập một STBY nổi (bánh chết cho đến khi thêm dây) và một timeout mà lúc đầu họ coi là “xa”, rồi sửa. Cuốn sổ đó đạt. Cuốn sổ có tên chip mà các ô đo trống thì không.

## Hình

Dùng ba ảnh này như những bức bạn phải kể được trong khi ký bảng.

![Đường cầu H bạn đã đi khi viết bảng chân lý]({{ site.imgurl }}/generated/hbridge_concept.png)

![Stall so với không tải, đường cong đứng sau ghi chú dòng của bạn]({{ site.imgurl }}/generated/stall_current.png)

![Cảm nhận, tính, tác động, gồm nhánh dừng mà một lần đọc hỏng phải đi]({{ site.imgurl }}/generated/sense_compute_act.png)

## Lab

### An toàn

Buổi ký này không bắt bạn lặp mọi thí nghiệm ở đầy công suất. Nếu một dòng thiếu vì stall sẽ không an toàn, hãy tính và nói vì sao bạn từ chối stall. Đừng cắm VM vào USB “chỉ để chụp ảnh”. Bánh ở trên không nếu bạn chạy lại một dòng bảng chân lý. Tay trên công tắc nguồn nếu bạn chạy lại cú dừng trên sàn.

### BOM

| Món | Vai trò |
|------|------|
| `lab-notes.md` và ảnh dây | Chứng cứ |
| Đồng hồ vạn năng | Chỉ khi một ô điện áp còn trống |
| Driver, một motor, cảm biến khoảng cách | Chỉ để điền một dòng bạn đã bỏ |
| Cầu chì và đế, nếu bộ kit chưa có | Món Chương 07 bạn có thể mua ngay |

### Các bước

1. Chép bảng ký vào `lab-notes.md`.
2. Điền mỗi ô từ ghi chú bạn đã có. Ô nào trống, làm phép đo hoặc phép tính nhỏ nhất khiến nó thành thật.
3. Đính hoặc dẫn ảnh dây. Chú thích bằng tên chip và “nguồn VM: …”.
4. Đọc đoạn đạt bên dưới thành tiếng. Nếu bạn ngập ở một dòng, dòng đó chưa xong.
5. Viết danh sách mua chỉ cho chỗ thiếu: driver, motor TT, cầu chì. Bỏ những món đã có.

### Kết quả mong đợi

Một bảng đã điền và một đoạn đạt viết bằng lời của bạn. Bạn lab, chỉ nhìn ảnh và bảng, chỉ được trạng thái motor tiến và điều kiện cảm biến ép PWM về 0.

### Lỗi thường gặp

| Bạn thấy | Cần kiểm |
|--------------|----------------|
| Mọi ô nói “có” mà không có số | Thay “có” bằng một điện áp, một dòng, một độ rộng xung, hoặc một khoảng cách. |
| Bảng chân lý không có dòng hãm/trôi | Quay lại bài 05-01 và ghi trạng thái hai ngõ vào bằng nhau trên chip của bạn. |
| Ảnh chỉ có một cáp USB, không có pin | Nguồn motor chưa tách. Chụp lại với VM trên pack. |
| Dòng servo trống vì không có càng | Viết phép tính 7,5% và đối chiếu 75 µs ở 1 kHz. |
| Các chế độ hỏng là danh sách trong giáo trình | Gọi tên hai chế độ bạn đã gây ra hoặc đã diễn tập, kể cả trục đã làm gì. |

### Bảng ký

| Dòng | Chứng cứ của bạn | Xong |
|-----|----------------|------|
| Chip driver và chân hay cắn (STBY, jumper 7805, hoặc dải VM) | | |
| Bảng chân lý: IN1, IN2, PWM, chiều, gồm trôi hoặc hãm | | |
| Nguồn motor tách khỏi USB, mass chung (ảnh) | | |
| Dòng không tải, và ampe stall hoặc watt stall đã tính | | |
| Servo: các góc, hoặc $$1.5/20 = 7.5\%$$ và `writeMicroseconds(1500)` | | |
| Bang-bang: xa, dưới 20 cm, timeout/0 | | |
| Ảnh dây đã lưu | | |
| Hai chế độ hỏng bạn gặp hoặc diễn tập | | |

**Đạt nghĩa là** mọi dòng trên đã điền, ảnh khớp câu chuyện nguồn, và bạn nói được trục làm gì khi cảm biến khoảng cách timeout. Với điều đó, bạn được bắt đầu cơ khí Chương 06, và bạn sẵn sàng để Chương 07 tin dấu tiến của bạn, cầu chì của bạn, và thói quen đặt PWM về 0 trước mọi việc khác.

## Mua ở Việt Nam / Where to buy in Vietnam

Chỉ mua chỗ thiếu. Những chỗ thiếu thường gặp ở cổng này là một driver (TB6612 nên chọn, L298N chấp nhận được), một hoặc hai motor hộp số TT, và một cầu chì 2–3 A có đế trên dây dương pin. Giá chạy. Khoảng thô: module L298N khoảng 35.000–70.000 VND, module TB6612 khoảng 40.000–120.000 VND, motor TT khoảng 25.000–45.000 VND, cầu chì và đế khoảng 5.000–25.000 VND.

- Trang L298N đã kiểm, khoảng 45.000 VND: [hshop.vn/mach-dieu-khien-dong-co-dc-l298](https://hshop.vn/mach-dieu-khien-dong-co-dc-l298)
- HShop: [TB6612](https://hshop.vn/search?q=TB6612), [motor TT](https://hshop.vn/search?q=motor%20TT), [cầu chì](https://hshop.vn/search?q=cau%20chi)
- Shopee: [TB6612](https://shopee.vn/search?keyword=TB6612), [motor TT](https://shopee.vn/search?keyword=motor%20TT), [cầu chì](https://shopee.vn/search?keyword=cau%20chi)
- Lazada: [L298N](https://www.lazada.vn/catalog/?q=L298N), [motor TT](https://www.lazada.vn/catalog/?q=motor%20TT)
- Thế Giới IC: [TB6612](https://www.thegioiic.com/search?q=TB6612), [L298N](https://www.thegioiic.com/search?q=L298N)

## Bài tập

1. Ô nào, nếu để lại mỗi chữ “có”, làm hỏng cổng dù các ô kia đã là số?
2. Ghi chú stall của bạn nói 1,2 A ở 6 V. Tính $$R$$ và $$P$$ rồi nói “khoảng 7 W” có đạt không.
3. Bạn không có servo. Viết đúng phép tính và lời gọi hàm thuộc về dòng đó.
4. Gọi tên ba trường hợp bang-bang mà dòng phải chứa.
5. Chương 06 bắt đầu khi câu nói nào là đúng? Kể cả hành vi timeout.

### Gợi ý đáp án

Một ô chỉ nói “có” thì làm hỏng dòng đó; cổng muốn một con số, một tên chân, hoặc một ảnh. $$R \approx 5~\Omega$$ và $$P = 7.2~\mathrm{W}$$, nên “khoảng 7 W” đạt phần số học. Không có servo thì viết $$1.5/20 = 7.5\%$$ và `writeMicroseconds(1500)`. Ba trường hợp là một số đọc xa hợp lệ (PWM 80 tiến), một số đọc dưới 20 cm (PWM 0), và một timeout hoặc 0 (PWM 0). Bạn được bắt đầu Chương 06 khi nói được rằng cảm biến khoảng cách timeout ép motor tắt, và phần còn lại của bảng đã điền bằng chứng cứ của chính bạn.

## Đọc thêm

- Datasheet ST L298: [https://www.st.com/resource/en/datasheet/l298.pdf](https://www.st.com/resource/en/datasheet/l298.pdf)
- Pololu TB6612FNG: [https://www.pololu.com/product/713](https://www.pololu.com/product/713)
- Chọn motor của SparkFun (stall so với không tải): [https://learn.sparkfun.com/tutorials/motors-and-selecting-the-right-one/all](https://learn.sparkfun.com/tutorials/motors-and-selecting-the-right-one/all)
- Topic ROS 2, chỗ ở về sau của `/cmd_vel`: [https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Topics/Understanding-ROS2-Topics.html](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Topics/Understanding-ROS2-Topics.html)
