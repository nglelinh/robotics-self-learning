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

Thời lượng ước tính: **70–90 phút**. Các bạn làm xong lab từ một bức ảnh chi tiết in bị gãy. Có máy in hay không là tùy chọn.

## Mục tiêu học

Hết bài này, các bạn chọn một tấm mica 2WD mua sẵn cho Capstone A và dành in 3D cho giá đỡ, giá cảm biến, và đai giữ pin. Các bạn dự đoán một khe cắt laser 0,1–0,2 mm làm lỗ đã vẽ thay đổi thế nào, nêu được nhiệt độ mà nhựa PLA mềm trong ô tô kín, và xoay giá động cơ sao cho lực siết bu-lông không bóc các lớp in ra khỏi nhau.

## Kiến thức cần có

Các bạn biết hình học khung từ Bài 01 và thói quen ốc M3 từ Bài 02. Không cần bản quyền CAD. Một phác bằng bút chì, có ghi chiều dày bằng milimét, là đủ.

## Vì sao bài này quan trọng với Capstone A và ROS

Capstone A phải lăn được trong tháng này. Một bản in của cả khung nuốt cả tuần trên một máy các bạn có thể không có, và một tấm nhựa PLA để trong ô tô đỗ có thể vênh trước khi URDF xong. Hãy mua khung mica 2WD. In những mảnh bộ kit không có: một giá nhằm cảm biến siêu âm, một đai ngăn pin trượt (Bài 07), một nắp nhỏ che mối hàn. ROS không nhìn thấy tên polyme. Nó nhìn vị trí bánh. Một giá động cơ nứt làm những vị trí ấy đổi, và $$b$$ các bạn đã đo trở thành lời nói dối. Chọn vật liệu là cách $$b$$ giữ nguyên con số trong `diff_drive_controller`.

## Tấm mica, giá in

Mica đúc dày khoảng 3 mm là tấm kit thông thường. Nó phẳng, cắt laser sạch, và giòn. Một con ốc siết vào lỗ đã chật sẽ nêm nhựa, và vết nứt chạy giữa các lỗ. Hãy cho mỗi ốc M3 một lỗ thông và một đai ốc phía sau, loại nyloc của Bài 02. Mica là vật liệu khớp cài kém. Thiết kế ngàm bằng PETG, hoặc bỏ ngàm ra khỏi Capstone.

Khe cắt laser là bề rộng vật liệu tia đốt mất, thường 0,1–0,2 mm trên máy cắt sở thích khi cắt mica. Xưởng cắt đúng đường các bạn vẽ. Một lỗ có đường kính vẽ chính là đường kính đường chạy sẽ ra lớn hơn khoảng bằng khe cắt ấy:

$$
d_{\text{cut}} \approx d_{\text{drawn}} + k.
$$

Vẽ lỗ thông 3,2 mm và khe cắt 0,2 mm cho khoảng 3,4 mm, ốc M3 vẫn đi qua sạch. Vẽ lỗ 3,0 mm vì muốn ốc cắn vào mica, đường cắt rơi gần 3,2 mm, ốc lắc, và siết quá tay bắt đầu vết nứt. Nói với xưởng chiều dày, gửi DXF theo milimét, và giữ các đường kín. Một đường hở là một yêu cầu máy sẽ kết thúc theo hướng các bạn không chọn.

Nhựa PLA in dễ và mềm trong ô tô kín, khoảng 55–60 °C, tức một buổi chiều bình thường ở Việt Nam. Một giá vuông lúc sáng có thể từ từ biến dạng trước giờ lab. PETG chịu nhiệt ấy tốt hơn và tạo sợi nhiều hơn khi in, nên chi tiết cần vài phút với dao. Với giá động cơ, yêu cầu ẩn là hướng in. Sợi đùn yếu nhất giữa các lớp. Lực siết bu-lông và mô-men động cơ mà bóc lớp này khỏi lớp kia sẽ xé tai giá. Xoay mô hình sao cho mặt phẳng mà lực căng muốn xé cắt ngang các đường lớp. Vết nứt khi đó phải bẻ một sợi, không phải kéo khóa một mối dán. Một giá in “nằm đẹp” với tai đứng trên ranh giới lớp chính là cái gãy ở lần kẹt đầu tiên.

