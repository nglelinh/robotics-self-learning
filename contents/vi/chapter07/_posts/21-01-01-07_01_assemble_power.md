---
layout: post
title: "Lắp khung, motor và nguồn"
chapter: "07"
order: 1
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter07
lesson_type: required
draft: false
---

Bài này chuyển tấm khung rời thành một khung robot hoàn chỉnh, nhưng bánh xe vẫn chưa được cấp PWM để quay. Bạn sẽ lắp động cơ, gắn bánh caster, cố định khối pin và đo kiểm toàn bộ cây nguồn trước khi nạp bất kỳ chương trình điều khiển nào.

## Mục tiêu học

1. Lắp hai động cơ TT sao cho lốp không cọ tấm mica, gắn bánh caster với vết tiếp xúc nằm sau chốt xoay, và cố định pin để trọng tâm rơi vào khoảng giữa trục bánh chủ động và bánh caster.
2. Đi dây cực dương pin qua công tắc nguồn, cầu chì 2–3 A rồi tách sang nhánh VM của mạch driver và đầu vào mạch hạ áp LM2596; chỉnh đầu ra buck về 5,0 V trước khi gắn ESP32.
3. Nối cực âm pin, GND driver, GND buck và GND vi điều khiển về một điểm mass chung, đồng thời giữ toàn bộ dây động cơ trên cầu đấu vít của driver (không qua breadboard).
4. Ghi điện áp pin không tải và điện áp đầu ra buck vào `lab-notes.md` kèm ảnh chụp đi dây; không sử dụng cổng USB làm nguồn nuôi động cơ.

## Kiến thức cần có

Bài trước ([pin và cây nguồn]({% multilang_post_url contents/chapter07/07_00_batteries_power_safety %})) đã xác định hóa học pin và quy trình chỉnh buck về 5,0 V trước khi gắn ESP32. Chương 04 đã nhấn mạnh cảm biến và vi điều khiển phải chung đất. Chương 05 trình bày mạch cầu H: TB6612 sẽ ở trạng thái ngủ khi chân STBY ở mức thấp, còn IC ổn áp 7805 trên mạch L298N không đủ ổn định để nuôi ESP32. Chương 06 đã cung cấp hai kích thước hình học là khổ vết $$b$$ và bán kính lăn $$r$$ (mẫu tham khảo trong khóa học có $$b = 0{,}15~\mathrm{m}$$ và $$r = 31{,}2~\mathrm{mm}$$). Hãy chép sẵn hai số đo của riêng bạn vào ghi chú hôm nay. Bạn chỉ cần biết đo điện áp một chiều; bài này chưa dùng node ROS hay tín hiệu PWM.

## Vì sao bài này quan trọng với Capstone A và ROS

Chương này chưa làm việc trực tiếp với ROS 2. Ở các chương sau, thông điệp `geometry_msgs/Twist` sẽ gửi vận tốc tiến `linear.x` và vận tốc quay `angular.z` để một node tách thành lệnh cho hai bánh xe. Mọi thuật toán tách lệnh đều trở nên vô nghĩa nếu mũi xe bị bốc đầu khi chạy, mạch buck chưa được chỉnh điện áp hoặc vi điều khiển tự reset ngay khi động cơ khởi động. Các bài 03 và 04 sẽ dùng giao thức văn bản đơn giản thay cho `Twist`, nhưng phần cứng nguồn và cân bằng trọng tâm phải được hoàn thiện vững chắc ngay từ bước này.

## Trọng tâm phải nằm giữa trục và caster

Hai lốp xe tuyệt đối không được cọ vào tấm mica vì lực cản cọ sát sẽ đẩy động cơ về gần trạng thái kẹt (stall) và sinh nhiệt như đã phân tích ở Chương 05. Bánh caster lắp dưới phần mũi khung với trục xoay thẳng đứng và vết tiếp xúc nằm phía sau chốt xoay; nếu lắp ngược càng, bánh sẽ rung lắc khi di chuyển.

