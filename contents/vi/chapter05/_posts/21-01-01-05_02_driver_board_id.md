---
layout: post
title: "Nhận diện driver: L298N, TB6612, DRV8833"
chapter: "05"
order: 2
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter05
lesson_type: required
draft: false
---

Chữ in trên module đỏ là một phần của mạch. Trước khi tin sơ đồ chân trong tutorial, bạn phải gọi tên con chip thực sự được hàn trên board, vì L298N, TB6612 và DRV8833 không đồng ý với nhau về sụt áp, nguồn logic, chân chờ, và dòng stall mà một motor TT được phép đòi. Bài này dạy bạn đặt tên cho tấm mạch đang cầm, và đo các ray của nó trước khi bất kỳ chân vi điều khiển nào chạm vào.

## Mục tiêu học

Hết bài, bạn nhận ra module L298N, module TB6612 và breakout DRV8833 từ thân chip, tấm tản nhiệt, và tên chân. Bạn nói được jumper 5 V của L298N làm gì, khi nào phải tháo, và vì sao ổn áp đó là nguồn tồi cho radio ESP32. Bạn giải thích vì sao STBY trên TB6612 phải được kéo lên cao, và vì sao DRV8833 là linh kiện motor nhỏ trên pack 1S–2S dưới 10 V. Bạn đo VM và ray logic bằng đồng hồ trước khi nối GPIO, và ghi mọi cổng vít vào sổ lab.

## Kiến thức cần có

Bạn dùng được thang điện áp một chiều của đồng hồ và biết que đen là que nào. Từ vựng cầu H của bài 05-01 — đường tiến, đường lùi, bắn chéo (shoot-through), PWM trên enable — là tấm bản đồ bạn đang khớp với một board thật. Bạn cũng đã biết dòng motor không lấy từ USB.

## Vì sao bài này quan trọng với Capstone A và ROS

Capstone A lăn trên hai motor hộp số TT vàng, ăn pack 2S. Driver dưới hai motor ấy quyết định bao nhiêu volt của pin tới được chổi than, và một chân bị quên có để cả hai bánh ngủ hay không. PWM trái và phải có dấu ở Chương 07 giả định một cầu đang sống, với bảng chân lý đã biết. ROS 2 không sửa được một ổn áp sụt khi Wi-Fi phát: vi điều khiển reset, giá trị PWM cuối hoặc một ngõ vào nổi còn đó, và khung xe có thể bò. Chọn TB6612 làm mặc định, và biết cách sống an toàn với L298N nếu cửa hàng bán cho bạn con đó, là một phần của việc làm cho `cmd_vel` có nghĩa là chuyển động bạn định.

## Trên bàn đang có gì

Module L298N là tấm đỏ hoặc xanh khá cục, có tản nhiệt kim loại bắt vít trên vỏ DIP lớn, và một jumper nhỏ gần ổn áp 5 V. Cổng vít nhận VM, GND, và hai motor. Hàng logic thường là IN1, IN2, ENA, IN3, IN4, ENB, thêm một chân 5 V.

Module TB6612 nhỏ hơn. Toshiba TB6612FNG là cầu MOSFET. Những chân bạn phải chỉ được là VM, VCC, GND, AIN1, AIN2, PWMA, BIN1, BIN2, PWMB, và STBY. Hai motor chung một chip. Thường không có tản nhiệt bắt vít lớn, vì sụt áp nhỏ hơn nhiều so với Darlington.

Breakout DRV8833 thì tí hon. TI DRV8833 là cầu kép, nguồn motor khoảng 2,7–10,6 V. Nhiều board hobby chạy chế độ IN/IN, trong đó hai ngõ vào của một kênh mã hóa cả hướng lẫn PWM. Bạn hiếm khi thấy tản nhiệt lớn. Linh kiện này thoải mái với motor nhỏ và với pack 1S hoặc 2S còn dưới 10 V. Một cặp motor TT lúc stall đòi dòng nhiều hơn cái cầu nhỏ này vui lòng giữ.

## L298N và jumper 5 V

