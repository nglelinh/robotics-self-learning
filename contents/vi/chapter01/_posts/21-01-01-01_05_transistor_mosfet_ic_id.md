---
layout: post
title: "Transistor, MOSFET, IC ổn áp và dạng vỏ"
chapter: "01"
order: 5
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter01
lesson_type: required
draft: false
---

## Mục tiêu

Học xong, bạn từ chối mọi sơ đồ chân đoán theo hình vỏ. TO-92 hoặc TO-220 có thể là 2N2222, BC547, 2N3904, AMS1117, 7805, hoặc một MOSFET nhỏ, và chỉ chữ in biết nó là gì. Bạn đánh số DIP từ chấm hoặc rãnh, ngược chiều kim đồng hồ. Bạn giải thích vì sao cực cổng MOSFET không phải cực bazơ lấy dòng, và vì sao $V_{GS(th)}$ không phải điện áp để khoá mô-tơ mở hoàn toàn. Bạn so một 2N2222 dùng như công tắc đèn với TB6612 mà xe thực sự cần, và nói vì sao không được đổ 12 V vào chân 5 V của ESP32 với hy vọng ổn áp onboard sẽ gánh.

## Cần có gì trước

Bạn nhận catot diode bằng vạch, và dùng được thang diode trên linh kiện mất nguồn. Bạn biết GPIO là vật 12 mA đến 40 mA, còn mô-tơ TT kẹt là vật cỡ ampe. Bài này là nhận dạng, cộng hai thông số ngăn linh kiện cháy: thứ tự chân, và nhiệt khi phải chịu sụt áp.

## Vì sao xe hai bánh không giao mô-tơ cho một transistor lẻ

Board ESP32 giấu một AMS1117-3.3, hoặc họ hàng của nó, giữa USB 5 V và rail 3,3 V. Pico có ổn áp riêng giữa VBUS và 3V3. Nhờ chúng, board nói logic 3,3 V với TB6612, dải logic của driver khoảng 2,7 V đến 5,5 V. Đó không phải giấy phép đưa pin 12 V vào chân ghi 5V.

Một transistor nhỏ trông như cách bật một mô-tơ TT từ GPIO. Mô-tơ có điện cảm, nên khi khoá ngắt cần một đường hồi tiếp, và dòng kẹt nằm gần hoặc vượt quá mức 2N2222 muốn gánh. MOSFET được chọn vì ngưỡng "chỉ có 2 V" vẫn có thể mở dở ở 3,3 V và nóng. TB6612 đã giải quyết việc này cho hai kênh, 1,2 A liên tục và 3,2 A đỉnh. Bài này dạy nhận vỏ để khỏi lắp ổn áp vào chỗ sơ đồ vẽ transistor.

## Vỏ linh kiện, và vì sao chữ in thắng

TO-92 là viên nhựa đen nhỏ ba chân. TO-220 là vỏ có tai lớn hơn. Cả hai hình đều bị nhiều loại silic dùng chung. 2N2222, BC547 và 2N3904 là transistor lưỡng cực nhỏ với thứ tự chân khác nhau. P2N2222 và 2N2222 là cặp nổi tiếng: cùng họ, khác thứ tự chân. AMS1117 và 7805 là ổn áp, không phải công tắc. MOSFET nhỏ trong vỏ TO-92 sẽ không sống nếu bạn đấu theo sơ đồ chân 2N2222 đã học thuộc.

![Nhiều vỏ cùng bóng dáng nhưng không cùng sơ đồ chân]({{ site.imgurl }}/generated/component_lookalikes.png)

Đọc chữ trên mặt phẳng, rồi mở đúng datasheet đó. Chữ mòn thì linh kiện là vô danh. Đừng thử thứ tự chân trên GPIO đang có điện.

Vỏ DIP đánh số từ rãnh hoặc chấm. Rãnh ở trên, chân 1 nằm góc trên bên trái. Số chạy xuống cạnh trái rồi lên cạnh phải: ngược chiều kim đồng hồ khi nhìn từ trên. Cùng luật ấy có ích khi một IC chuyển mức ngồi cưỡi rãnh breadboard.

## Công tắc lưỡng cực, MOSFET, và con số $V_{GS(th)}$ không phải

