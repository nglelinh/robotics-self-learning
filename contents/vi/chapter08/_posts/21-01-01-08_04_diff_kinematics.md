---
layout: post
title: "Động học robot dẫn động vi sai"
chapter: "08"
order: 4
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter08
lesson_type: required
draft: false
---

Thời lượng ước tính: **~75 phút**.

Một robot hai bánh không hề hiểu "rẽ trái với bán kính 0,5 m" là gì — hai động cơ DC bên dưới chỉ biết quay ở vận tốc bao nhiêu vòng/phút. Cầu nối toán học biến ý định chuyển động của thân xe $$(v, \omega)$$ thành lệnh cho từng bánh xe $$(v_L, v_R)$$, và ngược lại biến số xung encoder thành vị trí $$(x, y, \theta)$$ trên sàn, chính là **động học dẫn động vi sai (differential-drive kinematics)**.

## Bản đồ kiến thức nền: Ba trụ cột của Động học Robot Vi sai

1. **Hệ tọa độ thân robot chuẩn REP-103**:
   Trục $$+x$$ hướng về mũi xe, $$+y$$ sang trái, $$+z$$ hướng lên trên; quy tắc bàn tay phải cho $$\omega > 0$$ là quay ngược chiều kim đồng hồ (rẽ trái, tức bánh phải chạy nhanh hơn bánh trái).
2. **Động học thuận, nghịch & Ràng buộc phi holonomic**:
   Hai phương trình tuyến tính $$v = (v_R + v_L)/2$$ và $$\omega = (v_R - v_L)/L$$ nối vận tốc bánh với vận tốc thân. Vì không có thành phần trượt ngang $$v_y = 0$$, robot là hệ *phi holonomic*: muốn dịch ngang bắt buộc phải thực hiện chuỗi quay–tiến–quay.
3. **Tích phân Odometry (Từ xung encoder đến tư thế $$(x, y, \theta)$$)**:
   Cộng dồn quãng đường vi phân $$\Delta s$$ và góc quay $$\Delta \theta$$ ở từng chu kỳ lấy mẫu $$\Delta t$$ giúp ước lượng vị trí liên tục — nhưng sai số trôi góc $$\Delta \theta$$ sẽ tích lũy theo thời gian nếu không có cảm biến ngoài (IMU/LiDAR) hiệu chỉnh.

## Mục tiêu

Sau bài này, bạn đo chính xác khổ vết (khẩu độ bánh) của khung Capstone, chuyển đổi vận tốc thân robot $$(v, \omega)$$ thành tốc độ vành bánh trái và phải, rồi tính ngược lại để kiểm chứng. Bạn biết dự đoán bán kính quay của một lệnh điều khiển trước khi robot di chuyển và giải thích được vì sao cơ cấu vi sai không thể trượt ngang. Hai phương trình động học này là phần cốt lõi của mọi hàm xử lý `cmd_vel` từ Chương 10 trở đi.

## Kiến thức cần trước

Bạn xác định đúng bánh trái và bánh phải theo hướng nhìn từ trên thân robot về phía mũi xe, và đã hoàn thành bài teleop vòng hở ở Chương 07. Dụng cụ mới duy nhất cần dùng là thước hoặc thước dây. Vòng PID ở Bài 08-03 là tùy chọn trong bài này: động học tạo ra tốc độ đặt mục tiêu, còn chạy thử bằng PWM vòng hở khi kê bánh trên không vẫn đủ để kiểm chứng chiều quay.

## Vì sao bài này nằm trên lộ trình

Thông điệp `geometry_msgs/Twist` không gửi trực tiếp lệnh “động cơ trái” hay “động cơ phải”. Nav2, `teleop_twist_keyboard` và các chính sách điều khiển về sau đều xuất vận tốc tịnh tiến và vận tốc góc trong hệ tọa độ thân robot; tầng điều khiển dưới phải giải động học nghịch để tính tốc độ hai bánh. Nếu nhập sai khổ vết bánh, bản đồ Chương 11 sẽ sai tỉ lệ dù thuật toán SLAM hoạt động chuẩn xác; nếu ngược dấu $$\omega$$, robot sẽ quay ra xa mục tiêu khiến bộ lập kế hoạch thất bại. Hãy viết hàm động học nghịch một lần duy nhất, ghi rõ đơn vị và gọi lại thống nhất từ node cầu nối serial.

