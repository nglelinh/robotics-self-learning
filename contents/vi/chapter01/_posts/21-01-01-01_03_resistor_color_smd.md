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

Học xong, bạn đọc điện trở bốn vạch theo thứ tự chữ số, chữ số, hệ số nhân, và dung sai, rồi tính khoảng giá trị dung sai cho phép. Bạn giải mã nâu-đen-đỏ-vàng thành 1 kΩ ±5% và nâu-lam-cam-vàng thành 16 kΩ ±5% mà không phải tính lại từ đầu. Bạn nhận ra hàng năm vạch là ba chữ số cộng hệ số nhân, đọc mã SMD ba số như 103 hoặc 472, và coi chữ R trong mã kiểu R22 là dấu phẩy thập phân. Bạn đối chiếu giá trị vừa giải với đồng hồ khi mạch mất nguồn, và biết lúc nào điện trở của que đo mới là thứ mình đang thấy.

## Cần có gì trước

Cần định luật Ohm ở bài đầu, nhất là $I = V/R$ và lý do đèn báo dùng khoảng 180 Ω chứ không phải hình trụ nào nằm gần mỏ hàn. Cần thói quen đo ôm của bài trước: linh kiện mất nguồn, que đỏ ở ổ điện áp/ôm, không ở ổ dòng. Chưa phải hàn SMD. Kit toàn chân xuyên lỗ thì phần SMD vẫn đáng đọc, vì cùng kiểu mã đang in trên linh kiện nhỏ đã hàn sẵn trên board ESP32 và module TB6612.

## Vì sao xe hai bánh cần biết vạch màu

Đèn 3,3 V trên ESP32 hoặc Pico chỉ sáng đúng nếu hình trụ vừa cắm thực sự gần 180 Ω. Nâu-đen-cam là 10 kΩ, không phải 1 kΩ, và đèn khi đó chạy ở

$$
I = \frac{1.3}{10000} = 0.13\ \mathrm{mA}
$$

trông như GPIO chết trong phòng có đèn. Lỗi ngược lại, vài ôm ở chỗ cần vài trăm ôm, xả thẳng chân cắm.

Cùng kỹ năng ấy xuất hiện ngoài breadboard. Điện trở kéo lên của nút nhấn, điện trở nối tiếp bạn có thể dùng sau này để thu echo của HC-SR04, và các con nhỏ trên module driver đều là điện trở, hoặc có vạch hoặc có mã in. TB6612 không an toàn hơn chỉ vì con trở "trông hơi đỏ". Hai mô-tơ TT vẫn không được đối xử như điện trở trên GPIO. Đọc linh kiện trước, rồi mới quyết định nó có được vào mạch hay không.

## Bốn vạch, rồi đến năm

Điện trở bốn vạch chuẩn được đọc từ đầu sát các vạch, vạch dung sai — trên đồ chơi gần như luôn là vàng hoặc bạc — để bên phải. Hai vạch đầu là chữ số có nghĩa. Vạch thứ ba là hệ số nhân, một luỹ thừa của mười. Vạch thứ tư là dung sai, tức giá trị thật được phép lệch bao xa so với số sơn.

Màu chữ số dùng trong khóa này: đen 0, nâu 1, đỏ 2, cam 3, vàng 4, lục 5, lam 6, tím 7, xám 8, trắng 9. Hệ số nhân dùng cùng bảng màu như luỹ thừa mười: đen ×1, nâu ×10, đỏ ×100, cam ×1 000, vàng ×10 000. Vàng khi là hệ số nhân nghĩa là ×0,1, khi là vạch dung sai nghĩa là ±5%. Bạc ở vạch dung sai là ±10%.

Nâu, đen, đỏ, vàng là số đầu tiên bạn nên đọc thành tiếng. Nâu là 1, đen là 0, đỏ nghĩa là ×100:

$$
10 \times 100 = 1000\ \Omega = 1\ \mathrm{k}\Omega
$$

Vàng nói ±5%, nên khoảng thật là 950 Ω đến 1 050 Ω. Đồng hồ đọc 980 Ω là con tốt, không phải hàng giả.

Nâu, lam, cam, vàng là số thứ hai. Nâu là 1, lam là 6, cam nghĩa là ×1 000:

$$
16 \times 1000 = 16000\ \Omega = 16\ \mathrm{k}\Omega
$$

