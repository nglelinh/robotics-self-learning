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

Đây là cửa ra của Chương 00. Dành 60–90 phút, chủ yếu kiểm bằng chứng từ bài 00-01 tới 00-06. Một dấu tick không có file, ảnh, hoặc dòng đã dán thì không tính. Chương 01 sẽ bảo bạn đo linh kiện thật. Đừng bắt đầu chương đó bằng cảm giác.

## Mục tiêu học

Bạn sẽ **rà** bàn lab bằng một thủ tục viết ra, từng mục một. Bạn sẽ **gắn** bằng chứng vào mỗi mục: một tổng trong `bom.csv`, tiếng bíp của đồng hồ trên ngắn đã biết, một cổng serial hoặc một kế hoạch rõ nếu board chưa tới, một câu lộ trình A hoặc B, ảnh cục sạc hoặc ghi chú chưa mua cell, và thẻ lên nguồn từ bài 00-03. Bạn sẽ **tách** dụng cụ thiếu làm Chương 01 không an toàn khỏi khung xe thiếu thì chưa sao. Bạn sẽ **dự đoán** dòng thiếu nào khiến bài điện đầu tiên mất an toàn. Bạn sẽ **liệt kê** chỉ những chỗ thiếu sẽ mua, dùng bài 00-05 làm giỏ chứ không lập giỏ mới.

## Cần có trước

Bạn cần sổ, câu lộ trình, thẻ lên nguồn, ảnh kiểm kê Sóng 1, và `bom.csv` mà bài 00-05 bảo bạn lập. Nếu một thứ bị bỏ, buổi rà ghi sự bỏ đó. Chưa cần robot chạy, ROS 2, hay mối hàn. Bạn cần sẵn sàng để một ô không được tick.

## Vì sao việc này dính tới Capstone

Capstone A dừng bánh khi lệnh im khoảng 300 ms. Hành vi đó cần một bàn phân biệt được mass với một điều ước. Topic ROS 2 sau này sẽ mô tả cùng robot đó. Chúng sẽ không sửa một buổi Chương 01 đo ohm trên ray đang sống, hay một cell lithium tới mà không có quyết định về cục sạc. Cửa này tìm, khi đồ còn trong túi, bằng chứng thiếu nào sẽ làm chương sau mất an toàn.

![Thứ tự trên thẻ lên nguồn là một mục buổi rà này phải thấy]({{ site.imgurl }}/generated/power_order.png)

Nếu không tìm thấy thẻ, đừng vẽ lại từ trí nhớ giữa buổi rà rồi gọi là thẻ cũ. Làm lại trang của bài 00-03 rồi chụp. Hình nhắc thứ tự: mass chung, logic, tín hiệu, nguồn motor cuối, bánh nhấc.

## Cái gì được tính là bằng chứng

Một dấu tick là lời khẳng định một hiện vật cụ thể tồn tại. Hiện vật phải là thứ bạn đưa được cho một bạn khác.

**Hóa đơn vật tư** tính khi `bom.csv` (hoặc cùng bảng trong sổ) có một tổng bạn tự viết, kèm ngày. Ảnh chụp trang chủ một shop không có tổng thì không phải tổng. Nếu bài 00-05 chưa xong, dòng này mở, và bạn làm xong bài đó trước khi giả vờ Chương 00 đã đóng.

**Đồng hồ** tính khi sổ nói hai que đã chạm nhau và đồng hồ kêu, hoặc khi sổ ghi sự thất bại ("không bíp; cầu chì hoặc pin"). Ảnh đồng hồ trong giỏ hàng không kêu. Nếu đồng hồ chưa tới, dòng vẫn mở. Việc thông mạch của Chương 01 bị chặn tới khi dòng đóng. Đó là kết quả đúng, không phải một lần thương lượng.

**Cáp USB** tính theo một trong hai cách. Một cổng serial hiện khi board được cắm, tên được dán vào sổ, và cổng mất khi bạn rút. Hoặc board chưa tới, và sổ có kế hoạch viết ra: chỉ USB, không nguồn motor, ghi cổng, rút. Cáp chỉ thắp LED thì chưa chứng minh dữ liệu. Viết `chưa chứng minh` thay vì tick dòng.

**Câu lộ trình** tính khi nó nêu lộ trình A hoặc B, MCU (ESP32 hoặc Pico 2), và sự từ chối mua LiDAR trước Capstone A. "Tôi thích robot" không phải lộ trình.

