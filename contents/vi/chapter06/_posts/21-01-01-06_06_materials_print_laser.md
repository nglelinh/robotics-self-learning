---
layout: post
title: "Vật liệu khung: in 3D vs cắt laser"
chapter: "06"
order: 6
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter06
lesson_type: required
draft: false
---

Thời lượng ước tính: **70–90 phút**. Bạn có thể hoàn thành bài thực hành chỉ với một bức ảnh chi tiết in 3D bị gãy; việc có sẵn máy in hay không là tùy chọn.

Khi bắt đầu chế tạo khung robot trong xưởng lab, hai công cụ chế mẫu nhanh phổ biến nhất nằm ngay trước mắt bạn: **máy in 3D FDM (nhựa PLA/PETG)** và **máy cắt laser (mica Acrylic / gỗ dán MDF/Plywood)**. Chọn sai công cụ không chỉ tốn hàng giờ chờ in mà còn tạo ra một bộ khung mềm oặt hoặc giòn gãy ngay cú va chạm đầu tiên. Bí quyết của người làm cơ khí robot là kết hợp cả hai: dùng cắt laser cho **các tấm khung phẳng chịu lực lớn** và dùng in 3D cho **các gá lắp hình học phức tạp** (giá đỡ động cơ, ngàm cảm biến, ống dẫn dây).

## Kiến thức cần nhớ: Cơ học vật liệu, Tính dị hướng của in 3D và Độ cứng uốn

### 1. Tính dị hướng (Anisotropy) của in 3D FDM
Chi tiết in 3D được đắp từng lớp nhựa nóng chảy chồng lên nhau theo trục Z. Vì liên kết giữa các lớp yếu hơn liên kết dọc sợi nhựa, một giá đỡ động cơ chịu lực kéo **vuông góc với mặt lớp in** rất dễ tách lớp (delamination) và gãy đôi! Định hướng chi tiết trên bàn in sao cho phương chịu kéo chính nằm dọc theo mặt phẳng XY là kỹ năng cần có của người thiết kế CAD cho in 3D.

### 2. Nhựa PLA vs. PETG vs. Tấm cắt Laser (Acrylic / Plywood)
- **PLA:** cứng, dễ in, độ chính xác cao, nhưng giòn và mềm oặt ngay ở $$55\text{–}60^\circ\text{C}$$ (gắn trực tiếp lên động cơ nóng sẽ bị biến dạng!).
- **PETG / ABS:** dẻo dai hơn, chịu nhiệt tốt hơn ($$75\text{–}95^\circ\text{C}$$), rất hợp làm gá động cơ và chi tiết chịu va đập.
- **Acrylic (Mica) & Gỗ dán cắt laser:** cắt xong cả bộ khung 2 tầng chỉ trong **5 phút** (so với 8 tiếng in 3D!), độ cứng phẳng cực tốt, nhưng Acrylic giòn khi khoan/va chạm mạnh ở góc vuông sắc (luôn bo góc `fillet`!).

### 3. Quy luật lập phương của độ cứng uốn ($$I = \frac{b h^3}{12}$$)
Độ chống võng của một tấm khung phẳng tỉ lệ với mô-men quán tính mặt cắt $$I = \frac{b h^3}{12}$$ (với $$h$$ là chiều dày tấm). Tăng độ dày tấm lên gấp đôi khiến khối lượng tăng **2 lần**, nhưng độ cứng chống uốn tăng vọt lên tới **$$2^3 = 8$$ lần**!

### Giải thích: Cầm tay so sánh độ cứng uốn và khối lượng giữa tấm khung in 3D và tấm cắt laser

Xét một tấm sàn khung robot kích thước **$$200\text{ mm} \times 150\text{ mm}$$** (diện tích $$A = 300\text{ cm}^2$$):

1. **Hiệu ứng tăng độ dày từ $$h_1 = 3\text{ mm}$$ lên $$h_2 = 6\text{ mm}$$:**
   $$\frac{I_2}{I_1} = \left(\frac{h_2}{h_1}\right)^3 = \left(\frac{6}{3}\right)^3 = 2^3 = 8\times\text{ cứng hơn!}$$
   Cùng một tải trọng pin đặt ở giữa sàn, độ võng giảm xuống chỉ còn **1/8**, trong khi trọng lượng tấm chỉ tăng $$2\times$$ (hoặc thậm chí ít hơn nếu ta thêm các gân tăng cứng thay vì làm đặc toàn bộ!).

