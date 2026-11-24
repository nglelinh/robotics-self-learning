---
layout: post
title: "Chào mừng, kết quả học và cách học"
chapter: "00"
order: 1
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter00
lesson_type: required
draft: false
---

Hãy dành khoảng 90 phút cho bài học này. Bạn chỉ cần một trình soạn thảo văn bản và một cuốn lịch; hiện tại chưa cần robot hay hệ điều hành Ubuntu. Mục tiêu của bài là giúp bạn lập một lộ trình học tập cụ thể và đủ rõ ràng để sử dụng xuyên suốt cho đến khi khung xe robot lăn bánh.

## Mục tiêu học

Sau bài học này, bạn sẽ **trình bày** được cấu trúc cốt lõi của khóa học, từ bước nhận diện linh kiện, vượt qua mốc điều khiển từ xa (teleop) ở Chương 07, cho đến việc đọc hiểu các tài liệu về học máy cho robot (robot learning) về sau. Bạn sẽ **tính toán** được nhịp học 4–6 giờ mỗi tuần trong 12–16 tuần và phân bổ các mốc chương lên lịch cá nhân. Bạn cũng sẽ **tạo** sổ lab gồm sáu trường thông tin bắt buộc: ngày, ảnh chụp, sơ đồ dây, đoạn log serial, lỗi gặp phải và cách khắc phục; đồng thời **phân biệt** được ghi chép có bằng chứng với nhận xét cảm tính dựa trên việc có kèm log serial và mô tả lỗi hay không. Cuối cùng, bạn sẽ biết cách **tìm** bản tiếng Việt hoặc tiếng Anh của cùng một bài học theo `chapter` và `order`, và chủ động **hoãn** việc mua LiDAR, dùng Nav2 hay cài đặt ROS 2 đầy đủ cho tới khi xe vi sai biết tự dừng khi mất lệnh điều khiển.

## Cần có trước

Bạn chỉ cần đọc hiểu được tài liệu kỹ thuật ở tốc độ chậm và biết tạo thư mục trên máy tính. Lúc này bạn chưa cần đồng hồ vạn năng, mỏ hàn hay kiến thức nền về robot. Định luật Ohm sẽ được học ở Chương 01 thông qua thực hành đo đạc thay vì học thuộc lòng. Thói quen quan trọng nhất cần rèn ngay từ đầu là ghi chép trung thực những gì gặp lỗi; một dòng nhật ký chung chung như "bắt đầu khóa học" sẽ không giúp ích gì khi bạn cần gỡ lỗi ở tuần thứ chín.

---

Hãy tưởng tượng khoảnh khắc đầu tiên chiếc xe robot hai bánh bạn tự tay lắp ráp chạy thẳng đúng một mét, dừng êm ái trước vật cản rồi quay góc $$90^\circ$$ mà không cần bạn chạm vào bàn phím. Đằng sau khoảnh khắc kỳ diệu ấy không phải là phép màu lập trình, mà là sự phối hợp nhịp nhàng giữa **điện tử cơ bản**, **vi điều khiển thời gian thực**, **toán học động học–điều khiển** và **kỷ luật kiểm thử phần cứng**. Bài mở đầu này đặt ra bản đồ tư duy để bạn bước từ bàn học lý thuyết sang bàn lab cơ điện tử một cách chắc chắn nhất.

## Bản đồ kiến thức nền: Kỹ thuật Robot (Robotics) là gì và nghiên cứu những gì?

Với sinh viên đại học, robot học là giao điểm thực chiến của ba trụ cột kỹ thuật cốt lõi:

1. **Vòng lặp Cảm nhận – Lập kế hoạch – Hành động (Sense–Plan–Act):** Mọi robot tự hành đều lặp đi lặp lại một chu trình kín ở tần số cố định: cảm biến đo thế giới thực (*Sense*) → thuật toán ước lượng trạng thái và tính lệnh điều khiển (*Plan*) → động cơ thực thi lực/mô-men (*Act*).
2. **Sự ràng buộc của Vật lý và Thời gian thực (Real-Time Constraints):** Khác với phần mềm web có thể chờ 200 ms không sao, một robot tự cân bằng hay xe chạy $$1\text{ m/s}$$ bị trễ 200 ms đã lao thẳng vào tường (đi thêm $$20\text{ cm}$$ mất kiểm soát!).
3. **Kỹ thuật kiểm chứng theo tầng (Incremental Bring-Up):** Không bao giờ lắp hết mạch rồi mới cắm pin; kỹ sư robot kiểm chứng từng tầng độc lập — Nguồn → Vi điều khiển → Cảm biến → Động cơ → Điều khiển vòng kín.

