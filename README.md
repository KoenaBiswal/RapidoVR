# 🚖 Rapido IIT Kharagpur — Driver System & 3D Cinematic Animation

A comprehensive project featuring the **Rapido Driver Work System UI** and a **high-fidelity 3D cinematic animation** of the Rapido bike-taxi workflow across the Indian Institute of Technology (IIT) Kharagpur campus (from the iconic Main Heritage Building to Nalanda Academic Complex).

---

## 👥 Contributors

| Roll Number | Name |
| :--- | :--- |
| **23MF3IM07** | Praveen Kumar |
| **23MF3IM08** | Stanley Jones |
| **23MF3IM09** | Kavya Nagar |
| **23MF3IM10** | Khushi Pakhre |
| **23MF3IM11** | Koena Biswal |

---

## 📱 1. Rapido Driver UI (`rapido_driver_ui.html`)
Created by **Khushi Pakhre**, this interactive web application models the complete workflow and decision states of a Rapido Captain:
- **Offline / Online State Toggle**: Duty status management.
- **Ride Request Card**: Pickup (IIT KGP Main Building), drop-off (Nalanda Complex), estimated fare, distance, and acceptance timer.
- **Navigation & En Route View**: Turn-by-turn routing along Scholars Avenue with real-time speed and status updates.
- **OTP Verification & Ride Start**: Secure customer boarding protocol.
- **Ride Completion & Payment**: Fare summary, digital payment settlement, and rating.

To test the UI, open `rapido_driver_ui.html` in any modern web browser.

---

## 🎬 2. 3D Cinematic Animation (`iitkgp_rapido_animation.mp4`)
A complete 75-second (1,800 frames @ 24 fps) cinematic animation rendered in HD:
- **Route**: IIT Kharagpur Main Heritage Building → Scholars Avenue → Hijli Detention Camp intersection → Nalanda Academic Complex.
- **Workflow Journey**:
  1. Student books a ride on mobile at Main Building.
  2. Rapido Captain arrives on commercial bike (yellow helmet, reflective jacket, luggage box).
  3. Student verifies OTP, dons yellow passenger helmet, and boards the pillion.
  4. Dynamic multi-angle riding sequence along tree-lined Scholars Avenue.
  5. Smooth deceleration and arrival at Nalanda Complex portico.
  6. Passenger alights, helmet returned, payment completed.

### Cinematic Camera Sequence (10 Shots)
| Shot | Frame Range | Camera & Shot Type | Description |
| :---: | :---: | :---: | :--- |
| **01** | `1 - 150` | `Cam_01_Establishing` (28mm) | Grand aerial pan of IIT KGP Main Building clock tower & portico. |
| **02** | `151 - 300` | `Cam_02_PhoneBooking` (85mm) | Over-the-shoulder macro close-up of student booking Rapido ride. |
| **03** | `301 - 480` | `Cam_03_CaptainArrival` (50mm) | Dynamic low-angle tracking shot of Captain arriving and braking. |
| **04** | `481 - 660` | `Cam_04_PassengerMount` (42mm) | Medium profile of student boarding pillion with safety helmet. |
| **05** | `661 - 840` | `Cam_05_LowSpeedPursuit` (35mm) | Low asphalt pursuit tracking wheels accelerating down the boulevard. |
| **06** | `841 - 1050` | `Cam_06_CanopyChase` (24mm) | High crane tracking under lush green campus tree canopy. |
| **07** | `1051 - 1260` | `Cam_07_CockpitPOV` (20mm) | First-person handlebar POV showing speedometer, mirrors, and road. |
| **08** | `1261 - 1440` | `Cam_08_NalandaDrone` (32mm) | Expansive drone establishing shot of circular Nalanda Complex. |
| **09** | `1441 - 1620` | `Cam_09_NalandaArrival` (50mm) | Ground tracking of bike pulling up smoothly to Nalanda drop-off. |
| **10** | `1621 - 1800` | `Cam_10_HeroOutro` (35mm) | Passenger alighting, fare settled, hero camera pull-back outro. |

---

## 🛠️ 3. Pipeline & Generation Scripts

- **`build_masterpiece_animation.py`**: Full procedural Python script to build the entire 3D scene in Blender (geometry, rigs, materials, cameras, timeline markers).
- **`generate_highres_textures.py`**: Procedural generation script for all 2D high-res textures.
- **`render_full_video.py`**: Headless batch rendering script for the full 1,800-frame video.
- **`render_all_shots_stills.py`**: Automated verification still generator across all 10 cameras.

---

## 🎨 4. Textures & Visual Assets

- `rapido_phone_screen.png`: High-resolution booking UI screen texture.
- `iitkgp_clock_face.png`: Heritage clock face for the Main Building tower.
- `campus_road_sign.png`: Campus directional wayfinding sign.
- `bike_license_plate.png`: West Bengal commercial registration plate.
- `shot01_establishing.png` — `shot10_hero_outro.png`: 10 showcase stills representing each camera cut.