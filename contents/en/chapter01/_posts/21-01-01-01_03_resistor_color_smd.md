---
layout: post
title: "Resistor identification: color bands and SMD codes"
chapter: "01"
order: 3
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter01
lesson_type: required
draft: false
---

## Learning objectives

By the end of this lesson you will be able to read a four-band resistor as digit, digit, multiplier, and tolerance, and compute the window the tolerance allows. You will decode brown-black-red-gold as 1 kΩ ±5% and brown-blue-orange-gold as 16 kΩ ±5% without looking up the arithmetic a second time. You will recognize a five-band part as three digits plus a multiplier, read a three-digit SMD code such as 103 or 472, and treat an R in a code such as R22 as a decimal point. You will confirm a decoded value with an unpowered meter and know when probe resistance, not the part, is what you are seeing.

## Prerequisites

You need Ohm's law from the first lesson, especially $I = V/R$ and the reason a status LED uses about 180 Ω rather than whatever cylinder was nearest the iron. You need the meter's ohms habit from the previous lesson: unpowered part, red lead in the voltage/ohms jack, not the current jack. No SMD soldering is required. If your kit is all through-hole, the SMD section is still worth reading, because the same codes are printed on the small parts already soldered to an ESP32 board and a TB6612 module.

## Why this matters on the diff-drive robot

The 3.3 V lamp on the ESP32 or Pico only works if the cylinder you just inserted is actually near 180 Ω. Brown-black-orange is 10 kΩ, not 1 kΩ, and the lamp then runs at $I = 1.3 / 10000 = 0.13\ \mathrm{mA}$, which looks like a dead GPIO in a lit room. The opposite mistake, a few ohms where you wanted hundreds, dumps the pin.

The same skill shows up off the breadboard. Pull-ups on a button, the series resistor you may later use to tame an HC-SR04 echo, and the tiny parts on a motor-driver module are all resistors with either bands or a printed code. The TB6612 does not become safer because the resistor "looks red." Two TT motors still must not be treated as resistors on a GPIO; identifying a 10 Ω shunt is not an invitation to build one. Read the part, then decide whether it belongs in the circuit at all.

## Four bands, then five

A standard four-band resistor is read from the end closest to the bands, with the tolerance band — almost always gold or silver on a hobby part — kept on the right. The first two bands are significant digits. The third is a multiplier, a power of ten. The fourth is the tolerance, how far the real resistance may sit from the painted number.

The digit colors used in this course are: black 0, brown 1, red 2, orange 3, yellow 4, green 5, blue 6, violet 7, grey 8, white 9. The multiplier uses the same colors as powers of ten: black ×1, brown ×10, red ×100, orange ×1 000, yellow ×10 000. Gold as a multiplier means ×0.1, and as a tolerance band means ±5%. Silver as tolerance means ±10%.

Brown, black, red, gold is the first number you should be able to say out loud. Brown is 1, black is 0, red means ×100:

$$
10 \times 100 = 1000\ \Omega = 1\ \mathrm{k}\Omega
$$

Gold says ±5%, so the honest window is 950 Ω to 1050 Ω. A meter reading of 980 Ω is a good part, not a counterfeit.

Brown, blue, orange, gold is the second. Brown is 1, blue is 6, orange means ×1 000:

$$
16 \times 1000 = 16000\ \Omega = 16\ \mathrm{k}\Omega
$$

again ±5%, so about 15.2 kΩ to 16.8 kΩ. If you reverse the resistor and try to start from the gold band, the code becomes nonsense, because gold is not a digit.

![Four-band color code, tolerance band on the right]({{ site.imgurl }}/generated/resistor_color_code.png)

Five-band resistors add a third significant digit before the multiplier, and the last band is still the tolerance. Brown-black-black-red-brown is 1, 0, 0, ×100, ±1%:

$$
100 \times 100 = 10\ \mathrm{k}\Omega
$$

within about ±1%. You do not need a drawer full of five-band parts to finish the robot. You do need to notice when a resistor has four color bands of digits and a fifth tolerance band, because reading it as a four-band code shifts the multiplier by a factor of ten. Count the bands before you multiply.

## SMD codes, including the letter you do not memorize

A three-digit SMD resistor code is the same idea printed in ink. The first two digits are the significant figures. The third is the power of ten. So 103 is $10 \times 10^3 = 10\ \mathrm{k}\Omega$, and 472 is $47 \times 10^2 = 4700\ \Omega = 4.7\ \mathrm{k}\Omega$. A code of 100 is $10 \times 10^0 = 10\ \Omega$, not 100 Ω. The trailing zero is an exponent, not another digit to append.

