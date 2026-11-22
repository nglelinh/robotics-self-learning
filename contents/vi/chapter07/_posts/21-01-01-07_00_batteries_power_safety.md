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

Thời lượng ước tính: **~100 phút**. Trong bài này, bánh xe chưa được phép quay. Bạn sẽ xác định rõ loại hóa học pin, chọn dòng cầu chì phù hợp và chốt sơ đồ dây nguồn trước khi chuyển sang bài lắp khung.

## Mục tiêu

Sau bài này, bạn phân biệt được pin Li-ion 18650, LiPo dạng túi (pouch) và LiFePO4 dựa trên điện áp danh định và điện áp sạc đầy, từ đó không sử dụng nhầm bộ sạc khác hóa học. Bạn biết cách tính dòng xả liên tục theo hệ số C trên nhãn nhưng không dùng con số này để thay thế cho dòng đo thực tế khi chọn cầu chì. Bạn bố trí đúng vị trí cầu chì trên nhánh cực dương, chỉnh mạch hạ áp (buck) về 5,0 V trước khi kết nối ESP32, và vẽ hoàn chỉnh cây nguồn gồm: pin, công tắc, cầu chì, nhánh VM, mạch buck và điểm mass chung.

## Kiến thức cần trước

Bài an toàn ở Chương 00 đã nghiêm cấm việc gắn mạch sạc TP4056 lên đế pin 2S và quy định thứ tự đấu nối: mass, nguồn logic, tín hiệu, rồi mới tới VM. Định luật Ohm ở Chương 01 đủ để tính sụt áp trên dây dẫn, và bạn cần biết đo điện áp một chiều bằng đồng hồ vạn năng. Chưa cần firmware teleop; nếu chưa có cell pin trên bàn, bạn vẫn hoàn thành đầy đủ phần tính toán trên giấy và ghi `chưa có pin` vào các ô đo thực tế.

## Vì sao bài này nằm trên lộ trình

Các lỗi thường gặp nhất khiến Capstone A ngừng hoạt động đều bắt nguồn từ hệ thống nguồn: vi điều khiển tự reset ngay khi động cơ khởi động, cầu chì lắp sai nhánh nên không ngắt khi chập pin, hoặc dùng bộ sạc 4,2 V/cell cho pin LiFePO4. Bộ điều khiển PID hay lệnh `cmd_vel` không thể cứu một cell pin bị phồng. Bài lắp khung ngay sau đây giả định rằng nhánh cực dương đã đi qua công tắc và cầu chì, đầu ra buck đã được chỉnh đúng 5,0 V và toàn bộ mass đã gom về một nút chung. ROS 2 chỉ gửi ý định chuyển động, còn năng lượng và dòng ngắn mạch nằm trực tiếp ở khối pin.

![Cây nguồn: pin, công tắc, chì, rồi tách VM và buck]({{ site.imgurl }}/generated/ch07_battery_wiring.png)

## Khái niệm

Ba loại hóa học pin phổ biến trên robot cỡ nhỏ có mức điện áp sạc đầy khác nhau:

| Hóa học | Danh định một cell | Đầy (khoảng) | Pack 2S danh định | Pack 2S đầy | Sạc |
| --- | --- | --- | --- | --- | --- |
| Li-ion 18650 | 3,6–3,7 V | 4,20 V | 7,2–7,4 V | 8,40 V | Từng cell tới 4,20 V, hoặc sạc 2S có cân bằng |
| LiPo pouch | 3,7 V | 4,20 V | 7,4 V | 8,40 V | Sạc cân bằng đúng số cell, không phải sạc 18650 một ngăn |
| LiFePO4 | 3,2 V | khoảng 3,60–3,65 V | 6,4 V | khoảng 7,3 V | Sạc LiFePO4. Cấm hồ sơ 4,20 V/cell |

