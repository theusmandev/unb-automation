import fitz  # PyMuPDF
from PIL import Image, ImageOps
from fpdf import FPDF
import os

def change_pdf_background(input_pdf, bg_color=(255, 255, 200)):  # light yellow
    folder = os.path.dirname(input_pdf)
    base_name = os.path.splitext(os.path.basename(input_pdf))[0]
    output_pdf = os.path.join(folder, f"{base_name}_bgchanged.pdf")

    doc = fitz.open(input_pdf)
    pdf = FPDF()

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)

        # Render page
        pix = page.get_pixmap(dpi=200)
        img_path = os.path.join(folder, f"page_{page_num+1}.png")
        pix.save(img_path)

        # Open in Pillow
        img = Image.open(img_path).convert("RGBA")

        # Make background color image
        bg = Image.new("RGBA", img.size, bg_color)

        # Paste PDF page on background
        bg.paste(img, (0, 0), img)

        # Save new image
        bg_path = os.path.join(folder, f"bg_{page_num+1}.jpg")
        bg.convert("RGB").save(bg_path, "JPEG", quality=90)

        # Add to PDF
        pdf.add_page()
        pdf.image(bg_path, 0, 0, 210, 297)

        # Cleanup
        os.remove(img_path)
        os.remove(bg_path)

    pdf.output(output_pdf, "F")
    print(f"✅ Background changed PDF saved: {output_pdf}")


# Run
change_pdf_background(r"E:\pdf color change\sheeshe-ke-ghar-qurratulain-hyder-ebooks-1.pdf", bg_color=(230, 255, 230))  # light green
