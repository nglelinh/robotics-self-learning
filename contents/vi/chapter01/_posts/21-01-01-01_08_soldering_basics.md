---
layout: post
title: "Hàn dây và header cho robot"
chapter: "01"
order: 8
owner: "Nguyen Le Linh"
lang: vi
categories:
  - chapter01
lesson_type: required
draft: false
---

Trong phạm vi khóa học này, một mối hàn đạt yêu cầu là sợi dây động cơ vẫn dẫn điện tốt và ổn định sau khi khung xe rung lắc trong quá trình chạy. Bạn sẽ học cách tráng thiếc dây lõi bện, hàn vào chân header hoặc pad mạch thử, rồi bọc bảo vệ để lực uốn rơi vào phần vỏ dây chứ không dồn lên mối thiếc. Một mối hàn trông bóng bẩy nhưng nứt gãy ngay lần chạy thử đầu tiên vẫn là mối hàn hỏng.

## Mục tiêu

Sau bài học này, bạn sẽ thực hiện đúng trình tự hàn chuẩn: làm nóng đồng thời pad và chân linh kiện, đưa thiếc vào mối nóng, rút dây thiếc trước rồi mới rút mũi mỏ hàn. Bạn sẽ nhận diện được mối hàn đạt chuẩn (hình nón lõm, bề mặt bóng, bám ướt đều cả hai mặt) và phân loại các lỗi thường gặp (mối tròn thành cục, mối nguội xỉn sần, cầu thiếc, bong pad đồng và cháy vỏ dây). Bạn sẽ giải thích được lý do hợp kim thiếc chì 60/40 hoặc Sn63 phù hợp cho thao tác hàn cơ bản (kèm thông gió tốt) cùng vai trò thực sự của nhựa thông (flux). Bạn cũng sẽ biết cách bọc gen co nhiệt, tạo vòng giảm lực kéo cho dây động cơ TT, tránh tráng thiếc vào đầu bấm Dupont, và kiểm tra mối hàn tập bằng thang thông mạch kèm ảnh chụp đối chiếu.

## Kiến thức cần có

Bạn đã biết sử dụng thang thông mạch từ bài 02 và phân biệt được hai đầu của thanh header. Buổi thực hành này chỉ dùng dây và mạch thử bỏ đi (có thể đặt tờ sơ đồ chân bài 07 bên cạnh để tham khảo), tuyệt đối không đặt khung xe hay pin lithium lên bàn. Hãy đọc kỹ mục An toàn trước khi cắm điện mỏ hàn.

---

Dây cắm breadboard rất tuyệt để thử nghiệm trong 10 phút, nhưng ngay khi xe robot chạy qua khe gạch trên sàn nhà, rung động cơ học sẽ làm dây tiếp xúc chập chờn và tạo ra những lỗi ma quái không thể tái hiện! **Kỹ năng hàn thiếc (Soldering)** tạo ra liên kết luyện kim bền vững giữa dây đồng và pad mạch in — và bí mật của một mối hàn bóng đẹp nằm ở **truyền nhiệt đúng thứ tự**, chứ không phải bôi thật nhiều thiếc.

## Kiến thức cần nhớ: Vật lý Luyện kim của Mối hàn Điện tử

1. **Cơ chế Liên kết Luyện kim (Intermetallic Bond):** Thiếc hàn không phải là "keo dán" — khi cả chân linh kiện và pad đồng đạt nhiệt độ nóng chảy (~$$183^\circ\text{C}$$ với thiếc chì 63/37 hoặc ~$$217^\circ\text{C}$$ với thiếc không chì SAC305), hợp kim thiếc hòa tan bề mặt đồng tạo thành lớp nối điện–cơ bền chắc.
2. **Vai trò của Nhựa thông (Flux):** Bề mặt đồng luôn có lớp oxit ngăn thiếc bám dính. Lõi nhựa thông (flux) bên trong cuộn thiếc bay hơi và khử lớp oxit ngay tại khoảnh khắc nung nóng — giữ mỏ hàn quá lâu làm cháy hết flux sẽ tạo ra **mối hàn nguội** xỉn màu, nứt gãy.
3. **Giảm lực kéo cơ học (Strain Relief):** Dây đồng nhiều sợi rất dễ gãy ngay sát chân mối hàn cứng khi bị uốn lặp đi lặp lại; ống co nhiệt (heat-shrink) và kẹp cố định dây bảo vệ mối hàn sống sót qua hàng trăm giờ chạy xe.

