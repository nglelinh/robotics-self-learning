---
layout: post
title: "Giới hạn dòng, stall và nhiệt"
chapter: "05"
order: 5
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter05
lesson_type: required
draft: false
---

Thông số động cơ có hai mức dòng điện rất khác nhau: dòng không tải đo khi bánh quay tự do trên không, và dòng kẹt trục (stall) khi rô-to đứng yên khiến suất điện động ngược bằng 0. Bài này giúp bạn quy đổi dòng stall thành công suất tỏa nhiệt trên động cơ và mạch cầu H, chọn cỡ cầu chì phù hợp trên dây dương pin và xử lý tình huống sụt áp (brownout) như một lỗi điều khiển.

Rất nhiều mạch driver và động cơ robot chết không phải vì quá áp, mà vì một kịch bản quen thuộc: bánh xe robot kẹt vào chân bàn, phần mềm vẫn vô tư đẩy PWM 100%, dòng điện vọt lên mức **dòng kẹt (stall current)** cao gấp 5–10 lần dòng chạy bình thường, và chỉ trong vài chục giây lớp sơn cách điện cuộn dây đồng nóng chảy bốc khói! Hiểu về **giới hạn dòng, dòng kẹt và mô hình nhiệt** là tấm khiên bắt buộc để bảo vệ cả phần cứng lẫn an toàn cháy nổ trong phòng lab.

## Bản đồ kiến thức nền: Định luật Joule, Mạch nhiệt tương đương và Cắt dòng bảo vệ

### 1. Vì sao dòng kẹt (Stall Current) lại nguy hiểm theo hàm bình phương?
Khi bánh xe bị chặn cứng ($$\omega = 0$$), sức phản điện động $$E = K_e \omega$$ tụt về $$0$$, toàn bộ điện áp pin đặt thẳng lên điện trở cuộn dây nhỏ xíu $$R_a$$: $$I_{\text{stall}} = V / R_a$$. Tệ hơn nữa, công suất tỏa nhiệt tuân theo định luật Joule **$$P_{\text{nhiệt}} = I^2 R_a$$**: dòng tăng lên $$4$$ lần thì nhiệt lượng đốt nóng cuộn dây tăng vọt lên **$$16$$ lần**!

### 2. Mô hình điện trở nhiệt (Thermal Resistance $$R_{\theta}$$)
Trong kỹ thuật điện tử công suất, nhiệt chảy từ nhân bán dẫn (junction) ra môi trường y hệt dòng điện chảy qua điện trở:
$$T_J = T_{\text{amb}} + P_{\text{loss}} \cdot R_{\theta JA},$$
với $$T_J$$ là nhiệt độ nhân chip (thường giới hạn tối đa $$125\text{–}150^\circ\text{C}$$), $$T_{\text{amb}}$$ là nhiệt độ phòng, và $$R_{\theta JA}$$ ($$^\circ\text{C/W}$$) là tổng trở nhiệt từ nhân ra không khí. Chỉ cần biết công suất tổn hao $$P_{\text{loss}}$$ và $$R_{\theta JA}$$ trên datasheet, bạn tính được ngay chip có cần gắn tản nhiệt hay không trước khi cấp nguồn!

### 3. Ba lớp phòng thủ: Cầu chì, Giới hạn dòng phần cứng (Chopper) và Giám sát phần mềm
Một hệ thống robot chuẩn không bao giờ dựa vào một lớp bảo vệ duy nhất: (1) **Cầu chì / polyfuse** cắt mạch khi ngắn mạch nặng; (2) **Giới hạn dòng chủ động (current limiting / Vref)** trên driver tự băm xung khi dòng chạm ngưỡng; và (3) **Watchdog phát hiện kẹt trong firmware** (thấy PWM cao mà xung encoder bằng 0 trong > 1 giây thì tự ngắt động cơ).

### Khung giải thích: Cầm tay tính công suất đốt nhiệt khi kẹt trục và nhiệt độ nhân chip driver (nên đọc chậm)

