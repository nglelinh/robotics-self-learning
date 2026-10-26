#!/usr/bin/env python3
"""Educational figures for the robotics lessons. Numbers printed here are copied into the lessons."""

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Rectangle

OUT = os.path.join(os.path.dirname(__file__), "..", "img", "generated")
os.makedirs(OUT, exist_ok=True)


def save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, dpi=140, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("wrote", path)


def pid_step():
    # Second-order teaching plant, not a measured TT motor:
    # ydd + 2*zeta*wn*yd + wn^2*y = wn^2*(u - bias)
    dt = 0.005
    wn = 8.0
    zeta = 0.9
    bias = 0.08
    r = 0.25
    t_end = 6.0
    n = int(t_end / dt)

    def run(kp, ki, kd):
        y = 0.0
        yd = 0.0
        I = 0.0
        e_prev = r
        ys, us = [], []
        for _ in range(n):
            e = r - y
            I = float(np.clip(I + e * dt, -1.0, 1.0))
            u = kp * e + ki * I + kd * (e - e_prev) / dt
            u = float(np.clip(u, -2.0, 2.0))
            yd = yd + dt * (wn ** 2 * ((u - bias) - y) - 2 * zeta * wn * yd)
            y = y + dt * yd
            e_prev = e
            ys.append(y)
            us.append(u)
        return np.array(ys), np.array(us)

    cases = [
        ("P: Kp=8", 8, 0, 0, "#c0392b"),
        ("PD: Kp=8, Kd=0,15", 8, 0, 0.15, "#2471a3"),
        ("PID: Kp=4, Ki=2, Kd=0,08", 4, 2.0, 0.08, "#1e8449"),
    ]
    t = np.arange(n) * dt
    fig, ax = plt.subplots(figsize=(8.2, 4.4))
    ax.plot(t, np.full_like(t, r), "k--", lw=1.2, label="setpoint 0,25 m/s")
    for label, kp, ki, kd, color in cases:
        ys, us = run(kp, ki, kd)
        ax.plot(t, ys, color=color, lw=2, label=label)
        print(label, "y_final", round(ys[-1], 4), "u_final", round(us[-1], 2), "ymax", round(ys.max(), 4))
    ax.set_xlabel("t (s)")
    ax.set_ylabel("tốc độ vành y (m/s)")
    ax.set_title("Mô phỏng bậc hai: lệch tải b = 0,08")
    ax.legend(loc="lower right", fontsize=8)
    ax.set_xlim(0, t_end)
    ax.set_ylim(0, 0.45)
    ax.grid(True, alpha=0.3)
    save(fig, "ch08_pid_step_response.png")


def odom_path():
    r = 0.033
    L = 0.16
    N = 1440  # counts per wheel revolution
    # 20 ms ticks. Straight 1.0 m, then spin left ~90 deg, then straight 0.5 m.
    meters_per_count = 2 * np.pi * r / N
    # straight: both wheels +counts. 1.0 m / meters_per_count
    c_straight = int(round(1.0 / meters_per_count))
    # 90 deg: delta_s_r - delta_s_l = L * dpsi, dpsi = pi/2
    # opposite counts: arc = (L/2) * dpsi
    arc = (L / 2) * (np.pi / 2)
    c_turn = int(round(arc / meters_per_count))
    c_short = int(round(0.50 / meters_per_count))
    print("meters_per_count", meters_per_count)
    print("counts straight 1m", c_straight, "turn counts", c_turn, "short", c_short)

    ticks = []
    for _ in range(50):
        ticks.append((c_straight / 50, c_straight / 50))
    for _ in range(20):
        ticks.append((-c_turn / 20, c_turn / 20))
    for _ in range(25):
        ticks.append((c_short / 25, c_short / 25))

    x, y, psi = 0.0, 0.0, 0.0
    xs, ys = [x], [y]
    for dl, dr in ticks:
        ds_l = dl * meters_per_count
        ds_r = dr * meters_per_count
        ds = 0.5 * (ds_r + ds_l)
        dpsi = (ds_r - ds_l) / L
        x += ds * np.cos(psi + 0.5 * dpsi)
        y += ds * np.sin(psi + 0.5 * dpsi)
        psi += dpsi
        xs.append(x)
        ys.append(y)
    print("end pose", round(x, 4), round(y, 4), round(psi, 4))

    fig, ax = plt.subplots(figsize=(6.2, 5.2))
    ax.plot(xs, ys, color="#1a5276", lw=2)
    ax.scatter([xs[0]], [ys[0]], c="#1e8449", s=40, label="start", zorder=3)
    ax.scatter([xs[-1]], [ys[-1]], c="#c0392b", s=40, label="end", zorder=3)
    ax.annotate("", xy=(xs[10], ys[10]), xytext=(xs[0], ys[0]),
                arrowprops=dict(arrowstyle="->", color="#1e8449"))
    ax.set_aspect("equal")
    ax.grid(True, alpha=0.3)
    ax.set_xlabel("x (m)")
    ax.set_ylabel("y (m)")
    ax.set_title("Odometry điểm giữa: thẳng, quay trái, thẳng")
    ax.legend()
    save(fig, "ch08_odom_path.png")


