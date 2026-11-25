---
layout: post
title: "Tư duy an toàn cho lab robot"
chapter: "00"
order: 3
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter00
lesson_type: required
draft: false
---

Hãy dành khoảng 80 phút cho bài học này. Bạn hoàn toàn có thể hoàn thành bài trên giấy trước khi linh kiện giao tới. Nếu trên bàn của bạn đã có sẵn mỏ hàn hoặc cell pin lithium, mọi quy tắc trong bài cần được áp dụng ngay lập tức.

## Mục tiêu học

Sau bài học này, bạn sẽ **gọi tên** được ba mối nguy thực tế trên bàn làm việc: năng lượng tích trữ, bánh xe đang quay và firmware quên ngắt PWM. Bạn sẽ **viết** một thẻ quy trình cấp nguồn gọn trên một trang theo đúng thứ tự: nối mass chung, cấp nguồn logic từ USB, nối tín hiệu điều khiển, và cuối cùng mới cấp nguồn VM cho động cơ khi bánh xe đã nhấc khỏi mặt bàn. Bạn sẽ **áp dụng** nguyên tắc an toàn pin lithium: sạc cell 18650 riêng từng viên đến 4,2 V, tuyệt đối không kẹp mạch TP4056 vào đế pin 2S (8,4 V khi đầy). Bạn cũng sẽ **loại bỏ** mọi phương án đưa điện áp động cơ hay tín hiệu echo 5 V trực tiếp vào chân 3,3 V vì giới hạn cực đại tuyệt đối của GPIO ESP32 không chịu được 5 V; đồng thời **thực hiện** danh sách kiểm tra cấp nguồn chỉ bằng USB (không gắn động cơ) và **đối chiếu** sự cố với bảng xử lý lỗi.

## Cần có trước

Từ bài 00-01 và 00-02, bạn đã nắm rõ quy tắc dừng PWM sau 300 ms và đã chốt Lộ trình A hoặc B trong sổ lab. Lúc này chưa cần có sẵn linh kiện. Hãy ghi nhớ hai nguyên tắc nền tảng: chân GPIO chỉ dùng cho tín hiệu logic chứ không phải nguồn công suất, và một bánh xe còn chạm mặt bàn có thể kéo cả robot trượt đi ngay khi xung PWM khác 0.

---

Một viên pin Li-ion 18650 nhỏ gọn nằm lọt trong lòng bàn tay trông có vẻ vô hại — cho đến khi hai sợi dây đỏ và đen vô tình chạm nhau trên mặt bàn lộn xộn vụn thiếc hàn. Trong chưa đầy một giây, dòng điện vọt qua ngưỡng hàng chục ampe, lớp vỏ nhựa bốc khói và mạch vi điều khiển cháy rụi! **Tư duy an toàn phòng lab** không phải là danh sách nội quy nhàm chán; đó là kỹ năng phòng thủ bằng vật lý giúp bạn bảo vệ đôi mắt, bàn tay và chính ví tiền của mình.

## Kiến thức cần nhớ: Vật lý của Sự cố Điện và An toàn Pin Lithium

1. **Ngắn mạch & Công suất nhiệt Joule ($$P = I^2 R = V^2 / R$$):** Khi hai cực nguồn chạm trực tiếp, điện trở mạch giảm xuống chỉ còn nội trở pin $$r$$ (vài chục mili-ohm), đẩy dòng điện và nhiệt lượng tăng vọt theo bình phương dòng điện!
2. **An toàn Hóa học Pin Lithium (Li-ion / LiPo):** Pin lithium có mật độ năng lượng rất cao và chất điện phân dễ cháy. Xả sâu dưới $$3.0\text{ V/cell}$$, sạc quá $$4.2\text{ V/cell}$$ hoặc ngắn mạch đều có thể gây phồng pin và thoát nhiệt mất kiểm soát (*thermal runaway*).
3. **Trình tự cấp nguồn phân tầng (Power-On Sequence):** Luôn kiểm tra thông mạch nguồn–GND ở trạng thái tắt pin, cấp nguồn qua cổng USB giới hạn dòng 500 mA trước, rồi mới đóng cầu chì và bật công tắc pin động cơ.

