---
layout: post
title: "ESD, cực tính, cầu chì và sụt áp"
chapter: "01"
order: 9
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter01
lesson_type: required
draft: false
---

Ba tai nạn hay bị đổ cho chương trình "bị random". Tĩnh điện làm hỏng chân trước khi bạn nạp code. Pin cắm ngược giết driver trong lúc giắc khớp. Mô-tơ kẹt kéo sụt rail 5 V, ESP32 khởi động lại, log trông như bị ma. Bài này tách ba chuyện đó ra, và kết bằng một giả thuyết bạn sẽ kiểm khi mô-tơ thật sự có mặt.

## Mục tiêu

Bạn cầm board bằng cạnh sau khi đã chạm kim loại nối đất, không diễn kịch tĩnh điện và cũng không nhún vai. Bạn nói được cực ngược giết tụ hóa và giết chân VM của TB6612, và bạn đo cực bằng đồng hồ trước lần cấp nguồn đầu, không tin màu dây. Bạn chọn cầu chì tự phục hồi hoặc cầu chì 2–3 A, cao hơn dòng chạy nhẹ của hai mô-tơ TT và thấp hơn dòng làm khói dây pin. Bạn giải thích sụt áp là rail 5 V dùng chung bị gục khi kẹt rotor, và bạn viết cách xử lý: pin động cơ riêng, chỉ chung mass, tụ 100–470 µF trên VM đúng cực, dây mô-tơ đủ dày, bánh nhắc khỏi mặt bàn, và firmware kéo PWM về 0 nếu nguồn sụt hoặc lệnh im khoảng 300 ms.

## Kiến thức cần có

Vạch cực của tụ hóa ở bài 04 và việc tách VM với VCC ở bài 07 là mặc định. Chỉ cần số học của định luật Ohm. Hôm nay đo rail USB. Không quay bánh, không nối pin động cơ.

## Vì sao bài này quan trọng

Xe capstone là ESP32 hoặc Pico 3,3 V, một TB6612, hai mô-tơ TT, và một HC-SR04. Mô-tơ sẽ bị kẹt: bánh vào lề, tay giữ lốp. Nếu VM hóa ra chính là chân 5 V đang nuôi board, dòng kẹt kéo rail đó xuống, nguồn 3,3 V đi theo, chip reset giữa lệnh. Trông như lỗi logic. Một bản im hơn của cùng sự nhầm là chân echo 5 V của HC-SR04 chĩa vào GPIO mà bài 07 đã cấm. Cả hai đều là chuyện điện. Sửa vòng lặp không hết. Pin động cơ riêng, nối với nguồn logic bằng đúng một sợi mass, mới khiến lần hỏng sau đọc được.

![Rail logic đứng cạnh rail mô-tơ]({{ site.imgurl }}/generated/power_rails_3v3.png)

Hai nguồn chỉ gặp nhau ở mass. Rail 3,3 V nuôi vi điều khiển và chân logic của driver. Rail mô-tơ nuôi VM. USB vẽ chui vào rail mô-tơ là hình sụt áp vẽ trước. HC-SR04 được lấy 5 V cho chính nó; echo vẫn không được vào GPIO.

![Thứ tự cấp nguồn, bánh còn nhấc khỏi bàn]({{ site.imgurl }}/generated/power_order.png)

Logic được phép lên bằng USB. Chuỗi mô-tơ tắt trong buổi này. STBY ở trạng thái nghỉ cho đến khi cả hai rail đã có và chương trình sẵn sàng.

## ESD, vừa đủ

Phóng tĩnh điện là tia lửa thường không thấy. Đi thảm rồi chạm pad Pico trần hoặc cực cổng MOSFET là đủ chọc thủng lớp ôxít. Thói quen thì tẻ và đủ: chạm kim loại nối đất, chẳng hạn vỏ máy tính đang cắm điện, rồi cầm board bằng cạnh; board trần ở trong túi đến khi đã ngồi; đừng chuyền board trần qua phòng. Bỏ màn cọ bóng bay. Đừng nhún vai vì board lần trước còn sống. Module đã hàn cứng hơn transistor rời, và vẫn làm đúng chuỗi ấy. Vòng đeo tay là đồ thêm, không phải điều kiện đạt.

