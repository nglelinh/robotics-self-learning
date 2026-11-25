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

Sau bài học này, bạn sẽ nhận diện chính xác cấu trúc dải năm lỗ, rãnh giữa và thanh nguồn trên breadboard để biết những lỗ nào thực sự nối chung với nhau. Bạn sẽ lường trước việc nhiều breadboard cỡ lớn bị ngắt đôi ở giữa thanh nguồn và kiểm chứng chỗ ngắt đó bằng thang thông mạch thay vì dựa vào trí nhớ. Bạn sẽ nắm vững quy tắc đo điện áp một chiều mắc song song với linh kiện, không đo dòng trực tiếp trên củ sạc USB trong bài này, và chỉ đo điện trở khi đã ngắt nguồn. Trước mỗi lần đo áp, bạn luôn chọn thang đo cao hơn mức điện áp dự kiến và không để ngón tay chạm vào phần kim loại đầu que đo.

## Cần có gì trước

Bạn đã nắm được khái niệm vôn, ampe và lý do đèn LED báo trạng thái phải có điện trở nối tiếp. Bài này không lặp lại định luật Ohm mà tập trung vào kỹ năng thao tác trên bàn lab: hiểu rõ sơ đồ nối lỗ của breadboard và chọn đúng thang đo trên đồng hồ để không vô tình gây ngắn mạch. Bạn chỉ cần một đồng hồ vạn năng số và một breadboard không hàn.

---

Hàng trăm sinh viên điện tử đã từng dành trọn một buổi chiều kiểm tra lại từng dòng code chỉ vì một lỗi cực kỳ ngớ ngẩn trên **breadboard**: đường thanh nguồn dài bên mép breadboard bị ngắt đôi ở chính giữa (chỗ vạch đỏ/xanh bị đứt quãng) mà mắt thường không để ý! Biết cách hình dung mạng lưới lá đồng ẩn dưới lớp nhựa breadboard và sử dụng **đồng hồ vạn năng** đúng thang đo là kỹ năng cứu bạn khỏi 90% nỗi đau gỡ lỗi phần cứng.

## Kiến thức cần nhớ: Kết nối Breadboard và Nguyên lý Đồng hồ Vạn năng

1. **Bản đồ Lá đồng Ẩn của Breadboard:** Mỗi hàng 5 lỗ ở khu vực giữa nối thông ngang với nhau (bị tách đôi bởi rãnh giữa dành cho IC); hai dải nguồn dọc hai bên nối thông theo chiều dọc (nhưng nhiều breadboard cỡ lớn tách làm hai nửa trên–dưới!).
2. **Đo Song song (Vôn kế — Trở kháng cực lớn) vs. Đo Nối tiếp (Ampe kế — Trở kháng cực nhỏ):** Vôn kế có nội trở ~$$10\text{ M}\Omega$$ nên kẹp *song song* vào mạch mà không làm nhiễu dòng; ngược lại Ampe kế có điện trở shunt chỉ ~$$0.1\ \Omega$$ nên **bắt buộc phải cắt mạch mắc nối tiếp**!
3. **Đo Thông mạch & Điện trở (Chỉ đo khi TẮT nguồn):** Thang thông mạch phát ra một dòng thử cực nhỏ từ pin bên trong đồng hồ để kiểm tra xem hai điểm có thông nhau không; đo khi mạch đang có điện sẽ cho kết quả sai hoặc hỏng đồng hồ.

### Ví dụ làm từng bước: Vì sao đo nhầm thang Ampe song song nguồn lại làm nổ cầu chì đồng hồ?

Giả sử bạn có một mạch đơn giản gồm nguồn **$$V = 5.0\text{ V}$$** nối với điện trở tải **$$R_{\text{tải}} = 500\ \Omega$$**:
- **Đo dòng ĐÚNG (cắt dây, mắc Ampe kế nối tiếp tải, nội trở shunt $$R_s = 0.1\ \Omega$$):**
  $$
  I_{\text{đúng}} = \frac{5.0}{500 + 0.1} \approx \mathbf{10.0\text{ mA}} \quad (\text{an toàn tuyệt đối!}).
  $$