### Ví dụ làm từng bước: Tính dòng ngắn mạch của bộ pin 2S 18650

Xét một bộ pin 2S Li-ion sạc đầy có điện áp $$V = 2 \times 4.2\text{ V} = \mathbf{8.4\text{ V}}$$ và tổng nội trở (2 cell + dây dẫn ngắn) chỉ khoảng $$r = 0.08\ \Omega$$. Nếu hai đầu dây nguồn vô tình chập nhau không qua cầu chì:

$$
I_{\text{ngắn mạch}} = \frac{V}{r} = \frac{8.4\text{ V}}{0.08\ \Omega} = \mathbf{105\text{ A}},
$$

$$
P_{\text{nhiệt}} = V \cdot I = 8.4 \times 105 = \mathbf{882\text{ W}}!
$$

Gần **900 watt** nhiệt tỏa ra ngay trong hai viên pin và sợi dây đồng mảnh — tương đương một chiếc bàn ủi điện dồn vào một điểm tiếp xúc 2 mm! Giờ lắp nối tiếp một **cầu chì 5 A** sát cực dương pin: ngay khi dòng vượt 10 A, dây chì chảy đứt trong vài mili-giây, ngắt hoàn toàn mạch trước khi pin kịp nóng lên!

### Giải thích: Quy trình 4 bước cấp nguồn an toàn không bao giờ bỏ qua

1. **Bước 1 — Dọn sạch mặt bàn kim loại trước khi mở công tắc:** Vụn chân linh kiện, tua-vít hay kẹp kim loại nằm dưới gầm bo mạch là nguyên nhân số 1 gây chập mạch bất ngờ.
2. **Bước 2 — Đo thông mạch `VCC–GND` khi chưa có điện:** Dùng thang đo thông mạch/Ohm của đồng hồ vạn năng; nếu kêu bíp liên tục ($$R < 5\ \Omega$$), tuyệt đối *không* cấp nguồn cho đến khi tìm ra điểm chạm!
3. **Bước 3 — Kiểm tra cực tính bằng màu dây chuẩn hóa:** Quy ước cứng Đỏ = Dương (`+`), Đen = Âm (`GND`); chỉ cần cắm ngược cực 0,5 giây là đủ phá hủy IC ổn áp không có diode bảo vệ.
4. **Bước 4 — Sờ nhanh kiểm tra nhiệt sau 5 giây đầu:** Sau khi bật nguồn, chạm nhẹ mu bàn tay gần IC ổn áp và driver động cơ; nếu nóng rát bất thường, tắt công tắc ngay lập tức!

**Kiểm tra nhanh.** Một cell pin 18650 đang đo được $$2.6\text{ V}$$ (thấp hơn ngưỡng xả sâu $$3.0\text{ V}$$). Bạn có nên cắm ngay vào bộ sạc nhanh 2 A để "cứu" pin không? **Tuyệt đối không!** Sạc dòng cao vào cell xả kiệt có thể tạo nhánh kim loại lithium (*dendrite*) gây chập ngầm bên trong và cháy nổ — cần loại bỏ an toàn hoặc chỉ phục hồi cực chậm bằng bộ sạc chuyên dụng có giám sát nhiệt.

---

## Vì sao bài này gắn liền với Capstone

Bản demo Chương 07 chỉ đáng tin cậy khi xe chạy theo lệnh và dừng ngay khi mất lệnh. Điều đó trở nên vô nghĩa nếu ngay lần cấp nguồn đầu tiên, xe lao khỏi bàn hoặc điện áp pin động cơ đi thẳng vào chân 3,3 V. Cơ chế timeout chỉ hoạt động khi vi điều khiển còn sống và đang chạy chương trình; các topic ROS 2 về sau cũng không thể cứu một chân mạch đã bị cháy.

## Ba mối nguy chính và trình tự cấp nguồn an toàn

