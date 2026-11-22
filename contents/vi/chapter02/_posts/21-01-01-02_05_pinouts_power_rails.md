---
layout: post
title: "Sơ đồ chân, mức logic và đường nguồn"
chapter: "02"
order: 5
owner: "Nguyen Le Linh"
lang: vi
categories: [chapter02]
lesson_type: required
draft: false
---

## Mục tiêu

Sau bài này, bạn xác định được đúng vị trí chân nguồn USB 5 V và chân nguồn 3,3 V đã ổn áp trên bo mạch của mình, rồi đo kiểm cả hai bằng đồng hồ vạn năng khi chỉ cấp nguồn qua USB. Bạn nắm vững nguyên tắc mọi chân GPIO của ESP32 và Pico đều là 3,3 V và có thể hỏng nếu đưa 5 V vào. Bạn vẽ được sơ đồ đấu nguồn pin 2S vào chân VM của TB6612 trên giấy, đồng thời liệt kê đầy đủ các chân header mà nguồn pin tuyệt đối không được chạm tới. Bạn cũng thiết kế được mạch chuyển mức tín hiệu Echo của HC-SR04 kèm nối chung mass trước khi đấu dây cảm biến thật. Trong suốt bài thực hành này, không kết nối pin.

## Cần gì trước khi học

Bạn cần đã hoàn thành bài nhịp tim để xác nhận bo mạch kết nối tốt với máy tính và biết rõ chân LED của mình. Bạn cần biết đặt đồng hồ vạn năng ở thang đo điện áp một chiều và đặt que đen lên chân mass (GND) xác định. Kiến thức về mạch chia áp ở chương 01 là phần tính toán duy nhất cần dùng. Nguồn động cơ chưa được đấu nối; danh sách đầy đủ gồm driver và pin nằm ở bài mua sắm chương 00 ([Hóa đơn linh kiện và cách mua]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %})).

## Vì sao bài này gắn với Capstone A

Nhiều lỗi nghiêm trọng khi chạy firmware teleop ở chương 07 không xuất phát từ lỗi lập trình mà từ lỗi đấu nối phần cứng: đưa thẳng xung Echo 5 V vào GPIO 3,3 V; quên nối chung mass giữa mạch động cơ và vi điều khiển khiến tín hiệu PWM bị trôi mức tham chiếu và TB6612 không đọc được; hoặc cấp nhầm pin 7,4 V vào chân 5V hay 3V3 trên bo mạch. Hậu quả là chip bị reset liên tục hoặc hỏng chân ngay lần cấp điện đầu tiên. Cơ chế tự ngắt 300 ms và quy tắc nhấc bánh không thể bảo vệ được một chân GPIO đã bị quá áp. Thẻ sơ đồ chân bạn lập trong bài này sẽ là tài liệu đối chiếu trực tiếp khi bắt đầu lắp driver ở chương 05 và xuất PWM ở chương 07.

## Hai đường nguồn trên bo mạch và đường nguồn riêng cho động cơ

Chân GPIO của ESP32 và Pico hoạt động ở mức logic 3,3 V; cấp 5 V vào chân GPIO có thể làm hỏng chân chip. Trên ESP32, điện áp cực đại tuyệt đối chỉ cao hơn nguồn nuôi khoảng một mức sụt áp diode:

$$
V_{DD} + 0{,}3\,\mathrm{V} = 3{,}3\,\mathrm{V} + 0{,}3\,\mathrm{V} = 3{,}6\,\mathrm{V}.
$$

Giới hạn chịu áp trên Pico cũng tương tự, chỉ nhỉnh hơn 3,3 V vài phần mười vôn. Điện áp 5 V vượt xa cả hai giới hạn này.

Tách biệt với giới hạn hư hỏng trên, quy tắc ước lượng trong học tập cho mức logic cao là điện áp nên đạt ít nhất khoảng $$0{,}7 \times 3{,}3\,\mathrm{V} \approx 2{,}3\,\mathrm{V}$$ để được đọc ổn định là mức cao (giá trị $$V_{IL}$$ và $$V_{IH}$$ chính xác tra trong datasheet). Quy tắc vận hành đơn giản và an toàn nhất là không bao giờ nối trực tiếp ngõ ra 5 V vào chân GPIO 3,3 V.

