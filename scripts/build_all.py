#!/usr/bin/env python3
"""Generate all EN/VI lessons, outline, README, config, credits, home pages."""
from __future__ import annotations
import json, textwrap, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CUR = json.loads((ROOT / "scripts" / "curriculum.json").read_text(encoding="utf-8"))
OWNER = "Nguyen Le Linh"
EMAIL = "nglelinh@gmail.com"

URLS = {
    "ros2": "https://docs.ros.org/en/jazzy/",
    "ros2t": "https://docs.ros.org/en/jazzy/Tutorials.html",
    "nav2": "https://docs.nav2.org/",
    "gazebo": "https://gazebosim.org/docs/harmonic/",
    "microros": "https://micro.ros.org/",
    "esp32": "https://docs.espressif.com/projects/esp-idf/en/latest/esp32/",
    "pico": "https://www.raspberrypi.com/documentation/microcontrollers/raspberry-pi-pico.html",
    "arduino": "https://docs.arduino.cc/",
    "pio": "https://docs.platformio.org/",
    "lerobot": "https://github.com/huggingface/lerobot",
    "hf": "https://huggingface.co/docs/lerobot",
    "duck": "https://docs.duckietown.com/",
    "mit": "https://manipulation.mit.edu/",
    "moveit": "https://moveit.picknik.ai/main/index.html",
    "urdf": "https://docs.ros.org/en/jazzy/Tutorials/Intermediate/URDF/URDF-Main.html",
    "tf2": "https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-TF2.html",
    "lino": "https://github.com/linorobot/linorobot2",
    "logic": "https://learn.sparkfun.com/tutorials/logic-levels",
    "pololu": "https://www.pololu.com/docs/0J44",
    "pid": "https://www.ni.com/en/shop/labview/pid-theory-explained.html",
    "mqtt": "https://mqtt.org/",
    "cv": "https://docs.opencv.org/4.x/",
    "act": "https://tonyzhaozh.github.io/aloha/",
    "dp": "https://diffusion-policy.cs.columbia.edu/",
    "rt1": "https://robotics-transformer1.github.io/",
    "openx": "https://robotics-transformer-x.github.io/",
    "bt": "https://www.behaviortree.dev/",
    "slam": "https://github.com/SteveMacenski/slam_toolbox",
}

def im(path, alt):
    return f"![{alt}]({{{{ site.imgurl }}}}/{path})"

# slug -> list of (path, alt)
IMGS = {
    "kit_catalog_tooling": [
        ("generated/kit_catalog_overview.png", "Beginner bench kit families"),
        ("wikimedia/Digital_Multimeter_Aka.jpg", "Digital multimeter (Commons)"),
        ("wikimedia/Soldering_iron.jpg", "Soldering iron (Commons)"),
        ("wikimedia/breadboard.jpg", "Breadboard (Commons)"),
    ],
    "voltage_current_ohm": [("generated/ohms_law_triangle.png", "Ohm law triangle")],
    "breadboard_meter": [
        ("generated/breadboard_anatomy.png", "Breadboard anatomy"),
        ("wikimedia/Digital_Multimeter_Aka.jpg", "Multimeter"),
        ("wikimedia/breadboard.jpg", "Breadboard photo"),
    ],
    "resistor_color_smd": [
        ("generated/resistor_color_code.png", "Resistor color code chart"),
        ("wikimedia/resistors_assortment.jpg", "Resistor assortment (Commons)"),
    ],
    "cap_diode_led_id": [
        ("generated/capacitor_polarity.png", "Capacitor polarity"),
        ("wikimedia/Electrolytic_capacitor.jpg", "Electrolytic capacitor"),
        ("wikimedia/LEDs.jpg", "LEDs"),
        ("generated/component_lookalikes.png", "Lookalike components"),
    ],
    "transistor_mosfet_ic_id": [("generated/component_lookalikes.png", "Package lookalikes")],
    "connectors_drivers_boards": [
        ("generated/hbridge_concept.png", "H-bridge concept"),
        ("wikimedia/Dosmotorsl298n.jpg", "L298N-style driver"),
        ("generated/pcb_mcu_anatomy.png", "MCU board anatomy"),
        ("wikimedia/ESP32_on_Lolin32_Lite_clone_board_cropped.jpg", "ESP32-class board"),
        ("wikimedia/Raspberry_Pi_Pico.jpg", "Raspberry Pi Pico"),
    ],
    "soldering_basics": [("wikimedia/Soldering_iron.jpg", "Soldering iron")],
    "component_id_lab": [
        ("generated/resistor_color_code.png", "Color code"),
        ("generated/component_lookalikes.png", "Lookalikes"),
        ("wikimedia/resistors_assortment.jpg", "Resistors"),
    ],
    "mcu_landscape": [
        ("generated/pcb_mcu_anatomy.png", "MCU PCB anatomy"),
        ("wikimedia/ESP32_on_Lolin32_Lite_clone_board_cropped.jpg", "ESP32"),
        ("wikimedia/Raspberry_Pi_Pico.jpg", "Pico"),
    ],
    "pinouts_power_rails": [("generated/pcb_mcu_anatomy.png", "Headers and rails")],
    "sensor_package_id": [("generated/sensor_package_id.png", "Sensor ID sheet")],
    "ultrasonic_tof": [("generated/sensor_package_id.png", "Ranging modules")],
    "dc_hbridge": [("generated/hbridge_concept.png", "H-bridge"), ("wikimedia/Commutator_and_brushes_DC_motor.jpg", "DC motor detail")],
    "driver_board_id": [("generated/hbridge_concept.png", "H-bridge"), ("wikimedia/Dosmotorsl298n.jpg", "L298N module")],
    "chassis_anatomy": [("generated/diff_drive_kinematics.png", "Diff-drive chassis")],
    "fasteners_bearings_shafts": [("wikimedia/Ball_bearing.jpg", "Ball bearing")],
    "gear_trains_ratios": [("generated/gear_train_ratio.png", "Gear ratio")],
    "linkages_belts_cams": [("generated/four_bar_linkage.png", "Four-bar"), ("generated/belt_pulley.png", "Belt/pulley")],
    "wheels_casters_diff": [("generated/diff_drive_kinematics.png", "Diff-drive")],
    "mechanisms_lab": [("generated/gear_train_ratio.png", "Measure ratio")],
    "assemble_power": [("generated/diff_drive_kinematics.png", "Chassis")],
    "diff_kinematics": [("generated/diff_drive_kinematics.png", "Kinematics")],
    "welcome_and_outcomes": [("generated/kit_catalog_overview.png", "Course kit overview")],
    "bom_and_shopping": [("generated/kit_catalog_overview.png", "BOM families")],
}

