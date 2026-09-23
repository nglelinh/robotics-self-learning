#!/usr/bin/env python3
"""Simple labeled teaching diagrams for chapters 00–03."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parents[1] / "img" / "generated"
OUT.mkdir(parents=True, exist_ok=True)

def font(size):
    for p in (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ):
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def font_b(size):
    for p in (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    ):
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return font(size)

FG = (25, 32, 40)
MUTED = (70, 82, 96)
BLUE = (24, 88, 158)
RED = (176, 48, 48)
GREEN = (28, 120, 72)
AMBER = (168, 104, 16)
BG = (255, 255, 255)
LINE = (40, 48, 58)

def new(w, h):
    im = Image.new("RGB", (w, h), BG)
    return im, ImageDraw.Draw(im)

def title(d, text, w):
    f = font_b(28)
    d.text((28, 18), text, fill=FG, font=f)

def save(im, name):
    im.save(OUT / name, "PNG")
    print("wrote", name)

def tracks():
    im, d = new(1100, 520)
    title(d, "Two study tracks  |  Hai lộ trình", 1100)
    f, fs = font(20), font(16)
    d.rounded_rectangle((40, 80, 520, 470), 16, outline=BLUE, width=3)
    d.rounded_rectangle((580, 80, 1060, 470), 16, outline=GREEN, width=3)
    d.text((60, 100), "Track A — MCU budget", fill=BLUE, font=font_b(22))
    d.text((60, 140), "ESP32 or Pico + TT chassis", fill=FG, font=f)
    d.text((60, 175), "TB6612 / DRV8833 driver", fill=FG, font=f)
    d.text((60, 210), "HC-SR04 or small ToF", fill=FG, font=f)
    d.text((60, 245), "Firmware teleop (Ch.07)", fill=FG, font=f)
    d.text((60, 300), "No Ubuntu required yet.", fill=MUTED, font=fs)
    d.text((60, 330), "Capstone A is the goal.", fill=MUTED, font=fs)
    d.text((600, 100), "Track B — ROS 2 later", fill=GREEN, font=font_b(22))
    d.text((600, 140), "Same robot as Track A", fill=FG, font=f)
    d.text((600, 175), "Ubuntu 24.04 + Jazzy", fill=FG, font=f)
    d.text((600, 210), "Gazebo Harmonic (Ch.10)", fill=FG, font=f)
    d.text((600, 245), "micro-ROS on the MCU", fill=FG, font=f)
    d.text((600, 300), "Buy LiDAR only after", fill=MUTED, font=fs)
    d.text((600, 330), "Capstone A is reliable.", fill=MUTED, font=fs)
    d.text((60, 400), "Shared rule: trust the bench before you trust a topic.", fill=FG, font=f)
    save(im, "tracks_mcu_ros.png")

def power_order():
    im, d = new(1100, 280)
    title(d, "Power order  |  Thứ tự nguồn", 1100)
    f = font(18)
    boxes = [
        (40, "1. GND common\nchung mass"),
        (250, "2. Logic 3.3 V\nUSB / LDO"),
        (470, "3. Signals\nGPIO / PWM"),
        (690, "4. Motor VM\nlast ON"),
        (900, "5. Wheels up\nbánh nhấc"),
    ]
    for x, text in boxes:
        d.rounded_rectangle((x, 90, x + 180, 220), 12, outline=LINE, width=2, fill=(245, 248, 252))
        d.multiline_text((x + 14, 115), text, fill=FG, font=f, spacing=6)
    save(im, "power_order.png")

def rails():
    im, d = new(1100, 560)
    title(d, "ESP32 / Pico rails  |  Đường nguồn", 1100)
    f, fs = font(18), font(15)
    rows = [
        (90, RED, "5 V / VBUS", "USB power only. Do NOT feed motors from the 3.3 V pin."),
        (190, BLUE, "3.3 V GPIO", "ESP32 and Pico pins are 3.3 V logic. 5 V in can damage them."),
        (290, GREEN, "GND", "One common ground: MCU, driver logic, motor supply return."),
        (390, AMBER, "VM motor", "Separate battery or buck. Driver VM ≠ 3.3 V pin."),
    ]
    for y, color, name, note in rows:
        d.rectangle((40, y, 70, y + 50), fill=color)
        d.text((90, y + 4), name, fill=FG, font=font_b(22))
        d.text((90, y + 32), note, fill=MUTED, font=fs)
    d.text((40, 490), "Level-shift 5 V sensors (HC-SR04 echo) before a 3.3 V input.", fill=FG, font=f)
    save(im, "power_rails_3v3.png")

def pullup():
    im, d = new(980, 520)
    title(d, "Button to GND with pull-up  |  Nút nhấn kéo lên", 980)
    f = font(18)
    # MCU pin box
    d.rounded_rectangle((80, 160, 280, 280), 10, outline=BLUE, width=3)
    d.text((110, 195), "GPIO", fill=BLUE, font=font_b(22))
    d.text((100, 230), "INPUT_PULLUP", fill=MUTED, font=font(16))
    # wire to button
    d.line((280, 220, 520, 220), fill=LINE, width=3)
    d.line((400, 220, 400, 120), fill=LINE, width=3)
    d.rounded_rectangle((330, 50, 470, 120), 8, outline=AMBER, width=3)
    d.text((348, 72), "pull-up", fill=AMBER, font=f)
    d.text((360, 130), "to 3.3 V", fill=MUTED, font=font(16))
    # button
    d.rounded_rectangle((520, 170, 700, 270), 10, outline=FG, width=3)
    d.text((560, 200), "BUTTON", fill=FG, font=font_b(20))
    d.line((610, 270, 610, 380), fill=LINE, width=3)
    d.line((560, 380, 660, 380), fill=LINE, width=4)
    d.text((680, 365), "GND", fill=GREEN, font=font_b(20))
    d.text((80, 430), "Released: GPIO reads HIGH. Pressed: GPIO reads LOW.", fill=FG, font=f)
    d.text((80, 465), "Thả: đọc HIGH. Nhấn: đọc LOW. Không cần điện trở ngoài nếu bật pull-up.", fill=FG, font=f)
    save(im, "gpio_pullup_button.png")

def pwm():
    im, d = new(1100, 480)
    title(d, "PWM duty  |  Độ rộng xung", 1100)
    f = font(18)
    def wave(y, duty, label, color):
        d.text((30, y - 8), label, fill=color, font=font_b(18))
        x0, high, low = 280, y, y + 50
        period = 140
        on = int(period * duty)
        x = x0
        for _ in range(5):
            d.line((x, high, x + on, high), fill=color, width=3)
            d.line((x + on, high, x + on, low), fill=color, width=3)
            d.line((x + on, low, x + period, low), fill=color, width=3)
            d.line((x + period, low, x + period, high), fill=color, width=3)
            x += period
    wave(110, 0.25, "25%  slow", BLUE)
    wave(220, 0.50, "50%  mid", AMBER)
    wave(330, 0.90, "90%  fast", RED)
    d.text((30, 430), "Average voltage ≈ duty × VM. Start near 20–30% with wheels up.", fill=FG, font=f)
    save(im, "pwm_duty_cycle.png")

def debounce():
    im, d = new(1100, 420)
    title(d, "Contact bounce  |  Dội tiếp điểm", 1100)
    f = font(18)
    # ideal
    d.text((40, 80), "Ideal edge", fill=GREEN, font=font_b(18))
    d.line((220, 140, 360, 140), fill=GREEN, width=3)
    d.line((360, 140, 360, 90), fill=GREEN, width=3)
    d.line((360, 90, 900, 90), fill=GREEN, width=3)
    # bounce
    d.text((40, 190), "Real button", fill=RED, font=font_b(18))
    pts = [(220, 300), (360, 300), (360, 230), (390, 290), (410, 240), (440, 280), (470, 230), (500, 230), (900, 230)]
    d.line(pts, fill=RED, width=3)
    d.line((500, 180, 500, 340), fill=MUTED, width=1)
    d.text((510, 250), "stable after ~10–50 ms", fill=MUTED, font=f)
    d.text((40, 370), "Count one press only after the line stays still. Encoders need the same care.", fill=FG, font=f)
    save(im, "debounce_timeline.png")

def fsm():
    im, d = new(1100, 460)
    title(d, "Teleop state machine  |  Máy trạng thái", 1100)
    f = font(18)
    def box(x, y, w, h, text, color):
        d.rounded_rectangle((x, y, x + w, y + h), 12, outline=color, width=3)
        d.text((x + 16, y + 22), text, fill=color, font=font_b(20))
    box(60, 160, 220, 80, "IDLE", BLUE)
    box(420, 160, 240, 80, "TELEOP", GREEN)
    box(800, 160, 220, 80, "FAULT", RED)
    d.line((280, 200, 420, 200), fill=LINE, width=3)
    d.polygon([(410, 192), (430, 200), (410, 208)], fill=LINE)
    d.text((300, 160), "cmd", fill=MUTED, font=f)
    d.line((660, 200, 800, 200), fill=LINE, width=3)
    d.polygon([(790, 192), (810, 200), (790, 208)], fill=LINE)
    d.text((670, 155), "timeout\n~300 ms", fill=MUTED, font=f)
    d.line((910, 240, 910, 340), fill=LINE, width=3)
    d.line((910, 340, 170, 340), fill=LINE, width=3)
    d.line((170, 340, 170, 240), fill=LINE, width=3)
    d.polygon([(162, 250), (170, 230), (178, 250)], fill=LINE)
    d.text((400, 350), "reset / clear fault → IDLE, PWM = 0", fill=FG, font=f)
    d.text((60, 400), "In FAULT every motor PWM is forced to 0.", fill=FG, font=f)
    save(im, "firmware_state_machine.png")

def solder():
    im, d = new(1100, 420)
    title(d, "Solder joint  |  Mối hàn", 1100)
    f = font(18)
    # good cone
    d.ellipse((180, 140, 280, 240), outline=GREEN, width=4)
    d.polygon([(230, 150), (200, 250), (260, 250)], outline=GREEN)
    d.line((230, 80, 230, 300), fill=MUTED, width=4)
    d.text((140, 320), "Good: shiny fillet\nTốt: bóng, ôm chân", fill=GREEN, font=f)
    # bad blob
    d.ellipse((620, 130, 780, 270), outline=RED, width=4)
    d.line((700, 80, 700, 300), fill=MUTED, width=4)
    d.text((600, 320), "Bad: cold blob\nXấu: cục, mờ, không ôm", fill=RED, font=f)
    save(im, "solder_joint_compare.png")

def led():
    im, d = new(980, 360)
    title(d, "LED series resistor  |  Điện trở nối tiếp LED", 980)
    f = font(20)
    d.line((60, 180, 900, 180), fill=LINE, width=3)
    d.rounded_rectangle((80, 140, 200, 220), 8, outline=RED, width=3)
    d.text((100, 165), "3.3 V", fill=RED, font=font_b(20))
    d.rectangle((320, 150, 460, 210), outline=BLUE, width=3)
    d.text((345, 165), "R", fill=BLUE, font=font_b(22))
    # LED triangle-ish
    d.polygon([(620, 150), (620, 210), (690, 180)], outline=AMBER)
    d.line((690, 150, 690, 210), fill=AMBER, width=3)
    d.text((600, 230), "LED", fill=AMBER, font=f)
    d.text((820, 160), "GND", fill=GREEN, font=font_b(20))
    d.text((60, 280), "R = (Vsupply − Vf) / I      example: (3.3 − 2.0) / 0.008 ≈ 162 Ω → use 180 Ω", fill=FG, font=f)
    save(im, "led_series_resistor.png")

if __name__ == "__main__":
    tracks(); power_order(); rails(); pullup(); pwm(); debounce(); fsm(); solder(); led()
