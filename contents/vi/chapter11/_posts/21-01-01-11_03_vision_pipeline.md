---
layout: post
title: "Pipeline thị giác cơ bản"
chapter: "11"
order: 3
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter11
lesson_type: required
draft: false
---

Thời lượng ước tính: **~75 phút** khi camera USB nhận diện tại `/dev/video0`, hoặc khoảng 45 phút nếu máy chưa có camera và bạn hoàn thành phần thiết kế pipeline trên giấy.

## Mục tiêu học

Sau bài học này, bạn sẽ xây dựng quy trình xử lý thị giác theo đúng thứ tự **ánh sáng → camera → thuật toán** (tránh chỉnh ngưỡng màu khi ánh sáng môi trường làm cháy sáng thẻ màu). Bạn nắm được kiểu dữ liệu `usb_cam` xuất bản, tính được tọa độ trọng tâm (centroid), giới hạn tần số ra quyết định ở mức 5–10 Hz thay vì gửi lệnh theo từng khung hình, phân biệt rõ hệ tọa độ quang học với `camera_link` theo chuẩn REP-103, và biết cách ghi nhận tình huống thiếu `/dev/video0` một cách trung thực.

## Kiến thức cần có

Bạn chạy được script Python cơ bản và hiểu ảnh số là một mảng hai chiều (hoặc ba chiều theo kênh màu). Từ bài tour Nav2, bạn đã nắm cấu trúc `geometry_msgs/msg/Twist` gồm thành phần tịnh tiến và thành phần quay. Bài thực hành này không yêu cầu camera chiều sâu hay RealSense.

## Vì sao bài này nằm trên lộ trình

Trên lộ trình từ khung xe Capstone lên ROS 2 Jazzy, qua Gazebo rồi đến tự hành, xe đã có cầu nối từ `/cmd_vel` sang PWM, còn ROS 2 cho phép camera xuất bản `sensor_msgs/msg/Image` song song với dữ liệu lidar. Thử nghiệm thực tế với một tấm thẻ màu trên bàn giúp bạn thấy ngay sự nhạy cảm của ngưỡng màu trước ánh sáng — điều mà camera mô phỏng khó phản ánh hết. Hành động điều khiển trong bài giữ ở mức cơ bản (quay về phía thẻ hoặc dừng lại) nhưng vẫn dùng đúng message `Twist` như Nav2. Duy trì nhịp quyết định 5–10 Hz thay vì chạy hết tốc độ 30 Hz giúp cầu nối hoạt động êm và dễ phối hợp với bộ điều hướng về sau.

## Khái niệm

**Bước 1: Ánh sáng.** Cùng một tấm thẻ đỏ nhưng đặt dưới đèn trần hay dưới nắng chiều sẽ cho giá trị màu hoàn toàn khác nhau. Nếu mắt thường không thấy sự tách biệt rõ rệt giữa thẻ và nền, OpenCV cũng không thể phân đoạn ổn định; do đó hãy điều chỉnh nguồn sáng hoặc tránh ngược sáng trước khi chỉnh ngưỡng màu (hue).

**Bước 2: Camera.** Sử dụng camera USB chuẩn UVC (thường xuất hiện tại `/dev/video0`), với driver `usb_cam` hoặc `v4l2_camera` xuất bản `sensor_msgs/msg/Image`.

**Bước 3: Thuật toán.** Bài này tập trung vào phân ngưỡng màu kết hợp tính trọng tâm, chưa dùng mạng nơ-ron phát hiện vật thể.

![Ảnh camera thành mặt nạ ngưỡng, rồi thành centroid có thể phát một lệnh yaw chậm]({{ site.imgurl }}/generated/ch11_vision.png)

Trên máy ROS 2 Jazzy đã cài gói nhị phân, cú pháp chạy driver `usb_cam` là:

```bash
sudo apt install ros-jazzy-usb-cam
source /opt/ros/jazzy/setup.bash
ros2 run usb_cam usb_cam_node_exe
```

