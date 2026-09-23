---
layout: post
title: "Đọc datasheet và sơ đồ chân"
chapter: "01"
order: 7
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter01
lesson_type: required
draft: false
---

Datasheet là trang duy nhất được phép cho một sợi dây tồn tại. Bài này chốt một thứ tự đọc, rồi dùng cho module TB6612FNG của xe hai bánh và cho chân ESP32 không được chạm xung echo 5 V.

## Mục tiêu

Bạn mở một PDF lạ và đi đúng một vòng: thông số cực đại tuyệt đối, sơ đồ chân và tên chân, điều kiện làm việc khuyến nghị, vài dòng đặc tính điện bạn sẽ dùng thật, sơ đồ ứng dụng mẫu, rồi bản vẽ vỏ để biết chân 1 nằm đâu. Với module kiểu TB6612, bạn chép được cửa sổ nguồn động cơ, cửa sổ nguồn logic, quy tắc chân STBY, dòng liên tục và dòng đỉnh, rồi đặt được AIN1, AIN2, PWMA, BIN1, BIN2, PWMB, AO1, AO2, BO1, BO2 lên một tờ giấy. Bạn chỉ vào hàng cực đại của ESP32 và nói vì sao dây echo của HC-SR04 không được cắm thẳng vào GPIO. Nhãn in trên board clone chỉ là tin đồn, cho đến khi đồng hồ và datasheet cùng một ý.

## Kiến thức cần có

Cần định luật Ohm ở bài 01, thói quen đo của bài 02, và cực tính ở bài 04. Hôm nay không cấp nguồn mô-tơ. Mang một trang sổ còn đọc được ở chương 02.

## Vì sao bài này quan trọng

Xe capstone là dẫn động vi sai: hai mô-tơ TT, module TB6612FNG, board 3,3 V kiểu ESP32 hoặc Pico. VM lấy pin động cơ, không lấy USB. VCC được ngồi trên rail 3,3 V. Echo của HC-SR04 là ngõ ra 5 V, còn GPIO thì không chịu 5 V. Học tên chân như học nhãn dán thì buổi chạy đầu trông như lỗi phần mềm: bánh kẹt ở chế độ chờ, hoặc GPIO chết lúc cảm biến trả lời. Thứ tự dưới đây tìm con số cấm sợi dây, trước khi sợi dây được nối.

![Cầu H đang làm gì với các chân ra mô-tơ]({{ site.imgurl }}/generated/hbridge_concept.png)

Mỗi mô-tơ nằm giữa một cặp chân ra. Chiều là chân nào cao, tốc độ là PWM, và cả hai vô nghĩa khi STBY còn tắt cầu. Xem hình sau khi đã có tên chân.

## Thứ tự đọc, không đảo

**1. Thông số cực đại tuyệt đối.** Đây là hàng rào hỏng. Vượt qua thì hãng không còn hứa linh kiện sống. Không phải điểm để vận hành. Chép một ô khớp sợi dây định nối: điện áp nguồn, điện áp chân logic, hoặc dòng ra. Vượt ô đó thì phương án bị cấm.

**2. Sơ đồ chân và tên chân.** Bảng chân là từ điển. AO1 chưa phải "bánh trái" cho đến khi bạn quyết định phích nào cắm vào AO1. Trên module TB6612FNG, những tên phải chỉ được bằng bút chì là AIN1, AIN2, PWMA, BIN1, BIN2, PWMB, AO1, AO2, BO1, BO2, cùng VM, VCC, GND và STBY. Chân vào là chỗ GPIO được phép điều khiển. Chân ra là chỗ được phép chạm mô-tơ. Trộn hai nhóm là cách đưa dòng mô-tơ vào vi điều khiển.

**3. Điều kiện làm việc khuyến nghị.** Robot sống ở vùng này, nơi các bảng còn lại được đo. Trang bán module có thể chặt hơn con chip trần, vì đồng và header là một phần của món bạn mua. Trang bán chặt hơn thì trang bán thắng.

**4. Đặc tính điện bạn sẽ dùng.** Bỏ những dòng chưa đo được. Với driver này, chép điện áp tối thiểu vẫn được tính là mức cao, việc STBY phải ở mức cao nếu không mọi hàng khác vô nghĩa, rồi dòng liên tục và dòng đỉnh.

