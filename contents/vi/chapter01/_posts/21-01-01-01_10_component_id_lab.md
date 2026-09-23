---
layout: post
title: "Lab — thông mạch, đo ohm và linh kiện dễ nhầm"
chapter: "01"
order: 10
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter01
lesson_type: required
draft: false
---

Giờ này là một buổi bàn. Các bài trước đưa mã màu, vạch diode và vạch tụ hóa từng món một. Hôm nay chúng nằm chung một breadboard chưa có điện, và điểm là một bảng số bạn tự đo. Ảnh đống linh kiện không phải số đo. Mã màu chưa kiểm bằng đồng hồ là một phỏng đoán, sau này sẽ bị hàn vào xe.

## Mục tiêu

Bạn lập bản đồ hàng nào trên breadboard kêu và khe nào thì hở, rồi chụp bản đồ đó. Bạn giải mã năm điện trở và đo từng con ngoài mạch, rồi giữ hoặc loại theo dung sai. Bạn dùng chế độ diode cho một LED và một diode, ghi số thuận, và viết chân nào là anode. Bạn tách ba cặp dễ nhầm bằng chữ: điện trở vạch màu với cuộn cảm vạch màu, tụ gốm với tụ tantali, transistor TO-92 với IC ổn áp TO-92. Bạn gọi tên ba lỗi đo trước khi chúng chui vào bảng: đo ohm khi linh kiện còn trong mạch, que diode bị chính chiếc đồng hồ của bạn đảo cực, và điện trở năm vạch bị đọc như bốn vạch.

## Kiến thức cần có

Bài 02 đến 05 là nền: hàng breadboard, đồng hồ, mã điện trở, tụ, diode và LED. Cần thông mạch, ohm và chế độ diode. Không cần mỏ hàn, không cần cấp nguồn TB6612. Thiếu món nào thì viết bước đó và đánh dấu dry-run. Đừng mượn số của người khác.

## Vì sao bài này quan trọng

Xe vẫn là ESP32 hoặc Pico 3,3 V, một TB6612, hai mô-tơ TT trên pin riêng, và HC-SR04 có echo 5 V. Không module nào bào chữa cho một linh kiện sai trên bộ dây quanh chúng. LED trạng thái trên GPIO cần điện trở đã đo, không phải vạch bạn đọc lệch một thập phân. Tụ đệm trên VM, 100–470 µF ở bài 09, là tụ hóa nhôm có vạch âm; hạt tantali thường dùng vạch theo nghĩa ngược, và lấy nhầm quy tắc ấy là cách làm xì linh kiện trên rail mô-tơ. IC ổn áp TO-92 cắm vào chỗ transistor, hoặc ngược lại, là cách giết rail 3,3 V trong khi mô-tơ vẫn vô can. Bảng của buổi này là bằng chứng bạn tách được các món ấy trước khi chúng chui vào gen co.

## Trên bàn có gì

Trong giờ này: một đồng hồ, một breadboard, năm điện trở, một tụ hóa, một tụ gốm, một LED, một diode, và vài sợi dây. Không cần gì thêm, và không có điện. Tụ gốm là đĩa hoặc khối nhỏ không dấu cực. Tụ hóa là vỏ lon. Diode là số in trên con bạn đang cầm; ghi đúng số đó, đừng đổi 1N4001 thành 1N4007 chỉ vì bài viết chữ "diode".

![Vạch màu sẽ được kiểm, không được tin suông]({{ site.imgurl }}/generated/resistor_color_code.png)

Để bảng này cạnh năm điện trở lúc điền cột danh định. Đồng hồ được phép không đồng ý. Khi nó không đồng ý, đọc lại vạch, kể cả khả năng bạn đã coi năm vạch thành bốn. Đừng sửa số đồng hồ cho khớp bảng.

![Vỏ giống nhau, ruột thì không]({{ site.imgurl }}/generated/component_lookalikes.png)

Hình này là lý do có danh sách dễ nhầm. Cùng đường viền, khác linh kiện. Danh sách của bạn ghi cặp nào, phép thử nào, kết quả nào. "Trông khác mà" không phải phép thử.

