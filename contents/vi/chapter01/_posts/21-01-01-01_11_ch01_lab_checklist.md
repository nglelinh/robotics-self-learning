---
layout: post
title: "Checklist lab chương 01"
chapter: "01"
order: 11
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter01
lesson_type: required
draft: false
---

Chương 01 chỉ thực sự hoàn tất khi sổ lab của bạn có đủ **bảy bằng chứng** cụ thể, mỗi bằng chứng đều có tiêu chí kiểm tra rõ ràng. Một dấu tick bên cạnh dòng chữ "tôi đã hiểu sơ đồ chân" không được tính là bằng chứng. Bài học này hướng dẫn bạn tự rà soát: thế nào là đạt thực chất, thế nào là đánh dấu hình thức, và cần quay lại bài nào khi một hạng mục chưa đạt. Bạn có thể hoàn thiện bảy cổng theo bất kỳ thứ tự nào, nhưng tuyệt đối không dùng ảnh của người khác thay thế cho phần mình còn thiếu.

## Mục tiêu

Sau bài học này, bạn sẽ tự đánh giá được đủ bảy cổng đầu ra của Chương 01 dựa trên hiện vật thực tế: phép tính điện trở LED ở 3,3 V, ảnh sơ đồ thanh nguồn breadboard, bảng năm điện trở đã giải mã và đo ngoài mạch, kết quả xác định cực tính bằng thang đo diode, ảnh mạch lái ghi rõ tên chip `TB6612` hoặc `DRV8833` (không ghi chung chung là "cầu H"), ảnh mối hàn (hoặc lịch hẹn làm bù nếu chưa có mỏ hàn), và đoạn phân tích sụt áp có nêu rõ nguồn pin động cơ riêng. Bạn cũng sẽ nhận diện được các dấu tick hình thức (thiếu số đo hoặc chụp nhầm chip) và chỉ ra đúng bài học cần mở lại để khắc phục.

## Kiến thức cần có

Các hiện vật cần kiểm tra được tạo ra từ bài 01 (phép tính LED) và chuỗi bài 07 đến 10. Nếu còn thiếu dụng cụ, xem lại danh sách mua sắm ở Chương 00 bài 05. Bạn chỉ cần chuẩn bị sổ lab và các ảnh chụp của mình; vẫn chưa chạy xe, luôn giữ bánh nhấc khỏi bàn và chưa nối động cơ.

---

Kết thúc Chương 01 là một cột mốc quan trọng: bạn đã đi từ định luật Ohm trên giấy tới việc tự tay nhận diện linh kiện, đo kiểm an toàn bằng đồng hồ vạn năng, hàn dây chắc chắn và bảo vệ mạch khỏi ngược cực hay sụt áp. **Checklist Chương 01** đóng vai trò bộ lọc kỹ thuật giúp bạn chắc chắn tầng điện–nguồn đã "sạch bóng lỗi" trước khi cắm bo vi điều khiển ESP32 hoặc Pico vào ở Chương 02.

## Bản đồ kiến thức nền: Bảy Cổng Kiểm soát Chất lượng Tầng Điện tử

1. **Cổng Nguồn & Thông mạch:** Không có chạm chập `VCC–GND`, điện áp các đường nguồn (pin, 5 V Buck, 3,3 V) nằm đúng dung sai $$\pm 5\%$$ cả lúc không tải lẫn lúc đóng tải giả.
2. **Cổng Linh kiện & Phân cực:** Đọc đúng điện trở (màu & SMD), xác định chính xác cực tính LED, diode và tụ hóa, kiểm chứng được mạch phân áp 5 V → 3,3 V bằng đồng hồ.
3. **Cổng Cơ–Điện & An toàn:** Mối hàn bóng chắc, có ống co nhiệt chống chập, cầu chì gắn đúng cực dương pin và dây nguồn động cơ tách riêng khỏi nhánh logic.

### Ví dụ cầm tay chỉ việc: Bảng nghiệm thu định lượng cho hệ nguồn trước khi cắm ESP32

Thay vì đánh dấu tick cảm tính, hãy điền và kiểm chứng đúng 4 con số đo thật sau trên bàn lab của bạn:

| Hạng mục nghiệm thu | Điều kiện đo | Ngưỡng đạt chuẩn | Ví dụ kết quả ĐẠT |
|---|---|---|---|
| **1. Thông mạch `5V–GND` (tắt nguồn)** | Thang Ohm / Thông mạch | Không kêu bíp, $$R > 1\text{ k}\Omega$$ | $$R = 14.2\text{ k}\Omega$$ |
| **2. Đầu ra mạch Buck 5 V (không tải)** | Thang DC V (20 V) | $$[4.85\text{ V},\ 5.15\text{ V}]$$ | $$5.02\text{ V}$$ |
| **3. Sụt áp Buck khi đóng tải $$500\text{ mA}$$** | Mắc tải giả $$10\ \Omega / 5\text{ W}$$ | $$\Delta V < 0.15\text{ V}$$ | $$4.96\text{ V}$$ ($$\Delta V = 0.06\text{ V}$$) |
| **4. Mạch phân áp 5 V → 3,3 V** | Cấp 5,02 V vào đầu trên | $$[3.0\text{ V},\ 3.45\text{ V}]$$ | $$3.26\text{ V}$$ |

Chỉ cần **một** trong 4 chỉ số trên trượt ngưỡng (ví dụ Buck ra $$6.8\text{ V}$$ do chưa vặn biến trở chỉnh áp!), bạn đã tự cứu sống bo ESP32 trị giá hàng trăm nghìn đồng trước khi cắm nó vào!

### Khung giải thích: 4 bước vượt qua cổng kiểm tra Chương 01 trung thực (nên đọc chậm)

1. **Bước 1 — Không bao giờ "tick hình thức":** Mọi hạng mục chưa có số đo ghi trong sổ lab đều coi là *chưa đạt*.
2. **Bước 2 — Kiểm tra lặp lại sau khi rung lắc nhẹ cụm dây:** Cầm nhẹ cụm dây nguồn lắc qua lại trong khi đồng hồ vẫn kẹp đo điện áp — nếu số đo nhảy loạn xạ, mối hàn hoặc đầu nối đang lỏng.
3. **Bước 3 — Chụp lại ảnh mặt trên và mặt dưới mạch vừa hàn:** Ảnh chụp sắc nét là bằng chứng tuyệt vời giúp bạn tự soi cầu thiếc (solder bridge) khi phóng to trên màn hình.
4. **Bước 4 — Lưu sơ đồ phân bổ đường nguồn vào thư mục `docs/`:** Sang Chương 02, bạn sẽ nối thẳng bo vi điều khiển vào đúng các đầu chờ đã kiểm chứng này.

**Kiểm tra nhanh.** Tại sao khi kiểm tra điện áp đầu ra của mạch Buck mới mua (loại có biến trở chỉnh áp như LM2596/MP1584), ta **bắt buộc** phải đo và vặn chỉnh về 5,0 V *trước* khi nối vào bo mạch robot? Vì nhiều mạch Buck xuất xưởng đang để mức áp mặc định gần bằng $$V_{\text{in}}$$ (7–8 V) — cắm thẳng vào sẽ đốt cháy ngay toàn bộ mạch 5 V và 3,3 V!

---

## Vì sao bài này quan trọng

Xe Capstone là hệ dẫn động vi sai dùng ESP32 hoặc Pico 3,3 V, mạch lái TB6612 hoặc DRV8833, hai động cơ TT dùng pin riêng và cảm biến HC-SR04 có chân echo 5 V. Sang Chương 02 bạn sẽ bắt đầu lắp ráp và cấp điện cho các khối này. Nếu sơ đồ breadboard chỉ là ảnh board trống không đánh dấu, bạn dễ tốn cả buổi chiều gỡ lỗi đèn LED không sáng; nếu ảnh driver chỉ ghi "cầu H", rất dễ quên kéo chân `STBY` khiến bánh đứng yên; nếu chưa nắm vững đoạn phân tích sụt áp, hiện tượng mạch reset khi dùng chung nguồn USB sẽ bị nhầm thành lỗi chương trình. Buổi rà soát này giúp bạn phát hiện sớm mọi lỗ hổng ngay trên sổ ghi chép.

