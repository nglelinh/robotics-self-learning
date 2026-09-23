---
layout: post
title: "Camera cho robot: USB, CSI, băng thông"
chapter: "04"
order: 6
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter04
lesson_type: required
draft: false
---

Thời lượng: **60–75 phút**. Bài bắt buộc là một bản dự toán băng thông. Camera trên bàn là tùy chọn, và Chương 07 không đợi bạn mua.

## Mục tiêu học

Bạn tính băng thông không nén và MJPEG cho một khổ rộng, cao và tốc độ khung cho trước, rồi đem số đó so với những gì USB 2.0 thực sự đưa được khi phải chia sẻ. Bạn phân biệt webcam UVC (USB, laptop là host), camera CSI (cáp ruy-băng không đi qua bộ điều khiển USB), và ESP32-CAM (JPEG trên một board là bộ não Capstone kém). Bạn viết một câu hoãn camera đến phần nhận thức, và câu đó chứa số 147 Mbit/s để checklist thấy bạn đã làm phép nhân.

## Kiến thức cần có

Phiếu nhận diện Bài 04-02 đã có một dòng “phích USB, cáp dẹt, hay hai ống nhôm”. Chương 02 là ESP32 và Pico, nên bạn biết board nào được phép làm máy tính của robot. Bạn nhân được. Chưa cần OpenCV, GPU, hay tuyến ảnh ROS. Những chữ đó còn mới thì cứ để mới đến Chương 11.

## Vì sao bài này quan trọng với Capstone A và ROS

Capstone A không cần camera. Firmware Chương 07 teleop hai bánh từ lệnh serial và dừng khi timeout hoặc khi có số đo khoảng cách. Một luồng video USB trên cùng laptop đó là dự án khác: nó tranh băng thông USB, tranh CPU, và tranh cả tuần của bạn. Ai chặn lab motor chỉ vì đơn camera thì cả hai việc đều dở dang.

Khi phần nhận thức bắt đầu, đường ROS 2 thường gặp là `usb_cam` hoặc một node V4L2 khác, xuất `sensor_msgs/Image` cho điểm ảnh thô và `sensor_msgs/CompressedImage` cho JPEG. Trường encoding (`yuyv`, `rgb8`, `jpeg`) chính là lựa chọn “byte trên mỗi điểm ảnh” trong công thức dưới đây. Camera CSI trên Pi không băng qua liên kết USB đó, nên nó không đổi tổng 147 Mbit/s, nhưng nó cũng không cắm được vào ESP32. Viết câu hoãn ngay bây giờ, có số ở trong, và tiếp tục mua cảm biến khoảng cách cùng cặp động cơ encoder.

![Dòng nào là camera: phích USB hoặc cáp dẹt, không phải hai ống nhôm]({{ site.imgurl }}/generated/sensor_package_id.png)

Hình là phiếu nhận diện của Bài 04-02. Dòng camera là đầu nối rộng: phích USB, hoặc cáp dẹt cắm vào một module lớn. Hai ống nhôm là cảm biến siêu âm của bài trước. Cửa sổ tí hon là ToF hoặc IMU, không phải camera cảnh. Phiếu của bạn còn gọi mọi hình chữ nhật đen là camera thì sửa dòng đó trước khi đọc một số băng thông như thể nó là khoảng cách.

## Byte trên giây, rồi megabit

Băng thông ảnh không nén là

$$
B \approx w \times h \times \mathrm{fps} \times (\text{byte trên mỗi điểm ảnh}).
$$

YUYV là định dạng 4:2:2: hai byte mỗi điểm ảnh, không JPEG. Luồng 640×480 ở 30 khung mỗi giây là

$$
B = 640 \times 480 \times 2 \times 30 = 18{,}432{,}000~\mathrm{byte/s}.
$$

Nhân 8,

$$
18{,}432{,}000 \times 8 = 147{,}456{,}000~\mathrm{bit/s} \approx 147~\mathrm{Mbit/s}.
$$

Trần lý thuyết của USB 2.0 là 480 Mbit/s. Chia với adapter serial, hub và phần mào đầu giao thức, thông lượng video thực tế thường gần 280–300 Mbit/s hơn. Một luồng thô 640×480 đã chiếm khoảng một nửa ngân sách thực tế đó. Luồng thô thứ hai không còn chỗ. Video trên USB là isochronous: gói đến muộn bị bỏ, bạn thấy khung rách chứ không thấy một lần gửi lại sạch sẽ.

MJPEG khoảng 10:1 trên cùng khung hình đó là

$$
147 / 10 \approx 15~\mathrm{Mbit/s}.
$$