![Nhìn từ trên: khẩu độ và tốc độ hai bánh]({{ site.imgurl }}/generated/ch08_diff_kinematics.png)

## Khái niệm

Theo quy ước REP-103, trục $$+x$$ hướng về phía trước, $$+y$$ sang trái và $$+z$$ hướng lên trên. Vận tốc góc $$\omega$$ dương tương ứng với chuyển động rẽ trái (bánh phải chạy nhanh hơn bánh trái). Gọi $$v_R$$ và $$v_L$$ là vận tốc dài tại vành bánh phải và bánh trái (m/s, dương khi tiến), còn $$L$$ là khổ vết bánh tính bằng mét — đo giữa hai tâm vết tiếp xúc mặt lốp, không phải chiều rộng tấm mica.

**Động học thuận** (từ tốc độ hai bánh suy ra vận tốc thân):

$$
v = \frac{v_R + v_L}{2}
$$

$$
\omega = \frac{v_R - v_L}{L}
$$

**Động học nghịch** (từ lệnh `Twist` suy ra tốc độ hai bánh):

$$
v_R = v + \omega \frac{L}{2}
$$

$$
v_L = v - \omega \frac{L}{2}
$$

Khi $$v = 0$$ và $$\omega \neq 0$$, hai bánh quay ngược chiều với cùng độ lớn vận tốc, làm robot xoay tại chỗ quanh tâm trục. Khi $$v \neq 0$$ và $$\omega \neq 0$$, bán kính quỹ đạo quay là:

$$
R = \frac{v}{\omega}
$$

Với $$\omega > 0$$ và $$v > 0$$, tâm quay tức thời nằm về phía bên trái robot một khoảng $$R$$. Lưu ý rằng khung vi sai không có thành phần vận tốc ngang $$v_y$$ (ràng buộc phi holonomic); mọi bộ điều khiển cố ra lệnh trượt ngang sẽ gây dao động — nguyên tắc này sẽ gặp lại khi cấu hình Nav2.

Bán kính bánh $$r$$ chỉ xuất hiện khi quy đổi sang tốc độ góc trục bánh hoặc số xung encoder:

$$
\dot{\theta} = \frac{v_{\text{wheel}}}{r}
$$

Không đưa $$r$$ vào phương trình tính $$v, \omega$$ để tránh nhầm lẫn giữa đơn vị vòng/giây (hoặc rad/s) và m/s trong cùng một biến.

Cần phân biệt rõ ba thang giá trị: tín hiệu trục joystick (không có đơn vị m/s) phải được quy đổi có chủ đích — ví dụ đẩy hết cần tiến tương ứng $$v = 0,3$$ m/s và gạt hết cần quay tương ứng $$\omega = 1,0$$ rad/s — và ghi chú rõ bên cạnh phương trình. Sau khi qua động học nghịch ra m/s ở vành bánh, một hàm quy đổi riêng sẽ ánh xạ sang thang số nguyên −100…100 của Bài 08-01 (dựa trên tốc độ đo thực tế ở Chương 07), tránh đặt hệ số cảm tính.

## Ví dụ làm từng bước

Đo trực tiếp giữa hai tâm vết tiếp xúc được $$L = 0,16$$ m và bán kính bánh $$r = 0,033$$ m. Xét lệnh rẽ trái nhẹ với $$v = 0,20$$ m/s và $$\omega = 0,50$$ rad/s:

$$
\frac{L}{2} = 0,08
$$

$$
v_R = 0,20 + 0,50 \times 0,08 = 0,24 \text{ m/s}
$$

$$
v_L = 0,20 - 0,50 \times 0,08 = 0,16 \text{ m/s}
$$

