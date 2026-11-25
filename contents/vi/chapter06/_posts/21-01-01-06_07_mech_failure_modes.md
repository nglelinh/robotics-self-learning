---
layout: post
title: "Hỏng hóc cơ khí và chống kéo dây"
chapter: "06"
order: 7
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter06
lesson_type: required
draft: false
---

Thời lượng ước tính: **60–80 phút**, bao gồm một lần kiểm tra lực kéo khi đã ngắt nguồn và thực hành làm điểm giảm lực kéo dây (strain relief) có chụp ảnh trước và sau.

Trong các cuộc thi robotics sinh viên, tỷ lệ robot dừng cuộc chơi vì *lỗi thuật toán* thực ra thấp hơn nhiều so với tỷ lệ dừng vì *lỗi cơ – điện cơ bản*: một đầu dây nguồn bị đứt ngầm sát mối hàn sau 50 lần gập mở, một bánh xe tự văng ra vì thiếu keo khóa ren, hay một dây tín hiệu bị kéo căng làm tuột giắc cắm giữa chừng. Nhận diện sớm các **chế độ hỏng hóc cơ khí (failure modes)** và thiết kế **chống kéo dây (strain relief)** giúp robot của bạn sống sót qua hàng trăm giờ chạy thử thay vì hỏng đúng hôm chấm đồ án.

## Kiến thức cần nhớ: Mỏi kim loại, Sụt áp dây dẫn và Quản lý bó dây (Harnessing)

### 1. Đứt ngầm do mỏi uốn (Fatigue Fracture) và Chống kéo dây (Strain Relief)
Đồng mềm chịu kéo thẳng khá tốt, nhưng nếu bị uốn đi uốn lại ngay tại đúng ranh giới cứng của **mối hàn thiếc** hoặc đầu chân giắc cắm, dây sẽ đứt gãy do mỏi chỉ sau vài chục chu kỳ. **Strain relief** (dùng dây rút cố định bó dây vào khung *trước* khi đi vào bo mạch, dùng ống co nhiệt bọc chân mối hàn, và giữ bán kính uốn tối thiểu $$R_{\min} \approx 8\text{–}10 \times D_{\text{dây}}$$) chuyển lực giật cơ học vào khung xe thay vì vào mối hàn mỏng manh.

### 2. Chống lỏng cơ khí và tập trung ứng suất tại góc nhọn
Các vết nứt trên tấm mica hay chi tiết in 3D gần như luôn bắt đầu từ một **góc vuông $$90^\circ$$ sắc nhọn** nơi ứng suất tập trung gấp nhiều lần. Bo tròn góc trong (fillet bán kính $$2\text{–}3\text{ mm}$$) và không khoan lỗ ốc quá sát mép tấm (giữ khoảng cách mép $$\ge 1{,}5\times$$ đường kính lỗ) ngăn nứt vỡ hiệu quả.

### 3. Chọn sai tiết diện dây (AWG) — nguyên nhân ngầm gây sụt áp và reset vi điều khiển
Dây jumper breadboard (26–28 AWG) có điện trở rất lớn, chỉ chịu được vài trăm mA. Dùng dây jumper mảnh để cấp dòng $$3\text{ A}$$ cho động cơ không chỉ gây nóng chảy vỏ nhựa mà còn làm sụt áp mạnh trên đường dây khiến mạch điều khiển reset bất thường!

### Giải thích: Cầm tay tính sụt áp dây nguồn 24 AWG vs. 18 AWG và bán kính uốn bó dây

**Phần A — So sánh sụt áp trên dây nguồn tổng dài $$0{,}5\text{ m}$$ (tổng khứ hồi dây dương + dây mass $$L = 1{,}0\text{ m}$$) khi robot kéo dòng $$I = 3{,}0\text{ A}$$:**
- **Dùng dây mảnh 24 AWG** (điện trở $$r \approx 0{,}084\,\Omega/\text{m}$$):
  $$\Delta V_{24} = I \cdot R = 3{,}0 \times 0{,}084 = 0{,}252\text{ V}, \qquad P_{\text{nóng}} = I^2 R = 9 \times 0{,}084 \approx 0{,}76\text{ W}.$$
  *(Nếu là dây jumper 28 AWG với $$r \approx 0{,}213\,\Omega/\text{m}$$, sụt áp vọt lên **$$0{,}64\text{ V}$$** và dây nóng **$$1{,}92\text{ W}$$**!)*
