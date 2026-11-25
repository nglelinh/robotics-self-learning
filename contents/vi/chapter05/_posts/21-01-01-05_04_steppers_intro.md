---
layout: post
title: "Stepper và microstep"
chapter: "05"
order: 4
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter05
lesson_type: required
draft: false
---

Động cơ bước (stepper) di chuyển theo từng nấc góc rời rạc theo số xung bạn cấp. Bài này trình bày về động cơ bước hybrid $1{,}8^\circ$, tác dụng thực sự của chế độ vi bước (microstep), cách tính và chỉnh điện áp tham chiếu giới hạn dòng trên mạch lái kiểu A4988 mà không vặn biến trở theo cảm tính, cũng như lý do hệ dẫn động của Capstone A vẫn dùng động cơ DC kết hợp encoder.

Nếu bạn từng đứng ngắm một chiếc máy in 3D vẽ từng đường nhựa mảnh như sợi tóc lặp đi lặp lại chính xác đến phần trăm milimet mà *không hề có một cái encoder nào trên trục động cơ*, bạn đã chứng kiến sức mạnh của **động cơ bước (stepper motor)**. Thay vì quay liên tục như động cơ DC, động cơ bước chia một vòng quay thành hàng trăm nấc từ trường rời rạc; mỗi khi bộ điều khiển gửi một xung `STEP`, roto nhảy chính xác thêm đúng một bước góc — biến chuyển động cơ khí thành một bài toán đếm xung số hóa thuần túy!

## Kiến thức cần nhớ: Từ trường bước rời rạc, Vi bước (Microstepping) và Đường cong mô-men

### 1. Cấu trúc cực từ và bước góc cơ bản (Full-Step)
Động cơ bước lưỡng cực phổ biến nhất (NEMA 17) có góc bước cơ bản **$$1{,}8^\circ$$**, tương đương **$$360^\circ / 1{,}8^\circ = 200\text{ bước/vòng}$$**. Nhờ điều khiển hở vòng (open-loop) theo xung `STEP` và chân hướng `DIR`, ta biết chính xác vị trí góc mà không cần cảm biến phản hồi — với điều kiện tuyệt đối là tải không bao giờ vượt quá mô-men giữ làm **trượt bước (missed steps)**.

### 2. Vi bước (Microstepping) — mượt hơn nhờ điều chế dòng hình sin–cos
Chạy bước đủ (full-step) gây rung và cộng hưởng cơ khí mạnh. Driver hiện đại (A4988, DRV8825, TMC2209) điều khiển dòng điện qua hai cuộn dây A và B theo hàm $$\cos\theta$$ và $$\sin\theta$$ để chia mỗi bước đủ thành $$4, 8, 16$$ hoặc $$256$$ **vi bước (microsteps)**. Chuyển động trở nên êm ru, nhưng hãy nhớ một sự thật vật lý quan trọng: vi bước giúp **tăng độ mượt**, chứ *không* tăng độ chính xác tuyệt đối tương xứng vì mô-men gia tăng giữa hai vi bước kề nhau rất nhỏ!

### 3. Giới hạn tần số xung và sụt giảm mô-men ở tốc độ cao
Khi động cơ bước quay nhanh, sức phản điện động và độ tự cảm cuộn dây $$L$$ cản trở dòng điện tăng kịp trong thời gian một bước quá ngắn, khiến mô-men giảm mạnh ở RPM cao. Đó là lý do mọi máy CNC/máy in 3D đều cần **hồ sơ tăng tốc hình thang hoặc đường cong chữ S (acceleration ramp)** thay vì nhảy vọt ngay từ 0 lên tốc độ tối đa.

### Giải thích: Cầm tay tính tần số xung vi bước 1/16 và độ sụt mô-men gia tăng

Xét động cơ NEMA 17 chuẩn (**$$1{,}8^\circ/\text{bước}$$**, tức **200 bước/vòng**) chạy ở chế độ vi bước **1/16** với mục tiêu quay đều ở tốc độ **$$120\text{ RPM}$$**:

1. **Độ phân giải góc và tổng số vi bước mỗi vòng:**
   $$N_{\text{micro}} = 200 \times 16 = 3\,200\text{ vi bước/vòng}, \qquad \Delta\theta = \frac{1{,}8^\circ}{16} = 0{,}1125^\circ/\text{vi bước}.$$
