---
layout: post
title: "Steppers and microstepping intuition"
chapter: "05"
order: 4
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter05
lesson_type: required
draft: false
---

Whenever a machine needs open-loop precision down to hundredths of a millimeter — 3D printers, CNC routers, laser cutters, and lab pipetting arms — you will almost always find **stepper motors**. Instead of spinning freely when voltage is applied, a stepper rotates in discrete magnetic detents (typically 200 full steps per revolution, or $$1.8^\circ$$ per step), allowing a microcontroller to command exact position simply by counting `STEP` pulses.

This lesson explains bipolar stepper physics, **microstepping** (sinusoidal current shaping), and why steppers trade low-speed precision for lower efficiency and missed-step risk compared to closed-loop DC encoder motors.r

---

A stepper motor moves in counted angles. You tell it how many steps to take, and you trust that it took them. This lesson covers the 1.8 degree hybrid motor, what microstepping actually smooths, how to set the coil current on an A4988-style board without guessing at the potentiometer, and why Capstone A's wheels stay with DC motors and encoders.

## Learning objectives

1. Convert 1.8 degrees per full step into 200 full steps per revolution, and say what an output shaft does after a gearbox.
2. Explain microstepping as a smoothness setting (1/2, 1/4, 1/16) whose holding torque is still the motor's holding torque.
3. Compute the A4988 reference voltage for a chosen current when the sense resistors are $$0.068~\Omega$$, and know to remeasure if a clone uses $$0.1~\Omega$$.
4. Name the open-loop failure: missed steps under load look quiet and leave you at the wrong position.

## Prerequisites

You can measure a small DC voltage, down near half a volt, with the meter black lead on ground. Ohm's law and the stall-current idea from the DC motor lesson transfer directly to "current in a coil." You do not need a stepper on the desk. A photo of an A4988 or DRV8825, plus the calculation, completes the lab. If you do have a bare NEMA17, you can count one revolution.

## Key ideas: Electromagnetic Detents, Sinusoidal Microstepping, and Pull-Out Torque Curves

Three physical ideas explain both the magic and the limits of stepper motors:

- **Full Steps & Microstepping Geometry:** A standard NEMA-17 motor has 50 rotor teeth and 2 stator phases (A and B), giving $$200\text{ full steps/rev}$$ ($$1.8^\circ/\text{step}$$). A current-controlled driver (`A4988`, `TMC2209`) energizes phases sinusoidally — $$I_A = I_{\max}\cos\phi$$, $$I_B = I_{\max}\sin\phi$$ — subdividing each full step into $$M = 8, 16, \text{ or } 32$$ **microsteps** for silky-quiet motion.
- **Holding Torque vs. Incremental Microstep Torque:** Microstepping smooths vibration dramatically, yet incremental torque per microstep shrinks approximately as $$\sin(\pi / (2M))$$ — meaning 1/16 microstepping delivers smooth motion but cannot overcome heavy static friction with a single microstep.
- **Open-Loop Slip & High-Speed Torque Roll-Off:** Because coil inductance $$L$$ opposes rapid current reversals at high step rates, stepper torque drops steeply with RPM. If load torque exceeds pull-out torque, the rotor silently **misses steps** with no encoder to warn the firmware.r

---

## Why this matters for Capstone A and the ROS path

Capstone A drives with DC gearmotors and encoders. The encoder closes the loop that a stepper pretends not to need. Steppers come back when you add a small arm, a pen lift, or a camera slide: a joint that should hold position with the power on and move a known angle. ROS joint trajectories assume you know steps per revolution of the output shaft after gearing. If you advertise 200 steps per revolution on a shaft that is behind a 50:1 gearbox, the arm will move a tiny fraction of the angle the planner drew. Getting the current limit right is what keeps that joint from missing steps while the trajectory still "succeeds" in software.

## Full steps and the quiet way to lose them

A common hybrid stepper is marked 1.8 degrees per full step.

$$
\frac{360^\circ}{1.8^\circ} = 200
$$

