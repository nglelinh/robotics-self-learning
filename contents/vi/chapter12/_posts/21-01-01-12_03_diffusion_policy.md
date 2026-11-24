---
layout: post
title: "Trực giác Diffusion Policy"
chapter: "12"
order: 3
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter12
lesson_type: required
draft: false
---

Thời lượng: **~65 phút**, dành để đọc trang dự án, phân tích phép tính trung bình hành động và viết một đoạn nhận xét (không chạy khử nhiễu hay huấn luyện trên GPU).

Trong bài toán đẩy một khối chữ T vào đúng vị trí mục tiêu (Push-T), nếu tay máy gặp góc vuông đối xứng, đi vòng sang trái hay đi vòng sang phải đều hoàn hảo — nhưng đi **chính giữa** (trung bình của trái và phải) thì lại đẩy hỏng! **Diffusion Policy** mang chính ý tưởng khử nhiễu dần từ mô hình sinh ảnh sang không gian hành động robot: thay vì đoán trực tiếp một điểm trung bình mờ nhạt, mạng học trường vector **khử nhiễu từng bước** để kéo một chuỗi hành động ngẫu nhiên về đúng một nhánh quỹ đạo sắc nét hợp lệ.

## Bản đồ kiến thức nền: Ba trụ cột của Diffusion Policy

1. **Biểu diễn Phân phối Đa đỉnh (Multimodal Action Distribution)**:
   Mô hình hóa phân phối xác suất điều kiện $$p(\mathbf{A}_t \mid \mathbf{O}_t)$$ trên cả một khối hành động tương lai (action horizon $$T_p$$), giữ nguyên mọi nhánh rẽ hợp lệ thay vì bị sụp đổ về giá trị trung bình.
2. **Quá trình Khuếch tán Thuận (Thêm nhiễu) & Ngược (Khử nhiễu $$K$$ bước)**:
   Trong huấn luyện, mạng dự đoán phần nhiễu $$\varepsilon_\theta(\mathbf{A}_t^k, \mathbf{O}_t, k)$$ đã thêm vào hành động thật. Khi suy luận trên robot, ta bắt đầu từ nhiễu Gaussian trắng $$\mathbf{A}_t^K \sim \mathcal{N}(0, I)$$ và chạy vòng lặp khử nhiễu (DDPM / DDIM) để thu được quỹ đạo sạch $$\mathbf{A}_t^0$$.
3. **Ba Cửa sổ Thời gian ($$T_o, T_p, T_a$$ — Receding Horizon Control)**:
   Quan sát $$T_o$$ khung hình gần nhất → dự đoán khối $$T_p$$ bước hành động tương lai → chỉ thực thi $$T_a$$ bước đầu tiên ($$T_a \le T_p$$) rồi quan sát lại và lập kế hoạch mới!

## Mục tiêu

Sau bài học này, bạn sẽ giải thích được vì sao Diffusion Policy tạo ra quỹ đạo hành động bằng quá trình khử nhiễu lặp thay vì hồi quy một lần duy nhất. Thông qua ví dụ hai phiên mẫu xe Capstone vòng tránh một chiếc ghế, bạn sẽ chứng minh được vì sao lệnh trung bình lại đâm thẳng vào vật cản, đọc hiểu biểu diễn giản lược $$x_{t-1} = f(x_t, \text{observation})$$ như sơ đồ tư duy của bộ khử nhiễu đã học (chứ không phải phương trình cập nhật đầy đủ của bài báo), và đối chiếu rõ nét cơ chế của Diffusion Policy với ACT trong hai đoạn ngắn.

## Kiến thức cần trước

Hoàn thành bài 12-01 và 12-02: bạn nắm rõ cấu trúc khóa dataset và cách tính cửa sổ hở vòng $$k/f$$ giây của ACT. Bài học này không đòi hỏi GPU, môi trường conda hay checkpoint tải về; bạn chỉ cần truy cập trang dự án công khai.

## Vì sao bài này nằm trên lộ trình