**Năng lượng tích trữ** luôn sẵn sàng xả dòng lớn mà không báo trước, từ cổng USB, pin AA, cặp cell 18650 cho tới tụ điện trên mạch lái. Sự cố biểu hiện thành nhiệt lượng phá hủy mạch in, chân IC hoặc làm nóng phồng cell pin bị sạc sai quy cách. **Bánh xe đang quay** có thể làm giật cáp hoặc kéo khung xe rơi khỏi bàn ngay khi PWM khởi tạo sai. **Firmware quên ngắt PWM** xảy ra khi chương trình teleop bị treo sau lệnh "tiến", cửa sổ serial bị đóng đột ngột hoặc laptop chuyển sang chế độ ngủ. Quy tắc 300 ms giúp chuyển trạng thái mất lệnh thành lệnh dừng, nhưng nó không bảo vệ được khoảnh khắc trước khi chương trình bắt đầu chạy và cũng không bảo vệ chân GPIO khỏi quá áp.

Trình tự cấp nguồn an toàn chỉ gói gọn trong một trang giấy và cần thực hiện mỗi lần bật mạch, kể cả khi bạn chỉ muốn "thử nhanh":
1. **Mass chung (GND) trước:** nối chung mass của vi điều khiển, mass của mạch lái và cực âm pin thành một điểm tham chiếu chung vì dòng động cơ sẽ quay về đây. Nếu nối dây tín hiệu trước khi có mass chung, dòng điện có thể tìm đường hồi lưu qua chân GPIO và làm hỏng chip.
2. **Nguồn logic tiếp theo:** cắm USB vào vi điều khiển để tạo đường nguồn 3,3 V ổn định. Nguồn logic của mạch lái phải lấy từ đường nguồn ổn định này, không lấy từ pin động cơ.
3. **Tín hiệu điều khiển:** nối các đường PWM, chiều quay và chân standby (đảm bảo firmware đang đặt ở trạng thái dừng).
4. **Nguồn động cơ VM sau cùng:** đóng công tắc cấp VM cuối cùng, sau khi đã chắc chắn bánh xe được nhấc khỏi mặt bàn. Nhấc bánh sau khi xe đã giật chạy luôn là quá muộn.

![Nguồn lên theo mass chung, logic, tín hiệu, nguồn motor cuối, bánh khỏi mặt bàn]({{ site.imgurl }}/generated/power_order.png)

Hãy chép các bước đúng theo thứ tự trong hình. "Sau cùng" nghĩa là công tắc nguồn VM luôn đóng cuối cùng khi bánh xe đã ở trên không.

![Logic 3,3 V, USB 5 V, mass, và ray motor riêng]({{ site.imgurl }}/generated/power_rails_3v3.png)

Hãy xem sơ đồ màu dây như ranh giới cách ly: nguồn USB 5 V nuôi mạch vi điều khiển chứ không nuôi hai động cơ TT đang kẹt trục; GPIO thuộc miền logic 3,3 V; mass là điểm nối chung có chủ đích; còn đường nguồn động cơ (VM) lấy từ pin riêng và tuyệt đối không được nối vào chân GPIO hay chân 3,3 V.

## An toàn pin lithium

Một cell Li-ion 18650 có điện áp danh định khoảng 3,6–3,7 V và **đạt 4,2 V khi sạc đầy**. Bạn phải sạc **từng cell riêng lẻ** tới 4,2 V bằng bộ sạc ghi rõ dùng cho Li-ion / Li-ion 18650. Khi mắc nối tiếp hai cell trong đế 2S, điện áp danh định là 7,4 V và **đạt 8,4 V khi đầy**. Cụm nối tiếp đó dùng để cấp cho chân VM của mạch lái, không phải đầu vào của mạch sạc một cell.

Mạch sạc TP4056 được thiết kế để nạp một cell đơn lên 4,2 V. Kẹp TP4056 vào hai đầu đế 2S đồng nghĩa đặt mạch sạc 4,2 V lên bộ pin 8,4 V — đây là thao tác sai và nguy hiểm. Hãy tháo từng cell ra, sạc riêng lẻ rồi mới lắp lại vào đế.

