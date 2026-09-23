---
layout: post
title: "Soldering robot harnesses"
chapter: "01"
order: 8
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter01
lesson_type: required
draft: false
---

Soldering, in this course, means a motor lead that still conducts after the chassis has shaken it. You tin stranded wire, join it to a header pin or a scrap pad, and cover the joint so the flex happens in the wire. A shiny joint that cracks at the first test is still a failed joint.

## Learning objectives

You will heat the pad and the lead together, feed solder into that joint, take the solder away, and only then take the iron away. You will accept a joint that is a shiny fillet wetting both surfaces, and you will reject a ball, a dull grainy cold joint, a bridge, a lifted pad, and burned insulation. You will say why 60/40 or Sn63 is a reasonable alloy for a hobby harness when the room is ventilated, and why flux is part of the joint rather than a smell to tolerate. You will add strain relief and heat-shrink on a TT motor lead that must flex, and you will refuse to tin a Dupont crimp and expect it to stay. You will continuity-beep one practice joint and photograph it against the fillet figure.

## Prerequisites

You can beep continuity from lesson 02, and you know which end of a header is the pin. This lab uses scrap, so lesson 07's card can wait. Read the safety section before you plug an iron in. No chassis and no lithium cell belong on this bench.

## Why it matters

The diff-drive capstone runs two TT motors from a TB6612, on a battery that is not the ESP32 or Pico USB cable. Those leads land on AO1, AO2, BO1, and BO2 and they flex at every tie point. A cold joint can beep and still drop voltage only when a wheel stalls, so the cart pulls while the two PWM commands match. The HC-SR04 flexes less, and the same habit still matters: a 5 V echo wire fraying into a 3.3 V neighbor is worse than an open. Dupont jumpers stay on the breadboard. The motor path wants a pad, a fillet, and a loop of slack.

![A plug-in iron needs a stand the moment it is hot]({{ site.imgurl }}/wikimedia/Soldering_iron.jpg)

The photograph is the tool, not the technique. A 60 W iron has no temperature knob. You control heat by how long the tip touches copper. The stand is what keeps that tip off the notebook, the lead, and your arm while you reach for the solder.

![Shiny fillet against a ball]({{ site.imgurl }}/generated/solder_joint_compare.png)

Use this figure as the lab rubric. The acceptable side is concave, shiny for a tin-lead alloy, and wetting both the pad and the lead so the outline of the pin is still visible. The reject side is a ball or a dull grainy mass. A beep does not promote the reject side.

## Heat, then solder, then leave

Clean the tip until it is bright, then melt a little solder onto it. That coat is how heat crosses into the joint. A black tip scorches flux and does not transfer heat. The 60 W iron linked below has one setting: plugged in. It is hotter than a header pad needs, so contact time is the control. One to three seconds is the usual window. A tiny pad you lean on for ten seconds lifts.

Touch the tip to the pad and the lead together so both are hot. Feed solder into the corner where they meet, not as a blob painted from the iron. The wire should melt because the copper is hot. If it melts only on the tip, the pad is still cold. When the fillet has wet both surfaces, remove the solder first, then the iron. Do not blow, and do not move the lead until the fillet has frozen. Movement in that second cracks later.

Flux is why the solder spreads instead of balling. Rosin-core wire already contains some. A dab of paste on a dull pad finishes the job. The paste linked below is RELIFE RL-426A. The URL slug says `mo-han`, which also names an iron. Read the jar. If the box is an iron and not flux paste, do not dab it on the pad.

Sn63/Pb37, and the older 60/40 alloy, melt near $$183^\circ\mathrm{C}$$. Common lead-free alloys melt nearer $$217^\circ\mathrm{C}$$ and wet more stubbornly, which is a poor match for an iron you cannot turn down. For hobby motor harnesses, tin-lead is acceptable if you ventilate and you wash your hands. It is not acceptable as a reason to skip the fan. Flux smoke is an irritant. A small fan across the bench, or an open window, keeps your face out of the plume. Safety glasses stay on, because flux spits.

## What the fillet is telling you

A good joint is a shiny fillet that has wetted both the pad and the lead. "Wetted" means the solder feathered onto the copper instead of sitting beside it with a ditch. You can still see the shape of the lead inside the solder. The surface, for Sn63 or 60/40, looks smooth rather than sandy.

