---
layout: post
title: "Pin, nguồn và an toàn trước khi lắp Capstone"
chapter: "07"
order: 0
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter07
lesson_type: required
draft: false
---

Thời lượng: **~100 phút**. Bánh chưa được phép quay. Bài này chốt hóa học của pin, dòng cầu chì, và sơ đồ dây trước bài lắp khung.

## Mục tiêu

Bạn phân biệt được Li-ion 18650, LiPo pouch và LiFePO4 bằng điện áp danh định và điện áp đầy, rồi từ chối cục sạc không cùng hóa học. Bạn tính dòng liên tục mà hệ số C tuyên bố, và bạn không dùng con số đó thay cho dòng đã đo. Bạn chọn cầu chì trên cực dương, chỉnh buck về 5,0 V trước khi có ESP32, và vẽ lại cây nguồn: pin, công tắc, chì, VM, buck, mass chung.

## Kiến thức cần trước

Bài an toàn chương 00 đã cấm kẹp TP4056 lên đế 2S và đã đặt thứ tự mass, logic, tín hiệu, VM. Định luật Ohm ở chương 01 đủ để đổi sụt áp trên dây thành dòng. Bạn đọc được điện áp một chiều. Chưa cần firmware teleop. Nếu cell chưa có trên bàn, bạn vẫn làm hết phần giấy và ghi `chưa có pin` vào chỗ lẽ ra là số đo.

## Vì sao bài này nằm trên lộ trình

Capstone A chết theo những kiểu nguồn nhàm: MCU reset khi motor khởi động, cầu chì nằm sai nhánh nên chập pin không bao giờ đứt, hoặc sạc 4,2 V/cell áp lên LiFePO4. PID và `cmd_vel` không sửa một cell phồng. Bài lắp khung ngay sau bài này giả định cực dương đã đi qua công tắc và chì, buck đã là 5,0 V, và mass là một nút. ROS 2 chỉ xuất bản ý định. Dòng ngắn mạch thì pin tự cung cấp.

![Cây nguồn: pin, công tắc, chì, rồi tách VM và buck]({{ site.imgurl }}/generated/ch07_battery_wiring.png)

## Khái niệm

Ba hóa học hay gặp trên robot nhỏ không dùng chung một số "pin đầy".

| Hóa học | Danh định một cell | Đầy (khoảng) | Pack 2S danh định | Pack 2S đầy | Sạc |
| --- | --- | --- | --- | --- | --- |
| Li-ion 18650 | 3,6–3,7 V | 4,20 V | 7,2–7,4 V | 8,40 V | Từng cell tới 4,20 V, hoặc sạc 2S có cân bằng |
| LiPo pouch | 3,7 V | 4,20 V | 7,4 V | 8,40 V | Sạc cân bằng đúng số cell, không phải sạc 18650 một ngăn |
| LiFePO4 | 3,2 V | khoảng 3,60–3,65 V | 6,4 V | khoảng 7,3 V | Sạc LiFePO4. Cấm hồ sơ 4,20 V/cell |

LiPo và Li-ion 18650 cùng họ điện áp 4,20 V khi đầy. Vỏ khác nhau: túi mềm thủng là cháy, cell trụ thủng cũng cháy nhưng khó chọc hơn. LiFePO4 không phải "LiPo an toàn hơn nên sạc chung cục". Điện áp đầy thấp hơn khoảng nửa vôn mỗi cell. Cục sạc dừng ở 4,20 V sẽ đẩy LiFePO4 qua vùng nó không được thiết kế để ở đó.

Hệ số C là tuyên bố của nhà sản xuất: dòng xả liên tục bằng C nhân dung lượng tính bằng ampe, khi dung lượng đổi ra ampe-giờ.

$$
I_{\text{C}} = C \times \frac{Q_{\mathrm{mAh}}}{1000}
$$

Cell 18650 ghi 2500 mAh và "10C" thì $I_{\text{C}} = 10 \times 2{,}5 = 25$ A. Đó là tuyên bố trên tem, không phải giấy phép bỏ cầu chì. Hai motor TT không bao giờ cần 25 A. Chập tua-vít thì cell có thể cố đưa một phần dòng đó ra trong khoảnh khắc. Cầu chì tồn tại vì hệ số C lớn.

