import fitz  # PyMuPDF
from pathlib import Path

# ========================= CONFIGURATION =========================
INPUT_FOLDER = Path(r"C:\Users\PCS\Downloads\Zainab Khan Novels - Copy - Copy (3)")
OUTPUT_FOLDER = INPUT_FOLDER / "Output"
OUTPUT_FOLDER.mkdir(exist_ok=True)

WATERMARK_TEXT = "For more novels Visit: www.urdunovelbanks.com"

# Bottom area kitna check karna hai (pixels mein)
CHECK_HEIGHT = 70           # Neeche se 70 pixels ka area check karega
PIXEL_THRESHOLD = 8000      # Agar itne se zyada black/dark pixels mile to samjho text hai → skip
# (A4 page par 70px height mein 8000-10000 pixels safe value hai, aap apne PDFs ke hisaab se adjust kar sakte hain)
# =================================================================

def has_text_at_bottom(page):
    """Check karega ke page ke neeche already text/footer hai ya nahi"""
    page_height = page.rect.height
    
    # Neeche ka area define karo
    clip_rect = fitz.Rect(0, page_height - CHECK_HEIGHT, page.rect.width, page_height)
    
    # Is area ki image banao (grayscale)
    pix = page.get_pixmap(clip=clip_rect, dpi=150, colorspace=fitz.csGRAY)
    
    # Total dark pixels count karo (threshold 180 se neeche = dark)
    dark_pixels = 0
    for i in range(pix.width * pix.height):
        if pix.pixel(i % pix.width, i // pix.width)[0] < 180:
            dark_pixels += 1
    
    return dark_pixels > PIXEL_THRESHOLD

def add_watermark(pdf_path, output_path):
    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    
    for page_number in range(total_pages):
        # Pehla aur aakhri page hamesha skip (jaise pehle tha)
        if page_number == 0 or page_number == total_pages - 1:
            continue
            
        page = doc[page_number]
        
        # Check karo ke neeche already text/footer hai ya nahi
        if has_text_at_bottom(page):
            print(f"  ↳ Page {page_number + 1} skipped (already has footer text)")
            continue
        
        page_width = page.rect.width
        page_height = page.rect.height

        # Watermark rectangle (bottom se 15-40px ke beech)
        rect = fitz.Rect(0, page_height - 40, page_width, page_height - 10)

        page.insert_textbox(
            rect,
            WATERMARK_TEXT,
            fontsize=12,
            fontname="times-bolditalic",
            color=(0, 0, 0.5),   # Navy blue
            align=1             # Center
        )
        print(f"  ↳ Watermark added on page {page_number + 1}")

    doc.save(output_path, garbage=4, deflate=True)
    doc.close()

def process_folder():
    pdf_files = list(INPUT_FOLDER.glob("*.pdf"))
    if not pdf_files:
        print("Koi PDF file nahi mili folder mein!")
        return
        
    for file in pdf_files:
        output_pdf = OUTPUT_FOLDER / f"{file.stem}_watermarked.pdf"
        print(f"\nProcessing →", file.name)
        add_watermark(str(file), str(output_pdf))

    print("\n🎉 Sab PDFs process ho gaye!")
    print("Output folder:", OUTPUT_FOLDER)

# ======================= RUN =======================
process_folder()