def frames():
    fig, ax = plt.subplots(figsize=(6.4, 5.4))
    ax.set_aspect("equal")
    ax.set_xlim(-0.2, 1.3)
    ax.set_ylim(-0.3, 1.2)
    ax.axis("off")
    ax.set_title("base_link và một frame con quay 90°")

    def axes(origin, theta, name, color):
        o = np.array(origin, dtype=float)
        R = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
        xh = o + R @ np.array([0.38, 0.0])
        yh = o + R @ np.array([0.0, 0.38])
        ax.annotate("", xy=xh, xytext=o, arrowprops=dict(arrowstyle="-|>", color=color, lw=2))
        ax.annotate("", xy=yh, xytext=o, arrowprops=dict(arrowstyle="-|>", color=color, lw=2))
        ax.text(*(o + R @ np.array([0.42, -0.02])), f"{name} +x", color=color, fontsize=9)
        ax.text(*(o + R @ np.array([0.02, 0.42])), f"+y", color=color, fontsize=9)
        ax.plot(*o, "o", color=color)

    axes((0.15, 0.15), 0.0, "base", "#1a5276")
    axes((0.70, 0.45), np.pi / 2, "laser", "#c0392b")
    ax.annotate("", xy=(0.70, 0.45), xytext=(0.15, 0.15),
                arrowprops=dict(arrowstyle="->", color="#7f8c8d", lw=1.5))
    ax.text(0.28, 0.38, "t = (0,55; 0,30) m", color="#7f8c8d", fontsize=9)
    save(fig, "ch08_math_frames.png")


def quaternion():
    fig, ax = plt.subplots(figsize=(6.2, 4.6))
    ax.set_aspect("equal")
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.3, 1.3)
    ax.axhline(0, color="#bbb", lw=1)
    ax.axvline(0, color="#bbb", lw=1)
    circ = Circle((0, 0), 1.0, fill=False, ls="--", color="#85929e")
    ax.add_patch(circ)
    theta = np.pi / 2
    ax.annotate("", xy=(0, 1), xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color="#1e8449", lw=2))
    ax.annotate("", xy=(1, 0), xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color="#1a5276", lw=2))
    arc_t = np.linspace(0, theta, 40)
    ax.plot(0.45 * np.cos(arc_t), 0.45 * np.sin(arc_t), color="#c0392b", lw=2)
    ax.text(0.15, 0.22, "θ = 90°", color="#c0392b")
    ax.text(1.05, -0.08, "v", color="#1a5276")
    ax.text(0.05, 1.05, "v'", color="#1e8449")
    half = theta / 2
    qz = np.sin(half)
    qw = np.cos(half)
    ax.set_title(f"Yaw 90°: q = (x, y, z, w) = (0, 0, {qz:.3f}, {qw:.3f})")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    print("quat yaw90", 0, 0, qz, qw)
    save(fig, "ch08_quaternion_yaw.png")


def battery():
    fig, ax = plt.subplots(figsize=(9.2, 4.8))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 8)
    ax.axis("off")
    ax.set_title("Cây nguồn Capstone: pin → công tắc → chì → VM và buck")

    def box(x, y, w, h, text, color):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08,rounding_size=0.15",
                                    facecolor=color, edgecolor="#1c2833", lw=1.2))
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=8)

    box(0.3, 3.2, 2.2, 1.6, "Pin\n2S", "#f5b041")
    box(3.1, 3.2, 2.0, 1.6, "Công tắc", "#d5d8dc")
    box(5.7, 3.2, 1.8, 1.6, "Cầu chì\n2–3 A", "#f1948a")
    box(8.2, 5.0, 2.4, 1.6, "VM driver\nTB6612", "#85c1e9")
    box(8.2, 1.2, 2.4, 1.6, "Buck\n→ 5,0 V", "#82e0aa")
    box(11.4, 5.0, 2.3, 1.6, "Motor\ntrái / phải", "#aed6f1")
    box(11.4, 1.2, 2.3, 1.6, "ESP32\nlogic", "#abebc6")
    box(14.1, 3.2, 1.6, 1.6, "GND\nchung", "#fad7a0")

    def arrow(x1, y1, x2, y2):
        ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=12, color="#1c2833"))

    arrow(2.5, 4.0, 3.1, 4.0)
    arrow(5.1, 4.0, 5.7, 4.0)
    arrow(7.5, 4.2, 8.2, 5.6)
    arrow(7.5, 3.8, 8.2, 2.2)
    arrow(10.6, 5.8, 11.4, 5.8)
    arrow(10.6, 2.0, 11.4, 2.0)
    ax.plot([1.4, 1.4, 14.9], [3.2, 0.5, 0.5], color="#b9770e", lw=1.4)
    ax.plot([14.9, 14.9], [0.5, 3.2], color="#b9770e", lw=1.4)
    ax.text(6.2, 0.15, "mass chung: cực âm pin, GND driver, GND buck, GND ESP32", fontsize=8, color="#b9770e")
    ax.text(0.3, 7.2, "Không nối cực dương pin vào chân 5 V hoặc 3,3 V của ESP32.", fontsize=8, color="#922b21")
    save(fig, "ch07_battery_wiring.png")