**Phần A — Sức nóng khủng khiếp khi kẹt trục (Stall) so với khi có giới hạn dòng:**
Xét động cơ DC $$12\text{ V}$$ có điện trở cuộn dây $$R_a = 1{,}5\,\Omega$$:
1. **Khi kẹt cứng không có giới hạn dòng:**
   $$I_{\text{stall}} = \frac{12\text{ V}}{1{,}5\,\Omega} = 8{,}0\text{ A} \implies P_{\text{nhiệt, stall}} = I_{\text{stall}}^2 R_a = 8{,}0^2 \times 1{,}5 = 96{,}0\text{ W}!$$
   Động cơ nhỏ cầm tay đang biến thành một chiếc mỏ hàn $$96\text{ W}$$ — cháy cuộn dây chỉ trong vài giây!
2. **Khi mạch driver đặt giới hạn dòng chủ động ở $$I_{\lim} = 2{,}0\text{ A}$$:**
   $$P_{\text{nhiệt, lim}} = 2{,}0^2 \times 1{,}5 = 6{,}0\text{ W}$$
   — giảm dòng đi $$4\times$$ nhưng cắt nhiệt lượng đốt nóng xuống tới **$$16\times$$** (từ $$96\text{ W}$$ còn $$6\text{ W}$$)!

**Phần B — Kiểm tra nhiệt độ nhân chip driver bằng điện trở nhiệt:**
Giả sử một chip driver không gắn tản nhiệt có $$R_{\theta JA} = 45^\circ\text{C/W}$$, đang tỏa công suất tổn hao $$P_{\text{loss}} = 2{,}5\text{ W}$$ trong phòng lab nóng $$T_{\text{amb}} = 30^\circ\text{C}$$:
$$T_J = 30 + 2{,}5 \times 45 = 30 + 112{,}5 = 142{,}5^\circ\text{C}!$$
Con số $$142{,}5^\circ\text{C}$$ đã chạm sát ngưỡng ngắt nhiệt ($$150^\circ\text{C}$$) của hầu hết IC bán dẫn — chứng minh bằng tính tay rằng bạn *bắt buộc* phải giảm dòng tải, đổi sang driver MOSFET có $$R_{\text{DS(on)}}$$ nhỏ hơn, hoặc gắn tản nhiệt trước khi chạy liên tục!

## Mục tiêu học

Sau bài này, bạn phân biệt rõ dòng không tải với dòng stall và dùng dòng stall làm cơ sở chọn mạch cầu H cũng như cầu chì. Từ điện áp định mức và dòng stall, bạn ước lượng được điện trở cuộn dây và công suất nhiệt tỏa ra trong động cơ khi bị kẹt. Bạn tính được nhiệt tỏa trên L298N từ mức sụt áp của chip và giải thích vì sao TB6612 mát hơn ở cùng dòng tải. Bạn cũng biết vị trí lắp cầu chì trên dây dương pin và lý do phải coi hiện tượng sụt nguồn reset vi điều khiển là một sự cố điều khiển cần chặn bằng phần mềm.

## Kiến thức cần có

Bạn chỉ cần vận dụng định luật Ohm, công thức công suất $$P = I^2 R$$, khái niệm suất điện động ngược (bài 05-01) và đặc tính các mạch cầu H (bài 05-02). Để đo thực tế, cần nguồn bàn có giới hạn dòng hoặc ampe kế mắc nối tiếp; nếu không có thiết bị giới hạn dòng an toàn, bạn thực hiện nhánh tính toán từ thông số datasheet.

## Vì sao bài này quan trọng với Capstone A và ROS

Chương 07 bắt buộc dùng pin kèm cầu chì vì cổng USB không đủ dòng cho hai động cơ TT khi kẹt trục. Ngay cả bộ pin 18650 yếu cũng có thể bị sụt áp mạnh khi hai bánh khởi động đồng thời: mạch giám sát sụt áp (brownout) của ESP32 sẽ reset chip, các chân GPIO trở về trạng thái khởi động và một mạch cầu H chưa được khóa chặt có thể làm robot giật chạy trước khi chương trình kịp đưa PWM về 0. Vì vậy, firmware phải luôn đặt `PWM = 0` ngay những dòng đầu tiên của `setup()` và giữ trạng thái dừng an toàn cho đến khi nhận lệnh hợp lệ mới.

## Dòng không tải và dòng kẹt trục (stall)

Khi bánh quay tự do (không tải), suất điện động ngược triệt tiêu phần lớn điện áp nguồn nên dòng rất nhỏ (thường vài chục đến vài trăm miliampe với động cơ TT vàng). Khi trục bị kẹt đứng yên, tốc độ bằng 0, suất điện động ngược bằng 0 và dòng vọt lên cực đại:

