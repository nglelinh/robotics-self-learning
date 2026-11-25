---
layout: post
title: "Đọc datasheet và sơ đồ chân"
chapter: "01"
order: 7
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter01
lesson_type: required
draft: false
---

Datasheet là tài liệu kỹ thuật duy nhất có giá trị quyết định xem một kết nối dây có hợp lệ hay không. Bài học này thiết lập một trình tự đọc datasheet chuẩn gồm sáu bước, sau đó áp dụng trực tiếp cho module lái động cơ TB6612FNG của xe hai bánh và giới hạn chân GPIO trên ESP32 trước xung echo 5 V.

## Mục tiêu

Sau bài học này, bạn có thể mở bất kỳ tài liệu PDF datasheet nào và tra cứu theo đúng một trình tự thống nhất: thông số cực đại tuyệt đối, sơ đồ và tên chân, điều kiện làm việc khuyến nghị, các đặc tính điện thực sự cần dùng, sơ đồ ứng dụng mẫu, và bản vẽ cơ khí vỏ IC để xác định chân số 1. Với module TB6612FNG, bạn sẽ trích xuất chính xác dải điện áp nguồn động cơ, dải nguồn logic, quy tắc chân STBY, dòng liên tục và dòng đỉnh, đồng thời vẽ lại sơ đồ các chân AIN1, AIN2, PWMA, BIN1, BIN2, PWMB, AO1, AO2, BO1, BO2 ra giấy. Bạn cũng sẽ chỉ ra đúng dòng thông số cực đại trên datasheet ESP32 cấm nối thẳng dây echo của HC-SR04 vào GPIO, và hiểu vì sao ký hiệu in trên các mạch tương thích giá rẻ chỉ được tin tưởng sau khi đã đối chiếu với đồng hồ đo và datasheet.

## Kiến thức cần có

Bạn cần nắm định luật Ohm (bài 01), thói quen đo an toàn bằng đồng hồ vạn năng (bài 02) và cực tính linh kiện (bài 04). Bài này không cấp nguồn động cơ; bạn chỉ cần một quyển sổ ghi chép rõ ràng để mang sang dùng tiếp ở Chương 02.

---

Khi mới học điện tử, thói quen phổ biến nhất là gõ Google tìm một sơ đồ nối dây vẽ sẵn trên blog rồi cắm theo y hệt — cho đến ngày bo mạch mua về có nhãn chân hơi khác, hoặc một cảm biến bốc khói mà không biết tại sao! **Datasheet** (tài liệu kỹ thuật chính hãng) là bản "hiến pháp" duy nhất đáng tin cậy 100% cho mọi con chip: bạn không cần đọc hết 800 trang, mà chỉ cần biết đúng **6 trang cốt lõi** chứa điện áp trần, sơ đồ chân và bảng sự thật.

## Kiến thức cần nhớ: Giải phẫu Một Tài liệu Kỹ thuật (Datasheet)

1. **Absolute Maximum Ratings (Giới hạn Tuyệt đối — Vùng Chết):** Cho biết mức điện áp/dòng/nhiệt độ mà chỉ cần chạm tới là linh kiện có thể hỏng vĩnh viễn — *không bao giờ* thiết kế chạy sát ngưỡng này!
2. **Recommended Operating Conditions (Vùng Làm việc Khuyến nghị):** Dải điện áp nguồn (`VCC`), mức logic nhận diện `HIGH/LOW` ($$V_{IH}, V_{IL}$$) và dòng tải liên tục an toàn.
3. **Pinout & Truth Table (Sơ đồ Chân & Bảng Sự thật):** Xác định chính xác chân nào là nguồn, chân nào là chân khởi động nhạy cảm (*strapping pins* trên ESP32 như GPIO 0, 2, 12, 15), và tổ hợp mức logic nào làm động cơ quay thuận, nghịch hay phanh.

### Ví dụ làm từng bước: Áp dụng 6 bước đọc Datasheet kiểm tra ngưỡng 3,3 V của ESP32 và mạch phân áp

