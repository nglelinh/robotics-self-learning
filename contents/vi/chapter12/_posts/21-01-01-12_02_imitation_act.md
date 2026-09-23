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

Thời lượng: **~70 phút**. Phần lớn là đọc chậm một abstract và một ghi chú số về 0,2 s chuyển động hở vòng. Không có lần train nào trong 70 phút đó.

## Mục tiêu

Bạn định nghĩa behavior cloning là một ánh xạ từ observation sang action, khớp trên demonstration chứ không trên reward. Bạn nói được ACT (Zhao và cộng sự, RSS 2023) thực sự xuất ra cái gì: một chunk $$k$$ action tương lai từ một transformer, luyện như conditional variational autoencoder để hơn một kiểu demonstration có chỗ đứng. Bạn tính cửa sổ hở vòng cho $$k = 10$$ ở 50 Hz, nối cửa sổ đó với watchdog chương 08, và giải thích temporal ensemble là trung bình các chunk chồng lên nhau, không chứng minh lại cả bài báo.

## Kiến thức cần trước

Dataset card bài 12-01 nằm trong sổ: camera, $$v$$ theo m/s, $$\omega$$ theo rad/s, một fps. Bạn biết firmware đưa động cơ về 0 sau 300 ms kể từ khung tốt cuối cùng. Bạn đọc được một abstract. Không cần GPU, không cần phần cứng ALOHA, không cần cài xong policy. Máy bạn học báo hết bộ nhớ thì bạn học đó đã bắt đầu nhầm bài.

## Vì sao bài này nằm trên lộ trình

Cho tới tour Nav2, lệnh trên `cmd_vel` là một `Twist` mỗi nhịp, do một bộ điều khiển bạn gọi được tên. Policy học đổi hình dạng lệnh đó. ACT không phát "20 ms tới". Nó phát một danh sách ngắn các action tương lai, rồi để robot thực hiện trong lúc mạng không bị hỏi lại. Danh sách đó là một loạt chuyển động hở vòng. Cầu Capstone chuyển tiếp được loạt đó. Nó không làm loạt đó an toàn. Timeout 300 ms vẫn cần, và một mình nó không đủ: timeout nổ khi khung ngừng đến, còn policy còn sống thì khung vẫn đến hết chunk xấu. Bài này là cách bạn đọc loạt xung đó trước khi ai đó rủ bạn train.

## Khái niệm

Behavior cloning là bắt chước có giám sát. Bạn thu demonstration trong đó một người lái. Mỗi cặp lưu lại là một observation và action người đã gửi lúc đó. Policy được luyện để, khi nhìn observation, nó tái tạo action. Định nghĩa không có hàm reward và không bắt buộc simulator. Chất lượng ánh xạ là chất lượng log: đơn vị, đồng hồ, và câu chuyện timeout của bài trước. Log có action $$(v, \omega)$$ và robot lúc phát nhận $$(v, \omega)$$ thì cloning ít nhất đang nhắm đúng thân. Clone vector khớp SO-101 rồi phát trên Capstone vẫn là lỗi embodiment, chỉ là hàm giờ đắt hơn.

Một đầu hồi quy đơn có kiểu hỏng cùn, bài sau sẽ đặt vào giữa, và ACT đã trả lời trước. Hai demonstration của một việc thường không đồng ý. Một người đi vòng cốc bên trái, người kia bên phải. Trung bình các action đó chĩa vào cốc. Mạng luyện bằng bình phương sai số bị kéo về trung bình đó. Zhao, Kumar, Levine và Finn, trong *Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware*, luyện policy như một conditional variational autoencoder. Một biến ẩn được phép chọn một kiểu. Bộ giải mã, một transformer, rồi dự đoán action khớp với kiểu đó và với ảnh cùng trạng thái khớp hiện tại. Lúc phát, encoder đã nhìn demonstration không còn. Biến ẩn lấy từ phân phối tiên nghiệm, thường đơn giản đặt ở tâm. Biến ẩn là cách mô hình được phép cam kết một cách làm. Nó không phải giấy chứng nhận cách đó an toàn, và không phải cảm biến va chạm thứ hai.

Đầu ra của transformer đó là một **chunk**: $$k$$ action tương lai, không phải một action. Chunking là nửa thực dụng trong tên phương pháp, "action chunking". Tính một policy tốn thời gian. Ở 50 Hz, chu kỳ điều khiển là 20 ms. Mạng cần 80 ms thì policy buộc trả lời mỗi chu kỳ đã trễ bốn nhịp. Chunk mười action phủ 80 ms đó và hơn nữa, nên robot thực hiện danh sách đã tính trong lúc danh sách sau được tạo. Cái giá là danh sách hở vòng cho đến khi bạn lập kế hoạch lại. Động cơ không biết danh sách là một phỏng đoán. ALOHA, phần cứng trong bài báo, là giàn leader-follower hai tay giá thấp, dùng để thu demonstration cho các việc nhỏ cần hai tay. Bạn không dựng ALOHA. Bạn mượn ý tưởng chunk và hỏi chunk làm gì với khung vi sai đã có watchdog.

