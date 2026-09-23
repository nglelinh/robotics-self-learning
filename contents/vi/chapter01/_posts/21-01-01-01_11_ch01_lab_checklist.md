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

Chương 01 khép khi bảy bằng chứng đã ở trong sổ, mỗi bằng chứng hỏng theo một cách chỉ tay được. Dấu tích cạnh câu "tôi hiểu sơ đồ chân" không phải bằng chứng. Bài này là buổi kiểm: thế nào là đạt thật, thế nào là dấu tích cho có, và đường quay lại khi một dòng còn mỏng. Các cổng làm theo thứ tự nào cũng được. Không được lấy ảnh của người khác thế vào chỗ mình thiếu.

## Mục tiêu

Bạn chấm bảy cổng bằng hiện vật, không bằng cảm giác đã xong: một phép tính điện trở LED ở 3,3 V, một ảnh sơ đồ rail breadboard, năm điện trở vừa giải mã vừa đo, một lời gọi cực đã xác nhận bằng chế độ diode, một ảnh driver ghi TB6612 hoặc DRV8833 chứ không ghi "cầu H", một ảnh mối hàn hoặc một lịch bù nếu chưa có mỏ, và một đoạn sụt áp có nói pin động cơ riêng. Bạn nhận ra dấu tích cho có, ví dụ dấu xong mà không có số, hoặc ảnh chụp nhầm chip, và bạn gọi tên đúng một bài để sửa. Bạn nhận một trang sổ cẩu thả và nói cổng nào trượt.

## Kiến thức cần có

Bài 07 đến 10 tạo ra hiện vật mà trang này soi, bài 01 tạo ra phép tính LED. Thiếu đồ thì danh sách mua là chương 00 bài 05. Cần sổ và ảnh của bạn. Vẫn chưa cần xe chạy. Bánh để trên không. Không nối mô-tơ để ăn mừng.

## Vì sao bài này quan trọng

Capstone là xe dẫn động vi sai trên ESP32 hoặc Pico 3,3 V, một TB6612 hoặc DRV8833, hai mô-tơ TT với pin riêng, và HC-SR04 có echo 5 V. Chương 02 bắt đầu gắn các món ấy. Sơ đồ rail chỉ là ảnh breadboard trống thì LED tối sẽ ngốn một buổi chiều. Ảnh driver chỉ ghi "cầu H" thì STBY không bao giờ được kéo và bánh đứng yên. Đoạn sụt áp chưa được viết thì reset lúc mô-tơ dùng chung USB trông như chương trình bị ma. Buổi kiểm là cách thấy các lỗ ấy khi thứ duy nhất đang "chạy" là cuốn sổ.

## Kiểm một dòng thế nào

Một cổng có hiện vật và một phép thử làm được mà không phải hỏi giảng viên định nói gì. Hiện vật là một phép tính có đơn vị, một ảnh có chữ, hoặc một đoạn có con số. Phép thử là một so sánh: nằm trong cửa sổ dung sai, vạch được gọi là âm, tên chip đọc được, đoạn văn có chữ "pin động cơ riêng". Dấu tích cho có thì có dấu, thiếu phép so sánh. "Xong" mà không có ohm, "đã chụp" một board không chữ, và "đã hiểu sụt áp" mà không có câu, là ba kiểu dấu cho có mà chương này hay gặp. Chúng tính là còn mở. Không tính là gần đạt.

Đường sửa thì cố ý ngắn. Mở lại đúng bài ghi trên cổng, làm lại đúng bước tạo ra hiện vật, và ghi ngày file mới. Đừng viết lại cả chương, và đừng bắt đầu cho xe chạy ở chương 02 khi đoạn sụt áp hoặc nhãn driver vẫn là dấu cho có. Hai cổng ấy là chỗ làm hỏng linh kiện hoặc giả dạng lỗi phần mềm. Ngoại lệ là chưa có mỏ: được hẹn một buổi bù, và tờ hẹn là hiện vật cho đến khi mối hàn tồn tại.

## Bảy cổng

**1. Phép tính LED ở 3,3 V.** Viết số cho LED trạng thái sẽ treo trên GPIO. Chọn một điện áp thuận và cho thấy nó. LED đỏ, $$V_F = 2{,}0\,\mathrm{V}$$ là chấp nhận được nếu bài 10 chưa đo. Với điện trở 220 Ω,