### Ví dụ cầm tay chỉ việc: Tính ngân sách thời gian cho vòng lặp điều khiển $$50\text{ Hz}$$

Giả sử xe robot của bạn chạy vòng lặp điều khiển chính ở tần số $$f = 50\text{ Hz}$$. Khi đó mỗi chu kỳ điều khiển chỉ có đúng:

$$
T = \frac{1}{f} = \frac{1}{50\text{ s}^{-1}} = \mathbf{20\text{ ms}}.
$$

Ta cộng tay thời gian thực thi của 3 khối trong một chu kỳ trên ESP32:
- **Cảm nhận (Sense):** đọc 2 bộ mã hóa vòng quay (encoder) + cảm biến IMU qua I2C mất **$$2.5\text{ ms}$$**.
- **Lập kế hoạch (Plan):** tính vận tốc góc, chạy bộ điều khiển PID và cập nhật trạng thái mất **$$0.8\text{ ms}$$**.
- **Hành động (Act):** cập nhật độ rộng xung PWM cho 2 động cơ + ghi log nhẹ mất **$$0.7\text{ ms}$$**.

Tổng thời gian tính toán là $$2.5 + 0.8 + 0.7 = \mathbf{4.0\text{ ms}} \ll 20\text{ ms}$$ (chỉ chiếm $$20\%$$ CPU, còn $$16\text{ ms}$$ dự phòng!). Nhưng nếu bạn lỡ viết một lệnh `delay(50)` để chờ cảm biến siêu âm, chu kỳ lập tức vọt lên $$54\text{ ms}$$ (tần số tụt xuống $$18.5\text{ Hz}$$) và bộ điều khiển PID lập tức bị dao động!

### Khung giải thích: Bốn nguyên tắc vàng để tự học Robotics không bỏ cuộc giữa chừng (nên đọc chậm)

1. **Bước 1 — Tách biệt lỗi phần cứng với lỗi phần mềm:** Trước khi sửa 100 dòng code, luôn đo điện áp đường nguồn bằng đồng hồ vạn năng — hơn một nửa "lỗi code" ở người mới thực chất là dây cắm lỏng hoặc sụt áp pin.
2. **Bước 2 — Ghi sổ lab bằng con số đo được:** Đừng ghi *"xe chạy tạm ổn"*; hãy ghi *"Pin 7.82 V, sai số quãng đường 1.00 m là +1.8 cm, dòng không tải 210 mA"*.
3. **Bước 3 — Luôn có trạng thái an toàn mặc định:** Mọi firmware phải khởi động với động cơ tắt (PWM = 0) và có nút hoặc lệnh dừng khẩn cấp.
4. **Bước 4 — Đi từ mô hình nhỏ kiểm chứng được bằng tay:** Hiểu rõ xe vi sai 2 bánh trên bàn làm việc giúp bạn mở rộng mượt mà lên robot tự hành chạy ROS 2 trong công nghiệp.

**Kiểm tra nhanh.** Nếu xe robot chạy với vận tốc $$v = 0.8\text{ m/s}$$ và vòng lặp điều khiển chạy ở $$f = 20\text{ Hz}$$ ($$T = 50\text{ ms}$$), giữa hai lần cập nhật lệnh xe đi được bao xa? Đúng $$0.8 \times 0.05 = \mathbf{0.04\text{ m} = 4\text{ cm}}$$ — đó là lý do xe chạy càng nhanh thì tần số vòng lặp phải càng cao!

---

## Vì sao bài này gắn liền với Capstone

