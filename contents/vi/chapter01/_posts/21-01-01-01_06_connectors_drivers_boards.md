---
layout: post
title: "Giắc nối, driver động cơ và mạch vi điều khiển"
chapter: "01"
order: 6
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter01
lesson_type: required
draft: false
---

## Mục tiêu

Sau bài học này, bạn sẽ phân biệt rõ dây cắm Dupont bước 2,54 mm (chỉ dùng cho tín hiệu) với các loại giắc nối được phép mang dòng động cơ, đồng thời tránh ép nhầm vỏ JST-XH vào giắc servo hay XT30 vào XT60. Bạn sẽ tính được điện áp thực tế động cơ TT nhận từ bộ pin 7,4 V khi qua TB6612 so với L298N, và hiểu giới hạn của phương án thay thế DRV8833 (tối đa 1,5 A, nhanh nóng khi kẹt). Bạn cũng sẽ phân biệt được mạch phát triển ESP32 có sẵn USB với module WROOM trần, chỉ ra đúng chân VBUS và 3V3 trên Raspberry Pi Pico, và giải thích vì sao chân echo của HC-SR04 không được nối thẳng vào GPIO 3,3 V.

## Cần có gì trước

Bạn đã biết đo điện áp một chiều song song, nắm rõ dòng giới hạn của chân GPIO chỉ ở mức vài chục miliampe và biết động cơ TT kẹt trục tiêu thụ dòng lớn hơn nhiều. Bài này chưa điều khiển PWM động cơ mà dừng ở việc đọc ký hiệu IC, tên chân và tính toán sụt áp trước khi quay bánh xe đầu tiên.

---

Một chiếc xe robot có thuật toán PID tinh vi đến đâu cũng sẽ đâm sầm vào chân bàn nếu chỉ vì một sợi dây Dupont lỏng lẻo tuột khỏi chân driver khi xe chạy qua gờ gạch! Trong thực tế cơ điện tử, **giắc nối**, **mạch lái động cơ (motor driver)** và **bo vi điều khiển** là ba điểm giao tiếp cơ–điện dễ sinh lỗi nhất nhưng lại thường bị người mới coi nhẹ nhất.

## Bản đồ kiến thức nền: Giao diện Cơ–Điện, Mạch lái Cầu H và Ngưỡng Điện áp Bo mạch

1. **Chuẩn Bước chân Giắc nối (Pitch):** Đầu nối điện tử khác nhau ở từng phần trăm milimét — chuẩn header/Dupont là **2,54 mm** (0,1 inch), chuẩn JST-XH trên pin/bo mạch là **2,50 mm**, còn JST-PH nhỏ hơn là **2,00 mm**. Cố ép cắm chéo hai chuẩn sẽ làm cong chân và hỏng tiếp xúc!
2. **Nguyên lý Cầu H (H-Bridge):** Bốn công tắc bán dẫn bố trí hình chữ H quanh động cơ DC cho phép đảo chiều dòng điện (quay thuận/nghịch), phanh ngắn mạch (brake) hoặc thả trôi (coast), và điều tốc bằng xung PWM.
3. **Ranh giới Điện áp giữa Đường `VIN / 5V` và Chân Logic `3V3`:** Trên bo ESP32/Pico, chân `VIN`/`VBUS` đi qua ổn áp để tạo nguồn 3,3 V cho chip, nhưng các chân tín hiệu GPIO nối thẳng vào silicon 3,3 V — không chịu được điện áp 5 V!

### Ví dụ cầm tay chỉ việc: Tính độ lệch tích lũy khi cắm nhầm giắc JST-XH (2,50 mm) vào header 2,54 mm

