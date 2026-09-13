import bpy
import os

BLEND_FILE = r"C:\Users\PRAVEEN KUMAR\.gemini\antigravity\scratch\iitkgp_rapido\iitkgp_rapido_animation.blend"
OUTPUT_DIR = r"C:\Users\PRAVEEN KUMAR\.gemini\antigravity\scratch\iitkgp_rapido"

bpy.ops.wm.open_mainfile(filepath=BLEND_FILE)
scene = bpy.context.scene

shots = [
    ("shot01_establishing", 90, "CAM_01_Establishing"),
    ("shot02_booking_ui", 250, "CAM_02_BookingUI"),
    ("shot03_captain_arrival", 400, "CAM_03_CaptainArrival"),
    ("shot04_boarding", 550, "CAM_04_Boarding"),
    ("shot05_low_pursuit", 720, "CAM_05_LowPursuit"),
    ("shot06_canopy_chase", 960, "CAM_06_CanopyChase"),
    ("shot07_cockpit_pov", 1180, "CAM_07_CockpitPOV"),
    ("shot08_nalanda_drone", 1380, "CAM_08_NalandaDrone"),
    ("shot09_nalanda_arrival", 1560, "CAM_09_CanopyArrival"),
    ("shot10_hero_outro", 1720, "CAM_10_HeroOutro"),
]

for name, frame, cam_name in shots:
    scene.frame_set(frame)
    cam = bpy.data.objects.get(cam_name)
    if cam:
        scene.camera = cam
    out_path = os.path.join(OUTPUT_DIR, f"{name}.png")
    scene.render.filepath = out_path
    bpy.ops.render.render(write_still=True)
    print(f"Rendered {name} at frame {frame} -> {out_path}")

print("ALL 10 SHOTS RENDERED SUCCESSFULLY!")
