---
layout: post
title: "Giới hạn dòng, stall và nhiệt"
chapter: "05"
order: 5
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter05
lesson_type: required
draft: false
---

Datasheet motor có hai dòng quan trọng trên một robot nhỏ, và chúng không gần nhau. Dòng không tải là thứ bạn đo khi bánh ở trên không. Dòng stall là thứ đồng sẽ hút khi trục dừng và suất điện động ngược sụp. Bài này biến số stall ấy thành watt, thành tản nhiệt của driver, thành cầu chì trên dây pin, và thành cú brownout làm robot bỏ chạy.

## Mục tiêu học

Hết bài, bạn phân biệt dòng không tải với dòng stall, và dùng dòng stall để chọn cỡ driver cùng cầu chì. Từ điện áp định mức và dòng stall, bạn ước lượng điện trở cuộn và số watt tiêu tán trong motor đang stall. Bạn ước lượng nhiệt trong L298N từ sụt áp của nó, và nói vì sao TB6612 mát hơn ở cùng dòng. Bạn đặt cầu chì trên dây dương của pin, và coi một nguồn sụt làm reset vi điều khiển là lỗi điều khiển.

## Kiến thức cần có

Định luật Ohm và $$P = I^2 R$$ là toàn bộ hộp công cụ toán. Câu chuyện suất điện động ngược (back-EMF) ở bài 05-01 là lý do dòng stall lớn. Việc nhận diện driver ở bài 05-02 cho bạn biết nhiệt đang rơi vào Darlington có tản nhiệt bắt vít, hay vào cầu MOSFET. Bạn cần nguồn bàn có núm dòng, hoặc một ampe kế mắc nối tiếp, nếu sẽ đo motor thật. Nhánh số học vẫn mở nếu bạn không stall an toàn được.

## Vì sao bài này quan trọng với Capstone A và ROS

Chương 07 đặt pin và cầu chì lên khung vì một cổng USB không nuôi nổi hai motor TT đang stall. Một cặp 18650 yếu cũng sụt khi cả hai bánh khởi động cùng lúc. Nếu vi điều khiển reset, các chân GPIO đi lại qua lúc boot, và một cầu H mới khởi tạo một nửa có thể đẩy bánh trước khi code tới dòng đặt PWM về không. Brownout là lỗi điều khiển, không chỉ lỗi nguồn. ROS 2 về sau sẽ phát `cmd_vel` như thể đế đang thức. Firmware vẫn phải fail-safe khi nguồn sụt hoặc tác vụ cảm biến dừng: motor tắt, và ở tắt, cho đến khi một lần `setup` mới đã chạy. Các con số trong bài này là cách bạn chọn cầu chì sống sót lúc chạy bình thường và vẫn đứt khi dây chập.

## Hai dòng trên một đường cong

Hình của bài phác dòng theo tốc độ. Lúc không tải trục quay nhanh, suất điện động ngược triệt phần lớn nguồn, dòng nhỏ: thường vài trăm miliampe hoặc ít hơn với motor TT vàng, đôi khi chỉ vài chục miliampe với motor trần. Lúc stall, tốc độ bằng không, suất điện động ngược bằng không, và

$$
I_{stall} \approx \frac{V}{R}
$$

Dòng stall trên datasheet, ở điện áp định mức, là con số bạn đưa cho driver và cầu chì. Dòng khi chạy trên sàn phẳng nằm giữa hai đầu, gần không tải cho đến khi bạn leo, đẩy, hoặc đụng mép thảm. Hộp số kẹt vào chân ghế về mặt điện là một lần stall, dù PWM vẫn nói “tiến”.

## Watt trong cái vỏ bằng ngón tay cái

