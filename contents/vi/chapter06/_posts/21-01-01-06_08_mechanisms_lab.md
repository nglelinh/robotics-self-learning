---
layout: post
title: "Lab: đo tỉ số truyền và checklist lắp"
chapter: "06"
order: 8
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter06
lesson_type: required
draft: false
---

Thời lượng ước tính: **80–110 phút**. Đây là bài thực hành trực tiếp trên cơ khí; nguồn điện phải tắt hoàn toàn trong mọi bước kiểm tra.

Thông số in trên nhãn hộp số giá rẻ mua online không phải lúc nào cũng khớp 100% với thực tế: một động cơ quảng cáo "hộp số 30:1" đôi khi thực chất là 29,86:1 hoặc 34:1, và độ rơ thực tế sau khi lắp lên khung có thể lớn gấp đôi thông số lý thuyết. **Bài lab đo tỉ số truyền và kiểm tra lắp ráp** rèn cho bạn thói quen quý giá của kỹ sư thực nghiệm: *đừng tin mù quáng vào nhãn bán hàng — hãy tự đo trực tiếp bằng thước, đánh dấu phấn và đồng hồ, rồi đưa con số đo thật vào cấu hình phần mềm!*

## Kiến thức cần nhớ: Phương pháp đo thực nghiệm cơ cấu truyền động

### 1. Đo tỉ số truyền thực nghiệm (Phương pháp đếm nhiều vòng)
Nếu chỉ quay trục vào 1 vòng để ước lượng góc trục ra bằng mắt, sai số đọc góc lên tới vài phần trăm. Kỹ thuật chuẩn là **đánh dấu vạch tham chiếu trên cả hai trục**, quay trục đầu vào đúng $$N_{\text{in}}$$ vòng lớn (ví dụ 10–20 vòng) cho đến khi trục ra quay đủ 1 hoặc nhiều vòng chẵn, từ đó tính $$G = N_{\text{in}} / N_{\text{out}}$$ với sai số nhỏ hơn $$0{,}5\%$$.

### 2. Đo độ rơ góc (Backlash) bằng phương pháp tay đòn khuếch đại
Đo trực tiếp góc rơ $$1^\circ$$ trên trục tròn đường kính $$6\text{ mm}$$ bằng mắt thường là bất khả thi. Thay vào đó, kẹp một thanh thước mảnh dài $$L = 100\text{ mm}$$ vào trục đầu ra, giữ cứng trục vào rồi lắc nhẹ đầu thanh thước qua lại đo khoảng dịch chuyển tuyến tính $$\Delta x$$ bằng thước cặp, sau đó đổi sang độ: $$\Delta\theta = \frac{\Delta x}{L} \cdot \frac{180^\circ}{\pi}$$.

### 3. Kiểm tra kẹt cơ khí (Binding) theo chu kỳ quay $$360^\circ$$
Quay tay trục bánh xe trọn một vòng $$360^\circ$$ (khi đã ngắt động cơ): nếu thấy nhẹ ở nửa vòng này nhưng đột nhiên nặng khựng ở nửa vòng kia, chắc chắn trục đang bị **lệch tâm (eccentricity)** hoặc bánh răng bị đảo — bắt buộc căn chỉnh lại trước khi cấp điện!

### Giải thích: Cầm tay xử lý số liệu đo tỉ số truyền và góc rơ Backlash trong phòng lab

**Phần A — Xác định tỉ số truyền thực của một hộp số không rõ nhãn:**
Bạn đánh dấu vạch sơn trắng lên trục động cơ và trục bánh xe. Quay trục động cơ đúng **$$15$$ vòng trọn vẹn**, thấy vạch trên bánh xe quay đúng **$$1$$ vòng** trở về vị trí cũ:
$$G_{\text{đo}} = \frac{N_{\text{in}}}{N_{\text{out}}} = \frac{15}{1} = 15{:}1.$$
*(Nếu quay $$30$$ vòng trục vào mà trục ra quay được $$1$$ vòng + $$18^\circ = 1{,}05$$ vòng, thì $$G_{\text{đo}} = 30 / 1{,}05 \approx 28{,}57{:}1$$ — sai khác tới 5% so với con số "30:1" in trên nhãn!)*

