import fitz  # PyMuPDF
from fpdf import FPDF
import os

def convert_to_scanned(input_pdf):
    folder = os.path.dirname(input_pdf)
    output_pdf = os.path.join(folder, "scanned_output.pdf")

    doc = fitz.open(input_pdf)
    pdf = FPDF()

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)

        # Render page as image
        pix = page.get_pixmap(dpi=200)
        img_path = os.path.join(folder, f"page_{page_num+1}.jpg")
        pix.save(img_path)

        # Add image into PDF
        pdf.add_page()
        pdf.image(img_path, 0, 0, 210, 297)

        os.remove(img_path)

    pdf.output(output_pdf, "F")
    print(f"✅ Scanned PDF saved: {output_pdf}")


# Run
convert_to_scanned(r"E:\pdf color change\sheeshe-ke-ghar-qurratulain-hyder-ebooks-1.pdf")
