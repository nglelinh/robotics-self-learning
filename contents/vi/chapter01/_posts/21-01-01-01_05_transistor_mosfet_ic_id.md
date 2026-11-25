---
layout: post
title: "Transistor, MOSFET, IC ổn áp và dạng vỏ"
chapter: "01"
order: 5
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter01
lesson_type: required
draft: false
---

## Mục tiêu

Sau bài học này, bạn sẽ loại bỏ thói quen đoán sơ đồ chân linh kiện chỉ dựa vào hình dạng vỏ ngoài: cùng vỏ TO-92 hoặc TO-220 có thể là 2N2222, BC547, 2N3904, AMS1117, 7805 hay một MOSFET nhỏ — chỉ ký hiệu in trên thân kết hợp datasheet mới xác định đúng danh tính linh kiện. Bạn sẽ đánh số chân IC vỏ DIP chính xác từ dấu chấm hoặc rãnh khuyết theo chiều ngược kim đồng hồ, giải thích được vì sao cực cổng (gate) MOSFET khác với cực bazơ (base) của transistor lưỡng cực, và hiểu vì sao điện áp ngưỡng $V_{GS(th)}$ không phải mức điện áp để MOSFET dẫn bão hòa hoàn toàn khi lái động cơ. Bạn cũng sẽ so sánh vai trò công tắc đơn của 2N2222 với mạch cầu H TB6612, đồng thời tính được tổn hao nhiệt để giải thích vì sao không được cấp 12 V vào chân 5 V của ESP32.

## Cần có gì trước

Bạn đã biết xác định catot của diode bằng vạch sơn và sử dụng thang đo diode trên linh kiện không cấp nguồn. Bạn cũng nhớ chân GPIO chỉ chịu dòng khoảng 12 mA đến 40 mA trong khi động cơ TT khi kẹt kéo dòng cỡ ampe. Bài này tập trung vào kỹ năng nhận dạng vỏ linh kiện cùng hai yếu tố tránh cháy hỏng: đúng thứ tự chân và kiểm soát công suất tỏa nhiệt.

---

Nếu vi điều khiển là "bộ não" thì **transistor, MOSFET và IC ổn áp** chính là "cơ bắp và hệ tuần hoàn" của xe robot. Một chân GPIO chỉ đủ sức thắp một đèn LED nhỏ 10 mA, nhưng nhờ một con MOSFET công suất nhỏ bằng hạt đậu, tín hiệu 3,3 V yếu ớt ấy có thể đóng ngắt dòng điện hàng chục ampe cho động cơ! Ngược lại, chọn nhầm một IC ổn áp tuyến tính để hạ trực tiếp pin 8,4 V xuống 3,3 V sẽ biến bo mạch thành một chiếc lò sưởi mini chỉ sau 10 giây.

## Kiến thức cần nhớ: Linh kiện Bán dẫn Công suất và Ổn áp trên Robot

1. **Transistor Lưỡng cực (BJT) vs. MOSFET:** BJT điều khiển bằng *dòng điện* cực Base ($$I_C = \beta I_B$$, sụt áp $$V_{CE(\text{sat})} \approx 0.2\text{–}1\text{ V}$$); MOSFET điều khiển bằng *điện áp* cực Gate ($$V_{GS}$$) với dòng kích gần bằng 0 và điện trở mở $$R_{DS(\text{on})}$$ chỉ vài chục mili-ohm — mát hơn và hiệu quả hơn hẳn cho đóng cắt động cơ.
2. **Cạm bẫy Điện áp Ngưỡng $$V_{GS(\text{th})}$$:** Trong datasheet, $$V_{GS(\text{th})}$$ là mức điện áp MOSFET *mới chớm mở* (dòng chỉ vài trăm $$\mu\text{A}$$), **không phải** mức mở bão hòa hoàn toàn! Với GPIO 3,3 V, phải chọn **Logic-Level MOSFET** có thông số $$R_{DS(\text{on})}$$ được đặc tả ngay tại $$V_{GS} = 2.5\text{–}3.3\text{ V}$$.
3. **Ổn áp Tuyến tính (LDO như AMS1117) vs. Ổn áp Xung (Buck Converter):** LDO đốt toàn bộ phần điện áp dư $$(V_{\text{in}} - V_{\text{out}}) \cdot I$$ thành nhiệt; Buck đóng ngắt cuộn cảm ở tần số cao đạt hiệu suất $$85\text{–}95\%$$, bắt buộc dùng khi chênh lệch áp lớn hoặc dòng tải cao.