Nếu một cell đo được khoảng 2,1 V, nó đã tụt sâu dưới ngưỡng cắt an toàn thông thường (khoảng 2,5–3,0 V). Cố sạc lại ở dòng bình thường có thể gây kết tủa kim loại bên trong và dẫn đến ngắn mạch nội. Tuyệt đối không dùng TP4056 để "kích pin", mà hãy đưa cell đó đi tái chế. Với cell bị phồng vỏ, pin đã hỏng: không sạc, không chọc thủng và không cất giữ "phòng khi cần". Không để cell 18650 trần trong túi cùng chìa khóa hay vật kim loại vì dễ gây chập cực tức thời; pin luôn phải nằm trong đế hoặc hộp bảo quản. Trong những buổi thử động cơ đầu tiên, bạn hoàn toàn có thể dùng hộp pin AA để làm quen với việc tách nguồn VM khỏi nguồn logic trước khi chuyển sang pin lithium. Chưa mua pin luôn là trạng thái an toàn hơn việc dùng bộ sạc không khớp nhãn.

## Bảo vệ chân mạch, mỏ hàn và mắt

Điện áp cực đại tuyệt đối trên chân GPIO của ESP32 **không** phải 5 V; giới hạn của pad chỉ cao hơn đường nguồn 3,3 V vài phần mười vôn, hoàn toàn không chịu được mức 5 V hay điện áp pin động cơ. Chân GPIO của Raspberry Pi Pico cũng thuộc nhóm logic 3,3 V tương tự. Vì chân echo của HC-SR04 xuất mức cao khoảng 5 V còn pin động cơ thường ở mức 7–8 V, đường echo bắt buộc phải đi qua mạch chuyển mức logic, còn pin chỉ được nối vào chân VM.

Luôn đeo kính bảo hộ khi cắt chân linh kiện và khi hàn, vì mẩu chân linh kiện cắt ra có thể bắn mạnh vào mắt. Khói nhựa thông (rosin) gây kích ứng nên cần làm việc ở nơi thông gió tốt, tránh cúi mặt trực tiếp phía trên mối hàn. Mỏ hàn đang nóng phải luôn đặt trên giá đỡ, không đặt lên dây điện hay mặt bàn. Hôm nay bạn chưa cần bật mỏ hàn, chỉ cần ghi rõ các quy tắc này ở vị trí dễ thấy nhất trên bàn làm việc.

Phần bảo vệ bằng phần mềm vẫn là quy tắc timeout đã học ở bài trước:

$$
t_{\mathrm{silence}} > 300\,\mathrm{ms} \implies \text{duty PWM} = 0.
$$

Hôm nay bạn chưa nạp đoạn mã này, nhưng cần nhớ rằng một bố trí không được coi là sẵn sàng nếu cách duy nhất để dừng robot là rút dây USB sau khi xe đã chạy khỏi thảm. Khi mất tín hiệu điều khiển, xe bắt buộc phải dừng thay vì duy trì tốc độ cũ.

## Bảng nhận diện lỗi trước khi gặp

| Tình huống thấy hoặc sắp làm | Nguyên nhân thường gặp | Cách xử lý |
| --- | --- | --- |
| Cổng serial biến mất khi nối động cơ vào chân 5 V của mạch | Cổng USB không cấp nổi dòng khi hai động cơ kẹt; đường 3,3 V sụp áp | Tách động cơ sang nguồn VM riêng, giữ mass chung, chỉ dùng USB cho phần logic |
| Chân GPIO hỏng sau khi nối trực tiếp echo siêu âm | Đưa mức 5 V vào chân không chịu được 5 V | Dừng ngay; chân có thể đã hỏng; lắp mạch chuyển mức cho đường echo trước khi thử lại |
| Mạch TP4056 kẹp lên hai đầu đế pin 2S | Đặt mạch sạc 4,2 V lên bộ pin 8,4 V | Ngắt kết nối ngay; tháo từng cell ra sạc riêng ngoài robot |
| Cell 18650 đo khoảng 2,1 V hoặc vỏ bị phồng | Pin xả quá sâu hoặc đã hư hại bên trong | Không sạc, không bỏ túi; đưa đi tái chế |
| Để bánh chạm bàn khi nạp firmware mới "thử một chút" | Chuyển động ngoài ý muốn vì PWM có thể khác 0 trước khi vào vòng lặp | Nhấc bánh khỏi bàn trước; cấp VM sau cùng; vẫn giữ timeout trong mã nguồn |
| Đặt mỏ hàn đè lên dây hoặc cắt chân linh kiện không đeo kính | Gây bỏng, chảy vỏ dây hoặc mẩu chân linh kiện bắn vào mắt | Dùng giá đỡ, đeo kính bảo hộ, đảm bảo thông gió; rút điện nếu bố trí chưa đạt |

