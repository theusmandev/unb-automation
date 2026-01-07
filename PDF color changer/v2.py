from pdf2image import convert_from_path
from fpdf import FPDF
import os

def convert_to_scanned(input_pdf):
    # Input ka folder aur output path
    folder = os.path.dirname(input_pdf)
    output_pdf = os.path.join(folder, "scanned_output.pdf")

    # Step 1: Convert PDF pages to images
    pages = convert_from_path(input_pdf, dpi=200)  # DPI quality control
    image_files = []

    for i, page in enumerate(pages):
        filename = os.path.join(folder, f"page_{i+1}.jpg")
        page.save(filename, "JPEG")
        image_files.append(filename)

    # Step 2: Create new PDF with images
    pdf = FPDF()
    for img in image_files:
        pdf.add_page()
        pdf.image(img, 0, 0, 210, 297)  # A4 page size

    pdf.output(output_pdf, "F")

    # Step 3: Temp images delete karna (optional)
    for img in image_files:
        os.remove(img)

    print(f"✅ Scanned PDF saved: {output_pdf}")


# === Run ===
convert_to_scanned(r"E:\pdf color change\sheeshe-ke-ghar-qurratulain-hyder-ebooks-1.pdf")