Khối pin phải được buộc cố định chắc chắn để không xê dịch làm lệch trọng tâm hoặc gây chập dây. Nhìn từ mặt bên, trọng tâm chung của xe phải nằm trong khoảng giữa trục hai bánh chủ động và điểm chạm đất của bánh caster. Nếu trọng tâm lệch ra phía sau trục bánh, mũi xe sẽ nhấc lên khi tăng tốc và khiến lệnh đi thẳng bị lệch hướng.

Chọn gốc tọa độ $$x = 0$$ tại trục hai bánh chủ động, điểm chạm caster tại $$x = +90~\mathrm{mm}$$ về phía mũi xe. Giả sử khung và hai động cơ nặng $$220~\mathrm{g}$$ có trọng tâm riêng tại $$x = +15~\mathrm{mm}$$, còn khối pin nặng $$90~\mathrm{g}$$. Tọa độ trọng tâm chung là:

$$
x_{cg} = \frac{220 \times 15 + 90 \times x_b}{310}.
$$

Nếu đặt pin phía sau trục tại $$x_b = -40~\mathrm{mm}$$:

$$
x_{cg} = \frac{3300 - 3600}{310} \approx -1{,}0~\mathrm{mm}.
$$

Trọng tâm rơi ra sau trục bánh nên bánh caster mất tải và mũi xe sẽ bốc đầu ngay khi tăng tốc. Ngược lại, nếu đặt cùng khối pin đó ở khoảng giữa trục và caster tại $$x_b = +35~\mathrm{mm}$$:

$$
x_{cg} = \frac{3300 + 3150}{310} \approx 20{,}8~\mathrm{mm},
$$

nằm gọn trong đoạn từ $$0$$ đến $$90~\mathrm{mm}$$. Khi đó bánh caster chịu một phần tải trọng khoảng $$(20{,}8/90)\times 310~\mathrm{g} \approx 72~\mathrm{g}$$, đủ để giữ mũi xe bám sàn ổn định trong khi hai bánh chủ động vẫn gánh phần lớn trọng lượng. Hãy ghi lại giá trị $$x_b$$ thực tế của bạn bên cạnh $$b$$ và $$r$$.

![Bề rộng $$b$$ và caster phải còn tải]({{ site.imgurl }}/generated/chassis_measures.png)

## Cây nguồn, đo trước khi gắn MCU

Nhánh công suất động cơ và nhánh logic dùng chung khối pin và chung điểm mass, nhưng tuyệt đối không dùng chung một IC ổn áp tuyến tính và không đi dòng động cơ qua breadboard.

![Pin, cầu chì, VM, và buck chỉnh 5,0 V trước khi cắm MCU]({{ site.imgurl }}/generated/power_tree.png)

Cực dương pin nối qua công tắc nguồn, qua cầu chì 2–3 A, rồi rẽ làm hai nhánh: nhánh VM cấp cho mạch driver và nhánh vào của mạch hạ áp LM2596. Cực âm pin, GND driver, GND buck và GND của vi điều khiển phải nối chung về một nút. Toàn bộ dây động cơ đi thẳng từ cầu đấu vít của driver tới hai cực động cơ, không cắm qua breadboard vì tiếp điểm breadboard chỉ chịu được vài trăm miliampe trong khi dòng kẹt động cơ lên tới cỡ ampe.

Luôn chỉnh đầu ra mạch buck trước khi cắm vi điều khiển. Pack pin 2S đầy thường đo khoảng $$8{,}2~\mathrm{V}$$ không tải (dải hoạt động $$7{,}4$$–$$8{,}4~\mathrm{V}$$). Dùng đồng hồ đo hai cực đầu ra buck và vặn chiết áp về đúng $$5{,}0~\mathrm{V}$$ (chẳng hạn $$5{,}02~\mathrm{V}$$ khi không tải). Chỉ sau khi xác nhận mức áp này, bạn mới cấp nguồn cho ESP32 (hoặc cấp nguồn ESP32 qua cáp USB lúc nạp code nhưng vẫn giữ nối chung GND). Không bao giờ đưa điện áp VM vào chân 5 V hay 3,3 V của ESP32, và không dùng cổng USB (giới hạn khoảng $$500~\mathrm{mA}$$) để nuôi động cơ khi hai động cơ TT có dòng kẹt khoảng $$2{,}4~\mathrm{A}$$.

