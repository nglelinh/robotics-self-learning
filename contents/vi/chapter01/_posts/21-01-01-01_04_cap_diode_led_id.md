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

Học xong, bạn chỉ vào vạch trên tụ hoá nhôm và nói đó là chân âm, đồng thời coi tụ gốm đĩa hoặc tụ chip là không phân cực trừ khi thân nó ghi khác. Bạn đọc mã gốm kiểu 104 thành 100 nF. Bạn gọi catot của diode bằng vạch sơn, và kiểm LED bằng thang diode của đồng hồ thay vì chỉ tin chân dài. Bạn cũng giải thích được vì sao tụ 100 µF mắc ngang chân VM của driver làm dịu xung ngắn mà vẫn không thay được nguồn riêng cho hai mô-tơ TT.

## Cần có gì trước

Bạn dùng được $V = IR$ và đã chọn điện trở nối tiếp cho LED đỏ trên 3,3 V. Bạn biết thang diode chỉ dùng khi linh kiện mất nguồn, que đỏ không nằm ở ổ dòng. Kit chưa về thì ảnh trong bài vẫn đủ để học cực tính. Phần thực hành là thử diode, không phải thí nghiệm có điện.

## Chỗ này cứu xe hai bánh khỏi hiểu nhầm "cái tụ là pin"

ESP32 hoặc Pico chạy 3,3 V. TB6612 lấy điện mô-tơ ở VM, khoảng 4,5 V đến 10 V, và logic ở VCC vui với 3,3 V. Tụ hoá 100 µF mắc ngang VM là bể chứa cục bộ cho xung PWM của mô-tơ TT. Nó không phải pin. Năng lượng trong 100 µF hết trong chưa đầy một mili giây ở dòng kẹt, nên bộ pin vẫn phải có, và vẫn không được nối vào GPIO.

Đèn báo là LED cộng điện trở. Diode hồi tiếp, khi có, là loại cỡ 1N4007 với vạch hướng về đầu dương của mô-tơ. Tụ hoá cắm ngược trên pin đang sống có thể xì. Bài này dạy tách tụ, diode và LED trước khi bất kỳ dây nào trong số đó nóng.

## Tụ: vạch, mã, và 100 µF làm được đến đâu

Tụ hoá nhôm có cực. Vạch chạy dọc một bên, thường có dấu trừ trong đó, đánh dấu chân âm. Trên nguồn một cực, chân ấy về mass, chân kia lên rail đang cần được giữ cứng. Điện áp ghi trên vỏ phải cao hơn điện áp lớn nhất rail đó sẽ gặp. Pin 2S đầy khoảng 8,4 V, nên 16 V hoặc 25 V là dễ thở, 6,3 V thì không.

![Cực tính tụ hoá: vạch là chân âm]({{ site.imgurl }}/generated/capacitor_polarity.png)

![Tụ hoá nhôm, vạch đánh dấu phía âm]({{ site.imgurl }}/wikimedia/Electrolytic_capacitor.jpg)

Tụ gốm trong khóa này thường không phân cực. Đĩa không vạch, hoặc miếng SMD nâu không dấu cực, cắm chiều nào cũng được. Đừng bịa cực cho nó chỉ vì tụ hoá bên cạnh có cực. Một số tụ tantali có cực và ký hiệu khác; nếu bạn không mua tantali thì đừng cho rằng mọi hình chữ nhật be là tantali.

Tụ gốm xuyên lỗ hay dùng mã ba số theo picofarad. Hai số đầu là chữ số có nghĩa, số thứ ba là luỹ thừa của mười, cùng kiểu mã điện trở SMD nhưng đơn vị là pF. Con ghi 104 là

$$
10 \times 10^{4}\ \mathrm{pF} = 100000\ \mathrm{pF} = 100\ \mathrm{nF} = 0.1\ \mu\mathrm{F}
$$

Mã 103 là 10 nF. Mã không phải điện dung tính bằng nanofarad. Tụ hoá thường in thẳng, ví dụ 100 µF 16 V, vì 100 µF mà viết bằng mã picofarad thì vô lý.