Tra mục *Absolute Maximum Ratings* của ESP32: điện áp tối đa trên bất kỳ chân GPIO nào là $$V_{\text{IO,max}} = V_{DD} + 0.3\text{ V} = 3.3 + 0.3 = \mathbf{3.6\text{ V}}$$.
- Nếu cảm biến siêu âm xuất tín hiệu Echo **$$5.0\text{ V}$$** nối thẳng vào GPIO ESP32: $$5.0\text{ V} > 3.6\text{ V}$$ (vượt trần $$1.4\text{ V}$$) → làm chảy diode kẹp bảo vệ bên trong chân chip!
- Thiết kế nhanh mạch phân áp bảo vệ với hai điện trở phổ thông $$R_1 = 1.2\text{ k}\Omega$$ và $$R_2 = 2.2\text{ k}\Omega$$:
  $$
  V_{\text{GPIO}} = 5.0 \times \frac{2.2}{1.2 + 2.2} = 5.0 \times \frac{2.2}{3.4} \approx \mathbf{3.24\text{ V}}!
  $$
  Kiểm tra cả hai biên từ datasheet ESP32 ($$V_{IH} = 0.75 \times 3.3 = 2.475\text{ V}$$ và trần $$3.6\text{ V}$$):
  $$
  2.475\text{ V} < \mathbf{3.24\text{ V}} < 3.6\text{ V} \implies \text{nhận chắc mức HIGH và an toàn tuyệt đối!}
  $$

### Giải thích: Quy trình 4 bước tra Datasheet trong 3 phút

1. **Bước 1 — Kiểm tra đúng mã hậu tố linh kiện:** `TB6612FNG` khác hoàn toàn chân với `DRV8833`; `ESP32-WROOM-32` có chân khác `ESP32-S3` — luôn đối chiếu đúng mã in trên lưng chip.
2. **Bước 2 — Đọc `Absolute Maximum` trước `Typical`:** Đánh dấu ngay điện áp tối đa cho chân nguồn và chân tín hiệu để dựng rào chắn an toàn.
3. **Bước 3 — Khoanh vùng các chân đặc biệt (Input-only, Strapping, ADC2):** Trên ESP32 cổ điển, GPIO 34–39 *chỉ đọc vào* (không xuất PWM được), còn nhóm ADC2 bị khóa khi bật Wi-Fi!
4. **Bước 4 — Kiểm tra bảng sự thật (Truth Table) trước khi viết code:** Ví dụ trên TB6612FNG, `AIN1=H, AIN2=H` là phanh ngắn mạch (`Short Brake`), còn `AIN1=L, AIN2=L` là dừng thả trôi (`Stop`) — nắm bảng này giúp debug động cơ trong 30 giây.

**Kiểm tra nhanh.** Trên mạch phân áp bảo vệ Echo ở trên, nếu nguồn 5 V của mạch Buck dao động lên mức cao nhất $$5.25\text{ V}$$, điện áp vào chân GPIO ESP32 là bao nhiêu? $$5.25 \times (2.2 / 3.4) \approx \mathbf{3.40\text{ V}} < 3.6\text{ V}$$ — vẫn giữ nguyên biên an toàn!

---

## Vì sao bài này quan trọng

Xe Capstone là hệ dẫn động vi sai gồm hai động cơ TT, module TB6612FNG và vi điều khiển 3,3 V (ESP32 hoặc Pico). Nguồn VM lấy từ pin động cơ (không lấy từ USB), nguồn VCC nối vào đường 3,3 V, còn chân echo của HC-SR04 xuất 5 V nên không được nối trực tiếp vào GPIO 3,3 V. Nếu chỉ nhớ tên chân một cách máy móc theo nhãn dán, buổi chạy thử đầu tiên rất dễ gặp các lỗi tưởng như do phần mềm: bánh xe đứng yên vì quên kéo chân STBY, hoặc cháy chân GPIO ngay khi cảm biến phản hồi. Trình tự đọc datasheet giúp bạn phát hiện các giới hạn cấm trước khi đấu dây.

![Cầu H đang làm gì với các chân ra mô-tơ]({{ site.imgurl }}/generated/hbridge_concept.png)

Mỗi động cơ được mắc giữa một cặp chân ngõ ra (AO1/AO2 hoặc BO1/BO2). Chiều quay quyết định bởi cặp chân logic hướng, tốc độ quyết định bởi xung PWM, và cả hai đều vô hiệu nếu chân STBY đang giữ cầu H ở trạng thái chờ.

## Trình tự sáu bước đọc datasheet

Hãy luôn đi theo đúng thứ tự sau mà không đảo lộn:

**1. Thông số cực đại tuyệt đối (Absolute Maximum Ratings).** Đây là ngưỡng gây hỏng linh kiện — vượt qua giới hạn này nhà sản xuất không đảm bảo IC còn sống, tuyệt đối không phải điểm vận hành bình thường. Hãy chép đúng các dòng liên quan tới dây bạn định nối (điện áp nguồn, điện áp chân logic, dòng ngõ ra); phương án nào vượt ngưỡng này phải bị loại bỏ ngay.

