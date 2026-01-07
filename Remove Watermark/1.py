import fitz  # PyMuPDF
from PIL import Image
import io

def rasterize_pdf(input_pdf, output_pdf):
    doc = fitz.open(input_pdf)
    images = []

    for page in doc:
        pix = page.get_pixmap(dpi=200)
        img = Image.open(io.BytesIO(pix.tobytes("png")))
        images.append(img.convert("RGB"))

    images[0].save(output_pdf, save_all=True, append_images=images[1:])

rasterize_pdf("input.pdf", "output_clean.pdf")