Ở các chương trước, xe Capstone bám theo tuyến đường do bộ lập kế hoạch tường minh tính ra. **Diffusion Policy** (Chi và cộng sự) đưa ra một cách tiếp cận khác khi quỹ đạo học từ các phiên điều khiển mẫu mà người lái có nhiều phương án đi khác nhau. Trong hành lang, hai người lái có thể vòng qua một chiếc ghế từ hai phía trái và phải; nếu buộc bộ điều khiển bám theo giá trị trung bình của hai đường đó, xe sẽ lao thẳng vào chiếc ghế — trong khi cả ROS 2 Jazzy lẫn firmware đều sẵn sàng chuyển tiếp và thực thi giá trị trung bình đó mà không hề cảnh báo. Bài học giúp bạn nhận diện bài toán phân phối đa chế độ (multimodal) ngay trong dữ liệu, đồng thời củng cố thói quen kiểm soát cửa sổ hở vòng tương tự như ở ACT.

## Khái niệm

Một mô hình hồi quy thông thường nhận đầu vào `observation` và xuất ngay một `action` (hoặc một chunk) trong một lượt tính duy nhất. Cách này hoạt động tốt khi mọi mẫu huấn luyện cùng đi theo một phương án; nhưng khi dữ liệu tách thành hai phương án hợp lệ khác nhau, hàm mất mát bình phương sai số sẽ kéo dự đoán về điểm trung bình — một phương án thỏa hiệp không nằm trong tập mẫu và thường gây va chạm.

Chi, Feng, Du, Xu, Cousineau, Burchfiel và Song mô hình hóa policy như một quá trình **khử nhiễu có điều kiện** (conditional denoising): bắt đầu từ một chuỗi nhiễu ngẫu nhiên có cùng kích thước với quỹ đạo hành động, một mạng nơ-ron (lấy `observation` làm điều kiện) sẽ từng bước khử bớt nhiễu để kéo chuỗi đó tiến dần về một quỹ đạo hợp lệ tương tự tập mẫu. Bốn khối trên sơ đồ minh họa tiến trình này: từ nhiễu thuần, qua các bước giảm nhiễu trung gian, đến quỹ đạo hoàn chỉnh gồm chuỗi $$(v, \omega)$$ (hoặc góc khớp) theo đúng đơn vị của robot. Các bước trung gian ban đầu tuyệt đối không được gửi tới động cơ, và `observation` luôn tham gia ở mọi bước khử nhiễu (nếu che camera, mô hình không còn căn cứ hình ảnh để chọn đường vòng phù hợp).

Phép cập nhật dạng giản lược dùng để nắm trực giác trong khóa học này là:

$$
x_{t-1} = f(x_t, \text{observation})
$$

Trong đó $$x_t$$ là quỹ đạo còn nhiễu ở bước khử nhiễu thứ $$t$$ (lưu ý chỉ số $$t$$ đếm bước khử nhiễu chứ **không phải** bước thời gian điều khiển), còn $$f$$ đại diện cho bộ khử nhiễu đã học. Trong bài báo gốc, bước cập nhật đầy đủ bao gồm dự đoán thành phần nhiễu theo một lịch nhiễu (noise schedule) và cộng thêm nhiễu ngẫu nhiên để các lần lấy mẫu khác nhau có thể hội tụ về các nhánh hành động (mode) khác nhau.

Đánh đổi của quá trình lặp là độ trễ tính toán cao hơn, nhưng lợi ích cốt lõi là mô hình học được phân phối xác suất trên toàn bộ các phương án hợp lệ: mỗi lần lấy mẫu sẽ rút ra một quỹ đạo nhất quán (hoặc vòng trái, hoặc vòng phải) thay vì trộn hai hướng lại thành cú đâm thẳng. Lưu ý rằng việc lấy trung bình hai mẫu đầu ra của Diffusion Policy sẽ tái tạo lại chính lỗi đâm vật cản mà phương pháp này muốn tránh.

Tương tự khái niệm chunk ở ACT, Diffusion Policy thường áp dụng chiến lược **chân trời lùi** (receding horizon): do khử nhiễu quỹ đạo dài khá tốn kém và đoạn cuối quỹ đạo dễ lỗi thời khi môi trường thay đổi, hệ thống chỉ thực thi một đoạn ngắn ở đầu quỹ đạo rồi chạy khử nhiễu lại từ đầu. Nếu 10 bước khử nhiễu tốn 100 ms và bạn thực thi 8 bước hành động đầu ở tần số 50 Hz, cửa sổ hở vòng dài $$8/50 = 0.16$$ s — tương đương quy mô của ACT với $$k = 10$$. Do đó, watchdog 300 ms vẫn không tự ngắt nếu mô hình tiếp tục phát lệnh tiến khi có người bước vào trước xe; bạn vẫn cần lệnh dừng tường minh `0`.