cũng ±5%, khoảng 15,2 kΩ đến 16,8 kΩ. Lật ngược điện trở và bắt đầu từ vạch vàng thì mã thành vô nghĩa, vì vàng không phải chữ số.

![Mã bốn vạch, vạch dung sai nằm bên phải]({{ site.imgurl }}/generated/resistor_color_code.png)

Điện trở năm vạch thêm một chữ số có nghĩa nữa trước hệ số nhân, vạch cuối vẫn là dung sai. Nâu-đen-đen-đỏ-nâu là 1, 0, 0, ×100, ±1%:

$$
100 \times 100 = 10\ \mathrm{k}\Omega
$$

trong khoảng ±1%. Không cần cả ngăn kéo năm vạch mới ráp được xe. Cần nhận ra khi một con có bốn vạch chữ số và vạch dung sai thứ năm, vì đọc nó như bốn vạch sẽ lệch hệ số nhân một bậc mười. Đếm vạch trước khi nhân.

## Mã SMD, kể cả chữ cái không cần học thuộc

Mã điện trở SMD ba chữ số là cùng ý ấy, in bằng mực. Hai số đầu là phần có nghĩa. Số thứ ba là luỹ thừa của mười. Vậy 103 là $10 \times 10^3 = 10\ \mathrm{k}\Omega$, và 472 là $47 \times 10^2 = 4700\ \Omega = 4{,}7\ \mathrm{k}\Omega$. Mã 100 là $10 \times 10^0 = 10\ \Omega$, không phải 100 Ω. Số 0 đứng cuối là số mũ, không phải một chữ số để viết thêm vào đuôi.

Khi giá trị dưới 10 Ω, chữ R đứng chỗ dấu phẩy. R22 nghĩa là 0,22 Ω. 4R7 nghĩa là 4,7 Ω. Chữ R dễ mất trên thân tối, và nó quan trọng: con 0,22 Ω dùng làm điện trở LED từ 3,3 V gần như là một ngắn mạch.

Mã bốn số kéo cùng quy tắc ra ba chữ số có nghĩa: 4701 là $470 \times 10^1 = 4{,}7\ \mathrm{k}\Omega$. Hệ EIA-96 thì khác. Nó in hai chữ số cộng một chữ cái, và hai chữ số là chỉ số tra bảng chứ không phải chính điện trở. Bạn sẽ gặp trên hàng SMD 1%. Đừng học thuộc bảng. Thấy hai số và một chữ thì tra, hoặc đo. Đoán bừa biến chỉ số "01" thành một điện trở một ôm mà không phải một ôm.

![Một hộp hỗn hợp: vạch, thân, và công suất không phải cùng một thông tin]({{ site.imgurl }}/wikimedia/resistors_assortment.jpg)

Cỡ thân gợi ý công suất, không gợi ý điện trở. Trụ xuyên lỗ 1/4 W là mặc định của chương này. Thân sứ to hơn có thể là 1 W trở lên và có thể xếp vạch khác. Phép tính LED ở bài đầu tản khoảng 0,011 W, nên 1/4 W ở đó là thoải mái. Nó không biến một con 10 Ω, 1/4 W thành tải giả an toàn cho mô-tơ đang kẹt.

## Ví dụ: năm mã, rồi cửa sổ của đồng hồ

Giải những mã này trước khi đụng núm vặn.

1. Nâu, đen, đỏ, vàng → $10 \times 100 = 1\ \mathrm{k}\Omega$, ±5%, cửa sổ 950 Ω đến 1 050 Ω.
2. Nâu, lam, cam, vàng → $16 \times 1000 = 16\ \mathrm{k}\Omega$, ±5%, cửa sổ 15,2 kΩ đến 16,8 kΩ.
3. Đỏ, đỏ, nâu, vàng → $22 \times 10 = 220\ \Omega$, ±5%, khoảng 209 Ω đến 231 Ω. Đây là điện trở đèn thay thế khi thiếu 180 Ω.
4. SMD 103 → $10 \times 10^3 = 10\ \mathrm{k}\Omega$.
5. SMD R22 → 0,22 Ω. Chữ R là dấu phẩy, không phải một màu.

Đưa mục 3 vào công thức đèn của bài 1, $V_f = 2{,}0\ \mathrm{V}$ trên rail 3,3 V:

$$
I = \frac{3.3 - 2.0}{220} = \frac{1.3}{220} \approx 5.9\ \mathrm{mA}
$$

Công suất trên điện trở đó là $P = I^2 R \approx (0{,}0059)^2 \times 220 \approx 0{,}008\ \mathrm{W}$, vẫn là một phần nhỏ của 1/4 W. Cùng công thức với nâu-đen-cam bị đọc nhầm (10 kΩ) cho 0,13 mA và một đèn bạn sẽ gọi là chết. Cùng công thức với R22 cho $I = 1{,}3 / 0{,}22 \approx 6\ \mathrm{A}$, dòng mà cả LED lẫn GPIO đều không sống nổi. Mã không phải gợi ý.

Trên đồng hồ, con sai số 5% phải rơi trong cửa sổ của nó. Đọc thấp 2% vẫn là con tốt. Hai hiệu ứng hay lừa ở đầu thang thấp. Hơi tay trên điện trở màng làm giá trị trôi một chút khi bạn kẹp thân; giữ chân, đừng kẹp viên, hoặc buông ra vài giây. Với con dưới vài ôm, chính que và dây đo cũng vài phần mười ôm. Chập hai que, ghi độ lệch đó, rồi trừ đi trước khi kết tội mã R22. Đừng "zero" đồng hồ bằng cách đo một điện trở còn hàn trên board đang có điện.

## Thực hành

1. Lấy năm điện trở trong kit, hoặc dùng năm mã ở ví dụ nếu kit chưa về. Viết cách đọc vạch hoặc mã SMD và số ôm bạn khẳng định, kèm cửa sổ ± với hàng có vạch.
2. Nguồn tắt. Không có gì cắm vào điện trở. Que đỏ ở ổ điện áp/ôm, đen ở COM, núm ở thang ôm. Đồng hồ chọn thang tay thì bắt đầu ở thang cao hơn giá trị bạn chờ.
3. Đo từng con. Viết số đồng hồ cạnh giá trị đã giải. Con 5% phải nằm trong cửa sổ. Nếu không, kiểm tra xem bạn có bắt đầu từ vạch vàng không, và có đếm nhầm năm vạch thành bốn không.
4. Con nào dưới khoảng 10 Ω thì chập que trước, ghi điện trở đó, rồi trừ.
5. Tuỳ chọn: đặt con 180 Ω hoặc 220 Ω lại vào vòng LED của bài 1, chỉ đo trong mạch khi nguồn đã rút. Nói xem linh kiện bên cạnh có thể song song với nó không. Không chắc thì nhấc một chân.

Bạn sẽ thấy số đo nằm trong dung sai với những con còn lành và được đọc đúng. Con 1 kΩ ±5% đọc 1,02 kΩ là đạt. Thang thông mạch có lẽ im với cả năm con, và đó không phải lỗi của điện trở.

| Bạn thấy | Nguyên nhân hay gặp | Cách xử lý |
| --- | --- | --- |
| Đồng hồ ra khoảng 10 lần hoặc 0,1 lần giá trị đã giải | Đọc vạch từ đầu sai, hoặc năm vạch bị đọc như bốn | Đặt vàng hoặc bạc bên phải và đếm lại vạch. |
| Con "1 kΩ" đọc gần 10 kΩ | Vạch nhân bị thấy là đỏ trong khi nó là cam, hoặc ngược lại | Soi vạch thứ ba dưới đèn. Cam và đỏ là cặp hay lẫn. |
| Con ôm thấp luôn cao hơn 0,4 Ω | Điện trở của que và dây | Trừ số đo khi hai que chập nhau. |
| Số ôm trôi trong khi board còn nguồn | Nguồn chưa rút | Rút. Thang ôm không dành cho rail đang sống. |
| Thông mạch im trên con 220 Ω | Thông mạch không phải thang ôm | Chuyển sang Ω. Im ở đây là đúng. |

An toàn: không đo ôm trên rail có điện, trên pin, hoặc trên chân VM của driver. Pin 2S không phải điện trở. Que đỏ không nằm ở ổ dòng, để lần đo áp sau trên chân 3,3 V không thành một ngắn mạch.

## Bài tập