Tầng ra của L298N là Darlington lưỡng cực. Khi có dòng, cầu sụt khoảng 2 V, và tích của sụt áp với dòng thành nhiệt trong chip. Tản nhiệt bắt vít đang làm việc thật. Logic trên module này là thế giới 5 V: chân nguồn logic của chip muốn khoảng 5 V.

Con 7805 onboard, khi jumper còn cắm, lấy đầu vào từ nguồn motor và tạo ra 5 V đó. Nếu nguồn motor trên 12 V, ổn áp tiêu tán quá nhiều và chín. Trường hợp ấy phải rút jumper và cấp 5 V từ một ổn áp riêng. Ngay cả ở 12 V trở xuống, đừng nuôi radio Wi-Fi của ESP32 từ con 7805 đó. Các cú bùng dòng của radio làm ổn áp nhỏ sụt, ESP32 brownout, robot khởi động lại giữa lệnh. Dùng một buck riêng cho logic, và giữ mass chung với VM.

GPIO 3,3 V thường đủ để ngõ vào L298 coi là mức cao, vì ngưỡng mức cao của ngõ vào khoảng 2,3 V, miễn là chính chân nguồn logic là 5 V chắc, và mass đã chung. Jumper và chân 5 V là để nuôi logic của chip, không phải để “mượn 5 V cho cả con robot”.

## TB6612, mặc định của Capstone

TB6612FNG dùng MOSFET, nên điện áp còn lại cho motor gần VM hơn nhiều so với L298N. VCC, nguồn logic, nhận khoảng 2,7–5,5 V, nghĩa là ESP32 3,3 V có thể nuôi thẳng chân logic. VM có thể lên khoảng 15 V; ở trong khoảng board của bạn ghi, và pack 2S gần 7,4–8,4 V là mức dễ chịu. Dòng liên tục khoảng 1,2 A mỗi kênh, là ngân sách công bằng cho một motor TT nếu bạn tôn trọng thời gian stall.

STBY phải được kéo lên cao, nếu không các cầu ngủ. Chân STBY nổi là lỗi kinh điển “code hoàn hảo mà bánh chết”. Nối nó vào VCC nếu bạn muốn chip thức bất cứ khi nào có nguồn logic, hoặc kéo từ một GPIO mà bạn đặt cao trong `setup` và hạ khi muốn trôi bằng phần cứng. PWMA và PWMB nhận các nhát băm tốc độ. AIN1 và AIN2, cùng cặp B, nhận hướng. Đọc bảng của Pololu hoặc Toshiba, rồi xác nhận trôi so với hãm trên bàn như bài 05-01.

## DRV8833 và những board quá nhỏ

DRV8833 là cầu kép tốt cho một cơ cấu nhỏ, một robot tí hon trên 1S, hoặc một thí nghiệm 2S mà motor stall thấp hơn nhiều so với cặp TT đòi. Nhiều breakout đưa ra IN1/IN2 và IN3/IN4, và chờ bạn PWM một ngõ vào trong khi giữ ngõ kia. Thường có một chân sleep phải được giữ ở trạng thái thức, cùng tinh thần với STBY. Nếu motor duy nhất của bạn là cặp TT của Capstone, hãy chọn TB6612.

MX1508 và L9110 xuất hiện trong cùng kết quả tìm kiếm. Chúng ổn cho một motor rất nhỏ trên bàn demo. Chúng là cầu sai cho robot TT trên 2S: cả dòng lẫn khối nhiệt đều quá nhỏ, và một lần stall thành một vỏ chip chảy. Nếu ngăn kéo chỉ có board đó, dùng nó để học tên chân trên motor tí hon, rồi mua TB6612 trước khi dựng khung.

## Ví dụ tính

Giả sử nguồn motor là 12 V và jumper L298N vẫn cắm, nên 7805 sụt $$12 - 5 = 7~\mathrm{V}$$. Lấy $$0.20~\mathrm{A}$$ làm số tròn cho một radio ESP32 đang bận (một cú bùng Wi-Fi thật có thể cao hơn).

