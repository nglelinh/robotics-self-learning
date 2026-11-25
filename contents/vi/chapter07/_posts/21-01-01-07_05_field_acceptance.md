---
layout: post
title: "Test thực địa, log và nghiệm thu"
chapter: "07"
order: 5
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter07
lesson_type: required
draft: false
---

Đã kết thúc giai đoạn thử trên hộp kê. Trong bài này, bạn đặt robot xuống một làn sàn trống, chạy thử đủ bốn hướng ở mức PWM đã giới hạn và lập nhật ký (log) đủ tin cậy làm cơ sở cho chương sau. Tiêu chuẩn đạt dựa trên tập các quan sát đo được cụ thể, không dựa vào cảm tính “xe chạy được là ổn”.

Trong thế giới phần mềm, bạn viết unit test để biết code đúng hay sai. Trong thế giới robotics, unit test trên laptop không bao giờ đủ — một robot chỉ được coi là hoàn thiện khi vượt qua **bài kiểm tra nghiệm thu thực địa (Field Acceptance Test)** trên mặt sàn thật với các tiêu chí **đạt / không đạt (Pass/Fail) định lượng** rõ ràng và có tệp nhật ký (log) chứng minh! Nếu không có bài test định lượng, bạn sẽ không bao giờ biết lần sửa code mới nhất giúp robot chạy thẳng hơn hay thực ra làm nó tệ đi.

## Kiến thức cần nhớ: Kiểm thử thực địa, Ghi nhật ký đồng bộ và Tiêu chí nghiệm thu

### 1. Bộ 4 bài test thực địa kinh điển cho robot vi sai
Một quy trình nghiệm thu chuẩn gồm 4 kịch bản lặp lại được: (1) **Chạy thẳng 3–5 m** đo độ lệch ngang (đánh giá cân bằng bánh & odometry); (2) **Quay tại chỗ $$360^\circ$$** đo sai số góc (đánh giá hiệu chuẩn khoảng cách hai bánh $$L$$); (3) **Test ngắt kết nối đột ngột** kiểm tra Watchdog dừng đúng ngưỡng; và (4) **Test chạy bền 10 phút** giám sát nhiệt độ driver và đường cong tụt áp pin.

### 2. Ghi log có dấu thời gian (Timestamped Telemetry CSV)
Mắt thường rất dễ đánh lừa: bạn thấy xe "hơi giật", nhưng không biết do mất gói UART, do điện áp pin tụt, hay do encoder nhảy xung. Ghi log định dạng CSV gồm `(timestamp_ms, cmd_v, cmd_w, enc_L, enc_R, v_bat)` giúp bạn vẽ đồ thị phân tích hậu kiểm chính xác đến từng mili-giây.

### 3. Nghiệm thu dựa trên ngưỡng định lượng (Acceptance Criteria)
Mọi yêu cầu phải chuyển thành con số đo được trước khi chạy test (ví dụ: lệch ngang $$< 5\%$$ quãng đường, sai số quay $$360^\circ$$ nhỏ hơn $$\pm 10^\circ$$, thời gian dừng khẩn cấp $$< 0{,}5\text{ s}$$).

### Giải thích: Cầm tay đánh giá kết quả bài test chạy thẳng 5 mét và truy ngược sai số đường kính bánh

Bạn dán một đường băng keo thẳng dài **$$D = 5{,}00\text{ m}$$** trên sàn hành lang, đặt robot ngay vạch xuất phát rồi cho chạy thẳng $$5{,}00\text{ m}$$ với tiêu chí nghiệm thu **độ lệch ngang $$\le 5\%$$ ($$\le 25\text{ cm}$$)** và **sai số quãng đường $$\le 3\%$$ ($$\pm 15\text{ cm}$$)**.

Kết quả đo thực địa bằng thước dây:
- Xe dừng ở tọa độ dọc $$x = 4{,}92\text{ m}$$ và lệch sang trái $$\Delta y = 0{,}15\text{ m}\;(15\text{ cm})$$.

