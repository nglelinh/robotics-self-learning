---
layout: post
title: "Breadboard, đồng hồ vạn năng và cách đo an toàn"
chapter: "01"
order: 2
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter01
lesson_type: required
draft: false
---

## Mục tiêu

Học xong, bạn chỉ được dải năm lỗ, rãnh giữa, và thanh nguồn, rồi nói lỗ nào thực sự là một dây. Bạn đoán trước rằng nhiều breadboard cỡ lớn ngắt mỗi thanh nguồn ở giữa, và chứng minh chỗ ngắt bằng tiếng bíp thông mạch chứ không bằng trí nhớ. Bạn đo điện áp một chiều song song với linh kiện, từ chối đo dòng qua củ sạc USB trong bài này, và chỉ đo điện trở khi mạch đã cắt nguồn. Mỗi lần đo áp bạn bắt đầu ở thang cao hơn điện áp mình đang chờ, ngón tay không chạm đầu que.

## Cần có gì trước

Bạn đã gọi được tên vôn và ampe, và nhớ LED báo trạng thái phải có điện trở nối tiếp. Bài này không chứng minh lại định luật Ohm. Nó dạy hình học của bàn thí nghiệm: lỗ nào là một nút, và thang nào của đồng hồ đang nhìn điện áp chứ không phải đang nối tắt thứ bạn tưởng mình đang đo. Một đồng hồ số và một breadboard không hàn là đủ.

## Vì sao xe hai bánh kẹt ở chỗ này

Trên đồ án, ESP32 hoặc Pico, TB6612, và dây mô-tơ TT gặp nhau trên breadboard hoặc trên chân Dupont theo một luật: năm lỗ trong một cột là một nút, rãnh giữa là bức tường. Thanh nguồn đứt ở giữa, jumper trông đã cắm nhưng trượt lò xo, hoặc que đỏ còn nằm ở ổ đo dòng, đều trông như robot chết trong khi chip chưa hề có điện.

Logic của TB6612 là 3,3 V lấy từ vi điều khiển, còn VM là nguồn mô-tơ riêng. Nếu bạn "chữa" cầu H im lặng bằng cách nhảy 5 V vào GPIO, một lỗi đo thành chân hỏng. Echo của HC-SR04 là ngõ ra 5 V; chọc que bừa không phải cách an toàn để phát hiện điều đó. Bài này là tiếng bíp và lần đo áp, làm khi xe vẫn còn là linh kiện trong khay.

## Breadboard thực sự nối thế nào

Breadboard không hàn là lưới kẹp lò xo dưới lớp nhựa màu. Chân cắm vào một lỗ được nối với mọi lỗ khác trên cùng mảnh kẹp. Mối đó không kín khí. Chân quá ngắn hoặc bẩn có thể trông đã vào lỗ mà vẫn hở, nên đồng hồ mới là thứ quyết định nút có tồn tại hay không.

Hai hàng dài ở mép là thanh nguồn, thường kẻ đỏ và xanh hoặc đen. Mọi lỗ dọc một vạch màu không đứt là cùng một dây dẫn. Thanh đỏ phía trên không phải thanh đỏ phía dưới. Trên nhiều board cỡ lớn, kể cả loại 830 lỗ thông dụng, kẹp còn dừng ở một khe giữa, và vạch màu được in đứt đúng chỗ đó. Cấp 5 V vào đầu trái thì đầu phải vẫn tối cho đến khi bạn nhảy dây qua khe. Board mini đôi khi không có khe. Đừng nhớ theo nhãn hiệu. Hãy đo cái bạn đang cầm.

![Cấu tạo breadboard: thanh nguồn, dải năm lỗ, rãnh giữa]({{ site.imgurl }}/generated/breadboard_anatomy.png)

Phần giữa là các dải đầu cuối. Mỗi cột có năm lỗ phía trên rãnh và năm lỗ phía dưới. Năm lỗ đó nối dọc với nhau. Cột bên cạnh là một mạng khác. Rãnh chạy dọc giữa board là chất cách điện: lỗ bên này không thông lỗ cùng số cột bên kia. Khe ấy để chip DIP ngồi dạng cưỡi ngựa mà các chân của chính nó không chập vào nhau. Dò "hai bên cùng một cột" rồi chờ tiếng bíp là đang bắt rãnh biến thành dây.

