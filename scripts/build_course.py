#!/usr/bin/env python3
"""Build full bilingual robotics self-learning Jekyll course."""
from __future__ import annotations
import json, re, textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CUR = json.loads((ROOT / "scripts" / "curriculum.json").read_text(encoding="utf-8"))
OWNER = "Nguyen Le Linh"
EMAIL = "nglelinh@gmail.com"
BASE = "robotics-self-learning"
URL = "https://nglelinh.github.io"

LINKS = {
    "ros2_jazzy": "https://docs.ros.org/en/jazzy/",
    "ros2_tutorials": "https://docs.ros.org/en/jazzy/Tutorials.html",
    "nav2": "https://docs.nav2.org/",
    "gazebo": "https://gazebosim.org/docs/harmonic/",
    "microros": "https://micro.ros.org/",
    "esp32": "https://docs.espressif.com/projects/esp-idf/en/latest/esp32/",
    "pico": "https://www.raspberrypi.com/documentation/microcontrollers/raspberry-pi-pico.html",
    "arduino": "https://docs.arduino.cc/",
    "platformio": "https://docs.platformio.org/",
    "lerobot": "https://github.com/huggingface/lerobot",
    "hf_lerobot": "https://huggingface.co/docs/lerobot",
    "duckietown": "https://docs.duckietown.com/",
    "mit_manip": "https://manipulation.mit.edu/",
    "moveit2": "https://moveit.picknik.ai/main/index.html",
    "urdf": "https://docs.ros.org/en/jazzy/Tutorials/Intermediate/URDF/URDF-Main.html",
    "tf2": "https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-TF2.html",
    "linorobot2": "https://github.com/linorobot/linorobot2",
    "sparkfun_logic": "https://learn.sparkfun.com/tutorials/logic-levels",
    "pololu_motor": "https://www.pololu.com/docs/0J44",
    "pid": "https://www.ni.com/en/shop/labview/pid-theory-explained.html",
    "mqtt": "https://mqtt.org/",
    "opencv": "https://docs.opencv.org/4.x/",
    "aloha_act": "https://tonyzhaozh.github.io/aloha/",
    "diff_policy": "https://diffusion-policy.cs.columbia.edu/",
    "rt1": "https://robotics-transformer1.github.io/",
    "openx": "https://robotics-transformer-x.github.io/",
    "bt_cpp": "https://www.behaviortree.dev/",
    "slam_toolbox": "https://github.com/SteveMacenski/slam_toolbox",
}

def img(path, alt):
    return f"![{alt}]({{{{ site.imgurl }}}}/{path})"

# Map lesson slug -> list of (relpath, alt) images + lab flag + topic tags
META = {}

def M(slug, images=None, lab=False, tags=None, links=None):
    META[slug] = {
        "images": images or [],
        "lab": lab,
        "tags": tags or [],
        "links": links or [],
    }

# Chapter 00
M("welcome_and_outcomes", images=[("generated/kit_catalog_overview.png","Course kit overview")],
  links=["ros2_jazzy","lerobot","duckietown"])
M("learning_tracks_budget", links=["linorobot2","microros","platformio"])
M("safety_mindset_lab", lab=True, images=[("wikimedia/Soldering_iron.jpg","Soldering iron (Wikimedia)")], links=["sparkfun_logic"])
M("kit_catalog_tooling", lab=True,
  images=[("generated/kit_catalog_overview.png","Bench kit families"),
          ("wikimedia/Digital_Multimeter_Aka.jpg","Digital multimeter"),
          ("wikimedia/breadboard.jpg","Solderless breadboard"),
          ("wikimedia/Soldering_iron.jpg","Soldering iron")],
  links=["arduino","pololu_motor"])
M("bom_and_shopping", images=[("generated/kit_catalog_overview.png","BOM families")], links=["pololu_motor"])
M("workspace_toolchain_preview", links=["platformio","ros2_tutorials","esp32","pico"])
M("ch00_lab_checklist", lab=True)

# Chapter 01 — heavy ID
M("voltage_current_ohm", images=[("generated/ohms_law_triangle.png","Ohm's law triangle")], lab=True)
M("breadboard_meter", lab=True,
  images=[("generated/breadboard_anatomy.png","Breadboard anatomy"),
          ("wikimedia/Digital_Multimeter_Aka.jpg","Multimeter"),
          ("wikimedia/breadboard.jpg","Breadboard photo")])
M("resistor_color_smd", lab=True,
  images=[("generated/resistor_color_code.png","Resistor color code chart"),
          ("wikimedia/resistors_assortment.jpg","Resistor assortment")])
M("cap_diode_led_id", lab=True,
  images=[("generated/capacitor_polarity.png","Capacitor polarity"),
          ("wikimedia/Electrolytic_capacitor.jpg","Electrolytic capacitor"),
          ("wikimedia/LEDs.jpg","LEDs"),
          ("generated/component_lookalikes.png","Lookalikes")])
M("transistor_mosfet_ic_id", lab=True,
  images=[("generated/component_lookalikes.png","Package lookalikes")],
  links=["sparkfun_logic"])
M("connectors_drivers_boards", lab=True,
  images=[("generated/hbridge_concept.png","H-bridge concept"),
          ("wikimedia/Dosmotorsl298n.jpg","L298N-style driver"),
          ("generated/pcb_mcu_anatomy.png","MCU board anatomy"),
          ("wikimedia/ESP32_on_Lolin32_Lite_clone_board_cropped.jpg","ESP32 board"),
          ("wikimedia/Raspberry_Pi_Pico.jpg","Raspberry Pi Pico")])
