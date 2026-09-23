---
layout: post
title: "Lộ trình tiếp theo và tài liệu"
chapter: "12"
order: 5
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter12
lesson_type: required
draft: false
---

Thời lượng: **~60 phút**. Mười phút với hình, hai mươi phút chọn một hướng, ba mươi phút viết kế hoạch một tháng mà đọc lại được mà không mua gì tối nay.

## Mục tiêu

Bạn chọn một hướng cho tháng tới, không chọn ba. Hướng A ở lại đế ngoài hiện trường: Nav2, lidar khi bạn sẵn sàng, và linorobot2 như một stack vi sai để đọc, trong khi cầu của chính bạn vẫn là đường ra động cơ. Hướng B là cánh tay và dataset LeRobot, chỉ khi sau này bạn tự quyết định mua phần cứng. Hướng C là lý thuyết: Modern Robotics, sách miễn phí, và khóa manipulation của MIT. Bạn viết một kế hoạch nêu đúng Capstone bạn đang có và một thói quen an toàn bạn sẽ không bỏ. Bạn để danh mục tài liệu là một bản đồ, không phải năm bài báo phải xong trong một cuối tuần.

## Kiến thức cần trước

Chương 08 đến 11 nằm sau lưng trong trình tự khóa học, kể cả khi vài lab còn thô. Bạn nói được timeout 300 ms làm gì, `cmd_vel` mang gì, và vì sao policy của một kẹp khác không phải bộ điều khiển cho bánh của bạn. Bạn có thói quen dataset card từ bài 12-01. Bạn không cần bo mới, cảm biến mới, hay một bản build Nav2 sạch để viết kế hoạch. Kế hoạch đi trước để tab mua sắm không viết hộ.

## Vì sao bài này nằm trên lộ trình

Khóa học đi từ một khung vi sai bạn cầm được tới một đồ thị Jazzy bạn vẽ được, rồi tới một chồng bài báo phát action cho những robot bạn không có. Cái kết trung thực là một tháng với một sợi chỉ. Một cuối tuần mở RT-2, Diffusion Policy, một tutorial Nav2, một listing kẹp và một listing Jetson thì không xong cái nào, và tiêu khoản tiền đáng lẽ ở lại với đế cho đến khi timeout trở nên nhàm. Dòng cuối của hình là bài tập: một hướng trong một tháng hơn năm bài báo trong một cuối tuần. Dòng phía trên là ràng buộc trên mọi hướng: timeout, đơn vị, sổ ghi, và một công tắc nguồn vẫn áp dụng.

## Khái niệm

Ba hướng. Bạn sẽ viết một hướng vào lab. Bạn vẫn cần nhận ra hai hướng kia, để một bài trên diễn đàn không kéo bạn sang ngang ở tuần đầu.

