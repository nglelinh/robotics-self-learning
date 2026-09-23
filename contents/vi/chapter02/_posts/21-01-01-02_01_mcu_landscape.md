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

Hết bài này bạn so được ba lựa chọn thật cho một robot vi sai nhỏ: bo mạch ESP32 có cổng USB, Raspberry Pi Pico hoặc Pico 2, và board họ Arduino Uno. Bạn nói được mỗi loại dùng mức logic nào, có sóng vô tuyến sẵn hay không, và ngôn ngữ bạn sẽ gõ trong buổi đầu. Khi sau này điện thoại phải điều khiển xe, bạn chọn ESP32 NodeMCU-32S, và bạn phân biệt được module trần với Pico không có Wi-Fi. Bạn viết được thứ tự đưa board lên để một lần sụt nguồn không bị ngộ nhận là lỗi ngẫu nhiên trong chương trình. Bạn cũng tính được ngưỡng học tập cho mức cao 3,3 V và từ chối tín hiệu 5 V trên GPIO.

## Cần gì trước khi học

Bạn chỉnh được đồng hồ về điện áp một chiều, và bạn biết GPIO là chân mà chip có thể kéo hoặc đọc. Điện trở nối tiếp trước LED ở chương 01 là đủ. Chưa cần từng nạp firmware. Giỏ hàng đầy đủ nằm ở bài mua sắm chương 00 ([Hóa đơn linh kiện và cách mua]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %})). Bài này chỉ chọn bộ não và sợi cáp để máy tính nhận board.

## Vì sao bài này gắn với Capstone A

Capstone A ở chương 07 là xe vi sai: hai bánh dẫn động, một bánh đa hướng, và firmware biến lệnh thành PWM cho TB6612 ở các bài sau. Luồng lệnh không được tin mãi. Nếu khoảng 300 ms không có lệnh mới, cả hai bánh về duty 0, và lần đầu bánh được phép quay thì bánh phải nhấc khỏi mặt bàn. Vòng lặp đó nằm trên một vi điều khiển bạn đã tin. Chương 08 có bài Wi-Fi và MQTT, tức là lúc teleop rời cáp USB để tới điện thoại hoặc laptop. ESP32 đã có Wi-Fi 2,4 GHz và BLE trên module, nên đó là lựa chọn mặc định của môn. Pico không có hậu tố W vẫn chạy firmware chương 07 qua USB, và đó là board thử nhanh rất tốt, nhưng nó không vào bài radio chương 08 cho đến khi bạn mua board khác. Câu bạn ghi hôm nay là sơ đồ chân, toolchain, và câu chuyện sóng vô tuyến của cả học kỳ.

## Ba board, ba việc khác nhau

ESP32 trong môn này là module Xtensa lõi kép trên một bo mạch phát triển, Wi-Fi và BLE nằm trong vỏ kim loại, GPIO 3,3 V. Thứ cần mua không phải cái vỏ đó một mình. Board dùng được ngay phải có sẵn cổng USB, ổn áp 3,3 V, chip USB-serial, nút BOOT, và hàng chân. Chip serial thường là CH340, rất hay gặp ở hàng bán tại Việt Nam, hoặc CP2102, hệ điều hành thường nhận không cần driver thêm. Module trần không có những thứ đó. NodeMCU-32S gắn CH340 là hình dạng của lựa chọn mặc định. Listing Vietduino ESP32 là một bo mạch hoàn chỉnh khác nếu bạn thích silk đó. Dòng ESP32-S3-WROOM-1 là module trần, giá thấp hơn vẫn không được đưa vào danh sách khởi đầu.

Raspberry Pi Pico hoặc Pico 2 là đường thử nhanh. Pico gốc dùng RP2040. Pico 2 dùng RP2350. Cả hai chạy GPIO 3,3 V và cả hai trả lời trong REPL MicroPython. Pico gốc và Pico 2 không có chữ W thì không có Wi-Fi sẵn. Pico W và Pico 2 W mới thêm radio. Trong sổ tay phải ghi đúng dòng chữ trên board, vì chân LED và file firmware đổi theo hậu tố đó. Chọn họ này khi bạn muốn học REPL trước, và khi bài Wi-Fi chương 08 có thể chờ một board W hoặc một lần chuyển sang ESP32.

