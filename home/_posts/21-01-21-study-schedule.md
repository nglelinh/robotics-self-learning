---
layout: post
title: "Lịch 24 tuần"
chapter: home
order: 6
owner: Nguyen Le Linh
---

## Lịch 24 tuần

Mỗi tuần dành **6–8 giờ**: giờ bài trong [mục lục]({{ site.baseurl }}/home/contents/) cộng thời gian ghi sổ và sửa lỗi. 96 bài cộng lại khoảng 135 giờ bài; phần sổ kéo mỗi tuần vào khoảng trên. Làm tuần nào xong tuần đó. Bài Lab cần bàn hoặc máy; bài Concept có thể đọc trước rồi quay lại khi có linh kiện.

Đường chính của ROS 2 là **rclpy** và **rclcpp**. [rclgo](https://github.com/tiiuae/rclgo) là đường phụ cho người đã quen Go: đọc API sau khi topic bằng Python hoặc C++ đã chạy, không thay bài trên site.

Cột **Mua** là tuần cần hàng về trước khi làm phần cứng của tuần đó. Phần mô phỏng không chờ lidar hay tay máy. Giá để trống trong BOM; điền sau khi mở trang shop.

| Tuần | Trọng tâm | Giờ | Mua trước tuần này |
| ---: | --- | ---: | --- |
| 1 | Bàn lab và an toàn | 7,5 | Dụng cụ bàn nếu chưa có |
| 2 | Đo điện, linh kiện thụ động | 7,0 | Đợt 1: điện trở, LED, dây |
| 3 | Linh kiện chủ động và datasheet | 7,5 | |
| 4 | Hàn, checklist điện, chọn MCU | 7,0 | ESP32 hoặc Pico |
| 5 | Blink, serial, vào C++ / MicroPython | 7,0 | |
| 6 | GPIO, PWM, ngắt, máy trạng thái | 7,0 | |
| 7 | Bus và encoder, kèm sổ I2C | 7,0 | |
| 8 | ToF, camera, cầu H | 7,0 | Cảm biến, driver, motor đợt 2 |
| 9 | Servo, dòng, vòng kín nhỏ | 7,0 | |
| 10 | Khung, bánh răng, bánh xe | 7,0 | |
| 11 | Vật liệu và checklist cơ khí | 6,5 | |
| 12 | Pin rồi mới lắp khung | 6,5 | Pin, cầu chì, buck, BMS, khung |
| 13 | Driver và teleop | 6,5 | |
| 14 | Nghiệm thu xe và toán cho TF | 6,5 | |
| 15 | Serial, MQTT, PID | 6,5 | Encoder nếu motor TT chưa có |
| 16 | Odometry và checklist chương 08 | 6,5 | |
| 17 | Linux trên SBC và cài Jazzy | 6,5 | Pi 5 hoặc Jetson, hoặc hoãn và dùng laptop |
| 18 | Topic, TF2, URDF | 8,0 | |
| 19 | Gazebo và micro-ROS | 6,5 | |
| 20 | Nối xe thật và sim-to-real | 6,5 | |
| 21 | Đọc SLAM, Nav2, BT, MoveIt | 7,0 | |
| 22 | Capstone B: SLAM rồi Nav2 | 6,5 | Lidar trước nửa xe thật, không trước phần sim |
| 23 | LeRobot, ACT, Diffusion Policy, VLA | 7,0 | |
| 24 | Lab SO-101 hoặc đường giấy | 6,5 | Tay SO-101 chỉ nếu làm đường tay thật |

## Tuần 1 — bàn lab (7,5 giờ)

Bài: [00_01]({{ site.baseurl }}/contents/vi/chapter00/00_01_welcome_and_outcomes/), [00_02]({{ site.baseurl }}/contents/vi/chapter00/00_02_learning_tracks_budget/), [00_03]({{ site.baseurl }}/contents/vi/chapter00/00_03_safety_mindset_lab/), [00_04]({{ site.baseurl }}/contents/vi/chapter00/00_04_kit_catalog_tooling/), [00_05]({{ site.baseurl }}/contents/vi/chapter00/00_05_bom_and_shopping/). Khoảng 7 giờ bài. Sổ 0,5 giờ: liệt kê dụng cụ đang có và món còn thiếu. **Mua** kính, đồng hồ, mỏ hàn, breadboard nếu bàn trống. Chưa mua lidar, Pi hay Jetson.

## Tuần 2 — đo và nhận linh kiện thụ động (7 giờ)

Bài: [00_06]({{ site.baseurl }}/contents/vi/chapter00/00_06_workspace_toolchain_preview/), [00_07]({{ site.baseurl }}/contents/vi/chapter00/00_07_ch00_lab_checklist/), [01_01]({{ site.baseurl }}/contents/vi/chapter01/01_01_voltage_current_ohm/), [01_02]({{ site.baseurl }}/contents/vi/chapter01/01_02_breadboard_meter/), [01_03]({{ site.baseurl }}/contents/vi/chapter01/01_03_resistor_color_smd/). Khoảng 6,5 giờ bài, sổ 0,5 giờ. **Mua đợt 1** theo BOM: điện trở, LED, dây nhảy. Checklist chương 00 phải đạt trước khi cắm nguồn bàn.

## Tuần 3 — linh kiện chủ động (7,5 giờ)

Bài: [01_04]({{ site.baseurl }}/contents/vi/chapter01/01_04_cap_diode_led_id/), [01_05]({{ site.baseurl }}/contents/vi/chapter01/01_05_transistor_mosfet_ic_id/), [01_06]({{ site.baseurl }}/contents/vi/chapter01/01_06_connectors_drivers_boards/), [01_07]({{ site.baseurl }}/contents/vi/chapter01/01_07_datasheet_pinouts/), [01_08]({{ site.baseurl }}/contents/vi/chapter01/01_08_soldering_basics/). Khoảng 7,25 giờ bài, sổ 0,25 giờ: một chân datasheet bạn sẽ dùng ở chương 02.

## Tuần 4 — xong điện, mở MCU (7 giờ)

Bài: [01_09]({{ site.baseurl }}/contents/vi/chapter01/01_09_esd_polarity_brownout/), [01_10]({{ site.baseurl }}/contents/vi/chapter01/01_10_component_id_lab/), [01_11]({{ site.baseurl }}/contents/vi/chapter01/01_11_ch01_lab_checklist/), [02_01]({{ site.baseurl }}/contents/vi/chapter02/02_01_mcu_landscape/), [02_02]({{ site.baseurl }}/contents/vi/chapter02/02_02_esp32_platformio/). Khoảng 6,5 giờ bài, sổ 0,5 giờ. **Mua** một ESP32 có USB-UART trên board, hoặc Pico nếu bạn chọn nhánh MicroPython. Đừng mua module SoC trần chưa có cổng nạp.

## Tuần 5 — chương trình đầu tiên (7 giờ)

Bài: [02_03]({{ site.baseurl }}/contents/vi/chapter02/02_03_pico_micropython/), [02_04]({{ site.baseurl }}/contents/vi/chapter02/02_04_blink_serial_hello/), [02_05]({{ site.baseurl }}/contents/vi/chapter02/02_05_pinouts_power_rails/), [02_06]({{ site.baseurl }}/contents/vi/chapter02/02_06_ch02_lab_checklist/), [03_01]({{ site.baseurl }}/contents/vi/chapter03/03_01_cpp_vs_micropython/). Khoảng 6,5 giờ bài, sổ 0,5 giờ: dán ảnh serial “hello” vào sổ. Pico là để biết MicroPython; ESP32 vẫn là máy của capstone nếu bạn chỉ giữ một board.

## Tuần 6 — mẫu firmware (7 giờ)

Bài: [03_02]({{ site.baseurl }}/contents/vi/chapter03/03_02_gpio_patterns/), [03_03]({{ site.baseurl }}/contents/vi/chapter03/03_03_pwm_timers/), [03_04]({{ site.baseurl }}/contents/vi/chapter03/03_04_interrupts_debounce/), [03_05]({{ site.baseurl }}/contents/vi/chapter03/03_05_state_machines_fw/), [03_06]({{ site.baseurl }}/contents/vi/chapter03/03_06_ch03_lab_checklist/). Khoảng 6,75 giờ bài, sổ 0,25 giờ. PWM tuần này là tín hiệu, chưa nối motor.

## Tuần 7 — bus và đếm xung (7 giờ)

Bài: [04_01]({{ site.baseurl }}/contents/vi/chapter04/04_01_bus_interfaces/), [04_02]({{ site.baseurl }}/contents/vi/chapter04/04_02_sensor_package_id/), [04_03]({{ site.baseurl }}/contents/vi/chapter04/04_03_encoders_counts/), [04_04]({{ site.baseurl }}/contents/vi/chapter04/04_04_imu_basics/). Khoảng 5,75 giờ bài. Sổ 1,25 giờ: quét địa chỉ I2C nếu đã có IMU, hoặc vẽ sơ đồ chân module bạn định mua tuần sau. Tuần này ngắn hơn các tuần lab vì chưa bắt buộc hàng cảm biến về.

## Tuần 8 — khoảng cách và driver (7 giờ)

Bài: [04_05]({{ site.baseurl }}/contents/vi/chapter04/04_05_ultrasonic_tof/), [04_06]({{ site.baseurl }}/contents/vi/chapter04/04_06_cameras_robots/), [04_07]({{ site.baseurl }}/contents/vi/chapter04/04_07_ch04_lab_checklist/), [05_01]({{ site.baseurl }}/contents/vi/chapter05/05_01_dc_hbridge/), [05_02]({{ site.baseurl }}/contents/vi/chapter05/05_02_driver_board_id/). Khoảng 6,5 giờ bài, sổ 0,5 giờ. **Mua đợt 2:** HC-SR04 hoặc VL53L0X, mạch chuyển mức nếu echo 5 V, driver TB6612 hoặc DRV8833, hai motor TT. Camera để đọc; chưa cần mua.

## Tuần 9 — chấp hành và nhiệt (7 giờ)

Bài: [05_03]({{ site.baseurl }}/contents/vi/chapter05/05_03_servos_pwm/), [05_04]({{ site.baseurl }}/contents/vi/chapter05/05_04_steppers_intro/), [05_05]({{ site.baseurl }}/contents/vi/chapter05/05_05_current_thermal/), [05_06]({{ site.baseurl }}/contents/vi/chapter05/05_06_closed_loop_intro/), [05_07]({{ site.baseurl }}/contents/vi/chapter05/05_07_ch05_lab_checklist/). Khoảng 6,5 giờ bài, sổ 0,5 giờ. Ghi dòng không tải và dòng khi giữ trục, vì tuần 12 dùng số đó để chọn cầu chì.

## Tuần 10 — cơ cấu (7 giờ)

Bài: [06_01]({{ site.baseurl }}/contents/vi/chapter06/06_01_chassis_anatomy/), [06_02]({{ site.baseurl }}/contents/vi/chapter06/06_02_fasteners_bearings_shafts/), [06_03]({{ site.baseurl }}/contents/vi/chapter06/06_03_gear_trains_ratios/), [06_04]({{ site.baseurl }}/contents/vi/chapter06/06_04_linkages_belts_cams/), [06_05]({{ site.baseurl }}/contents/vi/chapter06/06_05_wheels_casters_diff/). Khoảng 6,5 giờ bài, sổ 0,5 giờ: đo đường kính bánh bạn sẽ lắp, ghi mét trên một vòng.

## Tuần 11 — lắp được thì mới siết (6,5 giờ)

Bài: [06_06]({{ site.baseurl }}/contents/vi/chapter06/06_06_materials_print_laser/), [06_07]({{ site.baseurl }}/contents/vi/chapter06/06_07_mech_failure_modes/), [06_08]({{ site.baseurl }}/contents/vi/chapter06/06_08_mechanisms_lab/), [06_09]({{ site.baseurl }}/contents/vi/chapter06/06_09_ch06_lab_checklist/). Khoảng 5 giờ bài. Sổ 1,5 giờ: checklist ốc, backlash, và một tờ nháp vị trí pin, driver, MCU. Chưa cắm pin.

## Tuần 12 — nguồn trước, khung sau (6,5 giờ)

Bài: [07_00]({{ site.baseurl }}/contents/vi/chapter07/07_00_batteries_power_safety/), [07_01]({{ site.baseurl }}/contents/vi/chapter07/07_01_assemble_power/). Khoảng 4 giờ bài. Sổ 2,5 giờ: điện áp từng cell, điện áp sau buck **trước** khi nối ESP32, vị trí cầu chì trên cực dương. **Mua** pin đúng hóa học (Li-ion / LiPo / LiFePO4), sạc đúng điện áp đầy, BMS nếu pack chưa có, buck, cầu chì 2 A và 3 A, khung nếu chưa có từ đợt motor. Không dùng sạc 4,20 V/cell cho LiFePO4. Không mắc TP4056 ngang pack 2S.

## Tuần 13 — xe nghe lệnh serial (6,5 giờ)

Bài: [07_02]({{ site.baseurl }}/contents/vi/chapter07/07_02_driver_bringup/), [07_03]({{ site.baseurl }}/contents/vi/chapter07/07_03_teleop_protocol/), [07_04]({{ site.baseurl }}/contents/vi/chapter07/07_04_teleop_firmware/). Khoảng 5 giờ bài, sổ 1,5 giờ: log một phiên teleop, bánh kê lên trước khi cho xuống sàn.

## Tuần 14 — nghiệm thu và toán khung (6,5 giờ)

Bài: [07_05]({{ site.baseurl }}/contents/vi/chapter07/07_05_field_acceptance/), [07_06]({{ site.baseurl }}/contents/vi/chapter07/07_06_ch07_lab_checklist/), [08_00]({{ site.baseurl }}/contents/vi/chapter08/08_00_math_for_tf/). Khoảng 5 giờ bài. Sổ 1,5 giờ: chạy lại bài NumPy quay rồi tịnh tiến, ghi một quaternion yaw 90°. Bài toán này đứng trước TF2 ở chương 09.

## Tuần 15 — PID (6,5 giờ)

Bài: [08_01]({{ site.baseurl }}/contents/vi/chapter08/08_01_serial_protocols/), [08_02]({{ site.baseurl }}/contents/vi/chapter08/08_02_wifi_mqtt/), [08_03]({{ site.baseurl }}/contents/vi/chapter08/08_03_pid_tuning/). Khoảng 4,75 giờ bài. Sổ 1,75 giờ: chạy mô phỏng bậc hai, đổi Kp, lưu ảnh bước nhảy đối chiếu bài. **Mua** đĩa và mạch encoder nếu motor TT chưa có xung; PID trên xe cần số đếm.

## Tuần 16 — từ xung tới tư thế (6,5 giờ)

Bài: [08_04]({{ site.baseurl }}/contents/vi/chapter08/08_04_diff_kinematics/), [08_05]({{ site.baseurl }}/contents/vi/chapter08/08_05_loop_timing/), [08_06]({{ site.baseurl }}/contents/vi/chapter08/08_06_ch08_lab_checklist/). Khoảng 4,25 giờ bài. Sổ 2 giờ: chạy `pose_from_counts`, so quỹ đạo với hình trong bài, ghi số đếm cho 1 m thẳng và cho quay tại chỗ π/2.

## Tuần 17 — máy trên xe và Jazzy (6,5 giờ)

Bài: [09_00]({{ site.baseurl }}/contents/vi/chapter09/09_00_linux_on_sbc/), [09_01]({{ site.baseurl }}/contents/vi/chapter09/09_01_jazzy_install_ws/). Khoảng 4 giờ bài. Sổ 2,5 giờ: SSH không màn hình, luật udev ra `/dev/esp32`, `ROS_DOMAIN_ID` giống nhau trên laptop và SBC, một unit systemd cho micro-ROS agent. **Mua** Raspberry Pi 5 và cài Ubuntu 24.04 (ảnh mới trên trang Ubuntu có thể là 26.04; đừng nhận mặc định đó), hoặc Jetson Orin Nano với JetPack 7 trên Ubuntu 24.04. JetPack 6 là Ubuntu 22.04: không `apt install ros-jazzy-*`. Chưa có SBC thì làm tuần này trên laptop Ubuntu 24.04 và đánh dấu hoãn. Mac: USB serial đi qua máy ảo Ubuntu; Docker Desktop trên Mac không đưa `/dev/ttyUSB` vào container. Viết node bằng rclpy hoặc rclcpp. rclgo chỉ là đọc thêm.

## Tuần 18 — graph ROS (8 giờ)

Bài: [09_02]({{ site.baseurl }}/contents/vi/chapter09/09_02_nodes_topics/), [09_03]({{ site.baseurl }}/contents/vi/chapter09/09_03_services_actions/), [09_04]({{ site.baseurl }}/contents/vi/chapter09/09_04_launch_params_qos/), [09_05]({{ site.baseurl }}/contents/vi/chapter09/09_05_tf2_frames/), [09_06]({{ site.baseurl }}/contents/vi/chapter09/09_06_urdf_basics/), [09_07]({{ site.baseurl }}/contents/vi/chapter09/09_07_ch09_lab_checklist/). Khoảng 7,75 giờ bài, sổ 0,25 giờ: một cây frame `base_link` → `base_laser` với số đo thật, chưa lấy số ví dụ của hãng. Tuần dày nhất lịch; nếu trượt, đẩy checklist sang đầu tuần 19 chứ đừng bỏ TF2.

## Tuần 19 — mô phỏng (6,5 giờ)

Bài: [10_01]({{ site.baseurl }}/contents/vi/chapter10/10_01_gazebo_harmonic/), [10_02]({{ site.baseurl }}/contents/vi/chapter10/10_02_urdf_sim_bringup/), [10_03]({{ site.baseurl }}/contents/vi/chapter10/10_03_microros_mcu/). Khoảng 4,5 giờ bài, sổ 2 giờ: tên topic sau khi spawn, và agent nói chuyện được với firmware. Gazebo Harmonic đi với Jazzy.

## Tuần 20 — cầu sang xe thật (6,5 giờ)

Bài: [10_04]({{ site.baseurl }}/contents/vi/chapter10/10_04_bridge_capstone/), [10_05]({{ site.baseurl }}/contents/vi/chapter10/10_05_sim_to_real/), [10_06]({{ site.baseurl }}/contents/vi/chapter10/10_06_ch10_lab_checklist/). Khoảng 4,5 giờ bài, sổ 2 giờ: bảng sim-to-real (khung, dấu encoder, `use_sim_time`). Checklist chương 10 là cổng đạt, bài 10_05 vẫn là danh sách đối chiếu.

## Tuần 21 — đọc tự hành (7 giờ)

Bài: [11_01]({{ site.baseurl }}/contents/vi/chapter11/11_01_slam_overview/), [11_02]({{ site.baseurl }}/contents/vi/chapter11/11_02_nav2_tour/), [11_03]({{ site.baseurl }}/contents/vi/chapter11/11_03_vision_pipeline/), [11_04]({{ site.baseurl }}/contents/vi/chapter11/11_04_bt_peek/), [11_05]({{ site.baseurl }}/contents/vi/chapter11/11_05_moveit_peek/). Khoảng 6,25 giờ bài, sổ 0,75 giờ: một đoạn bạn sẽ cấu hình ở tuần 22 (`map` → `odom` → `base_link`). Chưa cần lidar trên bàn.

## Tuần 22 — Capstone B (6,5 giờ)

Bài: [11_06]({{ site.baseurl }}/contents/vi/chapter11/11_06_capstone_b_slam/), [11_07]({{ site.baseurl }}/contents/vi/chapter11/11_07_capstone_b_nav2/), [11_08]({{ site.baseurl }}/contents/vi/chapter11/11_08_ch11_lab_checklist/). Khoảng 5 giờ bài, sổ 1,5 giờ: ảnh map mô phỏng, rồi `echo /cmd_vel` trước khi bánh chạm sàn. Làm TurtleBot3 waffle trong sim trước. **Mua** LD06 hoặc RPLIDAR A1 chỉ trước nửa xe thật. Không có lidar vẫn qua được phần sim và checklist nếu bạn ghi rõ phần thật còn thiếu.

## Tuần 23 — đọc robot learning (7 giờ)

Bài: [12_01]({{ site.baseurl }}/contents/vi/chapter12/12_01_lerobot_intro/), [12_02]({{ site.baseurl }}/contents/vi/chapter12/12_02_imitation_act/), [12_03]({{ site.baseurl }}/contents/vi/chapter12/12_03_diffusion_policy/), [12_04]({{ site.baseurl }}/contents/vi/chapter12/12_04_vla_overview/), [12_05]({{ site.baseurl }}/contents/vi/chapter12/12_05_next_paths_refs/). Khoảng 6,25 giờ bài, sổ 0,75 giờ: một câu phân biệt ACT, diffusion policy và VLA. Chưa train.

## Tuần 24 — tay hoặc đường giấy (6,5 giờ)

Bài: [12_06]({{ site.baseurl }}/contents/vi/chapter12/12_06_so101_arm_lab/), [12_07]({{ site.baseurl }}/contents/vi/chapter12/12_07_ch12_lab_checklist/). Khoảng 3 giờ bài. Sổ 3,5 giờ. Đường giấy (không mua tay): đọc dataset card, ghi vì sao ví dụ train trên trang LeRobot là ACT, và chỉ gọi `--policy.type=diffusion` khi chuỗi đó có trong gói bạn cài. Đường tay: **mua** follower SO-101 và leader nếu bạn teleoperate; làm từng động cơ, kẹp trước. Không điền giá GPU thuê.

Nếu một tuần trượt quá 8 giờ, dừng ở bài đang dở và ghi câu lệnh lỗi vào sổ. Tuần sau bắt đầu bằng câu đó, không bởi bài mới.