### Ví dụ làm từng bước: So sánh tỏa nhiệt giữa LDO tuyến tính và mạch Buck ở dòng 0,4 A

Giả sử bạn hạ nguồn pin Li-ion 2S đầy ($$V_{\text{in}} = 8.4\text{ V}$$) xuống $$V_{\text{out}} = 3.3\text{ V}$$ để nuôi ESP32 + cảm biến ăn dòng $$I = 0.4\text{ A}$$ (công suất hữu ích $$P_{\text{out}} = 3.3 \times 0.4 = \mathbf{1.32\text{ W}}$$):

| Loại mạch ổn áp | Công suất tỏa nhiệt $$P_{\text{nhiệt}}$$ | Hiệu suất $$\eta$$ | Hậu quả thực tế trên bàn lab |
|---|---|---|---|
| **LDO tuyến tính (AMS1117-3.3)** | $$(8.4 - 3.3) \times 0.4 = \mathbf{2.04\text{ W}}$$ | $$\dfrac{3.3}{8.4} = \mathbf{39.3\%}$$ | Vỏ SOT-223 nóng vọt quá $$120^\circ\text{C}$$ → tự ngắt nhiệt hoặc cháy! |
| **Mạch hạ áp xung Buck ($$\eta = 90\%$$)** | $$1.32 \times \left(\dfrac{1}{0.90} - 1
ight) = \mathbf{0.147\text{ W}}$$ | **$$90\%$$** | Mát hơn **14 lần** — chạm tay chỉ hơi ấm nhẹ! |

### Giải thích: 4 bước chọn đúng linh kiện bán dẫn cho robot

1. **Bước 1 — Đọc kỹ dạng vỏ (TO-92, TO-220, SOT-23, SOT-223):** Dạng vỏ quyết định khả năng thoát nhiệt tối đa — cùng là ổn áp 3,3 V nhưng vỏ TO-220 chịu nhiệt tốt hơn vỏ SOT-23 gấp nhiều lần.
2. **Bước 2 — Luôn tra $$R_{DS(\text{on})}$$ tại đúng điện áp GPIO (3,3 V):** Nếu datasheet chỉ ghi $$R_{DS(\text{on})}$$ tại $$V_{GS} = 10\text{ V}$$ (như IRF540N cổ điển), cắm vào ESP32 3,3 V sẽ làm MOSFET mở lửng, nóng rực và động cơ quay yếu.
3. **Bước 3 — Dùng IC cầu H tích hợp (TB6612FNG / DRV8833) thay vì tự ráp 4 transistor rời:** IC tích hợp sẵn mạch bảo vệ chống ngắn mạch chéo (*shoot-through*), diode dập xung và chân điều khiển PWM gọn gàng.
4. **Bước 4 — Dùng Buck cho tầng hạ áp lớn, LDO cho tầng lọc sạch cuối:** Hạ 8,4 V → 5,0 V bằng Buck rồi dùng LDO tích hợp trên bo ESP32 hạ 5,0 V → 3,3 V là công thức tối ưu cả hiệu suất lẫn độ sạch nhiễu!

