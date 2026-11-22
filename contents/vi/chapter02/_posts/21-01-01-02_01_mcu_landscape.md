---
layout: post
title: "Chọn vi điều khiển cho robot nhỏ"
chapter: "02"
order: 1
owner: "Nguyen Le Linh"
lang: vi
categories: [chapter02]
lesson_type: required
draft: false
---

## Mục tiêu

Sau bài này, bạn có thể so sánh ba lựa chọn thực tế cho một robot vi sai cỡ nhỏ: bo mạch ESP32 có cổng USB, Raspberry Pi Pico (hoặc Pico 2), và bo mạch họ Arduino Uno. Bạn nắm rõ mức logic, khả năng kết nối không dây tích hợp và ngôn ngữ lập trình buổi đầu của từng loại. Khi cần điều khiển xe bằng điện thoại về sau, bạn biết chọn ESP32 NodeMCU-32S, đồng thời phân biệt được module trần với các bản Pico không có Wi-Fi. Bạn cũng lập được trình tự khởi chạy bo mạch từng bước để không nhầm lỗi sụt nguồn với lỗi ngẫu nhiên trong chương trình, biết tính ngưỡng thực hành cho mức cao 3,3 V và loại bỏ tín hiệu 5 V khỏi các chân GPIO.

## Cần gì trước khi học

Bạn chỉ cần biết chỉnh đồng hồ vạn năng sang thang đo điện áp một chiều và hiểu GPIO là chân mà vi điều khiển có thể xuất hoặc đọc tín hiệu. Kiến thức về điện trở nối tiếp trước LED ở chương 01 là đủ; bạn chưa cần kinh nghiệm nạp firmware. Danh sách linh kiện đầy đủ nằm ở bài mua sắm chương 00 ([Hóa đơn linh kiện và cách mua]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %})). Bài này chỉ tập trung chọn bộ điều khiển trung tâm và cáp dữ liệu để máy tính nhận diện bo mạch.

## Vì sao bài này gắn với Capstone A

Capstone A ở chương 07 là xe vi sai gồm hai bánh dẫn động, một bánh đa hướng và firmware chuyển đổi lệnh điều khiển thành tín hiệu PWM cho mạch cầu H TB6612 ở các bài sau. Luồng lệnh phải có cơ chế an toàn: nếu sau khoảng 300 ms không nhận được lệnh mới, hệ số chu kỳ (duty) của cả hai bánh phải đưa về 0; ở lần đầu cho phép bánh quay, bánh xe phải được nhấc khỏi mặt bàn. Vòng lặp điều khiển đó cần chạy trên một vi điều khiển đã được kiểm chứng. Đến chương 08, bài học về Wi-Fi và MQTT sẽ chuyển việc điều khiển từ xa (teleop) từ cáp USB sang điện thoại hoặc laptop. Vì ESP32 tích hợp sẵn Wi-Fi 2,4 GHz và BLE ngay trên module, đây là lựa chọn mặc định của môn học. Pico không có hậu tố W vẫn chạy tốt firmware chương 07 qua USB và rất tiện để thử nghiệm nhanh, nhưng sẽ không dùng được cho phần kết nối không dây ở chương 08 nếu bạn không đổi sang bản có W hoặc chuyển sang ESP32. Quyết định bạn ghi lại hôm nay sẽ định hình sơ đồ chân, bộ công cụ lập trình (toolchain) và phương án kết nối không dây cho cả học kỳ.

## Ba bo mạch, ba vai trò khác nhau

