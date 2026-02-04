
import os
import math
from PIL import Image, ImageEnhance, ImageStat, ImageDraw, ImageFilter, ImageFont

# Input & Output folders
input_folder = r"C:\Users\PCS\Downloads\2"
output_folder = os.path.join(input_folder, 'thumbnails_1000x667')
os.makedirs(output_folder, exist_ok=True)

# Clean output folder (except existing .webp files)
for f in os.listdir(output_folder):
    file_path = os.path.join(output_folder, f)
    if os.path.isfile(file_path) and not f.lower().endswith('.webp'):
        os.remove(file_path)

# Canvas size
thumb_width = 1200
thumb_height = 800
thumb_size = (thumb_width, thumb_height)

# Drop shadow settings
angle_degrees = 37
distance = 30
blur_radius = 20
opacity = 128
shadow_color = (0, 0, 0, opacity)
angle_radians = math.radians(angle_degrees)
x_offset = -int(distance * math.cos(angle_radians))
y_offset = int(distance * math.sin(angle_radians))

# Watermark Settings
watermark_text = "www.urdunovelbanks.com"
font_path = r"E:\unb-workstation\Writers All Novels\RobotoCondensed-BoldItalic.ttf"

try:
    font = ImageFont.truetype(font_path, 30)
except IOError:
    print("Font nahi mila! Default font use kar raha hun.")
    font = ImageFont.load_default()

# Auto best color for text (Black or White)
def get_best_text_color(bg_color):
    r, g, b = bg_color
    luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    return (0, 0, 0, 255) if luminance > 0.5 else (255, 255, 255, 255)

