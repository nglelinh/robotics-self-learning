---
layout: post
title: "Checklist lab chương 00: bàn đã sẵn sàng"
chapter: "00"
order: 7
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter00
lesson_type: required
draft: false
---

Đây là bài kiểm tra đầu ra của Chương 00. Hãy dành 60–90 phút để rà soát toàn bộ bằng chứng bạn đã tạo từ bài 00-01 đến 00-06. Một dấu đánh dấu hoàn thành nhưng không có tệp, ảnh chụp hay dòng log kèm theo sẽ không được tính. Chương 01 sẽ bước vào đo đạc linh kiện thực tế, nên bạn cần đảm bảo mọi điều kiện an toàn và dụng cụ đều đã được kiểm chứng rõ ràng.

## Mục tiêu học

Sau bài học này, bạn sẽ **rà soát** bàn lab theo một quy trình văn bản từng bước và **gắn** bằng chứng cụ thể cho từng hạng mục: tổng ngân sách trong `bom.csv`, tiếng bíp thông mạch của đồng hồ trên mối nối đã biết, tên cổng serial thực tế (hoặc kế hoạch kiểm tra rõ ràng nếu mạch chưa về), phát biểu Lộ trình A hoặc B, ảnh nhãn bộ sạc (hoặc ghi chú chưa mua pin), và thẻ quy trình cấp nguồn từ bài 00-03. Bạn cũng sẽ **phân biệt** được những dụng cụ thiếu gây mất an toàn cho Chương 01 với những món Đợt 2 chưa cần gấp như khung xe, **nhận diện** mục thiếu nào khiến bài đo điện đầu tiên trở nên rủi ro, và **lập danh sách** chỉ gồm các món còn thiếu dựa trên bài 00-05 thay vì dựng thêm giỏ hàng mới.

## Cần có trước

Bạn cần chuẩn bị đầy đủ sổ lab, câu lộ trình, thẻ quy trình cấp nguồn, ảnh kiểm kê Đợt 1 và tệp `bom.csv` từ bài 00-05. Nếu còn hạng mục nào bỏ dở, buổi kiểm tra sẽ ghi nhận trung thực tình trạng đó. Lúc này vẫn chưa cần robot chạy, chưa cần ROS 2 hay mối hàn nào; điều quan trọng nhất là sẵn sàng để trống những ô chưa thực sự đạt yêu cầu.

## Vì sao bài này gắn liền với Capstone

Capstone A yêu cầu dừng bánh xe khi mất lệnh quá khoảng 300 ms — hành vi này chỉ tin cậy trên một bàn làm việc mà bạn phân biệt rõ điểm mass chung với các phỏng đoán cảm tính. Tầng ROS 2 về sau cũng không thể khắc phục hậu quả của việc đo ohm trên mạch đang cấp điện ở Chương 01, hay việc nhận cell lithium mà chưa kiểm tra bộ sạc. Buổi rà soát này giúp phát hiện sớm các lỗ hổng an toàn ngay khi linh kiện còn đang trong túi.

![Thứ tự trên thẻ lên nguồn là một mục buổi rà này phải thấy]({{ site.imgurl }}/generated/power_order.png)

Nếu làm thất lạc thẻ quy trình, đừng tự vẽ lại từ trí nhớ giữa buổi kiểm tra rồi coi như thẻ cũ; hãy mở lại bài 00-03, viết lại cẩn thận và chụp ảnh lưu vào sổ. Thứ tự bắt buộc luôn là: mass chung, nguồn logic, tín hiệu điều khiển, và nguồn động cơ VM sau cùng khi bánh xe đã nhấc khỏi bàn.

## Tiêu chuẩn nào được tính là bằng chứng

Mỗi dấu tick chỉ hợp lệ khi đi kèm một bằng chứng cụ thể mà người khác có thể kiểm tra trực tiếp:

