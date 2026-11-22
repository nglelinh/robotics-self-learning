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

Sau bài học này, bạn sẽ nêu đúng định nghĩa và đơn vị của điện áp, dòng điện, điện trở và công suất. Bạn sẽ vận dụng $V = IR$ để tính đại lượng còn thiếu trong một mạch vòng, đồng thời tính công suất tỏa nhiệt trên điện trở bằng $P = VI = I^2 R = V^2/R$. Bạn sẽ chọn được điện trở hạn dòng nối tiếp cho LED đỏ trên nguồn 3,3 V, kiểm chứng mức công suất 1/4 W là hoàn toàn dư dả, và giải thích được vì sao không thể xem động cơ TT như một điện trở để đấu thẳng vào chân GPIO của ESP32 hay Raspberry Pi Pico.

## Cần có gì trước

Bạn chỉ cần nắm vững bốn phép tính số học cơ bản và giữ thói quen luôn ghi kèm đơn vị sau mỗi con số (viết mỗi `0,008` rất dễ gây nhầm giữa 8 mA và lỗi lệch dấu phẩy). Bài này có thể làm các ví dụ tính toán trên giấy mà chưa cần breadboard; nếu đã có sẵn đồng hồ vạn năng và LED đỏ, bạn có thể làm luôn phần thực hành.

## Bài học này nằm ở đâu trên xe hai bánh

Đồ án Capstone là một xe dẫn động vi sai hai bánh sử dụng ESP32 hoặc Pico ở mức logic 3,3 V, mạch lái TB6612FNG điều khiển hai động cơ TT từ nguồn pin riêng, và cảm biến HC-SR04 đo khoảng cách ở giai đoạn sau. Đèn báo trạng thái chương trình chỉ gồm một LED đỏ mắc nối tiếp điện trở trên đường nguồn 3,3 V: chọn điện trở quá lớn sẽ làm đèn tối đến mức tưởng nhầm firmware bị treo, còn bỏ quên điện trở sẽ làm hỏng LED hoặc chân GPIO.

Trong khi đó, một động cơ TT khi kẹt trục có thể rút dòng cỡ ampe, còn chân GPIO chỉ nên cấp dòng an toàn quanh 12 mA và có ngưỡng nguy hiểm khoảng 40 mA. Nếu dòng động cơ lấy chung từ cổng USB đang nuôi vi điều khiển, đường nguồn 5 V sẽ sụt áp khiến mạch ổn áp không giữ nổi mức 3,3 V và chip bị reset đúng lúc bánh xe nhận lệnh chạy. Định luật Ohm giúp bạn tách bạch lỗi nguồn điện với lỗi phần mềm ngay từ bước tính toán.

## Điện áp, dòng điện và điện trở

**Điện áp** là năng lượng trên mỗi đơn vị điện tích, luôn được định nghĩa là hiệu điện thế giữa hai điểm. Một vôn tương ứng với một joule trên một coulomb. Nói một chân có điện áp 3,3 V nghĩa là điện tích di chuyển từ chân đó về mass giải phóng 3,3 J cho mỗi coulomb. Vì là hiệu giữa hai điểm nên chạm một que đo đơn lẻ không thể đo được điện áp.

**Dòng điện** là lượng điện tích đi qua một điểm trong mỗi giây, ký hiệu là $I$ với đơn vị ampe (1 A bằng 1 coulomb/giây). Ở quy mô chân GPIO và LED, đơn vị thường dùng là miliampe:

$$
1\ \mathrm{mA} = 0.001\ \mathrm{A}
$$

Do đó 8 mA tương đương $0{,}008\ \mathrm{A}$. Động cơ TT hoạt động ở thang dòng lớn hơn nhiều: vài trăm miliampe khi chạy tự do và lên tới cỡ ampe khi kẹt trục. Toàn bộ sơ đồ trong khóa học tuân theo quy ước chiều dòng điện đi từ cực dương sang cực âm.

**Điện trở** $R$, đơn vị ôm ($\Omega$), đặc trưng cho mức độ cản trở dòng điện của linh kiện. Ở cùng một điện áp, điện trở càng lớn thì dòng điện càng nhỏ. Một sợi dây jumper chỉ có điện trở vài phần mười ôm, điện trở 180 Ω là mức cản dòng được tính toán có chủ đích, còn một công tắc đang hở có điện trở rất lớn khiến dòng điện coi như bằng 0.

