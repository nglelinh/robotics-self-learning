---
layout: post
title: "Học bắt chước và tổng quan ACT"
chapter: "12"
order: 2
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter12
lesson_type: required
draft: false
---

Thời lượng: **~70 phút**, tập trung đọc kỹ phần tóm tắt (abstract) của bài báo gốc và phân tích phép tính số học về 0,2 s chuyển động hở vòng (không chạy huấn luyện).

Nếu bạn huấn luyện một mạng nơ-ron đơn giản kiểu Hành vi Nhân bản (Behavioral Cloning) dự đoán **từng bước hành động một** ($$o_t \mapsto a_t$$), một căn bệnh chết người lập tức xuất hiện: **sai số cộng dồn (compounding errors)**. Chỉ cần tay máy lệch 2 mm ở giây thứ 3, nó rơi vào trạng thái chưa từng thấy trong dữ liệu mẫu, rồi lệch thành 1 cm ở giây thứ 4 và gắp trượt hoàn toàn! Kiến trúc **ACT (Action Chunking with Transformers)** giải quyết căn bệnh đó bằng một ý tưởng cực kỳ thông minh: thay vì dự đoán 1 bước, hãy dự đoán hẳn **một khối $$k$$ bước hành động liên tiếp** và làm mượt bằng tổ hợp thời gian.

## Kiến thức cần nhớ: Ba trụ cột của Chính sách ACT (Action Chunking with Transformers)

1. **Phân khối Hành động (Action Chunking — dự đoán $$k$$ bước cùng lúc)**:
   Giảm độ dài hiệu dụng của bài toán xuống $$k$$ lần (ví dụ với $$k = 100$$ bước ở 50 Hz = 2 giây), cắt mạnh sai số tích lũy và xử lý mượt các đoạn dừng tạm tự nhiên của người trình diễn.
2. **CVAE (Conditional Variational Autoencoder) xử lý Dữ liệu Đa mẫu (Multimodal)**:
   Cùng một vật trên bàn, người trình diễn lúc thì vòng tay từ trái sang, lúc thì từ phải sang. Nếu chỉ hồi quy MSE thuần túy, mạng sẽ lấy *trung bình* hai đường đi và đâm thẳng vào vật cản! Biến ẩn $$z$$ của CVAE giúp mô hình biểu diễn trọn vẹn nhiều phong cách hoàn thành khác nhau.
3. **Tổ hợp Thời gian (Temporal Ensembling)**:
   Ở mỗi bước $$t$$, mô hình kết hợp trung bình có trọng số mũ $$w_i = \exp(-m \cdot i)$$ giữa dự đoán mới nhất và các dự đoán còn dư từ những bước trước đó để chuyển động cánh tay êm mượt không giật cục.

## Mục tiêu

Sau bài học này, bạn sẽ định nghĩa được **học bắt chước hành vi** (behavior cloning) là ánh xạ từ quan sát (observation) sang hành động (action) học từ dữ liệu mẫu thay vì hàm phần thưởng (reward). Bạn nắm rõ đầu ra của mô hình ACT (Zhao và cộng sự, RSS 2023): một khối (**chunk**) gồm $$k$$ hành động tương lai do kiến trúc transformer sinh ra, được huấn luyện theo khung conditional variational autoencoder (CVAE) để xử lý nhiều cách thực hiện hợp lệ cùng lúc. Bạn tự tính được cửa sổ hở vòng cho $$k = 10$$ ở tần số 50 Hz, đối chiếu trực tiếp với watchdog chương 08, và giải thích bản chất của cơ chế kết hợp theo thời gian (temporal ensemble) là phép lấy trung bình các chunk chồng lấp.

## Kiến thức cần trước

Đã hoàn thành dataset card ở bài 12-01 (camera, $$v$$ theo m/s, $$\omega$$ theo rad/s và `fps`), hiểu cơ chế watchdog 300 ms trên firmware tự đưa động cơ về 0 khi mất khung dữ liệu, và biết cách đọc tóm tắt bài báo khoa học. Bài này không yêu cầu GPU, phần cứng ALOHA hay cài đặt thư viện huấn luyện.

## Vì sao bài này nằm trên lộ trình

