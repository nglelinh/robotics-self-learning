---
layout: post
title: "Lab: bring-up driver và test quay"
chapter: "07"
order: 2
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter07
lesson_type: required
draft: false
---

Buck đã ở 5,0 V. Đây là lần đầu bánh được quay bằng điện: xe kê lên, từng motor một, cho đến khi PWM dương làm cả hai lốp lăn về phía mũi.

## Mục tiêu học

1. Kê robot lên hộp cho cả hai lốp rời mặt bàn, và quay từng motor với PWM giữ trong 60–80 nấc trên 255.
2. Kéo STBY của TB6612 lên cao trước khi đổ lỗi cho sketch, rồi ghi cặp chân IN làm bánh trái tiến và cặp làm bánh phải tiến.
3. Bánh quay ngược thì đảo hai dây motor đó, hoặc đánh dấu sẽ đảo dấu trong firmware, và không làm cả hai.
4. Đo dòng không tải, stall chỉ trong một giây, và dừng nếu driver có mùi hoặc không chạm được vào lá tản nhiệt.

## Kiến thức cần có

Bài 07-01 để lại đất chung, cầu chì trên cực dương, và buck 5,0 V đã đo trước khi gắn ESP32. Chương 05 là bảng sự thật của cầu H: một cặp tiến, một cặp lùi, và cả hai khóa trên một nhánh là chập. Bạn nhận được TB6612 (STBY, PWMA, PWMB, AIN, BIN) hoặc L298N (ENA, ENB, INx, tản nhiệt, jumper 5 V). Chương 06 cho $$b$$, $$r$$, và định nghĩa tiến là hướng mũi. Yaw dương ở chương ấy là bánh phải nhanh hơn bánh trái. Dấu bạn tìm hôm nay là dấu mà PID chương 08 và topic chương 09 sẽ kế thừa. Lab này không có node ROS.

## Vì sao bài này quan trọng với Capstone A và ROS

`geometry_msgs/Twist` sau này có `linear.x` là tiến và `angular.z` là yaw. Hai trường ấy thành lệnh trái và lệnh phải. Nếu "dương" của bánh phải trên thực tế là lùi, mọi `linear.x` dương thành vòng quay, và PID chương 08 sẽ cố triệt một lỗi đi dây. Tìm dấu ở đây, bánh trên không, nơi lốp ngược không kéo được robot khỏi bàn. Bài 03 chỉ đặt tên cho hai số. Chúng chưa phải mét trên giây.

## Một kênh, duty nhỏ, STBY phải thức

Kê khung lên hộp hoặc chồng sách. Cả hai lốp ở trên không. Lốp còn trên bàn ở PWM đầu tiên là cách robot rời mặt bàn.

Ra lệnh một motor. Motor kia PWM 0. Duty đầu là 60, 70, hoặc cùng lắm 80 trên 255, không phải 255. Pack đang $$7{,}6~\mathrm{V}$$:

$$
D = \frac{70}{255} \approx 0{,}275, \qquad V_{avg} \approx 0{,}275 \times 7{,}6~\mathrm{V} \approx 2{,}09~\mathrm{V}
$$

trước sụt áp cầu. TB6612 là cầu MOSFET, đưa gần hết 2 V ấy tới chổi than, nên lốp quay chậm và bạn thấy hướng. L298N có thể sụt $$1{,}5$$–$$2~\mathrm{V}$$ và cùng duty chỉ bò; đó là lý do chọn TB6612, không phải lý do mở full thang. Nếu L298N buộc phải tăng duty mới thấy chuyển động, tăng từng nấc nhỏ và giữ luật stall bên dưới.

Trên TB6612, STBY phải cao, nếu không cả hai cầu ngủ dù IN và PWM có nói gì. STBY nổi là lỗi quen "sketch đúng mà bánh đứng im". Nối nó lên VCC cho lab này, hoặc để GPIO kéo cao ở bài 04. Trên L298N, bẫy tương ứng là ENA hoặc ENB còn thấp, hoặc jumper 5 V đã rút mà chân logic không có 5 V nào khác.

![Tiến là một đường chéo của chữ H; đường kia là lùi]({{ site.imgurl }}/generated/hbridge_concept.png)

![Module L298N: vít motor, tản nhiệt trên cặp Darlington]({{ site.imgurl }}/wikimedia/Dosmotorsl298n.jpg)