Pin LiPo và Li-ion 18650 có cùng mức điện áp đầy 4,20 V mỗi cell nhưng khác nhau về vỏ bảo vệ: túi mềm của LiPo rất dễ bị thủng và bốc cháy, trong khi cell trụ kim loại khó bị đâm thủng hơn nhưng vẫn cháy nếu hư hại vỏ. Riêng LiFePO4 không thể sạc chung bằng bộ sạc LiPo/Li-ion dù an toàn nhiệt hơn, vì điện áp đầy của nó thấp hơn khoảng 0,55 V mỗi cell; dùng bộ sạc ngắt ở 4,20 V sẽ đẩy LiFePO4 vào vùng quá áp nguy hiểm.

Hệ số C là thông số nhà sản xuất công bố: dòng xả liên tục danh định bằng C nhân với dung lượng tính theo ampe-giờ (Ah):

$$
I_{\text{C}} = C \times \frac{Q_{\mathrm{mAh}}}{1000}
$$

Ví dụ, một cell 18650 ghi 2500 mAh và 10C có $I_{\text{C}} = 10 \times 2{,}5 = 25$ A. Đây là mức dòng xả khả dụng theo nhãn, tuyệt đối không phải lý do để bỏ cầu chì. Hai động cơ TT không bao giờ cần tới 25 A, nhưng nếu tua-vít vô tình làm chập cực pin, cell vẫn có thể phóng ra dòng lớn ngay tức thì. Cầu chì cần thiết chính vì pin có khả năng cấp dòng ngắn mạch cao.

Dung lượng thực của cell 18650 hiếm khi vượt quá khoảng 3500 mAh; những nhãn in 9900 mAh là thông số ảo, như đã cảnh báo trong bài mua sắm ở Chương 00.

Mạch BMS (quản lý và thường có chức năng cân bằng pin) nằm giữa các cell và hai cực đầu ra của pack, có nhiệm vụ ngắt khi xảy ra quá áp, dưới áp hoặc quá dòng theo ngưỡng thiết kế của mạch. Tuy nhiên, BMS không thay thế cho cầu chì chọn theo tiết diện dây và không thay thế công tắc ngắt nguồn đặt trong tầm tay. Nếu một pack pin giá rẻ quảng cáo “có mạch bảo vệ” nhưng bạn không quan sát thấy bảng mạch thực tế, hãy coi như pack đó chưa có bảo vệ.

Mạch hạ áp (buck converter) dùng trong khóa học thường là loại dựa trên IC LM2596, yêu cầu điện áp đầu vào cao hơn điện áp đầu ra. Bạn phải chỉnh biến trở cho đến khi đồng hồ đo được đúng 5,0 V ở đầu ra **khi chưa cắm ESP32**. Các module quảng cáo dòng 3 A thường nóng nhanh và sụt áp trước khi đạt 3 A liên tục; chúng phù hợp để cấp nguồn cho ESP32 và một vài cảm biến nhỏ, tuyệt đối không cấp nguồn cho hai động cơ qua mạch buck.

Cầu chì phải lắp trên nhánh cực dương, ngay sau công tắc nguồn và trước điểm rẽ sang VM của driver và đầu vào mạch buck. Dòng định mức của cầu chì cần cao hơn dòng vận hành thực tế nhưng thấp hơn ngưỡng gây cháy đoạn dây nhỏ nhất trong mạch.

Để ước lượng ban đầu, hãy đo dòng tiêu thụ thực tế của cả xe khi hai động cơ chạy trên sàn không bị kẹt, gọi là $I_{\mathrm{run}}$. Cầu chì tác động chậm có định mức khoảng $1{,}5$ đến $2$ lần $I_{\mathrm{run}}$ sẽ chịu được xung dòng khởi động. Với hai động cơ TT chạy nguồn 2S trong khóa học này, mức cầu chì thường chốt ở **2 A hoặc 3 A** sau khi đã đo thực tế (khớp với checklist Chương 07). Nếu $I_{\mathrm{run}}$ đo được đã lên tới 2,5 A thì không nên gắn cầu chì 2 A rồi đổ lỗi cho động cơ hỏng khi đứt chì; hãy đo kiểm lại trước khi đổi cỡ cầu chì hoặc điều chỉnh chế độ chạy.

