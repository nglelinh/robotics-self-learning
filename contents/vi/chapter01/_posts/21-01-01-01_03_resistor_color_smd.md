---
layout: post
title: "Nhận điện trở: vạch màu và mã SMD"
chapter: "01"
order: 3
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter01
lesson_type: required
draft: false
---

## Mục tiêu

Sau bài học này, bạn sẽ đọc thành thạo điện trở 4 vạch theo thứ tự: chữ số thứ nhất, chữ số thứ hai, hệ số nhân và dung sai, đồng thời tính được khoảng giá trị cho phép theo dung sai. Bạn sẽ nhận diện nhanh hai mã thông dụng như nâu-đen-đỏ-vàng (1 kΩ ±5%) và nâu-lam-cam-vàng (16 kΩ ±5%), nhận biết điện trở 5 vạch (ba chữ số có nghĩa cộng hệ số nhân), giải mã điện trở dán SMD ba số như `103` hoặc `472`, và hiểu vai trò dấu thập phân của chữ `R` trong mã như `R22`. Bạn cũng sẽ biết cách đối chiếu giá trị đọc được với đồng hồ vạn năng ở trạng thái ngắt nguồn và trừ sai số điện trở dây que đo khi đo trị số nhỏ.

## Cần có gì trước

Bạn cần nắm định luật Ohm từ bài 01 (đặc biệt là $I = V/R$ và lý do đèn báo dùng điện trở quanh 180 Ω) cùng quy tắc đo điện trở của bài 02 (linh kiện không cấp nguồn, que đỏ cắm ở lỗ V/Ω). Bài này chưa yêu cầu hàn linh kiện dán (SMD), nhưng kiến thức đọc mã SMD vẫn rất hữu ích vì các linh kiện nhỏ hàn sẵn trên board ESP32 và module TB6612 đều dùng quy chuẩn này.

## Vì sao xe hai bánh cần đọc chính xác mã điện trở

Đèn báo 3,3 V trên ESP32 hay Pico chỉ sáng đúng thiết kế nếu điện trở bạn cắm thực sự gần mức 180 Ω. Nếu nhầm sang nâu-đen-cam (10 kΩ thay vì 1 kΩ), dòng qua LED chỉ còn:

$$
I = \frac{1.3}{10000} = 0.13\ \mathrm{mA}
$$

khiến đèn tối đến mức dễ nhầm là chân GPIO bị hỏng. Ngược lại, cắm nhầm điện trở vài ôm vào vị trí cần vài trăm ôm sẽ gây quá dòng trực tiếp cho chân vi điều khiển.

Kỹ năng này còn áp dụng rộng rãi hơn ngoài breadboard: từ điện trở kéo lên cho nút nhấn, cầu chia áp cho chân echo của cảm biến HC-SR04 cho tới các điện trở dán trên module mạch lái động cơ. Việc đọc chính xác và đo kiểm linh kiện trước khi lắp mạch giúp loại trừ hoàn toàn các lỗi chủ quan do nhầm trị số.

## Điện trở 4 vạch và 5 vạch màu

Với điện trở 4 vạch tiêu chuẩn, bạn đặt đầu có các vạch nằm sát nhau về bên trái, còn vạch dung sai (thường là màu vàng nhũ hoặc bạc ở linh kiện phổ thông) về bên phải. Hai vạch đầu biểu thị hai chữ số có nghĩa, vạch thứ ba là hệ số nhân (lũy thừa của 10), và vạch thứ tư là dung sai — cho biết trị số thực tế được phép lệch bao nhiêu phần trăm so với trị số danh định.

Bảng quy ước màu chữ số: đen 0, nâu 1, đỏ 2, cam 3, vàng 4, lục 5, lam 6, tím 7, xám 8, trắng 9. Hệ số nhân dùng cùng bảng số mũ của 10: đen ×1, nâu ×10, đỏ ×100, cam ×1.000, vàng ×10.000. Riêng màu vàng kim (nhũ vàng) ở vị trí hệ số nhân nghĩa là ×0,1, còn ở vị trí dung sai là ±5%; màu bạc ở vị trí dung sai là ±10%.