Chương 07 là mốc **Capstone A**: một xe dẫn động vi sai gồm hai bánh chủ động và một bánh đa hướng (caster), được bạn điều khiển thủ công khi bánh xe đang nhấc khỏi mặt bàn. Điều khiển từ xa (teleop) nghĩa là bạn trực tiếp gửi lệnh lái chứ chưa để robot tự tìm đường. Quy tắc an toàn cốt lõi là nếu không có lệnh mới trong hơn 300 ms, chu kỳ xung (duty PWM) phải tự động đưa về 0. ROS 2 Jazzy chỉ xuất hiện sau khi bạn vượt qua bài kiểm tra này. Về bản chất, một topic trong ROS 2 chỉ là một kênh truyền thông điệp có tên nằm phía trên phần cứng mà bạn đã kiểm chứng, chứ bản thân topic không tạo ra mô-men xoắn. Gazebo Harmonic và micro-ROS cũng tuân theo nguyên tắc đó ở tầng mô phỏng và vi điều khiển. Nếu ngay từ bây giờ bạn chưa nắm rõ quy tắc dừng 300 ms, mọi việc cài đặt phần mềm về sau rất dễ trở thành cách né tránh thực hành trên bàn lab.

## Lộ trình cốt lõi của khóa học

Khóa học được thiết kế theo một tuyến thống nhất, với một số chương mở rộng tùy chọn ở giai đoạn cuối.

Bạn sẽ bắt đầu bằng kỹ năng nhận diện phần cứng cơ bản: cấu trúc hàng lỗ trên breadboard, mạch lái động cơ (driver), phân biệt cáp USB chỉ sạc với cáp truyền dữ liệu, và kiểm tra sự tương thích giữa cell pin với bộ sạc. Chương 00 xây dựng thói quen làm việc an toàn trên bàn lab, còn Chương 01 chuyển các khái niệm điện áp, dòng điện và điện trở thành những con số đo đạc thực tế.

Tiếp theo là phần firmware trên ESP32 hoặc Raspberry Pi Pico. Chương 02 hướng dẫn nạp chương trình vào vi điều khiển, còn Chương 03 đưa bạn vào cấu trúc mã nguồn đặc trưng cho robot: chân GPIO, định thời và điều chế độ rộng xung (PWM). PWM là kỹ thuật giữ một chân ở mức logic cao trong một tỷ lệ nhất định của mỗi chu kỳ ngắn, từ đó mạch lái động cơ chuyển đổi thành mức công suất cấp cho động cơ.

Từ Chương 04 đến Chương 06, bạn bổ sung cảm biến, mạch lái động cơ và lắp ráp cơ khí cho hệ hai bánh chủ động. Chương 07 là bài nghiệm thu Capstone A: bạn gửi lệnh tiến, xoay hoặc dừng qua cổng serial USB (hoặc qua một trang Wi-Fi đơn giản nếu dùng ESP32) trong trạng thái bánh xe nhấc khỏi mặt bàn. Một bộ đếm thời gian sẽ lưu lại thời điểm nhận lệnh hợp lệ gần nhất. Gọi $t_{\mathrm{last}}$ là mốc thời gian đó và $t_{\mathrm{now}}$ là thời điểm hiện tại trong vòng lặp điều khiển. Khoảng thời gian mất lệnh được tính là:

$$
t_{\mathrm{silence}} = t_{\mathrm{now}} - t_{\mathrm{last}}.
$$

Quy tắc dừng an toàn của khóa học là:

$$
t_{\mathrm{silence}} > 300\,\mathrm{ms} \implies \text{duty PWM} = 0.
$$

Dấu lớn hơn ở đây là bất đẳng thức chặt: lệnh đến đúng mốc 300 ms vẫn được coi là hợp lệ. Hôm nay bạn chưa cần lập trình vòng lặp này, nhưng cần hiểu ý nghĩa vật lý của nó. Ở tốc độ chậm $0{,}3\,\mathrm{m/s}$, robot vẫn có thể trôi thêm khoảng 9 cm trong khoảng thời gian chờ đó:

$$
s \approx 0{,}3\,\mathrm{m/s} \times 0{,}3\,\mathrm{s} = 0{,}09\,\mathrm{m}.
$$

Quãng đường 9 cm là đủ để làm giật đứt cáp USB hoặc kéo xe rơi khỏi bàn, vì vậy bài nghiệm thu bắt buộc phải nhấc bánh lên.

Chỉ khi bản demo teleop hoạt động ổn định và lặp lại được, bạn mới chuyển sang tầng truyền thông. Chương 08 xây dựng giao tiếp và vòng điều khiển đơn giản trên phần cứng đã vận hành. Chương 09 cài đặt ROS 2 Jazzy (chỉ hỗ trợ trên Ubuntu 24.04); lúc này, một topic vận tốc thực sự có ý nghĩa vì bạn đã nắm rõ firmware phản ứng thế nào khi luồng tin nhắn bị ngắt. Chương 10 giới thiệu Gazebo Harmonic (bộ mô phỏng đi kèm Jazzy) và micro-ROS (giải pháp giúp vi điều khiển giao tiếp trực tiếp với ROS 2). Bạn chỉ nên triển khai micro-ROS sau khi vi điều khiển đã lái được khung xe độc lập, bởi nếu không, một topic im lặng và một động cơ mất điện sẽ gây ra triệu chứng giống hệt nhau.