- **Dùng dây nguồn chuẩn 18 AWG** (điện trở $$r \approx 0{,}021\,\Omega/\text{m}$$):
  $$\Delta V_{18} = 3{,}0 \times 0{,}021 = 0{,}063\text{ V}, \qquad P_{\text{nóng}} = 9 \times 0{,}021 \approx 0{,}19\text{ W}$$
  — giảm sụt áp và nhiệt tổn hao tới **4 lần**!

**Phần B — Kiểm tra bán kính uốn an toàn cho bó dây động (trên khớp quay/nắp mở):**
Với một bó dây bọc lưới đường kính ngoài $$D = 4\text{ mm}$$, bán kính uốn động tối thiểu theo quy tắc $$8\text{–}10\times D$$ là:
$$R_{\min} = 8 \times 4\text{ mm} = 32\text{ mm}\;(\text{đến } 40\text{ mm}).$$
Bẻ gập bó dây thành góc nhọn bán kính $$5\text{ mm}$$ sẽ làm gãy lõi đồng bên trong sau vài chục lần mở nắp bảo trì!

## Mục tiêu học

Sau bài này, các bạn nhận diện được bốn dạng hỏng cơ khí phổ biến: bánh xe trượt kêu tách trong khi encoder vẫn đếm xung, càng hoặc moay-ơ nhựa mòn răng, mối hàn đứt ngầm do khung rung uốn và bánh xe cọ khung gây mùi khét do động cơ quá tải. Các bạn biết lắp điểm giảm lực kéo dây (strain relief) kết hợp vòng dây dự phòng để bảo vệ mối hàn, đồng thời soạn hai mục kiểm tra bắt buộc trước khi chạy Capstone A.

## Kiến thức cần có

Kiến thức từ Bài 01 đến Bài 06: $$b$$ và $$r$$, cách siết vít cố định trục lên mặt vát chữ D, tỉ số truyền, khoảng đuôi bánh caster và tính chất vật liệu khung. Chương 05 đã cung cấp khái niệm dòng kẹt của động cơ; trong bài thực hành này, nguồn luôn tắt hoàn toàn.

## Vì sao bài này quan trọng với Capstone A và ROS

ROS tính toán quỹ đạo odometry mượt mà dựa vào xung encoder kết hợp các tham số $$i$$, $$b$$, $$r$$. Tuy nhiên, nhiều hỏng hóc cơ khí vẫn cho ra tín hiệu xung hoàn hảo trong khi chuyển động thực trên sàn bị sai lệch: vít cố định trục trượt khỏi mặt vát, moay-ơ mòn răng, bánh xe cọ khung hay bánh caster mất tải. Nhìn trên đồ thị topic, chúng dễ bị nhầm là lỗi cấu hình tham số, nhưng bản chất lại là lỗi cơ khí phải xử lý bằng tay khi đã ngắt pin trước khi tinh chỉnh phần mềm.

Tương tự, thiếu giảm lực kéo dây thường chỉ bộc lộ sau một thời gian chạy thử: mỗi cú xóc làm dây uốn ngay tại mối hàn, dẫn đến mỏi đồng và đứt ngầm khiến lệnh `cmd_vel` vẫn gửi bình thường nhưng động cơ đã mất điện.

## Những hỏng tìm được bằng tay

**Vít cố định trục trượt khỏi mặt vát chữ D:** Moay-ơ phát tiếng tách và bánh xe khựng lại, nhưng trục động cơ cùng encoder vẫn quay bình thường. Odometry vẫn cộng dồn quãng đường $$r \Delta\theta$$ như thể bánh đang lăn, tạo ra sai số odometry ảo kinh điển. Dù đã lắp đúng ở Bài 02, bạn vẫn cần kiểm tra lại sau mỗi lần vận chuyển vì vít tỳ lệch sang phần tròn sẽ lỏng dần theo thời gian.

**Càng servo hoặc moay-ơ nhựa bị mòn răng:** Các chi tiết nhựa mềm giá rẻ dễ bị trục kim loại làm mòn tròn rãnh răng. Khi răng đã mất, ốc giữ vẫn có cảm giác chặt nhưng trục quay tự do bên trong lỗ. Giải pháp duy nhất là thay càng hoặc moay-ơ mới; bôi keo lên răng đã mòn chỉ mang tính đối phó tạm thời và sẽ sớm hỏng lại.

