---
layout: post
title: "BOM và cách mua bộ kit robot ở Việt Nam"
chapter: "00"
order: 5
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter00
lesson_type: required
draft: false
---

Thời lượng: **90–120 phút**, kể cả bài lab bảng tính. Các mức giá dưới đây lấy từ trang sản phẩm công khai của Hshop ngày **23 tháng 9 năm 2026**. Giá sẽ đổi. Coi mỗi con số là một lần đọc, rồi mở lại listing trước khi chuyển khoản.

## Mục tiêu

Hết bài này bạn lập được bảng vật tư Track A cho robot vi sai của capstone, chọn mạch ESP32 hoặc Pico theo thông số chứ không theo tem giảm giá, giải thích được vì sao không lấy L298N cho động cơ TT 3–6 V, ghép pin lithium với đúng kiểu sạc, và điền file `bom.csv` sao cho mỗi dòng có nơi mua, từ khóa tiếng Việt, linh kiện thay thế, và cột đã nhận hay chưa.

## Cần gì trước khi học

Chỉ cần chịu ghi chép. Bài 00-02 (bạn đi Track A hay Track B) giúp quyết định Wi-Fi có phải nằm trên mạch ngay từ đầu hay không. Chưa cần thuộc định luật Ohm. Phần driver và pin dạy đúng hai con số không được mua sai. Trước khi có đồng hồ vạn năng, điện thoại để chụp kiện hàng cũng là dụng cụ.

## Vì sao bài này quyết định capstone

Teleop ở chương 07 hỏng theo những kiểu rất nhàm: driver nuốt mất khoảng hai vôn, cổng USB bị bắt quay bánh, chân echo 5 V cắm thẳng vào GPIO 3,3 V, hoặc mạch sạc 4,2 V bị kẹp lên bộ pin 8,4 V. ROS 2 không sửa được những lỗi đó. BOM là danh sách để phần cứng khớp với firmware. Mua theo thông số, rồi robot mới chạy.

![Các nhóm đồ trong kit]({{ site.imgurl }}/generated/kit_catalog_overview.png)

![Thứ tự nguồn: mass chung, logic, tín hiệu, nguồn motor bật sau cùng, bánh không chạm bàn]({{ site.imgurl }}/generated/power_order.png)

## Bạn đang mua cái gì

BOM là bảng, mỗi dòng là một thứ phải có thật trên bàn, kể cả tua-vít bạn đã có sẵn. BOM không phải ảnh giỏ hàng. Mỗi dòng phải trả lời được: đó là gì, mua mấy cái, thông số nào thì mới chấp nhận, nó làm gì trên robot này, thay bằng gì được, mua ở đâu. Dòng không có thông số thì bạn không phân biệt được hàng thay đúng và hàng rẻ nhìn giống.

Robot mặc định của khóa học là **xe vi sai**: hai bánh dẫn động, một bánh đa hướng, vi điều khiển logic 3,3 V, driver MOSFET, một cảm biến khoảng cách, và pin motor không bao giờ cấp dòng vào chân 3,3 V. IMU, encoder bánh xe, cảm biến ToF là dòng mua sau, khi xe đã chạy theo lệnh. Track B thêm máy Ubuntu 24.04 cho ROS 2 Jazzy. Đừng mua LiDAR cho có cảm giác sẵn sàng.

```
USB 5 V ---- logic ESP32 / Pico (GPIO 3,3 V)
                 |
                GND -------- mass chung với driver
                 |
2S 18650 ~7,4 V ---- VM của TB6612 ---- hai động cơ TT
                 |
                 +-- không nối vào chân 3,3 V
```

![Đường 3,3 V, USB 5 V, và đường nguồn motor riêng]({{ site.imgurl }}/generated/power_rails_3v3.png)

## Danh sách Track A mặc định

Chia ba đợt để khung xe đến muộn vẫn không chặn chương 01.

**Đợt 1 — bàn lab (học chương 01 ngay tuần này).** Đồng hồ vạn năng, mỏ hàn khoảng 60 W có đế, thiếc, kìm cắt, breadboard cắm, dây jumper, cáp USB có data, mạch vi điều khiển, vài LED, một nút nhấn.

**Đợt 2 — chuyển động (trước chương 05).** Khung xe, hoặc động cơ TT rời kèm gá và bánh đa hướng, driver TB6612FNG (DRV8833 chỉ là phương án nhỏ hơn), HC-SR04, và mạch chuyển mức 3,3 V / 5 V cho chân echo.

**Đợt 3 — năng lượng (sau khi bạn đo được điện áp).** Hai cell 18650 có mức dung lượng hợp lý, đế pin, và sạc nạp **từng cell** lên 4,2 V. Đế nối tiếp trên xe không phải là sạc.

Chưa đưa vào hóa đơn đầu: RPLiDAR, Raspberry Pi 5, máy hiện sóng, nguồn 12 V 10 A, và mọi "combo robot" mà driver là L298N dán sẵn hộp 4 pin AA không có tài liệu.