- **Bảng vật tư (`bom.csv`):** đạt khi tệp `bom.csv` (hoặc bảng tương đương trong sổ) có con số tổng chi phí tự tính kèm ngày khảo sát giá. Ảnh chụp trang chủ một cửa hàng không được tính là bảng tổng hợp. Nếu bài 00-05 chưa xong, hạng mục này vẫn ở trạng thái `mở`.
- **Đồng hồ vạn năng:** đạt khi sổ ghi nhận kết quả chạm hai que đo có tiếng bíp thông mạch (hoặc ghi rõ lỗi thực tế như `không bíp; cần kiểm tra cầu chì hoặc pin`). Ảnh đồng hồ trong giỏ hàng không chứng minh nó hoạt động. Nếu chưa có đồng hồ, hạng mục này vẫn `mở` và các bài đo thông mạch Chương 01 phải chờ.
- **Cáp USB truyền dữ liệu:** đạt theo một trong hai cách: đã cắm mạch thấy tên cổng serial xuất hiện (dán vào sổ) và biến mất khi rút; hoặc nếu mạch chưa giao tới, sổ đã có kế hoạch rõ ràng: "chỉ cắm USB, không nối VM, ghi nhận tên cổng rồi rút". Cáp chỉ làm sáng đèn nguồn trên mạch chưa đủ chứng minh khả năng truyền dữ liệu — hãy ghi `chưa chứng minh` thay vì đánh dấu đạt.
- **Câu lộ trình:** đạt khi nêu rõ Lộ trình A hoặc B, loại vi điều khiển (ESP32 hoặc Pico 2) và cam kết không mua LiDAR trước khi đạt Capstone A. Một câu chung chung kiểu "tôi muốn học robot" không đạt yêu cầu.
- **Bộ sạc pin:** đạt khi có ảnh chụp đọc rõ nhãn thông số (Li-ion, 4,2 V, sạc từng cell), hoặc sổ ghi rõ `chưa mua cell`. Có cell pin trần nhưng không có ghi chú là một rủi ro an toàn đang mở; ảnh TP4056 đang kẹp lên đế 2S là bằng chứng của một lỗi sai, không phải điều kiện đạt.
- **Thẻ quy trình cấp nguồn:** đạt khi ảnh chụp hoặc bản giấy thể hiện đủ thứ tự: mass chung, nguồn logic USB, tín hiệu, nguồn VM cuối cùng, nhấc bánh khỏi bàn, quy tắc dừng PWM 300 ms, và lệnh cấm đưa nguồn động cơ hay echo 5 V vào GPIO 3,3 V. Thẻ viết sai thứ tự (đặt pin lên đầu) sẽ không đạt dù đã viết ra giấy.
- **Không gian làm việc:** đạt khi các thư mục từ bài 00-06 đã tồn tại đầy đủ và nhật ký cài đặt ghi rõ số phiên bản hoặc trạng thái `chưa cài`. Một thư mục `ros_ws/` trống kèm lý do trung thực là đạt; ngược lại, thư mục chứa nhiều mã nguồn tải về chưa dùng cần được dọn gọn trước khi đánh dấu hoàn thành.

## Quy trình rà soát từng bước

Hãy thực hiện lần lượt theo đúng thứ tự dưới đây, không bỏ qua các mục bạn nghĩ mình đã làm tốt:

1. Mở sổ lab, tạo mục `Cửa ra Chương 00` và liệt kê đủ 7 hạng mục bằng chứng trên để đánh dấu trạng thái `đạt` hoặc `mở`.
2. Kiểm tra `bom.csv`, ghi lại tổng chi phí bằng VND và ngày khảo sát giá; nếu chưa có tệp thì đánh `mở`. Mở ảnh kiểm kê Đợt 1 từ bài 00-04 và đối chiếu từng món: đồng hồ, mỏ hàn, giá đỡ, thiếc hàn, kìm cắt, breadboard, dây cắm, cáp dữ liệu, vi điều khiển, LED và nút nhấn (ghi `có` hoặc `thiếu`). Khung xe và mạch lái thuộc Đợt 2 nên thiếu chúng không làm trượt Chương 00, nhưng có sẵn chúng cũng không bù đắp được việc thiếu đồng hồ.
3. Kiểm tra lại tiếng bíp thông mạch của đồng hồ ngay cả khi tuần trước bạn đã thử: đặt thang thông mạch trên thiết bị không cấp điện, chạm hai que đo vào nhau và ghi nhận kết quả. Nếu tiếng bíp thất bại, tuyệt đối không chuyển sang đo ohm trên cổng USB đang có điện.
4. Kiểm tra bằng chứng cáp USB: nếu đã có mạch trên bàn, cắm cáp (không nối pin động cơ), dán tên cổng serial vào sổ rồi rút ra. Nếu chưa có mạch, đọc lại kế hoạch đã viết để chắc chắn có điều khoản cấm nối VM ở lần cắm đầu. Thiếu cả tên cổng lẫn kế hoạch thì đánh `mở`.
5. Đọc lại câu lộ trình để xác nhận có quy tắc dừng 300 ms và chọn TB6612FNG (không phải L298N nếu bảng đã có dòng mạch lái). Nếu bảng vẫn để L298N, hãy đánh `mở` dòng mạch lái vì quy tắc sụt áp ở bài 00-05 chưa được áp dụng.
6. Kiểm tra bằng chứng bộ sạc: nhãn trên ảnh phải khớp chuẩn sạc từng cell 4,2 V, hoặc ghi chú xác nhận `chưa mua cell`. Nếu thấy TP4056 đang nối với đế 2S, hãy ngắt kết nối ngay và giữ mục này ở trạng thái `mở`.
7. Đối chiếu thẻ quy trình cấp nguồn với hình minh họa đầu bài; nếu nguồn VM không nằm ở bước cuối cùng, hãy viết lại và chụp ảnh bản mới.
8. Mở thư mục `firmware/` và `ros_ws/README.md` để xác nhận nhật ký cài đặt khớp với chiếc máy tính trước mặt; không ghi đã cài Jazzy nếu đang dùng Windows.