### Ví dụ làm từng bước: Tính sụt áp và tỏa nhiệt trên một mối hàn nguội (Cold Joint)

Giả sử dây nguồn cấp cho cặp động cơ robot kéo dòng $$I = 2.0\text{ A}$$ đi qua một mối hàn nối dây:
- **Mối hàn đạt chuẩn (bóng mượt, hình nón lõm):** điện trở tiếp xúc chỉ $$R_{\text{tốt}} = 0.01\ \Omega$$:
  - Sụt áp: $$\Delta V = 2.0 \times 0.01 = \mathbf{0.02\text{ V}}$$ (không đáng kể).
  - Công suất nhiệt: $$P = 2.0^2 \times 0.01 = \mathbf{0.04\text{ W}}$$ (hoàn toàn mát lạnh).
- **Mối hàn nguội / dính oxit (xỉn, vón cục):** điện trở tiếp xúc tăng vọt lên $$R_{\text{nguội}} = 0.8\ \Omega$$:
  - Sụt áp: $$\Delta V = 2.0 \times 0.8 = \mathbf{1.6\text{ V}}$$ (xe đột ngột mất lực hoặc reset!).
  - Công suất nhiệt dồn tại đúng hạt thiếc nhỏ: $$P = 2.0^2 \times 0.8 = \mathbf{3.2\text{ W}}$$ — đủ làm chảy vỏ nhựa và bong mạch đồng!

### Giải thích: Quy trình 4 bước tạo mối hàn chuẩn công nghiệp

1. **Bước 1 — Lau sạch mũi hàn và tráng một lớp thiếc mỏng (tinning):** Mũi hàn đen bị oxy hóa không truyền nhiệt được; một giọt thiếc tươi trên đầu mũi giúp truyền nhiệt sang pad nhanh gấp nhiều lần.
2. **Bước 2 — Chạm mũi hàn vào *cả* pad đồng và chân linh kiện (1–2 giây):** Làm nóng bề mặt cần hàn trước, tuyệt đối không nhỏ thiếc lên đầu mũi hàn rồi quệt sang!
3. **Bước 3 — Đưa sợi thiếc vào phía đối diện của chân linh kiện:** Thiếc sẽ tự chảy mượt bao quanh chân thành hình chóp núi lửa lõm (concave fillet); rút dây thiếc trước, rồi mới nhấc mũi hàn ra.
4. **Bước 4 — Giữ bất động 2 giây và kiểm tra bằng mắt + lực kéo nhẹ:** Mối hàn tốt phải bóng, mượt, không có gai nhọn và chịu được lực kéo nhẹ bằng tay không bong.

**Kiểm tra nhanh.** Nếu bạn thấy mối hàn bị vón thành hình quả cầu tròn ngồi lên trên pad đồng (chân linh kiện không dính xuống pad), lỗi xảy ra ở bước nào? Bạn đã chỉ làm nóng chân linh kiện (hoặc nhỏ thiếc lên mũi hàn) mà **chưa làm nóng đủ pad đồng** — chỉ cần thêm chút nhựa thông và chạm mũi hàn đều vào cả pad lẫn chân trong 2 giây, thiếc sẽ tự kéo mượt xuống pad!

---

## Vì sao bài này quan trọng