Cắm cả hai chân LED vào cùng một cột năm lỗ là nối tắt LED. Cắm hai bên rãnh mà không có dây nối sang là hở mạch. Cả hai lỗi đều trông gọn.

![Breadboard không hàn, thanh nguồn chạy dọc mép]({{ site.imgurl }}/wikimedia/breadboard.jpg)

## Vặn núm đồng hồ là đang hỏi điều gì

Ba thói quen chặn gần như mọi cầu chì cháy trong lab sinh viên. Que đen luôn ở ổ COM. Que đỏ ở ổ ghi V, Ω, hoặc ký hiệu tương đương khi đo áp, đo trở, hoặc thông mạch. Que đỏ chỉ chuyển sang ổ đo dòng lúc thực sự đo dòng, và phải cắm trả lại khi xong. Để que ở ổ dòng rồi "đo điện áp" là đặt shunt của đồng hồ thẳng lên nguồn. Đó gần như một ngắn mạch. Cầu chì mA đứt. Thang vôn sau đó vẫn chạy, nên hỏng bị giấu đến ngày bạn cần đo dòng.

![Đồng hồ vạn năng số: núm, màn hình, ổ que đo]({{ site.imgurl }}/wikimedia/Digital_Multimeter_Aka.jpg)

Điện áp một chiều đo song song. Mạch vẫn nối. Bạn chạm hai điểm cần hiệu điện thế. Đảo que trên đồng hồ số chỉ ra dấu trừ, không làm hỏng linh kiện. Núm để thang DC cao hơn điện áp đang chờ: thang 20 V phủ USB 5 V và pin 2S gần 8,4 V. Đồng hồ tự chọn thang vẫn cần bạn chọn ký hiệu vôn một chiều, không phải ôm. Bạn đang nhìn ngang linh kiện, không chen vào đường dòng.

Dòng điện đo nối tiếp. Bạn ngắt một dây để dòng chạy qua đồng hồ, và chỉ sau khi que đỏ đã ở ổ dòng. Bài này không đo dòng trên củ sạc USB và không đo dòng trên GPIO. Củ sạc sẽ cố đẩy một ampe hoặc hơn vào đồng hồ nếu bạn kẹp ngang ngõ ra của nó, và dòng kẹt của mô-tơ TT có thể đứt cầu chì mA rẻ trong một cái giật. Đo trở và thông mạch chỉ làm khi mạch mất nguồn, vì đồng hồ tự cấp một điện áp thử nhỏ. Thông mạch bíp khi gặp dây hoặc lò xo khép. Điện trở 180 Ω thường im trên thang thông mạch: thang này nghĩa là "gần như ngắn", không phải "có nối gì đó". Muốn con số thì chuyển sang ôm.

## Ví dụ tính: thanh nguồn trông có điện mà không có

Một củ sạc USB được nhảy vào thanh đỏ và thanh xanh bên trái của board 830 lỗ. Không cắm gì khác. Không ESP32, không GPIO. Đồng hồ ở thang 20 V DC, đen ở COM, đỏ ở ổ điện áp.

Trên thanh đỏ bên trái, so với thanh xanh bên trái, đồng hồ đọc 5,08 V. Đó là củ sạc khỏe, cao hơn 5 V trên nhãn một chút, bình thường. Đưa que đỏ sang thanh đỏ bên phải, qua chỗ vạch màu bị in đứt, que đen vẫn ở thanh xanh trái. Đồng hồ đọc 0,02 V. Đó không phải "hao một chút trên dây". Đó là hở mạch. Rút sạc, cắt hết nguồn, chuyển sang thông mạch. Dò dọc thanh đỏ qua khe giữa thì im. Một jumper ngắn qua khe đỏ, một jumper qua khe xanh, rồi cắm lại sạc: thanh bên phải đọc 5,07 V.