**Cục sạc** tính khi ảnh cho thấy nhãn bạn đọc được (Li-ion, 4,2 V, một cell), hoặc khi sổ nói `chưa mua cell`. Một cell trần không ghi chú là mục an toàn đang mở, không phải trung lập. Ảnh TP4056 đang kẹp qua đế 2S là bằng chứng của một lỗi, không phải một dấu tick.

**Thẻ lên nguồn** tính khi ảnh hoặc chính trang giấy cho thấy mass chung, logic USB, tín hiệu, VM cuối, bánh nhấc, dừng PWM 300 ms, và lệnh cấm điện áp motor cùng echo 5 V vào GPIO 3,3 V. Thẻ bắt đầu bằng pin thì trượt mục dù giấy có tồn tại.

**Không gian làm việc** từ bài 00-06 tính khi các thư mục tồn tại và nhật ký cài có phiên bản hoặc chữ `chưa cài`. Một `ros_ws/` trống với sự thành thật đó là đạt. Một `ros_ws/` đầy clone bạn không định giữ là đống bạn dọn trước khi tick.

## Thủ tục rà

Làm theo thứ tự. Đừng nhảy tới mục bạn biết mình đã đạt.

Mở sổ và thêm đề mục `Cửa ra Chương 00`. Chép bảy mục bằng chứng ở trên thành các dòng bạn sẽ đánh `đạt` hoặc `mở`.

Đọc `bom.csv` và viết tổng bằng đồng lên đề mục cửa ra, kèm ngày giá được chép. Nếu không thấy file, đánh `mở` và ngừng nhận bài mua sắm đã xong. Mở ảnh Sóng 1 từ bài 00-04 và đối với các dòng: đồng hồ, mỏ, giá, thiếc, kìm, breadboard, dây cắm, cáp dữ liệu, MCU, LED, nút. Mỗi dòng `có` hoặc `thiếu`. Khung xe và driver là Sóng 2. Vắng chúng không làm trượt Chương 00. Có chúng không tha cho một đồng hồ thiếu.

Làm lại bài bíp, dù tuần trước đã làm. Hai que chạm, đồng hồ ở thông mạch, mạch không có điện. Viết "bíp" hoặc chuyện thực sự xảy ra. Nếu bạn sắp đo ray USB đang nuôi bằng thang ohm vì bài bíp thất bại, dừng. Đó là lỗi mà quy tắc tồn tại để chặn.

Kiểm bằng chứng USB. Nếu board ở trên bàn, cắm không có pin motor, dán tên cổng, rồi rút. Nếu board không ở trên bàn, đọc kế hoạch đã viết và xác nhận nó cấm VM ở lần cắm đầu. Không kế hoạch và không cổng thì mục mở.

Đọc câu lộ trình thành tiếng. Xác nhận nó nhắc dừng 300 ms và nêu TB6612FNG chứ không phải L298N nếu driver đã có trong bảng. Nếu bảng nói L298N, phép sụt áp của bài mua sắm chưa được áp. Đánh dòng driver `mở` dù phần còn lại của câu nghe tự tin.

Nhìn bằng chứng cục sạc. Hoặc nhãn trên ảnh khớp một cell ở 4,2 V, hoặc ghi chú nói chưa mua cell. Nếu đế 2S và TP4056 cùng ảnh và đang nối, ngắt chúng trước khi rà tiếp, và đừng tick dòng.

Tìm thẻ lên nguồn. So với hình đầu bài này. Nếu VM không đứng cuối, viết lại thẻ. Chụp bản bạn sẽ thực sự làm theo.

Mở thư mục firmware và `ros_ws/README.md`. Xác nhận nhật ký cài khớp máy trước mặt. Đừng xóa thứ bạn còn cần, nhưng bỏ lời nhận Jazzy đã cài nếu máy là Windows.

**Khi cửa thành thật.** Đề mục cửa ra liệt kê đạt hoặc mở cho mọi mục. Tổng, tiếng bíp, cổng hoặc kế hoạch, câu lộ trình, quyết định cell, và thẻ, mỗi cái là một hiện vật thật. Mục mở nêu bài sẽ đóng nó: 00-04 cho thiếu giá, 00-05 cho thiếu tổng, 00-03 cho thiếu thẻ, 00-06 cho thiếu thư mục.

**Khi có người đang vội.** Mọi dòng đều đạt, và phần đính kèm duy nhất là "trông ổn". Đặt lại `mở` cho mọi dòng bạn không chỉ ra được trong một phút.