LAB_SLUGS = {s for s in [
    "safety_mindset_lab","kit_catalog_tooling","ch00_lab_checklist",
    "breadboard_meter","resistor_color_smd","cap_diode_led_id","transistor_mosfet_ic_id",
    "connectors_drivers_boards","soldering_basics","component_id_lab","ch01_lab_checklist",
    "esp32_platformio","pico_micropython","blink_serial_hello","ch02_lab_checklist",
    "gpio_patterns","pwm_timers","interrupts_debounce","ch03_lab_checklist",
    "sensor_package_id","encoders_counts","imu_basics","ultrasonic_tof","ch04_lab_checklist",
    "driver_board_id","servos_pwm","closed_loop_intro","ch05_lab_checklist",
    "gear_trains_ratios","mechanisms_lab","ch06_lab_checklist",
    "assemble_power","driver_bringup","teleop_protocol","teleop_firmware","field_acceptance","ch07_lab_checklist",
    "wifi_mqtt","pid_tuning","jazzy_install_ws","nodes_topics","gazebo_harmonic","urdf_sim_bringup","bridge_capstone","sim_to_real",
]}

# Rich EN teaching blurbs (VI will be full translations for key lessons; others get complete VI summaries)
TEACH = {}

def teach(slug, en, vi, math_en="", math_vi="", links=None):
    TEACH[slug] = dict(en=en.strip(), vi=vi.strip(), math_en=math_en.strip(), math_vi=math_vi.strip(), links=links or [])

teach("welcome_and_outcomes",
"""This course is a bilingual path from **component literacy** to **built robots** and then to ROS 2 Jazzy and modern robot learning literacy.

You will: (1) identify tools and parts; (2) program ESP32/Pico; (3) assemble a differential-drive robot and teleoperate it in firmware; (4) map that robot into ROS 2 concepts and simulation; (5) read LeRobot / ACT / Diffusion Policy / VLA materials without hype.

Study cadence: ~4–6 hours/week for 12–16 weeks. Keep `lab-notes.md` with photos and serial logs.""",
"""Khóa học song ngữ từ **đọc linh kiện** đến **robot lắp được**, rồi ROS 2 Jazzy và robot learning.

Bạn sẽ: (1) nhận diện dụng cụ/linh kiện; (2) lập trình ESP32/Pico; (3) lắp robot vi sai và teleop firmware; (4) ánh xạ sang ROS 2 và mô phỏng; (5) đọc LeRobot/ACT/Diffusion/VLA đúng mức.

Nhịp ~4–6 giờ/tuần trong 12–16 tuần. Giữ `lab-notes.md`.""",
links=["ros2","lerobot","duck","mit"])

teach("learning_tracks_budget",
"""**Track A — budget MCU:** ESP32 or Pico + TT chassis + TB6612/DRV8833-class driver + ranging. Capstone A works without ROS.

**Track B — ROS:** same hardware + Ubuntu 24.04 for Jazzy; optional Pi 5 later.

Do not buy LiDAR before Capstone A acceptance. Optional architecture reference: [linorobot2](https://github.com/linorobot/linorobot2).""",
"""**Track A:** ESP32/Pico + khung TT + driver + cảm biến khoảng cách — Capstone A không cần ROS.

**Track B:** cùng phần cứng + Ubuntu 24.04 / Jazzy; Pi 5 tùy chọn.

Không mua LiDAR trước khi nghiệm thu Capstone A.""",
links=["lino","microros","pio"])

teach("safety_mindset_lab",
"""Energy + motion + bugs = hazard. Ritual: power last on / first off; lift wheels for motion tests; lithium only with matched charger; software timeout stops PWM if teleop silent ~300 ms; never feed motor rails into 3.3 V pins ([logic levels](https://learn.sparkfun.com/tutorials/logic-levels)).""",
"""Năng lượng + chuyển động + lỗi phần mềm = rủi ro. Nghi thức: cấp nguồn sau cùng; nhấc bánh khi test; sạc lithium đúng; timeout ~300 ms cắt PWM; không đưa điện motor vào chân 3.3 V.""",
links=["logic"])

teach("kit_catalog_tooling",
"""### Must-have families
Multimeter, temperature-controlled iron + solder/flux/wick, breadboard + Dupont, strippers/cutters, hex drivers, heat-shrink, calipers.

### Later lab upgrades
Current-limited bench PSU, USB logic analyzer, entry oscilloscope.

Beginner kit = measure + solder + prototype. Lab kit = measure currents safely and debug timing. See figures for layout.""",
"""### Bộ tối thiểu
Đồng hồ vạn năng, mỏ hàn chỉnh nhiệt, breadboard + Dupont, kìm/tuốt, tô vít lục giác, heat-shrink, thước kẹp.

### Nâng cấp sau
PSU giới hạn dòng, logic analyzer, scope nhập môn.""",
links=["arduino","pololu"])