Kiểm tra ngược lại bằng động học thuận:

$$
v = \frac{0,24 + 0,16}{2} = 0,20
$$

$$
\omega = \frac{0,24 - 0,16}{0,16} = 0,50
$$

Bán kính quỹ đạo là $$R = 0,20 / 0,50 = 0,40$$ m. Trên mặt sàn, trung điểm trục bánh sẽ vẽ cung tròn bán kính khoảng 0,40 m vì bánh phải chạy trên vòng ngoài lớn hơn nên có tốc độ cao hơn bánh trái.

Nếu vòng PID cần vận tốc góc của trục bánh phải:

$$
\dot{\theta}_R = \frac{0,24}{0,033} \approx 7,27 \text{ rad/s}
$$

Đoạn mã Python sau có thể dùng trực tiếp trong node cầu nối Chương 10:

```python
def wheel_speeds(v: float, omega: float, track: float) -> tuple[float, float]:
    half = 0.5 * track
    return v - omega * half, v + omega * half  # trái, phải

def body_from_wheels(v_l: float, v_r: float, track: float) -> tuple[float, float]:
    return 0.5 * (v_r + v_l), (v_r - v_l) / track

assert abs(body_from_wheels(*wheel_speeds(0.2, 0.5, 0.16), 0.16)[1] - 0.5) < 1e-9
```

Kiểm tra trường hợp xoay tại chỗ với $$v = 0$$, $$\omega = 1,0$$ rad/s và $$L = 0,16$$ m: ta được $$v_R = 0,08$$ m/s và $$v_L = -0,08$$ m/s. Nếu cả hai giá trị đều dương thì dấu cộng/trừ trong công thức đang bị sai.

## Từ số đếm encoder tới tư thế

Các phương trình trên viết theo vận tốc vành bánh, còn cảm biến encoder trả về số xung đếm. Gọi $N$ là số xung trên mỗi vòng trục bánh, $r$ là bán kính lăn (mét), $\Delta c_L$ và $\Delta c_R$ là độ biến thiên số xung có dấu trong một chu kỳ cập nhật:

$$
\Delta s_L = \frac{2\pi r}{N}\Delta c_L, \qquad
\Delta s_R = \frac{2\pi r}{N}\Delta c_R
$$

$$
\Delta s = \frac{\Delta s_R + \Delta s_L}{2}, \qquad
\Delta \psi = \frac{\Delta s_R - \Delta s_L}{L}
$$

Trong mỗi chu kỳ ngắn, quỹ đạo xe xấp xỉ một cung tròn. Để giảm sai số rời rạc hóa, ta chiếu quãng đường $\Delta s$ theo hướng ở **giữa** chu kỳ (phương pháp điểm giữa — midpoint) thay vì hướng ở đầu chu kỳ:

$$
x \leftarrow x + \Delta s \cos\left(\psi + \frac{\Delta\psi}{2}\right)
$$

$$
y \leftarrow y + \Delta s \sin\left(\psi + \frac{\Delta\psi}{2}\right)
$$

$$
\psi \leftarrow \psi + \Delta\psi
$$

Nếu chỉ dùng góc $\psi$ đầu chu kỳ, mỗi đoạn quay sẽ bị trễ pha nửa bước. Khi đi thẳng ($\Delta\psi = 0$) hai cách cho kết quả giống nhau; khi xoay tại chỗ ($\Delta s = 0$) tọa độ $x, y$ đứng yên và chỉ góc $\psi$ thay đổi.

Xét ví dụ chuẩn với $r = 0{,}033$ m, $L = 0{,}16$ m và $N = 1440$ xung/vòng. Mỗi xung tương ứng quãng đường:

$$
\frac{2\pi \cdot 0{,}033}{1440} \approx 1{,}440 \times 10^{-4}~\mathrm{m}
$$