Số này ngồi thoải mái cạnh một cổng serial. Bạn trả giá bằng CPU giải mã trên máy chủ. RGB ba byte mỗi điểm ảnh nặng hơn YUYV: $$640 \times 480 \times 3 \times 30 = 27{,}648{,}000$$ byte/s, khoảng 221 Mbit/s, tức một luồng đã cãi nhau với phần còn lại của bus.

## Ba cách robot “có camera”

**USB UVC.** Webcam nói USB Video Class. Trên laptop, `lsusb` liệt kê nó, và sau này một node V4L2 mở `/dev/video0`. Host là máy tính, không phải một chân GPIO. Đây là camera hợp lý cho Chương 11 nếu não robot là Pi hoặc PC và ESP32 chỉ là board motor. Đó cũng chính là luồng 147 Mbit/s vừa tính, trừ khi bạn yêu cầu camera xuất MJPEG.

**CSI.** Camera Raspberry Pi đi cáp ruy-băng vào cổng CSI của Pi. Các điểm ảnh không qua bộ chủ USB, nên không cộng vào tài khoản 480 Mbit/s. Chúng cũng không tồn tại trên ESP32 DevKit hay Pico. Mua camera Pi “cho robot” trong khi máy tính duy nhất của robot là ESP32 là mua một camera không có chỗ cắm.

**ESP32-CAM, OV2640.** Module xuất JPEG, nên bài toán băng thông trên dây trông như đã xong, rồi chính cái board trở thành vấn đề. Camera chiếm một đám chân, ổn áp onboard sụt áp khi radio và cảm biến cùng kéo dòng, và khung xe vẫn còn nợ một driver motor. Làm thí nghiệm phụ thì được. Làm não Capstone A thì vụng. Đừng thay devkit ESP32 đang nháy LED bằng module này chỉ để “sẵn sàng cho thị giác”.

ESP32 trong ảnh của môn học là devkit có USB cho serial và GPIO trống cho TRIG, ECHO, rồi PWM. Nó không phải host CSI. Cứ đối xử với nó như vậy cho đến khi một chương sau đưa cho bạn một máy tính khác.

## Lab: bản dự toán là bài nộp

### An toàn

Không động cơ. Cắm webcam thì cắm cổng USB của laptop, không cắm GPIO. Đừng nuôi ESP32-CAM từ chân 3,3 V của devkit; board camera muốn nguồn 5 V riêng và vẫn dễ sụt áp. Đừng đi tìm tia laser trong webcam. Lab này không đụng VL53L0X.

### BOM

| Món | Vai trò |
|------|---------|
| Giấy hoặc `lab-notes.md` | Tờ băng thông bắt buộc |
| Webcam USB, nếu đã có | `lsusb` tùy chọn |
| Laptop | Host cho camera tùy chọn đó |
| ESP32-CAM | Không bắt buộc, và không phải não Capstone |

### Các bước

1. Tính $$640 \times 480 \times 2 \times 30$$ theo byte mỗi giây và theo Mbit/s. Bạn phải ra 18.432.000 byte/s và khoảng 147 Mbit/s. Viết phép nhân vào sổ.
2. Chia 10 cho một luồng MJPEG ước lượng và ghi khoảng 15 Mbit/s. Nói rõ ngân sách thực tế USB 2.0 khoảng 280–300 Mbit/s, dùng chung.
3. Quyết định, trong một câu, rằng camera đợi đến Chương 11. Câu phải chứa 147 Mbit/s. Một câu đạt: “Hoãn camera đến Chương 11; một luồng YUYV 640×480 đã khoảng 147 Mbit/s.”
4. Tùy chọn, chỉ khi đã cắm camera: chạy `lsusb` và chép dòng vừa xuất hiện. Nhìn được đầu nối thì ghi USB-A, micro-USB, hoặc cáp CSI. Không có camera thì dừng ở bước 3. Đó là một lab đủ.
5. Trên phiếu Bài 04-02, chỉ vào dòng camera và ghi loại đầu nối bạn sẽ mua sau, hoặc “chưa mua”.

### Kết quả mong đợi

Ba số (18.432.000 byte/s, 147 Mbit/s, MJPEG khoảng 15 Mbit/s) và câu hoãn nằm trong `lab-notes.md`. Thiếu camera không phải thiếu lab. Mua ESP32-CAM không phải điểm cộng cho Chương 07.

### Lỗi thường gặp