**5. Sơ đồ ứng dụng mẫu.** Chép ý: tụ gần VM, tụ gần VCC, một mass chung, các chân vào do chip khác điều khiển. Module có thể đã gắn sẵn tụ nhỏ. Thêm một tụ không cứu được mass bị quên giữa ESP32 và driver.

**6. Bản vẽ vỏ, để tìm chân 1.** Hình là nhìn từ trên: mắt nhìn xuống mặt nhựa, chân cắm xuống board. Chân 1 nằm cạnh chấm hoặc cạnh vát. Ảnh chụp từ đáy sẽ lật hàng. Chấm và nhãn in không thống nhất chân AO1 thì đồng hồ phân xử.

Board clone nói dối bằng mực. Nhãn "5V" dán lên chân logic 3,3 V, GND đổi chỗ với VM, mũi tên ECHO chỉ vào chân trigger: hàng đó vẫn được giao. Chỉ cấp nguồn cho rail nghi ngờ, nguồn có hạn dòng, que đen ở mass, rồi ghi số vôn lên tờ giấy. Sau bước đó, nhãn in không còn quyền biểu quyết.

## TB6612FNG, đi một vòng

Dùng cửa sổ của module mà khóa này mua, và cách hoạt động Toshiba được Pololu tóm trên trang carrier ở mục đọc thêm. Ô trên trang ấy khác bài này thì trang ấy đúng. Listing module của bạn còn chặt hơn cả hai thì listing thắng.

Cực đại tuyệt đối đi trước để pin ngược hoặc quá áp bị loại trước khi giắc khớp. Bảng đó là hàng rào. Đoạn sau mới là chỗ được sống.

Tên chân đi thứ hai. Mô-tơ A nhận lệnh từ AIN1 và AIN2, chân tốc độ là PWMA. Mô-tơ B là BIN1, BIN2 và PWMB. Miếng đồng chạm dây mô-tơ là AO1 với AO2, hoặc BO1 với BO2. STBY không phải GPIO dư. Trên chip này nó là công tắc tắt cả hai cầu. Bảng điều khiển không có chuyển động nào cho đến khi STBY ở mức cao. Nhiều module kéo STBY xuống sẵn trên board, nên quên một sợi dây là cả hai bánh đứng yên trong khi sổ tay ghi "tiến".

Điều kiện khuyến nghị đi thứ ba. Module mà khóa này coi là món cần mua có VM từ 4,5 V đến 10 V. Một cell lithium khoảng 3,7 V nằm dưới sàn đó. Bộ pin khi sạc no vượt 10 V thì vượt trần module, dù PDF của chip trần có vẻ rộng rãi hơn. VCC logic từ 2,7 V đến 5,5 V, nên rail 3,3 V là nguồn logic hợp lệ. USB 5 V cũng nằm trong cửa sổ logic ấy, và vẫn là nguồn mô-tơ tồi. Chuyện đó là bài 09. VM và VCC là hai chân khác nhau có chủ đích.

Những dòng sẽ dùng đi thứ tư. Dòng liên tục khoảng 1,2 A mỗi kênh, dòng đỉnh khoảng 3,2 A. Hai mô-tơ TT quay không tải nằm rất thấp so với 1,2 A. Kẹt rotor thì không. Để trạng thái kẹt ngồi trên dòng liên tục thì driver thành cầu chì ngoài ý muốn. Chép luôn quy tắc mức cao. Nhiều bản in đặt

$$
V_{IH,\min} = 0{,}7 \times V_{CC}
$$

Tại $$V_{CC} = 3{,}3\,\mathrm{V}$$ thì được $$2{,}31\,\mathrm{V}$$. GPIO kéo lên 3,3 V vượt qua được. Cùng hệ số ấy ở 5 V là $$3{,}5\,\mathrm{V}$$, và GPIO 3,3 V không vượt 3,5 V. Một con số đó cấm câu "cấp logic 5 V vì nhãn in nói vậy, rồi điều khiển chân vào từ ESP32". Hãy nuôi VCC bằng 3,3 V. Đừng sống trong khoảng trống rồi hy vọng chân vào "gần đúng".

