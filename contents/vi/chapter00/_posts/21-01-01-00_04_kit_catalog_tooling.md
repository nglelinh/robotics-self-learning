---
layout: post
title: "Danh mục dụng cụ bàn lab"
chapter: "00"
order: 4
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter00
lesson_type: required
draft: false
---

Dành khoảng 90 phút. Nếu đã có đồng hồ, chứng minh nó trên một mối nối đã biết rồi cất. Nếu chưa có, vẫn làm xong kiểm kê Sóng 1 và chụp các chỗ thiếu. Đừng làm nóng mỏ hàn trong bài này.

## Mục tiêu học

Bạn **nói** mỗi dụng cụ Sóng 1 dùng để làm gì, và **nêu** quan sát chứng tỏ nó chạy. Bạn **chọn** điện áp một chiều và thông mạch trên đồng hồ, và **từ chối** đo điện trở trên ray còn đang có điện. Bạn **mô tả** mối hàn là kết quả của việc đốt nóng chi tiết, không phải của việc nhỏ một giọt thiếc lên kim loại nguội, với thiếc Sn63 0,8 mm và một cái giá. Bạn **phân biệt** breadboard, vốn để tín hiệu, với đường phải tải dòng motor. Bạn **tách** kìm cắt khỏi kìm tuốt theo kiểu hỏng mà mỗi cái tránh được. Bạn **kiểm kê** bàn với Sóng 1, chụp ảnh, và ghi chỗ thiếu để bài 00-05 là danh sách mua chứ không phải đoán.

## Cần có trước

Thẻ lên nguồn từ bài 00-03 đã có, ít nhất trên giấy. Bạn biết VM motor không phải chân 3,3 V, và mỏ hàn cần giá cùng kính trước khi cần ổ cắm. Chương 01 là lúc que đo thành bài đo thật. Hôm nay bạn học dụng cụ nào trả lời câu hỏi nào, để bài đó không biến thành một chuyến ra tiệm giữa chừng.

## Vì sao việc này dính tới Capstone

Chương 07 hỏng theo những cách nhàm: một sợi dây trông đã cắm mà đứt trong đầu bấm, một mass bạn "đo" khi đồng hồ còn ở thang ohm trên ray đang sống, một dây motor bị bắt sống trong lò xo breadboard. Các lỗi đó trông như lỗi firmware. Chúng sẽ đẩy bạn vào tutorial ROS 2, mà tutorial không kêu bíp một sợi dây. Dụng cụ trong danh mục này là cách tách "timeout PWM sai" khỏi "dây sai" trước khi có đồ thị topic để rối thêm.

## "Chạy được" nghĩa là gì với từng dụng cụ

Sóng 1, chép từ hóa đơn vật tư để bài này và bài 00-05 khớp nhau, là bàn cho Chương 01 bắt đầu: đồng hồ vạn năng, mỏ 60 W có giá, thiếc, kìm cắt, breadboard không hàn, dây cắm, cáp USB truyền được dữ liệu, vi điều khiển, vài LED, và một nút nhấn. Sóng 2 là khung xe, TB6612FNG, và HC-SR04. Sóng 3 là cell và cục sạc từng cell một. Bài này là dụng cụ của Sóng 1. Bản thân vi điều khiển là một dòng trên phiếu kiểm kê, không phải dụng cụ bạn học cách vung.

![Chân dung các họ đồ trên bàn, không phải một bộ có thương hiệu]({{ site.imgurl }}/generated/kit_catalog_overview.png)

Bức vẽ là các loại đồ. Đồng hồ, mỏ, breadboard và đồ cầm tay là sóng bắt buộc. Nguồn bàn và máy phân tích logic, nếu hình vẽ chúng như thiết bị sau, không phải món mua hôm nay. Hàng dưới, board và robot, mua từ bài 00-05 khi bạn sẵn sàng, không mua trùng ở đây.

### Đồng hồ

Đồng hồ vạn năng số trả lời ba câu bạn sẽ hỏi liên tục, và một câu bạn không được hỏi do tai nạn.

**Điện áp một chiều** đo hiệu giữa hai điểm. Vạch chọn là V có gạch thẳng. Đen trên mass, đỏ trên điểm bạn quan tâm. Chân USB 5 V lành khoảng 5 V. Chân 3,3 V lành khoảng 3,2–3,4 V. Số 0,00 V nghĩa là tắt, sai chân, hoặc không thực sự đang trên mass. Nó không có nghĩa đồng hồ hỏng cho tới khi thông mạch đã chứng minh hai que.