![Một bộ điện trở, trước khi món nào vào mạch]({{ site.imgurl }}/wikimedia/resistors_assortment.jpg)

Chọn năm trị bạn giải được, trong đó ít nhất một con không phải 220 Ω và không phải 10 kΩ, để buổi này không đậu bằng trí nhớ.

![Chân nào của tụ là cực âm]({{ site.imgurl }}/generated/capacitor_polarity.png)

Trên lon nhôm trong kit này, vạch là cực âm. Bạn sẽ chỉ vào nó. Bạn sẽ không áp câu ấy cho hạt tantali.

![Cực LED là câu hỏi của đồng hồ nếu chân đã bị cắt]({{ site.imgurl }}/wikimedia/LEDs.jpg)

Chân dài thường là anode, mặt vát trên vành thường là cathode. Chân đã cắt và thấu kính rẻ làm hỏng thói quen ấy. Chế độ diode là bước bạn ghi lại.

## Các bước

Cả giờ không có điện. Không USB, không pin, không mô-tơ.

1. **Lập hàng nào kêu.** Chế độ thông mạch. Kêu một nhóm năm lỗ ở giữa và xác nhận chúng là một nút. Kêu qua rãnh giữa và xác nhận hở. Kêu từng rail nguồn từ đầu đến cuối. Tiếng kêu dừng giữa đường thì rail bị chia; đánh dấu chỗ đứt trên bản phác. Bản này là một phần điểm. "LED chết" về sau vẫn có thể chỉ là bạn chưa bao giờ đứng trên cùng một nút.
2. **Giải mã, rồi đo, năm điện trở.** Với mỗi con, ghi màu, ohm danh định, và dung sai. Đo ngoài mạch. Trị lớn thì đừng kẹp chân bằng ngón tay, vì da cũng là điện trở. Con 5% chỉ đạt trong khoảng

$$
R_{\mathrm{danh}}(1 - 0{,}05) \le R_{\mathrm{do}} \le R_{\mathrm{danh}}(1 + 0{,}05)
$$

Vàng ở vạch cuối là 5%. Mã và đồng hồ lệch nhau thì đồng hồ bắt đầu lần đọc vạch thứ hai. Con ra ngoài cửa sổ thì để riêng. Nó không quay lại túi "đã biết tốt". Chập hai que một lần và ghi độ lệch ấy, thường vài phần mười ôm. Nó có nghĩa với con 10 Ω và gần như vô nghĩa với con 10 kΩ.
3. **Chế độ diode cho LED và cho diode.** Ghi số thuận và chân vật lý nào đang ở que đỏ khi có số ấy. Sau khi bạn đã xác nhận đồng hồ đấu thế nào, chân đó là anode của phép đo này. Ghi luôn số hở hoặc quá tải khi đảo que, và dấu nhìn thấy: mặt vát, chân ngắn, hoặc vạch cathode. LED đỏ thường khoảng 1,6–2,2 V và có thể le lói. Diode silic thường khoảng 0,5–0,8 V. "OL" cả hai chiều trên LED có thể là con chết hoặc đồng hồ không đủ áp để sáng màu đó. Nói bạn tin trường hợp nào, và vì sao.
4. **Danh sách dễ nhầm, ba cặp.** Viết vào sổ dù trên bàn chỉ có một vế của cặp. Nói bạn sẽ đo gì.

Điện trở và cuộn cảm nhỏ có thể mang cùng kiểu vạch màu. Điện trở đo gần mã của nó. Cuộn cảm, một vòng dây, đo gần như ngắn, vài ôm hoặc ít hơn, rất thấp so với mã 1 kΩ hay 10 kΩ. Đừng gắn cuộn ấy làm điện trở nối tiếp của LED. Bạn sẽ không hạn dòng, và có thể nấu LED hoặc GPIO.

Đĩa gốm không có cực. Tụ tantali có cực, và vạch hoặc thanh trên nhiều hạt tantali chỉ cực dương, ngược với lon nhôm trong hình cực tính. Không chắc hạt thuộc họ nào thì không mắc ngang VM. Quy tắc nhôm và quy tắc tantali không đổi cho nhau.

