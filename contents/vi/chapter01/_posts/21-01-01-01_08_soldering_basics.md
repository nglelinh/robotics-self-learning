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

Hàn, trong khóa này, là một sợi dây mô-tơ vẫn dẫn điện sau khi khung xe đã rung nó. Bạn tráng thiếc dây bện, hàn vào chân header hoặc một pad vụn, rồi bọc mối để chỗ bị uốn là đoạn dây chứ không phải chỗ thiếc. Mối bóng mà nứt ở lần thử đầu vẫn là mối hỏng.

## Mục tiêu

Bạn đốt nóng cả pad lẫn chân linh kiện, đưa thiếc vào chính mối đó, rút thiếc ra, rồi mới rút mỏ. Bạn nhận mối lõm, bóng, thấm cả hai mặt, và loại cục tròn, mối nguội đục hạt, cầu thiếc, pad bong và vỏ dây cháy. Bạn nói được vì sao 60/40 hoặc Sn63 hợp với bộ dây hobby khi có gió thoáng, và vì sao flux là một phần của mối chứ không phải mùi để chịu. Bạn thêm giảm lực kéo và gen co nhiệt cho dây mô-tơ TT phải uốn, và bạn không tráng thiếc một đầu bấm Dupont rồi hy vọng nó bền. Bạn thông mạch một mối tập và chụp ảnh đối chiếu hình mối hàn.

## Kiến thức cần có

Biết kêu thông mạch từ bài 02, và biết đầu nào của header là chân cắm. Buổi này dùng đồ vụn, tờ sơ đồ chân bài 07 để đó cũng được. Đọc mục an toàn trước khi cắm điện. Không có khung xe và không có pin lithium trên bàn này.

## Vì sao bài này quan trọng

Xe capstone chạy hai mô-tơ TT qua TB6612, pin riêng, không phải cáp USB của ESP32 hay Pico. Dây ấy ra AO1, AO2, BO1, BO2 và bị uốn ở mọi chỗ buộc. Mối nguội vẫn kêu trên đồng hồ nhưng chỉ sụt áp khi bánh bị kẹt, nên xe kéo lệch trong khi hai lệnh PWM giống nhau. Dây HC-SR04 ít uốn hơn, nhưng cùng một thói quen: dây echo 5 V sờ nhầm hàng xóm 3,3 V còn tệ hơn dây đứt. Dây Dupont để trên breadboard. Đường mô-tơ cần pad, mối lõm, và một vòng dây chùng.

![Mỏ cắm điện phải có đế ngay khi nóng]({{ site.imgurl }}/wikimedia/Soldering_iron.jpg)

Ảnh là dụng cụ, chưa phải kỹ thuật. Mỏ 60 W không có núm nhiệt. Bạn khống chế nhiệt bằng thời gian mũi chạm đồng. Đế là thứ giữ mũi khỏi sổ, khỏi dây, khỏi tay trong lúc với lấy thiếc.

![Mối lõm bóng đặt cạnh cục thiếc]({{ site.imgurl }}/generated/solder_joint_compare.png)

Lấy hình này làm thước của buổi lab. Bên đạt thì lõm, bóng với thiếc chì, thấm cả pad lẫn chân, và vẫn thấy hình chân kim loại. Bên loại là cục tròn hoặc khối đục hạt. Tiếng kêu thông mạch không nâng bên loại lên thành đạt.

## Đốt nóng, rồi mới cho thiếc, rồi rời đi

Lau mũi đến khi sáng, rồi chảy một ít thiếc lên mũi. Lớp đó là đường nhiệt đi vào mối. Mũi đen chỉ cháy flux, không truyền nhiệt. Mỏ 60 W ở đường link bên dưới chỉ có một nấc: cắm điện. Nó nóng hơn mức pad header cần, nên thời gian tiếp xúc mới là núm chỉnh. Thường một đến ba giây. Pad nhỏ mà tì mười giây thì bong.

Đặt mũi chạm cùng lúc pad và chân để cả hai nóng. Đưa thiếc vào góc chỗ chúng gặp nhau, đừng tô một cục từ trên mũi mỏ. Dây thiếc phải chảy vì đồng đã nóng. Thiếc chỉ chảy khi chọc vào mũi thì pad vẫn lạnh. Khi thiếc đã thấm cả hai mặt, rút dây thiếc trước, rồi rút mỏ. Đừng thổi, và đừng dịch chân cho đến khi mối đông. Cựa trong giây đó là vết nứt để dành.