2. **So sánh khối lượng tấm dày $$h = 4\text{ mm}$$ (thể tích $$V = 300 \times 0{,}4 = 120\text{ cm}^3$$):**
   - **Tấm in 3D PLA** (mật độ nhựa đặc $$1{,}24\text{ g/cm}^3$$, in 20% infill + vỏ thành → mật độ hiệu dụng $$\approx 0{,}45\text{ g/cm}^3$$):
     $$m_{\text{PLA}} \approx 120 \times 0{,}45 = 54\text{ g}$$ (nhẹ, nhưng tốn ~3–4 giờ in).
   - **Tấm Acrylic cắt laser đặc** ($$\rho = 1{,}18\text{ g/cm}^3$$):
     $$m_{\text{Acrylic}} = 120 \times 1{,}18 = 141{,}6\text{ g}$$ (nặng hơn ~88 g, nhưng cắt xong trong **2 phút**, siêu phẳng và cứng!).

## Mục tiêu học

Sau bài này, các bạn hiểu lý do nên chọn tấm khung mica 2WD mua sẵn cho Capstone A và chỉ dùng in 3D cho các giá đỡ, giá cảm biến và đai giữ pin. Các bạn tính được sự thay đổi kích thước lỗ khi cắt laser với khe cắt (kerf) 0,1–0,2 mm, biết ngưỡng nhiệt độ làm mềm nhựa PLA trong khoang ô tô kín, và biết xoay hướng in giá động cơ sao cho lực siết bu-lông không tách các lớp in ra khỏi nhau.

## Kiến thức cần có

Các bạn đã nắm hình học khung xe ở Bài 01 và quy cách ốc M3 ở Bài 02. Không cần phần mềm CAD bản quyền; một bản phác thảo bằng bút chì có ghi rõ chiều dày theo milimét là đủ.

## Vì sao bài này quan trọng với Capstone A và ROS

Capstone A cần lăn bánh được trong tháng này. In 3D toàn bộ khung xe sẽ tốn nhiều thời gian trên máy in (thậm chí bạn chưa có máy), và khung bằng nhựa PLA dễ bị cong vênh nếu để trong ô tô đỗ dưới nắng trước khi kịp hoàn thiện URDF. Phương án hợp lý nhất là mua sẵn khung mica 2WD, chỉ in 3D những chi tiết bộ kit không có như giá gắn cảm biến siêu âm, đai cố định pin (Bài 07) hoặc nắp che mối hàn.

ROS không quan tâm vật liệu khung là loại nhựa nào; nó chỉ phụ thuộc vào vị trí chính xác của hai bánh xe. Nếu giá động cơ bị nứt hoặc biến dạng, vị trí bánh thay đổi và khổ vết $$b$$ đã đo không còn đúng nữa. Chọn đúng vật liệu và hướng in chính là cách giữ giá trị $$b$$ ổn định đúng như tham số trong `diff_drive_controller`.

## Tấm mica, giá in

Mica đúc dày khoảng 3 mm là vật liệu phổ biến nhất cho tấm khung kit. Mica phẳng, cắt laser sắc nét nhưng khá giòn. Nếu siết ốc vào một lỗ quá chật, phần ren sẽ tạo ứng suất nêm và gây nứt lan giữa các lỗ. Do đó, với mỗi ốc M3, hãy dùng lỗ thông và bắt đai ốc nyloc (Bài 02) ở mặt sau. Mica cũng không phù hợp cho các ngàm cài đàn hồi; nếu cần ngàm cài, hãy dùng nhựa PETG hoặc bỏ thiết kế ngàm khỏi Capstone A.

Khe cắt laser (kerf) là bề rộng phần vật liệu bị tia laser đốt mất, thường vào khoảng 0,1–0,2 mm trên máy cắt laser phổ thông khi cắt mica. Vì xưởng cắt đúng theo đường nét bản vẽ, đường kính lỗ cắt thực tế sẽ lớn hơn đường kính vẽ một lượng xấp xỉ khe cắt:

$$
d_{\text{cut}} \approx d_{\text{drawn}} + k.
$$