Những watt đó thoát thành nhiệt trong cuộn. Motor stall gần như không có công cơ, nên gần như toàn bộ $$I \times V$$ đốt đồng và chổi than. Một hai giây đo là một điểm dữ liệu. Giữ trục “để cảm mô-men” nửa phút sẽ nấu men cách điện. Hai motor stall cùng lúc hút khoảng gấp đôi dòng stall của một motor, trước tổn hao trên dây. Cổng USB giới hạn gần 0,5 A không cấp nổi mức đó. Cổng gập, vi điều khiển reset, và bạn học brownout với bánh vẫn trên bàn nếu may.

## Nhiệt ở driver và sụt áp của pack

L298N sụt khoảng 2 V ở 1 A. Chip, không phải motor, tiêu tán khoảng

$$
P \approx 2~\mathrm{V} \times 1~\mathrm{A} = 2~\mathrm{W}
$$

trên kênh đó. Hai kênh làm việc nặng có thể gấp đôi. Tản nhiệt bắt vít là đồ bắt buộc, và module vẫn cần không khí. TB6612 sụt ít hơn nhiều ở cùng dòng, nên board mát hơn, và nó vẫn có giới hạn nhiệt cùng giới hạn dòng. Mát hơn không có nghĩa là vô hạn. Nếu vỏ TB6612 đau khi chạm, motor đang stall hoặc định mức liên tục (khoảng 1,2 A mỗi kênh) đã bị bỏ qua.

Một cặp 18650 mệt có điện trở trong. Khi cả hai motor khởi động, VM sụt. Buck nuôi vi điều khiển sụt theo nếu chúng chung pack. Mạch phát hiện brownout của ESP32 reset chip. Trong lúc reset, các chân motor chưa phải giá trị an toàn của bạn. Firmware đặt PWM về 0 như hành động đầu tiên trong `setup`, và từ chối bật lại cầu cho đến một khoảng trễ đã biết cùng một trạng thái ngõ vào đã biết, sẽ biến brownout thành một cú dừng. Firmware để enable nổi sẽ biến brownout thành một cú lao ngắn xuyên phòng.

## Cầu chì là cuộc nói chuyện với mạch chập

Đặt cầu chì trên dây dương của pin, gần pack, để một mạch chập bất kỳ phía sau đều phải đi qua nó. Cầu chì 2–3 A trên một pack 2S nhỏ là một cuộc nói chuyện để bắt đầu, không phải luật. Nó phải nằm trên dòng chạy bình thường của cả hai motor cộng logic, và nó phải đứt khi chập chết. Nếu mỗi motor TT chạy gần 0,3 A và logic gần 0,2 A, cầu chì 2 A còn dư cho lúc chạy và vẫn sẽ bàn chuyện một lần stall cứng hoặc một dây bị kẹp. Polyfuse chấp nhận được: nó ấm, mở, rồi hồi sau khi nguội. Hãy cho nó thời gian nguội đó. Đừng quấn băng trong một hộp nóng rồi vẫn trông chờ dòng giữ in trên túi.

## Ví dụ tính

Người bán ghi motor 6 V với dòng stall 1,2 A. Điện trở cuộn khoảng

$$
R \approx \frac{6}{1.2} = 5~\Omega
$$

Lúc stall ở điện áp định mức ấy, đồng tiêu tán

$$
P = I^2 R = (1.2)^2 \times 5 = 1.44 \times 5 = 7.2~\mathrm{W}
$$

Bạn kiểm cùng kết quả bằng $$P = I \times V = 1.2 \times 6 = 7.2~\mathrm{W}$$. Bảy watt trong một motor cỡ ngón tay cái là lý do bài thử stall chỉ khoảng một giây rồi thả. Hai motor như vậy stall cùng lúc khoảng 2,4 A trước tổn hao trên dây. Cổng USB ở 0,5 A sẽ brownout hoặc reset board. Đó là lý do Chương 07 dùng pin và cầu chì.

Nếu sau này đồng hồ của bạn chỉ 0,15 A không tải ở một PWM vừa phải, hãy giữ cả hai số. Khoảng cách giữa 0,15 A và 1,2 A là phần dư mà cầu chì và driver phải sống sót khi bánh dừng vào tường.

