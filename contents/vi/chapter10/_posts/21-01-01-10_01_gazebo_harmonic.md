---
layout: post
title: "Giới thiệu Gazebo Harmonic"
chapter: "10"
order: 1
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter10
lesson_type: required
draft: false
---

Thời lượng: **~70 phút**.

Nếu mỗi lần sửa một dòng thuật toán tránh vật cản bạn lại phải nạp firmware, sạc pin, đặt robot xuống sàn và chạy theo đỡ khi xe lao vào chân bàn, tốc độ nghiên cứu sẽ chậm đi hàng chục lần. **Gazebo Harmonic** là phòng thí nghiệm vật lý số giúp bạn kiểm thử hàng trăm kịch bản va chạm, trơn trượt và cảm biến giả lập ngay trên máy tính trước khi chạm vào phần cứng thật.

## Bản đồ kiến thức nền: Ba trụ cột của Mô phỏng Vật lý Gazebo Harmonic

1. **Động cơ vật lý (Physics Engine — DART) & Bước thời gian mô phỏng**:
   Tính toán trọng lực, ma sát lốp–sàn, mô-men động cơ và va chạm ở từng bước rời rạc (thường `max_step_size = 0.001 s`, tức 1000 Hz) rồi xuất thời gian mô phỏng lên topic `/clock`.
2. **Cầu nối `ros_gz_bridge` & Tách biệt đồng hồ (`use_sim_time`)**:
   Gazebo Harmonic dùng hệ thống truyền tin riêng (`gz-transport`). `ros_gz_bridge` ánh xạ hai chiều giữa topic Gazebo và ROS 2 (`/cmd_vel`, `/odom`, `/scan`, `/clock`). Mọi node ROS 2 khi chạy mô phỏng **bắt buộc** đặt `use_sim_time:=true` để không bị lệch đồng hồ tường!
3. **Hệ số Thời gian Thực (RTF — Real-Time Factor)**:
   $$\text{RTF} = \frac{\text{Thời gian mô phỏng trôi qua}}{\text{Thời gian thực ngoài đời}}$$. Nếu $$\text{RTF} = 1{,}0$$, 1 giây trong Gazebo đúng bằng 1 giây thật; nếu $$\text{RTF} < 0{,}5$$ do máy yếu hoặc mesh quá nặng, thuật toán điều khiển thời gian thực sẽ bị méo nhịp.

## Mục tiêu

Sau bài học này, bạn sẽ mở được một môi trường mô phỏng (world) của Gazebo Harmonic từ terminal ROS 2 Jazzy và phân biệt rõ lệnh `gz sim` với tệp thực thi `gazebo` của dòng Classic cũ. Bạn sẽ giải thích được vì sao khóa học kết hợp Jazzy với Harmonic, và vì sao việc nạp Humble hoặc cài gói Classic sẽ dẫn sang một bộ mô phỏng khác. Bạn dùng `gz topic -l` để xác nhận world đang chạy đã có `/clock`, hiểu vai trò của cờ `-r` gắn với nút chạy (play) để không nhầm trạng thái tạm dừng là lỗi cài đặt, đồng thời đọc hiểu ký hiệu chiều truyền dữ liệu của `ros_gz_bridge` (chưa chạy cầu nối trong bài này). Cuối cùng, bạn lưu lại ảnh cửa sổ giao diện hoặc log chạy server không màn hình làm minh chứng world trống hoạt động bình thường.

## Kiến thức cần trước

Hoàn thành bài 09-01: máy chạy Ubuntu 24.04 đã cài ROS 2 Jazzy từ gói `.deb` và `printenv ROS_DISTRO` trả về `jazzy`. Bạn cần thao tác quen với hai cửa sổ terminal song song và biết dùng Ctrl-C để dừng tiến trình đang chạy. Bài này chưa cần robot thật, chưa cần URDF hay firmware micro-ROS. Nếu `printenv ROS_DISTRO` đang trả về `humble`, hãy khắc phục dứt điểm trước khi cài bất kỳ gói nào bên dưới.

## Vì sao bài này nằm trên lộ trình

