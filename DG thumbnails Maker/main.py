#v2
import os
import math
from PIL import Image, ImageEnhance, ImageStat, ImageDraw, ImageFilter

# 📁 Input & Output folders
input_folder = r"C:\Users\PCS\Downloads\New folder"
output_folder = os.path.join(input_folder, 'thumbnails_final_v2')
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

# 🎨 Target Background Color (Light Beige/Cream, like reference image 2)
bg_color = (250, 240, 230)

# 🌑 Soft Drop Shadow settings
blur_radius = 30
shadow_opacity = 100 # 0-255
shadow_offset = (10, 10) # Slight offset to the bottom-right

# 🔁 Process all images
counter = 1
for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
        img_path = os.path.join(input_folder, filename)
        
        try:
            # Open and Convert
            img = Image.open(img_path).convert("RGBA")

            # 🔧 Resize image to fit well within the canvas
            max_h = int(thumb_height * 0.85)
            max_w = int(thumb_width * 0.85)
            img.thumbnail((max_w, max_h), Image.LANCZOS)

            # 🎯 Center position for the image
            img_x = (thumb_width - img.width) // 2
            img_y = (thumb_height - img.height) // 2

            # ☁️ Create soft drop shadow
            # Create a larger canvas for blur
            shadow_canvas = Image.new("RGBA", (thumb_width + blur_radius*2, thumb_height + blur_radius*2), (0, 0, 0, 0))
            shadow_draw = ImageDraw.Draw(shadow_canvas)
            # Draw the shadow rectangle
            shadow_draw.rectangle(
                [img_x + shadow_offset[0], img_y + shadow_offset[1], img_x + img.width + shadow_offset[0], img_y + img.height + shadow_offset[1]],
                fill=(0, 0, 0, shadow_opacity)
            )
            # Apply blur
            shadow_canvas = shadow_canvas.filter(ImageFilter.GaussianBlur(blur_radius))
            # Crop shadow back to thumbnail size
            shadow_final = shadow_canvas.crop((0, 0, thumb_width, thumb_height))

            # 🖼 Create final composite image
            final_thumb = Image.new("RGB", thumb_size, bg_color)
            
            # Paste Shadow first
            final_thumb.paste(shadow_final, (0, 0), shadow_final)
            
            # Paste Main Image on top
            final_thumb.paste(img, (img_x, img_y), img)

            # 💾 Save as .webp
            custom_name = f"www.urdunovelbanks.com({counter}).webp"
            output_path = os.path.join(output_folder, custom_name)
            final_thumb.save(output_path, format="WEBP", optimize=True, quality=90)

            print(f"Generated: {custom_name}")
            counter += 1

        except Exception as e:
            print(f"Error processing {filename}: {e}")

print(f"\n✔️ Tamam thumbnails '{output_folder}' mein target design ke mutabiq generate ho chuki hain.")