Đây là con số giữ cho câu chuyện tụ trung thực. Năng lượng trong tụ là

$$
E = \frac{1}{2} C V^2
$$

Với $C = 100\ \mu\mathrm{F} = 100 \times 10^{-6}\ \mathrm{F}$ ở pin danh định 7,4 V,

$$
E = \frac{1}{2} \times 100 \times 10^{-6} \times (7.4)^2 \approx 0.0027\ \mathrm{J}
$$

Một mô-tơ TT kẹt gần 0,8 A ở 7,4 V là khoảng 6 W. Thời gian 100 µF nuôi nổi công suất đó xấp xỉ $0{,}0027 / 6 \approx 0{,}5\ \mathrm{ms}$. Nửa mili giây năng lượng kẹt có ích với sườn PWM và với điện cảm của dây pin dài. Nó không phải nguồn cho bánh xe. Hai mô-tơ khiến bể chứa càng nhỏ so với tải. Đặt 100 µF ngang VM và GND, vạch về GND, và vẫn cấp cho TB6612 một bộ pin thật. Đừng treo bộ pin đó lên chân 3V3 của Pico hoặc ESP32 rồi gọi tụ là giải pháp.

## Diode và LED

Diode silic dẫn dễ một chiều và chặn chiều kia. Vạch trên 1N4007 đánh dấu catot, đầu mà dòng quy ước đi ra khi diode phân cực thuận. Đầu kia là anot. LED đỏ trong đèn báo đóng vai tương tự, sụt thuận gần 2 V thay vì khoảng 0,7 V.

Chân dài của LED thường là anot, vạt phẳng trên vành thường là catot. Chữ "thường" là cả vấn đề. Bộ LED rẻ bị cắt sẵn chân, hoặc người học trước đã tỉa. Hãy tin đồng hồ. Thang diode, trên linh kiện mất nguồn, hiện sụt thuận một chiều và hở chiều kia. Diode silic thường khoảng 0,5 V đến 0,7 V. LED đỏ thường gần 1,6 V đến 2,0 V, và có thể le lói vì đồng hồ đang đẩy một dòng thử nhỏ. Cả hai chiều đều như ngắn thì linh kiện chết. Cả hai chiều đều hở thì chết, hoặc nó không phải diode.

![LED nhiều màu; độ dài chân chỉ là gợi ý]({{ site.imgurl }}/wikimedia/LEDs.jpg)

![Các vỏ trông giống nhau cho đến khi đọc chữ in]({{ site.imgurl }}/generated/component_lookalikes.png)

Miếng SMD nâu trơn thường là tụ; miếng có mã ba số thường là điện trở. Phải kiểm. Đèn báo là con mắc nối tiếp với khoảng 180 Ω từ 3,3 V. Diode hồi tiếp cạnh một transistor trần có vạch ở đầu dương của mô-tơ, để dòng muốn tiếp tục chạy khi khoá ngắt không đi xuyên transistor. TB6612 đã có sẵn đường đó. Bạn vẫn cần nhận ra 1N4007 khi nó rơi khỏi kit.

## Ví dụ: số thang diode bạn nên thấy

Lấy một 1N4007 và một LED đỏ, tháo khỏi mạch, không nguồn. Thang diode cấp dòng nhỏ và hiện điện áp nó cần.

Một chiều trên 1N4007 có thể thấy khoảng 0,62 V. Đảo que thì màn hình quá tầm, thường là "OL". Đầu có vạch là catot: số hiện khi que đỏ ở anot (đầu không vạch) và que đen ở vạch. Dòng quy ước trong phép thử diode đi ra từ que đỏ.

Một chiều trên LED đỏ có thể thấy khoảng 1,8 V và ánh le. Chiều kia quá tầm. Chân nằm dưới que đỏ lúc đọc 1,8 V là anot. Nếu chân đó cũng là chân dài thì nhà sản xuất và đồng hồ đồng ý. Nếu chúng bất đồng, tin đồng hồ và đánh dấu anot bằng bút trước khi cắt chân.

