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

Bạn gọi được tên, trên chính board của mình, chân USB 5 V và chân 3,3 V đã ổn áp, rồi đo cả hai khi chỉ có USB. Bạn coi mọi GPIO của ESP32 và Pico là chân 3,3 V mà 5 V có thể giết. Bạn đặt pin 2S lên chân VM của TB6612 trong một bản vẽ, và liệt kê các chân header mà pin đó không bao giờ được chạm. Bạn đổi mức echo của HC-SR04 trên giấy, có mass chung, trước khi bất kỳ cảm biến nào được đi dây. Cả lab, pin không được nối.

## Cần gì trước khi học

Lab nhịp tim đã chứng minh board được máy tính nhận và bạn biết chân LED của mình. Bạn chỉnh được đồng hồ về điện áp một chiều và đặt que đen lên một mass gọi được tên. Mạch chia áp của chương 01 là phần toán mạch duy nhất. Nguồn motor chưa nối. Giỏ đầy đủ, gồm driver và pin, là bài mua sắm chương 00 ([Hóa đơn linh kiện và cách mua]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %})). Bạn không mua pin để xong trang này.

## Vì sao bài này gắn với Capstone A

Firmware teleop chương 07 hỏng theo những kiểu không giống một câu `if` sai. Echo siêu âm 5 V rơi vào GPIO 3,3 V. Dây hồi của motor không chung mass với logic, nên chân “PWM” nổi so với driver và TB6612 đọc ra vô nghĩa. Pin 7,4 V bị kẹp vào chân ghi 5V hoặc 3V3 vì nhãn trông rộng rãi. Chip reset, hoặc một chân chết, ngay lần đầu robot được bảo chạy. Thời gian chờ khoảng 300 ms và quy tắc bánh nhấc lên vẫn quan trọng, và chúng không cứu được một chân đã nhìn thấy pin. Tấm thẻ bạn vẽ ở đây là bản đồ bạn sẽ cầm khi driver ở chương 05 và PWM ở chương 07 cuối cùng được phép. Wi-Fi ở chương 08 không làm GPIO cứng hơn.

## Hai ray, và một ray thứ ba không nằm trên header này

Chân GPIO của ESP32 và Pico là logic 3,3 V. Năm vôn trên một GPIO có thể giết chân. Trên ESP32, cực đại tuyệt đối chỉ hơn ray một khoảng sụt diode:

$$
V_{DD} + 0{,}3\,\mathrm{V} = 3{,}3\,\mathrm{V} + 0{,}3\,\mathrm{V} = 3{,}6\,\mathrm{V}.
$$

Giới hạn của Pico cùng kiểu, chỉ nhỉnh hơn 3,3 V vài phần mười. Năm vôn vượt cả hai giới hạn.

Một quy tắc đọc kiểu học tập, tách khỏi vạch hỏng đó, nói mức cao nên ít nhất khoảng $$0{,}7 \times 3{,}3\,\mathrm{V} \approx 2{,}3\,\mathrm{V}$$ trước khi bạn tin. $$V_{IL}$$ và $$V_{IH}$$ thật nằm trong datasheet. Quy tắc vận hành đơn giản hơn cả hai công thức: đừng nuôi GPIO từ một chân 5 V.

Trên dev board ESP32 cổ điển, chân ghi 5V hoặc VIN là USB 5 V, thường qua một diode Schottky, nên header ngồi thấp hơn 5 V của laptop vài phần mười vôn. Nó nuôi được một cảm biến nhỏ khi bạn còn trên bàn. Nó không nuôi được động cơ TT. Dòng không tải của một động cơ TT trên listing của môn đã khoảng 110 mA đến 150 mA, và lúc kẹt thì lớn hơn nhiều lần. Hai motor cộng một đỉnh Wi-Fi làm sập cổng USB. Sự từ chối đến dưới dạng mất kết nối hoặc reset brownout, cùng banner lặp mà bạn đã học ở lab nhịp tim. Chân ghi 3V3 là ngõ ra của ổn áp. Nó nuôi module. Motor không thuộc về nó.

Pico gọi cùng các ý đó thẳng hơn. VBUS là USB 5 V và có mặt khi cáp đang cắm. VSYS là ngõ vào hệ thống. USB tới VSYS qua một diode, và một nguồn ngoài đặt thẳng lên VSYS bị giới hạn khoảng 1,8 V đến 5,5 V. 3V3 là ray đã ổn áp và nó là ngõ ra. Đừng đưa 7,4 V vào 3V3. Đừng đưa 7,4 V vào VSYS. Cả hai đều ngoài việc những chân đó được làm ra để nhận, và 7,4 V trên 3V3 là một cú đánh thẳng vào ngõ ra ổn áp.

![USB 5 V, 3,3 V đã ổn áp, và ray motor nằm ngoài header]({{ site.imgurl }}/generated/power_rails_3v3.png)

