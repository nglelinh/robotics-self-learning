---
layout: post
title: "Lắp khung, motor và nguồn"
chapter: "07"
order: 1
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter07
lesson_type: required
draft: false
---

Bài này biến khung thành robot, nhưng bánh chưa được phép quay bằng PWM. Bạn bắt motor, đặt caster, buộc pin, rồi đo cây nguồn trước khi bất kỳ sketch nào được chạm vào bánh.

## Mục tiêu học

1. Gắn hai motor TT sao cho lốp không cà tấm mica, caster có vết tiếp xúc nằm sau chốt xoay, và pin được buộc để trọng tâm nằm giữa trục bánh và caster.
2. Đi cực dương ắc quy qua công tắc rồi cầu chì 2–3 A, tách ra VM của driver và đầu vào LM2596; chỉnh buck về 5,0 V trước khi cắm ESP32.
3. Nối cực âm pin, GND driver, GND buck và GND MCU thành một nút, và giữ dòng motor trên vít của driver.
4. Ghi điện áp pin không tải và điện áp buck vào `lab-notes.md`, kèm ảnh đi dây, và không lấy USB làm nguồn motor.

## Kiến thức cần có

Chương 04 đã nói cảm biến và vi điều khiển phải chung đất. Chương 05 là cầu H: TB6612 ngủ khi STBY thấp, và 7805 trên mạch L298N không phải nguồn cho ESP32. Chương 06 để lại hai kích thước, bề rộng $$b$$ giữa hai vết tiếp xúc lốp và bán kính lăn $$r$$ từ một vòng đẩy trên giấy. Bàn thí nghiệm mẫu của khóa này có $$b = 0{,}15~\mathrm{m}$$ và $$r = 31{,}2~\mathrm{mm}$$. Chép hai số ấy vào ghi chú hôm nay; bài này chưa dùng chúng để chạy. Bạn đọc được điện áp một chiều. Chưa có node ROS và chưa có PWM.

## Vì sao bài này quan trọng với Capstone A và ROS

Chương này chưa đụng ROS 2. Sau này một `geometry_msgs/Twist` mang `linear.x` là tốc độ tiến và `angular.z` là tốc độ quay, rồi một node tách twist thành hai lệnh bánh. Việc tách ấy vô nghĩa nếu mũi xe nhấc lên, buck chưa được chỉnh, hoặc MCU reset khi motor vừa khởi động. Bài 03 và 04 dùng một dòng chữ thay cho twist đó. Một bản tin Twist không buộc được pin.

## Trọng tâm phải nằm giữa trục và caster

Lốp không được cà mica. Lốp cà tấm là stall, và chương 05 đã tính stall thành nhiệt. Caster nằm dưới mũi, trục xoay thẳng đứng, vết lốp nằm sau chốt. Càng lắp ngược sẽ rung.

Buộc pin. Pin trượt là khối lượng di động và là chỗ chờ chập. Nhìn từ cạnh, trọng tâm phải nằm giữa trục bánh chủ động và điểm chạm của caster. Trọng tâm phía sau trục thì mũi nhấc, và lệnh đi thẳng sau này trông như xe tự quay.

Lấy trục làm $$x = 0$$, điểm chạm caster là $$x = +90~\mathrm{mm}$$ về phía mũi. Tấm và motor $$220~\mathrm{g}$$, tâm riêng của chúng ở $$x = +15~\mathrm{mm}$$, pin $$90~\mathrm{g}$$. Tâm chung là

$$
x_{cg} = \frac{220 \times 15 + 90 \times x_b}{310}.
$$

Buộc pin phía sau trục, $$x_b = -40~\mathrm{mm}$$:

$$
x_{cg} = \frac{3300 - 3600}{310} \approx -1{,}0~\mathrm{mm}.
$$

Khối lượng đã vượt qua trục. Caster mất tải và mũi nhấc ngay khi xe tăng tốc. Buộc cùng cục pin giữa trục và caster, $$x_b = +35~\mathrm{mm}$$:

$$
x_{cg} = \frac{3300 + 3150}{310} \approx 20{,}8~\mathrm{mm},
$$

nằm giữa $$0$$ và $$90~\mathrm{mm}$$. Caster chịu khoảng $$(20{,}8/90)\times 310~\mathrm{g} \approx 72~\mathrm{g}$$. Mũi giữ trên sàn, trục vẫn chịu phần lớn trọng lượng. Ghi $$x_b$$ của bạn cạnh $$b$$ và $$r$$.

![Bề rộng $$b$$ và caster phải còn tải]({{ site.imgurl }}/generated/chassis_measures.png)

## Cây nguồn, đo trước khi gắn MCU

Dòng motor và dòng logic chung pin và chung đất. Chúng không chung một IC ổn áp, và không đi qua hàng lỗ breadboard.

![Pin, cầu chì, VM, và buck chỉnh 5,0 V trước khi cắm MCU]({{ site.imgurl }}/generated/power_tree.png)

