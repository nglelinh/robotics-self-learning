---
layout: post
title: "Danh mục dụng cụ bàn lab"
chapter: "00"
order: 4
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter00
lesson_type: required
draft: false
---

Hãy dành khoảng 90 phút cho bài học này. Nếu đã có đồng hồ vạn năng, bạn hãy kiểm tra hoạt động của nó trên một mối nối đã biết rồi cất gọn. Nếu chưa có, bạn vẫn hoàn thành bước kiểm kê Đợt 1 và chụp ảnh ghi nhận những món còn thiếu. Lưu ý: không cắm điện làm nóng mỏ hàn trong bài này.

## Mục tiêu học

Sau bài học này, bạn sẽ **nêu** được công dụng của từng dụng cụ trong Đợt 1 và **mô tả** dấu hiệu thực tế chứng tỏ chúng hoạt động tốt. Bạn sẽ **chọn** đúng thang đo điện áp một chiều và thông mạch trên đồng hồ, đồng thời **từ chối** đo điện trở trên mạch đang có điện. Bạn sẽ **mô tả** được mối hàn đạt chuẩn là kết quả của việc làm nóng đều pad và chân linh kiện (với thiếc Sn63 đường kính 0,8 mm và giá đỡ mỏ hàn) thay vì nhỏ một giọt thiếc lên kim loại nguội. Bạn sẽ **phân biệt** rõ breadboard (chỉ dùng cho đường tín hiệu) với đường dây chịu dòng động cơ, và **tách bạch** vai trò của kìm cắt với kìm tuốt dây theo loại hư hại mà mỗi dụng cụ giúp phòng tránh. Cuối cùng, bạn sẽ **kiểm kê** bàn làm việc theo danh sách Đợt 1, chụp ảnh và liệt kê chính xác những món còn thiếu để bài 00-05 trở thành danh sách mua sắm có căn cứ.

## Cần có trước

Bạn đã hoàn thiện thẻ quy trình cấp nguồn từ bài 00-03 (ít nhất trên giấy), nắm rõ nguồn động cơ VM tách biệt với chân 3,3 V và mỏ hàn luôn đi kèm giá đỡ cùng kính bảo hộ. Chương 01 sẽ bắt đầu các bài đo thực tế bằng que đo; hôm nay bạn cần biết dụng cụ nào giải quyết câu hỏi nào để tránh gián đoạn giữa chừng.

---

Lập trình trên màn hình máy tính cho phép bạn đặt điểm dừng (breakpoint) để nhìn thấy mọi biến số. Nhưng khi mạch robot trên bàn không chạy, dòng điện vô hình và điện áp không hề phát sáng — **dụng cụ bàn lab** chính là "đôi mắt và đôi tay" giúp bạn nhìn thấy thế giới vật lý! Hiểu đúng chức năng và giới hạn đo của đồng hồ vạn năng, mỏ hàn, kìm tuốt dây và thước kẹp giúp bạn bắt bệnh phần cứng trong 2 phút thay vì đoán mò suốt buổi tối.

## Kiến thức cần nhớ: Bốn nhóm dụng cụ cốt lõi trên bàn lab Robotics

1. **Nhóm Đo lường (Đồng hồ vạn năng, Thước kẹp):** Biến các đại lượng ẩn (điện áp, thông mạch, điện trở, dòng điện, kích thước cơ khí) thành con số định lượng có sai số xác định.
2. **Nhóm Lắp ráp Điện (Breadboard, Mỏ hàn nhiệt độ ổn định, Dây jumper):** Tạo kết nối điện chắc chắn với điện trở tiếp xúc thấp — tách bạch giai đoạn thử nghiệm nhanh (breadboard) với giai đoạn chịu rung động trên xe chạy thật (hàn/cosse).
3. **Nhóm Gia công Cơ khí & An toàn (Kìm cắt, Kìm tuốt dây, Kính bảo hộ, Đế gá PCB):** Giữ linh kiện cố định, cắt chân dây không bắn vào mắt và đảm bảo khoảng hở lắp đặt chính xác cho trục bánh xe và cảm biến.

### Ví dụ làm từng bước: Kiểm định sai số linh kiện bằng đồng hồ vạn năng

