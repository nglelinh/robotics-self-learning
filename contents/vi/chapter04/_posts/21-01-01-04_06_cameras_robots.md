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

Thời lượng: **60–75 phút**. Yêu cầu bắt buộc của bài là bản dự toán băng thông; việc có sẵn camera trên bàn chỉ là tùy chọn và Chương 07 không yêu cầu bạn mua camera.

## Mục tiêu học

Sau bài này, bạn tính được băng thông video không nén và MJPEG theo độ phân giải và tốc độ khung hình, rồi đối chiếu với thông lượng thực tế của bus USB 2.0 khi chia sẻ cùng các thiết bị khác. Bạn phân biệt được ba phương án: webcam chuẩn UVC (USB, máy tính làm host), camera CSI (cáp dẹt không đi qua bộ điều khiển USB) và ESP32-CAM (xuất JPEG nhưng không phù hợp làm bộ điều khiển chính của Capstone A). Cuối bài, bạn viết câu quyết định hoãn camera đến phần nhận thức kèm con số 147 Mbit/s cho checklist chương 04.

## Kiến thức cần có

Bạn đã lập phiếu nhận diện linh kiện ở Bài 04-02 và nắm rõ giới hạn phần cứng của ESP32/Pico từ Chương 02. Bài này chỉ cần các phép tính nhân chia cơ bản; chưa cần OpenCV, GPU hay xử lý ảnh trên ROS (các nội dung đó dành cho Chương 11).

## Vì sao bài này quan trọng với Capstone A và ROS

Capstone A không cần camera: firmware Chương 07 điều khiển hai bánh qua lệnh serial và dừng an toàn bằng timeout hoặc cảm biến khoảng cách. Đưa thêm luồng video USB vào cùng thời điểm chỉ làm tranh chấp băng thông USB, tài nguyên CPU và thời gian triển khai, dễ làm chậm tiến độ phần động cơ.

Đến phần nhận thức (Chương 11), hệ thống ROS 2 thường dùng `usb_cam` hoặc node V4L2 để xuất ảnh thô qua `sensor_msgs/Image` hoặc ảnh nén JPEG qua `sensor_msgs/CompressedImage`. Trường mã hóa (`yuyv`, `rgb8`, `jpeg`) quyết định trực tiếp số byte trên mỗi điểm ảnh trong công thức tính băng thông bên dưới. Camera CSI trên Raspberry Pi không đi qua bộ điều khiển USB nhưng cũng không có cổng cắm trên ESP32. Do đó, việc tính trước băng thông và chốt kế hoạch hoãn camera giúp bạn tập trung ngân sách vào cảm biến khoảng cách và động cơ encoder.

![Dòng nào là camera: phích USB hoặc cáp dẹt, không phải hai ống nhôm]({{ site.imgurl }}/generated/sensor_package_id.png)

Đối chiếu lại phiếu nhận diện ở Bài 04-02: nhóm camera có đầu nối USB hoặc cáp dẹt bản rộng, khác hẳn hai ống nhôm của cảm biến siêu âm hay cửa sổ quang tí hon của cảm biến ToF.

## Tính băng thông: từ byte/giây sang Mbit/s

Băng thông của một luồng video không nén được ước lượng bởi:

$$
B \approx w \times h \times \mathrm{fps} \times (\text{byte trên mỗi điểm ảnh}).
$$

Định dạng YUYV (4:2:2) dùng trung bình 2 byte cho mỗi điểm ảnh. Với độ phân giải 640×480 ở tốc độ 30 khung hình/giây:

$$
B = 640 \times 480 \times 2 \times 30 = 18{,}432{,}000~\mathrm{byte/s}.
$$

Đổi sang bit/giây bằng cách nhân 8:

$$
18{,}432{,}000 \times 8 = 147{,}456{,}000~\mathrm{bit/s} \approx 147~\mathrm{Mbit/s}.
$$

Tốc độ lý thuyết của USB 2.0 là 480 Mbit/s, nhưng khi trừ phần mào đầu giao thức và chia sẻ bus với hub hay bộ chuyển đổi USB-serial, thông lượng thực tế cho video chỉ vào khoảng 280–300 Mbit/s. Như vậy, chỉ một luồng YUYV 640×480 đã chiếm gần một nửa ngân sách thực tế, không còn đủ chỗ cho luồng thô thứ hai. Hơn nữa, video trên USB dùng chế độ truyền đẳng thời (isochronous): gói đến trễ sẽ bị bỏ qua thay vì truyền lại, gây rách hoặc mất khung hình.

Nếu dùng nén MJPEG với tỉ lệ nén khoảng 10:1 trên cùng độ phân giải và tốc độ khung:

$$
147 / 10 \approx 15~\mathrm{Mbit/s}.
$$

Mức 15 Mbit/s chạy thoải mái cùng cổng serial trên USB 2.0, đánh đổi bằng tải CPU giải mã trên máy tính chủ. Ngược lại, định dạng RGB (3 byte/điểm ảnh) còn nặng hơn YUYV: $$640 \times 480 \times 3 \times 30 = 27{,}648{,}000~\mathrm{byte/s}$$, tương đương khoảng 221 Mbit/s, rất dễ tranh chấp băng thông với các thiết bị khác trên cùng bus.