When the value is under 10 Ω the letter R stands in for the decimal point. R22 means 0.22 Ω. 4R7 means 4.7 Ω. That R is easy to miss on a dark body, and it matters: a 0.22 Ω part used as an LED resistor from 3.3 V is almost a short.

Four-digit codes extend the same rule to three significant figures: 4701 is $470 \times 10^1 = 4.7\ \mathrm{k}\Omega$. The EIA-96 system is different. It prints two digits plus a letter, and the digits are an index into a table rather than the resistance itself. You will see it on 1% SMD parts. Do not memorize the table. If the code is two digits and a letter, look it up or measure the part. Guessing turns an index of "01" into a one-ohm resistor that is not one ohm.

![A mixed assortment: bands, bodies, and wattage are not the same thing]({{ site.imgurl }}/wikimedia/resistors_assortment.jpg)

Body size is a hint about power, not about resistance. A 1/4 W through-hole cylinder is the default in this chapter. A physically larger ceramic cylinder may be 1 W or more and may use a different band layout. The LED calculation from the first lesson dissipated about 0.011 W, so 1/4 W is comfortable there. It does not make a 10 Ω, 1/4 W part a safe dummy load for a stalled motor.

## Worked example: five codes, then the meter window

Decode these before you touch the dial.

1. Brown, black, red, gold → $10 \times 100 = 1\ \mathrm{k}\Omega$, ±5%, window 950 Ω to 1050 Ω.
2. Brown, blue, orange, gold → $16 \times 1000 = 16\ \mathrm{k}\Omega$, ±5%, window 15.2 kΩ to 16.8 kΩ.
3. Red, red, brown, gold → $22 \times 10 = 220\ \Omega$, ±5%, window about 209 Ω to 231 Ω. This is the substitute status-lamp resistor when 180 Ω is missing.
4. SMD 103 → $10 \times 10^3 = 10\ \mathrm{k}\Omega$.
5. SMD R22 → 0.22 Ω. The R is the decimal point, not a color.

Now put number 3 in the lamp formula from lesson 1, $V_f = 2.0\ \mathrm{V}$ on a 3.3 V rail:

$$
I = \frac{3.3 - 2.0}{220} = \frac{1.3}{220} \approx 5.9\ \mathrm{mA}
$$

Power in that resistor is $P = I^2 R \approx (0.0059)^2 \times 220 \approx 0.008\ \mathrm{W}$, still a small fraction of 1/4 W. The same formula with a misread brown-black-orange (10 kΩ) gives 0.13 mA and a lamp you will call dead. The same formula with R22 gives $I = 1.3 / 0.22 \approx 6\ \mathrm{A}$, which neither the LED nor a GPIO can survive. The code is not a suggestion.

On the meter, expect a 5% part to fall inside its window. A reading 2% low is still a good part. Two effects fool students on the low end. Finger heat on a film resistor shifts the value a little while you pinch the body; hold the leads, not the capsule, or let go and wait a few seconds. On a part under a few ohms, the probes and leads themselves are a few tenths of an ohm. Short the probes, note that offset, and subtract it before you accuse an R22 of being the wrong code. Do not "zero" the meter by measuring a resistor that is still soldered into a live board.

## Hands-on lab

1. Pick five resistors from the kit, or use the five codes in the worked example if the kit has not arrived. Write the band or SMD reading and the ohms you claim, including the ± window for banded parts.
2. Power is off. Nothing is plugged into the resistor. Red lead in the voltage/ohms jack, black in COM, dial on ohms. If the meter is manual-ranging, start on a range above the value you expect.
3. Measure each part. Write the meter reading next to the decoded value. A 5% part should land inside its window. If it does not, check that you did not start from the gold band, and check that you did not count a five-band part as four.
4. For any part under about 10 Ω, short the probes first, record that resistance, and subtract.
5. Optional: place the 180 Ω or 220 Ω part back into the unpowered LED loop from lesson 1 and measure it again in circuit only with the supply unplugged. Then say whether neighboring parts could be in parallel with it. If you are not sure, lift one lead.

You should see meter readings inside the tolerance window for intact, correctly read parts. A 1 kΩ ±5% part at 1.02 kΩ is a pass. Continuity mode will probably stay silent on all five, which is not a failure of the resistors.

