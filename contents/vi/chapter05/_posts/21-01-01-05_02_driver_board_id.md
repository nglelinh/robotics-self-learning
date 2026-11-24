---
layout: post
title: "Nhận diện driver: L298N, TB6612, DRV8833"
chapter: "05"
order: 2
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter05
lesson_type: required
draft: false
---

Trước khi làm theo bất kỳ sơ đồ đấu nối nào trên mạng, bạn cần nhận diện chính xác con chip được hàn trên bo mạch cầu H, vì L298N, TB6612 và DRV8833 khác nhau hoàn toàn về mức sụt áp, nguồn logic, chân kích hoạt (standby/sleep) và khả năng chịu dòng stall của động cơ TT. Bài này hướng dẫn cách phân biệt ba dòng mạch phổ biến và đo kiểm các đường nguồn trước khi nối chân vi điều khiển.

Nếu bạn từng mua bộ kit xe robot sinh viên và thấy trên mạch có một con chip to đùng gắn miếng tản nhiệt nhôm khổng lồ màu đen mang tên **L298N**, hẳn bạn từng tự hỏi: *tại sao cùng kéo 2 động cơ bánh xe nhỏ xíu mà mạch L298N lại to nặng và nóng ran, còn mạch TB6612FNG hay DRV8833 lại nhỏ bằng đầu ngón tay cái và mát rượi?* Câu trả lời nằm ngay ở công nghệ bán dẫn bên trong cầu H: thế hệ transistor **BJT Darlington** từ thập niên 1980 so với **MOSFET** hiện đại — một khác biệt nhỏ trong datasheet nhưng quyết định trực tiếp việc xe bạn chạy được 20 phút hay 1 giờ trên cùng một cục pin!

## Bản đồ kiến thức nền: So sánh công nghệ bán dẫn trong Driver động cơ

### 1. BJT Darlington (L298N) — sụt áp cố định lớn và tổn hao nhiệt tuyến tính
Mạch L298N dùng các cặp transistor lưỡng cực (BJT) mắc Darlington. Nhược điểm cố hữu của BJT là dù dòng nhỏ hay lớn, mỗi cầu H luôn bị **sụt áp bão hòa $$V_{\text{CE(sat)}} \approx 1{,}8\text{–}3{,}2\text{ V}$$**. Điện áp sụt này không biến mất mà biến thành nhiệt tỏa ra trên miếng nhôm tản nhiệt theo $$P_{\text{tổn hao}} = V_{\text{drop}} \cdot I$$, đồng thời "ăn mất" phần lớn điện áp pin nếu bạn dùng pin 2S (7,4 V) hoặc pin AA (6 V).

### 2. MOSFET (TB6612FNG, DRV8833) — điện trở kênh $$R_{\text{DS(on)}}$$ cực nhỏ
Các driver thế hệ mới dùng công tắc **MOSFET** hoạt động như một điện trở cực nhỏ $$R_{\text{DS(on)}} \approx 0{,}2\text{–}0{,}5\,\Omega$$ (tổng cả nhánh trên + nhánh dưới). Sụt áp chỉ là $$V_{\text{drop}} = I \cdot R_{\text{DS(on)}}$$ và tổn hao nhiệt là $$P = I^2 R_{\text{DS(on)}}$$ — nhỏ hơn L298N từ 4 đến 10 lần ở dòng 1 A, cho phép thu nhỏ mạch xuống cỡ con tem mà không cần tản nhiệt cồng kềnh.

### 3. Mức logic điều khiển (3,3 V vs. 5 V) và các chân bảo vệ
Khi chọn driver cho ESP32/Raspberry Pi (logic 3,3 V) hay Arduino (5 V), cần kiểm tra 4 thông số vàng trên datasheet: dải điện áp động cơ ($$V_M$$), dòng liên tục/đỉnh ($$I_{\text{rms}} / I_{\text{peak}}$$), ngưỡng logic đầu vào ($$V_{\text{IH}}$$), và tính năng bảo vệ quá nhiệt/quá dòng (như chân `STBY` trên TB6612 hoặc giới hạn dòng `AISEN/BISEN` trên DRV8833).

### Khung giải thích: Cầm tay so sánh sụt áp và nhiệt tỏa ra giữa L298N và TB6612FNG trên pin LiPo 2S (nên đọc chậm)

