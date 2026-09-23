---
layout: post
title: "Giắc nối, driver động cơ và mạch vi điều khiển"
chapter: "01"
order: 6
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter01
lesson_type: required
draft: false
---

## Mục tiêu

Học xong, bạn tách được dây Dupont bước 2,54 mm — đó là dây tín hiệu — khỏi giắc được phép mang dòng mô-tơ. Bạn từ chối ép vỏ JST-XH vào phích servo hoặc XT30 vào XT60. Bạn tính điện áp mô-tơ TT thực sự thấy từ pin 7,4 V khi đi qua TB6612 so với khi đi qua L298N, và gọi DRV8833 là phương án nhỏ hơn với trần 1,5 A, nóng khi kẹt. Bạn phân biệt board ESP32 với module WROOM trần, chỉ VBUS với 3V3 trên Pico, và giải thích vì sao echo của HC-SR04 không được rơi thẳng vào GPIO 3,3 V.

## Cần có gì trước

Bạn đo được điện áp một chiều song song, biết GPIO chỉ vài chục miliampe, và biết mô-tơ TT kẹt thì không phải vậy. Chưa cần PWM cho mô-tơ. Bài dừng ở chữ trên chip, tên chân, và một phép sụt áp trước khi bánh đầu tiên quay.

## Vì sao xe hai bánh chết ở giắc và ở driver

Đồ án là hai mô-tơ TT, một TB6612, ESP32 hoặc Pico ở 3,3 V, và một HC-SR04. Dây Dupont đúng cho AIN1, AIN2, PWMA và STBY. Chúng là cách nghèo để mang dòng kẹt vào VM, và là cách tệ hơn nữa để giả vờ GPIO chính là VM.

Pin 2S danh định khoảng 7,4 V. Cầu MOSFET rơi vài phần mười vôn. L298N, cùng giá vào ngày đã kiểm, rơi khoảng hai vôn, nên mô-tơ sống ở đầu chậm của dải điện áp. Echo của HC-SR04 là ngõ ra 5 V, còn GPIO của ESP32 hoặc Pico không phải ngõ vào 5 V. Mạch chuyển mức là món 10 000 ₫. Không việc nào trong số này cần firmware. Chúng cần đọc lụa trước khi cắm pin.

## Giắc: bước chân không phải gợi ý

Dupont, jumper chân vuông rời, làm trên bước 2,54 mm. Nó hợp breadboard và hợp tín hiệu logic vào TB6612. Tiếp điểm và sợi dây mảnh phía sau không phải giắc mô-tơ. Cú kẹt gần một ampe làm ấm một mối bấm đã mỏi và rơi mất điện áp bạn vừa tính kỹ ở driver. Dupont cho tín hiệu. Dây dày hơn, được cố định tử tế, cho dòng mô-tơ và cho dây pin vào VM.

JST-XH là họ khác. Bước chân 2,50 mm, không phải 2,54 mm, đủ gần để cám dỗ ép, và đủ khác để bẻ chân. Nó hay gặp trên dây cân bằng và trên đuôi pin nhỏ. Servo dùng phích ba chân kiểu JR, cũng gần 2,54 mm, với vai định hướng dễ bị phá nếu bạn gọt đi. XT30 và XT60 là giắc đạn cho dòng lớn hơn. Chúng không cắm vào nhau, và không cắm vào JST. Không trượt vào với một tiếng khớp và không có kim loại bị cong thì dừng. Ép vỏ là cách pin bị đảo cực lên VM.

## Sụt áp của driver, tính ở 7,4 V

Cầu H lái dòng mô-tơ. Nó không sản xuất dòng đó. Vi điều khiển bảo cầu đóng khoá chiều nào. Pin trên VM cấp ampe.

![Vi điều khiển lái cầu; pin cấp dòng cho mô-tơ]({{ site.imgurl }}/generated/hbridge_concept.png)

Module TB6612FNG trong giỏ là cầu MOSFET. Trang Hshop, đọc ngày 23 tháng 9 năm 2026, cho VM từ 4,5 V đến 10 V, logic từ 2,7 V đến 5,5 V, 1,2 A liên tục và 3,2 A đỉnh. GPIO 3,3 V là mức cao hợp lệ. Độ sụt hợp lý của kiểu cầu này, ở dòng vừa phải, là vài phần mười vôn. Lấy 0,3 V làm số để tính:

$$
V_\mathrm{motor} \approx 7.4 - 0.3 = 7.1\ \mathrm{V}
$$

Module L298N cùng giá 45 000 ₫ và là món ta không chọn làm mặc định. Nó là cầu Darlington. Tính khoảng 2 V sụt ở dòng mô-tơ:

$$
V_\mathrm{motor} \approx 7.4 - 2.0 = 5.4\ \mathrm{V}
$$

Mô-tơ TT trong khóa này thuộc lớp 3 V đến 9 V. 5,4 V vẫn quay được. Nó quay chậm hơn và yếu hơn 7,1 V, và pin không còn tươi làm khoảng cách tệ thêm. Cũng đừng dùng ổn áp 5 V onboard của module L298N để chạy ESP32.

![Module kiểu L298N: kéo được tải, và sụt áp lớn]({{ site.imgurl }}/wikimedia/Dosmotorsl298n.jpg)

DRV8833 là phương án nhỏ hơn, niêm yết 25 000 ₫, VM từ 2,7 V đến 10,8 V và 1,5 A tối đa mỗi kênh trên trang Hshop đó. Một mô-tơ TT mỗi kênh là dùng đúng. Kẹt lâu làm vỏ nhỏ nóng rất nhanh. Đừng song song cả hai mô-tơ dẫn động lên một kênh DRV8833 rồi gọi đó là phương án dự phòng. Trên TB6612, STBY phải được giữ cao, nếu không cầu ngủ và mô-tơ đứng im trong khi firmware trông hoàn hảo.

## Board: 5 V được phép tồn tại ở đâu

Board phát triển ESP32 có ổ USB, một chip UART như CH340 hoặc CP2102 gần ổ đó, một ổn áp 3,3 V, và một module vỏ kim loại. Module ESP32-WROOM trần là cái vỏ và các pad, không USB và không có ổn áp để cắm cáp. Túi không có ổ USB thì bạn chưa mua board phát triển mà giỏ hàng yêu cầu, kể cả khi vỏ ghi ESP32.

![ESP32 trên board phát triển nhỏ, có USB và ổn áp]({{ site.imgurl }}/wikimedia/ESP32_on_Lolin32_Lite_clone_board_cropped.jpg)

![Những thứ cần nhìn trên board vi điều khiển: USB, ổn áp, module, header]({{ site.imgurl }}/generated/pcb_mcu_anatomy.png)

Raspberry Pi Pico có header hai hàng và không có module Wi-Fi vỏ kim loại riêng trên bản gốc. VBUS là rail 5 V của USB khi board cắm vào máy. 3V3 là ngõ ra đã ổn áp. Logic GPIO là 3,3 V. Đừng nuôi mô-tơ TT từ 3V3, và đừng coi VBUS là một GPIO.

![Raspberry Pi Pico: header hai hàng, logic 3,3 V]({{ site.imgurl }}/wikimedia/Raspberry_Pi_Pico.jpg)

![Logic 3,3 V, USB 5 V, nguồn mô-tơ tách khỏi rail đó]({{ site.imgurl }}/generated/power_rails_3v3.png)

Chân trig của HC-SR04 thường nhận mức cao 3,3 V. Chân echo đẩy ra khoảng 5 V. Echo đó không được vào thẳng GPIO của ESP32 hoặc Pico. Mạch chuyển mức 4 kênh, món 10 000 ₫ trong giỏ, là cách thẳng: phía 3,3 V về vi điều khiển, phía 5 V về cảm biến, mass chung. Cầu chia chỉ trên echo là cách kia. Hai điện trở, 10 kΩ phía trên và 20 kΩ phía dưới, cho

$$
V_\mathrm{out} = 5 \times \frac{20}{10 + 20} \approx 3.3\ \mathrm{V}
$$

mức mà chân 3,3 V chịu được. Đừng đặt cầu chia đó lên một chân mà cảm biến đang muốn đọc như ngõ vào 5 V, trừ khi bạn đã kiểm 3,3 V là mức cao hợp lệ với nó. Trig từ GPIO thường ổn, không cần cầu chia. Echo mới là chân cắn.

