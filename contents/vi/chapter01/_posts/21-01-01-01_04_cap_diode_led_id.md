---
layout: post
title: "Tụ điện, diode và LED"
chapter: "01"
order: 4
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter01
lesson_type: required
draft: false
---

## Mục tiêu

Sau bài học này, bạn sẽ nhận biết được vạch đánh dấu chân âm trên tụ hóa nhôm, đồng thời phân biệt tụ gốm đĩa hoặc tụ dán không phân cực (trừ khi thân linh kiện có ký hiệu cực riêng). Bạn sẽ đọc được mã tụ gốm ba chữ số như `104` thành 100 nF, xác định chân catot của diode qua vạch sơn, và kiểm tra cực tính LED bằng thang đo diode trên đồng hồ thay vì chỉ dựa vào độ dài chân. Bạn cũng sẽ tính toán và giải thích được vì sao một tụ điện 100 µF mắc ngang chân VM của mạch lái giúp làm mượt các xung ngắn nhưng không thể thay thế bộ pin riêng cho hai động cơ TT.

## Cần có gì trước

Bạn đã vận dụng được định luật Ohm $V = IR$, biết chọn điện trở hạn dòng cho LED đỏ trên nguồn 3,3 V, và nắm quy tắc chỉ sử dụng thang đo diode trên linh kiện đã ngắt nguồn (que đỏ nằm ở lỗ V/Ω, không ở lỗ đo dòng). Nếu chưa có bộ kit trên tay, các hình minh họa trong bài vẫn đủ để học cách nhận diện cực tính; phần thực hành chỉ dùng phép thử diode không cấp nguồn.

## Vì sao cần phân biệt tụ đệm với nguồn pin trên xe hai bánh

Trên xe đồ án, ESP32 hoặc Pico hoạt động ở mức 3,3 V; mạch lái TB6612 nhận nguồn động cơ ở chân VM (4,5 V đến 10 V) và nguồn logic ở chân VCC (3,3 V). Một tụ hóa 100 µF mắc ngang chân VM đóng vai trò bộ đệm năng lượng cục bộ cho các xung đóng cắt PWM của động cơ TT, nhưng **không phải là nguồn pin**: lượng năng lượng tích trữ trong tụ 100 µF cạn sạch trong chưa tới một mili giây khi động cơ kẹt trục. Do đó xe vẫn bắt buộc có bộ pin động cơ riêng, cách ly khỏi chân GPIO.

Ngoài ra, đèn báo trạng thái là LED mắc kèm điện trở, còn diode hồi tiếp (nếu dùng mạch đóng cắt rời) thường là loại 1N4007 với vạch catot hướng về cực dương nguồn động cơ. Việc nhận diện đúng cực tính trước khi lắp mạch giúp tránh tình huống tụ hóa bị cắm ngược cực và xì nổ khi cấp điện.

## Tụ điện: vạch cực, mã số và giới hạn năng lượng của tụ 100 µF

**Tụ hóa nhôm** là linh kiện phân cực. Dải vạch sáng chạy dọc một bên thân vỏ (thường in kèm dấu trừ) đánh dấu **chân âm**. Trên đường nguồn một chiều, chân âm nối về mass (GND), chân còn lại nối lên đường nguồn cần lọc. Điện áp định mức in trên vỏ tụ phải lớn hơn điện áp tối đa mà đường nguồn đạt tới: với pin 2S sạc đầy ở 8,4 V, nên chọn tụ định mức 16 V hoặc 25 V, tuyệt đối không dùng loại 6,3 V.

![Cực tính tụ hoá: vạch là chân âm]({{ site.imgurl }}/generated/capacitor_polarity.png)

![Tụ hoá nhôm, vạch đánh dấu phía âm]({{ site.imgurl }}/wikimedia/Electrolytic_capacitor.jpg)

**Tụ gốm** dùng trong khóa học (dạng đĩa không vạch hoặc tụ dán SMD màu nâu không dấu cực) là linh kiện không phân cực, có thể cắm theo chiều nào cũng được. Không nên tự gán cực tính cho tụ gốm chỉ vì tụ hóa bên cạnh có cực. Lưu ý rằng một số tụ tantali có phân cực với quy ước ký hiệu ngược lại; nếu bạn không chủ động mua tụ tantali, đừng mặc định mọi tụ dán hình chữ nhật màu vàng nhạt là tantali.

Tụ gốm xuyên lỗ thường dùng mã ba chữ số tính theo **picofarad (pF)**, tương tự quy tắc mã điện trở SMD: hai chữ số đầu là phần có nghĩa, chữ số thứ ba là số mũ của 10. Ví dụ tụ ghi `104` có giá trị:

$$
10 \times 10^{4}\ \mathrm{pF} = 100000\ \mathrm{pF} = 100\ \mathrm{nF} = 0.1\ \mu\mathrm{F}
$$

Tương tự, mã `103` là 10 nF. Đơn vị gốc của mã là pF chứ không phải nF. Riêng tụ hóa có điện dung lớn nên nhà sản xuất luôn in thẳng giá trị lên vỏ (ví dụ `100 µF 16 V`).

Để thấy rõ giới hạn của tụ 100 µF trên đường nguồn động cơ, ta tính năng lượng tích trữ trong tụ theo công thức:

$$
E = \frac{1}{2} C V^2
$$

Với $C = 100\ \mu\mathrm{F} = 100 \times 10^{-6}\ \mathrm{F}$ ở điện áp pin danh định 7,4 V:

$$
E = \frac{1}{2} \times 100 \times 10^{-6} \times (7.4)^2 \approx 0.0027\ \mathrm{J}
$$

Một động cơ TT kẹt trục rút khoảng 0,8 A ở 7,4 V tiêu thụ công suất xấp xỉ 6 W. Thời gian tụ 100 µF duy trì nổi công suất đó chỉ khoảng $0{,}0027 / 6 \approx 0{,}5\ \mathrm{ms}$. Nửa mili giây năng lượng này rất có ích để bù sườn xung PWM và giảm ảnh hưởng điện cảm của dây pin dài, nhưng hoàn toàn không thể thay thế nguồn pin nuôi bánh xe — đặc biệt khi có hai động cơ chạy song song. Hãy đặt tụ 100 µF ngang chân VM và GND (vạch âm về GND) đi kèm một bộ pin thật cho TB6612, không lấy nguồn từ chân 3V3 của Pico hay ESP32.

## Diode và LED

Diode silic cho dòng điện đi qua dễ dàng theo một chiều (phân cực thuận) và chặn dòng ở chiều ngược lại. Vạch sơn quanh một đầu thân của diode 1N4007 đánh dấu **catot** (đầu dòng điện quy ước đi ra khi dẫn thuận); đầu còn lại là **anot**. Đèn LED đỏ hoạt động theo cùng nguyên lý, chỉ khác là điện áp rơi thuận vào khoảng 2 V thay vì ~0,7 V như diode silic thường.

Theo quy ước sản xuất, chân dài của LED thường là anot và cạnh vát phẳng trên vành nhựa thường là catot. Tuy nhiên, từ "thường" không đảm bảo tuyệt đối vì chân linh kiện có thể đã bị cắt ngắn hoặc lệch chuẩn ở các lô hàng giá rẻ. Cách chắc chắn nhất là dùng **thang đo diode** trên đồng hồ vạn năng khi linh kiện không cấp nguồn: đồng hồ sẽ hiển thị điện áp thuận ở một chiều và báo hở (`OL`) ở chiều đảo ngược. Diode silic thường hiển thị khoảng 0,5 V đến 0,7 V; LED đỏ thường hiển thị khoảng 1,6 V đến 2,0 V kèm ánh sáng mờ do dòng thử nhỏ từ đồng hồ. Nếu cả hai chiều đều gần 0 V (chập) hoặc cả hai chiều đều `OL` (đứt), linh kiện đã hỏng.

![LED nhiều màu; độ dài chân chỉ là gợi ý]({{ site.imgurl }}/wikimedia/LEDs.jpg)

![Các vỏ trông giống nhau cho đến khi đọc chữ in]({{ site.imgurl }}/generated/component_lookalikes.png)

Trên mạch dán, linh kiện SMD màu nâu trơn thường là tụ gốm, còn linh kiện có in mã ba chữ số thường là điện trở — vẫn cần kiểm tra kỹ trước khi kết luận. Với mạch đóng cắt động cơ bằng transistor rời, cần mắc thêm một diode hồi tiếp (như 1N4007) song song động cơ với vạch catot hướng về cực dương nguồn để xả dòng cảm ứng khi khóa ngắt; module TB6612 đã tích hợp sẵn cơ chế bảo vệ này, nhưng bạn vẫn cần nhận diện được 1N4007 khi gặp trong bộ linh kiện.

## Ví dụ: kết quả chuẩn ở thang đo diode

Chuẩn bị một diode 1N4007 và một LED đỏ rời ngoài mạch (không cấp nguồn). Khi chuyển đồng hồ sang thang đo diode (que đen ở COM, que đỏ ở V/Ω), dòng thử quy ước đi ra từ que đỏ.

Với diode 1N4007, đặt que đỏ vào đầu không vạch (anot) và que đen vào đầu có vạch (catot), màn hình hiển thị khoảng 0,62 V; đảo ngược hai que thì màn hình báo `OL`.