**Thông mạch** kêu khi điện trở giữa hai que rất nhỏ. Chạm hai que vào nhau. Bạn phải nghe một tiếng bíp và thấy màn hình gần 0 Ω, đôi khi vài phần mười ohm của chính dây que. Tiếng bíp đó là bằng chứng đồng hồ sống. Một dây ngắn lành thì kêu. **OL** nghĩa là đồng hồ không thấy đường.

**Ohm** giữ một con số khi không có tiếng bíp. Chỉ đo điện trở trên chi tiết **không có điện**. Đồng hồ bơm một dòng nhỏ. Trên ray đang nuôi, dòng đó đánh nhau với nguồn, số đọc vô nghĩa, và bạn có thể hỏng đồng hồ hoặc board. Không bao giờ đo ohm trên ray đang có điện.

Chế độ dòng là cái bẫy. Que đỏ chuyển sang lỗ ghi A hoặc mA, và đồng hồ trở thành gần như ngắn mạch. Đo điện áp theo cách đó là ngắn nguồn. Nhìn lỗ cắm trước mỗi lần đo áp.

![Đồng hồ cầm tay; lỗ cắm quan trọng ngang vạch chọn]({{ site.imgurl }}/wikimedia/Digital_Multimeter_Aka.jpg)

Máy của bạn có thể là UNI-T UT33D+ hoặc Wadfow. Cái nào cũng đủ nếu nó kêu và đọc được điện áp một chiều. Bằng chứng còn sống là tiếng bíp đó, trước khi bạn tin một con số trên robot.

### Mỏ, giá, và thiếc

Mối hàn là việc giữa pad và chân. Đốt hai thứ đó, rồi để một ít thiếc chảy lên kim loại nóng. Chảy giọt trên mũi rồi chấm lên chân nguội thì được viên trông đầy mà rơi tuần sau. "Được" nghĩa là thiếc thấm cả hai mặt, mối bóng, pad bên cạnh không cầu.

Hợp kim trong danh sách khóa là Sn63/Pb37 đường kính 0,8 mm. Đường kính đủ nhỏ cho chân header. Giá không tùy chọn: mũi 60 W bỏ trên dây sẽ kết thúc buổi lab. Kính vẫn ở trên mắt khi cắt chân, vì mẩu chì là đạn. Khói flux là lý do mở cửa sổ, không phải lý do cúi sát.

![Mỏ không giá là ảnh của mối nguy, không phải bố trí bạn muốn]({{ site.imgurl }}/wikimedia/Soldering_iron.jpg)

Đọc bức ảnh như một mỏ trần, tức mối nguy. Mỏ của bạn nằm trong giá bạn mua cùng. Bạn biết cặp đó chạy khi mỏ đứng yên lúc bạn với tay lấy thiếc. Chương 00 không đòi một mối tập.

### Breadboard không phải đường motor

Breadboard không hàn là lưới lò xo. Lỗ cùng hàng thì nối nhau. Rãnh giữa cho chip ngồi dạng yên ngựa. Ray mép trên nhiều board 830 điểm **đứt ở giữa**. Ray không kêu từ đầu này sang đầu kia là cái khe, không phải bí ẩn.

![Breadboard không hàn: ổn cho tín hiệu, sai cho dòng motor]({{ site.imgurl }}/wikimedia/breadboard.jpg)

Breadboard chạy được khi một sợi dây kêu từ đầu hàng tới cuối hàng, và im khi bắc qua rãnh giữa. Dòng motor không thuộc về các lò xo đó. Motor TT đang stall là một phần lớn của ampe, và điện trở tiếp xúc biến thành nhiệt cùng sụt áp. Tín hiệu ở trên breadboard. Dây motor chờ vít của TB6612FNG.

### Kìm cắt và kìm tuốt

Kìm cắt xén một chân. Đó là kìm cỡ 170 trong danh sách mua. Nó chạy được khi chân rời sạch và mẩu chì bị bắt lại. Dùng nó để tuốt thì nó cứa đồng, dây gãy sau ở vết cứa. Kìm tuốt bỏ vỏ mà không cắn ruột dẫn. Dao là thứ thay tệ hơn và thuộc danh sách thiếu. Dây cắm cũng hỏng trong đầu bấm trong khi nhựa vẫn đẹp, nên motor im với một sợi PWM trông ổn là một bài bíp.

### Sau này, không phải bây giờ