Sơ đồ đi thứ năm. VM tới pin động cơ, VCC tới 3,3 V, mass nối nhau, mô-tơ trên AO1/AO2 và BO1/BO2, bốn GPIO cho AIN1, AIN2, PWMA và STBY. Tụ đệm mắc ngang VM, đúng cực; bài 09 chọn dung lượng. Bản vẽ vỏ đi thứ sáu: đánh dấu chân 1 dù bạn chỉ đụng header.

"Thuận chiều kim đồng hồ" trong datasheet theo dây mô-tơ, không theo mũi xe. STBY cao, AIN1 khác AIN2, PWMA cao thì mô-tơ chạy; đảo AIN1 với AIN2 thì đảo chiều; STBY thấp thì vẫn chờ. Lần chạy sau: STBY cao, hai chân hướng khác nhau, PWM vừa.

## GPIO của ESP32 không phải chỗ để sống ở 5 V

Mở PDF Espressif và đi cùng thứ tự. Điện áp cực đại trên GPIO nằm ở rail 3,3 V, cao hơn rail ấy vài trăm milivôn, không phải 5 V. Vùng khuyến nghị là nguồn vào/ra 3,3 V đó. Hàng cực đại chỉ là hàng rào, không phải chỗ để ở. Xung 5 V nằm ngoài hàng rào.

HC-SR04 làm hàng rào ấy cụ thể. Cảm biến nuôi bằng 5 V, dây echo vọt lên khoảng 5 V khi có xung phản hồi. Ô cực đại ấy cấm nối thẳng vào bất kỳ GPIO nào của ESP32. Trigger là ngõ vào của cảm biến, thường kéo được từ 3,3 V. Echo thì không. Mạch chia áp là việc sau; hôm nay tờ MCU ghi "echo không nối thẳng" và chép điện áp đã buộc quyết định đó. Pico cùng giới hạn: tài liệu Raspberry Pi mô tả chân 3,3 V không chịu 5 V, và code dùng số GP trên hình, không phải đếm pad từ đầu USB.

Board clone in "5V" cạnh một lỗ bạn tưởng là GPIO thì hãy đo khi chỉ cắm USB. Lỗ nào ngồi gần 5 V là chân nguồn. Không phải chỗ nhận echo, cũng không phải chỗ gắn LED khi chưa có điện trở.

## Thực hành

Không có gì quay. Bạn nộp hai tờ.

1. Đặt tên hai trang: "sơ đồ chân MCU" và "sơ đồ chân driver". Ghi ngày. Board chưa về thì làm tờ MCU từ PDF ESP32 và ghi "chưa mua board".
2. Tờ driver phải thấy đủ sáu bước. Chép VM 4,5–10 V, VCC 2,7–5,5 V, "STBY phải mức cao", 1,2 A liên tục, 3,2 A đỉnh. Phác header và gắn nhãn AIN1, AIN2, PWMA, BIN1, BIN2, PWMB, AO1, AO2, BO1, BO2, VM, VCC, GND, STBY. Nhãn in khác chữ thì giữ hai cột.
3. Tờ MCU chép điện áp cực đại của GPIO và tên bảng. Ghi echo của HC-SR04 là ngõ ra 5 V, không được rơi vào GPIO. Gán chân ra hợp lệ cho AIN1, AIN2, PWMA và STBY. ESP32 kiểu module thông dụng thì tránh chân flash và chân chỉ vào.
4. Không cấp VM. Nếu nuôi được riêng rail logic bằng nguồn 3,3 V có hạn dòng, đo chân nhãn "5V" và chân nhãn "3V3", que đen ở mass. Không làm an toàn được thì viết các bước đo và đánh dấu "dry-run".
5. Cất hai tờ vào sổ. Ảnh `ch01-07-mcu-card` và `ch01-07-driver-card` là đủ nếu chương 02 còn đọc được.

Dừng nếu một chân nóng, hoặc lỗ bạn sắp gọi là GPIO đo được gần 5 V.

## Bài tập

Mỗi câu trả lời gồm một con số, bảng chứa nó, và sợi dây mà con số ấy cấm.