$$
I_{stall} \approx \frac{V}{R}
$$

Khi chạy trên sàn phẳng, dòng tiêu thụ nằm giữa hai cực trị này nhưng sẽ tăng vọt ngay khi xe leo dốc, đẩy vật cản hoặc kẹt bánh vào chân bàn. Do đó, mọi tính toán chọn mạch cầu H và cầu chì đều phải xét đến dòng stall.

## Công suất nhiệt trong động cơ bị kẹt

Khi động cơ bị kẹt, công cơ học sinh ra gần như bằng 0 nên toàn bộ công suất điện $$P = I \times V$$ chuyển thành nhiệt đốt nóng cuộn dây và chổi than. Chỉ nên giữ thử stall khoảng 1–2 giây nếu có giới hạn dòng; giữ lâu hàng chục giây sẽ làm chảy lớp men cách điện. Hai động cơ kẹt đồng thời sẽ hút khoảng gấp đôi dòng stall của một động cơ, vượt xa giới hạn ~0,5 A của cổng USB máy tính và lập tức gây sụt nguồn reset bo mạch.

## Nhiệt trên mạch cầu H và hiện tượng sụt áp pin

Với mức sụt áp khoảng 2 V ở dòng 1 A, mỗi kênh của L298N tỏa nhiệt trực tiếp trên chip khoảng:

$$
P \approx 2~\mathrm{V} \times 1~\mathrm{A} = 2~\mathrm{W}
$$

Chạy nặng cả hai kênh sẽ tăng gấp đôi lượng nhiệt đó, đòi hỏi tấm tản nhiệt kim loại thông thoáng. TB6612 dùng MOSFET nên sụt áp nhỏ hơn nhiều và chạy mát hơn hẳn, nhưng vẫn có giới hạn dòng liên tục khoảng 1,2 A mỗi kênh — nếu vỏ chip nóng rát tay thì động cơ đang bị quá tải hoặc kẹt trục.

Khi bộ pin 18650 yếu hoặc có nội trở cao, dòng khởi động làm `VM` sụt mạnh; nếu mạch hạ áp nuôi vi điều khiển dùng chung pin, nguồn logic cũng sụt theo gây brownout reset. Để tránh robot lao đi sau reset, hàm `setup()` phải kéo PWM về 0 và đặt chân hướng an toàn trước mọi thao tác khởi tạo khác.

## Vai trò của cầu chì trên dây dương pin

Lắp cầu chì nối tiếp ngay trên dây dương sát bộ pin để mọi sự cố ngắn mạch phía sau đều được ngắt kịp thời. Với robot nhỏ dùng pin 2S và hai động cơ TT, cầu chì cỡ 2–3 A là điểm khởi đầu hợp lý: đủ cao hơn tổng dòng chạy bình thường (ví dụ mỗi động cơ 0,3 A + logic 0,2 A = 0,8 A) nhưng vẫn kịp đứt khi xảy ra ngắn mạch hoặc kẹt trục kéo dài. Có thể dùng cầu chì tự phục hồi (polyfuse/PTC): khi quá dòng nó nóng lên để ngắt mạch và tự nối lại sau khi nguội — cần để thoáng khí, không bọc kín băng keo cách nhiệt làm sai lệch dòng cắt.

## Ví dụ tính tay

Giả sử nhà sản xuất công bố động cơ 6 V có dòng stall 1,2 A. Điện trở cuộn dây xấp xỉ:

$$
R \approx \frac{6}{1.2} = 5~\Omega
$$

Công suất tỏa nhiệt trong cuộn dây khi kẹt ở 6 V là:

$$
P = I^2 R = (1.2)^2 \times 5 = 1.44 \times 5 = 7.2~\mathrm{W}
$$

Kiểm tra lại bằng $$P = I \times V = 1.2 \times 6 = 7.2~\mathrm{W}$$. Mức 7,2 W trong một thân động cơ nhỏ giải thích vì sao chỉ được phép đo stall tối đa một giây. Hai động cơ như vậy kẹt cùng lúc sẽ đòi tới 2,4 A — lớn hơn nhiều so với giới hạn 0,5 A của cổng USB. Nếu đồng hồ đo dòng không tải ở PWM vừa chỉ khoảng 0,15 A, khoảng cách từ 0,15 A đến 1,2 A cho thấy độ dự phòng mà driver và cầu chì phải chịu được khi xe chạm tường.

