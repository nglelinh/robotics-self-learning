---
layout: post
title: "Điện áp, dòng điện, công suất và định luật Ohm"
chapter: "01"
order: 1
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter01
lesson_type: required
draft: false
---

## Mục tiêu

Học xong, bạn gọi đúng điện áp, dòng điện, điện trở, công suất và đơn vị của từng cái. Bạn dùng $V = IR$ để tìm số còn thiếu trong một vòng, rồi tính nhiệt trên điện trở bằng $P = VI = I^2 R = V^2/R$. Bạn chọn điện trở nối tiếp cho LED đỏ trên 3,3 V và thấy thân 1/4 W là thừa sức. Bạn cũng nói được vì sao mô-tơ TT không phải điện trở để mắc thẳng vào GPIO của ESP32 hay Pico.

## Cần có gì trước

Chỉ cần cộng trừ nhân chia, mỗi con số đi kèm đơn vị. Viết trần 0,008 thì lúc là 8 mA, lúc là dấu phẩy bị trượt. Chưa cần breadboard; ví dụ làm trên giấy. Có đồng hồ và LED đỏ thì phần thực hành dùng luôn.

## Việc này nằm ở đâu trên xe hai bánh

Đồ án là xe vi sai hai bánh. ESP32 hoặc Pico nói logic 3,3 V. TB6612FNG lái hai mô-tơ TT từ nguồn riêng, HC-SR04 đo khoảng cách sau. Đèn "chương trình còn sống" là LED đỏ cộng một điện trở trên rail 3,3 V. Trở quá lớn thì đèn tối như firmware chết. Quên trở thì LED hoặc GPIO chết thật.

Mô-tơ TT kẹt kéo cỡ ampe. GPIO thoải mái quanh 12 mA và nguy hiểm khoảng 40 mA. Dòng mô-tơ đi nhờ USB đang nuôi chip thì rail 5 V sụt, ổn áp không giữ nổi 3,3 V, mạch reset đúng lúc bánh được lệnh chạy. Định luật Ohm tách hai lỗi đó trước khi đổ cho phần mềm.

## Điện áp, dòng điện, điện trở

Điện áp là năng lượng trên mỗi đơn vị điện tích, luôn là hiệu giữa hai điểm. Một vôn là một joule trên một coulomb. Chân 3,3 V nói rằng điện tích rơi từ chân ấy xuống mass nhả 3,3 J mỗi coulomb. Que chỉ chạm một điểm thì chưa đo được điện áp.

Dòng điện là điện tích đi qua một điểm mỗi giây. Một ampe là một coulomb mỗi giây, ký hiệu $I$. Trên GPIO và LED người ta nói bằng miliampe:

$$
1\ \mathrm{mA} = 0.001\ \mathrm{A}
$$

nên 8 mA là $0{,}008\ \mathrm{A}$. Mô-tơ TT ở một thang khác: vài trăm miliampe khi đang lăn, và một cú kéo cỡ ampe khi rô-to bị khóa. Sơ đồ trong khóa này vẽ dòng quy ước, từ dương về âm.

Điện trở $R$, đơn vị ôm ($\Omega$), cho biết linh kiện cản dòng mạnh đến mức nào. Cùng một điện áp, điện trở càng lớn thì dòng càng nhỏ. Dây jumper chỉ một phần của ôm. Điện trở 180 Ω là chỗ thắt có chủ đích. Công tắc hở là điện trở lớn đến mức dòng coi như bằng không.

Với điện trở ở nhiệt độ ổn định, ba đại lượng buộc vào nhau bởi định luật Ohm:

$$
V = IR
$$

tức là $I = V/R$ và $R = V/I$. Định luật này mô tả linh kiện thuần trở. Điện trở thì đủ đúng cho mọi phép tính trong chương. LED thì không. Nó hầu như không dẫn cho đến khi điện áp trên nó đạt mức sụt thuận, rồi dòng tăng rất dốc. Vì vậy LED luôn đi cùng một điện trở, chứ không bị đối xử như một điện trở.

![Tam giác định luật Ohm: che đại lượng cần tìm]({{ site.imgurl }}/generated/ohms_law_triangle.png)

Tam giác chỉ là mẹo nhớ cho $V = IR$. Che chữ nào thì tính chữ đó. Che $V$ thì nhân $I$ với $R$. Che $I$ thì chia $V$ cho $R$. Công suất không nằm trên tam giác này.

