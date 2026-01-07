import fitz  # PyMuPDF
from PIL import Image, ImageEnhance
from fpdf import FPDF
import os

def convert_to_scanned(input_pdf):
    folder = os.path.dirname(input_pdf)
    base_name = os.path.splitext(os.path.basename(input_pdf))[0]
    output_pdf = os.path.join(folder, f"{base_name}_scanned.pdf")

    doc = fitz.open(input_pdf)
    pdf = FPDF()

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)

        # Render page to image
        pix = page.get_pixmap(dpi=200)
        img_path = os.path.join(folder, f"page_{page_num+1}.jpg")
        pix.save(img_path)

        # Open image with Pillow
        img = Image.open(img_path).convert("L")  # grayscale
        # Enhance contrast
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.5)
        # Brightness thoda adjust
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(1.2)

        # Save back
        img.save(img_path, "JPEG", quality=70)

        # Add image in PDF
        pdf.add_page()
        pdf.image(img_path, 0, 0, 210, 297)

        os.remove(img_path)  # cleanup

    pdf.output(output_pdf, "F")
    print(f"✅ Scanner-style PDF saved: {output_pdf}")


# Run
convert_to_scanned(r"C:\Users\PCS\Downloads\main abdul qadir hun by sarwat nazir.pdf")