Trên mạch L298N, jumper 5 V kích hoạt IC ổn áp tuyến tính 7805 lấy nguồn từ VM. Với pin 2S, đầu ra này tạm đủ nuôi phần logic nội bộ của chính chip L298N nhưng không đủ ổn định cho ESP32 khi phát Wi-Fi, nên vẫn bắt buộc dùng mạch buck rời cho ESP32 (nếu VM lớn hơn $$12~\mathrm{V}$$, phải rút bỏ jumper 5 V). Kiểm tra công suất tỏa nhiệt trên 7805 tại điện áp đỉnh 2S với dòng $$0{,}25~\mathrm{A}$$:

$$
P \approx (8{,}4 - 5{,}0) \times 0{,}25 = 0{,}85~\mathrm{W}
$$

trên một vỏ IC nhỏ; ở mức $$12~\mathrm{V}$$ với cùng dòng điện, nhiệt lượng tăng lên $$1{,}75~\mathrm{W}$$. Do đó, cấp nguồn ESP32 qua mạch buck là lựa chọn bắt buộc trong cả hai trường hợp.

Pin lithium phải luôn đặt trong đế pin hoặc pack có mạch BMS, không để đầu dây hàn trần dễ chạm chập. Sạc pin bằng bộ sạc đúng số cell và luôn có người giám sát. Mạch TP4056 chỉ dành cho pin 1S (đầy gần $$4{,}2~\mathrm{V}$$), không thể tạo ra $$8{,}4~\mathrm{V}$$ và không cân bằng được hai cell nối tiếp trên pack 2S.

## Lab

### An toàn

Bài thực hành này không phát PWM nên có thể đặt xe trực tiếp trên mặt bàn. Giữ công tắc pin ở trạng thái ngắt cho đến khi công tắc, cầu chì và toàn bộ dây mass đã đấu xong. Đảm bảo pin lithium nằm trong đế hoặc pack có BMS, không gắn TP4056 vào pack 2S. Nếu mạch buck có mùi khét hoặc nóng bất thường, ngắt công tắc nguồn ngay lập tức.

### BOM

| Món | Việc |
|------|------|
| Khung 2WD, hai motor TT, lốp, caster | Phần cơ chương 06 |
| Pack 2S hoặc đế 18650 có BMS | Nguồn motor và logic |
| Công tắc, đế cầu chì, chì 2–3 A | Nhánh dương |
| TB6612 (nên dùng) hoặc L298N | Chỉ cấp VM; hôm nay chưa ra lệnh |
| Buck LM2596 | Logic 5,0 V, chỉnh trước MCU |
| ESP32 devkit | Gắn sau khi buck đã 5,0 V |
| Đồng hồ, dây buộc, `lab-notes.md` | Số đo |

### Các bước

1. Bắt cố định hai động cơ TT lên khung, sau đó dùng tay xoay thử từng lốp để chắc chắn không bị cọ vào tấm mica.
2. Lắp bánh caster sao cho vết tiếp xúc nằm phía sau chốt xoay. Chép hai thông số $$b$$ và $$r$$ từ Chương 06 vào sổ tay hôm nay.
3. Buộc cố định khối pin vào khoảng giữa trục bánh và bánh caster. Ước lượng tọa độ trọng tâm $$x_{cg}$$ và ghi kết quả theo milimét.
4. Đấu dây cực dương pin qua công tắc, cầu chì rồi rẽ sang VM của driver và đầu vào buck. Nối chung cả bốn điểm mass; đảm bảo dây động cơ chỉ bắt trên cầu đấu vít của driver.
5. Khi chưa gắn ESP32, bật công tắc pin. Đo điện áp pack không tải và đầu ra mạch buck, vặn biến trở buck về đúng $$5{,}0~\mathrm{V}$$, chụp ảnh hệ thống dây rồi mới gắn ESP32 vào đường nguồn 5 V (hoặc cấp USB nạp code nhưng giữ mass chung).

