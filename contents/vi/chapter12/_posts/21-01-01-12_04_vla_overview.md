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

Thời lượng: **~75 phút**, dành để đọc kỹ hai hệ thống nhằm hoàn thành bảng đối chiếu và nhận diện ba tên tuổi còn lại (không tải hay nạp checkpoint).

ACT và Diffusion Policy rất giỏi thực hiện **một kỹ năng chuyên biệt** mà chúng được dạy (ví dụ "gắp khối đỏ bỏ vào cốc"), nhưng nếu bạn đổi câu lệnh thành *"hãy đặt quả táo lên chiếc đĩa màu xanh gần nhất"*, bạn phải thu dữ liệu và huấn luyện lại từ đầu. **VLA (Vision–Language–Action)** — như RT-2, OpenVLA, $$\pi_0$$ hay SmolVLA — hợp nhất tri thức ngữ nghĩa khổng lồ của mô hình ngôn ngữ–thị giác (VLM) với đầu ra hành động liên tục của robot để hướng tới chính sách đa nhiệm hiểu ngôn ngữ tự nhiên.

## Kiến thức cần nhớ: Bốn trụ cột của Mô hình Thị giác–Ngôn ngữ–Hành động (VLA)

1. **Nền tảng VLM Tiền huấn luyện (Pretrained Vision–Language Backbone)**:
   Thừa hưởng khả năng nhận diện vật thể, màu sắc, quan hệ không gian ("bên trái", "phía sau") từ hàng tỷ cặp ảnh–văn bản trên Internet.
2. **Đầu ra Hành động (Discrete Action Token vs. Flow Matching / Diffusion Head)**:
   VLA đời đầu (như OpenVLA) lượng tử hóa mỗi chiều hành động thành 256 token rời rạc để sinh giống chữ; thế hệ mới hơn ($$\pi_0$$, SmolVLA) gắn thêm **action expert dùng Flow Matching / Diffusion** để sinh hành động liên tục mượt mà ở tần số cao.
3. **Khoảng cách Hiện thân (Embodiment Gap) & Fine-tuning**:
   Mỗi robot có số khớp, góc gắn camera và hệ tọa độ khác nhau. Do đó một mô hình VLA gốc hiếm khi chạy tốt ngay lập tức (zero-shot) trên cánh tay SO-101 của bạn mà thường cần **fine-tune (LoRA)** trên vài chục đến vài trăm tập dữ liệu đặc thù của đúng cánh tay đó.
4. **Đánh đổi Tốc độ – Kích thước (7B Parameters vs. Edge Deployment)**:
   Chạy mô hình 7 tỷ tham số ở 5–10 Hz đòi hỏi GPU mạnh (hoặc suy luận qua mạng LAN), mở ra hướng nén mô hình nhỏ gọn (SmolVLA) và suy luận bất đồng bộ.

## Mục tiêu

Sau bài học này, bạn sẽ định nghĩa được mô hình **Vision-Language-Action (VLA)** là ánh xạ từ hình ảnh kết hợp câu lệnh ngôn ngữ sang hành động của một robot cụ thể. Bạn đặt được năm hệ thống tiêu biểu — **RT-1**, **RT-2**, **Open X-Embodiment**, **OpenVLA** và **pi0** — lên cùng một khung so sánh (đầu vào, không gian hành động và mức độ tương thích với `Twist` hoặc góc khớp của Capstone/SO-101). Bạn cũng sẽ diễn giải rõ khoảng cách hình thái phần cứng (*embodiment gap*) qua ví dụ cụ thể, nắm vững nguyên tắc ưu tiên watchdog phần cứng cao hơn mọi câu lệnh ngôn ngữ và đánh giá trung thực khả năng huấn luyện tại nhà trên laptop.

## Kiến thức cần trước

Bạn biết cách đọc trang giới thiệu dự án nghiên cứu. Các bài 12-01 đến 12-03 đã trang bị kiến thức về khóa dataset, hành động dạng chunk và vấn đề đa phương án. Topic `/cmd_vel` của chương 09 vẫn mang `linear.x` (m/s) và `angular.z` (rad/s); camera ở chương 11 (nếu có) là camera gắn thân xe chứ không phải camera cổ tay trên tay kẹp song song. Bài này thiết kế cho laptop thông thường không có GPU chuyên dụng.

## Vì sao bài này nằm trên lộ trình

