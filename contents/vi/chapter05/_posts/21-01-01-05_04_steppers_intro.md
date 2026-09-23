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

Stepper đi theo những góc đã đếm. Bạn bảo nó bước bao nhiêu, rồi tin rằng nó đã bước bấy nhiêu. Bài này nói về motor hybrid 1,8 độ, vi bước (microstep) thực sự làm mượt cái gì, cách đặt dòng cuộn trên board kiểu A4988 mà không đoán mò chiết áp, và vì sao bánh của Capstone A vẫn ở lại với motor DC cùng encoder.

## Mục tiêu học

Hết bài, bạn đổi 1,8 độ mỗi bước đầy thành 200 bước đầy mỗi vòng, và nói được trục ra làm gì sau một hộp số. Bạn giải thích vi bước là một chỉnh độ mượt (1/2, 1/4, 1/16) trong khi mô-men giữ vẫn là mô-men giữ của motor. Bạn tính điện áp chuẩn của A4988 cho một dòng đã chọn khi điện trở cảm là $$0.068~\Omega$$, và biết phải đo lại nếu bản clone dùng $$0.1~\Omega$$. Bạn gọi tên được kiểu hỏng vòng hở: mất bước dưới tải thì im, và bạn đứng ở sai vị trí.

## Kiến thức cần có

Bạn đo được một điện áp một chiều nhỏ, xuống gần nửa volt, que đen của đồng hồ trên mass. Định luật Ohm và ý niệm dòng stall từ bài motor DC chuyển thẳng sang “dòng trong một cuộn”. Bạn không cần stepper trên bàn. Một ảnh A4988 hoặc DRV8825, cộng phép tính, là xong lab. Nếu có NEMA17 trần, bạn có thể đếm một vòng.

## Vì sao bài này quan trọng với Capstone A và ROS

Capstone A dẫn động bằng motor hộp số DC và encoder. Encoder khép vòng mà stepper giả vờ không cần. Stepper quay lại khi bạn thêm một cánh tay nhỏ, một cơ cấu nhấc bút, hoặc một ray trượt camera: một khớp phải giữ vị trí khi còn nguồn và đi một góc đã biết. Quỹ đạo khớp của ROS giả định bạn biết số bước mỗi vòng của trục ra sau hộp số. Nếu bạn quảng cáo 200 bước mỗi vòng trên một trục đang đứng sau hộp số 50:1, cánh tay sẽ đi một phần rất nhỏ của góc mà planner đã vẽ. Đặt đúng giới hạn dòng là thứ giữ khớp đó khỏi mất bước trong khi quỹ đạo vẫn “thành công” trên phần mềm.

## Bước đầy, và cách mất chúng trong im lặng

Một stepper hybrid phổ biến được ghi 1,8 độ mỗi bước đầy.

$$
\frac{360^\circ}{1.8^\circ} = 200
$$

bước đầy mỗi vòng của trục motor. Các driver như Allegro A4988 và TI DRV8825 là cầu băm: chúng đóng cắt điện áp cuộn sao cho dòng trong mỗi cuộn dây ở gần một giới hạn bạn đặt. Chân STEP đẩy bộ dịch. Chân DIR chọn dấu. Motor giữ vị trí bằng cách duy trì dòng trong các cuộn ngay cả khi trục đứng yên, đó là lý do stepper đang có nguồn thì ấm lúc nghỉ.

Vi bước (1/2, 1/4, 1/8, 1/16 trên A4988 điển hình, và các chế độ mịn hơn trên DRV8825) chia mỗi bước đầy thành những mẫu dòng nhỏ hơn, nên chuyển động nghe mượt hơn và cộng hưởng dễ chịu hơn. Nó không nhân mô-men giữ lên 16. Mô-men bạn chống lại bằng ngón tay vẫn do motor, giới hạn dòng, và nguồn quyết định. Dưới một bàn tay nặng, rôto có thể tụt sau bước điện. Không gì trong driver giơ cờ lỗi. Cơ cấu giờ ở sai góc, còn bộ đếm bước của chương trình vẫn tin quỹ đạo. Đó là vòng hở. Một encoder, nếu bạn thêm, mới biến lời nói dối ấy thành một con số bạn nhìn thấy.

Trên A4988, các chân MS1, MS2 và MS3 chọn hệ số chia. Bảng in trên lụa là chuẩn của board bạn; mẫu thường gặp đi từ tất cả thấp (bước đầy) lên tất cả cao (1/16). Hãy để các chân đó ở một trạng thái đã biết. Một chân MS nổi là một chế độ vi bước ngẫu nhiên.

## Chiết áp giới hạn dòng

Board A4988 kiểu Pololu dùng điện trở cảm $$0.068~\Omega$$ dưới chip. Giới hạn dòng và điện áp trên cần gạt chiết áp liên hệ bởi

$$
I_{max} = \frac{V_{ref}}{8 \times 0.068} = \frac{V_{ref}}{0.544}
$$