Cho tới hết chương Nav2, lệnh trên `/cmd_vel` luôn là từng message `Twist` đơn lẻ sinh ra ở mỗi nhịp bởi một bộ điều khiển tường minh. Với các policy học máy như ACT, dạng đầu ra thay đổi: thay vì chỉ dự đoán cho 20 ms kế tiếp, mạng xuất ra một chuỗi ngắn các hành động tương lai để robot thực thi liên tiếp trước khi truy vấn lại mạng. Chuỗi đó là một đoạn chuyển động **hở vòng** (open-loop). Cầu nối Capstone vẫn truyền tiếp được các lệnh này, nhưng tự thân nó không đảm bảo an toàn: watchdog 300 ms chỉ kích hoạt khi *mất khung truyền*, trong khi một policy đang chạy bình thường vẫn có thể phát đều đặn phần còn lại của một chunk nguy hiểm. Bài học này giúp bạn phân tích rủi ro đó trước khi bước vào huấn luyện.

## Khái niệm

**Behavior cloning** là bài toán học có giám sát: con người điều khiển robot để thu thập các cặp `(observation, action)` mẫu, sau đó mạng nơ-ron được huấn luyện để tái tạo lại hành động tương ứng khi gặp quan sát tương tự — không cần định nghĩa hàm reward và không bắt buộc có bộ mô phỏng. Chất lượng mô hình phụ thuộc trực tiếp vào chất lượng log dữ liệu (đơn vị, đồng hồ và trạng thái watchdog như ở bài 12-01). Nếu dữ liệu huấn luyện thuộc vector khớp của cánh tay SO-101 rồi đem áp lên xe Capstone, lỗi sai hình thái phần cứng vẫn xảy ra y nguyên.

Một đầu hồi quy đơn giản huấn luyện bằng sai số bình phương gặp hạn chế nghiêm trọng khi có nhiều cách giải quyết hợp lệ cho cùng một tình huống (ví dụ một mẫu đi vòng sang trái chiếc cốc, mẫu kia đi vòng sang phải — giá trị trung bình của hai hành động lại đâm thẳng vào chiếc cốc). Trong bài báo *Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware*, Zhao, Kumar, Levine và Finn giải quyết vấn đề này bằng cách huấn luyện policy như một **conditional variational autoencoder (CVAE)**: một biến ẩn cho phép mô hình chọn một "phong cách" thực hiện cụ thể, sau đó bộ giải mã transformer dự đoán chuỗi hành động phù hợp với phong cách đó cùng ảnh camera và trạng thái khớp hiện tại. Khi triển khai thực tế, phần encoder dùng lúc huấn luyện được bỏ đi và biến ẩn được lấy từ phân phối tiên nghiệm (thường đặt tại tâm 0). Biến ẩn giúp mô hình cam kết theo một phương án nhất quán chứ không phải chứng nhận an toàn hay cảm biến tránh va chạm.

Đầu ra của transformer là một **chunk** gồm $$k$$ hành động tương lai liên tiếp — đây là ý nghĩa của tên gọi **Action Chunking**. Lý do thực tiễn rất rõ ràng: ở tần số điều khiển 50 Hz, mỗi chu kỳ chỉ dài 20 ms; nếu mạng mất 80 ms để suy luận thì việc hỏi mạng từng bước sẽ luôn trễ bốn chu kỳ. Dự đoán một chunk 10 bước giúp che phủ thời gian suy luận và cho robot thực thi liên tục trong khi chờ lượt tính kế tiếp. Tuy nhiên, cái giá phải trả là robot chạy hở vòng suốt khoảng thời gian chưa lập kế hoạch lại. Trong bài báo gốc, tác giả dùng hệ thống phần cứng **ALOHA** (cặp cánh tay leader-follower giá thấp cho thao tác hai tay); ở đây ta không chế tạo ALOHA mà mượn khái niệm chunking để phân tích tác động lên xe vi sai Capstone.

**Temporal ensemble** là kỹ thuật làm mượt ở giai đoạn phát lại: policy được gọi đủ dày sao cho nhiều chunk dự đoán chồng lấp lên cùng một thời điểm tương lai, và lệnh thực thi là trung bình có trọng số của các dự đoán đó (ưu tiên chunk mới hơn theo trọng số suy giảm). Mục đích là giảm giật cục khi hai lần suy luận liên tiếp hơi lệch nhau — không phải cơ chế dừng khẩn cấp, vì trung bình giữa "đang tiến" và "dừng" vẫn là "bò chậm về trước". Lệnh dừng thực sự phải là một giá trị `0` chủ động hoặc ngắt nguồn/timeout.

