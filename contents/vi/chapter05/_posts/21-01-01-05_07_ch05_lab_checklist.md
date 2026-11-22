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

Bài này là mốc kiểm tra hoàn thành Chương 05 trước khi chuyển sang phần cơ khí ở Chương 06 và tích hợp hai kênh PWM có dấu, pin cùng cầu chì ở Chương 07. Bạn vượt qua chương này khi điền đầy đủ bảng kiểm chứng bên dưới bằng số liệu và ảnh thực tế của chính mình: tên chip cầu H, bảng chân lý, nguồn động cơ tách khỏi USB, ghi chú dòng không tải/stall, phép tính xung servo (ngay cả khi không có servo), kiểm thử dừng bang-bang, ảnh đấu dây và hai lỗi đã gặp hoặc chủ động diễn tập.

## Mục tiêu học

Sau bài này, bạn hoàn thiện bảng ký duyệt Chương 05 bằng các bằng chứng đo đạc và tính toán cụ thể thay vì đánh dấu chung chung. Bạn nộp được ảnh chụp đấu dây chứng minh nguồn động cơ tách biệt khỏi USB nhưng nối chung mass, trình bày rõ ràng tiêu chí hoàn thành trước khi bước vào Chương 06, và lập danh sách mua bổ sung ngắn gọn chỉ gồm những linh kiện thực sự còn thiếu (mạch cầu H, động cơ TT, cầu chì).

## Kiến thức cần có

Nội dung bảng tổng hợp trực tiếp từ bài 05-01 đến bài 05-06. Bạn cần mở sẵn `lab-notes.md`, đồng hồ vạn năng và ảnh chụp mạch thật. Với các mục chưa có phần cứng (như servo hoặc bước đo stall), bắt buộc hoàn thành phần tính toán tương ứng thay vì ghi "để sau".

## Vì sao bài này quan trọng với Capstone A và ROS

Khi ghép khung xe ở Chương 06 và nối hệ thống dây ở Chương 07, mọi tầng phần mềm phía trên (bao gồm lệnh `Twist` từ ROS 2 về sau) đều dựa vào sự chính xác của các ghi chép tại đây. Một bảng chân lý sai dấu, một mức dòng stall chưa đối chiếu với cầu chì hay một nhánh timeout bị bỏ sót đều sẽ dẫn tới robot quay sai chiều, tự reset do sụt áp hoặc không dừng trước vật cản. Bước rà soát này bảo đảm toàn bộ nền tảng chấp hành đã vững trước khi lắp ráp cơ khí.

## Yêu cầu chi tiết của từng mục kiểm tra

- **Nhận diện mạch cầu H:** ghi đúng mã chip (`L298N`, `TB6612` hoặc `DRV8833`) thay vì màu bo mạch, kèm một chân dễ gây lỗi đặc trưng: với TB6612 là "phải kéo `STBY` lên cao"; với L298N là "rút jumper 5 V khi `VM > 12 V` và không nuôi ESP32 từ IC 7805 tích hợp"; với DRV8833 là "dải `VM` 2,7–10,6 V và cần chú ý giới hạn dòng stall".
- **Bảng chân lý:** ghi đủ các tổ hợp `(IN1, IN2, PWM)` và hành vi thực tế của trục, khoanh rõ bộ ba quy ước chiều tiến cho Chương 07 và phân biệt trạng thái trôi (coast) với hãm (brake).
- **Nguồn động cơ tách khỏi USB:** ảnh chụp phải thể hiện rõ pin/nguồn bàn cấp cho `VM`, cáp USB chỉ cắm vào vi điều khiển và có dây nối `GND` chung giữa hai khối.
- **Ghi chú dòng không tải và stall:** ghi dòng không tải đo được cho một động cơ, cộng dòng stall đo trong 1 giây (nếu có nguồn giới hạn dòng) hoặc công suất stall tính từ datasheet, kèm câu chọn cầu chì trên dây dương pin cao hơn dòng chạy bình thường.
- **Xung servo:** nếu đã thực hành với servo, ghi ba góc đo; nếu không có servo, ghi phép tính:

$$
\frac{1.5~\mathrm{ms}}{20~\mathrm{ms}} = 7.5\%
$$

kèm giải thích rằng duty 7,5% ở 1 kHz chỉ tạo xung 75 µs nên phải dùng `writeMicroseconds(1500)` từ thư viện servo.

- **Kiểm thử vòng kín bang-bang:** nêu rõ ba trường hợp bằng số liệu cụ thể (xa hợp lệ $\rightarrow$ `PWM = 80` tiến, dưới 20 cm $\rightarrow$ `PWM = 0`, timeout hoặc 0 $\rightarrow$ `PWM = 0`) và khẳng định `/cmd_vel` về sau không được ghi đè cú dừng này.
- **Ảnh đấu dây:** ảnh rõ nét để bạn cùng nhóm có thể nhận diện `VM`, dây mass chung và dây tín hiệu PWM.
- **Hai chế độ lỗi:** ghi hai lỗi thực tế bạn đã gặp hoặc chủ động diễn tập kiểm thử (ví dụ rút dây Echo để kiểm tra dừng an toàn, hoặc tính đối chiếu dòng stall 2,4 A so với giới hạn 0,5 A của USB), không chép nguyên văn danh sách giáo trình.

## Ví dụ một sổ ghi chép đạt yêu cầu

Một sổ mẫu ghi: dùng `TB6612`, `STBY` nối `3V3`, chiều tiến là `IN1 = 1`, `IN2 = 0`, `PWM > 0`; `VM` cấp từ pin 2S, USB chỉ cắm ESP32; đo không tải 0,18 A ở 7,4 V; tài liệu nhà bán ghi stall 1,2 A ở 6 V. Kiểm tra tính toán:

$$
R \approx \frac{6}{1.2} = 5~\Omega
$$

$$
P = I^2 R = (1.2)^2 \times 5 = 7.2~\mathrm{W}
$$

Ước lượng "khoảng 7 W khi stall ở 6 V" là hợp lý; hai động cơ kẹt cùng lúc khoảng 2,4 A, trong khi tổng dòng chạy bình thường ước tính $0{,}2 + 0{,}2 + 0{,}1 = 0{,}5~\mathrm{A}$ nên chọn cầu chì 2 A trên dây dương pin. Dòng servo ghi $$1500/20000 = 0.075$$; dòng bang-bang ghi 180 mm dừng, 900 mm chạy `PWM = 80`, timeout dừng; hai lỗi diễn tập gồm để nổi `STBY` (bánh không quay cho tới khi nối dây) và lỗi ban đầu xử lý timeout nhầm sang nhánh tiến rồi đã sửa. Sổ này đạt đầy đủ tiêu chí.

## Hình đối chiếu

Sử dụng ba sơ đồ sau để rà soát kiến thức trong quá trình ký duyệt bảng:

![Đường cầu H bạn đã đi khi viết bảng chân lý]({{ site.imgurl }}/generated/hbridge_concept.png)

![Stall so với không tải, đường cong đứng sau ghi chú dòng của bạn]({{ site.imgurl }}/generated/stall_current.png)

![Cảm nhận, tính, tác động, gồm nhánh dừng mà một lần đọc hỏng phải đi]({{ site.imgurl }}/generated/sense_compute_act.png)

## Lab

### An toàn

Buổi rà soát này không yêu cầu chạy lại thí nghiệm ở công suất lớn. Nếu không đủ điều kiện đo stall an toàn, chỉ cần trình bày phần tính toán. Tuyệt đối không cấp `VM` từ USB để chụp ảnh; luôn nhấc bánh khi kiểm tra lại bảng chân lý và giữ tay trên công tắc nguồn nếu chạy thử trên sàn.

### BOM

