import fitz       # PyMuPDF
import cv2
import numpy as np
from PIL import Image
import io
import os

# --- Input & Output Paths ---
input_pdf = r"C:\Users\PCS\Downloads\Kiran digest October 2025.pdf"
output_pdf = r"C:\Users\PCS\Downloads\Kiran digest October 2025okok.pdf"

def page_to_pil_images(input_pdf, dpi=150):
    """Convert PDF pages to PIL Images using PyMuPDF (JPEG-ready)."""
    doc = fitz.open(input_pdf)
    pil_images = []
    for page in doc:
        mat = fitz.Matrix(dpi/72, dpi/72)  # scale factor for DPI
        pix = page.get_pixmap(matrix=mat, alpha=False)
        # Convert to JPEG bytes instead of PNG for lighter size
        img_bytes = pix.tobytes("jpg")  
        img = Image.open(io.BytesIO(img_bytes))
        pil_images.append(img.convert("RGB"))
    doc.close()
    return pil_images

def mask_watermark_by_color_bgr(image_bgr):
    """Detect blue/red watermark areas."""
    hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)

    # Blue text range
    lower_blue = np.array([90, 60, 40])
    upper_blue = np.array([140, 255, 255])
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

    # Red hearts range
    lower_red1 = np.array([0, 80, 40])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 80, 40])
    upper_red2 = np.array([180, 255, 255])
    mask_red = cv2.bitwise_or(cv2.inRange(hsv, lower_red1, upper_red1),
                              cv2.inRange(hsv, lower_red2, upper_red2))

    mask = cv2.bitwise_or(mask_blue, mask_red)

    # Morphological clean-up
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11,11))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
    mask = cv2.dilate(mask, kernel, iterations=1)

    return mask

def inpaint_image(image_pil, mask):
    """Remove watermark using OpenCV inpainting."""
    img = np.array(image_pil)[:, :, ::-1].copy()  # RGB->BGR
    mask = mask.astype(np.uint8)
    inpainted = cv2.inpaint(img, mask, inpaintRadius=3, flags=cv2.INPAINT_TELEA)
    return Image.fromarray(inpainted[:, :, ::-1])  # back to PIL RGB

def process_pdf(input_pdf, output_pdf, dpi=150, jpeg_quality=70):
    print(f"Processing PDF:\n{input_pdf}\n")
    images = page_to_pil_images(input_pdf, dpi=dpi)
    cleaned_images = []

    for i, img in enumerate(images):
        print(f"➡️ Cleaning page {i+1}/{len(images)} ...")
        img_bgr = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        mask = mask_watermark_by_color_bgr(img_bgr)
        if cv2.countNonZero(mask) < 50:
            print("   No watermark detected on this page.")
            cleaned_images.append(img)
            continue
        cleaned = inpaint_image(img, mask)
        cleaned_images.append(cleaned)

    # Save final compressed PDF (JPEG-based)
    cleaned_images[0].save(
        output_pdf,
        save_all=True,
        append_images=cleaned_images[1:],
        quality=jpeg_quality,
        optimize=True
    )
    print(f"\n✅ Clean & compressed PDF saved to:\n{output_pdf}")

# --- Run ---
if os.path.exists(input_pdf):
    process_pdf(input_pdf, output_pdf, dpi=250, jpeg_quality=90)
else:
    print("❌ Input PDF not found at:", input_pdf)