Trên bo mạch ESP32 cổ điển, chân ghi `5V` hoặc `VIN` lấy nguồn 5 V từ cổng USB (thường đi qua một diode Schottky nên điện áp thực đo thấp hơn 5 V vài phần mười vôn). Đường này có thể cấp cho một cảm biến tiêu thụ dòng nhỏ khi thử trên bàn, nhưng tuyệt đối không dùng để cấp nguồn cho động cơ TT. Dòng không tải của một động cơ TT theo thông số bán hàng đã vào khoảng 110 mA đến 150 mA, và tăng lên gấp nhiều lần khi bị kẹt trục. Hai động cơ cộng thêm xung dòng phát Wi-Fi sẽ làm sụt nguồn cổng USB, gây mất kết nối hoặc reset do sụt áp (brownout) — biểu hiện giống hiện tượng lặp lại dòng tiêu đề đã gặp ở bài nhịp tim. Trong khi đó, chân `3V3` là ngõ ra của mạch ổn áp dùng để nuôi khối logic, hoàn toàn không dành cho động cơ.

Trên Raspberry Pi Pico, tên các chân nguồn thể hiện rõ chức năng hơn: `VBUS` là nguồn 5 V trực tiếp từ USB khi cắm cáp; `VSYS` là ngõ vào nguồn hệ thống nhận từ USB qua diode và chấp nhận nguồn ngoài trong khoảng 1,8 V đến 5,5 V; `3V3` là ngõ ra đã ổn áp. Không bao giờ đưa pin 7,4 V vào `3V3` hay `VSYS`, vì cả hai đều vượt quá giới hạn thiết kế, đặc biệt đưa 7,4 V vào `3V3` sẽ đánh thẳng vào ngõ ra mạch ổn áp.

![USB 5 V, 3,3 V đã ổn áp, và ray motor nằm ngoài header]({{ site.imgurl }}/generated/power_rails_3v3.png)

Hãy hiểu sơ đồ nguồn theo cả mức điện áp lẫn khả năng cấp dòng: đường 5 V từ USB chỉ đủ cho tải nhỏ, đường 3,3 V dành riêng cho mạch logic, mass (GND) phải nối chung, còn đường nguồn động cơ phải tách riêng hoàn toàn khỏi hàng chân vi điều khiển.

![Giải phẫu board: que đo đặt lên header, không đặt lên module]({{ site.imgurl }}/generated/pcb_mcu_anatomy.png)

Cổng USB cấp cho `VBUS` (hoặc chân `5V` trên ESP32), còn mạch ổn áp tạo ra đường `3V3`. Khi đo kiểm, đặt đầu que đo trực tiếp vào các chân header, không đặt lên vỏ kim loại của module.

Việc nối chung mass giữa vi điều khiển và mạch cầu H là bắt buộc. TB6612 đọc mức điện áp PWM dựa trên tham chiếu mass logic của chính nó. Nếu chân GND của driver không nối với GND của ESP32 hoặc Pico, driver sẽ không nhận diện được mức cao/thấp một cách ổn định. Khi lắp driver ở các chương sau, phải nối chung chân GND logic với vi điều khiển, còn đường nguồn động cơ VM đi riêng từ pin.

## Xử lý chân Echo 5 V

Ngõ ra Echo của cảm biến siêu âm HC-SR04 xuất xung 5 V, do đó bắt buộc phải hạ mức điện áp trước khi đưa vào chân GPIO của ESP32 hoặc Pico. Cách chắc chắn nhất là dùng mạch chuyển mức logic (level shifter): nối phía điện áp thấp (LV) vào chân `3V3` của bo mạch, phía điện áp cao (HV) vào nguồn 5 V của cảm biến và nối chung mass. Tín hiệu Echo đi qua chiều từ HV sang LV rồi vào GPIO. Nhiều cảm biến HC-SR04 có thể nhận tín hiệu kích (Trigger) ở mức 3,3 V, nhưng đó là đặc tính ngõ vào của cảm biến chứ không đồng nghĩa với việc được bỏ qua mạch chuyển mức ở chân Echo.

Trong trường hợp cần tính toán bằng mạch chia điện trở, nếu mắc điện trở $$1\,\mathrm{k}\Omega$$ từ chân Echo đến nút nối GPIO và điện trở $$2\,\mathrm{k}\Omega$$ từ nút đó xuống GND, điện áp thu được là:

$$
V_{\mathrm{GPIO}} = 5\,\mathrm{V} \times \frac{2}{1 + 2} \approx 3{,}33\,\mathrm{V}.
$$

Giá trị 3,33 V nằm khá sát giới hạn trên cho phép, và sai số điện trở hoặc chiều dài dây dẫn có thể làm điện áp tại nút này dịch chuyển, vì vậy dùng module chuyển mức vẫn ổn định hơn khi lắp trên robot thật. Bài này chưa đấu cảm biến; bạn chỉ cần ghi công thức chia áp lên thẻ sơ đồ chân để chuẩn bị cho các chương sau.

## Ví dụ đã làm