Cần đặt rõ mối quan hệ giữa watchdog và chunk: watchdog chương 08 ngắt động cơ sau 300 ms không có khung serial hợp lệ (bảo vệ khi tuột cáp USB hoặc treo tiến trình). Nó **không** bảo vệ được tình huống tiến trình policy vẫn chạy khỏe và tiếp tục gửi các bước còn lại của một chunk đi thẳng ngay khi có người vừa bước vào trước mặt xe — vì dưới góc nhìn firmware, các khung truyền vẫn đều đặn. Do đó, cơ chế cắt chunk phải nằm ngay ở tầng phát lệnh: lập tức hủy các bước còn lại và xuất bản $$(0, 0)$$. Ngoài ra, tần suất lập kế hoạch lại cũng quyết định độ rủi ro: chỉ hỏi lại mạng khi hết chunk khiến toàn bộ chunk trở thành hở vòng, trong khi hỏi dày hơn giúp loại bỏ dự đoán cũ sớm hơn nhưng vẫn không thay thế được lệnh dừng tường minh `0`.

## Hình

![ACT biến ảnh và trạng thái khớp thành một chunk]({{ site.imgurl }}/generated/ch12_act.png)

Khối bên trái biểu diễn đầu vào điều kiện của mô hình (ảnh và trạng thái khớp trong bài báo gốc — tương ứng với ảnh camera và vận tốc đo $$(v, \omega)$$ trên Capstone). Khối giữa là chunk gồm $$k$$ hành động, còn khối phải là quá trình thực thi rồi lập kế hoạch lại. Ghi chú đỏ nhắc nhở điều quan trọng nhất khi ứng dụng lên phần cứng: chunk mang bản chất hở vòng nên luôn cần đi kèm watchdog và cơ chế dừng khẩn tường minh (nguồn tham khảo: Zhao và cộng sự, ACT / ALOHA, 2023).

## Ví dụ đọc có số

Xét một chunk minh họa với $$k = 10$$ ở tần số điều khiển $$f = 50$$ Hz:

$$
T_{\text{open}} = \frac{k}{f} = \frac{10}{50} = 0.2\,\text{s}
$$

Nếu thực thi trọn vẹn cả chunk rồi mới quan sát lại, cửa sổ hở vòng dài 0,2 s. Bảng dưới đây là một chunk hành động giả định cho Capstone (bắt đầu từ $$t = 0$$, mỗi bước cách nhau 0,02 s):

| Bước | Thời gian (s) | $$v$$ (m/s) | $$\omega$$ (rad/s) |
| --- | --- | --- | --- |
| 0 | 0.00 | 0.25 | 0.00 |
| 1 | 0.02 | 0.25 | 0.00 |
| 2 | 0.04 | 0.25 | 0.00 |
| 3 | 0.06 | 0.25 | 0.00 |
| 4 | 0.08 | 0.24 | 0.00 |
| 5 | 0.10 | 0.24 | 0.00 |
| 6 | 0.12 | 0.20 | 0.00 |
| 7 | 0.14 | 0.15 | 0.00 |
| 8 | 0.16 | 0.10 | 0.00 |
| 9 | 0.18 | 0.05 | 0.00 |

Giả sử tại $$t = 0.08$$ s (bước 4), có người bước vào trước camera. Sáu bước còn lại (từ bước 4 đến bước 9) tương ứng 0,12 s lệnh đã lên lịch sẵn. Lấy vận tốc đại diện khoảng 0,20 m/s, quãng đường xe tiếp tục bị đẩy đi là:

$$
0.20 \times 0.12 = 0.024\,\text{m}
$$

tức khoảng 2,4 cm (chưa kể quán tính phanh của bánh xe). Tại thời điểm 0,08 s, watchdog 300 ms hoàn toàn không kích hoạt vì cầu nối vẫn đang đều đặn gửi các bước 4, 5, 6. Để dừng ngay lập tức, hệ thống phải chủ động hủy chunk và xuất bản `0` (nhanh hơn nhiều so với việc ngừng gửi rồi chờ hết 300 ms).

Với độ dài chunk lớn hơn — chẳng hạn 100 bước ở 50 Hz thường xuất hiện trong tài liệu ACT:

$$
\frac{100}{50} = 2.0\,\text{s}
$$

cửa sổ hở vòng lên tới 2 giây nếu không lập kế hoạch lại sớm — hoàn toàn không an toàn cho xe di động chạy trong hành lang. Do đó không thể áp dụng máy móc độ dài chunk của bài báo gốc sang xe Capstone.

Xét thêm tác động của temporal ensemble tại một thời điểm chồng lấp: chunk cũ dự đoán $$v = 0.25$$ m/s tại $$t = 0.20$$ s, còn chunk mới (sau khi thấy vật cản) dự đoán $$v = 0.00$$ m/s. Trung bình cộng vẫn cho ra $$0.125$$ m/s; ngay cả khi dùng trung bình có trọng số nghiêng về chunk mới (tỉ lệ 3/4 mới và 1/4 cũ), kết quả vẫn là $$0.0625$$ m/s — xe vẫn tiến lên. Ensemble chỉ làm mượt lệnh chứ không thay thế được lệnh dừng `0`.

### Giải thích: Tính tay trọng số Tổ hợp Thời gian (Temporal Ensembling) trong ACT

Giả sử tại bước thời gian $$t = 10$$, ta đang có **3 dự đoán** cho góc khớp vai $$q_1(10)$$ đến từ 3 lần suy luận gần nhất (với hệ số suy giảm $$m = 0{,}5$$):
- Dự đoán từ bước $$t = 10$$ (mới nhất, tuổi $$i = 0$$): $$\hat{a}^{(0)} = 42{,}0^\circ$$, trọng số $$w_0 = e^{-0{,}5 \times 0} = \mathbf{1{,}000}$$.
- Dự đoán từ bước $$t = 9$$ (tuổi $$i = 1$$): $$\hat{a}^{(1)} = 40{,}0^\circ$$, trọng số $$w_1 = e^{-0{,}5 \times 1} \approx \mathbf{0{,}607}$$.
- Dự đoán từ bước $$t = 8$$ (tuổi $$i = 2$$): $$\hat{a}^{(2)} = 39{,}0^\circ$$, trọng số $$w_2 = e^{-0{,}5 \times 2} \approx \mathbf{0{,}368}$$.

**Tính hành động thực tế gửi xuống động cơ:**
$$a_{10}^* = \frac{1{,}000(42{,}0) + 0{,}607(40{,}0) + 0{,}368(39{,}0)}{1{,}000 + 0{,}607 + 0{,}368} = \frac{42{,}00 + 24{,}28 + 14{,}35}{1{,}975} = \frac{80{,}63}{1{,}975} \approx \mathbf{40{,}83^\circ}.$$

Thay vì nhảy giật từ $$40^\circ$$ lên $$42^\circ$$ rồi lại tụt xuống, cơ chế trung bình mũ tạo ra quỹ đạo góc khớp cực kỳ mượt mà cho động cơ servo!

## Lab

Bài thực hành này chỉ yêu cầu đọc hiểu và phân tích (không tải trọng số hay chạy huấn luyện).