Capstone A đã vận hành bằng khung truyền chương 08, còn chương 09 đã chuẩn bị sẵn topic, TF và tệp `xacro` trên laptop. Bài này mở ra môi trường mô phỏng mà Nav2 sẽ dùng để lập kế hoạch đường đi và các thuật toán học máy về sau có thể ghi dữ liệu bag để đối chiếu với thực tế. Thành phần kết nối giữa ROS và Gazebo là họ gói `ros_gz`, không phải gói `gazebo_ros` của bản Classic. Việc làm quen đúng tên tiến trình khi world còn trống giúp bạn tách bạch lỗi: nếu bài sau gặp trục trặc khi đưa robot vào mô phỏng (spawn), bạn sẽ biết chắc đó là lỗi mô hình chứ không phải cài nhầm phiên bản Gazebo.

![Gazebo Harmonic cạnh ROS 2 Jazzy, ros_gz ở giữa]({{ site.imgurl }}/generated/ch10_gazebo_stack.png)

## Khái niệm

Gazebo Classic và Gazebo Sim là hai hệ thống mã nguồn khác nhau dù mang tên gần giống nhau. Classic dùng lệnh `gazebo` thường xuất hiện trong các hướng dẫn ROS 1 cũ. Gazebo Sim là dòng phát triển hiện hành: dùng lệnh `gz sim`, định dạng world là SDF và liệt kê topic bằng `gz topic`. Harmonic là phiên bản Gazebo Sim được biên dịch đồng bộ với ROS 2 Jazzy (trong khi Humble đi cùng Fortress). Các hướng dẫn yêu cầu chạy `sudo apt install gazebo` hoặc `ros-humble-gazebo-ros-pkgs` không phù hợp cho chương này.

Tên gói tổng hợp (metapackage) trên `apt` cho Jazzy là:

```bash
sudo apt install ros-jazzy-ros-gz
```

Gói này cài đặt sẵn các thành phần khóa học sử dụng, gồm `ros_gz_sim` (để khởi chạy và spawn mô hình) và `ros_gz_bridge` (để chuyển tiếp topic giữa hai đồ thị ROS và Gazebo). Cài đặt xong không tự động chạy world mà chỉ đưa các tệp thực thi vào đường dẫn ROS sau khi bạn nạp Jazzy.

Trong bài này ta dùng hai world có sẵn: `shapes.sdf` chứa vài khối hình học cơ bản để kiểm tra khả năng dựng hình đồ họa, còn `empty.sdf` là world trống mà các bài sau sẽ đưa robot Capstone vào. Câu lệnh khởi chạy theo tài liệu `ros_gz`:

```bash
ros2 launch ros_gz_sim gz_sim.launch.py gz_args:="empty.sdf -r"
```

Chuỗi trong `gz_args` được truyền trực tiếp cho `gz sim`. Cờ `-r` yêu cầu mô phỏng bắt đầu chạy ngay; nếu thiếu `-r`, server chỉ nạp world rồi dừng ở trạng thái tạm dừng (pause) khiến đồng hồ mô phỏng đứng yên tại 0 — điều này sẽ làm mọi node bật `use_sim_time` về sau bị đứng vì `/clock` không tăng.

`/clock` ban đầu là topic nội bộ của Gazebo chứ chưa xuất hiện trên ROS. Khi server đang chạy, `gz topic -l` sẽ liệt kê `/clock` ngay cả khi chưa bật cầu nối. Ký hiệu chiều truyền tin trong cầu nối rất dễ nhầm, nên ở bài này ta chỉ đọc phần trợ giúp mà chưa chạy cầu:

```bash
ros2 run ros_gz_bridge parameter_bridge -h
```

Ký hiệu nằm giữa kiểu dữ liệu ROS và kiểu dữ liệu Gazebo quy định chiều truyền. Hai dạng khóa học sẽ dùng (theo README của `ros_gz_bridge`) là cầu nối hai chiều cho lệnh vận tốc và cầu nối một chiều cho đồng hồ. Dạng hai chiều:

```bash
ros2 run ros_gz_bridge parameter_bridge /cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist
```

Dạng một chiều cho đồng hồ (chỉ từ Gazebo sang ROS):

```bash
ros2 run ros_gz_bridge parameter_bridge /clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock
```

Tuyệt đối không đảo ngược chiều đồng hồ, vì nếu có thêm một publisher thứ hai phát lên `/clock` sẽ gây xung đột với bộ mô phỏng. Chúng ta sẽ thực sự chạy hai lệnh này ở bài 10-02.