Nguồn có giới hạn dòng, máy phân tích logic, và oscilloscope làm buổi sửa sau này nhanh hơn. Không cái nào trong ba thứ đó cần để qua Chương 00, và không cái nào sửa một mass chung bị thiếu. Ghi chúng là việc sau.

## Lab: kiểm kê với Sóng 1

Dọn một góc bàn. Bày mọi món Sóng 1 bạn thực sự có. Đừng mượn đồ từ phòng khác vào ảnh "cho đủ".

Các dòng: đồng hồ, mỏ, giá, thiếc, kìm cắt, breadboard, dây cắm, cáp USB truyền dữ liệu, vi điều khiển, ít nhất một LED, ít nhất một nút nhấn. Mỗi dòng ghi `có` hoặc `thiếu`. Chụp bố trí. Đưa ảnh vào sổ. Ở trường serial, ghi tên cổng nếu board hiện khi chỉ cắm USB, hoặc `cáp chưa chứng minh — chưa có board` hoặc `cáp chưa chứng minh — không thấy cổng`.

Rồi chứng minh đồng hồ nếu bạn có. Hai que chạm: bíp. Ghi "bíp trên ngắn đã biết". Không bíp nghĩa là đồng hồ chưa phải dụng cụ. Đừng đo ohm trên thứ đang cắm điện. Không có đồng hồ nghĩa là `thiếu đồng hồ`, và các bài đo của Chương 01 phải chờ. Nếu có breadboard, bíp một hàng và xác nhận rãnh giữa im. Nếu có mỏ, xác nhận giá và để mỏ rút điện. Kiểm kê không cần mũi nóng.

**Bạn sẽ thấy gì.** Một ảnh, một danh sách thiếu, và một tiếng bíp hoặc một dòng thiếu đồng hồ viết rõ.

**Khi lệch.** Đồng hồ của bạn bè trong ảnh không tính. Bíp trên board đang cắm điện không phải bài đo ohm; rút điện trước. Dây motor trên breadboard thì rút ra. Một đồng hồ là đủ, không phải hai.

## Ví dụ làm sẵn

Ảnh của Quân có đồng hồ Wadfow, mỏ 60 W, không giá, một cuộn thiếc 0,8 mm, kìm cắt, không breadboard, một cáp USB chỉ sạc mà anh chưa chứng minh, và không vi điều khiển. Anh ghi thiếu: giá, breadboard, dây cắm, cáp dữ liệu, MCU, LED, nút. Anh chạm hai que và có tiếng bíp, nên dòng đồng hồ là `có`, bằng chứng "bíp trên ngắn đã biết". Anh không đo ohm cổng USB khi cáp còn cắm laptop.

Anh chỉ tính giá các món dụng cụ còn thiếu, theo snapshot Hshop ngày 23 tháng 9 năm 2026, và để MCU cho bài 00-05. Anh đã có mỏ, thiếc và kìm. Chỗ thiếu hôm nay là giá và breadboard:

$$
40000 + 35000 = 75000
$$

đồng, cộng dây cắm và cáp dữ liệu từ bài 00-05, cộng board. Một bộ dụng cụ cho ngăn kéo trống, một đồng hồ không phải hai, là Wadfow 185000 ₫, hoặc UT33D+ 285000 ₫, cộng mỏ 75000 ₫, giá 40000 ₫, thiếc 24000 ₫, kìm 35000 ₫, và breadboard 830 điểm 35000 ₫. Với đồng hồ Wadfow tổng là

$$
185000 + 75000 + 40000 + 24000 + 35000 + 35000 = 394000
$$

đồng. Với UT33D+ tổng ngăn kéo trống là 494000 ₫. Quân ghi cả hai con số, ngày 23 tháng 9 năm 2026, và không đặt oscilloscope.

## Bài tập

1. Hai que đang chạm và đồng hồ im. Bạn có được đo chân 3,3 V rồi tin con số không? Kiểm tra gì trước?
2. Bạn muốn điện trở của một điện trở 10 kΩ vẫn cắm trên ray ESP32 đang nuôi. Vì sao phép đo bị từ chối, và bạn làm gì thay vào đó?
3. Mối hàn trông như quả cầu ngồi trên chân. Bước nào bị bỏ: đốt mối, hay cho thiếc? Thiếc Sn63 0,8 mm đổi lượng bạn cần thế nào?
4. Dây motor đang stall bị ấn vào lỗ breadboard vì vít ở phòng khác. Cái gì hỏng về điện, và dây đó nên chờ ở đâu?
5. Ảnh Sóng 1 của bạn có đồng hồ và mỏ, không giá, không thiếc, không kìm. Chỗ thiếu nào có thể làm bạn hoặc dây cháy trước khi Chương 01 kịp bảo đo một điện trở?

