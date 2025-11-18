


import os
import math
from PIL import Image, ImageEnhance, ImageStat, ImageDraw, ImageFilter

# 📁 Input & Output 
input_folder = r"E:\SUNB\sumaira hameed novels\pngs"
output_folder = os.path.join(input_folder, 'thumbnails_1000x667')
os.makedirs(output_folder, exist_ok=True)

# 🧹 Clean output folder: delete all files except .webp
for f in os.listdir(output_folder):
    if not f.lower().endswith('.webp'):
        os.remove(os.path.join(output_folder, f))

# 🎯 Canvas size
thumb_width = 1000
thumb_height = 667
thumb_size = (thumb_width, thumb_height)

# 🌑 Drop shadow settings (Canva-style)
angle_degrees = 37
distance = 30
blur_radius = 20
opacity = 128  # 50% opacity
shadow_color = (0, 0, 0, opacity)  # Black with alpha

# ➕➖ Shadow offset based on angle
angle_radians = math.radians(angle_degrees)
x_offset = -int(distance * math.cos(angle_radians))   # Left
y_offset = int(distance * math.sin(angle_radians))    # Down

# 🔁 Process all images
counter = 1
for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
        img_path = os.path.join(input_folder, filename)
        img = Image.open(img_path).convert("RGB")

        # 🎨 Enhance image
        img = ImageEnhance.Color(img).enhance(1.3)
        img = ImageEnhance.Brightness(img).enhance(1.1)
        img = ImageEnhance.Contrast(img).enhance(1.2)

        # 🎯 Get average background color
        stat = ImageStat.Stat(img)
        avg_color = tuple(int(c) for c in stat.mean[:3])
        background = Image.new("RGB", thumb_size, avg_color)

        # 🔧 Resize image to fit in thumbnail
        max_cover_width = int(thumb_width * 0.5)
        max_cover_height = int(thumb_height * 0.9)
        img.thumbnail((max_cover_width, max_cover_height), Image.LANCZOS)

        # 🎯 Center position
        x = (thumb_width - img.width) // 2
        y = (thumb_height - img.height) // 2

        # ☁️ Create drop shadow
        shadow = Image.new("RGBA", img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(shadow)
        draw.rectangle([0, 0, img.width, img.height], fill=shadow_color)
        shadow = shadow.filter(ImageFilter.GaussianBlur(blur_radius))

        # 🖼 Create final composite image
        composite = background.convert("RGBA")
        composite.paste(shadow, (x + x_offset, y + y_offset), shadow)
        composite.paste(img, (x, y))

        # 💾 Save as .webp with custom name
        final_image = composite.convert("RGB")
        custom_name = f"www.urdunovelbanks.com({counter}).webp"
        output_path = os.path.join(output_folder, custom_name)
        final_image.save(output_path, format="WEBP", optimize=True, quality=85)

        counter += 1

print("✔️ Sirf WEBP thumbnails successfully generate ho chuki hain:", output_folder)