Chương 11 và 12 là hai chương tùy chọn, đòi hỏi đọc tài liệu một cách tỉnh táo. LeRobot là thư viện của Hugging Face dành cho tập dữ liệu robot và các chính sách điều khiển (policy) học từ dữ liệu. ACT dự đoán một chuỗi hành động ngắn phía trước, diffusion policy sinh hành động bằng quá trình khử nhiễu từng bước, còn VLA ánh xạ trực tiếp hình ảnh và câu lệnh thành hành động. Không mô hình nào trong số này thay thế được một mạch lái động cơ biết ngắt PWM an toàn. Khi đọc các tài liệu này, hãy chú ý vào giả thuyết, dữ liệu thực nghiệm và giới hạn của chúng; một kho mã nguồn không thể tự biến khung xe đầu tiên của bạn thành nền tảng nghiên cứu.

Nhiều video hướng dẫn thường đặt các công cụ phức tạp ở bước đầu tiên, nhưng khóa học này chủ động hoãn chúng lại: chưa dùng LiDAR, chưa dùng Nav2 và chưa cài ROS 2 trong tuần này (trừ khi bạn chỉ đọc trước trang hướng dẫn trên máy đã cài sẵn Ubuntu 24.04). Thực hành trên bàn lab luôn được ưu tiên. Một chiếc xe lăn được vài giây chưa phải là robot tự hành, và điện áp pin động cơ tuyệt đối không được nối vào chân 3,3 V.

## Nhịp học: 4–6 giờ mỗi tuần trong 12–16 tuần

Khối lượng học tập thiết kế là **4–6 giờ mỗi tuần** trong khoảng **12–16 tuần**. Với 14 tuần và 5 giờ mỗi tuần, tổng thời gian là:

$$
5 \times 14 = 70
$$

giờ. Tương tự, 12 tuần với 6 giờ/tuần đạt 72 giờ, còn 16 tuần với 4 giờ/tuần đạt 64 giờ. Quỹ thời gian này đủ để hoàn thành từ Chương 00 đến Chương 10, miễn là mỗi tuần bạn đều có ít nhất một buổi thực hành trên bàn lab (hoặc chuẩn bị quy trình trên giấy trước khi linh kiện về). Một tuần 5 giờ có thể chia hợp lý thành khoảng 90 phút đọc tài liệu, 120 phút thực hành và 90 phút hoàn thiện ghi chép. Dồn 12 giờ vào một ngày Chủ nhật rồi bỏ trống ba tuần liền chỉ khiến bạn quên mất sơ đồ dây và trạng thái lỗi của chính mình.

Bảng dưới đây gắn các mốc chương với bằng chứng đầu ra tương ứng:

| Tuần | Chương | Bằng chứng bạn cần hoàn thành |
|-----:|--------|-------------------------------|
| 1–3 | 00 và 01 | Thẻ quy trình cấp nguồn, tiếng bíp thông mạch của đồng hồ trên mối nối đã biết, và mục sổ lab ghi số đo điện áp hoặc trạng thái "không có" trung thực |
| 4–6 | 02 và 03 | Firmware chạy trên ESP32 hoặc Pico kèm đoạn log serial dán vào sổ lab |
| 7–11 | 04 tới 07 | Demo teleop nhấc bánh; duty PWM tự động về 0 khi mất lệnh quá khoảng 300 ms |
| 12–14 | 08 tới 10 | Một topic ROS 2 trên Ubuntu 24.04 điều khiển chuyển động đã kiểm chứng; ghi nhận rõ vai trò của Gazebo Harmonic và micro-ROS trong sổ lab |
| Sau, tùy chọn | 11 và 12 | Ghi chú đọc hiểu về LeRobot, ACT, diffusion policy hoặc VLA, phân biệt rõ phần nào đo được trên robot của bạn và phần nào không |

Nếu bận đột xuất trong một tuần, hãy lùi các mốc kế tiếp lại thay vì cắt bỏ bài kiểm tra nhấc bánh để chạy theo ROS 2 Jazzy.