## Thực hành: viết thẻ cấp nguồn và kiểm tra chỉ bằng USB

Thực hiện bài lab này khi **không gắn động cơ vào mạch**. Nếu chưa có mạch vi điều khiển, bạn vẫn viết thẻ quy trình và ghi `chưa có board` vào vị trí tên cổng serial.

Lấy một tờ giấy rời, đặt tiêu đề `LÊN NGUỒN` và ghi bốn bước theo đúng thứ tự: (1) Mass chung (GND), (2) Nguồn logic từ USB, (3) Tín hiệu PWM và chiều quay ở trạng thái dừng, (4) Nguồn động cơ VM cuối cùng. Phía dưới ghi thêm bốn dòng cảnh báo: `NHẤC BÁNH TRƯỚC KHI CẤP VM`, `MẤT LỆNH > 300 ms → PWM = 0`, `CẤM: đưa nguồn pin hoặc echo 5 V vào GPIO 3,3 V`, và `18650: sạc từng cell tới 4,2 V, không kẹp TP4056 qua đế 2S`. Dán tờ giấy này ngay trước khu vực làm việc hoặc đặt cạnh bàn phím.

Sau đó, thực hiện kiểm tra cấp nguồn chỉ bằng USB theo đúng trình tự:
1. Kiểm tra mặt bàn để chắc chắn không có động cơ, không có pin động cơ và không có dây VM. Ngắt hoàn toàn pin trước khi cắm USB; nếu đã có bánh xe, không để chúng nối với mạch lái đang cấp điện.
2. Chỉ cắm vi điều khiển vào máy tính bằng cáp USB truyền dữ liệu. Kiểm tra xem cổng serial mới (hoặc ổ đĩa BOOTSEL nếu dùng Pico) có xuất hiện không.
3. Dán tên cổng vào sổ lab; nếu chưa có mạch, ghi `không có — chưa có board` kèm kế hoạch: "khi có mạch sẽ chỉ cắm USB, không nối VM, ghi lại tên cổng rồi rút ra". Sau khi kiểm tra xong thì rút cáp, không vội gắn động cơ.

Nếu bạn đã có sẵn cell lithium, hãy chụp ảnh nhãn bộ sạc và ghi lại chính xác thông số hóa học pin trên nhãn; nếu bộ sạc mất nhãn thì ghi `sẽ không sạc`. Nếu chưa có pin, ghi `chưa mua cell`. Nếu đã có mỏ hàn, hãy kiểm tra chắc chắn đã có giá đỡ trước khi nghĩ đến việc cắm điện, đồng thời ghi chú kính bảo hộ đang có sẵn hay còn thiếu.

**Kết quả cần đạt:** Thẻ quy trình đặt ở chỗ nhìn thấy ngay mà không cần mở lại bài học. Sổ lab có ảnh chụp hoặc bản phác thẻ, có tên cổng serial thực tế (hoặc kế hoạch cụ thể), và có trạng thái sạc pin rõ ràng (`khớp`, `sẽ không sạc` hoặc `chưa mua cell`). Toàn bộ bước USB không có sự xuất hiện của động cơ.

**Cách xử lý khi lệch chuẩn:** Nếu trên thẻ có mục cấp VM trước, hãy viết lại ngay. Luôn nhấc bánh cho mọi lần thử firmware mới đầu tiên. Mọi hướng dẫn lấy nguồn chân 5 V của DevKit để chạy động cơ đều xếp vào mục cấm. Nếu bộ sạc đang kẹp vào đế 2S chỉ vì vừa giắc, hãy tháo ra ngay và sạc từng cell riêng lẻ.

## Ví dụ làm sẵn