### Kết quả mong đợi

Tệp `lab-notes.md` có ghi ngày, điện áp pack không tải (ví dụ $$8{,}15~\mathrm{V}$$ với pack 2S đầy), điện áp đầu ra buck sai lệch chỉ vài chục milivôn quanh $$5{,}0~\mathrm{V}$$ đo trước khi gắn MCU, hai số đo $$b$$, $$r$$ và xác nhận dây động cơ không đi qua breadboard. Ảnh chụp thể hiện rõ công tắc, cầu chì, dây buộc pin và điểm mass chung. Chưa có lệnh quay bánh nào được thực hiện.

### Lỗi thường gặp

| Bạn thấy | Thường là |
|----------|-----------|
| Mũi nhấc khi đặt xe xuống | Pin nằm sau trục; dịch về phía caster |
| Lốp cà mica | Sai đệm; sau này thành stall |
| Buck ra 8 V hoặc 12 V | Chiết áp còn ở đầu; đừng cắm ESP32 |
| ESP32 reset khi chạm VM | Logic đang ăn 7805, hoặc đất chưa thành một nút |
| Với tay lấy TP4056 | Mạch ấy là 1S; pack 2S cần sạc 2S và BMS |

## Mua ở Việt Nam / Where to buy in Vietnam

Chỉ đặt mua các linh kiện còn thiếu, không cần mua thêm bộ robot mới. Giá tham khảo khoảng năm 2026 (có thể thay đổi theo thời điểm): khung mica 2WD 60.000–150.000 đồng, động cơ TT 25.000–45.000 đồng/chiếc, module TB6612 25.000–70.000 đồng, mạch buck LM2596 10.000–25.000 đồng, pack 2S hoặc đế 18650 80.000–180.000 đồng, công tắc 8.000–20.000 đồng, đế cầu chì kèm chì 2–3 A 10.000–25.000 đồng, ESP32 devkit 70.000–150.000 đồng. Nếu hết TB6612, có thể dùng tạm L298N (đã kiểm tra giá khoảng 45.000 đồng), nhưng TB6612 mát hơn và trong mọi trường hợp vẫn dùng mạch buck để cấp nguồn ESP32. Lưu ý đế 1S không thay thế được pack 2S.