LED cần điện trở nối tiếp vì điện áp của nó gần như đứng yên trong khi dòng bỏ chạy. Điện áp trên tụ thì dịch chuyển, nên $E = \tfrac{1}{2}CV^2$ là câu hỏi đúng cho con 100 µF. Không con nào trong hai con đó là mô-tơ để treo lên GPIO.

## Thực hành

Lab này cố ý không cấp nguồn. Bạn sẽ không cắm ngược tụ hoá lên rail đang sống.

1. Gom một tụ hoá, một tụ gốm ghi 104 nếu có, một 1N4007 hoặc diode có vạch bất kỳ, và một LED. Mọi pin và cáp USB đều rút.
2. Trên tụ hoá, tìm vạch. Ghi chân nào là âm. Đọc điện áp định mức. Dưới 16 V thì không hợp pin 8,4 V, dù lab này không cấp pin đó.
3. Nếu gốm ghi 104, viết $10 \times 10^4\ \mathrm{pF} = 100\ \mathrm{nF}$ trước khi tra cứu.
4. Thang diode, que đỏ ở ổ điện áp/ôm, đen ở COM. Dò 1N4007 cả hai chiều. Ghi chiều nào ra điện áp gần 0,5 V đến 0,7 V, và xác nhận chiều đó đặt que đen lên vạch.
5. Dò LED cả hai chiều. Ghi số thuận và chân nào nằm dưới que đỏ. So với độ dài chân và với vạt phẳng, ghi mọi chỗ không khớp.

Mỗi diode phải dẫn một chiều và chặn chiều kia. LED có thể le sáng ở chiều dẫn. Tụ hoá trong lab này được nhận bằng mắt; bạn không nạp nó, và không đo điện dung trừ khi đồng hồ có thang điện dung và linh kiện đã ra khỏi mạch.

| Bạn thấy | Nguyên nhân hay gặp | Cách xử lý |
| --- | --- | --- |
| Cả hai chiều của diode đều OL | Que không tiếp xúc, hoặc linh kiện đứt | Lau chân và thử lại. Vẫn hở thì để riêng. |
| Cả hai chiều gần 0 V | Linh kiện chập, hoặc bạn còn ở thang thông mạch trên một sợi dây | Kiểm núm. Diode lành không bíp cả hai chiều. |
| LED sáng ở thang diode nhưng chân dài lại là catot | Chân đã bị cắt, hoặc lô hàng lạ | Đánh dấu anot theo đồng hồ. Đừng cãi một ánh le. |
| Muốn "xem phân cực ngược làm gì" với tụ hoá | Đó đúng sự cố lab này từ chối biểu diễn | Dừng. Đọc đoạn dưới. Đừng cấp điện ngược. |

Tụ hoá nhôm bị đảo trên rail đang sống không ngồi im. Màng oxit đánh thủng, dòng rò đun chất điện phân, áp suất tăng, vạch xé trên vỏ mở ra hoặc vỏ nổ. Con hỏng thường thành ngắn mạch. Trên pin mô-tơ, ngắn đó xả được cell. Ta mô tả để bạn nhận ra vỏ đã xì. Ta không lắp nó.

An toàn: chỉ thang diode, linh kiện ra khỏi mạch, USB rút, không nối VM. Đừng xả tụ lớn bằng cách chập nó với ngón tay hoặc với đầu que đang cầm. Tụ 100 µF trong kit là nhỏ; thói quen vẫn quan trọng khi board sau này không nhỏ.

## Bài tập