**2. Sơ đồ chân và tên chân (Pinout & Pin Functions).** Bảng mô tả chân đóng vai trò từ điển kết nối: ví dụ AO1 chỉ trở thành "bánh trái" khi bạn quy ước rõ động cơ nào gắn vào đó. Trên TB6612FNG, bạn cần ghi rõ đầy đủ các chân `AIN1`, `AIN2`, `PWMA`, `BIN1`, `BIN2`, `PWMB`, `AO1`, `AO2`, `BO1`, `BO2`, cùng `VM`, `VCC`, `GND` và `STBY`. Phân tách rạch ròi nhóm chân đầu vào logic (nối GPIO) và nhóm chân ngõ ra công suất (nối động cơ) để tránh đưa dòng động cơ về vi điều khiển.

**3. Điều kiện làm việc khuyến nghị (Recommended Operating Conditions).** Đây là vùng hoạt động ổn định mà mọi thông số đặc tính điện phía sau được đo đạc. Lưu ý rằng giới hạn trên trang thông số của module có thể chặt hơn giới hạn của con chip trần do ảnh hưởng của đường mạch đồng và hàng chân header; khi hai tài liệu khác nhau, luôn tuân theo giới hạn chặt hơn.

**4. Các đặc tính điện cần dùng (Electrical Characteristics).** Không cần đọc hết toàn bộ bảng dài mà chỉ trích đúng thông số bạn áp dụng: với mạch lái động cơ, đó là điện áp tối thiểu được nhận là mức cao ($V_{IH,\min}$), điều kiện kéo mức cao cho chân `STBY`, dòng liên tục và dòng đỉnh.

**5. Sơ đồ ứng dụng mẫu (Typical Application Circuit).** Ghi nhận cấu trúc chuẩn: tụ lọc đặt sát chân VM, tụ lọc đặt sát chân VCC, nối mass chung, và các chân vào điều khiển từ vi điều khiển. Ngay cả khi module đã hàn sẵn tụ nhỏ, tụ lọc vẫn không thể thay thế sợi dây mass chung giữa ESP32 và mạch lái.

**6. Bản vẽ cơ khí vỏ IC (Package Outline) để tìm chân số 1.** Bản vẽ tiêu chuẩn là hình chiếu nhìn từ mặt trên xuống (top view), trong đó chân số 1 nằm cạnh dấu chấm hoặc cạnh vát; lưu ý rằng nhìn từ mặt đáy sẽ bị lật ngược hàng chân. Nếu ký hiệu in lụa trên module mâu thuẫn với dấu chấm định vị, hãy dùng đồng hồ vạn năng đo kiểm tra để phân xử.

Các mạch tương thích giá rẻ đôi khi in sai nhãn lụa (chẳng hạn ghi "5V" ở chân logic 3,3 V, đảo vị trí GND với VM, hoặc in lệch mũi tên chân ECHO/TRIG). Khi nghi ngờ một đường nguồn, hãy đo trực tiếp bằng đồng hồ ở chế độ DC V (que đen đặt tại mass) trên nguồn có giới hạn dòng rồi ghi kết quả thực tế ra giấy — số đo luôn có giá trị cao hơn chữ in.

## Áp dụng sáu bước cho TB6612FNG

Hãy đối chiếu thông số của module TB6612FNG dùng trong khóa học với tài liệu tóm tắt chip Toshiba trên trang Pololu ở mục Đọc thêm (nếu thông số trên trang nhà sản xuất module chặt hơn thì ưu tiên làm theo mức chặt hơn).

**Bước 1 (Cực đại tuyệt đối):** Kiểm tra trước để loại bỏ mọi phương án ngược cực hoặc quá áp trước khi cắm giắc.

**Bước 2 (Tên chân):** Động cơ A nhận tín hiệu chiều quay từ `AIN1`, `AIN2` và tín hiệu tốc độ từ `PWMA`; động cơ B tương ứng là `BIN1`, `BIN2` và `PWMB`. Hai cặp ngõ ra nối dây động cơ là `AO1`/`AO2` và `BO1`/`BO2`. Chân `STBY` không phải chân dư mà là công tắc bật/tắt cả hai cầu H: bảng chân lý chỉ cho phép động cơ chạy khi `STBY` ở mức cao. Vì nhiều module thiết kế kéo sẵn `STBY` xuống mức thấp, quên nối chân này sẽ khiến cả hai bánh đứng yên dù mã nguồn đang gửi lệnh tiến.

