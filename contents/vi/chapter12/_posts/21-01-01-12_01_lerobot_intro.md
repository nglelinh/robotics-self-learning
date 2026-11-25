---
layout: post
title: "Giới thiệu LeRobot / HF robotics"
chapter: "12"
order: 1
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter12
lesson_type: required
draft: false
---

Thời lượng: **~70 phút** (khoảng 25 phút đọc tài liệu và kho mã nguồn, 30 phút viết dataset card, 15 phút làm bài tập).

Suốt 11 chương vừa qua, ta lập trình robot theo lối cổ điển: tự viết phương trình động học, tự thiết kế bản đồ và tự chỉnh hàng chục tham số PID/Nav2. Cách tiếp cận đó cực kỳ chính xác với xe chạy trong hành lang, nhưng lại bó tay trước những thao tác tưởng chừng đơn giản với trẻ lên 5: *gấp một chiếc áo sơ mi, nhặt một sợi dây cáp mềm hay múc một thìa cà phê*. Chương 12 mở ra làn sóng **Robot Học (Robot Learning)** với hệ sinh thái mã nguồn mở **LeRobot (Hugging Face)** — nơi robot học kỹ năng trực tiếp từ dữ liệu trình diễn của con người.

## Kiến thức cần nhớ: Ba trụ cột của Hệ sinh thái LeRobot

1. **Chuẩn Dữ liệu Tập trình diễn (`LeRobotDataset`)**:
   Lưu trữ đồng bộ từng khung hình camera (video nén MP4/AV1), trạng thái góc khớp `observation.state` và hành động mục tiêu `action` theo đúng khung thời gian (ví dụ 30 Hz) dưới dạng Parquet + Video chuẩn hóa, dễ chia sẻ trên Hugging Face Hub.
2. **Đường ống Teleoperation → Train → Eval Thống nhất**:
   Dùng cánh tay chủ–tớ (leader–follower như SO-101) ghi lại 50–100 lượt trình diễn sạch, huấn luyện chính sách học bắt chước (ACT, Diffusion Policy) trên GPU rồi triển khai vòng kín ngay trên cùng giao diện phần mềm.
3. **Không thay thế mà Xây trên nền Kỹ thuật Robot Cổ điển**:
   Hiệu chuẩn góc 0 của servo, đồng bộ tốc độ khung hình camera, giới hạn mô-men an toàn và độ trễ vòng lặp từ Chương 08–10 vẫn quyết định 80% sự thành bại của dữ liệu huấn luyện!

## Mục tiêu

Sau bài học này, bạn sẽ xác định đúng ba thành phần mà hệ sinh thái LeRobot liên kết trên cùng một giao ước dữ liệu: **dataset**, **policy** và **robot**. Bạn nhận diện được các phần cứng tiêu biểu của dự án như SO-100, Koch v1.1 và LeKiwi (các mẫu cánh tay và đế di động chi phí thấp) và giải thích vì sao chúng khác với khung xe vi sai Capstone. Bạn sẽ viết một bảng mô tả tập dữ liệu (dataset card) dài một trang cho một tập mẫu giả định gồm camera, vận tốc dài $$v$$ và vận tốc góc $$\omega$$ với hệ đơn vị thống nhất giữa lúc ghi và lúc phát lại, đồng thời trích nguyên văn dòng mô tả trên README của kho lưu trữ vào `lab-notes.md` kèm ngày truy cập.

## Kiến thức cần trước

Bạn chỉ cần trình duyệt web và terminal. Xe Capstone đã nhận vận tốc dài theo m/s và vận tốc góc theo rad/s, với watchdog 300 ms trên firmware chương 08 tự ngắt động cơ khi mất lệnh, và topic `geometry_msgs/Twist` ở chương 09 cũng dùng đúng cặp `linear.x` và `angular.z`. Bài này không yêu cầu GPU, tay điều khiển leader hay robot thứ hai; nếu mạng chậm có thể bỏ qua lệnh `pip` vì sản phẩm chính là trích dẫn README và dataset card.

## Vì sao bài này nằm trên lộ trình

