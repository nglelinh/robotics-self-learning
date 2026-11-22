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

Buổi học này dành trọn cho thực hành trên bàn lab. Các bài trước đã giới thiệu lần lượt mã màu điện trở, cực tính diode và vạch tụ hóa; hôm nay bạn sẽ tổng hợp tất cả trên một breadboard không cấp điện và ghi lại toàn bộ thành một bảng số đo thực tế. Một bức ảnh chụp đống linh kiện không thể thay thế số liệu đo đạc, và mã màu chưa kiểm chứng bằng đồng hồ chỉ là phỏng đoán rủi ro nếu mang đi hàn lên xe.

## Mục tiêu

Sau buổi thực hành này, bạn sẽ lập được sơ đồ kiểm tra thực tế trên breadboard (nhóm lỗ nào thông mạch, khe nào hở) và chụp ảnh lưu sổ. Bạn sẽ giải mã rồi đo ngoài mạch năm điện trở để quyết định đạt hay loại theo khoảng dung sai. Bạn sẽ dùng thang đo diode kiểm tra một LED và một diode, ghi lại điện áp thuận và xác định rõ chân nào là anode. Bạn cũng sẽ phân biệt rõ ba cặp linh kiện dễ nhầm lẫn (điện trở vạch màu với cuộn cảm vạch màu, tụ gốm với tụ tantali, transistor vỏ TO-92 với IC ổn áp vỏ TO-92) và tránh được ba nguồn sai số phổ biến: đo ohm khi linh kiện còn trong mạch, đồng hồ bị đảo cực que ở chế độ diode, và đọc nhầm điện trở năm vạch thành bốn vạch.

## Kiến thức cần có

Bạn cần ôn lại kiến thức từ bài 02 đến bài 05 về breadboard, cách dùng đồng hồ vạn năng (thang thông mạch, thang ohm, thang diode), mã màu điện trở, tụ điện, diode và LED. Buổi này không dùng mỏ hàn và không cấp nguồn cho TB6612. Nếu thiếu linh kiện nào, hãy viết rõ quy trình đo và đánh dấu `dry-run` thay vì chép số liệu của người khác.

## Vì sao bài này quan trọng

Xe đồ án gồm ESP32 hoặc Pico 3,3 V, mạch lái TB6612, hai động cơ TT dùng pin riêng và cảm biến HC-SR04 có chân echo 5 V. Chỉ một linh kiện nhận diện nhầm cũng đủ gây hỏng mạch: LED báo trên chân GPIO cần đúng điện trở đã đo chứ không phải con bị đọc lệch một bậc mười; tụ đệm 100–470 µF trên chân VM là tụ hóa nhôm có vạch đánh dấu cực âm, trong khi nhiều tụ tantali lại dùng vạch chỉ cực dương nên nhầm quy tắc sẽ làm cháy nổ trên đường nguồn động cơ; còn cắm nhầm IC ổn áp TO-92 vào vị trí transistor (hoặc ngược lại) có thể làm hỏng đường 3,3 V. Bảng số liệu của buổi lab này là bằng chứng bạn đã kiểm soát được từng linh kiện trước khi lắp ráp.

## Dụng cụ và linh kiện trên bàn

Bạn cần chuẩn bị: một đồng hồ vạn năng, một breadboard, năm điện trở, một tụ hóa, một tụ gốm, một LED, một diode và vài sợi dây cắm — tất cả ở trạng thái **không cấp điện**. Tụ gốm có dạng đĩa hoặc khối nhỏ không dấu cực, còn tụ hóa có vỏ trụ nhôm. Với diode, hãy đọc và ghi đúng mã in trên thân con bạn đang cầm (ví dụ phân biệt rõ `1N4001` với `1N4007`).

![Vạch màu sẽ được kiểm, không được tin suông]({{ site.imgurl }}/generated/resistor_color_code.png)