## Sổ lab

Hãy duy trì một tệp duy nhất là `notes/lab-notes.md`. Mỗi mục ghi chép cần đủ sáu trường thông tin:
- **Ngày:** thời điểm thực hiện buổi lab.
- **Ảnh:** tên tệp ảnh chụp bàn làm việc hoặc mạch; ghi `không có` nếu chưa có vật thể để chụp.
- **Sơ đồ dây:** ảnh chụp bản vẽ tay bằng bút chì; nếu chưa lắp mạch thì ghi `chưa có mạch`.
- **Đoạn serial:** nội dung sao chép trực tiếp từ Serial Monitor, shell Thonny, hoặc lệnh echo của ROS 2 về sau; nếu chưa có mạch thì ghi `không có — chưa có board`.
- **Cái gì hỏng:** mô tả triệu chứng đo được cụ thể (ví dụ: cổng serial bị ngắt khi cấp nguồn hai động cơ từ chân 5 V USB), tránh ghi chung chung kiểu "động cơ hỏng".
- **Cái gì sửa được:** nêu rõ thao tác thay đổi đã thực hiện (kể cả ghi chú như "chưa cấp nguồn; đã viết xong quy tắc dừng 300 ms trước khi đặt mua linh kiện").

Để trống bất kỳ trường nào đều làm giảm giá trị tra cứu của sổ lab thành ghi chú cảm tính.

Trang web khóa học hỗ trợ song ngữ Việt – Anh. Nút chuyển ngôn ngữ ánh xạ bài học theo **chapter** và **order**, không theo tiêu đề. Bài này thuộc `chapter: "00"`, `order: 1`, và bản tiếng Anh tương ứng cũng dùng đúng cặp giá trị đó. Khi gặp một đoạn khó hiểu, bạn có thể chuyển ngôn ngữ để đối chiếu trực tiếp. Các thuật ngữ kỹ thuật như GPIO, PWM, breadboard, Capstone và ROS 2 được giữ thống nhất ở cả hai ngôn ngữ.

## Hình minh họa

![Các họ linh kiện và dụng cụ mà khóa sẽ yêu cầu bạn nhận ra]({{ site.imgurl }}/generated/kit_catalog_overview.png)

Hình trên minh họa các nhóm linh kiện và dụng cụ sẽ xuất hiện trong khóa học, không phải giỏ hàng mua sắm. Danh sách vật tư cụ thể nằm ở bài 00-05; mua sắm theo hình minh họa rất dễ dẫn đến việc mua LiDAR trước khi có đồng hồ vạn năng.

![Hai lộ trình học dùng chung một robot]({{ site.imgurl }}/generated/tracks_mcu_ros.png)

Lộ trình A hoàn thành nghiệm thu Capstone A thuần bằng firmware vi điều khiển mà không cần Ubuntu. Lộ trình B sử dụng đúng khung xe đó, sau đó bổ sung tầng phần mềm gồm Ubuntu 24.04, ROS 2 Jazzy, Gazebo Harmonic và micro-ROS khi phần cứng đã chạy ổn định. Cả hai lộ trình đều dùng chung một bài nghiệm thu, và LiDAR chỉ nên cân nhắc sau khi bài kiểm tra đó đạt độ tin cậy.

## Thực hành: mở sổ lab và lập lịch 14 tuần

Tạo thư mục khóa học cùng tệp `notes/lab-notes.md` và điền đủ sáu trường dưới ngày hôm nay. Ở trường sơ đồ dây, hãy viết rõ phát biểu Capstone A: xe hai bánh chủ động, nhấc bánh khỏi bàn, điều khiển qua serial hoặc trang Wi-Fi đơn giản, đưa duty PWM về 0 nếu mất lệnh quá 300 ms. Ở trường đoạn serial, ghi `không có — chưa có board` nếu chưa có cổng kết nối thực tế; tuyệt đối không tự bịa log.

