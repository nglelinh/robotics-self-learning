---
layout: post
title: "Hai lộ trình: MCU tiết kiệm và ROS"
chapter: "00"
order: 2
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter00
lesson_type: required
draft: false
---

Hãy dành khoảng một giờ cho bài học này. Bạn cần chuẩn bị sẵn phát biểu Capstone A từ bài chào mừng và thông tin chính xác về máy tính mình đang sử dụng. Các mức giá nêu trong bài chỉ nhằm giúp bạn hình dung khung ngân sách, không phải danh sách mua hàng; danh sách mua sắm chính thức nằm ở [bài 00-05]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %}).

## Mục tiêu học

Sau bài học này, bạn sẽ **chọn** được Lộ trình A hoặc Lộ trình B bằng một phát biểu ngắn gọn nêu rõ hệ điều hành máy tính, hạn mức ngân sách bằng VND và mục tiêu trong hai tháng tới. Bạn sẽ **xác định** được cấu hình phần cứng của robot Lộ trình A gồm ESP32 hoặc Pico 2, động cơ giảm tốc TT, mạch lái TB6612FNG (thay vì L298N) và cảm biến HC-SR04 — đủ để nghiệm thu Capstone A mà không cần Ubuntu. Bạn sẽ **tính** được mức sụt áp khoảng 2 V của mạch cầu Darlington và phân tích tác động của nó lên bộ pin 7,4 V. Bạn cũng sẽ **sắp xếp** Ubuntu 24.04, ROS 2 Jazzy, Gazebo Harmonic và micro-ROS vào giai đoạn sau khi robot đã chạy ổn định (Raspberry Pi chỉ là tùy chọn mở rộng về sau), đồng thời **cam kết bằng văn bản** không mua LiDAR trước khi nghiệm thu thành công Capstone A.

## Cần có trước

Từ bài 00-01, bạn đã nắm được yêu cầu của bài teleop nhấc bánh, quy tắc ngắt PWM sau 300 ms và đã tạo sổ lab đủ sáu trường. Hiện tại bạn chưa cần Ubuntu, ROS hay đơn hàng linh kiện nào. Ngay cả khi đã có sẵn Raspberry Pi hoặc laptop cài song song Linux, bạn vẫn bắt đầu từ cùng một khung xe vi sai; có sẵn phần cứng mạnh không phải lý do để bỏ qua phần firmware cơ bản.

## Vì sao bài này gắn liền với Capstone

Capstone A không phụ thuộc vào ROS. Bài nghiệm thu này chỉ cần một vi điều khiển kiểm soát được ngưỡng 300 ms và một mạch lái động cơ đáp ứng đúng tín hiệu PWM rồi ngắt an toàn khi mất lệnh. Nếu tháng đầu tiên chỉ trôi qua với việc phân vùng ổ đĩa cài Linux, bạn vẫn chưa kiểm chứng được dây động cơ. Lộ trình B hoàn toàn thực tế vì nó dẫn tới ROS 2 Jazzy, Gazebo Harmonic và micro-ROS, nhưng các công cụ đó chỉ là tầng truyền thông xây dựng phía trên nền tảng phần cứng đã đáng tin cậy. Chốt lộ trình ngay từ bây giờ giúp bạn tránh mua sắm cảm tính và không rơi vào cảnh mua LiDAR trước khi cơ chế tự dừng tồn tại.

## Hai lộ trình hợp lệ trên cùng một khung robot

**Lộ trình A** là hướng vi điều khiển tiết kiệm và hoàn toàn đủ để vượt qua Capstone A. Bộ xử lý trung tâm là mạch ESP32 hoặc Raspberry Pi Pico 2. Bạn nên chọn ESP32 nếu muốn mở rộng sang điều khiển teleop qua Wi-Fi ở giai đoạn sau (dùng điện thoại hoặc laptop cùng mạng gửi lệnh mà không cần cắm cáp USB). Ngược lại, Pico 2 phù hợp nếu bạn ưu tiên làm việc với MicroPython qua cáp USB ngay từ đầu. Cả hai mạch đều dùng mức logic 3,3 V, đều thực thi tốt quy tắc dừng 300 ms và không yêu cầu Ubuntu.