Đặt bảng mã màu bên cạnh năm điện trở khi điền cột giá trị danh định. Nếu số đo trên đồng hồ khác với kết quả giải mã, hãy kiểm tra lại các vạch màu (kể cả khả năng đếm nhầm năm vạch thành bốn vạch) chứ không sửa số đo cho khớp với bảng.

![Vỏ giống nhau, ruột thì không]({{ site.imgurl }}/generated/component_lookalikes.png)

Hình trên minh họa các cặp linh kiện có ngoại hình tương tự nhau nhưng cấu tạo hoàn toàn khác. Trong danh sách phân biệt, bạn cần ghi rõ từng cặp, phép thử áp dụng và kết quả đo đặc trưng.

![Một bộ điện trở, trước khi món nào vào mạch]({{ site.imgurl }}/wikimedia/resistors_assortment.jpg)

Hãy chọn năm trị số khác nhau mà bạn giải mã được, trong đó có ít nhất một giá trị ngoài cặp quen thuộc 220 Ω và 10 kΩ để rèn kỹ năng đọc thực chất.

![Chân nào của tụ là cực âm]({{ site.imgurl }}/generated/capacitor_polarity.png)

Trên tụ hóa vỏ nhôm trong bộ kit, dải vạch luôn chỉ cực âm — nhưng không được áp dụng máy móc quy tắc này cho tụ tantali.

![Cực LED là câu hỏi của đồng hồ nếu chân đã bị cắt]({{ site.imgurl }}/wikimedia/LEDs.jpg)

Dù chân dài thường là anode và mặt vát trên vành thường là cathode, thói quen này không còn đáng tin khi chân đã bị cắt. Kết quả đo ở thang diode mới là căn cứ ghi vào sổ.

## Các bước thực hiện

Toàn bộ buổi thực hành diễn ra trong trạng thái **mất nguồn hoàn toàn** (không cắm USB, không nối pin, không gắn động cơ).

1. **Lập bản đồ thông mạch breadboard:** Chuyển đồng hồ sang thang thông mạch. Đo một nhóm năm lỗ ở khu vực giữa để xác nhận chúng nối chung một nút; đo qua rãnh giữa để xác nhận hở mạch; đo dọc từng thanh nguồn từ đầu đến cuối để kiểm tra xem thanh có bị ngắt đôi ở giữa không và đánh dấu rõ vị trí khe ngắt lên bản vẽ phác thảo. Bản đồ này giúp bạn tránh cảnh "LED không sáng" về sau chỉ vì cắm lệch nút.
2. **Giải mã rồi đo năm điện trở:** Với từng điện trở, ghi dãy màu, trị số danh định và dung sai, sau đó đo ngoài mạch. Khi đo điện trở trị số lớn, không dùng ngón tay kẹp cả hai chân vì điện trở cơ thể người sẽ làm sai lệch kết quả. Một điện trở dung sai 5% (vạch cuối màu vàng kim) chỉ đạt khi nằm trong khoảng:

$$
R_{\mathrm{danh}}(1 - 0{,}05) \le R_{\mathrm{do}} \le R_{\mathrm{danh}}(1 + 0{,}05)
$$

Nếu kết quả đo lệch khỏi cửa sổ, hãy đọc lại vạch màu; nếu vẫn nằm ngoài dung sai, tách riêng linh kiện đó ra khỏi nhóm đạt chuẩn. Đồng thời, chập hai que đo để ghi nhận điện trở nền của dây đo (thường vài phần mười ôm) — mức bù này rất đáng kể khi đo điện trở nhỏ cỡ 10 Ω, nhưng không đáng kể ở cỡ 10 kΩ.