## Ba phương án lắp camera cho robot

- **Webcam USB (UVC):** giao tiếp theo chuẩn USB Video Class; trên Linux, lệnh `lsusb` sẽ liệt kê thiết bị và node V4L2 mở cổng `/dev/video0`. Máy tính chủ (laptop hoặc Raspberry Pi) đóng vai trò host, không nối vào GPIO. Đây là phương án hợp lý cho Chương 11 khi ESP32 chỉ đảm nhiệm điều khiển động cơ (và nên cấu hình xuất MJPEG để tiết kiệm băng thông).
- **Camera CSI:** nối trực tiếp bằng cáp ruy-băng vào cổng CSI của Raspberry Pi. Dữ liệu ảnh không đi qua bộ điều khiển USB nên không chiếm dụng băng thông 480 Mbit/s của USB 2.0. Tuy nhiên, ESP32 DevKit và Pico không có cổng CSI nên không thể sử dụng loại này.
- **ESP32-CAM (OV2640):** nén sẵn JPEG giúp giảm tải đường truyền, nhưng bản thân bo mạch lại bị chiếm nhiều chân GPIO cho camera, mạch ổn áp dễ sụt nguồn khi chạy đồng thời Wi-Fi và cảm biến, đồng thời thiếu chân thuận tiện cho mạch cầu H động cơ. Có thể dùng làm mạch thí nghiệm phụ, nhưng không dùng thay ESP32 DevKit làm bộ điều khiển chính của Capstone A.

## Lab: lập bản dự toán băng thông

### An toàn

Không dùng động cơ. Nếu có webcam USB để thử lệnh `lsusb`, chỉ cắm vào cổng USB của laptop, không nối vào GPIO. Không cấp nguồn cho ESP32-CAM từ chân `3V3` của ESP32 DevKit (ESP32-CAM cần nguồn 5 V riêng ổn định).

### BOM

| Món | Vai trò |
|------|---------|
| Giấy hoặc `lab-notes.md` | Ghi bản tính băng thông bắt buộc |
| Webcam USB (nếu có sẵn) | Thực hành kiểm tra tùy chọn bằng `lsusb` |
| Laptop | Máy chủ cho webcam tùy chọn |
| ESP32-CAM | Không bắt buộc và không dùng làm bộ điều khiển Capstone A |

### Các bước

1. Thực hiện phép tính $$640 \times 480 \times 2 \times 30$$ để ra 18.432.000 byte/s và khoảng 147 Mbit/s, ghi đầy đủ vào sổ tay.
2. Chia cho 10 để ước lượng luồng MJPEG (khoảng 15 Mbit/s) và ghi chú ngân sách thực tế của USB 2.0 khoảng 280–300 Mbit/s khi dùng chung.
3. Viết một câu chốt quyết định hoãn camera đến Chương 11, bắt buộc có chứa con số 147 Mbit/s (ví dụ: "Hoãn camera đến Chương 11; một luồng YUYV 640×480 ở 30 fps đã chiếm khoảng 147 Mbit/s.").
4. *(Tùy chọn, nếu có sẵn camera)* Cắm vào laptop, chạy `lsusb`, chép lại dòng thiết bị vừa xuất hiện và ghi loại đầu nối (USB-A, micro-USB hay CSI). Nếu chưa có camera, dừng ở bước 3 là đã hoàn thành bài lab.
5. Cập nhật dòng camera trên phiếu nhận diện Bài 04-02 với loại đầu nối dự kiến mua sau hoặc ghi "chưa mua".

### Kết quả mong đợi

Sổ tay `lab-notes.md` có đủ ba con số (18.432.000 byte/s, ~147 Mbit/s, MJPEG ~15 Mbit/s) kèm câu quyết định hoãn camera. Chưa có camera vật lý vẫn hoàn thành đầy đủ bài thực hành này.

### Lỗi thường gặp

| Hiện tượng | Nguyên nhân thường gặp |
|------------|------------------------|
| Ghi băng thông là 18 triệu bit/s | Quên nhân 8 để đổi từ byte sang bit |
| Cho rằng USB 2.0 (480 Mbit/s) tải được hai luồng thô | Lấy trần lý thuyết thay vì thông lượng thực tế ~280–300 Mbit/s |
| Khung hình bị rách khi cắm chung hub với USB-serial | Bus USB 2.0 đã quá tải thông lượng thực tế |
| Cắm camera CSI của Pi với ESP32 nhưng không thấy `/dev/video` | ESP32 DevKit không có giao diện CSI |
| Trì hoãn Chương 07 để chờ đơn hàng camera | Bỏ qua quyết định hoãn camera của bài này |

## Mua ở Việt Nam

Không cần mua camera để hoàn thành Chương 04 hay bắt đầu Chương 07. Nếu dự trù cho Chương 11, một webcam chuẩn UVC phổ thông là lựa chọn ít rủi ro nhất.