Nếu vẽ lỗ thông 3,2 mm với khe cắt 0,2 mm, lỗ thực tế đạt khoảng 3,4 mm — ốc M3 đi qua dễ dàng. Ngược lại, nếu vẽ 3,0 mm với ý định để ốc tự tạo ren trong mica, lỗ cắt ra khoảng 3,2 mm khiến ốc bị lỏng; còn cố siết chặt quá tay sẽ làm nứt tấm. Khi gửi xưởng cắt, hãy xuất file DXF theo đơn vị milimét, đảm bảo mọi đường biên đều khép kín và ghi rõ chiều dày tấm vật liệu. Một đường biên bị hở có thể khiến máy cắt bỏ qua hoặc kết thúc đường cắt sai ý muốn.

Nhựa PLA dễ in nhưng bắt đầu mềm ở khoảng 55–60 °C — mức nhiệt rất dễ đạt tới trong khoang ô tô đỗ ngoài trời vào buổi chiều ở Việt Nam. Một giá đỡ vuông vức buổi sáng có thể bị biến dạng trước giờ học. Nhựa PETG chịu nhiệt tốt hơn, dù khi in dễ tạo sợi mảnh (stringing) cần gọt nhẹ bằng dao sau khi in.

Với các giá đỡ chịu lực như giá động cơ, yếu tố quyết định độ bền là hướng in. Chi tiết in 3D yếu nhất theo phương vuông góc với mặt phẳng lớp in (liên kết giữa các lớp yếu hơn sợi nhựa liên tục). Nếu lực siết bu-lông hoặc mô-men động cơ tác động theo hướng bóc tách hai lớp in, tai giá đỡ sẽ dễ dàng bị gãy. Hãy xoay mô hình trên bàn in sao cho mặt phẳng chịu lực kéo xé cắt ngang qua các đường lớp — khi đó vết nứt buộc phải bẻ đứt sợi nhựa liên tục thay vì tách dọc đường nối lớp. Một giá đỡ đặt in “trông gọn đẹp” nhưng để phần tai chịu lực xếp chồng song song với mặt nứt sẽ gãy ngay ở lần kẹt bánh đầu tiên.

Bạn hoàn toàn có thể thực hiện việc này mà không cần sở hữu máy in 3D. Phòng lab hoặc dịch vụ in chỉ cần file STL (đơn vị milimét), tên vật liệu (PLA hoặc PETG) và ghi chú hướng in nếu cần. Tương tự, xưởng cắt laser cần file DXF (milimét), đường vẽ khép kín và chiều dày tấm cụ thể. Ghi đủ các thông số này ngay trong đơn đặt hàng sẽ giúp chi tiết gia công đúng kích thước ngay từ lần đầu.

![Tấm khung các bạn đang quyết định không in lại: đo nó, rồi chỉ in những giá nó còn thiếu]({{ site.imgurl }}/generated/chassis_measures.png)

Hình trên là khung xe mua sẵn, nơi $$b$$ và $$r$$ được cố định bởi độ cứng của tấm mica. Chi tiết in 3D phù hợp để giữ cảm biến hoặc pin, nhưng sẽ tiềm ẩn rủi ro sai lệch trục bánh nếu bạn tự in lại toàn bộ khung ngay sát Chương 07.

## Ví dụ tính tay

Giả sử bạn thiết kế bản vẽ rãnh động cơ có lỗ thông M3 với $$d_{\text{drawn}} = 3.2$$ mm và xưởng báo khe cắt $$k = 0.15$$ mm:

$$
d_{\text{cut}} \approx 3.2 + 0.15 = 3.35\ \text{mm}.
$$

Ốc M3 có đường kính đỉnh ren khoảng 3,0 mm, nên lỗ 3,35 mm đủ rộng để ốc đi qua thoải mái và lực kẹp do đai ốc phía sau đảm nhận. Nếu bạn vẽ 2,8 mm với hy vọng ren ốc sẽ bám trực tiếp vào mica:

$$
d_{\text{cut}} \approx 2.8 + 0.15 = 2.95\ \text{mm},
$$

khiến ốc khó lọt qua hoặc tạo lực nêm làm nứt mica. Với đai giữ pin in 3D, mức nhiệt 58 °C trong cabin ô tô đã nằm trong vùng làm mềm của PLA; vì vậy nên chọn nhựa PETG nếu robot có thể phải để trong xe hơi, trong khi tấm khung chính vẫn giữ nguyên là mica mua sẵn.