Trước khi tin vào dụng cụ hay linh kiện mới mua, hãy kiểm tra dung sai bằng phép tính cụ thể:
- **Kiểm tra điện trở $$1\text{ k}\Omega$$ dung sai $$\pm 5\%$$ (vạch vàng kim):**
  $$
  R_{\min} = 1{,}000 \times (1 - 0.05) = \mathbf{950\ \Omega}, \qquad R_{\max} = 1{,}000 \times (1 + 0.05) = \mathbf{1{,}050\ \Omega}.
  $$
  Nếu đồng hồ đọc $$982\ \Omega$$ → linh kiện đạt chuẩn! Nếu đồng hồ đọc $$10.2\text{ k}\Omega$$ → bạn đã lấy nhầm sang điện trở $$10\text{ k}\Omega$$!
- **Kiểm tra đường nguồn $$5.0\text{ V}$$ cấp cho cảm biến (dung sai cho phép $$\pm 5\%$$):**
  $$
  V_{\min} = 5.0 \times 0.95 = \mathbf{4.75\text{ V}}, \qquad V_{\max} = 5.0 \times 1.05 = \mathbf{5.25\text{ V}}.
  $$
  Nếu đo lúc không tải được $$5.02\text{ V}$$ nhưng vừa chạy động cơ tụt xuống $$4.40\text{ V}$$ → nguồn bị sụt áp, cần kiểm tra pin hoặc mạch hạ áp!

### Giải thích: Quy tắc 4 bước quản lý dụng cụ giúp giảm 80% lỗi vặt

1. **Bước 1 — Luôn kiểm tra que đo đồng hồ trước khi đo:** Chập hai đầu que đo ở thang Ohm; nếu hiển thị $$0.2\text{–}0.5\ \Omega$$ là dây tốt, nếu nhảy số loạn xạ thì chính dây đo đã đứt ngầm.
2. **Bước 2 — Để đồng hồ ở thang DC V (20 V) sau khi dùng xong:** Không bao giờ bỏ quên que đỏ ở lỗ đo dòng 10 A — lần sau đo điện áp pin sẽ gây ngắn mạch tức thì!
3. **Bước 3 — Dùng đúng tiết diện dây cho đúng dòng:** Dây jumper mảnh (26–28 AWG) chỉ dùng cho tín hiệu logic (vài mA); dây cấp nguồn động cơ (1–3 A) phải dùng dây 20–22 AWG để tránh sụt áp và nóng chảy vỏ.
4. **Bước 4 — Đầu tư trước cho dụng cụ đo và hàn cơ bản:** Một chiếc đồng hồ vạn năng chính xác và mỏ hàn chỉnh nhiệt tốt phục vụ bạn suốt nhiều năm, đáng giá hơn nhiều so với việc mua sớm cảm biến đắt tiền.

**Kiểm tra nhanh.** Một bộ mạch hạ áp buck được chỉnh về $$5.00\text{ V}$$ bằng tua-vít, đồng hồ vạn năng có độ chính xác $$\pm 1\%$$ đọc ra $$5.03\text{ V}$$. Điện áp thật nằm trong khoảng nào? Sai số đo là $$\pm 0.05\text{ V}$$, nên điện áp thật nằm trong $$[4.98\text{ V},\ 5.08\text{ V}]$$ — hoàn toàn an toàn cho mọi cảm biến 5 V!

---

## Vì sao bài này gắn liền với Capstone

Bài nghiệm thu Chương 07 thường gặp những lỗi phần cứng rất cơ bản: một sợi dây cắm trông có vẻ chắc chắn nhưng bị đứt lõi bên trong đầu bấm, một phép đo mass thực hiện nhầm ở thang ohm trên mạch đang cấp điện, hay dây động cơ cắm trực tiếp vào lò xo của breadboard. Những sự cố này dễ bị nhầm thành lỗi firmware và kéo bạn đi tìm lỗi ở tầng phần mềm hay ROS 2, trong khi công cụ gỡ lỗi thực sự chỉ là một tiếng bíp thông mạch. Danh mục dụng cụ trong bài giúp bạn tách bạch "lỗi timeout PWM" với "lỗi dây dẫn" trước khi hệ thống trở nên phức tạp hơn.