| Bạn thấy | Thường là |
|----------|-----------|
| Ghi băng thông 18 triệu bit | Quên nhân 8 từ byte sang bit |
| “USB 2.0 là 480, nên hai luồng thô vừa” | Bạn dùng trần lý thuyết, không phải khoảng 300 Mbit/s dùng chung |
| Khung rách khi adapter serial cùng hub | Ngân sách thực tế đã chật |
| Camera Pi với ESP32, không có gì ở `/dev/video` | CSI không cắm vào devkit đó |
| Chương 07 bị chặn vì đơn camera | Quyết định của bài này bị bỏ qua |

## Mua ở Việt Nam / Where to buy in Vietnam

Đừng mua camera để xong Chương 04 hay để bắt đầu Chương 07. Nếu bạn đã biết mình muốn một cái cho Chương 11, webcam UVC thường là món mua nhàm và đúng. Giá thay đổi.

| Món | Từ khóa | Khoảng giá (VND) | Thay thế |
|------|---------|------------------|----------|
| Webcam USB | `camera usb robot` | 80.000–200.000 | Bất kỳ camera UVC nào laptop đã nhận. Lời quảng cáo trên 720p không đổi kế hoạch Capstone. |
| ESP32-CAM | `ESP32-CAM` | 70.000–140.000 | Chỉ là board phụ. Không thay devkit đang kéo motor. |

- [Hshop: camera USB](https://hshop.vn/search?q=camera%20usb)
- [Shopee: camera usb robot](https://shopee.vn/search?keyword=camera%20usb%20robot)
- [Lazada: ESP32-CAM](https://www.lazada.vn/catalog/?q=ESP32-CAM)
- [Thế Giới IC: ESP32-CAM](https://www.thegioiic.com/search?q=ESP32-CAM)

## Bài tập

1. Tính tốc độ byte và tốc độ bit của YUYV 640×480 ở 30 fps.
2. Cùng các khung đó dưới MJPEG khoảng 10:1. Khoảng 15 Mbit/s có nằm vừa trên bus USB 2.0 thực tế 300 Mbit/s đang kèm một đường serial 12 Mbit/s không? Một luồng thô 147 Mbit/s thứ hai có nằm vừa cạnh luồng thứ nhất không?
3. Chế độ nhỏ hơn: 320×240, RGB (3 byte/điểm ảnh), 15 fps. $$B$$ bằng bao nhiêu Mbit/s, và so với luồng 147 Mbit/s thì thế nào?
4. Vì sao camera CSI của Pi không làm nhẹ ngân sách USB, và vì sao ESP32-CAM vẫn là não Chương 07 kém dù JPEG của nó nhỏ?
5. Viết một câu quyết định camera mà checklist Chương 04 sẽ tìm. Có số 147 Mbit/s trong câu.

### Gợi ý đáp án

1. $$18{,}432{,}000$$ byte/s, tức $$147{,}5~\mathrm{Mbit/s}$$ (khoảng 147). 2. $$15 + 12$$ nằm rất thoải. Hai luồng thô khoảng 295 Mbit/s trước cả đường serial, không vừa ngân sách thực tế 280–300 Mbit/s. 3. $$320 \times 240 \times 3 \times 15 = 3{,}456{,}000$$ byte/s $$\approx 27{,}6~\mathrm{Mbit/s}$$, khoảng một phần năm luồng YUYV 640×480. 4. CSI không đi vào host USB nên tổng USB không đổi, và cáp ruy-băng Pi không có ổ cắm trên ESP32. JPEG của ESP32-CAM thì nhỏ, nhưng board vẫn tiêu chân và dòng ổn áp mà não motor cần. 5. Bất kỳ câu nào hoãn camera đến Chương 11 và nói YUYV 640×480 ở 30 fps khoảng 147 Mbit/s.

## Đọc thêm

- [Định dạng điểm ảnh YUYV của V4L2](https://www.kernel.org/doc/html/latest/userspace-api/media/v4l/pixfmt-yuyv.html) — hai byte mỗi điểm ảnh, số 2 trong công thức.
- [`usb_cam` trên ROS 2](https://index.ros.org/p/usb_cam/) — node thường đứng sau webcam UVC, xuất ảnh chứ không xuất khoảng cách.
- [`sensor_msgs/Image`](https://docs.ros.org/en/humble/p/sensor_msgs/msg/Image.html) và [`sensor_msgs/CompressedImage`](https://docs.ros.org/en/humble/p/sensor_msgs/msg/CompressedImage.html) — thô và JPEG, tức lựa chọn 147 hay 15.
- [Tài liệu camera Raspberry Pi](https://www.raspberrypi.com/documentation/accessories/camera.html) — cáp CSI, và vì sao đó không phải ngoại vi của ESP32.