## Hình

![Dòng stall theo tốc độ: dòng nhỏ khi đang quay, dòng lớn khi trục dừng]({{ site.imgurl }}/generated/stall_current.png)

Đọc phía trái đường cong là số stall trên datasheet, phía phải là dòng không tải bạn được phép đo lâu hơn một giây.

![Đồng hồ mắc nối tiếp hoặc màn hình dòng của nguồn, dùng cho một motor với bánh trên không]({{ site.imgurl }}/wikimedia/Digital_Multimeter_Aka.jpg)

Nếu bạn cắm đồng hồ vào mạch, dùng lỗ dòng lớn, bắt đầu ở PWM 0, và đừng stall motor qua một cầu chì đồng hồ mà bạn không đủ tiền thay. Số đọc dòng của chính nguồn bàn là dụng cụ điềm tĩnh hơn.

## Lab

### An toàn

Bánh trên không, tháo khỏi khung, mỗi lần một motor. Stall một giây chỉ được phép khi giới hạn dòng của nguồn đặt gần 2 A, để một lỗi dây không thành lửa. Nếu bạn không có một giới hạn mình tin, đừng stall: dùng dòng stall của người bán và tính watt. Đừng cầm bánh răng nhỏ đang quay. Đừng nuôi motor từ USB. Mass chung nếu vi điều khiển đang phát PWM.

### BOM

| Món | Vai trò |
|------|------|
| Một motor chổi than | Linh kiện đang thử |
| Nguồn bàn có giới hạn dòng, hoặc pin cộng ampe kế nối tiếp | Nguồn và số đọc |
| Cầu H hoặc dây nguồn trực tiếp | Đặt một điện áp đã biết |
| Đồng hồ vạn năng | Volt, và ampe nếu đó là cách của bạn |
| Sổ | Ampe không tải, và ampe stall hoặc watt đã tính |

### Các bước

1. Đặt giới hạn dòng của nguồn gần 2 A nếu có. Đặt điện áp bằng điện áp định mức của motor, hoặc bằng một giá trị vừa phải mà bạn ghi lại.
2. Chạy motor không tải ở PWM vừa (hoặc thẳng từ nguồn). Ghi điện áp và dòng sau một giây. Đó là không tải ở điện áp ấy.
3. Tùy chọn: stall trục khoảng một giây thôi, đọc dòng, thả. Nếu giới hạn gập ngay, viết “nguồn đã giới hạn” rồi dừng. Đừng lặp.
4. Nếu bạn bỏ qua stall, chép dòng stall của người bán, tính $$R \approx V/I_{stall}$$ và $$P = I^2 R$$, rồi gắn nhãn chúng là ước lượng từ datasheet.
5. Viết một câu về cầu chì bạn sẽ đặt trên dây dương pin cho hai motor này, và vì sao nó nằm trên dòng chạy.

### Kết quả mong đợi

Hai số trong `lab-notes.md`: một dòng không tải đã đo, và hoặc một dòng stall một giây đã đo, hoặc công suất stall đã tính từ số của người bán. Một câu cầu chì có dòng (2 A hoặc 3 A là điểm bắt đầu hợp lý cho robot TT 2S nhỏ) và ước lượng dòng chạy nằm dưới nó.

### Lỗi thường gặp

| Bạn thấy | Cần kiểm |
|--------------|----------------|
| Dòng đọc gần 0 mà trục vẫn quay | Đồng hồ đang mắc song song với motor, hoặc đang ở lỗ điện áp trong khi bạn tưởng đang đo ampe. |
| Điện áp nguồn sụp và MCU reset | USB hoặc một pack tí hon đang nuôi stall. Chuyển sang pin và một giới hạn, bánh trên không. |
| Tản nhiệt L298N nóng không chạm được sau một lần chạy ngắn | Sụt áp nhân dòng là vài watt. Stall ngắn hơn, thêm gió, hoặc đổi TB6612. |
| Polyfuse mở và giữ mở hàng phút | Nó đang làm việc. Để nguội. Đừng nâng điểm cắt cho đến khi mạch chập đã hết. |
| Robot giật sau một lần reset | `setup` chưa ép PWM về 0 và một chiều đã biết trước mọi việc khác. |

