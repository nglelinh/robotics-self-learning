---
layout: post
title: "ESD, cực tính, cầu chì và sụt áp"
chapter: "01"
order: 9
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter01
lesson_type: required
draft: false
---

Ba sự cố phần cứng rất dễ bị đổ lỗi nhầm cho phần mềm "chạy thiếu ổn định": phóng tĩnh điện làm hỏng chân IC ngay trước khi bạn nạp code; cắm ngược cực pin phá hủy mạch lái ngay lúc vừa chạm giắc; và động cơ kẹt trục kéo sụt đường nguồn 5 V khiến ESP32 liên tục khởi động lại. Bài học này tách bạch cả ba cơ chế và giúp bạn xây dựng một giả thuyết kỹ thuật rõ ràng để kiểm chứng khi lắp động cơ về sau.

## Mục tiêu

Sau bài học này, bạn sẽ hình thành thói quen chống tĩnh điện đúng mức: chạm vào vật kim loại nối đất rồi cầm mạch ở phần cạnh viền. Bạn sẽ hiểu tác hại của việc đảo cực đối với tụ hóa và chân VM của TB6612, luôn đo cực tính bằng đồng hồ trước lần cấp nguồn đầu tiên thay vì tin theo màu dây. Bạn sẽ biết cách chọn cầu chì tự phục hồi hoặc cầu chì 2–3 A (cao hơn dòng chạy không tải của hai động cơ TT nhưng thấp hơn mức dòng gây cháy dây pin). Cuối cùng, bạn sẽ giải thích được hiện tượng sụt áp (brownout) khi dùng chung nguồn 5 V lúc kẹt trục và trình bày đủ biện pháp xử lý: dùng pin động cơ riêng, chỉ nối chung mass, lắp tụ 100–470 µF đúng cực ngang chân VM, dùng dây động cơ đủ tiết diện, nhấc bánh khỏi mặt bàn, và lập trình firmware đưa PWM về 0 khi nguồn sụt hoặc mất lệnh quá khoảng 300 ms.

## Kiến thức cần có

Bạn đã nắm rõ cách xác định cực tính tụ hóa (bài 04), tách biệt chân VM và VCC (bài 07) và tính toán cơ bản theo định luật Ohm. Hôm nay bạn chỉ đo đường nguồn USB — không quay bánh xe và chưa nối pin động cơ.

---

Ba "sát thủ thầm lặng" thường xuyên đánh gục các dự án robot sinh viên nhất không hề xuất hiện trong thông báo lỗi trình biên dịch: **phóng tĩnh điện (ESD)** đánh thủng cổng MOSFET mà không để lại vết cháy nào, **cắm ngược cực nguồn** phá hủy IC ổn áp trong tích tắc, và **sụt áp (brownout)** khiến ESP32 liên tục tự khởi động lại đúng khoảnh khắc hai bánh xe vừa quay! Bài này trang bị cho bạn bộ giáp điện tử để chặn đứng cả ba sát thủ ấy.

## Kiến thức cần nhớ: Bảo vệ Mạch Điện tử khỏi ESD, Ngược cực và Sụt áp

1. **Phóng tĩnh điện (ESD — Electrostatic Discharge):** Khi bạn đi trên sàn nhựa hay kéo áo khoác len, cơ thể tích điện tới $$3.000\text{–}10.000\text{ V}$$! Tuy dòng ngắn nhưng điện trường cực lớn đủ đánh thủng lớp oxit cổng dày vài nanomet của chip CMOS — giải pháp đơn giản là luôn chạm tay vào khung kim loại tiếp đất trước khi cầm bo mạch và cầm vào mép PCB.
2. **Bảo vệ Ngược cực (Reverse Polarity Protection):** Một diode Schottky nối tiếp (mất $$0.3\text{ V}$$), cầu chì + diode song song, hoặc mạch P-MOSFET chống ngược cực sẽ cứu toàn bộ bo mạch khi bạn vô tình đấu nhầm dây đỏ–đen.
3. **Sụt áp (Brownout) & Tách đường Nguồn:** Khi động cơ DC khởi động, dòng tăng vọt gấp $$3\text{–}5\times$$ dòng chạy đều; theo định luật Ohm $$\Delta V = I \cdot R_{\text{dây+pin}}$$, điện áp đường nguồn lập tức sụt sâu. Nếu vi điều khiển dùng chung đường nguồn yếu đó và sụt xuống dưới ngưỡng **Brownout Detector** (~$$2.43\text{ V}$$ trên ESP32), chip sẽ tự reset lặp đi lặp lại (*boot loop*)!

