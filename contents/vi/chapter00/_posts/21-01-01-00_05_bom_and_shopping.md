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

Thời lượng dự kiến là **90–120 phút**, bao gồm cả phần thực hành lập bảng tính. Các mức giá trong bài được ghi nhận từ trang sản phẩm công khai của Hshop vào ngày **23 tháng 9 năm 2026**. Do giá linh kiện thay đổi theo thời điểm, hãy xem các con số này là mốc tham khảo và kiểm tra lại trang bán hàng trước khi thanh toán.

## Mục tiêu

Sau bài học này, bạn sẽ lập được bảng vật tư (BOM) cho xe vi sai theo Lộ trình A (Track A) phục vụ Capstone, biết chọn mạch ESP32 hoặc Pico theo thông số kỹ thuật thay vì theo chương trình giảm giá, giải thích được lý do không dùng L298N cho động cơ TT 3–6 V, ghép đúng bộ sạc cho pin lithium, và hoàn thiện tệp `bom.csv` với đầy đủ nơi mua, từ khóa tìm kiếm tiếng Việt, phương án thay thế và cột theo dõi tình trạng nhận hàng.

## Cần gì trước khi học

Bạn chỉ cần chuẩn bị sẵn công cụ ghi chép và quyết định chọn Lộ trình A hay Lộ trình B từ bài 00-02 để biết có cần Wi-Fi trên vi điều khiển ngay từ đầu hay không. Hiện tại chưa cần thuộc định luật Ohm; phần mạch lái và pin trong bài cung cấp đúng hai thông số quan trọng nhất để bạn không mua nhầm. Khi chưa có đồng hồ vạn năng, điện thoại để quay chụp kiện hàng cũng là một công cụ kiểm tra hữu ích.

---

Đi mua linh kiện robot lần đầu mà không có bảng vật tư (**BOM — Bill of Materials**) rất giống việc đi siêu thị khi đang đói mà không có danh sách: bạn mang về một túi đầy bo mạch và cảm biến lẻ tẻ, nhưng khi ngồi lắp mới phát hiện mạch lái động cơ làm tụt mất 2 volt của pin, còn đầu nối pin lại không khớp với công tắc! Đọc hiểu BOM bằng con mắt kỹ sư giúp bạn chọn đúng từng cụm linh kiện tương thích điện áp, dòng điện và cơ khí ngay từ đầu.

## Kiến thức cần nhớ: Tư duy Hệ thống đằng sau một Bảng BOM Robot

1. **Chuỗi Năng lượng (Pin → Cầu chì → Công tắc → Buck 5 V → Vi điều khiển & Driver):** Mọi linh kiện trên xe phải cùng nằm trong một "ngân sách điện áp và dòng điện" khép kín — điện áp pin phải lớn hơn điện áp định mức động cơ cộng sụt áp driver, nhưng nhỏ hơn giới hạn tối đa của mạch hạ áp.
2. **Hiệu suất Mạch lái Động cơ (BJT L298N vs. MOSFET TB6612FNG):** Không phải cầu H nào cũng giống nhau! Mạch dùng transistor lưỡng cực cũ (L298N) sụt áp tới $$2\text{ V}$$ và tỏa nhiệt dữ dội, trong khi mạch dùng MOSFET hiện đại (TB6612FNG / DRV8833) có điện trở mở $$R_{\text{DS(on)}}$$ cực nhỏ, giữ pin bền hơn và xe khỏe hơn hẳn.
3. **Quản lý Rủi ro Mua sắm theo Đợt:** Tách BOM thành các đợt tương ứng với từng chương học giúp bạn kiểm chứng từng khối hoạt động trước khi chi tiền nâng cấp lên SBC và LiDAR.

### Ví dụ làm từng bước: So sánh tổn hao nhiệt L298N vs. TB6612FNG và Tính thời lượng pin 2S

**Phần A — Tổn hao công suất trên mạch lái khi kéo dòng $$I = 1.0\text{ A}$$ (2 động cơ chạy cùng lúc):**
- **L298N (cầu H BJT, sụt áp $$V_{\text{drop}} \approx 2.0\text{ V}$$):**
  $$
  P_{\text{nhiệt, L298N}} = V_{\text{drop}} \times I = 2.0\text{ V} \times 1.0\text{ A} = \mathbf{2.0\text{ W}}!
  $$
  Nếu pin 2S chỉ có $$7.4\text{ V}$$, động cơ chỉ còn nhận được $$7.4 - 2.0 = \mathbf{5.4\text{ V}}$$ (mất tới 27% điện áp thành nhiệt đốt tản nhiệt!).
- **TB6612FNG (cầu H MOSFET, tổng $$R_{\text{on}} \approx 0.5\ \Omega$$):**
  $$
  P_{\text{nhiệt, TB6612}} = I^2 \cdot R_{\text{on}} = (1.0)^2 \times 0.5 = \mathbf{0.5\text{ W}} \quad (\text{mát hơn }\mathbf{4\times}\text{!})
  $$
  Điện áp sụt chỉ $$1.0 \times 0.5 = 0.5\text{ V}$$, động cơ nhận đủ $$6.9\text{ V}$$ mạnh mẽ hơn hẳn!

**Phần B — Thời lượng chạy của bộ pin 2S 18650 (2.200 mAh, 7.4 V):** năng lượng định mức $$E = 7.4 \times 2.2 = \mathbf{16.28\text{ Wh}}$$. Với dòng xả trung bình toàn xe $$0.8\text{ A}$$ và giữ lại $$15\%$$ dung lượng chống xả cạn:

$$
t_{\text{chạy}} = \frac{2.2\text{ Ah} \times 0.85}{0.8\text{ A}} \approx \mathbf{2.34\text{ giờ}}.
$$

### Giải thích: 4 bước rà soát bảng BOM trước khi nhấn nút đặt hàng

1. **Bước 1 — Khớp mức logic giữa MCU và ngoại vi:** ESP32/Pico dùng logic **3,3 V**; nếu mua cảm biến xuất 5 V (như HC-SR04 bản cũ), bắt buộc phải có sẵn điện trở chia áp hoặc mạch chuyển mức trong BOM.
2. **Bước 2 — Kiểm tra dòng hãm trục (stall current) của động cơ:** Driver động cơ và cầu chì phải chịu được dòng khởi động/kẹt bánh, không chỉ dòng không tải.
3. **Bước 3 — Mua dư linh kiện tiêu hao giá rẻ:** Điện trở, LED, tụ 100 µF, dây jumper và đầu nối nên mua dư 20–30% để không bị đứt mạch thực hành chỉ vì cháy 1 linh kiện giá 1.000 đồng.
4. **Bước 4 — Đồng bộ chuẩn giắc cắm (JST / XT30 / DC barrel):** Tránh cảnh pin một kiểu giắc, sạc một kiểu giắc và mạch công tắc lại là dây trần phải xoắn tay!