M("datasheet_pinouts", links=["esp32","pico","arduino"])
M("soldering_basics", lab=True, images=[("wikimedia/Soldering_iron.jpg","Soldering iron")])
M("esd_polarity_brownout", links=["sparkfun_logic"])
M("component_id_lab", lab=True,
  images=[("generated/resistor_color_code.png","Color code"),
          ("generated/component_lookalikes.png","Lookalikes"),
          ("wikimedia/resistors_assortment.jpg","Resistors")])
M("ch01_lab_checklist", lab=True)

# Ch 02-05
M("mcu_landscape", images=[("generated/pcb_mcu_anatomy.png","MCU PCB anatomy"),
    ("wikimedia/ESP32_on_Lolin32_Lite_clone_board_cropped.jpg","ESP32"),
    ("wikimedia/Raspberry_Pi_Pico.jpg","Pico")], links=["esp32","pico","arduino"])
M("esp32_platformio", lab=True, links=["platformio","esp32"])
M("pico_micropython", lab=True, links=["pico"])
M("blink_serial_hello", lab=True)
M("pinouts_power_rails", images=[("generated/pcb_mcu_anatomy.png","Pin headers")], links=["sparkfun_logic"])
M("ch02_lab_checklist", lab=True)
M("cpp_vs_micropython")
M("gpio_patterns", lab=True)
M("pwm_timers", lab=True)
M("interrupts_debounce", lab=True)
M("state_machines_fw")
M("ch03_lab_checklist", lab=True)
M("bus_interfaces")
M("sensor_package_id", lab=True, images=[("generated/sensor_package_id.png","Sensor package ID sheet")])
M("encoders_counts", lab=True)
M("imu_basics", lab=True)
M("ultrasonic_tof", lab=True, images=[("generated/sensor_package_id.png","Ranging modules")])
M("cameras_robots", links=["opencv"])
M("ch04_lab_checklist", lab=True)
M("dc_hbridge", images=[("generated/hbridge_concept.png","H-bridge")], links=["pololu_motor"])
M("driver_board_id", lab=True,
  images=[("generated/hbridge_concept.png","H-bridge"),
          ("wikimedia/Dosmotorsl298n.jpg","L298N module")])
M("servos_pwm", lab=True)
M("steppers_intro")
M("current_thermal", links=["pololu_motor"])
M("closed_loop_intro", lab=True)
M("ch05_lab_checklist", lab=True)

# Ch 06 mechanisms heavy
M("chassis_anatomy", images=[("generated/diff_drive_kinematics.png","Diff-drive chassis")])
M("fasteners_bearings_shafts", images=[("wikimedia/Ball_bearing.jpg","Ball bearing")])
M("gear_trains_ratios", lab=True, images=[("generated/gear_train_ratio.png","Gear train ratio")])
M("linkages_belts_cams", images=[("generated/four_bar_linkage.png","Four-bar linkage"),
                                 ("generated/belt_pulley.png","Belt and pulley")])
M("wheels_casters_diff", images=[("generated/diff_drive_kinematics.png","Diff-drive diagram")])
M("materials_print_laser")
M("mech_failure_modes")
M("mechanisms_lab", lab=True, images=[("generated/gear_train_ratio.png","Measure gear ratio")])
M("ch06_lab_checklist", lab=True)

# Capstone + later
M("assemble_power", lab=True, images=[("generated/diff_drive_kinematics.png","Chassis")])
M("driver_bringup", lab=True)
M("teleop_protocol", lab=True)
M("teleop_firmware", lab=True)
M("field_acceptance", lab=True)
M("ch07_lab_checklist", lab=True)
M("serial_protocols")
M("wifi_mqtt", lab=True, links=["mqtt"])
M("pid_tuning", lab=True, links=["pid"])
M("diff_kinematics", images=[("generated/diff_drive_kinematics.png","Kinematics")])
M("loop_timing")
M("jazzy_install_ws", lab=True, links=["ros2_jazzy","ros2_tutorials"])
M("nodes_topics", lab=True, links=["ros2_tutorials"])
M("services_actions", links=["ros2_tutorials"])
M("launch_params_qos", links=["ros2_tutorials"])
M("tf2_frames", links=["tf2"])
M("urdf_basics", links=["urdf"])
M("gazebo_harmonic", lab=True, links=["gazebo"])
M("urdf_sim_bringup", lab=True)
M("microros_mcu", links=["microros"])
M("bridge_capstone", lab=True, links=["linorobot2","microros"])
M("sim_to_real", lab=True)
M("slam_overview", links=["slam_toolbox","nav2"])
M("nav2_tour", links=["nav2"])
M("vision_pipeline", links=["opencv"])
M("bt_peek", links=["bt_cpp","nav2"])
M("moveit_peek", links=["moveit2"])
M("lerobot_intro", links=["lerobot","hf_lerobot"])
M("imitation_act", links=["aloha_act","lerobot"])
M("diffusion_policy", links=["diff_policy"])
M("vla_overview", links=["rt1","openx"])
M("next_paths_refs", links=["ros2_jazzy","nav2","lerobot","mit_manip","duckietown","microros"])


def plan(en=True):
    if en:
        return """## 60-minute study plan

| Minutes | Activity |
|--------:|----------|
| 0–5 | Skim objectives and figures |
| 5–25 | Read core explanations; work any math |
| 25–45 | Hands-on / identification / firmware lab |
| 45–55 | Check exercises; note mistakes |
| 55–60 | Save links + 3 takeaways |
"""
    return """## Kế hoạch học 60 phút

| Phút | Hoạt động |
|-----:|-----------|
| 0–5 | Lướt mục tiêu và hình |
| 5–25 | Đọc giải thích; làm phần toán |
| 25–45 | Lab thực hành / nhận diện / firmware |
| 45–55 | Bài tập; ghi lỗi thường gặp |
| 55–60 | Lưu link + 3 ý chính |
"""


# Per-slug teaching bodies (EN). VI generated with parallel teaching text.
BODIES_EN: dict[str, str] = {}
BODIES_VI: dict[str, str] = {}

