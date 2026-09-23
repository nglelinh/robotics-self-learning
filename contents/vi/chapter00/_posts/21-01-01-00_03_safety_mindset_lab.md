---
layout: post
title: "Tư duy an toàn cho lab robot"
chapter: "00"
order: 3
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter00
lesson_type: required
draft: false
---

Dành cho bài này 80 phút. Bạn đạt được bằng giấy trước khi bưu kiện tới. Nếu mỏ hàn hoặc cell lithium đã ở trên bàn, các quy tắc áp dụng ngay.

## Mục tiêu học

Bạn sẽ **gọi tên** ba mối nguy thật sự có trên bàn này: năng lượng tích trữ, bánh đang quay, và firmware quên tắt PWM. Bạn sẽ **viết** một thẻ lên nguồn một trang, thứ tự điện là mass chung, rồi logic từ USB, rồi tín hiệu, rồi VM motor cuối cùng, bánh đã nhấc sẵn. Bạn sẽ **áp** quy tắc lithium: sạc 18650 từng cell một tới 4,2 V, và không bao giờ kẹp TP4056 qua một đế 2S, tức pack 8,4 V khi đầy. Bạn sẽ **từ chối** kế hoạch đưa điện áp motor, hoặc echo 5 V, vào chân 3,3 V, vì điện áp cực đại tuyệt đối của GPIO ESP32 không phải 5 V. Bạn sẽ **chạy** checklist bật nguồn chỉ bằng USB, chưa có motor, và **khớp** triệu chứng với cách xử lý trong bảng lỗi.

## Cần có trước

Bài 00-01 và 00-02: bạn nói được quy tắc dừng 300 ms, và sổ có một câu lộ trình A hoặc B. Chưa cần linh kiện. Chân GPIO là chân logic, không phải nguồn, và một bánh trên mặt bàn thành cái tời ngay khi PWM khác không.

## Vì sao việc này dính tới Capstone

Demo Chương 07 chạy khi bạn bảo và im khi lệnh dừng. Nó không đáng tin nếu lần cấp nguồn đầu có thể kéo robot khỏi bàn hoặc đưa pack motor vào chân 3,3 V. Timeout chỉ chạy sau khi chip đã sống. Topic ROS 2 sẽ không sửa một pad bạn đã đốt.

## Ba mối nguy, và thứ tự khiến chúng nhàm

**Năng lượng tích trữ** xả dòng mà không hỏi: cổng USB, pin AA, một cặp 18650, tụ trên board lái. Hư hại là nhiệt trên mạch in, trên một chân, hoặc trên cell bị sạc sai cách. **Bánh đang quay** kéo cáp hoặc bước khỏi bàn ngay lần PWM lên sai. **Firmware quên tắt PWM** là chương trình teleop chết sau lệnh "tiến", cửa sổ serial bạn đóng, laptop ngủ. Quy tắc 300 ms biến phần mềm cũ thành một lệnh dừng. Nó không bảo vệ giây trước khi chương trình của bạn bắt đầu, và không bảo vệ GPIO khỏi quá áp.

Nghi thức vừa một trang. Làm mỗi lần, kể cả lần bạn muốn gọi là thử nhanh. Mass chung trước: mass vi điều khiển, mass driver, và cực âm pin là một nút, vì dòng motor trở về đó. Tín hiệu nối trước mass đó có thể trở về qua GPIO và giết chân. Nguồn logic kế tiếp, USB vào vi điều khiển, từ đó có 3,3 V cho các chân. Nguồn logic của driver lấy từ ray yên đó, không lấy từ pin motor. Tín hiệu sau cùng trong nhóm logic: PWM, hướng, và standby, đã mang nghĩa dừng nếu firmware đang chạy. VM motor cuối, qua công tắc nếu có. Bánh đã nhấc sẵn. Nhấc sau khi giật là cách bánh caster rời bàn.

![Nguồn lên theo mass chung, logic, tín hiệu, nguồn motor cuối, bánh khỏi mặt bàn]({{ site.imgurl }}/generated/power_order.png)

Chép các ô theo thứ tự đó. "Cuối" nghĩa là công tắc đóng cuối. Bánh đã ở trên không.

![Logic 3,3 V, USB 5 V, mass, và ray motor riêng]({{ site.imgurl }}/generated/power_rails_3v3.png)