Cực dương pin đi tới công tắc, rồi cầu chì 2–3 A, rồi tách thành VM của driver và đầu vào LM2596. Cực âm pin, GND driver, GND buck và GND MCU là một nút. Dây motor đi từ vít driver tới cực motor, không xuyên breadboard: tiếp xúc breadboard chỉ chịu vài trăm miliampe, còn stall là cấp ampe.

Chỉnh buck khi chưa cắm vi điều khiển. Pin 2S mới thường đo khoảng $$8{,}2~\mathrm{V}$$ không tải (cửa sổ khoảng $$7{,}4$$–$$8{,}4~\mathrm{V}$$). Vặn chiết áp đến khi ra $$5{,}0~\mathrm{V}$$; $$5{,}02~\mathrm{V}$$ để hở là số cần có. Sau đó mới đưa chân ấy cho ESP32, hoặc để ESP32 ăn USB lúc nạp và vẫn chung đất. Không đưa VM vào chân 5 V hoặc 3,3 V. Không nuôi motor bằng USB: một cổng khoảng $$500~\mathrm{mA}$$, còn hai motor TT stall cỡ $$2{,}4~\mathrm{A}$$.

Trên L298N, jumper 5 V bật 7805 lấy điện từ VM. Với pin 2S, cách đó tạm được cho logic nhỏ của chính con chip, và là nguồn tệ cho ESP32 khi Wi-Fi phát. Hãy dùng buck. Nếu VM trên $$12~\mathrm{V}$$, rút jumper. Thử nhiệt ở đỉnh 2S, giả sử $$0{,}25~\mathrm{A}$$ qua 7805:

$$
P \approx (8{,}4 - 5{,}0) \times 0{,}25 = 0{,}85~\mathrm{W}
$$

trên một IC nhỏ. Ở $$12~\mathrm{V}$$ cùng dòng ấy là $$1{,}75~\mathrm{W}$$. ESP32 ăn buck trong cả hai trường hợp.

Pin lithium nằm trong đế hoặc trong pack đã có BMS. Không để đầu dây hàn trần lòng thòng. Sạc bằng cục đúng số cell, và ngồi cạnh. TP4056 chỉ dành cho 1S, đầy gần $$4{,}2~\mathrm{V}$$. Một TP4056 trên pack 2S không tạo ra $$8{,}4~\mathrm{V}$$ và không cân bằng hai cell.

## Lab

### An toàn

Bài này không có PWM, nên lốp được đặt trên bàn. Ngắt pin cho đến khi cầu chì, công tắc và các đất đã vào chỗ. Lithium ở trong đế hoặc pack có BMS. Sạc bằng sạc đúng loại, có người trông. Không mắc một TP4056 ngang pack 2S. Buck có mùi thì ngắt công tắc.

### BOM

| Món | Việc |
|------|------|
| Khung 2WD, hai motor TT, lốp, caster | Phần cơ chương 06 |
| Pack 2S hoặc đế 18650 có BMS | Nguồn motor và logic |
| Công tắc, đế cầu chì, chì 2–3 A | Nhánh dương |
| TB6612 (nên dùng) hoặc L298N | Chỉ cấp VM; hôm nay chưa ra lệnh |
| Buck LM2596 | Logic 5,0 V, chỉnh trước MCU |
| ESP32 devkit | Gắn sau khi buck đã 5,0 V |
| Đồng hồ, dây buộc, `lab-notes.md` | Số đo |

### Các bước

1. Bắt hai motor. Quay tay từng lốp cho khỏi cà tấm.
2. Gắn caster sao cho vết lốp nằm sau chốt. Chép $$b$$ và $$r$$ vào ghi chú.
3. Buộc pin giữa trục và caster. Ước lượng $$x_{cg}$$ và ghi số milimét.
4. Đi cực dương qua công tắc, cầu chì, rồi VM và đầu vào buck. Nối bốn đất. Dây motor chỉ ở vít driver.
5. Chưa cắm MCU, bật pin. Đo điện áp pack và đầu ra buck, chỉnh buck về $$5{,}0~\mathrm{V}$$, chụp ảnh đi dây, rồi mới gắn ESP32 vào rail 5 V ấy hoặc vào USB.

### Kết quả mong đợi

`lab-notes.md` có ngày, điện áp pack không tải (ví dụ 2S khỏe là $$8{,}15~\mathrm{V}$$), đầu ra buck lệch vài chục milivolt quanh $$5{,}0~\mathrm{V}$$ trước khi gắn MCU, $$b$$ và $$r$$, và một câu rằng dây motor không vào breadboard. Ảnh thấy công tắc, cầu chì, dây buộc và đất chung. Chưa có bánh nào bị ra lệnh.

### Lỗi thường gặp

| Bạn thấy | Thường là |
|----------|-----------|
| Mũi nhấc khi đặt xe xuống | Pin nằm sau trục; dịch về phía caster |
| Lốp cà mica | Sai đệm; sau này thành stall |
| Buck ra 8 V hoặc 12 V | Chiết áp còn ở đầu; đừng cắm ESP32 |
| ESP32 reset khi chạm VM | Logic đang ăn 7805, hoặc đất chưa thành một nút |
| Với tay lấy TP4056 | Mạch ấy là 1S; pack 2S cần sạc 2S và BMS |