### Bảng kit gộp

Thông số lấy từ datasheet thường gặp hoặc từ listing Hshop được dẫn ở phần mua hàng. Khi hàng tới, đọc chữ in trên IC.

| Dòng | SL | Thông số chấp nhận | Vai trò trên capstone | Món nên mua | Thay được bằng |
|------|---:|--------------------|------------------------|-------------|----------------|
| Vi điều khiển | 1 | GPIO 3,3 V, USB-UART, từ 20 chân dùng được | Firmware, sau này teleop Wi-Fi | Mạch ESP32 dạng dev board, khoảng 30 chân, CH340 hoặc CP2102 | Pico 2 nếu chấp nhận teleop qua USB trước, Wi-Fi để sau |
| Khung | 1 | Hai bánh dẫn, sàn bắt mạch | Thân xe vi sai | Kit 2WD mica TT, hoặc kit 4WD của Hshop dùng hai bánh dẫn cộng bánh đa hướng | Động cơ TT rời, hai bánh, hai gá, một bánh đa hướng, một tấm cứng |
| Động cơ TT | 2 bánh dẫn | 3–9 V, hộp số khoảng 1:48 | Bánh trái và phải | Motor đi kèm khung | TT 1:48 của Hshop, listing 20 000 ₫/cái |
| Driver | 1 | Cầu H MOSFET, VM khoảng 5–10 V, mỗi kênh ≥ 1 A liên tục | Chiều quay và PWM | Module TB6612FNG, VM 4,5–10 V, 1,2 A liên tục / 3,2 A đỉnh | DRV8833, VM 2,7–10,8 V, listing Hshop ghi tối đa 1,5 A/kênh; kẹt bánh thì nóng |
| Khoảng cách | 1 | HC-SR04 hoặc ToF nhỏ | Khoảng cách vật cản | HC-SR04 | Module VL53L0X nếu muốn I²C và 3,3 V ngay từ đầu |
| Chuyển mức | 1 | 4 kênh 3,3 V ↔ 5 V | Echo HC-SR04 vào ESP32 | Module MOSFET | Cầu chia áp chỉ trên echo (trig 3,3 V đôi khi không đủ với module kém) |
| Pin motor | 2 cell | Li-ion 18650, mức công bố ≤ 3500 mAh | VM qua driver | Cell nạp **bên ngoài** xe | 6 pin AA (~9 V) nếu bạn chưa muốn lithium; không dùng pin vuông 9 V |
| Sạc | 1 | 4,2 V mỗi cell, tự ngắt khi đầy | Nạp từng cell | Sạc khay 4 ngăn 18650 | TP4056 **chỉ** cho một cell, không kẹp lên đế 2S |
| Đồng hồ | 1 | V DC, Ω, chuông thông mạch | Kiểm tra dây | UNI-T UT33D+ hoặc đồng hồ hobby rẻ hơn | Đồng hồ nào có chuông; nếu đo dòng thì phải có cầu chì |
| Mỏ hàn | 1 | ~60 W, đế, thiếc 0,8 mm | Dây và header | Mỏ 60 W cố định là đủ cho Dupont và hàng chân | Trạm hàn để sau, chưa cần để bắt đầu |
| Mạch thử | 1 | Breadboard 830 lỗ, dây đực-đực và đực-cái | Chương 01–03 | — | Breadboard 400 lỗ nếu dây ngắn |
| Ốc | 1 bộ | Vít M3, trụ nhựa | Kê mạch khỏi mặt kim loại | Thường có trong khung | Bộ M3 ở cửa hàng cơ khí |

## Vì sao dòng driver không phải "cầu H nào cũng được"

Trên Hshop, module L298N và module TB6612FNG cùng giá **45 000 ₫** (SKU HS0695V và HS2458V vào ngày viết bài). Giá không phải chỗ khác nhau. L298N là cầu Darlington. Khi có dòng motor, nó rơi khoảng 1,8 V đến 2,5 V giữa pin và động cơ. TB6612FNG là cầu MOSFET; động cơ gần như nhận đủ điện áp nguồn motor.

$$
V_{motor} \approx V_{pin} - V_{roi}
$$

Lấy bộ hai cell ở 7,4 V danh định. Rơi 2,0 V với Darlington, rơi 0,3 V với MOSFET:

$$
V_{L298} \approx 7{,}4 - 2{,}0 = 5{,}4\,\text{V}
$$

$$
V_{TB6612} \approx 7{,}4 - 0{,}3 = 7{,}1\,\text{V}
$$