Giả sử bạn cố cắm một đầu nối cái **JST-XH 10 chân** (bước chân $$2.50\text{ mm}$$) vào hàng chân rào **Dupont 10 chân** (bước chân $$2.54\text{ mm}$$):
- Mỗi khoảng chân lệch nhau $$2.54 - 2.50 = 0.04\text{ mm}$$.
- Qua 9 khoảng chân (từ chân 1 đến chân 10), tổng độ lệch tích lũy là:
  $$
  \Delta L = 9 \times 0.04\text{ mm} = \mathbf{0.36\text{ mm}}!
  $$
  Với độ dày chân kim loại chỉ $$0.64\text{ mm}$$, độ lệch $$0.36\text{ mm}$$ đủ làm cong gãy chân số 9–10 hoặc nứt vỏ nhựa! Tương tự, tính lại sụt áp trên pin $$7.4\text{ V}$$: qua **L298N** động cơ chỉ còn $$7.4 - 2.0 = \mathbf{5.4\text{ V}}$$ (mất 27% lực kéo), còn qua **TB6612FNG** động cơ giữ được $$7.4 - 0.5 = \mathbf{6.9\text{ V}}$$!

### Khung giải thích: 4 nguyên tắc chọn giắc nối và mạch lái bền bỉ cho xe robot (nên đọc chậm)

1. **Bước 1 — Dùng giắc có khóa gài (JST / XT30) cho mọi đường nguồn và động cơ:** Giắc Dupont chỉ dùng trên bàn thử nghiệm breadboard; khi xe chạy rung lắc, giắc có ngàm chống cắm ngược cực vừa chắc chắn vừa chống cháy mạch.
2. **Bước 2 — Luôn nối chung mass (`GND`) giữa bo MCU và mạch lái động cơ:** Hai nguồn riêng (pin động cơ và USB/Buck logic) *bắt buộc* phải nối chung một dây `GND` chuẩn tham chiếu, nếu không tín hiệu PWM sẽ bị "trôi" vô nghĩa.
3. **Bước 3 — Kiểm tra chân `STBY` (Standby) trên TB6612FNG:** Rất nhiều người lắp xong động cơ không quay chỉ vì quên kéo chân `STBY` lên mức `HIGH` (3,3 V)!
4. **Bước 4 — Ghi nhãn rõ điện áp trên từng cụm giắc:** Dán băng keo màu đánh dấu `7.4V BAT`, `5V BUCK`, `3.3V LOGIC` ngay trên khung xe để không bao giờ cắm nhầm khi tháo lắp nhanh.

**Kiểm tra nhanh.** Nếu hai động cơ trên xe có dòng làm việc mỗi chiếc $$0.6\text{ A}$$ và dòng hãm trục (khi kẹt bánh) là $$1.8\text{ A}$$, một kênh của TB6612FNG (dòng liên tục $$1.2\text{ A}$$, dòng đỉnh $$3.2\text{ A}$$) có đáp ứng an toàn không? **Có!** Cả dòng làm việc ($$0.6 < 1.2\text{ A}$$) lẫn dòng hãm ngắn hạn ($$1.8 < 3.2\text{ A}$$) đều nằm gọn trong giới hạn an toàn.

---

## Vì sao xe hai bánh thường hỏng ở giắc nối và mạch lái

Hệ thống xe đồ án gồm hai động cơ TT, một mạch lái TB6612, vi điều khiển ESP32 hoặc Pico chạy mức 3,3 V và cảm biến siêu âm HC-SR04. Dây cắm Dupont phù hợp để nối các chân điều khiển AIN1, AIN2, PWMA và STBY, nhưng không phù hợp để dẫn dòng kẹt động cơ vào chân VM — và càng không thể coi chân GPIO là nguồn VM.

Với bộ pin 2S danh định 7,4 V, cầu H MOSFET chỉ sụt vài phần mười vôn, còn L298N (dù có cùng giá bán tại thời điểm khảo sát) lại sụt tới khoảng 2 V khiến động cơ chạy ở vùng yếu. Bên cạnh đó, chân echo của HC-SR04 xuất mức 5 V trong khi chân GPIO của ESP32 và Pico không chịu được 5 V; chỉ cần thêm một mạch chuyển mức giá khoảng 10.000 ₫ là giải quyết triệt để. Toàn bộ các vấn đề này đều được phòng tránh bằng cách đọc kỹ nhãn in trên mạch trước khi cắm pin.

## Các họ giắc nối: bước chân không thể ép vừa

**Dây Dupont** (đầu cắm vuông đơn bước chân 2,54 mm) được thiết kế cho breadboard và đường tín hiệu logic nối vào TB6612. Do tiết diện lõi đồng mảnh và tiếp điểm nhỏ, dòng kẹt gần 1 A đi qua đầu bấm Dupont dễ gây nóng và làm sụt áp. Do đó, chỉ dùng Dupont cho tín hiệu; đường pin vào VM và đường ra động cơ cần dây tiết diện lớn hơn và được bắt chặt qua trạm vít hoặc hàn cố định.