## Mua ở Việt Nam / Where to buy in Vietnam

Mua phần còn thiếu, đừng mua thêm một con robot. Giá đổi. Khoảng năm 2026: khung mica 2WD 60.000–150.000 đồng, motor TT 25.000–45.000 đồng một cái, module TB6612 25.000–70.000, buck LM2596 10.000–25.000, pack 2S hoặc đế 18650 80.000–180.000, công tắc 8.000–20.000, đế chì kèm chì 2–3 A 10.000–25.000, ESP32 devkit 70.000–150.000. L298N đã kiểm trang khoảng 45.000 đồng nếu hết TB6612; TB6612 mát hơn, và buck vẫn nuôi ESP32. Đế 1S không thay pack 2S.

- L298N đã kiểm, khoảng 45.000 đồng: [hshop.vn/mach-dieu-khien-dong-co-dc-l298](https://hshop.vn/mach-dieu-khien-dong-co-dc-l298)
- [Hshop khung](https://hshop.vn/search?q=khung+xe+2wd), [buck](https://hshop.vn/search?q=LM2596), [ESP32](https://hshop.vn/search?q=ESP32)
- [Shopee khung 2WD](https://shopee.vn/search?keyword=khung%20xe%202WD%20acrylic), [LM2596](https://shopee.vn/search?keyword=LM2596), [cầu chì](https://shopee.vn/search?keyword=c%E1%BA%A7u%20ch%C3%AC%202A)
- [Lazada ESP32](https://www.lazada.vn/catalog/?q=ESP32), [pin 18650](https://www.lazada.vn/catalog/?q=pin%2018650%202S)
- [Thế Giới IC LM2596](https://www.thegioiic.com/search?q=LM2596), [ESP32](https://www.thegioiic.com/search?q=ESP32)

## Bài tập

1. Tấm và motor $$220~\mathrm{g}$$ tại $$x = +15~\mathrm{mm}$$, pin $$90~\mathrm{g}$$ tại $$x_b = -20~\mathrm{mm}$$, caster tại $$+90~\mathrm{mm}$$. Tính $$x_{cg}$$. Mũi có giữ xuống không?
2. Buck không tải $$5{,}02~\mathrm{V}$$. Gắn ESP32 thì chân ấy còn $$4{,}15~\mathrm{V}$$. Kiểm gì trước khi kết luận board hỏng?
3. Bạn học mắc một TP4056 ngang pack 2S để sạc bằng USB. Sai ở số cell, và sạc nào mới đúng?
4. VM $$8{,}4~\mathrm{V}$$, jumper 5 V của L298N còn cắm. Ước lượng nhiệt 7805 ở $$0{,}25~\mathrm{A}$$. Vì sao ESP32 vẫn phải ăn buck?
5. Hai dây motor cắm qua breadboard rồi mới tới driver. Cầu chì nằm sau buck thay vì trên cực dương pin. Viết lại đường pin, công tắc, chì, tải, và nói breadboard không chịu được gì.

### Gợi ý đáp án

1. $$x_{cg} = (3300 - 1800)/310 \approx 4{,}8~\mathrm{mm}$$, vẫn giữa trục và caster nên mũi chưa nhấc, nhưng caster nhẹ. Nếu caster kêu, dịch pin về khoảng $$+35~\mathrm{mm}$$. 2. Kiểm đất chung, kiểm USB và buck không cùng đút vào chân 5 V, và tìm dây mỏng hoặc buck sụt khi có tải. Đừng vặn chiết áp khi MCU đang gắn. 3. TP4056 là 1S, đầy gần $$4{,}2~\mathrm{V}$$. Pack 2S đầy gần $$8{,}4~\mathrm{V}$$, cần sạc 2S và BMS. 4. $$P \approx (8{,}4-5)\times 0{,}25 = 0{,}85~\mathrm{W}$$. Wi-Fi đòi hơn 0,25 A yên lặng và 7805 sụt. Jumper có thể nuôi logic của chính L298N trên 2S; ESP32 ở trên buck. Trên $$12~\mathrm{V}$$ thì rút jumper. 5. Cực dương, công tắc, chì 2–3 A, rồi VM và đầu vào buck. Dòng motor ở vít. Chì đặt sau buck không bảo vệ chập trên VM.

## Đọc thêm

- [Datasheet L298 của ST](https://www.st.com/resource/en/datasheet/l298.pdf)
- [Mạch Pololu TB6612FNG](https://www.pololu.com/product/713)
- [geometry_msgs/Twist (Jazzy)](https://docs.ros.org/en/jazzy/p/geometry_msgs/interfaces/msg/Twist.html)
- [Arduino `Serial`](https://www.arduino.cc/reference/en/language/functions/communication/serial/)