## Hình minh họa

![Dòng stall theo tốc độ: dòng nhỏ khi đang quay, dòng lớn khi trục dừng]({{ site.imgurl }}/generated/stall_current.png)

Phía trái đồ thị ứng với tốc độ bằng 0 (dòng stall lớn nhất), phía phải ứng với tốc độ không tải (dòng nhỏ nhất).

![Đồng hồ mắc nối tiếp hoặc màn hình dòng của nguồn, dùng cho một motor với bánh trên không]({{ site.imgurl }}/wikimedia/Digital_Multimeter_Aka.jpg)

Khi đo bằng đồng hồ vạn năng, phải cắm que vào lỗ đo dòng lớn (10 A), bắt đầu ở `PWM = 0` để tránh đứt cầu chì đồng hồ; sử dụng bộ nguồn bàn có đồng hồ dòng tích hợp sẽ an toàn và thuận tiện hơn.

## Lab

### An toàn

Tháo động cơ khỏi khung (hoặc nhấc bánh khỏi bàn) và chỉ thử từng động cơ một. Chỉ thực hiện bước đo stall 1 giây khi có nguồn bàn đặt giới hạn dòng khoảng 2 A; nếu không có giới hạn dòng đáng tin cậy, hãy bỏ qua bước kẹt trục thật và tính công suất từ thông số nhà sản xuất. Không cấp nguồn động cơ từ USB và luôn nối chung mass nếu dùng vi điều khiển phát PWM.

### BOM

| Món | Vai trò |
|------|------|
| Một động cơ DC chổi than | Đối tượng kiểm thử |
| Nguồn bàn có giới hạn dòng, hoặc pin kèm ampe kế nối tiếp | Cấp nguồn và đo dòng |
| Mạch cầu H hoặc dây nguồn trực tiếp | Đặt điện áp xác định |
| Đồng hồ vạn năng | Đo điện áp và dòng điện |
| Sổ tay | Ghi dòng không tải, dòng stall hoặc công suất tính tay |

### Các bước

1. Đặt giới hạn dòng khoảng 2 A trên nguồn bàn (nếu có) và chỉnh điện áp bằng điện áp định mức (hoặc mức vừa phải, ghi rõ vào sổ).
2. Cho động cơ chạy không tải, ghi điện áp và dòng điện sau 1 giây.
3. *(Tùy chọn, chỉ khi có nguồn giới hạn dòng)* Giữ kẹt trục tối đa 1 giây, đọc dòng rồi thả ngay; nếu nguồn lập tức cắt dòng thì ghi "nguồn đã giới hạn" và dừng, không lặp lại.
4. Nếu bỏ qua bước đo stall trực tiếp, lấy dòng stall từ datasheet để tính $$R \approx V/I_{stall}$$ và $$P = I^2 R$$, ghi rõ là số ước lượng từ tài liệu.
5. Viết một câu chọn giá trị cầu chì trên dây dương pin cho hai động cơ và giải thích vì sao giá trị đó cao hơn dòng chạy bình thường.

### Kết quả mong đợi

Sổ `lab-notes.md` có đầy đủ dòng không tải đo được, dòng stall 1 giây (hoặc công suất stall tính từ datasheet) và câu chọn cầu chì (thường 2 A hoặc 3 A cho robot TT chạy 2S) kèm so sánh với tổng dòng chạy.

### Lỗi thường gặp

| Hiện tượng | Cần kiểm tra |
|------------|--------------|
| Đồng hồ dòng báo gần 0 dù trục đang quay | Mắc đồng hồ song song thay vì nối tiếp, hoặc cắm nhầm lỗ đo áp |
| Sụt nguồn và vi điều khiển reset | Đang lấy nguồn động cơ từ USB hoặc pin yếu; chuyển sang pin đủ dòng có bảo vệ |
| Tản nhiệt L298N nóng rát sau thời gian ngắn | Công suất sụt áp lớn; giảm thời gian tải nặng, tăng thoáng khí hoặc đổi TB6612 |
| Polyfuse ngắt và giữ trạng thái hở nhiều phút | Cầu chì đang bảo vệ mạch; chờ nguội và xử lý điểm chập trước khi thử lại |
| Robot giật chạy sau khi reset | `setup()` chưa ép `PWM = 0` ngay từ đầu |

## Mua ở Việt Nam