Kiểm tra các chỉ số nghiệm thu:
1. **Sai số quãng đường dọc:**
   $$\frac{\vert 4{,}92 - 5{,}00 \vert}{5{,}00} = \frac{0{,}08}{5{,}00} = 1{,}6\% \le 3\% \implies \textbf{ĐẠT}.$$
2. **Độ lệch ngang và góc lệch hướng tương đương:**
   $$\text{Tỷ lệ lệch ngang} = \frac{0{,}15}{5{,}00} = 3{,}0\% \le 5\% \implies \textbf{ĐẠT}.$$
   Góc lệch hướng trung bình: $$\theta_{\text{lệch}} \approx \arctan\!\left(\frac{0{,}15}{5{,}00}\right) \approx 1{,}72^\circ.$$
3. **Chẩn đoán nếu lần sau xe lệch tới $$\Delta y = 0{,}45\text{ m}$$ ($$9\% \to \textbf{KHÔNG ĐẠT}$$):**
   Vì xe đi theo cung tròn bán kính $$R \approx \frac{D^2}{2 \Delta y} = \frac{25}{0{,}90} \approx 27{,}8\text{ m}$$, với track width $$L = 0{,}20\text{ m}$$, hai bánh đang chênh nhau khoảng $$\frac{L}{R} = \frac{0{,}20}{27{,}8} \approx 0{,}72\%$$ — chỉ cần chỉnh lại hệ số bù đường kính bánh trái/phải $$0{,}7\%$$ trong cấu hình là xe lập tức chạy thẳng tắp!

## Mục tiêu học

1. Thực hiện chuỗi thử nghiệm trên làn sàn trống dài $$2~\mathrm{m}$$: tiến khoảng $$2~\mathrm{s}$$, dừng, lùi, quay trái và quay phải trong giới hạn $$\pm 180$$, luôn giữ tay sẵn sàng tại công tắc nguồn pin.
2. Chứng minh rằng khi ngắt chương trình gửi lệnh hoặc rút cáp USB (trong khi ESP32 vẫn ăn nguồn từ mạch buck), robot dừng hẳn chuyển động trong vòng $$0{,}5~\mathrm{s}$$.
3. Đo điện áp pin trước và sau lượt chạy; nếu thấy sụt áp bất thường khi có tải, xác định ngay là lỗi pack pin, dây dẫn hoặc cầu chì.
4. Ghi chép đầy đủ nhật ký gỡ lỗi (thời điểm, lệnh gửi, hành vi thực tế, điện áp, giả thuyết lỗi) và chỉ nghiệm thu xe khi bảng dấu, timeout, cố định pin và kích thước hình học Chương 06 đều có đầy đủ trong sổ.

## Kiến thức cần có

Các bài 07-01 đến 07-04 đã hoàn thiện toàn bộ hệ thống cơ sở: pin buộc chắc chắn, cực dương qua cầu chì, mạch buck 5,0 V, bảng dấu chiều quay, giao thức chữ, bước kéo PWM và timeout. Chương 05 cung cấp kiến thức về dòng kẹt và kiểm soát nhiệt mạch cầu. Hai kích thước $$b$$ và $$r$$ từ Chương 06 đã được lưu trong `lab-notes.md` (ví dụ mẫu $$b = 0{,}15~\mathrm{m}$$ hoặc $$148~\mathrm{mm}$$ đo thực tế, và $$r = 31{,}2~\mathrm{mm}$$). Bài này vẫn chưa dùng `Twist`; bạn có thể ghi lại quãng đường và thời gian chạy như một số liệu quan sát, nhưng không được gán cứng thành hệ số quy đổi cho PWM — phần hiệu chuẩn sang m/s thuộc Chương 08.

## Vì sao bài này quan trọng với Capstone A và ROS