Đối chiếu ngắn gọn hai kiến trúc để tránh nhầm lẫn:

- **ACT (Zhao và cộng sự):** dùng một lượt suy luận duy nhất qua transformer để sinh chunk $$k$$ hành động. Biến ẩn của CVAE giúp chọn một phong cách thực hiện nhằm tránh trung bình hóa các mẫu trái ngược. Độ trễ gồm một lượt tính mạng cộng cửa sổ hở vòng của đoạn thực thi; cơ chế temporal ensemble làm mượt lệnh nhưng cũng có thể tạo ra giá trị trung gian nhỏ giữa "tiến" cũ và "dừng" mới.
- **Diffusion Policy (Chi và cộng sự):** không hồi quy trực tiếp một lần mà khởi đầu từ nhiễu và chạy lặp bộ khử nhiễu nhiều bước cho đến khi thu được quỹ đạo sạch. Tính đa chế độ đến từ quá trình lấy mẫu ngẫu nhiên có thể hội tụ về các nhánh khác nhau (vòng trái hoặc vòng phải), đổi lại phải trả chi phí nhiều lượt tính mạng cho mỗi lần lập kế hoạch lại. Cả hai phương pháp đều xử lý được hành động đa phương án, và cả hai đều vẫn đòi hỏi watchdog cùng lệnh dừng tường minh khi triển khai trên phần cứng thật.

## Hình

![Từ nhiễu đến một quỹ đạo]({{ site.imgurl }}/generated/ch12_diffusion.png)

Từ trái sang phải là tiến trình khử nhiễu: nhiễu thuần (đỏ), giảm nhiễu (vàng), tiệm cận hành động (nhạt) và quỹ đạo hoàn chỉnh (xanh). Các mũi tên biểu diễn bước khử nhiễu chứ không phải trục thời gian chạy của robot. Ghi chú phía dưới tóm tắt trọng tâm bài học: trung bình của "rẽ trái" và "rẽ phải" là đâm thẳng vào vật cản (nguồn: Chi và cộng sự, Diffusion Policy, 2023).

## Ví dụ đọc có số

Xét hai phiên điều khiển mẫu trên Capstone tại cùng một thời điểm quyết định khi chiếc ghế nằm chính giữa, cách camera 0,40 m. Cả hai người lái cùng giữ vận tốc tiến 0,15 m/s nhưng chọn hai hướng rẽ ngược nhau:

| Mẫu | $$v$$ (m/s) | $$\omega$$ (rad/s) | Hướng đi |
| --- | --- | --- | --- |
| L | 0.15 | $$+0.50$$ | Vòng sang trái |
| R | 0.15 | $$-0.50$$ | Vòng sang phải |
| Trung bình | 0.15 | $$0.00$$ | Đâm thẳng vào ghế |

Phép trung bình làm vận tốc góc yaw triệt tiêu hoàn toàn về 0 trong khi vận tốc tiến vẫn giữ nguyên 0,15 m/s. Nếu giữ nguyên lệnh này, thời gian để xe đâm vào chiếc ghế cách 0,40 m là:

$$
\frac{0.40}{0.15} \approx 2.7\,\text{s}
$$

Trong khi đó, một bộ khử nhiễu đã học từ cả hai mẫu (dựa trên ảnh có chiếc ghế) sẽ kéo lần lấy mẫu về hẳn nhánh L hoặc hẳn nhánh R. Nếu không chắc chắn về nhánh được chọn, hành động an toàn phải là dừng lại ($$v = 0$$), tuyệt đối không lấy trung bình.

Liên hệ với biểu diễn $$x_{t-1} = f(x_t, \text{observation})$$: ở các bước khử nhiễu gần cuối, $$x_t$$ có thể chứa hành động đầu xấp xỉ $$(0.15, 0.48)$$ và hàm $$f$$ (kèm ảnh camera) tinh chỉnh nó về $$(0.15, 0.50)$$. Ở các bước khử nhiễu sớm, $$x_t$$ chỉ là nhiễu thuần nên tuyệt đối không gửi lên `/cmd_vel` — luôn phân biệt rạch ròi chỉ số bước khử nhiễu $$t$$ với nhịp điều khiển 50 Hz.

## Áp dụng cùng trực giác cho cánh tay SO-101