**JST-XH** là chuẩn giắc có bước chân 2,50 mm (thường gặp ở dây sạc cân bằng và giắc pin nhỏ). Dù 2,50 mm gần giống 2,54 mm, việc cố ép cắm vào hàng chân 2,54 mm sẽ làm cong gãy chân. **Giắc servo kiểu JR** có ba chân bước 2,54 mm kèm gờ định hướng chống cắm ngược — tuyệt đối không gọt bỏ gờ này. Với dòng công suất lớn hơn, **XT30** và **XT60** dùng chân đồng dạng đạn và hoàn toàn không tương thích lẫn nhau hay với JST. Nếu hai đầu giắc không trượt vào nhẹ nhàng và khớp khít, hãy dừng ngay; cố dùng lực rất dễ làm đảo cực pin trên chân VM.

## So sánh sụt áp mạch lái ở nguồn 7,4 V

Cầu H chỉ đóng vai trò đóng cắt điều hướng dòng điện cho động cơ chứ không tự sinh ra dòng: vi điều khiển ra lệnh chọn chiều quay và PWM, còn nguồn pin nối vào chân VM mới là nơi cung cấp dòng điện.

![Vi điều khiển lái cầu; pin cấp dòng cho mô-tơ]({{ site.imgurl }}/generated/hbridge_concept.png)

**Module TB6612FNG** dùng cầu MOSFET. Theo thông số trên Hshop (ngày 23 tháng 9 năm 2026), mạch hỗ trợ VM từ 4,5 V đến 10 V, nguồn logic từ 2,7 V đến 5,5 V, dòng liên tục 1,2 A và dòng đỉnh 3,2 A mỗi kênh; mức cao 3,3 V của GPIO hoàn toàn hợp lệ. Với độ sụt áp thực tế khoảng 0,3 V ở dòng trung bình:

$$
V_\mathrm{motor} \approx 7.4 - 0.3 = 7.1\ \mathrm{V}
$$

Ngược lại, **module L298N** (cùng giá 45.000 ₫ nhưng không chọn làm mặc định) sử dụng cầu Darlington nên sụt khoảng 2,0 V khi có tải:

$$
V_\mathrm{motor} \approx 7.4 - 2.0 = 5.4\ \mathrm{V}
$$

Động cơ TT của khóa học hoạt động trong dải 3–9 V; ở 5,4 V động cơ vẫn quay nhưng chậm và yếu hơn hẳn mức 7,1 V, đặc biệt khi pin vơi dần. Ngoài ra, không nên lấy nguồn 5 V từ ổn áp tích hợp trên module L298N để nuôi ESP32.

![Module kiểu L298N: kéo được tải, và sụt áp lớn]({{ site.imgurl }}/wikimedia/Dosmotorsl298n.jpg)

**DRV8833** (giá tham khảo 25.000 ₫ trên Hshop) là lựa chọn thay thế gọn hơn, dải VM 2,7–10,8 V và tối đa 1,5 A mỗi kênh. Mạch hoạt động tốt khi mỗi kênh kéo một động cơ TT, nhưng vỏ nhỏ khiến chip nóng nhanh nếu bánh xe kẹt lâu; tuyệt đối không đấu song song hai động cơ lên cùng một kênh DRV8833. Riêng với TB6612, luôn nhớ kéo chân **STBY** lên mức cao, bởi nếu để thấp hoặc bỏ nổi, cầu H sẽ ở chế độ ngủ và động cơ đứng yên dù mã nguồn không báo lỗi.

## Mạch vi điều khiển và giới hạn điện áp 5 V

Một **mạch phát triển (dev board) ESP32** hoàn chỉnh có sẵn cổng USB, chip chuyển đổi USB-UART (như CH340 hoặc CP2102) nằm cạnh cổng USB, mạch ổn áp 3,3 V và module ESP32 bọc vỏ kim loại. Ngược lại, **module ESP32-WROOM trần** chỉ gồm phần vỏ kim loại cùng hàng chân hàn viền ngoài, không có cổng USB lẫn mạch ổn áp. Nếu sản phẩm không có cổng USB, đó không phải mạch phát triển yêu cầu trong BOM.