| Món | Vai trò |
|------|------|
| `lab-notes.md` và ảnh đấu dây | Hồ sơ bằng chứng |
| Đồng hồ vạn năng | Bổ sung nếu còn thiếu số đo điện áp |
| Mạch cầu H, một động cơ, cảm biến khoảng cách | Bổ sung nếu còn thiếu mục thực hành |
| Cầu chì và đế *(nếu chưa có)* | Chuẩn bị sẵn cho Chương 07 |

### Các bước

1. Chép bảng ký duyệt bên dưới vào `lab-notes.md`.
2. Điền đầy đủ từng dòng từ kết quả các bài trước; nếu thiếu mục nào thì bổ sung phép đo hoặc phép tính tương ứng.
3. Đính kèm ảnh đấu dây kèm chú thích tên chip và nguồn cấp `VM`.
4. Rà soát lại toàn bộ bảng để bảo đảm giải thích trôi chảy từng mục, đặc biệt hành vi dừng khi cảm biến timeout.
5. Lập danh sách mua bổ sung ngắn gọn chỉ gồm các món còn thiếu (mạch cầu H, động cơ TT, cầu chì).

### Kết quả mong đợi

Bảng ký duyệt hoàn chỉnh kèm phần tóm tắt đạt yêu cầu bằng lời của bạn sao cho người khác nhìn vào ảnh và bảng có thể xác định ngay cấu hình chiều tiến và điều kiện ngắt PWM về 0.

### Lỗi thường gặp

| Hiện tượng | Cần kiểm tra |
|------------|--------------|
| Các ô chỉ ghi chữ "có" mà thiếu số liệu | Thay bằng con số cụ thể (điện áp, dòng, độ rộng xung, khoảng cách) |
| Bảng chân lý thiếu trạng thái trôi/hãm | Xem lại bài 05-01 và ghi rõ hành vi khi hai ngõ vào bằng nhau |
| Ảnh chỉ thấy cáp USB mà không thấy nguồn động cơ | Chưa tách nguồn `VM`; chụp lại với pin/nguồn bàn nối vào `VM` |
| Bỏ trống dòng servo vì không có phần cứng | Bổ sung phép tính 7,5% và so sánh với 75 µs ở 1 kHz |
| Hai lỗi chỉ chép lại từ giáo trình | Thay bằng hai tình huống thực tế bạn đã gặp hoặc diễn tập kiểm thử |

### Bảng ký duyệt

| Hạng mục | Bằng chứng của bạn | Xong |
|-----|----------------|------|
| Chip cầu H và chân dễ gây lỗi (`STBY`, jumper 7805, hoặc dải `VM`) | | |
| Bảng chân lý: `IN1`, `IN2`, `PWM`, chiều quay, gồm trôi hoặc hãm | | |
| Nguồn động cơ tách khỏi USB, nối chung mass (ảnh) | | |
| Dòng không tải, và dòng stall đo được hoặc công suất stall tính tay | | |
| Servo: ba góc đo, hoặc $$1.5/20 = 7.5\%$$ và `writeMicroseconds(1500)` | | |
| Bang-bang: xa, dưới 20 cm, timeout/0 | | |
| Ảnh đấu dây đã lưu | | |
| Hai chế độ lỗi đã gặp hoặc diễn tập | | |

**Điều kiện hoàn thành:** điền đầy đủ mọi dòng trong bảng, ảnh đấu dây khớp sơ đồ tách nguồn và trình bày rõ cơ chế ép động cơ dừng khi cảm biến timeout. Khi đạt mốc này, bạn đã sẵn sàng sang phần cơ khí Chương 06 và đấu dây hoàn chỉnh ở Chương 07.

## Mua ở Việt Nam

Chỉ mua bổ sung linh kiện còn thiếu (thường là TB6612 hoặc L298N, cặp động cơ TT và cầu chì 2–3 A kèm đế). Giá tham khảo thay đổi theo thời điểm (L298N khoảng 35.000–70.000 VND, TB6612 khoảng 40.000–120.000 VND, động cơ TT khoảng 25.000–45.000 VND, cầu chì và đế khoảng 5.000–25.000 VND):

