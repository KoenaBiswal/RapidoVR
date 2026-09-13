import bpy
import os
import time
import shutil

project_dir = r"C:\Users\PRAVEEN KUMAR\.gemini\antigravity\scratch\iitkgp_rapido"
artifact_dir = r"C:\Users\PRAVEEN KUMAR\.gemini\antigravity\brain\937562a5-2f15-41af-afda-4febfe10fc4f"

blend_path = os.path.join(project_dir, "iitkgp_rapido_animation.blend")
bpy.ops.wm.open_mainfile(filepath=blend_path)

scene = bpy.context.scene
scene.render.resolution_x = 1280
scene.render.resolution_y = 720
scene.render.resolution_percentage = 100

# Configure FFmpeg H.264 MP4 export
scene.render.image_settings.file_format = 'FFMPEG'
scene.render.ffmpeg.format = 'MPEG4'
scene.render.ffmpeg.codec = 'H264'
scene.render.ffmpeg.constant_rate_factor = 'HIGH'
scene.render.ffmpeg.ffmpeg_preset = 'REALTIME'

# Set full 1800-frame timeline (75.0 seconds at 24 FPS)
scene.frame_start = 1
scene.frame_end = 1800

video_output_path = os.path.join(project_dir, "iitkgp_rapido_animation.mp4")
scene.render.filepath = video_output_path

print(f"Starting full animation video render (1800 frames at 720p 24fps)...")
t0 = time.time()
bpy.ops.render.render(animation=True)
t1 = time.time()
elapsed = t1 - t0
print(f"Successfully finished rendering full animation in {elapsed:.1f}s ({1800/elapsed:.2f} fps)!")
print(f"Output saved to: {video_output_path}")

# Copy video to artifact directory
dest_video = os.path.join(artifact_dir, "iitkgp_rapido_animation.mp4")
shutil.copy2(video_output_path, dest_video)
print(f"Copied video to artifact directory: {dest_video}")

# Copy all key shot stills to artifact directory
stills = [
    "shot01_establishing.png",
    "shot02_booking_ui.png",
    "shot03_captain_arrival.png",
    "shot04_boarding.png",
    "shot05_low_pursuit.png",
    "shot06_canopy_chase.png",
    "shot07_cockpit_pov.png",
    "shot08_nalanda_drone.png",
    "shot09_nalanda_arrival.png",
    "shot10_hero_outro.png",
]
for s in stills:
    src_still = os.path.join(project_dir, s)
    if os.path.exists(src_still):
        dest_still = os.path.join(artifact_dir, s)
        shutil.copy2(src_still, dest_still)
        print(f"Copied {s} -> {dest_still}")

print("SUCCESSFULLY COPIED ALL ASSETS TO ARTIFACT DIRECTORY!")