Listing động cơ TT tỉ số 1:48 của Hshop ghi điện áp khuyến nghị **3–9 V**, dòng không tải **110–150 mA**, khoảng **200–208 vòng/phút ở 5–6 V**, mô-men **0,8 kg·cm ở 6 V**. Năm vôn đã là vùng chậm và yếu của chính listing đó. Bốn pin AA mới chỉ khoảng 6 V trước khi trừ sụt trên L298N, nên motor có thể còn gần 4 V và xe bò. Module L298N còn có IC 7805. Đừng lấy 5 V từ con 7805 đó để nuôi ESP32 khi nguồn motor trên 12 V. Bộ pin của ta dưới 10 V, và dù vậy vẫn không nuôi vi điều khiển từ chân 5 V của module driver. Logic của TB6612FNG là **2,7–5,5 V**, nên mức cao 3,3 V từ GPIO là hợp lệ. Chân STBY phải được kéo lên, nếu không cầu H ngủ.

Module DRV8833 giá **25 000 ₫**. Listing Hshop cho VM **2,7–10,8 V** và **tối đa 1,5 A mỗi kênh**. Đủ làm phương án thay khi mỗi kênh một động cơ TT. Ít đồng và vỏ nhỏ hơn TB6612, nên kẹt bánh lâu sẽ nóng sớm. Đừng mắc song song hai motor trên một kênh DRV8833.

Dòng kẹt trục không phải dòng không tải. Listing không ghi dòng kẹt. Hãy dự phòng vài lần 150 mA, rồi **đo** sau: bánh nhấc khỏi mặt bàn, đồng hồ mắc nối tiếp, chỉ bấm một xung ngắn. Mua driver chỉ vì tem ghi 2 A là dòng đó chưa xong.

![Ý tưởng cầu H: vi điều khiển chỉ chọn chiều dòng, không phải nguồn cấp dòng cho motor]({{ site.imgurl }}/generated/hbridge_concept.png)

## Pin, đế và sạc là một quyết định

Một cell 18650 khoảng 3,6–3,7 V danh định và **đầy ở 4,2 V**. Hai cell nối tiếp, đúng kiểu đế "2×18650 nối tiếp", khoảng **7,4 V danh định và 8,4 V khi đầy**. Điện áp đó đi vào chân VM của driver. Không đi vào GPIO, và không đi vào TP4056.

Các mạch TP4056 trên Hshop (bản USB-C 10 000 ₫ và bản mini-USB 2 000 ₫) là sạc **một cell**. Chúng cố đưa một cell lên 4,2 V ở khoảng 1 A. Kẹp một mạch như vậy lên cặp nối tiếp là bắt sạc 4,2 V làm việc với cụm 8,4 V, hoặc chỉ nạp một phần cụm trong khi hai cell lệch nhau. Cả hai cách đều sai dòng BOM. Hãy nạp từng cell trong sạc có khay, đo điện áp hở mạch nằm khoảng 3,6 V đến 4,20 V, rồi mới lắp vào đế. Sạc 4 khay cổng USB trên Hshop giá **68 000 ₫** (listing ghi 14500 / 18650 / 21700). Dùng một khay cho đến khi bạn tin mạch đó.

Dung lượng có trần vật lý. Cell 18650 thật hiếm khi quá khoảng 3500 mAh. Cell trung thực thường 2000–3000 mAh. Hshop niêm yết Sunpower **2000 mAh giá 35 000 ₫** và **2500 mAh giá 45 000 ₫**. Listing chợ viết 9900 mAh hoặc 12000 mAh với giá tương tự là bịa. Chữ "10C" trên tên Sunpower là tuyên bố dòng xả, không phải dung lượng. Đừng tin hệ số C nếu không có datasheet. Hai động cơ TT cũng không cần hệ số C tưởng tượng.

Cell hobby thường **không** có mạch bảo vệ. Tua-vít chạm hai cực có thể xả hàng chục ampe. Đừng để cell trong túi cùng chìa khóa. Đừng sạc trên giường. Dừng nếu cell phồng, dưới khoảng 2,5 V, hoặc nóng. Pin vuông 9 V là lỗi kinh điển còn lại: nội trở sụp ngay khi motor kẹt, vi điều khiển reset trong khi driver vẫn đang được lệnh chạy.

Khi học trên bàn, nuôi vi điều khiển bằng USB. Nối mass USB với mass driver. Bật pin motor sau cùng, và chỉ khi bánh đã được nhấc.

## Cách mua

Mua thông số, không mua ảnh thumbnail. Tem giảm 30 % trên combo L298N vẫn là cầu H sai. Đọc điện áp, dòng liên tục, mức logic và loại giắc trước khi đọc phần giảm giá.

Đợt 1 nên gom một shop để thiếu cáp USB không phải chờ kiện thứ hai. Ở Việt Nam, Hshop (hshop.vn, cửa hàng 269/20 Lý Thường Kiệt, Phường Phú Thọ, TP.HCM) có listing kỹ thuật và SKU. Chính họ ghi SKU kết thúc bằng **V** là giá công ty đã gồm VAT. Họ cũng yêu cầu quay video mở hộp trong bảy ngày nếu bạn muốn bảo hành cơ bản. Shopee và Lazada là chợ tìm kiếm: lọc shop có đánh giá, đọc kỹ đó là module hay dev board, ưu tiên shop chụp rõ chữ trên IC. Thế Giới IC (thegioiic.com) và IC Đây Rồi (icdayroi.com, Thủ Đức) là quầy linh kiện. Họ rất hợp để mua **module** ESP32 hoặc IC ổn áp, và rất dễ bị nhìn nhầm thành mạch cắm USB.