Với LED đỏ, ở chiều thuận màn hình hiển thị khoảng 1,8 V và LED hơi phát sáng; đảo ngược hai que thì báo `OL`. Chân đang chạm que đỏ tại thời điểm đọc được 1,8 V chính là **anot**. Nếu kết quả này trái với độ dài chân ban đầu, hãy tin đồng hồ và đánh dấu lại chân anot bằng bút trước khi cắt chân.

Tóm lại, LED luôn cần điện trở nối tiếp vì điện áp rơi trên nó gần như cố định trong khi dòng tăng rất nhanh; còn tụ điện có điện áp thay đổi theo điện tích nên ta đánh giá bằng công thức năng lượng $E = \tfrac{1}{2}CV^2$.

## Thực hành

Bài lab này thực hiện hoàn toàn ở trạng thái **không cấp nguồn** để đảm bảo không cắm ngược tụ hóa lên đường nguồn đang có điện.

1. Chuẩn bị một tụ hóa nhôm, một tụ gốm ghi `104` (nếu có), một diode có vạch (như 1N4007) và một đèn LED. Rút toàn bộ pin và cáp USB khỏi bàn.
2. Quan sát tụ hóa: xác định vạch chân âm và đọc điện áp định mức trên vỏ. Ghi chú rõ nếu định mức dưới 16 V thì không dùng được cho pin 2S (8,4 V).
3. Với tụ gốm ghi `104`, tự tính $10 \times 10^4\ \mathrm{pF} = 100\ \mathrm{nF}$ ra giấy trước khi đối chiếu.
4. Chuyển đồng hồ sang thang đo diode (que đen ở COM, que đỏ ở V/Ω). Đo 1N4007 theo cả hai chiều, ghi lại chiều cho giá trị ~0,5–0,7 V và xác nhận que đen lúc đó đang đặt ở đầu có vạch.
5. Đo LED theo cả hai chiều, ghi lại điện áp thuận và xác định chân anot ở que đỏ; so sánh với độ dài chân và mặt vát nhựa rồi ghi chú nếu có điểm không khớp.

**Kết quả kỳ vọng:** Mỗi diode và LED chỉ dẫn theo đúng một chiều và báo `OL` ở chiều ngược lại; LED đỏ có thể sáng mờ ở chiều thuận. Trong bài này, bạn chỉ nhận diện tụ hóa bằng mắt và không nạp điện cho tụ (chỉ đo điện dung nếu đồng hồ có riêng thang đo tụ và linh kiện nằm ngoài mạch).

| Hiện tượng quan sát | Nguyên nhân thường gặp | Cách khắc phục |
| --- | --- | --- |
| Cả hai chiều đo diode đều hiện `OL` | Đầu que tiếp xúc kém hoặc linh kiện bị đứt | Làm sạch chân linh kiện và đo lại; nếu vẫn hở thì loại bỏ |
| Cả hai chiều đo đều gần 0 V | Linh kiện bị chập, hoặc đang nhầm thang thông mạch trên dây dẫn | Kiểm tra lại vị trí núm vặn; diode tốt không kêu bíp cả hai chiều |
| LED sáng ở thang diode nhưng chân dài lại là catot | Chân đã bị cắt trước đó hoặc lô sản xuất ngược chuẩn | Đánh dấu lại chân anot theo kết quả đo của đồng hồ |
| Muốn cấp điện ngược thử xem tụ hóa phản ứng thế nào | Gây nguy hiểm cháy nổ và hỏng linh kiện | Dừng ngay, không thử nghiệm cấp điện ngược cực cho tụ hóa |

Nếu tụ hóa nhôm bị cấp điện ngược cực trên đường nguồn đang hoạt động, lớp màng oxit cách điện sẽ bị đánh thủng, dòng rò lớn làm sôi chất điện phân, tăng áp suất khiến van xả trên đỉnh vỏ tụ xì bung hoặc nổ, và linh kiện hỏng thường chuyển sang trạng thái ngắn mạch làm xả mạnh nguồn pin. Chúng ta tìm hiểu cơ chế này để phòng tránh và nhận biết tụ đã hỏng, tuyệt đối không lắp thử.

**Lưu ý an toàn:** Chỉ thao tác ở thang đo diode với linh kiện rời, rút toàn bộ USB và không nối nguồn VM. Không xả tụ dung lượng lớn bằng cách chập trực tiếp bằng tay hay đầu que cầm trần; dù tụ 100 µF trong kit khá nhỏ, việc rèn thói quen an toàn rất cần thiết cho các mạch công suất lớn về sau.

## Video tham khảo

