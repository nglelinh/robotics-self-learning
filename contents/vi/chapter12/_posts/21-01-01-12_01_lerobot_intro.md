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

Thời lượng: **~70 phút**. Khoảng 25 phút đọc docs và repository, 30 phút viết dataset card, 15 phút làm bài tập.

## Mục tiêu

Bạn gọi đúng ba thứ mà dự án LeRobot giữ trên một hợp đồng: dataset, policy, và robot. Bạn chỉ ra dòng SO-100, Koch v1.1 và LeKiwi là cánh tay và đế di động giá thấp của chính dự án đó, rồi nói vì sao không cái nào trong số đó là khung vi sai Capstone. Bạn viết một dataset card một trang cho một episode giả, khóa là camera, vận tốc tiến $$v$$ và vận tốc góc $$\omega$$, đơn vị giống nhau lúc ghi và lúc phát. Bạn chép nguyên câu mô tả một dòng trên README của repository vào `lab-notes.md`, kèm ngày bạn đọc.

## Kiến thức cần trước

Bạn mở được trình duyệt và terminal. Capstone đã nhận vận tốc tiến theo mét trên giây và vận tốc góc theo radian trên giây. Firmware chương 08 vẫn đưa động cơ về 0 nếu 300 ms không có khung mới. `geometry_msgs/Twist` ở chương 09 là cùng một cặp: `linear.x` và `angular.z`. Không cần card đồ họa, không cần tay leader, không cần robot thứ hai. Mạng chậm thì bỏ qua `pip`. Bài nộp là câu trích và tấm card.

## Vì sao bài này nằm trên lộ trình

Capstone A là khung vi sai chạy khi firmware chấp nhận $$v$$ và $$\omega$$. ROS 2 Jazzy đặt hai số đó lên một topic. Thư viện học không thay stack này. Nó thêm một file. File phải chứa đúng quan sát mà robot sau này tạo ra được, và đúng action mà firmware sau này chịu nhận. Một ghi chú bảo action là PWM động cơ, ghi chú kia bảo là radian, thì bạn đã ghi một robot và phát lại trên robot khác. Bài 12-02 và 12-03 giả sử khóa đã tồn tại, rồi mới cãi nhau về cách policy điền khóa. Bài 12-04 là cùng một lỗi, ở tầm một checkpoint đã công bố. Bài 12-05 bảo bạn chọn một tháng. Tháng thì tùy. Hợp đồng khóa và đơn vị thì không tùy.

## Khái niệm