Ổ đo dòng gần như một dây ngắn, nên bài lab không bao giờ dùng ổ đó trên củ sạc này. Hình dung thô một shunt 10 A, cỡ một phần trăm ôm, cho

$$
I \approx \frac{5}{0.01} = 500\ \mathrm{A}
$$

trong một thế giới mà củ sạc cấp nổi dòng ấy. Củ sạc thật gập về khoảng một đến hai ampe, đủ đứt cầu chì 200 mA, và đó không phải phép đo "robot cần bao nhiêu dòng". Bài trước đã nói hai mô-tơ TT kẹt mỗi cái cỡ một ampe. Bạn sẽ đo việc đó sau, nối tiếp, trên nguồn mô-tơ, trong một xung ngắn, que đỏ ở ổ chịu nổi dòng đó. Không học nó bằng cách ngắn cổng USB.

## Thực hành

1. Rút mọi nguồn. Que đen vào COM, que đỏ vào ổ điện áp/ôm. Vặn sang thông mạch.
2. Bíp một jumper từ đầu kim loại này sang đầu kia. Phải có tiếng. Cắm một đầu vào thanh đỏ, đầu kia vào một hàng năm lỗ. Bíp từ một lỗ khác của hàng đó về một lỗ khác trên thanh: có tiếng. Bíp sang hàng bên cạnh: im.
3. Bíp qua rãnh giữa, cùng số cột. Mong đợi sự im lặng. Rãnh không phải dây.
4. Tìm chỗ đứt thanh nguồn. Bíp từ nửa trái của thanh đỏ sang nửa phải. Board 830 lỗ điển hình sẽ im, và vạch màu in có khe. Nhảy một dây qua khe rồi bíp lại. Phải có tiếng. Làm tương tự với thanh xanh.
5. Chỉ khi đó mới đo áp. Dùng củ sạc điện thoại hoặc pin dự phòng, không dùng GPIO và không dùng chân 3V3. Nếu có mạch tách USB thì đưa 5 V và GND vào thanh bạn vừa chứng minh. Nếu đo đầu dây rời, chỉ đo đầu củ sạc mà bạn hiểu, đỏ trên 5 V và đen trên GND. Núm ở thang DC cao hơn 5 V, thường là 20 V. Đọc màn hình.

Bạn sẽ nghe bíp qua jumper tốt và trong một hàng, im qua rãnh, và im qua giữa thanh nguồn cho đến khi có cầu nối. Số của củ sạc nên gần 4,7 V đến 5,3 V. Đọc gần 0 V trong khi thông mạch đã bíp nghĩa là bạn không đứng trên thanh mình tưởng, hoặc củ sạc không phải nguồn mình tưởng.

| Bạn thấy | Nguyên nhân hay gặp | Cách xử lý |
| --- | --- | --- |
| Không bíp dù jumper trông đã cắm | Chân trượt lò xo, hoặc kẹp đó bị bẹt | Đổi sang lỗ khác cùng cột. Cả cột chết thì bỏ cột đó. |
| Thanh trái khoảng 5 V, thanh phải khoảng 0 V | Khe giữa đang hở | Thêm một jumper qua khe đỏ và một qua khe xanh, đo lại. |
| Thông mạch bíp trong khi sạc còn cắm | Bạn đo ôm hoặc thông mạch trên mạch đang có điện | Rút nguồn trước. Mạch đo ôm không phải đồng hồ vôn. |
| Màn hình loé, sau đó mọi số mA là 0 còn thang 20 V vẫn thấy sạc | Que đỏ ở ổ dòng và bị kẹp ngang củ sạc | Cầu chì mA đã đứt. Đừng ngắn lại lần nữa để "xác nhận". |

An toàn: bắt đầu ở thang áp cao hơn cái bạn chờ, để pin 2S gần 8 V không bị gặp trước tiên ở thang 200 mV. Ngón tay rời đầu que khi đo pin hoặc củ sạc; chỉ phần kim loại đầu que được chạm mạch. Bài này không đo dòng trên USB. Đừng cắm củ sạc vào GPIO của ESP32 hoặc Pico để "xem 5 V có ở đó không".