Để đi thẳng 1 m, mỗi bánh quay khoảng 6945 xung cùng chiều. Để xoay trái tại chỗ một góc $\pi/2$, mỗi bánh đi cung dài $(L/2)\cdot(\pi/2)$, tương ứng khoảng 873 xung (bánh phải dương, bánh trái âm). Nếu robot đi thẳng 1 m, xoay trái $\pi/2$ rồi đi tiếp 0,5 m, tư thế cuối sẽ rất gần $(1{,}00~\mathrm{m},\ 0{,}50~\mathrm{m},\ \pi/2)$ (sai lệch dưới 1 mm chỉ do làm tròn số xung nguyên).

![Đường odometry: thẳng, quay trái, thẳng]({{ site.imgurl }}/generated/ch08_odom_path.png)

```python
import math

def pose_from_counts(counts_l, counts_r, radius, track, counts_per_rev):
    """Từng phần tử là số đếm mới trong một nhịp, có dấu. Tư thế trả về theo mét và radian."""
    meters = 2.0 * math.pi * radius / counts_per_rev
    x = y = psi = 0.0
    for c_l, c_r in zip(counts_l, counts_r):
        ds_l = c_l * meters
        ds_r = c_r * meters
        ds = 0.5 * (ds_r + ds_l)
        dpsi = (ds_r - ds_l) / track
        psi_mid = psi + 0.5 * dpsi
        x += ds * math.cos(psi_mid)
        y += ds * math.sin(psi_mid)
        psi += dpsi
    return x, y, psi

r, L, N = 0.033, 0.16, 1440
meters = 2.0 * math.pi * r / N
c_straight = int(round(1.0 / meters))       # ~6945
c_turn = int(round((L / 2) * (math.pi / 2) / meters))  # ~873
c_short = int(round(0.50 / meters))          # ~3472
# 50 nhịp thẳng, 20 nhịp quay, 25 nhịp thẳng. Tổng đếm giữ nguyên.
ticks = (
    [(c_straight / 50, c_straight / 50)] * 50
    + [(-c_turn / 20, c_turn / 20)] * 20
    + [(c_short / 25, c_short / 25)] * 25
)
x, y, psi = pose_from_counts([a for a, _ in ticks], [b for _, b in ticks], r, L, N)
assert abs(x - 1.0) < 0.01 and abs(y - 0.5) < 0.01
assert abs(psi - math.pi / 2) < 0.02
print(round(x, 4), round(y, 4), round(psi, 4))
```

Kết quả in ra phải xấp xỉ `1.0 0.5 1.5708`. Nếu giá trị $y$ bị âm, bạn đã đảo nhầm bánh trái và bánh phải khi quay.

Hàm trên chính là phần lõi tạo nên thông điệp `nav_msgs/Odometry` sau này: $x, y$ và góc yaw (chuyển sang quaternion theo Bài 08-00) điền vào trường tư thế, còn $\Delta s / \Delta t$ và $\Delta\psi / \Delta t$ điền vào trường vận tốc — tuyệt đối không ghi trực tiếp số xung thô vào `linear.x`.

### Khung giải thích (nên đọc chậm): Tính tay quỹ đạo Odometry sau 2 bước thời gian $$\Delta t = 0{,}5\text{ s}$$

Giả sử robot có khổ vết $$L = 0{,}20\text{ m}$$, xuất phát tại gốc $$(x_0, y_0, \theta_0) = (0, 0, 0)$$. Trong mỗi nhịp $$\Delta t = 0{,}5\text{ s}$$, bộ mã hóa đo được vận tốc vành bánh $$v_L = 0{,}20\text{ m/s}$$ và $$v_R = 0{,}30\text{ m/s}$$:

1. **Tính vận tốc thân xe:**
   $$v = \frac{0{,}30 + 0{,}20}{2} = \mathbf{0{,}25\text{ m/s}}, \qquad \omega = \frac{0{,}30 - 0{,}20}{0{,}20} = \mathbf{0{,}50\text{ rad/s}}.$$
   Bán kính cung quay là $$R = v / \omega = 0{,}25 / 0{,}50 = \mathbf{0{,}50\text{ m}}$$ về phía bên trái.
