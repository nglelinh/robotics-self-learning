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

Thời lượng: **~75 phút**.

## Mục tiêu

Bạn đo khẩu độ bánh của khung Capstone, đổi vận tốc thân $$(v, \omega)$$ thành tốc độ vành bánh trái và phải, rồi đổi ngược lại để kiểm tra số. Bạn dự đoán bán kính quay của một lệnh joystick trước khi robot nhúc nhích, và giải thích được vì sao khung vi sai không trượt ngang. Hai phương trình đó là thân của mọi callback `cmd_vel` từ chương 10 trở đi.

## Kiến thức cần trước

Bạn chỉ được bánh nào là bánh trái khi ngồi trên robot nhìn về phía trước. Teleop vòng hở chương 07 đã làm những bánh đó quay. Thước hoặc thước dây là đồ mới duy nhất. PID bài 08-03 là tùy chọn ở đây: động học ra đích tốc độ, PWM vòng hở vẫn cho thấy hình dạng của cú quay khi bánh ở trên không.

## Vì sao bài này nằm trên lộ trình

`geometry_msgs/Twist` không phải “động cơ trái” và “động cơ phải.” Nav2, teleop_twist_keyboard, và policy sau này đều xuất tốc độ tiến và tốc độ góc trong hệ thân robot. Ai đó phải nghịch đảo thành hai tốc độ bánh. Người đó dùng sai khẩu độ thì mọi bản đồ chương 11 sai tỉ lệ dù phần mềm SLAM hoàn hảo. Đổi dấu $$\omega$$ thì robot quay khỏi đích và planner “thất bại” vì lý do cơ khí. Viết hàm nghịch một lần, kèm đơn vị, và gọi nó từ cầu nối serial.

![Nhìn từ trên: khẩu độ và tốc độ hai bánh]({{ site.imgurl }}/generated/ch08_diff_kinematics.png)

## Khái niệm

REP-103 đặt $$+x$$ về phía trước, $$+y$$ sang trái, $$+z$$ lên trên. Tốc độ góc $$\omega$$ dương là cua trái: bánh phải nhanh hơn bánh trái. $$v_R$$ và $$v_L$$ là tốc độ vành bánh theo mét trên giây, dương khi tiến. $$L$$ là khẩu độ tính bằng mét, khoảng cách giữa hai vết tiếp xúc, không phải chiều ngang tấm mica và không phải khoảng cách hai trục nếu lốp phình.

Chiều thuận, từ bánh lên thân:

$$
v = \frac{v_R + v_L}{2}
$$

$$
\omega = \frac{v_R - v_L}{L}
$$

Chiều nghịch, từ Twist xuống bánh:

$$
v_R = v + \omega \frac{L}{2}
$$

$$
v_L = v - \omega \frac{L}{2}
$$

Nếu $$v = 0$$ và $$\omega \neq 0$$, hai bánh bằng nhau và ngược dấu, robot quay tại chỗ quanh tâm. Bán kính quay khi $$v \neq 0$$ là

$$
R = \frac{v}{\omega}
$$

tâm quay nằm bên trái robot một đoạn $$R$$ khi $$\omega > 0$$ và $$v > 0$$. Không có $$v_y$$. Lệnh đòi khung trượt ngang không phải lỗi nhỏ; cơ cấu không làm được. Bộ điều khiển bỏ qua điều đó sẽ dao động. Bạn gặp lại câu này trong tour Nav2.

Bán kính bánh $$r$$ chỉ xuất hiện khi bạn cần tốc độ trục hoặc số đếm encoder:

$$
\dot{\theta} = \frac{v_{\text{wheel}}}{r}
$$

Đừng đưa $$r$$ vào công thức $$v, \omega$$. Lỗi hay gặp là trộn vòng trên giây với mét trên giây trong cùng một biến.

Trục joystick không phải mét trên giây. Chọn thang có chủ đích, ví dụ cần đầy về trước là $$v = 0,3$$ m/s và cần yaw đầy là $$\omega = 1,0$$ rad/s, rồi viết thang đó cạnh phương trình. Số nguyên −100…100 của bài 08-01 là thang thứ ba. Một hàm đổi m/s của vành bánh sang số nguyên đó sau động học nghịch, dùng tốc độ bạn đã thấy ở PWM 100 trong bài quay chương 07. Đừng giấu thang trong câu “thấy hợp thì thôi.”

## Ví dụ làm từng bước

Đo thước: vết tiếp xúc đến vết tiếp xúc, $$L = 0,16$$ m. Bán kính bánh $$r = 0,033$$ m, chỉ dùng ở cuối. Lệnh: $$v = 0,20$$ m/s, $$\omega = 0,50$$ rad/s (cua trái nhẹ).

$$
\frac{L}{2} = 0,08
$$

$$
v_R = 0,20 + 0,50 \times 0,08 = 0,24 \text{ m/s}
$$

$$
v_L = 0,20 - 0,50 \times 0,08 = 0,16 \text{ m/s}
$$

Kiểm tra:

$$
v = \frac{0,24 + 0,16}{2} = 0,20
$$

$$
\omega = \frac{0,24 - 0,16}{0,16} = 0,50
$$

Bán kính $$R = 0,20 / 0,50 = 0,40$$ m. Trên sàn, một mẩu băng dính ở tâm hình học của trục nên đi vòng tròn bán kính khoảng 0,40 m. Lốp phải đi vòng lớn hơn lốp trái, nên nó nhanh hơn.

Tốc độ trục bánh phải, nếu PID cần:

$$
\dot{\theta}_R = \frac{0,24}{0,033} \approx 7,27 \text{ rad/s}
$$

Python để lát nữa dán vào cầu nối:

```python
def wheel_speeds(v: float, omega: float, track: float) -> tuple[float, float]:
    half = 0.5 * track
    return v - omega * half, v + omega * half  # trái, phải

def body_from_wheels(v_l: float, v_r: float, track: float) -> tuple[float, float]:
    return 0.5 * (v_r + v_l), (v_r - v_l) / track

assert abs(body_from_wheels(*wheel_speeds(0.2, 0.5, 0.16), 0.16)[1] - 0.5) < 1e-9
```

Quay tại chỗ, $$v = 0$$, $$\omega = 1,0$$, $$L = 0,16$$: $$v_R = 0,08$$, $$v_L = -0,08$$. Nếu cả hai số đều dương, bạn đã cộng $$\omega L$$ vào cả hai bánh thay vì tách dấu.

## Lab

1. Đặt robot lên bàn, bánh trên không hoặc trên giá. Đo $$L$$ ba lần và ghi trung bình theo mét.
2. Đánh dấu lốp bằng phấn. Ra lệnh hai bánh cùng tốc độ trong hai giây và xác nhận cả hai dấu chạy về trước. Việc này chốt dấu $$v_L$$ và $$v_R$$ trong firmware.
3. Ra lệnh quay tại chỗ ở trên với PWM thấp (ánh xạ 0,08 m/s sang độ rộng xung mà chương 07 gọi là “tiến chậm”). Bánh trái phải quay lùi.
4. Tùy chọn trên sàn, chỗ trống, tốc độ chậm: chạy $$v = 0,2$$, $$\omega = 0,5$$ một phần tư vòng và so bán kính đo thước với 0,40 m đã nhân theo $$L$$ thật của bạn. Tính lại $$R = v/\omega$$ bằng số của bạn trước khi cho chạy.
5. Cất hàm và $$L$$ đã đo trong cùng file bạn sẽ import từ cầu nối chương 10.

**Ghi chú mong đợi**

```text
L_mean = 0.158 m
lệnh bằng nhau: cả hai bánh tiến
v=0, w>0: phải tiến, trái lùi
R dự đoán = 0.40 m, R đo = 0.45 m  (trượt, đừng "sửa" bằng hệ số ngẫu nhiên)
```

Sai bán kính khoảng 10 phần trăm trên thảm là trượt và miết, không phải công thức hỏng. Bánh trái ngược chiều là sai dấu.

**Khi hỏng thì thường vì**

| Bạn thấy | Nguyên nhân hay gặp |
| --- | --- |
| Robot cua nhầm phía | Dấu $$\omega$$, hoặc tuple trái/phải bị đảo |
| Lệnh đi thẳng lại thành vòng | Thang PWM một bánh mềm hơn, hoặc một lốp nhỏ hơn. Động học không giấu được việc đó; PID thì có thể |
| Bán kính bằng một nửa dự đoán | Bạn đo chiều ngang tấm, hoặc dùng đường kính làm $$L$$ |
| Cả hai bánh lùi khi cua trái | Bạn đặt $$v_L = v + \omega L/2$$ |
| Về sau tỉ lệ bản đồ vô nghĩa | $$L$$ hoặc $$r$$ đang là centimét trong công thức mét |

## Mua ở Việt Nam

Không có linh kiện mới. Thước dây 3 m ở quầy văn phòng phẩm là đủ (khoảng 15.000–40.000 đồng trên Shopee, từ khóa `thước dây 3m`). Lốp méo hoặc mút bị bẹp thì thay cả cặp để $$r$$ khớp: tìm `bánh xe robot cao su 65mm`, khoảng 20.000–60.000 đồng mỗi bánh. Mua hai bánh cùng lúc. Trộn hai đường kính là một lỗi động học giả.

## Bài tập

1. Khẩu độ của bạn là 0,20 m. Joystick xin $$v = 0$$, $$\omega = -0,8$$ rad/s. Tính $$v_L$$, $$v_R$$ và gọi tên cú cua. Gợi ý: bánh phải âm, bánh trái dương, cua phải (yaw âm).
2. Cả hai bánh 0,3 m/s. $$v$$ và $$\omega$$ là bao nhiêu? Gợi ý: $$v = 0,3$$, $$\omega = 0$$, không phụ thuộc $$L$$.
3. Vì sao không có cặp $$v_L, v_R$$ nào thỏa $$v_x = 0$$, $$v_y = 0,2$$, $$\omega = 0$$? Gợi ý: cả hai công thức chỉ tạo chuyển động dọc $$x$$ và quay. $$v_y$$ đồng nhất bằng 0.
4. Bạn đo $$L = 15,5$$ cm rồi gõ `0.155` ở một file và `15.5` ở cầu nối. Triệu chứng nào hiện ra ở $$R$$? Gợi ý: bán kính sai 100 lần, trông như “robot quay tại chỗ dù lệnh là gì.”
5. Hàm này đứng chỗ nào so với PID? Gợi ý: Twist → hàm này → hai setpoint m/s → hai vòng PID → hai PWM. Bỏ PID nghĩa là những số m/s chỉ là hy vọng.

## Đọc thêm

- [REP-103, đơn vị và quy ước hệ tọa độ](https://www.ros.org/reps/rep-0103.html).
- [REP-105](https://www.ros.org/reps/rep-0105.html) về `base_link`, hệ mà các phương trình này sống trong đó.
- [Modern Robotics, chương 13](https://hades.mech.northwestern.edu/index.php/Modern_Robotics) (bản mở) nếu bạn muốn chương robot bánh sau khi mô hình hai dòng bắt đầu thấy nhỏ.
- `geometry_msgs/Twist` trong [tài liệu message Jazzy](https://docs.ros.org/en/jazzy/p/geometry_msgs/msg/Twist.html): `linear.x` là $$v$$, `angular.z` là $$\omega$$, bốn trường còn lại gần 0 trên khung này.