Giả sử robot dùng pin LiPo 2S (**$$V_{\text{bat}} = 7{,}4\text{ V}$$**) kéo **2 động cơ**, mỗi động cơ ăn dòng liên tục **$$I = 1{,}0\text{ A}$$** (tổng công suất cấp từ pin $$P_{\text{pin}} = 7{,}4 \times 2{,}0 = 14{,}8\text{ W}$$):

| Thông số đánh giá (ở $$I = 1{,}0\text{ A/kênh}$$) | Driver **L298N** (BJT, $$V_{\text{drop}} \approx 2{,}0\text{ V}$$) | Driver **TB6612FNG** (MOSFET, $$R_{\text{DS(on)}} \approx 0{,}5\,\Omega$$) | Chênh lệch thực tế |
| :--- | :---: | :---: | :--- |
| **Sụt áp trên mỗi cầu H** | $$2{,}0\text{ V}$$ | $$1{,}0 \times 0{,}5 = 0{,}5\text{ V}$$ | L298N mất áp gấp **4×** |
| **Điện áp thực đến động cơ** | $$7{,}4 - 2{,}0 = 5{,}4\text{ V}$$ | $$7{,}4 - 0{,}5 = 6{,}9\text{ V}$$ | TB6612 giúp xe chạy nhanh hơn **28%**! |
| **Nhiệt lãng phí (cả 2 kênh)** | $$2 \times (2{,}0 \times 1{,}0) = 4{,}0\text{ W}$$ | $$2 \times (1{,}0^2 \times 0{,}5) = 1{,}0\text{ W}$$ | L298N đốt nhiệt gấp **4×** |
| **Hiệu suất truyền điện của driver** | $$5{,}4 / 7{,}4 \approx 73{,}0\%$$ | $$6{,}9 / 7{,}4 \approx 93{,}2\%$$ | Tiết kiệm **20,2%** dung lượng pin! |

Bảng tính ngắn gọn này cho thấy rõ: L298N chỉ còn phù hợp làm mô hình học tập giá rẻ khi cấp nguồn 12 V; còn với mọi robot chạy pin 2S thực thụ, chuyển sang TB6612FNG hoặc DRV8833 là nâng cấp rẻ mà hiệu quả nhất bạn có thể làm!

## Mục tiêu học

Sau bài này, bạn nhận diện được module L298N, TB6612 và DRV8833 dựa trên vỏ chip, tản nhiệt và nhãn chân. Bạn giải thích được chức năng jumper 5 V trên L298N, thời điểm bắt buộc phải tháo jumper và lý do không dùng mạch ổn áp 7805 tích hợp để cấp nguồn cho ESP32. Bạn hiểu rõ vì sao phải kéo chân `STBY` của TB6612 lên mức cao và giới hạn sử dụng của DRV8833 trên pin 1S–2S dưới 10 V. Bạn cũng thực hiện được phép đo `VM` và đường nguồn logic bằng đồng hồ vạn năng trước khi nối bất kỳ chân GPIO nào.

## Kiến thức cần có

Bạn đã quen với thang đo điện áp một chiều trên đồng hồ vạn năng, nắm các khái niệm cầu H từ bài 05-01 (chiều tiến/lùi, trùng dẫn, PWM trên chân enable) và tuân thủ nguyên tắc không lấy nguồn động cơ từ USB.

## Vì sao bài này quan trọng với Capstone A và ROS

Capstone A sử dụng hai động cơ giảm tốc TT chạy nguồn pin 2S. Mạch cầu H quyết định bao nhiêu điện áp từ pin thực sự tới được động cơ và liệu mạch có hoạt động ổn định khi phát Wi-Fi hay không. Nếu nguồn logic bị sụt áp khiến ESP32 reset giữa chừng, các chân điều khiển có thể ở trạng thái không xác định và làm robot di chuyển ngoài ý muốn. Chọn TB6612 làm mặc định (và biết cách dùng an toàn nếu phải thay tạm bằng L298N) là bước chuẩn bị thiết yếu để lệnh `cmd_vel` ở tầng ROS sau này vận hành tin cậy.

## Nhận diện ba dòng module phổ biến