Capstone A vận hành nhờ firmware nhận $$(v, \omega)$$, còn ROS 2 Jazzy đưa hai đại lượng đó lên topic. Thư viện học máy không thay thế ngăn xếp điều khiển này mà bổ sung thêm lớp dữ liệu và chính sách (policy). Tệp dữ liệu bắt buộc phải lưu đúng các quan sát (observation) mà robot thực tế tạo ra được và đúng định dạng hành động (action) mà firmware chấp nhận. Nếu khâu ghi lưu giá trị PWM nhưng khâu huấn luyện lại hiểu là radian hay m/s, bạn đang huấn luyện cho một robot hoàn toàn khác với robot chạy thực tế. Các bài 12-02 và 12-03 sẽ đi sâu vào cách policy sinh hành động dựa trên các khóa dữ liệu đã chốt ở đây, còn bài 12-04 mở rộng cùng nguyên tắc đó sang các mô hình lớn đã công bố.

## Khái niệm

[LeRobot](https://huggingface.co/docs/lerobot/index) là một thư viện Python, một chuẩn định dạng tập dữ liệu và tập hợp các cấu hình phần cứng do Hugging Face phát triển. Trang tài liệu chính mô tả quy trình gồm bốn bước: **teleoperate** (con người điều khiển từ xa), **record** (ghi lại các phiên mẫu gồm video camera đồng bộ với lệnh điều khiển), **train** (huấn luyện một policy/mạng nơ-ron bắt chước các hành động đó) và **deploy** (đưa policy xuất lệnh điều khiển trực tiếp robot). Trong phạm vi bài này chúng ta dừng trước bước `train`; bốn động từ trên dùng để định vị tài liệu chứ chưa chạy huấn luyện.

**Dataset** đồng bộ hóa hình ảnh, trạng thái (`state`) và hành động (`action`) theo cùng một trục thời gian trong cấu trúc `LeRobotDataset`. Dữ liệu cánh tay robot thường chứa `observation.images.<camera>`, góc khớp hiện tại và góc khớp đích; trong khi dữ liệu xe vi sai chứa ảnh camera và hành động hai thành phần $$(v, \omega)$$. Định dạng này hỗ trợ cả hai nhưng sẽ không tự cảnh báo nếu bạn trộn nhầm đơn vị hoặc cấu trúc.

**Policy** nhận đầu vào là `observation` và xuất ra `action` (ví dụ ACT ở bài 12-02). Trọng số của mạng luôn gắn chặt với số chiều và ý nghĩa vật lý của từng phần tử: đúng số chiều nhưng lệch đơn vị vẫn dẫn đến điều khiển sai.

**Robot** trong LeRobot bao gồm phần cứng kèm tệp cấu hình (động cơ, camera và các khóa dữ liệu tương ứng). Trên tài liệu chính thức, SO-101 là mẫu cánh tay chi phí thấp chủ lực (kế nhiệm SO-100), Koch v1.1 là cánh tay cộng đồng được hỗ trợ, còn LeKiwi là đế di động có gắn thêm cánh tay — đó là các hình thái phần cứng (*embodiment*) của dự án. Trong khi đó, xe Capstone chỉ có hai bánh dẫn động, không có tay kẹp, nhận lệnh $$(v, \omega)$$ và có watchdog 300 ms. Vector góc khớp của SO-101 không tương thích `/cmd_vel`, và ngay cả LeKiwi cũng chứa thêm chiều hành động của cánh tay nên không thể dùng chung khóa trực tiếp với Capstone.

Nguyên tắc cốt lõi là sự đồng nhất giữa lúc ghi và lúc phát: lúc ghi, người lái điều khiển và logger lưu lại; lúc phát, policy xuất lệnh và firmware thực thi — cả hai phải dùng chính xác cùng tên khóa và cùng đơn vị. Chỉ cần camera gắn thấp hơn 15 cm hoặc đảo dấu góc yaw, cột dữ liệu vẫn mang tên `w` nhưng chuyển động thực tế đã đổi ngược. Ngoài ra, `fps: 10` đồng nghĩa khoảng cách giữa các lệnh là 0,1 s; nếu camera chạy 30 Hz mà không đồng bộ dấu thời gian, ảnh sẽ bị ghép lệch với lệnh. Đặc biệt, phải giữ nguyên watchdog 300 ms trong lúc ghi dữ liệu để phản ánh đúng đặc tính an toàn của robot thật (nếu đường truyền bị gián đoạn khiến log xuất hiện các đoạn $$(0, 0)$$, hãy đánh dấu lọc frame chứ không tắt watchdog).

## Hình

![Dataset, policy và robot dùng chung khóa]({{ site.imgurl }}/generated/ch12_lerobot.png)

Sơ đồ gồm ba khối và hai chiều luồng dữ liệu: khối `dataset` lưu trữ `observation` và `action`; mũi tên đi qua `policy` biểu thị giai đoạn phát lại (đọc quan sát, sinh hành động gửi xuống robot); mũi tên xanh `record` đi ngược lại biểu thị giai đoạn ghi mẫu (người điều khiển robot, logger lưu đúng các khóa tương ứng). Ghi chú đỏ bên dưới nhấn mạnh yêu cầu đồng nhất khóa và đơn vị trên dataset card trước khi nghĩ đến bước huấn luyện.

## Ví dụ đọc có số

Dưới đây là một dataset card mẫu mô tả một tập dữ liệu (episode) giả định dài 2 giây ở tần số 10 Hz (tổng cộng 20 khung dữ liệu) cho xe Capstone, đặt ở đầu thư mục dữ liệu để mọi script phía sau đọc thống nhất:

```text
robot_name: capstone_diff
embodiment: two-wheel diff-drive, no arm
fps: 10
episode_length_s: 2.0
features:
  observation.images.cam:
    dtype: video
    shape: [480, 640, 3]
    names: [height, width, channel]
    info: RGB, forward camera, 10 Hz, same clock as action
  observation.state:
    dtype: float32
    shape: [2]
    names: [v_meas_m_s, w_meas_rad_s]
  action:
    dtype: float32
    shape: [2]
    names: [v_cmd_m_s, w_cmd_rad_s]
```

Xét từng thời điểm cụ thể: ở dòng 0 (hành lang trống), trạng thái đo $$(0.00, 0.00)$$ và hành động $$(0.20, 0.00)$$ — xe tiến thẳng với vận tốc 0,20 m/s (đi được khoảng 2 cm trong một chu kỳ 0,1 s). Ở dòng 8 (ghế xuất hiện phía bên trái khung hình), hành động là $$(0.10, -0.40)$$ — giảm tốc và quay phải với yaw $$-0.40$$ rad/s (theo quy tắc bàn tay phải với trục $$z$$ hướng lên, yaw âm là rẽ phải). Đến dòng 19, hành động về $$(0.00, 0.00)$$ do người lái chủ động dừng.

Nếu hệ đơn vị bị lệch (ví dụ script teleop ghi giá trị kiểu PWM chương 07 trong $$[-100, 100]$$ nhưng dataset card lại khai báo m/s và rad/s), bộ nạp dữ liệu sẽ hiểu nhầm mức `70` là 70 m/s mà mạng nơ-ron không hề báo lỗi. Để loại bỏ rủi ro này, cả logger và cầu nối phát lại phải tuân thủ duy nhất một khai báo `names` và đơn vị.

Kiểm tra tính nhất quán số lượng khung hình:

$$
N = \text{fps} \times T = 10 \times 2.0 = 20
$$

Nếu thư mục chỉ có 20 ảnh nhưng card lại ghi nhầm `fps: 30`, thời lượng thực tế sẽ bị bóp méo và các thao tác quay sẽ bị kéo giãn sai tốc độ.

### Giải thích: Tính tay kích thước bộ dữ liệu 50 lượt trình diễn (episodes) trên LeRobot

Giả sử bạn thu thập **50 lượt trình diễn** gắp một khối lập phương bằng cánh tay **6 khớp (SO-101)** gắn 2 camera (1 camera cổ tay + 1 camera toàn cảnh), mỗi lượt dài **15 giây** ở tần số **30 Hz**:
- Tổng số bước thời gian (frames) trong toàn bộ dataset:
  $$N_{\text{frames}} = 50\text{ lượt} \times 15\text{ s} \times 30\text{ Hz} = \mathbf{22.500\text{ bước}}.$$
- Kích thước bảng trạng thái & hành động (Parquet: 6 float32 `state` + 6 float32 `action` = 48 byte/bước):
  $$22.500 \times 48\text{ B} \approx \mathbf{1{,}08\text{ MB}}$$ (siêu nhẹ!).
- Kích thước 2 luồng video nén H.264/AV1 (~1,5 Mbps mỗi camera, tổng 750 giây = 12,5 phút):
  $$2 \times \frac{1{,}5\text{ Mb/s}}{8} \times 750\text{ s} \approx \mathbf{281\text{ MB}}.$$

Toàn bộ bộ dữ liệu huấn luyện một kỹ năng thao tác khéo léo chỉ nặng dưới **300 MB** — hoàn toàn tải được trong vài giây và huấn luyện xong trong 30–60 phút trên 1 GPU tầm trung!

## Lab

Bài thực hành này thực hiện hoàn toàn trên máy tính (không cần bật xe). Tệp `lab-notes.md` cần nộp hai nội dung: một câu trích dẫn có ngày và một dataset card tự viết.

**1. Khảo sát cấu trúc tài liệu.** Mở [trang index LeRobot](https://huggingface.co/docs/lerobot/index), đọc mục "How it works" và chép lại đúng thứ tự bốn bước: `teleoperate`, `record`, `train`, `deploy`, kèm ghi chú rằng bài học này dừng trước bước `train`. Tiếp theo, ghi lại tên các tiêu đề (heading) thực tế bạn thấy trên trang hiện tại cho các mục cài đặt, dataset, imitation learning và robots, kèm ngày truy cập (nếu trang tài liệu đã đổi tên tiêu đề, ghi đúng tên thực tế):

```text
date: 2026-09-23
docs: https://huggingface.co/docs/lerobot/index
verbs: Teleoperate, Record, Train, Deploy
pages I opened:
  - Installation (có lệnh; tôi không cần chạy)
  - (heading dataset tôi thực sự thấy)
  - (heading imitation tôi thực sự thấy)
  - Robots: trang index có tên SO-101, LeKiwi, Koch v1.1
stopped before: any train command
```

**2. Trích dẫn mô tả kho mã nguồn.** Mở [huggingface/lerobot](https://github.com/huggingface/lerobot), chép nguyên văn dòng mô tả ngắn ngay dưới tên kho lưu trữ đặt trong dấu ngoặc kép kèm ngày truy cập (không diễn giải lại).

**3. Viết dataset card.** Viết lại dataset card cho riêng bạn bằng cách thay đổi ít nhất một thông số nhưng vẫn đảm bảo phép nhân nhất quán (ví dụ `fps: 5`, `episode_length_s: 3.0`, tương ứng 15 dòng). Giữ nguyên khóa `observation.images.cam`, đơn vị m/s cho $$v$$ và rad/s cho $$\omega$$; bổ sung một dòng dữ liệu mẫu kèm câu giải thích rằng cặp giá trị đó tương ứng trực tiếp với `linear.x` và `angular.z` trên cầu nối Capstone.

*(Tùy chọn)* Nếu muốn kiểm tra phiên bản gói trong terminal mà không cài đặt hay huấn luyện:

```bash
pip index versions lerobot
```

**Kết quả mong đợi:** lệnh trên trả về danh sách phiên bản (hoặc thông báo lỗi mạng/phiên bản `pip` cũ đều được chấp nhận) — dừng ngay tại đây, không chạy bất kỳ lệnh `train` nào. Phần bài viết phải đảm bảo thống nhất đơn vị m/s và rad/s cho `action`, câu trích README đặt trong ngoặc kép, ghi rõ ngày xem tài liệu và không chứa log huấn luyện hay checkpoint.

**Các lỗi thường gặp**

| Sai sót | Hệ quả |
| --- | --- |
| Logger lưu PWM nhưng tài liệu policy khai báo m/s và rad/s | Lúc phát lại, policy sinh lệnh cho một hình thái robot khác hẳn lúc ghi |
| Tích `fps` và thời lượng không khớp số khung hình | Sai lệch tốc độ thời gian, khiến chuyển động rẽ nhẹ thành giật cục hoặc ngược lại |
| Tắt watchdog 300 ms trong lúc ghi dữ liệu teleop | Dữ liệu ghi không phản ánh đúng hành vi an toàn của firmware thật khi mất kết nối |
| Đường truyền rớt gói tạo nhiều đoạn `(0, 0)` đột ngột trong log | Policy sẽ học theo các lần khựng bất thường; cần sửa đường truyền hoặc lọc frame |
| Chạy lệnh huấn luyện vì thấy `train` là bước thứ ba trong docs | Nằm ngoài phạm vi bài lab; sản phẩm nộp chỉ gồm dataset card và trích dẫn |

## Phần cứng tùy chọn (không yêu cầu trong tuần này)

Bài học này không yêu cầu mua thêm thiết bị. Các bộ cánh tay hạng SO-100 là kit nhập khẩu (khung in 3D, servo, tay leader, camera), tổng chi phí về Việt Nam thường ở mức nhiều triệu đồng (cần tự kiểm tra giá mới nhất nếu sau này có nhu cầu) và hoàn toàn không bắt buộc trong khóa học. Khung xe bạn đang thiết kế dataset card cho chính là chiếc Capstone đã lắp ráp.

## Video tham khảo

- **Xem trước:** [Core Concepts: Imitation Learning](https://www.youtube.com/watch?v=GDmhrAHxgQE) — Sanjiban Choudhury (tiếng Anh). Giới thiệu nền tảng học bắt chước (ghi hành động mẫu của người rồi huấn luyện policy tái tạo lại), phân biệt với học tăng cường (reinforcement learning) ở các video ngắn của [Chinbi](https://chinbi.com).
- [How to Train an AI Robotic Arm With No Code (Hugging Face LeRobot + SO-101)](https://www.youtube.com/watch?v=7tGT8hqRSAo) — Brogan M. Pratt (tiếng Anh). Minh họa hệ sinh thái LeRobot với tay SO-101, giúp phân biệt rõ ba thành phần dataset, policy và robot.

## Bài tập

1. Trên dataset card bạn vừa viết, hai đại lượng nào tạo thành `action` và đơn vị của từng đại lượng là gì? *Gợi ý:* $$v$$ (m/s) và $$\omega$$ (rad/s), khớp với `Twist` (không dùng PWM).
2. Hành động của SO-101 là vector góc khớp đích, trong khi cầu nối Capstone nhận hai đại lượng vô hướng $$(v, \omega)$$. Vì sao không thể cắt lấy hai phần tử đầu của vector SO-101 để gán làm $$v$$ và $$\omega$$? *Gợi ý:* hai phần tử đó biểu thị góc khớp của một cánh tay cơ khí khác hoàn toàn về hình thái và đơn vị; cắt bớt chiều vector không tạo ra động học xe vi sai.
3. Bạn chọn `fps: 5` và `episode_length_s: 3.0` thì có bao nhiêu dòng dữ liệu? Nếu một người bạn có 15 ảnh ghi ở 5 Hz nhưng lại khai báo nhầm `fps: 10`, card đó biểu thị thời lượng bao lâu và sai lệch gì xảy ra? *Gợi ý:* $$5 \times 3.0 = 15$$ dòng; khai báo `fps: 10` khiến thời lượng trên giấy chỉ còn $$15/10 = 1.5$$ s (nén đôi thời gian nên vận tốc góc trông nhanh gấp đôi).
4. Đường truyền serial bị mất 0,5 s trong lúc ghi mẫu khi watchdog 300 ms trên firmware vẫn bật. Log sẽ ghi nhận hành động nào trong khoảng gián đoạn đó, và điều gì xảy ra nếu bạn đã tắt watchdog? *Gợi ý:* khi còn watchdog, lệnh về 0 sau khoảng 300 ms; nếu tắt watchdog, lệnh cuối khác 0 bị giữ nguyên suốt khoảng trống — chỉ trường hợp đầu khớp đúng hành vi khi phát lại trên phần cứng thật.
5. Dán câu mô tả README bạn đã trích dẫn và viết thêm một mệnh đề xác nhận phạm vi thực hành tuần này. *Gợi ý:* giữ nguyên văn câu trên kho GitHub kèm ghi chú rằng tuần này không chạy huấn luyện.

## Đọc thêm

- [Tài liệu LeRobot](https://huggingface.co/docs/lerobot/index) — xem mục lục và các trang khái niệm chính (bước `train` chỉ đọc để nắm bức tranh tổng thể).
- [huggingface/lerobot trên GitHub](https://github.com/huggingface/lerobot) — nguồn trích dẫn dòng mô tả ngắn cho bài lab.