| What you see | Likely cause | What to change |
| --- | --- | --- |
| Meter reads about 10× or 0.1× your decode | Bands read from the wrong end, or a five-band part read as four | Put gold or silver on the right and count the bands again. |
| A "1 kΩ" part reads near 10 kΩ | Multiplier band read as red when it is orange, or the reverse | Check the third band under a lamp. Orange and red are the classic mix-up. |
| Low-ohm part reads 0.4 Ω high, every time | Probe and lead resistance | Subtract the shorted-probe reading. |
| Ohms reading wanders while the board is powered | Supply still connected | Unplug. Ohms mode is not for a live rail. |
| Continuity is silent on a 220 Ω part | Continuity is not the ohms range | Switch to Ω. Silence here is expected. |

Safety: never measure ohms on a powered rail, a battery, or the VM pin of a motor driver. A 2S pack is not a resistor. Keep the red lead out of the current jack so a later voltage check on the 3.3 V pin is not a short.

## Exercises

1. Decode yellow-violet-brown-gold, orange-orange-red-gold, and blue-grey-black-gold. Give each nominal value and the ±5% window.
2. Someone reads a resistor as gold-orange-violet-red. What did they do, and what is the legal four-band reading if those colors are red, violet, orange, gold?
3. Decode SMD 222, 510, 4R7, and 1003. Which of them, if any, is 10 kΩ?
4. A 1 kΩ ±5% part measures 980 Ω on an unpowered meter. Keep it, or reject it? What percent error is 980 Ω from 1000 Ω?
5. A button pull-up on a 3.3 V GPIO was supposed to be 10 kΩ. The part fitted is brown-black-red-gold. Estimate the current when the button shorts the pin to ground, and say whether the pin is happier with this part or with a true 10 kΩ pull-up.

<details>
<summary>Suggested answers</summary>

1. Yellow-violet-brown-gold is $47 \times 10 = 470\ \Omega$, about 447 Ω to 494 Ω. Orange-orange-red-gold is $33 \times 100 = 3.3\ \mathrm{k}\Omega$, about 3.14 kΩ to 3.47 kΩ. Blue-grey-black-gold is $68 \times 1 = 68\ \Omega$, about 65 Ω to 71 Ω.
2. Gold was placed on the left. Gold is tolerance, so it belongs on the right. The legal reading is red-violet-orange-gold: $27 \times 1000 = 27\ \mathrm{k}\Omega$, ±5%.
3. 222 is $22 \times 10^2 = 2.2\ \mathrm{k}\Omega$. 510 is $51 \times 10^0 = 51\ \Omega$. 4R7 is 4.7 Ω. 1003 is $100 \times 10^3 = 100\ \mathrm{k}\Omega$. None of them is 10 kΩ. The three-digit code for 10 kΩ is 103.
4. 980 Ω sits inside 950 Ω to 1050 Ω. The error is $20/1000 = 2\%$, inside the 5% band. Keep it.
5. Brown-black-red-gold is 1 kΩ, so $I = 3.3 / 1000 = 3.3\ \mathrm{mA}$ while the button is held. A 10 kΩ pull-up would draw $3.3 / 10000 = 0.33\ \mathrm{mA}$. Both are inside a GPIO's rough 12 mA to 40 mA budget, and 10 kΩ is the kinder pull-up. The 1 kΩ part is a lamp-resistor cousin, not a better button resistor.

</details>

## Further reading

SparkFun's resistor tutorial covers bands, power, and the series and parallel cases you already used for the LED: [Resistors](https://learn.sparkfun.com/tutorials/resistors). When a band is ambiguous under bad light, a calculator is faster than a second guess: [Digi-Key resistor color-code calculator](https://www.digikey.com/en/resources/conversion-calculators/conversion-calculator-resistor-color-code). Use it to check yourself, then put the part on the meter anyway.

## Where to buy in Vietnam

The full cart is in [Bill of materials and how to buy the kit in Vietnam]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %}). This lesson adds a resistor assortment only.

Hshop search for điện trở did not return a 1/4 W assortment when this page was written. Use a search page, not a guessed product link: [Shopee search for bộ điện trở 1/4W](https://shopee.vn/search?keyword=b%E1%BB%99%20%C4%91i%E1%BB%87n%20tr%E1%BB%9F%201%2F4W). That URL is a search page. Read the listing for 1/4 W and for 5% or 1%, and prefer a kit that includes 180 Ω or 220 Ω plus 1 kΩ and 10 kΩ. Confirm the price on the day you order. Loose resistors from a component counter such as [Thế Giới IC](https://www.thegioiic.com/) or [IC Đây Rồi](https://icdayroi.com/) are fine if the bag is labeled and you still measure five of them in the lab.
