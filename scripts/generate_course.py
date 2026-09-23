#!/usr/bin/env python3
"""Generate full EN/VI robotics self-learning Jekyll course."""
from __future__ import annotations
import json, re, textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CUR = json.loads((ROOT / "scripts" / "curriculum.json").read_text(encoding="utf-8"))
OWNER = "Nguyen Le Linh"

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

# Per-lesson teaching focus: (hook, theory_blocks, math, lab, pitfalls, links)
# theory_blocks: list of (heading, paragraphs)
FOCUS: dict[str, dict] = {}

def F(slug, **kwargs):
    FOCUS[slug] = kwargs

# ===================== CHAPTER 00 =====================
F("welcome_and_outcomes",
  hook_en="This course takes you from soldering nerves to ROS 2 Jazzy topics and a literate reading of LeRobot-style robot learning—without pretending every hobbyist needs Drake on day one.",
  hook_vi="Khóa học đưa bạn từ lo lắng khi hàn mạch đến topic ROS 2 Jazzy và đọc hiểu robot learning kiểu LeRobot—không bắt buộc Drake ngay ngày đầu.",
  objectives_en=[
    "State course outcomes in one paragraph",
    "Contrast firmware-first vs ROS-first learning",
    "Estimate a 12–16 week pace at 4–6 h/week",
    "Start a learning log + firmware repo",
    "Bookmark official docs hubs",
  ],
  objectives_vi=[
    "Nêu đầu ra khóa học trong một đoạn",
    "Phân biệt firmware-first và ROS-first",
    "Ước lượng nhịp 12–16 tuần, 4–6 giờ/tuần",
    "Bắt đầu nhật ký học + repo firmware",
    "Bookmark cụm tài liệu chính thức",
  ],
  theory_en=[
    ("What you will build",
     "By Chapter 07 you teleoperate a differential-drive robot from embedded firmware. By Chapter 10 you can map that robot into ROS 2 / micro-ROS. By Chapter 12 you can discuss imitation learning, ACT, Diffusion Policy, and VLA at overview depth and point to real public resources."),
    ("How to study",
     "Prefer one working subsystem over ten unfinished tutorials. Keep `lab-notes.md` with wiring photos, serial snippets, and failure modes. Separate motor power from logic early—brownouts look like 'random' bugs."),
  ],
  theory_vi=[
    ("Bạn sẽ xây gì",
     "Chương 07: teleop robot vi sai bằng firmware. Chương 10: nối vào ROS 2 / micro-ROS. Chương 12: đọc overview imitation learning, ACT, Diffusion Policy, VLA kèm tài nguyên công khai thật."),
    ("Cách học",
     "Một phân hệ chạy tốt hơn mười tutorial dang dở. Giữ `lab-notes.md`. Tách nguồn motor và logic sớm."),
  ],
  math_en="No new equations today—but open a note titled *Power budget* and write \(P = VI\) as a reminder that stall currents dominate battery and driver choice.",
  math_vi="Chưa có phương trình mới—mở ghi chú *Ngân sách nguồn* và viết \(P = VI\) để nhớ dòng stall quyết định pin/driver.",
  lab_en="Create repo `my-robot-labs/` with folders `notes/`, `firmware/`, `ros_ws/` (empty). Write a one-sentence personal goal.",
  lab_vi="Tạo repo `my-robot-labs/` với `notes/`, `firmware/`, `ros_ws/`. Viết mục tiêu một câu.",
  pitfalls_en=["Skipping safety/BOM then buying incompatible chargers", "Jumping to Nav2 before motors spin reliably"],
  pitfalls_vi=["Bỏ qua an toàn/BOM rồi mua sạc không khớp", "Nhảy Nav2 khi motor chưa quay ổn"],
  links=["ros2_jazzy", "lerobot", "duckietown", "mit_manip"],
)

