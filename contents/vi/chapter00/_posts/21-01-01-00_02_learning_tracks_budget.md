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

Dành khoảng một giờ. Bạn cần câu Capstone từ bài chào mừng, và một mô tả thật về máy tính bạn đang có. Giá trong bài này là hình dạng của một ngân sách, không phải giỏ hàng. Giỏ hàng là [bài 00-05]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %}).

## Mục tiêu học

Ra khỏi bài này bạn **chọn** được lộ trình A hoặc B trong một câu có hệ điều hành laptop, trần tiền bằng VND, và mục tiêu hai tháng. Bạn **chỉ** được một robot lộ trình A gồm ESP32 hoặc Pico 2, motor bánh răng TT, TB6612FNG chứ không phải L298N, và HC-SR04, không cần Ubuntu để nghiệm thu Capstone A. Bạn **tính** được điện áp mà driver Darlington vứt đi, khoảng 2 V, và nói điều đó làm gì với một pack 7,4 V. Bạn **đặt** Ubuntu 24.04, ROS 2 Jazzy, Gazebo Harmonic và micro-ROS sau khi cùng robot đó đã chạy, Raspberry Pi chỉ là lựa chọn sau. Bạn **từ chối** mua LiDAR trước khi Capstone A được nghiệm thu, và viết sự từ chối đó ra.

## Cần có trước

Bài 00-01: bạn nói được bài teleop bánh nhấc và quy tắc dừng PWM 300 ms, và đã có sổ với sáu trường. Chưa cần Ubuntu, ROS, hay đơn hàng đã trả tiền. Nếu bạn đã có Raspberry Pi, hoặc laptop dual-boot Linux, bạn vẫn bắt đầu từ cùng một khung xe. Sở hữu máy không phải lý do bỏ robot firmware.

## Vì sao việc này dính tới Capstone

Capstone A không link với ROS. Nó cần một vi điều khiển canh được khoảng 300 ms, và một driver nhận PWM rồi buông ra. Nếu tháng đầu chỉ để chia ổ đĩa, dây motor vẫn chưa được thử. Lộ trình B là thật. Đó là đường tới topic Jazzy, Gazebo Harmonic và micro-ROS. Các topic đó là lớp nhắn tin trên vật lý bạn đã tin. Chọn lộ trình bây giờ là cách bạn không để một tab mua hàng chọn hộ, và không để LiDAR tới trước khi timeout tồn tại.

## Hai đường hợp lệ, một robot biết chạy

**Lộ trình A** là đường vi điều khiển tiết kiệm, và đủ cho Capstone A. Não là board ESP32 hoặc Raspberry Pi Pico 2. ESP32 là board bạn chọn khi muốn teleop Wi-Fi sau này: điện thoại hoặc laptop cùng bàn gửi lệnh mà demo cuối không cần cáp USB. Pico 2 là board bạn chọn khi muốn MicroPython và cáp USB trước. Cả hai nói logic 3,3 V. Cả hai chạy được quy tắc dừng 300 ms. Cả hai không đòi Ubuntu.

Cơ khí là motor bánh răng TT trên khung nhỏ, hai bánh dẫn động và một bánh caster. Driver bạn muốn là module **TB6612FNG**, cầu H MOSFET. Module người ta mua vì video dùng nó thường là **L298N**, cầu Darlington. Ở dòng motor, cặp Darlington rơi khoảng 2 V giữa pin và motor. Cầu MOSFET rơi vài phần mười vôn. Với pack hai cell ngồi gần 7,4 V,

$$
V_{\mathrm{L298}} \approx 7{,}4\,\mathrm{V} - 2{,}0\,\mathrm{V} = 5{,}4\,\mathrm{V},
$$

$$
V_{\mathrm{TB6612}} \approx 7{,}4\,\mathrm{V} - 0{,}3\,\mathrm{V} = 7{,}1\,\mathrm{V}.
$$

