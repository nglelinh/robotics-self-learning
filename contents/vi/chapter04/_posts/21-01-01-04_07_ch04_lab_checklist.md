---
layout: post
title: "Checklist lab chương 04"
chapter: "04"
order: 7
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter04
lesson_type: required
draft: false
---

Thời lượng: **50–70 phút**. Đây là cửa ký duyệt, không phải một cảm biến mới. Bạn qua khi `lab-notes.md` chứa bằng chứng bên dưới. Nhớ mang máng “lab coi như xong” không mở được Chương 05.

## Mục tiêu học

Bạn tự chấm sổ Chương 04 theo các mốc đạt hoặc trượt: một địa chỉ I2C kèm ảnh, $$N$$ của encoder từ một vòng bánh và số mét trên mỗi xung đi kèm, số IMU lúc để yên hoặc giấy hoãn có ngày, bảng đo khoảng cách hoặc dry-run 5,8 ms, và một câu camera có chứa 147 Mbit/s. Bạn dán một khối mà bạn cùng lớp kiểm được mà không phải hỏi bạn định nói gì. Bạn kể hai kiểu hỏng chính bạn gặp hoặc cố tình dựng, và bạn nhận ra một sổ đã điền kín mà vẫn trượt.

## Kiến thức cần có

Bài 04-01 đến 04-06 là phần việc đang được ký. Bạn cần `lab-notes.md`, phiếu nhận diện Bài 04-02, và các số các bài đó đã tính: $$N$$ và $$r = 0{,}0325~\mathrm{m}$$ nếu bạn dùng bánh ví dụ, bước lọc bổ trợ ra 9,889 độ, echo 5,8 ms là 99,5 cm, cầu chia 3,33 V, và ngân sách camera 147 Mbit/s. Chương 05 bắt đầu motor và cầu H. Chương đó giả định trang này đã thật, vì echo 5 V trên một GPIO vẫn là echo 5 V sau khi driver motor được nối cạnh nó.

## Vì sao bài này quan trọng với Capstone A và ROS

Firmware teleop Chương 07 ra lệnh hai bánh và dừng khi timeout hoặc khi có số đo khoảng cách. Số đo đó chỉ tốt bằng bảng bạn ký ở đây, và số đếm bánh tùy chọn trong nhật ký nghiệm thu chỉ tốt bằng $$N$$. ROS 2 sau này xuất đúng các đại lượng đó thành `sensor_msgs/Range`, `nav_msgs/Odometry`, rồi `sensor_msgs/Imu` và `sensor_msgs/Image`. $$N$$ bị nhân đôi thì odometry báo một nửa hành lang. Timeout cất thành 0 cm thì topic khoảng cách nói robot đang ở trong tường. Câu camera giữ Chương 11 là một kế hoạch, không phải một tải USB bất ngờ khoảng 147 Mbit/s.

![Phiếu nhận diện mà cửa này kiểm: bus, điện áp, và module nào được hoãn]({{ site.imgurl }}/generated/sensor_package_id.png)

## Khối dán vào `lab-notes.md`

Chép khối này, thay chỗ trống bằng bằng chứng của bạn, và xóa mọi dòng bạn không chống đỡ được. Để trống mà vẫn giữ dòng là trượt.

```
## Ky duyet chuong 04
Ngay:
I2C: dia chi thay = ____ ; file anh = ____
Encoder: N = ____ xung moi vong truc ra (ba lan: __, __, __)
         r = ____ m ; met moi xung = ____
         kenh dan khi tien: ____  (hoac "mot kenh, khong biet chieu")
IMU: |a| = ____ g ; truc luc de yen = ____ dau ____
     lech gyro deg/s = (__, __, __)
     HOAC giay hoan ngay ____ va da kiem buoc loc 9.889 deg
Do tam: 20 cm -> __ cm (sai __) ; 40 -> __ (sai __) ; 80 -> __ (sai __)
       HOAC dry-run: 5.8 ms -> 99.5 cm ; cau chia 5*(2/3) = 3.33 V
Camera: hoan den chuong 11 ; YUYV 640x480 30 fps xap xi 147 Mbit/s
Hong 1:
Hong 2:
```