- **Đo dòng SAI (để que ở lỗ Ampe rồi chạm song song trực tiếp hai cực nguồn 5 V):** dòng điện đi tắt hoàn toàn qua điện trở shunt $$0.1\ \Omega$$:
  $$
  I_{\text{sai}} = \frac{5.0\text{ V}}{0.1\ \Omega} = \mathbf{50\text{ A}}!
  $$
  Dòng vọt lên **50 A** làm **đứt ngay cầu chì bảo vệ 10 A** (hoặc cháy mạch nếu đo trên cổng mA 200 mA)!

### Giải thích: 4 bước kiểm tra mạch breadboard bằng đồng hồ vạn năng

1. **Bước 1 — Nối cầu thanh nguồn nếu breadboard bị tách giữa:** Dùng hai sợi dây ngắn nối liền nửa trên và nửa dưới của thanh `+` và `-`, rồi kiểm tra bằng thang thông mạch.
2. **Bước 2 — Đo thông mạch `VCC–GND` khi chưa cấp điện:** Đảm bảo không có chân linh kiện nào chạm chéo làm ngắn mạch.
3. **Bước 3 — Cấp nguồn và đo điện áp tại *chân linh kiện* (không chỉ tại đầu nguồn):** Đặt que đen cố định vào một điểm `GND` chung, chấm que đỏ lần lượt tới chân `VCC` của từng IC để phát hiện dây cắm lỏng.
4. **Bước 4 — Chỉ chuyển sang thang Ampe khi thực sự cần đo dòng:** Và ngay sau khi đọc xong, rút que đỏ trả về lỗ `VΩmA` lập tức!

**Kiểm tra nhanh.** Bạn dùng đồng hồ thang DC V đo trực tiếp tại cực pin được $$5.00\text{ V}$$, nhưng đo tại chân `VCC` của cảm biến cắm cuối thanh nguồn breadboard lại chỉ được $$0.00\text{ V}$$. Nguyên nhân khả dĩ nhất là gì? Thanh nguồn breadboard bị ngắt đôi ở giữa (hoặc sợi dây jumper nối thanh nguồn bị đứt lõi bên trong)!

---

## Vì sao xe hai bánh hay gặp lỗi ở bước này

Trên xe đồ án, mạch ESP32 hoặc Pico, mạch lái TB6612 và hệ thống dây tín hiệu gặp nhau trên breadboard hoặc đầu cắm Dupont theo đúng quy tắc hình học: năm lỗ trong cùng một cột là một nút chung, còn rãnh giữa là rào cách điện. Một thanh nguồn bị ngắt ở giữa, một đầu dây cắm trượt khỏi kẹp lò xo, hay que đo đỏ còn quên ở lỗ đo dòng đều tạo ra triệu chứng giống như mạch bị chết trong khi chip thậm chí chưa được cấp điện.

Mạch TB6612 nhận nguồn logic 3,3 V từ vi điều khiển và nguồn động cơ VM từ pin riêng. Nếu bạn cố xử lý tình trạng cầu H không chạy bằng cách cấp 5 V vào GPIO, một lỗi đo đạc đơn giản sẽ biến thành hỏng chân phần cứng. Chân echo của cảm biến HC-SR04 cũng xuất mức 5 V nên cần đo kiểm cẩn thận. Bài này rèn thói quen đo thông mạch và đo điện áp an toàn ngay khi các linh kiện còn nằm rời trên bàn.

## Cấu trúc nối dây bên trong breadboard

Bên dưới lớp nhựa đục lỗ của breadboard không hàn là các thanh kẹp lò xo bằng kim loại. Khi bạn cắm chân linh kiện vào một lỗ, nó được nối điện với tất cả các lỗ khác nằm trên cùng thanh kẹp đó. Do tiếp xúc cơ khí không kín khít hoàn toàn, chân linh kiện quá ngắn hoặc bị ôxy hóa có thể trông như đã cắm chặt nhưng thực tế vẫn hở mạch — vì vậy đồng hồ vạn năng mới là căn cứ cuối cùng xác nhận hai điểm có nối nhau hay không.

