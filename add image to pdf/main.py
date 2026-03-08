

import os
import pathlib
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4  # not needed but safe
from PIL import Image
import tempfile

def add_cover_to_all_pdfs(folder_path: str):
    folder = pathlib.Path(folder_path)
    
    if not folder.is_dir():
        print(f"❌ Error: Folder nahi mila → {folder_path}")
        return

    # 1. Find the single cover image
    image_extensions = (".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tiff")
    image_files = [f for f in folder.iterdir() if f.suffix.lower() in image_extensions and f.is_file()]
    
    if not image_files:
        print("❌ Error: Koi cover image (PNG/JPG/WebP) nahi mili folder mein.")
        return
    if len(image_files) > 1:
        print(f"⚠️ Warning: Multiple images mili, pehli use kar raha hun: {image_files[0].name}")
    
    image_file = image_files[0]
    print(f"✅ Cover image selected: {image_file.name}")

    # 2. Find all PDFs (ignore temp/output files)
    pdf_files = [f for f in folder.iterdir() 
                 if f.suffix.lower() == ".pdf" 
                 and not f.name.startswith("~") 
                 and "_with_cover" not in f.name]
    
    if not pdf_files:
        print("❌ Error: Koi PDF file nahi mili.")
        return

    print(f"📚 Total PDFs to process: {len(pdf_files)}\n")

    # Use a proper temporary file (better than fixed "temp_image.pdf")
    temp_image_pdf = folder / "temp_cover_adding.pdf"  # we'll delete it safely

    try:
        # Open image once (performance + consistency)
        with Image.open(image_file) as img:
            img_width, img_height = img.size

        for pdf_file in pdf_files:
            print(f"🔄 Processing → {pdf_file.name}", end="")

            try:
                reader = PdfReader(pdf_file)
                if len(reader.pages) == 0:
                    print(" → Skipped (empty PDF)")
                    continue

                first_page = reader.pages[0]
                page_width = float(first_page.mediabox.width)
                page_height = float(first_page.mediabox.height)

                # Create cover page (only once per PDF is fine, but we do it inside loop for safety)
                scale = min(page_width / img_width, page_height / img_height)
                scaled_w = img_width * scale
                scaled_h = img_height * scale

                c = canvas.Canvas(str(temp_image_pdf), pagesize=(page_width, page_height))
                x = (page_width - scaled_w) / 2
                y = (page_height - scaled_h) / 2
                c.drawImage(str(image_file), x, y, width=scaled_w, height=scaled_h, preserveAspectRatio=True)
                c.showPage()
                c.save()

                # Merge: Cover + Original PDF
                writer = PdfWriter()

                # Add cover
                cover_reader = PdfReader(temp_image_pdf)
                writer.add_page(cover_reader.pages[0])

                # Add all original pages
                for page in reader.pages:
                    writer.add_page(page)

                # Write to a temporary output first (safer than direct replace)
                temp_output = pdf_file.with_name(f"{pdf_file.stem}_temp_with_cover.pdf")
                with open(temp_output, "wb") as f:
                    writer.write(f)

                # Now replace original safely
                pdf_file.unlink()                    # delete old
                temp_output.replace(pdf_file)        # rename new → original name

                print(" → ✔ Done")

            except Exception as e:
                print(f" → ❌ Failed: {e}")
                continue

    except Exception as e:
        print(f"❌ Critical error (image open?): {e}")
    finally:
        # Always clean up temp file
        try:
            if temp_image_pdf.exists():
                temp_image_pdf.unlink()
        except:
            pass

    print("\n🎉 Sab kaam khatam! Cover add ho gaya har PDF mein.")

# ============= RUN =============
if __name__ == "__main__":
    # Change this path as needed
    folder_path = r"C:\Users\PCS\Downloads\Lahu se lal Novel - Copy"
    add_cover_to_all_pdfs(folder_path)






