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

Dành khoảng chín mươi phút. Bạn cần một trình soạn thảo và một lịch. Chưa cần robot, cũng chưa cần Ubuntu. Việc của bài này là viết một bản đồ mà bạn vẫn dùng được khi khung xe cuối cùng cũng lăn.

## Mục tiêu học

Hết bài này bạn **nêu** được xương sống của khóa, từ việc nhận ra linh kiện, qua teleop Chương 07, tới chỗ đọc các bài robot learning sau này. Bạn **tính** được nhịp 4–6 giờ mỗi tuần trong 12–16 tuần và đặt các mốc chương lên lịch đó. Bạn **mở** một sổ lab với sáu trường: ngày, ảnh, sơ đồ dây, đoạn serial, cái gì hỏng, cái gì sửa được. Bạn **phân biệt** một ghi chú là bằng chứng hay chỉ là cảm giác, bằng cách nhìn chỗ thiếu đoạn serial hoặc thiếu mô tả lỗi. Bạn **tìm** bản tiếng Việt hoặc tiếng Anh của cùng một bài bằng chapter và order, và bạn **hoãn** LiDAR, Nav2, cùng một bản cài ROS 2 đầy đủ, cho tới khi robot vi sai đã dừng khi lệnh im.

## Cần có trước

Bạn đọc được một trang kỹ thuật nếu đọc chậm, và tạo được thư mục. Chưa cần đồng hồ, chưa cần mỏ hàn, chưa cần học robot từ trước. Định luật Ohm để Chương 01, lúc đó sẽ đo chứ không học thuộc. Cái cần ngay là ghi lại thứ đã hỏng. Câu "bắt đầu khóa học" không cứu được bạn ở tuần chín.

## Vì sao việc này dính tới Capstone

Chương 07 là Capstone A: hai bánh dẫn động và một bánh caster, bạn lái bằng tay khi bánh đang nhấc khỏi mặt bàn. Teleop nghĩa là bạn tự lái, không giao cho robot tự tìm đường. Nếu lệnh ngừng khoảng 300 ms, duty PWM phải về 0. ROS 2 Jazzy đứng sau bài kiểm đó. Một topic là một dòng tin có tên, lớp nhắn tin đặt trên vật lý mà bạn đã tin. Topic không tạo ra mô-men. Gazebo Harmonic và micro-ROS là cùng ý đó trong mô phỏng và trên vi điều khiển. Nếu bây giờ bạn chưa nói được quy tắc 300 ms, mọi lần cài đặt sau này chỉ là cách tránh bàn lab.

## Xương sống, theo đúng thứ tự bạn sẽ sống với nó

Khóa này là một đường, cuối đường có vài phòng tùy chọn.

Bạn bắt đầu bằng việc nhận ra linh kiện: một hàng breadboard, một board lái động cơ, một cáp USB chỉ sạc, một cell pin mà cục sạc không khớp nhãn. Chương 00 là thói quen trên bàn. Chương 01 biến điện áp, dòng và điện trở thành con số bạn đã đo.

Rồi tới firmware trên ESP32 hoặc Raspberry Pi Pico. Chương 02 đưa chương trình vào chip. Chương 03 khiến nó giống mã robot: chân, thời gian, và PWM. PWM, điều chế độ rộng xung, là một chân ở mức cao trong một phần của chu kỳ ngắn. Board lái biến phần đó thành mức motor bị yêu cầu quay mạnh tới đâu.

Chương 04 tới 06 thêm cảm biến, board lái, và cơ khí của hai bánh dẫn động. Chương 07 là bài nghiệm thu. Bạn gửi tiến, xoay, hoặc dừng, qua serial USB hoặc, sau này, một trang Wi-Fi nhỏ nếu bạn chọn ESP32. Bánh ở trên không. Một bộ đếm nhớ lệnh hợp lệ cuối. Gọi $t_{\mathrm{last}}$ là mốc đó và $t_{\mathrm{now}}$ là thời điểm trong vòng lặp. Khoảng im là

$$
t_{\mathrm{silence}} = t_{\mathrm{now}} - t_{\mathrm{last}}.
$$

Quy tắc dừng của khóa:

$$
t_{\mathrm{silence}} > 300\,\mathrm{ms} \implies \text{duty PWM} = 0.
$$