$$
I = \frac{3{,}3 - 2{,}0}{220} = \frac{1{,}3}{220} \approx 5{,}9\,\mathrm{mA}
$$

Đạt: biểu thức, phép thế, kết quả bằng miliampe, và một câu nói dòng này nằm trong dải 5–10 mA mà LED nhỏ và GPIO 3,3 V sống được. Dùng $$V_F$$ đo ở bài 10 thì tốt hơn, nếu bạn ghi ra. Lấy 3,3 chia điện trở mà quên $$V_F$$ thì trượt, chữ đẹp cũng vậy. Kết quả gần không với LED xanh chỉ đạt nếu bạn nói LED sẽ mờ và chọn màu khác hoặc điện trở nhỏ hơn.

**2. Sơ đồ rail breadboard.** Ảnh hoặc bản phác từ bài 10 cho thấy một nút năm lỗ, rãnh giữa hở, và mỗi rail nguồn liền hay bị chia. Đạt: người khác chỉ nhìn tờ ấy vẫn cắm đúng nút bạn định. Ảnh board trống không chữ thì trượt.

**3. Năm điện trở, vừa giải vừa đo.** Năm dòng, mỗi dòng có màu, trị danh định, dung sai, và số đo ngoài mạch, đánh đạt hoặc trượt theo cửa sổ. Có mã màu mà không có số đo thì trượt. Có số đo mà không có màu thì trượt. Đo khi điện trở còn trong mạch thì trượt. Bốn dòng tốt và dòng thứ năm trống không phải "gần xong".

**4. Một lời gọi cực bằng chế độ diode.** LED hoặc diode, có điện áp thuận và một câu dạng "chân này là anode". Đạt: người lạ nối được LED ấy từ 3,3 V qua điện trở của cổng 1, anode về phía GPIO, cathode về mass, không phải hỏi bạn. Ảnh không chữ thì trượt. Nói vạch tụ hóa "chắc là âm" không xong cổng này; cổng này là lời gọi bằng chế độ diode. Vạch tụ vẫn phải có trong sổ bài 10, và bài 09 không chấp nhận tụ VM cắm ngược.

**5. Ảnh driver, có tên.** Ảnh module lái mô-tơ trên đó bạn đã viết TB6612 hoặc DRV8833, kèm tên chân của đúng chip ấy: với TB6612, ít nhất AIN1, AIN2, PWMA và STBY. "Cầu H", "mạch mô-tơ", hoặc "cái board nhỏ" đều trượt dù ảnh nét. Module chưa về thì dòng này là dry-run có ngày, ghi chip bạn đã đặt. Hình chữ nhật không tên chip là dấu cho có.

**6. Mối hàn, hoặc lịch bù.** Ảnh mối của bạn từ bài 08, có ghi thông mạch, đối chiếu vành tốt trong hình mối hàn. Kêu mà thành cục thì trượt. Mối đẹp mà hở thì trượt. Chưa có mỏ thì ghi ngày sẽ làm lab và dòng đế-với-kính bạn sẽ tuân. Lịch đó là sự chậm thật. Ảnh mối nhà máy trên module mua về, nhận là của mình, không phải sự chậm. Đó là trượt.

**7. Đoạn sụt áp.** Ghi chú bài 09, có số 5 V và 3,3 V lúc chỉ cắm USB nếu bạn đo được, giả thuyết lần reset sau là mô-tơ kéo sụt rail dùng chung, và cách xử lý: pin động cơ riêng, chỉ chung mass, tụ 100–470 µF trên VM, dây dày, bánh nhắc, PWM về 0 nếu rail sụt hoặc lệnh im khoảng 300 ms. Đoạn cho mô-tơ TT ăn chân 5 V của ESP32 thì trượt dù câu văn gọn. Lệnh cấm echo của HC-SR04, 5 V vào GPIO 3,3 V, được phép ngồi cùng ghi chú; thiếu câu ấy không tự làm trượt cổng này, và có câu ấy không tha cho đoạn thiếu pin.

## Dấu tích cho có trông thế nào