Xét ví dụ đầu tiên: **nâu – đen – đỏ – vàng (kim)**. Nâu = 1, đen = 0, đỏ = ×100:

$$
10 \times 100 = 1000\ \Omega = 1\ \mathrm{k}\Omega
$$

Với dung sai ±5%, khoảng giá trị hợp lệ là từ 950 Ω đến 1.050 Ω. Do đó nếu đồng hồ đo được 980 Ω, linh kiện vẫn hoàn toàn đạt chuẩn.

Xét ví dụ thứ hai: **nâu – lam – cam – vàng (kim)**. Nâu = 1, lam = 6, cam = ×1.000:

$$
16 \times 1000 = 16000\ \Omega = 16\ \mathrm{k}\Omega
$$

Khoảng dung sai ±5% tương ứng từ 15,2 kΩ đến 16,8 kΩ. Nếu bạn xoay ngược điện trở và bắt đầu đọc từ vạch vàng kim thì sẽ ra kết quả vô nghĩa vì vàng kim không đại diện cho chữ số có nghĩa.

![Mã bốn vạch, vạch dung sai nằm bên phải]({{ site.imgurl }}/generated/resistor_color_code.png)

Điện trở **5 vạch** bổ sung thêm một chữ số có nghĩa thứ ba trước hệ số nhân, còn vạch cuối cùng vẫn là dung sai. Ví dụ **nâu – đen – đen – đỏ – nâu** tương ứng 1, 0, 0, ×100, ±1%:

$$
100 \times 100 = 10\ \mathrm{k}\Omega
$$

với sai số ±1%. Bạn không bắt buộc phải mua bộ điện trở 5 vạch để làm robot, nhưng cần tạo thói quen đếm tổng số vạch trước khi đọc, bởi nếu đọc nhầm một con 5 vạch theo quy tắc 4 vạch thì hệ số nhân sẽ bị lệch hẳn một bậc mười.

## Mã điện trở dán SMD

Mã SMD 3 chữ số hoạt động theo cùng nguyên lý nhưng được in trực tiếp bằng số: hai chữ số đầu là phần có nghĩa, chữ số thứ ba là số mũ của 10. Ví dụ `103` là $10 \times 10^3 = 10\ \mathrm{k}\Omega$, còn `472` là $47 \times 10^2 = 4700\ \Omega = 4{,}7\ \mathrm{k}\Omega$. Đặc biệt lưu ý mã `100` là $10 \times 10^0 = 10\ \Omega$, không phải 100 Ω — chữ số 0 cuối cùng là số mũ (nghĩa là thêm không chữ số 0).

Đối với trị số nhỏ hơn 10 Ω, chữ cái `R` đóng vai trò dấu phẩy thập phân: `R22` nghĩa là 0,22 Ω và `4R7` nghĩa là 4,7 Ω. Chữ `R` rất nhỏ trên thân linh kiện tối màu nhưng mang ý nghĩa sống còn: dùng nhầm một điện trở 0,22 Ω làm điện trở hạn dòng LED trên 3,3 V gần như tương đương ngắn mạch.

Mã SMD 4 chữ số mở rộng lên ba chữ số có nghĩa cộng một chữ số mũ: ví dụ `4701` là $470 \times 10^1 = 4{,}7\ \mathrm{k}\Omega$. Riêng chuẩn **EIA-96** (thường gặp trên điện trở dán sai số 1%) gồm hai chữ số và một chữ cái, trong đó hai chữ số là mã tra bảng chứ không phải trị số trực tiếp. Bạn không cần học thuộc bảng EIA-96; khi thấy ký hiệu gồm hai số kèm một chữ cái, hãy tra bảng hoặc đo bằng đồng hồ thay vì đoán theo kiểu "01 là 1 Ω".

![Một hộp hỗn hợp: vạch, thân, và công suất không phải cùng một thông tin]({{ site.imgurl }}/wikimedia/resistors_assortment.jpg)