F("learning_tracks_budget",
  hook_en="Two tracks share Chapters 00–07 hardware intuition; they diverge on compute spend.",
  hook_vi="Hai lộ trình dùng chung trực giác phần cứng chương 00–07; khác nhau ở chi phí máy tính.",
  objectives_en=[
    "Compare Track A (MCU budget) vs Track B (ROS PC/Pi)",
    "Pick ESP32 or Pico as primary MCU",
    "Defer Pi 5 until bridging needs it",
    "Limit first shopping trip to essentials",
    "Map chapters to tracks",
  ],
  objectives_vi=[
    "So sánh Track A (MCU) và Track B (ROS)",
    "Chọn ESP32 hoặc Pico",
    "Hoãn Pi 5 đến khi cần bridge",
    "Giới hạn lần mua đầu",
    "Map chương theo track",
  ],
  theory_en=[
    ("Track A — MCU (~$40–90 parts)",
     "ESP32 DevKit or Pico + TT diff chassis + TB6612/DRV8833-class driver + ranging + optional IMU/encoders. Outcome: teleop, stops, later PID—no ROS required."),
    ("Track B — ROS",
     "Same robot plus Ubuntu 24.04 for ROS 2 Jazzy. Optional Raspberry Pi 5 onboard later. Outcome: topics, TF, URDF, Gazebo Harmonic, Nav2 tour, LeRobot on a workstation."),
    ("Why Capstone A first",
     "Duckietown-style programs work because autonomy sits on a boring reliable base. Finish teleop firmware before SLAM shopping."),
  ],
  theory_vi=[
    ("Track A — MCU",
     "ESP32/Pico + khung TT + driver TB6612/DRV8833 + ranging + IMU/encoder tùy chọn. Teleop ổn định không cần ROS."),
    ("Track B — ROS",
     "Cùng robot + Ubuntu 24.04 / ROS 2 Jazzy; Pi 5 tùy chọn sau."),
    ("Capstone A trước",
     "Tự hành chỉ vững khi nền teleop nhàm chán nhưng đáng tin."),
  ],
  math_en="Rough cost model: \(C \\approx C_{\\mathrm{mcu}}+C_{\\mathrm{chassis}}+C_{\\mathrm{driver}}+C_{\\mathrm{batt}}+C_{\\mathrm{tools}}\). Keep \(C_{\\mathrm{sensors}}\) small until Capstone A acceptance.",
  math_vi="Mô hình chi phí: \(C \\approx C_{\\mathrm{mcu}}+C_{\\mathrm{chassis}}+C_{\\mathrm{driver}}+C_{\\mathrm{batt}}+C_{\\mathrm{tools}}\). Giữ \(C_{\\mathrm{sensors}}\) nhỏ đến khi nghiệm thu Capstone A.",
  lab_en="Write Track A or B choice; list ≤3 purchases for this week; price TB6612 vs L298N.",
  lab_vi="Chọn track; ≤3 món mua tuần này; so giá TB6612 vs L298N.",
  pitfalls_en=["Buying LiDAR before blink", "Assuming VM GPU is required for Jazzy tutorials"],
  pitfalls_vi=["Mua LiDAR trước khi blink", "Nghĩ cần GPU cho tutorial Jazzy cơ bản"],
  links=["linorobot2", "microros", "platformio"],
)

F("safety_mindset_lab",
  hook_en="Robots combine stored energy, spinning parts, and buggy software. Safety is a design constraint.",
  hook_vi="Robot gồm năng lượng tích trữ, chi tiết quay và phần mềm lỗi. An toàn là ràng buộc thiết kế.",
  objectives_en=["List electrical/mechanical/battery/software hazards","Practice power-last ritual","Clamp PWM and command timeouts","Plan E-stop story","Ventilate soldering"],
  objectives_vi=["Liệt kê rủi ro điện/cơ/pin/phần mềm","Nghi thức cấp nguồn sau cùng","Giới hạn PWM và timeout lệnh","Lên kế hoạch E-stop","Thông gió khi hàn"],
  theory_en=[
    ("Non-negotiables",
     "Matched lithium chargers only; fire-safe charging; never short packs. Red/black polarity. Never put motor voltage on 3.3 V pins. Lift wheels when testing motion code. Watchdog: if teleop silent >200–500 ms, command zero."),
    ("E-stop layers",
     "Hardware kill on battery high-side when feasible; software timeout; mechanical blocking during bring-up."),
  ],
  theory_vi=[
    ("Không thỏa hiệp",
     "Sạc lithium đúng loại; cực tính; tách nguồn; nhấc bánh khi test; timeout teleop."),
    ("Lớp E-stop",
     "Ngắt phần cứng nếu được; timeout phần mềm; chèn cơ khi bring-up."),
  ],
  math_en="Energy in a capacitor \(E=\\frac12 CV^2\) is a reminder that bulk caps and packs store punch—discharge intentionally.",
  math_vi="\(E=\\frac12 CV^2\) nhắc rằng tụ/pin tích năng lượng—xả có chủ đích.",
  lab_en="Photo your charger; write 5-step power-up checklist; pseudocode teleop timeout.",
  lab_vi="Chụp bộ sạc; checklist 5 bước; pseudocode timeout.",
  pitfalls_en=["Leaving stalled motors powered","USB powering motors"],
  pitfalls_vi=["Để motor stall còn cấp nguồn","Lấy USB nuôi motor"],
  links=["sparkfun_logic"],
)