## Lab: đọc một lớp gãy, phác hướng in

### An toàn

Chi tiết nhựa bị gãy thường có cạnh sắc dọc theo lớp tách; hãy cầm vào mặt cạnh nguyên vẹn, tránh chạm vào mảnh vỡ nhỏ. Nếu đến trực tiếp xưởng cắt laser, bàn máy và vật liệu vừa cắt còn nóng, hãy chờ người vận hành lấy chi tiết ra. Bài này không cần máy in hay dung môi; không dùng keo tùy tiện để “hàn” mica khi đang phân tích dạng hỏng.

### BOM

| Hạng mục | Vai trò |
|------|------|
| Một chi tiết in đã gãy, hoặc một ảnh rõ của nó | Mổ lớp |
| Bút chì, hình cạnh và hình trước | Hướng giá |
| `lab-notes.md` | Phép khe cắt và câu vật liệu |

### Các bước

1. Quan sát kỹ mặt gãy của chi tiết in 3D: các đường lớp hiện lên như những sọc mảnh song song. Xác định xem vết gãy chạy dọc theo ranh giới giữa các sọc hay cắt ngang qua chúng. Nếu chạy dọc theo sọc, tải trọng đã tác động đúng vào mặt phẳng yếu nhất.
2. Phác thảo một giá động cơ TT gồm đế bắt vào khung và phần tai dựng lên để bắt động cơ. Đánh dấu trục siết bu-lông, sau đó vẽ hướng các đường lớp sao cho chúng cắt ngang mặt phẳng chịu lực xé. Ghi rõ “in úp mặt này xuống” lên mặt tiếp xúc với bàn in.
3. Tính một ví dụ kích thước lỗ sau cắt laser cho một lỗ trên bản vẽ của bạn (dùng $$k = 0.2$$ mm nếu xưởng chưa cung cấp thông số). Ghi rõ đường kính vẽ và đường kính dự kiến sau cắt.
4. Viết một câu chốt phương án vật liệu cho Capstone A: dùng khung mica mua sẵn, ghi rõ tên các chi tiết sẽ in (giá đỡ, đai pin) và vật liệu tương ứng.
5. Nếu không có mẫu hỏng thực tế lẫn ảnh tự chụp, hãy dùng ảnh một chi tiết in bị gãy tìm được trong lab và ghi chú rõ nguồn ảnh.

### Kết quả mong đợi

Một ghi chú chỉ ra mặt phẳng yếu của chi tiết in, một bản phác thảo đánh dấu rõ mặt đặt lên bàn in cùng hướng lớp in, và một phép tính khe cắt (ví dụ vẽ 3,2 mm, cắt ra dự kiến 3,4 mm). Câu chốt vật liệu chỉ định mica cho khung chính và PLA hoặc PETG cho giá đỡ (nêu rõ PETG nếu có yêu cầu chịu nhiệt trong ô tô).

### Lỗi thường gặp

| Các bạn thấy | Thường nghĩa là |
|--------------|------------------------|
| Vết nứt đi theo các sọc | Các lớp chính là mặt xé; xoay chi tiết |
| Lỗ chật và mica nứt chân chim | Lỗ vẽ bỏ qua khe cắt, hoặc ốc bị dùng như một tarô |
| Giá vênh sau một quãng nắng | PLA trên khoảng 55–60 °C |
| Xưởng cắt viền ngoài và bỏ lỗ | Đường hở, hoặc lỗ nằm trên một lớp xưởng đã tắt |
| STL trả về bé xíu | File theo inch, hoặc theo centimét, và xưởng đã theo các con số |

## Mua ở Việt Nam / Where to buy in Vietnam

Ưu tiên ngân sách cho bộ khung mica 2WD. Chỉ cần mua cuộn nhựa khi bạn hoặc phòng lab tự in giá đỡ. Cắt laser là dịch vụ gia công tính phí theo file DXF; luôn ghi rõ chiều dày tấm và đơn vị milimét khi gửi file.