**Bước 3 (Điều kiện khuyến nghị):** Module của khóa học có dải `VM` từ 4,5 V đến 10 V. Một cell lithium đơn (~3,7 V) nằm dưới ngưỡng thấp này, còn bộ pin sạc đầy vượt 10 V lại vượt ngưỡng trên của module dù datasheet chip trần có thể cho phép cao hơn. Nguồn logic `VCC` nằm trong dải 2,7 V đến 5,5 V, hoàn toàn tương thích với đường 3,3 V của vi điều khiển. Nguồn USB 5 V tuy nằm trong dải logic nhưng không dùng để cấp cho động cơ (xem chi tiết ở bài 09). Hai chân `VM` và `VCC` được thiết kế tách biệt hoàn toàn.

**Bước 4 (Đặc tính điện cần dùng):** Dòng liên tục mỗi kênh khoảng 1,2 A và dòng đỉnh khoảng 3,2 A. Hai động cơ TT quay không tải rút dòng rất nhỏ so với 1,2 A, nhưng khi kẹt trục dòng tăng rất mạnh; duy trì trạng thái kẹt vượt mức liên tục sẽ làm cháy mạch lái. Đồng thời, cần lưu ý ngưỡng nhận diện mức logic cao:

$$
V_{IH,\min} = 0{,}7 \times V_{CC}
$$

Tại $$V_{CC} = 3{,}3\,\mathrm{V}$$, ngưỡng này là $$2{,}31\,\mathrm{V}$$, nên tín hiệu mức cao 3,3 V từ GPIO vượt qua dễ dàng. Ngược lại, nếu cấp $$V_{CC} = 5\,\mathrm{V}$$, ngưỡng tối thiểu tăng lên $$3{,}5\,\mathrm{V}$$ và chân GPIO 3,3 V **không đạt** mức cao tiêu chuẩn. Phép tính này khẳng định bắt buộc phải cấp `VCC` bằng 3,3 V khi điều khiển từ ESP32 hay Pico, không cấp 5 V rồi trông chờ mạch tự nhận.

**Bước 5 & 6 (Sơ đồ ứng dụng và bản vẽ vỏ):** Nối `VM` vào pin động cơ, `VCC` vào 3,3 V, nối mass chung, đấu động cơ vào `AO1`/`AO2` và `BO1`/`BO2`, và nối bốn chân GPIO tới `AIN1`, `AIN2`, `PWMA`, `STBY` kèm tụ đệm đúng cực ngang chân `VM` (sẽ chọn trị số cụ thể ở bài 09). Cuối cùng, đánh dấu rõ vị trí chân số 1 trên bản vẽ.

Lưu ý rằng chiều "thuận kim đồng hồ" (CW) trong bảng chân lý datasheet phụ thuộc vào cách bạn đấu hai dây động cơ chứ không tự động khớp hướng tiến của khung xe. Khi `STBY` ở mức cao, `AIN1` khác trạng thái `AIN2` và `PWMA` có xung thì động cơ quay; đảo trạng thái `AIN1`/`AIN2` sẽ đảo chiều quay; đưa `STBY` xuống thấp sẽ chuyển mạch về chế độ chờ.

## Giới hạn 5 V trên chân GPIO của ESP32

Áp dụng đúng trình tự trên cho tài liệu PDF của Espressif: điện áp cực đại tuyệt đối trên chân GPIO của ESP32 chỉ cao hơn đường nguồn 3,3 V vài trăm milivôn, **không phải 5 V**. Vùng làm việc khuyến nghị là mức nguồn vào/ra 3,3 V; mọi xung 5 V đều nằm ngoài hàng rào an toàn.

Với cảm biến **HC-SR04** (nuôi bằng 5 V), chân `Echo` xuất mức cao xấp xỉ 5 V khi có xung phản hồi, nên bảng thông số cực đại cấm tuyệt đối việc nối thẳng `Echo` vào bất kỳ chân GPIO nào của ESP32. Chân `Trig` (ngõ vào kích cảm biến) thường nhận được mức cao 3,3 V, nhưng chân `Echo` bắt buộc phải hạ mức. Tờ sơ đồ chân MCU hôm nay cần ghi rõ cảnh báo "không nối thẳng Echo" kèm con số giới hạn điện áp. Raspberry Pi Pico cũng có giới hạn tương tự (chân GPIO 3,3 V không chịu 5 V), đồng thời lưu ý khi lập trình phải dùng số chân `GP` trên sơ đồ chứ không đếm theo số thứ tự chân vật lý từ đầu USB.