**Hướng A, đế ngoài hiện trường.** Bạn đã có robot. Kỹ năng tiếp theo là những thứ chương 11 đã tour và chưa làm xong: một bản đồ, một planner, một controller, trên ROS 2 Jazzy. Tutorial khớp distro là [hướng dẫn bắt đầu Nav2 cho Jazzy](https://docs.nav2.org/jazzy/getting_started/). Lidar 360° nhỏ là cảm biến các tutorial đó chờ, một `LaserScan`, không phải cảm biến một điểm. Khoảng giá cho các máy nhỏ là 1,5–3,5 triệu đồng, và hãy đối listing khi bạn thực sự sắp mua. Mua tuần này không phải điều kiện để chọn hướng. [linorobot2](https://github.com/linorobot/linorobot2) là một stack vi sai công khai bạn đọc như tài liệu tham chiếu: một launch bringup, một URDF, và một config Nav2 ngồi cạnh nhau thế nào. Bạn không thay firmware của mình bằng repository đó. Cầu của bạn, khung serial của bạn, và timeout 300 ms ở lại. Nếu một config linorobot2 xuất bản `cmd_vel` vào một driver bạn chưa đọc, bạn có hai bên cùng viết động cơ. Một bên viết, là bạn, với timeout nằm trong cùng tiến trình ghi PWM.

**Hướng B, cánh tay và dữ liệu.** LeRobot, từ bài 12-01, là cửa phần mềm khi bạn quyết định muốn demonstration trong không gian khớp. Hạng SO-100, Koch và LeKiwi là thân của dự án, không phải Capstone. Chọn hướng này cho một tháng sau nghĩa là có dataset card trước khi trả tiền: khóa, đơn vị, fps, và timeout vẫn nằm trong firmware của bất kỳ đế nào cánh tay được bắt lên. Nó không nghĩa là một cánh tay, một lidar và một máy thứ hai đến cùng lúc. Cánh tay là hướng tùy chọn đắt. Một kit leader-follower đầy đủ thường nhiều triệu đồng sau servo và ship. Các ghi chú này vẫn không bịa URL shop. Chưa gọi được tên vector action bạn sẽ ghi thì bạn chưa sẵn sàng mở tab mua.

**Hướng C, lý thuyết.** [Modern Robotics](https://hades.mech.northwestern.edu/index.php/Modern_Robotics) (Lynch và Park) miễn phí trên trang đó. Một tháng là một chương bạn nối được với đế, không phải cả cuốn. Phần robot bánh là chương nói thẳng $$v$$ và $$\omega$$. Hãy chép đúng tiêu đề bạn thấy trên trang vào kế hoạch, để bạn đi theo trang, không đi theo trí nhớ mục lục. [Khóa manipulation của MIT](https://manipulation.csail.mit.edu/) là nửa kia của hướng này: ghi chú về bàn tay, tiếp xúc, và lập kế hoạch, giải thích vì sao các bài VLA quan tâm những kẹp bạn không sở hữu. Đọc như ghi chú. Mua một cánh tay 6 bậc tự do để "theo video" là món mua của hướng B, lấy lý do của hướng C, và đó là cách một tháng sụp.

Kiểu hỏng của chính bài này, nêu ra để bạn thấy trước: một cánh tay 6 bậc, một lidar, và một bo hạng Jetson trong cùng một tuần. Ba đường học, một ví, và Capstone vẫn là robot duy nhất có timeout bạn đã thử. Jetson không xóa timeout. Lidar không xóa timeout. Cánh tay không xóa timeout trên những bánh mà cánh tay ngồi lên. Món có thể chờ thì hãy chờ.

Các thói quen an toàn không tùy chọn trên hướng nào:

- Timeout lệnh 300 ms ở lại trong firmware bạn nạp.
- Lần chuyển động đầu của bất kỳ publisher mới nào là bánh nhấc lên, hoặc khung trên giá, cho đến khi lệnh đúng là lệnh bạn nghĩ.
- E-stop phần cứng hoặc công tắc nguồn tay với tới mà không cần bàn phím luôn nằm trong tầm. Policy, planner, và chữ "stop" đã gõ đều có thể hỏng trong lúc node còn sống.

Đơn vị cũng ở lại trên lộ trình. Hướng A nói `Twist`. Hướng B sẽ nói đích khớp vào cái ngày cánh tay tồn tại, và các đích đó không được ghi đè $$v$$ và $$\omega$$ trong cùng một cột. Đạo hàm của hướng C chỉ có ích nếu bạn vẫn biết số nào là radian trên giây trên dây.

## Hình

![Ba hướng cho tháng tới]({{ site.imgurl }}/generated/ch12_paths.png)

Ba hộp, một tháng, một lựa chọn. Hộp xanh lá là đế hiện trường: Nav2, lidar, linorobot2 để tham chiếu. Hộp vàng là cánh tay và dữ liệu: LeRobot và cánh tay hạng SO-100, để sau. Hộp xanh dương là lý thuyết: Modern Robotics và khóa MIT. Phía dưới: timeout, đơn vị, sổ ghi, và công tắc nguồn vẫn áp dụng trên mọi hướng. Dòng đậm là nhịp. Bạn được đọc tiêu đề một bài báo trên hướng bạn không chọn. Bạn không được biến bài đó thành dự án thứ hai.

## Ví dụ đọc có số

Một kế hoạch trông đầy mà rỗng:

```text
path: A và một chút B, và tôi sẽ lướt RT-2
robot: cái gì đó có bánh, có khi mua cái mới
safety: cẩn thận
buy: lidar, arm, board
```

Một kế hoạch kiểm được:

```text
path: A
robot I already have: Capstone diff-drive, cái có cầu serial
safety habit I will not drop: 300 ms không có khung mới thì v = 0 và w = 0
also still true: bánh nhấc lên trước publisher mới; công tắc nguồn trong tầm tay
this month I will not buy: một cánh tay, một bo hạng Jetson
first page I will open: https://docs.nav2.org/jazzy/getting_started/
lidar: không phải tuần này. Nếu một tháng nữa đế vẫn bám cmd_vel, đối lại lidar 360 nhỏ trong khoảng 1,5–3,5 triệu đồng
reference I will read and not flash over my firmware: https://github.com/linorobot/linorobot2
```

Kế hoạch thứ hai nêu một hướng, một robot bạn chỉ được, và một thói quen có con số. "Cẩn thận" không phải thói quen. Ngưỡng 300 ms thì phải. Dòng linorobot2 nói repository dùng để làm gì. Nó là tài liệu để đọc. Nó không phải bản thay cầu.

Khoảng giá, để dòng "không phải tuần này" có thước. Lidar 360° nhỏ nằm khoảng 1,5–3,5 triệu đồng. Đối lại, vì listing dịch. Raspberry Pi 5, nếu hướng A mọc quá laptop, khởi điểm gần 2,4 triệu đồng cho bản RAM thấp tại [listing Pi 5 lắp ráp tại Anh trên Hshop](https://hshop.vn/may-tinh-raspberry-pi-5-made-in-uk). RAM nhiều thì đắt hơn. Đối biến thể trên trang. Cánh tay là hướng tùy chọn đắt và cố ý không ghi giá ở đây. Cộng cả ba vào một giỏ là đúng kiểu hỏng. Ứng viên phần cứng duy nhất của hướng A trong tháng, và chỉ sau khi đế đã đáng tin, là lidar hoặc Pi, không phải cả hai trong ngày đầu, và không đứng cạnh một cánh tay.

## Lab

Viết kế hoạch vào `lab-notes.md` thành một khối bạn theo được bốn tuần. Các dòng bắt buộc:

```text
path: A hoặc B hoặc C
robot I already have: Capstone diff-drive
safety habit I will not drop: <một trong: timeout 300 ms, bánh nhấc lên ở lần chạy đầu, E-stop phần cứng>
this month I will not buy:
first link I will actually open:
what I will have in my notes after week one:
```

Bằng chứng tuần một của hướng A là một câu về trang Nav2 bạn đã mở và phần nào của linorobot2 bạn từ chối chép đè lên driver động cơ. Bằng chứng tuần một của hướng B là một dataset card cho cánh tay bạn chưa có, đơn vị khớp ghi "chưa biết cho đến datasheet servo", và một dòng tường minh rằng $$v$$ và $$\omega$$ của Capstone ở lại khóa riêng. Bằng chứng tuần một của hướng C là một tiêu đề chương hoặc bài giảng chép từ Modern Robotics hoặc từ trang khóa MIT, cộng một phương trình hoặc một định nghĩa bạn nối được với đế. Chưa nối được thì viết câu hỏi bạn sẽ hỏi tuần sau. Đừng bịa tiêu đề. Tên chương trên trang khác trí nhớ thì trang thắng.

**Kỳ vọng.** Đúng một chữ hướng. Dòng robot nói Capstone, không nói "một robot di động". Dòng an toàn là một thói quen cụ thể, và timeout 300 ms hoặc chính là thói quen đó, hoặc vẫn được ghi là còn hiệu lực. Dòng "sẽ không mua" gồm ít nhất hai món không nằm trên hướng của bạn. Không có ảnh giỏ hàng.

**Các kiểu hỏng**

| Kế hoạch | Vấn đề |
| --- | --- |
| Hướng "A+B+C, nhẹ thôi" | Đó là cuối tuần năm bài báo đội lốt. Chọn một chữ |
| Việc đầu tiên là một cánh tay, một lidar và một Jetson trong một đơn | Bạn đã mua ba hướng. Lab xin một tháng trên một hướng |
| Hướng C, và timeout "không liên quan vì tôi chỉ đọc" | Đọc không xóa firmware trên robot ở góc phòng. Thói quen còn hiệu lực lần nạp tới |
| linorobot2 được nạp làm driver động cơ ở ngày thứ hai | Bạn thay một timeout bạn hiểu bằng một stack bạn chưa đọc. Hãy đọc. Giữ cầu của bạn |
| Ghi chú tuần một là "xem vài video" | Nêu trang và đoạn bạn sẽ tóm tắt được |

## Bài tập

Mỗi câu trả lời nêu một hướng. Một câu áp được cho cả ba hướng là chưa xong.

1. Hướng A. Nêu một thứ bạn sẽ chép từ việc đọc linorobot2, và một thứ bạn sẽ không thay. Gợi ý: thứ đáng chép là hình dạng một launch bringup, hoặc cách URDF đặt tên `base_link`. Thứ không thay là cầu serial của bạn và ngưỡng 300 ms trong firmware ghi PWM. "Tôi sẽ dùng stack của họ" là câu sai.
2. Hướng B. Viết các khóa action bạn sẽ đòi thấy trước khi trả tiền cho một cánh tay hạng SO-100. Gợi ý: tên khớp, đơn vị từ datasheet servo (radian hoặc số đếm encoder, không phải một cái nhún vai), fps, và một khóa camera. Thêm một dòng rằng $$v$$ và $$\omega$$ của Capstone vắng mặt trong các cột khớp đó. Chưa viết được khóa thì hướng này là tháng sau.
3. Hướng C. Từ trang Modern Robotics, nêu phần robot bánh bạn sẽ mở, dùng đúng tiêu đề in trên trang, và nói đại lượng Capstone nào phần đó phải giải thích. Gợi ý: nó phải giải thích $$v$$ và $$\omega$$, hoặc quan hệ giữa tốc độ bánh và cặp đó. Lần bấm đầu rơi vào chương về nắm thì nói vậy và chuyển. Được phép lấy trang khóa MIT thay vào, nếu bạn trích tiêu đề bài giảng và vẫn nêu $$v$$ cùng $$\omega$$ là thứ bạn không quên.
4. Ngân sách hướng A. Bạn chưa đáng mua lidar chừng nào `cmd_vel` trên đế thật chưa làm đúng điều cầu tuyên bố, bánh chạm đất, timeout đã được chứng minh. Khoảng VND nào bạn sẽ đối khi ngày đó đến, và bạn làm gì nếu listing cao hơn khoảng? Gợi ý: 1,5–3,5 triệu đồng cho máy 360° nhỏ. Listing cao hơn khoảng thì bạn chờ, hoặc bạn chủ đích chọn một hạng cảm biến khác. Bạn không "mua cho đủ bộ" bằng một cánh tay.
5. Với đúng hướng bạn đã chọn trong lab, viết phép kiểm tuần bốn thành một câu hỏi có/không mà sổ ghi trả lời được. Gợi ý: hướng A, "Tôi chỉ được trang Nav2 nuốt `cmd_vel` của tôi, và dòng firmware vẫn timeout ở 300 ms, chứ?" Hướng B, "Dataset card dùng một hệ đơn vị, và tháng này tôi không mua gì, chứ?" Hướng C, "Tôi phát biểu lại được quan hệ bánh tôi đã chép, và timeout vẫn nằm trong firmware lần nạp cuối, chứ?" Chọn câu khớp chữ của bạn.

## Tài liệu tuyển

Các link khóa học thực sự dùng, gom lại để tháng sau không phụ thuộc một lần tìm kiếm. Mở cái khớp hướng của bạn. Các cái còn lại chỉ lướt tiêu đề.

**Stack bạn đã bắt đầu**

- [Tài liệu ROS 2 Jazzy](https://docs.ros.org/en/jazzy/)
- [Nav2 bắt đầu, Jazzy](https://docs.nav2.org/jazzy/getting_started/)
- [Cài Gazebo cùng ROS, Harmonic](https://gazebosim.org/docs/harmonic/ros_installation). Simulator đi cặp với Jazzy trong hướng dẫn đó là Gazebo Harmonic.
- [slam_toolbox](https://github.com/SteveMacenski/slam_toolbox)
- [linorobot2](https://github.com/linorobot/linorobot2), stack vi sai để tham chiếu. Giữ cầu của bạn.

**Thư viện và bài báo, để đọc**

- [Docs LeRobot](https://huggingface.co/docs/lerobot/index) và [huggingface/lerobot](https://github.com/huggingface/lerobot)
- [Zhao và cộng sự, ACT, arXiv:2304.13705](https://arxiv.org/abs/2304.13705)
- [Chi và cộng sự, Diffusion Policy, arXiv:2303.04137](https://arxiv.org/abs/2303.04137) và [trang dự án](https://diffusion-policy.cs.columbia.edu/)
- [RT-1](https://robotics-transformer1.github.io/) và [arXiv:2212.06817](https://arxiv.org/abs/2212.06817)
- [RT-2, arXiv:2307.15818](https://arxiv.org/abs/2307.15818)
- [Open X-Embodiment](https://robotics-transformer-x.github.io/)
- [OpenVLA, arXiv:2406.09246](https://arxiv.org/abs/2406.09246) và [openvla.github.io](https://openvla.github.io/)
- [pi0](https://www.physicalintelligence.company/blog/pi0)

**Lý thuyết, đọc miễn phí**

- [Modern Robotics](https://hades.mech.northwestern.edu/index.php/Modern_Robotics)
- [MIT manipulation](https://manipulation.csail.mit.edu/)

**Một máy tính, chỉ khi hướng A mọc quá laptop**

- [Raspberry Pi 5 trên Hshop](https://hshop.vn/may-tinh-raspberry-pi-5-made-in-uk). Bản RAM thấp từng được liệt kê từ khoảng 2,4 triệu đồng. Đối lại biến thể.
