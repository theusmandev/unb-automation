# import os
# import math
# from PIL import Image, ImageEnhance, ImageDraw, ImageFilter, ImageFont

# # 📁 Input & Output folders
# input_folder = r"E:\SUNB\Writers All Novels\Rabia khan Novels\pngs"
# output_folder = os.path.join(input_folder, 'thumbnails_1000x667')
# texture_folder = r"E:\SUNB\urdu afsana bank\texture"
# os.makedirs(output_folder, exist_ok=True)

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

# # 📂 Load texture backgrounds
# texture_files = [os.path.join(texture_folder, f) for f in os.listdir(texture_folder)
#                  if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
# if not texture_files:
#     raise ValueError("⚠️ Texture folder me koi valid image nahi mila!")

# def get_background(size, texture_index):
#     texture_path = texture_files[texture_index % len(texture_files)]
#     background = Image.open(texture_path).convert("RGB")
#     return background.resize(size)

# # 🖋️ Watermark setup
# watermark_text = "URDUFICTIONBANK.BLOGSPOT.COM"
# # Specify the path to the Arial font file
# font_path = r"C:\Users\PCS\Downloads\Caprasimo-Regular.ttf"  # Path for Arial Bold on Windows
# # Alternatively, if you have the font file in a custom folder, e.g.:
# # font_path = r"E:\SUNB\fonts\arialbd.ttf"

# try:
#     font = ImageFont.truetype(font_path, 20)  # Load Arial Bold font with size 36
# except IOError:
#     print("⚠️ Arial font file not found at specified path! Falling back to default font.")
#     font = ImageFont.load_default()

# def create_vertical_watermark():
#     """Make rotated vertical watermark image."""
#     temp = Image.new("RGBA", (1, 1))
#     d = ImageDraw.Draw(temp)
#     try:
#         bbox = d.textbbox((0, 0), watermark_text, font=font)
#         text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
#     except AttributeError:
#         text_w, text_h = font.getsize(watermark_text)
    
#     text_img = Image.new("RGBA", (text_w + 10, text_h + 10), (0, 0, 0, 0))
#     draw = ImageDraw.Draw(text_img)
#     draw.text((3, 3), watermark_text, font=font, fill=(0, 0, 0, 180))
#     draw.text((0, 0), watermark_text, font=font, fill=(255, 255, 255, 255))
#     return text_img.rotate(270, expand=True)

# # 🔁 Process images
# counter = 1
# for filename in os.listdir(input_folder):
#     if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
#         img_path = os.path.join(input_folder, filename)
#         img = Image.open(img_path).convert("RGB")

#         # Enhance
#         img = ImageEnhance.Color(img).enhance(1.3)
#         img = ImageEnhance.Brightness(img).enhance(1.1)
#         img = ImageEnhance.Contrast(img).enhance(1.2)

#         background = get_background(thumb_size, counter - 1)

#         max_cover_width = int(thumb_width * 0.75)
#         max_cover_height = int(thumb_height * 0.95)
#         img.thumbnail((max_cover_width, max_cover_height), Image.LANCZOS)

#         x = (thumb_width - img.width) // 2
#         y = (thumb_height - img.height) // 2

#         shadow = Image.new("RGBA", img.size, (0, 0, 0, 0))
#         draw = ImageDraw.Draw(shadow)
#         draw.rectangle([0, 0, img.width, img.height], fill=shadow_color)
#         shadow = shadow.filter(ImageFilter.GaussianBlur(blur_radius))

#         composite = background.convert("RGBA")
#         composite.paste(shadow, (x + x_offset, y + y_offset), shadow)
#         composite.paste(img, (x, y))

#         # ✍️ Create and paste watermark relative to cover
#         watermark = create_vertical_watermark()
#         right_margin = 10  # cover se 10px right side par
#         wm_x = x + img.width + right_margin
#         wm_y = (y + img.height // 2) - (watermark.height // 2)

#         # Bounds check (overflow na ho)
#         if wm_x + watermark.width > thumb_width:
#             wm_x = thumb_width - watermark.width - 5

#         composite.alpha_composite(watermark, (wm_x, wm_y))

#         final_image = composite.convert("RGB")
#         custom_name = f"www.urdunovelbanks.com({counter}).webp"
#         output_path = os.path.join(output_folder, custom_name)
#         final_image.save(output_path, format="WEBP", optimize=True, quality=85)

#         counter += 1