### Ví dụ làm từng bước: Tính sụt áp gây Brownout Reset khi động cơ khởi động

Giả sử xe dùng nguồn 5 V (hoặc pin 2S yếu) đi qua một sợi dây jumper mảnh dài + tiếp điểm breadboard có tổng điện trở $$R_{\text{đường}} = 0.5\ \Omega$$. Khi 2 động cơ cùng khởi động đột ngột, dòng đỉnh đạt $$I_{\text{đỉnh}} = 2.5\text{ A}$$:

$$
\Delta V_{\text{sụt}} = I_{\text{đỉnh}} \cdot R_{\text{đường}} = 2.5\text{ A} \times 0.5\ \Omega = \mathbf{1.25\text{ V}}!
$$

- Trên đường nguồn $$5.0\text{ V}$$ chung: điện áp tại chân `5V` của ESP32 tụt ngay xuống $$5.0 - 1.25 = \mathbf{3.75\text{ V}}$$.
- Qua bộ ổn áp LDO AMS1117 (cần điện áp rơi tối thiểu $$V_{\text{dropout}} \approx 1.1\text{ V}$$): điện áp đầu ra đường 3,3 V tụt xuống chỉ còn $$3.75 - 1.1 = \mathbf{2.65\text{ V}}$$ (và chỉ cần thêm một gai nhiễu nhỏ $$0.25\text{ V}$$ là chạm ngưỡng brownout $$2.43\text{ V}$$ → **ESP32 lập tức reset!**).
- **Cách khắc phục bằng con số:** thay dây động cơ bằng dây 20 AWG hàn chắc ($$R_{\text{đường}} \approx 0.05\ \Omega$$) và đi nhánh sao (*star topology*) tách riêng đường pin cấp cho động cơ khỏi nhánh Buck cấp cho ESP32 → độ sụt giảm **10 lần** xuống chỉ còn $$0.125\text{ V}$$!

### Giải thích: 4 tuyến phòng thủ chống hỏng mạch trên xe robot

1. **Bước 1 — Phòng ESD bằng thói quen cầm mép bo:** Luôn chạm tay vào vật kim loại lớn trước khi chạm vào ESP32/IMU; cất bo mạch trong túi chống tĩnh điện khi không dùng.
2. **Bước 2 — Chống ngược cực bằng cơ khí trước, điện tử sau:** Dùng giắc có ngàm định hướng (JST/XT30) kết hợp màu dây chuẩn Đỏ/Đen để không thể cắm ngược ngay từ thao tác tay.
3. **Bước 3 — Luôn đi nguồn hình sao (Star Power Distribution):** Tách hai nhánh dây riêng từ cực pin (sau công tắc & cầu chì): Nhánh 1 chạy thẳng tới Driver động cơ; Nhánh 2 chạy qua mạch Buck 5 V + tụ lọc tới ESP32.
4. **Bước 4 — Đọc thông báo `Brownout detector was triggered` trên Serial Monitor:** Khi thấy dòng chữ này trên ESP32, **đừng** tắt bộ phát hiện brownout bằng phần mềm — hãy sửa ngay đường nguồn và dây dẫn!