Temporal ensemble là mẹo lúc phát, và ở đây chỉ là một ý. Policy được hỏi đủ dày để vài chunk chồng trên cùng một thời điểm tương lai. Lệnh thực sự gửi đi là trung bình các dự đoán đó. Chunk mới được tin hơn chunk cũ. Bài báo dùng trọng số suy giảm cho việc này, và bạn không cần hằng số suy giảm. Mục đích của trung bình là giấu rung khi các lần hỏi liên tiếp lệch nhau một chút. Mục đích không phải dừng robot. Trung bình của "tiến" và "dừng" là "bò". Ensemble là bộ làm mượt. Lệnh dừng phải là số 0 bạn chủ đích xuất bản, hoặc một timeout vì việc xuất bản đã ngừng.

Đặt watchdog cạnh chunk, vì hai đồng hồ không đồng ý. Chương 08 xóa động cơ khi không có khung hợp lệ trong 300 ms. Việc đó cứu bạn khi cáp USB rơi hoặc tiến trình policy chết. Nó không cứu bạn khi tiến trình vẫn khỏe và tiếp tục đăng phần còn lại của chunk bảo tiến, trong lúc một người bước vào trước mặt. Với firmware, các khung đó còn tươi. Việc cắt phải nằm ở chỗ mở chunk: bỏ các bước còn lại, xuất bản $$(0, 0)$$, để động cơ thấy một số 0 thật. Tần số lập kế hoạch lại là nửa kia. Bạn chỉ hỏi mạng khi chunk hết thì cửa sổ hở vòng là cả chunk. Bạn hỏi dày hơn và lấy ensemble phần chồng thì một dự đoán xấu được nghỉ sớm hơn, và bạn vẫn cần một số 0 tường minh khi cảnh không còn là cảnh chunk đã giả định.

## Hình

![ACT biến ảnh và trạng thái khớp thành một chunk]({{ site.imgurl }}/generated/ch12_act.png)

Hộp trái là observation mà bài báo lấy làm điều kiện: ảnh và trạng thái khớp. Trên Capstone, thứ tương ứng trung thực là camera cộng $$(v, \omega)$$ đo được, không phải vector sáu khớp bạn không có. Hộp giữa là chunk $$k$$ action. Hộp phải nói thực hiện, rồi lập kế hoạch lại. Dòng đỏ là phần sinh viên bỏ qua khi tóm tắt bài báo thành "robot học được việc": chunk là hở vòng, và nó vẫn cần timeout cùng một lệnh dừng. Chân hình trỏ Zhao và cộng sự, ACT / ALOHA, 2023. Đó là trích dẫn, không phải danh mục linh kiện.

## Ví dụ đọc có số

Dùng một chunk để dạy, không dùng bảng siêu tham số của bài báo. Lấy $$k = 10$$ và tần số điều khiển 50 Hz:

$$
T_{\text{open}} = \frac{k}{f} = \frac{10}{50} = 0.2\,\text{s}
$$

Hai phần mười giây là loạt hở vòng nếu bạn thực hiện chunk đến hết rồi mới nhìn lại. Chunk dưới đây là action Capstone theo đơn vị dataset card, bắt đầu tại $$t = 0$$. Mỗi bước 0,02 s.

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

Tại $$t = 0.08$$ s, bước 4, một người bước vào trước camera. Bước 4 đến 9 vẫn nằm trong danh sách. Đó là 0,12 s lệnh còn thừa. Quãng đường ước lượng, lấy 0,20 m/s làm đại diện sáu bước đó, là

$$
0.20 \times 0.12 = 0.024\,\text{m}
$$

khoảng 2,4 cm hành trình được lệnh, chưa kể quãng dừng của chính bánh. Hai centimet không phải sự an ủi nếu vật cản là một bàn chân. Lần gọi mạng sau chỉ được hẹn ở cuối chunk thì quyết định sau đến lúc 0,2 s. Watchdog không nổ lúc 0,08 s, vì cầu vẫn đang giao bước 4, 5, 6 đúng giờ. Thứ cắt loạt xung là một lệnh dừng: xuất bản số 0 cho phần còn lại của cửa sổ, hoặc ngừng xuất bản và chờ hết 300 ms. Chờ timeout là cách chậm hơn. Xuất bản số 0 là cách khớp với "có người trước mặt ngay bây giờ".

Chunk dài hơn làm cùng một ý to hơn. Tài liệu ACT thường bàn chunk cỡ một trăm bước ở 50 Hz, tức

$$
\frac{100}{50} = 2.0\,\text{s}
$$

hở vòng nếu bạn không lập kế hoạch lại sớm. Hai giây chuyển động tiến đã cam kết không thuộc về Capstone trong hành lang. Biết bài báo dùng chunking không có nghĩa chấp nhận độ dài chunk của bài báo trên đế của bạn.

Temporal ensemble trên một thời điểm chồng: chunk cũ vẫn nói $$v = 0.25$$ tại $$t = 0.20$$, chunk mới, hỏi sau khi người đã xuất hiện, nói $$v = 0.00$$. Trung bình cộng là $$0.125$$ m/s. Đó không phải dừng. Kể cả trung bình có trọng số nghi về chunk mới, chẳng hạn ba phần tư giá trị mới và một phần tư giá trị cũ, vẫn là $$0.0625$$ m/s, vẫn tiến. Ensemble làm lệnh nhỏ lại. Nó không thay số 0.