Bộ điều khiển PID ở Chương 08 hoạt động dựa trên giả định chiều quay hai bánh đã đúng dấu và bánh tự dừng khi mất lệnh. Nếu bánh phải bị đảo chiều, khâu tỉ lệ sẽ khuếch đại sai số quay theo hướng ngược lại. Tương tự, Chương 09 giả định khung xe luôn dừng an toàn khi node phát lệnh bị tắt (hoặc laptop rơi vào chế độ ngủ). Buổi nghiệm thu này là cổng kiểm tra cuối cùng của phần cứng cơ bản: bốn hướng khớp bảng dấu, dừng an toàn khi mất tín hiệu, pin cố định an toàn và sổ tay lưu đủ ảnh đi dây, đặc tả giao thức, điện áp cùng $$b$$, $$r$$.

![Hình học log phải dẫn: $$b$$ giữa hai vết lốp, $$r$$ từ phép lăn]({{ site.imgurl }}/generated/chassis_measures.png)

![Tiến, quay, và trường hợp trộn mà bạn sắp xin bằng PWM, không bằng m/s]({{ site.imgurl }}/generated/diff_drive_kinematics.png)

Các mũi tên trong hình thứ hai biểu diễn trực quan từng trạng thái chuyển động: `V 80 80` đẩy cả hai bánh tiến, còn `V -60 60` cho bánh phải tiến và bánh trái lùi để quay trái khi bảng dấu chính xác. Lưu ý rằng công thức trên hình viết theo đơn vị vận tốc, trong khi lệnh bạn gửi hiện tại vẫn đang ở đơn vị nấc PWM.

## Làn, công tắc giết, và điện áp biết động

Dọn một làn sàn trống dài ít nhất $$2~\mathrm{m}$$ (không có mép bậc hay vật cản trong quãng phanh) và luôn giữ công tắc pin trong tầm với. Thiết lập máy chủ gửi lặp lại mỗi $$200~\mathrm{ms}$$, firmware quá hạn $$250~\mathrm{ms}$$ và giữ mức duty ở 60 hoặc 80 (không dùng 255).

Thực hiện tuần tự chuỗi năm bước sau (duy trì gửi lặp cho tới khi chuyển lệnh):

1. `V 80 80` trong khoảng $$2~\mathrm{s}$$: cả hai lốp quay tiến, xe bám thẳng làn.
2. `V 0 0` (hoặc ngừng gửi để kích hoạt timeout): xe dừng lại.
3. `V -80 -80` trong khoảng $$2~\mathrm{s}$$: xe lùi thẳng.
4. `V -60 60` trong một đoạn ngắn: mũi xe quay sang trái.
5. `V 60 -60` trong một đoạn ngắn: mũi xe quay sang phải.

Tiếp theo, tắt đột ngột tiến trình máy gửi hoặc rút cáp USB trong khi ESP32 vẫn nhận nguồn từ mạch buck. Xe phải dừng hẳn trong vòng $$0{,}5~\mathrm{s}$$ (theo tính toán ở Bài 04 là khoảng $$330~\mathrm{ms}$$ sau lệnh `V 60 60` cuối). Nếu xe vẫn trôi tới 3 giây thì bài nghiệm thu trượt, dù bốn hướng chạy đều đẹp.

Đo điện áp nghỉ trước và sau lượt chạy: một pack pin tốt sau lượt thử ngắn thường chỉ giảm nhẹ, ví dụ từ $$8{,}15~\mathrm{V}$$ xuống $$8{,}05~\mathrm{V}$$. Nếu đo được khi đang có tải — giả sử nghỉ $$8{,}20~\mathrm{V}$$ nhưng sụt xuống $$6{,}90~\mathrm{V}$$ ở dòng $$0{,}60~\mathrm{A}$$ — ta ước lượng tổng nội trở mạch nguồn là:

$$
R \approx \frac{1{,}30}{0{,}60} \approx 2{,}2~\Omega.
$$