## Cách kiểm tra một hạng mục

Mỗi cổng kiểm tra gồm một **hiện vật cụ thể** (phép tính có đơn vị, ảnh chụp có chú thích chữ, đoạn phân tích kèm số đo) và một **tiêu chí đối chiếu** rõ ràng (nằm trong dung sai, vạch tụ được gọi là âm, đọc rõ mã IC, có cụm từ "pin động cơ riêng"). Ngược lại, **dấu tick hình thức** là khi chỉ đánh dấu hoàn thành nhưng thiếu phép đối chiếu — ví dụ ghi "xong" không kèm số ohm, "đã chụp" nhưng ảnh mờ không đọc được tên chip, hay "đã hiểu sụt áp" mà không có phân tích. Mọi mục hình thức đều được tính là `chưa đạt` (còn mở).

Khi có cổng chưa đạt, hướng xử lý rất gọn: mở lại đúng bài học tương ứng, làm lại đúng bước tạo hiện vật và ghi ngày cập nhật mới (không cần làm lại cả chương). Tuyệt đối không chuyển sang chạy thử động cơ ở Chương 02 khi cổng nhãn driver hoặc cổng phân tích sụt áp vẫn còn mở, vì hai cổng này liên quan trực tiếp đến nguy cơ hỏng phần cứng. Ngoại lệ duy nhất là trường hợp chưa có mỏ hàn: bạn được phép ghi một ngày hẹn cụ thể để thực hành bù và coi lịch hẹn đó là hiện vật tạm thời.

## Bảy cổng kiểm tra đầu ra

**1. Phép tính điện trở LED ở 3,3 V.** Trình bày đầy đủ phép tính chọn điện trở cho đèn LED báo trạng thái nối vào chân GPIO, ghi rõ điện áp thuận $V_F$ sử dụng (với LED đỏ, có thể lấy $$V_F = 2{,}0\,\mathrm{V}$$ nếu chưa đo ở bài 10). Ví dụ với điện trở 220 Ω:

$$
I = \frac{3{,}3 - 2{,}0}{220} = \frac{1{,}3}{220} \approx 5{,}9\,\mathrm{mA}
$$

*Tiêu chí đạt:* Có đủ công thức, bước thay số, kết quả kèm đơn vị mA, và nhận xét dòng này nằm trong dải an toàn 5–10 mA cho LED nhỏ và GPIO 3,3 V (tốt nhất dùng đúng $V_F$ đã đo ở bài 10). Lấy thẳng 3,3 V chia cho điện trở mà bỏ quên $V_F$ sẽ bị tính là trượt. Với LED xanh có $V_F$ cao, kết quả dòng quá nhỏ chỉ đạt nếu bạn nhận xét đèn sẽ mờ và đề xuất đổi màu LED hoặc giảm điện trở phù hợp.

**2. Sơ đồ thanh nguồn breadboard.** Ảnh chụp hoặc bản vẽ từ bài 10 thể hiện rõ nút năm lỗ, rãnh giữa cách điện và tình trạng từng thanh nguồn (liền mạch hay bị ngắt đôi ở giữa). *Tiêu chí đạt:* Người khác chỉ cần nhìn bản vẽ này vẫn cắm đúng nút bạn định; ảnh chụp breadboard trống không có chú thích sẽ trượt.

**3. Bảng năm điện trở (vừa giải mã vừa đo).** Đủ 5 dòng, mỗi dòng có dãy màu vạch, trị số danh định, dung sai và số đo ngoài mạch, kèm kết luận đạt/trượt theo cửa sổ dung sai. Thiếu màu vạch, thiếu số đo, đo khi còn gắn trong mạch hoặc chỉ làm 4 dòng đều bị tính là trượt.