- Trang L298N đã kiểm tra, khoảng 45.000 VND: [hshop.vn/mach-dieu-khien-dong-co-dc-l298](https://hshop.vn/mach-dieu-khien-dong-co-dc-l298)
- HShop: [TB6612](https://hshop.vn/search?q=TB6612), [motor TT](https://hshop.vn/search?q=motor%20TT), [cầu chì](https://hshop.vn/search?q=cau%20chi)
- Shopee: [TB6612](https://shopee.vn/search?keyword=TB6612), [motor TT](https://shopee.vn/search?keyword=motor%20TT), [cầu chì](https://shopee.vn/search?keyword=cau%20chi)
- Lazada: [L298N](https://www.lazada.vn/catalog/?q=L298N), [motor TT](https://www.lazada.vn/catalog/?q=motor%20TT)
- Thế Giới IC: [TB6612](https://www.thegioiic.com/search?q=TB6612), [L298N](https://www.thegioiic.com/search?q=L298N)

## Video tham khảo

- **Xem trước:** [TB6612FNG H-Bridge Motor Controller - Better than L298N?](https://www.youtube.com/watch?v=JPPTRj0KWbg) — DroneBot Workshop, tiếng Anh. Đối chiếu lại sơ đồ đấu dây và hoạt động đảo chiều/tốc độ của đúng module bạn sử dụng trước khi chốt chương.

## Bài tập

1. Nếu một ô trong bảng ký duyệt chỉ ghi chữ "có", điều gì xảy ra với kết quả kiểm tra dù các ô khác đều có số liệu?
2. Tài liệu ghi dòng stall 1,2 A ở 6 V. Tính $$R$$ và $$P$$, rồi đánh giá nhận định "khoảng 7 W" có đạt yêu cầu tính toán không.
3. Nếu không có servo vật lý, cần ghi phép tính và lời gọi hàm nào vào dòng servo?
4. Liệt kê đủ ba trường hợp bắt buộc phải có trong dòng bang-bang.
5. Cần thỏa mãn điều kiện gì (bao gồm hành vi timeout) để chính thức chuyển sang Chương 06?

### Gợi ý đáp án

1. Dòng đó không đạt; mỗi mục yêu cầu bằng chứng cụ thể (số liệu đo, tên chân, phép tính hoặc ảnh).
2. $$R \approx 5~\Omega$$ và $$P = 7.2~\mathrm{W}$$, nên nhận định "khoảng 7 W" đạt yêu cầu.
3. Ghi $$1.5/20 = 7.5\%$$ và lời gọi hàm `writeMicroseconds(1500)` (kèm đối chiếu 75 µs ở 1 kHz).
4. Ba trường hợp: khoảng cách xa hợp lệ (`PWM = 80` tiến), khoảng cách dưới 20 cm (`PWM = 0`), và timeout hoặc 0 (`PWM = 0`).
5. Hoàn thành đủ tất cả các dòng bảng ký duyệt bằng bằng chứng thực tế và xác nhận cảm biến timeout luôn ép động cơ dừng.

## Đọc thêm

- Datasheet ST L298: [https://www.st.com/resource/en/datasheet/l298.pdf](https://www.st.com/resource/en/datasheet/l298.pdf)
- Pololu TB6612FNG: [https://www.pololu.com/product/713](https://www.pololu.com/product/713)
- SparkFun — chọn động cơ (stall so với không tải): [https://learn.sparkfun.com/tutorials/motors-and-selecting-the-right-one/all](https://learn.sparkfun.com/tutorials/motors-and-selecting-the-right-one/all)
- Topic ROS 2 (cơ chế cho `/cmd_vel` về sau): [https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Topics/Understanding-ROS2-Topics.html](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Topics/Understanding-ROS2-Topics.html)
