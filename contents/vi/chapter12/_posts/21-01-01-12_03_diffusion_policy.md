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

Thời lượng: **~65 phút**. Bạn đọc một trang dự án, nhìn một phép trung bình, và viết một đoạn. Bạn không khử nhiễu cái gì trên GPU.

## Mục tiêu

Bạn giải thích vì sao diffusion policy sinh một quỹ đạo action bằng khử nhiễu lặp, thay vì nhả một lần hồi quy. Bạn chỉ ra, với hai demonstration Capstone vòng một cái ghế, rằng action trung bình lao vào ghế. Bạn đọc phác thảo $$x_{t-1} = f(x_t, \text{observation})$$ như hình một bộ khử nhiễu đã học, không phải phương trình cập nhật của bài báo. Bạn đối chiếu hình đó với ACT trong hai đoạn: một lượt thuận của CVAE theo chunk, đối lại nhiều bước làm sạch một quỹ đạo.

## Kiến thức cần trước

Bài 12-01 và 12-02 đã xong. Bạn nói được khóa dataset là gì, và nói được chunk ACT hở vòng trong $$k/f$$ giây. Cái ghế trong bài này là đồ đạc, không phải robot mới. Không GPU, không môi trường conda, không checkpoint. Trang dự án là trang công khai.

## Vì sao bài này nằm trên lộ trình

Capstone đã gặp một planner chọn một đường và một controller bám đường đó. Diffusion Policy, Chi và cộng sự, là một đề xuất khác cho chỗ đường đến từ đâu khi đường được người demo vẽ mà những người đó không đồng ý với nhau. Trong hành lang, hai người lái vòng ghế hai phía. Tracker bị bảo bám trung bình của hai đường đó sẽ nhắm vào ghế. Jazzy sẵn sàng xuất bản trung bình đó như một `Twist`. Firmware sẵn sàng đổi nó thành PWM. Không chương nào từ 08 đến 11 tính "lệnh này là trung bình của hai ý hay". Bạn phải tự thấy trung bình đó, trong dữ liệu, trước khi hào hứng với một policy sinh mẫu. Bài này là lần thấy đó. Đây cũng là lần thứ hai bạn gặp một quỹ đạo sinh ra thành loạt, nên thói quen cắt ở 0,2 s từ ACT vẫn đúng khi loạt đó được khử nhiễu chứ không phải hồi quy.

## Khái niệm

Policy hồi quy nhìn observation và nhả action, hoặc một chunk action, trong một phát. Luyện đẩy đầu ra về phía các số đã demo. Demonstration chung một cách làm thì việc này chạy. Chúng tách làm hai thì bình phương sai số là một thỏa hiệp. Thỏa hiệp không phải một trong các cách đã demo.

Chi, Feng, Du, Xu, Cousineau, Burchfiel và Song đặt policy thành khử nhiễu có điều kiện. Bạn bắt đầu bằng một cục nhiễu có hình quỹ đạo. Một mạng, nhận observation làm điều kiện, bước một bước nhỏ về phía quỹ đạo có thể đến từ demonstration. Bạn lặp bước đó. Bốn hộp trên hình là các lần lặp: nhiễu, bớt nhiễu, gần thành action, một quỹ đạo. Các bước sớm không có việc gì để gửi tới động cơ. Các bước muộn là một chuỗi thời gian của $$(v, \omega)$$, hoặc của đích khớp, theo đơn vị của robot đã sinh ra log. Observation là đầu vào ở mọi bước, dù hình chỉ vẽ action đang sạch dần. Che camera thì bộ khử nhiễu không có lý do để thích đường trái hơn đường phải.

Phép cập nhật bạn được phép nhớ cho khóa học này là một phác thảo:

$$
x_{t-1} = f(x_t, \text{observation})
$$