Hai hàng dài chạy dọc hai mép là **thanh nguồn**, thường in vạch màu đỏ và xanh (hoặc đen). Các lỗ nằm dọc theo một vạch màu liên tục là cùng một đường dẫn; thanh đỏ phía trên độc lập với thanh đỏ phía dưới. Đặc biệt, trên nhiều loại breadboard cỡ lớn (kể cả loại 830 lỗ thông dụng), thanh kẹp kim loại bị ngắt đôi tại chính giữa, tương ứng với khoảng hở trên vạch màu in. Nếu bạn cấp 5 V vào nửa bên trái thì nửa bên phải vẫn không có điện cho đến khi bạn cắm dây nối cầu qua khe giữa. Một số breadboard cỡ nhỏ không có khe ngắt này, nên đừng đoán theo thói quen mà hãy đo thông mạch trực tiếp chiếc bạn đang dùng.

![Cấu tạo breadboard: thanh nguồn, dải năm lỗ, rãnh giữa]({{ site.imgurl }}/generated/breadboard_anatomy.png)

Khu vực trung tâm gồm các **dải đầu cuối**, trong đó mỗi cột có năm lỗ phía trên rãnh giữa và năm lỗ phía dưới rãnh giữa. Năm lỗ trong cùng một nửa cột nối thông với nhau, nhưng hoàn toàn tách biệt với cột bên cạnh. **Rãnh giữa** là đường cách điện giúp các IC vỏ DIP đặt bắc ngang qua mà hai hàng chân đối diện không chập vào nhau.

Hai lỗi cắm mạch kinh điển trên breadboard là cắm cả hai chân LED vào cùng một nhóm năm lỗ (làm nối tắt LED) hoặc cắm hai linh kiện ở hai bên rãnh giữa mà quên dây nối cầu (làm hở mạch). Cả hai lỗi này nhìn bên ngoài đều rất gọn gàng nhưng mạch sẽ không hoạt động.

![Breadboard không hàn, thanh nguồn chạy dọc mép]({{ site.imgurl }}/wikimedia/breadboard.jpg)

## Ý nghĩa của từng thang đo trên đồng hồ vạn năng

Ba thói quen sau giúp tránh hầu hết các sự cố cháy cầu chì đồng hồ trong phòng lab:
1. Que đen luôn cắm cố định ở lỗ **COM**.
2. Que đỏ cắm ở lỗ ghi **V, Ω** (hoặc ký hiệu tương đương) cho mọi phép đo điện áp, điện trở và thông mạch.
3. Chỉ chuyển que đỏ sang lỗ đo dòng (**A** hoặc **mA**) khi thực sự cần đo dòng, và **rút trả lại lỗ V, Ω ngay sau khi đo xong**.

Nếu quên que đỏ ở lỗ đo dòng rồi đem đo điện áp, điện trở shunt rất nhỏ bên trong đồng hồ sẽ nối tắt trực tiếp nguồn điện, làm đứt ngay cầu chì mA. Điều nguy hiểm là thang đo điện áp sau đó vẫn hoạt động bình thường nên bạn chỉ phát hiện hỏng cầu chì vào lần đo dòng kế tiếp.

![Đồng hồ vạn năng số: núm, màn hình, ổ que đo]({{ site.imgurl }}/wikimedia/Digital_Multimeter_Aka.jpg)

**Đo điện áp một chiều (DC V)** thực hiện bằng cách **mắc song song**: giữ nguyên mạch đang hoạt động và đặt hai đầu que đo vào hai điểm cần xác định hiệu điện thế. Nếu đặt ngược que trên đồng hồ số, màn hình chỉ hiện dấu trừ mà không làm hỏng linh kiện. Hãy luôn chọn thang DC cao hơn điện áp dự kiến (ví dụ thang 20 V bao phủ tốt cả nguồn USB 5 V lẫn pin 2S đầy 8,4 V). Ngay cả với đồng hồ tự chọn thang (auto-ranging), bạn vẫn cần xoay đúng ký hiệu điện áp một chiều chứ không phải thang ôm.