2. **Tần số xung `STEP` vi điều khiển phải phát:**
   Tốc độ $$120\text{ RPM} = \frac{120}{60} = 2\text{ vòng/giây}$$.
   $$f_{\text{step}} = 2\text{ vòng/s} \times 3\,200\text{ vi bước/vòng} = 6\,400\text{ Hz} \implies T_{\text{step}} = \frac{1}{6\,400} = 156{,}25\,\mu\text{s}.$$
   Nếu vi điều khiển bận in `Serial.println()` chậm mất $$1\text{ ms}$$, động cơ sẽ lập tức khựng và trượt bước!
3. **Kiểm chứng độ sụt mô-men gia tăng (Incremental Torque) ở vi bước 1/16:**
   Mô-men kéo roto nhảy đúng 1 vi bước tỉ lệ với $$\sin\!\left(\frac{90^\circ}{M}\right)$$ (với $$M = 16$$ là hệ số vi bước):
   $$\frac{\tau_{\text{inc}}}{\tau_{\text{hold}}} = \sin\!\left(\frac{90^\circ}{16}\right) = \sin(5{,}625^\circ) \approx 0{,}098 = 9{,}8\%!$$
   Nghĩa là mỗi vi bước 1/16 chỉ tạo được chưa đầy **10%** mô-men giữ toàn phần — nếu ma sát trục lớn hơn $$9{,}8\%$$ mô-men giữ, roto sẽ đứng im vài vi bước rồi mới nhảy cục bộ!

## Mục tiêu học

Sau bài này, bạn quy đổi được góc bước đầy $1{,}8^\circ$ thành 200 bước mỗi vòng và tính được số bước trên trục ra sau hộp giảm tốc. Bạn hiểu vi bước (1/2, 1/4, 1/16) giúp chuyển động mượt hơn nhưng không làm tăng mô-men giữ của động cơ. Bạn tính được điện áp tham chiếu $$V_{ref}$$ cho mạch A4988 khi điện trở cảm biến dòng là $$0.068~\Omega$$ và biết điều chỉnh công thức khi bo mạch clone dùng $$0.1~\Omega$$. Bạn cũng nhận diện được kiểu lỗi đặc trưng của điều khiển vòng hở: mất bước dưới tải xảy ra âm thầm mà không báo lỗi.

## Kiến thức cần có

Bạn biết đo điện áp một chiều nhỏ (dưới 1 V) với que đen đặt trên mass, và nắm vững định luật Ohm cùng khái niệm dòng cuộn dây từ bài động cơ DC. Không bắt buộc phải có động cơ bước trên bàn; bạn có thể hoàn thành bài thực hành với ảnh chụp bo A4988/DRV8825 kết hợp phần tính toán (hoặc đếm thử một vòng nếu có sẵn NEMA17).

## Vì sao bài này quan trọng với Capstone A và ROS

Hệ bánh xe của Capstone A dùng động cơ DC kèm encoder để khép vòng phản hồi. Động cơ bước thường xuất hiện khi bạn mở rộng thêm cánh tay nhỏ, cơ cấu nâng hạ bút hoặc thanh trượt camera — những khớp cần giữ vị trí ổn định và quay góc xác định. Khi lập kế hoạch quỹ đạo khớp trên ROS, hệ thống cần biết chính xác tổng số bước trên một vòng **trục ra sau hộp số** (nếu khai báo nhầm 200 bước cho trục gắn sau hộp số 50:1, khớp sẽ chỉ quay một góc rất nhỏ so với kế hoạch), đồng thời phải đặt đúng giới hạn dòng để tránh mất bước âm thầm.

## Bước đầy, vi bước và hiện tượng mất bước

Một động cơ bước hybrid phổ biến có góc bước đầy $1{,}8^\circ$, tương ứng:

$$
\frac{360^\circ}{1.8^\circ} = 200
$$

bước đầy trên mỗi vòng trục động cơ. Các mạch lái kiểu băm dòng (chopper) như Allegro A4988 và TI DRV8825 điều tiết dòng trong cuộn dây quanh giới hạn đã cài đặt; chân `STEP` nhận xung dịch bước, chân `DIR` chọn chiều quay. Vì cuộn dây luôn duy trì dòng để tạo mô-men giữ ngay cả lúc trục đứng yên, động cơ bước đang cấp nguồn thường ấm lên khi nghỉ.