**4. Xác định cực tính bằng thang đo diode.** Kết quả đo một LED hoặc một diode kèm số điện áp thuận và câu kết luận rõ ràng dạng "chân này là anode". *Tiêu chí đạt:* Người khác có thể nối đúng LED đó từ 3,3 V qua điện trở của cổng 1 (anode về phía GPIO, cathode về mass) mà không cần hỏi thêm. Lưu ý: việc nhận diện vạch cực âm tụ hóa vẫn cần có trong sổ bài 10 và tuân thủ ở bài 09, nhưng không thay thế được phép đo diode của cổng 4.

**5. Ảnh mạch lái động cơ có ghi rõ tên chip.** Ảnh chụp module mạch lái trên đó bạn chú thích rõ `TB6612` hoặc `DRV8833` kèm tên các chân điều khiển tương ứng (với TB6612 tối thiểu có `AIN1`, `AIN2`, `PWMA`, `STBY`). Các nhãn chung chung như "cầu H", "mạch động cơ" hay "board nhỏ" đều trượt dù ảnh rất nét. Nếu module chưa về tới, mục này được ghi dạng `dry-run` có ngày và nêu rõ loại chip đã đặt mua.

**6. Ảnh mối hàn hoặc lịch thực hành bù.** Ảnh mối hàn tập từ bài 08 kèm kết quả đo thông mạch và đối chiếu với hình mối hàn chuẩn. Mối kêu bíp nhưng vo cục, hoặc mối trông bóng nhưng hở mạch đều trượt. Nếu chưa có mỏ hàn, ghi rõ ngày hẹn thực hành bù kèm quy tắc an toàn giá đỡ và kính bảo hộ. Chụp ảnh mối hàn nhà máy có sẵn trên module mua về rồi nhận là bài tập của mình sẽ tính là trượt.

**7. Đoạn phân tích sụt áp (brownout).** Ghi chú từ bài 09 có số đo chân 5 V và 3,3 V khi chỉ cắm USB (nếu đã đo được), giả thuyết mạch reset do động cơ kéo sụt đường nguồn dùng chung, và đủ các giải pháp: pin động cơ riêng, chỉ nối chung mass, tụ 100–470 µF đúng cực ngang VM, dây đủ dày, nhấc bánh khỏi bàn, và firmware kéo PWM về 0 khi nguồn sụt hoặc mất lệnh quá khoảng 300 ms. Bất kỳ đoạn viết nào cho phép động cơ TT lấy nguồn từ chân 5 V của ESP32 đều trượt ngay lập tức. Bạn có thể ghi kèm lệnh cấm nối thẳng echo 5 V của HC-SR04 vào GPIO 3,3 V, nhưng câu này không thay thế được phần tách pin động cơ.

## Nhận diện các dấu tick hình thức

Đối chiếu với bảy cổng trên: ghi "Điện trở: xong" trượt cổng 3 (thiếu giải mã và số đo); "Cực tính ổn" trượt cổng 4 (không ghi rõ anode và điện áp thuận); "Driver: cầu H trong kit" trượt cổng 5 (sang Chương 02 không phân biệt được `STBY` của TB6612 với `nSLEEP` của DRV8833); "Đã hiểu cách hàn" trượt cổng 6 (không có ảnh lẫn ngày hẹn); "Sụt áp: động cơ ăn nhiều dòng" trượt cổng 7 (thiếu tách pin riêng, mass chung và ngưỡng cắt PWM 300 ms). Cách sửa không phải là viết thêm lời giải thích dài dòng, mà là bổ sung đúng hiện vật cổng yêu cầu.

Khi dụng cụ đã có sẵn, việc bổ sung mỗi cổng trượt rất nhanh: cổng 3 chỉ cần đo lại năm điện trở; cổng 5 chỉ mất vài phút tra trang Pololu/TI để ghi lại đúng tên chân; cổng 6 nếu chưa có mỏ hàn thì đặt mua theo bài 08 và chốt ngày thực hành bù.

## Thực hành

Đây là buổi tự kiểm tra; chỉ lắp lại mạch khi cần tạo lại một hiện vật bị trượt.