- **L298N:** bo mạch kích thước lớn (thường màu đỏ hoặc xanh), nổi bật với tấm tản nhiệt kim loại bắt vít trên vỏ chip công suất lớn và một jumper 5 V nằm gần IC ổn áp. Hàng cầu đấu vít (domino) nhận `VM`, `GND` và hai động cơ; hàng chân cắm logic gồm `IN1`, `IN2`, `ENA`, `IN3`, `IN4`, `ENB` cùng chân `5V`.
- **TB6612FNG:** module nhỏ gọn dùng cầu MOSFET của Toshiba, các chân chính gồm `VM`, `VCC`, `GND`, `AIN1`, `AIN2`, `PWMA`, `BIN1`, `BIN2`, `PWMB` và `STBY`. Vì sụt áp rất nhỏ nên mạch không cần tản nhiệt kim loại lớn.
- **DRV8833:** bo mạch breakout rất nhỏ dùng chip cầu kép của Texas Instruments, dải nguồn động cơ khoảng 2,7–10,6 V. Nhiều module chạy chế độ `IN/IN` (hai chân điều khiển mã hóa cả chiều lẫn PWM) và không có tản nhiệt lớn. Mạch phù hợp với động cơ cỡ nhỏ chạy pin 1S–2S, nhưng dòng stall của cặp động cơ TT thường vượt quá khả năng chịu tải liên tục của chip này.

## L298N và jumper 5 V

Tầng công suất của L298N là transistor Darlington lưỡng cực nên sụt khoảng 2 V khi có dòng chạy qua; toàn bộ phần điện áp sụt nhân với dòng điện chuyển thành nhiệt trên chip, đòi hỏi tấm tản nhiệt lớn. Phần logic của L298N yêu cầu nguồn 5 V.

Khi cắm jumper 5 V, IC ổn áp tuyến tính 7805 tích hợp lấy điện từ nguồn động cơ `VM` để tạo ra 5 V nuôi khối logic. Nếu `VM` vượt quá 12 V, 7805 sẽ tiêu tán công suất quá lớn và quá nhiệt — trường hợp này **bắt buộc rút jumper** và cấp 5 V từ nguồn ngoài. Ngay cả khi `VM` dưới 12 V, tuyệt đối không lấy chân 5 V của L298N để cấp nguồn cho ESP32: các xung dòng khi Wi-Fi phát sóng dễ làm sụt áp 7805, gây reset (brownout) cho ESP32. Hãy dùng một mạch hạ áp (buck) riêng cho vi điều khiển và nối chung mass với `VM`.

Tín hiệu GPIO 3,3 V thường vẫn đạt ngưỡng nhận mức cao của L298N (khoảng 2,3 V) miễn nguồn logic 5 V ổn định và đã nối chung mass.

## TB6612FNG — lựa chọn mặc định của Capstone A

Do sử dụng MOSFET, TB6612FNG có sụt áp rất thấp nên truyền gần trọn điện áp pin tới động cơ. Chân nguồn logic `VCC` chấp nhận dải rộng 2,7–5,5 V, có thể cấp trực tiếp từ đường 3,3 V của ESP32. Cực `VM` chịu tới khoảng 15 V (rất thoải mái cho pin 2S 7,4–8,4 V) với dòng liên tục khoảng 1,2 A mỗi kênh — phù hợp với động cơ TT nếu tránh để kẹt trục kéo dài.

Điểm dễ quên nhất trên TB6612 là chân `STBY` (Standby): chân này **bắt buộc phải kéo lên mức cao** (nối vào `VCC` hoặc điều khiển bằng một chân GPIO kéo cao trong `setup()`), nếu không cả hai cầu đều ở trạng thái ngủ và động cơ không quay dù mã nguồn hoàn toàn đúng.

## DRV8833 và các mạch cầu quá nhỏ

DRV8833 phù hợp cho các cơ cấu chấp hành nhỏ chạy 1S hoặc 2S có dòng stall thấp; tương tự `STBY` trên TB6612, nhiều bo DRV8833 có chân `SLEEP` cần kéo cao để kích hoạt. Với cặp động cơ TT của Capstone A, nên chọn TB6612 thay vì DRV8833.

Ngoài ra, các mạch giá rẻ như MX1508 hay L9110 thường xuất hiện chung trong kết quả tìm kiếm nhưng có khả năng chịu dòng và tản nhiệt quá nhỏ cho động cơ TT chạy pin 2S — một lần kẹt trục có thể làm hỏng chip ngay lập tức.

## Ví dụ tính tay

Giả sử nguồn động cơ `VM = 12 V` và vẫn cắm jumper 5 V trên L298N để nuôi ESP32 tiêu thụ trung bình $$0.20~\mathrm{A}$$ (thực tế xung dòng Wi-Fi còn cao hơn). Công suất tỏa nhiệt trên IC 7805 là:

$$
P_{7805} \approx (12 - 5) \times 0.20 = 1.4~\mathrm{W}
$$

Với vỏ IC nhỏ không có tản nhiệt đáng kể, 1,4 W dễ làm 7805 quá nhiệt, kéo sụt đường 5 V và khiến ESP32 tự reset. Nếu `VM > 12 V`, công suất tỏa nhiệt càng lớn hơn nên bắt buộc phải rút jumper. Bên cạnh đó, với dòng tải 1 A qua một kênh L298N (sụt áp khoảng 2 V), bản thân chip L298N đã tỏa khoảng $$2~\mathrm{W}$$ nhiệt trên mỗi kênh. Dùng TB6612 trên pin 2S giúp tránh cả hai nguồn sinh nhiệt này.

## Hình minh họa

![Module cầu H kép L298N với tản nhiệt bắt vít]({{ site.imgurl }}/wikimedia/Dosmotorsl298n.jpg)

Nhận diện nhanh L298N qua tấm tản nhiệt kim loại lớn, hàng cầu đấu vít cho `VM`/động cơ và jumper 5 V gần IC ổn áp.

![Đồng hồ số dùng để đo VM và ray logic trước khi nối bất kỳ GPIO nào]({{ site.imgurl }}/wikimedia/Digital_Multimeter_Aka.jpg)

Đặt que đen vào `GND` của driver, que đỏ đo lần lượt `VM` và chân nguồn logic (5 V hoặc 3,3 V) trước khi nối dây sang vi điều khiển.

## Lab

### An toàn

Ngắt nguồn động cơ khi đo thông mạch. Khi đo `VM`, đặt đồng hồ ở thang điện áp một chiều và cẩn thận không để đầu que trượt chạm giữa `VM` với chân logic. Không nối chân ESP32 trước khi xác minh xong hai đường nguồn; luôn nhấc bánh khỏi bàn nếu đã gắn động cơ.

### BOM

| Món | Vai trò |
|------|------|
| Module cầu H thực tế của bạn | Đối tượng nhận diện và đo kiểm |
| Đồng hồ vạn năng | Đo điện áp một chiều và thông mạch |
| Điện thoại | Chụp ảnh bo mạch để ghi chú nhãn chân |
| Bộ pin 2S hoặc nguồn bàn có giới hạn dòng *(tùy chọn)* | Cấp `VM` để đo kiểm |
| Sổ tay | Ghi danh sách chân và hai giá trị điện áp đo được |

### Các bước

1. Chụp rõ mặt trên và mặt dưới bo mạch, khoanh tròn mã chip in trên thân IC.
2. Ghi toàn bộ tên các cầu đấu vít và hàng chân cắm theo đúng nhãn in trên mạch (`VM`, `VCC`, `GND`, `ENA`, `STBY`, ...) vào `lab-notes.md`.
3. Nếu mạch có jumper 5 V, ghi rõ chức năng của jumper và xác định nên giữ hay rút đối với mức điện áp pin của bạn.
4. Cấp `VM` (chưa nối vi điều khiển), đo và ghi lại điện áp `VM` cùng đường nguồn logic.
5. Xác nhận vai trò của chân `STBY` (trên TB6612), jumper 5 V (trên L298N) hoặc chân `SLEEP`/`FAULT` (trên DRV8833).
6. Chỉ sau khi hoàn tất các bước trên mới nối nguồn logic, dây `GND` chung và các chân tín hiệu điều khiển.

### Kết quả mong đợi

Gọi đúng tên chip, có ảnh chụp gắn nhãn chân, có đủ hai giá trị điện áp đo được (`VM` và logic) và nêu đúng vai trò của `STBY` hoặc jumper 5 V (với DRV8833, nêu rõ dải 2,7–10,6 V và đánh giá mức tương thích với pin đang dùng).

### Lỗi thường gặp

| Hiện tượng | Cần kiểm tra |
|------------|--------------|
| Chân logic 5 V đo ra 0 V dù đã cắm jumper | Thiếu `VM`, cắm nhầm chân jumper hoặc hỏng IC 7805 |
| ESP32 tự reset khi bật Wi-Fi | Đang lấy nguồn từ 7805 của L298N; chuyển sang mạch buck riêng |
| Ngõ ra TB6612 không hoạt động | Chân `STBY` để thấp hoặc để nổi; kéo `STBY` lên cao |
| DRV8833 tự ngắt khi chạy động cơ TT | Dòng stall vượt ngưỡng bảo vệ quá dòng của chip; đổi driver phù hợp hơn |
| MX1508 nóng rát tay | Động cơ quá tải so với mạch; ngắt nguồn ngay |