Bạn đặt $$V_{ref}$$ bằng chiết áp nhỏ, đo từ cần gạt xuống mass, driver đã có nguồn và các cuộn motor đã nối, trừ khi ghi chú của nhà bán bảo một quy trình an toàn khác. Board clone đôi khi gắn điện trở cảm $$0.1~\Omega$$. Khi ấy số 0,544 ở mẫu số sai với PCB của bạn, và bạn tính lại $$8 \times R_{sense}$$ từ ghi chú sản phẩm trước khi vặn chiết áp. Một chiết áp vặn hết cữ “cho khỏe” có thể đặt một dòng mà motor không tản nổi thành nhiệt.

Đừng rút một cuộn khi driver còn enable. Cuộn là một cuộn cảm, và mở nó khi đang có dòng sẽ ném một cú sốc cảm ứng vào chip. Disable driver, hoặc rút VM, trước khi sắp lại dây motor.

## Demo unipolar có hộp số là một loài khác

28BYJ-48 bán kèm board ULN2003 là motor unipolar 5 V nhỏ với hộp số nhựa. Nó là demo bàn dễ chịu: năm dây, một dãy Darlington, và chuyển động chậm đếm được bằng mắt. Nó là bánh dẫn động tồi cho Capstone. Hộp số được làm cho tải kiểu đồng hồ, mẫu dòng là bước unipolar qua ULN2003, và tốc độ cùng mô-men ở trục ra không thuộc về dưới một khung robot. Hãy thích nó như một thí nghiệm “bước là có thật”. Gắn lại motor TT lên cầu H cho con robot phải lăn.

## Ví dụ tính

Bạn muốn giới hạn dòng 1,0 A trên A4988 kiểu Pololu với điện trở cảm $$0.068~\Omega$$.

$$
V_{ref} = I_{max} \times 0.544 = 1.0 \times 0.544 = 0.544~\mathrm{V} \approx 0.54~\mathrm{V}
$$

Que đen trên GND, que đỏ trên cần gạt chiết áp, driver có nguồn, cuộn đã nối (hoặc theo nhà bán nếu họ bắt một thứ tự cụ thể). Vặn chiết áp đến khi đọc khoảng 0,54 V. Nếu ghi chú board nói điện trở cảm là $$0.1~\Omega$$, tính lại:

$$
V_{ref} = I_{max} \times (8 \times 0.1) = 0.80~\mathrm{V}
$$

cho cùng 1,0 A. Dùng 0,54 V trên bản clone đó sẽ đặt dòng thấp hơn bạn tưởng; vặn chiết áp hết cữ có thể đặt dòng cao hơn nhiều. Viết giá trị điện trở bạn giả định ngay cạnh điện áp đã đo.

Với một khớp ROS về sau, cũng viết số bước mỗi vòng của trục ra. Motor 200 bước ở vi bước 1/16 lấy $$200 \times 16 = 3200$$ vi bước mỗi vòng motor. Sau hộp số 50:1, đó là $$3200 \times 50 = 160000$$ vi bước mỗi vòng của trục ra. Bộ đổi quỹ đạo cần số của trục ra, không phải số 200 trần.

## Hình

![Đồng hồ số, dụng cụ bạn dùng trên chiết áp giới hạn dòng]({{ site.imgurl }}/wikimedia/Digital_Multimeter_Aka.jpg)

Que đen trên mass driver. Que đỏ trên cần gạt chiết áp, không phải trên VM. Bạn đang tìm một phần của volt. Nếu đọc được điện áp pin, bạn đang đặt que sai chân.

## Lab

### An toàn

Nếu driver đang có nguồn, đừng ngắt một cuộn motor. Đặt giới hạn dòng trước khi lệnh một hành trình dài. Giữ VM trong dải của driver (module A4988 thường dùng gần 8–12 V; hãy đọc board của bạn). 28BYJ-48 ở trên 5 V. Bánh của robot Capstone không liên quan đến lab này.

### BOM

| Món | Vai trò |
|------|------|
| Đồng hồ vạn năng | $$V_{ref}$$ |
| Module A4988 hoặc DRV8825, nếu có | Chiết áp và các chân MS |
| Stepper bốn dây cuộn, tùy chọn | Một vòng đếm được |
| Hoặc một ảnh rõ của module như vậy | Nhánh nhận diện |
| Sổ | Giá trị điện trở, $$V_{ref}$$, số bước |

### Các bước

1. Nếu không có phần cứng, vẽ chiết áp và các chân MS từ ảnh sản phẩm. Tính $$V_{ref}$$ cho 1,0 A với giả định $$0.068~\Omega$$, và viết số 0,80 V thay thế cho bản clone $$0.1~\Omega$$. Dừng ở đây.
2. Nếu có phần cứng, tìm ký hiệu điện trở cảm hoặc ghi chú sản phẩm. Ghi $$R_{sense}$$.
3. Nối các cuộn theo cặp mà datasheet gọi là một cuộn dây (điện trở vài ohm giữa hai dây của một cặp, và hở giữa các cuộn). Cấp nguồn driver theo cách nhà bán khuyên và đo $$V_{ref}$$. Chỉ chỉnh khi bạn hiểu đích.
4. Đặt chế độ bước đầy. Bước 200 lần với nhịp chậm và nhìn một cờ trên trục. NEMA17 trần 1,8 độ phải về lại cờ sau khoảng 200 bước. 28BYJ-48 có hộp số thì không.
5. Bóp nhẹ trục trong một chuyển động chậm và xem cờ có kết thúc sai chỗ trong khi code vẫn chạy xong không. Đó là mất bước. Thả ra trước khi driver hoặc motor nóng.

