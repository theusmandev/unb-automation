import fitz  # PyMuPDF
from pathlib import Path

# Hard-coded paths
INPUT_FOLDER = Path(r"C:\Users\PCS\Downloads\Zainab Khan Novels - Copy")
OUTPUT_FOLDER = INPUT_FOLDER / "Output"
OUTPUT_FOLDER.mkdir(exist_ok=True)

WATERMARK_TEXT = "For more novels Visit: www.urdunovelbanks.com"


def add_watermark(pdf_path, output_path):
    doc = fitz.open(pdf_path)
    total_pages = len(doc)

    for page_number in range(total_pages):

        # Skip first & last page
        if page_number == 0 or page_number == total_pages - 1:
            continue

        page = doc[page_number]
        w = page.rect.width
        h = page.rect.height

        # --------------------------------------------
        # LEFT SIDE VERTICAL WATERMARK (ROTATE = 90°)
        # --------------------------------------------
        rect = fitz.Rect(
            10,         # x1 (near left edge)
            h * 0.20,   # y1
            40,         # x2
            h * 0.80    # y2
        )

        page.insert_textbox(
            rect,
            WATERMARK_TEXT,
            fontsize=12,
            fontname="times-bolditalic",
            color=(0, 0, 0.5),
            rotate=90,     # vertical text
            align=1        # center align
        )

    doc.save(output_path)
    doc.close()


def process_folder():
    for file in INPUT_FOLDER.iterdir():
        if file.suffix.lower() == ".pdf":
            output_pdf = OUTPUT_FOLDER / f"{file.stem}_watermarked.pdf"
            print(f"Processing: {file.name}")
            add_watermark(str(file), str(output_pdf))

    print("\nDone! Watermarked PDFs saved in:")
    print(OUTPUT_FOLDER)


process_folder()