Chế độ vi bước (1/2, 1/4, 1/8, 1/16 trên A4988 và mịn hơn trên DRV8825) chia mỗi bước đầy thành các nấc dòng trung gian nhỏ hơn, giúp giảm rung ồn và cộng hưởng cơ khí. Tuy nhiên, vi bước **không nhân mô-men giữ** lên 16 lần — mô-men vẫn phụ thuộc vào động cơ, dòng cài đặt và nguồn cấp. Nếu tải ngoài vượt mô-men giữ, rô-to sẽ trượt tụt lại phía sau mà mạch lái không phát ra bất kỳ tín hiệu báo lỗi nào; bộ đếm bước của phần mềm vẫn nghĩ cơ cấu đã tới đích. Đó là bản chất của điều khiển vòng hở (chỉ khi gắn thêm encoder mới phát hiện được sai lệch vị trí này).

Trên A4988, ba chân `MS1`, `MS2`, `MS3` chọn hệ số vi bước (thường từ tất cả mức thấp cho bước đầy đến tất cả mức cao cho 1/16 — luôn đối chiếu bảng tra của đúng bo mạch và không để chân `MS` bị nổi).

## Chỉnh biến trở giới hạn dòng

Trên bo A4988 chuẩn Pololu dùng điện trở cảm biến dòng $$R_{sense} = 0.068~\Omega$$, mối liên hệ giữa dòng cực đại $$I_{max}$$ và điện áp tham chiếu $$V_{ref}$$ đo trên biến trở là:

$$
I_{max} = \frac{V_{ref}}{8 \times 0.068} = \frac{V_{ref}}{0.544}
$$

Bạn đo $$V_{ref}$$ giữa đầu vít/chân giữa (wiper) của biến trở và `GND` khi mạch đã cấp nguồn theo hướng dẫn nhà sản xuất. Lưu ý nhiều bo clone sử dụng điện trở $$R_{sense} = 0.1~\Omega$$ (khi đó mẫu số là $$8 \times 0.1 = 0.8$$ thay vì 0,544), nên bắt buộc kiểm tra trị số $$R_{sense}$$ in trên bo mạch trước khi chỉnh. Không vặn biến trở hết cỡ vì dòng vượt định mức sẽ làm cháy cuộn dây hoặc quá nhiệt chip.

**Quy tắc an toàn bắt buộc:** không bao giờ rút hoặc cắm dây cuộn dây động cơ khi mạch lái đang cấp điện (`enable`). Ngắt mạch đột ngột cuộn cảm đang có dòng sẽ tạo xung điện áp ngược lớn làm hỏng chip lái ngay lập tức; luôn tắt `enable` hoặc ngắt nguồn `VM` trước khi thay đổi dây.

## Động cơ bước đơn cực 28BYJ-48

Bộ 28BYJ-48 kèm mạch ULN2003 là động cơ bước đơn cực (unipolar) 5 V có hộp giảm tốc nhựa. Đây là bộ thí nghiệm rẻ và dễ quan sát tốc độ chậm trên bàn, nhưng không phù hợp làm bánh dẫn động cho Capstone A vì kết cấu hộp số nhựa và mô-men/tốc độ đầu ra không đáp ứng tải khung xe.

## Ví dụ tính tay

Để đặt giới hạn dòng $$I_{max} = 1.0~\mathrm{A}$$ trên bo A4988 có $$R_{sense} = 0.068~\Omega$$:

$$
V_{ref} = I_{max} \times 0.544 = 1.0 \times 0.544 = 0.544~\mathrm{V} \approx 0.54~\mathrm{V}
$$

Đặt que đen lên `GND`, que đỏ lên chân giữa/đầu vít biến trở và chỉnh nhẹ đến khoảng 0,54 V. Nếu bo mạch dùng $$R_{sense} = 0.1~\Omega$$, tính lại:

$$
V_{ref} = I_{max} \times (8 \times 0.1) = 0.80~\mathrm{V}
$$