3. **Kiểm tra LED và diode ở thang đo diode:** Ghi lại điện áp thuận và xác định chân vật lý đang chạm que đỏ lúc hiện số đo (sau khi đã xác nhận cực tính que đo của đồng hồ, chân đó chính là anode). Ghi kèm trạng thái `OL` khi đảo que và dấu hiệu nhận dạng ngoài (mặt vát, chân ngắn hoặc vạch cathode). Thông thường LED đỏ đọc khoảng 1,6–2,2 V (có thể sáng mờ), còn diode silic khoảng 0,5–0,8 V. Nếu LED hiện `OL` cả hai chiều, có thể LED đã hỏng hoặc điện áp thử của đồng hồ chưa đủ cao để làm sáng màu LED đó — hãy ghi rõ nhận định của bạn.
4. **Ghi chú ba cặp linh kiện dễ nhầm lẫn:** Chép vào sổ cách phân biệt cả ba cặp dưới đây (ngay cả khi trên bàn bạn mới chỉ có một loại trong cặp):
   - **Điện trở vạch màu và cuộn cảm vạch màu:** Cuộn cảm nhỏ dạng ống cũng có thể in vạch màu giống điện trở, nhưng khi đo bằng thang ohm, điện trở sẽ khớp gần trị số mã màu còn cuộn cảm (vốn là cuộn dây dẫn) chỉ đo được vài ôm hoặc thấp hơn rất nhiều. Nếu cắm nhầm cuộn cảm thay cho điện trở hạn dòng LED, dòng sẽ tăng vọt làm hỏng LED hoặc GPIO.
   - **Tụ gốm và tụ tantali:** Tụ gốm dạng đĩa không phân cực, còn tụ tantali có phân cực và vạch trên nhiều tụ tantali lại đánh dấu **cực dương** (ngược hoàn toàn với tụ hóa nhôm). Nếu không chắc chắn chủng loại, tuyệt đối không mắc ngang đường nguồn VM.
   - **Transistor TO-92 và IC ổn áp TO-92:** Cả hai dùng chung dạng vỏ bán trụ ba chân nên phải dựa hoàn toàn vào mã in trên thân. Mã kiểu `78L05` là IC ổn áp (vào – mass – ra), còn `S8050` hay `BC547` là transistor (thứ tự chân E–B–C phải tra đúng datasheet). Linh kiện bị mờ mất mã phải để riêng và không được dùng cho mạch nguồn ESP32.

## Ba lỗi thường tạo ra số đo giả

1. **Đo điện trở khi linh kiện còn gắn trong mạch:** Khi còn hàn hoặc cắm chung với mạch khác, đồng hồ sẽ đo điện trở tương đương của cả mạng nhánh song song (một điện trở 220 Ω tốt có thể chỉ đọc ra 80 Ω). Luôn nhấc ít nhất một chân ra khỏi mạch trước khi đo.
2. **Nhầm cực tính que đo ở chế độ diode:** Phần lớn đồng hồ số đặt cực dương ở que đỏ, nhưng một số mẫu hoặc thao tác cắm nhầm lỗ có thể làm đảo chiều. Hãy kiểm chứng một lần trên diode đã biết rõ vạch cathode: que nào chạm đầu không vạch mà hiện điện áp thuận thì que đó mang cực dương, rồi ghi chú ngay đầu bảng (`đỏ = dương anode` hoặc `đỏ bị đảo`).
3. **Đọc điện trở năm vạch như bốn vạch:** Điện trở 5 vạch gồm 3 chữ số có nghĩa + hệ số nhân + dung sai, còn loại 4 vạch chỉ có 2 chữ số có nghĩa + hệ số nhân + dung sai. Ví dụ nâu-đen-đen-đỏ-nâu khác hoàn toàn công thức với nâu-đen-đen-vàng. Nếu số đo lệch đúng 10 lần hoặc 100 lần, hãy đếm lại số vạch trước tiên.

## Bảng ghi chép bắt buộc trong sổ lab

Chép bảng sau vào sổ và điền đầy đủ kết quả thực tế (lưu với mã `ch01-10-id-table`):

