import fitz  # PyMuPDF
import os

def pdf_page_to_png(pdf_path, page_number=1):
    # Get Downloads folder path
    downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")

    # Extract PDF file name (without extension)
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]

    # Output image path (same name as PDF)
    output_name = f"{pdf_name}.png"
    output_path = os.path.join(downloads_folder, output_name)

    # Open PDF and extract page
    doc = fitz.open(pdf_path)
    page = doc[page_number - 1]  # 0-based index
    pix = page.get_pixmap()
    pix.save(output_path)

    print(f"✅ Page {page_number} from '{pdf_path}' saved as '{output_path}'")

# ------------------------------
# FUNCTION CALL (IMPORTANT)
# ------------------------------

pdf_file = r"E:\unb-workstation\Writers All Novels\workstation\alia bukhari novel\ok\replace"
pdf_page_to_png(pdf_file)   # <-- ye call zaroor honi chahiye