NPN dùng làm công tắc cần dòng bazơ, thường cỡ một phần mười dòng colectơ, qua một điện trở từ GPIO. Tải 150 mA đã đòi khoảng 15 mA, gần hết ngân sách GPIO cẩn thận. Cú kẹt 800 mA theo cùng quy tắc đòi khoảng 80 mA, GPIO không có, và định mức của chính 2N2222 là giới hạn kế tiếp. Khi khoá ngắt, dòng mô-tơ không dừng ngay. Cần diode hồi tiếp, vạch về phía nguồn mô-tơ, nếu không xung áp rơi lên colectơ.

Cổng MOSFET thì khác. Khi đóng cắt bình thường bạn không đẩy một dòng cổng liên tục. Bạn nạp cổng lên một điện áp, và điện trở kênh phụ thuộc cổng cao hơn cực nguồn bao nhiêu. $V_{GS(th)}$, điện áp ngưỡng, là mức mà nhà sản xuất đo một dòng thử rất nhỏ, thường một phần tư miliampe. Đó là lúc bắt đầu dẫn, không phải lời hứa $R_{DS(on)}$ thấp. Datasheet có thể ghi ngưỡng từ khoảng 2 V đến 4 V rồi chỉ công bố $R_{DS(on)}$ ở $V_{GS} = 4{,}5\ \mathrm{V}$ hoặc $10\ \mathrm{V}$. Giữ cổng "vừa ngưỡng" thì FET nằm vùng tuyến tính: nó rơi vôn, nó nóng, mô-tơ chậm.

MOSFET mức logic là con có điện trở dẫn thấp được công bố ở $V_{GS}$ cỡ logic, đôi khi 4,5 V, đôi khi 2,5 V. Kể cả con tốt, dùng làm khoá phía thấp cho một mô-tơ TT, vẫn cần diode hồi tiếp. Hai mô-tơ, hai chiều, và PWM là lý do giỏ hàng dùng TB6612 chứ không phải transistor bạn vừa nhận dạng. Driver vẫn là các MOSFET. Bạn chỉ không tự đấu cổng của chúng trên breadboard cho đồ án.

## Ổn áp, và oát bị vứt thành nhiệt

Ổn áp tuyến tính như 7805 giữ ngõ ra 5 V bằng cách biến phần điện áp thừa thành nhiệt. Công suất trong ổn áp là độ sụt nhân dòng:

$$
P = (V_\mathrm{in} - V_\mathrm{out}) \, I
$$

Lấy một ca nhẹ. Nguồn 9 V, ra 5 V, tải 200 mA:

$$
P = (9 - 5) \times 0.2 = 0.8\ \mathrm{W}
$$

TO-220 với một chút đồng hoặc tai nhỏ làm được việc đó. Nó sẽ ấm. Bây giờ tưởng tượng 12 V đổ vào chân 5 V của board ESP32, nơi AMS1117-3.3 tạo 3,3 V cho board đang lấy 150 mA khi Wi-Fi bật:

$$
P = (12 - 3.3) \times 0.15 \approx 1.3\ \mathrm{W}
$$

Đó là nhiều với một SOT-223 nhỏ trên module mỏng, và còn giả định nạn nhân duy nhất là ổn áp. Trên nhiều board, chân ghi 5V cũng chính là nút 5 V của USB. Mười hai vôn ở đó có thể chạm ổ USB và chip UART. Điện áp tối đa của riêng AMS1117 không phải lời hứa về phần còn lại của board. Trên bàn, nuôi ESP32 hoặc Pico từ USB. Pin mô-tơ chỉ vào VM của TB6612, trong khoảng 4,5 V đến 10 V. Mass chung. Đừng hy vọng.

## Ví dụ: phân loại chữ in, rồi mới đến tiếp giáp

Giả sử khay có bốn con mà bạn không được tin cái vỏ: TO-92 in BC547, TO-92 in 2N2222, TO-220 in 7805, và một MOSFET nhỏ mà chữ in thực sự đọc ra là MOSFET. Họ là: BC547 và 2N2222 là NPN, sơ đồ chân khác nhau; 7805 là ổn áp tuyến tính 5 V; MOSFET là khoá điều khiển bằng điện áp. Câu đó không cho biết chân nào là emiter. Chữ in cộng datasheet mới cho biết.