Ở đây $$x_t$$ là quỹ đạo nhiễu ở bước $$t$$, và $$t$$ đếm bước khử nhiễu, không đếm nhịp điều khiển. Chữ $$f$$ thay cho một bộ khử nhiễu đã học. Cập nhật thật của bài báo dự đoán nhiễu, trộn với một lịch, và thêm ngẫu nhiên để hai lần chạy có thể chọn hai mode. Bạn lập trình chữ $$f$$ thành "trừ một hằng số" thì bạn chưa lập trình Diffusion Policy. Bạn đã lập trình bức tranh. Đó là độ sâu đúng cho tối nay.

Vì sao vòng lặp đáng cái giá độ trễ: vật được làm sạch là cả một quỹ đạo ngắn, và phân phối luyện có thể đặt xác suất lên cả hai đường vòng ghế. Một mẫu là một trong hai đường. Mẫu không phải trung bình của hai đường. Bạn thực hiện một mẫu. Lấy trung bình hai mẫu, một trái một phải, là dựng lại cú đâm mà bạn đang tránh. "Sinh" ở đây nghĩa là "rút một quỹ đạo mạch lạc", không phải "trộn mọi demonstration thành một lệnh dịu".

Thói quen chân trời lùi thì quen từ chunk ACT. Khử nhiễu một quỹ đạo dài thì đắt, và đầu xa của nó là phần dễ sai nhất khi thế giới dịch. Các cài đặt vì thế chỉ thực hiện một đoạn đầu, rồi khử nhiễu lại. Đoạn đầu hở vòng suốt thời gian nó kéo dài. Mười bước khử nhiễu tốn 100 ms rồi bạn thực hiện tám action ở 50 Hz, thì đoạn đầu dài $$8/50 = 0.16$$ s. Cùng cấp với cửa sổ ACT $$k = 10$$. Người bước vào trước đoạn đầu là cùng một việc khẩn. Watchdog vẫn chỉ nhận ra sự im lặng. Bộ khử nhiễu cứ phát "tiến" thì không im.

Hai đoạn đối chiếu, vì tên hay bị tráo trong sổ tay.

ACT, Zhao và cộng sự, hỏi transformer một lần để lấy chunk $$k$$ action. Biến ẩn CVAE là cách mô hình đó tránh dự đoán trung bình của vài kiểu demonstration: biến ẩn chọn một kiểu, chunk là hồi quy khi đã có kiểu và observation. Độ trễ là một lần đánh giá mạng mỗi câu hỏi, cộng thời gian hở vòng của đoạn đầu bạn thực hiện. Temporal ensemble trung bình các chunk chồng để dịu rung, và chính trung bình đó có thể đưa lại một thỏa hiệp nhỏ giữa "dừng" mới và "tiến" cũ.

Diffusion Policy, Chi và cộng sự, không nhả chunk bằng một lần hồi quy. Nó bắt đầu từ nhiễu và áp bộ khử nhiễu đã học nhiều lần cho đến khi quỹ đạo trông như thứ demonstration chịu, với ảnh đã cho. Đa mode nằm ở chỗ các lần rút nhiễu khác nhau, hoặc các lựa chọn giữa chừng khác nhau, có thể rơi vào mode khác nhau, trái hoặc phải, thay vì vào một mã ẩn bạn đặt bằng 0. Bạn trả giá bằng nhiều lần gọi mạng mỗi lần lập kế hoạch lại. Cả hai phương pháp đều biểu diễn được hơn một cách làm. Cả hai vẫn có thể ra lệnh cho Capstone lao vào ghế nếu bạn thực hiện nhầm mẫu, hoặc lấy trung bình các mẫu, hoặc tắt timeout vì video demo trông mượt. Chọn giữa chúng tuần này là một lựa chọn đọc. Không phải một cuộc đua train.

## Hình

![Từ nhiễu đến một quỹ đạo]({{ site.imgurl }}/generated/ch12_diffusion.png)