| # | Linh kiện | Quan sát ban đầu | Danh định hoặc cực tính | Kết quả đo | Đạt? |
|---|-----------|-------------|--------------------|---------|------|
| 1 | Hàng năm lỗ | Ghi rõ cột/lỗ | Một nút chung | Kêu hoặc hở | |
| 2 | Rãnh giữa | Đo qua khe | Hở mạch | Kêu hoặc hở | |
| 3 | Thanh nguồn đỏ | Từ đầu đến cuối | Liền hoặc ngắt đôi | Ghi vị trí ngắt | |
| 4–8 | Năm điện trở | Dãy màu vạch | Trị số Ω và % | Số đo Ω | Có/Không |
| 9 | LED | Chân anode | Dài/ngắn, mặt vát | Điện áp thuận (V) | |
| 10 | Diode | Chân anode | Vạch là cathode | Điện áp thuận (V) | |
| 11 | Tụ hóa | Vị trí vạch | Cực âm | Tên tệp ảnh | |

Các dòng điện trở chỉ đạt khi có đủ cả giá trị giải mã và giá trị đo ngoài mạch; dòng LED chỉ đạt khi có điện áp thuận và xác định rõ chân anode.

## Ví dụ

Xét một điện trở có bốn vạch nâu, đen, đỏ, vàng kim: tương ứng 1, 0, hai chữ số 0 và dung sai 5%, tức $$1{,}0\,\mathrm{k}\Omega \pm 5\%$$. Cửa sổ dung sai là:

$$
1000 \times 0{,}95 = 950,\qquad 1000 \times 1{,}05 = 1050
$$

Đồng hồ đo được 1.027 Ω, nằm trong khoảng 950–1.050 Ω nên đạt. Với điện trở thứ hai mã 220 Ω, khi đo trực tiếp lúc còn cắm cạnh mạch LED trên breadboard chỉ ra 86 Ω; sau khi nhấc một chân ra khỏi mạch, đồng hồ đọc 218 Ω — nằm gọn trong khoảng $$220 \times 0{,}95$$ đến $$220 \times 1{,}05$$ nên đạt (giá trị 86 Ω ban đầu là do ảnh hưởng nhánh song song).

Điện trở thứ ba có năm vạch nhưng bị đọc nhầm theo quy tắc bốn vạch ra 1.000 Ω trong khi đồng hồ đo khoảng 100 Ω; sau khi đếm lại đủ năm vạch (ba chữ số có nghĩa cộng hệ số nhân), kết quả hoàn toàn khớp.

Trên diode đã biết, đầu có vạch là cathode nên đầu kia là anode; đặt que đỏ vào anode và que đen vào vạch cathode cho 0,62 V, đảo que hiện `OL`. Trên LED đỏ, đặt que đỏ vào chân dài cho 1,85 V kèm ánh sáng mờ, chứng tỏ chân dài đúng là anode. Hai mức điện áp thuận khác nhau rõ rệt (~0,6 V với diode thường và ~1,8 V với LED đỏ) cũng giúp khẳng định không bị ghi nhầm giữa hai linh kiện.

## Video tham khảo

