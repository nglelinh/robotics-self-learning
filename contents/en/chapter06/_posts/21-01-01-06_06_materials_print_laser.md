---
layout: post
title: "Chassis materials: 3D-print vs laser-cut"
chapter: "06"
order: 6
owner: "Nguyen Le Linh"
lang: en
categories:
  - chapter06
lesson_type: required
draft: false
---

Estimated time: **70–90 minutes**. You can finish the lab from a photo of a broken printed part. Owning a printer is optional.

## Learning objectives

By the end of this lesson you can choose a bought acrylic 2WD plate for Capstone A and reserve 3D printing for brackets, sensor mounts, and a battery strap. You can predict how a 0.1–0.2 mm laser kerf changes a drawn hole, name the temperature at which PLA goes soft in a closed car, and orient a motor mount so bolt tension does not peel the printed layers apart.

## Prerequisites

You know the chassis geometry from Lesson 01 and the M3 fastener habit from Lesson 02. You do not need a CAD license. A pencil sketch with a thickness labeled in millimeters is enough.

## Why this matters for Capstone A and the ROS path

Capstone A has to roll this month. A printed copy of an entire chassis spends the week on a machine you may not have, and a PLA plate left in a parked car can warp before the URDF is finished. Buy the acrylic 2WD frame. Print the pieces the kit does not include: a bracket that aims an ultrasonic sensor, a strap that stops the battery from sliding (Lesson 07), a small cover over a solder joint. ROS never sees the polymer name. It sees wheel positions. A cracked motor mount changes those positions and the $$b$$ you measured becomes a lie. Material choice is how $$b$$ stays the number in `diff_drive_controller`.

## Acrylic plate, printed bracket

Cast acrylic around 3 mm is the usual kit plate. It is flat, it laser-cuts cleanly, and it is brittle. A screw tightened in a hole that is already tight wedges the plastic and a crack runs between holes. Give every M3 a clearance hole and a nut on the far side, the nyloc from Lesson 02. Acrylic is a poor snap-fit material. Design clips in PETG or keep clips out of the Capstone.

Laser kerf is the width of material the beam removes, often 0.1–0.2 mm on a hobby cutter in acrylic. Shops cut the path you drew. A hole whose drawn diameter is the path diameter comes out larger by about that kerf:

$$
d_{\text{cut}} \approx d_{\text{drawn}} + k.
$$

Draw a 3.2 mm clearance hole and a 0.2 mm kerf yields about 3.4 mm, which an M3 screw still passes through cleanly. Draw a 3.0 mm hole because you wanted the screw to bite the acrylic, and the cut lands near 3.2 mm, the screw rattles, and over-tightening starts the crack. Tell the shop the thickness, send DXF in millimeters, and keep paths closed. An open contour is a request the machine finishes in a direction you did not choose.

PLA prints easily and softens in a closed car, around 55–60 °C, which is a normal afternoon in Vietnam. A bracket that was square at breakfast can creep by the time lab starts. PETG tolerates that heat better and strings more while printing, so the part needs a few minutes with a knife. For a motor mount the hidden requirement is orientation. Fused filament is weakest between layers. Bolt tension and motor torque that peel one layer off the next will split the ear of the bracket. Turn the model so the plane that tension would crack cuts across the layer lines. The crack then has to break a strand, not unzip a bond. A mount printed “flat and pretty” with the ear standing on layer boundaries is the one that fails on the first stall.

You can do all of this without a printer. A campus lab or a shop will take an STL in millimeters and a named material, PLA or PETG, and a note about orientation if you care. A laser shop wants DXF, millimeters, closed paths, and a stated sheet thickness. Put those words in the email so the first cut is the one you measured.

![The plate you are deciding not to reprint: measure it, then print only the brackets it lacks]({{ site.imgurl }}/generated/chassis_measures.png)

The figure is the bought chassis. $$b$$ and $$r$$ are properties of how that plate holds the wheels. A printed part is allowed to hold a sensor. It is a risky place to reinvent the axle line a week before Chapter 07.

## Worked example

You send a motor-slot drawing with an M3 hole at $$d_{\text{drawn}} = 3.2$$ mm. The shop quotes kerf $$k = 0.15$$ mm.

$$
d_{\text{cut}} \approx 3.2 + 0.15 = 3.35\ \text{mm}.
$$

An M3 screw is about 3.0 mm on the crest, so 3.35 mm is a comfortable clearance. The nut does the clamping. If instead you draw 2.8 mm hoping for a threaded bite in acrylic,

$$
d_{\text{cut}} \approx 2.8 + 0.15 = 2.95\ \text{mm},
$$

and the screw either will not start or will wedge. That wedge is the crack. On the printed battery strap, PLA at 58 °C in a closed cabin is at the softening range. PETG is the material you name for that strap if the robot ever waits in a car. The plate itself stays the acrylic kit.

## Lab: read a broken layer, sketch the orientation

### Safety