Transistor TO-92 và IC ổn áp TO-92 chung thân nửa trụ. Mã quyết định. Mã kiểu 78L05 là IC ổn áp, chân thuộc họ vào, mass, ra. Mã kiểu S8050 hoặc BC547 là transistor, thứ tự emitter, base, collector phải tra chứ không đoán. Mã bị mòn thì vào túi chưa biết. Nó không được nuôi ESP32.

## Lỗi tạo ra số giả

Đo ohm trong mạch là đo cả mạng, không đo con ấy. Điện trở 220 Ω ngồi cạnh linh kiện khác có thể hiện 80 Ω mà vẫn là con 220 Ω tốt. Nhấc một chân. Không nhấc được thì bạn không đang đo con đó.

Một số đồng hồ đảo chiều chế độ diode, hoặc que bị cắm nhầm ổ từ hôm qua. Que đỏ là dương trên hầu hết máy số và không phải trên mọi máy. Chứng minh máy của bạn một lần: que nào cho số thuận trên một diode đã biết thì que đó là phía anode của diode ấy. Ghi "đỏ = nguồn anode" hoặc "đỏ bị đảo" trên đầu bảng. Giả định ngược sẽ gắn nhầm mọi cathode trong sổ, kể cả LED sắp treo lên chân 3,3 V.

Đọc điện trở năm vạch như bốn vạch sẽ đẩy hệ số nhân. Năm vạch là ba chữ số, rồi hệ số, rồi dung sai. Bốn vạch là hai chữ số, rồi hệ số, rồi dung sai. Nâu-đen-đen-đỏ-nâu không phải cùng công thức với nâu-đen-đen-vàng. Đồng hồ lệch khoảng mười hoặc một trăm lần thì đếm lại vạch trước khi kết tội linh kiện.

## Bảng sổ phải có

Chép và điền. Khoảng dự kiến nằm đây để chữ "ok" trống không thể đạt.

| # | Linh kiện | Cái bạn đọc | Danh định hoặc cực | Đo được | Đạt? |
|---|-----------|-------------|--------------------|---------|------|
| 1 | hàng năm lỗ | lỗ nào | một nút | kêu hoặc hở | |
| 2 | rãnh giữa | qua khe | hở | kêu hoặc hở | |
| 3 | rail đỏ | đầu đến cuối | liền hoặc đứt | đứt ở đâu | |
| 4–8 | năm điện trở | màu | Ω và % | Ω | có/không |
| 9 | LED | chân anode | dài hay không | V thuận | |
| 10 | diode | chân anode | vạch là cathode | V thuận | |
| 11 | tụ hóa | vạch | âm | tên ảnh | |

Hàng điện trở chỉ đạt khi có cả trị giải mã và trị đo. Hàng LED chỉ đạt khi có một số và chữ anode gắn với một chân. Lưu `ch01-10-id-table`.

## Ví dụ

Vạch nâu, đen, đỏ, vàng. Đó là 1, 0, hai số 0, 5%, tức $$1{,}0\,\mathrm{k}\Omega \pm 5\%$$.

$$
1000 \times 0{,}95 = 950,\qquad 1000 \times 1{,}05 = 1050
$$

Đồng hồ hiện 1027 Ω. Hàng đạt. Con thứ hai, mã 220 Ω, còn ngồi trên breadboard cạnh mạch LED và đồng hồ hiện 86 Ω. Số đó bỏ. Nhấc một chân. Số mới là 218 Ω, nằm trong $$220 \times 0{,}95$$ đến $$220 \times 1{,}05$$, hàng đạt. 86 Ω là của mạng, không phải của con.

Con thứ ba có năm vạch nhưng lần đầu bị ghi như bốn vạch, ra 1000 Ω trên giấy và khoảng 100 Ω trên đồng hồ. Đếm lại thành ba chữ số cộng hệ số thì hết lệch một thập phân. Con chưa bao giờ hỏng.

