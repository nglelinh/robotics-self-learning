---
layout: post
title: "Tổng quan Vision-Language-Action"
chapter: "12"
order: 4
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter12
lesson_type: required
draft: false
---

Thời lượng: **~75 phút**. Bạn đọc hai hệ đủ kỹ để điền một bảng, và để ba tên còn lại là tên bạn có thể quay lại. Không checkpoint nào được nạp.

## Mục tiêu

Bạn định nghĩa vision-language-action model là ánh xạ từ một ảnh cộng một câu lệnh chữ sang một action trên một robot cụ thể. Bạn đặt RT-1, RT-2, Open X-Embodiment, OpenVLA và pi0 lên bản đồ đó: mỗi cái đọc gì, viết gì, và những gì nó viết có phải `Twist` hay đích khớp của Capstone hay không. Bạn nói khoảng cách embodiment bằng một ví dụ cụ thể, và bạn giữ timeout động cơ cao hơn mọi câu một người gõ. Ô "train ở nhà" của RT-2 trong bảng lab là một chữ không thẳng thắn.

## Kiến thức cần trước

Bạn đọc được một trang dự án. Bài 12-01 đến 12-03 đã cho khóa dataset, một chunk, và một lý do để không lấy trung bình hai demonstration. `cmd_vel` chương 09 vẫn là `linear.x` theo m/s và `angular.z` theo rad/s. Camera chương 11, nếu bạn có, là cảm biến trên đế của bạn, không phải camera cổ tay trên một kẹp song song. Laptop không GPU là máy được kỳ vọng.

## Vì sao bài này nằm trên lộ trình

Jazzy, Nav2 và cầu nối đã cho phép gõ một đích rồi xem khung vi sai bám một đường. Các bài báo trong bài này gõ đích bằng ngôn ngữ thường và chờ một mạng phát lệnh động cơ. Đó là một hướng nghiên cứu thật, và rất dễ đọc nhầm thành "robot giờ hiểu câu, nên firmware được nghỉ". Không được. Checkpoint là một hàm từ camera và vector action của các robot đã sinh dữ liệu cho nó. Tay máy di động của RT-1, một kẹp trong Open X-Embodiment, và Capstone không chung vector đó. Ngôn ngữ không vá chỗ lệch. Bài này là cách bạn đọc câu khẳng định mà không chĩa câu đó vào bánh xe của mình.

## Khái niệm

Một vision-language-action model, gọi tắt VLA, nhận điểm ảnh và một chuỗi, trả về một action. Chuỗi là chỉ dẫn: "nhặt quả táo", "đi ra cửa". Action là thứ robot luyện đã thực hiện, rời rạc hóa hoặc liên tục. Lời hứa, khi nó chạy, là bạn hỏi một việc bằng lời thay vì chỉ bằng log cần lái. Giới hạn, dòng đỏ trên hình, là kẹp của lab khác là một robot khác. Embodiment là một phần của mô hình. Đổi thân thì cùng bộ trọng số trở thành một hàm tự tin nhằm nhầm động cơ.