**Kiểm tra nhanh.** Nếu bạn thấy ESP32 chạy code nhấp LED bình thường khi cắm USB, nhưng cứ gửi lệnh cho động cơ quay ở tốc độ 100% là Serial Monitor in lại dòng khởi động `rst:0x1 (POWERON_RESET)` hoặc `Brownout detector was triggered`, lỗi nằm ở code hay ở phần cứng nguồn? **100% ở phần cứng nguồn** — dòng khởi động động cơ đang kéo tụt đường nguồn nuôi ESP32!

---

## Vì sao bài này quan trọng

Xe Capstone gồm vi điều khiển 3,3 V (ESP32 hoặc Pico), một mạch lái TB6612, hai động cơ TT và một cảm biến HC-SR04. Khi vận hành thực tế, hiện tượng kẹt bánh (va chạm vướng vật cản hoặc bị giữ bánh) chắc chắn sẽ xảy ra. Nếu chân VM đang nối chung vào đường 5 V nuôi vi điều khiển, dòng kẹt sẽ kéo tụt đường 5 V, làm nguồn 3,3 V sụp theo và khiến chip tự reset giữa chừng — biểu hiện bên ngoài rất giống lỗi phần mềm. Một dạng lỗi âm thầm khác là đưa thẳng chân echo 5 V của HC-SR04 vào chân GPIO (đã cấm ở bài 07). Cả hai đều là lỗi phần cứng mà việc sửa mã nguồn không thể khắc phục; tách riêng nguồn động cơ và chỉ nối chung một điểm mass là nền tảng để hệ thống hoạt động ổn định và dễ chẩn đoán.

![Rail logic đứng cạnh rail mô-tơ]({{ site.imgurl }}/generated/power_rails_3v3.png)

Hai hệ thống nguồn chỉ gặp nhau duy nhất tại điểm mass (GND): đường 3,3 V nuôi vi điều khiển và chân logic của mạch lái, còn nguồn động cơ nuôi chân VM. Việc nối chung nguồn USB vào đường động cơ chắc chắn dẫn đến sụt áp. Cảm biến HC-SR04 được cấp nguồn 5 V riêng cho mạch nuôi, nhưng chân echo vẫn tuyệt đối không được nối thẳng vào GPIO.

![Thứ tự cấp nguồn, bánh còn nhấc khỏi bàn]({{ site.imgurl }}/generated/power_order.png)

Trong buổi thực hành hôm nay, chỉ cấp nguồn logic qua USB và giữ hoàn toàn ngắt phần động cơ. Ở giai đoạn vận hành sau này, chân STBY phải giữ ở trạng thái chờ cho tới khi cả hai nguồn đã ổn định và chương trình sẵn sàng.

## Phóng tĩnh điện (ESD) ở mức thực tế

Phóng tĩnh điện (ESD) có thể tạo ra xung điện áp lớn dù bạn không nhìn thấy tia lửa; chỉ cần bước trên thảm rồi chạm trực tiếp vào chân mạch Pico trần hay cực cổng MOSFET cũng đủ đánh thủng lớp ôxít bên trong IC. Thói quen phòng tránh rất đơn giản và hiệu quả: chạm tay vào một bề mặt kim loại nối đất (như vỏ thùng máy tính đang cắm điện) trước khi thao tác, luôn cầm mạch ở mép cạnh thay vì chạm vào linh kiện, giữ mạch trong túi chống tĩnh điện khi chưa dùng và không chuyền tay mạch trần ngang phòng. Các module hàn sẵn tuy bền hơn transistor rời nhưng vẫn cần tuân thủ thói quen này. Vòng đeo tay chống tĩnh điện là trang bị bổ sung tốt, nhưng không phải điều kiện bắt buộc cho bài lab này.

## Kiểm soát cực tính

Cấp ngược cực cho tụ hóa nhôm sẽ làm tụ nóng lên nhanh chóng cho đến khi xì bung vỏ, thậm chí làm hỏng đường mạch đồng xung quanh; cấp ngược cực vào chân VM cũng phá hủy mạch lái bên trong. Luôn nhớ: dải vạch trên vỏ tụ hóa là **cực âm** nối về mass; cực dương pin nối vào chân **VM**, tuyệt đối không nối vào GPIO.