def body(slug, en, vi):
    BODIES_EN[slug] = en.strip()
    BODIES_VI[slug] = vi.strip()

# --- Content library (concise but complete teaching) ---
body("welcome_and_outcomes", f"""
This course builds **robots you can touch**: electronics → firmware → differential-drive teleop → ROS 2 Jazzy → simulation/micro-ROS → a literate overview of modern robot learning (LeRobot, ACT, Diffusion Policy, VLA).

Audience: self-learners with basic programming who want hobby → serious beginner/intermediate skills.

### Outcomes
1. Identify common parts and bench tools safely.
2. Wire and program ESP32/Pico for motors and sensors.
3. Assemble a diff-drive robot and teleoperate it **without ROS**.
4. Explain ROS 2 nodes/topics/TF/URDF and try Gazebo Harmonic.
5. Read LeRobot-style docs without mythology.

Official hubs: [ROS 2 Jazzy]({LINKS['ros2_jazzy']}), [LeRobot]({LINKS['lerobot']}), [Duckietown docs]({LINKS['duckietown']}) (autonomy patterns; optional). MIT Manipulation / Drake is an **advanced optional** track only ([site]({LINKS['mit_manip']})).
""", f"""
Khóa học xây **robot cầm được**: điện tử → firmware → teleop vi sai → ROS 2 Jazzy → mô phỏng/micro-ROS → robot learning hiện đại (LeRobot, ACT, Diffusion Policy, VLA).

### Đầu ra
1. Nhận diện linh kiện và dụng cụ bàn an toàn.
2. Lập trình ESP32/Pico cho motor và cảm biến.
3. Lắp robot vi sai và teleop **không cần ROS**.
4. Hiểu node/topic/TF/URDF và thử Gazebo Harmonic.
5. Đọc tài liệu kiểu LeRobot đúng mức.

Tài liệu: [ROS 2 Jazzy]({LINKS['ros2_jazzy']}), [LeRobot]({LINKS['lerobot']}), [Duckietown]({LINKS['duckietown']}). MIT Manipulation là track **tùy chọn nâng cao**.
""")

body("learning_tracks_budget", f"""
**Track A (budget MCU):** ESP32 or Pico + TT chassis + TB6612/DRV8833-class driver + ranging/IMU. Capstone A works offline.

**Track B (ROS):** same robot + Ubuntu 24.04 for ROS 2 Jazzy; optional Pi 5 later for onboard compute.

Shared rule: finish Capstone A before shopping LiDAR/SLAM. See [linorobot2]({LINKS['linorobot2']}) as a ROS 2 diff-drive reference architecture—not a required clone.
""", f"""
**Track A:** ESP32/Pico + khung TT + driver TB6612/DRV8833 + cảm biến. Capstone A chạy offline.

**Track B:** cùng robot + Ubuntu 24.04 / ROS 2 Jazzy; Pi 5 tùy chọn sau.

Quy tắc: xong Capstone A trước khi mua LiDAR/SLAM. Tham khảo [linorobot2]({LINKS['linorobot2']}).
""")

body("safety_mindset_lab", f"""
### Lab safety ritual
1. Eye protection when cutting/soldering; ventilate fumes.
2. Lithium packs: matched charger, fire-safe bag, never pierce/short.
3. Power **last on / first off**; lift wheels when testing motion.
4. Software E-stop: if no command for 200–500 ms → PWM = 0.
5. Never put motor voltage on 3.3 V GPIO ([logic levels]({LINKS['sparkfun_logic']})).

### Lab BOM (this lesson)
Safety glasses, iron stand, damp sponge/brass wool, meter, fire-safe surface.
""", f"""
### Nghi thức an toàn
1. Bảo vệ mắt; thông gió khi hàn.
2. Pin lithium: sạc đúng, túi chống cháy.
3. Cấp nguồn sau cùng; nhấc bánh khi test.
4. E-stop phần mềm: mất lệnh 200–500 ms → PWM = 0.
5. Không đưa điện motor vào GPIO 3.3 V.

### BOM lab: kính, đế mỏ hàn, ĐHVN, mặt bàn chịu nhiệt.
""")

body("kit_catalog_tooling", f"""
### Must-have bench kit (families, not stale store prices)
| Family | Why |
|--------|-----|
| Digital multimeter | Continuity, voltage, rough resistance |
| Temperature-controlled iron + solder + wick/flux | Harnesses, headers |
| Breadboard + Dupont jumpers | Prototyping |
| Wire strippers, flush cutters, tweezers | Mechanical + electronics |
| Hex/Phillips drivers, needle-nose | Chassis screws |
| Heat-shrink + lighter/gun | Strain relief |
| Calipers (digital OK) | Shaft/gear measurements |

### Nice-to-have / later lab
Bench PSU with current limit; USB logic analyzer; entry oscilloscope; helping hands.

### Beginner kit vs “lab kit”
Beginner: meter + iron + breadboard + jumpers + basic hand tools. Lab kit adds PSU current limit, better iron tips, calipers, organizer bins labeled by part family.
""", f"""
### Bộ bàn tối thiểu
Đồng hồ vạn năng, mỏ hàn chỉnh nhiệt + thiếc/flux, breadboard + Dupont, kìm/tuốt dây, tô vít, heat-shrink, thước kẹp.

### Nâng cấp lab
PSU có giới hạn dòng, logic analyzer, scope nhập môn.

### Beginner vs lab kit
Beginner đủ để blink/spin; lab kit giúp đo dòng và lắp cơ khí chính xác hơn.
""")