Dùng màu như danh sách cấm. USB 5 V nuôi board, không nuôi hai motor TT đang stall. GPIO là thế giới 3,3 V. Mass là nút bạn cố ý dùng chung. Ray motor là pin riêng và không bao giờ đáp xuống GPIO hoặc chân 3,3 V.

## Lithium, đúng kiểu người ta bị thương

Một cell 18650 lithium-ion khoảng 3,6–3,7 V danh định và **4,2 V khi đầy**. Bạn sạc **từng cell một** tới 4,2 V, trên cục sạc có nhãn Li-ion hoặc Li-ion 18650. Hai cell nối tiếp, tức đế 2S, khoảng 7,4 V danh định và **8,4 V khi đầy**. Cặp nối tiếp đó là pack motor. Nó không phải đầu vào của cục sạc.

TP4056 cố đưa một cell lên 4,2 V. Kẹp nó qua đế 2S là đặt cục sạc đó lên pack 8,4 V. Đừng. Lấy một cell ra, sạc riêng, rồi mới đặt lại.

Cell khoảng 2,1 V nằm rất thấp dưới ngưỡng cắt thường gặp gần 2,5–3,0 V. Sạc nó với dòng bình thường có thể mạ kim loại bên trong và tạo ngắn mạch trong. Đừng "đánh thức" bằng TP4056. Đem đi tái chế. Cell phồng đã hỏng: đừng sạc, đừng chọc, đừng cất "phòng khi". Một viên 18650 trần trong túi cùng chìa khóa có thể hàn thành ngắn mạch. Cell sống trong đế hoặc hộp. Các lần thử motor đầu được phép dùng đế AA để bạn học VM khác logic trước khi sở hữu lithium. Chưa có cell là trạng thái an toàn. Cục sạc không khớp thì không.

## Chân, mỏ hàn, và mắt

Điện áp cực đại tuyệt đối trên GPIO của ESP32 **không** phải 5 V. Pad nằm cao hơn ray 3,3 V vài phần mười vôn, không phải ở 5 V và không phải ở điện áp motor. Chân Pico cùng loại đầu vào 3,3 V. Echo của HC-SR04 khoảng 5 V khi cao. Pack thường 7–8 V. Echo cần mạch dịch mức. Pack chỉ được vào VM.

Đeo kính khi cắt chân linh kiện và khi hàn. Mẩu chì bay. Khói rosin cần không khí chuyển động, không phải phòng kín và mặt cúi trên mối hàn. Mỏ nằm trên giá, không nằm trên dây. Hôm nay bạn không hàn. Bạn viết quy tắc đó ở chỗ tay sẽ thấy.

Nửa phần mềm của nghi thức là timeout bạn đã viết:

$$
t_{\mathrm{silence}} > 300\,\mathrm{ms} \implies \text{duty PWM} = 0.
$$

Hôm nay bạn chưa nạp vòng lặp đó. Đừng gọi một bố trí là sẵn sàng nếu cách dừng duy nhất là rút USB sau khi robot đã rời thảm. Một đường teleop im phải là dừng, không phải giữ tốc độ cuối.

## Lỗi nên nhận ra trước khi gặp

| Bạn thấy hoặc sắp làm | Thường là | Bạn làm |
| --- | --- | --- |
| Cổng serial mất khi motor buộc vào chân 5 V của board | Cổng USB không nuôi nổi hai motor stall; ray 3,3 V sụp | Motor trên VM riêng, mass chung, logic chỉ từ USB |
| GPIO chết sau khi nối echo siêu âm | 5 V vào chân có cực đại tuyệt đối không phải 5 V | Dừng; chân có thể đã hỏng; dịch mức trên echo trước khi thử lại |
| TP4056 kẹp qua đế 2S | Cục sạc 4,2 V trên pack 8,4 V | Tháo ra; sạc từng cell, ngoài robot |
| Cell đo khoảng 2,1 V, hoặc vỏ phồng | Lithium xả quá hoặc đã hỏng | Không sạc; không bỏ túi; tái chế |
| Bánh trên bàn, firmware mới, "thử một tí" | Chuyển động bất ngờ, PWM có thể khác 0 trước vòng lặp | Bánh nhấc trước; VM cuối; timeout vẫn cần khi code chạy |
| Mỏ nằm trên dây, hoặc mắt không có kính khi cắt chân | Bỏng, dây chảy, hoặc mẩu chì vào mắt | Giá, kính, thông gió; rút điện nếu bố trí đã sai |