Về lâu dài, bạn có thể lắp thêm diode Schottky nối tiếp trên dây dương hoặc dùng giắc chống cắm ngược như XT30 (lưu ý diode Schottky sẽ làm sụt vài phần mười vôn ở dòng động cơ nên cần cân nhắc trước khi lắp). Còn ngay ở bước hiện tại, quy tắc bắt buộc là đo điện áp pin bằng đồng hồ trước khi nối vào mạch lái: đặt que đỏ vào dây bạn cho là cực dương, que đen vào dây còn lại — nếu màn hình hiện số dương thì đúng, nếu hiện dấu trừ thì dừng ngay. Tuyệt đối không đoán cực chỉ dựa vào màu vỏ dây.

Cảm biến HC-SR04 cũng có cực tính nguồn: `VCC` nhận 5 V, `Trig` là ngõ vào, `Echo` là ngõ ra 5 V. Đảo ngược `VCC` và `GND` sẽ làm hỏng cảm biến, còn cắm thẳng `Echo` vào GPIO vi phạm giới hạn bài 07 — hãy luôn kiểm tra lại cả hai điểm này trên tờ sơ đồ chân trước khi cấp điện.

## Vì sao cổng USB không thể nuôi động cơ

Theo thông số động cơ TT 1:48 dùng trong khóa học, dòng chạy không tải của mỗi động cơ nằm trong khoảng 110–150 mA. Khi cả hai bánh quay trên không, tổng dòng tiêu thụ khoảng:

$$
2 \times 130\,\mathrm{mA} \approx 0{,}26\,\mathrm{A}
$$

Làm tròn khoảng $$0{,}3\,\mathrm{A}$$. Vì cổng USB tiêu chuẩn cấp khoảng 500 mA, lúc thử không tải nhìn bề ngoài có vẻ vẫn còn dư:

$$
0{,}50 - 0{,}30 = 0{,}20\,\mathrm{A}
$$

Tuy nhiên đây là khoảng dư ảo. Dòng kẹt trục thực tế lớn gấp nhiều lần dòng không tải — chỉ riêng một động cơ TT bị kẹt đã đòi hỏi dòng vượt quá giới hạn 500 mA của cổng USB. Do đó, USB không bao giờ được dùng làm nguồn cho động cơ. Mức 1,2 A liên tục của TB6612 chỉ là giới hạn chịu dòng của chip chứ không phải nguồn tự cấp dòng; nguồn cung cấp dòng bắt buộc phải là pin nối vào chân VM.

## Cơ chế sụt áp (brownout) và giải pháp thiết kế

Đường nguồn 5 V dùng chung luôn tồn tại điện trở ký sinh trên cáp và đầu cắm. Khi dòng kẹt tăng vọt, độ sụt áp trên đường dây được tính bằng:

$$
\Delta V = I_{\mathrm{ket}} \times R_{\mathrm{duong}}
$$

Khi đường 5 V bị kéo tụt, mạch ổn áp 3,3 V mất khoảng chênh áp làm việc (dropout), dẫn đến ESP32 hoặc Pico bị reset ngay giữa lệnh điều khiển. Nếu thấy thông báo khởi động (boot banner) bất ngờ xuất hiện trên Serial Monitor ngay lúc xe nhận lệnh chạy, đó chính là dấu hiệu điển hình của sụt áp.