Xe Capstone điều khiển hai động cơ TT qua TB6612 bằng nguồn pin riêng. Các sợi dây nối ra cặp chân `AO1`/`AO2` và `BO1`/`BO2` thường xuyên bị uốn cong tại các điểm cố định trên khung. Một mối hàn nguội vẫn có thể kêu bíp khi đo thông mạch không tải, nhưng lại gây sụt áp đáng kể khi bánh xe kẹt, khiến xe chạy lệch hướng dù hai bánh nhận cùng mức PWM. Tương tự, ở cụm dây cảm biến HC-SR04, mối hàn kém chất lượng khiến dây echo 5 V chạm sang chân 3,3 V bên cạnh sẽ gây hỏng nặng hơn cả đứt dây. Dây Dupont chỉ dùng trên breadboard, còn đường động cơ cần mối hàn chuẩn, bọc gen co nhiệt và có vòng dây chùng giảm lực kéo.

![Mỏ cắm điện phải có đế ngay khi nóng]({{ site.imgurl }}/wikimedia/Soldering_iron.jpg)

Bức ảnh trên minh họa phần dụng cụ chứ chưa phải thao tác chuẩn. Do mỏ hàn 60 W phổ thông không có núm chỉnh nhiệt độ, bạn kiểm soát nhiệt lượng bằng chính thời gian tiếp xúc giữa mũi mỏ và đồng. Giá đỡ mỏ hàn giúp giữ mũi nóng tách biệt khỏi sổ ghi chép, dây điện và tay bạn mỗi khi cần lấy thiếc.

![Mối lõm bóng đặt cạnh cục thiếc]({{ site.imgurl }}/generated/solder_joint_compare.png)

Hãy dùng hình trên làm chuẩn đối chiếu cho bài lab: mối hàn đạt (bên tốt) có dạng hình nón hơi lõm, bề mặt sáng bóng với thiếc chì, bám ướt đều cả pad lẫn chân và vẫn thấy rõ dáng chân linh kiện; mối loại là dạng giọt cầu tròn hoặc khối đục sần. Lưu ý rằng tiếng bíp thông mạch không thể biến một mối hàn xấu thành mối đạt.

## Quy trình hàn: làm nóng, đưa thiếc rồi rút ra

Trước hết, làm sạch mũi mỏ hàn đến khi sáng rồi tráng một lớp thiếc mỏng lên đầu mũi; lớp thiếc này tạo cầu dẫn nhiệt vào mối hàn (mũi bị đen ôxy hóa chỉ làm cháy flux chứ không truyền nhiệt tốt). Vì mỏ hàn 60 W cắm trực tiếp nóng hơn mức cần thiết của pad header, thời gian chạm mũi là yếu tố quyết định — thông thường chỉ từ 1 đến 3 giây; tì mũi mỏ quá lâu (chẳng hạn 10 giây) sẽ làm bong tróc lớp đồng pad nhỏ.

Đặt mũi mỏ hàn chạm đồng thời cả pad đồng và chân linh kiện để cả hai nóng lên cùng lúc. Đưa dây thiếc vào góc tiếp giáp giữa pad và chân (không lấy sẵn một giọt thiếc trên mũi mỏ rồi chấm sang). Thiếc phải chảy ra nhờ sức nóng từ pad và chân đồng; nếu thiếc chỉ chảy khi chạm vào mũi mỏ thì pad vẫn còn nguội. Khi thiếc đã chảy đều bám ướt cả hai mặt, **rút dây thiếc ra trước**, sau đó mới **rút mỏ hàn ra**. Không thổi hơi để làm nguội nhanh và giữ tuyệt đối cố định dây trong vài giây cho tới khi thiếc đông hoàn toàn — mọi rung lắc lúc thiếc đang đông đều tạo vết nứt ngầm.

**Nhựa thông (flux)** giúp làm sạch lớp ôxy hóa để thiếc loang đều thay vì vo tròn. Dây thiếc lõi nhựa thông đã tích hợp sẵn một phần, nhưng với pad bị xỉn màu, bạn có thể chấm thêm một chút mỡ hàn. Với sản phẩm `RELIFE RL-426A` ở mục mua hàng bên dưới, lưu ý đường dẫn web có chữ `mo-han` (trùng cách viết không dấu của "mỏ hàn" và "mỡ hàn"), nên hãy đọc kỹ tên sản phẩm trước khi đặt.