**Đo dòng điện** thực hiện bằng cách **mắc nối tiếp**: phải ngắt hở một nhánh dây để dòng điện đi xuyên qua đồng hồ, và chỉ thực hiện sau khi đã chuyển que đỏ sang lỗ đo dòng phù hợp. Trong bài này, tuyệt đối không đo dòng trực tiếp trên củ sạc USB hay chân GPIO, bởi củ sạc có thể đẩy dòng 1 A trở lên làm đứt ngay cầu chì mA nếu bạn kẹp ngang ngõ ra.

**Đo điện trở (Ω) và thông mạch** chỉ được phép làm khi **mạch đã ngắt hoàn toàn nguồn điện**, vì đồng hồ tự phát một điện áp thử nhỏ. Thang thông mạch phát tiếng bíp khi gặp dây dẫn hoặc tiếp điểm khép kín có điện trở rất nhỏ; một điện trở 180 Ω thường sẽ không kêu bíp ở thang này vì thông mạch chỉ báo hiệu "gần như ngắn mạch". Khi cần biết trị số chính xác, hãy chuyển sang thang đo Ω.

## Ví dụ thực tế: thanh nguồn tưởng có điện nhưng thực chất đang hở

Giả sử bạn nối nguồn từ củ sạc USB vào nửa bên trái của thanh đỏ và thanh xanh trên breadboard 830 lỗ (chưa gắn ESP32 hay linh kiện nào khác). Đặt đồng hồ ở thang 20 V DC, que đen ở COM, que đỏ ở lỗ V/Ω.

Khi đo giữa thanh đỏ trái và thanh xanh trái, đồng hồ hiển thị 5,08 V — mức điện áp bình thường của củ sạc tốt. Giữ nguyên que đen ở thanh xanh trái và di chuyển que đỏ sang nửa phải của thanh đỏ (qua khe ngắt trên vạch in), màn hình chỉ hiện 0,02 V. Đây không phải sụt áp nhỏ trên dây mà là hở mạch. Bạn rút củ sạc để cắt hoàn toàn nguồn, chuyển đồng hồ sang thang thông mạch và đo dọc thanh đỏ qua khe giữa thì thấy im lặng. Sau khi cắm thêm một dây nối cầu qua khe giữa thanh đỏ và một dây qua khe giữa thanh xanh rồi cấp nguồn lại, nửa phải thanh đỏ đo được 5,07 V.

Lý do tuyệt đối không kẹp lỗ đo dòng ngang củ sạc có thể thấy qua phép ước tính với điện trở shunt 10 A cỡ $0{,}01\ \Omega$:

$$
I \approx \frac{5}{0.01} = 500\ \mathrm{A}
$$

Dĩ nhiên củ sạc thực tế sẽ kích hoạt bảo vệ và giới hạn dòng về khoảng 1–2 A, nhưng mức đó vẫn dư sức làm đứt cầu chì 200 mA bên trong đồng hồ. Bài toán đo dòng hai động cơ TT kẹt trục (mỗi chiếc cỡ 1 A) sẽ thực hiện về sau bằng cách mắc nối tiếp trên nguồn pin động cơ, phát một xung ngắn và cắm que đỏ vào lỗ đo dòng có giới hạn phù hợp.

## Thực hành

1. Ngắt mọi nguồn điện. Cắm que đen vào COM, que đỏ vào lỗ V/Ω và xoay núm sang thang thông mạch.
2. Đo thông mạch một sợi dây jumper từ đầu này sang đầu kia để chắc chắn có tiếng bíp. Cắm một đầu dây vào thanh đỏ, đầu kia vào một nhóm năm lỗ. Đo thông mạch từ một lỗ khác của nhóm đó về một lỗ khác trên thanh đỏ (phải có tiếng bíp), sau đó chạm sang cột kế bên (phải im lặng).
3. Đo thông mạch xuyên qua rãnh giữa trên cùng một số cột và xác nhận không có tiếng bíp.
4. Kiểm tra chỗ ngắt giữa của thanh nguồn: đo từ nửa trái sang nửa phải thanh đỏ. Với loại 830 lỗ có khe ngắt, đồng hồ sẽ im; hãy cắm một dây nối cầu qua khe rồi đo lại để xác nhận đã kêu bíp. Lặp lại tương tự với thanh xanh.
5. Chuyển sang đo điện áp bằng củ sạc điện thoại hoặc pin dự phòng (không dùng GPIO hay chân 3V3). Nếu có mạch tách nguồn USB, đưa 5 V và GND vào thanh nguồn vừa kiểm tra; nếu đo trực tiếp đầu dây nguồn, đặt que đỏ vào cực 5 V và que đen vào GND. Chọn thang DC cao hơn 5 V (thường là 20 V) và ghi lại số đo.