## Mua ở Việt Nam

Chọn mua theo đúng mã chip đã xác định: ưu tiên TB6612 cho động cơ TT chạy 2S; L298N chấp nhận được cho bài thực hành cơ bản; DRV8833 chỉ dùng cho động cơ nhỏ. Giá tham khảo thay đổi theo thời điểm (L298N khoảng 35.000–70.000 VND, TB6612 khoảng 40.000–120.000 VND, DRV8833 khoảng 30.000–80.000 VND):

- Trang L298N đã kiểm tra, khoảng 45.000 VND: [hshop.vn/mach-dieu-khien-dong-co-dc-l298](https://hshop.vn/mach-dieu-khien-dong-co-dc-l298)
- HShop: [TB6612](https://hshop.vn/search?q=TB6612), [DRV8833](https://hshop.vn/search?q=DRV8833), [L298N](https://hshop.vn/search?q=L298N)
- Shopee: [TB6612](https://shopee.vn/search?keyword=TB6612), [DRV8833](https://shopee.vn/search?keyword=DRV8833)
- Lazada: [TB6612](https://www.lazada.vn/catalog/?q=TB6612), [DRV8833](https://www.lazada.vn/catalog/?q=DRV8833)
- Thế Giới IC: [TB6612](https://www.thegioiic.com/search?q=TB6612), [DRV8833](https://www.thegioiic.com/search?q=DRV8833)

## Video tham khảo

- **Xem trước:** [TB6612FNG H-Bridge Motor Controller - Better than L298N?](https://www.youtube.com/watch?v=JPPTRj0KWbg) — DroneBot Workshop, tiếng Anh. So sánh trực tiếp TB6612 và L298N về sụt áp, chân logic và chân `VM`.
- [What is an H-Bridge?](https://www.youtube.com/watch?v=3N_4VpzmKY0) — CircuitBread, tiếng Anh. Ôn lại nguyên lý cầu H bên trong cả hai dòng module.

## Bài tập

1. Một module có tấm tản nhiệt bắt vít và jumper 5 V, cấp nguồn động cơ từ pin 3S (12,6 V). Cần xử lý jumper thế nào và cấp nguồn cho ESP32 từ đâu?
2. Chương trình điều khiển TB6612 đã đặt đúng `AIN1`, `AIN2` và `PWMA` nhưng trục động cơ vẫn đứng yên. Chân nào cần kiểm tra đầu tiên?
3. Nguồn `VM` cấp vào bo DRV8833 đo được 11,1 V từ pin 3S. Mức áp này có nằm trong dải 2,7–10,6 V cho phép không?
4. Ở dòng 1 A, một kênh L298N sụt áp 2 V. Công suất chuyển thành nhiệt trên kênh đó là bao nhiêu watt?
5. Cửa hàng gợi ý dùng MX1508 cho robot hai động cơ TT chạy pin 2S. Bạn nên chọn mạch cầu H nào thay thế?

### Gợi ý đáp án

1. Rút jumper 5 V trên L298N (vì nguồn vượt 12 V) và cấp nguồn cho ESP32 từ mạch hạ áp (buck) riêng có nối chung mass.
2. Kiểm tra chân `STBY` và đảm bảo nó được kéo lên mức cao.
3. Không; 11,1 V vượt quá giới hạn trên 10,6 V của DRV8833 và có thể làm hỏng chip.
4. $$P = 2~\mathrm{V} \times 1~\mathrm{A} = 2~\mathrm{W}$$.
5. Chọn TB6612 (không dùng MX1508 hay L9110 cho cặp động cơ TT trên 2S).

## Đọc thêm

- Datasheet TI DRV8833 (dải `VM` và giao diện `IN/IN`): [https://www.ti.com/lit/ds/symlink/drv8833.pdf](https://www.ti.com/lit/ds/symlink/drv8833.pdf)
- Mạch mang TB6612FNG của Pololu (`STBY`, `VM` và dòng định mức): [https://www.pololu.com/product/713](https://www.pololu.com/product/713)
- Mạch mang DRV8833 của Pololu: [https://www.pololu.com/product/2130](https://www.pololu.com/product/2130)
- Datasheet ST L298: [https://www.st.com/resource/en/datasheet/l298.pdf](https://www.st.com/resource/en/datasheet/l298.pdf)