Xe Capstone có vector hành động 2 chiều $(v, \omega)$, còn cánh tay follower SO-101 có 6 động cơ (`pan`, `lift`, `elbow`, `wrist flex`, `wrist roll`, `gripper`). Hai mẫu gắp một khối vật thể từ hai phía tương ứng hai vector 6 chiều khác nhau; việc lấy trung bình từng khớp có thể tạo ra tư thế cánh tay đâm xuyên qua vật thể — hoàn toàn tương đồng với hiện tượng triệt tiêu yaw khi tránh ghế. Nếu huấn luyện Diffusion Policy trên tập dữ liệu của SO-101, mô hình sẽ chọn một trong hai cách gắp; nó không liên quan gì đến `/cmd_vel` của xe trừ khi bạn dùng đúng bộ khóa hành động $(v, \omega)$.

Trên tài liệu imitation learning của LeRobot tại thời điểm đối chiếu, lệnh ví dụ `lerobot-train` đang dùng `--policy.type=act`, còn `diffusion` là một lớp con (subclass) đăng ký trong mã nguồn. Ở [bài lab SO-101]({% multilang_post_url contents/chapter12/12_06_so101_arm_lab %}), bạn sẽ kiểm tra tệp cấu hình trước khi thay đổi `policy.type` (vẫn không yêu cầu GPU).

![Sáu khớp không phải vector của một VLA khác thân]({{ site.imgurl }}/generated/ch12_so101_action.png)

### Khung giải thích (nên đọc chậm): Tính tay ngân sách thời gian suy luận DDIM trên cánh tay robot chạy ở 10 Hz

Giả sử cánh tay robot cập nhật lệnh điều khiển ở **10 Hz** (mỗi nhịp chỉ có đúng `100 ms`), và ta cấu hình Diffusion Policy với $$T_o = 2$$ khung quan sát, $$T_p = 16$$ bước dự đoán và chỉ thực thi $$T_a = 8$$ bước đầu tiên:
- **Thời gian thực thi 1 khối hành động $$T_a = 8$$ bước:** $$8 \times 100\text{ ms} = \mathbf{800\text{ ms}}$$ (robot có cả 0,8 giây quỹ thời gian trước khi cần khối mới!).
- **So sánh DDPM (100 bước khử nhiễu) vs. DDIM (10 bước khử nhiễu)** khi mỗi lượt forward mạng U-Net/Transformer tốn `12 ms` trên GPU:
  - Dùng DDPM 100 bước: $$100 \times 12\text{ ms} = \mathbf{1.200\text{ ms}} > 800\text{ ms}$$ → **Quá hạn!** Robot bị khựng lại chờ tính toán!
  - Dùng DDIM 10 bước: $$10 \times 12\text{ ms} = \mathbf{120\text{ ms}} \ll 800\text{ ms}$$ → **Chạy mượt thời gian thực**, thậm chí đủ nhanh để giảm $$T_a = 2$$ bước giúp phản ứng cực nhạy trước vật cản di động!

## Lab