Dấu lớn hơn là nghiêm: lệnh rơi đúng 300 ms vẫn còn tính là mới. Hôm nay bạn chưa nạp vòng lặp này. Với tốc độ chậm $0{,}3\,\mathrm{m/s}$, robot có thể trườn khoảng 9 cm trong cửa sổ đó:

$$
s \approx 0{,}3\,\mathrm{m/s} \times 0{,}3\,\mathrm{s} = 0{,}09\,\mathrm{m}.
$$

Chín centimét cũng đủ giật đứt cáp USB, nên nghiệm thu là bánh nhấc lên.

Chỉ khi bản demo đó lặp lại được bạn mới thêm lớp nhắn tin. Chương 08 là truyền thông và vòng điều khiển đơn giản trên phần cứng bạn đã thấy chuyển động. Chương 09 cài ROS 2 Jazzy, và chỉ trên Ubuntu 24.04. Một topic vận tốc có ích vì bạn đã biết firmware làm gì khi tin nhắn dừng. Chương 10 gọi tên Gazebo Harmonic, bộ mô phỏng đi với Jazzy, và micro-ROS, cách để chính vi điều khiển đó nói ROS 2. micro-ROS đáng làm sau khi board đã kéo khung xe mà không cần nó. Một topic im và một motor im, nếu không, là cùng một triệu chứng.

Chương 11 và 12 là tùy chọn và đòi hỏi đọc cẩn thận. LeRobot là thư viện Hugging Face về dữ liệu robot và policy đã học. ACT dự đoán một khúc hành động phía trước. Diffusion policy sinh hành động bằng khử nhiễu từng bước. VLA ánh xạ ảnh và câu lệnh thành hành động. Không cái nào thay board lái biết tắt PWM. Đọc điều được khẳng định, dữ liệu, và giới hạn. Một repository không biến khung xe đầu thành nền tảng nghiên cứu.

Video hay coi vài thứ là bước một. Khóa này hoãn chúng: không LiDAR trong chương này, không Nav2, không cài ROS 2 tuần này trừ khi bạn chỉ đọc trang cài trên máy đã có Ubuntu 24.04. Bàn lab vẫn đi trước. Lăn được một giây không phải tự hành. Điện áp pin motor không lên chân 3,3 V.

## Nhịp: bốn đến sáu giờ, trong mười hai đến mười sáu tuần

Tải thiết kế là **4–6 giờ mỗi tuần** trong khoảng **12–16 tuần**. Mười bốn tuần, mỗi tuần năm giờ, là

$$
5 \times 14 = 70
$$

giờ. Mười hai tuần nhân sáu giờ là 72. Mười sáu tuần nhân bốn giờ là 64, đủ cho Chương 00 tới 10 nếu mỗi tuần có một buổi chạm bàn lab, hoặc chạm các thủ tục trên giấy trước khi hàng tới. Một tuần năm giờ là khoảng 90 phút đọc, 120 phút trên bàn, và 90 phút dọn ghi chú. Một chủ nhật mười hai giờ rồi ba tuần im sẽ làm bạn quên dây nào lỏng.

Các mốc chương là xương sống có ngày.

| Tuần | Chương | Bằng chứng bạn đưa ra được |
|-----:|--------|----------------------------|
| 1–3 | 00 và 01 | Thẻ lên nguồn, đồng hồ kêu trên một mối nối đã biết, và một mục sổ có điện áp hoặc chữ "không có" viết thật |
| 4–6 | 02 và 03 | Firmware trên ESP32 hoặc Pico, và một đoạn serial dán vào sổ |
| 7–11 | 04 tới 07 | Teleop bánh nhấc; duty PWM bằng 0 nếu lệnh im hơn khoảng 300 ms |
| 12–14 | 08 tới 10 | Một topic ROS 2 trên Ubuntu 24.04 mô tả chuyển động bạn đã tin; Gazebo Harmonic và micro-ROS được gọi tên từ sổ lab |
| Sau, tùy chọn | 11 và 12 | Một ghi chú đọc về LeRobot, ACT, diffusion policy hoặc VLA, nói rõ cái gì được đo trên robot của bạn và cái gì không |

Nếu một tuần sụp, bạn trượt mốc. Đừng bỏ bài bánh nhấc để "đuổi" Jazzy.

