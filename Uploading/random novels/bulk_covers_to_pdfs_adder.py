import os
import shutil
import pathlib
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from PIL import Image

def process_all_pdfs(source_path):
    source_dir = pathlib.Path(source_path)
    
    # 1. Zarori Folders banana
    processed_dir = source_dir / "Processed_PDFs"
    missing_dir = source_dir / "Missing_Images"
    
    processed_dir.mkdir(exist_ok=True)
    missing_dir.mkdir(exist_ok=True)

    # 2. Tamam images ki list pehle hi save kar lena (for fast matching)
    image_extensions = {".png", ".jpg", ".jpeg", ".webp"}
    images_dict = {}
    
    for file in source_dir.iterdir():
        if file.suffix.lower() in image_extensions:
            # Naam ko lowercase karke aur spaces hata kar save karna
            clean_name = file.stem.strip().lower()
            images_dict[clean_name] = file

    print(f"Scanning folder: {source_path}\n")

    # 3. PDF files ko check karna
    for pdf_file in source_dir.glob("*.pdf"):
        # Output folders ko skip karein agar wo source ke andar hain
        if "Processed_PDFs" in str(pdf_file) or "Missing_Images" in str(pdf_file):
            continue

        pdf_stem_clean = pdf_file.stem.strip().lower()
        image_file = images_dict.get(pdf_stem_clean)

        if not image_file:
            # Agar image nahi mili
            print(f"[-] Missing: {pdf_file.name} (Moving to Missing_Images)")
            shutil.move(str(pdf_file), str(missing_dir / pdf_file.name))
        else:
            # Agar image mil gayi
            print(f"[+] Processing: {pdf_file.name}")
            try:
                output_path = processed_dir / pdf_file.name
                update_pdf_cover(pdf_file, image_file, output_path)
                
                # Update ke baad original file ko delete ya move kar sakte hain
                # Agar aap original file source folder mein rehne dena chahte hain to os.remove hataden
                os.remove(pdf_file) 
                print(f"    Done -> Saved in Processed_PDFs")
            except Exception as e:
                print(f"    Error: {e}")

def update_pdf_cover(pdf_path, img_path, output_path):
    reader = PdfReader(str(pdf_path))
    
    # Page size lena (2nd page se, agar ho)
    ref_page = reader.pages[1] if len(reader.pages) > 1 else reader.pages[0]
    page_width = float(ref_page.mediabox.width)
    page_height = float(ref_page.mediabox.height)

    # Temporary Image PDF banana
    temp_pdf = pdf_path.parent / f"temp_{pdf_path.stem}.pdf"
    
    img = Image.open(img_path)
    img_width, img_height = img.size
    scale = min(page_width / img_width, page_height / img_height)
    sw, sh = img_width * scale, img_height * scale

    c = canvas.Canvas(str(temp_pdf), pagesize=(page_width, page_height))
    c.drawImage(str(img_path), (page_width-sw)/2, (page_height-sh)/2, width=sw, height=sh)
    c.showPage()
    c.save()

    # Merge process
    writer = PdfWriter()
    img_reader = PdfReader(str(temp_pdf))
    writer.add_page(img_reader.pages[0])

    for i in range(1, len(reader.pages)):
        writer.add_page(reader.pages[i])

    with open(output_path, "wb") as f:
        writer.write(f)

    # Cleanup temp file
    if temp_pdf.exists():
        os.remove(temp_pdf)

if __name__ == "__main__":
    folder_path = r"E:\unb-workstation\Writers All Novels\Uploadings\random novels - Copy"
    process_all_pdfs(folder_path)