| Món | Từ khóa | Khoảng giá (VND) | Thay thế |
|------|---------|------------------|----------|
| Webcam USB | `camera usb robot` | 80.000–200.000 | Bất kỳ webcam UVC nào laptop nhận diện trực tiếp. |
| ESP32-CAM | `ESP32-CAM` | 70.000–140.000 | Chỉ dùng làm mạch phụ, không thay thế ESP32 DevKit điều khiển động cơ. |

- [Hshop: camera USB](https://hshop.vn/search?q=camera%20usb)
- [Shopee: camera usb robot](https://shopee.vn/search?keyword=camera%20usb%20robot)
- [Lazada: ESP32-CAM](https://www.lazada.vn/catalog/?q=ESP32-CAM)
- [Thế Giới IC: ESP32-CAM](https://www.thegioiic.com/search?q=ESP32-CAM)

## Video tham khảo

- **Xem trước:** [How to choose a camera for your Raspberry Pi](https://www.youtube.com/watch?v=wQB1ffECTS0) — Yahboom Technology, tiếng Anh. So sánh cách chọn camera theo cổng kết nối và băng thông, đối chiếu USB với CSI.
- [Why choose a MIPI CSI-2 interface rather than USB?](https://www.youtube.com/watch?v=lfI-mcwCYF4) — AlliedVisionTV, tiếng Anh. Giải thích sự khác biệt về đường truyền dữ liệu giữa CSI và USB.

## Bài tập

1. Tính tốc độ theo byte/s và Mbit/s của luồng ảnh YUYV 640×480 ở 30 fps.
2. Nén luồng trên bằng MJPEG tỉ lệ 10:1 (khoảng 15 Mbit/s). Mức này có chạy thoải mái trên bus USB 2.0 thực tế 300 Mbit/s cùng một đường serial 12 Mbit/s không? Ngược lại, có thể chạy đồng thời hai luồng thô 147 Mbit/s trên cùng bus đó không?
3. Với chế độ nhỏ hơn là 320×240, định dạng RGB (3 byte/điểm ảnh) ở 15 fps, tính băng thông $$B$$ theo Mbit/s và so sánh với luồng 147 Mbit/s.
4. Vì sao camera CSI của Raspberry Pi không tiêu tốn băng thông USB (nhưng cũng không dùng được trên ESP32), và vì sao ESP32-CAM vẫn không phù hợp làm bộ điều khiển Chương 07 dù luồng JPEG khá nhỏ?
5. Viết một câu quyết định hoãn camera đạt yêu cầu checklist Chương 04 (có chứa con số 147 Mbit/s).

### Gợi ý đáp án

1. $$18{,}432{,}000~\mathrm{byte/s}$$, tương đương $$147{,}5~\mathrm{Mbit/s}$$ (xấp xỉ 147 Mbit/s).
2. $$15 + 12 = 27~\mathrm{Mbit/s}$$, nằm rất thoải mái trong ngưỡng 300 Mbit/s. Hai luồng thô chiếm tới khoảng 295 Mbit/s (chưa tính đường serial), vượt quá ngân sách thực tế 280–300 Mbit/s.
3. $$320 \times 240 \times 3 \times 15 = 3{,}456{,}000~\mathrm{byte/s} \approx 27{,}6~\mathrm{Mbit/s}$$, bằng khoảng một phần năm luồng YUYV 640×480.
4. Camera CSI đi trực tiếp vào bộ xử lý hình ảnh qua cáp ruy-băng chứ không qua bộ điều khiển USB, nhưng ESP32 không có cổng CSI. Với ESP32-CAM, dù dữ liệu JPEG nhỏ, bo mạch lại bị chiếm nhiều chân GPIO và dễ sụt nguồn ổn áp khi gánh thêm động cơ.
5. Bất kỳ câu nào nêu rõ hoãn camera đến Chương 11 kèm số liệu YUYV 640×480 ở 30 fps chiếm khoảng 147 Mbit/s.

## Đọc thêm

- [Định dạng điểm ảnh YUYV của V4L2](https://www.kernel.org/doc/html/latest/userspace-api/media/v4l/pixfmt-yuyv.html) — tài liệu giải thích quy cách 2 byte mỗi điểm ảnh trong công thức.
- [`usb_cam` trên ROS 2](https://index.ros.org/p/usb_cam/) — gói phần mềm phổ biến đọc webcam UVC trong ROS 2.
- [`sensor_msgs/Image`](https://docs.ros.org/en/jazzy/p/sensor_msgs/msg/Image.html) và [`sensor_msgs/CompressedImage`](https://docs.ros.org/en/jazzy/p/sensor_msgs/msg/CompressedImage.html) — hai định dạng bản tin tương ứng ảnh thô (147 Mbit/s) và ảnh nén JPEG (~15 Mbit/s).
- [Tài liệu camera Raspberry Pi](https://www.raspberrypi.com/documentation/accessories/camera.html) — chi tiết giao diện CSI và lý do không dùng trên ESP32.