Giá trị $$2{,}2~\Omega$$ là rất lớn so với mức vài trăm miliôm của một pack pin khỏe. Nguyên nhân thường nằm ở cell đã chai, dây dẫn quá mảnh, cầu chì tự phục hồi (polyfuse) bị nóng hoặc tiếp xúc đế pin kém. Cần xử lý triệt để lỗi nguồn này trước khi nghiệm thu vì nguồn yếu sẽ gây sụt áp và làm reset MCU giữa làn chạy (lưu ý hàm `setup()` đã đặt PWM về 0 trước khi kéo `STBY` cao).

Nếu bạn bấm giờ một đoạn chạy thử — ví dụ xe đi $$1{,}6~\mathrm{m}$$ trong $$4{,}0~\mathrm{s}$$ — tốc độ trung bình quan sát được là:

$$
v_{obs} = \frac{1{,}6}{4{,}0} = 0{,}40~\mathrm{m/s}.
$$

Hãy ghi nhận chính xác bối cảnh: “ở PWM 80, lượt thử trên sàn này đạt khoảng $$0{,}40~\mathrm{m/s}$$”, tuyệt đối không quy ước cứng “PWM 80 = $$0{,}40~\mathrm{m/s}$$” như một hằng số cho `Twist`.

## Log là dụng cụ nghiệm thu

Mỗi hàng trong bảng nhật ký tương ứng với một sự kiện thực tế. Cột “Giả thuyết” để trống khi robot hành xử đúng bảng dấu, và bắt buộc phải ghi chẩn đoán khi có sai lệch:

| Giờ | Lệnh | Robot làm gì | Điện áp | Giả thuyết |
|-----|------|--------------|---------|------------|
| 0:00 | nghỉ | đứng, pin đã buộc | 8,15 V | |
| 0:12 | `V 80 80` trong 2 s | thẳng theo làn | 7,9 V có tải | |
| 0:15 | giết máy gửi | dừng rõ trong 0,5 s | 8,12 V | |
| 0:30 | `V -60 60` | mũi trái | 8,0 V | |
| 0:40 | `V 60 -60` | mũi phải | 8,0 V | |

Không được bỏ qua một hàng lỗi để chấm đạt chung. Nếu ngắt máy gửi mà xe vẫn chạy tiếp tới vạch băng dính thì cơ chế timeout chưa hoạt động (thanh ghi LEDC vẫn giữ PWM cũ); bạn phải quay lại Bài 04 để kiểm chứng dừng trên hộp kê trước khi chạy lại trên sàn. Nếu lệnh `V 80 80` khiến xe xoay tròn thì một bên động cơ bị ngược dấu — chỉ đảo dây hoặc đảo cực tính firmware một lần duy nhất. Không chuyển sang Chương 08 khi còn bất kỳ lỗi nào chưa khép lại.

**Tiêu chí nghiệm thu đạt:** Đủ cả bốn hướng khớp bảng dấu; cơ chế dừng theo timeout hoạt động trong $$0{,}5~\mathrm{s}$$; pin buộc chắc chắn và không có đầu hàn lithium trần; sổ tay lưu đầy đủ ảnh đi dây, đặc tả giao thức (`V`, `S`, $$200~\mathrm{ms}$$, $$250~\mathrm{ms}$$), bảng dấu, các mức điện áp và kích thước $$b$$, $$r$$.

## Lab

### An toàn

Chuẩn bị làn sàn trống dài $$2~\mathrm{m}$$ có thêm khoảng trống phanh và giữ công tắc pin sẵn sàng trong tay. Duy trì mức duty đã kiểm thử; ngắt công tắc ngay nếu xe lao về phía người hoặc mép bậc. Nếu xe kẹt vào tường, tối đa 1 giây phải ngắt nguồn; dừng ngay toàn bộ thử nghiệm nếu thấy mùi khét hoặc mạch driver quá nóng.

### BOM

| Món | Việc |
|------|------|
| Cây nguồn và firmware đã nhận | Bài 01–04 |
| Sàn trống, băng ở $$2~\mathrm{m}$$ | Làn |
| Đồng hồ | Điện áp trước và sau |
| `lab-notes.md` | Log |
| Công tắc pin trong tay | Nút giết |