**Dấu hiệu buổi kiểm tra đạt chuẩn:** Mọi hạng mục đều được đánh `đạt` hoặc `mở` dựa trên bằng chứng thực tế. Với mỗi mục còn `mở`, bạn ghi rõ bài học cần quay lại để hoàn thiện (bài 00-04 nếu thiếu giá đỡ mỏ hàn, 00-05 nếu thiếu tổng BOM, 00-03 nếu thiếu thẻ cấp nguồn, 00-06 nếu thiếu cây thư mục).

**Dấu hiệu làm vội:** Đánh dấu `đạt` cho tất cả các dòng nhưng chỉ kèm nhận xét "trông ổn". Với bất kỳ mục nào không tìm thấy bằng chứng trong vòng một phút, hãy chuyển ngay về trạng thái `mở`.

## Ví dụ làm sẵn

Ghi chú kiểm tra đầu ra của My sau khi đối chiếu thực tế như sau: tổng `bom.csv` là 1.620.000 ₫ (giá ngày 23 tháng 9 năm 2026, lưu trong `notes/`); đồng hồ kêu bíp rõ khi chập que (đã thử lại hôm nay); cáp USB ghi nhận mạch chưa về kèm kế hoạch "chỉ cắm USB, không nối VM, ghi tên cổng rồi rút; cáp hiện có ở trạng thái chưa chứng minh cho tới khi hiện cổng"; câu lộ trình là "Lộ trình A, ESP32, TB6612FNG, không mua LiDAR trước khi đạt teleop nhấc bánh có dừng 300 ms; Lộ trình B trên máy Ubuntu phòng lab sau Chương 07"; pin ghi `chưa mua`; thẻ cấp nguồn đã chụp ảnh đầy đủ bước VM cuối và nhấc bánh; nhật ký cài đặt ghi rõ chưa cài Arduino IDE trên laptop, chưa cài Jazzy và chỉ ghi tên Gazebo Harmonic.

My chỉ đánh dấu đạt cho kế hoạch USB chứ không đánh dấu đạt cho cáp dữ liệu, giữ nguyên dòng `cáp chưa chứng minh`. Những món còn thiếu của cô là giá đỡ mỏ hàn (40.000 ₫ theo giá ngày 23 tháng 9 năm 2026) và dây cắm. Khung xe thuộc Đợt 2 nên chưa chặn tiến độ Chương 01; thiếu giá đỡ chỉ tạm chặn phần thực hành hàn (không bật mỏ hàn), còn các bài đo và nhận diện linh kiện vẫn có thể bắt đầu bình thường.

Trong khi đó, Khoa có đủ tiếng bíp đồng hồ, thẻ quy trình và câu lộ trình, nhưng ảnh chụp lại cho thấy mạch TP4056 đang kẹp qua đế hai cell pin vì "thấy vừa giắc". Mục bộ sạc của anh bị đánh `mở` vì bức ảnh là bằng chứng lỗi an toàn. Anh phải ngắt kết nối ngay, viết cam kết chỉ sạc riêng từng cell tới 4,2 V rồi mới được rà soát lại. Ngoài ra, tệp `bom.csv` của Khoa chưa có dòng tổng, nên anh cần quay lại bài 00-05 hoàn thiện trước khi chốt Chương 00.