**Kiểm tra nhanh.** Nếu bạn dùng động cơ vàng TT (điện áp định mức 6 V) với pin 2S (7.4 V) qua TB6612FNG (sụt áp 0.5 V), điện áp tối đa đặt lên động cơ là $$6.9\text{ V}$$. Làm sao tránh quá áp? Giới hạn hệ số xung PWM tối đa ở khoảng $$6.0 / 6.9 \approx \mathbf{87\%}$$ trong firmware!

---

## Vì sao bài này quyết định Capstone

Bài teleop ở Chương 07 thường hỏng bởi những nguyên nhân phần cứng rất dễ tránh: mạch lái gây sụt khoảng 2 V, cổng USB phải gánh dòng kéo bánh xe, chân echo 5 V cắm thẳng vào chân GPIO 3,3 V, hoặc mạch sạc một cell 4,2 V bị kẹp lên bộ pin 8,4 V. ROS 2 không thể khắc phục các lỗi phần cứng này. Bảng BOM giúp đảm bảo phần cứng khớp hoàn toàn với firmware; mua đúng thông số là điều kiện đầu tiên để robot chạy ổn định.

![Các nhóm đồ trong kit]({{ site.imgurl }}/generated/kit_catalog_overview.png)

![Thứ tự nguồn: mass chung, logic, tín hiệu, nguồn motor bật sau cùng, bánh không chạm bàn]({{ site.imgurl }}/generated/power_order.png)

## Bạn đang mua những gì

BOM (Bill of Materials) là bảng liệt kê mọi linh kiện và dụng cụ cần có trên bàn làm việc — kể cả những món bạn đã sở hữu sẵn như tua-vít — chứ không phải ảnh chụp giỏ hàng. Mỗi dòng trong bảng phải trả lời rõ: đó là gì, số lượng bao nhiêu, thông số kỹ thuật tối thiểu chấp nhận được, vai trò trên robot, phương án thay thế và nơi mua. Nếu bỏ trống cột thông số, bạn sẽ không phân biệt được linh kiện thay thế đúng chuẩn với hàng giá rẻ có ngoại hình tương tự.

Robot mặc định của khóa học là **xe dẫn động vi sai**: gồm hai bánh chủ động, một bánh đa hướng, vi điều khiển logic 3,3 V, mạch lái động cơ MOSFET, một cảm biến khoảng cách, và nguồn pin động cơ cách ly hoàn toàn khỏi đường 3,3 V. Các cảm biến như IMU, encoder bánh xe hay ToF là phần bổ sung sau khi xe đã chạy theo lệnh. Lộ trình B sẽ thêm máy tính cài Ubuntu 24.04 cho ROS 2 Jazzy. Bạn không nên mua LiDAR ngay tuần đầu chỉ để tạo cảm giác sẵn sàng; LiDAR quét phẳng (LD06 hoặc RPLIDAR A1), Raspberry Pi 5 hoặc Jetson và bộ pin có mạch BMS được xếp ở Đợt 4 bên dưới, đúng thời điểm các chương sau cần dùng.

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

## Danh sách Lộ trình A mặc định

Danh sách được chia thành ba đợt để ngay cả khi khung xe giao chậm, bạn vẫn có thể bắt đầu Chương 01 đúng kế hoạch.

**Đợt 1 — bàn lab (để học Chương 01 ngay tuần này):** đồng hồ vạn năng, mỏ hàn khoảng 60 W kèm giá đỡ, thiếc hàn, kìm cắt, breadboard không hàn, dây cắm jumper, cáp USB truyền dữ liệu, mạch vi điều khiển, vài đèn LED và một nút nhấn.

**Đợt 2 — chuyển động (chuẩn bị trước Chương 05):** khung xe (hoặc động cơ TT rời kèm gá bắt và bánh đa hướng), mạch lái TB6612FNG (hoặc phương án nhỏ hơn là DRV8833), cảm biến siêu âm HC-SR04 và mạch chuyển mức logic 3,3 V / 5 V cho chân echo.

**Đợt 3 — năng lượng (sau khi bạn đã biết đo điện áp):** hai cell pin 18650 có dung lượng thực tế, đế giữ pin và bộ sạc nạp **từng cell riêng lẻ** lên 4,2 V. Lưu ý rằng đế pin nối tiếp gắn trên xe không phải là bộ sạc.

Chưa cần đưa vào đơn hàng đầu tiên: RPLIDAR, Raspberry Pi 5, máy hiện sóng, nguồn 12 V 10 A, và các "combo xe robot" đóng gói sẵn mạch L298N cùng hộp 4 pin AA không rõ thông số.

### Bảng tổng hợp bộ kit

Các thông số dưới đây tổng hợp từ datasheet phổ biến và trang sản phẩm Hshop dẫn ở mục mua hàng. Khi nhận linh kiện, hãy luôn kiểm tra trực tiếp ký hiệu in trên thân IC.

| Hạng mục | SL | Thông số chấp nhận | Vai trò trên Capstone | Gợi ý nên mua | Phương án thay thế |
|------|---:|--------------------|------------------------|-------------|----------------|
| Vi điều khiển | 1 | GPIO 3,3 V, có chip USB-UART, từ 20 chân khả dụng | Chạy firmware, về sau làm teleop Wi-Fi | Mạch phát triển ESP32 (~30 chân), chip CH340 hoặc CP2102 | Pico 2 nếu ưu tiên teleop qua USB trước, Wi-Fi để sau |
| Khung xe | 1 | Hai bánh chủ động, có sàn lắp mạch | Thân xe vi sai | Kit 2WD mica động cơ TT, hoặc kit 4WD của Hshop (chỉ dùng 2 bánh chủ động kèm bánh đa hướng) | Động cơ TT rời, 2 bánh xe, 2 gá bắt, 1 bánh đa hướng và 1 tấm đế cứng |
| Động cơ TT | 2 bánh dẫn | Điện áp 3–9 V, tỉ số truyền khoảng 1:48 | Dẫn động bánh trái và phải | Động cơ đi kèm khung xe | Động cơ TT 1:48 của Hshop (giá tham khảo 20.000 ₫/cái) |
| Mạch lái (Driver) | 1 | Cầu H MOSFET, VM khoảng 5–10 V, mỗi kênh ≥ 1 A liên tục | Điều khiển chiều quay và tốc độ PWM | Module TB6612FNG (VM 4,5–10 V, 1,2 A liên tục / 3,2 A đỉnh) | DRV8833 (VM 2,7–10,8 V, tối đa 1,5 A/kênh; dễ nóng khi kẹt bánh) |
| Cảm biến khoảng cách | 1 | HC-SR04 hoặc cảm biến ToF nhỏ | Đo khoảng cách vật cản | HC-SR04 | Module VL53L0X nếu muốn dùng giao tiếp I²C và mức 3,3 V ngay từ đầu |
| Chuyển mức logic | 1 | 4 kênh 3,3 V ↔ 5 V | Hạ mức chân echo HC-SR04 về ESP32 | Module chuyển mức MOSFET | Cầu chia áp chỉ cho chân echo (lưu ý trig 3,3 V có thể thiếu ổn định với một số module kém) |
| Pin động cơ | 2 cell | Li-ion 18650, dung lượng công bố ≤ 3500 mAh | Cấp nguồn VM qua mạch lái | Cell rời, tháo ra sạc **bên ngoài** xe | 6 pin AA (~9 V) nếu chưa muốn dùng lithium; không dùng pin vuông 9 V |
| Bộ sạc | 1 | 4,2 V mỗi cell, tự ngắt khi đầy | Sạc riêng từng cell | Bộ sạc khay 4 ngăn 18650 | TP4056 **chỉ** dùng cho 1 cell đơn, tuyệt đối không kẹp lên đế 2S |
| Đồng hồ vạn năng | 1 | Đo V DC, Ω, có còi thông mạch | Kiểm tra dây và nguồn | UNI-T UT33D+ hoặc mẫu phổ thông tương đương | Đồng hồ bất kỳ có còi thông mạch; thang đo dòng phải có cầu chì |
| Mỏ hàn | 1 | ~60 W, có giá đỡ, thiếc 0,8 mm | Hàn dây động cơ và hàng chân header | Mỏ hàn 60 W thông thường là đủ | Trạm hàn chỉnh nhiệt để nâng cấp về sau |
| Mạch thử | 1 | Breadboard 830 lỗ, dây cắm đực-đực và đực-cái | Thực hành Chương 01–03 | — | Breadboard 400 lỗ nếu bố trí dây ngắn |
| Ốc vít | 1 bộ | Vít M3, trụ đồng/nhựa cách điện | Cố định mạch cách ly khỏi bề mặt dẫn điện | Thường có sẵn trong bộ khung | Bộ ốc M3 mua tại cửa hàng cơ khí |