Các bạn làm được tất cả việc này khi không có máy in. Lab trường hoặc một xưởng nhận STL theo milimét, một tên vật liệu, PLA hoặc PETG, và một ghi chú về hướng in nếu các bạn quan tâm. Xưởng laser muốn DXF, milimét, đường kín, và chiều dày tấm đã nêu. Đặt những từ ấy vào email để đường cắt đầu tiên là đường các bạn đã đo.

![Tấm khung các bạn đang quyết định không in lại: đo nó, rồi chỉ in những giá nó còn thiếu]({{ site.imgurl }}/generated/chassis_measures.png)

Hình là khung đã mua. $$b$$ và $$r$$ là tính chất của cách tấm ấy giữ bánh. Một chi tiết in được phép giữ cảm biến. Nó là chỗ rủi ro nếu dùng để phát minh lại đường trục một tuần trước Chương 07.

## Ví dụ tính tay

Các bạn gửi một bản vẽ rãnh động cơ với lỗ M3 ở $$d_{\text{drawn}} = 3.2$$ mm. Xưởng báo khe cắt $$k = 0.15$$ mm.

$$
d_{\text{cut}} \approx 3.2 + 0.15 = 3.35\ \text{mm}.
$$

Ốc M3 khoảng 3,0 mm trên đỉnh ren, nên 3,35 mm là lỗ thông thoải mái. Đai ốc làm việc kẹp. Nếu thay vào đó các bạn vẽ 2,8 mm với hy vọng ren cắn trong mica,

$$
d_{\text{cut}} \approx 2.8 + 0.15 = 2.95\ \text{mm},
$$

và ốc hoặc không vào, hoặc sẽ nêm. Cú nêm ấy là vết nứt. Trên đai pin in, PLA ở 58 °C trong cabin kín đang nằm trong vùng mềm. PETG là vật liệu các bạn gọi tên cho đai ấy nếu robot từng phải chờ trong ô tô. Bản thân tấm khung vẫn là kit mica.

## Lab: đọc một lớp gãy, phác hướng in

### An toàn

Nhựa gãy sắc dọc lớp đã hỏng. Cầm ở cạnh, không cầm mảnh vụn. Nếu tới xưởng laser, bàn máy và phế phẩm còn nóng; để người vận hành đưa chi tiết cho các bạn. Không cần máy in, và không cần dung môi. Đừng “hàn” mica bằng keo tùy tiện khi vẫn đang nhận dạng dạng hỏng.

### BOM

| Hạng mục | Vai trò |
|------|------|
| Một chi tiết in đã gãy, hoặc một ảnh rõ của nó | Mổ lớp |
| Bút chì, hình cạnh và hình trước | Hướng giá |
| `lab-notes.md` | Phép khe cắt và câu vật liệu |

### Các bước

1. Nhìn vết gãy. Đường lớp là những sọc mảnh. Quyết định vết nứt chạy giữa các sọc hay cắt ngang chúng. Giữa các sọc nghĩa là tải đã bóc mặt phẳng yếu.
2. Phác một giá động cơ TT: một thành trên khung và một tai để bắt động cơ. Đánh dấu trục bu-lông. Vẽ đường lớp sao cho chúng cắt ngang mặt phẳng mà bu-lông sẽ xé. Viết “in úp mặt này xuống” lên mặt phải chạm bàn in để tạo những đường ấy.
3. Tính một ví dụ khe cắt cho một lỗ các bạn quan tâm, dùng $$k = 0.2$$ mm nếu xưởng chưa cho số của họ. Ghi đường kính đã vẽ và đường kính cắt dự kiến.
4. Viết phương án vật liệu Capstone trong một câu: khung mica mua sẵn; vật liệu in và tên chi tiết cho giá đỡ và đai pin.
5. Nếu không có chi tiết cũng không có ảnh, dùng bất kỳ ảnh in hỏng nào tìm được trong lab, và nói rõ điều đó.

### Kết quả mong đợi

Một ghi chú nêu mặt phẳng yếu, một phác có đánh dấu mặt bàn in và hướng lớp, và một cặp khe cắt chẳng hạn 3,2 mm đã vẽ và 3,4 mm dự kiến. Câu vật liệu chỉ mica cho tấm khung và PLA hoặc PETG cho giá, với PETG được gọi tên nếu đai phải gặp ô tô nóng.

### Lỗi thường gặp