**Kết quả kỳ vọng:** Đồng hồ kêu bíp qua dây jumper tốt và trong cùng một nhóm năm lỗ; im lặng qua rãnh giữa và qua khe ngắt thanh nguồn trước khi nối cầu. Điện áp đo được của củ sạc nằm trong khoảng 4,7 V đến 5,3 V. Nếu đo ra gần 0 V dù thông mạch đã tốt, hãy kiểm tra lại xem bạn có đặt que nhầm thanh nguồn hoặc củ sạc chưa có điện không.

| Hiện tượng quan sát | Nguyên nhân thường gặp | Cách khắc phục |
| --- | --- | --- |
| Không kêu bíp dù dây jumper trông đã cắm sâu | Chân dây trượt khỏi lò xo hoặc kẹp lỗ đó bị giãn | Chuyển sang lỗ khác cùng cột; nếu cả cột tiếp xúc kém thì đánh dấu bỏ cột đó |
| Nửa trái thanh nguồn đo ~5 V, nửa phải ~0 V | Khe ngắt giữa thanh nguồn chưa được nối cầu | Cắm dây nối cầu qua khe giữa cả thanh đỏ lẫn thanh xanh rồi đo lại |
| Thang thông mạch kêu bíp khi vẫn đang cắm nguồn | Đo ohm hoặc thông mạch trên mạch còn điện | Rút nguồn ngay trước khi đo thông mạch hoặc điện trở |
| Màn hình lóe lên, sau đó thang mA luôn đọc 0 dù thang 20 V vẫn bình thường | Quên que đỏ ở lỗ đo dòng rồi kẹp ngang nguồn sạc | Cầu chì mA đã đứt; không thử kẹp lại lần nữa để kiểm chứng |

**Lưu ý an toàn:** Luôn bắt đầu ở thang đo áp cao hơn điện áp dự kiến (tránh để thang 200 mV khi đo pin 2S gần 8 V). Giữ ngón tay phía sau gờ bảo vệ, không chạm vào đầu kim loại của que đo. Không đo dòng trên cổng USB và không đưa nguồn 5 V của củ sạc vào chân GPIO của ESP32 hay Pico.

## Video tham khảo