## Đạt và trượt

**I2C.** Có ít nhất một địa chỉ (`0x68`, `0x69` hoặc `0x29` là các địa chỉ hay gặp) và một ảnh thấy module cùng dây. “Quét ổn, không lỗi”, không địa chỉ không ảnh, là trượt.

**Encoder.** $$N$$ là một vòng quay tay của trục ra, ba lần lệch nhau không quá một xung. Mét trên mỗi xung là $$2\pi r / N$$. Bánh ví dụ: $$r = 0{,}0325~\mathrm{m}$$, chu vi $$\approx 0{,}2042~\mathrm{m}$$, nên $$N = 20$$ nghĩa là $$0{,}01021~\mathrm{m}$$ mỗi xung. PPR của người bán là trượt khi bộ đếm in một số khác. Một kênh chỉ đạt nếu sổ nói không biết chiều từ chân đó.

**IMU.** Độ lớn lúc để yên gần 1 g, kèm trục, dấu, và độ lệch gyro theo độ/giây sau thang datasheet, hoặc giấy hoãn có ngày. Giấy hoãn vẫn phải có bước lọc bổ trợ ($$\theta$$ kế tiếp $$= 9{,}889~\mathrm{deg}$$) và $$0{,}5~\mathrm{deg/s} \times 60~\mathrm{s} = 30~\mathrm{deg}$$. In LSB thô như độ thì cả hai đường đều trượt.

**Đo tầm.** Bảng 20 / 40 / 80 cm có sai số có dấu. Ở 40 cm, lệch trong 5 cm trên bìa phẳng là đạt sạch; lệch lớn hơn chỉ đạt khi sổ nêu nguyên nhân. Thiếu một mốc là trượt. Dry-run vì hàng chưa về chỉ đạt khi trang có $$5{,}8~\mathrm{ms} \rightarrow 99{,}5~\mathrm{cm}$$ và $$5 \times 2/3 \approx 3{,}33~\mathrm{V}$$. Câu “chạy tới 4 m” không phải trang đó.

**Camera.** Một câu: camera đợi Chương 11, và luồng YUYV 640×480 ở 30 fps khoảng 147 Mbit/s. Thiếu số là trượt dòng. Mua ESP32-CAM tuần này không làm dòng đó đạt.

**Hai lỗi.** Mỗi lỗi nêu bạn thấy gì và bạn đã sửa hoặc sẽ sửa gì. “Không có, mọi thứ chạy” trượt cửa dù các dòng khác hoàn hảo. Giả lập đảo A/B trong sổ, hoặc bia vải không có echo, được tính nếu bạn ghi số.

## Một sổ trông xong mà vẫn trượt

Đây là kiểu trang bị trả lại. Người viết không lười. Người viết đo nhầm thứ, và Chương 05 sẽ thừa kế nó.

```
# lab-notes.md — vi du KHONG dat
Ngay: 12/9

I2C: quet on, khong loi. (khong dia chi, khong anh)

Encoder: nguoi ban ghi 40 PPR nen N = 40.
Quay tay mot vong thay khoang 20 nhay nhung minh giu 40.
r = 0.0325 m
met moi xung = 0.2042/40 = 0.0051 m

IMU: de phang, az = 16384 do. Gyro 70.

Do tam: ECHO vao GPIO18, khong dien tro, VCC 5 V.
So nhay. Minh se lay trung binh trong code.
Chua lam moc 20 cm. Moc 40 cm doi khi ra 80.

Camera: dang dat ESP32-CAM de Chuong 07 nhin thay hanh lang.

Loi: khong co.
```