Dung lượng 18650 thật hiếm khi quá khoảng 3500 mAh. Tem 9900 mAh là tem. Bài mua sắm chương 00 đã nói điều này. Bài này không nới quy tắc.

BMS (mạch bảo vệ và thường là cân bằng) ngồi giữa các cell và cực ra của pack. Nó cắt khi một cell quá áp, dưới áp, hoặc dòng quá lớn theo ngưỡng của chính board đó. BMS không thay cầu chì bạn chọn theo dây, và không thay công tắc trong tầm tay. Pack rẻ ghi "có bảo vệ" mà bạn không thấy mạch thì coi như không có, cho đến khi bạn nhìn thấy board.

Buck trong khóa này là module hạ áp, thường gặp hàng kiểu LM2596. Điện áp vào phải cao hơn điện áp ra. Bạn vặn biến trở đến khi đồng hồ đọc 5,0 V trên đầu ra, **trong khi ESP32 chưa cắm**. Module quảng cáo 3 A thường nóng và sụt trước khi tới 3 A liên tục. ESP32 cộng một cảm biến là tải hợp lý. Hai motor không đi qua buck.

Cầu chì đặt trên cực dương, sau công tắc, trước chỗ tách nhánh VM và buck. Dòng định mức ngồi trên dòng chạy đã đo và dưới dòng làm cháy dây nhỏ nhất.

Một ước lượng để bắt đầu, chưa phải chữ ký: đo dòng chạy của cả xe (hai motor trên sàn, không kẹt). Gọi số đó $I_{\mathrm{run}}$. Cầu chì chậm khoảng $1{,}5$ đến $2$ lần $I_{\mathrm{run}}$ sẽ chịu dòng khởi động. Hai motor TT trên 2S trong khóa này thường được chốt ở cầu chì **2 A hoặc 3 A** sau khi bạn đã đo, đúng như checklist chương 07. Nếu $I_{\mathrm{run}}$ đã là 2,5 A, đừng vẫn gắn chì 2 A rồi gọi motor là hỏng vì chì nổ. Đo lại, rồi mới đổi chì hoặc đổi cách chạy.

Dây Dupont là dây tín hiệu. Dòng motor đi dây mềm đủ tiết diện, vào vít của driver. Sụt trên dây:

$$
\Delta V = I R_{\mathrm{dây}}
$$

Một mét dây mỏng, $R$ cỡ vài phần mười ôm, ở 2 A đã ăn vài phần mười vôn và nóng cục bộ. Nếu dây nóng trong khi motor chỉ chạy không tải, dừng và tăng tiết diện. Đừng bọc thêm băng.

Sạc và cất:

- Sạc ở nơi bạn nhìn thấy cell, không trên giường, không trong nắng kính xe.
- LiPo để trong túi chống cháy khi sạc và khi cất. Không chọc, không gấp túi.
- Cất lâu ở trạng thái không đầy: Li-ion và LiPo khoảng 3,7–3,8 V mỗi cell. LiFePO4 khoảng 3,3 V mỗi cell. Số này là vùng cất, không phải ngưỡng cắt dưới tải.
- Cell phồng, thủng, dưới khoảng 2,5 V với Li-ion, hoặc nóng khi không tải: không sạc. Đem điểm tái chế pin. Không bỏ vào túi cùng chìa khóa.
- Ngắt sạc khi rời nhà. BMS không phải người trông.

## Ví dụ tính

Pack LiPo 2S ghi 2200 mAh, tem 25C. Tuyên bố liên tục:

$$
I_{\text{C}} = 25 \times 2{,}2 = 55~\mathrm{A}
$$

Xe đo được $I_{\mathrm{run}} = 0{,}8$ A khi đi thẳng chậm, và một xung kẹt ngắn khoảng 2 A. Cầu chì 2 A hoặc 3 A nằm đúng vùng: trên 0,8 A, dưới 55 A, và gần dòng kẹt. Tem 25C không kéo bạn lên cầu chì 50 A. Dây của bạn sẽ là cầu chì, theo cách xấu.