Chuyển khoản cho cửa hàng điện tử sau khi họ xác nhận còn hàng. Ví sàn thì ổn cho dây jumper và khung xe. Đừng chuyển cho người lạ trên mạng xã hội để mua "pin 18650 đã test" mà không có đường trả.

Khi kiện tới, làm các việc sau trước khi mừng:

1. Quay video mở hộp. Đếm túi theo `bom.csv`.
2. Đồng hồ: chuông khi chập hai que đo, rồi khoảng 5 V trên củ sạc USB bạn đã tin.
3. Vi điều khiển: cắm cáp **có data** vào máy tính. Phải xuất hiện cổng serial mới. Cáp chỉ sạc thì im lặng, trông như mạch chết.
4. Chỉ cắm USB, chân 3,3 V đọc khoảng 3,3 V. Nếu ra 5 V thì dừng.
5. Driver: chữ trên IC đúng TB6612FNG hoặc DRV8833, không phải L298N.
6. Motor: trục quay tay không có tiếng sạn. Tỉ số trên túi khớp dòng đã trả tiền.
7. Cell: không phồng, mỗi cell khoảng 3,4 V đến 4,2 V. Chưa nối tiếp khi chưa có cả hai số đo.

## Mua ở Việt Nam

Link dưới đây hoặc là **trang sản phẩm đã trả về giá ngày 23 tháng 9 năm 2026**, hoặc là **trang tìm kiếm**. Trang tìm kiếm được ghi rõ. Đừng coi URL tìm kiếm là lời hứa rằng kết quả đầu tiên đúng món. Link Shopee là trang tìm theo từ khóa. Tìm trên Lazada bằng `https://www.lazada.vn/catalog/?q=` cộng từ khóa; trình duyệt tự động đôi khi gặp captcha, trình duyệt thường vẫn ra danh sách.

### Vi điều khiển

Từ khóa: `ESP32 NodeMCU 38 chân CH340`, `ESP32 DevKit V1`, `Raspberry Pi Pico 2`.

