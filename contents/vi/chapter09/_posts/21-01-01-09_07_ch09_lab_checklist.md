---
layout: post
title: "Checklist lab chương 09"
chapter: "09"
order: 7
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter09
lesson_type: required
draft: false
---

Thời lượng: **~70 phút**. Mục kiểm tra cuối chương này yêu cầu bằng chứng thực tế rằng ROS 2 Jazzy đang chạy ổn định trên Ubuntu 24.04, đồ thị ROS có topic hoạt động và cây TF có ít nhất một cạnh tĩnh mà bạn giải thích được.

Kết thúc Chương 09, bạn đã chuyển từ lập trình đơn lẻ trên MCU sang vận hành trọn vẹn một ngăn xếp phần mềm **ROS 2 Jazzy** trên Linux: có workspace sạch, có launch file tham số hóa, có cây hệ tọa độ TF2 và mô hình URDF hiển thị trực tiếp trên RViz2. Danh sách nghiệm thu này đảm bảo mọi mảnh ghép đã khớp nhau chặt chẽ trước khi bước sang mô phỏng Gazebo và cầu nối phần cứng ở Chương 10.

## Bản đồ kiến thức nền: Ba tiêu chuẩn nghiệm thu Ngăn xếp ROS 2 (Chương 09)

1. **Tính tự động & Tái lập bằng một lệnh Launch**:
   Toàn bộ hệ thống (driver/mô phỏng, `robot_state_publisher`, RViz2) khởi chạy sạch sẽ từ một tệp launch duy nhất kèm cấu hình YAML.
2. **Tính nhất quán của Đồ thị Node–Topic–TF2**:
   Không có khung TF bị đứt gãy (`view_frames` tạo đúng một cây liên thông duy nhất), không có cảnh báo xung đột QoS và mọi tên topic tuân thủ quy ước chuẩn (`/cmd_vel`, `/odom`, `/tf`).
3. **Tính hợp lệ của Mô hình URDF/Xacro**:
   Kiểm tra qua `check_urdf`, bánh xe xoay đúng chiều khi đẩy `/joint_states` và mọi `<link>` đều có thông số quán tính hợp lý cho bước mô phỏng kế tiếp.

## Mục tiêu

Bạn cần hoàn thành và xác nhận đủ sáu tiêu chí: đúng phiên bản Ubuntu, workspace đã nạp đúng thứ tự, đọc được dữ liệu từ một topic, gọi được một service hoặc action, đồng bộ `ROS_DOMAIN_ID` (nếu dùng SBC) và kiểm chứng cạnh `base_link` tới frame cảm biến bằng `tf2_echo`. Bất kỳ mục nào thiếu log minh chứng đều chưa đạt.

## Kiến thức cần trước

Hoàn thành các bài từ 09-00 đến 09-06; máy tính (laptop hoặc SBC) đã kiểm tra được `printenv ROS_DISTRO`. Sổ thực hành chương 08 cần đã hoàn tất, hoặc ghi rõ những hạng mục còn tồn đọng của chương 08 vì cây TF không thể bù đắp cho thông số chiều rộng trục bánh bị đo sai.

## Vì sao bài này nằm trên lộ trình

Gazebo Harmonic ở chương 10 sẽ khởi chạy trực tiếp trên đồ thị ROS hiện tại. Nếu thêm `use_sim_time` lên một môi trường ROS vốn đã lỗi, số lượng topic bất thường sẽ tăng lên và rất khó gỡ. Do đó, cần xác nhận đồ thị ROS vận hành chuẩn xác ngay từ khi chưa có mô phỏng.

## Tiêu chí đạt và không đạt

**Phiên bản cài đặt.** Trên máy cài gói qua `apt`, `printenv ROS_DISTRO` phải trả về `jazzy` và `lsb_release -sc` phải là `noble`. Nếu mạch Jetson vẫn đang ở `jammy`, tiêu chí này chưa đạt cho đến khi bạn không cố cài Jazzy lên đó nữa. Lưu ảnh chụp màn hình terminal làm minh chứng.

**Workspace.** Biên dịch thành công ít nhất một gói trong `~/ros2_ws` bằng `colcon`, và khi mở terminal mới hệ thống phải tự động nạp underlay trước rồi đến overlay. Nếu `ros2 pkg list` không hiển thị gói của bạn ở terminal mới thì tiêu chí này chưa đạt (trừ khi bạn đã cấu hình đúng trong `.bashrc` và dán dòng cấu hình đó vào sổ).

**Topic.** Chạy `talker` hoặc node tự viết, dùng `ros2 topic echo` lấy ít nhất một bản ghi kèm tên kiểu message. Danh sách trống khi bạn chưa chạy bất kỳ publisher nào là chưa thực hiện, không phải "lỗi DDS".

**Service hoặc action.** Thực hiện thành công một lệnh gọi service/action, hoặc ghi lại rõ một lỗi đã gặp kèm cách khắc phục. Không có câu lệnh và log lưu trong sổ là chưa đạt.