body("bom_and_shopping", f"""
Primary hardware track: **ESP32 (or Pico) + diff-drive chassis + motor driver + ultrasonic/IMU**; optional Pi 5 later.

Prefer TB6612/DRV8833-class drivers over oversized L298N when possible ([Pololu motor driver docs]({LINKS['pololu_motor']})). Buy a **chemistry-matched** charger with the pack.

Shopping rule: blink + spin week-1 parts first; defer cameras/LiDAR.
""", f"""
Phần cứng chính: **ESP32/Pico + khung vi sai + driver + siêu âm/IMU**; Pi 5 tùy chọn.

Ưu tiên TB6612/DRV8833. Mua sạc đúng hóa học pin. Tuần 1: blink + spin trước.
""")

body("workspace_toolchain_preview", f"""
Folder layout: `notes/`, `firmware/`, `ros_ws/` (later). Tool map: Arduino/PlatformIO for ESP32; MicroPython for Pico; ROS 2 Jazzy on Ubuntu 24.04; Gazebo Harmonic for sim; LeRobot on a workstation.
""", f"""
Thư mục: `notes/`, `firmware/`, `ros_ws/`. ESP32: Arduino/PlatformIO; Pico: MicroPython; ROS 2 Jazzy trên Ubuntu 24.04.
""")

body("ch00_lab_checklist", f"""
### Chapter 00 acceptance checklist
- [ ] Safety glasses + iron station ready
- [ ] Multimeter beeps on continuity
- [ ] Track A or B chosen in writing
- [ ] BOM spreadsheet started (must/nice)
- [ ] Repo `my-robot-labs` created
- [ ] Charger model photographed & labeled
""", f"""
### Checklist chương 00
- [ ] Kính + trạm hàn sẵn sàng
- [ ] ĐHVN kêu thông mạch
- [ ] Đã chọn Track A/B
- [ ] BOM spreadsheet
- [ ] Repo lab
- [ ] Ảnh ghi model sạc
""")

# Ch01 bodies
body("voltage_current_ohm", f"""
Electric potential difference \(V\), current \(I\), resistance \(R\): \(V=IR\). Power \(P=VI=I^2R=V^2/R\).

### Lab
Measure a known resistor with meter; compute expected current through LED+resistor on 3.3 V (do **not** omit series resistor on LED).
""", f"""
\(V=IR\), \(P=VI\). Lab: đo điện trở; tính dòng LED trên 3.3 V (luôn có điện trở hạn dòng).
""")

body("breadboard_meter", f"""
Breadboard columns are shorted in groups; the center trench splits sides for ICs. Meter modes: V DC, continuity diode beep, Ω.

### Lab procedure
1. Continuity-test a Dupont wire.
2. Build LED + resistor from rail to GPIO later—or to 3.3 V via resistor for passive check.
3. Measure rail voltage under no load.
""", f"""
Breadboard: cột thông theo nhóm; khe giữa cho IC. Lab: test dây Dupont; đo điện áp rail.
""")

body("resistor_color_smd", f"""
4-band THT: digit, digit, multiplier, tolerance. Example Brown-Blue-Orange-Gold → \(16\\times10^3\\Omega=16\\,\\mathrm{{k}}\\Omega\) ±5%.

SMD codes: `103` → \(10\\times10^3=10\\,\\mathrm{{k}}\\Omega\). EIA-96 less common on hobby kits.

### Lab
Decode 5 random THT resistors by eye, then confirm with ohmmeter. Note meter error on very low/high values.
""", f"""
Điện trở 4 vạch: chữ số–chữ số–bội–dung sai. SMD `103` = 10 kΩ. Lab: đoán 5 điện trở rồi đo xác nhận.
""")

body("cap_diode_led_id", f"""
Electrolytics: stripe marks **negative**. Ceramics usually non-polar. LED: flat edge / short lead often cathode; confirm with meter diode mode. Signal diode: band = cathode.

### Lookalikes
Blank brown SMD → often capacitor; coded SMD → often resistor. When unsure: datasheet + meter, never assume.
""", f"""
Tụ hóa: sọc = cực âm. LED: cạnh phẳng/chân ngắn thường cathode. Lab nhận diện: đừng đoán SMD blank.
""")

body("transistor_mosfet_ic_id", f"""
TO-92 small signal transistors vs TO-220 power packages—same plastic family can be NPN/PNP/MOSFET: **read the printing**. Regulators (e.g. 7805 family) often TO-220. ICs: notch/dot marks pin 1.

### Lab
Sort a mixed bag into: passive 2-lead, diode/LED, TO-92, TO-220, module boards. Photograph labels.
""", f"""
TO-92 vs TO-220: phải đọc chữ in. IC: khuyết/dot = chân 1. Lab: phân loại túi linh kiện hỗn hợp.
""")

body("connectors_drivers_boards", f"""
Connectors: Dupont (0.1"), JST-XH/PH (battery/sensor), XT60 (higher current packs)—**do not force mismatch**.

Driver boards: L298N (large heatsink, older), TB6612/DRV8833 (smaller, usually more efficient for small robots). MCU boards: ESP32 DevKit (USB-UART, antenna) vs Pico (dual-row 0.1" headers).

See H-bridge concept figure and compare to a physical L298N-style board if you own one.
""", f"""
Dupont / JST / XT60 không lẫn. Driver: L298N vs TB6612/DRV8833. Board: ESP32 DevKit vs Pico.
""")

body("datasheet_pinouts", f"""
Datasheet workflow: Absolute Maximum Ratings → pinout → recommended operating → timing/I2C addresses → example schematic. Never trust silk-screen alone when modules are cloned.
""", f"""
Quy trình datasheet: giới hạn tuyệt đối → pinout → điều kiện khuyến nghị → địa chỉ I2C → schematic mẫu.
""")

body("soldering_basics", f"""
Heat the joint, not only the solder. Aim for shiny wetting on pads/wires. Use flux; wick mistakes. Strain-relieve every cable that moves with the robot.
""", f"""
Hâm nóng mối hàn; thiếc bóng ướt đẫm. Dùng flux; gia cố chống kéo mọi dây chuyển động.
""")