![ESP32 trên board phát triển nhỏ, có USB và ổn áp]({{ site.imgurl }}/wikimedia/ESP32_on_Lolin32_Lite_clone_board_cropped.jpg)

![Những thứ cần nhìn trên board vi điều khiển: USB, ổn áp, module, header]({{ site.imgurl }}/generated/pcb_mcu_anatomy.png)

**Raspberry Pi Pico** có hai hàng chân header song song (bản gốc không có module Wi-Fi bọc kim loại). Trên board này, **VBUS** là đường nguồn 5 V lấy từ cổng USB khi cắm máy tính, **3V3** là đầu ra đã ổn áp, và các chân GPIO chạy ở mức logic 3,3 V. Không lấy nguồn từ chân 3V3 để chạy động cơ TT và không nhầm VBUS là chân tín hiệu GPIO.

![Raspberry Pi Pico: header hai hàng, logic 3,3 V]({{ site.imgurl }}/wikimedia/Raspberry_Pi_Pico.jpg)

![Logic 3,3 V, USB 5 V, nguồn mô-tơ tách khỏi rail đó]({{ site.imgurl }}/generated/power_rails_3v3.png)

Đối với cảm biến siêu âm **HC-SR04**, chân `Trig` thường nhận tốt xung kích 3,3 V từ vi điều khiển, nhưng chân `Echo` xuất mức cao xấp xỉ 5 V nên tuyệt đối không cắm thẳng vào GPIO 3,3 V của ESP32 hay Pico. Cách an toàn và gọn nhất là dùng mạch chuyển mức logic 4 kênh (giá khoảng 10.000 ₫): nối phía 3,3 V với vi điều khiển, phía 5 V với cảm biến và nối mass chung. Cách thay thế là lắp cầu chia áp riêng cho chân `Echo` bằng điện trở 10 kΩ (phía trên) và 20 kΩ (phía dưới):

$$
V_\mathrm{out} = 5 \times \frac{20}{10 + 20} \approx 3.3\ \mathrm{V}
$$

mức điện áp hoàn toàn an toàn cho chân 3,3 V. Không lắp cầu chia áp lên chân đầu vào cần mức cao 5 V nếu chưa kiểm chứng cảm biến có nhận được 3,3 V hay không; thông thường chỉ cần hạ mức chân `Echo`, còn chân `Trig` có thể nối trực tiếp từ GPIO.

## Thực hành

Thực hiện toàn bộ các bước sau khi **đã tháo pin và chưa gắn động cơ**:

1. Chụp ảnh cận cảnh IC trên mạch lái đủ nét để đọc rõ ký hiệu (`TB6612FNG`, `DRV8833` hoặc `L298N`). Nếu ảnh chỉ thấy nhãn của bên bán module mà không thấy ký hiệu trên thân IC, hãy ghi chú rõ điều này.
2. Chụp ảnh chip USB-UART trên mạch vi điều khiển (thường là `CH340` hoặc `CP2102` nằm gần cổng USB của ESP32). Nếu mạch không có cổng USB và chip nối tiếp, bạn đang cầm module trần.
3. Dựa theo thông số TB6612, vẽ nhanh sơ đồ chân lên giấy và ghi nhãn đầy đủ: `AIN1`, `AIN2`, `PWMA`, `STBY`, `VM`, `VCC` và `GND`, sau đó đối chiếu với ký hiệu in lụa trên module (nếu đã có hàng). Xác nhận rõ: `VM` là nguồn động cơ (4,5–10 V), `VCC` là nguồn logic (2,7–5,5 V, nối từ chân 3,3 V của MCU), `GND` nối mass chung, và `STBY` phải kéo lên mức cao.
4. Trên ESP32 hoặc Pico, chỉ ra đúng ba vị trí: chân `3V3`, chân `5V` (hoặc `VBUS`) và một chân `GPIO`. Tự kiểm tra xem chân nào trong ba chân đó được phép nối thẳng vào chân `Echo` của HC-SR04 — đáp án đúng là **không chân nào** cho đến khi tín hiệu echo đã đi qua mạch chuyển mức hoặc cầu chia áp.