Nhìn lốp trái so với mũi xe. Ghi cặp IN làm nó tiến, rồi làm bánh phải, vẫn một mình. Ví dụ bạn phải thay bằng số của mình: trái tiến là AIN1 cao, AIN2 thấp, PWMA 70; phải tiến là BIN1 cao, BIN2 thấp, PWMB 70. Bánh phải lùi với mẫu ấy thì đảo hai vít của motor đó một lần, hoặc giữ vít và đảo dấu phải trong firmware bài 04. Không làm cả hai. Hai lần đảo triệt nhau, và lệnh thẳng ở bài 05 thành vòng quay.

## Dòng không tải, và stall không được giữ

Một lốp trên không ở PWM 70, motor TT vàng thường hút cỡ $$0{,}10$$–$$0{,}20~\mathrm{A}$$. Ghi số đồng hồ của bạn, nối tiếp motor đó hoặc ở dây pin khi motor kia tắt. Hai motor sau này cộng lại. Chúng không nhân dòng stall vào số không tải.

![Dòng không tải là đầu thấp của đường cong; stall là đầu cao]({{ site.imgurl }}/generated/stall_current.png)

Nếu cần một điểm stall, kẹp lốp một giây, đọc đồng hồ, rồi thả. Stall người bán ghi $$1{,}2~\mathrm{A}$$ tại $$6~\mathrm{V}$$ là bậc độ lớn, không phải giá trị để giữ. Ở PWM 70, dòng stall thấp hơn stall đủ điện áp, và vẫn nóng cuộn dây lẫn lá tản. Có mùi, hoặc không đặt ngón lên lá L298N hay thân TB6612, thì ngắt công tắc. Câu cho bài sau: với bảng IN của bạn, PWM dương làm cả hai lốp tiến, PWM âm đảo chiều, PWM 0 là dừng. Đó là bảng dấu.

## Lab

### An toàn

Lốp rời mặt bàn. Lần quay đầu chỉ một motor. PWM nằm trong 60–80 trên 255 cho đến khi hướng rõ. Công tắc pin là nút giết, và tay với tới được. Đo stall một giây. Lá nóng hoặc có mùi thì kết thúc. Dòng motor vẫn từ pin có chì, không từ USB. Ngón tay tránh bánh răng.

### BOM

| Món | Việc |
|------|------|
| Robot bài 07-01 | Cây nguồn đã đo |
| TB6612 hoặc L298N | Cầu đang thử |
| ESP32 hoặc ba sợi dây | STBY hoặc ENA cao, cặp IN, PWM |
| Ampe kế | Không tải, và stall một giây nếu đo |
| Băng dính trên mỗi lốp | Hướng nhìn từ mũi |
| `lab-notes.md` | Bảng dấu |

### Các bước

1. Hộp dưới khung. Cả hai lốp không chạm hộp và không chạm bàn.
2. STBY cao trên TB6612, hoặc ENA/ENB sẵn trên L298N. PWM 0. Bật pin.
3. Chỉ motor trái. PWM 70. Thử hai cách IN không phải cả hai cao. Ghi cặp nào làm lốp lăn về mũi.
4. Lặp cho motor phải. Bánh ngược thì đảo hai vít motor đó, hoặc ghi "đảo trong firmware", không cả hai.
5. Đo dòng không tải ở PWM 70 từng motor. Tùy chọn: stall một giây rồi thả. Viết "PWM dương → cả hai bánh tiến" bằng tên chân của bạn.

### Kết quả mong đợi

Một bảng dấu có mức chân, dòng không tải từng motor (dạng ví dụ: trái $$0{,}12~\mathrm{A}$$, phải $$0{,}15~\mathrm{A}$$ tại PWM 70 — số của bạn sẽ khác), và một dòng nói STBY hoặc enable đã cao. Cả hai mảnh băng, nhìn từ đuôi xe, đi về phía mũi khi lệnh dương. Ghi chú không được nói đã sửa bằng cách vừa đảo dây vừa đảo code.

### Lỗi thường gặp

| Bạn thấy | Thường là |
|----------|-----------|
| Cả hai motor chết, code trông đúng | STBY thấp hoặc nổi; ENA/ENB thấp trên L298N |
| Chỉ một motor quay | Chân PWM, cặp IN, hoặc vít kênh đó hở |
| Lốp quay rồi driver có mùi | Duty quá cao hoặc giữ stall quá lâu; ngắt nguồn |
| Trái tiến, phải lùi, cùng mẫu IN | Đảo dây motor phải hoặc dấu firmware, một lần |
| Dòng gần stall dù lốp "tự do" | Lốp cà tấm, hoặc hộp số kẹt |