**Kiểm tra nhanh.** Nếu LDO trên bo ESP32 hạ từ $$5.0\text{ V}$$ (đầu ra Buck) xuống $$3.3\text{ V}$$ ở dòng $$0.25\text{ A}$$, công suất nhiệt trên LDO còn bao nhiêu? Chỉ $$(5.0 - 3.3) \times 0.25 = \mathbf{0.425\text{ W}}$$ — hoàn toàn nằm trong ngưỡng an toàn của vỏ SOT-223!

---

## Vì sao xe hai bánh không dùng transistor rời để lái động cơ

Mạch ESP32 tích hợp sẵn IC ổn áp AMS1117-3.3 (hoặc tương đương) giữa nguồn USB 5 V và đường nguồn 3,3 V; Raspberry Pi Pico cũng có mạch ổn áp riêng giữa VBUS và 3V3. Nhờ đó vi điều khiển xuất mức logic 3,3 V tương thích với dải logic 2,7 V đến 5,5 V của TB6612. Tuy nhiên, sự có mặt của ổn áp trên mạch không đồng nghĩa bạn được phép đưa nguồn pin 12 V vào chân 5 V của board.

Nhiều người mới nghĩ có thể dùng một transistor nhỏ làm công tắc bật/tắt động cơ TT trực tiếp từ chân GPIO. Thực tế, động cơ là tải cảm nên khi khóa ngắt bắt buộc phải có diode hồi tiếp, và dòng kẹt của động cơ TT dễ vượt quá giới hạn chịu dòng của 2N2222. Ngay cả với MOSFET, nếu chọn loại có ngưỡng $V_{GS(th)}$ quanh 2 V thì ở mức điều khiển 3,3 V kênh dẫn vẫn có thể chỉ mở một phần, gây nóng và sụt áp. Module TB6612 giải quyết trọn vẹn bài toán này cho hai kênh độc lập (1,2 A liên tục, 3,2 A đỉnh). Bài học này giúp bạn nhận biết chính xác các họ vỏ linh kiện để tránh cắm nhầm IC ổn áp vào vị trí transistor.

## Vỏ linh kiện và nguyên tắc đọc ký hiệu trên thân

TO-92 là dạng vỏ nhựa đen ba chân cỡ nhỏ, còn TO-220 là dạng vỏ công suất lớn hơn có tai kim loại bắt tản nhiệt. Rất nhiều loại linh kiện khác nhau dùng chung hai chuẩn vỏ này: 2N2222, BC547 và 2N3904 đều là transistor lưỡng cực NPN nhưng có thứ tự chân khác nhau — ngay cả cặp cùng họ nổi tiếng là P2N2222 và 2N2222 cũng đảo thứ tự chân cho nhau. Trong khi đó, AMS1117 và 7805 là IC ổn áp chứ không phải transistor đóng cắt. Nếu đấu một MOSFET vỏ TO-92 theo sơ đồ chân học thuộc của 2N2222, linh kiện sẽ hỏng ngay lập tức.

![Nhiều vỏ cùng bóng dáng nhưng không cùng sơ đồ chân]({{ site.imgurl }}/generated/component_lookalikes.png)

Nguyên tắc bắt buộc là luôn đọc rõ ký hiệu in trên mặt phẳng của thân linh kiện rồi mở đúng datasheet tương ứng. Nếu chữ in bị mờ không đọc được, hãy xếp vào nhóm chưa xác định và tuyệt đối không cắm thử lên chân GPIO đang có điện.

Đối với IC vỏ **DIP** (hai hàng chân song song), bạn đặt đầu có rãnh khuyết hoặc dấu chấm hướng lên trên: chân số 1 nằm ở góc trên bên trái, sau đó đánh số tăng dần xuống hết cạnh trái rồi vòng lên hết cạnh phải (theo chiều ngược kim đồng hồ khi nhìn từ mặt trên). Quy tắc này cũng rất hữu ích khi bạn lắp các IC chuyển mức logic bắc ngang rãnh giữa breadboard.

## Transistor lưỡng cực, MOSFET và hiểu lầm về $V_{GS(th)}$