1. Mở sổ lab và kẻ bảng gồm 7 dòng tương ứng với 7 cổng.
2. Cổng 1: viết lại đầy đủ phép tính LED 3,3 V trên một dòng mới (ngay cả khi bài 01 đã tính).
3. Đính kèm sơ đồ breadboard, bảng năm điện trở và kết quả xác định cực tính ở thang diode; sửa ngay bất kỳ mục nào không qua được tiêu chí đối chiếu.
4. Chú thích rõ mã IC (`TB6612` hoặc `DRV8833`) lên ảnh mạch lái (hoặc ghi `dry-run` kèm ngày dự kiến nhận hàng).
5. Xem kỹ lại ảnh mối hàn dưới ánh sáng tốt; nếu mối vo cục thì làm lại trước khi chấm, hoặc ghi ngày hẹn bù nếu chưa có mỏ hàn.
6. Đọc lại đoạn phân tích sụt áp và kiểm tra chắc chắn có đủ ba từ khóa cốt lõi: "pin động cơ riêng", "mass chung" và "300 ms".
7. Đánh dấu `đạt` hoặc `trượt` cho từng cổng, lưu trang với mã `ch01-11-audit` kèm ngày kiểm tra. Với mỗi cổng trượt, ghi rõ số thứ tự bài học sẽ mở lại để sửa.

Toàn bộ buổi rà soát này không cấp nguồn quay bánh xe.

## Ví dụ

Giả sử một trang sổ ghi như sau: *"Điện trở LED xong. Ảnh breadboard đính kèm, không đánh dấu. Đo ba điện trở, hai con trông đúng. Cực tính: vạch chắc là âm. Driver là cầu H. Hàn tuần sau có lẽ. Sụt áp: đừng để mô-tơ kẹt."*

Kết quả chấm từng cổng:
- **Cổng 1 trượt:** chỉ ghi "xong", không có phép tính.
- **Cổng 2 trượt:** ảnh breadboard trống không chú thích không phải sơ đồ thanh nguồn.
- **Cổng 3 trượt:** mới đo ba con thay vì năm con, và "trông đúng" không phải đối chiếu giải mã với số đo.
- **Cổng 4 trượt:** đoán vạch tụ hóa không thay thế được phép đo cực tính bằng thang diode.
- **Cổng 5 trượt:** nhãn "cầu H" không nêu rõ mã chip và tên chân.
- **Cổng 6 chưa đạt:** "tuần sau có lẽ" cần đổi thành một ngày cụ thể mới thành lịch bù hợp lệ.
- **Cổng 7 trượt:** thiếu pin riêng, thiếu mass chung, thiếu tụ đệm và thiếu quy tắc ngắt PWM 300 ms.

Hướng sửa cho buổi kế tiếp: làm lại thực tế trên bàn các cổng 1, 3, 4 và viết lại đoạn cổng 7; bổ sung chú thích lên ảnh cho cổng 2 và 5; chốt một ngày cụ thể cho cổng 6.

## Video tham khảo