1. Giải vàng-tím-nâu-vàng, cam-cam-đỏ-vàng, và lam-xám-đen-vàng. Cho giá trị danh định và cửa sổ ±5%.
2. Có người đọc một điện trở thành vàng-cam-tím-đỏ. Họ đã làm gì, và cách đọc bốn vạch hợp lệ là gì nếu các màu đó là đỏ, tím, cam, vàng?
3. Giải SMD 222, 510, 4R7 và 1003. Cái nào, nếu có, là 10 kΩ?
4. Con 1 kΩ ±5% đo được 980 Ω khi mất nguồn. Giữ hay loại? 980 Ω lệch bao nhiêu phần trăm so với 1 000 Ω?
5. Điện trở kéo lên của nút trên GPIO 3,3 V lẽ ra là 10 kΩ. Con đang cắm là nâu-đen-đỏ-vàng. Ước lượng dòng khi nút ngắn chân xuống mass, và nói chân vui hơn với con này hay với kéo lên 10 kΩ thật.

<details>
<summary>Gợi ý đáp án</summary>

1. Vàng-tím-nâu-vàng là $47 \times 10 = 470\ \Omega$, khoảng 447 Ω đến 494 Ω. Cam-cam-đỏ-vàng là $33 \times 100 = 3{,}3\ \mathrm{k}\Omega$, khoảng 3,14 kΩ đến 3,47 kΩ. Lam-xám-đen-vàng là $68 \times 1 = 68\ \Omega$, khoảng 65 Ω đến 71 Ω.
2. Vàng bị đặt bên trái. Vàng là dung sai nên phải ở bên phải. Cách đọc đúng là đỏ-tím-cam-vàng: $27 \times 1000 = 27\ \mathrm{k}\Omega$, ±5%.
3. 222 là $22 \times 10^2 = 2{,}2\ \mathrm{k}\Omega$. 510 là $51 \times 10^0 = 51\ \Omega$. 4R7 là 4,7 Ω. 1003 là $100 \times 10^3 = 100\ \mathrm{k}\Omega$. Không cái nào là 10 kΩ. Mã ba số của 10 kΩ là 103.
4. 980 Ω nằm trong 950 Ω đến 1 050 Ω. Sai số $20/1000 = 2\%$, trong băng 5%. Giữ.
5. Nâu-đen-đỏ-vàng là 1 kΩ, nên $I = 3{,}3 / 1000 = 3{,}3\ \mathrm{mA}$ khi nút bị giữ. Kéo lên 10 kΩ chỉ lấy $3{,}3 / 10000 = 0{,}33\ \mathrm{mA}$. Cả hai đều trong ngân sách GPIO thô 12 mA đến 40 mA, và 10 kΩ dịu hơn. Con 1 kΩ là họ hàng của điện trở đèn, không phải điện trở nút tốt hơn.

</details>

## Đọc thêm

Bài điện trở của SparkFun gồm vạch màu, công suất, và mắc nối tiếp song song mà bạn đã dùng cho LED: [Resistors](https://learn.sparkfun.com/tutorials/resistors). Vạch nào tối nghĩa dưới đèn xấu thì máy tính nhanh hơn một lần đoán thứ hai: [máy tính mã màu điện trở của Digi-Key](https://www.digikey.com/en/resources/conversion-calculators/conversion-calculator-resistor-color-code). Dùng để tự kiểm, rồi vẫn đặt con lên đồng hồ.

## Mua ở Việt Nam

Cả giỏ hàng nằm ở [BOM và cách mua bộ kit robot ở Việt Nam]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %}). Bài này chỉ thêm một bộ điện trở.

Lúc viết trang này, tìm "điện trở" trên Hshop không ra bộ 1/4 W. Dùng trang tìm kiếm, đừng đoán slug sản phẩm: [Shopee, tìm bộ điện trở 1/4W](https://shopee.vn/search?keyword=b%E1%BB%99%20%C4%91i%E1%BB%87n%20tr%E1%BB%9F%201%2F4W). URL đó là trang tìm kiếm. Đọc listing xem có ghi 1/4 W và 5% hoặc 1% không, ưu tiên bộ có 180 Ω hoặc 220 Ω cùng 1 kΩ và 10 kΩ. Xem giá đúng ngày đặt. Điện trở lẻ ở quầy linh kiện như [Thế Giới IC](https://www.thegioiic.com/) hoặc [IC Đây Rồi](https://icdayroi.com/) cũng được nếu túi có nhãn, và bạn vẫn đo năm con trong bài lab.