**Transistor lưỡng cực NPN** khi làm việc như công tắc cần có dòng điều khiển đi vào cực bazơ (thường chọn khoảng 1/10 dòng colectơ) qua một điện trở từ chân GPIO. Với tải 150 mA, dòng bazơ cần khoảng 15 mA — đã sát ngưỡng khuyến nghị của GPIO. Nếu động cơ kẹt ở 800 mA, dòng bazơ tương ứng lên tới ~80 mA, vượt xa khả năng cấp dòng của GPIO lẫn giới hạn của chính 2N2222. Ngoài ra, khi transistor ngắt đột ngột, cuộn dây động cơ sinh xung áp ngược nên bắt buộc phải mắc diode hồi tiếp (vạch catot hướng về cực dương nguồn động cơ) để bảo vệ cực colectơ.

**MOSFET** hoạt động theo nguyên lý điều khiển bằng điện áp đặt lên cực cổng (gate) thay vì duy trì dòng liên tục. Khi đóng cắt thông thường, cực cổng gần như không rút dòng tĩnh; điện trở kênh dẫn $R_{DS(on)}$ phụ thuộc vào mức điện áp cổng so với cực nguồn ($V_{GS}$). Cần đặc biệt lưu ý: thông số điện áp ngưỡng $V_{GS(th)}$ trên datasheet chỉ là mốc mà tại đó MOSFET *bắt đầu* dẫn một dòng thử rất nhỏ (thường khoảng 250 µA), **không phải** mức điện áp để MOSFET dẫn bão hòa hoàn toàn. Nhiều MOSFET ghi $V_{GS(th)}$ trong khoảng 2–4 V nhưng chỉ đảm bảo $R_{DS(on)}$ thấp tại $V_{GS} = 4{,}5\ \mathrm{V}$ hoặc $10\ \mathrm{V}$. Nếu điều khiển cực cổng chỉ ở mức "vừa qua ngưỡng" (như 3,3 V), MOSFET sẽ rơi vào vùng tuyến tính, gây sụt áp lớn, tỏa nhiệt mạnh và làm động cơ chạy yếu.

**MOSFET mức logic (logic-level MOSFET)** là loại được nhà sản xuất công bố $R_{DS(on)}$ thấp ngay ở mức $V_{GS}$ nhỏ (như 2,5 V hoặc 4,5 V). Dù vậy, dùng một MOSFET rời làm khóa phía thấp cho động cơ TT vẫn chỉ quay được một chiều và vẫn cần diode hồi tiếp. Vì robot cần điều khiển hai động cơ quay thuận/nghịch bằng PWM, ta dùng mạch cầu H tích hợp sẵn MOSFET là TB6612 thay vì tự ráp mảng transistor rời trên breadboard.

## IC ổn áp tuyến tính và công suất tỏa nhiệt

Các IC ổn áp tuyến tính như 7805 duy trì điện áp đầu ra cố định 5 V bằng cách tiêu tán toàn bộ phần chênh lệch điện áp thành nhiệt năng. Công suất tỏa nhiệt trên ổn áp được tính bằng:

$$
P = (V_\mathrm{in} - V_\mathrm{out}) \, I
$$

Xét trường hợp nhẹ với nguồn vào 9 V, đầu ra 5 V và dòng tải 200 mA:

$$
P = (9 - 5) \times 0.2 = 0.8\ \mathrm{W}
$$

Vỏ TO-220 có tai kim loại tản nhiệt có thể chịu được mức 0,8 W này (vỏ sẽ hơi ấm). Bây giờ, xét tình huống đưa 12 V vào chân 5 V của mạch ESP32 (nơi IC ổn áp AMS1117-3.3 hạ xuống 3,3 V ở dòng tải 150 mA khi bật Wi-Fi):

$$
P = (12 - 3.3) \times 0.15 \approx 1.3\ \mathrm{W}
$$