$$
P_{7805} \approx (12 - 5) \times 0.20 = 1.4~\mathrm{W}
$$

Nhiệt đó nằm trong một ổn áp nhỏ gần như không có đồng. Ray 5 V sụt, vi điều khiển reset, và bất kỳ PWM nào tình cờ đang bật trở thành một bất ngờ. Trên 12 V tích ấy còn tệ hơn, đó là lý do jumper phải rút. Cùng 1 A qua một kênh L298N sụt khoảng 2 V thì đặt khoảng $$2~\mathrm{W}$$ vào chip Darlington, đó là lý do tản nhiệt bắt vít không phải đồ trang trí. TB6612 trên 2S tránh cả hai lò sưởi này cho motor Capstone.

## Hình

![Module cầu H kép L298N với tản nhiệt bắt vít]({{ site.imgurl }}/wikimedia/Dosmotorsl298n.jpg)

Tìm vỏ lớn dưới tấm kim loại, cổng vít cho motor và VM, và jumper cấp cho ổn áp onboard. Nếu board của bạn khớp hình này, hãy coi nó là L298N cho đến khi ký hiệu trên chip nói khác.

![Đồng hồ số dùng để đo VM và ray logic trước khi nối bất kỳ GPIO nào]({{ site.imgurl }}/wikimedia/Digital_Multimeter_Aka.jpg)

Đen trên mass driver, đỏ trên VM, rồi đỏ trên chân logic 5 V hoặc 3,3 V. Ghi số xuống. Một chân đã ở điện áp pin không phải là đích của GPIO.

## Lab

### An toàn

Tắt nguồn motor khi dò thông mạch. Khi đo VM, dùng thang volt, bắt đầu bằng một tay, và đừng để que trượt từ VM sang chân logic. Đừng nối chân ESP32 cho đến khi cả hai ray đã biết. Bánh ở trên không nếu đã gắn motor.

### BOM

| Món | Vai trò |
|------|------|
| Module driver bạn thực sự có | Đối tượng cần nhận diện |
| Đồng hồ vạn năng | Điện áp một chiều, rồi thông mạch nếu muốn |
| Điện thoại | Một ảnh đã gắn nhãn |
| Tùy chọn: pack 2S hoặc nguồn bàn | Nguồn VM, có giới hạn dòng |
| Sổ | Danh sách chân và hai điện áp đã đo |

### Các bước

1. Chụp mặt trên và mặt dưới board. Khoanh ký hiệu chip nếu nhìn thấy.
2. Trong `lab-notes.md`, gắn nhãn mọi cổng vít và mọi chân logic bằng tên trên lụa (VM, VCC, GND, ENA, STBY, và các chân còn lại).
3. Nếu có jumper 5 V, viết nó nối cái gì. Nói jumper ở lại hay phải rút với điện áp pack của bạn.
4. Cấp VM từ pin hoặc nguồn bàn, vi điều khiển vẫn chưa nối. Đo VM và đo ray logic. Ghi cả hai.
5. Chỉ vào STBY hoặc jumper L298N và nói to phần đó làm gì. Nếu bạn có DRV8833, chỉ vào chân sleep hoặc fault và nói “thức” nghĩa là gì trên board đó.
6. Chỉ sau đó mới nối VCC hoặc logic 5 V, mass chung, và các chân vào.

### Kết quả mong đợi

Bạn gọi được tên chip, có một ảnh đã gắn nhãn chân, và có hai số đồng hồ đã ghi (VM và logic). Bạn nói được STBY hoặc jumper 5 V làm gì mà không phải đọc lại chữ lụa. Người có DRV8833 nói được dải motor 2,7–10,6 V và pack của mình có nằm trong dải đó hay không.

### Lỗi thường gặp