Ra khỏi mạch và mất nguồn, thang diode trên một tiếp giáp lưỡng cực chỉ là kiểm tra tỉnh táo, không phải sơ đồ chân đầy đủ. Tiếp giáp bazơ-emiter và bazơ-colectơ mỗi cái giống một diode, gần 0,6 V một chiều và hở chiều kia. Đường emiter-colectơ không được bíp như dây ở cả hai chiều. Nếu hai tiếp giáp chung một chân, chân đó là ứng viên của bazơ. Dừng ở đó. Đừng tuyên bố emiter với colectơ sau một buổi dò, và đừng lắp lên GPIO trước khi datasheet đồng ý. Ổn áp sẽ không hiện hai sụt diode gọn như 2N2222. Điều đó có ích: nếu "transistor" của bạn không thử diode như transistor, có thể đó là con 7805 bạn sắp đấu thành công tắc.

Xe vẫn không được một 2N2222 trên mô-tơ TT sau khi thử diode thành công. Chiều quay và phanh cần cầu H. Module TB6612 ta dùng chịu 1,2 A liên tục và 3,2 A đỉnh, logic nhận 3,3 V. Đó mới là cái khoá.

## Thực hành

1. Nếu có linh kiện rời, xếp theo chữ in thành lưỡng cực, MOSFET, ổn áp, hoặc không rõ. Nếu chỉ có ảnh trong bài và board trong kit, xếp các ảnh đó cùng cách và ghi họ bên cạnh.
2. Trên DIP nào nhìn thấy, tìm rãnh hoặc chấm và đánh số chân 1. Xác nhận số chạy xuống một cạnh rồi lên cạnh kia.
3. Trên board ESP32, tìm ổn áp nhỏ gần cổng USB nếu lụa hoặc thân có chữ họ AMS1117. Đừng cấp 12 V để thử. Ghi chân nào ghi 5V và chân nào ghi 3V3.
4. Mất nguồn, ra khỏi mạch, thử diode một diode đã biết và một transistor lưỡng cực đã biết nếu có. Ghi hai tiếp giáp. Không có transistor rời thì bỏ que đo và giữ bảng phân loại ở bước 1. Đừng thử diode một con còn hàn trên board đang có điện.

Bạn kết thúc với một danh sách đã gắn nhãn, không phải với một mô-tơ đang quay. Thử diode đạt khi thấy khoảng 0,5 V đến 0,7 V trên hai tiếp giáp chung một chân, và không chập emiter với colectơ. 7805 không vào danh sách đó.

| Bạn thấy | Nguyên nhân hay gặp | Cách xử lý |
| --- | --- | --- |
| Hai con TO-92, một sơ đồ chân cho cả hai | Khác chữ in, hoặc 2N2222 với P2N2222 | Đọc chữ. Mở đúng datasheet. Đừng chép thứ tự chân của con đầu. |
| Thử diode thấy ngắn cả hai chiều trên mọi chân | Linh kiện hỏng, hoặc que đang trên mạch hàn không rỗng | Nhấc linh kiện. Vẫn ngắn thì bỏ. |
| Ổn áp nóng khi 12 V vào chân 5 V | Độ sụt tuyến tính nhân dòng của board, và 12 V trên rail mang tên USB | Rút 12 V. Nuôi board từ USB. Pin mô-tơ chỉ vào VM. |
| Cổng MOSFET mát, mô-tơ chậm, thân FET nóng | Cổng bị giữ gần $V_{GS(th)}$, kênh chưa mở hết | Đây là lý do đồ án dùng TB6612, không phân cực FET ở ngưỡng. |

An toàn: lab này không có nguồn mô-tơ, không thí nghiệm 12 V, thang diode chỉ trên linh kiện rời. Tai TO-220 của ổn áp trên board đã lắp có thể vừa mang điện vừa nóng; đừng nắm để xem xe có chạy không.

## Bài tập