## Công suất, và vòng LED nối tiếp

Công suất là năng lượng mỗi giây, đơn vị oát. Với linh kiện hai chân, đó là tích của điện áp trên chính linh kiện ấy và dòng đi qua nó:

$$
P = VI
$$

Trên điện trở, thế Ohm vào. Nếu $I = V/R$ thì

$$
P = \frac{V^2}{R}
$$

Nếu $V = IR$ thì

$$
P = I^2 R
$$

Ba cách cho cùng một số trên điện trở. Trên LED, điện áp nằm gần sụt thuận còn điện trở mới đặt dòng, nên LED dùng $P = V_f I$ và điện trở nối tiếp dùng $I^2 R$. Trong $V^2/R$, chữ $V$ là điện áp trên điện trở, không phải cả nguồn.

Thân 1/4 W chịu 0,25 W nếu có không khí. Điện trở LED ở đây chỉ vài chục milioát. Điện trở nhỏ bị bắt dẫn cỡ ampe sẽ nâu vỏ, và $I^2 R$ nói trước.

Trong một vòng nối tiếp, dòng giống nhau mọi chỗ và các điện áp cộng lại bằng nguồn:

$$
V_\mathrm{s} = V_R + V_f
$$

nên $V_R = V_\mathrm{s} - V_f$ và $I = V_R / R$. Mắc song song thì mỗi nhánh thấy cùng điện áp, còn dòng thì cộng. Hai mô-tơ trên một driver là trường hợp thứ hai. Pin chịu tổng dòng. Dây USB của vi điều khiển không phải là pin đó.

## Ví dụ tính: đèn báo 3,3 V

Nguồn 3,3 V, LED đỏ với $V_f \approx 2{,}0\ \mathrm{V}$, dòng mục tiêu 8 mA để trong phòng vẫn thấy rõ mà không hành hạ chân cắm.

$$
R = \frac{V_\mathrm{s} - V_f}{I} = \frac{3.3 - 2.0}{0.008} = \frac{1.3}{0.008} = 162.5\ \Omega
$$

Chọn giá trị thông dụng kế trên, 180 Ω, để dòng thực nằm dưới mục tiêu:

$$
I = \frac{3.3 - 2.0}{180} = \frac{1.3}{180} \approx 7.2\ \mathrm{mA}
$$

Kiểm tra nhiệt bằng dòng mục tiêu và con trở bạn sẽ cắm thật. Cách này hơi bi quan, đúng cái cần trước khi tin mức công suất:

$$
P = I^2 R = (0.008)^2 \times 180 = 0.0115\ \mathrm{W} \approx 0.011\ \mathrm{W}
$$

Mức 1/4 W là 0,25 W, nên điện trở chỉ chạy khoảng 4% định mức. Lấy đúng 7,2 mA mà 180 Ω tạo ra thì nhiệt còn thấp hơn, khoảng 0,009 W. Cùng con số ấy nếu dùng 1,3 V mà điện trở thực sự gánh: $P = VI \approx 0{,}0072 \times 1{,}3 \approx 0{,}009\ \mathrm{W}$ và $P = V^2/R = 1{,}69/180 \approx 0{,}009\ \mathrm{W}$. Bản thân LED tản $P_\mathrm{LED} \approx 2{,}0 \times 0{,}0072 \approx 0{,}014\ \mathrm{W}$.

![Một vòng: nguồn, điện trở nối tiếp, LED, mass]({{ site.imgurl }}/generated/led_series_resistor.png)

Dòng ra khỏi cực dương, qua điện trở, vào LED ở anot, ra ở catot, về mass. Dòng trong điện trở chính là dòng trong LED. LED cắm ngược thì vòng tối. Đó không phải lý do để bỏ điện trở khi bạn lật lại. Không có điện trở thì không còn gì đặt dòng. LED bị ép ngồi gần 3,3 V trong khi sụt thuận chỉ khoảng 2 V, dòng thành cái mà chân cắm và đường đặc tuyến dốc của LED cho phép, thường gấp nhiều lần 20 mA.

## Ví dụ tính: mô-tơ không phải điện trở của GPIO

Giả sử mô-tơ TT kẹt kéo khoảng 0,8 A ở 6 V. Định luật Ohm bị dùng sai sẽ "ra một điện trở":

$$
R_\mathrm{stall} \approx \frac{6}{0.8} = 7.5\ \Omega
$$