Từ trái sang phải: hộp đỏ là nhiễu, hộp vàng là bớt nhiễu, hộp nhạt gần thành action, hộp xanh là quỹ đạo. Mũi tên là bước khử nhiễu, không phải thời gian dọc đường robot. Dòng chú dưới hộp nói phép tính của bài bằng lời: trung bình của "trái hoặc phải" là thẳng vào vật cản. Chân hình ghi Chi và cộng sự, Diffusion Policy, 2023, và bảo đọc chứ đừng train làm lab tối nay. Hãy tin chân hình.

## Ví dụ đọc có số

Hai demonstration, một điểm quyết định, đơn vị Capstone. Ghế cách camera 0,40 m, nằm giữa. Cả hai người lái giữ vận tốc tiến vừa phải và chỉ bất đồng về yaw.

| Demo | $$v$$ (m/s) | $$\omega$$ (rad/s) | Ý |
| --- | --- | --- | --- |
| L | 0.15 | $$+0.50$$ | vòng bên trái |
| R | 0.15 | $$-0.50$$ | vòng bên phải |
| Trung bình | 0.15 | $$0.00$$ | nhắm vào ghế |

Trung bình không phải một pha trộn thận trọng. Yaw triệt tiêu. Vận tốc tiến thì không. Thời gian tới ghế cách 0,40 m, nếu không ai yaw và tốc độ giữ nguyên, là

$$
\frac{0.40}{0.15} \approx 2.7\,\text{s}
$$

Bạn không có 2,7 s báo trước bên trong một đoạn đầu hở vòng 0,16 s. Đoạn đầu mang action trung bình đã chĩa vào vật cản. Bộ khử nhiễu đã thấy cả hai demonstration, với ảnh có cái ghế, nên kéo một lần rút nhiễu về demo L hoặc demo R. Đừng bắt nó xuất cả hai rồi cầu của bạn lấy trung bình. Chưa chắc mình đã rút mode nào thì lệnh an toàn là $$v = 0$$, không phải trung bình.

Đặt phác thảo cạnh các số đó. Ở bước khử nhiễu muộn, $$x_t$$ có thể là một chuỗi ngắn mà action đầu gần $$(0.15, 0.48)$$, một đường trái còn nhiễu. Khi đó $$f$$, với ảnh, kéo nó về $$(0.15, 0.50)$$. Ở bước sớm, $$x_t$$ chưa phải đường vòng cái gì cả, và gửi nó lên `cmd_vel` là lái trên nhiễu thuần. Chỉ số $$t$$ trong phác thảo không phải nhịp 50 Hz. Trộn hai đồng hồ là cách một người thực hiện bước "nhiễu" như thể nó là bước "quỹ đạo".

## Lab