teach("bom_and_shopping",
"""Default robot: ESP32 (or Pico) + diff TT chassis + driver + HC-SR04/ToF + optional IMU/encoders + matched battery/charger. Prefer efficient drivers when possible ([Pololu motor driver guide](https://www.pololu.com/docs/0J44)). Buy by ratings (stall current, voltage), not by fading sale prices.""",
"""Robot mặc định: ESP32/Pico + khung TT + driver + HC-SR04/ToF + IMU/encoder tùy chọn + pin/sạc khớp. Mua theo định mức, không theo giá flash sale.""",
links=["pololu"])

teach("workspace_toolchain_preview",
"""Folders: `notes/`, `firmware/`, `ros_ws/`. ESP32 via Arduino/PlatformIO; Pico via MicroPython; ROS 2 Jazzy on Ubuntu 24.04; Gazebo Harmonic; LeRobot on a PC.""",
"""Thư mục `notes/`, `firmware/`, `ros_ws/`. ESP32: Arduino/PlatformIO; Pico: MicroPython; ROS 2 Jazzy trên Ubuntu 24.04.""",
links=["pio","ros2t","esp32","pico","gazebo"])

teach("ch00_lab_checklist",
"""Tick before Chapter 01: eye protection + iron station; meter continuity beep; Track A/B written; BOM started; repo created; charger model photographed.""",
"""Checklist trước chương 01: kính + trạm hàn; ĐHVN thông mạch; chọn track; BOM; repo; ảnh sạc.""")

teach("voltage_current_ohm",
"""Potential \(V\), current \(I\), resistance \(R\): \(V=IR\). Power \(P=VI=I^2R\). Always series-resist LEDs.""",
"""\(V=IR\), \(P=VI\). LED luôn có điện trở hạn dòng.""",
math_en="Example: 3.3 V, red LED ~2.0 V drop, target 8 mA → \(R\\approx(3.3-2.0)/0.008=162.5\\,\\Omega\) → use 180 Ω.",
math_vi="Ví dụ: 3.3 V, LED đỏ ~2.0 V, 8 mA → \(R\\approx162.5\\Omega\) → chọn 180 Ω.")

teach("breadboard_meter",
"""Columns short internally; trench splits sides. Meter: V DC, continuity, Ω. Lab: beep a jumper; measure 3.3 V rail; never probe motor supply with wrong range carelessly.""",
"""Cột breadboard thông dọc; khe giữa cho IC. Lab: test dây; đo rail 3.3 V.""")

teach("resistor_color_smd",
"""4-band: digits + multiplier + tolerance. Brown-Blue-Orange-Gold = 16 kΩ ±5%. SMD `103` = 10 kΩ. Lab: decode five parts by eye, confirm with meter.""",
"""4 vạch: chữ số + bội + dung sai. SMD `103` = 10 kΩ. Lab: đoán 5 điện trở rồi đo.""")

teach("cap_diode_led_id",
"""Electrolytic stripe = negative. Ceramic usually non-polar. LED flat/short lead often cathode; diode band = cathode. SMD blank brown often cap; coded often resistor—verify.""",
"""Tụ hóa: sọc = âm. LED/diode: biết cực. SMD blank thường tụ; có số thường điện trở.""")

teach("transistor_mosfet_ic_id",
"""TO-92 vs TO-220 packages look similar across NPN/PNP/MOSFET/regulators—**read the printing**. IC pin 1 at notch/dot. Lab: sort a mixed bag into families and photograph markings.""",
"""TO-92/TO-220: phải đọc chữ. IC: khuyết = chân 1. Lab phân loại túi hỗn hợp.""")

teach("connectors_drivers_boards",
"""Dupont 0.1", JST battery/sensor plugs, XT60-class high current—do not force mismatches. Drivers: L298N (large sink) vs TB6612/DRV8833 (smaller/efficient). MCU: ESP32 DevKit vs Pico silhouette. Use H-bridge figure + board photos.""",
"""Không lẫn connector. Driver L298N vs TB6612/DRV8833. Board ESP32 vs Pico.""")

teach("datasheet_pinouts",
"""Workflow: Absolute Maximum Ratings → pinout → recommended operating → bus addresses → example schematic. Clone modules may have wrong silk—trust measurements + datasheet.""",
"""Quy trình datasheet: giới hạn tuyệt đối → pinout → điều kiện khuyến nghị → địa chỉ bus → schematic.""",
links=["esp32","pico","arduino"])

teach("soldering_basics",
"""Heat the joint; feed solder; shiny wetting; flux helps; wick mistakes. Add strain relief on moving cables. Lab: tin a wire and join to a header scrap.""",
"""Hâm nóng mối hàn; thiếc bóng; flux; chống kéo dây. Lab: thiếc hóa dây và hàn header.""")

teach("esd_polarity_brownout",
"""ESD discipline; reverse polarity kills drivers; motor stall current browns out MCU—common ground, bulk capacitance, separate motor supply when possible.""",
"""ESD; sai cực; sụt áp khi stall. Chung GND; tụ đệm; tách nguồn motor nếu được.""",
links=["logic"])

