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

Thời lượng ước tính: khoảng 75 phút khi camera USB xuất hiện thành `/dev/video0`, và khoảng 45 phút khi bạn ghi nhận thiết bị không có rồi vẫn đi hết pipeline trên giấy.

## Mục tiêu học

Bạn sắp pipeline theo ánh sáng, rồi camera, rồi thuật toán, và không chỉnh ngưỡng khi cửa sổ làm trắng thẻ. Bạn nói được `usb_cam` phát gì, tính centroid, hành động một lần ở 5 đến 10 Hz thay vì từng khung hình, nêu khung quang học khác `camera_link` theo REP-103, và ghi `/dev/video0` mất tích như một kết quả chứ không phải lab hỏng.

## Kiến thức cần có

Bạn chạy được một script Python ngắn và biết ảnh là một mảng. Bạn đã gặp `geometry_msgs/msg/Twist` ở tour Nav2, nên biết lệnh vận tốc có phần tịnh tiến và phần quay. Không cần camera độ sâu, và bài này không đòi RealSense.

## Vì sao bài này nằm trên lộ trình

Lộ trình là đế Capstone, rồi ROS 2 Jazzy, rồi Gazebo, rồi tự hành. Đế đã có cầu từ `cmd_vel` sang PWM. Jazzy là cách camera phát `sensor_msgs/msg/Image` cạnh topic lidar. Một thẻ trên bàn cho thấy ngưỡng gãy dưới ánh sáng thật nhanh hơn camera giả lập. Hành động ở đây khiêm tốn: quay về phía thẻ, hoặc dừng. Đó vẫn là Twist mà Nav2 phát. Vòng 30 Hz đánh nhau với cầu nối. Vòng 5 đến 10 Hz chia sẻ được robot với navigator sau.

## Khái niệm

Bắt đầu bằng ánh sáng. Thẻ đỏ dưới đèn trần và cùng thẻ đó trong nắng chiều là hai phép đo khác nhau. Mắt không thấy mảng tách biệt thì OpenCV không cứu demo. Dịch đèn hoặc tắt ngược sáng trước khi sửa hue. Camera đứng thứ hai: thiết bị USB UVC, thường là `/dev/video0`. `usb_cam` hoặc `v4l2_camera` phát `sensor_msgs/msg/Image`. Thuật toán đứng thứ ba, và ở đây là ngưỡng màu cộng centroid, không phải bộ phát hiện neural.

![Ảnh camera thành mặt nạ ngưỡng, rồi thành centroid có thể phát một lệnh yaw chậm]({{ site.imgurl }}/generated/ch11_vision.png)

Trên máy Jazzy đã cài gói nhị phân, hình dạng driver là:

```bash
sudo apt install ros-jazzy-usb-cam
source /opt/ros/jazzy/setup.bash
ros2 run usb_cam usb_cam_node_exe
```

`ros2 launch usb_cam camera.launch.py` thêm trình xem. Topic ảnh thường là `/image_raw`, kiểu `sensor_msgs/msg/Image`. Topic im thì sửa đường dẫn thiết bị trước mọi ngưỡng. Lab không bắt buộc node này. Nó gọi OpenCV trực tiếp.

Ngưỡng HSV ổn hơn kênh đỏ thô, và vẫn mong manh. Chốt một cận dưới, một cận trên, và ánh sáng bạn đã dùng. Mặt nạ trắng trên thẻ. Moment biến mặt nạ thành centroid. Với pixel $$(x_i, y_i)$$,

$$
c_x = \frac{\sum_i x_i}{N}, \qquad c_y = \frac{\sum_i y_i}{N},
$$

đúng việc `cv2.moments` làm khi chia `m10` cho `m00` và `m01` cho `m00`. Tính tay một mặt nạ ba pixel trắng tại $$(100, 80)$$, $$(102, 80)$$, và $$(101, 82)$$:

$$
c_x = \frac{100 + 102 + 101}{3} = 101, \qquad c_y = \frac{80 + 80 + 82}{3} \approx 80{,}67.
$$