- **Xem trước:** [Resistor Color Code Chart Tutorial Review - Physics](https://www.youtube.com/watch?v=G1mZutobxDU) — The Organic Chemistry Tutor, tiếng Anh. Đọc mã màu rồi đối chiếu bằng thang ohm để xác nhận giá trị trước khi lắp mạch.
- [CÁCH SỬ DỤNG ĐỒNG HỒ VẠN NĂNG ĐO ĐIỆN ĐƠN GIẢN](https://www.youtube.com/watch?v=FsBgW0WDQSw) — Sơn Tiện Ích, tiếng Việt. Thực hành sử dụng thang ohm và thang thông mạch giúp phân biệt chính xác các linh kiện dễ nhầm lẫn.

## Bài tập

1. Một điện trở danh định 470 Ω (vạch cuối màu vàng kim) đo ngoài mạch được 502 Ω. Hãy tính khoảng dung sai 5% và đưa ra kết luận đạt hay loại.
2. Ở thang đo diode (đã xác nhận que đỏ mang cực dương), đồng hồ hiện `OL` khi que đỏ chạm chân dài LED và hiện 1,9 V khi que đỏ chạm chân ngắn. Chân nào là anode, và kết quả `OL` mang ý nghĩa gì?
3. Một điện trở 1 kΩ nằm trên mạch đã tắt nguồn nhưng đo được 120 Ω. Bước xử lý đầu tiên bạn cần làm là gì, và vì sao chưa vội kết luận "đọc sai mã màu"?
4. Một linh kiện có các vạch màu giống mã 10 kΩ nhưng đo ngoài mạch chỉ ra 1,2 Ω. Đó nhiều khả năng là linh kiện gì, và có được dùng làm điện trở hạn dòng cho LED 3,3 V không?
5. Bạn gặp một linh kiện vỏ TO-92 bị mờ mất chữ in. Hãy viết ghi chú phân loại cho nó và cho biết có thể dùng nó cho mạch nguồn ESP32 hay không.

<details markdown="1">
<summary>Gợi ý đáp án</summary>

1. Khoảng dung sai 5% là từ $$470 \times 0{,}95 = 446{,}5\,\Omega$$ đến $$470 \times 1{,}05 = 493{,}5\,\Omega$$. Giá trị 502 Ω nằm ngoài khoảng này nên trượt, cần tách riêng.
2. Chân ngắn là anode (vì đặt que đỏ dương vào đó cho sụt thuận 1,9 V). Kết quả `OL` là trạng thái phân cực ngược bình thường, không có nghĩa LED hỏng; trường hợp này cho thấy quy ước chân dài đã không còn đúng và cần tin theo đồng hồ.
3. Nhấc ít nhất một chân điện trở ra khỏi mạch rồi đo lại, vì các nhánh song song trong mạch làm tổng trở đo được thấp hơn thực tế. Tắt nguồn là điều kiện cần nhưng chưa đủ khi đo trong mạch.
4. Nhiều khả năng đó là cuộn cảm dạng vạch màu (hoặc linh kiện đã hỏng ngắn mạch). Tuyệt đối không dùng làm điện trở hạn dòng LED vì trở kháng quá nhỏ sẽ gây quá dòng làm hỏng LED và GPIO.
5. Ghi chú: "Vỏ TO-92, mất mã in, không rõ là transistor hay IC ổn áp và không biết thứ tự chân." Tuyệt đối không dùng để cấp nguồn cho ESP32 vì rất dễ gây ngắn mạch hoặc quá áp đường nguồn.

</details>

## Đọc thêm

- [SparkFun: dùng đồng hồ vạn năng](https://learn.sparkfun.com/tutorials/how-to-use-a-multimeter) — ôn lại ba chức năng dùng trong buổi lab: thông mạch, đo ohm và thang diode.
- [SparkFun: mã màu điện trở](https://learn.sparkfun.com/tutorials/resistors/resistor-color-code) — bảng tra nhanh cho cả điện trở 4 vạch và 5 vạch.
- [Datasheet ESP32 (PDF)](https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf) — tài liệu tham chiếu về giới hạn 3,3 V từ bài 07.

## Mua ở Việt Nam

Nếu đã chuẩn bị đủ bộ dụng cụ từ Chương 00 theo [BOM và cách mua bộ kit robot ở Việt Nam]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %}), bạn không cần mua thêm gì ở bài này.

Nếu còn thiếu dụng cụ đo cơ bản, bạn có thể tham khảo breadboard [test board CAMMB-102 trên Hshop](https://hshop.vn/test-board-cammb-102) (giá tham khảo 35.000 ₫ ngày 23 tháng 9 năm 2026) và đồng hồ vạn năng [UNI-T UT33D+ tại Hshop](https://hshop.vn/dong-ho-van-nang-dien-tu-digital-multimeter-uni-t-ut33d-chinh-hang) (xem giá hiện hành trên trang). Điện trở lẻ, LED, diode và tụ hóa có thể mua trực tiếp tại [Hshop](https://hshop.vn/), [Thế Giới IC](https://www.thegioiic.com/) hoặc [IC Đây Rồi](https://icdayroi.com/), và nhớ ghi lại chính xác mã in trên diode nhận được.