teach("component_id_lab",
"""BOM: assort resistors, electrolytic, ceramic, LED, diode, jumpers, meter. Procedure: map breadboard continuity; decode+measure resistors; diode-mode polarity; write lookalike list.""",
"""BOM linh kiện thụ động + ĐHVN. Quy trình: thông cột breadboard; đoán+đo R; cực diode/LED; danh sách dễ nhầm.""")

teach("ch01_lab_checklist",
"""Checklist: Ohm LED calc; breadboard rails; 5 resistors verified; polarity demos; driver vs MCU ID; one clean solder joint.""",
"""Checklist: tính R LED; rail breadboard; 5 điện trở; cực tính; nhận diện board; một mối hàn sạch.""")

# Generic fillers for remaining slugs
GENERIC = {
"mcu_landscape": ("ESP32 (Wi-Fi teleop), Pico (MicroPython simplicity), Uno-class (5 V learning). Pick one Capstone MCU.", "ESP32 / Pico / Uno-class — chọn một MCU cho Capstone.", ["esp32","pico","arduino"]),
"esp32_platformio": ("Install PlatformIO or Arduino-ESP32; select board; 115200 serial. Lab: blink.", "Cài PlatformIO/Arduino-ESP32; lab blink.", ["pio","esp32"]),
"pico_micropython": ("Flash MicroPython UF2; REPL hello; blink LED lab.", "Nạp MicroPython; REPL; lab blink.", ["pico"]),
"blink_serial_hello": ("Lab: blink + serial heartbeat. Motor-induced resets ⇒ brownout hunt.", "Lab blink + heartbeat serial.", []),
"pinouts_power_rails": ("3.3 V GPIO; level-shift 5 V sensors; shared GND with drivers.", "GPIO 3.3 V; đổi mức; chung GND.", ["logic"]),
"ch02_lab_checklist": ("Toolchain + blink + serial + pin card in notebook.", "Toolchain, blink, serial, thẻ chân.", []),
"cpp_vs_micropython": ("MicroPython iterates fast; C++ tighter timing—both OK for Capstone A.", "MicroPython nhanh thử; C++ chặt timing.", []),
"gpio_patterns": ("Lab: INPUT_PULLUP button + LED; debounce 10–50 ms.", "Lab nút + LED; debounce.", []),
"pwm_timers": ("PWM duty ≈ average voltage; start low; note audible whine.", "PWM duty; bắt đầu thấp.", []),
"interrupts_debounce": ("Short ISRs; volatile flags; mechanical debounce for encoders/buttons.", "ISR ngắn; debounce.", []),
"state_machines_fw": ("IDLE → TELEOP → FAULT beats spaghetti loop().", "Máy trạng thái rõ ràng.", []),
"ch03_lab_checklist": ("GPIO lab; unloaded PWM spin; state diagram sketched.", "GPIO; PWM; state diagram.", []),
"bus_interfaces": ("I2C address+pullups; SPI speed; UART simplicity.", "I2C/SPI/UART.", []),
"sensor_package_id": ("ID sheet: HC-SR04 twin cans; VL53 ToF; MPU6050; IR pair; encoder; camera FPC.", "Phiếu ID cảm biến.", []),
"encoders_counts": ("Lab: hand-turn counting; estimate CPR; note A/B order.", "Lab đếm xung quay tay.", []),
"imu_basics": ("Accel vs gyro; static bias calib; fusion overview.", "Accel/gyro/fusion.", []),
"ultrasonic_tof": ("Lab: compare sensor distance to ruler; note FOV/soft target errors.", "Lab so với thước.", []),
"cameras_robots": ("USB vs CSI; bandwidth/lighting dominate. OpenCV common.", "USB/CSI; OpenCV.", ["cv"]),
"ch04_lab_checklist": ("Name each sensor; I2C scan; ranging notes.", "Tên sensor; I2C scan; ranging.", []),
"dc_hbridge": ("H-bridge reverses motors; avoid shoot-through; compare figure to your board.", "Cầu H đảo chiều.", ["pololu"]),
"driver_board_id": ("Lab: label VMOT/GND/PWM/EN from module docs on a photo.", "Lab ghi nhãn chân driver.", []),
"servos_pwm": ("~50 Hz, 1–2 ms pulse; avoid continuous stall; often need 5 V supply.", "Servo 50 Hz; tránh stall.", []),
"steppers_intro": ("Discrete steps; microstepping smoother; stronger drivers.", "Stepper và microstep.", []),
"current_thermal": ("Stall ≫ no-load current; heatsink L298N; respect continuous ratings.", "Dòng stall; nhiệt.", ["pololu"]),
"closed_loop_intro": ("Lab: if range < threshold → PWM 0. Sense→compute→act.", "Lab dừng khi gần vật cản.", []),
"ch05_lab_checklist": ("Pins labeled; bidirectional spin; thermal note.", "Ghim; hai chiều; nhiệt.", []),
"chassis_anatomy": ("Two driven wheels + caster; center mass; protect wires.", "Hai bánh chủ động + caster.", []),
"fasteners_bearings_shafts": ("M2/M3; nyloc vs vibe; bearings; set screws loosen—threadlock carefully.", "Ốc, bạc đạn, set screw.", []),
"gear_trains_ratios": ("Ratio \(i=N_2/N_1\); torque↑ speed↓; backlash on reverse; worm/planetary options.", "Tỉ số truyền; backlash.", ""),
"linkages_belts_cams": ("Four-bar DOF; timing belt pitch; rack-and-pinion linearization.", "Four-bar; đai; rack-pinion.", []),
"wheels_casters_diff": ("Diameter enters odometry; casters free; see kinematics figure.", "Odometry và caster.", []),
"materials_print_laser": ("PETG/ABS tougher than brittle PLA; acrylic plates; strain-relief holes.", "PETG/ABS vs PLA; acrylic.", []),
"mech_failure_modes": ("Stripped TT gears, binding, loose hubs, wire fatigue—inspect after crashes.", "Hỏng bánh răng, kẹt trục, đứt dây.", []),
"mechanisms_lab": ("Count teeth; predict ratio; measure rotation relationship.", "Đếm răng; đo tỉ số.", []),
"ch06_lab_checklist": ("Fastener inventory; ratio computed; one strain relief; failure watchlist.", "Ốc; tỉ số; chống kéo; watchlist.", []),
"assemble_power": ("Square chassis; mount motors; fused/switched battery plan; common GND.", "Lắp khung; pin; GND.", []),
"driver_bringup": ("Wheels up; low PWM both ways; heat sniff test short runs.", "Nhấc bánh; PWM thấp.", []),
"teleop_protocol": ("Framed packets e.g. `V L R\\n`; document units −100..100.", "Gói tin có khung.", []),
"teleop_firmware": ("Parse; timeout stop; clamp; optional ramp—still no ROS.", "Parse; timeout; kẹp PWM.", []),
"field_acceptance": ("1 m corridor; pivots; unplug-host e-stop; file a bug.", "Đi thẳng; quay; E-stop.", []),
"ch07_lab_checklist": ("Built BOM; teleop OK; timeout; notes committed.", "BOM; teleop; timeout; git notes.", []),
"serial_protocols": ("Length/delimiter framing beats raw prints.", "Khung gói tin.", []),
"wifi_mqtt": ("Lab: ESP32 MQTT pub/sub velocity-style topic on local broker.", "Lab MQTT ESP32.", ["mqtt"]),
"pid_tuning": ("P then D then I; [PID primer](https://www.ni.com/en/shop/labview/pid-theory-explained.html).", "Chỉnh P→D→I.", ["pid"]),
"diff_kinematics": ("\(v=(v_R+v_L)/2\), \(\\omega=(v_R-v_L)/L\); map joystick→wheel speeds.", "Ánh xạ joystick → bánh.", []),
"loop_timing": ("Fixed 50–100 Hz loops; measure jitter; avoid long delay().", "Vòng 50–100 Hz.", []),
"jazzy_install_ws": ("Install Jazzy on Ubuntu 24.04; colcon ws; `ros2 topic list`.", "Cài Jazzy; workspace; topic list.", ["ros2","ros2t"]),
"nodes_topics": ("Pub/sub lab via official tutorials.", "Lab pub/sub.", ["ros2t"]),
"services_actions": ("Services sync; actions long-running (Nav2).", "Service và action.", ["ros2t"]),
"launch_params_qos": ("Launch graphs; params; matching QoS.", "Launch, param, QoS.", ["ros2t"]),
"tf2_frames": ("map→odom→base_link→sensors.", "Cây TF.", ["tf2"]),
"urdf_basics": ("Links/joints; visual vs collision.", "URDF link/joint.", ["urdf"]),
"gazebo_harmonic": ("Spawn in Gazebo Harmonic; verify joints.", "Spawn Gazebo Harmonic.", ["gazebo"]),
"urdf_sim_bringup": ("robot_state_publisher + spawn; RViz TF.", "Bring-up sim + TF.", []),
"microros_mcu": ("micro-ROS XRCE-DDS on MCU.", "micro-ROS trên MCU.", ["microros"]),
"bridge_capstone": ("Start with PC serial bridge cmd_vel→PWM; then micro-ROS.", "Bridge serial trước.", ["microros","lino"]),
"sim_to_real": ("Units, frames, latency, motor signs, E-stop parity.", "Checklist sim-to-real.", []),
"slam_overview": ("SLAM needs decent odometry; see slam_toolbox overview.", "SLAM và odometry.", ["slam","nav2"]),
"nav2_tour": ("Planner, controller, BT navigator, recoveries.", "Tour Nav2.", ["nav2"]),
"vision_pipeline": ("Capture→detect→act; lighting first; OpenCV.", "Pipeline thị giác.", ["cv"]),
"bt_peek": ("BehaviorTree.CPP + Nav2 BT XML.", "Behavior Tree peek.", ["bt","nav2"]),
"moveit_peek": ("Optional manipulator stack—not required for diff-drive path.", "MoveIt tùy chọn.", ["moveit"]),
"lerobot_intro": ("HF LeRobot: datasets, policies, train scripts—read official docs.", "Giới thiệu LeRobot.", ["lerobot","hf"]),
"imitation_act": ("Imitation learning; ACT chunking baseline (ALOHA/ACT).", "IL và ACT.", ["act","lerobot"]),
"diffusion_policy": ("Diffusion Policy: action via denoising.", "Diffusion Policy.", ["dp"]),
"vla_overview": ("Read RT-1 / Open-X style VLA systems—do not train from scratch as homework.", "Tổng quan VLA.", ["rt1","openx"]),
"next_paths_refs": ("Next: Nav2 depth, linorobot2, LeRobot arm kit, optional MIT Manipulation. See COURSE_OUTLINE.md.", "Lộ trình tiếp theo.", ["ros2","nav2","lerobot","mit","duck","microros"]),
}