## Dấu hiệu hoạt động tốt của từng dụng cụ

Để đồng bộ với bảng vật tư ở bài 00-05, **Đợt 1** là bộ dụng cụ và linh kiện nền tảng giúp bạn bắt đầu ngay Chương 01: đồng hồ vạn năng, mỏ hàn 60 W kèm giá đỡ, thiếc hàn, kìm cắt, breadboard không hàn, dây cắm (jumper), cáp USB truyền dữ liệu, mạch vi điều khiển, vài đèn LED và một nút nhấn. **Đợt 2** gồm khung xe, mạch lái TB6612FNG và cảm biến HC-SR04. **Đợt 3** gồm cell pin và bộ sạc riêng từng cell. Bài này tập trung vào các dụng cụ của Đợt 1; bản thân vi điều khiển chỉ là một mục trên phiếu kiểm kê chứ không phải dụng cụ thao tác.

![Chân dung các họ đồ trên bàn, không phải một bộ có thương hiệu]({{ site.imgurl }}/generated/kit_catalog_overview.png)

Hình minh họa giới thiệu các nhóm thiết bị trên bàn lab. Đồng hồ vạn năng, mỏ hàn, breadboard và dụng cụ cầm tay là nhóm bắt buộc ngay Đợt 1. Các thiết bị như nguồn bàn hay máy phân tích logic (nếu có trong hình) dành cho giai đoạn sau, chưa cần mua hôm nay. Hàng bên dưới gồm vi điều khiển và khung robot sẽ đặt mua theo bài 00-05 khi sẵn sàng.

### Đồng hồ vạn năng

Đồng hồ vạn năng số giúp bạn trả lời ba câu hỏi thường gặp nhất — và có một phép đo bạn không được thực hiện nhầm.

**Điện áp một chiều (DC V)** đo hiệu điện thế giữa hai điểm, ký hiệu chữ V kèm vạch thẳng. Cắm que đen vào mass (GND), đặt que đỏ lên điểm cần đo. Đường USB 5 V tốt sẽ đọc khoảng 5 V; đường 3,3 V tốt đọc khoảng 3,2–3,4 V. Kết quả 0,00 V nghĩa là mạch đang tắt, chạm sai chân hoặc que đen chưa tiếp xúc đúng mass — đừng vội kết luận đồng hồ hỏng trước khi kiểm tra que đo bằng thang thông mạch.

**Thông mạch** phát tiếng bíp khi điện trở giữa hai que đo rất nhỏ. Hãy chạm trực tiếp hai đầu que đo vào nhau: bạn phải nghe tiếng bíp rõ và thấy màn hình hiện gần 0 Ω (đôi khi có vài phần mười ohm của chính dây đo). Tiếng bíp này là bằng chứng đồng hồ và dây đo hoạt động bình thường. Một sợi dây ngắn còn tốt sẽ kêu bíp; ký hiệu **OL** nghĩa là mạch đang hở.

**Đo điện trở (Ω)** cho biết giá trị trở kháng khi thang thông mạch không kêu. Chỉ đo điện trở trên linh kiện **đã ngắt hoàn toàn nguồn điện**. Khi đo ohm, đồng hồ tự bơm một dòng thử nhỏ; nếu mạch vẫn đang cấp nguồn, dòng này xung đột với nguồn mạch khiến số đo sai lệch và có thể làm hỏng đồng hồ hoặc board. Tuyệt đối không đo ohm trên đường nguồn đang có điện.

**Lưu ý bẫy đo dòng điện:** Khi chuyển que đỏ sang lỗ cắm ghi A hoặc mA, đồng hồ trở thành gần như một đoạn dây nối tắt. Nếu quên rút que đỏ về lỗ đo áp mà đem đi đo điện áp, bạn sẽ làm ngắn mạch nguồn. Hãy luôn kiểm tra lại vị trí lỗ cắm của que đỏ trước mỗi lần đo áp.

![Đồng hồ cầm tay; lỗ cắm quan trọng ngang vạch chọn]({{ site.imgurl }}/wikimedia/Digital_Multimeter_Aka.jpg)