## Vì sao mạch lái không phải "cầu H nào cũng như nhau"

Trên Hshop tại thời điểm khảo sát, cả module L298N và TB6612FNG đều có giá **45.000 ₫** (mã SKU HS0695V và HS2458V), nên sự khác biệt không nằm ở giá bán. L298N sử dụng cầu Darlington nên khi có dòng động cơ chạy qua, nó làm sụt khoảng 1,8 V đến 2,5 V giữa pin và động cơ. Ngược lại, TB6612FNG dùng cầu MOSFET nên gần như truyền trọn vẹn điện áp nguồn tới động cơ:

$$
V_{motor} \approx V_{pin} - V_{roi}
$$

Với bộ pin hai cell có điện áp danh định 7,4 V (ước tính sụt 2,0 V trên Darlington và 0,3 V trên MOSFET):

$$
V_{L298} \approx 7{,}4 - 2{,}0 = 5{,}4\,\text{V}
$$

$$
V_{TB6612} \approx 7{,}4 - 0{,}3 = 7{,}1\,\text{V}
$$

Theo trang sản phẩm động cơ TT tỉ số 1:48 trên Hshop, điện áp khuyến nghị là **3–9 V**, dòng không tải **110–150 mA**, tốc độ khoảng **200–208 vòng/phút ở 5–6 V**, và mô-men **0,8 kg·cm ở 6 V**. Như vậy, mức 5 V vốn đã nằm ở vùng chạy chậm và yếu. Nếu dùng 4 pin AA mới (~6 V) đi qua L298N, điện áp đến động cơ chỉ còn gần 4 V khiến xe di chuyển rất yếu. Ngoài ra, module L298N tích hợp IC ổn áp 7805, nhưng bạn không nên lấy 5 V từ mạch này để nuôi ESP32 khi nguồn động cơ vượt 12 V — và ngay cả khi bộ pin dưới 10 V, vẫn không nên nuôi vi điều khiển từ chân 5 V của mạch lái. Trong khi đó, chân logic của TB6612FNG hoạt động trong dải **2,7–5,5 V**, tương thích trực tiếp với mức cao 3,3 V của GPIO. Lưu ý rằng chân STBY phải được kéo lên mức cao để đánh thức cầu H.

Module DRV8833 có giá **25.000 ₫**, dải VM **2,7–10,8 V** và dòng tối đa **1,5 A mỗi kênh** theo thông số trên Hshop. Mạch này dùng thay thế tốt khi mỗi kênh kéo một động cơ TT, nhưng do diện tích đồng tản nhiệt và vỏ IC nhỏ hơn TB6612 nên sẽ nhanh nóng nếu bánh bị kẹt lâu. Không mắc song song hai động cơ trên cùng một kênh DRV8833.

Cần phân biệt rõ dòng kẹt trục với dòng không tải. Trang bán hàng không công bố dòng kẹt, vì vậy bạn cần dự phòng dòng gấp vài lần mức 150 mA và tự **đo kiểm** về sau (nhấc bánh khỏi bàn, mắc đồng hồ nối tiếp và cấp một xung ngắn). Chọn mạch lái chỉ dựa vào nhãn quảng cáo "2 A" là chưa đủ căn cứ.

![Ý tưởng cầu H: vi điều khiển chỉ chọn chiều dòng, không phải nguồn cấp dòng cho motor]({{ site.imgurl }}/generated/hbridge_concept.png)

## Pin, đế giữ pin và bộ sạc là một tổ hợp thống nhất

Một cell 18650 có điện áp danh định khoảng 3,6–3,7 V và **đầy ở 4,2 V**. Hai cell lắp trong đế "2×18650 nối tiếp" tạo ra **7,4 V danh định và 8,4 V khi đầy**. Điện áp này chỉ nối vào chân VM của mạch lái, tuyệt đối không đưa vào GPIO hay vào mạch sạc TP4056.

Các mạch TP4056 trên Hshop (bản USB-C giá 10.000 ₫ và bản mini-USB giá 2.000 ₫) là mạch sạc **một cell**, hoạt động bằng cách nạp một cell lên 4,2 V ở dòng khoảng 1 A. Kẹp mạch này lên hai đầu đế pin 2S sẽ ép mạch 4,2 V làm việc với cụm 8,4 V hoặc gây lệch áp giữa hai cell — cả hai đều sai và mất an toàn. Cách đúng là sạc riêng từng cell trong bộ sạc có khay, đo điện áp hở mạch nằm trong khoảng 3,6 V đến 4,20 V rồi mới lắp vào đế trên xe. Bộ sạc 4 khay cổng USB trên Hshop có giá **68.000 ₫** (hỗ trợ 14500 / 18650 / 21700); bạn nên thử nghiệm với một khay trước cho đến khi kiểm chứng được mạch ngắt ổn định.