- **Xem trước:** [Ohms Law Explained - The basics circuit theory](https://www.youtube.com/watch?v=HsLLq6Rm5tU) — The Engineering Mindset, tiếng Anh. Ôn lại nhanh định luật Ohm và công suất trước khi chốt checklist Chương 01.

## Bài tập

Mỗi tình huống dưới đây là một trích đoạn sổ lab chưa đạt. Hãy chỉ ra cổng nào trượt, thiếu thông tin gì và cách sửa gọn nhất:

1. *"$$3{,}3 / 180 = 18\,\mathrm{mA}$$, LED sẽ sáng."* — Thuộc cổng nào, và phép tính đã bỏ quên đại lượng nào?
2. *"Năm điện trở: 220, 1k, 10k, 330, 470. Đều tốt."* — Thuộc cổng nào, và thiếu nửa bằng chứng nào?
3. *"Chế độ diode: đồng hồ kêu bíp nên cực tính ổn."* — Thuộc cổng nào, và vì sao tiếng kêu chứng tỏ dùng sai chức năng?
4. *"Ảnh lưu driver.jpg. Đây là cầu H mua trên Shopee, chân đấu như video."* — Cổng nào trượt, và cần ghi rõ tên mã nào để đạt?
5. *"Mối hàn trông ổn, không có ảnh, mỏ hàn ở tiệm đến 15h thứ Sáu mới lấy. Đoạn sụt áp ghi cả hai mô-tơ TT dùng chung chân 5 V của ESP32 cho gọn dây, chân echo cắm thẳng vào GPIO 4."* — Cổng nào trượt, cổng nào có thể tính là lịch bù, và chi tiết nào thực sự gây nguy hiểm phần cứng?

<details markdown="1">
<summary>Gợi ý đáp án</summary>

1. Cổng 1 trượt do bỏ quên điện áp thuận $V_F$ của LED nên 18 mA không phải dòng thực tế. Sửa lại thành $$I = (3{,}3 - V_F) / 180$$ có nêu rõ $V_F$ (ví dụ với $$V_F = 2{,}0\,\mathrm{V}$$ thì dòng khoảng $$7{,}2\,\mathrm{mA}$$).
2. Cổng 3 trượt vì mới ghi trị số danh định mà thiếu toàn bộ 5 con số đo thực tế bằng đồng hồ ngoài mạch (và nhận xét dung sai).
3. Cổng 4 trượt vì tiếng kêu bíp thuộc thang thông mạch chứ không phải thang đo diode. Cần đo lại ở thang diode để ghi điện áp thuận và xác định rõ chân anode.
4. Cổng 5 trượt. Cần ghi rõ tên chip là `TB6612` hoặc `DRV8833` kèm tên chân tương ứng, bởi "cầu H" và "như video" không phân biệt được chân `STBY` hay `nSLEEP`.
5. Cổng 6 có thể tính là lịch bù nếu ghi rõ ngày dương lịch cho mốc "15h thứ Sáu" và cam kết bổ sung ảnh mối hàn sau đó. Cổng 7 trượt nặng và rất nguy hiểm: tuyệt đối không cấp nguồn hai động cơ TT từ chân 5 V của ESP32 và không cắm thẳng echo 5 V vào GPIO 4; cần sửa lại theo bài 09 và lệnh cấm ở bài 07.

</details>

## Đọc thêm

- [Module TB6612FNG của Pololu](https://www.pololu.com/product/713) — đối chiếu tên chip và sơ đồ chân cho cổng 5 nếu dùng TB6612.
- [TI DRV8833](https://www.ti.com/product/DRV8833) — tài liệu tên chân cho phương án DRV8833 (tránh nhầm với sơ đồ TB6612).
- [Datasheet ESP32 (PDF)](https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf) — căn cứ giới hạn 3,3 V đứng sau cổng 1 và cổng 7.
- [Hướng dẫn hàn của Adafruit](https://learn.adafruit.com/adafruit-guide-excellent-soldering) — tiêu chuẩn hình dạng mối hàn để tự chấm cổng 6.

## Mua ở Việt Nam

Không cần lập thêm bộ kit mới; chỉ đối chiếu các cổng còn mở với bài [BOM và cách mua bộ kit robot ở Việt Nam]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %}) và mua đúng phần còn thiếu.

Nếu thiếu dụng cụ hàn cho cổng 6 (giá tham khảo Hshop ngày 23 tháng 9 năm 2026): [mỏ hàn 60 W](https://hshop.vn/mo-han-60w-wadfow-wel3616-soldering-iron) 75.000 ₫, [giá đỡ](https://hshop.vn/de-gac-mo-han-tron-b-2-co-khay-roi) 40.000 ₫ và [cuộn thiếc Sn63 0,8 mm](https://hshop.vn/thiec-han-sunchi-kp26-0-8mm-sn63-pb37-solder-wire) 24.000 ₫. Nếu thiếu breadboard cho cổng 2: [CAMMB-102](https://hshop.vn/test-board-cammb-102) 35.000 ₫. Nếu thiếu đồng hồ cho cổng 3 và 4: [UNI-T UT33D+](https://hshop.vn/dong-ho-van-nang-dien-tu-digital-multimeter-uni-t-ut33d-chinh-hang). Điện trở và LED lẻ có thể mua tại [Hshop](https://hshop.vn/), [Thế Giới IC](https://www.thegioiic.com/) hoặc [IC Đây Rồi](https://icdayroi.com/).