Mở trang dự án [diffusion-policy.cs.columbia.edu](https://diffusion-policy.cs.columbia.edu/) và abstract tại [arXiv:2303.04137](https://arxiv.org/abs/2303.04137). Bạn tìm câu khẳng định policy mô hình một phân phối trên chuỗi action, và một hình nào đó cho thấy quỹ đạo hiện ra hoặc một việc đa mode. Đừng đi theo link "train" hoặc "download checkpoint" quá mức đọc để biết nó có tồn tại.

Rồi viết một đoạn trong `lab-notes.md` về đa mode, dùng Capstone. Cảnh là hai demonstration vòng một cái ghế hai phía khác nhau. Đoạn phải có action trung bình, và phải nói trung bình đâm vào ghế. Dùng số của ví dụ, hoặc đổi số và tính lại thời gian chạm sao cho số mới vẫn đâm. Kết đoạn bằng một câu tường minh: bạn không train mô hình và không nạp trọng số.

**Kỳ vọng.** Một đoạn mà bạn học kiểm được mà không cần xem video. Có hai phía, một yaw bị triệt, một vận tốc tiến khác 0, cái ghế, và một lời từ chối train. Đoạn chỉ nói "diffusion giỏi đa mode hơn" là chưa xong, vì chưa hề nhắc trung bình.

**Các kiểu hỏng**

| Lỗi | Vì sao đoạn hỏng |
| --- | --- |
| Bạn gộp hai demonstration thành một episode "trung tính" và gọi dataset sạch hơn | Bạn đã xóa cả hai đường vòng thành công và chèn vào cú va |
| Bạn coi GPU không có, hoặc lỗi hết bộ nhớ, là lab trượt | Lab là đoạn văn. Tắt tiến trình train là cách thoát, không phải kết quả |
| Bạn viết diffusion an toàn hơn vì nó lặp | Vòng lặp sinh một mẫu. Mẫu có thể nói tiến. An toàn vẫn là timeout cộng một số 0 tường minh khi đoạn đầu sai |
| Bạn gửi một bước khử nhiễu sớm tới động cơ vì nó đã có hình $$(v, \omega)$$ | Bước sớm là nhiễu mang hình đó. Chỉ quỹ đạo đã xong mới là ứng viên lệnh, và chỉ theo đơn vị của dataset |

## Bài tập

1. Demo L là $$(v, \omega) = (0.20, +0.80)$$ và demo R là $$(0.20, -0.40)$$, đơn vị m/s và rad/s. Action trung bình là gì, và nó yaw về phía nào? Gợi ý: trung bình $$v = 0.20$$, trung bình $$\omega = +0.20$$. Yaw không triệt tiêu. Trung bình vẫn không cần phải là một trong hai demonstration. Nói bạn có thực hiện nó khi ghế nằm giữa hay không.
2. Trong phác thảo, chỉ số dưới $$t$$ đếm cái gì? Gợi ý: các bước khử nhiễu. Nó không đếm chu kỳ điều khiển 20 ms. Viết một câu giữ hai đồng hồ tách nhau.
3. Bạn thực hiện một đoạn đầu 8 action ở 50 Hz sau khi quỹ đạo đã sạch. Đoạn đầu dài bao lâu, và watchdog 300 ms có hết hạn trong lúc đó nếu bạn vẫn xuất bản? Gợi ý: $$8/50 = 0.16$$ s. Watchdog không hết hạn, vì việc xuất bản còn tiếp. Nêu lệnh bạn xuất bản nếu đoạn đầu chĩa vào ghế.
4. ACT cam kết bằng một biến ẩn và một lượt thuận. Diffusion Policy cam kết bằng cách rút một quỹ đạo ra khỏi nhiễu. Nêu một cái giá của lựa chọn thứ hai mà lựa chọn thứ nhất không trả ở mỗi lần lập kế hoạch lại. Gợi ý: nhiều lần đánh giá bộ khử nhiễu mỗi lần lập lại, thay vì một lượt transformer. Cái giá là độ trễ, không phải giấy phép bỏ lệnh dừng.
5. Đoạn của bạn nói trung bình đâm ghế. Đổi ghế còn cách 0,15 m và giữ $$v = 0.15$$ với $$\omega = 0$$. Bao lâu thì chạm, và khoảng đó có dài hơn đoạn đầu 0,16 s không? Gợi ý: $$0.15/0.15 = 1.0$$ s hành trình nếu tốc độ giữ. Một giây dài hơn đoạn đầu, nghĩa là riêng đoạn đầu chưa đâm xong, và cũng nghĩa là đoạn đầu đã cam kết bạn vào hướng xấu. Cách sửa là một số 0, không phải một bài ngắn hơn.

## Đọc thêm

- [Trang dự án Diffusion Policy](https://diffusion-policy.cs.columbia.edu/). Đọc phần ý tưởng và các hình. Lệnh train cứ để đó: bạn không chạy.
- [Chi và cộng sự, arXiv:2303.04137](https://arxiv.org/abs/2303.04137). Abstract đủ để xác nhận tác giả và câu khẳng định. Lịch nhiễu trong bài báo là máy thật của bộ khử nhiễu đã học, sâu hơn phác thảo $$f$$.
