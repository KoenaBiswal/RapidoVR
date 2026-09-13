import os
import math
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = r"C:\Users\PRAVEEN KUMAR\.gemini\antigravity\scratch\iitkgp_rapido"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_font(size, bold=False):
    # Try common Windows system fonts
    font_names = ["arialbd.ttf" if bold else "arial.ttf", "segoeuib.ttf" if bold else "segoeui.ttf", "calibrib.ttf" if bold else "calibri.ttf"]
    for name in font_names:
        try:
            return ImageFont.truetype(f"C:/Windows/Fonts/{name}", size)
        except Exception:
            continue
    return ImageFont.load_default()

def create_phone_screen():
    w, h = 1080, 2340
    img = Image.new("RGB", (w, h), (248, 249, 251))
    draw = ImageDraw.Draw(img)

    # Status Bar
    font_status = get_font(42, bold=True)
    draw.text((80, 50), "09:42", fill=(20, 20, 20), font=font_status)
    draw.text((w - 240, 50), "5G  100%", fill=(20, 20, 20), font=font_status)
    # Dynamic Island / notch
    draw.rounded_rectangle([w//2 - 120, 40, w//2 + 120, 95], radius=28, fill=(10, 10, 10))

    # App Header Bar
    font_app = get_font(60, bold=True)
    draw.rectangle([0, 120, w, 240], fill=(255, 255, 255))
    # Rapido logo badge
    draw.rounded_rectangle([60, 140, 310, 220], radius=20, fill=(255, 204, 0))
    draw.text((85, 150), "rapido", fill=(20, 20, 20), font=font_app)
    font_sub = get_font(36, bold=False)
    draw.text((340, 162), "IIT Kharagpur Campus", fill=(80, 80, 80), font=font_sub)
    draw.line([0, 240, w, 240], fill=(230, 230, 230), width=2)

    # Mini Map Section (Graphic representation)
    map_box = [60, 270, w - 60, 1020]
    draw.rounded_rectangle(map_box, radius=32, fill=(232, 238, 242), outline=(210, 215, 220), width=3)
    
    # Campus roads on map
    # Scholars' Avenue main road
    draw.line([(140, 920), (320, 780), (560, 620), (840, 400), (940, 340)], fill=(255, 255, 255), width=36)
    draw.line([(140, 920), (320, 780), (560, 620), (840, 400), (940, 340)], fill=(255, 190, 0), width=20)
    # Cross road
    draw.line([(240, 480), (750, 850)], fill=(255, 255, 255), width=24)
    draw.line([(400, 320), (450, 950)], fill=(255, 255, 255), width=20)
    
    # Parks / campus green patches
    draw.rounded_rectangle([180, 320, 380, 460], radius=16, fill=(195, 225, 200))
    draw.rounded_rectangle([620, 660, 920, 880], radius=16, fill=(195, 225, 200))
    font_map = get_font(28, bold=True)
    draw.text((200, 370), "Main Ground", fill=(100, 140, 105), font=font_map)
    draw.text((680, 740), "Gymkhana", fill=(100, 140, 105), font=font_map)

    # Pickup Pin (Main Building)
    p_x, p_y = 220, 860
    draw.ellipse([p_x - 24, p_y - 24, p_x + 24, p_y + 24], fill=(30, 180, 80), outline=(255, 255, 255), width=4)
    # Destination Pin (Nalanda)
    d_x, d_y = 860, 380
    draw.ellipse([d_x - 24, d_y - 24, d_x + 24, d_y + 24], fill=(230, 40, 40), outline=(255, 255, 255), width=4)

    # Captain bike moving icon on map
    b_x, b_y = 440, 700
    draw.ellipse([b_x - 30, b_y - 30, b_x + 30, b_y + 30], fill=(255, 204, 0), outline=(20, 20, 20), width=4)
    draw.text((b_x - 18, b_y - 20), "🏍", fill=(20, 20, 20), font=get_font(32))

    # Location labels
    font_loc = get_font(32, bold=True)
    draw.rounded_rectangle([p_x + 30, p_y - 30, p_x + 380, p_y + 20], radius=12, fill=(255, 255, 255), outline=(180, 180, 180), width=2)
    draw.text((p_x + 45, p_y - 24), "Pickup: Main Building", fill=(20, 20, 20), font=font_loc)

    draw.rounded_rectangle([d_x - 420, d_y - 30, d_x - 30, d_y + 20], radius=12, fill=(255, 255, 255), outline=(180, 180, 180), width=2)
    draw.text((d_x - 405, d_y - 24), "Drop: Nalanda Complex", fill=(20, 20, 20), font=font_loc)

    # Booking Confirmation Card
    card_top = 1060
    draw.rounded_rectangle([60, card_top, w - 60, card_top + 420], radius=28, fill=(255, 255, 255), outline=(220, 220, 225), width=3)

    # Captain details header
    draw.ellipse([100, card_top + 40, 200, card_top + 140], fill=(255, 204, 0))
    draw.text((120, card_top + 50), "👨‍✈️", font=get_font(60))
    
    font_head = get_font(44, bold=True)
    draw.text((220, card_top + 45), "Captain Ramesh Kumar", fill=(20, 20, 20), font=font_head)
    font_desc = get_font(34, bold=False)
    draw.text((220, card_top + 100), "Honda Shine  •  WB 22 KGP 2026", fill=(100, 100, 100), font=font_desc)
    
    # Rating & badge
    draw.rounded_rectangle([w - 240, card_top + 50, w - 100, card_top + 110], radius=16, fill=(240, 248, 240))
    font_rate = get_font(34, bold=True)
    draw.text((w - 220, card_top + 62), "★ 4.92", fill=(40, 140, 50), font=font_rate)

    draw.line([90, card_top + 170, w - 90, card_top + 170], fill=(240, 240, 240), width=2)

    # Ride details row
    draw.text((100, card_top + 200), "Arrival in 2 mins", fill=(220, 60, 20), font=get_font(40, bold=True))
    draw.text((100, card_top + 260), "Distance: 1.4 km  •  Via Scholars' Ave", fill=(100, 100, 100), font=get_font(32))

    # OTP Box
    draw.rounded_rectangle([w - 380, card_top + 200, w - 100, card_top + 310], radius=18, fill=(248, 248, 252), outline=(210, 210, 220), width=2)
    draw.text((w - 360, card_top + 215), "START OTP", fill=(120, 120, 120), font=get_font(24, bold=True))
    draw.text((w - 350, card_top + 245), "4892", fill=(20, 20, 20), font=get_font(52, bold=True))

    # Fare info
    draw.text((100, card_top + 340), "Total Campus Fare:", fill=(100, 100, 100), font=get_font(34))
    draw.text((420, card_top + 332), "₹25.00", fill=(20, 20, 20), font=get_font(44, bold=True))

    # Ride Status Alert Banner
    bar_top = card_top + 460
    draw.rounded_rectangle([60, bar_top, w - 60, bar_top + 140], radius=24, fill=(255, 247, 215), outline=(255, 204, 0), width=3)
    draw.text((100, bar_top + 30), "🛵 Captain has arrived at Main Building!", fill=(160, 110, 0), font=get_font(38, bold=True))
    draw.text((100, bar_top + 80), "Please collect your sanitized Rapido helmet", fill=(140, 110, 20), font=get_font(30))

    # Big Action Button
    btn_top = bar_top + 180
    draw.rounded_rectangle([60, btn_top, w - 60, btn_top + 130], radius=65, fill=(255, 204, 0))
    font_btn = get_font(46, bold=True)
    draw.text((w//2 - 250, btn_top + 38), "BOARDING VERIFIED", fill=(20, 20, 20), font=font_btn)

    # Home indicator bar
    draw.rounded_rectangle([w//2 - 180, h - 40, w//2 + 180, h - 25], radius=8, fill=(180, 180, 180))

    img.save(os.path.join(OUTPUT_DIR, "rapido_phone_screen.png"))
    print("Created rapido_phone_screen.png")

def create_clock_face():
    size = 1024
    img = Image.new("RGBA", (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    center = size // 2
    r = size // 2 - 30

    # Outer bezel
    draw.ellipse([center - r, center - r, center + r, center + r], fill=(250, 248, 242, 255), outline=(60, 45, 30, 255), width=24)
    # Inner ring
    r_inner = r - 40
    draw.ellipse([center - r_inner, center - r_inner, center + r_inner, center + r_inner], outline=(90, 70, 50, 255), width=8)

    # Minute tick marks
    for i in range(60):
        angle = math.radians(i * 6 - 90)
        is_hour = (i % 5 == 0)
        tick_len = 36 if is_hour else 16
        w_tick = 8 if is_hour else 4
        x1 = center + (r_inner - 10) * math.cos(angle)
        y1 = center + (r_inner - 10) * math.sin(angle)
        x2 = center + (r_inner - 10 - tick_len) * math.cos(angle)
        y2 = center + (r_inner - 10 - tick_len) * math.sin(angle)
        draw.line([(x1, y1), (x2, y2)], fill=(40, 30, 20, 255), width=w_tick)

    # Roman numerals
    romans = ["XII", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI"]
    font_roman = get_font(68, bold=True)
    for idx, text in enumerate(romans):
        angle = math.radians(idx * 30 - 90)
        num_r = r_inner - 100
        x = center + num_r * math.cos(angle)
        y = center + num_r * math.sin(angle)
        bbox = draw.textbbox((0, 0), text, font=font_roman)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        draw.text((x - tw//2, y - th//2 - 10), text, fill=(30, 20, 15, 255), font=font_roman)

    # Clock Hands (Set to 09:42 AM)
    # Hour hand: 9 hours + 42/60 = 9.7 -> 9.7 * 30 deg = 291 deg - 90 = 201 deg
    angle_h = math.radians(291 - 90)
    h_len = r_inner * 0.52
    hx = center + h_len * math.cos(angle_h)
    hy = center + h_len * math.sin(angle_h)
    draw.line([(center, center), (hx, hy)], fill=(20, 15, 10, 255), width=22)

    # Minute hand: 42 mins -> 42 * 6 deg = 252 deg - 90 = 162 deg
    angle_m = math.radians(252 - 90)
    m_len = r_inner * 0.78
    mx = center + m_len * math.cos(angle_m)
    my = center + m_len * math.sin(angle_m)
    draw.line([(center, center), (mx, my)], fill=(20, 15, 10, 255), width=14)

    # Center brass cap
    draw.ellipse([center - 28, center - 28, center + 28, center + 28], fill=(180, 140, 50, 255), outline=(40, 30, 20, 255), width=4)

    img.save(os.path.join(OUTPUT_DIR, "iitkgp_clock_face.png"))
    print("Created iitkgp_clock_face.png")

def create_road_sign():
    w, h = 1200, 600
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Green highway sign board
    draw.rounded_rectangle([15, 15, w - 15, h - 15], radius=32, fill=(18, 108, 62, 255), outline=(255, 255, 255, 255), width=14)

    # White inner border line
    draw.rounded_rectangle([35, 35, w - 35, h - 35], radius=22, outline=(255, 255, 255, 255), width=5)

    font_title = get_font(72, bold=True)
    draw.text((w//2 - 340, 65), "SCHOLARS' AVENUE", fill=(255, 255, 255, 255), font=font_title)

    draw.line([60, 160, w - 60, 160], fill=(255, 255, 255, 255), width=5)

    # Direction 1: Nalanda
    font_body = get_font(52, bold=True)
    draw.text((80, 200), "↑  NALANDA COMPLEX", fill=(255, 255, 255, 255), font=font_body)
    draw.text((w - 280, 205), "1.2 km", fill=(240, 240, 240, 255), font=get_font(44, bold=False))

    # Direction 2: Gymkhana / Hall of Residence
    draw.text((80, 290), "←  GYMKHANA / TSG", fill=(255, 255, 255, 255), font=font_body)
    draw.text((w - 280, 295), "0.5 km", fill=(240, 240, 240, 255), font=get_font(44, bold=False))

    # Direction 3: Main Building
    draw.text((80, 380), "↓  MAIN BUILDING", fill=(255, 255, 255, 255), font=font_body)
    draw.text((w - 280, 385), "0.2 km", fill=(240, 240, 240, 255), font=get_font(44, bold=False))

    # Footer
    draw.line([60, 470, w - 60, 470], fill=(255, 255, 255, 255), width=3)
    draw.text((w//2 - 200, 495), "IIT KHARAGPUR", fill=(255, 215, 0, 255), font=get_font(46, bold=True))

    img.save(os.path.join(OUTPUT_DIR, "campus_road_sign.png"))
    print("Created campus_road_sign.png")

def create_license_plate():
    w, h = 600, 180
    img = Image.new("RGB", (w, h), (255, 215, 0)) # Commercial Yellow
    draw = ImageDraw.Draw(img)

    # Black border
    draw.rounded_rectangle([6, 6, w - 6, h - 6], radius=14, outline=(15, 15, 15), width=10)

    # Blue IND strip on left
    draw.rounded_rectangle([16, 16, 80, h - 16], radius=8, fill=(0, 50, 160))
    draw.text((24, 30), "IND", fill=(255, 255, 255), font=get_font(26, bold=True))
    draw.ellipse([36, 80, 60, 104], fill=(255, 215, 0)) # Chakra dot

    # Number
    font_num = get_font(74, bold=True)
    draw.text((110, 45), "WB 22 KGP 2026", fill=(15, 15, 15), font=font_num)

    img.save(os.path.join(OUTPUT_DIR, "bike_license_plate.png"))
    print("Created bike_license_plate.png")

if __name__ == "__main__":
    create_phone_screen()
    create_clock_face()
    create_road_sign()
    create_license_plate()