Công suất 1,3 W là quá lớn đối với vỏ SOT-223 nhỏ gắn trên một mạch in mỏng. Nguy hiểm hơn, trên nhiều mạch phát triển, chân ghi 5V nối chung trực tiếp với đường 5 V của cổng USB và chip giao tiếp UART, nên cấp 12 V vào đó có thể phá hủy cả chip UART lẫn cổng USB. Giới hạn điện áp vào tối đa ghi trên datasheet riêng của AMS1117 không bảo vệ phần còn lại của mạch. Do đó trên bàn lab, hãy luôn cấp nguồn ESP32/Pico qua USB, còn pin động cơ chỉ nối vào chân VM của TB6612 (4,5–10 V) và nối chung mass.

## Ví dụ: phân loại bằng ký hiệu trước khi đo kiểm tiếp giáp

Giả sử trên khay có bốn linh kiện không thể phân biệt chỉ qua dáng vỏ: TO-92 ghi `BC547`, TO-92 ghi `2N2222`, TO-220 ghi `7805` và một MOSFET có ký hiệu đọc rõ. Ta phân loại ngay được: BC547 và 2N2222 thuộc họ transistor NPN (nhưng khác thứ tự chân), 7805 là IC ổn áp tuyến tính 5 V, và linh kiện cuối là MOSFET điều khiển bằng điện áp. Tuy nhiên, việc gọi tên họ vẫn chưa đủ để biết chân nào là cực phát (emitter) — bắt buộc phải mở đúng datasheet theo mã in trên thân.

Khi linh kiện rời ngoài mạch và không cấp nguồn, thang đo diode trên đồng hồ có thể dùng để kiểm tra nhanh tình trạng tiếp giáp của transistor lưỡng cực (chứ không thay thế datasheet để chốt sơ đồ chân). Hai tiếp giáp bazơ–phát (B–E) và bazơ–góp (B–C) hoạt động giống hai diode, cho điện áp thuận quanh 0,6 V ở một chiều và `OL` ở chiều ngược lại; đường phát–góp (E–C) không được thông mạch cả hai chiều. Chân dùng chung cho cả hai tiếp giáp thuận là ứng viên cực bazơ. Phép đo này rất hữu ích để phát hiện nhầm lẫn: nếu một linh kiện vỏ ba chân không cho kết quả hai tiếp giáp diode như trên, rất có thể đó là một IC ổn áp như 7805 chứ không phải transistor.

Dù đã kiểm tra tốt một con 2N2222, bạn vẫn không dùng nó để kéo động cơ TT trên xe đồ án; việc đảo chiều và hãm động cơ cần cầu H TB6612 chịu 1,2 A liên tục, 3,2 A đỉnh và nhận trực tiếp logic 3,3 V.

## Thực hành

1. Nếu có sẵn các linh kiện rời, hãy phân loại chúng theo chữ in trên thân thành bốn nhóm: transistor lưỡng cực, MOSFET, IC ổn áp và chưa xác định. Nếu chưa có linh kiện rời, thực hiện phân loại tương tự dựa trên các hình minh họa trong bài và các IC hàn sẵn trên board trong bộ kit.
2. Quan sát bất kỳ IC vỏ DIP nào bạn có (hoặc trong hình): tìm rãnh khuyết hoặc dấu chấm, xác định chân số 1 và đọc thứ tự chạy xuống cạnh trái rồi vòng lên cạnh phải.
3. Trên mạch ESP32, tìm IC ổn áp 3,3 V (thường thuộc họ AMS1117) nằm gần cổng USB; xác định vị trí ký hiệu in lụa của chân `5V` và chân `3V3` (tuyệt đối không cấp 12 V để thử).
4. Ở trạng thái mất nguồn và linh kiện rời ngoài mạch, dùng thang đo diode kiểm tra một diode đã biết và một transistor lưỡng cực đã biết (nếu có) rồi ghi lại hai giá trị tiếp giáp. Nếu chưa có transistor rời, bỏ qua bước đo và giữ nguyên bảng phân loại ở bước 1; không đo thang diode trên linh kiện đang hàn trên mạch có điện.