Nếu gặp mạch tương thích in nhãn "5V" cạnh một lỗ cắm bạn tưởng là GPIO, hãy cắm riêng USB và đo kiểm tra: bất kỳ lỗ nào đo được gần 5 V đều là chân nguồn, không phải chân nhận tín hiệu echo hay chân đấu LED trực tiếp.

## Thực hành

Bài thực hành này không quay động cơ; sản phẩm đầu ra là hai trang sơ đồ chân hoàn chỉnh.

1. Tạo hai trang ghi chép trong sổ lab mang tên "Sơ đồ chân MCU" và "Sơ đồ chân driver", ghi rõ ngày thực hiện (nếu mạch chưa về, lập trang MCU từ PDF ESP32 và ghi chú `chưa mua board`).
2. Trên trang **driver**, trình bày đủ sáu bước: ghi rõ `VM` 4,5–10 V, `VCC` 2,7–5,5 V, quy tắc `STBY` phải ở mức cao, dòng 1,2 A liên tục và 3,2 A đỉnh. Phác thảo hàng chân header và gắn đủ nhãn `AIN1`, `AIN2`, `PWMA`, `BIN1`, `BIN2`, `PWMB`, `AO1`, `AO2`, `BO1`, `BO2`, `VM`, `VCC`, `GND`, `STBY` (nếu chữ in lụa trên module khác datasheet, kẻ hai cột đối chiếu).
3. Trên trang **MCU**, chép lại giới hạn điện áp cực đại của GPIO cùng tên bảng thông số gốc; ghi rõ lệnh cấm nối thẳng chân `Echo` 5 V của HC-SR04 vào GPIO. Gán trước các chân ngõ ra hợp lệ cho `AIN1`, `AIN2`, `PWMA` và `STBY` (với ESP32 thông dụng, tránh chọn các chân dùng cho bộ nhớ flash và các chân chỉ hỗ trợ ngõ vào).
4. Không cấp nguồn `VM`. Nếu có nguồn 3,3 V giới hạn dòng để cấp riêng phần logic (hoặc chỉ cắm USB cho mạch phát triển), đo kiểm tra chân ghi `5V` và chân ghi `3V3` với que đen đặt tại mass; nếu chưa có thiết bị để đo an toàn, viết rõ các bước đo và đánh dấu `dry-run`.
5. Lưu ảnh chụp hai trang ghi chép vào sổ với tên `ch01-07-mcu-card` và `ch01-07-driver-card` (đảm bảo đủ rõ nét để dùng lại ở Chương 02).

Dừng ngay nếu phát hiện chân nào nóng bất thường hoặc một chân bạn định dùng làm GPIO lại đo được gần 5 V.

## Video tham khảo