## Video tham khảo

- **Xem trước:** [EEVblog 1636 - Ultimate Multimeter Beginners Guide!](https://www.youtube.com/watch?v=52w3xeXrMU8) — EEVblog, tiếng Anh. Ôn lại cách đo điện áp và điện trở trên đồng hồ vạn năng trước khi xác nhận bàn lab đã sẵn sàng.

## Bài tập

Các tình huống dưới đây yêu cầu bạn chỉ ra thiếu sót gây mất an toàn trong buổi rà soát:

1. Bài đo đầu tiên của Chương 01 sử dụng thang thông mạch và điện áp một chiều. Nếu mục nào trong danh sách đầu ra còn `mở` sẽ khiến bài đo đó thiếu tin cậy hoặc mất an toàn, và bằng chứng nào giúp đóng mục đó?
2. Một sinh viên đánh dấu "cáp USB đã chứng minh" chỉ vì thấy đèn LED nguồn trên mạch sáng, mà không có tên cổng serial. Dấu tick này sai ở đâu, và sẽ gây ra rắc rối gì khi sang Chương 02?
3. Một bạn chưa viết thẻ quy trình cấp nguồn với lý do "Chương 01 chưa dùng động cơ nên để sau". Hãy nêu ít nhất một hoạt động ngay trong Chương 01 (đo đạc, hàn hoặc bảo quản cell lithium đang có sẵn) vẫn chịu sự ràng buộc trực tiếp của tấm thẻ này.
4. Tệp `bom.csv` liệt kê L298N cùng đế pin 2S, bỏ trống dòng tổng, và câu lộ trình viết "học ROS trước". Hãy phân tích vì sao các yếu tố này làm mất an toàn hoặc gây sai lệch cho bài thử động cơ về sau (dựa trên mức sụt áp ~2 V và quy tắc sạc pin).
5. Một sinh viên chưa mua pin, đã có tiếng bíp đồng hồ, đủ thẻ cấp nguồn, và giữ `ros_ws/` trống trên Windows kèm lý do rõ ràng. Bạn này đã được phép bắt đầu các bài nhận diện linh kiện không cấp nguồn của Chương 01 chưa, và vẫn bị cấm làm những gì?

<details>
<summary>Gợi ý đáp án</summary>

1. Nếu mục đồng hồ vạn năng còn `mở` (chưa có tiếng bíp trên mối nối ngắn đã biết), mọi số đo "0 Ω" hay "3,3 V" về sau đều không đáng tin cậy, thậm chí dễ dẫn đến cắm nhầm lỗ đo dòng gây ngắn mạch nguồn. Cần đóng mục này bằng kết quả chạm hai que kêu bíp ghi rõ trong sổ. Thiếu khung xe không gây rủi ro này.
2. Đèn LED sáng chỉ chứng tỏ cáp có cấp nguồn 5 V. Cáp chỉ sạc sẽ không bao giờ tạo cổng serial, khiến buổi nạp firmware Chương 02 thất bại theo cách rất dễ nhầm thành lỗi hỏng mạch. Bằng chứng hợp lệ phải là tên cổng xuất hiện/biến mất theo thao tác cắm rút, hoặc một kế hoạch kiểm tra ghi rõ `chưa chứng minh`.
3. Thực hành hàn ở Chương 01 vẫn bắt buộc có giá đỡ, kính bảo hộ và thông gió; nếu đã có cell lithium trên kệ vẫn phải tuân thủ quy tắc sạc từng cell 4,2 V và không kẹp TP4056 qua đế 2S; ngoài ra việc đo nguồn USB 5 V khi quên que đỏ ở lỗ đo dòng cũng là tai nạn cùng nhóm.
4. L298N gây sụt khoảng 2 V khiến động cơ yếu và dễ nhầm sang lỗi phần mềm; đế 2S không đi kèm quy chuẩn sạc rõ ràng dễ dẫn đến kẹp TP4056 vào bộ pin 8,4 V; còn "học ROS trước" bỏ qua lớp timeout ngắt PWM 300 ms. Bỏ trống dòng tổng cũng cho thấy chưa kiểm soát được cấu hình đã đặt mua.
5. Được phép bắt đầu các bài nhận diện linh kiện không cấp nguồn và đo thông mạch trên mạch đã ngắt điện. Tuy nhiên, bạn này vẫn không được hàn khi chưa có giá đỡ, không được cấp nguồn động cơ, không được sạc pin lithium khi chưa kiểm tra bộ sạc, và không được lấy việc `ros_ws/` trống làm lý do trì hoãn thực hành phần cứng.

</details>

## Đọc thêm

Bài kiểm tra đầu ra không bổ sung lý thuyết mới; chỉ mở lại các tài liệu sau cho những hạng mục đang ở trạng thái `mở`:

- [Cách dùng đồng hồ](https://learn.sparkfun.com/tutorials/how-to-use-a-multimeter) — xem lại nếu phép thử thông mạch không kêu và cần đối chiếu vị trí núm vặn, lỗ cắm que đo.
- [Mức logic](https://learn.sparkfun.com/tutorials/logic-levels) — xem lại nếu bạn vừa phải bổ sung lệnh cấm đưa mức 5 V vào chân 3,3 V trên thẻ quy trình.
- [Cài ROS 2 Jazzy](https://docs.ros.org/en/jazzy/Installation.html) — chỉ dùng để đối chiếu yêu cầu hệ điều hành Ubuntu 24.04; giữ `ros_ws/` trống trên Windows là kết quả đúng của Chương 00.

## Mua ở Việt Nam

Chỉ mua bổ sung những món còn thiếu từ buổi rà soát, không mua dư. Danh sách vật tư chính vẫn nằm tại [bài 00-05]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %}). Bảng giá dụng cụ dưới đây được ghi nhận từ Hshop ngày **23 tháng 9 năm 2026**:

| Hạng mục còn thiếu theo buổi rà soát | Giá tham khảo | Đường dẫn |
| --- | ---: | --- |
| Chưa có đồng hồ (hoặc đồng hồ không bíp cần thay mới) | 285.000 ₫ hoặc 185.000 ₫ | [UT33D+](https://hshop.vn/dong-ho-van-nang-dien-tu-digital-multimeter-uni-t-ut33d-chinh-hang), [Wadfow WDM1501](https://hshop.vn/dong-ho-van-nang-ky-thuat-so-vom-wadfow-wdm1501-digital-multimeter-true-rms) |
| Thiếu mỏ hàn | 75.000 ₫ | [Wadfow 60 W](https://hshop.vn/mo-han-60w-wadfow-wel3616-soldering-iron) |
| Thiếu giá đỡ mỏ hàn | 40.000 ₫ | [giá đỡ](https://hshop.vn/de-gac-mo-han-tron-b-2-co-khay-roi) |
| Thiếu thiếc hàn 0,8 mm | 24.000 ₫ | [dây Sn63](https://hshop.vn/thiec-han-sunchi-kp26-0-8mm-sn63-pb37-solder-wire) |
| Thiếu kìm cắt chân | 35.000 ₫ | [kìm 170](https://hshop.vn/kim-cat-day-dien-nho-170-cat-chan-linh-kien-dien-tu) |
| Thiếu breadboard | 35.000 ₫ | [board 830 lỗ](https://hshop.vn/test-board-cammb-102) |

Chỉ cần chọn một mẫu đồng hồ vạn năng. Nếu thiếu dây cắm, cáp USB truyền dữ liệu hoặc kính bảo hộ, bạn có thể tìm qua các trang tìm kiếm: [Shopee, cáp USB data](https://shopee.vn/search?keyword=c%C3%A1p%20usb%20data), [Lazada, dây jumper](https://www.lazada.vn/catalog/?q=d%C3%A2y%20jumper) và [Shopee, kính bảo hộ](https://shopee.vn/search?keyword=k%C3%ADnh%20b%E1%BA%A3o%20h%E1%BB%99). Ngoài ra, [Thế Giới IC](https://www.thegioiic.com/) và [IC Đây Rồi](https://icdayroi.com/) là hai địa chỉ cửa hàng linh kiện thuận tiện nếu bạn đến mua trực tiếp theo danh sách thiếu. Không cần mua thêm LiDAR, Raspberry Pi hay máy hiện sóng để hoàn thành Chương 00.