Board họ Arduino Uno, ATmega328P và các bản sao, là logic 5 V. Cần nhận ra nó để khỏi nhầm với bộ não của robot. Nó không có Wi-Fi, và mức cao 5 V không được phép chạm chân 3,3 V. Echo của HC-SR04, hoặc một chân Uno bị ghi là “chỉ là tín hiệu”, có thể giết chân ESP32 hoặc Pico. Nếu bạn đã có Uno thì giữ làm mốc 5 V trên bàn. Đừng cắm nó vào ổ cắm của Capstone A.

![Giải phẫu bo mạch: USB, ổn áp, hàng chân, và module]({{ site.imgurl }}/generated/pcb_mcu_anatomy.png)

Cổng USB là cách laptop nhận board. Ổn áp tạo ra 3,3 V. Hàng chân là chỗ duy nhất bạn được đi dây. Module trần trong khay chỉ có vỏ kim loại, không có phần còn lại.

![Module ESP32 trên một bo mạch clone nhỏ]({{ site.imgurl }}/wikimedia/ESP32_on_Lolin32_Lite_clone_board_cropped.jpg)

Đối chiếu board của bạn với vỏ kim loại, ổ USB, và hàng chân trước khi tin một sơ đồ vẽ cho bản clone khác.

![Raspberry Pi Pico, đường MicroPython]({{ site.imgurl }}/wikimedia/Raspberry_Pi_Pico.jpg)

BOOTSEL, phích micro-USB, và các nhãn `3V3`, `VSYS`, `VBUS` là mốc của đường này. Ảnh là Pico gốc: không radio, LED onboard ở GPIO 25.

## Mức logic là một con số

Trong ngõ vào CMOS, mức cao là điện áp so với nguồn của chính con chip đó. Quy tắc học tập, không phải $$V_{IH}$$ trong datasheet, là chỉ coi chân ở mức cao khi điện áp đạt khoảng $$0{,}7$$ lần nguồn:

$$
0{,}7 \times 3{,}3\,\mathrm{V} \approx 2{,}3\,\mathrm{V}.
$$

Trên ESP32 và Pico, ngưỡng giảng đường đó khoảng 2,3 V. $$V_{IL}$$ và $$V_{IH}$$ thật nằm trong bảng đặc tính điện và chúng đổi theo $$V_{DD}$$. Bạn sẽ tra khi một mạch chia áp sát mép. Trước đó, quy tắc vận hành chặt hơn công thức: GPIO trong môn này chỉ là 3,3 V.

Ngưỡng hỏng là lý do Uno đứng cạnh những chân này thì vụng. Cực đại tuyệt đối của GPIO 3,3 V chỉ nhỉnh hơn ray một chút, cỡ

$$
3{,}3\,\mathrm{V} + 0{,}3\,\mathrm{V} = 3{,}6\,\mathrm{V}.
$$

Năm vôn nằm trên mức đó. Diode bảo vệ dẫn, chân nóng, và chip có thể chết ngay lần cắm đầu. Echo 5 V của HC-SR04 là cùng một vấn đề trong vỏ nhỏ hơn. Đổi mức để dành cho bài sơ đồ chân. Quyết định giữ 5 V ra khỏi hàng GPIO thì làm hôm nay.

## Thứ tự đưa board lên

Phần lớn lỗi firmware “ngẫu nhiên” tuần đầu là một đường nguồn bị sụt. Chip reset, bộ đếm về không, và đoạn code vừa sửa trông có tội. Mỗi bước dưới đây chỉ thêm một việc, nên dấu hiệu đó còn nhìn thấy.

Máy tính phải thấy board trước. Với ESP32 đó là một cổng serial. Với Pico, khi bạn gọi bootloader, đó là ổ tên `RPI-RP2`. Rồi LED onboard nhấp theo chương trình của bạn, tức là clock và một chân bạn đã chọn còn sống. Rồi một dòng serial ở 115200 baud chứng tỏ cáp mang dữ liệu. Rồi bạn đọc một nút nhấn hoặc một sợi nhảy xuống mass, tức là ngõ vào có thật. Rồi bạn tạo PWM trên một chân chưa gắn gì ngoài có thể một LED và điện trở. Chỉ sau năm quan sát đó mới nối driver và pin. Động cơ TT khi kẹt có thể kéo sập nguồn USB. Sinh viên kẹp driver ngay ngày đầu sẽ mất một tuần viết lại vòng lặp vốn không sai.

![Từ sketch vi điều khiển tới phần ROS sau này]({{ site.imgurl }}/generated/tracks_mcu_ros.png)

Phía trái hình là chương này: một vi điều khiển, một lần nhấp, một dòng serial. Teleop của Capstone A nằm xa hơn trên cùng con chip, PWM chỉ nhằm vào TB6612 khi phần dây driver đã được phép. Phần ROS sau này giả định thứ tự này đã xong.