Đối chiếu với các cổng. "Điện trở: rồi" trượt cổng 3, vì không giải mã và không đo. "Cực tính ổn" trượt cổng 4, vì không chân nào được gọi là anode và không có điện áp. "Driver: cầu H trong kit" trượt cổng 5, vì chương 02 không tách được STBY khỏi chân sleep của DRV8833. "Đã hiểu hàn" trượt cổng 6, vì không ảnh cũng không ngày. "Sụt áp: mô-tơ ngốn dòng" trượt cổng 7, vì thiếu pin riêng, mass chung, và nhát cắt PWM 300 ms. Sửa không phải là thêm tính từ. Sửa là hiện vật mà cổng đã nêu.

Khi đồ đã ở trên bàn, sửa gọn trong một buổi. Cổng 3 là đo lại, không phải một chương lý thuyết mới. Cổng 6 chưa có mỏ thì mua theo danh sách bài 08 và ghi ngày, không phải viết lại định nghĩa mối lõm. Cổng 5 ghi sai tên thì mười phút với trang Pololu hoặc trang TI và một nhãn mới. Đừng mở lab cho xe chạy để "theo kịp".

## Thực hành

Buổi này là buổi kiểm. Chỉ dựng mạch mới khi phải thay một hiện vật đã trượt.

1. Mở sổ và kẻ bảy dòng, mỗi cổng một dòng.
2. Cổng 1: viết lại phép tính LED 3,3 V trên một dòng mới, dù bài 01 đã có dòng tương tự.
3. Gắn sơ đồ rail, bảng năm điện trở, và dòng cực tính chế độ diode. Dòng nào trượt phép thử thì sửa trước khi chấm.
4. Ghi tên chip lên ảnh driver. Board chưa có thì viết dry-run và ngày bạn chờ nó về.
5. Soi lại ảnh mối dưới đèn. Vành thành cục thì làm lại trước khi chấm, hoặc ghi ngày bù nếu vẫn chưa có mỏ.
6. Đọc đoạn sụt áp một lần và gạch dưới "riêng", "mass chung", và "300 ms". Thiếu chữ nào thì thêm từ bài 09, đừng bịa một câu mềm hơn.
7. Đánh mỗi cổng đạt hoặc trượt. Ghi ngày trang `ch01-11-audit`. Dòng trượt phải nêu bài sẽ mở lại.

Trong buổi kiểm không bánh nào quay.

## Ví dụ

Một trang ghi: "Điện trở LED xong. Ảnh breadboard đính kèm, không đánh dấu. Đo ba điện trở, hai con trông đúng. Cực tính: vạch chắc là âm. Driver là cầu H. Hàn tuần sau có lẽ. Sụt áp: đừng để mô-tơ kẹt."

Cổng 1 trượt, hoặc cùng lắm là dở dang, vì trang không có phép tính. "Xong" là dấu cho có. Cổng 2 trượt: ảnh breadboard không chữ không phải sơ đồ rail. Cổng 3 trượt: ba số đo không phải năm, và "trông đúng" không phải giải mã cộng đồng hồ. Cổng 4 trượt: đoán vạch tụ hóa không phải lời gọi anode bằng chế độ diode. Cổng 5 trượt: "cầu H" là nhãn bị cấm. Cổng 6 chưa đạt; "tuần sau có lẽ" chỉ thành lịch bù khi một ngày thật thay chữ "có lẽ". Cổng 7 trượt: không pin riêng, không mass chung, không tụ, không nhát 300 ms. Trang không đậu nhờ thành thật. Giờ tiếp theo là cổng 1, 3 và 4 trên bàn, cộng đoạn viết lại cho cổng 7. Cổng 2 và 5 cần một cây bút trên ảnh. Cổng 6 cần một ngày.

## Bài tập

Mỗi mục là một mẩu sổ cẩu thả. Nói cổng nào trượt, thiếu gì, và sửa nhỏ nhất là gì.