Đọc hình như một lời hứa về dòng, không chỉ về áp. Ray 5 V đến từ USB và có thể mượn nhẹ. Ray 3,3 V dành cho logic. Mass là chung. Ray motor không phải một trong hai chân đó.

![Giải phẫu board: que đo đặt lên header, không đặt lên module]({{ site.imgurl }}/generated/pcb_mcu_anatomy.png)

Cổng USB giải thích VBUS hoặc chân 5V của dev board. Ổn áp giải thích 3V3. Đồng hồ đặt lên header. Vỏ kim loại không phải điểm đo.

Mass chung với driver là bắt buộc. TB6612 đo PWM của bạn so với mass logic của chính nó. Nếu mass đó không phải mass của vi điều khiển, driver không thấy mức cao đáng tin, dù điện áp GPIO trông đúng trên một đồng hồ đang tham chiếu sai chỗ. Khi driver tới, chân GND của nó buộc vào một chân GND trên ESP32 hoặc Pico. Nguồn motor thì không.

## Chân echo

Ngõ ra echo của HC-SR04 là một xung 5 V. Xung đó phải được đổi mức trước khi tới ngõ vào ESP32 hoặc Pico. Module chuyển mức là dụng cụ chắc: phía điện áp thấp là 3V3 của board, phía điện áp cao là 5 V của cảm biến, và các mass buộc vào nhau. Echo đi từ phía cao sang phía thấp rồi vào GPIO. Nhiều module nhận mức cao 3,3 V trên chân trigger. Đó là tính chất ngõ vào của cảm biến, và không phải giấy phép bỏ qua việc dịch echo. Bạn sẽ xác nhận trigger ở chương cảm biến. Hôm nay không khám phá điều đó bằng cách hy sinh một GPIO.

Mạch chia điện trở là phép tính cho thấy vì sao echo 5 V thô là trái phép. Với $$1\,\mathrm{k}\Omega$$ từ echo tới nút GPIO và $$2\,\mathrm{k}\Omega$$ từ nút đó xuống GND:

$$
V_{\mathrm{GPIO}} = 5\,\mathrm{V} \times \frac{2}{1 + 2} \approx 3{,}33\,\mathrm{V}.
$$

Nó ngồi gần đỉnh vùng được phép, nên shifter dễ chịu hơn khi robot phải chạy ổn. Dung sai và cáp dài làm nút đó dịch. Lab này không lắp cảm biến. Viết phân số lên thẻ chân để lần đi dây sau có một con số đi kèm.

## Ví dụ đã làm

Một bộ pin 2S bằng cell 18650 ngồi gần 7,4 V danh định, đầy thì cao hơn, yếu thì thấp hơn. Hà vẽ chỗ đáp hợp pháp duy nhất của dây đỏ: cực VM của TB6612. Module kiểu Hshop trong ghi chú chương 00 nhận nguồn motor trong dải có chứa 7,4 V. Dây đen đáp vào GND của driver, và một sợi riêng nối GND đó với GND của vi điều khiển.

Dây dương của pin có một danh sách chân không bao giờ được chạm. Trên header ESP32: mọi GPIO, chân 3V3, và chân 5V/VIN. Chân 5V đó là USB 5 V. Pin 2S ở đó có thể đẩy ngược vào laptop. Trên Pico: mọi chân GP, 3V3, VSYS, và VBUS. Cửa sổ cho phép của VSYS khoảng 1,8 V đến 5,5 V, và 7,4 V nằm ngoài. 3V3 là ngõ ra trên cả hai board. VCC logic của driver, chân nhỏ chờ 3,3 V hoặc 5 V, không phải VM. Hà viết “chỉ VM” cạnh pin và “VCC logic lấy từ 3V3, không lấy từ pin” cạnh driver.

Không có sợi nào được nối. Bản vẽ là ví dụ đã làm. Phần đồng hồ là một việc khác, nhỏ hơn: chỉ USB.

## Lab

Chỉ cáp USB. Pin rút, driver rút, cảm biến rút.

1. Que đỏ ở lỗ đo áp, que đen trên một chân GND gọi được tên, đồng hồ ở điện áp một chiều.
2. Đo ray 5 V: chân dev board ghi 5V hoặc VIN, hoặc VBUS của Pico. Viết con số.
3. Đo 3,3 V: chân ghi 3V3, hoặc 3V3(OUT) của Pico. Viết con số.
4. Vẽ thẻ chân: hai ray đó, GND, chân LED của nhịp tim, một GPIO trống đã đối chiếu silk, và một danh sách cấm. Danh sách cấm gồm “5 V không bao giờ lên GPIO” và câu “pin 2S chỉ chạm VM và GND của driver.”
5. Trên cùng thẻ, phác echo HC-SR04 qua mạch chuyển mức hoặc mạch chia 1 kΩ / 2 kΩ. Không nối cảm biến.