**Phần B — Đo độ rơ góc Backlash bằng thanh thước dài $$L = 100\text{ mm}$$:**
Giữ chặt trục đầu vào, lắc nhẹ đầu thanh thước dài $$100\text{ mm}$$ gắn trên trục ra và đo được tổng biên độ lắc tự do **$$\Delta x = 2{,}0\text{ mm}$$**:
$$\Delta\theta_{\text{rad}} = \frac{\Delta x}{L} = \frac{2{,}0}{100} = 0{,}020\text{ rad} \implies \Delta\theta_{\text{độ}} = 0{,}020 \times \frac{180^\circ}{\pi} \approx 1{,}15^\circ.$$
Ghi ngay con số $$G = 15{:}1$$ và backlash $$1{,}15^\circ$$ vào sổ lab: đó là cơ sở định lượng để bạn biết odometry có thể lệch tối đa bao nhiêu mỗi lần xe đảo chiều!

## Mục tiêu học

Sau bài này, các bạn có một giá trị tỉ số truyền đã được dự đoán và đo kiểm thực tế, một ước lượng độ rơ (backlash) tại bánh xe theo độ, và một danh sách kiểm tra lắp ráp (checklist) hoàn chỉnh để thực hiện trước khi cấp điện ở Chương 07. Các bạn phân biệt rõ tác dụng của bánh trung gian đơn với tầng đổi tỉ số, đồng thời biết nhân tỉ số hộp giảm tốc với tỉ số bộ truyền đai ngoài (nếu có).

## Kiến thức cần có

Kiến thức từ Bài 01 đến Bài 07: $$b$$, $$r$$, quy cách ốc M3, định nghĩa tỉ số truyền $$i = N_{\text{out}}/N_{\text{in}} = \omega_{\text{in}}/\omega_{\text{out}}$$ và kỹ thuật kiểm tra giảm lực kéo dây. Dụng cụ chỉ cần kim chỉ cắt từ bìa cứng và thước đo góc (hoặc thước đo góc in trên giấy).

## Vì sao bài này quan trọng với Capstone A và ROS

Chương 07 sẽ là lần đầu tiên khung robot được cấp điện áp. Checklist trong bài này đóng vai trò chốt chặn an toàn: một bánh xe cọ khung, khối pin lỏng hay vít cố định trục đặt sai vị trí sẽ làm hỏng buổi thực hành cấp nguồn bằng đúng các dạng lỗi đã phân tích ở Bài 07.

Tỉ số truyền bạn đo hôm nay chính là tham số `diff_drive_controller` dùng để quy đổi xung thành mét. Với bánh răng nhựa đúc, sai số đo nằm trong phạm vi 10% so với thông số nhãn là chấp nhận được. Nếu bộ kit chưa về kịp, phần tính dự đoán trên bản vẽ là sản phẩm nộp (ghi rõ nhãn “bản vẽ”); tuyệt đối không tự bịa số đo góc thực tế.

## Các bạn đang kiểm gì

Trước hết, đếm số răng nếu nhìn thấy hoặc đọc tỉ số đóng dấu trên vỏ hộp giảm tốc — đây là giá trị dự đoán. Bước kiểm chứng được thực hiện theo phương pháp động học: gắn một kim chỉ lên trục đầu vào và một kim chỉ lên trục đầu ra, xoay trục vào một số vòng đã biết rồi đo góc quay đầu ra. Với tỉ số $$i$$, ba vòng quay của trục đầu vào phải tạo ra góc đầu ra:

$$
\theta_{\text{out}} = \frac{3}{i} \times 360^\circ.
$$

Tiếp theo, giữ cố định trục đầu vào và lắc nhẹ bánh xe. Góc bánh dịch chuyển trước khi kim đầu vào bắt đầu nhúc nhích chính là độ rơ (backlash). Chỉ cần ước lượng bằng mắt theo độ: vài độ là bình thường ở hộp số nhựa đúc, nhưng nếu lên tới hàng chục độ thì nguyên nhân là vít cố định trục lỏng hoặc đai nhảy răng — đây là lỗi cơ khí cần sửa ngay.