# print("✔️ Watermark placed relative to novel cover with Arial font:", output_folder)




















import os
import math
from PIL import Image, ImageEnhance, ImageDraw, ImageFilter, ImageFont

# 📁 Input & Output folders
input_folder = r"E:\SUNB\Writers All Novels\Rabia khan Novels\pngs"
output_folder = os.path.join(input_folder, 'thumbnails_1000x667')
texture_folder = r"E:\SUNB\urdu afsana bank\texture"
os.makedirs(output_folder, exist_ok=True)

# 🎯 Canvas size
thumb_width = 1000
thumb_height = 667
thumb_size = (thumb_width, thumb_height)

# 🌑 Drop shadow settings
angle_degrees = 37
distance = 30
blur_radius = 20
opacity = 128
shadow_color = (0, 0, 0, opacity)
angle_radians = math.radians(angle_degrees)
x_offset = -int(distance * math.cos(angle_radians))
y_offset = int(distance * math.sin(angle_radians))

# 📂 Load texture backgrounds
texture_files = [os.path.join(texture_folder, f) for f in os.listdir(texture_folder)
                 if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
if not texture_files:
    raise ValueError("⚠️ Texture folder me koi valid image nahi mila!")

def get_background(size, texture_index):
    texture_path = texture_files[texture_index % len(texture_files)]
    background = Image.open(texture_path).convert("RGB")
    return background.resize(size)

# 🖋️ Watermark setup
watermark_text = "urdufictionbank.blogspot.com"
# Specify the path to the font file
font_path = r"C:\Users\PCS\Downloads\Agbalumo-Regular.ttf" # Path to your font
try:
    font = ImageFont.truetype(font_path, 25)  # Load font with size 20
except IOError:
    print("⚠️ Font file not found at specified path! Falling back to default font.")
    font = ImageFont.load_default()

def create_vertical_watermark():
    """Make rotated vertical watermark image with solid black text."""
    temp = Image.new("RGBA", (1, 1))
    d = ImageDraw.Draw(temp)
    try:
        bbox = d.textbbox((0, 0), watermark_text, font=font)
        text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    except AttributeError:
        text_w, text_h = font.getsize(watermark_text)
    
    text_img = Image.new("RGBA", (text_w + 10, text_h + 10), (0, 0, 0, 0))
    draw = ImageDraw.Draw(text_img)
    draw.text((0, 0), watermark_text, font=font, fill=(0, 0, 0, 255))  # Solid black text
    return text_img.rotate(270, expand=True)

# 🔁 Process images
counter = 1
for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
        img_path = os.path.join(input_folder, filename)
        img = Image.open(img_path).convert("RGB")

        # Enhance
        img = ImageEnhance.Color(img).enhance(1.3)
        img = ImageEnhance.Brightness(img).enhance(1.1)
        img = ImageEnhance.Contrast(img).enhance(1.2)

        background = get_background(thumb_size, counter - 1)

        max_cover_width = int(thumb_width * 0.75)
        max_cover_height = int(thumb_height * 0.95)
        img.thumbnail((max_cover_width, max_cover_height), Image.LANCZOS)

        x = (thumb_width - img.width) // 2
        y = (thumb_height - img.height) // 2

        shadow = Image.new("RGBA", img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(shadow)
        draw.rectangle([0, 0, img.width, img.height], fill=shadow_color)
        shadow = shadow.filter(ImageFilter.GaussianBlur(blur_radius))

        composite = background.convert("RGBA")
        composite.paste(shadow, (x + x_offset, y + y_offset), shadow)
        composite.paste(img, (x, y))

        # ✍️ Create and paste watermark relative to cover
        watermark = create_vertical_watermark()
        right_margin = 10  # cover se 10px right side par
        wm_x = x + img.width + right_margin
        wm_y = (y + img.height // 2) - (watermark.height // 2)

        # Bounds check (overflow na ho)
        if wm_x + watermark.width > thumb_width:
            wm_x = thumb_width - watermark.width - 5

        composite.alpha_composite(watermark, (wm_x, wm_y))

        final_image = composite.convert("RGB")
        custom_name = f"www.urdunovelbanks.com({counter}).webp"
        output_path = os.path.join(output_folder, custom_name)
        final_image.save(output_path, format="WEBP", optimize=True, quality=85)

        counter += 1

print("✔️ Watermark placed relative to novel cover with solid black text:", output_folder)