Luôn ghi giá trị $$R_{sense}$$ giả định bên cạnh mức $$V_{ref}$$ đã đo.

Đối với khớp nối dùng trên ROS: một động cơ 200 bước đầy chạy ở chế độ vi bước 1/16 cần $$200 \times 16 = 3200$$ vi bước cho một vòng trục động cơ; nếu qua thêm hộp số 50:1 thì cần $$3200 \times 50 = 160000$$ vi bước cho một vòng trục ra.

## Hình minh họa

![Đồng hồ số, dụng cụ bạn dùng trên chiết áp giới hạn dòng]({{ site.imgurl }}/wikimedia/Digital_Multimeter_Aka.jpg)

Que đen đặt tại `GND` của driver, que đỏ đặt tại chân giữa (wiper) của biến trở; kết quả đo nằm ở mức dưới 1 V (nếu hiện điện áp nguồn `VM` là đang đặt nhầm chân).

## Lab

### An toàn

Không rút dây cuộn động cơ khi driver đang có nguồn. Chỉnh xong giới hạn dòng trước khi cho chạy hành trình dài. Giữ `VM` trong dải cho phép của mạch lái (thường 8–12 V cho A4988; 5 V cho 28BYJ-48).

### BOM

| Món | Vai trò |
|------|------|
| Đồng hồ vạn năng | Đo điện áp $$V_{ref}$$ |
| Module A4988 hoặc DRV8825 *(nếu có)* | Xác định biến trở, $$R_{sense}$$ và các chân `MS` |
| Động cơ bước 4 dây *(tùy chọn)* | Kiểm tra đếm 200 bước/vòng |
| Hoặc ảnh chụp rõ nét của module | Dùng cho nhánh không có phần cứng |
| Sổ tay | Ghi $$R_{sense}$$, $$V_{ref}$$ và số bước |

### Các bước

1. Nếu không có phần cứng: vẽ/đánh dấu vị trí biến trở và các chân `MS` từ ảnh sản phẩm, tính $$V_{ref}$$ cho 1,0 A với $$0.068~\Omega$$ (0,54 V) và bản clone $$0.1~\Omega$$ (0,80 V). Hoàn thành đến đây là đủ.
2. Nếu có phần cứng: đọc trị số điện trở cảm biến dòng in trên bo mạch và ghi lại $$R_{sense}$$.
3. Xác định đúng hai cặp dây cuộn bằng đồng hồ (cùng một cuộn có điện trở vài ohm, hai cuộn khác nhau hở mạch), đấu dây khi đã ngắt điện, sau đó cấp nguồn theo hướng dẫn và đo/chỉnh $$V_{ref}$$.
4. Cấu hình chế độ bước đầy, dán cờ giấy lên trục, xuất chậm 200 xung và xác nhận trục NEMA17 $1{,}8^\circ$ quay đúng một vòng (lưu ý 28BYJ-48 có hộp số nên sẽ không ra 200 bước).
5. Giữ nhẹ trục trong lúc chạy chậm để quan sát hiện tượng mất bước (trục lệch vị trí khi chương trình kết thúc mà không báo lỗi), rồi thả tay ra trước khi mạch nóng.

### Kết quả mong đợi

Sổ tay ghi rõ giá trị $$V_{ref}$$ mục tiêu cho 1,0 A kèm $$R_{sense}$$ tương ứng, ảnh/hình đánh dấu biến trở và chân `MS` (hoặc kết quả đếm 200 bước đầy trên NEMA17), cùng câu khẳng định rằng mất bước vòng hở không tự sinh thông báo lỗi.

### Lỗi thường gặp

| Hiện tượng | Cần kiểm tra |
|------------|--------------|
| Động cơ chỉ rung/kêu mà không quay | Đấu sai cặp cuộn, giới hạn dòng quá thấp hoặc chân `SLEEP`/`ENABLE` chưa kích hoạt |
| Động cơ và chip nóng rát khi đứng yên | $$V_{ref}$$ chỉnh quá cao so với dòng định mức động cơ; hạ ngay xuống |
| Chạy êm hơn nhưng yếu hơn khi chạm tay | Đang bật vi bước; mô-men không tăng theo hệ số chia bước |
| Vị trí chỉ lệch khi mang tải | Mất bước; giảm tốc độ, chỉnh dòng tối đa đến định mức hoặc bổ sung encoder |
| Đồng hồ hiện điện áp `VM` khi đo biến trở | Đặt nhầm que đỏ; chuyển đúng sang chân giữa (wiper) và đo so với `GND` |