Thời gian mô phỏng và thời gian thực (wall time) không phải lúc nào cũng trùng nhau. Tỉ số giữa chúng gọi là hệ số thời gian thực (Real-Time Factor, RTF):

$$
\mathrm{RTF} = \frac{\Delta t_{\mathrm{sim}}}{\Delta t_{\mathrm{wall}}}
$$

Khi giao diện báo hệ số gần bằng 1, một giây mô phỏng tương ứng xấp xỉ một giây đồng hồ thực. Nếu hệ số tụt xuống thấp, lệnh vận tốc 0,2 m/s vẫn tạo ra quãng đường 0,2 m trên mỗi giây mô phỏng, nhưng thời gian thực bên ngoài sẽ trôi nhanh hơn. Trên một chiếc laptop bình thường, world trống cần đạt RTF gần bằng 1.

Chế độ không giao diện (headless) chạy cùng một server mô phỏng nhưng không mở cửa sổ GUI. Nếu `printenv DISPLAY` trả về rỗng, bạn không thể mở giao diện đồ họa mà cần thêm cờ chỉ chạy server (thường là `-s`, kiểm tra trong `gz sim --help`):

```bash
ros2 launch ros_gz_sim gz_sim.launch.py gz_args:="empty.sdf -r -s"
```

Bài lab vẫn đạt yêu cầu trên chế độ này nếu tiến trình không tự thoát và `gz topic -l` liệt kê được `/clock`. Hãy thực hành bài này trên laptop; Raspberry Pi 5 chỉ phù hợp chạy các tác vụ nhẹ hơn về sau, không dùng để thử giao diện Gazebo.

## Ví dụ làm từng bước

Thực hiện lần lượt ba lệnh kiểm tra để xác định đúng phiên bản Gazebo sắp chạy:

```bash
printenv ROS_DISTRO
gz sim --help
apt-cache policy ros-jazzy-ros-gz
```

Dòng đầu phải trả về `jazzy` và nội dung trợ giúp phải thuộc về `gz sim`. Nếu shell báo `gz: command not found`, hãy nạp lại Jazzy rồi kiểm tra `apt-cache policy`. Nếu không thấy gói ứng viên nào, nghĩa là máy chưa thêm nguồn `apt` của Jazzy hoặc không chạy Ubuntu 24.04 — không được "chữa cháy" bằng cách cài gói `gazebo` vì bản Classic không tương thích với tệp launch của chương này.

Khi gói đã sẵn sàng, khởi chạy world trống ở terminal thứ nhất và giữ tiến trình hoạt động:

```bash
source /opt/ros/jazzy/setup.bash
ros2 launch ros_gz_sim gz_sim.launch.py gz_args:="empty.sdf -r"
```

Mở terminal thứ hai, nạp Jazzy rồi liệt kê các topic bên phía Gazebo:

```bash
source /opt/ros/jazzy/setup.bash
gz topic -l
```

Kiểm tra sự xuất hiện của `/clock`. Lúc này `ros2 topic list` vẫn gần như trống vì chưa có cầu nối giữa hai đồ thị; Gazebo đang xuất bản trên hệ thống nội bộ của riêng nó. Nếu bạn nhấn Ctrl-C ở terminal đầu tiên, server tắt và danh sách topic Gazebo cũng biến mất.

### Khung giải thích (nên đọc chậm): Tính tay ảnh hưởng của `RTF = 0,4` và lỗi quên `use_sim_time`

Giả sử bạn chạy mô phỏng một thế giới phức tạp trên laptop không có GPU rời nên **RTF tụt xuống `0,4`** (mất 2,5 giây ngoài đời mới mô phỏng xong 1 giây trong Gazebo):
- Nếu bạn ra lệnh cho xe chạy với $$v = 0{,}5\text{ m/s}$$ trong đúng **4 giây thời gian mô phỏng**, xe đi đúng `2,0 m` trong thế giới ảo (nhưng ngoài đời bạn phải ngồi nhìn màn hình mất $$4 / 0{,}4 = \mathbf{10\text{ giây}}$$).
- **Thảm họa nếu quên bật `use_sim_time:=true` trên một node điều khiển:** Gazebo gán dấu thời gian `/scan` theo `/clock` (ví dụ `t = 12,0 s`), trong khi node quên cờ lại dùng đồng hồ hệ thống Unix (`t = 1.732.000.000 s`) → TF2 lập tức báo lỗi **`Extrapolation Error`** và loại bỏ toàn bộ dữ liệu cảm biến!