- **Xem trước:** [How To Read A Datasheet - Electronics with Becky Stern | DigiKey](https://www.youtube.com/watch?v=v2d5H5k_SAc) — DigiKey, tiếng Anh. Hướng dẫn trình tự đọc một datasheet cơ bản: tính năng, điện áp tối đa rồi tới sơ đồ chân.
- [How To Read A Datasheet - Phil's Lab #123](https://www.youtube.com/watch?v=1EXXqWweTkI) — Phil’s Lab, tiếng Anh. Đi sâu hơn vào bảng đặc tính điện và đồ thị; bạn có thể dừng ở phần bảng chân của con IC mình đang sử dụng.

## Bài tập

Với mỗi câu hỏi dưới đây, hãy nêu rõ con số thông số, tên bảng chứa thông số đó và kết nối dây bị cấm tương ứng:

1. Một người định nối thẳng chân `ECHO` của HC-SR04 vào chân GPIO 4 của ESP32 với suy nghĩ bảng cực đại sẽ chịu được. Thông số nào cấm kết nối này, và bạn sẽ ghi nhận mức điện áp nào nếu đo xung echo khi cảm biến nuôi bằng 5 V?
2. Một mạch lái ghi chân logic cần 5 V trong khi mức cao của ESP32 là 3,3 V. Tính $$0{,}7 \times 5$$ và $$0{,}7 \times 3{,}3$$. Kết quả nào cho thấy ESP32 không đạt chuẩn điều khiển, và cần cấp `VCC` bao nhiêu để khắc phục?
3. Có người định đấu tạm hai động cơ TT vào chân 5 V của ESP32 "chỉ để thử". Biết cổng USB cấp khoảng 500 mA còn mạch lái chịu 1,2 A liên tục. Giới hạn nào bị vượt quá trước, và vì sao mức 1,2 A của mạch lái không cho phép lấy USB làm nguồn `VM`?
4. Nếu chân `STBY` để hở và chương trình không kích lên mức cao, cơ chế nào của IC ngăn xung PWM làm bánh xe quay, và thao tác GPIO nào giải quyết việc này?
5. Giả sử bạn nhận được module DRV8833 thay vì TB6612. Vì sao không được chép nguyên các tên chân `AIN1`, `PWMA`, `STBY` từ trang ghi chép hôm nay sang module mới, và bạn phải mở tài liệu nào ở mục Đọc thêm?

<details markdown="1">
<summary>Gợi ý đáp án</summary>

1. Thông số cấm là giới hạn điện áp cực đại tuyệt đối (Absolute Maximum Ratings) của GPIO ESP32, vốn nằm sát mức nguồn 3,3 V chứ không phải 5 V. Xung echo khi cảm biến nuôi 5 V sẽ lên gần 5 V, nên không được nối thẳng mà cần mạch chuyển mức hoặc cầu chia áp.
2. $$0{,}7 \times 5 = 3{,}5\,\mathrm{V}$$, lớn hơn mức cao 3,3 V của GPIO nên cấp `VCC = 5 V` sẽ không đạt chuẩn mức cao. Với $$0{,}7 \times 3{,}3 = 2{,}31\,\mathrm{V}$$, chân GPIO 3,3 V vượt qua dễ dàng; do đó phải cấp `VCC = 3,3 V`.
3. Giới hạn 500 mA của cổng USB bị vượt quá trước (ngay cả một động cơ TT kẹt trục đã rút vượt mức này). Thông số 1,2 A chỉ là khả năng chịu dòng liên tục của mạch lái, không phải năng lực cấp dòng của cổng USB; nguồn `VM` bắt buộc phải lấy từ pin động cơ.
4. Khi `STBY` ở mức thấp (hoặc bị kéo xuống thấp do để hở), IC khóa cả hai cầu H ở chế độ chờ (standby) nên mọi lệnh PWM đều vô hiệu. Chỉ cần xuất mức logic cao giữ ổn định trên chân `STBY` trong thời gian cho phép chạy.
5. Mỗi họ IC có sơ đồ và tên chân riêng (ví dụ DRV8833 dùng `nSLEEP` thay vì `STBY`). Cần mở trang thông số TI DRV8833 ở mục Đọc thêm và thực hiện lại đủ 6 bước đọc datasheet cho đúng con chip đó.

</details>

## Đọc thêm

- [Module TB6612FNG của Pololu](https://www.pololu.com/product/713) — tóm tắt rõ ràng cách hoạt động của IC Toshiba: dải logic, chân STBY và mức dòng 1,2 A / 3,2 A (ưu tiên giới hạn chặt hơn nếu trang nhà sản xuất module quy định khác).
- [Datasheet ESP32 (PDF)](https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf) — bảng thông số cực đại tuyệt đối và danh sách chân GPIO.
- [TI DRV8833](https://www.ti.com/product/DRV8833) — tài liệu chính thức cho phương án mạch lái thay thế nếu bạn sử dụng DRV8833.
- [Tài liệu Raspberry Pi Pico](https://www.raspberrypi.com/documentation/microcontrollers/raspberry-pi-pico.html) — giới hạn vào/ra 3,3 V, vị trí chân số 1 và bảng ánh xạ số chân `GP` cho lập trình.

## Mua ở Việt Nam

Các linh kiện chính (ESP32 hoặc Pico, module TB6612, động cơ TT và HC-SR04) đã nằm trong danh sách ở bài [BOM và cách mua bộ kit robot ở Việt Nam]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %}). Không mua rời IC TB6612FNG dạng chip dán chân mịn để tự hàn tay cho đồ án.

Nếu chưa có đồng hồ vạn năng để kiểm tra nhãn in trên mạch, bạn có thể tham khảo [UNI-T UT33D+ tại Hshop](https://hshop.vn/dong-ho-van-nang-dien-tu-digital-multimeter-uni-t-ut33d-chinh-hang) (kiểm tra giá hiện hành trước khi đặt) hoặc đối chiếu thêm tại [Hshop](https://hshop.vn/), [Thế Giới IC](https://www.thegioiic.com/) và [IC Đây Rồi](https://icdayroi.com/).