Với ROS 2 Jazzy, Nav2 và cầu nối serial, bạn đã có thể gửi một tọa độ đích để khung xe vi sai tự bám đường. Các nghiên cứu trong bài này tiến thêm một bước: cho phép ra lệnh bằng ngôn ngữ tự nhiên để mạng nơ-ron trực tiếp xuất lệnh điều khiển. Tuy nhiên, rất dễ hiểu lầm rằng "robot hiểu ngôn ngữ tự nhiên nên tầng firmware và kiểm soát an toàn không còn quan trọng". Thực tế, mọi checkpoint đều gắn chặt với camera và vector hành động của chính phần cứng sinh ra tập dữ liệu huấn luyện (tay máy di động của RT-1 hay tay kẹp trong Open X-Embodiment hoàn toàn khác với xe Capstone). Bài học này giúp bạn đọc các công bố VLA một cách tỉnh táo và đánh giá đúng giới hạn triển khai.

## Khái niệm

Một mô hình **Vision-Language-Action (VLA)** nhận đầu vào là hình ảnh (pixel) cùng một chuỗi chỉ dẫn ngôn ngữ (như "nhặt quả táo" hay "đi ra cửa") và xuất ra một hành động robot (dạng rời rạc hoặc liên tục). Điểm hấp dẫn là giao diện ra lệnh linh hoạt bằng ngôn ngữ tự nhiên; nhưng giới hạn cốt lõi là **hình thái phần cứng (embodiment)** nằm ngay trong bản chất trọng số mô hình — chuyển sang một phần cứng khác đồng nghĩa mô hình đang xuất lệnh cho sai động cơ.

