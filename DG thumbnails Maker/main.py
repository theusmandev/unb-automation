
# v3
import os
from PIL import Image, ImageEnhance, ImageOps, ImageDraw, ImageFilter

# 📁 Folders
input_folder = r"C:\Users\PCS\Downloads\New folder"
output_folder = os.path.join(input_folder, 'canva_style_thumbnails')
os.makedirs(output_folder, exist_ok=True)

# 🎯 Canvas Settings
thumb_width, thumb_height = 1200, 800
bg_color = (248, 235, 215)  # Background cream color

# 🌑 Canva Shadow Settings
shadow_blur = 30      # Canva Blur amount: 30
shadow_intensity = 128# Canva Intensity 50% (255 ka half)
shadow_spread = 10   # Canva Size: 15

# 🔁 Process Images
counter = 1
for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
        img_path = os.path.join(input_folder, filename)
        
        try:
            # 1. Open Image
            raw_img = Image.open(img_path).convert("RGB")

            # 2. Cover Color Change (Image ko cream tint dena)
            # Hum image ko thora sepia/cream look den ge jesa sample me hai
            img = ImageOps.colorize(ImageOps.grayscale(raw_img), black="#3e2723", white="#f5e6cb")
            img = ImageEnhance.Contrast(img).enhance(1.1)

            # 3. Resize
            max_h = int(thumb_height * 0.82)
            img.thumbnail((thumb_width, max_h), Image.LANCZOS)
            img_w, img_h = img.size

            # 4. Create Shadow (Canva Style Backdrop)
            # Spread ki wajha se shadow image se thora bara hota hai
            shadow_w, shadow_h = img_w + (shadow_spread * 2), img_h + (shadow_spread * 2)
            shadow = Image.new("RGBA", (shadow_w, shadow_h), (0, 0, 0, 0))
            draw = ImageDraw.Draw(shadow)
            draw.rectangle([0, 0, shadow_w, shadow_h], fill=(0, 0, 0, shadow_intensity))
            shadow = shadow.filter(ImageFilter.GaussianBlur(shadow_blur))

            # 5. Composite Final Image
            final_thumb = Image.new("RGB", (thumb_width, thumb_height), bg_color)
            
            # Center positions
            x = (thumb_width - img_w) // 2
            y = (thumb_height - img_h) // 2
            
            # Paste Shadow (centered behind image)
            shadow_x = (thumb_width - shadow_w) // 2
            shadow_y = (thumb_height - shadow_h) // 2
            final_thumb.paste(shadow, (shadow_x, shadow_y), shadow)
            
            # Paste Image
            final_thumb.paste(img, (x, y))

            # 6. Save
            save_path = os.path.join(output_folder, f"www.urdunovelbanks.com({counter}).webp")
            final_thumb.save(save_path, "WEBP", quality=90)
            
            print(f"Done: {filename} -> {counter}")
            counter += 1

        except Exception as e:
            print(f"Error on {filename}: {e}")

print(f"\n✅ Done! Check folder: {output_folder}")