Một bộ pin 2S ghép từ hai cell 18650 có điện áp danh định 7,4 V (sạc đầy cao hơn và khi yếu thấp hơn). Hà vẽ đường đi hợp lệ duy nhất cho dây dương (màu đỏ) của pin: nối thẳng vào cực `VM` của mạch cầu H TB6612 (loại module bán tại Hshop trong ghi chú chương 00 hỗ trợ dải nguồn động cơ bao gồm 7,4 V). Dây âm (màu đen) nối vào cực `GND` của driver, đồng thời kéo một dây riêng nối `GND` này sang `GND` của vi điều khiển.

Bên cạnh đó, Hà lập danh sách các chân tuyệt đối không được chạm dây dương pin:
- Trên ESP32: mọi chân GPIO, chân `3V3` và chân `5V`/`VIN` (vì nối với nguồn USB 5 V, cấp pin 2S vào có thể đẩy ngược điện áp về laptop).
- Trên Pico: mọi chân GP, `3V3`, `VSYS` (giới hạn tối đa 5,5 V) và `VBUS`.

Chân `VCC` (nguồn logic) của mạch cầu H nhận 3,3 V hoặc 5 V chứ không phải nguồn pin `VM`. Hà ghi rõ trên bản vẽ: "pin 2S chỉ nối vào VM" và "VCC logic lấy từ 3V3, không lấy từ pin". Ở bước này chưa nối dây thật; phần thực hành đo điện áp chỉ tiến hành với nguồn USB.

## Lab

Chỉ cắm cáp USB; đảm bảo đã tháo hoàn toàn pin, mạch cầu H và cảm biến.

1. Cắm que đỏ vào lỗ đo điện áp (V), đặt que đen lên một chân `GND` xác định, chỉnh đồng hồ về thang đo điện áp một chiều (DCV).
2. Đo đường nguồn 5 V (chân `5V`/`VIN` trên ESP32 hoặc `VBUS` trên Pico) và ghi chính xác giá trị đo được.
3. Đo đường nguồn 3,3 V (chân `3V3` hoặc `3V3(OUT)` trên Pico) và ghi chính xác giá trị đo được.
4. Vẽ thẻ sơ đồ chân cho bo mạch của bạn gồm: hai đường nguồn vừa đo, các chân `GND`, chân LED của bài nhịp tim, một chân GPIO trống đã đối chiếu nhãn mạch và mục cấm (ghi rõ "không cấp 5 V vào GPIO" và "pin 2S chỉ nối vào VM và GND của driver").
5. Phác thảo mạch chuyển mức (hoặc mạch chia áp 1 kΩ / 2 kΩ) cho chân Echo của HC-SR04 ngay trên thẻ; chưa đấu dây cảm biến thật.

Kết quả đo chuẩn khi chỉ dùng USB nằm trong khoảng 4,7 V đến 5,1 V ở đường 5 V (chân `5V` của ESP32 qua diode thường đọc khoảng 4,7 V đến 4,9 V) và khoảng 3,25 V đến 3,35 V ở đường `3V3`. Ghi chính xác các chữ số đo được, không ghi chung chung là "5 V". Nếu đường `3V3` nằm ngoài khoảng cho phép — đặc biệt nếu vượt quá 3,6 V chứng tỏ có rò áp 5 V — phải rút cáp ngay để kiểm tra. Tuyệt đối không nối pin trong bài thực hành này.

![Thứ tự nối: mass chung, logic, tín hiệu, nguồn motor sau cùng, bánh nhấc]({{ site.imgurl }}/generated/power_order.png)

Sơ đồ nhắc lại trình tự đấu nối an toàn: hiện tại bạn vẫn đang ở bước kiểm tra nguồn USB; nguồn động cơ là bước cuối cùng và chỉ được cấp khi bánh xe đã nhấc khỏi bàn.

Các lỗi đo thường gặp: đặt ngược que đo (que đen vào `5V`, que đỏ vào `GND`) khiến đồng hồ hiện số âm; đặt que lên vỏ kim loại hoặc thân tụ thay vì chân header; hoặc đo chân `3V3` ra 0 V khi USB đang cắm (do đặt nhầm chân, thiếu tiếp xúc mass hoặc hỏng mạch ổn áp — cần dừng lại kiểm tra). Cấp nguồn động cơ TT từ chân `5V` sẽ gây sụt áp ngay khi động cơ khởi động hoặc kẹt trục.

An toàn: giữ pin ở ngoài khu vực mạch. Không đặt đồng hồ ở thang đo dòng điện (A/mA) rồi chạm trực tiếp giữa `5V` và `GND` vì sẽ gây ngắn mạch qua đồng hồ.

## Video tham khảo