## Sổ lab

Giữ một file, `notes/lab-notes.md`. Mỗi mục có sáu trường. **Ngày** là ngày bạn đụng việc. **Ảnh** là tên trong thư viện hoặc ảnh bàn; viết `không có` khi không có gì để chụp. **Sơ đồ dây** có thể là ảnh tờ chì; chưa có mạch thì viết "chưa có mạch". **Đoạn serial** là chữ dán từ serial monitor, shell Thonny, hoặc echo ROS 2 sau này. Chưa cắm board thì ghi `không có — chưa có board`. **Cái gì hỏng** gọi triệu chứng đo được, ví dụ cổng serial mất khi hai motor buộc vào 5 V USB, không phải "motor hỏng". **Cái gì sửa được** gọi tên thay đổi, kể cả "chưa cấp nguồn; tôi viết quy tắc dừng trước khi mua". Trường trống biến mục thành tâm trạng.

Site có hai ngôn ngữ. Công tắc ngôn ngữ khớp **chapter** và **order**, không khớp tiêu đề. Trang này là chapter `00`, order `1`, bản song sinh cũng vậy. Nếu một đoạn rối, chuyển ngôn ngữ cho đúng đoạn đó. Giữ GPIO, PWM, breadboard, Capstone và ROS 2 ổn định ở cả hai thứ tiếng.

## Hình

![Các họ linh kiện và dụng cụ mà khóa sẽ yêu cầu bạn nhận ra]({{ site.imgurl }}/generated/kit_catalog_overview.png)

Bức vẽ là chân dung các họ đồ, không phải giỏ. Hóa đơn là bài 00-05. Mua theo tranh là cách LiDAR tới trước đồng hồ.

![Hai lộ trình học dùng chung một robot]({{ site.imgurl }}/generated/tracks_mcu_ros.png)

Lộ trình A nghiệm thu Capstone A bằng firmware, không cần Ubuntu. Lộ trình B là cùng robot cộng Ubuntu 24.04, ROS 2 Jazzy, Gazebo Harmonic và micro-ROS sau khi khung đã chạy. Chung một bài nghiệm thu. LiDAR ở ngoài cho tới khi bài đó đáng tin.

## Lab: sổ và mười bốn tuần tới

Tạo thư mục khóa và `notes/lab-notes.md`. Điền đủ sáu trường dưới ngày hôm nay. Ở sơ đồ, viết câu Capstone A: hai bánh dẫn động, bánh nhấc, serial hoặc Wi-Fi đơn giản, duty PWM bằng 0 nếu im quá 300 ms. Ở serial, viết `không có — chưa có board` trừ khi cổng đã hiện. Đừng bịa log.

Đặt ba khối lịch trong bảy ngày tới, cộng 4–6 giờ: Đọc, Bàn, Ghi chú. Khi hàng chưa tới, buổi Bàn có thể là "viết thẻ lên nguồn". Chép bảng mốc và ghi tuần lịch thật cạnh 1–3, 4–6, 7–11, 12–14. Đi vắng thì trượt mốc sau, đừng xóa Chương 07. Ba thứ không mua tháng này: LiDAR, máy tính mua chỉ để học ROS, và cục sạc chưa đọc nhãn. Giỏ hàng là [bài 00-05]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %}).

**Bạn sẽ thấy gì.** Người lạ tìm đủ sáu trường trong một phút. Câu có số 300. Lịch có buổi lặp.

**Khi lệch.** Trường trống thì ghi `không có`. Tách chủ nhật sáu giờ. Bookmark Nav2 ghi "sau Chương 07". Pin lithium rời chờ bài 00-05 khớp cục sạc với hóa học cell.

## Ví dụ làm sẵn

Hà bắt đầu tối thứ Tư, laptop Windows, chưa có linh kiện. Kế hoạch 6 giờ mỗi tuần trong 12 tuần là $6 \times 12 = 72$ giờ, nhưng tuần 8 cô đi vắng nên Chương 07 rơi vào tuần không có nhà. Năm giờ mỗi tuần trong 14 tuần là 70 giờ và vẫn xong Chương 00–10 nếu buổi bàn được giữ. Cô ghi mốc: tuần 1–3 Chương 00–01, tuần 4–6 Chương 02–03, tuần 7–11 Chương 04–07, tuần 12–14 Chương 08–10, Chương 11–12 tùy chọn sau khi robot dừng vì im lệnh.