Lệnh `ros2 launch usb_cam camera.launch.py` sẽ mở kèm cửa sổ xem ảnh. Topic mặc định thường là `/image_raw` (`sensor_msgs/msg/Image`); nếu topic không có dữ liệu, cần kiểm tra đường dẫn thiết bị trước khi đụng tới thuật toán ngưỡng. Bài lab dưới đây gọi trực tiếp OpenCV nên chưa bắt buộc chạy node này.

Phân ngưỡng trong không gian màu HSV ổn định hơn kênh RGB thô nhưng vẫn phụ thuộc điều kiện chiếu sáng; hãy chốt rõ cận dưới, cận trên cùng điều kiện ánh sáng sử dụng. Sau khi tạo mặt nạ nhị phân (vùng thẻ mang giá trị trắng), ta dùng mô-men ảnh để tính trọng tâm (centroid). Với tập $$N$$ điểm ảnh trắng có tọa độ $$(x_i, y_i)$$:

$$
c_x = \frac{\sum_i x_i}{N}, \qquad c_y = \frac{\sum_i y_i}{N},
$$

chính là phép chia `m10 / m00` và `m01 / m00` từ hàm `cv2.moments`. Ví dụ với một mặt nạ gồm ba điểm ảnh tại $$(100, 80)$$, $$(102, 80)$$ và $$(101, 82)$$:

$$
c_x = \frac{100 + 102 + 101}{3} = 101, \qquad c_y = \frac{80 + 80 + 82}{3} \approx 80{,}67.
$$

Với ảnh rộng 320 pixel (tâm ngang tại 160), trọng tâm $$c_x = 101$$ nằm về phía bên trái tâm khung hình. Khi camera hướng thẳng về trước, điều này có nghĩa mục tiêu đang ở bên trái, nên xe vi sai cần quay trái (`angular.z` dương theo REP-103) để đưa trọng tâm tiến về giữa ảnh. Nếu diện tích `m00` quá nhỏ (không phát hiện thẻ), cần dừng hoặc phát `Twist` bằng 0 thay vì để xe đuổi theo nhiễu.

Tần số ra quyết định nên giữ chậm: dù camera thu 30 khung hình/giây, việc gửi 30 lệnh vận tốc mới mỗi giây sẽ làm rung hộp số và tranh chấp tài nguyên. Thay vào đó, chỉ trích xuất và ra quyết định ở nhịp 5–10 Hz, gửi một lệnh `Twist` (hoặc lệnh dừng rõ ràng) rồi giữ đến chu kỳ tiếp theo.