**Mỏi dây tại mối hàn:** Khi khung xe rung hoặc uốn nhẹ, mối hàn là điểm cứng cố định nên sợi đồng bị gãy mỏi bên trong lớp vỏ cách điện ngay sát chân mối hàn (cách vài milimét), dù nhìn bề ngoài dây vẫn nguyên vẹn. Giảm lực kéo dây (strain relief) giúp chuyển vùng uốn ra khỏi mối hàn: dùng dây rút nhựa hoặc một giọt keo nến cố định dây vào tấm khung để mối hàn không còn chịu lực kéo. Phía trước điểm cố định, luôn chừa một vòng dây dự phòng (độ chùng có chủ đích) để dây có khoảng nhường khi cụm linh kiện rung lắc. Áp dụng cách này cho cả dây nguồn động cơ và dây tín hiệu encoder — dây encoder đứt ngầm sẽ trông giống hệt cảm biến hỏng trong firmware Chương 04.

**Bánh xe cọ khung:** Mặt lốp chạm vào tấm khung hoặc đầu ốc lồi ra khiến tốc độ giảm mạnh, dòng điện tăng tiến sát dòng kẹt (Chương 05) và động cơ nhanh chóng có mùi khét. Bạn dễ dàng phát hiện lỗi này khi ngắt pin và xoay bánh bằng tay: mỗi vòng quay sẽ nghe tiếng cọ sột soạt. Hãy dịch bánh ra ngoài hoặc xử lý phần vật cản trước khi nghi ngờ lỗi mạch cầu H.

**Bánh caster rung lắc ở tốc độ cao:** Đầu xe dao động trái phải do khoảng đuôi (trail) bị lắp ngược, quá ngắn, hoặc trọng tâm (Bài 01) phân bổ quá ít lực đè lên bánh caster khiến bánh không ổn định hướng. Lỗi này chỉ khắc phục được bằng cách chỉnh lại cơ cấu caster và trọng tâm, không thể bù bằng bộ lọc phần mềm.

**Pin bị trượt:** Khối pin lỏng lẻo sẽ dịch chuyển trọng tâm ra ngoài tam giác đỡ, làm bánh caster nhấc bổng hoặc khiến một bánh chủ động mất độ bám và xe xoay ngang. Hãy dùng đai in 3D hoặc dây rút cố định chắc chắn pin đúng vị trí đã đo $$b$$ ở Bài 01.

![Những vùng khung mà các dạng hỏng này sống: bánh, đường trục, caster, và dây chạy dọc tấm]({{ site.imgurl }}/generated/chassis_measures.png)

Hãy dùng sơ đồ trên như bản đồ kiểm tra thực tế: chạm và kiểm tra lần lượt cả hai moay-ơ, khe hở hai bánh xe, càng caster, vị trí đặt pin và mọi đoạn dây đi ra từ mối hàn.

## Ví dụ tính tay

Giả sử encoder ghi nhận đủ một vòng quay tại trục bánh (sau khi chia tỉ số truyền), nhưng vít cố định trục bị trượt trọn vòng đó. Với bán kính lăn $$r = 31.2$$ mm, quãng đường ảo sinh ra là:

$$
s_{\text{phantom}} = 2\pi r = 2\pi \times 31.2 \approx 196\ \text{mm}.
$$

Bản đồ sẽ ghi thêm gần 20 cm mà xe thực tế chưa hề di chuyển. Chỉ cần hai lần trượt như vậy trên mỗi mét hành trình là tạo ra sai số 40 cm — mức sai lệch mà việc chỉnh hiệp phương sai (covariance) không thể che giấu trung thực. Giải pháp bắt buộc là kiểm tra cơ khí: đưa vít đúng mặt vát, vặn thử bánh và chụp ảnh xác nhận.

Bánh cọ khung cũng gây ra rủi ro nhiệt tương tự: thay vì chạy ở dòng không tải nhỏ (Chương 05), ma sát kéo điểm làm việc lên gần dòng kẹt làm cuộn dây nóng nhanh. Không cần tính thêm thông số mới; yêu cầu tiên quyết là loại bỏ hoàn toàn tiếng cọ trước khi cấp lại điện áp.