| Các bạn thấy | Thường nghĩa là |
|--------------|------------------------|
| Vết nứt đi theo các sọc | Các lớp chính là mặt xé; xoay chi tiết |
| Lỗ chật và mica nứt chân chim | Lỗ vẽ bỏ qua khe cắt, hoặc ốc bị dùng như một tarô |
| Giá vênh sau một quãng nắng | PLA trên khoảng 55–60 °C |
| Xưởng cắt viền ngoài và bỏ lỗ | Đường hở, hoặc lỗ nằm trên một lớp xưởng đã tắt |
| STL trả về bé xíu | File theo inch, hoặc theo centimét, và xưởng đã theo các con số |

## Mua ở Việt Nam / Where to buy in Vietnam

Dành tiền cho khung mica 2WD. Chỉ mua cuộn nhựa nếu các bạn, hoặc lab của các bạn, sẽ in giá. Một việc cắt laser là dịch vụ, xưởng tính giá từ file DXF; mang chiều dày và đơn vị milimét trong cùng một câu với file.

| Mua gì | Từ khóa | Khoảng giá (VND) | Ghi chú |
|------|----------|------------------|-------|
| Khung mica 2WD | `khung xe robot 2 bánh` | 80.000–200.000 | Tấm của Capstone |
| Nhựa PLA, 1 kg | `nhựa PLA` | 250.000–450.000 | Dễ in; để xa ô tô kín |
| Nhựa PETG, 1 kg | `nhựa PETG` | 280.000–500.000 | Chịu nhiệt hơn, tạo sợi nhiều hơn |

Các trang tìm:

- [Hshop: khung](https://hshop.vn/search?q=khung+xe+robot)
- [Shopee: nhựa PLA](https://shopee.vn/search?keyword=nh%E1%BB%B1a%20PLA)
- [Lazada: nhựa PLA](https://www.lazada.vn/catalog/?q=nh%E1%BB%B1a%20PLA)
- [Thế Giới IC](https://www.thegioiic.com/search?q=nh%E1%BB%B1a%20PLA)

Giá dịch chuyển. Một xưởng laser địa phương thường là tấm biển trên cửa makerspace hơn là một mã hàng toàn quốc. Hãy xin DXF, milimét, đường kín, và chiều dày tấm họ có sẵn, thường là mica 3 mm.

## Bài tập

1. Lỗ vẽ 3,4 mm, khe cắt 0,2 mm. Đường kính các bạn chờ trên mica là bao nhiêu, và ốc M3 còn đi qua không?
2. Các bạn cần ốc cắn vào nhựa in. Phần cứng nào từ Bài 02 thay cho “ren do chính con ốc cắt trong PLA”?
3. Tai động cơ nứt sạch dọc các sọc lớp ngay lần bánh kẹt đầu tiên. Mặt phẳng yếu là gì, và bản in lại phải xoay thế nào?
4. Robot ngồi trong ô tô khoảng 58 °C. Sợi nhựa nào rủi ro cho đai pin, và các bạn gọi tên sợi nào thay vào?
5. Liệt kê kiểu file, đơn vị, và câu thêm các bạn gửi xưởng laser, rồi kiểu file và hai sự thật các bạn gửi xưởng in.

### Gợi ý đáp án

1. Khoảng 3,6 mm. Đỉnh ren M3 gần 3,0 mm, nên ốc đi qua với khe hở dư; giữ một đai ốc phía sau. 2. Một đai đồng nóng chảy, rồi một ốc máy, kèm nyloc nếu mối rung. 3. Liên kết giữa các lớp là mặt nứt. In lại sao cho đường lớp cắt ngang mặt ấy; đánh dấu mặt úp xuống bàn in. 4. PLA mềm quanh 55–60 °C. Gọi PETG cho đai ấy. 5. Laser: DXF, milimét, đường kín, và chiều dày. In: STL, milimét, và một vật liệu được gọi tên, cộng hướng in nếu xưởng chịu làm theo.

## Đọc thêm

- [Gỡ lỗi in trên RepRap](https://reprap.org/wiki/Print_Troubleshooting) — tách lớp, tạo sợi, và các triệu chứng các bạn vừa chẩn đoán.
- [Polylactic acid](https://en.wikipedia.org/wiki/Polylactic_acid) — vì sao nhiệt độ hữu ích của PLA nằm gần một cabin nóng.
- [Laser cutting](https://en.wikipedia.org/wiki/Laser_cutting) — khe cắt như bề rộng bị lấy đi, chính là hiệu chỉnh trong ví dụ tính tay.