Cô chép quy tắc 300 ms vào cùng mục. Serial ghi `không có — chưa có board`. Ảnh ghi `không có`. Cái gì hỏng: chưa cấp nguồn. Cái gì sửa được: cô viết số tuần trước khi mở tab mua. Thứ Năm 20:00–21:30 là buổi Bàn, nhãn "thẻ an toàn, chưa hàn". File đó là đạt.

## Bài tập

1. Viết câu Capstone A của bạn. Phải có hai bánh dẫn động, bánh nhấc, serial hoặc Wi-Fi đơn giản, và PWM bị tắt khi im quá khoảng 300 ms. Rồi ghi khoảng tuần nào câu đó thành một demo bạn quay phim được.
2. So hai lịch. Kế hoạch P là 4 giờ mỗi tuần trong 16 tuần. Kế hoạch Q là 6 giờ mỗi tuần trong 12 tuần. Tính tổng giờ mỗi kế hoạch. Kế hoạch nào còn chỗ thật cho Chương 11 và 12 mà không lấy mất tuần của bài bánh nhấc?
3. Một mục sổ có ngày, ảnh LED sáng, và chữ "chạy được". Thiếu đoạn serial và thiếu "cái gì hỏng". Hai sự thật nào một buổi sửa lỗi sau này không lấy lại được từ mục này?
4. Một người muốn tuần 2 bắt đầu bằng notebook huấn luyện ACT của LeRobot. Mốc nào bị bỏ, và hành vi vật lý nào của robot tương lai chưa được notebook kiểm?
5. Lệnh gửi mỗi $100\,\mathrm{ms}$. Cần bao nhiêu lệnh mất liên tiếp để $t_{\mathrm{silence}} > 300\,\mathrm{ms}$? Sau đúng ba chu kỳ mất, motor đã bị bắt buộc tắt chưa?

<details>
<summary>Gợi ý đáp án</summary>

1. Một câu chấp nhận được: "Capstone A đạt khi robot vi sai hai bánh của tôi, bánh nhấc khỏi bàn, đi theo teleop từ serial hoặc một trang Wi-Fi đơn giản, và firmware đưa duty PWM về 0 nếu không có lệnh mới trong hơn 300 ms." Demo đó nằm ở tuần 7–11, Chương 07 là cửa.
2. P là $4 \times 16 = 64$ giờ. Q là $6 \times 12 = 72$ giờ. P có thể để Chương 11 và 12 sau Chương 00–10. Q không có tuần dư trong 12 tuần, nên bài bánh nhấc vẫn sở hữu tuần 7–11.
3. Không lấy lại được chữ board thực sự in ra, và không lấy lại được thứ đã hỏng trước khi LED sáng. Lần sau "lại hỏng" không có gì để so.
4. Bỏ firmware, board lái, và Chương 07. Notebook không kiểm tra robot dừng khi teleop im khoảng 300 ms, cũng không kiểm tra điện áp motor có ở ngoài chân 3,3 V hay không.
5. Ba chu kỳ mất là $300\,\mathrm{ms}$, chưa vượt ngưỡng. Chu kỳ thứ tư thành $400\,\mathrm{ms}$ và PWM phải về 0. Sau đúng ba chu kỳ, motor vẫn được phép chạy.

</details>

## Đọc thêm

- [Tài liệu ROS 2 Jazzy](https://docs.ros.org/en/jazzy/) — lớp nhắn tin sau này. Đọc phần giới thiệu nếu bạn muốn hình dung topic. Đừng bắt đầu cài từ bài này.
- [LeRobot](https://github.com/huggingface/lerobot) — thư viện Chương 11 và 12 sẽ yêu cầu đọc cẩn thận. Clone tuần này không lắp được khung xe.
- [Tài liệu Duckietown](https://docs.duckietown.com/) — một robot dạy học có stack được công bố, hữu ích như bức tranh về cách người ta viết tài liệu cho xe nhỏ. Không phải hóa đơn của khóa này.
- [Khóa manipulation của MIT](https://manipulation.mit.edu/) — cách nhìn chặt về thao tác và policy đã học. Coi là đích để đọc sau khi robot của bạn đã biết dừng.
