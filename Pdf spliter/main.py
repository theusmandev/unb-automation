import os
from pypdf import PdfReader, PdfWriter
from pathlib import Path

# ===============================
# SETTINGS
# ===============================
PDF_PATH = r"E:\unb-workstation\Writers All Novels\workstation\Munam Malik Novels\Namkeen Panion Ka Safar By Munam Malik.pdf"
OUTPUT_FOLDER = r"E:\unb-workstation\Writers All Novels\workstation\Munam Malik Novels\New folder (3)"
TOTAL_PARTS = 2               # Change karna ho to yahan badlo

# ===============================
# VALIDATION + PROGRAM
# ===============================
if not Path(PDF_PATH).is_file():
    print(f"Error: File not found → {PDF_PATH}")
    exit(1)

if TOTAL_PARTS < 2:
    print("Error: TOTAL_PARTS kam se kam 2 hona chahiye!")
    exit(1)

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

reader = PdfReader(PDF_PATH)
total_pages = len(reader.pages)

print(f"Total pages: {total_pages}")
print(f"Splitting into {TOTAL_PARTS} parts...\n")

pages_per_part = total_pages // TOTAL_PARTS
extra_pages = total_pages % TOTAL_PARTS

base_name = Path(PDF_PATH).stem   # better than os.path.splitext

start_page = 0

for part in range(1, TOTAL_PARTS + 1):
    writer = PdfWriter()

    end_page = start_page + pages_per_part + (1 if part <= extra_pages else 0)

    # Safety check
    end_page = min(end_page, total_pages)

    for page_num in range(start_page, end_page):
        writer.add_page(reader.pages[page_num])

    output_path = Path(OUTPUT_FOLDER) / f"{base_name}_part{part}.pdf"

    with open(output_path, "wb") as f:
        writer.write(f)

    pages_in_this_part = end_page - start_page
    print(f"Part {part:2d} → pages {start_page+1:4d} – {end_page:4d}  ({pages_in_this_part} pages) → {output_path.name}")

    start_page = end_page

print("\n" + "═" * 60)
print("✓ Done! PDF successfully split into parts!")
print("═" * 60)