**Kết quả kỳ vọng:** Bạn có hai ảnh chụp sắc nét và một bản vẽ chân có nhãn rõ ràng (toàn bộ dây động cơ vẫn để trong túi), thể hiện `VM` và `VCC` là hai chân tách biệt hoàn toàn. Nếu một module lạ nối chung hai chân này làm một, tuyệt đối không cấp pin 7,4 V vào đó vì sẽ đưa quá áp lên chân logic.

| Hiện tượng quan sát | Nguyên nhân thường gặp | Cách khắc phục |
| --- | --- | --- |
| Động cơ đứng yên dù firmware đang xuất PWM đúng | Chân STBY bị bỏ nổi hoặc ở mức thấp | Kéo chân STBY lên mức cao theo đúng đường nguồn logic 3,3 V |
| Xe chạy yếu trên bộ pin 7,4 V mới sạc | Sụt áp lớn của cầu Darlington L298N (chỉ còn ~5,4 V) | Chuyển sang dùng TB6612; không nâng áp pin vượt giới hạn VM để bù |
| Đầu cắm Dupont nối vào chân VM bị nóng | Dùng dây tín hiệu mảnh dẫn dòng động cơ | Thay bằng dây nguồn tiết diện lớn hơn; chỉ dùng Dupont cho AIN1, AIN2, PWMA, STBY |
| Chân GPIO bị hỏng sau khi nối HC-SR04 | Đưa trực tiếp tín hiệu Echo 5 V vào chân 3,3 V | Lắp mạch chuyển mức hoặc cầu chia áp cho Echo trước khi thử lại |
| Hai đầu giắc không thể cắm vừa nếu không ấn mạnh | Nhầm lẫn giữa các họ JST-XH, JR, XT30, XT60 | Dừng lại, dùng đúng chuẩn giắc tương thích và không gọt gờ định hướng |

**Lưu ý an toàn:** Luôn nhấc bánh xe khỏi mặt bàn và tháo rời pin trong bài này; giữ ngón tay cách xa đầu kim loại que đo khi thao tác với nguồn điện. Mọi phép tính với nguồn 7,4 V hiện thực hiện trên giấy cho tới khi bạn đo thực tế trên thang DC lớn hơn 10 V ở các bài sau.

## Video tham khảo