**Kết quả kỳ vọng:** Bạn hoàn thành bảng phân loại linh kiện có ghi rõ mã và họ (không quay động cơ trong bài này). Phép đo diode trên transistor lưỡng cực tốt cho điện áp khoảng 0,5–0,7 V trên hai tiếp giáp chung một chân và không chập giữa hai chân còn lại; IC ổn áp 7805 sẽ không cho kết quả giống như vậy.

| Hiện tượng quan sát | Nguyên nhân thường gặp | Cách khắc phục |
| --- | --- | --- |
| Hai linh kiện vỏ TO-92 nhưng cắm chung sơ đồ chân không chạy | Khác mã linh kiện, hoặc nhầm cặp 2N2222 với P2N2222 | Đọc chính xác mã in trên thân và tra đúng datasheet từng loại |
| Thang diode báo ngắn mạch cả hai chiều trên mọi chân | Linh kiện đã hỏng, hoặc đang đo khi còn hàn trên mạch có nhánh song song | Tháo linh kiện ra khỏi mạch; nếu vẫn chập thì loại bỏ |
| IC ổn áp nóng gắt khi cấp 12 V vào chân 5 V | Tổn hao nhiệt tuyến tính lớn và quá áp trên đường nguồn USB | Ngắt nguồn 12 V ngay; cấp nguồn board bằng USB và nối pin động cơ riêng vào VM |
| Cực cổng MOSFET nguội nhưng động cơ quay yếu và thân FET rất nóng | Điện áp $V_{GS}$ chỉ gần mức ngưỡng $V_{GS(th)}$ nên kênh chưa dẫn bão hòa | Dùng mạch lái chuyên dụng TB6612 thay vì điều khiển MOSFET rời ở vùng ngưỡng |

**Lưu ý an toàn:** Không cấp nguồn động cơ hay nguồn 12 V trong bài thực hành này; chỉ dùng thang đo diode trên linh kiện rời. Trên các mạch đã cấp điện về sau, cần cẩn thận vì tai kim loại của vỏ TO-220 có thể vừa nóng vừa nối trực tiếp với một chân điện bên trong.

## Video tham khảo