full steps per revolution of the motor shaft. Drivers such as the Allegro A4988 and the TI DRV8825 are chopper bridges: they switch the coil voltage so the current in each winding stays near a limit you set. The STEP pin advances the translator. The DIR pin chooses the sign. The motor holds by keeping current in the coils even when the shaft is standing still, which is why a powered stepper is warm at rest.

Microstepping (1/2, 1/4, 1/8, 1/16 on a typical A4988, and finer modes on a DRV8825) divides each full step into smaller current patterns so the motion sounds smoother and the resonance is kinder. It does not multiply holding torque by 16. The torque you can fight with your fingers is still set by the motor, the current limit, and the supply. Under a heavy hand the rotor can fall behind the electrical step. Nothing in the driver raises an error flag. The mechanism is now at the wrong angle, and the program's step counter still believes the trajectory. That is open loop. An encoder, if you add one, is what turns the lie into a number you can see.

On the A4988 the MS1, MS2, and MS3 pins select the divisor. The silkscreen table is the authority for your board; the usual pattern runs from all low (full step) up to all high (1/16). Leave those pins in a known state. A floating MS pin is a random microstep mode.

## The current-limit potentiometer

Pololu-style A4988 boards use $$0.068~\Omega$$ sense resistors under the chip. The current limit and the voltage on the potentiometer wiper are related by

$$
I_{max} = \frac{V_{ref}}{8 \times 0.068} = \frac{V_{ref}}{0.544}
$$

You set $$V_{ref}$$ with the small pot, measured from the wiper to ground, with the driver powered and the motor coils connected, unless your vendor's note tells you a different safe procedure. Clone boards sometimes fit $$0.1~\Omega$$ sense resistors. In that case the 0.544 in the denominator is wrong for your PCB, and you recompute $$8 \times R_{sense}$$ from the product note before you turn the pot. A pot turned to the stop "to be strong" can set a current the motor cannot shed as heat.

Never unplug a coil while the driver is enabled. The winding is an inductor, and opening it under current throws an inductive kick into the chip. Disable the driver, or remove VM, before you rearrange motor wires.

## A geared unipolar demo is a different animal

The 28BYJ-48 sold with a ULN2003 board is a small 5 V unipolar motor with a plastic gearbox. It is a friendly desk demo: five wires, a darlington array, and slow motion you can count by eye. It is a poor drive wheel for Capstone. The gearbox is built for a clockwork load, the current pattern is unipolar stepping through the ULN2003, and the output speed and torque do not belong under a robot chassis. Enjoy it as a "steps are real" experiment. Put the TT motors back on the H-bridge for the robot that has to roll.

## Worked example

You want a 1.0 A current limit on a Pololu-style A4988 with $$0.068~\Omega$$ sense resistors.

$$
V_{ref} = I_{max} \times 0.544 = 1.0 \times 0.544 = 0.544~\mathrm{V} \approx 0.54~\mathrm{V}
$$

Meter black on GND, red on the pot wiper, driver powered, coils connected (or follow the vendor if they insist on a specific order). Turn the pot until you read about 0.54 V. If the board's note says the sense resistors are $$0.1~\Omega$$, recompute:

$$
V_{ref} = I_{max} \times (8 \times 0.1) = 0.80~\mathrm{V}
$$

for the same 1.0 A. Using 0.54 V on that clone would set the current lower than you think; using a pot at maximum could set it much higher. Write the resistor value you assumed next to the voltage you measured.

For a later ROS joint, also write steps per output revolution. A 200-step motor at 1/16 microstep takes $$200 \times 16 = 3200$$ microsteps per motor revolution. Behind a 50:1 gearbox that is $$3200 \times 50 = 160000$$ microsteps per revolution of the output shaft. The trajectory converter needs the output number, not the bare 200.

## Figures

![Digital multimeter, the instrument you use on the current-limit potentiometer]({{ site.imgurl }}/wikimedia/Digital_Multimeter_Aka.jpg)

Black probe on the driver ground. Red probe on the potentiometer wiper, not on VM. You are looking for a fraction of a volt. If you read battery voltage, you are on the wrong pin.

## Lab

### Safety

If a driver is powered, do not disconnect a motor coil. Set the current limit before you command a long move. Keep VM within the driver range (A4988 modules are often used near 8–12 V; read your board). A 28BYJ-48 stays on 5 V. Wheels of the Capstone robot are not involved.