for k,v in GENERIC.items():
    if k not in TEACH:
        en, vi, links = v[0], v[1], v[2] if len(v)>2 else []
        if isinstance(links, str):
            links = []
        teach(k, en, vi, links=links)

def plan(lang):
    if lang=="en":
        return """## 60-minute plan\n\n| Min | Activity |\n|----:|----------|\n| 0–5 | Objectives + figures |\n| 5–25 | Core reading / math |\n| 25–45 | Lab or ID practice |\n| 45–55 | Exercises |\n| 55–60 | Notes + links |\n"""
    return """## Kế hoạch 60 phút\n\n| Phút | Việc |\n|-----:|------|\n| 0–5 | Mục tiêu + hình |\n| 5–25 | Đọc / toán |\n| 25–45 | Lab hoặc nhận diện |\n| 45–55 | Bài tập |\n| 55–60 | Ghi chú + link |\n"""

def lab_section(slug, lang):
    if slug not in LAB_SLUGS:
        return ""
    if lang=="en":
        return """\n## Hands-on lab notes\n\n**Safety:** wheels up for motion; power last; lithium attended.\n**Procedure:** follow the numbered guidance in Core ideas; photograph wiring.\n**Record:** meter readings / serial lines / tooth counts in `lab-notes.md`.\n**Common mistakes:** missing common GND; USB powering motors; swapped motor leads; floating buttons without pull-ups.\n"""
    return """\n## Ghi chú lab\n\n**An toàn:** nhấc bánh; nguồn sau cùng; pin lithium có người trông.\n**Quy trình:** làm theo phần ý tưởng cốt lõi; chụp ảnh đấu dây.\n**Ghi:** số đo / serial / số răng vào `lab-notes.md`.\n**Sai thường gặp:** thiếu GND chung; USB nuôi motor; đảo dây motor.\n"""