## Lab

1. Kiểm tra phiên bản ROS bằng `printenv ROS_DISTRO`. Nếu chưa phải `jazzy`, nạp lại `/opt/ros/jazzy/setup.bash` rồi kiểm tra lại (nếu máy cài cả Humble và Jazzy, lần `source` sau cùng sẽ có hiệu lực).
2. Cài gói `sudo apt install ros-jazzy-ros-gz`. Tuyệt đối không cài thêm gói `gazebo` hay `ros-humble-gazebo-ros-pkgs`.
3. Ở terminal A, khởi chạy world trống với `gz_args:="empty.sdf -r"` và để tiến trình chạy ở chế độ foreground.
4. Nếu không thấy cửa sổ hiện ra, kiểm tra `printenv DISPLAY`. Nếu biến này trống, dừng lệnh trước và khởi chạy lại với cờ `-s` như hướng dẫn chế độ headless ở trên.
5. Ở terminal B, nạp Jazzy và chạy `gz topic -l` để xác nhận có `/clock`. Chưa chạy `parameter_bridge` ở bài này.
6. Chạy `ros2 run ros_gz_bridge parameter_bridge -h`, ghi lại ký hiệu cho chiều hai hướng và chiều từ Gazebo sang ROS, rồi thoát trợ giúp. `ros2 topic list` lúc này chưa cần hiển thị `/clock`.
7. *(Tùy chọn, ~5 phút)* Chạy thử `shapes.sdf` thay cho `empty.sdf` để quan sát các khối hình học, sau đó quay lại `empty.sdf -r` (bài 10-02 sẽ spawn mô hình vào world tên `empty`).

**Kết quả mong đợi**

Cửa sổ Gazebo Sim mở ra ở trạng thái đang chạy nhờ cờ `-r` (hoặc tiến trình server chạy ổn định khi dùng `-s`). Terminal thứ hai in danh sách topic chứa `/clock`, và không có tiến trình `parameter_bridge` nào đang chạy:

```text
/clock
/stats
```

Danh sách thực tế sẽ dài hơn, nhưng bắt buộc phải có `/clock`. Khi chưa bật cầu nối, `ros2 topic list` chưa cần hiển thị `/clock`.

**Các lỗi thường gặp**

| Hiện tượng | Nguyên nhân thường gặp |
| --- | --- |
| `Unable to locate package ros-jazzy-ros-gz` | Không phải Ubuntu 24.04, hoặc chưa thêm nguồn `apt` của ROS 2 Jazzy |
| Lệnh `gazebo` mở cửa sổ khác, không có `gz sim` | Đang cài bản Gazebo Classic; chương này sử dụng `gz sim` |
| Lệnh launch thoát ngay hoặc không mở được GUI | Biến `DISPLAY` trống; chuyển sang cờ `-s` hoặc chạy trên máy có màn hình |
| `printenv ROS_DISTRO` in ra `humble` | Shell đã nạp nhầm Humble sau cùng nên không dùng được `ros_gz` của Jazzy |
| `gz topic -l` không kết nối được | Terminal khởi chạy world đã bị đóng khiến server ngừng hoạt động |
| Nút play ở trạng thái tạm dừng, thời gian đứng tại 0 | Quên cờ `-r`; bấm play để kiểm tra thời gian chạy, sau đó launch lại có `-r` |

## Mua ở Việt Nam