Biện pháp khắc phục đồng bộ về phần cứng gồm bốn điểm:
1. **Tách nguồn riêng:** cấp nguồn động cơ bằng pin riêng (trong dải VM 4,5–10 V của bài 07), còn mạch logic tạm cấp qua USB. Hai nguồn chỉ nối chung đúng một điểm mass (và không để dòng động cơ chạy dọc theo thanh nguồn breadboard mảnh).
2. **Lắp tụ đệm gần mạch lái:** mắc một tụ hóa nhôm 100–470 µF (định mức 16 V hoặc 25 V, lớn hơn trần 10 V của VM) ngay sát chân VM và GND của driver, đúng chiều vạch âm về mass. Tụ giúp bù sườn dòng đột ngột khi động cơ khởi động hoặc kẹt.
3. **Dây dẫn và an toàn cơ khí:** dùng dây động cơ đủ tiết diện và luôn nhấc bánh xe khỏi mặt bàn khi chưa chủ định cho xe chạy (đặt bánh chạm bàn trong lúc thử nghiệm rất dễ tự tạo tình huống kẹt tải).
4. **Bảo vệ bằng firmware:** lập trình đưa duty PWM về 0 nếu phát hiện nguồn sụt hoặc khi mất lệnh điều khiển quá khoảng 300 ms, đồng thời có thể hạ chân STBY về trạng thái chờ để đảm bảo dừng hẳn khi bên gửi mất kết nối.

## Chọn cầu chì bảo vệ

Lắp một cầu chì thường hoặc cầu chì tự phục hồi (resettable fuse) định mức **2–3 A** trên dây dương sát cực pin là biện pháp bảo vệ đơn giản và rẻ tiền. Mức 2–3 A đủ cao hơn dòng chạy bình thường (khoảng $$0{,}3\,\mathrm{A}$$) để không ngắt nhầm khi xe đang chạy, nhưng đủ thấp hơn dòng ngắn mạch hàng chục ampe có thể làm cháy dây pin. Chọn cầu chì dưới $$0{,}3\,\mathrm{A}$$ sẽ khiến mạch ngắt liên tục. Lưu ý rằng cầu chì chỉ bảo vệ quá dòng/ngắn mạch, không thay thế việc tách pin riêng và không chống cắm ngược cực, nên vẫn phải đo cực tính trước khi đấu nối.

## Thực hành

Thực hiện bài lab khi **chỉ cắm USB**, đã rút hoàn toàn động cơ và pin (nếu bánh đã lắp trên trục vẫn phải giữ nhấc khỏi mặt bàn).

1. Chạm tay vào bề mặt kim loại nối đất rồi cầm mạch vi điều khiển bằng phần cạnh viền; ghi nhận đã thực hiện vào sổ.
2. Cắm duy nhất cáp USB vào mạch. Dùng đồng hồ ở thang DC V (que đen đặt tại mass) đo thực tế điện áp tại chân `5V` và chân `3V3`, ghi lại chính xác con số đo được (không ghi chung chung là "ổn").
3. Mở lại tờ sơ đồ chân bài 07 (hoặc phác nhanh bốn chân cảm biến), khoanh tròn chân `Echo` của HC-SR04 và ghi rõ chú thích cấm nối thẳng ngõ ra 5 V này vào chân GPIO.
4. Chép và điền số đo thực tế của bạn vào khung giả thuyết sau cho Chương 02: *"Khi chỉ cấp nguồn USB, board đo được ___ V tại chân 5 V và ___ V tại chân 3,3 V. Nếu về sau mạch bị reset khi động cơ TT dùng chung đường 5 V này, giả thuyết là dòng kẹt kéo đường nguồn rơi vào vùng sụt áp (brownout). Biện pháp xử lý: tách pin động cơ riêng, chỉ nối chung mass, lắp tụ 100–470 µF đúng cực (vạch âm về mass) ngang chân VM, dùng dây động cơ đủ dày, nhấc bánh khỏi bàn, lập trình kéo PWM về 0 khi nguồn sụt hoặc mất lệnh quá khoảng 300 ms, và lắp cầu chì 2–3 A trên dây dương pin."*
5. Không gắn động cơ để thử nghiệm đoạn giả thuyết này. Bài lab đạt khi có đủ hai con số đo áp và đoạn giả thuyết đã hoàn thiện, lưu trong sổ với mã `ch01-09-brownout`.