<details>
<summary>Gợi ý đáp án</summary>

1. Không. Đồng hồ im khi hai que chạm thì chưa chứng minh thông mạch. Kiểm tra vạch, lỗ que, và pin trước khi tin một điện áp.
2. Thang ohm bơm dòng vào ray đang sống. Rút board, nhấc một chân điện trở nếu nó đang trong mạch, và đo chi tiết khi không có điện.
3. Chân và pad không được đốt; thiếc bị thả xuống như một giọt. Dây 0,8 mm mỏng hơn cho phép bạn cấp một lượng nhỏ lên mối nóng thay vì làm ngập.
4. Lò xo là tiếp xúc kém, có điện trở, với dòng motor. Nó nóng và sụt áp. Dây chờ vít driver hoặc một bộ dây đúng cách. Tín hiệu thì được dùng breadboard.
5. Thiếu giá. Mỏ nóng trên bàn hoặc trên chính dây của nó là nguy ngay. Thiếu thiếc và kìm chặn mối hàn và việc cắt chân; chúng không thay cái giá.

</details>

## Đọc thêm

- [Cách dùng đồng hồ vạn năng (SparkFun)](https://learn.sparkfun.com/tutorials/how-to-use-a-multimeter) — điện áp, thông mạch, và bẫy lỗ đo dòng, có hình.
- [Tài liệu Arduino](https://docs.arduino.cc/) — không phải sổ tay dụng cụ. Đó là nơi LED và nút trong danh sách Sóng 1 sẽ được dùng khi board tới. Đừng bắt đầu tutorial motor từ trang chủ.

## Mua ở Việt Nam

Mua chỗ thiếu, không mua bản thứ hai của thứ ảnh đã có. Giỏ robot đầy đủ vẫn là [bài 00-05]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %}). Giá dưới đây là snapshot Hshop ngày **23 tháng 9 năm 2026**.

| Dụng cụ | Snapshot | Trang |
| --- | ---: | --- |
| Đồng hồ UNI-T UT33D+ | 285000 ₫ | [UT33D+](https://hshop.vn/dong-ho-van-nang-dien-tu-digital-multimeter-uni-t-ut33d-chinh-hang) |
| Đồng hồ Wadfow WDM1501 | 185000 ₫ | [WDM1501](https://hshop.vn/dong-ho-van-nang-ky-thuat-so-vom-wadfow-wdm1501-digital-multimeter-true-rms) |
| Mỏ Wadfow 60 W | 75000 ₫ | [WEL3616](https://hshop.vn/mo-han-60w-wadfow-wel3616-soldering-iron) |
| Giá mỏ tròn | 40000 ₫ | [giá](https://hshop.vn/de-gac-mo-han-tron-b-2-co-khay-roi) |
| Thiếc Sunchi 0,8 mm Sn63/Pb37 | 24000 ₫ | [thiếc](https://hshop.vn/thiec-han-sunchi-kp26-0-8mm-sn63-pb37-solder-wire) |
| Kìm cắt 170 | 35000 ₫ | [kìm](https://hshop.vn/kim-cat-day-dien-nho-170-cat-chan-linh-kien-dien-tu) |
| Breadboard 830 điểm | 35000 ₫ | [breadboard](https://hshop.vn/test-board-cammb-102) |

Chọn một đồng hồ. Dây cắm, LED, nút và cáp USB dữ liệu là trang tìm kiếm, vì bài này không bịa thêm slug Hshop. [Shopee, dây cắm breadboard](https://shopee.vn/search?keyword=d%C3%A2y%20c%E1%BA%AFm%20breadboard) và [Lazada, dây jumper đực đực](https://www.lazada.vn/catalog/?q=d%C3%A2y%20jumper%20%C4%91%E1%BB%B1c%20%C4%91%E1%BB%B1c) là trang tìm kiếm. Kìm tuốt, nếu đó là chỗ thiếu mà kìm cắt không lấp được: [Shopee, kìm tuốt dây](https://shopee.vn/search?keyword=k%C3%ACm%20tu%E1%BB%91t%20d%C3%A2y). [Thế Giới IC](https://www.thegioiic.com/) và [IC Đây Rồi](https://icdayroi.com/) là trang chủ nếu bạn đứng tại quầy, không phải một SKU. Oscilloscope, máy phân tích logic và nguồn giới hạn dòng ở ngoài hóa đơn này.