## Ví dụ đã làm

An muốn cuối kỳ có điện thoại lái một robot hai bánh. Chương 07 là firmware teleop: PWM hướng tới TB6612, thời gian chờ gần 300 ms, bánh nhấc lên lần đầu được phép quay. Chương 08 là chỗ teleop đó dùng được Wi-Fi. An viết: “Vi điều khiển chính là ESP32 NodeMCU-32S có CH340, vì chương 08 cần Wi-Fi và tuần này cần một board 3,3 V nạp được ngay.”

ESP32-S3-WROOM-1 trần rẻ hơn và không cắm được vào laptop. Pico 2 không có W thì MicroPython rất dễ, nhưng không có radio, nên điện thoại phải chờ. An mua một bộ não. Dòng dưới câu đó là thứ tự đưa lên: cổng USB, LED onboard, dòng `hello` ở 115200, một nút đọc mức thấp khi nhấn, PWM trên chân không tải, rồi mới tới TB6612 và pin, khung xe được nhấc. Uno giữ vai trò mốc 5 V.

## Lab

Lab này làm trên giấy cũng được, trước khi hàng tới.

1. Vẽ bảng ba dòng. Dòng: họ Uno, bo mạch ESP32, Pico hoặc Pico 2. Cột: điện áp GPIO, sóng vô tuyến có sẵn, ngôn ngữ buổi đầu, và có phải bộ não Capstone A hay không.
2. Khoanh một dòng chính. Dưới bảng viết sáu bước: USB được nhận, LED onboard, serial 115200, đọc nút, PWM không tải, driver và pin.
3. Thêm một câu gọi tên brownout: đường nguồn sụt làm chip reset và trông giống lỗi phần mềm.
4. Nếu tuần này mua hàng, chép đúng tên sản phẩm và giá bạn thấy vào `lab-notes.md` kèm ngày. Nếu board đã ở trên bàn, ghi silk và tên chip USB-serial nếu có in, chưa nạp.

Bạn phải có một trang mà bạn cùng lớp đọc được. Đạt khi ghi một vi điều khiển chính, nói hai họ kia để làm gì, và liệt kê thứ tự đưa lên như trên. Câu “thử cả hai rồi tính” không đạt.

Ảnh listing chỉ có vỏ kim loại, không ổ USB, là module trần. Cáp chỉ sạc làm sáng LED nguồn và không tạo cổng. Sửa listing trước khi sửa driver.

An toàn: chưa nối pin, động cơ, hay cảm biến 5 V khi vẫn đang chọn board. Việc điện duy nhất hôm nay là đọc nhãn.

## Bài tập

1. Điền bảng so sánh Uno, ESP32, và Pico, kể cả Pico gốc với Pico W, Pico 2 với Pico 2 W. Một ô phải ghi “GPIO 5 V.”
2. Một bạn kẹp driver và pin 2S trước khi có bất kỳ dòng serial nào, rồi nói bộ đếm “tự khởi động lại.” Sự kiện điện là gì, và bước nào bị bỏ?
3. Tính $$0{,}7 \times 3{,}3$$ và $$3{,}3 + 0{,}3$$ theo vôn. Hai câu: mỗi số dùng để làm gì, và vì sao echo 5 V vẫn không được chạm chân.
4. Viết câu quyết định Capstone. Nếu chọn ESP32, ghi tên bo mạch và nói rõ không mua WROOM trần. Nếu chọn Pico, nói Wi-Fi sẽ đến bằng cách nào.
5. Một bạn nói Raspberry Pi 5 phải là bộ não vì “robot dùng Linux.” Capstone A học kỳ này thực sự chạy trên cái gì?

<details>
<summary>Đáp án</summary>