Treo cái đó lên GPIO 3,3 V thì cùng công thức đoán

$$
I \approx \frac{3.3}{7.5} \approx 0.44\ \mathrm{A} = 440\ \mathrm{mA}
$$

Ngân sách GPIO cẩn thận khoảng 12 mA. Trần thường được nhắc khoảng 40 mA. Bốn trăm miliampe vượt cả hai khoảng một bậc. Chân hỏng, hoặc ổn áp sụt và chip reset. Phép tính còn nhẹ tay: mô-tơ kẹt là cuộn dây cộng hộp số bị khóa, không phải điện trở màng 7,5 Ω. Khi rô-to quay, sức điện động ngược làm dòng nhỏ hơn lúc kẹt, nên thử không tải nói dối về dòng lúc xe dúi vào tường.

Dòng mô-tơ vào chân VM của TB6612, từ nguồn trong dải module, khoảng 4,5 V đến 10 V. GPIO chỉ mang chiều quay và PWM vào logic 2,7 V đến 5,5 V, nên 3,3 V là mức cao hợp lệ. Hai mô-tơ kẹt, mỗi cái gần 0,8 A, đòi khoảng 1,6 A. USB máy tính thường gần 0,5 A, nên bánh không lấy dòng từ USB hay từ chân 3,3 V.

## Thực hành

Có linh kiện thì lắp đèn sau phép tính.

1. Viết $R = (3{,}3 - 2{,}0) / 0{,}008 = 162{,}5\ \Omega$, và bên cạnh là con 180 Ω sẽ cắm, trước khi bất kỳ chân nào vào lỗ.
2. Mắc điện trở và LED đỏ nối tiếp giữa rail 3,3 V và GND. Trên board, rail đó là chân ghi 3V3, không phải GPIO và không phải chân 5V. Chân LED dài hơn, tức anot, hướng về phía dương. Vạt phẳng trên vành hướng về GND.
3. Chỉ cấp nguồn sau khi điện trở đã nằm trong vòng. Nhìn LED từ bên cạnh, đừng nhìn thẳng vào thấu kính.
4. Đồng hồ để thang DC vôn, que đỏ ở ổ điện áp, đo trên chính điện trở. Chia điện áp đó cho 180 Ω. Bạn đang suy ra dòng, chưa được ngắt mạch để đo ampe. Việc đó để bài sau.

Bạn sẽ thấy ánh đỏ rõ, không chói gắt. Điện áp trên điện trở 180 Ω nên nằm gần 1,1 V đến 1,5 V, tức dòng gần 6 mA đến 8 mA. Vỏ điện trở không nóng. Thay bằng 220 Ω thì $I = 1{,}3 / 220 \approx 5{,}9\ \mathrm{mA}$, tối hơn một chút và vẫn đạt.

| Bạn thấy | Nguyên nhân hay gặp | Cách xử lý |
| --- | --- | --- |
| LED tối, điện trở mát | LED ngược | Đổi chiều LED. Giữ điện trở trong mạch. |
| Loé một cái rồi tối | Thiếu điện trở nối tiếp, hoặc điện trở bị lỗ breadboard nối tắt | Bỏ LED đó. Lắp lại với 180 Ω trước khi tin chân GPIO. |
| Board reset, hoặc GPIO không còn đảo được | 5 V rơi vào chân ESP32 hoặc Pico, hoặc LED lấy 5 V rồi trả về qua GPIO | Dừng. Đèn chỉ lấy từ 3V3 xuống GND. Thử lại chân bằng LED tốt và 180 Ω. |
| Sáng đến mức mất hút trong phòng | Con trở thực ra hàng chục kilôom | Đo lại. $I = 1{,}3 / 10000 = 0{,}13\ \mathrm{mA}$ trông như tắt. |

An toàn: bánh xe nếu đã gắn thì phải nhấc khỏi mặt bàn, chưa nối nguồn mô-tơ, và không đưa VM hay 5 V của USB vào GPIO. Cả thí nghiệm chỉ là một LED vài miliampe.

## Bài tập