## Cực tính, bây giờ và lúc sau

Cực ngược trên tụ hóa nhôm làm vỏ nóng đến khi xì, và có thể cuốn theo lá đồng. Cực ngược trên VM gây cùng loại hỏng bên trong driver. Vạch trên vỏ là cực âm và nó về mass. Dương của pin vào VM, không bao giờ vào GPIO, và không "thử cho biết".

Diode Schottky nối tiếp trên dây dương, hoặc giắc XT30 chỉ cắm được một chiều, là cải tiến đúng cho lúc sau. Schottky ăn vài phần mười vôn ở dòng mô-tơ, nên đó là một quyết định, không phải phản xạ, và hôm nay chưa gắn trừ khi kit đã có sẵn. Hôm nay đo pin trước khi nó chạm driver: que đỏ vào dây bạn tin là dương, que đen vào dây kia. Số dương nghĩa là tin ấy khớp. Dấu trừ nghĩa là dừng. Hai sợi cùng màu đỏ không phải một hệ cực tính.

HC-SR04 có cực tính nhưng không phải pin. VCC của nó là 5 V, trig là ngõ vào, echo là ngõ ra 5 V. Đảo VCC với GND của cảm biến là cắm ngược một board nhỏ. Đưa echo vào GPIO là lệnh cấm của bài 07. Kiểm cả hai trên tờ sơ đồ chân trước khi cắm cảm biến.

## Con số khiến USB không nuôi được mô-tơ

Listing mô-tơ TT 1:48 mà khóa này mua ghi không tải khoảng 110–150 mA. Hai mô-tơ, bánh trên không, kéo khoảng

$$
2 \times 130\,\mathrm{mA} \approx 0{,}26\,\mathrm{A}
$$

Gọi tròn $$0{,}3\,\mathrm{A}$$. Cổng USB thường được tính 500 mA, nên lúc chạy nhẹ trông như còn chỗ:

$$
0{,}50 - 0{,}30 = 0{,}20\,\mathrm{A}
$$

phần dư ảo. Dòng kẹt cao hơn nhiều. Đừng bịa một ampe kẹt bạn chưa đo. Hãy ghi dòng kẹt gấp vài lần không tải, một mô-tơ TT kẹt đã xin hơn một cổng 500 mA. USB không được làm nguồn mô-tơ. Mức 1,2 A liên tục của TB6612 là trần của chip, không phải nguồn phát ra dòng. Nguồn là pin trên VM.

## Sụt áp, và cách sửa bạn sẽ dựng

Rail 5 V dùng chung có điện trở của cáp và của giắc. Dòng kẹt đi qua điện trở ấy là một cú sụt:

$$
\Delta V = I_{\mathrm{ket}} \times R_{\mathrm{duong}}
$$

Chưa cần đo dòng kẹt cũng thấy hình dạng sự cố. Chân 5 V tụt thì nguồn tạo 3,3 V hết khoảng dư, ESP32 reset, chương trình chạy lại giữa lệnh. Pico cũng sụt cùng kiểu. Banner khởi động hiện ra chỗ bạn chờ một báo tốc độ: đó chính là lỗi này.

Phần cứng, theo thứ tự nên thiết kế:

Mô-tơ có pin riêng, trong cửa sổ VM 4,5–10 V của bài 07. Logic tạm ở trên USB. Hai nguồn chung đúng một sợi mass, không chung gì khác. Đừng bắt sợi mass ấy gánh dòng mô-tơ dọc một rail breadboard mỏng.

Tụ hóa nhôm 100–470 µF mắc ngang VM, sát driver, chịu 16 V hoặc 25 V dưới trần 10 V ấy. Vạch là cực âm và về mass. Cắm ngược là cú xì của mục trước, lần này trên rail mô-tơ. Tụ gánh sườn dốc của cú kẹt để dây pin không phải gánh một mình.

Dây mô-tơ dày hơn dây tín hiệu. Bánh nhắc lên mỗi khi mô-tơ đã nối mà bạn không cố ý cho xe chạy. Bánh nằm trên bàn là một cú kẹt do bạn tạo.