Lưu ý rằng một bánh trung gian đơn chỉ đảo chiều quay chứ không làm thay đổi tỉ số $$i$$; chỉ tính nó là một cặp ăn khớp khi xác định dấu chiều quay (trừ khi đó là bánh răng kép gồm hai vòng răng khác số răng gắn cố định trên cùng trục). Nếu có thêm bộ truyền đai bên ngoài hộp số, tỉ số tổng tại bánh xe là tích của hai tầng — bỏ sót hệ số 2 ở bộ đai là lỗi phổ biến hơn cả việc đếm nhầm số răng.

Sau khi đo tỉ số, hãy kiểm tra toàn bộ checklist lắp ráp khi pin vẫn đặt rời trên bàn (chưa cắm giắc): ốc vít đã siết chặt; vít cố định trục tỳ đúng mặt vát; bánh xe không cọ tấm khung; bánh caster xoay trơn và có khoảng đuôi đúng hướng; dây có vòng dự phòng và mối hàn không chịu lực uốn; pin không bị trượt khỏi vị trí; cả hai động cơ khi xoay tay có lực cản tương đương nhau. Nếu một động cơ có cảm giác sượng hoặc nặng tay hơn hẳn bên còn lại, hãy ghi nhận và xử lý trước Chương 07 chứ không cố bù bằng cách tăng PWM.

![Gọi tên đầu vào trước khi chia: hình là dự đoán, hai kim là phép kiểm]({{ site.imgurl }}/generated/gear_train_ratio.png)

## Ví dụ tính tay

Xét động cơ TT đóng dấu tỉ số 1:48. Khi trục đầu vào quay 3 vòng, góc đầu ra dự đoán là:

$$
\theta_{\text{out}} = \frac{3}{48} \times 360^\circ = 22.5^\circ.
$$

Giả sử bạn đo được $$24^\circ$$ tại kim gắn trên bánh xe. Sai số tương đối là:

$$
\frac{24 - 22.5}{22.5} \approx 0.067,
$$

tương đương khoảng 7%, nằm trong ngưỡng cho phép 10% đối với hộp số nhựa đúc và kim chỉ thủ công. Bạn ghi vào sổ: $$i = 48$$ và “đã kiểm, 24° so với dự đoán 22,5°”. Nếu góc đo rơi vào khoảng $$45^\circ$$, có thể bạn đã bỏ quên hoặc nhân nhầm một tầng tỉ số 2:1; nếu gần $$67.5^\circ$$, có thể hộp số thực tế là $$i = 16$$ hoặc bạn đã đếm nhầm số vòng trục vào. Độ rơ ước lượng khi lắc bánh (ví dụ $$5^\circ$$) được ghi bên cạnh tỉ số, không cố khử bằng cách ép chặt cặp bánh răng gây kẹt.

Về chiều quay: một cặp ăn khớp ngoài (hoặc một số lẻ cặp ăn khớp ngoài) làm đầu ra quay ngược chiều đầu vào. Quy ước dấu firmware ở Bài 05 phải khớp với quan sát thực tế này bằng cách xoay trục bằng tay khi tắt nguồn.

## Lab: hai kim, rồi danh sách

### An toàn

Nguồn điện luôn tắt; pin đã ngắt kết nối và đặt xa vị trí thao tác để tránh vô tình chạm cực. Cẩn thận tránh kẹp tay vào bánh răng; hãy xoay trục thông qua kim chỉ hoặc phần đầu trục thay vì thò ngón tay vào vùng ăn khớp. Nếu trục bị cứng không quay được, dừng lại kiểm tra chỗ kẹt thay vì cấp điện để “phá kẹt”.

### BOM

| Hạng mục | Vai trò |
|------|------|
| Động cơ giảm tốc hoặc một bản vẽ bánh răng đúng tỉ lệ | Tỉ số |
| Hai kim: cờ băng dính hoặc mũi tên bìa | Đầu vào và đầu ra |
| Thước đo góc, hoặc một thước in | Góc đầu ra và độ rơ |
| Lục giác cho vít cố định trục | Mặt vát |
| Dây rút | Vòng dự phòng, nếu dây đã có trên động cơ |
| `lab-notes.md` | Dự đoán, phép đo, checklist |