- **Xem trước:** [MOSFET Explained - How MOSFET Works](https://www.youtube.com/watch?v=AwRJsze_9m4) — The Engineering Mindset, tiếng Anh. Giải thích nguyên lý điều khiển kênh dẫn bằng cực cổng của MOSFET; lưu ý đây mới là linh kiện đóng cắt đơn, chưa phải mạch cầu H.

## Bài tập

1. Trên một IC vỏ DIP có rãnh khuyết, khi nhìn từ mặt trên với rãnh hướng lên trên, chân số 1 nằm ở đâu và thứ tự chân chạy theo chiều nào?
2. Một datasheet MOSFET ghi $V_{GS(th)}$ từ 2 V đến 4 V tại dòng thử $250\ \mu\mathrm{A}$, nhưng thông số $R_{DS(on)}$ chỉ được công bố tại $V_{GS} = 10\ \mathrm{V}$. Vì sao không thể lập luận "ngưỡng chỉ 2 V nên chân GPIO 3,3 V kéo động cơ thoải mái"?
3. Tính công suất tỏa nhiệt của IC ổn áp 7805 khi hạ áp từ 12 V xuống 5 V ở dòng tải 300 mA. Vỏ TO-220 trong trường hợp này có cần gắn thêm tản nhiệt không?
4. Có người đề xuất dùng 2N2222 làm công tắc phía thấp cho động cơ TT có dòng kẹt 0,8 A, chọn dòng bazơ bằng 1/10 dòng colectơ lấy trực tiếp từ chân GPIO. Hãy tính dòng bazơ yêu cầu và nêu linh kiện bảo vệ còn thiếu khi transistor ngắt.
5. Vì sao một linh kiện vỏ TO-92 bị mờ mất chữ còn nguy hiểm hơn cả việc không có linh kiện thay thế nếu định dùng nó thay cho ổn áp 3,3 V của ESP32?

<details>
<summary>Gợi ý đáp án</summary>

1. Chân số 1 nằm ở góc trên bên trái ngay cạnh rãnh khuyết; số chân tăng dần xuống cạnh trái rồi vòng lên cạnh phải (ngược chiều kim đồng hồ khi nhìn từ trên xuống).
2. Điện áp ngưỡng $V_{GS(th)}$ chỉ là mốc bắt đầu dẫn dòng rất nhỏ (250 µA). Việc $R_{DS(on)}$ chỉ đảm bảo ở 10 V cho thấy ở mức 3,3 V, MOSFET có thể chỉ mở một phần, tỏa nhiệt mạnh và gây sụt áp lớn khiến động cơ chạy yếu. Cần MOSFET mức logic phù hợp, và tốt nhất cho xe hai bánh vẫn là dùng mạch lái TB6612.
3. $P = (12 - 5) \times 0{,}3 = 2{,}1\ \mathrm{W}$. Bắt buộc phải gắn tản nhiệt vì vỏ TO-220 trần tỏa trên 2 W sẽ rất nóng, dễ gây bỏng; đồng thời đây cũng không phải cách hợp lý để cấp nguồn cho ESP32.
4. Dòng bazơ yêu cầu khoảng $0{,}8 / 10 = 80\ \mathrm{mA}$, vượt xa giới hạn 12–40 mA của chân GPIO. Ngoài ra mạch còn thiếu diode hồi tiếp mắc song song động cơ. Giải pháp đúng là dùng TB6612.
5. Một linh kiện TO-92 không rõ mã có thể là transistor lưỡng cực, MOSFET hoặc ổn áp sai mức điện áp và sai thứ tự chân; lắp thay thế bừa có thể đẩy thẳng 5 V lên đường nguồn 3,3 V làm hỏng chip ESP32.

</details>

## Đọc thêm

Bài hướng dẫn của SparkFun giải thích rõ nguyên lý transistor lưỡng cực và MOSFET: [Transistors](https://learn.sparkfun.com/tutorials/transistors). Trang sản phẩm của Texas Instruments cung cấp đầy đủ đặc tính nhiệt và điện áp của họ ổn áp 7805: [LM7805](https://www.ti.com/product/LM7805). Luôn đọc mã in thực tế trên linh kiện của bạn trước khi tra sơ đồ chân.

## Mua ở Việt Nam

Bạn không cần mua transistor rời để hoàn thành xe vi sai vì phần đóng cắt đã có mạch lái TB6612 trong danh sách [BOM và cách mua bộ kit robot ở Việt Nam]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %}).

Nếu muốn mua thêm một diode và một transistor lưỡng cực rõ mã để thực hành bài đo tiếp giáp không nguồn, nên chọn mua tại các cửa hàng linh kiện dán nhãn mã đầy đủ như [Thế Giới IC](https://www.thegioiic.com/) hoặc [IC Đây Rồi](https://icdayroi.com/), hoặc tra cứu qua trang tìm kiếm [Shopee, tìm 2N2222](https://shopee.vn/search?keyword=2N2222) rồi kiểm tra kỹ chữ in khi nhận hàng. Mạch phát triển ESP32 (tích hợp sẵn ổn áp 3,3 V) có giá tham khảo 190.000 ₫ trên Hshop ngày 23 tháng 9 năm 2026: [ESP32 NodeMCU-32S](https://hshop.vn/kit-rf-thu-phat-wifi-ble-esp32-nodemcu-32s-ch340-ai-thinker).