## Mua ở Việt Nam / Where to buy in Vietnam

Chỗ còn thiếu là một cầu chì và, nếu bạn vẫn chưa có, một driver cùng một motor TT. Cầu chì lưỡi, cầu chì thủy tinh, hoặc polyfuse gần 2–3 A, cộng một đế bạn hàn hoặc cắm được, là đủ. Giá chạy. Khoảng thô: cầu chì nhỏ và đế khoảng 5.000–25.000 VND, motor TT khoảng 25.000–45.000 VND, module L298N khoảng 35.000–70.000 VND.

- Trang L298N đã kiểm, khoảng 45.000 VND: [hshop.vn/mach-dieu-khien-dong-co-dc-l298](https://hshop.vn/mach-dieu-khien-dong-co-dc-l298)
- HShop: [cầu chì](https://hshop.vn/search?q=cau%20chi), [motor TT](https://hshop.vn/search?q=motor%20TT), [TB6612](https://hshop.vn/search?q=TB6612)
- Shopee: [cầu chì](https://shopee.vn/search?keyword=cau%20chi), [polyfuse](https://shopee.vn/search?keyword=polyfuse), [motor TT](https://shopee.vn/search?keyword=motor%20TT)
- Lazada: [cầu chì](https://www.lazada.vn/catalog/?q=cau%20chi), [motor TT](https://www.lazada.vn/catalog/?q=motor%20TT)
- Thế Giới IC: [cầu chì](https://www.thegioiic.com/search?q=cau%20chi), [L298N](https://www.thegioiic.com/search?q=L298N)

## Bài tập

1. Motor 6 V stall ở 1,2 A. $$R$$ và watt stall là bao nhiêu?
2. Hai motor đó stall cùng lúc. Bạn tính dòng bao nhiêu, và vì sao cổng USB 0,5 A là nguồn sai?
3. Một kênh L298N sụt 2 V khi mang 0,8 A. Kênh đó nóng bao nhiêu watt?
4. Cả hai bánh chạy ở 0,35 A và logic hút 0,15 A. Cầu chì 2 A trên dây dương pin có nằm trên tổng chạy đó không?
5. ESP32 reset khi motor khởi động, rồi robot bò. Bạn đổi gì ở phần cứng và ở các dòng đầu của `setup`?

### Gợi ý đáp án

$$R \approx 5~\Omega$$ và $$P = 7.2~\mathrm{W}$$. Hai motor khoảng 2,4 A lúc stall, cao hơn nhiều cổng USB 0,5 A, nên Chương 07 dùng pin và cầu chì. Một kênh L298N ở 2 V và 0,8 A nóng khoảng 1,6 W. Tổng chạy là $$0.35 + 0.35 + 0.15 = 0.85~\mathrm{A}$$, nên cầu chì 2 A nằm trên mức chạy bình thường. Phần cứng cần một pack cứng hơn và một cầu chì; `setup` phải kéo PWM về 0 và một chiều an toàn trước khi cầu được phép cử động.

## Đọc thêm

- SparkFun, motor và con số dòng stall: [https://learn.sparkfun.com/tutorials/motors-and-selecting-the-right-one/all](https://learn.sparkfun.com/tutorials/motors-and-selecting-the-right-one/all)
- Datasheet ST L298, về sụt áp thành nhiệt: [https://www.st.com/resource/en/datasheet/l298.pdf](https://www.st.com/resource/en/datasheet/l298.pdf)
- Mạch mang TB6612FNG của Pololu, một cầu mát hơn ở dòng TT: [https://www.pololu.com/product/713](https://www.pololu.com/product/713)