body("esd_polarity_brownout", f"""
ESD: touch ground before CMOS pins; avoid carpet shuffle into exposed modules. Polarity mistakes kill drivers instantly. Brownouts: motors stall → voltage dips → MCU resets—“random” bugs that are power.

Bypass caps near modules; common ground between MCU and driver; separate motor supply when possible.
""", f"""
ESD, cực tính, sụt áp khi stall motor. Tụ bypass; common ground; tách nguồn motor nếu được.
""")

body("component_id_lab", f"""
### Lab BOM
Assorted THT resistors, 1 electrolytic, 1 ceramic, 2 LEDs, 1 diode, Dupont wires, meter.

### Procedure
1. Continuity map of a breadboard column.
2. Color-code decode + ohmmeter confirm (5 parts).
3. Diode/LED polarity with diode mode.
4. Write a “lookalike watchlist” from today’s parts.

### Expected observations
Meter Ω within ~5–10% of band decode for mid-range carbon films; LEDs drop ~1.8–3.2 V depending on color.
""", f"""
### Lab
Đo thông cột breadboard; đoán mã màu + đo ohm; xác định cực LED/diode; ghi danh sách dễ nhầm.
""")

body("ch01_lab_checklist", f"""
- [ ] Ohm’s law problems solved for LED resistor
- [ ] Breadboard rails understood
- [ ] 5 resistors decoded + measured
- [ ] Capacitor & diode polarity demonstrated
- [ ] Driver vs MCU boards identified by photo
- [ ] One joint soldered cleanly (or practiced on scrap)
""", f"""
- [ ] Bài Ohm cho LED
- [ ] Hiểu rail breadboard
- [ ] 5 điện trở đoán + đo
- [ ] Cực tụ & diode
- [ ] Nhận diện driver/MCU
- [ ] Một mối hàn sạch
""")