Motor TT vốn đã là hộp số nhỏ, hao. Bớt thêm 2 V là lý do "cùng một pin" thấy yếu trên L298N và bình thường trên TB6612. Carrier TB6612 của Pololu, [sản phẩm 713](https://www.pololu.com/product/713), là lời giải thích công khai rõ nhất về con chip đó nếu bạn muốn một kiểu sơ đồ thứ hai. Bạn được mua module khác dùng cùng chip. Bạn không bắt buộc nhập đúng carrier đó. DRV8833 là MOSFET thay thế nhỏ hơn khi TB6612 hết hàng. Nó vẫn không phải L298N.

Cảm biến khoảng cách trên giỏ đầu tiên là module siêu âm HC-SR04. Chân echo của nó vọt lên 5 V, nên không được cắm thẳng vào GPIO 3,3 V. Bài 00-05 có mạch dịch mức cho sợi dây đó. Lộ trình A không cài Ubuntu. Teleop serial từ Windows, macOS, hoặc Linux bạn đang có là đủ để nghiệm thu.

**Lộ trình B** là lộ trình A cộng một tầng phần mềm sau. Robot là cùng khung, cùng driver, cùng timeout. Khi teleop đã đáng tin, bạn dùng máy chạy **Ubuntu 24.04** và cài **ROS 2 Jazzy** ở đó. **Gazebo Harmonic** là bộ mô phỏng đi với bản phát hành đó, và là việc của Chương 10. **micro-ROS** cho vi điều khiển nói ROS 2 với máy đó. Nó là một đường truyền thêm lên trên PWM bạn đã nhìn thấy chạy. Raspberry Pi có thể xuất hiện sau như máy kèm tùy chọn. Nó không phải thiết bị quay motor đầu tiên, và không phải lý do mua LiDAR để Pi "có việc".

Người cài micro-ROS trên board chưa từng quay bánh sẽ sửa hai lỗi một lúc. Topic không có tin và motor không có điện, nhìn từ ghế, giống hệt nhau. Vì vậy khóa đặt đồ thị tin nhắn sau bàn lab.

![Lộ trình A bên trái, lộ trình B là tầng sau trên cùng robot]({{ site.imgurl }}/generated/tracks_mcu_ros.png)

Đọc bên trái hình là robot tháng này, bên phải là phần mềm bạn phải kiếm được. "Không cần Ubuntu" là giấy phép của lộ trình A cho Capstone A. "Chỉ mua LiDAR sau khi Capstone A đáng tin" là luật chi tiêu chung. LiDAR quay là một bài toán nguồn khác, một tutorial ROS khác, và thường là vài triệu đồng. Nó không làm quy tắc 300 ms đúng hơn.

## Bảng quyết định

Dùng bảng này như phiếu. Chép một hàng vào sổ và gạch các hàng kia, hoặc đánh một hàng "của tôi".

| Tình huống tháng này | Lộ trình | Làm ngay | Để sau |
| --- | --- | --- | --- |
| Hệ điều hành nào cũng được; khoảng 1,5–2,0 triệu VND; mục tiêu là "gõ là nó chạy" | A | ESP32 hoặc Pico 2, motor TT, TB6612FNG, HC-SR04, mạch dịch mức, dụng cụ, kế hoạch pin từ bài 00-05 | Ubuntu, Pi, LiDAR, Nav2, cài Jazzy |
| Windows hoặc macOS, và bạn muốn ROS về sau | A bây giờ, B sau Chương 07 | Cùng robot đó; viết "máy Ubuntu 24.04 của lab sau" | Đừng xóa ổ laptop; đừng mua LiDAR để biện minh cho một cái Pi tương lai |
| Bạn đã chạy Ubuntu 24.04 và muốn biết ROS | B, nhưng lắp robot lộ trình A trước | Cùng phần điện; được cài Jazzy song song trên máy đó | Đừng chặn Chương 07 bằng một world Gazebo; đừng bỏ bàn lab |
| Ngân sách chủ yếu là Pi cộng kit LiDAR từ một video | Dừng và tính lại | Viết lại mục tiêu thành teleop bánh nhấc | Kit đó không thực hiện dừng 300 ms hay sụt áp MOSFET |

Một LiDAR 4.000.000 ₫ cạnh lõi lộ trình A khoảng 800.000 ₫ là

$$
\frac{4{.}000{.}000}{800{.}000} = 5
$$

lần cái lõi, và nó không chớp LED đầu tiên. Tỷ số đó là lý do cấm mua trước nghiệm thu.

Giá phải có ngày. Một con số không ngày là chuyện bàn tán. Bài 00-05 giữ các snapshot Hshop có ngày cho thứ bạn sẽ đặt. Bài này không dựng lại bảng đó. Nếu một board nhảy một trăm nghìn đồng, lộ trình không đổi. Lộ trình chỉ đổi khi hệ điều hành, trần tiền, hoặc mục tiêu đổi.

## Lab: viết câu lộ trình

Mở `notes/lab-notes.md`. Dưới ngày hôm nay, viết ba dòng: hệ điều hành laptop, trần tiền VND cho 30 ngày tới, và mục tiêu một câu. Nếu mục tiêu có bản đồ, SLAM hoặc Nav2, thêm mệnh đề "sau Capstone A".

Chọn vi điều khiển bằng lời. Hoặc "board ESP32, teleop Wi-Fi sau, serial USB trước" hoặc "Pico 2, MicroPython, USB trước". Bạn được đổi trước khi trả tiền. Bạn không được để trống.

Viết câu này và ký tên sau nó: "Tôi sẽ không mua LiDAR trước khi teleop bánh nhấc Capstone A của tôi đạt, kể cả quy tắc dừng PWM 300 ms."

Thêm một dòng chỉ vào bài 00-05 như danh sách mua duy nhất. Đừng dán một giỏ thứ hai vào đây. Nếu bạn biết mình sẽ dùng máy lab chung cho Ubuntu, ghi tên máy đó là "Ubuntu lab, không phải laptop của tôi".

**Bạn sẽ thấy gì.** Người đọc sau biết bạn chọn lộ trình nào, nghiêng về MCU nào, và từ chối những món đắt nào. Ubuntu là "chưa", hoặc "máy lab sau", hoặc "đã cài, bàn lab vẫn trước".

**Khi lệch.** Bạn chọn B mà chỉ đặt một cái Pi. Motor vẫn do ESP32 hoặc Pico 2 lái; thêm các dòng đó bằng cách mở bài 00-05, không bịa kit mới. Bạn chọn A rồi cài Jazzy "thử cho biết" trên Windows. Đánh dấu trang cài vào mục "sau Chương 07" và đóng lại. Windows Subsystem cho Linux không phải lab robot. Ngân sách là một số không ngày. Tách "lõi robot" khỏi "dụng cụ" và ghi ngày ước lượng.

## Ví dụ làm sẵn

Minh có laptop Windows và trần khoảng 1,5–2,0 triệu VND trong tháng. Mục tiêu anh viết lần đầu là "học ROS và SLAM". Anh viết lại thành "lái robot hai bánh từ serial, có dừng 300 ms, rồi mới dùng máy Ubuntu của lab cho Jazzy". Bảng đặt anh vào lộ trình A ngay. Anh chọn ESP32 vì muốn teleop Wi-Fi như một biến thể sau của Chương 07, còn lệnh đầu vẫn là serial USB. Anh không mua thêm Pico 2. Anh không mua LiDAR. Anh ghi lộ trình B sẽ xảy ra trên máy lab trường đã có Ubuntu 24.04, không phải bằng cách chia lại ổ Windows tuần này. Danh sách anh sẽ chép là bài 00-05, không phải kit trên diễn đàn.

Một bạn khác, Lan, đã chạy Ubuntu 24.04 trên laptop của mình. Lan được phép làm theo [trang cài Jazzy](https://docs.ros.org/en/jazzy/Installation.html) song song, trong một buổi riêng, và ghi chuỗi phiên bản vào sổ. Lan không được bỏ bàn lab. Robot của Lan vẫn là motor TT, TB6612FNG, HC-SR04, và firmware đưa PWM về 0 khi gói tin dừng. Nếu Jazzy cài sạch mà motor còn trong túi, Lan không đi trước. Lan có lớp nhắn tin và chưa có vật lý. Gazebo Harmonic chỉ được gọi tên, chưa mở, cho tới khi khung xe đã qua teleop bánh nhấc ít nhất một lần. micro-ROS vẫn là một link, [micro.ros.org](https://micro.ros.org/), cho tới khi cùng board đó đã kéo bánh mà không cần nó.

Minh phác sụt áp Darlington để lựa driver không phải sở thích nhãn. Ở 7,4 V với khoảng 2 V rơi, motor thấy 5,4 V. Sụt MOSFET khoảng 0,3 V còn 7,1 V. Anh viết "TB6612FNG, không L298N" trong câu lộ trình. Cả hai người kết thúc mục bằng câu từ chối LiDAR. Không ai mở bảng tính thứ hai. Bài 00-05 là giỏ hàng.

## Bài tập

1. Laptop của bạn là Windows, trần 1.800.000 ₫, và bạn muốn robot chạy trong tháng này. Lộ trình nào, MCU nào nếu bạn quan tâm Wi-Fi sau, và driver nào? Ubuntu tuần này bạn làm gì?
2. Bạn đã có Ubuntu 24.04. Vì sao thứ lắp trước vẫn là khung xe lộ trình A, dù bạn được phép cài Jazzy song song?
3. Pin 6 V từ bốn viên AA nuôi một L298N rơi khoảng 2 V. Điện áp nào tới motor? Vì sao đó là cặp kém với motor TT, vốn đã yếu khi còn khoảng 4 V?
4. Một listing thêm LiDAR 3.500.000 ₫ vào kế hoạch lộ trình A "chỉ thêm một chút". Nghiệm thu Capstone A có dễ hơn không? LiDAR đứng ở đâu so với bài nghiệm thu?
5. micro-ROS đứng ở đâu so với ngày đầu bánh đáp lại lệnh serial? Một repo [linorobot2](https://github.com/linorobot/linorobot2) sẽ dụ bạn bỏ bước nào?

<details>
<summary>Gợi ý đáp án</summary>

1. Lộ trình A ngay. Chọn ESP32 nếu teleop Wi-Fi là đích sau; chọn Pico 2 nếu bạn muốn MicroPython qua USB trước và chấp nhận Wi-Fi là việc của người khác lúc này. Driver là TB6612FNG. Ubuntu chờ. Đừng cài Jazzy trên Windows rồi gọi đó là lab.
2. Jazzy cho thấy topic trên máy tính. Nó không cho thấy dây VM, hành vi stall, và timeout 300 ms chạy trên phần cứng mà sau này các topic sẽ mô tả. Cài song song thì được. Bỏ bàn lab thì không.
3. $6 - 2 = 4$ V tại motor. Bốn vôn là đầu yếu của hộp số TT nhỏ, ngay cả khi chưa tải. Robot bò hoặc stall, và triệu chứng trông như "motor hỏng".
4. Nghiệm thu không dễ hơn. LiDAR không thực hiện timeout hay driver MOSFET. Nó thuộc về sau Capstone A, nếu nó thuộc về đâu đó.
5. micro-ROS đến sau khi bánh đã đáp lại. linorobot2 là bức tranh một robot vi sai được mô tả cho ROS 2. Mở nó trước khi có driver và timeout sẽ dụ bạn sửa URDF trong khi bàn còn trống.

</details>

## Đọc thêm

- [linorobot2](https://github.com/linorobot/linorobot2) — một stack vi sai cụ thể cho ROS 2. Đọc như bức tranh đích của lộ trình B, không phải danh sách linh kiện tháng này.
- [micro-ROS](https://micro.ros.org/) — nó là gì. Mang tutorial trở lại sau khi khung xe chạy mà không cần nó.
- [Cài ROS 2 Jazzy](https://docs.ros.org/en/jazzy/Installation.html) — Ubuntu 24.04 là đường được hỗ trợ. Nếu máy hàng ngày là Windows, trang này là việc của máy lab sau.
- [Pololu TB6612FNG, sản phẩm 713](https://www.pololu.com/product/713) — vì sao một carrier MOSFET là driver để đem so với module Darlington.

Việc mua nằm ở [bài 00-05]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %}). Đừng dựng lại giỏ từ bốn link này.