Tiếp theo, đặt ba khung giờ cố định trong bảy ngày tới với tổng thời lượng 4–6 giờ: Đọc tài liệu, Thực hành bàn lab và Ghi chú. Khi linh kiện chưa về, buổi thực hành có thể dành cho việc viết thẻ quy trình cấp nguồn. Chép bảng mốc chương vào sổ và điền tuần lịch thực tế tương ứng với các giai đoạn 1–3, 4–6, 7–11 và 12–14. Nếu có tuần bận, hãy dịch chuyển mốc lùi lại chứ không bỏ qua Chương 07. Có ba món bạn chưa nên mua trong tháng này: LiDAR, máy tính mua riêng chỉ để học ROS, và bộ sạc chưa đọc rõ nhãn thông số. Danh sách mua sắm chính thức nằm tại [bài 00-05]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %}).

**Kết quả cần đạt:** Người đọc khác có thể tìm thấy đủ sáu trường thông tin trong vòng một phút, thấy rõ con số 300 ms trong phát biểu mục tiêu, và thấy các khung giờ lặp lại trên lịch của bạn.

**Cách xử lý khi lệch chuẩn:** Nếu một trường chưa có dữ liệu, hãy điền `không có` thay vì bỏ trống. Nếu bạn đang dồn 6 giờ vào riêng ngày Chủ nhật, hãy tách nhỏ ra nhiều buổi trong tuần. Các trang tài liệu về Nav2 nên được đánh dấu "đọc sau Chương 07", còn việc chọn pin lithium rời hãy chờ đến bài 00-05 để khớp đúng loại sạc với hóa học của cell pin.

## Ví dụ làm sẵn

Hà bắt đầu học vào tối thứ Tư bằng laptop Windows và chưa có linh kiện. Kế hoạch 6 giờ mỗi tuần trong 12 tuần cho tổng $6 \times 12 = 72$ giờ, nhưng đến tuần 8 cô phải đi công tác nên Chương 07 rơi đúng vào tuần không có mặt ở nhà. Cô điều chỉnh sang kế hoạch 5 giờ mỗi tuần trong 14 tuần (tổng 70 giờ), vẫn đủ hoàn thành Chương 00–10 nếu duy trì đều buổi thực hành. Cô ghi rõ các mốc: tuần 1–3 học Chương 00–01, tuần 4–6 học Chương 02–03, tuần 7–11 học Chương 04–07, tuần 12–14 học Chương 08–10, còn Chương 11–12 để tùy chọn sau khi robot đã biết tự dừng khi mất lệnh.

Trong cùng mục sổ lab, Hà chép lại quy tắc 300 ms. Trường serial ghi `không có — chưa có board`, ảnh ghi `không có`, lỗi ghi `chưa cấp nguồn`, và cách khắc phục ghi `đã chốt lịch theo từng tuần trước khi mở trang mua sắm`. Khung giờ 20:00–21:30 tối thứ Năm được đặt làm buổi thực hành với tiêu đề "viết thẻ an toàn, chưa hàn". Ghi chép như vậy là đạt yêu cầu.

## Video tham khảo