Với linh kiện thuần trở ở nhiệt độ ổn định, ba đại lượng liên hệ với nhau qua **định luật Ohm**:

$$
V = IR
$$

Từ đây ta suy ra $I = V/R$ và $R = V/I$. Lưu ý rằng định luật Ohm áp dụng chính xác cho điện trở, nhưng không mô tả tuyến tính cho LED. Đèn LED gần như không dẫn điện cho đến khi điện áp đặt lên nó đạt mức điện áp thuận $V_f$, sau đó dòng tăng rất dốc. Vì lý do này, LED luôn phải mắc kèm điện trở hạn dòng chứ không thể xem là một điện trở thông thường.

![Tam giác định luật Ohm: che đại lượng cần tìm]({{ site.imgurl }}/generated/ohms_law_triangle.png)

Tam giác trên là mẹo ghi nhớ nhanh cho $V = IR$: che đại lượng cần tìm để thấy phép tính tương ứng (che $V$ được $I \times R$, che $I$ được $V / R$). Lưu ý rằng công suất không nằm trong tam giác này.

## Công suất và mạch LED nối tiếp

**Công suất** là năng lượng tiêu thụ hoặc tỏa ra trong mỗi giây, đơn vị oát (W). Với linh kiện hai chân, công suất bằng tích điện áp rơi trên chính linh kiện đó và dòng điện chạy qua nó:

$$
P = VI
$$

Đối với điện trở, thay $I = V/R$ vào công thức trên ta được:

$$
P = \frac{V^2}{R}
$$

Và nếu thay $V = IR$ ta được:

$$
P = I^2 R
$$

Cả ba biểu thức đều cho cùng một giá trị công suất trên điện trở. Tuy nhiên với LED, điện áp trên LED giữ gần mức $V_f$ còn dòng điện do điện trở hạn chế, nên ta tính công suất LED bằng $P = V_f I$ và công suất điện trở bằng $I^2 R$. Khi dùng $V^2/R$ cho điện trở, cần nhớ $V$ là điện áp rơi riêng trên điện trở chứ không phải điện áp toàn nguồn.

Điện trở thân 1/4 W chịu được công suất tối đa 0,25 W trong điều kiện thoáng khí. Điện trở dùng cho đèn LED chỉ tỏa vài chục milioát nên rất mát; ngược lại, ép một điện trở nhỏ gánh dòng cỡ ampe sẽ làm cháy xém vỏ, và công thức $I^2 R$ cho phép bạn dự đoán trước điều này.

Trong mạch nối tiếp, dòng điện tại mọi điểm đều bằng nhau và tổng các điện áp rơi bằng điện áp nguồn:

$$
V_\mathrm{s} = V_R + V_f
$$

Suy ra $V_R = V_\mathrm{s} - V_f$ và $I = V_R / R$. Ngược lại, trong mạch song song, các nhánh chịu cùng điện áp còn tổng dòng điện bằng tổng dòng qua từng nhánh — đây chính là trường hợp hai động cơ đấu trên cùng một nguồn pin. Nguồn pin phải gánh tổng dòng của cả hai động cơ, và cổng USB của vi điều khiển không được thiết kế cho vai trò đó.

## Ví dụ tính toán: đèn báo trên đường 3,3 V

Giả sử ta dùng nguồn 3,3 V để thắp một LED đỏ có điện áp thuận $V_f \approx 2{,}0\ \mathrm{V}$, với dòng mục tiêu 8 mA để đủ sáng trong phòng mà vẫn an toàn cho chân mạch. Trị số điện trở lý thuyết là:

$$
R = \frac{V_\mathrm{s} - V_f}{I} = \frac{3.3 - 2.0}{0.008} = \frac{1.3}{0.008} = 162.5\ \Omega
$$

Chọn trị số tiêu chuẩn gần nhất lớn hơn là 180 Ω để dòng thực tế không vượt mức mục tiêu:

$$
I = \frac{3.3 - 2.0}{180} = \frac{1.3}{180} \approx 7.2\ \mathrm{mA}
$$

Để kiểm tra độ an toàn nhiệt một cách thận trọng, ta tính thử với dòng mục tiêu 8 mA và điện trở 180 Ω:

$$
P = I^2 R = (0.008)^2 \times 180 = 0.0115\ \mathrm{W} \approx 0.012\ \mathrm{W}
$$