2. **Cập nhật tư thế theo tích phân điểm giữa (Midpoint Odometry) mỗi bước $$\Delta s = v\Delta t = 0{,}125\text{ m}$$, $$\Delta\theta = \omega\Delta t = 0{,}25\text{ rad}$$:**

| Bước $$k$$ | Góc giữa $$\theta_{k-1} + \Delta\theta/2$$ | $$x_k$$ (m) | $$y_k$$ (m) | $$\theta_k$$ (rad) |
| :---: | :---: | :---: | :---: | :---: |
| 0 | — | $$0{,}000$$ | $$0{,}000$$ | $$0{,}000$$ |
| 1 | $$0{,}125\text{ rad}$$ | $$0 + 0{,}125\cos(0{,}125) \approx \mathbf{0{,}124}$$ | $$0 + 0{,}125\sin(0{,}125) \approx \mathbf{0{,}016}$$ | $$0{,}250$$ |
| 2 | $$0{,}375\text{ rad}$$ | $$0{,}124 + 0{,}125\cos(0{,}375) \approx \mathbf{0{,}240}$$ | $$0{,}016 + 0{,}125\sin(0{,}375) \approx \mathbf{0{,}062}$$ | $$0{,}500$$ |

Chú ý: nếu đo nhầm khổ vết $$L$$ sai 10% (ví dụ nhập $$0{,}18\text{ m}$$ thay vì $$0{,}20\text{ m}$$), góc quay tính ra sai lệch ngay 11% ở mỗi vòng quay — đó là lý do hiệu chuẩn thực nghiệm $$L$$ cực kỳ quan trọng trước khi vào SLAM!

## Lab

1. Đặt robot trên bàn (kê bánh trên không hoặc trên giá đỡ), đo khổ vết $$L$$ ba lần và ghi giá trị trung bình theo đơn vị mét.
2. Đánh dấu một điểm trên mỗi lốp bằng phấn hoặc băng dính. Gửi lệnh cùng tốc độ cho cả hai bánh trong 2 giây để xác nhận cả hai dấu đều quay tiến, chốt chắc dấu của $$v_L$$ và $$v_R$$ trong firmware.
3. Gửi lệnh xoay trái tại chỗ ở mức PWM thấp (tương ứng mức “tiến chậm” từ Chương 07) và xác nhận bánh phải quay tiến, bánh trái quay lùi.
4. (Tùy chọn trên sàn trống, tốc độ chậm): chạy lệnh $$v = 0,2$$ m/s, $$\omega = 0,5$$ rad/s khoảng một phần tư vòng và so sánh bán kính thực đo bằng thước với giá trị dự đoán $$R = v/\omega$$ tính theo $$L$$ thực tế của xe bạn.
5. Lưu hàm động học cùng giá trị $$L$$ đo được vào cùng một tệp Python để sẵn sàng import cho cầu nối ở Chương 10.

**Ghi chú mong đợi**

```text
L_mean = 0.158 m
lệnh bằng nhau: cả hai bánh tiến
v=0, w>0: phải tiến, trái lùi
R dự đoán = 0.40 m, R đo = 0.45 m  (trượt, đừng "sửa" bằng hệ số ngẫu nhiên)
```

Sai lệch bán kính khoảng 10% trên nền thảm là do trượt lốp, không phải lỗi công thức; nhưng nếu bánh trái quay sai chiều thì chắc chắn là lỗi dấu.

**Khi hỏng thì thường vì**

| Bạn thấy | Nguyên nhân hay gặp |
| --- | --- |
| Robot cua nhầm phía | Dấu $$\omega$$, hoặc tuple trái/phải bị đảo |
| Lệnh đi thẳng lại thành vòng | Thang PWM một bánh mềm hơn, hoặc một lốp nhỏ hơn. Động học không giấu được việc đó; PID thì có thể |
| Bán kính bằng một nửa dự đoán | Bạn đo chiều ngang tấm, hoặc dùng đường kính làm $$L$$ |
| Cả hai bánh lùi khi cua trái | Bạn đặt $$v_L = v + \omega L/2$$ |
| Về sau tỉ lệ bản đồ vô nghĩa | $$L$$ hoặc $$r$$ đang là centimét trong công thức mét |