Một sinh viên định để bánh xe chạm mặt bàn "chỉ để thử nhanh đoạn mã mới". Tuy nhiên, PWM chưa được kiểm chứng là khởi tạo ở mức 0, và bộ đếm timeout 300 ms chưa hoạt động trước khi hàm khởi tạo chạy xong. Cách làm đúng là giữ bánh nhấc khỏi bàn, ngắt nguồn VM, chỉ cấp nguồn logic qua USB trước, rồi mới chạy thử lần đầu ở trạng thái bánh trên không để tránh việc xe giật rơi khỏi bàn.

Trong cùng buổi chiều, một viên 18650 đo được 2,1 V và có người định dùng TP4056 để "hồi sức". Vì cell đã tụt sâu dưới ngưỡng an toàn, sổ lab ghi rõ không sạc, không bỏ túi và không kẹp lên đế 2S; chỉ những cell còn tốt mới được sạc riêng lẻ đến 4,2 V rồi mới lắp vào đế.

Cũng trên bàn đó, sợi dây echo từ HC-SR04 suýt được cắm thẳng vào chân GPIO của ESP32. Do giới hạn cực đại tuyệt đối của pad không phải 5 V, dây này phải chờ lắp mạch chuyển mức logic — cùng nguyên tắc cấm như đối với điện áp pin động cơ.

## Video tham khảo