Dung lượng pin có giới hạn vật lý: cell 18650 thật hiếm khi vượt quá 3500 mAh, phổ biến ở mức 2000–3000 mAh. Hshop niêm yết cell Sunpower **2000 mAh giá 35.000 ₫** và **2500 mAh giá 45.000 ₫**. Những bài đăng rao bán cell 9900 mAh hay 12000 mAh ở tầm giá tương đương đều là thông số giả. Ký hiệu "10C" trên tên pin Sunpower là thông số dòng xả công bố, không phải dung lượng; không nên tin tuyệt đối vào hệ số C khi không có datasheet, và hai động cơ TT cũng không đòi hỏi dòng xả quá lớn như vậy.

Cell pin phổ thông thường **không có mạch bảo vệ** tích hợp. Chạm tua-vít qua hai cực có thể gây phóng dòng hàng chục ampe tức thời. Không bỏ cell trần vào túi cùng chìa khóa, không sạc trên bề mặt dễ cháy, và ngưng sử dụng ngay nếu cell bị phồng, tụt dưới 2,5 V hoặc nóng bất thường. Một lỗi phổ biến khác là dùng pin vuông 9 V: nội trở lớn khiến điện áp sụp ngay khi động cơ kẹt, làm vi điều khiển khởi động lại trong khi mạch lái vẫn giữ lệnh chạy.

Khi thực hành trên bàn, hãy cấp nguồn vi điều khiển bằng cáp USB, nối mass chung giữa USB và mạch lái, và chỉ bật nguồn pin động cơ sau cùng khi bánh xe đã được nhấc lên.

## Đợt 4 — máy tính nhúng trên xe, LiDAR và pin nâng cấp (cho Chương 07, 09, 11)

Các đợt 1 đến 3 ở trên đã đủ để xe hoàn thành teleop. Những món trong bảng dưới đây **không** nằm trong đơn hàng tuần đầu mà chỉ mua khi học tới chương tương ứng. Cột giá được để trống để bạn tự điền đúng mức giá tại thời điểm mở trang mua hàng:

| Hạng mục | Thời điểm | Vai trò trên lộ trình | Nguồn tìm kiếm tham khảo | Giá (điền khi mua) |
| --- | --- | --- | --- | --- |
| Raspberry Pi 5 (RAM đủ chạy Ubuntu Server 24.04) | Đầu Chương 09 nếu muốn xe chạy độc lập không cần laptop | Máy tính chạy ROS 2 Jazzy, agent và bridge | [Hshop, raspberry pi](https://hshop.vn/search?q=raspberry+pi), [Shopee, Raspberry Pi 5](https://shopee.vn/search?keyword=raspberry%20pi%205) | |
| Jetson Orin Nano | Chỉ khi cần GPU xử lý trực tiếp trên xe | Lưu ý: JetPack 6 dùng Ubuntu 22.04 (không cài Jazzy gốc), JetPack 7 dùng Ubuntu 24.04. Đọc kỹ [quick start](https://docs.nvidia.com/jetson/orin-nano-devkit/user-guide/latest/quick_start.html) trước khi mua | Tìm `Jetson Orin Nano` trên [Shopee](https://shopee.vn/search?keyword=jetson%20orin%20nano) hoặc nhà phân phối có hóa đơn rõ ràng | |
| LiDAR quét phẳng LD06 hoặc RPLIDAR A1 | Chương 11, bài lab SLAM thực tế | Xuất dữ liệu `/scan` cho `slam_toolbox` (cảm biến ToF một tia không thay thế được) | [Hshop, lidar](https://hshop.vn/search?q=lidar), [Slamtec A1](https://www.slamtec.com/en/Lidar/A1), [LDRobot](https://www.ldrobot.com/) | |
| Pin LiPo 2S có giắc cân bằng, LiFePO4 đúng sạc, hoặc dùng tiếp 18650 Đợt 3 | Trước bài lắp khung Chương 07 | Cấp nguồn VM (tuyệt đối không dùng lẫn chế độ sạc giữa các loại pin) | [Hshop, lipo](https://hshop.vn/search?q=lipo); cell 18650 xem ở mục Nguồn bên dưới | |
| Mạch BMS đúng số cell và loại hóa học (nếu pack chưa có) | Mua cùng lúc với pin | Bảo vệ quá áp / dưới áp (không thay thế cầu chì) | Tìm `BMS 2S` trên [Shopee](https://shopee.vn/search?keyword=bms%202s) hoặc [Lazada](https://www.lazada.vn/catalog/?q=bms%202s); kiểm tra nhãn Li-ion hay LiFePO4 | |
| Mạch hạ áp (buck) và cầu chì 2 A, 3 A | Chương 07 | Tạo nguồn 5,0 V cho ESP32 và lắp cầu chì trên dây dương | Xem bài pin Chương 07; tham khảo [Thế Giới IC](https://www.thegioiic.com/), [IC Đây Rồi](https://icdayroi.com/) | |

Raspberry Pi 5 và Jetson Orin Nano là hai lựa chọn thay thế nhau cho một máy Ubuntu trên xe, không cần mua cả hai; tương tự, chỉ chọn một trong hai mẫu LiDAR LD06 hoặc A1. Bạn sẽ học cách tính chọn cầu chì ở bài [Pin, nguồn và an toàn]({% multilang_post_url contents/chapter07/07_00_batteries_power_safety %}) và cách chọn đúng ảnh hệ điều hành Ubuntu 24.04 ở bài [Linux trên SBC]({% multilang_post_url contents/chapter09/09_00_linux_on_sbc %}). Nguyên tắc không mua LiDAR sớm ở tuần đầu vẫn giữ nguyên cho đến Chương 11.

## Kinh nghiệm đặt mua và kiểm hàng

Hãy luôn mua dựa trên thông số kỹ thuật thay vì ảnh minh họa hay nhãn giảm giá: một bộ L298N giảm giá 30% vẫn là loại mạch lái gây sụt áp lớn. Trước khi đặt hàng, cần đọc kỹ dải điện áp, dòng liên tục, mức logic và loại giắc cắm.

Với Đợt 1, nên gom chung tại một cửa hàng để tránh cảnh thiếu sợi cáp USB mà phải chờ thêm đơn hàng khác. Tại Việt Nam, Hshop (`hshop.vn`, địa chỉ 269/20 Lý Thường Kiệt, Phường Phú Thọ, TP.HCM) có mô tả kỹ thuật và mã SKU rõ ràng (các mã SKU kết thúc bằng chữ **V** là giá công ty đã bao gồm VAT; cửa hàng cũng yêu cầu quay video mở hộp trong 7 ngày cho bảo hành cơ bản). Trên Shopee và Lazada, hãy lọc các gian hàng uy tín, đọc kỹ xem sản phẩm là mạch phát triển (dev board) hay module trần, và ưu tiên nơi có ảnh chụp rõ chữ in trên IC. Thế Giới IC (`thegioiic.com`) và IC Đây Rồi (`icdayroi.com`, Thủ Đức) là các cửa hàng linh kiện rất phù hợp khi mua IC ổn áp hoặc module rời, nhưng cần chú ý phân biệt module ESP32 trần với mạch phát triển có sẵn cổng USB.

Với cửa hàng điện tử chuyên dụng, bạn có thể chuyển khoản sau khi xác nhận còn hàng; với sàn thương mại điện tử, nên thanh toán qua hệ thống của sàn cho các món như dây jumper hay khung xe. Tránh chuyển khoản trực tiếp cho người bán không rõ nguồn gốc trên mạng xã hội để mua "pin 18650 đã test" mà không có chính sách đổi trả.

Khi kiện hàng giao tới, hãy kiểm tra theo đúng 7 bước sau trước khi lắp ráp:
1. Quay video quá trình mở hộp và kiểm đếm từng túi linh kiện đối chiếu với `bom.csv`.
2. Kiểm tra đồng hồ vạn năng: chạm hai que đo phải kêu bíp thông mạch, sau đó đo thử khoảng 5 V trên một củ sạc USB đáng tin cậy.
3. Kiểm tra vi điều khiển: cắm bằng cáp USB **có truyền dữ liệu** vào máy tính và xác nhận xuất hiện cổng serial mới (cáp chỉ sạc sẽ không hiện cổng và dễ bị nhầm là mạch hỏng).
4. Khi chỉ cắm USB, đo chân 3,3 V phải đạt khoảng 3,3 V; nếu đo ra 5 V thì dừng ngay.
5. Kiểm tra mạch lái: đọc chữ in trên thân IC để chắc chắn là TB6612FNG hoặc DRV8833, không phải L298N.
6. Kiểm tra động cơ: xoay nhẹ trục bằng tay xem có bị sượng không và đối chiếu tỉ số truyền ghi trên bao bì với đơn đặt hàng.
7. Kiểm tra cell pin: vỏ không phồng, điện áp mỗi cell nằm trong khoảng 3,4 V đến 4,2 V; không lắp nối tiếp trước khi đo đủ cả hai viên.

## Mua ở Việt Nam

Các liên kết dưới đây bao gồm **trang sản phẩm đã ghi nhận giá ngày 23 tháng 9 năm 2026** và **trang tìm kiếm theo từ khóa** (được ghi chú rõ). Với trang tìm kiếm, kết quả đầu tiên không phải lúc nào cũng đúng món cần mua nên bạn vẫn cần đọc kỹ thông số. Trên Lazada, bạn có thể tìm theo cấu trúc `https://www.lazada.vn/catalog/?q=` kèm từ khóa trên trình duyệt thông thường.

### Vi điều khiển

Từ khóa gợi ý: `ESP32 NodeMCU 38 chân CH340`, `ESP32 DevKit V1`, `Raspberry Pi Pico 2`.

- Trang Hshop đã kiểm: [ESP32 NodeMCU-32S CH340 Ai-Thinker, 190 000 ₫](https://hshop.vn/kit-rf-thu-phat-wifi-ble-esp32-nodemcu-32s-ch340-ai-thinker) — đây là mạch phát triển có sẵn USB, phù hợp để chọn mua.
- Trang Hshop đã kiểm (phân khúc cao hơn): [Vietduino ESP32, 265 000 ₫](https://hshop.vn/mach-phat-trien-vietduino-esp32).
- Trang Hshop đã kiểm (**không** chọn làm mạch duy nhất ban đầu): [module ESP32-S3-WROOM-1, 135 000 ₫](https://hshop.vn/mach-thu-phat-wifi-ble-soc-esp32-s3-esp32-s3-wroom-1-chinh-hang-espressif) — đây là module trần, chưa có chip USB-UART.
- Trang tìm kiếm Hshop: [raspberry pi pico](https://hshop.vn/search?q=raspberry+pi+pico) (thời điểm khảo sát có Pico 2 giá 195.000 ₫ và Pico 2 W giá 275.000 ₫).
- Trang Thế Giới IC: [ESP32-DevKitC-32U](https://www.thegioiic.com/esp32-devkitc-32u-module-wifi-bluetooth-2-4ghz) — cần đọc kỹ xem bản dùng đầu nối anten U.FL này có kèm sẵn cáp anten ngoài hay không.
- Tìm trên Shopee: [ESP32 DevKit](https://shopee.vn/search?keyword=esp32%20devkit%20ch340).
- Lưu ý: tránh các sản phẩm chỉ chụp ảnh module bọc kim loại không có cổng USB dù tiêu đề vẫn ghi "kit phát triển".

### Khung xe, động cơ, bánh đa hướng

Từ khóa gợi ý: `khung xe robot 2 bánh TT`, `động cơ giảm tốc TT 1:48`, `bánh đa hướng`.

- Tại thời điểm khảo sát, Hshop không có sẵn bộ khung 2WD mica giá rẻ, nhưng có [khung MKE-R01 4WD động cơ TT, 245 000 ₫](https://hshop.vn/khung-xe-mke-r01-4wd-robot-car-chassis-tt-motor). Bạn có thể dùng hai động cơ cho xe Capstone (để hai chiếc còn lại dự phòng) kèm một bánh đa hướng, hoặc chỉ ghép cặp bánh trái/phải sau khi đã đo dòng cụ thể.
- Linh kiện mua rời trên Hshop: [động cơ TT 1:48, 20 000 ₫](https://hshop.vn/dong-co-dc-giam-toc-tt-motor-ti-so-1-48), [bánh 65 mm, 8 000 ₫](https://hshop.vn/banh-xe-dong-co-dc-giam-toc-v1-plastic-geared-tt-motor-65mm), [gá bắt động cơ, 10 000 ₫](https://hshop.vn/ga-bat-dong-co-dc-giam-toc-tt-motor-mounting-bracket), [bánh đa hướng, 15 000 ₫](https://hshop.vn/banh-xe-nhua-da-huong-3pi-ball-caster-wheel).
- Tìm trên Shopee (trang tìm kiếm chung): [khung xe 2 bánh TT](https://shopee.vn/search?keyword=khung%20xe%20robot%202%20b%C3%A1nh%20TT) — mức giá phổ biến khoảng **90.000–180.000 ₫**; cần kiểm tra ảnh có đủ hai động cơ, bánh đa hướng và hộp pin.
- Tìm trên Lazada: [khung xe robot](https://www.lazada.vn/catalog/?q=khung%20xe%20robot%202%20banh).
- Tránh các bộ "kit robot" ghép sẵn L298N với hộp 4 pin AA.

### Driver động cơ

Từ khóa gợi ý: `TB6612FNG`, `DRV8833` (không chọn `module L298 giá rẻ` làm mặc định).

- Đã kiểm: [TB6612FNG, 45 000 ₫, SKU HS2458V](https://hshop.vn/mach-dieu-khien-dong-co-dc-tb6612fng-dc-motor-driver) — VM 4,5–10 V, logic 2,7–5,5 V, dòng 1,2 A liên tục, 3,2 A đỉnh, kích thước 20×20 mm.
- Phương án thay thế đã kiểm: [DRV8833, 25 000 ₫](https://hshop.vn/mach-dieu-khien-dong-co-drv8833-dc-motor-driver) — VM 2,7–10,8 V, dòng tối đa 1,5 A/kênh theo mô tả.
- Sản phẩm tham khảo nhưng **không** dùng làm mặc định: [module L298N, cùng giá 45 000 ₫](https://hshop.vn/mach-dieu-khien-dong-co-dc-l298) — chỉ cân nhắc nếu bạn nắm rõ mức sụt áp và dùng động cơ loại 12 V.
- Tìm trên Shopee: [TB6612FNG](https://shopee.vn/search?keyword=tb6612fng).
- Mạch tham chiếu chuẩn nếu có nhu cầu nhập chính hãng về sau: [Pololu 713](https://www.pololu.com/product/713).

### Cảm biến

Từ khóa gợi ý: `HC-SR04`, `VL53L0X`, `MPU6050 GY-521`, `đĩa encoder TT 20 xung`.

- Đã kiểm: [HC-SR04, 27 000 ₫](https://hshop.vn/cam-bien-sieu-am-srf04) — chân echo xuất mức 5 V nên cần mua kèm mạch chuyển mức logic.
- Mạch chuyển mức đã kiểm: [mạch chuyển mức 4 kênh, 10 000 ₫](https://hshop.vn/mach-chuyen-muc-tin-hieu-logic-4-kenh).
- Linh kiện nâng cấp về sau (đã kiểm): [GY-521 MPU6050, 85 000 ₫](https://hshop.vn/cam-bien-6-dof-bac-tu-do-gy-521-mpu6050) — giao tiếp I²C, cấp nguồn 3,3–5 V, logic 3,3 V; chưa cần ở giai đoạn đầu.
- Phương án ToF thay HC-SR04 (đã kiểm): [module VL53L0X, 115 000 ₫](https://hshop.vn/cam-bien-khoang-cach-tof-laser-radar-vl53l0x).
- Đĩa encoder (đã kiểm, kích thước nhỏ rất dễ thất lạc): [đĩa 20 xung, 1 000 ₫](https://hshop.vn/dia-encoder-20-xung-dong-co-dc-giam-toc-v1). Mạch cảm biến quang đọc đĩa là món riêng, tìm theo từ khóa `cảm biến tốc độ encoder hồng ngoại`.
- Tìm trên Shopee: [HC-SR04](https://shopee.vn/search?keyword=hc-sr04).

### Nguồn

Từ khóa gợi ý: `pin 18650 2500mAh`, `sạc 18650 4 ngăn`. Chỉ tìm `TP4056` khi bạn dùng đúng cho mục đích sạc một cell đơn.

- Cell pin đã kiểm: [Sunpower 2500 mAh, 45 000 ₫](https://hshop.vn/pin-sac-18650-li-ion-rechargeable-battery-3-7v-2500mah-10c-sunpower) và [Sunpower 2000 mAh, 35 000 ₫](https://hshop.vn/pin-sac-18650-li-ion-rechargeable-battery-3-7v-2000mah-10c-sunpower).
- Đế pin chân hàn đã kiểm: [đế 2×18650, 4 000 ₫](https://hshop.vn/hop-pin-2-co-18650). Lưu ý nhiều bộ khung xe đã kèm sẵn đế pin, tránh mua dư rồi mắc nối tiếp bốn cell.
- Đế pin không hàn đã kiểm: [đế DIY, 10 000 ₫](https://hshop.vn/hop-pin-ghep-noi-diy-solderless-18650-battery-holder).
- Bộ sạc khay đã kiểm: [sạc 4 ngăn USB, 68 000 ₫](https://hshop.vn/bo-sac-pin-18650-li-ion-usb-battery-charger-yh-18650-4).
- Mạch sạc một cell đã kiểm (**không** dùng cho cụm 2S): [TP4056 USB-C, 10 000 ₫](https://hshop.vn/mach-sac-pin-tp4056-lithium-battery-charge-controller-usb-c).
- Tìm trên Shopee: [sạc pin 18650](https://shopee.vn/search?keyword=s%E1%BA%A1c%20pin%2018650%204%20ng%C4%83n).
- Lưu ý: tránh các mạch "sạc nhanh 2 A" không rõ thiết kế giới hạn dòng và mọi cell pin quảng cáo trên 3500 mAh.

### Dụng cụ và mạch thử

Từ khóa gợi ý: `đồng hồ vạn năng`, `mỏ hàn 60W`, `breadboard 830`, `dây breadboard đực cái`.

- Đồng hồ vạn năng đã kiểm: [UNI-T UT33D+, 285 000 ₫](https://hshop.vn/dong-ho-van-nang-dien-tu-digital-multimeter-uni-t-ut33d-chinh-hang), [Wadfow WDM1501, 185 000 ₫](https://hshop.vn/dong-ho-van-nang-ky-thuat-so-vom-wadfow-wdm1501-digital-multimeter-true-rms). Mẫu UT136C+ (560.000 ₫) là phương án nâng cấp về sau, chưa cần thiết cho giai đoạn bắt đầu.
- Dụng cụ hàn đã kiểm: [Wadfow WEL3616 60 W, 75 000 ₫](https://hshop.vn/mo-han-60w-wadfow-wel3616-soldering-iron), [giá đỡ, 40 000 ₫](https://hshop.vn/de-gac-mo-han-tron-b-2-co-khay-roi), [thiếc Sn63 0,8 mm, 24 000 ₫](https://hshop.vn/thiec-han-sunchi-kp26-0-8mm-sn63-pb37-solder-wire).
- Kìm đã kiểm: [kìm cắt chân 170, 35 000 ₫](https://hshop.vn/kim-cat-day-dien-nho-170-cat-chan-linh-kien-dien-tu); nếu muốn thêm kìm tuốt dây hạn chế cứa lõi đồng, tham khảo [Wadfow WBQ8401, 130 000 ₫](https://hshop.vn/kim-tuot-day-dien-da-nang-wadfow-wbq8401-wire-stripper).
- Mạch thử đã kiểm: [breadboard 830 lỗ, 35 000 ₫](https://hshop.vn/test-board-cammb-102), [dây đực-đực, 30 000 ₫](https://hshop.vn/day-cam-breadboard-duc-duc-20cm-cap-det-40-soi-m-m-jumper-wire), [dây đực-cái, 30 000 ₫](https://hshop.vn/day-cam-breadboard-duc-cai-20cm-cap-det-40-soi-m-f-jumper-wire), [mạch cấp nguồn breadboard, 25 000 ₫](https://hshop.vn/mach-cap-nguon-cho-breadboard-400-830-lo-mb-102) (nên hoãn dùng mạch cấp nguồn breadboard cho tới khi bạn phân biệt chắc chắn đường 3,3 V và 5 V).
- Cáp USB đã kiểm: [Ugreen Micro-USB 1 m, 54 000 ₫](https://hshop.vn/cap-micro-usb-to-usb-2-0-dai-1m-cao-cap-60136-chinh-hang-ugreen). Cáp dài 30 cm (27.000 ₫) khá bất tiện khi đặt xe dưới sàn; nếu mạch dùng cổng USB-C thì chọn cáp USB-C truyền dữ liệu tương ứng.
- Phụ kiện nhỏ đã kiểm: [bộ LED 3 mm, 20 000 ₫](https://hshop.vn/bo-5-loai-led-sieu-sang-3mm-thong-dung-5-kind-3mm-transparent-color-led), [nút nhấn tròn, 10 000 ₫](https://hshop.vn/nut-nhan-nha-tron-pbs-11b-12mm-kem-cap), [dây điện đỏ đen 1 m, 8 000 ₫](https://hshop.vn/day-dien-do-den).
- Bộ điện trở: tại thời điểm khảo sát, tìm `điện trở` trên Hshop không ra bộ 1/4 W thông dụng, nên bạn có thể tìm trên Shopee theo [bộ điện trở 1/4W](https://shopee.vn/search?keyword=b%E1%BB%99%20%C4%91i%E1%BB%87n%20tr%E1%BB%9F%201%2F4W) (giá thường khoảng **30.000–80.000 ₫**), đảm bảo trong bộ có các trị số 220 Ω, 330 Ω, 1 kΩ và 10 kΩ.
- Tìm dụng cụ trên Shopee: [mỏ hàn 60W](https://shopee.vn/search?keyword=m%E1%BB%8F%20h%C3%A0n%2060W), [đồng hồ vạn năng](https://shopee.vn/search?keyword=%C4%91%E1%BB%93ng%20h%E1%BB%93%20v%E1%BA%A1n%20n%C4%83ng).
- Cửa hàng linh kiện rời: [IC Đây Rồi](https://icdayroi.com/) (khu vực Thủ Đức) và [Thế Giới IC](https://www.thegioiic.com/).

Nhắc lại nguyên tắc đi dây: dây Dupont chỉ dùng cho tín hiệu, còn dòng động cơ phải đi qua dây đỏ đen tiết diện lớn hơn, bắt chặt vào trạm vít hoặc hàn thẳng vào cực của mạch lái thay vì cắm qua hàng lỗ breadboard.

## Giỏ hàng mẫu: bạn Lan, Lộ trình A, trần 2.000.000 ₫

Lan học theo Lộ trình A và muốn làm teleop Wi-Fi ở Chương 08, nên chọn mạch ESP32 NodeMCU-32S thay vì Pico. Vì mới tiếp xúc với pin lithium, cô mua bộ sạc 4 khay để sạc từng cell riêng và tuyệt đối không kẹp TP4056 lên đế nối tiếp. Với bộ khung 4WD, cô tháo bớt hai động cơ để dự phòng và gắn thêm bánh đa hướng. Bảng dưới đây dùng mốc giá Hshop đã ghi nhận ở trên:

| Hạng mục | SL | Đơn giá (₫) | Thành tiền (₫) |
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

Cộng thêm bộ điện trở mua trên Shopee khoảng 50.000 ₫ và phí vận chuyển nội thành khoảng 30.000 ₫, tổng chi phí vào khoảng **1.500.000 ₫**, nằm gọn trong ngưỡng 1.500.000–2.500.000 ₫ và vẫn còn dư ngân sách cho trụ đồng M3 cùng cáp USB dự phòng. Nếu đổi đồng hồ sang Wadfow (185.000 ₫) sẽ tiết kiệm thêm 100.000 ₫. Đổi sang Pico 2 (195.000 ₫) hầu như không rẻ hơn mà lại phải hoãn phần Wi-Fi. Lan cũng cân nhắc việc mua thêm một mạch TB6612 thứ hai để kéo cả bốn bánh thay vì dùng bánh đa hướng, nhưng xác định đó là một cấu hình robot khác nên ghi rõ là phương án bị loại thay vì âm thầm sửa giỏ hàng.

Cô loại bỏ L298N dù cùng giá 45.000 ₫ vì ở nguồn 7,4 V, sụt áp 2,0 V chỉ còn lại 5,4 V — nằm sát vùng yếu (5–6 V, ~200 vòng/phút, 0,8 kg·cm ở 6 V) của động cơ TT. Mạch lái MOSFET giúp giữ điện áp gần mức 7 V để xe vận hành khỏe hơn.

## Thực hành: lập tệp `bom.csv` và kiểm tra từng dòng

Tạo tệp `bom.csv` trong thư mục ghi chú với dòng tiêu đề sau:

```text
part_id,name,qty,role,rating,vendor,url_or_search,unit_vnd,line_vnd,substitute,wave,received,photo,notes
```

**Các bước thực hiện:**

1. Chép danh sách mẫu của Lan, sau đó bỏ hoặc hoãn MPU6050 nếu vượt ngân sách của bạn. Thêm một dòng cho bộ điện trở, tạm ghi giá là "khoảng Shopee, chốt khi mở tin" cho tới khi có giá thực tế.
2. Duy trì đủ ba cột theo dõi thực tế: `received` (`yes`/`no`), `photo` (tên tệp ảnh chụp) và `notes` (ký hiệu đọc trực tiếp trên thân IC).
3. Ở dòng mạch lái, ghi rõ dải điện áp VM và ghi chú "không lấy L298N" vào cột `notes`.
4. Ở dòng bộ sạc, ghi chú "mỗi khay một cell, không kẹp lên đế 2S".
5. Nếu hàng chưa giao tới, để `received` là `no` nhưng vẫn phải hoàn thiện toàn bộ bảng; khi mạch và đồng hồ về tới thì chụp ảnh bổ sung.
6. Tính tổng cột `line_vnd`. Nếu vượt 2.500.000 ₫, cắt giảm theo thứ tự ưu tiên: cảm biến IMU, kìm tuốt dây, mạch cấp nguồn breadboard — không cắt đồng hồ vạn năng hay mạch lái động cơ.

**Kết quả cần đạt:** Một tổng chi phí có thể giải thích rõ ràng trong một phút; dòng mạch lái nêu rõ phương án thay thế là DRV8833 và loại bỏ L298N; dòng bộ sạc đảm bảo không dùng TP4056 cho đế pin nối tiếp.

**Các lỗi thường gặp:**

| Tình huống gặp phải | Nguyên nhân | Cách khắc phục |
|----------|-----------|----------|
| Giỏ hàng rẻ nhưng dùng mạch lái L298N | Bỏ qua yếu tố sụt áp cầu Darlington | Đổi sang TB6612FNG hoặc DRV8833; phần mềm không bù được sụt áp |
| Dòng ESP32 trỏ tới module WROOM trần | Không có cổng USB-UART | Đổi sang mạch phát triển (dev board) có sẵn cổng USB |
| Đặt hai cell 18650 kèm một mạch TP4056 | Sạc 4,2 V không tương thích cụm 8,4 V | Đổi sang bộ sạc khay để nạp riêng từng cell |
| Cột dung lượng pin ghi 9900 mAh | Thông số công bố sai sự thật | Bỏ qua sản phẩm đó, chọn cell uy tín ≤ 3500 mAh |
| Chọn cáp USB dài 30 cm | Quá ngắn khi thử xe trên sàn hoặc bàn | Đổi sang cáp truyền dữ liệu dài 1 m |
| Dự định đi dây động cơ bằng dây Dupont | Tiếp điểm breadboard gây sụt áp và sinh nhiệt | Dùng dây đỏ đen tiết diện lớn nối qua trạm vít |

**Lưu ý an toàn:** Rủi ro thực sự của bài này nằm ở pin lithium, không phải ở tệp bảng tính. Luôn sạc pin ở nơi dễ quan sát, tránh làm chập hai cực đế pin, và tuyệt đối không nối nguồn VM vào chân 5 V hay 3,3 V của ESP32 để "thử pin".

## Video tham khảo

- **Xem trước:** [PART1: Building Low-Cost Differential Wheeled Robot For Machine Learning, SLAM, and ROS](https://www.youtube.com/watch?v=RsZBxfpcLu8) — Aleksandar Haber PhD, tiếng Anh. Minh họa một mẫu xe vi sai chi phí thấp và các linh kiện thực tế cần dùng; hãy đối chiếu với bảng BOM của khóa thay vì sao chép nguyên giá trong video.
- [How To Read A Datasheet - Electronics with Becky Stern | DigiKey](https://www.youtube.com/watch?v=v2d5H5k_SAc) — DigiKey, tiếng Anh. Hướng dẫn cách đọc trang sản phẩm linh kiện tương tự đọc datasheet: chú ý điện áp, dòng điện và những thông số bị lược bỏ.

## Bài tập

1. Giả sử cụm pin 2S đang ở mức 8,0 V. Mạch L298N làm sụt 2,2 V còn mạch TB6612 làm sụt 0,4 V. Động cơ TT nhận được bao nhiêu vôn trong mỗi trường hợp, và mức nào nằm tốt hơn trong dải 3–9 V của động cơ?
2. Bạn có một đế pin nối tiếp 2S và chỉ có một mạch sạc TP4056. Hãy viết đúng trình tự nạp cả hai cell mà không kẹp mạch sạc lên cụm nối tiếp.
3. Một bài đăng trên Shopee có tiêu đề "ESP32 WiFi Bluetooth", nhưng ảnh chụp là module bọc vỏ kim loại có hàng chân hàn viền ngoài và không có cổng USB. Món này tương ứng với dòng nào trong BOM và còn thiếu phần nào?
4. Chân echo của HC-SR04 xuất mức 5 V trong khi chân GPIO của vi điều khiển chỉ chịu 3,3 V. Bạn cần thêm linh kiện nào, và dùng phép đo gì để chắc chắn chân echo chưa bị nối thẳng vào GPIO?
5. Tổng tiền linh kiện trước vận chuyển là 1.420.000 ₫, phí vận chuyển 35.000 ₫ và bộ điện trở 55.000 ₫. Nếu Lan mua thêm một mạch TB6612 nữa giá 45.000 ₫ thì tổng chi phí có còn dưới mức trần 2.000.000 ₫ không? Hãy viết phép tính cụ thể.

<details>
<summary>Gợi ý đáp án</summary>

1. Qua L298N: $$8{,}0 - 2{,}2 = 5{,}8\,\text{V}$$. Qua TB6612: $$8{,}0 - 0{,}4 = 7{,}6\,\text{V}$$. Cả hai đều nằm trong dải 3–9 V, nhưng 7,6 V giúp động cơ khỏe hơn rõ rệt so với mốc mô-men chuẩn 6 V trên bảng thông số, còn 5,8 V nằm về phía yếu.
2. Tháo rời hai cell khỏi đế. Nạp cell A đơn lẻ cho đến khi TP4056 báo đầy và ngắt gần 4,2 V, sau đó lặp lại tương tự với cell B. Đo kiểm tra điện áp cả hai viên rồi mới lắp vào đế 2S. TP4056 chỉ dùng cho từng cell rời, không kẹp lên hai cực đế nối tiếp.
3. Đó là module trần, không phải mạch phát triển (dev board). Nó còn thiếu mạch giao tiếp USB-UART và mạch ổn áp 3,3 V; người mới không nên bắt đầu khóa học bằng module trần.
4. Cần bổ sung mạch chuyển mức logic 4 kênh (hoặc cầu chia áp trên riêng chân echo). Khi cảm biến đã cấp nguồn nhưng chưa nối qua mạch chuyển mức, kiểm tra thông mạch để chắc chắn mạng dây echo và chân GPIO không thông trực tiếp với nhau.
5. $$1\,420\,000 + 35\,000 + 55\,000 + 45\,000 = 1\,555\,000$$ ₫, vẫn thấp hơn trần 2.000.000 ₫. Tuy nhiên, thêm mạch lái thứ hai đồng nghĩa thay đổi thiết kế sang hệ bốn động cơ chứ không phải phụ tùng dự phòng thông thường, nên cần ghi rõ trong cột ghi chú.

</details>

## Đọc thêm

- [Trang TB6612FNG của Pololu, mã 713](https://www.pololu.com/product/713) — thiết kế mạch MOSFET chuẩn mà các module trên thị trường tham khảo theo.
- [Thư mục DRV8833 của TI](https://www.ti.com/product/DRV8833) — thông số giới hạn dòng và dải điện áp VM của phương án thay thế gọn hơn.
- [Nhóm driver DC chổi than của Pololu](https://www.pololu.com/category/11/brushed-dc-motor-drivers) — giải thích vì sao thông số "2 A" trên mạch Darlington chưa phản ánh đầy đủ khả năng làm việc thực tế.
- [SparkFun: logic levels](https://learn.sparkfun.com/tutorials/logic-levels) — giải thích sự khác biệt giữa tín hiệu echo 5 V và chân GPIO 3,3 V.
- [Battery University, BU-409, nạp lithium-ion](https://batteryuniversity.com/article/bu-409-charging-lithium-ion) — lý thuyết về mức đầy 4,20 V mỗi cell và yêu cầu đối với bộ sạc pin mắc nối tiếp.
- [Datasheet ESP32 của Espressif](https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf) — tài liệu gốc xác nhận điện áp cực đại trên chân GPIO không phải 5 V.
- [Tài liệu module HC-SR04, SparkFun](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf) — thông số thời gian xung trig/echo và mức điện áp 5 V của chân echo.
