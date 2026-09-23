---
layout: post
title: "Voltage, current, power, and Ohm's law"
chapter: "01"
order: 1
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter01
lesson_type: required
draft: false
---

## Learning objectives

By the end of this lesson you will be able to name voltage, current, resistance, and power with their units, use $V = IR$ to find the missing quantity in one loop, and compute resistor heating with $P = VI = I^2 R = V^2/R$. You will size the series resistor for a red LED on a 3.3 V rail and show that a 1/4 W body is plenty. You will also explain why a TT gearmotor is not a resistor you may hang on an ESP32 or Pico GPIO.

## Prerequisites

Arithmetic is enough if every number keeps its unit. A bare 0.008 might be 8 mA or a slipped decimal. The numbers can be finished on paper. A meter and a red LED, if you already have them, are for the lab. The next lesson names holes and jacks.

## Why this matters on the diff-drive robot

The capstone is a two-wheel differential-drive robot. An ESP32 or a Pico speaks 3.3 V logic. A TB6612FNG steers two TT gearmotors from a separate battery, and an HC-SR04 later reports distance. The alive-lamp is a red LED and one resistor on 3.3 V. Too much resistance and the lamp looks dead. No resistor and the LED, or the pin, dies.

The motors are the other budget. A stalled TT motor draws on the order of an ampere. A GPIO is comfortable nearer 12 mA and is in trouble somewhere around 40 mA. If that motor current is borrowed from the USB lead that feeds the chip, the 5 V rail sags, the onboard regulator cannot hold 3.3 V, and the board resets at the instant the wheels were commanded to turn. Ohm's law separates those two failures before you blame the firmware.

## Voltage, current, and resistance

Voltage is energy per unit charge, always measured between two points. One volt means one joule per coulomb. A pin marked 3.3 V says a charge falling from that pin to ground gives up 3.3 J per coulomb. One meter lead, with nowhere for the other to land, has not measured a voltage.

Current is how much charge passes a point each second. One ampere is one coulomb per second. The symbol is $I$. On a GPIO and on an LED we speak in milliamperes:

$$
1\ \mathrm{mA} = 0.001\ \mathrm{A}
$$

so 8 mA is $0.008\ \mathrm{A}$. A TT motor lives elsewhere: a few hundred milliamperes while rolling, and an ampere-class spike when the rotor is locked. Diagrams in this course use conventional current, drawn from positive toward negative.

Resistance, $R$, in ohms ($\Omega$), is how hard a part pushes back. A larger resistance allows less current for the same voltage. A jumper is a fraction of an ohm. A 180 Ω resistor is a deliberate bottleneck. An open switch is so large a resistance that the current is effectively zero.

For a resistor at a steady temperature the three quantities are tied by Ohm's law:

$$
V = IR
$$

which rearranges to $I = V/R$ and $R = V/I$. The law is a model of ohmic parts. A resistor is close enough for every calculation in this chapter. An LED is not ohmic. It conducts very little until the voltage across it reaches a forward drop, then the current rises steeply. That is why an LED gets a resistor as a partner rather than being treated as a resistor itself.