## Bài tập

1. Board có 30 cột mỗi bên rãnh, và cả cặp thanh nguồn trên lẫn dưới đều bị tách một lần ở giữa. Có bao nhiêu nút năm lỗ trong vùng giữa? Có bao nhiêu đoạn thanh nguồn riêng?
2. Bạn muốn điện áp trên điện trở 180 Ω đang thắp LED từ 3,3 V. Que cắm ổ nào, núm ở đâu, có được tháo LED không?
3. Jumper bíp từ đầu này sang đầu kia và đo khoảng 0,3 Ω. Cắm vào một lỗ thì lỗ đó không bíp tới đầu kia của dây. Chỗ hở nằm đâu?
4. Một bạn "đo dòng USB" bằng cách kẹp đồng hồ ngang 5 V và GND, thấy loé sáng, rồi thang mA ra 0 trong khi thang 20 V vẫn hiện củ sạc. Cái gì hỏng?
5. Vì sao tiếng bíp ở thang thông mạch không đủ để kết luận điện trở LED 180 Ω là đúng con?

<details>
<summary>Gợi ý đáp án</summary>

1. Mỗi bên của mỗi cột là một nút, nên $30 \times 2 = 60$ nút năm lỗ. Đỏ trên, xanh trên, đỏ dưới, xanh dưới, mỗi thanh tách đôi, thành 8 đoạn.
2. Đen ở COM, đỏ ở ổ điện áp/ôm, núm ở thang DC cao hơn 3,3 V. Que đặt ngang điện trở, song song, LED vẫn nằm trong mạch. Tháo LED là hở vòng, điện áp trên điện trở sập về 0.
3. Dây còn tốt. Chỗ hở nằm giữa chân cắm và lò xo. Đổi lỗ khác trong cột đó. Đừng vứt jumper đã bíp thông hai đầu.
4. Cầu chì mA đứt. Đồng hồ đang bị dùng như một sợi ngắn ngang củ sạc. Thang vôn còn sống vì không đi qua cầu chì đó. Đừng đo lại để xác nhận.
5. Thông mạch là máy dò gần-ngắn. Con 180 Ω thường im, con 100 kΩ cũng im. Chỉ thang ôm, trên điện trở đã cắt nguồn, mới tách được hai con đó.

</details>

## Đọc thêm

Bài breadboard của SparkFun khớp với thanh nguồn, dải lỗ và rãnh trong hình: [How to use a breadboard](https://learn.sparkfun.com/tutorials/how-to-use-a-breadboard). Bài đồng hồ của họ là kỷ luật ổ cắm, mỗi chức năng một ảnh: [How to use a multimeter](https://learn.sparkfun.com/tutorials/how-to-use-a-multimeter). Đọc mục đo dòng, rồi nhìn lại que đỏ đang ở ổ nào trước khi khép mạch.

## Mua ở Việt Nam

Cả giỏ robot, gồm ESP32 hoặc Pico, TB6612, mô-tơ TT và HC-SR04, nằm ở [BOM và cách mua bộ kit robot ở Việt Nam]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %}). Bài này chỉ thêm đồ bàn thí nghiệm nếu danh sách đó chưa có.

Giá dưới đây đọc trên Hshop ngày 23 tháng 9 năm 2026. Mở lại trang trước khi trả tiền.

Breadboard 830 lỗ giá 35 000 ₫: [test board CAMMB-102](https://hshop.vn/test-board-cammb-102). Dây đực-đực, 40 sợi, giá 30 000 ₫: [dây cắm breadboard đực-đực](https://hshop.vn/day-cam-breadboard-duc-duc-20cm-cap-det-40-soi-m-m-jumper-wire). Đồng hồ UNI-T UT33D+ giá 285 000 ₫: [đồng hồ vạn năng UNI-T UT33D+](https://hshop.vn/dong-ho-van-nang-dien-tu-digital-multimeter-uni-t-ut33d-chinh-hang). Đồng hồ thay thế vẫn phải có còi thông mạch và thang miliampe có cầu chì — thang mà bạn hứa không ngắn ngang USB.