## Mua ở Việt Nam

Bài này không cần mua thêm linh kiện điện tử; một thước dây 3 m (tìm `thước dây 3m`, khoảng 15.000–40.000 đồng trên Shopee) là đủ. Nếu lốp bị méo hoặc xẹp không đều, nên thay đồng bộ cả cặp để bán kính $$r$$ khớp nhau (tìm `bánh xe robot cao su 65mm`, khoảng 20.000–60.000 đồng/chiếc). Không trộn hai lốp khác đường kính trên cùng một trục.

## Video tham khảo

- **Xem trước:** [Differential Drive & Odometry Explained: How It Works](https://www.youtube.com/watch?v=2QE3LG5h2tw) — Netizen Robotics, tiếng Anh. Chuyển đổi từ vận tốc hai bánh sang vận tốc tiến và vận tốc góc — đúng cặp phương trình trong bài.
- [Modern Robotics, Chapter 13.4:  Odometry](https://www.youtube.com/watch?v=eQ9E0Zvp9jw) — Northwestern Robotics, tiếng Anh. Tích phân từng bước từ số đo bánh xe thành tư thế $(x, y, \psi)$.

## Bài tập

1. Khổ vết đo được là 0,20 m và lệnh joystick yêu cầu $$v = 0$$, $$\omega = -0,8$$ rad/s. Tính $$v_L$$, $$v_R$$ và gọi tên chuyển động. Gợi ý: bánh phải âm, bánh trái dương — robot xoay phải tại chỗ (yaw âm).
2. Cả hai bánh đều chạy ở 0,3 m/s. Tính $$v$$ và $$\omega$$. Gợi ý: $$v = 0,3$$ m/s, $$\omega = 0$$ rad/s, không phụ thuộc vào $$L$$.
3. Vì sao không tồn tại cặp $$(v_L, v_R)$$ nào thỏa mãn $$v_x = 0$$, $$v_y = 0,2$$ m/s và $$\omega = 0$$? Gợi ý: cấu trúc bánh vi sai chỉ tạo ra chuyển động dọc trục $$x$$ và quay quanh tâm, nên $$v_y$$ luôn bằng 0.
4. Bạn đo $$L = 15,5$$ cm nhưng nhập `0.155` ở một tệp và nhầm thành `15.5` ở node cầu nối. Hiện tượng gì sẽ xảy ra với bán kính quay $$R$$? Gợi ý: bán kính quay thực tế nhỏ đi 100 lần (sai lệch 100 lần), khiến robot gần như xoay tại chỗ với hầu hết các lệnh rẽ.
5. Hàm động học này nằm ở vị trí nào trong chuỗi xử lý cùng với PID? Gợi ý: `Twist` → hàm động học nghịch → hai tốc độ đặt (m/s) → hai vòng PID → hai mức PWM. Nếu bỏ qua PID, các giá trị m/s đầu ra chỉ mang tính ước lượng.

## Đọc thêm

- [REP-103, đơn vị và quy ước hệ tọa độ](https://www.ros.org/reps/rep-0103.html).
- [REP-105](https://www.ros.org/reps/rep-0105.html) về hệ tọa độ `base_link` nơi các phương trình này được định nghĩa.
- [Modern Robotics, chương 13](https://hades.mech.northwestern.edu/index.php/Modern_Robotics) (bản mở) — tài liệu chuyên sâu về động học robot bánh xe.
- `geometry_msgs/Twist` trong [tài liệu message Jazzy](https://docs.ros.org/en/jazzy/p/geometry_msgs/msg/Twist.html): `linear.x` là $$v$$, `angular.z` là $$\omega$$, bốn trường còn lại bằng 0 trên khung vi sai.