Theo [REP-103](https://www.ros.org/reps/rep-0103.html), hệ tọa độ thân xe (`camera_link`) có `x` hướng trước, `y` sang trái, `z` hướng lên; trong khi hệ tọa độ quang học (`camera_optical_frame` — giá trị ghi vào `frame_id` của ảnh) có `z` hướng dọc trục ống kính ra trước, `x` sang phải ảnh và `y` hướng xuống dưới ảnh. Phép chuyển tĩnh phổ biến từ `camera_link` sang `camera_optical_frame` gồm roll $$-\pi/2$$ và yaw $$-\pi/2$$ (luôn kiểm tra lại trong URDF của bạn). Tọa độ pixel chưa phải tọa độ 3D trong `base_link` nếu chưa áp dụng phép chiếu và phép quay này; trong phạm vi bài này ta chỉ cần điều khiển quay trực tiếp theo độ lệch ngang trên ảnh.

## Ví dụ làm từng bước

Đoạn mã dưới đây cài đặt trọn vẹn thuật toán độc lập với ROS: mở camera đầu tiên, lọc một dải màu cam rộng trong không gian HSV và in tọa độ trọng tâm. Nếu thẻ của bạn có màu khác (ví dụ màu xanh), hãy điều chỉnh cận dưới/trên và ghi lại vào sổ. Chạy lệnh:

```bash
python3 card_centroid.py
```

```python
import sys
import cv2
import numpy as np

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("error: cannot open /dev/video0")
    sys.exit(1)

ok, frame = cap.read()
cap.release()
if not ok:
    print("error: camera opened but read failed")
    sys.exit(1)

hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
lower = np.array([5, 120, 80])
upper = np.array([25, 255, 255])
mask = cv2.inRange(hsv, lower, upper)
moments = cv2.moments(mask)
area = moments["m00"]
if area < 500:
    print("centroid none area=0")
else:
    u = int(moments["m10"] / area)
    v = int(moments["m01"] / area)
    print(f"centroid u={u} v={v} area={int(area)}")
```

Đưa tấm thẻ cam ra trước ống kính dưới nguồn sáng ổn định. Kết quả thành công có dạng:

```text
centroid u=312 v=248 area=1840
```

Giá trị cụ thể sẽ khác tùy vị trí: `u` tăng khi thẻ dịch sang phải, `area` tăng khi thẻ tiến lại gần. Nếu kết quả là `centroid none area=0`, hãy kiểm tra lại ánh sáng rồi mới chỉnh ngưỡng HSV. Nếu máy không có camera, dòng `error: cannot open /dev/video0` là kết quả ghi nhận hợp lệ — tuyệt đối không bịa số liệu trọng tâm.

Khi chuyển thành node ROS về sau, timer sẽ quyết định ở tần số 5–10 Hz: nếu `area < 500` thì phát `Twist` bằng 0; nếu `u` nằm bên trái tâm thì đặt `angular.z` khoảng `0.3`; nếu nằm bên phải thì khoảng `-0.3`, rồi giữ nguyên lệnh tới chu kỳ kế tiếp.

## Lab

Lưu đoạn mã trên thành `card_centroid.py` và chạy thử; đối chiếu kết quả theo đúng tình trạng phần cứng của bạn:

- Có camera và phát hiện được thẻ:

```text
centroid u=312 v=248 area=1840
```

- Có camera nhưng mặt nạ rỗng:

```text
centroid none area=0
```

- Không tìm thấy thiết bị camera:

```text
error: cannot open /dev/video0
```

Trong trường hợp không có thiết bị, chạy thêm `ls /dev/video*` và dán thông báo lỗi của shell vào sổ. Sau đó viết bốn câu trình bày rõ toàn bộ pipeline (ánh sáng, thiết bị, phân ngưỡng, trọng tâm) và giải thích vì sao không nên xuất bản `Twist` ở trọn tốc độ khung hình.

| Hiện tượng | Nguyên nhân thường gặp | Hướng kiểm tra |
| --- | --- | --- |
| `error: cannot open /dev/video0` | Không có camera UVC, hoặc dùng nhầm cáp chỉ sạc | Kiểm tra `ls /dev/video*` và đổi cổng USB |
| Camera mở được nhưng luôn báo `centroid none` | Ngưỡng hue không hợp với ánh sáng hoặc thẻ ngoài khung hình | Kiểm tra độ tương phản thẻ bằng mắt trước khi chỉnh cận |
| Trọng tâm nhảy hàng chục pixel dù thẻ đứng yên | Ánh sáng trộn lẫn (nắng + đèn) hoặc vùng mặt nạ quá nhỏ | Dùng một nguồn sáng ổn định và tăng ngưỡng diện tích |
| Động cơ rung mạnh khi nối với `Twist` | Xuất bản lệnh theo trọn tốc độ khung hình 30 Hz | Dùng timer 5–10 Hz, mỗi nhịp gửi một lệnh |
| Thẻ dịch sang phải ngoài đời nhưng `u` giảm | Ảnh bị lật gương hoặc đảo dấu góc yaw | Đảm bảo trục `u` tăng dần từ trái sang phải trên mảng ảnh |
| Tính toán hướng nhắm theo trục `camera_link` | Nhầm quy ước trục (`y` quang học hướng xuống, `z` thân hướng lên) | Đối chiếu chuẩn REP-103 phân biệt hệ quang học và hệ thân |

## Mua camera ở Việt Nam

Camera chiều sâu (như RealSense) nằm ngoài yêu cầu của bài. Bạn chỉ cần tìm trên Shopee với từ khóa `camera USB UVC` (giá tham khảo khoảng 150.000–450.000 đồng, lưu ý tránh cáp chỉ sạc). Một lựa chọn khác cho Raspberry Pi là camera dùng cảm biến IMX219 (ví dụ Waveshare IMX219-77 từng niêm yết khoảng 432.000 đồng, cần kiểm tra lại giá hiện tại). Cả hai loại đều dùng tốt cho script OpenCV và topic ảnh ROS.

## Video tham khảo

- **Xem trước:** [Control your Webcam with Python - OpenCV Beginners Tutorial #4](https://www.youtube.com/watch?v=sd25t4HmFdU) — Sam Westby Tech (tiếng Anh). Hướng dẫn đọc khung hình từ webcam bằng OpenCV — bước khởi đầu trực tiếp cho pipeline trong bài.
- [OpenCV Python Camera Calibration (Intrinsic, Extrinsic, Distortion)](https://www.youtube.com/watch?v=H5qbRTikxI4) — Kevin Wood | Robotics & AI (tiếng Anh). Giới thiệu ma trận nội tại và méo ống kính (chỉ cần nắm khái niệm, chưa cần chạy hiệu chỉnh trong bài này).

## Bài tập

### Bài 1

Tấm thẻ màu biến mất khỏi mặt nạ mỗi khi mở cửa sổ và xuất hiện lại khi kéo rèm, dù giữ nguyên cận HSV. Bạn cần xử lý tầng nào trước và giữ nguyên tầng nào?

**Gợi ý.** Tầng ánh sáng đứng đầu tiên — điều chỉnh nguồn sáng trong phòng trước, không vội sửa công thức tính mô-men.

### Bài 2

Một mặt nạ chỉ có bốn điểm ảnh trắng tại $$(10, 10)$$, $$(14, 10)$$, $$(12, 16)$$ và $$(12, 12)$$ trên ảnh rộng 64 pixel. Tính $$c_x$$, $$c_y$$ và cho biết vùng thẻ nằm bên trái hay bên phải tâm ảnh.

**Gợi ý.** Lấy trung bình cộng bốn hoành độ và bốn tung độ, sau đó so sánh $$c_x$$ với tâm ảnh là 32.

### Bài 3

Camera thu 30 khung hình/giây, nhưng vì sao cầu nối chỉ nên nhận lệnh `Twist` mới ở nhịp 5–10 Hz? Giải thích gắn với phần cứng xe Capstone.

**Gợi ý.** Giảm rung lắc cho hộp số động cơ và giúp dễ chia sẻ topic `/cmd_vel` với bộ điều hướng về sau nhờ dùng timer cố định.

### Bài 4

Nêu hướng của ba trục tọa độ trong hệ quang học và trong hệ thân theo REP-103. Hệ nào phải được ghi vào `frame_id` của ảnh?

**Gợi ý.** Hệ quang học: `z` hướng ra khỏi ống kính, `x` sang phải, `y` xuống dưới. Hệ thân: `x` hướng trước, `y` sang trái, `z` lên trên. Ảnh luôn gắn với hệ quang học.

### Bài 5

Khi script báo `error: cannot open /dev/video0`, hãy liệt kê ba bước kiểm tra có thể làm ngay mà không cần mua camera mới, đồng thời nêu phần bài nộp dạng văn bản vẫn cần hoàn thành.

**Gợi ý.** Chạy `ls /dev/video*`, thử cổng USB khác, ghi lại chính xác thông báo lỗi, và hoàn thiện bốn câu mô tả pipeline theo yêu cầu lab.

## Đọc thêm

- [Bài ngưỡng của OpenCV](https://docs.opencv.org/4.x/d7/d4d/tutorial_py_thresholding.html) — hướng dẫn phân đoạn `inRange` và kiểm tra trực quan mặt nạ trước khi tính trọng tâm.
- [usb_cam](https://github.com/ros-drivers/usb_cam) — tài liệu về `usb_cam_node_exe` và `camera.launch.py` cho camera V4L2 trên ROS 2.
- [REP-103](https://www.ros.org/reps/rep-0103.html) — chuẩn phân tách hệ trục thân và hệ trục quang học của ảnh.