Chỉ cần chuẩn bị thêm cầu chì 2–3 A (cầu chì thủy tinh, cầu chì lưỡi hoặc polyfuse kèm đế) nếu bộ kit chưa có; giá tham khảo thay đổi theo thời điểm (cầu chì và đế khoảng 5.000–25.000 VND, động cơ TT khoảng 25.000–45.000 VND, L298N khoảng 35.000–70.000 VND):

- Trang L298N đã kiểm tra, khoảng 45.000 VND: [hshop.vn/mach-dieu-khien-dong-co-dc-l298](https://hshop.vn/mach-dieu-khien-dong-co-dc-l298)
- HShop: [cầu chì](https://hshop.vn/search?q=cau%20chi), [motor TT](https://hshop.vn/search?q=motor%20TT), [TB6612](https://hshop.vn/search?q=TB6612)
- Shopee: [cầu chì](https://shopee.vn/search?keyword=cau%20chi), [polyfuse](https://shopee.vn/search?keyword=polyfuse), [motor TT](https://shopee.vn/search?keyword=motor%20TT)
- Lazada: [cầu chì](https://www.lazada.vn/catalog/?q=cau%20chi), [motor TT](https://www.lazada.vn/catalog/?q=motor%20TT)
- Thế Giới IC: [cầu chì](https://www.thegioiic.com/search?q=cau%20chi), [L298N](https://www.thegioiic.com/search?q=L298N)

## Video tham khảo

- **Xem trước:** [Do you know how to Test Stall Current?](https://www.youtube.com/watch?v=7KbEVKZ2JhA) — SoundTraxx, tiếng Anh. Minh họa kỹ thuật đo dòng khi giữ kẹt trục (áp dụng tương tự cho động cơ TT).
- [What is a fuse? the basics explained](https://www.youtube.com/watch?v=W770Z1yvXs8) — The Engineering Mindset, tiếng Anh. Giải thích nguyên lý hoạt động và cách chọn cầu chì bảo vệ mạch.

## Bài tập

1. Một động cơ 6 V có dòng stall 1,2 A. Tính điện trở cuộn $$R$$ và công suất tỏa nhiệt khi stall.
2. Hai động cơ trên kẹt trục cùng lúc sẽ hút tổng dòng bao nhiêu, và vì sao cổng USB 0,5 A không thể cấp nguồn cho chúng?
3. Một kênh L298N sụt 2 V ở dòng tải 0,8 A. Kênh này tỏa bao nhiêu watt nhiệt?
4. Khi chạy bình thường, mỗi bánh hút 0,35 A và mạch logic hút 0,15 A. Cầu chì 2 A trên dây dương pin có phù hợp (lớn hơn tổng dòng chạy) không?
5. ESP32 bị reset mỗi khi động cơ khởi động và khiến robot tự trôi đi. Cần thay đổi gì ở phần cứng và những dòng đầu tiên của hàm `setup()`?

### Gợi ý đáp án

1. $$R \approx 6 / 1.2 = 5~\Omega$$ và $$P = 1.2^2 \times 5 = 7.2~\mathrm{W}$$.
2. Tổng dòng khoảng 2,4 A, vượt xa mức 0,5 A của cổng USB nên phải dùng pin và cầu chì riêng.
3. $$P = 2~\mathrm{V} \times 0.8~\mathrm{A} = 1.6~\mathrm{W}$$.
4. Tổng dòng chạy là $$0.35 + 0.35 + 0.15 = 0.85~\mathrm{A}$$, nhỏ hơn nhiều so với 2 A nên cầu chì 2 A phù hợp.
5. Phần cứng: tách nguồn động cơ sang pin khỏe hơn kèm cầu chì; phần mềm: đặt `PWM = 0` và cấu hình chân hướng an toàn ngay đầu `setup()`.

## Đọc thêm

- SparkFun — động cơ và thông số dòng stall: [https://learn.sparkfun.com/tutorials/motors-and-selecting-the-right-one/all](https://learn.sparkfun.com/tutorials/motors-and-selecting-the-right-one/all)
- Datasheet ST L298 (sụt áp và công suất tỏa nhiệt): [https://www.st.com/resource/en/datasheet/l298.pdf](https://www.st.com/resource/en/datasheet/l298.pdf)
- Mạch mang TB6612FNG của Pololu (hiệu suất cao hơn cho dòng động cơ TT): [https://www.pololu.com/product/713](https://www.pololu.com/product/713)