Flux là lý do thiếc loang thay vì vo tròn. Dây lõi nhựa thông đã có một phần. Một chấm mỡ hàn trên pad xỉn là đủ. Tuýp bên dưới là RELIFE RL-426A. Đường dẫn có chữ `mo-han`, từ này cũng là tên của mỏ hàn. Đọc lọ. Nếu trong hộp là mỏ chứ không phải mỡ hàn, đừng chấm lên pad.

Sn63/Pb37 và hợp kim 60/40 chảy gần $$183^\circ\mathrm{C}$$. Thiếc không chì thường gần $$217^\circ\mathrm{C}$$ và khó thấm hơn, không hợp với mỏ không hạ nhiệt được. Với bộ dây hobby, thiếc chì chấp nhận được nếu có gió và bạn rửa tay. Không phải lý do để tắt quạt. Khói flux gây kích ứng. Quạt nhỏ thổi ngang bàn, hoặc cửa sổ mở, giữ mặt khỏi luồng khói. Kính bảo hộ ở trên mắt, vì flux bắn.

## Mối hàn đang nói gì

Mối tốt là một vành thiếc bóng, thấm cả pad lẫn chân. "Thấm" nghĩa là thiếc loe ra trên đồng chứ không ngồi cạnh đồng với một rãnh. Vẫn thấy dáng chân kim loại trong thiếc. Với Sn63 hoặc 60/40, mặt mối mịn chứ không như cát.

Mối nguội thì đục và sần: pad chưa nóng, hoặc dây động lúc hợp kim đông. Không thấm thì thành cục, thường còn đồng trần quanh chân. Cầu thiếc nối hai chân đáng lẽ tách, ví dụ PWMA và chân bên cạnh. Pad bong là lá đồng bị xé vì nhiệt quá hoặc vì giật dây khi thiếc chưa đông. Trên mạch vụn, đó là bài học. Trên module TB6612, đó là hết module. Vỏ dây cháy nghĩa là mỏ tì lên áo nhựa. Đồng vẫn có thể kêu, và sợi đứt đúng chỗ nhựa nâu.

Sửa mối xấu bằng cách lấy thiếc đi, không phải đắp thêm. Hút thiếc, khi mối còn chảy, kéo phần thừa ra. Rồi flux, rồi một lần làm lại cho sạch. Đừng nạy mối đã đông khỏi pad.

Dưới dòng mô-tơ, hình dạng là chuyện điện, không phải chuyện đẹp. Thông mạch chỉ chứng minh có một đường nào đó. Mối thấm một nửa, vài phần mười ôm, ở dòng kẹt sẽ sụt điện áp thật:

$$
V_{\mathrm{sut}} = I \times R_{\mathrm{moi}}
$$

Mối $$0{,}4\,\Omega$$ ở $$1{,}2\,\mathrm{A}$$ sụt khoảng nửa vôn và nung một hạt thiếc cỡ nửa oát. Một mô-tơ TT yếu hơn mô-tơ kia, xe cua, chương trình vô can.

## Giảm lực kéo, và đầu bấm không được hàn

Dây mô-tơ bị uốn, nên mối hàn không được làm bản lề. Tuốt vài milimét, xoắn, tráng một bó không dài hơn pad. Hàn xong. Luồn gen co qua mối và một đoạn áo dây, rồi co bằng mỏ để gần ống, không đâm vào ống. Một vòng hoặc một dây rút chịu lực kéo. Quên gen cho đến sau khi hàn thì ống không chui qua vỏ header; cắt mối và làm lại.

Đầu bấm Dupont là một lò xo. Tráng thiếc vào đó thì thiếc bò lên sợi đồng, lò xo hết đàn hồi, dây gãy sát mép thiếc sau vài chục lần cắm rút. Đầu bấm cần đúng kìm. Thiếc cần một pad hoặc một chân header định để yên. Dây breadboard giữ nguyên đầu bấm. Dây TT lên driver thì hàn, bọc gen, và giảm lực kéo.

## An toàn