[LeRobot](https://huggingface.co/docs/lerobot/index) là thư viện Python, một định dạng dataset, và một bộ cấu hình phần cứng gắn với Hugging Face. Trang index mô tả vòng lặp bốn động từ: teleoperate, record, train, deploy. Teleoperate là người lái. Record là mỗi demonstration thành video camera đồng bộ với action người đã gửi. Train là một policy, tức một mạng, bắt chước các action đó. Deploy là policy ghi action trở lại robot. Khóa học này dừng trước train. Bốn động từ là cách bạn đọc tài liệu, không phải script bài tập.

**Dataset** xếp một ảnh, một state, và một action trên một đồng hồ. File gọi là LeRobotDataset. Log cánh tay dùng `observation.images.<camera>`, vị trí khớp, và đích khớp. Log vi sai dùng camera và action hai thành phần. Định dạng chứa được cả hai và không cảnh báo khi bạn trộn.

**Policy** đọc observation và ghi action. ACT là policy bài sau sẽ đọc. Trọng số chờ một độ dài và một nghĩa cho từng ô. Đúng độ dài mà sai đơn vị vẫn là sai robot.

**Robot** ở đây là một thân cộng config: động cơ, camera, và khóa chúng điền. Trên docs, SO-101 là cánh tay giá thấp chủ lực, SO-100 là đời trước cùng họ. Koch v1.1 là cánh tay cộng đồng họ vẫn ghi tài liệu. LeKiwi là đế di động có cánh tay. Đó là embodiment của dự án. Capstone là hai bánh chủ động, không kẹp, action $$(v,\omega)$$, và timeout của bạn. Đích khớp SO-101 không xuất bản `cmd_vel`. Action của LeKiwi có cả cánh tay, nên chữ "mobile" không gộp khóa.

Lúc ghi là người lái, logger viết. Lúc phát là policy viết, firmware áp lệnh. Cùng tên, cùng đơn vị, cả hai lúc. Camera thấp hơn 15 cm, hoặc dấu yaw bị đảo, cột vẫn tên `w` mà chuyển động đổi. `fps: 10` nghĩa là các action cách 0,1 s. Camera 30 Hz đổ vào mà không căn giờ sẽ ghép ảnh với nhầm lệnh. Timeout 300 ms ở lại khi bạn ghi. Comment nó ra là log một robot bạn không được phép chạy. Link trễ làm log đầy $$(0, 0)$$ là lỗi kia: đánh dấu frame, đừng xóa watchdog.

## Hình

![Dataset, policy và robot dùng chung khóa]({{ site.imgurl }}/generated/ch12_lerobot.png)

Ba hộp, hai mũi tên. Hộp dataset giữ observation và action. Mũi tên xuyên qua policy là lúc phát: một dòng đi vào, một action đi ra, robot thực hiện. Mũi tên xanh ghi record chạy ngược: người lái robot, logger lưu cùng các khóa. Dòng đỏ dưới hộp là luật mà tấm card phải khóa lại. Dòng xám bảo đọc card trước một lần train. Tối nay lần train không bắt đầu. Tấm card thì có.

## Ví dụ đọc có số

Tấm card này mô tả một episode Capstone giả. Không phải file trên Hub, cũng không phải exporter bạn phải cài. Hai giây, mười khung mỗi giây, hai mươi dòng. Card nằm đầu thư mục để script sau không được đoán.

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

Dòng 0, hành lang trống: state đo $$(0.00, 0.00)$$, action $$(0.20, 0.00)$$. Đó là 0,20 m/s tiến, không quay. Trong một chu kỳ 0,1 s, đế trườn khoảng 2 cm nếu bánh chạm đất. Dòng 8, ghế xuất hiện bên trái ảnh: action $$(0.10, -0.40)$$, chậm hơn, yaw $$-0.40$$ rad/s. Trục $$z$$ hướng lên, quy tắc bàn tay phải, yaw âm là rẽ phải. Dòng 19 là $$(0.00, 0.00)$$, người lái chủ đích dừng, không phải timeout.

Cùng hai mươi dòng trở thành robot khác nếu đơn vị trôi. Script teleop vẫn viết lệnh kiểu PWM chương 07 trong $$[-100, 100]$$, còn tờ bạn đưa cho policy bảo vector là m/s và rad/s. Loader sau tin tờ giấy. Nó đọc 70 trong log và hiểu là 70 m/s. Không tầng nào trong mạng kiểm điều đó. Card chỉ xong khi mâu thuẫn này không còn chỗ đứng: một dòng `names`, một đơn vị, logger và cầu phát lại cùng nhập dòng đó.

Số dòng là phép kiểm, không phải khẩu hiệu:

$$
N = \text{fps} \times T = 10 \times 2.0 = 20
$$

Hai mươi ảnh mà card ghi `fps: 30` không còn là episode 2,0 s. Ai đó sẽ kéo giãn cú quay. Hãy ghi con số bạn kiểm được bằng cách liệt kê thư mục.

## Lab

Chỉ phần mềm. Đế có thể nằm trên kệ. `lab-notes.md` nhận hai thứ: một câu trích có ngày, và một dataset card.

**Sơ đồ docs.** Mở [trang index LeRobot](https://huggingface.co/docs/lerobot/index). Đọc mục "How it works" và chép bốn động từ đúng thứ tự: teleoperate, record, train, deploy. Bên dưới, viết câu bạn sẽ giữ: khóa học này dừng trước train. Rồi tìm, theo đúng heading đang có trên trang, một mục cài đặt, một mục về dataset, một mục imitation learning, và một mục robots. Docs đổi chỗ. Ghi ngày của ảnh chụp. Một ghi chú dùng được trông như sau, heading là heading bạn thấy:

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

Heading bị đổi tên thì ghi tên mới. Đừng bịa heading cho khớp bài giảng.

**Một câu từ repository.** Mở [huggingface/lerobot](https://github.com/huggingface/lerobot). Ngay dưới tên repository có một dòng mô tả. Chép nguyên câu đó vào `lab-notes.md`, để trong dấu ngoặc kép, kèm ngày. Đừng diễn giải. Nếu dòng đã đổi từ khi bài giảng được viết, dòng hôm nay mới là câu trích đúng.

**Dataset card.** Viết lại ví dụ ở trên cho ra của bạn. Đổi một con số và giữ phép tính khớp. Một sửa hợp lý là `fps: 5` và `episode_length_s: 3.0`, tức 15 dòng. Giữ khóa `observation.images.cam`, $$v$$ theo m/s, và $$\omega$$ theo rad/s. Thêm một dòng số và một câu nói rằng cặp số đó chính là `linear.x` và `angular.z` trên cầu Capstone.

Cài thư viện là việc tùy chọn. Lệnh terminal duy nhất bài này chấp nhận, nếu bạn muốn một dòng trong nhật ký, là liệt kê phiên bản:

```bash
pip index versions lerobot
```

**Kỳ vọng của lệnh.** Một danh sách ngắn mở đầu bằng tên gói, hoặc một lỗi mạng, quyền, hay `pip` cũ. Cả hai đều được. Danh sách phiên bản không phải policy đã luyện. Lệnh chạy được thì dừng. Đừng đi tiếp vào entrypoint train chỉ vì cài đặt tình cờ xong.

**Kỳ vọng của phần viết.** Mọi chỗ nói về `action` trên card đều là m/s và rad/s, kể cả dòng bạn bịa. Câu README nằm trong ngoặc kép. Ảnh chụp docs có ngày. Nhật ký không có đường loss, không có đường checkpoint.

**Các kiểu hỏng**

| Bạn tạo ra | Nó có nghĩa là |
| --- | --- |
| Comment logger nói PWM, ghi chú policy nói radian | Lúc phát, policy bị áp lên robot khác với lúc ghi |
| `fps` nhân số giây không bằng số ảnh | Cú quay bị kéo giãn. Né nhẹ thành giật, hoặc ngược lại |
| Ghi teleop khi timeout 300 ms đã bị gỡ | Log là của một đế giữ lệnh cuối khi link chết. Firmware thật không làm vậy, và bạn đã lái khi thiếu tính chất an toàn |
| Timeout vẫn còn, link đứng, log đầy số 0 đột ngột | Policy sẽ chép các lần dừng. Sửa link hoặc đánh dấu frame |
| Một lệnh train, vì docs liệt kê train là bước ba | Tắt nó. Bài nộp là card và câu trích |

## Phần cứng tùy chọn, không phải tuần này

Bài này không mua gì. Cánh tay hạng SO-100 là kit nhập: khung in, servo, tay leader, camera. Cộng bộ servo và tiền ship, hạng kit đó ở Việt Nam thường nằm ở mức nhiều triệu đồng. Hãy đối lại listing thật vào tuần bạn định mua. Bài giảng không gắn link shop cho cánh tay, vì link cũ còn hại hơn không có link. Khóa học không bắt mua. Camera tùy chọn ở chương 11 là cảm biến thêm duy nhất bạn có thể đã có, và card không cần ảnh sống. Robot mà card mô tả là Capstone bạn đã dựng.

## Bài tập

1. Trên card của bạn, hai số nào là action, đơn vị từng số là gì? Gợi ý: $$v$$ theo m/s và $$\omega$$ theo rad/s, cùng cặp với `Twist`. Cột nào còn ghi PWM thì card chưa xong.
2. Action của SO-101 là vector đích khớp. Cầu của bạn xuất bản hai vô hướng. Vì sao "lấy hai khớp đầu rồi gọi là $$v$$ và $$\omega$$" không phải bộ chuyển? Gợi ý: các ô đó là đơn vị khớp trên một thân khác. Phần còn lại của vector là cánh tay bạn không có. Cắt bớt không tạo ra khung vi sai.
3. Bạn đặt fps bằng 5 và episode dài 3,0 s. Có bao nhiêu dòng? Bạn học có 15 ảnh và ghi `fps: 10`. Card tuyên bố bao lâu, và thư mục dài bao lâu nếu camera thật chạy 5 Hz? Gợi ý: $$5 \times 3.0 = 15$$ dòng. Card của họ tuyên bố $$15/10 = 1.5$$ s. Thư mục là 3,0 s chuyển động bị dán nhãn một nửa thời gian, nên yaw trông nhanh gấp đôi.
4. Link serial rớt 0,5 s trong lúc ghi. Timeout là 300 ms và vẫn nằm trong firmware. Log phải hiện action gì cho đến khi link về? Log sẽ hiện gì nếu timeout đã bị gỡ trong phiên đó? Gợi ý: còn timeout thì về 0 sau khoảng 300 ms. Gỡ timeout thì lệnh khác 0 cuối cùng bị giữ suốt khoảng trống. Chỉ log thứ nhất khớp với lúc phát.
5. Dán câu README bạn đã trích, rồi thêm một mệnh đề của bạn. Gợi ý: câu trích là dòng trên repository hôm nay, không phải lời diễn. Mệnh đề của bạn phải nói rằng tuần này bạn không train.

## Đọc thêm

- [Tài liệu LeRobot](https://huggingface.co/docs/lerobot/index). Đi từ index, rồi sidebar bạn thực sự thấy. Bước train được mô tả ở đó và không phải bài này.
- [huggingface/lerobot trên GitHub](https://github.com/huggingface/lerobot). Dòng mô tả một câu dưới tiêu đề là một phần của lab.