- L298N đã kiểm, khoảng 45.000 đồng: [hshop.vn/mach-dieu-khien-dong-co-dc-l298](https://hshop.vn/mach-dieu-khien-dong-co-dc-l298)
- [Hshop khung](https://hshop.vn/search?q=khung+xe+2wd), [buck](https://hshop.vn/search?q=LM2596), [ESP32](https://hshop.vn/search?q=ESP32)
- [Shopee khung 2WD](https://shopee.vn/search?keyword=khung%20xe%202WD%20acrylic), [LM2596](https://shopee.vn/search?keyword=LM2596), [cầu chì](https://shopee.vn/search?keyword=c%E1%BA%A7u%20ch%C3%AC%202A)
- [Lazada ESP32](https://www.lazada.vn/catalog/?q=ESP32), [pin 18650](https://www.lazada.vn/catalog/?q=pin%2018650%202S)
- [Thế Giới IC LM2596](https://www.thegioiic.com/search?q=LM2596), [ESP32](https://www.thegioiic.com/search?q=ESP32)

## Video tham khảo

- **Xem trước:** [PART1: Building Low-Cost Differential Wheeled Robot For Machine Learning, SLAM, and ROS](https://www.youtube.com/watch?v=RsZBxfpcLu8) — Aleksandar Haber PhD, tiếng Anh. Trình tự lắp đặt một robot vi sai cỡ nhỏ từ khung, động cơ tới hệ thống nguồn; giữ pin ngắt cho tới khi đo xong điện áp buck.
- [BMS (Battery Management System) || DIY or Buy || Properly protecting Li-Ion/Li-Po Battery Packs](https://www.youtube.com/watch?v=rT-1gvkFj60) — GreatScott!, tiếng Anh. Minh họa bố trí pack pin và BMS thực tế trên xe; chú ý cực tính và đầu giắc trước khi đóng nắp.

## Bài tập

1. Khung và hai động cơ nặng $$220~\mathrm{g}$$ có trọng tâm tại $$x = +15~\mathrm{mm}$$, pin nặng $$90~\mathrm{g}$$ đặt tại $$x_b = -20~\mathrm{mm}$$, bánh caster ở $$+90~\mathrm{mm}$$. Tính $$x_{cg}$$ và cho biết mũi xe có giữ được trên sàn không.
2. Mạch buck đo không tải được $$5{,}02~\mathrm{V}$$, nhưng khi gắn ESP32 điện áp tụt xuống còn $$4{,}15~\mathrm{V}$$. Cần kiểm tra những gì trước khi kết luận bo mạch hỏng?
3. Một sinh viên nối một mạch TP4056 vào hai đầu pack 2S để sạc qua cổng USB. Lỗi sai về số cell ở đây là gì và cần dùng loại bộ sạc nào?
4. Với VM là $$8{,}4~\mathrm{V}$$ và jumper 5 V của L298N vẫn cắm, ước lượng công suất tỏa nhiệt trên IC 7805 ở dòng $$0{,}25~\mathrm{A}$$. Vì sao vẫn phải cấp nguồn ESP32 bằng mạch buck?
5. Hai dây động cơ bị cắm xuyên qua breadboard trước khi vào driver, và cầu chì lại đặt sau mạch buck thay vì trên cực dương pin. Hãy viết lại đúng thứ tự cây nguồn (pin, công tắc, cầu chì, tải) và nêu rõ giới hạn của breadboard.

### Gợi ý đáp án

1. $$x_{cg} = (3300 - 1800)/310 \approx 4{,}8~\mathrm{mm}$$. Điểm này vẫn nằm giữa trục và caster nên mũi xe chưa nhấc, nhưng tải đè lên caster khá nhẹ; nếu caster rung hoặc kêu, nên dời pin về phía trước khoảng $$+35~\mathrm{mm}$$.
2. Kiểm tra dây nối mass chung, kiểm tra xem cổng USB và đầu ra buck có đang cấp song song vào chân 5 V không, và kiểm tra dây quá mảnh hoặc mạch buck bị sụt áp khi chịu tải. Không vặn chiết áp buck trong lúc ESP32 đang cắm.
3. TP4056 là mạch sạc dành cho 1 cell (1S, đầy ở $$4{,}2~\mathrm{V}$$). Pack 2S có điện áp đầy gần $$8{,}4~\mathrm{V}$$ nên bắt buộc dùng bộ sạc 2S có cân bằng và BMS.
4. $$P \approx (8{,}4 - 5{,}0)\times 0{,}25 = 0{,}85~\mathrm{W}$$. Khi ESP32 phát Wi-Fi, dòng đỉnh vượt quá 0,25 A khiến IC 7805 nóng và sụt áp. Jumper 5 V trên 2S chỉ tạm nuôi logic của L298N (và phải rút bỏ nếu VM trên $$12~\mathrm{V}$$), còn ESP32 phải dùng mạch buck.
5. Thứ tự đúng: cực dương pin → công tắc → cầu chì 2–3 A → tách nhánh sang VM của driver và đầu vào buck. Dây động cơ nối trực tiếp trên cầu đấu vít vì tiếp điểm breadboard chỉ chịu được vài trăm miliampe, không chịu nổi dòng khởi động và dòng kẹt cỡ ampe.

## Đọc thêm

- [Datasheet L298 của ST](https://www.st.com/resource/en/datasheet/l298.pdf)
- [Mạch Pololu TB6612FNG](https://www.pololu.com/product/713)
- [geometry_msgs/Twist (Jazzy)](https://docs.ros.org/en/jazzy/p/geometry_msgs/interfaces/msg/Twist.html)
- [Arduino `Serial`](https://www.arduino.cc/reference/en/language/functions/communication/serial/)