### Các bước

1. Kiểm tra bánh xe đã chạm sàn, bánh caster bám tốt, pin buộc chắc chắn và ảnh đi dây đã lưu trong sổ. Đo điện áp nghỉ của pack pin.
2. Sẵn sàng tay ở công tắc nguồn. Chạy lần lượt chuỗi: tiến khoảng $$2~\mathrm{s}$$, dừng, lùi, quay trái và quay phải; đọc to hoặc ghi ngay lệnh vừa gửi để nhật ký trung thực.
3. Ngắt tiến trình máy gửi hoặc rút cáp USB (trong khi ESP32 vẫn ăn nguồn từ buck) và bấm giờ thời gian dừng; yêu cầu dưới $$0{,}5~\mathrm{s}$$.
4. Đo lại điện áp nghỉ sau lượt chạy. Nếu phát hiện sụt áp mạnh khi có tải, tính ước lượng nội trở $$R$$ và ghi giả thuyết nguyên nhân.
5. Chấm đạt hoặc trượt dựa theo đủ bốn tiêu chí nghiệm thu. Nếu trượt, sửa đúng một lỗi gốc rồi chạy lại toàn bộ chuỗi thử.

### Kết quả mong đợi

Một bảng nhật ký đã điền đầy đủ, xác nhận dừng hẳn trong nửa giây khi mất tín hiệu, điện áp nghỉ ổn định không sụt sâu, và chỉ ghi “đạt” khi hội tụ đủ hướng chạy, timeout, an toàn pin và bộ hồ sơ ghi chú (ảnh, giao thức, bảng dấu, $$b$$, $$r$$). Mọi số đo tốc độ đều được gắn nhãn là số liệu quan sát riêng lẻ, không gắn cứng vào giao thức.

### Lỗi thường gặp

| Bạn thấy | Thường là |
|----------|-----------|
| Lệnh thẳng mà xe vẽ vòng | Một dấu còn ngược; sửa một lần |
| Còn lăn sau khi laptop ngủ | Sketch không có timeout |
| Mũi nhấc lúc tăng tốc | Khối pin nằm sau trục; quay lại bài 01 |
| Điện áp sụt một volt trở lên ở dòng vừa phải | Cell, đế, dây, hoặc polyfuse |
| Chỉ dừng khi rút USB đồng thời reset chip | Buck không phải nguồn logic; thử lại khi MCU còn nuôi |

## Mua ở Việt Nam / Where to buy in Vietnam

Các buổi nghiệm thu thường trượt do thiếu dây buộc cố định pin, đế pin tiếp xúc kém hoặc chưa lắp cầu chì. Giá tham khảo khoảng năm 2026 (có thể thay đổi): pack 2S hoặc đế 18650 80.000–180.000 đồng, công tắc 8.000–20.000 đồng, đế chì kèm cầu chì 2–3 A 10.000–25.000 đồng, mạch buck LM2596 10.000–25.000 đồng, TB6612 25.000–70.000 đồng (L298N giá khoảng 45.000 đồng là phương án thay thế tạm).