1. "$$3{,}3 / 180 = 18\,\mathrm{mA}$$, LED sẽ sáng." Cổng nào, và phép tính đã bỏ số hạng nào?
2. "Năm điện trở: 220, 1k, 10k, 330, 470. Đều tốt." Cổng nào, và nửa bằng chứng nào vắng mặt?
3. "Chế độ diode: nó kêu, nên cực tính ổn." Cổng nào, và vì sao tiếng kêu là sai chức năng?
4. "Ảnh lưu driver.jpg. Đây là cầu H mua trên Shopee, chân đấu như video." Cổng nào trượt, và hai từ nào đã đủ cho nhãn đạt?
5. "Mối trông ổn, không ảnh, mỏ ở shop đến 15h thứ Sáu. Đoạn sụt áp nói cả hai mô-tơ TT dùng chung chân 5 V của ESP32 cho gọn dây, echo cắm thẳng GPIO 4." Cổng nào trượt, cổng nào được là lịch bù, và câu nào nguy hiểm chứ không chỉ thiếu?

<details markdown="1">
<summary>Gợi ý đáp án</summary>

1. Cổng 1 trượt. Điện áp thuận của LED bị bỏ, nên 18 mA không phải dòng qua điện trở. Viết lại $$I = (3{,}3 - V_F) / 180$$ với $$V_F$$ được nêu. $$V_F = 2{,}0\,\mathrm{V}$$ thì dòng khoảng $$7{,}2\,\mathrm{mA}$$, mức đó tin được là đạt.
2. Cổng 3 trượt. Trị danh định có, số đo thì không. "Đều tốt" không thay năm số ohm đo ngoài mạch.
3. Cổng 4 trượt. Tiếng thông mạch không phải chế độ diode. Sửa là một điện áp thuận và một anode được gọi tên. Tiếng kêu chỉ nói chân chưa đứt.
4. Cổng 5 trượt. Nhãn đạt là TB6612 hoặc DRV8833, kèm tên chân của chính chip đó. "Cầu H" và "như video" không chỉ ra STBY hay nSLEEP.
5. Cổng 6 được tính là lịch bù nếu "15h thứ Sáu" được ghi thành ngày và ảnh mối vẫn còn bị đòi lúc đó. Cổng 7 trượt, và câu ấy nguy hiểm: mô-tơ TT không được ăn chân 5 V của ESP32, echo không được rơi vào GPIO 4. Sửa đoạn theo bài 09 và lệnh cấm echo theo bài 07. Đừng coi câu ấy là suýt đạt.

</details>

## Đọc thêm

- [Module TB6612FNG của Pololu](https://www.pololu.com/product/713) — nhãn và tên chân mà cổng 5 cần khi chip là TB6612.
- [TI DRV8833](https://www.ti.com/product/DRV8833) — nhãn hợp lệ còn lại. Đừng trộn tên chân của nó với tờ TB6612.
- [Datasheet ESP32 (PDF)](https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf) — giới hạn 3,3 V đứng sau cổng 1 và cổng 7.
- [Hướng dẫn hàn của Adafruit](https://learn.adafruit.com/adafruit-guide-excellent-soldering) — chuẩn vành thiếc cho cổng 6, đặt cạnh hình mối của khóa này.

## Mua ở Việt Nam

Đừng dựng bộ kit thứ hai. So các cổng còn mở với chương 00, bài 05, [BOM và cách mua bộ kit robot ở Việt Nam]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %}), và chỉ mua chỗ thiếu.

Cổng 6, nếu thiếu mỏ, dùng trang bài 08 và giá ngày 23 tháng 9 năm 2026: [mỏ 60 W](https://hshop.vn/mo-han-60w-wadfow-wel3616-soldering-iron) 75.000₫, [đế](https://hshop.vn/de-gac-mo-han-tron-b-2-co-khay-roi) 40.000₫, và [cuộn Sn63 0,8 mm](https://hshop.vn/thiec-han-sunchi-kp26-0-8mm-sn63-pb37-solder-wire) 24.000₫. Cổng 2, nếu chưa có breadboard, là [CAMMB-102](https://hshop.vn/test-board-cammb-102) 35.000₫. Thiếu đồng hồ cho cổng 3 và 4 thì [UNI-T UT33D](https://hshop.vn/dong-ho-van-nang-dien-tu-digital-multimeter-uni-t-ut33d-chinh-hang). Điện trở hoặc LED lẻ, không bịa slug mới: [Hshop](https://hshop.vn/), [Thế Giới IC](https://www.thegioiic.com/), [IC Đầy Rồi](https://icdayroi.com/).