Nếu ngay khi chỉ cắm USB mà chân 5 V đã lệch xa mức 5 V, hãy dừng lại và ghi chú ngay — đó là dấu hiệu bất thường của cáp hoặc board cần xử lý trước khi làm tiếp.

## Ví dụ

Với hai động cơ TT 1:48 chạy không tải ở mức trung bình:

$$
I_{\mathrm{chay}} = 2 \times 0{,}130 = 0{,}26\,\mathrm{A}
$$

So với định mức cổng USB $$0{,}50\,\mathrm{A}$$, phần dư khoảng $$0{,}24\,\mathrm{A}$$ khi bánh nhấc trên không rất dễ tạo cảm giác an toàn giả tạo. Khi xảy ra kẹt trục, dòng kẹt $$\gg 0{,}3\,\mathrm{A}$$ và chỉ một động cơ kẹt đã vượt quá khả năng cổng 500 mA. Sơ đồ nguồn đúng phải là: USB cấp cho ESP32/Pico và nguồn logic 3,3 V của TB6612; pin riêng (4,5–10 V) cấp vào chân VM; nối chung một điểm mass; mắc tụ 220 µF hoặc 470 µF (vạch âm về mass) sát chân VM; gắn cầu chì 2 A hoặc 3 A trên dây dương pin; và firmware đưa PWM về 0 nếu mất lệnh quá khoảng 300 ms.

Lưu ý không nên chọn cầu chì 0,5 A với hy vọng "bảo vệ kẹt trục", vì mức đó quá sát dòng vận hành sẽ ngắt liên tục khiến người dùng có xu hướng nối tắt bỏ qua cầu chì. Hãy chọn cầu chì 2–3 A để chống ngắn mạch, còn việc bảo vệ kẹt trục xử lý bằng cơ chế timeout trong phần mềm.

## Video tham khảo

