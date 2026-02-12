# v1

import os
import math
from PIL import Image, ImageEnhance, ImageStat, ImageDraw, ImageFilter

# 📁 Input & Output folders
input_folder = r"C:\Users\PCS\Downloads\New folder"
output_folder = os.path.join(input_folder, 'thumbnails_final')
os.makedirs(output_folder, exist_ok=True)

# 🧹 Clean output folder: delete all files except .webp
for f in os.listdir(output_folder):
    if not f.lower().endswith('.webp'):
        try:
            os.remove(os.path.join(output_folder, f))
        except:
            pass

# 🎯 Canvas size (Landscape)
thumb_width = 1200
thumb_height = 800
thumb_size = (thumb_width, thumb_height)

# 🎨 Target Background Color (دوسری تصویر جیسا کریم رنگ)
bg_color = (245, 230, 205) # Specific Beige Color

# 🌑 Drop shadow settings
blur_radius = 25
opacity = 90  # Soft shadow
shadow_color = (0, 0, 0, opacity)
offset = (15, 15) # Shadow slightly to the bottom-right

# 🔁 Process all images
counter = 1
for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
        img_path = os.path.join(input_folder, filename)
        
        # Open and Convert
        img = Image.open(img_path).convert("RGBA")

        # 🎨 Enhance image (Thora contrast aur brightness behtar karne k liye)
        enhancer = ImageEnhance.Contrast(img.convert("RGB"))
        img = enhancer.enhance(1.1).convert("RGBA")

        # 🔧 Resize image to fit (Vertical style like the sample)
        # Hum image ko canvas ki height ka 85% tak rakhen gey
        max_h = int(thumb_height * 0.85)
        img.thumbnail((thumb_width, max_h), Image.LANCZOS)

        # 🎯 Center position
        x = (thumb_width - img.width) // 2
        y = (thumb_height - img.height) // 2

        # ☁️ Create drop shadow
        # Shadow canvas image se thora bara hona chahiye blur k liye
        shadow_canvas = Image.new("RGBA", (img.width + blur_radius * 2, img.height + blur_radius * 2), (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow_canvas)
        shadow_draw.rectangle([blur_radius, blur_radius, img.width + blur_radius, img.height + blur_radius], fill=shadow_color)
        shadow_canvas = shadow_canvas.filter(ImageFilter.GaussianBlur(blur_radius))

        # 🖼 Create final composite image
        final_thumb = Image.new("RGB", thumb_size, bg_color)
        
        # Paste Shadow
        final_thumb.paste(shadow_canvas, (x + offset[0] - blur_radius, y + offset[1] - blur_radius), shadow_canvas)
        
        # Paste Main Image
        final_thumb.paste(img, (x, y), img)

        # 💾 Save as .webp
        custom_name = f"www.urdunovelbanks.com({counter}).webp"
        output_path = os.path.join(output_folder, custom_name)
        final_thumb.save(output_path, format="WEBP", optimize=True, quality=90)

        print(f"Generated: {custom_name}")
        counter += 1

print("\n✔️ Mubarak ho! Tamam thumbnails target design k mutabiq generate ho chuki hain.")