**RT-1** (*Robotics Transformer*, Brohan và cộng sự — trang dự án [robotics-transformer1.github.io](https://robotics-transformer1.github.io/), bài báo [arXiv:2212.06817](https://arxiv.org/abs/2212.06817)) là mốc tiêu biểu theo hướng dữ liệu robot quy mô lớn. Kiến trúc transformer được huấn luyện trên tập dữ liệu mẫu lớn thu từ các robot tay máy di động của nhóm tác giả: nhận ảnh camera và câu lệnh, xuất ra vector hành động rời rạc gồm chuyển động cánh tay, đế di động và tay kẹp. Kênh di chuyển đế trong vector đó gắn với đơn vị và động học riêng của phần cứng RT-1, không phải `geometry_msgs/Twist` trên đồ thị ROS của Capstone.

**RT-2** ([arXiv:2307.15818](https://arxiv.org/abs/2307.15818)) khởi nguồn từ mô hình thị giác – ngôn ngữ (VLM) đã tiền huấn luyện trên dữ liệu web quy mô lớn, sau đó đồng tinh chỉnh (co-fine-tune) bằng cách mã hóa hành động robot thành các token trong cùng luồng ngôn ngữ. Nhờ đó mô hình có khả năng chuyển giao tri thức từ ngôn ngữ web sang kỹ năng điều khiển robot. Tuy nhiên, việc tinh chỉnh đòi hỏi hạ tầng trung tâm dữ liệu quy mô lớn chứ không thể thực hiện trên laptop cá nhân, và các token hành động vẫn gắn chặt với phần cứng cánh tay sinh dữ liệu.

**Open X-Embodiment** ([robotics-transformer-x.github.io](https://robotics-transformer-x.github.io/)) là sáng kiến hợp tác gom tập dữ liệu từ nhiều phòng thí nghiệm và nhiều mẫu robot khác nhau để huấn luyện các mô hình tổng quát (RT-X). Bài học quan trọng cho khóa này là giới hạn của sự đa dạng dữ liệu: camera cổ tay, tay kẹp song song, robot delta và xe hai bánh có góc nhìn và không gian hành động khác hẳn nhau. Chuẩn hóa tên cột trong tệp dữ liệu không làm đồng nhất động lực học vật lý — một mô hình học từ nhiều loại tay kẹp vẫn không tự động nắm được hình học camera, chiều rộng trục bánh và watchdog 300 ms của xe Capstone.

**OpenVLA** ([arXiv:2406.09246](https://arxiv.org/abs/2406.09246), trang dự án [openvla.github.io](https://openvla.github.io/)) là một mô hình VLA trọng số mở cùng hướng tiếp cận: lấy ảnh và chỉ dẫn để xuất hành động rời rạc, xây dựng từ xương sống VLM mở huấn luyện trên dữ liệu Open X-Embodiment. "Trọng số mở" cho phép nhà nghiên cứu có phần cứng phù hợp tải về kiểm thử, nhưng không có nghĩa laptop không GPU có thể huấn luyện lại hay chạy suy luận mạng nhiều tỉ tham số ở tần số 50 Hz cho vòng điều khiển serial; hơn nữa, đầu ra mặc định vẫn là chuyển động đầu cuối (end-effector) và tay kẹp chứ không phải `linear.x`, `angular.z`.

**pi0** (Physical Intelligence — đọc trực tiếp tại bài blog [pi0](https://www.pi.website/blog/pi0)) đại diện cho hướng sinh hành động liên tục bằng kỹ thuật **flow matching** (cùng họ ý tưởng với phương pháp khử nhiễu ở bài 12-03). Ảnh và ngôn ngữ đi vào, chuỗi hành động liên tục cho các robot của nhóm phát triển đi ra. Dù dùng flow matching, quỹ đạo tay kẹp vẫn không tự động biến thành lệnh cho khung xe hai bánh của bạn.

**Nguyên tắc an toàn đứng trên mọi lệnh ngôn ngữ.** Một câu lệnh chữ như `"stop"` hoàn toàn không phải nút dừng khẩn cấp (E-stop): đối với mạng nơ-ron, `"stop"` chỉ là thêm một token đầu vào; mô hình vẫn có thể xuất ra vận tốc nhỏ, hoàn thành nốt một chunk cũ hoặc phản ứng sai nếu dữ liệu huấn luyện dùng từ khóa khác. Watchdog 300 ms trên firmware cũng không đọc hiểu tiếng Anh mà chỉ giám sát khoảng nghỉ giữa các khung serial. Do đó, lệnh dừng chỉ thực sự có hiệu lực khi mã điều khiển chuyển thành PWM bằng 0, `Twist` bằng 0 hoặc công tắc nguồn phần cứng ngắt điện động cơ — và ở lần chạy thử đầu tiên của bất kỳ node mới nào, bánh xe vẫn phải nhấc khỏi mặt đất.

## Hình

![Ảnh và ngôn ngữ đi qua trọng số thành action]({{ site.imgurl }}/generated/ch12_vla.png)

Bốn khối chính biểu diễn luồng khái niệm `image + language → VLA weights → action` (không phải sơ đồ node ROS). Ghi chú màu đỏ nhấn mạnh khoảng cách phần cứng (*embodiment*) là một phần không tách rời của mô hình. Chân hình liệt kê năm hệ thống RT-1, RT-2, Open X-Embodiment, OpenVLA và pi0 với mục tiêu đọc hiểu và đối chiếu bảng, không chạy huấn luyện lại.

## Ví dụ đọc có số

Dưới đây là dòng mẫu hoàn chỉnh cho **RT-1** làm chuẩn mức độ chi tiết cho bài lab (nếu trang dự án cập nhật chi tiết mới hơn, ưu tiên theo trang dự án):

| Hệ thống | Đầu vào | Không gian hành động | Có phải `Twist` trên đồ thị của bạn hay đích khớp? | Chạy trên laptop tối nay? |
| --- | --- | --- | --- | --- |
| RT-1 | Ảnh RGB từ camera robot của nhóm tác giả kèm câu chỉ dẫn | Vector rời rạc cho tay máy di động (cánh tay, đế di động, tay kẹp) | Chuyển động đế nằm trong vector riêng của họ; không phải `/cmd_vel` hay đích khớp của Capstone | Đọc trang: có. Huấn luyện: không. Chạy suy luận trên laptop không GPU: không |

Để thấy rõ khoảng cách phần cứng: cầu nối Capstone nhận hai số thực $$(v, \omega)$$ mỗi nhịp, còn RT-1 rời rạc hóa chuyển động tay, đế và kẹp thành các mức (bin) gắn với chiều cao camera và kích thước khung xe riêng của họ. Ngay cả khi trích hai kênh đế để tự ánh xạ "bin 7 thành $$v = 0.2$$ m/s", đó đã là một bộ điều khiển hoàn toàn mới phải thử nghiệm lại với bánh nhấc khỏi sàn chứ không phải tính chất sẵn có của checkpoint.

Lưu ý thêm cho cột laptop của **RT-2**: câu trả lời trung thực cho việc huấn luyện RT-2 tại nhà là **không**, vì quá trình đồng tinh chỉnh mô hình thị giác – ngôn ngữ cỡ lớn vượt xa khả năng máy tính cá nhân; mục tiêu đúng là đọc [arXiv:2307.15818](https://arxiv.org/abs/2307.15818).

## SO-101 không phải một dòng VLA có sẵn

Cánh tay follower SO-101 ghi nhận vector hành động 6 giá trị ứng với 6 động cơ Feetech theo đúng tên khóa trong tập dữ liệu bạn tự thu, không có trong đầu ra của RT-1, RT-2, OpenVLA hay pi0. Việc tự ý gán "phần tử thứ tư cho khớp cổ tay" đồng nghĩa tạo ra bộ điều khiển mới và luôn tiềm ẩn rủi ro nếu không tắt mô-men (torque) hoặc cố định giá đỡ khi thử lần đầu.

Phần thực hành tay máy nằm ở [bài lab tay SO-101]({% multilang_post_url contents/chapter12/12_06_so101_arm_lab %}). Dòng đối chiếu bổ sung cho SO-101 (không thay thế hai dòng VLA yêu cầu ở mục Lab bên dưới):

| Hệ thống | Đầu vào | Không gian hành động | Có phải 6 khớp SO-101? | Chạy trên laptop tối nay? |
| --- | --- | --- | --- | --- |
| SO-101 của bạn | Ảnh camera (nếu gắn) kèm trạng thái khớp | 6 giá trị theo đúng đơn vị trong tệp dataset | Có, vì đây là phần cứng bạn trực tiếp thu dữ liệu | Đọc tài liệu và hiệu chỉnh (khi có tay trên bàn): có. Huấn luyện không có GPU: không |

### Giải thích: Tính tay sai số lượng tử hóa khi mã hóa hành động thành 256 bin rời rạc

Giả sử một mô hình VLA rời rạc hóa góc khớp vai $$q_1 \in [-90^\circ, +90^\circ]$$ (dải rộng $$180^\circ$$) thành đúng **256 token hành động** (tương ứng 255 khoảng chia đều):
- Độ phân giải góc mỗi bước token:
  $$\Delta q = \frac{180^\circ}{255} \approx \mathbf{0{,}706^\circ}.$$
- Nếu cánh tay dài $$L = 0{,}40\text{ m}$$, sai số vị trí đầu kẹp chỉ riêng do làm tròn góc 1 khớp đã là:
  $$\Delta s = L \cdot \Delta q_{\text{rad}} = 0{,}40 \times \left(0{,}706 \times \frac{\pi}{180}\right) \approx \mathbf{4{,}9\text{ mm}}!$$

Sai số 5 mm này không vấn đề gì khi nhặt một quả cam, nhưng sẽ làm **kẹt cứng** khi cắm một đầu dây USB đòi hỏi dung sai dưới 1 mm! Đó chính là lý do các VLA mới như $$\pi_0$$ chuyển từ token rời rạc sang đầu ra liên tục (Flow Matching / Diffusion)!

## Lab

Chọn **hai** trong bốn hệ thống sau (không chọn lại RT-1 vì đã làm mẫu) để đọc trang gốc — không tải tệp trọng số:

- RT-2: [arXiv:2307.15818](https://arxiv.org/abs/2307.15818)
- Open X-Embodiment: [robotics-transformer-x.github.io](https://robotics-transformer-x.github.io/)
- OpenVLA: [arXiv:2406.09246](https://arxiv.org/abs/2406.09246) và [openvla.github.io](https://openvla.github.io/)
- pi0: [pi.website/blog/pi0](https://www.pi.website/blog/pi0)

Chép khung bảng sau vào `lab-notes.md` và điền đầy đủ hai dòng bạn chọn:

| Hệ thống | Đầu vào | Không gian hành động | Có phải `Twist` trên đồ thị của bạn hay đích khớp? | Chạy trên laptop tối nay? |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |
|  |  |  |  |  |

**Kết quả mong đợi:** hai dòng đầy đủ thông tin sát nguồn gốc: cột đầu vào nêu rõ ảnh và ngôn ngữ (nếu tài liệu có), cột không gian hành động chỉ rõ phần cứng của bài báo khác với Capstone, cột `Twist` trả lời **không** cho `/cmd_vel` của bạn (kể cả khi robot trong bài có bánh xe), và cột laptop trả lời rõ **không** với việc huấn luyện tại nhà (không ghi mập mờ kiểu "có thể dùng Colab").

**Các lỗi thường gặp**

| Nội dung ghi trong bảng | Điểm sai |
| --- | --- |
| Ghi "có xuất bản `Twist`" vì thấy RT-1 có đế di động | Kênh điều khiển đế của họ khác hẳn topic, đơn vị và chiều rộng trục bánh của Capstone |
| Ghi "OpenVLA trọng số mở nên huấn luyện được tối nay" | Trọng số mở không thu nhỏ mô hình nhiều tỉ tham số xuống laptop không GPU để train hay suy luận thời gian thực |
| Ghi "Open X-Embodiment có nhiều robot nên đã bao phủ Capstone" | Bao phủ chỉ đúng khi tập dữ liệu thực sự chứa cảm biến và không gian hành động của chính xe bạn |
| Ghi "có câu lệnh `stop` nên không cần lo watchdog" | Watchdog chỉ giám sát khung serial, không hiểu ngôn ngữ; nếu policy còn phát lệnh thì động cơ vẫn chạy |
| Bất kỳ dòng nào điền "có" cho việc huấn luyện tại nhà | Phải sửa lại thành "không" (chỉ đọc và đối chiếu tài liệu) |

## Mua sắm

Bài học này không yêu cầu mua thêm phần cứng. Không nên vội mua tay kẹp, mạch Jetson hay máy tính mới chỉ vì các bài báo VLA dùng nhiều camera hơn; việc gắn thêm camera lên Capstone cũng không biến nó thành phần cứng của RT-1 hay OpenVLA.

## Video tham khảo

- **Xem trước:** [OpenVLA: LeRobot Research Presentation #5 by Moo Jin Kim](https://www.youtube.com/watch?v=-0s0v3q7mBk) — Hugging Face (tiếng Anh). Moo Jin Kim trình bày về OpenVLA trên kênh Hugging Face (nhận ảnh và câu lệnh, xuất hành động cho phần cứng cụ thể).
- [RT - 2 Visual Language Action Models | Robotics Transformer 2 | Google DeepMind](https://www.youtube.com/watch?v=yJYchWc9j8A) — MLNews (tiếng Anh). Video ngắn tóm tắt RT-2 để đặt cạnh OpenVLA trước khi đọc bài báo gốc.
- [π0: A Foundation Model for Robotics with Sergey Levine - 719](https://www.youtube.com/watch?v=5mY71rGXAkM) — The TWIML AI Podcast with Sam Charrington (tiếng Anh). Phỏng vấn Sergey Levine về π0, giúp đối chiếu hành động liên tục với hành động rời rạc của OpenVLA.

## Bài tập

1. Nếu bảng lab của bạn có dòng RT-2, hãy viết đầy đủ một câu cho cột laptop và nêu rõ hoạt động bạn thực sự được thực hiện với tệp PDF bài báo. *Gợi ý:* không huấn luyện tại nhà (kể cả trên máy mượn); chỉ đọc và trích dẫn thông tin từ phần tóm tắt/bài báo.
2. Trọng số OpenVLA được công bố công khai, nhưng vì sao điều đó không đồng nghĩa bạn có thể chạy vòng điều khiển trực tiếp trên chiếc laptop đang nạp ESP32? *Gợi ý:* mô hình nhiều tỉ tham số đòi hỏi GPU mạnh, trong khi vòng điều khiển cần nhịp lệnh ổn định cỡ 20 ms trên laptop không GPU.
3. Giả sử một người ánh xạ kênh "mở tay kẹp" của một VLA sang vận tốc góc $$\omega$$. Xe Capstone sẽ phản ứng thế nào mỗi lần policy mở kẹp? *Gợi ý:* xe sẽ xoay bất ngờ vì gắn nhầm kênh điều khiển không liên quan — dataset card ở bài 12-01 giúp ngăn chặn lỗi này bằng quy định đơn vị rõ ràng.
4. Người vận hành gõ lệnh `"stop"` nhưng node policy vẫn đều đặn gửi $$v = 0.15$$ mỗi 20 ms. Watchdog 300 ms có kích hoạt không và yếu tố nào mới thực sự dừng được bánh xe? *Gợi ý:* watchdog không kích hoạt vì khung vẫn đến đều; cần gửi lệnh `0` tường minh trên đường serial hoặc ngắt công tắc nguồn phần cứng.
5. Nêu các thông số đầu vào cụ thể của Capstone mà tập dữ liệu Open X-Embodiment không thể tự suy ra hộ bạn. *Gợi ý:* tư thế lắp camera nhìn trước, chiều rộng trục bánh và vector hành động hai chiều $$(v, \omega)$$ đặc trưng của chính khung xe Capstone.

## Đọc thêm

- [Trang RT-1](https://robotics-transformer1.github.io/) và [bài RT-1](https://arxiv.org/abs/2212.06817)
- [RT-2](https://arxiv.org/abs/2307.15818)
- [Open X-Embodiment](https://robotics-transformer-x.github.io/)
- [OpenVLA](https://arxiv.org/abs/2406.09246) và [trang dự án](https://openvla.github.io/)
- [pi0, Physical Intelligence](https://www.pi.website/blog/pi0)