Mở trang tóm tắt bài báo [Zhao và cộng sự, arXiv:2304.13705](https://arxiv.org/abs/2304.13705) và ghi bốn mục sau vào `lab-notes.md`:

1. Tên tác giả và thông tin hội nghị xuất bản (bài học dùng RSS 2023; nếu trích trực tiếp từ trang arXiv thì giữ nguyên chữ trên trang).
2. Đầu ra của phương pháp là gì: một chunk gồm nhiều hành động tương lai thay vì từng lệnh đơn lẻ (nêu rõ cụm từ "action chunking" từ bài báo gốc hoặc ghi rõ nếu bạn diễn giải lại).
3. Vai trò của phần cứng trong tiêu đề: hệ thống giàn thu mẫu hai tay chi phí thấp ALOHA (không phải phần cứng cần mua cho khóa này).
4. Phân tích độ dài chunk cho xe Capstone với phép tính tường minh: $$k = 10$$ ở 50 Hz cho $$T_{\text{open}} = 0.2$$ s, kèm một câu phân biệt rõ khi nào watchdog ngắt (khi bên xuất bản ngừng hoạt động) và khi nào bắt buộc gửi lệnh `0` tường minh (khi bên xuất bản vẫn chạy nhưng chunk hiện tại không còn an toàn).

**Kết quả mong đợi:** bản ghi chép dài khoảng nửa trang có phép chia ra 0,2 s, tách bạch lệnh dừng tường minh với watchdog timeout và không kèm log huấn luyện.

**Các lỗi thường gặp**

| Tình huống | Cách xử lý |
| --- | --- |
| Tự ý chạy script huấn luyện trên laptop khiến tràn bộ nhớ (OOM) | Dừng ngay; bài học không yêu cầu huấn luyện trên máy không có GPU chuyên dụng |
| Ghi chú kết luận chung chung "watchdog sẽ xử lý chunk lỗi" | Viết lại rõ: watchdog chỉ phát hiện trạng thái mất tín hiệu, không phát hiện được chunk xấu vẫn đang truyền đều |
| Chép một số $$k$$ từ tệp cấu hình bất kỳ mà thiếu phép chia theo tần số | Luôn quy đổi $$k / f$$ ra giây để đánh giá quãng đường hở vòng thực tế |
| Hiểu nhầm ALOHA là thiết bị cần đặt mua tiếp theo | ALOHA chỉ là hệ thống thu dữ liệu của bài báo; robot của khóa vẫn là Capstone |

## Video tham khảo

- **Xem trước:** [ALOHA and ACT: LeRobot Research Presentation #1 by Alexander Soare](https://www.youtube.com/watch?v=ft73x0LfGpM) — Hugging Face (tiếng Anh). Trình bày trực tiếp về bài báo ACT và hệ thống ALOHA trên kênh Hugging Face.
- [Core Concepts: Imitation Learning](https://www.youtube.com/watch?v=GDmhrAHxgQE) — Sanjiban Choudhury (tiếng Anh). Giải thích lý do học bắt chước không thể đơn thuần lấy trung bình các mẫu hành động — nền tảng cho kiến trúc của ACT.

## Bài tập

1. Diễn đạt khái niệm behavior cloning trong một câu gắn trực tiếp với các khóa dữ liệu của xe Capstone. *Gợi ý:* là ánh xạ nhận ảnh camera (và có thể kèm $$v, \omega$$ đo được) để dự đoán cặp lệnh $$v, \omega$$ mà người điều khiển đã gửi, không sử dụng hàm reward.
2. Khi hai phiên mẫu đi vòng sang hai phía của cùng một chiếc cốc, mô hình hồi quy bình phương sai số sẽ lấy trung bình hai hướng. Biến ẩn của CVAE giải quyết vấn đề gì mà phép trung bình không làm được? *Gợi ý:* giúp mô hình cam kết theo một hướng đi nhất quán thay vì đâm vào giữa (tuy nhiên vẫn không thay thế được cảm biến đo khoảng cách).
3. Tính cửa sổ hở vòng khi $$k = 100$$ ở 50 Hz và đánh giá có nên áp dụng nguyên văn cho Capstone chạy trong hành lang hay không. *Gợi ý:* $$100/50 = 2.0$$ s — quá dài và nguy hiểm cho hành lang; hãy đề xuất một giá trị $$k$$ nhỏ hơn kèm thời gian tương ứng.
4. Tại cùng một mốc thời gian, chunk cũ dự đoán $$v = 0.25$$ m/s còn chunk mới dự đoán $$v = 0$$ m/s. Nếu gửi giá trị trung bình cộng, bánh xe đã dừng chưa và cần gửi gì khi có người xuất hiện trước camera? *Gợi ý:* chưa dừng (trung bình là $$0.125$$ m/s); cần hủy chunk và xuất bản tường minh $$v = 0, \omega = 0$$.
5. Cầu nối vẫn gửi khung serial đều đặn mỗi 20 ms từ phần còn lại của một chunk đi thẳng ngay sau khi phát hiện vật cản. Watchdog 300 ms có tự ngắt động cơ không? *Gợi ý:* không, vì các khung liên tục đặt lại bộ định thời; phải chủ động gửi lệnh `0` hoặc dừng hẳn bên xuất bản.

## Đọc thêm

- [Zhao và cộng sự, Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware](https://arxiv.org/abs/2304.13705) — đọc phần tóm tắt và sơ đồ kiến trúc phương pháp (bỏ qua phần huấn luyện trong kho mã nguồn).
- [Docs LeRobot](https://huggingface.co/docs/lerobot/index) — xem mục giới thiệu ACT trong danh sách các policy được hỗ trợ.