So với định mức 1/4 W (0,25 W), điện trở chỉ hoạt động ở mức dưới 5% công suất cho phép. Nếu tính theo dòng thực tế 7,2 mA, công suất tỏa nhiệt trên điện trở còn nhỏ hơn nữa, khoảng 0,009 W — khớp với cả hai công thức còn lại khi dùng điện áp 1,3 V rơi riêng trên điện trở: $P = VI \approx 0{,}0072 \times 1{,}3 \approx 0{,}009\ \mathrm{W}$ và $P = V^2/R = 1{,}69/180 \approx 0{,}009\ \mathrm{W}$. Bản thân đèn LED tiêu thụ $P_\mathrm{LED} \approx 2{,}0 \times 0{,}0072 \approx 0{,}014\ \mathrm{W}$.

![Một vòng: nguồn, điện trở nối tiếp, LED, mass]({{ site.imgurl }}/generated/led_series_resistor.png)

Dòng điện đi từ cực dương, qua điện trở, vào chân anot của LED, ra chân catot rồi về mass. Vì mắc nối tiếp nên dòng qua điện trở bằng đúng dòng qua LED. Nếu cắm ngược cực LED thì đèn không sáng, nhưng tuyệt đối không được bỏ điện trở khi xoay lại chiều. Không có điện trở hạn dòng, LED sẽ bị ép gần mức 3,3 V trong khi điện áp thuận chỉ khoảng 2 V, khiến dòng tăng vọt gấp nhiều lần ngưỡng 20 mA và nhanh chóng làm hỏng linh kiện.

## Ví dụ tính toán: vì sao không đấu trực tiếp động cơ vào GPIO

Giả sử một động cơ TT khi kẹt trục kéo dòng khoảng 0,8 A ở điện áp 6 V. Nếu tạm tính điện trở tương đương của cuộn dây khi kẹt theo định luật Ohm:

$$
R_\mathrm{stall} \approx \frac{6}{0.8} = 7.5\ \Omega
$$

Nếu nối trực tiếp tải này vào chân GPIO 3,3 V, dòng điện ước tính sẽ là:

$$
I \approx \frac{3.3}{7.5} \approx 0.44\ \mathrm{A} = 440\ \mathrm{mA}
$$

Trong khi đó, mức dòng khuyến nghị cho một chân GPIO chỉ khoảng 12 mA và ngưỡng tối đa thường nêu khoảng 40 mA. Dòng 440 mA vượt ngưỡng an toàn tới hàng chục lần, đủ làm cháy chân GPIO hoặc gây sụt áp ổn áp khiến vi điều khiển tự khởi động lại. Hơn nữa, động cơ là tải cảm kèm hộp số chứ không phải điện trở thuần 7,5 Ω: khi rô-to quay tự do, sức điện động ngược làm giảm dòng tiêu thụ, nên kết quả thử không tải không phản ánh đúng dòng đỉnh khi bánh xe bị kẹt vào vật cản.

Vì vậy, dòng cấp cho động cơ phải đi qua chân VM của TB6612FNG từ nguồn pin riêng (dải 4,5 V đến 10 V). Chân GPIO chỉ truyền tín hiệu chiều quay và PWM vào ngõ logic (dải 2,7 V đến 5,5 V, tương thích mức cao 3,3 V). Khi cả hai động cơ TT cùng kẹt, tổng dòng yêu cầu lên tới khoảng 1,6 A, vượt xa mức ~0,5 A của cổng USB máy tính — do đó động cơ tuyệt đối không được lấy nguồn từ USB hay chân 3,3 V.

## Thực hành

Nếu đã có sẵn linh kiện, hãy lắp mạch đèn báo theo đúng các bước sau:

1. Ghi sẵn phép tính $R = (3{,}3 - 2{,}0) / 0{,}008 = 162{,}5\ \Omega$ và chọn điện trở 180 Ω ra giấy trước khi cắm bất kỳ linh kiện nào lên breadboard.
2. Mắc nối tiếp điện trở 180 Ω và LED đỏ giữa chân 3V3 và GND (lưu ý lấy từ chân nguồn 3V3 trên board, không lấy từ chân GPIO hay chân 5V). Chân dài của LED (anot) hướng về phía dương; cạnh vát phẳng trên vành nhựa (catot) hướng về phía GND.
3. Kiểm tra chắc chắn điện trở đã nằm đúng trong vòng nối tiếp rồi mới cấp nguồn. Quan sát ánh sáng LED từ góc nghiêng thay vì nhìn thẳng vào thấu kính.
4. Chuyển đồng hồ vạn năng sang thang đo điện áp một chiều (DC V), kiểm tra que đỏ đang ở lỗ đo áp, rồi đo trực tiếp hai đầu điện trở. Lấy điện áp đo được chia cho 180 Ω để tính dòng thực tế mà không cần ngắt mạch đo ampe (phép đo dòng sẽ học ở bài sau).