**Máy tính nhúng (SBC).** Nếu có Raspberry Pi hoặc Jetson: cần có liên kết `/dev/esp32` (hoặc ghi chú kế hoạch hoãn có ngày cụ thể), kết quả `systemctl status` của unit `systemd` và xác nhận hai máy dùng chung `ROS_DOMAIN_ID`. Nếu chưa dùng SBC, ghi rõ "chỉ dùng laptop" là đủ để đạt tiêu chí này.

**Cây tọa độ TF.** Lệnh `ros2 run tf2_ros tf2_echo base_link <frame>` phải in ra phép tịnh tiến theo đơn vị mét. Nếu xuất hiện hai publisher trên cùng một cạnh thì chưa đạt. Nếu bạn chủ động xoay góc yaw $90^\circ$, giá trị quaternion in ra phải xấp xỉ $(0,\ 0,\ 0{,}707,\ 0{,}707)$.

### Khung giải thích (nên đọc chậm): Bộ 4 lệnh kiểm tra nhanh "Sức khỏe ROS 2" trong 60 giây

Trước khi ký duyệt Chương 09, chạy đúng 4 lệnh sau và đối chiếu kỳ vọng:

| Lệnh kiểm tra | Kết quả đạt chuẩn | Dấu hiệu lỗi cần sửa ngay |
| :--- | :--- | :--- |
| `ros2 run tf2_tools view_frames` | 1 cây duy nhất `odom → base_link → ...` không đứt nhánh | Xuất hiện 2 cây rời nhau hoặc thời gian trễ TF âm |
| `ros2 topic hz /odom` | Tần số ổn định (ví dụ `20–50 Hz`), độ lệch chuẩn nhỏ | `no new messages` hoặc rớt nhịp thất thường |
| `ros2 topic info /scan --verbose` | QoS Publisher và Subscriber tương thích | `BEST_EFFORT` phát vào `RELIABLE` nhận |
| `check_urdf <(xacro robot.urdf.xacro)` | Báo `Successfully Parsed XML` và đúng số lượng link/joint | Lỗi cú pháp XML hoặc thiếu thẻ `<inertial>` |

## Lab

Sao chép mẫu sau vào sổ thực hành, điền đầy đủ kết quả thực tế (xóa các dòng không có minh chứng):

```text
## Ky duyet chuong 09
Ngay:
ROS_DISTRO=
Ubuntu codename=
pkg da build=
topic echo (lenh + 1 dong):
service/action:
SBC: co / khong. DOMAIN=
tf2_echo base_link -> :
```

### Lỗi thường gặp

| Hiện tượng | Hướng kiểm tra |
| --- | --- |
| Cả `humble` và `jazzy` xuất hiện trong cùng shell | Xóa bớt một dòng `source` trong `~/.bashrc` |
| `echo` không có dữ liệu | Publisher chưa chạy, khác `ROS_DOMAIN_ID`, hoặc không tương thích QoS |
| `tf2_echo` chờ mãi không in | Nhập sai tên frame; kiểm tra lại bằng `ros2 run tf2_tools view_frames` |
| Raspberry Pi chạy Ubuntu 26.04 | Không khớp kho gói `apt` của Jazzy; nạp lại Ubuntu 24.04 hoặc dừng ở tiêu chí bản cài |

## Video tham khảo

- **Xem trước:** [The ROS Transform System (TF) | Getting Ready to Build Robots with ROS #6](https://www.youtube.com/watch?v=QyvHhY4Y_Y8) — Articulated Robotics (tiếng Anh). Danh sách kiểm tra của chương yêu cầu một cây tọa độ hiển thị rõ ràng; video này giúp hình dung trực quan trước khi hoàn thành bước xác nhận.

## Bài tập

1. Tiêu chí nào không đạt nếu các topic vẫn giao tiếp được với nhau nhưng `lsb_release` trả về `jammy`?
2. Lệnh `tf2_echo` báo $x = 10$ trong khi cảm biến lidar chỉ cách tâm xe 10 cm. Bạn đang nhập sai đơn vị nào?
3. Vì sao ghi nhận "chỉ dùng laptop" vẫn được tính là đạt tiêu chí SBC?

### Gợi ý đáp án

1. Tiêu chí phiên bản cài đặt không đạt, vì các topic hoạt động không chứng minh bạn đang dùng đúng bản Ubuntu 24.04 cho Jazzy.
2. Sai đơn vị mét: hệ thống hiểu $10$ là 10 m thay vì $0{,}10$ m.
3. SBC chỉ cần khi đưa hệ thống lên xe thật, không phải điều kiện bắt buộc để học đồ thị ROS; việc ghi nhận minh bạch phạm vi thực hành được chấp nhận, còn bỏ trống không báo cáo thì không.

## Đọc thêm

- [Cài Jazzy](https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html)
- [Về TF2](https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-TF2.html)
- [Bài Linux trên SBC]({% multilang_post_url contents/chapter09/09_00_linux_on_sbc %})