1. Họ Uno: GPIO 5 V, không Wi-Fi sẵn, thường bắt đầu bằng Arduino C++, hợp kém làm não Capstone cạnh cảm biến 3,3 V. Bo mạch ESP32: GPIO 3,3 V, Wi-Fi và BLE, Arduino qua core ESP32 hoặc MicroPython sau, mặc định khi chương 08 cần radio. Pico gốc và Pico 2 không W: GPIO 3,3 V, không Wi-Fi sẵn, MicroPython là đường nhanh. Pico W và Pico 2 W: cùng họ 3,3 V, có thêm radio.
2. Nguồn sụt và chip reset (brownout). Họ bỏ chuỗi mà chỉ kết thúc sau khi đã thấy USB, nhấp LED, serial, nút, và PWM không tải. Bộ đếm khởi động lại chính là đường boot chạy thêm lần nữa.
3. $$0{,}7 \times 3{,}3 = 2{,}31\,\mathrm{V}$$, khoảng 2,3 V, ngưỡng giảng đường cho câu “đã đủ cao để tính là cao chưa?”. $$3{,}3 + 0{,}3 = 3{,}6\,\mathrm{V}$$, vùng cực đại tuyệt đối của chân 3,3 V. Echo 5 V cao hơn 3,6 V nên có thể hỏng chân, dù 5 V là mức cao bình thường trên Uno.
4. Câu ESP32 đạt khi nêu một bo mạch có USB (NodeMCU-32S hoặc DevKit khác với CH340 hoặc CP2102), Wi-Fi cho chương 08, và từ chối module trần. Câu Pico đạt khi nêu MicroPython, nói board không W thì không có Wi-Fi, và nêu board W sau này hoặc một lần chuyển sang ESP32.
5. Firmware teleop của Capstone A chạy trên ESP32 hoặc Pico. Pi 5 là máy Linux riêng và không thay con chip đó, sợi cáp dữ liệu, hay thứ tự đưa board lên.

</details>

## Mua ở Việt Nam

Giỏ đầy đủ, gồm TB6612, động cơ, và cảm biến, nằm ở bài mua sắm chương 00. Ở đây mua bộ não và một cáp dữ liệu. Giá dưới đây đọc từ listing công khai của Hshop ngày 23 tháng 9 năm 2026. Mở lại trang trước khi chuyển khoản.

Board mặc định: [ESP32 NodeMCU-32S CH340, 190 000 ₫](https://hshop.vn/kit-rf-thu-phat-wifi-ble-esp32-nodemcu-32s-ch340-ai-thinker). Có USB và CH340. Board hoàn chỉnh thứ hai, nếu muốn listing đó: [Vietduino ESP32, 265 000 ₫](https://hshop.vn/mach-phat-trien-vietduino-esp32). [ESP32-S3-WROOM-1, 135 000 ₫](https://hshop.vn/mach-thu-phat-wifi-ble-soc-esp32-s3-esp32-s3-wroom-1-chinh-hang-espressif) là module trần. Không phải bộ khởi đầu, dù rẻ hơn.

Đường MicroPython: trang tìm [raspberry pi pico](https://hshop.vn/search?q=raspberry+pi+pico) hôm đó hiện Pico 2 giá 195 000 ₫ và Pico 2 W giá 275 000 ₫. Trang sản phẩm: [Pico 2 (RP2350)](https://hshop.vn/mach-raspberry-pi-pico-2-rp2350) và [Pico 2 W](https://hshop.vn/mach-raspberry-pi-pico-2-w-rp2350). Pico 2 không W thì không có Wi-Fi.

Cáp khớp các board micro-USB này: [Ugreen Micro-USB 1 m, 54 000 ₫](https://hshop.vn/cap-micro-usb-to-usb-2-0-dai-1m-cao-cap-60136-chinh-hang-ugreen). Cáp chỉ sạc không được máy tính nhận.

Nếu so shop trên Shopee: [ESP32 DevKit CH340](https://shopee.vn/search?keyword=esp32%20devkit%20ch340) và [Raspberry Pi Pico 2](https://shopee.vn/search?keyword=raspberry%20pi%20pico%202). Đọc xem ảnh có ổ USB hay không. [Trang ESP32-DevKitC-32U của Thế Giới IC](https://www.thegioiic.com/esp32-devkitc-32u-module-wifi-bluetooth-2-4ghz) là listing kiểu dev board; xem anten có phải bản U.FL và có kèm cáp hay không. [IC Đây Rồi](https://icdayroi.com/) là quầy linh kiện ở Thủ Đức, hợp cho điện trở sau này, và dễ bị đọc nhầm thành chỗ bán board USB hoàn chỉnh.

## Đọc thêm

- [Datasheet ESP32 (PDF)](https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf) — điện áp GPIO, chân strapping, và bảng điện đứng sau ngưỡng 2,3 V.
- [Datasheet Raspberry Pi Pico](https://datasheets.raspberrypi.com/pico/pico-datasheet.pdf) — board nào có LED ở GPIO 25, và VBUS, VSYS, 3V3 nghĩa là gì.
- [Tài liệu vi điều khiển Raspberry Pi](https://www.raspberrypi.com/documentation/microcontrollers/) — Pico, Pico W, Pico 2, và Pico 2 W trong cùng một họ.