- **Xem trước:** [What Is ROS2? - Framework Overview](https://www.youtube.com/watch?v=7TVWlADXwRw) — Raymond Andrade, tiếng Anh. Giới thiệu tổng quan kiến trúc ROS 2 sẽ dùng ở nửa sau khóa học: node, topic và mô hình chạy nhiều tiến trình.
- [Raspberry Pi VS Arduino VS ESP32](https://www.youtube.com/watch?v=oJs0cVYuQTw) — TechteamGB, tiếng Anh. So sánh ba dòng mạch phổ biến trên lộ trình để bạn chọn một vi điều khiển phù hợp cho giai đoạn đầu thay vì mua dàn trải.
- [Cơ điện tử học làm robot](https://www.facebook.com/reel/1746806056360278) — Facebook Reel của Hoàng Quân (Cơ điện tử ICTU, [chinbi.com](https://chinbi.com)). Góc nhìn thực tế về quá trình sinh viên cơ điện tử tự làm robot từ bàn lab đến khi xe vận hành được.

## Bài tập

1. Viết phát biểu Capstone A của riêng bạn, trong đó có đủ các yếu tố: hai bánh chủ động, bánh nhấc khỏi bàn, điều khiển qua serial hoặc Wi-Fi đơn giản, và tắt PWM khi mất lệnh quá khoảng 300 ms. Ghi kèm khoảng tuần dự kiến bạn có thể quay video nghiệm thu demo này.
2. So sánh hai kế hoạch học: Kế hoạch P là 4 giờ/tuần trong 16 tuần; Kế hoạch Q là 6 giờ/tuần trong 12 tuần. Tính tổng số giờ của mỗi kế hoạch và cho biết kế hoạch nào vẫn giữ được quỹ thời gian hợp lý mà không cắt xén tuần dành cho bài nghiệm thu nhấc bánh.
3. Một mục sổ lab chỉ có ngày, ảnh đèn LED sáng và dòng chữ "chạy được", thiếu cả đoạn serial lẫn mục "cái gì hỏng". Khi cần gỡ lỗi về sau, bạn sẽ mất hai thông tin thực tế quan trọng nào?
4. Một người học muốn bắt đầu tuần 2 bằng việc chạy notebook huấn luyện mô hình ACT trong LeRobot. Họ đang bỏ qua những mốc nền tảng nào, và những hành vi vật lý nào của robot chưa hề được notebook đó kiểm chứng?
5. Giả sử lệnh điều khiển được gửi đều đặn mỗi $100\,\mathrm{ms}$. Cần bao nhiêu chu kỳ mất lệnh liên tiếp để thỏa mãn điều kiện $t_{\mathrm{silence}} > 300\,\mathrm{ms}$? Sau đúng ba chu kỳ mất lệnh, động cơ đã bắt buộc phải dừng chưa?

<details>
<summary>Gợi ý đáp án</summary>

1. Một phát biểu đạt yêu cầu: "Capstone A đạt khi xe vi sai hai bánh của tôi, trong trạng thái bánh nhấc khỏi mặt bàn, chạy theo lệnh teleop qua serial hoặc một trang Wi-Fi đơn giản, và firmware tự đưa duty PWM về 0 nếu không nhận được lệnh mới trong hơn 300 ms." Bản demo này nằm trong khoảng tuần 7–11, với mốc nghiệm thu ở Chương 07.
2. Kế hoạch P có $4 \times 16 = 64$ giờ; Kế hoạch Q có $6 \times 12 = 72$ giờ. Kế hoạch P giãn thời gian rộng hơn nên có thể sắp xếp Chương 11–12 sau khi hoàn tất Chương 00–10. Kế hoạch Q có tổng giờ cao hơn nhưng gói gọn trong 12 tuần nên không có tuần dư, do đó giai đoạn tuần 7–11 vẫn phải dành trọn cho bài nghiệm thu nhấc bánh.
3. Bạn không biết mạch thực sự đã in ra dữ liệu gì trên cổng serial, và cũng không biết trước khi LED sáng đã từng xảy ra sự cố gì. Nếu lần sau mạch gặp lại lỗi tương tự, bạn không có mốc dữ liệu để đối chiếu.
4. Người học đã bỏ qua giai đoạn firmware, mạch lái động cơ và bài nghiệm thu Chương 07. Notebook huấn luyện không kiểm chứng được việc robot có tự dừng khi mất lệnh teleop quá 300 ms hay không, cũng không kiểm tra được nguồn động cơ có đang cách ly an toàn khỏi chân logic 3,3 V hay không.
5. Sau đúng 3 chu kỳ mất lệnh, $t_{\mathrm{silence}} = 300\,\mathrm{ms}$, chưa vượt quá ngưỡng chặt $300\,\mathrm{ms}$ nên động cơ vẫn được phép chạy. Đến chu kỳ mất lệnh thứ tư, $t_{\mathrm{silence}} = 400\,\mathrm{ms} > 300\,\mathrm{ms}$ và duty PWM bắt buộc phải về 0.

</details>

## Đọc thêm

- [Tài liệu ROS 2 Jazzy](https://docs.ros.org/en/jazzy/) — tầng truyền thông sẽ dùng ở giai đoạn sau. Bạn có thể đọc phần giới thiệu để hình dung về topic, nhưng chưa cần cài đặt từ bài này.
- [LeRobot](https://github.com/huggingface/lerobot) — thư viện dành cho Chương 11 và 12. Việc tải mã nguồn ngay tuần đầu không giúp lắp ráp khung xe.
- [Tài liệu Duckietown](https://docs.duckietown.com/) — một hệ thống robot giáo dục có tài liệu công khai đầy đủ, hữu ích để tham khảo cách tổ chức tài liệu cho xe tự hành nhỏ (không phải danh sách mua sắm của khóa này).
- [Khóa manipulation của MIT](https://manipulation.mit.edu/) — tài liệu chuyên sâu về điều khiển thao tác và chính sách học máy; phù hợp để đọc thêm sau khi robot của bạn đã biết dừng an toàn.