Dòng I2C không địa chỉ, không ảnh. Encoder thấy khoảng 20 xung mà ghi $$N = 40$$, nên mét mỗi xung bằng một nửa của $$0{,}01021~\mathrm{m}$$: 140 xung thành $$0{,}71~\mathrm{m}$$ trong sổ thay vì $$1{,}43~\mathrm{m}$$. Dòng IMU in LSB như độ. Ở $$\pm 2~\mathrm{g}$$, 16384 là $$+1~\mathrm{g}$$; gyro thô 70 ở $$\pm 250~\mathrm{deg/s}$$ là $$70/131 \approx 0{,}53~\mathrm{deg/s}$$. ECHO 5 V không cầu chia nằm ngoài định mức GPIO; cách sửa là 1 kΩ / 2 kΩ, khoảng 3,33 V, rồi một bảng 20/40/80 thật. Dòng camera không nói 147 Mbit/s, và “không có lỗi” che đúng $$N$$ bị nhân đôi cùng chân echo trần đang nằm trên trang.

## Sửa gì trước Chương 05

Chương 05 thêm dòng motor và một driver có thể làm vi điều khiển reset. Đừng bắt đầu chương đó trên một GPIO đã thấy 5 V, hoặc với một $$N$$ bạn biết là đã nhân đôi. Trước khi ký: gắn cầu chia lên ECHO (1 kΩ / 2 kΩ, khoảng 3,33 V) hoặc tháo ECHO; viết lại $$N$$ từ số quay tay và tính lại mét mỗi xung; viết lại dòng IMU theo g và độ/giây, hoặc nộp giấy hoãn có ngày với 9,889 độ và 30 độ trôi; xong bảng đo tầm hoặc phép dry-run; thay câu camera và để ESP32-CAM trong túi nếu nó về; điền hai dòng lỗi từ việc bạn thực sự đã gỡ. Chương 05 sẽ không hỏi lại điện áp echo.

## Lab

### An toàn

Bạn đang sửa sổ. Nếu bật nguồn để chụp lại, chỉ USB, bánh trên không, ECHO qua cầu chia. Mô tả lỗi 5 V bằng chữ. Đừng tái hiện nó trên GPIO đang sống.

### BOM

| Món | Vai trò |
|------|---------|
| `lab-notes.md` | Tài liệu bạn ký |
| Ảnh phiếu Bài 04-02 | Dòng địa chỉ |
| Sổ Bài 04-05 | Bảng sai số hoặc dry-run |
| Máy tính | Tính lại $$2\pi r/N$$ và echo 5,8 ms trên chính trang này |

### Các bước

1. Dán khối ký duyệt vào `lab-notes.md` và điền từ bài bạn đã đo từng dòng. Module chưa về thì dùng giấy hoãn hoặc dry-run có ngày, không để trống.
2. Trên cùng trang, tính lại mét mỗi xung và $$343 \times 0{,}0058 / 2 = 0{,}995~\mathrm{m}$$.
3. Đặt trang của bạn cạnh sổ mẫu bị trượt. Câu nào na ná câu đó thì viết lại trước khi tick.
4. Viết hai lỗi ở ngôi thứ nhất, mỗi lỗi có một con số. Dừng. Đi dây motor đợi đến khi mọi dòng đạt.

### Kết quả mong đợi

Bạn cùng lớp tìm thấy một địa chỉ, một $$N$$, một véctơ g hoặc giấy hoãn, một bảng tầm hoặc 99,5 cm, câu 147 Mbit/s, và hai lỗi, mà không phải hỏi bạn.

### Lỗi thường gặp

| Bạn thấy | Thường là |
|----------|-----------|
| Ô nào cũng ghi “có” | Cửa này cần một số, một địa chỉ, hoặc một tên file |
| $$N$$ chép từ tiêu đề sản phẩm | Số quay tay không được phép thắng |
| Giấy hoãn không có 9,889 và không có 30 độ | Dòng IMU trống |
| Dry-run không có 3,33 V | Cầu chia bị bỏ luôn trên giấy |
| Câu camera không có tốc độ bit | Dòng đó trượt |

## Mua ở Việt Nam / Where to buy in Vietnam

Chốt chương bằng những món cửa ký duyệt vẫn còn thiếu. Bỏ camera. Giá thay đổi.

