import fitz  # PyMuPDF
from pathlib import Path
import traceback

# Hard-coded paths
INPUT_FOLDER = Path(r"E:\unb-workstation\Writers All Novels\workstation\Fatima Malik Novels")
OUTPUT_FOLDER = INPUT_FOLDER / "Output"
OUTPUT_FOLDER.mkdir(exist_ok=True)

# Watermark text
WATERMARK_TEXT = "For more novels Visit: www. urdunovelbanks.com"

def add_watermark(pdf_path, output_path):
    # Open with checks for broken files
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        raise ValueError(f"Could not open file: {e}")

    total_pages = len(doc)

    for page_number in range(total_pages):
        # Skip first & last page
        if page_number == 0 or page_number == total_pages - 1:
            continue

        page = doc[page_number]
        w = page.rect.width
        h = page.rect.height

        # LEFT SIDE VERTICAL WATERMARK
        rect = fitz.Rect(
            3,          # x1
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
            rotate=90,
            align=1
        )

    # Garbage=4 attempts to defragment/repair structure before saving
    doc.save(output_path, garbage=4, deflate=True)
    doc.close()

def process_folder():
    success_count = 0
    error_count = 0
    errors = []

    print(f"Starting processing in: {INPUT_FOLDER}\n")

    for file in INPUT_FOLDER.iterdir():
        if file.suffix.lower() == ".pdf":
            # Skip the output folder if it's inside the input folder
            if file.parent.name == "Output":
                continue

            output_pdf = OUTPUT_FOLDER / file.name
            print(f"Processing: {file.name}...", end=" ")

            try:
                add_watermark(str(file), str(output_pdf))
                print("DONE")
                success_count += 1
            except Exception as e:
                print("FAILED")
                print(f"  >>> Error: {e}")
                error_count += 1
                errors.append(file.name)

    print("\n" + "="*30)
    print("SUMMARY")
    print("="*30)
    print(f"Successfully processed: {success_count}")
    print(f"Failed: {error_count}")
    
    if errors:
        print("\nThe following files are corrupt and need manual checking:")
        for err_file in errors:
            print(f"- {err_file}")
    
    print(f"\nWatermarked PDFs saved in: {OUTPUT_FOLDER}")

if __name__ == "__main__":
    process_folder()

# # output pdfs with same titles

# import fitz  # PyMuPDF
# from pathlib import Path

# # Hard-coded paths
# INPUT_FOLDER = Path(r"E:\unb-workstation\Writers All Novels\Rahat Jabeen Novels")
# OUTPUT_FOLDER = INPUT_FOLDER / "Output"
# OUTPUT_FOLDER.mkdir(exist_ok=True)

# # Watermark text (plain text, non-clickable)
# WATERMARK_TEXT = "For more novels Visit: www. urdunovelbanks.com"


# def add_watermark(pdf_path, output_path):
#     doc = fitz.open(pdf_path)
#     total_pages = len(doc)

#     for page_number in range(total_pages):

#         # Skip first & last page
#         if page_number == 0 or page_number == total_pages - 1:
#             continue

#         page = doc[page_number]
#         w = page.rect.width
#         h = page.rect.height

#         # LEFT SIDE VERTICAL WATERMARK
#         rect = fitz.Rect(
#             3,          # x1 (left side)
#             h * 0.20,   # y1
#             40,         # x2
#             h * 0.80    # y2
#         )

#         page.insert_textbox(
#             rect,
#             WATERMARK_TEXT,
#             fontsize=12,
#             fontname="times-bolditalic",
#             color=(0, 0, 0.5),
#             rotate=90,
#             align=1
#         )

#     doc.save(output_path)
#     doc.close()


# def process_folder():
#     for file in INPUT_FOLDER.iterdir():
#         if file.suffix.lower() == ".pdf":

#             # SAME FILE NAME IN OUTPUT
#             output_pdf = OUTPUT_FOLDER / file.name

#             print(f"Processing: {file.name}")
#             add_watermark(str(file), str(output_pdf))

#     print("\nDone! Watermarked PDFs saved in:")
#     print(OUTPUT_FOLDER)


# process_folder()


#clickable link of urdunovelbank and with output watermark added in the end of output titles


# import fitz  # PyMuPDF
# from pathlib import Path

# # Hard-coded paths
# INPUT_FOLDER = Path(r"E:\unb-workstation\Writers All Novels\Farzana Kharal Novels - Copy")
# OUTPUT_FOLDER = INPUT_FOLDER / "Output"
# OUTPUT_FOLDER.mkdir(exist_ok=True)

# WATERMARK_TEXT = "For more novels Visit: www.urdunovelbanks.com"


# def add_watermark(pdf_path, output_path):
#     doc = fitz.open(pdf_path)
#     total_pages = len(doc)

#     for page_number in range(total_pages):

#         # Skip first & last page
#         if page_number == 0 or page_number == total_pages - 1:
#             continue

#         page = doc[page_number]
#         w = page.rect.width
#         h = page.rect.height

#         # --------------------------------------------
#         # LEFT SIDE VERTICAL WATERMARK (ROTATE = 90°)
#         # --------------------------------------------
#         rect = fitz.Rect(
#             3,         # x1 (near left edge)
#             h * 0.20,   # y1
#             40,         # x2
#             h * 0.80    # y2
#         )

#         page.insert_textbox(
#             rect,
#             WATERMARK_TEXT,
#             fontsize=12,
#             fontname="times-bolditalic",
#             color=(0, 0, 0.5),
#             rotate=90,     # vertical text
#             align=1        # center align
#         )

#     doc.save(output_path)
#     doc.close()


# def process_folder():
#     for file in INPUT_FOLDER.iterdir():
#         if file.suffix.lower() == ".pdf":
#             output_pdf = OUTPUT_FOLDER / f"{file.stem}_watermarked.pdf"
#             print(f"Processing: {file.name}")
#             add_watermark(str(file), str(output_pdf))

#     print("\nDone! Watermarked PDFs saved in:")
#     print(OUTPUT_FOLDER)


# process_folder()
