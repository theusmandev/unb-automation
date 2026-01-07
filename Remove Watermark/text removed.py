# import fitz  # PyMuPDF

# def remove_text_from_pdf(input_pdf, output_pdf, remove_strings):
#     # PDF open karo
#     doc = fitz.open(input_pdf)

#     for page in doc:
#         text_instances = []
#         for s in remove_strings:
#             text_instances.extend(page.search_for(s))  # search text

#         for inst in text_instances:
#             # Draw white rectangle over text
#             page.add_redact_annot(inst, fill=(1, 1, 1))
        
#         # Apply redaction
#         page.apply_redactions()

#     doc.save(output_pdf)
#     doc.close()
#     print("Watermark removed:", output_pdf)


# # Example use
# remove_text_from_pdf(
#     r"C:\Users\PCS\Downloads\sumaira hameed novels\Hayat mumkin hai.pdf",
#     r"C:\Users\PCS\Downloads\sumaira hameed novels\Hayatokokook mumkin hai.pdf",
#     ["digest Novels Lovers group", "❤️❤️"]
# )









# import fitz  # PyMuPDF
# import cv2
# import numpy as np
# from PIL import Image
# import os

# def remove_watermark_image(input_pdf, output_pdf):
#     doc = fitz.open(input_pdf)
#     temp_images = []

#     for page_num in range(len(doc)):
#         # Convert page to image
#         pix = doc[page_num].get_pixmap()
#         img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
#         img_path = f"page_{page_num}.png"
#         img.save(img_path)
#         temp_images.append(img_path)

#         # Load with OpenCV
#         image = cv2.imread(img_path)

#         # ---- Watermark colors detect ----
#         # Blue text
#         lower_blue = np.array([200, 0, 0])
#         upper_blue = np.array([255, 80, 80])

#         # Red hearts
#         lower_red = np.array([0, 0, 200])
#         upper_red = np.array([80, 80, 255])

#         mask_blue = cv2.inRange(image, lower_blue, upper_blue)
#         mask_red = cv2.inRange(image, lower_red, upper_red)

#         # Combine masks
#         mask = cv2.bitwise_or(mask_blue, mask_red)

#         # Remove watermark via inpainting
#         cleaned = cv2.inpaint(image, mask, 3, cv2.INPAINT_TELEA)

#         clean_path = f"cleaned_{page_num}.png"
#         cv2.imwrite(clean_path, cleaned)

#         # Replace original page with cleaned one
#         rect = fitz.Rect(0, 0, pix.width, pix.height)
#         page = doc[page_num]
#         page.clean_contents()
#         page.insert_image(rect, filename=clean_path)

#     # Save final cleaned PDF
#     doc.save(output_pdf)
#     print("✅ Watermark removed →", output_pdf)

#     # Cleanup temporary images
#     for f in temp_images:
#         if os.path.exists(f):
#             os.remove(f)
#         clean_f = f.replace("page_", "cleaned_")
#         if os.path.exists(clean_f):
#             os.remove(clean_f)


# # ---- Run on your two novels ----
# remove_watermark_image(
#     r"C:\Users\PCS\Downloads\sumaira hameed novels\Hayat mumkin hai.pdf",
#     r"C:\Users\PCS\Downloads\sumaira hameed novels\Hayat mumkin hai (Cleaned).pdf"
# )


# import fitz
# import cv2
# import numpy as np
# from PIL import Image
# import os

# def remove_top_watermark(input_pdf, output_pdf, crop_height=150):
#     doc = fitz.open(input_pdf)

#     for page_num in range(len(doc)):
#         # Convert page to image
#         pix = doc[page_num].get_pixmap()
#         img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
#         img_path = f"page_{page_num}.png"
#         img.save(img_path)

#         image = cv2.imread(img_path)

#         # Sirf top ka area select karo
#         h, w, _ = image.shape
#         mask = np.zeros((h, w), dtype=np.uint8)
#         mask[0:crop_height, 0:w] = 255  # top area mask

#         # Inpaint top area
#         cleaned = cv2.inpaint(image, mask, 3, cv2.INPAINT_TELEA)

#         clean_path = f"cleaned_{page_num}.png"
#         cv2.imwrite(clean_path, cleaned)

#         # Replace page with cleaned image
#         rect = fitz.Rect(0, 0, pix.width, pix.height)
#         page = doc[page_num]
#         page.clean_contents()
#         page.insert_image(rect, filename=clean_path)

#         # Cleanup
#         os.remove(img_path)
#         os.remove(clean_path)

#     doc.save(output_pdf)
#     print("✅ Clean PDF saved:", output_pdf)