Mỏ nằm trên đế từ lúc nóng. Đeo kính. Đừng búng thiếc khỏi mũi; lau lên bọt biển hoặc bùi nhùi của đế. Rút điện khi dừng, kể cả khi chỉ đi một lát. Không có trẻ em cạnh bàn này. Rửa tay sau thiếc chì. Không hàn cell lithium hay 18650 rời. Dùng bộ pin đã có sẵn dây.

## Thực hành

Tập trên đồ vụn. Module driver và mọi cục pin ở trong ngăn kéo.

1. Chỉ cắm điện sau khi mỏ đã ở trên đế, kính đã đeo, và quạt hoặc cửa sổ đang đẩy gió ngang bàn. Ghi hợp kim. Cuộn được dẫn link là Sn63/Pb37, đường kính 0,8 mm.
2. Tráng mũi đến khi bóng. Mũi không ăn thiếc thì đang ôxy hóa. Lau trước khi chạm pad.
3. Lấy một đoạn dây bện vụn. Tuốt khoảng 3 mm, xoắn, tráng thành một bó ngắn.
4. Hàn đầu ấy vào chân header hoặc pad mạch thủ. Đốt pad và chân cùng lúc, đưa thiếc vào mối, rút thiếc, rút mỏ, giữ yên đến khi đông.
5. Chụp mối cạnh hình so sánh, hoặc để hình trên điện thoại trong cùng khung. Nói bên nào khớp với mối của bạn. Đục, tròn, hoặc ngồi trên pad mà không thấm thì hút ra và làm một lần mới. Pad bong thì dừng, chuyển pad khác, và ghi "pad bong" cùng số giây bạn nghĩ mình đã tì.
6. Thông mạch từ đầu dây tự do đến đầu chân tự do. Kêu mà hình xấu vẫn trượt. Mối bóng mà hở thì trượt chiều kia.
7. Mối nằm trên dây rời thì thêm gen co. Lưu ảnh `ch01-08-joint`.

Những gì phải ghi: hợp kim, mối có khớp bên tốt của hình không, kết quả thông mạch, và lỗi bạn thật sự tạo ra (cầu, bong, không thấm, áo dây nâu). Lỗi là dữ liệu. Trang chỉ ghi "ok" không đạt.

## Ví dụ

Dây TT được tráng và hàn vào chân đực sẽ cắm vào driver. Mối xám và tròn. Đồng hồ kêu. Tải nhẹ, gần dải không tải 110–150 mA của một mô-tơ TT 1:48, sụt áp nhỏ và xe bò thẳng. Bánh kẹt vào một cuốn sách, dòng lên khoảng $$1{,}2\,\mathrm{A}$$. Đo hai đầu mối được chừng $$0{,}4\,\Omega$$.

$$
V_{\mathrm{sut}} = 1{,}2 \times 0{,}4 = 0{,}48\,\mathrm{V}
$$

$$
P = 1{,}2 \times 0{,}48 \approx 0{,}58\,\mathrm{W}
$$

Nửa oát trong một hạt thiếc thì nóng rất nhanh. Mô-tơ ấy thấy ít hơn mô-tơ kia khoảng nửa vôn, xe kéo lệch dù hai lệnh PWM giống nhau. Cách sửa: hút sạch mối, tráng sợi cho tử tế, tạo vành lõm, bọc gen, thêm vòng giảm kéo. Thông mạch lại chỉ sau khi thiếc nguội và tay đã buông.

## Bài tập

1. Liệt kê thứ tự chạm của một mối: mỏ chạm gì, thiếc chạm đâu, món nào rời trước, và khi nào được dịch dây. Đảo một bước là hỏng câu trả lời.
2. Mối $$0{,}5\,\Omega$$, một mô-tơ TT kẹt ở $$1{,}0\,\mathrm{A}$$. Tính sụt áp và công suất trên mối. Tiếng thông mạch có bắt được lỗi này không?
3. Hàn header xong mới nhớ gen co. Làm gì, và lực kéo phải rơi vào đâu khi dây đã được bọc?
4. Một người muốn tráng thiếc đầu bấm Dupont của dây mô-tơ "cho khỏi tuột". Từ chối trong hai câu và nói mối bạn sẽ làm thay.
5. Gọi tên lỗi: lá đồng bong khỏi mạch vụn; mặt sần như cát; thiếc nối hai chân header; áo dây nâu ngay cạnh một mối vẫn bóng.