1. Có người nối ECHO của HC-SR04 thẳng vào GPIO 4 của ESP32 và nói bảng cực đại sẽ gánh được. Con số nào cấm sợi dây, và bạn ghi gì nếu đo xung echo khi cảm biến nuôi 5 V?
2. Nhãn driver nói chân logic cần 5 V. Mức cao của ESP32 là 3,3 V. Tính $$0{,}7 \times 5$$ và $$0{,}7 \times 3{,}3$$. Kết quả nào cấm ESP32 điều khiển các chân vào đó, và VCC nào gỡ lệnh cấm?
3. Hai mô-tơ TT sắp bị cột vào chân 5 V của ESP32 "chỉ để thử". USB khoảng 500 mA. Driver chịu 1,2 A liên tục. Con số nào vỡ trước, và vì sao con số lớn hơn không phải giấy phép dùng USB làm VM?
4. STBY để hở và chương trình không kéo nó. Hành vi nào của chip cấm PWM làm bánh quay, và một thao tác GPIO nào gỡ được?
5. Về một board DRV8833 thay vì TB6612. Điều gì cấm chép AIN1, PWMA và STBY từ tờ hôm nay lên nhãn đó, và phải mở trang nào ở mục đọc thêm?

<details markdown="1">
<summary>Gợi ý đáp án</summary>

1. Lệnh cấm là điện áp cực đại của GPIO ESP32, nằm ở rail 3,3 V chứ không phải 5 V. Echo xung lên gần điện áp nuôi cảm biến, khoảng 5 V. Ghi mức cao đo được cạnh ô đó. Nối thẳng đã sai; mạch chia là việc sau.
2. $$0{,}7 \times 5 = 3{,}5\,\mathrm{V}$$, GPIO 3,3 V không tới, nên VCC = 5 V bị cấm với các chân vào ấy. $$0{,}7 \times 3{,}3 = 2{,}31\,\mathrm{V}$$, GPIO tới được. Nuôi VCC bằng 3,3 V.
3. Ngân sách USB 500 mA vỡ trước. Dòng kẹt của một mô-tơ TT đã vượt mức đó, hai mô-tơ còn nặng hơn. Con số 1,2 A là trần liên tục của driver, không phải lời hứa USB cấp được ngần ấy. VM ở lại trên pin động cơ.
4. STBY bị giữ thấp, kể cả chân không được điều khiển và bị kéo xuống, giữ cả hai cầu ở chế độ chờ. Kéo STBY lên cao và giữ trong lúc được phép chạy.
5. Tên chân không đi theo họ driver. Mở trang TI DRV8833 và làm lại sáu bước. Gắn đúng tên mà datasheet của chip đó in.

</details>

## Đọc thêm

- [Module TB6612FNG của Pololu](https://www.pololu.com/product/713) — cách Toshiba hoạt động, viết ngắn: dải logic, STBY, và chuyện 1,2 A / 3,2 A. Trang này sửa bài học nếu một ô khác, và listing module thắng khi nó chặt hơn.
- [Datasheet ESP32 (PDF)](https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf) — cực đại tuyệt đối và danh sách GPIO cho câu echo.
- [TI DRV8833](https://www.ti.com/product/DRV8833) — driver còn lại mà checklist chương cho phép ghi tên. Chip trong ảnh không phải TB6612 thì bắt đầu từ đây.
- [Tài liệu Raspberry Pi Pico](https://www.raspberrypi.com/documentation/microcontrollers/raspberry-pi-pico.html) — vào/ra 3,3 V, chân 1, và số GP mà code phải dùng.

## Mua ở Việt Nam

ESP32 hoặc Pico, module kiểu TB6612, mô-tơ TT và HC-SR04 đã nằm trong danh sách kit ở chương 00, bài 05, [BOM và cách mua bộ kit robot ở Việt Nam]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %}). Mua theo bài đó. Đừng lập một bộ thứ hai ở đây, và đừng mua TB6612FNG rời, chân nhỏ, để hàn tay cho capstone.

Chưa có đồng hồ thì chưa kiểm được nhãn in. Một trang đã kiểm là UNI-T UT33D tại [Hshop](https://hshop.vn/dong-ho-van-nang-dien-tu-digital-multimeter-uni-t-ut33d-chinh-hang). Đọc giá đang bán. So shop thì xem [Hshop](https://hshop.vn/), [Thế Giới IC](https://www.thegioiic.com/) và [IC Đầy Rồi](https://icdayroi.com/).