Kích thước thân điện trở phản ánh khả năng tản công suất chứ không cho biết trị số điện trở. Điện trở xuyên lỗ 1/4 W là cỡ mặc định trong chương này; các thân sứ lớn hơn thường chịu 1 W trở lên. Như đã tính ở bài 01, mạch LED chỉ tỏa khoảng 0,012 W nên cỡ 1/4 W rất thoải mái — nhưng điều đó không có nghĩa bạn có thể dùng một điện trở 10 Ω công suất 1/4 W làm tải giả cho động cơ đang kẹt.

## Ví dụ: giải mã năm trị số và đối chiếu đồng hồ

Hãy tự giải năm mã sau trước khi xoay núm đồng hồ:

1. Nâu – đen – đỏ – vàng (kim) → $10 \times 100 = 1\ \mathrm{k}\Omega \pm 5\%$, khoảng hợp lệ 950 Ω đến 1.050 Ω.
2. Nâu – lam – cam – vàng (kim) → $16 \times 1000 = 16\ \mathrm{k}\Omega \pm 5\%$, khoảng hợp lệ 15,2 kΩ đến 16,8 kΩ.
3. Đỏ – đỏ – nâu – vàng (kim) → $22 \times 10 = 220\ \Omega \pm 5\%$, khoảng hợp lệ 209 Ω đến 231 Ω (phương án thay thế cho 180 Ω ở mạch LED).
4. SMD `103` → $10 \times 10^3 = 10\ \mathrm{k}\Omega$.
5. SMD `R22` → 0,22 Ω (`R` là dấu thập phân).

Thay trị số mục 3 (220 Ω) vào công thức đèn báo bài 01 ($V_f = 2{,}0\ \mathrm{V}$ trên nguồn 3,3 V):

$$
I = \frac{3.3 - 2.0}{220} = \frac{1.3}{220} \approx 5.9\ \mathrm{mA}
$$

Công suất trên điện trở lúc này là $P = I^2 R \approx (0{,}0059)^2 \times 220 \approx 0{,}008\ \mathrm{W}$, rất nhỏ so với mức 0,25 W. Nếu đọc nhầm sang nâu-đen-cam (10 kΩ), dòng tụt xuống 0,13 mA khiến đèn gần như không sáng; còn nếu nhầm sang `R22` (0,22 Ω), dòng lý thuyết lên tới $I = 1{,}3 / 0{,}22 \approx 6\ \mathrm{A}$, vượt xa khả năng chịu đựng của cả LED lẫn chân GPIO.

Khi đo kiểm trên đồng hồ, điện trở dung sai 5% chỉ cần rơi trong khoảng hợp lệ là đạt (ví dụ lệch thấp 2% vẫn là linh kiện tốt). Ở dải đo nhỏ, cần chú ý hai yếu tố gây sai số: thứ nhất, nhiệt độ tay người khi kẹp trực tiếp lên thân điện trở màng có thể làm số đo trôi nhẹ, nên chỉ giữ một chân hoặc đặt linh kiện trên mặt bàn; thứ hai, với điện trở dưới vài ôm, bản thân dây và que đo đồng hồ đã có điện trở vài phần mười ôm — hãy chập hai que đo để ghi nhận giá trị nền rồi trừ ra trước khi kết luận về một điện trở như `R22`. Tuyệt đối không hiệu chuẩn đồng hồ bằng cách đo linh kiện trên mạch đang có điện.

## Thực hành

1. Chọn năm điện trở bất kỳ trong bộ kit (hoặc dùng năm ví dụ ở trên nếu kit chưa giao tới). Ghi rõ dãy vạch màu hoặc mã SMD, trị số danh định và khoảng dung sai cho phép ra giấy.
2. Đảm bảo mạch hoàn toàn mất nguồn và điện trở nằm rời ngoài mạch. Kiểm tra que đen ở COM, que đỏ ở lỗ V/Ω, vặn núm sang thang đo Ω (nếu đồng hồ chỉnh thang thủ công, bắt đầu từ thang lớn hơn trị số dự kiến).
3. Đo lần lượt từng điện trở và ghi kết quả bên cạnh giá trị đã giải mã. Nếu điện trở 5% rơi ngoài khoảng dung sai, kiểm tra lại xem bạn có đọc ngược từ vạch vàng kim hoặc đếm nhầm 5 vạch thành 4 vạch không.
4. Với bất kỳ điện trở nào dưới khoảng 10 Ω, chập hai que đo trước để ghi điện trở dây đo rồi trừ phần chênh lệch đó khỏi kết quả.
5. (Tùy chọn) Lắp lại điện trở 180 Ω hoặc 220 Ω vào mạch LED của bài 01 và đo trong mạch khi đã ngắt nguồn; nhận xét xem có nhánh linh kiện nào mắc song song ảnh hưởng đến số đo không (nếu không chắc chắn, hãy nhấc một chân điện trở lên khỏi breadboard để đo độc lập).