Mở trang dự án [diffusion-policy.cs.columbia.edu](https://diffusion-policy.cs.columbia.edu/) và trang tóm tắt [arXiv:2303.04137](https://arxiv.org/abs/2303.04137) để tìm nội dung mô tả việc mô hình hóa phân phối trên chuỗi hành động cùng hình minh họa bài toán đa phương án (không tải checkpoint hay chạy lệnh huấn luyện).

Sau đó viết một đoạn phân tích vào `lab-notes.md` về hiện tượng đa phương án trên xe Capstone: mô tả tình huống hai mẫu vòng tránh chiếc ghế từ hai phía, tính rõ lệnh trung bình cùng hệ quả đâm vào ghế (dùng bộ số trong ví dụ hoặc tự chọn bộ số mới kèm phép tính thời gian va chạm), và kết thúc bằng một câu xác nhận rõ bạn không huấn luyện mô hình hay nạp trọng số trong bài này.

**Kết quả mong đợi:** đoạn văn tự kiểm chứng được gồm đầy đủ hai hướng rẽ, góc yaw bị triệt tiêu, vận tốc tiến khác 0, nguy cơ đâm vào ghế và xác nhận không chạy huấn luyện. Một đoạn chỉ nhận xét chung chung "diffusion xử lý đa mode tốt hơn" mà không chứng minh qua phép trung bình là chưa đạt.

**Các lỗi thường gặp**

| Sai sót | Nguyên nhân |
| --- | --- |
| Gộp hai mẫu trái/phải thành một tập "trung tính" để làm sạch dữ liệu | Vô tình xóa cả hai đường né thành công và tạo ra mẫu đâm vào vật cản |
| Coi việc thiếu GPU hoặc lỗi tràn bộ nhớ là trượt lab | Bài lab đánh giá đoạn phân tích lý thuyết, không chấm quá trình huấn luyện |
| Kết luận Diffusion Policy tự động an toàn hơn vì có nhiều bước lặp | Quá trình lặp chỉ sinh ra một quỹ đạo mẫu; an toàn phần cứng vẫn phụ thuộc watchdog và lệnh dừng tường minh `0` |
| Gửi kết quả bước khử nhiễu trung gian tới động cơ vì thấy có dạng $$(v, \omega)$$ | Bước trung gian vẫn là nhiễu; chỉ quỹ đạo hoàn chỉnh sau bước cuối mới là ứng viên lệnh |

## Video tham khảo

- **Xem trước:** [Diffusion Policy: LeRobot Research Presentation #2 by Cheng Chi](https://www.youtube.com/watch?v=M03sZFfW-qU) — Hugging Face (tiếng Anh). Cheng Chi trực tiếp trình bày ý tưởng khử nhiễu quỹ đạo của Diffusion Policy trên kênh Hugging Face (xem để nắm trực giác, không cần chạy train).

## Bài tập

1. Giả sử mẫu L là $$(v, \omega) = (0.20, +0.80)$$ và mẫu R là $$(0.20, -0.40)$$ (đơn vị m/s và rad/s). Tính lệnh trung bình, cho biết chiều yaw và đánh giá có nên thực thi lệnh trung bình này khi chiếc ghế nằm chính giữa không. *Gợi ý:* trung bình là $$(0.20, +0.20)$$ — dù yaw không triệt tiêu về 0, lệnh này vẫn không thuộc hai mẫu hợp lệ ban đầu.
2. Trong biểu diễn giản lược $$x_{t-1} = f(x_t, \text{observation})$$, chỉ số $$t$$ biểu thị đại lượng gì? Viết một câu phân biệt nó với chu kỳ điều khiển 20 ms. *Gợi ý:* $$t$$ đếm bước khử nhiễu nội bộ của mạng, hoàn toàn tách biệt với trục thời gian thực thi lệnh trên robot.
3. Nếu bạn thực thi 8 bước đầu của quỹ đạo đã khử nhiễu ở tần số 50 Hz, cửa sổ hở vòng kéo dài bao lâu và watchdog 300 ms có kích hoạt trong khoảng thời gian đó không? *Gợi ý:* $$8/50 = 0.16$$ s; watchdog không kích hoạt vì lệnh vẫn đang được phát đều — nếu quỹ đạo hướng vào ghế, bắt buộc phải gửi tường minh lệnh `0`.
4. So với một lượt suy luận thuận của ACT, cơ chế rút mẫu từ nhiễu của Diffusion Policy phải trả thêm chi phí gì tại mỗi lần lập kế hoạch lại? *Gợi ý:* chi phí độ trễ do phải chạy lặp mạng khử nhiễu nhiều lần thay vì một lượt duy nhất.
5. Nếu chiếc ghế chỉ còn cách 0,15 m và lệnh trung bình giữ $$v = 0.15$$ m/s, $$\omega = 0$$, sau bao lâu xe sẽ chạm ghế và khoảng thời gian đó dài hay ngắn hơn cửa sổ hở vòng 0,16 s? *Gợi ý:* $$0.15/0.15 = 1.0$$ s — dài hơn cửa sổ 0,16 s nên xe chưa đâm ngay trong một nhịp hở vòng, nhưng đoạn đầu đã đẩy xe hướng thẳng vào vật cản và cần cắt bằng lệnh dừng `0`.

## Đọc thêm

- [Trang dự án Diffusion Policy](https://diffusion-policy.cs.columbia.edu/) — xem ý tưởng cốt lõi và hình minh họa (không chạy phần huấn luyện).
- [Chi và cộng sự, arXiv:2303.04137](https://arxiv.org/abs/2303.04137) — đọc phần tóm tắt để nắm rõ tuyên bố của tác giả và lịch nhiễu thực tế đứng sau phác thảo $$f$$.