Bài lab này thực hiện hoàn toàn bằng phần mềm trên laptop đã cài Jazzy, không cần cảm biến hay ESP32. Raspberry Pi 5 chỉ là tùy chọn cho máy tính đặt trên robot về sau, không dùng để chạy GUI Gazebo. Giá tham khảo năm 2026 trên Hshop cho bản RAM nhỏ khởi điểm khoảng 2,4 triệu đồng (cần kiểm tra lại giá hiện tại trước khi mua): [Raspberry Pi 5 made in UK](https://hshop.vn/may-tinh-raspberry-pi-5-made-in-uk) và [basic kit](https://hshop.vn/combo-raspberry-pi-5-ram-4-8gb-basic-kit). Nếu đường dẫn thay đổi, tìm trực tiếp "Raspberry Pi 5" trên [hshop.vn](https://hshop.vn/). Trên Shopee hoặc Lazada, tìm với từ khóa `Raspberry Pi 5 4GB` và lưu ý các gói bán rẻ hơn đáng kể thường không kèm bộ nguồn chuẩn.

## Video tham khảo

- **Xem trước:** [Correctly Install Gazebo Harmonic Inside of ROS2 Jazzy Installation -Fix Gazebo Installation Issues](https://www.youtube.com/watch?v=dY8JxldcuqA) — Aleksandar Haber PhD (tiếng Anh). Hướng dẫn cài Gazebo Harmonic cùng ROS 2 Jazzy và tránh cài nhầm các gói Gazebo Classic.
- [ROS2 Jazzy Tutorial: Develop and Control Gazebo Model of Mobile Robot in ROS2 and Python](https://www.youtube.com/watch?v=campHHAPtyg) — Aleksandar Haber PhD (tiếng Anh). Ví dụ đưa mô hình xe vào Gazebo và điều khiển từ ROS 2 (video khá dài, nên tập trung vào đoạn spawn và `cmd_vel`).
- [Lấy dữ liệu 3D từ một vị trí trên trái đất](https://www.facebook.com/reel/2078352426052273) — Facebook Reel ngắn của Hoàng Quân (Cơ điện tử ICTU, [chinbi.com](https://chinbi.com)) về cách lấy dữ liệu địa hình 3D từ một vị trí thực tế. Trong Gazebo, mặt đất là một mô hình có đơn vị và gốc tọa độ riêng, nên dữ liệu 3D chỉ đưa vào world chính xác sau khi đồng bộ hai yếu tố này.

## Bài tập

1. Chạy `printenv ROS_DISTRO` và `gz sim --help`, rồi giải thích trong hai câu vì sao việc máy không có tệp thực thi `gazebo` là hoàn toàn bình thường. *Gợi ý:* bộ mô phỏng tương thích với Jazzy là `gz sim` thuộc dòng Harmonic, còn tệp `gazebo` thuộc bản Classic cũ.
2. Khởi chạy `empty.sdf` một lần không có `-r` và một lần có `-r`. Ghi lại trạng thái nút play và đồng hồ mô phỏng trong mỗi trường hợp. *Gợi ý:* khi thiếu `-r`, server nạp world ở trạng thái tạm dừng nên `/clock` không tăng cho tới khi bạn bấm play.
3. Trong một phiên chạy, thời gian mô phỏng tăng 2,0 s trong khi đồng hồ thực trôi qua 4,0 s. Tính hệ số thời gian thực (RTF) và nhận xét xem kết quả này có bình thường với world trống trên laptop không. *Gợi ý:* RTF bằng thời gian mô phỏng chia thời gian thực, tức là 0,5; với world trống trên laptop, giá trị hợp lý cần gần 1 hơn.
4. Nêu tên gói `apt` cần cài trong bài này và hai tên gói dễ cài nhầm kéo theo sai bộ mô phỏng. *Gợi ý:* cài `ros-jazzy-ros-gz`; tránh cài `gazebo` hoặc gói `ros-humble-gazebo-ros`.
5. Ghi lại chính xác câu lệnh launch sẽ dùng lại ở bài sau (gồm tên tệp world và cờ `-r`). *Gợi ý:* tham số `gz_args` phải chứa `empty.sdf -r`, vì công cụ spawn sẽ tìm đúng world có tên `empty`.

## Đọc thêm

- [Bắt đầu với Gazebo Harmonic](https://gazebosim.org/docs/harmonic/getstarted/) — giới thiệu `gz sim`, world hình khối và cơ chế điều khiển chạy/tạm dừng.
- [Gazebo Harmonic với ROS](https://gazebosim.org/docs/harmonic/ros_installation/) — bảng ghép đôi chính thức giữa Jazzy, Harmonic và họ gói `ros_gz`.
- [Cài deb Jazzy trên Ubuntu](https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html) — kiểm tra lại nguồn `apt` nếu không tìm thấy `ros-jazzy-ros-gz`.
- [README ros_gz_bridge](https://github.com/gazebosim/ros_gz/blob/ros2/ros_gz_bridge/README.md) — giải thích chi tiết các ký hiệu `@` và `[` trước khi áp dụng ở bài 10-02.