A cold joint is dull and grainy: the pad was not hot, or the wire moved as the alloy froze. Insufficient wetting is the ball, often with bare copper still showing around it. A bridge joins two pins that should stay separate, such as PWMA and its neighbor. A lifted pad is foil torn off by too much heat or by pulling the wire early. On scrap, that is the lesson. On the TB6612 module, that is the end of the module. Burned insulation means the iron leaned on the jacket. The copper may still beep, and the strands break at the brown plastic.

Fix a bad joint by removing solder, not by piling more on. A desoldering pump, used with the joint molten, pulls the excess off. Then flux, then one clean attempt. Do not pry a frozen joint off a pad.

Under motor current the shape is an electrical fact, not a beauty contest. Continuity only proves some path exists. A half-wet joint of a few tenths of an ohm, at stall current, drops real voltage:

$$
V_{\mathrm{drop}} = I \times R_{\mathrm{joint}}
$$

A joint of $$0.4\,\Omega$$ at $$1.2\,\mathrm{A}$$ drops about half a volt and heats a speck of solder at about half a watt. One TT motor then runs weak, the cart arcs, and the firmware is innocent.

## Strain relief, and the crimp you should not solder

Motor leads flex, so the fillet must not be the hinge. Strip a few millimetres, twist, and tin a rope no longer than the pad. Make the joint. Slide heat-shrink over the fillet and a short way up the jacket, and shrink it with the iron near the tube, not stabbed into it. A loop or a tie takes the pull. Heat-shrink forgotten until after the joint will not crawl past a housing; cut the joint and start again.

A Dupont crimp is a spring. Tin it and solder wicks up the strands, the spring stops flexing, and the wire breaks beside the solder after a few dozen plug cycles. Crimps want the matching tool. Solder wants a pad or a header pin you mean to leave in place. Breadboard jumpers stay crimped. TT leads on the driver get soldered, sleeved, and strain-relieved.

## Safety

The iron rests in a stand from the moment it is hot. Wear eye protection. Do not flick solder off the tip; wipe it on the stand's sponge or brass wool. Unplug the iron when you stop, including for a short errand. Children do not share this bench. Wash your hands after leaded solder. Do not solder a lithium cell or a loose 18650. Use a pack that already has leads.

## Lab

Practice on scrap. The driver module and any battery stay in the drawer.

1. Plug the iron in only after it is in the stand, glasses are on, and a fan or a window is moving air across the bench. Write the alloy. The linked reel is 0.8 mm Sn63/Pb37.
2. Tin the tip until it is shiny. If it will not take solder, the tip is oxidized. Clean it before you touch a pad.
3. Take a scrap of stranded wire. Strip about 3 mm, twist, and tin the strands into one short rope.
4. Solder that end to a header pin or a protoboard scrap. Heat pad and lead together, feed solder into the joint, remove the solder, remove the iron, hold still until the fillet freezes.
5. Photograph the joint next to the solder-joint figure, or hold the figure on your phone in the same frame. Say out loud which side yours matches. If it is dull, balled, or sitting on the pad without wetting, pump the solder off and make one new attempt. If the pad lifts, stop, move to a fresh pad, and write "lifted pad" with how many seconds you think you stayed.
6. Beep continuity from the free end of the wire to the free end of the pin. A beep with a bad shape still fails. An open shiny joint fails the other way.
7. If the joint is on a free lead, add heat-shrink. File the photo as `ch01-08-joint`.

Observations you write down: alloy, whether the fillet matched the good side, the continuity result, and any fault you actually produced (bridge, lift, poor wetting, browned insulation). Faults are data. A page that says only "ok" does not pass.

## Worked example

A TT lead was tinned and soldered to a male pin that will plug into the driver. The joint is grey and rounded. The meter beeps. At light load, near the 110–150 mA no-load band of one TT 1:48 motor, the drop is small and the cart creeps straight. The wheel then stalls against a book and the current rises to about $$1.2\,\mathrm{A}$$. Measuring across the joint gives roughly $$0.4\,\Omega$$.

$$
V_{\mathrm{drop}} = 1.2 \times 0.4 = 0.48\,\mathrm{V}
$$

$$
P = 1.2 \times 0.48 \approx 0.58\,\mathrm{W}
$$

Half a watt in a grain-of-rice blob gets hot. That motor sees half a volt less than its partner, so the diff-drive pulls to one side while both PWM commands match. The repair is to pump the joint clear, tin the strands properly, form a concave fillet, sleeve it, and add a strain-relief loop. Beep again only after the metal has cooled and you are no longer holding it.