Ảnh rộng 320 pixel thì tâm ngang là 160. Vệt nằm bên trái tâm. Camera nhìn thẳng thấy đó là "đích bên trái", nên đế vi sai phải quay trái, tức `angular.z` dương theo REP-103, cho đến khi centroid đi về phía tâm. Nếu diện tích `m00` quá nhỏ, không có thẻ. Đừng phát gì, hoặc phát twist bằng không, thay vì đuổi nhiễu.

Hành động phải chậm. Camera có thể đưa 30 khung mỗi giây. Động cơ không nên nhận 30 lệnh vận tốc mới mỗi giây từ pipeline này. Chọn một lần đọc ở 5 đến 10 Hz, phát một Twist hoặc một lệnh dừng rõ ràng, và giữ đến quyết định sau. Đủ tốc độ khung hình trông linh trong cửa sổ và làm hộp số rung.

[REP-103](https://www.ros.org/reps/rep-0103.html) cho thân `x` về trước, `y` sang trái, `z` lên trên. Khung quang học khác: `z` ra khỏi ống kính, `x` sang phải trên ảnh, `y` xuống dưới trên ảnh. `camera_link` thường là giá kiểu thân. `camera_optical_frame` là khung nên đóng dấu trên ảnh. Khớp tĩnh thường gặp từ `camera_link` kiểu thân dùng roll $$-\pi/2$$ và yaw $$-\pi/2$$. Vẫn đọc khớp trong URDF của bạn. Centroid theo pixel chưa phải điểm trong `base_link` khi chưa có phép quay đó và mô hình camera. Bài này không đòi phép chiếu. Quay theo pixel.

## Ví dụ làm từng bước

Script sau là cả thuật toán, không cần ROS. Nó mở camera đầu tiên, lấy ngưỡng một dải cam rộng trong HSV, và in một centroid. Cam chỉ là ví dụ. Thẻ của bạn màu xanh thì đổi cận và ghi số mới vào vở. Chạy từ thư mục bạn nhìn thấy terminal:

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

Giữ thẻ cam trước ống kính dưới một đèn ổn định. Dòng khỏe trông như:

```text
centroid u=312 v=248 area=1840
```

Số của bạn sẽ khác. `u` tăng khi thẻ sang phải. `area` tăng khi thẻ lại gần. `centroid none area=0` nghĩa là cận trượt đèn này: đổi ánh sáng, rồi đổi cận. `error: cannot open /dev/video0` là dòng lab hợp lệ. Ghi lại. Đừng bịa centroid.

Node ROS về sau quyết định ở 5 hoặc 10 Hz. `area` dưới 500 thì phát Twist không. `u` bên trái tâm thì `angular.z` gần 0.3. `u` bên phải thì `angular.z` gần -0.3. Giữ lệnh đến tick sau. Đủ để cầu nối giật bánh về phía thẻ. Không phải navigator.

## Lab

Lưu script thành `card_centroid.py` rồi chạy. Chọn kết quả mong đợi khớp máy bạn đang có.

Nếu có camera và thẻ nằm trong khung, dòng mong đợi theo mẫu sau, với số của bạn:

```text
centroid u=312 v=248 area=1840
```

Nếu có camera mà mặt nạ trống, dòng mong đợi là:

```text
centroid none area=0
```

Nếu không thiết bị nào hiện ra, dòng mong đợi là:

```text
error: cannot open /dev/video0
```

Trường hợp mất thiết bị, chạy thêm `ls /dev/video*` và dán lời than của shell vào cùng ghi chú. Rồi viết bốn câu vẫn giải thích pipeline: ánh sáng, thiết bị, ngưỡng, centroid, và vì sao không phát Twist ở đủ tốc độ khung hình. Thiếu thiết bị không xóa lời giải thích đó.

| Bạn thấy | Nguyên nhân hay gặp | Việc cần kiểm |
| --- | --- | --- |
| `error: cannot open /dev/video0` | Không có thiết bị UVC, hoặc cáp chỉ sạc | `ls /dev/video*` và cổng khác |
| Camera mở, mãi `centroid none` | Cận hue đánh nhau với đèn, hoặc thẻ ra ngoài khung | Nhìn thẻ bằng mắt, rồi mới nhìn cận |
| Centroid giật hàng chục pixel dù thẻ đứng yên | Nắng trộn đèn, hoặc mặt nạ quá nhỏ | Một đèn, nâng ngưỡng diện tích |
| Bánh rú khi sau này nối Twist | Bạn phát theo tốc độ khung hình | Timer 5 đến 10 Hz, một lệnh mỗi tick |
| Thẻ sang phải ngoài đời nhưng `u` giảm | Ảnh bị lật gương, hoặc dấu yaw bị đảo | Tin `u` tăng về phía phải của mảng |
| Bạn nhắm bằng trục `camera_link` | Quang học `y` đi xuống, thân `z` đi lên | REP-103: quang học khác thân |

## Mua camera ở Việt Nam

Camera độ sâu nằm ngoài phạm vi. Tìm Shopee bằng `camera USB UVC`. Webcam UVC thường gần đây khoảng 150 đến 450 nghìn đồng. Xem lại listing, và tránh cáp ghi là chỉ sạc.

Camera Pi loại IMX219 là lựa chọn kia, thường vài trăm nghìn đồng. Một Waveshare IMX219-77 từng niêm yết gần 432.000 đồng. Xem lại trang hiện tại trước khi đặt. Cả hai loại nuôi được script hoặc topic ảnh ROS. Không loại nào phải là RealSense.

## Bài tập

### Bài 1

Thẻ biến mất khỏi mặt nạ mỗi khi cửa sổ mở, và hiện lại khi bạn kéo rèm, cùng các số hue. Bạn gỡ tầng nào, và tầng nào để yên?

**Gợi ý.** Ánh sáng đứng trước. Đừng viết lại công thức moment. Nói bạn sẽ đổi gì trong phòng.

### Bài 2

Mặt nạ chỉ trắng tại $$(10, 10)$$, $$(14, 10)$$, $$(12, 16)$$, và $$(12, 12)$$. Tính $$c_x$$ và $$c_y$$. Ảnh rộng 64. Vệt nằm trái hay phải tâm?

**Gợi ý.** Trung bình bốn giá trị `x` và bốn giá trị `y`. Tâm là 32. So $$c_x$$ với 32.

### Bài 3

Camera phát 30 ảnh mỗi giây. Vì sao cầu nối chỉ nên thấy Twist mới 5 đến 10 lần mỗi giây? Lấy động cơ Capstone làm lý do.

**Gợi ý.** Nói về rung và về việc chia sẻ `cmd_vel` với navigator sau này. Một câu về timer là đủ.

### Bài 4

Nêu ba hướng trục của khung quang học, và ba hướng trục của khung thân REP-103. Khung nào phải được đóng dấu trên ảnh?

**Gợi ý.** Quang học: `z` ra khỏi ống kính, `x` phải, `y` xuống. Thân: `x` trước, `y` trái, `z` lên. Ảnh dùng khung quang học.

### Bài 5

Script in `error: cannot open /dev/video0`. Liệt kê ba việc kiểm tra dạy bạn điều gì đó mà không mua camera, và nói phần viết bạn vẫn còn nợ.

**Gợi ý.** `ls` thư mục thiết bị, thử cổng USB khác, ghi đúng câu lỗi. Bạn vẫn nợ bốn câu pipeline trong lab.

## Đọc thêm

- [Bài ngưỡng của OpenCV](https://docs.opencv.org/4.x/d7/d4d/tutorial_py_thresholding.html) là chỗ xem phân đoạn kiểu `inRange` và xem mặt nạ trước khi tin centroid.
- [usb_cam](https://github.com/ros-drivers/usb_cam) mô tả `usb_cam_node_exe` và `camera.launch.py` cho camera V4L2 trên ROS 2.
- [REP-103](https://www.ros.org/reps/rep-0103.html) là chuẩn tách trục thân khỏi khung quang học trên ảnh.