Buck: pin nghỉ 8,1 V. Bạn vặn module, đồng hồ trên hai cực ra đọc 5,02 V, ESP32 vẫn nằm trong túi. Sau đó mới cắm logic. Nếu bạn cắm ESP32 trước rồi mới vặn, biến trở có thể đang ở 8 V.

LiFePO4 2S đầy khoảng $3{,}65 \times 2 = 7{,}3$ V. Motor TT ghi 3–9 V vẫn quay. Cục sạc dừng ở 8,4 V là cục sạc sai hóa học. Viết câu đó vào sổ trước khi cắm giắc.

## Lab

### An toàn

Không có PWM. Không có bánh trên mặt bàn nếu VM đã nối. Không sạc cell bạn không gọi được tên hóa học. Kính nếu bạn cắt dây. Một tay không đeo nhẫn khi làm việc cạnh pack trần.

### BOM

| Món | Việc | Giá |
| --- | --- | --- |
| Đồng hồ | Điện áp cell, đầu ra buck | Đã có từ chương 00, hoặc để trống đến khi bạn mua |
| Pin bạn sẽ dùng (18650, LiPo hoặc LiFePO4) | Nguồn VM | Điền khi mở listing. Đừng chép tem dung lượng |
| Công tắc và cầu chì 2 A và 3 A | Ngắt được bằng tay, và ngắt khi chập | Điền khi mở listing |
| Module buck hạ áp | 5,0 V cho logic | Điền khi mở listing |
| Túi LiPo nếu pack là túi mềm | Sạc và cất | Điền khi mở listing |