Hợp kim thiếc chì Sn63/Pb37 và 60/40 nóng chảy quanh mức $$183^\circ\mathrm{C}$$, thấp hơn đáng kể so với thiếc không chì (khoảng $$217^\circ\mathrm{C}$$ và khó bám ướt hơn khi dùng mỏ không chỉnh nhiệt). Với thực hành cơ bản, thiếc chì dễ thao tác hơn miễn là bạn đảm bảo thông gió tốt và rửa sạch tay sau khi hàn. Khói flux gây kích ứng đường hô hấp nên hãy đặt quạt nhỏ thổi ngang bàn hoặc mở cửa sổ, đồng thời luôn đeo kính bảo hộ phòng trường hợp flux nóng bắn ra.

## Cách nhận diện chất lượng mối hàn

- **Mối hàn đạt:** hình nón lõm gọn, thiếc loang đều bám sát vào cả pad đồng lẫn chân linh kiện (không có khe rãnh tách rời), bề mặt mịn bóng (với Sn63 hoặc 60/40) và vẫn nhận ra dáng chân kim loại bên trong.
- **Mối hàn nguội:** bề mặt đục và sần sùi như cát, do pad chưa đủ nóng hoặc dây bị xê dịch trong lúc thiếc đang đông.
- **Không bám ướt (vo cục):** thiếc cuộn tròn thành giọt cầu, thường để lộ phần đồng trần xung quanh chân.
- **Cầu thiếc:** thiếc chảy tràn nối chập hai chân kề nhau (ví dụ nối nhầm `PWMA` với chân bên cạnh).
- **Bong pad đồng:** lá đồng bị tách khỏi phíp mạch do giữ nhiệt quá lâu hoặc giật dây lúc thiếc chưa đông. Trên mạch thử đây là bài học kinh nghiệm, nhưng trên module TB6612 sẽ làm hỏng cả mạch.
- **Cháy vỏ dây:** mũi mỏ chạm vào vỏ nhựa cách điện; dù lõi đồng còn thông mạch nhưng dây rất dễ đứt gãy ngay tại vị trí vỏ bị chảy.

Khi sửa một mối hàn xấu, hãy hút bỏ lớp thiếc cũ trước chứ không đắp thêm thiếc mới. Dùng bơm hút thiếc khi mối đang chảy lỏng để lấy phần thừa ra, chấm thêm chút flux rồi hàn lại gọn gàng một lần; tuyệt đối không dùng kìm hay mũi mỏ cạy mối thiếc đã đông cứng khỏi pad.

Với đường dòng động cơ, hình dạng mối hàn ảnh hưởng trực tiếp đến thông số điện. Một mối hàn kém bám ướt chỉ có điện trở vài phần mười ôm vẫn kêu bíp ở thang thông mạch, nhưng khi gặp dòng kẹt sẽ gây sụt áp rõ rệt:

$$
V_{\mathrm{sut}} = I \times R_{\mathrm{moi}}
$$

Chẳng hạn, một mối hàn lỗi có điện trở $$0{,}4\,\Omega$$ ở dòng $$1{,}2\,\mathrm{A}$$ sẽ làm sụt gần nửa vôn và tỏa khoảng nửa oát nhiệt ngay trên hạt thiếc, khiến một bên động cơ yếu hơn bên kia và xe chạy lệch dù chương trình không hề sai.

## Giảm lực kéo và lưu ý với đầu bấm Dupont

Do dây động cơ thường xuyên rung và uốn, mối hàn không được chịu lực cơ học trực tiếp. Hãy tuốt khoảng vài milimét vỏ dây, xoắn gọn lõi bện và tráng thiếc một đoạn ngắn vừa bằng chiều dài pad. **Luồn sẵn ống gen co nhiệt** vào dây trước khi hàn; sau khi hàn xong, kéo gen co bọc kín mối hàn lẫn một đoạn vỏ nhựa rồi hơ nóng nhẹ bằng thân mỏ để gần (không chạm trực tiếp làm thủng ống). Cố định thêm một vòng dây chùng hoặc dây rút nhựa để lực kéo tác động lên vỏ dây thay vì mối hàn. Nếu quên luồn gen co trước khi hàn vào đầu nối lớn, bạn sẽ phải cắt mối làm lại.