1. LED xanh, $V_f = 2{,}2\ \mathrm{V}$, thắp từ 5 V ở 10 mA, mắc giữa 5 V và GND, không vào GPIO. Tính $R$, chọn giá trị kế trên trong bộ 220 Ω, 270 Ω, 330 Ω, rồi tính $P$ trên điện trở đó.
2. Hộp không có 180 Ω, bạn dùng 220 Ω cho đèn đỏ 3,3 V với $V_f = 2{,}0\ \mathrm{V}$. Tính dòng. Trong phòng còn dùng làm đèn báo được không?
3. Một mô-tơ TT lấy 0,15 A khi lăn và 0,8 A khi kẹt. Hai cái chạy cùng lúc. Tổng nào, nếu có, vừa cổng USB giới hạn 0,5 A?
4. Một người đo được 3,3 V trên LED đang tối và không có điện trở nối tiếp, rồi nói điện áp đúng nên LED còn tốt. Với $V_\mathrm{s} = V_R + V_f$, lập luận đó thiếu gì?
5. Với điện trở 180 Ω chịu 1,3 V, chứng minh $P = VI$, $P = I^2 R$ và $P = V^2/R$ ra cùng một kết quả. Vì sao không được thế $V = 3{,}3\ \mathrm{V}$ vào $V^2/R$ cho chính điện trở đó?

<details>
<summary>Gợi ý đáp án</summary>

1. $R = (5 - 2{,}2) / 0{,}010 = 280\ \Omega$. Giá trị kế trên là 330 Ω. Khi đó $I = 2{,}8 / 330 \approx 8{,}5\ \mathrm{mA}$ và $P \approx 0{,}024\ \mathrm{W}$, thấp hơn nhiều so với 0,25 W. Đèn này không nằm trên GPIO.
2. $I = 1{,}3 / 220 \approx 5{,}9\ \mathrm{mA}$. Được. Tối hơn 8 mA nhưng trong phòng vẫn thấy. Đừng tháo điện trở để "chữa" độ tối.
3. Lúc lăn: $0{,}30\ \mathrm{A}$, dưới 0,5 A. Lúc kẹt: $1{,}6\ \mathrm{A}$, không vừa. Thử lăn có thể trông an toàn rồi vẫn reset khi một bánh bị chặn. Dòng mô-tơ không lấy từ USB.
4. Không có điện trở thì $V_R = 0$, cả 3,3 V bị ép lên LED. LED đỏ còn tốt chỉ ngồi gần 2 V khi có điện trở đặt dòng vừa phải. Thấy cả điện áp nguồn trên một LED tối nghĩa là hở, ngược, hoặc đã hỏng.
5. $I = 1{,}3 / 180 \approx 7{,}2\ \mathrm{mA}$, cả ba công thức cho khoảng 0,0094 W. Thế 3,3 V là giả vờ điện trở gánh cả nguồn và bỏ quên 2 V của LED.

</details>

## Đọc thêm

All About Circuits trình bày định nghĩa và điều kiện của định luật trong chương một chiều: [Voltage, current, resistance, and Ohm's law](https://www.allaboutcircuits.com/textbook/direct-current/chpt-2/voltage-current-resistance-ohms-law/). Bài LED của SparkFun là phần đi cùng khi điện trở đã vào vòng: [Light-emitting diodes](https://learn.sparkfun.com/tutorials/light-emitting-diodes-leds).

## Mua ở Việt Nam

Khung xe, driver, vi điều khiển, cảm biến siêu âm và phần còn lại của giỏ hàng nằm ở [BOM và cách mua bộ kit robot ở Việt Nam]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %}). Bài này chỉ thêm đồ cho đèn, và chỉ khi giỏ đó chưa có.

Bộ LED 3 mm trên Hshop giá 20 000 ₫ ngày 23 tháng 9 năm 2026: [bộ 5 loại LED 3 mm](https://hshop.vn/bo-5-loai-led-sieu-sang-3mm-thong-dung-5-kind-3mm-transparent-color-led). Lấy LED đỏ cho phép tính ở trên. Xem lại giá trước khi chuyển khoản.

Bộ điện trở xuyên lỗ 1/4 W có 180 Ω hoặc 220 Ω là món cần mua. Lúc viết bài, tìm "điện trở" trên Hshop không ra bộ 1/4 W, nên dùng trang tìm kiếm và đọc shop: [Shopee, tìm bộ điện trở 1/4W](https://shopee.vn/search?keyword=b%E1%BB%99%20%C4%91i%E1%BB%87n%20tr%E1%BB%9F%201%2F4W). Đó là trang tìm kiếm, không phải một sản phẩm. Chọn 1/4 W, sai số 5% hoặc 1%. Đừng tin một con "180 Ω" không nhãn nếu chưa đo.