Trang tìm, không phải giá: [Hshop, từ khóa lipo](https://hshop.vn/search?q=lipo), [Shopee](https://shopee.vn/), [Lazada](https://www.lazada.vn/). Cell 18650 và sạc khay đã có link sản phẩm trong [bài BOM]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %}), snapshot ngày 23 tháng 9 năm 2026. Mở lại trang đó trước khi trả tiền.

### Các bước

1. Viết một dòng hóa học: 18650, LiPo, hoặc LiFePO4. Ghi điện áp đầy bạn được phép thấy. Nếu chưa có pin, ghi hóa học bạn định mua và dừng ở bước giấy.
2. Với từng cell hoặc từng dây cân bằng bạn với tới, đo điện áp hở. 18650 hoặc LiPo một cell phải nằm khoảng 3,4 V đến 4,20 V trước khi vào đế. Dưới khoảng 2,5 V: không sạc.
3. Vẽ sơ đồ vào `lab-notes.md` cùng các hộp của hình: pin, công tắc, chì, VM, buck, ESP32, mass chung. Đánh dấu chỗ cấm: cực dương pin không vào chân 5 V hoặc 3,3 V.
4. Nếu đã có buck và pin: bánh nhấc hoặc motor chưa gắn. Cấp pin qua chì. Vặn buck tới 5,0 V ± 0,05 V. Chụp đồng hồ. Rồi mới được nghĩ tới ESP32.
5. Tính $I_{\text{C}}$ từ tem nếu có tem. Viết một câu: dòng đó không phải dòng cầu chì. Ghi dòng chì bạn sẽ gắn (2 A hoặc 3 A) và $I_{\mathrm{run}}$ nếu bạn đo được, hoặc `chưa đo`.

### Kết quả mong đợi

Sổ có tên hóa học, điện áp đầy cho phép, ảnh hoặc số buck 5,0 V (hoặc câu chưa có buck), sơ đồ đủ bảy hộp, và câu từ chối dùng $I_{\text{C}}$ làm cầu chì.

### Lỗi thường gặp

| Bạn thấy | Cần kiểm |
| --- | --- |
| Buck ra hơn 6 V lúc ESP32 đã cắm | Bạn đã vặn khi có tải logic, hoặc biến trở chưa khóa. Rút ESP32, đặt lại 5,0 V |
| ESP32 reset đúng lúc motor kéo | Motor và logic chung một nguồn yếu, hoặc mass không chung, hoặc dây motor đi qua breadboard |
| TP4056 trên đế 2S | Tháo. Sạc từng cell 18650. LiPo 2S cần sạc cân bằng |
| LiFePO4 báo đầy ở 8,4 V | Sai hồ sơ sạc. Ngừng. Tìm sạc ghi LiFePO4 |
| Chì 2 A nổ khi chưa kẹt bánh | $I_{\mathrm{run}}$ đã cao hơn mức chì, hoặc chập VM xuống mass phía sau chì. Đo dòng, đừng tăng chì trước khi tìm chập |
| Cell nóng trên bàn, không tải | Ngừng. Không sạc. Có thể chập trong hoặc BMS hỏng |


## Video tham khảo

- **Xem trước:** [BMS (Battery Management System) || DIY or Buy || Properly protecting Li-Ion/Li-Po Battery Packs](https://www.youtube.com/watch?v=rT-1gvkFj60) — GreatScott!, tiếng Anh. BMS bảo vệ pack lithium: quá áp, dưới áp, quá dòng. Không thay cầu chì bằng cách bỏ BMS.
- [LiPo C Rating Explained – No, a Higher C Rating Won't Hurt Your ESC or Motor](https://www.youtube.com/watch?v=4qIYyaRKGVE) — RcHelpDotCom, tiếng Anh. Chữ C trên tem LiPo là dòng xả ghi trên nhãn. Bài này không lấy số đó làm cỡ cầu chì.
- [Buck Converter](https://www.youtube.com/watch?v=rfChSvb8FX0) — The Organic Chemistry Tutor, tiếng Anh. Buck hạ áp xuống 5 V. Đặt điện áp ra trước khi nối ESP32, đúng thứ tự lab.

Reel Chinbi là Facebook Reel ngắn của Hoàng Quân (Cơ điện tử ICTU, [chinbi.com](https://chinbi.com)). Câu sau link chỉ nhắc caption.

- [Test pin drone, ESC cháy](https://www.facebook.com/reel/931720623225817). Chú thích: dùng pin xe nâng nặng 3 tạ để test drone, phần test cháy ESC khi pin chưa hết, cảm ơn PKG Battery. Pack lớn không hết trước khi ESC cháy. Cầu chì và dòng liên tục tính trước khi nối pack đó.

## Bài tập

1. Tem LiPo 3S ghi 1500 mAh, 30C. $I_{\text{C}}$ bằng bao nhiêu, và vì sao xe hai motor TT vẫn không dùng cầu chì 40 A?
2. Hai cell 18650 đo 4,18 V và 3,71 V. Bạn có được lắp vào đế nối tiếp và chạy không? Sạc thế nào?
3. Buck đọc 5,0 V khi không tải và 4,6 V khi ESP32 vừa kết nối Wi-Fi. Việc đầu tiên là gì?
4. Vì sao mass của buck, driver và ESP32 phải là một nút trước khi có tín hiệu PWM?
5. Pack LiFePO4 4S đầy khoảng bao nhiêu vôn nếu mỗi cell đầy ở 3,65 V? Cục sạc 4S Li-ion (16,8 V) có được dùng không?

### Gợi ý đáp án

1. $30 \times 1{,}5 = 45$ A. Cầu chì bảo vệ dây và người, không bảo vệ uy tín của tem. Dòng chì bám $I_{\mathrm{run}}$. 2. Không lắp để chạy khi hai cell lệch gần nửa vôn. Sạc riêng từng cell tới khoảng 4,20 V, đo lại, rồi mới vào đế. 3. Buck không theo nổi dòng. Giảm tải hoặc đổi module. Đừng "bù" bằng cách vặn lên 5,5 V lúc không tải. 4. Dòng motor trở về nguồn. Nếu mass chưa chung, nó có thể trở về qua chân GPIO. 5. $4 \times 3{,}65 = 14{,}6$ V. Cục 16,8 V là hồ sơ 4,20 V/cell, không dùng cho LiFePO4.

## Đọc thêm

- [Battery University, BU-409, sạc lithium-ion](https://www.batteryuniversity.com/article/bu-409-charging-lithium-ion)
- [Battery University, BU-205, các họ lithium-ion](https://www.batteryuniversity.com/article/bu-205-types-of-lithium-ion)
- [Battery University, BU-409b, sạc LiFePO4](https://www.batteryuniversity.com/article/bu-409b-charging-lithium-iron-phosphate)
- [Bài an toàn chương 00]({% multilang_post_url contents/chapter00/00_03_safety_mindset_lab %})
- [BOM chương 00]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %})