# Create vertical watermark (bottom → top)
def create_vertical_watermark_bottom_to_top(bg_color):
    text_color = get_best_text_color(bg_color)
    
    temp = Image.new("RGBA", (200, 200))
    d = ImageDraw.Draw(temp)
    try:
        bbox = d.textbbox((0, 0), watermark_text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
    except AttributeError:
        # fallback for older PIL versions
        text_w, text_h = font.getsize(watermark_text)

    padding = 30
    text_img = Image.new("RGBA", (text_w + padding, text_h + padding), (0, 0, 0, 0))
    draw = ImageDraw.Draw(text_img)
    draw.text((padding//2, padding//2), watermark_text, font=font, fill=text_color)
    
    # Rotate 90° counterclockwise → bottom to top
    return text_img.rotate(90, expand=True)

# ────────────────────────────────────────────────
#              Main Processing Loop
# ────────────────────────────────────────────────

counter = 0
for filename in os.listdir(input_folder):
    if not filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
        continue
        
    img_path = os.path.join(input_folder, filename)
    try:
        img = Image.open(img_path).convert("RGB")
    except Exception:
        print(f"Skip: {filename} (open error)")
        continue

    counter += 1

    # Enhance
    img = ImageEnhance.Color(img).enhance(1.3)
    img = ImageEnhance.Brightness(img).enhance(1.1)
    img = ImageEnhance.Contrast(img).enhance(1.25)

    # Average color background
    stat = ImageStat.Stat(img)
    avg_color = tuple(int(c) for c in stat.mean[:3])
    background = Image.new("RGB", thumb_size, avg_color)

    # Resize cover
    max_cover_width = int(thumb_width * 0.5)
    max_cover_height = int(thumb_height * 0.9)
    img.thumbnail((max_cover_width, max_cover_height), Image.LANCZOS)

    # Center position
    x = (thumb_width - img.width) // 2
    y = (thumb_height - img.height) // 2

    # Shadow
    shadow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw_shadow = ImageDraw.Draw(shadow)
    draw_shadow.rectangle([0, 0, img.width, img.height], fill=shadow_color)
    shadow = shadow.filter(ImageFilter.GaussianBlur(blur_radius))

    # Composite layers
    composite = background.convert("RGBA")
    composite.paste(shadow, (x + x_offset, y + y_offset), shadow)
    composite.paste(img.convert("RGBA"), (x, y), img.convert("RGBA"))

    # Vertical watermark
    watermark = create_vertical_watermark_bottom_to_top(avg_color)
    margin = 18
    wm_x = x + img.width + margin
    wm_y = y + (img.height - watermark.height) // 2

    # Keep inside canvas
    if wm_x + watermark.width > thumb_width:
        wm_x = thumb_width - watermark.width - 12

    composite.alpha_composite(watermark, (wm_x, wm_y))

    # ───── Save with ORIGINAL filename + suffix ─────
    final_image = composite.convert("RGB")
    
    base_name = os.path.splitext(filename)[0]
    output_filename = f"{base_name}_(www.urdunovelbanks.com).webp"
    output_path = os.path.join(output_folder, output_filename)
    
    final_image.save(output_path, format="WEBP", optimize=True, quality=88)

    print(f"Generated: {output_filename}")

print(f"\nDone! Total {counter} thumbnails ban gaye")
print(f"Output folder: {output_folder}")

# import os
# import math
# from PIL import Image, ImageEnhance, ImageStat, ImageDraw, ImageFilter, ImageFont

# # Input & Output folders
# input_folder = r"E:\unb-workstation\Writers All Novels\humyon ayoub novels_GD_only\pngs"
# output_folder = os.path.join(input_folder, 'thumbnails_1000x667')
# os.makedirs(output_folder, exist_ok=True)

# # Clean output folder (except .webp)
# for f in os.listdir(output_folder):
#     file_path = os.path.join(output_folder, f)
#     if os.path.isfile(file_path) and not f.lower().endswith('.webp'):
#         os.remove(file_path)

# # Canvas size
# thumb_width = 1200
# thumb_height = 800
# thumb_size = (thumb_width, thumb_height)

# # Drop shadow
# angle_degrees = 37
# distance = 30
# blur_radius = 20
# opacity = 128
# shadow_color = (0, 0, 0, opacity)
# angle_radians = math.radians(angle_degrees)
# x_offset = -int(distance * math.cos(angle_radians))
# y_offset = int(distance * math.sin(angle_radians))

# # Watermark Settings
# watermark_text = "www.urdunovelbanks.com"
# font_path = r"E:\unb-workstation\Writers All Novels\RobotoCondensed-BoldItalic.ttf"

# try:
#     font = ImageFont.truetype(font_path, 26)
# except IOError:
#     print("Agbalumo font nahi mila! Default use kar raha hun.")
#     font = ImageFont.load_default()

# # Auto best color (Black or White)
# def get_best_text_color(bg_color):
#     r, g, b = bg_color
#     luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
#     return (0, 0, 0, 255) if luminance > 0.5 else (255, 255, 255, 255)

# # Watermark: Bottom-to-Top (90° rotate)
# def create_vertical_watermark_bottom_to_top(bg_color):
#     text_color = get_best_text_color(bg_color)
    
#     temp = Image.new("RGBA", (200, 200))
#     d = ImageDraw.Draw(temp)
#     try:
#         bbox = d.textbbox((0, 0), watermark_text, font=font)
#         text_w = bbox[2] - bbox[0]
#         text_h = bbox[3] - bbox[1]
#     except:
#         text_w, text_h = font.getsize(watermark_text)

#     padding = 30
#     text_img = Image.new("RGBA", (text_w + padding, text_h + padding), (0, 0, 0, 0))
#     draw = ImageDraw.Draw(text_img)
#     draw.text((padding//2, padding//2), watermark_text, font=font, fill=text_color)
    
#     # یہی تبدیلی ہے → 90° (نیچے سے اوپر)
#     return text_img.rotate(90, expand=True)

# # Process images
# counter = 1
# for filename in os.listdir(input_folder):
#     if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
#         img_path = os.path.join(input_folder, filename)
#         try:
#             img = Image.open(img_path).convert("RGB")
#         except:
#             continue

#         # Enhance
#         img = ImageEnhance.Color(img).enhance(1.3)
#         img = ImageEnhance.Brightness(img).enhance(1.1)
#         img = ImageEnhance.Contrast(img).enhance(1.25)

#         # Average color background
#         stat = ImageStat.Stat(img)
#         avg_color = tuple(int(c) for c in stat.mean[:3])
#         background = Image.new("RGB", thumb_size, avg_color)

#         # Resize cover
#         max_cover_width = int(thumb_width * 0.5)
#         max_cover_height = int(thumb_height * 0.9)
#         img.thumbnail((max_cover_width, max_cover_height), Image.LANCZOS)

#         # Center position
#         x = (thumb_width - img.width) // 2
#         y = (thumb_height - img.height) // 2

#         # Shadow
#         shadow = Image.new("RGBA", img.size, (0, 0, 0, 0))
#         draw_shadow = ImageDraw.Draw(shadow)
#         draw_shadow.rectangle([0, 0, img.width, img.height], fill=shadow_color)
#         shadow = shadow.filter(ImageFilter.GaussianBlur(blur_radius))

#         # Composite
#         composite = background.convert("RGBA")
#         composite.paste(shadow, (x + x_offset, y + y_offset), shadow)
#         composite.paste(img.convert("RGBA"), (x, y), img.convert("RGBA"))

#         # Watermark (نیچے سے اوپر)
#         watermark = create_vertical_watermark_bottom_to_top(avg_color)
#         margin = 18
#         wm_x = x + img.width + margin
#         wm_y = y + (img.height - watermark.height) // 2

#         # Safety bounds
#         if wm_x + watermark.width > thumb_width:
#             wm_x = thumb_width - watermark.width - 12

#         composite.alpha_composite(watermark, (wm_x, wm_y))

#         # Save
#         final_image = composite.convert("RGB")
#         custom_name = f"www.urdunovelbanks.com({counter}).webp"
#         output_path = os.path.join(output_folder, custom_name)
#         final_image.save(output_path, format="WEBP", optimize=True, quality=88)

#         print(f"Generated: {custom_name}")
#         counter += 1

# print(f"\nDone! Total {counter-1} thumbnails ban gaye (watermark neechay se ooper)")
# print(f"Folder: {output_folder}")






# import os
# import math
# from PIL import Image, ImageEnhance, ImageStat, ImageDraw, ImageFilter, ImageFont

# # 📁 Input & Output folders
# input_folder = r"E:\unb-workstation\Writers All Novels\Perveen shakir books - Copy\pngs - Copy"
# output_folder = os.path.join(input_folder, 'thumbnails_1000x667')
# os.makedirs(output_folder, exist_ok=True)

# # 🧹 Clean output folder (sirf .webp chhod kar baaki delete)
# for f in os.listdir(output_folder):
#     file_path = os.path.join(output_folder, f)
#     if os.path.isfile(file_path) and not f.lower().endswith('.webp'):
#         os.remove(file_path)

# # 🎯 Canvas size
# thumb_width = 1000
# thumb_height = 667
# thumb_size = (thumb_width, thumb_height)

# # 🌑 Drop shadow settings
# angle_degrees = 37
# distance = 30
# blur_radius = 20
# opacity = 128
# shadow_color = (0, 0, 0, opacity)
# angle_radians = math.radians(angle_degrees)
# x_offset = -int(distance * math.cos(angle_radians))
# y_offset = int(distance * math.sin(angle_radians))

# # 🖋️ Watermark Settings
# watermark_text = "www.urdunovelbanks.com"
# font_path = r"E:\unb-workstation\Writers All Novels\Agbalumo-Regular.ttf"

# try:
#     font = ImageFont.truetype(font_path, 26)  # تھوڑا بڑا کیا خوبصورت لگے
# except IOError:
#     print("⚠️ Agbalumo font nahi mila! Default font use ho raha hai.")
#     font = ImageFont.load_default()

# # ✨ Auto-detect best text color (Black or White)
# def get_best_text_color(bg_color):
#     r, g, b = bg_color
#     luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
#     return (0, 0, 0, 255) if luminance > 0.5 else (255, 255, 255, 255)

# # ✍️ Create smart vertical watermark
# def create_vertical_watermark(bg_color):
#     text_color = get_best_text_color(bg_color)
    
#     # Text size calculate karo
#     temp = Image.new("RGBA", (200, 200))
#     d = ImageDraw.Draw(temp)
#     try:
#         bbox = d.textbbox((0, 0), watermark_text, font=font)
#         text_w = bbox[2] - bbox[0]
#         text_h = bbox[3] - bbox[1]
#     except AttributeError:
#         text_w, text_h = font.getsize(watermark_text)

#     padding = 30
#     text_img = Image.new("RGBA", (text_w + padding, text_h + padding), (0, 0, 0, 0))
#     draw = ImageDraw.Draw(text_img)
#     draw.text((padding//2, padding//2), watermark_text, font=font, fill=text_color)
    
#     return text_img.rotate(270, expand=True)

# # 🔁 Process all images
# counter = 1
# for filename in os.listdir(input_folder):
#     if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
#         img_path = os.path.join(input_folder, filename)
#         try:
#             img = Image.open(img_path).convert("RGB")
#         except Exception as e:
#             print(f"❌ Error opening {filename}: {e}")
#             continue

#         # 🎨 Enhance image
#         img = ImageEnhance.Color(img).enhance(1.3)
#         img = ImageEnhance.Brightness(img).enhance(1.1)
#         img = ImageEnhance.Contrast(img).enhance(1.25)

#         # 🎯 Average color background
#         stat = ImageStat.Stat(img)
#         avg_color = tuple(int(c) for c in stat.mean[:3])
#         background = Image.new("RGB", thumb_size, avg_color)

#         # 🔧 Resize cover
#         max_cover_width = int(thumb_width * 0.5)
#         max_cover_height = int(thumb_height * 0.9)
#         img.thumbnail((max_cover_width, max_cover_height), Image.LANCZOS)

#         # 🎯 Center position
#         x = (thumb_width - img.width) // 2
#         y = (thumb_height - img.height) // 2

#         # ☁️ Drop shadow
#         shadow = Image.new("RGBA", img.size, (0, 0, 0, 0))
#         draw_shadow = ImageDraw.Draw(shadow)
#         draw_shadow.rectangle([0, 0, img.width, img.height], fill=shadow_color)
#         shadow = shadow.filter(ImageFilter.GaussianBlur(blur_radius))

#         # 🖼 Composite
#         composite = background.convert("RGBA")
#         composite.paste(shadow, (x + x_offset, y + y_offset), shadow)
#         composite.paste(img.convert("RGBA"), (x, y), img.convert("RGBA"))

#         # ✍️ Smart Watermark (auto black/white)
#         watermark = create_vertical_watermark(avg_color)
#         margin_from_cover = 18
#         wm_x = x + img.width + margin_from_cover
#         wm_y = y + (img.height - watermark.height) // 2

#         # Bounds safety
#         if wm_x + watermark.width > thumb_width:
#             wm_x = thumb_width - watermark.width - 12
#         if wm_y < 0:
#             wm_y = 10
#         if wm_y + watermark.height > thumb_height:
#             wm_y = thumb_height - watermark.height - 10

#         composite.alpha_composite(watermark, (wm_x, wm_y))

#         # 💾 Save
#         final_image = composite.convert("RGB")
#         custom_name = f"www.urdunovelbanks.com({counter}).webp"
#         output_path = os.path.join(output_folder, custom_name)
#         final_image.save(output_path, format="WEBP", optimize=True, quality=88)

#         print(f"Generated: {custom_name} | Background: {avg_color} | Watermark: {'White' if avg_color[0]+avg_color[1]+avg_color[2]<382 else 'Black'}")
#         counter += 1

# print(f"\nAll Done! Total {counter-1} professional thumbnails ban gaye hain!")
# print(f"Folder: {output_folder}")