- **Xem trước:** [What is ESD and How to Prevent it – ATM | Digi-Key Electronics](https://www.youtube.com/watch?v=pWhtyz-UFZc) — DigiKey, tiếng Anh. Giải thích tác hại của phóng tĩnh điện lên chân IC và thói quen xả tĩnh điện trước khi cầm mạch.
- [What is a fuse? the basics explained](https://www.youtube.com/watch?v=W770Z1yvXs8) — The Engineering Mindset, tiếng Anh. Minh họa nguyên lý ngắt mạch bảo vệ quá dòng của cầu chì.
- [The Best Protection for your Circuit is NOT a Fuse!.....but a Resettable Fuse? EB#54](https://www.youtube.com/watch?v=sF0KOVWj9p8) — GreatScott!, tiếng Anh. So sánh cầu chì thường với cầu chì tự phục hồi; lưu ý vẫn phải tính chọn dòng phù hợp theo bài học.

## Bài tập

1. Giả sử hai động cơ TT có dòng không tải 150 mA mỗi chiếc trên cổng USB 500 mA. Tính tổng dòng khi chạy không tải và phần dòng còn dư. Vì sao phần dư này không cho phép dùng USB nuôi chân VM khi bánh chạm sàn?
2. Khi chỉ cắm USB, chân 5 V đo được 4,95 V và chân 3,3 V đo được 3,28 V. Sang Chương 02, mỗi khi nối hai động cơ vào chính chân 5 V đó thì Serial Monitor lại in ra dòng chữ khởi động của mạch. Hãy viết một câu giả thuyết nguyên nhân và nêu cách thay đổi nguồn để kiểm chứng.
3. Một tụ hóa 470 µF mắc ngang chân VM bị cắm ngược với dải vạch hướng về phía cực dương (xa mass). Hậu quả gì có thể xảy ra và cần sửa như thế nào?
4. Trong lúc đang lái xe tiến, laptop chuyển sang chế độ ngủ khiến lệnh điều khiển ngừng gửi. Firmware cần làm gì sau khoảng 300 ms, và vì sao cầu chì 3 A không thay thế được đoạn mã này?
5. Một người nối chân `Echo` của HC-SR04 vào chân GP của Pico vì thấy "cảm biến chạy 5 V và Pico cũng có chân 5 V ngay bên cạnh". Giới hạn nào ở bài 07 cấm kết nối này, và bước kiểm tra nào giúp phát hiện sớm lỗi đảo ngược `VCC` với `GND` của cảm biến?

<details markdown="1">
<summary>Gợi ý đáp án</summary>

1. Tổng dòng không tải là $$2 \times 0{,}150 = 0{,}30\,\mathrm{A}$$, còn dư khoảng $$0{,}20\,\mathrm{A}$$ so với cổng 500 mA. Khi bánh chạm sàn hoặc kẹt trục, dòng tăng gấp nhiều lần và vượt xa phần dư này nên tuyệt đối không lấy USB cấp cho VM.
2. Giả thuyết: dòng khởi động/kẹt của động cơ kéo sụt đường nguồn 5 V dùng chung khiến đường 3,3 V tụt theo vào vùng reset (brownout). Kiểm chứng bằng cách chuyển động cơ sang nguồn pin riêng, giữ chung một điểm mass và chạy lại đúng lệnh đó xem thông báo khởi động có biến mất không.
3. Tụ hóa nhôm cắm ngược cực trên nguồn pin sẽ nóng mạnh và có nguy cơ xì bung hoặc nổ. Vạch in trên vỏ là cực âm và bắt buộc nối về mass; phải đảo đúng chiều tụ trước khi cấp nguồn.
4. Firmware phải tự động đưa duty PWM về 0 (và có thể hạ chân STBY) sau khoảng 300 ms không nhận lệnh mới. Cầu chì 3 A chỉ ngắt khi ngắn mạch hoặc quá dòng rất lớn chứ không ngắt ở dòng chạy bình thường, nên không thể tự dừng bánh xe.
5. Giới hạn điện áp cực đại tuyệt đối của chân GPIO (nằm ở mức 3,3 V chứ không phải 5 V) cấm nối thẳng chân Echo vào chân GP; chân 5 V bên cạnh là chân nguồn chứ không phải ngõ vào logic. Việc đo cực tính và kiểm tra điện áp giữa VCC và GND bằng đồng hồ trước khi cắm cảm biến sẽ phát hiện ngay lỗi đảo nguồn.

</details>

## Đọc thêm

- [SparkFun: mức logic](https://learn.sparkfun.com/tutorials/logic-levels) — giải thích dễ hiểu sự chênh lệch giữa ngõ ra 5 V và ngõ vào 3,3 V.
- [Battery University, BU-409](https://batteryuniversity.com/article/bu-409-charging-lithium-ion) — nắm vững quy tắc sạc pin lithium trước khi cấp nguồn cho chân VM.
- [Module TB6612FNG của Pololu](https://www.pololu.com/product/713) — minh họa kiến trúc tách biệt nguồn logic và nguồn động cơ giúp chống sụt áp.

## Mua ở Việt Nam

Pin động cơ, động cơ TT, mạch lái và cảm biến HC-SR04 đều nằm trong danh sách chung ở [BOM và cách mua bộ kit robot ở Việt Nam]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %}).

Nếu chưa có đồng hồ vạn năng để đo đường nguồn USB, bạn có thể tham khảo [UNI-T UT33D+ tại Hshop](https://hshop.vn/dong-ho-van-nang-dien-tu-digital-multimeter-uni-t-ut33d-chinh-hang) (kiểm tra giá hiện hành trước khi mua). Khi tới bước lắp tụ đệm VM, bạn có thể mua tụ hóa 100–470 µF (định mức 16 V hoặc 25 V) tại [Hshop](https://hshop.vn/), [Thế Giới IC](https://www.thegioiic.com/) hoặc [IC Đây Rồi](https://icdayroi.com/), và nhớ kiểm tra kỹ điện áp định mức cùng vạch cực âm trước khi hàn.