Trên diode, đầu có vạch là cathode, nên anode là chân kia. Que đỏ ở anode, que đen ở vạch, màn hình 0,62 V. Đảo que thì OL. Trên LED đỏ, que đỏ ở chân dài ra 1,85 V và le sáng, nên chân dài ấy là anode hôm nay. Hai điện áp trong cùng một bảng là cách chứng minh không bị tráo món: khoảng 0,6 V là diode, khoảng 1,8 V là LED đỏ.

## Bài tập

1. Điện trở 470 Ω, vạch vàng, đo được 502 Ω. Tính cửa sổ 5% và đưa kết luận.
2. Chế độ diode: OL khi đỏ ở chân LED dài, 1,9 V khi đỏ ở chân ngắn. Đồng hồ đã được chứng minh là que đỏ mang cực dương. Chân nào là anode, và OL nghĩa là gì?
3. Điện trở 1 kΩ trong board đã tắt nguồn đo được 120 Ω. Sửa đầu tiên là gì, và vì sao "mã sai" không phải bước ấy?
4. Một con có vạch như mã 10 kΩ nhưng đo 1,2 Ω. Danh tính nào hợp lý hơn, và nó có được làm điện trở nối tiếp cho LED 3,3 V không?
5. Một con TO-92 mất mã. Viết dòng dễ nhầm, và nói nó có được nuôi ESP32 không.

<details markdown="1">
<summary>Gợi ý đáp án</summary>

1. Cửa sổ là $$470 \times 0{,}95 = 446{,}5\,\Omega$$ đến $$470 \times 1{,}05 = 493{,}5\,\Omega$$. 502 Ω nằm ngoài. Trượt, để riêng.
2. Anode là chân ngắn, vì que đỏ dương đặt ở đó thì ra 1,9 V. OL là chiều ngược, chưa chắc LED chết. Thói quen chân dài đã hỏng, nên quy trình mới có đồng hồ.
3. Nhấc một chân rồi đo lại. Đường song song đọc thấp. Chỉ xét mã màu sau khi con đứng một mình. Board đã tắt nguồn là điều bắt buộc, vẫn chưa đủ.
4. Số đứng yên gần như ngắn, đối với mã 10 kΩ, là cặp dễ nhầm của cuộn cảm (hoặc con đã hỏng). Không được làm điện trở LED. Con 10 kΩ thật sẽ đo gần 10 kΩ.
5. "TO-92, mất mã, không biết transistor hay IC ổn áp, không biết thứ tự chân." Không được nuôi ESP32. Không biết chức năng cộng không biết chân là cách làm ngắn rail.

</details>

## Đọc thêm

- [SparkFun: dùng đồng hồ vạn năng](https://learn.sparkfun.com/tutorials/how-to-use-a-multimeter) — thông mạch, ohm và diode, ba chức năng duy nhất buổi này cho phép.
- [SparkFun: mã màu điện trở](https://learn.sparkfun.com/tutorials/resistors/resistor-color-code) — bốn vạch và năm vạch trên một trang, để đếm lại ở bước 2.
- [Datasheet ESP32 (PDF)](https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf) — rail 3,3 V mà điện trở LED phải tôn trọng, từ bài 07.

## Mua ở Việt Nam

Kit chương 00 đã ở trên bàn thì không mua gì. Danh sách là bài 05, [BOM và cách mua bộ kit robot ở Việt Nam]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %}).

Thiếu món trong danh sách trên bàn thì hai trang là đủ. Breadboard, 35.000₫ ngày 23 tháng 9 năm 2026, là [test board CAMMB-102 trên Hshop](https://hshop.vn/test-board-cammb-102). Đồng hồ, giá trên trang đang bán, là [UNI-T UT33D tại Hshop](https://hshop.vn/dong-ho-van-nang-dien-tu-digital-multimeter-uni-t-ut33d-chinh-hang). Điện trở lẻ, một LED, một diode và một tụ hóa lấy ở [Hshop](https://hshop.vn/), [Thế Giới IC](https://www.thegioiic.com/) và [IC Đầy Rồi](https://icdayroi.com/). Bài này không bịa slug cho chúng. Ghi số in trên diode bạn nhận được.