Riêng với **đầu bấm Dupont**, phần tiếp xúc bên trong là một lò xo đàn hồi. Tuyệt đối không tráng thiếc vào đầu dây bấm Dupont, vì thiếc sẽ thấm ngược lên sợi đồng làm mất độ đàn hồi và khiến dây gãy ngay sát mép thiếc sau vài chục lần cắm rút. Đầu bấm cần dùng đúng kìm bấm chuyên dụng, còn hàn thiếc chỉ áp dụng cho pad mạch hoặc chân header cố định.

## An toàn

Mỏ hàn khi cắm điện phải luôn đặt trên giá đỡ. Luôn đeo kính bảo hộ, không vẩy mũi mỏ để hất thiếc thừa mà hãy lau trên bọt biển ẩm hoặc bùi nhùi đồng của giá đỡ. Rút phích cắm ngay khi tạm nghỉ, giữ khu vực hàn xa tầm tay trẻ em và rửa sạch tay sau khi thao tác với thiếc chì. Tuyệt đối không hàn trực tiếp lên vỏ cell pin lithium hay 18650 rời — hãy dùng đế pin đã có sẵn dây nối.

## Thực hành

Thực hành hoàn toàn trên dây và mạch thử rời; cất module driver và mọi loại pin vào ngăn kéo.

1. Chỉ cắm điện mỏ hàn sau khi đã đặt mỏ lên giá đỡ, đeo kính bảo hộ và mở quạt/cửa sổ tạo luồng gió thổi ngang bàn. Ghi lại loại hợp kim thiếc sử dụng (cuộn tiêu chuẩn trong bài là Sn63/Pb37 đường kính 0,8 mm).
2. Làm sạch và tráng một lớp thiếc mỏng lên mũi mỏ đến khi sáng bóng; nếu mũi bị đen ôxy hóa không ăn thiếc, hãy lau sạch trước khi chạm vào mạch.
3. Lấy một đoạn dây lõi bện vụn, tuốt khoảng 3 mm vỏ, xoắn chặt lõi đồng và tráng thiếc thành một bó gọn.
4. Hàn đầu dây đó vào chân header hoặc pad trên mạch thử theo đúng trình tự: làm nóng đồng thời pad và chân, đưa thiếc vào mối, rút dây thiếc trước rồi mới rút mỏ hàn, giữ yên đến khi thiếc đông hẳn.
5. Chụp ảnh cận cảnh mối hàn đặt cạnh hình so sánh (hoặc mở hình mẫu trên điện thoại trong cùng khung hình) để tự đánh giá. Nếu mối bị đục, vo cục hay không bám ướt, dùng bơm hút thiếc lấy ra và làm lại. Nếu lỡ làm bong pad, dừng lại, chuyển sang pad khác và ghi rõ `pad bong` kèm ước lượng thời gian tì mũi vào sổ.
6. Đo thông mạch từ đầu dây tự do sang đầu chân tự do: mối kêu bíp nhưng hình dạng xấu vẫn tính là trượt, và mối trông bóng nhưng hở mạch cũng trượt.
7. Với mối nối giữa hai đoạn dây rời, bổ sung ống gen co nhiệt bảo vệ. Lưu ảnh kết quả với tên `ch01-08-joint`.

Sổ lab cần ghi đủ: loại hợp kim thiếc, đánh giá đối chiếu với hình mẫu, kết quả thông mạch và các lỗi thực tế đã gặp (cầu thiếc, bong pad, không bám ướt, cháy vỏ dây). Các lỗi ghi nhận được là dữ liệu học tập quan trọng; trang sổ chỉ ghi chữ "ok" không đạt yêu cầu.

## Ví dụ

