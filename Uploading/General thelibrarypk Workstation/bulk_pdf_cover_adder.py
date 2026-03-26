import os
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from PIL import Image
import pathlib

def process_all_novels(folder_path):
    folder = pathlib.Path(folder_path)
    if not folder.is_dir():
        print(f"Error: {folder_path} sahi folder path nahi hai.")
        return

    pdf_files = [f for f in folder.iterdir() if f.suffix.lower() == ".pdf"]
    
    if not pdf_files:
        print("Folder mein koi PDF nahi mili.")
        return

    # Tracking ke liye lists
    success_list = []
    skipped_list = []
    error_list = []

    print(f"--- Processing {len(pdf_files)} PDFs ---\n")

    for pdf_file in pdf_files:
        image_extensions = (".png", ".jpg", ".jpeg", ".webp")
        image_file = None
        
        # Matching image dhoondna (same name as PDF)
        for ext in image_extensions:
            temp_img_path = folder / (pdf_file.stem + ext)
            if temp_img_path.exists():
                image_file = temp_img_path
                break
        
        if not image_file:
            skipped_list.append(pdf_file.name)
            continue

        temp_image_pdf = folder / f"temp_{pdf_file.stem}.pdf"

        try:
            # 1. Original PDF open karein aur size check karein
            reader = PdfReader(str(pdf_file))
            first_page = reader.pages[0]
            page_width = float(first_page.mediabox.width)
            page_height = float(first_page.mediabox.height)

            # 2. Image ko usi size ke PDF page mein convert karein
            img = Image.open(image_file)
            img_width, img_height = img.size
            scale = min(page_width / img_width, page_height / img_height)
            scaled_width = img_width * scale
            scaled_height = img_height * scale

            c = canvas.Canvas(str(temp_image_pdf), pagesize=(page_width, page_height))
            x_offset = (page_width - scaled_width) / 2
            y_offset = (page_height - scaled_height) / 2
            c.drawImage(str(image_file), x_offset, y_offset, width=scaled_width, height=scaled_height)
            c.showPage()
            c.save()

            # 3. Naya PDF merge karein
            writer = PdfWriter()
            
            # Pehle naya image wala page add karein
            img_reader = PdfReader(str(temp_image_pdf))
            writer.add_page(img_reader.pages[0])

            # Ab original PDF ke SARE pages (0 se end tak) add karein
            for page in reader.pages: 
                writer.add_page(page)

            # Original file ko update karein
            with open(pdf_file, "wb") as f:
                writer.write(f)

            success_list.append(pdf_file.name)
            print(f"[SUCCESS] {pdf_file.name}")

        except Exception as e:
            error_list.append(f"{pdf_file.name} (Error: {str(e)})")
            print(f"[ERROR] {pdf_file.name}")
        
        finally:
            if temp_image_pdf.exists():
                try:
                    os.remove(temp_image_pdf)
                except:
                    pass

    # --- Final Summary Report ---
    print("\n" + "="*40)
    print("📌 FINAL PROCESSING SUMMARY")
    print("="*40)
    print(f"✅ Total Successful: {len(success_list)}")
    print(f"⏭️  Total Skipped (No Image): {len(skipped_list)}")
    print(f"❌ Total Errors: {len(error_list)}")
    
    if skipped_list:
        print("\n📂 FILES SKIPPED (Images not found):")
        for item in skipped_list:
            print(f"  - {item}")

    if error_list:
        print("\n⚠️  FILES WITH ERRORS:")
        for item in error_list:
            print(f"  - {item}")
    
    print("\n" + "="*40)

if __name__ == "__main__":
    # Apne folder ka path yahan change karein
    path = r"E:\unb-workstation\Writers All Novels\Uploadings\General thelibrarypk Workstation\Asia Mirza - Copy\New folder (2)"
    process_all_novels(path)