### Các bước

1. Ghi giá trị dự đoán (từ số răng đếm được hoặc dấu đóng trên vỏ hộp số) và tính $$\theta_{\text{out}}$$ cho đúng ba vòng quay của trục đầu vào.
2. Gắn một kim chỉ lên trục đầu vào và một kim chỉ lên trục đầu ra, đồng thời đánh dấu mốc $$0^\circ$$ trên mặt bàn.
3. Xoay trục đầu vào đúng 3 vòng, đo góc quay của kim đầu ra, so sánh với dự đoán và tính phần trăm sai lệch.
4. Giữ chặt trục đầu vào, lắc nhẹ trục đầu ra và ước lượng độ rơ theo độ tại bánh xe.
5. Kiểm tra và đánh dấu từng mục trong checklist lắp ráp vào sổ: ốc chặt; vít cố định trục trên mặt vát; bánh không cọ khung; caster xoay trơn và có khoảng đuôi; dây có vòng dự phòng và mối hàn không chịu uốn; pin không trượt; hai động cơ xoay tay có lực cản tương đương.
6. Nếu mới chỉ có bản vẽ, hoàn thành bước 1 cùng các phác thảo, ghi chú “bản vẽ, kết quả trên giấy là sản phẩm nộp” và chuẩn bị sẵn checklist để chạy ngay khi có phần cứng.

### Kết quả mong đợi

Một tỉ số truyền có kết quả đo nằm trong ngưỡng 10% so với nhãn (khi có phần cứng) hoặc bản tính dự đoán trên giấy được dán nhãn rõ ràng (khi chưa có phần cứng), kèm giá trị độ rơ tính theo độ. Mỗi dòng trong checklist được đánh dấu “đạt”, “không đạt” hoặc “chưa có trên bàn”; mọi dòng “không đạt” phải ghi rõ biện pháp khắc phục trước khi cấp điện.

### Lỗi thường gặp

| Các bạn thấy | Thường nghĩa là |
|--------------|------------------------|
| Góc là nghịch đảo của dự đoán | Tên đầu vào và đầu ra bị đảo |
| Góc bằng một nửa hoặc gấp đôi | Hộp giảm tốc và đai ngoài chưa được nhân, hoặc một trong hai bị áp hai lần |
| Chiều sai, tỉ số đúng | Một bánh trung gian bị tính như đổi tỉ số, hoặc một cặp ăn bị bỏ khỏi phép đếm dấu |
| Đầu ra oặt hàng chục độ | Vít cố định trục, moay-ơ mòn răng, hoặc đai nhảy răng |
| Một động cơ cứng hơn nhiều khi xoay tay | Chỗ cà, hoặc hộp số hỏng; đừng cấp điện để xác nhận |

## Mua ở Việt Nam / Where to buy in Vietnam

Chỉ đặt mua những linh kiện mà checklist chỉ ra còn thiếu. Bạn có thể dùng ứng dụng thước đo góc trên điện thoại nếu ngắm chuẩn dọc theo kim chỉ. Nên chọn mua động cơ TT có in rõ tỉ số trên vỏ để bước 1 không phải đoán.

| Mua gì | Từ khóa | Khoảng giá (VND) | Ghi chú |
|------|----------|------------------|-------|
| Động cơ giảm tốc TT | `động cơ giảm tốc TT encoder` | 45.000–120.000 mỗi cái | Dấu đóng là dự đoán |
| Bộ ốc M3, nếu lần phân loại ở Bài 02 bị thiếu | `ốc M3` | 25.000–70.000 | Dòng ốc trên checklist |
| Bánh caster, nếu mũi vẫn cày | `bánh caster robot` | 12.000–40.000 | Phải có đuôi |

Các trang tìm mua:

- [Hshop](https://hshop.vn/search?q=%C4%91%E1%BB%99ng+c%C6%A1+gi%E1%BA%A3m+t%E1%BB%91c+TT)
- [Shopee](https://shopee.vn/search?keyword=%C4%91%E1%BB%99ng%20c%C6%A1%20gi%E1%BA%A3m%20t%E1%BB%91c%20TT%20encoder)
- [Lazada](https://www.lazada.vn/catalog/?q=%E1%BB%91c%20M3)
- [Thế Giới IC](https://www.thegioiic.com/search?q=%E1%BB%91c%20M3)

Giá bán có thể thay đổi theo thời điểm.

## Video tham khảo

- **Xem trước:** [Compound Gears Explained:  Calculate Gear Ratio](https://www.youtube.com/watch?v=NmUq2TQ8m2M) — INTEGRAL PHYSICS, tiếng Anh. Đếm số răng, tính tỉ số truyền rồi quay trục vào để đối chiếu — đúng quy trình thực hành của bài này.
- [How to measure Gear Backlash and Center Distance](https://www.youtube.com/watch?v=8fYwUV6QV8c) — Evolvent Design, tiếng Anh. Đo khe hở độ rơ trước khi vội kết luận tỉ số truyền bị sai.

## Bài tập

1. Hộp giảm tốc đóng dấu tỉ số 1:90. Dự đoán góc quay đầu ra sau ba vòng quay của trục đầu vào.
2. Trên một động cơ đóng dấu 1:48, bạn đo được góc đầu ra $$12^\circ$$ sau ba vòng trục vào. Kết quả này có nằm trong ngưỡng 10% so với $$22.5^\circ$$ không? Bạn cần kiểm tra những gì tiếp theo?
3. Bánh dẫn 20 răng kéo bánh trung gian 20 răng, sau đó kéo bánh ra 40 răng. Tính tỉ số truyền $$i$$ và cho biết chiều quay đầu ra so với bánh dẫn.
4. Một hộp giảm tốc 1:48 nối tiếp với bộ đai GT2 gồm pulley động cơ 20 răng và pulley bánh xe 40 răng. Tính tỉ số tổng $$i$$ tại bánh xe và góc $$\theta_{\text{out}}$$ sau ba vòng quay động cơ.
5. Liệt kê 7 mục trong checklist lắp ráp và đánh dấu sao hai mục mà nếu bỏ qua sẽ trực tiếp gây ra sai số odometry ảo rõ rệt nhất.

### Gợi ý đáp án

1. $$\theta_{\text{out}} = \frac{3}{90} \times 360^\circ = 12^\circ$$.
2. Sai số tương đối $$|12 - 22.5|/22.5 \approx 47\%$$, vượt xa ngưỡng 10%. Cần kiểm tra lại: đã xoay đúng 3 vòng trục vào chưa, nhãn trên vỏ có thực sự là 1:48 không, và có tầng đai hoặc tầng giảm tốc nào bị bỏ sót hoặc tính nhầm hay không.
3. $$i = 40/20 = 2$$ (bánh trung gian đơn không đổi tỉ số). Có hai cặp ăn khớp ngoài nên chiều quay đảo hai lần, đầu ra quay cùng chiều bánh dẫn.
4. $$i = 48 \times (40/20) = 96$$. Sau 3 vòng động cơ, góc quay bánh xe là $$\theta_{\text{out}} = \frac{3}{96} \times 360^\circ = 11.25^\circ$$.
5. Bảy mục: ốc chặt; vít cố định trục trên mặt vát; bánh không cọ khung; caster xoay trơn và có khoảng đuôi; dây có vòng dự phòng và mối hàn không chịu uốn; pin không trượt; lực cản xoay tay hai động cơ tương đương. Hai mục nên đánh dấu sao là vít cố định trục và bánh cọ khung, vì cả hai đều làm encoder đếm xung khác với chuyển động thực trên sàn.

## Đọc thêm

- [Gear ratio](https://en.wikipedia.org/wiki/Gear_ratio) — nguyên lý chuỗi bánh răng kép, áp dụng tương tự cho trường hợp hộp giảm tốc nối tiếp bộ đai.
- [Công nghệ bánh răng SDP-SI](https://www.sdp-si.com/resources/elements-of-metric-gear-technology/index.php) — giải thích khái niệm độ rơ như một khe hở thiết kế có chủ đích.
- [diff_drive_controller](https://github.com/ros-controls/ros2_controllers/tree/master/diff_drive_controller) — nơi nhập các tham số $$i$$, $$b$$ và $$r$$ đo được vào hệ thống ROS.