def render(slug, title, chap, order, lang, ltype):
    t = TEACH.get(slug, dict(en=title, vi=title, math_en="", math_vi="", links=[]))
    body = t["en"] if lang=="en" else t["vi"]
    math = t["math_en"] if lang=="en" else t["math_vi"]
    links = t.get("links") or []
    figs = IMGS.get(slug, [])
    fig_md = "\n\n".join(im(p,a) for p,a in figs)
    if lang=="en":
        objs = "1. Explain the lesson ideas in your own words.\n2. Complete lab/ID tasks if present.\n3. Connect this lesson to Capstone A or ROS path.\n4. Note two failure modes.\n5. Save further-reading links."
        ex = "1. Five-bullet summary.\n2. Do (or dry-run) the lab; paste results.\n3. Sketch one diagram from memory.\n4. List two mistakes to avoid.\n5. Date an entry in `lab-notes.md`."
        fr = "\n".join(f"- [{k}]({URLS[k]})" for k in links if k in URLS) or "- See COURSE_OUTLINE.md"
        head = f"Estimated time: **~60 minutes**."
        h_obj, h_core, h_ex, h_fr, h_math = "Learning objectives", "Core ideas", "Exercises", "Further reading", "Math / check"
    else:
        objs = "1. Giải thích ý bài bằng lời bạn.\n2. Làm lab/nhận diện nếu có.\n3. Liên hệ Capstone A hoặc ROS.\n4. Ghi hai chế độ hỏng.\n5. Lưu link đọc thêm."
        ex = "1. Tóm tắt 5 ý.\n2. Làm lab (hoặc dry-run).\n3. Vẽ lại một sơ đồ.\n4. Hai lỗi cần tránh.\n5. Ghi `lab-notes.md`."
        fr = "\n".join(f"- [{k}]({URLS[k]})" for k in links if k in URLS) or "- Xem COURSE_OUTLINE.md"
        head = f"Thời lượng: **~60 phút**."
        h_obj, h_core, h_ex, h_fr, h_math = "Mục tiêu học", "Ý tưởng cốt lõi", "Bài tập", "Đọc thêm", "Toán / kiểm"

    fm = textwrap.dedent(f"""\
    ---
    layout: post
    title: "{title}"
    chapter: "{chap}"
    order: {order}
    owner: "{OWNER}"
    lang: {lang}
    categories:
      - chapter{chap}
    lesson_type: {"required" if ltype=="required" else "optional"}
    draft: false
    ---
    """)
    parts = [fm, head, "", f"## {h_obj}", "", objs, "", plan(lang)]
    if fig_md:
        parts += ["## Figures" if lang=="en" else "## Hình minh họa", "", fig_md, ""]
    parts += [f"## {h_core}", "", body, ""]
    if math:
        parts += [f"## {h_math}", "", math, ""]
    parts += [lab_section(slug, lang), f"## {h_ex}", "", ex, "", f"## {h_fr}", "", fr, ""]
    return "\n".join(parts)

def write_lessons():
    counts = {}
    missing = []
    for chap, info in CUR.items():
        counts[chap] = len(info["lessons"])
        for lang in ("en", "vi"):
            base = ROOT / "contents" / lang / f"chapter{chap}"
            if base.exists():
                shutil.rmtree(base)
            posts = base / "_posts"
            posts.mkdir(parents=True)
            title = info["title_en"] if lang=="en" else info["title_vi"]
            (base / "index.html").write_text(textwrap.dedent(f"""\
            ---
            layout: page
            lang: {lang}
            title: "{title}"
            chapter: "{chap}"
            owner: "{OWNER}"
            ---
            """), encoding="utf-8")
            for order,(slug,ten,tvi,ltype) in enumerate(info["lessons"],1):
                if slug not in TEACH:
                    missing.append(slug)
                title = ten if lang=="en" else tvi
                md = render(slug, title, chap, order, lang, ltype)
                (posts / f"21-01-01-{chap}_{order:02d}_{slug}.md").write_text(md, encoding="utf-8")
    return counts, missing