## Lab: thẻ, rồi bật nguồn chỉ bằng USB

Làm với motor **ở ngoài mạch**. Nếu chưa có board, vẫn viết thẻ và ghi `chưa có board` ở chỗ lẽ ra là tên cổng.

Xé một trang. Đặt tên `LÊN NGUỒN`. Bốn dòng: (1) GND chung, (2) logic từ USB, (3) tín hiệu PWM và hướng, đã mang nghĩa dừng, (4) VM motor cuối. Bên dưới viết `BÁNH NHẤC TRƯỚC VM`, `IM > 300 ms → PWM 0`, `CẤM: pin hoặc echo 5 V trên GPIO 3,3 V`, và `18650: từng cell, 4,2 V, không TP4056 qua đế 2S`. Dán trang ở chỗ tay làm việc. Không có băng dính thì để dưới bàn phím bạn dùng để ghi chú.

Rồi chạy checklist chỉ USB, theo thứ tự này.

Nhìn bàn và xác nhận không có motor, không pin motor, không dây VM. Ngắt pin trước khi cắm USB. Bánh, nếu bạn có, không nằm trên driver đang có điện và không thuộc bài thử này. Chỉ cắm vi điều khiển, bằng cáp bạn tin là truyền được dữ liệu. Tìm cổng serial hoặc, với Pico ở BOOTSEL, một ổ đĩa. Dán tên cổng, hoặc viết `không có — chưa có board` và kế hoạch "khi tới, chỉ USB, không VM, ghi cổng, rồi rút". Rút. Đừng gắn motor để ăn mừng.

Nếu đã có cell lithium, chụp nhãn cục sạc và gõ các chữ hóa học bạn đọc được. Nhãn mất nghĩa là `sẽ không sạc`. Chưa có lithium nghĩa là `chưa mua cell`. Nếu có mỏ hàn, xác nhận giá đỡ trước khi bật, và ghi kính bảo hộ đang ở trên bàn hay còn thiếu.

**Bạn sẽ thấy gì.** Thẻ nhìn thấy mà không cần mở bài. Sổ có ảnh hoặc phác thẻ, trường serial là tên cổng thật hoặc một kế hoạch rõ, và quyết định sạc: "khớp", "sẽ không sạc", hoặc "chưa mua cell". Không có motor trong bước USB.

**Khi lệch.** Nếu VM đứng đầu danh sách, viết lại thẻ. Bánh nhấc cho mọi lần thử firmware mới đầu tiên, kể cả trên bàn. Video nuôi motor từ chân 5 V của DevKit là `cấm`. Cục sạc kẹp vào vì giắc vừa thì tháo ra. Từng cell một.

## Ví dụ làm sẵn

Một bạn muốn bánh hạ xuống "chỉ để xem sketch mới". PWM chưa được chứng minh là bắt đầu ở 0, và timer 300 ms chưa chạy được trước khi setup xong. Giữ bánh nhấc, VM hở, chỉ logic USB, rồi lần chạy đầu trên không. Bánh hạ có thể kéo board khỏi bàn trước khi dòng đó chạy.

Cùng buổi chiều một viên 18650 đo 2,1 V và có người đưa TP4056 "hồi sức". Cell nằm dưới ngưỡng còn lành. Sổ ghi sẽ không sạc, không bỏ túi, không kẹp qua đế 2S. Cell lành, nếu có, được sạc riêng tới 4,2 V rồi mới đặt vào đế.

Sợi echo trong cùng đống sắp đáp vào GPIO ESP32. Cực đại tuyệt đối của pad đó không phải 5 V, nên dây chờ mạch dịch mức. Điện áp motor là lệnh cấm cùng loại, chỉ lớn hơn.

## Bài tập

Đây là tình huống. Viết hành động, không viết định nghĩa.