**Kết quả kỳ vọng:** Các điện trở tốt và đọc đúng mã sẽ cho số đo nằm gọn trong khoảng dung sai (ví dụ 1 kΩ ±5% đo được 1,02 kΩ là đạt). Nếu bạn thử ở thang thông mạch, đồng hồ sẽ không kêu với cả năm con — điều đó là hoàn toàn bình thường.

| Hiện tượng quan sát | Nguyên nhân thường gặp | Cách khắc phục |
| --- | --- | --- |
| Kết quả đo gấp ~10 lần hoặc bằng ~0,1 lần giá trị đọc | Đọc ngược chiều từ vạch dung sai, hoặc đọc nhầm 5 vạch thành 4 vạch | Xoay vạch vàng kim/bạc về bên phải và đếm lại tổng số vạch |
| Điện trở tưởng là 1 kΩ nhưng đo gần 10 kΩ | Nhầm màu vạch hệ số nhân giữa đỏ và cam | Soi kỹ vạch thứ ba dưới ánh sáng trắng tốt (đỏ và cam rất dễ lẫn) |
| Điện trở trị số nhỏ luôn đo dư thêm ~0,4 Ω | Cộng thêm điện trở của chính cặp dây que đo | Chập hai que đo để ghi điện trở dây rồi trừ đi |
| Số đo điện trở nhảy loạn khi đặt trên board | Mạch vẫn đang được cấp nguồn | Ngắt hoàn toàn nguồn điện trước khi đo thang Ω |
| Thang thông mạch im lặng trên điện trở 220 Ω | Nhầm thang thông mạch với thang đo Ω | Chuyển núm xoay sang thang Ω; việc không kêu ở đây là đúng |

**Lưu ý an toàn:** Không đo thang Ω trên đường nguồn đang có điện, trên pin hay chân VM của mạch lái; luôn giữ que đỏ ở lỗ V/Ω để tránh ngắn mạch khi chuyển sang đo áp trên chân 3,3 V sau đó.

## Video tham khảo