Bạn sẽ đọc khoảng 4,7 V đến 5,1 V trên ray USB và khoảng 3,25 V đến 3,35 V trên 3,3 V. Chân 5V của ESP32 bị trừ qua diode, gần 4,7 V đến 4,9 V, vẫn là ray USB khỏe. Viết con số, đừng làm tròn thành “5 V.” Số đọc 3,3 V ngoài cửa sổ đó là dừng. Số đọc trên 3,6 V ở 3V3 có nghĩa 5 V đang rò vào: rút và tìm. Lab này không nối pin, kể cả để “xem VM sẽ là bao nhiêu.”

![Thứ tự nối: mass chung, logic, tín hiệu, nguồn motor sau cùng, bánh nhấc]({{ site.imgurl }}/generated/power_order.png)

Hình là thứ tự mà thẻ đang giữ. Bạn vẫn ở bước USB. Nguồn motor là khối cuối, và bánh được nhấc khi việc đó cuối cùng thành hợp pháp.

Các lỗi. Que đen trên chân 5V và que đỏ trên GND cho số âm hoặc một số không khó hiểu. Đổi que và gọi lại tên GND. Đo lên vỏ kim loại, hoặc lên một tụ, không phải đo ray. Số 0 V trên 3V3 trong khi USB còn sống là sai chân, thiếu mass, hoặc ổn áp chết. Dừng. Bạn nào nuôi động cơ TT từ chân 5V sẽ làm brownout board ngay lúc motor kẹt. Chân đó là USB 5 V.

An toàn: pin ở trong túi. Đừng mắc đồng hồ ở chế độ đo dòng nối tắt giữa 5V và GND. Đó là một mạch ngắn qua đồng hồ.

## Bài tập

1. Tính ngõ ra mạch chia cho 5 V với $$1\,\mathrm{k}\Omega$$ phía trên và $$2\,\mathrm{k}\Omega$$ phía dưới. Nếu cả hai điện trở cao thêm 5 phần trăm, tỉ số có đổi không?
2. Cực nào của pin 2S 7,4 V được chạm TB6612, và những chân header ESP32 nào pin đó không bao giờ được chạm?
3. Trên bàn có một Pico. Nhãn nào là USB 5 V, nhãn nào nhận khoảng 1,8 V đến 5,5 V, và nhãn nào là ngõ ra đã ổn áp? 7,4 V gây hỏng ngay nhất ở đâu?
4. Đồng hồ đọc 4,86 V và 3,29 V, chỉ USB. Có nằm trong cửa sổ không? Thẻ chân vẫn cần câu nào về VM?
5. Echo của HC-SR04 bị đi thẳng vào GPIO 18 “chỉ để xem.” Điện áp nào đập vào chân, và món nào phải đứng trên sợi dây đó?

<details>
<summary>Đáp án</summary>

1. $$5 \times 2 / 3 \approx 3{,}33\,\mathrm{V}$$. Nếu cả hai điện trở nhân 1,05 thì tỉ số không đổi, nên nút lý tưởng vẫn khoảng 3,33 V. Sai số không đều thì không triệt. Đó là một lý do shifter dễ chịu hơn mạch chia ráp từ điện trở thừa.
2. Dương pin được chạm VM. Âm pin chạm GND driver, và GND đó phải chung với vi điều khiển. Pin không được chạm bất kỳ GPIO nào của ESP32, không chạm 3V3, không chạm chân 5V/VIN.
3. VBUS là USB 5 V. VSYS là ngõ vào nhận khoảng 1,8 V đến 5,5 V, USB tới qua diode. 3V3 là ngõ ra đã ổn áp. 7,4 V trên 3V3 đánh thẳng ngõ ra ổn áp. 7,4 V trên VSYS cũng ngoài cửa sổ cho phép.
4. 4,86 V nằm trong khoảng 4,7 V đến 5,1 V, và 3,29 V nằm trong khoảng 3,25 V đến 3,35 V. Thẻ vẫn cần một câu rõ: pin 2S chỉ chạm VM và mass driver, và pin đã không được nối trong lần đo.
5. Chân echo đẩy khoảng 5 V vào GPIO 3,3 V, trên vùng cực đại tuyệt đối cỡ 3,6 V. Một mạch chuyển mức (hoặc, như một thỏa hiệp đã tính, mạch chia) phải đứng trên sợi đó, mass buộc chung. Rút echo trước mọi thí nghiệm tiếp.

</details>

## Đọc thêm

- [Logic levels của SparkFun](https://learn.sparkfun.com/tutorials/logic-levels) — vì sao mức cao 5 V và ngõ vào 3,3 V cần mạch dịch.
- [Datasheet Pico](https://datasheets.raspberrypi.com/pico/pico-datasheet.pdf) — VBUS, VSYS, 3V3, và cửa sổ VSYS được phép.
- [Datasheet ESP32 (PDF)](https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf) — đặc tính điện của GPIO và mức cực đại tuyệt đối.