def write_outline(counts):
    lines = ["# COURSE_OUTLINE — Robotics Self-Learning\n",
             f"**EN title:** Build & Program Robots: From Embedded Systems to ROS 2 and Robot Learning\n",
             f"**VI title:** Lắp ráp & lập trình robot: Từ hệ thống nhúng đến ROS 2 và Robot Learning\n",
             f"**Author:** {OWNER} `<{EMAIL}>`\n",
             f"**Site:** https://nglelinh.github.io/{ROOT.name}/\n",
             "\n## Chapter map\n\n",
             "| Ch | EN | VI | Lessons |\n|----|----|----|--------:|\n"]
    total=0
    for chap, info in CUR.items():
        n=counts[chap]; total+=n
        lines.append(f"| {chap} | {info['title_en']} | {info['title_vi']} | {n} |\n")
    lines.append(f"\n**Total EN lessons:** {total} (×2 with VI ≈ {total*2} files)\n")
    lines.append("\n## Emphasis added (2026 refresh)\n")
    lines.append("- Ch.00 kit catalog & tooling labs\n- Ch.01 deep component identification + ID lab\n- Ch.04–05 sensor/driver package ID\n- Ch.06 mechanisms: gears, linkages, belts, bearings, failure modes\n- Generated educational diagrams under `img/generated/`\n- Wikimedia Commons photos under `img/wikimedia/` (see IMAGE_CREDITS.md)\n")
    lines.append("\n## References (public)\n")
    for k,u in URLS.items():
        lines.append(f"- {k}: {u}\n")
    lines.append("\nOptional advanced: MIT Manipulation (Drake) — not required.\n")
    for chap, info in CUR.items():
        lines.append(f"\n## Chapter {chap}: {info['title_en']} / {info['title_vi']}\n\n")
        for i,(slug,ten,tvi,lt) in enumerate(info["lessons"],1):
            flag = " (lab)" if slug in LAB_SLUGS else ""
            lines.append(f"- **EN** {chap}-{i:02d} {ten}{flag}\n  **VI** {tvi}\n")
    (ROOT/"COURSE_OUTLINE.md").write_text("".join(lines), encoding="utf-8")

def write_config_readme_home():
    cfg = f"""# Setup
title:               "Build & Program Robots: From Embedded Systems to ROS 2 and Robot Learning"
description:         "Bilingual self-learning course: electronics & component ID, embedded firmware, robot assembly, ROS 2 Jazzy, simulation/micro-ROS, and modern robot learning literacy."
url:                 https://nglelinh.github.io
baseurl:             '/robotics-self-learning'
imgurl:              https://nglelinh.github.io/robotics-self-learning/img
paginate:            5
permalink:           pretty

languages:           ["en", "vi"]
default_lang:        "en"
exclude_from_localization: ["javascript", "images", "css", "public", "img"]
parallel_localization: true

t:
  en:
    title: "Build & Program Robots: From Embedded Systems to ROS 2 and Robot Learning"
    description: "From bench components and diff-drive firmware to ROS 2 Jazzy, Gazebo Harmonic, micro-ROS, and LeRobot-era learning literacy."
    home: "Home"
    chapters: "Chapters"
    language: "Language"
    switch_language: "Switch to Vietnamese"
    required: "Required"
    optional: "Optional"
  vi:
    title: "Lắp ráp & lập trình robot: Từ hệ thống nhúng đến ROS 2 và Robot Learning"
    description: "Từ linh kiện bàn và firmware robot vi sai đến ROS 2 Jazzy, Gazebo Harmonic, micro-ROS và robot learning hiện đại."
    home: "Trang chủ"
    chapters: "Các chương"
    language: "Ngôn ngữ"
    switch_language: "Chuyển sang tiếng Anh"
    required: "Bắt buộc"
    optional: "Tùy chọn"

author:
  name:              {OWNER}
  email:             {EMAIL}

plugins:
  - jekyll-paginate
  - jekyll-feed

plugins_dir: _plugins

collections:
  posts:
    output: true
    permalink: /:categories/:title/

version:             0.1.0
markdown: kramdown
google_analytics_id: ""
"""
    (ROOT/"_config.yml").write_text(cfg, encoding="utf-8")

    readme = f"""# Robotics Self-Learning / Tự học Robotics

**EN:** Build & Program Robots: From Embedded Systems to ROS 2 and Robot Learning  
**VI:** Lắp ráp & lập trình robot: Từ hệ thống nhúng đến ROS 2 và Robot Learning  

Author: **{OWNER}** (`{EMAIL}`)  
GitHub Pages: https://nglelinh.github.io/robotics-self-learning/

## How to study

1. Read Chapter 00 (tracks, safety, **kit catalog**).
2. Chapter 01 heavily covers **component identification** + labs.
3. Chapters 02–05: MCU, firmware patterns, sensors/actuators (with package ID).
4. Chapter 06: **mechanical mechanisms** (gears, linkages, bearings…).
5. Chapter 07: Capstone A teleop (no ROS).
6. Chapters 08–11: control, ROS 2 Jazzy, sim/micro-ROS, autonomy peek.
7. Chapter 12: LeRobot / ACT / Diffusion / VLA literacy + references.

Keep `lab-notes.md`. Prefer one working subsystem over many unfinished tutorials.

## Default BOM (Track A)

ESP32 **or** Pico · TT diff chassis · TB6612/DRV8833-class driver · HC-SR04 or ToF · optional IMU/encoders · matched battery+charger · meter + iron + breadboard kit (see Ch.00).

Optional later: Raspberry Pi 5 for onboard ROS 2.

## Images

- `img/generated/` — labeled educational diagrams created for this course
- `img/wikimedia/` — openly licensed photos; see `IMAGE_CREDITS.md`

## Build locally

```bash
bundle install
bundle exec jekyll serve
```

## Mac sync

This tree may be built on the agent box. To place it on the Mac teaching folder, see `MAC_SYNC.md`.
"""
    (ROOT/"README.md").write_text(readme, encoding="utf-8")

    # home posts
    home = ROOT/"home"/"_posts"
    home.mkdir(parents=True, exist_ok=True)
    (home/"21-01-20-introduction.md").write_text(textwrap.dedent(f"""\
    ---
    layout: post
    title: introduction
    order: 3
    chapter: home
    owner: {OWNER}
    ---

    # Welcome — Build & Program Robots

    Bilingual path from electronics literacy and robot assembly to ROS 2 Jazzy and modern robot-learning literacy.

    ## You will learn

    - Component & tool identification on the bench
    - Embedded firmware on ESP32 / Pico
    - Diff-drive assembly and teleop firmware
    - ROS 2 Jazzy, TF/URDF, Gazebo Harmonic, micro-ROS
    - How to read LeRobot / ACT / Diffusion Policy / VLA materials

    Start at Chapter 00. Capstone A is Chapter 07.
    """), encoding="utf-8")

    (home/"21-01-20-contents.md").write_text(textwrap.dedent(f"""\
    ---
    layout: post
    title: contents
    chapter: home
    order: 1
    owner: {OWNER}
    ---

    See [COURSE_OUTLINE.md]({{{{ site.baseurl }}}}/COURSE_OUTLINE.md) for the full bilingual map (Ch.00–12), labs, and references.
    """), encoding="utf-8")

    (home/"21-05-20-author-details.md").write_text(textwrap.dedent(f"""\
    ---
    layout: post
    title: author-details
    chapter: home
    order: 5
    owner: {OWNER}
    ---

    **{OWNER}** — `{EMAIL}`
    """), encoding="utf-8")

    (home/"21-02-03-makers.md").write_text(textwrap.dedent(f"""\
    ---
    layout: post
    title: makers
    chapter: home
    order: 4
    owner: {OWNER}
    ---

    Course maintained by {OWNER}. Contributions welcome via GitHub issues/PRs.
    """), encoding="utf-8")