F("bom_and_shopping",
  hook_en="Primary lab track: ESP32 (or Pico) + diff-drive chassis + motor driver + ultrasonic/IMU; optional Pi 5 later.",
  hook_vi="Lab chính: ESP32 (hoặc Pico) + khung vi sai + driver + siêu âm/IMU; Pi 5 tùy chọn sau.",
  objectives_en=["Build a BOM with must/nice","Prefer modern H-bridge modules","Budget hand tools","Avoid fake chargers","Plan spares"],
  objectives_vi=["Lập BOM must/nice","Ưu tiên module H-bridge hiện đại","Ngân sách dụng cụ","Tránh sạc giả","Dự phòng linh kiện"],
  theory_en=[
    ("Default BOM",
     "ESP32 DevKit or Pico W; TT 2WD chassis; TB6612/DRV8833; HC-SR04 or VL53L0X; optional MPU-6050; encoders; chemistry-matched battery+charger; Dupont/silicone wire; iron+multimeter."),
    ("Driver choice",
     "L298N is common but inefficient/heaty. TB6612/DRV8833-class parts behave better for 3.3 V logic small robots (see Pololu motor driver docs)."),
  ],
  theory_vi=[
    ("BOM mặc định",
     "ESP32/Pico W; khung TT 2WD; TB6612/DRV8833; HC-SR04 hoặc VL53L0X; MPU-6050 tùy chọn; encoder; pin+sạc; dây; mỏ hàn+ĐHVN."),
    ("Chọn driver",
     "L298N phổ biến nhưng nóng/hao. TB6612/DRV8833 thường phù hợp robot nhỏ logic 3.3 V."),
  ],
  math_en="Check \(I_{\\mathrm{stall,left}}+I_{\\mathrm{stall,right}} < I_{\\mathrm{driver,cont}}\) with margin; peak may be higher briefly.",
  math_vi="Kiểm \(I_{\\mathrm{stall},L}+I_{\\mathrm{stall},R} < I_{\\mathrm{driver}}\) có hệ số an toàn.",
  lab_en="Spreadsheet BOM with vendor links; defer sensors not needed for blink/spin.",
  lab_vi="BOM spreadsheet; hoãn cảm biến chưa cần cho blink/spin.",
  pitfalls_en=["9 V block into ESP32 5 V pin myths","No common ground between driver and MCU"],
  pitfalls_vi=["Cấp 9V bừa vào ESP32","Thiếu common ground"],
  links=["pololu_motor", "arduino"],
)

F("workspace_toolchain_preview",
  hook_en="Install friction kills momentum—preview toolchains now.",
  hook_vi="Ma sát cài đặt giết đà học—xem trước toolchain.",
  objectives_en=["USB serial readiness","Choose IDE/PlatformIO/MicroPython","Note Jazzy↔Ubuntu 24.04 pairing","Create lab folders","Bookmark tutorial hubs"],
  objectives_vi=["Sẵn sàng USB serial","Chọn IDE/PlatformIO/MicroPython","Nhớ Jazzy↔Ubuntu 24.04","Tạo thư mục lab","Bookmark tutorial"],
  theory_en=[
    ("Map",
     "ESP32 sketches: Arduino IDE or PlatformIO. Pico: MicroPython + Thonny/`mpremote`. ROS 2 Jazzy: follow official install. Sim: Gazebo Harmonic. Policies: LeRobot on a workstation."),
  ],
  theory_vi=[
    ("Bản đồ",
     "ESP32: Arduino/PlatformIO. Pico: MicroPython. ROS 2 Jazzy: docs chính thức. Sim: Gazebo Harmonic. Policy: LeRobot trên máy trạm."),
  ],
  math_en="Treat toolchain setup as critical path: \(T_{\\mathrm{total}}=T_{\\mathrm{install}}+T_{\\mathrm{blink}}\); shrink \(T_{\\mathrm{install}}\) with PlatformIO board presets.",
  math_vi="\(T_{\\mathrm{total}}=T_{\\mathrm{install}}+T_{\\mathrm{blink}}\); giảm \(T_{\\mathrm{install}}\) bằng preset PlatformIO.",
  lab_en="Create folders; install one firmware toolchain; bookmark ROS 2 Jazzy tutorials.",
  lab_vi="Tạo thư mục; cài một toolchain firmware; bookmark tutorial Jazzy.",
  pitfalls_en=["Mixing ROS distros in one OS", "Wrong board selected in IDE"],
  pitfalls_vi=["Trộn nhiều distro ROS", "Chọn sai board trong IDE"],
  links=["platformio", "ros2_tutorials", "gazebo", "esp32", "pico"],
)