### BOM

| Item | Role |
|------|------|
| Multimeter | $$V_{ref}$$ |
| A4988 or DRV8825 module, if you have one | Pot and MS pins |
| Stepper with four coil wires, optional | One counted revolution |
| Or a clear photo of such a module | Identification path |
| Notebook | Resistor value, $$V_{ref}$$, step count |

### Steps

1. If you have no hardware, draw the pot and the MS pins from a product photo. Compute $$V_{ref}$$ for 1.0 A assuming $$0.068~\Omega$$, and write the alternate 0.80 V figure for a $$0.1~\Omega$$ clone. Stop here.
2. If you have hardware, find the sense-resistor marking or the product note. Record $$R_{sense}$$.
3. Connect the coils in the pairs the datasheet calls one winding (resistance is a few ohms between the two wires of a pair, and open between windings). Power the driver the way the vendor recommends and measure $$V_{ref}$$. Adjust only if you understand the target.
4. Set full-step mode. Step 200 times at a slow pace and watch a flag on the shaft. A bare 1.8 degree NEMA17 should return to the flag after about 200 steps. A geared 28BYJ-48 will not.
5. Pinch the shaft gently during a slow move and see whether the flag ends in the wrong place while the code still finishes. That is a missed step. Release before the driver or the motor is hot.

### Expected results

A written $$V_{ref}$$ target for 1.0 A with the resistor value you assumed, and either a photo with the pot and MS pins labeled or a counted revolution (about 200 full steps on a bare NEMA17). A sentence that says missed steps do not raise a fault by themselves.

### Faults

| What you see | What to check |
|--------------|----------------|
| Shaft buzzes and does not turn | Coil pairs swapped, current limit near zero, or sleep/enable held in reset. |
| Motor and chip get hot at idle | $$V_{ref}$$ is far above the motor's rated current. Reduce it. |
| Motion is smoother than full step but weak under a finger | Microstepping is on. Torque was not multiplied. |
| Position drifts only when loaded | Missed steps. Lower the speed, raise current only up to the motor rating, or add an encoder. |
| Meter shows VM on the pot | The red probe is on the wrong contact. Move to the wiper and measure to GND. |

## Explanation: Computing Step Rate, Linear Resolution, and Microstepping Phase Currents

Let's calculate the exact step frequency and phase currents for a 1/16 microstepping NEMA-17 actuator in four steps:

1. **Compute effective microsteps per revolution:** $$N_{\mu} = N_{\text{full}} \times M$$.
2. **Convert target RPM to `STEP` pulse frequency:**
   $$f_{\text{step}} = \frac{\text{RPM}}{60} \times N_{\mu}.$$
3. **Compute linear resolution** (for a lead screw of pitch $$P$$ or pulley of diameter $$D$$):
   $$\Delta x = \frac{\text{travel/rev}}{N_{\mu}}.$$
4. **Verify sinusoidal coil currents at microstep $$k$$:** $$I_A = I_{\max}\cos\!\left(\frac{k\pi}{2M}\right)$$, $$I_B = I_{\max}\sin\!\left(\frac{k\pi}{2M}\right)$$, keeping total power $$I_A^2 + I_B^2 = I_{\max}^2$$ constant!

### Concrete Worked Example: NEMA-17 with 1/16 Microstepping Driving a 60 mm Wheel at 120 RPM

Parameters: $$N_{\text{full}} = 200$$ steps/rev, microstepping $$M = 16$$, phase peak current $$I_{\max} = 1.00\text{ A}$$, wheel diameter $$D = 60\text{ mm}$$ (circumference $$\pi \times 60 = 188.5\text{ mm}$$):

- **Step 1 — Microsteps per revolution and linear step size:**
  $$N_{\mu} = 200 \times 16 = 3\,200\text{ microsteps/rev}.$$
  $$\Delta x = \frac{188.5\text{ mm}}{3\,200} \approx 0.0589\text{ mm/microstep}.$$
- **Step 2 — Required `STEP` pulse rate for 120 RPM (2 rev/s):**
  $$f_{\text{step}} = 2\text{ rev/s} \times 3\,200 = 6\,400\text{ Hz}\;\; (\text{one pulse every } 156.25\,\mu\text{s}).$$