| Mua gì | Từ khóa | Khoảng giá (VND) | Ghi chú |
|------|----------|------------------|-------|
| Khung mica 2WD | `khung xe robot 2 bánh` | 80.000–200.000 | Tấm của Capstone |
| Nhựa PLA, 1 kg | `nhựa PLA` | 250.000–450.000 | Dễ in; để xa ô tô kín |
| Nhựa PETG, 1 kg | `nhựa PETG` | 280.000–500.000 | Chịu nhiệt hơn, tạo sợi nhiều hơn |

Các trang tìm mua:

- [Hshop: khung](https://hshop.vn/search?q=khung+xe+robot)
- [Shopee: nhựa PLA](https://shopee.vn/search?keyword=nh%E1%BB%B1a%20PLA)
- [Lazada: nhựa PLA](https://www.lazada.vn/catalog/?q=nh%E1%BB%B1a%20PLA)
- [Thế Giới IC](https://www.thegioiic.com/search?q=nh%E1%BB%B1a%20PLA)

Giá bán có thể thay đổi theo thời điểm. Dịch vụ cắt laser thường đặt trực tiếp tại xưởng địa phương hoặc makerspace; hãy chuẩn bị sẵn file DXF (milimét, đường kín) và xác nhận chiều dày mica họ có sẵn (thường là 3 mm).

## Video tham khảo

- **Xem trước:** [Laser, CNC, or 3D Printer Which One Is RIGHT For You?](https://www.youtube.com/watch?v=6MA1Lv4YilM) — Andy Bird Builds, tiếng Anh. So sánh mục đích sử dụng giữa in 3D, cắt laser và CNC để chọn công nghệ theo yêu cầu lực và độ phẳng thay vì chọn theo máy sẵn có.

## Bài tập

1. Một lỗ được vẽ với đường kính 3,4 mm, khe cắt laser là 0,2 mm. Đường kính dự kiến trên tấm mica là bao nhiêu và ốc M3 có đi qua được không?
2. Bạn cần bắt ốc chắc chắn vào chi tiết nhựa in 3D. Chi tiết phần cứng nào ở Bài 02 thay thế cho việc để ốc tự cắt ren trực tiếp vào nhựa PLA?
3. Tai giá động cơ bị nứt gãy phẳng dọc theo các đường sọc lớp in ngay lần đầu bánh bị kẹt. Mặt phẳng yếu nằm ở đâu và cần xoay bản in lại thế nào?
4. Robot đặt trong ô tô nóng khoảng 58 °C. Loại nhựa in nào có nguy cơ biến dạng đai giữ pin, và nên đổi sang loại nhựa nào?
5. Liệt kê định dạng file, đơn vị và thông tin bắt buộc cần gửi cho xưởng cắt laser, cũng như định dạng file và thông tin cần gửi cho xưởng in 3D.

### Gợi ý đáp án

1. Đường kính dự kiến khoảng 3,6 mm. Vì đỉnh ren M3 gần 3,0 mm nên ốc đi qua thoải mái với khe hở dư; bắt thêm đai ốc phía sau để kẹp chặt.
2. Đai đồng cấy ren bằng nhiệt (threaded insert), kết hợp ốc máy và đai ốc nyloc nếu mối ghép chịu rung.
3. Mặt nứt chính là mặt tiếp giáp giữa các lớp in. Cần xoay chi tiết khi in lại sao cho các đường lớp cắt ngang mặt phẳng chịu lực xé và đánh dấu rõ mặt tiếp xúc bàn in.
4. Nhựa PLA dễ mềm quanh 55–60 °C; nên chuyển sang nhựa PETG cho đai giữ pin.
5. Cắt laser: file DXF, đơn vị milimét, đường vẽ khép kín và chiều dày tấm. In 3D: file STL, đơn vị milimét, tên vật liệu (PLA/PETG) kèm yêu cầu hướng in nếu cần.

## Đọc thêm

- [Gỡ lỗi in trên RepRap](https://reprap.org/wiki/Print_Troubleshooting) — hướng dẫn xử lý lỗi tách lớp, tạo sợi và các lỗi in 3D thường gặp.
- [Polylactic acid](https://en.wikipedia.org/wiki/Polylactic_acid) — đặc tính nhiệt của nhựa PLA và lý do vật liệu mềm trong khoang xe nóng.
- [Laser cutting](https://en.wikipedia.org/wiki/Laser_cutting) — giải thích khái niệm khe cắt (kerf) trong gia công laser.