Trong môn học này, ESP32 được dùng dưới dạng module lõi kép kiến trúc Xtensa gắn trên bo mạch phát triển (dev board), có sẵn Wi-Fi và BLE bên trong vỏ kim loại chống nhiễu, sử dụng mức logic GPIO 3,3 V. Thứ bạn cần mua không phải là module trần chỉ có vỏ kim loại. Một bo mạch dùng được ngay phải có cổng USB, mạch ổn áp 3,3 V, chip chuyển đổi USB-serial, nút BOOT và hàng chân cắm (header). Chip USB-serial phổ biến nhất là CH340 (rất thông dụng tại Việt Nam) hoặc CP2102 (thường được hệ điều hành tự nhận mà không cần cài thêm driver). Module trần không có các thành phần này. NodeMCU-32S dùng CH340 là cấu hình mặc định; Vietduino ESP32 cũng là một bo mạch hoàn chỉnh khác nếu bạn chuộng cách bố trí nhãn in trên mạch đó. Ngược lại, ESP32-S3-WROOM-1 là module trần, nên dù giá thấp hơn vẫn không đưa vào danh sách khởi đầu.

Raspberry Pi Pico hoặc Pico 2 là lựa chọn phù hợp để thử nghiệm nhanh. Pico bản gốc dùng chip RP2040, còn Pico 2 dùng chip RP2350. Cả hai đều dùng GPIO 3,3 V và hỗ trợ môi trường tương tác REPL của MicroPython. Tuy nhiên, Pico bản gốc và Pico 2 không có chữ W đều không tích hợp sẵn Wi-Fi; chỉ bản Pico W và Pico 2 W mới có chip không dây. Bạn cần ghi chính xác tên in trên bo mạch vào sổ tay vì chân LED tích hợp và tệp firmware thay đổi tùy theo hậu tố này. Hãy chọn dòng Pico khi bạn muốn học qua REPL trước và sẵn sàng chờ đổi sang bản W hoặc chuyển sang ESP32 khi đến bài Wi-Fi ở chương 08.

Các bo mạch họ Arduino Uno (dùng ATmega328P và các bản tương thích) hoạt động ở mức logic 5 V. Bạn cần nhận diện rõ dòng này để tránh nhầm lẫn với bộ điều khiển chính của robot. Uno không có Wi-Fi, và tín hiệu mức cao 5 V tuyệt đối không được nối trực tiếp vào chân 3,3 V. Tín hiệu Echo 5 V của cảm biến HC-SR04 hoặc một chân xuất tín hiệu từ Uno có thể làm hỏng chân GPIO của ESP32 hoặc Pico. Nếu đã có sẵn Uno, hãy giữ nó làm bo mạch tham chiếu 5 V trên bàn thí nghiệm, không dùng làm bộ điều khiển chính cho Capstone A.

![Giải phẫu bo mạch: USB, ổn áp, hàng chân, và module]({{ site.imgurl }}/generated/pcb_mcu_anatomy.png)

Cổng USB giúp máy tính giao tiếp với bo mạch, mạch ổn áp tạo ra nguồn 3,3 V, còn hàng chân header là nơi duy nhất để đấu dây. Module trần chỉ gồm phần vỏ kim loại, thiếu toàn bộ các khối phụ trợ còn lại.

![Module ESP32 trên một bo mạch clone nhỏ]({{ site.imgurl }}/wikimedia/ESP32_on_Lolin32_Lite_clone_board_cropped.jpg)

Hãy đối chiếu trực tiếp vỏ kim loại, cổng USB và hàng chân trên bo mạch thực tế của bạn trước khi áp dụng sơ đồ chân vẽ cho một biến thể khác.

![Raspberry Pi Pico, đường MicroPython]({{ site.imgurl }}/wikimedia/Raspberry_Pi_Pico.jpg)

Nút BOOTSEL, cổng micro-USB và các nhãn `3V3`, `VSYS`, `VBUS` là những mốc cần nhận diện trên dòng mạch này. Ảnh minh họa là Pico bản gốc: không có kết nối không dây, LED tích hợp nằm ở GPIO 25.

## Mức logic được xác định bằng con số

Với ngõ vào CMOS, mức logic cao được tính theo tỉ lệ với điện áp nguồn của chính vi mạch đó. Một quy tắc ước lượng thường dùng trong học tập (không thay thế thông số $$V_{IH}$$ chính thức trong datasheet) là chỉ coi chân ở mức cao khi điện áp đạt tối thiểu khoảng $$0{,}7$$ lần điện áp nguồn:

$$
0{,}7 \times 3{,}3\,\mathrm{V} \approx 2{,}3\,\mathrm{V}.
$$

Trên ESP32 và Pico, ngưỡng ước lượng này xấp xỉ 2,3 V. Giá trị $$V_{IL}$$ và $$V_{IH}$$ chính xác nằm trong bảng đặc tính điện của datasheet và thay đổi theo $$V_{DD}$$; bạn sẽ cần tra cứu khi thiết kế mạch chia áp sát ngưỡng. Trước khi đi sâu vào đó, quy tắc vận hành an toàn hơn cả là chỉ đưa tín hiệu tối đa 3,3 V vào các chân GPIO trong môn học này.

Giới hạn chịu áp là lý do không nên đặt Uno làm việc trực tiếp cùng các bo mạch 3,3 V. Điện áp cực đại tuyệt đối cho chân GPIO 3,3 V chỉ nhỉnh hơn điện áp nguồn một chút, vào khoảng:

$$
3{,}3\,\mathrm{V} + 0{,}3\,\mathrm{V} = 3{,}6\,\mathrm{V}.
$$

Mức 5 V vượt xa giới hạn này. Khi cấp 5 V vào chân 3,3 V, diode bảo vệ bên trong sẽ dẫn dòng mạnh, làm nóng chân và có thể gây hỏng chip ngay lần cắm đầu tiên. Tín hiệu Echo 5 V của cảm biến siêu âm HC-SR04 cũng gây ra rủi ro tương tự. Kỹ thuật chuyển mức điện áp sẽ được trình bày ở bài sơ đồ chân, còn ngay hôm nay bạn cần giữ nguyên tắc không nối bất kỳ tín hiệu 5 V nào vào hàng chân GPIO.

## Trình tự khởi chạy bo mạch

Phần lớn các lỗi phần mềm trông có vẻ "ngẫu nhiên" trong tuần đầu thực chất bắt nguồn từ sụt áp nguồn. Khi nguồn sụt, chip tự khởi động lại (reset), bộ đếm quay về 0, khiến đoạn mã vừa sửa trông như nguyên nhân gây lỗi. Trình tự dưới đây thêm từng thành phần một để dễ dàng khoanh vùng nguyên nhân nếu có sự cố.

Trước hết, máy tính phải nhận diện được bo mạch: với ESP32 là một cổng serial mới, còn với Pico ở chế độ bootloader là một ổ đĩa gắn ngoài (như `RPI-RP2` trên Pico gốc hoặc `RP2350` trên Pico 2). Kế tiếp, cho LED tích hợp nháy theo chương trình bạn nạp để xác nhận xung nhịp và chân điều khiển hoạt động. Sau đó, gửi một dòng dữ liệu qua cổng serial ở tốc độ 115200 baud để kiểm tra cáp có truyền dữ liệu. Tiếp theo, đọc tín hiệu từ một nút nhấn hoặc dây nối xuống mass (GND) để xác nhận ngõ vào số hoạt động. Cuối cùng, xuất thử xung PWM trên một chân không tải (hoặc chỉ gắn LED kèm điện trở hạn dòng). Chỉ sau khi hoàn tất năm bước này mới được đấu mạch lái động cơ (driver) và pin. Động cơ TT khi bị kẹt trục có thể kéo dòng lớn làm sụt nguồn USB; nếu nối driver ngay từ ngày đầu, bạn rất dễ mất thời gian sửa một vòng lặp chương trình vốn không hề sai.

![Từ sketch vi điều khiển tới phần ROS sau này]({{ site.imgurl }}/generated/tracks_mcu_ros.png)

Nửa bên trái của sơ đồ tương ứng với chương này: một vi điều khiển, bài thử nháy LED và một dòng serial. Phần điều khiển từ xa của Capstone A mở rộng trên chính con chip đó, xuất PWM tới TB6612 sau khi hoàn tất phần đấu dây driver. Phần ROS ở các chương sau dựa trên giả định rằng trình tự cơ bản này đã chạy ổn định.