Phần truyền động gồm hai động cơ giảm tốc TT lắp trên khung xe nhỏ cùng một bánh đa hướng (caster). Mạch lái động cơ khuyến nghị là **TB6612FNG** dùng cầu H MOSFET. Nhiều video hướng dẫn thường dùng **L298N** (cầu Darlington), nhưng ở dòng tải của động cơ, tầng Darlington gây sụt áp khoảng 2 V giữa pin và động cơ, trong khi cầu MOSFET chỉ sụt vài phần mười vôn. Với bộ pin hai cell có điện áp danh định gần 7,4 V:

$$
V_{\mathrm{L298}} \approx 7{,}4\,\mathrm{V} - 2{,}0\,\mathrm{V} = 5{,}4\,\mathrm{V},
$$

$$
V_{\mathrm{TB6612}} \approx 7{,}4\,\mathrm{V} - 0{,}3\,\mathrm{V} = 7{,}1\,\mathrm{V}.
$$

Động cơ TT vốn dùng hộp số nhựa nhỏ và có tổn hao cơ khí; mất thêm 2 V là lý do cùng một bộ pin nhưng xe chạy yếu hẳn trên L298N trong khi hoạt động bình thường trên TB6612FNG. Trang sản phẩm carrier TB6612 của Pololu ([sản phẩm 713](https://www.pololu.com/product/713)) là tài liệu tham khảo rất rõ ràng về con chip này, dù bạn hoàn toàn có thể mua module tương đương dùng cùng IC mà không cần nhập đúng mạch của Pololu. Nếu TB6612 hết hàng, DRV8833 là phương án thay thế dùng MOSFET gọn hơn — và vẫn tốt hơn L298N ở dải điện áp thấp.

Cảm biến khoảng cách trong bộ khởi đầu là module siêu âm HC-SR04. Lưu ý rằng chân echo của cảm biến xuất mức cao khoảng 5 V nên tuyệt đối không cắm trực tiếp vào chân GPIO 3,3 V; bài 00-05 sẽ bổ sung mạch chuyển mức logic cho đường tín hiệu này. Lộ trình A không yêu cầu cài Ubuntu: gửi lệnh teleop qua cổng serial từ Windows, macOS hay Linux hiện có đều đủ để nghiệm thu.

**Lộ trình B** là sự mở rộng của Lộ trình A thêm một tầng phần mềm phía trên, sử dụng đúng khung xe, mạch lái và cơ chế timeout đó. Khi hệ thống teleop đã chạy ổn định, bạn dùng máy tính cài **Ubuntu 24.04** và **ROS 2 Jazzy**. **Gazebo Harmonic** là bộ mô phỏng tương thích với bản phát hành này (triển khai ở Chương 10), còn **micro-ROS** cho phép vi điều khiển giao tiếp trực tiếp với ROS 2 trên máy tính. Raspberry Pi có thể được bổ sung sau như một máy tính đồng hành tùy chọn trên xe, nhưng nó không phải thiết bị dùng để quay động cơ ở bước đầu và cũng không phải lý do để mua LiDAR sớm.

Nếu cài micro-ROS trên một mạch chưa từng quay thử bánh xe, bạn sẽ phải gỡ cùng lúc hai lớp lỗi: một topic không có dữ liệu và một động cơ không có nguồn nhìn từ bên ngoài có biểu hiện giống hệt nhau. Đó là lý do khóa học luôn đặt tầng truyền thông phía sau thực hành bàn lab.

![Lộ trình A bên trái, lộ trình B là tầng sau trên cùng robot]({{ site.imgurl }}/generated/tracks_mcu_ros.png)

Hãy đọc sơ đồ theo thứ tự: phần bên trái là robot bạn cần hoàn thiện trong tháng này, phần bên phải là tầng phần mềm mở rộng sau khi phần cứng đã ổn định. Nguyên tắc "không cần Ubuntu" áp dụng cho Lộ trình A đến hết Capstone A, còn "chỉ mua LiDAR sau khi Capstone A đáng tin cậy" là kỷ luật chi tiêu chung cho cả hai lộ trình. Một cảm biến LiDAR quay kéo theo bài toán nguồn riêng, tài liệu ROS phức tạp hơn và chi phí thường lên tới vài triệu đồng, nhưng lại không giúp quy tắc dừng 300 ms chính xác hơn.

## Bảng quyết định

Hãy dùng bảng sau để chọn phương án phù hợp, chép dòng tương ứng vào sổ lab và đánh dấu rõ lựa chọn của bạn:

| Tình huống hiện tại | Lộ trình | Làm ngay | Để sau |
| --- | --- | --- | --- |
| Hệ điều hành nào cũng được; ngân sách khoảng 1,5–2,0 triệu VND; mục tiêu là "gửi lệnh là xe chạy" | A | ESP32 hoặc Pico 2, động cơ TT, TB6612FNG, HC-SR04, mạch chuyển mức, dụng cụ và kế hoạch pin theo bài 00-05 | Ubuntu, Raspberry Pi, LiDAR, Nav2, cài ROS 2 Jazzy |
| Đang dùng Windows hoặc macOS và muốn học ROS về sau | A trước, sang B sau Chương 07 | Lắp đúng robot Lộ trình A; ghi chú kế hoạch dùng máy Ubuntu 24.04 sau này | Không chia lại ổ cứng laptop vội; không mua LiDAR chỉ để có việc cho Raspberry Pi |
| Đã có sẵn máy chạy Ubuntu 24.04 và muốn tiếp cận ROS | B, nhưng vẫn lắp robot Lộ trình A trước | Làm phần điện tương tự Lộ trình A; có thể cài song song Jazzy trên máy đó | Không để mô phỏng Gazebo cản tiến độ Chương 07; không bỏ qua bàn lab |
| Ngân sách chủ yếu định chi cho Raspberry Pi kèm bộ LiDAR thấy trong video | Dừng lại và cân đối lại | Đặt lại mục tiêu là demo teleop nhấc bánh | Bộ kit đó không tự giải quyết quy tắc dừng 300 ms hay vấn đề sụt áp driver |

Một cảm biến LiDAR giá khoảng 4.000.000 ₫ đặt cạnh phần lõi phần cứng Lộ trình A khoảng 800.000 ₫ có tỷ lệ chi phí là:

$$
\frac{4{.}000{.}000}{800{.}000} = 5
$$

lần, trong khi nó thậm chí không giúp bạn làm nhấp nháy đèn LED đầu tiên. Tỷ lệ này giải thích vì sao khóa học yêu cầu hoãn mua LiDAR cho tới sau nghiệm thu.

Mọi con số về giá đều phải gắn kèm ngày khảo sát. Bài 00-05 lưu các mốc giá Hshop có ghi ngày cụ thể cho từng món bạn cần đặt mua, nên bài này không lặp lại bảng giá đó. Nếu một mạch vi điều khiển tăng hoặc giảm một trăm nghìn đồng, lộ trình học vẫn giữ nguyên; lộ trình chỉ thay đổi khi hệ điều hành, trần ngân sách hoặc mục tiêu học tập của bạn thay đổi.

## Thực hành: viết cam kết lộ trình

Mở `notes/lab-notes.md` và ghi ba dòng dưới ngày hôm nay: hệ điều hành máy tính đang dùng, hạn mức ngân sách bằng VND cho 30 ngày tới, và mục tiêu một câu. Nếu mục tiêu có nhắc tới lập bản đồ, SLAM hoặc Nav2, hãy bổ sung cụm "sau Capstone A".

Tiếp theo, viết rõ lựa chọn vi điều khiển: chọn "ESP32, ưu tiên serial USB trước và teleop Wi-Fi sau" hoặc "Pico 2, dùng MicroPython qua USB trước". Bạn vẫn có thể đổi ý trước khi đặt mua, nhưng không được để trống lựa chọn này.

Chép lại câu cam kết sau và ghi tên mình bên dưới: "Tôi sẽ không mua LiDAR trước khi bài teleop nhấc bánh Capstone A của tôi đạt yêu cầu, bao gồm quy tắc dừng PWM 300 ms."

Cuối cùng, thêm một dòng ghi chú chỉ về bài 00-05 như danh sách mua sắm duy nhất thay vì tạo thêm giỏ hàng thứ hai. Nếu bạn dự định dùng máy chung ở phòng lab cho Ubuntu về sau, hãy ghi rõ "dùng máy Ubuntu của lab, không dùng laptop cá nhân".

**Kết quả cần đạt:** Người đọc nhìn vào sổ biết ngay bạn đi lộ trình nào, chọn vi điều khiển gì, từ chối mua món đắt tiền nào, và trạng thái Ubuntu là "chưa cài", "dùng máy lab sau" hay "đã cài nhưng vẫn ưu tiên bàn lab".

**Cách xử lý khi lệch chuẩn:** Nếu bạn chọn Lộ trình B nhưng chỉ định mua Raspberry Pi, hãy nhớ động cơ vẫn do ESP32 hoặc Pico 2 điều khiển và bổ sung các món đó theo bài 00-05. Nếu bạn chọn Lộ trình A nhưng định cài thử Jazzy trên Windows, hãy lưu trang hướng dẫn vào mục "sau Chương 07" và đóng tab lại vì Windows Subsystem for Linux (WSL) không thay thế được môi trường thực hành robot. Nếu ngân sách chưa ghi ngày, hãy tách rõ phần "lõi robot" với "dụng cụ" kèm ngày ước tính.

## Ví dụ làm sẵn

Minh dùng laptop Windows với trần ngân sách khoảng 1,5–2,0 triệu VND trong tháng này. Ban đầu anh đặt mục tiêu là "học ROS và SLAM", sau đó viết lại thành "điều khiển xe hai bánh qua serial có quy tắc dừng 300 ms, rồi mới dùng máy Ubuntu của phòng lab để học Jazzy". Dựa theo bảng quyết định, anh đi theo Lộ trình A trước và chọn ESP32 để sau này mở rộng sang teleop Wi-Fi ở Chương 07, trong khi giai đoạn đầu vẫn dùng serial USB. Anh không mua thêm Pico 2, không mua LiDAR, và không phân vùng lại ổ đĩa Windows tuần này vì sẽ dùng máy Ubuntu 24.04 của trường về sau. Danh sách mua sắm anh sử dụng là bài 00-05.

Một bạn khác là Lan đã cài sẵn Ubuntu 24.04 trên laptop cá nhân. Lan có thể làm theo [trang cài đặt Jazzy](https://docs.ros.org/en/jazzy/Installation.html) trong một buổi riêng song song và ghi phiên bản thực tế vào sổ lab, nhưng không được bỏ qua thực hành phần cứng. Robot của Lan vẫn gồm động cơ TT, TB6612FNG, HC-SR04 và firmware đưa PWM về 0 khi mất lệnh. Nếu Jazzy đã cài xong nhưng linh kiện vẫn nằm nguyên trong túi, Lan chưa hề đi trước tiến độ mà mới chỉ có tầng phần mềm. Gazebo Harmonic chỉ được ghi tên chứ chưa mở cho đến khi khung xe vượt qua bài teleop nhấc bánh, và micro-ROS ([micro.ros.org](https://micro.ros.org/)) cũng chờ đến khi mạch tự quay được bánh xe độc lập.

Minh tự kiểm tra phép tính sụt áp để việc chọn mạch lái dựa trên cơ sở kỹ thuật thay vì cảm tính: ở nguồn 7,4 V, sụt áp 2 V của Darlington chỉ còn 5,4 V cho động cơ, còn sụt áp khoảng 0,3 V của MOSFET giữ lại 7,1 V. Anh ghi rõ "dùng TB6612FNG, không dùng L298N" vào câu lộ trình. Cả Minh và Lan đều kết thúc ghi chú bằng câu cam kết không mua LiDAR sớm và thống nhất lấy bài 00-05 làm danh sách mua sắm duy nhất.

## Video tham khảo

- **Xem trước:** [Raspberry Pi VS Arduino VS ESP32](https://www.youtube.com/watch?v=oJs0cVYuQTw) — TechteamGB, tiếng Anh. Đối chiếu ba dòng mạch với hai lộ trình trong bài: làm chủ vi điều khiển trước, máy tính chạy ROS để sau.
- [ROS 2 Series #1 | Giới thiệu sơ lược về ROS | TeslaEdison](https://www.youtube.com/watch?v=_vovUjZM6os) — TeslaEdison, tiếng Việt. Video giới thiệu tổng quan ROS 2 bằng tiếng Việt; lưu ý không nhầm tên bản phân phối trong video với ROS 2 Jazzy của khóa học.

## Bài tập

1. Bạn dùng laptop Windows, trần ngân sách 1.800.000 ₫ và muốn robot chạy trong tháng này. Bạn nên chọn lộ trình nào, vi điều khiển nào (nếu muốn làm Wi-Fi về sau) và mạch lái nào? Với Ubuntu trong tuần này, bạn nên xử lý thế nào?
2. Nếu máy tính của bạn đã cài sẵn Ubuntu 24.04, vì sao bạn vẫn phải lắp khung xe theo Lộ trình A trước dù được phép cài song song ROS 2 Jazzy?
3. Một bộ 4 pin AA tạo điện áp 6 V cấp qua L298N bị sụt khoảng 2 V. Điện áp thực tế tới động cơ là bao nhiêu? Vì sao đây là sự kết hợp kém với động cơ TT vốn đã yếu quanh mức 4 V?
4. Một cửa hàng gợi ý thêm cảm biến LiDAR giá 3.500.000 ₫ vào bộ Lộ trình A. Việc này có giúp nghiệm thu Capstone A dễ hơn không, và LiDAR nên xuất hiện ở giai đoạn nào?
5. micro-ROS nên được triển khai vào lúc nào so với ngày đầu tiên bánh xe đáp ứng lệnh serial? Nếu mở kho mã nguồn [linorobot2](https://github.com/linorobot/linorobot2) quá sớm, bạn dễ bị cuốn vào việc bỏ qua bước nền tảng nào?

<details>
<summary>Gợi ý đáp án</summary>

1. Chọn Lộ trình A ngay từ đầu. Chọn ESP32 nếu có kế hoạch làm teleop Wi-Fi về sau (hoặc Pico 2 nếu muốn dùng MicroPython qua USB trước). Mạch lái là TB6612FNG. Việc cài Ubuntu để sau, không cài Jazzy trên Windows rồi coi đó là thực hành robot.
2. Jazzy giúp bạn quan sát topic trên máy tính, nhưng không kiểm chứng được đường nguồn VM, hiện tượng kẹt trục (stall) và cơ chế timeout 300 ms trên phần cứng thật. Cài song song để tìm hiểu thì được, nhưng không thể thay thế bàn lab.
3. Điện áp tại động cơ chỉ còn $6 - 2 = 4$ V. Mức 4 V nằm ở vùng rất yếu của hộp số TT ngay cả khi không tải, khiến xe bò chậm hoặc kẹt trục và dễ bị nhầm là động cơ hỏng.
4. Không giúp nghiệm thu dễ hơn. LiDAR không thực thi quy tắc timeout và không thay thế mạch lái MOSFET. Nó chỉ nên cân nhắc sau khi Capstone A đã chạy ổn định.
5. micro-ROS chỉ nên triển khai sau khi bánh xe đã đáp ứng tốt lệnh serial. Kho mã nguồn `linorobot2` mô tả một robot vi sai hoàn chỉnh cho ROS 2; xem nó trước khi có mạch lái và cơ chế timeout rất dễ khiến bạn sa đà vào việc chỉnh sửa tệp URDF trong khi phần cứng thực tế chưa hề được lắp.

</details>

## Đọc thêm

- [linorobot2](https://github.com/linorobot/linorobot2) — một hệ thống phần mềm xe vi sai mẫu cho ROS 2; nên đọc để hình dung đích đến của Lộ trình B thay vì coi là danh sách linh kiện tháng này.
- [micro-ROS](https://micro.ros.org/) — tài liệu giới thiệu micro-ROS; hãy quay lại thực hành hướng dẫn sau khi khung xe đã vận hành độc lập.
- [Cài ROS 2 Jazzy](https://docs.ros.org/en/jazzy/Installation.html) — hướng dẫn cài đặt chính thức trên Ubuntu 24.04; nếu bạn đang dùng Windows, hãy để dành cho máy lab về sau.
- [Pololu TB6612FNG, sản phẩm 713](https://www.pololu.com/product/713) — tài liệu giải thích rõ lý do mạch lái MOSFET vượt trội hơn mạch Darlington ở điện áp thấp.

Toàn bộ danh sách mua sắm nằm tại [bài 00-05]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %}); đừng tự tạo giỏ hàng mới từ bốn liên kết tham khảo trên.