Dù bạn dùng UNI-T UT33D+ hay Wadfow, thiết bị đều đạt yêu cầu miễn là có còi thông mạch và đo được điện áp một chiều. Hãy luôn kiểm chứng bằng tiếng bíp chập que trước khi tin vào bất kỳ con số đo nào trên robot.

### Mỏ hàn, giá đỡ và thiếc hàn

Mối hàn tốt là sự liên kết nhiệt giữa pad đồng và chân linh kiện: bạn làm nóng cả hai chi tiết đó rồi mới đưa một lượng thiếc vừa đủ chảy vào mối nóng. Nếu làm chảy thiếc sẵn trên mũi mỏ rồi chấm lên chân nguội, mối hàn trông có vẻ đầy đặn nhưng rất dễ bong sau vài ngày. Mối hàn đạt chuẩn có bề mặt bóng, thiếc bám ướt đều cả hai mặt và không tạo cầu nối sang pad bên cạnh.

Loại thiếc khuyến nghị trong khóa học là hợp kim Sn63/Pb37 đường kính 0,8 mm, đủ mảnh để thao tác gọn trên chân header. Giá đỡ mỏ hàn là trang bị bắt buộc: đặt mũi mỏ 60 W đang nóng lên dây điện hoặc mặt bàn rất dễ gây tai nạn. Luôn đeo kính bảo hộ khi cắt chân linh kiện vì mẩu chân cắt ra có thể bắn vào mắt, và mở cửa sổ hoặc dùng quạt thông gió để đẩy khói flux ra khỏi vùng thở. Chương 00 chưa yêu cầu thực hành hàn.

![Mỏ không giá là ảnh của mối nguy, không phải bố trí bạn muốn]({{ site.imgurl }}/wikimedia/Soldering_iron.jpg)

Bức ảnh trên minh họa một chiếc mỏ hàn đặt trần không có giá đỡ — đây chính là trạng thái mất an toàn cần tránh. Mỏ hàn của bạn phải nằm vững trên giá đỡ mỗi khi bạn rời tay lấy thiếc.

### Breadboard không dành cho dòng động cơ

Breadboard không hàn hoạt động nhờ hệ thống lá lò xo bên dưới bề mặt nhựa: các lỗ trên cùng một hàng ngắn nối liền với nhau, còn rãnh giữa dùng để đặt IC bắc ngang qua. Lưu ý rằng thanh nguồn dọc mép trên nhiều loại breadboard 830 lỗ **bị ngắt ở chính giữa**; nếu đo thông mạch từ đầu này sang đầu kia không kêu, đó là do khe ngắt cấu tạo chứ không phải lỗi.

![Breadboard không hàn: ổn cho tín hiệu, sai cho dòng motor]({{ site.imgurl }}/wikimedia/breadboard.jpg)

Breadboard hoạt động tốt khi một sợi dây cắm đo thông mạch từ đầu đến cuối hàng lỗ và cách ly hoàn toàn qua rãnh giữa. Tuy nhiên, tuyệt đối không dẫn dòng động cơ qua các lá lò xo này: động cơ TT khi kẹt trục rút dòng lớn, khiến điện trở tiếp xúc sinh nhiệt và gây sụt áp. Breadboard chỉ dành cho dây tín hiệu, còn dây động cơ phải đi vào trạm vít hoặc chân hàn của TB6612FNG.

### Kìm cắt và kìm tuốt dây

Kìm cắt chân (cỡ 170 trong danh sách mua) dùng để cắt gọn chân linh kiện sau khi hàn; thao tác đạt khi vết cắt phẳng và mẩu chân được giữ lại không bắn lung tung. Nếu dùng kìm cắt để tuốt vỏ dây, lưỡi kìm rất dễ cứa vào lõi đồng khiến dây bị gãy ngầm về sau. Kìm tuốt dây chuyên dụng giúp bóc vỏ sạch mà không làm tổn thương lõi dẫn; tránh dùng dao rọc thay thế. Ngoài ra, dây cắm breadboard có thể đứt ngầm bên trong đầu bấm dù lớp nhựa bên ngoài vẫn nguyên vẹn, nên khi động cơ không chạy dù dây PWM trông bình thường, hãy kiểm tra thông mạch sợi dây đó trước tiên.