Firmware, khi đã có, kéo PWM về 0 nếu nguồn sụt, và cũng kéo về 0 nếu lệnh im khoảng 300 ms. Khoảng đó đủ dài để bỏ một gói đến muộn, và đủ ngắn để bên gửi chết không để tốc độ cuối cùng nằm trên bánh. STBY cũng được phép thả. Bài 07 đòi STBY cao mới có chuyển động; bài này đòi một đường trở về trạng thái tắt.

## Cầu chì

Cầu chì tự phục hồi hoặc cầu chì 2–3 A trên dây pin là bảo hiểm rẻ. Chọn cao hơn dòng chạy nhẹ, khoảng $$0{,}3\,\mathrm{A}$$, để lúc chạy bình thường không đứt, và thấp hơn dòng làm khói dây pin. Ngắn mạch chết có thể hàng chục ampe; cầu chì để dành cho việc đó, không phải cho một cú kẹt nhẹ. Cầu chì dưới $$0{,}3\,\mathrm{A}$$ là chọn sai. Nó không thay pin riêng và không biết cực. Đặt trên dây dương, sát pin, và vẫn đo cực.

## Thực hành

Chỉ USB. Mô-tơ rút. Pin rút. Bánh đã gắn trên trục thì vẫn để trên không.

1. Chạm kim loại nối đất, rồi cầm board bằng cạnh. Ghi là đã làm.
2. Chỉ cắm USB. Đo DC, que đen ở mass. Ghi chân 5 V, rồi chân 3,3 V. Ghi số, không ghi chữ "ổn".
3. Từ tờ bài 07, hoặc phác bốn chân nếu chưa có cảm biến, khoanh Echo của HC-SR04 và ghi lệnh cấm: ngõ ra 5 V, không phải GPIO.
4. Viết giả thuyết cho chương 02 theo khung này, điền số của bạn: "Chỉ USB, board đo được ___ V ở 5 V và ___ V ở 3,3 V. Nếu sau này reset khi mô-tơ TT dùng chung rail 5 V đó, giả thuyết là dòng kẹt kéo rail vào vùng sụt áp. Cách xử lý: pin động cơ riêng, chỉ chung mass, tụ 100–470 µF trên VM vạch về mass, dây mô-tơ dày, bánh nhắc, PWM bị kéo về 0 nếu rail sụt hoặc lệnh im khoảng 300 ms. Cầu chì 2–3 A trên dây pin."
5. Đừng nối mô-tơ để thử đoạn văn. Đạt khi có hai điện áp và đoạn văn ấy, lưu `ch01-09-brownout`.

Chân 5 V đã lệch xa 5 V khi chỉ có USB thì dừng và ghi lại. Board đang bệnh không cần mô-tơ để giải thích một lần reset.

## Ví dụ

Hai mô-tơ TT 1:48 ở giữa dải không tải:

$$
I_{\mathrm{chay}} = 2 \times 0{,}130 = 0{,}26\,\mathrm{A}
$$

USB là $$0{,}50\,\mathrm{A}$$. Phần dư khi bánh trên không khoảng $$0{,}24\,\mathrm{A}$$, và đó là toàn bộ sự tự tin sai. Dòng kẹt $$\gg 0{,}3\,\mathrm{A}$$, một mô-tơ kẹt đã là đòi hỏi quá đáng với cổng 500 mA. Vẽ lại: USB cho ESP32 hoặc Pico và cho logic TB6612 ở 3,3 V; pin riêng trong 4,5–10 V trên VM; một điểm mass; tụ 220 µF hoặc 470 µF, vạch về mass; cầu chì 2 A hoặc 3 A trên dây dương. Sổ đã ghi PWM về 0 nếu lệnh im khoảng 300 ms.

Cầu chì 0,5 A "để khỏi kẹt" nằm đúng trên dòng chạy nhẹ và sẽ đứt lúc chạy bình thường. Người ta sẽ nối tắt cầu chì. Chọn 2 A hoặc 3 A, và để thời gian chờ xử lý lúc kẹt.

## Bài tập