Một sợi dây động cơ TT được tráng thiếc và hàn vào chân đực cắm vào mạch lái, nhưng mối hàn bị xám đục và vo tròn. Khi đo bằng đồng hồ, thang thông mạch vẫn kêu bíp. Lúc xe chạy không tải (dòng chỉ quanh 110–150 mA của động cơ TT 1:48), sụt áp nhỏ nên xe vẫn đi thẳng. Tuy nhiên khi bánh xe bị kẹt vào cuốn sách, dòng tăng lên khoảng $$1{,}2\,\mathrm{A}$$; điện trở mối hàn lỗi đo được chừng $$0{,}4\,\Omega$$ gây ra:

$$
V_{\mathrm{sut}} = 1{,}2 \times 0{,}4 = 0{,}48\,\mathrm{V}
$$

$$
P = 1{,}2 \times 0{,}48 \approx 0{,}58\,\mathrm{W}
$$

Hơn nửa oát nhiệt tập trung trên một hạt thiếc nhỏ làm mối nóng nhanh, đồng thời động cơ bên đó bị hụt gần nửa vôn so với bên kia khiến xe kéo lệch dù hai kênh nhận cùng mức PWM. Cách khắc phục đúng là hút sạch mối cũ, tráng thiếc lại lõi đồng cẩn thận, hàn tạo vành lõm bám ướt tốt, bọc gen co nhiệt và thêm vòng giảm lực kéo, sau đó mới đo lại thông mạch khi mối đã nguội hẳn.

## Video tham khảo