# Shorter but complete bodies for remaining slugs via template filler below
EXTRA = {
"mcu_landscape": ("ESP32: Wi-Fi/BT, great for teleop. Pico: simple, excellent MicroPython. Uno-class: 5 V legacy learning. Pick one primary for Capstone A.",
 "ESP32: Wi-Fi tốt cho teleop. Pico: MicroPython dễ. Chọn một MCU chính cho Capstone A."),
"esp32_platformio": ("Install PlatformIO or Arduino ESP32 core; select correct board; USB driver; Serial at 115200. Lab: upload blink.",
 "Cài PlatformIO/Arduino ESP32; chọn đúng board; lab upload blink."),
"pico_micropython": ("Flash MicroPython UF2; Thonny or mpremote; `print('hello')` over REPL. Lab: blink onboard LED.",
 "Nạp MicroPython UF2; REPL hello; lab blink LED."),
"blink_serial_hello": ("Lab: blink + `Serial.println` heartbeat every 500 ms. If resets when motors later connect, suspect brownout.",
 "Lab: blink + heartbeat serial. Reset khi gắn motor → nghi sụt áp."),
"pinouts_power_rails": ("3.3 V logic on ESP32/Pico. Level-shift 5 V sensors. Shared GND mandatory with drivers.",
 "Logic 3.3 V. Đổi mức cho cảm biến 5 V. Chung GND với driver."),
"ch02_lab_checklist": ("Checklist: toolchain installed; blink OK; serial OK; pin card for your board taped in notebook.",
 "Checklist: toolchain; blink; serial; thẻ chân GPIO trong sổ."),
"cpp_vs_micropython": ("MicroPython: fast iteration. C++/Arduino: tighter timing/PWM. Both valid; Capstone A can be either.",
 "MicroPython nhanh thử. C++ chặt timing. Capstone A dùng được cả hai."),
"gpio_patterns": ("Lab: button INPUT_PULLUP + LED. Debounce in software 10–50 ms.",
 "Lab: nút INPUT_PULLUP + LED; debounce 10–50 ms."),
"pwm_timers": ("PWM duty cycle commands average voltage to motors. Start low duty. Note frequency audible whine.",
 "PWM điều khiển điện áp trung bình. Bắt đầu duty thấp."),
"interrupts_debounce": ("Encoder edges often use interrupts; keep ISRs short; volatile flags; debounce mechanics.",
 "ISR ngắn; cờ volatile; chống dội cơ học."),
"state_machines_fw": ("States: IDLE → TELEOP → FAULT. Explicit transitions beat spaghetti `loop()`.",
 "Trạng thái IDLE/TELEOP/FAULT rõ ràng hơn loop rối."),
"ch03_lab_checklist": ("Checklist: GPIO lab done; PWM spins motor unloaded; state diagram sketched.",
 "Checklist: GPIO; PWM quay motor không tải; phác state diagram."),
"bus_interfaces": ("I2C: SDA/SCL + pull-ups, addresses. SPI: fast, more wires. UART: simple serial sensors.",
 "I2C có địa chỉ; SPI nhanh; UART đơn giản."),
"sensor_package_id": ("Use the ID sheet: HC-SR04 twin cans; VL53 ToF tiny; MPU6050 flat I2C; IR reflectance pair; encoder disks; camera FPC.",
 "Dùng phiếu ID: HC-SR04, ToF, IMU, IR, encoder, camera."),
"encoders_counts": ("Lab: count pulses while rotating wheel by hand; estimate CPR; watch quadrature A/B order.",
 "Lab: đếm xung quay tay; ước CPR; xem A/B."),
"imu_basics": ("Accel senses gravity+linear; gyro senses rate; fusion estimates attitude. Calibrate still bias.",
 "Accel/gyro/fusion; hiệu chuẩn bias khi đứng yên."),
"ultrasonic_tof": ("Lab: log distance vs ruler for HC-SR04 or ToF; note soft-target errors and FOV.",
 "Lab: so khoảng cách đo với thước; ghi lỗi mục tiêu mềm."),
"cameras_robots": ("USB cams easy on SBC; CSI on Pi/ESP-CAM. Bandwidth & lighting dominate. OpenCV is a common stack ([docs]("+LINKS['opencv']+")).",
 "USB dễ trên SBC; CSI trên Pi/ESP-CAM. OpenCV phổ biến."),
"ch04_lab_checklist": ("Checklist: named each sensor on desk; one I2C scan; one ranging plot.",
 "Checklist: gọi tên từng sensor; I2C scan; một đồ thị ranging."),
"dc_hbridge": ("H-bridge enables reverse. Dead-time matters. See concept figure; compare to your driver board silk.",
 "Cầu H cho quay ngược; xem hình; đối chiếu board."),
"driver_board_id": ("Lab: photograph driver; label VMOT, GND, PWMs, EN pins from module docs—not from memory.",
 "Lab: chụp driver; ghi nhãn VMOT/GND/PWM theo tài liệu module."),
"servos_pwm": ("Hobby servo ~50 Hz pulses 1–2 ms. Do not stall continuously. Separate 5 V supply often needed.",
 "Servo xung ~50 Hz 1–2 ms; tránh stall; nguồn 5 V riêng thường cần."),
"steppers_intro": ("Steppers move in increments; microstepping smooths. Great for precise heads; heavier on drivers.",
 "Stepper từng bước; microstep mượt hơn."),
"current_thermal": ("Stall current dwarfs no-load. Heat-sink L298N. Respect driver continuous ratings ([Pololu]("+LINKS['pololu_motor']+")).",
 "Dòng stall lớn; tôn trọng định mức driver."),
"closed_loop_intro": ("Lab mini: ultrasonic stop—if distance < threshold, PWM=0. Sense→compute→act loop on desktop.",
 "Lab: siêu âm dừng khi gần vật cản."),
"ch05_lab_checklist": ("Checklist: driver pins labeled; motor spins both ways; thermal caution noted.",
 "Checklist: ghim driver; motor hai chiều; chú ý nhiệt."),
"chassis_anatomy": ("Diff-drive: two driven wheels + caster/skid. Keep mass centered; protect wiring from belts/gears.",
 "Hai bánh chủ động + caster; bảo vệ dây."),
"fasteners_bearings_shafts": ("M3/M2 common. Lock washers/nyloc vs vibration. Bearings reduce friction; set screws on hubs loosen—Loctite carefully.",
 "Ốc M3; bạc đạn; vít set lỏng vì rung."),
"gear_trains_ratios": ("Ratio \(i=N_2/N_1\); torque up, speed down. Backlash bites when reversing. Planetary compact; worm high ratio + often non-backdrivable.",
 "Tỉ số \(i=N_2/N_1\); backlash khi đảo chiều."),
"linkages_belts_cams": ("Four-bar: one DOF when grounded. Belts need pitch match. Rack-and-pinion: rotary→linear.",
 "Four-bar; đai; bánh răng-thanh răng."),
"wheels_casters_diff": ("Wheel diameter enters odometry. Casters should swivel freely. Diff-drive equations in figure.",
 "Đường kính bánh vào odometry; caster quay tự do."),
"materials_print_laser": ("PETG/ABS tougher than brittle PLA for impact. Laser-cut acrylic plate chassis common. Design strain relief holes.",
 "PETG/ABS bền hơn PLA giòn; acrylic cắt laser phổ biến."),
"mech_failure_modes": ("Stripped TT gears, binding shafts, loose set screws, wire fatigue at connectors—inspect after every crash.",
 "Hỏng bánh răng TT, kẹt trục, lỏng set screw, đứt dây."),
"mechanisms_lab": ("Lab: count teeth on two meshing gears; predict ratio; rotate and measure angular displacement roughly.",
 "Lab: đếm răng; đoán tỉ số; đo góc quay."),
"ch06_lab_checklist": ("Checklist: fasteners inventory; gear ratio computed; strain relief on one cable; failure watchlist written.",
 "Checklist: ốc vít; tỉ số; chống kéo dây; danh sách hỏng hóc."),
"assemble_power": ("Assemble chassis square; mount motors; route battery with fuse/switch if available; common GND plan.",
 "Lắp khung; motor; pin có công tắc; kế hoạch GND."),
"driver_bringup": ("Lab: wheels up; low PWM both directions; verify wiring map; smell/heat check 10 s runs.",
 "Lab: nhấc bánh; PWM thấp hai chiều; kiểm nhiệt."),
"teleop_protocol": ("Design framed packets: e.g. `V L R\\n` with checksum optional. Document endianness & units (duty −100..100).",
 "Gói tin có khung; ghi đơn vị duty."),
"teleop_firmware": ("Parse serial; timeout→stop; clamp PWM; optional accel ramp. Still no ROS.",
 "Parse serial; timeout dừng; kẹp PWM."),
"field_acceptance": ("Acceptance: drive forward 1 m corridor; left/right pivot; e-stop by unplugging host; log a bug.",
 "Nghiệm thu: đi thẳng, quay, E-stop, ghi bug."),
"ch07_lab_checklist": ("Capstone checklist: BOM built; teleop both wheels; safety timeout; notes committed to repo.",
 "Checklist capstone: BOM; teleop; timeout; ghi chú repo."),
"serial_protocols": ("Prefer length-prefixed or delimiter protocols over bare prints. COBS/SLIP optional later.",
 "Giao thức có độ dài/delimiter hơn print thrảo."),
"wifi_mqtt": ("Lab: ESP32 publishes `/robot/cmd` style topic or subscribe to velocity. Use [MQTT]("+LINKS['mqtt']+") broker locally.",
 "Lab: ESP32 MQTT pub/sub lệnh vận tốc."),
"pid_tuning": ("Start P until responsive; add D to damp; I for steady-state. See [PID theory]("+LINKS['pid']+"). Lab: tune wheel speed with encoder if available.",
 "Chỉnh P→D→I. Lab PID tốc độ bánh nếu có encoder."),
"diff_kinematics": ("\(v=(v_R+v_L)/2\), \(\\omega=(v_R-v_L)/L\). Implement mapping from joystick to \(v_L,v_R\).",
 "Ánh xạ joystick → \(v_L,v_R\)."),
"loop_timing": ("Fixed-rate control loop (e.g. 50–100 Hz). Measure jitter; avoid long `delay` in loop.",
 "Vòng cố định 50–100 Hz; tránh delay dài."),
"jazzy_install_ws": ("Follow [Jazzy install]("+LINKS['ros2_jazzy']+") on Ubuntu 24.04. Create workspace; `colcon build`; source install. Lab: `ros2 topic list`.",
 "Cài Jazzy theo docs; workspace; lab `ros2 topic list`."),
"nodes_topics": ("Publisher/subscriber; `std_msgs`, `geometry_msgs`. Lab: pub/sub turtlesim or demo nodes from [tutorials]("+LINKS['ros2_tutorials']+").",
 "Lab pub/sub theo tutorial ROS 2."),
"services_actions": ("Services: sync req/resp. Actions: long goals with feedback (Nav2 uses actions heavily).",
 "Service đồng bộ; action cho mục tiêu dài."),
"launch_params_qos": ("Launch composes graph; params configure; QoS must match for sensor streams.",
 "Launch + param + QoS khớp cho sensor."),
"tf2_frames": ("Frames tree: `map`→`odom`→`base_link`→sensors. See [TF2]("+LINKS['tf2']+").",
 "Cây frame map/odom/base_link."),
"urdf_basics": ("URDF/xacro describes links/joints. Visual vs collision. [URDF tutorial]("+LINKS['urdf']+").",
 "URDF mô tả link/joint."),
"gazebo_harmonic": ("Gazebo Harmonic ([docs]("+LINKS['gazebo']+")) spawn robot; verify joints. Lab: empty world + model.",
 "Lab spawn model trong Gazebo Harmonic."),
"urdf_sim_bringup": ("Bring up robot_state_publisher + spawn. Check TF tree in RViz.",
 "robot_state_publisher + spawn; xem TF."),
"microros_mcu": ("micro-ROS puts XRCE-DDS agents on MCU ([micro.ros.org]("+LINKS['microros']+")). Bridge Capstone topics carefully.",
 "micro-ROS trên MCU; nối topic cẩn thận."),
"bridge_capstone": ("Options: micro-ROS native; or serial bridge node on PC. Start with cmd_vel → PWM node on laptop talking serial.",
 "Bridge serial cmd_vel→PWM trước khi tối ưu."),
"sim_to_real": ("Checklist: unit match, frame names, latency, motor direction signs, emergency stop parity.",
 "Checklist đơn vị, frame, latency, dấu motor, E-stop."),
"slam_overview": ("SLAM builds map while localizing. Start with [slam_toolbox]("+LINKS['slam_toolbox']+") docs overview—don't expect magic on bad odometry.",
 "SLAM cần odometry tốt; đọc overview slam_toolbox."),
"nav2_tour": ("Nav2: map server, planner, controller, BT navigator, recoveries. Tour [docs.nav2.org]("+LINKS['nav2']+").",
 "Tour Nav2: planner, controller, BT."),
"vision_pipeline": ("Capture→undistort→detect→track→act. Lighting first. OpenCV tutorials ([docs]("+LINKS['opencv']+")).",
 "Pipeline thị giác; ưu tiên ánh sáng."),
"bt_peek": ("Behavior Trees structure autonomy. See [BehaviorTree.CPP]("+LINKS['bt_cpp']+") and Nav2 BT XML.",
 "BT cấu trúc tự hành; xem Nav2 BT."),
"moveit_peek": ("MoveIt 2 for manipulators—optional peek ([docs]("+LINKS['moveit2']+")). Mobile diff-drive course does not require it.",
 "MoveIt 2 tùy chọn; không bắt buộc cho robot vi sai."),
"lerobot_intro": ("Hugging Face [LeRobot]("+LINKS['lerobot']+") provides datasets, policies, and training scripts for real robots. Read the official docs ([HF docs]("+LINKS['hf_lerobot']+")).",
 "LeRobot: dataset + policy + script; đọc docs chính thức."),
"imitation_act": ("Imitation learning clones demos. ACT (Action Chunking with Transformers) is a strong manipulation baseline—see [ALOHA/ACT pages]("+LINKS['aloha_act']+").",
 "IL/ACT: học từ demo; xem trang ALOHA/ACT."),
"diffusion_policy": ("Diffusion Policy generates actions by denoising—strong for multimodal actions ([project]("+LINKS['diff_policy']+")).",
 "Diffusion Policy: khử nhiễu để sinh action."),
"vla_overview": ("Vision-Language-Action models ground language in robot control. Survey RT-1/RT-X style systems ([RT-1]("+LINKS['rt1']+"), [Open X-Embodiment]("+LINKS['openx']+")) as reading—not homework to train from scratch.",
 "VLA: đọc RT-1/Open-X; không bắt train từ đầu."),
"next_paths_refs": ("Next: deepen Nav2; linorobot2 bringup; LeRobot on a manipulator kit; optional MIT Manipulation. Full reference list lives in COURSE_OUTLINE.md.",
 "Tiếp: Nav2, linorobot2, LeRobot tay máy; MIT Manipulation tùy chọn. Xem COURSE_OUTLINE.md."),
}