def sbc_net():
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)
    ax.axis("off")
    ax.set_title("Cùng ROS_DOMAIN_ID, cùng mạng: laptop, SBC, ESP32")

    def box(x, y, w, h, text, color):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08,rounding_size=0.12",
                                    facecolor=color, edgecolor="#1c2833"))
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=8)

    box(0.4, 3.4, 3.2, 1.8, "Laptop\nUbuntu 24.04\nJazzy\nDOMAIN 42", "#d4e6f1")
    box(4.4, 3.4, 3.2, 1.8, "Pi 5 hoặc Orin Nano\nUbuntu 24.04\nagent / bridge\nDOMAIN 42", "#d5f5e3")
    box(8.4, 3.4, 3.2, 1.8, "ESP32\nmicro-ROS\n/dev/esp32", "#fdebd0")
    ax.annotate("", xy=(4.4, 4.3), xytext=(3.6, 4.3), arrowprops=dict(arrowstyle="<->", color="#1a5276"))
    ax.annotate("", xy=(8.4, 4.3), xytext=(7.6, 4.3), arrowprops=dict(arrowstyle="<->", color="#1a5276"))
    ax.text(3.55, 4.55, "DDS", fontsize=8, color="#1a5276")
    ax.text(7.6, 4.55, "serial", fontsize=8, color="#1a5276")
    ax.text(0.4, 1.6, "Mac: máy ảo Ubuntu 24.04 có USB passthrough.\nDocker Desktop trên macOS không đưa /dev/ttyUSB vào container.", fontsize=8)
    save(fig, "ch09_sbc_network.png")


def capstone_b():
    fig, ax = plt.subplots(figsize=(8.6, 3.6))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 4)
    ax.axis("off")
    ax.set_title("Capstone B: mô phỏng trước, robot thật sau")

    def box(x, y, text, color):
        ax.add_patch(FancyBboxPatch((x, y), 3.3, 2.2, boxstyle="round,pad=0.08,rounding_size=0.12",
                                    facecolor=color, edgecolor="#1c2833"))
        ax.text(x + 1.65, y + 1.1, text, ha="center", va="center", fontsize=8)

    box(0.3, 0.9, "1. Gazebo\nTurtleBot3\nslam:=True", "#d4e6f1")
    box(4.3, 0.9, "2. Lidar thật\n/scan + TF\nslam_toolbox", "#d5f5e3")
    box(8.3, 0.9, "3. Nav2\ngoal → Twist\nmap_saver", "#fdebd0")
    ax.annotate("", xy=(4.3, 2.0), xytext=(3.6, 2.0), arrowprops=dict(arrowstyle="-|>", color="#1c2833"))
    ax.annotate("", xy=(8.3, 2.0), xytext=(7.6, 2.0), arrowprops=dict(arrowstyle="-|>", color="#1c2833"))
    save(fig, "ch11_capstone_b.png")


def so101():
    fig, ax = plt.subplots(figsize=(8.2, 3.8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 4.2)
    ax.axis("off")
    ax.set_title("SO-101 ghi 6 số khớp. VLA không xuất vector đó.")
    ax.add_patch(FancyBboxPatch((0.3, 1.3), 5.2, 2.2, boxstyle="round,pad=0.08", facecolor="#d5f5e3", edgecolor="#1c2833"))
    ax.text(2.9, 2.4, "action SO-101\n6 motor: pan, lift, elbow,\nwrist flex, wrist roll, gripper", ha="center", va="center", fontsize=8)
    ax.add_patch(FancyBboxPatch((6.5, 1.3), 5.2, 2.2, boxstyle="round,pad=0.08", facecolor="#f5b7b1", edgecolor="#1c2833"))
    ax.text(9.1, 2.4, "action VLA (Open X)\nđầu cuối + kẹp\ncủa robot trong dataset", ha="center", va="center", fontsize=8)
    ax.annotate("", xy=(6.5, 2.4), xytext=(5.5, 2.4), arrowprops=dict(arrowstyle="<->", color="#922b21", lw=1.5))
    ax.text(0.4, 0.4, "Không gán ô kẹp của checkpoint sang một khớp cổ tay.", fontsize=8, color="#922b21")
    save(fig, "ch12_so101_action.png")


if __name__ == "__main__":
    pid_step()
    odom_path()
    frames()
    quaternion()
    battery()
    sbc_net()
    capstone_b()
    so101()