<details markdown="1">
<summary>Gợi ý đáp án</summary>

1. Mỏ chạm cùng lúc pad và chân. Thiếc đi vào mối, không phải tô từ mũi. Thiếc rời trước, rồi mỏ. Dây đứng yên đến khi mối đông.
2. $$V = 1{,}0 \times 0{,}5 = 0{,}5\,\mathrm{V}$$ và $$P = 0{,}5\,\mathrm{W}$$. Tiếng kêu chỉ nói có đường dẫn. Nó không thấy nửa ôm.
3. Vỏ header chặn ống thì cắt mối và làm lại, gen đã nằm sẵn trên dây. Dây rút hoặc vòng chùng kéo vào áo dây, không kéo vào mối.
4. Thiếc bò vào đầu bấm rồi sợi gãy sát chỗ đó. Bấm bằng đúng kìm, hoặc hàn dây mô-tơ vào chân header hay pad rồi giảm lực kéo. Đừng tráng đầu bấm.
5. Lá đồng bong là pad bị nhấc, vì nhiệt hoặc vì giật. Mặt sần là mối nguội. Thiếc giữa hai chân là cầu. Áo nâu là vỏ cháy, dù mối trông vẫn đúng.

</details>

## Đọc thêm

- [Adafruit: hàn cho ra mối tốt](https://learn.adafruit.com/adafruit-guide-excellent-soldering) — ảnh mối lõm, mối nguội, và cách giữ mũi. Đối chiếu ảnh lab với trang này và với hình của bài.
- [SparkFun: hàn xuyên lỗ](https://learn.sparkfun.com/tutorials/how-to-solder-through-hole-soldering/all) — cùng thứ tự đốt rồi mới đưa thiếc, có tên từng lỗi.
- [Module TB6612FNG của Pololu](https://www.pololu.com/product/713) — hàng header mà bạn đang tập để tới. Pad mô-tơ vẫn không phải bài tập vụn của hôm nay.

## Mua ở Việt Nam

Giá dưới đây đọc trên Hshop ngày **23 tháng 9 năm 2026**. Giá sẽ chạy. Xem trang đang bán trước khi trả tiền. Phần còn lại của robot nằm ở chương 00, bài 05, [BOM và cách mua bộ kit robot ở Việt Nam]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %}). Danh sách này chỉ là bàn để hàn một mối.

- Mỏ 60 W, WADFOW WEL3616, 75.000₫: [Hshop](https://hshop.vn/mo-han-60w-wadfow-wel3616-soldering-iron)
- Đế tròn có bọt biển, 40.000₫: [Hshop](https://hshop.vn/de-gac-mo-han-tron-b-2-co-khay-roi)
- Thiếc Sunchi 0,8 mm Sn63/Pb37, 24.000₫: [Hshop](https://hshop.vn/thiec-han-sunchi-kp26-0-8mm-sn63-pb37-solder-wire)
- Hút thiếc Handskit GS-107, 55.000₫: [Hshop](https://hshop.vn/hut-thiec-handskit-gs-107-desoldering-pump)
- Kìm cắt chân 170 mm, 35.000₫: [Hshop](https://hshop.vn/kim-cat-day-dien-nho-170-cat-chan-linh-kien-dien-tu)
- Mỡ hàn RELIFE RL-426A, 25.000₫: [Hshop](https://hshop.vn/mo-han-relife-rl-426a-30g-chinh-hang). Xác nhận trong lọ là mỡ hàn. Slug ghi `mo-han`; đừng mua nhầm thành mỏ.

Hshop hết hàng thì hai trang tìm này: [Shopee, mỏ hàn 60W](https://shopee.vn/search?keyword=mo%20han%2060W) và [Shopee, thiếc hàn](https://shopee.vn/search?keyword=thiec%20han). Trên Lazada, mở [trang catalog](https://www.lazada.vn/catalog/?q=) rồi tự gõ cùng từ khóa. Cửa hàng: [Hshop](https://hshop.vn/), [Thế Giới IC](https://www.thegioiic.com/), [IC Đầy Rồi](https://icdayroi.com/). Thanh header và một mẩu mạch thủ lấy ở các cửa đó; bài này không bịa link sản phẩm cho chúng. Kính bảo hộ không trở thành tùy chọn chỉ vì không có trong bảng giá.