## Ví dụ làm sẵn

Ghi chú cửa ra của My, viết sau khi cô thực sự nhìn, như sau. Tổng `bom.csv` 1.620.000 ₫, giá ngày 23 tháng 9 năm 2026, file trong `notes/`. Đồng hồ: bíp trên ngắn đã biết, làm lại hôm nay. USB: board chưa tới; kế hoạch là "chỉ USB, không VM, dán cổng, rút; cáp trong ngăn kéo chưa chứng minh tới khi cổng đó hiện". Lộ trình: "A, ESP32, TB6612FNG, không LiDAR trước teleop bánh nhấc với dừng 300 ms. B trên máy Ubuntu lab sau Chương 07". Cell: `chưa mua`. Thẻ lên nguồn: đã chụp, VM cuối, có dòng bánh nhấc. Nhật ký cài: Arduino IDE chưa cài trên laptop, Jazzy chưa cài, Gazebo Harmonic chỉ được gọi tên.

Cô tick kế hoạch đã viết, không tick cáp đã chứng minh, và để `cáp chưa chứng minh` hiện. Chỗ thiếu: một cái giá (40000 ₫ trên snapshot 23 tháng 9 năm 2026) và dây cắm. Khung xe thiếu là Sóng 2 và không chặn Chương 01. Thiếu giá thì chặn việc hàn, nên mỏ nóng ở ngoài bàn. Đo và nhận diện linh kiện thì được bắt đầu.

Một bạn khác, Khoa, có tiếng bíp, có thẻ, có câu lộ trình, và cũng có ảnh TP4056 nối qua hai cell vì "giắc vừa". Dòng cục sạc của anh là `mở`, và ảnh là bằng chứng lỗi, không phải sự sẵn sàng. Anh ngắt module, viết mỗi cell sẽ được sạc riêng tới 4,2 V hoặc không sạc, rồi mới được xem lại dấu tick. `bom.csv` của anh không có tổng. Anh quay lại bài 00-05 trước khi gọi cửa là đạt. Một stack nhắn tin trên Ubuntu sẽ không bắt được cả hai sơ suất.

## Bài tập

Các câu này hỏi bạn tìm chỗ thiếu mất an toàn. Chúng nói về buổi rà của bạn, hoặc các buổi rà dưới đây, không phải nhắc lại chương.

1. Bài đo đầu của Chương 01 đòi thông mạch và điện áp một chiều. Mục mở nào trong danh sách cửa ra của bạn làm bài đó không thành thật hoặc không an toàn, và bằng chứng nào sẽ đóng nó?
2. Một bạn tick "cáp USB đã chứng minh" vì LED board sáng. Không có tên cổng. Vì sao dấu tick sai, và Chương 02 có thể hỏng thế nào nếu họ giữ dấu đó?
3. Thẻ lên nguồn bị thiếu, và bạn đó nói Chương 01 không có motor nên thẻ có thể chờ. Nêu một việc của Chương 01 (đo, hàn, hoặc một cell lithium đã ở trên kệ) mà thẻ lẽ ra phải ràng buộc.
4. `bom.csv` liệt kê L298N và một đế 2S, tổng để trống, và câu lộ trình nói "ROS trước". Sự thật nào trong ba cái đó làm một bài thử motor sau này mất an toàn dù bài điện trở Chương 01 vẫn ổn? Giải thích bằng sụt khoảng 2 V hoặc bằng quy tắc cục sạc.
5. Chưa mua cell, đồng hồ kêu, thẻ có, và `ros_ws/` trống trên Windows với sự thật đó đã được viết. Bạn này có được bắt đầu các bài nhận diện không cấp nguồn của Chương 01 không? Họ vẫn bị cấm làm gì?

<details>
<summary>Gợi ý đáp án</summary>