### Kết quả mong đợi

Một đích $$V_{ref}$$ đã viết cho 1,0 A với giá trị điện trở bạn giả định, và hoặc một ảnh có nhãn chiết áp cùng các chân MS, hoặc một vòng đã đếm (khoảng 200 bước đầy trên NEMA17 trần). Một câu nói rằng mất bước tự nó không giơ lỗi.

### Lỗi thường gặp

| Bạn thấy | Cần kiểm |
|--------------|----------------|
| Trục kêu mà không quay | Cặp cuộn bị đảo, giới hạn dòng gần không, hoặc sleep/enable đang bị giữ reset. |
| Motor và chip nóng lúc nghỉ | $$V_{ref}$$ cao hơn nhiều so với dòng định mức của motor. Hạ xuống. |
| Chuyển động mượt hơn bước đầy nhưng yếu dưới ngón tay | Vi bước đang bật. Mô-men không được nhân. |
| Vị trí chỉ trôi khi có tải | Mất bước. Hạ tốc độ, tăng dòng chỉ đến định mức motor, hoặc thêm encoder. |
| Đồng hồ hiện VM trên chiết áp | Que đỏ đang ở tiếp điểm sai. Chuyển sang cần gạt và đo xuống GND. |

## Mua ở Việt Nam / Where to buy in Vietnam

Bạn có thể xong bài này mà không mua gì. Nếu muốn một demo bàn, 28BYJ-48 kèm ULN2003 là bộ unipolar rẻ. NEMA17 cộng A4988 là cấu hình hybrid khớp số đếm 200 bước. Giá chạy. Khoảng thô: bộ 28BYJ-48 khoảng 25.000–50.000 VND, module A4988 khoảng 20.000–55.000 VND, NEMA17 thường 150.000–400.000 VND tùy chiều dài thân.

- HShop: [A4988](https://hshop.vn/search?q=A4988), [28BYJ-48](https://hshop.vn/search?q=28BYJ-48), [NEMA17](https://hshop.vn/search?q=NEMA17)
- Shopee: [A4988](https://shopee.vn/search?keyword=A4988), [28BYJ-48](https://shopee.vn/search?keyword=28BYJ-48)
- Lazada: [A4988](https://www.lazada.vn/catalog/?q=A4988), [DRV8825](https://www.lazada.vn/catalog/?q=DRV8825)
- Thế Giới IC: [A4988](https://www.thegioiic.com/search?q=A4988), [ULN2003](https://www.thegioiic.com/search?q=ULN2003)

## Bài tập

1. Motor 1,8 độ lấy bao nhiêu bước đầy mỗi vòng? Bấy nhiêu là bao nhiêu vi bước 1/16?
2. Điện trở cảm là $$0.068~\Omega$$ và bạn đo $$V_{ref} = 0.30~\mathrm{V}$$. Bạn đã đặt giới hạn dòng bao nhiêu?
3. Ghi chú clone nói $$R_{sense} = 0.1~\Omega$$. $$V_{ref}$$ nào cho 0,8 A?
4. Cánh tay chạy xong chương trình 400 bước mà đầu cánh còn thiếu so với vạch, không in lỗi. Sự kiện vật lý nào khớp các sự thật đó?
5. Bạn định một khớp ROS trên motor 200 bước, bước đầy, hộp số 30:1. Một vòng trục ra là bao nhiêu bước?

### Gợi ý đáp án

Motor 1,8 độ lấy 200 bước đầy và $$200 \times 16 = 3200$$ vi bước 1/16. Với $$0.068~\Omega$$, $$I_{max} = 0.30 / 0.544 \approx 0.55~\mathrm{A}$$. Với $$0.1~\Omega$$, $$V_{ref} = 0.8 \times 0.8 = 0.64~\mathrm{V}$$. Một khoảng thiếu im lặng là mất bước ở vòng hở. Một vòng trục ra ở bước đầy sau hộp số 30:1 là $$200 \times 30 = 6000$$ bước.

## Đọc thêm

- Mạch mang A4988 của Pololu, gồm mục giới hạn dòng và công thức $$V_{ref}$$: [https://www.pololu.com/product/1182](https://www.pololu.com/product/1182)
- Datasheet TI DRV8825 (driver stepper kiểu băm và các chế độ vi bước): [https://www.ti.com/lit/ds/symlink/drv8825.pdf](https://www.ti.com/lit/ds/symlink/drv8825.pdf)
- Chọn motor của SparkFun, cho ngôn ngữ mô-men và dòng để đối chiếu với các bài DC: [https://learn.sparkfun.com/tutorials/motors-and-selecting-the-right-one/all](https://learn.sparkfun.com/tutorials/motors-and-selecting-the-right-one/all)