**Kết quả kỳ vọng:** LED phát sáng đỏ rõ, không chói gắt; điện áp rơi trên điện trở 180 Ω nằm trong khoảng 1,1 V đến 1,5 V (tương ứng dòng khoảng 6 mA đến 8 mA) và thân điện trở không nóng. Nếu thay bằng điện trở 220 Ω, dòng còn $I = 1{,}3 / 220 \approx 5{,}9\ \mathrm{mA}$, đèn hơi dịu hơn nhưng vẫn đạt yêu cầu.

| Hiện tượng quan sát | Nguyên nhân thường gặp | Cách khắc phục |
| --- | --- | --- |
| LED không sáng, điện trở nguội | Cắm ngược cực LED | Đảo chiều hai chân LED, vẫn giữ nguyên điện trở trong mạch |
| LED lóe sáng rồi tắt hẳn | Thiếu điện trở nối tiếp, hoặc cắm hai chân điện trở vào cùng hàng lỗ breadboard làm nối tắt | Thay LED mới, lắp lại đúng với điện trở 180 Ω trước khi kiểm tra chân mạch |
| Board bị reset hoặc chân GPIO ngừng hoạt động | Đưa nguồn 5 V vào chân 3,3 V hoặc đấu LED giữa 5 V và chân GPIO | Ngắt nguồn ngay; chỉ đấu đèn giữa chân 3V3 và GND; kiểm tra lại chân bằng LED tốt kèm trở 180 Ω |
| LED tối mờ gần như không thấy | Cắm nhầm điện trở trị số hàng chục kilôôm | Đo lại trị số điện trở; với 10 kΩ, $I = 1{,}3 / 10000 = 0{,}13\ \mathrm{mA}$ nên gần như tắt |

**Lưu ý an toàn:** Nếu đã lắp bánh xe, luôn nhấc bánh khỏi mặt bàn; không nối nguồn động cơ trong bài này và tuyệt đối không đưa nguồn VM hay nguồn USB 5 V vào chân GPIO.

## Video tham khảo