| Món | Từ khóa | Khoảng giá (VND) | Thay thế |
|------|---------|------------------|----------|
| HC-SR04 | `HC-SR04` | 15.000–40.000 | [Trang Hshop](https://hshop.vn/cam-bien-sieu-am-srf04), thường khoảng 20.000 |
| VL53L0X, tùy chọn | `VL53L0X` | 35.000–90.000 | [Hshop VL53L0X](https://hshop.vn/cam-bien-khoang-cach-tof-laser-radar-vl53l0x). Chỉ siêu âm vẫn qua cửa. |
| MPU-6050 GY-521 | `MPU6050` | 35.000–90.000 | [Hshop GY-521](https://hshop.vn/cam-bien-6-dof-bac-tu-do-gy-521-mpu6050), thường khoảng 85.000. MPU6500 nếu thư viện khớp. |
| Động cơ TT có encoder, một cặp | `động cơ TT encoder` | 40.000–90.000 một cái | Đo $$N$$; đừng tin tiêu đề |

- [Hshop: HC-SR04](https://hshop.vn/search?q=HC-SR04)
- [Shopee: MPU6050](https://shopee.vn/search?keyword=MPU6050%20GY-521)
- [Lazada: động cơ TT encoder](https://www.lazada.vn/catalog/?q=dong%20co%20TT%20encoder)
- [Thế Giới IC: VL53L0X](https://www.thegioiic.com/search?q=VL53L0X)

## Bài tập

Dùng sổ trượt và các số của bài. Trả lời ngắn.

1. Sổ trượt đặt $$N = 40$$ với $$r = 0{,}0325~\mathrm{m}$$ sau khi quay tay thấy khoảng 20 xung. Họ viết bao nhiêu mét mỗi xung, đáng lẽ phải viết bao nhiêu, và 140 xung là bao xa trong mỗi câu chuyện?
2. ECHO cắm GPIO, không cầu chia. Lúc echo cao, chân chịu bao nhiêu vôn, hai điện trở nào sửa được, và $$V_{\mathrm{pin}}$$ bằng bao nhiêu?
3. Giấy hoãn IMU chỉ nói “module để sau”. Có đạt không? Hai kết quả nào phải nằm trên dòng có ngày đó?
4. Trang dry-run có “5,8 ms → 99,5 cm” và không nhắc cầu chia. Đạt hay trượt, và thiếu điện áp nào?
5. Câu camera nào đạt, và câu nào trong sổ mẫu làm dòng đó trượt?

### Gợi ý đáp án

1. Họ viết $$0{,}0051~\mathrm{m}$$ mỗi xung; số quay tay $$N = 20$$ cho $$0{,}01021~\mathrm{m}$$. Một trăm bốn mươi xung là $$0{,}71~\mathrm{m}$$ trong sổ của họ và $$1{,}43~\mathrm{m}$$ sau khi sửa. 2. 5 V; 1 kΩ từ ECHO tới chân và 2 kΩ xuống mass; $$\approx 3{,}33~\mathrm{V}$$. 3. Trượt. Giấy hoãn cần kết quả lọc $$9{,}889~\mathrm{deg}$$ và độ trôi $$0{,}5 \times 60 = 30~\mathrm{deg}$$. 4. Trượt. Số thiếu là $$3{,}33~\mathrm{V}$$ từ $$5 \times 2/3$$. 5. Câu đạt hoãn camera đến Chương 11 và có khoảng 147 Mbit/s. “Đang đặt ESP32-CAM để Chương 07 nhìn” là trượt.

## Đọc thêm

- [Datasheet HC-SR04 (bản SparkFun)](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf) — vì sao ECHO là xung 5 V.
- [Datasheet MPU-6050](https://invensense.tdk.com/wp-content/uploads/2015/02/MPU-6000-Datasheet1.pdf) — thang biến 16384 thành 1 g.
- [`sensor_msgs/Range`](https://docs.ros.org/en/humble/p/sensor_msgs/msg/Range.html) và [`nav_msgs/Odometry`](https://docs.ros.org/en/humble/p/nav_msgs/msg/Odometry.html) — hai message mà cửa ký duyệt này đang giữ.
- [I2C của Espressif](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/peripherals/i2c.html) — lần quét mà bức ảnh phải khớp.