![Ohm's law triangle: cover the quantity you want]({{ site.imgurl }}/generated/ohms_law_triangle.png)

The triangle is only a memory aid for $V = IR$. Cover the letter you want. Cover $V$ and you multiply $I$ by $R$. Cover $I$ and you divide $V$ by $R$. Power is not on this triangle.

## Power, and the series LED loop

Power is energy per second, in watts. For any two-terminal part it is the product of the voltage across that part and the current through it:

$$
P = VI
$$

On a resistor, substitute Ohm's law. With $I = V/R$,

$$
P = \frac{V^2}{R}
$$

With $V = IR$,

$$
P = I^2 R
$$

The three expressions agree on a resistor. On an LED the voltage stays near the forward drop while the resistor sets the current, so use $P = V_f I$ for the LED and $I^2 R$ for the resistor. In $V^2/R$, $V$ is the voltage across the resistor, not the full supply.

A 1/4 W resistor may dissipate 0.25 W in free air. The LED resistors here dissipate tens of milliwatts. A low-value resistor asked to pass an ampere will brown, and $I^2 R$ tells you first.

In one series loop the current is the same everywhere and the voltages add to the supply:

$$
V_\mathrm{s} = V_R + V_f
$$

so $V_R = V_\mathrm{s} - V_f$ and $I = V_R / R$. In parallel, each branch sees the same voltage and the currents add. Two motors on one driver are that second case. The battery supplies the sum. The microcontroller's USB lead is not that battery.

## Worked example: the 3.3 V status lamp

The rail is 3.3 V, the LED is red with $V_f \approx 2.0\ \mathrm{V}$, and the target is 8 mA so the lamp is obvious indoors without stressing a pin.

$$
R = \frac{V_\mathrm{s} - V_f}{I} = \frac{3.3 - 2.0}{0.008} = \frac{1.3}{0.008} = 162.5\ \Omega
$$

Choose the next common value up, 180 Ω, so the current lands under the target:

$$
I = \frac{3.3 - 2.0}{180} = \frac{1.3}{180} \approx 7.2\ \mathrm{mA}
$$

Check the heat with the target current and the body you will actually fit. That estimate is slightly pessimistic, which is what you want before you trust a power rating:

$$
P = I^2 R = (0.008)^2 \times 180 = 0.0115\ \mathrm{W} \approx 0.011\ \mathrm{W}
$$

A 1/4 W part is rated 0.25 W, so the resistor runs at about 4% of its rating. Using the 7.2 mA that 180 Ω really sets gives a little less, about 0.009 W. The same number comes from the 1.3 V the resistor drops: $P = VI \approx 0.0072 \times 1.3 \approx 0.009\ \mathrm{W}$ and $P = V^2/R = 1.69/180 \approx 0.009\ \mathrm{W}$. The LED itself dissipates $P_\mathrm{LED} \approx 2.0 \times 0.0072 \approx 0.014\ \mathrm{W}$.

![One loop: supply, series resistor, LED, ground]({{ site.imgurl }}/generated/led_series_resistor.png)

Current leaves the positive rail, passes through the resistor, enters the LED at the anode, leaves at the cathode, and returns to ground. The current in the resistor is the current in the LED. If the LED is backwards the loop stays dark. That is not a reason to omit the resistor when you turn it around. With no resistor, nothing sets the current. The LED is asked to sit near 3.3 V with a forward drop near 2 V, and the current becomes whatever the pin and the steep LED curve will allow, often many times 20 mA.

## Worked example: a motor is not a GPIO resistor

Suppose a stalled TT motor draws about 0.8 A at 6 V. Ohm's law, misapplied, "finds a resistance":

$$
R_\mathrm{stall} \approx \frac{6}{0.8} = 7.5\ \Omega
$$

Hang that across a 3.3 V GPIO and the same formula predicts

$$
I \approx \frac{3.3}{7.5} \approx 0.44\ \mathrm{A} = 440\ \mathrm{mA}
$$

A cautious GPIO budget is about 12 mA. A figure often quoted as an absolute ceiling is about 40 mA. Four hundred milliamperes is an order of magnitude past both. The pin fails, or the regulator sags and the chip resets. The arithmetic is also too kind: a stalled motor is a coil plus a locked gearbox, not a stable 7.5 Ω film part. While it spins, back-emf makes the current smaller than stall, so a free-running bench test lies about a robot that has nosed into a wall.

Motor current belongs on the TB6612 VM pin, from a pack in the module's range of about 4.5 V to 10 V. The GPIO only carries direction and PWM into logic inputs specified from 2.7 V to 5.5 V, so 3.3 V is a legal high. Two stalled motors near 0.8 A each ask for about 1.6 A. A laptop USB port is often budgeted near 0.5 A, so the wheels are not powered from USB or from the 3.3 V pin.

## Hands-on lab

Build the lamp only after the arithmetic.

1. Write $R = (3.3 - 2.0) / 0.008 = 162.5\ \Omega$ and, beside it, the 180 Ω part you will fit, before any lead goes into a hole.
2. Place the resistor and a red LED in series between the 3.3 V rail and GND. On a dev board that rail is the pin marked 3V3, not a GPIO and not the pin marked 5V. The longer LED lead, the anode, points toward the positive side. The flat on the rim points toward GND.
3. Apply power only after the series resistor is in the loop. Look at the LED from the side, not straight into the lens.
4. Set the meter to DC volts, red lead in the voltage jack, and measure across the resistor only. Divide that voltage by 180 Ω. You are inferring current. Do not break the loop to measure amperes; that skill is the next lesson.

You should see a clearly visible red glow, not a dazzling one. The voltage across the 180 Ω resistor should sit near 1.1 V to 1.5 V, so the current is near 6 mA to 8 mA. The resistor will not feel hot. A 220 Ω substitute gives $I = 1.3 / 220 \approx 5.9\ \mathrm{mA}$, dimmer and still a success.

| What you see | Likely cause | What to change |
| --- | --- | --- |
| Dark LED, resistor cool | LED reversed | Swap the LED. Leave the resistor in the loop. |
| A flash, then darkness | Series resistor missing, or shorted by the way it was inserted | Retire that LED. Rebuild with 180 Ω before you trust the pin. |
| Board resets, or a GPIO no longer toggles | 5 V landed on an ESP32 or Pico pin, or the LED returned through a GPIO from the 5 V rail | Stop. Power the lamp only from 3V3 to GND. Retest the pin with a known-good LED and 180 Ω. |
| Glow that vanishes in room light | The part is tens of kilohms, not 180 Ω | Measure it. $I = 1.3 / 10000 = 0.13\ \mathrm{mA}$ looks black. |

Safety: keep any chassis wheels off the table, do not connect a motor supply, and do not land VM or USB 5 V on a GPIO. One LED at a few milliamps is the whole experiment.

## Exercises

1. A green LED with $V_f = 2.2\ \mathrm{V}$ is lit from 5 V at 10 mA, between 5 V and GND, not into a GPIO. Compute $R$, pick the next value up from 220 Ω, 270 Ω, and 330 Ω, and compute $P$ in that resistor.
2. The kit has no 180 Ω part, so you use 220 Ω for the 3.3 V red lamp with $V_f = 2.0\ \mathrm{V}$. Find the current. Is the lamp still usable indoors?
3. One TT motor draws 0.15 A while rolling and 0.8 A when stalled. Two run together. Which total, if either, fits on a USB port limited to 0.5 A?
4. A friend measures 3.3 V across a dark LED with no series resistor and says the voltage is correct, so the LED is fine. Using $V_\mathrm{s} = V_R + V_f$, what is missing?
5. For a 180 Ω resistor with 1.3 V across it, show that $P = VI$, $P = I^2 R$, and $P = V^2/R$ agree. Why is it wrong to plug $V = 3.3\ \mathrm{V}$ into $V^2/R$ for that resistor?

<details>
<summary>Suggested answers</summary>

1. $R = (5 - 2.2) / 0.010 = 280\ \Omega$. The next value up is 330 Ω. Then $I = 2.8 / 330 \approx 8.5\ \mathrm{mA}$ and $P \approx 0.024\ \mathrm{W}$, well under 0.25 W. This lamp is not on a GPIO.
2. $I = 1.3 / 220 \approx 5.9\ \mathrm{mA}$. Yes. Dimmer than 8 mA, still an obvious indoor indicator. Do not remove the resistor to "fix" the dimness.
3. Rolling: $0.30\ \mathrm{A}$, under 0.5 A. Stall: $1.6\ \mathrm{A}$, which does not fit. A rolling test can look safe and still reset the board when a wheel stalls. Motor current does not come from USB.
4. With no resistor, $V_R = 0$, so the entire 3.3 V is forced onto the LED. A healthy red LED sits near 2 V only when a resistor sets a modest current. Full supply across a dark LED means it is open, backwards, or already dead.
5. $I = 1.3 / 180 \approx 7.2\ \mathrm{mA}$, and all three formulas give about 0.0094 W. Using 3.3 V pretends the resistor drops the whole supply and ignores the LED's 2 V.

</details>

## Further reading

All About Circuits states the law in a DC chapter: [Voltage, current, resistance, and Ohm's law](https://www.allaboutcircuits.com/textbook/direct-current/chpt-2/voltage-current-resistance-ohms-law/). SparkFun's LED page is the companion once the resistor is in the loop: [Light-emitting diodes](https://learn.sparkfun.com/tutorials/light-emitting-diodes-leds).

## Where to buy in Vietnam

The chassis, driver, microcontroller, ultrasonic sensor, and the rest of the cart are listed in [Bill of materials and how to buy the kit in Vietnam]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %}). This lesson adds only the lamp parts, and only if that cart does not already include them.

A 3 mm LED assortment on Hshop was 20 000 ₫ on 23 September 2026: [bộ 5 loại LED 3 mm](https://hshop.vn/bo-5-loai-led-sieu-sang-3mm-thong-dung-5-kind-3mm-transparent-color-led). Use a red LED for the calculation above. Confirm the live price before you pay.

A 1/4 W assortment that includes 180 Ω or 220 Ω is the resistor buy. Hshop search for điện trở did not return a 1/4 W kit when this lesson was written, so use a search page and read the shop: [Shopee search for bộ điện trở 1/4W](https://shopee.vn/search?keyword=b%E1%BB%99%20%C4%91i%E1%BB%87n%20tr%E1%BB%9F%201%2F4W). That link is a search page, not one product. Look for 1/4 W and 5% or 1%. Do not trust a loose unlabeled "180 Ω" without measuring it.