for k,(en,vi) in EXTRA.items():
    if k not in BODIES_EN:
        body(k, en, vi)


def front_matter(title, chapter, order, lang, lesson_type):
    return textwrap.dedent(f"""\
    ---
    layout: post
    title: "{title}"
    chapter: "{chapter}"
    order: {order}
    owner: "{OWNER}"
    lang: {lang}
    categories:
      - chapter{chapter}
    lesson_type: {lesson_type}
    draft: false
    ---
    """)


def lab_block(en=True):
    if en:
        return """
### Lab frame (when this lesson is hands-on)
**BOM:** listed in body or chapter checklist. **Procedure:** follow numbered steps. **Expected:** measurements/behavior noted above. **Common mistakes:** wrong polarity, missing GND, motor USB power, floating inputs. **Safety:** wheels up; power last; lithium discipline.
"""
    return """
### Khung lab
**BOM** và **quy trình** trong bài. **Sai thường gặp:** sai cực, thiếu GND, nuôi motor bằng USB. **An toàn:** nhấc bánh; nguồn sau cùng.
"""


def render_lesson(slug, title, chapter, order, lang, lesson_type):
    meta = META.get(slug, {"images": [], "lab": False, "links": []})
    bodies = BODIES_EN if lang == "en" else BODIES_VI
    core = bodies.get(slug, BODIES_EN.get(slug, "Content forthcoming.") if lang=="en" else BODIES_VI.get(slug, BODIES_EN.get(slug, "")))
    # objectives from title heuristics
    if lang == "en":
        objs = "\n".join([f"{i}. Master the ideas in “{title}” and complete any lab steps." for i in range(1,4)])
        objs = f"1. Explain the key ideas of this lesson in your own words.\n2. Complete the lab or identification tasks if present.\n3. Write three takeaways and one open question.\n4. Link this lesson to Capstone A / ROS path as relevant.\n5. Bookmark the further reading links."
        further = "\n".join(f"- [{k}]({LINKS[k]})" for k in meta.get("links", []) if k in LINKS) or "- See COURSE_OUTLINE.md references"
        exercises = """1. Summarize the lesson in 5 bullets.
2. Perform the lab steps (or dry-run if hardware missing) and note results.
3. List two failure modes related to this topic.
4. Sketch one diagram from memory.
5. Add a dated entry to `lab-notes.md`."""
        header = f"Estimated time: **~60 minutes**. Owner: {OWNER}."
    else:
        objs = "1. Giải thích ý chính bằng lời của bạn.\n2. Hoàn thành lab/nhận diện nếu có.\n3. Viết 3 ý lấy đi và 1 câu hỏi mở.\n4. Liên hệ Capstone A / lộ trình ROS.\n5. Bookmark phần đọc thêm."
        further = "\n".join(f"- [{k}]({LINKS[k]})" for k in meta.get("links", []) if k in LINKS) or "- Xem COURSE_OUTLINE.md"
        exercises = """1. Tóm tắt 5 gạch đầu dòng.
2. Làm lab (hoặc dry-run) và ghi kết quả.
3. Liệt kê 2 chế độ hỏng liên quan.
4. Vẽ lại một sơ đồ từ trí nhớ.
5. Ghi `lab-notes.md`."""
        header = f"Thời lượng: **~60 phút**. Tác giả: {OWNER}."

    imgs = "\n\n".join(img(p,a) for p,a in meta.get("images", []))
    img_section = (f"\n## Figures\n\n{imgs}\n" if imgs else "")
    lab_extra = lab_block(lang=="en") if meta.get("lab") or slug.endswith("_lab") or "lab" in slug or slug.endswith("checklist") else ""

    parts = [
        front_matter(title, chapter, order, lang, lesson_type),
        header,
        "",
        "## Learning objectives" if lang=="en" else "## Mục tiêu học",
        "",
        objs,
        "",
        plan(lang=="en"),
        img_section,
        "## Core ideas" if lang=="en" else "## Ý tưởng cốt lõi",
        "",
        core,
        lab_extra,
        "## Exercises" if lang=="en" else "## Bài tập",
        "",
        exercises,
        "",
        "## Further reading" if lang=="en" else "## Đọc thêm",
        "",
        further,
        "",
    ]
    return "\n".join(parts)