## Ví dụ đã làm

An muốn cuối học kỳ dùng điện thoại để điều khiển một robot hai bánh. Ở chương 07, firmware điều khiển từ xa sẽ xuất PWM tới TB6612, tự ngắt sau khoảng 300 ms nếu mất lệnh và yêu cầu nhấc bánh trong lần chạy đầu tiên. Đến chương 08, hệ thống điều khiển này sẽ chuyển sang chạy qua Wi-Fi. An ghi vào sổ: "Vi điều khiển chính là ESP32 NodeMCU-32S dùng chip CH340, vì chương 08 cần Wi-Fi và tuần này cần một bo mạch 3,3 V có thể nạp chương trình ngay."

Module trần ESP32-S3-WROOM-1 tuy rẻ hơn nhưng không cắm trực tiếp vào laptop được. Pico 2 bản không có W tuy dễ học với MicroPython nhưng lại thiếu kết nối không dây cho điều khiển qua điện thoại. Vì vậy, An chỉ mua một bộ điều khiển chính, sau đó ghi tiếp trình tự khởi chạy bên dưới: nhận cổng USB, nháy LED tích hợp, in dòng `hello` ở 115200 baud, đọc nút nhấn kéo xuống mức thấp, xuất PWM không tải, rồi mới nối TB6612 và pin khi khung xe đã được nhấc lên. Arduino Uno chỉ giữ lại làm mốc tham chiếu 5 V.

## Lab

Bài thực hành này có thể làm trên giấy trước khi linh kiện giao tới.

1. Kẻ bảng gồm ba hàng tương ứng với họ Uno, bo mạch ESP32 và Pico (hoặc Pico 2), với các cột: mức điện áp GPIO, sóng vô tuyến tích hợp, ngôn ngữ buổi đầu và vai trò trong Capstone A.
2. Khoanh tròn lựa chọn chính. Bên dưới bảng, liệt kê đủ sáu bước khởi chạy: máy tính nhận USB, nháy LED tích hợp, serial 115200 baud, đọc nút nhấn, xuất PWM không tải, cuối cùng mới nối driver và pin.
3. Ghi thêm một câu mô tả hiện tượng sụt áp (brownout): nguồn bị sụt khiến chip tự reset, dễ gây nhầm lẫn với lỗi phần mềm.
4. Nếu mua hàng trong tuần này, chép chính xác tên sản phẩm, mức giá tham khảo và ngày kiểm tra vào `lab-notes.md`. Nếu đã có sẵn bo mạch trên bàn, ghi lại nhãn in trên mạch và tên chip USB-serial (nếu đọc được), chưa tiến hành nạp mã.

Kết quả cần trình bày rõ ràng trên một trang để người khác đọc hiểu được. Bài đạt khi bạn chốt rõ một vi điều khiển chính, nêu được vai trò của hai dòng còn lại và ghi đủ trình tự khởi chạy như trên. Cách viết chung chung như "thử cả hai rồi tính" không đạt yêu cầu.

Lưu ý khi chọn mua: ảnh sản phẩm chỉ có vỏ kim loại mà không có cổng USB là module trần; cáp USB chỉ hỗ trợ sạc vẫn làm sáng đèn nguồn nhưng máy tính sẽ không tạo cổng kết nối. Cần kiểm tra đúng loại sản phẩm và cáp trước khi tìm lỗi ở driver.

An toàn: chưa đấu nối pin, động cơ hay cảm biến 5 V trong lúc đang chọn bo mạch. Thao tác duy nhất trong bài này là đọc nhãn và thông số.

## Video tham khảo