- **Xem trước:** [Ohms Law Explained - The basics circuit theory](https://www.youtube.com/watch?v=HsLLq6Rm5tU) — The Engineering Mindset, tiếng Anh. Minh họa trực quan mối liên hệ giữa điện áp, dòng điện, điện trở và công suất trên một mạch đơn giản.
- [video tập giảng: Định luật Ôm đối với toàn mạch- Trần Thị Hồng Nhung](https://www.youtube.com/watch?v=Pd7jlqP4CRw) — Trường Đại học Giáo dục - ĐHQGHN, tiếng Việt. Bài giảng tiếng Việt về định luật Ohm cho toàn mạch, có đề cập sức điện động và điện trở trong.

## Bài tập

1. Cần thắp sáng một LED xanh lá có $V_f = 2{,}2\ \mathrm{V}$ từ nguồn 5 V với dòng mục tiêu 10 mA (mắc giữa nguồn 5 V và GND, không dùng GPIO). Tính giá trị $R$, chọn trị số kế trên trong tập {220 Ω, 270 Ω, 330 Ω} và tính công suất tỏa nhiệt $P$ trên điện trở đã chọn.
2. Nếu không có sẵn điện trở 180 Ω, bạn thay bằng điện trở 220 Ω cho LED đỏ ($V_f = 2{,}0\ \mathrm{V}$) trên nguồn 3,3 V. Hãy tính dòng điện qua mạch và nhận xét độ sáng trong phòng.
3. Một động cơ TT tiêu thụ 0,15 A khi chạy không tải và 0,8 A khi kẹt trục. Khi hai động cơ chạy cùng lúc, trường hợp nào (nếu có) nằm trong giới hạn 0,5 A của cổng USB?
4. Một người đo được 3,3 V trên một đèn LED đang tối (mắc không có điện trở nối tiếp) và kết luận rằng vì có đủ điện áp nên LED còn tốt. Dựa vào $V_\mathrm{s} = V_R + V_f$, lập luận này sai ở điểm nào?
5. Với điện trở 180 Ω chịu điện áp rơi 1,3 V, hãy chứng minh ba công thức $P = VI$, $P = I^2 R$ và $P = V^2/R$ đều cho cùng một kết quả. Vì sao không được thay $V = 3{,}3\ \mathrm{V}$ vào công thức $V^2/R$ cho điện trở này?

<details>
<summary>Gợi ý đáp án</summary>

1. $R = (5 - 2{,}2) / 0{,}010 = 280\ \Omega$. Chọn trị số kế trên là 330 Ω. Khi đó $I = 2{,}8 / 330 \approx 8{,}5\ \mathrm{mA}$ và $P \approx 0{,}024\ \mathrm{W}$, rất nhỏ so với định mức 0,25 W. Lưu ý mạch đèn này lấy nguồn 5 V độc lập, không mắc vào chân GPIO.
2. $I = 1{,}3 / 220 \approx 5{,}9\ \mathrm{mA}$. Hoàn toàn dùng làm đèn báo trong phòng được (chỉ dịu hơn mức 8 mA một chút). Không tháo bỏ điện trở để làm đèn sáng hơn.
3. Khi chạy không tải: tổng dòng $0{,}30\ \mathrm{A} < 0{,}5\ \mathrm{A}$. Khi kẹt trục: tổng dòng $1{,}6\ \mathrm{A} > 0{,}5\ \mathrm{A}$, vượt xa giới hạn cổng USB. Do đó, chạy thử không tải có thể tưởng là ổn nhưng mạch sẽ reset ngay khi bánh xe gặp vật cản.
4. Khi không có điện trở, $V_R = 0$ nên toàn bộ 3,3 V đặt trực tiếp lên LED. Một LED đỏ còn tốt đang dẫn điện chỉ giữ điện áp quanh 2 V khi có điện trở hạn dòng; việc đo thấy trọn 3,3 V trên một LED tối chứng tỏ LED đang bị cắm ngược, hở mạch hoặc đã cháy đứt.
5. Với $I = 1{,}3 / 180 \approx 7{,}2\ \mathrm{mA}$, cả ba công thức đều cho kết quả xấp xỉ 0,0094 W. Không được thay 3,3 V vì điện trở chỉ gánh 1,3 V; phần 2,0 V còn lại rơi trên LED.

</details>

## Đọc thêm

Tài liệu trực tuyến của All About Circuits trình bày chi tiết định nghĩa và phạm vi áp dụng của định luật Ohm trong mạch một chiều: [Voltage, current, resistance, and Ohm's law](https://www.allaboutcircuits.com/textbook/direct-current/chpt-2/voltage-current-resistance-ohms-law/). Bài hướng dẫn về LED của SparkFun bổ sung cách chọn điện trở hạn dòng thực tế: [Light-emitting diodes](https://learn.sparkfun.com/tutorials/light-emitting-diodes-leds).

## Mua ở Việt Nam

Toàn bộ danh sách khung xe, mạch lái, vi điều khiển và cảm biến nằm ở bài [BOM và cách mua bộ kit robot ở Việt Nam]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %}). Bài này chỉ bổ sung linh kiện cho mạch đèn báo nếu bạn chưa mua sẵn.

Bộ LED 3 mm trên Hshop có giá tham khảo 20.000 ₫ (ghi nhận ngày 23 tháng 9 năm 2026): [bộ 5 loại LED 3 mm](https://hshop.vn/bo-5-loai-led-sieu-sang-3mm-thong-dung-5-kind-3mm-transparent-color-led). Bạn dùng LED đỏ cho bài thực hành và nhớ kiểm tra lại giá trước khi đặt hàng.

Với bộ điện trở xuyên lỗ 1/4 W (cần có trị số 180 Ω hoặc 220 Ω), do thời điểm khảo sát Hshop không hiển thị bộ 1/4 W thông dụng, bạn có thể tìm qua trang tìm kiếm: [Shopee, tìm bộ điện trở 1/4W](https://shopee.vn/search?keyword=b%E1%BB%99%20%C4%91i%E1%BB%87n%20tr%E1%BB%9F%201%2F4W). Hãy chọn loại công suất 1/4 W, sai số 5% hoặc 1%, và luôn đo kiểm tra bằng đồng hồ trước khi cắm mạch thay vì chỉ tin vào nhãn túi.