- Trang Hshop đã kiểm: [ESP32 NodeMCU-32S CH340 Ai-Thinker, 190 000 ₫](https://hshop.vn/kit-rf-thu-phat-wifi-ble-esp32-nodemcu-32s-ch340-ai-thinker). Đây là dev board có USB. Mua loại này.
- Trang Hshop đã kiểm, đắt hơn: [Vietduino ESP32, 265 000 ₫](https://hshop.vn/mach-phat-trien-vietduino-esp32).
- Trang Hshop đã kiểm, **không** phải máy tính duy nhất bạn cần: [module ESP32-S3-WROOM-1, 135 000 ₫](https://hshop.vn/mach-thu-phat-wifi-ble-soc-esp32-s3-esp32-s3-wroom-1-chinh-hang-espressif). Module chưa có USB-UART cho đến khi bạn gắn thêm.
- Trang tìm Hshop đã kiểm: [raspberry pi pico](https://hshop.vn/search?q=raspberry+pi+pico) lúc đó có Pico 2 giá 195 000 ₫ và Pico 2 W giá 275 000 ₫.
- Trang Thế Giới IC đã thấy: [ESP32-DevKitC-32U](https://www.thegioiic.com/esp32-devkitc-32u-module-wifi-bluetooth-2-4ghz). Đọc xem anten có phải bản U.FL (DevKitC-32U) và cáp anten có đi kèm không.
- Tìm Shopee: [ESP32 DevKit](https://shopee.vn/search?keyword=esp32%20devkit%20ch340).
- Tránh ảnh vỏ kim loại không có ổ USB nếu tiêu đề vẫn ghi "kit phát triển".

### Khung xe, động cơ, bánh đa hướng

Từ khóa: `khung xe robot 2 bánh TT`, `động cơ giảm tốc TT 1:48`, `bánh đa hướng`.

- Các lần tìm cho bài này **không** thấy kit 2WD mica rẻ trên Hshop. Có thấy [khung MKE-R01 4WD động cơ TT, 245 000 ₫](https://hshop.vn/khung-xe-mke-r01-4wd-robot-car-chassis-tt-motor). Dùng hai motor cho capstone, để hai cái làm dự phòng, thêm bánh đa hướng, **hoặc** gom bánh trái một tốc độ và bánh phải một tốc độ chỉ sau khi đã đo dòng.
- Linh kiện rời, đã kiểm: [động cơ TT 1:48, 20 000 ₫](https://hshop.vn/dong-co-dc-giam-toc-tt-motor-ti-so-1-48), [bánh 65 mm, 8 000 ₫](https://hshop.vn/banh-xe-dong-co-dc-giam-toc-v1-plastic-geared-tt-motor-65mm), [gá, 10 000 ₫](https://hshop.vn/ga-bat-dong-co-dc-giam-toc-tt-motor-mounting-bracket), [bánh đa hướng, 15 000 ₫](https://hshop.vn/banh-xe-nhua-da-huong-3pi-ball-caster-wheel).
- Tìm Shopee (trang tìm, chưa lấy giá từng tin): [khung xe 2 bánh TT](https://shopee.vn/search?keyword=khung%20xe%20robot%202%20b%C3%A1nh%20TT). Tin rao thường nằm khoảng **90 000–180 000 ₫**; ảnh phải có hai motor, bánh đa hướng và hộp pin.
- Tìm Lazada: [khung xe robot](https://www.lazada.vn/catalog/?q=khung%20xe%20robot%202%20banh).
- Tránh "kit robot" chỉ có L298N và hộp 4 pin AA rồi gọi là đủ.

### Driver động cơ

Từ khóa: `TB6612FNG`, `DRV8833`. Đừng lấy `module L298 giá rẻ` làm mặc định.

- Đã kiểm: [TB6612FNG, 45 000 ₫, SKU HS2458V](https://hshop.vn/mach-dieu-khien-dong-co-dc-tb6612fng-dc-motor-driver). VM 4,5–10 V, logic 2,7–5,5 V, 1,2 A liên tục, 3,2 A đỉnh, 20×20 mm.
- Thay thế đã kiểm: [DRV8833, 25 000 ₫](https://hshop.vn/mach-dieu-khien-dong-co-drv8833-dc-motor-driver). VM 2,7–10,8 V, listing ghi tối đa 1,5 A/kênh.
- Món đã kiểm nhưng **không** để làm mặc định: [module L298N, cũng 45 000 ₫](https://hshop.vn/mach-dieu-khien-dong-co-dc-l298). Chỉ mua khi bạn hiểu điện áp rơi và motor thuộc loại 12 V.
- Tìm Shopee: [TB6612FNG](https://shopee.vn/search?keyword=tb6612fng).
- Mạch Pololu là bản tham chiếu đáng tin nếu sau này nhập: [Pololu 713](https://www.pololu.com/product/713).

### Cảm biến

Từ khóa: `HC-SR04`, `VL53L0X`, `MPU6050 GY-521`, `đĩa encoder TT 20 xung`.

- Đã kiểm: [HC-SR04, 27 000 ₫](https://hshop.vn/cam-bien-sieu-am-srf04). Echo ra 5 V. Mua mạch chuyển mức cùng lúc.
- Mạch chuyển mức đã kiểm: [4 kênh, 10 000 ₫](https://hshop.vn/mach-chuyen-muc-tin-hieu-logic-4-kenh).
- Dòng mua sau, đã kiểm: [GY-521 MPU6050, 85 000 ₫](https://hshop.vn/cam-bien-6-dof-bac-tu-do-gy-521-mpu6050). I²C, listing ghi nuôi 3,3–5 V, logic 3,3 V. Chưa cần để nhấp LED.
- ToF thay HC-SR04, đã kiểm: [module VL53L0X, 115 000 ₫](https://hshop.vn/cam-bien-khoang-cach-tof-laser-radar-vl53l0x).
- Đĩa encoder, đã kiểm nhưng rất dễ mất: [đĩa 20 xung, 1 000 ₫](https://hshop.vn/dia-encoder-20-xung-dong-co-dc-giam-toc-v1). Mạch cảm biến là dòng khác; tìm `cảm biến tốc độ encoder hồng ngoại`.
- Shopee: [HC-SR04](https://shopee.vn/search?keyword=hc-sr04).

### Nguồn

Từ khóa: `pin 18650 2500mAh`, `sạc 18650 4 ngăn`. Chỉ tìm `TP4056` khi bạn biết nó là một cell.

- Cell đã kiểm: [Sunpower 2500 mAh, 45 000 ₫](https://hshop.vn/pin-sac-18650-li-ion-rechargeable-battery-3-7v-2500mah-10c-sunpower), [2000 mAh, 35 000 ₫](https://hshop.vn/pin-sac-18650-li-ion-rechargeable-battery-3-7v-2000mah-10c-sunpower).
- Đế hàn chân, đã kiểm: [đế 2×18650, 4 000 ₫](https://hshop.vn/hop-pin-2-co-18650). Khung xe có thể đã kèm đế lò xo. Đừng mua cả hai rồi nối tiếp bốn cell.
- Đế không hàn, đã kiểm: [đế DIY, 10 000 ₫](https://hshop.vn/hop-pin-ghep-noi-diy-solderless-18650-battery-holder).
- Sạc khay đã kiểm: [sạc 4 ngăn USB, 68 000 ₫](https://hshop.vn/bo-sac-pin-18650-li-ion-usb-battery-charger-yh-18650-4).
- Mạch một cell đã kiểm, **không** dùng cho cụm 2S: [TP4056 USB-C, 10 000 ₫](https://hshop.vn/mach-sac-pin-tp4056-lithium-battery-charge-controller-usb-c).
- Tìm Shopee: [sạc pin 18650](https://shopee.vn/search?keyword=s%E1%BA%A1c%20pin%2018650%204%20ng%C4%83n).
- Tránh mạch "sạc nhanh 2A" không thấy điện trở chỉnh dòng, và mọi cell đề trên 3500 mAh.

### Dụng cụ và mạch thử

Từ khóa: `đồng hồ vạn năng`, `mỏ hàn 60W`, `breadboard 830`, `dây breadboard đực cái`.

- Đồng hồ đã kiểm: [UNI-T UT33D+, 285 000 ₫](https://hshop.vn/dong-ho-van-nang-dien-tu-digital-multimeter-uni-t-ut33d-chinh-hang), [Wadfow WDM1501, 185 000 ₫](https://hshop.vn/dong-ho-van-nang-ky-thuat-so-vom-wadfow-wdm1501-digital-multimeter-true-rms). UT136C+ giá 560 000 ₫ là nâng cấp sau, không phải mặc định cho sinh viên.
- Mỏ hàn đã kiểm: [Wadfow WEL3616 60 W, 75 000 ₫](https://hshop.vn/mo-han-60w-wadfow-wel3616-soldering-iron), [đế, 40 000 ₫](https://hshop.vn/de-gac-mo-han-tron-b-2-co-khay-roi), [thiếc Sn63 0,8 mm, 24 000 ₫](https://hshop.vn/thiec-han-sunchi-kp26-0-8mm-sn63-pb37-solder-wire).
- Kìm đã kiểm: [kìm cắt chân 170, 35 000 ₫](https://hshop.vn/kim-cat-day-dien-nho-170-cat-chan-linh-kien-dien-tu). Kìm tuốt nếu muốn một dụng cụ ít cứa đứt lõi đồng: [Wadfow WBQ8401, 130 000 ₫](https://hshop.vn/kim-tuot-day-dien-da-nang-wadfow-wbq8401-wire-stripper).
- Mạch thử đã kiểm: [breadboard 830 lỗ, 35 000 ₫](https://hshop.vn/test-board-cammb-102), [dây đực-đực, 30 000 ₫](https://hshop.vn/day-cam-breadboard-duc-duc-20cm-cap-det-40-soi-m-m-jumper-wire), [dây đực-cái, 30 000 ₫](https://hshop.vn/day-cam-breadboard-duc-cai-20cm-cap-det-40-soi-m-f-jumper-wire), [mạch cấp nguồn breadboard, 25 000 ₫](https://hshop.vn/mach-cap-nguon-cho-breadboard-400-830-lo-mb-102). Hoãn mạch cấp nguồn đến khi bạn phân biệt được ray 3,3 V và ray 5 V.
- Cáp đã kiểm: [Ugreen Micro-USB 1 m, 54 000 ₫](https://hshop.vn/cap-micro-usb-to-usb-2-0-dai-1m-cao-cap-60136-chinh-hang-ugreen). Cáp 30 cm giá 27 000 ₫ có bán và rất ngắn khi xe ở trên sàn. Mạch cổng USB-C thì mua cáp USB-C.
- Phụ kiện nhỏ đã kiểm: [bộ LED 3 mm, 20 000 ₫](https://hshop.vn/bo-5-loai-led-sieu-sang-3mm-thong-dung-5-kind-3mm-transparent-color-led), [nút nhấn tròn, 10 000 ₫](https://hshop.vn/nut-nhan-nha-tron-pbs-11b-12mm-kem-cap), [dây đỏ đen 1 m, 8 000 ₫](https://hshop.vn/day-dien-do-den).
- Trang đầu khi tìm `điện trở` trên Hshop **không** ra bộ điện trở 1/4 W (ra shunt và LCD). Tìm Shopee [bộ điện trở 1/4W](https://shopee.vn/search?keyword=b%E1%BB%99%20%C4%91i%E1%BB%87n%20tr%E1%BB%9F%201%2F4W), khoảng **30 000–80 000 ₫**. Trong bộ cần có 220 Ω, 330 Ω, 1 kΩ và 10 kΩ.
- Tìm dụng cụ trên Shopee: [mỏ hàn 60W](https://shopee.vn/search?keyword=m%E1%BB%8F%20h%C3%A0n%2060W), [đồng hồ vạn năng](https://shopee.vn/search?keyword=%C4%91%E1%BB%93ng%20h%E1%BB%93%20v%E1%BA%A1n%20n%C4%83ng).
- IC Đây Rồi nếu bạn ở Thủ Đức, hợp linh kiện rời: [icdayroi.com](https://icdayroi.com/). Thế Giới IC: [thegioiic.com](https://www.thegioiic.com/).

Dây Dupont là dây tín hiệu. Dòng motor đi trên dây đỏ đen to hơn, vặn vít hoặc hàn vào cực driver, không đi qua một hàng lỗ breadboard.

## Giỏ hàng mẫu: bạn Lan, Track A, trần 2 000 000 ₫

Lan học Track A. Cô muốn teleop Wi-Fi ở chương 08, nên vi điều khiển là ESP32 NodeMCU-32S, không phải Pico. Cô chưa chơi pin lithium, nên giỏ có sạc khay và cấm TP4056 kẹp lên đế nối tiếp. Cô rút hai motor khỏi kit 4WD, gắn bánh đa hướng, hai motor còn lại để dành. Giá là snapshot Hshop ở trên.

| Dòng | SL | Đơn giá (₫) | Thành tiền (₫) |
|------|---:|------------:|---------------:|
| ESP32 NodeMCU-32S CH340 | 1 | 190 000 | 190 000 |
| Khung MKE-R01 4WD (dùng 2 motor) | 1 | 245 000 | 245 000 |
| Bánh đa hướng | 1 | 15 000 | 15 000 |
| TB6612FNG | 1 | 45 000 | 45 000 |
| HC-SR04 | 1 | 27 000 | 27 000 |
| Chuyển mức 4 kênh | 1 | 10 000 | 10 000 |
| Breadboard 830 lỗ | 1 | 35 000 | 35 000 |
| Dây đực-đực và đực-cái | 2 | 30 000 | 60 000 |
| Cáp Ugreen Micro-USB 1 m | 1 | 54 000 | 54 000 |
| UNI-T UT33D+ | 1 | 285 000 | 285 000 |
| Mỏ 60 W + đế | 1+1 | 75 000 + 40 000 | 115 000 |
| Thiếc 0,8 mm | 1 | 24 000 | 24 000 |
| Kìm cắt | 1 | 35 000 | 35 000 |
| 18650 2500 mAh | 2 | 45 000 | 90 000 |
| Sạc 4 khay | 1 | 68 000 | 68 000 |
| MPU6050 (cô giữ, dù là tùy chọn) | 1 | 85 000 | 85 000 |
| Bộ LED + nút + dây 1 m | 1 | 20 000 + 10 000 + 8 000 | 38 000 |
| **Tổng linh kiện** | | | **1 421 000** |

Cộng bộ điện trở theo khoảng Shopee 50 000 ₫ và ship nội thành khoảng 30 000 ₫ thì gần **1 500 000 ₫**. Vẫn trong trần 1 500 000–2 500 000 ₫, còn chỗ cho trụ đồng M3 và một cáp USB dự phòng. Đổi đồng hồ sang Wadfow 185 000 ₫ thì tiết kiệm 100 000 ₫. Đổi ESP32 sang Pico 2 giá 195 000 ₫ gần như không rẻ hơn, và Wi-Fi bị hoãn. Thêm một TB6612 thứ hai thay cho bánh đa hướng, rồi dẫn cả bốn bánh thành hai cặp, là một robot khác. Lan ghi đó là phương án bị loại, không sửa giỏ trong im lặng.

Cô không thêm L298N "vì cũng 45 000". Ở 7,4 V với sụt 2,0 V, motor chỉ còn 5,4 V. Listing motor của Hshop: 5–6 V là khoảng 200 vòng/phút và 0,8 kg·cm ở 6 V. Cô muốn phía 7 V của đường đó, nên driver MOSFET ở lại.

## Lab: lập `bom.csv` và kiểm từng dòng

Tạo `bom.csv` trong thư mục ghi chú, dòng đầu:

```text
part_id,name,qty,role,rating,vendor,url_or_search,unit_vnd,line_vnd,substitute,wave,received,photo,notes
```

**Các bước**

1. Chép bảng của Lan, rồi xóa hoặc hoãn MPU6050 nếu vượt ngân sách của bạn. Thêm một dòng bộ điện trở, giá ghi "khoảng Shopee, chốt khi mở tin" cho đến khi có số thật.
2. Giữ ba cột bạn sẽ dùng: `received` (yes/no), `photo` (tên file ảnh), `notes` (chữ đọc được trên IC).
3. Dòng driver: ghi dải VM và câu "không lấy L298N" vào `notes`.
4. Dòng sạc: ghi "mỗi khay một cell, không kẹp lên đế 2S".
5. Hàng chưa về thì `received` để no, bảng vẫn phải xong. Hôm mạch và đồng hồ tới thì chụp ảnh.
6. Cộng cột thành tiền. Nếu quá 2 500 000 ₫, cắt theo thứ tự: IMU, kìm tuốt, mạch nguồn breadboard. Không cắt đồng hồ hoặc driver.

**Bạn phải thấy**

Một tổng giải thích được trong một phút, dòng driver có phương án thay là DRV8833 và món bị loại là L298N, dòng sạc không thể được thỏa bằng TP4056 trên đế nối tiếp.

**Lỗi hay gặp**

| Bạn thấy | Thường là | Cách sửa |
|----------|-----------|----------|
| Giỏ rẻ nhưng driver là L298N | Bỏ qua điện áp rơi | Đổi dòng; phần mềm không cứu được |
| Dòng ESP32 trỏ tới module WROOM | Không có USB | Đổi sang dev board có ổ cắm USB |
| Hai cell cộng một TP4056 | Sạc 4,2 V, cụm 8,4 V | Sạc khay, nạp từng cell |
| Cột dung lượng ghi 9900 mAh | Công bố giả | Bỏ tin đó |
| Tổng đang tính cáp 30 cm | Dây USB không tới xe | Mua cáp data 1 m |
| Ghi chú motor đi dây Dupont | Breadboard sẽ sụt áp hoặc nóng | Vít terminal và dây đỏ đen |

**An toàn.** Mối nguy của bài này là cell lithium, không phải file bảng tính. Sạc ở chỗ bạn nhìn thấy cell. Đừng chập đế pin. Đừng nối VM vào chân 5 V hoặc 3,3 V của ESP32 để "thử pin".

## Bài tập

1. Cụm 2S đang ở 8,0 V. L298N rơi 2,2 V, đường TB6612 rơi 0,4 V. Động cơ TT nhận bao nhiêu vôn trong mỗi trường hợp? Mức nào nằm giữa vùng dễ chịu của listing 3–9 V?
2. Đế của bạn ghi nối tiếp. Bạn chỉ có một mạch TP4056. Viết đúng trình tự nạp cả hai cell mà không kẹp sạc lên cặp nối tiếp.
3. Tiêu đề Shopee ghi "ESP32 WiFi Bluetooth", ảnh là module bọc kim loại, mép chân hàn, không có cổng USB. Đó là dòng nào trên BOM, và còn thiếu món gì?
4. Echo của HC-SR04 là 5 V. GPIO của bạn là 3,3 V. Bạn thêm món nào, và đo gì để chắc echo chưa cắm thẳng vào chân?
5. Tổng linh kiện 1 420 000 ₫ trước ship. Ship 35 000 ₫, bộ điện trở 55 000 ₫. Nếu Lan thêm một TB6612 nữa giá 45 000 ₫ thì còn dưới trần 2 000 000 ₫ không? Viết phép cộng.

<details>
<summary>Gợi ý đáp án</summary>

1. Đường L298: $$8{,}0 - 2{,}2 = 5{,}8\,\text{V}$$. Đường TB6612: $$8{,}0 - 0{,}4 = 7{,}6\,\text{V}$$. Cả hai đều trong 3–9 V. 7,6 V là điểm khỏe hơn so với mốc mô-men ở 6 V trên listing; 5,8 V là phía yếu.
2. Rút cell ra. Nạp cell A trong một khay đến khi sạc ngắt gần 4,2 V. Lặp lại với cell B. Đo cả hai. Sau đó mới lắp vào đế nối tiếp. TP4056 có thể nạp một cell rời; không được kẹp vào hai cực của đế.
3. Đó là module trần, không phải dòng dev board. Vẫn cần dev board, hoặc mạch nạp USB-UART kèm ổn áp 3,3 V. Đừng bắt đầu khóa học bằng module trần.
4. Thêm mạch chuyển mức 4 kênh (hoặc cầu chia trên echo). Khi cảm biến đã có nguồn mà echo chưa tới GPIO, net echo và net GPIO chưa được nối thẳng. Kiểm thông mạch: hai net đó không thông nhau cho đến khi phía hạ áp của mạch chuyển mức nằm ở giữa.
5. $$1\,420\,000 + 35\,000 + 55\,000 + 45\,000 = 1\,555\,000$$. Vẫn dưới 2 000 000 ₫. Driver thứ hai là đổi thiết kế (bốn motor), không phải đồ dự phòng miễn phí, nên cột ghi chú phải nói rõ.

</details>

## Đọc thêm

- [Trang TB6612FNG của Pololu, mã 713](https://www.pololu.com/product/713) — mạch MOSFET mà module Hshop đang làm theo.
- [Thư mục DRV8833 của TI](https://www.ti.com/product/DRV8833) — giới hạn dòng và dải VM của món thay rẻ.
- [Nhóm driver DC chổi than của Pololu](https://www.pololu.com/category/11/brushed-dc-motor-drivers) — vì sao tem "2 A" trên mạch Darlington chưa nói hết.
- [SparkFun: logic levels](https://learn.sparkfun.com/tutorials/logic-levels) — echo 5 V và GPIO 3,3 V.
- [Battery University, BU-409, nạp lithium-ion](https://batteryuniversity.com/article/bu-409-charging-lithium-ion) — 4,20 V mỗi cell, vì sao cụm nối tiếp cần sạc hiểu nối tiếp.
- [Datasheet ESP32 của Espressif](https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf) — điện áp tối đa trên GPIO không phải 5 V.
- [Tài liệu module HC-SR04, SparkFun](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf) — thời gian trig/echo; coi echo là 5 V.
