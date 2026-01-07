from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
import io

def create_background_bytes(width, height, color="#d1f0ff"):
    """
    reportlab se ek in-memory single-page PDF banaye jisme specified width/height
    aur fill color ho. Return karta hai io.BytesIO object (seeked to 0).
    """
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=(width, height))
    c.setFillColor(HexColor(color))
    c.rect(0, 0, width, height, fill=1)
    c.save()
    packet.seek(0)
    return packet

def apply_background(input_pdf_path, color, output_pdf_path):
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()

    for page_index, page in enumerate(reader.pages, start=1):
        # Page size in points
        width = float(page.mediabox.width)
        height = float(page.mediabox.height)

        # Background PDF bytes for THIS page size
        bg_bytes_io = create_background_bytes(width, height, color)
        bg_reader = PdfReader(bg_bytes_io)
        bg_page = bg_reader.pages[0]

        # 1) Add background page to writer
        writer.add_page(bg_page)
        # 2) Merge original page ON TOP of that background page
        writer.pages[-1].merge_page(page)

    # Save output
    with open(output_pdf_path, "wb") as fout:
        writer.write(fout)

if __name__ == "__main__":
    input_file = r"E:\pdf color change\sheeshe-ke-ghar-qurratulain-hyder-ebooks-1.pdf"
    output_file = r"E:\pdf color change\sheeshe-ke-ghar-colored.pdf"
    apply_background(input_file, "#d1f0ff", output_file)
    print("✅ Done — saved to:", output_file)