def write_chapter_index(chap, lang):
    info = CUR[chap]
    title = info["title_en"] if lang=="en" else info["title_vi"]
    return textwrap.dedent(f"""\
    ---
    layout: page
    lang: {lang}
    title: "{title}"
    chapter: "{chap}"
    owner: "{OWNER}"
    ---
    """)


def main():
    # clear old lesson posts but keep dirs
    for lang in ("en", "vi"):
        for p in (ROOT / "contents" / lang).glob("chapter*"):
            import shutil
            shutil.rmtree(p, ignore_errors=True)

    counts = {}
    for chap, info in CUR.items():
        counts[chap] = len(info["lessons"])
        for lang in ("en", "vi"):
            cdir = ROOT / "contents" / lang / f"chapter{chap}" / "_posts"
            cdir.mkdir(parents=True, exist_ok=True)
            (cdir.parent / "index.html").write_text(write_chapter_index(chap, lang), encoding="utf-8")
            for order, (slug, title_en, title_vi, ltype) in enumerate(info["lessons"], 1):
                title = title_en if lang=="en" else title_vi
                lesson_type = "required" if ltype == "required" else "optional"
                # map optional
                if ltype == "optional":
                    lesson_type = "optional"
                md = render_lesson(slug, title, chap, order, lang, lesson_type)
                fname = f"21-01-01-{chap}_{order:02d}_{slug}.md"
                (cdir / fname).write_text(md, encoding="utf-8")

    print("lesson counts", counts)
    print("total EN", sum(counts.values()))

if __name__ == "__main__":
    main()