- **Xem trước:** [What is ESD and How to Prevent it – ATM | Digi-Key Electronics](https://www.youtube.com/watch?v=pWhtyz-UFZc) — DigiKey, tiếng Anh. Giải thích về phóng tĩnh điện (ESD) và lý do chạm tay vào linh kiện khi chưa xả tĩnh điện có thể làm hỏng mạch trước khi robot kịp chạy.
- [What is a fuse? the basics explained](https://www.youtube.com/watch?v=W770Z1yvXs8) — The Engineering Mindset, tiếng Anh. Giải thích vai trò của cầu chì trên đường nguồn, đặt song song với quy tắc ngắt nguồn an toàn trong bài.

## Bài tập

Các câu hỏi dưới đây là tình huống thực tế; hãy nêu hành động xử lý cụ thể thay vì chép lại định nghĩa.

1. Một bạn đặt khung xe trên bàn, bánh vẫn chạm mặt bàn và muốn nạp firmware "chỉ một giây". Những điều kiện nào phải đảm bảo trước khi đóng nguồn VM, và vì sao quy tắc dừng 300 ms không đủ bảo vệ cho lần nạp đầu tiên?
2. Một cell 18650 đo được 2,1 V và có người đưa mạch TP4056 cho bạn. Bạn phải làm gì với cell đó và từ chối làm gì với đế pin 2S?
3. Dây echo của HC-SR04 sắp được cắm thẳng vào chân GPIO ESP32. Điện áp của dây này ở mức cao là bao nhiêu, và vì sao nhận xét "ESP32 chịu tốt" không phải là thông số kỹ thuật?
4. Bạn phát hiện mạch TP4056 đang kẹp vào đế chứa hai cell 18650 mắc nối tiếp (dùng cho nguồn VM sau này). Bạn cần ngắt bộ phận nào ngay lập tức, và nếu các cell còn tốt thì quy trình sạc đúng là gì?
5. Robot đang chạy teleop thì laptop chuyển sang chế độ ngủ, trong khi firmware chưa có bộ đếm thời gian mất lệnh. Bánh xe sẽ phản ứng thế nào, và điều kiện gán nào bắt buộc phải có trong vòng lặp điều khiển?

<details>
<summary>Gợi ý đáp án</summary>

1. Phải nhấc bánh khỏi mặt bàn, nối xong mass chung, nguồn logic rồi tín hiệu, và giữ VM hở cho tới khi chắc chắn bánh đang trên không. Quy tắc timeout chỉ chạy sau khi firmware đã khởi động và vào vòng lặp; trong lúc nạp hoặc reset, trạng thái chân có thể thay đổi bất ngờ khiến bánh kéo cả mạch rơi khỏi bàn.
2. Không sạc lại cell này, không cất trong túi, không kẹp TP4056 vào cell hay vào đế 2S; mang cell đi tái chế đúng quy định.
3. Chân echo ở mức cao khoảng 5 V, trong khi giới hạn cực đại tuyệt đối của GPIO ESP32 không phải 5 V. Dây này bắt buộc qua mạch chuyển mức; nối thẳng có thể làm hỏng chân vi điều khiển.
4. Ngắt TP4056 khỏi đế 2S ngay lập tức. Tháo từng cell lành ra sạc riêng lẻ tới 4,2 V ngoài robot, sau đó mới lắp vào đế 2S để cấp nguồn VM.
5. Bánh xe sẽ giữ nguyên lệnh chạy cuối cùng. Vòng lặp firmware bắt buộc phải đưa duty PWM về 0 khi khoảng thời gian mất lệnh vượt quá khoảng 300 ms.

</details>

Trước khi bước vào lắp khung ở Chương 07, bạn sẽ học tiếp bài [Pin, nguồn và an toàn trước khi lắp Capstone]({% multilang_post_url contents/chapter07/07_00_batteries_power_safety %}) để phân biệt chi tiết Li-ion 18650, LiPo và LiFePO4, tính chọn cầu chì và vẽ sơ đồ mạch hạ áp (buck). Thẻ một trang của buổi hôm nay vẫn là nguyên tắc bắt buộc, còn bài ở Chương 07 sẽ cụ thể hóa thành sơ đồ dây.

## Đọc thêm

- [Mức logic, SparkFun](https://learn.sparkfun.com/tutorials/logic-levels) — giải thích vì sao mức 5 V và 3,3 V không thể thay thế trực tiếp cho nhau, chính là bài toán của chân echo.
- [Battery University, BU-409, sạc lithium-ion](https://batteryuniversity.com/article/bu-409-charging-lithium-ion) — trình bày nguyên lý ngưỡng đầy 4,2 V và lý do pin Li-ion cần quy trình sạc chuyên biệt.

## Mua ở Việt Nam

Danh sách mua sắm đầy đủ cho robot nằm ở [bài 00-05]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %}). Các mức giá dưới đây được ghi nhận từ Hshop ngày **23 tháng 9 năm 2026**. Bạn chỉ cần mua một đồng hồ vạn năng: [UNI-T UT33D+](https://hshop.vn/dong-ho-van-nang-dien-tu-digital-multimeter-uni-t-ut33d-chinh-hang) giá 285.000 ₫ hoặc [Wadfow WDM1501](https://hshop.vn/dong-ho-van-nang-ky-thuat-so-vom-wadfow-wdm1501-digital-multimeter-true-rms) giá 185.000 ₫. Mỏ hàn và giá đỡ phải đi thành một cặp: [Wadfow 60 W](https://hshop.vn/mo-han-60w-wadfow-wel3616-soldering-iron) giá 75.000 ₫ và [giá đỡ tròn](https://hshop.vn/de-gac-mo-han-tron-b-2-co-khay-roi) giá 40.000 ₫ — mua mỏ hàn mà thiếu giá đỡ là vi phạm đúng quy tắc an toàn vừa học. Thiếc hàn, kìm cắt và breadboard được liệt kê ở bài 00-04.

Với kính bảo hộ và bộ sạc một cell, bạn có thể tra cứu qua các trang tìm kiếm sau: [Shopee, kính bảo hộ](https://shopee.vn/search?keyword=k%C3%ADnh%20b%E1%BA%A3o%20h%E1%BB%99), [Lazada, kính bảo hộ](https://www.lazada.vn/catalog/?q=k%C3%ADnh%20b%E1%BA%A3o%20h%E1%BB%99), [Shopee, sạc pin 18650](https://shopee.vn/search?keyword=s%E1%BA%A1c%20pin%2018650) và [Lazada, sạc pin 18650](https://www.lazada.vn/catalog/?q=s%E1%BA%A1c%20pin%2018650). Vì đây là các trang tìm kiếm chung, hãy đọc kỹ nhãn sản phẩm và chỉ chọn bộ sạc hỗ trợ nạp riêng từng cell Li-ion tới 4,2 V. Bạn cũng có thể tham khảo trang chủ của [Thế Giới IC](https://www.thegioiic.com/) và [IC Đây Rồi](https://icdayroi.com/) khi tìm linh kiện. Đừng mua LiDAR trong giai đoạn này.