## Thực hành

Làm khi pin đã tháo và mô-tơ chưa cắm. Nhận dạng trước.

1. Chụp chip driver, đủ gần để đọc chữ. Ghi TB6612FNG, DRV8833, hoặc L298N, đúng cái đang in. Nếu chỉ là nhãn của nhà bán module chứ không phải silic, hãy nói vậy.
2. Chụp chip UART của vi điều khiển. CH340 và CP2102 là hai con hay gặp trên board ESP32 của khóa này. Không ổ USB và không chip nối tiếp thì bạn đang cầm module trần.
3. Từ mô tả TB6612 trên Hshop, gắn nhãn một tờ phác: AIN1, AIN2, PWMA, STBY, VM, VCC và GND. Khớp các tên đó với lụa trên module nếu đã có. VM là nguồn mô-tơ, khoảng 4,5 V đến 10 V. VCC là logic, 2,7 V đến 5,5 V, nên chân 3,3 V của ESP32 hoặc Pico được phép nuôi nó. GND là mass chung với vi điều khiển. STBY phải được kéo cao, nếu không ngõ ra tắt.
4. Trên Pico hoặc ESP32, chỉ 3V3, nút 5 V của USB (VBUS hoặc chân ghi 5V), và một GPIO. Nói to chân nào trong ba chân đó được chạm echo của HC-SR04. Câu trả lời là không chân nào, cho đến khi echo đã được chuyển mức hoặc chia áp.

Bạn kết thúc với hai bức ảnh và một tờ đã gắn nhãn, mọi dây mô-tơ vẫn trong túi. Tờ đúng cho thấy VM và VCC là hai chân khác nhau. Nếu module của bạn nối chúng làm một, đó không phải đường tắt; đó là module không thể nhận pin 7,4 V mà không ép điện áp ấy lên chân logic. Đừng cấp nguồn theo cách đó.

| Bạn thấy | Nguyên nhân hay gặp | Cách xử lý |
| --- | --- | --- |
| Mô-tơ im, firmware tin là đang lái | STBY để nổi hoặc ở mức thấp | Kéo STBY lên cao cùng nguồn logic, đúng chân lụa ghi. |
| Xe bò trên pin 7,4 V còn tươi | Sụt của L298N, mô-tơ chỉ thấy khoảng 5,4 V | Dùng TB6612. Đừng nâng pin quá định mức VM của driver để bù. |
| Giắc Dupont nóng ở VM | Jumper tín hiệu đang mang dòng mô-tơ | Đưa dòng pin và mô-tơ sang dây dày hơn. Dupont chỉ còn trên AIN1, AIN2, PWMA, STBY. |
| GPIO chết sau khi cắm HC-SR04 | Echo 5 V vào chân 3,3 V | Thêm mạch chuyển mức hoặc cầu chia echo trước khi cảm biến quay lại. |
| Vỏ không vào nếu không dùng sức | JST-XH, JR, XT30 và XT60 là các họ khác nhau | Dừng. Đúng họ mới cắm. Đừng gọt vai định hướng. |

An toàn: bánh nhấc khỏi bàn dù lab này không quay chúng. Pin tháo. Đừng dò pin khi ngón tay chạm kim loại đầu que. Phép tính 7,4 V làm trên giấy cho đến bài sau, khi đo VM bằng đồng hồ ở thang cao hơn 10 V.

## Bài tập

1. Pin 7,4 V. Lặp phép sụt cho cầu MOSFET 0,3 V và cầu Darlington 2,0 V. Mô-tơ TT thích điện áp nào, và vì sao câu trả lời không phải "mua L298N vì nó cũng 45 000 ₫"?
2. Trang DRV8833 ghi 1,5 A tối đa mỗi kênh. Kẹt vài giây và chip nóng không dám chạm. Bạn đã chạm giới hạn nào, và vì sao "tối đa" không phải kế hoạch chạy liên tục cho hai mô-tơ trên một kênh?
3. Kể ba chân trên module TB6612 mà jumper Dupont được mang, và một mạng nó không nên mang lâu.
4. Một túi có ESP32-WROOM trần và một board NodeMCU-32S. Cái nào hiện cổng serial khi cắm cáp, và chip nào cạnh ổ USB cần được chụp?
5. Dây echo của HC-SR04 rơi vào GPIO của Pico. Dây đó đang muốn ở điện áp nào, VBUS là gì, và món nào trong giỏ phải nằm giữa chúng?