# # Example run
# remove_top_watermark(
#     r"C:\Users\PCS\Downloads\sumaira hameed novels\Hayat mumkin hai.pdf",
#     r"C:\Users\PCS\Downloads\sumaira hameed novels\Hayat mumkin hai (Cleaned).pdf",
#     crop_height=180   # watermark jitna neeche hota hai us hisaab se adjust karo
# )

















import fitz            # PyMuPDF
import numpy as np
import cv2
from PIL import Image
import os

def remove_colored_watermark(input_pdf, output_pdf, dpi=300,
                             blue_hue=(90, 140),       # HSV hue range for blue
                             red_hue1=(0, 10), red_hue2=(170, 180), # HSV ranges for red
                             sat_thresh=40, val_thresh=40, # min S & V to ignore very pale areas
                             morph_kernel_size=5,
                             inpaint_radius=3):
    """
    input_pdf: path to scanned PDF
    output_pdf: path to save cleaned PDF
    dpi: rendering DPI (300 gives good quality)
    Parameter ranges fine-tune detection.
    """

    doc = fitz.open(input_pdf)
    processed_images = []

    for p in range(len(doc)):
        page = doc[p]
        mat = fitz.Matrix(dpi/72, dpi/72)  # scale for DPI
        pix = page.get_pixmap(matrix=mat, alpha=False)  # RGB
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # PIL -> OpenCV (BGR)
        cv_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        hsv = cv2.cvtColor(cv_img, cv2.COLOR_BGR2HSV)

        # Blue mask
        lower_blue = np.array([blue_hue[0], sat_thresh, val_thresh], dtype=np.uint8)
        upper_blue = np.array([blue_hue[1], 255, 255], dtype=np.uint8)
        mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

        # Red mask (two ranges)
        lower_red1 = np.array([red_hue1[0], sat_thresh, val_thresh], dtype=np.uint8)
        upper_red1 = np.array([red_hue1[1], 255, 255], dtype=np.uint8)
        mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)

        lower_red2 = np.array([red_hue2[0], sat_thresh, val_thresh], dtype=np.uint8)
        upper_red2 = np.array([red_hue2[1], 255, 255], dtype=np.uint8)
        mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)

        mask_red = cv2.bitwise_or(mask_red1, mask_red2)

        # Combine masks
        mask = cv2.bitwise_or(mask_blue, mask_red)

        # Optional: remove small specks: morphological operations
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (morph_kernel_size, morph_kernel_size))
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=1)
        mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel, iterations=1)

        # If mask is empty, skip inpaint
        if cv2.countNonZero(mask) == 0:
            cleaned_bgr = cv_img
        else:
            # Convert mask to 8-bit single channel where nonzero = to inpaint
            inpaint_mask = mask.copy()
            # Inpaint
            cleaned_bgr = cv2.inpaint(cv_img, inpaint_mask, inpaintRadius=inpaint_radius, flags=cv2.INPAINT_TELEA)

            # Optional: slight smoothing to blend
            cleaned_bgr = cv2.fastNlMeansDenoisingColored(cleaned_bgr, None, h=3, hColor=3, templateWindowSize=7, searchWindowSize=21)

        # Convert BGR -> PIL RGB
        cleaned_rgb = cv2.cvtColor(cleaned_bgr, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(cleaned_rgb)

        # Convert to RGB if not already and append
        if pil_img.mode != "RGB":
            pil_img = pil_img.convert("RGB")
        processed_images.append(pil_img)

        print(f"Processed page {p+1}/{len(doc)} - mask pixels: {cv2.countNonZero(mask)}")

    # Save list of PIL images to single PDF
    if not processed_images:
        raise RuntimeError("No pages processed.")
    # Save: first image.save(..., save_all=True, append_images=[...])
    first = processed_images[0]
    rest = processed_images[1:]
    first.save(output_pdf, "PDF", resolution=dpi, save_all=True, append_images=rest)
    print("Saved cleaned PDF to:", output_pdf)


if __name__ == "__main__":
    # Example usage - badal kar apna path do
    in_pdf = r"C:\Users\PCS\Downloads\sumaira hameed novels\Hayat mumkin hai.pdf"

    out_pdf = r"C:\Users\PCS\Downloads\sumaira hameed novels\Hayat mokokooumkin hai.pdf"
    remove_colored_watermark(in_pdf, out_pdf, dpi=300,
                             blue_hue=(85,140),
                             red_hue1=(0,12), red_hue2=(170,180),
                             sat_thresh=50, val_thresh=30,
                             morph_kernel_size=5,
                             inpaint_radius=3)