1. Một bạn để khung xe trên bàn, bánh hạ, và muốn nạp firmware "chỉ một giây". Điều gì phải đúng trước khi VM được đóng, và vì sao quy tắc 300 ms không đủ cho lần nạp đầu?
2. Cell trên bàn đọc 2,1 V. Có người đưa TP4056. Bạn làm gì với cell, và từ chối làm gì với đế 2S?
3. Dây echo HC-SR04 sắp đi thẳng vào GPIO ESP32. Dây đó bao nhiêu vôn khi cảm biến trả lời, và vì sao "ESP32 cứng" không phải là thông số?
4. Bạn thấy TP4056 đã kẹp qua đế chứa hai cell nối tiếp. Đế đó sau này sẽ nuôi VM. Bạn ngắt cái gì, và nếu cell còn lành thì sạc thế nào?
5. Teleop đang chạy thì laptop ngủ. Firmware không có timer im. Bánh làm gì, và phép gán nào phải có trong vòng lặp?

<details>
<summary>Gợi ý đáp án</summary>

1. Bánh nhấc, mass rồi logic rồi tín hiệu đã xong, VM vẫn hở cho tới khi bạn nhìn được bánh trên không. Timeout chỉ chạy khi firmware đang thực thi. Reset có thể kéo chân trước, và bánh trên bàn có thể kéo board xuống sàn.
2. Không sạc cell, không bỏ túi, không kẹp TP4056 vào cell hoặc vào đế 2S. Đem tái chế.
3. Echo khoảng 5 V khi cao. Cực đại tuyệt đối GPIO ESP32 không phải 5 V. Dây cần mạch dịch mức. Chân có thể đã hỏng.
4. Ngắt TP4056 ngay. Sạc mỗi cell lành riêng tới 4,2 V, ngoài robot. Đế chỉ là pack cho VM sau bước đó.
5. Bánh giữ lệnh cuối. Vòng lặp phải đưa duty PWM về 0 khi im quá khoảng 300 ms.

</details>

## Đọc thêm

- [Mức logic, SparkFun](https://learn.sparkfun.com/tutorials/logic-levels) — vì sao 5 V và 3,3 V không thay nhau, tức bài toán chân echo thu nhỏ.
- [Battery University, BU-409, sạc lithium-ion](https://batteryuniversity.com/article/bu-409-charging-lithium-ion) — ý 4,2 V khi đầy, và vì sao lithium-ion không phải "pin sạc" chung chung.

## Mua ở Việt Nam

Giỏ robot là [bài 00-05]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %}). Giá ở đây là snapshot Hshop ngày **23 tháng 9 năm 2026**. Mua một đồng hồ: [UNI-T UT33D+](https://hshop.vn/dong-ho-van-nang-dien-tu-digital-multimeter-uni-t-ut33d-chinh-hang) giá 285000 ₫ hoặc [Wadfow WDM1501](https://hshop.vn/dong-ho-van-nang-ky-thuat-so-vom-wadfow-wdm1501-digital-multimeter-true-rms) giá 185000 ₫. Mỏ và giá là một cặp: [Wadfow 60 W](https://hshop.vn/mo-han-60w-wadfow-wel3616-soldering-iron) giá 75000 ₫ và [giá tròn](https://hshop.vn/de-gac-mo-han-tron-b-2-co-khay-roi) giá 40000 ₫. Mỏ không có giá là thất bại đúng quy tắc bạn vừa viết. Thiếc, kìm cắt và breadboard nằm ở bài 00-04.

Kính và cục sạc một cell là trang tìm kiếm, không phải slug sản phẩm bịa. [Shopee, kính bảo hộ](https://shopee.vn/search?keyword=k%C3%ADnh%20b%E1%BA%A3o%20h%E1%BB%99), [Lazada, kính bảo hộ](https://www.lazada.vn/catalog/?q=k%C3%ADnh%20b%E1%BA%A3o%20h%E1%BB%99), [Shopee, sạc pin 18650](https://shopee.vn/search?keyword=s%E1%BA%A1c%20pin%2018650), [Lazada, sạc pin 18650](https://www.lazada.vn/catalog/?q=s%E1%BA%A1c%20pin%2018650). Các URL đó là trang tìm kiếm. Chỉ mua cục sạc nếu nhãn nói một cell Li-ion tới 4,2 V. [Thế Giới IC](https://www.thegioiic.com/) và [IC Đây Rồi](https://icdayroi.com/) là trang chủ cửa hàng, không phải link sản phẩm. Đừng mua LiDAR từ các lần tìm này.