1. Dòng đồng hồ đang mở: không bíp trên ngắn đã biết nghĩa là mọi "0 Ω" hoặc "3,3 V" sau này không đáng tin, và người rồi đo dòng hoặc ohm bừa có thể ngắn một cổng. Đóng bằng một tiếng bíp, hai que chạm, viết vào sổ. Thiếu khung xe không gây hư kiểu này.
2. LED chỉ cho thấy điện đã tới. Cáp chỉ sạc không bao giờ hiện cổng serial, nên lần nạp Chương 02 thất bại theo kiểu trông như board hỏng. Dấu tick cần tên cổng hiện và mất theo phích, hoặc một kế hoạch chưa chứng minh viết rõ.
3. Hàn vẫn cần giá, kính, và thông gió. Cell trên kệ vẫn cần dòng "từng cell, 4,2 V, không qua 2S". Đo USB 5 V khi que đỏ nằm ở lỗ dòng là cùng họ tai nạn.
4. L298N sẽ rơi khoảng 2 V và khiến motor yếu trông như lỗi phần mềm, còn đế 2S cạnh một cục sạc không tên là cách TP4056 bị kẹp qua 8,4 V. "ROS trước" bỏ timeout lẽ ra phải đưa PWM về 0. Một trong ba cái là đủ để gọi bài thử motor mất an toàn. Tổng trống nghĩa là họ cũng không biết mình tưởng đã mua gì.
5. Được, cho nhận diện không cấp nguồn và cho thông mạch trên chi tiết không nối nguồn, miễn tiếng bíp là thật. Họ vẫn bị cấm hàn khi chưa có giá, cấm nối nguồn motor, cấm sạc lithium, và cấm coi `ros_ws/` trống là lý do bỏ bàn lab sau này.

</details>

## Đọc thêm

Cửa này không thêm một bài lý thuyết mới. Mở lại các trang này chỉ cho dòng vẫn còn mở.

- [Cách dùng đồng hồ](https://learn.sparkfun.com/tutorials/how-to-use-a-multimeter) — nếu bài bíp thất bại và bạn cần vạch cùng các lỗ được giải thích lại.
- [Mức logic](https://learn.sparkfun.com/tutorials/logic-levels) — nếu lệnh cấm 5 V trên thẻ là dòng bạn vừa viết lại.
- [Cài ROS 2 Jazzy](https://docs.ros.org/en/jazzy/Installation.html) — chỉ để xác nhận bạn không cài nó trên hệ điều hành sai. Một `ros_ws/` trống trên Windows là kết quả đúng của Chương 00.

## Mua ở Việt Nam

Mua các chỗ thiếu buổi rà đã viết, rồi dừng. Giỏ chính là [bài 00-05]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %}). Các trang dụng cụ dưới đây là snapshot Hshop ngày **23 tháng 9 năm 2026**. URL tìm kiếm là trang tìm kiếm.

| Nếu buổi rà nói thiếu cái này | Snapshot | Link |
| --- | ---: | --- |
| Không đồng hồ, hoặc đồng hồ không bíp và bạn thay | 285000 ₫ hoặc 185000 ₫ | [UT33D+](https://hshop.vn/dong-ho-van-nang-dien-tu-digital-multimeter-uni-t-ut33d-chinh-hang), [Wadfow WDM1501](https://hshop.vn/dong-ho-van-nang-ky-thuat-so-vom-wadfow-wdm1501-digital-multimeter-true-rms) |
| Không mỏ | 75000 ₫ | [Wadfow 60 W](https://hshop.vn/mo-han-60w-wadfow-wel3616-soldering-iron) |
| Không giá | 40000 ₫ | [giá](https://hshop.vn/de-gac-mo-han-tron-b-2-co-khay-roi) |
| Không thiếc 0,8 mm | 24000 ₫ | [dây Sn63](https://hshop.vn/thiec-han-sunchi-kp26-0-8mm-sn63-pb37-solder-wire) |
| Không kìm cắt | 35000 ₫ | [kìm 170](https://hshop.vn/kim-cat-day-dien-nho-170-cat-chan-linh-kien-dien-tu) |
| Không breadboard | 35000 ₫ | [board 830 điểm](https://hshop.vn/test-board-cammb-102) |

Một đồng hồ, không phải cả hai. Dây cắm và cáp dữ liệu, nếu đó là các dòng mở: [Shopee, cáp USB data](https://shopee.vn/search?keyword=c%C3%A1p%20usb%20data) và [Lazada, dây jumper](https://www.lazada.vn/catalog/?q=d%C3%A2y%20jumper). Kính nếu thẻ nói còn thiếu: [Shopee, kính bảo hộ](https://shopee.vn/search?keyword=k%C3%ADnh%20b%E1%BA%A3o%20h%E1%BB%99). [Thế Giới IC](https://www.thegioiic.com/) và [IC Đây Rồi](https://icdayroi.com/) là trang chủ cửa hàng, hữu ích khi bạn đứng tại quầy với danh sách thiếu trong tay. Đừng thêm LiDAR, Pi, hay oscilloscope để đóng Chương 00.