## Exercises

1. List the contact order for one joint: what the iron touches, where the solder wire touches, which item leaves first, and when you may move the lead. One swap is enough to fail the answer.
2. A joint is $$0.5\,\Omega$$ and one TT motor stalls at $$1.0\,\mathrm{A}$$. Compute the drop and the power in the joint. Would a continuity beep have caught it?
3. You soldered a header and only then remembered the heat-shrink. What do you do, and where must a pull land once the lead is covered?
4. A friend wants the Dupont crimp on a motor lead tinned "so it never falls out." Refuse in two sentences and name the joint you would make instead.
5. Name the fault for each clue: copper foil peeled off the scrap board; a dull sandy surface; solder joining two header pins; the wire jacket brown next to an otherwise shiny fillet.

<details markdown="1">
<summary>Hints and answers</summary>

1. The iron touches pad and lead together. Solder feeds into the joint, not onto the iron as the main supply of metal. Solder leaves first, then the iron. The lead stays still until the fillet has frozen.
2. $$V = 1.0 \times 0.5 = 0.5\,\mathrm{V}$$ and $$P = 0.5\,\mathrm{W}$$. A beep only says a path exists. It does not see half an ohm.
3. If the housing blocks the tube, cut the joint and remake it with heat-shrink already parked on the wire. The tie or the loop pulls on the insulation, not on the fillet.
4. Solder wicks into a crimp and the strands break beside it. Crimp with the right tool, or solder the motor lead to a header pin or a pad and add strain relief. Do not tin the crimp.
5. Peeled foil is a lifted pad, from heat or from force. A sandy surface is a cold joint. Solder between pins is a bridge. Brown jacket is burned insulation, even when the fillet itself looks right.

</details>

## Further reading

- [Adafruit guide to excellent soldering](https://learn.adafruit.com/adafruit-guide-excellent-soldering) — fillets, cold joints, and tip care in photographs. Match your lab photo to theirs as well as to this lesson's figure.
- [SparkFun through-hole soldering](https://learn.sparkfun.com/tutorials/how-to-solder-through-hole-soldering/all) — the same heat-then-feed order, with the defects named.
- [Pololu TB6612FNG carrier](https://www.pololu.com/product/713) — the header you are practising toward. Motor pads are still not today's scrap exercise.

## Where to buy in Vietnam

Prices below were read on Hshop on **23 September 2026**. They will move. Confirm the live page before you pay. The rest of the robot is Chapter 00, lesson 05, [Bill of materials and how to buy the kit in Vietnam]({% multilang_post_url contents/chapter00/00_05_bom_and_shopping %}). This list is only the bench for the joint.

- 60 W iron, WADFOW WEL3616, 75,000₫: [Hshop](https://hshop.vn/mo-han-60w-wadfow-wel3616-soldering-iron)
- Round stand with sponge, 40,000₫: [Hshop](https://hshop.vn/de-gac-mo-han-tron-b-2-co-khay-roi)
- Sunchi 0.8 mm Sn63/Pb37, 24,000₫: [Hshop](https://hshop.vn/thiec-han-sunchi-kp26-0-8mm-sn63-pb37-solder-wire)
- Handskit GS-107 desoldering pump, 55,000₫: [Hshop](https://hshop.vn/hut-thiec-handskit-gs-107-desoldering-pump)
- 170 mm flush cutter, 35,000₫: [Hshop](https://hshop.vn/kim-cat-day-dien-nho-170-cat-chan-linh-kien-dien-tu)
- RELIFE RL-426A paste, 25,000₫: [Hshop](https://hshop.vn/mo-han-relife-rl-426a-30g-chinh-hang). Confirm the jar is flux paste. The slug says `mo-han`; do not buy it thinking it is the iron.

The same two searches, if Hshop is out of stock: [Shopee, mỏ hàn 60W](https://shopee.vn/search?keyword=mo%20han%2060W) and [Shopee, thiếc hàn](https://shopee.vn/search?keyword=thiec%20han). On Lazada, open the [catalog search](https://www.lazada.vn/catalog/?q=) and type the same keywords yourself. Shop fronts: [Hshop](https://hshop.vn/), [Thế Giới IC](https://www.thegioiic.com/), [IC Đầy Rồi](https://icdayroi.com/). A header strip and a scrap of protoboard can come from those fronts; this page does not invent a product link for them. Eye protection is not optional because it was left off the price list.