Dây cắm Dupont chỉ dùng cho tín hiệu điều khiển. Dòng điện cấp cho động cơ phải đi qua dây đồng mềm đủ tiết diện, bắt trực tiếp vào cầu đấu vít trên mạch driver. Độ sụt áp trên dây dẫn tuân theo:

$$
\Delta V = I R_{\mathrm{dây}}
$$

Một đoạn dây dài và mỏng có điện trở cỡ vài phần mười ôm khi mang dòng 2 A sẽ sụt vài phần mười vôn và nóng cục bộ. Nếu thấy dây dẫn ấm lên dù động cơ mới chạy không tải, hãy dừng ngay và thay dây tiết diện lớn hơn, không quấn thêm băng dính để che.

Quy tắc sạc và bảo quản pin:

- Luôn sạc pin ở nơi dễ quan sát, không sạc trên giường hoặc đặt dưới nắng trong ô tô.
- Bảo quản và sạc pin LiPo bên trong túi chống cháy; không đâm thủng hoặc gấp gập túi cell.
- Khi cất giữ lâu ngày, không để pin ở trạng thái đầy 100%: giữ Li-ion/LiPo ở khoảng 3,7–3,8 V mỗi cell và LiFePO4 ở khoảng 3,3 V mỗi cell (đây là điện áp bảo quản, không phải ngưỡng xả kiệt dưới tải).
- Không bao giờ sạc lại cell bị phồng, thủng vỏ, sụt dưới khoảng 2,5 V (với Li-ion) hoặc tự nóng khi không tải; hãy mang đến điểm thu gom tái chế pin và không để chung với chìa khóa hay vật kim loại.
- Luôn rút sạc trước khi rời khỏi nhà; BMS không thể thay thế sự giám sát của con người.

## Ví dụ tính

Xét pack LiPo 2S có dung lượng 2200 mAh và nhãn 25C. Dòng xả liên tục theo nhãn là:

$$
I_{\text{C}} = 25 \times 2{,}2 = 55~\mathrm{A}
$$

Xe đo được $I_{\mathrm{run}} = 0{,}8$ A khi chạy thẳng chậm và xung dòng kẹt ngắn khoảng 2 A. Khi đó, cầu chì 2 A hoặc 3 A là lựa chọn hợp lý: cao hơn dòng chạy 0,8 A, thấp hơn nhiều so với 55 A và bảo vệ tốt gần ngưỡng dòng kẹt. Thông số 25C không phải lý do để lắp cầu chì 50 A — nếu làm vậy, dây dẫn sẽ cháy trước khi cầu chì kịp ngắt.

Với mạch buck: giả sử điện áp pin đo không tải là 8,1 V. Khi ESP32 vẫn để rời bên ngoài, bạn vặn biến trở cho đến khi đồng hồ trên hai cực ra báo 5,02 V rồi mới cấp vào phần logic. Nếu cắm ESP32 trước khi chỉnh, điện áp đầu ra ban đầu có thể đang ở mức 8 V và làm hỏng mạch ngay lập tức.

Với pack LiFePO4 2S: điện áp đầy xấp xỉ $3{,}65 \times 2 = 7{,}3$ V, vẫn đủ nằm trong dải hoạt động 3–9 V của động cơ TT. Một bộ sạc dừng ở 8,4 V là bộ sạc sai hóa học; cần ghi rõ điều này vào sổ trước khi cắm giắc.

## Lab

### An toàn

Không cấp tín hiệu PWM trong bài này và không đặt bánh xe chạm bàn nếu đã nối nguồn VM. Không sạc bất kỳ cell pin nào nếu chưa xác định chắc chắn hóa học pin. Đeo kính bảo hộ khi cắt dây và tháo nhẫn kim loại khi thao tác gần cực pin trần.