- **Xem trước:** [H Bridge Motor Control Basics Explained](https://www.youtube.com/watch?v=YYMsS50x1UY) — The Engineering Mindset, tiếng Anh. Giải thích nguyên lý bốn khóa đóng cắt của mạch cầu H trước khi làm việc với module thực tế.
- [Logic Level Converters - Learn & Example Project - TXS0108E](https://www.youtube.com/watch?v=f7aySy_0URE) — DIY Machines, tiếng Anh. Minh họa cách đấu nối mạch chuyển mức logic giữa thiết bị 5 V và vi điều khiển 3,3 V.

## Bài tập

1. Với nguồn pin 7,4 V, tính lại điện áp tại động cơ khi qua cầu MOSFET (sụt 0,3 V) và cầu Darlington (sụt 2,0 V). Động cơ TT hoạt động tốt hơn ở mức nào, và vì sao không chọn L298N dù cùng giá 45.000 ₫?
2. Thông số DRV8833 ghi tối đa 1,5 A mỗi kênh, nhưng khi bánh kẹt vài giây thì chip nóng bỏng. Bạn đã chạm vào giới hạn nào, và vì sao con số "tối đa" không cho phép mắc song song hai động cơ lên cùng một kênh?
3. Liệt kê ba chân trên module TB6612 phù hợp để nối bằng dây Dupont, và một đường điện không nên dùng dây Dupont lâu dài.
4. Trong túi có một module ESP32-WROOM trần và một mạch NodeMCU-32S. Mạch nào sẽ hiện cổng serial khi cắm cáp USB, và cần chụp ảnh con chip nào nằm cạnh cổng USB?
5. Dây Echo của HC-SR04 sắp nối vào một chân GP của Raspberry Pi Pico. Dây Echo xuất mức điện áp bao nhiêu, chân VBUS dùng để làm gì, và linh kiện nào trong giỏ hàng phải đặt giữa Echo và chân GP?

<details>
<summary>Gợi ý đáp án</summary>

1. Cầu MOSFET: $7{,}4 - 0{,}3 = 7{,}1\ \mathrm{V}$; cầu Darlington: $7{,}4 - 2{,}0 = 5{,}4\ \mathrm{V}$. Động cơ TT (dải 3–9 V) chạy khỏe và nhanh hơn rõ rệt ở 7,1 V; cùng giá bán nhưng hiệu suất điện áp khác nhau hoàn toàn nên TB6612 là lựa chọn đúng.
2. Chip đã chạm giới hạn tản nhiệt của vỏ nhỏ gần trần dòng 1,5 A. Thông số tối đa là giới hạn chịu đựng đỉnh chứ không phải dòng vận hành liên tục cho hai động cơ mắc song song trên một kênh.
3. Dây Dupont phù hợp cho các chân tín hiệu như AIN1, AIN2, PWMA và STBY; không nên dùng lâu dài cho đường nguồn động cơ VM.
4. NodeMCU-32S có sẵn cổng USB để hiện cổng serial; cần chụp ảnh chip chuyển đổi USB-UART (CH340 hoặc CP2102) nằm cạnh cổng cắm. Module WROOM trần không có chip này.
5. Dây Echo xuất mức cao khoảng 5 V. VBUS là đường nguồn USB 5 V của Pico (không phải GPIO và không nối Echo vào đây). Cần đặt mạch chuyển mức 4 kênh (nối mass chung) hoặc cầu chia áp ở giữa dây Echo và chân GP.

</details>

## Đọc thêm

Trang sản phẩm của Pololu mô tả chi tiết mạch lái [Pololu TB6612FNG carrier](https://www.pololu.com/product/713), kèm trang thông số của phương án thay thế [DRV8833](https://www.ti.com/product/DRV8833). Bài viết [Logic levels](https://learn.sparkfun.com/tutorials/logic-levels) của SparkFun giải thích rõ sự chênh lệch mức logic 3,3 V và 5 V, còn giới hạn chân GPIO cụ thể nằm trong [ESP32 datasheet](https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf).

## Mua ở Việt Nam

Các hạng mục còn lại của xe nằm ở bài [BOM và cách mua bộ kit robot ở Việt Nam]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %}). Dưới đây là các mức giá tham khảo trên Hshop ngày 23 tháng 9 năm 2026 (cần kiểm tra lại giá hiện hành trước khi đặt):

Mạch lái mặc định giá 45.000 ₫: [TB6612FNG](https://hshop.vn/mach-dieu-khien-dong-co-dc-tb6612fng-dc-motor-driver) (VM 4,5–10 V, logic 2,7–5,5 V, 1,2 A liên tục / 3,2 A đỉnh). Phương án nhỏ hơn giá 25.000 ₫: [DRV8833](https://hshop.vn/mach-dieu-khien-dong-co-drv8833-dc-motor-driver) (VM 2,7–10,8 V, tối đa 1,5 A/kênh). Mạch [module L298N](https://hshop.vn/mach-dieu-khien-dong-co-dc-l298) cũng có giá 45.000 ₫ nhưng không dùng làm mặc định do sụt áp lớn.

Mạch chuyển mức cho chân Echo của HC-SR04 giá 10.000 ₫: [mạch chuyển mức 4 kênh](https://hshop.vn/mach-chuyen-muc-tin-hieu-logic-4-kenh). Mạch phát triển ESP32 có sẵn USB giá 190.000 ₫: [NodeMCU-32S CH340](https://hshop.vn/kit-rf-thu-phat-wifi-ble-esp32-nodemcu-32s-ch340-ai-thinker). Với Raspberry Pi Pico, bạn có thể tra cứu qua trang tìm kiếm Hshop: [tìm Raspberry Pi Pico](https://hshop.vn/search?q=raspberry+pi+pico) (ngày 23 tháng 9 năm 2026 ghi nhận Pico 2 giá 195.000 ₫ và Pico 2 W giá 275.000 ₫). Luôn chọn mạch phát triển có sẵn cổng USB thay vì module trần trừ khi bạn đã có mạch nạp riêng.