1. DIP có rãnh. Nhìn từ trên, chân 1 ở đâu, và số chạy chiều nào?
2. Datasheet MOSFET ghi $V_{GS(th)}$ từ 2 V đến 4 V ở $250\ \mu\mathrm{A}$, và $R_{DS(on)}$ chỉ ở $V_{GS} = 10\ \mathrm{V}$. Vì sao câu "ngưỡng 2 V, GPIO của tôi 3,3 V" không phải một thiết kế lái mô-tơ?
3. Tính nhiệt của 7805 khi sụt từ 12 V xuống 5 V ở 300 mA. Có nên bắt tai đó vào thứ gì không?
4. Có người đề xuất 2N2222 làm khoá phía thấp cho một mô-tơ TT ở 0,8 A kẹt, dòng bazơ "một phần mười dòng colectơ" lấy từ GPIO. Ước lượng dòng bazơ và nói mô-tơ còn cần gì khi transistor ngắt.
5. Vì sao một TO-92 không chữ là phụ tùng tệ hơn cả việc không có phụ tùng, nếu định thay ổn áp 3,3 V của ESP32?

<details>
<summary>Gợi ý đáp án</summary>

1. Chân 1 ở góc trên bên trái của rãnh. Số chạy xuống cạnh trái rồi lên cạnh phải: ngược chiều kim đồng hồ khi nhìn mặt trên.
2. Ngưỡng là nơi một dòng thử rất nhỏ bắt đầu. $R_{DS(on)}$ ở 10 V không nói điều đáng tin về 3,3 V. FET có thể chỉ mở một phần, nóng, và rơi mất điện áp mô-tơ cần. Con mức logic công bố điện trở dẫn ở $V_{GS}$ thấp, và đồ án vẫn dùng driver.
3. $P = (12 - 5) \times 0{,}3 = 2{,}1\ \mathrm{W}$. Có. TO-220 trần ở 2 W gây bỏng, và đó vẫn là cách sai để nuôi ESP32.
4. Dòng bazơ theo quy tắc đó khoảng $0{,}8 / 10 = 80\ \mathrm{mA}$, vượt xa GPIO 12 mA đến 40 mA. Mô-tơ còn cần diode hồi tiếp. Hãy dùng TB6612.
5. TO-92 không chữ có thể là lưỡng cực, MOSFET, hoặc thứ khác. Lắp nó thay AMS1117 có thể đưa 5 V lên rail 3,3 V. Linh kiện vô danh không phải ổn áp cho đến khi chữ in nói vậy.

</details>

## Đọc thêm

Bài transistor của SparkFun là bức tranh lưỡng cực và MOSFET, không kèm tầng công suất mô-tơ tự chế: [Transistors](https://learn.sparkfun.com/tutorials/transistors). Họ 7805, gồm độ sụt bạn vừa đổi thành nhiệt, nằm ở trang sản phẩm của TI: [LM7805](https://www.ti.com/product/LM7805). Đọc chữ trên con bạn đang cầm trước khi mượn sơ đồ chân của bất kỳ trang nào.

## Mua ở Việt Nam

Không cần transistor rời để hoàn thành xe vi sai. Cái khoá là TB6612 đã có trong giỏ ở [BOM và cách mua bộ kit robot ở Việt Nam]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %}). Mua driver, ESP32 hoặc Pico, và mô-tơ ở đó, đừng mua một túi TO-92 lẫn lộn.

Nếu muốn một diode đã biết và một transistor lưỡng cực đã biết cho lab tiếp giáp không nguồn, mua ở quầy in mã linh kiện lên túi, như [Thế Giới IC](https://www.thegioiic.com/) hoặc [IC Đây Rồi](https://icdayroi.com/). Bài này không có slug sản phẩm đã kiểm cho riêng 2N2222, nên đừng bịa. Trang tìm kiếm, nếu dùng sàn, phải được coi là trang tìm kiếm: [Shopee, tìm 2N2222](https://shopee.vn/search?keyword=2N2222). Đọc chữ khi hàng về, và đừng trả giá tưởng tượng cho một thanh không nhãn. Board ESP32 bạn vẫn cần giá 190 000 ₫ trên Hshop ngày 23 tháng 9 năm 2026 và đã mang sẵn ổn áp 3,3 V: [ESP32 NodeMCU-32S](https://hshop.vn/kit-rf-thu-phat-wifi-ble-esp32-nodemcu-32s-ch340-ai-thinker).