### BOM

| Món | Việc | Giá |
| --- | --- | --- |
| Đồng hồ | Điện áp cell, đầu ra buck | Đã có từ chương 00, hoặc để trống đến khi bạn mua |
| Pin bạn sẽ dùng (18650, LiPo hoặc LiFePO4) | Nguồn VM | Điền khi mở listing. Đừng chép tem dung lượng |
| Công tắc và cầu chì 2 A và 3 A | Ngắt được bằng tay, và ngắt khi chập | Điền khi mở listing |
| Module buck hạ áp | 5,0 V cho logic | Điền khi mở listing |
| Túi LiPo nếu pack là túi mềm | Sạc và cất | Điền khi mở listing |

Các trang tìm kiếm tham khảo (giá thay đổi theo thời điểm): [Hshop, từ khóa lipo](https://hshop.vn/search?q=lipo), [Shopee](https://shopee.vn/), [Lazada](https://www.lazada.vn/). Liên kết sản phẩm cell 18650 và bộ sạc khay đã có trong [bài BOM]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %}) (ghi nhận ngày 23 tháng 9 năm 2026); hãy mở lại trang đó để kiểm tra trước khi đặt mua.

### Các bước

1. Ghi rõ một dòng hóa học pin bạn dùng (18650, LiPo hoặc LiFePO4) kèm mức điện áp sạc đầy tối đa cho phép. Nếu chưa có pin, ghi loại dự định mua và hoàn thành phần giấy.
2. Đo điện áp hở mạch của từng cell hoặc từng dây cân bằng tiếp cận được. Cell 18650 hoặc LiPo đơn cần nằm trong khoảng 3,4 V đến 4,20 V trước khi lắp vào đế; nếu dưới khoảng 2,5 V, tuyệt đối không sạc.
3. Vẽ sơ đồ cây nguồn vào `lab-notes.md` với đủ bảy khối như hình minh họa: pin, công tắc, cầu chì, nhánh VM, mạch buck, ESP32 và mass chung. Đánh dấu rõ vùng cấm: cực dương pin không được nối trực tiếp vào chân 5 V hay 3,3 V của vi điều khiển.
4. Nếu đã có pin và mạch buck: đảm bảo bánh xe được nhấc khỏi bàn (hoặc chưa gắn động cơ). Cấp nguồn pin qua công tắc và cầu chì, vặn biến trở mạch buck đến 5,0 V ± 0,05 V và chụp ảnh màn hình đồng hồ trước khi nghĩ đến việc cắm ESP32.
5. Tính $I_{\text{C}}$ từ nhãn pin (nếu có) và ghi rõ một câu khẳng định không dùng con số này để chọn cầu chì. Ghi cỡ cầu chì sẽ lắp (2 A hoặc 3 A) cùng giá trị $I_{\mathrm{run}}$ đã đo (hoặc ghi `chưa đo`).

### Kết quả mong đợi

Sổ tay `lab-notes.md` ghi đầy đủ tên hóa học pin, ngưỡng điện áp đầy cho phép, số đo hoặc ảnh đồng hồ đầu ra buck 5,0 V (hoặc ghi chú chưa có buck), sơ đồ cây nguồn đủ bảy khối và câu xác nhận không chọn cầu chì theo $I_{\text{C}}$.

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

- **Xem trước:** [BMS (Battery Management System) || DIY or Buy || Properly protecting Li-Ion/Li-Po Battery Packs](https://www.youtube.com/watch?v=rT-1gvkFj60) — GreatScott!, tiếng Anh. Giải thích cách BMS bảo vệ pack pin lithium trước quá áp, dưới áp và quá dòng; lưu ý không bỏ BMS cũng không dùng BMS thay cầu chì.
- [LiPo C Rating Explained – No, a Higher C Rating Won't Hurt Your ESC or Motor](https://www.youtube.com/watch?v=4qIYyaRKGVE) — RcHelpDotCom, tiếng Anh. Giải thích ý nghĩa hệ số C trên nhãn LiPo — thông số này không dùng làm cỡ cầu chì.
- [Buck Converter](https://www.youtube.com/watch?v=rfChSvb8FX0) — The Organic Chemistry Tutor, tiếng Anh. Nguyên lý mạch hạ áp buck xuống 5 V; luôn chỉnh điện áp ra trước khi nối ESP32.

Video ngắn (Facebook Reel) dưới đây của Hoàng Quân (Cơ điện tử ICTU, [chinbi.com](https://chinbi.com)):

- [Test pin drone, ESC cháy](https://www.facebook.com/reel/931720623225817) — Chú thích: dùng pin xe nâng nặng 3 tạ để test drone, phần test cháy ESC khi pin chưa hết, cảm ơn PKG Battery. Minh họa thực tế việc pack pin công suất lớn có thể đốt cháy mạch công suất rất nhanh nếu không tính trước cầu chì và dòng liên tục.

## Bài tập

1. Nhãn một pack LiPo 3S ghi 1500 mAh, 30C. Tính $I_{\text{C}}$, và giải thích vì sao xe hai động cơ TT vẫn không lắp cầu chì 40 A.
2. Hai cell 18650 đo được 4,18 V và 3,71 V. Bạn có được lắp ngay hai cell này vào đế nối tiếp 2S để chạy không? Cần sạc như thế nào?
3. Mạch buck đo được 5,0 V khi không tải nhưng sụt xuống 4,6 V ngay khi ESP32 bật Wi-Fi. Việc đầu tiên cần kiểm tra hoặc xử lý là gì?
4. Vì sao mass của mạch buck, mạch driver và ESP32 phải nối thành một nút chung trước khi cấp tín hiệu PWM?
5. Một pack LiFePO4 4S đầy ở khoảng bao nhiêu vôn nếu mỗi cell đầy là 3,65 V? Có dùng được bộ sạc 4S Li-ion (16,8 V) không?

### Gợi ý đáp án

1. $I_{\text{C}} = 30 \times 1{,}5 = 45$ A. Cầu chì dùng để bảo vệ dây dẫn và an toàn người dùng, không chọn theo dòng xả tối đa trên nhãn; dòng cầu chì phải bám theo $I_{\mathrm{run}}$ đo thực tế.
2. Không được lắp nối tiếp khi hai cell lệch nhau gần 0,5 V. Cần sạc riêng từng cell lên khoảng 4,20 V, đo lại để xác nhận cân bằng rồi mới lắp vào đế.
3. Mạch buck không đáp ứng nổi dòng đỉnh (hoặc dây nguồn quá mảnh gây sụt áp). Cần giảm tải, kiểm tra dây hoặc đổi module buck tốt hơn; tuyệt đối không vặn tăng lên 5,5 V lúc không tải để “bù”.
4. Dòng điện động cơ phải có đường hồi về nguồn ổn định; nếu không nối chung mass, dòng điện hoặc nhiễu có thể tìm đường hồi qua các chân GPIO làm hỏng vi điều khiển.
5. Điện áp đầy khoảng $4 \times 3{,}65 = 14{,}6$ V. Không được dùng bộ sạc 16,8 V vì đó là hồ sơ 4,20 V/cell dành cho Li-ion.

## Đọc thêm

- [Battery University, BU-409, sạc lithium-ion](https://www.batteryuniversity.com/article/bu-409-charging-lithium-ion)
- [Battery University, BU-205, các họ lithium-ion](https://www.batteryuniversity.com/article/bu-205-types-of-lithium-ion)
- [Battery University, BU-409b, sạc LiFePO4](https://www.batteryuniversity.com/article/bu-409b-charging-lithium-iron-phosphate)
- [Bài an toàn chương 00]({% multilang_post_url contents/chapter00/00_03_safety_mindset_lab %})
- [BOM chương 00]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %})