def write_credits_mac():
    credits = ROOT/"img"/"wikimedia"/"CREDITS.json"
    lines = ["# IMAGE_CREDITS\n\n## Generated diagrams\n\nAll files under `img/generated/` were created for this course (educational labeled diagrams).\n\n## Wikimedia Commons\n\n"]
    if credits.exists():
        data = json.loads(credits.read_text(encoding="utf-8"))
        for c in data:
            f = c.get("file","")
            if "_rejected" in f or any(x in f for x in ["Abandoned","Burnt","DL50","USS_Device","Crocodile"]):
                continue
            lines.append(f"- `{f}` — {c.get('commons_title','')} — {c.get('license','')} — {c.get('artist','')} — {c.get('source_url','')}\n")
    else:
        lines.append("(Run Wikimedia download to refresh CREDITS.json)\n")
    lines.append("\nDo not embed rejected/non-illustrative downloads from `img/wikimedia/_rejected/`.\n")
    (ROOT/"IMAGE_CREDITS.md").write_text("".join(lines), encoding="utf-8")

    (ROOT/"MAC_SYNC.md").write_text(textwrap.dedent(f"""\
    # Sync onto MacBook (machineId cbecf7d8-4473-4909-a9c2-eadeced14735)

    Target: `/Users/nguyenlelinh/teaching/robotics-self-learning`

    ## Box artifact

    Built on the agent computer when Mac local-exec is unavailable:

    - Tree: `/workspace/robotics-self-learning`
    - Tarball: `/workspace/robotics-self-learning.tar.gz`

    ## On Mac

    ```bash
    mkdir -p /Users/nguyenlelinh/teaching
    cd /Users/nguyenlelinh/teaching
    # after copying the tarball:
    tar xzf robotics-self-learning.tar.gz
    # Prefer copying from local course-self-learning-template only for structure;
    # this tree is already filled—do not re-clone teaching repos from GitHub.
    ```

    Then `gh auth login` if needed and push per README / GITHUB_SETUP.md.
    """), encoding="utf-8")

    (ROOT/"GITHUB_SETUP.md").write_text(textwrap.dedent("""\
    # GitHub setup

    ```bash
    cd robotics-self-learning
    git init -b main   # if needed
    git add -A
    git commit -m "Initial robotics self-learning course"
    gh repo create nglelinh/robotics-self-learning --public --source=. --remote=origin --push
    ```

    If `gh` auth fails:

    ```bash
    gh auth login
    # or create empty repo nglelinh/robotics-self-learning on GitHub, then:
    git remote add origin git@github.com:nglelinh/robotics-self-learning.git
    git push -u origin main
    ```

    Enable GitHub Pages via Actions (workflow from template `.github/workflows/`).
    """), encoding="utf-8")

def main():
    # authors
    (ROOT/"AUTHORS.md").write_text(f"# Authors\n\n- {OWNER} <{EMAIL}>\n", encoding="utf-8")
    counts, missing = write_lessons()
    write_outline(counts)
    write_config_readme_home()
    write_credits_mac()
    print("counts", counts)
    print("total", sum(counts.values()))
    print("missing_teach", missing)
    # verify no TODO stubs
    import subprocess, os
    r = subprocess.run(["rg","-l","TODO|TBD|coming soon","contents"], cwd=ROOT, capture_output=True, text=True)
    print("todo_files", r.stdout.strip() or "none")

if __name__ == "__main__":
    main()