Broken plastic is sharp along the layer that failed. Handle the edge, not the sliver. If you visit a laser shop, the bed and the offcut are hot; let the operator hand you the part. No printer is required, and no solvent is required. Do not “weld” acrylic with random glue while you are still identifying the failure.

### BOM

| Item | Role |
|------|------|
| A broken printed part, or a clear photo of one | The layer autopsy |
| Pencil, side view and front view | Bracket orientation |
| `lab-notes.md` | Kerf arithmetic and the material sentence |

### Steps

1. Look at the break. Layer lines are the fine stripes. Decide whether the crack ran between stripes or across them. Between stripes means the load peeled the weak plane.
2. Sketch a TT motor bracket: a wall on the chassis and an ear the motor bolts to. Mark the bolt axis. Draw the layer lines so they cross the plane the bolt would split. Write “print this face down” on the face that should touch the bed to make those lines.
3. Compute one kerf example for a hole you care about, using $$k = 0.2$$ mm if the shop has not told you their number. Record drawn diameter and expected cut diameter.
4. Write the Capstone material plan in one sentence: bought acrylic chassis; printed material and part name for the bracket and the battery strap.
5. If you have neither a part nor a photo, use any failed print picture you can find in a lab, and say so.

### Expected results

A note that names the weak plane, a sketch with bed face and layer direction marked, and a kerf pair such as 3.2 mm drawn and 3.4 mm expected. The material sentence specifies acrylic for the plate and PLA or PETG for the bracket, with PETG called out if the strap sees a hot car.

### Faults

| What you see | What it usually means |
|--------------|------------------------|
| Crack follows the stripes | Layers were the split plane; rotate the part |
| Hole is tight and the acrylic crazes | Drawn hole ignored kerf, or the screw was used as a thread |
| Bracket warped after a sunny commute | PLA above about 55–60 °C |
| Shop cut the outline and skipped holes | Open paths, or holes on a layer the shop had turned off |
| STL came back tiny | The file was in inches, or in centimeters, and the shop followed the numbers |

## Mua ở Việt Nam / Where to buy in Vietnam

Spend the money on the acrylic 2WD chassis. Buy filament only if you, or your lab, will print the brackets. A laser job is a service, priced by the shop from your DXF; bring thickness and millimeter units in the same sentence as the file.

| What | Keywords | Rough band (VND) | Notes |
|------|----------|------------------|-------|
| 2WD acrylic chassis | `khung xe robot 2 bánh` | 80.000–200.000 | The Capstone plate |
| PLA filament, 1 kg | `nhựa PLA` | 250.000–450.000 | Easy; keep it out of a closed car |
| PETG filament, 1 kg | `nhựa PETG` | 280.000–500.000 | Better heat, more stringing |

Search pages:

- [Hshop: khung](https://hshop.vn/search?q=khung+xe+robot)
- [Shopee: nhựa PLA](https://shopee.vn/search?keyword=nh%E1%BB%B1a%20PLA)
- [Lazada: nhựa PLA](https://www.lazada.vn/catalog/?q=nh%E1%BB%B1a%20PLA)
- [Thế Giới IC](https://www.thegioiic.com/search?q=nh%E1%BB%B1a%20PLA)

Prices move. A local laser shop is often a sign on a makerspace door rather than a nationwide SKU. Ask for DXF, millimeters, closed paths, and the sheet thickness they stock, commonly 3 mm acrylic.

## Exercises

1. Drawn hole 3.4 mm, kerf 0.2 mm. What diameter do you expect on the acrylic, and does an M3 screw still pass?
2. You need the screw to bite printed plastic. What hardware from Lesson 02 replaces “threads cut in PLA by the screw itself”?
3. A motor ear cracked cleanly along the layer stripes the first time the wheel stalled. What was the weak plane, and how do you orient the reprint?
4. The robot sits in a car at about 58 °C. Which filament is the risky one for the battery strap, and which do you name instead?
5. List the file type, the unit, and the extra sentence you send a laser shop, then the file type and the two facts you send a print shop.

### Answer guidance

1. About 3.6 mm. An M3 crest is near 3.0 mm, so the screw passes with extra clearance; keep a nut on the back. 2. A brass heat-set insert, then a machine screw, with a nyloc if the joint vibrates. 3. The interlayer bond was the crack plane. Reprint so layer lines cross that plane; mark the face that goes down on the bed. 4. PLA softens around 55–60 °C. Name PETG for that strap. 5. Laser: DXF, millimeters, closed paths, and the thickness. Print: STL, millimeters, and a named material, plus orientation if the shop will honor it.

## Further reading

- [RepRap print troubleshooting](https://reprap.org/wiki/Print_Troubleshooting) — layer splits, stringing, and the symptoms you just diagnosed.
- [Polylactic acid](https://en.wikipedia.org/wiki/Polylactic_acid) — why PLA’s useful temperature sits near a hot cabin.
- [Laser cutting](https://en.wikipedia.org/wiki/Laser_cutting) — kerf as removed width, which is the correction in the worked example.