<details>
<summary>Gợi ý đáp án</summary>

1. Cầu MOSFET: $7{,}4 - 0{,}3 = 7{,}1\ \mathrm{V}$. Darlington: $7{,}4 - 2{,}0 = 5{,}4\ \mathrm{V}$. Mô-tơ thích 7,1 V, trong lớp 3 V đến 9 V, nhanh và khoẻ hơn. Cùng giá không có nghĩa cùng điện áp ở đầu cực.
2. Bạn đã chạm giới hạn nhiệt của vỏ nhỏ, và đang ở trần 1,5 A. Tối đa là trần, không phải lúc chạy đều. Một mô-tơ mỗi kênh, và một cú kẹt bị để yên vẫn sẽ nóng. Đừng song song cả hai bánh dẫn động trên một kênh.
3. Dupont hợp AIN1, AIN2, PWMA và STBY. Nó không nên là đường lâu dài cho dòng VM.
4. NodeMCU-32S có USB. Chụp CH340 hoặc CP2102 cạnh ổ cắm. WROOM trần không có chip UART cho đến khi bạn thêm.
5. Echo muốn khoảng 5 V. VBUS là ngõ vào USB 5 V của Pico, không phải GPIO và không phải chỗ để echo rơi vào. Mạch chuyển mức 4 kênh nằm giữa echo và GPIO, mass chung. Cầu chia chỉ trên echo là cách kia.

</details>

## Đọc thêm

Trang carrier TB6612FNG của Pololu nói rõ chip dùng để làm gì, tách khỏi một listing sàn: [Pololu TB6612FNG carrier](https://www.pololu.com/product/713). Trang sản phẩm của phương án nhỏ hơn: [DRV8833](https://www.ti.com/product/DRV8833). Bài mức logic của SparkFun là chuyện 3,3 V với 5 V mà HC-SR04 tạo ra: [Logic levels](https://learn.sparkfun.com/tutorials/logic-levels). Con số GPIO phía sau cảnh báo nằm trong datasheet của Espressif: [ESP32 datasheet](https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf).

## Mua ở Việt Nam

Phần còn lại của robot, gồm khung, pin và đồng hồ, nằm ở [BOM và cách mua bộ kit robot ở Việt Nam]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %}). Giá dưới đây là listing Hshop đọc ngày 23 tháng 9 năm 2026. Xem lại trước khi trả.

Driver mặc định giá 45 000 ₫: [TB6612FNG](https://hshop.vn/mach-dieu-khien-dong-co-dc-tb6612fng-dc-motor-driver), VM 4,5–10 V, logic 2,7–5,5 V, 1,2 A liên tục và 3,2 A đỉnh. Phương án nhỏ hơn giá 25 000 ₫: [DRV8833](https://hshop.vn/mach-dieu-khien-dong-co-drv8833-dc-motor-driver), VM 2,7–10,8 V, 1,5 A tối đa mỗi kênh. L298N cũng 45 000 ₫ và không phải mặc định, vì độ sụt vừa tính: [module L298N](https://hshop.vn/mach-dieu-khien-dong-co-dc-l298).

Mạch chuyển mức cho echo HC-SR04 giá 10 000 ₫: [mạch chuyển mức 4 kênh](https://hshop.vn/mach-chuyen-muc-tin-hieu-logic-4-kenh). Board ESP32 có USB giá 190 000 ₫: [NodeMCU-32S CH340](https://hshop.vn/kit-rf-thu-phat-wifi-ble-esp32-nodemcu-32s-ch340-ai-thinker). Pico trên Hshop là trang tìm kiếm, không phải một slug trong danh sách này: [tìm Raspberry Pi Pico](https://hshop.vn/search?q=raspberry+pi+pico). Ngày 23 tháng 9 năm 2026 trang đó hiện Pico 2 giá 195 000 ₫ và Pico 2 W giá 275 000 ₫. Đọc lại tiêu đề trước khi cho vào giỏ. Mua board có USB, không mua module trần, trừ khi bạn đã có mạch nạp.