- L298N đã kiểm, khoảng 45.000 đồng: [hshop.vn/mach-dieu-khien-dong-co-dc-l298](https://hshop.vn/mach-dieu-khien-dong-co-dc-l298)
- [Hshop cầu chì](https://hshop.vn/search?q=cau+chi), [LM2596](https://hshop.vn/search?q=LM2596)
- [Shopee pin 2S](https://shopee.vn/search?keyword=pin%202S%2018650), [công tắc](https://shopee.vn/search?keyword=c%C3%B4ng%20t%E1%BA%AFc%20ngu%E1%BB%93n)
- [Lazada holder 18650](https://www.lazada.vn/catalog/?q=holder%2018650%202S)
- [Thế Giới IC cầu chì](https://www.thegioiic.com/search?q=cau%20chi)

## Video tham khảo

- **Xem trước:** [Differential Drive & Odometry Explained: How It Works](https://www.youtube.com/watch?v=2QE3LG5h2tw) — Netizen Robotics, tiếng Anh. Minh họa trực quan chuyển động đi thẳng khi hai bánh cùng tốc độ và quay khi có chênh lệch tốc độ — đúng các hành vi cần xác nhận trong buổi nghiệm thu.

## Bài tập

1. Pack pin đo lúc nghỉ được $$8{,}20~\mathrm{V}$$, khi cả hai động cơ chạy sụt xuống $$6{,}90~\mathrm{V}$$ ở dòng khoảng $$0{,}60~\mathrm{A}$$. Ước lượng tổng điện trở $$R$$ và đánh giá hệ nguồn này có đạt chuẩn nghiệm thu hay không.
2. Xe chạy thẳng $$1{,}6~\mathrm{m}$$ trong $$4{,}0~\mathrm{s}$$ ở mức PWM 80. Bạn ghi tốc độ quan sát là bao nhiêu, và nhận định nào không được phép đưa vào ghi chú `Twist`?
3. Khi rút cáp USB trong lúc ESP32 vẫn được nuôi bằng mạch buck, xe vẫn lăn tiếp khoảng $$3~\mathrm{s}$$. Tiêu chí nghiệm thu nào bị trượt và phần mã nguồn ở bài nào đang thiếu?
4. Xe đã hoàn thành chuỗi chạy trên sàn, sổ tay có đủ điện áp và ảnh đi dây nhưng để trống $$b$$ và $$r$$. Vì sao vẫn chưa thể nghiệm thu để sang Chương 08?
5. Lệnh `V 60 -60` làm mũi xe quay sang trái thay vì quay phải. Nêu một cách sửa đúng và cho biết thao tác thứ hai nào sẽ vô tình hủy bỏ cách sửa đó.

### Gợi ý đáp án

1. $$R \approx 1{,}30/0{,}60 \approx 2{,}2~\Omega$$ — quá lớn so với mức vài trăm miliôm của pack pin khỏe. Cần dừng nghiệm thu để kiểm tra cell pin, tiếp xúc đế pin, tiết diện dây hoặc polyfuse đang nóng.
2. Tốc độ quan sát $$v_{obs} = 1{,}6/4{,}0 = 0{,}40~\mathrm{m/s}$$ cho riêng lượt thử đó. Không được viết “PWM 80 = $$0{,}40~\mathrm{m/s}$$” như hằng số quy đổi cố định vì bước hiệu chuẩn thuộc Chương 08.
3. Tiêu chí dừng theo timeout bị trượt. Đoạn kiểm tra quá hạn $$250~\mathrm{ms}$$ ở Bài 04 đang bị thiếu hoặc không được thực thi, khiến thanh ghi PWM giữ nguyên mức duty cuối.
4. Mô hình động học và vòng điều khiển ở Chương 08 bắt buộc cần khổ vết $$b$$ và bán kính lăn $$r$$ đã đo ở Chương 06; để trống sẽ buộc bộ điều khiển phải dùng số ước đoán.
5. Đảo hai dây động cơ phải trên cầu vít **hoặc** đảo cực tính điều khiển bánh phải trong firmware (chỉ chọn một). Nếu làm cả hai cùng lúc thì hai lần đảo triệt tiêu nhau và lỗi quay ngược sẽ tái diễn; sau khi sửa cần chạy lại đủ bốn hướng.

## Đọc thêm

- [geometry_msgs/Twist (Jazzy)](https://docs.ros.org/en/jazzy/p/geometry_msgs/interfaces/msg/Twist.html)
- [Pololu TB6612FNG](https://www.pololu.com/product/713)
- [Datasheet L298 của ST](https://www.st.com/resource/en/datasheet/l298.pdf)
- [pySerial, phần mở đầu](https://pyserial.readthedocs.io/en/latest/shortintro.html)