- **Step 3 — Coil currents at microstep $$k = 4$$ (one quarter of a full step, $$\phi = 4\pi/32 = 22.5^\circ$$):**
  $$I_A = 1.00 \cos(22.5^\circ) \approx 0.924\text{ A}, \qquad I_B = 1.00 \sin(22.5^\circ) \approx 0.383\text{ A}.$$
  Check constant-power identity: $$0.924^2 + 0.383^2 = 0.854 + 0.147 \approx 1.00 = I_{\max}^2$$!

**Common Pitfall:** Unplugging a stepper motor's 4-pin cable *while the driver is powered ON* — breaking an energized inductive coil generates an instant high-voltage flyback spike that destroys `A4988`/`TMC2209` output MOSFETs. Always power off before touching stepper cables!

**Quick Check:** Why do mobile battery robots usually prefer DC gearmotors with encoders over NEMA-17 steppers? Because steppers draw near-full holding current *even while standing completely still*, draining a 2S battery 3×–5× faster than a DC motor idling at 0 A!

---

## Mua ở Việt Nam / Where to buy in Vietnam

You can finish this lesson with no purchase. If you want a desk demo, a 28BYJ-48 with ULN2003 is the cheap unipolar kit. A NEMA17 plus an A4988 is the hybrid setup that matches the 200-step count. Prices move. Rough bands: 28BYJ-48 kit about 25.000–50.000 VND, A4988 module about 20.000–55.000 VND, NEMA17 often 150.000–400.000 VND depending on body length.

- HShop: [A4988](https://hshop.vn/search?q=A4988), [28BYJ-48](https://hshop.vn/search?q=28BYJ-48), [NEMA17](https://hshop.vn/search?q=NEMA17)
- Shopee: [A4988](https://shopee.vn/search?keyword=A4988), [28BYJ-48](https://shopee.vn/search?keyword=28BYJ-48)
- Lazada: [A4988](https://www.lazada.vn/catalog/?q=A4988), [DRV8825](https://www.lazada.vn/catalog/?q=DRV8825)
- Thế Giới IC: [A4988](https://www.thegioiic.com/search?q=A4988), [ULN2003](https://www.thegioiic.com/search?q=ULN2003)

## Exercises

1. How many full steps does a 1.8 degree motor take per revolution? How many 1/16 microsteps is that?
2. Sense resistors are $$0.068~\Omega$$ and you measure $$V_{ref} = 0.30~\mathrm{V}$$. What current limit did you set?
3. A clone note says $$R_{sense} = 0.1~\Omega$$. What $$V_{ref}$$ gives 0.8 A?
4. The arm finishes a 400-step program and the tip is short of the mark, with no error printed. What physical event fits those facts?
5. You plan a ROS joint on a 200-step motor, full step, 30:1 gearbox. How many steps is one output revolution?

### Answer guidance

A 1.8 degree motor takes 200 full steps and $$200 \times 16 = 3200$$ microsteps of 1/16. With $$0.068~\Omega$$, $$I_{max} = 0.30 / 0.544 \approx 0.55~\mathrm{A}$$. For $$0.1~\Omega$$, $$V_{ref} = 0.8 \times 0.8 = 0.64~\mathrm{V}$$. A quiet shortfall is missed steps in open loop. One output revolution at full step behind 30:1 gearing is $$200 \times 30 = 6000$$ steps.

## Further reading

- Pololu A4988 carrier, including the current-limit section and the $$V_{ref}$$ formula: [https://www.pololu.com/product/1182](https://www.pololu.com/product/1182)
- TI DRV8825 datasheet (chopper stepper drive and microstep modes): [https://www.ti.com/lit/ds/symlink/drv8825.pdf](https://www.ti.com/lit/ds/symlink/drv8825.pdf)
- SparkFun motor selection, for torque and current language you can compare with the DC lessons: [https://learn.sparkfun.com/tutorials/motors-and-selecting-the-right-one/all](https://learn.sparkfun.com/tutorials/motors-and-selecting-the-right-one/all)