## Mua ở Việt Nam

Bạn có thể hoàn thành bài này mà không cần mua thêm linh kiện. Nếu muốn thực hành thêm trên bàn, bộ 28BYJ-48 + ULN2003 có giá rẻ (khoảng 25.000–50.000 VND), còn bộ NEMA17 (150.000–400.000 VND) + A4988 (20.000–55.000 VND) khớp đúng cấu hình 200 bước hybrid:

- HShop: [A4988](https://hshop.vn/search?q=A4988), [28BYJ-48](https://hshop.vn/search?q=28BYJ-48), [NEMA17](https://hshop.vn/search?q=NEMA17)
- Shopee: [A4988](https://shopee.vn/search?keyword=A4988), [28BYJ-48](https://shopee.vn/search?keyword=28BYJ-48)
- Lazada: [A4988](https://www.lazada.vn/catalog/?q=A4988), [DRV8825](https://www.lazada.vn/catalog/?q=DRV8825)
- Thế Giới IC: [A4988](https://www.thegioiic.com/search?q=A4988), [ULN2003](https://www.thegioiic.com/search?q=ULN2003)

## Video tham khảo

- **Xem trước:** [Microstepping in bipolar stepper motors](https://www.youtube.com/watch?v=X4qkWxRBTEg) — Texas Instruments, tiếng Anh. Giải thích nguyên lý điều chế dòng lệch pha giữa hai cuộn dây trong vi bước.
- [Operating Principles of a Microstep Stepper Motor Drive](https://www.youtube.com/watch?v=Bs1zIZV1uSY) — Oriental Motor USA, tiếng Anh. Minh họa trực quan cách chia nhỏ bước đầy để làm mượt chuyển động.

## Bài tập

1. Một động cơ bước $1{,}8^\circ$ cần bao nhiêu bước đầy cho một vòng quay? Ở chế độ vi bước 1/16, con số đó là bao nhiêu?
2. Với bo A4988 có $$R_{sense} = 0.068~\Omega$$ và điện áp đo được $$V_{ref} = 0.30~\mathrm{V}$$, giới hạn dòng đang đặt là bao nhiêu?
3. Với bo clone dùng $$R_{sense} = 0.1~\Omega$$, cần đặt $$V_{ref}$$ bao nhiêu để giới hạn dòng ở 0,8 A?
4. Một cánh tay chạy xong chương trình 400 bước nhưng đầu cánh vẫn thiếu so với vạch đích và phần mềm không báo lỗi. Hiện tượng vật lý nào đã xảy ra?
5. Một khớp ROS dùng động cơ 200 bước ở chế độ bước đầy qua hộp giảm tốc 30:1. Cần bao nhiêu bước cho một vòng trục ra?

### Gợi ý đáp án

1. 200 bước đầy và $$200 \times 16 = 3200$$ vi bước 1/16.
2. $$I_{max} = 0.30 / 0.544 \approx 0.55~\mathrm{A}$$.
3. $$V_{ref} = 0.8 \times (8 \times 0.1) = 0.64~\mathrm{V}$$.
4. Mất bước (skipped steps) do điều khiển vòng hở dưới tải vượt mô-men giữ.
5. $$200 \times 30 = 6000$$ bước trên một vòng trục ra.

## Đọc thêm

- Mạch mang A4988 của Pololu (hướng dẫn giới hạn dòng và công thức $$V_{ref}$$): [https://www.pololu.com/product/1182](https://www.pololu.com/product/1182)
- Datasheet TI DRV8825 (driver kiểu băm dòng và các chế độ vi bước): [https://www.ti.com/lit/ds/symlink/drv8825.pdf](https://www.ti.com/lit/ds/symlink/drv8825.pdf)
- SparkFun — chọn động cơ (đối chiếu khái niệm mô-men và dòng với động cơ DC): [https://learn.sparkfun.com/tutorials/motors-and-selecting-the-right-one/all](https://learn.sparkfun.com/tutorials/motors-and-selecting-the-right-one/all)