### Các thiết bị để dành cho giai đoạn sau

Nguồn cấp có giới hạn dòng, máy phân tích logic (logic analyzer) và máy hiện sóng (oscilloscope) giúp gỡ lỗi nhanh hơn ở các dự án lớn, nhưng không thiết bị nào trong số này là cần thiết để hoàn thành Chương 00, và chúng cũng không thay thế được một sợi dây mass chung bị đấu thiếu. Hãy xếp chúng vào danh sách nâng cấp về sau.

## Thực hành: kiểm kê bàn làm việc theo Đợt 1

Dọn gọn một góc bàn và bày ra toàn bộ các món thuộc Đợt 1 mà bạn thực sự đang sở hữu. Không mượn đồ từ nơi khác đặt vào chụp ảnh "cho đủ bộ".

Liệt kê đủ các mục sau vào sổ lab và đánh dấu `có` hoặc `thiếu` cho từng món: đồng hồ vạn năng, mỏ hàn, giá đỡ, thiếc hàn, kìm cắt, breadboard, dây cắm, cáp USB truyền dữ liệu, mạch vi điều khiển, ít nhất một đèn LED và ít nhất một nút nhấn. Chụp ảnh toàn bộ bố trí và lưu vào sổ. Ở trường đoạn serial, ghi tên cổng nếu mạch nhận cổng khi chỉ cắm USB; ngược lại, ghi rõ `cáp chưa chứng minh — chưa có board` hoặc `cáp chưa chứng minh — không thấy cổng`.

Nếu đã có đồng hồ, hãy kiểm tra ngay bằng cách chạm hai que đo ở thang thông mạch và ghi vào sổ "bíp trên mối nối ngắn đã biết". Nếu không kêu bíp, đồng hồ chưa đủ tin cậy để sử dụng. Tuyệt đối không đo ohm trên mạch đang cắm điện. Nếu chưa có đồng hồ, ghi `thiếu đồng hồ` và hoãn các bài đo của Chương 01 cho tới khi bổ sung đủ. Nếu có breadboard, hãy đo thông mạch một hàng lỗ và xác nhận hai bên rãnh giữa không thông nhau. Nếu có mỏ hàn, hãy kiểm tra giá đỡ đi kèm nhưng vẫn để mỏ rút điện.

**Kết quả cần đạt:** Một bức ảnh chụp thực tế, một danh sách rõ món nào còn thiếu, và xác nhận tiếng bíp của đồng hồ (hoặc ghi chú rõ `thiếu đồng hồ`).

**Cách xử lý khi lệch chuẩn:** Không tính đồng hồ mượn của bạn bè vào ảnh kiểm kê. Nếu lỡ đo thông mạch trên mạch đang cắm điện, hãy rút nguồn ngay trước khi đo lại. Rút mọi dây động cơ nếu đang cắm trên breadboard. Bạn chỉ cần một đồng hồ vạn năng đạt chuẩn, không cần mua hai chiếc.

## Ví dụ làm sẵn

Ảnh kiểm kê của Quân có: đồng hồ Wadfow, mỏ hàn 60 W nhưng chưa có giá đỡ, một cuộn thiếc 0,8 mm, kìm cắt, chưa có breadboard, một sợi cáp USB chỉ sạc chưa kiểm chứng và chưa có vi điều khiển. Anh liệt kê các món thiếu: giá đỡ mỏ hàn, breadboard, dây cắm, cáp USB dữ liệu, vi điều khiển, LED và nút nhấn. Anh chạm hai que đo của đồng hồ và nghe tiếng bíp rõ, nên ghi dòng đồng hồ là `có` kèm bằng chứng "bíp trên mối nối ngắn đã biết", đồng thời không đo ohm trên cổng USB đang cắm laptop.

Quân chỉ tính trước chi phí cho các dụng cụ còn thiếu theo mốc giá Hshop ngày 23 tháng 9 năm 2026 (còn vi điều khiển để tính gộp ở bài 00-05). Vì đã có mỏ hàn, thiếc và kìm cắt, phần dụng cụ cần mua thêm ngay hôm nay chỉ là giá đỡ và breadboard:

$$
40000 + 35000 = 75000
$$

đồng, cộng thêm dây cắm, cáp dữ liệu và mạch vi điều khiển theo bài 00-05. Nếu bắt đầu từ con số 0 (chỉ chọn một đồng hồ), bộ dụng cụ cơ bản gồm: Wadfow 185.000 ₫ (hoặc UT33D+ 285.000 ₫), mỏ hàn 75.000 ₫, giá đỡ 40.000 ₫, thiếc 24.000 ₫, kìm cắt 35.000 ₫ và breadboard 830 lỗ 35.000 ₫. Với đồng hồ Wadfow, tổng chi phí là:

$$
185000 + 75000 + 40000 + 24000 + 35000 + 35000 = 394000
$$

đồng; nếu chọn UNI-T UT33D+, tổng là 494.000 ₫. Quân ghi lại cả hai mức tổng kèm ngày khảo sát 23 tháng 9 năm 2026 và không mua máy hiện sóng.

## Video tham khảo

- **Xem trước:** [EEVblog 1636 - Ultimate Multimeter Beginners Guide!](https://www.youtube.com/watch?v=52w3xeXrMU8) — EEVblog, tiếng Anh. Hướng dẫn sử dụng đồng hồ vạn năng cho người mới, giúp bạn nắm vững cách chọn thang đo trước khi mua thêm dụng cụ.
- [iFixit's Soldering 101: Beginners Guide](https://www.youtube.com/watch?v=rK38rpUy568) — iFixit, tiếng Anh. Giới thiệu tổng quan mỏ hàn và thiếc trong danh mục dụng cụ; kỹ thuật hàn chi tiết sẽ có bài riêng ở Chương 01.

## Bài tập

1. Khi chạm hai que đo vào nhau ở thang thông mạch nhưng đồng hồ im lặng, bạn có nên dùng nó đo chân 3,3 V rồi tin kết quả đó không? Cần kiểm tra những gì trước?
2. Bạn muốn đo trị số của một điện trở 10 kΩ đang gắn trên đường nguồn của mạch ESP32 đang cấp điện. Vì sao phép đo này không được phép thực hiện, và cách đo đúng là gì?
3. Một mối hàn có hình dạng như giọt cầu nằm tròn trên chân linh kiện. Người hàn đã làm sai ở khâu nào (làm nóng mối hay đưa thiếc)? Thiếc Sn63 đường kính 0,8 mm hỗ trợ kiểm soát mối hàn như thế nào?
4. Có người cắm tạm dây động cơ đang kẹt trục vào lỗ breadboard vì ngại lấy tua-vít vặn vào trạm vít. Sự cố điện nào sẽ xảy ra, và dây động cơ cần được đấu vào đâu?
5. Ảnh kiểm kê Đợt 1 của bạn có đồng hồ và mỏ hàn, nhưng thiếu giá đỡ, thiếc hàn và kìm cắt. Món thiếu nào có thể gây cháy nổ hoặc bỏng ngay cả trước khi bước sang Chương 01?

<details>
<summary>Gợi ý đáp án</summary>

1. Không. Đồng hồ không kêu bíp khi chập que chứng tỏ đường đo chưa thông. Cần kiểm tra lại vị trí núm xoay, lỗ cắm que đo và pin của đồng hồ trước khi đo điện áp.
2. Thang đo ohm tự bơm dòng thử nên sẽ xung đột với nguồn đang cấp trên mạch. Cần rút nguồn mạch, nhấc một chân điện trở ra khỏi mạch (nếu cần) rồi mới đo ở trạng thái mất điện.
3. Chân linh kiện và pad đồng chưa được làm nóng đủ; thiếc bị chấm từ mũi mỏ sang nên không bám ướt. Dây thiếc mảnh 0,8 mm giúp bạn cấp lượng thiếc nhỏ, đều trực tiếp vào mối nóng thay vì làm ngập thiếc.
4. Tiếp điểm lò xo của breadboard có điện trở tiếp xúc đáng kể đối với dòng động cơ, dẫn đến nóng chảy nhựa và sụt áp. Dây động cơ phải nối vào trạm vít của mạch lái hoặc đầu nối chịu dòng phù hợp; breadboard chỉ dùng cho đường tín hiệu.
5. Thiếu giá đỡ mỏ hàn. Đặt mỏ hàn nóng trực tiếp lên mặt bàn hoặc lên dây điện gây nguy cơ bỏng và cháy ngay lập tức. Thiếu thiếc hay kìm cắt chỉ làm gián đoạn thao tác, không thay thế được vai trò an toàn của giá đỡ.

</details>

## Đọc thêm

- [Cách dùng đồng hồ vạn năng (SparkFun)](https://learn.sparkfun.com/tutorials/how-to-use-a-multimeter) — hướng dẫn trực quan về đo điện áp, đo thông mạch và cách tránh bẫy lỗ đo dòng.
- [Tài liệu Arduino](https://docs.arduino.cc/) — không phải cẩm nang dụng cụ, mà là nơi bạn sẽ thực hành LED và nút nhấn trong danh sách Đợt 1 khi có mạch; không nên bắt đầu ngay bằng các bài hướng dẫn điều khiển động cơ từ trang chủ.

## Mua ở Việt Nam

Chỉ mua những món còn thiếu từ bảng kiểm kê của bạn, tránh mua trùng. Danh sách vật tư đầy đủ cho robot vẫn nằm ở [bài 00-05]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %}). Bảng giá tham khảo dưới đây được ghi nhận từ Hshop ngày **23 tháng 9 năm 2026**:

| Dụng cụ | Giá tham khảo | Đường dẫn |
| --- | ---: | --- |
| Đồng hồ UNI-T UT33D+ | 285.000 ₫ | [UT33D+](https://hshop.vn/dong-ho-van-nang-dien-tu-digital-multimeter-uni-t-ut33d-chinh-hang) |
| Đồng hồ Wadfow WDM1501 | 185.000 ₫ | [WDM1501](https://hshop.vn/dong-ho-van-nang-ky-thuat-so-vom-wadfow-wdm1501-digital-multimeter-true-rms) |
| Mỏ hàn Wadfow 60 W | 75.000 ₫ | [WEL3616](https://hshop.vn/mo-han-60w-wadfow-wel3616-soldering-iron) |
| Giá đỡ mỏ hàn tròn | 40.000 ₫ | [giá đỡ](https://hshop.vn/de-gac-mo-han-tron-b-2-co-khay-roi) |
| Thiếc Sunchi 0,8 mm Sn63/Pb37 | 24.000 ₫ | [thiếc hàn](https://hshop.vn/thiec-han-sunchi-kp26-0-8mm-sn63-pb37-solder-wire) |
| Kìm cắt 170 | 35.000 ₫ | [kìm cắt](https://hshop.vn/kim-cat-day-dien-nho-170-cat-chan-linh-kien-dien-tu) |
| Breadboard 830 lỗ | 35.000 ₫ | [breadboard](https://hshop.vn/test-board-cammb-102) |

Bạn chỉ cần chọn một trong hai mẫu đồng hồ trên. Với dây cắm, LED, nút nhấn và cáp USB truyền dữ liệu, bạn có thể tìm qua các trang tìm kiếm sau: [Shopee, dây cắm breadboard](https://shopee.vn/search?keyword=d%C3%A2y%20c%E1%BA%AFm%20breadboard), [Lazada, dây jumper đực đực](https://www.lazada.vn/catalog/?q=d%C3%A2y%20jumper%20%C4%91%E1%BB%B1c%20%C4%91%E1%BB%B1c), và nếu cần kìm tuốt dây riêng thì xem [Shopee, kìm tuốt dây](https://shopee.vn/search?keyword=k%C3%ACm%20tu%E1%BB%91t%20d%C3%A2y). Ngoài ra, [Thế Giới IC](https://www.thegioiic.com/) và [IC Đây Rồi](https://icdayroi.com/) là hai trang chủ cửa hàng linh kiện thuận tiện nếu bạn đến mua trực tiếp tại quầy. Chưa cần đưa máy hiện sóng, máy phân tích logic hay nguồn bàn giới hạn dòng vào hóa đơn giai đoạn này.