## Lab

Chỉ đọc. Đừng clone cấu hình train, đừng tải trọng số, đừng mở job vì một GPU tình cờ rảnh ở phòng lab bạn không có.

Mở trang abstract: [Zhao và cộng sự, arXiv:2304.13705](https://arxiv.org/abs/2304.13705). Từ abstract và tiêu đề, viết bốn dòng vào `lab-notes.md`:

1. Tác giả và dòng hội nghị bạn thấy (các ghi chú này dùng RSS 2023; muốn trích thẳng trang abstract thì giữ đúng chữ trên trang).
2. Phương pháp dự đoán cái gì: một chunk action tương lai, không phải một lệnh kế tiếp. Cụm "action chunking" phải xuất hiện vì bạn tìm thấy nó, không phải vì chép mù câu này. Diễn giải thì nói là diễn giải.
3. Phần cứng trong tiêu đề dùng để làm gì: giàn demonstration hai tay giá thấp (ALOHA), thứ bạn không mua và không lắp.
4. Hệ quả độ dài chunk cho Capstone, phép tính nhìn thấy được: $$k = 10$$, 50 Hz, $$T_{\text{open}} = 0.2$$ s, và một câu chỉ rõ ai cắt chunk xấu. Watchdog cắt khi bên xuất bản chết. Bên xuất bản còn sống mà chunk xấu thì phải bị cắt bằng một số 0 tường minh.

**Kỳ vọng.** Một ghi chú khoảng nửa trang. Con số 0,2 s xuất hiện, kèm phép chia sinh ra nó. Lệnh dừng được gọi tên riêng với timeout. Không có log train.

**Các kiểu hỏng**

| Chuyện đã xảy ra | Bạn làm gì |
| --- | --- |
| Bạn mở script train và tiến trình chết vì hết bộ nhớ | Tắt nó. Lỗi đó không phải bài nộp, cũng không phải bằng chứng bạn "suýt" train ACT. Laptop không có GPU tử tế chưa bao giờ được kỳ vọng luyện xong bài báo này |
| Ghi chú nói "watchdog lo chunk" rồi dừng | Viết lại câu. Watchdog lo sự im lặng. Chunk còn đang chảy không phải im lặng |
| Bạn chép độ dài chunk từ một file config ngẫu nhiên và bỏ phép chia | Lab là hệ quả tính bằng giây, trên tần số điều khiển của bạn. Một $$k$$ không đơn vị không cho biết đế đi được bao xa |
| Ghi chú coi ALOHA là món mua tiếp theo | ALOHA là giàn thu dữ liệu của bài báo. Robot của khóa học này vẫn là Capstone |

## Bài tập

1. Viết behavior cloning thành một câu có dùng khóa của bạn. Gợi ý: ánh xạ nhận ảnh camera, và có thể cả $$v$$, $$\omega$$ đo được, rồi trả về $$v$$ và $$\omega$$ lệnh mà người demo đã gửi. Reward không có trong câu.
2. Hai demonstration đi hai bên một cái cốc, đầu bình phương sai số lấy trung bình chúng. Biến ẩn CVAE mua cho bạn cái gì mà trung bình không có? Gợi ý: một cách để cam kết action của một bên. Nó không mua một cảm biến khoảng cách, và cái ghế ở bài sau chính là trung bình này vẽ xuống sàn.
3. Tính lại thời gian hở vòng cho $$k = 100$$ ở 50 Hz, rồi nói bạn có thực hiện cả chunk đó trên Capstone trong hành lang hay không. Gợi ý: $$100/50 = 2.0$$ s. Câu trả lời cho hành lang là không. Nêu chunk ngắn hơn mà bạn chịu bàn, và thời gian của nó.
4. Tại một mốc thời gian, chunk cũ dự đoán $$v = 0.25$$ và chunk mới dự đoán $$v = 0$$. Bạn gửi trung bình cộng. Bánh đã dừng chưa? Gợi ý: chưa. Trung bình là $$0.125$$ m/s. Nói bạn sẽ xuất bản gì nếu có người trong camera.
5. Cầu phát một khung serial mới mỗi 20 ms, mỗi khung là bước kế của một chunk vẫn bảo tiến, sau khi bạn đã thấy vật cản. Timer 300 ms có hết hạn không? Gợi ý: không, khung còn tươi nên timer cứ reset. Cách sửa là xuất bản số 0 hoặc dừng bên xuất bản. Vừa nói chuyện với động cơ vừa chờ timeout thì không được gì.

## Đọc thêm

- [Zhao và cộng sự, Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware](https://arxiv.org/abs/2304.13705). Đọc abstract và các hình phương pháp. Hướng dẫn train trong repository của bài báo nằm ngoài lab này.
- [Docs LeRobot](https://huggingface.co/docs/lerobot/index). ACT được gọi tên ở đó như một policy để đọc. Gọi tên là toàn bộ việc dùng trang đó tối nay.