- **Xem trước:** [Raspberry Pi VS Arduino VS ESP32](https://www.youtube.com/watch?v=oJs0cVYuQTw) — TechteamGB, tiếng Anh. Giải thích vì sao Arduino, ESP32 và Raspberry Pi không thay thế trực tiếp cho nhau, khớp với bảng so sánh trong bài.
- [Raspberry Pi Pico - A Beginners Guide](https://www.youtube.com/watch?v=L03jT5slWnw) — Tinkernut, tiếng Anh. Giới thiệu Pico — lựa chọn thứ ba trong bài; chú ý quan sát cổng USB và sơ đồ chân trước khi so sánh với ESP32.

## Bài tập

1. Điền bảng so sánh Uno, ESP32 và dòng Pico (gồm cả Pico gốc với Pico W, Pico 2 với Pico 2 W). Bắt buộc có một ô ghi rõ "GPIO 5 V".
2. Một sinh viên nối mạch cầu H và pin 2S trước khi kiểm tra bất kỳ dòng serial nào, sau đó báo rằng bộ đếm "tự khởi động lại". Hiện tượng điện nào đang xảy ra và sinh viên đó đã bỏ qua những bước nào?
3. Tính $$0{,}7 \times 3{,}3$$ và $$3{,}3 + 0{,}3$$ theo đơn vị vôn. Giải thích trong hai câu ý nghĩa của mỗi con số và lý do không được nối trực tiếp chân Echo 5 V vào GPIO.
4. Viết câu quyết định chọn vi điều khiển cho Capstone A. Nếu chọn ESP32, nêu rõ tên bo mạch phát triển và lý do không mua module WROOM trần. Nếu chọn Pico, nêu rõ phương án bổ sung Wi-Fi về sau.
5. Có ý kiến cho rằng Raspberry Pi 5 phải là bộ điều khiển chính vì "robot chạy Linux". Trên thực tế, firmware của Capstone A trong học kỳ này chạy trên phần cứng nào?

<details>
<summary>Đáp án</summary>

1. Họ Uno: GPIO 5 V, không tích hợp Wi-Fi, thường khởi đầu bằng Arduino C++, không phù hợp làm bộ điều khiển chính cho Capstone A khi dùng chung với cảm biến 3,3 V. Bo mạch ESP32: GPIO 3,3 V, có sẵn Wi-Fi và BLE, lập trình bằng Arduino qua core ESP32 (hoặc MicroPython về sau), là lựa chọn mặc định vì chương 08 cần kết nối không dây. Pico gốc và Pico 2 không W: GPIO 3,3 V, không tích hợp Wi-Fi, dùng MicroPython để thử nghiệm nhanh. Pico W và Pico 2 W: cùng mức logic 3,3 V, có thêm kết nối không dây.
2. Đó là hiện tượng sụt áp khiến chip tự reset (brownout). Sinh viên này đã bỏ qua chuỗi kiểm tra cơ bản gồm: nhận cổng USB, nháy LED tích hợp, kiểm tra serial, đọc nút nhấn và xuất PWM không tải. Việc bộ đếm quay về 0 là dấu hiệu chip vừa khởi động lại.
3. $$0{,}7 \times 3{,}3 = 2{,}31\,\mathrm{V}$$ (xấp xỉ 2,3 V) là ngưỡng ước lượng trong học tập để xác định tín hiệu đã đủ cao để tính là mức logic 1 hay chưa. $$3{,}3 + 0{,}3 = 3{,}6\,\mathrm{V}$$ là vùng giới hạn điện áp cực đại tuyệt đối của chân 3,3 V. Tín hiệu Echo 5 V vượt quá 3,6 V nên có thể làm hỏng chân, dù 5 V là mức cao hợp lệ trên Uno.
4. Câu chọn ESP32 đạt khi nêu đúng bo mạch có cổng USB (như NodeMCU-32S hoặc DevKit dùng CH340/CP2102), nêu nhu cầu Wi-Fi cho chương 08 và loại trừ module trần. Câu chọn Pico đạt khi nêu ưu tiên MicroPython, xác nhận bản không W thiếu Wi-Fi và nêu rõ kế hoạch nâng cấp lên bản W hoặc chuyển sang ESP32 ở chương 08.
5. Firmware điều khiển từ xa của Capstone A chạy trên vi điều khiển (ESP32 hoặc Pico). Raspberry Pi 5 là máy tính chạy Linux riêng biệt, không thay thế vai trò của vi điều khiển, cáp dữ liệu hay trình tự khởi chạy cơ bản này.

</details>

## Mua ở Việt Nam

Danh sách linh kiện đầy đủ (gồm TB6612, động cơ và cảm biến) nằm ở bài mua sắm chương 00. Trong bài này, bạn chỉ cần mua bo mạch điều khiển và một sợi cáp dữ liệu. Giá dưới đây được ghi nhận từ trang công khai của Hshop vào ngày 23 tháng 9 năm 2026; hãy kiểm tra lại giá hiện tại trước khi đặt mua.

Lựa chọn mặc định: [ESP32 NodeMCU-32S CH340, 190 000 ₫](https://hshop.vn/kit-rf-thu-phat-wifi-ble-esp32-nodemcu-32s-ch340-ai-thinker) (có sẵn cổng USB và chip CH340). Một bo mạch hoàn chỉnh khác là [Vietduino ESP32, 265 000 ₫](https://hshop.vn/mach-phat-trien-vietduino-esp32). Riêng [ESP32-S3-WROOM-1, 135 000 ₫](https://hshop.vn/mach-thu-phat-wifi-ble-soc-esp32-s3-esp32-s3-wroom-1-chinh-hang-espressif) là module trần, không phù hợp để khởi đầu dù giá rẻ hơn.

Nếu đi theo hướng MicroPython: kết quả tìm kiếm [raspberry pi pico](https://hshop.vn/search?q=raspberry+pi+pico) tại thời điểm kiểm tra hiển thị Pico 2 giá 195 000 ₫ và Pico 2 W giá 275 000 ₫. Trang sản phẩm tương ứng là [Pico 2 (RP2350)](https://hshop.vn/mach-raspberry-pi-pico-2-rp2350) và [Pico 2 W](https://hshop.vn/mach-raspberry-pi-pico-2-w-rp2350). Lưu ý rằng Pico 2 bản không có W không tích hợp Wi-Fi.

Cáp dữ liệu tương thích với các bo mạch dùng cổng micro-USB kể trên: [Ugreen Micro-USB 1 m, 54 000 ₫](https://hshop.vn/cap-micro-usb-to-usb-2-0-dai-1m-cao-cap-60136-chinh-hang-ugreen). Tránh dùng cáp chỉ sạc vì máy tính sẽ không nhận bo mạch.

Nếu muốn so sánh thêm trên Shopee, có thể tìm [ESP32 DevKit CH340](https://shopee.vn/search?keyword=esp32%20devkit%20ch340) và [Raspberry Pi Pico 2](https://shopee.vn/search?keyword=raspberry%20pi%20pico%202), chú ý kiểm tra ảnh xem có cổng USB hay không. [Trang ESP32-DevKitC-32U của Thế Giới IC](https://www.thegioiic.com/esp32-devkitc-32u-module-wifi-bluetooth-2-4ghz) cũng là một mẫu dev board; cần xem kỹ anten có dùng đầu nối U.FL và sản phẩm có kèm cáp hay không. [IC Đây Rồi](https://icdayroi.com/) là cửa hàng linh kiện tại Thủ Đức, phù hợp để mua điện trở về sau, nhưng cần phân biệt kỹ giữa linh kiện rời và bo mạch phát triển có sẵn cổng USB.

## Đọc thêm

- [Datasheet ESP32 (PDF)](https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf) — thông số điện áp GPIO, các chân strapping và bảng đặc tính điện đứng sau ngưỡng 2,3 V.
- [Datasheet Raspberry Pi Pico](https://datasheets.raspberrypi.com/pico/pico-datasheet.pdf) — thông tin về LED tích hợp tại GPIO 25 và ý nghĩa các đường nguồn VBUS, VSYS, 3V3.
- [Tài liệu vi điều khiển Raspberry Pi](https://www.raspberrypi.com/documentation/microcontrollers/) — tổng quan các phiên bản Pico, Pico W, Pico 2 và Pico 2 W trong cùng một họ sản phẩm.