- **Xem trước:** [Diodes Explained - The basics how diodes work working principle pn junction](https://www.youtube.com/watch?v=Fwj_d3uO5g8) — The Engineering Mindset, tiếng Anh. Giải thích nguyên lý hoạt động và cực tính anot/catot của diode cũng như đèn LED.
- [Capacitors Explained - The basics how capacitors work working principle](https://www.youtube.com/watch?v=X4EUwTwZ110) — The Engineering Mindset, tiếng Anh. Minh họa quá trình tích phóng điện của tụ và cách nhận biết cực tính trên tụ hóa.

## Bài tập

1. Quy đổi hai mã tụ gốm `104` và `223` sang đơn vị nanofarad (nF).
2. Một tụ 100 µF được nạp đến 7,4 V. Hãy tính năng lượng tích trữ $E$ và ước lượng thời gian $E/P$ mà tụ có thể duy trì cho một tải động cơ kẹt công suất 6 W.
3. Ở thang đo diode, đồng hồ hiển thị 0,58 V trên 1N4007 khi que đen đặt ở đầu có vạch và `OL` khi đảo que. Đầu nào là catot, và que nào đang đặt ở anot lúc đọc được 0,58 V?
4. Giả sử một túi LED bị cắt ngắn hai chân bằng nhau. Hãy mô tả cách tìm chân anot không cần cấp nguồn ngoài, và nêu thao tác cần tránh khi muốn "thử cho sáng rõ hơn".
5. Một bạn mắc tụ hóa 100 µF đúng cực ngang chân 3V3 và GND của ESP32 rồi đấu hai động cơ TT trực tiếp vào chân 3V3 với suy nghĩ "tụ sẽ gánh giúp dòng kẹt". Lập luận năng lượng này sai ở đâu, và chân VM của TB6612 phải đấu vào nguồn nào?

<details>
<summary>Gợi ý đáp án</summary>

1. `104` là $10 \times 10^4\ \mathrm{pF} = 100\ \mathrm{nF}$. `223` là $22 \times 10^3\ \mathrm{pF} = 22\ \mathrm{nF}$.
2. $E = \tfrac{1}{2} \times 100 \times 10^{-6} \times 7{,}4^2 \approx 0{,}0027\ \mathrm{J}$. Thời gian duy trì khoảng $0{,}0027 / 6 \approx 0{,}45\ \mathrm{ms}$ — chỉ đủ lọc xung ngắn chứ không thể cấp nguồn chạy liên tục.
3. Đầu có vạch là catot (nơi đặt que đen khi phân cực thuận), còn que đỏ đang đặt ở chân anot.
4. Dùng thang đo diode ở trạng thái không cấp nguồn; chân chạm que đỏ khi đồng hồ hiện điện áp thuận (và LED có thể sáng mờ) chính là anot. Tuyệt đối không chích thẳng nguồn 5 V hay GPIO không có điện trở hạn dòng để làm LED sáng rõ hơn.
5. Tụ 100 µF chỉ dự trữ năng lượng trong chưa đầy 1 ms khi động cơ kẹt, nên mạch ổn áp 3V3 vẫn bị rút dòng cỡ ampe và lập tức sụt áp hoặc hỏng. Chân VM của TB6612 phải nối vào pin động cơ riêng (trong dải 4,5–10 V), nối mass chung và chỉ dùng GPIO cho tín hiệu logic.

</details>

## Đọc thêm

Các bài hướng dẫn ngắn gọn của SparkFun về cực tính và mã đọc: [Capacitors](https://learn.sparkfun.com/tutorials/capacitors), [Diodes](https://learn.sparkfun.com/tutorials/diodes) và [Light-emitting diodes](https://learn.sparkfun.com/tutorials/light-emitting-diodes-leds).

## Mua ở Việt Nam

Toàn bộ danh sách vi điều khiển, TB6612 và động cơ TT nằm ở bài [BOM và cách mua bộ kit robot ở Việt Nam]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %}).

Nếu chưa có bộ LED, bạn có thể tham khảo bộ LED 3 mm trên Hshop giá 20.000 ₫ (ghi nhận ngày 23 tháng 9 năm 2026): [bộ 5 loại LED 3 mm](https://hshop.vn/bo-5-loai-led-sieu-sang-3mm-thong-dung-5-kind-3mm-transparent-color-led).

Với diode 1N4007 và tụ hóa 100 µF (16 V hoặc 25 V), bạn có thể tìm qua trang tìm kiếm và tự kiểm tra điện áp định mức: [Shopee, tìm 1N4007](https://shopee.vn/search?keyword=1N4007) và [Shopee, tìm tụ 100uF](https://shopee.vn/search?keyword=t%E1%BB%A5%20100uF). Nếu chỉ cần mua vài linh kiện lẻ thay vì cả bộ, bạn có thể mua trực tiếp tại [Thế Giới IC](https://www.thegioiic.com/) hoặc [IC Đây Rồi](https://icdayroi.com/). Luôn ghi chú rõ cực tính tụ và vạch diode trước khi lắp mạch.
