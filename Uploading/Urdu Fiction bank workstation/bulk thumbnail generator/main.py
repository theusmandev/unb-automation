import os
import math
from PIL import Image, ImageEnhance, ImageDraw, ImageFilter, ImageFont, ImageOps

# ────────────────────────────────────────────────
#             Configuration & Folders
# ────────────────────────────────────────────────
input_folder = r"E:\unb-workstation\Writers All Novels\pngs"
output_folder = os.path.join(input_folder, 'thumbnails_1200x800_studio')
os.makedirs(output_folder, exist_ok=True)

for f in os.listdir(output_folder):
    file_path = os.path.join(output_folder, f)
    if os.path.isfile(file_path) and not f.lower().endswith('.webp'):
        os.remove(file_path)

thumb_width = 1200
thumb_height = 800
thumb_size = (thumb_width, thumb_height)

# Studio Shadow Settings
blur_radius = 40
opacity = 140
shadow_color = (0, 0, 0, opacity)
x_offset = 0
y_offset = 25  # Straight downward shadow

# Watermark Settings (Spaced out for premium look)
watermark_text = "W W W . U R D U N O V E L B A N K S . C O M"
font_path = r"E:\git-workstation\unb-automation\Bulk Thumbnail maker\RobotoCondensed-BoldItalic.ttf"

try:
    font = ImageFont.truetype(font_path, 20) # Smaller font
except IOError:
    font = ImageFont.load_default()

# ────────────────────────────────────────────────
#             Helper Functions
# ────────────────────────────────────────────────

def get_dominant_colors(image):
    """Extracts dominant top and bottom colors for the gradient."""
    # Resize to 1x2 to quickly get the average top and bottom colors
    small = image.resize((1, 2), Image.Resampling.LANCZOS)
    top_color = small.getpixel((0, 0))
    bottom_color = small.getpixel((0, 1))
    
    # Slightly darken the colors so the bright cover pops more
    top_color = tuple(int(c * 0.7) for c in top_color[:3])
    bottom_color = tuple(int(c * 0.5) for c in bottom_color[:3])
    return top_color, bottom_color

def create_gradient(width, height, color1, color2):
    """Creates a smooth vertical gradient."""
    gradient = Image.new('RGB', (1, 256))
    draw = ImageDraw.Draw(gradient)
    for i in range(256):
        r = int(color1[0] + (color2[0] - color1[0]) * i / 255)
        g = int(color1[1] + (color2[1] - color1[1]) * i / 255)
        b = int(color1[2] + (color2[2] - color1[2]) * i / 255)
        draw.line([(0, i), (0, i)], fill=(r, g, b))
    
    return gradient.resize((width, height), Image.Resampling.BICUBIC)

def add_white_border(im, border_width=4):
    """Adds a crisp white border around the cover."""
    bordered = Image.new("RGB", (im.width + border_width*2, im.height + border_width*2), (255, 255, 255))
    bordered.paste(im, (border_width, border_width))
    return bordered

# ────────────────────────────────────────────────
#             Main Processing Loop
# ────────────────────────────────────────────────

counter = 0

for filename in os.listdir(input_folder):
    if not filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
        continue
        
    img_path = os.path.join(input_folder, filename)
    try:
        img = Image.open(img_path).convert("RGB")
    except Exception:
        continue

    counter += 1

    # 1. Subtle Enhancements
    img = ImageEnhance.Color(img).enhance(1.1)
    img = ImageEnhance.Contrast(img).enhance(1.05)

    # 2. Extract Colors & Create Gradient Background
    top_col, bot_col = get_dominant_colors(img)
    background = create_gradient(thumb_width, thumb_height, top_col, bot_col)
    composite = background.convert("RGBA")

    # 3. Process Main Cover (Resize & Add Border)
    max_cover_width = int(thumb_width * 0.42)
    max_cover_height = int(thumb_height * 0.82)
    img.thumbnail((max_cover_width, max_cover_height), Image.Resampling.LANCZOS)
    
    img_with_border = add_white_border(img, border_width=5)

    # Center position for Cover
    x = (thumb_width - img_with_border.width) // 2
    # Move it slightly up to leave room for the watermark at the bottom
    y = ((thumb_height - img_with_border.height) // 2) - 15 

    # 4. Generate Soft Floating Shadow
    shadow = Image.new("RGBA", composite.size, (0, 0, 0, 0))
    draw_shadow = ImageDraw.Draw(shadow)
    
    # Shadow is smaller than the book to give a floating effect
    draw_shadow.rectangle(
        [x + 15, y + 20, x + img_with_border.width - 15, y + img_with_border.height - 5], 
        fill=shadow_color
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(blur_radius))

    # 5. Composite Layers
    composite.alpha_composite(shadow)
    composite.paste(img_with_border, (x, y))

    # 6. Add Centered Horizontal Watermark
    try:
        bbox = font.getbbox(watermark_text)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
    except AttributeError:
        text_w, text_h = font.getsize(watermark_text)

    # Semi-transparent white
    text_color = (255, 255, 255, 140)
    
    wm_x = (thumb_width - text_w) // 2
    wm_y = thumb_height - text_h - 25 # 25 pixels from the bottom

    draw_composite = ImageDraw.Draw(composite)
    draw_composite.text((wm_x, wm_y), watermark_text, font=font, fill=text_color)

    # 7. Save
    final_image = composite.convert("RGB")
    base_name = os.path.splitext(filename)[0]
    output_filename = f"{base_name}_(www.urdunovelbanks.com).webp"
    output_path = os.path.join(output_folder, output_filename)
    
    final_image.save(output_path, format="WEBP", optimize=True, quality=92)
    print(f"Generated: {output_filename}")

print(f"\nDone! Total {counter} Studio-Style thumbnails ban gaye.")