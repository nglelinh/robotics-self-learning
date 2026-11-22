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

Thời lượng: **~60 phút** (10 phút xem sơ đồ định hướng, 20 phút chọn một hướng duy nhất và 30 phút lập kế hoạch thực hành một tháng mà chưa cần mua sắm thêm).

## Mục tiêu

Sau bài học này, bạn sẽ chọn **duy nhất một** hướng phát triển cho tháng tới thay vì dàn trải cả ba: **Hướng A** phát triển tiếp khung xe hiện có (Nav2, lidar khi sẵn sàng, tham khảo `linorobot2` nhưng vẫn giữ nguyên cầu nối động cơ của mình); **Hướng B** tìm hiểu cánh tay robot và tập dữ liệu LeRobot (chỉ đầu tư phần cứng khi bạn chủ động quyết định về sau); hoặc **Hướng C** đào sâu lý thuyết với sách miễn phí *Modern Robotics* và khóa học *Manipulation* của MIT. Bạn sẽ viết ra một kế hoạch cụ thể gắn với chiếc Capstone sẵn có kèm cam kết duy trì các thói quen an toàn, đồng thời sử dụng danh mục tài liệu cuối bài như bản đồ tra cứu dài hạn.

## Kiến thức cần trước

Đã đi qua trình tự chương 08 đến chương 11 (kể cả khi một vài bài lab thực tế còn dang dở): bạn hiểu vai trò watchdog 300 ms, cấu trúc `/cmd_vel`, lý do policy của tay kẹp khác không áp được cho bánh xe Capstone và cách viết dataset card ở bài 12-01. Bạn không cần mạch mới, cảm biến mới hay bản build Nav2 hoàn chỉnh để lập kế hoạch — chính kế hoạch rõ ràng sẽ giúp bạn tránh mua sắm cảm tính.

## Vì sao bài này nằm trên lộ trình

Khóa học đã đưa bạn đi từ khung xe vi sai thực tế, qua đồ thị ROS 2 Jazzy và mô phỏng Gazebo, đến việc đọc hiểu các bài báo học máy hiện đại. Bước chuyển tiếp hiệu quả nhất là tập trung theo đuổi một chủ đề duy nhất trong một tháng, thay vì mở cùng lúc quá nhiều bài báo, hướng dẫn và giỏ hàng phần cứng trong một cuối tuần mà không hoàn thiện được mục tiêu nào. Dù chọn hướng nào, các nguyên tắc nền tảng (watchdog, thống nhất đơn vị, ghi chép sổ thực hành và công tắc nguồn phần cứng) vẫn luôn giữ nguyên hiệu lực.

## Khái niệm

Dưới đây là ba hướng đi để bạn chọn một cho kế hoạch tháng tới, đồng thời hiểu rõ hai hướng còn lại để không bị phân tâm giữa chừng:

**Hướng A — Phát triển xe di động thực tế.** Tận dụng ngay khung xe Capstone sẵn có để hoàn thiện những phần mới tham quan ở chương 11: dựng bản đồ, lập kế hoạch và bám quỹ đạo trên ROS 2 Jazzy theo [hướng dẫn bắt đầu Nav2 cho Jazzy](https://docs.nav2.org/jazzy/getting_started/). Cảm biến phù hợp khi bạn sẵn sàng là lidar quét 360° cỡ nhỏ (phát `LaserScan`, giá tham khảo khoảng 1,5–3,5 triệu đồng — tự kiểm tra giá mới nhất khi mua; không bắt buộc mua ngay tuần này). Kho mã nguồn [linorobot2](https://github.com/linorobot/linorobot2) là tài liệu tham khảo hữu ích để xem cách tổ chức tệp launch bringup, URDF và cấu hình Nav2 cho xe vi sai. Tuy nhiên, không nạp đè firmware của dự án đó lên mạch của bạn: giữ nguyên cầu nối serial, khung dữ liệu và watchdog 300 ms để đảm bảo chỉ có duy nhất một tầng điều khiển ghi xung PWM.

**Hướng B — Cánh tay robot và dữ liệu LeRobot.** Khi bạn muốn thực hành học bắt chước trong không gian khớp, LeRobot (bài 12-01) là điểm xuất phát với các mẫu phần cứng như SO-100/SO-101, Koch và LeKiwi. Chọn hướng này đồng nghĩa bạn hoàn thiện dataset card (tên khóa, đơn vị, `fps`) trước khi chi tiền. Cánh tay là nhánh tùy chọn có chi phí cao (một bộ kit leader-follower đầy đủ gồm servo và vận chuyển thường ở mức nhiều triệu đồng); không nên mua dồn dập cùng lúc cả cánh tay, lidar lẫn máy tính phụ khi chưa chốt rõ vector hành động cần thu thập.

**Hướng C — Củng cố nền tảng lý thuyết.** Giáo trình [Modern Robotics](https://hades.mech.northwestern.edu/index.php/Modern_Robotics) (Lynch và Park) được phát hành miễn phí trực tuyến. Trong một tháng, hãy chọn đúng một chương liên kết trực tiếp với xe bánh (nơi phân tích rõ $$v$$ và $$\omega$$) và chép chính xác tiêu đề từ trang web vào kế hoạch. Nửa còn lại là [Khóa manipulation của MIT](https://manipulation.csail.mit.edu/) giúp hiểu sâu về thao tác tay máy, tiếp xúc cơ học và lập kế hoạch — lý giải vì sao các bài báo VLA tập trung nhiều vào tay kẹp. Hãy đọc theo hướng lý thuyết thuần túy, tránh lấy lý do học hướng C để mua phần cứng của hướng B.

Sai lầm phổ biến nhất ở giai đoạn này là đặt mua cùng lúc cánh tay 6 bậc, lidar và mạch Jetson trong một tuần — dàn trải ngân sách ra ba hướng trong khi chưa khai thác hết chiếc Capstone sẵn có. Những thói quen an toàn bắt buộc phải giữ trên mọi hướng gồm:

- Duy trì watchdog 300 ms trong firmware nạp trên vi điều khiển.
- Luôn nhấc bánh khỏi mặt sàn (hoặc đặt khung lên giá đỡ) ở lần chạy thử đầu tiên của bất kỳ publisher mới nào.
- Luôn đặt công tắc nguồn phần cứng hoặc E-stop trong tầm tay với để ngắt trực tiếp khi cần, không phụ thuộc bàn phím hay phần mềm.

Bên cạnh đó, tính nhất quán về đơn vị luôn được giữ vững: Hướng A dùng `Twist` (m/s, rad/s), Hướng B dùng góc khớp theo datasheet servo (không ghi đè cột $$v, \omega$$), còn các công thức ở Hướng C luôn đối chiếu về đúng đơn vị vật lý trên dây truyền.

## Hình

![Ba hướng cho tháng tới]({{ site.imgurl }}/generated/ch12_paths.png)

Sơ đồ tóm tắt ba hướng lựa chọn cho một tháng (xanh lá: xe hiện trường với Nav2/lidar/linorobot2; vàng: cánh tay và dữ liệu LeRobot; xanh dương: lý thuyết Modern Robotics và MIT), đặt trên nền tảng chung gồm watchdog, đơn vị, sổ ghi chép và công tắc nguồn. Bạn có thể đọc lướt tiêu đề các hướng khác để biết thêm, nhưng không biến chúng thành dự án song song thứ hai.

## Ví dụ đọc có số

So sánh một bản kế hoạch chung chung (khó kiểm chứng):

```text
path: A và một chút B, và tôi sẽ lướt RT-2
robot: cái gì đó có bánh, có khi mua cái mới
safety: cẩn thận
buy: lidar, arm, board
```

với một bản kế hoạch cụ thể và kiểm chứng được:

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

Bản kế hoạch thứ hai chốt duy nhất một hướng, chỉ rõ phần cứng sẵn có, nêu thói quen an toàn bằng con số cụ thể (300 ms thay vì nói chung "cẩn thận") và xác định rõ `linorobot2` chỉ để tham khảo kiến trúc.

Khung giá tham khảo để cân nhắc cho Hướng A (chỉ mua khi xe hiện tại đã vận hành ổn định, không mua dồn trong ngày đầu): lidar 360° nhỏ khoảng 1,5–3,5 triệu đồng; Raspberry Pi 5 (nếu cần tách khỏi laptop) khởi điểm gần 2,4 triệu đồng cho bản RAM thấp tại [listing Pi 5 lắp ráp tại Anh trên Hshop](https://hshop.vn/may-tinh-raspberry-pi-5-made-in-uk) (kiểm tra lại giá biến thể thực tế); cánh tay là nhánh đắt tiền nên không ghép chung giỏ hàng với Hướng A.

## Lab

Viết bản kế hoạch bốn tuần của bạn vào `lab-notes.md` theo đầy đủ các trường bắt buộc sau:

```text
path: A hoặc B hoặc C
robot I already have: Capstone diff-drive
safety habit I will not drop: <một trong: timeout 300 ms, bánh nhấc lên ở lần chạy đầu, E-stop phần cứng>
this month I will not buy:
first link I will actually open:
what I will have in my notes after week one:
```

Sản phẩm kiểm chứng sau tuần đầu tiên theo từng hướng:
- **Hướng A:** một nhận xét về trang tài liệu Nav2 đã mở và nêu rõ thành phần nào của `linorobot2` bạn không sao chép đè lên driver động cơ.
- **Hướng B:** một dataset card cho cánh tay dự kiến (ghi rõ đơn vị khớp "chờ xác nhận từ datasheet servo") cùng cam kết tách riêng khóa $$(v, \omega)$$ của Capstone.
- **Hướng C:** tiêu đề chương hoặc bài giảng trích chính xác từ *Modern Robotics* hoặc khóa MIT kèm một phương trình/định nghĩa liên hệ trực tiếp với khung xe Capstone (nếu chưa liên hệ được, ghi rõ câu hỏi cần giải đáp cho tuần sau).

**Kết quả mong đợi:** chỉ chọn duy nhất một chữ cái hướng (A, B hoặc C), ghi đích danh `Capstone diff-drive`, nêu rõ thói quen an toàn cụ thể (vẫn duy trì watchdog 300 ms), liệt kê ít nhất hai món sẽ *không* mua trong tháng này và không kèm ảnh giỏ hàng.

**Các lỗi thường gặp**

| Sai sót trong kế hoạch | Vấn đề |
| --- | --- |
| Ghi "chọn A + B + C nhẹ nhàng" | Thực chất là dàn trải không trọng tâm; bắt buộc chọn một hướng duy nhất |
| Bước đầu tiên là đặt mua cả cánh tay, lidar và Jetson | Gộp ba hướng thành một đơn hàng, trái mục tiêu tập trung một tháng |
| Chọn Hướng C rồi ghi watchdog "không liên quan vì chỉ đọc sách" | Đọc lý thuyết không làm thay đổi firmware đang nạp sẵn trên robot; quy tắc an toàn vẫn giữ nguyên |
| Nạp luôn firmware `linorobot2` đè lên driver động cơ ngay ngày thứ hai | Thay thế cơ chế watchdog bạn nắm rõ bằng mã nguồn chưa đọc kỹ; chỉ dùng để tham khảo |
| Mục tiêu tuần một chỉ ghi "xem vài video" | Thiếu đầu ra kiểm chứng; cần nêu cụ thể trang tài liệu và nội dung sẽ tóm tắt |

## Video tham khảo

- **Xem trước:** [Core Concepts: Imitation Learning](https://www.youtube.com/watch?v=GDmhrAHxgQE) — Sanjiban Choudhury (tiếng Anh). Nền tảng lý thuyết cần nắm nếu bạn cân nhắc hướng học bắt chước trước khi đầu tư cánh tay.
- [π0: A Foundation Model for Robotics with Sergey Levine - 719](https://www.youtube.com/watch?v=5mY71rGXAkM) — The TWIML AI Podcast with Sam Charrington (tiếng Anh). Mở rộng góc nhìn về mô hình nền tảng trong robotics (nằm ngoài phạm vi thực hành 24 tuần của khóa).

## Bài tập

Mỗi câu hỏi tương ứng với một hướng cụ thể (không viết câu trả lời chung chung dùng cho cả ba hướng):

1. **Hướng A:** Nêu một thành phần bạn có thể học hỏi từ `linorobot2` và một thành phần tuyệt đối giữ nguyên của riêng mình. *Gợi ý:* học cách tổ chức tệp launch bringup hoặc quy ước đặt tên `base_link` trong URDF; giữ nguyên cầu nối serial và watchdog 300 ms trên firmware.
2. **Hướng B:** Liệt kê các khóa dữ liệu hành động bắt buộc phải làm rõ trước khi đặt mua cánh tay hạng SO-100. *Gợi ý:* tên từng khớp, đơn vị từ datasheet servo (radian hoặc xung encoder), `fps`, khóa camera và xác nhận không trộn $$(v, \omega)$$ của Capstone vào các cột khớp này.
3. **Hướng C:** Tra cứu trang *Modern Robotics* (hoặc khóa MIT), trích chính xác tiêu đề phần liên quan đến robot bánh xe và nêu rõ đại lượng nào của Capstone được giải thích trong phần đó. *Gợi ý:* liên hệ trực tiếp với $$v$$, $$\omega$$ và mối quan hệ với vận tốc hai bánh.
4. **Ngân sách Hướng A:** Chỉ khi xe Capstone thực sự bám ổn định `/cmd_vel` dưới sàn và watchdog đã kiểm chứng, bạn mới xét mua lidar. Khung giá tham khảo cho lidar 360° nhỏ là bao nhiêu và bạn xử lý thế nào nếu giá niêm yết vượt khung? *Gợi ý:* 1,5–3,5 triệu đồng; nếu vượt khung thì chờ hoặc đổi phân khúc cảm biến phù hợp chứ không chuyển sang mua cánh tay cho "đủ bộ".
5. Với đúng hướng bạn đã chọn trong lab, viết một câu hỏi Có/Không làm tiêu chí tự kiểm tra cuối tuần thứ tư dựa trên sổ ghi chép. *Gợi ý:* Hướng A về việc Nav2 nối đúng `/cmd_vel` và giữ watchdog 300 ms; Hướng B về dataset card thống nhất đơn vị và chưa mua sắm vội; Hướng C về việc tự phát biểu lại quan hệ động học bánh xe trong khi vẫn duy trì watchdog trên firmware.

## Tài liệu tuyển

Tổng hợp các liên kết cốt lõi của khóa học để tra cứu dài hạn (chỉ mở sâu các mục khớp với hướng bạn chọn):

**Ngăn xếp kỹ thuật đã thực hành**

- [Tài liệu ROS 2 Jazzy](https://docs.ros.org/en/jazzy/)
- [Nav2 bắt đầu, Jazzy](https://docs.nav2.org/jazzy/getting_started/)
- [Cài Gazebo cùng ROS, Harmonic](https://gazebosim.org/docs/harmonic/ros_installation) — bộ mô phỏng tương thích trực tiếp với Jazzy.
- [slam_toolbox](https://github.com/SteveMacenski/slam_toolbox)
- [linorobot2](https://github.com/linorobot/linorobot2) — kho mã nguồn xe vi sai để tham khảo (vẫn giữ nguyên cầu nối của bạn).

**Thư viện và bài báo nghiên cứu**

- [Docs LeRobot](https://huggingface.co/docs/lerobot/index) và [huggingface/lerobot](https://github.com/huggingface/lerobot)
- [Zhao và cộng sự, ACT, arXiv:2304.13705](https://arxiv.org/abs/2304.13705)
- [Chi và cộng sự, Diffusion Policy, arXiv:2303.04137](https://arxiv.org/abs/2303.04137) và [trang dự án](https://diffusion-policy.cs.columbia.edu/)
- [RT-1](https://robotics-transformer1.github.io/) và [arXiv:2212.06817](https://arxiv.org/abs/2212.06817)
- [RT-2, arXiv:2307.15818](https://arxiv.org/abs/2307.15818)
- [Open X-Embodiment](https://robotics-transformer-x.github.io/)
- [OpenVLA, arXiv:2406.09246](https://arxiv.org/abs/2406.09246) và [openvla.github.io](https://openvla.github.io/)
- [pi0](https://www.pi.website/blog/pi0)

**Lý thuyết nền tảng (miễn phí)**

- [Modern Robotics](https://hades.mech.northwestern.edu/index.php/Modern_Robotics)
- [MIT manipulation](https://manipulation.csail.mit.edu/)

**Máy tính nhúng (chỉ cân nhắc khi Hướng A cần tách khỏi laptop)**

- [Raspberry Pi 5 trên Hshop](https://hshop.vn/may-tinh-raspberry-pi-5-made-in-uk) — bản RAM thấp từng có giá khởi điểm khoảng 2,4 triệu đồng (cần đối chiếu lại biến thể và giá hiện tại).