## Mua ở Việt Nam / Where to buy in Vietnam

Bạn đáng lẽ đã có driver. Nếu bài 07-01 còn motor mà chưa có cầu, mua TB6612 trước. L298N dùng tạm được và nóng hơn; giữ tản nhiệt, và ESP32 vẫn ăn buck. Giá đổi. Khoảng 2026: module TB6612 25.000–70.000 đồng, motor TT 25.000–45.000 một cái, L298N khoảng 45.000 trên trang đã kiểm bên dưới. DRV8833 hợp motor nhỏ hơn nhiều, yếu nếu cặp TT bị stall.

- L298N đã kiểm, khoảng 45.000 đồng: [hshop.vn/mach-dieu-khien-dong-co-dc-l298](https://hshop.vn/mach-dieu-khien-dong-co-dc-l298)
- [Hshop TB6612](https://hshop.vn/search?q=TB6612), [motor TT](https://hshop.vn/search?q=motor%20TT)
- [Shopee TB6612](https://shopee.vn/search?keyword=TB6612), [motor TT](https://shopee.vn/search?keyword=motor%20TT)
- [Lazada TB6612](https://www.lazada.vn/catalog/?q=TB6612), [L298N](https://www.lazada.vn/catalog/?q=L298N)
- [Thế Giới IC TB6612](https://www.thegioiic.com/search?q=TB6612), [L298N](https://www.thegioiic.com/search?q=L298N)

## Bài tập

1. VM $$8{,}0~\mathrm{V}$$, lệnh đầu 80 nấc trên 255. Tính $$D$$ và $$V_{avg}$$ trước sụt cầu. Nếu L298N sụt thêm $$1{,}8~\mathrm{V}$$, chổi than còn bao nhiêu?
2. Không tải ở PWM 70 là $$0{,}14~\mathrm{A}$$. Kẹp một giây được $$0{,}95~\mathrm{A}$$. Vì sao cả hai số hợp đường stall, và vì sao phải thả?
3. STBY nổi, AIN1 cao, AIN2 thấp, PWM 80. Lốp vẫn đứng. Sợi dây đầu tiên cần thêm là gì?
4. Bánh phải quay ngược. Bạn đảo dây của nó và còn nhân lệnh phải với $$-1$$ trong sketch sắp viết. PWM dương trên sàn sẽ làm gì?
5. Trái tiến là AIN1 = 1, AIN2 = 0. Phải tiến, trước khi sửa, là BIN1 = 0, BIN2 = 1. Viết câu bảng dấu mà bài 04 phải làm, không đảo thêm lần nữa.

### Gợi ý đáp án

1. $$D = 80/255 \approx 0{,}314$$, $$V_{avg} \approx 0{,}314 \times 8{,}0 \approx 2{,}51~\mathrm{V}$$. Sau sụt $$1{,}8~\mathrm{V}$$, chổi than còn khoảng $$0{,}7~\mathrm{V}$$, có thể không thắng ma sát. Đó là lý do TB6612, không phải lý do mở 255. 2. Không tải là đầu dòng thấp, sức phản điện gần triệt nguồn. Kẹp lốp làm sức phản điện sụp và dòng tiến về stall. Một giây rồi thả; lá nóng hoặc có mùi thì dừng hẳn. 3. Kéo STBY lên cao. Chân ấy chưa cao thì TB6612 ngủ, cặp IN không có tiếng nói. 4. Hai lần đảo triệt nhau. PWM dương vẫn làm lốp ấy lùi, sổ nói đã "sửa", và lệnh thẳng thành vòng quay. Chỉ làm một trong hai cách. 5. Lệnh trái dương: AIN1 cao, AIN2 thấp. Lệnh phải dương: BIN1 thấp, BIN2 cao. Âm thì đảo từng cặp. Không đảo thêm vít bên phải.

## Đọc thêm

- [Pololu TB6612FNG](https://www.pololu.com/product/713)
- [Datasheet L298 của ST](https://www.st.com/resource/en/datasheet/l298.pdf)
- [geometry_msgs/Twist (Jazzy)](https://docs.ros.org/en/jazzy/p/geometry_msgs/interfaces/msg/Twist.html)
- [Arduino `Serial`](https://www.arduino.cc/reference/en/language/functions/communication/serial/)
