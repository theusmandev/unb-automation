import fitz       # PyMuPDF
import cv2
import numpy as np
from PIL import Image
import io
import os

# --- Input & Output Paths ---
input_pdf = r"C:\Users\PCS\Downloads\Kiran digest October 2025.pdf"
output_pdf = r"C:\Users\PCS\Downloads\Kiran digest October 2025okok.pdf"

def page_to_pil_images(input_pdf, dpi=200):
    """Convert PDF pages to PIL Images using PyMuPDF."""
    doc = fitz.open(input_pdf)
    pil_images = []
    for page in doc:
        mat = fitz.Matrix(dpi/72, dpi/72)  # scale
        pix = page.get_pixmap(matrix=mat, alpha=False)
        img = Image.open(io.BytesIO(pix.tobytes("png")))
        pil_images.append(img.convert("RGB"))
    doc.close()
    return pil_images

def mask_watermark_by_color_bgr(image_bgr):
    """
    Create mask for likely watermark regions by HSV thresholds for blue (text)
    and red (hearts). Returns combined binary mask (uint8, 0/255).
    """
    hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)

    # --- Blue text threshold (tune if necessary) ---
    lower_blue = np.array([90, 60, 40])
    upper_blue = np.array([140, 255, 255])
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

    # --- Red hearts threshold (two ranges because red wraps hue) ---
    lower_red1 = np.array([0, 80, 40])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 80, 40])
    upper_red2 = np.array([180, 255, 255])
    mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask_red = cv2.bitwise_or(mask_red1, mask_red2)

    # Combine masks
    mask = cv2.bitwise_or(mask_blue, mask_red)

    # Clean up small holes and expand slightly
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11,11))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
    mask = cv2.dilate(mask, kernel, iterations=1)

    return mask

def inpaint_image(image_pil, mask):
    """Apply OpenCV inpainting on image (PIL->BGR -> inpaint -> PIL)."""
    img = np.array(image_pil)[:, :, ::-1].copy()  # RGB->BGR
    if mask.dtype != np.uint8:
        mask = mask.astype(np.uint8)
    inpainted = cv2.inpaint(img, mask, inpaintRadius=3, flags=cv2.INPAINT_TELEA)
    result = Image.fromarray(inpainted[:, :, ::-1])
    return result

def process_pdf(input_pdf, output_pdf, dpi=200):
    print(f"Processing PDF:\n{input_pdf}\n")
    images = page_to_pil_images(input_pdf, dpi=dpi)
    cleaned_images = []
    for i, img in enumerate(images):
        print(f"➡️  Cleaning page {i+1}/{len(images)} ...")
        img_bgr = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        mask = mask_watermark_by_color_bgr(img_bgr)
        if cv2.countNonZero(mask) < 50:
            print("   No visible watermark detected on this page.")
            cleaned_images.append(img)
            continue
        cleaned = inpaint_image(img, mask)
        cleaned_images.append(cleaned)

    cleaned_images[0].save(output_pdf, save_all=True, append_images=cleaned_images[1:], quality=95)
    print(f"\n✅ Clean PDF saved to:\n{output_pdf}")

# --- Run the cleaner ---
if os.path.exists(input_pdf):
    process_pdf(input_pdf, output_pdf, dpi=200)
else:
    print("❌ Input PDF not found at:", input_pdf)