**RT-1** (Robotics Transformer, Brohan và cộng sự) là đầu "dữ liệu robot" của câu chuyện. Trang dự án là [robotics-transformer1.github.io](https://robotics-transformer1.github.io/), bài báo là [arXiv:2212.06817](https://arxiv.org/abs/2212.06817). Mạng là một transformer luyện trên một tập demonstration lớn từ chính các tay máy di động của nhóm tác giả. Đầu vào là ảnh camera và một câu chỉ dẫn. Đầu ra là action rời rạc cho nền đó: chuyển động tay, chuyển động đế, và kẹp, gói trong một vector, thường dự đoán từng bước. Chuyển động đế của họ không phải `geometry_msgs/Twist` trên đồ thị ROS của bạn. Nó là một trường trong action của họ, đơn vị của họ, động học của họ. Bạn đọc trang được. Bạn không thả hành vi đã phát hành đó lên Capstone rồi gọi cầu là xong.

**RT-2** ([arXiv:2307.15818](https://arxiv.org/abs/2307.15818)) bắt đầu từ một vision-language model đã đọc ảnh và chữ ở tầm web, rồi tinh chỉnh chung để action robot chỉ là thêm token trong cùng một dòng. Ý của bài báo là chuyển giao: một cụm từ robot chưa từng tập vẫn có thể lái một kỹ năng robot đã tập, vì phía ngôn ngữ đã biết đôi điều về các từ. Chuyển giao đó là câu đáng đọc. Cách luyện là tinh chỉnh một mô hình rất lớn ở trung tâm dữ liệu, không phải laptop. Viết "RT-2 hiểu ngôn ngữ" trong sổ lab là chưa đủ nếu câu sau không nói cánh tay nào đã sinh ra các token action.

**Open X-Embodiment** ([robotics-transformer-x.github.io](https://robotics-transformer-x.github.io/)) là một hợp tác dataset qua nhiều lab và nhiều robot, cùng các mô hình (RT-X) luyện trên cái hồ đó. Bài học hữu ích cho khóa này là khoảng trống mà cái hồ không lấp. Camera cổ tay, kẹp song song, robot delta, và đế hai bánh đóng góp ảnh khác nhau và vector action khác nhau. Chuẩn hóa tên cột không chuẩn hóa vật lý. Policy đã thấy một tá kẹp thì đã tập bài toán kẹp. Bài toán Capstone là $$v$$ và $$\omega$$ dưới một camera nhìn trước, với timeout 300 ms trong vòng lặp. Thêm embodiment trong file không phải một bộ não cho embodiment bạn bỏ ngoài, hoặc cho một embodiment bạn chỉ bỏ vào với một phần rất nhỏ dữ liệu.

**OpenVLA** ([arXiv:2406.09246](https://arxiv.org/abs/2406.09246), trang dự án [openvla.github.io](https://openvla.github.io/)) là một VLA trọng số mở cùng họ ý tưởng: ảnh và chỉ dẫn đi vào, action robot rời rạc đi ra, luyện từ một xương sống vision-language mở trên dữ liệu Open X-Embodiment. "Trọng số mở" nghĩa là một người nghiên cứu có đúng máy thì nạp được. Nó không nghĩa là laptop lớp học không GPU luyện được, và không nghĩa là laptop đó chạy một mạng nhiều tỉ tham số ở 50 Hz giữa các khung serial của bạn. Action các trọng số đó phát đi theo robot trong dataset, thường là chuyển động đầu cuối của một cánh tay cộng một kẹp, không phải `linear.x` và `angular.z` cho khung vi sai. Việc trung thực tối nay là bài báo và trang dự án.

**pi0**, của Physical Intelligence, là đầu flow-matching của cùng một ý. Hãy đọc bài blog [pi0](https://www.physicalintelligence.company/blog/pi0) thay vì một tin đồn về kiến trúc. Bài viết trình bày một policy tổng quát: ảnh và ngôn ngữ đi vào, action liên tục đi ra, sinh bằng flow (họ hàng của phép khử nhiễu bạn vừa đọc, không phải một ACT thứ hai). Robot trong bài là của họ. Flow matching không đổi quỹ đạo kẹp thành đế bánh của bạn. Nếu chữ trên blog đã đổi lúc bạn mở, hãy trích đúng chỗ bạn thấy và giữ câu embodiment bằng lời của bạn.

An toàn nằm dưới mọi dòng của bảng. Một lệnh ngôn ngữ không phải E-stop. Chuỗi "stop" chỉ là thêm một token. Mạng vẫn có thể phát một action tiến nhỏ, hoặc phát dừng muộn một chunk, hoặc bỏ qua từ đó vì demonstration dùng từ khác. Timeout động cơ không đọc tiếng Anh. Nó chỉ nhận ra khung serial đã ngừng. Nếu node policy còn sống và vẫn xuất bản phần còn lại của quỹ đạo, timer 300 ms cứ reset, đúng như với chunk ACT xấu. Một chữ "dừng" đã gõ chỉ an toàn sau khi mã của bạn biến nó thành PWM bằng 0, một `Twist` bằng 0, hoặc một ngắt phần cứng. Công tắc nguồn tay với tới vẫn thắng chuỗi chỉ dẫn. Lần đầu một node mới được phép xuất bản, bánh vẫn phải nhấc lên.

## Hình

![Ảnh và ngôn ngữ đi qua trọng số thành action]({{ site.imgurl }}/generated/ch12_vla.png)

Bốn hộp: image, language, VLA weights, action. Mũi tên là lượt thuận của ý tưởng, không phải đồ thị ROS. Dòng đỏ là lời sửa: kẹp của lab khác là robot khác, và embodiment là một phần của mô hình. Chân hình liệt kê RT-1, RT-2, Open X-Embodiment, OpenVLA và pi0, với chỉ dẫn đọc và đừng train lại. Lab của bạn nghe chân hình. Hai dòng của một bảng là thứ nộp, không phải một lần tinh chỉnh.

## Ví dụ đọc có số

Tự điền RT-1 trước khi điền bất kỳ ai khác, và nếu một ô ở đây lệch so với trang dự án thì lấy trang dự án. Dòng này là thước lab bị chấm: đầu vào cụ thể, không gian action có tên một thân, và ô laptop không giả vờ.

| Hệ | Đầu vào | Không gian action | `Twist` trên đồ thị của bạn, hay đích khớp? | Laptop tối nay? |
| --- | --- | --- | --- | --- |
| RT-1 | Ảnh RGB từ camera robot của họ, cộng một câu chỉ dẫn | Vector rời rạc cho tay máy di động của họ: tay, đế, kẹp | Chuyển động đế nằm trong vector của họ. Không phải `cmd_vel` của bạn. Cũng không phải đích khớp của bạn | Đọc trang: có. Train: không. Chạy cụm suy luận của họ trên laptop không GPU: không |

Một con số làm embodiment cụ thể. Cầu của bạn nhận hai số thực mỗi nhịp. Action kiểu RT-1 gói tay, đế và kẹp thành một lệnh rời rạc cho một nền có các khớp đó. Kể cả khi hai bin rời rạc là "đế tiến" và "đế yaw", mép bin được chọn cho robot của họ, chiều cao camera của họ, và chiều dài cơ sở bánh của họ. Ánh xạ bin 7 thành $$v = 0.2$$ m/s là một bộ điều khiển mới bạn phải thiết kế và thử với bánh nhấc lên. Nó không phải tính chất của checkpoint. Checkpoint chưa thấy `observation.images.cam` của bạn, cũng chưa thấy timeout 300 ms của bạn.

Ô laptop của RT-2, để câu trả lời kỳ vọng hiện ra trước khi bạn chép: train RT-2 ở nhà là không. Tinh chỉnh chung các xương sống vision-language mà các bài đó xuất phát không phải việc của máy lớp học. Đọc [arXiv:2307.15818](https://arxiv.org/abs/2307.15818) là toàn bộ bài nếu bạn chọn cột đó.

## Lab

Chọn **hai** hệ trong danh sách: RT-2, Open X-Embodiment, OpenVLA, pi0. Đừng chọn RT-1. Dòng đó là ví dụ đã làm. Mở các trang, không mở file trọng số.

- RT-2: [arXiv:2307.15818](https://arxiv.org/abs/2307.15818)
- Open X-Embodiment: [robotics-transformer-x.github.io](https://robotics-transformer-x.github.io/)
- OpenVLA: [arXiv:2406.09246](https://arxiv.org/abs/2406.09246) và [openvla.github.io](https://openvla.github.io/)
- pi0: [physicalintelligence.company/blog/pi0](https://www.physicalintelligence.company/blog/pi0)

Chép dòng tiêu đề bảng vào `lab-notes.md` và thêm hai dòng của bạn.

| Hệ | Đầu vào | Không gian action | `Twist` trên đồ thị của bạn, hay đích khớp? | Laptop tối nay? |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |
|  |  |  |  |  |

**Kỳ vọng.** Hai dòng đã điền. Đầu vào nhắc ảnh và chữ ở chỗ trang có nhắc. Ô không gian action nêu một thân không phải Capstone, hoặc nói thẳng robot trên trang không phải của bạn. Ô Twist là không đối với `cmd_vel` của bạn, kể cả khi robot kia có bánh. Nếu một trong hai dòng là RT-2, ô laptop nói không với việc train ở nhà, bằng các chữ đó hoặc chữ thẳng hơn. Ô viết "có lẽ với Colab" là một chữ không mà bạn chưa viết xong. Khóa học này cũng không giao một lần train trên máy thuê.

**Các kiểu hỏng**

| Bảng nói | Sai ở đâu |
| --- | --- |
| "Có xuất bản `Twist`" vì RT-1 có đế di động | Kênh đế của họ không phải topic của bạn, đơn vị của bạn, hay khoảng cách hai bánh của bạn |
| "Trọng số mở, nên tối nay train được" ở dòng OpenVLA | Trọng số mở cho bạn đọc một tên file. Chúng không thu một job luyện nhiều tỉ tham số xuống laptop không GPU, và suy luận đúng tần số điều khiển trên máy đó cũng là không |
| "Open X-Embodiment có nhiều robot, nên Capstone được phủ" | Phủ nghĩa là cảm biến của bạn và vector action của bạn có trong dữ liệu, với lượng đủ. Một câu trên trang dự án không phải điều đó |
| "Chỉ dẫn là stop, nên timeout không quan trọng" | Timeout không thấy chuỗi. Nó thấy khung serial. Policy còn xuất bản thì động cơ còn được cấp |
| Bất kỳ dòng nào ô cuối là có đối với train | Viết lại. Đọc thì có. Train các hệ này ở nhà thì không |

## Mua sắm

Không món mua nào phục vụ bài này. Đừng mua kẹp, bo hạng Jetson, hay máy thứ hai vì một demo VLA có nhiều camera hơn bạn. Camera tùy chọn ở chương 11 đã là phần bàn về ảnh của khóa học. Camera trên Capstone vẫn không biến đế thành robot bên trong RT-1 hay OpenVLA.

## Bài tập

1. Bảng của bạn có RT-2. Viết ô laptop thành một câu đầy đủ, rồi thêm việc bạn được phép làm với PDF. Gợi ý: train ở nhà là không, kể cả một notebook mượn mà bạn hy vọng là đủ lớn. Bạn được trích abstract.
2. Trọng số OpenVLA là công khai. Vì sao "công khai" không trùng "chạy trên chiếc laptop đã nạp ESP32"? Gợi ý: mạng là một VLA nhiều tỉ tham số. Laptop không có GPU. Điều khiển muốn một lệnh mỗi 20 ms. Nạp một file trọng số không phải vòng lặp đó.
3. Một bạn học ánh xạ bit "mở" của kẹp sang $$\omega$$. Capstone làm gì lần đầu policy mở kẹp? Gợi ý: nó quay, vì bạn đã đặt một kênh không liên quan lên vận tốc góc. Dataset card bài 12-01 đã từ chối phép đặt tên đó bằng cách ghi đơn vị.
4. Người vận hành gõ "stop" và node policy vẫn xuất bản $$v = 0.15$$ mỗi 20 ms. Watchdog 300 ms có nổ không? Dây nào thực sự dừng bánh? Gợi ý: watchdog không nổ. Bạn cần số 0 trên khung serial, hoặc ngắt phần cứng. Chuỗi không nằm trên dây đó.
5. Nêu một đầu vào mà Open X-Embodiment không bịa hộ bạn được. Gợi ý: tư thế camera nhìn trước trên Capstone, khoảng cách hai bánh, và một vector action chỉ có $$(v, \omega)$$. Một hồ robot khác không đo các thứ đó.

## Đọc thêm

- [Trang RT-1](https://robotics-transformer1.github.io/) và [bài RT-1](https://arxiv.org/abs/2212.06817).
- [RT-2](https://arxiv.org/abs/2307.15818).
- [Open X-Embodiment](https://robotics-transformer-x.github.io/).
- [OpenVLA](https://arxiv.org/abs/2406.09246) và [trang dự án](https://openvla.github.io/).
- [pi0, Physical Intelligence](https://www.physicalintelligence.company/blog/pi0).
