import cv2
import numpy as np
import os
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw, ImageFont

# --- 📁 فولڈرز اور سیٹنگز ---
input_folder = r"E:\git-workstation\unb-automation\Palak Japakhtay Qissay thumbnail Maker\Output"
# یہاں اپنے بیک گراؤنڈ امیج کا مکمل پاتھ لکھیں
background_image_path = r"C:\Users\PCS\Downloads\Untitled design (1) (1).png"
output_folder = os.path.join(input_folder, 'thumbnails_with_watermark')
os.makedirs(output_folder, exist_ok=True)

# تصویر کا رنگ بدلنے کے لیے
content_hex_color = "#FFEFD5" 
# کینوس کا ریفرنس رنگ (ٹیکسٹ کلر ڈیسائیڈ کرنے کے لیے)
reference_bg_color = (245, 230, 205) 

# تھمب نیل سائز
thumb_width, thumb_height = 1200, 800
blur_radius = 25
shadow_opacity = 90
shadow_offset = (15, 15)

# 🖋️ واٹر مارک سیٹنگز
watermark_text = "www.urdunovelbanks.com"
font_path = r"E:\unb-workstation\Writers All Novels\RobotoCondensed-BoldItalic.ttf"

try:
    font = ImageFont.truetype(font_path, 32)
except IOError:
    print("⚠️ Font nahi mila! Default use ho raha hai.")
    font = ImageFont.load_default()

# --- 🛠️ مددگار فنکشنز ---

def hex_to_bgr(hex_str):
    hex_str = hex_str.lstrip('#')
    rgb = tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))
    return np.array([rgb[2], rgb[1], rgb[0]], dtype=np.float32)

def get_best_text_color(bg_color):
    r, g, b = bg_color
    luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    return (0, 0, 0, 255) if luminance > 0.5 else (255, 255, 255, 255)

def create_vertical_watermark(bg_color):
    text_color = get_best_text_color(bg_color)
    temp_img = Image.new("RGBA", (1, 1))
    temp_draw = ImageDraw.Draw(temp_img)
    try:
        bbox = temp_draw.textbbox((0, 0), watermark_text, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    except:
        tw, th = font.getsize(watermark_text)

    padding = 20
    txt_img = Image.new("RGBA", (tw + padding, th + padding), (0, 0, 0, 0))
    d = ImageDraw.Draw(txt_img)
    d.text((padding//2, padding//2), watermark_text, font=font, fill=text_color)
    return txt_img.rotate(90, expand=True)

# --- 🔁 مین پروسیسنگ لوپ ---

def main():
    target_color_bgr = hex_to_bgr(content_hex_color)
    counter = 1

    # چیک کریں کہ بیک گراؤنڈ امیج موجود ہے یا نہیں
    if not os.path.exists(background_image_path):
        print(f"❌ Error: Background image not found at {background_image_path}")
        return

    print("🚀 Processing started using Hardcoded Background...")

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
            img_path = os.path.join(input_folder, filename)
            
            # 1. OpenCV Logic
            cv_img = cv2.imread(img_path)
            if cv_img is None: continue
            
            img_float = cv_img.astype(np.float32) / 255.0
            colored_img = img_float * target_color_bgr
            colored_img = np.clip(colored_img, 0, 255).astype(np.uint8)
            
            img_rgb = cv2.cvtColor(colored_img, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(img_rgb).convert("RGBA")

            # 2. PIL: Thumbnail Design
            pil_img = ImageEnhance.Contrast(pil_img.convert("RGB")).enhance(1.1).convert("RGBA")
            max_h = int(thumb_height * 0.85)
            pil_img.thumbnail((thumb_width, max_h), Image.LANCZOS)

            x = (thumb_width - pil_img.width) // 2
            y = (thumb_height - pil_img.height) // 2

            # Shadow
            shadow_canvas = Image.new("RGBA", (pil_img.width + blur_radius*2, pil_img.height + blur_radius*2), (0,0,0,0))
            ImageDraw.Draw(shadow_canvas).rectangle(
                [blur_radius, blur_radius, pil_img.width + blur_radius, pil_img.height + blur_radius], 
                fill=(0, 0, 0, shadow_opacity)
            )
            shadow_canvas = shadow_canvas.filter(ImageFilter.GaussianBlur(blur_radius))

            # --- 🖼️ ہارڈ کوڈڈ بیک گراؤنڈ لوڈ کرنا ---
            # ہم ہر بار بیک گراؤنڈ لوڈ کر رہے ہیں تاکہ کینوس فریش رہے
            final_thumb = Image.open(background_image_path).convert("RGB")
            final_thumb = final_thumb.resize((thumb_width, thumb_height), Image.LANCZOS)

            # پیسٹ کریں شیڈو اور مین امیج
            final_thumb.paste(shadow_canvas, (x + shadow_offset[0] - blur_radius, y + shadow_offset[1] - blur_radius), shadow_canvas)
            final_thumb.paste(pil_img, (x, y), pil_img)

            # 3. واٹر مارک (Reference color used for text visibility)
            watermark = create_vertical_watermark(reference_bg_color)
            wm_x = x + pil_img.width + 50
            wm_y = y + (pil_img.height - watermark.height) // 2
            
            if wm_x + watermark.width > thumb_width:
                wm_x = thumb_width - watermark.width - 10

            final_thumb.paste(watermark, (wm_x, wm_y), watermark)

            # 4. سیو کرنا
            output_filename = f"www.urdunovelbanks.com({counter}).webp"
            final_thumb.save(os.path.join(output_folder, output_filename), "WEBP", quality=90)
            
            print(f"✅ Generated: {output_filename}")
            counter += 1

    print(f"\n✨ مبارک ہو! تمام {counter-1} تھمب نیلز نئے بیک گراؤنڈ کے ساتھ تیار ہیں۔")

if __name__ == "__main__":
    main()