## Lab: giật thử và một điểm neo

### An toàn

Ngắt pin, rút nguồn mạch cầu H và rút cáp USB nếu mạch điều khiển đang gắn trên khung. Mọi thao tác kéo kiểm tra đều thực hiện bằng tay khi không có điện. Keo nến là nguồn nhiệt duy nhất trong bài: giữ đầu súng bắn keo cách xa lớp cách điện dây và tay người thao tác. Không cấp điện cho động cơ rồi giữ bánh để thử độ bền mối dây.

### BOM

| Hạng mục | Vai trò |
|------|------|
| Khung, hoặc một dây động cơ trên bàn nếu tấm chưa về | Các mối |
| Dây rút, hoặc một cây keo nến và súng | Một điểm giảm lực kéo dây |
| Điện thoại | Trước và sau |
| `lab-notes.md` | Hai mục kiểm ngày Capstone |

### Các bước

1. Khi nguồn đã tắt, kéo nhẹ từng đầu giắc bằng cách cầm vào phần vỏ nhựa của giắc (không nắm lõi dây). Nếu giắc lỏng, cắm chặt lại và có thể chấm một giọt keo nến nhỏ cố định vỏ giắc nếu kết cấu cho phép.
2. Quan sát và thử uốn nhẹ từng dây gần mối hàn; nếu mối hàn bị dịch chuyển hoặc chịu lực uốn trực tiếp, vị trí đó đang thiếu giảm lực kéo dây.
3. Chụp ảnh vị trí mối dây dễ hỏng nhất. Gắn thêm dây rút hoặc điểm neo keo nến sao cho đoạn dây bắt đầu uốn nằm cách mối hàn ít nhất 1 cm, đồng thời chừa một vòng dây chùng dự phòng. Chụp ảnh sau khi hoàn thiện.
4. Dùng tay xoay và vặn thử từng bánh xe để xác nhận vít cố định trục bám chắc và lốp không cọ vào khung hay đầu ốc.
5. Thử đẩy nhẹ khối pin; nếu pin có thể xê dịch, ghi chú cần bổ sung đai giữ pin.
6. Viết hai mục kiểm tra cơ khí sẽ thực hiện vào ngày chạy Capstone theo đúng thứ tự trước khi bất kỳ ai gửi lệnh `cmd_vel`.

### Kết quả mong đợi

Một cặp ảnh trước và sau của mối dây đã được làm giảm lực kéo dây, kèm hai mục kiểm tra cụ thể trong sổ tay (ví dụ: kiểm tra vít cố định trục trên mặt vát và kiểm tra không có tiếng cọ khi xoay bánh bằng tay). Khi lắc nhẹ vòng dây dự phòng, mối hàn phải đứng yên hoàn toàn.

### Lỗi thường gặp

| Các bạn thấy | Thường nghĩa là |
|--------------|------------------------|
| Bánh kêu tách, trục không theo | Vít cố định trục trượt khỏi mặt vát, hoặc moay-ơ mòn răng |
| Sợi đứt ngay cạnh một mối nhìn vẫn đẹp | Mỏi; thêm giảm lực kéo dây trên mối thay thế |
| Một tiếng cạo mỗi vòng, và trí nhớ về mùi động cơ ở Chương 05 | Bánh cà |
| Caster đập trái phải | Khoảng đuôi hoặc trọng tâm |
| Pin dịch khi nghiêng tấm | Thiếu đai; caster sẽ mất tải ở lần tăng tốc đầu |

## Mua ở Việt Nam / Where to buy in Vietnam

Một túi dây rút nhựa và keo nến hữu ích hơn nhiều so với việc mua động cơ mới. Chỉ cần mua thêm bánh xe hoặc moay-ơ dự phòng nếu chi tiết hiện tại đã bị mòn tròn lỗ trục.

| Mua gì | Từ khóa | Khoảng giá (VND) | Ghi chú |
|------|----------|------------------|-------|
| Dây rút | `dây rút nhựa` | 10.000–30.000 | Giảm lực kéo dây và đai pin tạm |
| Keo nến | `keo nến` | 15.000–40.000 | Neo dây, giữ keo khỏi tiếp điểm |
| Bánh TT dự phòng | `bánh xe cao su 65mm` | 15.000–45.000 | Nếu moay-ơ đã mòn răng |