- **Xem trước:** [HOW TO USE LOGIC LEVEL SHIFTER ON ARDUINO TO CONVERT CIRCUITS AND SENSORS FROM 5V TO 3.3V CIRCUITS](https://www.youtube.com/watch?v=RBDVBafNF44) — Circuit Desolator, tiếng Anh. Giải thích lý do không nối thẳng 5 V vào 3,3 V và cách dùng mạch chuyển mức trước khi ghép cảm biến với ESP32.
- [Logic Level Converters - Learn & Example Project - TXS0108E](https://www.youtube.com/watch?v=f7aySy_0URE) — DIY Machines, tiếng Anh. Giới thiệu module chuyển mức 8 kênh; chú ý phân biệt phía điện áp cao (HV) và phía điện áp thấp (LV) cho khớp sơ đồ chân trong bài.

## Bài tập

1. Tính điện áp ngõ ra của mạch chia áp cho nguồn 5 V với điện trở phía trên $$1\,\mathrm{k}\Omega$$ và phía dưới $$2\,\mathrm{k}\Omega$$. Nếu cả hai điện trở cùng tăng thêm 5%, tỉ số chia áp có thay đổi không?
2. Các cực của pin 2S 7,4 V được phép nối vào chân nào của TB6612, và tuyệt đối không được chạm vào những chân header nào của ESP32?
3. Trên Raspberry Pi Pico, chân nào là USB 5 V, chân nào nhận nguồn ngoài trong dải 1,8 V đến 5,5 V, và chân nào là ngõ ra đã ổn áp? Nếu cấp nhầm 7,4 V thì chân nào chịu rủi ro hư hỏng trực tiếp nhất?
4. Khi chỉ cắm USB, đồng hồ đo được 4,86 V và 3,29 V. Hai giá trị này có nằm trong ngưỡng bình thường không? Thẻ sơ đồ chân vẫn cần bổ sung câu ghi chú gì về cực VM?
5. Một sinh viên nối thẳng chân Echo của HC-SR04 vào GPIO 18 "chỉ để thử nhanh". Mức điện áp nào tác động lên chân GPIO và cần bổ sung mạch gì trên đường dây đó?

<details>
<summary>Đáp án</summary>

1. $$5 \times 2 / 3 \approx 3{,}33\,\mathrm{V}$$. Nếu cả hai điện trở cùng nhân với 1,05 thì hệ số triệt tiêu ở cả tử và mẫu nên tỉ số chia áp không đổi, điện áp lý tưởng vẫn xấp xỉ 3,33 V. Tuy nhiên, nếu sai số giữa hai điện trở lệch nhau thì điện áp sẽ thay đổi — đó là lý do dùng module chuyển mức ổn định hơn mạch chia áp ghép từ điện trở rời.
2. Cực dương pin nối vào `VM`, cực âm nối vào `GND` của mạch cầu H (và `GND` này phải nối chung với `GND` của vi điều khiển). Pin tuyệt đối không được chạm vào bất kỳ chân GPIO nào của ESP32, chân `3V3` hay chân `5V`/`VIN`.
3. `VBUS` là USB 5 V; `VSYS` là ngõ vào chấp nhận khoảng 1,8 V đến 5,5 V (nhận từ USB qua diode); `3V3` là ngõ ra đã ổn áp. Đưa 7,4 V vào `3V3` sẽ đánh thẳng vào ngõ ra ổn áp, còn đưa vào `VSYS` cũng vượt xa ngưỡng cho phép tối đa 5,5 V.
4. Cả hai đều đạt: 4,86 V nằm trong khoảng 4,7 V – 5,1 V và 3,29 V nằm trong khoảng 3,25 V – 3,35 V. Thẻ vẫn cần ghi rõ: pin 2S chỉ nối vào cực `VM` và `GND` của driver, đồng thời xác nhận chưa nối pin trong lần đo này.
5. Chân Echo đẩy xung 5 V vào GPIO 3,3 V, vượt quá giới hạn cực đại tuyệt đối khoảng 3,6 V. Cần tháo dây Echo ngay và lắp qua mạch chuyển mức logic (hoặc mạch chia áp đã tính toán) kèm nối chung mass trước khi thử tiếp.

</details>

## Đọc thêm

- [Logic levels của SparkFun](https://learn.sparkfun.com/tutorials/logic-levels) — giải thích chi tiết lý do cần chuyển mức giữa tín hiệu 5 V và ngõ vào 3,3 V.
- [Datasheet Pico](https://datasheets.raspberrypi.com/pico/pico-datasheet.pdf) — sơ đồ và thông số các đường nguồn VBUS, VSYS, 3V3 cùng dải điện áp cho phép của VSYS.
- [Datasheet ESP32 (PDF)](https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf) — bảng đặc tính điện của chân GPIO và các mức giới hạn cực đại tuyệt đối.