| Bạn thấy | Cần kiểm |
|--------------|----------------|
| Logic 5 V đọc 0 dù jumper đang cắm | Thiếu VM, jumper cắm sai chân, hoặc 7805 đã hỏng. |
| ESP32 reset khi Wi-Fi khởi động | Radio đang ăn từ 7805 của module. Chuyển nguồn logic sang buck riêng. |
| Ngõ ra TB6612 cứ chết | STBY thấp hoặc nổi. Kéo lên cao rồi đo lại. |
| DRV8833 tắt trên motor TT | Dòng stall cao hơn cái cầu nhỏ giữ nổi. Đổi motor hoặc đổi driver. |
| MX1508 nóng không chạm được | Motor quá lớn với board đó. Rút nguồn. |

## Mua ở Việt Nam / Where to buy in Vietnam

Mua con chip bạn nhận diện được, không mua tấm đỏ đầu tiên trong ảnh. Với motor TT của Capstone trên 2S, tìm TB6612 trước. L298N là board lab hợp lệ nếu bạn chấp nhận sụt áp và tản nhiệt. DRV8833 hợp motor nhỏ hơn. Giá chạy. Khoảng thô: module L298N khoảng 35.000–70.000 VND, module TB6612 khoảng 40.000–120.000 VND, breakout DRV8833 khoảng 30.000–80.000 VND.

- Trang L298N đã kiểm, khoảng 45.000 VND: [hshop.vn/mach-dieu-khien-dong-co-dc-l298](https://hshop.vn/mach-dieu-khien-dong-co-dc-l298)
- HShop: [TB6612](https://hshop.vn/search?q=TB6612), [DRV8833](https://hshop.vn/search?q=DRV8833), [L298N](https://hshop.vn/search?q=L298N)
- Shopee: [TB6612](https://shopee.vn/search?keyword=TB6612), [DRV8833](https://shopee.vn/search?keyword=DRV8833)
- Lazada: [TB6612](https://www.lazada.vn/catalog/?q=TB6612), [DRV8833](https://www.lazada.vn/catalog/?q=DRV8833)
- Thế Giới IC: [TB6612](https://www.thegioiic.com/search?q=TB6612), [DRV8833](https://www.thegioiic.com/search?q=DRV8833)

## Bài tập

1. Module của bạn có tản nhiệt bắt vít và jumper 5 V. Nguồn motor là pack 3S ở 12,6 V. Bạn làm gì với jumper, và ESP32 lấy nguồn từ đâu?
2. Chương trình TB6612 đặt AIN1, AIN2 và PWMA đúng, mà trục không nhúc nhích. Chân nào là chân bạn kiểm đầu tiên?
3. VM trên board DRV8833 đo được 11,1 V từ pack 3S. Số đó có nằm trong khoảng 2,7–10,6 V không?
4. Ở 1 A, một kênh L298N sụt 2 V. Chip đang biến bao nhiêu công suất thành nhiệt trên kênh đó?
5. Ảnh người bán cho thấy MX1508 cho robot hai motor TT trên 2S. Bạn mua board nào cho khung xe?

### Gợi ý đáp án

Rút jumper L298N khi trên 12 V, và nuôi ESP32 từ một buck riêng với mass chung. TB6612 im thì kiểm STBY và kéo nó lên cao. Pack 11,1 V nằm trên dải motor khoảng 10,6 V của DRV8833, nên pack đó không thuộc về chip này. Một kênh L298N ở 2 V và 1 A tiêu tán khoảng 2 W. Robot hai motor TT trên 2S cần TB6612, không phải MX1508 hay L9110.

## Đọc thêm

- Datasheet TI DRV8833 (dải VM và giao diện IN/IN): [https://www.ti.com/lit/ds/symlink/drv8833.pdf](https://www.ti.com/lit/ds/symlink/drv8833.pdf)
- Mạch mang TB6612FNG của Pololu (STBY, VM, và dòng): [https://www.pololu.com/product/713](https://www.pololu.com/product/713)
- Mạch mang DRV8833 của Pololu: [https://www.pololu.com/product/2130](https://www.pololu.com/product/2130)
- Datasheet ST L298: [https://www.st.com/resource/en/datasheet/l298.pdf](https://www.st.com/resource/en/datasheet/l298.pdf)