Các trang tìm mua:

- [Shopee: dây rút](https://shopee.vn/search?keyword=d%C3%A2y%20r%C3%BAt%20nh%E1%BB%B1a)
- [Lazada: keo nến](https://www.lazada.vn/catalog/?q=keo%20n%E1%BA%BFn)
- [Hshop: bánh xe](https://hshop.vn/search?q=b%C3%A1nh+xe+cao+su)
- [Thế Giới IC](https://www.thegioiic.com/search?q=d%C3%A2y%20%C4%91i%E1%BB%87n)

Giá bán có thể thay đổi theo thời điểm. Một đầu giắc tuột ra là lỗi cơ khí – hàn mạch (Chương 01), không phải lỗi phần mềm.

## Video tham khảo

- **Xem trước:** [How to measure Gear Backlash and Center Distance](https://www.youtube.com/watch?v=8fYwUV6QV8c) — Evolvent Design, tiếng Anh. Hướng dẫn đo độ rơ giữa hai bánh răng — khe hở gây ra vùng trễ khi encoder đã đếm nhưng bánh chưa dịch chuyển.
- [What is Bearing? Types of Bearings and How they Work?](https://www.youtube.com/watch?v=8q25EUszBSI) — The Engineers Post, tiếng Anh. Nhận diện hỏng hóc bạc đạn và lệch trục trước khi cố siết chặt thêm.

## Bài tập

1. Robot di chuyển rất chậm trên sàn trong khi số xung encoder tăng rất nhanh. Nêu tên dạng hỏng và cách kiểm tra bằng tay.
2. Phần răng nhựa bên trong một càng servo đã bị mòn tròn dù ốc bắt vẫn chặt. Cần thay chi tiết nào, và vì sao bôi keo không phải giải pháp đáng tin cậy?
3. Dây động cơ được hàn và kéo căng thẳng tới mạch cầu H, không có độ chùng. Cần bổ sung những gì, và mối hàn phải có trạng thái ra sao khi lắc thử dây?
4. Động cơ kéo dòng cao, quay chậm và có mùi khét, dù vít cố định trục vẫn giữ chắc. Bạn cần tìm lỗi cản cơ khí nào?
5. Viết hai mục kiểm tra cho ngày chạy Capstone thành câu hoàn chỉnh sao cho thành viên khác có thể thực hiện khi pin vẫn đang ngắt.

### Gợi ý đáp án

1. Bánh xe bị trượt trên trục (vít cố định trục trượt khỏi mặt vát hoặc moay-ơ mòn răng). Kiểm tra bằng cách tắt nguồn rồi dùng tay vặn thử bánh; bánh không được trượt hay kêu tách.
2. Thay càng servo mới. Keo bôi lên phần răng đã tròn sẽ nhanh chóng bong ra ở lần chịu tải tiếp theo.
3. Bổ sung điểm giảm lực kéo dây (dây rút hoặc keo nến neo vào khung) cùng một vòng dây chùng dự phòng. Khi lắc dây, mối hàn phải đứng yên hoàn toàn.
4. Bánh xe cọ vào tấm khung hoặc đầu ốc. Xoay bánh bằng tay khi tắt nguồn để tìm và loại bỏ vị trí cọ sát.
5. Chọn bất kỳ hai mục kiểm tra nào trong bài thực hiện ở trạng thái tắt nguồn (ví dụ: vít cố định trục tỳ đúng mặt vát, xoay bánh không có tiếng cọ, caster có khoảng đuôi và chịu tải ổn định, pin cố định không trượt, mọi mối hàn đã được giảm lực kéo dây), kèm tiêu chí rõ ràng thế nào là đạt.

## Đọc thêm

- [Adafruit, dây và giắc](https://learn.adafruit.com/wires-and-connectors/wire) — kiến thức về dây dẫn, mối nối và nguyên nhân dây đồng đứt mỏi sát mối hàn.
- [SparkFun, căn bản giắc nối](https://learn.sparkfun.com/tutorials/connector-basics/all) — phân loại giắc nối và quy tắc cầm vỏ giắc khi tháo lắp.
- [Gỡ lỗi in trên RepRap](https://reprap.org/wiki/Print_Troubleshooting) — phân tích lỗi mòn răng moay-ơ nhựa và nứt lớp in nếu chi tiết hỏng là chi tiết in 3D.