- **Xem trước:** [iFixit's Soldering 101: Beginners Guide](https://www.youtube.com/watch?v=rK38rpUy568) — iFixit, tiếng Anh. Hướng dẫn 5 yếu tố cốt lõi của một mối hàn tốt: nhiệt độ, thiếc, thời gian, độ bóng và tránh thổi nguội mối.
- [Soldering Tutorial for Beginners: Five Easy Steps](https://www.youtube.com/watch?v=Qps9woUGkvI) — oneTesla, tiếng Anh. Minh họa lặp lại trình tự hàn chuẩn trên một mạch nhỏ, giúp bạn làm quen nhịp thao tác trước khi hàn hàng chân header.

## Bài tập

1. Nêu chính xác trình tự tiếp xúc khi tạo một mối hàn: mũi mỏ chạm vào đâu, dây thiếc đưa vào đâu, thứ tự rút ra và thời điểm được phép di chuyển dây.
2. Một mối hàn lỗi có điện trở $$0{,}5\,\Omega$$ nằm trên đường dây động cơ TT đang kẹt ở dòng $$1{,}0\,\mathrm{A}$$. Tính độ sụt áp và công suất tỏa nhiệt tại mối hàn. Thang thông mạch có phát hiện được lỗi này không?
3. Bạn hàn xong dây vào chân header mới nhớ ra quên luồn ống gen co nhiệt. Cách xử lý đúng là gì, và lực kéo khi vận hành phải dồn vào vị trí nào?
4. Có người định tráng thiếc lên đầu bấm Dupont của dây động cơ "cho chắc khỏi tuột". Hãy giải thích ngắn gọn lý do từ chối và nêu phương án đấu nối thay thế đúng kỹ thuật.
5. Gọi đúng tên bốn lỗi hàn sau: lá đồng tách khỏi mạch thử; bề mặt mối xám đục sần như cát; thiếc nối dính hai chân header cạnh nhau; lớp nhựa vỏ dây cháy nâu ngay sát một mối hàn trông vẫn bóng.

<details markdown="1">
<summary>Gợi ý đáp án</summary>

1. Mũi mỏ chạm đồng thời pad đồng và chân linh kiện; đưa dây thiếc trực tiếp vào mối nóng (không chấm từ mũi mỏ); rút dây thiếc ra trước rồi mới rút mỏ hàn; giữ dây đứng yên cho tới khi thiếc đông cứng hoàn toàn.
2. $$V = 1{,}0 \times 0{,}5 = 0{,}5\,\mathrm{V}$$ và $$P = 0{,}5\,\mathrm{W}$$. Thang thông mạch không phát hiện được lỗi này vì tiếng bíp chỉ báo có đường dẫn điện chứ không phân biệt được điện trở 0,5 Ω.
3. Nếu vỏ nhựa header chặn không luồn được ống gen qua, cần cắt bỏ mối cũ, luồn sẵn gen co vào dây rồi hàn lại. Dây rút nhựa hoặc vòng dây chùng phải giữ vào phần vỏ cách điện của dây chứ không kéo vào mối hàn.
4. Thiếc thấm vào đầu bấm Dupont làm mất độ đàn hồi lò xo và khiến sợi đồng dễ gãy sát mép thiếc. Cách đúng là bấm bằng kìm chuyên dụng, hoặc hàn dây động cơ trực tiếp vào chân header/pad kèm bọc gen co và giảm lực kéo.
5. Lần lượt là: bong pad đồng (lifted pad) do quá nhiệt hoặc giật dây; mối hàn nguội (cold joint); cầu thiếc (solder bridge); và cháy vỏ dây.

</details>

## Đọc thêm

- [Adafruit: hàn cho ra mối tốt](https://learn.adafruit.com/adafruit-guide-excellent-soldering) — bộ ảnh đối chiếu rất trực quan giữa mối hàn đạt chuẩn và các dạng lỗi phổ biến.
- [SparkFun: hàn xuyên lỗ](https://learn.sparkfun.com/tutorials/how-to-solder-through-hole-soldering/all) — hướng dẫn chi tiết kỹ thuật hàn xuyên lỗ và cách khắc phục từng lỗi.
- [Module TB6612FNG của Pololu](https://www.pololu.com/product/713) — tham khảo hàng chân header thực tế bạn sẽ hàn sau khi đã thành thạo trên mạch thử.

## Mua ở Việt Nam

Các mức giá dưới đây được ghi nhận trên Hshop ngày **23 tháng 9 năm 2026** (cần kiểm tra lại giá hiện hành trước khi thanh toán). Phần còn lại của bộ robot nằm ở [BOM và cách mua bộ kit robot ở Việt Nam]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %}); danh sách này chỉ liệt kê dụng cụ phục vụ riêng bài thực hành hàn:

- Mỏ hàn 60 W WADFOW WEL3616, 75.000 ₫: [Hshop](https://hshop.vn/mo-han-60w-wadfow-wel3616-soldering-iron)
- Giá đỡ tròn có bọt biển, 40.000 ₫: [Hshop](https://hshop.vn/de-gac-mo-han-tron-b-2-co-khay-roi)
- Thiếc hàn Sunchi 0,8 mm Sn63/Pb37, 24.000 ₫: [Hshop](https://hshop.vn/thiec-han-sunchi-kp26-0-8mm-sn63-pb37-solder-wire)
- Bơm hút thiếc Handskit GS-107, 55.000 ₫: [Hshop](https://hshop.vn/hut-thiec-handskit-gs-107-desoldering-pump)
- Kìm cắt chân 170 mm, 35.000 ₫: [Hshop](https://hshop.vn/kim-cat-day-dien-nho-170-cat-chan-linh-kien-dien-tu)
- Mỡ hàn RELIFE RL-426A, 25.000 ₫: [Hshop](https://hshop.vn/mo-han-relife-rl-426a-30g-chinh-hang) — lưu ý kiểm tra đúng sản phẩm là hũ mỡ hàn (vì đường dẫn có chữ `mo-han` dễ nhầm với mỏ hàn).

Nếu Hshop tạm hết hàng, bạn có thể tìm thêm tại [Shopee, mỏ hàn 60W](https://shopee.vn/search?keyword=mo%20han%2060W), [Shopee, thiếc hàn](https://shopee.vn/search?keyword=thiec%20han), hoặc nhập cùng từ khóa trên [trang catalog Lazada](https://www.lazada.vn/catalog/?q=). Thanh header và mạch thử rời có thể mua trực tiếp tại [Hshop](https://hshop.vn/), [Thế Giới IC](https://www.thegioiic.com/) hoặc [IC Đây Rồi](https://icdayroi.com/). Đừng quên trang bị thêm kính bảo hộ vì đây là vật dụng bắt buộc khi hàn và cắt chân linh kiện.