- **Xem trước:** [Resistor Color Code Chart Tutorial Review - Physics](https://www.youtube.com/watch?v=G1mZutobxDU) — The Organic Chemistry Tutor, tiếng Anh. Hướng dẫn cách đọc điện trở 4 vạch màu và tính dung sai; hãy luôn đối chiếu lại bằng đồng hồ vạn năng.
- [How to Read Resistor Color Codes | 4-Band Resistor Values and Tolerance](https://www.youtube.com/watch?v=GLD7AgAYqwA) — Engineering Technology Simulation Learning Videos, tiếng Anh. Giải mã chậm từng vạch màu trên điện trở 4 vạch, phù hợp làm đối chứng cho bài thực hành.

## Bài tập

1. Giải mã các điện trở 4 vạch sau (nêu trị số danh định và khoảng dung sai ±5%): vàng-tím-nâu-vàng(kim), cam-cam-đỏ-vàng(kim), và lam-xám-đen-vàng(kim).
2. Một người đọc một điện trở thành vàng(kim)-cam-tím-đỏ. Họ đã mắc lỗi gì, và trị số đúng là bao nhiêu khi đọc theo thứ tự đỏ-tím-cam-vàng(kim)?
3. Giải mã các điện trở SMD sau: `222`, `510`, `4R7` và `1003`. Mã nào trong số này (nếu có) có giá trị 10 kΩ?
4. Một điện trở 1 kΩ ±5% đo ngoài mạch được 980 Ω. Linh kiện này đạt hay loại, và độ lệch so với 1.000 Ω là bao nhiêu phần trăm?
5. Điện trở kéo lên (pull-up) cho nút nhấn trên chân GPIO 3,3 V theo thiết kế là 10 kΩ, nhưng thực tế bị cắm nhầm điện trở nâu-đen-đỏ-vàng(kim). Hãy tính dòng điện khi nhấn nút nối chân xuống mass và so sánh với khi dùng đúng 10 kΩ.

<details>
<summary>Gợi ý đáp án</summary>

1. Vàng-tím-nâu-vàng(kim): $47 \times 10 = 470\ \Omega$, khoảng 446,5 Ω đến 493,5 Ω (làm tròn 447 Ω đến 494 Ω). Cam-cam-đỏ-vàng(kim): $33 \times 100 = 3{,}3\ \mathrm{k}\Omega$, khoảng 3,14 kΩ đến 3,47 kΩ. Lam-xám-đen-vàng(kim): $68 \times 1 = 68\ \Omega$, khoảng 65 Ω đến 71 Ω.
2. Họ đã đặt vạch dung sai (vàng kim) ở bên trái thay vì bên phải. Đọc đúng chiều đỏ-tím-cam-vàng(kim) cho $27 \times 1000 = 27\ \mathrm{k}\Omega \pm 5\%$.
3. `222` là $22 \times 10^2 = 2{,}2\ \mathrm{k}\Omega$; `510` là $51 \times 10^0 = 51\ \Omega$; `4R7` là 4,7 Ω; `1003` là $100 \times 10^3 = 100\ \mathrm{k}\Omega$. Không mã nào là 10 kΩ (mã 3 chữ số của 10 kΩ là `103`).
4. 980 Ω nằm gọn trong khoảng 950 Ω đến 1.050 Ω, với sai số $20/1000 = 2\% < 5\%$, nên giữ lại dùng bình thường.
5. Nâu-đen-đỏ-vàng(kim) là 1 kΩ, nên khi nhấn giữ nút, dòng qua điện trở là $I = 3{,}3 / 1000 = 3{,}3\ \mathrm{mA}$. Với điện trở kéo lên 10 kΩ, dòng chỉ là $3{,}3 / 10000 = 0{,}33\ \mathrm{mA}$. Dù cả hai đều nằm trong giới hạn an toàn, mức 10 kΩ tiêu thụ ít dòng hơn gấp 10 lần và phù hợp hơn cho mạch kéo lên nút nhấn.

</details>

## Đọc thêm

Bài hướng dẫn của SparkFun tổng hợp đầy đủ mã màu, công suất và cách mắc điện trở: [Resistors](https://learn.sparkfun.com/tutorials/resistors). Khi màu vạch khó phân biệt dưới ánh sáng yếu, bạn có thể tra nhanh bằng [máy tính mã màu điện trở của Digi-Key](https://www.digikey.com/en/resources/conversion-calculators/conversion-calculator-resistor-color-code) rồi kiểm chứng lại trên đồng hồ vạn năng.

## Mua ở Việt Nam

Toàn bộ bộ kit robot nằm ở bài [BOM và cách mua bộ kit robot ở Việt Nam]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %}). Bài này chỉ cần thêm một bộ điện trở xuyên lỗ.

Do thời điểm khảo sát Hshop không hiển thị bộ điện trở 1/4 W phổ thông, bạn có thể tìm mua qua trang tìm kiếm: [Shopee, tìm bộ điện trở 1/4W](https://shopee.vn/search?keyword=b%E1%BB%99%20%C4%91i%E1%BB%87n%20tr%E1%BB%9F%201%2F4W). Hãy đọc kỹ mô tả để chọn loại 1/4 W, sai số 5% hoặc 1%, ưu tiên bộ có sẵn các trị số 180 Ω hoặc 220 Ω cùng 1 kΩ và 10 kΩ. Ngoài ra, bạn có thể mua điện trở lẻ có dán nhãn trị số tại các cửa hàng linh kiện như [Thế Giới IC](https://www.thegioiic.com/) hoặc [IC Đây Rồi](https://icdayroi.com/), và vẫn đo kiểm tra lại bằng đồng hồ trong bài thực hành.