- **Xem trước:** [CÁCH SỬ DỤNG ĐỒNG HỒ VẠN NĂNG ĐO ĐIỆN ĐƠN GIẢN](https://www.youtube.com/watch?v=FsBgW0WDQSw) — Sơn Tiện Ích, tiếng Việt. Hướng dẫn bằng tiếng Việt cách chọn đúng lỗ cắm và thang đo khi đo điện áp, điện trở.
- [Breadboard tutorial: How to use a breadboard (for beginners)](https://www.youtube.com/watch?v=W6mixXsn-Vc) — LeftyMaker, tiếng Anh. Giải thích rõ sơ đồ nối sẵn bên trong breadboard và thói quen dùng thông mạch để kiểm chứng.

## Bài tập

1. Một breadboard có 30 cột ở mỗi bên rãnh giữa, đồng thời cả thanh nguồn trên và dưới đều bị ngắt đôi một lần ở giữa. Hỏi khu vực trung tâm có bao nhiêu nút năm lỗ độc lập, và có tất cả bao nhiêu đoạn thanh nguồn tách biệt?
2. Bạn cần đo điện áp rơi trên điện trở 180 Ω đang mắc nối tiếp với LED trên nguồn 3,3 V. Que đo cắm vào lỗ nào, núm vặn chọn thang gì, và có được tháo LED ra khi đo không?
3. Một sợi dây jumper đo thông mạch trực tiếp hai đầu kêu bíp rõ (khoảng 0,3 Ω), nhưng khi cắm một đầu vào lỗ breadboard thì đo từ lỗ bên cạnh cùng cột sang đầu dây kia lại không kêu. Điểm hở mạch nằm ở đâu?
4. Một bạn định "đo dòng USB" bằng cách kẹp hai que đồng hồ trực tiếp vào 5 V và GND, thấy màn hình lóe lên rồi từ đó thang mA luôn đọc 0 trong khi thang 20 V vẫn đo áp bình thường. Bộ phận nào đã hỏng?
5. Vì sao việc thang thông mạch không kêu bíp không đủ cơ sở để kết luận một điện trở 180 Ω là đúng trị số hay đã hỏng?

<details>
<summary>Gợi ý đáp án</summary>

1. Mỗi cột có hai nút độc lập ở hai bên rãnh giữa nên tổng cộng có $30 \times 2 = 60$ nút năm lỗ. Với 4 thanh nguồn (đỏ trên, xanh trên, đỏ dưới, xanh dưới) đều tách đôi ở giữa, ta có 8 đoạn thanh nguồn độc lập.
2. Que đen cắm ở COM, que đỏ ở lỗ V/Ω, núm chọn thang DC V cao hơn 3,3 V. Đặt hai que đo song song vào hai đầu điện trở trong khi vẫn giữ LED trong mạch; nếu tháo LED sẽ làm hở mạch khiến điện áp rơi trên điện trở về 0 V.
3. Bản thân sợi dây vẫn tốt; điểm hở nằm ở tiếp xúc giữa chân dây và kẹp lò xo của lỗ cắm đó. Chỉ cần chuyển sang lỗ khác trong cùng cột, không cần bỏ sợi dây.
4. Cầu chì bảo vệ thang mA bên trong đồng hồ đã đứt do bị nối tắt ngang nguồn 5 V. Thang đo điện áp không đi qua cầu chì này nên vẫn hoạt động. Không thử chập lại lần nữa.
5. Thang thông mạch chỉ phát hiện mức điện trở rất thấp (gần ngắn mạch), nên cả điện trở 180 Ω lẫn 100 kΩ đều thường không kêu bíp. Phải dùng thang đo điện trở (Ω) trên linh kiện đã ngắt nguồn mới xác định được trị số thật.

</details>

## Đọc thêm

Bài hướng dẫn của SparkFun giải thích rõ cấu tạo thanh nguồn, dải năm lỗ và rãnh giữa: [How to use a breadboard](https://learn.sparkfun.com/tutorials/how-to-use-a-breadboard). Bài hướng dẫn về đồng hồ vạn năng minh họa trực quan vị trí lỗ cắm cho từng chức năng: [How to use a multimeter](https://learn.sparkfun.com/tutorials/how-to-use-a-multimeter) — hãy đọc kỹ mục đo dòng và tạo thói quen nhìn lại lỗ cắm que đỏ trước mỗi lần đo.

## Mua ở Việt Nam

Toàn bộ danh sách linh kiện robot nằm tại [BOM và cách mua bộ kit robot ở Việt Nam]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %}). Bài này chỉ liệt kê lại ba dụng cụ đo thử cơ bản nếu bạn chưa mua sẵn (giá tham khảo trên Hshop ngày 23 tháng 9 năm 2026; cần kiểm tra lại trang bán trước khi thanh toán).

Breadboard 830 lỗ giá 35.000 ₫: [test board CAMMB-102](https://hshop.vn/test-board-cammb-102). Dây cắm đực-đực (bộ 40 sợi) giá 30.000 ₫: [dây cắm breadboard đực-đực](https://hshop.vn/day-cam-breadboard-duc-duc-20cm-cap-det-40-soi-m-m-jumper-wire). Đồng hồ vạn năng UNI-T UT33D+ giá 285.000 ₫: [đồng hồ vạn năng UNI-T UT33D+](https://hshop.vn/dong-ho-van-nang-dien-tu-digital-multimeter-uni-t-ut33d-chinh-hang). Nếu chọn mẫu đồng hồ thay thế khác, cần đảm bảo có còi thông mạch và thang đo mA có cầu chì bảo vệ.