1. Hai mô-tơ không tải 150 mA, USB 500 mA. Tính tổng lúc chạy nhẹ và phần còn lại. Vì sao phần còn lại không có nghĩa USB được nuôi VM khi bánh chạm đất?
2. Chân 5 V đo 4,95 V, chân 3,3 V đo 3,28 V khi chỉ có USB. Ở chương 02, serial in banner khởi động mỗi lần cả hai mô-tơ cắm vào chính chân 5 V đó. Viết một câu giả thuyết, và nói đổi nguồn nào để kiểm.
3. Tụ 470 µF trên VM có vạch hướng ra xa mass. Cái gì hỏng, và chân nào phải đổi?
4. Laptop ngủ, lệnh dừng, PWM cuối là "hai bánh tiến". Firmware phải làm gì trong khoảng 300 ms, và vì sao cầu chì 3 A không thay dòng code đó?
5. Echo của HC-SR04 nối vào chân GP của Pico "vì cảm biến chạy 5 V và Pico có chân 5 V ngay cạnh". Con số nào ở bài 07 cấm việc đó, và bước kiểm nào hôm nay bắt được việc đảo VCC với GND của cảm biến?

<details markdown="1">
<summary>Gợi ý đáp án</summary>

1. $$2 \times 0{,}150 = 0{,}30\,\mathrm{A}$$, còn khoảng $$0{,}20\,\mathrm{A}$$ trên cổng 500 mA. Dòng kẹt cao hơn không tải rất nhiều và không nhét vào phần dư ấy. USB không vào VM.
2. Giả thuyết: dòng mô-tơ kéo sụt rail 5 V dùng chung và rail 3,3 V đi theo vào vùng reset. Phép thử là chuyển mô-tơ sang pin riêng, giữ một mass chung, rồi xem banner còn hiện trên cùng lệnh ấy không.
3. Tụ hóa nhôm cắm ngược trên pin có thể xì. Vạch là cực âm và phải về mass. Đổi chân đó, đừng cấp nguồn để "xem nó xì".
4. Firmware đặt PWM về 0, và có thể thả STBY, khoảng 300 ms sau khi lệnh im. Cầu chì 3 A không đứt ở dòng mô-tơ bình thường, nên bánh giữ lệnh cuối cho đến khi có thứ khác dừng chúng.
5. Điện áp cực đại của GPIO, ở rail 3,3 V chứ không phải 5 V, cấm echo trên chân GP. Đo VCC của cảm biến so với GND trước khi cắm sẽ bắt nguồn cảm biến bị đảo. Chân 5 V cạnh đó là chân nguồn, không phải ngõ vào logic.

</details>

## Đọc thêm

- [SparkFun: mức logic](https://learn.sparkfun.com/tutorials/logic-levels) — vì sao echo 5 V và GPIO 3,3 V không phải cùng một mức "cao", tức hàng rào datasheet của bài 07 viết bằng lời thường.
- [Battery University, BU-409](https://batteryuniversity.com/article/bu-409-charging-lithium-ion) — giới hạn sạc của bộ pin lithium có thể đặt lên VM sau này. Đọc trước khi tự nghĩ ra bộ sạc.
- [Module TB6612FNG của Pololu](https://www.pololu.com/product/713) — nguồn logic và nguồn mô-tơ là hai chân khác nhau, nửa phần cứng của cách chống sụt áp.

## Mua ở Việt Nam

Pin động cơ, mô-tơ TT, driver và HC-SR04 nằm trong kit ở chương 00, bài 05, [BOM và cách mua bộ kit robot ở Việt Nam]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %}). Đừng mua thêm một bộ từ trang này.

Buổi lab cần đồng hồ nếu bạn chưa có. Listing UNI-T UT33D ở [Hshop](https://hshop.vn/dong-ho-van-nang-dien-tu-digital-multimeter-uni-t-ut33d-chinh-hang); đọc giá đang bán, bài này không chốt một số. Khi nào dựng tụ VM, chứ chưa phải hôm nay, tụ hóa 100–470 µF, 16 V hoặc 25 V, tìm ở [Hshop](https://hshop.vn/), [Thế Giới IC](https://www.thegioiic.com/) và [IC Đầy Rồi](https://icdayroi.com/). Trang này không bịa slug tụ. Xem điện áp ghi trên vỏ và vạch chỉ chân nào trước khi hàn.