1. Một tụ gốm ghi 104, tụ kia ghi 223. Đổi cả hai ra nF.
2. Tụ 100 µF đang ở 7,4 V. Tính năng lượng tích. Ước lượng $E/P$ cho thấy năng lượng đó nuôi một cú kẹt 6 W được bao lâu?
3. Thang diode hiện 0,58 V trên 1N4007 khi que đen ở đầu có vạch, và OL khi đảo que. Đầu nào là catot, và que nào đang ở anot lúc đọc 0,58 V?
4. Bộ LED bị cắt mọi chân bằng nhau. Mô tả phép thử không nguồn vẫn tìm được anot, và nói bạn từ chối làm gì để "cho phép thử rõ hơn".
5. Một bạn đặt tụ hoá 100 µF ngang chân 3V3 của ESP32 và GND, vạch đúng, rồi nối hai mô-tơ TT vào chính chân 3V3 vì "tụ sẽ cấp dòng kẹt". Lập luận năng lượng sai ở đâu, và VM phải nối vào đâu?

<details>
<summary>Gợi ý đáp án</summary>

1. 104 là $10 \times 10^4\ \mathrm{pF} = 100\ \mathrm{nF}$. 223 là $22 \times 10^3\ \mathrm{pF} = 22\ \mathrm{nF}$.
2. $E = \tfrac{1}{2} \times 100 \times 10^{-6} \times 7{,}4^2 \approx 0{,}0027\ \mathrm{J}$. Thời gian khoảng $0{,}0027 / 6 \approx 0{,}45\ \mathrm{ms}$. Đó là một xung, không phải lúc chạy đều.
3. Đầu có vạch là catot, vì que đen ở đó trong lúc đọc thuận. Que đỏ ở anot.
4. Thang diode, không nguồn. Anot là chân dưới que đỏ khi bạn thấy sụt thuận và thường là ánh le. Đừng cấp 5 V hoặc GPIO không có điện trở nối tiếp để cho sáng hơn.
5. Lúc kẹt, tụ giữ chưa tới một mili giây năng lượng, nên ổn áp 3V3 vẫn bị đòi khoảng một ampe và sẽ sụt hoặc hỏng. VM của TB6612 phải thấy pin mô-tơ, trong dải 4,5 V đến 10 V của module, mass chung, GPIO chỉ làm logic.

</details>

## Đọc thêm

Trang tụ của SparkFun ngắn hơn về cực tính và mã: [Capacitors](https://learn.sparkfun.com/tutorials/capacitors). Trang diode nói về vạch và sụt thuận: [Diodes](https://learn.sparkfun.com/tutorials/diodes). Trang LED là bài bạn đã gặp ở phần điện trở: [Light-emitting diodes](https://learn.sparkfun.com/tutorials/light-emitting-diodes-leds).

## Mua ở Việt Nam

Cả giỏ, gồm vi điều khiển, TB6612, và mô-tơ TT — những thứ khiến câu chuyện 100 µF có nghĩa — nằm ở [BOM và cách mua bộ kit robot ở Việt Nam]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %}). Mua những món đó ở đó. Bài này không thêm một driver nữa.

Nếu bộ LED chưa có trong giỏ, Hshop niêm yết bộ 3 mm giá 20 000 ₫ ngày 23 tháng 9 năm 2026: [bộ 5 loại LED 3 mm](https://hshop.vn/bo-5-loai-led-sieu-sang-3mm-thong-dung-5-kind-3mm-transparent-color-led). Xem lại giá.

1N4007 và tụ hoá 100 µF, 16 V hoặc 25 V không có một link sản phẩm Hshop đã kiểm trong danh sách nguồn của bài này. Dùng trang tìm kiếm và tự đọc điện áp định mức: [Shopee, tìm 1N4007](https://shopee.vn/search?keyword=1N4007) và [Shopee, tìm tụ 100uF](https://shopee.vn/search?keyword=t%E1%BB%A5%20100uF). Cả hai là trang tìm kiếm, không phải sản phẩm. [Thế Giới IC](https://www.thegioiic.com/) và [IC Đây Rồi](https://icdayroi.com/) là quầy linh kiện nếu bạn muốn mua hai con lẻ thay vì một bộ. Đừng cấp điện cho chúng trước khi đã ghi vạch tụ và vạch diode ra giấy.
